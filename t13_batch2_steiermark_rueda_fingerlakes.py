#!/usr/bin/env python3
"""Terminal 13 — Batch 2: Steiermark + Rueda DO + Finger Lakes (new regions, full coverage)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, description, key_producers,
      designation_type=None, designation_name=None, reputation_tier="prestigious",
      quality_trajectory="established", historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS region: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, description, key_producers,
           designation_type, designation_name, reputation_tier, quality_trajectory,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, description,
          json.dumps(key_producers) if isinstance(key_producers, list) else key_producers,
          designation_type, designation_name, reputation_tier, quality_trajectory,
          historical_context))
    rid = cur.fetchone()[0]
    print(f"  ✓ NEW region: {name} (id={rid})")
    return rid

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
    print(f"  ✓ NEW producer: {name} (id={pid})")
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
    print(f"  ✓ NEW product: {name} (id={pid})")
    return pid

def V(region_id, year, rating, descriptor, narrative, price_traj="stable", window_from=None, window_to=None):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory,
           drinking_window, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,1)
        ON CONFLICT (region_id, vintage_year) DO NOTHING
    """, (region_id, year, rating, descriptor, narrative, price_traj,
          json.dumps({"from": window_from, "to": window_to}) if window_from else None))
    action = "✓" if cur.rowcount else "~"
    print(f"  {action} {year} → region {region_id}: {descriptor} ({rating})")

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ─── STEIERMARK (STYRIA) ──────────────────────────────────────────────────────
print("=== STEIERMARK (STYRIA) ===")

STEIERMARK = R(
    name="Steiermark DAC",
    country="Austria",
    beverage_family="wine",
    description=(
        "Austria's southernmost wine region and home to some of the world's finest Sauvignon Blanc — "
        "the Styrian Sauvignon Blanc from Südsteiermark (South Styria) is widely regarded as the "
        "benchmark of the variety outside of Sancerre and Pouilly-Fumé. The steep slate, schist, and "
        "volcanic Opok soil terroirs of Südsteiermark's Sausal and Gamlitzer subzones produce wines "
        "of extraordinary mineral precision, vibrant acidity, and tropical-citrus aromatics with a "
        "distinctive mineral intensity. Welschriesling, Chardonnay (locally called Morillon), and "
        "Gelber Muskateller are additional key varieties. Steiermark DAC established in 2018 "
        "formalises the appellation's precision and diversity. The wines are among Austria's most "
        "internationally sought-after and are prized on fine dining wine lists worldwide."
    ),
    key_producers=["Tement", "Polz", "Gross", "Neumeister", "Lackner-Tinnacher"],
    designation_type="DAC",
    designation_name="Steiermark DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    historical_context=(
        "Styria has been a wine region since Roman times — the region's steep terraced vineyards are "
        "among the most dramatic in central Europe. Erich Tement's pioneering work in the 1990s "
        "established Südsteiermark Sauvignon Blanc as a world-class category alongside Sancerre. "
        "The region was instrumental in transforming Austria's fine wine image after the 1985 crisis."
    )
)

print("\n--- Steiermark Producers ---")
TEMENT = P(
    "Weingut Tement", "winery", STEIERMARK, "Austria",
    production_philosophy="Terroir-driven Sauvignon Blanc from Opok and Muschelkalk, Südsteiermark",
    philosophy_description=(
        "Erich and Armin Tement are the family most responsible for establishing Südsteiermark "
        "Sauvignon Blanc as a world-class wine category. The estate's benchmark Zieregg vineyard "
        "— a steep south-facing Opok slope — produces the reference expression of Styrian Sauvignon: "
        "mineral, laser-focused, with citrus zest, white grapefruit, elderflower, and a stony "
        "precision that ages magnificently for 10+ years. Tement farms organically and is the "
        "most prestigious producer in the appellation."
    ),
    reputation_narrative=(
        "Weingut Tement is the most prestigious producer in Steiermark and the defining name for "
        "Styrian Sauvignon Blanc internationally. Zieregg appears on the world's top restaurant wine lists."
    ),
    price_positioning="ultra_premium"
)

POLZ = P(
    "Polz Winery", "winery", STEIERMARK, "Austria",
    production_philosophy="Estate Sauvignon Blanc and Welschriesling from Gamlitz, Südsteiermark",
    philosophy_description=(
        "Erich and Walter Polz are among the most important producers in Gamlitz, producing "
        "benchmark Sauvignon Blanc and Welschriesling from their steep Opok-soil vineyards. "
        "The Polz estate Sauvignon shows the characteristic Styrian profile: vibrant tropical "
        "fruit, elderflower, and stony precision. The Hochgrassnitzberg single-vineyard is the "
        "estate's flagship — a wine of extraordinary mineral depth and aging capacity."
    ),
    reputation_narrative=(
        "Polz is among Südsteiermark's most acclaimed producers, with wines on leading Austrian "
        "and international fine dining lists. A benchmark for the Gamlitz subzone."
    ),
    price_positioning="premium"
)

