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

# ── 1. LAVAUX (Switzerland) ──────────────────────────────────────────────────
print("\n=== Lavaux (Switzerland) ===")
r = R("Lavaux", "Switzerland", "wine",
      designation_type="AOC",
      designation_name="Lavaux AOC",
      reputation_tier="prestigious",
      quality_trajectory="established",
      description="Terraced vineyards above Lake Geneva since the 11th century; UNESCO World Heritage Site. Chasselas reaches its pinnacle here — mineral, precise, and terroir-expressive across 14 communal appellations from Lutry to Chexbres. Cool lake-moderated climate on steep south-facing slopes.",
      key_producers="Henri Badoux, Domaine Louis Bovard, Domaine Bovy, Luc Massy",
      historical_context="Cistercian monks began cultivating these terraced hillsides in the 12th century. The Lavaux landscape was inscribed as a UNESCO World Heritage Site in 2007, recognised for its exceptional integration of human viticulture with dramatic natural terrain.")

VIN(r, 2023, "excellent", "stable", "Warm, dry summer with precise harvest timing; textbook Chasselas with vivid lake minerality")
VIN(r, 2022, "exceptional", "rising", "Near-perfect season; extended ripening produced concentrated yet elegant Chasselas of rare depth")
VIN(r, 2021, "good", "stable", "Spring frosts reduced yields; surviving fruit showed fine acidity and typical freshness")
VIN(r, 2020, "very_good", "stable", "Hot summer with good diurnal range; ripe, approachable style with solid structure")
VIN(r, 2019, "exceptional", "rising", "Historic warm vintage; Chasselas achieved exceptional concentration rarely seen in the appellation")

p1 = P("Henri Badoux", "Switzerland", r, "winery",
        "One of Lavaux's leading estates, Henri Badoux crafts benchmark Chasselas from steep terraced parcels above Lake Geneva. Aigle Les Murailles is its flagship — a Swiss white wine icon known for its stony minerality and profound sense of place.")
prod1, new1 = PROD("Henri Badoux Aigle Les Murailles Chasselas", "wine_still", p1, r, "Switzerland",
    subcategory="Chasselas",
    description="Iconic Swiss Chasselas from Aigle's limestone terraces; stony minerality, citrus blossom, and a clean saline finish — the benchmark for the variety",
    price_tier="mid_range")
if new1:
    PAIR(prod1, "Lake Geneva perch fillets meunière", "complement", "classic", "main", "Stony minerality and bright acidity perfectly frame delicate lake fish; a quintessential Swiss pairing")
    PAIR(prod1, "Gruyère cheese fondue with kirsch", "bridge", "classic", "main", "Subtle creaminess and mineral lift cut through rich melted cheese — the Swiss table's signature pairing")
    PAIR(prod1, "Charcuterie and cornichons", "complement", "established", "starter", "Light body and citrus freshness refresh the palate between slices of cured pork")
    PAIR(prod1, "Poached trout with herb butter", "complement", "classic", "main", "Delicate fruit and chalky mineral echo the freshwater character of the fish")

p2 = P("Domaine Louis Bovard", "Switzerland", r, "winery",
        "A family estate at the heart of the Lavaux UNESCO landscape, Louis Bovard produces some of the most site-expressive Chasselas in Switzerland from historic single-parcel vineyards above Cully.")
prod2, new2 = PROD("Domaine Louis Bovard Medinette Chasselas Lavaux", "wine_still", p2, r, "Switzerland",
    subcategory="Chasselas",
    description="Single-parcel Chasselas from Cully; floral, textured, and mineral with striking terroir precision — one of Lavaux's most individual expressions",
    price_tier="premium")
if new2:
    PAIR(prod2, "Roasted pike-perch with lemon cream", "complement", "established", "main", "Textured Chasselas with mineral lift pairs effortlessly with freshwater fish in cream sauce")
    PAIR(prod2, "Raclette with pickled onions", "bridge", "classic", "main", "Gentle phenolics and acidity cleanse through rich melted cheese; deeply Swiss")
    PAIR(prod2, "Vacherin Fribourgeois", "complement", "established", "cheese", "Soft washed-rind cheese brings out the wine's floral and hazelnut notes")
    PAIR(prod2, "White asparagus with hollandaise", "complement", "suggested", "starter", "Floral and lightly vegetal Chasselas resonates with white asparagus — a classic spring pairing")

