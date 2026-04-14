#!/usr/bin/env python3
"""T23 Batch 21 — New wine regions: Gavi DOCG (Italy), Constantia WO (South Africa), Vacqueyras AOC (France), Vernaccia di San Gimignano DOCG (Italy), Ribera del Guadiana DO (Spain)"""

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

# ── GAVI DOCG (ITALY) ─────────────────────────────────────────────
print("\n=== Gavi DOCG (Italy) ===")
r_gav = R("Gavi", "Italy", "wine",
           designation_type="DOCG",
           designation_name="Gavi DOCG",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Piedmont's premier white wine DOCG in the Alessandria province producing Cortese — a crisp, mineral, and supremely food-friendly white variety. Gavi (also called Cortese di Gavi) ranges from bright, simple aperitif wines to the complex, barrel-aged Gavi di Gavi from the town of Gavi itself on ancient limestone and clay soils. The region's proximity to the Ligurian coast makes Gavi the natural partner for Ligurian seafood and Genoese cuisine.",
           key_producers="La Scolca, Broglia, Castellari Bergaglio, Pio Cesare, Villa Sparina",
           historical_context="Cortese's cultivation in the Monferrato hills dates to at least the 17th century. La Scolca's Giorgio Soldati modernized and championed Gavi in the 1970s, creating a category for crisp, dry northern Italian white wine that rivaled Soave's dominance. Gavi received DOCG status in 1998. The appellation's proximity to Genoa and Turin established it as the natural choice for the region's prosperous restaurateurs.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Gavi vintage; Cortese from limestone and clay soils showed extraordinary mineral precision and citrus freshness."),
    (2021, "very_good", "stable", "Classic vintage; the Alessandrian hills' cooling evening temperatures produced wines of excellent natural acidity and varietal character."),
    (2020, "excellent", "stable", "Benchmark year; La Scolca White Label and Broglia Bruno Broglia produced the finest Gavi expressions of the decade."),
    (2019, "very_good", "rising", "Outstanding vintage; Gavi di Gavi wines from the town of Gavi itself showed exceptional mineral complexity."),
    (2018, "very_good", "stable", "Solid vintage; Cortese's characteristic apple blossom and mineral character was particularly expressive in this cooler year."),
]:
    VIN(r_gav, yr, qd, pt, sn)

p_sco = P("La Scolca", "Italy", r_gav,
           description="Giorgio Soldati's pioneering Gavi estate that championed Cortese as a world-class white wine variety in the 1970s. La Scolca's Black Label Gavi di Gavi is Italy's most recognized and internationally exported Gavi; the White Label is the accessible benchmark. The estate is credited with elevating Gavi from local table wine to international recognition.")
