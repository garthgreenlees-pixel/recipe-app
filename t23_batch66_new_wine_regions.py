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

# ── REGION 1: Franken (Germany/Bavaria) ──────────────────────────────────────
print("\n=== Region 1: Franken ===")
r1 = R("Franken", "Germany", "wine",
    designation_type="Anbaugebiet", designation_name="Franken",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Franken (Franconia) is Germany's most distinctive wine region, using the unique Bocksbeutel (flat-sided flask) for its top wines — among the world's oldest bottle shapes. Silvaner is the signature variety, producing earthy, mineral, and herbal whites that are unmatched in Germany for food versatility. Müller-Thurgau and Riesling are also produced, and a small but serious Spätburgunder tradition exists.",
    key_producers="Weingut Horst Sauer, Bürgerspital, Juliusspital, Rudolf Fürst",
    historical_context="Franken's wine tradition dates to the 8th century with Frankish nobility planting vines along the Main River. The Bocksbeutel was officially adopted in 1728 — among the world's oldest protected wine bottle shapes. The region's cool-continental climate and unique soils (Muschelkalk limestone, Keuper sandstone, and Buntsandstein) give Silvaner a mineral precision found nowhere else. Rudolf Fürst's Spätburgunder from volcanic Keuper soils has attracted serious international attention.")

VIN(r1, 2022, "excellent", "rising", "Outstanding Franken vintage; Silvaner achieved exceptional mineral concentration from the Muschelkalk terroir with fine aromatic depth")
VIN(r1, 2021, "very_good", "stable", "Fine balanced year with classic Silvaner character; good herbaceous mineral depth and food-friendly acidity")
VIN(r1, 2020, "good", "stable", "Accessible year with good typicity; fresh, earthy Silvaner with characteristic herbal mineral note")
VIN(r1, 2019, "excellent", "rising", "Benchmark Franken vintage; extraordinary Silvaner mineral precision from the Muschelkalk limestone soils")
VIN(r1, 2018, "very_good", "stable", "Classic vintage with excellent structure; Silvaner GGs showing remarkable 10-year aging capability")

prod1a_id = P("Weingut Horst Sauer", "Germany", r1, "winery",
    "One of Franken's most celebrated estates; Horst Sauer's Escherndorfer Lump Silvaner and Riesling from the steep Muschelkalk terraces above the Main River are among Germany's most mineral and ageworthy white wines — achieving Großes Gewächs status with complete authority.")
prod1a, new1a = PROD("Horst Sauer Escherndorfer Lump Silvaner GG", "wine_still", prod1a_id, r1, "Germany",
    subcategory="white", price_tier="premium",
    description="The benchmark Franken Silvaner from Sauer's flagship Escherndorfer Lump vineyard on Muschelkalk limestone; earthy, herbal, and profoundly mineral. White pepper, green tomato vine, chalk mineral, and a saline freshness unique to Franken's limestone terroir. Großes Gewächs designation confirms its premier cru status.")
if new1a:
    PAIR(prod1a, "Wiener Schnitzel mit Kartoffelsalat und Preiselbeeren", "complement", "classic", "main",
        "The Austro-German bistro classic of veal schnitzel, potato salad, and cranberry sauce is Silvaner's great food match; the wine's acidity cuts through the breadcrumb coating")
    PAIR(prod1a, "Spargel mit Sauce hollandaise und Schinken (white asparagus season)", "complement", "classic", "starter",
        "Germany's spring asparagus with hollandaise is inseparable from Silvaner; the wine's herbal mineral character mirrors the asparagus's vegetal richness perfectly")
    PAIR(prod1a, "Mainfränkischer Zwiebelkuchen (Frankish onion tart) with Speck", "complement", "classic", "starter",
        "Franconian onion tart with cured pork is the regional Silvaner pairing par excellence; the wine's mineral freshness cuts through the rich onion custard")
    PAIR(prod1a, "Forelle Müllerin Art (pan-fried trout) with lemon butter and almonds", "complement", "classic", "fish_course",
        "River trout prepared Müllerin-style with almond butter is the classic Main River freshwater fish pairing for mineral Franken Silvaner")

