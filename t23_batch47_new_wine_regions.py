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

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
        (name, country, region_id, producer_type, description))
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
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. ORVIETO (Italy) ───────────────────────────────────────────────────────
print("\n=== Orvieto (Italy) ===")
r = R("Orvieto", "Italy", "wine",
      designation_type="DOC",
      designation_name="Orvieto DOC / Orvieto Classico DOC",
      reputation_tier="respected",
      quality_trajectory="rediscovering",
      description="One of Central Italy's oldest and most historic white wine appellations, centred on the dramatic tufa hilltop city of Orvieto in Umbria. Traditionally produced from Trebbiano Toscano, Verdello, and Grechetto, Orvieto's historic reputation was built on off-dry and sweet (amabile) styles. Modern producers have pivoted to dry, mineral whites of genuine character from Grechetto — rediscovering the appellation's potential for serious wine.",
      key_producers="Barberani, Tenuta Le Velette, Decugnano dei Barbi, Palazzone, Custodi",
      historical_context="Orvieto has been producing wine since Etruscan times, with the tufa cave cellars beneath the city naturally maintaining ideal storage temperatures. The wine was served at the papal court in Viterbo and was beloved by Renaissance popes and artists. The appellation's decline in the 20th century mirrored that of many Italian whites — squeezed between cheap Soave and more fashionable regions. The Orvieto Classico revival is being led by quality-focused producers working with native Grechetto.")

VIN(r, 2023, "excellent", "rising", "Warm Umbrian season; excellent Grechetto ripeness and mineral precision in Orvieto Classico")
VIN(r, 2022, "very_good", "rising", "Good vintage with the characteristic almond-bitter finish of Grechetto at full expression")
VIN(r, 2021, "good", "stable", "Cooler year; wines of unusual freshness and delicate aromatic character")
VIN(r, 2020, "very_good", "stable", "Hot summer; rich, concentrated whites and well-structured sweet Muffato styles")
VIN(r, 2019, "excellent", "rising", "Benchmark Orvieto vintage; finest Grechetto in recent memory")

p1 = P("Barberani", "Italy", r, "winery",
        "The definitive estate producer of modern Orvieto Classico, Barberani has led the appellation's quality revival with their Calcaia Muffato noble-rot wine and their Castagnolo dry white. Luigi Barberani's family has been farming the Lago di Corbara hillsides for generations, producing wines that demonstrate what Orvieto can achieve with serious viticulture.")
prod1, new1 = PROD("Barberani Castagnolo Orvieto Classico Secco DOC", "wine_still", p1, r, "Italy",
    subcategory="Grechetto Procanico",
    description="Benchmark dry Orvieto Classico; Grechetto-dominant blend with fresh almonds, citrus peel, white peach, and a distinctive mineral-bitter finish that captures the Umbrian terroir beautifully",
    price_tier="mid_range")
if new1:
    PAIR(prod1, "Pasta al tartufo nero di Norcia (black truffle pasta)", "complement", "classic", "main", "The wine's almond and mineral notes are a natural foil for the earthiness of Norcia black truffle in Umbrian pasta")
    PAIR(prod1, "Fritto misto di lago (mixed fried freshwater fish from Lake Corbara)", "complement", "classic", "main", "The local pairing: crisp, mineral Orvieto with fried freshwater fish from the nearby lake — a deeply Umbrian table experience")
    PAIR(prod1, "Bruschetta al pomodoro with local olive oil", "complement", "established", "starter", "Crisp Umbrian white and the simplest bruschetta — citrus and almond notes elevate the tomato and oil")
    PAIR(prod1, "Grilled pigeon with lentils from Castelluccio", "complement", "established", "main", "The wine's mineral precision frames the delicate game bird and the earthy Umbrian lentils beautifully")

p2 = P("Palazzone", "Italy", r, "winery",
        "A highly regarded Orvieto estate producing wines of exceptional concentration and terroir precision from organic vineyards on the Orvieto Classico hills. Their single-vineyard Campo del Guardiano and the Terre Vineate Orvieto are consistently cited as two of the appellation's finest dry whites.")
