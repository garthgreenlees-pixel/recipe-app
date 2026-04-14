#!/usr/bin/env python3
"""B161 — Wachau DAC (Austria), Kamptal DAC, Kremstal DAC,
   Steiermark DAC, Burgenland (Neusiedlersee) — Austrian wine deep dive"""

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
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region inserted: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
        (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Wachau DAC ─────────────────────────────────────────────────────────────
print("=== Wachau DAC ===")
r1 = R("Wachau DAC", "Austria", "wine",
        designation_type="DAC", designation_name="Wachau",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Austria's most prestigious wine region, the Wachau occupies a dramatic "
            "bend in the Danube between Krems and Melk, with near-vertical gneiss and "
            "granite terraces carved by the river. Grüner Veltliner and Riesling "
            "dominate, producing wines of extraordinary mineral precision, weight, and "
            "longevity. The three-tier Steinfeder/Federspiel/Smaragd classification "
            "defines wine weight, not sweetness."
        ),
        key_producers="Domäne Wachau, F.X. Pichler, Emmerich Knoll, Rudi Pichler, Hirtzberger",
        historical_context=(
            "The Wachau's classification system — Vinea Wachau — was established in "
            "1983 by the leading producers to protect quality and provenance. F.X. Pichler "
            "established the region's international reputation with wines of extraordinary "
            "concentration. The UNESCO World Heritage landscape draws visitors worldwide."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Wachau year; gneiss mineral and freshness"),
    (2021, "very_good",  "stable",  "Elegant, precise; Riesling exceptional"),
    (2020, "excellent",  "rising",  "Rich and concentrated; great Smaragd vintage"),
    (2019, "excellent",  "stable",  "Classic Wachau; mineral precision and depth"),
    (2018, "very_good",  "stable",  "Warm; powerful Smaragd wines with good balance"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("F.X. Pichler Weingut", "winery", r1, "Austria",
        production_philosophy="old_vine_low_yield",
        philosophy_description="Ultra-low yields; concentrated Smaragd wines; M designation for top selections.",
        reputation_narrative="Austria's most iconic winemaker; Loibenberg M Smaragd is among the world's greatest whites.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("F.X. Pichler Loibenberg Riesling Smaragd Wachau", "wine_still", p1a, r1, "Austria",
    subcategory="white",
    description="Iconic Smaragd Riesling from gneiss Loibenberg; concentrated, mineral, ages for 20+ years.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Vienna Schnitzel (Wiener Schnitzel) with lemon", "complement", "classic", "main",
         "Austria's iconic dish and Austria's iconic wine — the national pairing")
    PAIR(prod1a, "grilled Danube fish (zander) with herb butter", "complement", "classic", "main",
         "Danube fish and Wachau Riesling — regional tradition")
    PAIR(prod1a, "white asparagus with hollandaise and chervil", "complement", "classic", "main",
         "Austrian white asparagus season and Wachau Smaragd")
    PAIR(prod1a, "grilled langoustine with lemon and herbs", "complement", "established", "main",
         "powerful Smaragd and delicate crustacean")

prod1b, new1b = PROD("F.X. Pichler Kellerberg Grüner Veltliner Smaragd Wachau", "wine_still", p1a, r1, "Austria",
    subcategory="white",
    description="Benchmark Smaragd Grüner Veltliner from Kellerberg; white pepper, mineral, extraordinary.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "roast chicken with tarragon cream sauce", "complement", "classic", "main",
         "classic Austrian preparation and GV Smaragd")
    PAIR(prod1b, "turbot with white pepper and herbs", "complement", "established", "main",
         "white pepper in wine mirrors preparation")
    PAIR(prod1b, "warm asparagus salad with Parma ham", "complement", "classic", "main",
         "asparagus and Grüner Veltliner — classic Austrian combination")
    PAIR(prod1b, "aged Gruyère and caraway crackers", "complement", "established", "cheese",
         "mineral GV and aged Swiss-style cheese")

p1b = P("Emmerich Knoll Weingut", "winery", r1, "Austria",
        production_philosophy="traditional_wachau",
        philosophy_description="Traditional Wachau; old-vine gneiss; Kreutle and Loibenberg top sites.",
        reputation_narrative="The most traditional of Wachau's great estates; wines of extraordinary longevity.",
        price_positioning="ultra_premium")
prod1c, new1c = PROD("Knoll Loibner Kreutle Grüner Veltliner Smaragd Wachau", "wine_still", p1b, r1, "Austria",
    subcategory="white",
    description="Classic Wachau Smaragd GV from Kreutle site; white pepper, mineral, built for long aging.",
    price_tier="ultra_premium")
if new1c:
    PAIR(prod1c, "Wiener Schnitzel with potato salad and lemon", "complement", "classic", "main",
         "Austria's national dish and Wachau GV — the benchmark pairing")
    PAIR(prod1c, "roast carp with herbs (Wachau tradition)", "complement", "classic", "main",
         "Wachau river fish and Wachau wine — regional tradition")
    PAIR(prod1c, "asparagus cream soup", "complement", "classic", "starter",
         "Austrian asparagus tradition and Grüner Veltliner")
    PAIR(prod1c, "aged Alp cheese with rye bread", "complement", "established", "cheese",
         "mountain cheese and mineral GV Smaragd")

prod1d, new1d = PROD("Knoll Riesling Smaragd Wachau", "wine_still", p1b, r1, "Austria",
    subcategory="white",
    description="Wachau Smaragd Riesling from Knoll; slate-driven mineral precision; age-worthy.",
    price_tier="ultra_premium")
if new1d:
    PAIR(prod1d, "grilled zander (pike-perch) from the Danube", "complement", "classic", "main",
         "Danube fish and Wachau Riesling")
    PAIR(prod1d, "Saibling (Arctic char) with herbs and butter", "complement", "established", "main",
         "Austrian mountain fish and Wachau Riesling")
    PAIR(prod1d, "crab and herb salad with citrus", "complement", "established", "starter",
         "mineral Riesling and shellfish")
    PAIR(prod1d, "apricot Knödel (Wachau apricot specialty)", "complement", "classic", "dessert",
         "Wachau is famous for apricots; the regional dessert and regional wine")

# ── 2. Kamptal DAC ────────────────────────────────────────────────────────────
print("=== Kamptal DAC ===")
r2 = R("Kamptal DAC", "Austria", "wine",
        designation_type="DAC", designation_name="Kamptal",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description=(
            "The Kamptal runs north from Krems along the Kamp River, where Grüner "
            "Veltliner and Riesling grow on volcanic and loess soils. The Heiligenstein "
            "— a volcanic site unique in Austria — produces Riesling of extraordinary "
            "spice, mineral complexity, and longevity. Loimer and Bründlmayer lead "
            "the quality revolution that has made Kamptal internationally celebrated."
        ),
        key_producers="Willi Bründlmayer, Loimer, Hirsch, Jurtschitsch, Eichinger",
        historical_context=(
            "Kamptal's fame rests on the Heiligenstein — a volcanic (rhyolite) site "
            "surrounded by gneiss and limestone that produces distinctly spicy Riesling "
            "unlike any in Europe. Bründlmayer's Zöbinger Heiligenstein is consistently "
            "ranked among Austria's greatest wines."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Kamptal year; Heiligenstein and Grüner excel"),
    (2021, "very_good",  "stable",  "Fresh, precise wines; excellent freshness"),
    (2020, "excellent",  "stable",  "Rich and structured; great Riesling vintage"),
    (2019, "very_good",  "stable",  "Classic; accessible and food-friendly"),
    (2018, "very_good",  "stable",  "Warm year; powerful and concentrated"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Weingut Willi Bründlmayer", "winery", r2, "Austria",
        production_philosophy="biodynamic_multi_terroir",
        philosophy_description="Biodynamic; diverse terroir expression; Heiligenstein Riesling is the flagship.",
        reputation_narrative="Austria's most celebrated Kamptal estate; Heiligenstein Riesling is world-famous.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Bründlmayer Zöbinger Heiligenstein Riesling Alte Reben Kamptal", "wine_still", p2a, r2, "Austria",
    subcategory="white",
    description="Old-vine volcanic Riesling from the Heiligenstein; unique spice, mineral, extraordinary longevity.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "grilled Austrian Saibling with lemon and chive", "complement", "classic", "main",
         "Austrian mountain fish and volcanic Riesling")
    PAIR(prod2a, "white asparagus with sauce maltaise", "complement", "classic", "main",
         "Austrian spring tradition and Kamptal Riesling")
    PAIR(prod2a, "smoked eel with apple and horseradish", "complement", "classic", "starter",
         "classic preparation and volcanic mineral Riesling")
    PAIR(prod2a, "veal escalope with lemon and capers (piccata style)", "complement", "established", "main",
         "mineral precision and delicate veal")

prod2b, new2b = PROD("Bründlmayer Grüner Veltliner Loess Kamptal", "wine_still", p2a, r2, "Austria",
    subcategory="white",
    description="Loess-terroir Grüner Veltliner; entry Bründlmayer; fresh, white pepper, food-friendly.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "wiener schnitzel with potato salad", "complement", "classic", "main",
         "Austria's national dish and Grüner Veltliner")
    PAIR(prod2b, "grilled chicken with herb salad", "complement", "established", "main",
         "food-friendly GV and chicken")
    PAIR(prod2b, "green salad with vinaigrette", "complement", "classic", "starter",
         "Austrian Grüner Veltliner and fresh salad")
    PAIR(prod2b, "smoked trout with cucumber", "complement", "classic", "starter",
         "Austrian fish preparation and white pepper wine")

p2b = P("Weingut Fred Loimer", "winery", r2, "Austria",
        production_philosophy="biodynamic_natural",
        philosophy_description="Biodynamic; natural winemaking; diverse Kamptal and Austrian expressions.",
        reputation_narrative="One of Kamptal's most dynamic producers; natural wine pioneer in Austria.",
        price_positioning="premium")
prod2c, new2c = PROD("Loimer Kamptal Riesling 1 ÖTW", "wine_still", p2c := None or p2b, r2, "Austria",
    subcategory="white",
    description="First-growth classified Kamptal Riesling from Loimer; precise, mineral, age-worthy.",
    price_tier="premium")
if new2c:
    PAIR(prod2c, "grilled zander with wild garlic butter", "complement", "established", "main",
         "Austrian fish and precise Kamptal Riesling")
    PAIR(prod2c, "asparagus tart with herb cream", "complement", "established", "starter",
         "spring vegetable and Austrian Riesling")
    PAIR(prod2c, "fresh oysters with vinegar mignonette", "complement", "established", "aperitif",
         "mineral Riesling and briny oyster")
    PAIR(prod2c, "cucumber gazpacho with crème fraîche", "complement", "established", "starter",
         "fresh mineral and cool soup")

prod2d, new2d = PROD("Loimer Grüner Veltliner Kamptal Langenlois", "wine_still", p2b, r2, "Austria",
    subcategory="white",
    description="Village Grüner Veltliner from Langenlois; bright, white pepper, accessible.",
    price_tier="mid_range")
if new2d:
    PAIR(prod2d, "Wiener Würstl (Vienna sausage) with mustard", "complement", "classic", "amuse",
         "Viennese street food and Grüner Veltliner")
    PAIR(prod2d, "green bean salad with vinaigrette", "complement", "classic", "starter",
         "Austrian salad tradition and GV")
    PAIR(prod2d, "pan-fried trout with almond butter", "complement", "classic", "main",
         "Austrian freshwater fish and white pepper Grüner")
    PAIR(prod2d, "Liptauer cheese spread with paprika", "complement", "classic", "amuse",
         "Austrian cheese spread and local wine")

# ── 3. Kremstal DAC ───────────────────────────────────────────────────────────
print("=== Kremstal DAC ===")
r3 = R("Kremstal DAC", "Austria", "wine",
        designation_type="DAC", designation_name="Kremstal",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Kremstal surrounds the historic town of Krems at the eastern end of the "
            "Wachau, transitioning from the dramatic gorge to more open plains. "
            "Grüner Veltliner and Riesling grow on loess terraces and primary rock soils, "
            "producing wines of great versatility — from fresh and approachable to "
            "concentrated and age-worthy. Nikolaihof and Salomon Undhof are the "
            "region's most storied estates."
        ),
        key_producers="Nikolaihof, Salomon Undhof, Stadt Krems, Mantlerhof",
        historical_context=(
            "Krems has been a wine trading centre since the Middle Ages — its wine "
            "merchants supplied the Habsburg court. Nikolaihof is Austria's oldest "
            "winery, with cellars dating to Roman times. The estate's biodynamic "
            "vineyards have been managed under the Nikolaihof family since 1894."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "stable",  "Outstanding Kremstal year; loess and primary rock both shine"),
    (2021, "very_good",  "stable",  "Fresh and accessible; excellent everyday quality"),
    (2020, "very_good",  "stable",  "Rich and ripe; good concentration"),
    (2019, "very_good",  "stable",  "Classic year; food-friendly style"),
    (2018, "very_good",  "stable",  "Warm year; full-bodied and approachable"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Nikolaihof Weingut", "winery", r3, "Austria",
        production_philosophy="biodynamic_heritage",
        philosophy_description="Austria's oldest winery (Roman origins); biodynamic since 1971; extended aging.",
        reputation_narrative="One of Austria's most historic and storied estates; Im Weingebirge is the benchmark.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Nikolaihof Im Weingebirge Riesling Smaragd Wachau", "wine_still", p3a, r3, "Austria",
    subcategory="white",
    description="Old-vine Smaragd Riesling from Roman-era vineyard; age-worthy, mineral, profound.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "grilled Danube salmon with herb butter", "complement", "classic", "main",
         "Danube river fish and Kremstal/Wachau Riesling")
    PAIR(prod3a, "poached Saibling with dill and lemon", "complement", "classic", "main",
         "Austrian mountain fish and old-vine Riesling")
    PAIR(prod3a, "white asparagus with truffle hollandaise", "complement", "classic", "main",
         "Austrian asparagus season elevated")
    PAIR(prod3a, "aged Manchego with walnuts", "complement", "established", "cheese",
         "structured Riesling and aged hard cheese")

prod3b, new3b = PROD("Nikolaihof Steiner Hund Grüner Veltliner Smaragd Kremstal", "wine_still", p3a, r3, "Austria",
    subcategory="white",
    description="From the Steiner Hund site; biodynamic GV Smaragd of extraordinary depth and longevity.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Wiener Schnitzel with lingonberry jam", "complement", "classic", "main",
         "classic Austrian dish and Kremstal GV Smaragd")
    PAIR(prod3b, "roast pork with Knödel and gravy", "complement", "classic", "main",
         "Austrian Sunday roast and Grüner Veltliner")
    PAIR(prod3b, "fresh herb and ricotta tart", "complement", "established", "main",
         "herbal freshness bridge to white pepper notes")
    PAIR(prod3b, "aged Alpkäse (Alpine cheese)", "complement", "classic", "cheese",
         "mountain cheese and Austrian Smaragd GV")

p3b = P("Salomon Undhof Weingut", "winery", r3, "Austria",
        production_philosophy="traditional_estate",
        philosophy_description="Historic Kremstal estate; Wachtberg and Kögl are top sites for Riesling.",
        reputation_narrative="One of Kremstal's most reliable and respected producers.",
        price_positioning="premium")
prod3c, new3c = PROD("Salomon Undhof Kögl Riesling Kremstal", "wine_still", p3b, r3, "Austria",
    subcategory="white",
    description="Premium Kremstal Riesling from Kögl site; mineral, structured, food-friendly.",
    price_tier="premium")
if new3c:
    PAIR(prod3c, "grilled trout with almonds and butter", "complement", "classic", "main",
         "Austrian freshwater fish and Kremstal Riesling")
    PAIR(prod3c, "ceviche with lime and herbs", "complement", "established", "starter",
         "citrus and mineral echo")
    PAIR(prod3c, "steamed asparagus with butter sauce", "complement", "classic", "main",
         "Austrian spring tradition")
    PAIR(prod3c, "goat cheese with honey and herbs", "complement", "established", "cheese",
         "mineral Riesling and fresh cheese")

prod3d, new3d = PROD("Salomon Undhof Grüner Veltliner Kremstal", "wine_still", p3b, r3, "Austria",
    subcategory="white",
    description="Estate Grüner Veltliner; fresh, white pepper, food-friendly — everyday Austrian quality.",
    price_tier="mid_range")
if new3d:
    PAIR(prod3d, "Backhendl (Austrian fried chicken) with green salad", "complement", "classic", "main",
         "Austrian fried chicken and Grüner Veltliner — tradition")
    PAIR(prod3d, "mixed vegetable strudel", "complement", "established", "main",
         "herbal freshness and vegetable")
    PAIR(prod3d, "grilled zucchini and herb antipasto", "complement", "established", "main",
         "fresh white pepper and grilled vegetables")
    PAIR(prod3d, "fresh Liptauer spread with pumpernickel", "complement", "classic", "amuse",
         "Austrian cheese spread and GV")

# ── 4. Südsteiermark DAC ──────────────────────────────────────────────────────
print("=== Südsteiermark DAC ===")
r4 = R("Südsteiermark DAC", "Austria", "wine",
        designation_type="DAC", designation_name="Südsteiermark",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Southern Styria (Südsteiermark) produces Austria's most aromatic and "
            "vibrant white wines from steep Opok (marl-limestone) slopes near the "
            "Slovenian border. Sauvignon Blanc, Muskateller, Welschriesling, and "
            "Weissburgunder thrive in the continental-influenced climate. Sauvignon "
            "Blanc from the Südsteiermark — sometimes labeled Ried (single vineyard) "
            "— is considered among Europe's finest, rivaling Pouilly-Fumé."
        ),
        key_producers="Tement, Polz, Sabathi, Wohlmuth, Sattlerhof",
        historical_context=(
            "Südsteiermark's wine industry modernized dramatically in the 1980s-90s "
            "when producers like Tement and Polz began producing internationally "
            "recognized wines. The region's Opok soils — unique compressed marl — "
            "give Sauvignon Blanc a distinctive texture and mineral character."
        ))

for yr, qd, pt, sn in [
    (2023, "excellent",  "rising",  "Outstanding Steiermark year; Sauvignon Blanc exceptional"),
    (2022, "very_good",  "stable",  "Classic; aromatic and food-friendly"),
    (2021, "excellent",  "stable",  "Superb freshness; one of the best recent vintages"),
    (2020, "very_good",  "stable",  "Rich and textured; good concentration"),
    (2019, "very_good",  "stable",  "Consistent quality; mineral character"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Weingut Tement", "winery", r4, "Austria",
        production_philosophy="opok_terroir_precision",
        philosophy_description="Opok specialist; Zieregg Sauvignon Blanc is Austria's most famous GV-equivalent.",
        reputation_narrative="Südsteiermark's benchmark estate; Zieregg Sauvignon Blanc is world-renowned.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Tement Ried Zieregg Sauvignon Blanc Südsteiermark", "wine_still", p4a, r4, "Austria",
    subcategory="white",
    description="Austria's most celebrated Sauvignon Blanc site; Opok mineral, herbaceous, extraordinary.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "grilled sea bass with green herb sauce", "complement", "classic", "main",
         "herbaceous Sauvignon Blanc and white fish")
    PAIR(prod4a, "fresh goat cheese and herb tart", "complement", "classic", "starter",
         "classic Sauvignon and goat cheese pairing")
    PAIR(prod4a, "Styrian pumpkin soup with pumpkin seed oil", "complement", "established", "starter",
         "regional Styrian tradition and local wine")
    PAIR(prod4a, "asparagus with hollandaise and smoked salmon", "complement", "classic", "main",
         "Austrian spring vegetable and aromatic Sauvignon")

prod4b, new4b = PROD("Tement Sauvignon Blanc Südsteiermark", "wine_still", p4a, r4, "Austria",
    subcategory="white",
    description="Estate Sauvignon Blanc; fresh, aromatic, mineral — excellent value Austrian white.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "fresh Styrian Leber (liver) with onions and herbs", "complement", "established", "main",
         "regional Austrian preparation and local wine")
    PAIR(prod4b, "smoked salmon with cream cheese and dill", "complement", "classic", "starter",
         "aromatic Sauvignon and smoked fish")
    PAIR(prod4b, "summer salad with cucumber and vinaigrette", "complement", "classic", "starter",
         "fresh aromatic and garden salad")
    PAIR(prod4b, "fresh chèvre with herbs", "complement", "classic", "amuse",
         "Sauvignon Blanc and fresh goat cheese")

p4b = P("Weingut Polz", "winery", r4, "Austria",
        production_philosophy="organic_opok",
        philosophy_description="Organic Südsteiermark; Obegg and Hochgrassnitzberg are top single vineyard sites.",
        reputation_narrative="One of Südsteiermark's most consistent producers; Hochgrassnitzberg is a benchmark.",
        price_positioning="premium")
prod4c, new4c = PROD("Polz Hochgrassnitzberg Sauvignon Blanc Südsteiermark", "wine_still", p4b, r4, "Austria",
    subcategory="white",
    description="Single-vineyard Opok Sauvignon Blanc; mineral, fresh herbs, gooseberry — age-worthy.",
    price_tier="premium")
if new4c:
    PAIR(prod4c, "grilled white fish with herb butter", "complement", "classic", "main",
         "mineral Sauvignon and simple fish")
    PAIR(prod4c, "fresh asparagus with vinaigrette", "complement", "classic", "starter",
         "Austrian spring vegetable and Styrian wine")
    PAIR(prod4c, "goat cheese salad with walnuts", "complement", "classic", "starter",
         "classic Sauvignon and goat cheese")
    PAIR(prod4c, "pumpkin seed oil drizzled over antipasto", "complement", "established", "amuse",
         "Styrian specialty oil bridge to wine")

prod4d, new4d = PROD("Polz Welschriesling Südsteiermark", "wine_still", p4b, r4, "Austria",
    subcategory="white",
    description="Fresh Welschriesling from Opok soils; light, crisp, with apple and citrus character.",
    price_tier="entry")
if new4d:
    PAIR(prod4d, "fried calamari with lemon aioli", "complement", "established", "main",
         "crisp acidity and fried seafood")
    PAIR(prod4d, "fresh cucumber and herb salad", "complement", "classic", "starter",
         "refreshing acidity and garden vegetables")
    PAIR(prod4d, "Styrian Liptauer cheese spread", "complement", "classic", "amuse",
         "regional cheese spread and local white wine")
    PAIR(prod4d, "fish and chips style pike with lemon", "complement", "established", "main",
         "crisp acidity and fried fish")

# ── 5. Neusiedlersee DAC (Burgenland) ─────────────────────────────────────────
print("=== Neusiedlersee DAC ===")
r5 = R("Neusiedlersee DAC", "Austria", "wine",
        designation_type="DAC", designation_name="Neusiedlersee",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "Austria's Burgenland, surrounding the shallow Neusiedlersee, is the home "
            "of Austria's great dessert wines and increasingly impressive reds. "
            "The lake's mist creates ideal botrytis conditions for Trockenbeerenauslese, "
            "Beerenauslese, and Ausbruch from Rust. Simultaneously, Zweigelt, Blaufränkisch, "
            "and international varieties produce concentrated reds of international quality "
            "from the warm, continental climate."
        ),
        key_producers="Kracher, Feiler-Artinger, Umathum, Schloss Halbturn",
        historical_context=(
            "Alois Kracher put Neusiedlersee's sweet wines on the world map with his "
            "TBA wines achieving record prices at auction in the 1990s. The designation "
            "Ausbruch — between Beerenauslese and TBA — dates to the 17th century in "
            "the town of Rust, making it one of Austria's oldest wine classifications."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding vintage for reds; good botrytis for dessert wines"),
    (2021, "very_good",  "stable",  "Classic Burgenland; excellent reds and sweet wines"),
    (2020, "excellent",  "stable",  "Rich and concentrated; both reds and dessert wines excel"),
    (2019, "very_good",  "stable",  "Good consistency; approachable reds"),
    (2017, "excellent",  "rising",  "Classic vintage; botrytis wines of extraordinary quality"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Weingut Alois Kracher", "winery", r5, "Austria",
        production_philosophy="botrytis_precision",
        philosophy_description="World-renowned TBA specialist; two series: Zwischen den Seen and Nouvelle Vague.",
        reputation_narrative="Austria's greatest dessert wine producer; TBA wines are world benchmarks.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Kracher Trockenbeerenauslese Cuvée Burgenland", "wine_dessert", p5a, r5, "Austria",
    subcategory="botrytis_sweet",
    description="Austria's most celebrated TBA; Chardonnay and Welschriesling blend of extraordinary botrytis richness.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Roquefort with honeycomb and walnuts", "complement", "classic", "cheese",
         "TBA sweetness balances intense blue cheese")
    PAIR(prod5a, "foie gras with peach chutney", "complement", "classic", "starter",
         "sweet richness of TBA and foie gras")
    PAIR(prod5a, "fresh strawberries with crème fraîche", "complement", "classic", "dessert",
         "fruit and sweet botrytis wine")
    PAIR(prod5a, "crème brûlée", "complement", "classic", "dessert",
         "sweet TBA and caramel-vanilla dessert")

prod5b, new5b = PROD("Kracher Beerenauslese Welschriesling Burgenland", "wine_dessert", p5a, r5, "Austria",
    subcategory="botrytis_sweet",
    description="BA Welschriesling; lighter than TBA but with extraordinary honey and apricot richness.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "blue cheese (Gorgonzola) with pear", "complement", "classic", "cheese",
         "sweet BA balances bold blue cheese")
    PAIR(prod5b, "apricot tart with crème pâtissière", "complement", "classic", "dessert",
         "apricot echo in wine and tart")
    PAIR(prod5b, "peach and almond semifreddo", "complement", "established", "dessert",
         "stone fruit and sweet wine")
    PAIR(prod5b, "aged Stilton with quince paste", "complement", "established", "cheese",
         "sweet richness and powerful blue cheese")

p5b = P("Weingut Umathum", "winery", r5, "Austria",
        production_philosophy="organic_red_specialist",
        philosophy_description="Organic pioneer; Burgenland red specialist; Zweigelt and Blaufränkisch.",
        reputation_narrative="Among Austria's finest red wine producers; Haideboden and Ried Hallebühl are benchmarks.",
        price_positioning="premium")
prod5c, new5c = PROD("Umathum Zweigelt Haideboden Burgenland", "wine_still", p5b, r5, "Austria",
    subcategory="red",
    description="Benchmark Austrian Zweigelt from Haideboden; vibrant red fruit, mineral, food-friendly.",
    price_tier="premium")
if new5c:
    PAIR(prod5c, "roast duck with cherry and herb jus", "complement", "classic", "main",
         "Austrian Zweigelt and duck — a regional classic")
    PAIR(prod5c, "Burgenland Mangalica pork roast", "complement", "classic", "main",
         "regional heritage pork and local red wine")
    PAIR(prod5c, "grilled beef with mushroom sauce", "complement", "established", "main",
         "Zweigelt and beef")
    PAIR(prod5c, "aged Gouda with mustard", "complement", "established", "cheese",
         "Austrian red and aged cheese")

prod5d, new5d = PROD("Umathum Blaufränkisch Ried Hallebühl Burgenland", "wine_still", p5b, r5, "Austria",
    subcategory="red",
    description="Single-vineyard Blaufränkisch; the signature Austrian red grape at its most profound.",
    price_tier="premium")
if new5d:
    PAIR(prod5d, "roast venison with red cabbage and Knödel", "complement", "classic", "main",
         "Austrian game preparation and Blaufränkisch")
    PAIR(prod5d, "grilled lamb chops with herb butter", "complement", "classic", "main",
         "Blaufränkisch and lamb — Austrian interpretation")
    PAIR(prod5d, "wild boar ragù with pasta", "complement", "established", "main",
         "game and structured Austrian red")
    PAIR(prod5d, "aged Bergkäse with caraway crackers", "complement", "established", "cheese",
         "Austrian mountain cheese and regional red")

# ── Final counts ──────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")
print("B161 complete.")
cur.close()
conn.close()
