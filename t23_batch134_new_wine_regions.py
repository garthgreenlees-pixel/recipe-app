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

# ── B134 ──────────────────────────────────────────────────────────────────────
# Targets: Franken (Germany), Mittelburgenland DAC (Austria),
#          Pic Saint-Loup AOC (France), Faugères AOC (France),
#          Cannonau di Sardegna DOC (Italy)

# 1. FRANKEN — Germany
print("=== Franken ===")
r1 = R("Franken", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Franken",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Bavaria's wine region centered on the Main river around Würzburg; famous for the distinctive flat Bocksbeutel bottle and Silvaner — Germany's most underrated white grape. Muschelkalk (fossil-rich limestone) and Keuper (clay-rich red sandstone) soils give Franken Silvaner its earthy, mineral character distinct from all other German wine. Also produces excellent Riesling, Müller-Thurgau, and red Spätburgunder (Pinot Noir). The Würzburger Stein is one of Germany's greatest single vineyards.",
        key_producers="Bürgerspital Würzburg, Juliusspital, Weingut Rainer Sauer, Rudolf Fürst",
        historical_context="Franken was among Germany's most important wine regions in the Middle Ages; Würzburg's three great charitable estates (Bürgerspital, Juliusspital, Neumünster) date to the 14th-16th centuries. The distinctive flat Bocksbeutel bottle is legally protected and unique to Franken and a few Portuguese regions. Silvaner was once Germany's most planted variety; Franken is now its spiritual home. Rudolf Fürst produces Franken's most acclaimed Spätburgunder (Pinot Noir).")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Excellent warm year; Silvaner shows earthy minerality and good concentration; Riesling also exceptional"),
    (2019, "very_good", "rising", "Good growing season; Franken Silvaner shows its characteristic muschelkalk mineral depth; fresh and food-friendly"),
    (2020, "excellent", "rising", "Excellent; Silvaner from fossil limestone shows profound mineral character; late harvest varieties exceptional"),
    (2021, "very_good", "rising", "Good year; Main river influence moderated summer heat; Silvaner precise and mineral; Riesling elegant"),
    (2022, "excellent", "stable", "Warm conditions; Silvaner achieves unusual richness; keuper soils particularly expressive; exceptional Spätburgunder"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Bürgerspital zum Heiligen Geist", "winery", r1, "Germany",
        production_philosophy="traditional",
        philosophy_description="One of Germany's oldest charitable wine estates; founded 1316; 130 hectares across Franken's best sites including Würzburger Stein; produces benchmark Silvaner and Riesling in the Bocksbeutel tradition.",
        reputation_narrative="The oldest and most historic Franken estate; Bürgerspital's Würzburger Stein Silvaner is one of Germany's most distinguished white wines; profits support hospital care as they have for 700 years.",
        price_positioning="premium")

pr1a1, n = PROD("Bürgerspital Würzburger Stein Silvaner Franken", "wine_still", p1a, r1, "Germany",
    subcategory="Silvaner single vineyard", price_tier="premium",
    description="Benchmark Franken Silvaner from the famous Stein site on muschelkalk limestone; earthy mineral, white vegetables, citrus, herbal depth; full body; Germany's greatest Silvaner expression; ages magnificently.")
if n:
    PAIR(pr1a1, "White asparagus (Spargel) with hollandaise and ham", "complement", "classic", "starter", "The definitive Franken Silvaner pairing; white asparagus season; earthy Silvaner echoes asparagus mineral depth")
    PAIR(pr1a1, "Grilled river trout with dill and lemon butter", "complement", "classic", "fish_course", "Bavarian freshwater fish tradition; Silvaner's mineral depth suits trout; dill echoes herbal notes; lemon bridges")
    PAIR(pr1a1, "Bratwurst with sauerkraut and mustard", "complement", "classic", "main", "Franconian classic; Silvaner's earthiness complements pork sausage; sauerkraut acidity mirrors wine's freshness")
    PAIR(pr1a1, "Zwiebelkuchen (Franconian onion tart)", "complement", "classic", "starter", "Traditional Franken autumn dish; Silvaner's earthy depth bridges the caramelized onion; herbal notes echo")

pr1a2, n = PROD("Bürgerspital Würzburger Stein Riesling Spätlese", "wine_still", p1a, r1, "Germany",
    subcategory="Riesling Spätlese", price_tier="premium",
    description="Spätlese Riesling from the legendary Würzburger Stein; lime, slate mineral, slight off-dry sweetness; less austere than Mosel; shows Franken's limestone character through a different lens.")
if n:
    PAIR(pr1a2, "Freshwater crayfish bisque with cream", "complement", "classic", "starter", "Bavarian river crayfish; Riesling's lime and mineral suit the delicate bisque; cream balanced by wine's acidity")
    PAIR(pr1a2, "Roasted pork with caraway and potato dumplings", "complement", "classic", "main", "Traditional Bavarian roast; Spätlese's sweetness handles the caraway spice; potato dumplings grounded by mineral")
    PAIR(pr1a2, "Asian-spiced duck salad with citrus dressing", "complement", "established", "starter", "Riesling's versatility shines; spice notes meet the Spätlese's sweetness; citrus bridges the duck richness")
    PAIR(pr1a2, "Obatzda (Bavarian spiced cheese) with pretzels", "complement", "classic", "amuse", "Traditional Bavarian cheese spread; Riesling's sweetness and acidity handle the pungent paprika-spiced cheese")

