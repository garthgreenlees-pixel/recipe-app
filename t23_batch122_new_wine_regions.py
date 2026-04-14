import psycopg2
conn = psycopg2.connect("postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable")
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B122 ─────────────────────────────────────────────────────────────────────
# Targets: Wachau DAC (Austria), Kremstal DAC (Austria), Neusiedlersee DAC (Austria),
#          Rheingau (Germany), Mosel (Germany)

# 1. WACHAU DAC — Austria
print("=== Wachau DAC ===")
r1 = R("Wachau DAC", "Austria", "wine",
        designation_type="DAC",
        designation_name="Wachau DAC",
        reputation_tier="iconic",
        quality_trajectory="established",
        description="The Danube gorge between Melk and Krems produces Austria's most celebrated white wines on ancient terraced gneiss and primary rock. The unique Wachau ripeness classification (Steinfeder, Federspiel, Smaragd) replaced Germany's Prädikat system with a place-based approach. Smaragd (named after the local Emerald lizard) reaches full ripeness while retaining freshness. Grüner Veltliner and Riesling from Achleiten, Singerriedel and Kellerberg are world-class.",
        key_producers="Domäne Wachau, F.X. Pichler, Rudi Pichler, Prager, Knoll, Hirtzberger",
        historical_context="Wachau wine culture dates to Roman times and was preserved by Augustinian monks at Klosterneuburg. The Vinea Wachau growers' association was founded 1983, creating the Steinfeder/Federspiel/Smaragd classification unique to the region. Declared a UNESCO World Heritage Site in 2000.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"exceptional","rising")]:
    VIN(r1, yr, qd, pt, f"Wachau {yr}: Danube gorge; temperature variation creates exceptional aromatic precision")

p1a = P("F.X. Pichler", "winery", r1, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="The most celebrated Wachau estate; Riesling M from Loibenberg and Kellerberg Grüner are considered Austria's finest whites.",
        reputation_narrative="Franz Xavier Pichler is a legend of Austrian wine; his 'M' bottlings (Monumental) set the benchmark for Wachau Riesling and Grüner Veltliner worldwide.",
        price_positioning="ultra_premium")
pr1a1, n = PROD("F.X. Pichler Riesling Loibenberg Smaragd", "wine_still", p1a, r1, "Austria",
                subcategory="Riesling", price_tier="ultra_premium",
                description="Loibenberg Smaragd Riesling; volcanic gneiss minerality with peach, citrus and a 20-year ageing horizon.")
if n:
    PAIR(pr1a1, "Poached Danube pike with butter sauce", "complement", "classic", "main", "The great Austrian tradition: Wachau Riesling with Danube pike-perch")
    PAIR(pr1a1, "Wiener Schnitzel with lingonberry", "complement", "classic", "main", "Austria's national dish at its finest with Loibenberg Riesling")
    PAIR(pr1a1, "Marinated crayfish salad", "complement", "classic", "starter", "Freshwater crayfish and Riesling are Austria's definitive pairing")
    PAIR(pr1a1, "Roast chicken with tarragon cream", "complement", "established", "main", "Smaragd Riesling's weight and mineral precision frame herb-cream chicken")

pr1a2, n = PROD("F.X. Pichler Grüner Veltliner Kellerberg Smaragd", "wine_still", p1a, r1, "Austria",
                subcategory="Grüner Veltliner", price_tier="ultra_premium",
                description="Kellerberg Smaragd Grüner Veltliner; white pepper, grapefruit and extraordinary mineral depth from volcanic terraces.")
if n:
    PAIR(pr1a2, "Tafelspitz with apple-horseradish (apfelkren)", "complement", "classic", "main", "The canonical Austrian pairing: Grüner Veltliner Smaragd with Tafelspitz")
    PAIR(pr1a2, "White asparagus with ham and hollandaise", "complement", "classic", "main", "Grüner Veltliner's pepper-mineral defines the perfect asparagus wine")
    PAIR(pr1a2, "Grilled langoustines with herb butter", "complement", "established", "main", "Smaragd weight and mineral precision frame crustacean richness beautifully")
    PAIR(pr1a2, "Erdäpfelsuppe (potato soup) with chives", "complement", "established", "starter", "Wachau white pepper mineral is the natural match for Austrian potato soup")

p1b = P("Domäne Wachau", "winery", r1, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="The great Wachau cooperative; Achleiten and Singerriedel single-vineyard bottlings at accessible prices.",
        reputation_narrative="Formerly Freie Weingärtner Wachau, Domäne Wachau unites hundreds of growers; their Smaragd bottlings offer top sites at fair prices.",
        price_positioning="premium")
pr1b1, n = PROD("Domäne Wachau Riesling Achleiten Smaragd", "wine_still", p1b, r1, "Austria",
                subcategory="Riesling", price_tier="premium",
                description="Achleiten Smaragd Riesling; amphitheatre terraces of gneiss produce wines of electric precision and stony mineral.")
if n:
    PAIR(pr1b1, "Trout en papillote with dill and lemon", "complement", "classic", "main", "Alpine trout and Riesling mineral is the quintessential Austrian river valley combination")
    PAIR(pr1b1, "Smoked eel with horseradish cream", "complement", "established", "starter", "Riesling's acidity cuts through the richness of smoked eel")
    PAIR(pr1b1, "Marillenknödel (apricot dumplings)", "complement", "suggested", "dessert", "Wachau apricots and Riesling fruit create a regional taste of place")
    PAIR(pr1b1, "Grilled sea bass with herb oil", "complement", "established", "main", "Smaragd Riesling elevates any fine white fish with mineral precision")

pr1b2, n = PROD("Domäne Wachau Grüner Veltliner Federspiel", "wine_still", p1b, r1, "Austria",
                subcategory="Grüner Veltliner", price_tier="mid_range",
                description="Federspiel-level Grüner Veltliner; crisp, peppery and refreshing — the everyday Wachau table wine.")
if n:
    PAIR(pr1b2, "Fried chicken Viennese style", "complement", "established", "main", "Everyday Grüner cuts through breaded chicken with peppery freshness")
    PAIR(pr1b2, "Radishes and butter on bread", "complement", "classic", "amuse", "The most Austrian of combinations: crisp Grüner Veltliner with buttered radishes")
    PAIR(pr1b2, "Käsespätzle (cheese noodles)", "complement", "established", "main", "Peppery fresh Grüner cuts through the cheesy richness of Käsespätzle")
    PAIR(pr1b2, "Grilled zucchini and mixed vegetables", "complement", "established", "main", "Light peppery Grüner is ideal for vegetable-forward summer dishes")

# 2. KREMSTAL DAC — Austria
print("=== Kremstal DAC ===")
r2 = R("Kremstal DAC", "Austria", "wine",
        designation_type="DAC",
        designation_name="Kremstal DAC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Immediately downstream from the Wachau, Kremstal surrounds the ancient city of Krems at the mouth of the Krems valley. A mix of primary rock terraces (like Wachau) and loess plateau producing Grüner Veltliner and Riesling of great range and diversity. Sandgrube 13 and Kremser Kremsleiten are important single-vineyard sites. More varied in style than Wachau with both powerful and elegant expressions.",
        key_producers="Nigl, Salomon-Undhof, Stadt Krems, Mantlerhof",
        historical_context="Krems is one of Austria's oldest cities with documented wine production since the 12th century. The Kremstal DAC was created in 2007 with the Erste Lage classification recognising the district's best vineyard sites.")
for yr, qd, pt in [(2018,"very_good","rising"),(2019,"excellent","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r2, yr, qd, pt, f"Kremstal {yr}: diverse soils between primary rock and loess; Grüner and Riesling both excel")

p2a = P("Nigl", "winery", r2, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="The Kremstal's defining producer; single-vineyard Senftenberger Piri Riesling and Privat Grüner set the benchmark.",
        reputation_narrative="Martin Nigl transformed his family estate into one of Austria's most acclaimed properties; benchmark precision Riesling from primary rock.",
        price_positioning="premium")
pr2a1, n = PROD("Nigl Riesling Privat", "wine_still", p2a, r2, "Austria",
                subcategory="Riesling", price_tier="ultra_premium",
                description="Privat selection Riesling from best parcels; extraordinary tension with citrus, stone and mineral depth of great complexity.")
if n:
    PAIR(pr2a1, "Steamed cod with herb beurre blanc", "complement", "classic", "main", "Riesling's mineral-citrus precision mirrors and elevates the herb butter")
    PAIR(pr2a1, "Crab salad with avocado and citrus", "complement", "established", "starter", "Citrus-mineral Riesling lifts crab's delicate sweetness to extraordinary effect")
    PAIR(pr2a1, "Sweetbread with capers and lemon", "complement", "established", "main", "Riesling's acidity and mineral cut through the richness of sweetbread")
    PAIR(pr2a1, "Lobster bisque", "complement", "established", "starter", "The wine's intensity matches the rich concentration of bisque")

pr2a2, n = PROD("Nigl Grüner Veltliner Kremser Freiheit", "wine_still", p2a, r2, "Austria",
                subcategory="Grüner Veltliner", price_tier="mid_range",
                description="Entry Nigl Grüner; crisp white pepper, green herbs and fresh citrus — bright, mineral and versatile.")
if n:
    PAIR(pr2a2, "Grüner Veltliner dumpling soup (Nockerln)", "complement", "classic", "starter", "The grape's name in the dish; a circular Austrian flavour pairing")
    PAIR(pr2a2, "Fried whitebait with lemon aioli", "cleanse", "established", "starter", "Fresh peppery Grüner cleanses the palate between bites of fried fish")
    PAIR(pr2a2, "Asparagus risotto", "complement", "established", "main", "White pepper and herb character mirrors the asparagus-forward risotto")
    PAIR(pr2a2, "Sushi platter with pickled ginger", "complement", "established", "main", "Mineral Grüner is one of the best white wines for Japanese cuisine")

p2b = P("Salomon-Undhof", "winery", r2, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="Historic Kremstal estate with roots to 1792; Riesling Kögl and Pfaffenberg are signature single-vineyard sites.",
        reputation_narrative="Bertold Salomon's family estate; also produces exceptional Riesling from Fleurieu Peninsula in South Australia under Salomon Estate.",
        price_positioning="premium")
pr2b1, n = PROD("Salomon-Undhof Riesling Kögl", "wine_still", p2b, r2, "Austria",
                subcategory="Riesling", price_tier="premium",
                description="Kögl single-vineyard Riesling; elegantly structured with grapefruit, white flower and a long stony mineral finish.")
if n:
    PAIR(pr2b1, "Poached white fish with sorrel sauce", "complement", "classic", "main", "The citrus and mineral of Kögl Riesling elevates sorrel's lemony tartness")
    PAIR(pr2b1, "Gravlax with dill and mustard", "complement", "established", "starter", "Classic Scandinavian-Austrian crossover pairing; Riesling and cured salmon")
    PAIR(pr2b1, "Zander fillet with mushroom ragù", "complement", "established", "main", "Riesling mineral and grapefruit lifts this Danube freshwater fish")
    PAIR(pr2b1, "Käsekrainer sausage with mustard", "complement", "suggested", "main", "Austrian cheese-filled sausage is a casual companion for Kremstal Riesling")

pr2b2, n = PROD("Salomon-Undhof Grüner Veltliner Wieden", "wine_still", p2b, r2, "Austria",
                subcategory="Grüner Veltliner", price_tier="mid_range",
                description="Wieden single-vineyard Grüner; loess-influenced with ripe pear, white pepper and a creamy texture.")
if n:
    PAIR(pr2b2, "Backhendl (Viennese fried chicken)", "complement", "classic", "main", "Crispy Backhendl and Grüner Veltliner is a Viennese Sunday tradition")
    PAIR(pr2b2, "Semolina dumplings in beef broth", "complement", "established", "starter", "Loess-textured Grüner Veltliner rounds out the savoury depth of beef broth")
    PAIR(pr2b2, "Creamy mushroom pasta", "complement", "established", "main", "Pear and cream texture in Wieden Grüner complements mushroom pasta richness")
    PAIR(pr2b2, "Grilled vegetables with goat's cheese", "complement", "established", "main", "Fresh herb-pepper character complements charred vegetables and tangy cheese")

# 3. NEUSIEDLERSEE DAC — Austria
print("=== Neusiedlersee DAC ===")
r3 = R("Neusiedlersee DAC", "Austria", "wine",
        designation_type="DAC",
        designation_name="Neusiedlersee DAC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="The shallow steppe lake Neusiedlersee on the Hungarian border creates a unique microclimate producing Austria's finest Blaufränkisch, Zweigelt and sweet wines. The lake generates morning mists encouraging noble rot (Botrytis) for Trockenbeerenauslese and Ausbruch production. The Pannonian warmth also ripens full-bodied reds. Rust is famous for its Ausbruch sweet wines. Zweigelt dominates red production.",
        key_producers="Kracher, Umathum, Ernst Triebaumer, Paul Achs, Heinrich",
        historical_context="The Neusiedlersee region was the birthplace of Austrian sweet wine's international fame — Alois Kracher's TBA wines won global acclaim in the 1990s and 2000s. The border region was behind the Iron Curtain until 1989, accelerating Burgenland's quality revolution afterwards.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","stable"),(2021,"very_good","stable"),(2022,"excellent","stable")]:
    VIN(r3, yr, qd, pt, f"Neusiedlersee {yr}: lake mist encourages botrytis; Blaufränkisch shows warm Pannonian ripeness")

p3a = P("Kracher Winery", "winery", r3, "Austria",
        production_philosophy="traditional",
        philosophy_description="The world's reference for Austrian sweet wine; TBA and Ausbruch from Botrytis-affected lakeside vineyards.",
        reputation_narrative="Alois Kracher's TBA wines became Austria's most celebrated sweet wines; Gerhard Kracher continues his father's legacy to extraordinary acclaim.",
        price_positioning="ultra_premium")
pr3a1, n = PROD("Kracher TBA No.9 Zwischen den Seen", "wine_dessert", p3a, r3, "Austria",
                subcategory="Trockenbeerenauslese", price_tier="ultra_premium",
                description="Zwischen den Seen (Between the Lakes) TBA; extraordinary botrytised sweetness from lakeside vineyards — a world classic.")
if n:
    PAIR(pr3a1, "Sauternes-style foie gras terrine", "complement", "classic", "starter", "The Kracher TBA is to foie gras as Sauternes; a classic sweet-rich pairing")
    PAIR(pr3a1, "Époisses or aged Munster cheese", "contrast", "established", "cheese", "The wine's concentrated sweetness powerfully contrasts pungent washed-rind cheese")
    PAIR(pr3a1, "Quince paste and Manchego", "complement", "established", "cheese", "Botrytised sweetness echoes the membrillo's concentrated quince flavour")
    PAIR(pr3a1, "Peach Melba with vanilla ice cream", "complement", "established", "dessert", "Peachy TBA sweetness mirrors and elevates the classic peach-raspberry dessert")

pr3a2, n = PROD("Kracher Cuvée Auslese Burgenland", "wine_dessert", p3a, r3, "Austria",
                subcategory="Auslese", price_tier="premium",
                description="Entry Kracher Auslese; elegant botrytised sweetness with apricot, orange peel and honeyed depth.")
if n:
    PAIR(pr3a2, "Linzer Torte with raspberry jam", "complement", "classic", "dessert", "Austrian tradition: Auslese sweetness with the country's oldest cake recipe")
    PAIR(pr3a2, "Apricot and almond Sachertorte variation", "complement", "established", "dessert", "Apricot-honey Auslese mirrors the famous Viennese chocolate and apricot cake")
    PAIR(pr3a2, "Roquefort with walnut bread", "contrast", "classic", "cheese", "Classic sweet-salty combination of botrytised wine and pungent blue")
    PAIR(pr3a2, "Crème caramel with orange zest", "complement", "established", "dessert", "Caramel-orange Auslese finds natural harmony with the baked custard")

p3b = P("Umathum Winery", "winery", r3, "Austria",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Neusiedlersee estate; benchmark Blaufränkisch and Zweigelt from Pannonian red wine country.",
        reputation_narrative="Josef Umathum's biodynamic reds from Frauenkirchen are Burgenland's benchmark; Hallebühl Blaufränkisch is one of Austria's finest reds.",
        price_positioning="premium")
pr3b1, n = PROD("Umathum Blaufränkisch vom Stein", "wine_still", p3b, r3, "Austria",
                subcategory="Blaufränkisch", price_tier="premium",
                description="Vom Stein single-vineyard Blaufränkisch; dark cherry, graphite, violets and structured tannins of considerable elegance.")
if n:
    PAIR(pr3b1, "Esterhazy rostbraten (beef steak with sour cream)", "complement", "classic", "main", "Pannonian beef preparation and Blaufränkisch are Burgenland's great pairing")
    PAIR(pr3b1, "Wild duck with red cabbage and dumplings", "complement", "established", "main", "Graphite-structured Blaufränkisch complements game bird and braised cabbage")
    PAIR(pr3b1, "Veal goulash with egg noodles", "complement", "established", "main", "Dark-fruited Blaufränkisch is the natural companion for Central European goulash")
    PAIR(pr3b1, "Venison ragù with cranberry", "complement", "established", "main", "Graphite and cherry Blaufränkisch echoes venison's forest-floor depth")

pr3b2, n = PROD("Umathum Zweigelt Neusiedlersee", "wine_still", p3b, r3, "Austria",
                subcategory="Zweigelt", price_tier="mid_range",
                description="Classic Neusiedlersee Zweigelt; juicy cherry, spice and smooth tannins — approachable and charming.")
if n:
    PAIR(pr3b2, "Grilled bratwurst with sauerkraut", "complement", "established", "main", "Zweigelt's juicy cherry and spice are the natural companion for grilled sausage")
    PAIR(pr3b2, "Schnitzel sandwich (Schnitzelsemmel)", "complement", "established", "main", "Casual Zweigelt is the Austrians' everyday breaded meat sandwich wine")
    PAIR(pr3b2, "Beef burger with grilled onions", "complement", "established", "casual", "Fruit-forward Zweigelt is Austria's approachable all-purpose red")
    PAIR(pr3b2, "Roast chicken with paprika", "complement", "established", "main", "Cherry-spice Zweigelt complements paprika-rubbed roast chicken")

# 4. RHEINGAU — Germany
print("=== Rheingau ===")
r4 = R("Rheingau", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Rheingau",
        reputation_tier="prestigious",
        quality_trajectory="rediscovering",
        description="The south-facing Rhine bend between Wiesbaden and Rüdesheim is one of Germany's most historically important Riesling regions. Slate, quartzite and loam soils; sheltered by the Taunus mountains and warmed by Rhine reflection. The Grosses Gewächs (GG) classification from VDP producers represents the finest dry Riesling. Johannisberg, Steinberg and Rüdesheimer Berg Schlossberg are legendary sites. Also Germany's traditional home of Spätburgunder (Pinot Noir).",
        key_producers="Schloss Johannisberg, Robert Weil, Georg Breuer, Leitz, Küng",
        historical_context="The Rheingau's Benedictine monks at Johannisberg monastery documented the first German Spätlese in 1775. The region was Germany's most fashionable wine estate for centuries. VDP classification and a move to dry Grosses Gewächs has revived its global reputation.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Rheingau {yr}: south-facing Rhine bend; Riesling of exceptional structure and mineral length")

p4a = P("Robert Weil", "winery", r4, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="Kiedrich Gräfenberg is the Rheingau's finest site; Robert Weil produces benchmark dry GG and legendary sweet Riesling.",
        reputation_narrative="Wilhelm Weil has elevated the estate to Austria's gold standard; Kiedrich Gräfenberg TBA and GG are internationally the most sought-after Rheingau wines.",
        price_positioning="ultra_premium")
pr4a1, n = PROD("Robert Weil Kiedrich Gräfenberg Riesling GG", "wine_still", p4a, r4, "Germany",
                subcategory="Riesling Grosses Gewächs", price_tier="ultra_premium",
                description="Benchmark Rheingau GG from Gräfenberg; dry with crystalline mineral, lime zest and a 20-year ageing potential.")
if n:
    PAIR(pr4a1, "Steamed lobster with herb mayonnaise", "complement", "classic", "main", "GG Riesling's mineral precision and weight frames lobster's delicate sweetness")
    PAIR(pr4a1, "Sashimi of tuna and yellowtail", "complement", "established", "main", "Dry Rheingau Riesling is Germany's finest sushi partner")
    PAIR(pr4a1, "Sole meunière with capers", "complement", "classic", "main", "Citrus-mineral GG elevates butter-fried sole with perfect acidic counterpoint")
    PAIR(pr4a1, "Sauerkraut with smoked pork knuckle", "complement", "classic", "main", "The great Riesling-pork combination of the Rhine; acidity cuts through richness")

pr4a2, n = PROD("Robert Weil Rheingau Riesling Tradition", "wine_still", p4a, r4, "Germany",
                subcategory="Riesling", price_tier="premium",
                description="Entry Robert Weil Riesling; off-dry style with delicate peach, apricot and mineral freshness.")
if n:
    PAIR(pr4a2, "Thai green curry with jasmine rice", "complement", "established", "main", "Off-dry Riesling is Germany's definitive pairing for aromatic Asian cuisine")
    PAIR(pr4a2, "Spiced duck with mango chutney", "complement", "established", "main", "Riesling's sweetness and acidity frame spice-rubbed duck and mango perfectly")
    PAIR(pr4a2, "Pad see ew noodles", "complement", "established", "main", "Semi-sweet mineral Riesling is a revelatory pairing for Thai noodle dishes")
    PAIR(pr4a2, "Grilled pork ribs with honey glaze", "complement", "established", "main", "Off-dry Riesling's sweetness mirrors and tames the honey-glazed rib")

p4b = P("Georg Breuer", "winery", r4, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="Rüdesheim GG pioneer; Berg Schlossberg and Nonnenberg are Rheingau icons; advocate of dry Rheingau Riesling.",
        reputation_narrative="Theresa Breuer continues her father Bernhard's revolution; Georg Breuer was instrumental in championing dry GG Riesling over sweet styles.",
        price_positioning="premium")
pr4b1, n = PROD("Georg Breuer Berg Schlossberg Riesling GG", "wine_still", p4b, r4, "Germany",
                subcategory="Riesling Grosses Gewächs", price_tier="premium",
                description="Berg Schlossberg GG; volcanic blueschist soils produce a mineral, full-bodied dry Riesling with exceptional length.")
if n:
    PAIR(pr4b1, "Fried Schnitzel (pork or veal)", "complement", "classic", "main", "German tradition: dry mineral Riesling cuts through breaded meat beautifully")
    PAIR(pr4b1, "Sauerkraut with weisswurst", "complement", "classic", "main", "Rheingau Riesling is the Rhine's traditional partner for fermented pork sausage")
    PAIR(pr4b1, "Grilled sea bream with fennel", "complement", "established", "main", "Volcanic mineral GG elevates any delicate fish to fine-dining quality")
    PAIR(pr4b1, "Cheese fondue with crusty bread", "complement", "established", "main", "Dry acidic Riesling cuts through molten cheese richness perfectly")

pr4b2, n = PROD("Georg Breuer Rheingau Riesling Charm", "wine_still", p4b, r4, "Germany",
                subcategory="Riesling", price_tier="mid_range",
                description="Entry Breuer Riesling; fresh green apple, mineral and citrus at an accessible price — their entry-level ambassador wine.")
if n:
    PAIR(pr4b2, "Vietnamese bánh mì with pickled vegetables", "complement", "established", "main", "Fresh mineral Riesling is an outstanding pairing for pickled-vegetable sandwiches")
    PAIR(pr4b2, "Fish and chips with malt vinegar", "cleanse", "established", "main", "Crisp Riesling cleanses the richness of battered fish with each sip")
    PAIR(pr4b2, "Grilled chicken with lemon and herbs", "complement", "established", "main", "Citrus-fresh Riesling is versatile with herb-marinated chicken")
    PAIR(pr4b2, "Apple strudel (Apfelstrudel)", "complement", "classic", "dessert", "The German-Austrian tradition of Riesling and apple strudel is celebrated")

# 5. MOSEL — Germany
print("=== Mosel ===")
r5 = R("Mosel", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Mosel",
        reputation_tier="iconic",
        quality_trajectory="ascending",
        description="The steep blue slate vineyards of the Mosel, Saar and Ruwer rivers produce Germany's most celebrated Riesling. Extreme gradients (up to 70°) on Devonian blue and red slate; the river's reflection amplifies sunlight. Wines of ethereal delicacy, low alcohol and extraordinary ageing potential. The Prädikat system (Kabinett through Trockenbeerenauslese) codifies ripeness levels. Grosses Gewächs from the Bernkasteler Doctor, Wehlener Sonnenuhr and Scharzhofberg are legendary. Mosel Riesling at its best rivals any white wine in the world.",
        key_producers="Egon Müller, Joh. Jos. Prüm, Markus Molitor, Dönnhoff, Van Volxem",
        historical_context="Mosel Riesling was the world's most expensive white wine in the 19th century, selling for more than Burgundy's greatest. The region's extreme vineyards require entirely hand labour. Egon Müller's Scharzhofberger TBA remains one of the most expensive wines in the world at auction.")
for yr, qd, pt in [(2018,"exceptional","rising"),(2019,"excellent","rising"),(2020,"exceptional","rising"),(2021,"excellent","rising"),(2022,"exceptional","rising")]:
    VIN(r5, yr, qd, pt, f"Mosel {yr}: blue slate vineyards; Riesling of unmatched mineral precision and ageing potential")

p5a = P("Joh. Jos. Prüm", "winery", r5, "Germany",
        production_philosophy="traditional",
        philosophy_description="The reference estate of the Mosel Mittelmosel; Wehlener Sonnenuhr is the family's greatest site; long-lived Spätlese and Auslese.",
        reputation_narrative="Manfred Prüm's estate at Wehlen produces Germany's most revered Riesling Spätlese and Auslese; Wehlener Sonnenuhr Auslese is a world classic.",
        price_positioning="ultra_premium")
pr5a1, n = PROD("JJ Prüm Wehlener Sonnenuhr Riesling Spätlese", "wine_still", p5a, r5, "Germany",
                subcategory="Riesling Spätlese", price_tier="ultra_premium",
                description="The world benchmark for Riesling Spätlese; ethereal slate mineral with peach, citrus and off-dry delicacy; ages 20+ years.")
if n:
    PAIR(pr5a1, "Lobster bisque with cream and tarragon", "complement", "classic", "main", "The greatest Riesling Spätlese meets the greatest crustacean — a legendary pairing")
    PAIR(pr5a1, "Alsatian choucroute garnie", "complement", "classic", "main", "Germany's other great tradition: Riesling Spätlese with choucroute pork and sauerkraut")
    PAIR(pr5a1, "Moules marinières with cream", "complement", "established", "main", "Slate mineral and delicate sweetness lifts mussels in cream sauce beautifully")
    PAIR(pr5a1, "Aged Gruyère with honeycomb", "complement", "established", "cheese", "Off-dry Spätlese's delicate sweetness echoes the honeycomb beside aged cheese")

pr5a2, n = PROD("JJ Prüm Riesling Kabinett", "wine_still", p5a, r5, "Germany",
                subcategory="Riesling Kabinett", price_tier="premium",
                description="Kabinett from Sonnenuhr; featherweight delicacy at 8% alcohol with crisp apple, citrus and slate minerality.")
if n:
    PAIR(pr5a2, "Vietnamese pho with fresh herbs", "complement", "established", "main", "Kabinett's delicate sweetness and bright acidity pair beautifully with pho aromatics")
    PAIR(pr5a2, "Grilled trout with lemon and almonds", "complement", "classic", "main", "Lightweight Kabinett is the classic companion for delicate freshwater fish")
    PAIR(pr5a2, "Sushi rolls with cucumber and avocado", "complement", "established", "main", "Featherweight off-dry Riesling is an inspired sushi companion")
    PAIR(pr5a2, "Pear tarte tatin", "complement", "established", "dessert", "Kabinett's delicate pear and apple echoes the caramelised fruit of the tart")

p5b = P("Egon Müller-Scharzhof", "winery", r5, "Germany",
        production_philosophy="traditional",
        philosophy_description="Saarburg estate farming the mythical Scharzhofberg; Egon Müller IV produces the world's most expensive Riesling.",
        reputation_narrative="Scharzhofberger TBA by Egon Müller holds world auction records; the estate's Kabinett is considered the entry point to Germany's greatest Riesling terroir.",
        price_positioning="ultra_premium")
pr5b1, n = PROD("Egon Müller Scharzhofberger Riesling Spätlese", "wine_still", p5b, r5, "Germany",
                subcategory="Riesling Spätlese", price_tier="ultra_premium",
                description="Scharzhofberg Spätlese; ethereal Saar Riesling with citrus blossom, slate and unmatched tension; legendary 30+ year potential.")
if n:
    PAIR(pr5b1, "Terrine of foie gras with Sauternes jelly", "complement", "classic", "starter", "The great Saar Spätlese with foie gras is Germany's answer to Sauternes")
    PAIR(pr5b1, "Butter-poached sole with caviar", "complement", "classic", "main", "Germany's finest Riesling deserves the finest fish preparation")
    PAIR(pr5b1, "Lightly smoked wild salmon", "complement", "classic", "starter", "Scharzhofberg's ethereal mineral and citrus lifts delicate smoked salmon")
    PAIR(pr5b1, "Roquefort with quince paste", "complement", "established", "cheese", "Off-dry Saar Spätlese and pungent blue cheese is a celebrated combination")

pr5b2, n = PROD("Le Gallais Wiltinger Braune Kupp Riesling Kabinett", "wine_still", p5b, r5, "Germany",
                subcategory="Riesling Kabinett", price_tier="premium",
                description="From the Le Gallais parcel; featherweight Saar Kabinett with crystalline acidity and delicate off-dry fruit.")
if n:
    PAIR(pr5b2, "Steamed dim sum with soy dipping sauce", "complement", "established", "main", "Delicate off-dry Kabinett complements the subtle flavours of dim sum")
    PAIR(pr5b2, "Prawn cocktail with Marie Rose sauce", "complement", "established", "starter", "Refreshing off-dry Kabinett balances the richness of prawn cocktail sauce")
    PAIR(pr5b2, "Summer fruit pavlova", "complement", "suggested", "dessert", "Kabinett's delicate sweetness complements the meringue without overwhelming")
    PAIR(pr5b2, "Smoked mackerel pâté on toast", "complement", "established", "starter", "Riesling's mineral acidity cuts through the oily richness of smoked mackerel")

# Final counts
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

cur.close()
conn.close()
print("B122 complete.")
