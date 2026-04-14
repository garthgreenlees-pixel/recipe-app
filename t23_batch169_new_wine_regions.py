#!/usr/bin/env python3
"""B169 — Global spread: Istria DOC, Goriška Brda, Walker Bay WO, Salta Wine Region, Russian River Valley AVA"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
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

# === ISTRIAN WINE REGION ===
print("=== Istrian Wine Region ===")
r1 = R("Istrian Wine Region", "Croatia", "wine",
       designation_type="region",
       designation_name="Istria Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Istria, the triangular peninsula shared between Croatia, Slovenia, and Italy on the northern Adriatic, produces some of central Europe's most distinctive wines. Malvazija Istarska (Malvasia Istriana) is the dominant white variety — rich, aromatic, and uniquely Istrian. The red Teran (Refosco) from the red terra rossa soils ('crvena zemlja') produces high-acid, iron-rich reds of great character. Motovun and Poreč are the key towns. The Italian influence on cuisine and viticulture is pronounced — Istrian white truffles are among the world's finest, making local wines the ideal accompaniment.",
       key_producers="Roxanich, Kabola, Benvenuti Winery, Coronica, Clai Sveti Jakov",
       historical_context="Istrian wine history dates back 2,500 years to Greek and Roman colonisation of the Adriatic coast. The region was part of Italy until 1947 (when it became Yugoslav territory), and the Italian wine influence remains strong, particularly in variety names and winemaking traditions.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Landmark Istrian vintage — Malvazija wines of exceptional aromatic depth and structure."),
    (2020,"very_good","stable","Good vintage; Teran and Malvazija both showing classic varietal character."),
    (2021,"excellent","rising","Outstanding conditions; white wines of unusual freshness alongside structured Teran reds."),
    (2022,"very_good","stable","Warm year; rich, aromatic Malvazija alongside opulent Teran with soft tannins."),
    (2023,"excellent","rising","Exceptional vintage for Istrian whites — Malvazija of extraordinary complexity."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Roxanich Winery Istria", "winery", r1, "Croatia",
       production_philosophy="minimal_intervention",
       philosophy_description="Mladen Rožanić is Croatia's most internationally recognised artisan winemaker, producing extended skin-contact 'orange' Malvazija wines alongside traditional fresh styles. His Milva and Ines u Bijelom wines have introduced Croatian wine to international fine wine circles.",
       reputation_narrative="Roxanich is Croatia's most acclaimed artisan producer — the amber/orange Malvazija wines have been featured in Natural Wine guides worldwide, while the traditional Malvazija shows the variety's freshness-and-richness balance that makes it Istria's greatest wine.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Roxanich Ines u Bijelom Malvazija Istarska", "wine_still", p1, r1, "Croatia",
                    subcategory="orange_amber", description="Extended skin-contact Malvazija Istarska from Istrian clay soils — amber-golden colour with tannic grip. Stone fruit, dried apricot, chamomile, white pepper, and a long mineral finish. Croatia's most celebrated orange wine.", price_tier="premium")
if is_new:
    PAIR(prod, "Istrian white truffle shaved on fresh pasta with butter", "complement", "classic", "main", "One of Croatia's greatest terroir pairings — Istrian white truffle with Istrian amber Malvazija shares the region's earthy, aromatic complexity.")
    PAIR(prod, "Grilled scampi from the Kvarner Gulf with olive oil", "complement", "classic", "starter", "Kvarner seafood with Istrian wine — the amber wine's tannic texture handles scampi richness; olive oil bridges the minerality.")
    PAIR(prod, "Pršut (Istrian prosciutto) with young pecorino and figs", "complement", "classic", "starter", "A perfect Istrian antipasto — the wine's tannic grip and dried fruit notes bridge to the cured meat and cheese.")
    PAIR(prod, "Chicken with walnut sauce and fresh herbs", "complement", "established", "main", "Stone fruit and tannic grip in the amber wine match walnut sauce's richness; herbs bridge both.")
prod, is_new = PROD("Kabola Malvazija Istarska Manzan", "wine_still", p1, r1, "Croatia",
                    subcategory="white", description="Fresh-style Malvazija Istarska from Kabola's organic Motovun vineyard — fragrant, rich white wine with peach, acacia blossom, almond, and a mineral finish from the red terra rossa soil. Croatia's most food-friendly white.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled Adriatic sea bass with lemon and olive oil", "complement", "classic", "main", "The quintessential Istrian coastal pairing — Malvazija's richness matches sea bass's delicate flavour beautifully.")
    PAIR(prod, "Pasta with Istrian truffles and Parmesan", "complement", "classic", "main", "Acacia and stone fruit in Malvazija bridge to truffle's earthiness — a regional match of complete harmony.")
    PAIR(prod, "Octopus salad with capers, red onion and parsley", "complement", "established", "starter", "The wine's almond and mineral notes complement octopus's brininess; capers echo the wine's bright character.")
    PAIR(prod, "Grilled whole branzino with salt and herbs", "complement", "classic", "main", "Peach and acacia Malvazija mirrors branzino's Mediterranean character; the wine's light body suits delicate fish.")

# === GORIŠKA BRDA ===
print("=== Goriška Brda ===")
r2 = R("Goriška Brda", "Slovenia", "wine",
       designation_type="PDO",
       designation_name="Goriška Brda Protected Designation of Origin",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Goriška Brda ('Collio' in Italian, shared with Friuli-Venezia Giulia across the border) is Slovenia's most prestigious wine region, producing white wines of extraordinary complexity from a unique combination of marine Eocene flysch soils (Ponca), Mediterranean sunshine, and cooling Alpine winds. Rebula (Ribolla Gialla) is the star indigenous variety; Pinela, Zelen, and Klarnica are other unique local whites. The region has also pioneered the modern 'orange wine' movement through extended skin contact maceration. Movia and Radikon (Italian side) are reference producers.",
       key_producers="Movia, Ščurek, Marjan Simčič, Klinec, Guerila Wines",
       historical_context="Goriška Brda sits on the border of Slovenia and Italy's Friuli region — historically the same viticultural area divided by the post-WWI border. The Ponca flysch soils that give both sides their distinctive mineral character are geologically identical. Aleš Kristančič at Movia has been one of the pioneers of natural wine and biodynamic viticulture in central Europe.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark vintage for Brda — Rebula and white blends of extraordinary mineral depth."),
    (2019,"very_good","stable","Fine conditions; white wines of excellent freshness and characteristic Ponca mineral."),
    (2020,"excellent","rising","Outstanding year; extended-maceration whites particularly successful for complexity."),
    (2021,"very_good","stable","Good vintage; wines showing classic flysch mineral character and aromatic precision."),
    (2022,"excellent","rising","Exceptional conditions; Rebula wines of benchmark quality across the appellation."),
    (2023,"excellent","rising","Another outstanding vintage; Brda's international reputation continues to rise."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Movia Winery Brda", "winery", r2, "Slovenia",
       production_philosophy="biodynamic",
       philosophy_description="Aleš Kristančič runs Movia as a biodynamic estate on both sides of the Slovenian-Italian border, producing wines from Ponca flysch soils without any additions or filtration. The estate's Lunar wine (Rebula with extended skin contact, riddled like Champagne and disgorged at the table) is one of the wine world's most theatrical and memorable experiences.",
       reputation_narrative="Movia is Slovenia's most internationally acclaimed winery and one of the natural wine movement's founding estates. Aleš Kristančič's uncompromising approach — no additions, no filtration, biodynamic farming — has produced wines that have helped define the orange wine category internationally.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Movia Lunar Rebula Brda", "wine_still", p2, r2, "Slovenia",
                    subcategory="orange_amber", description="The most theatrical wine in Europe — Rebula fermented on skins in amphora, then bottled like Champagne and disgorged tableside. Amber, tannic, mineral: dried stone fruit, chamomile, orange peel, and the distinctive Ponca flysch mineral backbone. An experience as much as a wine.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Raw Adriatic oysters with shallot vinegar", "complement", "adventurous", "amuse", "The amber wine's tannins and mineral bridge to raw oysters' brininess in an unexpected but powerful pairing.")
    PAIR(prod, "Prosciutto di San Daniele with melon and fresh herbs", "complement", "classic", "starter", "The wine's stone fruit and tannic structure complement cured ham; melon echoes the wine's dried apricot character.")
    PAIR(prod, "Grilled Adriatic prawns with aioli", "complement", "established", "starter", "Amber Rebula's tannic mineral grip handles prawns' richness; aioli's garlic echoes the wine's aromatic complexity.")
    PAIR(prod, "Aged Tolminc cheese from Slovenian Alps with honey", "complement", "established", "cheese", "Alpine hard cheese with Brda's greatest wine — shared Slovenian terroir; honey bridges the amber wine's dried fruit notes.")
prod, is_new = PROD("Marjan Simčič Leonardo Rebula Brda", "wine_still", p2, r2, "Slovenia",
                    subcategory="white", description="Fresh-style single-vineyard Rebula from the Leonardo parcel — golden, aromatic, mineral. Lemon blossom, white peach, almond, and the distinctive Ponca mineral salinity. Shows what Rebula can achieve in a modern, clean style without skin contact.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled Adriatic sea bass with capers and lemon", "complement", "classic", "main", "Classic Adriatic fish with Brda's finest fresh Rebula — lemon echoes the wine's citrus; capers bridge the mineral salinity.")
    PAIR(prod, "Pasta with porcini mushrooms, cream and parsley", "complement", "established", "main", "Almond and mineral Rebula bridges to porcini's earthiness; cream's richness is balanced by the wine's salinity.")
    PAIR(prod, "Veal scaloppine with lemon and parsley", "complement", "classic", "main", "The wine's freshness and mineral precision match veal's delicacy; lemon mirrors Rebula's citrus character.")
    PAIR(prod, "Sheep's milk ricotta with local honey and walnuts", "complement", "established", "cheese", "Almond notes bridge to ricotta's mild creaminess; honey echoes the wine's stone fruit character beautifully.")

# === WALKER BAY WO ===
print("=== Walker Bay WO ===")
r3 = R("Walker Bay WO", "South Africa", "wine",
       designation_type="WO",
       designation_name="Walker Bay Wine of Origin",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Walker Bay, 120km east of Cape Town on the southern tip of South Africa, is the Cape's coolest and most dramatically situated wine region. The Atlantic Ocean's cooling influence, Benguela current winds, and maritime climate enable Pinot Noir, Chardonnay, and Syrah to ripen slowly with remarkable elegance and mineral complexity. The Hemel-en-Aarde Valley ('Heaven and Earth') sub-region is South Africa's most celebrated cool-climate terroir, with Hamilton Russell Vineyards producing what many consider Africa's greatest Pinot Noir since 1981.",
       key_producers="Hamilton Russell Vineyards, Creation Wines, Bouchard Finlayson, Newton Johnson, Storm Wines",
       historical_context="Walker Bay wine production was pioneered by Tim Hamilton Russell in 1975 when he identified the Hemel-en-Aarde Valley's Burgundian potential. Despite initial government skepticism about wine production in this remote coastal area, Hamilton Russell's determination created one of South Africa's most prestigious wine regions.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Walker Bay vintage — Pinot Noir and Chardonnay of exceptional mineral depth."),
    (2019,"very_good","stable","Fine vintage; Hemel-en-Aarde wines showing classic cool-climate elegance and precision."),
    (2020,"excellent","rising","Outstanding year; Hamilton Russell and Creation wines achieving international acclaim."),
    (2021,"very_good","stable","Good conditions; wines of classic Walker Bay restraint and mineral complexity."),
    (2022,"excellent","rising","Benchmark vintage for Walker Bay Pinot Noir — wines of Burgundian precision."),
    (2023,"very_good","stable","Fine conditions; consistent quality across the Hemel-en-Aarde sub-regions."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Hamilton Russell Vineyards Walker Bay", "winery", r3, "South Africa",
       production_philosophy="terroir_expression",
       philosophy_description="Hamilton Russell Vineyards pioneered fine wine production in Walker Bay and remains South Africa's most prestigious estate. Anthony Hamilton Russell's focus on Pinot Noir and Chardonnay from the Hemel-en-Aarde Valley's unique clay-shale soils has produced wines that are the reference point for South African cool-climate viticulture.",
       reputation_narrative="Hamilton Russell Pinot Noir is Africa's most internationally acclaimed red wine — consistently compared to premier cru Burgundy in elegance, mineral complexity, and ageing potential. The estate has been instrumental in establishing South Africa as a serious cool-climate wine country.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Hamilton Russell Pinot Noir Hemel-en-Aarde", "wine_still", p3, r3, "South Africa",
                    subcategory="red", description="Africa's benchmark Pinot Noir from clay-shale soils in the Hemel-en-Aarde Valley. Elegant, precise, and mineral — red cherry, raspberry, dried herbs, wild strawberry, and a distinctive earth-mineral backbone unique to these ancient coastal soils. Requires 5+ years ageing for full expression.", price_tier="premium")
if is_new:
    PAIR(prod, "Pan-roasted Karoo lamb loin with mint jus", "complement", "classic", "main", "South Africa's finest Pinot Noir with its finest lamb — mineral Walker Bay wine meets Karoo's mineral-sweet lamb.")
    PAIR(prod, "Roasted beet salad with aged goat cheese and walnut", "complement", "established", "starter", "The wine's earthy mineral notes bridge to beet; goat cheese's tang contrasts Pinot's red fruit character.")
    PAIR(prod, "Grilled yellowtail with lemon and capers", "complement", "established", "main", "Cape coastal Pinot Noir and Cape coastal fish — mineral freshness mirrors yellowtail's oceanic character.")
    PAIR(prod, "Wild mushroom risotto with truffle oil and Parmesan", "bridge", "classic", "main", "The wine's earth-mineral backbone bridges to truffle; Parmesan's umami amplifies Pinot's depth.")
prod, is_new = PROD("Hamilton Russell Chardonnay Hemel-en-Aarde", "wine_still", p3, r3, "South Africa",
                    subcategory="white", description="Africa's finest Chardonnay from the same clay-shale terroir as the Pinot Noir. Mineral, restrained, and Burgundian — white peach, citrus, almond, and a saline mineral finish from the Atlantic's influence. Consistently rated among the world's top Chardonnays.", price_tier="premium")
if is_new:
    PAIR(prod, "Cape crayfish (South African lobster) with drawn butter", "complement", "classic", "main", "Africa's finest Chardonnay with Africa's finest crustacean — mineral precision and citrus match Cape crayfish's sweetness.")
    PAIR(prod, "Grilled whole Cape sole with herb butter", "complement", "classic", "main", "Mineral, restrained Chardonnay is the ideal partner for delicate sole; herb butter bridges the wine's almond notes.")
    PAIR(prod, "Seared scallops with saffron beurre blanc", "complement", "classic", "starter", "Saline mineral Chardonnay and scallop share coastal DNA; saffron bridges the wine's stone fruit complexity.")
    PAIR(prod, "Aged Gruyère with quince and walnut bread", "complement", "established", "cheese", "Almond and mineral notes in the Chardonnay bridge to Gruyère's nuttiness; quince echoes the wine's stone fruit character.")

# === SALTA WINE REGION ===
print("=== Salta Wine Region ===")
r4 = R("Salta Wine Region", "Argentina", "wine",
       designation_type="region",
       designation_name="Salta Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Salta, in northwestern Argentina's Andean foothills at 1,700–3,000m altitude, produces some of the world's most extreme and distinctive wines. The Calchaquí Valleys — particularly Cafayate — are home to Torrontés (Argentina's signature white) and high-altitude Malbec and Cabernet Sauvignon. The world's highest vineyards, some approaching 3,000m, experience intense UV radiation, massive diurnal temperature swings (up to 25°C), and low humidity that produce wines of extraordinary aromatic concentration, natural acidity, and colour intensity. Colomé and Achaval Ferrer (Cafayate labels) are reference producers.",
       key_producers="Colomé, El Esteco, Domingo Hermanos, Piattelli Vineyards, Tacuil",
       historical_context="Salta's Calchaquí Valleys have been home to viticulture since the Spanish Jesuit missionaries planted vineyards in the 16th century. Some of the original Colomé vineyard blocks planted in the 1830s still produce wine, making them among the oldest continuously productive vineyards in the Americas.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark Salta vintage — high-altitude Malbec and Torrontés of extraordinary aromatic intensity."),
    (2019,"very_good","stable","Good vintage; extreme altitude freshness preserved in both whites and reds."),
    (2020,"excellent","rising","Outstanding year; Cafayate wines of exceptional concentration from the intense Andean conditions."),
    (2021,"very_good","stable","Fine conditions; Torrontés and Malbec both showing classic high-altitude character."),
    (2022,"excellent","rising","Exceptional vintage for Salta — wines of benchmark quality at all altitude levels."),
    (2023,"very_good","stable","Good vintage; extreme diurnal variation produced wines of great freshness and depth."),
]:
    VIN(r4, yr, qd, pt, sn)

p4 = P("Colomé Estate Winery Salta", "winery", r4, "Argentina",
       production_philosophy="biodynamic",
       philosophy_description="Colomé, at 2,200–3,000m in the Calchaquí Valley, operates some of the world's highest vineyards, including the Altura Máxima at 3,111m. The Swiss Hess family have biodynamically farmed this historic estate since 2001, producing Malbec and Torrontés of extraordinary altitude-driven intensity and freshness.",
       reputation_narrative="Colomé is Argentina's most altitude-extreme estate — the Altura Máxima vineyard at 3,111m produces Malbec that is uniquely aromatic, high in natural acidity, and unlike any other Malbec on earth. The estate has also established a museum dedicated to artist James Turrell.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Colomé Altura Máxima Malbec Salta", "wine_still", p4, r4, "Argentina",
                    subcategory="red", description="World's highest Malbec from 3,111m — uniquely aromatic, high-acid, with extraordinary freshness for such an intense wine. Violet, dark cherry, black plum, graphite, and a distinctive UV-intensity concentration balanced by the altitude's natural acidity. Unlike any other Malbec on earth.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled Andean lamb with native potato and chimichurri", "complement", "classic", "main", "High-altitude Malbec with the local Andean lamb tradition — both shaped by altitude, both possessing extraordinary freshness.")
    PAIR(prod, "Empanadas de carne (beef and olive empanadas)", "complement", "classic", "starter", "Classic Argentine pairing — the wine's violets and dark fruit complement the empanada's spiced beef filling.")
    PAIR(prod, "Grilled prime Argentine beef (asado) with chimichurri", "complement", "classic", "main", "The quintessential Argentine pairing elevated — altitude Malbec and Andean-quality beef create an extraordinary combination.")
    PAIR(prod, "Dark chocolate with chilli and sea salt", "complement", "adventurous", "dessert", "UV-intensified Malbec's dark fruit bridges to dark chocolate; chilli echoes the wine's spice; salt heightens both.")
prod, is_new = PROD("El Esteco Don David Torrontés Cafayate Salta", "wine_still", p4, r4, "Argentina",
                    subcategory="white", description="High-altitude Torrontés from Cafayate at 1,700m — Argentina's most distinctive white variety at its most aromatic. Intensely perfumed: rose, jasmine, lychee, peach, and fresh spice, with a dry, mineral finish that prevents the variety from cloying. One of the wine world's most unique aromatic whites.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled spiced prawns with lime and fresh coriander", "complement", "classic", "starter", "Torrontés's rose and lychee aromatics complement the prawn's sweetness; lime echoes the wine's citrus freshness.")
    PAIR(prod, "Thai green curry with jasmine rice and fresh herbs", "complement", "classic", "main", "Aromatic Torrontés and aromatic Thai cuisine — jasmine in the wine mirrors jasmine rice; rose and lychee bridge to Thai spice.")
    PAIR(prod, "Ceviche with tiger's milk, chilli and fresh coriander", "complement", "established", "starter", "High-altitude freshness mirrors ceviche's citrus; aromatic intensity bridges to the fresh herb components.")
    PAIR(prod, "Fruit-based cheese course with melon and Manchego", "complement", "established", "cheese", "Rose and stone fruit in Torrontés bridge to the fruit accompaniment; Manchego's mild flavour doesn't compete with the wine's aromatics.")

# === RUSSIAN RIVER VALLEY AVA ===
print("=== Russian River Valley AVA ===")
r5 = R("Russian River Valley AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Russian River Valley American Viticultural Area",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Russian River Valley in Sonoma County is California's most celebrated cool-climate wine region, defined by persistent morning fog from the Pacific that cools the valley while afternoons warm enough to ripen Pinot Noir and Chardonnay. The region's Goldridge sandy loam soils — a unique sandy, well-draining terroir — and its foggy maritime climate produce California's most elegant, Burgundy-comparable Pinot Noir and Chardonnay. Williams Selyem, Rochioli, and Kosta Browne have defined the RRV style: rich, complex, and precise.",
       key_producers="Williams Selyem, Rochioli Vineyard, Kosta Browne, Gary Farrell, Benovia Winery",
       historical_context="Russian River Valley gained AVA status in 1983 but became internationally famous in the 1990s when wines from Williams Selyem and Rochioli began receiving international acclaim. The region's unique combination of Goldridge soil and daily fog cycle was identified as the critical factor producing California's finest cool-climate wines.")
for yr, qd, pt, sn in [
    (2018,"very_good","stable","Good vintage; fog-driven elegance preserved in Pinot Noir and Chardonnay."),
    (2019,"excellent","rising","Landmark RRV vintage — wines of exceptional mineral precision and aromatic complexity."),
    (2020,"challenging","stable","Smoke impact on some parcels; careful producers made excellent wine from clean sites."),
    (2021,"excellent","rising","Outstanding vintage; Pinot Noir and Chardonnay of benchmark quality across the AVA."),
    (2022,"very_good","stable","Fine conditions; more accessible Pinot Noir style with generous fruit and soft tannins."),
    (2023,"excellent","rising","Exceptional vintage for Russian River Valley — considered by many the finest in a decade."),
]:
    VIN(r5, yr, qd, pt, sn)

p5 = P("Williams Selyem Winery Russian River", "winery", r5, "USA",
       production_philosophy="minimal_intervention",
       philosophy_description="Williams Selyem was founded by Burt Williams and Ed Selyem in 1981 and created California's first true cult wine mailing list. Now owned by John Dyson, the winery continues producing benchmark Russian River Valley Pinot Noir from vineyard designates including Rochioli, Allen, and Precious Mountain.",
       reputation_narrative="Williams Selyem changed American wine — their small-production, Burgundian-inspired Pinot Noir proved that California could make world-class cool-climate wine. The mailing list (years-long waits) and cult following established a new model for premium California wine production.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Williams Selyem Rochioli Riverblock Pinot Noir Russian River", "wine_still", p5, r5, "USA",
                    subcategory="red", description="Single-vineyard Pinot Noir from the legendary Rochioli Riverblock parcel on Goldridge sandy loam — California's most revered Pinot terroir. Complex and mineral: dark cherry, cola, dried herbs, earth, and the unique Goldridge sandy mineral character. Ageable for 10–15 years.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted duck breast with cherry, juniper and lentils", "complement", "classic", "main", "The quintessential luxury RRV Pinot pairing — cherry notes mirror the sauce; duck's richness matches the wine's depth.")
    PAIR(prod, "Wild mushroom and foie gras terrine with brioche", "complement", "classic", "starter", "Pinot Noir's earthy complexity bridges to mushroom; foie's richness is balanced by the wine's mineral acidity.")
    PAIR(prod, "Grilled Pacific salmon with pinot noir reduction", "complement", "classic", "main", "California's iconic pairing — RRV Pinot and Pacific salmon; the wine's acidity and red fruit complement the salmon perfectly.")
    PAIR(prod, "Aged Humboldt Fog or Cypress Grove goat cheese", "complement", "classic", "cheese", "California coastal Pinot and California artisan goat cheese — mineral, cool-climate connection between wine and cheese.")
prod, is_new = PROD("Rochioli Estate Chardonnay Russian River Valley", "wine_still", p5, r5, "USA",
                    subcategory="white", description="The benchmark Russian River Valley Chardonnay from Joe Rochioli's estate — intensely mineral, precise, and restrained. Lemon curd, white peach, mineral, with subtle oak and the signature Goldridge sandy minerality. One of California's most age-worthy Chardonnays.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Dungeness crab with drawn butter and sourdough", "complement", "classic", "main", "The Northern California classic — RRV Chardonnay and Dungeness crab is the region's defining food pairing.")
    PAIR(prod, "Pan-seared halibut with beurre blanc and herbs", "complement", "classic", "main", "Mineral Chardonnay's precision and richness match halibut's delicate firmness; beurre blanc bridges the wine's texture.")
    PAIR(prod, "Seared scallops with citrus brown butter and capers", "complement", "classic", "starter", "The wine's lemon curd and mineral notes bridge to capers; brown butter echoes Chardonnay's subtle oak.")
    PAIR(prod, "Triple cream brie with California honey and crackers", "complement", "established", "cheese", "RRV Chardonnay's richness matches triple cream's buttery intensity; honey bridges the wine's stone fruit character.")

# === DB STATE ===
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
print("B169 complete.")
cur.close()
conn.close()