p1b = P("Rudolf Fürst", "winery", r1, "Germany",
        production_philosophy="biodynamic",
        philosophy_description="Franken's most acclaimed red wine producer; Paul Fürst's Spätburgunder (Pinot Noir) from Bürgstadter Berg is biodynamically farmed; arguably Germany's finest Pinot Noir outside of Baden.",
        reputation_narrative="The producer who put Franken Pinot Noir on the map; Rudolf Fürst's Centgrafenberg Spätburgunder is one of Germany's most collected and critically acclaimed red wines.",
        price_positioning="ultra_premium")

pr1b1, n = PROD("Rudolf Fürst Centgrafenberg Spätburgunder Franken", "wine_still", p1b, r1, "Germany",
    subcategory="Spätburgunder single vineyard", price_tier="ultra_premium",
    description="Benchmark Franken Pinot Noir from Bürgstadter Centgrafenberg on Buntsandstein sandstone; red cherry, forest floor, spice, fine mineral; Burgundian elegance with German precision; one of Germany's finest reds.")
if n:
    PAIR(pr1b1, "Roasted wild duck with red cabbage and dumplings", "complement", "classic", "main", "Traditional Franconian game preparation; Spätburgunder's elegance suits duck; red cabbage's sweet-sour mirrors acidity")
    PAIR(pr1b1, "Grilled venison loin with lingonberry and mushroom", "complement", "classic", "main", "Bavarian game; Pinot's forest floor echoes wild mushroom; lingonberry mirrors wine's red fruit; perfect match")
    PAIR(pr1b1, "Sauerkraut-braised pork cheek with caraway potatoes", "complement", "established", "main", "Franconian tradition with game variety; Spätburgunder's freshness cuts the braised richness; spice bridges")
    PAIR(pr1b1, "Aged Allgäuer Bergkäse with sourdough bread", "complement", "established", "cheese", "Bavarian mountain cheese; Pinot's acidity and red fruit balance the nutty fat; sourdough bridges")

pr1b2, n = PROD("Rudolf Fürst Klingenberger Spätburgunder Franken", "wine_still", p1b, r1, "Germany",
    subcategory="Spätburgunder", price_tier="premium",
    description="Village-level Spätburgunder from Klingenberg on red sandstone; more accessible than Centgrafenberg; red cherry, earthy spice, fine tannins; excellent introduction to Fürst's style.")
if n:
    PAIR(pr1b2, "Rouladen (German beef roll with mustard and pickles)", "complement", "classic", "main", "Classic German braise; Spätburgunder's acidity cuts the richness; pickles bridge; mustard echoes wine's spice")
    PAIR(pr1b2, "Chicken schnitzel with lemon and potato salad", "complement", "established", "main", "Lighter German classic; Pinot's freshness suits schnitzel; lemon echoes wine's acidity; potato salad bridges")
    PAIR(pr1b2, "Mushroom ragout with Franconian bread dumplings", "complement", "established", "main", "Earthy preparation; Spätburgunder's forest floor bridges; dumplings absorb the wine's tannin perfectly")
    PAIR(pr1b2, "Camembert with lingonberry jam", "complement", "established", "cheese", "Soft cheese with berry; Pinot's fruit mirrors lingonberry; wine's freshness cuts the Camembert fat")

# 2. MITTELBURGENLAND DAC — Austria
print("=== Mittelburgenland DAC ===")
r2 = R("Mittelburgenland DAC", "Austria", "wine",
        designation_type="DAC",
        designation_name="Mittelburgenland DAC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Austria's premier red wine DAC in the central Burgenland; Blaufränkisch from iron-rich clay soils produces intense, spicy reds with dark cherry, violets, white pepper, and mineral depth. The variety is identical to Germany's Lemberger and Slovakia's Frankovka; in Mittelburgenland it achieves its greatest expression. Pannobile producers (voluntary quality group) set the standard; wines age 10-20+ years.",
        key_producers="Weingut Moric, Ernst Triebaumer, Hans Igler, Pöckl",
        historical_context="Mittelburgenland received DAC status in 2005, one of Austria's first. Blaufränkisch has deep roots in the region dating to medieval times; the iron-rich Eisenberg soils produce distinctively mineral wines. Roland Velich's Moric label (focusing on old vine Blaufränkisch) brought international attention in the early 2000s. The Pannobile voluntary quality group established by Umathum, Moric and others set strict quality standards before DAC regulations.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Warm year; Blaufränkisch shows unusual concentration; iron mineral well-expressed; structured aging wines"),
    (2019, "excellent", "rising", "Excellent vintage; classic Blaufränkisch with dark cherry, pepper and iron mineral; elegant and structured"),
    (2020, "very_good", "rising", "Good growing season; Pannonian influence balanced by iron soils; Blaufränkisch fragrant and precise"),
    (2021, "exceptional", "rising", "Exceptional Mittelburgenland vintage; Blaufränkisch shows extraordinary depth; landmark wines produced"),
    (2022, "excellent", "rising", "Excellent; warm conditions with good final freshness; old vine Blaufränkisch concentrated and complex"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Weingut Moric", "winery", r2, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="Roland Velich's project focusing exclusively on old vine Blaufränkisch from Burgenland; Neckenmarkt and Lutzmannsburg single-vineyard wines show what the variety can achieve; minimal intervention.",
        reputation_narrative="The producer who transformed Blaufränkisch's international reputation; Moric's old vine single-vineyard wines (particularly Lutzmannsburg) are among Austria's most collected and critically acclaimed reds.",
        price_positioning="ultra_premium")

