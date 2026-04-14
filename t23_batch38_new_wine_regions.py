import psycopg2

conn = psycopg2.connect("postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable")
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === LODI AVA (USA) ===
print("\n=== Lodi AVA (USA) ===")
r_lodi = R(
    name="Lodi",
    country="USA",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Lodi AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="California's most important appellation for old-vine Zinfandel, centred on the Sacramento-San Joaquin Delta east of San Francisco Bay. Lodi's unique combination of warm days, cool Delta breezes from San Francisco Bay, and deep, sandy-loam soils has allowed Zinfandel vines planted by Italian immigrants in the early 20th century to survive — some are over 120 years old. These pre-Prohibition plantings, many on their original roots, produce wines of extraordinary concentration and complexity. The appellation also grows excellent Petite Sirah, Cinsault, and Albariño from its diverse climate sub-zones.",
    key_producers="Turley Wine Cellars, Bokisch Vineyards, McCay Cellars, Michael-David Winery",
    historical_context="Italian immigrants — primarily from Piedmont and Tuscany — planted Zinfandel throughout the Sacramento Delta in the late 19th and early 20th centuries, producing wine for Italian-American communities in San Francisco. Prohibition (1920–1933) devastated many wineries but preserving the vines as 'table grape' and 'juice grape' producers saved the old plantings. The post-Prohibition renaissance saw these ancient vines recognised as a treasure — Lodi now protects its Heritage Vine programme for vines over 50 years old."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Excellent growing season with Delta cooling providing unusual freshness. Old-vine Zinfandel of extraordinary complexity."),
    (2020, "very_good", "stable", "Good vintage despite some wildfire smoke impact. Old-vine concentration preserved through the heat."),
    (2019, "excellent", "rising", "Outstanding vintage — long, warm season with cool nights preserving acidity. Benchmark old-vine Zinfandel."),
    (2018, "very_good", "stable", "Classic Lodi vintage with excellent old-vine concentration and ripe berry character."),
    (2017, "excellent", "stable", "One of the decade's finest. Old-vine Zinfandel of remarkable depth and freshness."),
]:
    VIN(r_lodi, yr, qd, pt, sn)

p_turley = P(
    name="Turley Wine Cellars",
    country="USA",
    region_id=r_lodi,
    producer_type="winery",
    description="California's most dedicated and celebrated old-vine Zinfandel specialist, producing vineyard-designate wines from ancient plantings across Lodi, Napa, Amador County, and the Sierra Foothills. Founded by Larry Turley in 1993, the winery farms only old-vine Zinfandel and Petite Sirah — some vines over 120 years old — using minimal intervention and whole-cluster fermentation. Turley's 40+ vineyard designates represent a comprehensive documentation of California's old-vine heritage."
)
prod_turley, new = PROD(
    name="Turley Dogtown Vineyard Old Vines Zinfandel Lodi",
    category="wine_still",
    subcategory="Zinfandel",
    producer_id=p_turley,
    region_id=r_lodi,
    origin_country="USA",
    description="From the Dogtown Vineyard — ancient head-trained Zinfandel vines planted in 1905 on the sandy Delta soils of southern Lodi. The wine shows what century-old Zinfandel achieves on deep sand: incredible concentration without heaviness, black cherry, bramble, dried herbs, coffee, vanilla spice, and an earthy complexity rarely found in Californian wine. Despite the 16%+ alcohol typical of old-vine Lodi, the wine's fresh acidity from the Delta breeze gives genuine balance and aging potential.",
    price_tier="premium"
)
if new:
    PAIR(prod_turley, "Barbecued beef brisket with tangy tomato sauce and coleslaw", "complement", "classic", "main", "American BBQ and Zinfandel is one of California's great food and wine pairings — the wine's jammy fruit and spice complement the smoky, sweet brisket while its freshness cuts through the fat.")
    PAIR(prod_turley, "Grilled lamb chops with rosemary, garlic, and chimichurri", "complement", "established", "main", "Old-vine Zinfandel's depth and herbaceous notes are ideal for lamb. Rosemary echoes its dried herb character while chimichurri adds freshness that the wine's acidity can bridge.")
    PAIR(prod_turley, "Spicy Italian sausage pizza with fennel, pepperoni, and San Marzano", "complement", "classic", "main", "Zinfandel — descended from Southern Italian Primitivo — with Italian-American pizza is a natural pairing. Spice echoes the wine's pepper, fennel bridges its anise notes, and tomato mirrors its acidity.")
    PAIR(prod_turley, "Aged dry Jack cheese with fig jam and walnuts", "complement", "established", "cheese", "California aged cow's milk cheese with California's signature grape — dry Jack's sharp, nutty character complements Zinfandel's jammy fruit. Fig jam echoes its dark fruit while walnuts bridge its earthy depth.")