prod_sco, new = PROD("La Scolca Gavi di Gavi White Label", "wine_still", p_sco, r_gav, "Italy",
                     subcategory="Cortese",
                     description="The world's most recognized Gavi di Gavi — Cortese from the town of Gavi on limestone-clay soils. Apple blossom, citrus zest, white peach, mineral freshness, and the crisp, dry character that makes this Italy's quintessential aperitif white. Versatile, elegant, and consistently reliable.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sco, "Trofie al pesto genovese with green beans and potatoes", "complement", "classic", "main", "Ligurian pasta and Piedmontese white — Gavi's mineral freshness and citrus character is the ideal foil for basil pesto's richness; the wine's acidity prevents the pesto from becoming heavy")
    PAIR(prod_sco, "Fritto misto di mare (mixed fried seafood) with lemon and aioli", "complement", "classic", "main", "Cortese's crisp acidity and citrus freshness is the definitive Italian pairing for fried seafood; the wine's mineral precision cuts through the batter; lemon in the garnish mirrors the wine")

p_bro = P("Broglia", "Italy", r_gav,
           description="The Broglia family's Gavi estate on the highest and most mineral sites of the appellation, producing Bruno Broglia — the region's most collected and cellar-worthy single-vineyard Cortese. Broglia's wines demonstrate that Cortese, at its best, is capable of genuine aging and Burgundian depth.")
prod_bro, new = PROD("Broglia Bruno Broglia Gavi di Gavi", "wine_still", p_bro, r_gav, "Italy",
                     subcategory="Cortese",
                     description="Gavi's most complex and age-worthy single-vineyard expression from Broglia's highest limestone sites — more textural and mineral than La Scolca, with greater depth and cellaring potential. White peach, almond, mineral chalk, citrus, and a long finish that develops beautifully over 5-8 years.",
                     price_tier="premium")
if new:
    PAIR(prod_bro, "Trenette avvantaggiate al pesto with Parmigiano and pecorino sardo", "complement", "classic", "main", "The Ligurian pasta tradition's finest expression paired with Piedmont's finest Cortese — the wine's almond and mineral character finds resonance in the pecorino; pesto's basil bridges the herbal notes")
    PAIR(prod_bro, "Grilled branzino fillet with caponata, olive oil, and sea salt", "complement", "classic", "main", "Ligurian sea bass and mineral Gavi — the wine's citrus and almond character mirrors the fish's delicacy; caponata's sweet-sour character bridges the wine's acidity")

# ── CONSTANTIA WO (SOUTH AFRICA) ─────────────────────────────────
print("\n=== Constantia WO (South Africa) ===")
r_con = R("Constantia", "South Africa", "wine",
           designation_type="WO",
           designation_name="Constantia WO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="South Africa's oldest and most historically significant wine ward on the cool, south-facing slopes of the Cape Peninsula's Constantiaberg mountain range, just 15km from Cape Town's center. Constantia produces the world-famous Vin de Constance — the 'Constance wine' beloved by Napoleon Bonaparte, Jane Austen, and Charles Dickens — from Muscat de Frontignan on deep granite and shale soils. The ward also produces outstanding Sauvignon Blanc, Semillon, and the wines of Buitenverwachting, Klein Constantia, and Groot Constantia.",
           key_producers="Klein Constantia, Buitenverwachting, Groot Constantia, Eagles' Nest, Steenberg",
           historical_context="The Constantia estate was established by Governor Simon van der Stel in 1685. The Vin de Constance was the most famous wine in the world during the 18th-19th centuries — Napoleon requested it on St. Helena, Jane Austen recommended it as a remedy for heartbreak in 'Sense and Sensibility', and Baudelaire wrote poetry about it. After a 150-year absence following Phylloxera and changing tastes, Klein Constantia revived Vin de Constance in 1986 — the world's most remarkable wine comeback story.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Constantia vintage; Vin de Constance and Sauvignon Blanc both showed extraordinary cool peninsula mineral freshness."),
    (2021, "very_good", "stable", "Classic vintage; the south-facing Constantiaberg slopes produced wines of excellent precision and the characteristic cool Cape mineral."),
    (2020, "excellent", "stable", "Benchmark year; Klein Constantia Vin de Constance and Buitenverwachting Christine produced internationally acclaimed wines."),
    (2019, "exceptional", "rising", "Greatest Constantia vintage of the modern era; Vin de Constance of extraordinary complexity; Sauvignon Blanc of mineral perfection."),
    (2018, "very_good", "stable", "Solid vintage; the granite-shale soils produced wines of excellent mineral freshness and the ward's characteristic aromatic precision."),
]:
    VIN(r_con, yr, qd, pt, sn)

p_kle = P("Klein Constantia", "South Africa", r_con,
           description="The estate that revived Vin de Constance in 1986 after 150 years of absence. Klein Constantia's Michael Fridjhon and winemakers have produced the world's most historically significant wine revival — the 19th-century sweet Muscat wine beloved by Napoleon and Jane Austen, reborn from original Muscat de Frontignan vines on the original estate. The dry wines (KC, Perdeblokke Sauvignon Blanc) are also Constantia's finest.")