pr2a1, n = PROD("Moric Lutzmannsburg Alte Reben Blaufränkisch", "wine_still", p2a, r2, "Austria",
    subcategory="Blaufränkisch old vine single vineyard", price_tier="ultra_premium",
    description="Old vine Blaufränkisch from Lutzmannsburg on iron-rich clay; extraordinary concentration; dark cherry, violets, iron mineral, white pepper, graphite; immense aging potential; one of Austria's greatest reds.")
if n:
    PAIR(pr2a1, "Grilled Mangalica pork (Hungarian heritage breed) with wild herbs", "complement", "classic", "main", "Pannonian tradition; Mangalica's fat tames Blaufränkisch's tannin; wild herbs echo wine's herbal mineral depth")
    PAIR(pr2a1, "Wild boar gulasch with spicy paprika and sour cream", "complement", "classic", "main", "Central European game classic; Blaufränkisch's iron and pepper bridge the paprika; sour cream tames the spice")
    PAIR(pr2a1, "Aged Bergkäse with caraway and rye bread", "complement", "established", "cheese", "Austrian mountain cheese; Blaufränkisch's acidity and mineral depth suit the aged fat; caraway echoes wine's spice")
    PAIR(pr2a1, "Venison ragù with Kasnudeln (cheese pasta)", "complement", "established", "main", "Austrian game pasta; Blaufränkisch's iron and cherry bridge the venison richness; cheese pasta balances tannin")

pr2a2, n = PROD("Moric Burgenland Blaufränkisch", "wine_still", p2a, r2, "Austria",
    subcategory="Blaufränkisch", price_tier="premium",
    description="Entry Moric Blaufränkisch from younger vines across Burgenland; vibrant red cherry, pepper, iron mineral; fresh and expressive; excellent introduction to the house's philosophy and the variety's character.")
if n:
    PAIR(pr2a2, "Wiener Schnitzel with potato salad and lemon", "complement", "established", "main", "Austrian classic; Blaufränkisch's freshness and iron mineral cut the breaded veal; lemon echoes acidity")
    PAIR(pr2a2, "Tafelspitz (boiled beef) with horseradish and spinach", "complement", "classic", "main", "Vienna's most famous dish; Blaufränkisch's pepper and cherry bridge; horseradish heat meets wine's spice")
    PAIR(pr2a2, "Grilled lamb with eggplant and yoghurt", "complement", "established", "main", "Eastern European influence; Blaufränkisch's dark cherry suits lamb; eggplant bridges the earthy mineral depth")
    PAIR(pr2a2, "Liptauer (spiced Austrian cheese) with rye bread", "complement", "classic", "amuse", "Traditional Austrian cheese spread; Blaufränkisch's acidity cuts the pungent paprika-spiced cheese; pepper bridge")

p2b = P("Ernst Triebaumer", "winery", r2, "Austria",
        production_philosophy="traditional",
        philosophy_description="Historic Rust estate with old vine Blaufränkisch; Mariental single vineyard is one of Burgenland's most prestigious; traditional winemaking with moderate intervention.",
        reputation_narrative="One of Burgenland's founding quality producers; Triebaumer's Mariental Blaufränkisch has been a reference wine for the region since the 1980s and showed the variety's international potential.",
        price_positioning="premium")

pr2b1, n = PROD("Ernst Triebaumer Mariental Blaufränkisch", "wine_still", p2b, r2, "Austria",
    subcategory="Blaufränkisch single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Blaufränkisch from the prestigious Mariental site; dark cherry, iron, white pepper, violets; structured tannins; classic Burgenland expression of great elegance and aging potential.")
if n:
    PAIR(pr2b1, "Roast venison with red cabbage and bread dumplings", "complement", "classic", "main", "Austrian hunting tradition; Blaufränkisch's game affinity; red cabbage sweet-sour mirrors wine's fruit acidity")
    PAIR(pr2b1, "Paprikáš csirke (Hungarian chicken paprikash)", "complement", "established", "main", "Pannonian classic; Blaufränkisch's pepper echoes paprika; cream bridges tannin; regional border crossing")
    PAIR(pr2b1, "Grilled beef entrecôte with herb butter", "complement", "established", "main", "Premium beef; Mariental's structure handles the richness; herb butter bridges wine's pepper and cherry notes")
    PAIR(pr2b1, "Aged Gruyère with walnut bread and grape must", "complement", "established", "cheese", "Alpine cheese with Pannonian wine; walnut bridges Blaufränkisch's mineral depth; grape must echoes cherry")

