#!/usr/bin/env python3
"""T23 Batch 16 — New wine regions: Bierzo DO (Spain), Grampians GI (Australia), Santorini PDO (Greece), Bekaa Valley (Lebanon), Colchagua Valley DO (Chile)"""

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

# ── BIERZO DO (SPAIN) ─────────────────────────────────────────────
print("\n=== Bierzo DO (Spain) ===")
r_bie = R("Bierzo", "Spain", "wine",
           designation_type="DO",
           designation_name="Bierzo DO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Spain's most distinctive emerging appellation in the Castilla y León mountains of northwestern Galicia, producing Mencía — an aromatic, mineral red variety unique to this slate and quartzite terrain — of striking transparency and complexity. Often called 'the Pinot Noir of Spain', Mencía's light color, bright acidity, and mineral character bears little resemblance to Spain's more powerful reds. The region's ancient Roman mining landscape and extreme Atlantic-continental climate create wines of haunting individuality.",
           key_producers="Descendientes de J. Palacios, Pittacum, Dominio de Tares, Bodegas Estefanía, Telmo Rodriguez",
           historical_context="Bierzo was historically associated with the pilgrimage route to Santiago de Compostela. The Romans mined gold here (Las Médulas UNESCO site) and planted vines alongside. The modern wine revolution came in 1999 when Álvaro Palacios's nephew Ricardo Pérez Palacios established Descendientes de J. Palacios, bringing Bierzo to international attention and demonstrating Mencía's world-class potential from ancient slate terraces.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Bierzo vintage; Mencía from ancient slate terraces showed extraordinary mineral transparency and dark cherry intensity."),
    (2021, "very_good", "stable", "Elegant vintage; Atlantic influence produced wines of exceptional freshness and the characteristic Bierzo mineral linearity."),
    (2020, "excellent", "stable", "Benchmark year; Pétalos del Bierzo and La Faraona produced internationally acclaimed old-vine Mencía of great depth."),
    (2019, "exceptional", "rising", "Greatest Bierzo vintage of the modern era; La Faraona achieved legendary critical scores; Mencía showed its full potential."),
    (2018, "excellent", "stable", "Excellent vintage; ancient terraced vineyard Mencía showed extraordinary mineral precision from the slate and quartzite."),
]:
    VIN(r_bie, yr, qd, pt, sn)

p_dpj = P("Descendientes de J. Palacios", "Spain", r_bie,
           description="Ricardo Pérez Palacios and his uncle Álvaro's Bierzo estate that launched the region's international reputation from 1999. Pétalos del Bierzo is the accessible entry and one of Spain's most consistent value wines; La Faraona from ancient terraced slate is Spain's most expensive and rarified Mencía — placed among the world's great red wines.")