prod_kle, new = PROD("Klein Constantia Vin de Constance", "wine_still", p_kle, r_con, "South Africa",
                     subcategory="Muscat de Frontignan",
                     description="The world's most storied wine revival — Muscat de Frontignan from Constantia granite soils, air-dried for additional concentration, producing South Africa's greatest dessert wine. Orange marmalade, dried apricot, rose water, honey, and the distinctive cool Cape mineral freshness that preserves the sweetness from cloying. Napoleon requested this wine on St. Helena.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_kle, "Cape Malay koeksisters (twisted doughnuts) with syrup, cinnamon, and coconut", "complement", "classic", "dessert", "South Africa's most iconic dessert and its most iconic wine — the wine's orange and rose character bridges the koeksister's spiced syrup; the cool mineral freshness cuts through the sweetness")
    PAIR(prod_kle, "Roquefort with honeycomb, walnuts, and griddled sourdough", "complement", "classic", "cheese", "The world's great pairing of sweet wine and blue cheese — Vin de Constance's rose water and apricot character balances Roquefort's salty intensity; honeycomb bridges the sweetness; walnuts add textural complexity")

p_bui = P("Buitenverwachting", "South Africa", r_con,
           description="Lars Maack's Constantia estate producing some of South Africa's finest Sauvignon Blanc (Christine) and red blends (Buiten Blanc, Hussey's Vlei) from the historic Constantia ward's granite and clay soils. Christine Sauvignon Blanc is consistently South Africa's most internationally acclaimed dry white wine and a benchmark for the cool Cape Peninsula style.")
prod_bui, new = PROD("Buitenverwachting Christine Sauvignon Blanc", "wine_still", p_bui, r_con, "South Africa",
                     subcategory="Sauvignon Blanc",
                     description="South Africa's most critically acclaimed Sauvignon Blanc — old-vine Constantia Sauvignon Blanc with extended lees contact producing a wine of extraordinary mineral complexity and cellar-worthiness. Grapefruit, lime blossom, flinty mineral, and a textural weight and length that develops magnificently over 5-10 years. The cool Peninsula terroir at its finest.",
                     price_tier="premium")
if new:
    PAIR(prod_bui, "West Coast crayfish (kreef) with drawn butter, lemon, and sourdough", "complement", "classic", "main", "Cape Peninsula crayfish and Peninsula Sauvignon Blanc — the wine's mineral freshness and citrus character mirrors the crayfish's sweetness; lemon in the garnish echoes the wine's character")
    PAIR(prod_bui, "Snoek braai (grilled cured fish) with apricot jam glaze and bread", "complement", "established", "main", "Cape Town's traditional grilled fish and Constantia's finest white — snoek's robust, smoky character is complemented by the wine's mineral freshness; apricot jam bridges the wine's fruit notes")

# ── VACQUEYRAS AOC (FRANCE) ───────────────────────────────────────
print("\n=== Vacqueyras AOC (France) ===")
r_vac = R("Vacqueyras", "France", "wine",
           designation_type="AOC",
           designation_name="Vacqueyras AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The Rhône Valley's most underrated and food-friendly appellation in the southern Vaucluse between Gigondas and Beaumes-de-Venise, producing powerful Grenache, Syrah, and Mourvèdre reds alongside small quantities of white and rosé from the garrigue-covered limestone slopes of the Dentelles de Montmirail. Vacqueyras received its own AOC in 1990, graduated from Côtes du Rhône Villages status; the wines represent extraordinary value compared to neighboring Gigondas and Châteauneuf-du-Pape.",
           key_producers="Domaine le Sang des Cailloux, Château des Tours, Domaine de la Monardière, Domaine du Vieux Télégraphe, Tardieu-Laurent",
           historical_context="Vacqueyras's wine history dates to medieval times when Troubadour Raimbaut de Vacqueyras celebrated the wines of this village in his 12th-century poetry. The village's name comes from 'Vallis Quarreria' — valley of quarries — reflecting the limestone terroir that defines the wine's character. Serge Férigoule's Sang des Cailloux estate pioneered the appellation's modern reputation for structured, terroir-driven Grenache.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vacqueyras vintage; Grenache and Mourvèdre from garrigue limestone showed extraordinary dark fruit depth and Mediterranean spice."),
    (2021, "very_good", "stable", "Elegant vintage; the Dentelles de Montmirail's altitude produced wines of excellent freshness; Syrah component particularly fine."),
    (2020, "excellent", "stable", "Benchmark year; Sang des Cailloux and Château des Tours produced Vacqueyras of the highest quality."),
    (2019, "exceptional", "rising", "Greatest Vacqueyras vintage of the modern era; wines of legendary Grenache concentration and garrigue complexity."),
    (2018, "excellent", "stable", "Excellent vintage; Mourvèdre showed its finest expression in years from the limestone Vacqueyras terraces."),
]:
    VIN(r_vac, yr, qd, pt, sn)

p_sca = P("Domaine le Sang des Cailloux", "France", r_vac,
           description="Serge Férigoule's pioneering Vacqueyras estate that launched the appellation's modern reputation for world-class Grenache. 'Blood of the Stones' — named for the reddish iron-rich limestone soils — produces Vacqueyras of extraordinary power, garrigue complexity, and age-worthiness that rivals neighboring Gigondas at a fraction of the price.")
