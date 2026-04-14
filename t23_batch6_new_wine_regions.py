#!/usr/bin/env python3
"""T23 Batch 6 — New wine regions: Tokaj, Abruzzo, Umbria, Penedes, Finger Lakes"""

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

# ── TOKAJ ────────────────────────────────────────────────────────
print("\n=== Tokaj ===")
r_tok = R("Tokaj", "Hungary", "wine",
           designation_type="PDO",
           designation_name="Tokaj PDO",
           reputation_tier="iconic",
           quality_trajectory="ascending",
           description="Hungary's legendary wine region producing Tokaji Aszu — the world's original botrytised sweet wine, predating Sauternes by centuries. Furmint, Harslevelu, and Yellow Muscat thrive on volcanic loess and rhyolite tuff. Also producing world-class dry Furmint.",
           key_producers="Royal Tokaji, Disznoko, Oremus, Szepsy, Chateau Pajzos",
           historical_context="Tokaj was the first wine region in the world to be officially classified (1730). The Aszu wines were the most expensive in 18th-century Europe, valued by Russian tsars and French kings. Communist collectivization destroyed quality; post-1989 privatization and investment restored it.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Exceptional botrytis conditions; Aszu of remarkable concentration and freshness. Dry Furmint also at its finest."),
    (2021, "very_good", "stable", "More elegant style; Aszu with higher acidity and lower sugar than usual, promising extraordinary longevity."),
    (2020, "exceptional", "rising", "The finest Tokaj vintage in decades; 6 Puttonyos Aszu of legendary quality from Szepsy and Royal Tokaji."),
    (2019, "excellent", "stable", "Ideal botrytis development; classic vintage with perfect balance of sweetness and acidity."),
    (2017, "excellent", "stable", "Landmark dry Furmint vintage; crisp, mineral whites showing the variety's world-class potential."),
]:
    VIN(r_tok, yr, qd, pt, sn)

p_roy = P("Royal Tokaji", "Hungary", r_tok,
           description="The estate that relaunched Tokaj's international reputation, founded in 1990 by Hugh Johnson and a group of wine enthusiasts. Single-vineyard Aszu from classified First Growth vineyards (Nyulaszo, Betsek, Szt. Tamas) are the region's benchmarks.")
