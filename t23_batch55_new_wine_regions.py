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

# ── 1. Yarra Valley (Australia/Victoria) ─────────────────────────────────────
print("\n=== Yarra Valley (Australia) ===")
r1 = R("Yarra Valley", "Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Yarra Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Victoria's most celebrated cool-climate wine region, the Yarra Valley sits in the foothills of the Great Dividing Range east of Melbourne, producing Pinot Noir and Chardonnay of Burgundian elegance alongside vibrant Shiraz, Cabernet Franc and sparkling wines. The Yarra's diversity of elevations and soils — from the fertile lower valley flats to the cooler Upper Yarra granite hills — enables a remarkable range of wine styles, with the finest Upper Yarra Pinot Noirs and Chardonnays rivalling some of Australia's greatest. Home to pioneering estates since the 1860s.",
    key_producers="Yering Station, De Bortoli Yarra, Coldstream Hills, Giant Steps, Oakridge",
    historical_context="The Yarra Valley holds a unique place in Australian wine history — the first vines were planted in 1838 by the Ryrie brothers at Yering Station, making it one of Victoria's oldest wine regions. After phylloxera devastated Victorian vineyards in the 1890s, the Yarra was abandoned for over 70 years. The modern revival began with Yering Station's replanting in 1962 and James Halliday's Coldstream Hills in 1985, establishing the modern quality benchmark. Today the Valley is Melbourne's cellar door destination, hosting 150+ producers across its diverse sub-regions.")

VIN(r1, 2023, "excellent", "stable", "Outstanding Yarra vintage; Pinot Noir of exceptional elegance and Chardonnay of fine mineral precision")
VIN(r1, 2022, "very_good", "stable", "Warm year with good fruit concentration; generous, approachable Yarra Pinot and Chardonnay")
VIN(r1, 2021, "excellent", "stable", "Classic Yarra character; elegant, cool-influenced Pinot Noir and structured Chardonnay")
VIN(r1, 2020, "very_good", "stable", "Good vintage despite fire smoke concerns; Upper Yarra producers made excellent wines of genuine character")
VIN(r1, 2019, "exceptional", "rising", "One of Yarra Valley's finest vintages; benchmark Pinot Noir and Chardonnay of extraordinary complexity and aging potential")

p1a = P("Oakridge Wines", "Australia", r1, description="One of the Yarra Valley's most exciting and progressive producers, Dave Bicknell's Oakridge estate produces single-vineyard, single-block expressions of Pinot Noir and Chardonnay that have consistently achieved outstanding critical scores and established the producer as one of Australia's finest voices for cool-climate Victoria.")
prod1a, new1a = PROD("Oakridge 864 Single Block Pinot Noir Yarra Valley", "wine_still", p1a, r1, "Australia",
    subcategory="Pinot Noir",
    description="One of the Yarra Valley's most critically acclaimed single-block Pinot Noirs — from a single elevated block in the Upper Yarra, showing silky red cherry, earth and iron mineral character with the linear, cool-climate precision that distinguishes great Yarra Pinot from warmer Australian expressions.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Duck confit with pickled cherries and lentils", "complement", "classic", "main", "Yarra Valley's finest Pinot Noir with Victorian duck — the wine's red cherry and earth notes frame the confit's richness in a pairing of Burgundian logic transposed to the Dandenong Ranges.")
    PAIR(prod1a, "Rabbit rillettes with grain mustard and toast", "complement", "established", "starter", "The wine's delicate tannin and cool-climate precision are the ideal companion for rabbit's lean, gentle protein — one of Pinot's classic light meat pairings.")
    PAIR(prod1a, "Yarra Valley mushroom tart with thyme and gruyere", "complement", "classic", "main", "Forest mushroom and cheese tart with Valley Pinot — earthy umami mirrored by the wine's earth and iron mineral character in a locally complete pairing.")
    PAIR(prod1a, "Aged Milawa Blue cheese with walnut bread", "complement", "established", "cheese", "Victorian blue cheese from the alpine foothills with the Valley's finest Pinot — the wine's fruit and acidity provide the definitive sweet-tart contrast.")