# ── 2. NELSON (New Zealand) ──────────────────────────────────────────────────
print("\n=== Nelson (New Zealand) ===")
r2 = R("Nelson", "New Zealand", "wine",
       designation_type="GI",
       designation_name="Nelson GI",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Top of New Zealand's South Island; highest sunshine hours in the country. Small artisan-focused region with diverse varietals on clay and silt loam soils. Strong organic and biodynamic viticulture ethos. Produces elegant Sauvignon Blanc, world-class Chardonnay, and fine aromatic whites.",
       key_producers="Neudorf Vineyards, Seifried Estate, Mahana, Fromm Winery, Rimu Grove",
       historical_context="Hermann Seifried established Nelson's first commercial winery in 1973 after emigrating from Austria. The region has grown steadily as a boutique alternative to Marlborough, with particular strength in Chardonnay and aromatic varieties.")

VIN(r2, 2023, "excellent", "stable", "Warm, sunny season with good diurnal shifts; standout Sauvignon Blanc and Chardonnay")
VIN(r2, 2022, "very_good", "stable", "Slightly wetter start resolved into fine late summer; well-balanced wines with good structure")
VIN(r2, 2021, "good", "stable", "La Nina conditions brought more rainfall; careful canopy management rewarded with clean fruit")
VIN(r2, 2020, "excellent", "stable", "Long, warm, even-ripening season; particularly fine Chardonnay and Pinot Noir")
VIN(r2, 2019, "very_good", "stable", "Consistent vintage with excellent fruit purity across all varietals")

p3 = P("Neudorf Vineyards", "New Zealand", r2, "winery",
        "Nelson's most celebrated estate, Neudorf pioneered recognition of the region's Chardonnay and Pinot Noir potential. Their Moutere Chardonnay is one of New Zealand's benchmark whites, combining Burgundian discipline with Southern Hemisphere generosity.")
prod3, new3 = PROD("Neudorf Moutere Chardonnay Nelson", "wine_still", p3, r2, "New Zealand",
    subcategory="Chardonnay",
    description="Benchmark NZ Chardonnay from clay-rich Moutere Valley soils; complex and layered with stone fruit, hazelnut, and a long mineral finish",
    price_tier="premium")
if new3:
    PAIR(prod3, "Roasted free-range chicken with tarragon cream", "complement", "classic", "main", "Rich, textured Chardonnay with hazelnut notes resonates with roasted poultry and cream sauce")
    PAIR(prod3, "Pan-seared Pacific salmon with lemon butter", "complement", "established", "main", "Stone fruit and mineral complexity frame the richness of salmon beautifully")
    PAIR(prod3, "Crayfish bisque", "complement", "established", "starter", "The wine's weight and citrus-hazelnut complexity elevate crustacean richness")
    PAIR(prod3, "Aged Gouda with honeycomb", "bridge", "suggested", "cheese", "Textured Chardonnay with toasty notes pairs naturally with nutty aged cheese and honey")

p4 = P("Seifried Estate", "New Zealand", r2, "winery",
        "The founding estate of Nelson's wine industry, established in 1973 by Austrian immigrant Hermann Seifried. The family produces a comprehensive range across all key varietals with particular strength in Riesling, Sauvignon Blanc, and Gewurztraminer.")
prod4, new4 = PROD("Seifried Estate Nelson Sauvignon Blanc", "wine_still", p4, r2, "New Zealand",
    subcategory="Sauvignon Blanc",
    description="Classic Nelson Sauvignon Blanc with lifted passionfruit, lemongrass, and cut grass aromatics backed by crisp, refreshing acidity",
    price_tier="entry")
if new4:
    PAIR(prod4, "Green-lipped mussels with white wine and herbs", "complement", "classic", "starter", "Bright tropical aromatics and herb-edged acidity are a natural foil for fresh New Zealand mussels")
    PAIR(prod4, "Goat's cheese salad with citrus dressing", "complement", "established", "starter", "Herbaceous lift and acidity resonate with tangy goat's cheese and citrus")
    PAIR(prod4, "Grilled asparagus with lemon aioli", "complement", "established", "starter", "The wine's green herbaceous notes pair classically with spring asparagus")
    PAIR(prod4, "Thai green curry with jasmine rice", "bridge", "suggested", "main", "Tropical fruit and bright acidity cut through coconut-based curry heat")