prod_roy, new = PROD("Royal Tokaji Aszu 5 Puttonyos", "wine_dessert", p_roy, r_tok, "Hungary",
                     subcategory="Tokaji Aszu",
                     description="Five-puttonyos Aszu from classified Tokaj vineyards — botrytised Furmint and Harslevelu of extraordinary sweetness and acidity. Apricot, orange peel, saffron, and volcanic minerality. Ageable for 30+ years.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_roy, "Roquefort with walnut bread and pear", "complement", "classic", "cheese", "The wine's apricot-saffron intensity against the cheese's salt and blue mold creates a classic sweet-savoury harmony")
    PAIR(prod_roy, "Foie gras torchon with brioche and Tokaji jelly", "complement", "classic", "starter", "The canonical pairing of the region — the wine's botrytised sweetness and acidity cut through the foie gras fat; a historic combination")

p_szep = P("Istvan Szepsy", "Hungary", r_tok,
            description="The greatest living Tokaj winemaker — Istvan Szepsy's family farm has produced Aszu from Királyudvar since the 17th century. His wines set the international benchmark for both sweet Aszu and dry Furmint.")
prod_szep, new = PROD("Szepsy Furmint Dry", "wine_still", p_szep, r_tok, "Hungary",
                      subcategory="Furmint",
                      description="Benchmark dry Furmint from the Királyudvar vineyard — volcanic mineral intensity, high acidity, and textural richness. Green apple, white peach, and volcanic stone. Challenges the world's finest white wines.",
                      price_tier="premium")
if new:
    PAIR(prod_szep, "Pike-perch with saffron cream sauce and asparagus", "complement", "classic", "main", "Furmint's saffron notes and volcanic acidity are natural partners for freshwater fish; the cream sauce is balanced by the wine's structure")
    PAIR(prod_szep, "Langoustines in bisque with tarragon and cream", "complement", "established", "starter", "The wine's mineral intensity and citrus acidity lift the rich bisque; volcanic stone notes harmonize with the shellfish")

# ── ABRUZZO DOC ──────────────────────────────────────────────────
print("\n=== Abruzzo DOC ===")
r_abr = R("Abruzzo", "Italy", "wine",
           designation_type="DOC",
           designation_name="Abruzzo DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Central Italian region on the Adriatic coast with the Apennines as backbone, producing powerful Montepulciano d'Abruzzo reds and Trebbiano d'Abruzzo whites. The region offers extraordinary value with wines of genuine regional character.",
           key_producers="Valentini, Emidio Pepe, Illuminati, Nicodemi, Cataldi Madonna",
           historical_context="Abruzzo has been making wine since Etruscan times. Edoardo Valentini's uncompromising biodynamic viticulture and extended aging created Trebbiano and Montepulciano of world-class quality, inspiring a generation of artisan producers.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Abruzzo vintage; Montepulciano of great concentration and Trebbiano achieving rare mineral depth."),
    (2021, "very_good", "stable", "Elegant vintage; lower yields produced more precise and focused expressions from all varieties."),
    (2020, "excellent", "stable", "Classic Adriatic vintage with ideal ripeness and colour extraction for Montepulciano."),
    (2019, "excellent", "stable", "Benchmark year; Valentini's Trebbiano from this vintage considered among his finest."),
    (2018, "very_good", "stable", "Solid vintage; coastal producers with Atlantic influence made the most precise wines."),
]:
    VIN(r_abr, yr, qd, pt, sn)

p_val = P("Valentini", "Italy", r_abr,
           description="The reclusive genius of Abruzzo — Edoardo Valentini and his son Francesco produced Trebbiano d'Abruzzo and Montepulciano d'Abruzzo that are considered among Italy's greatest wines. Minimal intervention, long aging, and rigorous selection define the estate.")
prod_val, new = PROD("Valentini Montepulciano d'Abruzzo", "wine_still", p_val, r_abr, "Italy",
                     subcategory="Montepulciano",
                     description="The greatest Montepulciano d'Abruzzo ever produced — Valentini's wine defies the appellation's image with 5+ years of barrel aging, extraordinary depth, and 20-year aging potential. Dark cherry, tar, iron, and wild herbs.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_val, "Slow-braised wild boar with rosemary and mountain herbs", "complement", "classic", "main", "Montepulciano's iron and dark fruit intensity is the natural partner for wild game; the wine's structure handles the richness")
    PAIR(prod_val, "Lamb arrosticini (skewers) with chilli oil and flat bread", "complement", "classic", "main", "The regional pairing of Abruzzo — lamb skewers and Montepulciano are ancient companions; the wine's cherry and herb notes complete the picture")

p_cat = P("Cataldi Madonna", "Italy", r_abr,
           description="Family estate in Ofena, one of Abruzzo's most distinctive terroirs. Luigi Cataldi Madonna produces Montepulciano and Pecorino of exceptional character, championing indigenous varieties and authentic regional identity.")
prod_cat, new = PROD("Cataldi Madonna Pecorino", "wine_still", p_cat, r_abr, "Italy",
                     subcategory="Pecorino",
                     description="Abruzzo's prized indigenous white grape — Pecorino (no relation to the cheese) produces wines of remarkable mineral intensity, herbal bitterness, and long finish. Cataldi Madonna's expression is the regional benchmark.",
                     price_tier="mid_range")
if new:
    PAIR(prod_cat, "Spaghetti alle vongole with white wine, garlic, and parsley", "complement", "classic", "main", "Pecorino's mineral saline intensity is the perfect foil for the clams; herbal bitterness echoes the parsley")
    PAIR(prod_cat, "Grilled orata (sea bream) with capers and lemon", "complement", "established", "main", "The wine's citrus and herbal character mirrors the Mediterranean preparation; acidity lifts the delicate white fish")

# ── UMBRIA DOC ───────────────────────────────────────────────────
print("\n=== Umbria DOC ===")
r_umb = R("Umbria", "Italy", "wine",
           designation_type="DOC",
           designation_name="Umbria DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Italy's green heart — landlocked central region producing Sagrantino di Montefalco DOCG (the most tannic grape variety in the world), Orvieto DOC whites, and Torgiano DOC reds. Ancient wine culture with unique indigenous varieties.",
           key_producers="Arnaldo Caprai, Paolo Bea, Lungarotti, Adanti, Tabarrini",
           historical_context="Sagrantino was nearly extinct in the 1960s; Marco Caprai's Arnaldo Caprai estate revived it in the 1970s-80s and created an international reputation. The variety's extraordinary tannin level and dark fruit have attracted collectors worldwide.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Umbria vintage; Sagrantino achieved exceptional tannin ripeness while retaining freshness."),
    (2021, "very_good", "stable", "Elegant vintage; Sagrantino showing more approachability than usual with excellent fruit intensity."),
    (2020, "exceptional", "rising", "The finest Montefalco Sagrantino vintage in two decades; wines destined for 20+ year cellaring."),
    (2019, "excellent", "stable", "Benchmark vintage; Orvieto whites also showed rare mineral precision and aging potential."),
    (2018, "very_good", "stable", "Solid vintage across all appellations; Sagrantino's tannins fully ripened in the warm summer."),
]:
    VIN(r_umb, yr, qd, pt, sn)