p1b = P("Giant Steps Winery", "Australia", r1, description="One of the Yarra Valley's most consistent and internationally acclaimed estates, Phil Sexton's Giant Steps produces benchmark single-vineyard Pinot Noir and Chardonnay from the Valley's finest sites, with a philosophy of minimal intervention and maximum terroir expression that has earned consistent high scores from international critics.")
prod1b, new1b = PROD("Giant Steps Harry's Monster Chardonnay Yarra Valley", "wine_still", p1b, r1, "Australia",
    subcategory="Chardonnay",
    description="A landmark Yarra Valley Chardonnay from Giant Steps' finest blocks — showing white peach, citrus, cashew and mineral complexity with impeccably balanced natural acidity and subtle oak integration that ages magnificently and represents the finest expression of Australian cool-climate Chardonnay.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled Victorian rock lobster with lime beurre blanc", "complement", "classic", "main", "The wine's mineral precision and citrus-driven freshness frame rock lobster's sweet flesh with aristocratic cool-climate elegance.")
    PAIR(prod1b, "Seared flathead with capers, lemon and butter", "complement", "established", "main", "Victorian flathead — one of the country's finest coastal fish — with cool-climate Chardonnay; the wine's mineral precision mirrors the fish's delicate sweetness.")
    PAIR(prod1b, "Corn-fed chicken with morel cream sauce", "complement", "classic", "main", "Chardonnay's most universal partnership — chicken with cream and mushroom — elevated by the Yarra's distinctive mineral freshness into something genuinely exciting.")
    PAIR(prod1b, "Camembert from Yarra Valley Dairy with truffle honey", "complement", "classic", "cheese", "The Valley's own soft-ripened cheese with its finest white wine — local terroir expressed simultaneously through food and wine in the most direct possible pairing.")

# ── 2. Colchagua Valley (Chile) ───────────────────────────────────────────────
print("\n=== Colchagua Valley (Chile) ===")
r2 = R("Colchagua Valley", "Chile",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Valle de Colchagua DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's most prestigious red wine appellation and one of South America's most internationally recognised wine regions, Colchagua Valley lies 180km south of Santiago in the Rapel Valley, producing powerful Carmenere, Cabernet Sauvignon, Syrah and Malbec of warm-climate intensity and genuine terroir complexity. The region's warm days, cool nights, Pacific-influenced morning fog and diverse soils from alluvial to coastal granite have made Colchagua home to Chile's most internationally celebrated red wine estates.",
    key_producers="Montes, Casa Lapostolle, Los Vascos, Bisquertt, Clos Apalta",
    historical_context="Colchagua's wine history began with Spanish colonial settlers in the 16th century, but modern quality viticulture dates from the 1980s when international investment and improved technology transformed the Central Valley's potential. Aurelio Montes's pioneering work at Montes Winery in the 1990s established that Colchagua's warm climate could produce world-class red wines rather than just bulk product. The crowning achievement came with Clos Apalta's recognition in 2008 when Wine Spectator named their flagship wine the World's Best Wine — the first Latin American wine to receive the honour.")

VIN(r2, 2023, "excellent", "stable", "Outstanding Chilean year; Colchagua Carmenere and Cabernet of exceptional ripeness and structure")
VIN(r2, 2022, "very_good", "stable", "Reliable vintage; powerful, fruit-forward Colchagua reds with good tannic structure")
VIN(r2, 2021, "excellent", "stable", "Fine balance; elegant expressions of Carmenere and Cabernet from the valley's finest sites")
VIN(r2, 2020, "very_good", "stable", "Good concentration from the dry season; authentic Colchagua character across all red varieties")
VIN(r2, 2019, "exceptional", "rising", "Benchmark Colchagua vintage; concentrated, age-worthy reds of international quality recognition")

