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

# ── Region 1: Gaillac ────────────────────────────────────────────────────────
print("=== Region 1: Gaillac ===")
r = R("Gaillac", "France", "wine",
      designation_type="AOC", designation_name="Gaillac AOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Ancient Southwest French appellation near Albi; indigenous varieties Mauzac, Len de l'El, Duras and Braucol; predates Bordeaux as a wine region; sparkling, sweet and dry styles.",
      key_producers="Domaine Plageoles, Château Lastours, Causse Marines",
      historical_context="Gaillac claims to be France's oldest wine region; Roman amphora found here; Mauzac was the original base of Blanquette de Limoux.")
VIN(r, 2022, "very_good", "stable", "Good ripeness year; Mauzac showed lovely floral character and fresh acidity.")
VIN(r, 2021, "excellent", "stable", "Cool year favoured indigenous whites; Len de l'El of notable freshness.")
VIN(r, 2020, "very_good", "stable", "Warm year; structured reds from Duras and Braucol; rich sweet Mauzac.")
VIN(r, 2019, "excellent", "rising", "Outstanding for both reds and whites; complex, characterful indigenous varieties.")
VIN(r, 2018, "very_good", "stable", "Classic Gaillac year; approachable, food-friendly across all styles.")
p1 = P("Domaine Plageoles", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Robert and Bernard Plageoles are the guardians of Gaillac's indigenous varieties; Mauzac Nature pétillant ancestral; Ondenc and Muscadelle rarities; no additions or fining.",
       reputation_narrative="France's most important indigenous-variety conservator; Plageoles' ancestral pétillant Mauzac Nature is a cult wine among natural wine lovers.",
       price_positioning="mid_range")
p2 = P("Causse Marines", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Patrice Lescarret's biodynamic estate; indigenous Gaillac varieties; funky, complex natural wines including Peyrouzelles (Len de l'El) and Rasdu (Duras).",
       reputation_narrative="Causse Marines put Gaillac back on the natural wine map; cult following among Parisian natural wine bars.",
       price_positioning="mid_range")
pr1, n1 = PROD("Plageoles Mauzac Nature Pétillant Ancestral", "wine_sparkling", p1, r, "France",
               subcategory="Mauzac", price_tier="mid_range",
               description="Ancestral method pétillant from indigenous Mauzac; quince, green apple, chamomile and a gentle mousse; bone-dry with characteristic bitter-almond finish.")
if n1:
    PAIR(pr1, "Rillettes de canard with cornichons", "complement", "classic", "aperitif", "Ancestral fizz cuts duck fat; bitter almond bridges pork and quince notes.")
    PAIR(pr1, "Cassoulet de Castelnaudary (white bean and duck)", "contrast", "established", "main", "Petillant freshness contrasts heavy cassoulet; bubbles cut rich confit fat.")
    PAIR(pr1, "Roquefort with honey on walnut bread", "complement", "adventurous", "cheese", "Bitter almond and quince echo Roquefort's pungency; honey mediates saltiness.")
    PAIR(pr1, "Tarte Tatin with crème fraîche", "complement", "suggested", "dessert", "Green apple and quince in wine echo caramelised apple tart; bitter almond bridges pastry.")
pr2, n2 = PROD("Causse Marines Peyrouzelles Len de l'El", "wine_still", p2, r, "France",
               subcategory="Len de l'El", price_tier="mid_range",
               description="Natural Len de l'El from Gaillac limestone; orange blossom, Granny Smith, herbal notes and textured natural energy; low sulphur, minimal intervention.")
if n2:
    PAIR(pr2, "Confit de canard with sarladaise potatoes", "complement", "classic", "main", "Southwest classic; wine's texture and freshness contrast rich duck confit and potato.")
    PAIR(pr2, "Tomme des Pyrénées with walnuts", "complement", "established", "cheese", "Regional pairing; herbal wine notes echo mountain cheese; walnut bridges bitterness.")
    PAIR(pr2, "Tuna tartare with preserved lemon and capers", "complement", "suggested", "starter", "Orange blossom and herb notes complement tuna; preserved lemon echoes wine's citrus.")
    PAIR(pr2, "Grilled pork tenderloin with apple and thyme", "complement", "suggested", "main", "Apple-herbal register echoes wine; acidity cuts pork fat; thyme bridges herb notes.")

