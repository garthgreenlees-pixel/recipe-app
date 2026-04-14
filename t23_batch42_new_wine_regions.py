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

# ── 1. WAIPARA VALLEY (New Zealand) ─────────────────────────────────────────
print("\n=== Waipara Valley (New Zealand) ===")
r = R("Waipara Valley", "New Zealand", "wine",
      designation_type="GI",
      designation_name="Waipara Valley GI",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="North Canterbury's premier wine subregion; sheltered from coastal winds by the Teviotdale Hills, Waipara enjoys warmer, drier conditions than other Canterbury areas. Exceptional Pinot Noir with silky precision, world-class Riesling of striking floral-petrol complexity, and aromatic whites from limestone-rich soils. Home to New Zealand's most exciting cool-climate experimenting estates.",
      key_producers="Black Estate, Bell Hill, Pegasus Bay, Greystone, Muddy Water",
      historical_context="Waipara's wine industry began in the 1980s, but its reputation took off in the 1990s when producers like Pegasus Bay demonstrated the valley's capacity for premium Riesling and Pinot Noir. The region was separated from the broader Canterbury GI to reflect its distinct terroir character, sheltered by the Teviotdale Hills and sitting on unique limestone-clay soils.")

VIN(r, 2023, "excellent", "rising", "Outstanding warm season; Pinot Noir of exceptional depth and Riesling of piercing aromatic intensity")
VIN(r, 2022, "very_good", "stable", "Good vintage with fine structural balance; elegant Riesling and silky Pinot Noir")
VIN(r, 2021, "good", "stable", "Cooler, wetter year required careful canopy work; aromatic whites rewarded with fine acidity")
VIN(r, 2020, "excellent", "rising", "Long, even-ripening season; some of the valley's finest Pinot Noir in recent memory")
VIN(r, 2019, "very_good", "stable", "Reliable, well-balanced vintage across all varietals")

p1 = P("Pegasus Bay", "New Zealand", r, "winery",
        "Waipara Valley's founding quality estate, established by the Donaldson family in 1986. Pegasus Bay produces benchmark Riesling, Pinot Noir, and Pinot Gris from limestone-rich soils, combining European discipline with New Zealand's natural fruit generosity. Their aged Riesling is among New Zealand's most celebrated cellar wine.")
prod1, new1 = PROD("Pegasus Bay Prima Donna Pinot Noir Waipara Valley", "wine_still", p1, r, "New Zealand",
    subcategory="Pinot Noir",
    description="Reserve Waipara Valley Pinot Noir; complex, silky, and structured with dark cherry, dried rose, and earthy mineral depth — one of New Zealand's finest expressions of the variety",
    price_tier="premium")
if new1:
    PAIR(prod1, "Roasted duck with cherry and thyme jus", "complement", "classic", "main", "Reserve Pinot's dark cherry intensity and silky tannins are a natural match for roasted duck in red fruit sauce")
    PAIR(prod1, "Aged Canterbury lamb rack with herb crust", "complement", "established", "main", "Earthy, structured Waipara Pinot pairs beautifully with the richness of Canterbury lamb")
    PAIR(prod1, "Wild mushroom and truffle gnocchi", "complement", "established", "main", "Earthy, forest-floor mineral in Pinot resonates with wild mushroom and truffle in a rich pasta")
    PAIR(prod1, "Aged Gouda or Gruyere with walnuts", "bridge", "suggested", "cheese", "Silky red-fruited Pinot bridges elegantly with nutty aged cheese")

p2 = P("Black Estate", "New Zealand", r, "winery",
        "An artisan organic estate producing intensely mineral and site-expressive Pinot Noir and Chardonnay from Waipara's limestone-heavy Omihi Hills subzone. Black Estate's Home Vineyard wines are among New Zealand's most sought-after and critically acclaimed natural-leaning wines.")
prod2, new2 = PROD("Black Estate Home Pinot Noir Waipara Valley", "wine_still", p2, r, "New Zealand",
    subcategory="Pinot Noir",
    description="Organic estate Pinot Noir from limestone Omihi Hills; intensely mineral with pomegranate, dried herb, and chalky precision — one of NZ's most terroir-expressive reds",
    price_tier="premium")
