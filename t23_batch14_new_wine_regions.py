#!/usr/bin/env python3
"""T23 Batch 14 — New wine regions: McLaren Vale GI (Australia), Yarra Valley GI (Australia), Priorat DOQ (Spain), Alentejo DOC (Portugal), Jura AOC (France)"""

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

# ── MCLAREN VALE GI (AUSTRALIA) ───────────────────────────────────
print("\n=== McLaren Vale GI (Australia) ===")
r_mcl = R("McLaren Vale", "Australia", "wine",
           designation_type="GI",
           designation_name="McLaren Vale GI",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="South Australia's most celebrated warm-climate wine region on the Fleurieu Peninsula south of Adelaide, producing the country's most acclaimed Shiraz alongside outstanding Grenache, Mataro (Mourvèdre), and Cabernet Sauvignon. The region's exceptional diversity of soils — 40 distinct types including ironstone, red clay, and ancient schist — combined with sea breezes from Gulf St. Vincent create wines of remarkable complexity and regional character.",
           key_producers="d'Arenberg, Wirra Wirra, Clarendon Hills, Yangarra Estate, Coriole",
           historical_context="McLaren Vale was first planted by John Reynell in 1838. For much of the 20th century the region supplied bulk wine to the Barossa. The quality revolution began in the 1980s when Chester Osborn at d'Arenberg and producers at Wirra Wirra demonstrated that McLaren Vale's ancient soils could produce Shiraz and Grenache of world-class distinction. The region's GSM (Grenache-Shiraz-Mourvèdre) blends have become an Australian calling card.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding McLaren Vale vintage; Shiraz and Grenache from ironstone soils showed extraordinary fruit depth with rare elegance."),
    (2021, "very_good", "stable", "Classic vintage; the Gulf St. Vincent sea breezes produced wines of uncommon freshness for the warm region."),
    (2020, "excellent", "stable", "Benchmark year; d'Arenberg Dead Arm and Yangarra GSM produced the finest wines of the decade."),
    (2019, "excellent", "rising", "Outstanding vintage; old-vine Grenache from the ancient Blewitt Springs sub-region reached extraordinary quality."),
    (2018, "very_good", "stable", "Solid vintage; Shiraz of power and concentration; Cabernet of firm structure and dark fruit intensity."),
]:
    VIN(r_mcl, yr, qd, pt, sn)

p_dar = P("d'Arenberg", "Australia", r_mcl,
           description="Chester Osborn's iconoclastic McLaren Vale estate producing an enormous range of eccentric, site-specific wines from ancient dryland vineyards. The Dead Arm Shiraz and The Coppermine Road Cabernet are d'Arenberg's benchmarks; the Cube winery building is McLaren Vale's most distinctive architectural landmark.")
