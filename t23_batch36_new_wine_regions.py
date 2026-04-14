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

# === PENEDÈS DO (Spain) ===
print("\n=== Penedès DO (Spain) ===")
r_penedes = R(
    name="Penedès",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Penedès DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Catalonia's largest and most diverse wine appellation, centred on the hills west of Barcelona between the coast and the Pyrenees. Penedès encompasses everything from sea-level vineyards producing fresh white Xarel-lo for Cava to high-altitude Parellada sites at 800m. It is also the home region of Cava — Spain's traditional method sparkling wine — but increasingly celebrated for dry white blends of Xarel-lo, Macabeo, and Malvasia, and reds from Garnacha, Ull de Llebre (Tempranillo), and international varieties. The region has produced influential producers like Torres and Gramona.",
    key_producers="Mas Martinet, Joan d'Anguera, Alta Alella, Domènech",
    historical_context="The Penedès has been cultivated since Phoenician and Greek colonial times, with Roman viticulture documented throughout the region. The modern era began with Miguel Torres's introduction of French varieties and temperature-controlled winemaking in the 1960s, revolutionising Spanish wine technology. Today Penedès is increasingly focused on indigenous varieties and sustainability as it moves beyond its Cava-focused identity."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool vintage producing fresh, mineral whites and elegant reds. Xarel-lo of exceptional purity."),
    (2020, "very_good", "stable", "Warm year with good acidity from altitude vineyards. Reds of good concentration."),
    (2019, "excellent", "rising", "Outstanding vintage across all categories. High-altitude Parellada whites of great character."),
    (2018, "very_good", "stable", "Reliable vintage with good fruit character. Cava base wines of excellent quality."),
    (2017, "very_good", "stable", "Good vintage across the appellation. White wine varieties performed particularly well."),
]:
    VIN(r_penedes, yr, qd, pt, sn)

