#!/usr/bin/env python3
"""T23 Batch 8 — New wine regions: Uco Valley, Tenerife, Corsica, Nemea PDO, England"""

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

# ── UCO VALLEY (ARGENTINA) ───────────────────────────────────────
print("\n=== Uco Valley (Argentina) ===")
r_uco = R("Uco Valley", "Argentina", "wine",
           designation_type="GI",
           designation_name="Valle de Uco GI",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Argentina's most exciting wine sub-region within Mendoza, at 1000-1500m altitude in the shadow of the Andes. Gualtallary, Altamira, and Los Chacayes sub-zones produce Malbec and white varieties of extraordinary refinement — higher acidity, more defined structure, and longer aging potential than the valley floor.",
           key_producers="Zuccardi, Achaval Ferrer, Clos de los Siete, Clos des Cimes, Catena Zapata",
           historical_context="The Uco Valley emerged as Argentina's fine wine frontier in the 2000s, when altitude-seeking producers discovered that Gualtallary's alluvial limestone soils and extreme diurnal temperature range produced Malbec with Burgundian elegance. Zuccardi's Valle de Uco wines set the international benchmark.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "The finest Uco Valley vintage in the modern era; Gualtallary Malbec of extraordinary mineral precision and Chardonnay of Burgundian elegance."),
    (2021, "excellent", "rising", "Outstanding vintage; Altamira and Los Chacayes produced Malbec of rare freshness and structural definition."),
    (2020, "very_good", "stable", "Excellent conditions; old-vine Malbec at altitude showed exceptional complexity and aging potential."),
    (2019, "excellent", "stable", "Benchmark Uco Valley vintage; Zuccardi Jose Zuccardi from this year considered among Argentina's greatest."),
    (2018, "very_good", "stable", "Solid vintage; the limestone sub-zones consistently produced more refined Malbec than the valley floor."),
]:
    VIN(r_uco, yr, qd, pt, sn)

p_zuc = P("Zuccardi Valle de Uco", "Argentina", r_uco,
           description="The definitive Uco Valley estate, producing Argentina's finest and most internationally acclaimed single-vineyard Malbecs from Gualtallary's limestone soils. Sebastian Zuccardi's commitment to place-based winemaking has transformed the global perception of Argentine wine.")
