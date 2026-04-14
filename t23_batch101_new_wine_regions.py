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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
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

# ── Region 1: Franciacorta ────────────────────────────────────────────────────
print("=== Region 1: Franciacorta ===")
r = R("Franciacorta", "Italy", "wine",
      designation_type="DOCG", designation_name="Franciacorta DOCG",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Lombardy's lake-district sparkling wine DOCG; Chardonnay, Pinot Nero and Pinot Bianco in the Champagne method; Italy's most serious sparkling wine rival to Champagne; aged minimum 18 months.",
      key_producers="Ca' del Bosco, Bellavista, Berlucchi, Contadi Castaldi",
      historical_context="Guido Berlucchi created the first Franciacorta in 1961; Ca' del Bosco (Maurizio Zanella) and Bellavista elevated it to DOCG status in 1995; Italy's answer to Champagne.")
VIN(r, 2019, "exceptional", "rising", "Outstanding Franciacorta harvest; Chardonnay of rare precision; benchmark for NV blending.")
VIN(r, 2018, "excellent", "rising", "Classic year; Franciacorta of fine structure and aging potential.")
VIN(r, 2017, "excellent", "stable", "Good base year; top producers delivered precise, food-friendly cuvées.")
VIN(r, 2016, "very_good", "stable", "Consistent quality; Franciacorta DOCG wines aging well.")
VIN(r, 2015, "exceptional", "rising", "Landmark vintage; Satèn and Blanc de Blancs of extraordinary complexity now showing.")
p1 = P("Ca' del Bosco", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Maurizio Zanella's iconic Franciacorta estate; Annamaria Clementi is their prestige vintage wine; obsessive attention to base wine quality; dosage from reserve wines aged up to 9 years.",
       reputation_narrative="Ca' del Bosco is Italy's most celebrated sparkling wine producer; Annamaria Clementi is the Krug of Franciacorta.",
       price_positioning="premium")
p2 = P("Bellavista", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Vittorio Moretti's benchmark estate; Teatro alla Scala is their long-aged prestige cuvée; Alma (NV) is their accessible introduction; focus on Chardonnay expression.",
       reputation_narrative="Bellavista's Teatro alla Scala is among Italy's greatest sparkling wines; the estate helped establish Franciacorta's international reputation.",
       price_positioning="premium")
pr1, n1 = PROD("Ca' del Bosco Cuvée Prestige Franciacorta Brut", "wine_sparkling", p1, r, "Italy",
               subcategory="Chardonnay Pinot blend", price_tier="premium",
               description="Flagship NV Franciacorta from reserve wines averaging 2.5 years; white peach, citrus, brioche, chalk mineral and a fine, persistent perlage; Italy's most polished non-vintage sparkling wine.")
if n1:
    PAIR(pr1, "Risotto Milanese with saffron and bone marrow", "complement", "classic", "main", "Lombardy regional pairing; Franciacorta's mineral-brioche bridges saffron and marrow richness.")
    PAIR(pr1, "Vitello tonnato with capers and tuna sauce", "complement", "classic", "starter", "Northern Italian classic; sparkling acidity cuts tuna mayo richness; chalk bridges veal delicacy.")
    PAIR(pr1, "Burrata with prosciutto crudo and melon", "complement", "established", "starter", "Sparkling mineral-peach mirrors melon; fine bubbles cut prosciutto fat; bridges burrata cream.")
    PAIR(pr1, "Grilled scampi with garlic and olive oil", "complement", "established", "fish_course", "Lake-district tradition; mineral Franciacorta echoes scampi sweetness; citrus bridges.")
pr2, n2 = PROD("Bellavista Alma Franciacorta Brut", "wine_sparkling", p2, r, "Italy",
               subcategory="Chardonnay", price_tier="premium",
               description="Chardonnay-focused NV Franciacorta; floral, precise and mineral — apple blossom, lemon, almond biscuit and delicate chalk mineral; elegant aperitif and food companion.")
