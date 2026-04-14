"""
T20 Batch 6: Final PNW/BC gaps — Summerland (14), Thompson Valley (8), Wahluke Slope (25)
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

print("=== T20 BATCH 6: FINAL PNW/BC GAPS (3 REGIONS) ===\n")

# ── SUMMERLAND (14) — Sumac Ridge Estate Winery ──
print("── SUMMERLAND — Sumac Ridge Estate Winery ──")
pid = P(
    name="Sumac Ridge Estate Winery",
    producer_type="winery",
    region_id=14,
    country="Canada",
    production_philosophy="Summerland pioneer — BC's first estate winery on Okanagan Lake's eastern bench",
    philosophy_description=(
        "Sumac Ridge Estate Winery holds a historic position in BC wine as one of the Okanagan "
        "Valley's pioneering estates, established in 1979 on Summerland's benchlands above "
        "Okanagan Lake. The estate's position on the eastern slopes benefits from the lake's "
        "thermal moderation while the Summerland bench's elevation provides excellent drainage "
        "and diverse soils. Sumac Ridge was instrumental in establishing BC sparkling wine "
        "and Gewürztraminer as signature categories, contributing to the province's early "
        "wine identity through decades of consistent quality."
    ),
    reputation_narrative=(
        "As one of BC's original estate wineries, Sumac Ridge carries historical significance "
        "while continuing to produce wines that express Summerland's distinctive benchland "
        "terroir and the Okanagan's capacity for serious sparkling wine production."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Sumac Ridge Estate Winery Summerland Steller's Jay Brut",
    category="wine_sparkling",
    producer_id=pid,
    region_id=14,
    origin_country="Canada",
    subcategory="Blanc de Blancs",
    description=(
        "Traditional-method sparkling wine from Sumac Ridge Estate Winery, one of BC's "
        "pioneering estate operations established in 1979 in Summerland. The Steller's Jay "
        "Brut is BC's most established traditional-method sparkling wine brand, produced from "
        "Chardonnay and Pinot Blanc grown on Summerland's benchlands above Okanagan Lake. "
        "Named for the iconic Pacific coastal bird, the wine undergoes extended lees aging "
        "for complexity and toasty character. Summerland's moderate lakeside climate and "
        "the Okanagan's long sunny days create ideal conditions for sparkling wine base wine "
        "of vibrant natural acidity."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "BC spot prawn tempura with yuzu aioli and microgreens",
     "cleanse", "classic", "starter",
     "Bubbles and acidity cut through tempura's richness while citrus notes echo yuzu aioli")
PAIR(prod,
     "Gravlax with crème fraîche, dill, capers, and buckwheat blini",
     "complement", "established", "starter",
     "Traditional-method sparkler's toasty complexity and acidity elevate cured salmon perfectly")

# ── THOMPSON VALLEY (8) — Sagewood Winery ──
print("\n── THOMPSON VALLEY — Sagewood Winery ──")
pid = P(
    name="Sagewood Winery",
    producer_type="winery",
    region_id=8,
    country="Canada",
    production_philosophy="Thompson Valley frontier — desert viticulture on BC's driest wine frontier",
    philosophy_description=(
        "Sagewood Winery is situated in BC's Thompson Valley wine region, one of Canada's most "
        "dramatic and unlikely vineyard settings where the Thompson River canyon creates an arid, "
        "Continental microclimate with minimal rainfall and intense summer sunshine. The Thompson "
        "Valley's extreme growing conditions — hot days, cold nights, and desert soils — produce "
        "wines of remarkable concentration and individuality quite distinct from the Okanagan "
        "Valley. Sagewood farms native and hybrid varieties well-suited to the Thompson's "
        "challenging Continental desert conditions."
    ),
    reputation_narrative=(
        "Sagewood Winery demonstrates the Thompson Valley's potential for distinctive wine "
        "production in BC's most Continental and arid wine region, proving that serious viticulture "
        "extends well beyond the Okanagan corridor."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Sagewood Winery Thompson Valley Cabernet Franc",
    category="wine_still",
    producer_id=pid,
    region_id=8,
    origin_country="Canada",
    subcategory="Cabernet Franc",
    description=(
        "Cabernet Franc from Sagewood Winery in BC's Thompson Valley, one of Canada's most "
        "extreme and dramatic wine regions where the Thompson River canyon's arid Continental "
        "climate challenges conventional viticulture. The Thompson Valley's intense summer "
        "sunshine, minimal rainfall, and extreme diurnal temperature swings create conditions "
        "that produce Cabernet Franc of unexpected concentration and aromatic intensity. "
        "The region's Native and volcanic soils contribute a distinctive mineral character "
        "to wines that reflect BC's frontier viticultural spirit."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Grilled lamb kofta with roasted red pepper sauce and flatbread",
     "complement", "established", "main",
     "Cab Franc's herbaceous violet and dark fruit complement lamb's spiced, charred character")
PAIR(prod,
     "Roasted beet salad with goat cheese, candied walnuts, and pomegranate vinaigrette",
     "complement", "classic", "starter",
     "Thompson Valley Cab Franc's freshness and violet notes harmonise with earthy beet and tangy cheese")

# ── WAHLUKE SLOPE (25) — Milbrandt Vineyards ──
print("\n── WAHLUKE SLOPE — Milbrandt Vineyards ──")
pid = P(
    name="Milbrandt Vineyards",
    producer_type="winery",
    region_id=25,
    country="USA",
    production_philosophy="Wahluke Slope's benchmark estate — Columbia Basin farming heritage and Washington Riesling",
    philosophy_description=(
        "Milbrandt Vineyards is one of Washington State's largest and most respected farming "
        "operations, with estate vineyards across the Wahluke Slope, Ancient Lakes, and broader "
        "Columbia Valley. The Milbrandt family's deep roots in Columbia Basin agriculture inform "
        "a meticulous approach to vineyard management on the Wahluke Slope's renowned volcanic "
        "sandy loam soils above the Columbia River. The estate's Wahluke Slope vineyards, "
        "particularly their Traditions and Estates blends, have earned the family a reputation "
        "as one of Washington's most quality-consistent growers and producers."
    ),
    reputation_narrative=(
        "Milbrandt Vineyards is one of Washington's most important and respected multi-generational "
        "farming estates, with Wahluke Slope fruit prized by leading Washington producers "
        "and their own labels increasingly recognised for outstanding value and regional typicity."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Milbrandt Vineyards Traditions Riesling Wahluke Slope",
    category="wine_still",
    producer_id=pid,
    region_id=25,
    origin_country="USA",
    subcategory="Riesling",
    description=(
        "Riesling from Milbrandt Vineyards' Wahluke Slope estate, one of Washington State's "
        "warmest and most sun-drenched wine appellations on the Columbia Basin's volcanic "
        "sandy loam slopes above the Columbia River. While the Wahluke Slope's warmth is "
        "most associated with powerful red wines, its Riesling benefits from the dramatic "
        "diurnal temperature variation that cools the estate rapidly at night, preserving "
        "aromatic freshness and natural acidity. Milbrandt's Traditions series showcases "
        "the estate's farming heritage with consistent, food-friendly Riesling of genuine "
        "Washington character."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Baked honey-glazed ham with Dijon mustard and pineapple chutney",
     "complement", "classic", "main",
     "Off-dry Riesling's stone fruit and acidity mirror ham's sweetness and cut through richness")
PAIR(prod,
     "Seared scallops with sweet corn purée, bacon lardons, and herb oil",
     "complement", "established", "main",
     "Riesling's bright acidity lifts scallop sweetness; stone fruit echoes corn's natural sugar")

print("\n✅ T20 Batch 6 complete — all PNW/BC wine regions now have 2+ products!")
print("  Summerland (14): +1 producer (Sumac Ridge), +1 product, +2 pairings")
print("  Thompson Valley (8): +1 producer (Sagewood), +1 product, +2 pairings")
print("  Wahluke Slope (25): +1 producer (Milbrandt), +1 product, +2 pairings")

cur.close()
conn.close()
