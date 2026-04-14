"""
T20 Batch 5: BC Canada single-product region depth
Targets: Gulf Islands (5), Lake Country (15), Lillooet (6),
         Shuswap (7), Skaha Bench (11)
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

print("=== T20 BATCH 5: BC CANADA DEPTH (5 REGIONS) ===\n")

# ── GULF ISLANDS (5) — Salt Spring Vineyards ──
print("── GULF ISLANDS — Salt Spring Vineyards ──")
pid = P(
    name="Salt Spring Vineyards",
    producer_type="winery",
    region_id=5,
    country="Canada",
    production_philosophy="Gulf Islands cool-climate estate — maritime Pinot and artisan wine on Salt Spring Island",
    philosophy_description=(
        "Salt Spring Vineyards is the Gulf Islands' most established estate winery, farming "
        "vineyards on Salt Spring Island where the Salish Sea's maritime influence creates "
        "genuinely cool growing conditions for Pinot Noir, Pinot Gris, and Ortega. The Gulf "
        "Islands' fog, ocean breezes, and rocky soils produce wines of marked elegance and "
        "restraint compared to the warmer Okanagan. Salt Spring Vineyards champions the "
        "island's unique maritime terroir and artisan production ethos."
    ),
    reputation_narrative=(
        "A pioneer of Gulf Islands viticulture, Salt Spring Vineyards demonstrates the potential "
        "of BC's maritime island terroir for cool-climate varieties, producing wines of genuine "
        "elegance that complement the island's food-artisan culture."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Salt Spring Vineyards Pinot Noir Gulf Islands",
    category="wine_still",
    producer_id=pid,
    region_id=5,
    origin_country="Canada",
    subcategory="Pinot Noir",
    description=(
        "Pinot Noir from Salt Spring Vineyards on Salt Spring Island, BC's Gulf Islands wine "
        "region. The Salish Sea surrounds the Gulf Islands, moderating temperatures and creating "
        "a distinctly maritime growing environment very different from the Okanagan Valley. "
        "The island's rocky, thin soils and sea breezes produce Pinot Noir of delicate structure "
        "and marked elegance, with the long, cool growing season preserving natural acidity "
        "and fine-grained tannins. Salt Spring Island's artisan culture aligns perfectly with "
        "the small-production, terroir-focused approach this Pinot Noir demands."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Salt Spring Island lamb chops with rosemary, garlic, and minted pea purée",
     "complement", "classic", "main",
     "Local Gulf Islands lamb and local Pinot Noir — terroir synergy; rosemary lifts red fruit")
PAIR(prod,
     "Grilled wild BC salmon with pinot reduction and pickled fennel slaw",
     "bridge", "established", "main",
     "Cool-climate maritime Pinot's delicacy matches wild Pacific salmon's gentle richness")

# ── LAKE COUNTRY (15) — Indigenous World Winery ──
print("\n── LAKE COUNTRY — Indigenous World Winery ──")
pid = P(
    name="Indigenous World Winery",
    producer_type="winery",
    region_id=15,
    country="Canada",
    production_philosophy="Syilx Nation estate — Indigenous stewardship of Lake Country terroir",
    philosophy_description=(
        "Indigenous World Winery is owned and operated by the Syilx Okanagan Nation Alliance, "
        "making it one of BC's most significant Indigenous-owned wineries. Located in the Lake "
        "Country sub-region north of Kelowna, the estate farms vineyards on territory that has "
        "been Syilx land since time immemorial, honouring traditional land stewardship while "
        "producing wines that express the distinctive Lake Country terroir. The operation "
        "represents an important intersection of Indigenous sovereignty, sustainable farming, "
        "and BC wine culture."
    ),
    reputation_narrative=(
        "Indigenous World Winery holds special significance in BC wine, representing Indigenous "
        "land sovereignty and cultural expression through viticulture, while producing genuine "
        "quality wines from Lake Country's distinctive northern Okanagan terroir."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Indigenous World Winery Lake Country Chardonnay",
    category="wine_still",
    producer_id=pid,
    region_id=15,
    origin_country="Canada",
    subcategory="Chardonnay",
    description=(
        "Chardonnay from Indigenous World Winery in the Lake Country sub-region of the Okanagan "
        "Valley, operated by the Syilx Okanagan Nation Alliance on traditional Syilx territory. "
        "Lake Country's northerly position within the Okanagan, moderated by Okanagan Lake's "
        "thermal mass, produces Chardonnay of fresh acidity and orchard fruit character distinct "
        "from the fuller, richer Chardonnay of the warmer southern Okanagan. The estate's "
        "commitment to Indigenous land stewardship and sustainable farming contributes to wines "
        "of genuine site expression and cultural significance."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Seared BC spot prawns with lemon butter, garlic, and fresh herbs",
     "complement", "classic", "main",
     "Fresh Chardonnay's acidity and orchard fruit lift spot prawns' sweetness with butter")
PAIR(prod,
     "Roasted free-range chicken with Okanagan apple and herb jus",
     "complement", "established", "main",
     "Lake Country Chardonnay's freshness mirrors apple jus while oak notes harmonise with roasting")

# ── LILLOOET (6) — Fort Berens Estate Winery (second product) ──
print("\n── LILLOOET — Fort Berens Estate (second product) ──")
# Fort Berens already exists (has the Riesling) — add a second product under them
cur.execute("SELECT id FROM beverage_producers WHERE name=%s", ("Fort Berens Estate Winery",))
row = cur.fetchone()
if row:
    fort_berens_id = row[0]
    print(f"  ~ EXISTS: Fort Berens Estate Winery (id={fort_berens_id})")
else:
    fort_berens_id = P(
        name="Fort Berens Estate Winery",
        producer_type="winery",
        region_id=6,
        country="Canada",
        production_philosophy="Lillooet pioneer — Continental BC viticulture at extreme latitude and elevation",
        philosophy_description=(
            "Fort Berens Estate Winery is Lillooet's pioneering and most significant producer, "
            "farming vineyards in one of BC's most extreme wine regions where the Fraser River "
            "Canyon creates a hot, dry Continental climate 250km north of the Okanagan. "
            "Lillooet's unique geography — arid desert conditions at 50°N latitude — produces "
            "wines of remarkable concentration and individuality."
        ),
        reputation_narrative=(
            "Fort Berens established Lillooet as a credible BC wine appellation, producing wines "
            "that express the region's unique Continental desert character and proving that "
            "viticulture is possible in BC's most unexpected locations."
        ),
        price_positioning="premium",
        authority_tier=2
    )

prod = PROD(
    name="Fort Berens Estate Cabernet Franc Lillooet",
    category="wine_still",
    producer_id=fort_berens_id,
    region_id=6,
    origin_country="Canada",
    subcategory="Cabernet Franc",
    description=(
        "Cabernet Franc from Fort Berens Estate Winery in Lillooet, BC's most northerly and "
        "climatically extreme wine region. The Fraser River Canyon creates an arid, hot "
        "Continental climate at 50°N latitude that allows Cabernet Franc to ripen fully in "
        "what appears, on paper, an impossible location for red Bordeaux varieties. The region's "
        "extreme diurnal temperature variation — hot days and cold nights in the canyon — "
        "preserves natural acidity and aromatic complexity in this unique expression of BC's "
        "frontier viticulture."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Roasted leg of lamb with wild sage, juniper berries, and rosemary potatoes",
     "complement", "classic", "main",
     "Cab Franc's violet and herbaceous lift complement lamb's juniper-sage crust perfectly")
PAIR(prod,
     "Duck pâté en croûte with Okanagan cherry compote and cornichons",
     "complement", "established", "starter",
     "Lillooet Cab Franc's dark fruit bridges duck richness while acidity cuts through pâté fat")

# ── SHUSWAP (7) — Recline Ridge (second product) ──
print("\n── SHUSWAP — Recline Ridge (second product) ──")
cur.execute("SELECT id FROM beverage_producers WHERE name=%s", ("Recline Ridge Vineyards & Winery",))
row = cur.fetchone()
if row:
    rr_id = row[0]
    print(f"  ~ EXISTS: Recline Ridge Vineyards & Winery (id={rr_id})")
else:
    rr_id = P(
        name="Recline Ridge Vineyards & Winery",
        producer_type="winery",
        region_id=7,
        country="Canada",
        production_philosophy="Shuswap pioneer — Bacchus and cool-climate aromatics in BC's Thompson-Shuswap",
        philosophy_description=(
            "Recline Ridge Vineyards is the Shuswap wine region's pioneering estate, farming "
            "vineyards in the Tappen area of the Shuswap's southern arm where the Thompson "
            "River valley creates a warm growing corridor. The estate specialises in Germanic "
            "varietals and hybrid crosses suited to the Shuswap's short growing season, "
            "producing wines of fresh acidity and aromatic charm."
        ),
        reputation_narrative=(
            "Recline Ridge established the Shuswap as a credible BC wine sub-region, demonstrating "
            "that viticulture is viable in BC's interior Thompson-Shuswap corridor."
        ),
        price_positioning="mid_range",
        authority_tier=2
    )

prod = PROD(
    name="Recline Ridge Vineyards Shuswap Pinot Gris",
    category="wine_still",
    producer_id=rr_id,
    region_id=7,
    origin_country="Canada",
    subcategory="Pinot Gris",
    description=(
        "Pinot Gris from Recline Ridge Vineyards in the Shuswap wine region of BC's Thompson-"
        "Shuswap area. One of BC's most northerly wine appellations, the Shuswap benefits from "
        "warm summer days in the Thompson River valley while cold nights preserve natural acidity "
        "in cooler-climate varieties. Recline Ridge's Pinot Gris shows the variety's characteristic "
        "pear and peach aromatics with the crisp, refreshing acidity that comes from the Shuswap's "
        "shorter, cooler growing season compared to the southern Okanagan."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Sablefish with miso-ginger glaze and bok choy",
     "complement", "classic", "main",
     "Pinot Gris' pear and acidity cut through sablefish's buttery richness; ginger echoes wine's spice")
PAIR(prod,
     "Fresh prawn spring rolls with peanut dipping sauce and mint",
     "complement", "established", "starter",
     "Off-dry orchard fruit and fresh acidity balance spring roll's richness and peanut sweetness")

# ── SKAHA BENCH (11) — Meyer Family Vineyards ──
print("\n── SKAHA BENCH — Meyer Family Vineyards ──")
pid = P(
    name="Meyer Family Vineyards",
    producer_type="winery",
    region_id=11,
    country="Canada",
    production_philosophy="Skaha Bench Chardonnay specialist — Burgundian vision from BC's most sun-drenched bench",
    philosophy_description=(
        "Meyer Family Vineyards is one of the Skaha Bench's most respected estates, producing "
        "benchmark Chardonnay and Pinot Noir from vineyards on the south-facing bench above "
        "Skaha Lake between Penticton and Okanagan Falls. The Skaha Bench receives more sun "
        "hours than almost any other Okanagan location, creating powerful, concentrated wines. "
        "Proprietor JAK Meyer studied winemaking in Burgundy and applies French-inspired precision "
        "to his BC estate, with a particular focus on single-vineyard Chardonnay that has earned "
        "national recognition."
    ),
    reputation_narrative=(
        "Meyer Family Vineyards produces some of BC's most critically acclaimed Chardonnay, "
        "demonstrating that the Skaha Bench's exceptional sun exposure and diverse soils can "
        "produce whites of Burgundian depth and complexity."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Meyer Family Vineyards Skaha Bench Chardonnay",
    category="wine_still",
    producer_id=pid,
    region_id=11,
    origin_country="Canada",
    subcategory="Chardonnay",
    description=(
        "Chardonnay from Meyer Family Vineyards on the Skaha Bench, the sun-drenched south-facing "
        "bench above Skaha Lake in the southern Okanagan Valley between Penticton and Okanagan "
        "Falls. Proprietor JAK Meyer's Burgundian training informs a precise, terroir-focused "
        "approach that maximises the Skaha Bench's exceptional sun exposure and diverse glacial "
        "soils. The resulting Chardonnay shows the warmth and concentration of the Bench's "
        "intense sunshine balanced by the natural acidity preserved through careful canopy "
        "management and cool-night temperature swings above Skaha Lake."
    ),
    price_tier="premium"
)
PAIR(prod,
     "BC Dungeness crab Benedict with hollandaise and chive on brioche",
     "complement", "classic", "main",
     "Burgundian-trained Chardonnay's richness and acidity balance hollandaise and fresh crab")
PAIR(prod,
     "Roasted BC spot prawn bisque with crème fraîche and fresh tarragon",
     "complement", "established", "starter",
     "Skaha Bench Chardonnay's weight and oak complement bisque's cream while acidity lifts tarragon")

print("\n✅ T20 Batch 5 complete.")
print("  Gulf Islands (5): +1 producer (Salt Spring Vineyards), +1 product, +2 pairings")
print("  Lake Country (15): +1 producer (Indigenous World Winery), +1 product, +2 pairings")
print("  Lillooet (6): +1 product (Fort Berens Cab Franc), +2 pairings")
print("  Shuswap (7): +1 product (Recline Ridge Pinot Gris), +2 pairings")
print("  Skaha Bench (11): +1 producer (Meyer Family Vineyards), +1 product, +2 pairings")

cur.close()
conn.close()
