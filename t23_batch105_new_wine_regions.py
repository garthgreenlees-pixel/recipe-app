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

# ── Region 1: Côtes du Rhône Villages ────────────────────────────────────────
print("=== Region 1: Côtes du Rhône Villages ===")
r = R("Côtes du Rhône Villages", "France", "wine",
      designation_type="AOC", designation_name="Côtes du Rhône Villages AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Southern Rhône quality tier above generic Côtes du Rhône; 22 named villages including Cairanne, Séguret, Rasteau; Grenache-led blends with Syrah and Mourvèdre of genuine character.",
      key_producers="Domaine Marcel Richaud, Château des Estaillades, Domaine des Escaravailles",
      historical_context="Cairanne became a standalone appellation in 2016; Rasteau also has its own AOC; the Villages tier has driven southern Rhône's quality revolution in the 2000s-2020s.")
VIN(r, 2022, "excellent", "stable", "Good southern Rhône year; Grenache of freshness and herbal depth.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, aromatic Villages reds with fine garrigue character.")
VIN(r, 2020, "exceptional", "rising", "Outstanding year; Villages wines of surprising depth and structure.")
VIN(r, 2019, "excellent", "stable", "Classic profile; fruit-forward, food-friendly Villages wines.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; plush, generous Grenache blends.")
p1 = P("Domaine Marcel Richaud", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Eric Richaud's biodynamic Cairanne estate; L'Ebrescade (old-vine Grenache) is their flagship; certified Demeter; old-vine Grenache from limestone and clay soils.",
       reputation_narrative="Marcel Richaud's L'Ebrescade proved Cairanne could rival the finest Châteauneuf; benchmark for serious southern Rhône value.",
       price_positioning="mid_range")
p2 = P("Domaine des Escaravailles", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Gilles Ferran's Rasteau-Cairanne estate; La Ponce from ancient Grenache vines; wines of garrigue, mineral depth and excellent value; sustainable certified.",
       reputation_narrative="Escaravailles produces some of the finest Rasteau and Cairanne wines; La Ponce is a benchmark for overlooked southern Rhône quality.",
       price_positioning="mid_range")
pr1, n1 = PROD("Richaud L'Ebrescade Cairanne", "wine_still", p1, r, "France",
               subcategory="Grenache blend", price_tier="mid_range",
               description="Old-vine biodynamic Cairanne Grenache; dark fruit, garrigue, lavender, black olive and a structured, mineral finish; rivals Châteauneuf at a quarter of the price; ages magnificently.")
if n1:
    PAIR(pr1, "Grilled lamb cutlets with herbes de Provence", "complement", "classic", "main", "Southern Rhône lamb pairing; garrigue and dark fruit mirror Provençal herbs and charred lamb.")
    PAIR(pr1, "Gratin d'aubergines with Comté and tomato", "complement", "established", "main", "Garrigue Grenache suits Mediterranean vegetable gratin; dark fruit bridges tomato acidity.")
    PAIR(pr1, "Wild boar daube with olives and orange peel", "complement", "established", "main", "Structured old-vine Grenache suits braised boar; olive and orange echo wine's black olive note.")
    PAIR(pr1, "Aged Banon goat's cheese in chestnut leaves", "complement", "adventurous", "cheese", "Biodynamic Grenache's depth suits pungent Banon; garrigue bridges chestnut-leaf earthiness.")
pr2, n2 = PROD("Escaravailles La Ponce Rasteau", "wine_still", p2, r, "France",
               subcategory="Grenache Mourvèdre", price_tier="value",
               description="Old-vine Rasteau from ancient Grenache and Mourvèdre; dark cherry, thyme, rosemary, black pepper and garrigue; structured and age-worthy; remarkable value for depth of character.")
if n2:
    PAIR(pr2, "Saucisse de Toulouse grillée with Dijon mustard", "complement", "established", "main", "Southern French pairing; Grenache-Mourvèdre suits hearty pork sausage; thyme bridges.")
    PAIR(pr2, "Daube Provençale with capers and anchovy", "complement", "classic", "main", "Provençal classic; garrigue and dark cherry bridge slow-braised beef; anchovy amplifies savory depth.")
    PAIR(pr2, "Socca with rosemary and sea salt", "complement", "classic", "aperitif", "Provençal street food pairing; wine's rosemary note echoes socca; Grenache warmth suits chickpea.")
    PAIR(pr2, "Aged Pélardon chèvre with thyme honey", "complement", "suggested", "cheese", "Southern French pairing; Mourvèdre depth and dark fruit suit aged goat's cheese; honey bridges.")

