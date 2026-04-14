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
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B133 ──────────────────────────────────────────────────────────────────────
# Targets: Muscadet AOC (France), Vouvray AOC (France),
#          Saumur-Champigny AOC (France), Vernaccia di San Gimignano DOCG (Italy),
#          Primitivo di Manduria DOC (Italy)

# 1. MUSCADET AOC — Loire Valley, France
print("=== Muscadet AOC ===")
r1 = R("Muscadet AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Muscadet Sèvre et Maine AOC",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description="Loire Valley white wine appellation at the Atlantic coast producing Melon de Bourgogne wines; the 'Sèvre et Maine' sub-appellation is the quality heartland on schist, granite, and gneiss soils. Extended lees aging ('sur lie' — minimum winter on the lees) creates yeasty, brioche richness alongside the briny, saline freshness. The world's definitive oyster wine; misunderstood but increasingly celebrated for its complexity and terroir expression.",
        key_producers="Domaine de la Pépière, Muscadet de la Louvetrie, Château du Cléray, Jérémie Huchet",
        historical_context="Muscadet became synonymous with cheap acidic French white wine in the 1970s-80s due to excessive production and thin, harsh wines. The reputation revival began with quality-focused producers bottling 'sur lie' and exploring granite and schist terroirs. Marc Olivier's Pépière and Loire natural wine movement restored Muscadet's credibility. The best Sèvre et Maine wines can age for 20+ years, developing extraordinary complexity that rivals white Burgundy.")