p2a = P("Montes Winery", "Chile", r2, description="Chile's most internationally exported and celebrated winery, Aurelio Montes pioneered quality winemaking in Colchagua from the late 1980s, producing the Montes Alpha and Montes Folly that helped establish Chile's reputation for world-class Carmenere and Syrah. Today Montes is one of South America's most ambitious and innovative wine producers.")
prod2a, new2a = PROD("Montes Purple Angel Carmenere Colchagua Valley DO", "wine_still", p2a, r2, "Chile",
    subcategory="Carmenere, Petit Verdot",
    description="Chile's most celebrated premium Carmenere — Montes Purple Angel from Colchagua's finest parcels, showing the variety's signature deep violet colour, dark cherry, chocolate, plum and distinctive green pepper note; structured tannins and aged complexity that establish Carmenere as Chile's truly unique contribution to the world's great red wine varieties.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Chilean prime ribeye with chimichurri and Andean potato", "complement", "classic", "main", "The wine's dark intensity and structured tannins frame Chilean prime beef with the authority its quality demands — Carmenere's natural affinity for red meat expressed at its most compelling.")
    PAIR(prod2a, "Slow-cooked lamb shoulder with cumin and coriander", "complement", "established", "main", "The wine's plum depth and herbal green note bridge spiced lamb in a Middle Eastern-Chilean fusion of surprising coherence.")
    PAIR(prod2a, "Roasted duck with dark cherry and balsamic", "complement", "classic", "main", "Carmenere's cherry-fruit depth and structured tannins match duck's richness with classical logic, the balsamic bridging the wine's dark fruit.")
    PAIR(prod2a, "Aged Chilean Manchego-style cheese with quince", "complement", "established", "cheese", "The wine's dark complexity and fine tannins are balanced by the nutty cheese and sweet quince in a Chilean-Spanish cheese pairing of refinement.")

p2b = P("Casa Lapostolle", "Chile", r2, description="One of Colchagua's most prestigious and internationally recognised estates, founded by the French Marnier-Lapostolle family (Grand Marnier) with Michel Rolland as winemaking consultant, producing the legendary Clos Apalta — the wine that made Wine Spectator's Wine of the Year in 2008 — alongside excellent single-varietal expressions of Carmenere and Merlot.")
prod2b, new2b = PROD("Casa Lapostolle Clos Apalta Colchagua Valley DO", "wine_still", p2b, r2, "Chile",
    subcategory="Carmenere, Merlot, Cabernet Sauvignon",
    description="Chile's most celebrated wine and the first Latin American wine named Wine Spectator Wine of the Year — a complex blend dominated by Carmenere from century-old dry-farmed vines on Colchagua's finest granite and clay sites; showing extraordinary dark fruit concentration, silky tannin, mineral depth and the complexity that justifies international comparison with the world's finest red wines.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Asado whole-roasted suckling pig on the grill", "complement", "classic", "main", "The wine's powerful concentration and silky tannins are perfectly matched by the suckling pig's caramelised skin and tender flesh in a celebratory Chilean pairing of genuine luxury.")
    PAIR(prod2b, "Truffle-studded beef tenderloin with bone marrow jus", "elevate", "adventurous", "main", "The wine's extraordinary complexity and mineral depth elevate beef and truffle into a pairing that justifies Chile's finest wine receiving the world's greatest wine award.")
    PAIR(prod2b, "Wild mushroom and blue cheese tart with herbs", "complement", "established", "main", "The wine's mineral depth and dark fruit complexity find an unexpected but satisfying companion in the earthy, funky blue cheese-mushroom tart.")
    PAIR(prod2b, "Aged Mahon cheese with dried fig and walnut", "complement", "established", "cheese", "The wine's dark intensity is balanced by aged cheese's crystalline nuttiness and the sweet-tart dried fig in a cheese course of international character.")

# ── 3. Jumilla (Spain) ────────────────────────────────────────────────────────
print("\n=== Jumilla (Spain) ===")
r3 = R("Jumilla", "Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Jumilla DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Spain's most important Monastrell (Mourvèdre) appellation, Jumilla in Murcia and Castilla-La Mancha produces powerful, concentrated red wines and increasingly vibrant rosés from ungrafted dry-farmed Monastrell bush vines — many over 50 years old — on limestone and sandy soils at 600–900m altitude. The extreme continental climate with 40°C summers and -5°C winters creates exceptional fruit concentration in the old-vine Monastrell, making Jumilla one of Spain's most exciting value and premium wine regions.",
    key_producers="Bodegas Juan Gil, Casa Castillo, Bodegas Carchelo, El Nido, Paco Garcia",
    historical_context="Jumilla's Monastrell vines predate phylloxera — the sandy limestone soils that killed the European wine industry's grafted vines elsewhere protected Jumilla's own-rooted bush vines, making this one of the world's most significant repositories of pre-phylloxera viticulture. The DO was established in 1966; international recognition came in the 1990s when importers discovered the extraordinary value of Jumilla's concentrated, concentrated Monastrell. Today producers like Casa Castillo are producing world-class wines that challenge the notion that Monastrell is merely Spain's workhorse variety.")

