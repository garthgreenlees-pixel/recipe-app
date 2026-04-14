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

# ── 1. GISBORNE (New Zealand) ────────────────────────────────────────────────
print("\n=== Gisborne (New Zealand) ===")
r = R("Gisborne", "New Zealand", "wine",
      designation_type="GI",
      designation_name="Gisborne GI",
      reputation_tier="respected",
      quality_trajectory="established",
      description="New Zealand's easternmost wine region and self-proclaimed Chardonnay Capital of the country. Rich, alluvial Poverty Bay soils and warm maritime climate produce full-bodied, generously fruited whites. Gisborne was also the first NZ region to produce wine commercially and retains significant bulk production alongside growing premium estates.",
      key_producers="Millton Vineyard, Milton Estate, Maison Noire, TW Wines, Spade Oak",
      historical_context="Gisborne (Poverty Bay) was New Zealand's first wine-producing region, establishing vines in the 1850s. The region peaked as a bulk wine supplier in the 1980s-90s but has since pivoted toward premium estate wine, organic viticulture, and indigenous varietals including Chenin Blanc and Gewurztraminer.")

VIN(r, 2023, "excellent", "stable", "Warm, sunny season ideal for Chardonnay; full-bodied wines with excellent tropical fruit development")
VIN(r, 2022, "very_good", "stable", "Good harvest conditions; round, generous style with characteristic Gisborne richness")
VIN(r, 2021, "good", "stable", "La Nina rainfall challenged the vintage; organic estates rewarded with clean, vibrant fruit")
VIN(r, 2020, "very_good", "stable", "Ideal warm season producing concentrated, well-structured Chardonnay and Gewurztraminer")
VIN(r, 2019, "excellent", "stable", "Outstanding vintage; richest, most complex Chardonnay from Gisborne in years")

p1 = P("Millton Vineyard", "New Zealand", r, "winery",
        "New Zealand's first certified biodynamic wine estate and Gisborne's most celebrated producer. James and Annie Millton have farmed their Manutuke property according to Demeter biodynamic principles since the late 1980s, producing Gisborne Chardonnay and Chenin Blanc of remarkable depth and longevity.")
prod1, new1 = PROD("Millton Te Arai Vineyard Chardonnay Gisborne", "wine_still", p1, r, "New Zealand",
    subcategory="Chardonnay",
    description="Biodynamic Gisborne Chardonnay from Te Arai Vineyard; rich, complex, and textured with peach, melon, and hazelnut with a long mineral finish",
    price_tier="premium")
if new1:
    PAIR(prod1, "Pan-seared blue cod with brown butter and capers", "complement", "classic", "main", "Rich, textured Chardonnay frames the buttery fish beautifully with matching weight and acidity")
    PAIR(prod1, "Roasted corn bisque with crab", "complement", "established", "starter", "The wine's tropical fruit and hazelnut notes resonate with sweet corn and delicate crab")
    PAIR(prod1, "Brie with honeycomb and walnuts", "bridge", "suggested", "cheese", "Textured, lightly oxidative Chardonnay bridges elegantly with creamy Brie and honey")
    PAIR(prod1, "Pork belly with apple and fennel", "complement", "established", "main", "The wine's generous fruit and weight match the richness of slow-roasted pork belly")

p2 = P("TW Wines", "New Zealand", r, "winery",
        "A modern Gisborne estate producing terroir-focused wines that showcase the region's unique combination of warmth and alluvial soils. Their Gewurztraminer and Chardonnay are regularly cited as benchmarks for the region's expressive aromatic style.")
prod2, new2 = PROD("TW Wines Gisborne Gewurztraminer", "wine_still", p2, r, "New Zealand",
    subcategory="Gewurztraminer",
    description="Aromatic, off-dry Gisborne Gewurztraminer with intense lychee, rose petal, and ginger spice; full-bodied with a lingering exotic finish",
    price_tier="mid_range")
