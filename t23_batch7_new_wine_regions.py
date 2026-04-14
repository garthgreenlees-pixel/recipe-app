#!/usr/bin/env python3
"""T23 Batch 7 — New wine regions: Galilee (Israel), Cafayate (Argentina), Rheinhessen, Pico Island (Azores), Pic Saint-Loup"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
    cur.execute("""INSERT INTO beverage_producers
      (name, country, region_id, producer_type, reputation_narrative, authority_tier)
      VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
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

# ── GALILEE (ISRAEL) ─────────────────────────────────────────────
print("\n=== Galilee (Israel) ===")
r_gal = R("Galilee", "Israel", "wine",
           designation_type="GI",
           designation_name="Galilee GI",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Israel's premier wine region in the Upper Galilee and Golan Heights, producing structured reds and aromatic whites from high-altitude volcanic and limestone terroirs. Merlot, Cabernet Sauvignon, Syrah, and Viognier excel in the cooler mountain climate.",
           key_producers="Golan Heights Winery, Galil Mountain, Yarden, Pelter, Dalton",
           historical_context="Winemaking in Galilee dates to biblical times. Modern quality production began with the establishment of Golan Heights Winery in 1983, which demonstrated that cool-altitude sites could produce world-class wine. The region's elevation (400-1200m) is crucial to quality.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Cabernet Sauvignon and Merlot from high-altitude sites showed remarkable structure and freshness."),
    (2021, "very_good", "stable", "Classic Galilee vintage; cooler conditions produced elegant reds with good acidity."),
    (2020, "excellent", "stable", "Warm vintage with excellent ripeness; Syrah and Viognier from the slopes excelled."),
    (2019, "excellent", "rising", "Benchmark year; Yarden wines from this vintage achieved international critical acclaim."),
    (2018, "very_good", "stable", "Solid vintage across all varieties; consistent quality from the major estates."),
]:
    VIN(r_gal, yr, qd, pt, sn)

p_yar = P("Yarden Winery", "Israel", r_gal,
           description="The flagship label of Golan Heights Winery, Israel's most internationally acclaimed wine producer. Yarden Cabernet Sauvignon and Yarden El Rom consistently rank among the Middle East's finest wines.")
prod_yar, new = PROD("Yarden Cabernet Sauvignon", "wine_still", p_yar, r_gal, "Israel",
                     subcategory="Cabernet Sauvignon",
                     description="Benchmark Israeli Cabernet from high-altitude Golan Heights — cassis, dark cherry, cedar, and Mediterranean garrigue with structured tannins and genuine aging potential. Consistent and internationally award-winning.",
                     price_tier="premium")
if new:
    PAIR(prod_yar, "Slow-roasted lamb with za'atar, pomegranate, and tahini", "complement", "classic", "main", "Middle Eastern spice profile mirrors the wine's Mediterranean garrigue; pomegranate acidity balances the Cabernet's fruit")
    PAIR(prod_yar, "Lamb kofta with harissa, yogurt, and fresh herbs", "complement", "established", "main", "Cabernet's dark fruit and structure handle the spiced lamb; the wine's cedar notes harmonize with the herb-rich preparation")

p_gal = P("Galil Mountain Winery", "Israel", r_gal,
           description="A joint venture between Kibbutz Yiron and Golan Heights Winery in the Upper Galilee highlands (900m), producing elegant red blends and an outstanding Syrah from basalt and limestone terroirs.")
prod_gal, new = PROD("Galil Mountain Syrah", "wine_still", p_gal, r_gal, "Israel",
                     subcategory="Syrah",
                     description="Cool-climate Syrah from 900m altitude — dark berry, violet, black olive, and white pepper with elegant tannins and mountain freshness. A revelation from the Middle East.",
                     price_tier="mid_range")
if new:
    PAIR(prod_gal, "Roasted eggplant with tahini, pomegranate seeds, and mint", "complement", "established", "starter", "Syrah's olive and violet notes mirror the roasted eggplant; pomegranate's acidity bridges the wine's dark fruit")
    PAIR(prod_gal, "Grilled lamb chops with ras el hanout and preserved lemon couscous", "complement", "classic", "main", "Israeli Syrah and lamb is a natural partnership; the wine's olive and pepper character echoes the Moroccan spice blend")

