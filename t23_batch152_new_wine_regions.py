#!/usr/bin/env python3
"""B152 — Vernaccia di San Gimignano DOCG (IT), Judean Hills (Israel),
   Moravia Wine Region (Czech Republic), Colchagua Valley DO (Chile),
   Aconcagua Valley DO (Chile)"""

import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
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

# ── 1. Vernaccia di San Gimignano DOCG ────────────────────────────────────────
print("=== Vernaccia di San Gimignano DOCG ===")
r1 = R("Vernaccia di San Gimignano DOCG", "Italy", "wine",
        designation_type="DOCG", designation_name="Vernaccia di San Gimignano DOCG",
        reputation_tier="respected",
        quality_trajectory="established",
        description=(
            "Italy's first DOC (1966) and later DOCG, Vernaccia di San Gimignano "
            "is Tuscany's premier white wine. Produced from the indigenous Vernaccia "
            "grape in the hilltop town of San Gimignano, the wine ranges from crisp "
            "and mineral to richly textured Riserva versions. Characterized by almond "
            "bitterness on the finish, lemon zest, white peach, and flint minerality."
        ),
        key_producers="Panizzi, Falchini, Teruzzi, Cesani, Montenidoli",
        historical_context=(
            "Vernaccia grapes have been cultivated near San Gimignano since the 13th century. "
            "Michelangelo reportedly loved the wine. First DOC in Italy (1966), elevated "
            "to DOCG in 1993."
        ))

