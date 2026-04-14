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

# ── 1. Piave DOC (Italy/Veneto) ───────────────────────────────────────────────
print("\n=== Piave DOC (Italy) ===")
r1 = R("Piave DOC", "Italy",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Piave DOC",
    reputation_tier="overlooked",
    quality_trajectory="rediscovering",
    description="A historic Veneto appellation along the Piave River producing wines from the indigenous Raboso grape — one of Italy's most challenging and rewarding native varieties, delivering extreme tannic structure, fierce acidity and dark berry concentration. Piave Raboso was once Venice's everyday red; quality-focused producers are now reclaiming it as a serious age-worthy wine. The appellation also produces Pinot Grigio, Glera and Merlot.",
    key_producers="Ornella Molon, Bosco del Merlo, Rechsteiner, Casa Vinicola Zonin",
    historical_context="Piave's riverine alluvial plains were among Veneto's most productive wine areas historically, supplying Venice with everyday drinking wine for centuries. The Raboso grape was documented in the region before the 18th century; phylloxera devastated the vineyards in the 1890s, and 20th-century mass production diminished quality. The DOC was established in 1971; a generational shift toward lower yields and longer ageing is restoring Raboso's fierce reputation.")

VIN(r1, 2023, "very_good", "stable", "Warm Veneto season; Raboso of excellent concentration and structured tannins")
VIN(r1, 2022, "excellent", "stable", "Outstanding vintage; Piave Raboso Riserva potential across the appellation")
VIN(r1, 2021, "very_good", "stable", "Balanced year with good acidity retention; wines for medium-term cellaring")
VIN(r1, 2020, "good", "stable", "Reliable vintage; approachable Raboso with softer tannins than usual")
VIN(r1, 2019, "excellent", "rising", "Benchmark year; concentrated, structured Raboso with exceptional aging potential")

p1a = P("Ornella Molon", "Italy", r1, description="One of Piave DOC's finest family estates, run with precision by Ornella Molon Traverso, producing benchmark Piave Raboso and other Veneto varieties with a commitment to minimal intervention and expression of the river valley's distinctive terroir.")
prod1a, new1a = PROD("Ornella Molon Raboso Piave DOC", "wine_still", p1a, r1, "Italy",
    subcategory="Raboso",
    description="The benchmark Piave Raboso from one of the appellation's most committed producers — intense ruby-garnet with dark plum, leather, violets and iron minerality; the ferocious tannin and high acidity that define this indigenous variety at its authentic best.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Slow-braised Venetian duck with polenta taragna", "complement", "classic", "main", "Piave's traditional pairing — the region's most structured red with slow-braised poultry and cornmeal reveals Raboso's capacity to tame richness with its fierce tannic grip.")
    PAIR(prod1a, "Aged Asiago d'Allevo DOP with walnut bread", "complement", "established", "cheese", "The wine's high acidity and dark fruit complement the nutty, crystalline intensity of Asiago Stravecchio in a classic Veneto pairing.")
    PAIR(prod1a, "Bigoli in salsa with anchovy and onion", "bridge", "classic", "main", "Venice's ancient pasta in anchovy-onion sauce finds an unexpected but historically authentic bridge in the wine's saline mineral character and structured tannins.")
    PAIR(prod1a, "Venison stew with porcini mushrooms and polenta", "complement", "established", "main", "The wine's dark gamey depth and structured tannins embrace venison and forest mushroom richness in a mountain-Veneto pairing of remarkable harmony.")