# ── CAFAYATE (ARGENTINA) ──────────────────────────────────────────
print("\n=== Cafayate (Argentina) ===")
r_caf = R("Cafayate", "Argentina", "wine",
           designation_type="GI",
           designation_name="Cafayate GI",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="High-altitude wine valley in Salta Province, Argentina (1700-2000m), home to the world's most distinctive Torrontes — Argentina's signature white grape. Also producing elegant Malbec and Tannat at extraordinary altitude. The combination of altitude, sun, and cool nights produces wines of unique aromatic intensity.",
           key_producers="El Esteco, Domingo Molina, Clos de los Siete, Bodega Nanni, Lavaque",
           historical_context="Cafayate's viticulture dates to the Jesuit missions of the 17th century. The valley's isolation and extreme altitude preserved traditional winemaking and indigenous varieties. International recognition came in the 1990s as Torrontes attracted global attention for its extraordinary aromatics.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage at altitude; Torrontes of exceptional floral intensity and Malbec with remarkable freshness."),
    (2021, "very_good", "stable", "Classic Cafayate vintage; the diurnal temperature range produced wines of exceptional aromatic precision."),
    (2020, "excellent", "stable", "Ideal conditions; El Esteco and Domingo Molina produced benchmark Torrontes of extraordinary complexity."),
    (2019, "excellent", "stable", "Landmark vintage; high-altitude Malbec from Cafayate showed that altitude can transform the variety."),
    (2018, "very_good", "stable", "Solid vintage across all varieties; Torrontes showed its classic rose-geranium-peach character."),
]:
    VIN(r_caf, yr, qd, pt, sn)

p_est = P("El Esteco", "Argentina", r_caf,
           description="Cafayate's most historic estate, producing Torrontes and Malbec from high-altitude vineyards in Salta. The Don David reserve range and single-vineyard expressions are considered Argentina's finest Salta wines.")
prod_est, new = PROD("El Esteco Don David Torrontes", "wine_still", p_est, r_caf, "Argentina",
                     subcategory="Torrontes",
                     description="Reserve Torrontes from 1750m altitude — an explosion of rose petal, white peach, apricot, and orange blossom with crisp, refreshing acidity. Argentina's most distinctive indigenous white variety at its finest.",
                     price_tier="mid_range")
if new:
    PAIR(prod_est, "Ceviche with aji amarillo, red onion, and tiger's milk", "complement", "established", "starter", "Torrontes' floral-citrus intensity mirrors the aji amarillo's exotic aromatics; the wine's acidity echoes the tiger's milk")
    PAIR(prod_est, "Grilled prawns with garlic, lime, and fresh coriander", "complement", "classic", "starter", "Torrontes' aromatic intensity and high acidity is the perfect foil for grilled shellfish; floral notes mirror the coriander")

p_mol = P("Domingo Molina", "Argentina", r_caf,
           description="Small artisan estate in the Cafayate valley producing single-vineyard Torrontes and high-altitude Malbec of extraordinary character. One of Argentina's most sought-after boutique producers.")
prod_mol, new = PROD("Domingo Molina Torrontes", "wine_still", p_mol, r_caf, "Argentina",
                     subcategory="Torrontes",
                     description="Single-vineyard Torrontes from 2000m altitude — the most aromatic expression of Argentina's signature grape. Rose water, jasmine, stone fruit, and saline mineral finish from the ancient desert soils.",
                     price_tier="premium")
if new:
    PAIR(prod_mol, "Empanadas de humita with corn, cheese, and aji mirasol", "complement", "classic", "amuse", "Torrontes' floral aromatics and fresh acidity cut through the corn richness; the wine's fruit mirrors the aji pepper's sweetness")
    PAIR(prod_mol, "Spiced lamb mechoui with chermoula and flatbread", "complement", "established", "main", "The wine's perfumed intensity handles the lamb spice; floral notes mirror the chermoula herb and citrus character")

