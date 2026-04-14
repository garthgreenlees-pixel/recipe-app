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

# ── REGION 1: Riviera del Garda Bresciano ────────────────────────────────────
print("=== Region 1: Riviera del Garda Bresciano ===")
r1 = R("Riviera del Garda Bresciano", "Italy", "wine",
        designation_type="DOC", designation_name="Riviera del Garda Bresciano DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Western Lake Garda DOC producing Groppello, Marzemino and Sangiovese reds and Chardonnay whites; the lake's moderating influence creates wines of uncommon freshness for Lombardy.",
        key_producers="Pasini San Giovanni, Comincioli",
        historical_context="Groppello is Lake Garda's native red variety; the lake's thermal mass gives this western shore a Mediterranean microclimate unusual for northern Italy; wines were celebrated by Mozart who visited the area.")
VIN(r1, 2022, "very_good", "stable", "Lake-moderated warm year; Groppello shows excellent berry and herb character.")
VIN(r1, 2021, "good", "stable", "Balanced season; lake freshness well preserved in the wines.")
VIN(r1, 2020, "very_good", "stable", "Good vintage; Groppello's distinctive character well expressed.")
VIN(r1, 2019, "good", "stable", "Standard vintage; reliable lake-influenced expression.")
VIN(r1, 2018, "good", "stable", "Consistent vintage; honest and food-friendly Garda wines.")
p1a = P("Pasini San Giovanni", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The most historically important Lake Garda estate; centuries of Groppello cultivation on the western Bresciano shore; benchmark for the DOC.",
        reputation_narrative="Most respected Riviera del Garda producer; Groppello Classico earns specialist attention.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Comincioli", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Quality-focused Garda Bresciano estate; Groppello and Chardonnay from the lake's thermal terroir.",
        reputation_narrative="Growing reputation for honest lake-influenced wines; earns attention in Garda specialist circles.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Pasini San Giovanni Riviera del Garda Groppello", "wine_still", p1a, r1, "Italy",
                  subcategory="Groppello",
                  description="Native lake-shore Groppello with raspberry, wild cherry, bitter herb and a distinctive almond finish; light-medium body with lake mineral freshness.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Freshwater perch from Lake Garda", "complement", "classic", "fish_course", "Lake fish and lake wine; the most regional pairing in Lombard cuisine.")
    PAIR(pr1a, "Carne salada (Trentino salt-cured beef)", "complement", "classic", "starter", "Lake Garda's signature cured beef with local red; lemon and herb echo the wine's bitter finish.")
    PAIR(pr1a, "Risotto con lavarello (lake whitefish risotto)", "complement", "classic", "main", "Lake whitefish risotto and Groppello; the Garda lakeside tradition.")
    PAIR(pr1a, "Grilled lake trout with Garda olive oil", "complement", "established", "fish_course", "Trout from the lake and wine from its shore; olive oil from nearby Garda groves bridges.")
pr1b, n1b = PROD("Comincioli Garda Classico Chardonnay", "wine_still", p1b, r1, "Italy",
                  subcategory="Chardonnay",
                  description="Lake Garda-influenced Chardonnay with citrus, stone fruit and a distinctive lake mineral freshness; unoaked for purity.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Bigoli in salsa (Venetian anchovy pasta)", "complement", "established", "main", "Anchovy pasta and clean lake Chardonnay; the wine's freshness balances the anchovy intensity.")
    PAIR(pr1b, "Grilled pike (luccio) al limone", "complement", "classic", "fish_course", "Lake pike with lemon and lake Chardonnay; freshwater fish tradition on the Garda shore.")
    PAIR(pr1b, "Pasta al burro con Grana Padano", "complement", "classic", "main", "Simple butter pasta and lake-fresh Chardonnay; Lombard simplicity at its best.")
    PAIR(pr1b, "Bresaola with rocket and Parmigiano", "complement", "established", "starter", "Lombard air-dried beef and mineral Chardonnay; a northern Italian casual classic.")

