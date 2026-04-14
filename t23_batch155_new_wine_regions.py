#!/usr/bin/env python3
"""B155 — Côte-Rôtie AOC, Condrieu AOC, Saint-Joseph AOC,
   Crozes-Hermitage AOC, Cornas AOC — Northern Rhône Deep Dive"""

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

# ── 1. Côte-Rôtie AOC ─────────────────────────────────────────────────────────
print("=== Côte-Rôtie AOC ===")
r1 = R("Côte-Rôtie AOC", "France", "wine",
        designation_type="AOC", designation_name="Côte-Rôtie",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Côte-Rôtie — 'roasted slope' — is the Northern Rhône's most prestigious "
            "appellation, producing singular Syrah wines from near-vertical granite "
            "terraces above Ampuis. The wines combine power with extraordinary elegance "
            "and complexity: violets, black olive, smoked meat, and an iron-mineral "
            "backbone that no other Syrah wine can replicate. Viognier may be blended "
            "in up to 20% to add perfume and stability."
        ),
        key_producers="Guigal, Jamet, Rostaing, Clusel-Roch, Stéphane Ogier",
        historical_context=(
            "Guigal's single-vineyard wines (La Mouline, La Landonne, La Turque) — "
            "the famous 'La La La' — established Côte-Rôtie as one of the world's "
            "most sought-after wines in the 1980s. Robert Parker awarded the 1985 "
            "La Mouline 100 points, triggering global demand. The tiny appellation "
            "covers barely 300 hectares."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Syrah year; concentration with freshness"),
    (2021, "very_good",  "stable",  "Elegant, fragrant wines of great finesse"),
    (2020, "exceptional","rising",  "Among the greatest Côte-Rôtie vintages ever made"),
    (2019, "excellent",  "stable",  "Classic vintage; violet perfume and iron mineral"),
    (2017, "very_good",  "stable",  "Accessible and aromatic; drinking beautifully now"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Jamet Domaine", "winery", r1, "France",
        production_philosophy="traditional_minimalist",
        philosophy_description="Old-vine Syrah from Côte Brune; no new oak, whole-bunch, traditional aging.",
        reputation_narrative="Among Côte-Rôtie's most beloved producers; wines of ethereal elegance.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Jamet Côte-Rôtie AOC", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Benchmark Côte-Rôtie; iron mineral, violet, smoked meat — the essence of the appellation.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "roast leg of lamb with olive tapenade", "complement", "classic", "main",
         "black olive in wine echoes tapenade; Syrah and lamb is Northern Rhône tradition")
    PAIR(prod1a, "grilled côte de bœuf with bone marrow", "complement", "classic", "main",
         "smoked meat notes and iron mineral with aged beef")
    PAIR(prod1a, "wild boar ragù with pasta", "complement", "established", "main",
         "game and structured Syrah")
    PAIR(prod1a, "aged sheep's milk cheese with black olive", "complement", "established", "cheese",
         "black olive bridge to wine character")

prod1b, new1b = PROD("Jamet Côtes du Rhône Rouge", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Village-level Syrah from Jamet; extraordinary value from Northern Rhône master.",
    price_tier="mid_range")
if new1b:
    PAIR(prod1b, "grilled lamb chops with herbs", "complement", "classic", "main",
         "classic Rhône lamb pairing")
    PAIR(prod1b, "beef daubed with olives", "complement", "established", "main",
         "Provence-style beef and Syrah")
    PAIR(prod1b, "tapenade and anchovies on toast", "complement", "established", "amuse",
         "black olive bridge to wine")
    PAIR(prod1b, "wild mushroom tartine", "complement", "established", "starter",
         "earthy Syrah and mushroom")

p1b = P("Stéphane Ogier", "winery", r1, "France",
        production_philosophy="terroir_precision",
        philosophy_description="Single-parcel Côte-Rôtie with meticulous site selection; younger generation.",
        reputation_narrative="Rising star of Côte-Rôtie; Belle Hélène is a benchmark single-vineyard wine.",
        price_positioning="ultra_premium")
prod1c, new1c = PROD("Ogier Côte-Rôtie La Belle Hélène", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Single-parcel La Landonne sector; concentrated, mineral, extraordinary aging potential.",
    price_tier="ultra_premium")
if new1c:
    PAIR(prod1c, "roast rack of lamb with tapenade crust", "complement", "classic", "main",
         "olive and violet bridge to wine character")
    PAIR(prod1c, "wild boar with rosemary and black olive", "complement", "established", "main",
         "game and old-vine Syrah")
    PAIR(prod1c, "aged Mimolette cheese", "complement", "established", "cheese",
         "iron mineral and aged firm cheese")
    PAIR(prod1c, "smoked duck breast with olive salad", "bridge", "established", "amuse",
         "smoked meat and violet bridge")

prod1d, new1d = PROD("Ogier Côte-Rôtie L'Âme Soeur", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Estate Côte-Rôtie; elegant, floral, with classic violet and iron mineral.",
    price_tier="ultra_premium")
if new1d:
    PAIR(prod1d, "magret de canard with cherry compote", "complement", "classic", "main",
         "duck and Syrah — classic Southern French pairing")
    PAIR(prod1d, "venison with juniper and blackberry", "complement", "established", "main",
         "game and structured Syrah")
    PAIR(prod1d, "blue cheese and walnut tart", "complement", "established", "cheese",
         "tannin and mineral cut through blue cheese")
    PAIR(prod1d, "violet and lamb brochette amuse", "bridge", "suggested", "amuse",
         "violet flower bridge to wine perfume")

# ── 2. Condrieu AOC ───────────────────────────────────────────────────────────
print("=== Condrieu AOC ===")
r2 = R("Condrieu AOC", "France", "wine",
        designation_type="AOC", designation_name="Condrieu",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "The world's most celebrated Viognier appellation, Condrieu produces just "
            "5km south of Côte-Rôtie on the same granite slopes. Pure Viognier of "
            "extraordinary aromatic intensity — apricot, peach blossom, jasmine, and "
            "white pepper — combined with rich texture and surprising freshness. The "
            "tiny appellation (less than 200 hectares) produces limited quantities "
            "of this unique white wine style."
        ),
        key_producers="Guigal, Yves Cuilleron, André Perret, François Villard, Stéphane Ogier",
        historical_context=(
            "By the 1960s, Condrieu was nearly extinct — just 6 hectares remained under "
            "vine. The revival of Viognier worldwide in the 1980s and 1990s drove dramatic "
            "replanting. The grape spread to California, South Africa, and beyond, but "
            "Condrieu remains the definitive expression."
        ))