prod2, new2 = PROD("Palazzone Campo del Guardiano Orvieto Classico Superiore", "wine_still", p2, r, "Italy",
    subcategory="Grechetto Verdello",
    description="Single-vineyard Orvieto Classico Superiore from organic tufa-clay soils; complex, textured, and mineral with white blossom, almonds, and a saline-mineral finish of unusual depth and aging potential",
    price_tier="premium")
if new2:
    PAIR(prod2, "Lago di Corbara perch in acqua pazza (crazy water herb broth)", "complement", "established", "main", "Textured, mineral Orvieto with lake perch in the Umbrian herb broth tradition is one of the region's most elegant local pairings")
    PAIR(prod2, "Castelluccio lentil soup with olive oil and rosemary", "complement", "established", "main", "The wine's earthy depth resonates with the nutty richness of lentil soup from the famous Umbrian plateau")
    PAIR(prod2, "Umbrian cheese selection with truffle honey", "bridge", "suggested", "cheese", "The wine's almond and mineral notes bridge with local sheep's and cow's cheeses and the earthiness of truffle honey")
    PAIR(prod2, "Storione (sturgeon) with capers and lemon from Lake Corbara", "complement", "suggested", "main", "Complex, structured Orvieto Superiore holds up to the meaty firmness of lake sturgeon with bright acidic garnish")

# ── 2. CINQUE TERRE (Italy) ──────────────────────────────────────────────────
print("\n=== Cinque Terre (Italy) ===")
r2 = R("Cinque Terre", "Italy", "wine",
       designation_type="DOC",
       designation_name="Cinque Terre DOC / Sciacchetra DOC",
       reputation_tier="respected",
       quality_trajectory="rediscovering",
       description="One of Italy's most dramatically terraced and challenging wine regions, clinging to the Ligurian Riviera cliffs between Genova and La Spezia. The impossibly steep stone-walled terraces overlook the Mediterranean and are worked by hand — no machinery can reach most vineyards. Bosco, Albarola, and Vermentino produce the region's distinctive dry whites, while the passito Sciacchetra (made from sun-dried grapes) is one of Italy's rarest and most prized sweet wines.",
       key_producers="Cantina Cinque Terre, Buranco, Possa, Forlini Cappellini, Sassarini",
       historical_context="The terraced vineyards of Cinque Terre have been worked since medieval times — a system of stone walls (muretti a secco) built without mortar over centuries holds the steep hillsides in place. At their peak in the 19th century the terraces covered thousands of hectares; today fewer than 200 hectares remain in production as the region's difficult viticulture struggles to attract younger generations. The Cinque Terre National Park protects the remaining terraced landscape.")

VIN(r2, 2023, "excellent", "rising", "Warm Ligurian Riviera season; Bosco and Vermentino of exceptional mineral freshness from the cliff terraces")
VIN(r2, 2022, "very_good", "rising", "Good vintage; wines of characteristic saline, mineral freshness — ideal for Ligurian seafood")
VIN(r2, 2021, "good", "stable", "Cooler Mediterranean year; lighter, aromatic whites with the sea-spray freshness of the terraces")
VIN(r2, 2020, "very_good", "stable", "Hot season; concentrated Bosco with typical mineral lift despite the warmth")
VIN(r2, 2019, "excellent", "rising", "Benchmark vintage; finest Cinque Terre whites in recent years and exceptional Sciacchetra")

p3 = P("Cantina Cinque Terre", "Italy", r2, "winery",
        "The cooperative that has sustained wine production in Cinque Terre for decades, working with the region's 300+ small growers to produce wines from the impossibly steep terraced vineyards. Without this cooperative, Cinque Terre wine would likely have collapsed — their mechanical monorail systems on the cliffs make the logistics of harvesting possible.")