VIN(r3, 2023, "excellent", "stable", "Outstanding Monastrell year in Jumilla; bush vine concentration and complexity at their finest")
VIN(r3, 2022, "very_good", "stable", "Good vintage; powerful, concentrated Monastrell with the characteristic Jumilla dusty mineral character")
VIN(r3, 2021, "excellent", "stable", "Fine balance in extreme climate; elegant Monastrell of remarkable freshness given Jumilla conditions")
VIN(r3, 2020, "very_good", "stable", "Reliable dry year; concentrated, age-worthy Jumilla reds from stressed ungrafted old vines")
VIN(r3, 2019, "excellent", "rising", "Benchmark Jumilla vintage; extraordinary old-vine Monastrell of international calibre")

p3a = P("Casa Castillo", "Spain", r3, description="Jumilla's most internationally celebrated and critically acclaimed producer, Jose Maria Vicente's estate farms biodynamically from old-vine ungrafted Monastrell bush vines to produce wines of extraordinary complexity and elegance that have established Jumilla as Spain's most surprising fine wine region, with Pie Franco — from oldest pre-phylloxera vines — achieving legendary status.")
prod3a, new3a = PROD("Casa Castillo Pie Franco Monastrell Jumilla DO", "wine_still", p3a, r3, "Spain",
    subcategory="Monastrell",
    description="Spain's most celebrated Monastrell — from pre-phylloxera ungrafted Monastrell bush vines over 100 years old on the Jumilla limestone plateau, biodynamically farmed by Jose Maria Vicente, producing wines of extraordinary depth, complexity and freshness that challenge the assumption that Monastrell is incapable of producing wine at the highest level.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Slow-roasted Murcian lamb with romesco sauce", "complement", "classic", "main", "The wine's concentrated dark fruit and earthy mineral depth frame Murcian lamb's richness with rustic Spanish authority — Monastrell and local lamb is Jumilla's most natural pairing.")
    PAIR(prod3a, "Wild boar stew with dried orange peel and thyme", "complement", "established", "main", "Pre-phylloxera Monastrell's intensity handles wild boar's gamey richness with dark fruit and mineral depth while the orange peel bridges the wine's aromatic complexity.")
    PAIR(prod3a, "Paella de marisco with saffron and mussels", "complement", "adventurous", "main", "An unexpected but revealing pairing — the wine's concentration and earthy depth create an intriguing tension with the saffron-spiked shellfish rice.")
    PAIR(prod3a, "Manchego cheese aged 12 months with membrillo", "complement", "classic", "cheese", "Spain's most celebrated cheese and its most exciting Monastrell — the wine's concentrated fruit and fine tannins are perfectly balanced by the nutty manchego and sweet quince paste.")

p3b = P("Bodegas Juan Gil", "Spain", r3, description="One of Jumilla's most consistent and internationally distributed quality producers, Juan Gil Hernandez's family estate produces benchmark Monastrell at exceptional value, with their aged selections demonstrating the variety's capacity for genuine complexity and aging potential from Jumilla's extraordinary old ungrafted vineyards.")
prod3b, new3b = PROD("Bodegas Juan Gil Blue Label Monastrell Jumilla DO", "wine_still", p3b, r3, "Spain",
    subcategory="Monastrell",
    description="One of Spain's most celebrated value wines — Juan Gil's Blue Label Monastrell from old-vine ungrafted Jumilla bush vines, showing extraordinary dark fruit concentration, dark chocolate, mineral and dried herbs character at a price that makes it one of the world's most outstanding quality-value propositions in red wine.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Chorizo al vino with crusty bread", "complement", "classic", "starter", "The wine's dark fruit and mineral depth are the perfect companion for Spanish chorizo cooked in red wine — a Murcia-inspired pairing of rustic authenticity.")
    PAIR(prod3b, "Albondigas in tomato sauce with pine nuts", "complement", "established", "main", "Spanish meatballs in rich tomato sauce find their natural red wine companion in concentrated Monastrell, the tomato's acidity bridging the wine's dark fruit.")
    PAIR(prod3b, "Lamb chops a la brasa with salsa de mojo rojo", "complement", "classic", "main", "Grilled Murcian lamb chops with spiced pepper sauce and the region's most famous grape — a pairing of complete regional logic and culinary satisfaction.")
    PAIR(prod3b, "Queso de Murcia al vino with grapes", "complement", "classic", "cheese", "Murcia's distinctive red-rind cheese (washed in Monastrell wine) with the same variety in the glass — a circular pairing of wine and cheese united by a shared grape.")