# ── Region 2: Vacqueyras ──────────────────────────────────────────────────────
print("=== Region 2: Vacqueyras ===")
r = R("Vacqueyras", "France", "wine",
      designation_type="AOC", designation_name="Vacqueyras AOC",
      reputation_tier="respected", quality_trajectory="established",
      description="Southern Rhône village appellation between Gigondas and Beaumes-de-Venise; Grenache-led reds of considerable structure and garrigue character; one of the southern Rhône's best value appellations.",
      key_producers="Château des Tours, Clos des Cazaux, Domaine La Garrigue",
      historical_context="Vacqueyras received its own AOC in 1990; troubadour Raimbaut de Vaqueiras praised the wines in the 12th century; often compared to a mini-Châteauneuf without the premium.")
VIN(r, 2022, "excellent", "stable", "Good year; Grenache of characteristic southern richness and herb notes.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, garrigue-scented Vacqueyras of fine balance.")
VIN(r, 2020, "exceptional", "rising", "Outstanding southern Rhône vintage; Vacqueyras of Gigondas-level depth.")
VIN(r, 2019, "excellent", "stable", "Classic profile; plush, generous reds of consistent quality.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; accessible, food-friendly Vacqueyras.")
p1 = P("Château des Tours", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Emmanuel Reynaud's (Château Rayas nephew) Vacqueyras estate; old-vine Grenache from sand and pebble soils; same philosophy as Rayas; wines of extraordinary purity and depth.",
       reputation_narrative="Château des Tours is the cult wine of Vacqueyras; Reynaud's pure Grenache philosophy produces wines of Châteauneuf-calibre purity at accessible prices.",
       price_positioning="mid_range")
p2 = P("Clos des Cazaux", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="The Archimbaud-Vache family's benchmark Vacqueyras and Gigondas estate; Cuvée des Templiers is their prestige Vacqueyras; organic practices; old-vine Grenache from rocky limestone.",
       reputation_narrative="Clos des Cazaux is one of Vacqueyras's most consistent quality estates; Cuvée des Templiers demonstrates the appellation's serious potential.",
       price_positioning="mid_range")
pr1, n1 = PROD("Château des Tours Vacqueyras Rouge", "wine_still", p1, r, "France",
               subcategory="Grenache", price_tier="mid_range",
               description="Pure old-vine Grenache from sandy pebble terroir; extraordinary purity — kirsch, raspberry, pepper, garrigue and a long, silky finish; Rayas philosophy applied to Vacqueyras with stunning results.")
if n1:
    PAIR(pr1, "Rack of lamb with lavender salt and grilled vegetables", "complement", "classic", "main", "Southern Rhône classic; pure Grenache's kirsch and garrigue mirror lavender lamb.")
    PAIR(pr1, "Provençal stuffed vegetables (petits farcis)", "complement", "classic", "main", "Regional Provençal pairing; Grenache's fruit and herb notes echo stuffed summer vegetables.")
    PAIR(pr1, "Chicken tagine with olives and preserved lemon", "complement", "established", "main", "Grenache's fruit and warmth bridge Moroccan spice and olive; preserved lemon echoes wine's acidity.")
    PAIR(pr1, "Aged Comté 24 months with walnut bread", "complement", "suggested", "cheese", "Silky Grenache suits aged Comté; kirsch bridges; walnut bread echoes wine's Rhône garrigue.")
pr2, n2 = PROD("Clos des Cazaux Cuvée des Templiers Vacqueyras", "wine_still", p2, r, "France",
               subcategory="Grenache Mourvèdre Syrah", price_tier="mid_range",
               description="Prestige Vacqueyras blend from old vines on rocky limestone; Grenache with Mourvèdre and Syrah; dark fruit, leather, garrigue, iron and a robust structured finish; serious and age-worthy.")
if n2:
    PAIR(pr2, "Braised lamb shank with rosemary and red wine", "complement", "classic", "main", "Mourvèdre-structured Vacqueyras suits slow-braised lamb; rosemary echoes garrigue.")
    PAIR(pr2, "Grilled duck magret with fig reduction", "complement", "established", "main", "Dark fruit and leather Vacqueyras suits duck magret; fig bridges wine's black fruit.")
    PAIR(pr2, "Cassoulet with Toulouse sausage and duck confit", "complement", "classic", "main", "Classic southwestern pairing; robust Mourvèdre structure suits hearty cassoulet richness.")
    PAIR(pr2, "Époisses cheese with crusty baguette", "contrast", "adventurous", "cheese", "Robust Vacqueyras stands up to Époisses pungency; dark fruit and leather contrast washed rind.")