p_cap = P("Arnaldo Caprai", "Italy", r_umb,
           description="Marco Caprai's landmark estate that revived Sagrantino di Montefalco and made Umbria internationally famous. The 25 Anni Sagrantino is considered Italy's most tannic and age-worthy red wine.")
prod_cap, new = PROD("Arnaldo Caprai 25 Anni Sagrantino", "wine_still", p_cap, r_umb, "Italy",
                     subcategory="Sagrantino",
                     description="The definitive Sagrantino di Montefalco — from old vines with 36 months in French oak, aged a further 24 in bottle. Blackberry, dried fig, chocolate, and volcanic tannins that need a decade to integrate.",
                     price_tier="premium")
if new:
    PAIR(prod_cap, "Slow-roasted Chianina beef with black truffle and rosemary jus", "complement", "classic", "main", "Sagrantino's massive tannins require the richest preparations; beef fat softens the tannins and the truffle mirrors the wine's earthy depth")
    PAIR(prod_cap, "Dark chocolate fondant with espresso and orange zest", "complement", "established", "dessert", "The wine's chocolate and dried fig notes find resonance in the dessert; bitter chocolate softens the tannins")

p_bea = P("Paolo Bea", "Italy", r_umb,
           description="Giampiero Bea's legendary natural wine estate producing Sagrantino and Montefalco Rosso of extraordinary complexity and longevity. Minimal intervention, extended maceration, and zero filtration define the philosophy.")
prod_bea, new = PROD("Paolo Bea Sagrantino di Montefalco", "wine_still", p_bea, r_umb, "Italy",
                     subcategory="Sagrantino",
                     description="Natural Sagrantino with extended maceration and zero filtration — wild, complex, and deeply authentic. Blackberry preserve, dried herbs, leather, and massive but ripe tannins. Among Italy's most individual wines.",
                     price_tier="premium")
if new:
    PAIR(prod_bea, "Wild hare ragu with pappardelle and black pepper", "complement", "classic", "main", "Wild game's iron and gamey character is the traditional Sagrantino partner; the wine's massive structure and dark fruit match the richness")
    PAIR(prod_bea, "Aged Pecorino di Pienza with truffled honey and walnuts", "complement", "established", "cheese", "Sheep's cheese fat softens the wine's volcanic tannins; truffle honey bridges the dried fig complexity")

