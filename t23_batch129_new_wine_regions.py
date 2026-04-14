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

# ── B129 ──────────────────────────────────────────────────────────────────────
# Targets: Valdeorras DO (Spain), Bierzo DO (Spain), Bandol AOC (France),
#          Patrimonio AOC (France/Corsica), Sagrantino di Montefalco DOCG (Italy)

# 1. VALDEORRAS DO — Spain
print("=== Valdeorras DO ===")
r1 = R("Valdeorras DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Valdeorras DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Galician DO along the Sil River valley in Ourense province; granite and slate soils at 400-700m altitude produce Galicia's most mineral Godello whites and structured Mencía reds. Rafael Palacios's As Sortes single-vineyard Godello from 70-year-old vines on steep slate terraces is considered one of Spain's greatest white wines. The valley's sheltered microclimate and dramatic slate soils give wines extraordinary mineral precision.",
        key_producers="Rafael Palacios, Valdesil, Bodegas Godeval, A Coroa",
        historical_context="Valdeorras was historically overshadowed by Rías Baixas until Rafael Palacios (brother of Álvaro) arrived in 2004 and revealed Godello's extraordinary potential on the valley's slate terraces. The region was granted DO status in 1977 but only gained international recognition in the 2000s. Godello's revival here paralleled the renaissance of Spanish white wines generally.")
