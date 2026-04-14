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

# ── 1. NAPA VALLEY SUB-REGION: STAGS LEAP DISTRICT (USA) ────────────────────
print("\n=== Stags Leap District (USA) ===")
r = R("Stags Leap District", "USA", "wine",
      designation_type="AVA",
      designation_name="Stags Leap District AVA",
      reputation_tier="prestigious",
      quality_trajectory="established",
      description="One of Napa Valley's most celebrated sub-AVAs, famous as the source of the 1976 Paris Tasting wines that defeated Bordeaux First Growths in blind competition. The palisade rock formation on the eastern valley wall creates a unique thermal belt — warm days with afternoon shadow from the rocks creating rapid cooling — resulting in Cabernet Sauvignon of extraordinary silkiness, approachability, and iron-mineral precision.",
      key_producers="Stag's Leap Wine Cellars, Clos du Val, Shafer Vineyards, Chimney Rock, Pine Ridge",
      historical_context="The Stags Leap District achieved international fame when Warren Winiarski's Stag's Leap Wine Cellars 1973 Cabernet Sauvignon defeated Chateau Mouton Rothschild and other Bordeaux First Growths at the 1976 Paris Tasting judged by French experts. This event, captured in the film Bottle Shock, transformed global perceptions of California wine and established Napa Valley as a world-class wine region.")

VIN(r, 2023, "excellent", "rising", "Outstanding Napa growing season; Stags Leap Cabernet of exceptional silkiness and iron-mineral precision")
VIN(r, 2022, "very_good", "rising", "Good vintage; characteristic approachable, cashmere-textured Cabernet from the eastern valley palisades")
VIN(r, 2021, "good", "stable", "Smoke-affected harvest required fruit sorting; best wines showed the district's signature elegance")
VIN(r, 2020, "good", "stable", "Challenging wildfire smoke vintage; careful selection produced wines of typical district character")
VIN(r, 2019, "excellent", "rising", "Benchmark Napa vintage; finest Stags Leap District Cabernet in a generation")

p1 = P("Stag's Leap Wine Cellars", "USA", r, "winery",
        "The most historically significant estate in Napa Valley, Warren Winiarski's Stag's Leap Wine Cellars produced the 1973 Cabernet Sauvignon that defeated Bordeaux at the 1976 Paris Tasting. The estate is now owned by Ste. Michelle Wine Estates and Antinori, and continues to produce benchmark Napa Cabernet from the original Fay and SLV vineyards.")
prod1, new1 = PROD("Stag's Leap Wine Cellars Artemis Cabernet Sauvignon Stags Leap District", "wine_still", p1, r, "USA",
    subcategory="Cabernet Sauvignon",
    description="Signature Stags Leap District Cabernet; blackcurrant, cassis, cedar, and the distinctive iron-mineral quality of the palisade rock formation — silky, elegant, and more approachable than Oakville or Rutherford neighbours",
    price_tier="premium")
if new1:
    PAIR(prod1, "Dry-aged prime rib with horseradish crust and jus", "complement", "classic", "main", "The definitive California luxury pairing: silky, iron-mineral Napa Cabernet with dry-aged prime rib")
    PAIR(prod1, "Grilled portobello mushroom with truffle oil and Parmesan", "complement", "established", "main", "The wine's cedar and iron notes resonate with the earthy, umami-rich mushroom and truffle")
    PAIR(prod1, "Rack of lamb with rosemary and Cabernet reduction", "complement", "classic", "main", "Cassis-fruited Stags Leap Cabernet and herb-crusted rack of lamb — the California restaurant fine dining classic")
    PAIR(prod1, "Aged Cabbot Clothbound Cheddar or Fiscalini Bandaged Cheddar", "bridge", "established", "cheese", "The wine's cassis and cedar notes bridge elegantly with the crystalline, nutty complexity of aged American cheddar")

p2 = P("Shafer Vineyards", "USA", r, "winery",
        "One of Napa Valley's most celebrated family estates, Shafer's Hillside Select Cabernet Sauvignon from the Stags Leap District is consistently rated as one of America's greatest wines. The estate's careful farming of the rocky hillside soils produces wines of extraordinary concentration, complexity, and aging potential.")
