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

# ── Region 1: Jurançon ────────────────────────────────────────────────────────
print("=== Region 1: Jurançon ===")
r = R("Jurançon", "France", "wine",
      designation_type="AOC", designation_name="Jurançon AOC",
      reputation_tier="prestigious", quality_trajectory="established",
      description="Pyrenean foothill appellation south of Pau; Petit Manseng and Gros Manseng produce France's most exotic dry and sweet whites; moelleux (sweet) rivals Sauternes in complexity.",
      key_producers="Domaine Cauhapé, Clos Uroulat, Domaine de Souch",
      historical_context="Henri IV of France was baptised with Jurançon wine dropped on his lips; 'this wine is fiery and imperious like a king' said Colette; Petit Manseng's late harvest produces remarkable concentration.")
VIN(r, 2022, "excellent", "rising", "Classic Jurançon year; Petit Manseng of great purity and exotic fruit intensity.")
VIN(r, 2021, "exceptional", "rising", "Benchmark vintage; Jurançon Moelleux of outstanding concentration and acidity.")
VIN(r, 2020, "very_good", "stable", "Warm year; concentrated dry Jurançon; late-harvest wines of great richness.")
VIN(r, 2019, "excellent", "stable", "Good balance; dry Jurançon of fine aromatic complexity.")
VIN(r, 2018, "excellent", "rising", "Classic Petit Manseng year; moelleux wines of textbook exotic-fruit concentration.")
p1 = P("Domaine Cauhapé", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Henri Ramonteu's pioneer estate; full range from dry Jurançon Sec to legendary Noblesse du Temps moelleux; biodynamic principles; Petit Manseng from old vines.",
       reputation_narrative="Cauhapé is Jurançon's defining estate; Noblesse du Temps is considered the appellation's greatest sweet wine.",
       price_positioning="mid_range")
p2 = P("Clos Uroulat", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Charles Hours's small natural estate; Marie (dry Jurançon) and Clos Uroulat (moelleux) from old-vine Petit Manseng; minimal intervention; certified organic.",
       reputation_narrative="Clos Uroulat is the cult natural wine of Jurançon; among France's greatest small-production sweet wines; long-aging potential.",
       price_positioning="mid_range")
pr1, n1 = PROD("Cauhapé Ballet d'Octobre Jurançon Moelleux", "wine_dessert", p1, r, "France",
               subcategory="Petit Manseng", price_tier="mid_range",
               description="Late-harvest Petit Manseng moelleux; extraordinary — mango, passion fruit, apricot, honey, ginger and a rapier acidity; rivalling great Sauternes in complexity and longevity.")
if n1:
    PAIR(pr1, "Foie gras au torchon with fig compote", "complement", "classic", "starter", "The great Southwestern pairing; sweet Jurançon acidity cuts foie richness; fig echoes wine's fruit.")
    PAIR(pr1, "Roquefort with toasted walnut bread", "complement", "established", "cheese", "Sweet-acidic Jurançon stands up to Roquefort; acidity cuts fungal pungency; honey bridges.")
    PAIR(pr1, "Crème brûlée with passion fruit", "complement", "established", "dessert", "Passion fruit in wine echoes the brûlée topping; acidity prevents over-sweetness.")
    PAIR(pr1, "Seared foie gras with ginger and mango", "complement", "classic", "starter", "Ginger and mango in wine echo accompaniments; sweet-acid balance matches foie richness.")
pr2, n2 = PROD("Clos Uroulat Jurançon Moelleux", "wine_dessert", p2, r, "France",
               subcategory="Petit Manseng", price_tier="premium",
               description="Natural Jurançon Moelleux from old-vine Petit Manseng; concentrated, tensile and singular — orange marmalade, candied ginger, saffron, beeswax and perpetual acidity; decades of life ahead.")
