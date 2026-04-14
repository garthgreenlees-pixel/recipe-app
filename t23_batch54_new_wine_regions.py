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

# ── 1. Eden Valley (Australia/South Australia) ────────────────────────────────
print("\n=== Eden Valley (Australia) ===")
r1 = R("Eden Valley", "Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Eden Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="South Australia's highest-altitude cool-climate wine region, situated at 400–600m in the Barossa Ranges east of the Barossa Valley. Eden Valley produces some of Australia's finest Riesling — renowned for its extraordinary lime-mineral precision and capacity to age for 20+ years — alongside elegant Shiraz that contrasts dramatically with the Barossa's warm-climate power. Henschke's Hill of Grace, from 100+ year old Shiraz vines, is one of Australia's most celebrated and historically significant wines.",
    key_producers="Henschke, Yalumba, Pewsey Vale, Eden Road, Irvine",
    historical_context="Eden Valley's viticulture predates the Barossa Valley itself, with German Lutheran settlers planting Riesling in the 1840s. The cool altitude was originally considered a disadvantage; only in the 20th century was it recognised as producing Riesling of superior minerality and longevity. The discovery of ancient pre-phylloxera Shiraz vines by Cyril Henschke in the 1950s — the Hill of Grace vineyard — created Australia's most historic and sought-after red wine property. Today Eden Valley's Riesling and old-vine Shiraz represent Australian wine heritage at its most precious.")

VIN(r1, 2023, "excellent", "stable", "Superb Eden Valley vintage; Riesling of remarkable mineral precision and classic cool-climate finesse")
VIN(r1, 2022, "very_good", "stable", "Good year with fine altitude-preserved acidity; elegant Riesling and structured Hill of Grace-style Shiraz")
VIN(r1, 2021, "excellent", "stable", "Classic vintage; benchmark Eden Riesling and fine old-vine Shiraz expressing the valley's signature cool mineral character")
VIN(r1, 2020, "very_good", "stable", "Reliable cool season; Hill of Grace-style elegance preserved despite warm Australian conditions")
VIN(r1, 2019, "exceptional", "rising", "One of Eden Valley's finest recent vintages; age-worthy Riesling and complex old-vine Shiraz of benchmark quality")

p1a = P("Henschke", "Australia", r1, description="One of Australia's most revered winery dynasties, the Henschke family has farmed Eden Valley since 1868 and now produces Hill of Grace — Australia's most celebrated and sought-after Shiraz — from a single historic vineyard of pre-phylloxera vines over 130 years old, alongside benchmark Mount Edelstone Shiraz and the finest Eden Valley Rieslings.")
prod1a, new1a = PROD("Henschke Hill of Grace Eden Valley Shiraz", "wine_still", p1a, r1, "Australia",
    subcategory="Shiraz",
    description="Australia's most historically significant and internationally celebrated red wine — Shiraz from 100+ year old ungrafted pre-phylloxera vines in the Hill of Grace vineyard, producing wine of extraordinary complexity, fine-grained tannins, dark fruit, dark chocolate, aged beef and iron mineral character that requires 10–20 years to reach its peak and ages magnificently for 40+ years.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Aged dry-aged Coorong beef ribeye with bone marrow", "complement", "classic", "main", "Australia's most profound red wine with its most exceptional dry-aged beef — the wine's aged complexity and fine tannins create a pairing of historical and gastronomic significance.")
    PAIR(prod1a, "Braised Barossa Valley pork belly with apple jus", "complement", "established", "main", "The wine's mineral elegance and fine fruit contrast beautifully with the richness of slow-cooked pork, the apple jus bridging the Shiraz's dark fruit.")
    PAIR(prod1a, "Roasted South Australian lamb rack with rosemary", "complement", "classic", "main", "Australian lamb from nearby pastoral country with the state's most celebrated red wine — terroir expressed simultaneously through animal and vine in a pairing of national significance.")
    PAIR(prod1a, "Aged Australian cheddar with truffle honey", "complement", "established", "cheese", "The wine's extraordinary complexity finds its equal in mature Australian cheddar, the truffle honey bridging the wine's earthy depth.")