if new2:
    PAIR(prod2, "Braised Canterbury rabbit with mustard cream", "complement", "established", "main", "The wine's mineral precision and delicate fruit handle rabbit's gentle flavour with elegance")
    PAIR(prod2, "Smoked salmon with beetroot relish and dill cream", "complement", "suggested", "starter", "Mineral, red-fruited Pinot bridges the smoke and beet earthiness with good acidity")
    PAIR(prod2, "Roasted beet salad with feta and hazelnuts", "complement", "established", "starter", "Earthy, mineral Pinot from limestone soils resonates with beet's earthiness and hazelnut richness")
    PAIR(prod2, "Canterbury venison tartare with juniper oil", "complement", "adventurous", "starter", "Precise, mineral Pinot complements the clean iron richness of raw venison with herbal juniper")

# ── 2. RUTHERGLEN (Australia) ────────────────────────────────────────────────
print("\n=== Rutherglen (Australia) ===")
r2 = R("Rutherglen", "Australia", "wine",
       designation_type="GI",
       designation_name="Rutherglen GI",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Home to one of the world's most unique and celebrated wine styles: Rutherglen Muscat and Topaque (formerly Tokay), classified in a four-tier system from Rutherglen to Grand to Rare. Made from dried Muscat Blanc a Petits Grains on the vine, then aged in a solera-like system of fractional blending. No other wine region on earth produces anything quite like them. Also produces robust Durif and Shiraz.",
       key_producers="Chambers Rosewood, Stanton and Killeen, Campbells, All Saints Estate, Morris Wines",
       historical_context="Rutherglen was established by gold rush-era settlers in the 1850s and 1860s. Its Muscat and Muscadelle (Topaque) styles evolved from simple fortified wines into the extraordinary sticky raisined category known today. The four-tier Rutherglen classification system was established in 1997. Many of the region's solera stocks contain wine components over 100 years old.")

VIN(r2, 2023, "excellent", "stable", "Ideal hot, dry conditions for Muscat sugar concentration; outstanding vintage")
VIN(r2, 2022, "very_good", "stable", "Good vintage with consistent Muscat grape drying; well-balanced Topaque and Muscat")
VIN(r2, 2021, "very_good", "stable", "Hot season with reliable fruit concentration; fine Durif and Shiraz alongside classic stickies")
VIN(r2, 2020, "good", "stable", "Slightly more variable; solid production with the solera system maintaining house character")
VIN(r2, 2019, "excellent", "stable", "Outstanding growing conditions; exceptional Muscat concentration for the vintage component")

p3 = P("Chambers Rosewood", "Australia", r2, "winery",
        "Producing wine since 1858, Chambers Rosewood is widely regarded as the greatest producer of Rutherglen Muscat on earth. Their Rare Muscat — the top tier of their four-level classification — commands extraordinary prices and critical reverence, with a solera containing components dating back to the 19th century.")
prod3, new3 = PROD("Chambers Rosewood Grand Muscat Rutherglen", "wine_fortified", p3, r2, "Australia",
    subcategory="Muscat Blanc a Petits Grains",
    description="Grand tier Rutherglen Muscat; intense raisin, dried orange peel, mocha, and roasted coffee with a luscious, syrupy texture and extraordinary complex finish from decades of solera aging",
    price_tier="ultra_premium")
if new3:
    PAIR(prod3, "Dark chocolate and coffee cake", "complement", "classic", "dessert", "The wine's roasted coffee and mocha notes create a seamless pairing with dark chocolate and espresso-flavoured cake")
    PAIR(prod3, "Blue-veined cheese — Roquefort or King Island Blue", "contrast", "classic", "cheese", "One of the world's great sweet-savory contrasts: luscious, raisined Muscat against pungent, salty blue cheese")
    PAIR(prod3, "Christmas pudding with brandy butter", "complement", "classic", "dessert", "Dried fruit, raisin, and spice in Rutherglen Muscat mirror the complexity of a great Christmas pudding")
    PAIR(prod3, "Sticky date pudding with toffee sauce", "complement", "established", "dessert", "Toffee and date notes in the wine create an indulgent complementary pairing with the caramel dessert")

