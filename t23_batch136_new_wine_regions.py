#!/usr/bin/env python3
"""B136 — Cahors AOC (France), Marcillac AOC (France), Gaillac AOC (France),
   Côtes du Roussillon Villages AOC (France), Collioure AOC (France)
Constraints confirmed:
  quality_descriptor: exceptional/excellent/very_good/good/average/challenging/poor
  price_trajectory: rising/stable/declining/speculative/unavailable
  reputation_tier: iconic/prestigious/respected/emerging/overlooked
  quality_trajectory: ascending/established/declining/emerging/rediscovering
  producer_type: winery/distillery/brewery/tea_garden/coffee_estate/sake_brewery/cidery/meadery/kombucha_brewery/multi_category
  meal_context: aperitif/amuse/starter/fish_course/main/cheese/pre_dessert/dessert/digestif/celebration/casual/any
  pairing_type: complement/contrast/bridge/cleanse/elevate
  confidence: classic/established/suggested/adventurous/experimental
  price_tier: ultra_premium/premium/mid_range/value/entry
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

# ── CAHORS AOC (France) ───────────────────────────────────────────────────────
print("=== Cahors AOC ===")
r = R("Cahors AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Cahors AOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Southwest France's 'Black Wine' appellation producing intensely structured Malbec (Côt) from limestone causse plateau and river-valley terraces above the Lot River. Cahors Malbec predates Argentine plantings and offers earthy, iron-tinged, tannic wines capable of long cellaring.",
      key_producers="Château du Cèdre, Clos Triguedina, Domaine de Lagrezette",
      historical_context="Medieval Cahors wine was exported to England and Rome before Bordeaux rose to dominance. The 1956 frost nearly destroyed the appellation. Malbec revival since the 1980s has restored Cahors's reputation as a source of serious, distinctive southern French reds.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm, dry vintage produced concentrated Malbec of exceptional depth and structure."),
    (2019, "very_good", "stable", "Balanced conditions; rich fruit with good tannic framework for medium-term aging."),
    (2020, "good", "stable", "Heat stress challenged some estates; best causse plateau wines showed concentration."),
    (2021, "very_good", "stable", "Cooler year restored freshness and aromatic lift to Cahors Malbec."),
    (2022, "excellent", "rising", "Superb ripening on causse limestone; wines of power, mineral precision and aging potential."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Château du Cèdre", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Pascal and Jean-Marc Verhaeghe at Château du Cèdre produce benchmark Cahors from old Malbec vines on the causse limestone plateau, using low yields, traditional fermentation and minimal oak to showcase the variety's authentic terroir expression.",
       reputation_narrative="Consistently regarded as Cahors's finest estate, Château du Cèdre's Le Cèdre cuvée demonstrates that Cahors Malbec can rival international standards for complexity and longevity.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Château du Cèdre Le Cèdre Cahors", "wine_still", p1, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Flagship Cahors from 40-year-old Malbec vines on causse limestone; intense blackberry, iron, violet and earthy mineral complexity with structured tannins built for 15+ years of aging.")
if is_new:
    PAIR(prod, "Cassoulet de canard with crispy duck confit", "complement", "classic", "main", "Iron-tannic Cahors Malbec is the defining match for rich, slow-cooked cassoulet with duck.")
    PAIR(prod, "Roasted côte de boeuf with bone marrow butter", "complement", "classic", "main", "Causse limestone Malbec's iron-blackberry structure handles the richness of dry-aged beef and marrow.")
    PAIR(prod, "Magret de canard with Périgueux sauce (truffle)", "complement", "established", "main", "Earthy truffle and duck fat richness are elevated by the mineral iron-tannic depth of Cahors.")
    PAIR(prod, "Aged Cantal or Laguiole cheese", "complement", "established", "cheese", "Firm southern French cheese mirrors the causse mineral character of this tannic Malbec.")

prod, is_new = PROD("Château du Cèdre Prestige Cahors", "wine_still", p1, r, "France",
    subcategory="red", price_tier="premium",
    description="Accessible Cahors Malbec from the Cèdre estate; dark berry, earthen spice and structured tannins with the signature mineral character of the limestone causse.")
if is_new:
    PAIR(prod, "Confit de canard with Sarladaise potatoes", "complement", "classic", "main", "Regional classic — Périgord duck confit with potatoes is inseparable from Cahors Malbec.")
    PAIR(prod, "Grilled lamb merguez with harissa and flatbread", "complement", "established", "casual", "Spiced lamb sausage and harissa heat find balance in earthy, dark-fruited Cahors.")
    PAIR(prod, "Wild mushroom tart with thyme and Gruyère", "complement", "established", "main", "Earthy Malbec character resonates with forest mushroom and aged cheese depth.")
    PAIR(prod, "Charcuterie board with rillettes, pâté and cornichons", "complement", "suggested", "casual", "Southwest French charcuterie finds its natural regional wine companion in Cahors Malbec.")

p2 = P("Clos Triguedina", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The Baldès family has farmed Cahors for generations at Clos Triguedina, producing structured, age-worthy Malbec wines that honour the appellation's heritage while embracing modern quality standards.",
       reputation_narrative="One of Cahors's historic estates, Clos Triguedina's Probus cuvée remains one of the appellation's most acclaimed and age-worthy expressions of Malbec.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Clos Triguedina Probus Cahors", "wine_still", p2, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Icon of Cahors — old-vine Malbec aged 18 months in new oak; deeply concentrated with cassis, dark plum, iron minerals and profound tannic structure requiring a decade of patience.")
if is_new:
    PAIR(prod, "Slow-braised ox cheek with Périgueux and root vegetables", "complement", "classic", "main", "Powerful structured Malbec demands the collagen richness of long-braised ox cheek.")
    PAIR(prod, "Lièvre à la royale (pressed hare with blood sauce)", "complement", "established", "main", "The most demanding French game dish finds its ideal match in Cahors's most structured Malbec.")
    PAIR(prod, "Venison haunch with juniper and celeriac purée", "complement", "established", "main", "Dark game meat and juniper spice are supported by the iron-tannic mineral depth of Probus.")
    PAIR(prod, "Cantal entre-deux with walnut bread", "complement", "suggested", "cheese", "Semi-aged Cantal's buttery firmness is the ideal regional partner for mature Cahors Malbec.")

prod, is_new = PROD("Clos Triguedina Cahors Malbec", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Classic Cahors from Malbec across Triguedina's limestone terraces; dark fruit, earthen spice and tannic structure with regional authenticity.")
if is_new:
    PAIR(prod, "Duck breast with cherry and red wine reduction", "complement", "classic", "main", "Malbec's blackberry-cherry fruit mirrors the cherry reduction while handling duck fat richness.")
    PAIR(prod, "Toulouse sausage and lentil stew", "complement", "established", "casual", "Hearty pork sausage and earthy lentils find a structured companion in Cahors Malbec.")
    PAIR(prod, "Grilled pork belly with black garlic and bok choy", "bridge", "suggested", "main", "Earthy, dark-fruited Malbec bridges the smoky pork belly and umami of black garlic.")
    PAIR(prod, "Mushroom and Morbier gratin", "complement", "suggested", "main", "Washed-rind Morbier and baked mushroom earthiness echo the wine's forest floor mineral notes.")

# ── MARCILLAC AOC (France) ────────────────────────────────────────────────────
print("=== Marcillac AOC ===")
r = R("Marcillac AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Marcillac AOC",
      reputation_tier="overlooked",
      quality_trajectory="ascending",
      description="Small appellation in the Aveyron producing distinctive reds from Fer Servadou (Mansois) on iron-rich red sandstone soils. Wines display a unique metallic, peppery, blackcurrant and violet character unlike any other French red. Remarkable value for the quality level.",
      key_producers="Domaine du Cros, Cave de Marcillac, Domaine Jean-Luc Matha",
      historical_context="Marcillac's vineyards supplied the pilgrims of Conques and the cathedral workers of Rodez for centuries. Nearly abandoned after the phylloxera crisis, the appellation was saved by a small group of dedicated growers. AOC status granted 1990 recognised Fer Servadou's unique expression on the local rougier (red iron soils).")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Superb vintage on iron soils; Fer Servadou showed vivid blackcurrant and iron-pepper complexity."),
    (2019, "very_good", "stable", "Rich and generous; Mansois wines with ripe fruit and characteristic mineral grip."),
    (2020, "good", "stable", "Warm year challenged freshness; best sites retained Marcillac's distinctive peppery lift."),
    (2021, "very_good", "stable", "Cooler conditions produced Fer Servadou of elegant floral and iron-tinged precision."),
    (2022, "excellent", "rising", "Outstanding iron-soil vintage; wines of characteristic peppery grip and lasting intensity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine du Cros", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Philippe Teulier at Domaine du Cros is the leading ambassador of Marcillac's Fer Servadou, producing wines that showcase the variety's unique iron-mineral, peppery character from the appellation's distinctive rougier red sandstone terroir.",
       reputation_narrative="The benchmark estate for understanding Marcillac's singular terroir, Domaine du Cros produces wines that challenge the dominance of better-known Southwest French appellations.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Domaine du Cros Lo Sang del País Marcillac", "wine_still", p1, r, "France",
    subcategory="red", price_tier="premium",
    description="Flagship Marcillac from Fer Servadou on iron-red sandstone; dark blackcurrant, violet, iron mineral and black pepper character that is wholly distinctive and fiercely regional.")
if is_new:
    PAIR(prod, "Aligot with Tomme fraîche and garlic sausage", "complement", "classic", "main", "Aveyron's most famous dish — silky potato-cheese purée with garlic sausage — is natural with Marcillac's iron red.")
    PAIR(prod, "Tripoux d'Aveyron (stuffed tripe parcels)", "complement", "classic", "main", "The offal character and iron richness of tripoux resonates deeply with Marcillac's mineral iron notes.")
    PAIR(prod, "Grilled lamb chops with herbes de maquis", "complement", "established", "main", "Peppery Fer Servadou handles lamb's richness with the mineral precision of the Aveyron highlands.")
    PAIR(prod, "Roquefort with walnut bread and honey", "contrast", "established", "cheese", "Sharp, creamy Roquefort contrasts with the dry iron-tannic grip of Marcillac in a defining regional pairing.")

prod, is_new = PROD("Domaine du Cros Marcillac Vieilles Vignes", "wine_still", p1, r, "France",
    subcategory="red", price_tier="mid_range",
    description="Old-vine Fer Servadou from Marcillac; concentrated iron-mineral, cassis and spice with greater depth than the entry-level cuvée at remarkable value.")
if is_new:
    PAIR(prod, "Farçous (Aveyron herb and vegetable patties)", "complement", "classic", "casual", "Local Aveyron vegetable fritters are the natural everyday companion to Marcillac Fer Servadou.")
    PAIR(prod, "Pork collar with dried fruit and Armagnac sauce", "complement", "established", "main", "Dried fruit sweetness and Armagnac depth are bridged by the blackcurrant-iron character of old-vine Marcillac.")
    PAIR(prod, "Duck gizzard confit salad with walnuts", "complement", "established", "casual", "Iron-rich Fer Servadou is the regional companion for warm gizzard salad with walnut richness.")
    PAIR(prod, "Mushroom and truffle omelette with cep butter", "complement", "suggested", "main", "Earthy forest floor character of Marcillac echoes the truffle-mushroom depth of the rustic omelette.")

p2 = P("Domaine Jean-Luc Matha", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Jean-Luc Matha produces minimally interventionist Marcillac from Fer Servadou on rougier soils, using whole-cluster fermentation and no added sulphur to produce vivid, earthy expressions of the appellation's unique character.",
       reputation_narrative="A champion of natural winemaking in Marcillac, Jean-Luc Matha's wines show the full peppery, violet and iron intensity of Fer Servadou without cosmetic correction.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Domaine Matha Marcillac Mansois", "wine_still", p2, r, "France",
    subcategory="red", price_tier="mid_range",
    description="Natural, whole-cluster Marcillac from Fer Servadou (Mansois); vivid violet, iron, cassis and white pepper with characteristic rougier mineral grip.")
if is_new:
    PAIR(prod, "Grilled boudin noir with apple and mashed potato", "complement", "established", "main", "Iron-rich blood sausage and apple sweetness are a classical match for the mineral iron intensity of Marcillac.")
    PAIR(prod, "Charcuterie with saucisson sec and cornichons", "complement", "classic", "casual", "Cured pork and pickles are a natural companion to peppery, dark-fruited Fer Servadou.")
    PAIR(prod, "Pasta with wild boar ragù and Parmesan", "complement", "established", "main", "Game ragù earthiness and Parmesan salt echo the iron-tannic, spiced character of natural Marcillac.")
    PAIR(prod, "Grilled pigeon with blackcurrant jus and lentils", "complement", "suggested", "main", "Pigeon's delicate game character and blackcurrant jus mirror the wine's violet-cassis intensity perfectly.")

prod, is_new = PROD("Domaine Matha Cuvée Vieilles Vignes Marcillac", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Top natural cuvée from old Fer Servadou vines at Matha; concentrated, earthy and deeply characterful with rougier iron and whole-cluster spice depth.")
if is_new:
    PAIR(prod, "Roasted partridge with juniper and smoked lardons", "complement", "classic", "main", "Game bird with lardons brings out the iron-mineral and peppery complexity of old-vine Marcillac.")
    PAIR(prod, "Lentilles vertes du Puy with smoked duck", "complement", "established", "main", "Green lentil earthiness and smoked duck resonate with the iron mineral notes of Fer Servadou.")
    PAIR(prod, "Tomme de Lozère with dried figs and hazelnuts", "complement", "established", "cheese", "Semi-hard mountain cheese with dried fruit and nut echoes the peppery mineral depth of Marcillac.")
    PAIR(prod, "Boeuf bourguignon with root vegetables", "complement", "suggested", "main", "Slow-braised beef and wine-reduced sauce find structural support in old-vine Fer Servadou tannins.")

# ── GAILLAC AOC (France) ──────────────────────────────────────────────────────
print("=== Gaillac AOC ===")
r = R("Gaillac AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Gaillac AOC",
      reputation_tier="overlooked",
      quality_trajectory="ascending",
      description="One of France's oldest wine regions in the Tarn Valley of Southwest France, producing an extraordinary diversity of styles: dry, off-dry and sweet whites from Mauzac and Len de l'El; perlé (lightly sparkling) whites; and red wines from Braucol (Fer Servadou) and Duras. Gaillac's indigenous variety focus makes it one of France's most distinctive appellations.",
      key_producers="Domaine Plageoles, Château Moulin Bordes, Causse Marine",
      historical_context="Gaillac claims among the oldest wine traditions in France, with viticulture documented from the 1st century AD. The Benedictine monks of Gaillac Abbey shaped its medieval wine trade. The appellation's diversity of indigenous varieties — Mauzac, Braucol, Ondenc, Duras — makes it unique in French viticulture.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm vintage produced rich, concentrated Mauzac and Braucol with excellent structure."),
    (2019, "very_good", "stable", "Balanced conditions; aromatic whites and well-structured reds of genuine terroir character."),
    (2020, "good", "stable", "Heat challenged lighter varieties; Braucol and Duras reds showed best results."),
    (2021, "very_good", "stable", "Cool year produced fresh, aromatic whites and elegant, lighter-structured reds."),
    (2022, "excellent", "rising", "Benchmark vintage; Gaillac's indigenous varieties showed their finest expression in years."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Plageoles", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Robert and Bernard Plageoles are the guardians of Gaillac's indigenous varieties, maintaining a living library of ancient varietals including Ondenc, Mauzac Roux, and Verdanel. Their museum vineyard approach preserves viticultural heritage while producing wines of compelling authenticity.",
       reputation_narrative="No estate in France has done more to preserve viticultural biodiversity than Domaine Plageoles. Their Vin de Voile (sous-voile aging) and late-harvest wines are among Southwest France's most remarkable.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Plageoles Gaillac Mauzac Nature", "wine_still", p1, r, "France",
    subcategory="white", price_tier="premium",
    description="Ancestral method sparkling Gaillac from Mauzac; cloudy, alive and deeply traditional with apple, quince and yeast character from native fermentation in bottle.")
if is_new:
    PAIR(prod, "Rillettes de porc with sourdough and cornichons", "complement", "classic", "casual", "Sparkling Mauzac freshness and yeast character cuts through the rich fat of pork rillettes.")
    PAIR(prod, "Foie gras mi-cuit with toasted brioche and Sauternes gelée", "bridge", "established", "starter", "The wine's apple-quince character bridges foie gras richness without the weight of a dry wine.")
    PAIR(prod, "Roquefort on walnut toast with pear chutney", "contrast", "established", "cheese", "Ancestral bubbles and apple-quince acidity contrast with sharp Roquefort and balance pear sweetness.")
    PAIR(prod, "Tarte aux pommes with crème fraîche", "complement", "established", "dessert", "Apple-dominated Mauzac Nature finds its perfect fruit mirror in a classic French apple tart.")

prod, is_new = PROD("Plageoles Gaillac Braucol Rouge", "wine_still", p1, r, "France",
    subcategory="red", price_tier="premium",
    description="Single-varietal Braucol (Fer Servadou) from Gaillac; peppery, iron-tinged and dark-fruited with the distinctive character of this Southwest French native grape.")
if is_new:
    PAIR(prod, "Cassoulet Tarnais with goose and Toulouse sausage", "complement", "classic", "main", "Gaillac's regional cassoulet variant with goose and sausage is the natural match for Braucol.")
    PAIR(prod, "Grilled côtelette d'agneau with tapenade and herbs", "complement", "established", "main", "Lamb and olive-herb tapenade find the right tannic frame in peppery, dark-fruited Braucol.")
    PAIR(prod, "Duck gizzard and mushroom fricassée", "complement", "established", "main", "Iron-mineral Braucol resonates with the earthy duck gizzard and mushroom combination.")
    PAIR(prod, "Tomme des Pyrénées with quince paste", "complement", "suggested", "cheese", "Firm mountain cheese and quince sweetness mirror the iron-peppery depth of Gaillac Braucol.")

p2 = P("Causse Marine", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Patrice Lescarret at Causse Marine farms biodynamically in Gaillac, producing natural, orange, and unusual wines from indigenous and forgotten varieties. His exploration of ancestral winemaking techniques produces wines of singular, uncompromising character.",
       reputation_narrative="A pioneer of natural and orange wine in Southwest France, Causse Marine's distinctive approach to Gaillac's indigenous varieties has attracted international attention to this often-overlooked appellation.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Causse Marine Peyrouzelles Gaillac Blanc", "wine_still", p2, r, "France",
    subcategory="white", price_tier="premium",
    description="Natural Gaillac white from Len de l'El and Mauzac; orange-tinged, aromatic, textured and vivid with characteristic quince, herbs and mineral depth from limestone soils.")
if is_new:
    PAIR(prod, "Salade de gesiers (duck gizzard salad with walnuts)", "complement", "classic", "casual", "Textured, orange-inflected natural white suits the earthy richness of warm duck gizzard and walnut salad.")
    PAIR(prod, "Brandade de morue (salt cod purée with garlic and olive oil)", "complement", "established", "main", "Mineral, aromatic white wine bridges the richness of brandade with herbal freshness.")
    PAIR(prod, "Burrata with roasted peach and basil", "complement", "established", "casual", "Quince-aromatic Gaillac blanc matches stone fruit sweetness and the creaminess of burrata.")
    PAIR(prod, "Tempura prawn with ginger dipping sauce", "complement", "suggested", "casual", "Aromatic, textured natural white handles the fried prawn crunch and ginger spice with aplomb.")

prod, is_new = PROD("Causse Marine Rasdu Gaillac Rouge", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Natural Gaillac red from Duras and Braucol; vivid, earthy and peppery with minimal intervention showing pure indigenous variety character.")
if is_new:
    PAIR(prod, "Pintade rôtie (roast guinea fowl) with root vegetables", "complement", "established", "main", "Earthy, peppery Duras-Braucol blend suits the delicate game character of guinea fowl.")
    PAIR(prod, "Saucisses de Toulouse grillées avec flageolets", "complement", "classic", "casual", "Toulouse sausage with flageolet beans is the natural Southwest French companion for natural Gaillac rouge.")
    PAIR(prod, "Rabbit terrine with mustard and gherkins", "complement", "established", "starter", "Natural, earthy Gaillac red suits the rustic richness of rabbit terrine with mustard sharpness.")
    PAIR(prod, "Aubergine caviar with garlic and herbs", "complement", "suggested", "casual", "Smoky aubergine purée and herbal aromatics mirror the earthy, spiced character of this natural red.")

# ── CÔTES DU ROUSSILLON VILLAGES AOC (France) ─────────────────────────────────
print("=== Côtes du Roussillon Villages AOC ===")
r = R("Côtes du Roussillon Villages AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Côtes du Roussillon Villages AOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Northern Roussillon's most prestigious red wine appellation, producing concentrated, sun-drenched wines from Grenache, Syrah, Mourvèdre and Carignan on ancient schist, granite and limestone soils. Villages such as Maury, Tautavel and Latour-de-France produce wines of distinctive terroir character and exceptional concentration.",
      key_producers="Domaine Gauby, Mas Amiel, Clos du Rouge Gorge, Domaine Cazes",
      historical_context="Roussillon winemaking dates to Greek colonisation at Agde in 600 BC. Under French rule from 1659, the region developed its reputation for fortified Vins Doux Naturels. The modern table wine renaissance led by Domaine Gauby and others since the 1990s has revealed Roussillon's extraordinary potential for concentrated, terroir-driven reds.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Low yields from summer heat produced intensely concentrated village reds with remarkable structure."),
    (2019, "very_good", "stable", "Well-balanced vintage; aromatic Grenache-Syrah blends with good freshness for the zone."),
    (2020, "very_good", "stable", "Warm and dry; old-vine Carignan and Grenache produced exceptional concentration."),
    (2021, "good", "stable", "Cooler than typical; elegant, more approachable village wines of genuine freshness."),
    (2022, "excellent", "rising", "Outstanding vintage on schist; wines of benchmark concentration and Roussillon terroir precision."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Gauby", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Gérard Gauby pioneered the modern Roussillon renaissance, converting to biodynamics and working with incredibly old Grenache, Carignan and Macabeu vines to produce wines of extraordinary concentration, mineral depth and complexity that changed how the world viewed southern French wines.",
       reputation_narrative="The single most influential producer in Roussillon, Domaine Gauby's biodynamic wines from old vines on schist and granite have placed Roussillon alongside Burgundy in discussions of French terroir wine.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Gauby La Muntada Côtes du Roussillon Villages", "wine_still", p1, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Iconic old-vine Grenache and Carignan from Gauby's oldest parcels on Calce schist; profound mineral depth, dark fruit and savage character representing the pinnacle of Roussillon red wine.")
if is_new:
    PAIR(prod, "Wild hare à la royale with blood sauce", "complement", "classic", "main", "The most powerful traditional game preparation meets Roussillon's most profound old-vine red.")
    PAIR(prod, "Slow-roasted lamb shoulder with anchovy and rosemary", "complement", "classic", "main", "Schist-mineral Grenache handles the richness of slow lamb with anchovy umami and rosemary herbality.")
    PAIR(prod, "Braised boar with olives, tomato and herbes de garrigue", "complement", "established", "main", "Wild game and garrigue herb sauce echo the savage mineral intensity of this old-vine Roussillon red.")
    PAIR(prod, "Maroilles or Époisses washed-rind cheese", "contrast", "established", "cheese", "Pungent washed-rind cheese and the wine's savage mineral intensity create dramatic, memorable tension.")

prod, is_new = PROD("Gauby Vieilles Vignes Côtes du Roussillon", "wine_still", p1, r, "France",
    subcategory="red", price_tier="premium",
    description="Old-vine Roussillon red from Grenache, Syrah and Carignan; Gauby's entry-level wine demonstrates extraordinary quality, with garrigue herbs, dark berry and schist mineral character.")
if is_new:
    PAIR(prod, "Grilled côte d'agneau with tapenade and fennel gratin", "complement", "classic", "main", "Grenache-Syrah-Carignan blend is the natural partner for lamb with olive-herb depth and fennel sweetness.")
    PAIR(prod, "Catalan lamb stew (gigot à la catalane)", "complement", "classic", "main", "Roussillon's regional lamb preparation is inseparable from old-vine village reds of this calibre.")
    PAIR(prod, "Manchego with honey and Marcona almonds", "complement", "established", "cheese", "Spanish sheep cheese across the border resonates with Catalonia's garrigue-scented old-vine reds.")
    PAIR(prod, "Grilled Merguez with harissa and roasted peppers", "complement", "established", "casual", "Spiced lamb sausage and North African harissa fire find a natural partner in concentrated Roussillon red.")

p2 = P("Clos du Rouge Gorge", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Cyril Fhal at Clos du Rouge Gorge produces natural, minimal-intervention wines from old-vine Carignan and Grenache in Roussillon's Latour-de-France village, showing the extraordinary character of ancient vines and terroir without cosmetic winemaking.",
       reputation_narrative="One of the most exciting natural wine producers in Roussillon, Clos du Rouge Gorge's old-vine Carignan wines demonstrate the variety's capacity for elegance and complexity.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Clos du Rouge Gorge Vieux Carignan", "wine_still", p2, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Old-vine Carignan from Latour-de-France granite; transparent, mineral and deeply aromatic natural wine showing the full complexity of ancient Carignan with dark berry, iron and wild herb intensity.")
if is_new:
    PAIR(prod, "Grilled sardines with peppers and olive oil", "complement", "established", "main", "Old-vine Carignan's mineral freshness and iron notes suit chargrilled sardines with Mediterranean simplicity.")
    PAIR(prod, "Boquerones (marinated anchovies) with sourdough", "complement", "established", "casual", "Saline anchovy intensity and natural Carignan mineral edge create a vivid Catalan coastal pairing.")
    PAIR(prod, "Rabbit with olives and preserved lemon", "complement", "established", "main", "Transparent, mineral Carignan suits delicate braised rabbit with olive brine and lemon brightness.")
    PAIR(prod, "Charcuterie with fuet and pan con tomate", "complement", "classic", "casual", "Catalan cured meats and tomato bread find their natural companion in this old-vine natural Roussillon red.")

prod, is_new = PROD("Clos du Rouge Gorge L'Ubac Blanc", "wine_still", p2, r, "France",
    subcategory="white", price_tier="ultra_premium",
    description="Rare natural white from old-vine Grenache Gris and Macabeu in Roussillon; textured, oxidative and mineral with stone fruit, almond and sea-mineral complexity.")
if is_new:
    PAIR(prod, "Grilled John Dory with olive oil and fresh herbs", "complement", "established", "main", "Oxidative, mineral Roussillon white suits the delicate, sweet flesh of John Dory with Provençal herbs.")
    PAIR(prod, "Jamón ibérico de bellota with Manchego", "complement", "classic", "casual", "Catalan border food culture — cured Iberian ham and aged sheep cheese — meets this textured natural white.")
    PAIR(prod, "Clams with sherry, garlic and parsley", "complement", "established", "main", "Oxidative mineral white bridges the briny ocean clam and the nuttiness of dry sherry in the sauce.")
    PAIR(prod, "Aged goat cheese with lavender honey", "complement", "established", "cheese", "Almond-oxidative natural white mirrors aged goat cheese complexity with lavender-honey sweetness.")

# ── COLLIOURE AOC (France) ────────────────────────────────────────────────────
print("=== Collioure AOC ===")
r = R("Collioure AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Collioure AOC",
      reputation_tier="respected",
      quality_trajectory="established",
      description="Dramatic coastal appellation in the Roussillon, where terraced vineyards cling to schist slopes above the Mediterranean. Collioure produces powerful, structured red and rosé wines from Grenache, Syrah and Mourvèdre alongside the appellation's historic fortified Banyuls wines from the same terroir.",
      key_producers="Domaine de la Rectorie, Domaine du Mas Blanc, Clos des Paulilles",
      historical_context="Collioure became France's first AOC for table wines from Roussillon in 1949. The dramatic schist terraces carved by hand over centuries represent a unique viticultural heritage. The coastal vineyards' combination of Mediterranean sun, sea breeze and thin schist soils produces wines of remarkable concentration and mineral intensity.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Heat and coastal wind produced concentrated, structured reds of extraordinary depth on schist."),
    (2019, "very_good", "stable", "Balanced vintage with characteristic coastal freshness maintaining Collioure's mineral identity."),
    (2020, "very_good", "stable", "Warm, concentrated vintage; schist terraces produced intense, sun-drenched reds and rosés."),
    (2021, "good", "stable", "Cooler conditions; elegant, approachable wines with freshness unusual for the appellation."),
    (2022, "excellent", "rising", "Classic Collioure vintage; schist mineral intensity with concentrated fruit and garrigue depth."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine de la Rectorie", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Marc and Thierry Parcé at Domaine de la Rectorie are the leading producers of both Collioure and Banyuls, farming old-vine schist terraces by hand to produce wines of distinctive mineral power and Mediterranean concentration.",
       reputation_narrative="The defining domaine for understanding Collioure's potential for serious terroir wine, Rectorie produces both the appellation's most powerful reds and its most profound Banyuls Vins Doux Naturels.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Rectorie Collioure Rouge Coume Pascole", "wine_still", p1, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Flagship Collioure from old-vine Grenache on coastal schist; powerful, mineral and deeply aromatic with dark berry, garrigue and sea-salt character. Long aging potential on the schist terraces.")
if is_new:
    PAIR(prod, "Grilled rack of lamb with tapenade and olive oil", "complement", "classic", "main", "Schist-mineral Grenache is the defining regional partner for lamb with the olive depth of tapenade.")
    PAIR(prod, "Braised wild boar with olives, orange peel and thyme", "complement", "established", "main", "Mediterranean game preparation echoes the garrigue and dark fruit intensity of Collioure's old-vine reds.")
    PAIR(prod, "Anchois de Collioure with sourdough and butter", "complement", "classic", "casual", "The appellation's famous salted anchovies with their intense ocean depth are natural with Collioure rouge.")
    PAIR(prod, "Catalan black rice with squid ink and garlic aioli", "bridge", "established", "main", "Mineral schist Grenache bridges the deep umami of squid ink rice and the richness of aioli.")

prod, is_new = PROD("Rectorie Collioure Rosé l'Argile", "wine_still", p1, r, "France",
    subcategory="rosé", price_tier="premium",
    description="Powerful Collioure rosé from Grenache on coastal schist; structured, mineral and deeply expressive with red berry, garrigue and salt character far from typical Provence rosé.")
if is_new:
    PAIR(prod, "Bouillabaisse with rouille and garlic toasts", "complement", "classic", "main", "Structured Mediterranean rosé is the classic companion for Provence's most celebrated fish stew.")
    PAIR(prod, "Catalan suquet de peix (coastal fish stew)", "complement", "classic", "main", "Collioure's coastal fish stew tradition demands the mineral rosé of its own schist-terraced appellation.")
    PAIR(prod, "Grilled red mullet with fennel and lemon", "complement", "established", "main", "Mineral, garrigue-inflected rosé suits the distinctive flavour of red mullet with its coastal herb seasoning.")
    PAIR(prod, "Brandade with black olives and capers", "complement", "established", "casual", "Salt cod purée and olive-caper brine find the right mineral frame in this structured Collioure rosé.")

p2 = P("Domaine du Mas Blanc", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Historic Collioure estate founded by André Parcé, pioneer of modern Roussillon and Banyuls quality. Domaine du Mas Blanc continues traditional schist viticulture with hand-harvested Grenache and Mourvèdre to produce structured, age-worthy wines.",
       reputation_narrative="The founding family of modern Collioure winemaking, Domaine du Mas Blanc established the quality foundation on which all subsequent Collioure producers have built.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Mas Blanc Collioure Les Junquets Rouge", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Classic Collioure from Mourvèdre, Grenache and Syrah on schist; structured, earthy and mineral with coastal garrigue character and genuine aging potential.")
if is_new:
    PAIR(prod, "Slow-braised lamb shoulder with harissa and preserved lemon", "complement", "classic", "main", "Mourvèdre-dominant Collioure matches North African-spiced slow lamb with its structured mineral depth.")
    PAIR(prod, "Grilled merguez with roasted peppers and hummus", "complement", "established", "casual", "Spiced Catalan-influenced flavours find a natural companion in structured Collioure Mourvèdre blend.")
    PAIR(prod, "Thon à la catalane (Catalan tuna stew with olives)", "complement", "established", "main", "Rich Mediterranean tuna preparation is a natural companion to powerful coastal Collioure rouge.")
    PAIR(prod, "Manchego and Idiazabal selection with quince", "complement", "established", "cheese", "Catalan-Spanish border sheep cheeses mirror the garrigue-mineral depth of Collioure's coastal reds.")

prod, is_new = PROD("Mas Blanc Collioure Les Piloums Blanc", "wine_still", p2, r, "France",
    subcategory="white", price_tier="premium",
    description="Rare Collioure blanc from Grenache Gris and Grenache Blanc on coastal schist; mineral, textured and aromatic with stone fruit, almond and Mediterranean herb character.")
if is_new:
    PAIR(prod, "Grilled sea bass with Catalan romesco sauce", "complement", "classic", "main", "Mineral Collioure blanc suits sea bass with the complex pepper-almond-tomato depth of romesco.")
    PAIR(prod, "Salt-crusted turbot with virgin olive oil and herbs", "complement", "classic", "main", "Textured, mineral schist white suits the delicate sweet flesh of whole salt-crusted turbot.")
    PAIR(prod, "Grilled langoustines with garlic and herb butter", "complement", "established", "main", "Stone fruit and mineral Collioure blanc elevate the sweetness of langoustines with herb-butter richness.")
    PAIR(prod, "Salade de poulpe (octopus salad with potatoes and olives)", "complement", "established", "casual", "Mineral coastal white suits the Mediterranean simplicity of octopus salad with olive and potato.")

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
print("B136 complete.")
conn.close()
