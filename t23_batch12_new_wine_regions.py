#!/usr/bin/env python3
"""T23 Batch 12 — New wine regions: Moravia (Czech Republic), Itata Valley (Chile), Elgin (South Africa), Anderson Valley AVA (USA), Aglianico del Vulture DOC (Italy)"""

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

# ── MORAVIA (CZECH REPUBLIC) ─────────────────────────────────────
print("\n=== Moravia (Czech Republic) ===")
r_mor = R("Moravia", "Czech Republic", "wine",
           designation_type="PDO",
           designation_name="Moravian PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The heartland of Czech wine production, accounting for 96% of all Czech vineyards. Moravia's sub-regions — Znojmo, Velke Pavlovice, Slovacko, and Mikulov — produce aromatic whites from Welschriesling, Grüner Veltliner, and the indigenous Pálava, a Gewürztraminer-Müller-Thurgau cross producing intensely aromatic wines of genuine distinction.",
           key_producers="Nové Vinařství, Sonberk, Vinselekt Michlovský, Chateau Lednice, Thaya",
           historical_context="Winemaking in Moravia dates to the Roman era; the Mikulov region's limestone terroir has produced wine continuously for over 2,000 years. After decades of Soviet collective farming that prioritized quantity over quality, the 1989 Velvet Revolution unleashed a generation of passionate winemakers. The Pálava variety — bred at Mikulov's wine research institute in 1977 — has become the region's signature wine internationally.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Moravian vintage; Pálava and Welschriesling showed extraordinary aromatic complexity from the limestone Mikulov terroir."),
    (2021, "very_good", "stable", "Classic central European vintage; Grüner Veltliner and Riesling excelled in the cooler Znojmo sub-region."),
    (2020, "excellent", "stable", "Benchmark year; Nové Vinařství and Sonberk produced internationally acclaimed Pálava and late harvest wines."),
    (2019, "exceptional", "rising", "Finest Moravian vintage in the modern era; ice wines and late harvest Pálava reached extraordinary concentration."),
    (2018, "very_good", "stable", "Solid vintage; the limestone subsoils of Mikulov delivered wines of excellent mineral freshness."),
]:
    VIN(r_mor, yr, qd, pt, sn)

p_son = P("Sonberk", "Czech Republic", r_mor,
           description="Moravia's most architecturally striking and critically acclaimed estate on the Pavlov limestone hills above the Nové Mlýny reservoir. Sonberk's Pálava and Riesling are considered the finest expressions of these varieties in the Czech Republic, attracting attention from international wine journalists.")
prod_son, new = PROD("Sonberk Palava", "wine_still", p_son, r_mor, "Czech Republic",
                     subcategory="Palava",
                     description="Moravia's indigenous aromatic variety at its finest — explosive lychee, rose petal, ginger, and apricot from Pavlov limestone with a long, mineral finish. A Czech original of world-class aromatic intensity, often compared to Alsatian Gewürztraminer.",
                     price_tier="premium")
if new:
    PAIR(prod_son, "Roasted pork neck with caraway, sauerkraut, and bread dumplings", "complement", "classic", "main", "The wine's aromatic intensity cuts through Czech cuisine's richness; caraway's spice finds direct resonance in Pálava's ginger notes")
    PAIR(prod_son, "Washed-rind cheese (Olomoucké tvarůžky) with rye bread and butter", "complement", "classic", "cheese", "Moravian pungent cheese and Pálava is a local classic — the wine's aromatic power matches the cheese's intensity; each lifts the other")

p_nov = P("Nové Vinařství", "Czech Republic", r_mor,
           description="Martin Vajčner's Velke Pavlovice estate producing natural, minimal-intervention wines from indigenous Moravian varieties. Nové Vinařství's Pálava and Svatomartinské wines have become cult items in Prague's natural wine bars and beyond.")
prod_nov, new = PROD("Nové Vinařství Welschriesling", "wine_still", p_nov, r_mor, "Czech Republic",
                     subcategory="Welschriesling",
                     description="Mineral, crisp, and refreshingly direct — Moravian Welschriesling from the Velke Pavlovice limestone terroir. Green apple, white flower, citrus zest, and a streak of Moravian mineral freshness. Ideal as a food wine and café partner.",
                     price_tier="mid_range")
if new:
    PAIR(prod_nov, "Smažený sýr (fried cheese) with tartare sauce and potato salad", "complement", "classic", "main", "The wine's bright acidity cuts through the battered cheese; its crisp character refreshes the palate between every bite")
    PAIR(prod_nov, "Carp fillet with brown butter, lemon, and parsley", "complement", "established", "main", "Czech Christmas carp and Moravian white — the wine's citrus and mineral character mirrors the freshwater fish; lemon is already built in")