p4 = P("Campbells Winery", "Australia", r2, "winery",
        "One of Rutherglen's most historic and trusted estates, Campbells has been farming the region since 1870. Their Merchant Prince Muscat and Isabella Topaque are beloved benchmark wines at the Grand tier, combining accessibility with the hallmark Rutherglen intensity.")
prod4, new4 = PROD("Campbells Isabella Topaque Rutherglen", "wine_fortified", p4, r2, "Australia",
    subcategory="Muscadelle",
    description="Grand tier Rutherglen Topaque (formerly Tokay) from Muscadelle; cold tea, butterscotch, toffee, and spiced orange with a distinctive tangy freshness cutting through the sweetness",
    price_tier="premium")
if new4:
    PAIR(prod4, "Creme brulee with caramelised sugar crust", "complement", "classic", "dessert", "Butterscotch and toffee in Topaque create a seamless match with the caramel-cream of classic brulee")
    PAIR(prod4, "Aged cheddar with quince paste", "contrast", "established", "cheese", "The wine's tangy, sweet-toffee character provides delicious contrast to sharp aged cheddar and quince")
    PAIR(prod4, "Almond and orange biscotti", "complement", "established", "dessert", "Spiced orange and almond notes in the Topaque resonate with the nut and citrus of Italian biscotti")
    PAIR(prod4, "Pecan tart with maple glaze", "complement", "suggested", "dessert", "The wine's toffee-butterscotch profile pairs naturally with the maple and nut richness of a pecan tart")

# ── 3. GRECO DI TUFO (Italy) ─────────────────────────────────────────────────
print("\n=== Greco di Tufo (Italy) ===")
r3 = R("Greco di Tufo", "Italy", "wine",
       designation_type="DOCG",
       designation_name="Greco di Tufo DOCG",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="One of Campania's three great DOCG white wine appellations, named for both its ancient grape variety and the tufa volcanic soil of the Irpinia hills. Greco di Tufo produces structured, mineral whites with striking almond, white peach, and smoky volcanic notes. Naturally high in acidity and built for aging, the best examples rival top white Burgundy in complexity after 5-10 years.",
       key_producers="Feudi di San Gregorio, Mastroberardino, Benito Ferrara, Di Meo, Terredora di Paolo",
       historical_context="The Greco grape is one of Italy's oldest, brought to Campania by Greek colonists in antiquity. The town of Tufo gave its name both to the local tufa volcanic rock and the wine style. The area was granted DOCG status in 2003 alongside Fiano di Avellino, marking Campania's emergence as Italy's most exciting source of indigenous white wines.")

VIN(r3, 2023, "excellent", "rising", "Warm, volcanic growing season with exceptional mineral-almond Greco intensity")
VIN(r3, 2022, "very_good", "rising", "Good vintage with the characteristic smoky, structured style building for aging")
VIN(r3, 2021, "very_good", "stable", "Cooler conditions produced particularly taut, high-acid Greco ideal for cellaring")
VIN(r3, 2020, "good", "stable", "Hot summer; approachable, generously fruited wines with typical almond complexity")
VIN(r3, 2019, "excellent", "rising", "Benchmark Campanian vintage; outstanding Greco di Tufo with exceptional cellaring potential")

p5 = P("Terredora di Paolo", "Italy", r3, "winery",
        "One of the founding family estates of modern Campanian wine, Terredora di Paolo produces benchmark Greco di Tufo and Fiano di Avellino from extensive Irpinia holdings. Their Terre di Dora and Loggia della Serra Greco wines are consistently among the appellation's most precise and food-friendly expressions.")
prod5, new5 = PROD("Terredora di Paolo Terre di Dora Greco di Tufo DOCG", "wine_still", p5, r3, "Italy",
    subcategory="Greco",
    description="Estate Greco di Tufo from volcanic tufa soils; white peach, toasted almond, bitter citrus peel, and a distinctive smoky mineral finish — benchmark Campanian white",
    price_tier="mid_range")