# ── PENEDES DO ───────────────────────────────────────────────────
print("\n=== Penedes DO ===")
r_pen = R("Penedes", "Spain", "wine",
           designation_type="DO",
           designation_name="Penedes DO",
           reputation_tier="respected",
           quality_trajectory="established",
           description="Catalonia's largest wine region south of Barcelona, producing Cava (the finest Spanish sparkling wine) as well as serious still wines from Xarello, Macabeu, Parellada, and Garnacha. A region of extraordinary diversity from sea level to 800m altitude.",
           key_producers="Torres, Gramona, Recaredo, Can Feixes, Albet i Noya",
           historical_context="Penedes was transformed by Miguel Torres in the 1960s, who introduced temperature-controlled fermentation and French varieties to Catalonia. Cava production began in 1872 when Josep Raventos produced Spain's first bottle-fermented sparkling wine following a visit to Champagne.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Xarello-based Cava of exceptional freshness and aging potential."),
    (2021, "very_good", "stable", "Elegant, focused vintage; high-altitude still wines showed the most complexity and restraint."),
    (2020, "excellent", "stable", "Classic Penedes conditions; Garnacha and Carinena reds from old mountain vines excelled."),
    (2019, "excellent", "stable", "Benchmark Cava vintage — Gramona and Recaredo produced their finest wines in years."),
    (2018, "very_good", "stable", "Solid vintage; the native Catalan varieties Xarello and Parellada showed excellent freshness."),
]:
    VIN(r_pen, yr, qd, pt, sn)

p_gra = P("Gramona", "Spain", r_pen,
           description="One of Cava's most prestigious houses, producing Gran Reserva and Tres Lustros Cava of extraordinary depth and age-worthiness. The Batlle and Imperial Gran Reserva are benchmarks of what Cava can achieve from Xarello.")
prod_gra, new = PROD("Gramona Imperial Gran Reserva Cava", "wine_sparkling", p_gra, r_pen, "Spain",
                     subcategory="Cava Gran Reserva",
                     description="Xarello-dominant Gran Reserva aged minimum 36 months — toasty brioche, green apple, lemon curd, and remarkable aging potential. Spain's most complex sparkling wine at its level.",
                     price_tier="premium")
if new:
    PAIR(prod_gra, "Jamon Iberico with pan con tomate and arbequina olive oil", "complement", "classic", "aperitif", "Cava's acidity and toasty autolysis cut through the fat; a classic Catalan combination of centuries standing")
    PAIR(prod_gra, "Salt cod croquettes with aioli and smoked paprika", "complement", "established", "amuse", "Fine mousse lifts the fried croquette; Xarello's herbaceous character mirrors the cod's briny intensity")

p_tor = P("Torres", "Spain", r_pen,
           description="Spain's most internationally famous family winery, founded by Jaime Torres in 1870. Miguel Torres revolutionized Spanish wine in the 1960s-70s and the estate continues to produce benchmark Penedes and Priorat wines.")
prod_tor, new = PROD("Torres Gran Coronas Cabernet Sauvignon", "wine_still", p_tor, r_pen, "Spain",
                     subcategory="Cabernet Sauvignon",
                     description="The wine that won the Paris Tasting in 1979, beating Chateau La Tour. Gran Coronas is Torres' flagship Cabernet from Penedes highlands — cassis, cedar, tobacco, and Mediterranean warmth.",
                     price_tier="premium")
if new:
    PAIR(prod_tor, "Roasted rack of lamb with romesco and grilled spring onions", "complement", "classic", "main", "Catalan tradition matches Cabernet with lamb; romesco's nut-tomato richness finds resonance in the wine's fruit and cedar")
    PAIR(prod_tor, "Grilled Catalan sausages (butifarra) with white beans", "complement", "established", "main", "The wine's structure matches the rich sausage; Catalan white beans carry the regional authenticity")

