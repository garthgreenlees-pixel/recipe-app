#!/usr/bin/env python3
"""T23 Batch 23 — New wine regions: Willamette Valley AVA (USA), Ribera del Duero DO (Spain), Soave DOC (Italy), Muscadet Sèvre et Maine AOC (France), Txakoli de Getaria DO (Spain)"""

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

# ── WILLAMETTE VALLEY AVA (USA) ───────────────────────────────────
print("\n=== Willamette Valley AVA (USA) ===")
r_wil = R("Willamette Valley", "USA", "wine",
           designation_type="AVA",
           designation_name="Willamette Valley AVA",
           reputation_tier="iconic",
           quality_trajectory="ascending",
           description="Oregon's supreme wine valley and America's most important Pinot Noir AVA — a long trough between the Coast Range and the Cascades in northwestern Oregon, blessed with cool maritime influence, diverse Jory and Missoula Flood sedimentary soils, and a long growing season ideal for Burgundian varieties. Willamette Valley's best Pinot Noir rivals Burgundy's finest at a fraction of the price. The valley is divided into six distinct sub-AVAs — Chehalem Mountains, Dundee Hills, Eola-Amity Hills, McMinnville, Ribbon Ridge, and Yamhill-Carlton — each with distinct soil types and microclimates. Chardonnay and Pinot Gris are also regionally significant.",
           key_producers="Eyrie Vineyards, Domaine Drouhin Oregon, Ponzi Vineyards, Adelsheim Vineyard, Argyle Winery, Evening Land, Beaux Frères, Rex Hill",
           historical_context="David Lett of Eyrie Vineyards planted the first Pinot Noir vines in the Willamette Valley in 1966, defying Oregon's agricultural establishment who dismissed the project as folly. When Eyrie's 1975 South Block Pinot Noir placed second in a blind Paris tasting against top Burgundies in 1979, Robert Drouhin of Burgundy was so impressed he purchased land in the Dundee Hills and established Domaine Drouhin Oregon — cementing the valley's international reputation. Oregon's 1977 wine law requiring minimum 90% varietal labeling (versus California's 75%) established the quality ethos that defines Willamette today.")

for yr, qd, pt, sn in [
    (2022, "very_good", "rising", "Warm, dry Willamette vintage producing concentrated, structured Pinot Noir with exceptional colour and extract; Chardonnay of surprising richness."),
    (2021, "exceptional", "rising", "Widely considered the greatest Willamette vintage ever produced; Pinot Noir of extraordinary aromatic complexity, structure, and aging potential."),
    (2020, "good", "stable", "Challenging vintage affected by wildfire smoke; careful producers made elegant, pale Pinot Noir from smoke-free parcels; not a collector's year but honest wines."),
    (2019, "excellent", "rising", "Benchmark Willamette year; classic cool-climate conditions produced Pinot Noir of silky texture, red fruit clarity, and enviable natural acidity."),
    (2018, "excellent", "stable", "Warm and precocious vintage; Pinot Noir of generous fruit concentration; Dundee Hills Jory soil wines showed excellent mineral backbone."),
]:
    VIN(r_wil, yr, qd, pt, sn)

p_eye = P("Eyrie Vineyards", "USA", r_wil,
           description="The founding estate of Oregon wine — David Lett planted the first Willamette Valley Pinot Noir vines in 1966 and his 1975 South Block placed second against top Burgundies in Paris, igniting the Oregon wine revolution. The Eyrie Vineyards Original Vines Pinot Noir, from the oldest Pinot Noir vines in the Pacific Northwest, remains Oregon's most historically significant wine and the benchmark for Willamette terroir expression.")