# ── Region 2: Costières de Nîmes ─────────────────────────────────────────────
print("=== Region 2: Costières de Nîmes ===")
r = R("Costières de Nîmes", "France", "wine",
      designation_type="AOC", designation_name="Costières de Nîmes AOC",
      reputation_tier="overlooked", quality_trajectory="ascending",
      description="Southern Rhône gateway appellation between Montpellier and Arles; galets roulés soils similar to Châteauneuf; Grenache, Syrah and Mourvèdre produce excellent value southern reds and rosés.",
      key_producers="Château Mourgues du Grès, Château de la Tuilerie, Domaine de l'Amarine",
      historical_context="Often dismissed as Languedoc but sits within the Rhône system; galets roulés soils bring it closer to Châteauneuf-du-Pape in terroir than geography suggests.")
VIN(r, 2022, "excellent", "stable", "Good balance in warm year; Grenache-led reds of great freshness.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, aromatic rosé and fresh reds.")
VIN(r, 2020, "excellent", "stable", "Outstanding year; concentrated, garrigue-rich reds of great depth.")
VIN(r, 2019, "very_good", "stable", "Warm and generous; plush, fruit-forward Grenache blends.")
VIN(r, 2018, "very_good", "stable", "Classic southern style; approachable, food-friendly reds.")
p1 = P("Château Mourgues du Grès", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="François Collard's benchmark estate on galets roulés; organic certified; Grenache-Syrah Terres d'Argence is their prestige red; excellent value rosé.",
       reputation_narrative="The most acclaimed estate in Costières de Nîmes; demonstrates the appellation's potential for serious, affordable southern Rhône-style wines.",
       price_positioning="value")
p2 = P("Château de la Tuilerie", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Chantal Count's organic estate; galets roulés on clay-limestone; Grenache Blanc and Viognier whites alongside classic Grenache-Syrah reds.",
       reputation_narrative="One of the appellation's most consistent producers; whites of surprising elegance and accessible, food-friendly reds.",
       price_positioning="value")
pr1, n1 = PROD("Château Mourgues du Grès Terres d'Argence Rouge", "wine_still", p1, r, "France",
               subcategory="Grenache blend", price_tier="value",
               description="Prestige red from galets roulés; Grenache, Syrah and Mourvèdre; dark fruit, garrigue, lavender and white pepper; remarkable Châteauneuf-like quality at a fraction of the price.")
if n1:
    PAIR(pr1, "Grilled lamb merguez with flatbread and harissa", "complement", "classic", "main", "Southern Rhône-style with Mediterranean food; garrigue and lamb spice in harmony.")
    PAIR(pr1, "Provençal ratatouille with herbes de Provence", "complement", "established", "main", "Regional pairing; garrigue mirrors herb garden flavours; dark fruit bridges tomato acidity.")
    PAIR(pr1, "Grilled duck magret with cherry reduction", "complement", "suggested", "main", "Dark fruit echoes cherry reduction; Grenache warmth mirrors duck fat.")
    PAIR(pr1, "Aged Comté with Dijon mustard", "bridge", "suggested", "cheese", "Garrigue notes and dark fruit bridge aged cheese; mustard amplifies savoury register.")
pr2, n2 = PROD("Château de la Tuilerie Costières de Nîmes Blanc", "wine_still", p2, r, "France",
               subcategory="Grenache Blanc blend", price_tier="value",
               description="Organic Grenache Blanc and Viognier blend; white peach, apricot, almond and a soft, rounded southern freshness; excellent value Mediterranean white.")
if n2:
    PAIR(pr2, "Bouillabaisse with rouille and croûtons", "complement", "classic", "main", "Southern French pairing; Viognier apricot bridges saffron-spiced fish; richness balanced by acidity.")
    PAIR(pr2, "Grilled sea bass with fennel and Pernod", "complement", "established", "fish_course", "Stone fruit and almond echo fennel's anise character; Grenache Blanc bridges.")
    PAIR(pr2, "Tapenade and anchoiade with crudités", "complement", "classic", "aperitif", "Provençal aperitif pairing; wine's soft southern character suits anchovy and olive.")
    PAIR(pr2, "Goat's cheese salad with herbs and honey", "complement", "suggested", "starter", "Stone fruit softens goat's cheese tang; almond note bridges; honey mirrors wine's warmth.")