# ── RHEINHESSEN ───────────────────────────────────────────────────
print("\n=== Rheinhessen ===")
r_rhe = R("Rheinhessen", "Germany", "wine",
           designation_type="Gebiet",
           designation_name="Rheinhessen",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Germany's largest wine region south of Mainz, historically associated with Liebfraumilch but now producing world-class Riesling, Spatburgunder (Pinot Noir), and Silvaner from the Rhine terraces and Roter Hang hillside. A quiet revolution in quality has made this Germany's most exciting emerging region.",
           key_producers="Kuhling-Gillot, Wittmann, Battenfeld-Spanier, Kruger-Rumpf, Schales",
           historical_context="Rheinhessen was Germany's 'wine lake' for decades — vast quantities of sweet Liebfraumilch destined for British supermarkets. The VDP wine reform and a new generation of quality-focused growers transformed the region's image; the Roter Hang vineyards are now recognized as Germany's finest Riesling terroir outside the Mosel.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Riesling from the Roter Hang achieved exceptional mineral depth and Spatburgunder showed Burgundian elegance."),
    (2021, "very_good", "stable", "Cool, classic vintage; Riesling of piercing acidity and Silvaner from Westhofen excelled."),
    (2020, "exceptional", "rising", "The finest Rheinhessen vintage in decades; Wittmann and Battenfeld-Spanier produced epochal Rieslings."),
    (2019, "excellent", "stable", "Warm vintage producing concentrated, age-worthy Riesling from the best sites."),
    (2018, "excellent", "stable", "Outstanding conditions; Spatburgunder from clay soils achieved extraordinary depth and color."),
]:
    VIN(r_rhe, yr, qd, pt, sn)

p_wit = P("Wittmann", "Germany", r_rhe,
           description="Philipp Wittmann's biodynamic estate in Westhofen is considered Rheinhessen's finest producer. His GG Kirchspiel and Morstein Rieslings rival the Mosel's best, and his Spatburgunder has established Rheinhessen as a serious Pinot Noir appellation.")
prod_wit, new = PROD("Wittmann Riesling Trocken", "wine_still", p_wit, r_rhe, "Germany",
                     subcategory="Riesling",
                     description="Estate Riesling from biodynamic Westhofen vineyards — pristine, mineral, and dry. Lime, white grapefruit, herbal bitterness, and the characteristic Rheinhessen loess mineral note. Entry into one of Germany's great estates.",
                     price_tier="premium")
if new:
    PAIR(prod_wit, "White asparagus with hollandaise and Westphalian ham", "complement", "classic", "main", "The classic German Spargel season pairing — dry Riesling's acidity cuts through the hollandaise; herbal bitterness echoes the asparagus")
    PAIR(prod_wit, "Trout meuniere with capers and brown butter", "complement", "classic", "main", "Biodynamic Riesling's mineral precision and citrus acidity is the ideal partner for freshwater fish; the wine mirrors the caper brine")

p_bsp = P("Battenfeld-Spanier", "Germany", r_rhe,
           description="H.O. Spanier's radical biodynamic estate at Hohen-Sulzen produces Riesling and Spatburgunder that challenge any German wine in quality. The estate's near-zero-intervention philosophy and ancient organic soils produce wines of extraordinary complexity.")
prod_bsp, new = PROD("Battenfeld-Spanier Spatburgunder", "wine_still", p_bsp, r_rhe, "Germany",
                     subcategory="Spatburgunder",
                     description="Biodynamic Pinot Noir (Spatburgunder) from limestone and loess — pale ruby, delicate, and haunting. Wild strawberry, rose hip, dried herbs, and a long mineral finish. One of Germany's finest Pinot Noirs.",
                     price_tier="premium")
if new:
    PAIR(prod_bsp, "Roasted duck with braised red cabbage and potato dumplings", "complement", "classic", "main", "German Spatzle cuisine and Spatburgunder is a regional classic; the wine's delicate fruit is not overwhelmed by the duck's richness")
    PAIR(prod_bsp, "Mushroom risotto with Schwarzwald ham and aged Emmental", "complement", "established", "main", "The wine's earthy complexity mirrors the mushroom intensity; German ham adds a smoky resonance")