GROSS = P(
    "Weingut Gross", "winery", STEIERMARK, "Austria",
    production_philosophy="Sauvignon Blanc and Morillon (Chardonnay) from Ratsch and Eckberg",
    philosophy_description=(
        "The Gross family in Ratsch an der Weinstraße produce some of Südsteiermark's most "
        "refined Sauvignon Blanc and Morillon (Chardonnay). The estate's Nussberg single-vineyard "
        "Sauvignon is a wine of extraordinary precision and citrus-mineral focus. Gross also "
        "produces one of the appellation's finest Morillon — a barrel-fermented Chardonnay that "
        "demonstrates the variety's capacity for complexity in Styrian soils."
    ),
    reputation_narrative=(
        "Weingut Gross is among the most respected names in Steiermark for both Sauvignon Blanc "
        "and Morillon. A reference producer for the Ratsch subzone's refined mineral style."
    ),
    price_positioning="premium"
)

print("\n--- Steiermark Products ---")
TEMENT_ZIR = PROD(
    "Tement Zieregg Sauvignon Blanc",
    "wine_still", TEMENT, STEIERMARK, "Austria",
    subcategory="white",
    description=(
        "The defining expression of Südsteiermark Sauvignon Blanc — Tement's Zieregg vineyard on "
        "steep Opok (calcareous clay-marl) soils produces the benchmark of the appellation. White "
        "grapefruit, elderflower, lemon zest, white peach, and a deep mineral-stony precision that "
        "rivals the finest Sancerre. The wine ferments and ages in large oak casks, gaining texture "
        "and complexity without oak influence. Zieregg ages magnificently for 10-15 years, revealing "
        "petrol and mineral depth with time. One of the great white wines of central Europe."
    ),
    price_tier="ultra_premium"
)

TEMENT_ESTATE = PROD(
    "Tement Steiermark Sauvignon Blanc",
    "wine_still", TEMENT, STEIERMARK, "Austria",
    subcategory="white",
    description=(
        "Tement's estate Sauvignon Blanc is itself a benchmark of Steiermark — the same Opok "
        "terroir precision at an accessible price. Citrus zest, white peach, elderflower, and "
        "the characteristic stony Styrian minerality. The estate label demonstrates why South "
        "Styria is among Europe's great Sauvignon Blanc appellations."
    ),
    price_tier="premium"
)

POLZ_HOCHG = PROD(
    "Polz Hochgrassnitzberg Sauvignon Blanc",
    "wine_still", POLZ, STEIERMARK, "Austria",
    subcategory="white",
    description=(
        "Polz's flagship single-vineyard Sauvignon Blanc from the steep Hochgrassnitzberg site "
        "in Gamlitz — a wine of extraordinary mineral intensity and aging potential. The Opok "
        "subsoil delivers the characteristic stony precision; the ripe tropical aromatics (passion "
        "fruit, guava, mango) are balanced by high acidity and a limestone mineral spine that "
        "persists for 8-12 years."
    ),
    price_tier="premium"
)

GROSS_MORILLON = PROD(
    "Weingut Gross Nussberg Morillon",
    "wine_still", GROSS, STEIERMARK, "Austria",
    subcategory="white",
    description=(
        "Gross Nussberg Morillon (Chardonnay) is one of Steiermark's finest expressions of the "
        "variety — fermented and aged in large Austrian oak, producing a wine of considerable "
        "complexity: ripe apple, butter brioche, lemon curd, and that distinctive Styrian mineral "
        "precision. A white wine of serious depth that challenges top white Burgundy in texture "
        "and longevity. Age 5-10 years for full expression."
    ),
    price_tier="premium"
)

# ─── RUEDA DO ─────────────────────────────────────────────────────────────────
print("\n=== RUEDA DO ===")