prod_dpj, new = PROD("Descendientes de J. Palacios Pétalos del Bierzo", "wine_still", p_dpj, r_bie, "Spain",
                     subcategory="Mencia",
                     description="Spain's most celebrated and accessible Mencía — translucent ruby, wild cherry, floral violet, mineral slate, and the freshness that makes Mencía unlike any other Spanish red. Light-bodied yet complex, this is one of Spain's finest value wines and the gateway to Bierzo's remarkable potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_dpj, "Pulpo a la gallega (Galician octopus) with smoked paprika, olive oil, and potato", "complement", "classic", "main", "Galicia's most famous dish and the region's signature red — Mencía's mineral acidity cuts through the octopus's texture; paprika bridges the wine's earthy character; a cross-regional northwestern Spain pairing")
    PAIR(prod_dpj, "Empanada Gallega (tuna and pepper pie) with salsa verde", "complement", "established", "main", "The Galician savory pastry and Bierzo Mencía — the wine's mineral freshness and cherry notes complement the tuna filling; salsa verde bridges the herb character")

p_bit = P("Pittacum", "Spain", r_bie,
           description="The Bierzo cooperative estate producing Mencía from ancient, ungrafted terraced vines that survived Phylloxera due to the region's slate soils. Aurea and Petit Aurea represent some of Bierzo's finest old-vine expressions from the highest altitude vineyards.")
prod_bit, new = PROD("Pittacum Aurea Mencia", "wine_still", p_bit, r_bie, "Spain",
                     subcategory="Mencia",
                     description="Old-vine, ungrafted Mencía from ancient Bierzo slate terraces at altitude — more concentrated and structured than Pétalos, with deep cherry, dried flowers, iron minerality, and the characteristic Mencía freshness. One of Bierzo's finest single-parcel expressions from centenarian vines.",
                     price_tier="premium")
if new:
    PAIR(prod_bit, "Cocido maragato (chickpea, pork, and chorizo stew served in reverse order)", "complement", "classic", "main", "Bierzo's regional stew tradition — the Mencía's mineral freshness cuts through the rich pork and chickpea broth; chorizo's paprika bridges the wine's earthy character")
    PAIR(prod_bit, "Slow-roasted Ibérico pork jowl with black garlic and roasted root vegetables", "complement", "established", "main", "Ibérico pork's rich marbling and Bierzo Mencía's mineral structure — the wine's acidity and cherry character handles the fat; black garlic's umami depth bridges")

# ── GRAMPIANS GI (AUSTRALIA) ─────────────────────────────────────
print("\n=== Grampians GI (Australia) ===")
r_grp = R("Grampians", "Australia", "wine",
           designation_type="GI",
           designation_name="Grampians GI",
           reputation_tier="respected",
           quality_trajectory="established",
           description="Victoria's historic wine region in the Grampians mountain range at 300-500m altitude, producing Australia's oldest and most distinctive Shiraz from ancient soils of red volcanic basalt, sandy loam, and limestone. The Grampians — particularly the Great Western sub-region — has produced sparkling wine since 1865 and some of Australia's most age-worthy Shiraz from old, dry-farmed vines. Best's Great Western and Mount Langi Ghiran are the region's benchmark producers.",
           key_producers="Best's Great Western, Mount Langi Ghiran, Seppelt Great Western, Clayfield Wines",
           historical_context="The Great Western cellars at Seppelt were hand-carved by Chinese goldminers during the 1860s gold rush — the 'Drives' stretch for 3km underground and now store vintage sparkling wines. Best's Thomson Family Shiraz comes from ungrafted vines planted by Joseph Best in 1868 — among Australia's oldest continuous plantings. The region produced many of Australia's finest bottles of sparkling wine, known as 'Great Western Champagne', throughout the early 20th century.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Grampians vintage; Shiraz from ancient volcanic basalt showed extraordinary peppery complexity and mineral freshness."),
    (2021, "very_good", "stable", "Classic cool-altitude vintage; Best's Thomson Family Shiraz from ungrafted vines showed haunting mineral transparency."),
    (2020, "excellent", "stable", "Benchmark year; Mount Langi Ghiran and Best's produced Shiraz of exceptional elegance and white pepper intensity."),
    (2019, "excellent", "rising", "Outstanding vintage; the Grampians' cool altitude produced Shiraz of Rhône-like elegance with Australian dark fruit depth."),
    (2018, "very_good", "stable", "Solid vintage; old-vine Shiraz from ancient volcanic soils showed excellent mineral character and aging potential."),
]:
    VIN(r_grp, yr, qd, pt, sn)

p_bes = P("Best's Great Western", "Australia", r_grp,
           description="The Thomson family's historic Grampians estate, continuously farmed since 1866, producing Thomson Family Shiraz from 154-year-old ungrafted vines — one of Australia's most extraordinary wine treasures. Best's Great Western Shiraz is considered among Australia's most age-worthy red wines, developing in bottle for 30+ years.")