if n2:
    PAIR(pr2, "Carpaccio di polpo with capers and herbs", "complement", "established", "starter", "Almond mineral Franciacorta mirrors octopus delicacy; capers echo wine's salinity.")
    PAIR(pr2, "Lake Garda whitefish al cartoccio", "complement", "classic", "fish_course", "Lombardy lake tradition; Chardonnay-mineral Franciacorta suits delicate lake fish.")
    PAIR(pr2, "Saffron tagliolini with lobster and cherry tomatoes", "complement", "established", "main", "Lemon-mineral wine bridges saffron richness; lobster sweetness mirrors Chardonnay fruit.")
    PAIR(pr2, "Almond panna cotta with amarena cherries", "complement", "suggested", "dessert", "Almond biscuit note in wine echoes panna cotta; cherry brightness mirrors lemon acidity.")

# ── Region 2: Trentino Alto Adige ────────────────────────────────────────────
print("=== Region 2: Alto Adige ===")
r = R("Alto Adige", "Italy", "wine",
      designation_type="DOC", designation_name="Alto Adige DOC",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Italy's most northerly wine zone in the Alps; German-speaking South Tyrol; Pinot Grigio, Gewurztraminer, Lagrein and Pinot Nero from steep Alpine slopes; wines of extraordinary precision and depth.",
      key_producers="Elena Walch, Hofstätter, Tramin, Alois Lageder",
      historical_context="The region was Austrian until 1919; German names (Südtirol) still used alongside Italian; some of Italy's highest vineyards (1000m+) produce Riesling and Pinot Bianco of Alpine precision.")
VIN(r, 2022, "excellent", "rising", "Outstanding Alto Adige year; Pinot Bianco and Gewurztraminer of remarkable purity.")
VIN(r, 2021, "very_good", "stable", "Good alpine year; precise, food-friendly whites and elegant Lagrein.")
VIN(r, 2020, "excellent", "stable", "Warm year retained Alpine freshness; concentrated whites with depth.")
VIN(r, 2019, "exceptional", "rising", "Benchmark year; Gewurztraminer and Pinot Nero of extraordinary intensity.")
VIN(r, 2018, "very_good", "stable", "Good balance; versatile, food-friendly Alto Adige wines.")
p1 = P("Elena Walch", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Julia Walch's premium estate; Castel Ringberg and Kastelaz single-vineyard sites; Gewurztraminer Kastelaz is among Italy's most celebrated whites; biodynamic practices.",
       reputation_narrative="Elena Walch's Gewurztraminer Kastelaz is Italy's finest expression of the variety; the estate defines premium Alto Adige.",
       price_positioning="premium")
p2 = P("Hofstätter", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Martin Foradori Hofstätter's historic estate; Pinot Nero Barthenau Vigna S. Urbano from old vines on volcanic basalt; benchmark for Alto Adige's potential with Burgundian varieties.",
       reputation_narrative="Hofstätter's Barthenau Pinot Nero is one of Italy's greatest red wines; proves Alto Adige can match Burgundy for Pinot Nero complexity.",
       price_positioning="premium")
pr1, n1 = PROD("Elena Walch Gewurztraminer Kastelaz", "wine_still", p1, r, "Italy",
               subcategory="Gewurztraminer", price_tier="premium",
               description="Single-vineyard Kastelaz Gewurztraminer from hillside above Termeno; extraordinary — rose petal, lychee, saffron, ginger and a long, dry, spice-laden finish; Italy's most complex Gewurz.")