# ── Region 3: Roussette de Savoie ────────────────────────────────────────────
print("=== Region 3: Roussette de Savoie ===")
r = R("Roussette de Savoie", "France", "wine",
      designation_type="AOC", designation_name="Roussette de Savoie AOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Alpine Savoie appellation for the Altesse grape (Roussette); high-altitude limestone vineyards produce wines of remarkable mineral tension, herbal freshness and longevity.",
      key_producers="Domaine Dupasquier, Domaine Belluard, André et Michel Quénard",
      historical_context="Altesse (Roussette) is thought to have originated in Cyprus; it thrives on Savoie's limestone and clay soils; Frangy is the most respected cru.")
VIN(r, 2022, "very_good", "stable", "Good mountain year; Altesse showed herbal freshness and mineral precision.")
VIN(r, 2021, "excellent", "stable", "Cool alpine year; textbook mineral Altesse with fine acidity and herb notes.")
VIN(r, 2020, "excellent", "stable", "Warm year retained freshness; concentrated, textured Roussette.")
VIN(r, 2019, "very_good", "stable", "Good balance; approachable Altesse with characteristic violet and herbal notes.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; generous Roussette with excellent food versatility.")
p1 = P("Domaine Dupasquier", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Multi-generational Savoie estate; Roussette de Savoie Marestel cru from steep limestone slopes; traditional vinification; benchmark for Alpine Altesse.",
       reputation_narrative="Dupasquier's Marestel Roussette is the gold standard for the appellation; age-worthy, complex and distinctly alpine.",
       price_positioning="mid_range")
p2 = P("Domaine Belluard", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Dominique Belluard's biodynamic estate; Gringet (rare Savoie variety) alongside Altesse; Mont Blanc pétillant ancestral; zero sulphur approach.",
       reputation_narrative="One of France's most exciting natural producers; Belluard's rare Gringet and Altesse have cult status among natural wine circles.",
       price_positioning="mid_range")
pr1, n1 = PROD("Dupasquier Roussette de Savoie Marestel", "wine_still", p1, r, "France",
               subcategory="Altesse", price_tier="mid_range",
               description="Cru Marestel Altesse; hawthorn, violet, green almond, chalk and a long herbal-mineral finish; austere in youth, complex with age.")
if n1:
    PAIR(pr1, "Fondue Savoyarde with Gruyère and Comté", "complement", "classic", "main", "Alpine regional pairing; mineral Altesse cuts fondue richness; herbal notes echo cheese.")
    PAIR(pr1, "Freshwater perch meunière with capers", "complement", "classic", "fish_course", "Alpine lake tradition; mineral-herbal wine mirrors delicate freshwater perch.")
    PAIR(pr1, "Tartare de féra (lake fish) with herbs", "complement", "established", "starter", "Alpine pairing; mineral wine amplifies delicate lake fish; herbs bridge green notes.")
    PAIR(pr1, "Reblochon raclette with potatoes and charcuterie", "complement", "established", "main", "Savoie classic; mineral acidity cuts washed-rind cheese richness; herbal notes bridge.")
pr2, n2 = PROD("Belluard Mont Blanc Gringet Pétillant Ancestral", "wine_sparkling", p2, r, "France",
               subcategory="Gringet", price_tier="mid_range",
               description="Rare ancestral pétillant from ancient Gringet variety; apple, almond, wild herbs and a persistent fine mousse; bone-dry with distinctive alpine character.")
if n2:
    PAIR(pr2, "Cured Alpine charcuterie board", "complement", "classic", "aperitif", "Mountain pairing; dry fizz cuts cured fat; herbal notes echo alpine herbs in charcuterie.")
    PAIR(pr2, "Smoked trout rillettes with crème fraîche", "complement", "established", "starter", "Almond and apple notes bridge smoked trout; bubbles cut rich rillette texture.")
    PAIR(pr2, "Ravioles du Royans (small cheese ravioli)", "complement", "suggested", "starter", "Savoie regional match; fine bubbles lift delicate cheese pasta; acidity refreshes.")
    PAIR(pr2, "Wild herb frittata with mountain cheese", "complement", "suggested", "starter", "Herbal register echoes wild herbs; Gringet's alpine character bridges mountain cheese.")

