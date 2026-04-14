"""
T20 Batch 3: USA sub-AVA depth — second products for 5 single-product regions
Targets: Ancient Lakes (26), Lake Chelan (27), Rattlesnake Hills (24),
         Elkton Oregon (41), Rogue Valley (42)
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

print("=== T20 BATCH 3: USA SUB-AVA DEPTH (5 REGIONS) ===\n")

# ── ANCIENT LAKES (26) — Lone Canary Winery ──
print("── ANCIENT LAKES — Lone Canary Winery ──")
pid = P(
    name="Lone Canary Winery",
    producer_type="winery",
    region_id=26,
    country="USA",
    production_philosophy="Ancient Lakes terroir champion — Riesling and aromatic whites from Washington's cool plateau",
    philosophy_description=(
        "Lone Canary Winery focuses on the Ancient Lakes AVA's exceptional cool-climate potential, "
        "sourcing from the Columbia Plateau's volcanic soils at elevation above the Columbia River. "
        "The Ancient Lakes region's combination of sandy loam soils, intense sun, and cold nights "
        "produces aromatics of exceptional precision and food-friendliness. Lone Canary specialises "
        "in Riesling and Gewürztraminer that showcase the AVA's Germanic character."
    ),
    reputation_narrative=(
        "A dedicated proponent of the Ancient Lakes AVA, Lone Canary demonstrates that Washington's "
        "cooler northern Columbia Plateau can produce aromatic whites of world-class quality and "
        "distinctive character separate from the warmer Yakima and Walla Walla valleys."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Lone Canary Ancient Lakes Riesling",
    category="wine_still",
    producer_id=pid,
    region_id=26,
    origin_country="USA",
    subcategory="Riesling",
    description=(
        "Riesling from the Ancient Lakes AVA of Washington State, sourced from high-elevation "
        "sites on the Columbia Plateau where volcanic soils and cold night temperatures preserve "
        "exceptional aromatic intensity. The Ancient Lakes region receives significantly cooler "
        "temperatures than the rest of the Columbia Valley, with the basalt cliffs of the Columbia "
        "River corridor creating a unique microclimate for aromatic white wines of refreshing "
        "precision and vivid fruit. Lone Canary is a dedicated voice for this underappreciated AVA."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Seared Pacific halibut with citrus beurre blanc and fennel fronds",
     "complement", "classic", "main",
     "Riesling's bright acidity and citrus precision lift delicate halibut and echo beurre blanc")
PAIR(prod,
     "Vietnamese pho with rare beef, rice noodles, and aromatic herb plate",
     "contrast", "established", "main",
     "Off-dry aromatic Riesling soothes star anise and ginger complexity while cooling chilli heat")

# ── LAKE CHELAN (27) — Lake Chelan Winery ──
print("\n── LAKE CHELAN — Lake Chelan Winery ──")
pid = P(
    name="Lake Chelan Winery",
    producer_type="winery",
    region_id=27,
    country="USA",
    production_philosophy="Lake Chelan's founding estate — alpine viticulture above the Cascade foothills",
    philosophy_description=(
        "One of Lake Chelan's founding estate wineries, Lake Chelan Winery was instrumental in "
        "establishing the AVA designation in 2009 for this high-elevation alpine wine region "
        "nestled in the Cascade Mountains. At 1,100 feet elevation along a glacially carved lake, "
        "the estate produces wines of remarkable freshness, with the lake's thermal mass moderating "
        "temperature extremes and creating ideal conditions for Riesling, Pinot Gris, and red Bordeaux varieties."
    ),
    reputation_narrative=(
        "A pioneer in establishing Lake Chelan's wine identity, Lake Chelan Winery continues to "
        "demonstrate the unique terroir potential of Washington's alpine lake district, producing "
        "wines that stand apart from the warmer Columbia Valley appellations."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Lake Chelan Winery Estate Pinot Gris Lake Chelan",
    category="wine_still",
    producer_id=pid,
    region_id=27,
    origin_country="USA",
    subcategory="Pinot Gris",
    description=(
        "Estate Pinot Gris from Lake Chelan Winery, one of the founding estates in the Lake Chelan "
        "AVA established in 2009. Situated at 1,100 feet elevation along the glacially carved Lake "
        "Chelan in the North Cascade foothills, the estate benefits from the lake's thermal mass, "
        "which extends the growing season and moderates extreme temperatures. The resulting Pinot Gris "
        "shows the Italian-influenced richness of Alsatian weight combined with Pacific Northwest "
        "freshness — a textural, food-friendly expression of this underappreciated Washington AVA."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Roasted pork tenderloin with apple-sage stuffing and caramelised onion gravy",
     "complement", "established", "main",
     "Textural Pinot Gris' richness complements pork's fat while apple notes echo stuffing")
PAIR(prod,
     "Smoked trout dip with cream cheese, dill, and rye crackers",
     "complement", "classic", "casual",
     "Wine's body and acidity balance smoked fish richness; orchard fruit notes complement dill")

# ── RATTLESNAKE HILLS (24) — Bonair Winery ──
print("\n── RATTLESNAKE HILLS — Bonair Winery ──")
pid = P(
    name="Bonair Winery",
    producer_type="winery",
    region_id=24,
    country="USA",
    production_philosophy="Rattlesnake Hills estate pioneer — Yakima Valley's volcanic bench specialist",
    philosophy_description=(
        "Bonair Winery is one of the Rattlesnake Hills AVA's founding producers, farming estate "
        "vineyards on the basalt-covered volcanic benches south of the Yakima River. The Rattlesnake "
        "Hills benefit from higher elevation than the valley floor, producing red wines of greater "
        "structure and aromatics. Bonair focuses on Cabernet Sauvignon and Chardonnay that express "
        "the region's volcanic mineral complexity and moderate temperatures."
    ),
    reputation_narrative=(
        "As a Rattlesnake Hills pioneer, Bonair Winery demonstrates the distinctive character of "
        "this elevated Yakima Valley sub-AVA, producing wines that benefit from the basalt bench's "
        "heat retention and the elevation's cooling influence on aromatic development."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Bonair Winery Rattlesnake Hills Cabernet Sauvignon",
    category="wine_still",
    producer_id=pid,
    region_id=24,
    origin_country="USA",
    subcategory="Cabernet Sauvignon",
    description=(
        "Estate Cabernet Sauvignon from Bonair Winery's vineyards on the Rattlesnake Hills AVA's "
        "elevated volcanic bench above the Yakima River. The Rattlesnake Hills' basalt-covered "
        "benches sit at higher elevation than the Yakima Valley floor, creating a distinct microclimate "
        "with excellent heat retention through the day and cooler nights that preserve aromatic "
        "complexity. The resulting Cabernet Sauvignon shows Washington's characteristic density "
        "and structure with additional mineral complexity from the volcanic substrate."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Grilled rack of lamb with herb crust and roasted root vegetables",
     "complement", "classic", "main",
     "Washington Cab's structure and dark fruit match lamb's gaminess and roasted herbal notes")
PAIR(prod,
     "Sharp aged cheddar, candied walnuts, and dried cherry board",
     "complement", "established", "cheese",
     "Cassis-driven Cabernet bridges aged cheese fat while tannins cleanse the palate")

# ── ELKTON OREGON (41) — Rivers Edge Winery ──
print("\n── ELKTON OREGON — River's Edge Winery ──")
pid = P(
    name="River's Edge Winery — Elkton Oregon",
    producer_type="winery",
    region_id=41,
    country="USA",
    production_philosophy="Elkton Oregon's cool maritime pioneer — Pinot Noir at the edge of possibility",
    philosophy_description=(
        "River's Edge Winery is situated in the Elkton Oregon AVA, one of the Umpqua Valley's "
        "coolest sub-AVAs where the North Umpqua and Umpqua Rivers create a maritime corridor "
        "for cool Pacific air to penetrate inland. The Elkton Oregon designation was established "
        "to capture this distinctive cool-climate character, particularly suited to Pinot Noir, "
        "Pinot Gris, and aromatic varieties that struggle in warmer Umpqua locations. The winery "
        "emphasises site-specific expression in this underexplored Oregon AVA."
    ),
    reputation_narrative=(
        "A dedicated advocate for the Elkton Oregon AVA's distinct cool-climate character, River's "
        "Edge demonstrates that the Umpqua River corridor can produce Pinot Noir of genuine "
        "elegance and Burgundian restraint quite different from warmer Oregon regions."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="River's Edge Winery Elkton Oregon Pinot Noir",
    category="wine_still",
    producer_id=pid,
    region_id=41,
    origin_country="USA",
    subcategory="Pinot Noir",
    description=(
        "Pinot Noir from the Elkton Oregon AVA, one of the Umpqua Valley's coolest and most "
        "maritime-influenced sub-appellations, where the Umpqua River corridor channels Pacific "
        "air deep into the interior. This cool-climate influence creates growing conditions "
        "distinctly different from the warmer Umpqua Valley proper, producing Pinot Noir of "
        "refreshing acidity, delicate aromatics, and Burgundian restraint. The Elkton Oregon "
        "designation was established specifically to recognise this unique terroir pocket."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Roasted quail with pomegranate reduction and wild rice pilaf",
     "complement", "established", "main",
     "Cool-climate Pinot's delicacy matches quail's lightness; pomegranate echoes red fruit")
PAIR(prod,
     "Pacific Northwest charcuterie with smoked duck, hazelnuts, and lingonberry jam",
     "complement", "classic", "starter",
     "Elegant Pinot's earthy undertones complement cured meats while acidity cuts through fat")

# ── ROGUE VALLEY (42) — EdenVale Winery ──
print("\n── ROGUE VALLEY — EdenVale Winery ──")
pid = P(
    name="EdenVale Winery",
    producer_type="winery",
    region_id=42,
    country="USA",
    production_philosophy="Rogue Valley heritage estate — Southern Oregon's Bordeaux specialist",
    philosophy_description=(
        "EdenVale Winery is one of the Rogue Valley's most established estate wineries, "
        "situated in the Medford area of Southern Oregon. The estate farms Bordeaux varietals "
        "that thrive in the Rogue Valley's Mediterranean-influenced climate — warm days, "
        "cool nights, and exceptional sunshine hours that allow Merlot, Cabernet Franc, and "
        "Cabernet Sauvignon to reach genuine ripeness. EdenVale's historic farmstead property "
        "adds historical character to their commitment to estate-grown, Southern Oregon wines."
    ),
    reputation_narrative=(
        "EdenVale represents the Rogue Valley's potential for serious Bordeaux-style wines, "
        "demonstrating that Southern Oregon's warm, dry climate can produce structured, age-worthy "
        "red wines with genuine complexity and regional character."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="EdenVale Winery Rogue Valley Merlot",
    category="wine_still",
    producer_id=pid,
    region_id=42,
    origin_country="USA",
    subcategory="Merlot",
    description=(
        "Estate Merlot from EdenVale Winery in the Rogue Valley AVA, Southern Oregon, where "
        "the Mediterranean-influenced climate — warm sunny days and cool nights moderated by "
        "Cascade Mountain air — allows Merlot to develop full ripeness while retaining freshness. "
        "The Rogue Valley's volcanic and alluvial soils provide excellent drainage, concentrating "
        "flavours without irrigation stress. EdenVale's historic farmstead property in the Medford "
        "area produces Merlot of genuine plush character with Southern Oregon's characteristic "
        "brightness."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Slow-roasted pork shoulder with plum and port glaze and roasted fennel",
     "complement", "classic", "main",
     "Plush Merlot's dark plum and velvet tannins harmonise with braised pork and sweet glaze")
PAIR(prod,
     "Mushroom and truffle tart with Gruyère and fresh thyme",
     "complement", "established", "main",
     "Merlot's earthy, fruit-forward character bridges mushroom umami and truffle's earthiness")

print("\n✅ T20 Batch 3 complete.")
print("  Ancient Lakes (26): +1 producer (Lone Canary), +1 product, +2 pairings")
print("  Lake Chelan (27): +1 producer (Lake Chelan Winery), +1 product, +2 pairings")
print("  Rattlesnake Hills (24): +1 producer (Bonair), +1 product, +2 pairings")
print("  Elkton Oregon (41): +1 producer (River's Edge), +1 product, +2 pairings")
print("  Rogue Valley (42): +1 producer (EdenVale), +1 product, +2 pairings")

cur.close()
conn.close()
