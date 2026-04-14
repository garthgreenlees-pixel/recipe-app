#!/usr/bin/env python3
"""B165 — Global diversity: Baden QbA, Swiss Valais AOC, Swartland WO, Finger Lakes AVA, Clare Valley GI"""
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

# === BADEN QbA ===
print("=== Baden QbA ===")
r1 = R("Baden QbA", "Germany", "wine",
       designation_type="QbA",
       designation_name="Baden Qualitätswein bestimmter Anbaugebiete",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Germany's most southerly and warmest wine region, Baden stretches 400km from Heidelberg to Basel along the eastern bank of the Rhine. Unlike other German regions, Baden specialises in Spätburgunder (Pinot Noir), producing Germany's most celebrated red wines. Grauburgunder (Pinot Gris) and Weissburgunder (Pinot Blanc) also excel. The Kaiserstuhl — a volcanic island in the Rhine — produces intense, volcanic-mineral wines of great complexity. Baden's southern warmth and the Burgundy varieties' affinity for the region make these wines genuinely comparable to fine Burgundy.",
       key_producers="Bernhard Huber, Franz Keller, Rudolf Fürst (Franken/Baden), Dr. Heger, Weingut Salwey",
       historical_context="Baden has long been Germany's warmest wine region, producing powerful reds long before climate change made this fashionable. The Kaiserstuhl's volcanic soils have produced distinctive Pinot Noir for centuries, and the region's proximity to Burgundy has influenced both viticulture and winemaking styles.")
