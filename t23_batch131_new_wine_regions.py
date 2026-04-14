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

# ── B131 ──────────────────────────────────────────────────────────────────────
# Targets: Luján de Cuyo DOC (Argentina), Valle de Uco (Argentina),
#          Yarra Valley (Australia), Mornington Peninsula (Australia),
#          Eden Valley (Australia)

# 1. LUJÁN DE CUYO DOC — Mendoza, Argentina
print("=== Luján de Cuyo DOC ===")
r1 = R("Luján de Cuyo DOC", "Argentina", "wine",
        designation_type="DOC",
        designation_name="Luján de Cuyo DOC",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Argentina's first DOC (2006) and home to the country's most prestigious Malbec; the historic heartland of Mendoza's wine industry at 950-1100m altitude with alluvial soils, abundant sunshine and dramatic diurnal temperature variation. Luján's Malbec from old vines (pre-1940s) produces the richest, most structured expression of the variety. Districts Perdriel and Vistalba produce Mendoza's most sought-after wines.",
        key_producers="Catena Zapata, Achaval Ferrer, Clos de los Siete, Zuccardi",
        historical_context="Luján de Cuyo was established as Argentina's first DOC in 2006, recognizing the historic importance of the sub-region. The area was settled by European immigrants in the late 19th century; many old Malbec vineyards date to pre-1940. Nicolás Catena Zapata championed the region globally from the 1990s, commissioning research that proved Argentine Malbec could rival Bordeaux. The DOC requires minimum 12 months aging.")
