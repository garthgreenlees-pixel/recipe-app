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

# ── Region 1: Crémant de Loire ────────────────────────────────────────────────
print("=== Region 1: Crémant de Loire ===")
r = R("Crémant de Loire", "France", "wine",
      designation_type="AOC", designation_name="Crémant de Loire AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Loire Valley's cross-appellation sparkling wine designation; Chenin Blanc, Cabernet Franc and Pinot Gris; minimum 9 months on lees; wines of mineral freshness, Chenin complexity and excellent value.",
      key_producers="Domaine des Roches Neuves, Ackerman, Bouvet-Ladubay, Château Brissac",
      historical_context="Crémant de Loire was created in 1975 to provide quality-oriented alternative to Saumur Mousseux; minimum lees requirements raised; Chenin Blanc's natural acidity makes it ideal sparkling base.")
VIN(r, 2022, "excellent", "stable", "Good Loire year; Chenin-based Crémant of fine mineral freshness and clean acidity.")
VIN(r, 2021, "exceptional", "rising", "Outstanding vintage; Crémant de Loire approaching Champagne-level quality.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer Crémant with good depth and Chenin complexity.")
VIN(r, 2019, "excellent", "stable", "Classic profile; food-friendly Crémant de Loire of consistent mineral quality.")
VIN(r, 2018, "very_good", "stable", "Good balance; accessible, versatile Crémant de Loire.")
p1 = P("Domaine des Roches Neuves", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Thierry Germain's biodynamic Saumur-Champigny and Crémant estate; Insolite (pure Chenin) and Crémant from biodynamic Chenin Blanc; minimal intervention; outstanding quality.",
       reputation_narrative="Roches Neuves produces the finest estate-grown Crémant de Loire; Insolite still wine is Loire's benchmark natural Chenin Blanc.",
       price_positioning="mid_range")
p2 = P("Ackerman", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The oldest Loire sparkling house (1811); tuffeau cave aging; Cuvée 1811 prestige Crémant from Chenin Blanc; wide range of accessible to serious Crémant de Loire.",
       reputation_narrative="Ackerman created Loire sparkling wine in 1811; Cuvée 1811 is the historical benchmark for Crémant de Loire; consistent, widely available quality.",
       price_positioning="mid_range")
