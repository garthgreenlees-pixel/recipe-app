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

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── REGION 1: Maremma Toscana ────────────────────────────────────────────────
print("=== Region 1: Maremma Toscana ===")
r1 = R("Maremma Toscana", "Italy", "wine",
        designation_type="DOC", designation_name="Maremma Toscana DOC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Broad Tuscan coastal DOC covering the wild Maremma region; home to Bolgheri's neighbours and Massa Maritima hills; Vermentino whites, Sangiovese and Cabernet-based super-Tuscans from diverse coastal terroirs.",
        key_producers="Brancaia, Moris Farms",
        historical_context="Maremma Toscana DOC was established to accommodate the growing number of quality producers outside Bolgheri and Morellino; Italy's most dynamic quality frontier through the 2000s-2020s.")
VIN(r1, 2022, "excellent", "rising", "Outstanding coastal Maremma vintage; Vermentino and Cabernet both exceptional.")
VIN(r1, 2021, "very_good", "stable", "Good maritime balance; Vermentino aromatic and precise; reds structured.")
VIN(r1, 2020, "excellent", "rising", "One of the decade's finest for coastal Tuscany; concentration and complexity both high.")
VIN(r1, 2019, "very_good", "stable", "Classic Maremma expression; warm Mediterranean depth and good tannin.")
VIN(r1, 2018, "good", "stable", "Solid vintage; accessible and food-friendly across all varieties.")
p1a = P("Moris Farms", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Maremma estate producing Morellino, Vermentino and Avvoltore super-Tuscan from coastal Maremma; one of the DOC's founding voices.",
        reputation_narrative="Avvoltore is a landmark Maremma red that demonstrated coastal Tuscany's premium potential.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Roccapesta", "winery", r1, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Maremma estate in Scansano producing Morellino and Maremma DOC wines with minimal intervention.",
        reputation_narrative="Growing reputation for honest, organic Maremma wines; earns specialist press attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Moris Farms Avvoltore Maremma Toscana", "wine_still", p1a, r1, "Italy",
                  subcategory="Sangiovese-Cabernet-Syrah",
                  description="Landmark super-Tuscan blend with Sangiovese, Cabernet Sauvignon and Syrah; dark fruit, Mediterranean herbs, leather and coastal mineral; powerful and age-worthy.",
                  price_tier="premium")
if n1a:
    PAIR(pr1a, "Grilled bistecca with salsa verde", "complement", "classic", "main", "Tuscan steak tradition with coastal super-Tuscan; salsa verde bridges the herb notes.")
    PAIR(pr1a, "Slow-braised wild boar with Maremma herbs", "complement", "classic", "main", "Maremma hunting tradition; the land's greatest game with its signature wine.")
    PAIR(pr1a, "Aged Pecorino di Maremma with honey", "complement", "classic", "cheese", "Local sheep's cheese with local red; honey bridges and sweetens the dark fruit.")
    PAIR(pr1a, "Duck confit with lentils", "complement", "established", "main", "Rich duck fat and lentil earthiness met by Avvoltore's Mediterranean depth.")
pr1b, n1b = PROD("Roccapesta Maremma Toscana Vermentino", "wine_still", p1b, r1, "Italy",
                  subcategory="Vermentino",
                  description="Organic coastal Maremma Vermentino with citrus, white peach, wild herbs and a pleasantly bitter almond finish; briny mineral and Mediterranean freshness.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Grilled branzino with Mediterranean herbs", "complement", "classic", "fish_course", "Coastal Tuscan fish with coastal Tuscan white; herb and mineral match.")
    PAIR(pr1b, "Fried anchovies with lemon", "complement", "classic", "starter", "Tyrrhenian anchovy tradition; Vermentino's bitter almond and acidity cut through the oil.")
    PAIR(pr1b, "Grilled prawns with wild fennel", "complement", "established", "fish_course", "Maremma coastal seafood; fennel herb bridges Vermentino's Mediterranean character.")
    PAIR(pr1b, "Caprese with buffalo mozzarella", "complement", "classic", "starter", "Simple Tuscan summer salad and fresh coastal white; classic Mediterranean pairing.")

