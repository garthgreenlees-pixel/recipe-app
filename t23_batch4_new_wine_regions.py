#!/usr/bin/env python3
"""T23 Batch 4 — New wine regions: Languedoc, Prince Edward County, Rueda, Kakheti, Campania
Improvements:
  - PROD() returns (id, is_new) — PAIR only called on new inserts, preventing duplicates
  - All schema constraints verified against live DB before writing
"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    """reputation_tier: iconic/prestigious/respected/emerging/overlooked
       quality_trajectory: ascending/established/declining/emerging/rediscovering"""
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_regions
      (name, country, beverage_family, designation_type, designation_name,
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, beverage_family, designation_type, designation_name,
       reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    """quality_descriptor: exceptional/excellent/very_good/good/average/challenging/poor"""
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    """producer_type: winery/distillery/brewery/tea_garden/coffee_estate/sake_brewery/cidery/meadery/kombucha_brewery/multi_category"""
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
      (name, country, region_id, producer_type, reputation_narrative, authority_tier)
      VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    """Returns (id, is_new). Only call PAIR() when is_new=True to prevent duplicates."""
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── LANGUEDOC AOP ────────────────────────────────────────────────
print("\n=== Languedoc AOP ===")
r_lng = R("Languedoc", "France", "wine",
           designation_type="AOP",
           designation_name="Languedoc AOP",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="France's largest wine region stretching from the Rhone delta to the Pyrenees. Historically a bulk wine producer, now producing some of France's most exciting wines from Grenache, Syrah, Mourvedre, Carignan, and Roussanne at exceptional value.",
           key_producers="Grange des Peres, Mas de Daumas Gassac, Domaine de la Rectorie, Domaine Gauby, Peyre Rose",
           historical_context="The Languedoc was France's wine lake — vast quantities of mediocre wine for decades. The Vin de Pays revolution and the subsequent AOP reforms transformed quality perceptions from the 1980s onwards.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding growing season; concentrated, structured reds with remarkable freshness for the southern latitude."),
    (2021, "very_good", "stable", "Cooler vintage producing elegant Languedoc with better acidity than the decade average."),
    (2020, "excellent", "rising", "Classic Languedoc vintage — powerful, ripe, long-lived reds from Grenache and Mourvedre."),
    (2019, "excellent", "stable", "Dry, warm season; excellent Grenache ripeness with good freshness in higher-altitude blocks."),
    (2018, "very_good", "stable", "Solid vintage; Carignan and Syrah particularly successful in cooler sub-appellations."),
]:
    VIN(r_lng, yr, qd, pt, sn)

p_gdp = P("Grange des Peres", "France", r_lng,
           description="Laurent Vaille's legendary estate producing Languedoc's most sought-after red and white wines from a unique blend of southern and northern Rhone varieties. Minimal intervention, maximum terroir expression.")
prod_gdp, new = PROD("Grange des Peres Rouge", "wine_still", p_gdp, r_lng, "France",
                      subcategory="Syrah Blend",
                      description="Blend of Syrah, Mourvedre, and Counoise from granite and limestone terraces. Dense, complex, and age-worthy — dark berry, iron, garrigue, and extraordinary length. One of France's cult wines.",
                      price_tier="ultra_premium")
if new:
    PAIR(prod_gdp, "Shoulder of lamb slow-roasted with herbes de Provence", "complement", "classic", "main", "Garrigue aromatics echo the regional herbs; Mourvedre's animal notes harmonize with the lamb's richness")
    PAIR(prod_gdp, "Wild boar stew with juniper and black olive tapenade", "complement", "established", "main", "The wine's iron and dark fruit intensity matches the game's wild character; tapenade mirrors the olive notes")

p_mdg = P("Mas de Daumas Gassac", "France", r_lng,
           description="Aime Guibert's iconic estate that proved Languedoc could produce world-class wine. The red Grand Vin — mostly Cabernet Sauvignon — shocked the wine world in the 1970s and defined the region's ambition.")
prod_mdg, new = PROD("Mas de Daumas Gassac Grand Vin Rouge", "wine_still", p_mdg, r_lng, "France",
                      subcategory="Cabernet Sauvignon",
                      description="Predominantly Cabernet Sauvignon from unique glacial soils, aged in old oak. Combines Bordeaux structure with Mediterranean warmth — cassis, cedar, garrigue, and extraordinary longevity.",
                      price_tier="premium")
if new:
    PAIR(prod_mdg, "Grilled entrecote with shallot confit and pommes frites", "complement", "classic", "main", "Cabernet's structure and cassis intensity embrace the beef; the wine's garrigue notes add Mediterranean depth")
    PAIR(prod_mdg, "Aged Combalou Roquefort with walnut bread and quince", "complement", "established", "cheese", "Cabernet tannins cut through the rich sheep's cheese; cassis and quince find sweet resonance")

# ── PRINCE EDWARD COUNTY VQA ──────────────────────────────────────
print("\n=== Prince Edward County VQA ===")
r_pec = R("Prince Edward County", "Canada", "wine",
           designation_type="VQA",
           designation_name="Prince Edward County VQA",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Ontario's most exciting emerging wine region on a limestone peninsula in Lake Ontario, producing remarkable cool-climate Chardonnay and Pinot Noir. The unique Hillier Clay Limestone soils produce wines of Burgundian elegance and transparency.",
           key_producers="Closson Chase, Trail Estate, Hinterland, Rosehall Run, By Chadsey's Cairns",
           historical_context="Commercial wine production began only in the 1990s; the County achieved VQA sub-appellation status in 2007. Its limestone soils and extreme climate have attracted winemakers seeking true cool-climate expression.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Ideal growing conditions; Chardonnay achieved benchmark mineral precision and Pinot Noir showed extraordinary elegance."),
    (2021, "very_good", "stable", "Cool season with good acid retention; textbook County Pinot Noir with haunting Burgundian character."),
    (2020, "good", "stable", "Challenging early season followed by excellent autumn; resilient producers made focused, site-expressive wines."),
    (2019, "excellent", "rising", "Outstanding vintage; warm summer with perfect autumn — the finest Chardonnay the County had produced to that point."),
    (2018, "very_good", "stable", "Solid vintage; limestone minerality particularly pronounced across all varieties."),
]:
    VIN(r_pec, yr, qd, pt, sn)

p_cc = P("Closson Chase Vineyards", "Canada", r_pec,
          description="The County's benchmark estate, producing Chardonnay and Pinot Noir of Burgundian elegance from the limestone Closson Chase terroir. Proprietor Deborah Paskus's vision defined what Prince Edward County wine could become.")
prod_cc, new = PROD("Closson Chase Chardonnay", "wine_still", p_cc, r_pec, "Canada",
                    subcategory="Chardonnay",
                    description="Estate Chardonnay from limestone-clay soils showing classic County minerality — white peach, green apple, wet stone, and a long saline finish. Restraint and terroir expression over winemaking technique.",
                    price_tier="premium")
if new:
    PAIR(prod_cc, "Butter-poached Lake Ontario pickerel with chive and lemon beurre blanc", "complement", "classic", "main", "Limestone minerality echoes the freshwater fish's delicacy; restrained oak complements the butter sauce")
    PAIR(prod_cc, "Mushroom risotto with aged Ontario Parmesan and truffle", "complement", "established", "main", "The wine's mineral core cuts through risotto richness; truffle finds resonance in the wine's earthy complexity")

p_tr = P("Trail Estate Winery", "Canada", r_pec,
          description="Newer estate making waves in Prince Edward County with single-vineyard Chardonnay and Pinot Noir from limestone-heavy blocks. Winemaker Mackenzie Brisbois brings Burgundian training to County limestone.")
prod_tr, new = PROD("Trail Estate Pinot Noir", "wine_still", p_tr, r_pec, "Canada",
                    subcategory="Pinot Noir",
                    description="Cool-climate Pinot Noir from County limestone clay, transparent and haunting — wild strawberry, rose hip, earth, and delicate limestone minerality with silky tannins.",
                    price_tier="premium")
if new:
    PAIR(prod_tr, "Duck confit with cherry gastrique and wild mushrooms", "complement", "classic", "main", "Pinot's cherry and earth notes harmonize with the duck; cherry gastrique echoes the wine's fruit character")
    PAIR(prod_tr, "Roasted beet and goat cheese salad with candied walnuts", "complement", "established", "starter", "The wine's wild strawberry transparency mirrors the beet's earthy sweetness; goat cheese acidity lifts both")

# ── RUEDA DO ─────────────────────────────────────────────────────
print("\n=== Rueda DO ===")
r_rue = R("Rueda", "Spain", "wine",
           designation_type="DO",
           designation_name="Rueda DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Castile y Leon DO on the high plateau (700-800m altitude) producing Spain's finest Verdejo wines — vibrant, aromatic whites with a distinctive herbal bitterness. Also makes outstanding Sauvignon Blanc and some Tinto Fino reds.",
           key_producers="Bodega Naia, Marques de Riscal, Jose Pariente, Bodegas Mocen, Ossian",
           historical_context="Rueda was nearly destroyed by phylloxera but Verdejo survived on ungrafted vines in pockets. The DO was established in 1980, making it one of Spain's first white wine DOs; high altitude and chalky clay soils produce wines of exceptional freshness.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding growing season at altitude; Verdejo of exceptional aromatic intensity and mineral precision."),
    (2022, "very_good", "stable", "Warm year balanced by altitude; ripe, expressive Verdejo with good acid structure."),
    (2021, "excellent", "stable", "Classic high-altitude Rueda — bracing acidity, intense herbal aromatics, long finish."),
    (2020, "good", "stable", "Warmer vintage; best results from higher-elevation and clay-heavy blocks."),
    (2019, "very_good", "stable", "Benchmark Rueda vintage — textbook Verdejo with maximum aromatic expression."),
]:
    VIN(r_rue, yr, qd, pt, sn)

p_nai = P("Bodega Naia", "Spain", r_rue,
           description="One of Rueda's most admired artisan producers, crafting single-vineyard Verdejo of exceptional depth and aging potential. Naia's old-vine ferment-on-skins Verdejo challenges every assumption about the variety.")
prod_nai, new = PROD("Naia Verdejo", "wine_still", p_nai, r_rue, "Spain",
                     subcategory="Verdejo",
                     description="Concentrated Verdejo from old vines at altitude — fennel, white stone fruit, bitter almond, and a saline-mineral finish. More textural than the crisp archetype; built for the table.",
                     price_tier="mid_range")
if new:
    PAIR(prod_nai, "Jamon Iberico de bellota with pan con tomate", "complement", "classic", "aperitif", "Verdejo's bitter almond note echoes the acorn-finished ham; the wine's acidity cuts through the fat")
    PAIR(prod_nai, "Grilled sea bream with roasted garlic and herbs", "complement", "classic", "main", "The wine's fennel and herb aromatics mirror the Mediterranean preparation; acidity lifts the delicate fish")

p_jop = P("Jose Pariente", "Spain", r_rue,
           description="Family winery founded by Victoria Pariente, a pioneer of modern Rueda. The estate produces benchmark Verdejo and Sauvignon Blanc showcasing the DO's aromatic intensity and altitude-driven freshness.")
prod_jop, new = PROD("Jose Pariente Verdejo", "wine_still", p_jop, r_rue, "Spain",
                     subcategory="Verdejo",
                     description="Clean, vibrant estate Verdejo — citrus zest, white stone fruit, herbal bitterness, and excellent acidity. Textbook Rueda expression of freshness and drinkability at premium quality.",
                     price_tier="mid_range")
if new:
    PAIR(prod_jop, "Gazpacho with burrata and basil oil", "complement", "established", "starter", "The wine's citrus brightness amplifies the tomato's acidity; herbal bitterness finds resonance with the basil")
    PAIR(prod_jop, "Crab tostadas with avocado and pickled jalapeno", "complement", "established", "starter", "Verdejo's herbal-citrus character lifts the crab's sweetness; the wine's brisk acidity cuts the avocado richness")

# ── KAKHETI ──────────────────────────────────────────────────────
print("\n=== Kakheti ===")
r_kak = R("Kakheti", "Georgia", "wine",
           designation_type="PDO",
           designation_name="Kakheti PDO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Georgia's primary wine region in the Alazani River valley, producing the world's oldest wine tradition in qvevri (clay amphorae buried underground). Rkatsiteli and Saperavi are the flagship varieties; amber wines from extended skin-contact are Kakheti's global signature.",
           key_producers="Pheasant's Tears, Alaverdi Monastery, Telavi Wine Cellar, Gotsa Family Wines, Shalauri Wine Cellar",
           historical_context="Archaeological evidence suggests wine production in Kakheti dates to 6000 BCE — the oldest documented winemaking in human history. The Soviet era industrialized production; the post-independence revival of qvevri winemaking began in the 2000s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Ideal conditions in the Alazani valley; Rkatsiteli achieved exceptional amber wine complexity and Saperavi deep fruit intensity."),
    (2021, "very_good", "stable", "Good growing season with well-timed rainfall; traditional qvevri wines of authentic character."),
    (2020, "excellent", "stable", "Benchmark year for both amber whites and Saperavi reds; international attention at its peak."),
    (2019, "very_good", "stable", "Classic Kakheti vintage; the amber wines showed extraordinary textural complexity."),
    (2018, "good", "stable", "Solid vintage; best results from producers with old-vine Rkatsiteli in clay-heavy soils."),
]:
    VIN(r_kak, yr, qd, pt, sn)

p_pht = P("Pheasant's Tears", "Georgia", r_kak,
           description="John Wurdeman's pioneering natural wine estate that introduced Kakheti's qvevri wines to the international fine wine world. The winery's commitment to traditional methods and native varieties defines the Georgian wine renaissance.")
prod_pht, new = PROD("Pheasant's Tears Rkatsiteli", "wine_still", p_pht, r_kak, "Georgia",
                     subcategory="Rkatsiteli",
                     description="Classic amber wine from 6 months of skin contact in qvevri. The archetypal Georgian expression — dried apricot, chamomile, walnut tannins, and extraordinary textural depth with tangy, oxidative notes.",
                     price_tier="mid_range")
if new:
    PAIR(prod_pht, "Grilled chicken with walnut sauce (Satsivi) and pomegranate", "complement", "classic", "main", "Regional pairing of ancient depth — walnut tannins in wine echo the walnut sauce; amber texture embraces the roasted chicken")
    PAIR(prod_pht, "Cheese platter with aged Sulguni and honeycomb", "complement", "classic", "cheese", "Amber wine's oxidative character is the traditional Georgian cheese pairing; the honey bridges the walnut tannins")

p_ala = P("Alaverdi Monastery", "Georgia", r_kak,
           description="One of Georgia's oldest and most revered wine institutions — a functioning monastery producing qvevri wines using traditions maintained since the 11th century. The monks' Rkatsiteli and Saperavi are deeply authentic.")
prod_ala, new = PROD("Alaverdi Monastery Saperavi", "wine_still", p_ala, r_kak, "Georgia",
                     subcategory="Saperavi",
                     description="Traditional qvevri-fermented Saperavi from the monastery's ancient vineyards. Deeply colored, tannic, and complex — dark plum, blackberry, pomegranate, and earthy tannins with extraordinary aging potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ala, "Lamb and herb dumplings (Khinkali) with tkemali plum sauce", "complement", "classic", "main", "Regional pairing — Saperavi's dark fruit and tannic grip cut through the lamb fat; plum sauce echoes the wine's fruit")
    PAIR(prod_ala, "Slow-roasted pork belly with pomegranate glaze and walnuts", "complement", "established", "main", "Saperavi's pomegranate acidity cuts through the pork fat; the wine's tannins embrace the caramelized glaze")

# ── CAMPANIA DOC ─────────────────────────────────────────────────
print("\n=== Campania DOC ===")
r_cam = R("Campania", "Italy", "wine",
           designation_type="DOC",
           designation_name="Campania DOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Southern Italian wine region centred on Naples, producing some of Italy's most compelling indigenous varieties — Fiano di Avellino, Greco di Tufo, and Aglianico del Taurasi. Ancient volcanic soils create wines of extraordinary mineral complexity.",
           key_producers="Feudi di San Gregorio, Mastroberardino, Marisa Cuomo, I Favati, Villa Raiano",
           historical_context="Campania was Falerno and the wines of ancient Rome. After centuries of decline, master producer Antonio Mastroberardino revived Taurasi and the indigenous varieties in the 20th century; a new generation has elevated quality to international prominence.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Volcanic growing season with ideal heat accumulation; Aglianico achieved exceptional tannic ripeness and aromatic complexity."),
    (2021, "very_good", "stable", "Well-balanced vintage; Fiano di Avellino particularly successful with bright acidity and mineral depth."),
    (2020, "exceptional", "rising", "Outstanding Campania vintage; Taurasi from this year destined for multi-decade cellaring."),
    (2019, "excellent", "stable", "Benchmark expressions of Fiano and Greco; whites showed remarkable precision and aging potential."),
    (2018, "very_good", "stable", "Consistent vintage; indigenous varieties expressed volcanic terroir with authenticity."),
]:
    VIN(r_cam, yr, qd, pt, sn)

p_fsg = P("Feudi di San Gregorio", "Italy", r_cam,
           description="Campania's most internationally acclaimed estate, producing benchmark Taurasi DOCG, Fiano di Avellino DOCG, and Greco di Tufo DOCG. Their Serpico and Patrimo single-vineyard wines are among Southern Italy's finest.")
prod_fsg, new = PROD("Feudi di San Gregorio Fiano di Avellino", "wine_still", p_fsg, r_cam, "Italy",
                     subcategory="Fiano",
                     description="DOCG Fiano from volcanic tuff soils in Avellino — hazelnut, white peach, fennel, and honeyed minerality with a long, smoky finish. One of Southern Italy's finest white wines.",
                     price_tier="premium")
if new:
    PAIR(prod_fsg, "Whole roasted branzino with capers, olives, and preserved lemon", "complement", "classic", "main", "Fiano's volcanic minerality and hazelnut notes complement the Mediterranean fish; fennel aromatics mirror the herb")
    PAIR(prod_fsg, "Linguine alle vongole with white wine and parsley", "complement", "classic", "main", "Regional pairing of deep authenticity — Campanian Fiano and Campanian clams share volcanic mineral intensity")

p_mas = P("Mastroberardino", "Italy", r_cam,
           description="The legendary family estate that saved Campania's indigenous varieties from extinction. Antonio Mastroberardino's championing of Aglianico, Fiano, and Greco redefined Southern Italian wine quality in the 20th century.")
prod_mas, new = PROD("Mastroberardino Aglianico Radici", "wine_still", p_mas, r_cam, "Italy",
                     subcategory="Aglianico",
                     description="The estate's flagship Taurasi-style Aglianico from volcanic slopes — dense blackberry, iron, tobacco, and volcanic tannins. Needs 10+ years of cellaring to reveal its extraordinary complexity.",
                     price_tier="premium")
if new:
    PAIR(prod_mas, "Slow-braised short rib with porcini mushrooms and polenta", "complement", "classic", "main", "Aglianico's iron-rich tannins and dark fruit power embrace the collagen-rich short rib; porcini amplifies earthy depth")
    PAIR(prod_mas, "Grilled lamb cutlets with garlic, rosemary, and anchovy butter", "complement", "established", "main", "Volcanic tannins cut through the lamb fat; rosemary and anchovy mirror the wine's savoury, iron minerality")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
