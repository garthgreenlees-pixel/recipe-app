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

# ── REGION 1: Gigondas AOC (France/Southern Rhône) ──────────────────────────
print("\n=== Region 1: Gigondas ===")
r1 = R("Gigondas", "France", "wine",
    designation_type="AOC", designation_name="Gigondas AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Gigondas produces some of the Southern Rhône's most serious and age-worthy reds from Grenache, Syrah, and Mourvèdre on the slopes of the Dentelles de Montmirail — a dramatic limestone ridge that gives the wines a mineral tension rarely found in the southern Rhône. The wines are more structured and complex than typical Côtes du Rhône, rivalling Châteauneuf-du-Pape at more accessible prices.",
    key_producers="Domaine du Cayron, Château Raspail-Ay, Domaine Santa Duc, Domaine Les Palières",
    historical_context="Gigondas achieved its own AOC in 1971, breaking away from Côtes du Rhône Villages classification. The village's name derives from the Latin 'jocunditas' (joyfulness). The Dentelles de Montmirail's rugged limestone outcrops create well-drained, mineral-rich soils that give Gigondas its distinctive tension versus the rounder Grenache character of the Rhône plain.")

VIN(r1, 2023, "very_good", "stable", "Excellent Southern Rhône vintage; Grenache achieved fine ripeness with the Dentelles giving characteristic mineral tension")
VIN(r1, 2022, "excellent", "rising", "Outstanding Gigondas year; concentrated and mineral with the limestone terroir giving exceptional structure")
VIN(r1, 2021, "good", "stable", "Cooler year with more elegant, lighter-bodied Grenache; good typicity with fresh fruit and mineral character")
VIN(r1, 2020, "excellent", "rising", "Very hot year producing powerful, concentrated Gigondas; age-worthy and deeply fruited")
VIN(r1, 2019, "very_good", "rising", "Classic Gigondas vintage with excellent Grenache expression and fine mineral depth from the limestone")

prod1a_id = P("Domaine du Cayron", "France", r1, "winery",
    "One of Gigondas's most authentic and consistent estates; the Faraud family has farmed the Dentelles de Montmirail vineyards organically for generations, producing rich, complex Grenache-dominant wines with genuine mineral character.")
prod1a, new1a = PROD("Cayron Gigondas", "wine_still", prod1a_id, r1, "France",
    subcategory="red", price_tier="mid_range",
    description="Domaine du Cayron's classic Gigondas: Grenache-dominant with Syrah and Clairette, from old vines on the limestone Dentelles slopes. Garrigue, black cherry, leather, and mineral depth — one of the appellation's most consistent and authentic expressions.")
if new1a:
    PAIR(prod1a, "Daube d'agneau with black olives, orange peel, and rosemary", "complement", "classic", "main",
        "Provençal lamb daube and Southern Rhône Grenache is the region's great pairing; black olive mirrors the wine's garrigue while slow cooking softens tannins")
    PAIR(prod1a, "Grilled Merguez sausages with harissa and flatbread", "complement", "established", "casual",
        "Spiced North African sausage meets Gigondas's pepper and dark fruit; harissa's heat is tamed by Grenache's ripe fruit sweetness")
    PAIR(prod1a, "Wild boar terrine with cornichons and Dijon mustard", "complement", "established", "starter",
        "Game pâté's iron richness and mustard's sharpness find a natural pairing in Gigondas's structured Grenache")
    PAIR(prod1a, "Aged Picodon with lavender honey and walnut", "bridge", "established", "cheese",
        "Drôme goat cheese with Provençal honey bridges Gigondas's garrigue herbs and dark fruit; walnuts add bitterness to balance")

prod1b_id = P("Domaine Santa Duc", "France", r1, "winery",
    "Yves Gras's ambitious Gigondas estate producing some of the appellation's most concentrated and age-worthy wines from old Grenache vines; Santa Duc's Hautes Garrigues is consistently one of Gigondas's finest single-vineyard bottlings.")