# ── REGION 2: Bolgheri Sassicaia ─────────────────────────────────────────────
print("=== Region 2: Bolgheri Sassicaia ===")
r2 = R("Bolgheri Sassicaia", "Italy", "wine",
        designation_type="DOC", designation_name="Bolgheri Sassicaia DOC",
        reputation_tier="iconic",
        quality_trajectory="established",
        description="The world's only single-estate DOC; Sassicaia by Tenuta San Guido — Italy's most celebrated super-Tuscan and the wine that launched the premium Tuscan revolution through Cabernet Sauvignon on coastal gravel.",
        key_producers="Tenuta San Guido",
        historical_context="Marchese Mario Incisa della Rocchetta planted Cabernet Sauvignon in 1944 inspired by Bordeaux; Sassicaia was initially private; commercial release in 1968 transformed Italian wine; first and only single-estate DOC in Italy.")
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage; Sassicaia shows exceptional concentration and freshness.")
VIN(r2, 2021, "very_good", "stable", "Classic year; Cabernet purity and mineral precision both excellent.")
VIN(r2, 2020, "excellent", "rising", "Landmark vintage; many critics consider it vintage of the decade.")
VIN(r2, 2019, "very_good", "stable", "Warm and generous; Sassicaia shows remarkable depth and length.")
VIN(r2, 2018, "very_good", "stable", "Strong vintage; structured and age-worthy; classic Sassicaia profile.")
p2a = P("Tenuta San Guido", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The estate that created Sassicaia and Italy's super-Tuscan movement; Cabernet Sauvignon from coastal Bolgheri gravel produces Italy's most famous and collectable red wine.",
        reputation_narrative="Sassicaia has achieved 100-point scores and is Italy's most internationally recognised wine; consistently listed among the world's greatest.",
        price_positioning="ultra_premium",
        authority_tier=2)
pr2a, n2a = PROD("Tenuta San Guido Sassicaia Bolgheri", "wine_still", p2a, r2, "Italy",
                  subcategory="Cabernet Sauvignon-Cabernet Franc",
                  description="Italy's most iconic wine; blackcurrant, graphite, cedar, tobacco and coastal mineral with extraordinary length; minimum 15-20 year ageing recommended.",
                  price_tier="ultra_premium")
if n2a:
    PAIR(pr2a, "Aged Chianina tagliata with rocket and Parmigiano", "complement", "classic", "main", "Italy's greatest beef with Italy's most famous red; graphite mineral and dry-aged beef.")
    PAIR(pr2a, "Roasted whole rack of lamb with herbs", "complement", "established", "main", "Premium Cabernet Sauvignon demands premium lamb; herbs bridge the wine's cedar and cassis.")
    PAIR(pr2a, "Wild venison saddle with black truffle", "complement", "classic", "main", "Italian game and Italian luxury wine; truffle links the terroir complexity.")
    PAIR(pr2a, "Aged Parmigiano Reggiano 48 months", "complement", "classic", "cheese", "Long-aged cheese with long-aged super-Tuscan; saline crystals against graphite tannin.")
p2b = P("Le Macchiole", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Bolgheri pioneer producing single-variety super-Tuscans; Messorio (Merlot) and Scrio (Syrah) are among Italy's most sought boutique wines.",
        reputation_narrative="Alongside Sassicaia, Le Macchiole defines Bolgheri's ultra-premium tier; Messorio earns 95-100 points consistently.",
        price_positioning="ultra_premium",
        authority_tier=2)
pr2b, n2b = PROD("Le Macchiole Messorio Bolgheri", "wine_still", p2b, r2, "Italy",
                  subcategory="Merlot",
                  description="100% Merlot from Bolgheri; plum, mocha, violet and coastal mineral with velvety texture; competes with Pomerol's finest at a Tuscan address.",
                  price_tier="ultra_premium")
if n2b:
    PAIR(pr2b, "Braised wagyu short rib", "complement", "classic", "main", "Premium Merlot demands premium beef; Bolgheri mineral and wagyu marbling create Italian luxury.")
    PAIR(pr2b, "Duck liver parfait with brioche", "complement", "established", "starter", "Rich fowl liver and plush Merlot; coastal mineral freshness cuts through the parfait richness.")
    PAIR(pr2b, "Slow-roasted lamb shoulder with Maremma herbs", "complement", "established", "main", "Mediterranean herb lamb and coastal Merlot; shared warmth and depth.")
    PAIR(pr2b, "Aged Taleggio with fig jam", "complement", "established", "cheese", "Washed rind cheese's pungency tamed by Merlot's plush fruit; fig sweetness bridges.")

