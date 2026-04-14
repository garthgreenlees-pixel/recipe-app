#!/usr/bin/env python3
"""B141 — Tokaj (Hungary supplement), Villány (Hungary supplement),
   Eger (Hungary supplement), Weinviertel DAC (Austria),
   Burgenland (Neusiedlersee DOC Austria / Ruster Ausbruch)
All constraints verified from B136-B140.
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

# ── TOKAJ (Hungary) supplements ───────────────────────────────────────────────
print("=== Tokaj ===")
r = R("Tokaj", "Hungary", "wine",
      designation_type="PDO",
      designation_name="Tokaj PDO",
      reputation_tier="iconic",
      quality_trajectory="ascending",
      description="Hungary's most celebrated wine region producing the world's first classified wines (1730) and the legendary Aszú sweet wines from Botrytis-affected Furmint. Tokaj Aszú Eszencia can achieve sugar levels above 800g/L and age for centuries. Dry Furmint has emerged as one of the world's most distinctive white varieties with mineral, smoky and quince character.",
      key_producers="Royal Tokaj, Disznókő, Oremus, Hetszolo",
      historical_context="Tokaj wine was first classified by quality in 1730 under Charles III, predating Burgundy's grand cru system by over a century. Louis XIV called it 'Vinum Regum, Rex Vinorum' (wine of kings, king of wines). The 1989 fall of communism allowed international investment to restore Tokaj's international reputation. Puttonyos measures Aszú concentration from 3 to 6 puttonyos.")
for yr, qd, pt, sn in [
    (2017, "excellent", "rising", "Outstanding Aszú conditions with textbook botrytis; Eszencia of extraordinary concentration."),
    (2018, "very_good", "stable", "Good botrytis development; Aszú wines of characteristic apricot concentration and acid tension."),
    (2019, "excellent", "rising", "Benchmark dry Furmint vintage; mineral, smoky whites of extraordinary freshness and precision."),
    (2020, "very_good", "stable", "Good balance of dry and sweet styles; Furmint of genuine complexity."),
    (2021, "excellent", "rising", "Outstanding conditions for both dry Furmint and botrytised Aszú wines of benchmark quality."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Disznókő", "winery", r, "Hungary",
       production_philosophy="terroir_focused",
       philosophy_description="Owned by AXA Millésimes, Disznókő is one of Tokaj's most consistent premier cru estates, farming the First Growth Disznókő vineyard with meticulous attention to botrytis development and producing Aszú wines of benchmark quality and international recognition.",
       reputation_narrative="Disznókő is one of Tokaj's most internationally recognised estates, producing Aszú wines that demonstrate the region's unique capacity for extraordinary sweet wines alongside excellent dry Furmint.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Disznókő Tokaji Aszú 6 Puttonyos", "wine_dessert", p1, r, "Hungary",
    subcategory="botrytis_sweet", price_tier="ultra_premium",
    description="Benchmark Tokaji Aszú 6 Puttonyos from the First Growth Disznókő vineyard; golden amber, intensely concentrated botrytised Furmint with apricot jam, orange peel, saffron, honey and extraordinary acid tension.")
if is_new:
    PAIR(prod, "Foie gras terrine with toasted brioche", "complement", "classic", "main", "The world's most celebrated sweet wine meets France's most luxurious product in a pairing of unchallenged classic status.")
    PAIR(prod, "Roquefort with pear, walnut and honey", "contrast", "classic", "cheese", "Aszú's sweet-acid tension contrasts with sharp Roquefort in the most powerful of sweet wine-blue cheese pairings.")
    PAIR(prod, "Crème brûlée with orange zest and cardamom", "complement", "established", "dessert", "Caramel-citrus crème brûlée finds perfect resonance with the apricot-orange peel sweetness of 6 Puttonyos.")
    PAIR(prod, "Peking duck with plum sauce and pancakes", "bridge", "established", "main", "Apricot-sweet Aszú bridges the lacquered duck and plum sauce with its combination of sweetness and acid tension.")

prod, is_new = PROD("Disznókő Tokaj Furmint Dry", "wine_still", p1, r, "Hungary",
    subcategory="white", price_tier="premium",
    description="Dry Furmint from Disznókő's First Growth vineyard; mineral, smoky and precise with quince, green apple and the characteristic volcanic mineral tension of great Tokaj Furmint.")
if is_new:
    PAIR(prod, "Goose liver pâté with apple and green pepper jelly", "complement", "established", "starter", "Mineral, smoky Furmint suits Hungarian goose liver in its lighter pâté form with apple-pepper counterpoint.")
    PAIR(prod, "Grilled pike-perch (fogas) with dill sauce", "complement", "classic", "main", "Lake Balaton's prized pike-perch with dill sauce is a natural Hungarian pairing for dry, mineral Furmint.")
    PAIR(prod, "Cream of asparagus soup with smoked paprika oil", "complement", "established", "starter", "Smoky Furmint's mineral character bridges cream of asparagus with the smoky paprika drizzle beautifully.")
    PAIR(prod, "Grilled camembert with cranberry and brioche", "complement", "suggested", "casual", "Mineral, quince-driven Furmint suits the rich camembert with the tartness of cranberry as counterpoint.")

p2 = P("Royal Tokaj", "winery", r, "Hungary",
       production_philosophy="traditional",
       philosophy_description="Founded with British investment by Hugh Johnson, Royal Tokaj was a pioneer of the post-communist Tokaj revival, establishing the principle that classified cru vineyards could produce distinctly different Aszú wines reflecting their terroir.",
       reputation_narrative="Royal Tokaj's single-vineyard Aszú wines from First and Second Growth sites established the modern benchmark for how Tokaj's great terroirs could be communicated to international wine lovers.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Royal Tokaj Mézes Mály Aszú 6 Puttonyos", "wine_dessert", p2, r, "Hungary",
    subcategory="botrytis_sweet", price_tier="ultra_premium",
    description="Tokaj's most celebrated First Growth single-vineyard Aszú; from the Mézes Mály ('honey badger') vineyard, luscious concentrated honey, apricot, saffron and mineral complexity with legendary acid balance.")
if is_new:
    PAIR(prod, "Foie gras d'oie rôti avec confiture d'abricots", "complement", "classic", "main", "Roast goose foie gras with apricot confiture and the honey-apricot concentration of First Growth Aszú.")
    PAIR(prod, "Stilton with dried apricot and hazelnut", "contrast", "classic", "cheese", "Blue-veined Stilton and dried apricot find their perfect sweet counterpart in Mézes Mály Aszú concentration.")
    PAIR(prod, "Mango and passionfruit soufflé", "complement", "established", "dessert", "Tropical fruit soufflé and its sauce mirrors the honey-tropical concentration of Hungary's greatest sweet wine.")
    PAIR(prod, "Duck liver parfait with Tokaji jelly and brioche", "complement", "classic", "starter", "Duck liver parfait traditionally served with Tokaji-gelée is the definitive regional appetiser pairing.")

prod, is_new = PROD("Royal Tokaj Tokaji Late Harvest Furmint", "wine_still", p2, r, "Hungary",
    subcategory="sweet_white", price_tier="premium",
    description="Late-harvest Furmint from Royal Tokaj; off-dry, aromatic and honeyed with quince, peach and mineral character — between dry Furmint and full Aszú in sweetness and complexity.")
if is_new:
    PAIR(prod, "Túrós rétes (Hungarian cottage cheese strudel)", "complement", "classic", "dessert", "Hungary's beloved cottage cheese strudel meets this off-dry Furmint in a wholly authentic Hungarian pairing.")
    PAIR(prod, "Apple tart with cream and cinnamon", "complement", "established", "dessert", "Apple-quince character of late harvest Furmint mirrors and suits an apple tart with cinnamon spice.")
    PAIR(prod, "Fresh goat cheese with peach and mint", "complement", "established", "casual", "Off-dry Furmint's peach-mineral character suits fresh goat cheese with summer stone fruit and mint.")
    PAIR(prod, "Grilled scallops with Hungarian paprika butter", "bridge", "suggested", "main", "Late-harvest Furmint bridges scallop sweetness and the sweet-smoky paprika butter in a complex pairing.")

# ── WEINVIERTEL DAC (Austria) ──────────────────────────────────────────────────
print("=== Weinviertel DAC ===")
r = R("Weinviertel DAC", "Austria", "wine",
      designation_type="DAC",
      designation_name="Weinviertel DAC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Austria's largest wine region north of Vienna, producing its finest Grüner Veltliner under the Weinviertel DAC designation. The loess, sand and limestone soils of this expansive flatland and gentle hill country produce Grüner Veltliner of characteristic peppery, mineral character at remarkable value. The DAC designation ensures authentic regional style.",
      key_producers="Bründlmayer (adjacent), Pfaffl, Zull",
      historical_context="Weinviertel means 'wine quarter' — a reflection of the region's centuries-long dominance of Austrian wine production. The DAC system (Districtus Austriae Controllatus) was introduced 2002, with Weinviertel as the first DAC. It requires characteristic Grüner Veltliner with the regional peppery-mineral character, distinguishing authentic Weinviertel style from more neutral wines.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Outstanding Grüner Veltliner vintage; peppery, mineral character of exceptional freshness."),
    (2020, "very_good", "stable", "Good loess-limestone conditions; DAC wines of characteristic pepper and citrus freshness."),
    (2021, "excellent", "rising", "Benchmark Weinviertel vintage; Grüner Veltliner of extraordinary peppery mineral precision."),
    (2022, "very_good", "stable", "Consistent DAC quality; food-friendly, peppery Grüner Veltliner throughout the region."),
    (2023, "excellent", "rising", "Superb Weinviertel conditions; DAC Grüner Veltliner of freshness and pepper precision."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Pfaffl", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Roman Pfaffl at Weingut Pfaffl is one of Weinviertel's leading quality producers, farming loess and sand vineyards with care to produce Grüner Veltliner and Riesling of genuine mineral character and DAC typicity.",
       reputation_narrative="Pfaffl is one of Weinviertel DAC's most respected producers, demonstrating that the region can produce Grüner Veltliner of genuine quality and terroir expression beyond simple everyday drinking.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Pfaffl Hundsleiten Grüner Veltliner Weinviertel DAC", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Weinviertel DAC Grüner Veltliner from loess soils; characteristic white pepper, citrus and mineral freshness with good mid-palate weight and the authentic peppery DAC finish.")
if is_new:
    PAIR(prod, "Wiener Schnitzel with lingonberry jam and cucumber salad", "complement", "classic", "main", "Austria's national dish — breaded veal escalope — is inseparable from peppery Grüner Veltliner.")
    PAIR(prod, "Tafelspitz (boiled prime beef) with chive sauce and roast potatoes", "complement", "classic", "main", "Vienna's classic boiled beef with its delicate broths and sauces finds peppery Grüner Veltliner the ideal match.")
    PAIR(prod, "Grüner asparagus with hollandaise and Schinkenbrot", "complement", "classic", "casual", "Austrian asparagus season is defined by the classic pairing of white pepper GV and white asparagus.")
    PAIR(prod, "Szegediner Gulasch (Viennese sauerkraut goulash with sour cream)", "complement", "established", "main", "Vienna's sauerkraut pork goulash with sour cream finds the peppery freshness of Weinviertel GV ideal.")

prod, is_new = PROD("Pfaffl Grüner Veltliner Weinviertel DAC", "wine_still", p1, r, "Austria",
    subcategory="white", price_tier="mid_range",
    description="Estate Weinviertel DAC Grüner Veltliner from Pfaffl; fresh, peppery and mineral with citrus and herb character — the authentic, food-friendly expression of Austria's signature grape.")
if is_new:
    PAIR(prod, "Beuschel (Viennese lung and heart ragout) with Semmelknödel", "complement", "established", "main", "Viennese offal ragout with bread dumpling is a natural Weinviertel Grüner Veltliner pairing.")
    PAIR(prod, "Gebackener Emmentaler (breaded Emmental cheese)", "complement", "established", "casual", "Fried cheese Viennese-style finds the peppery mineral freshness of entry Weinviertel GV ideal.")
    PAIR(prod, "Liptauer spread with caraway, pickled gherkins on dark bread", "complement", "classic", "casual", "The classic Austrian tavern snack of spiced curd cheese finds Grüner Veltliner its natural companion.")
    PAIR(prod, "Grilled Marchfelder Spargel (asparagus from Marchfeld flats)", "complement", "classic", "casual", "Weinviertel asparagus from the neighbouring Marchfeld flatlands with simple butter and GV pepper freshness.")

p2 = P("Zull", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Werner Zull farms loess and sand vineyards in the Weinviertel, producing Grüner Veltliner that showcases the different terroir expressions of Austria's largest wine region from light and peppery to more structured single-vineyard examples.",
       reputation_narrative="Zull is one of Weinviertel's quality producers, demonstrating the range of expression available from Grüner Veltliner across the region's diverse loess, sand and limestone soils.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Zull Grüner Veltliner Weinviertel DAC Klassik", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="mid_range",
    description="Crisp, peppery Weinviertel DAC Grüner Veltliner from Zull; fresh, citrus-bright and characteristically peppery from loess soils — excellent value expression of the Weinviertel's signature style.")
if is_new:
    PAIR(prod, "Erdäpfelsalat (Austrian potato salad with vinegar dressing)", "complement", "classic", "casual", "Austrian potato salad with its vinegary dressing finds the peppery citrus freshness of Weinviertel GV ideal.")
    PAIR(prod, "Grilled Brathuhn (Austrian roast chicken) with herbs", "complement", "classic", "casual", "Austrian-style roast chicken is one of the most food-friendly pairings for peppery Grüner Veltliner.")
    PAIR(prod, "Palatschinken mit Marillenmarmelade (crêpes with apricot jam)", "complement", "suggested", "dessert", "Light apricot-jam crêpes find the mineral freshness of peppery Grüner Veltliner a pleasant contrast.")
    PAIR(prod, "Topfenstrudel with vanilla sauce", "complement", "suggested", "dessert", "Austrian curd cheese strudel with vanilla sauce and peppery GV — an Austrian pairing of charming simplicity.")

prod, is_new = PROD("Zull Grüner Veltliner Vom Löss Weinviertel", "wine_still", p2, r, "Austria",
    subcategory="white", price_tier="mid_range",
    description="Loess-specific Grüner Veltliner from Zull; soft, rounded and textured from the distinctive loess soils with the region's characteristic white pepper and citrus freshness.")
if is_new:
    PAIR(prod, "Backerbsensuppe (Austrian fried bread-pearl soup)", "complement", "classic", "casual", "Traditional Viennese fried bread pearl soup finds the soft, rounded loess Grüner Veltliner natural.")
    PAIR(prod, "Fried Zander (pike-perch) with dill tartare sauce", "complement", "established", "main", "Fried freshwater fish with dill-herb sauce finds the rounded loess character of this GV ideal.")
    PAIR(prod, "Käsekrainer sausage with mustard and pretzel", "complement", "classic", "casual", "Austria's beloved cheese-filled sausage with mustard is the definitive tavern pairing for Weinviertel GV.")
    PAIR(prod, "Cauliflower gratin with smoked ham and Gruyère", "complement", "established", "main", "Rich cauliflower and ham gratin finds the peppery freshness of loess Grüner Veltliner an ideal foil.")

# ── NEUSIEDLERSEE (Burgenland, Austria) ───────────────────────────────────────
print("=== Neusiedlersee DAC ===")
r = R("Neusiedlersee DAC", "Austria", "wine",
      designation_type="DAC",
      designation_name="Neusiedlersee DAC",
      reputation_tier="respected",
      quality_trajectory="established",
      description="Burgenland's flat lake basin around the Neusiedlersee produces two distinct wine types: powerful, modern reds from Zweigelt and Blaufränkisch, and the unique botrytised Ruster Ausbruch dessert wines from Furmint, Welschriesling and other varieties on the ancient free city of Rust's vineyard terraces. The lake's mist creates ideal conditions for noble rot.",
      key_producers="Weingut Umathum, Ernst Triebaumer (Rust), Kollwentz",
      historical_context="Rust's winemakers were granted free city status by Emperor Leopold I in 1681 in exchange for 30,000 Goldfloren worth of wine — testament to the Ausbruch's historic value. The Neusiedlersee's unique microclimate, with autumn mist and then warm drying winds, makes it one of the world's most reliable regions for botrytised wine production.")
for yr, qd, pt, sn in [
    (2017, "excellent", "rising", "Outstanding botrytis conditions for Ausbruch production; extraordinary concentration and acid balance."),
    (2018, "very_good", "stable", "Good Zweigelt and Blaufränkisch reds of characteristic lake-basin warmth and dark fruit."),
    (2019, "excellent", "rising", "Benchmark vintage; exceptional Neusiedlersee reds of power and Ausbruch of concentration."),
    (2020, "very_good", "stable", "Consistent quality from the lake basin; Zweigelt of characteristic dark plum and spice."),
    (2021, "excellent", "rising", "Outstanding conditions; Neusiedlersee produced its finest Blaufränkisch and Ruster Ausbruch in a decade."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Weingut Umathum", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Josef Umathum is one of Burgenland's most respected producers, farming biodynamically beside the Neusiedlersee to produce Zweigelt, Blaufränkisch and St. Laurent of genuine complexity and the authentic warmth of the lake basin.",
       reputation_narrative="Umathum's wines, especially the Hallebühl and vom Stein single-vineyard Zweigelt, demonstrate that Burgenland's red varieties can achieve depth and longevity rivalling Austria's Wachau whites.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Umathum Hallebühl Zweigelt Neusiedlersee", "wine_still", p1, r, "Austria",
    subcategory="red", price_tier="premium",
    description="Single-vineyard biodynamic Zweigelt from the Hallebühl site beside the Neusiedlersee; dark plum, sour cherry, spice and fine tannin — one of Austria's finest expressions of the variety.")
if is_new:
    PAIR(prod, "Wiener Saftgulasch (Viennese beef goulash) with Semmelknödel", "complement", "classic", "main", "Vienna's paprika beef goulash with bread dumpling finds the spiced dark plum of lake-basin Zweigelt ideal.")
    PAIR(prod, "Grilled Blunzn (Austrian blood sausage) with sauerkraut", "complement", "classic", "casual", "Austrian blood sausage with sauerkraut is a natural Burgenland companion for warm, dark-fruited Zweigelt.")
    PAIR(prod, "Rindsuppe with Frittaten (beef broth with crêpe strips)", "complement", "established", "main", "Austrian beef broth with crêpe noodles finds the rounded warmth of biodynamic Zweigelt ideal.")
    PAIR(prod, "Steirisches Backhendl (Styrian fried chicken) with potato salad", "complement", "established", "casual", "Crispy fried chicken Austrian-style with vinegary potato salad suits the dark plum warmth of Zweigelt.")

prod, is_new = PROD("Umathum Frauenkirchen Zweigelt Neusiedlersee", "wine_still", p1, r, "Austria",
    subcategory="red", price_tier="mid_range",
    description="Estate Zweigelt from the lake basin; fresh, juicy and dark-fruited with characteristic Burgenland sour cherry, spice and smooth tannin — an accessible, food-friendly Austrian red.")
if is_new:
    PAIR(prod, "Paprikahendl (Hungarian-style paprika chicken with sour cream)", "complement", "classic", "main", "Paprika chicken with cream sauce is a classic lake-basin companion for Zweigelt's dark fruit and spice.")
    PAIR(prod, "Pizza bianca with Scamorza and Speck Alto Adige", "complement", "established", "casual", "Smoky ham and white pizza find the juicy dark-fruited warmth of Burgenland Zweigelt ideal.")
    PAIR(prod, "Grilled Mangalica pork chop with potato rösti", "complement", "established", "main", "Hungarian Mangalica pork and its rich fat suit the warm, smooth dark fruit of Neusiedlersee Zweigelt.")
    PAIR(prod, "Liptauer-topped Brettljause (Austrian charcuterie board)", "complement", "classic", "casual", "The Austrian tavern charcuterie board with spiced curd cheese finds Zweigelt its most natural companion.")

p2 = P("Kollwentz", "winery", r, "Austria",
       production_philosophy="terroir_focused",
       philosophy_description="Anton Kollwentz pioneered quality Burgenland red winemaking from the 1970s, producing Zweigelt, Blaufränkisch and Gloria single-vineyard wines that demonstrated the Neusiedlersee's potential for serious, complex reds.",
       reputation_narrative="Kollwentz's Gloria single-vineyard Zweigelt is one of Austria's most celebrated red wines, demonstrating the Neusiedlersee's capacity for wines of international quality and genuine terroir expression.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Kollwentz Gloria Zweigelt Neusiedlersee", "wine_still", p2, r, "Austria",
    subcategory="red", price_tier="ultra_premium",
    description="Kollwentz's iconic single-vineyard Zweigelt; concentrated, age-worthy and complex with dark plum, spice, tobacco and mineral depth — Austria's greatest expression of Zweigelt.")
if is_new:
    PAIR(prod, "Beef Wellington with Périgueux sauce and truffle", "complement", "established", "main", "Austria's greatest Zweigelt demands the luxury of beef Wellington with its truffle-enriched Périgueux.")
    PAIR(prod, "Roasted Barbary duck with cherry jus and red cabbage", "complement", "classic", "main", "Dark cherry character of Gloria Zweigelt mirrors the cherry jus and duck richness of this classic preparation.")
    PAIR(prod, "Zwiebelrostbraten (roast beef with onion gravy)", "complement", "classic", "main", "Vienna's roast beef with caramelised onion gravy is the most authentic pairing for Kollwentz's icon Zweigelt.")
    PAIR(prod, "Aged Vorarlberger Bergkäse with wild honey", "complement", "established", "cheese", "Aged Austrian mountain cheese with wild honey finds the complex mineral depth of Gloria Zweigelt ideal.")

prod, is_new = PROD("Kollwentz Blaufränkisch Neusiedlersee", "wine_still", p2, r, "Austria",
    subcategory="red", price_tier="premium",
    description="Kollwentz Blaufränkisch from the Neusiedlersee; structured, mineral and dark-fruited with characteristic Burgenland spice, dark berry and iron mineral character from the lake basin's volcanic and loess soils.")
if is_new:
    PAIR(prod, "Hirschgulasch (venison goulash with Preiselbeeren)", "complement", "classic", "main", "Austrian venison goulash with lingonberries is the definitive companion for structured Burgenland Blaufränkisch.")
    PAIR(prod, "Grilled Wildschweinstelze (wild boar knuckle) with sauerkraut", "complement", "established", "main", "Wild boar knuckle braised with sauerkraut demands the iron-mineral structure of Neusiedlersee Blaufränkisch.")
    PAIR(prod, "Sauerbraten (marinated pot roast) with Rotkraut and Klöße", "complement", "established", "main", "German-Austrian marinated pot roast with red cabbage and potato dumplings needs structured Blaufränkisch.")
    PAIR(prod, "Mostbröckl (Tyrolean air-dried beef) with radish and dark bread", "complement", "established", "casual", "Tyrolean air-dried beef with radish and rye bread is an Alpine salumi companion for mineral Blaufränkisch.")

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
print("B141 complete.")
conn.close()