if n2:
    PAIR(pr2, "Époisses washed-rind cheese with walnut baguette", "complement", "adventurous", "cheese", "Sweet-acid Jurançon balances Époisses pungency; beeswax and orange echo washed rind.")
    PAIR(pr2, "Tarte tatin with crème fraîche and caramel", "complement", "suggested", "dessert", "Candied fruit and caramel in wine echo tarte tatin; acidity prevents cloying.")
    PAIR(pr2, "Tempura king prawns with mango chilli sauce", "bridge", "adventurous", "starter", "Mango in wine bridges mango sauce; acidity cuts prawn fat; ginger bridges chilli.")
    PAIR(pr2, "Bleu des Causses with dried figs and hazelnuts", "complement", "established", "cheese", "Acid-sweet wine stands up to blue cheese; dried figs echo wine's fruit; hazelnut bridges.")

# ── Region 2: Soave Classico ─────────────────────────────────────────────────
print("=== Region 2: Soave Classico ===")
r = R("Soave Classico", "Italy", "wine",
      designation_type="DOC", designation_name="Soave Classico DOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Volcanic and limestone hillside zone east of Verona; Garganega and Trebbiano di Soave produce Italy's most underrated dry whites; volcanic basalt gives wines a distinctive mineral-almond character.",
      key_producers="Pieropan, Gini, Coffele, Inama",
      historical_context="Soave became famous in the 1970s bulk era; the Classico zone was almost abandoned; a quality revolution led by Pieropan and Gini restored its reputation from the 1990s onward.")
VIN(r, 2022, "excellent", "rising", "Volcanic hillside year; precise Garganega of outstanding mineral definition.")
VIN(r, 2021, "very_good", "stable", "Good balance; aromatic Soave Classico with fine almond and citrus character.")
VIN(r, 2020, "excellent", "stable", "Warm year; concentrated Garganega with depth from low-yield old vines.")
VIN(r, 2019, "very_good", "stable", "Classic profile; food-friendly Soave Classico of consistent quality.")
VIN(r, 2018, "excellent", "stable", "Good minerality; Soave Classico of fine aging potential from top producers.")
p1 = P("Pieropan", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Nino Pieropan's iconic estate; La Rocca (volcanic tuff) and Calvarino (limestone) are single-vineyard benchmarks; Recioto di Soave from dried Garganega is their prized sweet wine.",
       reputation_narrative="Pieropan is the reference producer for serious Soave Classico; La Rocca and Calvarino proved the region's ageworthy potential when others had given up.",
       price_positioning="mid_range")
p2 = P("Gini", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Sandro and Claudio Gini's volcanic-hillside estate; La Froscà from 70-year-old Garganega; Contrada Salvarenza from pre-phylloxera vines — Italy's most ageworthy Soave.",
       reputation_narrative="Gini's Contrada Salvarenza is the Soave Classico cult wine; proves Garganega from centenarian vines can age 20+ years.",
       price_positioning="mid_range")
pr1, n1 = PROD("Pieropan La Rocca Soave Classico", "wine_still", p1, r, "Italy",
               subcategory="Garganega", price_tier="mid_range",
               description="Single-vineyard volcanic tuff Soave; Garganega of extraordinary mineral purity — white almond, chamomile, citrus, volcanic smoke and a long mineral finish; ages magnificently.")
if n1:
    PAIR(pr1, "Risotto all'Amarone con radicchio", "complement", "established", "main", "Verona regional pairing; mineral white suits radicchio bitterness; almond echoes Amarone's richness.")
    PAIR(pr1, "Linguine with clam sauce (vongole veraci)", "complement", "classic", "main", "Mineral almond Soave echoes clam brine; volcanic smoke bridges; acidity lifts the sauce.")
    PAIR(pr1, "Grilled lake perch from Lake Garda", "complement", "classic", "fish_course", "Veneto regional classic; mineral volcanic Soave mirrors delicate lake perch sweetness.")
    PAIR(pr1, "Monte Veronese cheese with local honey", "complement", "classic", "cheese", "Verona regional pairing; almond note echoes Monte Veronese; honey bridges wine's floral notes.")