for yr, qd, pt, sn in [
    (2018,"exceptional","stable","A legendary Baden vintage — Spätburgunder of unusual concentration rivalling great Burgundy."),
    (2019,"excellent","rising","Outstanding Spätburgunder across the region; Kaiserstuhl volcanic wines particularly successful."),
    (2020,"very_good","stable","Fine vintage; Grauburgunder and Weissburgunder produced wines of great elegance."),
    (2021,"very_good","stable","Cooler year produced more elegant, Burgundian-style Spätburgunder with bright acidity."),
    (2022,"excellent","rising","Another exceptional red vintage; Spätburgunder of great depth and structure."),
    (2023,"excellent","rising","Fine conditions across Baden; volcanic Kaiserstuhl wines particularly impressive."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Weingut Bernhard Huber", "winery", r1, "Germany",
       production_philosophy="terroir_expression",
       philosophy_description="Bernhard Huber (continued by his son Julian) is widely considered Germany's greatest Spätburgunder producer. Their Malterdingen-based estate produces wines from the Bienenberg vineyard that rival premier and grand cru Burgundy at a fraction of the price.",
       reputation_narrative="Huber's Bienenberg Spätburgunder GG is consistently rated among Germany's finest red wines and has changed international perceptions of German Pinot Noir's quality potential — elegant, complex, and age-worthy.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Huber Bienenberg Spätburgunder GG Baden", "wine_still", p1, r1, "Germany",
                    subcategory="red", description="Grosses Gewächs Spätburgunder from the Bienenberg's limestone and loess — elegant, Burgundy-benchmark quality. Red cherry, raspberry, silky tannins, subtle oak, and a mineral freshness that evolves over 10+ years. Germany's most celebrated red.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted Bresse chicken with mushroom cream sauce", "complement", "classic", "main", "The GG's Burgundian elegance mirrors the classic French preparation — red fruit and silky tannins lift the chicken perfectly.")
    PAIR(prod, "Slow-roasted duck breast with cherry reduction", "complement", "classic", "main", "Cherry notes in the wine echo the reduction; the Spätburgunder's acidity cuts through duck's richness.")
    PAIR(prod, "Roasted wild mushrooms with thyme and parsley", "bridge", "established", "starter", "Earthy mineral notes bridge to wild mushroom depth; red fruit brightens the earthiness.")
    PAIR(prod, "Aged Époisses or Munster cheese", "complement", "established", "cheese", "The GG's pinot elegance handles washed rind intensity; shared earthiness between wine and cheese creates harmony.")
prod, is_new = PROD("Huber Malterdingen Spätburgunder Baden", "wine_still", p1, r1, "Germany",
                    subcategory="red", description="Village Spätburgunder from Malterdingen — the accessible entry to Huber's range, but with hallmark elegance. Bright red cherry, strawberry, violet, fine tannins, and mineral freshness. Perfect for earlier drinking.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled salmon fillet with pinot noir butter sauce", "complement", "adventurous", "main", "Light-bodied Spätburgunder is the ideal red for rich salmon — a classic pairing that crosses the fish-red wine boundary.")
    PAIR(prod, "Roasted pork loin with sage and apple", "complement", "established", "main", "Elegant Spätburgunder fruit bridges to pork's sweetness; apple echoes the wine's bright fruit character.")
    PAIR(prod, "Warm goat cheese salad with roasted beets", "complement", "classic", "starter", "Red cherry and mineral freshness balance goat cheese's tang; beets echo the wine's earthy depth.")
    PAIR(prod, "Venison carpaccio with pickled wild berries", "complement", "established", "starter", "The wine's red fruit and silky tannins complement raw venison's delicacy; berries echo the fruit character.")

# === SWISS VALAIS AOC ===
print("=== Swiss Valais AOC ===")
r2 = R("Swiss Valais AOC", "Switzerland", "wine",
       designation_type="AOC",
       designation_name="Valais Appellation d'Origine Contrôlée",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Switzerland's most important wine region, the Valais stretches along the upper Rhône Valley, sheltered by the Alps on both sides. The unique microclimate — 300+ days of sunshine, warm Foehn winds, and low rainfall — produces Switzerland's most concentrated and complex wines. Fendant (Chasselas) is the dominant white; Dôle (Pinot Noir and Gamay) the classic red; but the region's greatest wines come from indigenous varieties like Petite Arvine, Humagne Rouge, Cornalin (Rouge du Pays), and Amigne de Vétroz. These near-extinct grapes, grown on vertiginous terraced vineyards above the Rhône, produce wines of extraordinary character found nowhere else on earth.",
       key_producers="Marie-Thérèse Chappaz, Gilles Besse, Jean-René Germanier, Domaine du Mont d'Or",
       historical_context="Valais viticulture dates to the Roman era, and the vertiginous terrace vineyards — some of the steepest in Europe — represent centuries of human endeavour. The region's indigenous varieties, like Petite Arvine and Cornalin, survived in isolation while the rest of the world planted international varieties.")
for yr, qd, pt, sn in [
    (2018,"exceptional","stable","A legendary Valais vintage — all varieties showing extraordinary concentration and balance."),
    (2019,"excellent","stable","Excellent year; Petite Arvine and Humagne Rouge particularly compelling."),
    (2020,"very_good","stable","Fine vintage; Fendant and Dôle wines of good freshness and typical Alpine character."),
    (2021,"very_good","stable","Cooler year produced more elegant wines with good acidity and floral aromatics."),
    (2022,"excellent","rising","Outstanding vintage for Cornalin and Humagne Rouge; concentratedreds of great structure."),
    (2023,"excellent","rising","Fine conditions produced Petite Arvine of exceptional aromatic intensity and precision."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Marie-Thérèse Chappaz", "winery", r2, "Switzerland",
       production_philosophy="biodynamic",
       philosophy_description="Marie-Thérèse Chappaz is Switzerland's most celebrated winemaker, farming biodynamically on vertiginous terraces above Fully in the Valais. Her Petite Arvine and Cornalin are Switzerland's reference expressions of these rare indigenous varieties, produced in tiny quantities and sought by collectors worldwide.",
       reputation_narrative="Chappaz is considered the greatest winemaker in Swiss history — her estate-bottled Petite Arvine, Cornalin, and sweet VT wines have placed Switzerland among the world's most distinctive wine nations. She farms with extraordinary respect for her steep, ancient terraces.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Chappaz Petite Arvine Valais", "wine_still", p2, r2, "Switzerland",
                    subcategory="white", description="The definitive expression of Petite Arvine — Switzerland's most distinctive indigenous white. Intensely aromatic: grapefruit, spring flowers, passion fruit, and the variety's signature salty mineral finish from the Alpine terraces. Among Switzerland's rarest and most sought wines.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Raclette with Alpine potatoes and pickled cornichons", "complement", "classic", "main", "The quintessential Valais pairing — Petite Arvine's salt and acidity cut through raclette's richness; cornichons echo the wine's bright minerality.")
    PAIR(prod, "Air-dried Bundnerfleisch (Valais dried beef) with pickled vegetables", "complement", "classic", "starter", "Salt in the wine bridges to cured beef's intensity; acidity refreshes between bites of the preserved meat.")
    PAIR(prod, "Grilled lake perch from Lake Geneva with lemon", "complement", "classic", "main", "A Swiss Alpine classic — Petite Arvine's mineral salinity mirrors the freshwater fish; lemon echoes the wine's citrus.")
    PAIR(prod, "Asparagus risotto with Parmesan and lemon zest", "complement", "established", "main", "The wine's acidity and floral notes lift asparagus; Parmesan's umami bridges to Petite Arvine's mineral depth.")
prod, is_new = PROD("Chappaz Cornalin Valais Rouge", "wine_still", p2, r2, "Switzerland",
                    subcategory="red", description="Cornalin (Rouge du Pays) — a nearly extinct Alpine indigenous variety revived by Chappaz. Deep ruby, intensely perfumed: wild raspberry, Alpine flowers, red plum, dried herbs, and a silky, medium-bodied structure. One of the world's rarest great red wines.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Braised venison with Alpine herbs and cranberry", "complement", "classic", "main", "Alpine Cornalin's red fruit and floral character match mountain game perfectly; cranberry echoes the wine's wild berry notes.")
    PAIR(prod, "Fonduta with truffles and polenta", "bridge", "established", "main", "The wine's floral complexity bridges to truffle's earthiness; polenta's corn sweetness echoes Cornalin's fruit.")
    PAIR(prod, "Aged Gruyère with walnut bread and honey", "complement", "established", "cheese", "Great Alpine cheese meets the Valais's greatest red — Gruyère's nuttiness bridges Cornalin's wild herb notes.")
    PAIR(prod, "Roasted duck magret with cherry and balsamic", "complement", "classic", "main", "The wine's cherry and floral notes echo the cherry preparation; balsamic bridges the wine's natural acidity.")

# === SWARTLAND WO ===
print("=== Swartland WO ===")
r3 = R("Swartland WO", "South Africa", "wine",
       designation_type="WO",
       designation_name="Swartland Wine of Origin",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The Swartland, northwest of Cape Town, has been transformed from bulk wine producer to South Africa's most exciting wine region by the 'Swartland Revolution' — a generation of artisan winemakers who relocated here for its old-vine Chenin Blanc, dryland Grenache, Syrah, and Cinsault. The region's schist, granite, and clay soils combined with Mediterranean climate and cooling Atlantic breezes produce wines of extraordinary intensity and complexity. Key producers Eben Sadie and Chris Mullineux have placed Swartland among the world's great wine regions.",
       key_producers="Sadie Family Wines, Mullineux & Leeu, Lammershoek, David & Nadia, AA Badenhorst",
       historical_context="Swartland means 'black land' in Afrikaans — named for the renosterbos shrub that darkens the landscape. While historically the source of anonymous co-op wine, the Swartland Revolution of the early 2000s brought artisan producers who recognised the region's old-vine potential and transformed it into one of the world's most talked-about emerging wine regions.")
for yr, qd, pt, sn in [
    (2017,"excellent","rising","A landmark Swartland vintage — old-vine Chenin and Rhône varieties of extraordinary complexity."),
    (2018,"very_good","stable","Fine vintage; particularly successful for Chenin Blanc and single-vineyard Syrah."),
    (2019,"challenging","stable","A difficult year due to drought; careful producers made concentrated, vibrant wines."),
    (2020,"excellent","rising","Outstanding vintage; Swartland Revolution wines of exceptional depth and freshness."),
    (2021,"excellent","rising","One of the finest recent Swartland vintages — old-vine Chenin of benchmark quality."),
    (2022,"very_good","stable","Warm year; Syrah and Grenache showing rich, spicy concentration."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Sadie Family Wines", "winery", r3, "South Africa",
       production_philosophy="biodynamic",
       philosophy_description="Eben Sadie is the architect of the Swartland Revolution and South Africa's most celebrated winemaker. His Columella (old-vine Syrah blend) and Palladius (old-vine Chenin Blanc blend) have become national icons. His single-vineyard 'Old Vine Series' explores individual parcels across the Cape Winelands.",
       reputation_narrative="Sadie Family Wines has defined South African fine wine for the 21st century. Columella and Palladius are consistently among Africa's greatest wines, while the Old Vine Series has inspired a generation of artisan producers across the Cape.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Sadie Columella Swartland", "wine_still", p3, r3, "South Africa",
                    subcategory="red", description="South Africa's most iconic red — old-vine Syrah with Mourvedre, Grenache, and other Rhône varieties from Swartland's schist and granite soils. Dark-fruited, spiced, with olives, violets, leather, iron, and a long mineral finish. Requires 10+ years cellaring for full expression.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Slow-roasted Karoo lamb shoulder with harissa and preserved lemon", "complement", "classic", "main", "South Africa's great terroir wine meets its greatest meat — Karoo lamb's mineral sweetness bridges to Columella's iron-mineral backbone.")
    PAIR(prod, "Braised oxtail with red wine, herbs and root vegetables", "complement", "established", "main", "Columella's power and complexity demand collagen-rich oxtail; shared earthiness deepens both.")
    PAIR(prod, "Grilled Springbok loin with wild berry reduction", "complement", "established", "main", "Indigenous Cape game meets South Africa's finest Syrah — the wine's spice and dark fruit mirror springbok's lean gaminess.")
    PAIR(prod, "Aged Cheddar with biltong and dried fruit", "complement", "adventurous", "cheese", "South African biltong's savouriness bridges Columella's iron and spice; aged Cheddar's sharpness complements the wine's fruit.")
prod, is_new = PROD("Sadie Palladius Old Vine White Swartland", "wine_still", p3, r3, "South Africa",
                    subcategory="white", description="Swartland's greatest white — old-vine Chenin Blanc with Clairette, Viognier, Grenache Blanc, and others from multiple sites. Profound: beeswax, quince, yellow flowers, smoke, and a mineral depth that places it among Africa's greatest white wines.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Whole-roasted chicken with herbs and preserved lemon", "complement", "classic", "main", "Palladius's complexity demands equally complex preparation; preserved lemon echoes the wine's waxy citrus character.")
    PAIR(prod, "Cape Malay chicken curry with turmeric and coconut", "complement", "adventurous", "main", "The wine's tropical and floral notes bridge to Cape Malay spices; its richness stands up to coconut's creaminess.")
    PAIR(prod, "Grilled yellowtail with capers and herb oil", "complement", "established", "main", "Old-vine Chenin's texture and mineral depth match yellowtail's meaty flesh; capers echo the wine's natural acidity.")
    PAIR(prod, "Aged Gruyère with quince paste", "complement", "established", "cheese", "Beeswax and quince notes in Palladius mirror the quince paste; Gruyère's Alpine nuttiness bridges the wine's depth.")

p4 = P("Mullineux and Leeu Family Wines", "winery", r3, "South Africa",
       production_philosophy="biodynamic",
       philosophy_description="Chris and Andrea Mullineux are the most critically acclaimed winemakers in South Africa, producing single-terroir Syrah and Chenin Blanc wines that capture the Swartland's distinct soil types — schist, granite, iron, and clay. Their Leeu Passant range extends the philosophy across the Cape.",
       reputation_narrative="Mullineux wines have earned Platter's South African Wine Guide's top awards multiple times. Their Schist and Granite Syrah wines demonstrate that terroir-specific single-vineyard wine is as relevant in South Africa as in Burgundy or the Northern Rhône.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Mullineux Schist Syrah Swartland", "wine_still", p4, r3, "South Africa",
                    subcategory="red", description="Single-terroir Syrah from schist soils — dark, spicy, with smoked meat, graphite, black olive, and violet. The schist profile gives this Swartland Syrah its distinctive mineral edge and structure for long ageing.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled duck breast with olive tapenade and thyme", "complement", "classic", "main", "Schist Syrah's olive and spice notes mirror tapenade; duck's richness complements the wine's dark fruit depth.")
    PAIR(prod, "Lamb chops with rosemary and black olive oil", "complement", "classic", "main", "Syrah's pepper and dark fruit stand up to charred lamb; olive oil bridges the wine's olive note naturally.")
    PAIR(prod, "Roasted portobello mushrooms with truffle and thyme", "bridge", "established", "starter", "Graphite and mineral notes in the wine bridge to truffle and mushroom earthiness.")
    PAIR(prod, "Boerewors with chakalaka and pap", "complement", "adventurous", "main", "South African farm sausage with spiced tomato relish — rustic Swartland wine with equally rustic South African fare.")

# === FINGER LAKES AVA ===
print("=== Finger Lakes AVA ===")
r4 = R("Finger Lakes AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Finger Lakes American Viticultural Area",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="The Finger Lakes region in upstate New York, centred on Seneca and Cayuga Lakes, is America's premier cool-climate wine region. The deep lakes moderate temperatures, preventing winter freezing and enabling Riesling to ripen fully while retaining extraordinary acidity. Finger Lakes Riesling — dry, off-dry, and late harvest — has earned comparisons to Mosel and Alsace. Blaufränkisch, Gewürztraminer, and Cabernet Franc also succeed in warmer vintages. The region combines Old World viticulture sensibility with American entrepreneurialism.",
       key_producers="Dr. Konstantin Frank, Hermann J. Wiemer, Red Newt Cellars, Ravines Wine Cellars, Bloomer Creek",
       historical_context="The Finger Lakes wine industry was transformed by Dr. Konstantin Frank, who in the 1960s proved that vinifera grapes could survive the harsh upstate New York winters. His Riesling planted in 1958 still produces wines today, vindicating his controversial decision to plant European varieties.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark Finger Lakes vintage — Riesling of exceptional balance and aromatic intensity."),
    (2019,"very_good","stable","Good ripeness achieved in a challenging year; Seneca Lake producers particularly successful."),
    (2020,"excellent","rising","Fine vintage with excellent Riesling acidity and concentration across the region."),
    (2021,"very_good","stable","Classic cool Finger Lakes vintage producing precise, mineral Riesling for ageing."),
    (2022,"very_good","rising","Warm year; accessible, aromatic Riesling alongside concentrated Blaufränkisch."),
    (2023,"excellent","rising","Outstanding vintage for dry and off-dry Riesling — wines of international reference quality."),
]:
    VIN(r4, yr, qd, pt, sn)

p5 = P("Dr. Konstantin Frank Winery", "winery", r4, "USA",
       production_philosophy="terroir_expression",
       philosophy_description="The pioneering winery that proved vinifera viticulture was possible in the Finger Lakes, founded by the visionary Ukrainian-American scientist Konstantin Frank. Now run by his grandson Frederick, the estate remains the region's most historic and produces benchmark Riesling and Gewürztraminer.",
       reputation_narrative="Dr. Frank's Winery is the Finger Lakes' founding estate and still produces the region's most historically significant wines. Their dry Riesling and Salmon Run off-dry Riesling have introduced millions of Americans to Finger Lakes viticulture.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Dr. Frank Dry Riesling Finger Lakes", "wine_still", p5, r4, "USA",
                    subcategory="white", description="Benchmark dry Finger Lakes Riesling — lime, green apple, white peach, and the distinctive slate-mineral backbone of cool-climate lake viticulture. Bright, refreshing, and structured for ageing.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Pan-seared rainbow trout with lemon and capers", "complement", "classic", "main", "Finger Lakes Riesling and local lake fish — the regional pairing. Mineral acidity and citrus mirror the fish's delicate flavours.")
    PAIR(prod, "Pork chop with apple and onion", "complement", "established", "main", "Off-dry Riesling notes and apple are natural bridges to pork; the wine's acidity cuts through the meat's richness.")
    PAIR(prod, "Sautéed wild ramps with butter and salt", "complement", "established", "starter", "The wine's mineral freshness complements seasonal wild ramps; butter bridges Riesling's slight richness.")
    PAIR(prod, "Aged cheddar from Finger Lakes creamery", "complement", "established", "cheese", "Local cheddar with local Riesling — mineral wine and sharp cheese create a classic New York food and wine pairing.")
prod, is_new = PROD("Dr. Frank Gewurztraminer Finger Lakes", "wine_still", p5, r4, "USA",
                    subcategory="white", description="Aromatic Finger Lakes Gewürztraminer — rose petal, lychee, ginger, and spice in a slightly off-dry style. One of America's finest expressions of this Alsatian variety, showing that cool lake temperatures preserve Gewürztraminer's aromatic intensity.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Thai green curry with jasmine rice", "complement", "classic", "main", "The wine's ginger and lychee notes mirror Thai aromatics; slight sweetness tames chilli heat — a classic pairing.")
    PAIR(prod, "Foie gras terrine with ginger and peach chutney", "complement", "established", "starter", "Ginger and stone fruit in the wine bridge to the chutney; slight sweetness contrasts foie's richness beautifully.")
    PAIR(prod, "Smoked salmon with crème fraîche and dill", "complement", "classic", "starter", "Rose petal Gewürztraminer echoes smoked salmon's floral smoke character; dill bridges the herbal freshness.")
    PAIR(prod, "Munster or Limburger washed rind cheese", "complement", "classic", "cheese", "The Alsatian classic — Gewürztraminer and pungent washed rind cheese is one of wine's great regional matches.")

# === CLARE VALLEY GI ===
print("=== Clare Valley GI ===")
r5 = R("Clare Valley GI", "Australia", "wine",
       designation_type="GI",
       designation_name="Clare Valley Geographic Indication",
       reputation_tier="respected",
       quality_trajectory="established",
       description="Clare Valley, 130km north of Adelaide in South Australia, is one of Australia's most distinctive wine regions. At 400–500m altitude with warm days and cool nights, it produces Australia's greatest Riesling — bone dry, high acid, lime and slate-mineral driven, with extraordinary ageing potential. Clare Riesling develops petrol and toast complexity with age that rivals German and Alsatian expressions. Shiraz from the valley's red soils is also world-class, and Clare was an early adopter of screw cap closures, which helped preserve the Riesling's freshness.",
       key_producers="Grosset Wines, Jim Barry Wines, Skillogalee, Wendouree, Pike's Wines",
       historical_context="Clare Valley was settled for wine production in the 1840s by German and Silesian settlers who recognized the valley's similarity to their homeland. This heritage explains the region's affinity for Riesling. Clare was the pioneer of the screwcap movement in Australian wine, helping to standardize closure quality.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Outstanding Clare Riesling vintage — wines of exceptional concentration and ageing potential."),
    (2019,"very_good","stable","Fine year; Riesling showing classic lime and slate mineral character."),
    (2020,"very_good","stable","Challenging bushfire season but the valley escaped damage; quality Riesling produced."),
    (2021,"excellent","rising","A landmark Clare vintage — Riesling of extraordinary mineral precision and depth."),
    (2022,"very_good","stable","Good ripeness; both Riesling and Shiraz showing the valley's characteristic intensity."),
    (2023,"excellent","rising","Exceptional conditions produced Clare Riesling of benchmark quality."),
]:
    VIN(r5, yr, qd, pt, sn)

p6 = P("Grosset Wines Clare Valley", "winery", r5, "Australia",
       production_philosophy="minimal_intervention",
       philosophy_description="Jeffrey Grosset is Australia's most celebrated Riesling producer, making two distinct single-vineyard Clare Rieslings: Polish Hill (slate, intense mineral) and Springvale (limestone, floral). Both are benchmarks for Australian Riesling and have been critical to the region's international reputation.",
       reputation_narrative="Grosset's Polish Hill and Springvale Rieslings are consistently rated among Australia's finest white wines and have proven that Australian Riesling can age for 20+ years with compelling complexity. Jeffrey Grosset helped lead the screwcap revolution that transformed Australian wine quality.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Grosset Polish Hill Riesling Clare Valley", "wine_still", p6, r5, "Australia",
                    subcategory="white", description="Single-vineyard Riesling from the Polish Hill site with its distinctive Cambrian slate soils. Austere, laser-precise — lime zest, slate, white flowers, and a long mineral finish. Requires 5–15 years ageing for full expression; one of Australia's greatest white wines.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled Murray cod with lemon and capers", "complement", "classic", "main", "Australian freshwater fish with Clare's finest Riesling — slate mineral and lime mirror the fish's delicate sweetness.")
    PAIR(prod, "King prawns with nam prik and fresh lime", "complement", "classic", "starter", "Riesling's citrus and mineral freshness mirror the lime in nam prik; the wine tames chilli heat elegantly.")
    PAIR(prod, "Sashimi of kingfish with citrus dressing", "complement", "established", "starter", "The wine's limestone mineral notes mirror kingfish's delicate fat; citrus dressing echoes Riesling's lime character.")
    PAIR(prod, "Aged cheddar with quince paste — South Australian", "complement", "established", "cheese", "Clare Riesling's acidity cuts aged cheddar's richness; mineral notes contrast the quince sweetness beautifully.")
prod, is_new = PROD("Grosset Springvale Riesling Clare Valley", "wine_still", p6, r5, "Australia",
                    subcategory="white", description="Single-vineyard Riesling from limestone-derived soils at Springvale — more floral and approachable than Polish Hill. Lime blossom, citrus, slate, and a softer mineral finish that opens earlier. Also ages beautifully for 10+ years.", price_tier="premium")
if is_new:
    PAIR(prod, "Steamed barramundi with ginger and soy", "complement", "classic", "main", "Floral, delicate Springvale mirrors barramundi's sweetness; ginger echoes the wine's freshness.")
    PAIR(prod, "Oysters with cucumber granita and lime", "complement", "classic", "amuse", "Limestone mineral Riesling and briny oysters share oceanic depth; cucumber and lime mirror the wine's freshness.")
    PAIR(prod, "Lemon and herb roasted chicken with roasted fennel", "complement", "established", "main", "Floral Riesling and lemon chicken create a citrus harmony; fennel's anise notes echo the wine's herbal dimension.")
    PAIR(prod, "Mild goat cheese with cucumber and dill", "complement", "established", "cheese", "Springvale's floral freshness complements mild goat cheese; dill bridges the herbal notes.")

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
print("B165 complete.")
cur.close()
conn.close()