prod1b_id = P("Rudolf Fürst", "Germany", r1, "winery",
    "Franken's most celebrated red wine producer; Paul Fürst's single-vineyard Spätburgunder from volcanic Keuper sandstone has achieved cult status, producing elegant Pinot Noirs that challenge Burgundy premier cru — and Germany's best red wines — at extraordinary prices for the region.")
prod1b, new1b = PROD("Rudolf Fürst Centgrafenberg Spätburgunder GG", "wine_still", prod1b_id, r1, "Germany",
    subcategory="red", price_tier="ultra_premium",
    description="Rudolf Fürst's legendary Centgrafenberg Spätburgunder from volcanic Keuper sandstone; Germany's most celebrated red wine from outside traditional Pinot regions. Extraordinary silky tannin, dark cherry, violet, and volcanic mineral precision with 20-year aging potential. Allocated and sought globally.")
if new1b:
    PAIR(prod1b, "Rehrücken (roast saddle of venison) with black cherry and juniper cream", "complement", "classic", "main",
        "German roast venison with black cherry is the definitive Fürst Spätburgunder pairing; the wine's cherry depth and volcanic mineral match the game's complexity")
    PAIR(prod1b, "Wild duck breast with Schwarzwälder Kirschtorte reduction and red cabbage", "complement", "established", "main",
        "Wild duck with Black Forest cherry reduction creates a game-fruit pairing that amplifies Fürst's Pinot Noir's cherry depth and mineral precision")
    PAIR(prod1b, "Aged Frankenkäse with cherry jam and dark rye bread", "bridge", "established", "cheese",
        "Regional Franconian cheese with cherry jam bridges the Centgrafenberg's dark fruit; dark rye bread's earthy character echoes the volcanic Keuper terroir")
    PAIR(prod1b, "Taube (wood pigeon) with lentilles du Puy and smoked bacon", "complement", "established", "main",
        "Wood pigeon's depth and lentil earthiness are natural vehicles for Fürst's silky, complex Pinot Noir; smoked bacon adds savouriness to echo the volcanic mineral")

# ── REGION 2: Kremstal DAC (Austria) ────────────────────────────────────────
print("\n=== Region 2: Kremstal ===")
r2 = R("Kremstal", "Austria", "wine",
    designation_type="DAC", designation_name="Kremstal DAC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Kremstal is one of Lower Austria's finest wine regions, centred on the Danube River around the medieval city of Krems. Grüner Veltliner and Riesling dominate from loess and primary rock (gneiss and granite) terroirs, producing wines of comparable mineral complexity to the neighbouring Wachau but with more accessibility and value. The Kremstal DAC was established in 2003.",
    key_producers="Nigl, Salomon Undhof, Stadt Krems, Weingut Loimer",
    historical_context="Winemaking around Krems dates to at least the Celts and Romans; documentary evidence goes back to the 8th century. The medieval city of Krems was a major wine trading hub in the Middle Ages. The Kremstal DAC system (established 2003) was among Austria's first regional wine designations, protecting and defining the quality hierarchy from Kremstal to Ortswein to Riedenwein (single-vineyard).")

VIN(r2, 2022, "excellent", "rising", "Outstanding Kremstal vintage; exceptional Grüner Veltliner concentration and mineral precision from both loess and primary rock terroirs")
VIN(r2, 2021, "very_good", "stable", "Fine balanced year with elegant, mineral Kremstal wines; Riesling particularly successful with excellent acidity and citrus depth")
VIN(r2, 2020, "good", "stable", "Good vintage with characteristic Grüner Veltliner pepper and mineral freshness at accessible quality")
VIN(r2, 2019, "excellent", "rising", "Benchmark Kremstal vintage; extraordinary mineral precision especially from primary rock sites above the Danube")
VIN(r2, 2018, "very_good", "stable", "Classic vintage with excellent structure and aging potential; Riesling single-vineyard wines showing remarkable 10-year capability")

prod2a_id = P("Nigl", "Austria", r2, "winery",
    "Kremstal's benchmark estate for single-vineyard Grüner Veltliner and Riesling; Martin Nigl's biodynamic estate on primary rock (gneiss and granite) above Senftenberg produces some of Lower Austria's most mineral and elegant wines — consistently among Austria's finest at any price.")