prod_zuc, new = PROD("Zuccardi Jose Zuccardi Malbec", "wine_still", p_zuc, r_uco, "Argentina",
                     subcategory="Malbec",
                     description="Argentina's most celebrated single-vineyard wine from Gualtallary limestone at 1200m. Extraordinary mineral precision, dark violet, blackberry, and iron with Burgundian-like terroir transparency and 15+ year aging potential.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_zuc, "Asado de tira (short ribs) over parrilla with chimichurri", "complement", "classic", "main", "Argentina's greatest wine and its most iconic food tradition — Uco Valley Malbec and asado are inseparable; the wine's mineral depth handles the char")
    PAIR(prod_zuc, "Empanadas de carne with raisin, hard-boiled egg, and cumin", "complement", "established", "amuse", "The wine's dark fruit and iron complexity pairs naturally with the sweet-savoury meat filling; cumin mirrors the wine's earthy depth")

p_ach = P("Achaval Ferrer", "Argentina", r_uco,
           description="Roberto Cipresso and partners produce single-parcel Malbecs from old vines in Lujan de Cuyo and Uco Valley that are considered among Argentina's most complex and age-worthy wines. The Quimera blend and single-vineyard Malbecs define Argentine quality.")
prod_ach, new = PROD("Achaval Ferrer Malbec Finca Mirador", "wine_still", p_ach, r_uco, "Argentina",
                     subcategory="Malbec",
                     description="Single-parcel Malbec from Uco Valley, aged in French oak — dark violet, plum, leather, and floral notes with the mountain freshness that defines the valley's finest expressions.",
                     price_tier="premium")
if new:
    PAIR(prod_ach, "Grilled bife de chorizo (sirloin) with Maldon salt and herbs", "complement", "classic", "main", "Argentine Malbec and sirloin is the classic pairing; the wine's plum fruit and leather notes complement the char")
    PAIR(prod_ach, "Mollejas (sweetbreads) with lemon and wild herbs", "complement", "established", "main", "Malbec's floral notes and dark fruit handle the rich sweetbreads; the wine's freshness from altitude prevents the pairing from becoming heavy")

# ── TENERIFE DO (CANARY ISLANDS) ─────────────────────────────────
print("\n=== Tenerife DO (Canary Islands) ===")
r_ten = R("Tenerife", "Spain", "wine",
           designation_type="DO",
           designation_name="Tenerife DO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="The Canary Islands' most important wine island, producing extraordinary volcanic wines from pre-phylloxera Listan Negro, Negramoll, and Listan Blanco vines grown on lava soils at altitude. The island's five DOs range from the Atlantic coast to 1700m on Teide's slopes, creating extraordinary terroir diversity.",
           key_producers="Suertes del Marques, Envinate, Monje, Tajinaste, Vinatigo",
           historical_context="The Canary Islands were spared by phylloxera — the volcanic soil and island isolation preserved pre-phylloxera vines that now grow ungrafted. These ancient vines, some over 200 years old, are among the oldest wine-producing plants in the world. Shakespeare's Falstaff drank 'sack' from the Canaries.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Listan Negro of exceptional volcanic complexity and Listan Blanco of saline precision."),
    (2021, "very_good", "stable", "Classic Atlantic vintage; wines of haunting mineral character from the ancient ungrafted vines."),
    (2020, "excellent", "stable", "Benchmark year; Suertes and Envinate produced wines that excited the international natural wine world."),
    (2019, "excellent", "rising", "Landmark vintage for Tenerife; old-vine expressions of extraordinary volcanic authenticity."),
    (2018, "very_good", "stable", "Solid vintage; the volcanic basalt delivered characteristic mineral intensity across all varieties."),
]:
    VIN(r_ten, yr, qd, pt, sn)

p_sue = P("Suertes del Marques", "Spain", r_ten,
           description="The estate that put Tenerife on the international wine map, producing old-vine Listan Negro wines from La Orotava valley that are collected worldwide. Jonatan Garcia Lima's minimal-intervention approach reveals the extraordinary character of the ancient volcanic terroir.")
prod_sue, new = PROD("Suertes del Marques 7 Fuentes", "wine_still", p_sue, r_ten, "Spain",
                     subcategory="Listan Negro",
                     description="Blend from seven ancient parcels of pre-phylloxera Listan Negro on volcanic lava soils — red cherry, dried strawberry, volcanic ash, orange peel, and extraordinary mineral transparency. Weightless yet profound.",
                     price_tier="premium")
if new:
    PAIR(prod_sue, "Grilled cherne (grouper) with mojo rojo and papas arrugadas", "complement", "classic", "main", "The Canary Islands' iconic pairing — volcanic fish-grape terroir unity; mojo rojo's paprika echoes the wine's volcanic mineral character")
    PAIR(prod_sue, "Grilled octopus with smoked paprika and salt-baked potatoes", "complement", "established", "main", "Light Listan Negro's transparency complements the octopus without overpowering; volcanic minerality echoes the oceanic ingredient")

p_env = P("Envinate", "Spain", r_ten,
           description="The visionary natural wine collective that explored Tenerife, Ribeira Sacra, and the Canary Islands, producing wines of extraordinary transparency and volcanic character. Their Tagon Tenerife wines are among Spain's most sought-after natural wines.")
prod_env, new = PROD("Envinate Tagon Tenerife", "wine_still", p_env, r_ten, "Spain",
                     subcategory="Listan Negro",
                     description="Natural Listan Negro from old ungrafted vines on volcanic lava soils — delicate ruby, cranberry, volcanic ash, wild herbs, and saline Atlantic mineral energy. Fragile, haunting, and irreplaceable.",
                     price_tier="premium")