# ── 3. WALKER BAY (South Africa) ─────────────────────────────────────────────
print("\n=== Walker Bay (South Africa) ===")
r3 = R("Walker Bay", "South Africa", "wine",
       designation_type="WO District",
       designation_name="Walker Bay WO",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="South Africa's most compelling cool-climate wine district; icy South Atlantic sweeps cold air inland across the Hemel-en-Aarde Valley. Pinot Noir and Chardonnay of genuine Burgundian precision produced here. Ward system — Hemel-en-Aarde Valley, Upper Hemel-en-Aarde, and Ridge — provides meaningful terroir differentiation.",
       key_producers="Hamilton Russell Vineyards, Creation Wines, Bouchard Finlayson, Newton Johnson, Ataraxia",
       historical_context="Tim Hamilton Russell planted the first vines here in 1975 after a long search for South Africa's coolest wine-growing land. The region has become the Cape's most internationally respected for Pinot Noir and Chardonnay, drawing comparisons with Burgundy.")

VIN(r3, 2023, "excellent", "rising", "Cool, even-ripening season with precise harvest timing; exceptional Pinot Noir and Chardonnay")
VIN(r3, 2022, "very_good", "rising", "Good vintage with solid structure; wines show the region's characteristic marine freshness")
VIN(r3, 2021, "excellent", "rising", "Standout year; cool summer yielded wines of fine-boned elegance and outstanding aging potential")
VIN(r3, 2020, "good", "stable", "Slightly warmer; approachable, generous style with good concentration")
VIN(r3, 2019, "very_good", "stable", "Classic cool maritime year; refined, structured wines with long cellaring potential")

p5 = P("Hamilton Russell Vineyards", "South Africa", r3, "winery",
        "Pioneer of South African Pinot Noir and Chardonnay, farming the Hemel-en-Aarde Valley since 1975. Single-vineyard wines consistently rank among the Cape's greatest, with complexity and precision rivalling top Burgundy.")
prod5, new5 = PROD("Hamilton Russell Hemel-en-Aarde Valley Pinot Noir", "wine_still", p5, r3, "South Africa",
    subcategory="Pinot Noir",
    description="Benchmark South African Pinot Noir from the cool Hemel-en-Aarde Valley; silky-textured with red cherry, dried herbs, and a long earthy mineral finish",
    price_tier="premium")
if new5:
    PAIR(prod5, "Roasted duck breast with cherry jus", "complement", "classic", "main", "Red fruit intensity and silky tannins complement duck perfectly — a classical pairing")
    PAIR(prod5, "Grilled West Coast snoek with herb oil", "complement", "established", "main", "Cool-climate Pinot's delicacy pairs well with the richness of local game fish")
    PAIR(prod5, "Wild mushroom and truffle risotto", "complement", "established", "main", "Earthy, mineral Pinot resonates with forest floor notes in a fine mushroom risotto")
    PAIR(prod5, "Aged Gruyere with rye crispbread", "bridge", "suggested", "cheese", "Red-fruited Pinot with light earthy notes bridges elegantly with nutty aged cheese")

p6 = P("Creation Wines", "South Africa", r3, "winery",
        "Artisan estate in the Hemel-en-Aarde Ridge ward known for expressive single-varietal wines with exceptional food-pairing focus. Their wine-and-food pairing experiences are among the Cape Winelands' most sought-after.")
prod6, new6 = PROD("Creation Wines Hemel-en-Aarde Chardonnay", "wine_still", p6, r3, "South Africa",
    subcategory="Chardonnay",
    description="Complex cool-climate Chardonnay from Hemel-en-Aarde Ridge; white peach, hazelnut, and flinty minerality with a long saline finish",
    price_tier="premium")
if new6:
    PAIR(prod6, "West Coast rock lobster with lemon butter", "complement", "classic", "main", "Rich mineral Chardonnay with lemon butter and sweet lobster — a timeless Cape luxury pairing")
    PAIR(prod6, "Overstrand mussels in cream and wine sauce", "complement", "established", "starter", "Weight and acidity frame the creaminess and brine of local mussels beautifully")
    PAIR(prod6, "Abalone with seaweed butter", "complement", "suggested", "main", "Flinty, saline Chardonnay resonates with the ocean minerality of abalone")
    PAIR(prod6, "Pan-seared kingklip with capers and lemon", "complement", "established", "main", "Textured Chardonnay holds up to firm-fleshed local white fish with butter and acid components")