p1b = P("Bosco del Merlo", "Italy", r1, description="A pioneering Piave DOC estate committed to reviving Raboso as a serious fine wine, with exceptional vineyard management of low-yielding old vines and extended maceration producing Piave Raboso Riserva of genuine complexity and longevity.")
prod1b, new1b = PROD("Bosco del Merlo Wildbacher Piave DOC", "wine_still", p1b, r1, "Italy",
    subcategory="Wildbacher",
    description="A rare Venetian expression of the Austrian Wildbacher grape (Schilcher), producing a deep-coloured, intensely aromatic wine with violet, dark cherry and spice character unique to the Piave appellation — a genuine curiosity and one of Italy's most unusual indigenous red wines.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled speck with horseradish cream", "complement", "adventurous", "starter", "The wine's intense violet and spice character creates an intriguing mirror with smoke-cured speck and the sharp heat of fresh horseradish.")
    PAIR(prod1b, "Goulash with egg pasta and paprika", "complement", "established", "main", "The wine's Central European character — straddling Italian and Austrian traditions — finds harmony with the Austro-Hungarian goulash that influenced northern Italian cuisine.")
    PAIR(prod1b, "Taleggio cheese with apple mostarda", "bridge", "established", "cheese", "The wine's dark fruit and spice bridge the washed-rind pungency of Taleggio while apple mostarda echoes the wine's Schilcher-derived freshness.")
    PAIR(prod1b, "Roasted wild boar with polenta and sage butter", "complement", "classic", "main", "Wildbacher's intense dark character handles wild boar's gamey intensity with the same confidence as Raboso but with more aromatic lift.")

# ── 2. Luján de Cuyo sub-region correction — Tupungato (Argentina) ────────────
# (Luján de Cuyo inserted in B50; adding Tupungato as distinct high-altitude sub-region)
print("\n=== Tupungato (Argentina) ===")
r2 = R("Tupungato", "Argentina",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Tupungato — Valle de Uco, Mendoza",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Argentina's highest and most dramatic wine sub-region, sitting at 1000–1500m elevation in the Valle de Uco south of Mendoza city, producing Argentina's most elegant and complex expressions of Chardonnay, Malbec and Pinot Noir. The extreme altitude, volcanic soils and glacial meltwater irrigation create an entirely different expression from lowland Mendoza — more linear, mineral and age-worthy than the intense fruit power of Luján de Cuyo.",
    key_producers="Zuccardi Valle de Uco, Clos de los Siete, Achaval Ferrer, Clos Apalta, Catena Zapata",
    historical_context="Tupungato was considered marginal for viticulture until the 1990s when pioneers recognised the altitude's potential for aromatic preservation and acidity retention. Nicolas Catena's investment in the Valle de Uco proved that ultra-high Andean viticulture could produce world-class wine. A rush of international investment followed; Michel Rolland's Clos de los Siete project brought global attention, and Tupungato is now recognised as South America's most exciting high-altitude wine frontier.")

VIN(r2, 2023, "excellent", "stable", "High-altitude freshness preserved; fine Chardonnay and precise mineral Malbec across Valle de Uco")
VIN(r2, 2022, "very_good", "stable", "Structured and elegant; Tupungato Malbec showing its distinctive cool-climate linearity")
VIN(r2, 2021, "exceptional", "rising", "Widely regarded as the finest Valle de Uco vintage of the decade — combining concentration with extraordinary mineral precision")
VIN(r2, 2020, "very_good", "stable", "Rich and concentrated despite the cool season; exceptional for high-elevation Chardonnay")
VIN(r2, 2019, "excellent", "stable", "Classic vintage; benchmark Tupungato character of mineral precision and aging potential")