pr2b2, n = PROD("Ernst Triebaumer Blaufränkisch Mittleburgenland", "wine_still", p2b, r2, "Austria",
    subcategory="Blaufränkisch", price_tier="mid_range",
    description="Estate Blaufränkisch showing the regional character; fresh cherry, spice, iron mineral; lighter style with good acidity; excellent everyday Austrian red wine.")
if n:
    PAIR(pr2b2, "Gulasch mit Semmelknödel (beef goulash with bread dumplings)", "complement", "classic", "main", "Austrian comfort classic; Blaufränkisch's pepper echoes paprika spice; dumplings absorb tannin; tradition")
    PAIR(pr2b2, "Käsekrainer (cheese-stuffed sausage) with mustard", "complement", "classic", "main", "Viennese street food classic; Blaufränkisch's freshness cuts the cheese fat; mustard bridges spice notes")
    PAIR(pr2b2, "Esterhazy torte with almond cream", "contrast", "adventurous", "dessert", "Rich Austrian cake; Blaufränkisch's cherry fruit and acidity create interesting contrast; unusual but Austrian")
    PAIR(pr2b2, "Grilled chicken with roasted peppers", "complement", "established", "main", "Simple preparation; Blaufränkisch's fresh acidity suits poultry; peppers' sweetness bridges wine's cherry character")

# 3. PIC SAINT-LOUP AOC — Languedoc, France
print("=== Pic Saint-Loup AOC ===")
r3 = R("Pic Saint-Loup AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Pic Saint-Loup AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Languedoc's most dynamic and respected AOC at the foot of the dramatic Pic Saint-Loup mountain north of Montpellier; limestone soils at 150-400m altitude; Syrah and Grenache dominant for reds and rosés; the altitude and north-facing slopes provide freshness unusual in southern French wine. Considered the appellation that best represents Languedoc's potential for elegant, age-worthy reds.",
        key_producers="Mas Mortiès, Clos Marie, Château de Cazeneuve, Domaine de l'Hortus",
        historical_context="Pic Saint-Loup became its own AOC in 2017 (having been a sub-appellation of Coteaux du Languedoc previously). The limestone massif creates a unique microclimate with cool nights preserving freshness; north-facing slopes receive less direct sun than typical Languedoc. Domaine de l'Hortus established the region's fine wine reputation in the 1990s; the dramatic backdrop of the Pic itself attracts wine tourism.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm year; Syrah and Grenache achieve full ripeness; intense dark fruit with freshness from altitude"),
    (2019, "very_good", "rising", "Good growing season; limestone mineral well-expressed; Syrah shows pepper and violet; elegant reds"),
    (2020, "excellent", "rising", "Excellent; altitude freshness perfectly balanced ripeness; benchmark Pic Saint-Loup vintage"),
    (2021, "very_good", "rising", "Good year; cool north-facing vineyards; Syrah shows precision; Grenache fragrant; good food wines"),
    (2022, "excellent", "stable", "Warm conditions; altitude moderated; Syrah and Grenache both successful; structured wines with depth"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine de l'Hortus", "winery", r3, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The founding estate that created Pic Saint-Loup's fine wine identity; Jean Orliac's limestone plateau vineyards beneath the Pic produce Languedoc's most elegant Syrah-Grenache blends.",
        reputation_narrative="The producer who established Pic Saint-Loup as Languedoc's premier appellation; Domaine de l'Hortus's Grande Cuvée changed perceptions of southern French wine in the 1990s and triggered the region's quality revolution.",
        price_positioning="premium")

pr3a1, n = PROD("Domaine de l'Hortus Grande Cuvée Pic Saint-Loup", "wine_still", p3a, r3, "France",
    subcategory="Syrah Grenache", price_tier="premium",
    description="The benchmark Pic Saint-Loup red; Syrah and Grenache from limestone plateau beneath the Pic; dark cherry, garrigue, pepper, violets; fresh and structured; shows Languedoc can produce elegant age-worthy reds.")
if n:
    PAIR(pr3a1, "Côte d'agneau grillée with herbs de Provence", "complement", "classic", "main", "Classic Languedoc pairing; limestone Syrah's garrigue echoes Provençal herbs; lamb fat tamed by wine's structure")
    PAIR(pr3a1, "Wild boar terrine with cornichons and mustard", "complement", "established", "starter", "Regional game charcuterie; Pic Saint-Loup's structure handles the richness; garrigue notes echo wild herbs")
    PAIR(pr3a1, "Grilled magret de canard with fig compote", "complement", "classic", "main", "Duck and Languedoc Syrah; fig bridges the dark fruit; garrigue notes in wine echo duck's wild character")
    PAIR(pr3a1, "Roquefort with walnut bread", "complement", "established", "cheese", "Strong blue cheese; Grande Cuvée's structure can handle it; walnut bridges wine's earthy Syrah notes")