# ── 4. DRAGASANI (Romania) ───────────────────────────────────────────────────
print("\n=== Dragasani (Romania) ===")
r4 = R("Dragasani", "Romania", "wine",
       designation_type="DOC",
       designation_name="DOC Dragasani",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="One of Romania's oldest wine regions with viticultural history stretching back 3,000 years, in the Olt River valley of Wallachia. At the forefront of Romania's wine renaissance, championing indigenous varietals: Feteasca Neagra, Cramposie Selectionata, and ultra-rare Negru de Dragasani. Continental climate with limestone and clay soils.",
       key_producers="Crama Avincis, Prince Stirbey Winery, Bauer Winery, Licorna Winehouse",
       historical_context="Dragasani's vineyards were celebrated in antiquity and flourished under the Wallachian princes. The communist era imposed quantity over quality, but since 2000 a new generation of producers — particularly Prince Stirbey and Avincis — has revived historic varieties and put the region on the international map.")

VIN(r4, 2023, "good", "rising", "Warm, productive season; strong Feteasca Neagra concentration and color")
VIN(r4, 2022, "very_good", "rising", "Excellent vintage; prolonged ripening produced structured, age-worthy red wines")
VIN(r4, 2021, "average", "stable", "Wetter than ideal; careful selection rewarded with clean, food-friendly wines")
VIN(r4, 2020, "very_good", "rising", "Hot summer; excellent color and tannin development in indigenous varietals")
VIN(r4, 2019, "excellent", "rising", "Outstanding vintage across Romania; most concentrated Feteasca Neagra in a decade")

p7 = P("Crama Avincis", "Romania", r4, "winery",
        "The leading quality producer of the Dragasani appellation, Avincis has elevated the region's international profile through meticulous vineyard work with indigenous varietals. Their Feteasca Neagra and Villa Dobrussa wines are setting benchmarks for Romanian fine wine.")
prod7, new7 = PROD("Crama Avincis Villa Dobrussa Feteasca Neagra Dragasani", "wine_still", p7, r4, "Romania",
    subcategory="Feteasca Neagra",
    description="Reserve Feteasca Neagra from old vines; deep blackberry, dried herbs, and earthy spice with firm age-worthy tannins — Romania's most internationally celebrated red varietal",
    price_tier="premium")
if new7:
    PAIR(prod7, "Slow-braised lamb with herbs and polenta", "complement", "classic", "main", "Rich, tannic Feteasca Neagra finds its natural partner in braised lamb — a timeless Romanian pairing")
    PAIR(prod7, "Sarmale pork and rice cabbage rolls in tomato broth", "complement", "classic", "main", "Dark fruit and earthy spice resonate with the herbed pork filling and sour cabbage")
    PAIR(prod7, "Aged sheep's telemea cheese with walnuts", "bridge", "established", "cheese", "Tannic, dark-fruited red bridges naturally with pungent aged cheese and bitter walnut")
    PAIR(prod7, "Grilled wild boar sausages with mustard", "complement", "established", "main", "Rustic, structured Feteasca Neagra stands up to the intensity of wild game sausage")

p8 = P("Prince Stirbey Winery", "Romania", r4, "winery",
        "Historic estate reviving pre-communist aristocratic wine culture in Dragasani with indigenous varietals including the ultra-rare Cramposie Selectionata and Negru de Dragasani. One of Romania's most storied wine properties.")
prod8, new8 = PROD("Prince Stirbey Cramposie Selectionata Dragasani", "wine_still", p8, r4, "Romania",
    subcategory="Cramposie Selectionata",
    description="Romania's rarest white varietal — golden, full-bodied with peach, beeswax, and honeyed stone fruit; unique to Dragasani",
    price_tier="mid_range")
if new8:
    PAIR(prod8, "Fried carp with garlic sauce mujdei", "complement", "classic", "main", "Full-bodied local white echoes the rich, oily character of freshwater carp with the kick of garlic")
    PAIR(prod8, "Baked pumpkin with walnuts and honey", "complement", "established", "starter", "Honeyed, waxy white wine pairs naturally with the sweetness and nuttiness of baked pumpkin")
    PAIR(prod8, "Smoked cheese and sun-dried tomatoes", "complement", "suggested", "cheese", "Beeswax richness bridges smoked flavour and acidic tomato")
    PAIR(prod8, "Chicken paprikash with egg noodles", "complement", "suggested", "main", "Golden, full-bodied Cramposie holds up to the paprika richness of this Eastern European classic")