prod1b, new1b = PROD("Santa Duc Gigondas Les Hautes Garrigues", "wine_still", prod1b_id, r1, "France",
    subcategory="red", price_tier="premium",
    description="Santa Duc's flagship single-vineyard Gigondas from Hautes Garrigues: old vine Grenache with concentrated dark fruit, wild thyme, lavender, leather, and exceptional mineral depth from the Dentelles limestone. Requires 8-10 years aging and rewards 20.")
if new1b:
    PAIR(prod1b, "Slow-roasted leg of lamb with herbs de Provence and anchovy studding", "complement", "classic", "main",
        "Anchovy-studded lamb with Provençal herbs amplifies every character in Santa Duc's Gigondas: game, olive, mineral, herb")
    PAIR(prod1b, "Grilled duck breast with Provençal tapenade and roasted peppers", "complement", "classic", "main",
        "Duck's fat and tapenade's olive mirror Gigondas's dark fruit and savoury depth; roasted peppers add sweetness to balance tannin")
    PAIR(prod1b, "Cassoulet with confit duck, Toulouse sausage, and white beans", "complement", "established", "main",
        "Southwest France's great bean and meat dish requires a wine of Gigondas's structure; the old vine Grenache's density matches the dish's weight")
    PAIR(prod1b, "Roquefort with fig jam and toasted hazelnuts", "contrast", "adventurous", "cheese",
        "Intense blue cheese with sweet fig contrasts Gigondas's powerful dark fruit and garrigue; hazelnut adds nuttiness to bridge the gap")

# ── REGION 2: Vacqueyras AOC (France/Southern Rhône) ────────────────────────
print("\n=== Region 2: Vacqueyras ===")
r2 = R("Vacqueyras", "France", "wine",
    designation_type="AOC", designation_name="Vacqueyras AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Vacqueyras is one of the Southern Rhône's most characterful village appellations, elevated from Côtes du Rhône Villages in 1990. Grenache dominates, blended with Syrah and Mourvèdre, producing wines with deep colour, garrigue aromatics, and spiced dark fruit. The wines are more affordable than Gigondas or Châteauneuf-du-Pape while showing genuine terroir character.",
    key_producers="Domaine Le Sang des Cailloux, Domaine la Fourmone, Château des Tours, Tardieu-Laurent",
    historical_context="Vacqueyras sits between Gigondas and Beaumes-de-Venise on the flanks of the Dentelles de Montmirail. The appellation received its own AOC status in 1990 after years as a Côtes du Rhône Villages. The village name possibly derives from 'vallis quercea' (valley of oaks) in Latin, reflecting the garrigue-covered hillsides that define the wines' aromatic character.")

VIN(r2, 2023, "very_good", "stable", "Excellent Southern Rhône growing season; Grenache achieved good ripeness with garrigue expression well defined")
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage; concentrated and complex Vacqueyras with exceptional structure and longevity")
VIN(r2, 2021, "good", "stable", "Elegant year with lighter body and fresh fruit; more approachable style with good typicity")
VIN(r2, 2020, "excellent", "rising", "Hot year with powerful, concentrated wines; deep dark fruit and strong garrigue character")
VIN(r2, 2019, "very_good", "stable", "Classic vintage with excellent balance; garrigue, dark cherry, and spice in fine harmony")

prod2a_id = P("Domaine Le Sang des Cailloux", "France", r2, "winery",
    "Vacqueyras's most celebrated and compelling estate; Serge Férigoule's biodynamic Grenache-dominant wines consistently outperform the appellation's perceived status, achieving Châteauneuf-du-Pape complexity at a fraction of the price.")
