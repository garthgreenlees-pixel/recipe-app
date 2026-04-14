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

# ── B128 ─────────────────────────────────────────────────────────────────────
# Targets: Rueda DO (Spain), Toro DO (Spain), Penedès DO (Spain),
#          Swartland (South Africa), Walker Bay (South Africa)

# 1. RUEDA DO — Spain
print("=== Rueda DO ===")
r1 = R("Rueda DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Rueda DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Castilian plateau appellation at 700-900m altitude on the Duero river west of Valladolid, dedicated almost entirely to Verdejo — Spain's most important aromatic white grape. The high altitude, sandy soils over chalk and extreme diurnal temperature variation preserve Verdejo's vibrant citrus, herb and bitter almond character. Also produces Sauvignon Blanc (introduced in the 1970s) and the traditional Rueda Pálido fortified style. Verdejo has become Spain's bestselling premium white.",
        key_producers="Belondrade y Lurton, Javier Sanz, José Pariente, Ossian, Naia",
        historical_context="Rueda was traditionally known for oxidative, sherry-like Palido wines until Marqués de Riscal arrived in the 1970s and introduced Sauvignon Blanc, transforming the region's image. The Verdejo revolution followed; the DO was granted in 1980. Ossian's centenarian ungrafted Verdejo vines opened the world's eyes to the variety's grandeur.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"very_good","rising"),(2022,"excellent","rising")]:
    VIN(r1, yr, qd, pt, f"Rueda {yr}: Castilian plateau; high altitude Verdejo with vibrant citrus and bitter almond character")

p1a = P("Belondrade y Lurton", "winery", r1, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The prestige Rueda estate; barrel-fermented Verdejo of extraordinary richness and complexity — proving the variety can age like Burgundy.",
        reputation_narrative="Didier Belondrade and Brigitte Lurton created Spain's reference Rueda with their barrel-fermented Verdejo; one of Spain's most sought-after white wines.",
        price_positioning="ultra_premium")
pr1a1, n = PROD("Belondrade y Lurton Verdejo", "wine_still", p1a, r1, "Spain",
                subcategory="Verdejo", price_tier="ultra_premium",
                description="Barrel-fermented Verdejo from sandy plateau soils; complex with citrus cream, fennel, white peach and a long mineral finish that improves for 5+ years.")
if n:
    PAIR(pr1a1, "Roasted langoustines with saffron aioli", "complement", "classic", "main", "Belondrade's barrel-weight and citrus cream perfectly frames langoustine with saffron")
    PAIR(pr1a1, "Cured salt cod (bacalao) with pil-pil sauce", "complement", "established", "main", "The white wine's weight and citrus precision complements pil-pil's garlic-oil")
    PAIR(pr1a1, "White asparagus with jamón ibérico", "complement", "classic", "main", "Rueda's classic pairing: barrel Verdejo and white asparagus with the Castilian cured ham")
    PAIR(pr1a1, "Aged Manchego (12 month) with honey", "complement", "established", "cheese", "Aged sheep's cheese and barrel-fermented Verdejo; the Castilla y León table tradition")

pr1a2, n = PROD("Belondrade y Lurton Quinta Apolonia", "wine_still", p1a, r1, "Spain",
                subcategory="Verdejo", price_tier="premium",
                description="Second label of Belondrade; un-oaked Verdejo with citrus, bitter almond and fresh herb — more immediate and versatile than the flagship.")
if n:
    PAIR(pr1a2, "Gambas al pil-pil (garlic prawns)", "complement", "classic", "main", "Verdejo's citrus-herb character and garlic prawns; a classic combination")
    PAIR(pr1a2, "Pimientos de Padrón (blistered green peppers)", "complement", "classic", "amuse", "The Galician green pepper tradition and fresh Verdejo make a natural pair")
    PAIR(pr1a2, "Ensalada de verduras asadas con queso", "complement", "established", "starter", "Herb-inflected Verdejo complements roasted vegetables with cheese salad")
    PAIR(pr1a2, "Grilled dorada (gilt-head bream) with lemon", "complement", "established", "main", "Fresh citrus-mineral Verdejo is the natural Spanish companion for grilled sea bream")

p1b = P("Ossian", "winery", r1, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Old-vine Verdejo pioneer; centenarian ungrafted vines in Nieva on sandy soils; Ossian single-vineyard is Spain's reference for old-vine Verdejo.",
        reputation_narrative="The Medina family's Ossian winery demonstrated that pre-phylloxera Verdejo vines can produce wine of extraordinary complexity and ageing potential.",
        price_positioning="ultra_premium")
pr1b1, n = PROD("Ossian Verdejo Rueda", "wine_still", p1b, r1, "Spain",
                subcategory="Verdejo", price_tier="ultra_premium",
                description="Centenarian ungrafted Verdejo; extraordinary depth with fig leaf, citrus, mineral and a structure reminiscent of great Burgundy white.")
if n:
    PAIR(pr1b1, "Steamed lobster with herb cream", "complement", "established", "main", "Old-vine Verdejo's depth and mineral match the luxury of herb-sauced lobster")
    PAIR(pr1b1, "Seared scallops with cauliflower cream and truffle", "complement", "established", "main", "Complex Ossian Verdejo handles scallop sweetness and truffle with remarkable grace")
    PAIR(pr1b1, "Cochinillo asado (Segovian roasted suckling pig)", "complement", "classic", "main", "The great pairing of Segovia: roasted suckling pig and Castilian Verdejo")
    PAIR(pr1b1, "Aged Zamorano sheep's cheese", "complement", "established", "cheese", "Old-vine Verdejo and the Castilian sheep's cheese; the regional tradition")

pr1b2, n = PROD("Ossian Quintaluna Rueda", "wine_still", p1b, r1, "Spain",
                subcategory="Verdejo", price_tier="mid_range",
                description="Entry Ossian from young vines; fresh Verdejo with peach, grapefruit and bitter almond — accessible and food-friendly.")
if n:
    PAIR(pr1b2, "Ceviche with citrus and herbs", "complement", "established", "starter", "Citrus-fresh Verdejo mirrors ceviche's acid-herb profile")
    PAIR(pr1b2, "Pollo rustido (Spanish roast chicken)", "complement", "established", "main", "Everyday Verdejo is a versatile companion for Spanish roast chicken")
    PAIR(pr1b2, "Ensalada de pepino y tomate (salad)", "complement", "established", "starter", "Refreshing Verdejo mirrors the freshness of Spanish summer salad")
    PAIR(pr1b2, "Paella de verduras (vegetable paella)", "complement", "established", "main", "Fresh Verdejo complements vegetable paella's saffron and herb character")

# 2. TORO DO — Spain
print("=== Toro DO ===")
r2 = R("Toro DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Toro DO",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Arid, wind-swept plateau west of Zamora on the Duero at 620-750m altitude, producing Spain's most powerful Tempranillo variant — Tinta de Toro — from old ungrafted vines on sandy soils. The phylloxera-resistant sandy terrain preserved pre-phylloxera vines across the region. Extreme continental climate produces wines of extraordinary concentration, high alcohol and grippy tannins but with old-vine freshness. Numanthia (formerly Eguren family) and Pintia (Vega Sicilia) validated the region internationally.",
        key_producers="Numanthia, Pintia (Vega Sicilia), Bodegas Fariña, Abadía de la Lastra, Bodegas Toro Albalá",
        historical_context="Toro wine was exported throughout the Spanish Empire and was served at the court of the Catholic monarchs. The modern era began when the Eguren family created Numanthia in 1998, producing wines that attracted global attention. Vega Sicilia's arrival with Pintia in 2001 confirmed Toro's world-class potential.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","stable"),(2021,"exceptional","rising"),(2022,"excellent","stable")]:
    VIN(r2, yr, qd, pt, f"Toro {yr}: extreme continental plateau; old ungrafted Tinta de Toro of extraordinary concentration")

