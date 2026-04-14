#!/usr/bin/env python3
"""B171 — Diverse global: Lodi AVA, Mount Veeder AVA, Valle de Guadalupe MX, Canelones DO Uruguay, Nashik Valley India"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
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

# === LODI AVA ===
print("=== Lodi AVA ===")
r1 = R("Lodi AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Lodi American Viticultural Area",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Lodi in the California Central Valley is the American capital of old-vine Zinfandel, with some vines dating to the 1880s-1900s still producing intensely flavoured wine. The region's Mediterranean climate, modified by cooling Delta breezes from San Francisco Bay, allows Zinfandel and other warm-climate varieties to ripen fully while retaining freshness. Sandy loam soils over hard-pan retain moisture through dry summers. Turley Wine Cellars and Michael David Winery have elevated Lodi from bulk wine source to premium wine destination.",
       key_producers="Turley Wine Cellars, Michael David Winery, Jessie's Grove, Markus Wine Co, LangeTwins Family",
       historical_context="Lodi wine production dates to the 1850s when German and Italian immigrants brought Zinfandel cuttings. The region supplied most of California's home winemakers during Prohibition due to Zinfandel's thick skin (good for shipping). Post-Prohibition, Lodi became the source of much of California's bulk wine, but a quality revolution began in the 1990s as old-vine advocates recognised the region's ancient Zinfandel heritage.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Lodi vintage — old-vine Zinfandel of extraordinary concentration with freshness preserved by Delta breezes."),
    (2019,"very_good","stable","Good vintage; ancient vine Zinfandel showing characteristic brambly intensity."),
    (2020,"excellent","rising","Outstanding year; Lodi Zinfandel achieving national recognition for quality."),
    (2021,"very_good","stable","Fine conditions; old-vine wines of deep colour and ripe, complex fruit."),
    (2022,"excellent","rising","Exceptional vintage for old-vine Zinfandel — some of the finest in recent Lodi history."),
    (2023,"very_good","stable","Good vintage; consistent quality from heritage vine producers across the AVA."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Turley Wine Cellars Lodi", "winery", r1, "USA",
       production_philosophy="minimal_intervention",
       philosophy_description="Larry Turley is America's foremost Zinfandel producer, farming over 60 old and ancient vine Zinfandel vineyards across California with a focus on minimal intervention and natural fermentation. His Lodi vineyards — including the legendary Dogtown and Kirschenmann — contain some of the oldest producing vines in America.",
       reputation_narrative="Turley Wine Cellars has transformed perceptions of Zinfandel from simple pizza wine to world-class terroir-driven expression. Their old-vine single-vineyard wines, particularly from Lodi's ancient vine sites, are among California's most sought-after wines and age magnificently for 15+ years.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Turley Dogtown Vineyard Old Vine Zinfandel Lodi", "wine_still", p1, r1, "USA",
                    subcategory="red", description="Ancient vine Zinfandel from the Dogtown Vineyard's pre-Prohibition plantings on sandy loam. Intensely brambly — blackberry, boysenberry, black pepper, chocolate, and the distinctive 'wild' character of very old vine Zinfandel. Despite high alcohol, remarkable freshness from Delta breezes.", price_tier="premium")
if is_new:
    PAIR(prod, "Slow-smoked pork ribs with BBQ sauce", "complement", "classic", "main", "Old-vine Zinfandel is America's BBQ wine — the ripe fruit and spice perfectly mirror smoky pork ribs.")
    PAIR(prod, "Grilled lamb burgers with blue cheese and caramelised onion", "complement", "established", "main", "Brambly Zinfandel and blue cheese create bold flavour contrast; caramelised onion bridges the wine's sweetness.")
    PAIR(prod, "Braised short rib with wild mushrooms and polenta", "complement", "classic", "main", "Ancient vine concentration demands collagen-rich braised beef; mushrooms bridge the wine's earthy depth.")
    PAIR(prod, "Chocolate and cherry tart with vanilla cream", "complement", "adventurous", "dessert", "Old-vine Zinfandel's fruit density bridges dark chocolate; cherry echoes the wine's boysenberry character.")
prod, is_new = PROD("Michael David Earthquake Old Vine Zinfandel Lodi", "wine_still", p1, r1, "USA",
                    subcategory="red", description="Michael David's flagship old-vine Zinfandel — 'Earthquake' for its shaking intensity. Deep purple, opulent: boysenberry jam, chocolate, coffee, and a full-bodied richness from 100+ year old Delta-cooled vines. California's most famous value Zinfandel.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Pepperoni pizza with extra cheese and basil", "complement", "classic", "main", "Zinfandel and pizza is one of California's great informal pairings — spice in both wine and topping creates harmony.")
    PAIR(prod, "Grilled Italian sausage with peppers and onions", "complement", "classic", "main", "The Italian-American combination — old-vine California Zin and pork sausage is a natural match.")
    PAIR(prod, "Dark chocolate bark with dried cranberry and orange zest", "complement", "established", "dessert", "Rich old-vine Zinfandel's fruit intensity bridges dark chocolate; cranberry echoes the wine's bramble character.")
    PAIR(prod, "Sharp aged cheddar with dried fig chutney", "complement", "established", "cheese", "Boysenberry and chocolate Zinfandel complements aged cheddar's sharpness; fig chutney bridges the wine's sweetness.")

# === MOUNT VEEDER AVA ===
print("=== Mount Veeder AVA ===")
r2 = R("Mount Veeder AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Mount Veeder American Viticultural Area",
       reputation_tier="respected",
       quality_trajectory="established",
       description="Mount Veeder, in the Mayacamas Mountains between Napa and Sonoma at 400–800m elevation, is Napa Valley's most distinctive mountain wine terroir. Thin, volcanic, and extremely well-draining soils produce small-berried, intensely concentrated Cabernet Sauvignon of extraordinary structure and longevity. The altitude's fog and wind influence creates wines of greater freshness and minerality than the valley floor, with notable iron and volcanic mineral character alongside the classic Napa Cabernet dark fruit.",
       key_producers="Mayacamas Vineyards, Hess Collection, Mount Veeder Winery, The Hess Select",
       historical_context="Mount Veeder was one of Napa's first mountain AVAs, granted in 1990. Mayacamas Vineyards has farmed the mountain since 1941 and produces some of California's most historically significant Cabernet Sauvignon — age-worthy, austere, and iron-mineral in their youth, they are completely unlike valley floor Napa Cab.")
for yr, qd, pt, sn in [
    (2017,"excellent","rising","Outstanding mountain vintage — volcanic Cabernet of unusual mineral depth and structure."),
    (2018,"very_good","stable","Good vintage; Mayacamas range showing classic iron-mineral mountain character."),
    (2019,"excellent","rising","Benchmark year for Mount Veeder — wines combining concentration with mountain freshness."),
    (2020,"challenging","stable","Smoke impact at some elevations; lower sites produced good quality."),
    (2021,"excellent","rising","Outstanding conditions; mountain Cabernet of extraordinary longevity potential."),
    (2022,"very_good","stable","Fine vintage; volcanic mineral character well-expressed across the AVA."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Mayacamas Vineyards Mount Veeder", "winery", r2, "USA",
       production_philosophy="minimal_intervention",
       philosophy_description="Mayacamas, founded in 1941, is California's most historically significant mountain winery — their old-vine Cabernet Sauvignon requires 15–20 years to reach peak drinking. The estate's austere, iron-mineral style was considered outdated in the era of Parker scores but is now celebrated as California's most distinctive and age-worthy Cabernet.",
       reputation_narrative="Mayacamas Cabernet Sauvignon from great vintages (1968, 1971, 1973) has been shown to age magnificently for 50+ years — a level of longevity rare in California wine. The estate's revival under new ownership has restored this iron-mineral style to prominence in California's wine culture.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Mayacamas Vineyards Cabernet Sauvignon Mount Veeder", "wine_still", p2, r2, "USA",
                    subcategory="red", description="California's most historically significant mountain Cabernet Sauvignon from old-vine sites at 800m. Austere, iron-mineral, and austere in youth — volcanic iron, graphite, dark cherry, tobacco, and a tannic structure requiring 10–15 years minimum for full expression. 50+ year ageing potential.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Prime dry-aged bone-in ribeye with bone marrow and sea salt", "complement", "classic", "main", "Mountain Cabernet's iron and mineral character demands the finest beef — the wine's structure takes 20 minutes to open.")
    PAIR(prod, "Braised lamb shank with rosemary, garlic and roasted root vegetables", "complement", "classic", "main", "The wine's structure and mineral depth handle long-braised lamb; root vegetables echo the volcanic soil's earthiness.")
    PAIR(prod, "Wild mushroom and beef daube with polenta", "complement", "established", "main", "Iron-mineral Cabernet bridges to mushroom earthiness; slow-braised beef's collagen structure softens the wine's formidable tannins.")
    PAIR(prod, "Aged Parmigiano Reggiano 60-month with truffle", "complement", "classic", "cheese", "The wine's iron character and long tannins need the highest-quality aged cheese; truffle bridges the volcanic mineral depth.")
prod, is_new = PROD("Hess Collection Mount Veeder Cabernet Sauvignon", "wine_still", p2, r2, "USA",
                    subcategory="red", description="Estate Cabernet Sauvignon from Hess's mountain vineyards at Mount Veeder — more accessible than Mayacamas but equally distinctive. Volcanic iron, dark plum, cassis, cedar, and firm mountain tannins. The estate also hosts one of California's finest contemporary art museums.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled T-bone steak with garlic compound butter", "complement", "classic", "main", "Mountain Cabernet's iron and dark fruit stand up to grilled steak; garlic bridges the wine's herbal complexity.")
    PAIR(prod, "Lamb chops with mint crust and roasted garlic jus", "complement", "established", "main", "Mountain freshness and dark fruit complement lamb's mineral sweetness; mint bridges the wine's herbal aromatic.")
    PAIR(prod, "Aged gouda with apricot preserve and walnuts", "complement", "established", "cheese", "The wine's cassis and cedar bridge to aged Gouda's caramel; apricot preserves the wine's fruit echo.")
    PAIR(prod, "Venison medallions with blackcurrant and thyme jus", "complement", "classic", "main", "Mountain Cabernet's iron matches venison's gaminess; blackcurrant mirrors the wine's cassis; thyme bridges the herbal notes.")

# === VALLE DE GUADALUPE ===
print("=== Valle de Guadalupe ===")
r3 = R("Valle de Guadalupe", "Mexico", "wine",
       designation_type="region",
       designation_name="Valle de Guadalupe Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Valle de Guadalupe in Baja California, just 30km from Ensenada and 80km from the US border, is Mexico's most important and fastest-growing wine region. The Mediterranean climate — dry, warm summers with cooling Pacific fog — favours Nebbiolo, Grenache, Tempranillo, and Cabernet Sauvignon alongside indigenous white varieties. The region's 'Baja Med' cuisine movement — combining Mexican ingredients and techniques with Mediterranean wine culture — has attracted international culinary attention. Over 150 wineries now operate in the valley, from artisan boutiques to premium estates.",
       key_producers="Monte Xanic, Casa de Piedra, Adobe Guadalupe, Vena Cava, L.A. Cetto",
       historical_context="Baja California wine production began with Dominican missionaries in the 18th century. The modern era started in the 1980s when Hugo D'Acosta established Casa de Piedra and demonstrated that world-class wine could be produced in Mexico. The Baja Med food movement of the 1990s-2000s, centred on chef Javier Plascencia, created a culture of local wine-food pairing that has attracted global attention.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Landmark Valle vintage — Mediterranean varieties of exceptional concentration and complexity."),
    (2020,"very_good","stable","Good conditions; Nebbiolo and Grenache particularly successful from older vine sites."),
    (2021,"excellent","rising","Outstanding year; internationally recognised quality improvement across the valley."),
    (2022,"very_good","stable","Fine vintage; Cabernet Sauvignon and Tempranillo showing classic varietal character."),
    (2023,"excellent","rising","Exceptional vintage for Valle de Guadalupe — wines achieving international award success."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Monte Xanic Winery Baja California", "winery", r3, "Mexico",
       production_philosophy="terroir_expression",
       philosophy_description="Monte Xanic, founded in 1987, is Mexico's most acclaimed premium winery and the pioneer of fine wine production in Valle de Guadalupe. Their Gran Ricardo blend and Calixa Sauvignon Blanc have won international competitions and demonstrated that Mexican wine can compete at the highest global level.",
       reputation_narrative="Monte Xanic is Mexico's most internationally recognised fine wine producer — their success at global competitions has been crucial in establishing the credibility of Mexican wine in international markets and inspiring a generation of Baja California winemakers.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Monte Xanic Gran Ricardo Valle de Guadalupe", "wine_still", p3, r3, "Mexico",
                    subcategory="red", description="Mexico's most acclaimed red blend — Merlot, Cabernet Sauvignon, and Cabernet Franc from Valle de Guadalupe's Mediterranean-influenced soils. Dark fruit, chocolate, cedar, and Mediterranean herb character with surprising elegance for the warm climate.", price_tier="premium")
if is_new:
    PAIR(prod, "Birria de res (slow-braised spiced beef) with consommé", "complement", "adventurous", "main", "Mexican wine with Mexican cuisine — the wine's dark fruit and spice echo birria's chile-achiote depth.")
    PAIR(prod, "Grilled lobster taco with butter, lime and salsa verde", "complement", "adventurous", "main", "Baja Med pairing — Valle's finest red with Baja's famous lobster tacos in a cross-cultural food-wine moment.")
    PAIR(prod, "Carne asada with chipotle, lime and fresh cilantro", "complement", "classic", "main", "The quintessential Baja pairing — Valle de Guadalupe's red blend and the region's most celebrated grilled meat.")
    PAIR(prod, "Aged Manchego-style cheese from Baja with dried chilli", "complement", "established", "cheese", "Regional cheese with regional wine — dried chilli echoes the wine's spice; the cheese's fat softens its dark fruit.")
prod, is_new = PROD("Adobe Guadalupe Gabriel Valle de Guadalupe Red", "wine_still", p3, r3, "Mexico",
                    subcategory="red", description="Adobe Guadalupe's unique blend including Nebbiolo, Tempranillo, Syrah, Grenache, and other varieties — a Mediterranean-inspired blend showing Valle de Guadalupe's varietal diversity. Floral, spicy, and warm-climate rich.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled octopus with chilli-lime butter and corn salsa", "complement", "adventurous", "main", "Baja Med at its finest — Pacific octopus with Valle de Guadalupe wine in a Mexican-Mediterranean fusion.")
    PAIR(prod, "Duck carnitas with mole negro and fresh tortillas", "complement", "adventurous", "main", "Nebbiolo's floral notes and dark fruit mirror mole negro's chocolate and chilli complexity — a remarkable Baja Med pairing.")
    PAIR(prod, "Lamb barbacoa with avocado and lime", "complement", "established", "main", "Baja's version of the Spanish lamb-wine pairing — Mediterranean varieties with Mexican preparation.")
    PAIR(prod, "Queso fresco salad with roasted peppers and herbs", "complement", "established", "starter", "The wine's Grenache-Nebbiolo floral notes bridge to fresh Mexican cheese's mild creaminess.")

# === CANELONES DO ===
print("=== Canelones DO ===")
r4 = R("Canelones DO", "Uruguay", "wine",
       designation_type="DO",
       designation_name="Canelones Denominación de Origen",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Canelones, south of Montevideo, is Uruguay's wine heartland, producing over 60% of the country's wine. The region is centred on the French-origin Tannat grape — a high-tannin Pyrenean variety that has become Uruguay's signature red, producing wines of extraordinary structure and antioxidant content. Uruguay's Atlantic maritime influence moderates temperatures, producing Tannat of surprisingly refined tannins compared to the Madiran originals. Bodega Garzón (south, in Maldonado) and Pisano are leading estates. Viognier has also emerged as a successful white variety.",
       key_producers="Pisano Winery, Filgueira Winery, Bouza Bodega, Establecimiento Juanicó, Marichal Family Wines",
       historical_context="Tannat was brought to Uruguay by Basque immigrants in 1870, and it has become so identified with the country that Uruguay has officially declared it their national grape. While Madiran in France produces notoriously tannic expressions, Uruguayan winemakers have developed techniques (micro-oxygenation, blending) to soften Tannat's aggressive tannins into a more elegant, approachable style.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Canelones vintage — Tannat of exceptional concentration and balanced tannins."),
    (2019,"very_good","stable","Good vintage; Atlantic breezes preserved freshness in what was a warm year."),
    (2020,"excellent","rising","Outstanding conditions; Uruguayan Tannat achieving international recognition."),
    (2021,"very_good","stable","Fine vintage; wines showing the variety's capacity for elegance alongside power."),
    (2022,"excellent","rising","Exceptional vintage; Canelones wines earning medals at international competitions."),
    (2023,"very_good","stable","Good conditions; consistent quality across the DO's established producers."),
]:
    VIN(r4, yr, qd, pt, sn)

p4 = P("Pisano Winery Canelones", "winery", r4, "Uruguay",
       production_philosophy="terroir_expression",
       philosophy_description="The Pisano family has produced wine in Canelones since 1924, and they are one of Uruguay's most respected multi-generational producers. Their AMAT (Arte, Mano, Amor, Tierra) premium range showcases Tannat and Viognier at the highest level, demonstrating Uruguay's potential for world-class wine.",
       reputation_narrative="Pisano is Uruguay's most respected traditional winery — their AMAT Tannat has won multiple international gold medals and helped establish Uruguay as a serious fine wine nation beyond its regional reputation.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Pisano AMAT Tannat Canelones", "wine_still", p4, r4, "Uruguay",
                    subcategory="red", description="Uruguay's benchmark Tannat — aged 18 months in French oak. Deep ruby-purple, intensely concentrated: plum, blackberry, dark chocolate, tobacco, and the variety's characteristic antioxidant-rich firm tannins softened by Atlantic freshness. An extraordinary pairing wine.", price_tier="premium")
if is_new:
    PAIR(prod, "Chivito (Uruguayan national sandwich) with beef, egg, olives", "complement", "classic", "main", "The quintessential Uruguayan pairing — Tannat and the national sandwich, both deeply expressive of Uruguayan food culture.")
    PAIR(prod, "Grilled entrecôte with chimichurri and Uruguayan sea salt", "complement", "classic", "main", "Tannat's powerful tannins are the ideal match for quality grilled beef — South America's answer to Cabernet-Sauvignon-steak.")
    PAIR(prod, "Slow-roasted lamb leg with herbs and root vegetables", "complement", "established", "main", "Tannat's structure handles lamb's richness; herbs mirror the wine's Mediterranean character.")
    PAIR(prod, "Dark chocolate with Uruguayan dulce de leche and hazelnuts", "complement", "adventurous", "dessert", "Tannat's antioxidant-rich dark chocolate notes echo the dessert's richness; dulce de leche bridges the wine's fruit.")
prod, is_new = PROD("Bodega Garzón Tannat Reserve Maldonado Uruguay", "wine_still", p4, r4, "Uruguay",
                    subcategory="red", description="Garzón's estate Tannat from Maldonado's Atlantic-influenced granite and clay soils — Uruguayan Tannat at its most elegant. Firm tannins, plum, dark cherry, and Mediterranean herbs with a mineral freshness from the ocean's proximity.", price_tier="premium")
if is_new:
    PAIR(prod, "Asado de tira (Uruguayan short ribs) with salsa criolla", "complement", "classic", "main", "The definitive Uruguayan asado pairing — Tannat Reserve with the traditional Sunday short rib is a national institution.")
    PAIR(prod, "Lamb and herb empanadas with chimichurri", "complement", "established", "starter", "Tannat's structure and dark fruit complement the lamb filling; chimichurri's herb acidity bridges both.")
    PAIR(prod, "Braised venado (Pampas deer) with wild herbs", "complement", "established", "main", "Native game with Uruguay's native grape — shared South American terroir creates a compelling regional match.")
    PAIR(prod, "Aged Colonia cheese from Colonia del Sacramento", "complement", "established", "cheese", "Uruguayan aged cheese with Uruguayan Tannat — the wine's fruit and tannins balance the cheese's salt and fat.")

# === NASHIK VALLEY GI ===
print("=== Nashik Valley GI ===")
r5 = R("Nashik Valley GI", "India", "wine",
       designation_type="GI",
       designation_name="Nashik Valley Geographic Indication",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="Nashik in Maharashtra's Western Ghats, 170km northeast of Mumbai, is India's premier wine region, producing over 80% of India's quality wine. At 550–700m altitude, the region has a unique micro-climate with warm days, cool nights, and a clear dry season enabling commercial wine production. Sula Vineyards pioneered modern Indian wine here in 1999, introducing international varieties including Sauvignon Blanc, Chenin Blanc, Cabernet Sauvignon, and Shiraz. The region's rapid growth has created India's first wine tourism destination.",
       key_producers="Sula Vineyards, York Winery, Soma Vineyards, Four Seasons Winery, Grover Zampa",
       historical_context="Indian wine history dates to antiquity, but commercial modern production effectively began in the 1980s when Grover Zampa established vineyards in Karnataka. Sula Vineyards' founding in 1999 in Nashik by US-educated Rajeev Samant transformed the industry, creating a wine tourism model and demonstrating that India could produce internationally competitive wines.")
for yr, qd, pt, sn in [
    (2019,"very_good","rising","Strong Nashik vintage — Sauvignon Blanc and Chenin Blanc of notable freshness."),
    (2020,"good","stable","Reasonable vintage despite monsoon challenges; established producers maintained quality."),
    (2021,"very_good","rising","Good conditions; Sula and York wines receiving international export attention."),
    (2022,"very_good","stable","Fine vintage; consistent quality across the region's premium tier producers."),
    (2023,"excellent","rising","Landmark vintage for Nashik — Indian wine reaching new quality benchmarks."),
]:
    VIN(r5, yr, qd, pt, sn)

p5 = P("Sula Vineyards Nashik", "winery", r5, "India",
       production_philosophy="terroir_expression",
       philosophy_description="Sula Vineyards, founded by Rajeev Samant and Kiran Vora in 1999, is India's most successful wine company and the pioneer of Indian wine tourism. Their SulaFest music and wine festival attracts over 20,000 visitors annually, and their wines are India's most widely exported. The estate's Dindori Reserve range competes internationally.",
       reputation_narrative="Sula Vineyards has single-handedly created India's wine consumer culture and built the most visible international reputation for Indian wine. Their success has inspired over 90 wineries to open in Nashik and established India as a credible wine-producing nation.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Sula Vineyards Rasa Sauvignon Blanc Nashik", "wine_still", p5, r5, "India",
                    subcategory="white", description="India's most acclaimed Sauvignon Blanc from Nashik's red basalt soils at 600m. Tropical fruit, citrus zest, and a herbaceous freshness unusual for the climate — demonstrating India's capacity for cool-climate style whites when properly managed.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Tandoori fish tikka with green chutney and naan", "complement", "classic", "main", "Indian wine with Indian food — Sauvignon Blanc's citrus freshness bridges green chutney's herb brightness and cuts through tandoor richness.")
    PAIR(prod, "Prawns in coconut and ginger curry", "complement", "established", "main", "The wine's tropical fruit mirrors coconut's sweetness; acidity cuts through the rich curry sauce.")
    PAIR(prod, "Grilled pomfret with goan masala and lime", "complement", "classic", "main", "India's favourite sea fish with India's freshest white — citrus and herb bridge the spiced masala perfectly.")
    PAIR(prod, "Paneer tikka with mint chutney and lemon", "complement", "established", "starter", "Sauvignon Blanc's bright acidity mirrors mint chutney's freshness; the wine's tropical notes complement paneer's mild richness.")
prod, is_new = PROD("York Winery Reserve Shiraz Nashik", "wine_still", p5, r5, "India",
                    subcategory="red", description="York Winery's premium Nashik Shiraz from selected basalt hillside plots — India's most acclaimed red wine. Dark purple, intense: dark cherry, plum, pepper, and Indian spice character unique to the warm-climate Nashik expression. Aged 12 months in French oak.", price_tier="premium")
if is_new:
    PAIR(prod, "Lamb rogan josh with basmati rice and raita", "complement", "classic", "main", "India's great wine with India's great dish — Shiraz's dark fruit and pepper echo rogan josh's warming spice.")
    PAIR(prod, "Grilled mutton seekh kebab with mint and onion", "complement", "classic", "main", "Nashik's wine style was built for spiced grilled meats — Shiraz's pepper and dark fruit complement the kebab's char.")
    PAIR(prod, "Chicken tikka masala with garlic naan", "complement", "established", "main", "The British-Indian classic gets an Indian wine pairing — Nashik Shiraz's warmth matches the masala's rich tomato spice.")
    PAIR(prod, "Smoked duck breast with tamarind glaze and fried shallots", "complement", "adventurous", "main", "Indo-French fusion pairing — the wine's dark fruit and spice bridge to tamarind's sweet-sour depth.")

# === DB STATE ===
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
print("B171 complete.")
cur.close()
conn.close()