# ── Region 4: Corbières ──────────────────────────────────────────────────────
print("=== Region 4: Corbières ===")
r = R("Corbières", "France", "wine",
      designation_type="AOC", designation_name="Corbières AOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Rugged limestone and schist garrigue country south of Carcassonne; Carignan, Grenache, Syrah and Mourvèdre produce intense, herb-scented reds of excellent value.",
      key_producers="Château Boutenac, Domaine des Perrières, Château Vieux Moulin",
      historical_context="One of southern France's oldest wine zones; schist and limestone terroir produces wines of surprising depth; Boutenac is the lone cru within the appellation.")
VIN(r, 2022, "excellent", "stable", "Warm Mediterranean year; concentrated Carignan and Grenache of great depth.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, aromatic reds with fresh garrigue character.")
VIN(r, 2020, "exceptional", "rising", "Outstanding year; old-vine Carignan of extraordinary intensity and terroir expression.")
VIN(r, 2019, "excellent", "stable", "Warm, generous vintage; plush, fruit-rich reds with herbal backbone.")
VIN(r, 2018, "very_good", "stable", "Good balance; food-friendly reds with characteristic Corbières garrigue.")
p1 = P("Château Boutenac", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Leading estate of the Boutenac cru; old-vine Carignan and Grenache on limestone; Cuvée Ceps d'Antan from 100-year-old Carignan is their iconic wine.",
       reputation_narrative="Château Boutenac proved that old-vine Carignan from Corbières can rival the southern Rhône's finest; Ceps d'Antan is a benchmark.",
       price_positioning="mid_range")
p2 = P("Domaine des Perrières", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Small natural producer on schist and limestone; Carignan and Grenache vinified with minimal intervention; indigenous yeasts; zero added sulphur on some cuvées.",
       reputation_narrative="One of Corbières' rising natural wine stars; demonstrating the appellation's overlooked potential for complex, terroir-driven reds.",
       price_positioning="value")
pr1, n1 = PROD("Château Boutenac Corbières Ceps d'Antan", "wine_still", p1, r, "France",
               subcategory="Carignan", price_tier="mid_range",
               description="100-year-old Carignan from Boutenac cru; dark fruit, iron, garrigue, dried lavender and extraordinary mineral depth; proves old Carignan is one of France's great vines.")
if n1:
    PAIR(pr1, "Slow-braised oxtail with olives and orange peel", "complement", "classic", "main", "Old-vine Carignan's iron and dark fruit mirror braised oxtail; orange peel echoes wine's brightness.")
    PAIR(pr1, "Lamb shoulder with preserved lemon tagine", "complement", "established", "main", "Garrigue and dark fruit bridge Moroccan spice and lamb richness.")
    PAIR(pr1, "Wild boar sausage with lentils du Puy", "complement", "established", "main", "Iron-mineral Carignan aligns with boar's earthiness; lentils bridge mineral character.")
    PAIR(pr1, "Aged Manchego with membrillo and walnuts", "complement", "suggested", "cheese", "Dark fruit and iron echo aged Manchego; membrillo bridges; walnuts add bitter depth.")
pr2, n2 = PROD("Domaine des Perrières Corbières Rouge", "wine_still", p2, r, "France",
               subcategory="Grenache Carignan blend", price_tier="value",
               description="Natural Grenache-Carignan blend; garnet colour, wild berries, rosemary, thyme and a fresh, garrigue-driven finish; minimal sulphur, zero fining.")
if n2:
    PAIR(pr2, "Grilled lamb chops with herbes de Provence", "complement", "classic", "main", "Garrigue in wine mirrors Provençal herbs; natural freshness suits simple grilled lamb.")
    PAIR(pr2, "Tomato and eggplant gratin with Parmesan", "complement", "established", "main", "Rosemary and thyme bridge herb-tomato gratin; Grenache fruit amplifies tomato sweetness.")
    PAIR(pr2, "Charcuterie platter with tapenade", "complement", "classic", "aperitif", "Southern French aperitif pairing; wild berry and garrigue suit cured meats and olive.")
    PAIR(pr2, "Grilled merguez with couscous and harissa", "complement", "suggested", "main", "Garrigue and fruit bridge North African spice; natural freshness refreshes heat.")

