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
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
        (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
        (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── REGION 1: Rias Baixas DO (Spain/Galicia) ─────────────────────────────────
print("\n=== Region 1: Rias Baixas ===")
r1 = R("Rias Baixas", "Spain", "wine",
    designation_type="DO", designation_name="Rías Baixas DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Rías Baixas is Spain's most celebrated white wine appellation, producing the benchmark Albariño wines in the rainy, Atlantic-influenced coastal rias (estuaries) of Galicia. The wines show extraordinary aromatic intensity — white peach, apricot, citrus peel, and white flowers — with a mineral salinity and crisp acidity that make them among Spain's most versatile food wines and ideally suited to the region's abundant seafood.",
    key_producers="Pazo de Señoráns, Álvaro Palacios (Ermita d'Espiells), Martín Códax, Do Ferreiro",
    historical_context="Albariño cultivation in Galicia dates to at least the 12th century, with Cistercian monks bringing cuttings from the Rhine Valley according to tradition (though genetic analysis suggests it is indigenous). The DO was established in 1988. The variety's dramatic quality revival in the 1980s-90s transformed it from a local curiosity to Spain's most internationally recognised white wine.")

VIN(r1, 2023, "excellent", "rising", "Outstanding Rias Baixas vintage; Albariño achieved exceptional aromatic concentration despite Atlantic rains with clean, mineral expression")
VIN(r1, 2022, "very_good", "stable", "Fine balanced year with characteristic Albariño freshness and stone fruit aromatics; good typicity")
VIN(r1, 2021, "good", "stable", "Wet year with higher than average disease pressure; careful viticulture yielded good aromatic freshness")
VIN(r1, 2020, "excellent", "rising", "Benchmark vintage; exceptional Albariño concentration and mineral salinity from the Atlantic rias terroir")
VIN(r1, 2019, "very_good", "rising", "Classic vintage with textbook Albariño character: white peach, citrus, mineral, and saline length")

prod1a_id = P("Pazo de Señoráns", "Spain", r1, "winery",
    "The benchmark single-estate Albariño producer in Rias Baixas; Marisol Bueno's estate in O Salnés produces both the standard Albariño and the extraordinary Selección de Añada — a late-release multi-vintage blend that ages magnificently for 15+ years, proving Albariño's longevity potential.")
prod1a, new1a = PROD("Pazo de Señoráns Albariño", "wine_still", prod1a_id, r1, "Spain",
    subcategory="white", price_tier="mid_range",
    description="The reference Rías Baixas Albariño: white peach, apricot blossom, citrus peel, and saline mineral from O Salnés's granite-based granitic soils. Fresh and immediate with excellent food versatility — consistently among Spain's finest whites at an honest price.")
if new1a:
    PAIR(prod1a, "Pulpo a la gallega (octopus with paprika, olive oil, and boiled potato)", "complement", "classic", "starter",
        "Galicia's iconic octopus dish and Albariño is the region's defining pairing; the wine's saline mineral and citrus acidity matches the paprika-dressed seafood perfectly")
    PAIR(prod1a, "Percebes (goose barnacles) simply cooked in sea water", "complement", "classic", "aperitif",
        "Galicia's luxury coastal delicacy — barnacles tasting of pure Atlantic ocean — are inseparable from local Albariño; the wine's brine mirrors the seafood exactly")
    PAIR(prod1a, "Grilled turbot (rodaballo) with lemon and Galician olive oil", "complement", "classic", "fish_course",
        "Turbot is Galicia's most prized fish; its firm white flesh and subtle sweetness are the ideal partner for Albariño's stone fruit and mineral precision")
    PAIR(prod1a, "Empanada gallega de atún with tomato and pepper", "complement", "established", "casual",
        "Galicia's ubiquitous tuna pastry is the everyday food pairing for local Albariño; the wine's freshness cuts through the pastry's richness")

prod1b_id = P("Do Ferreiro", "Spain", r1, "winery",
    "The most acclaimed artisan Albariño producer in Rias Baixas; Gerardo Méndez's biodynamic estate near Meaño produces old-vine, low-intervention Albariño from pre-phylloxera vines that show exceptional mineral depth and aging capability far beyond most examples.")
prod1b, new1b = PROD("Do Ferreiro Albariño Cepas Vellas", "wine_still", prod1b_id, r1, "Spain",
    subcategory="white", price_tier="premium",
    description="Do Ferreiro's old-vine Albariño from pre-phylloxera Cepas Vellas (Old Vines) — a direct expression of Rías Baixas's most profound terroir. Extraordinary mineral salinity, white peach depth, and a structure capable of 10-15 year aging. The most complete expression of Albariño's terroir potential.")
if new1b:
    PAIR(prod1b, "Almejas a la marinera (razor clams with white wine, garlic, and parsley)", "complement", "classic", "starter",
        "Galician razor clams' intense brine and garlic amplify Do Ferreiro's saline mineral character; the white wine used in cooking creates culinary continuity")
    PAIR(prod1b, "Whole roasted Galician lobster with herb butter and lemon", "complement", "classic", "fish_course",
        "Galician lobster with the region's definitive white wine is a luxury pairing of genuine regional authenticity; the wine's stone fruit matches the crustacean's sweetness")
    PAIR(prod1b, "White asparagus with Hollandaise and shaved Manchego", "complement", "established", "starter",
        "White asparagus and Albariño is a Spanish spring classic; Hollandaise richness is tamed by the wine's acidity while Manchego adds saline depth")
    PAIR(prod1b, "Sea bass ceviche with apple, celery, and green almond", "complement", "adventurous", "starter",
        "Apple and celery echo Albariño's stone fruit and fresh herb character; the ceviche's citrus marinade mirrors the wine's bright acidity")

# ── REGION 2: Penedès DO (Spain/Catalonia) ──────────────────────────────────
print("\n=== Region 2: Penedès ===")
r2 = R("Penedès", "Spain", "wine",
    designation_type="DO", designation_name="Penedès DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Penedès is Catalonia's most important wine region, producing diverse styles from indigenous Catalan varieties — Xarel·lo, Macabeo, Parellada — and international varieties across varying altitudes (coast to mountain). The region is also the heart of Cava production. Altitude differences create everything from ripe, full-bodied reds to crisp, mineral whites; a small premium producer tier is gaining serious attention for age-worthy wines.",
    key_producers="Torres, Jean Leon, Albet i Noya, Can Ràfols dels Caus",
    historical_context="Penedès has been producing wine since Phoenician and Roman times. The 20th century was defined by Miguel Torres Sr.'s modernisation of the winery in the 1960s-70s, introducing temperature-controlled stainless steel and French oak aging — revolutionary for Spain at the time. The region's Cava industry (regulated separately) dominates in volume, but artisan DO producers are reviving indigenous varieties and high-altitude sites.")

VIN(r2, 2023, "very_good", "stable", "Good Catalan vintage; diverse expressions across altitudes — coastal whites fresh and aromatic, mountain reds showing good structure")
VIN(r2, 2022, "excellent", "rising", "Outstanding year; exceptional concentration across all styles with high-altitude whites showing remarkable mineral precision")
VIN(r2, 2021, "good", "stable", "Balanced year with good freshness; Xarel·lo particularly successful for mineral white expressions")
VIN(r2, 2020, "very_good", "rising", "Strong vintage with good ripeness; Cabernet and Garnacha reds showing excellent depth and structure")
VIN(r2, 2019, "excellent", "rising", "Benchmark Penedès vintage; age-worthy reds and complex mineral whites across altitude sub-zones")

prod2a_id = P("Albet i Noya", "Spain", r2, "winery",
    "Penedès's pioneer of organic and biodynamic viticulture; the Albet i Noya estate has farmed without chemicals since 1979 and produces some of the region's finest indigenous variety wines — particularly their Xarel·lo whites and Garnacha Cabernet blends.")
prod2a, new2a = PROD("Albet i Noya Xarel·lo Classic Penedès", "wine_still", prod2a_id, r2, "Spain",
    subcategory="white", price_tier="mid_range",
    description="Albet i Noya's organic Xarel·lo from old Penedès vines: mineral, apple-driven, and textural. Xarel·lo at its finest — unmasked by barrel or blending — shows a complexity and aging capacity that has surprised critics and established the variety's credentials as Catalonia's finest indigenous white grape.")
if new2a:
    PAIR(prod2a, "Escalivada (roasted aubergine and peppers with anchovies and olive oil)", "complement", "classic", "starter",
        "Catalan's classic roasted vegetable dish with anchovy and olive oil is the archetypal Penedès white wine pairing; Xarel·lo's mineral freshness cuts through the olive oil richness")
    PAIR(prod2a, "Fideuà de mariscos (Catalan seafood noodle with aioli)", "complement", "classic", "main",
        "Catalan seafood fideuà — like paella but with noodles — with its rich saffron broth and aioli is a definitive Penedès white wine pairing")
    PAIR(prod2a, "Pan con tomate with Jamón Ibérico and Manchego", "complement", "established", "casual",
        "The simplest Catalan pleasure — tomato-rubbed bread with Ibérico ham and aged cheese — is the everyday pairing for crisp Penedès Xarel·lo")
    PAIR(prod2a, "Grilled calamari with lemon and alioli verde", "complement", "classic", "starter",
        "Catalan-style grilled squid with lemon and herbed aioli is a natural match for Xarel·lo's apple-mineral character and clean finish")

prod2b_id = P("Can Ràfols dels Caus", "Spain", r2, "winery",
    "One of Penedès's most ambitious artisan estates; Carlos Esteva's high-altitude organic estate produces wines from both indigenous Catalan varieties and Pinot Noir that challenge Spanish wine orthodoxy — particularly the Xarel·lo Lo Cau and single-parcel Indigène bottlings.")
prod2b, new2b = PROD("Can Ràfols Gran Caus Penedès Blanc", "wine_still", prod2b_id, r2, "Spain",
    subcategory="white", price_tier="premium",
    description="Can Ràfols's high-altitude estate white from Xarel·lo, Chenin Blanc, and Chardonnay at 600m elevation; complex and mineral with apple, citrus, and a mineral tension that ages gracefully for 8-10 years. A benchmark for Penedès's serious white wine ambition.")
if new2b:
    PAIR(prod2b, "Suquet de peix (Catalan fisherman's stew with sofregit and picada)", "complement", "classic", "main",
        "Catalonia's traditional fish stew with its almond-saffron picada and sofregit base needs a wine of Gran Caus's complexity and mineral structure")
    PAIR(prod2b, "Grilled langoustines with Romesco sauce and wild herbs", "complement", "established", "starter",
        "Langoustine's sweetness and Romesco's roasted pepper depth find their best Catalan white wine companion in Gran Caus's textured mineral complexity")
    PAIR(prod2b, "Aged Garrotxa goat cheese with honey and toasted pine nuts", "bridge", "established", "cheese",
        "Catalan semi-aged goat cheese with local honey bridges Gran Caus's apple-mineral character; pine nuts add Mediterranean nuttiness")
    PAIR(prod2b, "Monkfish with saffron, tomato, and clam broth", "complement", "established", "fish_course",
        "Firm monkfish with Catalan seafood flavours needs Gran Caus's structured mineral white; saffron and tomato are natural Penedès white companions")

# ── REGION 3: Dão DOC (Portugal) ─────────────────────────────────────────────
print("\n=== Region 3: Dão ===")
r3 = R("Dão", "Portugal", "wine",
    designation_type="DOC", designation_name="Dão DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Dão is one of Portugal's most distinctive and historically important wine regions, producing elegant, age-worthy reds from indigenous varieties — primarily Touriga Nacional, Alfrocheiro, and Tinta Roriz — grown on granite soils in a mountainous inland region of central Portugal. At their best, Dão reds show a Burgundian-like finesse with dark cherry, violet, earthy mineral, and remarkable longevity.",
    key_producers="Quinta dos Roques, Quinta da Pellada, Álvaro Castro, Niepoort",
    historical_context="Dão was one of Portugal's first regulated wine regions (1908), but its reputation stagnated under decades of cooperative dominance when grapes were pooled regardless of quality. The transformation began in the 1990s when independent producers like Álvaro Castro and later Dirk Niepoort began bottling single-vineyard and estate wines, revealing Dão's exceptional terroir for elegant, fine-structured Portuguese reds.")

VIN(r3, 2022, "excellent", "rising", "Outstanding Dão vintage; Touriga Nacional achieved exceptional aromatic complexity and mineral depth on the granite soils")
VIN(r3, 2021, "very_good", "stable", "Fine balanced year with classic Dão elegance; dark cherry and violet character with good aging structure")
VIN(r3, 2020, "excellent", "rising", "Powerful vintage; concentrated and deeply mineral with exceptional 15-20 year aging potential")
VIN(r3, 2019, "very_good", "rising", "Benchmark Dão vintage; extraordinary mineral precision and Touriga Nacional aromatic complexity")
VIN(r3, 2018, "good", "stable", "Accessible year with softer tannins; good varietal typicity at an earlier drinking window")

prod3a_id = P("Álvaro Castro", "Portugal", r3, "winery",
    "The single most important figure in Dão's modern quality revolution; Álvaro Castro's Quinta da Pellada and estate wines from old granite-soil vines have redefined what Dão can achieve — wines of genuine Burgundian refinement from Portugal's overlooked inland mountain region.")
prod3a, new3a = PROD("Álvaro Castro Dão Tinto Reserva", "wine_still", prod3a_id, r3, "Portugal",
    subcategory="red", price_tier="premium",
    description="Álvaro Castro's flagship Dão Reserva from old vines on granite: Touriga Nacional, Alfrocheiro, and Tinta Roriz blended with Burgundian sensibility. Dark cherry, violet, iron mineral, and remarkable elegance. One of Portugal's finest and most undervalued age-worthy reds.")
if new3a:
    PAIR(prod3a, "Roasted kid goat (Cabrito assado) with garlic, rosemary, and white wine", "complement", "classic", "main",
        "Kid goat is the Dão region's traditional celebratory food; its lean, aromatic character is the natural match for the wine's violet and mineral complexity")
    PAIR(prod3a, "Grilled Iberian pork with roasted garlic, herbs, and braised lentils", "complement", "established", "main",
        "Portuguese Iberian pork's depth meets Dão's mineral Touriga Nacional; lentils add earthy weight to bridge the wine's granite terroir")
    PAIR(prod3a, "Perdiz à Transmontana (partridge with cabbage and presunto)", "complement", "classic", "main",
        "Mountain partridge with Portuguese cured ham and cabbage is the most authentic Dão food pairing — traditional, regional, and precisely calibrated")
    PAIR(prod3a, "Queijo de Azeitão with fig preserve and roasted almonds", "bridge", "classic", "cheese",
        "Soft Setúbal sheep cheese with fig bridges Dão's dark cherry and violet; almonds add mineral nuttiness to the granite terroir echo")

prod3b_id = P("Niepoort", "Portugal", r3, "winery",
    "The visionary Port house that extended its expertise to table wines across Portugal; Dirk Niepoort's Dão wines from Quinta de Lemos and collaborations with local growers have brought a new level of ambition and global attention to the region's granite-terroir potential.")
prod3b, new3b = PROD("Niepoort Dão Tinto", "wine_still", prod3b_id, r3, "Portugal",
    subcategory="red", price_tier="mid_range",
    description="Niepoort's accessible Dão red: old vine Touriga Nacional and Alfrocheiro blended with the Port house's characteristic precision and restraint. Elegant violet, dark cherry, granite mineral, and fresh acidity — among Dão's finest value expressions and an ideal introduction to the region's character.")
if new3b:
    PAIR(prod3b, "Arroz de pato (duck rice with chouriço and crispy skin)", "complement", "classic", "main",
        "Portugal's beloved duck rice dish — a comfort classic with chouriço — is a natural match for Dão's elegant dark cherry and mineral structure")
    PAIR(prod3b, "Slow-roasted lamb with coriander, garlic, and Dão red wine reduction", "complement", "classic", "main",
        "Portuguese lamb slow-cooked in regional wine creates a culinary unity that amplifies every dimension of the Dão's elegant Touriga Nacional")
    PAIR(prod3b, "Grilled presunto and mushroom crostini with fresh herbs", "complement", "established", "starter",
        "Portuguese cured ham and mushroom on toast amplify Dão's dark fruit and earthy mineral through a simple, authentic wine bar pairing")
    PAIR(prod3b, "Bacalhau com natas (salt cod gratin with cream and potato)", "complement", "established", "main",
        "Portugal's classic salt cod gratin with cream needs Dão's acidity to cut through the richness; the wine's mineral depth elevates the dish's complexity")

# ── REGION 4: Kamptal (Austria) ─────────────────────────────────────────────
print("\n=== Region 4: Kamptal ===")
r4 = R("Kamptal", "Austria", "wine",
    designation_type="DAC", designation_name="Kamptal DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Kamptal is one of Austria's most celebrated wine regions, situated along the Kamp River in Lower Austria, producing benchmark Grüner Veltliner and Riesling from the loess, granite, and primary rock terroirs of the Strasser Weinberge and Heiligenstein. The wines range from peppery, mineral everyday Grüner Veltliner to grand cru-equivalent single-vineyard Rieslings of extraordinary complexity and longevity.",
    key_producers="Bründlmayer, Schloss Gobelsburg, Hirsch, Loimer",
    historical_context="The Kamptal DAC designation was established in 2008, recognising the region's long history of distinctive wine production. Willi Bründlmayer's pioneering work from the 1980s established Kamptal's international reputation, particularly with the Heiligenstein Riesling — one of Austria's greatest individual vineyard sites. The region's diversity of soils from loess to primary rock allows exceptional expression across both major varieties.")

VIN(r4, 2022, "excellent", "rising", "Outstanding Kamptal vintage; remarkable Heiligenstein Riesling and Zobings Grüner Veltliner with concentration and exceptional freshness")
VIN(r4, 2021, "very_good", "stable", "Fine vintage with good balance; elegant, mineral Grüner and structured Riesling with excellent aging potential")
VIN(r4, 2020, "good", "stable", "Accessible year with good typicity; fresh, peppery Grüner Veltliner and approachable Riesling")
VIN(r4, 2019, "excellent", "rising", "Benchmark Kamptal vintage; extraordinary Heiligenstein Riesling depth and complex Grüner mineral expression")
VIN(r4, 2018, "very_good", "stable", "Classic vintage with excellent structure; Riesling in particular showing remarkable 10-15 year aging capability")

prod4a_id = P("Bründlmayer", "Austria", r4, "winery",
    "The pre-eminent Kamptal estate and Austria's most internationally celebrated Riesling and Grüner Veltliner producer; Willi Bründlmayer's biodynamic approach produces wines of extraordinary precision from multiple sites including the legendary Heiligenstein volcanic ridge.")
prod4a, new4a = PROD("Bründlmayer Heiligenstein Riesling Alte Reben", "wine_still", prod4a_id, r4, "Austria",
    subcategory="white", price_tier="ultra_premium",
    description="Bründlmayer's flagship Kamptal Riesling from old vines on the Heiligenstein volcanic ridge: primary rock terroir of extraordinary mineral complexity. Apricot, white peach, volcanic mineral, and extraordinary acid tension. One of Austria's most celebrated wines with 20-30 year aging potential.")
if new4a:
    PAIR(prod4a, "Wiener Schnitzel with lingonberry, lemon wedge, and potato salad", "complement", "classic", "main",
        "Austria's national dish and Kamptal Riesling is the definitive Viennese restaurant pairing; the wine's acidity and mineral cut through the breadcrumb coating")
    PAIR(prod4a, "Grilled pike-perch with herb butter, capers, and boiled potatoes", "complement", "classic", "fish_course",
        "Danube River pike-perch with herb butter is the Austrian freshwater fish pairing for Heiligenstein Riesling; the wine's mineral depth mirrors the riverine terroir")
    PAIR(prod4a, "Crayfish with dill, sour cream, and cucumber salad", "complement", "established", "starter",
        "Austrian freshwater crayfish with dill sour cream is an elegant regional match for Heiligenstein Riesling's acidity and apricot-mineral depth")
    PAIR(prod4a, "Aged Bergkäse with mountain honey and caraway bread", "bridge", "classic", "cheese",
        "Austrian mountain cheese with local honey bridges Heiligenstein Riesling's mineral depth and stone fruit; caraway bread adds Austrian terroir authenticity")

prod4b_id = P("Schloss Gobelsburg", "Austria", r4, "winery",
    "The historic Cistercian monastic estate producing benchmark Kamptal Grüner Veltliner and Riesling; Michael Moosbrugger's estate combines historical continuity with modern precision, producing wines from the Gobelsburg castle estate's loess and primary rock vineyards.")
prod4b, new4b = PROD("Schloss Gobelsburg Grüner Veltliner Renner", "wine_still", prod4b_id, r4, "Austria",
    subcategory="white", price_tier="premium",
    description="Schloss Gobelsburg's single-vineyard Renner Grüner Veltliner from Kamptal loess-over-limestone; powerful and structured with white pepper, citrus peel, and mineral depth. Among Austria's finest Grüner Veltliner expressions — capable of 10-15 year aging with textbook pepperiness and mineral length.")
if new4b:
    PAIR(prod4b, "Grillhendl (Austrian rotisserie chicken) with green salad and potato", "complement", "classic", "main",
        "Austria's favourite summer food — rotisserie chicken — and Grüner Veltliner is the country's most versatile pairing; the wine's pepper and citrus cut through the golden chicken skin")
    PAIR(prod4b, "Spargel (white asparagus) with hollandaise and Viennese Schinken", "complement", "classic", "starter",
        "Austria's asparagus season is inextricably linked to Grüner Veltliner; the wine's white pepper and citrus are the natural accompaniment to the season's vegetable")
    PAIR(prod4b, "Tafelspitz (Viennese boiled beef) with horseradish and apple sauce", "complement", "classic", "main",
        "Austria's most beloved beef dish and Grüner Veltliner is the classic Viennese restaurant pairing; horseradish mirrors the wine's pepper while apple sauce echoes its fruit")
    PAIR(prod4b, "Sauerkraut with smoked pork and bread dumplings (Knödel)", "complement", "established", "main",
        "Austrian fermented cabbage with smoked pork and dumplings needs Grüner's acidity to cut through the fat; the wine's pepperiness matches the sauerkraut's tang")

# ── REGION 5: Ahr (Germany) ─────────────────────────────────────────────────
print("\n=== Region 5: Ahr ===")
r5 = R("Ahr", "Germany", "wine",
    designation_type="Anbaugebiet", designation_name="Ahr",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The Ahr is Germany's most northerly red wine region and one of its most climatically paradoxical — a narrow river valley south of Bonn produces Pinot Noir (Spätburgunder) and Frühburgunder of surprising depth and elegance from volcanic basalt and slate soils. The sheltered valley traps heat, enabling red wine ripeness at latitudes that seem impossible. The wines are some of Germany's most expensive and sought-after Pinot Noirs.",
    key_producers="Meyer-Näkel, Adeneuer, Nelles, Deutzerhof",
    historical_context="The Ahr Valley's monastic wine history stretches to the 7th century. The modern quality era began with Werner Näkel at Meyer-Näkel in the 1980s, who produced the first internationally recognised German Pinot Noir — transforming the Ahr from a tourist curiosity to a serious fine wine destination. The 2021 Ahr flood caused catastrophic vineyard and cellar damage, but the region's rebuilding has shown remarkable resilience.")

VIN(r5, 2022, "excellent", "rising", "Outstanding post-flood vintage; exceptional Spätburgunder depth from the surviving vineyards with volcanic basalt mineral character")
VIN(r5, 2021, "challenging", "stable", "The catastrophic July 2021 flood devastated vineyards and cellars; the wines made show remarkable character given the unprecedented conditions")
VIN(r5, 2020, "very_good", "stable", "Strong vintage with excellent Pinot ripeness and aromatic complexity from the volcanic basalt slate soils")
VIN(r5, 2019, "excellent", "rising", "Benchmark Ahr vintage before the flood; extraordinary Spätburgunder depth with Burgundy-rivalling complexity")
VIN(r5, 2018, "excellent", "rising", "Remarkable hot vintage; powerful, concentrated Pinot Noir with exceptional aging potential and unusually rich structure")

prod5a_id = P("Meyer-Näkel", "Germany", r5, "winery",
    "The producer who single-handedly established the Ahr's reputation for world-class Pinot Noir; Werner Näkel's estate produces Spätburgunder of Burgundy-competing quality from volcanic basalt slate vineyards — Germany's most acclaimed red wine estate.")
prod5a, new5a = PROD("Meyer-Näkel Blauschiefer Spätburgunder", "wine_still", prod5a_id, r5, "Germany",
    subcategory="red", price_tier="premium",
    description="Meyer-Näkel's vineyard-specific Blauschiefer (Blue Slate) Spätburgunder: Pinot Noir from the Ahr's volcanic blue slate soils — among Germany's most distinctive red wine terroirs. Dark cherry, dried herbs, violet, and a smoky slate mineral character unique to this valley. Outstanding Pinot Noir from one of Europe's most unlikely regions.")
if new5a:
    PAIR(prod5a, "Roasted duck breast with wild cherry and red cabbage", "complement", "classic", "main",
        "Duck and Pinot Noir is a universal pairing but the Ahr's slate mineral and dark cherry depth make this a particularly refined match; red cabbage is the German complement")
    PAIR(prod5a, "Reh (venison) medallion with juniper cream and Spätburgunder reduction", "complement", "classic", "main",
        "German venison with juniper and Ahr red wine reduction creates a perfect regional pairing; the wine's mineral character amplifies the game's complexity")
    PAIR(prod5a, "Sauerbraten with potato Knödel and red cabbage", "complement", "classic", "main",
        "Germany's iconic marinated beef roast with its sweet-sour sauce and potato dumplings is the traditional Ahr Spätburgunder pairing")
    PAIR(prod5a, "Aged Bergkäse with black cherry jam and dark rye bread", "bridge", "established", "cheese",
        "Mountain cheese with cherry jam bridges the Ahr's Pinot Noir dark fruit and slate mineral; dark rye bread echoes the volcanic terroir's earthiness")

prod5b_id = P("Adeneuer", "Germany", r5, "winery",
    "One of the Ahr's most consistent and established estates; the Adeneuer family has produced single-vineyard Spätburgunder from the Gärkammer and other premier sites for generations, achieving a balance of power and elegance characteristic of the valley's finest expressions.")
prod5b, new5b = PROD("Adeneuer Gärkammer Spätburgunder", "wine_still", prod5b_id, r5, "Germany",
    subcategory="red", price_tier="premium",
    description="Adeneuer's iconic single-vineyard Spätburgunder from the Gärkammer site — one of the Ahr's most celebrated plots on volcanic basalt. Elegant, structured Pinot Noir with dark cherry, violet, earthy mineral, and the valley's characteristic smoky depth. Among Germany's most distinguished red wines.")
if new5b:
    PAIR(prod5b, "Rouladen (beef rolls with mustard, onion, and pickles) with Rotkohl", "complement", "classic", "main",
        "Germany's most iconic slow-cooked beef dish with sweet-sour red cabbage is the traditional accompaniment for Ahr Spätburgunder in German fine dining")
    PAIR(prod5b, "Wild mushroom ragù with Spätzle and aged Emmental", "complement", "established", "main",
        "Forest mushroom sauce with Swabian egg noodles and Swiss cheese amplifies the Ahr's earthy mineral character; Emmental adds Alpine depth to the pairing")
    PAIR(prod5b, "Grilled Saumagen (stuffed pig's stomach) with mustard and sauerkraut", "complement", "classic", "casual",
        "This Palatinate regional sausage staple is an unusual but authentic German match for structured Ahr Pinot in a traditional tavern setting")
    PAIR(prod5b, "Aged Gouda with quince paste and walnut bread", "bridge", "established", "cheese",
        "Aged Gouda's caramel depth and quince sweetness bridge Gärkammer's dark cherry Pinot Noir; walnut adds mineral bitterness to the Ahr's volcanic slate character")

# ── Summary ──────────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nTotal regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("Done.")
conn.close()