# ── Region 3: Picpoul de Pinet ────────────────────────────────────────────────
print("=== Region 3: Picpoul de Pinet ===")
r = R("Picpoul de Pinet", "France", "wine",
      designation_type="AOP", designation_name="Picpoul de Pinet AOP",
      reputation_tier="respected", quality_trajectory="established",
      description="Languedoc coastal appellation near the Étang de Thau lagoon; Picpoul Blanc produces France's most seafood-specific dry white — electric acidity, lemon, green herb and saline freshness; the oyster wine of the South.",
      key_producers="Château de Pinet, Domaine Félines Jourdan, Cave de l'Ormarine",
      historical_context="Picpoul means 'lip-stinger' in Occitan — a reference to the grape's extreme acidity; the Thau lagoon produces 13,000 tonnes of oysters annually; Picpoul is the traditional accompaniment.")
VIN(r, 2023, "excellent", "stable", "Good Mediterranean year; Picpoul of fine electric acidity and coastal freshness.")
VIN(r, 2022, "very_good", "stable", "Warm year; rounder Picpoul with more body; still excellent with oysters.")
VIN(r, 2021, "excellent", "stable", "Classic profile; textbook lemon-saline Picpoul of great versatility.")
VIN(r, 2020, "very_good", "stable", "Good balance; reliable, food-friendly Picpoul de Pinet.")
VIN(r, 2019, "excellent", "stable", "Fine southern year; classic electric-acid Picpoul at its finest.")
p1 = P("Domaine Félines Jourdan", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Family estate on the Thau lagoon shoreline; Picpoul Blanc from garrigue-scented limestone; Félines is their classic; Piquepoul de Pinet is their premium old-vine expression.",
       reputation_narrative="Félines Jourdan is the most recognised Picpoul de Pinet estate internationally; Piquepoul old-vine shows the variety's surprising complexity.",
       price_positioning="value")
p2 = P("Cave de l'Ormarine", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The leading Picpoul cooperative; Duc de Morny is their classic Picpoul; sells the most Picpoul internationally; consistent, reliable and food-friendly at accessible prices.",
       reputation_narrative="Cave de l'Ormarine's Duc de Morny is the world's most consumed Picpoul de Pinet; consistent, widely available and perfectly suited to seafood.",
       price_positioning="value")
pr1, n1 = PROD("Félines Jourdan Piquepoul de Pinet", "wine_still", p1, r, "France",
               subcategory="Picpoul Blanc", price_tier="value",
               description="Estate Picpoul de Pinet from lagoon-side limestone; electric lemon, green apple, white flower and saline mineral; the electric acidity and freshness make this one of France's most versatile seafood whites.")
if n1:
    PAIR(pr1, "Oysters from the Thau lagoon with lemon", "complement", "classic", "aperitif", "The defining Picpoul pairing; wine's electric acidity and salinity mirror Thau oysters perfectly.")
    PAIR(pr1, "Moules farcies (stuffed mussels) with herbs", "complement", "classic", "starter", "Languedoc coastal classic; saline mineral wine echoes mussel brine; herb notes align.")
    PAIR(pr1, "Grilled gilt-head bream (daurade) with fennel", "complement", "established", "fish_course", "Mediterranean pairing; electric Picpoul acidity amplifies sea bream; fennel bridges.")
    PAIR(pr1, "Seafood platter with crustaceans and shellfish", "complement", "classic", "main", "The quintessential Languedoc aperitif; Picpoul's acidity suits all crustacean and shellfish.")
pr2, n2 = PROD("Duc de Morny Picpoul de Pinet", "wine_still", p2, r, "France",
               subcategory="Picpoul Blanc", price_tier="value",
               description="Classic cooperative Picpoul; lemon, green apple, fresh herb and a clean bracing finish; reliable, everyday seafood white of genuine freshness and excellent value.")
if n2:
    PAIR(pr2, "Grilled sardines with sea salt and lemon", "complement", "classic", "starter", "Mediterranean classic; electric Picpoul acidity cuts sardine oil; lemon echoes wine's citrus.")
    PAIR(pr2, "Spaghetti alle vongole in bianco", "complement", "established", "main", "Saline-electric Picpoul mirrors clam brine; lemon bridges the white wine in the sauce.")
    PAIR(pr2, "Fish tacos with lime crema and avocado", "complement", "suggested", "casual", "Electric acidity mirrors lime; freshness suits crispy fish; green apple bridges avocado.")
    PAIR(pr2, "Bouillabaisse with rouille and croutons", "complement", "established", "main", "Provençal-Languedoc coastal classic; electric Picpoul suits saffron-tomato fish broth.")

