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

# ── Region 1: Mâcon Villages ─────────────────────────────────────────────────
print("=== Region 1: Mâcon Villages ===")
r = R("Mâcon Villages", "France", "wine",
      designation_type="AOC", designation_name="Mâcon Villages AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Southern Burgundy's value Chardonnay zone; limestone and clay soils produce un-oaked, mineral Chardonnay of great food versatility; Pouilly-Fuissé, Saint-Véran and Viré-Clessé are the prestige sub-zones.",
      key_producers="Domaine de la Bongran, Domaine Valette, Domaine Bonhomme, Château de Fuissé",
      historical_context="Mâcon was Burgundy's workhorse region until a quality revolution in the 1990s; now top producers rival village-level Côte de Beaune Chardonnay at a fraction of the price.")
VIN(r, 2022, "excellent", "rising", "Classic Burgundy year; Mâcon Chardonnay of outstanding mineral freshness.")
VIN(r, 2021, "exceptional", "rising", "Benchmark vintage; Mâcon Villages and Pouilly-Fuissé of Côte de Beaune quality.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer, rounder Chardonnay; Pouilly-Fuissé excelled.")
VIN(r, 2019, "excellent", "stable", "Classic profile; mineral, food-friendly Mâcon Chardonnay.")
VIN(r, 2018, "very_good", "stable", "Good balance; accessible, approachable southern Burgundy Chardonnay.")
p1 = P("Domaine de la Bongran", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Jean Thévenet's eccentric estate; extended lees aging on un-oaked Viré-Clessé Chardonnay; Quintaine (rich, almost botrytis-style) and classic Viré-Clessé of unusual depth.",
       reputation_narrative="Bongran's Quintaine is the most eccentric and age-worthy Mâcon Chardonnay; extended lees aging creates wines of Meursault-like richness.",
       price_positioning="mid_range")
p2 = P("Château de Fuissé", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Jean-Jacques Vincent's benchmark Pouilly-Fuissé estate; Le Clos is their flagship from oldest vines; range from accessible Mâcon to prestigious single-vineyard Fuissé.",
       reputation_narrative="Fuissé is the definitive estate for Pouilly-Fuissé; Le Clos is among southern Burgundy's greatest whites.",
       price_positioning="mid_range")
pr1, n1 = PROD("Domaine de la Bongran Viré-Clessé Quintaine", "wine_still", p1, r, "France",
               subcategory="Chardonnay", price_tier="mid_range",
               description="Extended lees Chardonnay from Viré-Clessé; un-oaked but rich; honey, white peach, beeswax, lemon curd and remarkable depth; resembles minor Meursault at a fraction of the cost.")
if n1:
    PAIR(pr1, "Quenelles de brochet (pike dumplings) with Nantua sauce", "complement", "classic", "main", "Lyon-adjacent pairing; rich Chardonnay suits cream-crayfish sauce; beeswax bridges richness.")
    PAIR(pr1, "Gratin de macaroni with aged Gruyère", "complement", "classic", "main", "Burgundian comfort pairing; beeswax and lemon curd bridge aged cheese; richness suits gratin.")
    PAIR(pr1, "Roast free-range chicken with tarragon butter", "complement", "established", "main", "Classic southern Burgundy pairing; peach and beeswax notes bridge chicken and herb butter.")
    PAIR(pr1, "Époisses at perfect ripeness", "complement", "adventurous", "cheese", "Eccentric Mâcon Chardonnay suits Époisses' powerful character; beeswax bridges washed rind.")
pr2, n2 = PROD("Château de Fuissé Le Clos Pouilly-Fuissé", "wine_still", p2, r, "France",
               subcategory="Chardonnay", price_tier="premium",
               description="Flagship old-vine Pouilly-Fuissé from the Clos vineyard; barrel-fermented; white peach, hazelnut, flint mineral and a long, complex finish; one of southern Burgundy's benchmark whites.")