prod2a, new2a = PROD("Nigl Privat Grüner Veltliner", "wine_still", prod2a_id, r2, "Austria",
    subcategory="white", price_tier="premium",
    description="Nigl's flagship Privat Grüner Veltliner: the estate's finest old-vine selection from gneiss terraces above the Danube. White pepper, citrus peel, grapefruit, and a gneiss mineral tension of extraordinary precision. Among Austria's greatest Grüner Veltliners — structured for 15+ year evolution.")
if new2a:
    PAIR(prod2a, "Wachauer Marillenkuchen (Danube Valley apricot cake) with whipped cream", "complement", "adventurous", "dessert",
        "Danube Valley apricot cake with cream contrasts dry Grüner's pepper with the fruit's sweetness — an unusual but genuinely Austrian dessert pairing")
    PAIR(prod2a, "Zander (pike-perch) with dill, capers, and potato mousseline", "complement", "classic", "fish_course",
        "Danube River pike-perch with dill is the archetypal Kremstal fish pairing; Nigl's mineral Grüner mirrors the river's terroir character")
    PAIR(prod2a, "Tafelspitz mit Kernöl und Rösterdäpfl (Austrian boiled beef with pumpkin seed oil)", "complement", "classic", "main",
        "Austria's great boiled beef with pumpkin seed oil and fried potatoes needs Grüner Veltliner's pepper and acidity to balance; a classic Austrian fine dining pairing")
    PAIR(prod2a, "Topfenstrudel mit Schlagobers (Austrian curd cheese strudel with cream)", "contrast", "adventurous", "dessert",
        "Curd cheese strudel's slight sweetness contrasts Nigl's dry mineral Grüner in a traditional Austrian restaurant dessert wine pairing")

prod2b_id = P("Salomon Undhof", "Austria", r2, "winery",
    "One of Kremstal's oldest and most respected estates; Bert Salomon's historic estate beneath the Kremstal's famous Kögl vineyard produces single-site Grüner Veltliner and Riesling of benchmark mineral precision — representing Kremstal's historic quality identity with consistency.")
prod2b, new2b = PROD("Salomon Lindberg Grüner Veltliner", "wine_still", prod2b_id, r2, "Austria",
    subcategory="white", price_tier="mid_range",
    description="Salomon Undhof's single-vineyard Lindberg Grüner Veltliner: loess terroir producing full, textural Grüner with characteristic pepper, peach, and mineral depth. The estate's accessible expression of Kremstal's quality at an honest price — food-friendly and versatile.")
if new2b:
    PAIR(prod2b, "Zwiebelrostbraten (Austrian roast beef with caramelised onion gravy) and Erdäpfelpüree", "complement", "classic", "main",
        "Austrian beef with onion gravy and potato purée is a natural match for Kremstal Grüner's pepper and mineral structure — a Viennese restaurant staple pairing")
    PAIR(prod2b, "Käsespätzle mit Bergkäse und Röstzwiebeln (cheese egg noodles)", "complement", "established", "main",
        "Allgäu-style cheese noodles with caramelised onions is Austria's greatest comfort food; Grüner's pepper and freshness cuts through the cheese richness perfectly")
    PAIR(prod2b, "Grüner Veltliner Sülze (wine jelly terrine) with horseradish and mustard", "complement", "established", "starter",
        "Regional wine terrine using Grüner Veltliner — a Kremstal speciality — pairs obviously and authentically with the same wine from Salomon Undhof")
    PAIR(prod2b, "Grilled sea bream with lemon, fennel, and Austrian pumpkin seed oil", "complement", "established", "fish_course",
        "Mediterranean grilled fish with Austrian pumpkin seed oil and fennel bridges the wine's mineral freshness with the seed's nutty depth — an elegant fusion")

# ── REGION 3: Egri Bikavér (Hungary/Eger) ────────────────────────────────────
print("\n=== Region 3: Egri Bikavér ===")
r3 = R("Egri Bikavér", "Hungary", "wine",
    designation_type="PDO", designation_name="Egri Bikavér PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Egri Bikavér ('Bull's Blood of Eger') is Hungary's most internationally famous red wine, produced in the historic wine city of Eger in northern Hungary. A blend of at least three varieties from a permitted list including Kékfrankos (Blaufränkisch), Kadarka, Cabernet Franc, and Merlot. The Premium tier was established in 2004 with stricter requirements. The wines show dark fruit, paprika spice, herb, and volcanic mineral character.",
    key_producers="GIA (Gróf Buttler), Thummerer, St. Andrea, Bolyki",
    historical_context="The legend of Bull's Blood dates to 1552 when Ottoman invaders allegedly mistook the defenders' red wine for bull's blood and retreated in terror. The wine's international fame peaked in the communist era when it was widely exported. After decades of dilution with cheap mass production, a quality renaissance began in the 1990s-2000s with the Premium designation system recognising small-production quality estates.")

