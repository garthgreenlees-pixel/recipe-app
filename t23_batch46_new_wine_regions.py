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

# ── 1. YAMANASHI (Japan) ─────────────────────────────────────────────────────
print("\n=== Yamanashi (Japan) ===")
r = R("Yamanashi", "Japan", "wine",
      designation_type="GI",
      designation_name="GI Yamanashi",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Japan's most important wine-producing prefecture and home to the Koshu grape — Japan's only internationally recognised indigenous wine variety. Yamanashi sits at the foot of Mount Fuji, with alluvial soils and a humid continental climate challenging for viticulture but rewarded by meticulous Japanese farming precision. Koshu produces delicate, dry whites of characteristic citrus, white peach, and subtle mineral character, ideal for Japanese cuisine.",
      key_producers="Grace Wine (Chuo Budoshu), Chateau Mercian, Lumiere Winery, Suntory Tomi No Oka, Marufuji Rubaiyat",
      historical_context="Wine production in Yamanashi began in the Meiji era (1870s) when the Japanese government sent students to France to learn winemaking. The Koshu grape, believed to have arrived via the Silk Road, has been cultivated in the Katsunuma district for over 1,000 years. Yamanashi received Japan's first Geographical Indication for wine in 2013, and Koshu was accepted as an international variety by the OIV in 2010.")

VIN(r, 2023, "excellent", "rising", "Favourable Yamanashi growing season; outstanding Koshu freshness and mineral precision")
VIN(r, 2022, "very_good", "stable", "Good vintage; typical Koshu citrus-mineral profile at full expression")
VIN(r, 2021, "good", "stable", "La Nina rainfall challenged the harvest but Japanese meticulous canopy management preserved fruit quality")
VIN(r, 2020, "very_good", "stable", "Long, warm season; Koshu with unusual concentration and depth")
VIN(r, 2019, "excellent", "rising", "Benchmark Yamanashi vintage; most complex Koshu in recent years")

p1 = P("Grace Wine Chuo Budoshu", "Japan", r, "winery",
        "Japan's most internationally acclaimed wine estate, Grace Wine produces benchmark Koshu and Muscat Bailey A wines from estate vineyards in the Akeno district of Yamanashi. Their Cuvee Misawa single-vineyard Koshu has won international competitions and is considered the definitive expression of what Japanese wine can achieve.")
prod1, new1 = PROD("Grace Wine Cuvee Misawa Koshu Yamanashi GI", "wine_still", p1, r, "Japan",
    subcategory="Koshu",
    description="Japan's most celebrated indigenous white wine; single-vineyard Koshu from Akeno with delicate citrus blossom, white peach, yuzu, and a clean mineral-saline finish — the benchmark for Japanese wine",
    price_tier="premium")
if new1:
    PAIR(prod1, "Tofu dengaku with miso and sesame", "complement", "classic", "main", "Delicate, mineral Koshu with subtle fermented soy notes resonates naturally with the savoury-sweet miso glaze on silken tofu")
    PAIR(prod1, "Grilled sea bream (tai) with yuzu and sudachi", "complement", "classic", "main", "The wine's yuzu and citrus character and mineral precision are a natural foil for Japan's most ceremonial whole fish")
    PAIR(prod1, "Steamed hairy crab (kegani) with ponzu", "complement", "established", "main", "Koshu's delicate mineral freshness is the perfect match for the clean sweet flavour of premium Japanese crab")
    PAIR(prod1, "Sashimi platter with wasabi and soy", "cleanse", "classic", "main", "Japanese Koshu and premium sashimi: the wine's delicacy cleanses the palate between cuts with mineral clarity")

p2 = P("Chateau Mercian", "Japan", r, "winery",
        "One of Japan's oldest and most influential wine producers, established by Suntory in 1877 and now a Kirin group brand. Chateau Mercian's Kikyogahara Merlot and Koshu Kikyogahara wines are considered Japan's benchmarks for international varieties and for demonstrating Yamanashi's potential for world-class wine production.")
prod2, new2 = PROD("Chateau Mercian Koshu Kikyogahara Yamanashi GI", "wine_still", p2, r, "Japan",
    subcategory="Koshu",
    description="Classic Yamanashi Koshu from Kikyogahara's alluvial soils; fresh, light-bodied with lemon, white peach, and subtle minerals — ideal expression of the variety's food-friendly delicacy",
    price_tier="mid_range")
