#!/usr/bin/env python3
"""T23 Batch 28 — New wine regions: Pouilly-Fuissé AOC (France), Vouvray AOC (France), Cava DO (Spain), Lugana DOC (Italy), Primitivo di Manduria DOC (Italy)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── POUILLY-FUISSÉ AOC (FRANCE) ───────────────────────────────────
print("\n=== Pouilly-Fuissé AOC (France) ===")
r_pfu = R("Pouilly-Fuissé", "France", "wine",
           designation_type="AOC",
           designation_name="Pouilly-Fuissé AOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The Mâconnais's most prestigious and internationally celebrated white wine AOC — the dramatic limestone escarpments and ancient caves around the villages of Fuissé, Solutré, and Vergisson producing Chardonnay of mineral depth, richness, and complexity that rivals village and premier cru Côte de Beaune Burgundy at significantly lower prices. The 2020 introduction of Pouilly-Fuissé Premier Cru — recognizing 22 individual climat across the five villages — has provided a classification framework that elevates the appellation's finest single-vineyard wines. The soils of white limestone and clay over Jurassic rock create a distinctive mineral character.",
           key_producers="Guffens-Heynen, Château Fuissé, Roger Lassarat, Domaine Ferret, Domaine Cordier, Domaine Robert-Denogent",
           historical_context="Pouilly-Fuissé's dramatic landscape — dominated by the Rock of Solutré, a sheer limestone escarpment where Palaeolithic hunters drove horses over the edge — has been producing wine since Roman times. François Mitterrand climbed the Rock of Solutré every Pentecost for decades while president of France, making it a symbol of French political and cultural identity. The appellation's international reputation was built primarily through Château Fuissé's Vieilles Vignes bottling in the 1980s, which demonstrated to American wine buyers that the Mâconnais could produce white Burgundy of premier cru quality. The 2020 premier cru classifications were the culmination of 40 years of lobbying by estate owners.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Pouilly-Fuissé vintage; Chardonnay from limestone and clay showed extraordinary mineral complexity and the rich texture of the finest Mâconnais."),
    (2021, "very_good", "stable", "Classic vintage; cool conditions produced Pouilly-Fuissé of excellent freshness and the chalk-limestone mineral precision of great Mâconnais Chardonnay."),
    (2020, "exceptional", "rising", "Historic vintage in two senses — extraordinary quality AND the year of the first premier cru classifications; Guffens-Heynen and Château Fuissé produced wines of legendary quality."),
    (2019, "excellent", "stable", "Outstanding vintage; old-vine Chardonnay from limestone soils produced wines of unusual depth; premier cru movement built momentum from this exceptional year."),
    (2018, "very_good", "stable", "Warm vintage producing generous Pouilly-Fuissé of good richness; Chardonnay of toasted richness and mineral depth; accessible and delicious."),
]:
    VIN(r_pfu, yr, qd, pt, sn)

p_guf = P("Domaine Guffens-Heynen", "France", r_pfu,
           description="Jean-Marie Guffens's Belgian-owned Mâconnais estate — the most critically acclaimed and internationally recognized Pouilly-Fuissé producer. Guffens's obsessive low-yield, precise viticulture and his refusal to compromise quality at any price has produced single-vineyard Pouilly-Fuissé wines (En France, La Roche, La Merlière) that routinely blind-taste alongside premier cru Puligny-Montrachet. He also owns Verget négociant, producing the finest range of Mâconnais and Côte de Beaune white wines commercially available.")
prod_guf, new = PROD("Domaine Guffens-Heynen Pouilly-Fuissé En France", "wine_still", p_guf, r_pfu, "France",
                     subcategory="Chardonnay",
                     description="The Mâconnais's most ambitious and critically acclaimed single-vineyard Chardonnay — Jean-Marie Guffens's En France parcel on white limestone over Jurassic clay. Extraordinary complexity: hazelnut, white peach, lemon curd, chalk mineral, toasted oak, and a richness that develops magnificently over 8-10 years. Regularly blind-tasted against premier cru Côte de Beaune at a fraction of the price. The definitive argument for Pouilly-Fuissé's premier cru ambitions.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_guf, "Saint-Jacques avec crème de cerfeuil et truffe blanche (scallops with chervil cream)", "complement", "classic", "main", "The Mâconnais's great white wine and the finest scallop preparation — the wine's hazelnut and chalk mineral character bridges the scallop's sweet richness; chervil mirrors the wine's herbal complexity; white truffle amplifies the mineral depth")
    PAIR(prod_guf, "Quiche Bourguignonne with Époisses, lardons, and fresh herbs", "complement", "classic", "main", "The Burgundian cheese quiche and the Mâconnais's finest Chardonnay — the wine's richness and hazelnut depth bridges the Époisses's washed-rind intensity; lardons add savoury depth; pastry allows the wine's limestone mineral to shine")

p_fui = P("Château Fuissé", "France", r_pfu,
           description="The Vincent family's Pouilly-Fuissé estate — the producer that established the appellation's reputation for premier-level quality with the Vieilles Vignes bottling in the 1980s. Château Fuissé's Le Clos and Vieilles Vignes single-vineyard wines from the limestone soils around Fuissé village are considered the AOC's benchmark for terroir expression and aging potential. The estate has been central to the 2020 premier cru classification effort.")
prod_fui, new = PROD("Château Fuissé Pouilly-Fuissé Vieilles Vignes", "wine_still", p_fui, r_pfu, "France",
                     subcategory="Chardonnay",
                     description="The wine that built Pouilly-Fuissé's international reputation — old-vine Chardonnay from the limestone and clay slopes around Fuissé village, aged in Burgundy oak. Rich, complex, and mineral: white peach, hazelnut, chalk, lemon curd, and the toasted depth that develops over 7-10 years into something Burgundians would not be embarrassed to claim. Consistently one of the Mâconnais's finest wines.",
                     price_tier="premium")
if new:
    PAIR(prod_fui, "Oeufs en meurette bourguignons (eggs in red wine sauce) with lardons and croutons", "complement", "established", "starter", "The Burgundian classic breakfast-as-starter and the Mâconnais Chardonnay — the wine's richness and mineral depth bridges the red wine egg sauce; lardons' smoky depth is contrasted by the wine's fresh chalk mineral; croutons provide textural contrast")
    PAIR(prod_fui, "Brochet au beurre blanc (pike with white butter sauce) from the Saône", "complement", "classic", "main", "The Saône valley's traditional freshwater fish and its neighbouring Mâconnais Chardonnay — beurre blanc's butter mirrors the wine's richness; pike's delicate mineral freshness bridges the chalk limestone character")

# ── VOUVRAY AOC (FRANCE) ──────────────────────────────────────────
print("\n=== Vouvray AOC (France) ===")
r_vou = R("Vouvray", "France", "wine",
           designation_type="AOC",
           designation_name="Vouvray AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="The Loire Valley's most versatile and intellectually fascinating appellation — the tuffeau limestone hillsides northeast of Tours producing Chenin Blanc in every conceivable style from bone-dry to luxuriously sweet: Vouvray Sec (dry), Demi-Sec (off-dry), Moelleux (sweet), and Vouvray Pétillant or Mousseux (sparkling). The defining characteristic across all styles is Vouvray's extraordinary longevity — great Vouvray moelleux ages 50-100+ years, developing extraordinary honey-mineral-wax complexity. The tuffeau's chalk and silicon impart a distinctive mineral freshness that ties the wines across all sweetness levels.",
           key_producers="Huet, Philippe Foreau (Clos Naudin), Domaine des Aubuisières, François Chidaine, Vincent Carême",
           historical_context="Gaston Huet — the mayor of Vouvray and its most legendary producer — survived German captivity in WWII, returned to his estate, and spent the next 60 years demonstrating that Chenin Blanc from tuffeau limestone was one of France's great white wine traditions. His three single-vineyard wines (Le Haut-Lieu, Le Mont, Clos du Bourg) in both dry and sweet styles remain the definitive reference for Vouvray. Nicolas Joly's biodynamic inspiration spread to Vouvray through François Chidaine and others in the 2000s, creating a natural wine thread in the appellation. The expression 'en attendant ses vins de Vouvray' (while waiting for one's Vouvray) was a common Loire Valley expression for the long cellaring required before the wines showed their potential.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vouvray vintage; Chenin Blanc from tuffeau showed extraordinary aromatic complexity across all styles; moelleux wines of rare sweetness and mineral tension."),
    (2021, "very_good", "stable", "Classic vintage; cool Loire conditions produced Vouvray sec of excellent freshness and the chalk-tuffeau mineral precision; demi-sec wines of unusual elegance."),
    (2020, "excellent", "stable", "Benchmark year; Huet and Foreau both produced Clos de Bourg and Clos Naudin wines of extraordinary depth; moelleux of exceptional sweetness and longevity potential."),
    (2019, "exceptional", "rising", "Greatest Vouvray vintage of the era; noble rot produced moelleux of legendary concentration; the sec wines also extraordinary in their mineral depth."),
    (2018, "excellent", "stable", "Outstanding vintage for both sec and moelleux; botrytis was ideal; the 2018 Huet moelleux wines are destined for 30+ year development."),
]:
    VIN(r_vou, yr, qd, pt, sn)

p_hue = P("Domaine Huet", "France", r_vou,
           description="The most legendary Vouvray estate and the domaine that defines what Loire Chenin Blanc can achieve — Gaston Huet's three single-vineyard biodynamic holdings (Le Haut-Lieu, Le Mont, Clos du Bourg) produce dry, demi-sec, and moelleux wines that age 30-100+ years in exceptional vintages. Now managed by Noel Pinguet (Gaston's son-in-law) and subsequently the Hwang family with continued biodynamic commitment, Huet remains the reference for all serious Vouvray.")
prod_hue, new = PROD("Domaine Huet Le Mont Vouvray Sec", "wine_still", p_hue, r_vou, "France",
                     subcategory="Chenin Blanc",
                     description="Vouvray's benchmark dry Chenin Blanc — from the Le Mont hillside's tuffeau chalk and silicon, biodynamically farmed. Quince, green apple, lime, beeswax, chalk mineral, and a taut, restrained dryness that masks extraordinary complexity. At 5-10 years the wax and mineral integrate into something resembling great Chablis premier cru. At 20 years, a revelation of Chenin Blanc's unique capacity for longevity. Loire Valley winemaking at its most intellectually serious.",
                     price_tier="premium")
if new:
    PAIR(prod_hue, "Rillettes de Tours (slow-cooked pork rillettes) with Vouvray moelleux aspic and cornichons", "complement", "classic", "aperitif", "The Touraine's most traditional charcuterie and its dry white wine — Vouvray sec's quince and chalk mineral cuts through the rillettes' fat; cornichons' acidity bridges the wine's freshness; the moelleux aspic (if used in the terrine) creates a circular reference")
    PAIR(prod_hue, "Chaource (Champagne/Loire fresh cheese) with white truffle honey and hazelnuts", "complement", "classic", "cheese", "The Loire's fresh washed-rind cheese and its Chenin Blanc — Vouvray's beeswax and mineral bridges the cheese's fresh lactic creaminess; honey mirrors the wine's natural richness; hazelnuts bridge the chalk mineral")

p_for = P("Domaine du Clos Naudin (Philippe Foreau)", "France", r_vou,
           description="Philippe Foreau's Clos Naudin estate — the most critically acclaimed Vouvray producer alongside Huet, producing the appellation's most consistent moelleux wines from the walled Clos Naudin hillside. Foreau's approach of releasing wines only when ready — sometimes 10-15 years after harvest for exceptional moelleux — and his insistence on natural fermentation produce wines of extraordinary authenticity and longevity.")
prod_for_v, new = PROD("Clos Naudin Vouvray Moelleux Réserve", "wine_still", p_for, r_vou, "France",
                       subcategory="Chenin Blanc",
                       description="One of France's greatest sweet wines — Philippe Foreau's noble rot Chenin Blanc from the Clos Naudin tuffeau hillside, released only after years of development. Apricot jam, honey, quince paste, beeswax, chalk mineral, saffron, and a sweetness balanced by extraordinary natural acidity. Ages 30-50 years; at peak resembles Sauternes but with a Loire purity and mineral tension all its own. Extraordinary.",
                       price_tier="ultra_premium")
if new:
    PAIR(prod_for_v, "Foie gras de canard en terrine with Vouvray moelleux gelée and toasted brioche", "complement", "classic", "starter", "The great Loire sweet wine and foie gras pairing — Vouvray's apricot jam and mineral acidity balances the foie gras's extraordinary richness; the moelleux gelée creates a circular reference; brioche provides textural contrast")
    PAIR(prod_for_v, "Tarte Tatin aux poires with crème fraîche and vanilla bean", "complement", "classic", "dessert", "The Loire tradition of pear tarte tatin and its sweet Chenin Blanc — the wine's quince paste and apricot jam character finds direct resonance in the caramelized pear; crème fraîche's tartness mirrors the wine's mineral acidity; vanilla bridges the beeswax richness")

# ── CAVA DO (SPAIN) ───────────────────────────────────────────────
print("\n=== Cava DO (Spain) ===")
r_cav = R("Cava", "Spain", "wine",
           designation_type="DO",
           designation_name="Cava DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Spain's most important traditional method sparkling wine DO — produced primarily in Penedès (Catalonia) but also in other Spanish regions, using indigenous varieties Macabeo, Xarel-lo, and Parellada (plus Chardonnay, Pinot Noir, Monastrell, and Garnacha). Cava ranges from commercial Non-Vintage to serious Cava de Paraje Calificado from single vineyards aged 36+ months on lees. The finest artisan Cava — particularly from Gramona, Recaredo, and Llopart — achieves a mineral complexity and aging potential that competes directly with Champagne. The Corpinnat and other alternative designations have emerged as serious producers reject the DO's perceived commercial dilution.",
           key_producers="Gramona, Recaredo, Llopart, Juvé y Camps, Raventós i Blanc, Agustí Torelló Mata",
           historical_context="Josep Raventós i Fatjó of Codorníu produced the first Spanish traditional method sparkling wine in 1872 after observing Champagne production methods on a visit to France. The name 'Cava' (Catalan for cellar) replaced 'Champagne' in Spanish labeling in 1970 when EEC pressure forced Spain to abandon the Champagne designation. By the 1980s, Cava had become the world's largest producer of traditional method sparkling wine by volume. The Corpinnat rebellion of 2019 — in which Gramona, Recaredo, Raventós i Blanc, and others left the Cava DO to create a stricter Penedès alternative — highlighted the tension between mass-market and artisan production within the DO.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Cava vintage; indigenous varieties Xarel-lo and Macabeo showed extraordinary mineral complexity for extended lees-aged reserve wines."),
    (2021, "very_good", "stable", "Classic vintage; cool Mediterranean coastal conditions produced base wines of excellent natural acidity ideal for extended lees aging."),
    (2020, "excellent", "stable", "Benchmark year; Gramona and Recaredo both produced single-vineyard Cava de Paraje Calificado of international acclaim; serious Cava's reputation solidified."),
    (2019, "very_good", "stable", "Solid vintage; the year of the Corpinnat rebellion; Xarel-lo from old Penedès vines showed excellent mineral depth for extended aging."),
    (2018, "excellent", "rising", "Outstanding vintage for extended reserve Cavas; Gramona III Lustros and Recaredo Terrers wines of extraordinary complexity from the warm, dry season."),
]:
    VIN(r_cav, yr, qd, pt, sn)

p_gra = P("Gramona", "France", r_cav,  # Will fix country
           description="The Catalan artisan Cava estate that has done most to elevate the DO's international reputation — and most visibly abandoned it. Gramona's III Lustros (15 years on lees), Celler Batlle (10 years), and Argent range from single-vineyard Xarel-lo demonstrate that traditional method sparkling wine from Catalonia can achieve Champagne-level complexity. The family's decision to join Corpinnat and leave the Cava DO in 2019 was the most high-profile statement of artisan producers' frustration with the DO's commercial direction.")
prod_gra, new = PROD("Gramona III Lustros Gran Reserva Brut Nature", "wine_sparkling", p_gra, r_cav, "Spain",
                     subcategory="Xarel-lo",
                     description="Spain's most extraordinary extended-lees sparkling wine — Xarel-lo with Macabeo and Chardonnay, aged 15+ years (III Lustros) on lees in the family's Penedès cellars before disgorgement. Extraordinary autolytic complexity: toasted hazelnut, brioche, dried citrus peel, almond blossom, chalk mineral, and a persistent, fine mousse. Rivals vintage Champagne for mineral complexity. The definitive argument for Catalan traditional method wine.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_gra, "Jamón ibérico de bellota 5J pata negra with pan con tomate and aged Manchego", "complement", "classic", "aperitif", "Spain's most prestigious charcuterie and its most complex sparkling wine — the wine's autolytic complexity and mineral depth bridges the ibérico's extraordinary nutty-sweet fat; tomato bread provides acidic contrast; Manchego bridges the chalk mineral")
    PAIR(prod_gra, "Percebes (gooseneck barnacles) from Galicia with sea salt and hot water", "complement", "classic", "aperitif", "Spain's most oceanic delicacy and its most complex sparkling wine — the barnacle's intense brine and iodine character is one of the few ingredients that matches Gramona's autolytic mineral depth; the wine's chalk mineral mirrors the Atlantic mineral")

p_rec = P("Recaredo", "Spain", r_cav,
           description="The Mata family's Sant Sadurní d'Anoia estate — producing the most critically acclaimed and internationally distributed artisan Cava in the traditional Corpinnat style. Recaredo's Terrers single-vineyard wine and the Turó d'en Mota (disgorgement after 10+ years on lees) are considered among Spain's greatest sparkling wines, comparable to prestige Champagne in complexity and aging. Recaredo uses only biodynamic estate fruit and no dosage (Brut Nature).")
prod_rec, new = PROD("Recaredo Terrers Brut Nature Gran Reserva Corpinnat", "wine_sparkling", p_rec, r_cav, "Spain",
                     subcategory="Macabeo",
                     description="The most internationally recognized artisan Corpinnat — Macabeo, Xarel-lo, and Parellada from biodynamic old-vine Penedès parcels, zero dosage, aged 60+ months on lees. Lemon zest, green apple, chalk, toasted almond, brioche, and the saline Mediterranean mineral that distinguishes Catalan traditional method from Champagne. More mineral and austere than Gramona's style; enormously age-worthy. Spain's benchmark biodynamic sparkling wine.",
                     price_tier="premium")
if new:
    PAIR(prod_rec, "Espardenyes (sea cucumbers) with fideuà negra, romesco, and alioli", "complement", "classic", "main", "Catalonia's most challenging seafood and its finest sparkling wine — the wine's chalk mineral and zero-dosage austerity is one of the few sparkling wines that stands up to sea cucumber's oceanic intensity; fideuà negra's squid ink bridges the marine mineral")
    PAIR(prod_rec, "Pa amb tomàquet amb anxoves del Cantàbric (bread with tomato and Cantabrian anchovy)", "complement", "classic", "aperitif", "Catalonia's most fundamental food and its finest sparkling wine — the wine's mineral freshness and brioche character bridges the anchovy's salt-cured intensity; tomato's acidity mirrors the wine's natural freshness; olive oil bridges the autolytic depth")

# Fix Gramona country
cur.execute("UPDATE beverage_producers SET country='Spain' WHERE name='Gramona' AND country='France'")

# ── LUGANA DOC (ITALY) ────────────────────────────────────────────
print("\n=== Lugana DOC (Italy) ===")
r_lug = R("Lugana", "Italy", "wine",
           designation_type="DOC",
           designation_name="Lugana DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Lake Garda's most internationally celebrated white wine DOC — the southern shore of Italy's largest lake on the Lombardy-Veneto border, producing Turbiana (the local name for Trebbiano di Lugana — genetically distinct from other Trebbiano varieties) from the lake's glacial moraine and chalk-clay soils. Lugana wines have a distinctive white peach, almond, and subtle smoke mineral character imparted by the lake's microclimate and the unique Turbiana variety's thick skins. The finest single-vineyard and Riserva Luganas age magnificently over 10-15 years, surprising those who expect simple early-drinking whites from this holiday-destination lake.",
           key_producers="Ca' dei Frati, Ottella, Zenato, Cà Maiol, Pasini San Giovanni, Provenza",
           historical_context="Turbiana's genetic uniqueness was confirmed by DNA analysis in the 1990s, distinguishing it from the widespread and often undistinguished Trebbiano Toscano — a critical distinction that restored the variety's reputation. The lake-effect microclimate of Lake Garda (Italy's largest lake) moderates temperatures significantly, allowing late harvesting with natural acidity retention in a region that would otherwise be too warm for quality white wine. Ca' dei Frati's Brolettino (from the oldest vines) and the estate's I Frati single-vineyard wine have been central to establishing Lugana as Italy's surprise white wine success story of the past 20 years.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding Lugana vintage; Turbiana from Lake Garda clay-chalk showed extraordinary mineral complexity and the characteristic almond-smoke mineral freshness."),
    (2022, "very_good", "stable", "Classic vintage; lake-effect microclimate produced wines of excellent natural acidity and the characteristic Lugana white peach and mineral character."),
    (2021, "excellent", "stable", "Benchmark year; Ca' dei Frati and Ottella both produced single-vineyard Lugana of international acclaim; Riserva wines of exceptional aging potential."),
    (2020, "excellent", "rising", "Outstanding vintage; Lugana Riserva wines of extraordinary mineral depth and longevity; Italy's wine press rediscovery of Turbiana as a serious variety."),
    (2019, "very_good", "stable", "Solid vintage; Lake Garda's microclimate produced Turbiana of good freshness and the characteristic Lugana almond-smoke mineral at all price levels."),
]:
    VIN(r_lug, yr, qd, pt, sn)

p_cdf = P("Ca' dei Frati", "Italy", r_lug,
           description="The Dal Cero family's Lugana estate — the most internationally recognized and critically acclaimed producer in the DOC. Ca' dei Frati's I Frati (the benchmark entry Lugana), Brolettino (old-vine single-vineyard), and Cru San Giovanni (the estate's finest Turbiana from pre-phylloxera vines) have established Lugana as one of Italy's most exciting white wine stories. The Brolettino in particular — aged in oak with extended lees contact — demonstrates that Turbiana can develop Chardonnay-like complexity over 10+ years.")
prod_cdf, new = PROD("Ca' dei Frati Brolettino Lugana", "wine_still", p_cdf, r_lug, "Italy",
                     subcategory="Turbiana",
                     description="Lake Garda's most complex white wine — old-vine Turbiana from the Brolettino parcel, aged in French oak with extended lees contact. Extraordinary complexity: white peach, almond smoke, hazelnut, mineral chalk, dried herbs from the lake shore, and a richness that develops magnificently over 8-10 years. The wine that demonstrated that Turbiana can rival the finest Italian white wines when given the care it deserves.",
                     price_tier="premium")
if new:
    PAIR(prod_cdf, "Lavarello al forno (Lake Garda whitefish baked with lemon, capers, and white wine)", "complement", "classic", "main", "The most traditional Lugana food pairing — Lake Garda whitefish and its white wine; the wine's almond smoke and mineral character bridges the delicate freshwater fish; capers add a saline bridge; lemon amplifies the wine's citrus freshness")
    PAIR(prod_cdf, "Risotto al Lugana con burro di malga e Grana Padano (risotto with mountain butter)", "complement", "classic", "main", "The northern Italian rice tradition and Lake Garda's finest white — Lugana's mineral depth and hazelnut richness bridges the risotto's butter-parmesan richness; the wine appears as the base liquid in a circular reference")

p_ott = P("Ottella", "Italy", r_lug,
           description="Michele and Francesco Montresor's Lake Garda estate — producing some of Lugana's most precise and mineral-driven wines from the chalky clay soils of the southern shore. The Molceo single-vineyard Lugana Superiore and the Le Creete wines demonstrate Turbiana's capacity for mineral transparency and extended aging alongside the more commercially focused I Frati style of Ca' dei Frati.")
prod_ott, new = PROD("Ottella Lugana Le Creete", "wine_still", p_ott, r_lug, "Italy",
                     subcategory="Turbiana",
                     description="One of Lugana's most mineral and terroir-precise wines — Turbiana from the Le Creete chalk-clay soils on the southern Lake Garda shore. White peach, lime, almond blossom, lake mineral, fennel, and a chalk precision that distinguishes this from the richer, more oaked Ca' dei Frati style. Fresh, precise, and with the texture to develop over 5-7 years. The mineral face of Lugana at its most transparent.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ott, "Carpaccio di persico reale (lake perch carpaccio) with lemon, capers, and arugula", "complement", "classic", "starter", "Lake Garda's finest raw freshwater fish preparation and its most mineral white wine — Lugana's chalk mineral and almond blossom character bridges the delicate perch; capers add saline mineral depth; lemon bridges the wine's citrus freshness")
    PAIR(prod_ott, "Trota in saor (Lake Garda trout in Venetian sweet-sour marinade with raisins and pine nuts)", "complement", "classic", "main", "The ancient Venetian lake preservation technique and the white wine of the lake — Lugana's mineral freshness cuts through the saor's sweet-acid marinade; raisins' sweetness bridges the wine's white peach character; pine nuts bridge the almond note")

# ── PRIMITIVO DI MANDURIA DOC (ITALY) ─────────────────────────────
print("\n=== Primitivo di Manduria DOC (Italy) ===")
r_pri = R("Primitivo di Manduria", "Italy", "wine",
           designation_type="DOC",
           designation_name="Primitivo di Manduria DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Puglia's most celebrated and internationally recognized red wine DOC — the Taranto peninsula and Primitivo di Manduria Secco (dry) and Primitivo di Manduria Dolce Naturale DOCG (sweet) producing Primitivo (genetically identical to California's Zinfandel) of extraordinary concentration, richness, and dark fruit character from head-trained bush vines (alberello) on the Mediterranean terra rossa soils. Primitivo di Manduria's combination of 15-17% natural alcohol, intense dark fruit, and the complexity of very old alberello vines has attracted international collectors seeking Italy's most hedonistic red wines. The Dolce Naturale DOCG — a rare passito-style sweet Primitivo — is one of Italy's most distinctive and underrated dessert wines.",
           key_producers="Pervini (Sessantanni), Felline, Morella, Gianfranco Fino, Accademia dei Racemi, Soloperto",
           historical_context="Primitivo's genetic relationship to Zinfandel was confirmed definitively by DNA analysis in 1994 by Dr. Carole Meredith of UC Davis — tracing the variety from its Croatian ancestor Crljenak Kaštelanski through Puglia to California. The discovery created a permanent cultural connection between Primitivo di Manduria and Zinfandel producers in California, with regular cross-cultural wine events and collaborations. The Sessantanni (60 years old vines) from Pervini launched in 2009 triggered international collector interest in Primitivo di Manduria, demonstrating that the variety from ancient alberello vines could produce wines of genuine complexity and aging potential beyond simple fruit-bomb indulgence.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Primitivo di Manduria vintage; ancient alberello Primitivo from terra rossa showed extraordinary dark fruit concentration and the variety's characteristic power."),
    (2021, "very_good", "stable", "Classic vintage; Mediterranean summer produced wines of excellent concentration and the rich plum-chocolate character of great alberello Primitivo."),
    (2020, "excellent", "stable", "Benchmark year; Pervini Sessantanni and Gianfranco Fino Es both received extraordinary international attention; the 'Puglia revolution' in full force."),
    (2019, "exceptional", "rising", "Greatest Primitivo vintage of the modern era; old-vine alberello wines of historic concentration and 15+ year aging potential; prices rose dramatically."),
    (2018, "very_good", "stable", "Warm vintage producing generous Primitivo of excellent dark fruit richness; terra rossa soils expressed the variety's characteristic blueberry and tobacco complexity."),
]:
    VIN(r_pri, yr, qd, pt, sn)

p_per = P("Pervini", "Italy", r_pri,
           description="The producer that triggered the Primitivo di Manduria collector revolution — Pervini's Sessantanni (60-year-old vines) launched in 2009 demonstrated that ancient alberello Primitivo from Manduria's terra rossa could produce wines of genuine complexity and international stature. The Sessantanni has been placed on the lists of Italy's finest restaurants and has made Pervini the most globally recognized Primitivo di Manduria name.")
prod_per, new = PROD("Pervini Sessantanni Primitivo di Manduria", "wine_still", p_per, r_pri, "Italy",
                     subcategory="Primitivo",
                     description="The wine that redefined Primitivo di Manduria for international collectors — Primitivo from 60-year-old alberello bush vines on terra rossa, 15.5% natural alcohol, aged in large oak. Extraordinary concentration: blueberry jam, dark chocolate, tobacco, leather, dried herbs, Mediterranean spice, and a richness that is more complex and structured than its alcohol suggests. Develops magnificently over 8-12 years into something of genuine southern Italian grandeur.",
                     price_tier="premium")
if new:
    PAIR(prod_per, "Orecchiette con cime di rapa (Puglia pasta with turnip greens and anchovy)", "contrast", "established", "main", "Puglia's most iconic pasta dish and its most powerful red — the bitter greens and anchovy contrast Primitivo's dark fruit and power; the wine's concentration needs the vegetable bitterness as a foil")
    PAIR(prod_per, "Bombette pugliesi (pork rolls stuffed with caciocavallo and herbs) from the butcher's spit", "complement", "classic", "main", "Puglia's most beloved street food from Cisternino and its most celebrated wine — Primitivo's dark fruit and tobacco bridges the caciocavallo-stuffed pork; herb stuffing bridges the wine's Mediterranean complexity")
else:
    # Product already inserted (prior run failed mid-batch) — add pairings directly
    PAIR(prod_per, "Orecchiette con cime di rapa (Puglia pasta with turnip greens and anchovy)", "contrast", "established", "main", "Puglia's most iconic pasta dish and its most powerful red — the bitter greens and anchovy contrast Primitivo's dark fruit and power; the wine's concentration needs the vegetable bitterness as a foil")
    PAIR(prod_per, "Bombette pugliesi (pork rolls stuffed with caciocavallo and herbs) from the butcher's spit", "complement", "classic", "main", "Puglia's most beloved street food from Cisternino and its most celebrated wine — Primitivo's dark fruit and tobacco bridges the caciocavallo-stuffed pork; herb stuffing bridges the wine's Mediterranean complexity")

p_fel = P("Felline", "Italy", r_pri,
           description="Gregory Perrucci's Manduria estate — producing both Primitivo di Manduria and the acclaimed Vigna del Feudo single-vineyard wine from centenarian alberello vines on deep terra rossa. Felline's wines demonstrate Primitivo's capacity for elegance alongside power — the Vigna del Feudo develops over 10+ years into something resembling the great Campanian Aglianicos in structure and complexity.")
prod_fel, new = PROD("Felline Primitivo di Manduria", "wine_still", p_fel, r_pri, "Italy",
                     subcategory="Primitivo",
                     description="The elegant face of Primitivo di Manduria — Gregory Perrucci's alberello old-vine Primitivo from deep terra rossa, more restrained and precise than the Sessantanni hedonism. Dark plum, blueberry, dried herbs, tobacco, and the characteristic southern Italian warmth softened by careful winemaking. More food-friendly than many Primitivo; develops well over 5-7 years. The introduction to understanding the variety's genuine potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_fel, "Agnello alla pugliese (Apulian lamb stew with olives, capers, and tomatoes)", "complement", "classic", "main", "The Apulian tradition of lamb stew and its regional red — Primitivo's dark plum and tobacco bridges the stew's slow-cooked richness; olives' bitterness contrasts the wine's sweetness; capers bridge the wine's Mediterranean herb character")
    PAIR(prod_fel, "Burrata con pomodori di Manduria e basilico (burrata with local tomatoes and basil)", "complement", "established", "starter", "The Puglia summer table — burrata's cream against Primitivo is a contrast pairing that works beautifully; the wine's dark fruit and richness is offset by the cheese's milky freshness; tomatoes' acidity bridges both extremes; basil bridges the Mediterranean herb")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