if new5:
    PAIR(prod5, "Linguine alle vongole in bianco", "complement", "classic", "main", "The wine's bitter citrus and mineral depth perfectly frame delicate clams in white wine sauce")
    PAIR(prod5, "Grilled spigola with capers, olives, and lemon", "complement", "established", "main", "Structured, mineral Greco di Tufo frames firm white fish and Mediterranean garnish beautifully")
    PAIR(prod5, "Pasta e fagioli with Neapolitan pork rind", "complement", "established", "main", "The wine's almond and smoky minerality resonate with the earthy, pork-enriched legume stew")
    PAIR(prod5, "Aged Caciocavallo Silano cheese", "complement", "suggested", "cheese", "Structured, slightly bitter Greco holds up elegantly to aged, firm Southern Italian cheese")

p6 = P("Benito Ferrara", "Italy", r3, "winery",
        "A small artisan estate producing some of the most precise and mineral Greco di Tufo available. Gabriele Ferrara works his Tufo vineyards with meticulous attention to expressing the unique volcanic tufa soil, producing wines of remarkable concentration that improve dramatically with bottle age.")
prod6, new6 = PROD("Benito Ferrara Vigna Cicogna Greco di Tufo DOCG", "wine_still", p6, r3, "Italy",
    subcategory="Greco",
    description="Single-vineyard Greco di Tufo from old vines on tufa; intense almond, dried apricot, white smoke, and volcanic mineral — one of the appellation's most age-worthy expressions",
    price_tier="premium")
if new6:
    PAIR(prod6, "Grilled totani (squid) with wild herbs and lemon", "complement", "classic", "main", "Mineral, structured Greco is the natural Campanian pairing for grilled squid or cuttlefish")
    PAIR(prod6, "Baked ricotta and herb-stuffed eggplant", "complement", "established", "main", "The wine's bitter almond and smoky notes resonate with baked eggplant and fresh ricotta filling")
    PAIR(prod6, "Parmigiana di melanzane (eggplant Parmesan)", "complement", "established", "main", "Structured, slightly bitter Greco holds up to the richness of layered tomato, eggplant, and cheese")
    PAIR(prod6, "Ricotta salata with cherry tomatoes and basil", "complement", "suggested", "starter", "The wine's mineral freshness and almond notes complement the salty cheese and sweet tomato beautifully")

# ── 4. PALETTE (France) ──────────────────────────────────────────────────────
print("\n=== Palette (France) ===")
r4 = R("Palette", "France", "wine",
       designation_type="AOC",
       designation_name="Palette AOC",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="One of France's smallest and most prestigious wine appellations, just east of Aix-en-Provence. A tiny 60-hectare zone dominated almost entirely by Chateau Simone, the defining producer of the appellation. Palette is planted on a north-facing limestone slope in a natural amphitheatre — an anomaly in Provence that allows for cool, slow ripening and remarkable complexity. Whites, roses, and reds all produced with extraordinary aging potential.",
       key_producers="Chateau Simone, Chateau Henri Bonnaud",
       historical_context="Palette's wine history traces to the Augustinian monks of Aix who planted vines here in the 15th century. The Rougier family has owned Chateau Simone since 1830, making it one of Provence's most historic continuous family estates. The appellation was created in 1948 and remains one of France's most intimate, with only two producers legally entitled to use the appellation name.")

VIN(r4, 2023, "excellent", "rising", "Cool north-facing slope moderated a warm Provencal year; exceptional red and white complexity")
VIN(r4, 2022, "very_good", "rising", "Outstanding Provence vintage; Palette's unique terroir produced wines of unusual freshness and structure")
VIN(r4, 2021, "good", "stable", "Challenging for much of Provence but Palette's sheltered aspect handled conditions well")
VIN(r4, 2020, "excellent", "rising", "Long, even season; Chateau Simone red of exceptional aging potential")
VIN(r4, 2019, "very_good", "stable", "Classic vintage with the appellation's signature herbal complexity and mineral depth")

