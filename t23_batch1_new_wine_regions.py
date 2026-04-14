"""
T23 Batch 1: New wine regions — important global additions
Targets: Mornington Peninsula (AU), Niagara Peninsula (CA), Bierzo DO (ES),
         Cahors AOC (FR), Alto Adige DOC (IT)
"""
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

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""
        INSERT INTO beverage_vintages (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (region_id, year, quality_descriptor, price_trajectory, season_narrative))
    print(f"    ✓ Vintage {year}: {quality_descriptor}")

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

print("=== T23 BATCH 1: NEW WINE REGIONS (5 REGIONS) ===\n")

# ── MORNINGTON PENINSULA (Australia) ──
print("── MORNINGTON PENINSULA — Australia ──")
rid = R(
    name="Mornington Peninsula",
    country="Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Mornington Peninsula GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "The Mornington Peninsula is Victoria's premier cool-climate wine region, situated "
        "on a narrow peninsula 60km south of Melbourne between Port Phillip Bay and Western "
        "Port Bay. The maritime influence from two bodies of water creates a uniquely cool, "
        "temperate growing environment ideal for Pinot Noir and Chardonnay. The region's "
        "diverse soils — from red volcanic to sandy loam to terra rossa — combined with "
        "elevation variations from sea level to 200m produce wines of extraordinary site "
        "specificity. Pinot Noir and Chardonnay are the benchmark varieties, with the "
        "region home to some of Australia's most celebrated small-production estate wines."
    ),
    key_producers="Kooyong Estate, Port Phillip Estate, Stonier Wines, Paringa Estate, Main Ridge Estate, Ten Minutes by Tractor",
    historical_context=(
        "Commercial viticulture on the Mornington Peninsula began in the 1970s, with "
        "pioneers like Nat White at Main Ridge Estate establishing the region's potential "
        "for serious Pinot Noir and Chardonnay. The 1990s saw rapid expansion, and today "
        "the peninsula is recognised as Australia's most serious cool-climate wine region "
        "for Burgundian varieties, with over 50 estate wineries."
    )
)
for yr, q, t in [
    (2019, "exceptional", "rising"),
    (2020, "excellent", "stable"),
    (2021, "excellent", "rising"),
    (2022, "very_good", "stable"),
    (2023, "excellent", "rising"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Kooyong Estate",
    producer_type="winery",
    region_id=rid,
    country="Australia",
    production_philosophy="Mornington Peninsula's finest — Kooyong's single-vineyard Burgundian expression",
    philosophy_description=(
        "Kooyong Estate is widely considered the Mornington Peninsula's benchmark producer, "
        "farming 27ha of estate vineyards on deep red volcanic soils above the bay at Merricks "
        "North. Winemaker Glen Hayley produces a suite of single-vineyard Pinot Noirs and "
        "Chardonnays that showcase the Peninsula's extraordinary site diversity. Kooyong's "
        "approach — minimal intervention, whole-bunch components, indigenous fermentation — "
        "produces wines that rival Australia's finest Pinot Noir and Chardonnay and stand "
        "comparison with premier Burgundy."
    ),
    reputation_narrative=(
        "Kooyong Estate has established the Mornington Peninsula as a serious Pinot Noir "
        "region of international significance, with their single-vineyard range consistently "
        "among Australia's most sought-after cool-climate wines."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)
prod1 = PROD(
    name="Kooyong Estate Pinot Noir Mornington Peninsula",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Australia",
    subcategory="Pinot Noir",
    description=(
        "Estate Pinot Noir from Kooyong Estate on the Mornington Peninsula, produced from "
        "deep red volcanic soils at Merricks North. The Peninsula's maritime cooling from "
        "two bodies of water creates a long, cool growing season ideal for Pinot Noir of "
        "extraordinary aromatic intensity and structural elegance. Kooyong's estate wine "
        "demonstrates the variety's potential in Victoria's most serious cool-climate region, "
        "with a Burgundian approach of whole-cluster fermentation, indigenous yeast, and "
        "minimal intervention in the cellar."
    ),
    price_tier="ultra_premium"
)
PAIR(prod1, "Roasted duck breast with cherry gastrique and sautéed shiitake mushrooms",
     "complement", "classic", "main",
     "Mornington Pinot's cherry and earthy character create harmony with duck and forest mushrooms")
PAIR(prod1, "Pan-seared quail with pomegranate molasses, wilted radicchio, and walnuts",
     "complement", "established", "main",
     "Cool-climate Pinot's delicacy and bright acidity lift quail's lightness and radicchio's bitterness")

pid2 = P(
    name="Paringa Estate",
    producer_type="winery",
    region_id=rid,
    country="Australia",
    production_philosophy="Self-taught genius of the Peninsula — Paringa's powerful Pinot and Shiraz",
    philosophy_description=(
        "Paringa Estate is one of the Mornington Peninsula's most celebrated producers, "
        "founded by schoolteacher Lindsay McCall who taught himself winemaking through "
        "obsessive attention to viticulture and cellar practice. Paringa produces both "
        "Pinot Noir and Shiraz from the Peninsula's cool maritime climate, achieving a "
        "unique combination of concentration and elegance. The estate's Peninsula Pinot Noir "
        "and The Paringa single-vineyard are among Australia's most awarded wines."
    ),
    reputation_narrative=(
        "Lindsay McCall's self-taught journey to becoming one of Australia's most awarded "
        "winemakers is a Peninsula legend. Paringa Estate's wines combine the thoughtfulness "
        "of a teacher with the obsession of a craftsman, producing benchmark Peninsula Pinot."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Paringa Estate Peninsula Shiraz Mornington Peninsula",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Australia",
    subcategory="Shiraz",
    description=(
        "Cool-climate Shiraz from Paringa Estate on the Mornington Peninsula, one of "
        "Australia's most unusual expressions of this variety. The Peninsula's maritime "
        "cooling produces Shiraz of far greater elegance and aromatics than the warmer "
        "Barossa or McLaren Vale, with characteristics closer to a Northern Rhône Syrah "
        "— pepper, olive, violet, and restrained fruit — than the generous, opulent style "
        "of warmer Australian regions. A revelation for those who know only warm-climate "
        "Australian Shiraz."
    ),
    price_tier="premium"
)
PAIR(prod2, "Slow-braised short ribs with olives, capers, and rosemary gremolata",
     "complement", "established", "main",
     "Cool-climate Shiraz's olive and pepper character mirrors Mediterranean braising flavours")
PAIR(prod2, "Wood-fired lamb ribs with preserved lemon and mint yoghurt",
     "complement", "classic", "main",
     "Mornington Shiraz's pepper and violet lift lamb's smoky char and mint-acid contrast")

# ── NIAGARA PENINSULA (Canada) ──
print("\n── NIAGARA PENINSULA — Canada ──")
rid = R(
    name="Niagara Peninsula",
    country="Canada",
    beverage_family="wine",
    designation_type="VQA",
    designation_name="Niagara Peninsula VQA",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "The Niagara Peninsula is Ontario's most important wine region and Canada's second "
        "most significant after BC's Okanagan Valley, situated between Lake Ontario to the "
        "north and Lake Erie to the south. The twin lakes' thermal moderating influence and "
        "the Niagara Escarpment's slope and drainage create a unique microclimate that allows "
        "vinifera cultivation at this northern latitude. The region is particularly celebrated "
        "for its Icewine — benefiting from reliably cold winters — alongside serious Riesling, "
        "Pinot Noir, Chardonnay, and Cabernet Franc. The Niagara Escarpment and Twenty Mile "
        "Bench sub-appellations are the most prestigious sites."
    ),
    key_producers="Inniskillin, Cave Spring Cellars, Château des Charmes, Henry of Pelham, Tawse Winery, Norman Hardie",
    historical_context=(
        "Ontario viticulture dates to the early 19th century, but the modern era began with "
        "the 1988 Canada-US Free Trade Agreement that forced Ontario's wine industry to "
        "modernise from hybrid to vinifera grape cultivation. The Vintners Quality Alliance "
        "(VQA) system, established in 1988, created quality standards that transformed "
        "Niagara into a respected international wine region. Inniskillin's 1991 Vidal Icewine "
        "winning the Grand Prix d'Honneur at Vinexpo brought global attention to Canadian wine."
    )
)
for yr, q, t in [
    (2019, "excellent", "stable"),
    (2020, "very_good", "stable"),
    (2021, "excellent", "rising"),
    (2022, "very_good", "stable"),
    (2023, "excellent", "rising"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Tawse Winery",
    producer_type="winery",
    region_id=rid,
    country="Canada",
    production_philosophy="Niagara's biodynamic benchmark — Tawse's certified organic terroir expression",
    philosophy_description=(
        "Tawse Winery is the Niagara Peninsula's most critically acclaimed estate, farming "
        "certified biodynamic vineyards across four estate properties including Cherry Avenue "
        "in Vinemount Ridge and Growers Blend sites on the Beamsville Bench. Moray Tawse's "
        "investment in quality viticulture and winemaker Paul Pender's Burgundian approach "
        "have produced Ontario's most celebrated Chardonnay and Pinot Noir. Tawse is the "
        "only Canadian winery to win Canadian Winery of the Year four consecutive times."
    ),
    reputation_narrative=(
        "Tawse Winery has established Ontario's capacity for world-class Chardonnay and Pinot "
        "Noir, with their biodynamic estate wines consistently rated among Canada's finest "
        "and attracting international critical attention."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)
prod1 = PROD(
    name="Tawse Winery Quarry Road Vineyard Chardonnay Niagara Peninsula",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Canada",
    subcategory="Chardonnay",
    description=(
        "Single-vineyard Chardonnay from Tawse Winery's Quarry Road Vineyard on the "
        "Beamsville Bench in the Niagara Peninsula. The Beamsville Bench's loam-over-clay "
        "soils and Lake Ontario's moderating influence create conditions ideal for Chardonnay "
        "of genuine complexity and mineral expression. Tawse's biodynamic farming and "
        "Burgundian winemaking — whole-cluster pressing, barrel fermentation, extended lees "
        "aging — produce Ontario's most ambitious Chardonnay, showing that Canada can produce "
        "world-class white Burgundy-style wine."
    ),
    price_tier="ultra_premium"
)
PAIR(prod1, "Seared Lake Erie pickerel with lemon beurre blanc and asparagus",
     "complement", "classic", "main",
     "Ontario Chardonnay and local Lake Erie fish — regional terroir synergy with Burgundian style")
PAIR(prod1, "Roasted BC spot prawns with Niagara peach gastrique and fresh tarragon",
     "complement", "established", "main",
     "Tawse Chardonnay's peach and mineral notes mirror Niagara peach gastrique's fruit precision")

pid2 = P(
    name="Cave Spring Cellars",
    producer_type="winery",
    region_id=rid,
    country="Canada",
    production_philosophy="Beamsville Bench pioneers — Niagara Riesling's definitive estate since 1986",
    philosophy_description=(
        "Cave Spring Cellars is one of the Niagara Peninsula's founding estate wineries, "
        "established in 1986 on the Beamsville Bench by the Pennachetti family. Cave Spring "
        "is Canada's most respected Riesling producer, producing a range of styles from dry "
        "CSV (Cave Spring Vineyard) Riesling to exceptional Icewines that have won "
        "international recognition. Their commitment to the Beamsville Bench's distinctive "
        "clay-loam soils and the Escarpment's moderating influence has defined what serious "
        "Niagara Riesling can achieve."
    ),
    reputation_narrative=(
        "Cave Spring Cellars' Riesling programme is considered Canada's finest, with the CSV "
        "single-vineyard expression consistently ranked among North America's most serious "
        "dry Rieslings and demonstrating the Niagara Peninsula's exceptional potential for "
        "this noble variety."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Cave Spring CSV Riesling Niagara Peninsula",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Canada",
    subcategory="Riesling",
    description=(
        "The flagship CSV (Cave Spring Vineyard) Riesling from Cave Spring Cellars on the "
        "Beamsville Bench, produced from their single estate vineyard farmed since 1986. "
        "The Beamsville Bench's clay-loam soils over dolomitic limestone, combined with "
        "the Lake Ontario temperature moderation, produce Riesling of extraordinary purity "
        "and mineral precision. Cave Spring's CSV Riesling is dry-finished with the natural "
        "acidity preserved through careful harvest timing and cool fermentation, producing "
        "a wine of remarkable age-worthiness and complexity."
    ),
    price_tier="premium"
)
PAIR(prod2, "Ontario pickerel en papillote with dill, lemon, and capers",
     "complement", "classic", "main",
     "Niagara Riesling's precision and citrus acidity create natural harmony with freshwater fish")
PAIR(prod2, "Pork tenderloin with Niagara peach chutney and rosemary reduction",
     "complement", "established", "main",
     "Cave Spring Riesling's stone fruit character bridges pork's sweetness and Niagara peach")

# ── BIERZO DO (Spain) ──
print("\n── BIERZO DO — Spain ──")
rid = R(
    name="Bierzo DO",
    country="Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Bierzo DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "Bierzo is a mountainous wine region in northwest Spain's León province, situated at "
        "the transition between the Atlantic coast and the Castilian meseta. The region's "
        "distinctive Mencía grape, grown on steep slate and clay slopes along the Sil River "
        "tributaries, produces wines of remarkable elegance and aromatic complexity — more "
        "Burgundy-influenced than typical Spanish reds. The Mencia variety's combination of "
        "bright acidity, fine tannins, and floral, mineral character creates a style quite "
        "unlike any other Spanish red. The Corullón and Quilos sub-zones are particularly "
        "celebrated for old-vine Mencía of extraordinary finesse."
    ),
    key_producers="Descendientes de J. Palacios, Dominio de Tares, Pittacum, Paixar, Pérez Caramés",
    historical_context=(
        "Bierzo was awarded DO status in 1989, but its international reputation was largely "
        "created by Álvaro Palacios and his nephew Ricardo Pérez Palacios, who arrived in 1999 "
        "and identified the region's exceptional old-vine Mencía potential. Their Corullón and "
        "Las Lamas bottlings placed Bierzo on the world wine map and triggered a quality "
        "revolution that continues today."
    )
)
for yr, q, t in [
    (2019, "excellent", "rising"),
    (2020, "very_good", "stable"),
    (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"),
    (2023, "excellent", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Descendientes de J. Palacios",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Bierzo's revolution — Álvaro Palacios and Ricardo Pérez discovering Mencía's greatness",
    philosophy_description=(
        "Descendientes de J. Palacios is the estate that put Bierzo on the international wine "
        "map. Founded by Álvaro Palacios (of Priorat fame) and his nephew Ricardo Pérez Palacios "
        "in 1999, the estate identified and restored old-vine Mencía vineyards on the slate "
        "slopes above Corullón and the Sil River tributaries. Their Pétalos del Bierzo offers "
        "accessible elegance while the single-vineyard Corullón, Las Lamas, and La Faraona "
        "bottlings are among Spain's most sought-after wines, demonstrating that Mencía can "
        "achieve Pinot Noir-like finesse when grown on the right slate terroir."
    ),
    reputation_narrative=(
        "Descendientes de J. Palacios transformed Bierzo's reputation and created one of Spain's "
        "most exciting quality wine regions. Their wines have become benchmarks for Mencía's "
        "potential and among Spain's most critically acclaimed and expensive bottles."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod1 = PROD(
    name="Descendientes de J. Palacios Pétalos del Bierzo Mencía",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Spain",
    subcategory="Mencía",
    description=(
        "The entry-level but brilliant Pétalos del Bierzo from Descendientes de J. Palacios, "
        "produced from Mencía vines across multiple Bierzo parcels on slate and clay soils. "
        "The Pétalos — meaning 'petals' — captures Bierzo Mencía's distinctive floral, "
        "mineral character: violet and wild strawberry aromatics, light to medium body, "
        "refreshing acidity, and the distinctive mineral-slate quality that makes Bierzo "
        "so different from other Spanish reds. The most accessible expression of the "
        "Palacios-Pérez Palacios Bierzo vision."
    ),
    price_tier="premium"
)
PAIR(prod1, "Roasted Iberian pork cheeks with Piquillos peppers and potato gratin",
     "complement", "classic", "main",
     "Bierzo Mencía's mineral freshness and light tannins cut through Iberian pork's richness")
PAIR(prod1, "Grilled octopus (pulpo a la gallega) with paprika oil and sea salt",
     "complement", "established", "main",
     "Mencía's violet-mineral character and acidity elevate Galician octopus preparation beautifully")

pid2 = P(
    name="Dominio de Tares",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Bierzo's consistent quality benchmark — Tares' old-vine Mencía across the appellation",
    philosophy_description=(
        "Dominio de Tares is one of Bierzo's most important and consistent producers, working "
        "with old-vine Mencía across the appellation's diverse terroirs to produce wines of "
        "genuine quality and regional typicity. The estate's commitment to preserving old-vine "
        "heritage — some vines over 80 years old on slate and clay soils — and their precise "
        "winemaking have made them a reliable reference for authentic Bierzo character."
    ),
    reputation_narrative=(
        "Dominio de Tares is an essential reference for Bierzo's quality potential beyond "
        "the Palacios wines, demonstrating that the region's quality revolution extends across "
        "multiple committed producers working the appellation's exceptional terroir."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Dominio de Tares Bembibre Mencía Bierzo DO",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Spain",
    subcategory="Mencía",
    description=(
        "Reserve Mencía from Dominio de Tares' Bembibre single-vineyard selection in the "
        "Bierzo DO, sourced from old-vine plots on slate soils in the Sil River valley. "
        "The Bembibre shows Bierzo Mencía at its most concentrated and structured — "
        "darker fruit, more tannic grip, and deeper mineral complexity than the fresher "
        "village expressions — while maintaining the variety's characteristic floral "
        "lift and bright acidity. Aged in French oak for 12 months, the wine integrates "
        "wood beautifully into a structured, age-worthy expression."
    ),
    price_tier="premium"
)
PAIR(prod2, "Slow-roasted suckling pig (cochinillo) with crackling and Castilian bread",
     "complement", "classic", "main",
     "Bierzo Mencía's freshness and mineral acidity cut through cochinillo's rich fat perfectly")
PAIR(prod2, "Cecina de León (cured beef) with Manchego and pickled piquillo peppers",
     "complement", "established", "starter",
     "Mencía's violet and earth notes elevate the complex flavours of León's cured beef tradition")

# ── CAHORS AOC (France) ──
print("\n── CAHORS AOC — France ──")
rid = R(
    name="Cahors AOC",
    country="France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Cahors AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description=(
        "Cahors is the Lot Valley's historic wine appellation in southwest France, long known "
        "as the 'Black Wine of Cahors' for its intense, tannic Malbec (locally called Côt "
        "or Auxerrois). The appellation requires minimum 70% Malbec (Côt) with Merlot and "
        "Tannat permitted as blending partners. The Lot Valley's causses (limestone plateaus) "
        "and valley terraces provide diverse soil types that produce Malbec wines of greater "
        "structure and austerity than the Argentinian versions — more mineral, more tannic, "
        "and requiring longer aging. The appellation experienced a quality renaissance in "
        "the 1990s and 2000s as producers moved away from rough, harsh wines to polished, "
        "terroir-expressive Malbec."
    ),
    key_producers="Château Lagrezette, Château du Cèdre, Clos Triguedina, Château Lamartine, Clos la Coutale",
    historical_context=(
        "Cahors was once France's most important red wine appellation, trading its 'Black Wine' "
        "across Europe in the Middle Ages and being specified in papal and royal courts. Phylloxera "
        "devastated the vineyards in the 1870s-80s, and the appellation's reconstruction was "
        "slow and uneven. The 1999 appellation restructuring and investment by producers like "
        "Alain Dominique Perrin at Lagrezette began the quality revolution that positioned "
        "Cahors Malbec alongside Argentine Malbec internationally."
    )
)
for yr, q, t in [
    (2018, "excellent", "rising"),
    (2019, "exceptional", "rising"),
    (2020, "excellent", "stable"),
    (2021, "very_good", "stable"),
    (2022, "excellent", "rising"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Château du Cèdre",
    producer_type="winery",
    region_id=rid,
    country="France",
    production_philosophy="Cahors quality leader — Verhaeghe brothers' biodynamic Malbec of genuine distinction",
    philosophy_description=(
        "Château du Cèdre is widely considered Cahors' quality benchmark estate, farmed "
        "biodynamically by Pascal and Jean-Marc Verhaeghe on the first terrace above the Lot "
        "River. The estate's commitment to old-vine Malbec (Côt) — including century-old vines "
        "in their Cèdre Heritage cuvée — and biodynamic viticulture produces wines of "
        "extraordinary concentration and age-worthiness. The Verhaeghe brothers' meticulous "
        "approach to the chalky clay terroir of their first-terrace sites has established "
        "Château du Cèdre as Cahors' definitive address for serious collectors."
    ),
    reputation_narrative=(
        "Château du Cèdre is the standard-bearer for modern Cahors quality, demonstrating that "
        "Lot Valley Malbec can achieve genuine distinction and age-worthiness rivalling the best "
        "Bordeaux at a fraction of the price."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod1 = PROD(
    name="Château du Cèdre Le Cèdre Malbec Cahors AOC",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="France",
    subcategory="Malbec",
    description=(
        "The flagship Le Cèdre from Château du Cèdre, produced from old-vine Malbec (Côt) "
        "on the first terrace of chalky clay above the Lot River in Cahors. The Le Cèdre "
        "represents the estate's finest expression of Cahors terroir — deeply coloured, "
        "concentrated, and structured with the mineral austerity and dark fruit intensity "
        "characteristic of Lot Valley Malbec at its best. Unlike Argentine Malbec, Cahors "
        "Malbec shows greater tannic structure, mineral tension, and austere complexity that "
        "requires significant cellaring — 8–15 years for the Le Cèdre — to fully integrate."
    ),
    price_tier="premium"
)
PAIR(prod1, "Magret de canard (duck breast) with Périgueux sauce and foie gras",
     "complement", "classic", "main",
     "Cahors' defining pairing — local duck and Black Wine of Cahors create the perfect southwest French match")
PAIR(prod1, "Cassoulet with Toulouse sausage, duck confit, and white beans",
     "complement", "established", "main",
     "Tannic Cahors Malbec and the hearty cassoulet of southwest France — terroir and cultural synergy")

pid2 = P(
    name="Clos Triguedina",
    producer_type="winery",
    region_id=rid,
    country="France",
    production_philosophy="Cahors heritage estate — Baldès family's five centuries of Lot Valley Malbec",
    philosophy_description=(
        "Clos Triguedina is one of Cahors' oldest and most historically significant estates, "
        "farmed by the Baldès family for five generations. The estate's Probus cuvée — named "
        "for the Roman Emperor who permitted Gallic viticulture — is made exclusively from "
        "a single hectare of Malbec vines planted in 1963, producing one of Cahors' most "
        "concentrated and age-worthy expressions. The estate's respect for tradition and "
        "long aging protocols represent the authentic Cahors style."
    ),
    reputation_narrative=(
        "Clos Triguedina represents Cahors' living history, with the Baldès family's five "
        "generations of unbroken viticulture connecting the appellation's medieval past to "
        "its contemporary quality renaissance."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Clos Triguedina Cahors AOC Malbec",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="France",
    subcategory="Malbec",
    description=(
        "Estate Malbec (Côt) from Clos Triguedina, one of Cahors' most historic estates "
        "farmed by the Baldès family for five generations in the Lot Valley. The Cahors "
        "style of Malbec is distinctly different from Argentine interpretations — more "
        "mineral, more austere, with the limestone-clay terroir of the causses above the "
        "Lot River imparting a dark, earthy character and firm tannin structure. "
        "Traditional Cahors winemaking — extended maceration, aging in large oak foudres — "
        "produces wine designed for long cellaring and gradual evolution."
    ),
    price_tier="premium"
)
PAIR(prod2, "Confit de canard with Sarladaise potatoes and truffle salad",
     "complement", "classic", "main",
     "Lot Valley Malbec and Périgord duck confit — the emblematic southwest French pairing")
PAIR(prod2, "Rack of lamb with flageolet beans, herbs de Quercy, and garlic confit",
     "complement", "established", "main",
     "Cahors Malbec's structure and dark mineral fruit complement Quercy lamb's aromatic herbs")

# ── ALTO ADIGE DOC (Italy) ──
print("\n── ALTO ADIGE DOC — Italy ──")
rid = R(
    name="Alto Adige DOC",
    country="Italy",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Alto Adige DOC / Südtirol DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "Alto Adige (Südtirol in German) is Italy's northernmost wine region, a narrow Alpine "
        "valley bordered by Austria to the north and the Dolomite mountains to the east and west. "
        "The region's unique bilingual culture (both German and Italian are official languages) "
        "reflects its position as a meeting point of Alpine and Mediterranean influences. "
        "Alto Adige produces some of Italy's finest white wines — particularly Pinot Grigio, "
        "Pinot Bianco, Gewürztraminer, and Riesling — from steep alpine vineyards at 200–1,000m "
        "elevation. The dramatic diurnal temperature variation and volcanic porphyry soils create "
        "wines of extraordinary freshness, aromatic precision, and mineral complexity."
    ),
    key_producers="Elena Walch, Alois Lageder, Cantina Terlano, J. Hofstätter, Tiefenbrunner, Tramin",
    historical_context=(
        "Alto Adige's winemaking heritage dates to the Romans, but the region's modern wine "
        "identity was shaped by its Habsburg Austrian history — the region was only ceded to "
        "Italy after WWI in 1919. The Austrian influence remains strong in both culture and "
        "winemaking, with a focus on precision, freshness, and aromatic intensity that contrasts "
        "with the richer styles of southern Italy. The cooperative movement — particularly "
        "Cantina Terlano — has been central to maintaining quality standards across the region."
    )
)
for yr, q, t in [
    (2019, "excellent", "stable"),
    (2020, "exceptional", "rising"),
    (2021, "excellent", "rising"),
    (2022, "excellent", "stable"),
    (2023, "very_good", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Cantina Terlano",
    producer_type="winery",
    region_id=rid,
    country="Italy",
    production_philosophy="Alto Adige's collective benchmark — Terlano's half-century-aged Pinot Bianco and Sauvignon",
    philosophy_description=(
        "Cantina Terlano is arguably Italy's most prestigious wine cooperative and one of the "
        "world's most extraordinary wine institutions, holding a reserve wine collection dating "
        "back to 1955 that is released at 30–60 years of age. The cooperative's Rarity releases "
        "— particularly Pinot Bianco and Sauvignon Blanc — demonstrate that Alto Adige whites "
        "can age for decades and develop complexity rivalling the world's greatest wines. "
        "Terlano's wines consistently rank among Italy's finest whites, with their Terlaner I "
        "and Nova Domus Reserva among the most sought-after Italian whites produced."
    ),
    reputation_narrative=(
        "Cantina Terlano's Rarity reserve releases have stunned wine critics worldwide, "
        "demonstrating that Alto Adige's Pinot Bianco can develop extraordinary complexity "
        "over 50+ years of bottle aging. The cooperative's standards represent the pinnacle "
        "of Italian cooperative winemaking."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod1 = PROD(
    name="Cantina Terlano Terlaner I Bianco DOC Alto Adige",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Italy",
    subcategory="White Blend",
    description=(
        "Cantina Terlano's flagship white blend — Terlaner I — combining Pinot Bianco, "
        "Chardonnay, and Sauvignon Blanc from the cooperative's best Alto Adige vineyard "
        "parcels. The blend showcases the synergy of Alto Adige's great white varieties, "
        "with Pinot Bianco providing mineral structure, Chardonnay adding texture and "
        "depth, and Sauvignon contributing aromatic precision and freshness. Terlano's "
        "meticulous vinification — gentle pressing, temperature-controlled fermentation, "
        "aging on fine lees — produces a white of extraordinary complexity and longevity "
        "that improves with 10–15 years of cellaring."
    ),
    price_tier="ultra_premium"
)
PAIR(prod1, "White asparagus with hollandaise, prosciutto crudo, and shaved truffle",
     "complement", "classic", "main",
     "Alto Adige's alpine whites with local white asparagus season — the definitive Südtirol pairing")
PAIR(prod1, "Salt-baked mountain trout with fennel, lemon, and herbs",
     "complement", "established", "main",
     "Terlaner's mineral precision and alpine freshness create harmony with mountain trout's delicacy")

pid2 = P(
    name="Elena Walch",
    producer_type="winery",
    region_id=rid,
    country="Italy",
    production_philosophy="Alto Adige's estate pioneer — Elena Walch's Gewürztraminer and Pinot Grigio mastery",
    philosophy_description=(
        "Elena Walch is one of Alto Adige's most respected and distinctive estate wineries, "
        "producing single-vineyard wines from two estate sites — Kastelaz in Tramin and "
        "Castel Ringberg above Caldaro Lake. Elena Walch's Gewürztraminer from the Kastelaz "
        "site (the Tramin commune gave Gewürztraminer its name) is considered Italy's finest "
        "expression of this aromatic variety. Her Pinot Grigio, Pinot Bianco, and Lagrein "
        "demonstrate the full range of Alto Adige's terroir diversity."
    ),
    reputation_narrative=(
        "Elena Walch's Kastelaz Gewürztraminer is one of Italy's most celebrated white wines, "
        "demonstrating that the variety's birthplace (Tramin/Termeno) can produce the world's "
        "finest expression of this uniquely aromatic variety."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)
prod2 = PROD(
    name="Elena Walch Kastelaz Gewürztraminer Alto Adige DOC",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Italy",
    subcategory="Gewürztraminer",
    description=(
        "Single-vineyard Gewürztraminer from Elena Walch's Kastelaz estate in Tramin "
        "(Termeno), the village that gave Gewürztraminer its name. The Kastelaz site's "
        "unique volcanic porphyry soils and south-facing alpine exposure produce Gewürztraminer "
        "of extraordinary aromatic intensity and mineral complexity. While Alsatian and German "
        "versions are better known, the Kastelaz represents the variety in its ancestral home — "
        "lychee, rose petal, ginger, and white pepper with a savoury, almost smoky mineral "
        "finish quite different from richer international interpretations."
    ),
    price_tier="ultra_premium"
)
PAIR(prod2, "Pan-seared foie gras with quince compote and brioche toast",
     "complement", "classic", "starter",
     "Gewürztraminer's lychee and rose are the classic foie gras pairing; mineral finish balances fat")
PAIR(prod2, "Thai green curry with galangal, lemongrass, kaffir lime, and jasmine rice",
     "contrast", "established", "main",
     "Gewürztraminer's aromatic intensity and residual sweetness tame Thai curry's complex heat")

print("\n✅ T23 Batch 1 complete.")
print("  Mornington Peninsula: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Niagara Peninsula: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Bierzo DO: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Cahors AOC: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Alto Adige DOC: +2 producers, +2 products, +4 pairings, +5 vintages")

cur.close()
conn.close()