# ── REGION 3: Val di Cornia ──────────────────────────────────────────────────
print("=== Region 3: Val di Cornia ===")
r3 = R("Val di Cornia", "Italy", "wine",
        designation_type="DOC", designation_name="Val di Cornia DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Tuscan coastal DOC near Suvereto and Campiglia Marittima; iron-rich clay and schist soils produce powerful Sangiovese and Cabernet-based reds of surprising depth; the Maremma's most overlooked quality area.",
        key_producers="Gualdo del Re, Petra",
        historical_context="Val di Cornia surrounds Suvereto — a medieval hilltop town that gained its own DOCG; the iron-rich soils (Colline Metallifere) give wines a distinctive mineral quality; growing cult following for 'discovery' wines.")
VIN(r3, 2022, "very_good", "stable", "Iron-rich soils deliver mineral concentration; Sangiovese excellent.")
VIN(r3, 2021, "good", "stable", "Balanced year; wines fresh and structured with iron mineral well expressed.")
VIN(r3, 2020, "excellent", "rising", "Exceptional vintage; depth and mineral complexity both outstanding.")
VIN(r3, 2019, "very_good", "stable", "Warm Mediterranean expression; Suvereto reds show real power.")
VIN(r3, 2018, "good", "stable", "Solid vintage; honest and food-friendly.")
p3a = P("Gualdo del Re", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Val di Cornia estate producing serious Sangiovese and Cabernet from iron-rich Suvereto soils; benchmark for the emerging appellation.",
        reputation_narrative="Most celebrated Val di Cornia producer; earns consistent top scores from Italian and international press.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Petra", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Modern Suvereto estate with spectacular architecture; Cabernet-dominated blends from Colline Metallifere iron soils.",
        reputation_narrative="Internationally visible for architecture and wine quality; growing critical reputation.",
        price_positioning="premium",
        authority_tier=1)
pr3a, n3a = PROD("Gualdo del Re Suvereto Sangiovese Rennero", "wine_still", p3a, r3, "Italy",
                  subcategory="Sangiovese",
                  description="Iron-mineral Suvereto Sangiovese with dark cherry, dried herbs, iron and earth; more structured and mineral than Morellino with real ageing ambition.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Wild boar cinta senese with polenta", "complement", "classic", "main", "Tuscan native game with iron-mineral Sangiovese; the Colline Metallifere's signature match.")
    PAIR(pr3a, "Grilled beef tagliata with rucola", "complement", "classic", "main", "Tuscan beef and structured Sangiovese; iron mineral in both wine and red meat.")
    PAIR(pr3a, "Pecorino di Maremma stagionato", "complement", "classic", "cheese", "Aged coastal sheep cheese with iron-mineral red; regional Maremma unity.")
    PAIR(pr3a, "Ribollita with cavolo nero", "complement", "classic", "casual", "Tuscan bean and black cabbage stew; Sangiovese acidity cuts through the hearty richness.")
pr3b, n3b = PROD("Petra Suvereto Cabernet Franc Val di Cornia", "wine_still", p3b, r3, "Italy",
                  subcategory="Cabernet Franc",
                  description="Val di Cornia Cabernet Franc from iron-schist soils; violet, graphite, cassis and a distinctive iron mineral note that sets it apart from Bordeaux equivalents.",
                  price_tier="premium")
if n3b:
    PAIR(pr3b, "Roasted pigeon with Maremma truffle", "complement", "classic", "main", "Game bird and Maremma truffle with iron-mineral Cabernet Franc; a luxury Tuscan pairing.")
    PAIR(pr3b, "Lamb saddle with artichoke gratin", "complement", "established", "main", "Premium lamb and graphite Cabernet Franc; artichoke bitterness bridges the iron mineral.")
    PAIR(pr3b, "Aged Cacio di Fossa (pit-aged cheese)", "complement", "classic", "cheese", "Italian pit-aged cheese with Suvereto red; intense earthy cheese meets iron mineral wine.")
    PAIR(pr3b, "Braised veal cheeks with root vegetables", "complement", "established", "main", "Collagen-rich veal braise met by Cabernet Franc's structure; a refined Italian match.")