if new2:
    PAIR(prod2, "Tempura prawns and vegetables with dipping salt and lemon", "complement", "classic", "main", "The wine's light body and citrus freshness are the ideal complement for crisp tempura batter and delicate fried seafood")
    PAIR(prod2, "Chilled soba with yuzu dipping sauce", "complement", "classic", "main", "Koshu's citrus-mineral character and the bright buckwheat dipping sauce create a seamlessly Japanese pairing")
    PAIR(prod2, "Japanese clam miso soup with tofu", "complement", "established", "starter", "The wine's delicate mineral and umami resonance pairs naturally with the clean savoury depth of clam miso")
    PAIR(prod2, "Grilled squid with soy and ginger", "complement", "established", "main", "Light, fresh Koshu with citrus and mineral lift handles the savoury richness of chargrilled squid with Japanese seasoning")

# ── 2. MONTSANT (Spain) ──────────────────────────────────────────────────────
print("\n=== Montsant (Spain) ===")
r2 = R("Montsant", "Spain", "wine",
       designation_type="DO",
       designation_name="DO Montsant",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="The ring-shaped DO surrounding Priorat, producing wines of similar character from old-vine Garnacha and Carinyena at significantly more accessible prices. Montsant's soils include the same llicorella slate that defines Priorat alongside limestone and clay, producing wines with genuine depth and the wild Mediterranean character of the Ebro basin. Often called the best-value wine region in Spain.",
       key_producers="Celler de Capçanes, Venus la Universal, Acustic Celler, Estones de Montsant, Mas Perinet",
       historical_context="Montsant was carved out of the Falset sub-region of the larger Tarragona DO in 2001, recognising the distinct quality of old-vine Garnacha and Carinyena surrounding the Priorat. The region attracted investment from quality-focused producers who found Priorat prices prohibitive but saw the same llicorella and limestone potential in neighbouring Montsant villages. Today it is considered one of Spain's greatest value-for-quality appellations.")

VIN(r2, 2023, "excellent", "rising", "Outstanding growing season; old-vine Garnacha of unusual freshness and Mediterranean depth")
VIN(r2, 2022, "very_good", "rising", "Very good vintage; structured, layered Garnacha-Carinyena blends with excellent aging potential")
VIN(r2, 2021, "good", "stable", "Slightly cooler; wines of good freshness and the characteristic wild herb and dark berry profile")
VIN(r2, 2020, "excellent", "rising", "Benchmark Montsant vintage; concentrated, age-worthy reds at exceptional value")
VIN(r2, 2019, "very_good", "stable", "Classic vintage with reliable quality across the appellation")

p3 = P("Celler de Capcanes", "Spain", r2, "winery",
        "One of Montsant's most celebrated and historically important producers, Celler de Capcanes is a cooperative that has been pivotal in establishing the DO's reputation. Their Mas Donís Barrica and Peraj Hat'laHa (Flor de Primavera) wines have achieved international recognition, demonstrating that Montsant can produce wines of Priorat-level seriousness at half the price.")
prod3, new3 = PROD("Celler de Capcanes Mas Donis Barrica Montsant DO", "wine_still", p3, r2, "Spain",
    subcategory="Garnacha Syrah",
    description="Benchmark Montsant red; old-vine Garnacha and Syrah from llicorella slate soils — dense, mineral, and concentrated with dark blackberry, wild thyme, licorice, and a long structural finish",
    price_tier="mid_range")
if new3:
    PAIR(prod3, "Slow-roasted Catalan suckling pig with romesco sauce", "complement", "classic", "main", "Dense, mineral Garnacha-based wine from the Ebro basin is a natural match for Catalan roast pork with the region's iconic pepper-almond sauce")
    PAIR(prod3, "Escalivada (grilled eggplant and peppers) on sourdough", "complement", "established", "starter", "The wine's wild herb and mineral depth resonates with the smoky, sweet roasted vegetables of this Catalan classic")
    PAIR(prod3, "Cured black Iberian chorizo with manchego", "complement", "established", "starter", "Dense, structured Montsant handles the spiced richness of Iberian chorizo and the saltiness of aged manchego with its firm structure")
    PAIR(prod3, "Rabbit all-i-oli with wild mushrooms and saffron", "complement", "classic", "main", "Old-vine Garnacha and rabbit in Catalan all-i-oli (garlic emulsion) is a deeply regional and satisfying pairing")