for yr, qd, pt, sn in [
    (2018, "good", "stable", "Variable conditions; careful selection rewarded; fresh aromatic whites and medium-weight reds"),
    (2019, "very_good", "stable", "Challenging spring frost reduced yields; concentrated flavours; premium cuvées outstanding"),
    (2020, "excellent", "rising", "Balanced year; classic mineral Godello expression; elegant Mencía with fine tannins"),
    (2021, "very_good", "rising", "Warm dry summer; ripe Godello with good concentration; Mencía shows plush dark fruit"),
    (2022, "excellent", "rising", "Cool Atlantic growing season; Godello aromatics pristine; ideal ripeness with natural acidity"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Rafael Palacios", "winery", r1, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Rafael Palacios, brother of Álvaro Palacios, established this estate to champion Godello on steep slate terraces. As Sortes from 70+ year old vines is considered Spain's greatest white wine.",
        reputation_narrative="The reference producer for Valdeorras Godello; As Sortes has put the region on the global fine wine map and shown that Spanish white wine can rival Burgundy.",
        price_positioning="ultra_premium")

pr1a1, n = PROD("Rafael Palacios As Sortes Godello", "wine_still", p1a, r1, "Spain",
    subcategory="Godello", price_tier="ultra_premium",
    description="Flagship single-vineyard Godello from 70+ year old vines on steep slate terraces; profound mineral depth with white peach, citrus blossom, saline slate; extraordinary texture and length; one of Spain's greatest white wines.")
if n:
    PAIR(pr1a1, "Galician octopus (pulpo a feira) with smoked paprika", "complement", "classic", "starter", "Saline mineral Godello mirrors oceanic character of octopus; paprika's smokiness echoes the wine's subtle phenolic depth")
    PAIR(pr1a1, "Grilled turbot with herb butter", "complement", "classic", "fish_course", "Godello's textural richness matches the meaty turbot; citrus notes cut the butter; mineral finish cleanses the palate")
    PAIR(pr1a1, "Percebes (goose barnacles) with sea salt", "complement", "established", "starter", "Ultra-rare Galician delicacy; pure oceanic brine pairs perfectly with Godello's sea-spray minerality")
    PAIR(pr1a1, "Aged Tetilla cheese with honey", "bridge", "suggested", "cheese", "Galician cow's milk cheese; Godello's citrus cuts the fat; honey bridges the wine's floral aromatics")

pr1a2, n = PROD("Rafael Palacios Louro do Bolo Godello", "wine_still", p1a, r1, "Spain",
    subcategory="Godello", price_tier="premium",
    description="Entry-level Godello showing the house style; fresh and mineral with white flowers, ripe pear, citrus; refreshing acidity and clean mineral finish; excellent depth for price.")
if n:
    PAIR(pr1a2, "Steamed clams with white wine and garlic", "complement", "classic", "starter", "Classic Galician preparation; Godello's mineral freshness complements the briny shellfish perfectly")
    PAIR(pr1a2, "Empanada gallega de atún (Galician tuna pie)", "complement", "established", "main", "Traditional Galician snack; white wine's acidity cuts the pastry richness; mineral notes complement savory filling")
    PAIR(pr1a2, "Grilled sea bass with lemon", "complement", "classic", "fish_course", "Clean fish preparation allows Godello's aromatics to shine; citrus resonance; refreshing acidity balances")
    PAIR(pr1a2, "Calamari with alioli", "complement", "established", "starter", "Lightly fried squid; Godello's freshness cuts the oil; minerality echoes the seafood")

p1b = P("Bodegas Valdesil", "winery", r1, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Family winery dedicated to Godello and Mencía; single-vineyard Godello from Pedrouzos parcels and old-vine Mencía; indigenous yeast and minimal sulphur.",
        reputation_narrative="Leading Valdeorras estate producing single-parcel Godello and structured Mencía; Pedrouzos demonstrates old-vine Godello's extraordinary concentration on slate.",
        price_positioning="premium")

pr1b1, n = PROD("Valdesil Pedrouzos Godello", "wine_still", p1b, r1, "Spain",
    subcategory="Godello", price_tier="premium",
    description="Single-parcel Godello from Pedrouzos; old vines on slate and granite; intense citrus, stone fruit, graphite; full body with vibrant acidity and saline finish.")
if n:
    PAIR(pr1b1, "Pan-seared scallops with cauliflower purée", "complement", "classic", "starter", "Godello's texture mirrors creamy purée; mineral notes highlight scallop sweetness; citrus lifts the dish")
    PAIR(pr1b1, "Monkfish with potato and chorizo", "complement", "classic", "fish_course", "Robust fish stew; full-bodied Godello matches the weight; smokiness of chorizo complements wine's depth")
    PAIR(pr1b1, "Roasted Galician beef rib with vegetables", "complement", "established", "main", "Rich Godello with body to stand up to beef; mineral notes cut richness; Galician pairing tradition")
    PAIR(pr1b1, "Grilled vegetables with romesco", "complement", "established", "main", "Nutty romesco sauce bridges Godello's mineral and fruity characters; vegetable sweetness balanced by acidity")

pr1b2, n = PROD("Valdesil Valderroa Mencía", "wine_still", p1b, r1, "Spain",
    subcategory="Mencía", price_tier="premium",
    description="Structured Mencía red from Valdeorras; darker and more mineral than Bierzo Mencía; dark cherry, graphite, violet; firm tannins; mineral finish with good aging potential.")
if n:
    PAIR(pr1b2, "Roast suckling pig with Galician potatoes", "complement", "classic", "main", "Traditional Galician feast dish; Mencía's tannins cut the fat; dark fruit complements the roast")
    PAIR(pr1b2, "Lamb chops with herb crust", "complement", "established", "main", "Herb notes in Mencía echo the crust; firm tannins balance the lamb fat; mineral finish cleanses")
    PAIR(pr1b2, "Wild mushroom risotto with Manchego", "bridge", "suggested", "main", "Earthy Mencía echoes forest floor character of mushrooms; mineral graphite notes complement aged cheese")
    PAIR(pr1b2, "Aged Arzúa-Ulloa cheese", "complement", "established", "cheese", "Galician cow's milk cheese; Mencía's acidity and tannins balance the fat; regional pairing")

# 2. BIERZO DO — Spain
print("=== Bierzo DO ===")
r2 = R("Bierzo DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Bierzo DO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Northwestern Spanish DO in the province of León where the Atlantic and continental climates meet; slate and schist soils at 400-900m altitude; Mencía produces Burgundian-elegant reds of extraordinary fragrance and minerality. Álvaro Palacios and nephew Ricardo Pérez put Bierzo on the global map with La Faraona (one of Spain's rarest and most expensive wines) and accessible Petalos del Bierzo. Old Mencía vines on steep slate terraces produce wines of Pinot Noir-like delicacy.",
        key_producers="Descendientes de J. Palacios, Pittacum, Dominio de Tares, Raúl Pérez",
        historical_context="Bierzo received DO status in 1989 but remained obscure until Álvaro Palacios arrived in 1999 to make wine with old Mencía vines he discovered on abandoned slate terraces. His Petalos del Bierzo created the market for affordable Bierzo while La Faraona and the Corullón single-village wines attracted serious collectors. The region is now considered Spain's answer to Chambolle-Musigny.")
for yr, qd, pt, sn in [
    (2018, "very_good", "stable", "Ripe year; generous fruit; cool altitude vineyards excelled; Mencía shows plush dark fruit"),
    (2019, "excellent", "stable", "Classic Bierzo expression; aromatic precision and firm tannin; wines showing beautifully now"),
    (2020, "exceptional", "rising", "Exceptional vintage; concentration with elegance; best old-vine parcels produced benchmark wines"),
    (2021, "very_good", "rising", "Good balance; ripe dark fruit with firm mineral backbone; excellent ageing potential"),
    (2022, "excellent", "rising", "Cool wet spring then warm dry summer; Mencía achieves perfect phenolic ripeness; fragrant and structured"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Descendientes de J. Palacios", "winery", r2, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Álvaro Palacios and nephew Ricardo Pérez Palacios revived old Mencía vines on abandoned slate terraces. La Faraona is Spain's most sought-after red; Petalos makes Bierzo accessible.",
        reputation_narrative="The estate that defined modern Bierzo; La Faraona (€500+) rivals the world's greatest reds; Petalos is one of Spain's best-value quality reds, introducing millions to the region.",
        price_positioning="ultra_premium")

pr2a1, n = PROD("Descendientes de J. Palacios Petalos del Bierzo", "wine_still", p2a, r2, "Spain",
    subcategory="Mencía", price_tier="mid_range",
    description="Entry cuvée from Álvaro Palacios blending parcels across Bierzo; red cherry, raspberry, violet, slate; silky tannins, fresh acidity, medium body with Pinot-like grace; superb value.")
if n:
    PAIR(pr2a1, "Roast chicken with thyme and garlic", "complement", "classic", "main", "Mencía's silky texture and red fruit complement roast poultry; thyme echoes wine's herbal notes; elegant pairing")
    PAIR(pr2a1, "Charcuterie board with Ibérico ham", "complement", "classic", "starter", "Slate-driven Mencía pairs beautifully with cured meats; acidity refreshes between bites; Spanish tradition")
    PAIR(pr2a1, "Grilled lamb cutlets with mint sauce", "complement", "established", "main", "Bierzo Mencía's freshness cuts lamb fat; mint resonates with wine's herbal character; regional tradition")
    PAIR(pr2a1, "Roasted beetroot and goat cheese salad", "bridge", "suggested", "starter", "Mencía's red fruit echoes beetroot earthiness; goat cheese acidity bridges; elegant vegetarian pairing")

pr2a2, n = PROD("Descendientes de J. Palacios Villa de Corullón Mencía", "wine_still", p2a, r2, "Spain",
    subcategory="Mencía", price_tier="ultra_premium",
    description="Single-village wine from Corullón; old vines on slate; dark cherry, blackberry, smoky mineral, violet; structured tannins; long mineral finish; needs 3-10 years.")
if n:
    PAIR(pr2a2, "Roast leg of lamb with rosemary and garlic", "complement", "classic", "main", "Structured Mencía handles lamb's richness; rosemary echoes wine's herbal mineral character; classical match")
    PAIR(pr2a2, "Wild boar stew with chestnuts", "complement", "established", "main", "Game-weight Mencía matches wild boar intensity; chestnut earthiness resonates with slate minerality")
    PAIR(pr2a2, "Duck confit with lentils", "complement", "established", "main", "Rich duck fat tamed by Mencía's tannin and acidity; earthiness of lentils bridges the mineral character")
    PAIR(pr2a2, "Aged Zamorano sheep cheese", "complement", "established", "cheese", "Sharp aged sheep cheese; Mencía's tannins and acidity cut the fat; mineral finish complements aged notes")

p2b = P("Bodegas Pittacum", "winery", r2, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Small Bierzo winery focused on old-vine Mencía from El Bierzo Bajo; slate parcels; traditional winemaking with modern precision.",
        reputation_narrative="Consistent Bierzo producer making old-vine Mencía of real character; Pittacum Grand Cru demonstrates the depth possible from best slate parcels.",
        price_positioning="premium")

pr2b1, n = PROD("Pittacum Mencía Bierzo", "wine_still", p2b, r2, "Spain",
    subcategory="Mencía", price_tier="premium",
    description="Estate Mencía from old vines on slate; ripe cherry, damson, violet, cedar; smooth tannins; persistent mineral finish; classic Bierzo character.")
if n:
    PAIR(pr2b1, "Cocido maragato (Spanish meat stew)", "complement", "classic", "main", "Hearty Leonese stew of meats and chickpeas; Mencía's fruit and acidity balance the rich broth; regional tradition")
    PAIR(pr2b1, "Grilled chorizo with roasted peppers", "complement", "established", "starter", "Spiced chorizo's paprika notes echo Mencía's dark fruit; acidity refreshes; classic Spanish pairing")
    PAIR(pr2b1, "Mushroom and black truffle croquetas", "bridge", "suggested", "starter", "Earthy truffle resonates with Mencía's mineral depth; creamy croqueta balanced by wine's acidity")
    PAIR(pr2b1, "Roast pork belly with apple compote", "complement", "established", "main", "Pork richness tamed by Mencía tannins; apple's acidity bridges; fruit-forward pairing")

pr2b2, n = PROD("Pittacum Petit Pittacum Mencía", "wine_still", p2b, r2, "Spain",
    subcategory="Mencía", price_tier="mid_range",
    description="Younger vine Mencía; approachable style for early drinking; fresh raspberry, cherry, herbs; light tannins, crisp acidity; joyful everyday Bierzo.")
if n:
    PAIR(pr2b2, "Tapas spread with jamón and olives", "complement", "classic", "aperitif", "Fresh Mencía refreshes palate between bites; acidity cuts salt and fat; classic Spanish aperitif style")
    PAIR(pr2b2, "Grilled vegetables with hummus", "complement", "established", "main", "Light herbal Mencía suits roasted vegetables; minimal tannins won't overpower; Mediterranean bridge")
    PAIR(pr2b2, "Pork empanada", "complement", "established", "starter", "Savory pastry filling; Mencía's fruit balances; acidity cuts through the pastry richness")
    PAIR(pr2b2, "Pizza margherita", "complement", "suggested", "main", "Light Mencía's acidity matches tomato; tannins complement mozzarella; easy-going pairing")

# 3. BANDOL AOC — France
print("=== Bandol AOC ===")
r3 = R("Bandol AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Bandol AOC",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="One of France's most distinctive and under-appreciated appellations on the Mediterranean coast near Toulon in Provence; terraced limestone and clay-limestone soils in a natural amphitheatre sheltered from the Mistral wind. Mourvèdre-dominant reds require 18 months minimum oak aging and develop extraordinary complexity over 15-30 years. Exceptional savoury rosés and full-bodied whites also produced. The appellation has only 1,500 hectares but produces wines of global significance.",
        key_producers="Domaine Tempier, Château Pradeaux, Domaine de Terrebrune, Château Simone",
        historical_context="Bandol was one of France's first AOC appellations in 1941, recognising the quality of its Mourvèdre wines. Lucien and Lulu Peyraud of Domaine Tempier championed the region from the 1940s; their gastronomic table attracted Alice Waters and Richard Olney, who spread Bandol's reputation globally. The 18-month minimum aging for reds and 50% minimum Mourvèdre ensure the wines' unique character.")
for yr, qd, pt, sn in [
    (2018, "excellent", "stable", "Rich and generous; some heat stress offset by careful picking; rosés particularly successful"),
    (2019, "very_good", "stable", "Classic Bandol expression; Mourvèdre achieved full phenolic ripeness; age-worthy reds"),
    (2020, "exceptional", "rising", "Exceptional vintage; concentrated Mourvèdre with extraordinary depth; century-level wines possible"),
    (2021, "excellent", "rising", "Balanced year with good acidity retention; elegant reds with classical structure; outstanding rosés"),
    (2022, "very_good", "stable", "Hot Mediterranean summer; ripe concentrated Mourvèdre; rosés show fresh aromatic character"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine Tempier", "winery", r3, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The iconic Bandol estate that defined the appellation; Lucien and Lulu Peyraud revived the domaine post-WWII and championed Mourvèdre; single-vineyard cuvées La Tourtine and Migoua are legendary.",
        reputation_narrative="France's most storied Provence estate; Tempier's table hosted Alice Waters, Richard Olney and MFK Fisher, spreading Bandol's name worldwide. The family have maintained traditional Mourvèdre-focused winemaking for 80+ years.",
        price_positioning="ultra_premium")

pr3a1, n = PROD("Domaine Tempier Bandol Rouge", "wine_still", p3a, r3, "France",
    subcategory="Mourvèdre", price_tier="premium",
    description="Classic estate Bandol rouge; Mourvèdre-dominant blend aged in large foudres; black olive, garrigue, dark cherry, leather; firm structured tannins; extraordinary savoury complexity; the benchmark Bandol expression.")
if n:
    PAIR(pr3a1, "Provençal lamb daube with olives and herbes de Provence", "complement", "classic", "main", "The definitive Bandol pairing; garrigue in Mourvèdre echoes Provençal herbs; lamb tames the tannins perfectly")
    PAIR(pr3a1, "Grilled wild boar sausages with white bean cassoulet", "complement", "established", "main", "Game weight matches Mourvèdre's power; earthy bean cassoulet bridges; Southern French tradition")
    PAIR(pr3a1, "Bouillabaisse with rouille", "contrast", "adventurous", "main", "Unexpected classical Provençal pairing; rich saffron broth needs Mourvèdre's structure; rouille's spice echoes garrigue")
    PAIR(pr3a1, "Aged Comté cheese with walnut bread", "complement", "established", "cheese", "Nutty aged Comté; Mourvèdre's savoury depth and tannins balance the fat; walnut echoes wine's dried fruit")

pr3a2, n = PROD("Domaine Tempier Bandol Rosé", "wine_still", p3a, r3, "France",
    subcategory="Mourvèdre rosé", price_tier="premium",
    description="Iconic Bandol rosé; Mourvèdre-dominant unlike most Provence rosés; wild strawberry, white peach, dried herbs, floral; structured and savoury with crisp acidity; serious rosé that ages beautifully.")
if n:
    PAIR(pr3a2, "Grilled whole sea bream with herbs and lemon", "complement", "classic", "fish_course", "Iconic Mediterranean pairing; rosé's herbs echo the bream; citrus mirrors wine's acidity; coastal elegance")
    PAIR(pr3a2, "Salade Niçoise with seared tuna", "complement", "classic", "starter", "The definitive Provençal salad with serious rosé; olive notes in wine; anchovy saltiness balanced by acidity")
    PAIR(pr3a2, "Ratatouille with grilled polenta", "complement", "classic", "main", "Vegetable stew with Provençal herbs resonating with the rosé; garrigue notes in perfect harmony")
    PAIR(pr3a2, "Boquerones (marinated anchovies) with bread", "complement", "established", "starter", "Salty umami anchovies; rosé's acidity refreshes; Mourvèdre weight handles the intensity")

p3b = P("Château Pradeaux", "winery", r3, "France",
        production_philosophy="traditional",
        philosophy_description="Ancient Bandol estate with some of the appellation's oldest Mourvèdre vines; ultra-traditional with extremely long aging in foudres; wines requiring years of cellaring.",
        reputation_narrative="The most traditional Bandol producer; Pradeaux's ancient Mourvèdre vines and years of aging produce wines of extraordinary longevity that open after a decade and evolve for 30+ years.",
        price_positioning="ultra_premium")

pr3b1, n = PROD("Château Pradeaux Bandol Rouge", "wine_still", p3b, r3, "France",
    subcategory="Mourvèdre", price_tier="ultra_premium",
    description="Ultra-traditional Bandol from 80+ year old Mourvèdre vines; aged 3+ years in foudres; black olive tapenade, tar, leather, dried violet; immense structure; requires 10-20 years cellaring; legendary wine.")
if n:
    PAIR(pr3b1, "Aged côte de boeuf with bone marrow and herbs", "complement", "classic", "main", "Only a great red meat can stand up to Pradeaux's immense tannin; bone marrow richness tamed; herbed crust echoes garrigue")
    PAIR(pr3b1, "Slow-braised oxtail with root vegetables", "complement", "established", "main", "Long braise matches wine's long-aged complexity; collagen richness tames the tannins; earthy vegetables bridge")
    PAIR(pr3b1, "Truffle-studded roast pork shoulder", "complement", "established", "main", "Earthy truffle resonates with Mourvèdre's garrigue; pork fat tamed by tannin; Provençal luxury")
    PAIR(pr3b1, "Aged Époisses de Bourgogne washed-rind cheese", "complement", "adventurous", "cheese", "Pungent washed-rind meets powerful Mourvèdre; both are extreme; the clash becomes harmony with time")

pr3b2, n = PROD("Château Pradeaux Bandol Rosé", "wine_still", p3b, r3, "France",
    subcategory="Mourvèdre rosé", price_tier="premium",
    description="Serious Bandol rosé from old Mourvèdre and Cinsault; garrigue, dried rose petals, white cherry, mineral; structured with firm acidity; one of France's great rosés.")
if n:
    PAIR(pr3b2, "Socca (chickpea flatbread) with rosemary olive oil", "complement", "classic", "starter", "Provençal street food; rosé's herbs echo rosemary; chickpea earthiness bridges; casual Mediterranean perfection")
    PAIR(pr3b2, "Grilled red mullet with tapenade", "complement", "classic", "fish_course", "Red mullet's intense flavour needs Bandol's structure; olive tapenade mirrors wine's olive notes; coastal match")
    PAIR(pr3b2, "Pan bagnat (Niçoise sandwich)", "complement", "established", "main", "Provençal sandwich; rosé's acidity cuts the olive oil; tuna and vegetables complement the herbs in wine")
    PAIR(pr3b2, "Pistou soup with haricots verts", "complement", "established", "main", "Basil-herb soup echoes wine's garrigue character; bean earthiness bridges; classic Provençal summer pairing")

# 4. PATRIMONIO AOC — France (Corsica)
print("=== Patrimonio AOC ===")
r4 = R("Patrimonio AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Patrimonio AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Corsica's oldest and most prestigious AOC on the Cap Corse peninsula; schist and clay-limestone soils; Nielluccio (Sangiovese's Corsican relative) produces structured reds with Mediterranean herbs and maquis character. Vermentino whites show mineral elegance from schist soils. Antoine Arena and Domaine Leccia make wines of extraordinary individuality that reflect the island's wild character. The appellation covers only 450 hectares.",
        key_producers="Antoine Arena, Domaine Leccia, Yves Leccia, Clos Marfisi",
        historical_context="Patrimonio was Corsica's first AOC in 1968, predating mainland recognition of Corsican wine. The island's isolation preserved indigenous varieties (Nielluccio, Vermentino, Sciaccarello) and traditional methods. Antoine Arena's extreme natural winemaking brought international attention; his skin-contact whites and intense Nielluccio reds are now cult wines sought globally.")
for yr, qd, pt, sn in [
    (2018, "good", "stable", "Variable vintage; careful selection essential; some fine wines from best parcels on the peninsula"),
    (2019, "excellent", "stable", "Classic expression; Nielluccio's grippy tannins balanced by ripe fruit; Vermentino at its mineral best"),
    (2020, "very_good", "stable", "Hot summer moderated by sea breezes; ripe generous reds; good structured wines for aging"),
    (2021, "excellent", "rising", "Excellent balance; Nielluccio achieved phenolic ripeness; whites show great mineral precision"),
    (2022, "very_good", "stable", "Typical Mediterranean year; Nielluccio well-ripened with firm tannins; Vermentino shows aromatic intensity"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Domaine Leccia", "winery", r4, "France",
        production_philosophy="biodynamic",
        philosophy_description="Leading Patrimonio estate farmed biodynamically; Annette Leccia produces benchmark Nielluccio and Vermentino; Petra Bianca single parcel is exceptional.",
        reputation_narrative="The most accessible reference for Patrimonio quality; Domaine Leccia's biodynamic approach and single-parcel wines show what Nielluccio and Vermentino can achieve on Corsican schist.",
        price_positioning="premium")

pr4a1, n = PROD("Domaine Leccia Patrimonio Rouge Nielluccio", "wine_still", p4a, r4, "France",
    subcategory="Nielluccio", price_tier="premium",
    description="Benchmark Patrimonio rouge from biodynamic Nielluccio; morello cherry, maquis herbs, leather, mineral earth; firm tannins, fresh acidity; savory Corsican character showing the grape's Sangiovese lineage.")
if n:
    PAIR(pr4a1, "Corsican charcuterie (figatellu, lonzu, coppa)", "complement", "classic", "starter", "The definitive Corsican pairing; Nielluccio's acidity cuts cured meat fat; herbs in wine echo maquis-fed pigs")
    PAIR(pr4a1, "Roast Corsican lamb with maquis herbs", "complement", "classic", "main", "Island lamb; Nielluccio's structure handles the richness; maquis herbs in wine mirror the seasoning")
    PAIR(pr4a1, "Wild boar ragù with pasta", "complement", "established", "main", "Game intensity needs Nielluccio's tannic grip; acidity lifts the rich sauce; Corsican mountain tradition")
    PAIR(pr4a1, "Brocciu cheese (fresh Corsican whey cheese)", "complement", "established", "cheese", "Fresh Corsican cheese; Nielluccio's acidity and tannin balance the rich whey cheese; island pairing")

pr4a2, n = PROD("Domaine Leccia Patrimonio Blanc Vermentino", "wine_still", p4a, r4, "France",
    subcategory="Vermentino", price_tier="premium",
    description="Benchmark Patrimonio blanc; Vermentino on schist soils; white almond, citrus blossom, peach, mineral schist; full body, rich texture with lively acidity; genuine complexity.")
if n:
    PAIR(pr4a2, "Grilled langoustines with herb butter", "complement", "classic", "starter", "Vermentino's mineral richness mirrors the sweetness of langoustines; herb notes echo butter; Mediterranean luxury")
    PAIR(pr4a2, "Sea urchin on toast", "complement", "classic", "amuse", "Briny sea urchin with Vermentino's mineral schist character; almond notes echo the sea; coastal perfection")
    PAIR(pr4a2, "Grilled dorade royale (sea bream) with fennel", "complement", "classic", "fish_course", "Classic Mediterranean fish; Vermentino's anise-adjacent notes echo fennel; mineral finish cleanses")
    PAIR(pr4a2, "Corsican brocciu fiadone (cheese tart)", "complement", "established", "dessert", "Light cheesecake-like tart; Vermentino's floral notes complement; citrus acidity balances sweetness")

p4b = P("Antoine Arena", "winery", r4, "France",
        production_philosophy="natural",
        philosophy_description="Legendary Corsican producer; Antoine Arena and sons make France's most distinctive wines with extended skin contact and absolute minimal intervention; Carco Vermentino rivals great white Burgundy.",
        reputation_narrative="The cult natural wine producer of Corsica; Arena's skin-contact whites and intense Nielluccio reds are among France's most sought-after cult wines; allocation only.",
        price_positioning="ultra_premium")

pr4b1, n = PROD("Antoine Arena Patrimonio Rouge Morta Majo", "wine_still", p4b, r4, "France",
    subcategory="Nielluccio", price_tier="ultra_premium",
    description="Single-vineyard Nielluccio from Morta Majo parcel; wild cherry, garrigue, sun-dried tomato, iron minerality; muscular but elegant; extraordinary aromatic complexity; cult status wine.")
if n:
    PAIR(pr4b1, "Slow-braised Corsican goat with myrtle berries", "complement", "classic", "main", "Rare Corsican preparation; goat's gamey intensity tamed by Nielluccio; myrtle echoes maquis in the wine")
    PAIR(pr4b1, "Grilled Corsican wild boar with chestnuts", "complement", "classic", "main", "Ultimate island pairing; wild boar intensity matches Arena's power; chestnuts echo the forest character")
    PAIR(pr4b1, "Chestnut pasta with wild mushrooms", "complement", "established", "main", "Chestnuts are Corsica's traditional grain; earthy mushrooms bridge wine's mineral depth; island tradition")
    PAIR(pr4b1, "Aged Corsican Niolo cheese", "complement", "established", "cheese", "Strong aged goat/sheep Corsican cheese; only Arena's power can handle it; regional pride pairing")

pr4b2, n = PROD("Antoine Arena Patrimonio Blanc Grotte di Sole", "wine_still", p4b, r4, "France",
    subcategory="Vermentino skin-contact", price_tier="ultra_premium",
    description="Extended skin-contact Vermentino from Grotte di Sole parcel; apricot, dried orange peel, beeswax, saline mineral; grippy texture; oxidative complexity; unique orange wine of great character.")
if n:
    PAIR(pr4b2, "Grilled octopus with olive oil and herbs", "complement", "classic", "starter", "Robust Mediterranean preparation; orange wine's tannins suit the chewy texture; Mediterranean synergy")
    PAIR(pr4b2, "Cured fish (bottarga, dried tuna)", "complement", "established", "starter", "Intense cured fish; skin-contact wine's grip and oxidative character match the intensity; bold pairing")
    PAIR(pr4b2, "Charcuterie and aged cheeses", "complement", "established", "starter", "Skin-contact Vermentino handles rich, complex flavours; tannins cut fat; oxidative notes complement aged products")
    PAIR(pr4b2, "Roasted cauliflower with harissa and raisins", "bridge", "adventurous", "main", "Texture and sweetness in dish; orange wine bridges; harissa heat met by Vermentino's structure")

# 5. SAGRANTINO DI MONTEFALCO DOCG — Italy
print("=== Sagrantino di Montefalco DOCG ===")
r5 = R("Sagrantino di Montefalco DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Sagrantino di Montefalco DOCG",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Umbrian DOCG producing Italy's most tannic wine from the indigenous Sagrantino grape; clay-limestone hills at 300-600m altitude around the medieval hilltop town of Montefalco. Dry red requires 37 months minimum aging (12 in oak, 7 in bottle); the resulting wines are extraordinarily structured and age for 30+ years. Sweet Passito version from dried grapes is traditional at Easter. Sagrantino has the highest tannin levels of any Italian variety.",
        key_producers="Arnaldo Caprai, Paolo Bea, Antonelli San Marco, Tabarrini",
        historical_context="Sagrantino was nearly extinct in the 1970s when Marco Caprai began research into tannin management and modern winemaking. His 25 Anni cuvée (released 1994) revealed Sagrantino's potential and triggered international interest. Paolo Bea's natural approach from the same era showed an entirely different face of the variety. The DOCG was established in 1992, giving legal protection to this unique Umbrian variety that exists nowhere else on earth.")
for yr, qd, pt, sn in [
    (2018, "excellent", "stable", "Warm generous vintage; rich fruit with the characteristic tannin grip; good ageing trajectory"),
    (2019, "very_good", "stable", "Classic Sagrantino expression; firm and structured; decade+ aging potential for top wines"),
    (2020, "exceptional", "rising", "Exceptional Sagrantino; concentrated with extraordinary tannin structure; landmark vintage for the DOCG"),
    (2021, "excellent", "rising", "Excellent vintage; perfect balance of fruit and tannin; wines show great structure for aging"),
    (2022, "very_good", "stable", "Good ripening season; Sagrantino achieved high tannin ripeness; needs extended cellaring as always"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Arnaldo Caprai", "winery", r5, "Italy",
        production_philosophy="research_driven",
        philosophy_description="Marco Caprai single-handedly revived and modernized Sagrantino di Montefalco through 25 years of research into tannin management; 25 Anni is the benchmark wine of the DOCG.",
        reputation_narrative="The producer who transformed Sagrantino from near-extinction to global fame; Arnaldo Caprai's research showed how Sagrantino could be tamed into extraordinary wine; the foundation of modern Montefalco.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("Arnaldo Caprai 25 Anni Sagrantino di Montefalco", "wine_still", p5a, r5, "Italy",
    subcategory="Sagrantino", price_tier="ultra_premium",
    description="Iconic Sagrantino commemorating 25 years of research; dark blackberry, dried violet, licorice, leather, tobacco; immense tannin structure, extraordinary length; transformative with 15+ years aging.")
if n:
    PAIR(pr5a1, "Slow-braised Chianina beef with black truffle", "complement", "classic", "main", "Only Umbria's finest beef can handle Sagrantino's tannin; truffle earthiness bridges; regional luxury apex")
    PAIR(pr5a1, "Wild boar stew with olives and capers (cinghiale)", "complement", "classic", "main", "Umbrian game tradition; wild boar fat tames Sagrantino's ferocious tannins; olives add Mediterranean bridge")
    PAIR(pr5a1, "Lamb shank braised with rosemary and garlic", "complement", "established", "main", "Long braise creates gelatin richness that tames Sagrantino's tannins; rosemary echoes wine's herbal notes")
    PAIR(pr5a1, "Aged Pecorino di Norcia with black truffle honey", "complement", "established", "cheese", "Hard aged sheep cheese stands up to Sagrantino; truffle honey bridges the tannin and fat; Umbrian luxury")

pr5a2, n = PROD("Arnaldo Caprai Montefalco Rosso DOC", "wine_still", p5a, r5, "Italy",
    subcategory="Sangiovese blend", price_tier="mid_range",
    description="Entry to the Caprai range; Sangiovese-dominant blend with Sagrantino for structure; red cherry, herbs, light tannins, fresh acidity; accessible Umbrian red with real character.")
if n:
    PAIR(pr5a2, "Pappardelle with wild boar ragù", "complement", "classic", "main", "Classic Umbrian pasta; Sagrantino component handles the game; Sangiovese freshness cuts the richness")
    PAIR(pr5a2, "Grilled Umbrian sausages with lentils", "complement", "classic", "main", "Umbrian sausage tradition; lentils from Castelluccio are legendary; wine's earthiness bridges perfectly")
    PAIR(pr5a2, "Roast pigeon with truffle sauce", "complement", "established", "main", "Umbrian delicacy; game weight suits Sagrantino; truffle resonates with wine's earthy depth")
    PAIR(pr5a2, "Antipasto misto with Umbrian prosciutto", "complement", "established", "starter", "Regional cured meats; accessible Rosso's tannins and acidity cut the fat; Umbrian tradition")

p5b = P("Paolo Bea", "winery", r5, "Italy",
        production_philosophy="natural",
        philosophy_description="Natural wine legend; Giampiero Bea makes extreme old-school Sagrantino with years in chestnut barrels and no additions; Pagliaro is the reference natural Sagrantino.",
        reputation_narrative="The natural wine counterpoint to Caprai's modernism; Paolo Bea's extreme traditional approach produces Sagrantino of unique austerity and depth; Pagliaro requires a decade of aging but rewards magnificently.",
        price_positioning="ultra_premium")

pr5b1, n = PROD("Paolo Bea Sagrantino di Montefalco Pagliaro", "wine_still", p5b, r5, "Italy",
    subcategory="Sagrantino", price_tier="ultra_premium",
    description="Extreme natural Sagrantino; years in chestnut barrel with no additions; dried fruits, tar, leather, forest floor, iron; austere and profound; requires a decade of aging; benchmark natural wine.")
if n:
    PAIR(pr5b1, "Slow-braised oxtail with dark chocolate sauce", "complement", "established", "main", "Gelatinous oxtail richness handles the tannin; chocolate bridges wine's dried fruit notes; luxurious match")
    PAIR(pr5b1, "Cinghiale (wild boar) braised for 4 hours", "complement", "classic", "main", "Only long-braised game generates enough richness to meet Pagliaro's power; Umbrian apex pairing")
    PAIR(pr5b1, "Aged Salone d'oro lard cured with herbs", "complement", "adventurous", "starter", "Only pure fat can tame Pagliaro's extreme tannins; herbed lard is Umbrian tradition; extreme pairing")
    PAIR(pr5b1, "Aged Umbrian Pecorino stagionato", "complement", "classic", "cheese", "Hard aged sheep cheese; only one of Italy's most powerful wines can pair here; regional tradition")

pr5b2, n = PROD("Paolo Bea Arboreus Trebbiano Spoletino", "wine_still", p5b, r5, "Italy",
    subcategory="Trebbiano Spoletino skin-contact", price_tier="ultra_premium",
    description="Skin-contact Trebbiano Spoletino (indigenous Umbrian variety); dried apricot, chamomile, beeswax, orange peel; grippy tannins from skin contact; oxidative complexity; rare expression of great character.")
if n:
    PAIR(pr5b2, "Umbrian pork liver pâté on grilled bread", "complement", "established", "starter", "Rich offal preparation; orange wine's tannins and oxidative depth match; Umbrian tradition")
    PAIR(pr5b2, "Grilled trout with almond butter and capers", "complement", "established", "fish_course", "Freshwater fish from Umbrian rivers; orange wine handles the richness; caper acidity bridges")
    PAIR(pr5b2, "Chickpea farinata with rosemary", "complement", "established", "starter", "Dense chickpea flatbread; Trebbiano's grip handles the density; rosemary bridges wine's herbal notes")
    PAIR(pr5b2, "Aged Taleggio with chestnut honey", "bridge", "adventurous", "cheese", "Washed-rind cheese with honeyed sweetness; orange wine's tannins balance; chestnut echoes Umbrian landscape")

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
print("B129 complete.")
conn.close()