# ── REGION 2: Lugana ─────────────────────────────────────────────────────────
print("=== Region 2: Lugana ===")
r2 = R("Lugana", "Italy", "wine",
        designation_type="DOC", designation_name="Lugana DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Southern Lake Garda DOC on the Veneto-Lombardy border; Turbiana (Trebbiano di Lugana) whites of excellent body and mineral character from calcareous clay soils — rising global star among Italian whites.",
        key_producers="Ca' dei Frati, Zenato",
        historical_context="Lugana's Turbiana is genetically distinct from other Trebbiano clones; the dense calcareous clay gives unusual mineral richness and longevity; production tripled in 20 years as global recognition grew.")
VIN(r2, 2022, "excellent", "rising", "Outstanding Lugana vintage; Turbiana shows exceptional body and mineral depth.")
VIN(r2, 2021, "very_good", "stable", "Classic year; precise and mineral with excellent freshness.")
VIN(r2, 2020, "very_good", "stable", "Good vintage; Lugana's ageing potential demonstrated again.")
VIN(r2, 2019, "very_good", "stable", "Warm and expressive; rich and textured with lake influence.")
VIN(r2, 2018, "good", "stable", "Reliable vintage; consistent quality across the appellation.")
p2a = P("Ca' dei Frati", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The founding family of Lugana's quality revolution; three generations of Bottura family commitment to Turbiana's potential; Brolettino is the benchmark Lugana Superiore.",
        reputation_narrative="Ca' dei Frati is synonymous with Lugana excellence; most internationally recognised producer of the appellation.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Zenato", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Dual Lugana-Valpolicella estate; Sergio Zenato pioneered Lugana's global reputation through sustained export efforts and quality investment.",
        reputation_narrative="Most commercially important Lugana producer internationally; Sergio Zenato Riserva earned 95-point scores.",
        price_positioning="mid_range",
        authority_tier=2)
pr2a, n2a = PROD("Ca' dei Frati Brolettino Lugana Superiore", "wine_still", p2a, r2, "Italy",
                  subcategory="Turbiana",
                  description="Benchmark Lugana Superiore with extraordinary depth; citrus, white peach, mineral and a distinctive toasted almond finish; 8-10 year ageing potential.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Risotto al pesce persico del Garda", "complement", "classic", "main", "Lake perch risotto is the Lugana pairing; Turbiana's mineral body perfectly frames the delicate fish.")
    PAIR(pr2a, "Grilled lake whitefish (coregone)", "complement", "classic", "fish_course", "Garda's most prized lake fish with its most prized white wine; regional unity.")
    PAIR(pr2a, "Tortellini in brodo di cappone", "complement", "established", "main", "Northern Italian Sunday tradition; Lugana's mineral weight stands up to the rich broth.")
    PAIR(pr2a, "Seared scallops with Garda lemon and herb butter", "complement", "established", "fish_course", "Scallop sweetness and textured Turbiana; lake lemon bridges through both.")
pr2b, n2b = PROD("Zenato Sergio Zenato Lugana Riserva", "wine_still", p2b, r2, "Italy",
                  subcategory="Turbiana",
                  description="Riserva Lugana with depth and complexity; white peach, almond, mineral and subtle oak integration; one of Italy's finest white wine values.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Tagliolini with white truffle", "complement", "classic", "main", "White truffle and mineral Lugana; structured Turbiana handles both the richness and the earth.")
    PAIR(pr2b, "Carpaccio di branzino con olio di Garda", "complement", "established", "starter", "Raw sea bass with Garda olive oil; Lugana's mineral and texture complement the raw fish.")
    PAIR(pr2b, "Grilled sole with butter and capers", "complement", "classic", "fish_course", "Delicate flat fish and textured Turbiana; caper acidity bridges the wine's mineral note.")
    PAIR(pr2b, "Grana Padano and Lugana-soaked fruit", "complement", "classic", "cheese", "Aged Lombard cheese and the region's great white; a northern Italian cheese course classic.")