p2a = P("Numanthia", "winery", r2, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The founding Toro quality estate; Numanthia and Termanthia from centenarian ungrafted vines on sand are the world references for Tinta de Toro.",
        reputation_narrative="Founded by the Eguren family in 1998; now owned by LVMH; Termanthia from 100+ year ungrafted vines is one of Spain's most collectible red wines.",
        price_positioning="ultra_premium")
pr2a1, n = PROD("Numanthia Termanthia Toro", "wine_still", p2a, r2, "Spain",
                subcategory="Tinta de Toro", price_tier="ultra_premium",
                description="The iconic Toro single-vineyard; centenarian ungrafted Tinta de Toro with extraordinary density, dark plum, graphite and structural power that ages 20+ years.")
if n:
    PAIR(pr2a1, "Slow-roasted Castilian suckling lamb (lechazo)", "complement", "classic", "main", "Castilian lechazo asado and Toro's most powerful red; a Spanish luxury pairing")
    PAIR(pr2a1, "Roast boar shoulder with black truffle", "complement", "established", "main", "Termanthia's immense structure demands wild game and truffle richness")
    PAIR(pr2a1, "Grilled Wagyu rib with bone marrow butter", "complement", "established", "main", "Old-vine Toro power and the richest beef cut; a statement pairing")
    PAIR(pr2a1, "Aged Manchego Curado (4 year)", "complement", "classic", "cheese", "Long-aged sheep's cheese and Spain's most powerful red; a Castilian tradition")

