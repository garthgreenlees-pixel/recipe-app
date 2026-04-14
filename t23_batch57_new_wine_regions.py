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
    cur.execute("""INSERT INTO beverage_regions
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Aglianico del Vulture (Italy/Basilicata) ───────────────────────────────
print("\n=== Aglianico del Vulture (Italy) ===")
r1 = R("Aglianico del Vulture", "Italy",
    beverage_family="wine",
    designation_type="DOC/DOCG",
    designation_name="Aglianico del Vulture DOC / Aglianico del Vulture Superiore DOCG",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Southern Italy's most compelling and age-worthy red wine appellation, Aglianico del Vulture grows on the volcanic slopes of Monte Vulture in Basilicata — one of Italy's most isolated and least-known wine regions. Aglianico, the ancient grape of Magna Graecia, produces wines of extraordinary tannic structure, dark fruit concentration and volcanic mineral character that require 8–15 years to reveal their full complexity and can age for 30+ years; often compared to Barolo in its austerity, power and longevity.",
    key_producers="Cantina di Venosa, Elena Fucci, Basilisco, Grifalco, D'Angelo",
    historical_context="Aglianico is one of the ancient world's most significant grape varieties — its name derives from 'Hellenikos' (Greek) and it was the foundation of the legendary Falernian wine praised by Horace and Pliny. Monte Vulture's dormant volcano provided the mineral-rich soils that give the wine its distinctive character. The DOCG (Superiore) was awarded in 2011, recognising the appellation's exceptional potential. Elena Fucci's critically acclaimed Titolo single-vineyard bottling has brought international attention to what was previously a purely local obsession.")

VIN(r1, 2023, "excellent", "stable", "Outstanding Basilicata year; Aglianico of exceptional volcanic mineral concentration and tannic structure")
VIN(r1, 2022, "very_good", "stable", "Good year; complex Vulture Aglianico with the characteristic dark fruit intensity and mineral depth")
VIN(r1, 2021, "excellent", "stable", "Fine balance; elegant, structured Aglianico with remarkable aging potential from the volcanic soils")
VIN(r1, 2020, "very_good", "stable", "Reliable vintage; authentic Monte Vulture character with the dark fruit and iron mineral signature")
VIN(r1, 2019, "exceptional", "rising", "One of the finest Aglianico del Vulture vintages in memory; concentrated, age-worthy wines of international quality")

p1a = P("Elena Fucci", "Italy", r1, description="The most internationally celebrated Aglianico del Vulture producer and the estate that put Monte Vulture on the global wine map, Elena Fucci's small organic winery produces a single wine — Titolo — from a single organically farmed Aglianico vineyard that has achieved legendary status and critical scores that rival the finest Barolo and Brunello.")
prod1a, new1a = PROD("Elena Fucci Titolo Aglianico del Vulture DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="Aglianico",
    description="Italy's most celebrated Aglianico del Vulture and arguably southern Italy's finest red wine — a single-vineyard Aglianico from organic estate vines on Monte Vulture's volcanic soils, showing extraordinary dark cherry, violet, iron mineral, tobacco and volcanic ash complexity with the fierce tannin structure that demands 8–10 years cellaring and rewards patience with 25+ years of magnificent development.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Agnello lucano slow-braised with wild herbs and chilli", "complement", "classic", "main", "Basilicata's most authentic lamb preparation — slow-cooked mountain lamb with foraged herbs — with the region's greatest red wine; volcanic mineral depth and fierce tannin meet the earthy richness of long-braised mountain lamb.")
    PAIR(prod1a, "Handmade orecchiette with lamb and broccoli rabe", "complement", "classic", "main", "Southern Italian pasta shapes with Basilicata lamb — the wine's powerful tannin and dark fruit grip the bitter greens and rich meat in one of the Mezzogiorno's great regional pairings.")
    PAIR(prod1a, "Grilled salsiccia lucanica with roasted peppers", "complement", "established", "main", "Basilicata's famous spicy fennel sausage with Monte Vulture's fiercest red — the wine's volcanic intensity handles the pork fat and chilli with remarkable grip and mineral authority.")
    PAIR(prod1a, "Aged Pecorino di Moliterno with truffle honey", "complement", "established", "cheese", "Basilicata's indigenous aged sheep cheese with the region's greatest red — the wine's fierce tannin is tempered by the cheese's fat and salt while truffle honey bridges the dark fruit.")

p1b = P("Grifalco della Lucania", "Italy", r1, description="One of Aglianico del Vulture's most respected and quality-focused estates, Grifalco produces meticulous volcanic Aglianico wines from estate vineyards on Monte Vulture's ancient basalt soils, achieving exceptional critical acclaim for wines that combine the variety's characteristic austerity with surprising elegance and mineral purity.")
prod1b, new1b = PROD("Grifalco Damaschito Aglianico del Vulture DOC", "wine_still", p1b, r1, "Italy",
    subcategory="Aglianico",
    description="A benchmark single-vineyard Aglianico del Vulture — Grifalco's Damaschito from old vines on basalt volcanic soils, showing the variety's characteristic dark plum, iron mineral, tobacco and dried rose aromatics with the structured tannic grip that defines Monte Vulture Aglianico at its most authentic and compelling.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Braised wild boar with juniper and dark chocolate", "complement", "established", "main", "The wine's volcanic intensity and fierce tannin are ideally matched by wild boar's gamey richness and the dark bitter chocolate that bridges the Aglianico's dark fruit.")
    PAIR(prod1b, "Handmade lagane e ceci chickpea pasta", "complement", "classic", "main", "Basilicata's most ancient pasta recipe — lagane with chickpeas — with Monte Vulture Aglianico; peasant simplicity meets volcanic intensity in a pairing of deep historical authenticity.")
    PAIR(prod1b, "Agnello alla lucana with potatoes and rosemary", "complement", "classic", "main", "The wine's structured tannin and dark fruit intensity demand slow-roasted mountain lamb with the herbs of the volcanic plateau in a pairing of Basilicata's most powerful regional flavours.")
    PAIR(prod1b, "Provolone del Monaco aged cheese with chestnut honey", "complement", "established", "cheese", "The wine's iron-mineral depth and tobacco notes complement the aged provolone's sharp richness while chestnut honey bridges the dark fruit.")

# ── 2. Rheingau (Germany) ─────────────────────────────────────────────────────
print("\n=== Rheingau (Germany) ===")
r2 = R("Rheingau", "Germany",
    beverage_family="wine",
    designation_type="Anbaugebiet",
    designation_name="Rheingau Qualitätswein",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Germany's most historically prestigious wine region, the Rheingau sits along a south-facing 30km stretch of the Rhine River between Wiesbaden and Rüdesheim, where the river runs east-west, allowing vineyards to face south and maximise sun exposure on steep Taunus slate and quartzite slopes. The Rheingau has been the cradle of German wine history — producing Riesling of legendary complexity and longevity from the estates of great noble families — and established the stylistic benchmark for German fine wine with its combination of mineral precision, fruit purity and remarkable aging capacity.",
    key_producers="Robert Weil, Georg Breuer, Schloss Johannisberg, Hessische Staatsweingüter Kloster Eberbach, Leitz",
    historical_context="The Rheingau's wine tradition is medieval — Benedictine monks at Kloster Eberbach produced wine from 1136 that became famous throughout Europe. Schloss Johannisberg, established in 1130, is credited with the accidental discovery of Spätlese harvesting in 1775 when the harvest messenger was delayed and the overripe grapes produced Germany's first deliberate late-harvest wine. The Rheingau Classification (Erstes Gewächs) established in 1999 created Germany's first premier cru system. A quality renaissance from the 1990s restored the region's international reputation after decades of underachievement.")

VIN(r2, 2023, "excellent", "stable", "Outstanding Rheingau vintage; south-facing Riesling of exceptional mineral precision and classical German elegance")
VIN(r2, 2022, "very_good", "stable", "Warm year with good concentration; full, ripe Rheingau Riesling of approachable character")
VIN(r2, 2021, "excellent", "stable", "Elegant and precise; benchmark vintage for Rheingau Erstes Gewächs dry Riesling")
VIN(r2, 2020, "very_good", "stable", "Reliable year; characteristic Taunus slate mineral precision across the Rheingau's finest estates")
VIN(r2, 2019, "exceptional", "rising", "One of Rheingau's finest recent vintages; age-worthy, complex Riesling of benchmark historical quality")

p2a = P("Weingut Robert Weil", "Germany", r2, description="The most internationally acclaimed Rheingau estate and the benchmark for German Riesling of all styles from Grosses Gewächs dry to legendary TBA sweet wines, Wilhelm Weil's estate in Kiedrich produces wines of extraordinary concentration, mineral purity and longevity that are considered among Germany's finest and most age-worthy expressions of the Riesling variety.")
prod2a, new2a = PROD("Weingut Robert Weil Kiedricher Grafenberg Riesling Grosses Gewachs Rheingau", "wine_still", p2a, r2, "Germany",
    subcategory="Riesling",
    description="One of Germany's finest Grosses Gewächs — Robert Weil's benchmark dry Riesling from the legendary Kiedricher Gräfenberg vineyard on deep blue Taunus slate, showing extraordinary mineral depth, citrus, peach and the characteristic smoky flint signature of great Rheingau Riesling; ages magnificently for 15–20+ years.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Rhine salmon with brown butter and capers", "complement", "classic", "main", "The Rhine Valley's own heritage fish — once abundant, now rare — with the Rheingau's greatest Riesling; the wine's mineral precision and citrus character frame the salmon in a pairing of historical and regional completeness.")
    PAIR(prod2a, "Lobster thermidor with tarragon cream", "complement", "established", "main", "Dry Riesling's mineral precision and firm acidity cut through lobster cream with aristocratic German authority, the wine's citrus note bridging the tarragon.")
    PAIR(prod2a, "Zander fillet with Riesling butter sauce", "complement", "classic", "main", "Using the wine's own variety in the sauce — Zander (pike-perch) with Rheingau Riesling beurre blanc — creates the most self-referential and satisfying German wine-food pairing possible.")
    PAIR(prod2a, "Allgäuer Bergkäse aged 12 months with alpine herbs", "complement", "established", "cheese", "The wine's mineral slate character and citrus precision complement the nutty, crystalline alpine cheese with the mineral depth that only Taunus slate Riesling can provide.")

p2b = P("Georg Breuer", "Germany", r2, description="One of Rheingau's most innovative and internationally respected estates, Bernhard Breuer and his daughter Theresa pioneered the dry Riesling (Rheingau Erstes Gewächs) revolution and established the Berg Schlossberg and Rüdesheimer Berg sites as benchmark Rheingau Riesling expressions of world-class quality and mineral precision.")
prod2b, new2b = PROD("Georg Breuer Berg Schlossberg Riesling Rheingau Erstes Gewachs", "wine_still", p2b, r2, "Germany",
    subcategory="Riesling",
    description="A benchmark Rheingau Erstes Gewächs from the legendary Berg Schlossberg — one of Germany's most dramatically steep vineyard sites above Rüdesheim, producing dry Riesling of extraordinary power, spice, mineral concentration and the smoky-flint character unique to the Rheingau's deep Taunus quartzite soils.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Roasted Riesling-marinated pork cheeks with sauerkraut", "complement", "classic", "main", "The wine's own variety used to marinate the pork — Rheingau Riesling with Riesling-prepared pork in a circular German pairing of complete regional logic.")
    PAIR(prod2b, "White asparagus with Hollandaise and Rhine salmon", "complement", "classic", "main", "Germany's most celebrated seasonal combination — Spargel with Hollandaise and river fish with the Rheingau's finest dry Riesling — perfection defined.")
    PAIR(prod2b, "Sauerkraut-braised pork knuckle with mustard", "complement", "established", "main", "The wine's powerful mineral character and firm acidity cut through the rich pork fat and sauerkraut's acidity in one of Germany's most enduring wine-food traditions.")
    PAIR(prod2b, "Riesling-washed Limburger cheese with onion bread", "complement", "classic", "cheese", "Rheingau Riesling-washed Limburger with its own source wine — the pungent washed rind's aroma is tamed by the wine's mineral authority while its fat is cut by the Riesling's acidity.")

# ── 3. Bourgueil (France/Loire) ───────────────────────────────────────────────
print("\n=== Bourgueil (France) ===")
r3 = R("Bourgueil", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Bourgueil AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of the Loire Valley's most important and historically significant red wine appellations, Bourgueil produces Cabernet Franc of distinctive freshness, violet aromatics and tuffeau limestone mineral character from the north bank of the Loire in Indre-et-Loire. Bourgueil and its sub-appellation Saint-Nicolas-de-Bourgueil produce lighter, more herbaceous Cab Franc than Chinon but with excellent aging potential, particularly from the Restigné and La Chapelle plateau sites; the wines express the Loire's distinctive red-fruit-and-graphite character at its most approachable.",
    key_producers="Domaine Yannick Amirault, Cathiard-Molinier, Pierre-Jacques Druet, Lamé-Delille-Boucard",
    historical_context="Bourgueil's wine history dates from the 11th century when Benedictine monks at the Abbey of Bourgueil cultivated Cabernet Franc vines that would spread throughout the Loire Valley. Rabelais mentioned Bourgueil wine with delight in the 16th century; Balzac's novels are filled with references to Loire wines from this area. The modern appellation was established in 1937, predating many Loire AOCs. The distinction between gravel-terrace wines (fresh, fruity, early-drinking) and plateau tuffeau wines (structured, age-worthy, mineral) is the key to understanding Bourgueil's diverse production.")

VIN(r3, 2023, "excellent", "stable", "Outstanding Loire vintage; Bourgueil Cab Franc of exceptional violet freshness and graphite mineral character")
VIN(r3, 2022, "very_good", "stable", "Warm year; generous, fruit-forward Bourgueil with soft tannins and good Loire freshness")
VIN(r3, 2021, "excellent", "stable", "Classic Loire character; elegant, precise Cab Franc with fine mineral tuffeau expression")
VIN(r3, 2020, "very_good", "stable", "Good concentration with characteristic Loire freshness; excellent plateau tuffeau site expression")
VIN(r3, 2019, "excellent", "rising", "Fine Bourgueil vintage; structured, age-worthy tuffeau Cab Franc of benchmark character")

p3a = P("Domaine Yannick Amirault", "France", r3, description="One of Bourgueil's most critically acclaimed and internationally respected estates, Yannick Amirault produces a comprehensive range of Bourgueil Cab Franc wines from gravel and tuffeau terroirs that demonstrate the appellation's full quality range, with his La Coudraye and Les Quarterons bottlings achieving the highest scores for Loire red wine quality.")
prod3a, new3a = PROD("Domaine Yannick Amirault La Coudraye Bourgueil AOC", "wine_still", p3a, r3, "France",
    subcategory="Cabernet Franc",
    description="One of Bourgueil's most celebrated tuffeau expressions — from Amirault's La Coudraye vines on the limestone plateau above the Loire, showing distinctive violet, pencil shavings, raspberry, graphite and the characteristic chalky mineral finish of tuffeau-grown Cab Franc that ages magnificently for 10–15 years.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Grilled Loire Valley pigeon with peas and lardons", "complement", "classic", "main", "The Loire's most celebrated red wine pairing — Cab Franc with roasted pigeon; the wine's red fruit and fine tannins frame the rich bird with Loire elegance.")
    PAIR(prod3a, "Rillons de Tours (slow-cooked pork belly)", "complement", "classic", "main", "The Tours pork belly specialty — slow-rendered until caramelised — with Loire Cab Franc is one of the valley's most traditional and satisfying pairings.")
    PAIR(prod3a, "Rabbit with mustard cream and tarragon", "complement", "classic", "main", "The Loire's most beloved rabbit preparation with its finest red grape — Cab Franc's herbal note and bright acidity frame rabbit's gentle protein with regional authenticity.")
    PAIR(prod3a, "Sainte-Maure de Touraine goat cheese log", "complement", "classic", "cheese", "Loire's most famous goat cheese with its most celebratable red wine — the Cab Franc's red fruit and mineral acidity complement the chalky, herbaceous goat cheese in the valley's quintessential cheese pairing.")

p3b = P("Pierre-Jacques Druet", "France", r3, description="One of Bourgueil's most artisanal and revered producers, Pierre-Jacques Druet produces a remarkable range of small-lot Bourgueil wines from distinct terroir parcels — Vaumoureau, Grand Mont, Cent Boisselées — that demonstrate the appellation's capacity for genuine terroir complexity and differentiation from the Loire's diverse subsoils.")
prod3b, new3b = PROD("Pierre-Jacques Druet Grand Mont Bourgueil AOC", "wine_still", p3b, r3, "France",
    subcategory="Cabernet Franc",
    description="A benchmark single-parcel Bourgueil from the Grand Mont tuffeau terroir — showing the limestone plateau's characteristic concentration, violet and cassis depth, fine chalky tannin and mineral precision that makes Grand Mont wines some of the most age-worthy and complex Cab Francs produced anywhere in the Loire Valley.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Slow-roasted Loire Valley duck with orange and thyme", "complement", "classic", "main", "Loire duck — prepared with orange and thyme in the Touraine tradition — with the valley's most structured Cab Franc; the wine's dark fruit and herbal note bridge the citrus and rich duck.")
    PAIR(prod3b, "Chicken roti with garlic and herbes de Loire", "complement", "classic", "main", "Simple roasted chicken with local herbs and the valley's Cab Franc — the most universal and historically authentic Loire wine and food pairing of all.")
    PAIR(prod3b, "Andouillette with mustard and caramelised onion", "complement", "established", "main", "The Loire's most acquired taste — Tours andouillette (tripe sausage) — with the valley's most characterful red; the wine's mineral acidity and structure handle the intense charcuterie.")
    PAIR(prod3b, "Crottin de Chavignol aged with walnut bread", "complement", "classic", "cheese", "Aged Loire goat cheese with its most characteristic red wine — the Cab Franc's violet-mineral character and the crottin's lactic tang create one of France's most naturally balanced cheese-wine pairings.")

# ── 4. Cannonau di Sardegna (Italy/Sardinia) ──────────────────────────────────
print("\n=== Cannonau di Sardegna (Italy) ===")
r4 = R("Cannonau di Sardegna", "Italy",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Cannonau di Sardegna DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Sardinia's most important and internationally recognised red wine appellation, Cannonau di Sardegna produces characterful, warming reds from the Cannonau grape — genetically identical to Spain's Grenache and France's Garnacha but uniquely adapted to Sardinia's granitic terrain and extreme Mediterranean climate. Sardinian Cannonau, particularly from the Ogliastra and Nuoro areas, produces some of Italy's most distinctive and age-worthy Grenache expressions — concentrated dark fruit, wild herbs, iron mineral character — and is celebrated as a longevity wine, as the Sardinian Blue Zone has the world's highest concentration of male centenarians who drink it daily.",
    key_producers="Sella and Mosca, Argiolas, Sardus Pater, Giuseppe Sedilesu, Tenute Dettori",
    historical_context="Cannonau (Grenache) is believed to have originated in Sardinia thousands of years before its appearance in Spain — new genetic evidence suggests the grape may have been domesticated on the island in the Bronze Age, making it potentially the world's oldest cultivated wine variety. The DOC was established in 1972 and covers the entire island. The association between Cannonau wine and Sardinian longevity — documented in Dan Buettner's Blue Zone research — has created extraordinary global interest in this previously obscure island wine.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Sardinian year; Cannonau of exceptional dark fruit concentration and wild herb mineral character")
VIN(r4, 2022, "very_good", "stable", "Warm and concentrated; powerful, full-bodied Cannonau with the characteristic island mineral depth")
VIN(r4, 2021, "excellent", "stable", "Fine balance; elegant Cannonau di Sardegna with remarkable freshness for the hot Mediterranean climate")
VIN(r4, 2020, "very_good", "stable", "Reliable year; authentic Sardinian character with the dark fruit and macchia aroma that defines the variety")
VIN(r4, 2019, "exceptional", "rising", "One of Sardinia's finest recent Cannonau vintages; concentrated, age-worthy wines of benchmark quality")

p4a = P("Giuseppe Sedilesu", "Italy", r4, description="The most critically acclaimed artisan Cannonau producer on Sardinia, Giuseppe Sedilesu's family estate in Mamoiada in the Barbagia highlands farms ancient ungrafted Cannonau bush vines at altitude to produce wines of extraordinary concentration, mineral depth and longevity that have established Sardinian Cannonau as a serious fine wine of global significance.")
prod4a, new4a = PROD("Giuseppe Sedilesu Mamuthone Cannonau di Sardegna DOC", "wine_still", p4a, r4, "Italy",
    subcategory="Cannonau (Grenache)",
    description="The benchmark artisan Sardinian Cannonau — from Sedilesu's ancient ungrafted bush vines in the Barbagia highlands above Mamoiada, showing extraordinary dark cherry, iron mineral, wild myrtle and macchia aromatics with the structured tannin and concentrated power that makes highland Sardinian Cannonau unique among the world's Grenache expressions.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Porcetto sardo whole-roasted suckling pig on myrtle", "complement", "classic", "main", "Sardinia's most celebrated and ancient feast preparation — suckling pig slow-roasted and served on myrtle branches — with the island's most distinctive red wine; both sharing the myrtle-macchia aromatic signature of the Barbagia highlands.")
    PAIR(prod4a, "Pecora alla sarda braised mutton with saffron and herbs", "complement", "classic", "main", "Sardinia's ancient mutton braise with the island's ancient Cannonau grape — indigenous sheep and indigenous vine in a pairing of pre-Roman Mediterranean cultural depth.")
    PAIR(prod4a, "Culurgiones pasta with potato and mint filling", "complement", "established", "main", "Sardinia's unique stuffed pasta — potato and mint filling in a distinctive spiked crimp — with the island's powerful red; Cannonau's intensity handles the starchy richness while mint bridges the wine's wild herb character.")
    PAIR(prod4a, "Aged Pecorino Sardo with Sardinian honey and walnuts", "complement", "classic", "cheese", "The island's indigenous sheep cheese — aged Pecorino Sardo — with Sardinian Cannonau and local honey creates a Blue Zone-inspired tasting of Sardinia's most ancient food and wine traditions.")

p4b = P("Tenute Dettori", "Italy", r4, description="One of Sardinia's most distinctive and internationally celebrated natural wine producers, Alessandro Dettori farms ancient Cannonau, Vermentino and Monica vines without any additives or chemicals in Romangia, producing some of the island's most pure and characterful expressions of indigenous Sardinian varieties that have earned cult status among natural wine enthusiasts worldwide.")
prod4b, new4b = PROD("Tenute Dettori Dettori Rosso Cannonau di Sardegna DOC", "wine_still", p4b, r4, "Italy",
    subcategory="Cannonau",
    description="Alessandro Dettori's purist natural Cannonau — from ancient ungrafted vines in Romangia, fermented with indigenous yeasts and aged without sulphur additions in old wood, producing a wine of extraordinary aromatic intensity, dark fruit depth, orange peel, iron mineral and wild herb character that is unique in the Sardinian wine landscape.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Agnello sardo with wild rosemary and garlic", "complement", "classic", "main", "Sardinian mountain lamb with the island's wildest Cannonau expression — the natural wine's fierce fruit and wild herb character mirror the lamb's intensity in a pairing of raw Mediterranean authenticity.")
    PAIR(prod4b, "Sardinian fregola with bottarga and lemon", "complement", "established", "main", "The wine's orange peel and mineral depth create an unexpected bridge with the dried mullet roe's oceanic intensity over the toasted pasta beads.")
    PAIR(prod4b, "Lonza di tonno Sarda with capers and bread", "complement", "established", "starter", "Sardinian cured bluefin tuna with the island's most natural red wine — the wine's iron mineral and orange peel notes bridge the cured fish with Mediterranean island logic.")
    PAIR(prod4b, "Fiore Sardo cheese aged 6 months with acacia honey", "complement", "classic", "cheese", "Sardinia's oldest documented cheese — Fiore Sardo sheep milk — with the island's most ancient grape variety and local honey creates a pairing of Sardinian cultural heritage at its most pure.")

# ── 5. Irouleguy (France/Basque) ──────────────────────────────────────────────
print("\n=== Irouleguy (France) ===")
r5 = R("Irouleguy", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Irouléguy AOC",
    reputation_tier="overlooked",
    quality_trajectory="ascending",
    description="France's smallest and most geographically dramatic wine appellation, Irouléguy sits on the steep Pyrenean slopes of the Basque Country near Saint-Jean-Pied-de-Port, producing unique reds, rosés and whites from indigenous Basque varieties — Tannat, Cabernet Franc, Cabernet Sauvignon and the rare white Gros Manseng and Courbu. The extreme altitude (200–600m), iron-rich schist and ophite soils, and the distinctive Basque climate create wines of powerful character, mineral depth and authentic regional identity found nowhere else in France.",
    key_producers="Domaine Arretxea, Domaine Brana, Cave d'Irouléguy, Domaine Ilarria",
    historical_context="Irouléguy's wine history is intimately tied to the pilgrimage route to Santiago de Compostela — the Abbey of Roncevaux and its pilgrim hospice at Saint-Jean-Pied-de-Port maintained vineyards from the 11th century. The village cooperative Cave d'Irouléguy was established in 1953 when mountain viticulture was in crisis; its survival preserved the appellations diversity. The AOC was granted in 1970 and today attracts passionate small producers drawn by the extreme terroir, Basque cultural identity and the complete uniqueness of this tiny wine corner of France.")

VIN(r5, 2023, "excellent", "stable", "Outstanding Basque Pyrenean year; Irouléguy Tannat and Cabernet Franc of remarkable freshness and mineral depth")
VIN(r5, 2022, "very_good", "stable", "Good mountain year; concentrated Tannat with the characteristic iron-schist mineral of the Pyrenean foothill soils")
VIN(r5, 2021, "excellent", "stable", "Elegant and precise; fine balance of Tannat tannin and fresh Cab Franc in the classic Irouléguy blend")
VIN(r5, 2020, "very_good", "stable", "Reliable Basque year; authentic iron-mineral character across red and white Irouléguy expressions")
VIN(r5, 2019, "exceptional", "rising", "One of Irouléguy's finest vintages; concentrated, age-worthy Tannat blends of benchmark mountain character")

p5a = P("Domaine Arretxea", "France", r5, description="Irouléguy's most celebrated and internationally revered estate, Michel and Thérèse Riouspeyrous farm biodynamically on extreme steep slopes to produce wines of extraordinary mineral depth, wild character and authentic Basque identity that have established Irouléguy as one of France's most compelling small appellations for adventurous wine lovers.")
prod5a, new5a = PROD("Domaine Arretxea Haitza Irouleguy AOC Rouge", "wine_still", p5a, r5, "France",
    subcategory="Tannat, Cabernet Franc",
    description="The benchmark biodynamic Irouléguy red — from Arretxea's steep schist vineyards above Saint-Jean-Pied-de-Port, showing extraordinary iron mineral depth, dark cherry, violet, spice and the fierce Tannat tannin structure softened by Cab Franc elegance; a wine of complete Basque mountain identity and remarkable aging potential.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Basque axoa de veau veal mince with Espelette pepper", "complement", "classic", "main", "The Basque Country's most characteristic veal preparation — minced with Espelette pepper — with Irouléguy's most celebrated red; the wine's iron mineral and dark fruit perfectly frame the pepper-spiced veal.")
    PAIR(prod5a, "Grilled Basque beef txuleta rib chop with sea salt", "complement", "classic", "main", "The Basque ikastola rib chop — aged at room temperature and grilled over coals — with the Pyrenean's most structured red; the wine's Tannat tannin and mineral depth match the intense beef character.")
    PAIR(prod5a, "Ttoro Basque fish stew with bread", "bridge", "adventurous", "main", "An unexpected pairing — the wine's iron mineral and Tannat structure bridge the saffron-spiced fish stew's briny intensity in a demonstration of Irouléguy's extraordinary gastronomic versatility.")
    PAIR(prod5a, "Ossau-Iraty sheep cheese with Espelette jam", "complement", "classic", "cheese", "The Pyrenees' most celebrated cheese with the region's most distinctive red wine and Basque chilli jam — a triptych of Basque cultural identity and gastronomic completeness.")

p5b = P("Domaine Brana", "France", r5, description="One of Irouléguy's most historically significant and quality-focused estates, Etienne Brana's family produces both AOC Irouléguy wines and the famous Poire Williams eau-de-vie that has made the Brana name famous throughout the Basque Country; their Irouléguy wines demonstrate the appellation's capacity for both powerful reds and distinctive aromatic whites.")
prod5b, new5b = PROD("Domaine Brana Ohitza Irouleguy AOC Blanc", "wine_still", p5b, r5, "France",
    subcategory="Gros Manseng, Courbu",
    description="A unique and rare Basque white wine from Irouléguy's indigenous varieties — Gros Manseng and Courbu on iron-schist Pyrenean soils, showing distinctive white peach, citrus, Basque mineral character and a herbal mountain freshness that places this wine in a category of complete geographic and cultural singularity.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Grilled Basque anchovies with olive oil and vinegar", "complement", "classic", "starter", "The wine's mineral freshness and citrus precision are the natural companion for the Basque coast's prized anchovies — both products of the same Atlantic-mountain cultural territory.")
    PAIR(prod5b, "Piperade Basque with jambon de Bayonne", "complement", "classic", "main", "The Basque Country's most emblematic egg preparation with the appellation's most distinctive white wine — regional identity expressed simultaneously through food and vine.")
    PAIR(prod5b, "Bacalao a la Basque with tomato and olives", "complement", "established", "main", "Salt cod in the Basque tradition with Irouléguy's white — the wine's mountain mineral freshness and citrus drive frame the rehydrated bacalao with cross-Pyrenean logic.")
    PAIR(prod5b, "Mique Landaise bread dumpling with Basque ham", "complement", "classic", "main", "The southwest's rustic cornmeal dumpling with Bayonne ham finds an ideal mineral companion in the Basque mountains' most distinctive white wine.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
conn.close()
