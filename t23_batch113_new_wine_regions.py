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

# ── REGION 1: Sagrantino di Montefalco ──────────────────────────────────────
print("=== Region 1: Sagrantino di Montefalco ===")
r1 = R("Sagrantino di Montefalco", "Italy", "wine",
        designation_type="DOCG", designation_name="Sagrantino di Montefalco DOCG",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Small Umbrian DOCG producing 100% Sagrantino — Italy's most tannic native variety with extraordinary polyphenol concentration; rich, powerful reds demanding long ageing from red clay-limestone hillsides.",
        key_producers="Arnaldo Caprai, Paolo Bea",
        historical_context="Sagrantino was almost extinct in the 1970s; Marco Caprai revived it through investment and research in the 1980s; now one of Italy's most collected and celebrated appellations.")
VIN(r1, 2022, "very_good", "stable", "Warm Umbrian year; Sagrantino shows excellent dark fruit and manageable tannin.")
VIN(r1, 2021, "good", "stable", "Cooler season; more elegant expressions than usual; tannin refined.")
VIN(r1, 2020, "excellent", "rising", "Outstanding; best Sagrantino in a decade with extraordinary concentration.")
VIN(r1, 2019, "very_good", "stable", "Classic vintage; dark plum, blackberry and iron tannin in fine balance.")
VIN(r1, 2018, "very_good", "stable", "Strong vintage; powerful and age-worthy Sagrantino.")
p1a = P("Arnaldo Caprai", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The dominant force in Sagrantino's revival; Marco Caprai's research with viticulture and enology transformed the variety from obscure to celebrated.",
        reputation_narrative="25 Anni is universally considered Sagrantino's benchmark wine; Caprai's entire range is reference standard.",
        price_positioning="premium",
        authority_tier=2)
p1b = P("Paolo Bea", "winery", r1, "Italy",
        production_philosophy="traditional",
        philosophy_description="Artisan Sagrantino producer using traditional extended maceration, natural fermentation and no filtration; Sagrantino at its most austere and age-worthy.",
        reputation_narrative="Cult natural wine producer; Pagliaro Riserva is one of Umbria's rarest and most sought wines.",
        price_positioning="premium",
        authority_tier=2)
pr1a, n1a = PROD("Arnaldo Caprai Sagrantino di Montefalco 25 Anni", "wine_still", p1a, r1, "Italy",
                  subcategory="Sagrantino",
                  description="Benchmark Sagrantino with extraordinary tannin, dark plum, blackberry, iron and leather; 25-year ageing potential minimum; Italy's most structurally impressive red.",
                  price_tier="premium")
if n1a:
    PAIR(pr1a, "Slow-braised wild boar with juniper and bay", "complement", "classic", "main", "Sagrantino's massive tannin demands gamey, fatty meat; boar braised for 6 hours is the answer.")
    PAIR(pr1a, "Grilled Chianina bistecca tagliata", "complement", "classic", "main", "Italy's greatest beef with Italy's most tannic wine; iron and iron in mutual amplification.")
    PAIR(pr1a, "Aged Pecorino di Norcia with truffle honey", "complement", "classic", "cheese", "Old Umbrian sheep cheese and powerful red; tannin softened by fat and sweetened by honey.")
    PAIR(pr1a, "Umbrian black truffle pasta (strangozzi al tartufo)", "complement", "established", "main", "Earthy truffle and iron-mineral Sagrantino; Umbrian luxury pairing.")
pr1b, n1b = PROD("Paolo Bea Sagrantino di Montefalco Pagliaro", "wine_still", p1b, r1, "Italy",
                  subcategory="Sagrantino",
                  description="Natural Sagrantino of immense depth; unfiltered, extended maceration; dried herbs, dried plum, leather, iron and extraordinary tannin with 30+ year potential.",
                  price_tier="premium")
