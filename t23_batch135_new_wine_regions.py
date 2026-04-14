#!/usr/bin/env python3
"""B135 — Palette AOC (France), Jurançon AOC (France), Irouléguy AOC (France),
   Baga DOC (Portugal), Vinho Verde DOC (Portugal)"""
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

# ── PALETTE AOC (France) ──────────────────────────────────────────────────────
print("=== Palette AOC ===")
r = R("Palette AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Palette AOC",
      reputation_tier="prestigious",
      quality_trajectory="established",
      description="Tiny appellation near Aix-en-Provence producing complex, age-worthy red, white and rosé wines from old limestone vineyards. Dominated by Château Simone, the sole domaine holding most of the appellation's land. Whites from Clairette show remarkable longevity.",
      key_producers="Château Simone, Château Crémade",
      historical_context="One of France's smallest AOCs, established 1948. Château Simone has shaped the appellation's identity for over 200 years. The chalky limestone of the Palette basin creates unique terroir in Provence.")
for yr, qd, pt, sn in [
    (2018, "exceptional", "stable", "Cool nights preserved acidity in an otherwise warm year; whites of extraordinary tension."),
    (2019, "excellent", "rising", "Balanced warmth produced rich reds with fine structure; whites aromatically expressive."),
    (2020, "very_good", "stable", "Early harvest under heat stress; wines of concentration but requiring careful selection."),
    (2021, "good", "stable", "Challenging vintage; lighter reds, crisp whites showing delicate floral character."),
    (2022, "excellent", "rising", "Warm vintage with concentrated fruit; Clairette whites show honeyed complexity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Château Simone", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Château Simone uses extended maceration, large old foudres, and minimal intervention to produce wines of extraordinary age-worthiness from Palette's chalky limestone. The estate's white Clairette-based blend can age 20+ years.",
       reputation_narrative="The defining domaine of Palette AOC, Château Simone has produced wines from this tiny limestone appellation since the 18th century. Its whites are among Provence's most singular and age-worthy.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Château Simone Palette Blanc", "wine_still", p1, r, "France",
    subcategory="white", price_tier="ultra_premium",
    description="Powerful, mineral Provençal white from Clairette, Grenache Blanc and ancient varieties on chalk-limestone. Honeyed and nutty with age, built to last decades.")
if is_new:
    PAIR(prod, "Bouillabaisse with rouille and gruyère croûtons", "complement", "classic", "main", "Limestone minerality and Clairette richness match the saffron-fennel depth of classic bouillabaisse.")
    PAIR(prod, "Roasted chicken with herbes de Provence and olives", "complement", "classic", "main", "Provençal herbal wine aligns with the aromatic garlic-herb profile of the roast.")
    PAIR(prod, "Aged Comté or Beaufort cheese", "complement", "established", "cheese", "Nutty, oxidative white wine character bridges perfectly with aged alpine cheeses.")
    PAIR(prod, "Langoustine bisque with cream and tarragon", "elevate", "established", "main", "Chalk-driven mineral edge lifts the richness of crustacean bisque into elegance.")

prod, is_new = PROD("Château Simone Palette Rouge", "wine_still", p1, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Structured Palette red from Grenache, Mourvèdre and Cinsault aged in large old foudres. Earthy, iron-tinged and deeply complex with exceptional age potential.")
if is_new:
    PAIR(prod, "Daube de boeuf Provençal with olives and orange peel", "complement", "classic", "main", "The iron-earthy red matches the slow-braised beef and olive depth of a classic Provençal daube.")
    PAIR(prod, "Roasted rack of lamb with tapenade crust", "complement", "classic", "main", "Structured Mourvèdre backbone handles the lamb richness while herbal notes echo the tapenade.")
    PAIR(prod, "Wild boar stew with juniper and thyme", "complement", "established", "main", "Rustic garrigue character of Palette rouge aligns with game meat and aromatic herbs.")
    PAIR(prod, "Pissaladière with anchovies and caramelised onion", "bridge", "established", "casual", "Saline anchovy intensity and caramelised sweetness find a bridge in this earthy Grenache blend.")

p2 = P("Château Crémade", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Second major estate of Palette AOC, Château Crémade works with the appellation's chalky limestone terroir and traditional varieties to produce classically structured red and white wines.",
       reputation_narrative="Historic estate sharing Palette AOC's limestone plateau with Château Simone, producing wines of genuine complexity and regional character.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Château Crémade Palette Rouge", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Classic Palette red from Grenache and Mourvèdre on limestone; earthy, structured with Southern French character.")
if is_new:
    PAIR(prod, "Grilled lamb chops with rosemary and fleur de sel", "complement", "classic", "main", "Limestone-structured Grenache-Mourvèdre meets lamb fat and rosemary with Mediterranean harmony.")
    PAIR(prod, "Rabbit with mustard and Provençal herbs", "complement", "established", "main", "Earthy, medium-bodied red suits the delicate richness of braised rabbit with herbal mustard sauce.")
    PAIR(prod, "Ratatouille with aged goat cheese", "complement", "established", "casual", "Provençal vegetable sweetness and goat cheese tang mirror the wine's herbal and earthy notes.")
    PAIR(prod, "Olive-marinated duck breast with polenta", "bridge", "suggested", "main", "Duck richness and olive brine find a bridge in the wine's savoury, mineral-driven profile.")

prod, is_new = PROD("Château Crémade Palette Blanc", "wine_still", p2, r, "France",
    subcategory="white", price_tier="premium",
    description="Mineral, aromatic Palette white from Clairette and Grenache Blanc on limestone; floral and textured with Provençal character.")
if is_new:
    PAIR(prod, "Grilled sea bass with fennel and pastis butter", "complement", "classic", "main", "Clairette's anise-adjacent aromatics mirror the pastis-fennel seasoning of the sea bass.")
    PAIR(prod, "Tapenade bruschetta with fresh ricotta", "complement", "established", "casual", "Mineral white wine cuts through olive oil richness and matches the saline olive depth.")
    PAIR(prod, "Salade Niçoise with grilled tuna and anchovy", "complement", "established", "casual", "Provence-born white with minerality suits the composed salad of tuna, olive, and anchovy.")
    PAIR(prod, "Artichoke with lemon-herb vinaigrette", "bridge", "suggested", "casual", "Clairette's mineral freshness bridges the notoriously wine-difficult artichoke pairing.")

# ── JURANÇON AOC (France) ─────────────────────────────────────────────────────
print("=== Jurançon AOC ===")
r = R("Jurançon AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Jurançon AOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Foothills of the Pyrenees appellation producing both dry (Jurançon Sec) and sweet (Jurançon moelleux) wines from Petit Manseng and Gros Manseng. The passerillage technique—leaving grapes to dry on the vine—concentrates sugars for luscious late-harvest wines.",
      key_producers="Domaine Cauhapé, Clos Uroulat, Clos Guirouilh",
      historical_context="Henry IV of France was reportedly baptised with Jurançon wine. The appellation dates to 1936 as one of France's first. Petit Manseng's thick skins make it uniquely suited to late-harvest passerillage in the Pyrenean climate.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Optimal conditions for passerillage; sweet wines of extraordinary concentration and fresh acidity."),
    (2019, "very_good", "stable", "Warm vintage with good sugar development; dry Manseng wines fragrant and full."),
    (2020, "good", "stable", "Early rains followed by dry autumn; variable quality but fine moelleux from top estates."),
    (2021, "very_good", "stable", "Cool Pyrenean conditions maintained acidity beautifully; elegant Jurançon Sec vintage."),
    (2022, "excellent", "rising", "Late season passerillage conditions produced rich, concentrated sweet wines of precision."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Cauhapé", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Henri Ramonteu at Domaine Cauhapé pioneered the modern Jurançon renaissance, producing the full range from bone-dry Jurançon Sec to ultra-concentrated Noblesse du Temps. His vineyard practices emphasise low yields and late harvesting.",
       reputation_narrative="The leading estate of Jurançon, Henri Ramonteu's Domaine Cauhapé transformed the appellation's reputation from regional curiosity to internationally recognised wine destination.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Cauhapé Noblesse du Temps Jurançon", "wine_still", p1, r, "France",
    subcategory="sweet_white", price_tier="ultra_premium",
    description="Benchmark Jurançon moelleux from late-harvested Petit Manseng with passerillage concentration. Intense tropical fruit and citrus peel with cutting acidity and 20-year aging potential.")
if is_new:
    PAIR(prod, "Foie gras terrine with Sauternes gelée", "complement", "classic", "main", "Sweet Pyrenean wine meets the luxurious richness of foie gras with balanced acidity cutting through fat.")
    PAIR(prod, "Roquefort and walnut with honey drizzle", "contrast", "classic", "cheese", "The wine's tropical sweetness contrasts with sharp blue cheese, creating a tension of sweet-salty complexity.")
    PAIR(prod, "Tarte Tatin with crème fraîche", "complement", "established", "dessert", "Caramelised apple intensity meets passerillage concentration for a perfectly resonant pairing.")
    PAIR(prod, "Pressed duck liver with quince paste", "complement", "established", "main", "Stone fruit and citrus sweetness in the wine echoes and elevates the quince-duck liver combination.")

prod, is_new = PROD("Cauhapé Ballet d'Octobre Jurançon Sec", "wine_still", p1, r, "France",
    subcategory="dry_white", price_tier="premium",
    description="Dry Jurançon from Gros and Petit Manseng; floral, exotic and precise with Pyrenean mineral freshness and citrus-driven finish.")
if is_new:
    PAIR(prod, "Grilled scallops with citrus beurre blanc", "complement", "classic", "main", "Exotic citrus Manseng character elevates the sweet beurre blanc and matches scallop sweetness.")
    PAIR(prod, "Sashimi of sea bream with yuzu dressing", "complement", "established", "main", "Pyrenean mineral freshness and citrus notes are a natural match for citrus-dressed raw fish.")
    PAIR(prod, "Asparagus with hollandaise sauce", "bridge", "established", "casual", "Dry Manseng acidity bridges the hollandaise richness and asparagus's natural wine-challenging bitterness.")
    PAIR(prod, "Chicken breast with morel cream sauce", "elevate", "suggested", "main", "Floral exotic Manseng aromatics elevate the earthy morel cream to new aromatic complexity.")

p2 = P("Clos Uroulat", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Charles Hours at Clos Uroulat produces some of Jurançon's most elegant wines, using traditional techniques and low yields from old Petit Manseng vines to create wines of finesse and longevity.",
       reputation_narrative="Charles Hours's Clos Uroulat is revered for Jurançon wines of exceptional elegance and restraint, particularly the Cuvée Marie moelleux and the dry Clos Uroulat Sec.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Clos Uroulat Cuvée Marie Jurançon", "wine_still", p2, r, "France",
    subcategory="sweet_white", price_tier="ultra_premium",
    description="Elegant passerillage Jurançon from Petit Manseng; honeyed citrus and spice with extraordinary Pyrenean freshness and restraint. Among the most refined moelleux in France.")
if is_new:
    PAIR(prod, "Peach and apricot tarte with cardamom cream", "complement", "classic", "dessert", "Apricot-citrus concentration in the wine mirrors stone fruit tart with spice-cream counterpoint.")
    PAIR(prod, "Époisses cheese with toasted brioche", "contrast", "established", "cheese", "Washed-rind pungency contrasted by the wine's sweet citrus brightness creates memorable tension.")
    PAIR(prod, "Mango and passionfruit pavlova", "complement", "established", "dessert", "Tropical fruit concentration in Petit Manseng aligns with passionfruit's tart-sweet intensity.")
    PAIR(prod, "Smoked salmon with crème fraîche and dill blinis", "bridge", "suggested", "main", "Sweet acidity bridges the smoke and fat of salmon, while citrus notes echo the dill.")

prod, is_new = PROD("Clos Uroulat Jurançon Sec", "wine_still", p2, r, "France",
    subcategory="dry_white", price_tier="premium",
    description="Dry Jurançon from Gros Manseng; fragrant and exotic with white pepper, citrus blossom and clean Pyrenean mineral finish.")
if is_new:
    PAIR(prod, "Grilled langoustines with herb butter", "complement", "classic", "main", "Exotic floral Manseng aromatics elevate grilled langoustine sweetness with mineral precision.")
    PAIR(prod, "Pan-fried foie gras with caramelised quince", "bridge", "established", "main", "Dry Manseng bridges the richness of foie gras and sweetness of quince with bright acidity.")
    PAIR(prod, "Ceviche of white fish with Ají Amarillo", "complement", "established", "casual", "Citrus-forward dry Manseng mirrors the acid-citrus cure and spice of Peruvian ceviche.")
    PAIR(prod, "Courgette flower fritters with lemon aioli", "complement", "suggested", "casual", "Floral wine aromatics echo the delicate squash blossom with citrus-aioli freshness.")

# ── IROULÉGUY AOC (France) ───────────────────────────────────────────────────
print("=== Irouléguy AOC ===")
r = R("Irouléguy AOC", "France", "wine",
      designation_type="AOC",
      designation_name="Irouléguy AOC",
      reputation_tier="overlooked",
      quality_trajectory="ascending",
      description="France's smallest and most westerly appellation in the Basque Pyrenees, producing red, white and rosé wines from Tannat, Cabernet Franc, Cabernet Sauvignon, and Petit Courbu. Steep terraced vineyards on slate and sandstone deliver wines of rugged mountain character.",
      key_producers="Domaine Arretxea, Domaine Ilarria, Cave Coopérative d'Irouléguy",
      historical_context="Irouléguy wine history dates to monks of the Roncevaux Abbey in the 11th century. The appellation was established 1970. Its position in the Basque Country between France and Spain gives it a unique cultural and viticultural identity.")
for yr, qd, pt, sn in [
    (2018, "excellent", "stable", "Mountain vintage with ideal ripening; Tannat achieved rare suppleness alongside structure."),
    (2019, "very_good", "stable", "Warm conditions produced ripe, full-bodied reds with characteristic Pyrenean freshness."),
    (2020, "good", "stable", "Challenging with heat and drought; wines concentrated but some lacking freshness."),
    (2021, "very_good", "stable", "Cool mountain conditions produced bright, aromatic wines of excellent acid-fruit balance."),
    (2022, "excellent", "rising", "Outstanding ripening extended into October; Tannat of exceptional depth and refinement."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Domaine Arretxea", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Michel and Thérèse Riouspeyrous farm biodynamically in the steep Pyrenean vineyards of Irouléguy, working with Tannat, Cabernet Franc, and Petit Courbu to produce mountain wines of remarkable freshness and mineral tension.",
       reputation_narrative="The benchmark estate for understanding Irouléguy's potential for fine wine, Domaine Arretxea produces wines that challenge the perception of Tannat as merely a rough, heavy variety.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Arretxea Irouléguy Rouge Haitza", "wine_still", p1, r, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Benchmark Irouléguy rouge from old Tannat and Cabernet Franc on steep slate terraces. Mineral, dark-fruited and structured with Pyrenean freshness and a decade of aging potential.")
if is_new:
    PAIR(prod, "Axoa de veau (Basque veal stew with Espelette pepper)", "complement", "classic", "main", "The regional mountain red finds its natural partner in the Basque veal and Espelette spice dish.")
    PAIR(prod, "Grilled côte de boeuf with Basque piperade", "complement", "classic", "main", "Tannat's dark fruit and structure handles the charred beef fat with pepper-tomato piperade.")
    PAIR(prod, "Slow-roasted lamb shoulder with rosemary and garlic", "complement", "established", "main", "Mountain Tannat's firm tannins and dark berry character are classical with slow-roasted lamb.")
    PAIR(prod, "Etorki or Ossau-Iraty sheep cheese", "complement", "established", "cheese", "Local Basque sheep cheese echoes the mountain terroir of this Irouléguy red.")

prod, is_new = PROD("Arretxea Irouléguy Blanc Hegoxuri", "wine_still", p1, r, "France",
    subcategory="white", price_tier="premium",
    description="Rare Irouléguy white from Petit Courbu and Petit Manseng on slate; floral, tense and mineral with mountain freshness and citrus depth.")
if is_new:
    PAIR(prod, "Ttoro (Basque fish stew with saffron and peppers)", "complement", "classic", "main", "Mountain white's mineral freshness cuts through the saffron-rich Basque fish stew.")
    PAIR(prod, "Grilled sea bream with olive oil and fleur de sel", "complement", "established", "main", "Mineral Petit Courbu and citrus tension suit the clean, direct flavours of simply grilled fish.")
    PAIR(prod, "Chèvre frais with honey and toasted hazelnuts", "complement", "established", "casual", "Floral white wine matches fresh goat cheese's tang, balanced by honey sweetness and nut texture.")
    PAIR(prod, "Asparagus mimosa with herb vinaigrette", "bridge", "suggested", "casual", "Mineral freshness and citrus bridge the egg-asparagus combination of the classic French starter.")

p2 = P("Domaine Ilarria", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Peio Espil at Domaine Ilarria farms Tannat and Cabernet Franc on the steep terraced slopes of Irouléguy, using traditional Basque winemaking to produce structured, terroir-driven reds of genuine mountain character.",
       reputation_narrative="One of the finest independent producers in Irouléguy, Domaine Ilarria's reds demonstrate the appellation's capacity for complex, age-worthy Tannat-based wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Domaine Ilarria Irouléguy Rouge", "wine_still", p2, r, "France",
    subcategory="red", price_tier="premium",
    description="Classic Irouléguy rouge from Tannat and Cabernet Franc; dark berry, mineral, structured and authentic Pyrenean mountain red.")
if is_new:
    PAIR(prod, "Magret de canard (duck breast) with Espelette honey glaze", "complement", "classic", "main", "Basque mountain Tannat meets duck richness and the regional spice-honey combination.")
    PAIR(prod, "Cassoulet with Toulouse sausage and duck confit", "complement", "established", "main", "Full-bodied Tannat blend handles the hearty richness of cassoulet with its structured tannins.")
    PAIR(prod, "Grilled Basque chorizo with padron peppers", "complement", "established", "casual", "Spiced cured pork and mild green peppers suit the dark fruit and mountain character of this rouge.")
    PAIR(prod, "Manchego or Idiazabal smoked sheep cheese", "bridge", "suggested", "cheese", "Smoked-spiced sheep cheese from across the Pyrenees bridges the Basque mountain red beautifully.")

prod, is_new = PROD("Domaine Ilarria Irouléguy Blanc", "wine_still", p2, r, "France",
    subcategory="white", price_tier="premium",
    description="Fresh, mineral Irouléguy white from Courbu and Manseng; aromatic, lively and distinctly Basque in character.")
if is_new:
    PAIR(prod, "Pintxos bar — anchovy, olive and pepper skewers", "complement", "classic", "casual", "Fresh Basque white wine is the natural companion to pintxos of anchovy and pickled peppers.")
    PAIR(prod, "Grilled octopus with paprika and aioli", "complement", "established", "casual", "Mineral freshness and citrus cut through smoky octopus char and the richness of aioli.")
    PAIR(prod, "Salt cod (bacalao) with pil-pil sauce", "complement", "established", "main", "Atlantic cod and emulsified olive-garlic pil-pil find balance with the mineral Basque white.")
    PAIR(prod, "Mussels with cider and shallots", "complement", "suggested", "casual", "Briny mussels and apple-cidery brine mirror the coastal-mountain freshness of Irouléguy blanc.")

# ── BAGA DOC (Portugal) ───────────────────────────────────────────────────────
print("=== Baga DOC ===")
r = R("Baga DOC", "Portugal", "wine",
      designation_type="DOC",
      designation_name="Baga DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Bairrada's indigenous Baga grape produces some of Portugal's most demanding and age-worthy reds: high tannin, high acid, and earthy complexity that can achieve transcendence with two or more decades of cellaring. Modern winemakers are taming Baga's rough edges while preserving its distinctive character.",
      key_producers="Luís Pato, Filipa Pato, Casa de Saima, Quinta das Bágeiras",
      historical_context="Bairrada wine production dates to the 18th century. The Baga grape was long dismissed as too tannic but has undergone a revival led by Luís Pato and his daughter Filipa, who demonstrated that careful viticulture and winemaking can produce world-class results from this challenging variety.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool Atlantic conditions produced Baga of exceptional freshness and natural acidity; whites equally brilliant."),
    (2019, "very_good", "stable", "Good balance of fruit and structure; reds showing excellent aging potential from fine tannin."),
    (2020, "good", "stable", "Warm year produced more approachable reds; some wines lacked the traditional Baga austerity."),
    (2021, "excellent", "rising", "Benchmark vintage — cool, long season produced Baga with textbook acid-tannin structure for long aging."),
    (2022, "very_good", "stable", "Ripe but balanced; modern-style Baga with accessible tannins and bright Atlantic freshness."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Luís Pato", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="The patriarch of Bairrada wine, Luís Pato champions native Baga through meticulous single-vineyard work and whole-cluster fermentation, demonstrating that Baga can rival Pinot Noir in complexity when handled with care and given adequate cellaring.",
       reputation_narrative="Luís Pato is the defining figure of Bairrada winemaking. His decades-long advocacy for Baga has transformed how the world perceives Portuguese native varieties.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Luís Pato Vinha Barrosa Baga", "wine_still", p1, r, "Portugal",
    subcategory="red", price_tier="ultra_premium",
    description="Flagship single-vineyard Baga from centenarian vines on sandy-clay soils. Profound depth, high natural acidity and fine tannin structure built for multi-decade cellaring.")
if is_new:
    PAIR(prod, "Leitão da Bairrada (suckling pig with orange and garlic)", "complement", "classic", "main", "The regional classic — crisp Bairrada suckling pig and its citrus-garlic seasoning are inseparable from aged Baga.")
    PAIR(prod, "Roasted partridge with port and mushroom sauce", "complement", "classic", "main", "Earthy, high-acid Baga from sandy soils matches game bird with mushroom and port intensity.")
    PAIR(prod, "Aged Manchego with membrillo quince paste", "complement", "established", "cheese", "Tannic austerity and acidity of aged Baga are tamed by the fat of aged manchego and quince sweetness.")
    PAIR(prod, "Lamb chops with rosemary and charred onion", "complement", "established", "main", "Firm tannins from Baga's thick skins handle charred lamb fat with structured mineral precision.")

prod, is_new = PROD("Luís Pato Baga Maria Gomes Branco", "wine_still", p1, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Crisp Atlantic white from Maria Gomes (Fernão Pires) in Bairrada; floral, citrus-driven with mineral freshness from clay-limestone soils.")
if is_new:
    PAIR(prod, "Grilled sardines with tomato and olive oil salad", "complement", "classic", "casual", "Portugal's most iconic lunch dish meets the crisp Atlantic white of Bairrada in perfect regional harmony.")
    PAIR(prod, "Ameijoas à Bulhão Pato (clams with coriander and garlic)", "complement", "classic", "main", "Garlic-coriander clams and their briny ocean intensity are lifted by crisp mineral Portuguese white.")
    PAIR(prod, "Caldeirada (Portuguese fish stew)", "complement", "established", "main", "Atlantic-freshness white wine mirrors the mixed fish and potato stew of Portuguese coastal tradition.")
    PAIR(prod, "Bacalhau com natas (salt cod with cream gratin)", "complement", "established", "main", "Crisp acidity cuts through the rich cream gratin while complementing the salt cod's ocean depth.")

p2 = P("Filipa Pato", "winery", r, "Portugal",
       production_philosophy="natural",
       philosophy_description="Luís Pato's daughter Filipa brings a modernist, low-intervention philosophy to Bairrada, crafting fresher, more transparent expressions of Baga and Bical that highlight terroir over tradition.",
       reputation_narrative="Filipa Pato represents the next generation of Bairrada excellence, applying natural winemaking philosophies to indigenous varieties with outstanding results recognised internationally.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Filipa Pato Nossa Calcário Baga", "wine_still", p2, r, "Portugal",
    subcategory="red", price_tier="premium",
    description="Natural-winemaking Baga from limestone parcels; lighter, more transparent and more immediately approachable than traditional Bairrada style with vivid raspberry and earth character.")
if is_new:
    PAIR(prod, "Duck rice (arroz de pato) with orange and olives", "complement", "classic", "main", "Lighter limestone-driven Baga pairs beautifully with duck rice's rich fat balanced by orange and olive.")
    PAIR(prod, "Pork secreto with almond and orange salad", "complement", "established", "main", "Transparent Baga with fresh acidity suits the unctuousness of Iberian secreto with citrus brightness.")
    PAIR(prod, "Mushroom and truffle risotto", "complement", "established", "main", "Earthy transparency of limestone Baga elevates mushroom and truffle's forest floor complexity.")
    PAIR(prod, "Lentil and chorizo stew with smoked paprika", "complement", "suggested", "casual", "Natural acidity and earthy Baga character cuts through hearty lentil-chorizo richness.")

prod, is_new = PROD("Filipa Pato Bical White Bairrada", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Native Bical white from Bairrada; crisp, floral and mineral with natural winemaking transparency and Atlantic freshness.")
if is_new:
    PAIR(prod, "Percebes (goose barnacles) with lemon", "complement", "classic", "casual", "Bical's mineral Atlantic freshness is the classic Iberian companion to the ocean intensity of percebes.")
    PAIR(prod, "Ceviche of sea bass with coriander and lime", "complement", "established", "casual", "Floral, citrus-driven Bical mirrors the lime-herb freshness of acid-cured raw fish perfectly.")
    PAIR(prod, "Ovos verdes (green eggs with coriander)", "complement", "established", "casual", "Crisp natural white wine lifts and complements this simple, herbal Portuguese egg dish.")
    PAIR(prod, "Grilled calamari with piri-piri and lemon", "complement", "suggested", "casual", "Mineral Bical freshness suits grilled squid with the brightness to handle piri-piri heat.")

# ── VINHO VERDE DOC (Portugal) ────────────────────────────────────────────────
print("=== Vinho Verde DOC ===")
r = R("Vinho Verde DOC", "Portugal", "wine",
      designation_type="DOC",
      designation_name="Vinho Verde DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Northwestern Portugal's vast appellation producing light, high-acid wines with characteristic slight effervescence from Atlantic-influenced granitic and schist soils. While long associated with cheap semi-sweet brands, the single-varietal Alvarinho and Loureiro sub-regions produce world-class dry whites of precision and freshness.",
      key_producers="Quinta do Crasto, Quinta de Soalheiro, Anselmo Mendes",
      historical_context="Vinho Verde wine culture dates to Roman times in the Minho region. The name 'Green Wine' refers not to colour but to youth and freshness. The appellation established 1908 is Portugal's largest DOC. The Monção e Melgaço sub-region for Alvarinho has elevated the appellation's international reputation significantly since 2000.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool Atlantic season produced Alvarinho of outstanding freshness, aromatic complexity and ageability."),
    (2019, "very_good", "stable", "Warm for the north; riper Loureiro and Alvarinho with generous fruit character."),
    (2020, "very_good", "stable", "Balanced year with good acid retention; premium single-varietal wines of precision."),
    (2021, "excellent", "rising", "Cool, long season — benchmark vintage for Monção e Melgaço Alvarinho with mineral tension."),
    (2022, "good", "stable", "Drought stress affected some yields; top sites with irrigation produced fine wines."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Quinta de Soalheiro", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Pioneer of premium Alvarinho in Monção e Melgaço, Quinta de Soalheiro produces single-vineyard and classified Alvarinho that demonstrates the variety's capacity for complexity, mineral depth and aging potential beyond its refreshing youth.",
       reputation_narrative="Quinta de Soalheiro established the benchmark for premium Alvarinho, showing the world that Vinho Verde could produce wines of genuine complexity and international stature.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Soalheiro Alvarinho Primeiras Vinhas", "wine_still", p1, r, "Portugal",
    subcategory="white", price_tier="ultra_premium",
    description="Single-vineyard Alvarinho from old vines in Monção e Melgaço; intense mineral, citrus and stone fruit character with fine salinity and exceptional aging potential for the variety.")
if is_new:
    PAIR(prod, "Grilled turbot with lemon butter and samphire", "complement", "classic", "main", "Mineral Alvarinho precision and salinity elevate turbot with its briny samphire accompaniment.")
    PAIR(prod, "Percebes with rock salt and sea spray", "complement", "classic", "casual", "The saline mineral intensity of old-vine Alvarinho is the quintessential match for Atlantic goose barnacles.")
    PAIR(prod, "Crab with homemade mayonnaise and brown bread", "complement", "established", "casual", "Mineral freshness and stone-fruit Alvarinho lift sweet crab with citrus precision.")
    PAIR(prod, "Lobster bisque with cognac and cream", "elevate", "established", "main", "Mineral depth and salinity of old-vine Alvarinho elevates rich crustacean bisque to exceptional pairing.")

prod, is_new = PROD("Soalheiro Alvarinho Reserva", "wine_still", p1, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Fermented and aged on fine lees, Soalheiro Reserva Alvarinho shows greater texture and complexity while retaining the variety's signature freshness and mineral precision.")
if is_new:
    PAIR(prod, "Bacalhau à Brás (salt cod scrambled with eggs and olives)", "complement", "classic", "main", "Lees-textured Alvarinho with fresh acidity handles the salt cod richness of this iconic Portuguese dish.")
    PAIR(prod, "Grilled barnacles and prawns with garlic butter", "complement", "classic", "casual", "Lees-aged Alvarinho's texture suits garlic-butter shellfish while mineral freshness cuts through fat.")
    PAIR(prod, "Linguine alle vongole with white wine and parsley", "complement", "established", "main", "Wine-and-clam pasta echoes the mineral-saline character of the Alvarinho with satisfying harmony.")
    PAIR(prod, "Seared scallops with cauliflower purée and hazelnut", "elevate", "established", "main", "Lees texture and stone-fruit Alvarinho elevate sweet scallop and nutty cauliflower into elegance.")

p2 = P("Anselmo Mendes", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Anselmo Mendes is one of Portugal's most respected oenologists, working across multiple sub-regions of Vinho Verde with particular focus on single-varietal expressions of Alvarinho and Loureiro that reveal sub-regional terroir differences.",
       reputation_narrative="Known as the 'Alvarinho man', Anselmo Mendes has done more than any other individual to demonstrate the diversity and quality potential of Vinho Verde's sub-regional wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Anselmo Mendes Contacto Alvarinho", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Skin-contact Alvarinho with 24 hours maceration; textured, amber-tinged and broader than classic Alvarinho, showing phenolic interest alongside the variety's signature citrus and mineral character.")
if is_new:
    PAIR(prod, "Octopus à lagareiro with olive oil and potato", "complement", "classic", "main", "Skin-contact Alvarinho texture suits the olive oil richness of this classic octopus dish.")
    PAIR(prod, "Smoked mackerel pâté with pickled cucumber", "complement", "established", "casual", "Textured white wine with phenolic interest matches the oily richness and acidity of smoked fish pâté.")
    PAIR(prod, "Burrata with roasted peppers and anchovies", "complement", "established", "casual", "Skin-contact texture bridges the creaminess of burrata and the saline intensity of anchovy.")
    PAIR(prod, "Braised octopus with black olives and tomato", "complement", "suggested", "main", "Phenolic Alvarinho texture stands up to long-braised octopus with Mediterranean olive and tomato.")

prod, is_new = PROD("Anselmo Mendes Loureiro Vinho Verde", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="mid_range",
    description="Single-varietal Loureiro from Vinho Verde; floral, aromatic and light with peach blossom, lemon and a characteristic refreshing spritz of natural CO2.")
if is_new:
    PAIR(prod, "Salade Niçoise with grilled sardines", "complement", "established", "casual", "Light floral Loureiro freshness suits the composed salad with its grilled sardine and olive complexity.")
    PAIR(prod, "Steamed clams with white wine, garlic and coriander", "complement", "classic", "casual", "Classic Minho pairing — floral Loureiro mirrors the briny clam steam with coriander brightness.")
    PAIR(prod, "Rissóis de camarão (Portuguese prawn pastries)", "complement", "established", "casual", "Light, aromatic Loureiro freshness complements the fried pastry and prawn filling perfectly.")
    PAIR(prod, "Prosciutto and melon with fresh mint", "complement", "suggested", "casual", "Floral spritz of Loureiro echoes melon sweetness and cuts prosciutto salt with refreshing ease.")

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
print("B135 complete.")
conn.close()