p2a = P("Clos de los Siete", "Argentina", r2, description="Michel Rolland's landmark Argentine project uniting seven top Bordeaux and Argentine producers in a single high-elevation Valle de Uco estate, producing one of Argentina's most internationally recognised blends — a Malbec-dominant cuvée of remarkable consistency and approachability.")
prod2a, new2a = PROD("Clos de los Siete Tupungato Valle de Uco", "wine_still", p2a, r2, "Argentina",
    subcategory="Malbec, Merlot, Cabernet Sauvignon",
    description="Michel Rolland's Argentine flagship — a polished, internationally styled Malbec-dominant blend from high-altitude Valle de Uco vineyards showing dark plum, violet, chocolate and fine tannins that have introduced a generation of wine drinkers to premium Argentine wine.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Bife de chorizo with chimichurri and salad", "complement", "classic", "main", "Argentina's most loved steak cut with the country's definitive wine-food herb sauce — Clos de los Siete provides the perfect polished Malbec complement.")
    PAIR(prod2a, "Slow-roasted lamb shoulder with Andean spices", "complement", "established", "main", "The wine's polished tannins and generous dark fruit handle slow lamb with elegance, the Andean spice bridging the wine's complex fruit profile.")
    PAIR(prod2a, "Duck breast magret with blackberry reduction", "complement", "established", "main", "The wine's Merlot-Malbec blend echoes Bordeaux's duck affinity while adding Argentine generosity of fruit and texture.")
    PAIR(prod2a, "Aged Uruguayan chivito with chimichurri verde", "complement", "adventurous", "main", "The wine's dark intensity finds balance in the herb-forward green chimichurri cutting through the rich cured meat in this cross-River Plate pairing.")

p2b = P("Catena Zapata", "Argentina", r2, description="Argentina's most celebrated and internationally respected wine family, whose patriarch Nicolás Catena transformed Argentine wine by pioneering high-altitude viticulture in Mendoza and Valle de Uco, proving that Argentine terroir could produce world-class Chardonnay and Malbec comparable to the finest Burgundy and Bordeaux.")
prod2b, new2b = PROD("Catena Zapata Adrianna Vineyard Chardonnay Tupungato", "wine_still", p2b, r2, "Argentina",
    subcategory="Chardonnay",
    description="From the legendary Adrianna Vineyard at 1450m — one of the world's highest commercial vineyards — this Chardonnay produces arguably South America's most complex and age-worthy white wine, with extraordinary mineral depth, citrus oil precision and almost Burgundian tension that has earned comparison with the finest Grand Cru Chardonnays.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Butter-poached Argentine king crab with verjus", "complement", "classic", "main", "The wine's extraordinary mineral tension and citrus precision frame cold-water crustacean's sweet richness in a pairing of world-class elevation.")
    PAIR(prod2b, "Pan-seared halibut with celeriac puree and black truffle", "elevate", "adventurous", "main", "The Adrianna's almost-Burgundian depth and mineral intensity elevate halibut and truffle into a genuinely transcendent high-altitude Andean expression.")
    PAIR(prod2b, "Ricotta ravioli with brown butter and Alpine herbs", "complement", "established", "main", "The wine's Burgundy-like texture and butter complexity find their natural partner in delicate pasta with rich dairy and mountain herbs.")
    PAIR(prod2b, "Comté cheese 36 months aged with roasted hazelnuts", "complement", "established", "cheese", "The Adrianna's beeswax and oxidative complexity at this elevation mirrors great Comté's nutty depth in a genuinely profound cheese pairing.")

# ── 3. Montalcino (Italy/Tuscany) ─────────────────────────────────────────────
# Note: checking if Brunello di Montalcino exists — adding as distinct from generic Montalcino
print("\n=== Brunello di Montalcino (Italy) ===")
r3 = R("Brunello di Montalcino", "Italy",
    beverage_family="wine",
    designation_type="DOCG",
    designation_name="Brunello di Montalcino DOCG",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Italy's most prestigious red wine appellation and one of the world's great wine regions, producing single-varietal Sangiovese Grosso (Brunello) wines of extraordinary longevity from the hilltop town of Montalcino in southern Tuscany. Brunello di Montalcino requires minimum 5 years ageing before release (6 for Riserva) and routinely ages for 30+ years, developing profound complexity of dried rose, tobacco, iron, wild cherry and Tuscan terroir. Only 200+ producers farm 3,500 hectares of approved vineyards.",
    key_producers="Biondi-Santi, Poggio di Sotto, Cerbaiona, Col d'Orcia, Casanova di Neri, Soldera",
    historical_context="Ferruccio Biondi-Santi created modern Brunello di Montalcino in the 1870s by selecting and cultivating a superior Sangiovese clone (Brunello) and pioneering the extended ageing that would define the style. The DOCG was awarded in 1980, the first in Italy. A 2008 scandal (Brunellogate) where producers blended non-permitted varieties temporarily threatened the appellation's reputation, but rigorous enforcement restored international confidence and Brunello remains Italy's most collectable fine wine.")