# ── 4. Faugères (France/Languedoc) ────────────────────────────────────────────
print("\n=== Faugeres (France) ===")
r4 = R("Faugeres", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Faugères AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of Languedoc's most distinctive and quality-focused appellations, Faugères produces powerful, aromatic reds and increasingly exciting whites and rosés from Grenache, Syrah, Mourvèdre and Carignan on the schist soils of the foothills north of Béziers. The appellation's unique friable schist — which drains perfectly, retains heat and imparts a distinctive mineral character — combined with the Mediterranean climate and altitude creates wines of concentration, complexity and genuine terroir expression that distinguish Faugères from generic Languedoc.",
    key_producers="Domaine Leon Barral, Chateau des Estanilles, Domaine Alquier, Chateau de la Liquiere",
    historical_context="Faugères received AOC status in 1982 — one of the first Languedoc villages to do so — recognising the schist terroir's unique contribution to wine quality. The region was a beneficiary of the late 20th-century Languedoc quality revolution, attracting passionate small producers who rejected the industrial co-operative model for authentic expression of the schist landscape. Léon Barral's biodynamic approach established Faugères' reputation for authentic natural winemaking, and today the appellation is considered one of southern France's most philosophically consistent and quality-focused regions.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Mediterranean year; Faugères schist Grenache and Syrah of remarkable mineral complexity")
VIN(r4, 2022, "very_good", "stable", "Warm but structured; good concentration from the schist with the appellation's characteristic mineral character")
VIN(r4, 2021, "excellent", "stable", "Elegant and precise; one of the decade's finest Faugères vintages with fine acidity and mineral depth")
VIN(r4, 2020, "very_good", "stable", "Reliable southern year; authentic schist expression across Grenache, Syrah and Mourvèdre")
VIN(r4, 2019, "exceptional", "rising", "One of Faugères finest recent vintages; age-worthy, complex schist reds of benchmark quality")

p4a = P("Domaine Leon Barral", "France", r4, description="The most philosophically revered and internationally celebrated Faugères producer, Didier Barral farms biodynamically without chemicals, tractors or irrigation on his Lentheric estate, producing old-vine Faugères reds of extraordinary concentration, mineral depth and authenticity that have established the appellation's reputation as one of southern France's great terroir-driven wine regions.")
prod4a, new4a = PROD("Domaine Leon Barral Faugeres AOC Rouge", "wine_still", p4a, r4, "France",
    subcategory="Grenache, Carignan, Cinsault, Mourvèdre",
    description="The benchmark biodynamic Faugères from one of Languedoc's most revered and philosophically consistent producers — a field blend of old-vine southern varieties on pure schist, showing extraordinary dark fruit concentration, iron mineral depth, garrigue aromatics and the telltale schist signature that makes Faugères uniquely compelling among southern French reds.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Daube provencale with olives and orange zest", "complement", "classic", "main", "Provencal-Languedoc beef stew with the region's schist-mineral Grenache blend — the wine's dark fruit and garrigue herbs mirror the daube's slow-braised aromatic depth.")
    PAIR(prod4a, "Grilled Camargue bull beef with herbes de Provence", "complement", "established", "main", "Wild Camargue cattle with Languedoc's most mineral red — garrigue herbs and schist terroir create a pairing of unmistakable Mediterranean identity.")
    PAIR(prod4a, "Cassoulet with Toulouse sausage and duck confit", "complement", "classic", "main", "Languedoc's great bean and meat cassole dish with its most characterful schist red — a southern French pairing of extraordinary cultural depth and gastronomic satisfaction.")
    PAIR(prod4a, "Aged Pelardon goat cheese with lavender honey", "complement", "classic", "cheese", "Languedoc's indigenous goat cheese with Faugères schist red — the wine's mineral depth and garrigue aromatics complement the fresh goat tang while lavender honey bridges both.")