RUEDA = R(
    name="Rueda DO",
    country="Spain",
    beverage_family="wine",
    description=(
        "Spain's premier white wine appellation for Verdejo — a high-altitude plateau (750-900m) "
        "in Castilla y León producing wines of striking freshness, herbal character, and mineral "
        "precision. The combination of extreme continental climate (hot days, very cold nights) and "
        "alluvial soils with white limestone and gravel delivers Verdejo of unusual aromatic "
        "intensity: fennel, cut grass, white peach, and grapefruit with a characteristic bitter "
        "almond finish and persistent acidity. Rueda DO was Spain's first designated white wine DO "
        "(1980) and remains the standard for Verdejo globally. The appellation also produces fine "
        "Sauvignon Blanc (often blended with Verdejo) and traditional Rueda Palido (sherry-style)."
    ),
    key_producers=["Bodegas Naia", "José Pariente", "Cuatro Rayas", "Marqués de Riscal Rueda"],
    designation_type="DO",
    designation_name="Rueda DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    historical_context=(
        "Verdejo's history in Rueda dates to the 11th century when it was introduced to repopulate "
        "the Duero River plateau after the Reconquista. The variety was nearly abandoned for bulk "
        "production until the 1970s-80s renaissance, when Marqués de Riscal invested in modern "
        "Verdejo production and established the template for the modern Rueda style. DO status was "
        "awarded in 1980 — Spain's first white wine DO — recognising Verdejo's unique character."
    )
)

print("\n--- Rueda Producers ---")
JOSE_PARIENTE = P(
    "José Pariente", "winery", RUEDA, "Spain",
    production_philosophy="Single-estate Verdejo and Sauvignon Blanc from Rueda plateau, organic",
    philosophy_description=(
        "Victoria Pariente produces some of Rueda's most acclaimed Verdejo from the family estate's "
        "old vines on the Duero plateau. The José Pariente estate Verdejo is a benchmark of the "
        "appellation: vibrant, aromatic, with intense fennel, citrus, and mineral precision. The "
        "Cimentum single-vineyard from 50+ year old vines is one of Rueda's finest expressions, "
        "demonstrating that great Verdejo can rival international Sauvignon Blanc in complexity. "
        "Certified organic since 2017."
    ),
    reputation_narrative=(
        "José Pariente is one of Rueda's most admired producers — Victoria Pariente's meticulous "
        "approach to old-vine Verdejo produces wines of consistent excellence. The estate is a "
        "reference for fine dining lists seeking quality Spanish white wine."
    ),
    price_positioning="premium"
)

NAIA = P(
    "Bodegas Naia", "winery", RUEDA, "Spain",
    production_philosophy="Single-vineyard old-vine Verdejo, biodynamic, from sandy Rueda soils",
    philosophy_description=(
        "Naia is one of Rueda's most ambitious estates — biodynamic farming of old-vine Verdejo "
        "from the appellation's sandiest, most mineral soils. The Naia estate Verdejo is a "
        "benchmark of aromatic freshness and mineral precision; the Nas de Rei single-vineyard "
        "Verdejo from 70+ year old ungrafted vines is one of the appellation's greatest wines. "
        "A producer that demonstrates the aging potential and complexity of great Verdejo."
    ),
    reputation_narrative=(
        "Bodegas Naia is one of Rueda's most respected producers for quality-focused old-vine "
        "Verdejo. The Nas de Rei bottling is among the appellation's collectible wines."
    ),
    price_positioning="premium"
)

print("\n--- Rueda Products ---")
JOSE_PARIENTE_VRD = PROD(
    "José Pariente Verdejo",
    "wine_still", JOSE_PARIENTE, RUEDA, "Spain",
    subcategory="white",
    description=(
        "The estate Verdejo that defines modern Rueda: vivid aromatics of fennel, white peach, "
        "citrus zest, and cut herbs; bright acidity from the high-altitude plateau; and a "
        "characteristic bitter almond finish. José Pariente's Verdejo demonstrates the variety "
        "at its most compelling — fresh, food-friendly, and with greater complexity than its "
        "price suggests. A benchmark aperitif and seafood wine."
    ),
    price_tier="mid_range"
)

JOSE_PARIENTE_CIM = PROD(
    "José Pariente Cimentum Verdejo",
    "wine_still", JOSE_PARIENTE, RUEDA, "Spain",
    subcategory="white",
    description=(
        "From 50+ year old vine plots on Rueda's highest plateau sites — Cimentum is José Pariente's "
        "demonstration of Verdejo's capacity for serious wine. The old-vine concentration and site "
        "minerality adds complexity to the fennel-citrus-herbal aromatics: greater texture, a mineral "
        "precision reminiscent of Sancerre, and aging potential of 4-6 years. One of Rueda's finest "
        "expressions of the variety."
    ),
    price_tier="premium"
)