pr2a2, n = PROD("Numanthia Toro", "wine_still", p2a, r2, "Spain",
                subcategory="Tinta de Toro", price_tier="premium",
                description="Second label Numanthia; still deeply concentrated with dark fruit, iron mineral and the hallmark Toro structure — more approachable than Termanthia.")
if n:
    PAIR(pr2a2, "Roast leg of lamb (pierna de cordero asada)", "complement", "classic", "main", "Classic Castilian roasted lamb and Toro red; the great Duero river table tradition")
    PAIR(pr2a2, "Cocido madrileño (Madrid chickpea stew)", "complement", "established", "main", "The great Madrid stew finds its most natural Castilian red wine companion")
    PAIR(pr2a2, "Chorizo ibérico with bread and olive oil", "complement", "classic", "starter", "Concentrated Toro and Spanish cured chorizo; depth meets depth")
    PAIR(pr2a2, "Rabo de toro (braised oxtail)", "complement", "classic", "main", "Braised oxtail and powerful Toro red; the great Castilian combination")

p2b = P("Bodegas Fariña", "winery", r2, "Spain",
        production_philosophy="traditional",
        philosophy_description="Historic Toro family estate; Gran Colegiata and Colegiata are the benchmark entry-level Toro wines at excellent value.",
        reputation_narrative="Manuel Fariña is the patriarch of commercial Toro quality; his estate produces consistently good wines at prices far below the prestige estates.",
        price_positioning="mid_range")
pr2b1, n = PROD("Fariña Gran Colegiata Campus Toro", "wine_still", p2b, r2, "Spain",
                subcategory="Tinta de Toro", price_tier="mid_range",
                description="Gran Colegiata Campus; aged Toro with dark cherry, spice, vanilla and the region's hallmark powerful tannins — at an accessible price.")
if n:
    PAIR(pr2b1, "Caldereta de cordero (lamb stew with peppers)", "complement", "established", "main", "Toro's power matches the bold flavours of spiced Castilian lamb stew")
    PAIR(pr2b1, "Morcilla de Burgos (blood sausage with rice)", "complement", "classic", "main", "Spanish blood sausage and Toro red; the great Castilian pairing")
    PAIR(pr2b1, "Grilled ibérico pork ribs", "complement", "established", "main", "Ibérico pig richness and Toro power; Spain's most satisfying red wine-and-pork")
    PAIR(pr2b1, "Queso de Zamora (aged sheep's cheese)", "complement", "classic", "cheese", "Local Zamoran sheep's cheese and Toro red; the regional cheese tradition")

pr2b2, n = PROD("Fariña Colegiata Toro", "wine_still", p2b, r2, "Spain",
                subcategory="Tinta de Toro", price_tier="value",
                description="Entry Colegiata; approachable Tinta de Toro with dark fruit, spice and typical Toro structure at remarkable value.")