if n1b:
    PAIR(pr1b, "Cinghiale in umido con olive e capperi", "complement", "classic", "main", "Umbrian wild boar stew; the ultimate Sagrantino companion — fat, acid and herb against tannin.")
    PAIR(pr1b, "Agnello alla brace con rosmarino", "complement", "established", "main", "Charcoal lamb with rosemary; Bea's tannin needs the fat and char to show its best.")
    PAIR(pr1b, "Aged Parmigiano Reggiano (36 months)", "complement", "established", "cheese", "Crystalline aged cheese with powerful Sagrantino; saline crystals cut through the tannin.")
    PAIR(pr1b, "Dark chocolate with hazelnuts", "complement", "suggested", "dessert", "70%+ dark chocolate's bitterness in dialogue with Sagrantino's massive structure; rare.")

# ── REGION 2: Torgiano Rosso Riserva ─────────────────────────────────────────
print("=== Region 2: Torgiano Rosso Riserva ===")
r2 = R("Torgiano Rosso Riserva", "Italy", "wine",
        designation_type="DOCG", designation_name="Torgiano Rosso Riserva DOCG",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Tiny Umbrian DOCG created to recognise Lungarotti's Rubesco Riserva Vigna Monticchio; Sangiovese-Canaiolo from ancient Torgiano soils; one of Italy's most distinctive individual-producer DOCGs.",
        key_producers="Lungarotti",
        historical_context="Giorgio Lungarotti created modern Umbrian wine singlehandedly in the 1960s; his lobbying established Torgiano DOC and then DOCG for the Riserva; the Lungarotti wine museum in Torgiano is Italy's finest wine museum.")
VIN(r2, 2022, "very_good", "stable", "Classic vintage; Rubesco Riserva shows excellent dark cherry and mineral character.")
VIN(r2, 2021, "good", "stable", "Lighter year; more elegant and aromatic than usual; good ageing potential.")
VIN(r2, 2020, "excellent", "rising", "Outstanding; one of the finest Torgiano Riservas of the decade.")
VIN(r2, 2019, "very_good", "stable", "Warm and generous; Sangiovese shows depth and well-integrated tannin.")
VIN(r2, 2018, "very_good", "stable", "Strong vintage; classic Umbrian expression with excellent structure.")
p2a = P("Lungarotti", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The sole producer of Torgiano Rosso Riserva DOCG; three generations of the Lungarotti family have defined Umbrian wine quality and established the Torgiano wine culture.",
        reputation_narrative="Rubesco Riserva Vigna Monticchio is one of Italy's great collector wines; Giorgio Lungarotti's legacy is immeasurable.",
        price_positioning="premium",
        authority_tier=2)
p2b = P("Tenuta di Salviano", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Nearby Torgiano estate producing Sangiovese and Trebbiano Spoletino from Umbrian hillside vineyards.",
        reputation_narrative="Secondary Torgiano producer of genuine quality; growing reputation for age-worthy reds.",
        price_positioning="mid_range",
        authority_tier=1)
pr2a, n2a = PROD("Lungarotti Torgiano Rosso Riserva Vigna Monticchio", "wine_still", p2a, r2, "Italy",
                  subcategory="Sangiovese-Canaiolo",
                  description="Iconic single-vineyard Sangiovese with extraordinary complexity; dried cherry, leather, tobacco, dark chocolate and mineral; minimum 10-year ageing recommended.",
                  price_tier="premium")
if n2a:
    PAIR(pr2a, "Roast pigeon with black truffle sauce", "complement", "classic", "main", "Umbrian game bird with the region's most storied red; truffle unites land and wine.")
    PAIR(pr2a, "Bistecca di vitellone with rosemary and garlic", "complement", "established", "main", "Umbrian beef with the region's benchmark Sangiovese; structural match.")
    PAIR(pr2a, "Aged Parmigiano Reggiano with fig compote", "complement", "classic", "cheese", "Long-aged Sangiovese with long-aged cheese; fig sweetness bridges the wine's dried fruit.")
    PAIR(pr2a, "Slow-braised oxtail Umbrian-style", "complement", "established", "main", "Collagen-rich braise needs structured wine; Monticchio's depth handles the richness.")