p7 = P("Chateau Simone", "France", r4, "winery",
        "The defining producer of Palette AOC, Chateau Simone dominates the appellation with wines of extraordinary longevity and complexity. The Rougier family has made wine here since 1830, working with a unique blend of old Provencal varieties on north-facing limestone soils. Their white wines can age for decades; their red Palette is one of France's most distinctive wines.")
prod7, new7 = PROD("Chateau Simone Palette Rouge", "wine_still", p7, r4, "France",
    subcategory="Mourvedre blend",
    description="The benchmark red of Palette AOC; complex, age-worthy blend of Mourvedre, Grenache, and Cinsault with garrigue, dark cherry, leather, and a long limestone-mineral finish — one of Provence's most profound reds",
    price_tier="premium")
if new7:
    PAIR(prod7, "Roasted leg of lamb with herbes de Provence", "complement", "classic", "main", "The wine's garrigue and dark fruit are inseparable from slow-roasted Provencal lamb with wild herbs")
    PAIR(prod7, "Daube de boeuf Provencale (braised beef with olives)", "complement", "classic", "main", "Structured, herbal Palette red is perfectly suited to the olive-enriched Provencal beef stew")
    PAIR(prod7, "Sanglier (wild boar) with juniper and thyme", "complement", "established", "main", "Leather and garrigue notes in the wine echo the gamey richness of wild boar with aromatic herbs")
    PAIR(prod7, "Aged Banon cheese wrapped in chestnut leaves", "bridge", "suggested", "cheese", "The wine's herbal complexity and earth resonate with the distinctive wrapped goat's cheese of Provence")

p8 = P("Chateau Henri Bonnaud", "France", r4, "winery",
        "The second estate within the Palette appellation, Henri Bonnaud produces wines of exceptional quality from a similar north-facing limestone terroir, offering a second interpretation of the appellation's unique character with particular strength in Palette Blanc from old Clairette and Grenache Blanc vines.")
prod8, new8 = PROD("Chateau Henri Bonnaud Palette Blanc", "wine_still", p8, r4, "France",
    subcategory="Clairette blend",
    description="Rare Palette Blanc from old Clairette, Grenache Blanc, and Ugni Blanc; floral, mineral, and textured with white blossom, almonds, and a distinctive limestone freshness that develops extraordinary complexity with age",
    price_tier="premium")
if new8:
    PAIR(prod8, "Bouillabaisse with rouille and croutons", "complement", "classic", "main", "The wine's mineral freshness and textured body are a natural match for the iconic Provencal fish stew")
    PAIR(prod8, "Grilled whole sea bream with fennel and lemon", "complement", "classic", "main", "Limestone mineral and floral complexity frame delicate whole fish beautifully")
    PAIR(prod8, "Panisse (chickpea fritters) with anchovy aioli", "complement", "established", "starter", "The wine's almond notes and textured mineral echo the nuttiness of chickpea with umami anchovy")
    PAIR(prod8, "Fresh chevre with Provencal honey and herbs", "complement", "suggested", "cheese", "Floral, mineral Palette Blanc resonates with fresh goat's cheese, local honey, and aromatic herbs")

# ── 5. COLARES (Portugal) ────────────────────────────────────────────────────
print("\n=== Colares (Portugal) ===")
r5 = R("Colares", "Portugal", "wine",
       designation_type="DOC",
       designation_name="DOC Colares",
       reputation_tier="prestigious",
       quality_trajectory="rediscovering",
       description="One of the world's most historically significant and nearly-extinct wine appellations, just west of Lisbon on the Atlantic coast. Colares is planted on ancient sandy beaches where phylloxera cannot survive — making these among the world's last pre-phylloxera ungrafted vines, some over 100 years old. The indigenous Ramisco grape produces wines of extraordinary tannin, dark fruit, and iodine-salinity from the Atlantic. Minimal production; deeply endangered.",
       key_producers="Adega Regional de Colares, Viuva Gomes, Casal Santa Maria",
       historical_context="Colares's sandy coastal soils (not its rocky outcrops) saved it from the phylloxera epidemic of the 19th century — the louse cannot survive in pure sand. These extraordinary conditions preserve ungrafted pre-phylloxera vines across several centuries of uninterrupted production. At its peak in the early 20th century, Colares had thousands of hectares under vine; today fewer than 40 hectares remain, making it one of the world's most endangered wine regions.")