# ── Region 4: Faugères ────────────────────────────────────────────────────────
print("=== Region 4: Faugères ===")
r = R("Faugères", "France", "wine",
      designation_type="AOC", designation_name="Faugères AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Languedoc hillside appellation on friable blue schist soils; Grenache, Syrah, Mourvèdre and Carignan produce schist-mineral reds of real character; also Grenache Blanc and Marsanne whites.",
      key_producers="Léon Barral, Domaine de Cébène, Alquier",
      historical_context="Faugères' schist is so friable that vines almost seem to float; phylloxera spread slowly through schist (roots harder to penetrate); many old pre-phylloxera vines survive.")
VIN(r, 2022, "excellent", "rising", "Good schist year; Faugères of mineral depth and aromatic freshness.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, precise Faugères with fine schist mineral character.")
VIN(r, 2020, "exceptional", "rising", "Outstanding year; Faugères reds of rare depth and schist mineral intensity.")
VIN(r, 2019, "excellent", "stable", "Classic profile; structured reds with characteristic schist iron and herb notes.")
VIN(r, 2018, "very_good", "stable", "Good balance; food-friendly, accessible Faugères.")
p1 = P("Léon Barral", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Didier Barral's legendary natural estate; cow manure and composting; old-vine Carignan, Grenache, Cinsault and Terret Bourret; Jadis and Valinière are his great schist-mineral wines.",
       reputation_narrative="Léon Barral is one of France's most revered natural wine estates; Jadis and Valinière are schist-mineral masterpieces that have inspired a generation of Languedoc producers.",
       price_positioning="mid_range")
p2 = P("Domaine de Cébène", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Brigitte Chevalier's biodynamic estate; Les Bancèls and Belle Lurette from old-vine schist; indigenous yeasts; minimal sulphur; new generation of serious Faugères quality.",
       reputation_narrative="Domaine de Cébène is Faugères' most exciting modern producer; Belle Lurette and Les Bancèls are considered benchmarks for schist-terroir expression.",
       price_positioning="mid_range")
pr1, n1 = PROD("Léon Barral Jadis Faugères", "wine_still", p1, r, "France",
               subcategory="Carignan Grenache", price_tier="mid_range",
               description="Natural old-vine Faugères from schist; Carignan and Grenache of extraordinary mineral depth — iron, dried herbs, wild blackberry, schist earth and a long mineral finish; 15+ years of life ahead.")
if n1:
    PAIR(pr1, "Grilled wild boar sausages with lentils du Puy", "complement", "established", "main", "Schist iron and old-vine depth mirror wild boar's earthiness; lentils bridge mineral character.")
    PAIR(pr1, "Braised Catalan snails with alioli and herbs", "complement", "classic", "starter", "Languedoc tradition; natural Carignan's iron and herb notes suit escargots and alioli.")
    PAIR(pr1, "Lamb ribs with cumin, coriander and pomegranate", "complement", "suggested", "main", "Schist mineral and dried herb notes bridge North African spice; wild blackberry echoes pomegranate.")
    PAIR(pr1, "Aged Roquefort with black olives and walnuts", "complement", "adventurous", "cheese", "Old-vine depth stands up to Roquefort; iron and herb notes bridge pungency; walnuts echo.")
pr2, n2 = PROD("Domaine de Cébène Belle Lurette Faugères", "wine_still", p2, r, "France",
               subcategory="Grenache Syrah Carignan", price_tier="mid_range",
               description="Biodynamic Faugères from schist; Grenache, Syrah and Carignan; violet, wild herbs, iron-mineral, black olive and a structured finish of genuine schist character; modern Languedoc at its finest.")
if n2:
    PAIR(pr2, "Slow-roasted pork belly with herbes de Garrigue", "complement", "classic", "main", "Languedoc garrigue pairing; herb-mineral wine mirrors garrigue-rubbed pork; Grenache fruit bridges.")
    PAIR(pr2, "Duck breast with cherry tomato sauce and basil", "complement", "established", "main", "Violet and wild herbs echo basil; Grenache fruit mirrors cherry tomato; schist mineral grounds.")
    PAIR(pr2, "Grilled zucchini flowers with ricotta and herbs", "complement", "suggested", "starter", "Schist mineral and violet suit delicate zucchini flowers; ricotta bridges; herbs align.")
    PAIR(pr2, "Brebis des Pyrénées with fig jam", "complement", "classic", "cheese", "Southern pairing; biodynamic mineral Grenache suits sheep's milk; fig echoes wine's dried fruit.")