prod2, new2 = PROD("Shafer One Point Five Cabernet Sauvignon Stags Leap District", "wine_still", p2, r, "USA",
    subcategory="Cabernet Sauvignon",
    description="One step below Hillside Select; textured, complex Stags Leap Cabernet with dark cherry, graphite, tobacco, and the district's characteristic silky tannin structure — one of Napa's finest value wines",
    price_tier="ultra_premium")
if new2:
    PAIR(prod2, "Grilled filet mignon with Bordelaise sauce", "complement", "classic", "main", "The wine's graphite, dark cherry, and silky tannins make it the ideal partner for the most classic steakhouse preparation")
    PAIR(prod2, "Duck confit with cherry-Port reduction and crispy skin", "complement", "classic", "main", "Rich, complex Napa Cabernet with the sweetness of cherry-Port sauce and the richness of confited duck")
    PAIR(prod2, "Black truffle and aged Parmesan risotto", "complement", "established", "main", "The wine's tobacco and earthy complexity resonates with the luxurious depth of black truffle in a fine risotto")
    PAIR(prod2, "Aged Mimolette or Comté with sourdough", "bridge", "suggested", "cheese", "The wine's graphite and dark fruit notes bridge with the nutty, caramelised complexity of these aged cow's milk cheeses")

# ── 2. MAREMMA TOSCANA (consolidate sub-regions) ── let's do MENDOCINO instead
# Actually Maremma Toscana DOC already exists in DB; let's do Mendocino

print("\n=== Mendocino County (USA) ===")
r2 = R("Mendocino County", "USA", "wine",
       designation_type="AVA",
       designation_name="Mendocino AVA",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="California's northernmost major wine county, known for its wild coastline, redwood forests, and Anderson Valley's cool climate sub-AVA (already in DB). Mendocino County proper encompasses warmer inland valleys producing Zinfandel, Petite Sirah, and Cabernet Sauvignon, while pioneering the organic and biodynamic movement in California viticulture. Fetzer, Bonterra, and Frey Vineyards established the county as America's first major organic wine region.",
       key_producers="Frey Vineyards, Bonterra Vineyards, Fetzer, Navarro Vineyards, Brutocao Cellars",
       historical_context="Mendocino County's wine history dates to the 1850s Italian Swiss immigrants, but its modern identity was forged by the counterculture movement of the 1970s. Frey Vineyards became America's first certified organic wine producer in 1980, and the county's commitment to sustainable viticulture has remained its defining characteristic. The Anderson Valley sub-AVA attracted premium producers seeking cool-climate Burgundian conditions, while inland Redwood Valley built its reputation on old-vine Zinfandel.")

VIN(r2, 2023, "excellent", "stable", "Good Mendocino growing season; inland warmth produced concentrated Zinfandel and Petite Sirah")
VIN(r2, 2022, "very_good", "stable", "Reliable vintage across the county; organic producers particularly rewarded with clean, vibrant fruit")
VIN(r2, 2021, "good", "stable", "Smoke-affected in places; best inland sites produced wines of characteristic rusticity and warmth")
VIN(r2, 2020, "good", "stable", "Challenging wildfire year; Redwood Valley old-vine Zinfandel showed resilience and concentration")
VIN(r2, 2019, "excellent", "stable", "Benchmark Mendocino vintage; finest Zinfandel and Petite Sirah in recent memory")

p3 = P("Frey Vineyards", "USA", r2, "winery",
        "America's first certified organic and biodynamic wine producer, Frey Vineyards has farmed their Redwood Valley estate without synthetic inputs since 1980. Their wines — particularly the biodynamic Zinfandel and Petite Sirah — represent the pioneering spirit of Mendocino's sustainable wine movement and remain among America's most authentically farmed wines.")
prod3, new3 = PROD("Frey Biodynamic Zinfandel Mendocino", "wine_still", p3, r2, "USA",
    subcategory="Zinfandel",
    description="America's most historically significant organic wine estate; biodynamic old-vine Zinfandel from Redwood Valley — jammy, spiced, and rustic with blackberry, black pepper, and dried herb character",
    price_tier="mid_range")