NAIA_ESTATE = PROD(
    "Naia Verdejo",
    "wine_still", NAIA, RUEDA, "Spain",
    subcategory="white",
    description=(
        "Bodegas Naia's estate Verdejo from biodynamically-farmed old vines on sandy Rueda soils — "
        "a wine of exceptional aromatic intensity and mineral purity. White grapefruit, fennel, "
        "lime zest, and a distinctive flinty minerality from the sandy subsoils. Skin-contact "
        "influence adds textural complexity. Among the most precise and food-friendly Verdejos "
        "in the appellation."
    ),
    price_tier="mid_range"
)

# ─── FINGER LAKES ─────────────────────────────────────────────────────────────
print("\n=== FINGER LAKES ===")

FINGER_LAKES = R(
    name="Finger Lakes AVA",
    country="USA",
    beverage_family="wine",
    description=(
        "New York State's most important fine wine region — eleven glacially-carved lakes in upstate "
        "New York whose depths moderate the climate, extending the growing season in this otherwise "
        "extreme continental climate. The Finger Lakes are defined by Riesling: the region's cool "
        "climate, shale and limestone soils, and the moderating influence of the deep lake water "
        "produce Riesling of extraordinary precision, mineral depth, and natural acidity that rivals "
        "German Mosel and Austrian Wachau. Seneca Lake and Cayuga Lake are the two dominant sub-AVAs. "
        "The region is also notable for Gewurztraminer and Cabernet Franc. A fine dining wine list "
        "staple for American regional identity and Riesling enthusiasts."
    ),
    key_producers=["Hermann J. Wiemer", "Dr. Konstantin Frank", "Ravines Wine Cellars",
                   "Anthony Road Wine Company", "Red Newt Cellars"],
    designation_type="AVA",
    designation_name="Finger Lakes AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    historical_context=(
        "European immigrants planted the first vinifera vines in the Finger Lakes in the 19th century, "
        "but the modern fine wine era began with Dr. Konstantin Frank's pioneering work in the 1960s — "
        "proving that vinifera (not just hybrid) varieties could thrive in upstate New York's extreme "
        "winters. Hermann J. Wiemer (a German-trained winemaker) then established the Riesling "
        "benchmark from the 1970s onward. Today the Finger Lakes is the most respected wine region in "
        "the northeastern USA and its Riesling competes with Europe's finest."
    )
)

print("\n--- Finger Lakes Producers ---")
WIEMER = P(
    "Hermann J. Wiemer Vineyard", "winery", FINGER_LAKES, "USA",
    production_philosophy="Estate Riesling from Seneca Lake shale slopes, German-trained precision",
    philosophy_description=(
        "Hermann J. Wiemer (trained at Germany's Bernkastel vine nursery) founded the estate that "
        "would define Finger Lakes Riesling as a world-class category. The estate's Magdalena "
        "Vineyard on Seneca Lake's west slope produces Riesling of extraordinary mineral precision, "
        "high natural acidity, and aging potential rivalling German Mosel. Fred Merwarth (winemaker "
        "since 2007) has maintained and elevated Wiemer's legacy — producing dry, off-dry, and "
        "late-harvest Riesling of remarkable consistency and complexity."
    ),
    reputation_narrative=(
        "Hermann J. Wiemer is the most iconic name in Finger Lakes wine — the producer that proved "
        "Riesling of world-class quality can be grown in New York. Magdalena Vineyard Riesling "
        "appears on the finest American restaurant wine lists."
    ),
    price_positioning="premium"
)

DR_FRANK = P(
    "Dr. Konstantin Frank Winery", "winery", FINGER_LAKES, "USA",
    production_philosophy="Pioneer of vinifera viticulture in the Finger Lakes, family estate",
    philosophy_description=(
        "Dr. Konstantin Frank's 1960s demonstration that European vinifera varieties could survive "
        "Finger Lakes winters established the entire modern fine wine category for the northeastern "
        "USA. The Frank family estate on Keuka Lake continues the pioneering tradition — producing "
        "Riesling, Gewurztraminer, Pinot Gris, and Cabernet Franc of outstanding quality. The "
        "Château Frank sparkling (méthode traditionnelle) is among the USA's finest traditional-method "
        "sparkling wines. A living monument to American wine history."
    ),
    reputation_narrative=(
        "Dr. Konstantin Frank is the founding name of Finger Lakes fine wine — a historic estate "
        "of immense importance to American wine culture. Their wines are a benchmark for the region."
    ),
    price_positioning="premium"
)