if n2:
    PAIR(pr2, "Sautéed frogs' legs with garlic and parsley butter", "complement", "classic", "main", "Burgundian classic; mineral hazelnut Fuissé suits delicate frogs' legs; parsley bridges herb notes.")
    PAIR(pr2, "Crottin de Chavignol au chèvre (warm goat's cheese)", "complement", "established", "starter", "Mineral Chardonnay bridges goat's cheese; hazelnut echoes warm cheese nuttiness.")
    PAIR(pr2, "Sole meunière with capers and brown butter", "complement", "established", "fish_course", "Classic pairing; mineral Fuissé suits delicate sole; brown butter bridges; capers amplify acidity.")
    PAIR(pr2, "Corn-fed chicken with morel cream sauce", "complement", "classic", "main", "Burgundy classic; hazelnut and white peach bridge morel earthiness; cream suit wine's richness.")

# ── Region 2: Meursault premier cru additions ─────────────────────────────────
print("=== Region 2: Saint-Véran ===")
r = R("Saint-Véran", "France", "wine",
      designation_type="AOC", designation_name="Saint-Véran AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Southern Mâconnais Chardonnay appellation adjacent to Pouilly-Fuissé; limestone-clay soils from volcanic and ancient hillsides; wines of mineral freshness and excellent value relative to Côte de Beaune.",
      key_producers="Roger Lassarat, Domaine des Deux Roches, Verget",
      historical_context="Saint-Véran was created in 1971 to recognise the best villages south of Pouilly-Fuissé; the name comes from Saint Vérand, a local village; wines offer Mâcon quality at Burgundy character.")
VIN(r, 2022, "excellent", "stable", "Good Mâconnais year; Saint-Véran of fine mineral freshness and food versatility.")
VIN(r, 2021, "exceptional", "rising", "Benchmark year; Saint-Véran approaching Pouilly-Fuissé in quality.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer, generous Chardonnay with good depth.")
VIN(r, 2019, "excellent", "stable", "Classic profile; crisp, mineral Saint-Véran of consistent quality.")
VIN(r, 2018, "very_good", "stable", "Good balance; accessible, food-friendly Saint-Véran.")
p1 = P("Roger Lassarat", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="The benchmark Saint-Véran producer; Cuvée Prestige and Vieilles Vignes from old Chardonnay on limestone-clay; meticulous sorting and whole-cluster pressing; consistently over-delivers.",
       reputation_narrative="Roger Lassarat makes the reference Saint-Véran; Vieilles Vignes demonstrates what the appellation can achieve with low yields and old vines.",
       price_positioning="mid_range")
p2 = P("Verget", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Jean-Marie Guffens's négociant-éleveur house; sources from finest Mâconnais parcels including Saint-Véran; barrel-fermented selections from old vines; consistency and quality-focused approach.",
       reputation_narrative="Verget's Saint-Véran selections prove that great négociant work can rival estate wines; Guffens identifies and vinifies the best Mâconnais parcels.",
       price_positioning="mid_range")
pr1, n1 = PROD("Roger Lassarat Saint-Véran Vieilles Vignes", "wine_still", p1, r, "France",
               subcategory="Chardonnay", price_tier="mid_range",
               description="Old-vine Saint-Véran from limestone-clay; mineral, precise and complex — white peach, flint, lime and a long clean finish; one of southern Burgundy's finest under-recognised Chardonnays.")
if n1:
    PAIR(pr1, "Chicken liver mousse with brioche and cornichons", "complement", "established", "starter", "Mineral Chardonnay bridges liver mousse richness; acidity cuts fat; peach echoes brioche sweetness.")
    PAIR(pr1, "Grilled turbot with beurre blanc and herbs", "complement", "established", "fish_course", "Classic pairing; flint mineral and peach suit turbot; beurre blanc bridges wine's richness.")
    PAIR(pr1, "Goat's cheese tart with cherry tomatoes", "complement", "classic", "starter", "Southern Burgundy pairing; mineral Chardonnay and goat's cheese; tomato acidity bridges.")
    PAIR(pr1, "Pan-fried chicken breast with lemon and thyme", "complement", "established", "main", "Classic bistro pairing; peach and mineral Chardonnay suit chicken; lemon bridges acidity.")