pr2b, n2b = PROD("Lungarotti Torre di Giano Bianco Torgiano", "wine_still", p2a, r2, "Italy",
                  subcategory="Trebbiano Toscano-Grechetto",
                  description="Classic Lungarotti white from Trebbiano and Grechetto; citrus, almond and mineral with good freshness; the Umbrian white wine benchmark.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Umbrian lentil soup with extra virgin olive oil", "complement", "classic", "casual", "Castelluccio lentils with local white wine; an Umbrian winter classic.")
    PAIR(pr2b, "Grilled lake perch with herbs", "complement", "established", "fish_course", "Umbrian lake fish with local white; the wine's almond note complements the delicate fish.")
    PAIR(pr2b, "Strangozzi pasta with truffle shavings", "complement", "established", "main", "Umbrian pasta and white truffle with Lungarotti's white; a refined Umbrian lunch.")
    PAIR(pr2b, "Pecorino fresco di norcia with honey", "complement", "classic", "cheese", "Young sheep's cheese and Grechetto-Trebbiano white; almond and dairy in harmony.")

# ── REGION 3: Colli Martani ──────────────────────────────────────────────────
print("=== Region 3: Colli Martani ===")
r3 = R("Colli Martani", "Italy", "wine",
        designation_type="DOC", designation_name="Colli Martani DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Umbrian DOC in the hills between Torgiano and Montefalco; home to Grechetto di Todi whites and Sangiovese-Trebbiano Spoletino blends from limestone-clay hillsides.",
        key_producers="Perticaia, Terre de la Custodia",
        historical_context="Long overshadowed by Sagrantino and Torgiano; Colli Martani is Umbria's quiet achiever with Trebbiano Spoletino and Grechetto varieties showing increasing ambition from dedicated producers.")
VIN(r3, 2022, "very_good", "stable", "Warm Umbrian hills; Trebbiano Spoletino shows excellent aromatic concentration.")
VIN(r3, 2021, "good", "stable", "Balanced year; Grechetto and Trebbiano both expressive and fresh.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; emerging quality from ambitious producers.")
VIN(r3, 2019, "good", "stable", "Standard vintage; honest expressions of Umbrian varieties.")
VIN(r3, 2018, "good", "stable", "Reliable; Trebbiano Spoletino showing consistent improvement.")
p3a = P("Perticaia", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Quality-focused Colli Martani estate producing Trebbiano Spoletino whites of surprising depth and a structured Montefalco Rosso.",
        reputation_narrative="Leading voice for Trebbiano Spoletino's potential; earns national attention from Umbrian specialists.",
        price_positioning="mid_range",
        authority_tier=1)
p3b = P("Terre de la Custodia", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Large Colli Martani estate producing reliable Grechetto and Sangiovese from extensive Umbrian hillside holdings.",
        reputation_narrative="Volume benchmark for the DOC; consistent quality across accessible range.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Perticaia Trebbiano Spoletino Umbria", "wine_still", p3a, r3, "Italy",
                  subcategory="Trebbiano Spoletino",
                  description="Rare Trebbiano Spoletino with more body and aromatic complexity than other Trebbianos; stone fruit, hazelnut, herb and mineral with surprising ageing potential.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Pasta con le noci (walnut pasta)", "complement", "classic", "main", "Walnut richness and Trebbiano Spoletino's hazelnut notes; Umbrian nut tradition in dialogue.")
    PAIR(pr3a, "Roast pork loin with fennel and herbs", "complement", "established", "main", "Structured Trebbiano Spoletino handles pork's richness; fennel bridges the herb notes.")
    PAIR(pr3a, "Farro soup with Castelluccio lentils", "complement", "classic", "casual", "Umbrian grain and pulse tradition; textured white wine for hearty peasant soup.")
    PAIR(pr3a, "Grilled trout with almonds", "complement", "established", "fish_course", "River trout and the wine's almond character; Umbrian inland freshwater tradition.")
pr3b, n3b = PROD("Terre de la Custodia Colli Martani Grechetto", "wine_still", p3b, r3, "Italy",
                  subcategory="Grechetto",
                  description="Reliable Colli Martani Grechetto with citrus, almond and mineral freshness; versatile and food-friendly.",
                  price_tier="value")
if n3b:
    PAIR(pr3b, "Ribollita Umbra (bean and bread stew)", "complement", "classic", "casual", "Peasant Umbrian cuisine with honest local white; simple harmony.")
    PAIR(pr3b, "Grilled chicken with herbs", "complement", "classic", "main", "Classic Italian poultry with clean Grechetto; versatile everyday match.")
    PAIR(pr3b, "Bruschetta with tomato and basil", "complement", "classic", "casual", "Antipasto staple and Italian white; Grechetto's freshness matches the tomato acidity.")
    PAIR(pr3b, "Tagliatelle with porcini mushrooms", "complement", "established", "main", "Earthy mushroom pasta and almond-mineral Grechetto; Umbrian fungi tradition.")