if n1:
    PAIR(pr1, "Foie gras au torchon with lychee jelly", "complement", "established", "starter", "Lychee in wine echoes jelly; rose petal and saffron mirror foie's richness; dry finish refreshes.")
    PAIR(pr1, "Mild yellow Thai curry with coconut milk", "complement", "established", "main", "Lychee and rose mirror curry aromatics; ginger bridges spice; dry finish prevents cloying.")
    PAIR(pr1, "Smoked duck breast with Asian pear salad", "complement", "established", "main", "Rose petal echoes pear's floral note; saffron bridges duck fat; ginger mirrors dressing spice.")
    PAIR(pr1, "Munster washed-rind cheese with caraway", "complement", "classic", "cheese", "Classic Alsatian-Alto Adige pairing; Gewurz's spice stands up to pungent Munster; caraway bridges.")
pr2, n2 = PROD("Hofstätter Barthenau Vigna S. Urbano Pinot Nero", "wine_still", p2, r, "Italy",
               subcategory="Pinot Nero", price_tier="premium",
               description="Old-vine Pinot Nero from volcanic soil above Mazon; extraordinary — red cherry, dried rose, earth, graphite and Burgundian precision; more complex than most premier cru; ages 15+ years.")
if n2:
    PAIR(pr2, "Coniglio arrosto con erbe (roast rabbit with herbs)", "complement", "established", "main", "Alpine tradition; light Pinot Nero suits rabbit's delicacy; earth echoes herbs.")
    PAIR(pr2, "Tagliatelle with hare ragù and black truffle", "complement", "established", "main", "Graphite-earth Pinot Nero bridges hare richness; truffle amplifies earthy register.")
    PAIR(pr2, "Venison carpaccio with juniper and lingonberry", "complement", "established", "starter", "Alpine game pairing; dried rose and cherry echo lingonberry; graphite mirrors venison.")
    PAIR(pr2, "Aged Asiago d'allevo with chestnut honey", "complement", "suggested", "cheese", "Burgundian-weight Pinot suits aged hard cheese; chestnut honey bridges dried fruit notes.")

# ── Region 3: Verdicchio dei Castelli di Jesi ────────────────────────────────
print("=== Region 3: Verdicchio dei Castelli di Jesi ===")
r = R("Verdicchio dei Castelli di Jesi", "Italy", "wine",
      designation_type="DOC", designation_name="Verdicchio dei Castelli di Jesi DOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Marche hillside DOC producing Italy's most underrated versatile white; Verdicchio grape delivers bitter almond, herbal freshness and extraordinary mineral salinity; great with seafood and fish.",
      key_producers="Bucci, Umani Ronchi, Garofoli, Sartarelli",
      historical_context="Verdicchio's amphora-shaped bottle was designed by the Fazi Battaglia winery in 1953; the waxy finish and bitter almond note are distinctive Verdicchio fingerprints.")
VIN(r, 2022, "excellent", "stable", "Good Marche year; Verdicchio of vibrant freshness and characteristic bitter almond.")
VIN(r, 2021, "very_good", "stable", "Balanced vintage; food-friendly Verdicchio of consistent quality.")
VIN(r, 2020, "excellent", "stable", "Warm year; concentrated Verdicchio with good acidity and aging potential.")
VIN(r, 2019, "exceptional", "rising", "Outstanding year; Verdicchio Riserva of extraordinary mineral depth.")
VIN(r, 2018, "very_good", "stable", "Classic profile; mineral, herbal Verdicchio.")
p1 = P("Bucci", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Ampelio Bucci's prestige estate; Villa Bucci Riserva is aged in large Slavonian oak — one of Italy's great overlooked white wines; minimal intervention; old vine selections.",
       reputation_narrative="Bucci's Villa Bucci Riserva is the benchmark for serious, age-worthy Verdicchio; demonstrates the variety's extraordinary longevity.",
       price_positioning="premium")
p2 = P("Sartarelli", "winery", r, "Italy",
       production_philosophy="sustainable",
       philosophy_description="Donatella Sartarelli's dedicated Verdicchio estate; Balciana (late harvest Verdicchio) from passerillage is their unique sweet expression; Tralivio is their prestige dry wine.",
       reputation_narrative="Sartarelli's Balciana proved Verdicchio could make exceptional sweet wine; Tralivio is one of the Jesi DOC's most consistent dry Verdicchio benchmarks.",
       price_positioning="mid_range")