prod3, new3 = PROD("Cantina Cinque Terre Costa de Sera DOC", "wine_still", p3, r2, "Italy",
    subcategory="Bosco Albarola Vermentino",
    description="The benchmark Cinque Terre bianco from cliff-edge terraces; fresh, saline, and mineral with lemon zest, white blossom, dried herbs, and a sea-spray minerality that could only come from Ligurian Riviera vines",
    price_tier="mid_range")
if new3:
    PAIR(prod3, "Trenette al pesto Genovese (pasta with basil pesto)", "complement", "classic", "main", "The definitive Ligurian pairing: saline, herb-edged Cinque Terre white with the region's most iconic pasta and fresh basil sauce")
    PAIR(prod3, "Grilled gamberoni (large Mediterranean prawns) with olive oil and lemon", "complement", "classic", "main", "Saline, mineral Cinque Terre and fresh grilled Ligurian prawns — a seaside classic as simple and pure as it gets")
    PAIR(prod3, "Baccala mantecato (whipped salt cod with olive oil) on crostini", "complement", "established", "starter", "The wine's minerality and citrus precision cut through the rich, emulsified salt cod with the cleanness of sea air")
    PAIR(prod3, "Focaccia di Recco (cheese-filled thin focaccia)", "complement", "classic", "starter", "Saline, fresh Ligurian white and the region's most distinctive cheese flatbread — an effortlessly natural combination")

p4 = P("Possa", "Italy", r2, "winery",
        "A tiny artisan producer making some of the most extreme and terroir-precise wines in all of Italy. Heydi Bonanomi's cliff-edge Cinque Terre Bianco and rare Sciacchetra are produced from minuscule yields on the steepest terraces in Riomaggiore, achieving mineral intensity and complexity that has attracted international wine press attention.")
prod4, new4 = PROD("Possa Sciacchetra Cinque Terre DOC Passito", "wine_dessert", p4, r2, "Italy",
    subcategory="Bosco Albarola",
    description="Italy's rarest passito; sun-dried Bosco and Albarola from cliff-edge terraces — amber-golden with intense dried apricot, orange peel, beeswax, and a distinctive saline mineral finish from the Mediterranean clifftop position",
    price_tier="ultra_premium")
if new4:
    PAIR(prod4, "Aged Parmigiano-Reggiano with local chestnut honey", "complement", "classic", "cheese", "Saline, honeyed Sciacchetra with crystalline aged Parmesan and chestnut honey — one of Italy's greatest aged cheese pairings")
    PAIR(prod4, "Cannoli Siciliani with ricotta and candied orange peel", "complement", "established", "dessert", "The wine's candied citrus and honey complexity resonates with the sweet ricotta and orange in the iconic pastry")
    PAIR(prod4, "Gorgonzola Naturale with walnut bread", "contrast", "classic", "cheese", "Rare sweet wine and powerful blue cheese — the contrast of briny-sweet Sciacchetra against Gorgonzola Naturale is stunning")
    PAIR(prod4, "Dried fig and almond torrone nougat", "complement", "suggested", "dessert", "The wine's dried fruit and Mediterranean herb character echo the fig and almond in the Ligurian holiday confection")

# ── 3. GRANIT (Austria — Kamptal alternative) ── use KREMSTAL clarification
# Actually let's do Ribeauville/Alsace Haut-Rhin instead
# No, let's go: Trentino DOC (already done)
# Let's do: Colheita / Vintage Porto context – OR Serra Gaucha Brazil
# Better: do Valpolicella Superiore / Ripasso as distinct from Valpolicella DOC
# OR Grosseto Maremma (Morellino done) — let's do CASTILLA Y LEON or CAMPO DE BORJA

# Actually let's pick:
# 3. Cotes du Rhone Villages (France) — distinct from generic CDR; Rasteau, Chusclan etc
# 4. Campo de Borja (Spain) — Garnacha old vines; underrated; very global significance
# 5. Serra Gaucha (Brazil) — Wine heartland of Brazil; Italian heritage; significant for S America coverage