p1b = P("Pewsey Vale Vineyard", "Australia", r1, description="One of Eden Valley's oldest estates and benchmark Riesling producers, Pewsey Vale was established in 1847 and produces consistently excellent Eden Valley Riesling — their Contours Museum Reserve in particular, released after 5 years, demonstrates the extraordinary aging potential of this cool-altitude Australian Riesling.")
prod1b, new1b = PROD("Pewsey Vale The Contours Museum Reserve Riesling Eden Valley", "wine_still", p1b, r1, "Australia",
    subcategory="Riesling",
    description="The definitive expression of aged Eden Valley Riesling — released after 5 years with remarkable petrol, toast, honey and lime complexity that demonstrates why cool-altitude South Australian Riesling is one of the world's great aged white wine experiences.",
    price_tier="mid_range")
if new1b:
    PAIR(prod1b, "Smoked South Australian salmon with creme fraiche", "complement", "classic", "starter", "Aged Riesling's toasty complexity and preserved citrus acidity create the perfect foil for smoked salmon's richness in a classic Australian fine-dining pairing.")
    PAIR(prod1b, "Thai-style steamed barramundi with lemongrass and chilli", "contrast", "established", "main", "The wine's petrol and lime complexity cuts through Thai aromatics and chilli heat with the same brilliance as great German Spätlese.")
    PAIR(prod1b, "Prawn bisque with saffron and cream", "complement", "established", "main", "Aged Riesling's honeyed toast and mineral precision handle bisque richness while preserving freshness through the cream.")
    PAIR(prod1b, "Aged Gruyere with roasted hazelnuts", "complement", "established", "cheese", "The wine's developed toasty complexity mirrors aged Gruyere's nutty depth in a pairing where both wine and cheese have evolved through patient ageing.")

# ── 2. Swartland (South Africa) ───────────────────────────────────────────────
print("\n=== Swartland (South Africa) ===")
r2 = R("Swartland", "South Africa",
    beverage_family="wine",
    designation_type="WO",
    designation_name="Swartland WO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="South Africa's most exciting and philosophically distinctive wine region, Swartland lies north of Cape Town on the western Cape's Paardeberg and Kasteelberg granite mountains, where old-vine dry-farmed bush vines of Chenin Blanc, Syrah, Grenache and Carignan produce wines of extraordinary concentration, mineral depth and complexity. The Swartland Revolution — a loose movement of natural winemakers led by Eben Sadie, Chris Alheit and others — established the region as the heartland of South Africa's most progressive and internationally celebrated wine culture.",
    key_producers="Sadie Family Wines, Alheit Vineyards, Mullineux Family, Leeuwenkuil, AA Badenhorst",
    historical_context="Swartland's wine history is ancient — Huguenot settlers farmed wheat and wine here from the late 17th century — but its fine wine revolution is recent. In the early 2000s, Eben Sadie began seeking old dry-farmed bush vines of Chenin Blanc and Rhone varieties on the granitic slopes and producing wines that challenged South African wine's conventional focus on the Cape Winelands. The Swartland Independent Producers' Collective (2010) formalised a movement that had already become internationally celebrated, establishing Swartland as one of the world's most exciting natural wine regions.")

VIN(r2, 2023, "excellent", "stable", "Outstanding year for dry-farmed Swartland bush vines; Chenin Blanc and Syrah of remarkable concentration and granitic mineral character")
VIN(r2, 2022, "very_good", "stable", "Good year; old bush vine concentration with fine Swartland mineral depth across white and red varieties")
VIN(r2, 2021, "excellent", "stable", "Elegant and complex; one of the decade's finest Swartland vintages for both Chenin Blanc and Rhone varieties")
VIN(r2, 2020, "very_good", "stable", "Classic Swartland character; concentrated, mineral bush vine wines of authentic expression")
VIN(r2, 2019, "exceptional", "rising", "Among the finest Swartland vintages ever; extraordinary concentration and mineral precision from low-yielding dry-farmed vines")