pr2, n2 = PROD("Verget Saint-Véran Terroirs de Davayé", "wine_still", p2, r, "France",
               subcategory="Chardonnay", price_tier="mid_range",
               description="Négociant-selected Saint-Véran from Davayé terroir; barrel-fermented; hazelnut, white peach, mineral chalk and a clean, Burgundy-adjacent finish; excellent value Mâconnais.")
if n2:
    PAIR(pr2, "Moules à la crème with shallots and white wine", "complement", "established", "starter", "Southern Burgundy hazelnut-mineral suits mussel cream sauce; wine echoes the cooking liquid.")
    PAIR(pr2, "Warm salad of scallops with hazelnut dressing", "complement", "established", "starter", "Hazelnut in wine echoes dressing; mineral suits scallop sweetness; peach bridges cream.")
    PAIR(pr2, "Omelette aux champignons de Paris", "complement", "classic", "main", "Bistro classic; Chardonnay and mushroom omelette: mineral bridges egg richness; peach echoes mushroom.")
    PAIR(pr2, "Steamed fish dumplings with ginger broth", "complement", "adventurous", "starter", "Mineral Chardonnay bridges delicate fish dumpling; hazelnut echoes toasted sesame; acidity refreshes.")

# ── Region 3: Cava Paraje Calificado — Xarel·lo apex ────────────────────────
print("=== Region 3: Crémant d'Alsace ===")
r = R("Crémant d'Alsace", "France", "wine",
      designation_type="AOC", designation_name="Crémant d'Alsace AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Alsace's traditional method sparkling wine; Pinot Blanc, Auxerrois, Pinot Gris, Riesling and Pinot Noir; France's second-largest Crémant production after Alsace; wines of freshness, floral charm and value.",
      key_producers="Dopff au Moulin, Lucien Albrecht, Wolfberger, Gustave Lorentz",
      historical_context="Dopff au Moulin introduced the méthode champenoise to Alsace after visiting Épernay in 1900; Crémant d'Alsace AOC established 1976; produces 45 million bottles annually.")
VIN(r, 2022, "excellent", "stable", "Good Alsace year; Crémant of fine aromatic freshness and clean acidity.")
VIN(r, 2021, "very_good", "stable", "Classic Alsace profile; floral, food-friendly Crémant of consistent quality.")
VIN(r, 2020, "excellent", "stable", "Warm year; richer Crémant with Pinot Blanc depth and good mousse.")
VIN(r, 2019, "very_good", "stable", "Balanced year; Crémant d'Alsace at its most food-versatile.")
VIN(r, 2018, "very_good", "stable", "Good sparkling base; accessible Crémant of typical Alsace floral character.")
p1 = P("Dopff au Moulin", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The founding estate of Alsace sparkling wine; Cuvée Bartholdi and Blanc de Blancs are their prestige wines; Riesling Brut vintage and Pinot Noir Rosé Brut also produced.",
       reputation_narrative="Dopff au Moulin is the historical foundation of Alsace sparkling wine; Cuvée Bartholdi is the benchmark traditional Crémant d'Alsace.",
       price_positioning="mid_range")
p2 = P("Lucien Albrecht", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Family estate producing benchmark Crémant d'Alsace Blanc de Blancs from Auxerrois; extended lees aging (24+ months); consistently the appellation's most awarded producer.",
       reputation_narrative="Lucien Albrecht's Blanc de Blancs is considered the finest Crémant d'Alsace regularly available; precise, fresh and food-friendly.",
       price_positioning="mid_range")