if new3:
    PAIR(prod3, "BBQ baby back ribs with smoky chipotle glaze", "complement", "classic", "main", "Bold, jammy California Zinfandel and smoked, charred ribs with sweet-spicy BBQ sauce is one of America's great regional pairings")
    PAIR(prod3, "Grilled Italian sausage with peppers and onions", "complement", "classic", "main", "The wine's Italian-American heritage resonates perfectly with this classic California tailgate and Italian-American combination")
    PAIR(prod3, "Slow-cooked beef brisket with chimichurri", "complement", "established", "main", "Spiced, jammy Zinfandel and slow-smoked brisket with herbal chimichurri — bold, warm, and completely satisfying")
    PAIR(prod3, "Aged Tillamook cheddar with fig jam", "bridge", "suggested", "cheese", "The wine's jammy fruit and spice bridges with sharp Pacific Northwest cheddar and sweet fig preserves")

p4 = P("Navarro Vineyards", "USA", r2, "winery",
        "A beloved Mendocino family estate primarily known for their Anderson Valley Pinot Noir and Gewurztraminer, Navarro also produces excellent county-wide wines and is famous for their non-alcoholic grape juices. The family's commitment to quality and direct-to-consumer sales has made them one of California's most admired small producers for over four decades.")
prod4, new4 = PROD("Navarro Vineyards Methode a l'Ancienne Pinot Noir Mendocino", "wine_still", p4, r2, "USA",
    subcategory="Pinot Noir",
    description="Traditional-method Anderson Valley Pinot Noir from one of California's most beloved family estates; elegant, aromatic, and cool-climate with red cherry, dried rose, and earthy mineral — Mendocino's benchmark Pinot",
    price_tier="mid_range")
if new4:
    PAIR(prod4, "Roasted salmon fillet with pinot reduction and wild mushrooms", "complement", "classic", "main", "The classic California pairing: cool-climate Pinot Noir and Pacific wild salmon with mushroom — elegant and perfectly matched")
    PAIR(prod4, "Duck breast with cherry compote and roasted beet", "complement", "established", "main", "Aromatic, cherry-fruited Mendocino Pinot with duck and cherry sauce is a natural California fine dining combination")
    PAIR(prod4, "Grilled chanterelles on toast with thyme butter", "complement", "established", "starter", "The wine's earthy, forest-floor quality resonates with Pacific coast chanterelles in a simple but elegant preparation")
    PAIR(prod4, "Point Reyes blue cheese with honeycomb and walnuts", "contrast", "suggested", "cheese", "The wine's delicate red fruit and mineral provide a refined contrast to California's finest blue cheese")

# ── 3. KAMPTAL (already exists!) — let's do PRIORAT vs done
# Let's do: STELLENBOSCH sub-appellations? No, Stellenbosch exists
# Let's do: CRETE DOC already exists
# VINHO VERDE DOC exists
# Let's do: RIBEIRO (already exists)
# GALICIA: Let's do RIBEIRO exists, VALDEORRAS exists
# Actually: Let's do GRAN CANARIA or TENERIFE (Tenerife exists)
# Let's do: Bierzo DO already exists, BIERZO is there
# Let's go with DURIENSE / DOURO WHITE as distinct sub-region? No, Douro exists.

# New choice: Let's do MOUNT ETNA (Etna DOC) already exists
# Let's do FRASCATI or CASTELLI ROMANI (Lazio)
# Or: WEST CAPE (South Africa) – generic but Walker Bay etc are there
# Let's do CANNONAU DI SARDEGNA already exists

# Good new options:
# - Frascati DOC (Lazio, Italy) — Rome's wine; Grechetto + Malvasia; historic
# - Picolit (Friuli, Italy) — Rare, prestigious Italian dessert wine
# - Cassis (already added!)
# - Lirac (already added!)

# Let me do: TRENTINO (separate from Trento DOC) as still wine region
# OR: COLLI ORIENTALI DEL FRIULI — Ribolla Gialla, Tocai Friulano, Refosco
# OR: COTES DE PROVENCE — Provence rose heartland; not in DB as specific DO