if new:
    PAIR(prod_env, "Fresh white goat cheese (quesillo canario) with miel de palma", "complement", "classic", "aperitif", "The wine's light fruit and volcanic mineral transparency pairs beautifully with the delicate island goat cheese; palm honey bridges")
    PAIR(prod_env, "Carne de cabra (goat stew) with coriander and cumin", "complement", "established", "main", "Regional island pairing — light Listan Negro's transparency handles goat without fat-heaviness; the wine's wild herb notes mirror the stew")

# ── CORSICA AOP ──────────────────────────────────────────────────
print("\n=== Corsica AOP ===")
r_cor = R("Corsica", "France", "wine",
           designation_type="AOP",
           designation_name="Vin de Corse AOP",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The island of beauty's wine appellation, producing distinctive reds, whites, and roses from indigenous varieties — Nielluccio (related to Sangiovese), Sciacarello, and Vermentino. Granite and schist terroirs and Mediterranean climate create wines of vivid fruit, herbal intensity, and island character.",
           key_producers="Antoine Arena, Domaine Comte Abbatucci, Clos Canarelli, Yves Leccia, Domaine de Vacelli",
           historical_context="Corsica's wine history stretches back to Greek colonization (600 BCE) at Alalia. The island's isolation preserved indigenous varieties extinct elsewhere in the Mediterranean. Antoine Arena's rediscovery of Patrimonio's Vermentino and Nielluccio in the 1960s launched the modern quality era.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Nielluccio of extraordinary depth and Vermentino showing exceptional mineral complexity."),
    (2021, "very_good", "stable", "Elegant island vintage; Sciacarello's herbal character was particularly pronounced and defined."),
    (2020, "excellent", "stable", "Benchmark Corsican conditions; Arena's Patrimonio wines from this vintage are among his finest."),
    (2019, "excellent", "stable", "Classic Corsican vintage; the granite terroirs delivered wines of exceptional mineral transparency."),
    (2018, "very_good", "stable", "Solid vintage; Domaine Abbatucci produced his finest Ajaccio Sciacarello in years."),
]:
    VIN(r_cor, yr, qd, pt, sn)

p_are = P("Antoine Arena", "France", r_cor,
           description="The pioneer of fine Corsican wine, Antoine Arena's Patrimonio estate produces Nielluccio and Vermentino of world-class quality. His Carco and Morta Maio cuvees are considered the island's greatest wines.")
prod_are, new = PROD("Antoine Arena Patrimonio Bianco", "wine_still", p_are, r_cor, "France",
                     subcategory="Vermentino",
                     description="Arena's benchmark Vermentino from granite Patrimonio terroir — white flowers, citrus pith, bitter almond, and extraordinary mineral salinity. One of France's most distinctive and least-known great whites.",
                     price_tier="premium")
if new:
    PAIR(prod_are, "Grilled red mullet with tapenade and grilled fennel", "complement", "classic", "main", "Island wine and island fish — Vermentino's bitter almond and saline character complements the mullet's sweet flesh; fennel mirrors the floral notes")
    PAIR(prod_are, "Brocciu cheese tart with lemon zest and fresh mint", "complement", "classic", "cheese", "Corsica's fresh sheep's cheese is the traditional Vermentino partner — the wine's acidity cuts the cheese fat; mint mirrors the floral aromatics")

p_abb = P("Domaine Comte Abbatucci", "France", r_cor,
           description="Jean-Charles Abbatucci's legendary estate in Ajaccio produces Sciacarello-based reds and blended whites from ancient indigenous varieties preserved through 200 years of family viticulture. The estate is considered a living museum of Corsican varieties.")
prod_abb, new = PROD("Domaine Abbatucci Faustine Blanc", "wine_still", p_abb, r_cor, "France",
                     subcategory="Sciacarello Blanc",
                     description="White Sciacarello from old vines — an incredibly rare variety that produces wines of extraordinary herbal intensity, orange blossom, bitter almond, and granite mineral character. A wine unlike anything in France.",
                     price_tier="premium")
if new:
    PAIR(prod_abb, "Wild boar terrine with cornichons and Dijon mustard", "complement", "established", "starter", "The wine's herbal intensity and granite mineral notes cut through the game richness; island wild boar and island Sciacarello find natural affinity")
    PAIR(prod_abb, "Charcuterie Corsica — lonzu, coppa, figatellu with fig jam", "complement", "classic", "aperitif", "Corsican charcuterie and Corsican white wine are the island's great aperitif tradition; the wine's bitter almond mirrors the figatellu's liver intensity")