pr1, n1 = PROD("Bucci Villa Bucci Verdicchio Riserva", "wine_still", p1, r, "Italy",
               subcategory="Verdicchio", price_tier="premium",
               description="Large oak-aged Verdicchio Riserva; toasted almond, beeswax, bitter herbs, chamomile and a long saline mineral finish; the most age-worthy dry Verdicchio, developing magnificently over 10+ years.")
if n1:
    PAIR(pr1, "Grilled branzino (sea bass) with fennel and capers", "complement", "classic", "fish_course", "Adriatic regional pairing; bitter almond and mineral mirror sea bass; capers amplify salinity.")
    PAIR(pr1, "Vincigrassi (Marche lasagne with chicken livers)", "complement", "classic", "main", "Regional Marche pairing; bitter almond bridges rich liver and pasta; beeswax suits cream.")
    PAIR(pr1, "Porchetta with fennel and rosemary", "complement", "established", "main", "Marche regional classic; bitter herbal Verdicchio cuts pork fat; fennel bridges herbal notes.")
    PAIR(pr1, "Aged Pecorino delle Marche with truffle honey", "complement", "suggested", "cheese", "Bitter almond and beeswax mirror aged Pecorino; truffle honey bridges mineral notes.")
pr2, n2 = PROD("Sartarelli Tralivio Verdicchio Classico Superiore", "wine_still", p2, r, "Italy",
               subcategory="Verdicchio", price_tier="mid_range",
               description="Prestige Classico Superiore Verdicchio from low-yield vines; green almond, bitter herb, citrus, chalk and a saline mineral finish; the definitive expression of the DOC's freshness and food versatility.")
if n2:
    PAIR(pr2, "Brodetto di pesce all'Anconetana (fish stew)", "complement", "classic", "main", "Adriatic classic; mineral-bitter Verdicchio echoes saffron-tomato fish broth; almond bridges.")
    PAIR(pr2, "Grilled Adriatic calamari with lemon", "complement", "classic", "starter", "Coastal pairing; mineral freshness amplifies squid's sea character; bitter almond bridges.")
    PAIR(pr2, "Strozzapreti with clams and bottarga", "complement", "established", "main", "Marche pasta classic; saline mineral Verdicchio bridges clam brine and bottarga intensity.")
    PAIR(pr2, "Salt-baked sea bream with herbs", "complement", "established", "fish_course", "Mineral-herbal Verdicchio suits sea bream; bitter almond echoes salt crust seasoning.")

# ── Region 4: Vernaccia di Oristano ─────────────────────────────────────────
print("=== Region 4: Vernaccia di Oristano ===")
r = R("Vernaccia di Oristano", "Italy", "wine",
      designation_type="DOC", designation_name="Vernaccia di Oristano DOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Sardinian oxidative white wine; flor-aged under veil of yeast similar to Sherry Fino; dry, nutty, complex — hazelnut, chamomile, dried herbs and sea breeze; Sardinia's most unique and ancient white.",
      key_producers="Silvio Carta, Fratelli Porcu, Contini",
      historical_context="Sardinia's oldest documented wine; ancient Roman writers praised Vernaccia di Oristano; flor-veil aging predates Spanish Fino; possibly the world's oldest surviving wine tradition.")
VIN(r, 2018, "excellent", "stable", "Good Oristano year; Vernaccia of fine oxidative complexity and flor character.")
VIN(r, 2016, "excellent", "stable", "Classic Vernaccia vintage; hazelnut and chamomile of fine balance.")
VIN(r, 2014, "very_good", "stable", "Good aging potential; Vernaccia developing elegantly.")
VIN(r, 2012, "exceptional", "stable", "Outstanding year; aged Vernaccia of extraordinary nutty complexity.")
VIN(r, 2010, "excellent", "stable", "Fine decade vintage; Vernaccia now fully developed and drinking magnificently.")
p1 = P("Contini", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Attilio Contini's historic estate; Vernaccia di Oristano Riserva aged minimum 6 years under flor; Antico Gregori (solera) is their extraordinary blended riserva.",
       reputation_narrative="Contini is the most internationally recognised Vernaccia di Oristano producer; Antico Gregori is one of Italy's most unusual and compelling fortified wines.",
       price_positioning="mid_range")
