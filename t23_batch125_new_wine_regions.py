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

# ── B125 ─────────────────────────────────────────────────────────────────────
# Targets: Cornas AOC (France), Saint-Péray AOC (France),
#          Gaillac AOC (France), Irouléguy AOC (France), Jurançon AOC (France)

# 1. CORNAS AOC — France
print("=== Cornas AOC ===")
r1 = R("Cornas AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Cornas AOC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The smallest and most powerful Northern Rhône appellation, south of Saint-Joseph, exclusively Syrah on granite and clay-limestone terraces. Cornas wines are the most structured and tannic of the Northern Rhône — dark, muscular and demanding extended ageing. The name means 'burnt earth' in the local dialect, reflecting the heat-collecting terraces. Les Vieilles Vignes from Auguste Clape and Reynard from Thierry Allemand are global reference points.",
        key_producers="Auguste Clape, Thierry Allemand, Domaine du Tunnel, Vincent Paris, Franck Balthazar",
        historical_context="Cornas is one of France's oldest documented wine regions, mentioned in Charlemagne's time. The AOC was established in 1938. Cornas was long dismissed as rough country wine until the Clape family and later Thierry Allemand demonstrated its extraordinary terroir potential from the 1980s onwards.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"exceptional","rising"),(2022,"excellent","rising")]:
    VIN(r1, yr, qd, pt, f"Cornas {yr}: compact granite terraces; powerful Syrah of extraordinary concentration and ageing potential")

p1a = P("Auguste Clape", "winery", r1, "France",
        production_philosophy="traditional",
        philosophy_description="The reference Cornas producer; old-vine Syrah from the Les Mazards and other prime terraces; traditional extended maceration.",
        reputation_narrative="Pierre-Marie Clape and before him Auguste Clape defined Cornas to the world; their Cornas is considered France's most authentic expression of concentrated Syrah.",
        price_positioning="ultra_premium")
pr1a1, n = PROD("Clape Cornas", "wine_still", p1a, r1, "France",
                subcategory="Syrah", price_tier="ultra_premium",
                description="The reference Cornas; old-vine Syrah with extraordinary depth — blackberry, iron, smoked meat and granite mineral; 15-25 year ageing potential.")
if n:
    PAIR(pr1a1, "Roasted leg of wild boar with root vegetables", "complement", "classic", "main", "Cornas Syrah's power and structure is the natural partner for wild game")
    PAIR(pr1a1, "Beef daube Provençale with olives and orange", "complement", "classic", "main", "The great Southern French tradition: Syrah with daube of beef")
    PAIR(pr1a1, "Grilled côte de boeuf (bone-in rib steak)", "complement", "classic", "main", "Cornas's iron-mineral power demands the richest beef cuts")
    PAIR(pr1a1, "Aged Comté 24 months with walnuts", "complement", "established", "cheese", "Iron-mineral Syrah and aged nutty Comté; the great Jura-Rhône cheese combination")

pr1a2, n = PROD("Clape Renaissance Cornas", "wine_still", p1a, r1, "France",
                subcategory="Syrah", price_tier="premium",
                description="Second label Cornas; approachable earlier with similar dark fruit and mineral profile but softer tannins.")
if n:
    PAIR(pr1a2, "Roast duck with olive tapenade", "complement", "established", "main", "Dark Syrah with duck and olive is a great Northern Rhône combination")
    PAIR(pr1a2, "Lamb tagine with preserved lemon", "complement", "established", "main", "Powerful Syrah holds up beautifully to aromatic slow-braised lamb")
    PAIR(pr1a2, "Grilled lamb merguez sausages", "complement", "classic", "main", "Spiced North African sausage finds its natural companion in robust Cornas")
    PAIR(pr1a2, "Mushroom bourguignon with crusty bread", "complement", "established", "main", "Deep Syrah mineral and fruit complement mushroom richness as a vegetarian main")

p1b = P("Thierry Allemand", "winery", r1, "France",
        production_philosophy="natural",
        philosophy_description="Natural Cornas producer of cult status; Reynard and Chaillot are two of France's most sought-after Syrahs.",
        reputation_narrative="Thierry Allemand's tiny production from old Cornas vines has achieved legendary status; his wines sell on allocation to the world's top restaurants.",
        price_positioning="ultra_premium")
pr1b1, n = PROD("Thierry Allemand Cornas Reynard", "wine_still", p1b, r1, "France",
                subcategory="Syrah", price_tier="ultra_premium",
                description="Reynard from old Syrah vines on granite; ethereal elegance within Cornas's power — violets, iron, wild herbs and staggering mineral depth.")
if n:
    PAIR(pr1b1, "Lièvre à la royale (hare royale)", "complement", "classic", "main", "The ultimate French game dish demands the most profound Syrah in France")
    PAIR(pr1b1, "Roast Bresse chicken with truffle under skin", "complement", "established", "main", "Premium chicken with truffle meets Cornas's mineral and dark fruit complexity")
    PAIR(pr1b1, "Venison saddle with juniper berry jus", "complement", "classic", "main", "Reynard's wild character echoes the juniper and game of venison saddle")
    PAIR(pr1b1, "Aged Époisses cheese", "complement", "established", "cheese", "Powerful washed-rind cheese is the equal of Reynard Cornas in intensity")

pr1b2, n = PROD("Thierry Allemand Cornas Chaillot", "wine_still", p1b, r1, "France",
                subcategory="Syrah", price_tier="ultra_premium",
                description="Chaillot single-vineyard Cornas; younger vines but extraordinary tension — mineral, violet, blackberry and savagely structured.")
if n:
    PAIR(pr1b2, "Grilled calf's liver with caramelised onion", "complement", "established", "main", "Iron-mineral Syrah and liver are a classic French off-cut combination")
    PAIR(pr1b2, "Cassoulet with duck confit and sausage", "complement", "classic", "main", "Robust Southern France cassoulet and powerful Syrah; both products of the Midi")
    PAIR(pr1b2, "Black pudding with apple and potato", "complement", "established", "main", "Powerful iron Syrah mirrors the blood richness of black pudding")
    PAIR(pr1b2, "Aged Cantal or Salers cheese", "complement", "established", "cheese", "Robust French mountain cheese at its finest with Chaillot's structured power")

# 2. SAINT-PÉRAY AOC — France
print("=== Saint-Péray AOC ===")
r2 = R("Saint-Péray AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Saint-Péray AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The southernmost Northern Rhône appellation, south of Cornas, producing exclusively white wines from Marsanne (and occasionally Roussanne). Still and traditional-method sparkling versions produced. The region's granite soils produce Marsanne of striking mineral weight and aromatic complexity — almond, white flowers, quince and beeswax. The sparkling Saint-Péray Mousseux was historically France's most fashionable sparkling wine after Champagne.",
        key_producers="Domaine du Tunnel, Cuilleron, Jean-Luc Colombo, Voge",
        historical_context="Saint-Péray's sparkling wine was famous across 19th-century Europe, enjoyed by Napoleon and his court. The style fell from fashion after Champagne's dominance was established. The still version has seen a quality renaissance as producers showcase Marsanne's complexity from granite terraces.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r2, yr, qd, pt, f"Saint-Péray {yr}: granite-soil Marsanne; white wine of remarkable weight and aromatic complexity")

p2a = P("Domaine du Tunnel", "winery", r2, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Stéphane Robert's estate; benchmark still and sparkling Saint-Péray from granite terraces; also excellent Cornas.",
        reputation_narrative="Stéphane Robert is the leading voice for Saint-Péray quality; his Marsanne Vieilles Vignes and sparkling Méthode Traditionnelle are the appellation references.",
        price_positioning="premium")
pr2a1, n = PROD("Domaine du Tunnel Saint-Péray Marsanne VV", "wine_still", p2a, r2, "France",
                subcategory="Marsanne", price_tier="premium",
                description="Old-vine Marsanne from granite; rich and waxy with beeswax, quince, almond and exceptional mineral weight from Vieilles Vignes age.")
if n:
    PAIR(pr2a1, "Gratin de macaronis aux truffes", "complement", "classic", "main", "Waxy rich Marsanne and truffle-mac gratin; the great Northern Rhône white pairing")
    PAIR(pr2a1, "Roast chicken with tarragon cream sauce", "complement", "classic", "main", "The Rhône's answer to Burgundy chardonnay and chicken; Marsanne is perfect")
    PAIR(pr2a1, "Baked Camembert with garlic and herbs", "complement", "established", "starter", "Rich Marsanne weight balances and complements warm melted Camembert")
    PAIR(pr2a1, "Crab bisque with tarragon and cream", "complement", "established", "main", "Waxy Marsanne handles the rich crustacean cream with textural balance")

pr2a2, n = PROD("Domaine du Tunnel Saint-Péray Méthode Traditionnelle", "wine_sparkling", p2a, r2, "France",
                subcategory="Marsanne sparkling", price_tier="premium",
                description="Traditional-method Saint-Péray sparkling; Marsanne with fine bubbles, bready complexity and waxy almond fruit — historically famous.")
if n:
    PAIR(pr2a2, "Oysters Charentaise with mignonette", "complement", "established", "starter", "Sparkling Marsanne's yeasty mineral character lifts oysters beautifully")
    PAIR(pr2a2, "Gougères (Gruyère cheese puffs)", "complement", "classic", "amuse", "The classic sparkling wine amuse; Gruyère gougères with any fine sparkling white")
    PAIR(pr2a2, "Langoustines with herb mayonnaise", "complement", "established", "starter", "Sparkling Northern Rhône white mirrors langoustine sweetness with effervescent lift")
    PAIR(pr2a2, "Chicken liver mousse on brioche", "complement", "established", "starter", "Bready sparkling complexity frames liver richness with acidity and bubbles")

p2b = P("Alain Voge", "winery", r2, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Historic Saint-Péray and Cornas estate; Harmonie and Fleur de Crussol are the benchmark Saint-Péray whites.",
        reputation_narrative="Albéric Mazoyer continues Alain Voge's legacy; both Saint-Péray and Cornas from this estate are considered among the Northern Rhône's most reliable references.",
        price_positioning="premium")
pr2b1, n = PROD("Alain Voge Saint-Péray Fleur de Crussol", "wine_still", p2b, r2, "France",
                subcategory="Marsanne", price_tier="premium",
                description="Fleur de Crussol single-vineyard Marsanne; concentrated with white flowers, quince and a firm mineral structure that demands ageing.")
if n:
    PAIR(pr2b1, "Pike quenelles with Nantua sauce (crayfish)", "complement", "classic", "main", "The Lyon classic: Rhône white with pike quenelles in rich crayfish cream sauce")
    PAIR(pr2b1, "Coq au vin blanc with morels", "complement", "established", "main", "Rich Marsanne matches the cream-mushroom of a coq au vin blanc perfectly")
    PAIR(pr2b1, "Foie gras terrine with Sauternes jelly", "complement", "established", "starter", "Weighty Marsanne provides a powerful counterpoint to foie gras richness")
    PAIR(pr2b1, "Aged Beaufort or Abondance cheese", "complement", "established", "cheese", "Alpine cheese's nutty richness pairs naturally with mineral-weight Marsanne")

pr2b2, n = PROD("Alain Voge Saint-Péray Harmonie", "wine_still", p2b, r2, "France",
                subcategory="Marsanne-Roussanne", price_tier="mid_range",
                description="Entry Saint-Péray Harmonie blend; approachable almond, peach and mineral Marsanne-Roussanne — an introduction to the appellation.")
if n:
    PAIR(pr2b2, "Cream of leek and potato soup", "complement", "established", "starter", "Waxy white wine mirrors the cream-and-leek richness of vichyssoise")
    PAIR(pr2b2, "Salmon en papillote with dill", "complement", "established", "main", "Fresh-weighted Marsanne is the ideal companion for delicate steamed salmon")
    PAIR(pr2b2, "Tarte flambée with crème fraîche and lardons", "complement", "established", "main", "Alsatian classic finds a natural pairing in the warm-Rhône Marsanne blend")
    PAIR(pr2b2, "Cauliflower gratin with Gruyère", "complement", "established", "main", "Rounded almond Marsanne and nutty Gruyère gratin; a textural harmony")

# 3. GAILLAC AOC — France
print("=== Gaillac AOC ===")
r3 = R("Gaillac AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Gaillac AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="One of France's oldest wine appellations on the Tarn river in the Midi-Pyrénées, between Toulouse and Albi. Extraordinary variety of indigenous grapes including Mauzac (white), Len de l'El, Ondenc, Duras, Fer Servadou and Prunelart for reds. The region produces still, sparkling (Gaillac Mousseux) and passérillé dessert wines. The diversity of local varieties and the artisan producer movement have made Gaillac one of France's most interesting underdog appellations.",
        key_producers="Domaine Plageoles, Mas d'Aurel, Domaine Rotier, Causse Marines",
        historical_context="Gaillac is documented as a wine region since Roman times and was one of France's most commercially important wines in the Middle Ages. The appellation has 3,000 years of winegrowing history. The rediscovery of indigenous varieties like Ondenc and Mauzac by passionate vignerons has revived interest in this once-overlooked appellation.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r3, yr, qd, pt, f"Gaillac {yr}: Tarn valley harvest; indigenous varieties show remarkable character and freshness")

p3a = P("Domaine Plageoles", "winery", r3, "France",
        production_philosophy="traditional",
        philosophy_description="The guardian of Gaillac's indigenous varieties; Robert and Bernard Plageoles farm Mauzac, Ondenc, Duras and Prunelart.",
        reputation_narrative="Plageoles is synonymous with Gaillac heritage varieties; their Vin de Voile (oxidative Mauzac) and Ondenc are world-class rarities.",
        price_positioning="premium")
pr3a1, n = PROD("Plageoles Mauzac Nature Méthode Gaillacoise", "wine_sparkling", p3a, r3, "France",
                subcategory="Mauzac", price_tier="premium",
                description="Traditional Gaillac méthode ancestrale sparkling Mauzac; gentle persistent bubbles, apple, cidery freshness and beautiful mineral depth.")
if n:
    PAIR(pr3a1, "Roquefort tart with walnut pastry", "complement", "classic", "main", "Gaillac méthode ancestrale is the local tradition with Roquefort from nearby Aveyron")
    PAIR(pr3a1, "Cassoulet de Castelnaudary (with aperitif)", "complement", "established", "aperitif", "Regional sparkling before the cassoulet sets the tone of the Southwest table")
    PAIR(pr3a1, "Foie gras de canard with fig jam", "complement", "classic", "starter", "Gaillac sparkling with foie gras is a great Southwest France combination")
    PAIR(pr3a1, "Apple tarte Tatin", "complement", "established", "dessert", "Apple-cider Mauzac Nature mirrors the caramelised apple of Tarte Tatin")

pr3a2, n = PROD("Plageoles Vin de Voile Mauzac", "wine_still", p3a, r3, "France",
                subcategory="Mauzac", price_tier="premium",
                description="Oxidative Mauzac aged under a yeast veil (like Jura vin jaune); walnut, dried apple and a haunting mineral depth of great complexity.")
if n:
    PAIR(pr3a2, "Comté or aged Tomme de Savoie", "complement", "classic", "cheese", "Oxidative Mauzac and aged mountain cheese; the great Gaillac-meets-Jura pairing")
    PAIR(pr3a2, "Poulet rôti à la broche with garlic", "complement", "established", "main", "Oxidative white wine and roasted chicken is one of France's classic combinations")
    PAIR(pr3a2, "Boeuf en daube with herbes de Provence", "complement", "established", "main", "The weight and complexity of Vin de Voile suits a slow wine-braised beef")
    PAIR(pr3a2, "Grilled langouste with Gaillac reduction", "complement", "established", "main", "Indigenous oxidative white and spiny lobster; a unique Southwest luxury")

p3b = P("Causse Marines", "winery", r3, "France",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Gaillac estate; natural wines from Loin de l'Œil, Mauzac and Fer Servadou; some of France's most individual bottles.",
        reputation_narrative="Patrice Lescarret and Virginie Maignien's estate produces some of Gaillac's most eccentric and authentic wines; Zacmau (Mauzac) is a benchmark.",
        price_positioning="mid_range")
pr3b1, n = PROD("Causse Marines Peyrouzelles Fer Servadou", "wine_still", p3b, r3, "France",
                subcategory="Fer Servadou", price_tier="mid_range",
                description="Old-vine Fer Servadou (Braucol) from Gaillac; dark fruit, violet, iron and a rustic herbaceous charm that demands duck or game.")
if n:
    PAIR(pr3b1, "Confit de canard with sarladaise potatoes", "complement", "classic", "main", "Southwest France at its best: Fer Servadou and duck confit with garlic potatoes")
    PAIR(pr3b1, "Wild boar terrine with cornichons", "complement", "established", "starter", "Rustic iron-fruited Fer Servadou suits the earthy depth of wild boar terrine")
    PAIR(pr3b1, "Pigeon rôti with fig jus", "complement", "established", "main", "Dark fruit and violet of Fer Servadou mirror pigeon's richness with fig sweetness")
    PAIR(pr3b1, "Magret de canard with walnut vinaigrette", "complement", "classic", "main", "The great Southwest combination: duck breast and Fer Servadou from Gaillac")

pr3b2, n = PROD("Causse Marines Zacmau Mauzac", "wine_still", p3b, r3, "France",
                subcategory="Mauzac", price_tier="mid_range",
                description="Still Mauzac; fresh apple, quince and herbal notes with a gentle texture — one of France's most unusual and authentic indigenous whites.")
if n:
    PAIR(pr3b2, "Salade gaillacoise with duck gizzards", "complement", "classic", "starter", "Local classic: Gaillac white with the warm duck gizzard salad of the region")
    PAIR(pr3b2, "Fromage blanc with honey and walnuts", "complement", "established", "dessert", "Apple-quince Mauzac complements the simplicity of honey-drizzled fresh cheese")
    PAIR(pr3b2, "Crêpes with apple compote", "complement", "suggested", "dessert", "Apple-inflected white mirrors the compote filling in Southwest crêpes")
    PAIR(pr3b2, "Truite de rivière with brown butter", "complement", "established", "main", "Fresh Tarn river trout and local white wine is the Gaillac tradition")

# 4. IROULÉGUY AOC — France
print("=== Irouléguy AOC ===")
r4 = R("Irouléguy AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Irouléguy AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="France's smallest and most remote wine appellation, on the steep Atlantic slopes of the Pyrenees in the Basque Country near Saint-Jean-Pied-de-Port. The same grapes as the Spanish Basque txakoli tradition — Tannat and Cabernet Franc (Axeria) for reds, Gros Manseng and Petit Manseng for whites. Extraordinary altitude (up to 400m), Atlantic rainfall and schist soils create wines of intensity and freshness unusual for Southwestern France.",
        key_producers="Domaine Arretxea, Etxegaraya, Domaine Brana, Ilarria",
        historical_context="Irouléguy wine has been produced by Basque monks since the Middle Ages, principally to sustain pilgrims on the Way of Saint James (Camino de Santiago). The appellation is technically in France but cultural identity is purely Basque. Only 220 hectares under vine.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r4, yr, qd, pt, f"Irouléguy {yr}: Atlantic Pyrenean schist harvest; Tannat and Manseng of remarkable freshness")

p4a = P("Domaine Arretxea", "winery", r4, "France",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Irouléguy; Michel and Thérèse Riouspeyrous farm steep schist terraces above 300m; Haitza and Hegoxuri are the references.",
        reputation_narrative="Domaine Arretxea is considered France's greatest Irouléguy producer; their Haitza red and Hegoxuri white are reference points for the appellation.",
        price_positioning="premium")
pr4a1, n = PROD("Arretxea Haitza Irouléguy Rouge", "wine_still", p4a, r4, "France",
                subcategory="Tannat-Cabernet Franc", price_tier="premium",
                description="Haitza red from steep schist terraces; Tannat and Cabernet Franc with dark berry, iron, violets and a distinctive Pyrenean freshness.")
if n:
    PAIR(pr4a1, "Axoa de veau (Basque veal and pepper stew)", "complement", "classic", "main", "Irouléguy red and axoa is the most classic Basque wine-and-dish pairing")
    PAIR(pr4a1, "Grilled Basque-spiced lamb chops", "complement", "classic", "main", "Atlantic Tannat and Pyrenean lamb; the quintessential Basque mountain combination")
    PAIR(pr4a1, "Piperade with Bayonne ham", "complement", "classic", "main", "The Basque classic of pepper-egg dish with ham finds its natural Irouléguy companion")
    PAIR(pr4a1, "Aged Ossau-Iraty sheep's cheese", "complement", "classic", "cheese", "The definitive Basque pairing: Irouléguy red and Ossau-Iraty mountain cheese")

pr4a2, n = PROD("Arretxea Hegoxuri Irouléguy Blanc", "wine_still", p4a, r4, "France",
                subcategory="Petit Manseng-Gros Manseng", price_tier="premium",
                description="Hegoxuri white from schist; Petit and Gros Manseng with tropical citrus, white peach and mineral freshness from Atlantic altitude.")
if n:
    PAIR(pr4a2, "Grilled bar (sea bass) with Basque pepper sauce", "complement", "classic", "main", "Atlantic Pyrenean white with Bay of Biscay sea bass and spiced pepper sauce")
    PAIR(pr4a2, "Ttoro (Basque fish and shellfish stew)", "complement", "classic", "main", "The Basque coastal fish stew meets its natural mountain-white companion")
    PAIR(pr4a2, "Gambas with pil-pil garlic sauce", "complement", "established", "main", "Citrus-mineral Manseng white lifts the garlic-oil richness of pil-pil prawns")
    PAIR(pr4a2, "Cheese soufflé with Ossau-Iraty", "complement", "established", "main", "Manseng's mineral freshness contrasts beautifully with the soufflé's richness")

p4b = P("Domaine Ilarria", "winery", r4, "France",
        production_philosophy="organic",
        philosophy_description="Organic Irouléguy; Peio Espil farms traditional Basque terroir for Tannat-based reds and Manseng whites of freshness and character.",
        reputation_narrative="Ilarria is one of Irouléguy's most dynamic estates; Peio Espil's wines combine traditional Basque character with remarkable freshness from high-altitude schist.",
        price_positioning="mid_range")
pr4b1, n = PROD("Domaine Ilarria Irouléguy Rouge", "wine_still", p4b, r4, "France",
                subcategory="Tannat-Cabernet Franc-Cabernet Sauvignon", price_tier="mid_range",
                description="Organic Irouléguy red; approachable Tannat blend with dark cherry, spice and a firm but accessible tannic backbone.")
if n:
    PAIR(pr4b1, "Poule au pot (boiled chicken with vegetables)", "complement", "established", "main", "The French Basque Sunday tradition: Irouléguy red with the great boiled chicken")
    PAIR(pr4b1, "Lamb merguez with couscous and harissa", "complement", "established", "main", "Tannat's spiced dark fruit complements the spice of merguez and harissa")
    PAIR(pr4b1, "Garbure (Gascon bean and cabbage stew)", "complement", "classic", "main", "The great Basque-Gascon winter stew finds its regional wine companion")
    PAIR(pr4b1, "Pork shoulder braised with peppers", "complement", "established", "main", "Rustic Tannat blend matches the robust character of braised pork and peppers")

pr4b2, n = PROD("Domaine Ilarria Irouléguy Blanc", "wine_still", p4b, r4, "France",
                subcategory="Gros Manseng-Petit Manseng", price_tier="mid_range",
                description="Organic Manseng white from Irouléguy; fresh citrus and passion fruit with refreshing acidity from Atlantic Pyrenean altitude.")
if n:
    PAIR(pr4b2, "Moules marinières with Irouléguy blanc", "complement", "classic", "main", "Classic self-referential pairing: Irouléguy white cooked into its own mussels dish")
    PAIR(pr4b2, "Grilled merlu (hake) with garlic", "complement", "classic", "main", "Basque coast classic: local hake with the mountain white from across the hill")
    PAIR(pr4b2, "Anchois marinés (marinated anchovies) on toast", "complement", "established", "starter", "Citrus-mineral Manseng tames anchovy salt while mirror the acidity")
    PAIR(pr4b2, "Tomato and pepper salad (salade basquaise)", "complement", "classic", "starter", "The Basque summer salad finds its perfect complement in local white wine")

# 5. JURANÇON AOC — France
print("=== Jurançon AOC ===")
r5 = R("Jurançon AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Jurançon AOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="The steep hillside vineyards south of Pau in the Pyrenean foothills, producing distinctive dry (Jurançon Sec) and sweet (Jurançon moelleux) wines from Petit Manseng and Gros Manseng. The sweet Jurançon is made from late-harvest grapes concentrated by the foehn wind (a dry Alpine wind) — achieving tropical fruit sweetness without botrytis. Colette wrote of drinking Jurançon at Henri IV's baptism; Hemingway loved it. Henri Ramonteu at Domaine Cauhapé is the modern master.",
        key_producers="Domaine Cauhapé, Clos Lapeyre, Clos Joliette, Domaine Guirardel",
        historical_context="Jurançon is the royal wine of Béarn — used to anoint the lips of Henri IV (King of Navarre and France) at his baptism in 1553. The moelleux style concentrates Petit Manseng through passerillage (air drying) rather than noble rot, producing wines of exotic tropical sweetness with razor acidity.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","stable"),(2020,"excellent","rising"),(2021,"very_good","stable"),(2022,"excellent","rising")]:
    VIN(r5, yr, qd, pt, f"Jurançon {yr}: Pyrenean foothills harvest; passerillage Petit Manseng with tropical sweetness and high acidity")

p5a = P("Domaine Cauhapé", "winery", r5, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The reference Jurançon producer; Henri Ramonteu's Quintessence and Ballet d'Octobre are the world's finest Petit Manseng sweet wines.",
        reputation_narrative="Henri Ramonteu is the greatest living interpreter of Jurançon; his Quintessence du Petit Manseng is considered one of France's great sweet wines.",
        price_positioning="ultra_premium")
pr5a1, n = PROD("Cauhapé Quintessence du Petit Manseng", "wine_dessert", p5a, r5, "France",
                subcategory="Petit Manseng", price_tier="ultra_premium",
                description="The masterpiece of Jurançon; late-harvest passerillage Petit Manseng — extraordinary concentration of passion fruit, mango and candied citrus with razor acidity.")
if n:
    PAIR(pr5a1, "Foie gras au torchon with quince jelly", "complement", "classic", "starter", "The Béarn tradition: Jurançon sweet wine with local foie gras is a sacred pairing")
    PAIR(pr5a1, "Roquefort with walnut tarte", "contrast", "classic", "cheese", "The great Southwest contrast: Jurançon's tropical sweetness against pungent Roquefort")
    PAIR(pr5a1, "Millefeuille with vanilla pastry cream", "complement", "established", "dessert", "Tropical acidity of Quintessence refreshes and elevates the rich pastry cream")
    PAIR(pr5a1, "Mango and passion fruit tart", "complement", "established", "dessert", "The wine's tropical fruit concentration mirrors and elevates the exotic fruit tart")

pr5a2, n = PROD("Cauhapé Jurançon Sec Chant des Vignes", "wine_still", p5a, r5, "France",
                subcategory="Gros Manseng-Petit Manseng", price_tier="premium",
                description="Dry Jurançon from Cauhapé; Gros Manseng and Petit Manseng dry-fermented with grapefruit, white peach and a distinctive Pyrenean mineral note.")
if n:
    PAIR(pr5a2, "Grilled turbot with beurre blanc", "complement", "classic", "main", "Dry Jurançon and fine Atlantic fish; the most elegant Béarn white wine pairing")
    PAIR(pr5a2, "Scrambled eggs with black truffle", "complement", "established", "main", "Mineral dry Manseng and truffle eggs is a surprising luxury breakfast pairing")
    PAIR(pr5a2, "Fresh goat's cheese with herb oil", "complement", "established", "cheese", "Citrus-mineral dry Jurançon mirrors the fresh acid tang of local chèvre")
    PAIR(pr5a2, "Grilled prawns with Piment d'Espelette", "complement", "classic", "main", "Basque spiced prawns with citrus-mineral dry Jurançon; a natural Pyrenean combination")

p5b = P("Clos Lapeyre", "winery", r5, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Jean-Bernard Larrieu's estate; Jurançon Sec and the legendary late-harvest Vent Balaguer sweet wine from Petit Manseng.",
        reputation_narrative="Clos Lapeyre produces some of Jurançon's most consistent quality across both dry and sweet styles; Vent Balaguer is an exceptional moelleux.",
        price_positioning="premium")
pr5b1, n = PROD("Clos Lapeyre Vent Balaguer Jurançon Moelleux", "wine_dessert", p5b, r5, "France",
                subcategory="Petit Manseng", price_tier="premium",
                description="Vent Balaguer late-harvest Petit Manseng; passion fruit, lychee and apricot concentration balanced by Jurançon's trademark acidity.")
if n:
    PAIR(pr5b1, "Tarte aux abricots (apricot tart)", "complement", "established", "dessert", "Apricot-passion fruit Jurançon mirrors and amplifies the stone fruit of the tart")
    PAIR(pr5b1, "Poached pear with vanilla cream", "complement", "established", "dessert", "Jurançon's tropical acidity brightens the gentle sweetness of poached pear")
    PAIR(pr5b1, "Roquefort and pear salad", "contrast", "classic", "starter", "The great Gascon sweet wine-and-pungent-cheese salad tradition")
    PAIR(pr5b1, "Petit gâteau basque with cherry", "complement", "classic", "dessert", "The Basque almond pastry with cherry jam meets its local Jurançon companion")

pr5b2, n = PROD("Clos Lapeyre Jurançon Sec", "wine_still", p5b, r5, "France",
                subcategory="Gros Manseng", price_tier="mid_range",
                description="Entry dry Jurançon; fresh Gros Manseng with grapefruit, white peach and a dry, mineral finish from Pyrenean schist terraces.")
if n:
    PAIR(pr5b2, "Seared scallops with citrus butter", "complement", "established", "main", "Citrus-mineral dry Manseng lifts scallops with bright acidic precision")
    PAIR(pr5b2, "Grilled sea bream with fennel salad", "complement", "established", "main", "Fresh Pyrenean white is a natural companion for grilled Mediterranean fish")
    PAIR(pr5b2, "Avocado and prawn salad with citrus dressing", "complement", "established", "starter", "Grapefruit-fresh Manseng mirrors and amplifies citrus-dressed prawn avocado")
    PAIR(pr5b2, "Salad nicoise with seared tuna", "complement", "established", "starter", "Citrus mineral Jurançon Sec provides the ideal acidic counterpoint to nicoise")

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
print("B125 complete.")