for yr, qd, pt, sn in [
    (2023, "excellent",  "rising",  "Aromatic richness with good freshness"),
    (2022, "very_good",  "stable",  "Classic Condrieu character; ripe and fragrant"),
    (2021, "excellent",  "stable",  "Exceptional freshness preserved the aromatics"),
    (2020, "very_good",  "stable",  "Rich and textured; drink young"),
    (2019, "excellent",  "stable",  "Perfect conditions for Viognier aromatic expression"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Yves Cuilleron", "winery", r2, "France",
        production_philosophy="traditional_terroir",
        philosophy_description="Multiple Condrieu cuvées from distinct parcels; Viognier specialist.",
        reputation_narrative="One of Condrieu's most celebrated and prolific producers.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Cuilleron Condrieu Les Chaillets Viognier", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Benchmark Condrieu; late harvest Viognier of rich apricot and jasmine intensity.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "pan-seared foie gras with apricot compote", "complement", "classic", "main",
         "apricot echo bridges to wine and foie gras richness")
    PAIR(prod2a, "grilled scallops with vanilla and saffron butter", "complement", "established", "main",
         "rich texture and aromatic white")
    PAIR(prod2a, "lobster with Viognier cream sauce", "complement", "classic", "main",
         "Viognier in sauce echoes wine character")
    PAIR(prod2a, "peach and lavender tart", "complement", "established", "dessert",
         "peach echo to apricot-rich wine")

prod2b, new2b = PROD("Cuilleron Condrieu La Petite Côte Viognier", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Entry Condrieu; fresh and aromatic; more accessible style with genuine character.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "crab and avocado with citrus dressing", "complement", "established", "starter",
         "rich texture and aromatic white balance crab sweetness")
    PAIR(prod2b, "asparagus with hollandaise and smoked salmon", "complement", "established", "starter",
         "aromatic richness complements spring vegetables")
    PAIR(prod2b, "chicken with apricot and tarragon cream", "complement", "classic", "main",
         "apricot echo in sauce and wine")
    PAIR(prod2b, "spiced cauliflower soup", "complement", "suggested", "starter",
         "white pepper in wine bridges spiced cauliflower")

p2b = P("André Perret", "winery", r2, "France",
        production_philosophy="low_yield_precision",
        philosophy_description="Very low yields; old-vine Viognier with extraordinary concentration.",
        reputation_narrative="One of Condrieu's most respected small producers; Chéry is legendary.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("André Perret Condrieu Chéry Viognier", "wine_still", p2b, r2, "France",
    subcategory="white",
    description="Legendary single-vineyard Condrieu; extraordinary aromatic intensity and longevity.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "pan-roasted langoustine with apricot beurre blanc", "complement", "classic", "main",
         "apricot sauce bridges to wine character; crustacean and Viognier")
    PAIR(prod2c, "veal sweetbreads with Condrieu cream", "complement", "established", "main",
         "wine used in sauce creates perfect echo")
    PAIR(prod2c, "mango and jasmine crème brûlée", "complement", "established", "dessert",
         "tropical fruit and jasmine echo")
    PAIR(prod2c, "white peach and almond tart", "complement", "classic", "dessert",
         "stone fruit bridge to wine character")

prod2d, new2d = PROD("André Perret Condrieu Coteau de Chéry Viognier", "wine_still", p2b, r2, "France",
    subcategory="white",
    description="Village Condrieu from Perret; aromatic, textured, excellent quality-to-price.",
    price_tier="premium")
if new2d:
    PAIR(prod2d, "smoked salmon with crème fraîche and capers", "complement", "established", "starter",
         "aromatic richness and smoked fish")
    PAIR(prod2d, "prawn and mango salad with citrus", "complement", "established", "starter",
         "tropical fruit bridge")
    PAIR(prod2d, "chicken with mushroom and cream", "complement", "established", "main",
         "rich texture and aromatic bridge")
    PAIR(prod2d, "peach and ricotta amuse", "complement", "classic", "amuse",
         "stone fruit echo to wine character")

# ── 3. Saint-Joseph AOC ───────────────────────────────────────────────────────
print("=== Saint-Joseph AOC ===")
r3 = R("Saint-Joseph AOC", "France", "wine",
        designation_type="AOC", designation_name="Saint-Joseph",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Saint-Joseph stretches 60km along the Northern Rhône's right bank, "
            "producing both Syrah reds and Marsanne/Roussanne whites. The appellation "
            "is enormously variable — from everyday Rhône to serious granite-terroir "
            "wines rivaling Hermitage at a fraction of the cost. Key producers like "
            "Gonon and Coursodon produce benchmark wines from old-vine Syrah on "
            "the best granite sites."
        ),
        key_producers="Gonon, Coursodon, Cuilleron, Chapoutier, Clos de l'Arbalestrier",
        historical_context=(
            "Saint-Joseph's boundaries were dramatically expanded in 1969, diluting "
            "quality. The finest wines come from the original historic core around "
            "Mauves and Tournon. A counter-movement has emerged to reclaim these "
            "historic granite sites as the appellation's true heartland."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "stable",  "Superb year across the appellation"),
    (2021, "very_good",  "stable",  "Fresh, vibrant wines with good structure"),
    (2020, "excellent",  "rising",  "Outstanding granite-terroir expressions"),
    (2019, "very_good",  "stable",  "Classic Saint-Joseph; accessible and aromatic"),
    (2018, "good",       "stable",  "Warm vintage; earlier drinking style"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine Gonon", "winery", r3, "France",
        production_philosophy="old_vine_minimalist",
        philosophy_description="Old-vine Syrah from historic Mauves terroir; whole-bunch, no new oak.",
        reputation_narrative="Saint-Joseph's most revered small producer; wines sell out immediately.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Gonon Saint-Joseph Rouge", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Benchmark Saint-Joseph from historic granite parcels; earthy, mineral, age-worthy.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "grilled lamb chops with Provençal herbs", "complement", "classic", "main",
         "Northern Rhône lamb and Syrah tradition")
    PAIR(prod3a, "braised rabbit with tapenade and olives", "complement", "established", "main",
         "earthy game and mineral Syrah")
    PAIR(prod3a, "saucisson lyonnais with lentils", "complement", "classic", "main",
         "classic Lyon charcuterie and Rhône red")
    PAIR(prod3a, "aged Reblochon cheese", "complement", "established", "cheese",
         "alpine cheese and Rhône granite red")

prod3b, new3b = PROD("Gonon Saint-Joseph Blanc", "wine_still", p3a, r3, "France",
    subcategory="white",
    description="Old-vine Marsanne from Mauves; waxy, mineral, age-worthy Northern Rhône white.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "grilled turbot with almond butter", "complement", "classic", "main",
         "waxy Marsanne and flatfish with almond")
    PAIR(prod3b, "roast chicken with tarragon cream", "complement", "established", "main",
         "rich texture and herbal bridge")
    PAIR(prod3b, "smoked salmon and crème fraîche tart", "complement", "established", "starter",
         "waxy mineral and smoked fish")
    PAIR(prod3b, "almond and honey financier", "complement", "suggested", "pre_dessert",
         "almond echo to waxy Marsanne")

p3b = P("Domaine Coursodon", "winery", r3, "France",
        production_philosophy="traditional_granite",
        philosophy_description="Old-vine granite Saint-Joseph; L'Olivaie and Sensonne are top cuvées.",
        reputation_narrative="One of Saint-Joseph's finest; serious wines from historic granite parcels.",
        price_positioning="premium")
prod3c, new3c = PROD("Coursodon Saint-Joseph L'Olivaie Rouge", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Top cuvée from old-vine granite; concentrated, mineral, violet-scented Syrah.",
    price_tier="premium")
if new3c:
    PAIR(prod3c, "côte de bœuf with herb butter", "complement", "classic", "main",
         "smoked meat notes and aged beef")
    PAIR(prod3c, "wild boar with herbs and black olive", "complement", "established", "main",
         "black olive bridge and game")
    PAIR(prod3c, "tête de moine cheese rosette", "complement", "established", "cheese",
         "granite mineral and Alpine cheese")
    PAIR(prod3c, "lamb merguez with harissa", "complement", "established", "main",
         "spiced lamb and Syrah with pepper")

prod3d, new3d = PROD("Coursodon Saint-Joseph Sensonne Blanc", "wine_still", p3b, r3, "France",
    subcategory="white",
    description="Old-vine Marsanne and Roussanne; rich, mineral, aromatic Northern Rhône white.",
    price_tier="premium")
if new3d:
    PAIR(prod3d, "roasted scallops with lemon beurre blanc", "complement", "established", "main",
         "rich texture and mineral acidity")
    PAIR(prod3d, "poule au pot with vegetables", "complement", "classic", "main",
         "classic French chicken and Northern Rhône white")
    PAIR(prod3d, "baked camembert with herbs", "complement", "established", "cheese",
         "rich texture and mild washed-rind cheese")
    PAIR(prod3d, "white asparagus with sauce gribiche", "complement", "established", "starter",
         "waxy minerality and white asparagus")

# ── 4. Crozes-Hermitage AOC ───────────────────────────────────────────────────
print("=== Crozes-Hermitage AOC ===")
r4 = R("Crozes-Hermitage AOC", "France", "wine",
        designation_type="AOC", designation_name="Crozes-Hermitage",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "The largest Northern Rhône appellation, Crozes-Hermitage surrounds the "
            "famous Hermitage hill with Syrah reds and Marsanne/Roussanne whites. "
            "The best sites — Les Chassis, Les Varonniers, Larnage — produce wines "
            "nearly rivaling Hermitage itself at a fraction of the price. Jaboulet's "
            "Domaine de Thalabert and Chapoutier's Les Varonniers are benchmarks."
        ),
        key_producers="Jaboulet, Chapoutier, Alain Graillot, Belle, Ferraton",
        historical_context=(
            "Crozes-Hermitage received appellation status in 1937. The quality gap "
            "between simple cooperative Crozes and the finest single-vineyard wines "
            "is enormous. The best Crozes from Graillot or Jaboulet offer Northern "
            "Rhône character at accessible prices."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "stable",  "Top sites rivaling Hermitage in quality"),
    (2021, "very_good",  "stable",  "Fresh, vibrant wines across the appellation"),
    (2020, "excellent",  "stable",  "Outstanding year; best sites shine"),
    (2019, "very_good",  "stable",  "Consistent quality; value vintage"),
    (2018, "good",       "stable",  "Warm year; earlier drinking style"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Alain Graillot Domaine", "winery", r4, "France",
        production_philosophy="natural_traditional",
        philosophy_description="Natural winemaking with low sulfur; benchmark for Crozes-Hermitage quality.",
        reputation_narrative="Crozes-Hermitage's most celebrated producer; Guiraude is the prestige cuvée.",
        price_positioning="premium",
        authority_tier=1)
prod4a, new4a = PROD("Graillot Crozes-Hermitage Rouge", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Benchmark Crozes-Hermitage red; earthy Syrah with violet, olive, and mineral character.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "grilled lamb merguez with couscous", "complement", "classic", "main",
         "Northern Rhône Syrah and lamb spice tradition")
    PAIR(prod4a, "tapenade and anchovy flatbread", "complement", "established", "amuse",
         "black olive bridge to wine character")
    PAIR(prod4a, "slow-braised beef with olives", "complement", "established", "main",
         "earthy beef and Syrah")
    PAIR(prod4a, "Saint-Marcellin cheese", "complement", "classic", "cheese",
         "local Drôme cheese with local wine")

prod4b, new4b = PROD("Graillot Crozes-Hermitage La Guiraude Rouge", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Top selection Crozes; old-vine Syrah with greater depth and concentration.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "roast leg of lamb with tapenade", "complement", "classic", "main",
         "Northern Rhône lamb and olive tradition")
    PAIR(prod4b, "venison with berry and juniper sauce", "complement", "established", "main",
         "game and structured Syrah")
    PAIR(prod4b, "aged Comté with walnuts", "complement", "established", "cheese",
         "structured tannin and aged hard cheese")
    PAIR(prod4b, "braised wild boar with mushrooms", "complement", "established", "main",
         "game and earthy Syrah")

p4b = P("Domaine Belle", "winery", r4, "France",
        production_philosophy="terroir_precision",
        philosophy_description="Single-site wines from best Crozes terroirs; Larnage and Les Pierrelles.",
        reputation_narrative="Among Crozes's most consistent; Louis Belle wines are age-worthy benchmarks.",
        price_positioning="premium")
prod4c, new4c = PROD("Belle Crozes-Hermitage Les Pierrelles Rouge", "wine_still", p4b, r4, "France",
    subcategory="red",
    description="Single-site Crozes from clay-limestone; structured, mineral, food-friendly Syrah.",
    price_tier="mid_range")
if new4c:
    PAIR(prod4c, "duck confit with Puy lentils", "complement", "established", "main",
         "classic bistro Rhône pairing")
    PAIR(prod4c, "pork belly with mustard and herbs", "complement", "established", "main",
         "rich pork and earthy Syrah")
    PAIR(prod4c, "saucisson and cornichons", "complement", "classic", "amuse",
         "Lyon charcuterie tradition")
    PAIR(prod4c, "aged Cantal cheese", "complement", "established", "cheese",
         "structured Syrah and aged French cheese")

prod4d, new4d = PROD("Belle Crozes-Hermitage Blanc", "wine_still", p4b, r4, "France",
    subcategory="white",
    description="Marsanne-based Crozes-Hermitage blanc; waxy, mineral, age-worthy.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "grilled sea bass with lemon and herbs", "complement", "classic", "main",
         "mineral Marsanne and Mediterranean fish")
    PAIR(prod4d, "chicken with cream and mushrooms", "complement", "established", "main",
         "rich texture and waxy Marsanne")
    PAIR(prod4d, "smoked trout with horseradish cream", "complement", "established", "starter",
         "waxy mineral and smoked fish")
    PAIR(prod4d, "quiche Lorraine", "complement", "classic", "main",
         "classic French bistro pairing")

# ── 5. Cornas AOC ─────────────────────────────────────────────────────────────
print("=== Cornas AOC ===")
r5 = R("Cornas AOC", "France", "wine",
        designation_type="AOC", designation_name="Cornas",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description=(
            "The most rustic and powerful of the Northern Rhône appellations, Cornas "
            "produces 100% Syrah from a natural granite amphitheatre that concentrates "
            "heat and reflects sunlight. The wines are dark, brooding, and tannic in "
            "youth — requiring years of aging to reveal their extraordinary complexity "
            "of smoked meat, black pepper, iron, and black fruit. Auguste Clape and "
            "Thierry Allemand produce some of France's greatest wines here."
        ),
        key_producers="Auguste Clape, Thierry Allemand, Franck Balthazar, Vincent Paris",
        historical_context=(
            "Cornas was overlooked for centuries as too tannic and austere for popular "
            "taste. The wines of Auguste Clape — making wine since 1955 — and his "
            "successors revealed the extraordinary aging potential of old-vine Cornas. "
            "Robert Parker championed the region in the 1980s, transforming its fortunes."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Cornas year; structure and freshness"),
    (2021, "very_good",  "stable",  "More approachable style; good for earlier drinking"),
    (2020, "exceptional","rising",  "Greatest Cornas vintage in decades; profound"),
    (2019, "excellent",  "stable",  "Powerful and structured; needs long aging"),
    (2017, "very_good",  "stable",  "Accessible and aromatic; early pleasure"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Domaine Auguste Clape", "winery", r5, "France",
        production_philosophy="traditional_heritage",
        philosophy_description="Traditional Cornas; whole-bunch Syrah aged in old foudres; no new oak.",
        reputation_narrative="France's most revered Northern Rhône producer; Cornas is the benchmark.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Clape Cornas AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="The definitive Cornas; smoked meat, black pepper, iron mineral — requires 10+ years aging.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "roast wild boar with black olive and herbs", "complement", "classic", "main",
         "powerful Syrah and game — Cornas tradition")
    PAIR(prod5a, "aged côte de bœuf from Limousin", "complement", "classic", "main",
         "smoked meat notes and iron mineral with aged beef")
    PAIR(prod5a, "braised lamb shoulder with olives", "complement", "classic", "main",
         "black olive in wine and lamb")
    PAIR(prod5a, "aged Saint-Nectaire and walnut", "complement", "established", "cheese",
         "iron mineral and semi-firm cheese")

prod5b, new5b = PROD("Clape Renaissance Cornas AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Village-level Syrah from Clape; more accessible than Cornas but same house style.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "grilled lamb chops with olive tapenade", "complement", "classic", "main",
         "Northern Rhône lamb and olive tradition")
    PAIR(prod5b, "beef stew with mushrooms and herbs", "complement", "established", "main",
         "earthy Syrah and braised beef")
    PAIR(prod5b, "charcuterie selection from the Ardèche", "complement", "classic", "amuse",
         "regional charcuterie and local Syrah")
    PAIR(prod5b, "aged Pélardon goat cheese", "complement", "established", "cheese",
         "Southern French goat cheese and structured Syrah")

p5b = P("Thierry Allemand Domaine", "winery", r5, "France",
        production_philosophy="natural_minimal",
        philosophy_description="Biodynamic Cornas; natural winemaking; ultra-low production.",
        reputation_narrative="Cornas's other master; Chaillot and Reynard are among France's greatest reds.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Allemand Cornas Chaillot", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Young-vine Cornas from Allemand; more approachable but profound in character.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "roast duck with black cherry and star anise", "complement", "established", "main",
         "dark fruit and structured Syrah")
    PAIR(prod5c, "wild mushroom risotto with truffle", "complement", "established", "main",
         "earthy mineral bridge")
    PAIR(prod5c, "venison tartare with juniper", "complement", "established", "starter",
         "game and iron mineral bridge")
    PAIR(prod5c, "aged Comté 36 months", "complement", "established", "cheese",
         "intense mineral wine and aged nutty cheese")

prod5d, new5d = PROD("Allemand Cornas Reynard", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Old-vine Cornas; extraordinary concentration, mineral depth, legendary aging potential.",
    price_tier="ultra_premium")
if new5d:
    PAIR(prod5d, "slow-roasted leg of lamb with garlic and rosemary", "complement", "classic", "main",
         "definitive Cornas lamb pairing")
    PAIR(prod5d, "wood-roasted wild boar with black pepper", "complement", "classic", "main",
         "powerful game and powerful Syrah")
    PAIR(prod5d, "aged Cantal between 6-24 months", "complement", "established", "cheese",
         "intense mineral wine and aged mountain cheese")
    PAIR(prod5d, "smoked bone marrow with herbs", "bridge", "established", "amuse",
         "smoked meat bridge to wine character")

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
print("B155 complete.")
cur.close()
conn.close()