p4 = P("Acustic Celler", "Spain", r2, "winery",
        "A small artisan estate in Montsant producing natural-leaning wines from old-vine Garnacha, Carinyena, and Garnacha Blanca. Their Acustic Blanc and Brao wines are considered some of the most terroir-expressive and mineral-precise wines in the appellation, made with minimal intervention and remarkable concentration.")
prod4, new4 = PROD("Acustic Celler Blanc Montsant DO", "wine_still", p4, r2, "Spain",
    subcategory="Garnacha Blanca Macabeo",
    description="Montsant's finest white wine; old-vine Garnacha Blanca and Macabeo from llicorella soils — textured, oxidatively complex with honeyed lemon, almonds, and a saline mineral finish",
    price_tier="premium")
if new4:
    PAIR(prod4, "Grilled langoustines with Catalan olive oil", "complement", "established", "main", "The wine's textured mineral and citrus-almond complexity is a superb match for sweet langoustine with quality olive oil")
    PAIR(prod4, "Pa amb tomaquet with anchovies and olives", "complement", "classic", "starter", "Oxidatively complex Garnacha Blanca and the Catalan classic of tomato-rubbed bread with salt-cured anchovies — deeply regional")
    PAIR(prod4, "Grilled monkfish with romesco", "complement", "established", "main", "Textured, mineral white holds up to firm-fleshed monkfish with the bold flavors of romesco pepper-almond sauce")
    PAIR(prod4, "Aged Manchego or Idiazabal with quince paste", "bridge", "suggested", "cheese", "The wine's oxidative almond notes bridge naturally with sharp aged Spanish hard cheese and sweet membrillo")

# ── 3. BERGERAC (France) ─────────────────────────────────────────────────────
print("\n=== Bergerac (France) ===")
r3 = R("Bergerac", "France", "wine",
       designation_type="AOC",
       designation_name="Bergerac AOC",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="The Bordeaux-adjacent wine region of the Dordogne, producing wines from Bordeaux's classic varieties at more accessible prices. Bergerac's best estates — particularly in Monbazillac for sweet wine and Pecharmant for structured reds — match or exceed many classified Bordeaux growths in quality. The region is also Semillon's second great home after Sauternes, producing both dry and sweet versions of extraordinary character.",
       key_producers="Chateau Tour des Gendres, Chateau Tirecul La Graviere, Elian Da Ros, Chateau de Tiregand, Chateau Lestignac",
       historical_context="Bergerac's wine history is inseparable from the Bordeaux trade, which for centuries dammed the Dordogne River to prevent Bergerac wines from reaching English markets ahead of Bordeaux exports. The region fell into obscurity for much of the 20th century but has been revived by a generation of quality-focused producers who see the terroir potential unrealised by the volume-driven past.")

VIN(r3, 2023, "excellent", "rising", "Excellent Dordogne growing season; fine dry whites and structured reds with good acidity")
VIN(r3, 2022, "very_good", "rising", "Good vintage; Bergerac reds of unusual depth and Monbazillac of excellent botrytis development")
VIN(r3, 2021, "good", "stable", "Challenging year in southwest France; careful selection rewarded with elegant, food-friendly wines")
VIN(r3, 2020, "very_good", "stable", "Hot vintage; concentrated reds and richly botrytised Monbazillac sweet whites")
VIN(r3, 2019, "excellent", "rising", "Benchmark vintage for the region; finest Bergerac reds and Monbazillac in a generation")

p5 = P("Chateau Tour des Gendres", "France", r3, "winery",
        "The most internationally respected estate of the Bergerac appellation, Luc de Conti produces wines of Bordeaux Grand Cru quality from his biodynamic Dordogne vineyards. His Cuvee des Conti Bergerac Blanc and the Gloire de Mon Pere red are benchmarks that routinely outperform wines costing three times as much.")
prod5, new5 = PROD("Chateau Tour des Gendres Cuvee des Conti Bergerac Blanc", "wine_still", p5, r3, "France",
    subcategory="Semillon Sauvignon Blanc Muscadelle",
    description="Bergerac's benchmark dry white; biodynamic Semillon-dominant blend with waxy lemon curd, white peach, and a complex mineral depth that rivals fine Bordeaux Blanc at a fraction of the price",
    price_tier="mid_range")