VIN(r3, 2022, "excellent", "rising", "Outstanding Eger vintage; Kékfrankos achieved exceptional concentration and volcanic mineral depth from the hillside terraces")
VIN(r3, 2021, "very_good", "stable", "Fine balanced year with classic Bikavér character; good dark fruit and paprika-herb complexity")
VIN(r3, 2020, "good", "stable", "Accessible vintage with soft tannins; dark cherry and herb character with good everyday typicity")
VIN(r3, 2019, "excellent", "rising", "Benchmark Eger vintage; Premium Bikavér showing extraordinary complexity and aging potential beyond the appellation's typical horizon")
VIN(r3, 2018, "very_good", "stable", "Classic year with excellent structure; Kékfrankos tannins firm and ripe with good aging capability")

prod3a_id = P("St. Andrea", "Hungary", r3, "winery",
    "One of Eger's most celebrated and quality-focused estates; György Lőrincz's St. Andrea produces premium Egri Bikavér from high-altitude volcanic tuff and basalt terraces, achieving a complexity and age-worthiness that defines the denomination's potential beyond its everyday reputation.")
prod3a, new3a = PROD("St. Andrea Merengő Egri Bikavér Premium", "wine_still", prod3a_id, r3, "Hungary",
    subcategory="red", price_tier="premium",
    description="St. Andrea's flagship Premium Bikavér from single hillside parcels above Eger; Kékfrankos dominant with Kadarka, Cabernet Franc, and Merlot on volcanic tuff. Dark cherry, paprika, thyme, and volcanic mineral depth — a wine that challenges the simplistic 'Bull's Blood' reputation and reveals Hungary's red wine potential.")
if new3a:
    PAIR(prod3a, "Marhapörkölt (Hungarian beef goulash) with tarhonyakocka and sour cream", "complement", "classic", "main",
        "Hungarian beef goulash with its paprika-onion depth and egg pasta is the definitive Egri Bikavér food pairing; the wine's paprika character creates direct resonance")
    PAIR(prod3a, "Töltött káposzta (stuffed cabbage with pork and rice in tomato-paprika sauce)", "complement", "classic", "main",
        "Stuffed cabbage with paprika sauce is Hungary's great comfort dish; Bikavér's structure and dark fruit complement the dish's acidity and pork richness")
    PAIR(prod3a, "Lamb pörkölt with green peppers and nokedli (Hungarian egg dumplings)", "complement", "classic", "main",
        "Lamb goulash with paprika and dumplings is a more refined expression of Hungarian comfort food that matches Bikavér Premium's depth and volcanic mineral")
    PAIR(prod3a, "Pálinka-marinated wild boar with roasted beets and walnut salsa", "complement", "established", "main",
        "Wild boar marinated in Hungarian fruit brandy with beet's earthiness echoes Bikavér's volcanic mineral depth and dark fruit complexity")

prod3b_id = P("Thummerer Vilmos", "Hungary", r3, "winery",
    "A highly regarded Eger estate producing benchmark Egri Bikavér and varietal wines; Vilmos Thummerer's family estate has been building quality from small hillside plots, producing some of the denomination's most consistent and food-friendly expressions at accessible prices.")
prod3b, new3b = PROD("Thummerer Egri Bikavér", "wine_still", prod3b_id, r3, "Hungary",
    subcategory="red", price_tier="mid_range",
    description="Thummerer's reliable everyday Bikavér: Kékfrankos with Kadarka and Merlot producing an approachable dark cherry and paprika-spiced red with soft tannins. The accessible face of Eger's Bull's Blood tradition — food-friendly, authentic, and excellent value for the quality.")