prod_bes, new = PROD("Best's Great Western Thomson Family Shiraz", "wine_still", p_bes, r_grp, "Australia",
                     subcategory="Shiraz",
                     description="One of Australia's most historically significant wines — Shiraz from ungrafted vines planted by Joseph Best in 1868 on volcanic basalt at Great Western. Extraordinary white pepper, dark plum, iron, and the distinctive cool-climate Grampians mineral freshness. Requires 15-20 years of aging to reveal its full complexity.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_bes, "Roasted Victorian lamb shoulder with rosemary, anchovy, and garlic butter", "complement", "classic", "main", "Australia's most historic Shiraz and its most celebrated pastoral protein — the wine's white pepper and iron character mirrors the roasted lamb's mineral depth; rosemary bridges the wine's herb complexity")
    PAIR(prod_bes, "Aged hard cheese (12-month Montgomery's Cheddar) with quince paste and walnuts", "complement", "established", "cheese", "Old-vine Shiraz's complexity and longevity demands an equally complex cheese; the wine's white pepper and iron find resonance in the aged cheddar's crystal and depth")

p_mla = P("Mount Langi Ghiran", "Australia", r_grp,
           description="The Langi estate's Grampians winery producing Australia's most celebrated and consistently acclaimed peppery cool-climate Shiraz. Langi Shiraz — with its signature intense white pepper character from the volcanic highland terroir — has been one of Australia's most internationally awarded wines for decades.")
prod_mla, new = PROD("Mount Langi Ghiran Langi Shiraz", "wine_still", p_mla, r_grp, "Australia",
                     subcategory="Shiraz",
                     description="Australia's most celebrated peppery cool-climate Shiraz — the Grampians volcanic basalt and altitude produce a wine completely unlike Barossa or McLaren Vale. Intense white and black pepper, dark plum, violets, olive, and iron minerality with a long, fresh finish. Rhône-like in style, uniquely Australian in character.",
                     price_tier="premium")
if new:
    PAIR(prod_mla, "Duck breast with green peppercorn sauce, braised red cabbage, and potato rösti", "complement", "classic", "main", "The wine's signature pepper character finds direct resonance in the peppercorn sauce; duck fat is structured by the Shiraz's tannins; red cabbage bridges the wine's fruit")
    PAIR(prod_mla, "Grilled kangaroo fillet with bush tomato chutney and warrigal greens", "complement", "established", "main", "Australia's most distinctive protein and its most distinctive Shiraz — kangaroo's leanness needs the wine's structure; bush tomato's earthiness mirrors the volcanic mineral character")

# ── SANTORINI PDO (GREECE) ────────────────────────────────────────
print("\n=== Santorini PDO (Greece) ===")
r_sant = R("Santorini", "Greece", "wine",
            designation_type="PDO",
            designation_name="Santorini PDO",
            reputation_tier="prestigious",
            quality_trajectory="ascending",
            description="Greece's most volcanic and internationally recognized wine island in the Aegean, producing Assyrtiko of extraordinary mineral intensity from ancient, basket-trained vines (koulouri) on volcanic pumice and lava soils. The island's extreme conditions — 300+ days of sunshine, howling Meltemi winds, no phylloxera, no rain — require vines to be trained into ground-level baskets to protect the grapes. Assyrtiko's piercing acidity, citrus intensity, and volcanic mineral character is unlike any other white wine on earth.",
            key_producers="Domaine Sigalas, Santo Wines, Gaia Estate, Hatzidakis, Argyros Estate",
            historical_context="Santorini's winemaking tradition dates to the Minoan civilization — archaeological evidence of wine production on the island predates 1600 BCE. The island's unique kopylouri (basket) training system was developed to cope with the Meltemi winds that would destroy upright vines. Phylloxera never reached Santorini because the volcanic pumice soil cannot support the louse. Some vines are estimated to be 200+ years old, making Santorini home to among the world's oldest cultivated vines.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Santorini vintage; Assyrtiko from ancient volcanic pumice soils showed extraordinary citrus intensity and mineral precision."),
    (2021, "very_good", "stable", "Classic Aegean vintage; basket-vine Assyrtiko produced wines of haunting salinity and mineral freshness."),
    (2020, "excellent", "stable", "Benchmark year; Sigalas and Argyros produced internationally acclaimed barrel-fermented Assyrtiko and Nykteri."),
    (2019, "exceptional", "rising", "Greatest Santorini vintage in the modern era; Assyrtiko of legendary volcanic mineral intensity and aging potential."),
    (2018, "excellent", "stable", "Excellent vintage; the ancient vines' concentration produced Nykteri wines of extraordinary oxidative complexity."),
]:
    VIN(r_sant, yr, qd, pt, sn)

p_sig = P("Domaine Sigalas", "Greece", r_sant,
           description="Paris Sigalas's Santorini estate is considered the appellation's most internationally acclaimed producer, crafting Assyrtiko of extraordinary purity and barrel-fermented Assyrtiko of Burgundian complexity from ancient volcanic vines. Sigalas was a mathematics professor before founding the estate; his analytical precision informs the wine's clarity.")