RAVINES = P(
    "Ravines Wine Cellars", "winery", FINGER_LAKES, "USA",
    production_philosophy="Dry Riesling and dry wines from multiple Finger Lakes sites",
    philosophy_description=(
        "Morten Hallgren (French-trained, raised in Provence) founded Ravines to make the Finger "
        "Lakes' most food-friendly, dry Riesling — demonstrating that the region's Riesling is not "
        "simply sweet but capable of the precision and minerality of Alsace and Germany. The Argetsinger "
        "and Sawmill Creek single-vineyard Rieslings are benchmarks of dry Finger Lakes style: "
        "limey, mineral, high-acid, and magnificent with food. A reference producer for dry "
        "Finger Lakes Riesling advocates."
    ),
    reputation_narrative=(
        "Ravines is the most important producer of dry Finger Lakes Riesling — a style that has "
        "transformed the region's fine dining reputation. Morten Hallgren's wines are essential "
        "on any comprehensive American wine list."
    ),
    price_positioning="premium"
)

print("\n--- Finger Lakes Products ---")
WIEMER_MAGD = PROD(
    "Hermann J. Wiemer Magdalena Vineyard Riesling",
    "wine_still", WIEMER, FINGER_LAKES, "USA",
    subcategory="white",
    description=(
        "The definitive Finger Lakes Riesling — from Hermann J. Wiemer's home estate Magdalena "
        "Vineyard on Seneca Lake's west slope. This single-vineyard Riesling has propelled the "
        "Finger Lakes into the global Riesling conversation: extraordinary acidity, deep shale "
        "minerality, green apple, lime zest, and white flower aromatics. Whether harvested dry or "
        "with slight residual sugar, Magdalena Vineyard Riesling ages magnificently for 15-20 years, "
        "developing petrol, honey, and mineral complexity. The benchmark of American Riesling."
    ),
    price_tier="premium"
)

WIEMER_DRY = PROD(
    "Hermann J. Wiemer Dry Riesling",
    "wine_still", WIEMER, FINGER_LAKES, "USA",
    subcategory="white",
    description=(
        "Wiemer's estate dry Riesling — blended from Seneca Lake estate blocks — is a wine of "
        "remarkable consistency and precision. High natural acidity, citrus and green apple fruit, "
        "floral aromatics, and the characteristic Finger Lakes shale minerality in an accessible "
        "format. Among the finest-value dry Rieslings produced in the Americas."
    ),
    price_tier="mid_range"
)

DR_FRANK_RIESL = PROD(
    "Dr. Konstantin Frank Dry Riesling",
    "wine_still", DR_FRANK, FINGER_LAKES, "USA",
    subcategory="white",
    description=(
        "Dr. Konstantin Frank's estate dry Riesling from the Keuka Lake estate — a wine of "
        "historical importance and consistent quality. Citrus zest, green apple, white peach, "
        "and a distinctive mineral character from the glacially-deposited shale soils. The "
        "Frank family's commitment to dry-style Riesling has been vindicated by critical acclaim "
        "and a loyal fine dining following across America."
    ),
    price_tier="mid_range"
)

RAVINES_ARG = PROD(
    "Ravines Argetsinger Vineyard Riesling",
    "wine_still", RAVINES, FINGER_LAKES, "USA",
    subcategory="white",
    description=(
        "Ravines' single-vineyard Riesling from the Argetsinger site on Seneca Lake's east slope — "
        "one of the finest expressions of dry Finger Lakes Riesling. Morten Hallgren's "
        "French-influenced precision translates into a wine of Alsatian character: bone-dry, "
        "mineral, with lemon zest, green herbs, and a stony persistence that improves for 5-8 years. "
        "A must-have for any serious American restaurant wine list."
    ),
    price_tier="premium"
)

# ─── STEIERMARK VINTAGES ──────────────────────────────────────────────────────
print("\n=== STEIERMARK VINTAGES ===")
V(STEIERMARK, 2015, 95, "exceptional",
  "The greatest Steiermark vintage of the modern era: perfect continental conditions with warm days "
  "and cold nights delivering the ideal balance of ripeness and acidity for Sauvignon Blanc and Morillon. "
  "Tement Zieregg 2015 is considered one of the finest Styrian Sauvignon Blancs ever produced. "
  "Exceptional aging potential — the great wines from this vintage will drink well through 2030+.",
  "rising", 2017, 2032)

V(STEIERMARK, 2017, 91, "excellent",
  "A warm, early Steiermark vintage — the high altitude and extreme day-night temperature variation "
  "maintained the characteristic acidity of Styrian Sauvignon Blanc despite the heat. The wines show "
  "richer, more tropical fruit than cooler vintages. Best drunk 2019-2024.",
  "stable", 2018, 2024)

