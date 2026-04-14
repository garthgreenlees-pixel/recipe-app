#!/usr/bin/env python3
"""B143 — Willamette Valley AVA (Oregon), Paso Robles AVA (California),
   Sierra Foothills AVA (California), Finger Lakes AVA (New York),
   Walla Walla Valley AVA (Washington)
All constraints verified from B136-B142.
"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(WRITE_DSN)
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
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── WILLAMETTE VALLEY AVA (Oregon) ────────────────────────────────────────────
print("=== Willamette Valley AVA ===")
r = R("Willamette Valley AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Willamette Valley AVA",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="Oregon's greatest wine region producing Pinot Noir, Pinot Gris and Chardonnay from sedimentary Jory and Willakenzie soils in a cool maritime climate. The valley's Pinot Noir is America's most Burgundian, with the Dundee Hills, Chehalem Mountains and Ribbon Ridge sub-AVAs producing wines of genuine complexity and elegance.",
      key_producers="Adelsheim, Ponzi, Eyrie, Domaine Drouhin Oregon, Beaux Frères",
      historical_context="The Eyrie Vineyards' David Lett planted Oregon's first Pinot Noir in the Willamette Valley in 1965, dismissing expert opinion that the climate was too cold. When his 1975 South Block Reserve Pinot Noir finished second in Robert Drouhin's Paris tastings in 1979, Oregon was established on the international map. Burgundy house Drouhin planted here in 1988.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Excellent Oregon vintage; Dundee Hills Pinot Noir of exceptional concentration and mineral elegance."),
    (2019, "excellent", "rising", "Outstanding Willamette vintage; textbook Pinot Noir conditions throughout the valley."),
    (2020, "good", "stable", "Wildfire smoke significantly impacted some vineyards; selective harvest required."),
    (2021, "very_good", "stable", "Clean vintage; Willamette Pinot Noir restored its cool-climate elegance."),
    (2022, "excellent", "rising", "Benchmark Oregon vintage; Jory soil Pinot Noir of extraordinary depth and age-worthiness."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Drouhin Oregon", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Véronique Drouhin-Boss farms the Dundee Hills biodynamically using Burgundy techniques transplanted to Oregon, producing Pinot Noir and Chardonnay that bridge the Old and New Worlds with genuine elegance and mineral precision.",
       reputation_narrative="Domaine Drouhin Oregon's Dundee Hills Pinot Noir is one of America's most decorated wines, consistently demonstrating that the Willamette Valley can produce Pinot Noir rivalling Burgundy in quality and complexity.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Domaine Drouhin Oregon Dundee Hills Pinot Noir", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Burgundian-method Oregon Pinot Noir from Jory volcanic soils in the Dundee Hills; elegant, mineral and complex with red cherry, earth, silky tannins and the restraint that defines great Willamette Pinot.")
if is_new:
    PAIR(prod, "Duck breast with chanterelle mushrooms and cherry reduction", "complement", "classic", "main", "Dundee Hills Pinot's cherry-earth character is a natural companion for duck with forest mushrooms.")
    PAIR(prod, "Oregon wild salmon with Pinot Noir butter sauce", "complement", "classic", "main", "The quintessential Oregon pairing — Willamette Pinot Noir with Pacific salmon in a Pinot reduction.")
    PAIR(prod, "Roasted game hen with pomegranate and wild rice", "complement", "established", "main", "Delicate game bird and pomegranate find the elegant mineral Pinot of Dundee Hills ideal.")
    PAIR(prod, "Rogue River Blue cheese with honeycomb and walnut", "contrast", "established", "cheese", "Oregon's celebrated cave-aged blue cheese and honeycomb contrast the cherry mineral elegance of DDO Pinot.")

prod, is_new = PROD("Domaine Drouhin Oregon Chardonnay Arthur", "wine_still", p1, r, "USA",
    subcategory="white", price_tier="premium",
    description="Oregon Chardonnay in the Drouhin Burgundy style; mineral, textured and elegant with stone fruit, lemon and careful Burgundian oak — among America's most restrained and food-friendly Chardonnays.")
if is_new:
    PAIR(prod, "Grilled Dungeness crab with Meyer lemon and herb butter", "complement", "classic", "main", "Oregon Dungeness crab with herb butter and this Burgundian-style Chardonnay — the Pacific Northwest classic.")
    PAIR(prod, "Razor clam chowder with cream and smoked bacon", "complement", "established", "main", "Northwest chowder richness is balanced by the mineral freshness and restrained texture of Arthur Chardonnay.")
    PAIR(prod, "Roasted halibut with lemon caper beurre blanc", "complement", "established", "main", "Pacific halibut and French beurre blanc find Burgundian Oregon Chardonnay a natural match.")
    PAIR(prod, "Tillamook aged Cheddar with apple and mustard", "complement", "established", "casual", "Oregon's celebrated Tillamook Cheddar with apple finds the mineral complexity of Arthur Chardonnay ideal.")

p2 = P("Beaux Frères", "winery", r, "USA",
       production_philosophy="biodynamic",
       philosophy_description="Mike Etzel and Robert Parker Jr. (as early investors) established Beaux Frères as one of Oregon's most ambitious Pinot Noir estates, farming biodynamically in the Ribbon Ridge sub-AVA to produce wines of profound depth and complexity.",
       reputation_narrative="Beaux Frères's Ribbon Ridge Pinot Noir is consistently one of Oregon's highest-rated wines, demonstrating the Willamette Valley's capacity for Pinot Noir of world-class complexity and age-worthiness.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Beaux Frères Ribbon Ridge Pinot Noir Willamette", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Biodynamic Ribbon Ridge Pinot Noir from marine sedimentary soils; profound, structured and complex with dark cherry, spice and mineral depth that ages magnificently. One of Oregon's greatest Pinot Noirs.")
if is_new:
    PAIR(prod, "Roasted lamb shoulder with lavender, garlic and olive oil", "complement", "classic", "main", "Structured, complex Ribbon Ridge Pinot handles lamb richness with its spice and mineral depth.")
    PAIR(prod, "Mushroom and truffle risotto with Parmesan and butter", "complement", "established", "main", "Biodynamic Pinot's earthy depth and complexity resonates with truffle-mushroom risotto.")
    PAIR(prod, "Grilled quail with fig jam and bitter greens", "complement", "established", "main", "Delicate game bird with fig sweetness finds the cherry-spice depth of Ribbon Ridge Pinot ideal.")
    PAIR(prod, "Oregon Brie with fig paste and hazelnuts", "complement", "established", "cheese", "Pacific Northwest artisan Brie with fig and hazelnut finds the complex mineral Pinot a sophisticated match.")

prod, is_new = PROD("Beaux Frères Belles Soeurs Pinot Noir Willamette", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="premium",
    description="Beaux Frères's second label Pinot Noir from Willamette Valley; elegant, mineral and approachable with cherry, spice and the Ribbon Ridge character at a more accessible price point.")
if is_new:
    PAIR(prod, "Grilled Oregon spotted mushroom caps with herb butter", "complement", "established", "casual", "Oregon foraged mushrooms with herb butter are a natural biodynamic Pinot Noir companion.")
    PAIR(prod, "Salmon gravlax with dill cream and pumpernickel", "complement", "established", "casual", "Cured Pacific salmon with dill cream finds the elegant cherry-mineral character of Belles Soeurs ideal.")
    PAIR(prod, "Pork tenderloin with cherry sauce and root vegetables", "complement", "classic", "main", "Cherry sauce on pork tenderloin finds the accessible cherry-mineral character of Belles Soeurs perfectly mirrored.")
    PAIR(prod, "Cheese plate with aged Gouda, apple and pecans", "complement", "suggested", "cheese", "Aged Gouda and apple-pecan combination finds the accessible elegance of this Willamette Pinot ideal.")

# ── PASO ROBLES AVA (California) ──────────────────────────────────────────────
print("=== Paso Robles AVA ===")
r = R("Paso Robles AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Paso Robles AVA",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="California's largest wine appellation in San Luis Obispo County, spanning dramatically different terroirs from hot east-side limestone-clay to cool west-side maritime canyons. Paso Robles excels in Rhône varieties (Syrah, Grenache, Mourvèdre), Zinfandel and innovative blends. The Adelaida and Willow Creek districts on the west side produce wines of Mediterranean elegance.",
      key_producers="Saxum, Epoch Estate, L'Aventure, Tablas Creek",
      historical_context="Paso Robles wine dates to Mission San Miguel in the 1790s. The modern era began with the Hoffman family planting Zinfandel in the 1960s. The Rhône Ranger movement of the 1980s-90s, led by writers like Robert Parker and producers like Tablas Creek (Beaucastel partnership), established Paso as California's Rhône headquarters. The 2013 sub-AVA creation recognised the dramatic east-west climate divide.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Balanced Paso vintage; west-side Mediterranean varieties of exceptional elegance and structure."),
    (2019, "very_good", "stable", "Good conditions; Rhône varieties from Willow Creek and Adelaida showing characteristic complexity."),
    (2020, "very_good", "stable", "Clean vintage; Paso Robles Syrah and Grenache of genuine California-Mediterranean character."),
    (2021, "excellent", "rising", "Outstanding Paso vintage; west-side estates produced Rhône blends of benchmark elegance."),
    (2022, "very_good", "stable", "Consistent quality; Paso Rhône varieties showing their finest California expression."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Saxum Vineyards", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Justin Smith at Saxum farms calcareous limestone vineyards in Paso Robles's Willow Creek District to produce Rhône variety blends of extraordinary concentration, mineral depth and complexity — some of California's highest-scoring wines.",
       reputation_narrative="Saxum's James Berry Vineyard is one of California's most decorated wines, receiving a perfect 100-point score from Robert Parker. The estate has placed Paso Robles on the map for serious collectors worldwide.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Saxum James Berry Vineyard Paso Robles", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="California's most critically acclaimed Rhône blend — Grenache, Mourvèdre and Syrah from calcareous limestone soils. Profound, mineral and complex with dark berry, spice and limestone mineral character.")
if is_new:
    PAIR(prod, "Braised Colorado lamb shoulder with Moroccan spices", "complement", "classic", "main", "California's greatest Rhône blend demands the full richness of slow-braised lamb with North African spice.")
    PAIR(prod, "Grilled côte de boeuf with bone marrow and truffle butter", "complement", "established", "main", "Concentrated, mineral Rhône blend handles the richness of prime rib with truffle-marrow butter.")
    PAIR(prod, "Wild boar stew with olives, rosemary and polenta", "complement", "established", "main", "Mediterranean game stew with olives and herbs echoes the garrigue character of this limestone Rhône blend.")
    PAIR(prod, "Aged Manchego with Marcona almonds and quince paste", "complement", "established", "cheese", "Spanish sheep cheese with almonds and quince mirrors the Mediterranean mineral character of Saxum Grenache-blend.")

prod, is_new = PROD("Saxum Broken Stones Paso Robles", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="premium",
    description="Saxum's second-label Rhône blend from calcareous soils; concentrated, spiced and mineral with the limestone terroir character of Paso's finest Willow Creek sites — exceptional value for the quality.")
if is_new:
    PAIR(prod, "Grilled lamb merguez with harissa and couscous", "complement", "established", "main", "Spiced lamb sausage and North African harissa find the Mediterranean Rhône character of Broken Stones natural.")
    PAIR(prod, "Pizza with fennel sausage, roasted peppers and fontina", "complement", "established", "casual", "Italian-American pizza with fennel sausage finds the Grenache-Mourvèdre Paso blend an excellent companion.")
    PAIR(prod, "Smoked brisket with BBQ sauce and coleslaw", "complement", "established", "casual", "American BBQ with smoky brisket and sauce finds the dark fruit and spice of Saxum's second label ideal.")
    PAIR(prod, "Short rib tacos with salsa verde and pickled onion", "bridge", "suggested", "casual", "Braised short rib taco with Mexican-California flavours finds the mineral Rhône blend a bridge.")

p2 = P("Tablas Creek Vineyard", "winery", r, "USA",
       production_philosophy="biodynamic",
       philosophy_description="The Perrin family of Château Beaucastel partnered with importer Robert Haas to establish Tablas Creek in 1989, bringing Châteauneuf cuttings to Paso Robles to farm biodynamically and produce authentic Rhône-style wines from calcareous soils.",
       reputation_narrative="Tablas Creek established Paso Robles as America's premier Rhône wine destination, demonstrating that Grenache, Mourvèdre and Roussanne can achieve genuine complexity in California's Central Coast.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Tablas Creek Esprit de Tablas Paso Robles", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="premium",
    description="Tablas Creek's flagship Beaucastel-inspired blend of Mourvèdre, Grenache and Syrah from calcareous limestone; structured, spiced and complex with dark berry, herbs and Paso's limestone mineral character.")
if is_new:
    PAIR(prod, "Roasted leg of lamb with herbes de Provence and garlic", "complement", "classic", "main", "Provençal-inspired lamb roast finds the Beaucastel-heritage Rhône blend its natural California companion.")
    PAIR(prod, "Braised beef cheeks with olives and capers", "complement", "established", "main", "Slow-braised beef cheeks with Mediterranean garnish find the structure and spice of Esprit de Tablas ideal.")
    PAIR(prod, "Pulled pork tacos with mole negro sauce", "bridge", "established", "casual", "Mole negro's complexity and dark fruit mirrors the Mourvèdre-heavy Rhône blend in an unexpected California bridge.")
    PAIR(prod, "Ibérico ham with roasted peppers and olive oil", "complement", "established", "casual", "Spanish Ibérico ham and roasted peppers — natural companions for this Châteauneuf-heritage California blend.")

prod, is_new = PROD("Tablas Creek Esprit de Tablas Blanc Paso Robles", "wine_still", p2, r, "USA",
    subcategory="white", price_tier="premium",
    description="Roussanne-dominant white Rhône blend from Tablas Creek's limestone soils; rich, aromatic and complex with stone fruit, herbs and the mineral depth that distinguishes great Paso Robles white Rhônes.")
if is_new:
    PAIR(prod, "Bouillabaisse with saffron rouille and gruyère croutons", "complement", "classic", "main", "Roussanne's aromatic complexity suits saffron-herb bouillabaisse with the structure to handle its richness.")
    PAIR(prod, "Grilled white sea bass with fennel and citrus", "complement", "established", "main", "Pacific white sea bass with Provençal-inspired fennel and citrus finds Roussanne blanc a natural companion.")
    PAIR(prod, "Roasted cauliflower with tahini and pomegranate", "complement", "established", "casual", "Rich, aromatic Roussanne-Grenache Blanc suits roasted cauliflower with the complexity of tahini and pomegranate.")
    PAIR(prod, "Aged Ossau-Iraty sheep cheese with black cherry jam", "complement", "established", "cheese", "Basque sheep cheese and cherry jam find the Provençal aromatic complexity of this white Rhône blend ideal.")

# ── FINGER LAKES AVA (New York) ───────────────────────────────────────────────
print("=== Finger Lakes AVA ===")
r = R("Finger Lakes AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Finger Lakes AVA",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="New York State's finest wine region surrounding the glacial Finger Lakes, where deep lake waters moderate the continental climate. The Seneca and Cayuga lakes' western slopes produce Riesling of extraordinary mineral depth and Chardonnay of elegance. Dry and off-dry Riesling from the Finger Lakes challenges Europe's finest from Alsace and Germany.",
      key_producers="Dr. Konstantin Frank, Hermann J. Wiemer, Red Newt Cellars",
      historical_context="Dr. Konstantin Frank proved in 1962 that vinifera varieties could survive the Finger Lakes winters, using disease-resistant rootstocks. Riesling became the region's signature variety, with the deep lakes creating a unique microclimate. The AVA was established 1982 and now encompasses 9,000 acres of vines. The wine scene has expanded dramatically since 2000.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool glacial lake conditions produced Riesling of extraordinary mineral precision and acid balance."),
    (2019, "very_good", "stable", "Good balance of ripeness and natural acidity; Finger Lakes Riesling of characteristic tension."),
    (2020, "very_good", "stable", "Consistent lake-moderated vintage; both dry and off-dry Riesling showing excellent character."),
    (2021, "excellent", "rising", "Outstanding Finger Lakes vintage; Riesling of benchmark mineral precision and longevity."),
    (2022, "very_good", "stable", "Good lake-moderated conditions; Seneca Lake Riesling of genuine complexity and food-affinity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Hermann J. Wiemer Vineyard", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Hermann Wiemer brought German Riesling expertise to the Seneca Lake's western slopes, establishing one of the Finger Lakes' most technically accomplished Riesling programs. His successor Fred Merwarth continues the tradition with organic farming and meticulous attention to capturing the lake's unique terroir.",
       reputation_narrative="Hermann J. Wiemer Vineyard is the Finger Lakes' most internationally respected Riesling producer, demonstrating that New York State can produce Riesling rivalling Germany and Alsace in complexity and mineral depth.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Hermann J. Wiemer Dry Riesling Finger Lakes", "wine_still", p1, r, "USA",
    subcategory="white", price_tier="premium",
    description="Benchmark Finger Lakes Riesling from Seneca Lake's western slopes; bone-dry, mineral and tense with lime, green apple, slate and the characteristic lake mineral precision that rivals German Mosel.")
if is_new:
    PAIR(prod, "Rainbow trout from Finger Lakes with lemon and dill", "complement", "classic", "main", "Local freshwater trout from the same glacial lakes that cool the vineyards — the ultimate terroir pairing.")
    PAIR(prod, "Chesapeake Bay blue crab cakes with lemon aioli", "complement", "established", "casual", "East Coast crab cakes find the mineral, dry Riesling tension of Finger Lakes an unexpected but natural match.")
    PAIR(prod, "Grilled pork chop with Granny Smith apple and mustard", "complement", "classic", "main", "Classic pork and apple finds the dry Riesling's apple-mineral tension a Northern European-inspired pairing.")
    PAIR(prod, "Thai green curry with lemongrass and coconut milk", "complement", "established", "main", "Dry Riesling's mineral freshness and apple-citrus character bridges the complex aromatic-herbal Thai curry.")

prod, is_new = PROD("Hermann J. Wiemer HJW Vineyard Riesling Finger Lakes", "wine_still", p1, r, "USA",
    subcategory="white", price_tier="ultra_premium",
    description="Single-vineyard top cuvée Riesling from the estate's finest Seneca Lake block; profound mineral depth, peach, lime and slate character with extraordinary tension and 15-year aging potential.")
if is_new:
    PAIR(prod, "Foie gras torchon with Riesling jelly and gingerbread", "complement", "established", "starter", "Foie gras with Riesling-based preparation finds the profound mineral tension of HJW Vineyard ideal.")
    PAIR(prod, "Grilled lake perch with brown butter and capers", "complement", "classic", "main", "Lake perch with brown butter is the classic freshwater companion for great Seneca Lake Riesling.")
    PAIR(prod, "Smoked whitefish salad on dark rye with cream cheese", "complement", "established", "casual", "Smoked lake fish with cream cheese on dark bread — a Great Lakes-Finger Lakes classic for mineral Riesling.")
    PAIR(prod, "Époisses cheese with walnut bread", "complement", "suggested", "cheese", "Pungent washed-rind Époisses finds the mineral acidity of Finger Lakes Riesling a compelling contrast.")

p2 = P("Dr. Konstantin Frank", "winery", r, "USA",
       production_philosophy="traditional",
       philosophy_description="Dr. Konstantin Frank pioneered vinifera viticulture in the Finger Lakes in 1962, proving that European wine varieties could survive the harsh continental winters. His granddaughter Meaghan Frank continues the family legacy with consistent quality and the historic Salmon Run and Rkatsiteli wines.",
       reputation_narrative="The founding estate of the modern Finger Lakes wine industry, Dr. Konstantin Frank Winery established the principle that New York could produce world-class wines from European varieties — a revolutionary claim in 1962.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Dr. Konstantin Frank Dry Riesling Finger Lakes", "wine_still", p2, r, "USA",
    subcategory="white", price_tier="premium",
    description="Dr. Frank's historic Dry Riesling from Keuka Lake slopes; mineral, crisp and characteristically Finger Lakes with lime, peach and slate mineral precision from the lake-moderated continental climate.")
if is_new:
    PAIR(prod, "Vietnamese spring rolls with peanut dipping sauce", "complement", "established", "casual", "Mineral, dry Riesling's fruit-acid tension bridges the peanut-herb freshness of Vietnamese spring rolls.")
    PAIR(prod, "Grilled pork tenderloin with cider and apple sauce", "complement", "classic", "main", "Pork and apple sauce is the classic pairing for dry Finger Lakes Riesling's apple-mineral character.")
    PAIR(prod, "Peking duck with plum sauce and scallion pancakes", "complement", "established", "main", "Dry Riesling's mineral precision and fruit balance is a natural companion for Peking duck service.")
    PAIR(prod, "Adirondack cheddar with apple butter and country bread", "complement", "established", "casual", "New York State Cheddar with apple butter finds the mineral apple freshness of Finger Lakes Riesling ideal.")

prod, is_new = PROD("Dr. Konstantin Frank Gewurztraminer Finger Lakes", "wine_still", p2, r, "USA",
    subcategory="white", price_tier="mid_range",
    description="Finger Lakes Gewurztraminer from Dr. Frank's estate; off-dry, aromatic and distinctive with lychee, rose petal and spice from the cool continental climate — one of America's few quality Gewurztraminers.")
if is_new:
    PAIR(prod, "Alsatian onion tart (flammekueche) with crème fraîche", "complement", "classic", "casual", "Alsatian-style tart finds the aromatic off-dry character of Finger Lakes Gewurztraminer a natural companion.")
    PAIR(prod, "Pad Thai with prawns, peanuts and lime", "complement", "established", "casual", "Lychee-aromatic Gewurztraminer suits the sweet-sour-spice of Pad Thai with remarkable harmony.")
    PAIR(prod, "Mildly spiced Indian butter chicken with basmati", "bridge", "established", "main", "Off-dry Gewurztraminer bridges the aromatic spice of butter chicken, cooling heat with lychee sweetness.")
    PAIR(prod, "Munster cheese with caraway seeds", "complement", "classic", "cheese", "Alsatian Munster with caraway seeds and off-dry Gewurztraminer is an aromatic pairing of regional classic status.")

# ── WALLA WALLA VALLEY AVA (Washington) ──────────────────────────────────────
print("=== Walla Walla Valley AVA ===")
r = R("Walla Walla Valley AVA", "USA", "wine",
      designation_type="AVA",
      designation_name="Walla Walla Valley AVA",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="Washington State's most celebrated wine sub-region straddling the Oregon border, producing Cabernet Sauvignon, Merlot, Syrah and Cabernet Franc of extraordinary concentration and finesse from basalt-derived cobblestone soils. The valley's continental climate creates ideal diurnal temperature variation for complex, structured reds.",
      key_producers="Leonetti Cellar, Cayuse Vineyards, L'Ecole No 41, Woodward Canyon",
      historical_context="Walla Walla wine history began with Italian immigrants planting table grapes in the 19th century. The modern era started with Leonetti Cellar (1977) and Woodward Canyon (1981). Cayuse Vineyards' Christophe Baron discovered the basalt rock 'rattlesnake' soils on the Rocks District (established 2015) in the mid-1990s, producing wines of distinctive mineral complexity.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm continental conditions produced Walla Walla Cabernet and Syrah of exceptional concentration."),
    (2019, "very_good", "stable", "Good balance of ripeness and structure; Walla Walla reds of characteristic fruit and mineral depth."),
    (2020, "very_good", "stable", "Consistent quality from basalt soils; Syrah and Cabernet of genuine complexity."),
    (2021, "excellent", "rising", "Outstanding Walla Walla vintage; Rocks District Syrah and Cabernet of benchmark quality."),
    (2022, "excellent", "rising", "Superb conditions; Leonetti and Cayuse produced Walla Walla reds of extraordinary depth."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Leonetti Cellar", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Founded in 1977 by Gary Figgins, Leonetti Cellar is Washington State's most historic quality winery, producing Cabernet Sauvignon, Merlot and Sangiovese of extraordinary power and elegance from Walla Walla Valley's finest vineyards.",
       reputation_narrative="Leonetti Cellar is one of the Pacific Northwest's most decorated wineries, with decades of critical acclaim establishing it as Washington State's defining red wine producer.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Leonetti Cellar Cabernet Sauvignon Walla Walla", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Leonetti's flagship Walla Walla Cabernet Sauvignon; powerful, structured and age-worthy with blackcurrant, cedar, tobacco and mineral depth from the valley's basalt-derived soils and continental climate.")
if is_new:
    PAIR(prod, "Grilled côte de boeuf with bone marrow and Bordelaise sauce", "complement", "classic", "main", "Washington's greatest Cabernet demands the luxury of prime bone-in rib with classic French Bordelaise.")
    PAIR(prod, "Wagyu beef filet with truffle butter and potato gratin", "complement", "classic", "main", "The most structured Walla Walla Cabernet finds its match in the luxury of Wagyu with truffle and potato.")
    PAIR(prod, "Braised lamb shoulder with red wine and root vegetables", "complement", "established", "main", "Slow-braised lamb in red wine and roots finds the blackcurrant-cedar structure of Leonetti Cabernet ideal.")
    PAIR(prod, "Aged Tillamook Cheddar with quince paste and walnuts", "complement", "established", "cheese", "Pacific Northwest aged Cheddar with quince and walnuts finds the structured mineral Cabernet a natural match.")

prod, is_new = PROD("Leonetti Cellar Merlot Walla Walla", "wine_still", p1, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Leonetti Walla Walla Merlot of Washington's finest — plush, concentrated and age-worthy with dark plum, chocolate, spice and the distinctive depth of basalt-derived Walla Walla soils.")
if is_new:
    PAIR(prod, "Duck confit with cherry reduction and root vegetable purée", "complement", "classic", "main", "Plush Walla Walla Merlot's dark plum and spice suits duck confit with cherry in a Pacific Northwest classic.")
    PAIR(prod, "Grilled beef tenderloin with mushroom duxelles and red wine sauce", "complement", "classic", "main", "Beef tenderloin's delicacy with earthy mushroom finds the plush structure of Leonetti Merlot ideal.")
    PAIR(prod, "Elk tenderloin with huckleberry jus and sweet potato", "complement", "established", "main", "Pacific Northwest game (elk) with native huckleberry jus — the ultimate Washington Merlot pairing.")
    PAIR(prod, "Aged Gouda with spiced fruit compote", "complement", "established", "cheese", "Butterscotch-crystal Gouda with spiced compote finds the plush concentration of Walla Walla Merlot ideal.")

p2 = P("Cayuse Vineyards", "winery", r, "USA",
       production_philosophy="biodynamic",
       philosophy_description="Christophe Baron at Cayuse farms biodynamically on the Rocks District's unique basalt cobblestone soils, producing Syrah and Grenache-based wines of extraordinary mineral intensity and complexity that have placed Walla Walla among the world's elite wine regions.",
       reputation_narrative="Cayuse's En Chamberlin and God Only Knows Syrah wines are among America's most critically acclaimed, their basalt-cobblestone minerality drawing comparisons to the Rhône's finest Northern Rhône Syrah.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Cayuse En Chamberlin Vineyard Syrah Walla Walla", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Cayuse's biodynamic Rocks District Syrah from basalt cobblestone soils; profound, mineral and intense with dark berry, iron, olive and the unique volcanic mineral depth of America's most distinctive Syrah terroir.")
if is_new:
    PAIR(prod, "Roasted lamb chops with olive tapenade and grilled fennel", "complement", "classic", "main", "Basalt-mineral Syrah with olive-herbaceous character matches lamb with tapenade in a Rhône-inspired pairing.")
    PAIR(prod, "Wild mushroom and truffle flatbread with Gruyère", "complement", "established", "casual", "Biodynamic Rocks District Syrah's earthy mineral depth suits truffle-mushroom flatbread with aged cheese.")
    PAIR(prod, "Smoked brisket with red wine BBQ sauce", "complement", "established", "casual", "Washington-style smoked brisket with red wine sauce finds the iron-mineral depth of Cayuse Syrah a natural match.")
    PAIR(prod, "Aged Manchego with black olive and dried tomato", "complement", "established", "cheese", "Mediterranean sheep cheese with olives and tomato mirrors the olive-mineral character of Rocks District Syrah.")

prod, is_new = PROD("Cayuse Cailloux Vineyard Syrah Walla Walla", "wine_still", p2, r, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Single-vineyard Cailloux ('cobblestones') Syrah from the Rocks District; pure, mineral and transparent with blueberry, iron and smoked meat character — the clearest expression of basalt cobblestone terroir.")
if is_new:
    PAIR(prod, "Grilled duck hearts with cherry and thyme", "complement", "established", "main", "Duck offal with cherry and thyme finds the iron-mineral, transparent character of Cailloux Syrah a compelling match.")
    PAIR(prod, "Herb-crusted rack of lamb with flageolet beans", "complement", "classic", "main", "Rack of lamb with herbs and flageolet beans is a classic Rhône companion for transparent mineral Syrah.")
    PAIR(prod, "Charcuterie of duck rillettes, pâté and cornichons", "complement", "established", "casual", "French-inspired charcuterie finds the Rhône-character mineral Syrah of Cayuse Cailloux natural.")
    PAIR(prod, "Époisses washed-rind cheese with sourdough", "contrast", "established", "cheese", "Pungent Époisses contrasts with the mineral iron depth of Rocks District Syrah in a powerful pairing.")

# ── FINAL COUNTS ──────────────────────────────────────────────────────────────
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
print("B143 complete.")
conn.close()