prod2a, new2a = PROD("Sang des Cailloux Vacqueyras Floureto", "wine_still", prod2a_id, r2, "France",
    subcategory="red", price_tier="mid_range",
    description="Le Sang des Cailloux's flagship Vacqueyras: old vine Grenache from rocky ('cailloux') limestone soils — a name that translates as 'blood of the stones'. Deep, concentrated dark fruit, garrigue, spice, and mineral depth. Among the Southern Rhône's best over-performing wines.")
if new2a:
    PAIR(prod2a, "Lamb chops grilled over vine cuttings with thyme and sea salt", "complement", "classic", "main",
        "Vine-cutting grilled lamb is the authentic Southern Rhône cooking method — charcoal and lamb fat with thyme mirror Vacqueyras's garrigue perfectly")
    PAIR(prod2a, "Grilled wild mushrooms with garlic, parsley, and Pecorino", "complement", "established", "starter",
        "Mushroom earthiness amplifies Grenache's garrigue depth; Pecorino's salt adds savoury contrast to the wine's ripe fruit")
    PAIR(prod2a, "Ratatouille provençale with sourdough and olive oil", "complement", "classic", "main",
        "Provençal vegetable stew's herb and tomato character mirrors Vacqueyras's garrigue and spice; olive oil ties the Mediterranean palette")
    PAIR(prod2a, "Époisses with black cherry jam and walnut bread", "contrast", "adventurous", "cheese",
        "Pungent washed-rind Époisses contrasts and complements Vacqueyras's dark fruit; cherry jam creates a bridge to the wine's ripe core")

prod2b_id = P("Château des Tours", "France", r2, "winery",
    "Emmanuel Reynaud of Château Rayas fame produces Vacqueyras from his Château des Tours estate; the wines share Rayas's old-vine Grenache purity and clarity, translated into the Vacqueyras context — among the appellation's most elegant expressions.")
prod2b, new2b = PROD("Château des Tours Vacqueyras Rouge", "wine_still", prod2b_id, r2, "France",
    subcategory="red", price_tier="premium",
    description="Emmanuel Reynaud's Vacqueyras from Château des Tours: the Rayas touch applied to Vacqueyras Grenache. Elegant, pure, and mineral — more restrained than most Vacqueyras with old-vine clarity and impressive aging potential for the appellation.")
if new2b:
    PAIR(prod2b, "Roasted poussin with roasted garlic, thyme, and pan jus", "complement", "established", "main",
        "Young chicken with Provençal aromatics brings out the purity of Château des Tours Grenache; garlic confit mirrors the wine's mineral sweetness")
    PAIR(prod2b, "Tapenade de sardines on toasted sourdough with lemon", "complement", "classic", "aperitif",
        "Provençal sardine spread with olive and lemon is the Mediterranean aperitif classic for Southern Rhône Grenache")
    PAIR(prod2b, "Leg of lamb slow-roasted with anchovy and garlic", "complement", "classic", "main",
        "Slow-roasted lamb with anchovy is the Southern Rhône's most elegant food pairing; the wine's purity and precision matches the dish's restraint")
    PAIR(prod2b, "Aged Comté with honey and toasted almonds", "bridge", "established", "cheese",
        "Mountain Comté with honey is a classic French cheese pairing for elegant Grenache; almonds add nuttiness to bridge the wine's mineral depth")

# ── REGION 3: Patrimonio AOC (France/Corsica) ───────────────────────────────
print("\n=== Region 3: Patrimonio ===")
r3 = R("Patrimonio", "France", "wine",
    designation_type="AOC", designation_name="Patrimonio AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Patrimonio is Corsica's first AOC and arguably its finest wine appellation, situated in the northern tip of the island near Saint-Florent. Red wines from Nielluccio (Sangiovese) on schist and limestone show remarkable structure and mineral complexity — more reminiscent of fine Italian reds than typical southern French wines. Whites from Vermentinu are perfumed and mineral; the Muscat du Cap Corse is among France's finest vins doux naturels.",
    key_producers="Antoine Arena, Domaine Gentile, Domaine de Catarelli, Yves Leccia",
    historical_context="Patrimonio received AOC status in 1968 — the first in Corsica — reflecting the exceptional quality long recognised in the northern cap. The region's unique combination of Nielluccio (brought by Genoese rulers, genetically identical to Sangiovese) and the island's schist and limestone terroir produces wines of genuine distinction. Antoine Arena's pioneering biodynamic work from the 1980s established international recognition.")