V(STEIERMARK, 2019, 93, "exceptional",
  "An outstanding cool-climate Steiermark vintage — the extreme day-night temperature variation "
  "produced Sauvignon Blanc and Morillon of pristine acidity and mineral precision. The Opok "
  "soils delivered maximum mineral expression. Tement, Polz, and Gross produced exceptional "
  "single-vineyard wines of 10+ year aging potential.",
  "stable", 2021, 2030)

V(STEIERMARK, 2021, 92, "excellent",
  "Classic Steiermark vintage: cool, long growing season with excellent preservation of aromatic "
  "precision. The Sauvignon Blanc shows the characteristic fennel, citrus, and stony mineral "
  "character at their most defined. Excellent medium-term cellaring potential (5-8 years).",
  "stable", 2022, 2028)

V(STEIERMARK, 2022, 90, "excellent",
  "Warm, consistent Steiermark vintage delivering approachable Sauvignon Blanc with generous "
  "fruit and early accessibility. Less mineral tension than 2021 but excellent quality across "
  "the appellation. Drink 2023-2026.",
  "stable", 2023, 2026)

# ─── RUEDA VINTAGES ──────────────────────────────────────────────────────────
print("\n=== RUEDA VINTAGES ===")
V(RUEDA, 2018, 92, "excellent",
  "An excellent Rueda vintage — the high-altitude plateau delivered ideal conditions for Verdejo. "
  "Good balance of aromatic intensity and acidity. José Pariente's Cimentum from this vintage "
  "shows exceptional old-vine concentration.",
  "stable", 2019, 2024)

V(RUEDA, 2019, 93, "exceptional",
  "One of Rueda's finest recent vintages — the extreme continental climate produced Verdejo of "
  "extraordinary freshness and mineral precision. The night temperatures preserved natural acidity "
  "while daytime heat delivered full phenolic ripeness. Old-vine Verdejo from this vintage is "
  "outstanding.",
  "stable", 2020, 2025)

V(RUEDA, 2020, 90, "excellent",
  "A warm but consistent Rueda vintage. The high altitude mitigated heat stress; Verdejo maintained "
  "its characteristic herbal-citrus aromatics. Good quality across the appellation.",
  "stable", 2021, 2024)

V(RUEDA, 2021, 91, "excellent",
  "Classic Rueda vintage: excellent balance between the plateau's extreme day-night temperature "
  "variation and summer warmth. Verdejo of vivid aromatic intensity and bright acidity. "
  "Drink within 2-3 years for maximum freshness.",
  "stable", 2022, 2025)

V(RUEDA, 2022, 89, "very_good",
  "Good Rueda vintage — warm summer required careful canopy management but top producers "
  "achieved consistent quality. Fresh, aromatic Verdejo style for early drinking.",
  "stable", 2023, 2025)

# ─── FINGER LAKES VINTAGES ───────────────────────────────────────────────────
print("\n=== FINGER LAKES VINTAGES ===")
V(FINGER_LAKES, 2016, 94, "exceptional",
  "A near-perfect Finger Lakes Riesling vintage — ideal growing season with warm summers and "
  "the lake's moderating influence preserving acidity through a long September harvest. Wiemer "
  "Magdalena and Ravines Argetsinger 2016 are benchmark expressions: mineral, precise, and with "
  "exceptional aging potential of 15-20 years. One of the region's historic vintages.",
  "rising", 2018, 2035)

V(FINGER_LAKES, 2018, 91, "excellent",
  "A warm, challenging Finger Lakes vintage — late-season cold snaps threatened the crop but "
  "the best sites on Seneca and Cayuga Lakes produced concentrated, ripe Riesling. Less typical "
  "mineral precision than 2016 but showing generous fruit and early accessibility.",
  "stable", 2019, 2025)

V(FINGER_LAKES, 2019, 92, "excellent",
  "An excellent cool-climate Finger Lakes vintage — the Great Lakes influence kept temperatures "
  "moderate through September, producing Riesling of classic precision: citrus zest, mineral, "
  "high acidity. Wiemer dry Riesling 2019 is among the most food-friendly in years.",
  "stable", 2021, 2028)

V(FINGER_LAKES, 2021, 93, "exceptional",
  "Outstanding Finger Lakes vintage — one of the best recent years for Riesling. The long, cool "
  "growing season produced wines of extraordinary mineral precision and natural acidity. "
  "Magdalena Vineyard 2021 is a collector's wine with 15+ year potential.",
  "stable", 2023, 2035)

