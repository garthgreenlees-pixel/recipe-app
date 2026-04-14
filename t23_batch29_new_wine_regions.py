#!/usr/bin/env python3
"""T23 Batch 29 — New wine regions: Brunello di Montalcino DOCG (Italy), Pouilly-Fumé AOC (France), Amarone della Valpolicella DOCG (Italy), Dão DOC (Portugal), Châteauneuf-du-Pape AOC (France)"""

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
    # valid pairing_type: complement, contrast, bridge, cleanse, elevate
    # valid confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── BRUNELLO DI MONTALCINO DOCG (ITALY) ──────────────────────────
print("\n=== Brunello di Montalcino DOCG (Italy) ===")
r_bru = R("Brunello di Montalcino", "Italy", "wine",
           designation_type="DOCG",
           designation_name="Brunello di Montalcino DOCG",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Italy's most prestigious and internationally celebrated red wine DOCG — the Brunello clone of Sangiovese Grosso produced exclusively on the hillsides surrounding the Tuscan hill town of Montalcino at 300-600m elevation. Brunello di Montalcino is Italy's most age-worthy red wine: DOCG regulations require minimum 5 years aging (6 for Riserva), and the finest expressions develop extraordinary complexity over 20-40+ years. The variety's thick skins, high acidity, and substantial tannins combine with Montalcino's unique maritime-continental climate (drier and sunnier than Chianti Classico to the north) to produce wines of legendary longevity. The 2008 Brunellogate scandal — when producers were found to have adulterated Brunello with other varieties — temporarily shook the DOCG's credibility.",
           key_producers="Biondi-Santi, Casanova di Neri, Soldera (Case Basse), Salvioni, Il Poggione, Cerbaiona, Fuligni, Mastrojanni, Ciacci Piccolomini d'Aragona",
           historical_context="Ferruccio Biondi-Santi created Brunello di Montalcino in 1870 by selecting a superior Sangiovese Grosso clone he called 'Brunello' from his Greppo estate. His 1891 and 1925 Brunellos were still being consumed and reviewed in the 1970s — proving the variety's extraordinary longevity. The DOCG was granted in 1980, the first in Italy. A 1955 Biondi-Santi Riserva was famously opened at a Christie's wine auction in 2009 and reported as extraordinary — 54 years old and still vibrant. The estate's pre-phylloxera vines, some 150+ years old on their own rootstocks, remain the most important historical treasure in Italian wine.")

for yr, qd, pt, sn in [
    (2021, "exceptional", "rising", "Widely considered the greatest Brunello vintage since 2010; Sangiovese Grosso of legendary concentration, freshness, and 30+ year aging potential."),
    (2020, "excellent", "stable", "Outstanding vintage; warm, dry conditions produced Brunello of unusual concentration; some of the finest single-vineyard wines of the modern era."),
    (2019, "excellent", "stable", "Benchmark year; the cooler conditions produced wines of elegant structure and the characteristic Brunello freshness; destined for 25+ years."),
    (2018, "excellent", "rising", "Excellent, warm vintage; Brunello of good concentration and dark fruit depth; more approachable than cooler years but still built for 15+ years."),
    (2016, "exceptional", "rising", "Broadly acknowledged as the greatest Brunello vintage of the 21st century; Biondi-Santi and Soldera produced wines of legendary status destined for 40+ years."),
]:
    VIN(r_bru, yr, qd, pt, sn)

p_bio = P("Biondi-Santi", "Italy", r_bru,
           description="The founding dynasty of Brunello di Montalcino and the most historically significant wine estate in Italy — Ferruccio Biondi-Santi created Brunello in 1870 from a superior Sangiovese Grosso selection. The estate's Il Greppo vineyard contains pre-phylloxera Brunello vines planted in the 19th century. The Annata and Riserva wines are released only in exceptional years; the Riserva bottlings from 1888, 1891, 1925, and 1945 are the most historically important bottles in Italian wine. EPI Group (Champagne) acquired the estate in 2017, maintaining all historic practices.")