prod_sig, new = PROD("Sigalas Assyrtiko Santorini", "wine_still", p_sig, r_sant, "Greece",
                     subcategory="Assyrtiko",
                     description="The benchmark Santorini Assyrtiko — ancient basket vines on volcanic pumice producing a wine of extraordinary citrus intensity, saline mineral precision, and volcanic mineral depth. Lemon zest, grapefruit, sea spray, flint, and a searing acidity that makes this one of the Mediterranean's greatest white wines.",
                     price_tier="premium")
if new:
    PAIR(prod_sig, "Grilled octopus with fava (Santorini yellow split pea purée) and capers", "complement", "classic", "main", "The island's most famous dish and its most celebrated wine — Santorini's volcanic terroir in both the wine and the fava peas; the Assyrtiko's acidity is perfect for octopus")
    PAIR(prod_sig, "Fried whitebait with tzatziki and lemon on flatbread", "complement", "classic", "aperitif", "Aegean island fish and island wine — the wine's citrus and saline character mirrors the sea; acidity cuts through the frying; tzatziki's yogurt bridges")

p_arg = P("Argyros Estate", "Greece", r_sant,
           description="Matthew Argyros's historic Santorini estate farming ancient basket-trained vines of up to 200 years of age, producing the island's most structured and age-worthy Assyrtiko alongside Nykteri (the traditional Santorini white aged in barrel). Argyros Cuvée Monsignori is one of Greece's most critically acclaimed white wines.")