for yr, qd, pt, sn in [
    (2018, "very_good", "stable", "Classic year; old vine Malbec shows deep colour and plush dark fruit; tannins well-resolved"),
    (2019, "excellent", "rising", "Excellent vintage; cool nights preserved freshness; Malbec shows violet and dark cherry intensity"),
    (2020, "very_good", "rising", "Good growing season; concentration in old vine Malbec; structured wines with aging potential"),
    (2021, "exceptional", "rising", "Exceptional vintage; perfect diurnal variation; old vine Luján Malbec at its most complex and elegant"),
    (2022, "excellent", "rising", "Ideal conditions; violet, plum and mineral character; wines of great elegance for Luján"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Catena Zapata", "winery", r1, "Argentina",
        production_philosophy="research_driven",
        philosophy_description="Argentina's most celebrated wine producer; Nicolás Catena Zapata's research into high-altitude viticulture transformed Argentine wine globally; Adrianna Vineyard at 1450m is the country's most sought-after wine.",
        reputation_narrative="The producer who put Argentine Malbec on the world stage; Catena Zapata's research-driven approach and Adrianna Vineyard have earned comparisons to Petrus and DRC from international critics.",
        price_positioning="ultra_premium")

pr1a1, n = PROD("Catena Zapata Adrianna Vineyard White Bones Chardonnay", "wine_still", p1a, r1, "Argentina",
    subcategory="Chardonnay single vineyard", price_tier="ultra_premium",
    description="Single-parcel Chardonnay from the legendary Adrianna Vineyard at 1450m; White Bones parcel on limestone; citrus cream, white peach, crushed limestone mineral; rivals Grand Cru Burgundy; one of the world's great whites.")
if n:
    PAIR(pr1a1, "Seared scallops with truffle and cauliflower cream", "complement", "classic", "starter", "Adrianna's limestone mineral and cream texture mirrors the cauliflower purée; truffle bridges wine's earthy depth")
    PAIR(pr1a1, "Grilled king crab with herb butter", "complement", "established", "main", "Luxury shellfish; wine's richness and mineral match the sweet crab; herb butter bridges the creamy texture")
    PAIR(pr1a1, "Aged Manchego with membrillo quince", "complement", "established", "cheese", "Aged sheep cheese; wine's mineral depth handles the fat; quince sweetness bridges the citrus notes")
    PAIR(pr1a1, "Pan-seared Dover sole with lemon beurre blanc", "complement", "classic", "fish_course", "Classic French technique; Adrianna's Burgundy-like depth matches; lemon echoes wine's citrus; beurre blanc bridges")

pr1a2, n = PROD("Catena Zapata Malbec Argentino", "wine_still", p1a, r1, "Argentina",
    subcategory="Malbec", price_tier="ultra_premium",
    description="Iconic Catena flagship Malbec blending old vine Luján parcels; deep violet, plum, dark cherry, chocolate, fresh violets; velvety tannins; the wine that defined modern Argentine Malbec.")
if n:
    PAIR(pr1a2, "Asado de tira (Argentine short ribs grilled over coals)", "complement", "classic", "main", "The definitive Argentine pairing; short ribs' fat tames Malbec's tannin; coal smoke echoes wine's dark fruit")
    PAIR(pr1a2, "Empanadas de carne mendocinas (Mendoza-style beef empanadas)", "complement", "classic", "starter", "Mendoza tradition; Malbec's plum fruit balances spiced beef; pastry provides the perfect canvas")
    PAIR(pr1a2, "Grilled bone-in rib-eye with chimichurri", "complement", "classic", "main", "Argentine steak culture; Malbec's tannin cuts the fat; chimichurri herbs echo wine's violet floral notes")
    PAIR(pr1a2, "Provoleta (grilled provolone) with oregano", "complement", "classic", "starter", "Classic Argentine appetizer; melted cheese richness tamed by Malbec's acidity; oregano bridges herb notes")

p1b = P("Achaval Ferrer", "winery", r1, "Argentina",
        production_philosophy="terroir_driven",
        philosophy_description="Single-vineyard Malbec specialist; Quimera and three single-parcel Malbec wines from Luján's historic Finca Altamira, Bella Vista, and Mirador show the sub-regional complexity.",
        reputation_narrative="The producer that demonstrated Luján's single-vineyard terroir; Achaval Ferrer's old-vine Malbec parcels showed the world that Argentine wine could express distinct sense of place.",
        price_positioning="ultra_premium")

pr1b1, n = PROD("Achaval Ferrer Quimera Malbec Mendoza", "wine_still", p1b, r1, "Argentina",
    subcategory="Malbec blend", price_tier="premium",
    description="Flagship blend from old vine Luján and Tupungato parcels; deep violet, blackberry, plum, chocolate, fresh violets; velvety texture; the most elegant of the Achaval Ferrer range.")
if n:
    PAIR(pr1b1, "Lamb a la parrilla with salsa criolla", "complement", "classic", "main", "Argentine grill classic; lamb and Malbec; salsa criolla's tomato and herb echo wine's fruit and violet notes")
    PAIR(pr1b1, "Morcilla (blood sausage) with roasted peppers", "complement", "established", "starter", "Argentine asado staple; Malbec's dark fruit handles the iron-rich sausage; pepper sweetness bridges")
    PAIR(pr1b1, "Braised lamb shoulder with Mendoza spices", "complement", "established", "main", "Slow-braised lamb; Malbec's elegance suits the gentle cooking method; Andean spices bridge")
    PAIR(pr1b1, "Cheese empanadas with honey", "complement", "established", "starter", "Cheese-filled pastry; Malbec's fruit balances; honey bridges wine's dark fruit sweetness")

pr1b2, n = PROD("Achaval Ferrer Finca Bella Vista Malbec", "wine_still", p1b, r1, "Argentina",
    subcategory="Malbec single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Malbec from 70+ year old vines in Perdriel district; extraordinary concentration with dark cherry, violets, chocolate, mineral; considered among Argentina's greatest wines.")
if n:
    PAIR(pr1b2, "Prime dry-aged rib-eye with bone marrow butter", "complement", "classic", "main", "Luxury beef with extreme richness; Bella Vista's concentration handles the marrow fat; dark fruit bridges")
    PAIR(pr1b2, "Mollejas (sweetbreads) grilled over coals", "complement", "established", "main", "Classic Argentine offal; sweetbreads' richness tamed by Malbec's structure; coal smoke mirrors wine's depth")
    PAIR(pr1b2, "Aged Manchego and candied walnuts", "complement", "established", "cheese", "Aged sheep cheese; wine's concentration handles the intensity; walnut echoes the dark fruit depth")
    PAIR(pr1b2, "Duck magret with wild berry reduction", "complement", "classic", "main", "Duck breast with dark fruit sauce; Malbec's berry and plum character mirrors the reduction; fat tamed by tannin")

# 2. VALLE DE UCO — Mendoza, Argentina
print("=== Valle de Uco ===")
r2 = R("Valle de Uco", "Argentina", "wine",
        designation_type="GI",
        designation_name="Valle de Uco",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Argentina's most exciting wine region at 1000-1500m altitude in the Uco Valley, south of Mendoza city; limestone soils, extreme diurnal temperature variation (20°C+ daily range), and intense Andean sunlight produce wines of extraordinary freshness, complexity, and elegance. The region produces Argentina's most cerebral Malbec and has pioneered Cabernet Franc and white varieties at altitude. Cheval Blanc invested here (Cheval des Andes); Catena's Adrianna Vineyard is at 1450m.",
        key_producers="Zuccardi Valle de Uco, Cheval des Andes, Achaval Ferrer, Clos de los Siete",
        historical_context="Valle de Uco was considered too cold and remote for viticulture until the 1990s when visionary producers discovered that altitude provided natural freshness and limestone soils added minerality absent in the main Mendoza valley. Zuccardi's investment in the region produced Argentina's first perfect score from Robert Parker (Zuccardi Valle de Uco Concreto 2016). The sub-regions of Tupungato, Tunuyán, and San Carlos each offer distinct expressions.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good vintage; altitude freshness preserved; Malbec and Cab Franc show elegant mineral character"),
    (2019, "excellent", "rising", "Excellent Valle de Uco; cool nights and extreme diurnal range; wines of remarkable freshness and precision"),
    (2020, "very_good", "rising", "Good growing season; Tupungato showed limestone mineral; elegant and structured wines"),
    (2021, "exceptional", "rising", "Exceptional; perfect diurnal conditions; altitude Malbec at its most mineral and complex; benchmark vintage"),
    (2022, "excellent", "rising", "Ideal harvest; cool nights and warm days; Malbec and Cabernet Franc both excel; mineral and fresh"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Zuccardi Valle de Uco", "winery", r2, "Argentina",
        production_philosophy="terroir_driven",
        philosophy_description="The producer that transformed Valle de Uco's reputation; José Alberto Zuccardi's obsessive research into limestone parcels produced Argentina's first perfect 100-point score; Concreto and Finca Piedra Infinita are references.",
        reputation_narrative="The producer who proved Valle de Uco's greatness; Zuccardi's 2016 Concreto received Argentina's first Parker 100 points and triggered massive investment in the region; the benchmark for altitude Mendoza.",
        price_positioning="ultra_premium")

pr2a1, n = PROD("Zuccardi Concreto Malbec Valle de Uco", "wine_still", p2a, r2, "Argentina",
    subcategory="Malbec single vineyard", price_tier="ultra_premium",
    description="The wine that changed Argentine wine history; 100 points from Parker (2016); limestone soils at 1200m; violet, blueberry, mineral precision, compressed tannins; transcends the Malbec category.")
if n:
    PAIR(pr2a1, "Wagyu beef strip loin with Andean herbs", "complement", "classic", "main", "Elite beef with Concreto's power and elegance; Andean herbs echo the altitude terroir; wagyu fat tames the tannin")
    PAIR(pr2a1, "Roasted Patagonian lamb rack with quinoa", "complement", "classic", "main", "Premium Argentine lamb; Malbec's elegance suits the delicate lamb; quinoa earthiness bridges the mineral")
    PAIR(pr2a1, "Charcoal-grilled pigeon with berry reduction", "complement", "established", "main", "Game bird with dark fruit; Concreto's violet and blueberry mirror the reduction; mineral precision lifts the dish")
    PAIR(pr2a1, "Aged Manchego with Andean truffle salt", "complement", "established", "cheese", "Aged sheep cheese enhanced with Andean minerals; Concreto's limestone mineral echoes; extraordinary match")

pr2a2, n = PROD("Zuccardi Emma Bonarda Valle de Uco", "wine_still", p2a, r2, "Argentina",
    subcategory="Bonarda", price_tier="mid_range",
    description="Old vine Bonarda — Argentina's most planted but underrated variety; from 60-year-old vines at altitude; bright cherry, violet, fresh herbs; silky tannins; shows the variety at its most elegant and food-friendly.")
if n:
    PAIR(pr2a2, "Locro (Argentine winter stew with corn, beans and pork)", "complement", "classic", "main", "Argentina's national stew; Bonarda's fresh acidity lifts the dense stew; cherry fruit balances the pork richness")
    PAIR(pr2a2, "Pizza de mozzarella with olives and oregano", "complement", "classic", "main", "Argentine pizza tradition; Bonarda's bright acidity mirrors tomato; fresh fruit balances mozzarella fat")
    PAIR(pr2a2, "Grilled chicken with chimichurri", "complement", "classic", "main", "Lighter Argentine grill; Bonarda's freshness suits poultry; chimichurri herbs echo wine's herbal character")
    PAIR(pr2a2, "Charcuterie with Mendoza olives", "complement", "established", "aperitif", "Argentine aperitivo tradition; Bonarda's freshness refreshes; acidity cuts fat; violet notes bridge the cured meats")

p2b = P("Cheval des Andes", "winery", r2, "Argentina",
        production_philosophy="terroir_driven",
        philosophy_description="Joint venture between Château Cheval Blanc (Saint-Émilion) and Terrazas de los Andes; Bordeaux winemaking applied to Valle de Uco terroir; one of Argentina's most prestigious wines.",
        reputation_narrative="The Bordeaux-Argentine collaboration that showed high altitude Mendoza could produce wines of Old World sophistication; Cheval des Andes is consistently one of Argentina's most sought-after and highest-scoring wines.",
        price_positioning="ultra_premium")

pr2b1, n = PROD("Cheval des Andes Grand Vin Mendoza", "wine_still", p2b, r2, "Argentina",
    subcategory="Malbec Cabernet Franc blend", price_tier="ultra_premium",
    description="The flagship wine; Malbec and Cabernet Franc from Valle de Uco with Bordelais winemaking; dark plum, tobacco, cedar, violet, graphite; extraordinary structure; consistently one of South America's greatest red wines.")
if n:
    PAIR(pr2b1, "Boeuf bourguignon with Mendoza Malbec", "complement", "classic", "main", "Classic Burgundian braise with Argentine twist; wine's Bordelais structure handles the rich stew; regional echo")
    PAIR(pr2b1, "Grilled rack of lamb with Dijon and herbs", "complement", "classic", "main", "French-Argentine hybrid; lamb and Cabernet Franc is a Loire classic; Mendoza altitude adds freshness")
    PAIR(pr2b1, "Truffle-studded duck breast with lentils", "complement", "established", "main", "Old World luxury; Cheval des Andes' Bordeaux DNA suits duck; truffle bridges the graphite mineral character")
    PAIR(pr2b1, "Aged Mimolette with walnut bread", "complement", "established", "cheese", "French aged cheese; wine's Bordeaux character finds its fromage partner; walnut echoes the cedar and tobacco")

pr2b2, n = PROD("Cheval des Andes Uco Mendoza", "wine_still", p2b, r2, "Argentina",
    subcategory="Malbec blend", price_tier="premium",
    description="Second wine from Cheval des Andes; more accessible than Grand Vin but same Bordeaux-influenced approach; violet, plum, cedar; structured and elegant introduction to the estate's style.")
if n:
    PAIR(pr2b2, "Grilled rib-eye with Béarnaise sauce", "complement", "established", "main", "Argentine beef with French sauce; wine's Bordeaux structure suits Béarnaise's tarragon richness")
    PAIR(pr2b2, "Lamb and eggplant tagine", "complement", "suggested", "main", "Moroccan preparation; Malbec's dark fruit handles the spice; eggplant's richness tamed by tannin; unexpected bridge")
    PAIR(pr2b2, "Mushroom and truffle risotto", "complement", "established", "main", "Earthy risotto; wine's graphite and cedar echo the truffle; Cabernet Franc's herbal notes bridge mushrooms")
    PAIR(pr2b2, "Aged Pecorino with dark berry compote", "complement", "established", "cheese", "Hard sheep cheese; wine's fruit complements; berry compote bridges the Malbec's dark fruit character")

# 3. YARRA VALLEY — Victoria, Australia
print("=== Yarra Valley ===")
r3 = R("Yarra Valley", "Australia", "wine",
        designation_type="GI",
        designation_name="Yarra Valley GI",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Victoria's premium cool-climate wine region 50km east of Melbourne; rolling green hills at 50-400m altitude; Chardonnay and Pinot Noir of world class standard; also Cabernet Sauvignon and sparkling. The Yarra River valley provides a cool microclimate unique in Australian wine; rainfall without irrigation; multiple sub-zones from warmer lower Yarra to cooler Upper Yarra. De Bortoli, Yering Station, Oakridge, and Giant Steps lead quality.",
        key_producers="De Bortoli, Yering Station, Oakridge, Giant Steps, Punt Road",
        historical_context="The Yarra Valley was Victoria's most important wine region in the 19th century before prohibition and phylloxera devastated the industry. Revival began in the 1970s when James and Cassandra Halliday (later Australia's most influential critic) planted Coldstream Hills. The region now hosts over 80 producers. Cool climate Pinot Noir from Upper Yarra is frequently compared to Burgundy; sparkling wine production is also significant.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool classic year; Pinot Noir and Chardonnay both excellent; natural acidity and fresh fruit character"),
    (2019, "very_good", "rising", "Challenging bushfire season impacted some vineyards; careful selection produced excellent wines from unaffected fruit"),
    (2020, "very_good", "rising", "Cool year; Pinot Noir shows red fruit precision; Chardonnay mineral and taut; wines for aging"),
    (2021, "exceptional", "rising", "Exceptional Yarra vintage; Pinot Noir of Burgundian complexity; Chardonnay rivals premier cru; benchmark year"),
    (2022, "excellent", "rising", "Cool and balanced; Upper Yarra Pinot of great elegance; Chardonnay shows mineral tension and length"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Oakridge Wines", "winery", r3, "Australia",
        production_philosophy="terroir_driven",
        philosophy_description="The Yarra Valley's leading terroir-focused producer; David Bicknell's single-vineyard Chardonnay and Pinot Noir from Guerin, 864, and Local Vineyard ranges define modern Yarra Valley precision.",
        reputation_narrative="Consistently Australia's most acclaimed Yarra Valley producer; Oakridge's site-specific wines have redrawn the map of Australian Chardonnay and Pinot Noir, regularly cited as among the country's finest.",
        price_positioning="ultra_premium")

pr3a1, n = PROD("Oakridge 864 Drive Block Chardonnay Yarra Valley", "wine_still", p3a, r3, "Australia",
    subcategory="Chardonnay single block", price_tier="ultra_premium",
    description="Benchmark single-block Chardonnay from 864 Drive; white peach, citrus cream, struck flint, chalk mineral; pristine natural acidity; considered one of Australia's greatest Chardonnays.")
if n:
    PAIR(pr3a1, "Steamed Sydney rock oysters with mignonette", "complement", "classic", "amuse", "Pure brine from Sydney Harbour; Chardonnay's flint and citrus echo the oyster; mignonette's acidity matches wine's brightness")
    PAIR(pr3a1, "Pan-seared barramundi with beurre blanc and capers", "complement", "classic", "fish_course", "Australia's great fish; beurre blanc's richness mirrors Chardonnay's cream; capers bridge with mineral notes")
    PAIR(pr3a1, "Grilled lobster with herb and garlic butter", "complement", "classic", "main", "Luxury Australian seafood; wine's weight matches lobster; herb butter bridges botanical notes in the Chardonnay")
    PAIR(pr3a1, "Aged Gruyère with sourdough bread", "complement", "established", "cheese", "Nutty aged cheese; Chardonnay's mineral and citrus handles the fat; nutty character echoes wine's complexity")

pr3a2, n = PROD("Oakridge Local Vineyard Series Pinot Noir Yarra Valley", "wine_still", p3a, r3, "Australia",
    subcategory="Pinot Noir", price_tier="premium",
    description="Single-vineyard Upper Yarra Pinot Noir; red cherry, raspberry, spice, forest floor; silky texture; Burgundian precision with Australian freshness; one of Yarra's benchmark Pinots.")
if n:
    PAIR(pr3a2, "Roast duck with cherry sauce and turnip purée", "complement", "classic", "main", "Classic Pinot pairing; duck fat handled by the wine's silky tannin; cherry sauce mirrors wine's red fruit")
    PAIR(pr3a2, "Slow-roasted lamb shoulder with rosemary and garlic", "complement", "established", "main", "Yarra Pinot's silky structure suits slow-cooked lamb; rosemary echoes wine's herbal forest floor notes")
    PAIR(pr3a2, "Grilled quail with mushroom and thyme sauce", "complement", "classic", "main", "Delicate game bird; Pinot's finesse matches quail; mushroom and thyme bridge the forest floor character")
    PAIR(pr3a2, "Aged Comté with cherry compote", "complement", "established", "cheese", "Nutty French cheese with Yarra Pinot; cherry compote mirrors wine's red fruit; nutty echoes Burgundian style")

p3b = P("Giant Steps", "winery", r3, "Australia",
        production_philosophy="minimal_intervention",
        philosophy_description="Single-vineyard Yarra specialist; Phil Sexton's Chardonnay and Pinot Noir from Tarraford, Wombat Creek, Sexton, and Harry's Monster vineyards define the region's diversity.",
        reputation_narrative="One of Yarra's most acclaimed boutique producers; Giant Steps' single-vineyard approach has shown the depth of terroir expression possible in Victoria's coolest wine region.",
        price_positioning="premium")

pr3b1, n = PROD("Giant Steps Tarraford Vineyard Chardonnay Yarra Valley", "wine_still", p3b, r3, "Australia",
    subcategory="Chardonnay single vineyard", price_tier="premium",
    description="Single-vineyard Chardonnay from Tarraford; citrus cream, white nectarine, struck match, mineral; natural acidity; whole-bunch fermented; excellent Yarra Valley expression.")
if n:
    PAIR(pr3b1, "Roasted chicken with tarragon cream sauce", "complement", "classic", "main", "Classic white wine and chicken; Chardonnay's cream mirrors sauce; tarragon's anise echoes wine's spice")
    PAIR(pr3b1, "Kingfish sashimi with yuzu and daikon", "complement", "established", "starter", "Delicate raw fish; Chardonnay's mineral freshness complements yuzu citrus; minimal intervention suits the purity")
    PAIR(pr3b1, "Scrambled eggs with smoked salmon and crème fraîche", "complement", "classic", "starter", "Brunch luxury; Chardonnay's cream mirrors crème fraîche; mineral notes echo smoked salmon")
    PAIR(pr3b1, "Aged Manchego with honey and almonds", "complement", "established", "cheese", "Aged sheep cheese; Chardonnay's acidity cuts fat; honey bridges wine's stone fruit; almonds echo mineral")

pr3b2, n = PROD("Giant Steps Sexton Vineyard Pinot Noir Yarra Valley", "wine_still", p3b, r3, "Australia",
    subcategory="Pinot Noir single vineyard", price_tier="premium",
    description="Upper Yarra Pinot from Sexton Vineyard; bright red cherry, raspberry, spice, forest floor, fine tannins; pristine cool-climate freshness; Burgundian in style.")
if n:
    PAIR(pr3b2, "Charcuterie board with duck rillettes", "complement", "classic", "starter", "Pinot's acidity cuts through duck fat rillettes; red fruit notes balance; elegant aperitif pairing")
    PAIR(pr3b2, "Salmon en croûte with dill cream", "complement", "established", "main", "Rich pastry-wrapped salmon; Pinot's acidity cuts; dill echoes wine's herbal notes; Scandinavian-inspired")
    PAIR(pr3b2, "Mushroom and brie tart", "complement", "established", "main", "Earthy mushroom with creamy brie; Pinot's forest floor echoes mushroom; brie fat balanced by acidity")
    PAIR(pr3b2, "Grilled beef tenderloin with Pinot reduction", "complement", "established", "main", "Delicate beef; Yarra Pinot's structure handles the tenderness; reduction mirrors the wine's character")

# 4. MORNINGTON PENINSULA — Victoria, Australia
print("=== Mornington Peninsula ===")
r4 = R("Mornington Peninsula", "Australia", "wine",
        designation_type="GI",
        designation_name="Mornington Peninsula GI",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Victoria's ultra-cool wine region on the peninsula between Port Phillip Bay and Bass Strait; 110km south of Melbourne at 10-200m altitude; ocean influence creates one of Australia's coldest and wettest wine climates. Pinot Noir and Chardonnay of extraordinary elegance; also small quantities of Pinot Gris and Shiraz. Moorooduc, Red Hill, and Main Ridge are the key sub-zones. Stonier, Paringa Estate, and Ten Minutes By Tractor lead quality.",
        key_producers="Stonier, Paringa Estate, Ten Minutes By Tractor, Scorpo, Moorooduc Estate",
        historical_context="The Mornington Peninsula was first planted commercially in 1970s despite early skepticism about the cold maritime climate. The cool conditions proved ideal for Pinot Noir and Chardonnay. Ten Minutes By Tractor introduced sophisticated marketing; Paringa Estate became the benchmark for the region with James Halliday awarding it 5 red stars consistently. The region now hosts 50+ producers within easy reach of Melbourne.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Cool maritime year; Pinot Noir shows elegant red fruit; Chardonnay mineral and precise; both excellent"),
    (2019, "excellent", "rising", "Ideal vintage; ocean influence preserved freshness; Pinot Noir of Chambolle-like elegance; rare quality"),
    (2020, "very_good", "rising", "Good year; cool conditions; Pinot shows precision; Chardonnay mineral and taut with aging potential"),
    (2021, "exceptional", "rising", "Exceptional; cool and balanced; Mornington Pinot at its most Burgundian; Chardonnay rivals premier cru"),
    (2022, "excellent", "rising", "Excellent maritime conditions; cool ocean winds preserved natural acidity; wines of great finesse"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Paringa Estate", "winery", r4, "Australia",
        production_philosophy="terroir_driven",
        philosophy_description="The benchmark Mornington Peninsula producer; Lindsay McCall's Pinot Noir and Chardonnay from estate Red Hill vineyards consistently earn Australia's highest scores; Peninsula Vineyard is the reference.",
        reputation_narrative="Mornington's most decorated producer; Paringa Estate's Peninsula Vineyard Pinot Noir has earned 99+ points from Halliday repeatedly and is considered a benchmark for cool-climate Australian Pinot Noir.",
        price_positioning="ultra_premium")

pr4a1, n = PROD("Paringa Estate Peninsula Vineyard Pinot Noir", "wine_still", p4a, r4, "Australia",
    subcategory="Pinot Noir single vineyard", price_tier="ultra_premium",
    description="The reference Mornington Pinot Noir; from estate Red Hill vineyards; dark cherry, spice, forest floor, silky tannins; Burgundian complexity with Australian freshness; consistently one of Australia's greatest Pinots.")
if n:
    PAIR(pr4a1, "Roast duck breast with cherry jus and beetroot", "complement", "classic", "main", "Pinot's ultimate pairing; cherry jus mirrors wine's red fruit; beetroot earthiness echoes forest floor")
    PAIR(pr4a1, "Slow-cooked lamb shoulder with rosemary and olives", "complement", "established", "main", "Gentle lamb preparation; Pinot's elegance suits; rosemary and olive echo the wine's herbal and savory depth")
    PAIR(pr4a1, "Grilled salmon with lentils and herb oil", "complement", "established", "fish_course", "Salmon's fat handled by Pinot's acidity; lentil earthiness bridges forest floor; herb oil echoes botanical notes")
    PAIR(pr4a1, "Aged Époisses with crusty bread", "complement", "adventurous", "cheese", "Strong washed-rind; Pinot's elegance and acidity handles the pungency; Burgundian tradition transplanted to Australia")

pr4a2, n = PROD("Paringa Estate Chardonnay Mornington Peninsula", "wine_still", p4a, r4, "Australia",
    subcategory="Chardonnay", price_tier="premium",
    description="Estate Chardonnay from cool Red Hill vineyards; white peach, citrus, chalk mineral, subtle oak; excellent natural acidity; one of Mornington's finest; ages beautifully for 5-8 years.")
if n:
    PAIR(pr4a2, "Seared scallops with parsnip purée and crispy capers", "complement", "classic", "starter", "Mornington classic; Chardonnay's mineral freshness frames scallop sweetness; capers bridge with acidity")
    PAIR(pr4a2, "Grilled flathead with brown butter and lemon", "complement", "classic", "fish_course", "Melbourne's favourite local fish; Chardonnay's weight and citrus suit the delicate flathead perfectly")
    PAIR(pr4a2, "Chicken liver pâté with brioche and cornichons", "complement", "established", "starter", "Rich liver pâté; Chardonnay's acidity and mineral cut; cornichon echoes wine's acidity; classic bistro match")
    PAIR(pr4a2, "Aged Gruyère fondue with crusty bread", "complement", "established", "main", "Swiss tradition; Chardonnay's acidity cuts the fat; mineral notes echo the cheese's alpine character")

p4b = P("Ten Minutes By Tractor", "winery", r4, "Australia",
        production_philosophy="terroir_driven",
        philosophy_description="The Mornington Peninsula producer that introduced single-vineyard terroir thinking; Main, Judd, and McCutcheon Pinot Noir vineyards show Mornington's diversity.",
        reputation_narrative="The producer that put Mornington on the global fine wine map; Ten Minutes By Tractor's single-vineyard approach and wine tourism destination have made the Peninsula a must-visit for wine lovers.",
        price_positioning="premium")

pr4b1, n = PROD("Ten Minutes By Tractor McCutcheon Pinot Noir", "wine_still", p4b, r4, "Australia",
    subcategory="Pinot Noir single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Pinot from the cooler McCutcheon block; delicate red cherry, rose petal, spice, earthy depth; the most elegant and Chambolle-like of the estate's wines.")
if n:
    PAIR(pr4b1, "Roasted quail with mushroom risotto and truffle", "complement", "classic", "main", "Elegant game bird; McCutcheon's Chambolle-like grace matches quail; truffle echoes earthy depth in the Pinot")
    PAIR(pr4b1, "Grilled Atlantic salmon with sorrel sauce", "complement", "established", "fish_course", "Fatty salmon with sour sauce; Pinot's acidity cuts through; sorrel's acidity mirrors wine's fresh character")
    PAIR(pr4b1, "Pork belly with apple and pickled ginger", "complement", "established", "main", "Rich pork; Pinot's acidity cuts fat; apple's sweetness bridges red fruit; ginger adds a spice note")
    PAIR(pr4b1, "Comté with fig preserve", "complement", "established", "cheese", "Nutty French cheese in Mornington context; Pinot's fruit and acidity balance; fig bridges wine's red fruit")

pr4b2, n = PROD("Ten Minutes By Tractor Judd Chardonnay Mornington", "wine_still", p4b, r4, "Australia",
    subcategory="Chardonnay single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Chardonnay from the Judd block; citrus, white peach, struck flint, chalk mineral; very fine and precise; consistently one of Mornington's greatest Chardonnays.")
if n:
    PAIR(pr4b2, "Pan-fried john dory with beurre blanc and sea vegetables", "complement", "classic", "fish_course", "Delicate white fish; Chardonnay's precision matches john dory's delicacy; sea vegetables echo maritime mineral")
    PAIR(pr4b2, "Lobster thermidor with gruyère", "complement", "classic", "main", "Classic luxury pairing; Chardonnay's weight and mineral handles the cheese-rich lobster; citrus lifts the dish")
    PAIR(pr4b2, "Grilled kingfish with miso butter and daikon", "complement", "established", "fish_course", "Australian kingfish with Japanese influences; Chardonnay's mineral precision suits the clean flavours")
    PAIR(pr4b2, "Triple cream brie with honeycomb", "complement", "established", "cheese", "Rich creamy cheese; Chardonnay's acidity cuts through; honeycomb bridges wine's stone fruit character")

# 5. EDEN VALLEY — South Australia, Australia
print("=== Eden Valley ===")
r5 = R("Eden Valley", "Australia", "wine",
        designation_type="GI",
        designation_name="Eden Valley GI",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="South Australia's high-altitude cool wine region in the Barossa Ranges at 400-600m altitude; produces some of the world's greatest Riesling alongside elegant Shiraz and Chardonnay. The altitude provides freshness unavailable in the warmer Barossa Valley floor. Henschke's Hill of Grace Shiraz (from 150-year-old vines) is one of Australia's and the world's greatest wines. Two sub-zones: Eden Valley itself and the cooler High Eden.",
        key_producers="Henschke, Pewsey Vale, Eden Hall, Irvine",
        historical_context="Eden Valley was planted by German settlers in the 1840s who also brought Riesling to Clare Valley. The Henschke family has farmed the region since 1868; their Hill of Grace vineyard has vines from the 1860s. Australian Riesling from Eden Valley and Clare are the country's greatest; the variety ages magnificently. The Henschke Hill of Grace (often $500+) is one of the world's mythical wines.")
for yr, qd, pt, sn in [
    (2018, "very_good", "stable", "Good vintage; Eden Valley Riesling shows lime and mineral; Shiraz elegant at altitude; balanced wines"),
    (2019, "excellent", "rising", "Excellent; altitude freshness preserved; Riesling shows pristine lime and slate; Hill of Grace shows power"),
    (2020, "very_good", "rising", "Good year; some bushfire impact managed well; Riesling and Shiraz both excellent where unaffected"),
    (2021, "exceptional", "rising", "Exceptional Eden Valley; Riesling shows lime sherbet precision; Hill of Grace Shiraz magnificent; landmark year"),
    (2022, "excellent", "rising", "Excellent; cool conditions preserve natural acidity; Riesling mineral and taut; Shiraz shows elegance"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Henschke", "winery", r5, "Australia",
        production_philosophy="traditional",
        philosophy_description="Australia's most revered family wine estate; 5th generation Stephen and Prue Henschke farm biodynamically; Hill of Grace from 150-year-old Shiraz vines is a national treasure.",
        reputation_narrative="The producer of Australia's most mythical wine; Henschke's Hill of Grace from 160-year-old Eden Valley vines is one of the world's great wines, compared to Penfolds Grange and Petrus for iconic status.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("Henschke Hill of Grace Eden Valley Shiraz", "wine_still", p5a, r5, "Australia",
    subcategory="Shiraz single vineyard", price_tier="ultra_premium",
    description="One of Australia's and the world's greatest wines; from 160-year-old vines planted in the 1860s; dark chocolate, blackberry, meat, ironstone mineral; extraordinary concentration; needs 20+ years; mythical status.")
if n:
    PAIR(pr5a1, "Slow-roasted leg of lamb with Eden Valley herbs", "complement", "classic", "main", "Australia's finest Shiraz with its classic pairing; lamb fat tames Hill of Grace's immense structure; local herbs bridge")
    PAIR(pr5a1, "Grilled bone-in rib-eye with mushroom and bone marrow butter", "complement", "classic", "main", "Premium beef with luxury enrichment; Hill of Grace's concentration handles the marrow; mushroom echoes the ironstone")
    PAIR(pr5a1, "Aged Barossa Valley Cheddar with quince paste", "complement", "established", "cheese", "Local aged cheese; Hill of Grace's power meets its match; quince bridges the dark fruit character")
    PAIR(pr5a1, "Wild boar ragù with handmade pasta", "complement", "established", "main", "Game weight matches Hill of Grace; pasta richness tamed by the tannin; chocolate notes bridge the dark meat")

pr5a2, n = PROD("Henschke Julius Eden Valley Riesling", "wine_still", p5a, r5, "Australia",
    subcategory="Riesling", price_tier="premium",
    description="Named for Julius Henschke; benchmark Eden Valley Riesling; lime blossom, slate mineral, citrus; crisp acidity; extraordinary aging potential; develops into complex petrol and toast with 10+ years.")
if n:
    PAIR(pr5a2, "Barramundi ceviche with lime and chilli", "complement", "classic", "starter", "Citrus-cured Australian fish; Julius's lime and mineral mirror the ceviche acidity; chilli heat tamed by Riesling")
    PAIR(pr5a2, "Thai green curry with jasmine rice", "complement", "classic", "main", "Classic Riesling pairing; residual sweetness and acidity handle the spice; lime in wine echoes lemongrass")
    PAIR(pr5a2, "Smoked trout with horseradish cream", "complement", "classic", "starter", "River fish with pungent cream; Riesling's lime and mineral cut the smoke; acidity balances the horseradish")
    PAIR(pr5a2, "Aged Gruyère with toasted caraway", "complement", "established", "cheese", "Alpine-style cheese with spice; Riesling's mineral and acidity cut the fat; caraway echoes wine's herbal notes")

p5b = P("Pewsey Vale", "winery", r5, "Australia",
        production_philosophy="terroir_driven",
        philosophy_description="Yalumba's High Eden property at 550m altitude; produces some of Australia's finest Riesling; The Contours Museum Reserve is the flagship showing Riesling's extraordinary aging potential.",
        reputation_narrative="The benchmark for High Eden Riesling; Pewsey Vale's The Contours demonstrates that Australian Riesling can age as long and as gracefully as German or Alsatian Riesling.",
        price_positioning="premium")

pr5b1, n = PROD("Pewsey Vale The Contours Museum Reserve Eden Valley Riesling", "wine_still", p5b, r5, "Australia",
    subcategory="Riesling aged release", price_tier="ultra_premium",
    description="Museum release Riesling aged minimum 5 years before release; toast, petrol, citrus, slate; complex secondary development; shows what Australian Riesling becomes with age; one of the country's most impressive white wines.")
if n:
    PAIR(pr5b1, "Peking duck with pancakes, cucumber and hoisin", "complement", "established", "main", "Aged Riesling's petrol and toast echo duck's complexity; hoisin sweetness balanced by acidity; classic match")
    PAIR(pr5b1, "Grilled Murray cod with native herbs", "complement", "classic", "fish_course", "Freshwater Australian fish with native herbs; Contours' complexity suits the earthy cod; mineral echoes the river")
    PAIR(pr5b1, "Prawn bisque with crème fraîche and caviar", "complement", "classic", "starter", "Rich bisque with luxury garnish; aged Riesling's texture and acidity handle the richness; petrol notes add complexity")
    PAIR(pr5b1, "Aged Époisse with caraway rye bread", "complement", "adventurous", "cheese", "Powerful washed-rind; aged Riesling's petrol and acidity can handle it; Alsatian-style pairing translocated")

pr5b2, n = PROD("Pewsey Vale Individual Vineyard Riesling Eden Valley", "wine_still", p5b, r5, "Australia",
    subcategory="Riesling", price_tier="mid_range",
    description="Estate High Eden Riesling; lime, citrus blossom, slate, crisp acidity; fresh and vibrant expression of High Eden terroir; excellent value; ages into petrol and toast complexity over 5-10 years.")
if n:
    PAIR(pr5b2, "Grilled king prawns with lime and chilli butter", "complement", "classic", "starter", "Australian seafood; Riesling's lime mirrors the lime butter; chilli heat tamed by natural sweetness")
    PAIR(pr5b2, "Chicken laksa with coconut milk", "complement", "established", "main", "Southeast Asian noodle soup; Riesling cuts through the coconut richness; lime notes echo lemongrass")
    PAIR(pr5b2, "Lemongrass-marinated fish tacos", "complement", "established", "main", "Aromatic fish preparation; Eden Valley Riesling's citrus echoes lemongrass; mineral freshness complements")
    PAIR(pr5b2, "Fresh goat cheese with lemon zest and herbs", "complement", "classic", "starter", "Tangy fresh cheese; Riesling's acidity and citrus complement perfectly; herbs echo wine's botanical notes")

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
print("B131 complete.")
conn.close()