pr3a2, n = PROD("Domaine de l'Hortus Pic Saint-Loup Classique", "wine_still", p3a, r3, "France",
    subcategory="Syrah Grenache Mourvèdre", price_tier="mid_range",
    description="Entry Pic Saint-Loup from l'Hortus; garrigue, red cherry, pepper; lighter and more approachable than Grande Cuvée; excellent everyday Languedoc red showing the region's character.")
if n:
    PAIR(pr3a2, "Grilled merguez with couscous and harissa", "complement", "classic", "main", "North African-Southern French fusion; Languedoc red suits spiced sausage; garrigue bridges the harissa")
    PAIR(pr3a2, "Tapenade and anchoiade with crudités", "complement", "established", "aperitif", "Provençal aperitif spread; Pic Saint-Loup's mineral freshness refreshes; olive echoes wine's garrigue notes")
    PAIR(pr3a2, "Pizza with sausage, olives, and peppers", "complement", "established", "main", "Mediterranean flavours; Classique's garrigue bridges the olive and herbs; sausage fat handled by acidity")
    PAIR(pr3a2, "Ratatouille with grilled polenta", "complement", "established", "main", "Classic Provençal vegetable stew; garrigue in wine echoes the herbs; polenta's neutral richness grounded by tannin")

p3b = P("Clos Marie", "winery", r3, "France",
        production_philosophy="biodynamic",
        philosophy_description="Small biodynamic producer on steep limestone terraces; Christophe Peyrus makes intense, concentrated Pic Saint-Loup with minimal intervention; Manon is the flagship.",
        reputation_narrative="One of Pic Saint-Loup's most acclaimed artisan producers; Clos Marie's biodynamic approach and steep limestone terraces produce wines of intensity and mineral precision unusual in Languedoc.",
        price_positioning="ultra_premium")

pr3b1, n = PROD("Clos Marie Manon Pic Saint-Loup", "wine_still", p3b, r3, "France",
    subcategory="Syrah Grenache single parcel", price_tier="ultra_premium",
    description="Flagship Pic Saint-Loup from steep biodynamic terraces; intense dark cherry, garrigue, graphite, violet; concentrated but structured; one of Languedoc's most compelling individual wines.")
if n:
    PAIR(pr3b1, "Daube provençale (Provençal beef stew with olives)", "complement", "classic", "main", "Classic Languedoc braise; Manon's concentration handled by slow-cooked collagen; olives echo garrigue notes")
    PAIR(pr3b1, "Grilled Camargue bull steak with herb butter", "complement", "classic", "main", "Regional tradition; Camargue bull's intensity tamed by Manon's structure; herb butter bridges garrigue notes")
    PAIR(pr3b1, "Aged Pélardon goat cheese with honey", "complement", "established", "cheese", "Languedoc goat cheese; Manon's concentration balanced by acidity; honey bridges wine's dark fruit depth")
    PAIR(pr3b1, "Wild boar ragù with black olive pasta", "complement", "established", "main", "Game ragù with regional flavours; black olive echoes Manon's garrigue; game intensity meets wine's power")

pr3b2, n = PROD("Clos Marie Pic Saint-Loup L'Olivette", "wine_still", p3b, r3, "France",
    subcategory="Syrah Grenache Mourvèdre", price_tier="premium",
    description="Second wine from Clos Marie; garrigue, dark cherry, pepper, limestone mineral; more accessible than Manon but shows the same biodynamic precision.")
if n:
    PAIR(pr3b2, "Saucisse de Toulouse with white bean cassoulet", "complement", "classic", "main", "Southwest France classic; Languedoc Syrah bridges the sausage and beans; cassoulet richness tamed by acidity")
    PAIR(pr3b2, "Tapenade bruschetta with roasted cherry tomatoes", "complement", "established", "starter", "Mediterranean starter; wine's olive-garrigue notes echo tapenade; tomato acidity balanced by wine's fruit")
    PAIR(pr3b2, "Grilled lamb cutlets with ratatouille", "complement", "classic", "main", "Provençal pairing; L'Olivette's garrigue matches the herbs; lamb fat handled by tannin")
    PAIR(pr3b2, "Comté cheese with charcuterie", "complement", "established", "cheese", "French cheese board; Pic Saint-Loup's fruit and structure balance Comté's nutty fat; charcuterie bridges")