p2 = P("Silvio Carta", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Family estate producing traditional Vernaccia di Oristano under flor and aged in old chestnut barrels; wines of great complexity and accessibility at fair prices.",
       reputation_narrative="Silvio Carta is one of the most consistent producers of traditional flor-aged Vernaccia; benchmark for the appellation's classic style.",
       price_positioning="mid_range")
pr1, n1 = PROD("Contini Antico Gregori Vernaccia di Oristano", "wine_fortified", p1, r, "Italy",
               subcategory="Vernaccia", price_tier="premium",
               description="Extraordinary solera-system Vernaccia; hazelnut, dried chamomile, dried apricot, beeswax, sea breeze and an eternal finish; deeply complex, bone-dry and unlike anything else in Italy.")
if n1:
    PAIR(pr1, "Bottarga di muggine (grey mullet roe) with olive oil", "complement", "classic", "starter", "Sardinian regional classic; oxidative wine mirrors bottarga's salt-ocean intensity; hazelnut bridges.")
    PAIR(pr1, "Fried artichokes with anchovy dressing", "complement", "established", "starter", "Oxidative hazelnut Vernaccia suits bitter artichoke; anchovy bridges wine's saline depth.")
    PAIR(pr1, "Prawn and saffron risotto", "complement", "classic", "main", "Sardinian-coastal pairing; oxidative complexity bridges saffron and prawn sweetness.")
    PAIR(pr1, "Aged Pecorino Sardo with fava bean purée", "complement", "classic", "cheese", "Regional Sardinian pairing; oxidative wine mirrors aged sheep cheese; fava bridges vegetal notes.")
pr2, n2 = PROD("Silvio Carta Vernaccia di Oristano Riserva", "wine_fortified", p2, r, "Italy",
               subcategory="Vernaccia", price_tier="mid_range",
               description="Traditional 6-year flor-aged Vernaccia; dry, golden amber; toasted hazelnut, dried flowers, marine brine and a long, warming finish; Sardinia's answer to Fino Sherry.")
if n2:
    PAIR(pr2, "Maiorchino cheese with Sardinian bread (pane carasau)", "complement", "classic", "cheese", "Traditional Sardinian pairing; flor-aged wine and island cheese share oxidative affinity.")
    PAIR(pr2, "Grilled octopus with wild herb oil", "complement", "established", "main", "Sardinian coastal classic; oxidative marine wine mirrors octopus; herbs bridge.")
    PAIR(pr2, "Almonds, pistachios and dried figs aperitivo", "complement", "classic", "aperitif", "Hazelnut in wine echoes nuts; dried fig bridges wine's dried-fruit note; traditional island aperitif.")
    PAIR(pr2, "Tapas of jamón ibérico and olives", "complement", "adventurous", "aperitif", "Fino Sherry-like Vernaccia pairs beautifully with Iberian ham and olive; cross-cultural natural pairing.")

# ── Region 5: Nerello Mascalese heartland ────────────────────────────────────
print("=== Region 5: Faro ===")
r = R("Faro", "Italy", "wine",
      designation_type="DOC", designation_name="Faro DOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Sicily's smallest and most historic DOC, overlooking the Strait of Messina; Nerello Mascalese and Nocera blend; one of Italy's rarest wines; mineral, elegant and surprisingly age-worthy.",
      key_producers="Palari, Bonavita",
      historical_context="Faro DOC almost died out by 1990 with only 2 producers; Salvatore Geraci revived it with Palari in 1994; the wine that once rivalled Bordeaux is slowly reclaiming its status.")
