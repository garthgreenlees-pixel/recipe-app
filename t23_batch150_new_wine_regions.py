#!/usr/bin/env python3
"""B150 — Bierzo DO (Spain), Toro DO (Spain), Gigondas AOC (France), Vacqueyras AOC (France), Corbières AOC (France)"""
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Bierzo DO ─────────────────────────────────────────────────────────────
print("=== Bierzo DO ===")
r1 = R("Bierzo DO", "Spain", "wine",
        designation_type="DO", designation_name="Bierzo",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Bierzo, in the northwest Spanish province of León, is home to the Mencía grape — a variety of extraordinary elegance and aromatic complexity that produces wines bearing comparison to Burgundy's Pinot Noir. Grown on the steep, slate and granite slopes of the Bierzo valley, Mencía delivers floral red fruit, mineral depth, and a silky texture that is unlike any other Spanish red.",
        key_producers="Descendientes de J. Palacios, Raúl Pérez (Bodegas Castro Ventosa), Dominio de Tares, Pittacum",
        historical_context="Bierzo sits at the confluence of Atlantic and Mediterranean climates, sheltered by mountains on three sides. Its Mencía vines, some of them 80 or more years old, survived the phylloxera era through relative isolation. The region's modern renaissance was sparked when Álvaro Palacios and his nephew Ricardo Pérez Palacios arrived in 2000, releasing their Pétalos and La Faraona wines that transformed Bierzo into one of Spain's most exciting regions overnight.")

for yr, qd, pt in [
    (2018, "excellent", "rising"), (2019, "exceptional", "rising"), (2020, "very_good", "stable"),
    (2021, "excellent", "rising"), (2022, "very_good", "rising")]:
    VIN(r1, yr, qd, pt)

p1a = P("Descendientes de J. Palacios", "winery", r1, "Spain",
         production_philosophy="minimal_intervention",
         philosophy_description="Álvaro Palacios and Ricardo Pérez Palacios established this estate in Bierzo's Valtuille de Abajo village in 2000, applying their Priorat philosophy of terroir expression and minimal intervention to Mencía on ancient slate slopes. Their La Faraona is one of Spain's most coveted wines.",
         reputation_narrative="Descendientes de J. Palacios transformed Bierzo's international reputation with Pétalos and their single-vineyard wines, demonstrating that Mencía could produce wines of Burgundian elegance and depth. La Faraona is one of Spain's rarest and most sought-after wines.",
         price_positioning="ultra_premium")

prod1a1, new1 = PROD("Descendientes de J. Palacios Pétalos del Bierzo", "wine_still", p1a, r1, "Spain",
                      subcategory="Mencía", price_tier="mid_range",
                      description="The gateway wine to the Palacios Bierzo portfolio, Pétalos is an accessible but serious Mencía blending fruit from old slate-soil vines across the Bierzo valley. Wild cherry, violet, and earthy mineral with a silky texture and a long, fresh finish — a wine that has introduced Mencía to wine lovers worldwide.")
if new1:
    PAIR(prod1a1, "Grilled lamb chops with herbs and roasted peppers", "complement", "classic", "main", "Bierzo Mencía's floral lift and earthy mineral character are natural companions for grilled lamb; herbs echo the wine's aromatic complexity while roasted peppers add the sweetness that softens its tannin.")
    PAIR(prod1a1, "Pulpo a feira (Galician octopus with paprika and olive oil)", "complement", "classic", "starter", "The northwest Spanish pairing: Mencía's mineral freshness and cherry character complement octopus with paprika; the wine's moderate tannin is perfectly calibrated for the dish's tender texture.")
    PAIR(prod1a1, "Wild mushroom and chestnuts with thyme on toasted bread", "complement", "established", "starter", "Pétalos's earthy, forest-floor character resonates with wild mushrooms and chestnuts; thyme echoes the wine's herbal depth while the toast provides the starchy foil.")
    PAIR(prod1a1, "Empanada gallega (tuna and vegetable pastry)", "complement", "established", "casual", "Northwest Spain's most iconic pastry and Bierzo Mencía is a regional classic; the empanada's savoury filling and pastry richness are balanced by the wine's bright acidity and silky tannin.")

prod1a2, new2 = PROD("Descendientes de J. Palacios Las Lamas Bierzo", "wine_still", p1a, r1, "Spain",
                      subcategory="Mencía", price_tier="ultra_premium",
                      description="From one of Bierzo's most celebrated old-vine plots on steep slate soils in Valtuille de Abajo, Las Lamas is one of Spain's great single-vineyard wines: profound, mineral, and long-lived, with the precision and transparency of great Burgundy applied to old-vine Mencía.")
if new2:
    PAIR(prod1a2, "Roasted rack of lamb with Bierzo slate mineral sauce", "complement", "classic", "main", "Las Lamas's slate-mineral depth and concentration demand this level of preparation; the wine's precision and elegance echo the finest Burgundian lamb pairings translated to Spain.")
    PAIR(prod1a2, "Venison loin with wild mushroom jus and celeriac purée", "complement", "established", "main", "The wine's old-vine depth and mineral precision find their most natural expression with game; wild mushroom deepens the earthy connection while celeriac provides the textural base the wine's structure demands.")
    PAIR(prod1a2, "Wild boar terrine with pickled vegetables and sourdough", "complement", "established", "starter", "Las Lamas's complexity and structure can navigate the intensity of wild boar even in terrine form; pickled vegetables provide the acidity contrast that keeps the sophisticated pairing alive.")
    PAIR(prod1a2, "Aged Manchego with truffle and walnut", "complement", "established", "cheese", "The wine's mineral depth and old-vine concentration demand an aged hard cheese; truffle deepens the earthy mineral resonance while walnut adds the savoury bitterness that extends the finish.")