VIN(r3, 2023, "excellent", "stable", "Promising year showing fine balance between concentration and elegance; classic Brunello profile")
VIN(r3, 2022, "very_good", "stable", "Warm but not extreme; wines of generous fruit with good structural framework")
VIN(r3, 2021, "excellent", "rising", "Considered a great vintage alongside 2016 and 2019; exceptional balance and longevity")
VIN(r3, 2020, "good", "stable", "Challenging warm year; best estates produced structured, age-worthy wines nonetheless")
VIN(r3, 2019, "exceptional", "rising", "Widely regarded as one of the finest Brunello vintages in decades; extraordinary concentration and freshness")

p3a = P("Poggio di Sotto", "Italy", r3, description="Consistently ranked among Brunello di Montalcino's finest producers, Poggio di Sotto's traditional approach — minimal intervention, no filtration, very long ageing in large Slavonian oak botti — produces wines of extraordinary purity, complexity and longevity that wine critics consider among Italy's greatest red wines.")
prod3a, new3a = PROD("Poggio di Sotto Brunello di Montalcino DOCG", "wine_still", p3a, r3, "Italy",
    subcategory="Sangiovese Grosso",
    description="One of Montalcino's greatest traditional Brunellos — pale garnet with brick at the rim, profound aromas of dried rose, wild cherry, iron minerals, tobacco and Tuscan earth; silky tannins of extraordinary refinement and a finish measured in minutes rather than seconds that rewards 20+ years of cellaring.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Bistecca alla Fiorentina T-bone with rosemary salt", "complement", "classic", "main", "Tuscany's most iconic wine and most iconic beef preparation — the Brunello's iron minerals and silky tannins frame the char-grilled Chianina with perfect classical authority.")
    PAIR(prod3a, "Wild boar pappardelle with juniper and rosemary", "complement", "classic", "main", "Cinghiale ragu is Montalcino's most natural partner for Brunello — the wine's dark fruit and tobacco depth mirroring the earthiness of Tuscan wild boar ragù.")
    PAIR(prod3a, "White truffle tagliolini with butter and Parmigiano", "elevate", "adventurous", "main", "Brunello's extraordinary complexity elevates the umami intensity of white truffle into a transcendent experience of Italian gastronomy.")
    PAIR(prod3a, "Aged Pecorino di Pienza stagionato", "complement", "classic", "cheese", "Siena's finest aged sheep milk cheese with its home region's greatest red wine — the wine's acidity cuts pecorino's lanolin richness while dried fruit notes complement the cheese's sweetness.")

p3b = P("Col d'Orcia", "Italy", r3, description="One of Montalcino's most historically important estates, Count Marone Cinzano's Col d'Orcia has been producing benchmark Brunello since the 1970s with both traditional and modern interpretations, and is one of the appellation's most reliable and well-distributed producers across all quality levels.")
prod3b, new3b = PROD("Col d'Orcia Brunello di Montalcino DOCG", "wine_still", p3b, r3, "Italy",
    subcategory="Sangiovese Grosso",
    description="A benchmark traditional Brunello from one of Montalcino's most established and consistent estates — showing classic garnet-brick colour, dried cherry, leather and tobacco aromatics with firm but refined tannins and the characteristic mineral backbone of the Montalcino hills.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Roasted pigeon with lentils and aged balsamic", "complement", "established", "main", "Succulent pigeon's earthy richness and the sweet-sour balsamic drizzle find perfect proportion in Brunello's austere fruit and mineral depth.")
    PAIR(prod3b, "Porcini mushroom risotto with Parmigiano-Reggiano", "complement", "classic", "main", "Forest mushroom umami and aged cheese complexity find their definitive complement in Brunello's earth-mineral character and dried fruit depth.")
    PAIR(prod3b, "Lamb chops scottadito with salsa verde", "complement", "established", "main", "Grilled Roman-Tuscan lamb cutlets with herb salsa verde — the wine's Sangiovese acidity cuts the fat while its dried cherry notes frame the herbs.")
    PAIR(prod3b, "Aged Pecorino Romano with truffle honey", "bridge", "established", "cheese", "The wine's structured tannins and earthy depth bridge the sharp Romano and sweet truffle honey in a quintessentially Tuscan cheese pairing.")

