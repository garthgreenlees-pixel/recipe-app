#!/usr/bin/env python3
"""Terminal 18 — Batch 2: Hunter Valley + Hemel-en-Aarde Valley + Austrian Kamptal depth
New regions: Hunter Valley (Australia), Hemel-en-Aarde Valley (South Africa)
Austrian depth: second Kamptal producer (Kamptal currently has both products from Bründlmayer)
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

print("=== T18 BATCH 2: HUNTER VALLEY + HEMEL-EN-AARDE + KAMPTAL DEPTH ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# HUNTER VALLEY — Australia's Oldest Wine Region
# Famous for: aged Semillon + Shiraz
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── HUNTER VALLEY — NEW REGION ──")
r_hunter = R(
    "Hunter Valley",
    "Australia",
    "wine",
    designation_type="GI",
    designation_name="Hunter Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Hunter Valley is Australia's oldest wine region and the spiritual home of Hunter Semillon — "
        "a wine style unlike any other in the world. Planted in the 1820s north of Sydney in New South "
        "Wales, Hunter's warm, humid climate is counterintuitive for fine wine — yet the region's "
        "unique terroir produces Semillon of extraordinary longevity. Harvested early at very low alcohol "
        "(10-11%), Hunter Semillon is lean, almost aggressively acidic in youth, then transforms over "
        "10-20 years into a wine of extraordinary honeyed complexity, toasted brioche, and mineral depth "
        "without any oak influence. The region also produces approachable, earthy Shiraz with classic "
        "Australian leather and dark fruit character."
    ),
    key_producers="Tyrrell's, Brokenwood, McWilliam's Mount Pleasant, Thomas Wines, Lake's Folly, De Iuliis",
    historical_context=(
        "Hunter Valley's first vines were planted in 1825 by James Busby, Australia's 'Father of Wine'. "
        "The region's unique aged Semillon style was pioneered by Murray Tyrrell in the 1970s — demonstrating "
        "that Hunter white wines improved dramatically with bottle age despite their seemingly austere youth. "
        "Brokenwood's Graveyard Shiraz (first vintage 1983) became Australia's most sought-after Hunter red, "
        "establishing the region's credibility for premium Shiraz alongside its white wine heritage."
    )
)

print("\n  Adding Hunter Valley vintages...")
VIN(r_hunter, 2014, 96, "exceptional",
    "One of Hunter Valley's greatest vintages — long cool season with excellent acid retention. "
    "Semillon of extraordinary precision and aging potential. The benchmark recent white wine vintage.",
    price_trajectory="rising")
VIN(r_hunter, 2016, 88, "very_good",
    "Warm season with some rain events. Good Semillon with accessible character; "
    "Shiraz particularly successful with ripe, earthy depth.",
    price_trajectory="stable")
VIN(r_hunter, 2018, 84, "good",
    "Challenging season with heat and humidity. Careful selection required for freshness. "
    "Best wines from elevated sites with good drainage.",
    price_trajectory="stable")
VIN(r_hunter, 2019, 90, "excellent",
    "Exceptional conditions early in the season — cool spring and even ripening. "
    "Outstanding Semillon with classic structure and mineral freshness for long aging.",
    price_trajectory="rising")
VIN(r_hunter, 2021, 88, "very_good",
    "Good balanced vintage with moderate temperatures. Fresh, precise Semillon; "
    "Shiraz with excellent dark fruit and characteristic Hunter earthy character.",
    price_trajectory="stable")

print("\n── TYRRELL'S WINES (Hunter Valley) ──")
p_tyrrells = P(
    "Tyrrell's Wines",
    "winery", r_hunter, "Australia",
    production_philosophy="Hunter Valley's most historic family estate: founding producer of aged Hunter Semillon, producing Vat 1 — the world's greatest expression of the variety",
    philosophy_description=(
        "Tyrrell's Wines is Hunter Valley's most important wine family — founded in 1858 by Edward Tyrrell, "
        "the estate has been continuously family-owned for six generations. Their Vat 1 Semillon is "
        "Australia's most historically significant white wine: first produced under the Vat 1 label in 1963, "
        "it was Murray Tyrrell who proved to the world that Hunter Semillon develops extraordinary complexity "
        "with age. Harvested early at 10-11% alcohol with intense natural acid, Vat 1 is released at "
        "3 years old but achieves its peak at 10-20 years — transforming from a lean, austere white "
        "into a wine of honeyed complexity, brioche, and mineral depth without oak contact."
    ),
    reputation_narrative=(
        "Tyrrell's Vat 1 Semillon is Australia's most celebrated aged white wine — James Halliday awarded "
        "it 100 points in the 2000 release and has given it 6 Red Stars for decades. The wine is considered "
        "unique in the world of wine: no other region or variety produces Semillon of this aging character "
        "and without oak influence. Wine Advocate and Decanter cite Vat 1 as one of the world's great "
        "white wine originals — an argument for regional specificity over variety."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_tyrrells = PROD(
    "Tyrrell's Vat 1 Semillon Hunter Valley",
    "wine_still", p_tyrrells, r_hunter, "Australia",
    subcategory="semillon_hunter_valley",
    description=(
        "Tyrrell's Vat 1 is the world's greatest Hunter Semillon — one of Australia's most historically "
        "important white wines. Harvested at 10-11% alcohol with intense natural acid, the wine is released "
        "young but achieves its peak at 10-20 years: transforming from lean, austere, and citrus-bright "
        "into a wine of honeyed complexity, brioche, buttered toast, lemon curd, and mineral depth — "
        "all without a single piece of oak. An extraordinary demonstration of site, variety, and time. "
        "Best drunk: 10-25 years from vintage."
    ),
    price_tier="premium"
)
PAIR(prod_tyrrells,
    "Lightly crumbed flathead with tartare sauce and lemon",
    "complement", "classic", "fish_course",
    "Tyrrell's Vat 1 aged 10+ years achieves its finest expression with delicate Australian "
    "flathead — the wine's honeyed brioche and mineral depth bridges the fish's clean flavour "
    "while the crisp crumb provides the textural contrast to the wine's silk. Aged Vat 1's "
    "acid is the perfect foil for tartare sauce's richness; lemon amplifies the wine's citrus "
    "dimension. A pairing unique to the Hunter Valley style — impossible to replicate elsewhere.")
PAIR(prod_tyrrells,
    "Crustacean bisque with saffron, cream, and chive",
    "complement", "established", "starter",
    "Tyrrell's Vat 1 at 8-12 years of age — with its brioche and honey complexity emerging — "
    "achieves a compelling match with crustacean bisque. The wine's natural richness from age "
    "bridges the bisque's cream; saffron's aromatic depth mirrors the wine's honeyed complexity; "
    "the wine's acidity cuts through the richness cleanly. A pairing that showcases aged "
    "Hunter Semillon's extraordinary versatility as a serious food wine.")

print("\n── BROKENWOOD WINES (Hunter Valley) ──")
p_brokenwood = P(
    "Brokenwood Wines",
    "winery", r_hunter, "Australia",
    production_philosophy="Hunter Valley's most acclaimed red wine producer: Graveyard Vineyard Shiraz — Australia's most awarded and collectable Hunter Shiraz since 1983",
    philosophy_description=(
        "Brokenwood Wines was founded in 1970 as a partnership between lawyers and wine lovers, evolving into "
        "one of Hunter Valley's most important estates. Chief winemaker Iain Riggs joined in 1982 and "
        "produced the first Graveyard Vineyard Shiraz in 1983 — a wine that became Hunter Valley's most "
        "collected red. The Graveyard vineyard (named for its proximity to a local cemetery) is planted "
        "on Hunter's characteristic red volcanic soil: the deep, porous loam over clay that provides "
        "natural drainage and produces Shiraz of exceptional earthy depth and longevity. "
        "Brokenwood also produces exceptional Hunter Semillon and multi-regional Shiraz blends."
    ),
    reputation_narrative=(
        "Brokenwood Graveyard Shiraz is consistently awarded 95-100 points by James Halliday (5 Red Stars), "
        "Wine Advocate, and Decanter — it is cited as Hunter Valley's most important Shiraz and among "
        "Australia's greatest red wines. The 1986 and 1998 vintages are considered national icons. "
        "Iain Riggs was inducted into the Australian Wine Hall of Fame in 2012 for his contribution "
        "to Hunter Valley's reputation as a serious fine wine region."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_brokenwood = PROD(
    "Brokenwood Graveyard Vineyard Shiraz Hunter Valley",
    "wine_still", p_brokenwood, r_hunter, "Australia",
    subcategory="shiraz_hunter_valley",
    description=(
        "Brokenwood Graveyard Vineyard Shiraz is Hunter Valley's most celebrated red wine: single-vineyard "
        "Shiraz from red volcanic soil on the Graveyard site, produced only in exceptional years. "
        "Deep ruby with classic Hunter character: earthy dark fruit, tar, leather, fresh herbs, and "
        "a mineral complexity that distinguishes Hunter Shiraz from Barossa's opulent power. "
        "The wine is medium-bodied compared to Barossa — elegant, aromatic, and age-worthy over "
        "15-25 years. One of Australia's most allocated and collected Shiraz wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_brokenwood,
    "Roasted lamb with rosemary, garlic jus, and soft polenta",
    "complement", "classic", "main",
    "Brokenwood Graveyard's Hunter Shiraz earthiness and leather character achieves a natural "
    "pairing with roasted lamb — the wine's medium body is precisely calibrated for lamb's "
    "richness without the grip of Barossa Shiraz. Rosemary bridges the Hunter's herbaceous "
    "dimension; garlic jus amplifies the wine's earthy depth; soft polenta provides the "
    "gentle starchy base the wine's elegant tannin integrates into seamlessly.")
PAIR(prod_brokenwood,
    "Roasted mushroom and truffle risotto with aged Parmesan",
    "complement", "established", "main",
    "Graveyard Vineyard Shiraz's earthy, tar-and-leather Hunter character finds an unexpected "
    "but profound match with truffle risotto — the wine's earthy depth amplifies the truffle's "
    "intensity while the Shiraz's dark fruit provides the fruity counterpoint. Aged Parmesan's "
    "umami complexity bridges wine and food; the risotto's starchy richness integrates the "
    "wine's tannin. A pairing that reveals Hunter Shiraz's affinity with earthy, umami-rich foods.")

# ═══════════════════════════════════════════════════════════════════════════════
# HEMEL-EN-AARDE VALLEY — South Africa's Cool-Climate Pinot Noir
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── HEMEL-EN-AARDE VALLEY — NEW REGION ──")
r_hemel = R(
    "Hemel-en-Aarde Valley",
    "South Africa",
    "wine",
    designation_type="ward",
    designation_name="Hemel-en-Aarde Valley Ward",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "Hemel-en-Aarde Valley ('Heaven and Earth Valley') is South Africa's most celebrated cool-climate "
        "wine region — a series of three wards south of Hermanus on the Walker Bay coast, cooled by the "
        "Southern Ocean. The valley's ancient shale and clay soils at 100-300m altitude, combined with "
        "cool maritime breezes from Walker Bay, create conditions ideal for Pinot Noir and Chardonnay "
        "of European elegance. Hamilton Russell established the region's potential in 1976; today the "
        "three Hemel-en-Aarde wards (Valley, Ridge, Upper) produce South Africa's most internationally "
        "celebrated cool-climate wines — rivalling Burgundy in their elegance and mineral precision."
    ),
    key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Storm Wines, Ataraxia",
    historical_context=(
        "Tim Hamilton Russell planted the first vines in Hemel-en-Aarde Valley in 1976, ignoring "
        "conventional wisdom that Pinot Noir could not succeed in South Africa. His 1981 debut vintage "
        "of Pinot Noir attracted international attention — producing wine of genuine Burgundian elegance "
        "that challenged the assumption that South Africa was only suited to Cabernet and Chenin Blanc. "
        "Today, the three Hemel-en-Aarde wards are South Africa's most critically acclaimed wine area "
        "for fine table wine, producing wines that attract international collectors and sommeliers."
    )
)

print("\n  Adding Hemel-en-Aarde Valley vintages...")
VIN(r_hemel, 2015, 88, "very_good",
    "Good season with moderate temperatures and well-timed rainfall. "
    "Elegant Pinot Noir with fresh red berry character and cool-climate freshness.",
    price_trajectory="stable")
VIN(r_hemel, 2017, 94, "exceptional",
    "Outstanding vintage — cool, dry season with exceptional acid retention. "
    "Pinot Noir of extraordinary elegance and longevity; finest recent vintage.",
    price_trajectory="rising")
VIN(r_hemel, 2018, 86, "very_good",
    "Warm, dry vintage. Good Pinot with ripe character; Chardonnay "
    "particularly successful with generous stone fruit and mineral balance.",
    price_trajectory="stable")
VIN(r_hemel, 2020, 92, "excellent",
    "Cool La Niña season — excellent natural acidity and precision. "
    "Exceptional Pinot Noir and Chardonnay with Burgundy-like minerality and freshness.",
    price_trajectory="rising")
VIN(r_hemel, 2022, 89, "excellent",
    "Balanced vintage with well-timed rains. Fresh, precise Pinot Noir "
    "with classic red berry and earthy Hemel character; good aging potential.",
    price_trajectory="stable")

print("\n── HAMILTON RUSSELL VINEYARDS (Hemel-en-Aarde) ──")
p_hr = P(
    "Hamilton Russell Vineyards",
    "winery", r_hemel, "South Africa",
    production_philosophy="South Africa's founding cool-climate estate: Hemel-en-Aarde's Burgundian benchmark for Pinot Noir and Chardonnay since 1976",
    philosophy_description=(
        "Hamilton Russell Vineyards is South Africa's most important cool-climate estate — founded in 1976 "
        "by Tim Hamilton Russell on the conviction that the Hemel-en-Aarde Valley's oceanic climate could "
        "produce Pinot Noir and Chardonnay rivalling Burgundy. The estate covers 170 hectares of ancient "
        "shale and clay soils at 100-300m altitude, farmed without irrigation and with a philosophy of "
        "minimal intervention. Their Pinot Noir and Chardonnay are South Africa's most internationally "
        "acclaimed wines — Burgundian in their elegance while expressing the Valley's unique mineral terroir. "
        "The estate pioneered cool-climate winemaking in the Cape and established the Hemel-en-Aarde Valley's "
        "international reputation."
    ),
    reputation_narrative=(
        "Hamilton Russell Vineyards is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Decanter "
        "as South Africa's most Burgundy-like producer — the estate has been awarded Wine Spectator Top 100 "
        "Wine and consistently scores 93-97 from all major critics. Their wines demonstrate that South "
        "Africa can produce Pinot Noir and Chardonnay of international stature from a world-class terroir "
        "that stands alongside Burgundy's finest villages for elegance and mineral precision."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_hr = PROD(
    "Hamilton Russell Vineyards Pinot Noir Hemel-en-Aarde Valley",
    "wine_still", p_hr, r_hemel, "South Africa",
    subcategory="pinot_noir_hemel",
    description=(
        "Hamilton Russell's Pinot Noir is South Africa's most celebrated cool-climate red wine: ancient shale "
        "and clay soils in Hemel-en-Aarde Valley produce Pinot Noir of extraordinary elegance and mineral "
        "precision. Pale ruby with red cherry, violet, earthy clay mineral, fresh herbs, and a silky texture "
        "that rivals Burgundy's finest villages. The wine is medium-bodied and aromatic — unmistakably "
        "cool-climate in its freshness and mineral spine. Develops beautifully over 8-15 years."
    ),
    price_tier="premium"
)
PAIR(prod_hr,
    "Duck breast with pickled cherry and celeriac purée",
    "complement", "classic", "main",
    "Hamilton Russell Pinot Noir's cool-climate red cherry and clay mineral character achieves "
    "a compelling pairing with duck breast — the wine's silky texture bridges the duck's richness "
    "while the pickled cherry amplifies the Pinot's red fruit character. Celeriac purée provides "
    "earthy sweetness that mirrors the wine's Hemel-en-Aarde clay mineral. A pairing that "
    "positions South African cool-climate Pinot at the international fine dining table.")
PAIR(prod_hr,
    "Roasted salmon with lentils du Puy and herb oil",
    "complement", "established", "fish_course",
    "Hamilton Russell Pinot Noir's elegant, medium-bodied character and red fruit freshness "
    "creates a compelling match with roasted salmon — one of Pinot Noir's most reliable "
    "fish pairings. The wine's cherry freshness bridges the salmon's richness; lentils' "
    "earthy protein base provides mineral depth that echoes the wine's shale terroir; "
    "herb oil amplifies the wine's aromatic freshness. A Hemel-en-Aarde signature pairing.")

print("\n── BOUCHARD FINLAYSON (Hemel-en-Aarde) ──")
p_bouchard_sa = P(
    "Bouchard Finlayson",
    "winery", r_hemel, "South Africa",
    production_philosophy="Hemel-en-Aarde's most Burgundy-oriented estate: Peter Finlayson's partnership with Paul Bouchard (Burgundy) producing South Africa's most European-inspired Pinot Noir and Chardonnay",
    philosophy_description=(
        "Bouchard Finlayson was established in 1989 by Peter Finlayson (winemaker) and Paul Bouchard "
        "(Burgundy négociant family) — a cross-continental collaboration that brought Burgundian winemaking "
        "philosophy directly to Hemel-en-Aarde Valley. The estate covers 18 hectares of the Valley's "
        "oldest shale and clay soils, farmed sustainably with a focus on vineyard expression over "
        "winemaking intervention. Their Galpin Peak Pinot Noir — named for the mountain above the vineyard "
        "— is made with Burgundian restraint: whole-cluster fermentation, indigenous yeasts, and minimal "
        "new oak to preserve the distinctive Hemel clay mineral and cool-climate freshness."
    ),
    reputation_narrative=(
        "Bouchard Finlayson's Galpin Peak Pinot Noir is cited by Jancis Robinson and Decanter as "
        "one of South Africa's most important fine wine expressions — the Burgundy connection lending "
        "the estate unique winemaking credentials. Consistently scoring 90-95, Galpin Peak demonstrates "
        "that South African Pinot can achieve European complexity from the right combination of "
        "cool-climate site, Burgundian philosophy, and minimal intervention winemaking."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_bouchard_sa = PROD(
    "Bouchard Finlayson Galpin Peak Pinot Noir Hemel-en-Aarde",
    "wine_still", p_bouchard_sa, r_hemel, "South Africa",
    subcategory="pinot_noir_hemel",
    description=(
        "Bouchard Finlayson's Galpin Peak is South Africa's most Burgundy-inspired Pinot Noir: whole-cluster "
        "fermented Pinot from Hemel-en-Aarde's ancient shale soils, made with indigenous yeasts and minimal "
        "new oak. Pale ruby with red cherry, red plum, earthy shale mineral, violet, and a subtle whole-cluster "
        "spice. The wine has a European structure — firm, aromatic, and mineral — that develops genuine "
        "Burgundy-like complexity over 8-12 years. The Bouchard family's Burgundy connection is evident "
        "in every aspect of the wine's philosophy and style."
    ),
    price_tier="premium"
)
PAIR(prod_bouchard_sa,
    "Roasted quail with grape jus and root vegetable gratin",
    "complement", "established", "main",
    "Bouchard Finlayson Galpin Peak's whole-cluster complexity and shale mineral character "
    "achieves a refined pairing with quail — the game bird's delicate flavour is elevated "
    "rather than overwhelmed by the wine's European Pinot structure. Grape jus mirrors the "
    "Pinot's primary fruit character; root vegetable gratin provides earthy warmth that echoes "
    "the wine's shale mineral. A pairing of complete Hemel-en-Aarde elegance.")
PAIR(prod_bouchard_sa,
    "Grilled springbok loin with beetroot and fig reduction",
    "complement", "adventurous", "main",
    "Bouchard Finlayson Galpin Peak's cool-climate Pinot character finds its most distinctively "
    "South African expression with springbok loin — a lean, delicate game meat that mirrors the "
    "wine's medium-bodied elegance. Beetroot's earthy sweetness bridges the wine's mineral clay "
    "character; fig reduction amplifies the Pinot's stone fruit dimension. A pairing that combines "
    "European Burgundian winemaking philosophy with South Africa's indigenous game tradition.")

# ═══════════════════════════════════════════════════════════════════════════════
# KAMPTAL DEPTH — second producer
# Currently only Bründlmayer; add Schloss Gobelsburg
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── KAMPTAL — SCHLOSS GOBELSBURG (second producer) ──")
# Kamptal region_id = 227
p_gobelsburg = P(
    "Schloss Gobelsburg",
    "winery", 227, "Austria",
    production_philosophy="Kamptal's most historic estate: 12th-century monastic cellars producing benchmark Heiligenstein Riesling and Lamm Grüner Veltliner",
    philosophy_description=(
        "Schloss Gobelsburg is one of Austria's most historic wine estates — originally a Cistercian "
        "monastery winery founded in 1171, leased since 1996 by Michael Moosbrugger, who has "
        "transformed the estate into one of Kamptal's finest producers. The estate holds exceptional "
        "parcels in Kamptal's greatest single vineyards: the volcanic Heiligenstein (for Riesling "
        "of extraordinary spice and mineral complexity) and the loess-limestone Lamm (for Grüner "
        "Veltliner of extraordinary weight and structure). Moosbrugger also produces experimental "
        "amphorae-aged wines under the Gobelsburger label, demonstrating the estate's range from "
        "tradition to innovation. The 850-year-old cellars beneath the baroque schloss are among "
        "Austria's most impressive wine-making environments."
    ),
    reputation_narrative=(
        "Schloss Gobelsburg is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Decanter "
        "as one of Austria's most important wine estates. Their Heiligenstein Riesling Erste Lage "
        "consistently scores 93-97 and is considered a benchmark Austrian Riesling of the highest "
        "order. Michael Moosbrugger's vision has made Gobelsburg a reference point for understanding "
        "how Austria's Erste Lage classification system translates to genuine quality differentiation."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_gobelsburg = PROD(
    "Schloss Gobelsburg Heiligenstein Riesling Erste Lage Kamptal",
    "wine_still", p_gobelsburg, 227, "Austria",
    subcategory="riesling_kamptal",
    description=(
        "Schloss Gobelsburg's Heiligenstein Riesling is one of Austria's most compelling wines: "
        "from the 350-million year old volcanic Heiligenstein site — a unique outcrop of Riedelite "
        "(a rare volcanic sandstone) within Kamptal's predominantly loess and limestone geology. "
        "The distinctive terroir produces Riesling of extraordinary spice, mineral complexity, and "
        "aging potential: white peach, apricot, volcanic mineral smoke, Asian spice, and white flower. "
        "One of Austria's most distinctive Erste Lage expressions — develops 10-20 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_gobelsburg,
    "Roasted pike-perch with saffron risotto and wild herbs",
    "complement", "established", "fish_course",
    "Schloss Gobelsburg Heiligenstein's volcanic mineral and Asian spice character achieves "
    "a sophisticated pairing with pike-perch — the Danube fish's delicate flesh bridges the "
    "wine's mineral complexity while saffron amplifies the Riesling's aromatic depth. Wild "
    "herbs echo the wine's herbal mineral dimension; the risotto's starch bridges wine and "
    "fish. A pairing that connects the Heiligenstein's geological uniqueness with Austria's "
    "Danube river fish tradition.")
PAIR(prod_gobelsburg,
    "Thai basil prawn stir-fry with jasmine rice and lime leaf",
    "complement", "established", "main",
    "Gobelsburg Heiligenstein's exotic spice character and volcanic mineral depth creates an "
    "unexpected but compelling match with Thai basil prawns — the wine's Asian spice dimension "
    "bridges the Thai basil's aromatic character; lime leaf echoes the Riesling's citrus "
    "precision; the prawn's natural sweetness amplifies the wine's stone fruit. A pairing that "
    "reveals the Heiligenstein's unique ability to bridge Austrian and Southeast Asian cuisine.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T18 Batch 2 complete.")
print("  Hunter Valley: new region, 5 vintages, 2 producers (Tyrrell's, Brokenwood), 2 products, 4 pairings")
print("  Hemel-en-Aarde: new region, 5 vintages, 2 producers (Hamilton Russell, Bouchard Finlayson), 2 products, 4 pairings")
print("  Kamptal depth: 1 new producer (Schloss Gobelsburg), 1 product, 2 pairings")