# ── NEMEA PDO ────────────────────────────────────────────────────
print("\n=== Nemea PDO ===")
r_nem = R("Nemea", "Greece", "wine",
           designation_type="PDO",
           designation_name="Nemea PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The Peloponnese's most important wine appellation, dedicated exclusively to Agiorgitiko (St. George's grape) — a rich, velvety red variety producing wines from light roses to powerful, age-worthy reds. Three altitude zones (200-900m) create dramatically different expressions from the same grape.",
           key_producers="Gaia Estate, Skouras, Palivos Estate, Tetramythos, Parparoussis",
           historical_context="Nemea is the site of Hercules' first labor (the Nemean lion) and one of ancient Greece's great wine regions. The Agiorgitiko grape has been cultivated here for at least 2500 years. Modern quality focus began with George Skouras in the 1980s; Gaia's Gaia Estate established the PDO's international reputation in the 1990s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; high-altitude Agiorgitiko showed extraordinary structure and complexity."),
    (2021, "very_good", "stable", "Elegant vintage with good acid retention; medium-altitude wines of exceptional finesse."),
    (2020, "excellent", "stable", "Classic Nemea conditions; Gaia Estate produced one of its finest vintages."),
    (2019, "excellent", "stable", "Benchmark year for all altitude zones; the upper Nemea (Koutsi) wines showed Burgundian elegance."),
    (2018, "very_good", "stable", "Solid vintage; oak-aged Agiorgitiko from this year showed exceptional integration and depth."),
]:
    VIN(r_nem, yr, qd, pt, sn)

p_gai = P("Gaia Estate", "Greece", r_nem,
           description="Yiannis Paraskevopoulos and Leon Karatsalos founded Gaia to produce wines from Nemea's highest-altitude Agiorgitiko vines and Santorini's Assyrtiko. Gaia Notios and 14-18h Agiorgitiko are considered Greece's finest reds.")
prod_gai, new = PROD("Gaia Estate Agiorgitiko", "wine_still", p_gai, r_nem, "Greece",
                     subcategory="Agiorgitiko",
                     description="Flagship Nemea Agiorgitiko from high-altitude vineyards — dark cherry, sweet spice, velvety tannins, and earthy complexity. The most refined expression of Greece's finest red grape.",
                     price_tier="premium")
if new:
    PAIR(prod_gai, "Slow-roasted lamb with oregano, lemon, and kritharaki", "complement", "classic", "main", "Greek lamb and Agiorgitiko is the national pairing of the Peloponnese; the wine's velvety tannins and dark fruit embrace the lamb's richness")
    PAIR(prod_gai, "Moussaka with cinnamon-spiced lamb and bechamel", "complement", "classic", "main", "Agiorgitiko's sweet spice notes harmonize with the cinnamon; the wine's tannins cut through the bechamel richness")

p_sko = P("Skouras Winery", "Greece", r_nem,
           description="George Skouras is the visionary who transformed Nemea's reputation in the 1980s-90s. His Megas Oenos blend and single-vineyard Agiorgitiko wines have won international acclaim and defined the PDO's modern identity.")