# ── 4. Wachau (Austria) ───────────────────────────────────────────────────────
print("\n=== Wachau (Austria) ===")
r4 = R("Wachau", "Austria",
    beverage_family="wine",
    designation_type="DAC",
    designation_name="Wachau DAC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Austria's most iconic and internationally renowned wine region, a UNESCO World Heritage Site of terraced granite and gneiss vineyards along a dramatic 35km stretch of the Danube gorge between Melk and Krems in Lower Austria. The Wachau produces Austria's most celebrated Grüner Veltliner and Riesling from its legendary vineyard sites — Smaragd-category wines from the best parcels achieve world-class complexity and extraordinary aging potential, rivalling Alsace and the Mosel at their finest.",
    key_producers="Domäne Wachau, Franz Hirtzberger, Emmerich Knoll, F.X. Pichler, Nikolaihof",
    historical_context="The Wachau's steep terraced vineyards have been cultivated since Roman times, with Augustinian monks playing a formative role in the medieval period. The modern Wachau appellation system — with its unique classification of Steinfeder (light), Federspiel (medium) and Smaragd (full-bodied) based on alcohol levels — was created in 1983 by the Vinea Wachau producers' association, providing Austria's first serious quality framework and helping establish the region as a world benchmark for dry Austrian white wine.")

VIN(r4, 2023, "excellent", "stable", "Beautiful Wachau vintage with ideal ripening; Grüner Veltliner and Riesling of exceptional clarity and mineral precision")
VIN(r4, 2022, "very_good", "stable", "Warm year but acidity well-preserved in the granite sites; generous and approachable Smaragd wines")
VIN(r4, 2021, "excellent", "stable", "Elegant, cool-influenced year; wines of extraordinary mineral purity and aging potential")
VIN(r4, 2020, "very_good", "stable", "Concentrated and rich; top Smaragd wines showing remarkable depth and structure")
VIN(r4, 2019, "exceptional", "rising", "One of Wachau's greatest modern vintages; Smaragd wines of transcendent mineral precision and complexity")

p4a = P("Franz Hirtzberger", "Austria", r4, description="One of the Wachau's most revered and internationally celebrated producers, Franz Hirtzberger Sr and his son craft Grüner Veltliner and Riesling Smaragd from legendary Wachau vineyard sites including Singerriedel with extraordinary mineral precision, texture and longevity that rank among Austria's greatest white wines.")
prod4a, new4a = PROD("Franz Hirtzberger Riesling Smaragd Singerriedel Wachau DAC", "wine_still", p4a, r4, "Austria",
    subcategory="Riesling",
    description="Austria's most iconic Riesling from the legendary Singerriedel vineyard — pure granite and gneiss terroir expressing itself in extraordinary mineral tension, citrus-stone fruit precision, spice and a finish of almost infinite length that rewards 15–25 years of ageing.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Zander (pike-perch) with brown butter and capers", "complement", "classic", "main", "The Danube's most prized freshwater fish with the Wachau's greatest white — granite minerality and citrus precision frame the delicate pike-perch in a pairing of perfect regional logic.")
    PAIR(prod4a, "Wiener Schnitzel with lingonberry and lemon", "complement", "classic", "main", "Austria's defining national dish and its greatest white wine — the Riesling's crisp acidity cuts through the breadcrumb crust while mineral notes balance the tart lingonberry.")
    PAIR(prod4a, "Langoustine with grapefruit beurre blanc", "complement", "established", "starter", "The wine's citrus and mineral precision elevate langoustine's sweet flesh with aristocratic refinement in this high-end Austrian-French pairing.")
    PAIR(prod4a, "Aged Austrian goat cheese with pear mostarda", "complement", "established", "cheese", "The wine's mineral backbone and citrus drive complement aromatic goat cheese while the pear mostarda bridges its elegant fruit.")