p_bokisch = P(
    name="Bokisch Vineyards",
    country="USA",
    region_id=r_lodi,
    producer_type="winery",
    description="The most innovative estate in Lodi — Markus and Liz Bokisch's organic and Biodynamic property focused on Spanish and Portuguese varieties in Lodi's most diverse micro-climates. The estate has pioneered Albariño, Garnacha, Tempranillo, and Verdelho in Lodi, demonstrating that the appellation's versatility extends far beyond Zinfandel. Bokisch's Terra Alta Albariño and Las Cerezas Old Vine Garnacha are considered among California's finest expressions of these varieties."
)
prod_bokisch, new = PROD(
    name="Bokisch Las Cerezas Old Vine Garnacha Lodi",
    category="wine_still",
    subcategory="Garnacha",
    producer_id=p_bokisch,
    region_id=r_lodi,
    origin_country="USA",
    description="Old-vine Garnacha from Lodi's cooler Delta sub-zone — bush-trained century-old vines producing a California Garnacha of remarkable freshness and elegance. Vibrant red with strawberry, raspberry, dried herbs, white pepper, and a silky texture that speaks of the Sandy Delta soils. Organically farmed and minimally intervened, this wine demonstrates Lodi's potential for varieties beyond Zinfandel with genuine finesse and food-pairing versatility.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_bokisch, "Grilled pork tenderloin with romesco sauce and grilled broccolini", "complement", "established", "main", "The wine's light-bodied elegance and red fruit are ideal for pork. Romesco bridges its pepper and herb notes while broccolini's slight bitterness complements its silky tannins.")
    PAIR(prod_bokisch, "Herb-roasted chicken with tomatoes, olives, and capers", "complement", "classic", "main", "Old-vine Garnacha with Mediterranean chicken preparations — the wine's strawberry and herb notes bridge perfectly to the herb-roasted bird. Olives echo its mineral complexity.")
    PAIR(prod_bokisch, "Lamb meatballs with Spanish tomato sauce and pimentón", "complement", "established", "main", "The wine's Spanish variety heritage bridges naturally to Spanish preparations. Garnacha with lamb meatballs in tomato-pimentón sauce is a pairing of obvious affinity.")
    PAIR(prod_bokisch, "Manchego with quince paste and Marcona almonds", "complement", "established", "cheese", "Old-vine Garnacha with Spanish cheese — the wine's red fruit and silky character complement Manchego's nuttiness. Quince echoes its fruit while almonds bridge its mineral depth.")

# === COLCHAGUA VALLEY (Chile) ===
print("\n=== Colchagua Valley (Chile) ===")
r_colchagua = R(
    name="Colchagua",
    country="Chile",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Colchagua Valley DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's most internationally celebrated red wine valley — the Colchagua Valley stretches 140km east from the Pacific coast into the Andes foothills in the O'Higgins Region, with the Tinguiririca river providing irrigation to alluvial and granite soils. The warm Mediterranean climate is ideal for Carmenère — Chile's adopted signature variety, brought from Bordeaux in the 19th century and thought extinct until rediscovered in the 1990s — as well as Cabernet Sauvignon, Merlot, and Syrah. Apalta (in the eastern Andes foothills) has emerged as the appellation's finest sub-zone, home to Lapostolle's Clos Apalta and Montes's Alpha M.",
    key_producers="Casa Lapostolle, Montes, Viña Viu Manent, Los Vascos (Domaines Barons de Rothschild)",
    historical_context="The Colchagua Valley was developed for viticulture in earnest in the 1990s, when foreign investment (primarily French and North American) recognized the valley's potential. The discovery that most of Chile's 'Merlot' was in fact Carmenère — the forgotten Bordeaux variety believed extinct after phylloxera — in 1994 transformed Colchagua's identity. The valley now hosts Chile's most prestigious wine route and has established Colchagua as a world-class Carmenère source."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding vintage with ideal ripening conditions. Carmenère and Cabernet of exceptional depth."),
    (2020, "very_good", "stable", "Good vintage across the valley. Apalta sub-zone wines of excellent concentration."),
    (2019, "excellent", "rising", "One of the decade's best. Long, even ripening season produced wines of great complexity."),
    (2018, "very_good", "stable", "Reliable vintage with classic Colchagua character — ripe fruit, good structure."),
    (2017, "excellent", "stable", "Outstanding year particularly for Syrah and Carmenère from the eastern Andes sites."),
]:
    VIN(r_colchagua, yr, qd, pt, sn)

p_lapostolle = P(
    name="Casa Lapostolle",
    country="Chile",
    region_id=r_colchagua,
    producer_type="winery",
    description="The most internationally acclaimed estate in the Colchagua Valley — the Marnier-Lapostolle family's biodynamic property in the Apalta sub-zone, guided originally by Michel Rolland. Clos Apalta — a blend of Carmenère, Cabernet Sauvignon, and Merlot from steep granite hillsides — has repeatedly won Wine of the Year at Wine Spectator and is considered Chile's most internationally respected single wine. The estate demonstrates Carmenère's capacity for world-class quality when grown on its ideal terroir."
)
prod_clos_apalta, new = PROD(
    name="Clos Apalta Colchagua Valley",
    category="wine_still",
    subcategory="Carmenère",
    producer_id=p_lapostolle,
    region_id=r_colchagua,
    origin_country="Chile",
    description="Chile's most celebrated wine — a blend of Carmenère, Cabernet Sauvignon, Merlot, and Petit Verdot from biodynamic steep granite hillsides in the Apalta sub-zone of Colchagua. The wine is among the southern hemisphere's most complex and age-worthy reds: dark plum, black cherry, cedar, graphite, cocoa, green bell pepper (Carmenère's signature), spice, and a silky yet firm tannin structure. Named Wine Spectator Wine of the Year in 2008 and 2015. Chile's greatest ambassador wine.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_clos_apalta, "Slow-roasted lamb shoulder with chimichurri, roasted peppers, and garlic confit", "complement", "classic", "main", "The wine's Carmenère-driven complexity and dark fruit are natural companions for Chile's favourite celebratory meat. Chimichurri echoes its herbal notes while roasted peppers bridge the variety's characteristic bell pepper.")
    PAIR(prod_clos_apalta, "Grilled wagyu tenderloin with red wine reduction and truffle butter", "complement", "established", "main", "Chile's most prestigious wine with premium beef — the wine's complexity and fine tannins elevate the wagyu's richness. Truffle butter bridges its earthy depth while the red wine reduction connects its fruit.")
    PAIR(prod_clos_apalta, "Wild mushroom and Carmenère risotto with aged Parmigiano", "bridge", "adventurous", "main", "Using the same variety in the sauce as in the glass creates a bridge pairing of unusual elegance. The risotto's earthy mushroom notes mirror Carmenère's complexity.")
    PAIR(prod_clos_apalta, "Aged Manchego with dark chocolate and dried cherry", "complement", "suggested", "cheese", "The wine's dark fruit, cedar, and cocoa notes bridge to dark chocolate while aged sheep's milk cheese adds savoury contrast. Dried cherry echoes its fruit concentration.")

p_montes = P(
    name="Montes",
    country="Chile",
    region_id=r_colchagua,
    producer_type="winery",
    description="One of Chile's most innovative and internationally recognised wine companies, founded by Aurelio Montes in 1988 with a focus on premium quality from the Colchagua Valley. Montes Alpha M — a flagship Cabernet Sauvignon blend from the steep Finca de Apalta slopes — is considered one of Chile's greatest wines. The winery also pioneered premium Syrah in Chile with its Montes Alpha Syrah, and produces the accessible Montes Classic range that introduced millions of wine drinkers to Chilean fine wine."
)
prod_montes, new = PROD(
    name="Montes Alpha M Colchagua Valley",
    category="wine_still",
    subcategory="Cabernet Sauvignon",
    producer_id=p_montes,
    region_id=r_colchagua,
    origin_country="Chile",
    description="The prestige Bordeaux blend from Montes's Finca de Apalta estate — Cabernet Sauvignon with Merlot, Carmenère, and Petit Verdot from steep granite hillsides in the Apalta sub-zone, aged 18 months in new French oak. Among Chile's most structured and age-worthy reds: blackcurrant, dark plum, cedar, graphite, tobacco leaf, and dark chocolate with firm, polished tannins and a long mineral finish. Chile's most Bordeaux-like wine in character and aging potential.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_montes, "Rack of lamb with herb crust, red wine jus, and potato dauphinoise", "complement", "classic", "main", "Chile's most Bordeaux-like wine with the classic Bordeaux meat — rack of lamb with herb crust echoes the wine's herbal notes while potato dauphinoise provides richness that its structure can support.")
    PAIR(prod_montes, "Grilled porterhouse with bone marrow butter and crispy shallots", "complement", "established", "main", "Premium Colchagua Cabernet with aged beef — the wine's firm tannins support the marbled richness while its dark fruit and cedar notes complement the char and bone marrow.")
    PAIR(prod_montes, "Duck confit with Puy lentils and Carmenère reduction", "complement", "established", "main", "A refined pairing using the valley's character variety in the sauce — Carmenère reduction bridges duck's richness to the wine's dark fruit complexity. Lentils provide earthy grounding.")
    PAIR(prod_montes, "Aged Manchego with membrillo and candied walnuts", "complement", "suggested", "cheese", "Dense Cabernet blend with aged sheep's milk cheese — the wine's structure and dark fruit balance the cheese's richness. Membrillo echoes its plum notes while candied walnuts bridge its cedar complexity.")

# === MAULE VALLEY (Chile) ===
print("\n=== Maule Valley (Chile) ===")
r_maule = R(
    name="Maule",
    country="Chile",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Maule Valley DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Chile's largest wine valley and its historic heartland — the Maule Valley stretches from the Andes to the Pacific in the Maule Region, home to some of the oldest surviving vines in the Americas. Ancient ungrafted Carignan (Cariñena) and País (Mission) vines — some planted by Spanish missionaries and Basque immigrants in the 18th and 19th centuries — produce wines of extraordinary character through the natural wine movement's interest in recovering these forgotten plantings. The region's granite soils, Mediterranean climate, and cool Pacific breezes create conditions for wines of remarkable freshness despite the latitude.",
    key_producers="Garage Wine Co, Gillmore Estate, Clos des Fous, De Martino",
    historical_context="The Maule Valley was the first region colonised for viticulture in Chile — Spanish missionaries planted País (Listán Prieto) in the 17th century, and later Carignan and other Iberian varieties arrived. For most of the 20th century the region produced bulk wine from País for domestic consumption. The natural wine movement's discovery of ancient Maule vines in the 2000s transformed the region's international profile, with producers like Garage Wine Co and Louis-Antoine Luyt pioneering old-vine Carignan."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding for old-vine Carignan — cool, long season producing wines of exceptional freshness and mineral precision."),
    (2020, "very_good", "stable", "Good vintage with Pacific cooling providing freshness. Old-vine País wines of unusual elegance."),
    (2019, "excellent", "rising", "One of the best decades for Maule Carignan — concentrated, fresh wines with remarkable old-vine depth."),
    (2018, "very_good", "stable", "Reliable vintage across the valley. Granite-soil wines of excellent character."),
    (2017, "excellent", "stable", "Classic Maule vintage — deep, earthy wines with the characteristic granite mineral of the valley."),
]:
    VIN(r_maule, yr, qd, pt, sn)

p_garage = P(
    name="Garage Wine Co",
    country="Chile",
    region_id=r_maule,
    producer_type="winery",
    description="The pioneer of old-vine Maule Carignan — Derek Mossman Knapp and Pilar Miranda's small-batch winery began in a Constitución garage in 2007, purchasing fruit from ancient dry-farmed Carignan vineyards on granite soils. Their Truquilemu (100-year-old Carignan) and Lot series wines brought international attention to Maule's forgotten heritage vines, establishing the region as a natural wine destination and inspiring a wave of producers to seek out pre-industrial Chilean vineyards. Pivotal to the global rediscovery of Carignan."
)
prod_garage, new = PROD(
    name="Garage Wine Co Truquilemu Carignan Maule Valley",
    category="wine_still",
    subcategory="Carignan",
    producer_id=p_garage,
    region_id=r_maule,
    origin_country="Chile",
    description="The wine that put Maule on the natural wine map — 100-year-old dry-farmed Carignan from granite soils in the Truquilemo area of Maule, harvested by hand and fermented with indigenous yeasts in old concrete and barrels. Vibrant garnet with aromas of red cherry, dried herbs, iron mineral, earthy granite, and wild flowers. Silky tannins and electric acidity from the old vines' natural balance. A wine of profound historical importance — connecting modern Chilean wine to its 19th century heritage.",
    price_tier="premium"
)
if new:
    PAIR(prod_garage, "Cazuela de vacuno (Chilean beef and vegetable stew)", "complement", "classic", "main", "The wine's earthy, granite mineral character bridges to the humble depth of Chile's national stew — old-vine Carignan's natural freshness elevates the simple cazuela while its tannins complement the beef.")
    PAIR(prod_garage, "Asado al palo (whole lamb on a cross, wood-fired)", "complement", "classic", "main", "Chile's most traditional outdoor cooking with old-vine Maule Carignan — the wine's dry-farmed concentration and mineral depth match the intensity of whole-roasted lamb cooked over hardwood.")
    PAIR(prod_garage, "Wild boar terrine with pickled green tomato and mustard", "complement", "established", "starter", "The wine's earthy, mineral character bridges to game. Pickled green tomato echoes Carignan's natural acidity while mustard bridges its herbal notes.")
    PAIR(prod_garage, "Aged goat's cheese with honey and rosemary", "complement", "established", "cheese", "Old-vine Carignan's light body and mineral freshness are well-suited to aged goat's milk cheese. Honey moderates the wine's acidity while rosemary echoes its wild herb character.")

p_de_martino = P(
    name="De Martino",
    country="Chile",
    region_id=r_maule,
    producer_type="winery",
    description="One of Chile's most committed advocates for old-vine heritage and terroir-specific winemaking — Marco de Martino's estate produces benchmark wines from País, Carignan, and Cinsault across the old vine zones of Maule, Itata, and Elqui. The Viejas Tinajas range (fermented in ancient clay tinaja vessels) and the Alto Los Toros País have brought international recognition to Chile's pre-Phylloxera viticultural heritage. De Martino is essential to understanding the natural wine revolution in South America."
)
prod_demartino, new = PROD(
    name="De Martino Viejas Tinajas País Maule Valley",
    category="wine_still",
    subcategory="País",
    producer_id=p_de_martino,
    region_id=r_maule,
    origin_country="Chile",
    description="Fermented in pre-Columbian clay tinajas (terracotta amphorae), this País is a bridge between ancient and modern winemaking — the variety planted by Spanish missionaries in the 17th century, fermented in the clay vessels used centuries before that. Pale garnet with extraordinary delicacy: fresh cherry, wild strawberry, red rose, dried herbs, and a granite mineral freshness that makes it one of the most original and compelling wines produced in the Americas.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_demartino, "Pastel de choclo (corn pie with ground beef, olive, and egg)", "complement", "classic", "main", "Chile's most traditional pie with the country's most ancient wine variety — the wine's lightness and mineral freshness complement the corn's sweetness while its red fruit bridges the seasoned beef filling.")
    PAIR(prod_demartino, "Empanadas de pino with ají color and cumin", "complement", "classic", "starter", "Chilean empanadas with old-vine País — the wine's delicate fruit and mineral freshness are ideal for the spiced beef filling. The terracotta fermentation adds an earthy connection to the clay-vessel tradition.")
    PAIR(prod_demartino, "Roasted beet salad with goat cheese, walnuts, and honey vinaigrette", "complement", "established", "starter", "The wine's red fruit and mineral freshness mirror beet's earthy sweetness. Goat cheese bridges its light tannin while honey vinaigrette echoes its fruit character.")
    PAIR(prod_demartino, "Queso fresco with peach preserve and fresh herbs", "complement", "suggested", "cheese", "The wine's lightness and mineral freshness are ideal for fresh milk cheese. Peach preserve echoes its red fruit while herbs bridge its wild flower character.")

# === EMPORDÀ DO (Spain) ===
print("\n=== Empordà DO (Spain) ===")
r_emporda = R(
    name="Empordà",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Empordà DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Catalonia's northernmost wine appellation, occupying the Cap de Creus peninsula and the Empordà plain between the French border and the Mediterranean coast, swept by the tramuntana and garbí winds that moderate temperatures and prevent the humidity that would otherwise encourage disease. Ancient Garnacha and Carignan vines from the region's granite and schist soils produce wines of coastal Mediterranean character — aromatic, mineral, and often lightly structured with the freshness of the sea. The region is also home to Clos Mogador's Manyetes and other cult natural wine producers drawn by the wild, windswept terroir.",
    key_producers="Clos Mogador, Mas Estela, Espelt Viticultors, Vinyes dels Aspres",
    historical_context="The Empordà-Costa Brava was the first Catalan wine region to receive its DO, in 1972. The area's viticulture dates to ancient Greek colonisation — Emporion (modern Empúries) was one of the first Greek settlements in the Iberian Peninsula. The tramuntana wind — a fierce northerly that regularly reaches 100km/h — creates unique growing conditions that stress vines beneficially and preserve the aromatics that define Empordà's coastal wine character."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Ideal tramuntana wind conditions preserving freshness. Old-vine Garnacha and Carignan of exceptional mineral purity."),
    (2020, "very_good", "stable", "Good vintage across the region. Coastal influence particularly beneficial for aromatic white varieties."),
    (2019, "excellent", "rising", "Outstanding vintage — long Mediterranean summer with beneficial wind cooling. Wines of great depth and freshness."),
    (2018, "very_good", "stable", "Classic Empordà vintage with characteristic coastal minerality."),
    (2017, "excellent", "stable", "One of the decade's finest — concentrated, mineral wines with excellent longevity."),
]:
    VIN(r_emporda, yr, qd, pt, sn)

p_espelt = P(
    name="Espelt Viticultors",
    country="Spain",
    region_id=r_emporda,
    producer_type="winery",
    description="A leading family estate in the Empordà, producing wines that showcase the region's coastal Mediterranean character with indigenous varieties. Espelt farms organically on the granite and schist soils of the Cap de Creus area, producing Garnacha-based reds, Garnacha Gris whites, and the acclaimed Comabruna — a Syrah-Garnacha blend from the windswept Cap de Creus soils. The estate embodies the emerging artisan movement that is transforming Empordà's reputation from simple rosé production to serious wine country."
)
prod_espelt, new = PROD(
    name="Espelt Comabruna Empordà",
    category="wine_still",
    subcategory="Syrah",
    producer_id=p_espelt,
    region_id=r_emporda,
    origin_country="Spain",
    description="The flagship wine of one of Empordà's leading estates — Syrah and Garnacha from old-vine, wind-stressed organic vineyards on the granite slopes of Cap de Creus. The tramuntana wind produces wines of unusual freshness and mineral quality: dark cherry, violet, smoked olive, garrigue, sea spray, and a granite mineral character that speaks unmistakably of the windswept peninsula. One of Spain's most coastal and characterful red wines.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_espelt, "Grilled suquet de peix (Catalan fish stew) with saffron and alioli", "complement", "established", "main", "A bold pairing — the wine's mineral and coastal character bridge to the seafood stew's ocean depth. Saffron adds aromatic complexity while alioli moderates the wine's tannins.")
    PAIR(prod_espelt, "Catalan botifarra sausage with white beans and pa amb tomàquet", "complement", "classic", "main", "The most Catalan of pairings — regional sausage with the coastal wine. The wine's garrigue and dark fruit complement the herbed botifarra while white beans provide earthy depth.")
    PAIR(prod_espelt, "Roast duck legs with fig, orange, and rosemary", "complement", "established", "main", "The wine's dark fruit and olive notes bridge to duck's richness. Fig echoes its concentrated fruit while rosemary mirrors its garrigue herb character.")
    PAIR(prod_espelt, "Aged Garrotxa (Catalan goat's cheese) with honey and walnuts", "complement", "established", "cheese", "Catalonia's most celebrated goat's cheese with a coastal Catalan red — the wine's mineral precision and dark fruit complement Garrotxa's semi-firm, herbaceous character.")

p_mas_estela = P(
    name="Mas Estela",
    country="Spain",
    region_id=r_emporda,
    producer_type="winery",
    description="A small, artisan estate in the Selva de Mar area of Cap de Creus, producing wines from old Garnacha Roja and Garnacha Blanca vines on schist soils swept by the tramuntana wind. The estate produces intensely mineral whites from Garnacha Blanca and Grenache Gris that have attracted natural wine devotees for their purity and saline coastal character. Among Empordà's most authentic and sought-after small producers."
)
prod_mas_estela, new = PROD(
    name="Mas Estela Vinha de Figueres Garnacha Blanca Empordà",
    category="wine_still",
    subcategory="Garnacha Blanca",
    producer_id=p_mas_estela,
    region_id=r_emporda,
    origin_country="Spain",
    description="A white wine from old-vine Garnacha Blanca on wind-swept schist soils at Cap de Creus — one of Empordà's most mineral and intensely coastal whites. Golden, textured, and aromatic with dried citrus peel, white peach, sea salt, aromatic herbs, and a persistent mineral-saline finish that speaks of the schist soils and Mediterranean sea air. Fermented with indigenous yeasts in old barrels with minimal intervention. A wine of genuine regional character.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_mas_estela, "Grilled razor clams with garlic, white wine, and parsley", "complement", "classic", "main", "Coastal white with coastal shellfish — the wine's saline mineral quality mirrors the razor clam's oceanic brine. Garlic and parsley echo its aromatic herb character while white wine in the sauce bridges the two.")
    PAIR(prod_mas_estela, "Anchoas de l'Escala with tomato bread and olive oil", "complement", "classic", "starter", "The most local pairing possible — Escala (just south of Empordà) anchovies with a Garnacha Blanca from the same coastal terroir. The wine's saline mineral quality elevates the anchovy's brine and umami.")
    PAIR(prod_mas_estela, "Sea bass ceviche with orange, fennel, and chilli", "complement", "established", "starter", "The wine's citrus and saline notes mirror the ceviche's marinade precisely. Fennel bridges its aromatic complexity while chilli heat is moderated by its mineral freshness.")
    PAIR(prod_mas_estela, "Torta del Casar (Extremaduran sheep's milk cheese) with almonds", "complement", "suggested", "cheese", "The wine's saline-mineral quality contrasts beautifully with the buttery, intense Torta. Almonds bridge its mineral depth while the cheese's pungency is lifted by the wine's bright acidity.")

# === CASSIS AOC (France) ===
print("\n=== Cassis AOC (France) ===")
r_cassis = R(
    name="Cassis",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Cassis AOC",
    reputation_tier="respected",
    quality_trajectory="established",
    description="One of Provence's smallest and most distinctive appellations — the dramatic cliff-backed town of Cassis, 20km east of Marseille on the Calanques coastline, produces some of France's most mineral and food-friendly dry whites. The amphitheatre of Jurassic limestone cliffs surrounding the bay create a unique microclimate where the Mediterranean's warmth is tempered by altitude and sea breezes, and the white and blue-tinted limestone soils impart a distinctive minerality and aromatic complexity to Marsanne, Clairette, and Ugni Blanc. 'He who has seen Paris and not Cassis has seen nothing' goes the old Provençal saying — the white wine is as essential to the town as the calanques.",
    key_producers="Château de Fontblanche, Clos Sainte-Magdeleine, Domaine du Bagnol",
    historical_context="Cassis received one of France's earliest AOC designations in 1936. Its white wine has been praised since the 18th century by travellers who visited the picturesque fishing port — Frédéric Mistral, the Provençal poet, immortalised it in verse. The appellation is tiny — only around 200 hectares — and production is largely consumed locally or by tourists. The cliffs of the Calanques (Europe's highest sea cliffs) prevent expansion."
)
for yr, qd, pt, sn in [
    (2022, "very_good", "stable", "Good vintage with characteristic Cassis freshness and mineral limestone quality."),
    (2021, "excellent", "rising", "Outstanding Cassis vintage — cool conditions preserving exceptional freshness and mineral tension."),
    (2020, "very_good", "stable", "Hot year with good limestone minerality preserved. Marsanne of good aromatic depth."),
    (2019, "excellent", "rising", "One of the finest recent Cassis vintages — complex, mineral whites with genuine cellaring potential."),
    (2018, "very_good", "stable", "Classic Cassis vintage with characteristic aromatic freshness and limestone mineral quality."),
]:
    VIN(r_cassis, yr, qd, pt, sn)

p_ste_mag = P(
    name="Clos Sainte-Magdeleine",
    country="France",
    region_id=r_cassis,
    producer_type="winery",
    description="The most celebrated estate of Cassis — the Zafiropulo family's stunning property on the limestone cliffs above the calanques, producing the appellation's most mineral and complex whites. The estate's dramatic setting — vineyards literally carved from the limestone cliff face above the sea — produces Marsanne and Clairette of extraordinary saline-mineral character that no inland vineyard could replicate. Clos Sainte-Magdeleine blanc is considered the definitive expression of Cassis white wine."
)
prod_st_mag, new = PROD(
    name="Clos Sainte-Magdeleine Blanc Cassis",
    category="wine_still",
    subcategory="Marsanne",
    producer_id=p_ste_mag,
    region_id=r_cassis,
    origin_country="France",
    description="The benchmark Cassis white — from the estate's cliff-edge limestone vineyards above the Calanques, a blend of Marsanne, Clairette, and Ugni Blanc. The wine shows the extraordinary terroir of a vineyard between limestone cliff and Mediterranean sea: white peach, lemon blossom, fresh herbs, sea breeze, white pepper, and a saline-mineral limestone finish that lingers magnificently. Light gold, fresh, and complex — one of Provence's most characterful and food-friendly whites.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_st_mag, "Bouillabaisse with rouille, saffron, and toasted baguette", "complement", "classic", "main", "The supreme Provençal pairing — bouillabaisse from Marseille with Cassis white wine from the same coastline. The wine's mineral salinity and freshness are designed for the rich, saffron-scented fish stew. Rouille adds garlic intensity that bridges its aromatic complexity.")
    PAIR(prod_st_mag, "Grilled whole sea bass from the Calanques with herbs and lemon", "complement", "classic", "main", "The most direct regional pairing — fish from the same waters as the wine. The limestone mineral and sea air character of Cassis white elevates the simple grilled fish to something of profound regional identity.")
    PAIR(prod_st_mag, "Sea urchin toast with crème fraîche and chive on brioche", "complement", "established", "starter", "The wine's saline-mineral quality and freshness mirror sea urchin's oceanic intensity. Crème fraîche moderates the urchin's iodine character while brioche bridges the wine's slight richness.")
    PAIR(prod_st_mag, "Brandade de morue (salt cod purée) with olive oil and garlic", "complement", "classic", "starter", "A classic Provençal pairing — brandade's salt cod richness and garlic intensity are lifted by the wine's mineral acidity and freshness. The wine's white pepper note bridges the olive oil's richness.")

p_fonblanche = P(
    name="Château de Fontblanche",
    country="France",
    region_id=r_cassis,
    producer_type="winery",
    description="One of Cassis's largest and most historically significant estates, producing both white and rosé from the appellation's characteristic limestone soils. Fontblanche's white — the appellation's most widely available quality expression — shows the classic Cassis profile of freshness, mineral tension, and aromatic complexity at an accessible price point. The estate has been instrumental in maintaining Cassis's reputation as an appellation worth seeking out despite its tiny production."
)
prod_fonblanche, new = PROD(
    name="Château de Fontblanche Rosé Cassis",
    category="wine_still",
    subcategory="Grenache",
    producer_id=p_fonblanche,
    region_id=r_cassis,
    origin_country="France",
    description="A rosé from Cassis's limestone cliffs — Grenache, Cinsault, and Mourvèdre producing a Provençal rosé with the distinctive limestone mineral quality of the appellation. Pale salmon-pink, dry, and intensely aromatic: fresh strawberry, dried herbs, white peach, citrus zest, and the limestone salinity that makes Cassis rosé more mineral and food-compatible than most Provence rosé. One of the appellation's most versatile food pairing wines.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_fonblanche, "Grilled octopus with fennel, lemon, and olive tapenade", "complement", "classic", "main", "Cassis rosé with Provençal octopus preparation — the wine's saline mineral and fresh herb character bridge to the octopus's Mediterranean flavours. Tapenade echoes its mineral complexity.")
    PAIR(prod_fonblanche, "Pan bagnat (Niçoise sandwich with tuna, olive, and anchovy)", "complement", "classic", "starter", "The most Provençal of pairings — pan bagnat from the same Riviera coastline with Cassis rosé. The wine's freshness and mineral salinity are ideal for the salty, savoury Niçoise ingredients.")
    PAIR(prod_fonblanche, "Tapenade d'olives with goat cheese crostini and fresh basil", "complement", "established", "starter", "The wine's fresh herb and citrus notes bridge to Provençal tapenade. Goat cheese crostini adds creaminess while basil echoes its aromatic complexity — a perfect apéritif pairing.")
    PAIR(prod_fonblanche, "Grilled sardines with sea salt and lemon", "complement", "classic", "starter", "Cassis rosé with grilled sardines is a classic Mediterranean coastal pairing — the wine's mineral salinity mirrors the sardines' oceanic character while its freshness cuts through their oiliness.")

# Final counts
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nTotal regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("\nDone.")
cur.close()
conn.close()