p_mas_can = P(
    name="Can Ràfols dels Caus",
    country="Spain",
    region_id=r_penedes,
    producer_type="winery",
    description="The pioneering estate of high-altitude, cool-climate Penedès — Carlos Esteva's estate on the rocky limestone soils of the Gran Caus plateau at 300–500m, producing wines of exceptional mineral quality from both indigenous and international varieties. Can Ràfols dels Caus demonstrated that Penedès could produce world-class dry wines beyond Cava — their Grand Caus (Merlot blend) and Xarel-lo wines helped reshape the region's ambitions."
)
prod_can_rafols, new = PROD(
    name="Can Ràfols dels Caus Xarel-lo Penedès",
    category="wine_still",
    subcategory="Xarel-lo",
    producer_id=p_mas_can,
    region_id=r_penedes,
    origin_country="Spain",
    description="A benchmark dry Xarel-lo from high-altitude limestone soils on the Gran Caus plateau — a testament to the indigenous Catalan variety's capacity for serious white wine beyond Cava. Fermented with indigenous yeasts in old Burgundy barrels, the wine shows white peach, almonds, wild herbs, limestone mineral, and a fresh salinity that distinguishes Penedès coastal limestone from its inland counterparts. One of the most compelling arguments for Xarel-lo as a world-class variety.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_can_rafols, "Escalivada (roasted aubergine, peppers, onion with anchovies)", "complement", "classic", "starter", "The wine's mineral freshness and almond character bridge to the smoky sweetness of escalivada. Anchovies add saline depth that echoes the wine's limestone mineral quality — a quintessential Catalan pairing.")
    PAIR(prod_can_rafols, "Pan amb tomàquet with aged Manchego and jamón serrano", "complement", "classic", "starter", "The most Catalan of all starters with the most Catalan of white grapes — the wine's freshness and almond notes complement the tomato-rubbed bread, aged cheese, and cured ham.")
    PAIR(prod_can_rafols, "Grilled sea bream with romesco sauce and grilled calçots", "complement", "established", "main", "Mediterranean fish with Catalan white — romesco's pepper and almond character echoes the wine's almond notes, calçots add sweetness, and sea bream's delicacy is matched by Xarel-lo's mineral freshness.")
    PAIR(prod_can_rafols, "Fideuà de mariscos (seafood noodles with aioli)", "complement", "established", "main", "Catalonia's seafood noodle dish with a crisp Catalan white — the wine's freshness and acidity cut through the aioli's richness while its mineral quality bridges the seafood's oceanic character.")

p_parxet = P(
    name="Parxet",
    country="Spain",
    region_id=r_penedes,
    producer_type="winery",
    description="A leading Catalan sparkling wine producer in the Alella and Penedès regions, producing both Cava and still wines with an emphasis on freshness and indigenous variety expression. Parxet's Cava Brut Nature and the still Titiana Macabeo are considered benchmarks for what indigenous Catalan varieties can achieve in quality sparkling wine production beyond the commercial mainstream."
)
prod_parxet, new = PROD(
    name="Parxet Cava Brut Nature Penedès",
    category="wine_sparkling",
    subcategory="Xarel-lo",
    producer_id=p_parxet,
    region_id=r_penedes,
    origin_country="Spain",
    description="A Brut Nature Cava from the traditional Catalan varieties — Xarel-lo, Macabeo, and Parellada — with no dosage added, producing a bone-dry sparkling wine of genuine character. Fine persistent bubbles, aromas of green apple, brioche, almond, white flowers, and a limestone mineral quality that distinguishes serious Cava from simple sparkling wine. The traditional method aging gives autolytic complexity while the Brut Nature designation ensures pure, unmasked typicity.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_parxet, "Jamón ibérico de bellota with pan con tomate", "complement", "classic", "starter", "The quintessential Spanish apéritif pairing — Cava with acorn-fed Iberian ham. The bubbles and acidity cut through the ham's fat while the wine's almond notes bridge the nutty quality of bellota pork.")
    PAIR(prod_parxet, "Oysters with shallot mignonette and lemon", "complement", "classic", "starter", "Brut Nature's mineral precision and fine bubbles are ideal for raw oysters. The zero dosage ensures no sweetness competes with the oysters' natural brininess.")
    PAIR(prod_parxet, "Gambas al ajillo (garlic prawns) with crusty bread", "complement", "established", "starter", "Catalan seafood tapas with Catalan Cava — the wine's bubble and acidity cut through the olive oil and garlic while its almond and citrus notes echo the prawn's sweetness.")
    PAIR(prod_parxet, "Truita de patates (Spanish potato omelette) with salsa brava", "complement", "established", "starter", "Brut Nature Cava with the classic tortilla española — the bubbles refresh between bites of the dense egg and potato, while the wine's minerality provides contrast to the simple richness.")

# === MONTLOUIS-SUR-LOIRE AOC (France) ===
print("\n=== Montlouis-sur-Loire AOC (France) ===")
r_montlouis = R(
    name="Montlouis-sur-Loire",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Montlouis-sur-Loire AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The often-overlooked sibling appellation to Vouvray, Montlouis-sur-Loire sits on the south bank of the Loire directly opposite its more famous neighbour, producing 100% Chenin Blanc across all sweetness levels from bone-dry to botrytised. The key difference from Vouvray lies in the soils: Montlouis sits on sandy silts over tufa and flint rather than Vouvray's clay-limestone — producing wines that are often more delicate, approachable in youth, and intensely floral. A natural wine hub, hosting producers like François Chidaine and Noella Morantin who have attracted international attention.",
    key_producers="François Chidaine, Jacky Blot (Domaine de la Taille aux Loups), Noella Morantin",
    historical_context="Montlouis received its own appellation only in 1938, having previously been included within the Vouvray designation. The separation acknowledged the distinct soil character of the south bank — though for decades it remained in Vouvray's shadow. The modern renaissance was led by François Chidaine in the 1990s and 2000s, whose biodynamic approach demonstrated Montlouis's capacity for complex, age-worthy Chenin Blanc."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, fresh vintage producing dry Montlouis of exceptional mineral purity. Among the finest recent vintages."),
    (2020, "very_good", "stable", "Warm year with good natural acidity. Demi-sec and moelleux styles particularly successful."),
    (2019, "excellent", "rising", "Outstanding vintage — long, warm growing season produced Chenin Blanc of great complexity and sweetness range."),
    (2018, "very_good", "stable", "Hot year producing full, ripe wines. Sec wines of good weight and character."),
    (2017, "very_good", "stable", "Good vintage with classic Loire character — fresh, mineral Sec wines and elegant Demi-Sec."),
]:
    VIN(r_montlouis, yr, qd, pt, sn)

p_chidaine = P(
    name="François Chidaine",
    country="France",
    region_id=r_montlouis,
    producer_type="winery",
    description="The foremost producer of Montlouis — the winemaker who essentially created the modern reputation of the appellation through his biodynamic approach and commitment to indigenous yeasts, old vines, and minimal intervention. Chidaine farms biodynamically and produces an extensive range of Chenin Blanc across both Montlouis and Vouvray from multiple lieu-dits. His dry Montlouis (notably Les Bournais and Les Choisilles) are among the Loire's finest dry whites and have attracted international critical acclaim."
)
prod_chidaine, new = PROD(
    name="François Chidaine Montlouis-sur-Loire Sec Les Bournais",
    category="wine_still",
    subcategory="Chenin Blanc",
    producer_id=p_chidaine,
    region_id=r_montlouis,
    origin_country="France",
    description="From Les Bournais — a premier lieu-dit on sandy silex soils on the plateau above the Loire — this dry Chenin Blanc is the benchmark for modern Montlouis. Bone dry, mineral, and intensely aromatic: quince, white peach, lemon verbena, tufa mineral, chalk, and the distinctive honeyed undertone that Chenin Blanc acquires from its autolytic aging potential. Fermented with indigenous yeasts in old barrels. Among the Loire's most compelling dry whites.",
    price_tier="premium"
)
if new:
    PAIR(prod_chidaine, "Grilled Loire River pike with beurre blanc and chervil", "complement", "classic", "main", "The quintessential Loire pairing — freshwater pike with dry Chenin Blanc from the same valley. The wine's mineral acidity and white stone fruit echo the delicate fish, beurre blanc bridges its buttery texture.")
    PAIR(prod_chidaine, "Rillettes de Tours with cornichons and toasted brioche", "complement", "classic", "starter", "A true regional pairing — Tours is Chenin country, rillettes are a Tours specialty. The wine's acidity cuts through the pork fat while its mineral freshness refreshes between bites.")
    PAIR(prod_chidaine, "White asparagus with sauce mousseline and Serrano ham", "complement", "classic", "starter", "Dry Loire Chenin with white asparagus is a classic French combination. The wine's quince and white flower notes complement asparagus's sweetness while its acidity cuts through the egg sauce.")
    PAIR(prod_chidaine, "Aged Sainte-Maure de Touraine (goat's cheese log) with honey", "complement", "classic", "cheese", "Loire goat cheese with Loire Chenin Blanc is one of France's most celebrated regional pairings. The wine's acidity lifts the cheese's tanginess while its honeyed undertone bridges the honey.")

p_taille_loups = P(
    name="Domaine de la Taille aux Loups",
    country="France",
    region_id=r_montlouis,
    producer_type="winery",
    description="Jacky Blot's celebrated estate spanning both Montlouis and Vouvray — a meticulous producer of Chenin Blanc in all sweetness styles with a particular talent for the sweet botrytised Cuvée des Loups and Romulus. Blot is known for extreme precision in viticulture and winemaking, producing wines of crystalline mineral purity that age magnificently. His Triple Zéro sparkling and the Rare (pétillant naturel) are also exceptional."
)
prod_taille, new = PROD(
    name="Domaine de la Taille aux Loups Montlouis-sur-Loire Clos de la Bretonnière",
    category="wine_still",
    subcategory="Chenin Blanc",
    producer_id=p_taille_loups,
    region_id=r_montlouis,
    origin_country="France",
    description="From the Clos de la Bretonnière — a walled vineyard on deep sandy silex soils producing Montlouis of exceptional mineral precision and aromatic intensity. Bone dry, Jacky Blot's Chenin from this site shows extraordinary depth: quince, lemon curd, tufa mineral, beeswax, white flowers, and a saline finish that develops extraordinary complexity with age. A wine of great seriousness and longevity — Montlouis at its finest.",
    price_tier="premium"
)
if new:
    PAIR(prod_taille, "Zander (pikeperch) with lemon beurre fondue, asparagus, and chive oil", "complement", "classic", "main", "Loire river fish with Loire Chenin — the wine's mineral tension and citrus notes are natural partners for delicate freshwater fish. Asparagus mirrors its spring-like quality while chive oil adds herbal depth.")
    PAIR(prod_taille, "Tarte Tatin with Touraine apples and crème fraîche", "complement", "classic", "dessert", "Dry Chenin Blanc's quince and apple character is a natural bridge to tarte Tatin. The wine's acidity contrasts the caramelised sweetness while crème fraîche adds dairy richness.")
    PAIR(prod_taille, "Poached chicken in cream with morels and pearl onions", "complement", "established", "main", "Classic French chicken with cream sauce — the wine's mineral acidity cuts through cream while its stone fruit echoes the chicken's delicacy. Morels bridge its earthy undertones.")
    PAIR(prod_taille, "Crottin de Chavignol with green salad and walnut vinaigrette", "complement", "classic", "cheese", "Loire goat cheese with Loire Chenin — the wine's mineral acidity contrasts the cheese's tanginess while its honey undertone bridges the walnut dressing.")

# === CALATAYUD DO (Spain) ===
print("\n=== Calatayud DO (Spain) ===")
r_calatayud = R(
    name="Calatayud",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Calatayud DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="An Aragonese DO in the Jalón river valley south of Zaragoza, sharing altitude and old-vine Garnacha character with its neighbours Cariñena and Campo de Borja. Calatayud's unique claim to fame is its extreme high-altitude viticulture — vineyards at 700–1,000m in the sierra foothills produce some of Europe's highest-altitude Garnacha. Pre-phylloxera ungrafted old vines are common, with century-old bush vine Garnacha producing wines of extraordinary concentration, freshness, and character. The region's harsh continental climate and poor, stony soils push yields to minimal levels from these ancient vineyards.",
    key_producers="Dominio de Punctum, Bodegas Ángel, San Alejandro Cooperative, Langa",
    historical_context="Calatayud received its DO status in 1990, though winemaking here predates any modern appellation by millennia — the Roman town of Bilbilis (near modern Calatayud) was renowned for its wines. The region's old ungrafted vines survived because phylloxera had difficulty penetrating the sandy, stony soils of the high sierra. The cooperative movement was dominant for much of the 20th century, with bulk wine production masking the region's potential for quality."
)
for yr, qd, pt, sn in [
    (2020, "excellent", "rising", "Outstanding vintage for old-vine Garnacha — hot summer, cool nights, producing wines of extraordinary concentration and freshness."),
    (2019, "very_good", "stable", "Good vintage across the DO. Century-vine Garnacha showed excellent character."),
    (2018, "excellent", "rising", "One of the decade's best vintages — deep, complex wines with exceptional aging potential."),
    (2017, "very_good", "stable", "Reliable vintage with good natural character from altitude sites."),
    (2016, "excellent", "stable", "Classic Calatayud vintage — powerful, concentrated Garnacha with excellent structure."),
]:
    VIN(r_calatayud, yr, qd, pt, sn)

p_bodegas_ang = P(
    name="Bodegas Ángel",
    country="Spain",
    region_id=r_calatayud,
    producer_type="winery",
    description="One of Calatayud's most authentic small producers, working with ancient ungrafted Garnacha vines — some over 120 years old — on steep limestone and granite terraces at 800–950m altitude. The estate's minimal intervention approach in the winery allows the extraordinary character of century-old dryland Garnacha bush vines to speak without obscuration. Their El Angosto single-parcel wine is considered one of the most compelling old-vine Garnacha expressions in Spain."
)
prod_angel, new = PROD(
    name="Bodegas Ángel El Angosto Calatayud",
    category="wine_still",
    subcategory="Garnacha",
    producer_id=p_bodegas_ang,
    region_id=r_calatayud,
    origin_country="Spain",
    description="From a single parcel of pre-phylloxera ungrafted Garnacha vines — some over 120 years old — on limestone and granite terraces at nearly 1,000m altitude. The extreme age and altitude produce a Garnacha of extraordinary character: transparent ruby, intensely aromatic with dried raspberry, violet, orange peel, wild herbs, iron mineral, and an almost ethereal lightness that belies its depth. Fermented with indigenous yeasts in old wood, this is old-vine Garnacha at its most pure and expressive.",
    price_tier="premium"
)
if new:
    PAIR(prod_angel, "Roasted lamb sweetbreads with capers, lemon, and parsley", "complement", "established", "main", "The wine's delicate yet deep character is ideal for offal preparations — its mineral acidity cuts through sweetbreads' richness while violet and herb notes echo the aromatic garnish.")
    PAIR(prod_angel, "Migas pastoriles (shepherd's breadcrumbs) with chorizo and egg", "complement", "classic", "main", "The traditional Aragonese shepherd's dish with the region's ancient grape — a pairing of terroir and culture. The wine's earthy depth and red fruit complement the rustic migas and spiced chorizo.")
    PAIR(prod_angel, "Wild rabbit fricassee with thyme, olives, and white wine", "complement", "established", "main", "Old-vine Garnacha's elegance and mineral precision are ideal for delicate rabbit. Thyme and olives echo its herbal and mineral notes while the fricassee's acidity mirrors its bright fruit.")
    PAIR(prod_angel, "Aged Manchego with quince paste and toasted pine nuts", "complement", "established", "cheese", "The wine's dried fruit and mineral character complement aged sheep's milk cheese. Quince bridges its raspberry fruit while pine nuts echo its mineral depth.")

p_langa = P(
    name="Bodegas Langa",
    country="Spain",
    region_id=r_calatayud,
    producer_type="winery",
    description="A family winery in Calatayud producing wines from old Garnacha vines at altitude with a focus on traditional viticulture and minimal intervention. Langa's high-altitude vineyards — some of the highest in Calatayud at over 900m — produce wines of distinctive freshness that challenge the perception of Garnacha as a heavy, southern-sun variety. Their Aldehuela single-vineyard wine from century-old vines has attracted critical attention for its unusual combination of power and elegance."
)
prod_langa, new = PROD(
    name="Bodegas Langa Aldehuela Old Vines Garnacha Calatayud",
    category="wine_still",
    subcategory="Garnacha",
    producer_id=p_langa,
    region_id=r_calatayud,
    origin_country="Spain",
    description="From the Aldehuela single vineyard — old-vine Garnacha at 900m altitude on chalky limestone soils, producing wines of remarkable freshness and aromatic complexity despite the extreme continental conditions. Vivid red with aromas of wild strawberry, pomegranate, dried lavender, rosemary, and a stony mineral finish. The altitude produces acidity levels rarely seen in Garnacha, giving the wine an almost northern Rhône-like freshness and elegance.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_langa, "Lamb chops a la brasa with romesco and rocket", "complement", "classic", "main", "The wine's bright red fruit and mineral freshness are ideal for grilled lamb. Romesco's smoky pepper and almond character bridges its herb notes while rocket adds bitter freshness.")
    PAIR(prod_langa, "Grilled wild asparagus with Iberian ham and fried egg", "complement", "established", "starter", "High-altitude Garnacha with spring asparagus — the wine's wild herb and pomegranate notes bridge to asparagus's bitterness. Ham adds savouriness while the egg yolk moderates the wine's acidity.")
    PAIR(prod_langa, "Braised pork cheeks with prunes and thyme", "complement", "established", "main", "The wine's fresh yet deeply flavoured character suits braised pork preparations — prunes echo its dried fruit notes while thyme bridges its herbal complexity.")
    PAIR(prod_langa, "Fresh cheeses sampler with dried apricots and rosemary honey", "complement", "suggested", "cheese", "High-altitude Garnacha's fresh, aromatic character bridges to young cheese. Dried apricot echoes its fruit while rosemary honey connects to its herbal freshness.")

# === VALE DOS VINHEDOS (Brazil) ===
print("\n=== Vale dos Vinhedos GI (Brazil) ===")
r_vale = R(
    name="Vale dos Vinhedos",
    country="Brazil",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Vale dos Vinhedos GI",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Brazil's most prestigious wine appellation, nestled in the highland valleys of Rio Grande do Sul state, colonised by Italian immigrants who brought vine cuttings from Veneto and Trentino in the late 19th century. The Serra Gaúcha hills at 600–800m altitude provide cooling relief from Brazil's subtropical heat, enabling cool-climate varieties — particularly Merlot, Cabernet Franc, and Chardonnay — to produce wines of genuine quality. Vale dos Vinhedos was the first Brazilian GI (2002) and first to achieve DO status (2012), establishing a quality framework that has inspired the development of other Brazilian wine regions.",
    key_producers="Miolo Winery, Cave Geisse, Don Guerino, Pizzato",
    historical_context="Italian immigrants from Veneto, Lombardy, and Trentino settled the Serra Gaúcha highlands in the 1870s–1880s, planting the Isabella grape and later European vinifera varieties. The modern wine industry began in earnest in the 1970s with investment from large companies, but quality viticulture only emerged in the 1990s. Cave Geisse's pétillant naturel and Miolo's sparkling wines established Brazil's international sparkling wine credentials, while quality still wines followed."
)
for yr, qd, pt, sn in [
    (2022, "very_good", "rising", "Good conditions in the highlands. Merlot and Chardonnay showed excellent character from the elevated sites."),
    (2021, "excellent", "rising", "Outstanding vintage — cooler than average with good acid retention. Internationally competitive wines."),
    (2020, "very_good", "stable", "Reliable vintage across the GI. Sparkling wine base wines of excellent freshness."),
    (2019, "excellent", "rising", "One of the best recent vintages. Long, cool ripening produced wines of unexpected elegance."),
    (2018, "very_good", "stable", "Good conditions with subtropical humidity managed well by altitude. Merlot of good concentration."),
]:
    VIN(r_vale, yr, qd, pt, sn)

p_cave_geisse = P(
    name="Cave Geisse",
    country="Brazil",
    region_id=r_vale,
    producer_type="winery",
    description="Brazil's most internationally celebrated sparkling wine producer, founded by Chilean oenologist Mario Geisse in 1979. Cave Geisse's traditional method sparkling wines — produced from Chardonnay and Pinot Noir grown at altitude in the Serra Gaúcha highlands — have won major international awards and demonstrated that Brazil can produce serious sparkling wine to match European standards. The Geisse Brut Nature is considered one of South America's finest sparkling wines."
)
prod_geisse, new = PROD(
    name="Cave Geisse Brut Nature Vale dos Vinhedos",
    category="wine_sparkling",
    subcategory="Chardonnay",
    producer_id=p_cave_geisse,
    region_id=r_vale,
    origin_country="Brazil",
    description="South America's most acclaimed traditional method sparkling wine — Chardonnay and Pinot Noir from highland vineyards at 700m in the Serra Gaúcha, fermented in bottle with no dosage added. Fine, persistent bubbles; aromas of green apple, brioche, citrus zest, chalk, and a distinctive tropical freshness that marks it as undeniably South American. Extended lees aging produces autolytic complexity. A wine that challenges preconceptions about Brazilian fine wine and South American sparkling.",
    price_tier="premium"
)
if new:
    PAIR(prod_geisse, "Fresh palmito (heart of palm) salad with citrus vinaigrette", "complement", "established", "starter", "The wine's tropical freshness and mineral precision pair naturally with Brazil's iconic fresh palmito. Citrus vinaigrette echoes its brightness while the palm's subtle sweetness complements the wine's fruit.")
    PAIR(prod_geisse, "Ceviche de tilápia with Brazilian peppers, lime, and coriander", "complement", "established", "starter", "The wine's fine bubble and acidity are natural complements to ceviche's citrus curing. Brazilian peppers bridge to its lively fruit character while coriander adds aromatic freshness.")
    PAIR(prod_geisse, "Grilled sea bass with moqueca-style coconut and pepper broth", "complement", "adventurous", "main", "The wine's tropical freshness and acidity navigate the challenge of moqueca's coconut richness — an adventurous but compelling Brazilian fine dining pairing.")
    PAIR(prod_geisse, "Petit fours with passion fruit curd and mango sorbet", "complement", "suggested", "dessert", "The wine's tropical fruit underpinning bridges naturally to Brazilian fruit preparations. Passion fruit mirrors its acidity while mango sorbet echoes its lush fruit character.")

p_pizzato = P(
    name="Pizzato",
    country="Brazil",
    region_id=r_vale,
    producer_type="winery",
    description="A family winery in Vale dos Vinhedos producing some of Brazil's most ambitious still wines, with a focus on Merlot and DNA (a Marselan-based blend) from altitude vineyards at 600–750m. Pizzato is known for their commitment to technical excellence and French-influenced winemaking — their Focus Merlot is regularly cited as one of Brazil's finest red wines and represents a genuine contribution to South American fine wine beyond Argentina and Chile."
)
prod_pizzato, new = PROD(
    name="Pizzato Focus Merlot Vale dos Vinhedos",
    category="wine_still",
    subcategory="Merlot",
    producer_id=p_pizzato,
    region_id=r_vale,
    origin_country="Brazil",
    description="Brazil's benchmark Merlot — from high-altitude vineyards in Vale dos Vinhedos, fermented in stainless steel and aged in French barriques. The wine shows the elegance that altitude provides to Merlot in subtropical climates: dark cherry, plum, cedar, cocoa, and a mineral freshness that bridges Italian immigrant heritage and French winemaking technique. One of South America's most underrated red wines and the strongest argument for Brazilian fine wine credibility.",
    price_tier="premium"
)
if new:
    PAIR(prod_pizzato, "Costela de porco no bafo (slow-braised pork ribs with polenta)", "complement", "classic", "main", "The Italian-Brazilian pairing logic — Veneto immigrants who brought the vines also brought polenta and braised pork traditions. The wine's Merlot elegance and dark fruit complement the richness of braised pork ribs.")
    PAIR(prod_pizzato, "Churrasco (grilled picanha) with farofa and vinagrete", "complement", "established", "main", "Brazil's iconic barbecued beef with a fine Brazilian red — Merlot's soft tannins support the picanha's rich fat while the wine's dark fruit complements the char. Vinagrete's acidity bridges the wine's freshness.")
    PAIR(prod_pizzato, "Risotto negro (squid ink risotto) with sea bream and herbs", "complement", "adventurous", "main", "Italian-influenced Brazilian cuisine with an Italian-influenced wine — Merlot's soft elegance bridges squid ink's mineral depth. An adventurous pairing that works through shared Italian heritage.")
    PAIR(prod_pizzato, "Queijo Serra Gaúcha with jaleia de uva (grape jelly)", "complement", "suggested", "cheese", "Local Serra Gaúcha cheese with a regional red — grape jelly made from the same vineyards echoes the wine's dark fruit while the cheese's mild richness is complemented by Merlot's soft tannins.")

# === AJACCIO AOC (France / Corsica) ===
print("\n=== Ajaccio AOC (France / Corsica) ===")
r_ajaccio = R(
    name="Ajaccio",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Ajaccio AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The premium wine appellation of the Corse du Sud department, centred on the capital of Corsica and the western slopes of its central mountain range. Ajaccio is defined by its monopoly on the Sciaccarellu (Mammolo in mainland Italy) red grape variety — a light, fragrant, spicy variety unique to Corsica that produces wines of extraordinary elegance and aromatic complexity from the granite and quartz soils of the island's western coast. White wines from Vermentino and Ugni Blanc round out the appellation. The wines carry the wild garrigue character of Corsica — maquis herbs, granite mineral, and the sea.",
    key_producers="Domaine Comte Abbatucci, Domaine Maestracci, Antoine Arena, Clos Capitoro",
    historical_context="Corsica's wine tradition predates the island's Roman and Greek colonisation — the name Sciaccarellu may derive from the Etruscan period. Modern Ajaccio wines gained attention in the late 20th century through the Peraldi family and later through the biodynamic work of Domaine Comte Abbatucci, whose recovery of ancient Corsican varieties has become one of wine's most remarkable conservation stories."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Ideal growing conditions with Mediterranean sun and cool mountain influence. Sciaccarellu of exceptional elegance."),
    (2020, "very_good", "stable", "Warm year producing full, aromatic wines. Vermentino whites of tropical intensity."),
    (2019, "excellent", "rising", "Outstanding vintage across all styles. Sciaccarellu of great aromatic precision and aging potential."),
    (2018, "very_good", "stable", "Hot year with some freshness preserved by altitude vineyards. Characteristic garrigue complexity."),
    (2017, "excellent", "stable", "Classic Corsican vintage — balanced, aromatic wines with good structure and longevity."),
]:
    VIN(r_ajaccio, yr, qd, pt, sn)

p_abbatucci = P(
    name="Domaine Comte Abbatucci",
    country="France",
    region_id=r_ajaccio,
    producer_type="winery",
    description="The most celebrated and important estate in Corsica — Jean-Charles Abbatucci's biodynamic domain near Casalabriva, preserving and vinifying ancient Corsican varieties that exist nowhere else in the world. Abbatucci has identified, propagated, and bottled over a dozen varieties from the Corsican patrimony, including Minustellu, Aleatico, Biancone, and the rare Carcajolo Nero and Bianco. His Faustine and Impérial wines are considered reference points for Corsican fine wine, and his conservation work has attracted worldwide attention."
)
prod_abbatucci, new = PROD(
    name="Domaine Comte Abbatucci Faustine Ajaccio Rouge",
    category="wine_still",
    subcategory="Sciaccarellu",
    producer_id=p_abbatucci,
    region_id=r_ajaccio,
    origin_country="France",
    description="The flagship wine of Corsica's most important estate — Sciaccarellu from biodynamic granite vineyards at altitude above Casalabriva. Named after Napoleon's mother (born in Ajaccio), the wine is translucent ruby with aromas of wild strawberry, dried cherry, pink pepper, maquis herbs (rosemary, cistus, lentisk), and a distinctive granite mineral quality. Light-bodied, silky, and ethereally perfumed — Sciaccarellu at its most transcendent and one of France's most original red wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_abbatucci, "Brocciu-stuffed ravioli with Corsican mint and salted butter", "complement", "classic", "main", "Brocciu — Corsica's whey cheese — with the island's most distinctive red grape. The wine's delicacy and herb character echo the mint stuffing while its acidity cuts through the cheese richness.")
    PAIR(prod_abbatucci, "Charcuterie corse (lonzu, coppa, figatellu) with chestnut bread", "complement", "classic", "starter", "The most Corsican of pairings — the island's celebrated mountain charcuterie with its most ethereal red wine. The wine's wild herb and granite mineral complement the aromatic, maquis-grazed pork.")
    PAIR(prod_abbatucci, "Roasted wild Corsican blackbird (merle) if available, or pigeon", "complement", "established", "main", "Small game bird with Sciaccarellu — the wine's delicacy and wild character perfectly complements the intense, gamey flavour of small game. One of Corsica's most prized and rare traditional pairings.")
    PAIR(prod_abbatucci, "Brocciu frais with chestnut honey and walnuts", "complement", "established", "cheese", "Fresh Corsican whey cheese with the island's most elegant red — the wine's acidity and red fruit brighten the cheese's mild richness. Chestnut honey adds complexity while walnuts bridge its granite mineral.")

p_clos_cap = P(
    name="Clos Capitoro",
    country="France",
    region_id=r_ajaccio,
    producer_type="winery",
    description="One of Ajaccio's most established and reliable estates, producing benchmark Sciaccarellu reds and Vermentino whites from hillside granite vineyards above Piana. The Biancone family has cultivated these Ajaccio slopes for generations, and their wines represent the most traditional and accessible expression of Corsican wine character — aromatic, mineral, and distinctly Mediterranean in character."
)
prod_cap, new = PROD(
    name="Clos Capitoro Vermentino Ajaccio Blanc",
    category="wine_still",
    subcategory="Vermentino",
    producer_id=p_clos_cap,
    region_id=r_ajaccio,
    origin_country="France",
    description="A Vermentino white from Ajaccio's granite hillsides — Corsica's answer to Sardinia's Vermentino di Gallura. Pale gold with intense aromas of white peach, citrus blossom, almonds, maquis herbs, sea breeze, and the distinctive bitter almond finish that marks Corsican Vermentino. Fermented at low temperatures for maximum aromatic retention. Fresh, saline, and intensely Mediterranean — a wine that tastes like sunshine on granite.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_cap, "Grilled langoustines with garlic butter, lemon, and herbs", "complement", "classic", "main", "Corsican white with Mediterranean shellfish — the wine's saline minerality and citrus freshness are the ideal complement to sweet langoustine. Garlic and herbs echo its maquis character.")
    PAIR(prod_cap, "Chilled octopus with olives, capers, and lemon oil", "complement", "established", "starter", "Mediterranean island cuisine with island white wine — the wine's mineral freshness and bitter almond note mirror the octopus's oceanic character. Capers and olives echo its saline complexity.")
    PAIR(prod_cap, "Aioli grand with salt cod, vegetables, and hard eggs", "complement", "classic", "main", "The Provençal/Corsican grand aioli is a natural pairing for Corsican Vermentino. The wine's acidity cuts through the aioli while its mineral freshness bridges the salt cod.")
    PAIR(prod_cap, "Brocciu and fig tart with thyme honey", "complement", "suggested", "dessert", "The wine's bitter almond and stone fruit notes bridge to fig and honey. Brocciu provides a mild dairy base that the wine's acidity lifts, while thyme honey echoes its herbal maquis character.")

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