p4b = P("Nikolaihof Wachau", "Austria", r4, description="Austria's oldest winery and one of the Wachau's most philosophically distinctive estates, farmed biodynamically since 1971, producing wines of extraordinary mineral purity and age-worthiness from some of the region's oldest vines. Their late-released Riesling Vinothek wines are considered among Austria's most complex and long-lived whites.")
prod4b, new4b = PROD("Nikolaihof Wachau Gruner Veltliner Smaragd Steiner Hund", "wine_still", p4b, r4, "Austria",
    subcategory="Grüner Veltliner",
    description="A benchmark biodynamic Grüner Veltliner Smaragd from Nikolaihof's oldest vines in the legendary Steiner Hund vineyard — showing the variety's white pepper and grapefruit signature with extraordinary mineral depth from ancient granite soils and the mineral purity that comes from decades of biodynamic farming.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Boiled Tafelspitz beef with horseradish cream and chives", "complement", "classic", "main", "Austria's most revered beef dish and its most celebrated white grape — the white pepper and mineral acidity of Grüner Veltliner cut through the beef broth richness and echo the horseradish heat.")
    PAIR(prod4b, "Asparagus with Hollandaise and smoked salmon", "complement", "classic", "starter", "The quintessential Grüner Veltliner pairing — white asparagus and Hollandaise butter sauce; the wine's white pepper note and acidity are the definitive companion.")
    PAIR(prod4b, "Seared sea scallops with pea and mint risotto", "complement", "established", "main", "The wine's mineral precision and herbal white pepper note frame scallop sweetness and spring green richness with elegant restraint.")
    PAIR(prod4b, "Gruyere cheese fondue with kirsch and bread cubes", "complement", "adventurous", "main", "An Austrian-Swiss border pairing — the wine's acidity cuts through rich melted cheese while the white pepper note bridges the kirsch cherry spirit.")

# ── 5. Finger Lakes (USA/New York) ────────────────────────────────────────────
print("\n=== Finger Lakes (USA) ===")
r5 = R("Finger Lakes", "USA",
    beverage_family="wine",
    designation_type="AVA",
    designation_name="Finger Lakes AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="New York State's most important fine wine region, centred on the deep glacial lakes of central New York whose modulating thermal effect enables viticulture in an otherwise challenging continental climate. The Finger Lakes produce America's finest Rieslings — rivalling those of Germany and Alsace in complexity and age-worthiness — alongside excellent Chardonnay, Cabernet Franc and Pinot Noir. The region has attracted exceptional talent and investment, establishing itself as one of the world's most exciting emerging Riesling destinations.",
    key_producers="Dr. Konstantin Frank, Hermann J. Wiemer, Red Newt Cellars, Ravines Wine Cellars, Standing Stone Vineyards",
    historical_context="Dr. Konstantin Frank, a Ukrainian viticulturalist who emigrated to the USA in 1951, proved that vinifera vines could survive the Finger Lakes winters and established the region's potential for world-class wine. His namesake winery, founded in 1962, remains the benchmark. The region's deep shale soils — Seneca, Cayuga and Keuka Lakes — provide mineral-rich terroir that gives Finger Lakes Riesling its distinctive slate and citrus character, now recognised internationally as America's finest expression of the variety.")