# ── REGION 3: Valpolicella Ripasso ────────────────────────────────────────────
print("=== Region 3: Valpolicella Ripasso ===")
r3 = R("Valpolicella Ripasso", "Italy", "wine",
        designation_type="DOC", designation_name="Valpolicella Ripasso DOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Veneto DOC producing Valpolicella wine re-fermented on Amarone pomace; resulting in a richer, more concentrated style between Valpolicella and Amarone; the Veronese wine lover's everyday luxury.",
        key_producers="Masi, Zenato",
        historical_context="Ripasso ('re-passed') was originally a winemaker's secret technique for enriching the basic Valpolicella; commercialised in the 1970s by Masi; now one of Italy's most popular exports.")
VIN(r3, 2022, "very_good", "stable", "Warm Valpolicella year; Ripasso shows excellent concentration from pomace contact.")
VIN(r3, 2021, "good", "stable", "Balanced year; more elegant Ripasso than usual with good freshness.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; classic Ripasso depth and structure.")
VIN(r3, 2019, "very_good", "stable", "Warm and generous; cherry and dark fruit concentration both strong.")
VIN(r3, 2018, "good", "stable", "Solid vintage; accessible and food-friendly Ripasso.")
p3a = P("Masi Agricola", "winery", r3, "Italy",
        production_philosophy="traditional",
        philosophy_description="Valpolicella's most important winery and the commercialiser of Ripasso; Campofiorin was the first branded Ripasso; Masi's research centre has defined modern Amarone production.",
        reputation_narrative="Masi is Italy's most internationally recognised Valpolicella producer; Amarone Costasera earns consistent 95+ points.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Speri Vitivinicoltori", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic family estate in the Valpolicella Classico zone; single-vineyard approach across Ripasso, Amarone and Valpolicella.",
        reputation_narrative="Highly respected for traditional, terroir-expressive Valpolicella wines; Monte Sant'Urbano is the benchmark Amarone cru.",
        price_positioning="mid_range",
        authority_tier=2)
pr3a, n3a = PROD("Masi Campofiorin Ripasso Rosso del Veronese", "wine_still", p3a, r3, "Italy",
                  subcategory="Corvina-Rondinella-Molinara",
                  description="The original branded Ripasso; cherry, dried fruit, chocolate and tobacco with soft tannin and Veronese warmth; medium-full body and 5-10 year ageing potential.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Pasta e fagioli alla veneta", "complement", "classic", "casual", "Venetian bean and pasta soup; Ripasso's dried fruit depth complements the humble richness.")
    PAIR(pr3a, "Grilled Sopressa salume with polenta", "complement", "classic", "casual", "Veneto cured pork and polenta with local red; the Veronese everyday table tradition.")
    PAIR(pr3a, "Risotto all'Amarone con Parmigiano", "complement", "classic", "main", "Amarone-wine risotto and Ripasso; Corvina in both the dish and the glass.")
    PAIR(pr3a, "Braised beef cheeks with Valpolicella", "complement", "established", "main", "Wine-braised beef met by the same wine; Ripasso's dried fruit and spice complete the circle.")
pr3b, n3b = PROD("Speri Valpolicella Ripasso Classico Superiore", "wine_still", p3b, r3, "Italy",
                  subcategory="Corvina-Rondinella",
                  description="Classico zone Ripasso with more precision than volume brands; dark cherry, mocha, dried herbs and fine tannin; elegant and age-worthy.",
                  price_tier="mid_range")
if n3b:
    PAIR(pr3b, "Slow-roasted duck with Venetian spices", "complement", "established", "main", "Duck and Ripasso's spice-dried fruit character; Venetian spice tradition in both.")
    PAIR(pr3b, "Cotechino with lentils (New Year tradition)", "complement", "classic", "main", "Festive northern Italian pork sausage and Ripasso; the Veronese New Year pairing.")
    PAIR(pr3b, "Aged Asiago with mostarda di Cremona", "complement", "classic", "cheese", "Aged Veneto cheese with fruity mustard and Ripasso's dried fruit; sweet-spice harmony.")
    PAIR(pr3b, "Wild mushroom and truffle risotto", "complement", "established", "main", "Earthy mushroom and Ripasso's dried fruit depth; truffle amplifies the wine's complexity.")