prod_eye, new = PROD("Eyrie Vineyards Original Vines Pinot Noir", "wine_still", p_eye, r_wil, "USA",
                     subcategory="Pinot Noir",
                     description="Oregon's most historically significant wine — Pinot Noir from vines planted by David Lett in 1966, the oldest in the Pacific Northwest. Haunting transparency, dried cherry, dried rose, earth, cedar, and the cool maritime mineral depth that Willamette Valley's original visionary identified in the Dundee Hills red Jory volcanic soils. Understated, complex, and irreplaceable.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_eye, "Roasted Oregon hazelnut-crusted duck breast with pinot reduction and wild mushrooms", "complement", "classic", "main", "Oregon duck and Oregon's founding Pinot Noir — the wine's dried cherry and earth character bridges the duck's richness; hazelnuts mirror the wine's subtle nutty depth; wild mushrooms amplify the forest floor quality")
    PAIR(prod_eye, "Pacific Northwest chanterelle risotto with aged Tillamook cheddar and fresh thyme", "complement", "classic", "main", "Willamette Valley's forest floor chanterelles and the valley's founding Pinot — the wine's earth and cherry character mirrors the chanterelle's golden depth; thyme bridges the wine's herbal notes")

p_ddo = P("Domaine Drouhin Oregon", "USA", r_wil,
           description="Robert Drouhin of Beaune's Domaine Drouhin purchased Dundee Hills land in 1987 after his daughter Véronique placed Eyrie's 1975 against Burgundies — establishing the gold standard of Burgundian investment in Oregon. Véronique Drouhin-Boss crafts the Domaine's flagship Pinot Noir and Chardonnay with Burgundian precision from Jory volcanic soils. The Domaine's presence validated Willamette Valley to the Burgundian establishment.")
prod_ddo, new = PROD("Domaine Drouhin Oregon Dundee Hills Pinot Noir", "wine_still", p_ddo, r_wil, "USA",
                     subcategory="Pinot Noir",
                     description="The Burgundian benchmark for Willamette Valley — Véronique Drouhin-Boss's Dundee Hills Pinot Noir from the distinctive Jory volcanic red soils that give Oregon Pinot its characteristic structure and mineral depth. Red cherry, strawberry, violet, cedar, and the precise, cool-climate elegance that makes this wine the bridge between Burgundy and Oregon. The defining statement of what Willamette can achieve.",
                     price_tier="premium")
if new:
    PAIR(prod_ddo, "Grilled Oregon king salmon with sorrel beurre blanc and spring pea purée", "complement", "classic", "main", "The Pacific Northwest's greatest fish and Oregon's most Burgundian Pinot Noir — salmon's rich oil bridges the wine's cherry and mineral character; sorrel's acidity mirrors the wine's freshness; pea purée's sweetness complements the red fruit")
    PAIR(prod_ddo, "Slow-roasted Willamette Valley lamb with rosemary, garlic, and potato gratin", "complement", "established", "main", "Oregon lamb and the Dundee Hills Pinot — the wine's structure and minerality supports the lamb's richness; rosemary bridges the wine's herbal notes; garlic's transformation to sweetness complements the red fruit character")

# ── RIBERA DEL DUERO DO (SPAIN) ───────────────────────────────────
print("\n=== Ribera del Duero DO (Spain) ===")
r_rdd = R("Ribera del Duero", "Spain", "wine",
           designation_type="DO",
           designation_name="Ribera del Duero DO",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Spain's most celebrated and powerful red wine DO — the Duero River valley on the Castilian meseta at 850m elevation, producing Tempranillo (locally called Tinto Fino or Tinta del País) of extraordinary concentration, structure, and aging potential. The extreme continental climate — sub-zero winters, scorching summers, dramatic diurnal temperature variation of 20°C+ — stresses the vines and concentrates flavour to levels unmatched anywhere in Spain. Ribera del Duero's greatest wines — Vega Sicilia Único and Pingus — are among the most expensive and sought-after wines on earth.",
           key_producers="Vega Sicilia, Pingus, Emilio Moro, Pago de Carraovejas, Abadía Retuerta, Protos, Aalto, Pesquera",
           historical_context="Vega Sicilia planted the valley's first experimental vineyards in 1864 using Bordeaux varieties alongside Tinto Fino, but the region's potential was largely ignored until Alejandro Fernández of Bodegas Pesquera demonstrated in 1972 that Tinto Fino alone could produce world-class wine without Bordeaux varieties. The DO was created in 1982, and by 1991 Pesquera's wines had been called 'the Petrus of Spain' by Robert Parker, triggering international investment. Peter Sisseck's Pingus (1995) — initially just 4 barrels — became Spain's most expensive wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Ribera vintage; extreme diurnal variation produced Tinto Fino of exceptional concentration and freshness; long-lived wines in prospect."),
    (2021, "very_good", "stable", "Classic vintage; the Castilian meseta's cold nights preserved acidity in concentrated Tempranillo of excellent structure and dark fruit depth."),
    (2020, "excellent", "stable", "Benchmark year; drought conditions stressed vines producing wines of extraordinary concentration; Emilio Moro and Pago de Carraovejas both excellent."),
    (2019, "exceptional", "rising", "Greatest Ribera vintage of the modern era; Tinto Fino of historic concentration, structure, and longevity — comparable to the legendary 1994 vintage."),
    (2018, "excellent", "stable", "Excellent vintage; warm, dry conditions produced generous, approachable Ribera with excellent dark fruit density and supple tannins."),
]:
    VIN(r_rdd, yr, qd, pt, sn)

