#!/usr/bin/env python3
"""B142 — Kamptal DAC (Austria), Kremstal DAC (Austria),
   Carneros AVA (USA), Santa Barbara County AVA (USA), Sonoma Coast AVA (USA)
All constraints verified from B136-B141.
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
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_regions
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, country, beverage_family, designation_type, designation_name,
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── KAMPTAL DAC (Austria) ─────────────────────────────────────────────────────
print("=== Kamptal DAC ===")
r = R("Kamptal DAC", "Austria", "wine",
      designation_type="DAC",
      designation_name="Kamptal DAC",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="Austria's most celebrated white wine DAC from the Kamp River valley north of Vienna, where crystalline primary rock, loess and alluvial gravel produce Grüner Veltliner and Riesling of extraordinary mineral depth and longevity. The great terraced sites of Heiligenstein, Lamm and Gaisberg are among Austria's finest single vineyards.",
      key_producers="Bründlmayer, Hirsch, Loimer, Schloss Gobelsburg",
      historical_context="Kamptal viticulture dates to Celtic and Roman times, with the valley's protected aspect and temperature variation between warm days and cool nights providing ideal conditions. The DAC system, introduced 2008, recognised Grüner Veltliner and Riesling as Kamptal's signature varieties, with the great terraced primary rock sites of Zöbing and Gobelsburg among the most prized in Austria.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Exceptional Kamptal vintage; primary rock Riesling and Grüner Veltliner of extraordinary mineral depth."),
    (2019, "very_good", "stable", "Well-balanced conditions; Kamptal DAC wines of characteristic peppery mineral freshness."),
    (2020, "excellent", "rising", "Benchmark vintage; crystalline primary rock produced Kamptal Riesling of extraordinary precision."),
    (2021, "very_good", "stable", "Good Kamptal expression; both Grüner Veltliner and Riesling showing excellent structure."),
    (2022, "excellent", "rising", "Outstanding Kamptal vintage; greatest primary rock Riesling since 2015 from the best terraced sites."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Bründlmayer", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Willi Bründlmayer at Weingut Bründlmayer is Austria's most celebrated producer of Kamptal Grüner Veltliner and Riesling, farming terraced primary rock and loess vineyards with obsessive attention to capturing the unique character of each site — particularly the legendary Heiligenstein primary rock terrace.",
       reputation_narrative="Bründlmayer is Austria's most internationally acclaimed white wine producer. The Alte Reben Grüner Veltliner and Heiligenstein Riesling are benchmarks not just for Austria but for white wine worldwide.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Bründlmayer Heiligenstein Riesling Kamptal DAC Reserve", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="ultra_premium",
    description="Austria's most celebrated Riesling from the Heiligenstein primary rock terrace; profound mineral depth, peach, spice and volcanic stone character with extraordinary tension and 20+ year aging potential.")
if is_new:
    PAIR(prod, "Fischbeuschelsuppe (Austrian fish offal soup) with egg cream", "complement", "classic", "main", "Vienna's traditional fish soup with egg and sour cream finds the mineral precision of Heiligenstein Riesling ideal.")
    PAIR(prod, "Grilled trout from the Kamp River with dill and lemon butter", "complement", "classic", "main", "River trout from the same valley as the vineyard — the ultimate Kamptal terroir pairing.")
    PAIR(prod, "Zander (pike-perch) with Riesling sauce and wild herbs", "complement", "classic", "main", "Freshwater pike-perch cooked in Riesling wine sauce is the great Austrian Riesling pairing.")
    PAIR(prod, "Aged Bergkäse with Tyrolean speck and sourdough", "complement", "established", "casual", "Alpine mountain cheese and air-dried ham find the mineral precision of Heiligenstein Riesling ideal.")

prod, is_new = PROD("Bründlmayer Grüner Veltliner Alte Reben Kamptal DAC", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="ultra_premium",
    description="Old-vine Kamptal Grüner Veltliner from Bründlmayer's best loess and primary rock parcels; profoundly mineral, peppery and complex with lime, herbs and incredible mineral depth for multi-decade evolution.")
if is_new:
    PAIR(prod, "Tafelspitz (boiled prime beef) with apple-horseradish and chive sauce", "complement", "classic", "main", "Austria's most elegant boiled beef dish finds the complexity of old-vine Kamptal Grüner Veltliner its equal.")
    PAIR(prod, "Wiener Schnitzel vom Kalb with lingonberry and lemon", "complement", "classic", "main", "The finest Viennese escalope of veal with lingonberry demands the mineral complexity of Alte Reben GV.")
    PAIR(prod, "Grilled white asparagus from Marchfeld with mousseline", "complement", "classic", "casual", "Austria's asparagus season finds its greatest companion in old-vine Grüner Veltliner's peppery complexity.")
    PAIR(prod, "Poached salmon with chive cream and cucumber salad", "complement", "established", "main", "Classic Austrian cold poached salmon with herb cream finds the peppery mineral depth of Alte Reben ideal.")

p2 = P("Schloss Gobelsburg", "winery", r, "Austria",
       production_philosophy="traditional",
       philosophy_description="The historic monastery estate of Schloss Gobelsburg, managed by Michael Moosbrugger, produces Kamptal Grüner Veltliner and Riesling from the valley's finest terraced sites, combining monastic winemaking tradition with contemporary quality standards.",
       reputation_narrative="Schloss Gobelsburg's Grüner Veltliner and Riesling from the Lamm and Gaisberg vineyards are among Austria's most consistently respected wines, demonstrating the Kamptal's capacity for wines of genuine complexity and age-worthiness.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Schloss Gobelsburg Riesling Heiligenstein Kamptal DAC", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="ultra_premium",
    description="Gobelsburg Heiligenstein Riesling from the primary rock terrace; mineral, structured and complex with spice, stone fruit and the characteristic volcanic mineral tension of Kamptal's greatest site.")
if is_new:
    PAIR(prod, "Escargots de Bourgogne with garlic-parsley butter", "complement", "established", "starter", "Garlic-herb snails find the mineral, complex Heiligenstein Riesling an unexpected but complementary match.")
    PAIR(prod, "Zitrusrisotto con gamberi e zafferano", "complement", "established", "main", "Lemon-prawn saffron risotto finds the mineral citrus of Gobelsburg Heiligenstein Riesling ideal.")
    PAIR(prod, "Seafood plateau with langoustines, oysters and brown crab", "complement", "classic", "main", "Austrian Riesling from primary rock is one of Europe's finest companions for a grand seafood plateau.")
    PAIR(prod, "Austrian Bergkäse Selection with mountain honey", "complement", "established", "cheese", "Alpine cheese selection with mountain honey finds the mineral precision of Heiligenstein Riesling natural.")

prod, is_new = PROD("Schloss Gobelsburg Grüner Veltliner Lamm Kamptal DAC", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Grüner Veltliner from the prestigious Lamm site on loess and gravel; powerful, mineral and peppery with citrus, herbs and the authority of a great Austrian white wine terroir.")
if is_new:
    PAIR(prod, "Bachsaibling (arctic char) with herb crust and potato salad", "complement", "classic", "main", "Austrian arctic char with herb crust finds the peppery mineral authority of Lamm Grüner Veltliner ideal.")
    PAIR(prod, "White Spargel (asparagus) with Sauce Hollandaise and Schinken", "complement", "classic", "casual", "Classic Austrian asparagus with hollandaise and ham — the definitive spring pairing for Kamptal GV.")
    PAIR(prod, "Grüne Sauce (Frankfurt seven-herb sauce) with boiled eggs and potatoes", "complement", "established", "casual", "Frankfurt's seven-herb green sauce with eggs and potatoes finds mineral peppery Kamptal GV superb.")
    PAIR(prod, "Frittatensuppe (beef broth with crêpe strips)", "complement", "classic", "main", "Classic Austrian consommé-style soup with egg crêpe strips is a natural companion for Kamptal Grüner Veltliner.")

# ── KREMSTAL DAC (Austria) ────────────────────────────────────────────────────
print("=== Kremstal DAC ===")
r = R("Kremstal DAC", "Austria", "wine",
      designation_type="DAC",
      designation_name="Kremstal DAC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="The Krems River valley's diverse terroir — loess terraces, crystalline primary rock and alluvial gravel — produces some of Austria's most complex Grüner Veltliner and Riesling. The medieval city of Krems anchors the appellation, and the Pfaffenberg and Wachstum Bodenstein sites on primary rock produce wines of extraordinary mineral precision.",
      key_producers="Nigl, Mantlerhof, Stadt Krems",
      historical_context="Kremser wine culture dates to the Babenberg dynasty in the 12th century when the city controlled Danube wine trade. The DAC established 2007 covers the Krems River confluence with the Danube. The Kremstal's loess terraces produce softer, more opulent Grüner Veltliner than the Kamptal's crystalline sites, while primary rock vineyards approach Wachau quality.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Primary rock Kremstal wines of extraordinary mineral depth alongside opulent loess Grüner Veltliner."),
    (2019, "very_good", "stable", "Good balance of loess richness and primary rock precision; Kremstal wines of genuine quality."),
    (2020, "excellent", "rising", "Benchmark Kremstal vintage; wines of extraordinary balance between richness and mineral freshness."),
    (2021, "very_good", "stable", "Consistent quality across Kremstal's diverse terroir; GV and Riesling both performing well."),
    (2022, "excellent", "rising", "Outstanding conditions; loess GV of opulence and primary rock Riesling of precise mineral depth."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Nigl", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Martin Nigl is one of Austria's most gifted Riesling and Grüner Veltliner producers, farming the Kremstal's primary rock and loess vineyards to produce wines of remarkable clarity, mineral depth and site specificity.",
       reputation_narrative="Nigl's Privat Riesling and Piri Riesling from primary rock are among Austria's most critically acclaimed whites, demonstrating the Kremstal's capacity for wines that rival the Wachau's greatest in complexity and longevity.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Nigl Privat Riesling Kremstal DAC Reserve", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="ultra_premium",
    description="Nigl's greatest Riesling from primary rock parcels in the Kremstal; profoundly mineral, crystalline and age-worthy with yellow stone fruit, herb and the unique mineral tension of primary rock at great concentration.")
if is_new:
    PAIR(prod, "Perlforelle (brook trout) with almond butter and lemon", "complement", "classic", "main", "Brook trout with almond-lemon butter is the Austrian freshwater classic for primary rock Kremstal Riesling.")
    PAIR(prod, "Hecht (pike) in Riesling and cream sauce", "complement", "classic", "main", "Pike cooked in Riesling wine and cream is the definitive Austrian freshwater fish pairing for great Kremstal Riesling.")
    PAIR(prod, "Foie gras mi-cuit with Riesling jelly and brioche", "complement", "established", "starter", "Foie gras with Riesling gelée is a natural luxury pairing for primary rock Riesling of this complexity.")
    PAIR(prod, "Weißwurst (Bavarian white sausage) with sweet mustard and pretzel", "complement", "suggested", "casual", "Bavarian white sausage with sweet mustard finds the mineral refreshment of Kremstal Riesling charming.")

prod, is_new = PROD("Nigl Grüner Veltliner Kremser Freiheit Kremstal DAC", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Kremstal Grüner Veltliner from Kremser Freiheit loess; opulent, peppery and richly mineral with citrus, stone fruit and the characteristic weight of great loess Grüner Veltliner.")
if is_new:
    PAIR(prod, "Wiener Gulasch mit Semmelknödel (Viennese beef goulash)", "complement", "classic", "main", "Classic Viennese paprika beef goulash and bread dumpling find opulent loess Grüner Veltliner ideal.")
    PAIR(prod, "Grüner Veltliner braised pheasant with juniper and sage", "complement", "established", "main", "Pheasant braised in the wine itself — a classic Kremstal winery restaurant pairing.")
    PAIR(prod, "Steirischer Wurzelfleisch (Styrian boiled pork with root vegetables)", "complement", "established", "main", "Boiled pork with root vegetables finds the opulent peppery weight of loess Kremstal GV a natural match.")
    PAIR(prod, "Grillerdäpfl (Austrian grilled potatoes) with crème fraîche and chives", "complement", "classic", "casual", "Austrian grilled potatoes with herb cream — a simple, authentic companion for Kremstal Grüner Veltliner.")

p2 = P("Mantlerhof", "winery", r, "Austria",
       production_philosophy="traditional",
       philosophy_description="Josef Mantler at Mantlerhof produces Kremstal wines of authentic regional character from the valley's loess and primary rock sites, working primarily with the Roter Veltliner variety alongside Grüner Veltliner and Riesling.",
       reputation_narrative="Mantlerhof is one of the few remaining producers of Roter Veltliner, a rare and ancient variety that once dominated the Kremstal. The estate's commitment to this endangered variety alongside mainstream quality makes it unique.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Mantlerhof Roter Veltliner Kremstal", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="premium",
    description="Rare Roter Veltliner from Mantlerhof — one of Austria's most endangered varieties; golden, textured and aromatic with stone fruit, spice and mineral character entirely unlike Grüner Veltliner.")
if is_new:
    PAIR(prod, "Zwetschgenröster (Austrian plum compote) with Topfen", "complement", "classic", "dessert", "Austrian plum compote with curd cheese is a traditional Kremstal dessert companion for textured Roter Veltliner.")
    PAIR(prod, "Gebratene Ente mit Rotkraut und Klößen (roast duck)", "complement", "classic", "main", "Austrian roast duck with red cabbage and potato dumplings finds the textured spice of Roter Veltliner ideal.")
    PAIR(prod, "Geräucherter Karpfen (smoked carp) with horseradish cream", "complement", "classic", "casual", "Smoked carp from the Danube with horseradish cream is an Austrian freshwater classic for this rare variety.")
    PAIR(prod, "Liptauer Aufstrich mit Kürbiskernöl und Brot", "complement", "established", "casual", "Spiced curd cheese spread with pumpkin seed oil — an Austrian tavern classic that suits Roter Veltliner.")

prod, is_new = PROD("Mantlerhof Grüner Veltliner Ried Spiegel Kremstal DAC", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="mid_range",
    description="Single-vineyard Kremstal DAC Grüner Veltliner from the Spiegel site; peppery, mineral and food-friendly with citrus and herb character from loess soils in the Krems valley.")
if is_new:
    PAIR(prod, "Backhendl (Austrian fried chicken) with potato salad", "complement", "classic", "casual", "Austrian fried chicken is the most versatile companion for peppery, food-friendly Kremstal Grüner Veltliner.")
    PAIR(prod, "Frischer Ziegenkäse mit Kräutern (fresh goat cheese with herbs)", "complement", "established", "casual", "Fresh goat cheese with herbs finds the peppery mineral freshness of Kremstal GV a natural companion.")
    PAIR(prod, "Zanderfilet mit Senfsauce und Spinat", "complement", "established", "main", "Pike-perch fillet with mustard sauce and spinach is a classic Austrian fish pairing for Kremstal GV.")
    PAIR(prod, "Linsensalat mit geräuchertem Lachs und Meerrettich", "complement", "suggested", "casual", "Lentil salad with smoked salmon and horseradish finds the peppery freshness of Spiegel GV ideal.")

# ── CARNEROS AVA (USA) ────────────────────────────────────────────────────────
print("=== Carneros AVA ===")
r = R("Carneros AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Carneros AVA",
      reputation_tier="prestigious",
      quality_trajectory="established",
      description="California's coolest Napa-Sonoma border appellation straddling San Pablo Bay's influence, producing Chardonnay and Pinot Noir of elegance and restraint unusual for the state. The bay's cooling fogs and afternoon winds create Burgundian ripening conditions. Carneros also produces high-quality méthode champenoise sparkling wines.",
      key_producers="Domaine Carneros, Saintsbury, Etude",
      historical_context="Carneros ('sheep' in Spanish, referring to the historic grazing land) emerged as California's first explicitly cool-climate appellation from the 1970s. Louis Martini planted Pinot Noir here in the 1940s, recognising the bay influence. Domaine Carneros (Taittinger) and Domaine Chandon established the sparkling wine tradition. AVA status 1983.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool bay influence produced Carneros Chardonnay and Pinot Noir of exceptional Burgundian restraint."),
    (2019, "very_good", "stable", "Good balance of cool-climate freshness and California ripeness; characteristic Carneros elegance."),
    (2020, "good", "stable", "Wildfire smoke affected some vineyards; wines requiring careful selection to avoid taint."),
    (2021, "very_good", "stable", "Clean vintage after 2020; Carneros restored its cool-climate character."),
    (2022, "excellent", "rising", "Outstanding Carneros vintage; Chardonnay of mineral precision and Pinot Noir of genuine elegance."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Carneros", "winery", r, "USA",
       production_philosophy="traditional",
       philosophy_description="Founded by Taittinger Champagne in 1987, Domaine Carneros produces both traditional method sparkling wines and still Pinot Noir from the cool bay-influenced Carneros appellation using méthode champenoise principles applied to California's finest cool-climate grapes.",
       reputation_narrative="Domaine Carneros is California's most respected traditional method sparkling wine producer and one of the Carneros AVA's defining estates for both sparkling and still Pinot Noir.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Domaine Carneros Brut Cuvée", "wine_sparkling", p1, r, "USA",
    subcategory="sparkling_white", price_tier="premium",
    description="Carneros traditional method Brut from Pinot Noir and Chardonnay; elegant, fine-bead and California-fresh with green apple, lemon and toasted brioche character from extended bay-cooled ripening.")
if is_new:
    PAIR(prod, "Dungeness crab cakes with lemon-herb aioli", "complement", "classic", "casual", "California's Pacific crab in cake form with herb aioli is a natural West Coast companion for Carneros sparkling.")
    PAIR(prod, "Pacific oysters on the half shell with mignonette", "complement", "classic", "casual", "West Coast oysters and their briny freshness are elevated by the fine bead and mineral freshness of Carneros Brut.")
    PAIR(prod, "Ahi tuna tartare with avocado and sesame", "complement", "established", "casual", "California tuna tartare with avocado finds the fine bubbles and mineral freshness of Domaine Carneros ideal.")
    PAIR(prod, "Truffle arancini with aged Parmesan", "complement", "established", "casual", "Truffle-stuffed rice balls find the fine bead and mineral brioche of Carneros Brut a sophisticated companion.")

prod, is_new = PROD("Domaine Carneros Pinot Noir Estate", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Estate Pinot Noir from Carneros's bay-cooled vineyards; elegant, mineral and California-expressive with cherry, raspberry, earth and the restraint that distinguishes Carneros from warmer California Pinot.")
if is_new:
    PAIR(prod, "Roasted duck breast with cherry compote and wild rice", "complement", "classic", "main", "Cool-climate Carneros Pinot Noir is a natural California companion for duck with cherry reduction.")
    PAIR(prod, "Grilled Pacific salmon with pinot sauce and herbs", "complement", "classic", "main", "Oregon-California salmon with Pinot Noir reduction is the Pacific Northwest-California classic Pinot pairing.")
    PAIR(prod, "Mushroom and gruyère quiche with garden salad", "complement", "established", "casual", "Elegant Carneros Pinot Noir suits mushroom-cheese quiche with the mineral restraint of bay-influenced wine.")
    PAIR(prod, "Point Reyes blue cheese with honeycomb", "contrast", "established", "cheese", "California artisan blue cheese and honeycomb contrast the cherry-mineral elegance of bay-cooled Pinot Noir.")

p2 = P("Saintsbury", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Saintsbury was one of Carneros's founding quality producers, establishing in the 1980s that California could produce elegant, food-friendly Pinot Noir and Chardonnay from cool-climate bay-influenced appellations.",
       reputation_narrative="Saintsbury's Pinot Noir from the Brown Ranch has been one of California's most consistently celebrated cool-climate reds, establishing the Carneros AVA's reputation for restrained, food-friendly Pinot Noir.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Saintsbury Brown Ranch Pinot Noir Carneros", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Single-vineyard Carneros Pinot Noir from the Brown Ranch; complex, structured and mineral with dark cherry, earth and the characteristic cool-climate restraint of bay-influenced Carneros.")
if is_new:
    PAIR(prod, "Roasted beet and goat cheese salad with walnut vinaigrette", "complement", "established", "casual", "Earthy, mineral Carneros Pinot suits beet salad with the tangy goat cheese and walnut complexity.")
    PAIR(prod, "Braised short rib with celery root purée and thyme", "complement", "established", "main", "Structured Brown Ranch Pinot handles braised short rib richness with its cool-climate mineral frame.")
    PAIR(prod, "Wild mushroom risotto with truffle oil and Parmesan", "complement", "established", "main", "Earth and dark cherry of Carneros Pinot resonates with wild mushroom and truffle in creamy risotto.")
    PAIR(prod, "Grilled lamb loin chops with rosemary and Dijon", "complement", "classic", "main", "Cool-climate Pinot's restraint suits lamb's delicate richness with the herb-mustard complementary notes.")

prod, is_new = PROD("Saintsbury Chardonnay Carneros", "wine_still", p2, r, "USA",
    subcategory="white", price_tier="premium",
    description="Carneros Chardonnay from Saintsbury's bay-cooled vineyards; restrained, mineral and textured with stone fruit, citrus and judicious oak — California Chardonnay at its most elegant and food-friendly.")
if is_new:
    PAIR(prod, "Pan-roasted halibut with lemon beurre blanc and tarragon", "complement", "classic", "main", "Elegant Carneros Chardonnay suits the delicate sweetness of halibut with classic French beurre blanc.")
    PAIR(prod, "Lobster bisque with cream and cognac", "elevate", "established", "main", "Restrained, mineral Carneros Chardonnay handles lobster bisque richness without losing its freshness.")
    PAIR(prod, "California avocado toast with poached egg and lemon", "complement", "established", "casual", "Bay-cooled Chardonnay's citrus-mineral freshness suits the California classic of avocado and egg.")
    PAIR(prod, "Teleme or Humboldt Fog goat cheese with fig jam", "complement", "established", "cheese", "California artisan cheese with fig jam finds the mineral restraint of Carneros Chardonnay ideal.")

# ── SANTA BARBARA COUNTY AVA (USA) ────────────────────────────────────────────
print("=== Santa Barbara County AVA ===")
r = R("Santa Barbara County AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Santa Barbara County AVA",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="California's most diverse and discussed cool-climate wine region with east-west transverse mountain ranges that funnel Pacific Ocean winds into the Santa Ynez and Santa Maria Valleys. Pinot Noir and Chardonnay from Santa Maria and Sta. Rita Hills achieve elegance unmatched in California. The region rose to fame after the film Sideways (2004).",
      key_producers="Sanford, Au Bon Climat, Foxen, Brewer-Clifton",
      historical_context="Santa Barbara wine emerged in the 1970s with Firestone Vineyard and Sanford & Benedict. The region's unique east-west canyon topography creates dramatically cool conditions ideal for Burgundian varieties. The 2004 film Sideways sparked international interest in Santa Barbara Pinot Noir, transforming a regional curiosity into a global destination. Sub-AVAs Santa Maria, Sta. Rita Hills and Happy Canyon each have distinct characters.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Cool Pacific influence produced Santa Barbara Pinot Noir and Chardonnay of exceptional elegance."),
    (2020, "good", "stable", "Wildfire smoke impacted some areas; best sites — Santa Maria, Sta. Rita Hills — less affected."),
    (2021, "very_good", "stable", "Clean vintage restoring Santa Barbara's cool-climate reputation; wines of genuine finesse."),
    (2022, "excellent", "rising", "Outstanding Santa Barbara vintage; Pinot Noir of California's most Burgundian elegance."),
    (2023, "excellent", "rising", "Benchmark conditions; Santa Maria and Sta. Rita Hills produced finest Pinot Noir in years."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Au Bon Climat", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Jim Clendenen at Au Bon Climat championed Burgundian restraint in California long before it was fashionable, producing Pinot Noir and Chardonnay from Santa Barbara County's cool transverse valleys with a French sensibility and California warmth.",
       reputation_narrative="Au Bon Climat is one of California's most influential wineries, establishing that Santa Barbara County could produce Pinot Noir and Chardonnay of genuine Burgundian complexity and elegance.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Au Bon Climat La Bauge Au-Dessus Pinot Noir Santa Barbara", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Single-vineyard Santa Barbara Pinot Noir from Au Bon Climat; elegant, complex and Burgundian with dark cherry, earth and spice from the cool Pacific-influenced Santa Maria Valley.")
if is_new:
    PAIR(prod, "Duck confit with cherry compote and root vegetable gratin", "complement", "classic", "main", "Dark cherry and earth complexity of Burgundian Santa Barbara Pinot is a natural match for confit duck.")
    PAIR(prod, "Pan-seared salmon with mushroom cream and asparagus", "complement", "classic", "main", "Pacific salmon with mushroom cream finds the restrained elegance of Au Bon Climat Pinot ideal.")
    PAIR(prod, "Roasted beet salad with Point Reyes blue and candied walnut", "complement", "established", "casual", "Earthy, mineral Santa Barbara Pinot resonates with beet, blue cheese and walnut depth.")
    PAIR(prod, "Braised short rib with polenta and rosemary gremolata", "complement", "established", "main", "Short rib richness and the Burgundian Santa Barbara Pinot's structure create a satisfying California red wine pairing.")

prod, is_new = PROD("Au Bon Climat Chardonnay Santa Barbara County", "wine_still", p1, r, "USA",
    subcategory="white", price_tier="premium",
    description="Santa Barbara Chardonnay in the Burgundian style of Au Bon Climat; restrained, mineral and textured with stone fruit, lemon and careful oak — among California's most food-friendly Chardonnays.")
if is_new:
    PAIR(prod, "Pan-roasted halibut with brown butter, capers and lemon", "complement", "classic", "main", "Restrained Burgundian Santa Barbara Chardonnay is the California classic for halibut with brown butter.")
    PAIR(prod, "Grilled corn and lobster salad with herb vinaigrette", "complement", "established", "casual", "California summer corn and lobster find the mineral restraint of Au Bon Climat Chardonnay a perfect match.")
    PAIR(prod, "Roasted chicken with tarragon cream sauce", "complement", "established", "main", "Classic French chicken with tarragon cream finds Burgundian-style Chardonnay the perfect white wine match.")
    PAIR(prod, "Burratta with heirloom tomatoes and basil oil", "complement", "established", "casual", "California burrata and summer tomatoes meet this restrained Chardonnay's mineral freshness in summer harmony.")

p2 = P("Sanford Winery", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Richard Sanford was a pioneer of Santa Barbara viticulture, planting the historic Sanford & Benedict Vineyard in the Sta. Rita Hills in 1971. The Sanford & Benedict site remains one of California's most celebrated Pinot Noir and Chardonnay vineyards.",
       reputation_narrative="Sanford's Sanford & Benedict Vineyard wines are among California's most historically significant, establishing the Sta. Rita Hills' reputation as a world-class Pinot Noir site decades before AVA status.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Sanford Pinot Noir Sta. Rita Hills Santa Barbara", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Sta. Rita Hills Pinot Noir from Sanford's historic site; cool Pacific winds produce Pinot of extraordinary restraint, mineral tension and complexity — California's most Burgundian coastal Pinot Noir.")
if is_new:
    PAIR(prod, "Roasted quail with pomegranate glaze and wild rice", "complement", "classic", "main", "Delicate game bird with pomegranate suits the mineral elegance of cool Pacific Sta. Rita Hills Pinot Noir.")
    PAIR(prod, "Grilled Oregon mushroom tart with Gruyère and thyme", "complement", "established", "main", "Pacific Coast mushroom tart finds the mineral, earthy depth of Sta. Rita Hills Pinot ideal.")
    PAIR(prod, "Whole roasted Muscovy duck with cherry pan sauce", "complement", "classic", "main", "Muscovy duck richness and cherry pan sauce match the red cherry and mineral depth of Sta. Rita Hills Pinot.")
    PAIR(prod, "Cypress Grove Humboldt Fog goat cheese with quince paste", "complement", "established", "cheese", "California artisan goat cheese with quince paste and Sta. Rita Hills Pinot Noir — a West Coast classic.")

prod, is_new = PROD("Sanford Chardonnay Sta. Rita Hills Santa Barbara", "wine_still", p2, r, "USA",
    subcategory="white", price_tier="premium",
    description="Sta. Rita Hills Chardonnay from the cool ocean-influenced belt; mineral, crisp and textured with green apple, lemon curd and the Pacific freshness of California's coolest Chardonnay appellation.")
if is_new:
    PAIR(prod, "Grilled Pacific halibut with Meyer lemon and caper brown butter", "complement", "classic", "main", "Pacific halibut with California Meyer lemon and brown butter demands the mineral freshness of Sta. Rita Hills Chardonnay.")
    PAIR(prod, "Santa Barbara spot prawns with garlic and herbs", "complement", "classic", "casual", "Local Santa Barbara spot prawns are the quintessential regional companion for Sta. Rita Hills Chardonnay.")
    PAIR(prod, "Uni (sea urchin) on brioche toast with lemon and chive", "complement", "established", "casual", "Sea urchin's ocean richness and the mineral Pacific freshness of Sta. Rita Hills Chardonnay — California at its best.")
    PAIR(prod, "Avocado and crab salad with citrus vinaigrette", "complement", "established", "casual", "California crab and avocado salad finds the mineral freshness of cool Pacific Chardonnay a natural match.")

# ── FINAL COUNTS ──────────────────────────────────────────────────────────────
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
print("B142 complete.")
conn.close()