print("\n=== Cotes du Rhone Villages (France) ===")
r3 = R("Cotes du Rhone Villages", "France", "wine",
       designation_type="AOC",
       designation_name="Cotes du Rhone Villages AOC",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="The quality tier above generic Cotes du Rhone, allowing 22 named village appellations to append their name to the label. The top villages — Rasteau, Cairanne, Roaix, Valreas, Visan — produce wines rivalling Gigondas and Vacqueyras in quality from old-vine Grenache, Syrah, and Mourvedre. An underappreciated gateway to the finest southern Rhone wines at approachable prices, with remarkable consistency across the diverse village terroirs.",
       key_producers="Domaine Brusset, Chateau Saint-Maurice, Domaine de la Janasse, Domaine Grand Veneur, Domaine Sainte Anne",
       historical_context="The Cotes du Rhone Villages designation was created in 1966 to recognise superior quality wine zones within the broader Cotes du Rhone appellation. Cairanne became the first village to be promoted to its own independent AOC in 2016, demonstrating the designation's role as a quality pathway. Rasteau followed with its own red wine AOC in 2010, further confirming the Villages system as a genuine quality marker.")

VIN(r3, 2023, "excellent", "rising", "Excellent southern Rhone harvest; old-vine Grenache of rare fruit depth and village-level mineral character")
VIN(r3, 2022, "very_good", "rising", "Very good Rhone vintage; structured, layered reds with the characteristic garrigue and dark fruit of the Villages")
VIN(r3, 2021, "good", "stable", "Cooler year; more elegant, higher-acid style ideal for food pairing across the village appellation range")
VIN(r3, 2020, "excellent", "rising", "Benchmark Villages vintage; concentrated, age-worthy old-vine Grenache from all 22 villages")
VIN(r3, 2019, "very_good", "stable", "Classic year with reliable quality; particularly fine Rasteau and Cairanne")

p5 = P("Domaine Brusset", "France", r3, "winery",
        "One of the benchmarks for Cotes du Rhone Villages quality, Domaine Brusset produces exceptional wines from Cairanne — the first Villages appellation to achieve independent AOC status. Their Les Hauts de Montmirail and Cairanne Cotes du Rhone Villages wines demonstrate the full quality potential of old-vine Grenache from the region's best hillside terroirs.")
prod5, new5 = PROD("Domaine Brusset Cairanne Cotes du Rhone Villages", "wine_still", p5, r3, "France",
    subcategory="Grenache Syrah Mourvedre",
    description="Benchmark Cairanne red from the village that earned its own AOC; old-vine Grenache with garrigue, warm dark cherry, dried herbs, and a long structured finish — the southern Rhone at its most authentic and accessible",
    price_tier="mid_range")
if new5:
    PAIR(prod5, "Grilled lamb chops with tapenade and Provence herbs", "complement", "classic", "main", "Grenache-based Rhone Villages and grilled lamb with wild herbs and olive tapenade — the quintessential Provencal combination")
    PAIR(prod5, "Cassoulet de Castelnaudary with duck confit and pork", "complement", "classic", "main", "Rich, dark-fruited southern Rhone red is the natural partner for the slow-baked bean and duck stew of the southwest")
    PAIR(prod5, "Tapenade on toast with anchovy and hard-boiled egg", "complement", "established", "starter", "The wine's olive and wild herb notes echo the tapenade flavours, creating seamless Mediterranean harmony")
    PAIR(prod5, "Aged Comté or Beaufort cheese with crusty baguette", "bridge", "suggested", "cheese", "Warm, fruit-forward Grenache bridges naturally with the nutty, caramelised complexity of fine mountain cheese")

p6 = P("Domaine Grand Veneur", "France", r3, "winery",
        "A highly regarded Rhone Valley estate producing wines across the regional hierarchy from Cotes du Rhone to Chateauneuf-du-Pape. Their Cotes du Rhone Villages Les Champauvins is widely considered one of the best wines in the Villages tier — complex, concentrated, and built for the cellar at an accessible price point.")