if new5:
    PAIR(prod5, "Foie gras du Perigord with toasted brioche", "complement", "classic", "main", "Rich, waxy Semillon-based white and Perigord foie gras is one of the Dordogne's most celebrated regional food-wine combinations")
    PAIR(prod5, "River trout with brown butter and capers (truite meuniere)", "complement", "classic", "main", "Textured, mineral Bergerac white with river trout from the Dordogne — a deeply regional and beautiful pairing")
    PAIR(prod5, "Grilled sea bass with sauce beurre blanc", "complement", "established", "main", "Semillon's weight and citrus character frame the delicacy of sea bass in classic beurre blanc sauce")
    PAIR(prod5, "Aged Brillat-Savarin triple cream cheese with fig jam", "bridge", "suggested", "cheese", "The wine's waxy, lemon curd richness bridges with the luxurious triple cream cheese and sweet fig")

p6 = P("Chateau Tirecul La Graviere", "France", r3, "winery",
        "The undisputed benchmark for Monbazillac AOC, Chateau Tirecul La Graviere produces some of France's greatest sweet wines from Semillon and Muscadelle affected by noble rot in the Dordogne valley. Their Cuvee Madame has been rated one of the world's greatest sweet wines, comparing favourably with Chateau d'Yquem at a fraction of the price.")
prod6, new6 = PROD("Chateau Tirecul La Graviere Monbazillac AOC", "wine_dessert", p6, r3, "France",
    subcategory="Semillon Muscadelle",
    description="France's finest Monbazillac sweet wine; botrytised Semillon and Muscadelle of extraordinary concentration — saffron, apricot jam, honey, and orange marmalade with a clean acid backbone that promises decades of aging",
    price_tier="premium")
if new6:
    PAIR(prod6, "Foie gras du Perigord mi-cuit with truffle", "complement", "classic", "starter", "The most classic of Dordogne pairings: Monbazillac and foie gras together in the region's most celebrated food-wine combination")
    PAIR(prod6, "Roquefort with walnut bread and grape jam", "contrast", "classic", "cheese", "The sweet Monbazillac and pungent Roquefort is one of France's great sweet-savoury contrasts; the wine's acidity cuts through the salt")
    PAIR(prod6, "Tarte Tatin avec creme fraiche", "complement", "established", "dessert", "Caramelised apple tart and honey-apricot Monbazillac are a natural Perigord dessert combination")
    PAIR(prod6, "Stilton with port and walnut cake", "contrast", "adventurous", "cheese", "The interplay of Monbazillac's saffron-honeyed sweetness against powerful Stilton makes for a memorable cheese course")

# ── 4. PALMELA (Portugal) ────────────────────────────────────────────────────
print("\n=== Palmela (Portugal) ===")
r4 = R("Palmela", "Portugal", "wine",
       designation_type="DOC",
       designation_name="DOC Palmela",
       reputation_tier="respected",
       quality_trajectory="established",
       description="The Setubal Peninsula's most significant wine DO, south of Lisbon on the south bank of the Tagus. Palmela is the home territory of the Castelao grape (formerly Periquita) and produces wines of remarkable earthy, cherry-fruited character alongside Moscatel de Setubal — one of Portugal's great fortified wine traditions. The sandy soils of the peninsula give wines a distinctive light elegance unusual in Portuguese reds.",
       key_producers="Jose Maria da Fonseca, Bacalhoa Wines of Portugal, Quinta do Monte d'Oiro, Pegos Claros",
       historical_context="Palmela's wine history is dominated by the Jose Maria da Fonseca company, founded in 1834 and one of Portugal's oldest and most respected wine producers. Fonseca's Periquita (named for the Castelao grape's nickname) was one of the first Portuguese wines to achieve international export success. The Moscatel de Setubal fortified wine tradition dates to at least the 18th century.")

VIN(r4, 2023, "very_good", "stable", "Good Setubal Peninsula season; reliable Castelao character and Moscatel concentration")
VIN(r4, 2022, "excellent", "stable", "Excellent vintage; finest Palmela Castelao in recent years with good structure for aging")
VIN(r4, 2021, "good", "stable", "Solid vintage with the characteristic earthy, cherry fruit of the peninsula's sandy soils")
VIN(r4, 2020, "very_good", "stable", "Hot season; concentrated Castelao and richly sweet Moscatel fortified wines")
VIN(r4, 2019, "excellent", "stable", "Benchmark vintage; complex, age-worthy Palmela reds and exceptional Moscatel")