prod_sca, new = PROD("Sang des Cailloux Vacqueyras", "wine_still", p_sca, r_vac, "France",
                     subcategory="Grenache Blend",
                     description="The benchmark Vacqueyras — Grenache, Syrah, Mourvèdre, and Cinsault from iron-rich limestone producing a wine of extraordinary garrigue complexity, dark fruit intensity, and warm Mediterranean character. Wild cherry, dark plum, Provençal herbs, iron, and a long mineral finish from the limestone soils. Excellent value for the quality.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sca, "Daube Provençale (beef braised in wine with olives, capers, and herbs)", "complement", "classic", "main", "The southern Rhône's most classic braised beef dish and its appellation wine — Grenache's garrigue character mirrors the Provençal herbs; olive adds saline depth; the wine appears in the cooking liquid")
    PAIR(prod_sca, "Tian de légumes (Provençal baked layered vegetables) with goat cheese and thyme", "complement", "classic", "main", "Southern Rhône wine and the region's vegetarian tradition — the wine's garrigue and cherry character mirrors the thyme and roasted vegetables; goat cheese adds the acidity to lift both")

p_tor = P("Château des Tours", "France", r_vac,
           description="Emmanuel Reynaud's (of Château Rayas Châteauneuf-du-Pape) secondary estate producing Vacqueyras wines in the distinctive Rayas style — low yields, old-vine Grenache, minimal intervention. Château des Tours Vacqueyras is among the world's most sought-after value wines and a gateway to Reynaud's philosophy at a fraction of Rayas prices.")
prod_tor, new = PROD("Château des Tours Vacqueyras Rouge", "wine_still", p_tor, r_vac, "France",
                     subcategory="Grenache",
                     description="Emmanuel Reynaud's (Château Rayas) Vacqueyras — the Rayas philosophy applied to a more accessible terroir. Pale ruby Grenache of extraordinary elegance and transparency: wild cherry, raspberry, dried herbs, mineral, and a haunting lightness that recalls great Burgundy more than the southern Rhône. One of the world's great value wines.",
                     price_tier="premium")
if new:
    PAIR(prod_tor, "Whole roasted guinea fowl with Provençal herbs, garlic, and roasted cherry tomatoes", "complement", "established", "main", "The Reynaud philosophy's transparency and elegance makes this wine the ideal partner for Guinea fowl's delicate game; cherry tomatoes mirror the wine's bright fruit; herbs bridge the garrigue")
    PAIR(prod_tor, "Pan-fried foie gras with cherry compote and toasted brioche", "complement", "established", "starter", "Pale Grenache's cherry and transparency complements rather than overwhelms foie gras; cherry compote finds direct resonance in the wine's fruit; the wine's acidity cuts through the fat")

# ── VERNACCIA DI SAN GIMIGNANO DOCG (ITALY) ───────────────────────
print("\n=== Vernaccia di San Gimignano DOCG (Italy) ===")
r_ver = R("Vernaccia di San Gimignano", "Italy", "wine",
           designation_type="DOCG",
           designation_name="Vernaccia di San Gimignano DOCG",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Tuscany's only white wine DOCG in the medieval tower town of San Gimignano in the Sienese hills, producing Vernaccia — an indigenous variety of uncertain origin (possibly of Greek descent, despite the name's Latin root) on sandstone, clay, and tufa soils. The best Vernaccia di San Gimignano wines — particularly reserve bottlings and late-harvest versions — demonstrate an unexpected complexity and mineral depth. The ordinary commercial wine is a simple tourist aperitif; the serious producers reveal a distinctive, slightly bitter mineral character that pairs beautifully with Tuscan food.",
           key_producers="Panizzi, Fontaleoni, Mormoraia, Montenidoli, Cusona",
           historical_context="Vernaccia di San Gimignano was Italy's first wine to receive DOC status in 1966 — a recognition of its historical importance. Dante Alighieri mentioned the wines of San Gimignano in the Divine Comedy. Michelangelo was a regular consumer. For much of the 20th century the wine's quality declined as mass production took over the medieval town's tourism. The quality renaissance began in the 1990s with producers like Montenidoli and Panizzi demonstrating that Vernaccia could be taken seriously.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vernaccia vintage; sandstone and tufa soils produced wines of extraordinary mineral precision and the characteristic bitter almond finish."),
    (2021, "very_good", "stable", "Classic vintage; the Sienese hills' limestone and clay produced wines of excellent natural freshness and varietal expression."),
    (2020, "excellent", "stable", "Benchmark year; Panizzi Vigna Santa Margherita and Montenidoli produced internationally acclaimed Vernaccia of genuine depth."),
    (2019, "very_good", "rising", "Outstanding vintage; Vernaccia Riserva wines showed unexpected complexity and aging potential from the best sites."),
    (2018, "very_good", "stable", "Solid vintage; the bitter almond and mineral character of Vernaccia was particularly expressive in the cooler conditions."),
]:
    VIN(r_ver, yr, qd, pt, sn)