prod6, new6 = PROD("Domaine Grand Veneur Cotes du Rhone Villages Les Champauvins", "wine_still", p6, r3, "France",
    subcategory="Grenache Syrah",
    description="Top-tier Cotes du Rhone Villages; old-vine Grenache and Syrah from limestone terraces — dark cherry, black olive, garrigue, and pepper with a long, mineral finish demonstrating what this appellation can achieve",
    price_tier="mid_range")
if new6:
    PAIR(prod6, "Daube Provencale (slow-braised beef with olives and orange)", "complement", "classic", "main", "The wine's dark fruit, olive, and orange blossom notes mirror the classic flavours of the regional braised beef")
    PAIR(prod6, "Magret de canard with cherry and Armagnac reduction", "complement", "established", "main", "Rich, cherry-fruited Grenache pairs beautifully with Gascon duck breast in the classic southwest preparation")
    PAIR(prod6, "Socca (Nicoise chickpea crepe) with rosemary and olive oil", "complement", "established", "starter", "The wine's herbal warmth resonates with the nutty, crispy chickpea crepe of the Riviera")
    PAIR(prod6, "Ratatouille Nicoise with fresh herbs and olive oil", "complement", "established", "main", "Warm, fruity Rhone red and the quintessential summer vegetable stew of Provence — deeply Mediterranean and satisfying")

# ── 4. CAMPO DE BORJA (Spain) ────────────────────────────────────────────────
print("\n=== Campo de Borja (Spain) ===")
r4 = R("Campo de Borja", "Spain", "wine",
       designation_type="DO",
       designation_name="DO Campo de Borja",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="An Aragon wine region southwest of Zaragoza, famous for producing some of the world's best-value Garnacha from old, gnarly bush vines on poor clay and limestone soils. Campo de Borja has been nicknamed the Empire of Garnacha — and with justification. Old-vine Garnacha from the foothills of the Moncayo massif achieves extraordinary concentration, violet-spice character, and warm Mediterranean depth at remarkably low prices.",
       key_producers="Bodegas Borsao, Alto Moncayo, Bodega Aragonesas, Ejeana",
       historical_context="Campo de Borja was awarded DO status in 1977, but its reputation for quality was built much later when producers discovered that the region's old, ungrafted Garnacha bush vines — some over 80 years old — could produce wines of Priorat-level complexity at a fraction of the price. The Garnacha del Mundo project brought international attention, and the region's cooperatives shifted from bulk to quality production in the 2000s.")

VIN(r4, 2023, "very_good", "rising", "Warm Aragon growing season; old-vine Garnacha of exceptional violet-spice concentration")
VIN(r4, 2022, "excellent", "rising", "Outstanding vintage; finest Campo de Borja old-vine Garnacha in recent memory")
VIN(r4, 2021, "good", "stable", "Cooler year; more elegant, higher-acid style; excellent for food pairing")
VIN(r4, 2020, "very_good", "stable", "Hot growing season; concentrated, deeply coloured old-vine Garnacha with good aging potential")
VIN(r4, 2019, "excellent", "rising", "Benchmark vintage; most concentrated and complex Garnacha from the Moncayo foothills in years")

p7 = P("Alto Moncayo", "Spain", r4, "winery",
        "The prestige producer of Campo de Borja, Alto Moncayo has transformed the region's international reputation with limited-production old-vine Garnacha wines from the Moncayo massif at 800m altitude. Their Aquilon and Campo de Borja Garnacha are critically acclaimed as some of Spain's finest Garnacha expressions at any price.")
prod7, new7 = PROD("Alto Moncayo Campo de Borja Garnacha DO", "wine_still", p7, r4, "Spain",
    subcategory="Garnacha",
    description="Prestigious old-vine Garnacha from 800m altitude on the Moncayo massif; intense violet, dark plum, black pepper, and licorice with powerful concentration and a long, mineral finish — Campo de Borja at its summit",
    price_tier="premium")