VIN(r5, 2023, "excellent", "stable", "Outstanding year for dry and off-dry Riesling; exceptional mineral precision and aromatic clarity")
VIN(r5, 2022, "very_good", "stable", "Warmer year; ripe and generous Riesling with good sugar-acid balance and stone fruit character")
VIN(r5, 2021, "excellent", "stable", "Elegant and precise; benchmark year for Finger Lakes Riesling at all levels of sweetness")
VIN(r5, 2020, "good", "stable", "Challenging season but skilled producers made clean, characterful wines of good drinking")
VIN(r5, 2019, "exceptional", "rising", "One of the finest Finger Lakes vintages in memory; concentrated, mineral Riesling of extraordinary aging potential")

p5a = P("Hermann J. Wiemer Vineyard", "USA", r5, description="One of the Finger Lakes' most revered and internationally celebrated producers, Hermann J. Wiemer (a German-trained viticulturalist) established the benchmark for Finger Lakes Riesling with his meticulously farmed Seneca Lake estate, producing dry Rieslings of world-class mineral precision that have drawn comparison with the finest German Spätlese and Auslese.")
prod5a, new5a = PROD("Hermann J. Wiemer Dry Riesling Seneca Lake Finger Lakes AVA", "wine_still", p5a, r5, "USA",
    subcategory="Riesling",
    description="The defining expression of dry Finger Lakes Riesling — extraordinary slate and citrus mineral precision, white peach, lime zest and a laser-sharp acidity that rewards 10–15 years of ageing and has established the Finger Lakes as America's most serious Riesling region.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Seared New York Hudson Valley foie gras with quince", "complement", "classic", "starter", "The wine's powerful acidity and mineral precision cut through foie gras richness while the quince element bridges its delicate off-dry fruit.")
    PAIR(prod5a, "Lake trout with brown butter and toasted almonds", "complement", "classic", "main", "Finger Lakes' own native fish with its most celebrated wine — mineral Riesling and lake trout create the region's most natural and elegant pairing.")
    PAIR(prod5a, "Spicy Thai prawn curry with jasmine rice", "contrast", "established", "main", "The wine's mineral acidity and touch of residual sugar provide the perfect contrast and cleanse for Thai chilli heat and coconut cream richness.")
    PAIR(prod5a, "Rillette of smoked whitefish with rye crackers", "complement", "established", "starter", "Smoked lake fish and the mineral precision of Finger Lakes Riesling create a regionally authentic pairing of exceptional harmony and simplicity.")

p5b = P("Dr. Konstantin Frank Winery", "USA", r5, description="The pioneering estate that established the Finger Lakes as a serious vinifera wine region, founded by Ukrainian immigrant Dr. Konstantin Frank in 1962. Now led by the third generation, the winery continues to produce benchmark Rieslings, Pinot Noir and sparkling wines from their Lake Keuka estate vineyards.")
prod5b, new5b = PROD("Dr. Konstantin Frank Riesling Finger Lakes AVA", "wine_still", p5b, r5, "USA",
    subcategory="Riesling",
    description="The flagship Riesling from the estate that created the Finger Lakes wine tradition — showing the region's characteristic combination of pure citrus-mineral character, Keuka Lake slate terroir and vibrant acidity in an accessible, food-versatile style that has been America's gateway to fine Finger Lakes Riesling for over six decades.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "New England clam chowder with oyster crackers", "complement", "established", "main", "The wine's mineral salinity and refreshing acidity provide the perfect counterpoint to cream-based New England seafood chowder.")
    PAIR(prod5b, "Apple cider-braised pork belly with sauerkraut", "complement", "classic", "main", "The wine's Riesling character bridges apple and pork with natural affinity while its acidity cuts through pork belly's richness.")
    PAIR(prod5b, "Grilled oysters with mignonette and horseradish", "complement", "classic", "starter", "Mineral Riesling and fresh oysters are among wine and food's most elemental pairings; the wine's slate character mirrors the oyster's saline depth.")
    PAIR(prod5b, "Aged New York State cheddar with apple butter", "complement", "classic", "cheese", "A New York State celebration — the region's most iconic white wine with its most celebrated aged cheese, linked by apple fruit and mineral acidity.")

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
print("\nDone.")
conn.close()