p_emo = P("Emilio Moro", "Spain", r_rdd,
           description="The Moro family's benchmark Ribera del Duero estate — founded in 1932 and dedicated exclusively to old-vine Tinto Fino from the highest-elevation Peñafiel parcels. Emilio Moro's wines represent the most consistent quality-to-price ratio in the DO; the flagship Malleolus de Valderramiro from pre-phylloxera vines is considered one of Spain's finest wines.")
prod_emo, new = PROD("Emilio Moro Malleolus Ribera del Duero", "wine_still", p_emo, r_rdd, "Spain",
                     subcategory="Tempranillo",
                     description="The benchmark for approachable Ribera del Duero greatness — Tinto Fino from old Peñafiel vines aged in French and American oak. Dark plum, blackberry, cedar, tobacco, leather, and the characteristic iron-mineral depth of Ribera's high-altitude limestone soils. Generous, structured, and capable of 15+ years of development. Spain's most consistent value at the serious level.",
                     price_tier="premium")
if new:
    PAIR(prod_emo, "Roast suckling pig (cochinillo asado) with crispy crackling and natural juices", "complement", "classic", "main", "Castile's most iconic dish and its benchmark wine — the wine's dark fruit and structure handles the pig's richness; crackling's texture contrasts the wine's plush tannins; natural juices bridge the wine's mineral depth")
    PAIR(prod_emo, "Grilled Castilian lamb chops (chuletillas) with rock salt, garlic, and thyme", "complement", "classic", "main", "Ribera del Duero lamb and Ribera del Duero wine — the synergy of terroir; the wine's plummy depth and firm tannins match the lamb's char and fat; garlic bridges the wine's complexity")

p_pdc = P("Pago de Carraovejas", "Spain", r_rdd,
           description="José María Ruiz's prestige Ribera del Duero estate — one of the DO's most consistently acclaimed producers for luxury-level Tinto Fino wines blended with Cabernet Sauvignon and Merlot. The flagship Cuesta de las Liebres (Slope of the Hares) comes from a single high-altitude vineyard of extraordinary limestone complexity. Pago de Carraovejas wines appear on the wine lists of Spain's finest restaurants.")
prod_pdc, new = PROD("Pago de Carraovejas Crianza Ribera del Duero", "wine_still", p_pdc, r_rdd, "Spain",
                     subcategory="Tempranillo",
                     description="Ribera del Duero's benchmark prestige Crianza — Tinto Fino with Cabernet Sauvignon from high-elevation limestone parcels, aged in French oak with meticulous precision. Blackcurrant, dark cherry, violets, cedar, dark chocolate, and the powerful but polished structure that places Carraovejas among the DO's finest. The entry point to one of Spain's great estates.",
                     price_tier="premium")
if new:
    PAIR(prod_pdc, "Ibérico presa (shoulder cap) with Moros y Cristianos (black beans and rice)", "complement", "classic", "main", "Spain's finest pork cut and Ribera's most structured Crianza — the wine's blackcurrant and cedar character bridges the ibérico's complex fat; beans' earthiness mirrors the wine's mineral depth")
    PAIR(prod_pdc, "Manchego curado with quince paste (membrillo), Marcona almonds, and smoked paprika oil", "bridge", "classic", "cheese", "The classic Castilian cheese board and the Castilian red — the wine's dark fruit bridges Manchego's nutty tang; membrillo's sweetness mirrors the wine's dark plum; paprika bridges the oak spice")