p2a = P("Sadie Family Wines", "South Africa", r2, description="The most internationally celebrated and philosophically important winery in South Africa, Eben Sadie's small-production wines from Swartland's oldest bush vines have achieved cult status worldwide and established South Africa as a serious participant in global fine wine culture, winning multiple accolades as Africa's finest winery.")
prod2a, new2a = PROD("Sadie Family Palladius Swartland WO", "wine_still", p2a, r2, "South Africa",
    subcategory="Chenin Blanc, Grenache Blanc, Clairette Blanche, Viognier",
    description="South Africa's most celebrated white wine — a complex field blend of white varieties from old dry-farmed bush vines on Swartland granite, showing extraordinary mineral depth, waxy texture, citrus oil, white flowers and granite mineral character that has established Eben Sadie as one of the world's greatest winemakers and Swartland as a world-class wine region.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Whole-roasted Cape Malay spiced chicken with apricot", "complement", "established", "main", "The wine's aromatic complexity and texture handle the warm spice and apricot sweetness of Cape Malay cuisine with extraordinary elegance — South African terroir expressed through both kitchen and vineyard.")
    PAIR(prod2a, "Grilled Saldanha Bay abalone with lemon butter", "complement", "classic", "main", "South Africa's most precious shellfish with its most celebrated white wine — both expressions of the Western Cape's unique environment.")
    PAIR(prod2a, "Pan-fried line-caught snoek with apricot jam", "complement", "classic", "main", "Cape Town's most iconic fish preparation — barbecued snoek with apricot glaze — finds its most sophisticated companion in the textural, complex Palladius.")
    PAIR(prod2a, "Aged Karoo Camembert with Swartland wheat rusk", "complement", "established", "cheese", "The wine's waxy complexity and mineral depth complement the dense, earthy matured Camembert from the Karoo plateau in a distinctly South African pairing.")

p2b = P("Mullineux Family Wines", "South Africa", r2, description="Chris and Andrea Mullineux's acclaimed Swartland estate consistently produces some of the region's finest Syrah, Chenin Blanc and Straw Wine, winning International Winery of the Year (Wine Enthusiast) in 2016 — the first African winery to achieve the honour — and establishing Swartland's international reputation for world-class wine.")
prod2b, new2b = PROD("Mullineux Old Vines White Swartland WO", "wine_still", p2b, r2, "South Africa",
    subcategory="Chenin Blanc",
    description="A benchmark expression of old-vine Swartland Chenin Blanc from Mullineux's dry-farmed bush vine parcels on granite and slate — showing extraordinary complexity of quince, citrus oil, beeswax and granite mineral character that represents the pinnacle of South African Chenin Blanc production and challenges the finest Chenins of the Loire Valley.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Borek with feta and spinach, harissa oil", "complement", "adventurous", "starter", "The wine's waxy complexity and mineral freshness complement North African-Cape Malay-influenced pastries in a South African fusion pairing of regional cultural depth.")
    PAIR(prod2b, "Roasted Cape Bream with fennel and orange", "complement", "established", "main", "Atlantic Cape fish with the Swartland's finest Chenin — the wine's citrus and mineral drive frame the sweet white fish with elegant restraint.")
    PAIR(prod2b, "Bobotie with turmeric rice and chutney", "complement", "established", "main", "South Africa's national dish — Cape Malay spiced meat with egg custard topping — finds a textural, complex companion in old-vine Swartland Chenin that matches the dish's cultural complexity.")
    PAIR(prod2b, "Aged Boerenkaas farmhouse Gouda with quince preserve", "complement", "classic", "cheese", "The wine's quince and beeswax notes mirror the aged farmhouse Gouda's caramel depth in a South African cheese pairing of quiet authority.")

# ── 3. Nahe (Germany) ─────────────────────────────────────────────────────────
print("\n=== Nahe (Germany) ===")
r3 = R("Nahe", "Germany",
    beverage_family="wine",
    designation_type="Anbaugebiet",
    designation_name="Nahe Qualitätswein",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Germany's most diverse and mineralogically complex wine region, the Nahe Valley in Rhineland-Palatinate stands between the volcanic soils of the Mosel and the limestone of Rheinhessen. The variety of geological formations — porphyry, volcanic rhyolite, blue slate, quartzite and loam — creates an extraordinary patchwork of terroir, with each mineral expression captured in the Riesling that dominates the region. Nahe Riesling combines the Mosel's delicacy with Rheinhessen's body, often with a distinctive mineral complexity that is unique in German wine.",
    key_producers="Schlossgut Diel, Donnhoff, Emrich-Schonleber, Kruger-Rumpf, Staatliche Weinbaudomane",
    historical_context="The Nahe was designated a separate German wine region (Anbaugebiet) only in 1971, having previously been classified under Rheinhessen. The river Nahe — a tributary of the Rhine — gives its name to the region. Helmut Dönnhoff's extraordinary work from the 1970s elevated the region's international profile, producing Rieslings from the Hermannshöhle and Oberhäuser Brücke vineyards that are now considered among Germany's finest and most age-worthy expressions of the variety.")