p_pan = P("Panizzi", "Italy", r_ver,
           description="Giovanni Panizzi's San Gimignano estate producing the DOCG's most internationally acclaimed and age-worthy Vernaccia. The Vigna Santa Margherita single-vineyard wine from ancient tufa-sand soils consistently receives the highest Italian critical scores for Vernaccia and demonstrates the variety's genuine potential for complexity and longevity.")
prod_pan, new = PROD("Panizzi Vigna Santa Margherita Vernaccia", "wine_still", p_pan, r_ver, "Italy",
                     subcategory="Vernaccia",
                     description="The definitive Vernaccia di San Gimignano — from ancient tufa-sandstone Vigna Santa Margherita producing a wine of unusual mineral depth and age-worthiness. Citrus, white peach, bitter almond, mineral tufa, and a distinctive slightly bitter finish that is the variety's signature and makes it one of Tuscany's most food-friendly whites.",
                     price_tier="premium")
if new:
    PAIR(prod_pan, "Ribollita (Tuscan bread and vegetable stew) with Parmigiano and olive oil", "complement", "classic", "main", "Vernaccia's mineral freshness and bitter almond character bridges the rustic Tuscan stew; the wine's slightly bitter finish mirrors the vegetables' earthiness; Parmigiano adds depth")
    PAIR(prod_pan, "Crostini toscani (chicken liver pâté on toasted bread) with capers and anchovies", "complement", "classic", "aperitif", "Tuscan starter tradition and Tuscan white — Vernaccia's bitter almond and mineral character is the perfect foil for chicken liver's richness; caper's brine finds resonance in the wine's mineral quality")

p_mon = P("Montenidoli", "Italy", r_ver,
           description="Elisabetta Fagiuoli's organic and biodynamic San Gimignano estate is the DOCG's most philosophically distinctive and internationally admired producer. Her Vernaccia Tradizionale (skin contact) and regular Fiore are considered the most authentic expressions of Vernaccia's ancient character — wild, mineral, and utterly unlike the commercial versions.")
prod_mon_v, new = PROD("Montenidoli Tradizionale Vernaccia", "wine_still", p_mon, r_ver, "Italy",
                        subcategory="Vernaccia",
                        description="Elisabetta Fagiuoli's skin-contact Vernaccia — one of Italy's most distinctive and philosophically important white wines. Extended maceration produces a golden, textural wine with dried citrus, bitter almond, mineral tufa, beeswax, and a wildness that recalls the ancient Etruscan winemaking tradition. Polarizing and profound.",
                        price_tier="premium")
if new:
    PAIR(prod_mon_v, "Tripe alla Fiorentina with tomato, garlic, and Parmigiano Reggiano", "complement", "established", "main", "Vernaccia's bitter almond and mineral character is one of the few whites that can handle offal's intensity; the wine's slight bitterness mirrors the tripe's richness; tomato bridges the acidity")
    PAIR(prod_mon_v, "Panzanella with ripe summer tomatoes, cucumber, torn bread, and basil", "complement", "classic", "starter", "Tuscan bread salad and Tuscan white wine — Vernaccia's mineral freshness and bitter almond character lifts the panzanella's summer richness; basil bridges the herbal notes")