V(FINGER_LAKES, 2022, 90, "excellent",
  "Good Finger Lakes vintage with above-average quality. Warmer than 2021 but the lake "
  "moderation preserved characteristic Riesling freshness. Accessible from release; "
  "mid-term aging potential of 5-8 years.",
  "stable", 2023, 2028)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Steiermark pairings
PAIR(TEMENT_ZIR, "Steamed asparagus with lemon beurre blanc and chervil",
    "complement", "classic", "starter",
    "Tement Zieregg Sauvignon Blanc and asparagus: the quintessential Steiermark pairing. "
    "The wine's bright citrus and mineral precision is the natural companion for asparagus — "
    "the Opok soil minerality amplifies the vegetable's earthy sweetness; lemon beurre blanc "
    "bridges the wine's citrus character; chervil echoes the Sauvignon's herbal aromatics. "
    "A pairing of absolute regional logic from Austria's finest white wine appellation.")

PAIR(TEMENT_ZIR, "Grilled whole sea bass with fennel, lemon confit, and herbs",
    "elevate", "established", "fish_course",
    "Zieregg Sauvignon Blanc's mineral precision and high acidity elevates delicate whole fish: "
    "the wine's grapefruit and elderflower character bridges the fennel's anise note; lemon "
    "confit amplifies the wine's citrus precision; the Opok mineral backbone penetrates the "
    "sea bass's delicate richness without overwhelming it. One of the great Austrian white "
    "wine and fish pairings.")

PAIR(TEMENT_ESTATE, "Goat's cheese salad with walnut, honey, and radicchio",
    "complement", "classic", "starter",
    "Steiermark Sauvignon Blanc and goat's cheese: a classic. The wine's acidity cuts through "
    "the cheese's tang while the citrus and herbal aromatics complement the goat's character. "
    "Walnut adds earthy depth; honey bridges the wine's fruit; radicchio's bitterness amplifies "
    "the wine's mineral precision.")

PAIR(TEMENT_ESTATE, "Pan-fried zander with parsley root purée and brown butter",
    "complement", "established", "fish_course",
    "Tement estate Sauvignon Blanc with freshwater fish — a quintessential Austrian pairing. "
    "Zander's delicate white flesh and the parsley root purée's earthy sweetness find perfect "
    "balance with the wine's herbaceous precision and mineral acidity. Brown butter bridges the "
    "wine's texture with the fish's richness. Classic Styrian fine dining logic.")

PAIR(POLZ_HOCHG, "Crayfish bisque with tarragon and crème fraîche",
    "elevate", "established", "fish_course",
    "Polz Hochgrassnitzberg's tropical-mineral Sauvignon Blanc elevates the rich sweetness of "
    "crayfish bisque — the wine's passion fruit and citrus character amplifies the crustacean's "
    "natural sweetness while the mineral spine cuts through the cream. Tarragon bridges the "
    "wine's herbal character.")

PAIR(GROSS_MORILLON, "Roasted poularde with morel cream sauce and truffle",
    "elevate", "established", "main",
    "Gross Nussberg Morillon — Steiermark's finest Chardonnay — achieves its greatest expression "
    "with roasted poularde and morel cream: the wine's apple and butter richness mirrors the "
    "cream sauce while the Styrian mineral precision cuts through it. Truffle amplifies the "
    "Morillon's earthy complexity. A pairing that elevates Austrian white wine to Burgundy-level "
    "fine dining context.")

# Rueda pairings
PAIR(JOSE_PARIENTE_VRD, "Grilled gambas al ajillo (prawns with garlic and olive oil)",
    "complement", "classic", "starter",
    "José Pariente Verdejo and gambas al ajillo: the classic Spanish white wine and seafood pairing. "
    "The wine's fennel, citrus, and mineral character cuts through the olive oil richness; the "
    "garlic amplifies the Verdejo's herbal aromatics; the prawns' sweetness bridges the wine's "
    "characteristic bitter almond finish. An everyday Spanish pairing executed at high quality.")

PAIR(JOSE_PARIENTE_VRD, "Manchego cheese with membrillo (quince paste)",
    "complement", "classic", "cheese",
    "Rueda Verdejo and Manchego: the defining Spanish aperitivo pairing. The wine's bright "
    "herbal acidity cuts through the sheep's milk fat; the quince paste's sweetness bridges "
    "the Verdejo's bitter almond character; the cheese's caramel depth amplifies the wine's "
    "mineral finish. An essential pairing for any Spanish wine education.")