p7 = P("Jose Maria da Fonseca", "Portugal", r4, "winery",
        "Portugal's oldest and most internationally celebrated family wine company, founded in 1834. Fonseca's Periquita, Primum, and Moscatel de Setubal wines have represented Portuguese viticulture to the world for nearly two centuries, with the Moscatel de Setubal aged expressions regarded as world-class fortified wines.")
prod7, new7 = PROD("Jose Maria da Fonseca Periquita Original Palmela DOC", "wine_still", p7, r4, "Portugal",
    subcategory="Castelao",
    description="Portugal's most historically significant red wine label; Castelao (Periquita) from Palmela's sandy soils — cherry, earthy herbs, leather, and a medium-bodied freshness that made it Portugal's first internationally exported red wine",
    price_tier="entry")
if new7:
    PAIR(prod7, "Grilled sardines with sea salt and lemon", "complement", "classic", "main", "Portugal's most beloved food pairing: fresh grilled sardines with the country's most historically iconic red wine from just across the Tagus")
    PAIR(prod7, "Arroz de linguiça (Portuguese sausage rice)", "complement", "classic", "main", "Light, earthy Castelao and the smoky richness of linguiça sausage rice is a classic Setubal Peninsula table combination")
    PAIR(prod7, "Bacalhau a bras (salt cod with eggs and olives)", "complement", "established", "main", "The wine's earthy, medium-bodied character pairs naturally with Portugal's most beloved salt cod preparation")
    PAIR(prod7, "Caldo verde with Alentejano chourico", "complement", "established", "starter", "Fruity, light Castelao alongside Portugal's national soup with smoky chourico — a deeply Portuguese pairing")

p8 = P("Bacalhoa Wines of Portugal", "Portugal", r4, "winery",
        "A major Setubal Peninsula producer operating from the historic Azeitao estate, Bacalhoa is best known internationally for the JP Azeitao and Moscatel de Setubal wines. Their Moscatel de Setubal is one of the world's most complex and compelling fortified Muscat wines, rivalling Samos and Rutherglen at their best.")
prod8, new8 = PROD("Bacalhoa Moscatel de Setubal DOC", "wine_fortified", p8, r4, "Portugal",
    subcategory="Moscatel Graudo",
    description="Classic Moscatel de Setubal fortified wine; amber-golden with intense orange blossom, dried apricot, honey, and a distinctive pithy citrus complexity that sets it apart from all other world Muscats",
    price_tier="mid_range")
if new8:
    PAIR(prod8, "Pasteis de nata with cinnamon sugar", "complement", "classic", "dessert", "The Setubal Peninsula's most beloved fortified wine and Lisbon's most famous pastry: orange blossom and honey Moscatel with warm egg custard tart")
    PAIR(prod8, "Fresh melon with Alentejano pata negra ham", "complement", "classic", "starter", "Sweet Moscatel and Portuguese cured ham with melon — a Mediterranean summer opener of great elegance")
    PAIR(prod8, "Aged Azeitao cheese with fig and quince paste", "bridge", "established", "cheese", "The wine's orange blossom and honey bridges with the mild, buttery Azeitao sheep's cheese and sweet preserves")
    PAIR(prod8, "Arroz doce (Portuguese rice pudding with cinnamon)", "complement", "classic", "dessert", "Floral, orange-scented Moscatel and Portugal's most beloved rice pudding dessert are a natural national combination")

# ── 5. TIKVES (North Macedonia) ──────────────────────────────────────────────
print("\n=== Tikves (North Macedonia) ===")
r5 = R("Tikves", "North Macedonia", "wine",
       designation_type="PDO",
       designation_name="PDO Tikves",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="The most important wine-producing region of North Macedonia and one of the Balkans' most historically significant wine zones. Tikves produces wines from both indigenous varieties (Vranec, Temjanika) and international grapes from its warm, sub-continental climate with exceptional sunshine hours. The Tikves winery is one of the largest in the former Yugoslavia and has been producing wines since 1885. The indigenous Vranec grape is the region's most distinctive asset.",
       key_producers="Tikves Winery, Bovin, Popova Kula, Skovin, Stobi Winery",
       historical_context="The Vardar Valley has been producing wine since antiquity; Macedonian wine was traded throughout the ancient Mediterranean. The Tikves wine-producing zone became significant during the Yugoslav era when Tikves Winery was established as one of the largest in the region. Post-independence (1991), privatisation and quality investment have gradually elevated North Macedonian wine's international profile, with Vranec emerging as the most globally recognised indigenous Balkan variety.")