# ── FINGER LAKES AVA ─────────────────────────────────────────────
print("\n=== Finger Lakes AVA ===")
r_fla = R("Finger Lakes", "USA", "wine",
           designation_type="AVA",
           designation_name="Finger Lakes AVA",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="New York State's premier wine region on glacially carved lakes in the Appalachian plateau, producing America's finest Riesling and compelling Cabernet Franc. Seneca Lake's thermal mass moderates the extreme climate, allowing viticulture at 42 degrees north latitude.",
           key_producers="Dr. Konstantin Frank, Hermann J. Wiemer, Red Newt Cellars, Ravines Wine Cellars, Lamoreaux Landing",
           historical_context="Dr. Konstantin Frank proved in 1961 that vinifera varieties could survive Finger Lakes winters, planting Riesling and Chardonnay against local wisdom. Hermann J. Wiemer furthered this legacy; the region now produces Riesling rivaling Germany's finest.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Riesling of exceptional mineral precision and Cabernet Franc showing remarkable depth."),
    (2021, "very_good", "stable", "Cool, classic Finger Lakes vintage; Riesling with stunning acidity and citrus-mineral intensity."),
    (2020, "excellent", "stable", "Warm summer followed by ideal autumn; Cabernet Franc achieved its most complete ripeness in years."),
    (2019, "excellent", "stable", "Benchmark Riesling vintage; off-dry and dry expressions of extraordinary mineral precision."),
    (2018, "very_good", "stable", "Solid vintage; old-vine Riesling from Seneca Lake's west-facing slopes excelled."),
]:
    VIN(r_fla, yr, qd, pt, sn)

p_hjw = P("Hermann J. Wiemer Vineyard", "USA", r_fla,
           description="The estate that built on Dr. Frank's legacy and established Finger Lakes Riesling's international reputation. Hermann Wiemer's German heritage and deep understanding of cool-climate viticulture produced Rieslings of European elegance.")
prod_hjw, new = PROD("Hermann J. Wiemer Dry Riesling", "wine_still", p_hjw, r_fla, "USA",
                     subcategory="Riesling",
                     description="Benchmark Finger Lakes dry Riesling — lime, green apple, slate minerality, and the searing acidity that defines the region. More German than American in spirit; rewards 10+ years of cellaring.",
                     price_tier="premium")
if new:
    PAIR(prod_hjw, "Oysters Rockefeller with spinach and Pernod", "complement", "classic", "aperitif", "Riesling's piercing acidity and slate minerality is the quintessential oyster pairing; anise notes mirror the Pernod")
    PAIR(prod_hjw, "Spicy Thai green curry with jasmine rice and kaffir lime", "complement", "classic", "main", "Riesling's acid-sweet balance and residual sugar cool the chilli heat; citrus notes echo the kaffir lime")

p_kfr = P("Dr. Konstantin Frank Winery", "USA", r_fla,
           description="The founding estate of Finger Lakes fine wine, established by Dr. Konstantin Frank in 1962. The pioneering winery that proved vinifera could thrive in New York continues to produce landmark Riesling and Gewurztraminer under the Frank family.")
prod_kfr, new = PROD("Dr. Konstantin Frank Dry Riesling", "wine_still", p_kfr, r_fla, "USA",
                     subcategory="Riesling",
                     description="The founding estate's benchmark Riesling — vibrant, mineral, and age-worthy. Lime zest, white peach, slate, and piercing acidity. The wine that started the Finger Lakes fine wine revolution.",
                     price_tier="mid_range")
if new:
    PAIR(prod_kfr, "Smoked trout with apple horseradish and pumpernickel", "complement", "classic", "starter", "Riesling and smoked fish is a classic German-American pairing; the wine's acidity cuts the smoke and the apple notes find resonance")
    PAIR(prod_kfr, "Pork schnitzel with lingonberry jam and cucumber salad", "complement", "established", "main", "The founder's German heritage finds expression in this classic pairing; Riesling's acidity lifts the fried coating and the fruit mirrors the lingonberry")

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
