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

# ── Region 1: Agiorgitiko heartland — Nemea ──────────────────────────────────
print("=== Region 1: Nemea ===")
r = R("Nemea", "Greece", "wine",
      designation_type="PDO", designation_name="Nemea PDO",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Peloponnese highland appellation; Agiorgitiko (St. George) grape produces Greece's most food-friendly red — from light rosé to concentrated, age-worthy reds; great velvety tannins.",
      key_producers="Gaia Estate, Domaine Skouras, Palivou Estate, Semeli",
      historical_context="Ancient Nemea was home to the Nemean Games (forerunner of the Olympics) and Heracles's first labor; Agiorgitiko has been cultivated here since antiquity.")
VIN(r, 2021, "excellent", "rising", "Outstanding cool year; Agiorgitiko of Burgundian precision and fine tannins.")
VIN(r, 2020, "very_good", "stable", "Good balance; plush, generous Nemea reds with characteristic velvet.")
VIN(r, 2019, "excellent", "stable", "Classic Peloponnese year; structured, age-worthy Nemea reds.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; accessible, fruit-forward Agiorgitiko.")
VIN(r, 2017, "excellent", "stable", "Good balance; food-friendly Nemea reds of consistent quality.")
p1 = P("Gaia Estate", "winery", r, "Greece",
       production_philosophy="terroir_focused",
       philosophy_description="Yiannis Paraskevopoulos and Leon Karatsalos; Estate Nemea from high-altitude (600m) old-vine Agiorgitiko on red clay; also Thalassitis Santorini; benchmark for both appellations.",
       reputation_narrative="Gaia's Estate Nemea is the benchmark for high-altitude, serious Agiorgitiko; consistently demonstrates Greece's finest red wine potential.",
       price_positioning="premium")
p2 = P("Domaine Skouras", "winery", r, "Greece",
       production_philosophy="sustainable",
       philosophy_description="George Skouras's modern estate; Grande Cuvée (Agiorgitiko-Cabernet) and Megas Oenos (international blend) alongside pure Nemea; certified sustainable; precise winemaking.",
       reputation_narrative="Skouras helped define modern Greek red wine; Grande Cuvée is one of Greece's most internationally recognised reds.",
       price_positioning="mid_range")
pr1, n1 = PROD("Gaia Estate Nemea Agiorgitiko", "wine_still", p1, r, "Greece",
               subcategory="Agiorgitiko", price_tier="premium",
               description="High-altitude old-vine Nemea; red cherry, dried herbs, black olive, violet and velvety tannins with remarkable structure; one of Greece's truly great reds, aging 10+ years.")
if n1:
    PAIR(pr1, "Slow-roasted lamb shoulder with herbs and lemon", "complement", "classic", "main", "Greece's defining pairing; Agiorgitiko velvet suits slow-roasted lamb; herbs bridge.")
    PAIR(pr1, "Moussaka with cinnamon and béchamel", "complement", "classic", "main", "Definitive Greek pairing; cherry and herb notes echo cinnamon spice; velvet suits béchamel.")
    PAIR(pr1, "Grilled lamb liver with onions and paprika", "complement", "established", "main", "Velvet Agiorgitiko suits liver's richness; red cherry contrasts iron; herbs bridge.")
    PAIR(pr1, "Aged Kefalotiri cheese with quince paste", "complement", "established", "cheese", "Greek regional pairing; velvety tannins soften aged hard cheese; quince echoes red fruit.")
pr2, n2 = PROD("Skouras Megas Oenos Grande Cuvée", "wine_still", p2, r, "Greece",
               subcategory="Agiorgitiko Cabernet", price_tier="mid_range",
               description="Agiorgitiko and Cabernet Sauvignon blend; velvet Agiorgitiko tannins meet Cabernet structure — dark cherry, cassis, dried herbs, cedar and a long Greek-international finish.")