# 4. FAUGÈRES AOC — Languedoc, France
print("=== Faugères AOC ===")
r4 = R("Faugères AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Faugères AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Languedoc sub-appellation on ancient schist soils west of Montpellier; the unique blue-grey schist produces wines of mineral intensity and distinctive character quite unlike limestone-based Languedoc. Syrah, Grenache, and Mourvèdre dominate; Carignan from old vines adds complexity. Also produces white wines (including Roussanne and Marsanne). Schist soils retain heat and drain exceptionally; wines have extraordinary minerality.",
        key_producers="Château Haut-Fabrègues, Domaine Léon Barral, Château des Estanilles, Alquier",
        historical_context="Faugères was the first Languedoc village to obtain its own AOC (1982 for reds, 2005 for whites). The schist soils were considered poor for anything but low-yield quality wine; this is now a virtue. Léon Barral's natural farming from the 1990s showed that old vine Carignan and Mourvèdre on schist could produce wines of global standing. The AOC produces some of Languedoc's most mineral and terroir-expressive reds.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm year; schist heat retention produced concentrated wines; Syrah and Mourvèdre particularly rich"),
    (2019, "very_good", "rising", "Good year; schist mineral well-expressed; Carignan old vines show distinctive earthy character"),
    (2020, "excellent", "rising", "Excellent vintage; schist soils produced focused, mineral wines; benchmark year for quality Faugères"),
    (2021, "very_good", "rising", "Good growing season; mineral precision from schist; Syrah shows pepper and dark fruit elegance"),
    (2022, "excellent", "stable", "Warm conditions; schist retained heat well; concentrated wines with characteristic mineral backbone"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Domaine Léon Barral", "winery", r4, "France",
        production_philosophy="natural",
        philosophy_description="Didier Barral's natural farming estate on ancient schist; polyculture farming with animals; old vine Carignan, Mourvèdre and Syrah with no additions; one of Languedoc's most celebrated natural wine producers.",
        reputation_narrative="The legendary natural Faugères producer; Léon Barral's wines from ancient schist with zero additions have become some of Languedoc's most collected and highest-scoring wines globally.",
        price_positioning="ultra_premium")

pr4a1, n = PROD("Domaine Léon Barral Jadis Faugères", "wine_still", p4a, r4, "France",
    subcategory="Carignan Mourvèdre old vine", price_tier="ultra_premium",
    description="Old vine Carignan and Mourvèdre from schist; no additions; extraordinary mineral depth; dried cherry, iron, garrigue, violets; profound and structured; one of Languedoc's most revered wines.")
if n:
    PAIR(pr4a1, "Wild boar shoulder slow-roasted with Languedoc herbs", "complement", "classic", "main", "Regional game; Jadis's power and mineral intensity suit the wild boar; garrigue herbs echo wine's terroir")
    PAIR(pr4a1, "Aged Roquefort with walnut and fig compote", "complement", "classic", "cheese", "Strong blue cheese; Jadis's concentration can handle it; fig bridges dark fruit; walnut echoes schist mineral")
    PAIR(pr4a1, "Grilled leg of lamb with rosemary and anchovy", "complement", "classic", "main", "Languedoc tradition; lamb and Faugères; anchovy deepens umami; rosemary echoes the garrigue in the wine")
    PAIR(pr4a1, "Slow-braised oxtail with olives and orange peel", "complement", "established", "main", "Mediterranean braise; collagen richness meets Jadis's tannin; olive and orange bridge the schist mineral")

pr4a2, n = PROD("Domaine Léon Barral Faugères", "wine_still", p4a, r4, "France",
    subcategory="Syrah Grenache Mourvèdre Carignan", price_tier="premium",
    description="Entry Léon Barral Faugères; Syrah, Grenache, Mourvèdre, and Carignan; dark fruit, schist mineral, garrigue; natural winemaking; more accessible than Jadis; one of Languedoc's finest everyday wines.")
if n:
    PAIR(pr4a2, "Grilled lamb brochettes with harissa and flatbread", "complement", "classic", "main", "North African-Languedoc bridge; Faugères mineral handles harissa spice; lamb and Carignan classic match")
    PAIR(pr4a2, "Tapenade and grilled vegetables with olive oil", "complement", "established", "starter", "Mediterranean spread; wine's olive notes echo tapenade; schist mineral bridges the roasted vegetables")
    PAIR(pr4a2, "Pork belly with roasted fennel and orange", "complement", "established", "main", "Pork and Syrah; fennel echoes wine's herbal notes; orange peel bridges garrigue; belly fat tamed by tannin")
    PAIR(pr4a2, "Roasted red peppers stuffed with rice and herbs", "complement", "established", "main", "Mediterranean vegetarian; Faugères's mineral freshness suits; pepper sweetness bridges the garrique notes")

p4b = P("Château des Estanilles", "winery", r4, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Established Faugères estate producing whites and reds from old vine schist; Michel Louison's estate is one of the AOC's most reliable quality producers.",
        reputation_narrative="A dependable quality reference for Faugères; Château des Estanilles consistently produces mineral, food-friendly Faugères reds and whites that show the schist terroir's distinctive character.",
        price_positioning="premium")

pr4b1, n = PROD("Château des Estanilles Cuvée Prestige Faugères Rouge", "wine_still", p4b, r4, "France",
    subcategory="Syrah Mourvèdre Grenache", price_tier="premium",
    description="Prestige Faugères rouge from schist; Syrah, Mourvèdre, Grenache; garrigue, dark cherry, pepper, iron mineral; concentrated and structured; needs 5-8 years; benchmark traditional Faugères expression.")