if new2:
    PAIR(prod2, "Thai red duck curry with lychee and jasmine rice", "complement", "classic", "main", "Lychee-forward, lightly sweet Gewurztraminer mirrors the fruit and spice of Thai duck curry")
    PAIR(prod2, "Spiced lamb kebabs with mint yoghurt", "complement", "established", "main", "Rose petal and ginger spice of Gewurztraminer echo the spice of Middle Eastern lamb preparations")
    PAIR(prod2, "Washed-rind Epoisses or Munster cheese", "complement", "classic", "cheese", "The classic pairing: powerful washed-rind cheese is tamed and elevated by aromatic Gewurztraminer")
    PAIR(prod2, "Vietnamese pho with rare beef and herbs", "bridge", "suggested", "main", "Aromatic wine's spice and slight sweetness bridge the complex spiced broth and herb garnish")

# ── 2. BADEN (Germany) ──────────────────────────────────────────────────────
print("\n=== Baden (Germany) ===")
r2 = R("Baden", "Germany", "wine",
       designation_type="Anbaugebiet",
       designation_name="Baden QbA/Pradikatswein",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Germany's southernmost and warmest wine region, stretching 400km from the Rhine to Lake Constance. Known for Pinot Noir (Spatburgunder) and Pinot Gris (Grauburgunder) of Burgundian character, plus rich Weissburgunder. The Kaiserstuhl volcanic plateau is the heart of the region. Large cooperative system but world-class estates producing dry, age-worthy wines.",
       key_producers="Weingut Bernhard Huber, Dr. Heger, Ziereisen, Franz Keller, Martin Waßmer",
       historical_context="Baden's wine history stretches to the Romans. The region's diversity — from Taubertal in the north to Hegau near Lake Constance in the south — reflects its enormous size and climatic variation. Modern Baden is best known internationally for Bernhard Huber's benchmark Pinot Noir, which elevated the region's global reputation in the 2000s.")

VIN(r2, 2023, "excellent", "rising", "Warm, long growing season; outstanding Spatburgunder concentration from the Kaiserstuhl")
VIN(r2, 2022, "very_good", "rising", "Good vintage with ripe tannins and excellent fruit purity in red and white wines")
VIN(r2, 2021, "good", "stable", "Challenging spring, better summer; careful selection produced elegant, food-friendly wines")
VIN(r2, 2020, "very_good", "stable", "Hot summer tempered by altitude; Pinot Noir showed impressive depth and structure")
VIN(r2, 2019, "exceptional", "rising", "Benchmark vintage for Baden Spatburgunder; finest red wines in a generation")

p3 = P("Weingut Bernhard Huber", "Germany", r2, "winery",
        "Baden's most internationally celebrated producer and a pioneer of serious German Pinot Noir. Based in Malterdingen, Huber's Spatburgunder wines — particularly the reserve and single-vineyard cuvees — are considered among Germany's finest red wines and have drawn global attention to Baden's Pinot potential.")
prod3, new3 = PROD("Huber Malterdinger Spatburgunder Baden Reserve", "wine_still", p3, r2, "Germany",
    subcategory="Spatburgunder",
    description="Baden's benchmark Pinot Noir reserve; silky, complex red with Burgundian elegance — fresh cherry, forest floor, and fine-grained tannins with exceptional aging potential",
    price_tier="premium")
if new3:
    PAIR(prod3, "Roasted duck breast with Pinot sauce and beetroot", "complement", "classic", "main", "Silky, cherry-fruited Spatburgunder is a natural partner for roasted duck in a classic German preparation")
    PAIR(prod3, "Wild mushroom ragout on egg Spaetzle", "complement", "established", "main", "Forest floor and earth notes in Pinot resonate with wild mushroom and the richness of hand-rolled pasta")
    PAIR(prod3, "Venison saddle with juniper and Rotkohl", "complement", "established", "main", "Structured, cool-climate Pinot holds up to venison and earthy red cabbage beautifully")
    PAIR(prod3, "Aged Emmentaler and mountain honey", "bridge", "suggested", "cheese", "The wine's cherry fruit and fine tannins bridge elegantly with nutty aged mountain cheese")