if n2:
    PAIR(pr2, "Grilled lamb chops with tzatziki", "complement", "classic", "main", "Greek classic; Cabernet structure grips lamb fat; Agiorgitiko velvet suits herb yoghurt.")
    PAIR(pr2, "Beef stifado with pearl onions and spices", "complement", "established", "main", "Greek braised classic; cassis and dark cherry echo slow-cooked beef; cinnamon bridges wine's spice.")
    PAIR(pr2, "Spanakopita (spinach and feta pie)", "complement", "suggested", "starter", "Cedar and herb notes echo spinach and herb filling; Cabernet tannins grip feta richness.")
    PAIR(pr2, "Grilled halloumi with roasted cherry tomatoes", "complement", "established", "starter", "Velvet Agiorgitiko suits grilled cheese; cherry tomato echoes wine's fruit; herbs bridge.")

# ── Region 2: Assyrtiko beyond Santorini — Drama ─────────────────────────────
print("=== Region 2: Drama ===")
r = R("Drama", "Greece", "wine",
      designation_type="PGI", designation_name="Drama PGI",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Northern Greek PGI in Macedonia; Cabernet Sauvignon, Merlot, Syrah and indigenous varieties at altitude; cool continental climate produces Greece's most structured and age-worthy reds.",
      key_producers="Pavlidis Estate, Lazaridi Estate, Nico Lazaridi",
      historical_context="Drama began as a destination for investors attracted by its cooler climate; international varieties planted alongside Agiorgitiko produce Greece's most Bordeaux-like reds.")
VIN(r, 2021, "excellent", "rising", "Cool Drama year; structured Cabernet-based reds of fine precision.")
VIN(r, 2020, "very_good", "stable", "Good balance; Syrah and Merlot excelled; concentrated but fresh.")
VIN(r, 2019, "excellent", "stable", "Classic year; Drama reds of consistent structure and food affinity.")
VIN(r, 2018, "exceptional", "rising", "Benchmark Drama vintage; international varieties of great depth and aging potential.")
VIN(r, 2017, "very_good", "stable", "Good balance; accessible Drama reds with characteristic northern freshness.")
p1 = P("Pavlidis Estate", "winery", r, "Greece",
       production_philosophy="terroir_focused",
       philosophy_description="Thymiopoulos and Pavlidis estates collaborate; Drama-altitude Cabernet, Merlot and Syrah from red clay soils; Emphasis red is their prestige blend of Greek-international character.",
       reputation_narrative="Pavlidis is Drama's most internationally celebrated producer; Emphasis is considered one of Greece's great red wine blends.",
       price_positioning="mid_range")
p2 = P("Nico Lazaridi", "winery", r, "Greece",
       production_philosophy="sustainable",
       philosophy_description="Drama estate with Bordeaux-inspired winery; Magico Vouno and Château Nico Lazaridi are their prestige reds; Assyrtiko and Semillon whites also produced.",
       reputation_narrative="Nico Lazaridi established Drama's reputation for Bordeaux-variety reds; Château Nico Lazaridi is the denomination's most elegant expression.",
       price_positioning="mid_range")
pr1, n1 = PROD("Pavlidis Emphasis Drama Red", "wine_still", p1, r, "Greece",
               subcategory="Cabernet Merlot Syrah", price_tier="mid_range",
               description="Premium Drama blend of Cabernet Sauvignon, Merlot and Syrah; dark plum, cedar, tobacco, Mediterranean herbs and firm but polished tannins; one of Greece's most structured reds.")
if n1:
    PAIR(pr1, "Kleftiko (slow-baked lamb in parchment)", "complement", "classic", "main", "Northern Greek classic; structured Drama red suits slow-baked lamb's richness.")
    PAIR(pr1, "Grilled beef souvlaki with Greek salad", "complement", "established", "main", "Cabernet structure grips beef; Mediterranean herbs bridge; tomato-feta acidity suits wine's tannins.")
    PAIR(pr1, "Braised wild boar with wine and spices", "complement", "established", "main", "Game tannin alignment; Syrah's dark fruit bridges boar richness; cedar echoes wine reduction.")
    PAIR(pr1, "Aged Kasseri cheese with fig preserve", "complement", "suggested", "cheese", "Structured Drama red suits aged Greek cheese; fig echoes plum fruit; cedar bridges.")