p1b = P("Dominio de Tares", "winery", r1, "Spain",
         production_philosophy="terroir_expression",
         philosophy_description="Dominio de Tares is one of Bierzo's most consistent producers, focusing exclusively on the region's indigenous Mencía grape across a range of single-vineyard and appellation-wide expressions.",
         reputation_narrative="Dominio de Tares has been a reliable standard-bearer for Bierzo quality, demonstrating consistent excellence across vintages and price points that have built loyalty among sommeliers and collectors throughout Europe and North America.",
         price_positioning="mid_range")

prod1b1, new3 = PROD("Dominio de Tares Bembibre Mencía Bierzo", "wine_still", p1b, r1, "Spain",
                      subcategory="Mencía", price_tier="mid_range",
                      description="From the ancient hill town of Bembibre, one of Bierzo's most historic wine villages, this single-village Mencía displays the concentrated mineral character of the appellation's finest terroirs: cherry, violet, herbs, and slate with firm structure that rewards 5-8 years of cellaring.")
if new3:
    PAIR(prod1b1, "Slow-roasted leg of lamb with garlic and rosemary", "complement", "classic", "main", "Bembibre Mencía's structure and mineral depth are well-matched to roasted lamb; rosemary echoes the wine's herb character while garlic adds the savoury depth that bridges meat and wine.")
    PAIR(prod1b1, "Sopa de ajo (Castilian garlic soup) with poached egg", "complement", "established", "starter", "Northwest Spain's most warming dish finds resonance with Bierzo Mencía's earthy character; the poached egg adds richness while the soup's pimentón echoes the wine's red-fruit depth.")
    PAIR(prod1b1, "Grilled ribeye with chimichurri and roasted potatoes", "complement", "classic", "main", "The wine's structure and minerality are well-matched to grilled beef; chimichurri's herb freshness provides the bright contrast while potatoes absorb the rich drippings.")
    PAIR(prod1b1, "Tetilla cheese with membrillo and walnuts", "complement", "established", "cheese", "Galicia's most beloved mild fresh cheese is a local companion for Bierzo Mencía; membrillo bridges the wine's fruit while walnuts add the earthy depth that extends the finish.")

prod1b2, new4 = PROD("Dominio de Tares P3 Mencía Bierzo", "wine_still", p1b, r1, "Spain",
                      subcategory="Mencía", price_tier="premium",
                      description="P3 is Dominio de Tares's single-vineyard flagship, from their finest Bierzo hillside parcel. Old-vine Mencía of impressive depth and mineral complexity, with concentrated cherry, violet, and a long slate-mineral finish that defines what Bierzo can achieve at the highest level.")
if new4:
    PAIR(prod1b2, "Suckling pig (cochinillo) slow-roasted with herbs", "complement", "established", "main", "Bierzo's finest Mencía and slow-roasted cochinillo is a Castilian celebration pairing; the wine's structure and mineral depth can navigate the suckling pig's rich skin and tender flesh.")
    PAIR(prod1b2, "Wild hare stew with mushrooms and herbs (liebre en escabeche)", "complement", "established", "main", "The wine's earthy depth and mineral precision are natural companions for wild hare; escabeche's vinegar note echoes the wine's acidity while mushrooms amplify its forest-floor character.")
    PAIR(prod1b2, "Aged Zamorano cheese with black truffle honey and hazelnuts", "complement", "established", "cheese", "P3's mineral depth and old-vine concentration find resonance with aged Castilian sheep's cheese; black truffle honey bridges the wine's earthy character while hazelnuts add savoury depth.")
    PAIR(prod1b2, "Duck magret with cherries and aged balsamic reduction", "complement", "classic", "main", "Duck magret's richness and cherry reduction create a direct flavour bridge with the wine's cherry character; aged balsamic adds the sweet-sour depth that echoes Mencía's natural acidity.")

# ── 2. Toro DO ───────────────────────────────────────────────────────────────
print("=== Toro DO ===")
r2 = R("Toro DO", "Spain", "wine",
        designation_type="DO", designation_name="Toro",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Toro, on the banks of the River Duero in western Spain, produces some of the country's most powerful and concentrated red wines from the ancient Tinta de Toro grape — a local variation of Tempranillo adapted to the region's extreme continental climate. Old, ungrafted bush vines on sandy soils that survived the phylloxera epidemic produce wines of extraordinary intensity, dark fruit, and robust structure.",
        key_producers="Numanthia, Pintia (Vega Sicilia), Quinta de la Quietud, Dominio del Bendito, Bodegas Toresanas",
        historical_context="Toro's wine history extends to the 12th century, when the region supplied wine to the Spanish royal court. The sandy soils that saved vines from phylloxera, combined with the harsh continental climate (scorching summers, freezing winters), produce vines that stress to yield tiny, intensely flavoured grapes. The modern era was marked by Vega Sicilia's establishment of Pintia in the late 1990s, which validated Toro's world-class potential and sparked a wave of investment.")