VIN(r5, 2023, "good", "rising", "Atlantic-cooled season on sandy dunes; small crop of typical briny, tannic Ramisco")
VIN(r5, 2022, "very_good", "rising", "Excellent vintage for old-vine Ramisco; remarkable concentration from the pre-phylloxera vines")
VIN(r5, 2021, "average", "stable", "Wetter Atlantic year; lighter style but with the characteristic iodine and Atlantic character")
VIN(r5, 2020, "good", "stable", "Reliable vintage with fine dark fruit and the region's signature sandy-mineral quality")
VIN(r5, 2019, "excellent", "rising", "Benchmark vintage; deepest, most complex Ramisco in years from the ancient ungrafted vines")

p9 = P("Adega Regional de Colares", "Portugal", r5, "winery",
        "The cooperative winery that has been the guardian of Colares DOC for generations, responsible for preserving and vinifying Ramisco from the ancient ungrafted sandy-soil vines. Without this cooperative, the Colares appellation would likely not have survived the 20th century.")
prod9, new9 = PROD("Adega Regional de Colares Chitas Ramisco", "wine_still", p9, r5, "Portugal",
    subcategory="Ramisco",
    description="Historic Colares red from pre-phylloxera ungrafted Ramisco vines in coastal Atlantic sand; austere, tannic, and briny with dark cherry, iron, iodine, and an extraordinary maritime mineral finish requiring decades of aging",
    price_tier="premium")
if new9:
    PAIR(prod9, "Caldeirada de peixe (Portuguese fish stew)", "complement", "adventurous", "main", "The wine's iodine and Atlantic brine character creates a unique resonance with the hearty Portuguese fish stew — unexpected but compelling")
    PAIR(prod9, "Roasted suckling pig with crackling (leitao)", "complement", "classic", "main", "Tannic, structured old-vine Ramisco pairs classically with the richness of Portugals most iconic roast pork")
    PAIR(prod9, "Aged Serrano ham and manchado cheese", "complement", "established", "starter", "Intense, austere Ramisco cuts through the fat of cured ham with its powerful tannic grip")
    PAIR(prod9, "Bacalhau à Brás (salt cod with eggs and olives)", "complement", "established", "main", "The wine's iodine-salt character creates a fascinating resonance with the briny intensity of salt cod")

p10 = P("Casal Santa Maria", "Portugal", r5, "winery",
         "One of the small private estates reviving quality wine production in Colares, Casal Santa Maria works with old Ramisco and Malvasia vines to produce wines that express the unique pre-phylloxera character of this endangered coastal appellation. Their wines represent a genuine rescue effort for one of Portugal's most important viticultural heritage zones.")
prod10, new10 = PROD("Casal Santa Maria Ramisco Colares", "wine_still", p10, r5, "Portugal",
    subcategory="Ramisco",
    description="Private estate Colares Ramisco; younger in style than the cooperative's wine but showing the same briny Atlantic character, dark fruit, and structured tannin of the pre-phylloxera ungrafted vines",
    price_tier="ultra_premium")
if new10:
    PAIR(prod10, "Grilled perceves (goose barnacles) with lemon", "complement", "classic", "main", "The wine's iodine, brine, and dark mineral are a stunning match for the most intensely oceanic shellfish — a Colares classic")
    PAIR(prod10, "Slow-roasted black Iberian pork with local herbs", "complement", "established", "main", "Old-vine Ramisco tannin and dark fruit hold up beautifully to the fat richness of black Iberian pork")
    PAIR(prod10, "Aged Serpa cheese with fig preserves", "bridge", "suggested", "cheese", "The wine's dark fruit and earth bridge naturally with pungent aged sheep's cheese and sweet fig")
    PAIR(prod10, "Char-grilled chourico with red wine and garlic", "complement", "established", "starter", "Tannic, dark-fruited Ramisco is a natural match for the smoky, garlicky Portuguese cured sausage")

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