pr2, n2 = PROD("Château Nico Lazaridi Drama Red", "wine_still", p2, r, "Greece",
               subcategory="Cabernet Merlot", price_tier="mid_range",
               description="Bordeaux-inspired Drama blend; Cabernet Sauvignon and Merlot from altitude; blackcurrant, tobacco, graphite and a long Greek-mineral finish; the most refined and elegant Drama red.")
if n2:
    PAIR(pr2, "Rack of lamb with Dijon and herb crust", "complement", "established", "main", "Cabernet cassis and graphite suit lamb; herb crust bridges; Dijon amplifies tannin structure.")
    PAIR(pr2, "Pan-roasted venison with bilberry sauce", "complement", "established", "main", "Graphite-mineral red suits venison's lean richness; bilberry echoes cassis notes.")
    PAIR(pr2, "Beef fillet with green peppercorn sauce", "complement", "classic", "main", "Classic Cabernet pairing; fine tannins grip beef; green pepper bridges wine's tobacco note.")
    PAIR(pr2, "Graviera cheese aged in wax with olives", "complement", "suggested", "cheese", "Refined Drama red suits aged Graviera; cassis bridges; olives add Mediterranean character.")

# ── Region 3: Vin Jaune special — Château-Chalon ─────────────────────────────
print("=== Region 3: Château-Chalon ===")
r = R("Château-Chalon", "France", "wine",
      designation_type="AOC", designation_name="Château-Chalon AOC",
      reputation_tier="iconic", quality_trajectory="established",
      description="Jura's most prestigious single wine appellation; only 50 hectares; Savagnin aged under flor for 6 years and 3 months without topping up; the original and greatest Vin Jaune; walnut, curry and infinite length.",
      key_producers="Domaine Berthet-Bondet, Macle, Domaine des Carlines",
      historical_context="The flor yeast (voile) that forms in barrel prevents oxidation while allowing slow evaporation; the famous 62cl clavelin bottle represents what remains from 1 litre after aging; Château-Chalon declared non-existent some years.")
VIN(r, 2019, "exceptional", "rising", "Château-Chalon declared; Vin Jaune of extraordinary concentration and complexity.")
VIN(r, 2016, "excellent", "rising", "Declared vintage; wines of great depth and characteristic walnut-curry profile.")
VIN(r, 2015, "exceptional", "rising", "Benchmark decade; Vin Jaune of rare elegance and aging potential.")
VIN(r, 2014, "very_good", "stable", "Declared; accessible Vin Jaune style with classic flor character.")
VIN(r, 2011, "exceptional", "rising", "Iconic decade vintage; Château-Chalon wines now showing extraordinary development.")
p1 = P("Macle", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Jean and Laurent Macle's benchmark estate; the most celebrated Château-Chalon producer; traditional cellar and extended aging under voile; wines of extraordinary concentration.",
       reputation_narrative="Macle's Château-Chalon is considered the reference Vin Jaune; the most sought-after wine in the appellation and among France's most singular whites.",
       price_positioning="premium")
p2 = P("Domaine Berthet-Bondet", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Jean Berthet-Bondet's biodynamic estate; Château-Chalon and l'Étoile from Savagnin; traditional voile aging; oldest vines in the appellation.",
       reputation_narrative="Berthet-Bondet produces some of the appellation's most complex Château-Chalon; biodynamic practices and old vines create wines of extraordinary aromatic depth.",
       price_positioning="premium")
pr1, n1 = PROD("Macle Château-Chalon Vin Jaune", "wine_still", p1, r, "France",
               subcategory="Savagnin", price_tier="premium",
               description="The benchmark Vin Jaune; 6 years 3 months under voile; walnuts, roasted hazelnuts, curry leaf, dried chamomile, orange rind and a finish that lasts for minutes; needs 10+ years to open.")
