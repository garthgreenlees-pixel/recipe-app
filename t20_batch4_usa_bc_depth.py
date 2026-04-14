"""
T20 Batch 4: USA remaining sub-AVAs + BC Canada start
Targets: Naches Heights (28), Snipes Mountain (29), Applegate Valley (43),
         Columbia Gorge (30), Golden Mile Bench (9)
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

print("=== T20 BATCH 4: USA REMAINING + BC CANADA DEPTH (5 REGIONS) ===\n")

# ── NACHES HEIGHTS (28) — Treveri Cellars ──
print("── NACHES HEIGHTS — Treveri Cellars ──")
pid = P(
    name="Treveri Cellars",
    producer_type="winery",
    region_id=28,
    country="USA",
    production_philosophy="Washington sparkling wine specialist — Méthode Traditionnelle from Naches Heights elevation",
    philosophy_description=(
        "Treveri Cellars is Washington State's premier sparkling wine producer, established by "
        "the Buis family with expertise rooted in German sparkling wine tradition. The Naches "
        "Heights AVA's elevation above the Yakima Valley floor provides the cooler conditions "
        "essential for developing the natural acidity and delicate aromatics required for "
        "traditional-method sparkling wine. Treveri sources from Naches Heights and works "
        "exclusively with the méthode traditionnelle to produce Washington's most serious "
        "sparkling wines."
    ),
    reputation_narrative=(
        "Treveri established Washington State as a credible source of traditional-method "
        "sparkling wine, earning national recognition and demonstrating that the Naches Heights "
        "AVA's cool elevation is particularly suited to the unique demands of Champagne-method production."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Treveri Cellars Blanc de Blancs Brut Naches Heights",
    category="wine_sparkling",
    producer_id=pid,
    region_id=28,
    origin_country="USA",
    subcategory="Blanc de Blancs",
    description=(
        "Traditional-method Blanc de Blancs from Treveri Cellars, Washington State's leading "
        "sparkling wine producer, sourcing from the Naches Heights AVA's elevated vineyards "
        "above the Yakima Valley. The Naches Heights' cooler temperatures compared to the valley "
        "floor preserve the natural acidity essential for fine sparkling wine, while the volcanic "
        "basalt soils contribute a distinctive mineral character. Produced via méthode traditionnelle "
        "with extended lees aging, this all-Chardonnay cuvée demonstrates the Naches Heights' "
        "unique suitability for sparkling wine production in Washington State."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Dungeness crab cocktail with green goddess dressing and avocado",
     "complement", "classic", "starter",
     "Blanc de Blancs' chalky mousse and citrus precision elevate delicate crab sweetness")
PAIR(prod,
     "Parmesan arancini with saffron aioli and micro herbs",
     "cleanse", "established", "amuse",
     "Persistent bubbles and acidity cut through arancini's fried richness; mineral finish refreshes")

# ── SNIPES MOUNTAIN (29) — Kerloo Cellars ──
print("\n── SNIPES MOUNTAIN — Kerloo Cellars ──")
pid = P(
    name="Kerloo Cellars",
    producer_type="winery",
    region_id=29,
    country="USA",
    production_philosophy="Rhône specialist from Washington's smallest designated winegrowing region",
    philosophy_description=(
        "Kerloo Cellars is a small, quality-focused Washington producer specialising in Rhône "
        "varietals from the Snipes Mountain AVA, one of Washington's smallest and most distinctive "
        "appellations. The Snipes Mountain is a basalt mound rising from the Yakima Valley floor, "
        "providing unique south-facing exposures and warm, rocky soils that give the region's "
        "Grenache, Syrah, and Mourvèdre exceptional richness and concentration. Kerloo's "
        "commitment to minimal intervention and indigenous fermentation preserves the site's "
        "distinctive volcanic character."
    ),
    reputation_narrative=(
        "Kerloo Cellars has become a respected voice for Snipes Mountain's distinctive volcanic "
        "terroir, producing Rhône-style blends that showcase the region's unique combination "
        "of warmth, elevation, and basalt mineral complexity."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Kerloo Cellars Snipes Mountain Grenache",
    category="wine_still",
    producer_id=pid,
    region_id=29,
    origin_country="USA",
    subcategory="Grenache",
    description=(
        "Grenache from the Snipes Mountain AVA, one of Washington State's smallest and most "
        "distinctive wine appellations. The Snipes Mountain is a volcanic basalt mound rising "
        "above the Yakima Valley floor, its south-facing slopes and rocky soils creating exceptional "
        "warmth and drainage ideal for Grenache. The resulting wine shows Washington's characteristic "
        "concentration combined with Grenache's distinctive raspberry and Provençal herb character, "
        "amplified by the basalt's mineral signature. Kerloo Cellars' minimal-intervention approach "
        "preserves the site's unique expression."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Roasted lamb chops with herbes de Provence, ratatouille, and tapenade",
     "complement", "classic", "main",
     "Grenache's raspberry and Provençal herb character mirrors lamb's herbal crust and ratatouille")
PAIR(prod,
     "Grilled merguez sausage with harissa, flatbread, and cucumber-mint yoghurt",
     "complement", "established", "main",
     "Grenache's warmth and spice amplify merguez aromatics while fruit balances harissa heat")

# ── APPLEGATE VALLEY (43) — Troon Vineyard ──
print("\n── APPLEGATE VALLEY — Troon Vineyard ──")
pid = P(
    name="Troon Vineyard",
    producer_type="winery",
    region_id=43,
    country="USA",
    production_philosophy="Biodynamic Applegate Valley pioneer — regenerative farming and natural wine",
    philosophy_description=(
        "Troon Vineyard is one of the Applegate Valley's most important estates, practising "
        "certified biodynamic and regenerative farming on their dramatic hillside vineyard in "
        "Southern Oregon's Applegate Valley sub-AVA. Under winemaker Nate Wall, Troon has become "
        "a beacon for natural wine production in Oregon, focusing on skin-contact whites, "
        "field blends, and minimal-intervention reds from their diverse planting of Rhône, "
        "Italian, and Iberian varietals suited to the warm Applegate climate."
    ),
    reputation_narrative=(
        "Troon Vineyard is one of the Pacific Northwest's most exciting natural wine producers, "
        "combining certified biodynamic farming with creative winemaking to produce wines of "
        "genuine character that have placed the Applegate Valley on the national natural wine map."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Troon Vineyard Applegate Valley Vermentino",
    category="wine_still",
    producer_id=pid,
    region_id=43,
    origin_country="USA",
    subcategory="Vermentino",
    description=(
        "Vermentino from Troon Vineyard's certified biodynamic estate in the Applegate Valley, "
        "Southern Oregon. The Applegate Valley's warm days and cool nights — moderated by "
        "elevation and proximity to the Siskiyou Mountains — create ideal conditions for "
        "Mediterranean varietals like Vermentino that thrive in sun-drenched, well-drained "
        "hillside soils. Troon's minimal-intervention winemaking, including native fermentation "
        "and extended skin contact, produces a textural, savoury Vermentino with distinctive "
        "bitter almond finish characteristic of the variety at its best."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Grilled branzino with lemon, capers, Castelvetrano olives, and charred fennel",
     "complement", "classic", "main",
     "Vermentino's saline mineral and bitter almond character mirror Mediterranean fish preparations")
PAIR(prod,
     "Burrata with heirloom tomatoes, basil, and aged balsamic drizzle",
     "complement", "established", "starter",
     "Textural skin-contact Vermentino bridges creamy burrata and acidic tomatoes beautifully")

# ── COLUMBIA GORGE (30) — Marchesi Vineyards ──
print("\n── COLUMBIA GORGE — Marchesi Vineyards ──")
pid = P(
    name="Marchesi Vineyards",
    producer_type="winery",
    region_id=30,
    country="USA",
    production_philosophy="Columbia Gorge Italian specialist — Nebbiolo and Sangiovese in the wind corridor",
    philosophy_description=(
        "Marchesi Vineyards is a Columbia Gorge AVA producer with Italian roots, specialising "
        "in Nebbiolo, Sangiovese, and Dolcetto planted on north-bank Washington slopes above "
        "the Columbia River. The Columbia Gorge's famous wind corridor — the same phenomenon "
        "that powers wind turbines across the region — creates diurnal temperature swings that "
        "rival Piedmont's Alpine foothill climate, making it surprisingly suitable for northern "
        "Italian varietals that require long, cool growing seasons. The Marchesi family's Italian "
        "heritage informs a traditional, terroir-focused approach to winemaking."
    ),
    reputation_narrative=(
        "Marchesi Vineyards demonstrates the Columbia Gorge's unexpected affinity for Italian "
        "varietals, producing some of Washington and Oregon's most distinctive Nebbiolo from "
        "one of the Pacific Northwest's most climatically unique wine appellations."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Marchesi Vineyards Columbia Gorge Nebbiolo",
    category="wine_still",
    producer_id=pid,
    region_id=30,
    origin_country="USA",
    subcategory="Nebbiolo",
    description=(
        "Nebbiolo from Marchesi Vineyards in the Columbia Gorge AVA, planted on steep north-bank "
        "Washington slopes above the Columbia River. The Columbia Gorge's dramatic winds create "
        "temperature swings of 30°C between day and night, producing the slow, even ripening "
        "essential for Nebbiolo's demanding character. This New World Nebbiolo shows the variety's "
        "signature combination of assertive tannins, high acidity, and complex aromatics of dried "
        "rose, tar, leather, and wild cherry — a genuinely distinctive expression from one of "
        "America's most unusual wine regions."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Braised beef short rib with truffle polenta and Barolo-reduction jus",
     "complement", "classic", "main",
     "Nebbiolo's tannin and acidity cut through short rib fat; dried cherry mirrors braising notes")
PAIR(prod,
     "Aged Parmigiano-Reggiano and prosciutto di Parma with fig mostarda",
     "complement", "established", "cheese",
     "Classic Piedmontese pairing — Nebbiolo's tannins bind with aged cheese protein perfectly")

# ── GOLDEN MILE BENCH (9) — Tinhorn Creek Vineyards ──
print("\n── GOLDEN MILE BENCH — Tinhorn Creek Vineyards ──")
pid = P(
    name="Tinhorn Creek Vineyards",
    producer_type="winery",
    region_id=9,
    country="Canada",
    production_philosophy="Golden Mile Bench champion — BC's Bordeaux varietals from sun-drenched south-facing slopes",
    philosophy_description=(
        "Tinhorn Creek Vineyards is one of the Golden Mile Bench's defining estates, situated "
        "on the dramatic south-facing slopes between Oliver and Osoyoos in BC's southern Okanagan. "
        "The Golden Mile Bench designation was specifically created to recognise the distinctive "
        "terroir of these western benchland slopes, where volcanic and alluvial soils, intense "
        "sunshine, and exceptional drainage produce BC's most powerful red wines. Tinhorn Creek "
        "has championed sustainable viticulture and BC's capacity for serious Cabernet Franc, "
        "Merlot, and Cabernet Sauvignon since the 1990s."
    ),
    reputation_narrative=(
        "Tinhorn Creek is one of BC's most respected mid-scale estates, consistently producing "
        "wines that express the Golden Mile Bench's distinctive sun-drenched character and "
        "advocating for this unique appellation's global recognition."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Tinhorn Creek Oldfield Series Cabernet Franc Golden Mile Bench",
    category="wine_still",
    producer_id=pid,
    region_id=9,
    origin_country="Canada",
    subcategory="Cabernet Franc",
    description=(
        "Cabernet Franc from Tinhorn Creek Vineyards' reserve Oldfield Series, grown on the "
        "Golden Mile Bench's volcanic and alluvial south-facing slopes between Oliver and Osoyoos. "
        "The Golden Mile Bench's exceptional sun exposure — the most intense in British Columbia — "
        "combined with the volcanic benchland soils, produces Cabernet Franc of distinctive warmth "
        "and aromatic complexity. Tinhorn Creek's reserve programme showcases the best blocks from "
        "their estate, producing BC's most serious expression of this Bordeaux variety with "
        "characteristic violet, dark fruit, and graphite complexity."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Roasted duck leg confit with wild blueberry gastrique and celeriac purée",
     "complement", "classic", "main",
     "Cabernet Franc's violet and dark fruit harmonise with duck's richness and blueberry's brightness")
PAIR(prod,
     "Herb-crusted rack of lamb with Okanagan cherry reduction and rosemary jus",
     "complement", "established", "main",
     "BC Cab Franc's structure and herbaceous lift complement lamb's garlic-herb crust and cherry")

print("\n✅ T20 Batch 4 complete.")
print("  Naches Heights (28): +1 producer (Treveri), +1 product, +2 pairings")
print("  Snipes Mountain (29): +1 producer (Kerloo), +1 product, +2 pairings")
print("  Applegate Valley (43): +1 producer (Troon), +1 product, +2 pairings")
print("  Columbia Gorge (30): +1 producer (Marchesi), +1 product, +2 pairings")
print("  Golden Mile Bench (9): +1 producer (Tinhorn Creek), +1 product, +2 pairings")

cur.close()
conn.close()