VIN(r3, 2023, "excellent", "rising", "Outstanding Corsican vintage; Nielluccio achieved exceptional ripeness with mineral precision from the limestone")
VIN(r3, 2022, "very_good", "stable", "Fine balanced year; structured Nielluccio with good aging potential and authentic Corsican character")
VIN(r3, 2021, "good", "stable", "Elegant, cooler year; refined and perfumed Nielluccio with excellent mineral acidity")
VIN(r3, 2020, "excellent", "rising", "Hot year producing powerful, concentrated Patrimonio; age-worthy and deeply structured")
VIN(r3, 2019, "very_good", "rising", "Classic vintage with excellent Nielluccio expression; schist mineral character beautifully defined")

prod3a_id = P("Antoine Arena", "France", r3, "winery",
    "The visionary producer who put Corsican wine on the world map; Antoine Arena's biodynamic estate near Patrimonio produces benchmark Nielluccio and Vermentinu wines of haunting mineral purity that command serious critical attention internationally.")
prod3a, new3a = PROD("Arena Patrimonio Rouge", "wine_still", prod3a_id, r3, "France",
    subcategory="red", price_tier="premium",
    description="Antoine Arena's benchmark Patrimonio red: Nielluccio (Corsican Sangiovese) from schist and limestone vineyards near Saint-Florent. Cherry, wild herb, iron mineral, and a saline quality unique to the island's coastal geology. Biodynamic and hauntingly complex.")
if new3a:
    PAIR(prod3a, "Whole roasted suckling pig (porcinu) with Corsican charcuterie board", "complement", "classic", "main",
        "Corsican suckling pig and Patrimonio Nielluccio is the island's defining celebratory pairing; the wine's mineral freshness cuts through the rich fat")
    PAIR(prod3a, "Grilled red mullet with olive oil, capers, and lemon", "complement", "established", "fish_course",
        "Red mullet's intense flavour and firm flesh work well with lighter Nielluccio; caper brine amplifies the wine's mineral salinity")
    PAIR(prod3a, "Corsican brocciu frais with chestnut honey and fresh mint", "complement", "classic", "cheese",
        "The island's fresh whey cheese with chestnut honey is the traditional Corsican cheese course for Patrimonio's mineral reds")
    PAIR(prod3a, "Figatellu (Corsican liver sausage) grilled over chestnut wood", "complement", "classic", "starter",
        "Figatellu is Corsica's most characteristic charcuterie — liver sausage grilled over chestnut — meeting Arena's structured mineral Nielluccio")

prod3b_id = P("Domaine Gentile", "France", r3, "winery",
    "One of Patrimonio's most consistent and accessible estates; Dominique Gentile produces elegant Nielluccio reds and perfumed Vermentinu whites that showcase the appellation's character with reliability and good value.")
prod3b, new3b = PROD("Gentile Patrimonio Rouge", "wine_still", prod3b_id, r3, "France",
    subcategory="red", price_tier="mid_range",
    description="Domaine Gentile's reliable Patrimonio red: Nielluccio with characteristic cherry, island herb (maquis), iron mineral, and fresh acidity. An accessible introduction to Corsican wine's distinctive identity — more structured and mineral than comparable mainland French reds.")