for yr, qd, pt in [
    (2016, "exceptional", "rising"), (2017, "excellent", "rising"), (2018, "very_good", "stable"),
    (2019, "exceptional", "rising"), (2020, "excellent", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Numanthia", "winery", r2, "Spain",
         production_philosophy="terroir_expression",
         philosophy_description="Numanthia was founded in 1998 by the Eguren family (of Muga and Sierra Cantabria fame) to produce world-class Toro from ancient ungrafted vines. Their Termanthia, from a single vineyard of 120-year-old vines, is considered Toro's greatest wine and one of Spain's most collected.",
         reputation_narrative="Numanthia's acquisition by LVMH in 2008 brought global investment and recognition to Toro, while Termanthia's 100-point score from Robert Parker in 2002 placed the region on the world wine map overnight. The estate remains Toro's benchmark for concentrated, age-worthy power.",
         price_positioning="ultra_premium")

prod2a1, new5 = PROD("Numanthia Termanthia Toro", "wine_still", p2a, r2, "Spain",
                      subcategory="Tinta de Toro", price_tier="ultra_premium",
                      description="From a single plot of 120-year-old ungrafted Tinta de Toro vines, Termanthia is one of Spain's most profound red wines: extraordinary concentration, dense dark fruit, earth, and spice with fine-grained tannin that belies the wine's immense power. Ageable for 30+ years.")
if new5:
    PAIR(prod2a1, "Slow-roasted Toro suckling lamb (lechazo asado) in wood oven", "complement", "classic", "main", "Termanthia's power and concentration are the definitive match for Castilian wood-oven roasted lamb; the wine's dark fruit and structure navigate the milk-fed lamb's tenderness while the wood smoke adds a complementary depth.")
    PAIR(prod2a1, "Dry-aged prime rib with bone marrow and garlic", "complement", "classic", "main", "One of Spain's greatest wines demands one of beef's most luxurious preparations; bone marrow's richness and garlic's depth create the savoury anchor the wine's power demands.")
    PAIR(prod2a1, "Braised oxtail with spiced dark sauce and potato purée", "complement", "classic", "main", "Toro's rabo de toro is the region's signature braised dish; Termanthia's concentrated power and dark fruit navigate the rich, sticky sauce while potato purée softens the wine's massive tannin.")
    PAIR(prod2a1, "Aged Manchego Gran Reserva with Ibérico ham", "complement", "classic", "cheese", "Spain's greatest wine with its greatest charcuterie and aged sheep's cheese: this triumvirate of Spanish luxury products creates a pairing of extraordinary cultural and sensory coherence.")

prod2a2, new6 = PROD("Numanthia Numanthia Toro", "wine_still", p2a, r2, "Spain",
                      subcategory="Tinta de Toro", price_tier="premium",
                      description="The estate's second wine, Numanthia draws on younger vines from the same Toro vineyards as Termanthia. The wine delivers a more accessible interpretation of Toro's power: concentrated dark fruit, dark chocolate, and earth with robust tannin that still requires patience.")
if new6:
    PAIR(prod2a2, "Cocido castellano (chickpea and meat stew)", "complement", "classic", "main", "The hearty Castilian stew demands a wine of matching intensity; Numanthia's dark fruit and robust structure navigate the stew's rich broth and varied meats while the chickpeas absorb the wine's tannin.")
    PAIR(prod2a2, "Slow-cooked lamb shoulder with garlic and thyme", "complement", "classic", "main", "The wine's dark concentration and earthy power are ideal for slow-cooked lamb; garlic and thyme add the savoury-herbal complexity that bridges the wine's own aromatic character.")
    PAIR(prod2a2, "Grilled Ibérico pork secreto with black garlic aioli", "complement", "established", "main", "Ibérico pork's extraordinary marbling and the wine's concentration create a premium Castilian pairing; black garlic aioli adds the umami depth that bridges meat and wine while amplifying Numanthia's dark intensity.")
    PAIR(prod2a2, "Aged Leonés cheese with quince paste and Ibérico lard", "complement", "established", "cheese", "The wine's power demands aged hard cheese from the region; quince paste bridges its dark fruit while Ibérico lard's extraordinary flavour creates a uniquely Spanish luxury in the combination.")

p2b = P("Pintia Bodegas Toro", "winery", r2, "Spain",
         production_philosophy="classical",
         philosophy_description="Pintia is Vega Sicilia's Toro venture, established in 2001 to apply the legendary Ribera del Duero producer's philosophy of extreme quality and longevity to Toro's ancient Tinta de Toro vines. The wine is made with the same obsession for quality as Vega Sicilia's Unico.",
         reputation_narrative="Vega Sicilia's investment in Toro through Pintia was a defining moment for the appellation, confirming its world-class potential. The wine's restrained power relative to other Toro wines reflects Vega Sicilia's house style of elegance within concentration.",
         price_positioning="ultra_premium")

prod2b1, new7 = PROD("Pintia Toro", "wine_still", p2b, r2, "Spain",
                      subcategory="Tinta de Toro", price_tier="ultra_premium",
                      description="Vega Sicilia's Toro wine, made with the house's legendary attention to quality and restraint. Pintia displays more elegance than many Toro wines: dense but not heavy, with dark cherry, spice, and fine-grained tannin that reflects Vega Sicilia's philosophy of power in balance.")
if new7:
    PAIR(prod2b1, "Whole-roasted suckling lamb with Ibérico ham and herbs", "complement", "classic", "main", "Pintia's restrained power and Vega Sicilia elegance demand the finest Castilian table preparation; Ibérico ham's complexity and the lamb's tenderness create a luxury that matches the wine's stature.")
    PAIR(prod2b1, "Grilled Ibérico pluma with Pedro Ximénez reduction", "complement", "classic", "main", "Ibérico pork's extraordinary fat content and the wine's dark cherry depth are natural Spanish companions; PX reduction's sweetness bridges the wine's fruit while the pork's richness is framed by its tannin.")
    PAIR(prod2b1, "Wild mushroom and truffle risotto with Manchego", "complement", "established", "main", "Pintia's restrained Vega Sicilia character finds an unusual but compelling match in truffle risotto; Manchego's nuttiness adds local Spanish character while the risotto's creaminess softens the tannin.")
    PAIR(prod2b1, "Aged Manchego with Ibérico ham and spiced membrillo", "complement", "classic", "cheese", "The quintessential Spanish luxury combination: Pintia's power and elegance bridge Manchego's richness and Ibérico's complexity; spiced membrillo adds the fruit note that mirrors the wine's dark-cherry depth.")

prod2b2, new8 = PROD("Bodegas Toresanas Idus de Toro", "wine_still", p2b, r2, "Spain",
                      subcategory="Tinta de Toro", price_tier="mid_range",
                      description="An accessible expression of Toro's character from the valley's historic old-vine Tinta de Toro, displaying the region's distinctive combination of power and dark fruit in a slightly softer frame that allows enjoyment without extended cellaring.")
if new8:
    PAIR(prod2b2, "Lamb and vegetable stew with Castilian bread", "complement", "classic", "main", "A classic everyday Toro pairing: the wine's dark fruit and medium tannin complement lamb stew without overwhelming its rustic simplicity; Castilian bread absorbs the stew's richness.")
    PAIR(prod2b2, "Grilled chorizo with roasted peppers and garlic", "complement", "classic", "casual", "Toro's accessible expression with grilled chorizo is the Spanish barbecue classic; the sausage's paprika and pork fat find traction against the wine's dark fruit while roasted peppers add sweetness.")
    PAIR(prod2b2, "Migas castellanas with fried egg, chorizo, and grapes", "complement", "established", "main", "Migas is one of Castile's most traditional dishes; the grapes' sweetness in this combination echoes Toro's dark-fruit character while chorizo's spice and egg's richness create the full savouriness the wine demands.")
    PAIR(prod2b2, "Tetilla and Manchego cheese board with sobrasada", "complement", "established", "cheese", "A Spanish regional cheese board with sobrasada's soft spiced pork creates a pairing where the wine's tannin cuts through the fat while its dark fruit bridges the paprika spice.")

# ── 3. Gigondas AOC ──────────────────────────────────────────────────────────
print("=== Gigondas AOC ===")
r3 = R("Gigondas AOC", "France", "wine",
        designation_type="AOC", designation_name="Gigondas",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Gigondas, in the southern Rhône appellation carved from the Dentelles de Montmirail rocky massif, produces powerful, structured reds led by Grenache with Syrah and Mourvèdre. The appellation's limestone and clay soils and the mistral wind create wines of remarkable concentration and aromatic complexity — often described as Châteauneuf-du-Pape's wild younger sibling. Full appellation status was achieved in 1971.",
        key_producers="Domaine Santa Duc, Château de Montmirail, Domaine Les Pallières, Domaine du Pesquier",
        historical_context="Gigondas is one of the southern Rhône's most historically important wine communes, with winemaking dating to Roman times. The village gave its name to the appellation when it became one of the first communes to be elevated from Côtes du Rhône to independent AOC status in 1971 — a recognition of the distinctive character its rocky limestone terraces impart to Grenache and Syrah.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Domaine Santa Duc", "winery", r3, "France",
         production_philosophy="terroir_expression",
         philosophy_description="Yves Gras at Domaine Santa Duc is one of Gigondas's most respected producers, farming organically from old Grenache vines on the limestone Dentelles terraces and producing wines of exceptional concentration and aromatic precision.",
         reputation_narrative="Santa Duc's Les Hautes Garrigues and Prestige wines are consistently among Gigondas's finest, demonstrating the appellation's capacity for world-class southern Rhône of genuine site expression alongside Châteauneuf-du-Pape.",
         price_positioning="premium")

prod3a1, new9 = PROD("Domaine Santa Duc Les Hautes Garrigues Gigondas", "wine_still", p3a, r3, "France",
                      subcategory="Grenache", price_tier="premium",
                      description="From the highest, stoniest Gigondas terraces, Les Hautes Garrigues is Santa Duc's prestige cuvée: old-vine Grenache of extraordinary concentration, displaying ripe dark fruit, garrigue herbs, leather, and a long mineral finish that rivals the finest Châteauneuf-du-Pape at a fraction of the price.")
if new9:
    PAIR(prod3a1, "Slow-roasted leg of lamb with lavender and Provençal herbs", "complement", "classic", "main", "Gigondas Grenache's garrigue herb character finds a direct flavour echo in lavender and Provençal herbs; lamb's richness is framed by the wine's structure while the herbs create the aromatic bridge.")
    PAIR(prod3a1, "Wild boar stew with olives, capers, and anchovy (daube)", "complement", "classic", "main", "Southern French daube and Gigondas is a Provençal classic; the wine's power and garrigue character resonate with the stew's Mediterranean depth while olives and anchovies add the briny intensity that amplifies the wine's mineral note.")
    PAIR(prod3a1, "Grilled duck breast with herbes de Provence and olive tapenade", "complement", "established", "main", "The wine's herbal garrigue character and dark fruit are natural companions for Provençal-seasoned duck; tapenade's olive depth echoes the wine's own Mediterranean character while herbs create an aromatic unity.")
    PAIR(prod3a1, "Aged Comté with lavender honey and black walnut", "complement", "established", "cheese", "Gigondas's herbal depth and dark-fruit concentration find resonance with aged Comté; lavender honey bridges the wine's garrigue character while black walnut echoes its earthy depth.")

prod3a2, new10 = PROD("Domaine Santa Duc Gigondas Prestige des Hautes Garrigues", "wine_still", p3a, r3, "France",
                       subcategory="Grenache", price_tier="premium",
                       description="Santa Duc's most concentrated expression, from the oldest Grenache vines on the highest Gigondas limestone terraces. Extraordinarily dense dark fruit, black olive, garrigue, and leather with the structure to age 15+ years — one of the southern Rhône's great wines.")
if new10:
    PAIR(prod3a2, "Whole-roasted wild hare with Gigondas wine reduction", "complement", "classic", "main", "One of the southern Rhône's greatest wines demands game of matching intensity; the wine reduction creates a direct bridge between glass and plate while wild hare's iron character resonates with the wine's concentrated depth.")
    PAIR(prod3a2, "Venison cassoulet with duck confit and white beans", "complement", "established", "main", "The wine's concentration and garrigue character can navigate cassoulet's full complexity; duck confit and venison provide the game depth the wine demands while white beans soften its tannin.")
    PAIR(prod3a2, "Aged Pélardon (Provençal goat cheese) with truffle and walnut", "complement", "established", "cheese", "Southern French goat cheese aged and strong-flavoured is the local companion for Gigondas's most concentrated expression; truffle deepens the earthy resonance while walnut adds bitter-savour depth.")
    PAIR(prod3a2, "Braised pork cheeks with black olives and rosemary polenta", "complement", "established", "main", "The wine's old-vine power and olive character find a natural home with braised pork cheeks; black olives create a direct flavour bridge while rosemary polenta grounds the pairing in the southern Rhône's own landscape.")

p3b = P("Domaine Les Pallières", "winery", r3, "France",
         production_philosophy="minimal_intervention",
         philosophy_description="Domaine Les Pallières, farmed by the Brunier family of Domaine du Vieux Télégraphe, produces Gigondas of remarkable minerality from old vines on the Dentelles de Montmirail, combining the Brunier family's southern Rhône expertise with Gigondas's distinctive limestone terroir.",
         reputation_narrative="Les Pallières is widely considered one of Gigondas's finest estates, with the Brunier family's influence producing wines of unusual precision and mineral restraint that distinguish themselves from the appellation's sometimes more extracted styles.",
         price_positioning="premium")

prod3b1, new11 = PROD("Domaine Les Pallières Gigondas Les Racines", "wine_still", p3b, r3, "France",
                       subcategory="Grenache", price_tier="premium",
                       description="Les Pallières's old-vine Gigondas, from limestone-clay terraces in the Dentelles de Montmirail, fermented with whole clusters and aged in large foudres. The wine displays the Brunier house style: precise, mineral, and restrained, with dark cherry, garrigue, and limestone mineral in a long-lived framework.")
if new11:
    PAIR(prod3b1, "Roasted saddle of lamb with herbes de Provence and tapenade", "complement", "classic", "main", "Les Pallières's mineral restraint and garrigue character are ideal for Provençal lamb; tapenade's olive depth creates the Mediterranean bridge while herbes de Provence echo the wine's aromatic complexity.")
    PAIR(prod3b1, "Pan-roasted pigeon with black truffle and celeriac", "complement", "established", "main", "Gigondas's dark fruit and mineral precision find their most luxurious expression with pigeon and truffle; celeriac adds the earthy counterpoint while the wine's precision prevents the preparation from becoming too rich.")
    PAIR(prod3b1, "Grilled tuna with olive tapenade and roasted tomatoes", "complement", "established", "main", "The wine's restrained power and olive-mineral character can bridge the gap to tuna's meaty richness; tapenade creates a direct flavour connection while roasted tomatoes add Mediterranean sweetness.")
    PAIR(prod3b1, "Aged Comté with black olive paste and thyme honey", "complement", "classic", "cheese", "The wine's mineral depth and olive character find resonance with aged Comté; black olive paste echoes the wine's own character while thyme honey bridges its garrigue aromatics.")

prod3b2, new12 = PROD("Domaine Les Pallières Gigondas Vieilles Vignes", "wine_still", p3b, r3, "France",
                       subcategory="Grenache", price_tier="premium",
                       description="The estate's old-vine selection, from the most ancient Grenache and Mourvèdre parcels in the Dentelles, displaying greater concentration and complexity than the regular Les Racines with additional dark fruit, spice, and mineral depth.")
if new12:
    PAIR(prod3b2, "Wild mushroom and Gigondas wine reduction with pasta", "bridge", "established", "main", "A wine-based sauce with Gigondas creates a complete circle; wild mushroom's umami deepens the connection while the wine's garrigue character adds aromatic complexity to the pasta.")
    PAIR(prod3b2, "Duck confit with cherry compote and braised lentils", "complement", "classic", "main", "Old-vine Gigondas's dark-cherry depth and structure are natural companions for duck confit; cherry compote creates a direct flavour bridge while lentils add the earthy depth that grounds the pairing.")
    PAIR(prod3b2, "Whole-baked Camembert with herb and garlic crust", "complement", "established", "cheese", "Old-vine Gigondas's power and garrigue character can navigate warm, melted Camembert; herb crust echoes the wine's own aromatic complexity while garlic adds the savoury depth that completes the combination.")
    PAIR(prod3b2, "Braised rabbit with Provençal herbs, olives, and white beans", "complement", "classic", "main", "Rabbit with Provençal herbs is a classic southern French pairing for regional Grenache; olives echo the wine's own Mediterranean character while white beans provide the starchy foil that softens the tannin.")

# ── 4. Vacqueyras AOC ────────────────────────────────────────────────────────
print("=== Vacqueyras AOC ===")
r4 = R("Vacqueyras AOC", "France", "wine",
        designation_type="AOC", designation_name="Vacqueyras",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Vacqueyras, adjacent to Gigondas in the southern Rhône, produces generous, aromatic reds and rosés from Grenache, Syrah, and Mourvèdre on the alluvial terraces of the Dentelles de Montmirail. The appellation, elevated from Côtes du Rhône Villages to independent AOC in 1990, produces wines of remarkable value: comparable depth and warmth to Gigondas at more accessible prices.",
        key_producers="Domaine Le Sang des Cailloux, Château des Tours, Domaine Montvac, La Monardière",
        historical_context="Vacqueyras gained its village appellation in 1990, following Gigondas's 1971 elevation. The village's name is believed to derive from the Latin 'Vallis Querci' — valley of oaks — reflecting the garrigue landscape of holm oak and wild herbs that infuses the wines with their characteristic aromatic complexity.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r4, yr, qd, pt)

p4a = P("Domaine Le Sang des Cailloux", "winery", r4, "France",
         production_philosophy="minimal_intervention",
         philosophy_description="Serge Férigoule's Domaine Le Sang des Cailloux — 'Blood of the Stones' — is Vacqueyras's most celebrated estate, producing old-vine Grenache wines of extraordinary concentration from the appellation's stoniest, most heat-retaining sites.",
         reputation_narrative="Le Sang des Cailloux has established Vacqueyras as a serious appellation in its own right, with Serge Férigoule's concentrated, authentic wines consistently earning critical acclaim that has expanded the market for the village's wines internationally.",
         price_positioning="mid_range")

prod4a1, new13 = PROD("Le Sang des Cailloux Doucinello Vacqueyras", "wine_still", p4a, r4, "France",
                       subcategory="Grenache", price_tier="mid_range",
                       description="Le Sang des Cailloux's most approachable cuvée, from younger vines on the stony Vacqueyras terraces. Displaying generous red fruit, garrigue herbs, and warm Rhône spice in an accessible style that makes it one of the southern Rhône's best value wines.")
if new13:
    PAIR(prod4a1, "Grilled lamb sausages with herbes de Provence and tapenade", "complement", "classic", "main", "Vacqueyras Grenache's garrigue character and generous fruit are ideally suited to Provençal lamb sausages; tapenade bridges the wine's olive notes while herbes de Provence create the aromatic unity of place.")
    PAIR(prod4a1, "Pizza with spicy sausage, mozzarella, and fresh oregano", "complement", "established", "casual", "The wine's generous fruit and modest tannin are ideally calibrated for a well-made spicy pizza; mozzarella's creaminess is refreshed by the wine's acidity while sausage's spice echoes the wine's garrigue warmth.")
    PAIR(prod4a1, "Pissaladière (Provençal onion and olive tart)", "complement", "classic", "casual", "The wine's southern Rhône character finds an ideal companion in pissaladière's caramelised onion and olive combination; the wine's fruit bridges the onion's sweetness while its garrigue character echoes the anchovy's umami.")
    PAIR(prod4a1, "Cheese plate with Crottin de Chavignol and dried fruit", "complement", "established", "cheese", "The wine's garrigue herbs and red fruit find a pleasant match with aged goat cheese; dried fruit echoes the wine's warmth while the cheese's acidity bridges its own tartness.")

prod4a2, new14 = PROD("Le Sang des Cailloux Vacqueyras Cuvée Lopy", "wine_still", p4a, r4, "France",
                       subcategory="Grenache", price_tier="mid_range",
                       description="The estate's flagship old-vine cuvée, from the stoniest Vacqueyras plots where heat retention maximises Grenache ripeness. Cuvée Lopy delivers concentrated dark cherry, garrigue, leather, and warmth with a long, spiced finish — old-vine southern Rhône at its most authentic.")
if new14:
    PAIR(prod4a2, "Slow-roasted lamb shoulder with olives and Provençal herbs", "complement", "classic", "main", "Old-vine Grenache and slow-roasted lamb is the quintessential southern Rhône pairing; olives create the olive-garrigue bridge while Provençal herbs echo the wine's aromatic character.")
    PAIR(prod4a2, "Pieds et paquets (Provençal lamb tripe with herbs)", "complement", "classic", "main", "This deeply traditional Provençal dish demands a Grenache of old-vine authenticity; the wine's herbal garrigue resonates with the preparation's herb stuffing while its warmth complements the rich tripe.")
    PAIR(prod4a2, "Grilled entrecôte with herbed butter and haricots verts", "complement", "established", "main", "Old-vine Vacqueyras's concentration and garrigue character find a simple but effective match in grilled beef; herbed butter echoes the wine's complexity while haricots verts provide the clean vegetable contrast.")
    PAIR(prod4a2, "Aged Roquefort with fig jam and walnut", "contrast", "classic", "cheese", "Old-vine Grenache's sweetness and warmth create a compelling contrast with Roquefort's intensity; fig jam bridges the wine's fruit while walnut adds bitter depth that prolongs the finish.")

p4b = P("La Monardière", "winery", r4, "France",
         production_philosophy="sustainable",
         philosophy_description="La Monardière is one of Vacqueyras's most respected organic producers, farming the appellation's garrigue hillsides with genuine environmental commitment and producing wines of consistent charm and value that have built a loyal following among southern Rhône enthusiasts.",
         reputation_narrative="La Monardière provides a consistently reliable source of authentic, well-priced Vacqueyras wines that reflect the appellation's character without pretension — the kind of honest, food-friendly wine that built the southern Rhône's international reputation.",
         price_positioning="mid_range")

prod4b1, new15 = PROD("La Monardière Vieilles Vignes Vacqueyras", "wine_still", p4b, r4, "France",
                       subcategory="Grenache", price_tier="mid_range",
                       description="From La Monardière's oldest organic Grenache vines in Vacqueyras, displaying the appellation's characteristic combination of red fruit warmth, garrigue herbs, and Rhône spice in a genuinely honest style that rewards both everyday drinking and food pairing.")
if new15:
    PAIR(prod4b1, "Roasted chicken with ratatouille and Provençal herbs", "complement", "classic", "main", "Vacqueyras Grenache and ratatouille is one of southern France's defining home cooking pairings; the wine's garrigue character mirrors the vegetable medley's herbs while the roasted chicken provides the protein that grounds the combination.")
    PAIR(prod4b1, "Bouillabaisse-style fish stew with rouille and croutons", "complement", "established", "main", "While a traditional bouillabaisse partners with rosé or white, a lighter red Grenache can navigate the stew's rich saffron broth; rouille's garlic adds depth while croutons absorb the complexity.")
    PAIR(prod4b1, "Tian de légumes (Provençal vegetable gratin)", "complement", "established", "main", "Vacqueyras's most accessible expression finds a natural partner in Provençal vegetable gratin; the wine's warmth and herb character resonate with the gratin's layered Mediterranean vegetables.")
    PAIR(prod4b1, "Grilled merguez sausages with harissa and couscous", "complement", "classic", "casual", "The wine's generous fruit and moderate spice are well-calibrated for merguez; harissa's warmth amplifies the wine's own character while couscous absorbs the spice, keeping the combination balanced.")

prod4b2, new16 = PROD("La Monardière Les Deux Monardes Vacqueyras", "wine_still", p4b, r4, "France",
                       subcategory="Grenache", price_tier="mid_range",
                       description="A selection from La Monardière's finest old organic vines, Les Deux Monardes offers slightly greater concentration and structure than the Vieilles Vignes — more depth and ageing potential while maintaining the estate's characteristic freshness and garrigue character.")
if new16:
    PAIR(prod4b2, "Daube Provençale (beef stew with herbes de Provence and orange)", "complement", "classic", "main", "Daube and southern Rhône Grenache is a Provençal classic; the stew's orange peel echoes the wine's warmth while the herbes de Provence create the aromatic bridge that makes the pairing feel inevitable.")
    PAIR(prod4b2, "Duck thighs with olive and caper sauce (alla putanesca)", "complement", "established", "main", "The wine's garrigue character and dark fruit find a compelling match with the olive-caper sauce; duck thighs' richness provides the protein depth while the bold sauce echoes the wine's Mediterranean intensity.")
    PAIR(prod4b2, "Aged Cantal with fig compote and walnut bread", "complement", "established", "cheese", "The wine's Rhône warmth and red fruit character find resonance with aged Cantal's sharpness; fig compote bridges the wine's fruit while walnut bread adds the earthy depth that extends the pairing.")
    PAIR(prod4b2, "Lamb navarin with spring vegetables and fresh herbs", "complement", "established", "main", "Spring navarin's delicacy and herb character call for a Grenache of this balanced weight; fresh herbs echo the wine's own aromatic complexity while spring vegetables provide the clean vegetable contrast.")

# ── 5. Corbières AOC ─────────────────────────────────────────────────────────
print("=== Corbières AOC ===")
r5 = R("Corbières AOC", "France", "wine",
        designation_type="AOC", designation_name="Corbières",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Corbières, in the rugged hills south of Carcassonne in Languedoc, produces full-bodied reds from Carignan, Grenache, Syrah, and Mourvèdre on the region's diverse schist, limestone, and volcanic soils. One of France's largest AOCs by area, Corbières ranges from simple, fruit-forward everyday wines to ambitious, garrigue-scented reds that challenge more famous southern French appellations.",
        key_producers="Domaine Gauby (Corbières adjacent), Château Lastours, Domaine du Grand Arc, Château Haut-Gleon",
        historical_context="Corbières has been producing wine since the Roman occupation, with Cathar history deeply embedded in the landscape's castle ruins. The appellation was awarded AOC status in 1985. Despite its size — nearly 14,000 hectares — quality has consistently improved, particularly since the identification of 11 internal terroir zones, with the Boutenac sub-appellation achieving its own AOC in 2005.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "rising"), (2023, "good", "rising")]:
    VIN(r5, yr, qd, pt)

p5a = P("Château Lastours", "winery", r5, "France",
         production_philosophy="sustainable",
         philosophy_description="Château Lastours is one of Corbières's most ambitious estates, farming sustainably in the dramatic Cathar landscape south of Carcassonne. Their special cuvée, Simone Descamps, is consistently one of the appellation's most celebrated wines.",
         reputation_narrative="Château Lastours has been instrumental in elevating Corbières's image internationally, demonstrating that the appellation's diverse soils and varieties can produce wines of genuine complexity and age-worthiness. Their Simone Descamps cuvée has earned consistent critical praise.",
         price_positioning="mid_range")

prod5a1, new17 = PROD("Château Lastours Simone Descamps Corbières", "wine_still", p5a, r5, "France",
                       subcategory="Carignan blend", price_tier="mid_range",
                       description="Château Lastours's flagship, a Syrah and Carignan-led blend from the estate's finest Corbières parcels. Simone Descamps delivers garrigue herbs, dark cherry, leather, and a distinctive mineral note from the schist soils, with structure that rewards 5-10 years of cellaring.")
if new17:
    PAIR(prod5a1, "Slow-braised lamb with Corbières wine and Mediterranean herbs", "complement", "classic", "main", "A Corbières wine reduction with Corbières wine in the braise creates a complete circle; Mediterranean herbs echo the wine's garrigue character while lamb's richness is framed by the Carignan's natural acidity.")
    PAIR(prod5a1, "Grilled duck with lavender honey glaze and roasted figs", "complement", "established", "main", "The wine's dark cherry and garrigue character find resonance with duck and lavender; roasted figs echo the wine's dried-fruit warmth while honey bridges its fruit with the duck's richness.")
    PAIR(prod5a1, "Wild boar ragù with handmade pasta and aged Pélardon", "complement", "established", "main", "Corbières's garrigue depth and Carignan's acidity are well-matched to wild boar ragù; aged goat cheese adds the sharp counterpoint that amplifies the wine's own acidity while pasta absorbs the intensity.")
    PAIR(prod5a1, "Aged Cantal with fig jam and Languedoc walnut bread", "complement", "established", "cheese", "The wine's dark fruit and garrigue depth find resonance with aged Cantal's sharpness; fig jam bridges its warmth while walnut bread's earthiness grounds the southern French combination.")

prod5a2, new18 = PROD("Château Lastours Corbières Rouge Tradition", "wine_still", p5a, r5, "France",
                       subcategory="Grenache blend", price_tier="mid_range",
                       description="The estate's everyday Corbières rouge, blending Grenache, Syrah, and Carignan from younger vines across the property. Delivers the appellation's characteristic profile — ripe red fruit, garrigue herbs, and southern warmth — in an accessible, immediately enjoyable style.")
if new18:
    PAIR(prod5a2, "Cassoulet Languedocien with duck confit and sausage", "complement", "classic", "main", "The regional classic: Corbières and cassoulet is a fundamental Languedoc pairing, the wine's garrigue warmth resonating with the slow-cooked beans and duck while the white beans absorb the wine's tannin.")
    PAIR(prod5a2, "Grilled pork ribs with herbs and roasted vegetables", "complement", "classic", "main", "The wine's generous fruit and garrigue character are ideal for straightforward grilled pork; herbs echo the wine's aromatic character while roasted vegetables add Mediterranean sweetness.")
    PAIR(prod5a2, "Piperade with Basque pepper, tomato, and ham", "complement", "established", "main", "The wine's Languedoc character bridges to the Basque tradition; pepper's sweetness complements the wine's fruit while ham adds the savoury depth that grounds the colourful preparation.")
    PAIR(prod5a2, "Roquefort with grape must and walnut (fourme d'ambert board)", "contrast", "established", "cheese", "Corbières's southern warmth provides a compelling contrast to strong blue cheese; grape must bridges the wine's fruit while walnuts add the bitter depth that balances the combination.")

p5b = P("Domaine du Grand Arc", "winery", r5, "France",
         production_philosophy="minimal_intervention",
         philosophy_description="Domaine du Grand Arc, in the Boutenac sub-zone of Corbières, produces some of the appellation's most focused wines from old Carignan vines on limestone and schist, with minimal intervention to preserve the variety's natural freshness and mineral character.",
         reputation_narrative="Grand Arc is respected among natural wine enthusiasts for its commitment to old-vine Carignan and transparent winemaking, producing wines that demonstrate Corbières's capacity for genuinely expressive, site-specific wine.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Domaine du Grand Arc Carignan Corbières Boutenac", "wine_still", p5b, r5, "France",
                       subcategory="Carignan", price_tier="mid_range",
                       description="A pure old-vine Carignan from the Boutenac sub-appellation's limestone and schist soils, displaying the variety's hallmark combination of bright acidity, red cherry, and mineral intensity with a distinctive savoury depth that makes Carignan unique among Mediterranean varieties.")
if new19:
    PAIR(prod5b1, "Grilled merguez with harissa and coriander flatbread", "complement", "established", "casual", "Old-vine Carignan's bright acidity and red cherry character are natural companions for merguez; harissa's warmth amplifies the wine's garrigue while coriander adds the aromatic note that bridges the combination.")
    PAIR(prod5b1, "Pasta al ragù with pork and fennel sausage", "complement", "classic", "main", "Carignan's natural acidity and cherry fruit are ideal for tomato-based pasta; fennel sausage's spice echoes the wine's own character while the pasta absorbs the sauce's richness.")
    PAIR(prod5b1, "Grilled sardines with lemon, olive oil, and capers", "complement", "established", "starter", "Old-vine Carignan's bright acidity and mineral character can bridge to oily fish; lemon amplifies the wine's acidity while capers add the briny minerality that echoes Carignan's own character.")
    PAIR(prod5b1, "Tapenade toasts with anchovy and roasted tomatoes", "complement", "classic", "aperitif", "Carignan's acidity and cherry character are ideally calibrated for tapenade's rich umami; anchovy adds the salt-mineral depth while roasted tomatoes echo the wine's own brightness.")

prod5b2, new20 = PROD("Domaine du Grand Arc Corbières La Tradition", "wine_still", p5b, r5, "France",
                       subcategory="Grenache blend", price_tier="mid_range",
                       description="A Grenache-dominant Corbières blend from Grand Arc's estate vineyards, displaying the appellation's southern warmth with the house's characteristic freshness: ripe cherry, garrigue herbs, and a long, mineral finish that reflects the Boutenac zone's exceptional limestone soils.")
if new20:
    PAIR(prod5b2, "Chicken paillard with herbes de Provence and roasted garlic", "complement", "classic", "main", "The wine's garrigue warmth and cherry character are ideal for Provençal chicken; herbes de Provence create the aromatic unity of the southern French landscape while roasted garlic adds the savoury depth that grounds the pairing.")
    PAIR(prod5b2, "Lamb merguez tagine with preserved lemon and olives", "complement", "established", "main", "Corbières Grenache's warmth and fruit navigate North African-inflected lamb with ease; preserved lemon's tartness echoes the wine's acidity while olives bridge its Mediterranean character.")
    PAIR(prod5b2, "Grilled vegetables (tian) with Comté and dried herbs", "complement", "established", "casual", "The wine's garrigue character resonates with dried herbs on grilled vegetables; Comté's nutty complexity adds the richness that elevates this simple summer combination.")
    PAIR(prod5b2, "Aged Manchego with romesco sauce and sourdough", "complement", "established", "cheese", "Corbières Grenache's warmth and Spanish-influenced character find resonance with Manchego; romesco's roasted pepper and almond character echoes the wine's own Mediterranean depth.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
print("B150 complete.")
conn.close()