if n1:
    PAIR(pr1, "Comté aged 48 months with roasted walnut bread", "complement", "classic", "cheese", "The supreme Jura pairing; oxidative wine and aged Comté are mirror images of each other.")
    PAIR(pr1, "Poularde de Bresse aux morilles (morel cream chicken)", "complement", "classic", "main", "The classic pairing; Vin Jaune's weight matches morel cream; walnut note echoes sauce.")
    PAIR(pr1, "Langoustines with bisque reduction and curry leaf", "complement", "established", "fish_course", "Curry leaf in wine mirrors garnish; oxidative weight suits rich bisque; walnut bridges.")
    PAIR(pr1, "Japanese miso-glazed black cod", "bridge", "adventurous", "fish_course", "Walnut-curry Vin Jaune bridges miso's fermented depth; both share oxidative umami character.")
pr2, n2 = PROD("Berthet-Bondet Château-Chalon Vin Jaune", "wine_still", p2, r, "France",
               subcategory="Savagnin", price_tier="premium",
               description="Biodynamic old-vine Château-Chalon; deeper and more floral than Macle — jasmine, walnut, saffron, dried apricot and extraordinary mineral-oxidative finish; ages 30+ years.")
if n2:
    PAIR(pr2, "Gratin de queues d'écrevisses (crayfish gratin)", "complement", "classic", "main", "Classic Jura recipe; wine's walnut-saffron complex lifts crustacean gratin; cream bridges.")
    PAIR(pr2, "Roast pheasant with cream and Savagnin sauce", "complement", "classic", "main", "Jura game classic; Vin Jaune IS the sauce; walnut and cream bridge pheasant richness.")
    PAIR(pr2, "Mushroom and egg cocotte with aged Comté", "complement", "established", "starter", "Walnut-floral Vin Jaune bridges egg and mushroom; Comté echoes wine's oxidative character.")
    PAIR(pr2, "Époisses cheese at room temperature", "complement", "adventurous", "cheese", "The bravest Jura pairing; powerful Vin Jaune stands up to Époisses; both are extreme.")

# ── Region 4: Muscadet ────────────────────────────────────────────────────────
print("=== Region 4: Muscadet ===")
r = R("Muscadet", "France", "wine",
      designation_type="AOC", designation_name="Muscadet AOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Loire estuary appellation at the Atlantic mouth; Melon de Bourgogne grape produces France's most seafood-versatile dry white; muscular sur lie aging creates brioche and saline complexity.",
      key_producers="Domaine de la Pépière, Luneau-Papin, Domaine de l'Écu, Guy Bossard",
      historical_context="Muscadet was France's most fashionable wine in the 1970s-80s; over-production ruined its reputation; a quality revival led by sur lie specialists has restored its credibility.")
VIN(r, 2022, "excellent", "rising", "Outstanding Atlantic year; Muscadet of remarkable mineral precision and sur lie depth.")
VIN(r, 2021, "exceptional", "rising", "Benchmark vintage; finest Muscadet in a generation; Grand Cru crus will age decades.")
VIN(r, 2020, "very_good", "stable", "Good balance; mineral, food-friendly Muscadet with classic saline finish.")
VIN(r, 2019, "excellent", "stable", "Classic profile; textbook mineral Melon with fine sur lie character.")
VIN(r, 2018, "very_good", "stable", "Good year; reliable Muscadet of consistent mineral-saline quality.")
p1 = P("Domaine de la Pépière", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Marc Ollivier's benchmark natural Muscadet estate; certified biodynamic; Clos des Briords is their prestige single-vineyard; Clisson (Grand Cru Communal) ages up to 10 years.")
p1_ret = p1
p1 = P("Domaine de la Pépière", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Marc Ollivier's benchmark natural Muscadet estate; certified biodynamic; Clos des Briords is their prestige single-vineyard; Clisson (Grand Cru Communal) ages up to 10 years.",
       reputation_narrative="La Pépière is the most celebrated natural Muscadet producer; their Clos des Briords and Clisson are among France's most compelling natural whites.",
       price_positioning="mid_range")
p2 = P("Luneau-Papin", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Pierre-Marie Luneau's precise Muscadet estate; extended sur lie aging across multiple cuvées; L (Expression de L'Orthogneiss) is their prestige orthogneiss-terroir wine.",
       reputation_narrative="Luneau-Papin's L is the definitive expression of Muscadet's terroir; extended sur lie aging reveals the Melon grape's complexity.",
       price_positioning="mid_range")