if n:
    PAIR(pr4b1, "Cassoulet with duck confit and Toulouse sausage", "complement", "classic", "main", "Southwest France classic; Faugères mineral cuts through the rich cassoulet; sausage fat tamed by tannin")
    PAIR(pr4b1, "Magret de canard with fig and balsamic reduction", "complement", "established", "main", "Duck and Languedoc; fig mirrors wine's dark fruit; balsamic acidity bridges schist mineral")
    PAIR(pr4b1, "Grilled venison steak with blackberry jus", "complement", "established", "main", "Game and old Carignan; blackberry mirrors Prestige's dark fruit; venison's iron echoes wine's schist mineral")
    PAIR(pr4b1, "Aged Pélardon goat cheese with lavender honey", "complement", "established", "cheese", "Languedoc goat cheese; Faugères acidity balances; lavender bridges garrigue notes; honey softens tannin")

pr4b2, n = PROD("Château des Estanilles Faugères Blanc", "wine_still", p4b, r4, "France",
    subcategory="Roussanne Marsanne Grenache Blanc", price_tier="mid_range",
    description="Faugères blanc from schist soils; Roussanne, Marsanne, Grenache Blanc; white peach, apricot, schist mineral, beeswax; full body; rare expression of white Faugères; excellent food wine.")
if n:
    PAIR(pr4b2, "Roasted monkfish with saffron and rouille", "complement", "classic", "fish_course", "Meaty fish with golden sauce; Roussanne's weight matches monkfish; saffron bridges wine's apricot notes")
    PAIR(pr4b2, "Bouillabaisse with gruyère croutons", "complement", "established", "main", "Provençal fish stew; white Faugères's schist mineral complements the seafood; gruyère bridges the wine's body")
    PAIR(pr4b2, "Pan-seared foie gras with Muscat reduction", "complement", "established", "starter", "Rich liver; Roussanne-Marsanne blend has sufficient body; Muscat sweetness in reduction bridges the wine")
    PAIR(pr4b2, "Aged Manchego with quince paste", "complement", "established", "cheese", "Aged sheep cheese; white Faugères's body and acidity balance; quince bridges wine's stone fruit character")

# 5. CANNONAU DI SARDEGNA DOC — Sardinia, Italy
print("=== Cannonau di Sardegna DOC ===")
r5 = R("Cannonau di Sardegna DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Cannonau di Sardegna DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Sardinia's flagship red wine DOC from Cannonau (Grenache) grown across the island; the oldest Cannonau vines (some 100+ years old) are head-trained alberello; rich, full-bodied reds with cherry, herbs, Mediterranean warmth. The Nuoro region (particularly Oliena and Orgosolo) produces the finest expressions. Sardinia's blue zone longevity connection partly attributed to moderate Cannonau consumption.",
        key_producers="Gostolai, Giuseppe Sedilesu, Cantina di Orgosolo, Dettori",
        historical_context="Cannonau is genetically identical to Garnacha/Grenache but DNA research suggests Sardinia may be the origin of the variety — predating Spanish Garnacha. The variety has been on the island for at least 3000 years. The Blue Zone connection (Sardinia has one of the world's highest concentrations of centenarians) has been linked to the antioxidants in Cannonau. Oliena and Orgosolo in the Nuoro province produce the most traditional and age-worthy expressions.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good Cannonau year; warm conditions; old vine concentration; Mediterranean warmth balanced by herbal freshness"),
    (2019, "excellent", "rising", "Excellent vintage; old alberello vines show extraordinary depth; cherry and herbs with fine structure"),
    (2020, "very_good", "rising", "Good growing season; Nuoro Cannonau from granite shows mineral freshness alongside fruit richness"),
    (2021, "excellent", "rising", "Excellent; old vine Cannonau of great depth and complexity; benchmark expressions from Oliena"),
    (2022, "very_good", "stable", "Good year; Mediterranean heat produced concentrated reds; herbal character particularly pronounced"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Giuseppe Sedilesu", "winery", r5, "Italy",
        production_philosophy="traditional",
        philosophy_description="Organic Mamoiada producer making traditional Cannonau from old alberello vines on granite; the Mamuthone and Carnevale are iconic Sardinian reds showing the variety at its most authentic.",
        reputation_narrative="The most celebrated traditional Cannonau producer; Sedilesu's organic old vine wines from Mamoiada's granite soils show what the variety can achieve and have earned Italy's highest accolades for Sardinian wine.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("Giuseppe Sedilesu Mamuthone Cannonau di Sardegna", "wine_still", p5a, r5, "Italy",
    subcategory="Cannonau old vine", price_tier="ultra_premium",
    description="Named for the traditional Mamoiada carnival mask; old alberello Cannonau from granite soils; dark cherry, Mediterranean herbs, iron mineral, licorice; concentrated and structured; benchmark Sardinian Cannonau.")