p4b = P("Chateau des Estanilles", "France", r4, description="One of Faugères' most historic and consistent estates, Château des Estanilles produces a comprehensive range of schist-terroir wines from estate vineyards on the highest slopes of the appellation, with their Cuvée Syrah and Prestige in particular showing the variety's extraordinary capacity for mineral complexity on Faugères schist soils.")
prod4b, new4b = PROD("Chateau des Estanilles Cuvee Syrah Faugeres AOC", "wine_still", p4b, r4, "France",
    subcategory="Syrah",
    description="A benchmark Faugères Syrah from high-altitude schist vineyards — showing the Northern Rhône variety's capacity for mineral precision and aromatic complexity in a southern setting, with violet, dark cherry, bacon and distinctive schist mineral character that distinguishes it from both Châteauneuf and Côtes du Rhône expressions.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled duck magret with lavender and honey jus", "complement", "classic", "main", "Syrah's natural affinity for duck is enhanced by Faugères' garrigue herbs — the wine's violet and smoked meat notes frame the lavender-honey jus with southern French elegance.")
    PAIR(prod4b, "Braised rabbit with olives, capers and tomato", "complement", "established", "main", "Mediterranean braised rabbit with Languedoc Syrah — the wine's savoury depth and mineral character frame the olive-tomato braise with rustic southern French authority.")
    PAIR(prod4b, "Merguez sausage with harissa and roasted peppers", "complement", "established", "main", "North African-influenced Languedoc merguez with schist Syrah — the wine's dark fruit and mineral depth bridge the spice while its garrigue character links the Mediterranean peppers.")
    PAIR(prod4b, "Tomme de Brebis sheep milk cheese with quince", "complement", "classic", "cheese", "Southern French sheep cheese with Faugères Syrah — the wine's mineral depth and fine tannin frame the lanolin-rich cheese with the quince providing sweet-tart bridge.")

# ── 5. Pouilly-Fuissé (France/Burgundy) ──────────────────────────────────────
print("\n=== Pouilly-Fuisse (France) ===")
r5 = R("Pouilly-Fuisse", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Pouilly-Fuissé AOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Southern Burgundy's most celebrated white wine appellation, Pouilly-Fuissé produces Chardonnay from the dramatic limestone cliffs and gentle slopes around the four communes of Fuissé, Solutré-Pouilly, Vergisson and Chaintré in the Mâconnais. The volcanic and limestone soils, southern exposure and maritime influence create Chardonnay of significant weight, mineral complexity and the capacity to age — stylistically between Côte de Beaune Chardonnay and richer Mâcon, now elevated by a new Premier Cru classification (2020) recognising the finest vineyard sites.",
    key_producers="Domaine Ferret, Domaine J.A. Ferret, Chateau des Rontets, Domaine Valette, Verget",
    historical_context="Pouilly-Fuissé's history as a recognised quality wine region dates to the 18th century, but its modern reputation was built after World War II when the appellation gained international recognition in the USA. The 2020 recognition of 22 Premier Cru vineyard sites — after decades of lobbying — confirmed Pouilly-Fuissé's place among Burgundy's serious appellations and created new quality benchmarks for the Mâconnais region's finest Chardonnay expressions.")

VIN(r5, 2023, "excellent", "stable", "Outstanding Burgundy south; Pouilly-Fuissé Chardonnay of remarkable mineral precision and Mâconnais warmth")
VIN(r5, 2022, "very_good", "stable", "Warm year with good concentration; generous, ripe Pouilly-Fuissé with stone fruit and mineral character")
VIN(r5, 2021, "excellent", "stable", "Elegant and precise; benchmark Pouilly-Fuissé vintage with fine mineral character and Premier Cru potential realised")
VIN(r5, 2020, "very_good", "stable", "Good ripeness; the first year with Premier Cru labelling; excellent benchmark for the new classification")
VIN(r5, 2019, "excellent", "rising", "One of the Mâconnais's finest recent vintages; concentrated, mineral Pouilly-Fuissé of genuine aging potential")