pr1, n1 = PROD("Domaine de la Pépière Muscadet Clisson", "wine_still", p1, r, "France",
               subcategory="Melon de Bourgogne", price_tier="mid_range",
               description="Grand Cru Communal Muscadet from gneiss soils; extended sur lie; extraordinary — brioche, lemon curd, chalk mineral and saline length; ages 5-10 years; proves Muscadet is a serious wine.")
if n1:
    PAIR(pr1, "Oysters from Brittany with seaweed and lemon", "complement", "classic", "aperitif", "The definitive Muscadet pairing; mineral salinity mirrors oyster brine; sur lie brioche bridges.")
    PAIR(pr1, "Moules marinières with white wine and herbs", "complement", "classic", "starter", "Loire estuary classic; saline Muscadet mirrors mussel brine; herbs and sur lie suit the sauce.")
    PAIR(pr1, "Langoustines with mayonnaise and lemon", "complement", "established", "starter", "Grand Cru Muscadet elevates langoustine sweetness; brioche bridges mayo richness; chalk mineral amplifies.")
    PAIR(pr1, "Fish and chips with malt vinegar", "contrast", "adventurous", "main", "Mineral Muscadet contrasts English seaside tradition; both share Atlantic provenance.")
pr2, n2 = PROD("Luneau-Papin L d'Or Muscadet", "wine_still", p2, r, "France",
               subcategory="Melon de Bourgogne", price_tier="mid_range",
               description="Extended sur lie orthogneiss Muscadet; chalk, lemon oil, toasted brioche and a persistent saline mineral finish; more complex and age-worthy than standard Muscadet; genuinely impressive.")
if n2:
    PAIR(pr2, "Razor clams with parsley and garlic butter", "complement", "classic", "starter", "Atlantic mineral mirrors razor clam brine; parsley echoes sur lie herbal note; butter bridges.")
    PAIR(pr2, "Salt-baked sea bream with fennel", "complement", "established", "fish_course", "Mineral-chalk Muscadet suits delicate sea bream; fennel bridges wine's herbal freshness.")
    PAIR(pr2, "Coquilles Saint-Jacques with cream and tarragon", "complement", "established", "fish_course", "Sur lie brioche bridges cream; lemon oil note echoes tarragon; mineral mirrors scallop sweetness.")
    PAIR(pr2, "Sashimi platter with yuzu ponzu", "complement", "adventurous", "fish_course", "Mineral Atlantic Muscadet suits raw fish; saline finish mirrors soy-yuzu; chalk mirrors rice.")

# ── Region 5: Pouilly-Fumé ────────────────────────────────────────────────────
print("=== Region 5: Pouilly-Fumé ===")
r = R("Pouilly-Fumé", "France", "wine",
      designation_type="AOC", designation_name="Pouilly-Fumé AOC",
      reputation_tier="prestigious", quality_trajectory="established",
      description="Loire Valley's most prestigious Sauvignon Blanc appellation on the right bank opposite Sancerre; flint, limestone and clay soils; wines of smoky ('fumé') mineral character and herbal intensity.",
      key_producers="Didier Dagueneau, de Ladoucette, Henri Bourgeois, Gilles Blanchet",
      historical_context="Didier Dagueneau (1956–2008) revolutionised Pouilly-Fumé with single-vineyard bottlings and barrel fermentation; his Silex and Pur Sang are among France's most iconic white wines.")