PAIR(JOSE_PARIENTE_CIM, "Cured sea bass (lubina) with lemon, dill, and olive oil",
    "complement", "established", "starter",
    "José Pariente Cimentum's old-vine complexity and mineral depth makes it an ideal partner "
    "for cured sea bass — the wine's concentration bridges the fish's silky texture; lemon and "
    "dill amplify the Verdejo's citrus-herbal character; olive oil echoes the wine's Mediterranean "
    "weight. A sophisticated Rueda pairing beyond the standard aperitif use.")

PAIR(NAIA_ESTATE, "Grilled white asparagus with lemon oil and Serrano ham",
    "complement", "classic", "starter",
    "Naia Verdejo's precision and mineral purity pairs classically with white asparagus — "
    "one of spring's great fine dining ingredients. The wine's citrus and fennel character "
    "amplifies the asparagus's delicate sweetness; Serrano ham adds umami depth that the "
    "Verdejo's acidity cuts through; lemon oil bridges wine and vegetable.")

# Finger Lakes pairings
PAIR(WIEMER_MAGD, "Pan-roasted trout with lemon, capers, and brown butter (truite meunière)",
    "elevate", "classic", "fish_course",
    "Hermann J. Wiemer Magdalena Vineyard Riesling and freshwater trout: the Finger Lakes pairing "
    "of highest authority. The wine's mineral shale depth and precise acidity elevates the delicate "
    "trout — the lemon amplifies the Riesling's citrus precision; capers bridge the wine's mineral "
    "salinity; brown butter provides the richness the wine can penetrate. A pairing rooted in "
    "the lakes and streams of upstate New York.")

PAIR(WIEMER_MAGD, "Foie gras terrine with Riesling Spätlese jelly and toasted brioche",
    "contrast", "established", "amuse",
    "Wiemer Magdalena Riesling — with slight residual sugar — creates the classic Riesling-foie "
    "gras contrast: the wine's high acidity and mineral precision cuts through the fat while "
    "gentle sweetness amplifies the foie's richness. Riesling Spätlese jelly bridges the wine "
    "and the foie's character. A fine dining pairing that demonstrates Finger Lakes Riesling's "
    "European pedigree.")

PAIR(WIEMER_DRY, "Thai red curry with coconut milk, lemongrass, and jasmine rice",
    "complement", "established", "main",
    "Wiemer dry Riesling's high acidity and aromatic precision is the ideal counterpart to Thai "
    "red curry — the wine's citrus and floral character amplifies the lemongrass and kaffir lime; "
    "the acidity cuts through the coconut richness; the mineral backbone provides structure for "
    "the spice. A classic off-menu pairing that wine-savvy guests order instinctively.")

PAIR(DR_FRANK_RIESL, "Duck breast with cherry sauce and roasted root vegetables",
    "complement", "established", "main",
    "Dr. Frank dry Riesling's acidity and mineral precision cuts through duck breast's richness "
    "while the wine's apple and citrus character bridges the cherry sauce. Root vegetables "
    "provide an earthy base for the Riesling's mineral character. A pairing that demonstrates "
    "the Finger Lakes Riesling's versatility beyond seafood and delicate dishes.")

PAIR(DR_FRANK_RIESL, "Raw oysters with mignonette",
    "complement", "classic", "amuse",
    "Dr. Frank dry Riesling's precision and mineral acidity is a natural partner for raw oysters — "
    "the wine's lime zest and saline mineral character mirrors the oyster's brine while the "
    "acidity cleanses the palate. A classic American pairing demonstrating that Finger Lakes "
    "Riesling belongs in the same conversation as Chablis and Champagne for oyster service.")

PAIR(RAVINES_ARG, "Roasted sea scallops with parsnip purée and apple",
    "elevate", "established", "fish_course",
    "Ravines Argetsinger Riesling — bone-dry, mineral, Alsatian in style — elevates sea scallops "
    "with parsnip: the wine's dry mineral precision and citrus note amplifies the scallop's natural "
    "sweetness while cutting through the parsnip cream. Apple bridges the wine's fruit character "
    "with the scallop's delicacy. A pairing that announces the Finger Lakes as serious fine "
    "dining territory.")

PAIR(RAVINES_ARG, "Asian-spiced crab cake with mango salsa and chilli",
    "complement", "established", "starter",
    "Ravines Argetsinger's dry Riesling acidity and citrus precision is the ideal partner for "
    "crab cake with Asian spice — the wine's lime and mineral character amplifies the crab's "
    "sweetness; the chilli heat is tempered by the wine's acidity; mango bridges the wine's "
    "tropical aromatics. A modern American pairing that showcases Finger Lakes Riesling's "
    "food versatility.")

cur.close()
conn.close()
print("\n✅ Terminal 13 Batch 2 — Steiermark + Rueda DO + Finger Lakes complete.")