if new3b:
    PAIR(prod3b, "Gulyásleves (Hungarian goulash soup) with crusty bread", "complement", "classic", "casual",
        "Hungary's iconic goulash soup is the everyday casual pairing for Thummerer's accessible Bikavér; paprika-beef broth and the wine share the same aromatic register")
    PAIR(prod3b, "Langos with sour cream, grated cheese, and smoked sausage", "complement", "established", "casual",
        "Hungary's deep-fried bread with sour cream toppings — the street food classic — meets Bikavér's soft tannins and dark fruit in a casual Budapest market pairing")
    PAIR(prod3b, "Csirkepaprikás (Hungarian chicken paprikash) with sour cream and pasta", "complement", "classic", "main",
        "Chicken paprikash is Hungary's most beloved dish; the creamy paprika sauce and soft Bikavér's dark fruit is a deeply satisfying regional match")
    PAIR(prod3b, "Hortobágyi palacsinta (Hortobágy veal crêpes with paprika sauce)", "complement", "classic", "starter",
        "Thin crêpes stuffed with veal in paprika sauce is one of Hungary's most refined traditional dishes; Bikavér's fruit and structure complement the dish's delicacy")

# ── REGION 4: Villány (Hungary) ──────────────────────────────────────────────
print("\n=== Region 4: Villány ===")
r4 = R("Villány", "Hungary", "wine",
    designation_type="PDO", designation_name="Villány PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Villány is Hungary's warmest wine region, set in the far south near Croatia on ancient loess and red clay soils. The region produces Hungary's most internationally recognised single-variety reds from Cabernet Franc, Cabernet Sauvignon, Merlot, and the indigenous Portugieser — wines of considerable depth, elegance, and aging potential that have attracted serious international critical attention.",
    key_producers="Attila Gere, Malatinszky, Vylyan, Bock",
    historical_context="Villány's viticulture dates to Roman times; the town of Villány sits directly on an ancient Roman road. Modern quality winemaking began in earnest after 1989 when private estate bottling became possible following the end of the communist cooperative system. Attila Gere's pioneering work in the 1990s established the region's international reputation, and Villány Cabernet Franc has become a benchmark for the variety outside France and Italy.")

VIN(r4, 2022, "excellent", "rising", "Outstanding vintage for Villány; Cabernet Franc achieved exceptional ripeness and violet-herb complexity on the warm southern terroir")
VIN(r4, 2021, "very_good", "stable", "Fine balanced year with elegant Villány character; dark cherry and herb complexity with good acid-tannin structure")
VIN(r4, 2020, "excellent", "rising", "Hot year producing powerful, concentrated reds with exceptional depth; age-worthy Cabernet-based wines")
VIN(r4, 2019, "very_good", "rising", "Benchmark Villány vintage; extraordinary Cabernet Franc complexity with 15+ year aging potential on the finest sites")
VIN(r4, 2018, "good", "stable", "Accessible year with good typicity; softer tannins and inviting dark fruit character for earlier drinking pleasure")

prod4a_id = P("Attila Gere", "Hungary", r4, "winery",
    "The founding figure of Villány's international reputation; Attila Gere's estate produces benchmark Cabernet Franc and Merlot-dominant blends from the region's finest loess and red clay terraces — wines that introduced Villány to the global wine press in the 1990s.")
prod4a, new4a = PROD("Attila Gere Kopar Villány Cuvée", "wine_still", prod4a_id, r4, "Hungary",
    subcategory="red", price_tier="premium",
    description="Gere's flagship Kopar blend: Cabernet Franc, Merlot, and Cabernet Sauvignon from the finest Villány red clay and loess parcels. Dark cherry, violet, cedar, and Mediterranean herb complexity with impressive structure. The wine that established Villány's international credibility and Hungary's red wine potential.")
