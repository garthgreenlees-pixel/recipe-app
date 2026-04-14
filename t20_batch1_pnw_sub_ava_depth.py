#!/usr/bin/env python3
"""Terminal 20 — Batch 1: PNW Sub-AVA Depth
Second products for 5 single-product Washington/Oregon sub-AVAs:
Red Mountain, Rocks District of Milton-Freewater, Ribbon Ridge,
Yamhill-Carlton, Horse Heaven Hills
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

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

print("=== T20 BATCH 1: PNW SUB-AVA DEPTH (5 REGIONS) ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# RED MOUNTAIN (region 22) — second product
# Currently: Quilceda Creek Cabernet Sauvignon
# Adding: Col Solare (Columbia Crest / Marchesi Antinori collaboration)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── RED MOUNTAIN — Col Solare ──")
p_colsolare = P(
    "Col Solare",
    "winery", 22, "USA",
    production_philosophy="The Antinori-Columbia Crest collaboration: Italian mastery and Red Mountain terroir producing Washington's most European-influenced Cabernet",
    philosophy_description=(
        "Col Solare ('Shining Hill' in Italian) is the collaboration between Marchesi Antinori (Tuscany's "
        "most important wine family) and Ste. Michelle Wine Estates (Columbia Crest) — a partnership "
        "established in 1995 that combines Italian winemaking philosophy with Red Mountain's extraordinary "
        "Cabernet Sauvignon terroir. The estate's custom winery on Red Mountain opened in 2006, with "
        "vineyards on the Mountain's south-facing slopes of ancient Missoula Flood silt loam over caliche. "
        "Chief winemaker Marcus Notaro, guided by Antinori's Renzo Cotarella, produces a Cabernet-based "
        "blend that reflects both the Antinori philosophy of elegance and Red Mountain's concentrated "
        "power — the result is Washington's most European-influenced Cabernet expression."
    ),
    reputation_narrative=(
        "Col Solare is cited by Wine Advocate (Paul Gregutt), Wine Spectator, and Decanter as one of "
        "Washington State's most important red wine producers — the Antinori connection bringing "
        "international credibility to Red Mountain's emerging reputation. Scoring 93-97 from top critics, "
        "Col Solare demonstrates that Red Mountain can produce Cabernet-based blends at the international "
        "fine dining level alongside Napa Valley and the finest European Cabernet regions."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_colsolare = PROD(
    "Col Solare Red Mountain Estate",
    "wine_still", p_colsolare, 22, "USA",
    subcategory="cabernet_sauvignon_red_mountain",
    description=(
        "Col Solare Red Mountain Estate is Washington State's most Italian-inspired Cabernet: a blend "
        "of Cabernet Sauvignon (85%+) with Merlot, Cabernet Franc, and Petit Verdot from Red Mountain's "
        "south-facing silt loam vineyards. Deep ruby with extraordinary concentration: blackcurrant, "
        "dark chocolate, graphite, cedar, and the distinctive iron-mineral austerity of Red Mountain "
        "terroir. The wine has the structural elegance of the Antinori philosophy — less opulent than "
        "Red Mountain's more typical powerful style, but with greater age-worthiness and finesse. "
        "Develops magnificently over 15-20 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_colsolare,
    "Grilled dry-aged ribeye with chanterelle ragout and bordelaise",
    "complement", "classic", "main",
    "Col Solare's Antinori-influenced Cabernet elegance and Red Mountain iron-mineral depth "
    "achieves the Pacific Northwest's most ambitious steak pairing. The dry-aged ribeye's "
    "concentrated beef character matches the wine's structural power; chanterelle ragout "
    "bridges the wine's mushroom-mineral complexity; bordelaise sauce creates a European "
    "wine-sauce mirror. A pairing that positions Red Mountain at Washington's highest "
    "fine dining table alongside Napa Cabernet.")
PAIR(prod_colsolare,
    "Braised Wagyu short rib with roasted garlic polenta and gremolata",
    "complement", "established", "main",
    "Col Solare's Italian-influenced Cabernet character and Red Mountain mineral power finds "
    "an unexpected Italian-Pacific Northwest bridge with Wagyu short rib and polenta — the "
    "wine's Antinori elegance is amplified by the polenta's corn sweetness; gremolata's "
    "lemon-garlic freshness bridges the wine's graphite mineral. A pairing of extraordinary "
    "cultural fusion between Washington terroir and Italian winemaking philosophy.")

# ═══════════════════════════════════════════════════════════════════════════════
# ROCKS DISTRICT OF MILTON-FREEWATER (region 44) — second product
# Currently: Cayuse Vineyards Cailloux Vineyard Syrah
# Adding: K Vintners (Charles Smith Wines)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── ROCKS DISTRICT — K Vintners ──")
p_kvintners = P(
    "K Vintners",
    "winery", 44, "USA",
    production_philosophy="Charles Smith's visionary Rocks District Syrah: old-vine cobblestone-terroir Syrah rivalling the Northern Rhône for mineral intensity and aging potential",
    philosophy_description=(
        "K Vintners is Charles Smith's prestige label — focused exclusively on Washington State's "
        "greatest Syrah sites, particularly the Rocks District of Milton-Freewater. Their Rocks District "
        "Syrahs are considered among the Pacific Northwest's most extraordinary wines: produced from "
        "the unique basalt cobblestone terroir of the Rocks District (ancient river cobbles that absorb "
        "heat by day and radiate warmth overnight). Charles Smith's winemaking philosophy is minimal "
        "intervention: whole-cluster fermentation, indigenous yeasts, no fining, and extended aging in "
        "old French Rhône barrique. The result is Syrah of a mineral intensity and savouriness that "
        "rivals Hermitage and Côte-Rôtie while maintaining a distinctly Rocks District character."
    ),
    reputation_narrative=(
        "K Vintners' Rocks District Syrahs are cited by Wine Advocate (Paul Gregutt, who awarded 100 "
        "points to multiple releases), Wine Spectator, and Jancis Robinson as Washington State's most "
        "exciting wine category. Charles Smith is considered one of the Pacific Northwest's most "
        "visionary winemakers — his K Vintners series demonstrating that the Rocks District can produce "
        "Syrah of world-class complexity rivalling France's Northern Rhône in mineral depth and longevity."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_kvintners = PROD(
    "K Vintners Motor City Kitty Rocks District Syrah",
    "wine_still", p_kvintners, 44, "USA",
    subcategory="syrah_rocks_district",
    description=(
        "K Vintners Motor City Kitty is one of the Rocks District's most celebrated Syrahs: from old-vine "
        "Syrah on the ancient basalt cobblestone terroir of Milton-Freewater's Rocks District. "
        "Deep violet with extraordinary savouriness: olive tapenade, smoked meat, violets, graphite, "
        "iron mineral, and a concentrated dark fruit that emerges from beneath the mineral intensity. "
        "The wine has a Northern Rhône-like structure — not Washington's typical opulence, but "
        "a lean, mineral austerity that rewards 15-20 years of aging. Among Washington's most "
        "complex and age-worthy Syrahs."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_kvintners,
    "Grilled flat iron steak with olive tapenade and roasted bone marrow",
    "complement", "established", "main",
    "K Vintners Motor City Kitty's tapenade-mineral intensity and smoked meat character achieves "
    "a profound match with grilled flat iron steak — the wine's olive savouriness mirrors the "
    "tapenade; the steak's char amplifies the wine's smoked meat dimension; bone marrow's fat "
    "richness bridges the wine's iron-mineral austerity. A Pacific Northwest Syrah pairing of "
    "unexpected Northern Rhône-like intensity.")
PAIR(prod_kvintners,
    "Braised lamb neck with merguez spice and harissa yoghurt",
    "complement", "adventurous", "main",
    "K Vintners Rocks District Syrah's smoked meat and mineral savouriness achieves a compelling "
    "cross-cultural match with merguez-spiced lamb — the wine's Northern Rhône-like character "
    "bridges the North African spice tradition; harissa yoghurt's heat is moderated by the "
    "wine's mineral freshness; the lamb's richness integrates the wine's iron mineral. "
    "A pairing that reveals the Rocks District's affinity with bold, spiced preparations.")

# ═══════════════════════════════════════════════════════════════════════════════
# RIBBON RIDGE (region 35) — second product
# Currently: Beaux Frères Pinot Noir
# Adding: Brick House Vineyard & Winery
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── RIBBON RIDGE — Brick House Vineyard ──")
p_brickhouse = P(
    "Brick House Vineyard & Winery",
    "winery", 35, "USA",
    production_philosophy="Oregon's first biodynamic winery: old-vine Ribbon Ridge Pinot Noir with Burgundian restraint from volcanic Jory and Nekia soils",
    philosophy_description=(
        "Brick House Vineyard & Winery is Oregon's most philosophically consistent biodynamic estate — "
        "converted to Biodynamic agriculture in 1990 by Doug Tunnell (former CBS journalist turned "
        "winemaker), making it Oregon's first biodynamic winery. The 26-hectare estate on Ribbon Ridge's "
        "volcanic Jory and Nekia clay-loam soils produces three distinct Pinot Noir cuvées plus Gamay Noir "
        "and Chardonnay. Their approach emphasises Burgundian restraint over Oregon's typical lush fruit: "
        "whole-cluster fermentation, indigenous yeasts, and aging in 30% new French oak preserve the "
        "volcanic soil's mineral character. The wines are among Ribbon Ridge's most consistently precise "
        "and age-worthy expressions."
    ),
    reputation_narrative=(
        "Brick House is cited by Wine Advocate (Joe Czerwinski), Decanter, and Oregon wine specialists "
        "as Ribbon Ridge's most Burgundy-oriented producer — their Cuvée du Tonnelier Pinot Noir scoring "
        "92-96 and demonstrating the sub-AVA's capacity for structured, mineral-driven Pinot with "
        "genuine longevity. Doug Tunnell's 35-year commitment to biodynamics makes Brick House a reference "
        "point for Oregon wine's environmental credentials alongside biodynamic philosophy."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_brickhouse = PROD(
    "Brick House Cuvée du Tonnelier Pinot Noir Ribbon Ridge",
    "wine_still", p_brickhouse, 35, "USA",
    subcategory="pinot_noir_ribbon_ridge",
    description=(
        "Brick House's Cuvée du Tonnelier is Ribbon Ridge's most Burgundy-aligned Pinot Noir: "
        "from biodynamically farmed volcanic Jory and Nekia soils, made with whole-cluster inclusion "
        "and indigenous yeasts. Medium ruby with dark cherry, earth, spice, volcanic mineral, "
        "and a structural complexity that distinguishes Ribbon Ridge from the more approachable "
        "Dundee Hills Pinot. The wine has a Chambolle-like combination of elegance and mineral depth — "
        "rewarding 8-15 years of aging for full secondary character development."
    ),
    price_tier="premium"
)
PAIR(prod_brickhouse,
    "Roasted quail with pomegranate, wild mushrooms, and barley",
    "complement", "established", "main",
    "Brick House Cuvée du Tonnelier's whole-cluster spice and volcanic mineral character achieves "
    "a refined Pacific Northwest pairing with roasted quail — the game bird's delicate richness "
    "is elevated by the wine's spiced complexity; pomegranate's tartness bridges the Pinot's "
    "primary fruit; wild mushrooms amplify the wine's earthy volcanic mineral dimension. "
    "A pairing of complete Ribbon Ridge terroir authenticity.")
PAIR(prod_brickhouse,
    "Pan-seared wild salmon with hazelnut brown butter and lentils",
    "complement", "classic", "fish_course",
    "Brick House Cuvée du Tonnelier's mineral structure and dark cherry depth achieves the "
    "Oregon classic — Pinot Noir with Pacific salmon. The wine's whole-cluster spice bridges "
    "the salmon's richness; hazelnut brown butter amplifies the Pinot's nutty mineral dimension; "
    "lentils provide earthy depth that supports the wine's volcanic mineral backbone. "
    "A Ribbon Ridge pairing of Oregon's most celebrated wine-fish tradition.")

# ═══════════════════════════════════════════════════════════════════════════════
# YAMHILL-CARLTON (region 36) — second product
# Currently: Ken Wright Cellars Savoya Vineyard Pinot Noir
# Adding: Soter Vineyards
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── YAMHILL-CARLTON — Soter Vineyards ──")
p_soter = P(
    "Soter Vineyards",
    "winery", 36, "USA",
    production_philosophy="Yamhill-Carlton's most biodynamic estate: Tony Soter's Planet Oregon sparkling Rosé and estate Pinot Noir from Yamhill-Carlton's finest marine sedimentary soils",
    philosophy_description=(
        "Soter Vineyards was established in 2003 by Tony Soter — one of Napa Valley's most celebrated "
        "winemakers who relocated to Oregon to pursue his vision of biodynamic Pinot Noir and sparkling "
        "wine on Yamhill-Carlton's ancient marine sedimentary soils (Willakenzie series). The estate's "
        "50-hectare North Valley Vineyard in Carlton is Yamhill-Carlton's most biodynamically intensive — "
        "Demeter certified since 2016, with extensive cover cropping and biodynamic preparations. "
        "Their Planet Oregon sparkling Rosé (extra brut) and Mineral Springs Ranch Pinot Noir demonstrate "
        "Soter's Napa-meets-Burgundy philosophy: the precision of Napa winemaking combined with the "
        "restrained elegance demanded by Yamhill-Carlton's cooler conditions."
    ),
    reputation_narrative=(
        "Soter Vineyards is cited by Wine Advocate (Joe Czerwinski), Wine Spectator, and Oregon wine "
        "specialists as Yamhill-Carlton's most unique producer — the Planet Oregon sparkling Rosé "
        "is considered Oregon's most important méthode champenoise wine, scoring 92-95 and regularly "
        "placed alongside quality Champagne for its precision and complexity. The estate Pinot Noir "
        "consistently scores 93-96 from major critics, making Soter one of Yamhill-Carlton's "
        "essential fine dining wines."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_soter = PROD(
    "Soter North Valley Pinot Noir Yamhill-Carlton",
    "wine_still", p_soter, 36, "USA",
    subcategory="pinot_noir_yamhill_carlton",
    description=(
        "Soter's North Valley Pinot Noir is Yamhill-Carlton from its most biodynamically farmed expression: "
        "Demeter-certified old-vine Pinot from ancient Willakenzie marine sedimentary soils on the "
        "Carlton sub-ridge. Medium ruby with dark cherry, dried rose, earth, limestone mineral, "
        "and a distinctive saline note from the ancient marine sediment. The wine has Yamhill-Carlton's "
        "characteristic cool-climate freshness and mineral precision — more linear and structured than "
        "Dundee Hills, developing beautiful secondary character over 8-12 years."
    ),
    price_tier="premium"
)
PAIR(prod_soter,
    "Duck breast with pickled plum, hazelnuts, and duck jus",
    "complement", "classic", "main",
    "Soter North Valley's marine sediment mineral and dark cherry character achieves a compelling "
    "Yamhill-Carlton pairing with duck breast — the wine's cool-climate precision lifts the "
    "duck's richness while the pickled plum amplifies the Pinot's primary fruit; hazelnuts "
    "bridge the wine's earthy mineral dimension; duck jus creates a wine-sauce harmony. "
    "A pairing of complete Yamhill-Carlton terroir character.")
PAIR(prod_soter,
    "Roasted Dungeness crab with drawn butter and lemon",
    "complement", "established", "main",
    "Soter North Valley's saline marine mineral and structured Pinot character creates an "
    "Oregon coastal pairing — the wine's ancient marine sediment terroir finding its natural "
    "affinity with Dungeness crab. The wine's mineral salinity bridges the crab's natural "
    "brine; drawn butter amplifies the Pinot's richness; lemon echoes the wine's cool-climate "
    "freshness. A Yamhill-Carlton pairing of Oregon's land-sea wine-food heritage.")

# ═══════════════════════════════════════════════════════════════════════════════
# HORSE HEAVEN HILLS (region 23) — second product
# Currently: Andrew Will Champoux Vineyard
# Adding: Canoe Ridge Estate
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── HORSE HEAVEN HILLS — Canoe Ridge Estate ──")
p_canoeridge = P(
    "Canoe Ridge Estate",
    "winery", 23, "USA",
    production_philosophy="Horse Heaven Hills' benchmark estate vineyard: one of Columbia Valley's most important single sites for Merlot and Cabernet from Columbia River-cooled benchland",
    philosophy_description=(
        "Canoe Ridge Estate was established in 1994 on the Horse Heaven Hills benchland above the "
        "Columbia River — one of Washington State's most important single-vineyard sites. The estate's "
        "placement on the north-facing slopes above the Columbia River at 300-450m altitude creates "
        "a microclimate uniquely suited to Merlot and Cabernet Sauvignon: warm afternoons from the "
        "Horse Heaven hills' exposure, cooled by Columbia River breezes that extend the growing season "
        "and preserve natural acidity. The estate's 100-hectare planting is one of Washington's largest "
        "single continuous blocks — providing consistent old-vine material (vines planted 1994) for wines "
        "of growing complexity and structure."
    ),
    reputation_narrative=(
        "Canoe Ridge Estate is cited by Wine Advocate (Paul Gregutt) and Wine Spectator as one of Horse "
        "Heaven Hills' most important producers — their Estate Merlot consistently scoring 91-94 and "
        "demonstrating the sub-AVA's exceptional suitability for this Bordeaux variety in Washington's "
        "climate. The estate provides fine dining sommeliers with a benchmark Horse Heaven Hills wine "
        "that demonstrates the sub-AVA's distinct character from Columbia Valley's broader signature."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_canoeridge = PROD(
    "Canoe Ridge Estate Merlot Horse Heaven Hills",
    "wine_still", p_canoeridge, 23, "USA",
    subcategory="merlot_horse_heaven_hills",
    description=(
        "Canoe Ridge Estate's Merlot is Horse Heaven Hills at its most characteristic: from the "
        "100-hectare benchland vineyard above the Columbia River, cooled by river breezes that "
        "preserve natural acidity alongside Horse Heaven's impressive ripeness. Deep ruby with "
        "dark cherry, plum, chocolate, tobacco, and the distinctive dusty mineral of Columbia River "
        "benchland. The wine has Washington Merlot's characteristic generosity and approachability "
        "combined with Horse Heaven Hills' structural sophistication — developing beautifully over "
        "6-10 years. An approachable but serious expression of the sub-AVA."
    ),
    price_tier="premium"
)
PAIR(prod_canoeridge,
    "Slow-roasted pork belly with apple and sage stuffing",
    "complement", "classic", "main",
    "Canoe Ridge Estate Merlot's dark cherry generosity and tobacco complexity finds an "
    "elegant pairing with roasted pork belly — the wine's Washington Merlot richness "
    "supports the pork's fat without the grip of Cabernet Sauvignon. Apple amplifies the "
    "wine's fruit character; sage bridges the Merlot's earthy tobacco dimension; the slow "
    "roast's caramelisation creates beautiful wine-food tannin integration.")
PAIR(prod_canoeridge,
    "Lamb kefta with roasted eggplant and tzatziki",
    "complement", "established", "main",
    "Canoe Ridge Estate Merlot's plum and chocolate generosity creates a compelling Pacific "
    "Northwest-Mediterranean bridge with lamb kefta — the wine's approachable richness "
    "supports the spiced lamb without dominating; eggplant's earthy depth mirrors the "
    "Merlot's benchland mineral character; tzatziki's yoghurt freshness bridges wine "
    "and food with clean acid. A Horse Heaven Hills pairing of unexpected versatility.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T20 Batch 1 complete.")
print("  Red Mountain: +1 producer (Col Solare), +1 product, +2 pairings")
print("  Rocks District: +1 producer (K Vintners), +1 product, +2 pairings")
print("  Ribbon Ridge: +1 producer (Brick House), +1 product, +2 pairings")
print("  Yamhill-Carlton: +1 producer (Soter), +1 product, +2 pairings")
print("  Horse Heaven Hills: +1 producer (Canoe Ridge), +1 product, +2 pairings")