if new7:
    PAIR(prod7, "Slow-roasted Churra lamb shoulder with garlic and rosemary", "complement", "classic", "main", "Old-vine Aragon Garnacha and regional lamb is the quintessential Spanish pairing — concentrated fruit and structure match the richness of slow-cooked lamb")
    PAIR(prod7, "Grilled morcilla de Burgos with caramelised onion and peppers", "complement", "established", "main", "The wine's violet-spice intensity stands up to the rich, spiced blood sausage of Aragon")
    PAIR(prod7, "Lengua de ternera estofada (braised veal tongue with vegetables)", "complement", "established", "main", "Powerful, structured Garnacha holds up to the rich, gelatinous braised veal preparation")
    PAIR(prod7, "Aged Manchego DOP with quince paste and walnuts", "bridge", "established", "cheese", "The wine's dark fruit intensity bridges with sharp aged Manchego and the sweet-tart membrillo")

p8 = P("Bodegas Borsao", "Spain", r4, "winery",
        "The dominant cooperative producer of Campo de Borja and the most widely distributed label from the region. Borsao's Tres Picos Garnacha is one of Spain's most popular premium wines globally — offering old-vine Campo de Borja character at exceptional value.")
prod8, new8 = PROD("Bodegas Borsao Tres Picos Garnacha Campo de Borja DO", "wine_still", p8, r4, "Spain",
    subcategory="Garnacha",
    description="Spain's most widely distributed premium old-vine Garnacha; plush, concentrated, and warmly spiced with dark cherry, raspberry, violets, and pepper — extraordinary value from Aragon's most famous cooperative",
    price_tier="mid_range")
if new8:
    PAIR(prod8, "Grilled Iberian presa (pork shoulder cut) with chimichurri", "complement", "established", "main", "Plush, violet-fruited Garnacha mirrors the richness and sweetness of Iberian pork shoulder")
    PAIR(prod8, "Patatas bravas with spicy tomato sauce and aioli", "complement", "classic", "starter", "Warm, fruity old-vine Garnacha and the most Spanish of tapas bar classics — fun, bold, and entirely regional")
    PAIR(prod8, "Cochinillo asado (Segovian suckling pig)", "complement", "classic", "main", "Concentrated, warm Garnacha is the classic Spanish match for crispy-skinned whole suckling pig")
    PAIR(prod8, "Migas Aragonesas with egg, grapes, and chorizo", "complement", "classic", "main", "The wine's dark fruit and spice resonates with the Aragonese peasant dish of fried breadcrumbs with sausage and fruit")

# ── 5. SERRA GAUCHA (Brazil) ─────────────────────────────────────────────────
print("\n=== Serra Gaucha (Brazil) ===")
r5 = R("Serra Gaucha", "Brazil", "wine",
       designation_type="IP",
       designation_name="IP Serra Gaucha",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="Brazil's most important wine-producing region, in the highlands of Rio Grande do Sul near the border with Argentina and Uruguay. Serra Gaucha sits at 600-900m altitude with a temperate climate shaped by Italian immigrant winemakers who arrived in the 1870s. The region produces sparkling wines of genuine quality alongside still wines from both Italian varieties (Moscato Bianco, Prosecco/Glera) and international grapes. The Brazilian sparkling wine industry — led by sparkling wine specialists in the Vale dos Vinhedos — is the most internationally recognised aspect of Serra Gaucha production.",
       key_producers="Miolo Wine Group, Cave Geisse, Peterlongo, Casa Valduga, Lidio Carraro",
       historical_context="Italian immigrants from Veneto and Trentino settled the Serra Gaucha highlands from 1875, bringing winemaking traditions from northeastern Italy. The cooperative tradition established by these settlers dominated wine production for a century, producing primarily sweet Moscato and simple table wines. The quality revolution began in the 1970s-80s when Cave Geisse introduced traditional method sparkling wine production and Miolo invested in international varieties.")