pr2, n2 = PROD("Gini Contrada Salvarenza Soave Classico", "wine_still", p2, r, "Italy",
               subcategory="Garganega", price_tier="premium",
               description="Pre-phylloxera Garganega centenarian vines on volcanic basalt; extraordinary depth — bitter almond, beeswax, saffron, volcanic mineral and a finish that lasts for minutes; ages 20+ years.")
if n2:
    PAIR(pr2, "Turbot with leek cream and black truffle", "elevate", "established", "fish_course", "Ancient Garganega elevates turbot's delicacy; saffron mirrors truffle; almond bridges leek.")
    PAIR(pr2, "Asiago d'allevo stagionato with mostarda", "complement", "classic", "cheese", "Venetian regional pairing; beeswax-almond wine echoes aged Asiago; mostarda bridges.")
    PAIR(pr2, "White asparagus from Bassano with prosciutto", "complement", "classic", "starter", "Veneto spring classic; almond and saffron echo asparagus; wine's texture suits prosciutto.")
    PAIR(pr2, "Baccalà mantecato (Venetian salt cod mousse)", "complement", "established", "starter", "Mineral-saline wine echoes salt cod; almond bridges whipped richness; acidity refreshes.")

# ── Region 3: Lugana ─────────────────────────────────────────────────────────
print("=== Region 3: Lugana ===")
r = R("Lugana", "Italy", "wine",
      designation_type="DOC", designation_name="Lugana DOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Lake Garda's southern shore; Turbiana (Trebbiano di Lugana) produces Italy's most mineral and food-versatile dry white; clay and limestone soils; wines of texture, freshness and surprising longevity.",
      key_producers="Zenato, Ca' dei Frati, Cà Maiol, Pasini",
      historical_context="Lugana was one of Italy's first officially recognised DOCs (1967); Turbiana is an ancient indigenous variety; the lake's thermal influence creates unique growing conditions.")
VIN(r, 2023, "excellent", "rising", "Ideal Garda year; Turbiana of remarkable freshness and mineral definition.")
VIN(r, 2022, "very_good", "stable", "Warm year; rounder Lugana with tropical notes; good body.")
VIN(r, 2021, "excellent", "stable", "Classic profile; textbook mineral-almond Lugana with food-friendly acidity.")
VIN(r, 2020, "excellent", "stable", "Outstanding Lugana year; concentrated Turbiana with aging potential.")
VIN(r, 2019, "very_good", "stable", "Good balance; versatile, accessible Lugana.")
p1 = P("Ca' dei Frati", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Dal Cero family's benchmark Lugana estate; I Frati is their classic Turbiana; Brolettino (single vineyard) and Tre Filer (barrel-aged) demonstrate Lugana's range.",
       reputation_narrative="Ca' dei Frati is Lugana's most celebrated name; I Frati set the template for the appellation's mineral-almond style worldwide.",
       price_positioning="mid_range")
p2 = P("Zenato", "winery", r, "Italy",
       production_philosophy="sustainable",
       philosophy_description="Sergio Zenato's estate pioneering Lugana alongside Amarone; Sergio Zenato Reserve Lugana from old-vine Turbiana shows the variety's complexity and longevity.",
       reputation_narrative="Zenato put Lugana on the international map; their Riserva Sergio Zenato is a benchmark for aged Turbiana.",
       price_positioning="mid_range")
pr1, n1 = PROD("Ca' dei Frati I Frati Lugana", "wine_still", p1, r, "Italy",
               subcategory="Turbiana", price_tier="mid_range",
               description="Benchmark Lugana DOC; Turbiana from clay-limestone; white almond, citrus blossom, grapefruit and a mineral freshness that belies its complexity; the model for the appellation.")