# ── ITATA VALLEY (CHILE) ─────────────────────────────────────────
print("\n=== Itata Valley (Chile) ===")
r_ita = R("Itata Valley", "Chile", "wine",
           designation_type="DO",
           designation_name="Itata Valley DO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Chile's ancient wine heartland south of the Bio Bio river, where Spanish missionaries planted País and Muscat of Alexandria on granite soils 400 years ago. These old-vine, dry-farmed vineyards — many pre-dating Phylloxera — produce wines of haunting transparency and mineral purity now championed by Chile's natural wine movement. País, once scorned as peasant wine, has become one of the world's most exciting rediscoveries.",
           key_producers="De Martino, Clos des Fous, Louis-Antoine Luyt, Milan, Cacique Maravilla",
           historical_context="Itata's oldest vines were planted by Jesuit and Franciscan missionaries in the 17th century. The region was dismissed for generations as producing cheap wine for domestic consumption. Chilean sommeliers Rodrigo Zaror and winemakers like Louis-Antoine Luyt and Roberto Henríquez ignited the global interest in old-vine País around 2010, fundamentally changing how the world views Chile's viticultural heritage.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Itata vintage; old-vine País from granite soils showed extraordinary transparent fruit purity."),
    (2021, "very_good", "stable", "Classic southern Chilean vintage; the cool rainfall pattern favored Muscat and País equally."),
    (2020, "excellent", "stable", "Benchmark year; the natural wine community discovered Itata Valley's old-vine treasures in force."),
    (2019, "excellent", "rising", "Landmark vintage; De Martino and Clos des Fous raised international awareness of old-vine País."),
    (2018, "very_good", "stable", "Solid vintage; the 400-year-old vines' resilience produced wines of uncommon mineral depth."),
]:
    VIN(r_ita, yr, qd, pt, sn)

p_dem = P("De Martino", "Chile", r_ita,
           description="One of Chile's most innovative and progressive wineries, leading the revival of old-vine País and Muscat of Alexandria in Itata Valley. De Martino's Viejas Tinajas series ferments in ancient clay amphorae and is considered the benchmark for Chilean heritage wine.")
prod_dem, new = PROD("De Martino Viejas Tinajas Muscat", "wine_still", p_dem, r_ita, "Chile",
                     subcategory="Muscat of Alexandria",
                     description="Old-vine Muscat of Alexandria fermented in ancient clay tinajas — wildly aromatic, textural, and compelling. Orange blossom, dried apricot, ginger, and honey with a mineral grip from the granite soils. One of Chile's most unique and exciting wines.",
                     price_tier="premium")
if new:
    PAIR(prod_dem, "Ceviche de congrio (kingclip) with tiger's milk and cilantro", "complement", "established", "starter", "The wine's orange blossom and citrus intensity amplifies the ceviche's brightness; textural clay vessel character adds intrigue")
    PAIR(prod_dem, "Pebre (Chilean salsa) with empanadas de pino", "complement", "classic", "amuse", "Aromatic Muscat and Chile's herbal condiment find common ground; the wine's honey notes complement the empanada's savory filling")

p_clo = P("Clos des Fous", "Chile", r_ita,
           description="Pedro Parra, Francois Massoc, and partners' terroir-driven project producing wines from extreme Chilean sites including old-vine Itata País. Parra's geological expertise informs every viticultural decision; the wines are among Chile's most critically acclaimed natural wines.")
prod_clo, new = PROD("Clos des Fous Pais", "wine_still", p_clo, r_ita, "Chile",
                     subcategory="Pais",
                     description="Old-vine País from Itata's ancient granite soils — translucent garnet, wild cherry, dried strawberry, herbs, and the haunting mineral transparency that makes this forgotten variety so compelling. Minimally interventionist, naturally fermented.",
                     price_tier="mid_range")
if new:
    PAIR(prod_clo, "Cazuela de ave (Chilean chicken stew) with corn and pumpkin", "complement", "classic", "main", "The wine's transparency and bright cherry fruit complement the stew's mild richness without overwhelming; herbs in both bridge the pairing")
    PAIR(prod_clo, "Charcuterie board with longaniza, queso fresco, and sopaipillas", "complement", "established", "aperitif", "Old-vine País's light structure and wild fruit character cuts through the cured meats; sopaipilla's warmth echoes the wine's spice")