# ── SOAVE DOC (ITALY) ─────────────────────────────────────────────
print("\n=== Soave DOC (Italy) ===")
r_soa = R("Soave", "Italy", "wine",
           designation_type="DOC",
           designation_name="Soave DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The Veneto's most important white wine DOC and one of Italy's most historically significant — a zone east of Verona on volcanic basalt and limestone hillsides producing Garganega (minimum 70%) and Trebbiano di Soave. For decades Soave's reputation was damaged by industrial overproduction in the plains, but the Soave Classico zone on the original volcanic hillsides — and especially Soave Superiore DOCG from the finest terroirs — is producing wines of extraordinary mineral complexity, floral delicacy, and surprising longevity that rank among Italy's finest whites.",
           key_producers="Pieropan, Gini, Inama, Prà, Coffele, Ca' Rugate, Filippi",
           historical_context="Soave's medieval castle gave the wine its name (derived from 'suaves' — the Swabian German tribe that settled the hills in the 6th century). By the 1970s, Soave had become Italy's most exported white wine, but overproduction in the Soave Esteso plains destroyed its reputation. The Soave Revival began in the 1990s when Pieropan's Calvarino single-vineyard wine demonstrated that volcanic hillside Garganega was a white wine of Chablis-level complexity. The DOCG Soave Superiore designation was created in 2001 to protect the Classico hillside zone.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Soave vintage; Garganega from volcanic basalt showed extraordinary mineral precision and the characteristic almond-bitter finish of great Classico."),
    (2021, "very_good", "stable", "Elegant vintage; cool conditions preserved Garganega's delicate floral aromatics and the mineral freshness of the volcanic hillsides."),
    (2020, "excellent", "stable", "Benchmark year; Pieropan Calvarino and Gini La Froscà both produced single-vineyard Soave of international renown."),
    (2019, "excellent", "rising", "Outstanding vintage; Soave Superiore DOCG wines of exceptional depth and longevity potential; international wine press rediscovery of Soave in earnest."),
    (2018, "very_good", "stable", "Classic vintage; volcanic basalt hillsides produced wines of good mineral intensity; almond and white blossom character of authentic Classico well expressed."),
]:
    VIN(r_soa, yr, qd, pt, sn)

p_pie = P("Pieropan", "Italy", r_soa,
           description="The estate that saved Soave's reputation — Leonildo Pieropan's insistence on hillside Garganega when all his neighbours expanded into the plains produced wines that demonstrated Soave's potential for world-class white wine. The Calvarino and La Rocca single-vineyard wines are considered Italy's benchmark dry Garganega and among the finest white wines produced anywhere in Italy.")
prod_pie, new = PROD("Pieropan Calvarino Soave Classico", "wine_still", p_pie, r_soa, "Italy",
                     subcategory="Garganega",
                     description="The wine that rescued Soave's international reputation — Garganega from the Calvarino volcanic basalt hillside, aged in large Slovenian oak. Golden apple, white peach, almond blossom, bitter almond, volcanic mineral, and a haunting bitter-mineral finish that develops magnificently over 10+ years. Italy's benchmark dry Garganega and proof that Soave belongs among Italy's finest whites.",
                     price_tier="premium")
if new:
    PAIR(prod_pie, "Risotto all'Amarone with radicchio di Treviso and aged Monte Veronese", "contrast", "classic", "main", "The Veneto's contrast pairing — Soave's mineral freshness against Amarone-braised rice; the wine's acidity cuts through the risotto's richness; bitter almond mirrors the radicchio's bitter edge")
    PAIR(prod_pie, "Salt-baked sea bream with lemon, capers, and Soave-braised fennel", "complement", "classic", "main", "The classic Soave pairing — Mediterranean white fish and Garganega mineral wine; the wine's almond and white peach character bridges the fish's delicacy; capers add a saline bridge to the volcanic mineral")

p_gin = P("Gini", "Italy", r_soa,
           description="Sandro and Claudio Gini's biodynamic Soave Classico estate producing the La Froscà single-vineyard wine from volcanic tuff and basalt — considered by many critics the greatest single-vineyard Soave in the appellation. Gini's wines demonstrate the extraordinary mineral complexity achievable from old Garganega vines on the volcanic hillsides of the Classico zone.")
prod_gin, new = PROD("Gini La Froscà Soave Classico Superiore", "wine_still", p_gin, r_soa, "Italy",
                     subcategory="Garganega",
                     description="The rival to Pieropan Calvarino for Soave's greatest single-vineyard — old-vine Garganega from volcanic tuff and basalt farmed biodynamically. Extraordinary mineral depth, white blossom, green apple, almond, volcanic stone, and a texture of uncommon weight for a white wine. The La Froscà develops magnificently over 8-10 years into something resembling great white Burgundy.",
                     price_tier="premium")
