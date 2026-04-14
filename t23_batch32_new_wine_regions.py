import psycopg2

conn = psycopg2.connect("postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable")
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
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""
        INSERT INTO beverage_vintages (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
    """, (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === RHEINGAU (Germany) ===
print("\n=== Rheingau (Germany) ===")
r_rheingau = R(
    name="Rheingau",
    country="Germany",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Rheingau",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Germany's most historic Riesling region, where the Rhine bends east and south-facing slopes produce wines of remarkable structure and longevity. The Rheingau stretches from Rüdesheim to Hochheim, with legendary single vineyard sites including Schloss Johannisberg, Steinberg, and Rüdesheimer Berg Schlossberg. Wines here tend towards power and minerality, with a distinct slate and herbal character setting them apart from the steelier Mosel style.",
    key_producers="Weingut Robert Weil, Schloss Johannisberg, Georg Breuer, Weingut Künstler, Schloss Vollrads",
    historical_context="Monks at Kloster Eberbach established viticulture here in the 12th century. Schloss Johannisberg is credited with the discovery of Spätlese — harvesting overripe botrytised grapes — in 1775. The Rheingau was historically Germany's most prestigious wine region, rivaled only by Burgundy in European prestige."
)
for yr, qd, pt, sn in [
    (2021, "exceptional", "rising", "Ideal growing season with warm summer and cool autumn. Rieslings of great concentration and freshness, exceptional Spätlesen and Auslesen."),
    (2020, "excellent", "rising", "Warm, dry year producing powerful, rich Rieslings with good natural acidity. GGs show remarkable depth."),
    (2019, "exceptional", "rising", "Third of three consecutive warm vintages. Concentrated, complex wines with great aging potential."),
    (2018, "excellent", "stable", "Hot, dry summer produced full, rich wines. Lower acidity than typical but compensated by extract."),
    (2017, "very_good", "stable", "Late frosts reduced crop significantly. Survivors showed excellent quality and concentration."),
]:
    VIN(r_rheingau, yr, qd, pt, sn)

p_weil = P(
    name="Weingut Robert Weil",
    country="Germany",
    region_id=r_rheingau,
    producer_type="winery",
    description="The benchmark estate of the Rheingau and one of Germany's greatest wine producers. Based in Kiedrich, Robert Weil produces Rieslings of extraordinary purity from the Gräfenberg monopole vineyard — a steep, south-facing slate slope. Wilhelm Weil took over in the 1980s and raised the estate to international prominence. Their Trockenbeerenauslesen fetch some of the highest prices of any German wine."
)
prod_weil, new = PROD(
    name="Weingut Robert Weil Kiedrich Gräfenberg Riesling Spätlese",
    category="wine_dessert",
    subcategory="Riesling",
    producer_id=p_weil,
    region_id=r_rheingau,
    origin_country="Germany",
    description="From the Gräfenberg monopole — Kiedrich's greatest site — this Spätlese is the definitive Rheingau Riesling. Naturally sweet with impeccable balance, aromas of white peach, apricot, orange blossom, and wet slate. The hallmark petrol note emerges with age alongside honeyed complexity. Acidity cuts through the sweetness perfectly, giving a wine of extraordinary elegance.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_weil, "Foie gras terrine with brioche and Sauternes gel", "complement", "classic", "starter", "The wine's residual sugar and acidity mirror the fatty richness and sweetness of foie gras. Slate minerality cuts through the fat, while stone fruit notes harmonise with the terrine.")
    PAIR(prod_weil, "Spiced pork belly with apple and fennel", "complement", "established", "main", "Classic German affinity — Riesling Spätlese is made for pork. Apple and fennel echo the wine's fruit character, spice amplifies its complexity, and natural sweetness balances the fat.")
    PAIR(prod_weil, "Mango panna cotta with cardamom", "bridge", "suggested", "dessert", "The wine's tropical fruit notes bridge to mango, while its acidity prevents cloying sweetness. Cardamom adds aromatic interest without competing.")
    PAIR(prod_weil, "Aged Comté with honeycomb", "complement", "established", "cheese", "Nutty aged cheese meets the honey and stone fruit of Spätlese. Sweetness plays against the cheese's savouriness in a classic combination.")
else:
    # Product inserted on prior failed run — add pairings directly
    PAIR(prod_weil, "Foie gras terrine with brioche and Sauternes gel", "complement", "classic", "starter", "The wine's residual sugar and acidity mirror the fatty richness and sweetness of foie gras. Slate minerality cuts through the fat, while stone fruit notes harmonise with the terrine.")
    PAIR(prod_weil, "Spiced pork belly with apple and fennel", "complement", "established", "main", "Classic German affinity — Riesling Spätlese is made for pork. Apple and fennel echo the wine's fruit character, spice amplifies its complexity, and natural sweetness balances the fat.")
    PAIR(prod_weil, "Mango panna cotta with cardamom", "bridge", "suggested", "dessert", "The wine's tropical fruit notes bridge to mango, while its acidity prevents cloying sweetness. Cardamom adds aromatic interest without competing.")
    PAIR(prod_weil, "Aged Comté with honeycomb", "complement", "established", "cheese", "Nutty aged cheese meets the honey and stone fruit of Spätlese. Sweetness plays against the cheese's savouriness in a classic combination.")

p_breuer = P(
    name="Georg Breuer",
    country="Germany",
    region_id=r_rheingau,
    producer_type="winery",
    description="The pioneering Rüdesheim estate that championed dry Rheingau Riesling before it was fashionable. Bernhard Breuer was instrumental in founding the VDP and pushing for quality classification in the Rheingau. Today under Teresa Breuer, the estate crafts benchmark dry Rieslings from the steep Berg Schlossberg and Rüdesheimer Berg Rottland sites — wines of great ageworthiness and mineral precision."
)
prod_breuer, new = PROD(
    name="Georg Breuer Berg Schlossberg Rüdesheim Riesling Erstes Gewächs",
    category="wine_still",
    subcategory="Riesling",
    producer_id=p_breuer,
    region_id=r_rheingau,
    origin_country="Germany",
    description="The flagship dry Riesling from Rüdesheim's most prestigious site — a steep, slate-dominated slope producing wines of structural power and mineral intensity. Bone dry with electrifying acidity, aromas of white citrus, green apple, crushed slate, and white flowers. Builds extraordinary complexity with age, developing petrol, honey, and toast notes over a decade.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_breuer, "Grilled turbot with brown butter capers and parsley", "complement", "classic", "main", "The wine's mineral precision and citrus acidity are classically matched to turbot. Brown butter bridges to the wine's richness while capers mirror its salinity.")
    PAIR(prod_breuer, "Veal schnitzel with potato salad and lingonberries", "complement", "classic", "main", "The definitive Rheingau food pairing — dry Riesling with schnitzel. The wine's acidity cuts through the breading, lingonberry echoes its fruit, and its mineral backbone elevates the delicate veal.")
    PAIR(prod_breuer, "Sauerkraut and smoked pork knuckle", "complement", "established", "main", "The high acidity of dry Riesling is designed for fermented and fatty dishes. This traditional pairing demonstrates the wine's utility at a regional table.")
    PAIR(prod_breuer, "Seared scallops with pea purée and dashi foam", "bridge", "suggested", "starter", "Mineral Riesling bridges Japanese and European flavour registers. Dashi echoes the wine's saline quality, pea purée mirrors its green notes, and the scallop's sweetness balances its acidity.")

# === KAMPTAL (Austria) ===
print("\n=== Kamptal DAC (Austria) ===")
r_kamptal = R(
    name="Kamptal",
    country="Austria",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Kamptal DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="A premier Austrian wine region following the Kamp river north from the Danube, home to some of the world's finest dry Grüner Veltliner and Riesling. The region's volcanic Urgestein soils — predominantly gneiss and mica schist — impart a distinctive mineral tension and spice to wines from the great Heiligenstein and Lamm sites. Kamptal DAC protects both varieties, and the region's Erste Lagen and Grosse Lagen represent Austria's quality apex.",
    key_producers="Weingut Bründlmayer, Schloss Gobelsburg, Weingut Hirsch, Fred Loimer",
    historical_context="The Kamp valley has been cultivated since Roman times, though modern recognition came in the late 20th century when producers like Bründlmayer began bottling site-specific wines. The Heiligenstein — a volcanic, south-facing slope of ancient origin — is now recognised as one of Austria's greatest single vineyards."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, elegant vintage producing wines of great finesse. Heiligenstein Rieslings show exceptional minerality and aging potential."),
    (2020, "exceptional", "rising", "Rich, concentrated vintage with perfect ripeness. Grüner Veltliner of great complexity and length."),
    (2019, "excellent", "stable", "Warm, dry conditions produced powerful wines with good acidity from cooler nights. Outstanding across all styles."),
    (2018, "very_good", "stable", "Hot vintage producing rich, full wines. Early-picked lots show excellent freshness."),
    (2017, "excellent", "stable", "Cool spring, warm summer. Rieslings of particular precision and mineral definition."),
]:
    VIN(r_kamptal, yr, qd, pt, sn)

p_brundl = P(
    name="Weingut Bründlmayer",
    country="Austria",
    region_id=r_kamptal,
    producer_type="winery",
    description="The most celebrated estate in the Kamptal and a cornerstone of Austrian fine wine. Willi Bründlmayer has farmed biodynamically and crafted benchmark Grüner Veltliner and Riesling from Langenlois for decades. His Alte Reben Grüner Veltliner and Heiligenstein Riesling are considered among Austria's greatest wines, showing the depth and aging potential that makes Kamptal internationally significant."
)
prod_brundl, new = PROD(
    name="Bründlmayer Zöbinger Heiligenstein Riesling Alte Reben",
    category="wine_still",
    subcategory="Riesling",
    producer_id=p_brundl,
    region_id=r_kamptal,
    origin_country="Austria",
    description="Austria's most iconic single-vineyard Riesling, from old vines on the Heiligenstein — a volcanic outcrop of Permian red sandstone above Zöbing. The wine is dry, mineral, and almost impossibly complex, with white citrus, green apple, volcanic stone, white pepper, and floral notes. Aged in large neutral oak, it gains extraordinary mineral depth and longevity. Benchmark Austrian Riesling.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_brundl, "Freshwater crayfish with fennel fronds and dill butter", "complement", "classic", "starter", "Mineral Riesling and freshwater shellfish are a natural pairing in the Danube wine regions. The wine's volcanic tension and citrus precision elevate delicate crayfish.")
    PAIR(prod_brundl, "Roasted veal sweetbreads with lemon zest and capers", "complement", "established", "main", "The wine's mineral acidity cuts through the richness of sweetbreads. Lemon and caper echo its citrus and saline notes, producing a classical Austrian match.")
    PAIR(prod_brundl, "White asparagus with Hollandaise and chives", "complement", "classic", "starter", "White asparagus season in Austria is Heiligenstein season. The wine's green notes, pepper spice, and acidity are perfect foils for asparagus and egg-based sauce.")
    PAIR(prod_brundl, "Bergkäse with Alpine honey", "bridge", "suggested", "cheese", "Alpine cheese with honey echoes the wine's mountain-influenced mineral character and stone fruit complexity.")

p_gobelsburg = P(
    name="Schloss Gobelsburg",
    country="Austria",
    region_id=r_kamptal,
    producer_type="winery",
    description="One of Austria's oldest estates, now under the direction of Michael Moosbrugger in partnership with Willi Bründlmayer. The historic castle winery produces benchmark Kamptal Grüner Veltliner with a focus on the Lamm — a limestone and loess-rich Erste Lage producing wines of remarkable weight, spice, and longevity. Gobelsburg's wines are known for their traditional style and exceptional cellaring potential."
)
prod_gobel, new = PROD(
    name="Schloss Gobelsburg Langenlois Lamm Grüner Veltliner",
    category="wine_still",
    subcategory="Grüner Veltliner",
    producer_id=p_gobelsburg,
    region_id=r_kamptal,
    origin_country="Austria",
    description="From the Lamm — one of Kamptal's greatest Erste Lagen — this Grüner Veltliner is a wine of power, complexity, and extraordinary longevity. The signature white pepper and stone fruit are present, but layered over a deep mineral-limestone foundation. Fermented and aged in large traditional oak, it shows remarkable integration of fruit, spice, and terroir expression. Among Austria's most age-worthy dry whites.",
    price_tier="premium"
)
if new:
    PAIR(prod_gobel, "Schnitzel with potato-cucumber salad and lingonberry", "complement", "classic", "main", "The quintessential Austrian pairing — Grüner Veltliner with Wiener Schnitzel. The wine's acidity refreshes through breading, white pepper bridges to the potato salad's dressing, and lingonberry echoes the wine's fruit notes.")
    PAIR(prod_gobel, "Grilled pike-perch with roasted garlic and herb oil", "complement", "established", "main", "Danube river fish with Kamptal white — a regional pairing of natural logic. The wine's mineral weight and spice complement the delicate flesh without overwhelming it.")
    PAIR(prod_gobel, "White truffle risotto with aged Parmigiano", "elevate", "adventurous", "main", "White pepper and mineral depth of Grüner Veltliner bridge beautifully to white truffle. The wine's weight can sustain the richness of the dish.")
    PAIR(prod_gobel, "Spring pea soup with smoked cream and radish", "complement", "established", "starter", "Green vegetable notes in Grüner Veltliner mirror the freshness of spring peas. Smoked cream bridges to the wine's rounder, barrel-aged character.")

# === BIERZO DO (Spain) ===
print("\n=== Bierzo DO (Spain) ===")
r_bierzo = R(
    name="Bierzo",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Bierzo DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="A dramatic, mountainous DO in northwest Spain's León province where Mencía grown on ancient slate and schist soils produces wines of unique character — somewhere between the elegance of Pinot Noir and the structure of Syrah, yet entirely itself. The region's steep, terraced vineyards and extreme altitudes (400–900m) produce wines with freshness, floral aromatics, and earthy depth unlike anything else in Spain. Producers like Descendientes de J. Palacios have brought Bierzo to global attention.",
    key_producers="Descendientes de J. Palacios, Bodegas y Viñedos Luna Beberide, Dominio de Tares, Pittacum",
    historical_context="Bierzo was a Roman wine region, and some ancient vine parcels are believed to be over 100 years old on their original rootstock. The DO was founded in 1989, but the modern era began with Álvaro Palacios and his nephew Ricardo Pérez Palacios arriving in 1999, elevating the region to international recognition."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, fresh vintage producing elegant, aromatic Mencías with excellent energy and aging potential."),
    (2020, "exceptional", "rising", "Outstanding year across all quality levels. Single-vineyard wines of great concentration and finesse."),
    (2019, "excellent", "stable", "Long, warm autumn allowed perfect ripening. Rich yet fresh wines with beautiful blue fruit and floral notes."),
    (2018, "very_good", "stable", "Warm year with some heat stress mitigated by altitude and Atlantic influence."),
    (2017, "excellent", "stable", "Late spring frosts reduced yields, intensifying concentration in survivors. Exceptional single-vineyard wines."),
]:
    VIN(r_bierzo, yr, qd, pt, sn)

p_palacios_d = P(
    name="Descendientes de J. Palacios",
    country="Spain",
    region_id=r_bierzo,
    producer_type="winery",
    description="The estate that transformed Bierzo. Álvaro Palacios — already famous for Priorat — arrived in Bierzo in 1999 with nephew Ricardo Pérez Palacios, identifying pre-phylloxera Mencía vineyards on slate terraces. Their hierarchical range — from village wines to single-vineyard parcels — demonstrated that Bierzo could produce wines of Burgundy-like complexity. Moncerbal, Las Lamas, and La Faraona are now among Spain's most sought-after wines."
)
prod_corullon, new = PROD(
    name="Descendientes de J. Palacios Pétalos del Bierzo",
    category="wine_still",
    subcategory="Mencía",
    producer_id=p_palacios_d,
    region_id=r_bierzo,
    origin_country="Spain",
    description="The benchmark entry-level wine from Bierzo's most important estate — blended from old Mencía vines across multiple village sites. Vibrant ruby with aromas of crushed violets, blueberry, graphite, and slate. The palate is lively and light-textured with silky tannins, fresh acidity, and an earthy finish that speaks unmistakably of its mountain terroir. One of Spain's great value fine wines.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_corullon, "Roasted lamb chops with rosemary and garlic", "complement", "classic", "main", "The floral, earthy Mencía is a natural match for mountain lamb. Rosemary and garlic echo the wine's herbal and spice notes, while the light tannins support without dominating.")
    PAIR(prod_corullon, "Slow-braised octopus with smoked paprika and potato", "complement", "established", "main", "Galician-influenced octopus is a natural pairing for Bierzo wines — the wine's acidity cuts through the octopus's richness and smoked paprika bridges to its earthy depth.")
    PAIR(prod_corullon, "Cecina de León with aged Manchego and quince", "complement", "classic", "starter", "Cured beef from León is a regional pairing. The wine's fresh acidity and red fruit complement the cured meat's salt and fat while quince adds sweetness.")
    PAIR(prod_corullon, "Mushroom and lentil stew with smoked pork rib", "bridge", "suggested", "main", "Earthy mushroom and lentil echo the wine's terroir-driven depth. Smoked pork bridges to its subtle fruit character.")

p_luna = P(
    name="Bodegas y Viñedos Luna Beberide",
    country="Spain",
    region_id=r_bierzo,
    producer_type="winery",
    description="One of Bierzo's pioneering quality estates, producing Mencía from high-altitude vineyards in the Ancares foothills. Founded by Javier Martínez, Luna Beberide introduced French oak maturation to Bierzo and was among the first to demonstrate the grape's fine wine potential. Their single-vineyard Mencía wines show the region's capacity for structured, age-worthy reds."
)
prod_luna, new = PROD(
    name="Luna Beberide Mencía Bierzo Finca La Cuesta",
    category="wine_still",
    subcategory="Mencía",
    producer_id=p_luna,
    region_id=r_bierzo,
    origin_country="Spain",
    description="A single-vineyard Mencía from high-altitude slate soils at Finca La Cuesta in the Ancares foothills. The wine shows more structure and concentration than many Bierzo reds, with dark cherry, blackberry, violet, and iron-inflected mineral notes. Fermented in French oak with extended maceration producing silky yet firm tannins. A benchmark for age-worthy Bierzo.",
    price_tier="premium"
)
if new:
    PAIR(prod_luna, "Grilled Iberian pork secreto with charred calçots", "complement", "established", "main", "The wine's structure and dark fruit support the richness of Iberian pork. Charred calçot sweetness echoes the wine's fruit character while adding smoky complexity.")
    PAIR(prod_luna, "Roasted suckling pig with apple and sage", "complement", "classic", "main", "Mencía's earthy tannins and fresh acidity are ideal for suckling pig. Apple mirrors its fruit, sage echoes its herbal notes.")
    PAIR(prod_luna, "Wild boar stew with chestnuts and juniper", "complement", "adventurous", "main", "Mountain game from the same altitude as the vineyard — chestnut echoes the wine's earthy depth, juniper mirrors its mineral character.")
    PAIR(prod_luna, "Aged Idiazabal sheep's cheese with honey", "bridge", "suggested", "cheese", "The wine's slate minerality and dark fruit bridge to smoky sheep's milk cheese. Honey softens the tannins.")

# === BEKAA VALLEY (Lebanon) ===
print("\n=== Bekaa Valley (Lebanon) ===")
r_bekaa = R(
    name="Bekaa Valley",
    country="Lebanon",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Bekaa Valley",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Lebanon's premier wine region, a high-altitude valley (900-1000m) between the Lebanon and Anti-Lebanon mountain ranges producing wines of surprising quality and character. The continental climate — hot, dry summers and cold winters with reliable snowpack — combined with well-drained limestone soils produces wines of great concentration and freshness. Châteaux Musar, Ksara, and Kefraya have established Lebanon as one of the Middle East's most credible fine wine regions.",
    key_producers="Château Musar, Château Ksara, Château Kefraya, Massaya, Clos St. Thomas",
    historical_context="Wine has been produced in the Bekaa Valley since Phoenician times — the Romans built a great temple to Bacchus at Baalbek, still standing today. Modern Lebanese wine was essentially created by Gaston Hochar at Château Musar, who began selling internationally in the 1960s and continued producing through the Lebanese Civil War, gaining worldwide recognition."
)
for yr, qd, pt, sn in [
    (2020, "excellent", "rising", "Hot, dry vintage producing concentrated, structured wines. Château Musar and Kefraya released exceptional reds."),
    (2019, "very_good", "stable", "Balanced year with good natural acidity. Whites and rosés particularly fresh."),
    (2018, "excellent", "stable", "Long, warm growing season with cool nights preserving aromatic complexity."),
    (2017, "very_good", "stable", "Reliable vintage across the valley. Traditional varieties performed well."),
    (2016, "exceptional", "rising", "One of the great Bekaa vintages — concentrated reds with exceptional freshness and aging potential."),
]:
    VIN(r_bekaa, yr, qd, pt, sn)

p_musar = P(
    name="Château Musar",
    country="Lebanon",
    region_id=r_bekaa,
    producer_type="winery",
    description="Lebanon's most iconic wine estate and one of the world's most unique producers. Gaston Hochar founded the modern estate in 1930, and his son Serge — who passed in 2014 — became a legendary figure in world wine, producing through the Lebanese Civil War and creating wines of extraordinary idiosyncrasy. The Musar red blends Cabernet Sauvignon, Cinsault, and Carignan fermented in traditional cement vats and aged for over three years before release. These are wines that age for decades and challenge all conventional expectations."
)
prod_musar_red, new = PROD(
    name="Château Musar Red Bekaa Valley",
    category="wine_still",
    subcategory="Red Blend",
    producer_id=p_musar,
    region_id=r_bekaa,
    origin_country="Lebanon",
    description="One of the wine world's most distinctive and celebrated bottles. A blend of Cabernet Sauvignon, Cinsault, and Carignan from ancient vineyards, fermented in cement and aged three years in French oak before release, then held further in bottle. The result is deliberately oxidative, complex, and unlike anything else — aromas of dried rose, leather, orange peel, dark cherry, tobacco, and spice. Wines from great years (1970, 1972, 2016) can age 50+ years.",
    price_tier="premium"
)
if new:
    PAIR(prod_musar_red, "Slow-roasted lamb shoulder with za'atar, sumac, and flatbread", "complement", "classic", "main", "The quintessential Lebanese pairing — regional lamb with Château Musar. Za'atar and sumac echo the wine's dried herb and spice complexity, while the lamb's richness is matched by the wine's substantial tannins and depth.")
    PAIR(prod_musar_red, "Duck confit with pomegranate molasses and walnut", "complement", "established", "main", "The wine's oxidative notes and dried fruit character pair beautifully with duck. Pomegranate echoes its tart edge while walnut mirrors its earthy depth.")
    PAIR(prod_musar_red, "Kibbeh nayyeh with mint, lemon, and pine nuts", "complement", "adventurous", "starter", "Raw seasoned lamb is a natural Lebanese pairing for Musar. The wine's complexity and age elevate the delicate raw meat, while lemon and mint provide freshness.")
    PAIR(prod_musar_red, "Aged goat's cheese with dried apricot and pistachios", "bridge", "suggested", "cheese", "The wine's dried fruit character bridges to aged goat cheese. Pistachios echo its earthy depth and apricot mirrors its oxidative fruit notes.")

p_kefraya = P(
    name="Château Kefraya",
    country="Lebanon",
    region_id=r_bekaa,
    producer_type="winery",
    description="One of the Bekaa's largest and most successful estates, founded in 1946 by Michel de Bustros and expanded dramatically in the 1970s. Kefraya's diverse range covers everything from entry-level blends to their prestige Comte de M — a barrel-aged Cabernet-dominant blend considered one of Lebanon's finest wines. The estate is known for reliability across styles and a more international, structured approach compared to Château Musar's idiosyncratic character."
)
prod_kefraya, new = PROD(
    name="Château Kefraya Comte de M Bekaa Valley",
    category="wine_still",
    subcategory="Cabernet Sauvignon Blend",
    producer_id=p_kefraya,
    region_id=r_bekaa,
    origin_country="Lebanon",
    description="The prestige cuvée of Château Kefraya — a Cabernet Sauvignon-dominated blend aged in French barriques. More structured and internationally polished than Château Musar, with dark cherry, blackcurrant, cedar, and cigar box aromas. Full-bodied with fine-grained tannins and a long, mineral finish. One of Lebanon's most age-worthy and internationally approachable wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_kefraya, "Rack of lamb with herb crust and red wine reduction", "complement", "classic", "main", "Cabernet Sauvignon's affinity for lamb extends perfectly to Lebanese terroir. The wine's structure and dark fruit complement roasted lamb, while cedar notes echo the herb crust.")
    PAIR(prod_kefraya, "Grilled kafta with tahini and herb salad", "complement", "established", "main", "Lebanese spiced ground lamb with tahini is a natural regional pairing. The wine's structure supports the richness while its fruit complements the meat's spicing.")
    PAIR(prod_kefraya, "Warak enab (stuffed vine leaves) with yogurt and mint", "contrast", "adventurous", "starter", "The wine's tannic structure contrasts with the acidity of stuffed vine leaves. Yogurt moderates the tannins while mint provides aromatic freshness.")
    PAIR(prod_kefraya, "Dark chocolate tart with preserved orange and coffee cream", "complement", "suggested", "dessert", "The wine's dark fruit and cedar bridge to bitter chocolate. Preserved orange mirrors its dried fruit complexity.")

# === FINGER LAKES AVA (USA) ===
print("\n=== Finger Lakes AVA (USA) ===")
r_fl = R(
    name="Finger Lakes",
    country="USA",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Finger Lakes AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="New York's premier wine region, centred on a series of glacially carved lakes in upstate New York that moderate the harsh continental climate and provide unique growing conditions for cool-climate varieties. Seneca Lake (the deepest and warmest) and Cayuga Lake host the finest wineries. Riesling is the undisputed star — the region produces some of North America's greatest examples — though Cabernet Franc, Pinot Noir, and native-hybrid varieties also excel. A region of growing international significance.",
    key_producers="Dr. Konstantin Frank, Red Newt Cellars, Hermann J. Wiemer, Bloomer Creek, Forge Cellars",
    historical_context="Dr. Konstantin Frank, a Ukrainian immigrant viticulturist, proved in the 1950s that vinifera varieties could thrive in the Finger Lakes, overturning conventional wisdom that the climate was too harsh. His work at Hammondsport transformed the region. The modern fine wine era began in earnest in the 1980s and accelerated dramatically from the 2000s onward."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Warm, dry summer produced ripe, complex Rieslings and reds of unusual concentration."),
    (2020, "very_good", "stable", "Challenging early season with excellent late summer. Dry Rieslings showed particular purity."),
    (2019, "excellent", "stable", "Classic Finger Lakes vintage — cool, long ripening season producing Rieslings of extraordinary minerality."),
    (2018, "very_good", "stable", "Warm summer, long autumn. Rich, approachable wines across all categories."),
    (2017, "excellent", "rising", "Cool, long season producing elegant, age-worthy Rieslings and impressive Cab Franc."),
]:
    VIN(r_fl, yr, qd, pt, sn)

p_wiemer = P(
    name="Hermann J. Wiemer",
    country="USA",
    region_id=r_fl,
    producer_type="winery",
    description="One of the Finger Lakes' founding fine wine estates, established in 1979 by Hermann Wiemer — a German-trained winemaker who recognised the region's Riesling potential. The estate on Seneca Lake's western shore produces benchmark Rieslings from estate vineyards, including the HJW Vineyard and Josef Vineyard designated wines. Now continued by Fred Merwarth and Oskar Bynke, Wiemer remains the reference point for Finger Lakes Riesling at all quality levels."
)
prod_wiemer, new = PROD(
    name="Hermann J. Wiemer Seneca Lake Dry Riesling",
    category="wine_still",
    subcategory="Riesling",
    producer_id=p_wiemer,
    region_id=r_fl,
    origin_country="USA",
    description="The benchmark Finger Lakes dry Riesling — estate grown on Seneca Lake's shale and limestone-influenced soils. Steel-fermented for maximum freshness, it shows green apple, lemon zest, white peach, crushed slate, and a distinctive austerity that separates Finger Lakes Riesling from German and Alsatian counterparts. With age, develops petrol and toast complexity. One of North America's finest dry whites at any price.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_wiemer, "Pan-seared trout with capers, lemon, and brown butter", "complement", "classic", "main", "Freshwater trout from the Finger Lakes region is a natural pairing. The wine's citrus acidity, mineral shale notes, and freshness mirror the fish's delicacy and the brightness of lemon and caper.")
    PAIR(prod_wiemer, "Pork dumplings with ginger-soy dipping sauce", "contrast", "established", "starter", "Dry Riesling's acidity and mineral freshness contrast beautifully with rich pork dumplings. Ginger bridges to the wine's spice notes while soy's umami is lifted by the wine's bright acidity.")
    PAIR(prod_wiemer, "Chilled lobster salad with tarragon aioli", "complement", "established", "starter", "The wine's limestone minerality and citrus notes are ideal for lobster. Tarragon bridges to its herbal undertones while the richness of aioli is cut by its acidity.")
    PAIR(prod_wiemer, "New York State Cheddar with apple chutney", "complement", "suggested", "cheese", "Local terroir pairing — upstate New York cheddar with Seneca Lake Riesling. Apple chutney echoes the wine's fruit while cheddar's sharpness complements its mineral edge.")

p_frank = P(
    name="Dr. Konstantin Frank",
    country="USA",
    region_id=r_fl,
    producer_type="winery",
    description="The founding estate of Finger Lakes fine wine, established in 1962 by the Ukrainian viticulturist who proved vinifera varieties could thrive in the Finger Lakes. Now in its third generation under Meaghan Frank, the estate crafts an extensive range from its Keuka Lake vineyards, with the Rkatsiteli — an ancient Georgian variety — and the single-vineyard Magdalena Vineyard Riesling among the most distinctive offerings. Dr. Frank's success inspired a generation of Finger Lakes winemakers."
)
prod_frank, new = PROD(
    name="Dr. Konstantin Frank Keuka Lake Grüner Veltliner",
    category="wine_still",
    subcategory="Grüner Veltliner",
    producer_id=p_frank,
    region_id=r_fl,
    origin_country="USA",
    description="A rare example of Grüner Veltliner grown outside Austria, produced by one of the pioneers who proved vinifera could flourish in New York State. Estate grown on Keuka Lake's steep, shale-rich soils. The wine shows the variety's classic white pepper, citrus, and green herb character with a distinctly American expression — slightly rounder than its Austrian counterparts with good mineral tension. A testament to the Finger Lakes' versatility beyond Riesling.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_frank, "Grilled asparagus with lemon ricotta and pine nuts", "complement", "classic", "starter", "Grüner Veltliner is asparagus's most famous wine companion. The wine's white pepper and green herb notes mirror asparagus exactly, while ricotta rounds the pairing.")
    PAIR(prod_frank, "Pan-seared walleye with herb butter and roasted corn", "complement", "established", "main", "Great Lakes fish with regional Grüner — the wine's freshness and mineral quality are ideal for delicate freshwater fish. Corn echoes its softer fruit notes.")
    PAIR(prod_frank, "Charcuterie board with cornichons and Dijon mustard", "complement", "suggested", "starter", "The wine's pepper spice and fresh acidity cut through cured meats perfectly. Cornichons and mustard echo its sharp, herbal character.")
    PAIR(prod_frank, "Roasted chicken with tarragon cream and fingerling potatoes", "complement", "established", "main", "Classic white wine and chicken, elevated by tarragon that bridges to Grüner's herbal notes. The wine's weight suits the cream sauce without overwhelming it.")

# Final counts
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
print("\nDone.")
cur.close()
conn.close()