# ── Region 5: Penedès Whites ─────────────────────────────────────────────────
print("=== Region 5: Penedès Alt Penedès ===")
r = R("Alt Penedès", "Spain", "wine",
      designation_type="DO", designation_name="Alt Penedès DO",
      reputation_tier="respected", quality_trajectory="ascending",
      description="High-altitude sub-zone of Penedès southwest of Barcelona; limestone plateaus at 400-800m; cooler temperatures preserve freshness in Xarel·lo, Macabeu and Parellada whites.",
      key_producers="Gramona, Recaredo, Can Ràfols dels Caus",
      historical_context="The high-altitude vineyards were planted to escape phylloxera on poor limestone soils; now produce Penedès's most complex and age-worthy still whites.")
VIN(r, 2022, "excellent", "rising", "Cool high-altitude year; Xarel·lo of remarkable mineral precision and freshness.")
VIN(r, 2021, "very_good", "stable", "Good balance; aromatic whites with characteristic Penedès herbal energy.")
VIN(r, 2020, "excellent", "stable", "Concentrated vintage; Xarel·lo showed impressive complexity and aging potential.")
VIN(r, 2019, "exceptional", "rising", "Outstanding year; benchmark for high-altitude Xarel·lo and white blends.")
VIN(r, 2018, "very_good", "stable", "Warm but high altitude preserved freshness; versatile, food-friendly whites.")
p1 = P("Gramona", "winery", r, "Spain",
       production_philosophy="traditional",
       philosophy_description="Premier Cava and still wine estate; Xarel·lo from old limestone vineyards; III Lustros (Cava) aged 5+ years; barrel-fermented Xarel·lo demonstrates grape's complexity.",
       reputation_narrative="Gramona is the reference house for aged Cava and complex Xarel·lo; among Spain's most serious sparkling wine producers.",
       price_positioning="premium")
p2 = P("Can Ràfols dels Caus", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Pioneer of prestige still wines from Penedès; Gran Caus is their flagship red; Vinya Punta de Flecha Xarel·lo from high limestone proves the variety's serious potential.",
       reputation_narrative="Can Ràfols dels Caus revolutionised Penedès still wines; their high-altitude single-vineyard Xarel·lo is among Spain's most complex whites.",
       price_positioning="mid_range")
pr1, n1 = PROD("Gramona Xarel·lo Font Jui", "wine_still", p1, r, "Spain",
               subcategory="Xarel·lo", price_tier="premium",
               description="Old-vine, barrel-fermented Xarel·lo from high limestone; beeswax, fennel, toasted almond, white peach and a saline mineral persistence; demonstrates the variety's serious potential.")
if n1:
    PAIR(pr1, "Grilled lobster with garlic alioli", "complement", "established", "fish_course", "Old-vine Xarel·lo's richness matches lobster; garlic alioli echoes wine's savoury depth.")
    PAIR(pr1, "Grilled razor clams with herb oil", "complement", "classic", "starter", "Saline mineral wine echoes razor clam brine; beeswax bridges herb oil richness.")
    PAIR(pr1, "Chicken escabeche with saffron and almonds", "complement", "established", "main", "Almond and toasted note in wine echo almonds; saffron bridges wine's warm spice.")
    PAIR(pr1, "Aged Manchego with quince and toasted pine nuts", "complement", "suggested", "cheese", "Toasted almond and beeswax echo aged Manchego; quince bridges stone fruit notes.")
pr2, n2 = PROD("Can Ràfols dels Caus Xarel·lo Punta de Flecha", "wine_still", p2, r, "Spain",
               subcategory="Xarel·lo", price_tier="mid_range",
               description="Single-vineyard high-altitude Xarel·lo on limestone; herbal, mineral and complex — fennel, green apple, chalk and a long savoury finish of Mediterranean character.")
if n2:
    PAIR(pr2, "Catalan escalivada with anchovies", "complement", "classic", "starter", "Regional Catalan pairing; mineral-herb wine echoes roasted pepper and anchovy salinity.")
    PAIR(pr2, "Fideuà (Catalan seafood noodles) with alioli", "complement", "classic", "main", "Saline mineral wine echoes seafood base; fennel note bridges herb notes in aioli.")
    PAIR(pr2, "Grilled squid with lemon and parsley", "complement", "established", "starter", "Mineral freshness amplifies squid's sea character; herb note mirrors parsley.")
    PAIR(pr2, "Mushroom pa amb tomàquet (tomato bread)", "complement", "established", "starter", "Catalan classic; wine's savoury-mineral register bridges tomato acidity and mushroom.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("Done.")
conn.close()