if new:
    PAIR(prod_gin, "Bigoli in salsa (thick Venetian pasta with anchovy and onion sauce)", "complement", "established", "main", "The Veneto's most traditional pasta dish and its greatest white wine — the wine's mineral and almond character bridges the anchovy's umami intensity; onion's sweetness contrasts the bitter mineral finish")
    PAIR(prod_gin, "Grilled scallops with cauliflower purée, capers, and toasted pine nuts", "complement", "classic", "main", "Soave's mineral weight and texture supports the scallop's sweet richness; cauliflower's earthiness bridges the volcanic mineral; capers' acidity mirrors the wine's freshness")

# ── MUSCADET SÈVRE ET MAINE AOC (FRANCE) ─────────────────────────
print("\n=== Muscadet Sèvre et Maine AOC (France) ===")
r_mus = R("Muscadet Sèvre et Maine", "France", "wine",
           designation_type="AOC",
           designation_name="Muscadet Sèvre et Maine AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The Loire Valley's most important white wine appellation and France's definitive oyster wine — the western Loire around Nantes producing Melon de Bourgogne (locally known as Muscadet) from granite and gneiss soils, with extended lees aging (sur lie) for complexity. The finest Muscadet — Muscadet de Sèvre et Maine sur Lie, especially the Crus Communaux (Clisson, Gorges, Le Pallet, Goulaine, Mouzillon-Tillières, Château-Thébaud) — achieves a complexity and longevity that confounds those who dismiss it as simple. The best examples spend 12-40+ months on lees, developing extraordinary depth.",
           key_producers="Luneau-Papin, Domaine de la Pépière, Guy Bossard, Château du Coing de Saint Fiacre, Domaine de l'Écu",
           historical_context="Melon de Bourgogne was transplanted to the Loire from Burgundy in 1709 after the great freeze destroyed the existing vineyards — Burgundy's least valued variety became the Loire's most planted. For centuries, Muscadet fed the oyster and mussel trade of the Atlantic ports of Nantes and Saint-Nazaire. The sur lie tradition — leaving the wine on its fermentation lees until bottling — was codified in the 1950s as growers discovered that yeast contact gave the wine a distinctive richness and the characteristic spritz from residual CO2. The Crus Communaux — six communes recognizing the finest terroirs — were created in 2011 to acknowledge that the best Muscadet ages as well as lesser Chablis.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Muscadet vintage; Melon de Bourgogne from granite gneiss showed extraordinary mineral precision; Crus Communaux of exceptional longevity potential."),
    (2021, "very_good", "stable", "Classic vintage; cool Atlantic conditions produced wines of excellent natural acidity and the characteristic saline mineral freshness; ideal sur lie base wines."),
    (2020, "excellent", "stable", "Benchmark year; Luneau-Papin and Pépière's Clisson Cru wines received extraordinary international attention; Muscadet's revival confirmed."),
    (2019, "excellent", "rising", "Outstanding vintage; Crus Communaux wines of exceptional depth; Gorges granite wines showed the variety's ability to rival Chablis at premier cru level."),
    (2018, "very_good", "stable", "Solid vintage; warm conditions produced generous Muscadet of good body; sur lie aging added complexity to wines of unusual richness for the appellation."),
]:
    VIN(r_mus, yr, qd, pt, sn)

p_lup = P("Luneau-Papin", "France", r_mus,
           description="The most critically acclaimed and internationally recognized Muscadet producer — Pierre-Marie Luneau-Papin's estate produces the full range of Muscadet from entry-level to the L d'Or and Clisson Cru wines of extraordinary complexity aged 20-40 months on lees. Luneau-Papin has done more than any other single producer to demonstrate that Muscadet can achieve the complexity and longevity of premier cru Chablis.")
prod_lup, new = PROD("Luneau-Papin Clisson Cru Muscadet Sèvre et Maine sur Lie", "wine_still", p_lup, r_mus, "France",
                     subcategory="Melon de Bourgogne",
                     description="The finest expression of Muscadet's Crus Communaux ambition — Melon de Bourgogne from Clisson's ancient granite and gneiss, aged 30+ months on lees. Saline mineral depth, green apple, lemon curd, brioche from lees contact, chalk, and a persistent mousse-like texture from retained CO2. Profound and age-worthy; the wine that challenges all preconceptions about Muscadet.",
                     price_tier="mid_range")