VIN(r3, 2023, "excellent", "stable", "Outstanding German vintage; Nahe Riesling of extraordinary mineral diversity and aromatic precision")
VIN(r3, 2022, "very_good", "stable", "Good year with fine balance; Nahe's diverse geology producing wines of characteristic complexity")
VIN(r3, 2021, "excellent", "stable", "Elegant and precise; benchmark vintage for Nahe's full range of mineral Riesling expressions")
VIN(r3, 2020, "very_good", "stable", "Reliable year; complex mineral Rieslings across Nahe's diverse terroir patchwork")
VIN(r3, 2019, "exceptional", "rising", "One of Germany's finest recent vintages; Nahe Riesling of exceptional concentration and mineral diversity")

p3a = P("Donnhoff Weingut", "Germany", r3, description="Germany's most internationally celebrated Nahe producer and one of the country's finest winemakers, Helmut Dönnhoff's estate produces Rieslings from the Hermannshöhle and Oberhäuser Brücke vineyards that are considered benchmarks for German Riesling's capacity to combine mineral complexity with aromatic purity and extraordinary aging potential.")
prod3a, new3a = PROD("Donnhoff Norheimer Hermannshohle Riesling Spatlese Nahe", "wine_still", p3a, r3, "Germany",
    subcategory="Riesling",
    description="One of Germany's most celebrated Riesling Spätlese — from the legendary Hermannshöhle vineyard on blue slate and volcanic porphyry soils above the Nahe River, showing the variety's most complete expression: extraordinary mineral complexity, white peach, apricot, citrus and floral aromatics with classic Spätlese residual sweetness perfectly balanced by high natural acidity.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Alsatian Munster cheese with cumin bread", "complement", "established", "cheese", "Germany's greatest Spätlese with Alsace's most pungent cheese — the wine's sweetness and acidity balance the washed-rind intensity while mineral depth elevates both.")
    PAIR(prod3a, "Seared duck liver with cherry compote", "complement", "established", "starter", "The wine's apricot-peach sweetness and firm acidity create the classic German Spätlese duck liver pairing — fruit and richness in perfect tension.")
    PAIR(prod3a, "Thai red curry with coconut milk and Thai basil", "contrast", "classic", "main", "The wine's residual sweetness and high acidity are the definitive foil for Thai curry's chilli heat and coconut creaminess — a globally celebrated pairing.")
    PAIR(prod3a, "Riesling-braised pork belly with sauerkraut", "complement", "classic", "main", "The wine's own variety used to braise the pork — Riesling Spätlese with Riesling-cooked pork creates a circular German pairing of complete logic and satisfaction.")

p3b = P("Emrich-Schonleber", "Germany", r3, description="One of the Nahe's finest and most consistent estates, Frank Schönleber produces benchmark Rieslings from the Monzinger Halenberg and Frühlingsplätzchen vineyards on complex volcanic soils that express the Nahe's unique mineral diversity in wines of extraordinary precision, mineral character and aging potential.")
prod3b, new3b = PROD("Emrich-Schonleber Monzinger Halenberg Riesling Auslese Nahe", "wine_still", p3b, r3, "Germany",
    subcategory="Riesling",
    description="A benchmark Nahe Auslese from the volcanic Halenberg vineyard — intense apricot, peach and honey sweetness from noble rot-affected grapes balanced by the Nahe's characteristic mineral tension and high natural acidity, creating a wine of extraordinary complexity and multi-decade aging potential.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Foie gras avec brioche et compote de coings", "complement", "classic", "starter", "The wine's intense sweetness and high acidity with mineral precision create the definitive sweet wine-foie gras pairing in a German-French crossing of gastronomic traditions.")
    PAIR(prod3b, "Apfelstrudel mit Sahne", "complement", "established", "dessert", "Austrian apple strudel's warm spice and pastry richness find their perfect German companion in the wine's apricot-apricot sweetness and fresh acidity.")
    PAIR(prod3b, "Blue cheese from Allgäu with honey and walnuts", "complement", "classic", "cheese", "The wine's concentrated sweetness and mineral depth provide the definitive German counterpoint to blue cheese pungency in the classic sweet wine-blue cheese contrast pairing.")
    PAIR(prod3b, "Vanilla panna cotta with peach compote", "complement", "established", "dessert", "The wine's peach and apricot concentration mirrors the fruit compote while its acidity cuts through the cream's richness — a wine that outlives the dessert in complexity.")