if new3b:
    PAIR(prod3b, "Charcuterie corse — coppa, lonzu, and prisuttu — with sourdough", "complement", "classic", "starter",
        "The Corsican charcuterie trinity is the island's great food identity; Patrimonio Nielluccio's mineral freshness cuts through the cured richness")
    PAIR(prod3b, "Grilled Corsican lamb with maquis herb marinade", "complement", "classic", "main",
        "Island lamb grazed on wild herbs (maquis) creates a direct aromatic link to Nielluccio's distinctive herb-mineral character")
    PAIR(prod3b, "Pasta with brousse du rove and fresh herbs", "complement", "established", "main",
        "Fresh sheep milk curd with herbs is a simple, authentic match for young Patrimonio's cherry and herb freshness")
    PAIR(prod3b, "Veal escalope with lemon, capers, and sage butter", "complement", "established", "main",
        "Italian-influenced veal preparation suits Nielluccio's Sangiovese character; lemon and caper bring the wine's acidity into alignment")

# ── REGION 4: Châteauneuf-du-Pape AOC (France/Rhône) ───────────────────────
print("\n=== Region 4: Châteauneuf-du-Pape ===")
r4 = R("Châteauneuf-du-Pape", "France", "wine",
    designation_type="AOC", designation_name="Châteauneuf-du-Pape AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Châteauneuf-du-Pape is the Southern Rhône's greatest appellation — a vast terroir of rolled galets roulés (heat-retaining pebbles), sand, and limestone producing Grenache-dominant blends of extraordinary complexity, richness, and longevity. The 18 permitted varieties offer unmatched blending possibilities. Top estates rival Burgundy Grand Cru in price and prestige.",
    key_producers="Château Rayas, Château Beaucastel, Henri Bonneau, Domaine du Vieux Télégraphe",
    historical_context="Châteauneuf-du-Pape was France's first AOC wine, regulated in 1923 under Baron Le Roy — the model for the entire French AOC system. The papal connection (the Avignon papacy, 1309-77) gave the appellation its name. Château Rayas's single-vineyard 100% Grenache has achieved the world's highest price-to-prestige ratio for Grenache internationally.")

VIN(r4, 2022, "exceptional", "rising", "One of the great modern Châteauneuf vintages; extraordinary old-vine Grenache concentration with remarkable balance and aging structure")
VIN(r4, 2021, "good", "stable", "Fresher, more accessible style; good typicity but lighter body than the best vintages — early drinking pleasure")
VIN(r4, 2020, "excellent", "rising", "Outstanding vintage with powerful, concentrated wines; exceptional galets terroir expression")
VIN(r4, 2019, "very_good", "rising", "Fine vintage with classic Châteauneuf character; garrigue, dark fruit, and rich mineral depth")
VIN(r4, 2016, "exceptional", "rising", "One of the decade's finest Châteauneuf vintages; age-worthy Grenache of extraordinary complexity and depth")

prod4a_id = P("Château Beaucastel", "France", r4, "winery",
    "One of Châteauneuf-du-Pape's most prestigious and biodynamic estates; the Perrin family uses all 18 permitted varieties — unusual for the appellation — with the highest Mourvèdre content (30%) of any major estate, giving the wines exceptional structure and 50-year aging potential.")
prod4a, new4a = PROD("Château Beaucastel Châteauneuf-du-Pape", "wine_still", prod4a_id, r4, "France",
    subcategory="red", price_tier="ultra_premium",
    description="The reference for structured, age-worthy Châteauneuf: Beaucastel's 13-variety blend with 30% Mourvèdre gives leather, garrigue, dark cherry, and iron mineral complexity. One of the Southern Rhône's greatest wines — structured for 20-40 year evolution.")