# ── RIBERA DEL GUADIANA DO (SPAIN) ────────────────────────────────
print("\n=== Ribera del Guadiana DO (Spain) ===")
r_rgu = R("Ribera del Guadiana", "Spain", "wine",
           designation_type="DO",
           designation_name="Ribera del Guadiana DO",
           reputation_tier="overlooked",
           quality_trajectory="ascending",
           description="Extremadura's largely unexplored wine DO along the Guadiana River in southwestern Spain, one of Europe's hottest wine regions producing powerful reds from Tempranillo (locally called Roble), Garnacha, Graciano, and Cabernet Sauvignon on granite, slate, and alluvial soils. The extreme continental climate — summers reaching 45°C — and the vineyards' high altitude (300-700m) create wines of remarkable dark fruit intensity and untamed character. The region remains one of Spain's most undiscovered wine territories with prices far below quality.",
           key_producers="Bodegas Habla, Bodegas Viñas de Alange, Inurrieta, Pago Los Baldíos, Enrique Calvo",
           historical_context="Extremadura was Rome's most westerly Hispania province — the word itself derives from 'Extrema Durii' (the furthest reaches of the Duero). The region produced wine for the Spanish conquistadors who left for the Americas from these lands; Hernán Cortés and Francisco Pizarro were both Extremadurans. The modern DO was established in 1999. German wine critic Stefan Reinhardt's discovery of Bodegas Habla in 2010 brought international attention to the region's potential for concentrated, powerful reds.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Ribera del Guadiana vintage; Tempranillo and Cabernet from granite soils showed extraordinary dark fruit concentration."),
    (2021, "very_good", "stable", "Classic vintage; the Guadiana plateau's altitude moderated the heat, producing wines of excellent freshness and structure."),
    (2020, "excellent", "stable", "Benchmark year; Habla and Viñas de Alange produced Extremaduran wines of exceptional international quality."),
    (2019, "very_good", "rising", "Outstanding vintage; the region's potential for powerful, value-driven reds began attracting serious international attention."),
    (2018, "very_good", "stable", "Solid vintage; granite and slate soils produced wines of good mineral depth; the region's value proposition was strongly confirmed."),
]:
    VIN(r_rgu, yr, qd, pt, sn)

p_hab = P("Bodegas Habla", "Spain", r_rgu,
           description="German-owned Extremaduran estate that brought the region to international attention when critic Stefan Reinhardt gave multiple 100-point scores to their Habla de Ti and Habla No. 7. The estate's international investment has introduced the highest-quality winemaking to Spain's most overlooked wine territory.")
prod_hab, new = PROD("Habla de Ti Tempranillo", "wine_still", p_hab, r_rgu, "Spain",
                     subcategory="Tempranillo",
                     description="Ribera del Guadiana's most internationally acclaimed wine — old-vine Tempranillo from Extremadura's granite soils producing extraordinary dark fruit concentration and structured power. Dark plum, blackberry, tobacco, espresso, and the mineral depth of ancient granite. Received 100 points from major international critics; represents Spain's most exciting value in premium wine.",
                     price_tier="premium")
if new:
    PAIR(prod_hab, "Cochineta pibil (Extremaduran slow-roasted pork with achiote and sour orange)", "complement", "classic", "main", "Extremadura's rich pork tradition and its most powerful wine — the wine's dark fruit and tobacco handles the slow-roasted pork's richness; achiote's earthiness bridges the wine's mineral depth")
    PAIR(prod_hab, "Caza guisada (Extremaduran mixed game stew with chestnuts and mushrooms)", "complement", "classic", "main", "The Extremaduran hunting tradition meets its most powerful regional wine — game's intensity matches the wine's concentration; chestnuts echo the wine's earthy depth; mushrooms bridge the mineral character")

p_via = P("Bodegas Viñas de Alange", "Spain", r_rgu,
           description="Alange co-operative's premium arm producing Palacio Quemado wines from old-vine Tempranillo and Graciano on the granite soils of the Tierra de Barros sub-zone. Palacio Quemado's value-quality ratio is one of Spain's most impressive, consistently producing wines that compete with Rioja Reserva at a fraction of the price.")
prod_via, new = PROD("Palacio Quemado Gran Reserva Tempranillo", "wine_still", p_via, r_rgu, "Spain",
                     subcategory="Tempranillo",
                     description="Ribera del Guadiana's finest Gran Reserva — Tempranillo and Graciano from Alange's ancient granite vines with extended aging in American and French oak. Cedar, dark cherry, leather, tobacco, and the warm Extremaduran fruit concentration balanced by the granite soils' natural mineral freshness. Spain's most underrated Gran Reserva.",
                     price_tier="mid_range")
if new:
    PAIR(prod_via, "Migas extremeñas (fried breadcrumbs with chorizo, pimentón, and egg)", "complement", "classic", "main", "Extremadura's most traditional dish and its finest Gran Reserva — the wine's cedar and dark fruit handles the chorizo's fat richness; pimentón bridges the wine's earthy character")
    PAIR(prod_via, "Perdiz en escabeche (marinated partridge) with pickled vegetables and bay", "complement", "classic", "main", "Game bird in the Extremaduran hunting tradition paired with its regional wine — the wine's leather and tobacco complexity handles the partridge's rich gaminess; vinegar escabeche's acidity bridges")

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