print("\n=== Cotes de Provence (France) ===")
r3 = R("Cotes de Provence", "France", "wine",
       designation_type="AOC",
       designation_name="Cotes de Provence AOC",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The world's most celebrated rose wine appellation and France's largest AOC by production. Cotes de Provence produces over 80% rose from Grenache, Cinsault, Syrah, and Mourvedre on diverse Provencal terroirs — from coastal limestone to inland granite and clay. The iconic pale salmon pink style (Gris de Gris) defines the international perception of dry rose wine. Also produces underrated whites and reds.",
       key_producers="Domaine Ott, Chateau Miraval, Sacha Lichine Whispering Angel, Chateau d'Esclans, Domaine de Triennes",
       historical_context="Provence is the world's oldest wine region in France, with Greek settlers planting vines around Massalia (Marseille) around 600 BC. Rose wine has been produced here since antiquity. The modern Cotes de Provence AOC was created in 1977, and the region's global rose boom was ignited in the early 2000s when Sacha Lichine created Whispering Angel at Chateau d'Esclans, transforming pale Provence rose into an international luxury lifestyle symbol.")

VIN(r3, 2023, "excellent", "rising", "Outstanding Provence growing season; rose of exceptional freshness, aromatic lift, and pale colour")
VIN(r3, 2022, "very_good", "rising", "Very good vintage; consistent pale, mineral rose with the characteristic Provence elegance")
VIN(r3, 2021, "good", "stable", "Cooler Mediterranean year; wines of good freshness and bright strawberry-citrus character")
VIN(r3, 2020, "excellent", "rising", "Benchmark rose vintage; finest Cotes de Provence in a generation at all quality levels")
VIN(r3, 2019, "very_good", "stable", "Classic pale rose character across the appellation; fresh, aromatic, and food-friendly")

p5 = P("Domaine Ott", "France", r3, "winery",
        "The most iconic name in Provence rose production, Domaine Ott's distinctive clay amphora-shaped bottles have graced the tables of the French Riviera since 1912. The Ott estates — particularly Clos Mireille and Chateau Romassan — produce Provence rose of benchmark quality and complexity, often with more structure and aging potential than comparable wines.")
prod5, new5 = PROD("Domaine Ott Clos Mireille Rose Cotes de Provence AOC", "wine_still", p5, r3, "France",
    subcategory="Grenache Cinsault Syrah",
    description="Provence's most iconic coastal rose; pale salmon, silky, and mineral from the seaside Clos Mireille estate — wild strawberry, citrus, garrigue, and a saline mineral finish characteristic of the limestone coastal terroir",
    price_tier="premium")
if new5:
    PAIR(prod5, "Whole grilled loup de mer (sea bass) with fennel and pastis", "complement", "classic", "main", "The wine's saline mineral character and fennel-herb notes are the definitive French Riviera pairing for grilled whole sea bass")
    PAIR(prod5, "Tuna Nicoise salad with quail eggs and anchovy", "complement", "classic", "main", "Pale Provence rose and Salad Nicoise is one of France's most perfect warm-weather lunch combinations — inseparable")
    PAIR(prod5, "Bouillabaisse with rouille and grilled croutons", "complement", "classic", "main", "The great Marseille fish stew and the great Provence rose — the Riviera's most celebrated food and wine pairing")
    PAIR(prod5, "Ratatouille with fresh basil and Provencal olive oil", "complement", "classic", "main", "Fresh, herbal Provence rose mirrors the sun-drenched vegetables of ratatouille in the most summery of pairings")

p6 = P("Chateau d'Esclans Whispering Angel", "France", r3, "winery",
        "The estate that transformed Provence rose from a local table wine to a global luxury phenomenon. Sacha Lichine's Whispering Angel became the world's most recognised rose wine brand, demonstrating that pale, elegant Provence rose could command premium prices internationally and inspiring a generation of rose producers worldwide.")