pr1, n1 = PROD("Roches Neuves Crémant de Loire Blanc Brut", "wine_sparkling", p1, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Biodynamic Chenin Blanc Crémant; tuffeau mineral, apple blossom, quince and a fine, persistent mousse; natural energy and mineral freshness; the Loire's finest estate-grown sparkling white.")
if n1:
    PAIR(pr1, "Loire river crayfish with herb bisque", "complement", "classic", "starter", "Loire regional tradition; Chenin's mineral and quince mirror crayfish sweetness; herb bridges.")
    PAIR(pr1, "Sautéed wild mushrooms with parsley and garlic", "complement", "established", "starter", "Biodynamic Crémant's apple-quince suits mushroom earthiness; mineral bridges garlic.")
    PAIR(pr1, "Grilled asparagus with soft-boiled egg and tarragon", "complement", "classic", "starter", "Loire classic; Chenin and asparagus are natural partners; egg richness bridges mineral mousse.")
    PAIR(pr1, "Warm Valençay goat's cheese with honey", "complement", "classic", "cheese", "Loire AOC pairing; mineral Chenin Crémant suits goat's cheese; quince bridges honey.")
pr2, n2 = PROD("Ackerman Cuvée 1811 Brut Crémant de Loire", "wine_sparkling", p2, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Historic Crémant de Loire from tuffeau caves; Chenin Blanc-dominant; apple, lemon, chalk mineral and a clean, mousse-rich finish; the definitive accessible Crémant de Loire.")
if n2:
    PAIR(pr2, "Oysters from Île de Noirmoutier", "complement", "classic", "aperitif", "Atlantic Loire pairing; mineral Chenin sparkling echoes oyster brine; mousse refreshes.")
    PAIR(pr2, "Chicken rillettes with cornichons and country bread", "complement", "established", "aperitif", "Loire tradition; Crémant's mousse and Chenin acidity cut pâté richness.")
    PAIR(pr2, "Tarte aux pommes (French apple tart)", "complement", "suggested", "dessert", "Apple in wine mirrors apple tart; Chenin acidity prevents sweetness; mousse bridges pastry.")
    PAIR(pr2, "Steamed mussels with white wine and parsley", "complement", "classic", "starter", "Classic Loire pairing; mineral Chenin echoes mussel brine; apple bridges wine sauce.")

# ── Region 2: Cabernet d'Anjou ────────────────────────────────────────────────
print("=== Region 2: Anjou ===")
r = R("Anjou", "France", "wine",
      designation_type="AOC", designation_name="Anjou AOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Loire Valley's historic heartland around Angers; Cabernet Franc reds, Chenin Blanc whites and rosés; Savennières (dry Chenin) and Coteaux du Layon (sweet) are its most prestigious sub-zones.",
      key_producers="Domaine des Baumard, Nicolas Joly, Mark Angeli, Jo Pithon",
      historical_context="The House of Anjou produced wine for English kings (12th century); Plantagenet kings exported Anjou wine throughout England; Chenin Blanc's Loire heartland; Savennières is France's most distinctive dry white appellation.")
VIN(r, 2022, "excellent", "stable", "Good Loire year; Savennières Chenin of great mineral depth and precision.")
VIN(r, 2021, "exceptional", "rising", "Benchmark vintage; Savennières and Coteaux du Layon of outstanding quality.")
VIN(r, 2020, "very_good", "stable", "Warm year; Coteaux du Layon of great botrytis concentration.")
VIN(r, 2019, "excellent", "stable", "Classic profile; food-friendly Anjou Cabernet Franc and mineral Savennières.")
VIN(r, 2018, "very_good", "stable", "Good balance; Anjou reds of solid structure and accessible character.")
p1 = P("Domaine des Baumard", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Florent Baumard's benchmark Anjou estate; Savennières (Clos du Papillon) and Coteaux du Layon Clos Sainte-Catherine; two of Loire's most age-worthy wines; extended cave aging.",
       reputation_narrative="Baumard's Clos du Papillon Savennières and Quarts de Chaume are Loire benchmarks; Clos Sainte-Catherine rivals great Sauternes at a fraction of the price.",
       price_positioning="mid_range")
p2 = P("Nicolas Joly", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="The world's most famous biodynamic wine advocate; Coulée de Serrant is his legendary 7-hectare monopole Savennières; radical biodynamics; wines of extraordinary oxidative complexity.",
       reputation_narrative="Nicolas Joly's Coulée de Serrant is one of France's most legendary wines; a single vineyard with its own AOC; polarising but unforgettable.",
       price_positioning="premium")
pr1, n1 = PROD("Baumard Clos du Papillon Savennières", "wine_still", p1, r, "France",
               subcategory="Chenin Blanc", price_tier="premium",
               description="Benchmark Savennières Chenin Blanc from schist slopes; dry, austere and demanding — lemon oil, white flower, flint, beeswax; needs 5+ years; one of Loire's most structured whites.")
if n1:
    PAIR(pr1, "Pike au beurre blanc with Loire-style sauce", "complement", "classic", "fish_course", "The definitive Loire pairing; Savennières and pike au beurre blanc is an aristocratic tradition.")
    PAIR(pr1, "Veal kidneys with mustard and cream sauce", "complement", "established", "main", "Austere Savennières suits organ meat's richness; beeswax bridges mustard; flint echoes mineral.")
    PAIR(pr1, "Slow-cooked lobster with tarragon vinaigrette", "complement", "established", "fish_course", "Savennières' mineral-flint and lemon oil suit lobster; tarragon bridges herb notes.")
    PAIR(pr1, "Aged Coulommiers cheese with quince", "complement", "suggested", "cheese", "Beeswax and lemon in Savennières bridge aged Coulommiers; quince mediates richness.")
pr2, n2 = PROD("Nicolas Joly Coulée de Serrant Savennières", "wine_still", p2, r, "France",
               subcategory="Chenin Blanc", price_tier="premium",
               description="The legendary monopole Savennières; extreme biodynamic; oxidative, complex and singular — beeswax, lanolin, dried chamomile, white truffle, flint and an eternal mineral finish; a wine of pure philosophy.")
if n2:
    PAIR(pr2, "Sole normande with cream, mussels and shrimps", "complement", "classic", "fish_course", "Loire nobility pairing; oxidative beeswax and mineral mirror cream-mussel richness.")
    PAIR(pr2, "White asparagus with mousseline sauce", "complement", "classic", "starter", "Loire spring classic; Savennières' intensity suits white asparagus's richness; lanolin bridges.")
    PAIR(pr2, "Veal sweetbreads with Vin Jaune reduction", "complement", "established", "main", "Both oxidative wines; Coulée complements rather than echoes Vin Jaune's reduction notes.")
    PAIR(pr2, "Sautéed chanterelles with parsley and garlic", "complement", "established", "starter", "White truffle note in wine bridges chanterelle earthiness; biodynamic affinity.")

# ── Region 3: Vouvray ─────────────────────────────────────────────────────────
print("=== Region 3: Vouvray ===")
r = R("Vouvray", "France", "wine",
      designation_type="AOC", designation_name="Vouvray AOC",
      reputation_tier="prestigious", quality_trajectory="established",
      description="Loire Valley's most versatile Chenin Blanc appellation on tuffeau limestone near Tours; produces dry (Sec), off-dry (Sec-Tendre), demi-sec, moelleux and sparkling from the same vineyards according to vintage.",
      key_producers="Huet, Foreau, François Pinon, Gaston Huet",
      historical_context="Gaston Huet's domaine (now Clos Huet) produced legendary Vouvray through the 20th century; Foreau's Clos Naudin is the other reference; Chenin's ability to produce every style from bone-dry to botrytis sweet is unique in France.")
VIN(r, 2022, "excellent", "rising", "Fine Vouvray year; Chenin of great mineral freshness; moelleux of fine concentration.")
VIN(r, 2021, "exceptional", "rising", "Outstanding vintage; dry and demi-sec Vouvray of rare precision; limited moelleux.")
VIN(r, 2020, "very_good", "stable", "Warm year; rich demi-sec and moelleux; dry Sec somewhat less classic.")
VIN(r, 2019, "excellent", "stable", "Classic profile; Vouvray across styles of consistent high quality.")
VIN(r, 2018, "excellent", "rising", "Good botrytis year; moelleux of fine concentration; dry wines of good structure.")
p1 = P("Domaine Huet", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="The historic Vouvray reference estate (Gaston Huet, now Clos Huet); three monopole vineyards — Le Haut-Lieu, Le Mont, Clos du Bourg; full biodynamic; every style from Sec to TBA.",
       reputation_narrative="Huet is Vouvray's defining estate; Le Mont Moelleux and Clos du Bourg demi-sec are Loire benchmarks; wines age for 30-50 years.",
       price_positioning="premium")
p2 = P("Clos Naudin (Foreau)", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Philippe Foreau's benchmark Clos Naudin estate; 12 hectares of old-vine Chenin; traditional vinification; wines of extraordinary consistency from sparkling to moelleux.",
       reputation_narrative="Foreau's Clos Naudin is the other Vouvray reference alongside Huet; both estates prove Chenin's ability to produce France's most versatile range of wine styles.",
       price_positioning="premium")
pr1, n1 = PROD("Domaine Huet Le Mont Sec Vouvray", "wine_still", p1, r, "France",
               subcategory="Chenin Blanc", price_tier="premium",
               description="Bone-dry Chenin Blanc from the Le Mont single vineyard on tuffeau; flint, quince, lemon oil, beeswax and a seemingly eternal mineral finish; one of France's most age-worthy dry whites.")
if n1:
    PAIR(pr1, "River pike-perch (sandre) with beurre blanc", "complement", "classic", "fish_course", "The Loire's great fish pairing; mineral-flint Vouvray Sec mirrors delicate river fish; beurre blanc bridges.")
    PAIR(pr1, "Rillettes of Tours (pork rillettes) with cornichons", "complement", "classic", "starter", "Regional Tours pairing; dry Chenin's acidity cuts pork fat; quince bridges apple notes.")
    PAIR(pr1, "Roast pork with quince and apple stuffing", "complement", "established", "main", "Quince in wine echoes stuffing; flint mineral and Chenin's body bridge pork richness.")
    PAIR(pr1, "Aged Montoire goat's cheese", "complement", "classic", "cheese", "Loire classic; dry Vouvray and aged goat's cheese are natural partners in the Touraine.")
pr2, n2 = PROD("Clos Naudin Vouvray Moelleux Réserve", "wine_dessert", p2, r, "France",
               subcategory="Chenin Blanc", price_tier="premium",
               description="Benchmark botrytis Vouvray Moelleux Réserve; extraordinary — apricot, mango, saffron, honey, beeswax and a vibrant Chenin acidity; will age for 30+ years; one of France's greatest sweet wines.")
if n2:
    PAIR(pr2, "Tarte Tatin with crème fraîche", "complement", "classic", "dessert", "Loire classic; apricot-honey Vouvray mirrors caramelised apple; acidity prevents sweetness.")
    PAIR(pr2, "Roquefort with pear and walnut", "complement", "classic", "cheese", "Loire tradition; sweet Chenin stands up to Roquefort pungency; pear bridges; walnut echoes beeswax.")
    PAIR(pr2, "Foie gras mi-cuit with mango chutney", "complement", "established", "starter", "Sweet Vouvray and foie gras: Loire's version of Sauternes-foie pairing; mango echoes wine's fruit.")
    PAIR(pr2, "Fresh peach and almond tart", "complement", "suggested", "dessert", "Apricot-mango wine suits stone fruit tart; almond in pastry echoes Chenin's almond notes.")

# ── Region 4: Coteaux du Layon ────────────────────────────────────────────────
print("=== Region 4: Coteaux du Layon ===")
r = R("Coteaux du Layon", "France", "wine",
      designation_type="AOC", designation_name="Coteaux du Layon AOC",
      reputation_tier="prestigious", quality_trajectory="rediscovering",
      description="Anjou's great sweet wine valley; Chenin Blanc affected by botrytis on south-facing schist and clay slopes of the Layon river; Quarts de Chaume Grand Cru and Bonnezeaux are the apex sub-zones.",
      key_producers="Domaine des Baumard, Château Pierre-Bise, Jo Pithon, Domaine Ogereau",
      historical_context="Quarts de Chaume (Grand Cru since 2011) is a former feudal tithe of the finest grapes; Coteaux du Layon rivals Sauternes and Mosel Auslese for great sweet wine complexity but at lower prices.")
VIN(r, 2022, "very_good", "stable", "Good botrytis conditions; Coteaux du Layon of classic apricot-honey character.")
VIN(r, 2021, "excellent", "rising", "Outstanding botrytis year; Layon Moelleux of fine concentration and Chenin acidity.")
VIN(r, 2020, "exceptional", "rising", "Benchmark botrytis vintage; Quarts de Chaume and Bonnezeaux of legendary concentration.")
VIN(r, 2019, "very_good", "stable", "Good year; accessible, food-friendly Coteaux du Layon of consistent quality.")
VIN(r, 2018, "excellent", "rising", "Excellent botrytis conditions; Layon wines of fine balance and aging potential.")
p1 = P("Château Pierre-Bise", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Claude Papin's biodynamic Anjou-Layon estate; multiple single-vineyard Coteaux du Layon from schist, clay and volcanic soils; Les Rouannières is their benchmark botrytis wine.",
       reputation_narrative="Pierre-Bise is Layon's most celebrated natural producer; Les Rouannières is one of Anjou's great botrytis Chenin Blancs.",
       price_positioning="mid_range")
p2 = P("Domaine Ogereau", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Vincent Ogereau's organic Layon estate; Saint-Lambert Coteaux du Layon from old-vine Chenin on black schist; consistent, age-worthy botrytis wines at fair prices.",
       reputation_narrative="Ogereau is one of Layon's most consistently excellent producers; Saint-Lambert is a benchmark for honest, terroir-driven Coteaux du Layon.",
       price_positioning="mid_range")
pr1, n1 = PROD("Château Pierre-Bise Les Rouannières Coteaux du Layon", "wine_dessert", p1, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Biodynamic botrytis Coteaux du Layon from schist; dried apricot, honey, saffron, Chenin beeswax and a remarkable sweet-acid balance; one of Anjou's most sought-after Layon wines.")
if n1:
    PAIR(pr1, "Foie gras de canard poêlé with quince", "complement", "classic", "starter", "Classic Anjou pairing; sweet Chenin balances foie richness; quince echoes wine's stone fruit.")
    PAIR(pr1, "Tarte aux abricots (apricot tart) with crème pâtissière", "complement", "classic", "dessert", "Apricot mirror in wine; Chenin acidity prevents cloying; beeswax bridges pastry richness.")
    PAIR(pr1, "Roquefort with dried apricots on walnut bread", "complement", "established", "cheese", "Loire sweet wine and blue cheese classic; acidity and apricot bridge Roquefort's pungency.")
    PAIR(pr1, "Almond financier with orange blossom cream", "complement", "suggested", "dessert", "Almond-saffron notes in wine echo financier; orange blossom bridges Chenin's floral quality.")
pr2, n2 = PROD("Ogereau Saint-Lambert Coteaux du Layon", "wine_dessert", p2, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Organic black schist Layon; dried apricot, quince, lemon honey and a clean sweet-acid Chenin balance; accessible, food-friendly botrytis wine of genuine quality and excellent value.")
if n2:
    PAIR(pr2, "Camembert de Normandie rôti with honey", "complement", "established", "cheese", "Warm cheese with honey mirrors wine's honey-apricot; Chenin acidity cuts melted richness.")
    PAIR(pr2, "Crème brûlée with passion fruit topping", "complement", "established", "dessert", "Apricot-quince wine suits crème brûlée; Chenin acidity balances sweet; passion fruit bridges.")
    PAIR(pr2, "Terrine de foie gras with Sauternes jelly", "complement", "classic", "starter", "Classic Loire aperitif pairing; Layon's acidity lifts foie richness; apricot echoes Sauternes note.")
    PAIR(pr2, "Strawberry pavlova with cream", "complement", "suggested", "dessert", "Off-dry sweetness bridges strawberry and meringue; quince echoes fruit; acidity refreshes cream.")

# ── Region 5: Touraine ────────────────────────────────────────────────────────
print("=== Region 5: Touraine ===")
r = R("Touraine", "France", "wine",
      designation_type="AOC", designation_name="Touraine AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Broad Loire Valley appellation around Tours; Sauvignon Blanc, Gamay, Cabernet Franc and Chenin Blanc; home of the finest value Loire wines and innovative natural wine producers.",
      key_producers="Henry Marionnet, Jacky Blot, Domaine de la Garrelière, Noëlla Morantin",
      historical_context="Touraine's appellation covers the Loire's historic heartland; Rabelais, Balzac and Descartes were born here; home of the first Grolleau and Gamay wines of quality.")
VIN(r, 2022, "very_good", "stable", "Good Loire year; Touraine Sauvignon of fine freshness; Gamay of vibrant fruit.")
VIN(r, 2021, "excellent", "stable", "Classic year; Touraine Sauvignon approaching Sancerre in quality; Gamay of depth.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer Sauvignon; generous Gamay with good structure.")
VIN(r, 2019, "excellent", "stable", "Good balance; food-friendly Touraine wines of consistent quality.")
VIN(r, 2018, "very_good", "stable", "Reliable vintage; accessible, versatile Touraine range.")
p1 = P("Henry Marionnet", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Pioneer of pre-phylloxera vines; Provignage (ungrafted Gamay) and Première Vendange are remarkable expressions; Sauvignon de Touraine from old limestone-clay vines; unique ungrafted range.",
       reputation_narrative="Henry Marionnet's ungrafted Gamay Provignage is one of France's most unusual wines; demonstrates pre-phylloxera vine character; benchmark for Touraine artisan producers.",
       price_positioning="mid_range")
p2 = P("Noëlla Morantin", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Natural wine cult producer Noëlla Morantin; biodynamic since 2002; Gamay, Menu Pineau and Côt (Malbec) from old vines; L'Art de Vivre and Monsieur are her cult natural wines.",
       reputation_narrative="Morantin is one of France's most sought-after natural wine producers; L'Art de Vivre and Mon Cher Gamay have cult status in natural wine bars worldwide.",
       price_positioning="mid_range")
pr1, n1 = PROD("Henry Marionnet Provignage Gamay Non Greffé", "wine_still", p1, r, "France",
               subcategory="Gamay", price_tier="premium",
               description="Extraordinary pre-phylloxera ungrafted Gamay from 1850s vines on sand; more structured and complex than grafted Gamay — black cherry, violet, earth and remarkable tannic presence; one of France's most historic wines.")
if n1:
    PAIR(pr1, "Andouille de Vire sausage with lentils du Berry", "complement", "classic", "main", "Loire charcuterie tradition; ungrafted Gamay's structure suits smoky andouille; lentils bridge earth.")
    PAIR(pr1, "Grilled pigeon with wild mushrooms and thyme", "complement", "established", "main", "Pre-phylloxera depth suits pigeon's gamey character; earth and cherry echo mushroom and thyme.")
    PAIR(pr1, "Duck terrine with hazelnuts and cornichons", "complement", "established", "starter", "Structured Gamay suits rich duck terrine; violet bridges duck fat; cherry echoes cornichon acidity.")
    PAIR(pr1, "Tête de moine with cumin-spiced bread", "complement", "suggested", "cheese", "Pre-phylloxera Gamay's structure suits firm Swiss cheese; cherry bridges cumin spice.")
pr2, n2 = PROD("Noëlla Morantin L'Art de Vivre Gamay", "wine_still", p2, r, "France",
               subcategory="Gamay", price_tier="mid_range",
               description="Cult natural Touraine Gamay; transparent, biodynamic; sour cherry, dried rose, wild herbs and a mineral-natural freshness; zero sulphur; among France's most sought-after natural reds.")
if n2:
    PAIR(pr2, "Charcuterie board with Touraine rillettes", "complement", "classic", "aperitif", "Loire natural wine tradition; sour cherry and rose Gamay suits pork rillettes; wild herb bridges.")
    PAIR(pr2, "Grilled red mullet with tomato and basil", "complement", "suggested", "fish_course", "Natural light red suits red mullet; dried rose bridges tomato; sour cherry mirrors basil sweetness.")
    PAIR(pr2, "Warm Valençay goat's cheese with thyme honey", "complement", "classic", "cheese", "Loire classic; natural Gamay's acidity and cherry suit tangy goat's cheese; honey bridges.")
    PAIR(pr2, "Cold chicken salad with tarragon vinaigrette", "complement", "established", "main", "Natural freshness suits cold chicken; wild herb notes echo tarragon; cherry mirrors vinaigrette tang.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
total_r = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_producers")
total_p = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_products")
total_pr = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
total_pa = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
total_v = cur.fetchone()[0]
print(f"Total regions: {total_r}")
print(f"Total producers: {total_p}")
print(f"Total products: {total_pr}")
print(f"Total pairings: {total_pa}")
print(f"Total vintages: {total_v}")
if total_pa >= 8000:
    print(f"*** MILESTONE: {total_pa} PAIRINGS — 8000+ ACHIEVED! ***")
if total_v >= 3000:
    print(f"*** MILESTONE: {total_v} VINTAGES — 3000+ ACHIEVED! ***")
print("Done.")
conn.close()