if n1:
    PAIR(pr1, "Grilled lake whitefish with lemon and capers", "complement", "classic", "fish_course", "Lake Garda regional classic; mineral almond Lugana mirrors delicate lake fish perfectly.")
    PAIR(pr1, "Risotto al pesce persico (perch risotto)", "complement", "classic", "main", "Lago di Garda tradition; Turbiana's almond and citrus bridge delicate perch and rice.")
    PAIR(pr1, "Pasta al salmone affumicato e crème fraîche", "complement", "established", "main", "White almond and citrus cut smoked salmon richness; Turbiana texture suits cream.")
    PAIR(pr1, "Burrata with heirloom tomatoes and basil", "complement", "suggested", "starter", "Citrus blossom note echoes fresh basil; mineral acidity bridges tomato's acidity; almond suits cream.")
pr2, n2 = PROD("Zenato Riserva Sergio Zenato Lugana", "wine_still", p2, r, "Italy",
               subcategory="Turbiana", price_tier="mid_range",
               description="Aged Reserve Lugana from oldest Turbiana vines; hazelnut, beeswax, lemon curd, white truffle and remarkable longevity; demonstrates that Turbiana ages as well as great white Burgundy.")
if n2:
    PAIR(pr2, "Butter-poached lobster with truffle cream", "elevate", "established", "fish_course", "Reserve Lugana elevates lobster; white truffle note echoes truffle cream; beeswax bridges.")
    PAIR(pr2, "Veal saltimbocca alla Romana", "complement", "established", "main", "Hazelnut and lemon echo prosciutto and sage; mineral acidity refreshes veal richness.")
    PAIR(pr2, "Aged Grana Padano with aged balsamic", "complement", "classic", "cheese", "Beeswax-hazelnut Reserve mirrors nutty Grana; balsamic bridges wine's citrus acidity.")
    PAIR(pr2, "Sea bass carpaccio with truffle and citrus", "complement", "established", "starter", "White truffle in wine echoes truffle garnish; citrus amplifies sea bass delicacy.")

# ── Region 4: Prosecco DOCG ──────────────────────────────────────────────────
print("=== Region 4: Prosecco Superiore ===")
r = R("Conegliano Valdobbiadene Prosecco Superiore", "Italy", "wine",
      designation_type="DOCG", designation_name="Conegliano Valdobbiadene Prosecco Superiore DOCG",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="UNESCO World Heritage hillside Prosecco zone in the Veneto foothills; Glera grape produces the finest Prosecco — Rive (single-village) and Cartizze (grand cru hill) expressions of real complexity.",
      key_producers="Bisol, Nino Franco, Carpené Malvolti, Col Vetoraz",
      historical_context="Valdobbiadene has produced sparkling wine since the 1860s; Cartizze is a 107-hectare hill producing Italy's most sought-after Prosecco; UNESCO inscription 2019.")
VIN(r, 2023, "excellent", "stable", "Classic Veneto year; Glera of fine floral aromatics and clean acidity.")
VIN(r, 2022, "very_good", "stable", "Warm year; richer Prosecco style with more body and peach character.")
VIN(r, 2021, "excellent", "stable", "Cool year; elegant, precise Glera with apple and citrus blossom.")
VIN(r, 2020, "very_good", "stable", "Good balance; food-friendly Prosecco DOCG of consistent quality.")
VIN(r, 2019, "excellent", "rising", "Outstanding year for DOCG; Cartizze and Rive bottlings of real depth.")
p1 = P("Bisol", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Historic Valdobbiadene family estate; Jeio Brut, Crede DOCG and Cartizze are their range; multi-vineyard selections from steep hillside sites; benchmark for structured Prosecco.",
       reputation_narrative="Bisol is among Valdobbiadene's most prestigious estates; Crede is the definitive expression of the DOCG's hillside terroir.",
       price_positioning="mid_range")
p2 = P("Nino Franco", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Primo Franco's family house; Rustico is their classic NV Prosecco; Grave di Stecca is their prestige single-vineyard; Cartizze from the grand cru hill is their most celebrated wine.",
       reputation_narrative="Nino Franco's Rustico introduced Prosecco to international audiences; their Cartizze remains a benchmark for the style.",
       price_positioning="mid_range")