for yr, qd, pt, sn in [
    (2023, "excellent",  "rising",  "Warm dry summer with ideal harvest conditions"),
    (2022, "very_good",  "stable",  "Balanced year with good acidity retention"),
    (2021, "excellent",  "stable",  "Cool nights preserved aromatics and freshness"),
    (2020, "very_good",  "stable",  "Steady season; classic mineral expression"),
    (2019, "good",       "stable",  "Warm vintage; earlier harvest maintained acidity"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Panizzi Winery", "winery", r1, "Italy",
        production_philosophy="traditional_with_modern_technique",
        philosophy_description="Single-vineyard focus with careful oak integration.",
        reputation_narrative="Leading Vernaccia producer; Santa Margherita Riserva is the benchmark.",
        price_positioning="premium")
prod1a, new1a = PROD("Panizzi Vernaccia di San Gimignano DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="white",
    description="Benchmark Vernaccia; crisp, mineral, with characteristic almond finish.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "grilled sea bass with lemon and capers", "complement", "classic", "main",
         "citrus-minerality mirrors coastal fish")
    PAIR(prod1a, "white truffle risotto", "bridge", "established", "main",
         "almond earthiness bridges truffle notes")
    PAIR(prod1a, "burrata with heritage tomatoes", "complement", "classic", "starter",
         "acidity cuts richness of burrata")
    PAIR(prod1a, "saffron pasta alla senese", "complement", "established", "main",
         "mineral notes echo saffron earthiness")

prod1b, new1b = PROD("Panizzi Santa Margherita Vernaccia Riserva DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="white",
    description="Single-vineyard Riserva with texture, oak influence, and age potential.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "grilled lobster with butter and tarragon", "complement", "established", "main",
         "rich texture matches shellfish")
    PAIR(prod1b, "aged pecorino with honey", "complement", "classic", "cheese",
         "almond notes echo aged sheep's cheese")
    PAIR(prod1b, "roast chicken with herbs", "complement", "classic", "main",
         "texture and richness in balance")
    PAIR(prod1b, "mushroom and truffle crostini", "bridge", "suggested", "amuse",
         "earthy almond bridge to truffle")

p1b = P("Montenidoli Estate", "winery", r1, "Italy",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic pioneer producing complex age-worthy Vernaccia.",
        reputation_narrative="Among the most serious and long-lived Vernaccia producers.",
        price_positioning="premium")
prod1c, new1c = PROD("Montenidoli Tradizionale Vernaccia di San Gimignano DOCG", "wine_still", p1b, r1, "Italy",
    subcategory="white",
    description="Extended skin contact and barrel aging; structured and serious Vernaccia.",
    price_tier="premium")
if new1c:
    PAIR(prod1c, "salt-baked whole fish", "complement", "established", "main",
         "texture and structure handle bold preparations")
    PAIR(prod1c, "rabbit with olives and rosemary", "complement", "suggested", "main",
         "herbal bridge to Tuscan cuisine")
    PAIR(prod1c, "aged sheep's milk cheese", "complement", "classic", "cheese",
         "almond and beeswax mirror aged dairy")
    PAIR(prod1c, "smoked almond amuse", "bridge", "established", "amuse",
         "direct almond flavor echo")

prod1d, new1d = PROD("Montenidoli Fiore Vernaccia di San Gimignano DOCG", "wine_still", p1b, r1, "Italy",
    subcategory="white",
    description="Free-run juice, early harvest; delicate floral and citrus expression.",
    price_tier="mid_range")
if new1d:
    PAIR(prod1d, "seafood crudo with citrus", "complement", "classic", "starter",
         "delicate citrus mirrors raw seafood")
    PAIR(prod1d, "melon and prosciutto", "complement", "classic", "amuse",
         "floral-citrus bridge to cured meat sweetness")
    PAIR(prod1d, "asparagus and goat cheese tart", "complement", "established", "starter",
         "grassy minerality complements asparagus")
    PAIR(prod1d, "lemon sorbet", "cleanse", "classic", "pre_dessert",
         "citrus echo refreshes palate before dessert")

# ── 2. Judean Hills ────────────────────────────────────────────────────────────
print("=== Judean Hills ===")
r2 = R("Judean Hills", "Israel", "wine",
        designation_type="GI", designation_name="Judean Hills",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Israel's most prestigious wine region rising to 1,000m elevation around "
            "Jerusalem. Limestone soils, continental climate with warm days and cool "
            "nights produce wines of genuine complexity. Cabernet Sauvignon, Merlot, "
            "Syrah, Chardonnay, and indigenous Marawi dominate. Kosher traditions "
            "intersect with modern winemaking."
        ),
        key_producers="Domaine du Castel, Clos de Gat, Tzora Vineyards, Agur",
        historical_context=(
            "Wine has been produced in the Judean Hills for over 5,000 years. "
            "Modern fine wine began in the 1990s with Domaine du Castel pioneering "
            "Bordeaux-style wines of international quality."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Ideal diurnal variation; pristine harvest"),
    (2021, "very_good",  "stable",  "Balanced season with good freshness"),
    (2020, "excellent",  "stable",  "Outstanding vintage for reds and whites"),
    (2019, "very_good",  "stable",  "Warm year with cool nights preserving acidity"),
    (2018, "good",       "stable",  "Solid vintage; approachable style"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Domaine du Castel", "winery", r2, "Israel",
        production_philosophy="bordeaux_influenced",
        philosophy_description="French techniques applied to Judean terroir; gravity-flow cellar.",
        reputation_narrative="Israel's benchmark estate; Grand Vin is the country's most celebrated wine.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Domaine du Castel Grand Vin Judean Hills", "wine_still", p2a, r2, "Israel",
    subcategory="red",
    description="Israel's most sought-after red; Bordeaux blend of profound depth and elegance.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "lamb chops with herbs and pomegranate molasses", "complement", "classic", "main",
         "dark fruit and tannin balance rich lamb")
    PAIR(prod2a, "aged beef fillet with truffle", "complement", "established", "main",
         "Bordeaux-style tannin structure with prime beef")
    PAIR(prod2a, "wild mushroom and lentil ragù", "complement", "suggested", "main",
         "earthiness bridges to forest notes in wine")
    PAIR(prod2a, "aged hard cheese selection", "complement", "classic", "cheese",
         "tannin cuts through cheese fat")

prod2b, new2b = PROD("Domaine du Castel Blanc du Castel Chardonnay Judean Hills", "wine_still", p2a, r2, "Israel",
    subcategory="white",
    description="Israel's premier Chardonnay; barrel-fermented with Burgundian restraint.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "grilled sea bream with herbs", "complement", "classic", "main",
         "mineral Chardonnay and Mediterranean fish")
    PAIR(prod2b, "roasted cauliflower with tahini", "complement", "suggested", "main",
         "nutty richness bridges hazelnut notes in wine")
    PAIR(prod2b, "crab and avocado tartare", "complement", "established", "starter",
         "richness and acidity in balance")
    PAIR(prod2b, "parmesan and truffle arancini", "bridge", "established", "amuse",
         "hazelnut bridge to toasted richness")

p2b = P("Tzora Vineyards", "winery", r2, "Israel",
        production_philosophy="terroir_focused",
        philosophy_description="High-altitude single-vineyard wines; elegant and restrained style.",
        reputation_narrative="Known for some of Israel's most refined and age-worthy wines.",
        price_positioning="premium")
prod2c, new2c = PROD("Tzora Shoresh Judean Hills Red", "wine_still", p2b, r2, "Israel",
    subcategory="red",
    description="Elegant Cabernet-Syrah blend from high-elevation limestone vineyards.",
    price_tier="premium")
if new2c:
    PAIR(prod2c, "slow-roasted lamb shoulder with za'atar", "complement", "classic", "main",
         "spiced lamb and earthy red wine")
    PAIR(prod2c, "beet and walnut salad with labneh", "complement", "suggested", "starter",
         "earthy notes echo beet character")
    PAIR(prod2c, "eggplant and chickpea tagine", "complement", "established", "main",
         "herbal spice bridge to wine")
    PAIR(prod2c, "spiced lamb kebab with herb yogurt", "complement", "classic", "main",
         "classic regional pairing")

prod2d, new2d = PROD("Tzora Misty Hills Judean Hills White", "wine_still", p2b, r2, "Israel",
    subcategory="white",
    description="Complex white blend showing freshness and minerality of high-altitude Judean Hills.",
    price_tier="premium")
if new2d:
    PAIR(prod2d, "hummus with olive oil and pine nuts", "complement", "established", "starter",
         "mineral acidity cuts chickpea richness")
    PAIR(prod2d, "grilled fish with preserved lemon", "complement", "classic", "main",
         "citrus echo and mineral bridge")
    PAIR(prod2d, "mezze platter selection", "complement", "established", "starter",
         "versatile acidity handles variety")
    PAIR(prod2d, "watermelon and feta amuse", "complement", "classic", "amuse",
         "mineral and saline echo in wine")

# ── 3. Moravia Wine Region ────────────────────────────────────────────────────
print("=== Moravia Wine Region ===")
r3 = R("Moravia Wine Region", "Czech Republic", "wine",
        designation_type="GI", designation_name="Moravian Wine Region",
        reputation_tier="emerging",
        quality_trajectory="ascending",
        description=(
            "Moravia produces over 95% of Czech wine. Key varieties include Welschriesling, "
            "Müller-Thurgau, Pinot Gris, Sauvignon Blanc, Pinot Noir, and Blaufränkisch. "
            "The Mikulov and Znojmo sub-regions produce particularly notable wines gaining "
            "international recognition."
        ),
        key_producers="Château Bzenec, Vinařství Volařík, Lechovice, Nové Vinařství",
        historical_context=(
            "Viticulture in Moravia dates to the 2nd century AD under Roman influence. "
            "Post-1989 quality revolution brought investment and international varieties "
            "alongside indigenous grapes."
        ))

for yr, qd, pt, sn in [
    (2023, "very_good",  "stable",  "Cool growing season with excellent freshness"),
    (2022, "excellent",  "rising",  "Warm dry year with outstanding concentration"),
    (2021, "very_good",  "stable",  "Balanced season; good aromatic expression"),
    (2020, "good",       "stable",  "Rain at harvest challenged some producers"),
    (2019, "very_good",  "stable",  "Classic Moravian vintage with good acidity"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Nové Vinařství", "winery", r3, "Czech Republic",
        production_philosophy="natural_wine",
        philosophy_description="Natural wine approach with indigenous varieties and minimal intervention.",
        reputation_narrative="Modern Moravian estate leading quality revolution with natural methods.",
        price_positioning="mid_range")
prod3a, new3a = PROD("Nové Vinařství Frankovka Moravia", "wine_still", p3a, r3, "Czech Republic",
    subcategory="red",
    description="Blaufränkisch (Frankovka) with vibrant acidity, red fruit, and peppery finish.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "roast duck with red cabbage and bread dumplings", "complement", "classic", "main",
         "Moravian traditional duck pairing")
    PAIR(prod3a, "venison goulash with dumplings", "complement", "established", "main",
         "spiced game and peppery wine")
    PAIR(prod3a, "smoked pork with sauerkraut", "complement", "classic", "main",
         "acidity cuts through smoked fat")
    PAIR(prod3a, "aged Olomouc cheese", "complement", "classic", "cheese",
         "regional cheese with local wine")

prod3b, new3b = PROD("Nové Vinařství Welschriesling Moravia", "wine_still", p3a, r3, "Czech Republic",
    subcategory="white",
    description="Crisp Welschriesling with green apple, citrus, and refreshing acidity.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "freshwater trout with herbs and butter", "complement", "classic", "main",
         "Danube trout and Moravian white wine")
    PAIR(prod3b, "apple strudel with vanilla cream", "complement", "established", "dessert",
         "apple echo in wine and pastry")
    PAIR(prod3b, "smoked trout pâté on rye", "complement", "classic", "starter",
         "acidity cuts through smoked richness")
    PAIR(prod3b, "cucumber and dill amuse", "complement", "established", "amuse",
         "herbal freshness bridge")

p3b = P("Vinařství Volařík", "winery", r3, "Czech Republic",
        production_philosophy="traditional",
        philosophy_description="Family winery in Mikulov sub-region specializing in Pinot varieties.",
        reputation_narrative="Respected Moravian producer with limestone-driven Pinot Gris.",
        price_positioning="mid_range")
prod3c, new3c = PROD("Volařík Pinot Gris Moravia Reserve", "wine_still", p3b, r3, "Czech Republic",
    subcategory="white",
    description="Rich Pinot Gris with Alsatian-style weight and spice from Mikulov limestone.",
    price_tier="mid_range")
if new3c:
    PAIR(prod3c, "roast pork with spiced apple sauce", "complement", "classic", "main",
         "rich texture and apple echo")
    PAIR(prod3c, "foie gras terrine with brioche", "complement", "established", "starter",
         "off-dry richness balances liver")
    PAIR(prod3c, "camembert with walnuts and honey", "complement", "established", "cheese",
         "spice and honey bridge to cheese")
    PAIR(prod3c, "butternut squash velouté", "complement", "suggested", "starter",
         "rich texture mirrors squash")

prod3d, new3d = PROD("Volařík Sauvignon Blanc Znojmo Moravia", "wine_still", p3b, r3, "Czech Republic",
    subcategory="white",
    description="Crisp Sauvignon from cool Znojmo sub-region; vibrant and aromatic.",
    price_tier="mid_range")
if new3d:
    PAIR(prod3d, "asparagus with hollandaise", "complement", "classic", "starter",
         "grassiness echoes asparagus character")
    PAIR(prod3d, "fresh goat cheese and herb salad", "complement", "classic", "starter",
         "acidity cuts through goat cheese richness")
    PAIR(prod3d, "green pea soup with mint", "complement", "established", "starter",
         "herbal grassy bridge")
    PAIR(prod3d, "pea shoot and herb amuse", "complement", "established", "amuse",
         "fresh green echo")

# ── 4. Colchagua Valley DO ────────────────────────────────────────────────────
print("=== Colchagua Valley DO ===")
r4 = R("Colchagua Valley DO", "Chile", "wine",
        designation_type="DO", designation_name="Colchagua Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "Chile's most celebrated red wine valley in the Rapel region. Warm, dry "
            "climate suited to Carménère, Cabernet Sauvignon, Syrah, and Malbec. "
            "Sub-zones Marchigüe, Peralillo, and Santa Cruz produce wines of "
            "increasing complexity. Home to the famous Route of Wine."
        ),
        key_producers="Casa Lapostolle, Montes, Casa Silva, Clos Apalta",
        historical_context=(
            "Colchagua modernized rapidly in the 1990s with international investment. "
            "Discovery that Chile's 'Merlot' was actually Carménère transformed the "
            "valley's identity. Clos Apalta first made headlines in the mid-1990s."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "stable",  "Ideal conditions; Carménère fully ripe"),
    (2021, "very_good",  "stable",  "Balanced vintage with good freshness"),
    (2020, "excellent",  "stable",  "Classic Chilean vintage; outstanding concentration"),
    (2019, "very_good",  "stable",  "Steady year; approachable and elegant"),
    (2018, "excellent",  "stable",  "Outstanding year widely praised by critics"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Montes Wines Colchagua", "winery", r4, "Chile",
        production_philosophy="gravity_flow_modern",
        philosophy_description="Gravity-flow winery with Buddhist meditation cellar; terroir precision.",
        reputation_narrative="Pioneer of premium Chilean wine; Purple Angel and Alpha M are benchmarks.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Montes Purple Angel Carménère Colchagua", "wine_still", p4a, r4, "Chile",
    subcategory="red",
    description="Chile's most iconic Carménère; concentrated, structured, extraordinary depth.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "braised beef short rib with chimichurri", "complement", "classic", "main",
         "rich beef and concentrated Carménère")
    PAIR(prod4a, "dark chocolate tart with chili", "complement", "established", "dessert",
         "chocolate echo and chili warmth")
    PAIR(prod4a, "wood-fired lamb with herbs and garlic", "complement", "classic", "main",
         "smoke and herb bridge")
    PAIR(prod4a, "blue cheese and walnut", "complement", "established", "cheese",
         "tannin cuts through blue cheese intensity")

prod4b, new4b = PROD("Montes Alpha M Colchagua", "wine_still", p4a, r4, "Chile",
    subcategory="red",
    description="Bordeaux-blend flagship; gravity-flow winery, aged in French oak 18 months.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "prime beef tenderloin with bone marrow butter", "complement", "classic", "main",
         "structured tannin and prime beef")
    PAIR(prod4b, "slow-roasted lamb rack with herb crust", "complement", "classic", "main",
         "Bordeaux-style with lamb")
    PAIR(prod4b, "aged manchego and membrillo", "complement", "established", "cheese",
         "richness mirrors aged cheese")
    PAIR(prod4b, "truffle and beef tartare", "complement", "established", "starter",
         "cedar and earthiness bridge")

p4b = P("Casa Lapostolle", "winery", r4, "Chile",
        production_philosophy="biodynamic_french_influenced",
        philosophy_description="French-Chilean estate; biodynamic viticulture at Clos Apalta.",
        reputation_narrative="Clos Apalta is among South America's finest wines.",
        price_positioning="ultra_premium")
prod4c, new4c = PROD("Casa Lapostolle Clos Apalta Colchagua", "wine_still", p4b, r4, "Chile",
    subcategory="red",
    description="Iconic Carménère-dominant blend; consistently one of Chile's greatest wines.",
    price_tier="ultra_premium")
if new4c:
    PAIR(prod4c, "asado de tira (beef short ribs) over open fire", "complement", "classic", "main",
         "Chilean asado tradition with flagship wine")
    PAIR(prod4c, "wild boar ragù with fresh pasta", "complement", "established", "main",
         "game and structured red wine affinity")
    PAIR(prod4c, "dark chocolate fondant", "bridge", "established", "dessert",
         "chocolate echo in wine")
    PAIR(prod4c, "aged gouda with walnuts", "complement", "classic", "cheese",
         "richness and tannin in balance")

prod4d, new4d = PROD("Casa Lapostolle Apalta Rosé Colchagua", "wine_still", p4b, r4, "Chile",
    subcategory="rosé",
    description="Elegant rosé from Apalta vineyard; salmon-pink with strawberry and herb notes.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "ceviche with lime and ají amarillo", "complement", "classic", "starter",
         "acidity and citrus match ceviche")
    PAIR(prod4d, "salmon tartare with avocado", "complement", "established", "starter",
         "delicate fruit complements salmon")
    PAIR(prod4d, "grilled vegetable antipasto", "complement", "established", "starter",
         "fresh fruit and vegetable harmony")
    PAIR(prod4d, "prawn cocktail with Marie Rose", "complement", "classic", "amuse",
         "delicate rosé and shellfish")

# ── 5. Aconcagua Valley DO ────────────────────────────────────────────────────
print("=== Aconcagua Valley DO ===")
r5 = R("Aconcagua Valley DO", "Chile", "wine",
        designation_type="DO", designation_name="Aconcagua Valley",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Chile's northernmost fine wine region, just north of Santiago. Pacific "
            "Ocean influence through a gap in the coastal range creates warm days and "
            "dramatically cool nights. Cabernet Sauvignon and Syrah thrive inland; "
            "the coastal Aconcagua Costa sub-zone produces world-class Pinot Noir "
            "and Chardonnay."
        ),
        key_producers="Viña Errázuriz, Seña, Von Siebenthal, Viñedos Chadwick",
        historical_context=(
            "Errázuriz established the region's modern reputation in the 1870s. "
            "Seña — joint venture with Robert Mondavi — elevated international profile. "
            "Aconcagua Costa discovery in 2000s transformed Chile's Pinot Noir landscape."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Ideal coastal influence; Pinot Noir exceptional"),
    (2021, "very_good",  "stable",  "Balanced season; good freshness and structure"),
    (2020, "excellent",  "stable",  "Outstanding year across varieties"),
    (2019, "very_good",  "stable",  "Warm year with cool nights preserving acidity"),
    (2018, "very_good",  "stable",  "Classic Aconcagua vintage"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Viña Errázuriz", "winery", r5, "Chile",
        production_philosophy="terroir_heritage",
        philosophy_description="Fifth-generation estate; single-vineyard focus and sustainable viticulture.",
        reputation_narrative="Historic Aconcagua estate; Don Maximiano is the country's most storied reserve red.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Errázuriz Don Maximiano Founder's Reserve Aconcagua", "wine_still", p5a, r5, "Chile",
    subcategory="red",
    description="Chile's most historic reserve red; Cabernet-dominant blend of extraordinary complexity.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "prime rib roast with roasted bone marrow", "complement", "classic", "main",
         "structured tannin and rich beef")
    PAIR(prod5a, "lamb rack with herb crust and jus", "complement", "classic", "main",
         "classic Cabernet and lamb pairing")
    PAIR(prod5a, "aged cheddar and quince paste", "complement", "established", "cheese",
         "tannin balances aged cheese")
    PAIR(prod5a, "venison with juniper and dark berry sauce", "complement", "established", "main",
         "cedar and game affinity")

prod5b, new5b = PROD("Errázuriz Aconcagua Costa Pinot Noir", "wine_still", p5a, r5, "Chile",
    subcategory="red",
    description="Cool-climate Pinot from ocean-influenced Aconcagua Costa; elegant and complex.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "pan-roasted salmon with pinot noir reduction", "complement", "classic", "main",
         "classic Pinot and salmon pairing")
    PAIR(prod5b, "wild mushroom risotto with herbs", "complement", "established", "main",
         "earthy affinity between mushroom and Pinot")
    PAIR(prod5b, "duck breast with cherry compote", "complement", "classic", "main",
         "cherry echo and silky texture with duck")
    PAIR(prod5b, "smoked salmon and crème fraîche blini", "complement", "established", "amuse",
         "delicate Pinot and smoked fish")

p5b = P("Seña Estate", "winery", r5, "Chile",
        production_philosophy="bordeaux_icon",
        philosophy_description="Biodynamic viticulture; gravity-flow cellar producing Chile's premier icon wine.",
        reputation_narrative="Chile's most internationally acclaimed wine estate.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5c, new5c = PROD("Seña Aconcagua Valley Icon Red", "wine_still", p5b, r5, "Chile",
    subcategory="red",
    description="Chile's most internationally acclaimed red wine; Bordeaux blend of haunting complexity.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "dry-aged beef sirloin with red wine jus", "complement", "classic", "main",
         "iconic Chilean red with aged beef")
    PAIR(prod5c, "lamb shoulder with preserved lemon and herbs", "complement", "classic", "main",
         "structured Bordeaux blend with lamb")
    PAIR(prod5c, "truffle risotto with aged parmesan", "complement", "established", "main",
         "earthiness bridges mineral and truffle")
    PAIR(prod5c, "blue cheese and dark chocolate", "contrast", "adventurous", "cheese",
         "bold contrast between intensity levels")

prod5d, new5d = PROD("Seña Aconcagua Valley White", "wine_still", p5b, r5, "Chile",
    subcategory="white",
    description="Barrel-fermented white blend; complex and mineral with excellent aging potential.",
    price_tier="premium")
if new5d:
    PAIR(prod5d, "ceviche of scallop with citrus and herb", "complement", "established", "starter",
         "citrus and mineral echo")
    PAIR(prod5d, "grilled white fish with chimichurri", "complement", "classic", "main",
         "herb-driven white and chimichurri")
    PAIR(prod5d, "roasted chicken with herbs and lemon", "complement", "classic", "main",
         "rich texture and herb affinity")
    PAIR(prod5d, "smoked salmon rillette with capers", "complement", "established", "starter",
         "mineral and smoke bridge")

# ── Final counts ──────────────────────────────────────────────────────────────
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
print("B152 complete.")
cur.close()
conn.close()