prod6, new6 = PROD("Whispering Angel Rose Cotes de Provence AOC", "wine_still", p6, r3, "France",
    subcategory="Grenache Cinsault Vermentino",
    description="The world's most recognised Provence rose; the wine that made pale dry rose a global lifestyle symbol — elegant, pale salmon with fresh strawberry, white peach, and a mineral finish that has defined a generation",
    price_tier="mid_range")
if new6:
    PAIR(prod6, "Grilled langoustines with Provence herb butter", "complement", "classic", "main", "The world's most Instagrammed rose with the French Riviera's most photogenic crustacean — pale, mineral, and perfectly matched")
    PAIR(prod6, "Charcuterie board with melon, figs, and fresh mozzarella", "complement", "classic", "starter", "Fresh, pale rose and a Mediterranean antipasto spread — the definitive Riviera terrace aperitif combination")
    PAIR(prod6, "Pizza Margherita with fresh basil", "complement", "established", "main", "Pale Provence rose and fresh Margherita pizza — deceptively simple; the wine's acidity cuts through the cheese beautifully")
    PAIR(prod6, "Grilled peaches with fresh ricotta and honey", "complement", "suggested", "dessert", "The wine's fresh peach and strawberry notes create a naturally harmonious match with warm grilled peaches and cream")

# ── 4. KAMPTAL already exists. Let's do COLLI ORIENTALI DEL FRIULI (Italy)
print("\n=== Colli Orientali del Friuli (Italy) ===")
r4 = R("Colli Orientali del Friuli", "Italy", "wine",
       designation_type="DOC",
       designation_name="Colli Orientali del Friuli DOC",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="One of Italy's most important and underrated wine regions, in the hills near Udine and the Slovenian border. Colli Orientali produces some of Italy's finest indigenous white wines: Friulano (formerly Tocai), Ribolla Gialla, Malvasia Istriana, and Ramandolo (DOCG sweet Verduzzo). The amber/orange wine movement was pioneered here by Josko Gravner, Stanko Radikon, and Dario Princic, transforming the region's international reputation for Friulano and Ribolla Gialla.",
       key_producers="Josko Gravner, Radikon, Dorigo, Ronco del Gnemiz, Livio Felluga, Moschioni",
       historical_context="The Colli Orientali's winemaking history is deeply intertwined with Slovenia — the region was part of the Austro-Hungarian Empire and later split between Italy and Yugoslavia. The great estates of the Collio and Colli Orientali developed a tradition of varietal whites that were considered Italy's finest in the 1970s-80s. The amber wine revolution of the 1990s — led by Josko Gravner who abandoned modern white winemaking for Georgian-style skin contact and amphorae — transformed the region's global reputation.")

VIN(r4, 2023, "excellent", "rising", "Excellent Friuli growing season; Ribolla Gialla and Friulano of exceptional mineral precision")
VIN(r4, 2022, "very_good", "rising", "Very good vintage; skin-contact Ribolla Gialla and conventional Friulano both exceptional")
VIN(r4, 2021, "good", "stable", "Good structure across the region; amber wine producers particularly rewarded with fine tannin extraction")
VIN(r4, 2020, "very_good", "stable", "Warm season; conventional whites of good concentration and amber wines of unusual depth")
VIN(r4, 2019, "excellent", "rising", "Benchmark Friuli vintage; finest Colli Orientali wines in recent memory across all styles")

p7 = P("Radikon", "Italy", r4, "winery",
        "One of the pioneering producers of the orange/amber wine movement, Stanislao Radikon produces some of the world's most intensely characterful skin-contact Ribolla Gialla and Oslavje blend from the Oslavia area of the Colli Orientali. Radikon's wines age for extraordinary periods and have become collectors' items in the natural wine world.")
prod7, new7 = PROD("Radikon Ribolla Gialla Colli Orientali del Friuli", "wine_still", p7, r4, "Italy",
    subcategory="Ribolla Gialla",
    description="Pioneer skin-contact Ribolla Gialla from Oslavia; amber-golden with extended maceration — dried apricot, chamomile, walnut, and tannin on white wine; a world-defining expression of what Italian wine can be",
    price_tier="premium")