# ── ELGIN WO (SOUTH AFRICA) ──────────────────────────────────────
print("\n=== Elgin (South Africa) ===")
r_elg = R("Elgin", "South Africa", "wine",
           designation_type="WO",
           designation_name="Elgin WO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="South Africa's coolest wine ward in the apple-growing highlands of the Overberg, 45km east of Cape Town at 200-500m altitude. Elgin's continental maritime climate and ancient Bokkeveld shale soils produce Sauvignon Blanc, Pinot Noir, and Chardonnay of striking European elegance — a dramatic contrast to the warm-climate wines of Stellenbosch and Paarl.",
           key_producers="Paul Cluver, Almenkerk, Iona, Shannon, Elgin Vintners",
           historical_context="Elgin was established as a wine appellation only in 1999, making it one of South Africa's newest wards. The region's apple orchards dominated until winemakers recognized that the cool climate producing world-class apples could do the same for cool-climate varieties. Paul Cluver, whose family has farmed Elgin for generations, became the ward's pioneer and standard-bearer.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Elgin vintage; Sauvignon Blanc of razor-sharp precision and Pinot Noir of haunting mineral transparency."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; Chardonnay from Bokkeveld shale showed exceptional Burgundian elegance."),
    (2020, "exceptional", "rising", "Finest Elgin vintage in the modern era; Paul Cluver Seven Flags Pinot gained international cult status."),
    (2019, "excellent", "stable", "Benchmark year; international critics compared Elgin Sauvignon Blanc to the finest Sancerre."),
    (2018, "very_good", "stable", "Solid vintage; the Bokkeveld shale delivered wines of extraordinary mineral freshness and aging potential."),
]:
    VIN(r_elg, yr, qd, pt, sn)

p_clu = P("Paul Cluver Estate Wines", "South Africa", r_elg,
           description="The Cluver family's pioneering estate in the Elgin highlands, established in 1896 as an apple farm and converted to wine production. Paul Cluver's Seven Flags Pinot Noir is South Africa's most acclaimed cool-climate red wine; his Sauvignon Blanc and Riesling have set the benchmark for Elgin's style.")