if new4a:
    PAIR(prod4a, "Slow-roasted rack of lamb with truffle and garrigue herb crust", "complement", "classic", "main",
        "The definitive Châteauneuf pairing: lamb with truffle and Provençal herbs meet the wine's extraordinary garrigue complexity and Mourvèdre depth")
    PAIR(prod4a, "Wild duck with olive, cèpe, and Armagnac sauce", "complement", "classic", "main",
        "Wild duck's gaminess and olive-cèpe sauce mirror Beaucastel's leather and dark fruit; Armagnac deepens the aromatic register")
    PAIR(prod4a, "Aged Langres with marc de Bourgogne and walnut", "bridge", "established", "cheese",
        "Washed-rind Langres with marc bridges Châteauneuf's complex dark fruit; walnut bitterness tames the wine's tannin grip")
    PAIR(prod4a, "Périgord black truffle omelette with aged Comté and chives", "complement", "adventurous", "main",
        "Black truffle's earthy depth is the luxury vehicle for aged Beaucastel; Comté adds nutty complexity to echo the wine's layered character")

prod4b_id = P("Domaine du Vieux Télégraphe", "France", r4, "winery",
    "One of Châteauneuf-du-Pape's most consistent high-quality estates; the Brunier family's Vieux Télégraphe from the La Crau plateau's galets roulés is a benchmark for Grenache-dominant Châteauneuf of balance, complexity, and aging ability.")