# ── REGION 4: Terre di Pisa ──────────────────────────────────────────────────
print("=== Region 4: Terre di Pisa ===")
r4 = R("Terre di Pisa", "Italy", "wine",
        designation_type="DOC", designation_name="Terre di Pisa DOC",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Small Tuscan DOC on the hills between Pisa and Volterra producing Sangiovese from sandy marine-sediment soils with unusual elegance and minerality; a discovery appellation for Tuscan specialists.",
        key_producers="Podere Bello, Tenuta di Ghizzano",
        historical_context="Terre di Pisa's marine sand soils give Sangiovese a distinctive lightness and mineral salinity unlike any other Tuscan appellation; gaining attention from producers fleeing Chianti land prices.")
VIN(r4, 2022, "very_good", "stable", "Sandy soils deliver elegant, pale Sangiovese with good acidity.")
VIN(r4, 2021, "good", "stable", "Cooler season; light and aromatic Sangiovese with refreshing freshness.")
VIN(r4, 2020, "very_good", "stable", "Good quality; marine mineral well expressed in the Sangiovese.")
VIN(r4, 2019, "very_good", "stable", "Classic expression; elegant Sangiovese with unusual Pisan character.")
VIN(r4, 2018, "good", "stable", "Standard vintage; honest and food-friendly.")
p4a = P("Tenuta di Ghizzano", "winery", r4, "Italy",
        production_philosophy="organic",
        philosophy_description="Historic organic Pisan estate producing elegant Sangiovese and Merlot from ancient sandy hillside vineyards near Volterra; the appellation's quality leader.",
        reputation_narrative="Veneroso is the benchmark Terre di Pisa red; earns national attention for unusual Tuscan elegance.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Podere Bello", "winery", r4, "Italy",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Terre di Pisa estate focusing on light-handed Sangiovese from marine sand; natural wine philosophy.",
        reputation_narrative="Emerging natural wine voice for the appellation; earns attention from Italian specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Tenuta di Ghizzano Veneroso Terre di Pisa", "wine_still", p4a, r4, "Italy",
                  subcategory="Sangiovese-Merlot",
                  description="Organic Terre di Pisa red with cherry, violets, marine mineral and a lightness unusual for Tuscan reds; medium-bodied and distinctly elegant.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Pasta with fresh sea urchin (ricci)", "complement", "suggested", "main", "Unusual match: marine mineral Sangiovese and sea urchin; shared salinity creates discovery.")
    PAIR(pr4a, "Roast guinea fowl with lemon and herbs", "complement", "established", "main", "Delicate poultry and elegant sandy-soil Sangiovese; a refined Tuscan lunch.")
    PAIR(pr4a, "Grilled fish with Pisan olive oil", "complement", "established", "fish_course", "Marine-mineral Sangiovese and seafood — unconventional but the sandy soil bridges it.")
    PAIR(pr4a, "Light rabbit ragù with fresh tagliatelle", "complement", "established", "main", "Delicate game and delicate Terre di Pisa red; lighter Sangiovese style suits rabbit.")
pr4b, n4b = PROD("Podere Bello Terre di Pisa Sangiovese Naturale", "wine_still", p4b, r4, "Italy",
                  subcategory="Sangiovese",
                  description="Biodynamic sandy-soil Sangiovese with pale ruby colour, fresh cherry, herbs and sea mineral; light, lively and natural wine in character.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Grilled eel with Pisan herbs", "complement", "classic", "main", "Sandy-soil Sangiovese and Arno river eel; Pisan tradition dating to the medieval republic.")
    PAIR(pr4b, "Ribollita with Pisan olive oil finish", "complement", "classic", "casual", "Tuscan bean soup with local natural Sangiovese; simple and regional.")
    PAIR(pr4b, "Cecina (Ligurian chickpea flatbread)", "complement", "classic", "casual", "Tuscan-Ligurian chickpea tradition; the wine's lightness matches the humble flatbread.")
    PAIR(pr4b, "Fried local fish (bianchetti di mare)", "complement", "established", "casual", "Tiny fried whitebait from Pisan coast; pale natural Sangiovese and crispy fish.")