prod_clu, new = PROD("Paul Cluver Seven Flags Pinot Noir", "wine_still", p_clu, r_elg, "South Africa",
                     subcategory="Pinot Noir",
                     description="South Africa's most celebrated cool-climate Pinot Noir from ancient Bokkeveld shale at altitude. Red cherry, blood orange, dried rose, forest floor, and the distinctive saline minerality of Elgin's ancient soils. Burgundian in transparency, South African in intensity.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_clu, "Roasted springbok loin with fynbos-smoked salt and confit beetroot", "complement", "classic", "main", "South African game and South Africa's finest Pinot — springbok's lean gaminess is lifted by the wine's cherry transparency; fynbos smoke echoes the shale mineral")
    PAIR(prod_clu, "Seared salmon with preserved lemon gremolata and Elgin apple butter", "complement", "established", "main", "A regional pairing — Elgin's apple heritage in the butter meets Elgin's finest wine; salmon's fat is cut by Pinot's bright acidity")

p_alm = P("Almenkerk Wine Estate", "South Africa", r_elg,
           description="Belgian-owned Elgin estate producing Sauvignon Blanc and Bordeaux blends of striking European character. Almenkerk's Lace Sauvignon Blanc is considered one of South Africa's finest expressions of the variety — precise, mineral, and age-worthy.")
prod_alm, new = PROD("Almenkerk Lace Sauvignon Blanc", "wine_still", p_alm, r_elg, "South Africa",
                     subcategory="Sauvignon Blanc",
                     description="Elgin's most precise and mineral Sauvignon Blanc from Bokkeveld shale — flint, gooseberry, cut grass, green fig, and a long saline finish. The cool altitude produces acidity and minerality that rivals the finest Loire Valley expressions. Age-worthy and profound.",
                     price_tier="premium")
if new:
    PAIR(prod_alm, "Oysters on the half shell with mignonette and lemon", "complement", "classic", "aperitif", "Mineral Sauvignon Blanc and briny oysters — one of gastronomy's most enduring pairings; Elgin's flint character mirrors the shell's mineral")
    PAIR(prod_alm, "Cape Malay fish curry (pickled fish) with apricot and turmeric", "complement", "established", "main", "South African culinary heritage — the wine's bright acidity and green fruit cuts through the curry's richness; apricot finds resonance in the wine's fruit")

# ── ANDERSON VALLEY AVA (USA) ─────────────────────────────────────
print("\n=== Anderson Valley AVA (USA) ===")
r_and = R("Anderson Valley", "USA", "wine",
           designation_type="AVA",
           designation_name="Anderson Valley AVA",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="California's northernmost and most distinctive cool-climate wine region in Mendocino County, where the Anderson Valley's deep canyon channels Pacific fog and cool air from the coast. Famous for Pinot Noir, Gewürztraminer, and Alsatian varieties that thrive in conditions utterly unlike the rest of California. Also the source of premium sparkling wine base wines for Roederer Estate.",
           key_producers="Navarro Vineyards, Littorai, Husch Vineyards, Roederer Estate, Breggo",
           historical_context="Anderson Valley was long dominated by orchards, timber, and the ranching culture of Boonville — a town with its own unique dialect ('Boontling'). Navarro Vineyards pioneered Alsatian varieties in the 1970s after Ted Bennett and Deborah Cahn recognized that the foggy valley was more Alsace than California. Roederer Estate's 1988 establishment confirmed the valley's sparkling wine potential.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Anderson Valley vintage; Pinot Noir of extraordinary elegance and Gewürztraminer of Alsatian aromatic intensity."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; La Fog creep produced wines of haunting mineral freshness."),
    (2020, "very_good", "stable", "Challenging smoke-taint year for some; estates with better site exposure produced excellent wines."),
    (2019, "exceptional", "rising", "Finest Anderson Valley vintage in a decade; Littorai and Navarro produced benchmark Pinot Noir and Gewürztraminer."),
    (2018, "excellent", "stable", "Benchmark year; Roederer Estate L'Ermitage became the highest-rated California sparkling wine of the vintage."),
]:
    VIN(r_and, yr, qd, pt, sn)

p_nav = P("Navarro Vineyards", "USA", r_and,
           description="Ted Bennett and Deborah Cahn's pioneering Anderson Valley estate that proved Alsatian varieties — particularly Gewürztraminer, Riesling, and Pinot Gris — could reach world-class quality in Mendocino County. Navarro's dry-farmed, certified organic vineyards have been producing benchmark cool-climate California wines since 1974.")
prod_nav, new = PROD("Navarro Deep End Blend Gewurztraminer", "wine_still", p_nav, r_and, "USA",
                     subcategory="Gewurztraminer",
                     description="California's finest Gewürztraminer from the Anderson Valley's coolest, deepest reaches — intensely aromatic, dry, and mineral. Rose petal, lychee, ginger, and white pepper with the valley's distinctive mineral acidity. Drier and more serious than Alsatian Vendange Tardive.",
                     price_tier="premium")
if new:
    PAIR(prod_nav, "Vietnamese pho with rare beef, tripe, and herb plate", "complement", "classic", "main", "Aromatic Gewürztraminer and Southeast Asian spice — the wine's lychee and ginger notes mirror the pho's aromatic complexity; the dry style prevents sweetness overload")
    PAIR(prod_nav, "Roasted Dungeness crab with drawn butter and sourdough", "complement", "established", "main", "Pacific Coast crab from the same fog-influenced coast — the wine's aromatic intensity complements the crab's sweetness; butter finds resonance in the wine's texture")

p_lit = P("Littorai Wines", "USA", r_and,
           description="Ted Lemon's biodynamic estate producing some of California's most celebrated Pinot Noir and Chardonnay from Anderson Valley and Sonoma Coast sites. Lemon's Burgundy training at Domaine Dujac informs wines of extraordinary elegance, transparency, and mineral complexity.")
prod_lit, new = PROD("Littorai Savoy Vineyard Pinot Noir", "wine_still", p_lit, r_and, "USA",
                     subcategory="Pinot Noir",
                     description="Ted Lemon's biodynamic Anderson Valley Pinot Noir from the ancient Savoy Vineyard — the benchmark for cool-climate California Pinot. Wild strawberry, cranberry, dried herbs, forest floor, and a Burgundian mineral precision that few California wines achieve. Long aging potential.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_lit, "Roasted squab with black truffle butter, lentils, and sorrel", "complement", "classic", "main", "The wine's transparency and forest floor character is the ideal partner for squab; truffle mirrors the Pinot's earthy depth; sorrel's acid lifts both")
    PAIR(prod_lit, "Grilled king salmon with pinot reduction, wild mushrooms, and thyme", "complement", "established", "main", "West Coast salmon and Pacific Coast Pinot — the wine's delicate cherry and mineral character lifts the salmon's richness; mushrooms echo the forest floor notes")

# ── AGLIANICO DEL VULTURE DOC (ITALY) ────────────────────────────
print("\n=== Aglianico del Vulture DOC (Italy) ===")
r_vul = R("Aglianico del Vulture", "Italy", "wine",
           designation_type="DOC",
           designation_name="Aglianico del Vulture DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Basilicata's legendary DOC on the slopes of Monte Vulture — an extinct volcano in the Apennine mountains of southern Italy. The volcanic basalt soils and significant diurnal temperature variation at 300-700m altitude produce wines of extraordinary depth, structured tannin, dark fruit intensity, and volcanic mineral character. Aglianico del Vulture is considered the 'Barolo of the South.'",
           key_producers="Elena Fucci, Paternoster, D'Angelo, Cantine del Notaio, Musto Carmelitano",
           historical_context="Aglianico — likely brought to southern Italy by Greek colonists as 'Hellenico' — has been grown on Monte Vulture's volcanic slopes for over 2,000 years. The DOC was established in 1971 but remained obscure until Elena Fucci's single-vineyard Titolo (first vintage 2000) brought Basilicata to international wine attention. The DOCG upgrade for Superiore wines came in 2010.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vulture vintage; Aglianico from the volcanic basalt showed extraordinary dark fruit intensity and structured elegance."),
    (2021, "very_good", "stable", "Classic Basilicata vintage; the Apennine diurnal shifts produced wines of exceptional freshness balancing power."),
    (2020, "excellent", "stable", "Benchmark year; Elena Fucci Titolo received 100-point scores from multiple international critics."),
    (2019, "exceptional", "rising", "Greatest Aglianico del Vulture vintage in a generation; wines of legendary structure and dark volcanic fruit."),
    (2018, "excellent", "stable", "Exceptional vintage; volcanic mineral character was more pronounced than any recent year; cellar-worthy wines."),
]:
    VIN(r_vul, yr, qd, pt, sn)

p_efu = P("Elena Fucci", "Italy", r_vul,
           description="The producer who single-handedly brought Basilicata to the world's attention. Elena Fucci's Titolo — the only wine produced from this tiny Monte Vulture estate — consistently receives Italy's highest critical scores and has established Aglianico del Vulture as one of the world's great wine regions.")
prod_efu, new = PROD("Elena Fucci Titolo Aglianico del Vulture", "wine_still", p_efu, r_vul, "Italy",
                     subcategory="Aglianico",
                     description="Italy's most celebrated southern red wine — a single-vineyard Aglianico from 40-year-old vines on Monte Vulture's volcanic basalt at 600m. Blackberry, dark cherry, tar, violet, volcanic ash, and iron with massive but fine-grained tannins. Demands 10+ years of cellaring. Italy's 'Barolo of the South' in its most complete form.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_efu, "Agnello alla Lucana (slow-braised lamb) with wild herbs and chilli", "complement", "classic", "main", "Basilicata's traditional lamb preparation and its greatest wine — the wine's volcanic iron character and structured tannins handle the rich braised lamb; wild herbs echo the wine's complexity")
    PAIR(prod_efu, "Aged Canestrato Pugliese (hard sheep's cheese) with black truffle and honey", "complement", "classic", "cheese", "Volcanic Aglianico and aged southern Italian sheep's cheese — the wine's tar and iron complexity matches the cheese's intensity; truffle bridges the volcanic mineral notes")

p_dag = P("D'Angelo", "Italy", r_vul,
           description="The Rionero in Vulture estate that established Aglianico del Vulture's international reputation in the 1970s and 1980s. Rocco D'Angelo and now his children produce elegant, age-worthy Aglianico that balances Monte Vulture's volcanic power with genuine finesse.")
prod_dag, new = PROD("D'Angelo Aglianico del Vulture", "wine_still", p_dag, r_vul, "Italy",
                     subcategory="Aglianico",
                     description="The classic Aglianico del Vulture expression from the region's oldest modern estate. Dark plum, sour cherry, volcanic mineral, dried herb, and leather with the variety's characteristic firm tannin structure. Requires aging but rewards patience with extraordinary complexity.",
                     price_tier="premium")
if new:
    PAIR(prod_dag, "Pasta al ragù di cinghiale (wild boar ragù) with hand-rolled orecchiette", "complement", "classic", "main", "Southern Italian game pasta and southern Italian volcanic red — the wine's dark fruit and tannic structure handles the boar's gaminess; volcanic minerals add complexity")
    PAIR(prod_dag, "Porcini mushroom and guanciale risotto with Parmigiano", "complement", "established", "main", "The wine's earthy and iron character finds natural resonance with porcini; guanciale's fat is structured by the wine's firm tannins; a central Italian bridge from south to north")

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