# ── 4. Pfalz (Germany) ────────────────────────────────────────────────────────
print("\n=== Pfalz (Germany) ===")
r4 = R("Pfalz", "Germany",
    beverage_family="wine",
    designation_type="Anbaugebiet",
    designation_name="Pfalz Qualitätswein",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Germany's largest and sunniest wine region, the Pfalz (Palatinate) stretches along the Haardt Mountains west of the Rhine in Rhineland-Palatinate, producing the country's most food-versatile and internationally accessible Rieslings alongside excellent Pinot Noir (Spätburgunder), Pinot Gris and Dornfelder. The Pfalz's warmer, drier climate produces riper, fuller-bodied Rieslings than the Mosel — often completely dry — that pair superbly with food and represent outstanding value at all quality levels.",
    key_producers="Muller-Catoir, A. Christmann, Dr. Bürklin-Wolf, Bassermann-Jordan, Knipser",
    historical_context="The Pfalz was Germany's most important wine region for centuries — the Roman emperor Probus encouraged viticulture here in 280 AD, and the medieval prince-bishops of Speyer maintained vast vineyard holdings. The Deutsche Weinstrasse (German Wine Route), established in 1935, made the Pfalz Germany's most visited wine tourism region. Post-war quality reforms transformed the Pfalz from mass production to premium dry Riesling; producers like Müller-Catoir's Hans-Günter Schwarz established that Pfalz's warm-climate Riesling could rival the Mosel's elegance with its own distinct full-bodied character.")

VIN(r4, 2023, "excellent", "stable", "Outstanding German year; Pfalz Riesling of remarkable full-bodied precision and spice; excellent Spätburgunder")
VIN(r4, 2022, "very_good", "stable", "Warm and generous; ripe, full-bodied Pfalz Riesling and well-structured Pinot Noir")
VIN(r4, 2021, "excellent", "stable", "Elegant and precise; fine dry Riesling and cool-influenced Spätburgunder of great finesse")
VIN(r4, 2020, "very_good", "stable", "Classic Pfalz character; full-bodied dry Riesling and structured Dornfelder of good concentration")
VIN(r4, 2019, "exceptional", "rising", "Germany's finest recent vintage perfectly expressed in Pfalz's full-bodied dry Riesling of extraordinary complexity")

p4a = P("Muller-Catoir", "Germany", r4, description="The Pfalz's most internationally celebrated estate and the producer that established dry Pfalz Riesling as a world-class wine style, Müller-Catoir's Hans-Günter Schwarz produced wines of extraordinary concentration and complexity for three decades; the estate continues under Martin Müller with the same commitment to the highest dry Riesling expression in the Pfalz.")
prod4a, new4a = PROD("Muller-Catoir Haardter Burgergarten Riesling Pfalz", "wine_still", p4a, r4, "Germany",
    subcategory="Riesling",
    description="A benchmark dry Pfalz Riesling from the Haardt village's finest vineyard — showing the full-bodied, spicy, textural character that distinguishes Pfalz from the Mosel, with white peach, apricot kernel, white pepper and complex mineral depth from the vineyard's deep limestone soils.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Sauerbraten with gingersnap gravy and red cabbage", "complement", "classic", "main", "Germany's most complex marinated beef dish meets the Pfalz's most complex dry Riesling — the wine's spice and mineral texture perfectly frame the sweet-sour richness of the sauerbraten gravy.")
    PAIR(prod4a, "Flammkuchen with crème fraiche, onion and lardons", "complement", "classic", "main", "Alsatian-Palatine tarte flambée and dry Pfalz Riesling are the region's most natural pairing — the wine's full body and spice cut through the cream while complementing the onion sweetness.")
    PAIR(prod4a, "Saumagen (stuffed pig's stomach) with mustard", "complement", "classic", "main", "The Pfalz's most famous regional dish — Helmut Kohl's favourite — demands the region's most characterful dry Riesling to cut through its substantial richness.")
    PAIR(prod4a, "Camembert au four with rosemary and garlic", "complement", "established", "cheese", "The wine's textural richness and mineral precision complement the earthy, runny baked camembert with the same authority as Burgundy Chardonnay but with distinctly German spice.")