pr1, n1 = PROD("Dopff au Moulin Cuvée Bartholdi Brut Crémant d'Alsace", "wine_sparkling", p1, r, "France",
               subcategory="Pinot Blanc blend", price_tier="mid_range",
               description="The classic Crémant d'Alsace; Pinot Blanc-dominant with Auxerrois and Riesling; apple blossom, citrus, white peach and fine persistent mousse; remarkable value and food versatility.")
if n1:
    PAIR(pr1, "Choucroute garnie avec saucisses alsaciennes", "complement", "classic", "main", "Definitive Alsace pairing; Crémant's mousse and acidity cut sauerkraut fat; apple bridges.")
    PAIR(pr1, "Flammekueche (tarte flambée) with bacon and onion", "complement", "classic", "main", "Alsace wine bar staple; fine bubbles lift cream and bacon; apple blossom bridges onion.")
    PAIR(pr1, "Munster cheese with caraway seeds", "complement", "classic", "cheese", "Classic Alsace pairing; Crémant's freshness and bubbles suit Munster's strong character.")
    PAIR(pr1, "Smoked salmon blinis with crème fraîche and dill", "complement", "established", "starter", "Fine mousse suits smoked salmon; apple blossom bridges dill; acidity cuts richness.")
pr2, n2 = PROD("Lucien Albrecht Blanc de Blancs Brut Crémant d'Alsace", "wine_sparkling", p2, r, "France",
               subcategory="Auxerrois", price_tier="mid_range",
               description="24-month-lees Auxerrois Blanc de Blancs; pure, floral and mineral — white flower, green apple, brioche and a fine, persistent mousse; the appellation's most elegant expression.")
if n2:
    PAIR(pr2, "Foie gras d'Alsace mi-cuit with Gewurz reduction", "complement", "classic", "starter", "Alsace aperitif pairing; Crémant's mousse and acidity balance foie richness; brioche bridges.")
    PAIR(pr2, "Gratin de queues d'écrevisses (crayfish gratin)", "complement", "established", "main", "Alsace classic; fine mousse and mineral white flower suit delicate crayfish cream.")
    PAIR(pr2, "Light summer vegetable quiche with Gruyère", "complement", "established", "main", "Bistro pairing; Crémant's light mousse suits vegetable quiche; mineral bridges cheese.")
    PAIR(pr2, "Fresh Alsatian Munster with walnuts", "complement", "established", "cheese", "Crémant's freshness cuts young Munster; white flower and green apple bridge dairy.")

# ── Region 4: Crémant de Bourgogne ─────────────────────────────────────────
print("=== Region 4: Crémant de Bourgogne ===")
r = R("Crémant de Bourgogne", "France", "wine",
      designation_type="AOC", designation_name="Crémant de Bourgogne AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Burgundy's traditional method sparkling wine; Chardonnay, Pinot Noir and Aligoté from across the region; wines of good depth and Burgundian character; exceptional value relative to Champagne.",
      key_producers="Caves de Bailly, Louis Bouillot, Veuve Ambal, Domaine Parigot",
      historical_context="Crémant de Bourgogne was created in 1975 to provide an outlet for Burgundy's rejected grapes; now includes top-quality grapes producing serious sparkling wines.")
VIN(r, 2022, "excellent", "stable", "Classic Burgundy year; Chardonnay-based Crémant of fine mineral freshness.")
VIN(r, 2021, "exceptional", "rising", "Benchmark vintage; Crémant de Bourgogne of outstanding Chardonnay quality.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer Crémant style with peach and brioche depth.")
VIN(r, 2019, "excellent", "stable", "Good balance; food-friendly Crémant with mineral Burgundy character.")
VIN(r, 2018, "very_good", "stable", "Consistent quality; accessible, approachable Crémant de Bourgogne.")
p1 = P("Caves de Bailly", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Large cooperative cave carved in rock near Saint-Bris; 6 million bottles aged underground; Pinot Noir Blanc de Noirs is their most distinctive; diverse Chardonnay expressions.",
       reputation_narrative="Caves de Bailly is the most important Crémant de Bourgogne producer; their caves beneath Auxerre produce wines of consistent quality and excellent value.",
       price_positioning="value")