VIN(r5, 2023, "very_good", "rising", "Warm Vardar Valley season; excellent Vranec concentration and color")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage; finest Tikves Vranec in recent memory with exceptional structure")
VIN(r5, 2021, "good", "stable", "Reliable vintage; approachable, fruit-forward style across both indigenous and international varieties")
VIN(r5, 2020, "very_good", "rising", "Hot, dry growing season; powerful, tannic Vranec reds with long aging potential")
VIN(r5, 2019, "very_good", "stable", "Good vintage with improving quality; Tikves Winery's investment in cellar technology becoming evident")

p9 = P("Tikves Winery", "North Macedonia", r5, "winery",
        "The largest and most historically significant wine producer in North Macedonia, established in 1885 and producing wine continuously since. Tikves Winery's premium Barovo and Special Selection labels have introduced Vranec to international markets, demonstrating the grape's potential for serious, age-worthy red wine production.")
prod9, new9 = PROD("Tikves Special Selection Vranec Tikves PDO", "wine_still", p9, r5, "North Macedonia",
    subcategory="Vranec",
    description="Premium North Macedonian Vranec from the Vardar Valley; deep, inky, and powerful with blackberry jam, dark chocolate, dried herbs, and firm tannic structure — the Balkans' most internationally recognised indigenous red grape",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "Slow-cooked lamb tavche gravche (Macedonian bean pot with lamb)", "complement", "classic", "main", "The region's defining dish and wine: powerful Vranec with the smoky, herb-scented Macedonian lamb and white bean pot")
    PAIR(prod9, "Grilled cevapcici with kajmak and ajvar", "complement", "classic", "main", "Bold, tannic Vranec stands up to the intensely spiced grilled meat with creamy kajmak and roasted pepper relish")
    PAIR(prod9, "Stuffed bell peppers with rice and minced pork (punjene paprike)", "complement", "established", "main", "The wine's dark fruit and herb character resonates with the warm spice and richness of Macedonian stuffed peppers")
    PAIR(prod9, "Aged Macedonian kashkaval cheese with olives", "bridge", "established", "cheese", "Tannic, dark-fruited Vranec bridges with sharp, salty aged sheep's cheese — a deeply Balkan table combination")

p10 = P("Bovin Winery", "North Macedonia", r5, "winery",
         "A boutique Tikves estate producing some of North Macedonia's most ambitious and quality-focused wines, including an internationally recognised Vranec Reserve and a varietal Temjanika (the Macedonian equivalent of Gewurztraminer). Bovin's limited production wines have been praised by international critics and represent the region's quality ceiling.")
prod10, new10 = PROD("Bovin Temjanika Tikves PDO", "wine_still", p10, r5, "North Macedonia",
    subcategory="Temjanika",
    description="Macedonian indigenous aromatic white from Temjanika (Tamyanka/Taminjarika); intensely floral with rose petal, lychee, and exotic spice — the Balkans' most distinctive aromatic white wine",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Tarator (Bulgarian-style chilled yoghurt and cucumber soup)", "complement", "established", "starter", "The wine's exotic floral aromatics are freshened and echoed by the cool yoghurt and fresh dill of the chilled Balkan soup")
    PAIR(prod10, "Grilled fresh trout with garlic and lemon", "complement", "established", "main", "Aromatic, floral Temjanika with its Muscat-Gewurztraminer character pairs naturally with fresh mountain trout")
    PAIR(prod10, "Shopska salad with tomato, cucumber, and fresh sirene", "complement", "classic", "starter", "The wine's rose and lychee lift bridges with the freshness of tomato and the saltiness of Bulgarian-style white cheese")
    PAIR(prod10, "Baklava with walnut and honey syrup", "complement", "suggested", "dessert", "Aromatic, semi-dry Temjanika's floral sweetness complements the walnut and honey layers of Balkan baklava")

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
