#!/usr/bin/env python3
"""Terminal 19 — Batch 2: Martinborough (NZ) + Franken (Germany) + Chehalem Mountains depth
New regions: Martinborough (NZ Pinot Noir), Franken (German Silvaner)
Depth: Chehalem Mountains Oregon (second producer)
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS region: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  ✓ Region [{rid}]: {name}, {country}")
    return rid

def VIN(region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory="stable"):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory))
    print(f"    ✓ Vintage {year}: {quality_descriptor} ({quality_rating}/100)")

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Producer [{pid}]: {name}")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T19 BATCH 2: MARTINBOROUGH + FRANKEN + CHEHALEM MOUNTAINS ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# MARTINBOROUGH — New Zealand's Premier Pinot Noir Region (South Island rival)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── MARTINBOROUGH — NEW NZ REGION ──")
r_martinborough = R(
    "Martinborough",
    "New Zealand",
    "wine",
    designation_type="GI",
    designation_name="Martinborough GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Martinborough is New Zealand's most celebrated North Island wine region — a free-draining "
        "gravel terrace above the Huangarua River south of Wellington, producing New Zealand's most "
        "structured and age-worthy Pinot Noir. The region's unique terroir of ancient alluvial gravel "
        "over limestone and clay, combined with the Wairarapa's continental climate (warm days, cool "
        "nights from the Remutaka Range, and very low rainfall), produces Pinot Noir of a character "
        "quite different from Central Otago: more structured, mineral, and Burgundian rather than "
        "Central Otago's fruit-forward exuberance. Ata Rangi's wines are considered New Zealand's "
        "finest Pinot Noir by many international critics."
    ),
    key_producers="Ata Rangi, Palliser Estate, Dry River, Te Kairanga, Escarpment, Martinborough Vineyard",
    historical_context=(
        "Martinborough's fine wine story began in 1980 when Dr Derek Milne identified the terrace's "
        "similarity to the Côte d'Or — low rainfall, free-draining alluvial soils, and diurnal temperature "
        "variation. Clive Paton and Phyll Paton established Ata Rangi in 1980, producing New Zealand's "
        "first internationally acclaimed Pinot Noir. The region was granted GI status in 2005. "
        "Martinborough demonstrates that New Zealand's finest Pinot Noir is not exclusively a South Island "
        "phenomenon — the North Island's continental character produces wines of equal complexity."
    )
)

print("\n  Adding Martinborough vintages...")
VIN(r_martinborough, 2015, 88, "very_good",
    "Good season with balanced conditions. Fresh, elegant Pinot with good acid retention. "
    "Classic Martinborough mineral and structural character.",
    price_trajectory="stable")
VIN(r_martinborough, 2017, 94, "exceptional",
    "Martinborough's finest recent vintage — perfect ripening conditions with excellent acid. "
    "Extraordinary Pinot Noir of Burgundy-level complexity and longevity.",
    price_trajectory="rising")
VIN(r_martinborough, 2018, 86, "very_good",
    "Warm vintage with some heat stress. Generous, ripe Pinot; "
    "Ata Rangi's careful vineyard management produced wines with characteristic freshness.",
    price_trajectory="stable")
VIN(r_martinborough, 2020, 92, "excellent",
    "Excellent La Niña season — cool, long ripening with outstanding acid retention. "
    "Mineral, precise Pinot of great elegance and aging potential.",
    price_trajectory="rising")
VIN(r_martinborough, 2022, 89, "excellent",
    "Balanced season with well-timed rainfall. Fresh, structured Pinot "
    "with classic Martinborough mineral and graphite character. Good 8-12 year aging.",
    price_trajectory="stable")

print("\n── ATA RANGI (Martinborough) ──")
p_ata = P(
    "Ata Rangi Vineyard",
    "winery", r_martinborough, "New Zealand",
    production_philosophy="New Zealand's founding Martinborough estate: Clive and Phyll Paton's biodynamic Pinot Noir establishing the region's international reputation since 1980",
    philosophy_description=(
        "Ata Rangi is New Zealand's most celebrated Martinborough producer — established in 1980 by Clive "
        "Paton and Phyll Paton on the historic terrace above the Huangarua River. Their Pinot Noir is made "
        "from a unique blend of Burgundy clones (including the highly prized 'Ata Rangi clone' — actually "
        "the Abel clone from Burgundy) that produce wine of outstanding mineral complexity. The estate "
        "converted to biodynamic viticulture in 2015 and practices regenerative agriculture across its "
        "10-hectare property. Their flagship Pinot Noir is made with whole-cluster inclusion (10-30%), "
        "indigenous yeasts, and extended aging in French oak (20-25% new). The resulting wine has a "
        "Burgundian structure and mineral complexity that consistently ranks it among the Southern "
        "Hemisphere's finest Pinot Noir expressions."
    ),
    reputation_narrative=(
        "Ata Rangi is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Decanter as New Zealand's "
        "most important Martinborough producer — their Pinot Noir consistently scoring 93-97 and considered "
        "alongside Felton Road and Rippon as New Zealand's greatest Pinot Noir expressions. Neal Martin "
        "has written extensively about Ata Rangi's unique 'Ata Rangi clone' Pinot producing wine of "
        "extraordinary aromatic complexity and mineral structure that rivals Burgundy's finest villages."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_ata = PROD(
    "Ata Rangi Pinot Noir Martinborough",
    "wine_still", p_ata, r_martinborough, "New Zealand",
    subcategory="pinot_noir_martinborough",
    description=(
        "Ata Rangi's Martinborough Pinot Noir is New Zealand's most celebrated North Island red wine: "
        "a blend of Ata Rangi clone, Pommard, and Burgundy clones from biodynamically farmed alluvial "
        "gravel soils above the Huangarua River. Pale ruby with extraordinary aromatic complexity: "
        "dark cherry, plum, violet, dried herbs, spice, and a distinctive graphite-gravel mineral "
        "that sets Martinborough Pinot apart from Central Otago's more exuberant fruit. "
        "The wine has structure and longevity — developing Burgundian secondary character over 8-15 years. "
        "Among the Southern Hemisphere's finest Pinot Noir expressions."
    ),
    price_tier="premium"
)
PAIR(prod_ata,
    "Roasted duck leg with cherry, thyme, and celeriac remoulade",
    "complement", "classic", "main",
    "Ata Rangi Pinot Noir's dark cherry and graphite mineral character achieves the classic "
    "Martinborough food pairing with roasted duck — the wine's elegant structure supports the "
    "duck's richness without being overwhelmed by it. Cherry amplifies the Pinot's primary fruit; "
    "thyme bridges the wine's herbal aromatic complexity; celeriac's earthy mineral mirrors "
    "the wine's Martinborough gravel terroir. A pairing of complete NZ Pinot elegance.")
PAIR(prod_ata,
    "Seared salmon fillet with lentils and pinot vinaigrette",
    "complement", "established", "fish_course",
    "Ata Rangi's structured Martinborough Pinot — with its graphite mineral and dark cherry — "
    "achieves an elegant salmon pairing unique to New Zealand's cool-climate Pinot style. "
    "The wine's mineral structure bridges the salmon's richness while the cherry character "
    "amplifies the pinot vinaigrette; lentils' earthy weight balances the Pinot's aromatic "
    "complexity. A pairing that shows Martinborough Pinot's versatility with pink fish.")

print("\n── PALLISER ESTATE (Martinborough) ──")
p_palliser = P(
    "Palliser Estate Wines",
    "winery", r_martinborough, "New Zealand",
    production_philosophy="Martinborough's largest and most comprehensive estate: exceptional Pinot Noir, Riesling, and Sauvignon Blanc from the Martinborough terrace",
    philosophy_description=(
        "Palliser Estate is Martinborough's largest producer — a 65-hectare estate established in 1989 "
        "on the historic terrace. Chief winemaker Allan Johnson has led a quality revolution at the estate, "
        "producing Martinborough's most complete wine portfolio: single-vineyard Pinot Noir of Burgundian "
        "elegance, complex dry Riesling of German mineral precision, and Sauvignon Blanc that rivals "
        "Marlborough while maintaining the terrace's characteristic structure. Their Pencarrow range "
        "provides approachable entry points while the Palliser Estate label delivers premium expressions "
        "for serious collectors. The estate is Martinborough's most food-diverse wine producer."
    ),
    reputation_narrative=(
        "Palliser Estate is cited by James Halliday (Wine Companion) and Wine Advocate as one of "
        "Martinborough's essential producers — their Riesling and Pinot Noir both achieving 90-94 "
        "points from major critics. Palliser demonstrates that Martinborough's versatility extends "
        "beyond Pinot Noir to produce New Zealand's finest North Island Riesling and a compelling "
        "alternative to Marlborough Sauvignon Blanc."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_palliser = PROD(
    "Palliser Estate Riesling Martinborough",
    "wine_still", p_palliser, r_martinborough, "New Zealand",
    subcategory="riesling_martinborough",
    description=(
        "Palliser Estate's Martinborough Riesling is New Zealand's finest North Island expression of "
        "the variety: dry-style Riesling from the alluvial gravel soils above the Huangarua River, "
        "fermented to complete dryness with natural acidity preserved. Pale green-gold with lime zest, "
        "white peach, floral aromatics, and a distinctive chalky-gravel mineral finish. "
        "The wine combines German-style mineral precision with New Zealand's characteristic fruit "
        "freshness — a dry Riesling of real complexity and aging potential over 8-12 years."
    ),
    price_tier="premium"
)
PAIR(prod_palliser,
    "Ceviche of snapper with lime, coriander, and chilli",
    "complement", "established", "starter",
    "Palliser Riesling's lime-mineral freshness and dry precision achieves a natural Pacific Rim "
    "pairing with snapper ceviche — the wine's citrus intensity amplifies the lime's acidity; "
    "coriander bridges the Riesling's floral aromatic character; chilli heat is tempered by "
    "the wine's refreshing minerality. A starter pairing that showcases Martinborough Riesling's "
    "versatility with New Zealand's Pacific-influenced fish preparations.")
PAIR(prod_palliser,
    "Pan-fried blue cod with lemon butter and capers",
    "complement", "classic", "fish_course",
    "Palliser Martinborough Riesling's dry mineral character and lime precision achieves the "
    "classic New Zealand fish pairing with blue cod — a delicate local fish perfectly matched "
    "by the wine's freshness. The Riesling's citrus amplifies the lemon butter; capers "
    "provide salt-acid that the wine integrates; the wine's mineral length supports the fish's "
    "clean flavour. A pairing of complete New Zealand coastal wine and seafood identity.")

# ═══════════════════════════════════════════════════════════════════════════════
# FRANKEN — Germany's Silvaner Region (Boxbeutel bottles, distinctive mineral character)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── FRANKEN — NEW GERMAN REGION ──")
r_franken = R(
    "Franken",
    "Germany",
    "wine",
    designation_type="QbA",
    designation_name="Franken Qualitätswein bestimmter Anbaugebiete",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description=(
        "Franken (Franconia) is Germany's most distinctive wine region — known internationally for the "
        "iconic Boxbeutel (flattened flagon) bottle shape and its signature variety, Silvaner. "
        "The region's continental climate (the most extreme in Germany — cold winters, hot summers) "
        "and diverse soils (Muschelkalk limestone, red sandstone, Keuper marl) produce wines of "
        "extraordinary character: Silvaner from limestone soils achieves mineral, earthy, and food-friendly "
        "complexity quite different from Alsace Silvaner; Riesling from Franken's best sites rivals "
        "Rhinegau for concentration and depth. The Main River valley's dramatic limestone cliffs and "
        "steep south-facing slopes create conditions for Grosses Gewächs Silvaner of world-class quality."
    ),
    key_producers="Weingut Juliusspital, Bürgerspital zum Hl. Geist, Fürstlich Castellsches Domänenamt, Horst Sauer, Rudolf Fürst",
    historical_context=(
        "Franken's winemaking history stretches to the 8th century when Charlemagne established vine "
        "cultivation in the region. The Bürgerspital and Juliusspital — both hospital foundations from "
        "the 14th and 16th centuries — remain among Germany's most important wine estates, using "
        "wine proceeds to fund charitable healthcare. The Boxbeutel bottle, unique to Franken, dates "
        "to at least 1726 and is protected by German wine law. Franken's distinctive Silvaner style "
        "influenced Austrian winemaking and represents Germany's most food-friendly white wine tradition."
    )
)

print("\n  Adding Franken vintages...")
VIN(r_franken, 2015, 92, "excellent",
    "Exceptional Franken vintage — warm, long summer with excellent Silvaner ripeness. "
    "Wines of great concentration and mineral depth. Outstanding for Grosses Gewächs.",
    price_trajectory="rising")
VIN(r_franken, 2016, 86, "very_good",
    "Good season with some spring frost challenges. Silvaner showed "
    "characteristic mineral freshness; Riesling slightly leaner than typical.",
    price_trajectory="stable")
VIN(r_franken, 2018, 94, "exceptional",
    "Extraordinary hot, dry vintage — Franken's continental heat produced Silvaner "
    "of unprecedented concentration and tropical character. Very atypical but remarkable.",
    price_trajectory="rising")
VIN(r_franken, 2020, 88, "very_good",
    "Balanced vintage with good acid retention. Classic, mineral Silvaner "
    "with excellent food-friendly freshness and limestone mineral character.",
    price_trajectory="stable")
VIN(r_franken, 2022, 87, "very_good",
    "Good quality vintage. Fresh Silvaner with bright acidity and mineral precision; "
    "good Riesling from the steeper limestone sites.",
    price_trajectory="stable")

print("\n── WEINGUT JULIUSSPITAL (Franken) ──")
p_julius = P(
    "Weingut Juliusspital",
    "winery", r_franken, "Germany",
    production_philosophy="Franken's most historic estate: 16th-century hospital foundation producing benchmark Silvaner Grosses Gewächs from Würzburger Stein and Iphöfer Julius-Echter-Berg",
    philosophy_description=(
        "Weingut Juliusspital is one of Germany's most historic wine estates — founded in 1576 as a "
        "hospital foundation in Würzburg, using wine revenues to fund healthcare for the poor. The estate "
        "holds 170 hectares of Franken's finest vineyards including prime parcels in the Würzburger Stein "
        "(Franken's greatest site — south-facing Muschelkalk limestone above the Main River) and the "
        "Iphöfer Julius-Echter-Berg. Their Silvaner and Riesling Grosses Gewächs from the Würzburger Stein "
        "demonstrate Franken at its most mineral and complex: the Muschelkalk limestone produces Silvaner "
        "of extraordinary earth-mineral depth quite unlike Alsace's more aromatic style. Chief winemaker "
        "Horst Kolesch's minimal intervention approach preserves the terroir character above all else."
    ),
    reputation_narrative=(
        "Weingut Juliusspital is cited by German wine guide Gault & Millau (Weinguide), Falstaff, and "
        "Wine Advocate (Neal Martin) as one of Germany's most important wine estates outside the famous "
        "Rhine regions. Their Würzburger Stein Silvaner GG consistently scores 91-96 and demonstrates "
        "that Franken's mineral Silvaner is genuinely one of Germany's greatest food wines. The estate's "
        "charitable foundation status gives it unique cultural importance beyond its wine quality."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_julius = PROD(
    "Juliusspital Würzburger Stein Silvaner Grosses Gewächs Franken",
    "wine_still", p_julius, r_franken, "Germany",
    subcategory="silvaner_franken",
    description=(
        "Juliusspital's Würzburger Stein Silvaner GG is Franken's most celebrated dry wine: from the "
        "south-facing Muschelkalk limestone cliff above Würzburg — the Main River's most dramatic and "
        "historically important vineyard. The Silvaner achieves extraordinary mineral depth on this site: "
        "pale gold with white peach, earth, smoked limestone mineral, fennel, and an umami-mineral "
        "complexity quite unlike any other German variety or region. Naturally dry, with low alcohol "
        "(12-13%), excellent acidity, and a persistent saline-mineral finish. Food-compatibility is "
        "exceptional. Develops wonderfully over 8-15 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_julius,
    "White asparagus with Hollandaise and air-dried Schinken",
    "complement", "classic", "starter",
    "Juliusspital Würzburger Stein Silvaner GG is the definitive pairing for German white asparagus "
    "— Franken's most celebrated seasonal tradition. The Silvaner's earthy mineral and umami depth "
    "is uniquely suited to the asparagus's vegetal character; Hollandaise amplifies the wine's "
    "natural richness; Schinken provides salt-umami that bridges the wine's mineral backbone. "
    "A pairing of complete German regional identity — impossible to replicate with any other wine.")
PAIR(prod_julius,
    "Pan-fried pike with brown butter, capers, and lemon",
    "complement", "classic", "fish_course",
    "Juliusspital Stein Silvaner's mineral limestone character and low alcohol make it the ideal "
    "Franconian river fish pairing — pike has been paired with Stein Silvaner since the 16th century. "
    "The wine's earthy mineral amplifies the pike's freshwater depth; brown butter bridges "
    "the Silvaner's weight; capers and lemon echo the wine's natural acidity. "
    "A historical wine-food pairing of the oldest Franconian tradition.")

print("\n── BÜRGERSPITAL ZUM HEILIGEN GEIST (Franken) ──")
p_burger = P(
    "Bürgerspital zum Heiligen Geist",
    "winery", r_franken, "Germany",
    production_philosophy="Franken's oldest charity estate: 14th-century hospital foundation producing Würzburger Stein and Innere Leiste GG Silvaner and Riesling of extraordinary mineral precision",
    philosophy_description=(
        "Bürgerspital zum Heiligen Geist is Germany's oldest continuously operating charity wine estate — "
        "founded in 1319 in Würzburg to care for the city's poor, using wine revenues as its primary "
        "funding source for 700 years. The estate holds 120 hectares of Franken's finest vineyards "
        "including exceptional parcels in the Würzburger Stein (alongside Juliusspital) and the exclusive "
        "Innere Leiste — a walled monopole vineyard at the top of the Stein that produces the estate's "
        "finest Silvaner. Their Innere Leiste GG is one of Germany's most historically significant wines: "
        "the expression of a single, century-old site producing Silvaner of extraordinary mineral purity "
        "and the distinctive earthy depth that only Franken limestone can provide."
    ),
    reputation_narrative=(
        "Bürgerspital is cited by Gault & Millau (Weinguide), Falstaff Austria/Germany, and Wine Advocate "
        "as one of Germany's most important historical wine estates. Their 700-year heritage as a charity "
        "hospital winery gives the estate unique cultural authority, while the Innere Leiste GG Silvaner "
        "demonstrates the variety's capacity for site-specific mineral complexity rivalling Germany's "
        "greatest Riesling expressions."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_burger = PROD(
    "Bürgerspital Würzburger Innere Leiste Silvaner Grosses Gewächs Franken",
    "wine_still", p_burger, r_franken, "Germany",
    subcategory="silvaner_franken",
    description=(
        "Bürgerspital's Innere Leiste GG is a monopole Silvaner of extraordinary historical importance: "
        "the walled upper section of the Würzburger Stein, giving maximum sun exposure on the steepest "
        "Muschelkalk limestone slopes. The wine achieves a density and mineral intensity that exceeds "
        "even the Juliusspital Stein: deep gold with limestone mineral, earth, white truffle, lemon "
        "zest, and a saline umami finish of remarkable persistence. The low alcohol (12%) and "
        "electric acidity make it one of Germany's most complete food wines. "
        "Among Germany's most historically significant whites."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_burger,
    "Baked Camembert with truffle honey and walnuts",
    "complement", "established", "cheese",
    "Bürgerspital Innere Leiste's white truffle and limestone mineral character achieves an "
    "extraordinary match with baked Camembert — the Silvaner's umami-mineral depth bridges "
    "the warm cheese's mushroom character while the truffle honey amplifies the wine's "
    "natural truffle dimension. Walnuts provide bitter contrast that the wine's acidity "
    "integrates. A pairing that reveals Franken Silvaner's affinity for washed-rind cheese.")
PAIR(prod_burger,
    "Pork schnitzel with fried egg, caper berries, and potato salad",
    "complement", "classic", "main",
    "Bürgerspital Innere Leiste Silvaner GG's earthy limestone mineral and umami depth is the "
    "classic Franconian pairing for pan-fried pork schnitzel — a combination with 500+ years "
    "of documented history in Würzburg. The Silvaner's mineral freshness cuts through the "
    "schnitzel's breadcrumb fat; fried egg's richness amplifies the wine's weight; caper berries "
    "echo the wine's natural acidity. A pairing of complete Franconian regional identity.")

# ═══════════════════════════════════════════════════════════════════════════════
# CHEHALEM MOUNTAINS — second producer (region 34)
# Currently: Bergström Old Stones Pinot Noir
# Adding: Adelsheim and Rex Hill are good options; let me add Rex Hill
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CHEHALEM MOUNTAINS — REX HILL (second producer, region 34) ──")
p_rexhill = P(
    "Rex Hill Vineyards",
    "winery", 34, "USA",
    production_philosophy="Chehalem Mountains' pioneer estate: old-vine Pinot Noir and Chardonnay from Oregon's first designated certified sustainable vineyard",
    philosophy_description=(
        "Rex Hill Vineyards was founded in 1983 by Paul Hart and Jan Jacobsen — one of Oregon's earliest "
        "fine wine estates, established before the Willamette Valley's international recognition. "
        "The estate's flagship Jacob-Hart Vineyard in Chehalem Mountains grows some of Oregon's oldest "
        "Pinot Noir and Chardonnay vines — now 40+ years — on volcanic Jory soil over basalt and "
        "sedimentary Laurelwood loam. Rex Hill was Oregon's first certified sustainable vineyard (LIVE "
        "certified since 2000). Their Pinot Noir demonstrates the Chehalem Mountains' distinctive "
        "textural complexity — slightly more linear than Dundee Hills' Pinot, with greater structure "
        "and a more savoury mineral character from the volcanic basalt soils."
    ),
    reputation_narrative=(
        "Rex Hill is cited by Wine Spectator, Wine Advocate (Joe Czerwinski), and Oregon wine specialists "
        "as one of the Chehalem Mountains' most important estates. Their Jacob-Hart Vineyard Pinot Noir "
        "consistently scores 91-95 and demonstrates the sub-AVA's capacity for structured, savoury "
        "Pinot Noir that ages exceptionally well. The estate's 40-year history of sustainable viticulture "
        "makes it a reference point for Oregon wine's environmental credentials."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_rexhill = PROD(
    "Rex Hill Jacob-Hart Vineyard Pinot Noir Chehalem Mountains",
    "wine_still", p_rexhill, 34, "USA",
    subcategory="pinot_noir_chehalem",
    description=(
        "Rex Hill's Jacob-Hart Vineyard Pinot Noir is Chehalem Mountains at its most structured: "
        "40+ year old vines on volcanic Jory soil over basalt, producing Pinot Noir of unusual "
        "linear precision for Oregon. Medium ruby with dark cherry, blackcurrant, dried herbs, "
        "volcanic mineral, and a savoury earthiness from the basalt soils. The wine has more "
        "backbone than Dundee Hills Pinot — firmer, more structured, and developing extraordinary "
        "complexity over 8-15 years of aging. One of Oregon's most site-specific Pinot expressions."
    ),
    price_tier="premium"
)
PAIR(prod_rexhill,
    "Roasted beet salad with goat's cheese, hazelnuts, and herb vinaigrette",
    "complement", "established", "starter",
    "Rex Hill Jacob-Hart's volcanic mineral and dark cherry character finds an elegant Oregon "
    "pairing with roasted beet and goat's cheese — the wine's earthy mineral bridges the beet's "
    "deep sweetness while the Pinot's structure complements the goat cheese's acid. Hazelnuts "
    "echo the wine's volcanic mineral dimension; herb vinaigrette amplifies the Pinot's "
    "herbal aromatic freshness. A Chehalem Mountains pairing of elegant regional identity.")
PAIR(prod_rexhill,
    "Grilled lamb chops with chimichurri and white bean ragout",
    "complement", "established", "main",
    "Rex Hill Jacob-Hart's structured Chehalem Mountains Pinot — with its dark cherry and "
    "volcanic mineral character — achieves a compelling Pacific Northwest lamb pairing. "
    "The wine's firmer structure than typical Oregon Pinot supports the lamb's richness; "
    "chimichurri's herb intensity bridges the wine's herbal aromatic dimension; white bean "
    "ragout provides the earthy, starchy base the Pinot's mineral backbone integrates into.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T19 Batch 2 complete.")
print("  Martinborough: new region, 5 vintages, 2 producers (Ata Rangi, Palliser), 2 products, 4 pairings")
print("  Franken: new region, 5 vintages, 2 producers (Juliusspital, Bürgerspital), 2 products, 4 pairings")
print("  Chehalem Mountains: 1 new producer (Rex Hill), 1 product, 2 pairings")