pr1, n1 = PROD("Bisol Crede Valdobbiadene Prosecco Superiore Brut", "wine_sparkling", p1, r, "Italy",
               subcategory="Glera", price_tier="mid_range",
               description="Hillside DOCG Prosecco Brut; white peach, apple blossom, pear and a creamy, fine perlage; mineral freshness from clay-chalky soils; far more complex than DOC Prosecco.")
if n1:
    PAIR(pr1, "Prosciutto di San Daniele with melon and rocket", "complement", "classic", "aperitif", "Classic Venetian aperitif; Prosecco's peach and apple mirror melon; fine bubbles cut prosciutto fat.")
    PAIR(pr1, "Sarde in saor (sweet-sour sardines)", "complement", "classic", "starter", "Venetian classic; Prosecco's sweetness mirrors raisin-onion saor; fine bubbles refresh oily fish.")
    PAIR(pr1, "Cicchetti assortment (Venetian bar snacks)", "complement", "classic", "aperitif", "Quintessential Venice pairing; Prosecco DOCG is the mandatory wine for cicchetti culture.")
    PAIR(pr1, "Light seafood pasta with cherry tomatoes and basil", "complement", "established", "main", "Apple blossom and fine bubbles suit delicate seafood pasta; acidity mirrors tomato.")
pr2, n2 = PROD("Nino Franco Cartizze Valdobbiadene Superiore di Cartizze", "wine_sparkling", p2, r, "Italy",
               subcategory="Glera", price_tier="premium",
               description="Grand cru Cartizze Prosecco; off-dry; extraordinary peach, apricot, jasmine and almond; fine, persistent perlage; the pinnacle of Prosecco production — complex, rich and unique.")
if n2:
    PAIR(pr2, "Fragoline di bosco (wild strawberries) with mascarpone", "complement", "classic", "dessert", "Traditional Venetian dessert pairing; off-dry Cartizze echoes wild berry sweetness; jasmine bridges.")
    PAIR(pr2, "Tiramisu with Savoiardi and espresso", "complement", "classic", "dessert", "Venetian classic dessert; almond and peach of Cartizze bridge mascarpone and coffee.")
    PAIR(pr2, "Mozzarella di bufala with Parma ham and figs", "complement", "established", "starter", "Off-dry apricot bridges fresh mozzarella; jasmine notes echo fig sweetness; bubbles refresh.")
    PAIR(pr2, "Lobster bisque with cream and cognac", "complement", "adventurous", "starter", "Off-dry Cartizze's peach and richness bridge luxurious bisque; fine bubbles cut cream.")

# ── Region 5: MILESTONE — Champagne NV ───────────────────────────────────────
print("=== Region 5: Champagne (NV milestone) ===")
r = R("Champagne", "France", "wine",
      designation_type="AOC", designation_name="Champagne AOC",
      reputation_tier="iconic", quality_trajectory="established",
      description="The world's most celebrated sparkling wine appellation northeast of Paris; chalk soils and cool climate; Chardonnay, Pinot Noir and Pinot Meunier blended across houses; NV cuvées and prestige bottlings.",
      key_producers="Krug, Salon, Billecart-Salmon, Gosset, Jacques Selosse",
      historical_context="Dom Pérignon (1638-1715) perfected the second fermentation in bottle method; Champagne became the wine of celebration, coronations and the belle époque; the world's most copied wine style.")
