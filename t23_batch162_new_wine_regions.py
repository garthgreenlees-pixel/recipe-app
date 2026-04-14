#!/usr/bin/env python3
"""B162 — Portuguese wine regions: Douro DOC, Dão DOC, Bairrada DOC, Vinho Verde DOC, Madeira DOC"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None, **kwargs):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region inserted: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
        (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === DOURO DOC ===
print("=== Douro DOC ===")
r = R("Douro DOC", "Portugal", "wine_region",
      "Portugal's oldest demarcated wine region, the Douro Valley produces both the world's great fortified wine (Port) and increasingly acclaimed dry table wines. The terraced schist vineyards carved into steep valley slopes are among viticulture's most dramatic landscapes. Old-vine Touriga Nacional, Touriga Franca, and Tinta Roriz yield wines of immense concentration and complexity.",
      climate_classification="continental_semi_arid",
      latitude=41.17, longitude=-7.45,
      elevation_range="100–900m",
      annual_rainfall="400–900mm",
      soil_composition="Schist, granite",
      primary_varietals="Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca",
      regulatory_body="IVDP",
      total_area_ha=44000,
      sub_regions="Baixo Corgo, Cima Corgo, Douro Superior")
for yr, qd, pt, sn in [
    (2017,"exceptional","stable","A legendary vintage across the Douro with ideal ripening conditions and high concentration."),
    (2019,"excellent","rising","Excellent balance of fruit concentration and freshness in a warm but not excessive year."),
    (2020,"very_good","stable","Challenging year managed well by top estates, producing concentrated wines with good structure."),
    (2021,"excellent","rising","Widely acclaimed as one of the finest recent vintages for Douro table wines."),
    (2022,"very_good","stable","Warm vintage yielding rich, powerful wines with ripe tannins."),
    (2023,"good","stable","Fresh conditions produced elegant, aromatic wines across the valley."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Quinta do Crasto", "winery", r, "Portugal",
       production_philosophy="terroir_expression",
       philosophy_description="Historic Douro quinta producing benchmark table wines and Ports from old-vine terraced vineyards above the river. The Roquette family's commitment to quality has made Crasto one of the Douro's leading names.",
       reputation_narrative="Quinta do Crasto is one of the Douro's most celebrated estates, renowned for its LBV and Vintage Ports alongside outstanding dry Touriga Nacional table wines that rival any in Iberia.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Crasto Superior Douro Red", "wine_still", p1, r, "Portugal",
                    subcategory="red", description="Estate flagship dry red from old-vine Touriga Nacional and Tinta Roriz, showing deep violet colour, dark fruit, graphite, and firm schist-driven tannins.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted lamb with rosemary and garlic", "complement", "classic", "main", "The wine's dark fruit and firm tannins mirror the lamb's richness; both share earthy, iron-tinged depth.")
    PAIR(prod, "Wild boar stew with black olives", "complement", "established", "main", "Powerful Touriga tannins cut through gamey richness; olive bitterness bridges the wine's herbal notes.")
    PAIR(prod, "Aged sheep's milk cheese — Serra da Estrela", "bridge", "adventurous", "cheese", "The wine's schist minerality and the cheese's lanolin richness create an extraordinary Iberian pairing.")
    PAIR(prod, "Charcoal-grilled beef ribs with chimichurri", "complement", "classic", "main", "Bold tannins and dark fruit stand up to charred beef; herbaceous chimichurri echoes the wine's eucalyptus notes.")
prod, is_new = PROD("Crasto LBV Port Douro", "wine_still", p1, r, "Portugal",
                    subcategory="port_lbv", description="Late Bottled Vintage Port from a single year, offering plum, dark cherry, chocolate, and warming spice with a long, velvety finish.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Dark chocolate fondant with salted caramel", "complement", "classic", "dessert", "Rich plum and chocolate notes in the Port mirror the fondant's intensity; salt heightens the sweetness.")
    PAIR(prod, "Stilton or aged blue cheese", "contrast", "classic", "cheese", "The classic Port and Stilton pairing — wine's sweetness contrasts with cheese's salt and funk in perfect harmony.")
    PAIR(prod, "Dried fig and walnut tart", "complement", "established", "dessert", "Figs echo the Port's dried fruit character; walnuts add bitterness that refreshes the palate.")
    PAIR(prod, "Chocolate and cherry brownie", "complement", "classic", "dessert", "Dark cherry and chocolate in the Port amplify the brownie's richness for an indulgent finish.")

p2 = P("Quinta do Vale Meão", "winery", r, "Portugal",
       production_philosophy="biodynamic",
       philosophy_description="Legendary Douro Superior estate, the original home of Barca Velha, now producing iconic dry wines under the Olazabal family. The 'Meandro' label represents extraordinary old-vine terroir from schist vineyards.",
       reputation_narrative="Quinta do Vale Meão produces some of Portugal's most iconic wines from the remote Douro Superior, where extreme continental conditions yield wines of extraordinary concentration and longevity.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Vale Meão Douro Red", "wine_still", p2, r, "Portugal",
                    subcategory="red", description="Flagship estate red blending Touriga Nacional, Touriga Franca, and Tinta Amarela from 40+ year old vines in the Douro Superior. Deep, concentrated, and structured for long ageing.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted Iberian black pig suckling with thyme", "complement", "classic", "main", "The wine's power and complexity matches the suckling pig's richness; shared savouriness elevates both.")
    PAIR(prod, "Venison loin with juniper berry sauce", "complement", "established", "main", "Dark fruit tannins complement gamey venison; juniper's herbal bitterness echoes the wine's structure.")
    PAIR(prod, "Truffle risotto with aged Parmesan", "bridge", "adventurous", "main", "Mineral schist notes in the wine bridge to the earthy truffle; Parmesan's umami amplifies the wine's depth.")
    PAIR(prod, "Braised oxtail with root vegetables and Port reduction", "complement", "classic", "main", "A Douro-inspired pairing — wine's tannic backbone structures the collagen-rich braise perfectly.")

# === DÃO DOC ===
print("=== Dão DOC ===")
r2 = R("Dão DOC", "Portugal", "wine_region",
       "Portugal's great terroir-driven red wine region, Dão sits in a high-altitude granite plateau surrounded by mountain ranges that moderate temperatures. Touriga Nacional reaches its most elegant expression here — less powerful than Douro but with extraordinary finesse, floral character, and longevity.",
       climate_classification="continental",
       latitude=40.5, longitude=-7.8,
       elevation_range="400–800m",
       annual_rainfall="800–1200mm",
       soil_composition="Granite, sandy soils",
       primary_varietals="Touriga Nacional, Alfrocheiro, Tinta Roriz, Encruzado",
       regulatory_body="Comissão Vitivinícola Regional do Dão",
       total_area_ha=20000,
       sub_regions="Serra da Estrela foothills, Silgueiros, Nelas")
for yr, qd, pt, sn in [
    (2018,"very_good","stable","A fine vintage in Dão with excellent ripeness and natural freshness from altitude."),
    (2019,"excellent","rising","Widely considered one of the great recent Dão vintages — perfumed, structured, long-lived."),
    (2020,"good","stable","Warm year yielded richer wines than typical but retaining Dão's signature finesse."),
    (2021,"very_good","stable","Elegant, aromatic wines with good acidity and classic floral Touriga character."),
    (2022,"very_good","stable","Concentrated but fresh wines; altitude vineyards particularly successful."),
    (2023,"excellent","rising","Exceptional year producing some of the finest Dão wines in recent memory."),
]:
    VIN(r2, yr, qd, pt, sn)

p3 = P("Niepoort Vinhos", "winery", r2, "Portugal",
       production_philosophy="minimal_intervention",
       philosophy_description="Dirk Niepoort is one of Portugal's most influential winemakers, producing benchmark wines across the Douro and Dão using minimal intervention, native yeasts, and respect for old vine character.",
       reputation_narrative="Dirk Niepoort's Dão wines, particularly the Redoma series, have helped define the region's potential for elegant, age-worthy reds and whites at the highest level.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Niepoort Redoma Dão Tinto", "wine_still", p3, r2, "Portugal",
                    subcategory="red", description="Benchmark Dão red from Touriga Nacional and other old-vine indigenous varieties. Perfumed violets, dark cherry, granite minerality, and silky tannins with exceptional ageing potential.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted guinea fowl with lentils and herbs", "complement", "classic", "main", "Dão's elegant Touriga tannins lift roasted poultry without overwhelming; lentils echo the wine's earthy depth.")
    PAIR(prod, "Braised pork belly with black beans", "complement", "established", "main", "The wine's silky tannins and dark fruit complement rich pork; black beans add earthiness that bridges beautifully.")
    PAIR(prod, "Wild mushroom risotto with truffle oil", "bridge", "adventurous", "main", "Granite minerality in the Dão bridges to earthy mushrooms; violet aromatics add unexpected elegance.")
    PAIR(prod, "Roasted lamb rack with mint gremolata", "complement", "classic", "main", "Floral Touriga characters lift the lamb; mint gremolata echoes the wine's herbal freshness.")
prod, is_new = PROD("Niepoort Redoma Dão Branco", "wine_still", p3, r2, "Portugal",
                    subcategory="white", description="Exceptional Dão white from Encruzado and other native white varieties. Rich yet fresh with stone fruit, almond, lemon blossom, and a mineral backbone — one of Portugal's great whites.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled whole sea bream with lemon and herbs", "complement", "classic", "main", "The wine's citrus brightness and mineral freshness complement delicate white fish perfectly.")
    PAIR(prod, "Octopus with potato and olive oil — à lagareiro", "complement", "classic", "main", "A quintessential Dão white pairing — the wine's richness matches octopus while acidity cuts through olive oil.")
    PAIR(prod, "Aged sheep's milk cheese with honey", "bridge", "established", "cheese", "Almond and stone fruit in the wine bridge to the cheese's lanolin character; honey ties both together.")
    PAIR(prod, "Roasted chicken with garlic and bay leaf", "complement", "established", "main", "Stone fruit and herbal notes in the wine mirror roasted chicken's aromatics.")

p4 = P("Casa de Santar", "winery", r2, "Portugal",
       production_philosophy="terroir_expression",
       philosophy_description="Historic Dão estate with deep roots in the region, producing benchmark single-quinta wines that express Dão's granite soils and continental climate with elegance and authority.",
       reputation_narrative="Casa de Santar is one of Dão's benchmark estates, known for wines that elegantly balance concentration and freshness, making them ideal representatives of the region's terroir-driven style.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Casa de Santar Dão Tinto Reserva", "wine_still", p4, r2, "Portugal",
                    subcategory="red", description="Single-estate Dão red Reserva from Touriga Nacional, Alfrocheiro, and Tinta Roriz. Deep garnet, blackberry, violet, cedar, and firm granite tannins.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Slow-roasted pork shoulder with rosemary", "complement", "classic", "main", "The wine's ripe tannins and dark fruit complement slow-cooked pork; rosemary mirrors herbal notes.")
    PAIR(prod, "Beef and root vegetable stew", "complement", "established", "main", "Structured tannins cut through the stew's richness; shared earthy depth between wine and vegetables.")
    PAIR(prod, "Aged São Jorge cheese from the Azores", "complement", "established", "cheese", "Portuguese hard cheese with the wine's tannins and dark fruit creates a regional harmony.")
    PAIR(prod, "Grilled lamb chops with piri piri", "complement", "adventurous", "main", "Dark fruit in the wine stands up to spicy piri piri heat; tannins cut through lamb fat.")

# === BAIRRADA DOC ===
print("=== Bairrada DOC ===")
r3 = R("Bairrada DOC", "Portugal", "wine_region",
       "Bairrada is Portugal's most distinctive wine region, defined by the indigenous Baga grape — a notoriously tannic, high-acid variety that, in the hands of skilled producers, creates wines of extraordinary structure and longevity. The clay-limestone soils of this Atlantic-influenced coastal region also produce exceptional sparkling wines and increasingly fine whites from Bical.",
       climate_classification="atlantic",
       latitude=40.4, longitude=-8.5,
       elevation_range="30–200m",
       annual_rainfall="1000–1400mm",
       soil_composition="Clay, limestone, sandy",
       primary_varietals="Baga, Bical, Cerceal, Castelão",
       regulatory_body="Comissão Vitivinícola da Bairrada",
       total_area_ha=13000,
       sub_regions="Ançã, Tamengos, Aguim")
for yr, qd, pt, sn in [
    (2017,"very_good","stable","A powerful vintage in Bairrada with Baga showing great depth and structure."),
    (2018,"excellent","rising","Exceptional year — Baga of rare elegance with great fruit-tannin balance."),
    (2019,"very_good","stable","Classic Bairrada vintage with concentrated fruit and the region's characteristic tannic backbone."),
    (2020,"good","stable","Warm year; some wines slightly lacking freshness, but top producers excelled."),
    (2021,"excellent","rising","Among the greatest recent Bairrada vintages, particularly for long-ageing Baga."),
    (2022,"very_good","stable","Rich and concentrated wines with firm structure for extended cellaring."),
]:
    VIN(r3, yr, qd, pt, sn)

p5 = P("Luís Pato", "winery", r3, "Portugal",
       production_philosophy="terroir_expression",
       philosophy_description="The leading figure of Bairrada, Luís Pato has championed the Baga grape for decades, producing wines from single vineyard 'Vinhas Velhas' (old vines) that demonstrate Baga's capacity for greatness. His daughter Filipa now also makes acclaimed wines in the region.",
       reputation_narrative="Luís Pato is inseparable from Bairrada's identity — his single-vineyard Baga wines from Vinhas Velhas vines planted in 1961 are Portugal's most age-worthy reds and among Europe's most distinctive.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Luís Pato Vinha Pan Bairrada Red", "wine_still", p5, r3, "Portugal",
                    subcategory="red", description="Single-vineyard Baga from 1961-planted old vines. Deep ruby, intense black cherry, iron, dried herbs, and exceptional tannic structure requiring years of cellaring for full expression.", price_tier="premium")
if is_new:
    PAIR(prod, "Suckling pig — leitão à Bairrada", "complement", "classic", "main", "The definitive Bairrada pairing — the region's signature dish and wine. Baga's tannins cut through crispy crackling and rich pork; the combination is extraordinary.")
    PAIR(prod, "Aged manchego with quince paste", "bridge", "established", "cheese", "The wine's high acidity and tannins cut through the cheese's fat; quince sweetness bridges Baga's cherry fruit.")
    PAIR(prod, "Braised oxtail with herbs and red wine", "complement", "established", "main", "Old-vine Baga's structure demands the collagen richness of oxtail; shared earthiness deepens the pairing.")
    PAIR(prod, "Grilled sardines on charcoal", "contrast", "adventurous", "main", "An unexpected Portuguese pairing — Baga's high acidity cuts through sardine richness; the contrast is revelatory.")
prod, is_new = PROD("Luís Pato Bairrada Espumante Bruto", "wine_sparkling", p5, r3, "Portugal",
                    subcategory="sparkling_traditional_method", description="Traditional method sparkling wine from Bical and Cerceal — crisp, mineral, autolytic, with lemon, green apple, and a long bready finish. Among Portugal's finest sparklings.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled prawns with garlic butter", "complement", "classic", "starter", "The sparkling's mineral acidity cuts through butter; lemon notes echo the prawns' brininess.")
    PAIR(prod, "Oysters with shallot mignonette", "complement", "classic", "amuse", "Mineral, high-acid sparkling is the textbook pairing for briny oysters — the brininess amplifies the wine's sea-mineral character.")
    PAIR(prod, "Smoked salmon blini with crème fraîche", "complement", "established", "starter", "Autolytic complexity bridges to smoked salmon; bubbles cleanse the richness of crème fraîche.")
    PAIR(prod, "Seared scallops with cauliflower purée", "complement", "classic", "starter", "The sparkling's acidity contrasts scallop sweetness; bready notes bridge to the cauliflower.")

# === VINHO VERDE DOC ===
print("=== Vinho Verde DOC ===")
r4 = R("Vinho Verde DOC", "Portugal", "wine_region",
       "One of Portugal's largest and most distinctive wine regions, Vinho Verde ('green wine') spans the lush, rainy northwest. The Alvarinho sub-region (Monção e Melgaço) produces Portugal's most prized white wines — intensely aromatic, full-bodied expressions that rival great Rieslings in complexity. The broader region also produces fresh, slightly petillant whites for early drinking, plus some rosé.",
       climate_classification="atlantic",
       latitude=41.7, longitude=-8.3,
       elevation_range="50–450m",
       annual_rainfall="1200–2000mm",
       soil_composition="Granite, sandy loam",
       primary_varietals="Alvarinho, Loureiro, Arinto, Trajadura, Azal",
       regulatory_body="CVRVV",
       total_area_ha=21000,
       sub_regions="Monção e Melgaço, Lima, Cávado, Ave, Amarante, Sousa, Basto, Paiva")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Exceptional Alvarinho vintage with superb concentration and freshness in Monção e Melgaço."),
    (2020,"very_good","stable","Fine wines across the region; Alvarinho particularly successful with aromatic intensity."),
    (2021,"good","stable","Challenging year with high rainfall; careful canopy management produced fresh, elegant wines."),
    (2022,"very_good","rising","Warm, dry year produced richer, more concentrated Alvarinho than typical."),
    (2023,"excellent","rising","Widely acclaimed vintage for Alvarinho — aromatic, precise, and long-lived."),
]:
    VIN(r4, yr, qd, pt, sn)

p6 = P("Quinta de Soalheiro", "winery", r4, "Portugal",
       production_philosophy="terroir_expression",
       philosophy_description="The benchmark producer of Monção e Melgaço Alvarinho, Soalheiro has pioneered the region's identity for over four decades. Their sun-facing (soalheiro = sunny) granite terraces yield Alvarinho of extraordinary aromatic complexity and age-worthiness.",
       reputation_narrative="Quinta de Soalheiro is the reference producer for Monção e Melgaço Alvarinho — their single-vineyard and barrel-fermented expressions have demonstrated that Vinho Verde can produce world-class whites for cellaring.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Soalheiro Alvarinho Monção e Melgaço", "wine_still", p6, r4, "Portugal",
                    subcategory="white", description="Benchmark Monção e Melgaço Alvarinho from granite terraces. Intense peach, apricot, jasmine, and lime zest with a saline, mineral backbone and refreshing natural acidity.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled Atlantic turbot with lemon butter", "complement", "classic", "main", "The wine's citrus brightness and mineral salinity complement turbot perfectly; a great Atlantic pairing.")
    PAIR(prod, "Razor clams steamed with white wine and garlic", "complement", "classic", "starter", "Alvarinho's salinity and stone fruit mirror razor clams' brininess; garlic bridges the wine's aromatic intensity.")
    PAIR(prod, "Ceviche with tiger's milk and fresh coriander", "complement", "established", "starter", "Tropical fruit notes and high acidity in Alvarinho mirror the citrus-forward ceviche marinade.")
    PAIR(prod, "Salt cod — bacalhau à Gomes de Sá", "complement", "classic", "main", "A quintessential Portuguese pairing — Alvarinho's salinity and richness match salt cod's depth perfectly.")
prod, is_new = PROD("Soalheiro Granit Alvarinho", "wine_still", p6, r4, "Portugal",
                    subcategory="white", description="Barrel-fermented single-vineyard Alvarinho aged on fine lees. Richer, more complex, with stone fruit, hazelnut, beeswax, and a long granite-mineral finish — among Portugal's finest whites.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Lobster thermidor with tarragon", "complement", "classic", "main", "The barrel-fermented richness matches lobster's luxury; tarragon's anise note echoes Alvarinho's herbal dimension.")
    PAIR(prod, "Seared foie gras with quince", "contrast", "adventurous", "starter", "The wine's acidity cuts through foie's richness; quince sweetness bridges the Alvarinho's tropical fruit.")
    PAIR(prod, "White asparagus with hollandaise", "complement", "established", "starter", "Barrel notes in the wine bridge to the buttery hollandaise; asparagus echoes the wine's herbal freshness.")
    PAIR(prod, "Aged Comté with apple and walnut", "bridge", "established", "cheese", "Hazelnut notes in the Granit bridge to Comté's nuttiness; apple echoes the wine's stone fruit character.")

p7 = P("Anselmo Mendes", "winery", r4, "Portugal",
       production_philosophy="terroir_expression",
       philosophy_description="Anselmo Mendes is Vinho Verde's most celebrated winemaker, working with multiple sub-regions and producing benchmark Alvarinho wines alongside innovative blends that explore the region's full potential.",
       reputation_narrative="Anselmo Mendes elevated Vinho Verde's image internationally through his Muros Antigos and Contacto labels, demonstrating that the region's wines — particularly Alvarinho — deserve serious recognition.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Anselmo Mendes Contacto Alvarinho", "wine_still", p7, r4, "Portugal",
                    subcategory="white", description="Skin-contact Alvarinho with brief maceration, giving depth, texture, and complexity beyond the typical early-drinking style. Stone fruit, orange peel, almond, and a distinctive tannic grip.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled sardines with charred bread", "complement", "established", "main", "Skin-contact texture and phenolics handle sardine oiliness; citrus notes cut through richness.")
    PAIR(prod, "Piri piri chicken with charred lemon", "complement", "adventurous", "main", "The wine's phenolic grip stands up to piri piri heat; citrus notes echo the charred lemon.")
    PAIR(prod, "Cheese empanadas with green herb sauce", "bridge", "established", "starter", "Orange peel notes bridge to herby sauce; the wine's texture complements pastry richness.")
    PAIR(prod, "Smoked tuna with pickled vegetables", "complement", "established", "starter", "Skin-contact phenolics cut through smoked fish; citrus notes lift pickled vegetable acidity.")

# === MADEIRA DOC ===
print("=== Madeira DOC ===")
r5 = R("Madeira DOC", "Portugal", "wine",
       designation_type="DOC",
       designation_name="Madeira DOC",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="The island of Madeira, 1000km southwest of Lisbon, produces one of the world's most unique and long-lived wines. Madeira's volcanic soils, humid Atlantic climate, and unique estufagem or canteiro heating process create fortified wines of extraordinary complexity and near-immortal longevity. The classic varieties — Sercial, Verdelho, Bual, and Malmsey — define distinct styles from bone dry to lusciously sweet.",
       key_producers="Blandy's, Barbeito, Henriques & Henriques, d'Oliveiras",
       historical_context="Madeira wine's history spans over 500 years, initially used as ballast on trading ships where the heat and motion transformed the wine into something unique. The island became a key stop on Atlantic trade routes, making Madeira famous across Europe and the Americas.")
for yr, qd, pt, sn in [
    (2000,"excellent","speculative","Beginning to show the complexity and oxidative depth that defines mature Madeira."),
    (2005,"exceptional","speculative","A legendary year across all styles; wines of remarkable concentration and longevity."),
    (2010,"very_good","stable","Fine vintage showing good balance between fruit and Madeira's characteristic acidity."),
    (2015,"excellent","rising","Excellent ripeness levels across all varieties; particularly successful for Malmsey."),
    (2018,"very_good","stable","A fine modern vintage demonstrating Madeira's consistent quality from volcanic soils."),
    (2020,"good","stable","Fresh year producing elegant wines with Madeira's characteristic mineral backbone."),
]:
    VIN(r5, yr, qd, pt, sn)

p8 = P("Blandy's Madeira", "winery", r5, "Portugal",
       production_philosophy="traditional_methods",
       philosophy_description="The most famous Madeira house, Blandy's has produced wine on the island since 1811. Their range spans 5-year NV to century-old colheitas, representing Madeira's full spectrum from dry Sercial to rich Malmsey.",
       reputation_narrative="Blandy's is Madeira's most recognized house internationally, with a range of single-variety wines that have introduced countless wine lovers to the island's unique fortified styles.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Blandy's 10 Year Malmsey Madeira", "wine_still", p8, r5, "Portugal",
                    subcategory="madeira_malmsey", description="10-year-aged Malmsey (Malvasia) — rich, sweet, with caramel, dried apricot, orange peel, coffee, and a piercing acidity that lifts the sweetness. Madeira's most luscious style.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Crème brûlée with vanilla", "complement", "classic", "dessert", "Malmsey's caramel and dried fruit mirror the brûlée's custard richness; Madeira's acidity prevents cloying.")
    PAIR(prod, "Dark chocolate truffles with sea salt", "complement", "classic", "dessert", "Coffee and caramel notes in the Malmsey bridge to dark chocolate; salt heightens the wine's sweetness.")
    PAIR(prod, "Christmas pudding with brandy butter", "complement", "classic", "dessert", "Rich, dried fruit Madeira and Christmas pudding share overlapping flavours — a timeless festive pairing.")
    PAIR(prod, "Roquefort with honeycomb", "contrast", "established", "cheese", "Malmsey's sweetness contrasts Roquefort's salt-funk; the wine's acidity keeps the balance perfect.")
prod, is_new = PROD("Blandy's 10 Year Verdelho Madeira", "wine_still", p8, r5, "Portugal",
                    subcategory="madeira_verdelho", description="Off-dry Verdelho with 10 years canteiro ageing. Smoke, dried citrus, honey, hazelnut, and a savoury rancio complexity — one of Madeira's most versatile food wines.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Confit duck with orange and spice", "complement", "established", "main", "Verdelho's dried citrus and smokiness mirror confit duck's richness; honey notes bridge the orange component.")
    PAIR(prod, "Roasted foie gras terrine with fig", "complement", "established", "starter", "The wine's acidity cuts through foie richness; honey and citrus notes echo the fig accompaniment.")
    PAIR(prod, "Smoked meats charcuterie board", "complement", "established", "starter", "Verdelho's smokiness and savoury rancio complement cured meats; off-dry sweetness balances salt.")
    PAIR(prod, "Pâté de campagne with cornichons", "bridge", "established", "starter", "Rancio complexity bridges to the pâté's depth; cornichon's acidity echoes the wine's own lively character.")

p9 = P("Barbeito Madeira", "winery", r5, "Portugal",
       production_philosophy="minimal_intervention",
       philosophy_description="An independent family producer known for single-cask, terroir-driven Madeiras using the canteiro system (natural barrel heating). Barbeito's wines are celebrated for their purity, transparency, and ability to express individual variety and vintage character.",
       reputation_narrative="Barbeito is Madeira's most respected artisan producer, favoured by collectors for their small-batch, single-cask wines that demonstrate Madeira's extraordinary ageing potential and variety expression.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Barbeito Ricardo Freitas Sercial Madeira", "wine_still", p9, r5, "Portugal",
                    subcategory="madeira_sercial", description="Single-cask dry Sercial from the canteiro system — bone dry, intensely acidic, with lime zest, salted almonds, smoke, and a mineral volcanic finish. One of Madeira's most demanding and rewarding styles.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled langoustines with bisque", "complement", "established", "starter", "Sercial's high acidity and saline mineral notes mirror langoustine brininess; smoke adds depth.")
    PAIR(prod, "Sea urchin on toast with butter and chive", "complement", "adventurous", "amuse", "The wine's dry salinity and mineral complexity bridge to sea urchin's oceanic richness.")
    PAIR(prod, "Marinated anchovies with pickled peppers", "complement", "established", "starter", "Bone-dry Sercial's acidity cuts anchovy oil; saline notes reinforce the preserved fish's brininess.")
    PAIR(prod, "Aged manchego with salted almonds", "complement", "classic", "cheese", "Salted almond notes in the wine mirror aged manchego's texture; Sercial's acidity cuts through fat.")

# === DB STATE ===
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")
print("B162 complete.")
cur.close()
conn.close()