if new:
    PAIR(prod_lup, "Freshly opened Belon flat oysters with seaweed butter and Muscadet mignonette", "complement", "classic", "aperitif", "The most famous food-wine pairing in the Loire — Muscadet and Atlantic oysters; the wine appears in the mignonette itself; the wine's saline mineral character mirrors the oyster's brine; lees texture bridges the oyster's creaminess")
    PAIR(prod_lup, "Moules marinières (mussels) with white wine, shallots, cream, and parsley", "complement", "classic", "main", "The Loire-Atlantic classic — the Muscadet used to cook the mussels and served alongside; the wine's saline mineral and lees richness mirrors the mussel's briny sweetness; cream bridges the lees texture")

p_pep = P("Domaine de la Pépière", "France", r_mus,
           description="Marc Ollivier's biodynamic Muscadet estate producing the most consistently mineral and individual wines in the appellation — the Clos des Briords and Gorges Cru wines from ancient granite gneiss are considered the definitive expressions of Muscadet's age-worthy potential. Pépière's minimal-intervention winemaking has made it the natural wine community's benchmark for Loire mineral whites.")
prod_pep, new = PROD("Domaine de la Pépière Gorges Cru Muscadet sur Lie", "wine_still", p_pep, r_mus, "France",
                     subcategory="Melon de Bourgogne",
                     description="Muscadet's most mineral and age-worthy expression — Melon de Bourgogne from the Gorges Cru's ancient granite, biodynamically farmed and aged 24+ months on lees. Extraordinary granite mineral depth, saline freshness, green apple, lemon pith, and a crystalline precision that develops over 10+ years into something resembling great Chablis. The natural wine world's benchmark Muscadet.",
                     price_tier="mid_range")
if new:
    PAIR(prod_pep, "Raw Breton langoustines with lemon sea salt and chilled Muscadet butter", "complement", "classic", "main", "The Brittany coast's finest crustacean and its neighbouring Loire wine — the wine's granite mineral and saline character bridges the langoustine's oceanic sweetness; butter bridges the lees texture")
    PAIR(prod_pep, "Pissaladière niçoise-style tart with anchovy, caramelized onion, and black olive tapenade", "complement", "established", "starter", "The wine's saline mineral character bridges the anchovy's intensity; caramelized onion's sweetness contrasts the wine's crisp acidity; olive tapenade's bitterness finds resonance in the granite mineral")

# ── TXAKOLI DE GETARIA DO (SPAIN) ─────────────────────────────────
print("\n=== Txakoli de Getaria DO (Spain) ===")
r_txa = R("Txakoli de Getaria", "Spain", "wine",
           designation_type="DO",
           designation_name="Getariako Txakolina DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The Basque Country's most distinctive wine DO — a tiny coastal zone around the fishing village of Getaria on the Bay of Biscay, producing Txakoli (Txakolina) from Hondarribi Zuri and a small amount of Hondarribi Beltza on steep Atlantic-facing terraces. Txakoli is one of Europe's most thrillingly individual wines: bone dry, low in alcohol (10-11%), with a natural effervescence from CO2 retention, piercing Atlantic minerality, and a salty freshness that makes it arguably the world's perfect aperitif wine and the definitive accompaniment to Basque pintxos.",
           key_producers="Txomin Etxaniz, Ameztoi, Getariako Txakolina producers cooperative, Hiruzta",
           historical_context="Txakoli has been the Basque fishermen's wine for centuries — consumed in the port taverns of Getaria and San Sebastián as the natural partner to the day's catch. The wine's naturally low alcohol and high acidity made it the ideal quenching wine after hauling nets. By the 1970s, production had nearly collapsed as younger Basques preferred Spanish wine styles. The DO's creation in 1990 and the global explosion of interest in Basque cuisine and pintxos culture rescued Txakoli, which now appears on the world's finest restaurant wine lists — poured from height in the traditional style to aerate and emphasize the natural effervescence.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding Txakoli vintage; Atlantic coast conditions produced Hondarribi Zuri of exceptional saline mineral intensity and natural effervescence."),
    (2022, "very_good", "stable", "Classic vintage; Bay of Biscay influence produced wines of excellent natural acidity and the characteristic green apple-citrus freshness of great Txakoli."),
    (2021, "excellent", "stable", "Benchmark year; Txomin Etxaniz and Ameztoi both produced wines of extraordinary Atlantic mineral precision; the global pintxos boom drove prices higher."),
    (2020, "very_good", "stable", "Solid vintage; Atlantic humidity was well managed; Hondarribi Zuri wines of good mineral freshness and the characteristic salty-citrus character."),
    (2019, "excellent", "rising", "Outstanding vintage; Txakoli received exceptional international attention; sommeliers worldwide discovered the wine's versatility beyond pintxos."),
]:
    VIN(r_txa, yr, qd, pt, sn)