p2 = P("Domaine Parigot", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Small family estate producing estate-grown Crémant de Bourgogne; Pinot Noir Rosé Brut and Blanc de Blancs from Côte d'Or and Mâconnais; certified sustainable.",
       reputation_narrative="Parigot produces some of the finest estate-grown Crémant de Bourgogne; their Rosé Brut is considered among the denomination's most elegant expressions.",
       price_positioning="mid_range")
pr1, n1 = PROD("Caves de Bailly Blanc de Noirs Brut Crémant de Bourgogne", "wine_sparkling", p1, r, "France",
               subcategory="Pinot Noir", price_tier="value",
               description="100% Pinot Noir Blanc de Noirs; salmon-tinged, structured and food-friendly; red berry, brioche, chalk and a creamy mousse; one of France's best value Blanc de Noirs sparkling wines.")
if n1:
    PAIR(pr1, "Jambon persillé de Bourgogne (parsley ham terrine)", "complement", "classic", "starter", "Burgundy regional pairing; Blanc de Noirs structure suits ham terrine; red berry bridges parsley.")
    PAIR(pr1, "Grilled salmon with tarragon hollandaise", "complement", "established", "fish_course", "Blanc de Noirs red fruit bridges salmon richness; brioche suits hollandaise; tarragon echoes herbs.")
    PAIR(pr1, "Escargots de Bourgogne with garlic butter", "complement", "classic", "starter", "Burgundy classic; Blanc de Noirs structure cuts garlic butter; red berry bridges snail earthiness.")
    PAIR(pr1, "Duck rillettes with cornichons", "complement", "established", "aperitif", "Red fruit and brioche Crémant suits duck pâté; cornichons bridge wine's acidity.")
pr2, n2 = PROD("Domaine Parigot Rosé Brut Crémant de Bourgogne", "wine_sparkling", p2, r, "France",
               subcategory="Pinot Noir rosé", price_tier="mid_range",
               description="Estate Pinot Noir Rosé Brut; salmon-pink, precise and elegant — wild strawberry, raspberry, brioche and a fine persistent mousse; benchmark estate Crémant de Bourgogne rosé.")
if n2:
    PAIR(pr2, "Gravlax with cucumber and mustard-dill sauce", "complement", "established", "starter", "Rosé Crémant bridges cured salmon; wild strawberry echoes cucumber sweetness; fine mousse refreshes.")
    PAIR(pr2, "Duck magret salad with raspberries and walnuts", "complement", "established", "starter", "Raspberry in wine echoes salad; Pinot Noir structure suits duck; walnuts bridge bitterness.")
    PAIR(pr2, "Strawberry tart with crème pâtissière", "complement", "classic", "dessert", "Wild strawberry Crémant suits strawberry tart; mousse bridges cream richness; raspberry adds.")
    PAIR(pr2, "Salade lyonnaise with lardons and soft egg", "complement", "classic", "starter", "Lyon tradition; Rosé Crémant suits bitter greens, lardons and soft egg; red fruit bridges.")

# ── Region 5: Sparkling — Saumur Brut ────────────────────────────────────────
print("=== Region 5: Saumur ===")
r = R("Saumur", "France", "wine",
      designation_type="AOC", designation_name="Saumur AOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Loire Valley tuffeau limestone appellation; Cabernet Franc reds and Chenin Blanc whites; Saumur Brut (traditional method sparkling from Chenin) is one of France's most overlooked fine sparkling wines.",
      key_producers="Bouvet-Ladubay, Langlois-Château, Domaine des Roches Neuves, Château du Hureau",
      historical_context="Ackerman-Laurance created the first Loire sparkling wine in 1811 in Saumur; the tuffeau caves (60km of tunnels) provide ideal aging conditions; Saumur Brut predates Champagne's mass production.")