prod4b, new4b = PROD("Vieux Télégraphe Châteauneuf-du-Pape La Crau", "wine_still", prod4b_id, r4, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Vieux Télégraphe's benchmark La Crau Châteauneuf: Grenache from the highest galets roulés plateau, blended with Syrah and Mourvèdre. Rich and concentrated with remarkable mineral definition from the heat-reflecting stones; structured for 15-25 year evolution.")
if new4b:
    PAIR(prod4b, "Roast pigeon with black olive, foie gras, and Périgord truffle", "complement", "classic", "main",
        "The great luxury trio — pigeon, foie gras, truffle — is one of the few preparations that matches La Crau's complexity and power")
    PAIR(prod4b, "Grilled lamb shoulder with tapenade, rosemary, and anchovy stuffing", "complement", "classic", "main",
        "Anchovy-stuffed lamb with tapenade amplifies every dimension of Vieux Télégraphe: garrigue, olive, mineral, dark fruit")
    PAIR(prod4b, "Cassoulet with confit duck, lamb, and Toulouse sausage", "complement", "established", "main",
        "The greatest bean-and-meat dish requires a wine of La Crau's scale; the galets mineral depth integrates with cassoulet's rich fat")
    PAIR(prod4b, "Roquefort with dried fig, black pepper, and toasted walnut", "contrast", "classic", "cheese",
        "Roquefort and Châteauneuf is one of France's great contrasts; the wine's power matches the cheese's intensity while fig sweetens the collision")

# ── REGION 5: Rasteau AOC (France/Southern Rhône) ───────────────────────────
print("\n=== Region 5: Rasteau ===")
r5 = R("Rasteau", "France", "wine",
    designation_type="AOC", designation_name="Rasteau AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Rasteau is one of the Southern Rhône's smaller village appellations elevated to its own AOC in 2010, producing robust Grenache-dominant red wines from clay and limestone soils on the north bank of the Ouvèze. The village also produces the unique Rasteau Vin Doux Naturel — a Grenache-based naturally sweet wine that can be oxidative (rancio) in style, aged for years in wood.",
    key_producers="Domaine de la Soumade, Château Beaurenard, Domaine des Coteaux des Travers, Domaine Escaravailles",
    historical_context="Rasteau has produced wine since antiquity — Roman vine cultivation is documented. The Vin Doux Naturel was recognised with its own AOC in 1944. The village was historically significant in the Côtes du Rhône Villages system and achieved its own village AOC for red wines in 2010, recognising the unique quality achievable from the slopes north of Orange.")

VIN(r5, 2023, "very_good", "stable", "Excellent Southern Rhône growing season; Rasteau Grenache achieved good concentration with clay soils retaining freshness")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage; dense and complex Rasteau with excellent structure and aging potential beyond the village's typical horizon")
VIN(r5, 2021, "good", "stable", "More accessible, lighter year; fresh Grenache character with good fruit and moderate structure")
VIN(r5, 2020, "excellent", "rising", "Hot year with powerful concentration; deep dark fruit and strong garrigue character")
VIN(r5, 2019, "very_good", "stable", "Classic Rasteau vintage with excellent Grenache typicity; dark cherry, herbs, and clay mineral depth")

prod5a_id = P("Domaine de la Soumade", "France", r5, "winery",
    "The benchmark producer of Rasteau; André Romero's estate has been instrumental in building the appellation's reputation, producing consistently excellent red wines and the rare Rasteau Vin Doux Naturel from old vine Grenache.")
prod5a, new5a = PROD("Soumade Rasteau Cuvée Prestige", "wine_still", prod5a_id, r5, "France",
    subcategory="red", price_tier="mid_range",
    description="La Soumade's flagship Rasteau: old vine Grenache concentrated on clay-limestone soils. Dark plum, garrigue, liquorice, and mineral depth — a richly textured Grenache that shows the new Rasteau AOC's quality potential and value versus Gigondas or Châteauneuf.")
if new5a:
    PAIR(prod5a, "Braised pork cheeks with black olives, thyme, and orange", "complement", "classic", "main",
        "Slow-braised pork cheeks with Provençal flavours meet Rasteau's dark Grenache fruit and garrigue; olive and orange add brightness")
    PAIR(prod5a, "Chicken thighs with preserved lemon, olive, and harissa", "complement", "established", "main",
        "North African-influenced chicken with preserved lemon cuts Rasteau's richness; harissa heat meets the wine's fruit weight")
    PAIR(prod5a, "Charcuterie board with saucisson, pâté, and Dijon mustard", "complement", "established", "starter",
        "French charcuterie classics are the natural vehicle for Southern Rhône Grenache; mustard's sharpness refreshes the wine's richness")
    PAIR(prod5a, "Grilled lamb kebabs with tzatziki, sumac, and warm flatbread", "complement", "established", "casual",
        "Eastern Mediterranean lamb preparation meets Rasteau's Mediterranean Grenache; sumac's acidity mirrors the wine's herb character")

prod5b_id = P("Domaine Escaravailles", "France", r5, "winery",
    "A highly regarded Rasteau estate producing excellent Grenache-dominant reds and the appellation's rare fortified Vin Doux Naturel; Gilles Ferran's wines show excellent concentration and terroir authenticity at reasonable prices.")
prod5b, new5b = PROD("Escaravailles Rasteau Les Valentianes", "wine_still", prod5b_id, r5, "France",
    subcategory="red", price_tier="mid_range",
    description="Escaravailles's single-lieu-dit Rasteau from Les Valentianes; concentrated old vine Grenache with Syrah adding colour and spice depth. Dark cherry, garrigue, chocolate, and clay mineral character — excellent value and reliability for the new Rasteau AOC.")
if new5b:
    PAIR(prod5b, "Ratatouille with fresh herbs and baked eggs", "complement", "classic", "main",
        "Provençal vegetable ratatouille with eggs is a rustic match for Rasteau's garrigue and dark fruit; the herb character mirrors the wine's aromatic depth")
    PAIR(prod5b, "Duck magret with cherry sauce and roasted root vegetables", "complement", "established", "main",
        "Duck breast's fat and cherry sauce echo Rasteau's dark fruit core; root vegetable earthiness deepens the wine's clay mineral character")
    PAIR(prod5b, "Stilton with port-soaked raisins and oatcakes", "contrast", "adventurous", "cheese",
        "Bold blue cheese contrast with Grenache's dark fruit; port-soaked raisins bridge between the wine and the cheese's intensity")
    PAIR(prod5b, "Lamb kofta with yoghurt, pomegranate, and mint", "complement", "established", "casual",
        "Spiced lamb kofta with cooling yoghurt and pomegranate's sweet-tart note balance Rasteau's warm Grenache generosity")

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
print("Done.")
conn.close()