if new4a:
    PAIR(prod4a, "Rack of lamb with herb crust, red pepper sauce, and Villány lentils", "complement", "classic", "main",
        "Southern Hungarian lamb with herb crust and the region's lentils is a precise regional match for Gere's Cabernet Franc-dominant Kopar")
    PAIR(prod4a, "Libamáj (Hungarian foie gras) with Tokaji reduction and brioche", "complement", "classic", "starter",
        "Hungary's celebrated domestic goose foie gras with Tokaji glaze creates a luxury pairing with Kopar; the wine's dark fruit and herb complexity meet the foie's richness")
    PAIR(prod4a, "Slow-braised ox cheeks with truffle polenta and roasted garlic", "complement", "established", "main",
        "Ox cheek's gelatinous richness requires Kopar's structured tannin; truffle amplifies the Cabernet Franc's earthy violet complexity")
    PAIR(prod4a, "Aged Manchego with quince paste and dark chocolate", "bridge", "established", "cheese",
        "Aged sheep cheese with quince and chocolate bridges Villány's dark fruit and herb character — a sophisticated Central European cheese course pairing")

prod4b_id = P("Malatinszky", "Hungary", r4, "winery",
    "One of Villány's most ambitious and internationally recognised boutique estates; Csaba Malatinszky's estate produces a small range of premium single-vineyard wines from Cabernet Franc, Cabernet Sauvignon, and Merlot that achieve exceptional concentration and elegance.")
prod4b, new4b = PROD("Malatinszky Kúria Villány Cabernet Franc", "wine_still", prod4b_id, r4, "Hungary",
    subcategory="red", price_tier="premium",
    description="Malatinszky's single-variety Cabernet Franc from the estate's finest loess parcels; violet, dark cherry, cassis, and Mediterranean herb complexity with fine tannins and an age-worthy structure. Among Hungary's most internationally recognised Cabernet Franc expressions — showing what the variety can achieve on Hungarian terroir.")
if new4b:
    PAIR(prod4b, "Grilled duck breast with cherry sauce and sautéed chanterelles", "complement", "classic", "main",
        "Duck's fat richness and cherry sauce mirror Cabernet Franc's violet-cherry core; chanterelle's earthiness adds forest depth to echo the wine's herb character")
    PAIR(prod4b, "Borsos bárány (pepper-spiced lamb) with roasted red peppers and herb yoghurt", "complement", "classic", "main",
        "Spiced lamb with roasted Villány peppers (the region's other great product) creates a perfect local pairing for the estate's Cabernet Franc")
    PAIR(prod4b, "Wild mushroom pörkölt with nockerl and sour cream", "complement", "established", "main",
        "Hungarian mushroom goulash with light sour cream is an elegant meat-free match for Villány Cabernet Franc's herb and mineral depth")
    PAIR(prod4b, "Trappista cheese with green pepper jam and walnut bread", "bridge", "established", "cheese",
        "Hungarian Trappist cheese with sweet pepper jam and walnut bread creates a regional cheese course for Malatinszky's Cabernet Franc")

# ── REGION 5: Priorat DOQ (Spain/Catalonia) ──────────────────────────────────
print("\n=== Region 5: Priorat ===")
r5 = R("Priorat", "Spain", "wine",
    designation_type="DOQ", designation_name="Priorat DOQ",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Priorat is Spain's second DOQ (after Rioja) and one of the world's most distinctive wine terroirs — a remote mountainous enclave in Catalonia where Grenache and Carignan grow on llicorella schist (slate with mica flakes) producing wines of extraordinary concentration, mineral complexity, and age-worthiness. The wines can be among Spain's most expensive and are ranked alongside top Bordeaux and Burgundy in international markets.",
    key_producers="Álvaro Palacios, Clos Mogador, Clos de l'Obac (Costers del Siurana), Mas Doix",
    historical_context="The Carthusian monks of Escaladei established viticulture in Priorat in the 12th century. The region fell into near-abandonment after phylloxera in the late 19th century until a legendary group of seven producers — the 'Grup de Set' — led by René Barbier and Álvaro Palacios revived the region from 1989. Their Clos estates became internationally recognised, and Priorat's prices climbed from nothing to global prestige within a decade.")

VIN(r5, 2022, "excellent", "rising", "Outstanding Priorat vintage; old vine Garnacha on llicorella achieved exceptional mineral concentration and aging structure")
VIN(r5, 2021, "very_good", "stable", "Fine balanced year with classic Priorat mineral depth; Garnacha-Carignan blends showing elegant structure")
VIN(r5, 2020, "excellent", "rising", "Powerful vintage; densely concentrated wines with the llicorella's mineral intensity at its most profound")
VIN(r5, 2019, "very_good", "rising", "Benchmark Priorat vintage; extraordinary depth and complexity from old-vine Garnacha on slate schist")
VIN(r5, 2016, "exceptional", "rising", "One of the great modern Priorat vintages; age-worthy wines with extraordinary llicorella mineral character and 30+ year potential")