VIN(r5, 2023, "very_good", "rising", "Good Serra Gaucha growing season; sparkling base wines of fine acidity and tropical fruit")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage for Brazilian sparkling; finest methode traditionnelle base wines in recent years")
VIN(r5, 2021, "good", "stable", "Reliable vintage; consistent quality in Moscato Bianco and sparkling production")
VIN(r5, 2020, "very_good", "stable", "Good highland season; fine Espumante production and improving still red quality")
VIN(r5, 2019, "very_good", "stable", "Classic Serra Gaucha vintage; Cave Geisse sparked international interest with exceptional vintage")

p9 = P("Cave Geisse", "Brazil", r5, "winery",
        "The pioneer of quality traditional method sparkling wine in Brazil, Swiss-Brazilian winemaker Mario Geisse introduced Champagne-method production to Serra Gaucha in 1979 and has never looked back. Their Brut and Blanc de Blancs sparkling wines are considered Brazil's finest and have won international competitions against French Champagne.")
prod9, new9 = PROD("Cave Geisse Brut Nature Serra Gaucha IP", "wine_sparkling", p9, r5, "Brazil",
    subcategory="Chardonnay Pinot Noir",
    description="Brazil's benchmark traditional method sparkling wine; Chardonnay-dominant with fine, persistent bubbles, fresh citrus, toasted brioche, and a clean mineral finish — remarkable quality from the Brazilian highlands",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "Ostras (fresh Brazilian oysters) from Santa Catarina", "complement", "classic", "starter", "Brazil's finest sparkling wine with fresh oysters from the southern coast — a local luxury pairing gaining recognition")
    PAIR(prod9, "Camarao na moranga (prawns in pumpkin cream)", "complement", "established", "main", "The wine's bright acidity and fine bubbles cut through the rich pumpkin cream and sweet prawn filling beautifully")
    PAIR(prod9, "Coxinha de galinha (chicken croquettes) with catupiry cream cheese", "complement", "classic", "starter", "Brazilian sparkling and the country's most beloved street food — bubbles and acidity cut through the fried dough and creamy filling")
    PAIR(prod9, "Peixe grelhado com mandioquinha (grilled fish with yellow potato puree)", "complement", "established", "main", "Fine sparkling wine with grilled freshwater fish and the earthy sweetness of South American yellow potato — a modern Brazilian fine dining pairing")

p10 = P("Miolo Wine Group", "Brazil", r5, "winery",
         "Brazil's largest premium wine producer and the company most responsible for elevating Brazilian wine's international profile. Miolo's Lote 43 Merlot and Cuvee Giuseppe sparkling wine have won international competitions, and the company's diverse portfolio — from sparkling to reserve reds — represents the full ambition of modern Brazilian viticulture.")
prod10, new10 = PROD("Miolo Cuvee Giuseppe Brut Serra Gaucha IP", "wine_sparkling", p10, r5, "Brazil",
    subcategory="Chardonnay Pinot Noir Riesling",
    description="Brazilian premium sparkling wine tribute to Italian founder; fresh, aromatic, and well-structured with green apple, biscuit, and the lively acidity of high-altitude Serra Gaucha fruit",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Bolinho de bacalhau (salt cod fritters) with lime", "complement", "classic", "starter", "Brazil's beloved salt cod fritter with crisp, acid sparkling wine — bubbles and acidity cut through the salt-rich fried treat")
    PAIR(prod10, "Linguica toscana grilled with cassava farofa", "complement", "established", "main", "The wine's freshness and acidity provide welcome contrast to the smoky, fatty Italian-Brazilian sausage with earthy cassava")
    PAIR(prod10, "Salpicao de frango (Brazilian chicken salad with cream and olives)", "complement", "established", "main", "Light, fresh sparkling resonates with the tangy, creamy Brazilian chicken salad with a clean fizz refresh")
    PAIR(prod10, "Strawberry and cream cake (bolo de morango) from Serra Gaucha", "complement", "classic", "dessert", "Fresh, aromatic Brazilian sparkling and the cream-strawberry cake of the highlands — the regional celebration combination")

# ── COUNTS ───────────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nTotal regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("\nDone.")
conn.close()