# ── Region 5: Saint-Chinian ───────────────────────────────────────────────────
print("=== Region 5: Saint-Chinian ===")
r = R("Saint-Chinian", "France", "wine",
      designation_type="AOC", designation_name="Saint-Chinian AOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Languedoc appellation north of Béziers; schist in the north and limestone-clay in the south produce distinctly different wines; Grenache, Syrah, Mourvèdre and Carignan of genuine terroir character.",
      key_producers="Domaine Rimbert, Mas Champart, Clos Bagatelle, Borie La Vitarèle",
      historical_context="Saint-Chinian received appellation status in 1982; the schist-limestone divide within the appellation creates two very different wine styles; natural wine movement has elevated quality significantly.")
VIN(r, 2022, "excellent", "stable", "Good year; Saint-Chinian of characteristic schist-mineral and garrigue freshness.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, food-friendly Saint-Chinian of consistent quality.")
VIN(r, 2020, "exceptional", "rising", "Benchmark year; both schist and limestone wines showed outstanding depth.")
VIN(r, 2019, "excellent", "stable", "Classic Languedoc profile; structured, food-friendly reds of good depth.")
VIN(r, 2018, "very_good", "stable", "Good balance; accessible Saint-Chinian with characteristic garrigue warmth.")
p1 = P("Domaine Rimbert", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Jean-Marie Rimbert's organic schist estate; Le Mas au Schiste and Le Chant de Marjolaine from old-vine Carignan and Cinsault; indigenous yeasts; no-filtration; minimal sulphur.",
       reputation_narrative="Rimbert is Saint-Chinian's most acclaimed natural wine producer; Le Mas au Schiste is one of Languedoc's greatest old-vine expressions.",
       price_positioning="mid_range")
p2 = P("Mas Champart", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Matthieu and Isabelle Champart's limestone-clay estate; Causse du Bousquet from Mourvèdre-Grenache-Syrah on limestone; one of Saint-Chinian's most age-worthy and serious producers.",
       reputation_narrative="Mas Champart's Causse du Bousquet is Saint-Chinian's limestone-terroir benchmark; wines that rival Faugères schist for depth and longevity.",
       price_positioning="mid_range")
pr1, n1 = PROD("Rimbert Le Mas au Schiste Saint-Chinian", "wine_still", p1, r, "France",
               subcategory="Carignan Cinsault", price_tier="mid_range",
               description="Natural old-vine schist Saint-Chinian from Carignan and Cinsault; violet, wild berry, iron-mineral, rosemary and a mineral-driven finish; natural energy and genuine terroir expression.")
if n1:
    PAIR(pr1, "Barbecue lamb ribs with rosemary and thyme marinade", "complement", "classic", "main", "Schist mineral and rosemary in wine echo marinade; Carignan's violet matches grilled lamb.")
    PAIR(pr1, "Grilled Catalan blood sausage (botifarra negra)", "complement", "classic", "main", "Languedoc-Catalunya pairing; iron mineral and wild berry suit blood sausage richness.")
    PAIR(pr1, "Grilled summer vegetables with herbes de Garrigue", "complement", "established", "main", "Natural wine and vegetable terraine; schist mineral and rosemary mirror grilled vegetable char.")
    PAIR(pr1, "Aged Pélardon chèvre from the Cévennes", "complement", "classic", "cheese", "Regional pairing; schist mineral and violet suit aged local goat's cheese.")
pr2, n2 = PROD("Mas Champart Causse du Bousquet Saint-Chinian", "wine_still", p2, r, "France",
               subcategory="Mourvèdre Grenache Syrah", price_tier="mid_range",
               description="Limestone-clay Saint-Chinian blend of Mourvèdre, Grenache and Syrah; dark fruit, leather, black olive, thyme and a structured finish built for aging; the limestone terroir's most serious expression.")
if n2:
    PAIR(pr2, "Braised leg of lamb with garlic and rosemary", "complement", "classic", "main", "Mourvèdre structure grips lamb's richness; dark fruit and leather bridge slow-braise; thyme echoes herb.")
    PAIR(pr2, "Wild boar terrine with juniper and bay leaf", "complement", "established", "starter", "Leather and dark fruit Mourvèdre suits game terrine; juniper bridges herbal complexity.")
    PAIR(pr2, "Cassoulet languedocien with duck and Toulouse sausage", "complement", "classic", "main", "Regional cassoulet tradition; structured Mourvèdre blend suits cassoulet's hearty richness.")
    PAIR(pr2, "Aged Cantal with walnuts and chestnut honey", "complement", "suggested", "cheese", "Structured Saint-Chinian suits firm aged Cantal; walnut echoes Mourvèdre's earthy depth.")

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