prod_sko, new = PROD("Skouras Megas Oenos", "wine_still", p_sko, r_nem, "Greece",
                     subcategory="Agiorgitiko",
                     description="Skouras' benchmark Nemea blend of Agiorgitiko with Cabernet Sauvignon — dark plum, tobacco, Mediterranean herbs, and structured tannins. A wine that bridges Greek tradition and international ambition.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sko, "Beef stifado with pearl onions, cinnamon, and cloves", "complement", "classic", "main", "Greek beef stew with sweet spice finds natural resonance in Agiorgitiko's velvety fruit and earthy depth")
    PAIR(prod_sko, "Grilled lamb chops with skordalia and horta greens", "complement", "established", "main", "Simple grilled lamb with garlic puree is the traditional Greek taverna pairing with Nemea red; the wine's structure handles the garlic intensity")

# ── ENGLAND (SPARKLING) ──────────────────────────────────────────
print("\n=== England (Sparkling) ===")
r_eng = R("England", "United Kingdom", "wine",
           designation_type="PDO",
           designation_name="English Wine PDO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="England's wine industry has been transformed by climate change and chalk terroirs in Sussex, Kent, and Hampshire that mirror Champagne's geology. Traditional method sparkling wines from Chardonnay, Pinot Noir, and Pinot Meunier now rival Champagne at international competitions. Over 900 vineyards now operate across England.",
           key_producers="Nyetimber, Ridgeview, Chapel Down, Hambledon, Gusbourne",
           historical_context="England had vineyards in Roman and medieval times, but the modern English wine industry truly began with commercial planting in the 1970s. The quality revolution came with Nyetimber in 1988, which produced traditional method sparkling wines that defeated Champagne houses at blind tastings in 2010.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "The finest English vintage on record; long dry summer produced sparkling wines of extraordinary ripeness and complexity."),
    (2021, "very_good", "stable", "Classic English vintage with good acid structure; traditional method wines of elegant Champagne-like character."),
    (2020, "excellent", "rising", "Outstanding conditions; Nyetimber and Ridgeview produced their finest wines in years."),
    (2019, "excellent", "rising", "Benchmark English vintage; international competitions saw English sparkling wines defeat Champagne houses."),
    (2018, "very_good", "stable", "Solid vintage across the home counties; chalk-derived minerality particularly pronounced."),
]:
    VIN(r_eng, yr, qd, pt, sn)

p_nye = P("Nyetimber", "United Kingdom", r_eng,
           description="The estate that created English sparkling wine's international reputation. Planted in 1988 with Champagne varieties specifically for traditional method sparkling wine. Nyetimber Classic Cuvee has defeated Champagne houses in blind tastings and is served at royal events.")
prod_nye, new = PROD("Nyetimber Classic Cuvee", "wine_sparkling", p_nye, r_eng, "United Kingdom",
                     subcategory="Traditional Method",
                     description="England's most celebrated sparkling wine — Chardonnay, Pinot Noir, and Pinot Meunier from Sussex chalk. Toasty, biscuity, with green apple, lemon cream, and the distinctive chalk mineral character of English sparkling wine.",
                     price_tier="premium")
if new:
    PAIR(prod_nye, "Cornish crab on toasted sourdough with chervil mayonnaise", "complement", "classic", "starter", "English sparkling wine and British seafood is the natural pairing; chalk minerality mirrors the crab's delicate sweetness")
    PAIR(prod_nye, "Smoked salmon blinis with creme fraiche and chives", "complement", "classic", "aperitif", "Autolysis and citrus character cut through the smoke; chalk minerality lifts the salmon's richness — a quintessentially British pairing")

p_rid = P("Ridgeview Wine Estate", "United Kingdom", r_eng,
           description="Roberts family estate in Sussex producing exclusively traditional method sparkling wines dedicated to specific Champagne-method approaches. Ridgeview's Bloomsbury, Cavendish, and Fitzrovia wines have achieved international critical acclaim.")
prod_rid, new = PROD("Ridgeview Bloomsbury", "wine_sparkling", p_rid, r_eng, "United Kingdom",
                     subcategory="Traditional Method",
                     description="Ridgeview's flagship blend from the Downs chalk — predominantly Chardonnay with Pinot Noir and Pinot Meunier. Vibrant, elegant, and mineral; white peach, almond, and distinctive English chalk terroir.",
                     price_tier="premium")
if new:
    PAIR(prod_rid, "Devonshire crab with samphire and lemon butter sauce", "complement", "classic", "main", "Sussex sparkling wine and Devon crab are natural county neighbours; the wine's minerality and citrus lift the delicate crab")
    PAIR(prod_rid, "Chicken liver parfait with sourdough toast and fig chutney", "complement", "established", "amuse", "The wine's toasty autolysis and acidity cut through the rich liver; fig chutney echoes the wine's subtle fruit character")

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