# ── REGION 4: Custoza ────────────────────────────────────────────────────────
print("=== Region 4: Custoza ===")
r4 = R("Custoza", "Italy", "wine",
        designation_type="DOC", designation_name="Custoza DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Southern Lake Garda DOC between Lugana and Bardolino; Garganega, Trebbiano and Cortese blend producing fresh, floral, easy-drinking whites from morainic soils — Veneto's overlooked lunch wine.",
        key_producers="Cavalchina, Le Fraghe",
        historical_context="Custoza occupies the glacial moraines above the famous Solferino and Custoza battlefields; the wines are historically associated with refreshing Verona's restaurants and markets; quality is rising steadily.")
VIN(r4, 2022, "very_good", "stable", "Warm Garda year; Custoza shows excellent floral freshness and citrus clarity.")
VIN(r4, 2021, "good", "stable", "Balanced season; Garganega's floral note and Trebbiano's crispness both well expressed.")
VIN(r4, 2020, "very_good", "stable", "Good vintage; more concentration and mineral than usual.")
VIN(r4, 2019, "good", "stable", "Standard vintage; pleasant and food-friendly everyday white.")
VIN(r4, 2018, "good", "stable", "Consistent vintage; reliable and aromatic.")
p4a = P("Cavalchina", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Custoza estate; most respected voice for the DOC's quality potential; single-vineyard Amedeo is the appellation's benchmark white.",
        reputation_narrative="Cavalchina is Custoza's defining producer; Amedeo consistently earns top DOC scores.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Le Fraghe", "winery", r4, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Custoza estate; clean, precise expressions of Garganega and Trebbiano from morainic soils.",
        reputation_narrative="Growing reputation for organic quality in Custoza; earns specialist attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Cavalchina Custoza Superiore Amedeo", "wine_still", p4a, r4, "Italy",
                  subcategory="Garganega-Trebbiano",
                  description="Benchmark Custoza with floral complexity; white peach, acacia, almond and morainic mineral; more texture and length than standard Custoza.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Risotto con asparagi di Bassano", "complement", "classic", "main", "Venetian white asparagus risotto with lake-area white; the spring Verona tradition.")
    PAIR(pr4a, "Fritto di pesce del Garda", "complement", "classic", "casual", "Lake Garda fried fish tradition; floral Custoza refreshes between bites.")
    PAIR(pr4a, "Pasta con trota di lago (lake trout pasta)", "complement", "established", "main", "Lake trout pasta and lake-area white; freshwater mineral in both.")
    PAIR(pr4a, "Light carpaccio di salmone", "complement", "established", "starter", "Delicate raw salmon and floral Custoza; the wine's gentle structure suits the delicate fish.")
pr4b, n4b = PROD("Le Fraghe Custoza Bianco Camporengo", "wine_still", p4b, r4, "Italy",
                  subcategory="Garganega blend",
                  description="Organic morainic Custoza with Garganega-led aromatics; acacia, citrus and light mineral; clean and reliable.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Pizza bianca with mozzarella and basil", "complement", "classic", "casual", "Simple white pizza and floral Italian white; a Verona summer lunch standard.")
    PAIR(pr4b, "Insalata di polpo con limone", "complement", "established", "starter", "Octopus salad and organic lake-area white; lemon bridges the wine's citrus.")
    PAIR(pr4b, "Grilled orata (sea bream) with oil and lemon", "complement", "established", "fish_course", "Delicate fish and clean Custoza; olive oil and lemon link to wine's mineral freshness.")
    PAIR(pr4b, "Bruschetta with local cherry tomatoes", "complement", "classic", "casual", "Simple Veronese antipasto and fresh local white; summer in the Garda hills.")