# ── 5. MELNIK (Bulgaria) ─────────────────────────────────────────────────────
print("\n=== Melnik (Bulgaria) ===")
r5 = R("Melnik", "Bulgaria", "wine",
       designation_type="PDO",
       designation_name="PDO Melnik 55",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Bulgaria's most internationally celebrated wine region, famous for its sandstone pyramid landscape and the world-exclusive Broadleaf Melnik grape (Shiroka Melnishka Loza). Strong Mediterranean influence in the Struma Valley. Wines of remarkable concentration, natural tannic grip, and extraordinary aging potential.",
       key_producers="Damianitza Winery, Zlaten Rozhen, Orbelus Estate, Zagreus Winery",
       historical_context="Melnik has been producing wine for at least 2,000 years; its wines were famously exported to the Ottoman Empire and beyond. Winston Churchill was a reputed fan of Melnik wine. The region's isolation in the far southwest of Bulgaria preserved its indigenous varietals through the communist era.")

VIN(r5, 2023, "very_good", "rising", "Long warm season with good diurnal range; strong concentration in Broadleaf Melnik")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage; exceptional tannin structure and colour intensity in all red varietals")
VIN(r5, 2021, "good", "stable", "Slightly cooler; wines show more elegance than power with fine aging potential")
VIN(r5, 2020, "very_good", "stable", "Hot, dry vintage typical of Mediterranean influence; powerful, concentrated reds")
VIN(r5, 2019, "excellent", "rising", "Benchmark vintage; finest Broadleaf Melnik wines in recent memory")

p9 = P("Damianitza Winery", "Bulgaria", r5, "winery",
        "The leading international ambassador for Melnik wine, Damianitza has invested heavily in vineyard restoration and modern winemaking to showcase the full potential of Broadleaf Melnik 55. Their No Man's Land label has won international acclaim.")
prod9, new9 = PROD("Damianitza No Man's Land Melnik 55", "wine_still", p9, r5, "Bulgaria",
    subcategory="Broadleaf Melnik 55",
    description="Bulgaria's most distinctive indigenous grape; dark plum, black pepper, dried tobacco, and leather with powerful tannic structure built for long aging",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "Slow-cooked kavarma clay pot lamb with vegetables", "complement", "classic", "main", "Dark fruit and earthy spice are a natural match for Bulgaria's iconic braised lamb clay pot")
    PAIR(prod9, "Grilled kebapche spiced ground meat with shopska salad", "complement", "classic", "main", "Bold, tannic Melnik 55 stands up to intensely spiced ground meat — a quintessential Bulgarian pairing")
    PAIR(prod9, "Aged kashkaval cheese with walnuts and honey", "bridge", "established", "cheese", "Rich, structured red bridges with the sharpness of aged Bulgarian sheep's cheese and bitter walnut")
    PAIR(prod9, "Roasted eggplant with garlic and paprika", "complement", "suggested", "starter", "Earthy, smoky undertones resonate with roasted aubergine and paprika")

p10 = P("Zlaten Rozhen Winery", "Bulgaria", r5, "winery",
         "Smaller estate in the Melnik hills preserving traditional vinification methods for Shiroka Melnishka Loza, producing wines of intense regional character and good value that represent classic Melnik style.")
prod10, new10 = PROD("Zlaten Rozhen Shiroka Melnishka Loza Reserve Melnik", "wine_still", p10, r5, "Bulgaria",
    subcategory="Shiroka Melnishka Loza",
    description="Traditional Melnik varietal wine; concentrated dark fruits, rustic spice, and leather with the characteristic powerful tannic grip of the Struma Valley",
    price_tier="entry")
if new10:
    PAIR(prod10, "Grilled pork ribs with garlic and herbs", "complement", "classic", "main", "Robust, tannic red is a natural match for the richness of grilled pork with aromatic herbs")
    PAIR(prod10, "Lentil soup with smoked paprika and sausage", "complement", "established", "main", "Dark, spiced red resonates with the smoky, earthy depth of hearty lentil and sausage stew")
    PAIR(prod10, "Hard sujuk sausage and pickled vegetables", "complement", "established", "starter", "Bold, tannic Shiroka Melnishka cuts through the fat of cured meat with its structural grip")
    PAIR(prod10, "Banitsa cheese and egg pastry", "contrast", "suggested", "starter", "The wine's tannins provide pleasing contrast to the rich, creamy, salty pastry filling")

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