# ── REGION 5: Cortona ────────────────────────────────────────────────────────
print("=== Region 5: Cortona ===")
r5 = R("Cortona", "Italy", "wine",
        designation_type="DOC", designation_name="Cortona DOC",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Small Tuscan DOC near the Etruscan hilltown of Cortona and Lake Trasimeno; Syrah, Sangiovese and Chardonnay from clay-limestone soils; best known for Italy's finest Syrah.",
        key_producers="Stefano Amerighi, Tenimenti d'Alessandro",
        historical_context="Cortona's claim to fame is unexpected: Italy's finest Syrah grows here on clay soils between Tuscany and Umbria; Luca d'Alessandro proved Syrah could compete with the Rhône from this improbable Tuscan location.")
VIN(r5, 2022, "excellent", "rising", "Outstanding Syrah vintage; concentration and Northern Rhône-like pepper both excellent.")
VIN(r5, 2021, "very_good", "stable", "Cooler season; Syrah shows more floral and elegant character than usual.")
VIN(r5, 2020, "excellent", "rising", "Landmark vintage for Cortona; Syrah at its most complex and age-worthy.")
VIN(r5, 2019, "very_good", "stable", "Classic expression; dark olive, pepper and dark fruit in fine balance.")
VIN(r5, 2018, "very_good", "stable", "Strong vintage; structured and age-worthy Cortona Syrah.")
p5a = P("Stefano Amerighi", "winery", r5, "Italy",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Cortona producer making Italy's most celebrated Syrah from ancient clay-limestone soils; minimal intervention from vineyard to bottle.",
        reputation_narrative="Amerighi's Cortona Syrah is widely considered Italy's greatest Syrah expression; scores 95+ regularly.",
        price_positioning="premium",
        authority_tier=2)
p5b = P("Tenimenti d'Alessandro", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The estate that first demonstrated Cortona's Syrah potential; Il Bosco single-vineyard Syrah put Cortona on Italy's quality map.",
        reputation_narrative="Historic role in Cortona's quality narrative; Il Bosco remains a benchmark Syrah.",
        price_positioning="premium",
        authority_tier=2)
pr5a, n5a = PROD("Stefano Amerighi Cortona Syrah", "wine_still", p5a, r5, "Italy",
                  subcategory="Syrah",
                  description="Biodynamic Cortona Syrah of extraordinary depth; black olive, pepper, dark cherry, smoke and Northern Rhône-like mineral; 15+ year ageing recommended.",
                  price_tier="premium")
if n5a:
    PAIR(pr5a, "Roasted wild boar with olive and caper sauce", "complement", "classic", "main", "Tuscan game with Italy's finest Syrah; olive and caper bridge the wine's olive character.")
    PAIR(pr5a, "Slow-roasted lamb shoulder with Tuscan herbs", "complement", "classic", "main", "Syrah and lamb is the Rhône canon applied to Tuscany; pepper and herb in harmony.")
    PAIR(pr5a, "Grilled bistecca with smoked olive oil", "complement", "established", "main", "Italy's greatest steak with Italy's finest Syrah; smoke in both the wine and the grill.")
    PAIR(pr5a, "Aged Cacio di Fossa with black truffle honey", "complement", "established", "cheese", "Pit-aged cheese intensity met by Syrah's depth; truffle honey bridges the wine's olive note.")
pr5b, n5b = PROD("Tenimenti d'Alessandro Il Bosco Cortona Syrah", "wine_still", p5b, r5, "Italy",
                  subcategory="Syrah",
                  description="Founding Cortona Syrah; dark fruit, black olive, pepper and Tuscan mineral; rich and structured with proven ageing potential.",
                  price_tier="premium")
if n5b:
    PAIR(pr5b, "Grilled lamb chops with rosemary and mint", "complement", "classic", "main", "The Rhône applied to Tuscany; classic Syrah-lamb with Italian herb companions.")
    PAIR(pr5b, "Braised beef short ribs with black olives", "complement", "established", "main", "Rich braised beef and Cortona Syrah's olive character; a Tuscan-Mediterranean bridge.")
    PAIR(pr5b, "Duck breast with fig reduction", "complement", "established", "main", "Duck's richness and Syrah's dark fruit; fig sweetness bridges the black olive note.")
    PAIR(pr5b, "Aged Pecorino with black olive tapenade", "complement", "classic", "cheese", "Olive in both cheese accompaniment and wine; an assertive Cortona cheese course.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
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