p4 = P("Dr. Heger", "Germany", r2, "winery",
        "A benchmark producer on the Kaiserstuhl volcanic plateau, Dr. Heger crafts supremely mineral and age-worthy Grauburgunder and Weissburgunder alongside powerful, structured Spatburgunder. Their Achkarrer Schlossberg site produces some of Germany's most terroir-precise dry whites.")
prod4, new4 = PROD("Dr Heger Achkarrer Schlossberg Grauburgunder Baden GG", "wine_still", p4, r2, "Germany",
    subcategory="Grauburgunder",
    description="Grosses Gewachs Pinot Gris from the volcanic Kaiserstuhl; rich, mineral, and complex with stone fruit, white pepper, and a saline volcanic finish",
    price_tier="premium")
if new4:
    PAIR(prod4, "Grilled Rhine salmon with herb butter", "complement", "classic", "main", "Rich, mineral Grauburgunder matches the weight of salmon with its stone fruit and textured body")
    PAIR(prod4, "Spaghetti with white truffle and Parmesan", "complement", "established", "main", "Volcanic minerality and white pepper in the wine echo truffle's earthiness magnificently")
    PAIR(prod4, "Roasted white asparagus with hollandaise and ham", "complement", "classic", "main", "Alsace-inspired pairing: Pinot Gris and white asparagus with butter sauce is a timeless regional combination")
    PAIR(prod4, "Aged Munster cheese with cumin bread", "complement", "classic", "cheese", "Traditional Baden-Alsace pairing: powerful washed-rind cheese tamed by a structured Grauburgunder")

# ── 3. FIANO DI AVELLINO (Italy) ─────────────────────────────────────────────
print("\n=== Fiano di Avellino (Italy) ===")
r3 = R("Fiano di Avellino", "Italy", "wine",
       designation_type="DOCG",
       designation_name="Fiano di Avellino DOCG",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="One of Italy's great white wine DOCG appellations in the volcanic hills of Campania's Irpinia zone. Fiano di Avellino produces some of Southern Italy's most compelling whites from the ancient Fiano grape — complex, mineral, and built for aging. The volcanic and limestone soils of the Apennine foothills give wines a distinctive smoky, honeyed character that intensifies with bottle age.",
       key_producers="Mastroberardino, Feudi di San Gregorio, Benito Ferrara, Villa Diamante, Pietracupa",
       historical_context="Fiano (then called Apianum for its appeal to bees) was prized by the Romans. Mastroberardino preserved the variety through the 20th century when it was nearly extinct. DOCG status was awarded in 2003, recognising the appellation's quality superiority among Campanian whites.")

VIN(r3, 2023, "excellent", "rising", "Warm, dry growing season on Irpinia's volcanic slopes; exceptional aromatic intensity in Fiano")
VIN(r3, 2022, "very_good", "rising", "Good vintage with typical smoky complexity and age-worthy structure")
VIN(r3, 2021, "good", "stable", "Cooler year produced elegant, taut Fiano with exceptional freshness for long aging")
VIN(r3, 2020, "very_good", "stable", "Hot summer; rich, concentrated wines with the characteristic hazelnut and honey notes")
VIN(r3, 2019, "excellent", "rising", "Outstanding Campanian vintage; Fiano of benchmark complexity and cellaring potential")

p5 = P("Mastroberardino", "Italy", r3, "winery",
        "The historic guardian of Campanian viticulture, Mastroberardino preserved Fiano and Aglianico varietals through the 20th century when other producers abandoned them for international grapes. Their Radici and Vari labels are defining benchmarks for Fiano di Avellino and Taurasi DOCG.")
prod5, new5 = PROD("Mastroberardino Radici Fiano di Avellino DOCG", "wine_still", p5, r3, "Italy",
    subcategory="Fiano",
    description="Benchmark Fiano di Avellino from historic Irpinia holdings; hazelnut, smoke, ripe pear, and volcanic mineral — one of Southern Italy's most age-worthy whites",
    price_tier="premium")