prod_arg, new = PROD("Argyros Cuvée Monsignori Assyrtiko", "wine_still", p_arg, r_sant, "Greece",
                     subcategory="Assyrtiko",
                     description="Santorini's most celebrated single-vineyard Assyrtiko from ancient 200-year-old basket vines on volcanic pumice — barrel-fermented and aged, creating a wine of extraordinary complexity. Volcanic smoke, lemon curd, struck flint, sea air, and the mineral persistence that only comes from centuries-old vines on pure volcanic soil.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_arg, "Lobster thermidor with brandy cream, Gruyère, and tarragon", "complement", "classic", "main", "The wine's barrel complexity and volcanic mineral intensity handles luxury shellfish with ease; the cream is structured by Assyrtiko's piercing acidity; tarragon bridges the herbal notes")
    PAIR(prod_arg, "Grilled fresh tuna with capers, tomato, and anchovy butter sauce", "complement", "established", "main", "Mediterranean tuna and volcanic Santorini Assyrtiko — the wine's saline and mineral character mirrors the anchovy's intensity; tomato's acidity echoes the wine's lemon character")

# ── BEKAA VALLEY (LEBANON) ────────────────────────────────────────
print("\n=== Bekaa Valley (Lebanon) ===")
r_bek = R("Bekaa Valley", "Lebanon", "wine",
           designation_type="GI",
           designation_name="Bekaa Valley GI",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Lebanon's primary wine-producing region in the high-altitude valley (900-1100m) between the Lebanon and Anti-Lebanon mountain ranges, producing wines from international varieties — Cabernet Sauvignon, Syrah, Cinsault, and Merwah — that have been cultivated here for millennia. The region's extreme continental climate, ancient limestone soils, and high altitude create wines of remarkable structure and longevity despite the challenging political context. Château Musar is Lebanon's most celebrated and internationally known wine.",
           key_producers="Château Musar, Château Ksara, Château Kefraya, Domaine des Tourelles, Clos St. Thomas",
           historical_context="The Bekaa Valley's winemaking tradition dates to the Phoenicians — the Bible records the wines of Lebanon. Under Ottoman rule and French Mandate, the Jesuit fathers at Ksara established modern winemaking in the 1850s. Gaston Hochar founded Château Musar in 1930; his son Serge's wines gained international fame when Michael Broadbent selected the 1967 Musar at the 1979 Bristol Wine Fair as one of the world's most remarkable wines. Musar continued producing even during Lebanon's civil war.")

for yr, qd, pt, sn in [
    (2022, "excellent", "stable", "Outstanding Bekaa vintage in a year of relative stability; Cabernet Sauvignon and Cinsault blend produced wines of extraordinary complexity."),
    (2021, "very_good", "stable", "Solid vintage; the high-altitude vineyards' limestone soils produced wines of good structure despite challenging harvest conditions."),
    (2020, "very_good", "stable", "Good vintage; produced under extremely difficult circumstances following the Beirut explosion; wines showed remarkable resilience."),
    (2019, "excellent", "rising", "Outstanding vintage; Château Musar and Ksara produced their finest wines of the decade from the ancient Bekaa limestone."),
    (2018, "excellent", "stable", "Benchmark year; the combination of high altitude and cool nights produced wines of extraordinary freshness for the Middle East."),
]:
    VIN(r_bek, yr, qd, pt, sn)

p_mus = P("Château Musar", "Lebanon", r_bek,
           description="The Hochar family's legendary Ghazir estate and Bekaa Valley vineyards, producing Lebanon's most internationally celebrated and collected wine since 1930. Serge Hochar's Château Musar Rouge — a Cabernet Sauvignon, Cinsault, and Carignan blend fermented by each variety separately and aged for seven years before release — is one of the world's most eccentric, age-worthy, and deeply individual red wines.")
prod_mus, new = PROD("Château Musar Rouge", "wine_still", p_mus, r_bek, "Lebanon",
                     subcategory="Cabernet Sauvignon Blend",
                     description="Lebanon's most celebrated and controversial wine — released only after seven years of aging. A Cabernet Sauvignon, Cinsault, and Carignan blend from ancient Bekaa vines producing a wine unlike anything else on earth: dried fruits, tobacco, leather, cedar, Mediterranean herbs, and an oxidative complexity that polarizes and captivates. Best with 20-30 years of bottle age.",
                     price_tier="premium")
if new:
    PAIR(prod_mus, "Roasted leg of lamb with seven spices (baharat), pine nuts, and rice", "complement", "classic", "main", "Lebanon's most celebrated dish and Lebanon's most celebrated wine — the wine's cedar and spice complexity mirrors the baharat; lamb handles the wine's tannins; a pairing of centuries")
    PAIR(prod_mus, "Kibbeh nayyeh (raw lamb tartare) with bulgur, onion, and pine nuts", "complement", "established", "starter", "Raw lamb and aged Lebanese red — Musar's complexity and dried fruit character handles the raw lamb's richness; pine nuts bridge the wine's cedar notes")

p_ksa = P("Château Ksara", "Lebanon", r_bek,
           description="The Jesuit Fathers' 1857 Bekaa Valley estate — Lebanon's oldest continuously operating winery — producing a wide range of accessible and premium wines from Cabernet Sauvignon, Syrah, and Merwah (the ancient indigenous white variety). Ksara's Clos St. Alphonse and Reserve du Couvent are Lebanon's finest second labels.")
prod_ksa, new = PROD("Château Ksara Reserve du Couvent Rouge", "wine_still", p_ksa, r_bek, "Lebanon",
                     subcategory="Syrah Blend",
                     description="Lebanon's most consistently acclaimed and widely available premium red from the Jesuit Ksara cellar — Syrah, Cabernet Sauvignon, and Merlot from high-altitude Bekaa limestone. Blackberry, cedar, Mediterranean herbs, tobacco, and a warm, generous structure that reflects the Bekaa's ancient soils.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ksa, "Kafta (spiced minced lamb) with tomato, onion, and flatbread on the grill", "complement", "classic", "main", "Lebanese barbecue and Lebanese red wine — the wine's warm Mediterranean spice echoes the kafta's spice blend; the grilled char bridges the wine's cedar oak notes")
    PAIR(prod_ksa, "Mujaddara (lentil and rice pilaf) with caramelized onion and yogurt", "complement", "established", "main", "The Levant's most ancient and comforting dish paired with Lebanon's most historic winery — the wine's earthy character mirrors the lentils; yogurt provides acidity to lift both")

# ── COLCHAGUA VALLEY DO (CHILE) ───────────────────────────────────
print("\n=== Colchagua Valley DO (Chile) ===")
r_col = R("Colchagua Valley", "Chile", "wine",
           designation_type="DO",
           designation_name="Colchagua Valley DO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Chile's premier red wine valley south of Santiago in the Rapel Region, producing the country's most internationally acclaimed Carmenère — the 'lost Bordeaux variety' rediscovered in Chile in 1994 — alongside powerful Cabernet Sauvignon and structured Malbec. The valley's well-draining alluvial soils and warm Mediterranean climate create wines of dark fruit intensity and excellent structure. The Apalta sub-zone, with its unique curved shape and granite soils, produces Chile's finest wines.",
           key_producers="Montes, Casa Lapostolle, Viu Manent, Clos Apalta, Lapostolle",
           historical_context="Carmenère was brought to Chile from Bordeaux in the 1850s and survived there after Phylloxera eliminated it from France. For over a century it was misidentified as Merlot. In 1994, French ampelographer Jean-Michel Boursiquot identified the variety during a visit — Chile's 'lost' Bordeaux grape was suddenly the country's most distinctive asset. Robert Mondavi and Felipe Chadwick's Seña, established in 1997, helped establish Colchagua's international credentials.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Colchagua vintage; Carmenère from Apalta granite showed extraordinary dark chocolate intensity and mineral precision."),
    (2021, "very_good", "stable", "Classic Chilean vintage; Cabernet Sauvignon and Carmenère blends showed excellent fruit depth and structural finesse."),
    (2020, "excellent", "stable", "Benchmark year; Montes Alpha M and Casa Lapostolle Clos Apalta produced internationally acclaimed wines of exceptional quality."),
    (2019, "excellent", "rising", "Outstanding vintage; Carmenère reached its highest critical scores yet; Apalta granite produced wines of legendary concentration."),
    (2018, "very_good", "stable", "Solid vintage; Cabernet Sauvignon of excellent structure; Carmenère showed good varietal character and food-friendly tannins."),
]:
    VIN(r_col, yr, qd, pt, sn)

p_mon = P("Montes", "Chile", r_col,
           description="Aurelio Montes and Douglas Murray's pioneering Colchagua estate that proved Chilean wine could compete at the highest international level. Montes Alpha M — a Cabernet Sauvignon-dominated Bordeaux blend from the Apalta hillside — was Chile's first internationally acclaimed premium wine; Montes Folly Syrah from vertical Apalta slopes is Chile's most celebrated Syrah.")
prod_mon, new = PROD("Montes Purple Angel Carmenère", "wine_still", p_mon, r_col, "Chile",
                     subcategory="Carmenere",
                     description="Chile's most celebrated single-variety Carmenère from Apalta's granite hillside — dark chocolate, blackberry, red pepper, tobacco, and the distinctive Carmenère vegetal complexity when perfectly ripe. One of Chile's finest wines and the definitive expression of this unique variety at its most complete.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mon, "Osso buco a la Chilena with chicha de uva (grape reduction) and pebre", "complement", "classic", "main", "Chilean braised veal and Chilean Carmenère — the wine's dark chocolate and tobacco complexity handles the rich braising; red pepper in the pebre bridges the Carmenère's characteristic notes")
    PAIR(prod_mon, "Slow-roasted suckling pig (lechón) with merkén (smoked chilli) and roasted corn", "complement", "established", "main", "Colchagua's festive pork tradition and its finest Carmenère — the wine's dark fruit handles the pork's rich fat; merkén's smoke bridges the wine's tobacco character")

p_lap = P("Casa Lapostolle", "Chile", r_col,
           description="Alexandra Marnier Lapostolle's French-Chilean Apalta estate producing Clos Apalta — consistently Chile's highest-scoring wine and one of the Southern Hemisphere's finest reds. The Apalta hillside's unique curved shape, granitic soils, and warm microclimate create extraordinary conditions for Carmenère, Merlot, and Cabernet Sauvignon.")
prod_lap, new = PROD("Casa Lapostolle Clos Apalta", "wine_still", p_lap, r_col, "Chile",
                     subcategory="Carmenere Blend",
                     description="Chile's most critically acclaimed wine from the legendary Apalta hillside — Carmenère, Merlot, Cabernet Franc, and Petit Verdot from granitic soils. Dark cherry, chocolate, tobacco, cedar, violets, and the structured elegance that makes Apalta granite Chile's greatest wine terroir. Rivals Napa's finest Bordeaux blends.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_lap, "Prime beef tenderloin with black truffle crust, red wine jus, and pommes purée", "complement", "classic", "main", "Chile's finest red wine and its finest cut of beef — Carmenère's chocolate and cedar complexity handles the truffle intensity; the wine's structure matches the tenderloin's richness")
    PAIR(prod_lap, "Smoked duck breast with cherry reduction, lentils, and micro herbs", "complement", "established", "main", "The wine's dark cherry and tobacco character bridges the smoked duck; cherry reduction mirrors the Carmenère's fruit; lentils provide earthy depth the wine can match")

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