VIN(r, 2019, "exceptional", "rising", "One of the greatest Champagne harvests in a generation; Blanc de Blancs of rare purity.")
VIN(r, 2018, "excellent", "rising", "Rich, structured vintage; Pinot Noir-dominant blends of great depth and aging potential.")
VIN(r, 2015, "exceptional", "rising", "Iconic vintage; wines of extraordinary concentration, balance and decades of life ahead.")
VIN(r, 2013, "excellent", "stable", "Classic cool year; precise, mineral Champagne of fine aging potential.")
VIN(r, 2012, "exceptional", "rising", "Benchmark decade vintage; NVs blended around 2012 show outstanding complexity.")
p1 = P("Billecart-Salmon", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Family-owned grande maison since 1818; renowned for precision and finesse over power; Nicolas-François Billecart Blanc de Blancs and Cuvée Nicolas-François Billecart are their prestige wines.",
       reputation_narrative="Billecart-Salmon's Blanc de Blancs is considered one of France's great Champagnes; the most refined and elegant of the major houses.",
       price_positioning="premium")
p2 = P("Gosset", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The oldest wine house in Champagne (1584); no malolactic fermentation for freshness and aging potential; Grand Blanc de Blancs and Célébris Rosé are their pinnacle wines.",
       reputation_narrative="Gosset's no-malo philosophy creates Champagnes of remarkable tension and longevity; among the most age-worthy of the non-vintage style.",
       price_positioning="premium")
pr1, n1 = PROD("Billecart-Salmon Blanc de Blancs Grand Cru Champagne", "wine_sparkling", p1, r, "France",
               subcategory="Chardonnay", price_tier="premium",
               description="100% Grand Cru Chardonnay from Avize, Oger and Le Mesnil; extraordinary chalk mineral, lemon, brioche and white flower; fine bead and decades of aging potential.")
if n1:
    PAIR(pr1, "Oysters from Brittany with seaweed butter", "complement", "classic", "aperitif", "The definitive Blanc de Blancs pairing; chalk mineral echoes oyster brine; seaweed amplifies.")
    PAIR(pr1, "Truffled scrambled eggs on brioche", "complement", "classic", "starter", "Brioche note in wine echoes toast; chalk mineral bridges egg richness; truffle elevates.")
    PAIR(pr1, "Lobster thermidor with tarragon", "complement", "classic", "fish_course", "Classic Champagne and lobster; chalk mineral and acidity cut thermidor richness; citrus bridges.")
    PAIR(pr1, "Aged Comté 48 months with truffle oil", "complement", "established", "cheese", "Chalk mineral bridges aged Comté's nutty depth; white flower echoes truffle's earthiness.")
pr2, n2 = PROD("Gosset Grande Réserve Brut Champagne", "wine_sparkling", p2, r, "France",
               subcategory="Chardonnay Pinot blend", price_tier="premium",
               description="No-malolactic NV blend of all three varieties; extraordinary tension — red berry, citrus, brioche, almond and a prolonged chalk-mineral finish; more wine-like than any other NV Champagne.")
if n2:
    PAIR(pr2, "Seared foie gras with Champagne reduction", "complement", "classic", "starter", "No-malo tension cuts foie richness; red berry notes and chalk mineral elevate the reduction.")
    PAIR(pr2, "Chicken Kiev with herb butter", "complement", "established", "main", "Red berry and brioche Champagne suits butter-filled chicken; acidity cuts through richness.")
    PAIR(pr2, "Smoked salmon with blinis and crème fraîche", "complement", "classic", "starter", "Iconic Champagne pairing; tension and red berry bridge smoked salmon; brioche suits blinis.")
    PAIR(pr2, "Strawberry mille-feuille with vanilla cream", "complement", "suggested", "dessert", "Red berry notes echo strawberry; no-malo acidity prevents over-sweetness; brioche bridges pastry.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
total_regions = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_producers")
total_producers = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_products")
total_products = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
total_pairings = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
total_vintages = cur.fetchone()[0]
print(f"Total regions: {total_regions}")
print(f"Total producers: {total_producers}")
print(f"Total products: {total_products}")
print(f"Total pairings: {total_pairings}")
print(f"Total vintages: {total_vintages}")
if total_regions >= 500:
    print(f"*** MILESTONE: {total_regions} REGIONS — 500+ ACHIEVED! ***")
print("Done. B100 complete.")
conn.close()