# ── PICO ISLAND (AZORES) ─────────────────────────────────────────
print("\n=== Pico Island (Azores) ===")
r_pic = R("Pico Island", "Portugal", "wine",
           designation_type="DOC",
           designation_name="Pico DOC",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Volcanic island in the Atlantic Azores, producing one of the world's most unusual wines from Verdelho growing in UNESCO World Heritage basalt rock enclosures (currais) within metres of the ocean. The combination of Atlantic humidity, volcanic basalt, and oceanic spray creates wines of extraordinary mineral and saline intensity.",
           key_producers="Cooperativa Vitivinicola da Ilha do Pico, Antonio Macanita, Curral Atlantis",
           historical_context="Pico wine was exported to Russia and Brazil in the 18th century as a luxury product. Phylloxera destroyed the vineyards in 1852; the current basalt enclosure system (currais) was built in the 1860s and is now a UNESCO World Heritage Site since 2004.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Verdelho of extraordinary saline mineral intensity and Atlantic freshness."),
    (2021, "very_good", "stable", "Classic Atlantic vintage; the oceanic influence produced wines of haunting mineral salinity."),
    (2020, "excellent", "stable", "Ideal conditions; volcanic basalt yielded Verdelho of exceptional complexity and aging potential."),
    (2019, "excellent", "stable", "Benchmark year; the UNESCO currais produced wines that excited international collectors."),
    (2018, "very_good", "stable", "Solid vintage; the Atlantic spray and basalt created characteristic oceanic mineral character."),
]:
    VIN(r_pic, yr, qd, pt, sn)

p_mac = P("Antonio Macanita", "Portugal", r_pic,
           description="Antonio Macanita is the visionary winemaker who brought modern winemaking knowledge to the Azores without sacrificing the islands' unique character. His Frei Gigante from Pico and Terceira are considered the finest Azorean wines ever produced.")