if new5:
    PAIR(prod5, "Linguine alle vongole (clams) with white wine", "complement", "classic", "main", "Smoky, mineral Fiano is a natural match for fresh clams — a classic Neapolitan pairing")
    PAIR(prod5, "Roasted sea bass with capers and olives", "complement", "established", "main", "The wine's structure and mineral depth frame firm-fleshed white fish with Mediterranean garnish")
    PAIR(prod5, "Spaghetti aglio olio with bottarga", "complement", "established", "main", "Volcanic mineral and smoky notes in Fiano resonate beautifully with umami-rich cured fish roe")
    PAIR(prod5, "Aged Pecorino with local honey and walnuts", "bridge", "suggested", "cheese", "Smoky, honeyed Fiano bridges with sharp aged Pecorino and sweet honey in a classic Italian table")

p6 = P("Feudi di San Gregorio", "Italy", r3, "winery",
        "Campania's most internationally recognised modern winery, Feudi di San Gregorio elevated the region's profile through investment in viticulture and collaboration with Gancia and Bordeaux consultants. Their Campanaro Fiano is an ambitious single-vineyard expression of Irpinia's volcanic terroir.")
prod6, new6 = PROD("Feudi di San Gregorio Campanaro Fiano di Avellino", "wine_still", p6, r3, "Italy",
    subcategory="Fiano",
    description="Single-vineyard reserve Fiano; richer and more textured than the estate wine, with white peach, toasted hazelnut, smoke, and volcanic mineral on a long, structured finish",
    price_tier="premium")
if new6:
    PAIR(prod6, "Risotto al limone with seared prawns", "complement", "established", "main", "Textured, mineral Fiano resonates with the acidity and sweetness of prawn and lemon risotto")
    PAIR(prod6, "Grilled spigola (sea bass) with wild herbs", "complement", "classic", "main", "The wine's smoky mineral complexity pairs naturally with Mediterranean herbs and delicate white fish")
    PAIR(prod6, "Neapolitan seafood salad with lemon and olive oil", "complement", "classic", "starter", "Crisp, mineral Fiano cuts through the richness of mixed seafood with citrus dressing")
    PAIR(prod6, "Aged Provolone del Monaco", "complement", "suggested", "cheese", "Smoky, structured Fiano holds up to the sharpness of aged Provolone — a distinctly Campanian match")

# ── 4. MONTILLA-MORILES (Spain) ───────────────────────────────────────────────
print("\n=== Montilla-Moriles (Spain) ===")
r4 = R("Montilla-Moriles", "Spain", "wine",
       designation_type="DO",
       designation_name="DO Montilla-Moriles",
       reputation_tier="respected",
       quality_trajectory="rediscovering",
       description="The spiritual home of Pedro Ximenez, the luscious raisin grape used to make Spain's richest dessert wines. Located south of Cordoba in Andalusia, Montilla-Moriles produces bone-dry Fino and Amontillado-style unfortified wines (legally classified as wine, not fortified) alongside gloriously sweet PX. Often called the overlooked cousin of Jerez, the region's albariza-chalk soils and extreme heat produce naturally high-sugar PX grapes.",
       key_producers="Bodegas Alvear, Toro Albala, Bodegas Robles, Cruz Conde",
       historical_context="Montilla-Moriles predates Jerez as a wine region and historically supplied much of the base wine for Sherry blends. The region's Pedro Ximenez grape was named after a Spanish soldier who supposedly brought the vine from the Canary Islands in the 17th century. Alvear, founded in 1729, is one of Spain's oldest continuous wine estates.")

VIN(r4, 2023, "good", "stable", "Hot, dry Andalusian summer; typical high sugar accumulation in PX grapes; strong vintage")
VIN(r4, 2022, "very_good", "stable", "Excellent growing season; PX achieved exceptional concentration and natural sweetness")
VIN(r4, 2021, "good", "stable", "Reliable vintage; fine dry Fino-style wines and well-concentrated PX")
VIN(r4, 2020, "very_good", "stable", "Warm, even-ripening season producing PX of exceptional density and fig-like concentration")
VIN(r4, 2019, "excellent", "stable", "Outstanding year; richest, most complex PX in recent memory from the region's albariza soils")