p5a = P("Domaine Ferret", "France", r5, description="Pouilly-Fuissé's most historically celebrated and internationally recognised estate, Domaine Ferret produces the appellation's benchmark wines from old-vine Chardonnay parcels including the legendary Hors Classe selections — wines of extraordinary mineral depth and longevity that demonstrate Pouilly-Fuissé's capacity for world-class Chardonnay.")
prod5a, new5a = PROD("Domaine Ferret Hors Classe Pouilly-Fuisse AOC", "wine_still", p5a, r5, "France",
    subcategory="Chardonnay",
    description="The most celebrated Pouilly-Fuissé — Domaine Ferret's extraordinary Hors Classe bottling from the oldest, lowest-yielding vines on the estate's finest parcels, showing remarkable mineral concentration, hazelnut, white peach and limestone complexity that ages magnificently for 15–20 years and places Pouilly-Fuissé firmly among Burgundy's serious white wine appellations.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Quenelles de brochet with sauce Nantaise butter", "complement", "classic", "main", "Southern Burgundy's finest Chardonnay with one of France's most refined fish preparations — delicate pike dumplings in butter sauce demand a white wine of precisely this mineral, textural character.")
    PAIR(prod5a, "Veal sweetbreads with cream and morels", "complement", "classic", "main", "The wine's rich mineral texture and complex hazelnut notes frame veal sweetbreads and morel mushroom cream in a pairing of classical French gastronomic refinement.")
    PAIR(prod5a, "Pan-roasted langoustine with fennel butter", "complement", "established", "main", "The wine's limestone mineral precision and citrus notes frame sweet langoustine with elegant southern Burgundy authority.")
    PAIR(prod5a, "Aged Saint-Andre cheese with truffle honey", "complement", "established", "cheese", "The wine's creamy, mineral complexity mirrors the rich triple-cream cheese while truffle honey bridges the Chardonnay's earthy depth.")

p5b = P("Verget Maconnais", "France", r5, description="Jean-Marie Guffens-Heynen's celebrated négociant-éleveur, consistently producing some of Pouilly-Fuissé's finest and most mineral Chardonnays through meticulous selection of the best parcels and uncompromising winemaking that has established Verget as one of the Mâconnais's most reliable and exciting producers across a range of appellation wines.")
prod5b, new5b = PROD("Verget Terres de Fuisse Pouilly-Fuisse AOC", "wine_still", p5b, r5, "France",
    subcategory="Chardonnay",
    description="A benchmark négociant Pouilly-Fuissé from Verget's finest Fuissé parcel selections — showing the appellation's characteristic combination of Mâconnais warmth and limestone mineral precision in a wine of excellent concentration, white peach, hazelnut and mineral character at an accessible price.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Scallops with cauliflower puree and brown butter", "complement", "classic", "main", "The wine's creamy texture and mineral character complement the scallop's sweetness and cauliflower's earthiness in a classic Burgundy white-shellfish pairing.")
    PAIR(prod5b, "Roasted chicken with garlic cream sauce and tarragon", "complement", "classic", "main", "Chardonnay's most universal pairing elevated by the Pouilly-Fuissé's mineral weight — cream sauce, aromatic tarragon and the wine's limestone precision create harmonious balance.")
    PAIR(prod5b, "Gratin de truffes aux oeufs", "complement", "adventurous", "main", "Truffle and egg gratin — the Mâconnais variation of Burgundy's most luxurious egg preparation — finds its ideal companion in the mineral, concentrated southern Burgundy Chardonnay.")
    PAIR(prod5b, "Comté cheese 18 months with toasted hazelnuts", "complement", "classic", "cheese", "The wine's own hazelnut character mirrors the aged Comté's nutty depth while the limestone mineral character links the regional Alpine-Burgundy cheese pairing.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