VIN(r, 2022, "excellent", "rising", "Textbook Loire year; Sauvignon of great mineral precision and smoky depth.")
VIN(r, 2021, "exceptional", "rising", "Outstanding vintage; Pouilly-Fumé of rare complexity; Silex-type wines will age decades.")
VIN(r, 2020, "excellent", "stable", "Warm year; generous, aromatic Sauvignon with flint mineral character.")
VIN(r, 2019, "very_good", "stable", "Good balance; consistent Pouilly-Fumé of classic herbal-mineral profile.")
VIN(r, 2018, "excellent", "stable", "Classic year; structured Pouilly with fine aging potential.")
p1 = P("Domaine Didier Dagueneau", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="The late Didier Dagueneau's legendary estate, now run by his son Louis-Benjamin; Silex (flint), Pur Sang (limestone), Blanc Fumé de Pouilly — three benchmark single-vineyard expressions; barrel fermentation.",
       reputation_narrative="Dagueneau's Silex and Pur Sang are among France's most sought-after white wines; they transformed Pouilly-Fumé from good to extraordinary.",
       price_positioning="premium")
p2 = P("de Ladoucette", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The largest and most famous Pouilly-Fumé estate; Baron de 'L' is their prestige wine; wide range from accessible Pouilly to the iconic single-vintage Baron de 'L' Sauvignon.",
       reputation_narrative="De Ladoucette is Pouilly-Fumé's most internationally recognised estate; Baron de 'L' is the appellation's most celebrated wine outside of Dagueneau.",
       price_positioning="premium")
pr1, n1 = PROD("Dagueneau Silex Pouilly-Fumé", "wine_still", p1, r, "France",
               subcategory="Sauvignon Blanc", price_tier="premium",
               description="The legendary flint-terroir Pouilly-Fumé; barrel-fermented Sauvignon of extraordinary complexity — gunflint, citrus oil, white peach, green herbs and decades of aging potential; France's most iconic Sauvignon.")
if n1:
    PAIR(pr1, "Grilled langoustines with butter and lemon", "complement", "classic", "fish_course", "Iconic Loire pairing; gunflint and citrus amplify langoustine sweetness; barrel complexity bridges butter.")
    PAIR(pr1, "Turbot with bone broth and wild herbs", "complement", "established", "fish_course", "Prestigious pairing; Silex's complexity elevates finest turbot; herbs echo Sauvignon's register.")
    PAIR(pr1, "Crottin de Chavignol at peak affinage", "complement", "classic", "cheese", "The great Loire pairing; Sauvignon and goat's cheese are natural partners; Silex elevates.")
    PAIR(pr1, "Sea urchin on toasted sourdough with lemon", "elevate", "adventurous", "starter", "Gunflint mineral and citrus elevate sea urchin's iodine; barrel complexity bridges.")
pr2, n2 = PROD("de Ladoucette Baron de 'L' Pouilly-Fumé", "wine_still", p2, r, "France",
               subcategory="Sauvignon Blanc", price_tier="premium",
               description="Prestige Pouilly-Fumé single-vineyard; Sauvignon of great mineral depth and precision — grapefruit oil, white flower, gunflint and a long, clean finish; the most elegant mainstream Pouilly.")
if n2:
    PAIR(pr2, "Oysters with Champagne mignonette", "complement", "classic", "aperitif", "Mineral-citrus Sauvignon suits oysters; gunflint echoes oyster's iodine; white flower bridges.")
    PAIR(pr2, "Grilled sea bass with herb salsa verde", "complement", "established", "fish_course", "Loire mineral suits sea bass; herbal Sauvignon echoes salsa verde; grapefruit bridges lemon.")
    PAIR(pr2, "Warm goat's cheese tart with honey", "complement", "classic", "starter", "Textbook Loire Sauvignon and goat's cheese; grapefruit bridges honey sweetness.")
    PAIR(pr2, "Sushi omakase with wasabi and pickled ginger", "complement", "adventurous", "main", "Mineral Sauvignon suits vinegared rice and raw fish; grapefruit bridges ginger.")

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