p_txo = P("Txomin Etxaniz", "Spain", r_txa,
           description="The founding estate of modern Txakoli and the most internationally recognized producer in Getariako Txakolina — the Txueka family's vineyards on the Atlantic-facing slopes above Getaria produce the benchmark expression of Hondarribi Zuri's saline mineral character. Txomin Etxaniz is served at the Basque Country's finest restaurants and has introduced Txakoli to wine lists from Tokyo to New York.")
prod_txo, new = PROD("Txomin Etxaniz Getariako Txakolina", "wine_still", p_txo, r_txa, "Spain",
                     subcategory="Hondarribi Zuri",
                     description="The world's benchmark Txakoli — Hondarribi Zuri from Atlantic-facing terraces above the Bay of Biscay, bone dry at 10.5% alcohol with natural CO2 effervescence. Salty citrus, green apple, white grapefruit, sea spray mineral, and a scouring freshness unlike any other white wine. Poured from height to maximize the sparkle. The definitive aperitif wine of the Basque Country.",
                     price_tier="mid_range")
if new:
    PAIR(prod_txo, "Pintxos de anchoa del Cantábrico (Cantabrian anchovy on bread with olive oil)", "complement", "classic", "aperitif", "The Basque Country's most celebrated combination — Txakoli and Cantabrian anchovies; the wine's saline mineral and citrus character mirrors the anchovy's salt-cured intensity; natural effervescence cleanses between bites")
    PAIR(prod_txo, "Gilda pintxo (anchovy, guindilla pepper, and Manzanilla olive on a skewer)", "complement", "classic", "aperitif", "The world's first pintxo — invented at Bar Casa Vallés in San Sebastián in the 1940s, and named after Rita Hayworth. Txakoli's salty mineral freshness and the Gilda's olive-anchovy-pepper intensity are inseparable; the wine's effervescence cuts through the brine")

p_ame = P("Ameztoi", "Spain", r_txa,
           description="Ignacio Ameztoi's family estate producing Rubentis — the world's most celebrated rosado Txakoli — alongside the benchmark white from ancient Hondarribi Beltza and Zuri vineyards on the sea-facing slopes of Getaria. Ameztoi's Rubentis sparked a global fascination with Basque rosé and is considered one of the world's great summer wines.")
prod_ame, new = PROD("Ameztoi Rubentis Rosado Txakolina", "wine_still", p_ame, r_txa, "Spain",
                     subcategory="Hondarribi Beltza",
                     description="The world's most sought-after Txakoli rosado — Hondarribi Beltza with some Zuri from the steep Atlantic terraces, lightly pressed for salmon colour and natural effervescence. Wild strawberry, cranberry, citrus peel, sea spray, and an electric freshness that has made Rubentis one of the world's most coveted summer wines. Poured from height; consumed within the year.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ame, "Kokotxas al pil pil (salt cod cheeks in emulsified olive oil and garlic sauce)", "complement", "classic", "main", "The Basque Country's most technically demanding dish and its rosado Txakoli — the wine's electric citrus and saline character cuts through the pil pil emulsion; the rosado's red fruit adds complexity to the cod's gelatinous richness")
    PAIR(prod_ame, "Gambas a la plancha (grilled prawns) with sea salt, lemon, and garlic aioli", "complement", "classic", "aperitif", "The Spanish coast's most elemental dish and the Basque Country's most festive wine — Txakoli's saline effervescence mirrors the prawn's sea sweetness; lemon bridges the citrus freshness; aioli's richness is cut by the wine's electric acidity")

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