p7 = P("Bodegas Alvear", "Spain", r4, "winery",
        "Founded in 1729, Alvear is one of Spain's oldest continuous wine estates and the most internationally recognised producer of Montilla-Moriles. Their Pedro Ximenez wines — particularly the aged vintages — are regarded as the world's finest expressions of the variety, with extraordinary concentration and complexity.")
prod7, new7 = PROD("Alvear Pedro Ximenez Montilla-Moriles", "wine_fortified", p7, r4, "Spain",
    subcategory="Pedro Ximenez",
    description="Spain's most celebrated Pedro Ximenez; intense fig, raisin, date, and dark chocolate with a luxuriously viscous texture and endless sweet finish — the benchmark for the variety",
    price_tier="mid_range")
if new7:
    PAIR(prod7, "Dark chocolate fondant with sea salt", "complement", "classic", "dessert", "The wine's dark chocolate and fig notes create a seamless, indulgent pairing with a rich chocolate dessert")
    PAIR(prod7, "Vanilla ice cream poured over", "complement", "classic", "dessert", "The classic Andalusian serving: cold ice cream with warm PX poured directly over — an iconic Spanish dessert")
    PAIR(prod7, "Dried fig and almond tart", "complement", "established", "dessert", "Concentrated fig flavours in the wine echo and amplify the dried fruit and almond in the pastry")
    PAIR(prod7, "Manchego curado with quince paste", "complement", "established", "cheese", "Rich, sweet PX provides luscious contrast to salty aged Manchego with sweet membrillo")

p8 = P("Toro Albala", "Spain", r4, "winery",
        "A small artisan producer making some of the most aged and complex Pedro Ximenez wines in the world. Toro Albala's Don PX Gran Reserva vintages dating back to the 1940s are legendary, with extraordinary concentration and complexity achieved through decades of oxidative aging in old American oak casks.")
prod8, new8 = PROD("Toro Albala Don PX Gran Reserva Montilla-Moriles", "wine_fortified", p8, r4, "Spain",
    subcategory="Pedro Ximenez",
    description="One of the world's most extraordinary sweet wines; aged for decades in American oak — walnut, toffee, raisin, prune, and exotic spice of breathtaking complexity and concentration",
    price_tier="ultra_premium")
if new8:
    PAIR(prod8, "Blue cheese — Cabrales or Gorgonzola naturale", "contrast", "classic", "cheese", "The contrast of intensely sweet, complex PX against pungent, salty blue cheese is one of wine's great pairings")
    PAIR(prod8, "Bitter chocolate truffles with orange zest", "complement", "established", "dessert", "The wine's toffee, walnut, and dark fruit complement bitter chocolate with aromatic orange")
    PAIR(prod8, "Crema catalana with caramelised sugar", "complement", "classic", "dessert", "Caramel and vanilla in the custard resonate with the toffee and raisin complexity of aged PX")
    PAIR(prod8, "Foie gras terrine with brioche", "contrast", "adventurous", "starter", "The wine's sweetness and oxidative complexity create a remarkable counterpoint to rich foie gras")

# ── 5. ROBOLA OF CEPHALONIA (Greece) ─────────────────────────────────────────
print("\n=== Robola of Cephalonia (Greece) ===")
r5 = R("Robola of Cephalonia", "Greece", "wine",
       designation_type="PDO",
       designation_name="PDO Robola of Cephalonia",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="A small, prestigious PDO on the Ionian island of Cephalonia, producing some of Greece's most distinctive white wines from the indigenous Robola grape. High-altitude limestone vineyards (up to 800m) on the mountainous Omala valley produce wines of intense citrus, mineral freshness, and distinctive flinty character. Often described as Greece's answer to Chablis.",
       key_producers="Cooperative of Robola Producers of Cephalonia, Gentilini Winery, Sclavos Wines",
       historical_context="Robola's origins on Cephalonia are believed to date to Venetian occupation (1204-1797), when the island was an important wine-producing colony. The cooperative founded in 1953 saved the variety from extinction after the devastating 1953 earthquake that destroyed much of the island's infrastructure. Today, Robola is celebrated as one of Greece's most food-friendly and terroir-expressive whites.")