prod_dar, new = PROD("d'Arenberg The Dead Arm Shiraz", "wine_still", p_dar, r_mcl, "Australia",
                     subcategory="Shiraz",
                     description="Australia's most celebrated single-vineyard McLaren Vale Shiraz from a declining section of old vineyard (the 'dead arm'). Dark chocolate, blackberry, liquorice, white pepper, and the ironstone mineral character that defines this ancient region. Dense, age-worthy, and unmistakably Australian.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_dar, "Slow-roasted lamb shoulder with harissa, preserved lemon, and couscous", "complement", "classic", "main", "Australian Shiraz and slow lamb is the country's most celebrated pairing; the wine's dark spice and chocolate character handles harissa's heat; preserved lemon bridges the acidity")
    PAIR(prod_dar, "Smoked brisket with house-made BBQ sauce and pickled jalapeños", "complement", "established", "main", "The wine's dark fruit and chocolate intensity matches the smoke and caramelization of the brisket; the acid in the BBQ sauce mirrors the wine's structure")

p_yan = P("Yangarra Estate", "Australia", r_mcl,
           description="Jackson Family Wines' biodynamically farmed McLaren Vale estate producing old-vine Grenache and GSM blends from the ancient Blewitt Springs sub-region. Yangarra's High Sands Grenache — from 70-year-old bush vines on white silica sand — is considered Australia's finest Grenache.")
prod_yan, new = PROD("Yangarra High Sands Grenache", "wine_still", p_yan, r_mcl, "Australia",
                     subcategory="Grenache",
                     description="Australia's most celebrated old-vine Grenache from 70-year-old bush vines on unique white silica sand soils. Wild strawberry, raspberry, dried herbs, orange zest, and a silky texture quite unlike Shiraz-dominated McLaren Vale styles. Haunting, transparent, and profoundly individual.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_yan, "Roasted spatchcock chicken with herb butter and wild garlic jus", "complement", "established", "main", "Old-vine Grenache's silky transparency and herb character is the ideal partner for roasted poultry; the wine's wild herb notes mirror the herb butter")
    PAIR(prod_yan, "Duck confit with cherry gastrique and Puy lentils", "complement", "classic", "main", "Grenache's wild cherry and dried herb character is the Rhône's traditional partner for duck; the gastrique's cherry mirrors the wine's fruit; Australian old-vine depth adds complexity")

# ── YARRA VALLEY GI (AUSTRALIA) ───────────────────────────────────
print("\n=== Yarra Valley GI (Australia) ===")
r_yar = R("Yarra Valley", "Australia", "wine",
           designation_type="GI",
           designation_name="Yarra Valley GI",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Victoria's premier cool-climate wine region in the foothills of the Great Dividing Range east of Melbourne, producing Pinot Noir, Chardonnay, and sparkling wines of international distinction. The Upper Yarra's elevation and ancient volcanic soils contrast with the Lower Yarra's warmer alluvial conditions, creating a remarkable diversity of styles within a single appellation.",
           key_producers="Yering Station, Oakridge, Coldstream Hills, Giant Steps, De Bortoli",
           historical_context="The Yarra Valley was Victoria's most important wine region in the 1880s before Phylloxera devastated the vineyards in 1890. The modern era began with Dr. Bailey Carrodus's Yering Station in 1969, who recognized the valley's Burgundian potential. James Halliday's Coldstream Hills (1985) further established the region's Pinot Noir credentials internationally.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Yarra Valley vintage; Upper Yarra Pinot Noir of haunting mineral transparency and Chardonnay of Burgundian elegance."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; the cooler growing season produced wines of exceptional aromatic freshness."),
    (2020, "excellent", "stable", "Benchmark year; Oakridge and Giant Steps produced internationally acclaimed Pinot Noir."),
    (2019, "excellent", "rising", "Outstanding vintage; Upper Yarra Pinot reached its highest critical scores; Lower Yarra Cabernet excelled."),
    (2018, "very_good", "stable", "Solid vintage; Chardonnay of excellent Burgundian character from the elevated Upper Yarra sub-region."),
]:
    VIN(r_yar, yr, qd, pt, sn)

p_oak = P("Oakridge Wines", "Australia", r_yar,
           description="David Bicknell's Yarra Valley estate producing some of Australia's most critically acclaimed Pinot Noir and Chardonnay. The 864 series site-specific wines — particularly 864 Funder & Diamond Chardonnay — are considered benchmarks for Australian cool-climate white wine. Oakridge is at the forefront of the Yarra's quality revolution.")
prod_oak, new = PROD("Oakridge 864 Funder and Diamond Chardonnay", "wine_still", p_oak, r_yar, "Australia",
                     subcategory="Chardonnay",
                     description="Australia's most refined Yarra Valley Chardonnay from the elevated Funder and Diamond single vineyard. White peach, hazelnuts, struck flint, white flower, and the Burgundian mineral precision that distinguishes Upper Yarra Chardonnay from warmer Australian styles. Age-worthy and profound.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_oak, "Pan-roasted blue-eye trevalla with brown butter, lemon, and capers", "complement", "classic", "main", "Australian premium fish and Australia's finest Chardonnay — the wine's hazelnuts and mineral precision complement the fish's delicate flavour; brown butter mirrors the wine's texture")
    PAIR(prod_oak, "Roasted cep mushroom risotto with aged Parmigiano and black truffle", "complement", "established", "main", "Chardonnay's hazelnut and mineral character finds natural resonance with cep mushrooms; truffle adds an earthy dimension the wine can meet")

p_gia = P("Giant Steps", "Australia", r_yar,
           description="Phil Sexton's premium Yarra Valley estate producing site-specific Pinot Noir and Chardonnay wines from Upper Yarra's cool hillsides. Giant Steps' Tarraford Vineyard and Sexton Vineyard wines are among the Yarra's finest single-site expressions; the bakery-café complex in Healesville is a destination.")
prod_gia, new = PROD("Giant Steps Sexton Vineyard Pinot Noir", "wine_still", p_gia, r_yar, "Australia",
                     subcategory="Pinot Noir",
                     description="Upper Yarra Pinot Noir from the Sexton family's elevated volcanic basalt vineyard — translucent ruby, wild cherry, forest floor, dried rose, and the distinctive Upper Yarra mineral character. Burgundian in elegance and transparency; genuinely site-specific in character.",
                     price_tier="premium")
if new:
    PAIR(prod_gia, "Grilled quail with cherry vinegar glaze, lentils, and crispy prosciutto", "complement", "classic", "main", "Yarra Valley Pinot's cherry transparency is the ideal match for quail's delicate game flavour; the cherry glaze mirrors the wine; prosciutto adds textural contrast")
    PAIR(prod_gia, "Mushroom and thyme galette with Gruyère and caramelized onion", "complement", "established", "main", "The wine's forest floor and earthy character finds resonance with the mushroom filling; Gruyère's nuttiness bridges the Pinot's complexity")

# ── PRIORAT DOQ (SPAIN) ───────────────────────────────────────────
print("\n=== Priorat DOQ (Spain) ===")
r_pri = R("Priorat", "Spain", "wine",
           designation_type="DOQ",
           designation_name="Priorat DOQ",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Catalonia's most prestigious wine appellation on ancient llicorella (slate and quartz) soils in the mountains southwest of Tarragona. Old-vine Garnacha and Cariñena produce wines of extraordinary concentration, dark fruit intensity, and mineral depth. Priorat's dramatic rocky terraces — where donkeys are still used because tractors cannot navigate — produce Spain's most expensive and internationally acclaimed wines alongside Ribera del Duero.",
           key_producers="Álvaro Palacios, Clos Mogador, Cims de Porrera, Mas Doix, Terroir al Límit",
           historical_context="Medieval Carthusian monks established winemaking at the Scala Dei Priory in the 12th century — hence 'Priory' = Priorat. After Phylloxera destroyed the vineyards in the late 19th century, the region lay dormant for decades. René Barbier recruited Álvaro Palacios, Dafne Glorian, and other visionaries in 1989 to create the 'Clos movement' that transformed Priorat into one of the world's most sought-after wine regions.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Priorat vintage; old-vine Garnacha from llicorella expressed extraordinary mineral depth and dark fruit intensity."),
    (2021, "very_good", "stable", "Elegant vintage; lower yields from the slate soils produced wines of greater finesse than the region's typical power."),
    (2020, "excellent", "stable", "Benchmark year; L'Ermita and Clos Mogador produced internationally acclaimed wines of extraordinary concentration."),
    (2019, "exceptional", "rising", "Greatest Priorat vintage of the modern era; wines of legendary structure and llicorella mineral intensity."),
    (2018, "excellent", "stable", "Excellent vintage; old-vine Cariñena showed its finest expression from the terraced slate vineyards."),
]:
    VIN(r_pri, yr, qd, pt, sn)

p_alv = P("Álvaro Palacios", "Spain", r_pri,
           description="The visionary Rioja-born winemaker whose L'Ermita became Spain's most expensive and sought-after wine and whose Finca Dofí helped launch Priorat's international reputation in the early 1990s. Álvaro Palacios is considered the architect of modern Priorat and one of Spain's most important wine figures.")
prod_alv, new = PROD("Álvaro Palacios Les Terrasses", "wine_still", p_alv, r_pri, "Spain",
                     subcategory="Garnacha Blend",
                     description="Álvaro Palacios's accessible entry to Priorat — old-vine Garnacha and Cariñena from llicorella slate and quartz soils. Dark cherry, blackberry, mineral slate, dried herbs, and the unmistakable Priorat density without L'Ermita's extreme concentration. One of the best-value wines from a legendary producer.",
                     price_tier="premium")
if new:
    PAIR(prod_alv, "Cochinillo asado (roast suckling pig) with Catalan romesco sauce", "complement", "classic", "main", "Iberian roasted pork and Priorat's mineral Garnacha is a natural Catalonian pairing; the wine's dark fruit and mineral depth handles the pig's rich, crispy skin")
    PAIR(prod_alv, "Grilled lamb chops with allioli, escalivada, and flatbread", "complement", "classic", "main", "Garnacha and grilled lamb is the Catalan countryside's defining pairing; the wine's dark herb and slate character mirrors the charred meat and roasted vegetables")

p_mos = P("Clos Mogador", "Spain", r_pri,
           description="René Barbier's legendary single-vineyard estate that co-founded the modern Priorat movement in 1989. Clos Mogador is produced from a single dramatic terraced slate vineyard and is considered co-equal with L'Ermita as Priorat's greatest wine — more rustic, wilder, and more intensely mineral.")
prod_mos, new = PROD("Clos Mogador Priorat", "wine_still", p_mos, r_pri, "Spain",
                     subcategory="Garnacha Blend",
                     description="René Barbier's founding vision of Priorat — a single-vineyard Garnacha, Cabernet Sauvignon, and Syrah from the original Clos planted in 1989 on ancient llicorella. Black olive, iron, slate, dark cherry, and wild herbs with massive but refined tannins. Legendary and consistently great.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mos, "Slow-braised ox cheek with prunes, chocolate, and Priorat wine reduction", "complement", "classic", "main", "Priorat's dark mineral power demands the richest possible braised meat; prune's sweetness mirrors the wine's dark fruit; chocolate bridges the slate intensity")
    PAIR(prod_mos, "Truffle-stuffed roasted guinea fowl with black truffle jus and root vegetables", "complement", "established", "main", "The wine's iron and slate minerality provides the perfect foil for truffle's earthiness; guinea fowl's gaminess is matched by Priorat's wild herb character")

# ── ALENTEJO DOC (PORTUGAL) ───────────────────────────────────────
print("\n=== Alentejo DOC (Portugal) ===")
r_ale = R("Alentejo", "Portugal", "wine",
           designation_type="DOC",
           designation_name="Alentejo DOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Portugal's sun-drenched plains southeast of Lisbon, producing powerful, food-friendly reds from Alicante Bouschet, Trincadeira, Aragonez (Tempranillo), and Touriga Nacional. The region's cork oak forests supply 50% of the world's natural cork. Eight sub-regions — including Borba, Reguengos, and Évora — each express different aspects of the region's warm continental climate and schist, granite, and marble soils.",
           key_producers="Esporão, Herdade do Mouchão, José de Sousa, Quinta do Crasto, Herdade dos Grous",
           historical_context="Alentejo's wine history stretches to the Roman era; Évora contains extensive Roman ruins including a temple to Diana. The region's large estates (herdades) were nationalized during the 1974 Carnation Revolution and many deteriorated; private ownership returned in 1985 and quality rebounded dramatically. Esporão's wines, pioneered by Australian David Baverstock, demonstrated Alentejo's international potential in the 1990s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Alentejo vintage; Alicante Bouschet and Trincadeira from schist soils showed extraordinary depth and freshness despite the heat."),
    (2021, "very_good", "stable", "Classic warm-climate vintage; the region's ancient variety blend produced wines of excellent complexity and food-friendly structure."),
    (2020, "excellent", "stable", "Benchmark year; Esporão Reserva and Mouchão Torre de Palma produced internationally acclaimed single-varietal wines."),
    (2019, "excellent", "rising", "Outstanding vintage; Alicante Bouschet achieved extraordinary depth; Esporão Private Selection gained international cult status."),
    (2018, "very_good", "stable", "Solid vintage; Aragonez and Touriga Nacional showed excellent varietal character from the cooler sub-regions of Évora and Grândola."),
]:
    VIN(r_ale, yr, qd, pt, sn)

p_esp = P("Herdade do Esporão", "Portugal", r_ale,
           description="The Alentejo's most internationally known and commercially important estate, spanning 700 hectares of schist and marble near Reguengos de Monsaraz. Esporão's Private Selection and Reserva wines, crafted by Australian David Baverstock since 1992, pioneered Alentejo's global reputation. The estate's olive oil and cork operations also produce world-class products.")
prod_esp, new = PROD("Esporão Reserva Tinto", "wine_still", p_esp, r_ale, "Portugal",
                     subcategory="Alicante Bouschet Blend",
                     description="Alentejo's benchmark red wine blend — Aragonez, Trincadeira, Cabernet Sauvignon, and Alicante Bouschet from schist and marble soils. Dark plum, black cherry, tobacco, dried herbs, and a warm, generous structure that makes this one of Portugal's most food-friendly reds. Excellent value.",
                     price_tier="mid_range")
if new:
    PAIR(prod_esp, "Ensopado de borrego (slow-braised lamb) with coriander and crusty bread", "complement", "classic", "main", "Alentejo lamb stew and Alentejo red is the region's defining pairing; the wine's dark fruit and herb character mirrors the stew's spiced richness")
    PAIR(prod_esp, "Migas com entrecosto (pork ribs with bread porridge) and coriander", "complement", "classic", "main", "Traditional Alentejo cuisine demands its traditional wine; the wine's warm fruit and tobacco notes handle the pork's fat richness; coriander bridges the herb character")

p_mou = P("Herdade do Mouchão", "Portugal", r_ale,
           description="The Reynolds family's historic Alentejo estate, producing Portugal's most celebrated single-variety Alicante Bouschet from very old vines. Mouchão and Torre de Palma Alicante Bouschet have established this unusual Bordelais variety — planted in Alentejo for over a century — as one of Portugal's most distinctive and individualistic red wines.")
prod_mou, new = PROD("Herdade do Mouchão Alicante Bouschet", "wine_still", p_mou, r_ale, "Portugal",
                     subcategory="Alicante Bouschet",
                     description="Portugal's most distinctive single-variety red wine from ancient Alicante Bouschet vines — rare teinturier variety with naturally red flesh producing wines of extraordinary, almost opaque color. Blackberry jam, dried figs, leather, and an unusual sweetness of fruit balanced by robust tannins. A true Portuguese original.",
                     price_tier="premium")
if new:
    PAIR(prod_mou, "Chanfana (goat braised in red wine with garlic and bay)", "complement", "classic", "main", "Ancient Portuguese goat dish and ancient Alentejo wine — the wine's dark fruit and tannins handle the intense braising; garlic and bay mirror the wine's herbal warmth")
    PAIR(prod_mou, "Queijo de Évora (hard sheep's cheese) with quince membrillo and almonds", "complement", "classic", "cheese", "The wine's intense fruit and leather character matches the hard sheep's cheese; quince provides acidity to bridge the wine's sweetness; almonds echo the wine's earthy depth")

# ── JURA AOC (FRANCE) ─────────────────────────────────────────────
print("\n=== Jura AOC (France) ===")
r_jur = R("Jura", "France", "wine",
           designation_type="AOC",
           designation_name="Jura AOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="France's smallest and most idiosyncratic wine region in the western foothills of the Alps, producing entirely unique wines that exist nowhere else in the world. Vin Jaune — oxidatively aged Savagnin in small barrels under a flor-like voile for minimum six years — is one of France's greatest and most original wines. Poulsard, Trousseau, and Pinot Noir produce light, haunting reds of startling transparency. The Jura is the heartland of France's natural wine movement.",
           key_producers="Domaine Ganevat, Jacques Puffeney, Overnoy-Houillon, Stéphane Tissot, Henri Maire",
           historical_context="The Jura is Louis Pasteur's homeland — the father of pasteurization and germ theory was born in Dole and conducted his first experiments on Jura wine. Vin Jaune's unique character comes from the voile of yeast that develops on the wine's surface like Sherry's flor. Jean Bourdy's 1774 Vin Jaune is considered the world's oldest commercially available wine. Pierre Overnoy's natural wine philosophy, inherited by Emmanuel Houillon, made the Jura a pilgrimage destination.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Jura vintage; Vin Jaune of extraordinary walnut and curry complexity; Poulsard of haunting mineral transparency."),
    (2021, "very_good", "stable", "Elegant vintage; cool conditions produced natural Poulsard and Trousseau wines of remarkable purity and vitality."),
    (2020, "excellent", "stable", "Benchmark year; Ganevat and Tissot produced Chardonnay and Vin Jaune of the highest order."),
    (2019, "excellent", "rising", "Outstanding vintage; Vin Jaune from the Château-Chalon appellation reached extraordinary complexity."),
    (2018, "very_good", "stable", "Solid vintage; natural Poulsard wines from this year gained major international natural wine community attention."),
]:
    VIN(r_jur, yr, qd, pt, sn)

p_tis = P("Stéphane Tissot", "France", r_jur,
           description="The Jura's most technically proficient and commercially visible producer, farming biodynamically and producing an enormous range from Vin Jaune to natural Poulsard and single-vineyard Chardonnay. André & Mireille Tissot's wines are the Jura's most accessible entry point for newcomers, while the single-vineyard series represents the appellation's finest terroir expression.")
prod_tis, new = PROD("Tissot Vin Jaune Arbois", "wine_still", p_tis, r_jur, "France",
                     subcategory="Savagnin",
                     description="The Jura's most celebrated wine style — Savagnin aged under voile in old barrels for six years and three months in Arbois. Profound oxidative complexity: walnut, curry, dried porcini, yellow fruit, saffron, and a lingering, haunting finish. Vin Jaune is unique in the world and immortal in a properly stored clavelin.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_tis, "Poulet au Vin Jaune with morels and Comté cream sauce", "complement", "classic", "main", "The Jura's supreme pairing — the wine appears in the sauce creating a circular dialogue of walnut, cream, and mushroom; the wine's oxidative character makes the dish and vice versa")
    PAIR(prod_tis, "Comté 36-month (Jura mountain cheese) with toasted walnuts and honey", "complement", "classic", "cheese", "The Jura's greatest wine and greatest cheese — Comté's walnut and crystalline complexity mirrors Vin Jaune perfectly; honey bridges the wine's residual sweetness")

p_gan = P("Domaine Ganevat", "France", r_jur,
           description="Jean-François Ganevat's iconic Rotalier estate is the Jura's most sought-after and critically acclaimed producer, farming biodynamically from ancient vines on the marl and limestone Lias soils. Ganevat's single-parcel Poulsard, Trousseau, and Chardonnay wines are allocated among the world's finest wine collectors.")
prod_gan, new = PROD("Ganevat Poulsard Chalasses Vieilles Vignes", "wine_still", p_gan, r_jur, "France",
                     subcategory="Poulsard",
                     description="Jean-François Ganevat's benchmark Poulsard from ancient vines on Lias limestone — translucent salmon-pink, impossibly delicate, with wild strawberry, dried rose petal, mineral freshness, and an almost Burgundian haunting quality. Poulsard is unique to the Jura; Ganevat's version is its finest expression.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_gan, "Charcuterie Jurassienne — saucisse de Morteau, coppa, and terrine de campagne", "complement", "classic", "aperitif", "The Jura's most authentic pairing — local charcuterie and local Poulsard, both from the same mountain culture; the wine's delicate fruit and mineral freshness cuts through the cured meats")
    PAIR(prod_gan, "Morel mushroom omelette with crème fraîche and chives", "complement", "established", "main", "The Jura's signature spring dish and its most delicate red — Poulsard's transparency and mineral freshness lifts the morels' earthiness without dominating; crème fraîche bridges")

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