if new7:
    PAIR(prod7, "Smoked swordfish carpaccio with capers and lemon", "complement", "established", "starter", "The wine's tannin and amber fruit frame the smokiness and ocean richness of cured fish with acidic garnish")
    PAIR(prod7, "Aged Montasio cheese with speck and wild honey", "complement", "classic", "cheese", "Skin-contact Ribolla's tannin and oxidative notes are a natural match for aged Friulian cheese with smoked ham and honey")
    PAIR(prod7, "Sarde in saor (sweet and sour Venetian sardines)", "complement", "established", "starter", "The wine's apricot, chamomile, and tannic structure handle the sweet-sour sardine preparation with ease")
    PAIR(prod7, "Ribollita (Tuscan bread and vegetable soup)", "complement", "adventurous", "main", "The wine's earthiness and bitter herb note creates an unexpected but compelling match with the thick Tuscan peasant soup")

p8 = P("Livio Felluga", "Italy", r4, "winery",
        "The grande dame of Friuli winemaking, Livio Felluga built his estate over 70 years into one of Italy's most respected wine producers. Their Terre Alte blend (Friulano, Pinot Bianco, Sauvignon) is one of Italy's great white wines, while the estate's Friulano and Ribolla Gialla are considered benchmark expressions of the Colli Orientali's conventional style at its best.")
prod8, new8 = PROD("Livio Felluga Terre Alte Colli Orientali del Friuli", "wine_still", p8, r4, "Italy",
    subcategory="Friulano Pinot Bianco Sauvignon",
    description="Flagship Friuli white blend; complex, mineral, and age-worthy with white peach, lemon cream, almond, and a long chalky mineral finish — one of Italy's landmark white wine expressions",
    price_tier="premium")
if new8:
    PAIR(prod8, "Risotto al branzino con capesante (risotto with sea bass and scallops)", "complement", "established", "main", "Complex, mineral Friuli white holds up to the richness of seafood risotto with the wine's acidity and structure providing the frame")
    PAIR(prod8, "Vitello tonnato (cold veal with tuna sauce) — Friulian style", "complement", "classic", "main", "A different but equally classic match: Friuli's most complex white with this Piemontese classic, beloved throughout northern Italy")
    PAIR(prod8, "San Daniele prosciutto with figs and Friulian olive oil", "complement", "classic", "starter", "The wine's almond and mineral precision is the ideal complement for Italy's most prized cured ham with sweet figs")
    PAIR(prod8, "Aged Latteria cheese with walnut and pear", "bridge", "established", "cheese", "The wine's almond-mineral complexity bridges naturally with the sweet-nutty aged Friulian cow's milk cheese")

# ── 5. KAMPTAL already exists; let's do SONOMA COAST as distinct from Sonoma County
print("\n=== Sonoma Coast (USA) ===")
r5 = R("Sonoma Coast AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Sonoma Coast AVA",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The vast, diverse AVA stretching from the Petaluma Wind Gap to the Mendocino County line along California's Pacific coast. The true Sonoma Coast — the far western coastal ridges and canyons — is among California's coolest Pinot Noir and Chardonnay territory. Fog, wind, and proximity to the Pacific Ocean create Burgundian conditions that produce wines of extraordinary precision, mineral complexity, and aging potential, challenging the Willamette Valley for America's finest Pinot Noir.",
       key_producers="Hirsch Vineyards, Flowers Vineyard, Marcassin, Fort Ross-Seaview, Peay Vineyards",
       historical_context="Sonoma Coast viticulture was long dominated by the valley floor regions. The far coast — on steep ridgelines above the fog line facing the Pacific — was planted beginning in the 1980s by pioneering growers who saw the potential for cool-climate Burgundian varieties. Hirsch Vineyards (1980), Littorai, and Flowers established that the true coast could produce some of California's most complex and age-worthy Pinot Noir, transforming the Sonoma Coast's global reputation.")