for yr, qd, pt, sn in [
    (2018, "very_good", "stable", "Good year; Melon de Bourgogne shows briny mineral freshness; sur lie wines have excellent depth"),
    (2019, "excellent", "rising", "Excellent vintage; Atlantic conditions perfect; Muscadet shows saline mineral and lees complexity"),
    (2020, "very_good", "rising", "Good growing season; gneiss and granite terroirs well-expressed; sur lie wines rich and mineral"),
    (2021, "excellent", "rising", "Excellent; cool Atlantic year; Muscadet's natural acidity pristine; best sur lie wines outstanding"),
    (2022, "very_good", "stable", "Good vintage; warm summer balanced by Atlantic humidity; Melon shows citrus and brine character"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Domaine de la Pépière", "winery", r1, "France",
        production_philosophy="natural",
        philosophy_description="Marc Olivier's estate that led the Muscadet renaissance; natural viticulture, minimal sulphur, single-parcel Gros Plant and Melon sur lie; Clos des Briords from old vines on gneiss shows what Muscadet can be.",
        reputation_narrative="The producer who rehabilitated Muscadet's reputation; Marc Olivier's natural approach and single-parcel wines showed the world that Melon de Bourgogne on great terroir can age and rival white Burgundy in complexity.",
        price_positioning="premium")

pr1a1, n = PROD("Domaine de la Pépière Clos des Briords Muscadet Sèvre et Maine", "wine_still", p1a, r1, "France",
    subcategory="Melon de Bourgogne sur lie", price_tier="premium",
    description="Old vine Melon de Bourgogne from gneiss soils; extended sur lie aging; saline mineral, lemon zest, brioche, oyster shell; extraordinary depth for Muscadet; ages 15+ years; the wine that changed the region's reputation.")
if n:
    PAIR(pr1a1, "Fines de Claire oysters with lemon", "complement", "classic", "amuse", "The definitive Muscadet pairing; saline mineral wine mirrors oyster's oceanic brine; lemon echoes wine's citrus")
    PAIR(pr1a1, "Moules marinières with crusty bread", "complement", "classic", "starter", "Atlantic mussels with white wine; Muscadet's mineral freshness echoes mussels; sur lie richness mirrors cream")
    PAIR(pr1a1, "Sole meunière with brown butter and capers", "complement", "classic", "fish_course", "Loire classic; sur lie richness mirrors the butter; capers bridge with wine's saline mineral character")
    PAIR(pr1a1, "Plateau de fruits de mer (seafood platter)", "complement", "classic", "main", "Classic French seafood platter; Muscadet's briny mineral mirrors every element; the perfect shellfish wine")

pr1a2, n = PROD("Domaine de la Pépière Muscadet Sèvre et Maine sur Lie", "wine_still", p1a, r1, "France",
    subcategory="Melon de Bourgogne sur lie", price_tier="mid_range",
    description="Estate Muscadet sur lie; fresh and mineral with brioche, lemon, saline Atlantic character; excellent everyday expression of the appellation at exceptional value.")
if n:
    PAIR(pr1a2, "Clams steamed with white wine and parsley", "complement", "classic", "starter", "Simple preparation; Muscadet's mineral freshness echoes the clam brine; parsley bridges herbal notes")
    PAIR(pr1a2, "Grilled sardines with lemon and herbs", "complement", "classic", "starter", "Atlantic fish tradition; Pépière's freshness cuts the sardine richness; herbs bridge; coastal Bretagne pairing")
    PAIR(pr1a2, "Crab salad with avocado and citrus", "complement", "classic", "starter", "Delicate crab; Muscadet's mineral freshness frames the sweetness; citrus echoes wine's lemon character")
    PAIR(pr1a2, "Fish and chips with malt vinegar", "complement", "suggested", "main", "British classic with French wine; Muscadet's acidity cuts the batter fat; mineral freshness echoes malt vinegar")

p1b = P("Château du Cléray", "winery", r1, "France",
        production_philosophy="traditional",
        philosophy_description="Sauvion family estate producing classic Muscadet Sèvre et Maine sur lie; the benchmark for mainstream quality in the appellation.",
        reputation_narrative="One of Muscadet's most reliable and consistent producers; Château du Cléray's sur lie wines have introduced generations of wine drinkers to the appellation's Atlantic mineral character.",
        price_positioning="mid_range")

pr1b1, n = PROD("Château du Cléray Muscadet Sèvre et Maine sur Lie", "wine_still", p1b, r1, "France",
    subcategory="Melon de Bourgogne sur lie", price_tier="mid_range",
    description="Classic Muscadet sur lie from Sauvion; crisp, saline, lemon, brioche yeast; fresh and mineral; excellent everyday seafood wine.")
if n:
    PAIR(pr1b1, "Grilled langoustines with herb aioli", "complement", "classic", "starter", "Atlantic shellfish; Muscadet's mineral acidity frames the langoustine; herb aioli bridges botanical notes")
    PAIR(pr1b1, "Soupe de poissons with rouille and croutons", "complement", "established", "starter", "Classic French fish soup; Muscadet's acidity cuts the rich soup; mineral character echoes the ocean")
    PAIR(pr1b1, "Grilled plaice with lemon butter", "complement", "classic", "fish_course", "Simple flatfish preparation; Muscadet's freshness and citrus complement; lemon butter bridges the mineral")
    PAIR(pr1b1, "Chèvre fresh goat cheese with honey", "complement", "established", "cheese", "Loire goat cheese tradition; Muscadet's acidity mirrors the tanginess; honey softens; regional pairing")

pr1b2, n = PROD("Château du Cléray Prestige Muscadet Sèvre et Maine", "wine_still", p1b, r1, "France",
    subcategory="Melon de Bourgogne", price_tier="mid_range",
    description="Premium Muscadet with extended aging; deeper complexity; white flowers, lemon cream, oyster shell, light brioche; more structured than the standard sur lie.")
if n:
    PAIR(pr1b2, "Scallops with cauliflower cream and sea vegetable", "complement", "classic", "starter", "Delicate scallop; Muscadet's mineral matches the sea vegetable; cauliflower cream balanced by acidity")
    PAIR(pr1b2, "Pan-fried sole with caper beurre blanc", "complement", "classic", "fish_course", "Loire classic; Muscadet's weight matches the butter sauce; capers bridge with saline mineral notes")
    PAIR(pr1b2, "Lobster bisque with cream and cognac", "complement", "established", "starter", "Rich bisque; Prestige's depth handles the cream; mineral freshness cuts through; cognac bridges complexity")
    PAIR(pr1b2, "Grilled white asparagus with hollandaise", "complement", "classic", "starter", "Loire spring classic; Muscadet's mineral freshness and hollandaise; asparagus echoes wine's herbal notes")

# 2. VOUVRAY AOC — Loire Valley, France
print("=== Vouvray AOC ===")
r2 = R("Vouvray AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Vouvray AOC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Loire Valley's most versatile appellation from Chenin Blanc in all styles — dry (sec), off-dry (demi-sec), sweet (moelleux, liquoreux), and sparkling (pétillant, mousseux); tuffeau (chalk-limestone) caves traditionally used for storage; the best dry and sweet Vouvray ages magnificently for decades. The tension between richness and acidity in Chenin Blanc creates wines of extraordinary complexity.",
        key_producers="Domaine Huet, Domaine du Clos Naudin, François Pinon, Philippe Foreau",
        historical_context="Vouvray has produced wine since the Benedictine monks of Marmoutier planted vineyards in the 11th century. The appellation produces Chenin Blanc in the full range of styles; the vintage conditions determine whether a year becomes sec, demi-sec, or moelleux. Domaine Huet (now biodynamic under Noël Pinguet) is universally considered the greatest Vouvray producer; their three parcels (Haut-Lieu, Clos du Bourg, Le Mont) define the appellation.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good Vouvray year; Chenin Blanc achieved good ripeness; demi-sec and sec both excellent; moelleux scarce"),
    (2019, "excellent", "rising", "Excellent vintage; classic dry and demi-sec showing great mineral tension; moelleux exceptional where conditions allowed"),
    (2020, "exceptional", "rising", "Exceptional Chenin Blanc year; dry Vouvray of extraordinary depth; moelleux of legendary quality; landmark vintage"),
    (2021, "very_good", "rising", "Good growing season; Chenin shows precision and mineral backbone; excellent sec and demi-sec produced"),
    (2022, "excellent", "rising", "Excellent; warm summer with late freshness; Vouvray dry of great depth; some fine demi-sec; good moelleux"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Domaine Huet", "winery", r2, "France",
        production_philosophy="biodynamic",
        philosophy_description="The greatest Vouvray estate; three parcels — Haut-Lieu, Clos du Bourg, Le Mont — each producing sec, demi-sec, and moelleux in appropriate years; biodynamically farmed; wines of extraordinary longevity.",
        reputation_narrative="Universally considered the reference for Vouvray and one of France's greatest wine estates; Huet's Chenin Blanc across all three parcels defines the appellation and demonstrates Chenin's extraordinary range and aging potential.",
        price_positioning="ultra_premium")

pr2a1, n = PROD("Domaine Huet Clos du Bourg Vouvray Sec", "wine_still", p2a, r2, "France",
    subcategory="Chenin Blanc sec", price_tier="ultra_premium",
    description="Dry Vouvray from the historic walled vineyard Clos du Bourg; quince, white peach, chalk mineral, beeswax; extraordinary tension; develops into profound complexity over 20-30+ years; benchmark dry Chenin Blanc.")
if n:
    PAIR(pr2a1, "Freshwater pike with beurre blanc sauce", "complement", "classic", "fish_course", "The definitive Loire pairing; local fish with local wine; beurre blanc's butter mirrors Chenin's richness; chalk mineral echoes the river")
    PAIR(pr2a1, "Roast chicken with Touraine herbs and cream sauce", "complement", "classic", "main", "Loire valley Sunday tradition; Chenin's acidity and richness suit cream sauce; herbs echo wine's botanical depth")
    PAIR(pr2a1, "Crottin de Chavignol goat cheese (aged)", "complement", "classic", "cheese", "Loire goat cheese pairing tradition; Chenin's acidity mirrors tanginess; chalk mineral bridges; regional perfection")
    PAIR(pr2a1, "Seared foie gras with apple reduction", "complement", "classic", "starter", "Loire luxury; Chenin's richness and acidity balance the foie gras; apple reduction echoes wine's quince character")

pr2a2, n = PROD("Domaine Huet Le Mont Vouvray Demi-Sec", "wine_still", p2a, r2, "France",
    subcategory="Chenin Blanc demi-sec", price_tier="ultra_premium",
    description="Off-dry Vouvray from Le Mont parcel; honeydew melon, quince, lanolin, chalk; perfectly balanced sweetness and acidity; ideal pairing wine for complex dishes; ages magnificently over decades.")
if n:
    PAIR(pr2a2, "Seared langoustines with butter and ginger", "complement", "classic", "starter", "Demi-sec's sweetness frames langoustine; ginger adds spice bridge; butter richness mirrored by Chenin's texture")
    PAIR(pr2a2, "Roast pork with quince compote and sage", "complement", "classic", "main", "Quince in both wine and dish; Demi-sec's sweetness suits pork fat; sage herbal note bridges")
    PAIR(pr2a2, "Blue cheese soufflé with walnut", "complement", "established", "main", "Demi-sec Chenin's sweetness handles the pungent cheese; walnut bridges chalk mineral; Loire tradition")
    PAIR(pr2a2, "Thai spiced green papaya salad", "complement", "classic", "starter", "Spice and sweetness; demi-sec's residual sugar tames chilli; citrus mirrors wine's fruit; unexpected but classic")

p2b = P("Philippe Foreau Clos Naudin", "winery", r2, "France",
        production_philosophy="traditional",
        philosophy_description="Family estate producing precise, terroir-driven Vouvray across all styles; tuffeau soils; Philippe Foreau's traditional approach with indigenous yeasts produces wines of extraordinary elegance.",
        reputation_narrative="One of Vouvray's most celebrated and consistent producers; Clos Naudin's Chenin Blanc across sec, demi-sec, and moelleux styles shows how the variety expresses tuffeau limestone with precision and longevity.",
        price_positioning="ultra_premium")

pr2b1, n = PROD("Philippe Foreau Clos Naudin Vouvray Sec", "wine_still", p2b, r2, "France",
    subcategory="Chenin Blanc sec", price_tier="ultra_premium",
    description="Dry Vouvray from tuffeau soils; quince, citrus, chalk, beeswax; pristine mineral precision; indigenous yeasts; extraordinary aging potential; regularly compared to premier cru white Burgundy in complexity.")
if n:
    PAIR(pr2b1, "Grilled zander (river pike-perch) with cream and dill", "complement", "classic", "fish_course", "Loire freshwater fish; Chenin's chalk mineral and acidity suit the delicate fish; cream mirrors wine's texture")
    PAIR(pr2b1, "Asparagus with hollandaise and smoked salmon", "complement", "established", "starter", "Spring Loire classic; Chenin's mineral depth handles the richness; asparagus echoes wine's herbal dimension")
    PAIR(pr2b1, "Aged Camembert de Normandie with apple slices", "complement", "established", "cheese", "Soft ripened cheese; Chenin's acidity balances; apple echoes wine's quince; Norman-Loire regional bridge")
    PAIR(pr2b1, "Morel mushroom risotto with Parmesan", "complement", "classic", "main", "Spring mushroom; Vouvray's mineral complexity mirrors morel's earthy depth; Parmesan fat balanced by acidity")

pr2b2, n = PROD("Philippe Foreau Clos Naudin Vouvray Moelleux", "wine_still", p2b, r2, "France",
    subcategory="Chenin Blanc moelleux", price_tier="ultra_premium",
    description="Sweet Vouvray moelleux from botrytized Chenin Blanc; honey, apricot, quince, saffron, chalk; extraordinary balance of sweetness and acidity; one of France's great dessert wines; ages for 50+ years.")
if n:
    PAIR(pr2b2, "Tarte Tatin with crème fraîche", "complement", "classic", "dessert", "Loire apple tart; Moelleux's quince and honey echo the caramelized apple; crème fraîche bridges wine's richness")
    PAIR(pr2b2, "Roquefort with walnut bread and honey", "complement", "classic", "cheese", "Sauternes-Roquefort principle; sweet Chenin's acidity handles the blue cheese intensity; honey bridges")
    PAIR(pr2b2, "Pan-seared foie gras with Sauternes reduction", "complement", "classic", "starter", "Loire luxury tradition; Moelleux handles foie gras perfectly; Sauternes bridge in the reduction")
    PAIR(pr2b2, "Peach Melba with raspberry coulis", "complement", "classic", "dessert", "Peach resonates with Moelleux's apricot character; raspberry coulis bridges acidity; honeyed sweetness carries")

# 3. SAUMUR-CHAMPIGNY AOC — Loire Valley, France
print("=== Saumur-Champigny AOC ===")
r3 = R("Saumur-Champigny AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Saumur-Champigny AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The Loire Valley's most celebrated Cabernet Franc appellation; tuffeau chalk soils around the village of Champigny produce Loire's finest red wines with violet, pencil shavings, raspberry and earthy character. The wines are lighter than Bordeaux Cabernet Franc but show extraordinary freshness, terroir expression, and aging potential. Clos Rougeard from the Foucault brothers has become one of France's most collected wines.",
        key_producers="Clos Rougeard, Château du Hureau, Domaine Filliatreau, Domaine des Roches Neuves",
        historical_context="Saumur-Champigny received its own AOC in 1957, separating from the broader Saumur appellation. The chalk tuffeau soils (also used to build the Loire châteaux) give the wines their distinctive mineral character. Clos Rougeard from the Foucault brothers became France's most collected Cabernet Franc from the 2000s; allocated worldwide and fetching Burgundy Premier Cru prices. The 2019 sale of Clos Rougeard to the Bouygues family (owners of Montrose) caused international controversy.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Warm year; Cabernet Franc ripened fully; wines of unusual concentration for Saumur; dark fruit style"),
    (2019, "excellent", "rising", "Excellent; classic Loire freshness; Cabernet Franc shows violet, pencil and raspberry; exceptional year"),
    (2020, "very_good", "rising", "Good vintage; tuffeau chalk mineral well-expressed; elegant red fruit and earthy character"),
    (2021, "excellent", "rising", "Excellent; fresh cool year; classic Saumur-Champigny expression; violet and fresh red fruit; mineral depth"),
    (2022, "very_good", "stable", "Good year; warm summer; Cabernet Franc achieved ripeness; structured and fresh wines with tuffeau mineral"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Château du Hureau", "winery", r3, "France",
        production_philosophy="traditional",
        philosophy_description="Philippe Vatan's estate making some of Saumur-Champigny's finest Cabernet Franc from tuffeau soils; Lisagathe and Tuffe are the flagship cuvées showing the chalk's mineral expression.",
        reputation_narrative="One of Saumur-Champigny's most reliable quality references; Château du Hureau's Cabernet Franc shows the elegance and mineral depth possible from tuffeau chalk soils at their best.",
        price_positioning="premium")

pr3a1, n = PROD("Château du Hureau Lisagathe Saumur-Champigny", "wine_still", p3a, r3, "France",
    subcategory="Cabernet Franc single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Cabernet Franc from tuffeau chalk; violet, pencil shavings, red cherry, earthy mineral; silky tannins; one of Saumur's finest expressions of old vine Cabernet Franc; ages 10-15 years.")
if n:
    PAIR(pr3a1, "Rillettes de Tours with cornichons and bread", "complement", "classic", "starter", "Loire charcuterie classic; Cabernet Franc's freshness cuts pork fat; violet notes bridge the cured meat")
    PAIR(pr3a1, "Roast rack of veal with tarragon cream", "complement", "classic", "main", "Delicate veal; Loire Cabernet Franc's freshness suits; tarragon echoes wine's herbal notes; cream mirrors texture")
    PAIR(pr3a1, "Grilled salmon with lentils du Puy", "complement", "established", "fish_course", "Rich salmon with earthiness of lentils; Cabernet Franc bridges both; pencil mineral echoes lentil earthiness")
    PAIR(pr3a1, "Crottin de Chavignol goat cheese", "complement", "classic", "cheese", "Loire goat cheese with Loire red; tuffeau in wine echoes the chalk-grass character of the goats; regional tradition")

pr3a2, n = PROD("Château du Hureau Saumur-Champigny Réserve", "wine_still", p3a, r3, "France",
    subcategory="Cabernet Franc", price_tier="mid_range",
    description="Reserve Cabernet Franc showing house style; fresh red fruit, violet, earthy tuffeau mineral; medium body; excellent food wine; classic Saumur-Champigny expression at accessible price.")
if n:
    PAIR(pr3a2, "Bistro steak frites with Béarnaise sauce", "complement", "classic", "main", "Classic French bistro; Cabernet Franc's freshness suits steak; Béarnaise tarragon echoes wine's herbal notes")
    PAIR(pr3a2, "Chèvre chaud salad with walnuts and honey", "complement", "classic", "starter", "Warm goat cheese salad; Cabernet Franc's acidity handles; honey bridges fruit; walnut adds earthy bridge")
    PAIR(pr3a2, "Duck magret with cherry compote", "complement", "classic", "main", "Duck and Cabernet Franc; cherry compote mirrors wine's red fruit; duck fat tamed by fresh acidity; Loire classic")
    PAIR(pr3a2, "Mushroom crêpes with cream sauce", "complement", "established", "main", "Loire crêpe tradition; Cabernet Franc's earthy notes bridge mushroom; cream sauce balanced by acidity")

p3b = P("Domaine des Roches Neuves", "winery", r3, "France",
        production_philosophy="biodynamic",
        philosophy_description="Thierry Germain's biodynamic Saumur-Champigny estate; Portuguese-born winemaker with Loire terroir passion; Terres Chaudes and Marginale single-parcel Cabernet Franc are benchmarks.",
        reputation_narrative="One of Saumur-Champigny's most dynamic and internationally acclaimed producers; Thierry Germain's biodynamic approach and single-parcel wines have renewed collector interest in the appellation.",
        price_positioning="ultra_premium")

pr3b1, n = PROD("Domaine des Roches Neuves Terres Chaudes Saumur-Champigny", "wine_still", p3b, r3, "France",
    subcategory="Cabernet Franc single parcel", price_tier="ultra_premium",
    description="Single-parcel Cabernet Franc from warm tuffeau limestone; more concentrated than typical Saumur; dark cherry, violet, graphite mineral; structured tannins; Loire's most ambitious Cabernet Franc.")
if n:
    PAIR(pr3b1, "Slow-cooked lamb shoulder with thyme and garlic", "complement", "classic", "main", "Classic Cabernet Franc and lamb; Terres Chaudes' structure handles the slow-cooked richness; herbs bridge")
    PAIR(pr3b1, "Grilled pigeon with mushroom and hazelnut", "complement", "classic", "main", "Delicate game bird; Cabernet Franc's refinement mirrors pigeon's delicacy; mushroom echoes mineral depth")
    PAIR(pr3b1, "Beef cheeks braised in red wine with celeriac", "complement", "established", "main", "Gelatinous braise; wine's structure softened by collagen richness; celeriac's earthiness bridges the graphite")
    PAIR(pr3b1, "Aged Comté with grape must", "complement", "established", "cheese", "Nutty aged cheese; Terres Chaudes' mineral and fruit balance; grape must bridges the dark cherry notes")

pr3b2, n = PROD("Domaine des Roches Neuves Saumur-Champigny", "wine_still", p3b, r3, "France",
    subcategory="Cabernet Franc", price_tier="premium",
    description="Estate Saumur-Champigny; vibrant red cherry, violet, tuffeau mineral, pencil shavings; silky and fresh; excellent value introduction to the estate's biodynamic philosophy.")
if n:
    PAIR(pr3b2, "Roasted tomatoes and mozzarella with basil", "complement", "suggested", "starter", "Simple Italian-French bridge; Cabernet Franc's freshness suits tomato; violet notes match the basil aromatics")
    PAIR(pr3b2, "Lentil soup with smoked duck", "complement", "established", "main", "Hearty autumn dish; Cabernet Franc's earthy depth bridges lentils; smoked duck fat tamed by wine's freshness")
    PAIR(pr3b2, "Ratatouille with grilled bread", "complement", "established", "main", "Provençal vegetable stew; Loire red's fresh acidity suits; earthy notes bridge the roasted vegetables")
    PAIR(pr3b2, "Fromage de chèvre frais with herbs", "complement", "classic", "cheese", "Fresh goat cheese; Cabernet Franc's acidity mirrors the tanginess; herbs echo wine's floral herbal character")

# 4. VERNACCIA DI SAN GIMIGNANO DOCG — Tuscany, Italy
print("=== Vernaccia di San Gimignano DOCG ===")
r4 = R("Vernaccia di San Gimignano DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Vernaccia di San Gimignano DOCG",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Italy's first DOC (1966) and DOCG since 1993; the ancient Vernaccia grape around the medieval tower town of San Gimignano in Tuscany; alberese soil (clay-limestone) and galestro (friable limestone schist); the wines range from fresh and mineral to barrel-fermented versions of depth and complexity. Historically praised by Dante and Michelangelo; declined in quality during overproduction era; now revived by quality-focused producers.",
        key_producers="Panizzi, San Quirico, Montenidoli, Teruzzi",
        historical_context="Vernaccia di San Gimignano was Italy's first DOC in 1966, an honour that paradoxically led to overproduction and quality decline. The revival began in the 1990s when producers like Panizzi and Montenidoli took quality seriously. The Medieval town of San Gimignano's 14 surviving towers (originally 72) make it one of Italy's most photographed towns; wine tourism is central. Vernaccia is Dante's 'vino delle genti' mentioned in the Divine Comedy.")
for yr, qd, pt, sn in [
    (2019, "very_good", "stable", "Good Vernaccia year; mineral freshness and almond character; galestro soils particularly expressive"),
    (2020, "excellent", "rising", "Excellent vintage; Vernaccia shows citrus, bitter almond and mineral with unusual depth; best wines outstanding"),
    (2021, "very_good", "rising", "Good growing season; classic dry Vernaccia expression; floral aromatics particularly vibrant"),
    (2022, "excellent", "rising", "Excellent conditions; hot summer moderated by altitude breezes; Vernaccia aromatic and mineral; fine acidity"),
    (2023, "very_good", "stable", "Good year; typical Tuscan conditions; Vernaccia shows its characteristic bitter almond finish"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Panizzi", "winery", r4, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="The leading quality producer reviving Vernaccia's reputation; Giovanni Panizzi was the first to show barrel fermentation could add complexity without masking the variety's character.",
        reputation_narrative="The producer who led Vernaccia's quality renaissance; Panizzi's commitment to low yields and minimal oak showed that Vernaccia di San Gimignano could be complex, age-worthy and internationally relevant.",
        price_positioning="premium")

pr4a1, n = PROD("Panizzi Vernaccia di San Gimignano Riserva", "wine_still", p4a, r4, "Italy",
    subcategory="Vernaccia Riserva", price_tier="premium",
    description="Barrel-fermented Vernaccia Riserva; citrus, white peach, bitter almond, flint, light oak spice; textured and complex; ages 5-8 years; one of the DOCG's finest expressions showing the variety's potential.")
if n:
    PAIR(pr4a1, "Ribollita (Tuscan bread and vegetable soup)", "complement", "classic", "main", "Tuscan winter classic; Vernaccia's crisp acidity lifts the dense soup; bitter almond note bridges the kale")
    PAIR(pr4a1, "Grilled bistecca alla Fiorentina (T-bone steak)", "contrast", "adventurous", "main", "Unexpected white with Florentine tradition; Vernaccia's texture and bitter almond create interesting contrast")
    PAIR(pr4a1, "Pappardelle al cinghiale (wild boar pasta)", "bridge", "suggested", "main", "Vernaccia's weight bridges; bitter almond complements the game richness; Tuscan soul in both")
    PAIR(pr4a1, "Aged Pecorino Toscano with honey and walnuts", "complement", "classic", "cheese", "Tuscan sheep cheese; Vernaccia's citrus and almond balance the fat; honey bridges; regional tradition")

pr4a2, n = PROD("Panizzi Vernaccia di San Gimignano", "wine_still", p4a, r4, "Italy",
    subcategory="Vernaccia", price_tier="mid_range",
    description="Estate Vernaccia di San Gimignano; fresh and aromatic with citrus blossom, almond, peach, flint mineral; crisp acidity; excellent food wine and benchmark for the DOCG's fresh style.")
if n:
    PAIR(pr4a2, "Crostini toscani with chicken liver pâté", "complement", "established", "starter", "Classic Tuscan starter; Vernaccia's freshness cuts the rich pâté; bitter almond echoes the liver's character")
    PAIR(pr4a2, "Fritto misto di verdure (mixed fried vegetables)", "complement", "classic", "starter", "Fried Tuscan vegetables; Vernaccia's crisp acidity cuts the batter; bitter almond notes echo fried artichoke")
    PAIR(pr4a2, "Pici all'aglione (thick pasta with garlic tomato sauce)", "complement", "classic", "main", "Traditional Sienese pasta; Vernaccia's freshness lifts the tomato; acidity bridges the garlic intensity")
    PAIR(pr4a2, "Insalata di farro con verdure (farro grain salad)", "complement", "classic", "starter", "Tuscan grain salad; Vernaccia's mineral freshness suits; bitter almond bridges the nutty farro character")

p4b = P("Montenidoli", "winery", r4, "Italy",
        production_philosophy="natural",
        philosophy_description="Elisabetta Fagiuoli's estate producing Vernaccia and other varieties with minimal intervention; historic property with ancient terraced vineyards; Il Tradizionale shows skin-contact Vernaccia's character.",
        reputation_narrative="The pioneering natural wine producer of San Gimignano; Montenidoli's minimal intervention approach and historic terraced vineyards produce Vernaccia of unique complexity and age-worthiness.",
        price_positioning="premium")

pr4b1, n = PROD("Montenidoli Il Tradizionale Vernaccia di San Gimignano", "wine_still", p4b, r4, "Italy",
    subcategory="Vernaccia traditional", price_tier="premium",
    description="Traditional skin-contact Vernaccia; almond, citrus, dried flowers, earthy mineral; grippy texture from extended skin contact; unique expression of the variety; very different from fresh commercial style.")
if n:
    PAIR(pr4b1, "Trippa alla Fiorentina (Florentine tripe with tomato)", "complement", "classic", "main", "Traditional Florentine offal; Vernaccia's grip and mineral handle the intensity; tomato bridges the acidity")
    PAIR(pr4b1, "Salumi misti with lardo and finocchiona", "complement", "established", "starter", "Tuscan charcuterie; skin-contact Vernaccia's tannins cut fat; almond notes bridge fennel-spiced sausage")
    PAIR(pr4b1, "Aged Pecorino di Pienza with truffle oil", "complement", "established", "cheese", "Strong aged Tuscan sheep cheese; Vernaccia's grip handles it; truffle oil bridges earthy mineral depth")
    PAIR(pr4b1, "Ribollita with aged Parmesan", "complement", "classic", "main", "Enriched Tuscan soup; skin-contact Vernaccia's grip handles the density; bitter almond bridges the kale")

pr4b2, n = PROD("Montenidoli Fiore Vernaccia di San Gimignano", "wine_still", p4b, r4, "Italy",
    subcategory="Vernaccia", price_tier="mid_range",
    description="Fresh-style Vernaccia from Montenidoli; citrus blossom, peach, almond, mineral; vibrant and aromatic; shows the grape's floral freshness; excellent aperitivo wine.")
if n:
    PAIR(pr4b2, "Bruschetta al pomodoro with fresh basil", "complement", "classic", "amuse", "Tuscan classic; Vernaccia's acidity mirrors tomato; basil echoes wine's floral aromatic character")
    PAIR(pr4b2, "Caprese salad with buffalo mozzarella", "complement", "classic", "starter", "Classic Italian; Vernaccia's freshness complements; tomato and basil mirrored in wine's aromatics; summer pairing")
    PAIR(pr4b2, "Grilled fish with Tuscan herbs and olive oil", "complement", "classic", "fish_course", "Simple Tuscan preparation; Vernaccia's mineral freshness and bitter almond suit the herbs; olive oil bridges")
    PAIR(pr4b2, "Zucchini flowers stuffed with ricotta", "complement", "classic", "starter", "Delicate vegetable; Vernaccia's citrus and almond complement; ricotta fat balanced by wine's crisp acidity")

# 5. PRIMITIVO DI MANDURIA DOC — Puglia, Italy
print("=== Primitivo di Manduria DOC ===")
r5 = R("Primitivo di Manduria DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Primitivo di Manduria DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Puglia's most prestigious red wine appellation for Primitivo (genetically identical to Zinfandel); sandy soils in the Manduria area of Salento peninsula at low altitude; the 'dolce naturale' sweet style (minimum 16% alcohol) is traditional; dry Primitivo produces rich, generous reds of extraordinary concentration. DNA testing proved Primitivo and Zinfandel are the same variety (Croatian Crljenak) in 2001.",
        key_producers="Gianfranco Fino, Felline, San Marzano, Pervini",
        historical_context="Primitivo received DOC in 1974 and the Dolce Naturale style received DOCG recognition. DNA research in 2001 proved the variety is identical to California's Zinfandel and Croatia's Crljenak Kaštelanski, triggering enormous American interest in Puglian wine. Gianfranco Fino's single-vineyard old vine Primitivo (Es) from 2004 onwards transformed the region's reputation and now fetches premium prices. The Salento peninsula's extreme heat produces wines of exceptional richness.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good Primitivo year; old vine concentration; rich dark fruit with characteristic alcohol warmth"),
    (2019, "excellent", "rising", "Excellent vintage; Primitivo shows extraordinary concentration; dark plum, fig, chocolate; structured wines"),
    (2020, "very_good", "rising", "Good growing season; Manduria heat produced rich generous reds; balanced by sandy soil freshness"),
    (2021, "excellent", "rising", "Excellent; old vine Primitivo at its most expressive; concentration with surprising elegance; benchmark wines"),
    (2022, "very_good", "stable", "Good year; Salento heat moderated; Primitivo shows its characteristic dried fruit and spice character"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Gianfranco Fino", "winery", r5, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="The producer who transformed Primitivo di Manduria's reputation; single-vineyard Es from 60-80 year old head-trained vines in sandy soils; minimal intervention; concentrated and elegant wine that commands Barolo prices.",
        reputation_narrative="Italy's most celebrated Primitivo producer; Fino's Es from old alberello (bush vine) Primitivo commands premium prices and has shown that Puglian wine can reach the summit of Italian quality.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("Gianfranco Fino Es Primitivo di Manduria", "wine_still", p5a, r5, "Italy",
    subcategory="Primitivo single vineyard", price_tier="ultra_premium",
    description="The benchmark Primitivo di Manduria; from 60-80 year old alberello vines in Manduria's sandy soils; dark cherry, fig, chocolate, licorice, dried violet; extraordinary concentration with surprising elegance; commands Barolo prices.")
if n:
    PAIR(pr5a1, "Ragù di manzo con polpette (slow-cooked meatball ragù)", "complement", "classic", "main", "Southern Italian Sunday cooking; Es's extraordinary richness needs the slow-cooked beef; tomato acidity bridges")
    PAIR(pr5a1, "Grilled lamb ribs with cumin and herbs", "complement", "established", "main", "Rich lamb with spice; Primitivo's fruit and warmth suit the cumin; herbs echo wine's dried herb character")
    PAIR(pr5a1, "Braised oxtail with Puglian olives and tomatoes", "complement", "classic", "main", "Southern Italian offal tradition; oxtail's collagen richness handles Es's power; olives and tomatoes bridge acidity")
    PAIR(pr5a1, "Aged Canestrato Pugliese with fig compote", "complement", "classic", "cheese", "Puglia's great sheep basket cheese; Es's concentration and richness balance the aged intensity; fig bridges dark fruit")

pr5a2, n = PROD("Gianfranco Fino Jo Primitivo Salento", "wine_still", p5a, r5, "Italy",
    subcategory="Primitivo", price_tier="premium",
    description="Entry Fino wine from young vine Primitivo; more accessible than Es but same philosophy; dark cherry, blackberry, spice, light chocolate; rich and generous; excellent introduction to the house style.")
if n:
    PAIR(pr5a2, "Orecchiette con cime di rapa (Puglian pasta with broccoli rabe)", "complement", "classic", "main", "The regional classic; bitter broccoli rabe needs Primitivo's fruit and warmth; anchovy version adds umami bridge")
    PAIR(pr5a2, "Bombette (Puglian stuffed pork rolls grilled)", "complement", "classic", "main", "Puglian street food classic; pork rolled with cheese and herbs; Primitivo's richness suits the stuffed preparation")
    PAIR(pr5a2, "Lamb and chickpea stew with cumin", "complement", "established", "main", "Hearty stew; Jo's fruit and warmth handle the spice; chickpea earthiness bridges the wine's depth")
    PAIR(pr5a2, "Pizza al forno with mozzarella and sausage", "complement", "classic", "main", "Southern Italian pizza; Primitivo's richness suits the sausage; tomato acidity balanced by wine's fruit")

p5b = P("San Marzano Vini", "winery", r5, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Cooperative-origin winery producing benchmark accessible Primitivo di Manduria; F Eddo and Sessantanni (60 years old vines) are the flagship wines.",
        reputation_narrative="The producer that made high-quality Primitivo di Manduria accessible globally; San Marzano's Sessantanni from 60-year-old vines has exceptional value and consistent quality.",
        price_positioning="mid_range")

pr5b1, n = PROD("San Marzano Sessantanni Primitivo di Manduria", "wine_still", p5b, r5, "Italy",
    subcategory="Primitivo old vine", price_tier="mid_range",
    description="60-year-old vine Primitivo (Sessantanni = 60 years); exceptional value; dark cherry, prune, chocolate, spice; rich and full-bodied; a benchmark for accessible old vine Primitivo quality.")
if n:
    PAIR(pr5b1, "Grilled pork ribs with bbq glaze", "complement", "classic", "main", "Primitivo's dark fruit and richness suit bbq pork; glaze sweetness mirrors wine's fig notes; spice bridges")
    PAIR(pr5b1, "Lasagne al forno with meat ragù", "complement", "classic", "main", "Rich pasta bake; Primitivo's warmth and dark fruit handle; tomato acidity bridges; southern Italian tradition")
    PAIR(pr5b1, "Lamb shoulder with roasted peppers and olives", "complement", "established", "main", "Mediterranean preparation; Primitivo's richness suits; peppers' sweetness bridges wine's fruit; olives add depth")
    PAIR(pr5b1, "Aged Cacioricotta with honey and fig", "complement", "established", "cheese", "Puglian aged goat/sheep cheese; Primitivo's richness meets the aged intensity; fig mirrors wine's dried fruit")

pr5b2, n = PROD("San Marzano F Eddo Primitivo Salento", "wine_still", p5b, r5, "Italy",
    subcategory="Primitivo", price_tier="mid_range",
    description="Everyday Primitivo Salento from San Marzano; ripe cherry, plum, warm spice; medium-full body; excellent accessible expression of Puglian Primitivo at everyday price.")
if n:
    PAIR(pr5b2, "Focaccia barese with olives and rosemary", "complement", "classic", "amuse", "Puglian bread tradition; Primitivo's fruit balances the salt; rosemary bridges wine's herbal warmth")
    PAIR(pr5b2, "Spaghetti al pomodoro with Puglian olive oil", "complement", "classic", "main", "Simple tomato pasta; F Eddo's acidity matches tomato; Puglian olive oil bridges; regional simplicity at its best")
    PAIR(pr5b2, "Grilled lamb kebabs with yoghurt sauce", "complement", "established", "main", "Mediterranean lamb; Primitivo's warmth handles the spice; yoghurt bridges tannin; approachable pairing")
    PAIR(pr5b2, "Calzone with mozzarella and ham", "complement", "established", "main", "Southern Italian comfort food; Primitivo's richness suits; tomato acidity balanced; ham saltiness tamed by fruit")

# ── Summary ───────────────────────────────────────────────────────────────────
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
print("B133 complete.")
conn.close()