prod_bio, new = PROD("Biondi-Santi Brunello di Montalcino Annata", "wine_still", p_bio, r_bru, "Italy",
                     subcategory="Sangiovese Grosso",
                     description="The founding wine of Brunello di Montalcino and Italian fine wine's most historical expression — Sangiovese Grosso from Il Greppo's old vines, aged in Slavonian oak. Dried cherry, pomegranate, iron mineral, tobacco, cedar, violets, and the characteristic Brunello austerity that demands patience but rewards magnificently over 20-30 years. At 20 years, develops extraordinary brick-orange complexity unique in Italian wine. The benchmark against which all Brunello is measured.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_bio, "Scottiglia di cinghiale (Tuscan wild boar stew with red wine, herbs, and vegetables)", "complement", "classic", "main", "Montalcino's traditional game stew and its defining wine — Brunello's iron tannin and dried cherry character bridges the wild boar's richness; the wine's herbal complexity mirrors the herbs used in the stew")
    PAIR(prod_bio, "Bistecca alla Fiorentina (T-bone Chianina beef 1kg+) with rosemary, lemon, and sea salt", "complement", "classic", "main", "Italy's greatest beef and its greatest red — Brunello's iron tannin and acidity cuts through the extraordinary fat of a Chianina T-bone; the wine's cherry and tobacco bridges the char of the grill; rosemary mirrors the wine's herbal complexity")

p_cas = P("Casanova di Neri", "Italy", r_bru,
           description="Giacomo and Giovanni Neri's Montalcino estate — producing the most internationally acclaimed modern-style Brunello, including the Cerretalto (from 50-year-old vines on white galestro soils) that received 100/100 from Robert Parker for the 2001 vintage — the highest score ever awarded to an Italian wine. Casanova di Neri's wines are considered the bridge between Brunello's traditional austerity and a more accessible, internationally appealing style.")
prod_cas, new = PROD("Casanova di Neri Brunello di Montalcino Tenuta Nuova", "wine_still", p_cas, r_bru, "Italy",
                     subcategory="Sangiovese Grosso",
                     description="The accessible entry to serious Brunello from Casanova di Neri — Sangiovese Grosso from the Tenuta Nuova vineyards' varied Montalcino soils, aged in medium-sized French and Slavonian oak. Dark cherry, raspberry, dried violets, cedar, tobacco, and the mineral depth that comes from galestro and alberese soils. More approachable than Biondi-Santi's traditional style; develops beautifully over 15+ years. The modern face of Brunello.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_cas, "Pappardelle al ragù di cinghiale (wide pasta ribbons with wild boar ragù)", "complement", "classic", "main", "The Sienese tradition and Brunello — Sangiovese's acidity and cherry character bridges the wild boar ragù's rich depth; pappardelle's wide surface holds the sauce that mirrors the wine's complexity; the wine's tannin handles the richness")
    PAIR(prod_cas, "Pecorino di Pienza stagionato (Sienese aged sheep cheese) with truffle honey and walnuts", "complement", "classic", "cheese", "Montalcino's neighbouring Pienza cheese and its DOCG wine — Brunello's iron mineral and cherry bridges the pecorino's sharp mineral tang; truffle honey amplifies the wine's complexity; walnuts bridge the tannin structure")

# ── POUILLY-FUMÉ AOC (FRANCE) ─────────────────────────────────────
print("\n=== Pouilly-Fumé AOC (France) ===")
r_pfu_l = R("Pouilly-Fumé", "France", "wine",
             designation_type="AOC",
             designation_name="Pouilly-Fumé AOC",
             reputation_tier="prestigious",
             quality_trajectory="established",
             description="The Loire Valley's most prestigious Sauvignon Blanc appellation — the flint, limestone, and clay hillsides above the Loire River at Pouilly-sur-Loire producing Sauvignon Blanc of extraordinary aromatic precision, mineral complexity, and the famous 'gunflint' (pierre à fusil) character that comes from the silex and kimmeridgian limestone soils. Pouilly-Fumé's finest wines — particularly Didier Dagueneau's Silex and Pur Sang from silex soils — achieve a mineral depth and aging potential that challenges Sancerre for the Loire's greatest Sauvignon Blanc. The appellation produces only white wine from 100% Sauvignon Blanc.",
             key_producers="Didier Dagueneau, Henri Bourgeois, Château de Tracy, Jean-Claude Chatelain, Michel Redde",
             historical_context="Didier Dagueneau — the 'wild man of Pouilly' — was the Loire's most eccentric and gifted winemaker: a former dog sled racing champion who became obsessed with creating Sauvignon Blanc of Burgundian mineral complexity. His ultra-low yields (15-20 hl/ha versus the appellation average of 60), individual vine training, and meticulous cellar work produced wines (Silex, Pur Sang, Buisson Renard) that fundamentally changed international perception of Sauvignon Blanc's quality ceiling. His accidental death in 2008 (ultralight aircraft crash) made him wine's most mourned loss of the decade; his son Louis-Benjamin continues the estate with identical obsession.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Pouilly-Fumé vintage; Sauvignon Blanc from silex and kimmeridgian showed extraordinary mineral precision and the gunflint character of the finest parcels."),
    (2021, "very_good", "stable", "Classic vintage; cool Loire conditions produced Pouilly-Fumé of excellent freshness and the characteristic chalk-gunflint mineral that distinguishes the appellation."),
    (2020, "excellent", "stable", "Benchmark year; Louis-Benjamin Dagueneau and Bourgeois both produced wines of extraordinary depth; silex wines of 10+ year aging potential."),
    (2019, "exceptional", "rising", "Greatest Pouilly-Fumé vintage of the era; Sauvignon Blanc of legendary mineral precision; Dagueneau Silex and Pur Sang achieved record prices."),
    (2018, "excellent", "stable", "Outstanding vintage for mineral expression; silex parcels produced wines of exceptional gunflint character and longevity; approachable from 3 years."),
]:
    VIN(r_pfu_l, yr, qd, pt, sn)

p_dag = P("Dagueneau", "France", r_pfu_l,
           description="Louis-Benjamin Dagueneau's Pouilly-Fumé estate — continuing the obsessive work of father Didier, who died in 2008. The Silex (from the distinctive silex/flint soils), Pur Sang (from kimmeridgian clay), and Buisson Renard wines are considered the world's finest Sauvignon Blancs and among the greatest white wines produced anywhere. Ultra-low yields, individual vine selection, and the unique mineral soils of Pouilly create wines of exceptional complexity and longevity that confound those who expect simple Sauvignon.")
prod_dag, new = PROD("Dagueneau Silex Pouilly-Fumé", "wine_still", p_dag, r_pfu_l, "France",
                     subcategory="Sauvignon Blanc",
                     description="The world's benchmark for what Sauvignon Blanc can achieve — Didier Dagueneau's (now Louis-Benjamin's) Silex from the pure flint-silex soils above Pouilly-sur-Loire. Gunflint, smoke, white peach, citrus oil, chalk, and a mineral depth and structure that develops magnificently over 10-15 years. At peak resembles the finest white Burgundy with Sauvignon's unique aromatic signature. The wine that permanently raised the ceiling of what Sauvignon Blanc can be.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_dag, "Homard bleu en coque (live blue lobster in its shell) with tarragon beurre fondue", "complement", "classic", "main", "The Loire's most luxurious pairing — Dagueneau's mineral and citrus oil Sauvignon matches the lobster's oceanic sweetness; tarragon bridges the wine's herbal complexity; beurre fondue mirrors the wine's textural richness")
    PAIR(prod_dag, "Sandre de Loire en carpaccio (Loire perch-pike carpaccio) with trout roe and Pommery mustard vinaigrette", "complement", "classic", "starter", "The Loire river's finest freshwater fish preparation and the Loire's most mineral white — Silex's gunflint and citrus oil character bridges the delicate freshwater fish; trout roe adds marine mineral; mustard bridges the wine's herbal complexity")

p_bou = P("Henri Bourgeois", "France", r_pfu_l,
           description="The Bourgeois family's Sancerre and Pouilly-Fumé estate — the largest and most commercially successful quality producer in the Central Loire, with estate vineyards in both appellations. Henri Bourgeois's D.A. (Demi-Acre) Pouilly-Fumé and the single-vineyard Les Baronnes wines demonstrate the appellation's varied terroir; the family also produces benchmark Sancerre Les Monts Damnés.")
prod_bou, new = PROD("Henri Bourgeois La Demoiselle de Bourgeois Pouilly-Fumé", "wine_still", p_bou, r_pfu_l, "France",
                     subcategory="Sauvignon Blanc",
                     description="The most commercially accessible serious Pouilly-Fumé — Henri Bourgeois's benchmark Sauvignon Blanc from kimmeridgian clay-limestone soils. Grapefruit, lime, gooseberry, white peach, chalk mineral, and a fresh, direct Loire Sauvignon character. More approachable and earlier-drinking than Dagueneau's extreme mineral style; the ideal introduction to understanding what Pouilly-Fumé does differently to Sancerre.",
                     price_tier="mid_range")
if new:
    PAIR(prod_bou, "Crottin de Chavignol (aged Loire goat cheese) with wild garlic pesto and hazelnuts", "complement", "classic", "cheese", "The Central Loire's cheese and wine pairing par excellence — goat cheese and Pouilly-Fumé Sauvignon; the wine's citrus and chalk mineral mirrors the chèvre's lactic freshness; wild garlic bridges the Sauvignon's herbal character")
    PAIR(prod_bou, "Asparagus verte grillée (grilled green asparagus) with sauce gribiche and toasted almonds", "complement", "classic", "starter", "The spring Loire asparagus and its Sauvignon Blanc — Pouilly-Fumé's green, herbal character bridges the asparagus's vegetal intensity; sauce gribiche's acidity mirrors the wine's freshness; almonds bridge the chalk mineral")

# ── AMARONE DELLA VALPOLICELLA DOCG (ITALY) ──────────────────────
print("\n=== Amarone della Valpolicella DOCG (Italy) ===")
r_ama_v = R("Amarone della Valpolicella", "Italy", "wine",
             designation_type="DOCG",
             designation_name="Amarone della Valpolicella DOCG",
             reputation_tier="iconic",
             quality_trajectory="established",
             description="Italy's most powerful, concentrated, and internationally celebrated dry red wine DOCG — the Verona hills northwest of the city producing Amarone from Corvina Veronese, Rondinella, and Molinara grapes dried on bamboo mats (appassimento) for 3-4 months before crushing, reducing water content by 30-40% and concentrating sugars, tannins, and flavours to extraordinary levels. The result is a wine of 15-17% natural alcohol, extraordinary concentration of dark fruit, dried fig, chocolate, and leather, with a finish that can last minutes. The finest Amarone — from Dal Forno Romano and Quintarelli — are among Italy's most sought-after and expensive wines.",
             key_producers="Dal Forno Romano, Quintarelli, Allegrini, Bertani, Masi, Zenato, Tedeschi, Zymé",
             historical_context="Amarone emerged as a distinct wine style accidentally — legend holds that a barrel of Recioto (the sweet version) was forgotten in a cellar and fermented to dryness, becoming 'amaro' (bitter). The first commercial bottling of dry Amarone is credited to Bertani in 1958. Giusto Quintarelli — the 'Pope of Valpolicella' who died in 2012 — produced Amarone of legendary complexity from hand-selected fruit dried in his lofts in Negrar; his wines require 20+ years before peak. Romano Dal Forno's extreme approach — tiny yields, perfect appassimento, long maceration — produces Amarone of supreme concentration that regularly receives the highest scores of any Italian red wine.")

for yr, qd, pt, sn in [
    (2019, "exceptional", "rising", "Broadly considered the greatest Amarone vintage of the modern era; the ideal harvest conditions for appassimento produced wines of legendary concentration and balance."),
    (2017, "excellent", "stable", "Outstanding vintage; warm harvest conditions produced well-dried fruit of excellent sugar concentration; wines of unusual approachability with good structure."),
    (2016, "exceptional", "rising", "Historic Amarone vintage; cool, dry drying conditions produced wines of extraordinary freshness within the typical Amarone power; 25+ year aging potential."),
    (2015, "excellent", "stable", "Excellent vintage; generous, sun-blessed harvest produced Amarone of good concentration and the characteristic dark fruit power; developing well."),
    (2012, "exceptional", "rising", "The 2012 Amarone vintage is being compared to legendary 2001 and 1997; wines of extraordinary complexity now reaching their peak drinking window."),
]:
    VIN(r_ama_v, yr, qd, pt, sn)

p_dal = P("Dal Forno Romano", "Italy", r_ama_v,
           description="The most obsessive and perfectionist Amarone producer — Romano Dal Forno's Illasi estate produces Amarone (and Valpolicella Superiore) from extraordinarily low yields, perfect drying, extended maceration, and new French oak aging for wines of supreme concentration that regularly achieve the highest critical scores of any Italian red. Dal Forno Amarone is allocated to a waiting list; no retail pricing exists; the wines are among Italy's most expensive.")
prod_dal, new = PROD("Dal Forno Romano Amarone della Valpolicella", "wine_still", p_dal, r_ama_v, "Italy",
                     subcategory="Corvina",
                     description="Italy's most extreme and sought-after Amarone — Romano Dal Forno's obsessively made wine from ultra-low yields, perfect 90-day appassimento, and extended French oak aging. Extraordinary concentration: dried cherry, blackberry jam, dark chocolate, dried fig, espresso, leather, tar, and a persistence of 60+ seconds. At 15+ years it reveals a complexity that justifies its place among Italy's finest red wines. Not a subtle wine — the maximum expression of the Amarone concept.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_dal, "Risotto all'Amarone con Monte Veronese and Parmigiano-Reggiano", "complement", "classic", "main", "The Veronese tradition of cooking and pairing — risotto braised in Amarone; the wine appears in the dish; the wine's dark fruit and chocolate depth bridges the richness of the rice; Monte Veronese adds the local cheese bridge")
    PAIR(prod_dal, "Brasato all'Amarone (beef chuck braised for 6 hours in Amarone wine) with polenta", "complement", "classic", "main", "The greatest Veronese preparation — beef braised in the wine itself; the wine's extraordinary concentration is echoed and amplified in the braising liquid; polenta provides textural contrast; the circular pairing at its most intense")

p_qui = P("Quintarelli", "Italy", r_ama_v,
           description="Giuseppe Quintarelli's legendary Negrar estate — the 'Pope of Valpolicella' who produced Amarone of mythological complexity until his death in 2012, now continued by his daughter. Quintarelli's Amarone classico (released only after 8-10 years of aging in large old oak) is considered by many critics to be Italy's finest wine in its best vintages — of extraordinary aromatic complexity and longevity, with peak drinking at 25-40 years after harvest.")
prod_qui, new = PROD("Quintarelli Amarone della Valpolicella Classico", "wine_still", p_qui, r_ama_v, "Italy",
                     subcategory="Corvina",
                     description="The most legendary and sought-after Amarone — Giuseppe Quintarelli's hand-selected dried Corvina, Rondinella, and other Valpolicella varieties, aged 8-10 years in large old Slavonian oak before release. Dried cherry, tobacco, leather, violets, dried fig, spice, cedar, and an ethereal complexity that develops for 30-40 years. Restrained relative to Dal Forno's power; more about complexity than concentration. One of Italy's 5 greatest wines in peak vintages.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_qui, "Soppressa veronese (aged Veronese pork salami) with figs, walnuts, and aged Monte Veronese", "complement", "classic", "aperitif", "The Veronese charcuterie tradition and its greatest wine — Quintarelli's dried fruit complexity bridges the aged salami's depth; figs mirror the wine's dried fig character; walnuts bridge the tobacco and leather; Monte Veronese ties the regional identity")
    PAIR(prod_qui, "Formaggio di Garda Monte Veronese d'Allevo (6-month aged cheese) with acacia honey and truffle", "complement", "classic", "cheese", "The Veronese aged cheese and Amarone — Monte Veronese d'Allevo's sharp aged character meets Quintarelli's dried cherry and tobacco complexity; honey mirrors the wine's fruit; truffle amplifies the earthy complexity")

# ── DÃO DOC (PORTUGAL) ────────────────────────────────────────────
print("\n=== Dão DOC (Portugal) ===")
r_dao = R("Dão", "Portugal", "wine",
           designation_type="DOC",
           designation_name="Dão DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Portugal's most critically underappreciated and rapidly improving red wine DOC — the granite mountain plateau of central Portugal between the Serra da Estrela and Serra do Caramulo, producing Touriga Nacional, Tinta Roriz (Tempranillo), Alfrocheiro, and Jaen (Mencía) blended reds of extraordinary structure, mineral depth, and longevity. Dão's granite and schist soils and high altitude (400-800m) create ideal conditions for wines of freshness and complexity that rival Portugal's finest. The region also produces outstanding white wines from Encruzado — Portugal's most distinctive white variety — of extraordinary mineral complexity that develops like great white Burgundy.",
           key_producers="Quinta dos Roques, Quinta da Pellada (Álvaro Castro), Quinta do Crasto (not Dão), Luis Pato (Bairrada), Caves Aliança",
           historical_context="Dão was Portugal's first regulated wine region (1908), but for much of the 20th century its wines were monopolized by cooperatives producing mediocre bulk wine — a legacy of Salazar's corporatist economic policies that assigned wine production to regional cooperatives and banned private estates from using their own labels. When Portugal joined the EEC in 1986 and the cooperatives were broken up, private estates like Quinta dos Roques and Quinta da Pellada began producing single-estate wines that demonstrated Dão's extraordinary potential. Álvaro Castro's obsessive focus on old-vine Encruzado for white wine and Touriga Nacional for red established Dão as Portugal's most intellectually compelling wine region.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Dão vintage; Touriga Nacional from granite showed extraordinary dark cherry depth and mineral freshness; Encruzado whites of rare complexity."),
    (2021, "very_good", "stable", "Classic vintage; mountain altitude preserved freshness in warm Portuguese conditions; Dão reds of excellent structure and bright fruit character."),
    (2020, "excellent", "stable", "Benchmark year; Quinta dos Roques and Álvaro Castro both produced wines of extraordinary depth; international critics' rediscovery of Dão accelerated."),
    (2019, "excellent", "rising", "Outstanding vintage; Encruzado white wines of exceptional mineral depth received extraordinary attention; Dão's position as Portugal's quality leader solidified."),
    (2018, "very_good", "stable", "Warm vintage producing generous Dão reds of good concentration; granite soils maintained freshness and the characteristic mineral structure of the appellation."),
]:
    VIN(r_dao, yr, qd, pt, sn)

p_roq = P("Quinta dos Roques", "Portugal", r_dao,
           description="The Louro family's Dão estate — one of the private producers who demonstrated the region's potential after the cooperative era ended. The estate's Touriga Nacional, Alfrocheiro, and Encruzado whites from granite soils are considered Dão's benchmark wines for quality and consistency. Quinta dos Roques has been central to establishing Dão's reputation internationally as Portugal's most complex and mineral wine region.")
prod_roq, new = PROD("Quinta dos Roques Dão Touriga Nacional", "wine_still", p_roq, r_dao, "Portugal",
                     subcategory="Touriga Nacional",
                     description="Dão's benchmark single-varietal Touriga Nacional — from the granite plateau's 400m+ elevation, the variety expresses remarkable freshness alongside the expected dark fruit intensity. Wild blackberry, dried rose, cedar, granite mineral, violet, and a structured precision that develops magnificently over 10-15 years. More mineral and fresh than Douro Touriga Nacional; a demonstration of altitude's transforming effect on Portugal's finest native variety.",
                     price_tier="mid_range")
if new:
    PAIR(prod_roq, "Leitão da Bairrada (roast suckling pig) with orange, garlic, and cumin rub", "complement", "classic", "main", "Central Portugal's most famous preparation and its neighbouring Dão wine — Touriga Nacional's dark fruit and mineral depth bridges the suckling pig's rich crackled fat; orange mirrors the wine's floral aromatics; cumin bridges the wine's herbal complexity")
    PAIR(prod_roq, "Chanfana (slow-braised goat in red wine with paprika and bay) on corn bread", "complement", "classic", "main", "Dão's most traditional preparation — old goat braised for hours in red wine until the collagen dissolves; Touriga Nacional's structure and dark cherry bridges the dish's concentrated depth; the wine appears in the braising liquid")

p_pel = P("Quinta da Pellada", "Portugal", r_dao,
           description="Álvaro Castro's historic Dão estate — the estate that has done most to elevate Dão's critical reputation internationally, producing exceptional single-vineyard Encruzado (Garrafeira Encruzado — released 5-6 years after harvest) and Touriga Nacional reds of extraordinary mineral precision. Castro's obsessive focus on old vines, low yields, and minimal intervention has made Quinta da Pellada Dão's most critically celebrated and internationally recognized address.")
prod_pel, new = PROD("Quinta da Pellada Encruzado Dão Branco", "wine_still", p_pel, r_dao, "Portugal",
                     subcategory="Encruzado",
                     description="Portugal's most distinctive white wine — Álvaro Castro's Encruzado from old-vine granite Dão soils, aged in used French oak with extended lees contact. Extraordinary mineral complexity: quince, hazelnut, white peach, granite stone, toasted almond, and a waxy texture that develops over 8-10 years into something resembling great white Burgundy. The wine that proved Encruzado deserves to be spoken of alongside Chardonnay as Portugal's finest white variety.",
                     price_tier="premium")
if new:
    PAIR(prod_pel, "Bacalhau à brás (salt cod with scrambled eggs, olives, and fried potatoes)", "complement", "classic", "main", "Portugal's most universally beloved dish and its finest white wine — Encruzado's mineral complexity and texture matches the salt cod's intense salinity; eggs add richness that bridges the wine's hazelnut; olives' bitterness mirrors the wine's mineral depth")
    PAIR(prod_pel, "Trutas do Mondego (Mondego river trout) with broa (corn bread), lemon, and herbs", "complement", "classic", "main", "The Dão region's river trout from the Mondego and its greatest white wine — Encruzado's granite mineral and hazelnut character bridges the trout's delicate freshwater flesh; broa's corn sweetness contrasts the wine's mineral austerity; herbs bridge the wine's complexity")

# ── CHÂTEAUNEUF-DU-PAPE AOC (FRANCE) ─────────────────────────────
print("\n=== Châteauneuf-du-Pape AOC (France) ===")
r_cdp = R("Châteauneuf-du-Pape", "France", "wine",
           designation_type="AOC",
           designation_name="Châteauneuf-du-Pape AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="France's most celebrated and historically significant southern Rhône wine appellation — the papal city's vineyards on galets roulés (rounded river stones) and sand-limestone soils north of Avignon, producing powerful, complex red wines from up to 18 permitted grape varieties led by Grenache, Syrah, and Mourvèdre, and distinctive white wines from Grenache Blanc, Clairette, Roussanne, and Viognier. The galets roulés — round stones of Miocene origin that retain daytime heat and release it at night — are the appellation's iconic image. Châteauneuf-du-Pape's red wines range from the Grenache-dominant (pure, aromatic, accessible) to GSM blends (powerful, tannic, age-worthy) to the estate-specific styles of legendary producers.",
           key_producers="Château Rayas, Château Beaucastel, Château la Nerthe, Château Fortia, Domaine du Vieux Télégraphe, Henri Bonneau, Domaine de la Janasse",
           historical_context="The Avignon papacy (1309-1377) gave the appellation its name — the papal summer residence (Châteauneuf) was surrounded by vineyards planted by Pope John XXII in 1317. When Baron Le Roy de Boiseaumarié of Château Fortia created the first appellation contrôlée rules for Châteauneuf-du-Pape in 1923 (predating the national AOC system by 13 years), he established the template for French wine law — including permitted varieties, minimum alcohol levels, and geographical delimitation — that became the model for all French AOC regulations. Château Rayas's Grenache-only wines (100% from sandy soil parcels) are considered the appellation's most sought-after and age-worthy wines, rivaling Burgundy's finest for complexity.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Châteauneuf vintage; Grenache from galets roulés showed extraordinary aromatic richness; GSM blends of excellent structure and 20+ year potential."),
    (2021, "very_good", "stable", "Classic vintage; cooler conditions produced wines of excellent freshness and the characteristic Châteauneuf aromatic complexity; Grenache Blanc whites exceptional."),
    (2020, "excellent", "stable", "Benchmark year; Château Rayas and Beaucastel both produced wines of extraordinary depth; whites of unusual mineral freshness alongside the powerful reds."),
    (2019, "exceptional", "rising", "Greatest Châteauneuf vintage of the era; Grenache of legendary aromatic intensity and longevity; estate wines achieved record prices at auction."),
    (2016, "exceptional", "rising", "Widely considered the finest Châteauneuf vintage since 2010; wines of outstanding balance, structure, and the Grenache aromatic complexity that defines the appellation's greatness."),
]:
    VIN(r_cdp, yr, qd, pt, sn)

p_ray = P("Château Rayas", "France", r_cdp,
           description="The most legendary and sought-after estate in Châteauneuf-du-Pape — Emmanuel Reynaud's eccentric family domaine produces 100% Grenache wines from sandy soil parcels (the variety's preferred terrain, creating purity rather than power) of extraordinary aromatic complexity, transparency, and longevity that regularly blind-taste as premier cru Burgundy. Château Rayas is one of France's most allocated and expensive wines, released through a restricted list of négociants and collected globally.")
prod_ray, new = PROD("Château Rayas Châteauneuf-du-Pape Rouge", "wine_still", p_ray, r_cdp, "France",
                     subcategory="Grenache",
                     description="France's most sought-after Châteauneuf-du-Pape and one of the country's greatest red wines — 100% Grenache from sandy parcels, producing transparency and aromatic complexity that defies the appellation's powerful reputation. Raspberry, dried cherry, violet, kirsch, garrigue, forest floor, and a haunting delicacy that develops over 20-30 years into something that repeatedly confounds Burgundy specialists in blind tastings. Allocated, rare, and extraordinary.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_ray, "Agneau de Sisteron (Provençal lamb rack) with herbes de Provence, garlic, and tapenade croûte", "complement", "classic", "main", "The southern Rhône's finest lamb and its most legendary Grenache — the wine's dried cherry and garrigue character bridges Provençal lamb's herb-scented fat; tapenade's olive bitterness mirrors the wine's earthy complexity; herbes de Provence amplifies the garrigue notes")
    PAIR(prod_ray, "Truffes noires du Ventoux (black truffle) with scrambled eggs, sea salt, and brioche", "complement", "classic", "starter", "One of France's great luxury pairings — Provence black truffle and Châteauneuf Grenache; the wine's forest floor and dried cherry complexity resonates with truffle's earthy depth; eggs provide a neutral canvas; brioche mirrors the wine's kirsch richness")

p_bea = P("Château Beaucastel", "France", r_cdp,
           description="The Perrin family's 100-hectare Châteauneuf-du-Pape estate — producing wines from all 18 permitted varieties with Mourvèdre dominant in the red (unusual in the appellation) and Roussanne dominant in the white (the Roussanne Vieilles Vignes is France's finest expression of the variety). Beaucastel Hommage à Jacques Perrin from very old Mourvèdre vines is one of the appellation's most powerful and long-lived wines; the regular Châteauneuf-du-Pape Rouge requires 15+ years to show its potential.")
prod_bea, new = PROD("Château Beaucastel Châteauneuf-du-Pape Rouge", "wine_still", p_bea, r_cdp, "France",
                     subcategory="Grenache Mourvèdre blend",
                     description="The most internationally recognized and reliably structured Châteauneuf-du-Pape — Grenache, Mourvèdre, Syrah, and all 18 permitted varieties farmed biodynamically on galets roulés. Dark cherry, dried leather, garrigue, tobacco, iron mineral, and the characteristic Beaucastel Mourvèdre structure that rewards patience over 15+ years. The reference for the appellation's more complex, tannic style; cellar essential for the serious Rhône collector.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_bea, "Daube de boeuf provençale (Provençal beef stew with olives, orange, and herbes de Provence)", "complement", "classic", "main", "The Languedoc-Provence tradition and southern Rhône's most complex wine — Beaucastel's Mourvèdre structure and dark leather character bridges the beef daube's concentrated richness; olives mirror the wine's mineral depth; orange bridges the dried cherry")
    PAIR(prod_bea, "Sanglier en civet (wild boar in red wine sauce) with chestnuts and cèpes", "complement", "classic", "main", "Wild boar and Châteauneuf — the most natural pairing in Provence; Beaucastel's power and leather complexity matches the wild boar's assertive gamey richness; chestnuts bridge the wine's iron mineral; cèpes amplify the earthy tobacco notes")

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