# ── REGION 4: Vernaccia di San Gimignano ────────────────────────────────────
print("=== Region 4: Vernaccia di San Gimignano ===")
r4 = R("Vernaccia di San Gimignano", "Italy", "wine",
        designation_type="DOCG", designation_name="Vernaccia di San Gimignano DOCG",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Tuscan DOCG in the medieval tower town of San Gimignano; Italy's first DOC (1966) produces Vernaccia whites of distinctive bitter almond finish and mineral precision from Cretaceous clay-limestone soils.",
        key_producers="Panizzi, Teruzzi",
        historical_context="Vernaccia di San Gimignano was Italy's first wine DOC in 1966; Dante celebrated it; the appellation suffered from tourist demand and bulk production but a new generation is restoring its quality.")
VIN(r4, 2022, "very_good", "stable", "Warm Tuscan vintage; Vernaccia shows more tropical richness than usual with good structure.")
VIN(r4, 2021, "good", "stable", "Cooler season; classic lean Vernaccia with sharp mineral and bitter almond.")
VIN(r4, 2020, "excellent", "rising", "Outstanding; complex and structured Vernaccia of real ageing potential.")
VIN(r4, 2019, "very_good", "stable", "Classic expression; crisp, mineral and persistent with good length.")
VIN(r4, 2018, "good", "stable", "Reliable vintage; food-friendly and consistent.")
p4a = P("Panizzi", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading San Gimignano estate producing single-vineyard Vernaccia of genuine complexity; Vigna Santa Margherita is the appellation's most ambitious cru.",
        reputation_narrative="Universally acknowledged as the finest Vernaccia producer; consistently earns top scores in Italian wine press.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Teruzzi", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The historic San Gimignano estate that first showed Vernaccia could be a serious wine; Terre di Tufi is an iconic multi-varietal Tuscan white.",
        reputation_narrative="Pioneer of modern Vernaccia quality; Terre di Tufi remains one of Tuscany's landmark white wines.",
        price_positioning="mid_range",
        authority_tier=2)