if n:
    PAIR(pr2b2, "Pizza with spicy salami and peppers", "complement", "established", "casual", "Everyday Toro red and a spicy pizza; an unexpected delight")
    PAIR(pr2b2, "Hamburger with aged cheese and caramelised onion", "complement", "established", "casual", "Bold Tinto de Toro cuts through the richness of a loaded burger")
    PAIR(pr2b2, "Pasta with mushroom and meat ragù", "complement", "established", "main", "Accessible Toro red suits hearty pasta with meat-and-mushroom sauce")
    PAIR(pr2b2, "Grilled chicken thighs with paprika marinade", "complement", "established", "main", "Everyday Toro and paprika chicken; accessible Castilian casual dining")

# 3. PENEDÈS DO — Spain
print("=== Penedès DO ===")
r3 = R("Penedès DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Penedès DO",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Catalan appellation south-west of Barcelona, historically the most innovative region in Spain. The heartland of Cava production (Xarel·lo, Macabeo, Parellada) but also producing still wines of increasing ambition. Altitude zones from coastal (near sea level) to high Penedès (900m), allowing diverse varieties from international classics to Catalan indigenes. Torres family is the defining influence, with global varieties planted alongside Garnacha Blanca and other local grapes.",
        key_producers="Torres, Jean León, Raventós i Blanc, Can Feixes, Albert i Noya",
        historical_context="Penedès was transformed by Miguel Torres who returned from his Dijon oenology studies in the 1960s and introduced cold fermentation, temperature control, international varieties and single-vineyard selection. His Mas La Plana Cabernet Sauvignon beat Château Latour at the 1979 Paris tasting, establishing Spanish wine's international credibility.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r3, yr, qd, pt, f"Penedès {yr}: Catalan plateau harvest; diverse climate zones from coastal to high altitude")

p3a = P("Torres", "winery", r3, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The defining Penedès family; Mas La Plana Cabernet and Milmanda Chardonnay are the prestige expressions; Mas Borràs Pinot Noir is a pioneer.",
        reputation_narrative="Miguel Torres transformed Spanish wine in the 1960s-70s; Mas La Plana's Paris tasting victory over Latour in 1979 was a landmark for Spanish wine credibility.",
        price_positioning="premium")
pr3a1, n = PROD("Torres Mas La Plana Cabernet Sauvignon", "wine_still", p3a, r3, "Spain",
                subcategory="Cabernet Sauvignon", price_tier="premium",
                description="Historic Penedès Cabernet from the 1979 Paris victor estate; structured, dark-fruited and elegant — Spain's most celebrated Cabernet Sauvignon.")
if n:
    PAIR(pr3a1, "Roast rack of lamb with herbs Provençales", "complement", "classic", "main", "Spain's benchmark Cabernet and herb-roasted rack of lamb; a timeless pairing")
    PAIR(pr3a1, "Duck breast with blackcurrant jus", "complement", "established", "main", "Mas La Plana Cabernet and duck with blackcurrant; the French-Catalan fusion")
    PAIR(pr3a1, "Braised veal cheeks with polenta", "complement", "established", "main", "Soft-structured Penedès Cabernet complements veal cheeks without overpowering")
    PAIR(pr3a1, "Aged Manchego or Parmigiano with walnuts", "complement", "established", "cheese", "Classic aged cheese and Cabernet Sauvignon; universally complementary")

pr3a2, n = PROD("Torres Viña Esmeralda Moscatel", "wine_still", p3a, r3, "Spain",
                subcategory="Moscatel-Gewürztraminer", price_tier="value",
                description="Spain's bestselling aromatic white; Moscatel and Gewürztraminer with floral, citrus and fresh herb notes — Torres' entry-level classic.")
if n:
    PAIR(pr3a2, "Pollo tandoori with coriander raita", "complement", "established", "main", "Aromatic Moscatel-Gewürztraminer complements spiced Indian chicken superbly")
    PAIR(pr3a2, "Grilled sea bass with lemon and dill", "complement", "established", "main", "Floral aromatic white lifts delicate sea bass with refreshing precision")
    PAIR(pr3a2, "Vietnamese spring rolls with nuoc cham", "complement", "established", "starter", "Aromatic white mirrors the fresh herb character of Vietnamese spring rolls")
    PAIR(pr3a2, "Peach and ginger tarte", "complement", "suggested", "dessert", "Floral Moscatel echoes peach and the gentle ginger note of the tart")

p3b = P("Raventós i Blanc", "winery", r3, "Spain",
        production_philosophy="biodynamic",
        philosophy_description="Historic Cava family that left the DO in 2012 to create Conca del Riu Anoia; biodynamic sparkling from indigenous Catalan varieties.",
        reputation_narrative="Josep Maria Raventós i Blanc left the Cava DO after refusing to use non-Catalan varieties; his L'Hereu and Manuel Raventós sparkling are Catalonia's finest.",
        price_positioning="premium")
pr3b1, n = PROD("Raventós i Blanc L'Hereu Blanc de Blancs", "wine_sparkling", p3b, r3, "Spain",
                subcategory="Macabeo-Xarel·lo-Parellada", price_tier="premium",
                description="Biodynamic traditional-method from indigenous Catalan varieties; fresh, yeasty and mineral with white peach and citrus zest.")
if n:
    PAIR(pr3b1, "Oysters Boqueria with lemon and shallot", "complement", "classic", "starter", "Catalan sparkling and fresh oysters from the Boqueria market; Barcelona's great pairing")
    PAIR(pr3b1, "Pa amb tomàquet with anchovies (Catalan toast)", "complement", "classic", "amuse", "The fundamental Catalan combination: sparkling wine with tomato-rubbed bread and anchovies")
    PAIR(pr3b1, "Escalivada (roasted pepper and aubergine)", "complement", "established", "starter", "Crisp indigenous sparkling cuts through the smoky sweetness of escalivada")
    PAIR(pr3b1, "Boquerones en vinagre (pickled anchovies)", "complement", "classic", "starter", "The acidity of traditional sparkling mirrors and tames the vinegar-pickled anchovy")

pr3b2, n = PROD("Raventós i Blanc De Nit Rosé Sparkling", "wine_sparkling", p3b, r3, "Spain",
                subcategory="Monastrell-Xarel·lo-Macabeo", price_tier="premium",
                description="Rosé sparkling with wild strawberry, cherry and floral notes; pale salmon colour from Monastrell skin contact; fresh and expressive.")
if n:
    PAIR(pr3b2, "Jamón ibérico de bellota with pan", "complement", "classic", "aperitif", "Spain's finest sparkling rosé with the finest cured ham; a Catalan celebration")
    PAIR(pr3b2, "Burrata with heirloom tomatoes and basil", "complement", "established", "starter", "Rosé sparkling's strawberry and acid mirror the summer tomato-burrata combination")
    PAIR(pr3b2, "Salmón ahumado con blinis", "complement", "established", "starter", "Sparkling rosé and smoked salmon blinis; the classic celebration combination")
    PAIR(pr3b2, "Summer berry Pavlova", "complement", "established", "dessert", "Wild strawberry rosé bubbles and meringue with berry compote; a joyful pairing")

# 4. SWARTLAND — South Africa
print("=== Swartland ===")
r4 = R("Swartland", "South Africa", "wine",
        designation_type="WO",
        designation_name="Swartland WO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The dramatic schist, granite and slate hills north of Cape Town, South Africa's most exciting natural wine region. Old bush-vine Chenin Blanc, Grenache, Syrah and Cinsault from dryland-farmed vineyards of 40-100+ years. The Swartland Revolution movement (Sadie, Badenhorst, Mullineux) transformed the region from bulk producer to international natural wine destination. Wines of extraordinary freshness, minerality and terroir expression that challenge European benchmarks.",
        key_producers="Eben Sadie, Badenhorst Family, Mullineux, Intellego, David & Nadia",
        historical_context="Swartland was dismissed as a hot, flat wheat and bulk wine region until Eben Sadie created Columella and Palladius in 1999-2000, demonstrating the potential of its old-vine Rhône varieties. The Swartland Revolution festival (2010) brought global attention; Chris Mullineux and Andrea Mullineux's Straw Wine created the region's most celebrated sweet wine.")
for yr, qd, pt in [(2018,"exceptional","rising"),(2019,"excellent","rising"),(2020,"very_good","rising"),(2021,"exceptional","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Swartland {yr}: schist and granite dryland harvest; old-vine Chenin and Syrah of extraordinary mineral intensity")

p4a = P("Sadie Family Wines", "winery", r4, "South Africa",
        production_philosophy="terroir_driven",
        philosophy_description="Eben Sadie's estate; Columella (Syrah-Mourvèdre) and Palladius (Chenin Blanc-led blend) are South Africa's most celebrated wines.",
        reputation_narrative="Eben Sadie created the Swartland revolution and is South Africa's most internationally acclaimed winemaker; Columella is among the world's great Syrah expressions.",
        price_positioning="ultra_premium")
pr4a1, n = PROD("Sadie Columella", "wine_still", p4a, r4, "South Africa",
                subcategory="Syrah-Mourvèdre", price_tier="ultra_premium",
                description="South Africa's iconic Rhône blend; old-vine Syrah and Mourvèdre from Paardeberg granite — floral, iron-mineral, olive and dark fruit of extraordinary elegance.")
if n:
    PAIR(pr4a1, "Braised lamb shoulder with North African spices", "complement", "classic", "main", "Columella's Rhône character suits the warm spice of a Cape-Malay lamb braise")
    PAIR(pr4a1, "Cape venison potjie with wild herbs", "complement", "established", "main", "South African game stew and the Cape's finest Rhône red; a prestige local pairing")
    PAIR(pr4a1, "Grilled springbok loin with rosemary jus", "complement", "established", "main", "Columella's elegant power frames springbok's delicate game perfectly")
    PAIR(pr4a1, "Aged Winelands Boerenkaas cheese", "complement", "established", "cheese", "Cape farm cheese finds an extraordinary companion in Columella's mineral depth")

pr4a2, n = PROD("Sadie Palladius Swartland White", "wine_still", p4a, r4, "South Africa",
                subcategory="Chenin Blanc-led blend", price_tier="ultra_premium",
                description="Multi-varietal white blend led by old-vine Chenin; complex with quince, ginger, mineral and beeswax — South Africa's most celebrated white wine.")
if n:
    PAIR(pr4a2, "Crayfish with Cape herb butter (braaibroodjie-style)", "complement", "classic", "main", "Palladius and Cape crayfish with herb butter; South Africa's definitive luxury pairing")
    PAIR(pr4a2, "Smoked snoek pâté on melba toast", "complement", "classic", "starter", "The Cape's iconic smoked fish pâté meets South Africa's greatest white wine")
    PAIR(pr4a2, "Bouillabaisse-style Cape fish stew", "complement", "established", "main", "Complex white blend suits a spiced Cape fish stew's depth beautifully")
    PAIR(pr4a2, "Baked whole cauliflower with miso and butter", "complement", "established", "main", "Beeswax-quince Palladius complements the umami richness of miso-baked cauliflower")

p4b = P("Mullineux Family Wines", "winery", r4, "South Africa",
        production_philosophy="natural",
        philosophy_description="Chris and Andrea Mullineux; schist-specific Syrahs and Chenin Blancs; Straw Wine is South Africa's most celebrated sweet wine.",
        reputation_narrative="Mullineux wines are the critical and commercial leaders of the new Swartland; Schist Syrah and Straw Wine are internationally the most award-winning South African expressions.",
        price_positioning="premium")
pr4b1, n = PROD("Mullineux Schist Syrah Swartland", "wine_still", p4b, r4, "South Africa",
                subcategory="Syrah", price_tier="premium",
                description="Schist-specific Syrah; iron, violet, white pepper and dark berry with textural elegance from the specific schist soil structure.")
if n:
    PAIR(pr4b1, "Lamb sosaties (Cape skewers with apricot)", "complement", "classic", "main", "Cape Malay sosaties and schist Syrah; a Swartland classic that showcases both")
    PAIR(pr4b1, "Grilled karoo lamb chops with dried fruit salsa", "complement", "classic", "main", "Karoo lamb and Swartland Syrah are South Africa's most natural wine-food expression")
    PAIR(pr4b1, "Duck breast with cherry and balsamic reduction", "complement", "established", "main", "Elegant Syrah's violet and cherry complements duck with cherry sauce")
    PAIR(pr4b1, "Biltong and droëwors charcuterie board", "complement", "classic", "starter", "The iconic South African cured meat tradition with the Cape's finest Syrah")

pr4b2, n = PROD("Mullineux Kloof Street White Swartland", "wine_still", p4b, r4, "South Africa",
                subcategory="Chenin Blanc", price_tier="mid_range",
                description="Entry Mullineux Chenin Blanc; fresh peach, citrus and mineral from old Swartland bush vines — an accessible introduction to Swartland whites.")
if n:
    PAIR(pr4b2, "Bobotie (Cape Malay spiced meat pie)", "complement", "classic", "main", "The defining South African dish and a fresh Swartland white; the Cape table classic")
    PAIR(pr4b2, "Grilled yellowtail with herb oil", "complement", "classic", "main", "Cape Yellowtail and Swartland Chenin; South Africa's most satisfying fish-white pairing")
    PAIR(pr4b2, "Waterblommetjiebredie (Cape water flower stew)", "complement", "classic", "main", "The most traditional Cape stew finds its natural Swartland white companion")
    PAIR(pr4b2, "Thai green curry with coconut rice", "complement", "established", "main", "Fresh mineral Chenin is a remarkable match for aromatic Thai curry")

# 5. WALKER BAY — South Africa
print("=== Walker Bay ===")
r5 = R("Walker Bay", "South Africa", "wine",
        designation_type="WO",
        designation_name="Walker Bay WO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Cool-climate maritime appellation on the southern Cape coast near Hermanus, with the Atlantic-facing vineyards producing South Africa's finest Pinot Noir and Chardonnay. The Hemel-en-Aarde Valley ('Heaven and Earth') is the heartland with three nested appellations (Hemel-en-Aarde Ridge, Valley, Upper Hemel-en-Aarde) on clay, shale and limestone. Hamilton Russell established the Walker Bay template; Crystallum and Storm are the new generation reference producers.",
        key_producers="Hamilton Russell, Crystallum, Storm, Newton Johnson, Creation",
        historical_context="Tim Hamilton Russell planted vineyards in Walker Bay in 1976 against strong advice; his persistence created South Africa's cool-climate wine revolution. The Hemel-en-Aarde became recognised as a world-class Pinot Noir and Chardonnay terroir. The 2021 Walker Bay Pinot Noir gained international attention when compared to top Burgundy at blind tastings.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"exceptional","rising"),(2021,"excellent","rising"),(2022,"very_good","rising")]:
    VIN(r5, yr, qd, pt, f"Walker Bay {yr}: cool maritime harvest; Atlantic-influenced Pinot Noir of remarkable elegance and mineral precision")

p5a = P("Hamilton Russell Vineyards", "winery", r5, "South Africa",
        production_philosophy="terroir_driven",
        philosophy_description="The founding Walker Bay estate; benchmark Pinot Noir and Chardonnay from clay-shale Hemel-en-Aarde Valley.",
        reputation_narrative="Anthony Hamilton Russell's estate set the Walker Bay benchmark in the 1970s; the Pinot Noir is consistently South Africa's most Burgundy-esque expression.",
        price_positioning="premium")
pr5a1, n = PROD("Hamilton Russell Pinot Noir Walker Bay", "wine_still", p5a, r5, "South Africa",
                subcategory="Pinot Noir", price_tier="premium",
                description="The benchmark Cape Pinot Noir; clay-shale Hemel-en-Aarde with red cherry, earth, dried herbs and a saline mineral character unique to the Cape.")
if n:
    PAIR(pr5a1, "Seared Cape salmon with lemon-caper butter", "complement", "classic", "main", "Walker Bay Pinot and Cape salmon; South Africa's answer to the Burgundy-salmon tradition")
    PAIR(pr5a1, "Grilled duck breast with pomegranate jus", "complement", "established", "main", "Elegant Cape Pinot's red fruit and earth complement duck and pomegranate perfectly")
    PAIR(pr5a1, "Ostrich fillet with mushroom and herb jus", "complement", "classic", "main", "Walker Bay Pinot Noir and ostrich; the great South African alternative-protein pairing")
    PAIR(pr5a1, "Mild aged goat's cheese with honey", "complement", "established", "cheese", "Cape Pinot Noir's delicacy mirrors mild aged goat's cheese and honey perfectly")

pr5a2, n = PROD("Hamilton Russell Chardonnay Walker Bay", "wine_still", p5a, r5, "South Africa",
                subcategory="Chardonnay", price_tier="premium",
                description="South Africa's most celebrated Chardonnay; clay-shale minerality with citrus, white peach and subtle oak — a Burgundy-rivalling expression.")
if n:
    PAIR(pr5a2, "Grilled snoek with apricot jam", "complement", "classic", "main", "The Cape's most iconic fish preparation meets its finest local Chardonnay")
    PAIR(pr5a2, "Butter-poached Cape crayfish (kreef)", "complement", "classic", "main", "Walker Bay Chardonnay and Cape crayfish; the coastal luxury of the Western Cape")
    PAIR(pr5a2, "Chicken and mushroom pot pie", "complement", "established", "main", "Rich textured Chardonnay and chicken pot pie; a comforting Cape winter pairing")
    PAIR(pr5a2, "White asparagus with lemon hollandaise", "complement", "established", "main", "Classic white asparagus and Chardonnay pairing, with a Walker Bay twist")

p5b = P("Crystallum Wines", "winery", r5, "South Africa",
        production_philosophy="natural",
        philosophy_description="Peter-Allan Finlayson's natural Pinot Noir and Chardonnay from multiple Walker Bay sites; Clay Shales and Mabalel are the flagships.",
        reputation_narrative="Crystallum is the new generation Walker Bay reference; Peter-Allan Finlayson (son of Hamilton Russell's winemaker) produces wines of extraordinary purity.",
        price_positioning="premium")
pr5b1, n = PROD("Crystallum Clay Shales Pinot Noir", "wine_still", p5b, r5, "South Africa",
                subcategory="Pinot Noir", price_tier="premium",
                description="Clay shale-specific Pinot Noir; perfumed with wild strawberry, rose petal, dried herb and a delicate saline mineral character.")
if n:
    PAIR(pr5b1, "Grilled Cape tuna steaks with herb oil", "complement", "established", "main", "Delicate Walker Bay Pinot and meaty tuna steak; an elegant south coast pairing")
    PAIR(pr5b1, "Wild mushroom risotto with parmesan", "complement", "established", "main", "Pinot Noir's earth and red fruit complement mushroom risotto's umami depth")
    PAIR(pr5b1, "Lamb chops with herb salsa verde", "complement", "established", "main", "Light Walker Bay Pinot and herb-dressed lamb; a fresh Cape spring pairing")
    PAIR(pr5b1, "Aged Camembert or Brie de Meaux", "complement", "established", "cheese", "Classic Pinot and soft-ripened cheese; universally complementary and delicious")

pr5b2, n = PROD("Crystallum Mabalel Chardonnay", "wine_still", p5b, r5, "South Africa",
                subcategory="Chardonnay", price_tier="premium",
                description="Mabalel Chardonnay from Upper Hemel-en-Aarde; textured and mineral with white pear, citrus and integrated oak — the cool-climate Cape at its finest.")
if n:
    PAIR(pr5b2, "Whole roasted chicken with tarragon butter", "complement", "classic", "main", "Textured Chardonnay and roast chicken; the eternal wine-food marriage")
    PAIR(pr5b2, "Linguine with clams and white wine", "complement", "established", "main", "Mineral Walker Bay Chardonnay and clam pasta; surprisingly resonant")
    PAIR(pr5b2, "Pan-fried halibut with beurre blanc", "complement", "classic", "main", "Textured Chardonnay and butter-sauced halibut; the great French-influenced Cape pairing")
    PAIR(pr5b2, "Truffle scrambled eggs on brioche", "complement", "established", "starter", "Complex Chardonnay handles the richness of truffle-scented eggs with mineral grace")

# Final counts
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

cur.close()
conn.close()
print("B128 complete.")