VIN(r, 2021, "excellent", "rising", "Good Sicily year; Nerello of fine mineral character; elegant Faro of rare complexity.")
VIN(r, 2020, "very_good", "stable", "Warm year; concentrated Nerello-Nocera blend of Sicilian depth.")
VIN(r, 2019, "excellent", "stable", "Classic profile; structured Faro with mineral Messina Strait character.")
VIN(r, 2018, "exceptional", "rising", "Benchmark year; Palari Faro of extraordinary aging potential.")
VIN(r, 2017, "very_good", "stable", "Good balance; approachable Faro with genuine complexity.")
p1 = P("Palari", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Salvatore Geraci's iconic revival estate; single-estate Nerello Mascalese-Nocera-Nerello Cappuccio blend; hillside above Messina on ancient terraced vineyards.",
       reputation_narrative="Palari almost single-handedly resurrected Faro DOC; their Faro is considered one of Sicily's greatest red wines and one of Italy's most interesting.",
       price_positioning="premium")
p2 = P("Bonavita", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Giovanni Scarfone's small natural Faro estate; old-vine Nerello Mascalese on the hillsides above Messina; minimal intervention; indigenous yeasts; beautiful transparency and mineral energy.",
       reputation_narrative="Bonavita's natural Faro is a revelation — gossamer-light Nerello of great elegance that has attracted significant natural wine attention.",
       price_positioning="mid_range")
pr1, n1 = PROD("Palari Faro Rosso", "wine_still", p1, r, "Italy",
               subcategory="Nerello Mascalese", price_tier="premium",
               description="The iconic revival of Faro DOC; Nerello Mascalese-led blend from ancient terraced hillside; red cherry, dried rose, mineral-iron, wild herb and a long structured Sicilian finish; ages magnificently.")
if n1:
    PAIR(pr1, "Grilled swordfish with caponata", "complement", "classic", "main", "Sicilian regional classic; Nerello's light mineral body suits swordfish; caponata's sweet-sour bridges.")
    PAIR(pr1, "Braised rabbit all'agrodolce (sweet-sour)", "complement", "established", "main", "Sicilian tradition; mineral Nerello suits rabbit's delicacy; dried cherry and sweet-sour bridge.")
    PAIR(pr1, "Arancini with ragu and wild herbs", "complement", "classic", "starter", "Messina classic; wine's mineral-iron suit fried rice; herbs bridge the ragu filling.")
    PAIR(pr1, "Aged Caciocavallo Ragusano with honey", "complement", "suggested", "cheese", "Sicilian regional pairing; dried rose and iron echo aged Caciocavallo; honey bridges sweetness.")
pr2, n2 = PROD("Bonavita Faro Rosso", "wine_still", p2, r, "Italy",
               subcategory="Nerello Mascalese", price_tier="mid_range",
               description="Natural Nerello Mascalese Faro; transparent, gossamer-light; sour cherry, dried rose petal, sea spray and mineral-salt character; natural energy and fine grip — Burgundy-meets-Sicily.")
if n2:
    PAIR(pr2, "Grilled bluefin tuna with capers and lemon", "complement", "adventurous", "main", "Light natural red suits tuna steak; mineral-iron echoes ocean character; capers bridge salinity.")
    PAIR(pr2, "Pasta alla Norma with aubergine and ricotta salata", "complement", "classic", "main", "Sicilian classic; natural Nerello's acidity cuts tomato; dried rose bridges aubergine sweetness.")
    PAIR(pr2, "Grilled red mullet with fennel and wild herbs", "complement", "established", "fish_course", "Sicilian coastal pairing; gossamer Nerello suits red mullet's delicate flavour; herbs bridge.")
    PAIR(pr2, "Piacentinu Ennese saffron cheese", "complement", "suggested", "cheese", "Sicilian sheep's milk saffron cheese; wine's dried rose and mineral bridge unique cheese flavour.")

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