pr4a, n4a = PROD("Panizzi Vernaccia di San Gimignano Vigna Santa Margherita", "wine_still", p4a, r4, "Italy",
                  subcategory="Vernaccia",
                  description="Single-vineyard Vernaccia of real depth; bitter almond, citrus, mineral, white truffle and a long oxidative complexity; rivals top Burgundy whites in structure.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "White truffle tagliatelle (tartufo bianco)", "complement", "classic", "main", "San Gimignano is near the white truffle country; Vernaccia's mineral echoes the earth.")
    PAIR(pr4a, "Bistecca di vitellone Chianina al sangue", "complement", "suggested", "main", "Unusual pairing: rare steak and mineral white; bitter almond tannin cuts through rare beef fat.")
    PAIR(pr4a, "Crostino di fegato toscano (liver crostini)", "complement", "classic", "starter", "Tuscan liver crostini and bitter-mineral Vernaccia; the wine's bitterness complements the liver.")
    PAIR(pr4a, "Pan-fried veal sweetbreads", "complement", "established", "starter", "Delicate offal demands a structured white with bitterness and mineral; Vernaccia ideal.")
pr4b, n4b = PROD("Teruzzi Vernaccia di San Gimignano", "wine_still", p4b, r4, "Italy",
                  subcategory="Vernaccia",
                  description="Classic benchmark Vernaccia with citrus, bitter almond and mineral precision; the archetype of the variety.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Ribollita toscana", "complement", "classic", "casual", "Tuscan bean and bread soup with the region's classic white; winter Tuscan table tradition.")
    PAIR(pr4b, "Grilled sea bass with Tuscan olive oil", "complement", "established", "fish_course", "Simple elegant fish and elegant Tuscan white; bitter almond note links to the olive oil.")
    PAIR(pr4b, "Pappardelle con funghi porcini", "complement", "established", "main", "Mushroom pappardelle and mineral Vernaccia; earthy and clean.")
    PAIR(pr4b, "Pecorino senese fresco with herbs", "complement", "classic", "cheese", "Young Siena sheep's cheese with the region's signature white; fresh dairy meets bitter mineral.")

# ── REGION 5: Piave ─────────────────────────────────────────────────────────
print("=== Region 5: Piave ===")
r5 = R("Piave", "Italy", "wine",
        designation_type="DOC", designation_name="Piave DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Veneto DOC on the Piave river plain producing Raboso del Piave — one of Italy's most acidic and tannic native varieties — alongside Merlot and Cabernet Franc from alluvial-clay soils.",
        key_producers="Ornella Molon, Rechsteiner",
        historical_context="Raboso is one of Italy's most extreme red varieties; extremely high acid and tannin make it a challenge to enjoy young; the Piave's warrior wine has survived wars and phylloxera; now gaining cult status.")
VIN(r5, 2022, "very_good", "stable", "Warm year softens Raboso's extremity; more approachable than usual.")
VIN(r5, 2021, "good", "stable", "Classic tart Raboso vintage; high acidity and green-edged tannin.")
VIN(r5, 2020, "very_good", "stable", "Good ripeness; Raboso shows characteristic dark cherry with managed tannin.")
VIN(r5, 2019, "very_good", "stable", "Warm and generous; Raboso achieves unusual balance in this vintage.")
VIN(r5, 2018, "good", "stable", "Standard vintage; honest Raboso character for cellar ageing.")
p5a = P("Ornella Molon", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Piave DOC producer working alluvial soils to produce serious Raboso and other Veneto varieties; champion of the grape's potential.",
        reputation_narrative="Most respected Piave DOC voice; Raboso Maser is the appellation's quality benchmark.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Rechsteiner", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Austrian-origin Treviso estate producing Raboso and Merlot from Piave clay soils; classic approach with modern precision.",
        reputation_narrative="Respected for consistent quality and honest Piave character; well distributed in northeastern Italy.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Ornella Molon Raboso del Piave Maser", "wine_still", p5a, r5, "Italy",
                  subcategory="Raboso",
                  description="Benchmark Raboso with fierce tannin and acidity balanced by dark cherry intensity; dried plum, iron and earth; requires 10+ years ageing.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Bollito misto with mostarda di Cremona", "complement", "classic", "main", "Veneto boiled meats demand a tannic, acidic red to cut through; Raboso is the traditional match.")
    PAIR(pr5a, "Aged Montasio or Asiago d'Allevo", "complement", "classic", "cheese", "Aged Veneto cheese with fierce Veneto red; the fat and crystalline structure of old cheese tames Raboso.")
    PAIR(pr5a, "Cassoeula (Lombardy pork and cabbage stew)", "complement", "established", "main", "Rich fatty pork stew needs a wine with astringency; Raboso's tannin cleans the palate.")
    PAIR(pr5a, "Dark chocolate cake with sour cherry", "complement", "suggested", "dessert", "Raboso's extreme character meets dark chocolate and sour cherry; unusual but compelling.")
pr5b, n5b = PROD("Rechsteiner Piave Cabernet Franc", "wine_still", p5b, r5, "Italy",
                  subcategory="Cabernet Franc",
                  description="Piave Cabernet Franc from clay-alluvial soils; green pepper, violet, currant and a fine mineral edge; medium-bodied and food-friendly.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Grilled duck breast with cherry sauce", "complement", "established", "main", "Cabernet Franc's violet and currant amplify duck cherry sauce; green pepper adds dimension.")
    PAIR(pr5b, "Roasted lamb rack with herbs", "complement", "classic", "main", "Classic Cabernet Franc pairing; green herb and red meat in natural harmony.")
    PAIR(pr5b, "Risi e bisi (Venetian pea and rice soup)", "complement", "established", "casual", "Venetian spring tradition; Cabernet Franc's freshness matches the bright pea sweetness.")
    PAIR(pr5b, "Soft Taleggio with walnut bread", "complement", "established", "cheese", "Washed rind cheese and light-bodied Cabernet Franc; the wine's freshness balances the pungency.")

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