VIN(r, 2022, "excellent", "stable", "Good Loire year; Chenin Blanc of fine acidity ideal for Saumur Brut base wines.")
VIN(r, 2021, "exceptional", "rising", "Outstanding Chenin vintage; Saumur Brut wines of extraordinary mineral precision.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer Saumur style; tuffeau Cabernet Franc reds excelled.")
VIN(r, 2019, "excellent", "stable", "Classic profile; precise Chenin and structured Cabernet Franc reds.")
VIN(r, 2018, "very_good", "stable", "Good balance; food-friendly Saumur wines of consistent quality.")
p1 = P("Bouvet-Ladubay", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The historic Saumur sparkling house (1851); aged in tuffeau caves; Trésor prestige Brut (extended aging) and Excellence vintage-dated Chenin are their top wines.",
       reputation_narrative="Bouvet-Ladubay established Saumur as a serious sparkling wine destination; Trésor is the finest regularly available Saumur Brut.",
       price_positioning="mid_range")
p2 = P("Langlois-Château", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Saumur house owned by Bollinger (Champagne); Bollinger's expertise applied to Chenin-based Saumur Brut; Quadrille and Old Reserve aged up to 10 years in tuffeau caves.",
       reputation_narrative="Bollinger ownership elevated Langlois-Château to produce some of Saumur's most serious sparkling wines; Old Reserve is the denomination's cult wine.",
       price_positioning="mid_range")
pr1, n1 = PROD("Bouvet-Ladubay Trésor Brut Saumur", "wine_sparkling", p1, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Extended-aging Saumur Brut from Chenin Blanc; tuffeau mineral, honey, apple blossom and brioche with a persistent, fine mousse; the finest traditional Saumur Brut at an accessible price.")
if n1:
    PAIR(pr1, "Rillons de Tours with cornichons and mustard", "complement", "classic", "starter", "Loire regional pairing; Chenin Brut's mousse and honey cut rich pork belly confit.")
    PAIR(pr1, "Steamed Breton lobster with herb butter", "complement", "established", "fish_course", "Chenin's honey-mineral suits lobster sweetness; tuffeau bridges butter sauce richness.")
    PAIR(pr1, "Grilled sardines with lemon and sea salt", "complement", "established", "starter", "Chenin acidity cuts sardine oil; tuffeau mineral mirrors sea character; apple blossom bridges.")
    PAIR(pr1, "Soft-ripened Brillat-Savarin with brioche", "complement", "established", "cheese", "Honey and brioche in wine echo Brillat-Savarin's triple cream; mousse cuts richness.")
pr2, n2 = PROD("Langlois-Château Quadrille Brut Saumur", "wine_sparkling", p2, r, "France",
               subcategory="Chenin Blanc", price_tier="mid_range",
               description="Bollinger-influenced Saumur Brut; Chenin Blanc with extended tuffeau cave aging; chalk, apple, lemon and fine mousse; precise, mineral and more structured than typical Saumur Brut.")
if n2:
    PAIR(pr2, "Oysters with lemon and mignonette", "complement", "classic", "aperitif", "Tuffeau mineral and Chenin acidity suit oysters; fine mousse mirrors brine; citrus echoes lemon.")
    PAIR(pr2, "Whitebait fritters with lemon and tartare sauce", "complement", "established", "starter", "Fine mousse and acidity suit fried fish; chalk mineral bridges tartare; lemon amplifies.")
    PAIR(pr2, "Asparagus velouté with crème fraîche", "complement", "established", "starter", "Chenin and asparagus are a Loire classic; chalk mineral suits velouté; honey bridges cream.")
    PAIR(pr2, "Warm goat's cheese salad with walnuts", "complement", "classic", "starter", "Loire classic; Chenin-based sparkling and goat's cheese; walnut bridges mineral chalk.")

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
    print(f"*** MILESTONE: {total_pa} PAIRINGS — 8000 ACHIEVED! ***")
if total_v >= 3000:
    print(f"*** MILESTONE: {total_v} VINTAGES — 3000 ACHIEVED! ***")
print("Done.")
conn.close()