prod_mac, new = PROD("Antonio Macanita Frei Gigante Verdelho", "wine_still", p_mac, r_pic, "Portugal",
                     subcategory="Verdelho",
                     description="Verdelho from pre-phylloxera vines grown in ancient basalt currais within metres of the Atlantic. Saline, volcanic, and haunting — dried apricot, beeswax, ocean spray, and a mineral finish unlike any wine on earth.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mac, "Freshly shucked Atlantic oysters with lemon", "complement", "classic", "aperitif", "The wine's oceanic salinity and volcanic minerality mirrors the oyster's terroir; an expression of pure Atlantic identity")
    PAIR(prod_mac, "Grilled limpets (lapas) with garlic and lemon butter", "complement", "classic", "starter", "The Azores' iconic dish and Pico wine are inseparable — both are expressions of the same volcanic Atlantic place")

p_cur = P("Curral Atlantis", "Portugal", r_pic,
           description="Small artisan producer working exclusively from the UNESCO basalt currais of Pico, producing Verdelho of exceptional authenticity and saline mineral intensity. One of Portugal's most individual wine estates.")
prod_cur, new = PROD("Curral Atlantis Verdelho do Pico", "wine_still", p_cur, r_pic, "Portugal",
                     subcategory="Verdelho",
                     description="Traditional Verdelho from the oldest basalt enclosures on the island — oxidative notes, sea spray minerality, dried tropical fruit, and a finish that evolves with extraordinary length.",
                     price_tier="premium")
if new:
    PAIR(prod_cur, "Caldo verde (kale and chourico soup) with corn bread", "complement", "classic", "starter", "Verdelho's oxidative richness and saline character harmonize with the chourico's smoke; Atlantic wine meets Atlantic food")
    PAIR(prod_cur, "Octopus rice with paprika and black-eyed beans", "complement", "established", "main", "The wine's volcanic mineral intensity mirrors the oceanic depth of the octopus; paprika finds resonance in the oxidative notes")

# ── PIC SAINT-LOUP ───────────────────────────────────────────────
print("\n=== Pic Saint-Loup ===")
r_psl = R("Pic Saint-Loup", "France", "wine",
           designation_type="AOC",
           designation_name="Pic Saint-Loup AOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The most acclaimed Languedoc sub-appellation, north of Montpellier under the spectacular limestone ridge of the Pic Saint-Loup. Grenache, Syrah, and Mourverdre produce elegant, structured reds that outperform the broader Languedoc appellation and rival southern Rhone at a fraction of the price.",
           key_producers="Chateau de Cazeneuve, Mas Bruguiere, Domaine de l'Hortus, Clos Marie, Ermitage du Pic Saint-Loup",
           historical_context="Pic Saint-Loup achieved its own AOC in 2017 after decades as a sub-appellation. The limestone ridge creates a cooler microclimate than the surrounding Languedoc plain — altitude (250-400m) and calcareous soils produce wines of genuine elegance. The Cistercian monks of Valmagne were growing grapes here in the 12th century.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "The finest vintage in Pic Saint-Loup's modern history; Syrah-Grenache of extraordinary elegance and mineral depth."),
    (2021, "very_good", "stable", "Cool Atlantic influence produced elegant, classical wines with excellent freshness."),
    (2020, "excellent", "stable", "Outstanding Pic Saint-Loup vintage; Mas Bruguiere and l'Hortus produced wines of rare complexity."),
    (2019, "excellent", "stable", "Benchmark conditions; the rocky calcareous soils produced wines of exceptional mineral transparency."),
    (2018, "very_good", "stable", "Solid vintage; the limestone terroir delivered characteristic restraint and elegance."),
]:
    VIN(r_psl, yr, qd, pt, sn)

p_bru = P("Mas Bruguiere", "France", r_psl,
           description="The estate that defined Pic Saint-Loup's identity and reputation. Guilhem Bruguiere produces La Grenadiere and other cuvees from organic limestone vineyards under the ridge. One of southern France's finest and most authentic estates.")
prod_bru, new = PROD("Mas Bruguiere La Grenadiere", "wine_still", p_bru, r_psl, "France",
                     subcategory="Grenache Blend",
                     description="The estate's flagship blend of Grenache, Syrah, and Mourverdre from old limestone vines — violets, dark cherry, garrigue, and white pepper. Elegant structure with 10+ years of aging potential.",
                     price_tier="premium")
if new:
    PAIR(prod_bru, "Roasted rack of lamb with lavender jus and flageolet beans", "complement", "classic", "main", "Grenache's violet and dark cherry notes harmonize with the lamb; lavender mirrors the garrigue character of the wine")
    PAIR(prod_bru, "Wild mushroom tart with goat cheese and thyme", "complement", "established", "starter", "The wine's earthy complexity mirrors the mushroom intensity; limestone minerality finds affinity with the aged goat cheese")

p_hor = P("Domaine de l'Hortus", "France", r_psl,
           description="Jean Orliac's elegant estate under the Pic Saint-Loup limestone ridge producing Classique and Grande Cuvee red blends and an outstanding Viognier white from cool north-facing slopes.")
prod_hor, new = PROD("Domaine de l'Hortus Grande Cuvee", "wine_still", p_hor, r_psl, "France",
                     subcategory="Syrah Blend",
                     description="Grand cuvee Syrah-Grenache from the oldest, lowest-yielding vines on the property — concentrated, elegant, and mineral. Dark berry, iron, garrigue, and white pepper. Needs 5-8 years minimum.",
                     price_tier="premium")
if new:
    PAIR(prod_hor, "Slow-braised lamb shoulder with olives, tomato, and herbes de Provence", "complement", "classic", "main", "Syrah's iron and dark berry character is the classic southern French lamb pairing; olive notes in the wine find resonance")
    PAIR(prod_hor, "Grilled Cote de boeuf with garlic confit and green peppercorn sauce", "complement", "established", "main", "The wine's structure handles the beef's richness; garrigue notes from the wine mirror the herbes de Provence seasoning")

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