VIN(r5, 2023, "excellent", "rising", "Outstanding cool Pacific season; Hirsch and Fort Ross Pinot Noir of exceptional mineral precision and longevity")
VIN(r5, 2022, "very_good", "rising", "Very good vintage; coastal Pinot of great elegance and the characteristic coastal salinity and herb")
VIN(r5, 2021, "good", "stable", "Smoke-affected growing season; true coastal sites above the fog mostly spared; clean, elegant wines")
VIN(r5, 2020, "good", "stable", "Challenging wildfire year; best coastal vineyards showed resilience with characteristic minerality")
VIN(r5, 2019, "excellent", "rising", "Benchmark Sonoma Coast vintage; greatest coastal Pinot Noir in recent memory")

p9 = P("Hirsch Vineyards", "USA", r5, "winery",
        "The defining estate of the true Sonoma Coast, Hirsch Vineyards perches on ridges above Fort Ross with a direct view of the Pacific. David Hirsch planted his vineyards in 1980 and has farmed them biodynamically for decades. Wines from Hirsch achieve extraordinary mineral precision, coastal herb character, and aging potential that places them among California's greatest.")
prod9, new9 = PROD("Hirsch Vineyards Estate Pinot Noir Sonoma Coast", "wine_still", p9, r5, "USA",
    subcategory="Pinot Noir",
    description="California's most compelling coastal Pinot Noir; Hirsch Estate from Pacific ridge vineyards — red cherry, sea salt, Sonoma coastal herbs, and a long saline-mineral finish that develops extraordinary complexity with age",
    price_tier="ultra_premium")
if new9:
    PAIR(prod9, "Dungeness crab with drawn butter and sourdough", "complement", "established", "main", "The wine's coastal salinity and red cherry precision find an unexpected and compelling match with Pacific Dungeness crab")
    PAIR(prod9, "Roasted wild king salmon with beet and herb oil", "complement", "classic", "main", "California coastal Pinot Noir and wild Pacific salmon — one of the West Coast's most celebrated food-wine pairings")
    PAIR(prod9, "Duck confit with wild Pacific mushrooms and truffle oil", "complement", "classic", "main", "The wine's mineral complexity and herb character perfectly frame the earthy richness of duck confit with Pacific mushrooms")
    PAIR(prod9, "Aged Cowgirl Creamery Mt. Tam triple cream with honeycomb", "bridge", "suggested", "cheese", "The wine's coastal mineral and red fruit bridge with the indulgent richness of California's finest artisan triple cream")

p10 = P("Flowers Vineyard and Winery", "USA", r5, "winery",
         "One of the pioneering estates of the true Sonoma Coast, Flowers Vineyard produces Chardonnay and Pinot Noir from some of California's most wind-swept, fog-prone Pacific hillside sites. Their Camp Meeting Ridge and Andreen-Gale Coves Pinot Noir are considered benchmarks for the region's cool-climate, mineral precision.")
prod10, new10 = PROD("Flowers Vineyard Camp Meeting Ridge Pinot Noir Sonoma Coast", "wine_still", p10, r5, "USA",
    subcategory="Pinot Noir",
    description="Benchmark true Sonoma Coast Pinot Noir from Pacific ridgeline vines at Camp Meeting Ridge; complex and mineral with coastal herbs, red cherry, dried rose, and a saline precision that rivals Burgundy Premier Cru",
    price_tier="ultra_premium")
if new10:
    PAIR(prod10, "Seared wild Oregon halibut with herb gremolata", "complement", "established", "main", "Mineral, precise coastal Pinot with firm Pacific halibut and herb gremolata — refined California coastal dining at its best")
    PAIR(prod10, "Grilled quail with wild blackberry and thyme", "complement", "classic", "main", "The wine's red berry and herb complexity resonates with the delicacy of quail and wild blackberry in a California wine country preparation")
    PAIR(prod10, "Mushroom and leek tart with aged Gruyere", "complement", "established", "main", "Earthy, mineral Pinot with the richness of mushroom, leek, and aged cheese in a classic savory tart")
    PAIR(prod10, "Point Reyes Original Blue with Black Mission figs", "contrast", "established", "cheese", "The wine's red fruit and coastal mineral provide elegant contrast to the distinctive saltiness of California's finest blue cheese")

# ── COUNTS ───────────────────────────────────────────────────────────────────
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