prod5a_id = P("Álvaro Palacios", "Spain", r5, "winery",
    "The co-creator of modern Priorat; Álvaro Palacios's L'Ermita — from 100+ year old Garnacha vines on llicorella schist — is among Spain's most expensive and celebrated wines. His work in reviving Priorat from abandonment in 1989 is one of wine's great modern narratives.")
prod5a, new5a = PROD("Álvaro Palacios Les Terrasses Priorat", "wine_still", prod5a_id, r5, "Spain",
    subcategory="red", price_tier="premium",
    description="Palacios's entry Priorat: Les Terrasses blends Garnacha, Carignan, and Syrah from younger-vine llicorella terraces. Dark cherry, black olive, Mediterranean herb, and mineral slate — an accessible introduction to Palacios's Priorat quality at a fraction of L'Ermita's price but with the same DOQ terroir character.")
if new5a:
    PAIR(prod5a, "Slow-roasted suckling lamb shoulder with romesco and chargrilled vegetables", "complement", "classic", "main",
        "Catalan romesco sauce and lamb is a Priorat classic; the wine's mineral slate and dark fruit mirror the charred flavours while romesco adds roasted pepper depth")
    PAIR(prod5a, "Grilled wild boar with black olive, thyme, and mountain herbs", "complement", "classic", "main",
        "Priorat's mountainous landscape and wild boar with its local herb character creates a direct terroir pairing; the wine's llicorella mineral depth matches the game's complexity")
    PAIR(prod5a, "Fideos negros with squid ink and alioli (Catalan black noodles)", "complement", "established", "main",
        "Catalan black noodle dish with squid ink's saline depth and creamy alioli is an unusual but genuinely regional pairing for the slate mineral character of Les Terrasses")
    PAIR(prod5a, "Aged Garrotxa with fig preserve and toasted hazelnuts", "bridge", "classic", "cheese",
        "Semi-aged Catalan goat cheese with fig bridges the wine's dark fruit; hazelnuts add local mountain nuttiness to echo the llicorella's mineral depth")

prod5b_id = P("Clos Mogador", "Spain", r5, "winery",
    "One of Priorat's founding estates and most celebrated names; René Barbier's Clos Mogador has produced benchmark llicorella Garnacha since 1989. The wine's quality and complexity have established Priorat's global reputation alongside Álvaro Palacios's L'Ermita.")
prod5b, new5b = PROD("Clos Mogador Priorat", "wine_still", prod5b_id, r5, "Spain",
    subcategory="red", price_tier="ultra_premium",
    description="René Barbier's benchmark Priorat: old vine Garnacha, Carignan, Cabernet Sauvignon, and Syrah from llicorella schist. Extraordinary mineral depth — slate, black olive, dried herbs, dark cherry — with the concentration and structure for 25-30 year aging. One of Spain's most historically significant wines.")
if new5b:
    PAIR(prod5b, "Rack of lamb with coal-roasted garlic, herbs de Provence, and anchovy jus", "complement", "classic", "main",
        "Anchovy-herb lamb roasted over coal matches Clos Mogador's Mediterranean depth precisely; anchovy's umami amplifies the wine's mineral concentration")
    PAIR(prod5b, "Duck confit with lentilles du Puy and Larousses sauce (Catalan style)", "complement", "established", "main",
        "Duck confit's rendered fat and earthy lentils need Mogador's tannic concentration to balance; Catalan sauce adds herbal Mediterranean depth")
    PAIR(prod5b, "Truffle risotto with aged Parmigiano Reggiano and white truffle oil", "complement", "adventurous", "main",
        "Black truffle's earthy depth amplifies Mogador's llicorella mineral character; Parmigiano adds umami salinity to match the wine's extraordinary concentration")
    PAIR(prod5b, "Aged Manchego Reserva with Pedro Ximénez raisins and walnuts", "bridge", "classic", "cheese",
        "Mature Manchego with sweet-raisin PX creates the Spanish luxury cheese pairing for Clos Mogador's power and mineral slate depth")

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