p4b = P("A. Christmann Weingut", "Germany", r4, description="One of the Pfalz's most respected and internationally celebrated producers, Steffen Christmann produces biodynamic dry Rieslings from the legendary Idig and Reiterpfad GG (Grosses Gewächs) sites that represent the Pfalz's greatest expressions of full-bodied, complex dry Riesling at its most intellectually and gastronomically compelling.")
prod4b, new4b = PROD("A. Christmann Riesling Grosses Gewachs Konigsbacher Idig Pfalz", "wine_still", p4b, r4, "Germany",
    subcategory="Riesling",
    description="One of Germany's finest Grosses Gewächs — biodynamic dry Riesling from the legendary Idig GG site above the Haardt Mountains, showing extraordinary mineral complexity, precision and the full-bodied power unique to the Pfalz's finest dry Rieslings; among Germany's most collectable and age-worthy dry whites.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "Roasted whole Dover sole with parsley butter", "complement", "established", "main", "The wine's mineral precision and full body frame delicate flatfish with aristocratic dignity — dry Pfalz Riesling's finest gastronomic moment.")
    PAIR(prod4b, "Langoustine with Riesling butter sauce and chives", "complement", "classic", "main", "Using the wine's own variety in the sauce — Riesling-steamed langoustine with Riesling beurre blanc — creates a self-referential pairing of complete harmony.")
    PAIR(prod4b, "White asparagus with Hollandaise and ham", "complement", "classic", "main", "Germany's most celebrated seasonal pairing — Spargel with Hollandaise and the Pfalz's finest dry Riesling — a combination of regional tradition and gastronomic logic.")
    PAIR(prod4b, "Aged Bergkase mountain cheese with walnut bread", "complement", "established", "cheese", "The wine's complex mineral depth and textural richness mirror alpine mountain cheese's nutty, crystalline character in an Alpine-Rhineland cheese pairing of quiet authority.")

# ── 5. Maule Valley (Chile) ───────────────────────────────────────────────────
print("\n=== Maule Valley (Chile) ===")
r5 = R("Maule Valley", "Chile",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Valle del Maule DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Chile's largest wine appellation and one of its most historically important, Maule Valley sits 250km south of Santiago in the Central Valley, where the highest concentration of old-vine Carmenere, Pais and Cabernet Sauvignon in Chile is found. Maule's continental climate, granitic decomposed soils and the dry-farming tradition of subsistence viticulture have preserved vineyard material of extraordinary historical significance — some Pais vines date back 250 years. A quality revolution led by natural winemakers has elevated Maule from bulk wine to one of South America's most exciting old-vine regions.",
    key_producers="Garage Wine Co, De Martino, Gillmore, Bouchon, Vigno Collective",
    historical_context="Maule's viticulture dates from Spanish colonial settlement in the 16th century, with Jesuit missions establishing vineyards of Pais (Mission grape) for sacramental wine. The Central Valley's agriculture dominated 20th-century Chilean wine production, with Maule providing much of the bulk wine that depressed Chile's reputation. The Vignadores de Carignan (Vigno) collective, formed in 2009, changed the conversation by identifying the extraordinary old-vine Carignan and Pais heritage hidden in Maule's dry-farmed coastal hillsides and marketing them as Chile's greatest old-vine treasure.")

VIN(r5, 2023, "excellent", "stable", "Outstanding Chilean year; Maule old-vine Carignan and Pais of remarkable concentration and mineral character")
VIN(r5, 2022, "very_good", "stable", "Good season; dry-farmed bush vine concentration well-expressed across Carmenere and old Pais")
VIN(r5, 2021, "excellent", "stable", "Fine balance; elegant old-vine Carmenere and complex Carignan showing Maule's terroir at its finest")
VIN(r5, 2020, "very_good", "stable", "Reliable dry year; old-vine concentration from drought-stressed bush vines of exceptional character")
VIN(r5, 2019, "excellent", "rising", "Benchmark Maule vintage; concentrated, mineral old-vine wines establishing the region's serious fine wine credentials")

p5a = P("Garage Wine Co", "Chile", r5, description="The most internationally celebrated pioneer of Maule Valley's old-vine revolution, Derek Mossman Knapp's Garage Wine Co sources from old dry-farmed Carmenere, Pais and Carignan vineyards throughout Maule, producing wines of extraordinary concentration, mineral character and authenticity that have established the region as Chile's most exciting old-vine discovery.")
prod5a, new5a = PROD("Garage Wine Co Carignan Lot 49 Maule Valley DO", "wine_still", p5a, r5, "Chile",
    subcategory="Carignan",
    description="One of Chile's most exciting old-vine discoveries — Carignan from ancient dry-farmed bush vines in Maule's coastal granite hills, showing extraordinary dark fruit concentration, iron mineral, spice and the fierce tannin structure that old Carignan uniquely delivers; a wine of international quality hiding in South America's most overlooked wine region.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Cazuela de vacuno Chilean beef stew with corn", "complement", "classic", "main", "Chile's most comforting traditional stew — slow-braised beef with corn, potato and pumpkin — finds its most authentic companion in the concentrated, mineral old-vine Maule Carignan.")
    PAIR(prod5a, "Asado al palo whole lamb on a cross", "complement", "classic", "main", "Chilean asado's most theatrical preparation — whole lamb split-roasted over fire — demands a wine of old-vine intensity to match the smoke and char.")
    PAIR(prod5a, "Conger eel caldillo with potato and cilantro", "bridge", "adventurous", "main", "The wine's intense mineral depth bridges surprisingly well with Chile's beloved caldillo de congrio — Pablo Neruda's ode made wine-food reality.")
    PAIR(prod5a, "Smoked Patagonian lamb with merkén spice", "complement", "established", "main", "Mapuche-spiced smoked lamb from Chile's south finds a natural partner in the concentrated old-vine Carignan of the central valley.")

p5b = P("Gillmore Estate", "Chile", r5, description="One of Maule Valley's most committed quality-focused family estates, Daniel Gillmore produces benchmark Carmenere, Carignan and Semillon from old dry-farmed vines on granitic soils in the Loncomilla sub-valley, establishing himself as one of Chile's most interesting and authentic terroir-focused winemakers.")
prod5b, new5b = PROD("Gillmore Tabali de Cumpeo Carmenere Maule Valley DO", "wine_still", p5b, r5, "Chile",
    subcategory="Carmenere",
    description="A benchmark old-vine Maule Carmenere from Gillmore's family estate — showing the variety's distinctive deep violet colour, dark cherry, green pepper, graphite and iron mineral character from ancient granite soils, with the concentration and structure that establishes Carmenere as Chile's most distinctive indigenous red variety when produced from dry-farmed old vines.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Pastel de choclo Chilean corn pie with beef and olive", "complement", "classic", "main", "Chile's national dish of sweet corn crust over spiced beef and hard-boiled egg — Carmenere's pyrazine greenness and dark fruit bridge the dish's contrasting sweet and savoury elements perfectly.")
    PAIR(prod5b, "Grilled chorizo criollo with pebre salsa", "complement", "classic", "starter", "Chilean sausage with the fresh tomato-cilantro salsa of pebre — Carmenere's herbaceous green character links the vine-ripened spice with the fresh herb sauce.")
    PAIR(prod5b, "Braised Mapuche free-range chicken with merkén and corn", "complement", "established", "main", "Indigenous Mapuche-spiced chicken preparation with Chile's most distinctive red variety — terroir expressed through culinary and viticultural cultural heritage simultaneously.")
    PAIR(prod5b, "Empanada de pino with beef, olive, egg and raisins", "complement", "classic", "starter", "Chile's definitive baked empanada with its most characteristic red grape — the wine's dark fruit and herbaceous note complement the complex filling of spiced beef and sweet raisins.")

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