if n:
    PAIR(pr5a1, "Porceddu (Sardinian whole roasted suckling pig with myrtle)", "complement", "classic", "main", "The definitive Sardinian celebration dish; myrtle echoes Cannonau's herbal character; suckling pig fat handled by tannin")
    PAIR(pr5a1, "Pecora arrosto (roast sheep) with carasau bread", "complement", "classic", "main", "Traditional Nuoro preparation; sheep and Cannonau; carasau bread absorbs the cooking juices; regional tradition")
    PAIR(pr5a1, "Cinghiale (Sardinian wild boar) with myrtle berries", "complement", "classic", "main", "Island game with myrtle; myrtle bridges Cannonau's herbal depth; boar intensity tamed by old vine concentration")
    PAIR(pr5a1, "Aged Fiore Sardo with Sardinian honey", "complement", "classic", "cheese", "Sardinia's ancient sheep cheese; Cannonau's concentration meets the aged intensity; honey bridges herbal notes")

pr5a2, n = PROD("Giuseppe Sedilesu Carnevale Cannonau di Sardegna", "wine_still", p5a, r5, "Italy",
    subcategory="Cannonau", price_tier="premium",
    description="More accessible Sedilesu Cannonau; younger vines; fresh cherry, herbs, granite mineral; vibrant acidity; excellent everyday Sardinian red with traditional character.")
if n:
    PAIR(pr5a2, "Malloreddus with Sardinian pork ragù and saffron", "complement", "classic", "main", "Traditional Sardinian pasta; Cannonau's herb and cherry bridge saffron ragù; the classic island combination")
    PAIR(pr5a2, "Grilled lamb chops with rosemary and garlic", "complement", "classic", "main", "Mediterranean classic; Cannonau's cherry and herb notes echo rosemary; garlic bridges the iron mineral")
    PAIR(pr5a2, "Fritto misto with anchovies and vegetables", "complement", "established", "starter", "Sardinian coastal fried mix; Cannonau's freshness cuts the batter; acidity refreshes between bites")
    PAIR(pr5a2, "Pecorino Sardo fresco with olives and walnuts", "complement", "established", "starter", "Sardinian aperitivo; Cannonau's cherry cuts the fresh cheese; olives echo wine's Mediterranean herbal notes")

p5b = P("Alessandro Dettori", "winery", r5, "Italy",
        production_philosophy="natural",
        philosophy_description="Natural wine radical from Romangia; Alessandro Dettori makes extreme Cannonau with no sulphur and years of aging in old chestnut barrels; Dettori Rosso is a cult wine of extraordinary individuality.",
        reputation_narrative="Italy's most extreme natural Cannonau producer; Dettori's wines provoke fierce debate but are among Sardinia's most collected; his refusal to use sulphur and extended aging create wines of unique character.",
        price_positioning="ultra_premium")

pr5b1, n = PROD("Dettori Dettori Rosso Cannonau Romangia", "wine_still", p5b, r5, "Italy",
    subcategory="Cannonau natural", price_tier="ultra_premium",
    description="Extreme natural Cannonau with no additions; years in chestnut casks; dried cherry, tobacco, Mediterranean herbs, earth; volatile acidity adds complexity; cult wine of polarizing but compelling character.")
if n:
    PAIR(pr5b1, "Aged Fiore Sardo stagionato with bitter honey", "complement", "established", "cheese", "Very aged Sardinian sheep cheese; Dettori's volatile acidity and dried fruit handle the pungency; bitter honey bridges")
    PAIR(pr5b1, "Cinghiale (wild boar) slow-braised with myrtle and juniper", "complement", "classic", "main", "Extreme Sardinian game preparation; Dettori's intensity meets its match; myrtle and juniper bridge wine's complexity")
    PAIR(pr5b1, "Charcuterie with Sardinian guanciale and lardo", "complement", "established", "starter", "Cured fat; natural Cannonau's volatile acidity cuts through; dried fruit bridges the cured meat complexity")
    PAIR(pr5b1, "Roasted lamb with mountain herbs and carasau bread", "complement", "classic", "main", "Traditional Sardinian mountain feast; Dettori's power and herb notes suit the celebration; bread grounds")

pr5b2, n = PROD("Dettori Tenores Cannonau Romangia", "wine_still", p5b, r5, "Italy",
    subcategory="Cannonau natural", price_tier="ultra_premium",
    description="More mineral expression of Dettori's Cannonau; granite soils; dried cherry, herbs, chalky mineral; slightly more restrained than Dettori Rosso but same zero-sulphur philosophy.")
if n:
    PAIR(pr5b2, "Bottarga di muggine with grilled bread and olive oil", "complement", "established", "starter", "Sardinian cured roe; natural wine's oxidative notes complement; mineral Cannonau bridges the intense umami")
    PAIR(pr5b2, "Grilled Sardinian sausage with roasted potatoes", "complement", "classic", "main", "Island tradition; Tenores' herbal fruit matches the fennel-spiced sausage; natural acidity refreshes")
    PAIR(pr5b2, "Vegetable fritto with local herbs", "complement", "established", "starter", "Simple Sardinian fried preparation; natural Cannonau's freshness cuts; herbs bridge wine's Mediterranean character")
    PAIR(pr5b2, "Aged Pecorino di Osilo with wild flower honey", "complement", "established", "cheese", "Strong Sardinian sheep cheese; Tenores' mineral depth handles it; honey softens and bridges the herbal notes")

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
print("B134 complete.")
conn.close()