# ── REGION 5: Bardolino ──────────────────────────────────────────────────────
print("=== Region 5: Bardolino ===")
r5 = R("Bardolino", "Italy", "wine",
        designation_type="DOC", designation_name="Bardolino DOC",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Eastern Lake Garda DOC producing light, pale cherry-coloured Corvina-based reds and Chiaretto rosé; lake-cooling gives extraordinary freshness; one of Italy's most versatile light reds and best rosés.",
        key_producers="Guerrieri Rizzardi, Le Fraghe",
        historical_context="Bardolino was a resort wine for lake tourists; the Chiaretto rosé style predates Provence rosé's international fame by centuries; top producers are demonstrating that Bardolino can be elegant and serious.")
VIN(r5, 2022, "very_good", "stable", "Lake freshness preserved in warm year; Chiaretto of exceptional delicacy.")
VIN(r5, 2021, "good", "stable", "Classic light Bardolino; pale, fresh and aromatic with good acidity.")
VIN(r5, 2020, "very_good", "stable", "Good vintage; Bardolino shows more concentration than usual.")
VIN(r5, 2019, "good", "stable", "Standard vintage; light and aromatic for early drinking.")
VIN(r5, 2018, "good", "stable", "Consistent vintage; honest and food-friendly Bardolino.")
p5a = P("Guerrieri Rizzardi", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic 300-year-old estate on the Garda lakeside; produces the full Bardolino range including Tacchetto Classico; the appellation's most prestigious family estate.",
        reputation_narrative="One of Veneto's great historic wine families; Guerrieri Rizzardi wines embody Garda's elegance and tradition.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Le Fraghe Bardolino", "winery", r5, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Bardolino estate producing the finest Chiaretto in the region; Rodon is the benchmark organic Garda rosé.",
        reputation_narrative="Le Fraghe's Rodon Chiaretto is universally regarded as Italy's finest rosé alongside Cataldi Madonna Cerasuolo.",
        price_positioning="mid_range",
        authority_tier=2)
pr5a, n5a = PROD("Guerrieri Rizzardi Bardolino Classico Tacchetto", "wine_still", p5a, r5, "Italy",
                  subcategory="Corvina-Rondinella",
                  description="Classic Bardolino with pale ruby colour and extraordinary freshness; cherry, rose petal, herb and lake mineral; light-bodied and endlessly versatile.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Lake Garda perch fillets fried in butter", "complement", "classic", "fish_course", "The canonical Garda pairing; light Bardolino and local lake fish — a centuries-old tradition.")
    PAIR(pr5a, "Cold meats and pickles (affettati misti)", "complement", "classic", "casual", "Light Garda red is Italy's perfect charcuterie wine; handles everything without overpowering.")
    PAIR(pr5a, "Spaghetti aglio olio e peperoncino", "complement", "classic", "main", "Spice and garlic pasta with a light Italian red; Bardolino's freshness tames the heat.")
    PAIR(pr5a, "Grilled lake trout en papillote", "complement", "established", "fish_course", "Delicate lake fish and delicate Garda red; pale colour and light tannin suit the fish.")
pr5b, n5b = PROD("Le Fraghe Rodon Bardolino Chiaretto", "wine_still", p5b, r5, "Italy",
                  subcategory="Corvina-Rondinella",
                  description="Italy's finest rosé; pale copper-pink with extraordinary delicacy; wild strawberry, citrus blossom and lake mineral; dry and serious with real persistence.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Carpaccio di tonno con olio del Garda", "complement", "classic", "starter", "Tuna carpaccio with Garda olive oil; rosé's pale delicacy matches the raw fish.")
    PAIR(pr5b, "Grilled lake sardines (alborelle fritte)", "complement", "classic", "casual", "Tiny lake fish fried and served whole; Rodon's minerality and acidity are the perfect pair.")
    PAIR(pr5b, "Salmone al sale con aneto (salt-baked salmon)", "complement", "established", "fish_course", "Dill-fragrant salmon and delicate rosé; herb bridge connects wine and crust.")
    PAIR(pr5b, "Octopus salad with Garda lemon and capers", "complement", "established", "starter", "Adriatic octopus transported to the lake; rosé's freshness handles the Garda lemon acidity.")

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