VIN(r5, 2023, "excellent", "rising", "Ideal growing conditions on Cephalonia's high limestone terraces; exceptional mineral clarity in Robola")
VIN(r5, 2022, "very_good", "rising", "Good vintage with fine citrus-mineral profile; wines of real elegance and freshness")
VIN(r5, 2021, "good", "stable", "Slightly wetter year but island's drainage handled it well; clean, crisp, food-friendly style")
VIN(r5, 2020, "very_good", "stable", "Warm season with good acidity retention at altitude; beautifully balanced Robola")
VIN(r5, 2019, "excellent", "rising", "Outstanding vintage; most mineral and complex Robola expressions in recent years")

p9 = P("Gentilini Winery", "Greece", r5, "winery",
        "The finest private estate producer of Robola, Gentilini crafts benchmark Cephalonian wines from high-altitude limestone vineyards with meticulous attention to expressing the Robola grape's unique mineral character. Their Classico and Fumé labels are the most internationally recognised Robola expressions.")
prod9, new9 = PROD("Gentilini Classico Robola of Cephalonia PDO", "wine_still", p9, r5, "Greece",
    subcategory="Robola",
    description="Benchmark Robola from Cephalonia's high-altitude limestone vineyards; intense lemon, lime, white blossom, and distinctive flinty mineral — Greece's most Chablis-like white",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "Grilled fresh anchovies with lemon and olive oil", "complement", "classic", "starter", "The wine's citrus intensity and flinty mineral are a natural foil for fresh anchovies — a Greek island classic")
    PAIR(prod9, "Grilled red mullet with caper salsa", "complement", "established", "main", "Crisp, mineral Robola provides clean contrast to sweet, delicate red mullet flesh with acidic caper garnish")
    PAIR(prod9, "Kakavia fish soup with crusty bread", "complement", "classic", "main", "Mineral, citrus-driven Robola is the natural accompaniment to Cephalonia's traditional fisherman's broth")
    PAIR(prod9, "Feta and sun-dried tomato bruschetta", "complement", "established", "starter", "The wine's acidity and citrus freshness cut through salty feta and amplify the bright tomato")

p10 = P("Sclavos Wines", "Greece", r5, "winery",
         "An artisan estate producing natural and biodynamic wines from indigenous Cephalonian varieties. Spyros Sclavos works with minimum intervention and wild yeasts to produce some of the island's most authentic and terroir-driven expressions of Robola, Mavrodaphne, and Muscat.")
prod10, new10 = PROD("Sclavos Robola Fumee de Pierres Cephalonia", "wine_still", p10, r5, "Greece",
    subcategory="Robola",
    description="Skin-contact Robola with extended maceration; deeper, more textured than classical style with smoky mineral, citrus pith, and a saline, stony finish — natural wine at its finest",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Grilled octopus with olive oil and oregano", "complement", "classic", "main", "Textured, mineral Robola is one of Greece's most iconic pairings with chargrilled octopus")
    PAIR(prod10, "Barbouni (red mullet) fried in olive oil", "complement", "established", "main", "Saline mineral wine cuts through the richness of fried fish beautifully")
    PAIR(prod10, "Graviera cheese with dried figs", "bridge", "established", "cheese", "Nutty, hard Greek cheese with sweet figs resonates with the wine's mineral-saline finish")
    PAIR(prod10, "Chilled cucumber and yoghurt tzatziki with pitta", "complement", "suggested", "starter", "The wine's citrus and mineral freshness complement the cool, clean flavours of tzatziki perfectly")

# ── COUNTS ───────────────────────────────────────────────────────────────────
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
print("\nDone.")
conn.close()
