"""
T20 Batch 2: Oregon + Washington single-product region depth
Targets: McMinnville (37), Van Duzer Corridor (39), Umpqua Valley (40),
         Southern Oregon (32), Yakima Valley (21)
"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
conn.autocommit = True
cur = conn.cursor()

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

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence,
           meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T20 BATCH 2: OREGON + WASHINGTON DEPTH (5 REGIONS) ===\n")

# ── McMINNVILLE (37) — Nicolas-Jay ──
print("── McMINNVILLE — Nicolas-Jay ──")
pid = P(
    name="Nicolas-Jay",
    producer_type="winery",
    region_id=37,
    country="USA",
    production_philosophy="Burgundian precision applied to Oregon terroir",
    philosophy_description=(
        "A collaboration between Jean-Nicolas Méo of Maison Méo-Camuzet and Jay Boberg, "
        "Nicolas-Jay applies Burgundian principles of minimal intervention and terroir expression "
        "to estate fruit from the Eola-Amity Hills and Yamhill-Carlton districts, producing "
        "benchmark Willamette Valley Pinot Noir with extraordinary concentration and finesse."
    ),
    reputation_narrative=(
        "Immediately acclaimed upon release, Nicolas-Jay quickly established itself among "
        "Oregon's most prestigious Pinot Noir estates, with Méo's Burgundy expertise elevating "
        "Pacific Northwest terroir to a global conversation."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)
prod = PROD(
    name="Nicolas-Jay Kolpakowski Vineyard Pinot Noir McMinnville",
    category="wine_still",
    producer_id=pid,
    region_id=37,
    origin_country="USA",
    subcategory="Pinot Noir",
    description=(
        "Single-vineyard Pinot Noir from the Kolpakowski Vineyard in the McMinnville AVA, "
        "produced by the Jean-Nicolas Méo and Jay Boberg partnership. McMinnville's marine "
        "sedimentary soils and proximity to the Van Duzer Corridor create wines of exceptional "
        "complexity — earthy, spiced, and deeply structured. Vinified with Burgundian restraint, "
        "whole-cluster fermentation, and aging in French oak from Méo's personal cooperage contacts."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Roasted duck breast with cherry gastrique and wild mushroom ragout",
     "complement", "classic", "main",
     "Cherry fruit and earthy complexity mirror duck's richness; acidity cuts the fat elegantly")
PAIR(prod,
     "Oregon black truffle risotto with aged Comté",
     "complement", "established", "main",
     "Forest floor notes and Burgundian structure elevate truffle's earthiness")

# ── VAN DUZER CORRIDOR (39) — Willamette Valley Vineyards ──
print("\n── VAN DUZER CORRIDOR — Willamette Valley Vineyards ──")
pid = P(
    name="Willamette Valley Vineyards",
    producer_type="winery",
    region_id=39,
    country="USA",
    production_philosophy="People's wine — Oregon's farmer-owned Pinot estate",
    philosophy_description=(
        "Founded by Jim Bernau in 1983, Willamette Valley Vineyards operates as a public "
        "benefit corporation with over 10,000 co-owner shareholders. The Van Duzer Estate sits "
        "directly in the wind corridor, producing Pinot Noir of remarkable coolness and aromatic "
        "precision from estate vineyards farmed sustainably with Salmon-Safe certification."
    ),
    reputation_narrative=(
        "WVV combines scale with quality and mission, demonstrating that sustainable farming "
        "and broad accessibility can coexist with serious winemaking ambition in Oregon."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Willamette Valley Vineyards Van Duzer Estates Pinot Noir",
    category="wine_still",
    producer_id=pid,
    region_id=39,
    origin_country="USA",
    subcategory="Pinot Noir",
    description=(
        "Estate Pinot Noir from Willamette Valley Vineyards' Van Duzer Estate, situated directly "
        "in the wind corridor that gives the AVA its name. The Coast Range gap funnels cool Pacific "
        "air through the estate, creating long hang times and wines of intense aromatics and bright "
        "acidity. Farmed sustainably with Salmon-Safe certification; minimal-intervention winemaking "
        "preserves site character."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Pan-seared Chinook salmon with pinot reduction and hazelnut butter",
     "bridge", "classic", "main",
     "Oregon's iconic pairing — salmon and Pinot Noir share earthy, fruity affinity")
PAIR(prod,
     "Charcuterie board with aged Tillamook cheddar and Oregon hazelnuts",
     "complement", "established", "casual",
     "Cool-climate Pinot's freshness cuts through fat and amplifies charcuterie complexity")

# ── UMPQUA VALLEY (40) — HillCrest Vineyard ──
print("\n── UMPQUA VALLEY — HillCrest Vineyard ──")
pid = P(
    name="HillCrest Vineyard",
    producer_type="winery",
    region_id=40,
    country="USA",
    production_philosophy="Oregon's first estate — pioneering Umpqua since 1961",
    philosophy_description=(
        "Established in 1961 by Richard Sommer, HillCrest Vineyard is Oregon's oldest continually "
        "producing winery. Sommer planted Riesling and other vinifera varietals in the Umpqua "
        "Valley long before the Willamette Valley wine boom, proving the Oregon Coast Ranges "
        "could produce world-class wine. The estate remains dedicated to its pioneering heritage "
        "with minimal-intervention farming and traditional winemaking."
    ),
    reputation_narrative=(
        "As Oregon's founding estate, HillCrest holds irreplaceable historical significance. "
        "Sommer's vision predating the Eyrie Vineyards Burgundy comparison by nearly a decade "
        "established Oregon as a serious wine state."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="HillCrest Vineyard Umpqua Valley Riesling",
    category="wine_still",
    producer_id=pid,
    region_id=40,
    origin_country="USA",
    subcategory="Riesling",
    description=(
        "Estate Riesling from Oregon's oldest continually producing winery, established by "
        "Richard Sommer in 1961. The Umpqua Valley's warmer and drier climate compared to "
        "the Willamette Valley produces Riesling of greater body and richness, with distinctive "
        "orchard fruit character tempered by the Umpqua River Valley's elevation and cooling "
        "marine influence."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Dungeness crab with drawn butter and Meyer lemon",
     "complement", "classic", "main",
     "Off-dry Riesling's stone fruit and acidity cut through crab butter perfectly")
PAIR(prod,
     "Spicy Thai green curry with jasmine rice",
     "contrast", "established", "main",
     "Residual sugar and vibrant acidity tame chilli heat while fruit mirrors curry aromatics")

# ── SOUTHERN OREGON (32) — Del Rio Vineyards ──
print("\n── SOUTHERN OREGON — Del Rio Vineyards ──")
pid = P(
    name="Del Rio Vineyards",
    producer_type="winery",
    region_id=32,
    country="USA",
    production_philosophy="Rogue River estate benchmark — Rhône varietals in Southern Oregon sunshine",
    philosophy_description=(
        "Del Rio Vineyards is one of Southern Oregon's largest estate operations, farming 250 acres "
        "along the Rogue River in the Rock Point area of Southern Oregon. The estate supplies fruit "
        "to notable producers while making its own wines across Bordeaux, Rhône, and Italian varietals "
        "that thrive in Southern Oregon's warmer, sunnier climate. Rock Point volcanic soils produce "
        "wines of distinctive minerality and depth."
    ),
    reputation_narrative=(
        "Del Rio is Southern Oregon's most significant estate vineyard, supplying fruit to acclaimed "
        "producers across the state while building a respected reputation for estate wines of genuine "
        "terroir character."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Del Rio Vineyards Rock Point Estate Syrah Southern Oregon",
    category="wine_still",
    producer_id=pid,
    region_id=32,
    origin_country="USA",
    subcategory="Syrah",
    description=(
        "Estate Syrah from Del Rio Vineyards' Rock Point holdings along the Rogue River, Southern "
        "Oregon. The Rogue River Valley's Mediterranean-influenced climate — warm days, cool nights, "
        "and abundant sunshine — produces Syrah of Northern Rhône concentration with Pacific Northwest "
        "freshness. Volcanic basalt and alluvial soils on the Rock Point bench provide excellent "
        "drainage and mineral complexity."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Wood-grilled Wagyu hanger steak with chimichurri and roasted bone marrow",
     "complement", "classic", "main",
     "Full-bodied Syrah's dark fruit and savoury complexity match Wagyu's richness and marbling")
PAIR(prod,
     "Slow-braised lamb shoulder with Moroccan spices, preserved lemon, and couscous",
     "complement", "established", "main",
     "Syrah's pepper, leather, and dark fruit echo Northern African spice palate")

# ── YAKIMA VALLEY (21) — Kiona Vineyards ──
print("\n── YAKIMA VALLEY — Kiona Vineyards ──")
pid = P(
    name="Kiona Vineyards and Winery",
    producer_type="winery",
    region_id=21,
    country="USA",
    production_philosophy="Red Mountain's founding family — Washington pioneer estate since 1975",
    philosophy_description=(
        "Founded in 1975 by John Williams and Jim Holmes on Red Mountain — before Red Mountain had "
        "its own appellation — Kiona Vineyards holds the distinction of being among Washington's "
        "oldest estate wineries. While Red Mountain grew around them, Kiona remains a family operation "
        "producing wines from both their legendary Red Mountain holdings and broader Yakima Valley fruit, "
        "with a particularly noted Lemberger programme that introduced the variety to Washington."
    ),
    reputation_narrative=(
        "As one of Washington's founding estates, Kiona carries the weight of history while continuing "
        "to produce wines of genuine distinction from one of America's most powerful wine regions. "
        "Their Lemberger is the definitive American expression of this Austrian variety."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Kiona Vineyards Estate Cabernet Sauvignon Yakima Valley",
    category="wine_still",
    producer_id=pid,
    region_id=21,
    origin_country="USA",
    subcategory="Cabernet Sauvignon",
    description=(
        "Estate Cabernet Sauvignon from one of Washington State's founding wineries, planted on "
        "the slopes of Red Mountain within the broader Yakima Valley AVA. John Williams and Jim Holmes "
        "established Kiona in 1975, before Red Mountain existed as a designated appellation, making "
        "this estate a living monument to Washington's pioneer era. The Yakima Valley's Continental "
        "climate — extreme diurnal variation, low rainfall, and abundant sunshine — produces Cabernet "
        "of exceptional concentration and aging potential."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Dry-aged bone-in ribeye with roasted garlic compound butter and crispy rosemary potatoes",
     "complement", "classic", "main",
     "Washington Cab's power and structure match dry-aged beef's umami intensity and fat")
PAIR(prod,
     "Cedar-planked king salmon with apple-smoked bacon lardons and blackberry compote",
     "bridge", "established", "main",
     "Dark fruit mirrors compote; cedar and smoke echo plank-cooked salmon's character")

print("\n✅ T20 Batch 2 complete.")
print("  McMinnville (37): +1 producer (Nicolas-Jay), +1 product, +2 pairings")
print("  Van Duzer Corridor (39): +1 producer (WVV), +1 product, +2 pairings")
print("  Umpqua Valley (40): +1 producer (HillCrest), +1 product, +2 pairings")
print("  Southern Oregon (32): +1 producer (Del Rio), +1 product, +2 pairings")
print("  Yakima Valley (21): +1 producer (Kiona), +1 product, +2 pairings")

cur.close()
conn.close()
