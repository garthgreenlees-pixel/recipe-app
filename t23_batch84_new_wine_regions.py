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

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Barossa Valley ─────────────────────────────────────────────────
print("\n=== Region 1: Barossa Valley ===")
r1 = R("Barossa Valley", "Australia", "wine",
    designation_type="GI",
    designation_name="Barossa Valley GI",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Australia's most famous wine valley, 60km north of Adelaide, producing the world's greatest old-vine Shiraz from vineyards planted by Silesian settlers in the 1840s. The warm, dry climate and ancient soils — ironstone, red clay, and sandy alluvium — produce wines of extraordinary concentration, richness, and depth. The Barossa is also home to the world's largest collection of pre-phylloxera Grenache and Mourvèdre.",
    key_producers="Penfolds, Henschke, Torbreck, Yalumba, Two Hands",
    historical_context="Silesian Lutheran immigrants settled the Barossa in 1842, planting the vine cuttings they brought from Germany; these same vines survived phylloxera because of South Australia's sandy soils and strict quarantine, making the Barossa a living museum of 19th-century viticulture.")

for yr, qd, pt in [
    (2022, "very_good", "stable"), (2021, "excellent", "rising"),
    (2020, "excellent", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Henschke", "winery", r1, "Australia",
    production_philosophy="biodynamic",
    philosophy_description="Stephen and Prue Henschke steward Hill of Grace — a single-vineyard Shiraz from 1860s-planted vines that rivals Penfolds Grange as Australia's most celebrated wine. Biodynamic practices preserve the extraordinary old Silesian vine heritage.",
    reputation_narrative="Hill of Grace is Australia's Holy Grail wine; the estate is also South Australia's most admired family winery for breadth and quality.",
    price_positioning="ultra_premium")

prod1b_id = P("Torbreck Vintners", "winery", r1, "Australia",
    production_philosophy="terroir_focused",
    philosophy_description="Dave Powell's Torbreck pioneered the old-vine Barossa Grenache, Shiraz, Mourvèdre movement — RunRig is among Australia's most acclaimed wines, crafted from vine parcels averaging over 100 years of age.",
    reputation_narrative="Torbreck transformed international perception of Barossa old-vine wines; RunRig is consistently among Australia's top 10.",
    price_positioning="ultra_premium")

prod1a, new1a = PROD("Henschke Hill of Grace Shiraz", "wine_still", prod1a_id, r1, "Australia",
    subcategory="Shiraz",
    description="From the Gnadenberg vineyard in Eden Valley — Shiraz vines planted in the 1860s by Silesian settlers produce one of Australia's most profound and collectible wines. Complex, restrained, and age-worthy with violet, dark chocolate, and iron-mineral depth.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Slow-roasted lamb shoulder with Middle Eastern spices and pomegranate", "complement", "classic", "main",
         "Hill of Grace's structured Shiraz finds its match in spiced slow-roasted lamb — complexity meeting complexity.")
    PAIR(prod1a, "Venison loin with smoked beetroot and blackberry reduction", "complement", "established", "main",
         "Old-vine depth and tannin structure frame game with dark berry accompaniments in a powerful pairing.")
    PAIR(prod1a, "Aged Cheddar with black pepper and chutney", "complement", "established", "cheese",
         "Old-vine Barossa Shiraz's ripe fruit and firm tannin handle an aged sharp Cheddar with authority.")
    PAIR(prod1a, "Dark chocolate ganache tart with salt flakes", "complement", "adventurous", "dessert",
         "Australian Shiraz's dark chocolate note meets its match — sea salt amplifies both wine and chocolate.")

prod1b, new1b = PROD("Torbreck RunRig", "wine_still", prod1b_id, r1, "Australia",
    subcategory="Shiraz-Viognier",
    description="A tiny proportion of Viognier co-fermented with old-vine Barossa Shiraz — RunRig's Rhône-inspired approach produces extraordinary aromatic lift and violet intensity overlaid on massive, velvety concentration from ancient vine material.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "BBQ beef brisket with hickory smoke and molasses glaze", "complement", "classic", "main",
         "RunRig's massive richness and dark-fruit concentration match the intensity of long-smoked brisket.")
    PAIR(prod1b, "Roasted duck with cherry and five-spice", "bridge", "established", "main",
         "Viognier's aromatic lift and cherry fruit in the wine mirror the five-spice duck preparation.")
    PAIR(prod1b, "Kangaroo fillet with macadamia crust and bush tomato chutney", "complement", "adventurous", "main",
         "Indigenous Australian game with Australian old-vine Shiraz — a native terroir pairing of remarkable resonance.")
    PAIR(prod1b, "Stilton with port-soaked figs", "complement", "established", "cheese",
         "Blue cheese's bold salt and the fig's sweetness bridge with RunRig's fruit concentration and tannin.")

# ── Region 2: McLaren Vale ───────────────────────────────────────────────────
print("\n=== Region 2: McLaren Vale ===")
r2 = R("McLaren Vale", "Australia", "wine",
    designation_type="GI",
    designation_name="McLaren Vale GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="South Australia's most diverse wine region, a crescent of vineyards south of Adelaide between the Mount Lofty Ranges and the Gulf St. Vincent. The Mediterranean climate, ancient soils (kangaroo paw ironstone, sand over clay), and maritime influence produce Shiraz, Grenache, and Cabernet Sauvignon of extraordinary depth and mineral character. McLaren Vale is leading Australia's sustainable viticulture revolution.",
    key_producers="d'Arenberg, Wirra Wirra, Coriole, Clarendon Hills, Yangarra",
    historical_context="Vines first planted in 1838 by John Reynell at Chateau Reynella, now one of Australia's oldest continuously operating wineries; the region was a bulk wine source until the 1980s quality revolution led by Chester Osborn of d'Arenberg.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Clarendon Hills", "winery", r2, "Australia",
    production_philosophy="terroir_focused",
    philosophy_description="Roman Bratasiuk's single-vineyard wines from ancient Grenache, Syrah, and Cabernet vines represent McLaren Vale's most ambitious terroir project — each vineyard bottled separately to show the valley's extraordinary soil diversity.",
    reputation_narrative="McLaren Vale's most internationally acclaimed estate for single-vineyard wine precision; Astralis Syrah is among Australia's greatest.",
    price_positioning="ultra_premium")

prod2b_id = P("Yangarra Estate", "winery", r2, "Australia",
    production_philosophy="biodynamic",
    philosophy_description="Yangarra Estate focuses exclusively on Grenache and Rhône varieties from certified biodynamic old vines — their High Sands Grenache from 75-year-old bush vines on ancient sandy soil is one of Australia's most distinctive wines.",
    reputation_narrative="The benchmark estate for McLaren Vale Grenache; international recognition growing significantly since 2015.",
    price_positioning="premium")

prod2a, new2a = PROD("Clarendon Hills Astralis Syrah", "wine_still", prod2a_id, r2, "Australia",
    subcategory="Syrah",
    description="A single-vineyard Syrah from 1920s-planted bush vines on ancient red clay — McLaren Vale's most prestigious wine, combining extraordinary old-vine concentration with Clarendon's distinctive mineral character and age worthiness.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Slow-roasted Wagyu short rib with black garlic and roasted bones", "complement", "classic", "main",
         "Astralis's massive concentration and tannin structure meet Wagyu's extraordinary fat and umami with ease.")
    PAIR(prod2a, "Barbecued lamb ribs with harissa and preserved lemon", "complement", "established", "main",
         "North African spiced lamb with McLaren Vale Syrah — the aromatic spice complexity of both align.")
    PAIR(prod2a, "Chocolate lava cake with Morello cherry and vanilla cream", "complement", "adventurous", "dessert",
         "Astralis's dark chocolate and cherry character mirrors this dessert in an unexpected but compelling alignment.")
    PAIR(prod2a, "Montgomery Cheddar with quince paste and walnuts", "complement", "established", "cheese",
         "Aged Cheddar's depth and the wine's power are equals — quince bridges both with its aromatic sweetness.")

prod2b, new2b = PROD("Yangarra High Sands Grenache", "wine_still", prod2b_id, r2, "Australia",
    subcategory="Grenache",
    description="From 75-year-old bush vines on ancient sandy soil — an extraordinary Australian Grenache of great purity, red-fruit delicacy, and savoury depth, more Burgundian in texture than many expect from the Barossa region.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Roasted spatchcock with herb butter and jus", "complement", "established", "main",
         "High Sands' silky texture and red-fruit delicacy match roasted poultry in a light-handed luxury pairing.")
    PAIR(prod2b, "Lamb sweetbreads with capers and lemon-herb butter", "complement", "established", "main",
         "Delicate offal with silky old-vine Grenache — both light enough that neither overwhelms the other.")
    PAIR(prod2b, "Char-grilled octopus with romesco and sherry vinegar", "bridge", "adventurous", "starter",
         "Mediterranean flavour vocabulary with an Australian Grenache sharing Iberian varietal roots.")
    PAIR(prod2b, "Aged goat's cheese with roasted red pepper and pine nuts", "complement", "established", "cheese",
         "Grenache's red-fruit character and the roasted pepper's sweetness bridge through the goat's cheese tang.")

# ── Region 3: Clare Valley ───────────────────────────────────────────────────
print("\n=== Region 3: Clare Valley ===")
r3 = R("Clare Valley", "Australia", "wine",
    designation_type="GI",
    designation_name="Clare Valley GI",
    reputation_tier="respected",
    quality_trajectory="established",
    description="South Australia's most isolated and elevated wine valley, 130km north of Adelaide, producing Australia's most celebrated Riesling — defined by bone-dry, lime-accented wines with extraordinary aging potential. The valley's altitude moderates the continental climate; limestone and slate soils give the wines a distinctive mineral character. Clare Valley producers pioneered the screwcap closure for fine wine in Australia.",
    key_producers="Grosset, Kilikanoon, Jim Barry, Knappstein, Tim Adams",
    historical_context="Jesuit missionaries planted the first vines at Sevenhill in 1851; the valley remained primarily a Riesling producer while most of South Australia chased red wine fame — this isolation preserved Clare's Riesling heritage through the bulk wine era.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "very_good", "stable"),
    (2021, "excellent", "stable"), (2020, "very_good", "stable"), (2019, "excellent", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Grosset Wines", "winery", r3, "Australia",
    production_philosophy="terroir_focused",
    philosophy_description="Jeffrey Grosset is Australia's Riesling master — his Polish Hill and Watervale Rieslings are the benchmarks of Clare Valley, combining extreme precision, lime-zest character, and a mineral austerity that softens magnificently over decades.",
    reputation_narrative="Australia's most decorated Riesling producer; Polish Hill is routinely rated among the world's top 20 Rieslings.",
    price_positioning="premium")

prod3b_id = P("Jim Barry Wines", "winery", r3, "Australia",
    production_philosophy="traditional",
    philosophy_description="The Barry family has shaped Clare Valley's identity for 60 years — their flagship The Armagh Shiraz and Lodge Hill Riesling are benchmarks of the valley's breadth, from Riesling minerality to old-vine Shiraz concentration.",
    reputation_narrative="One of Clare Valley's founding families; The Armagh is a hallmark Australian Shiraz of collector status.",
    price_positioning="premium")

prod3a, new3a = PROD("Grosset Polish Hill Riesling", "wine_still", prod3a_id, r3, "Australia",
    subcategory="Riesling",
    description="From the rocky, slate-rich Polish Hill sub-region — Grosset's most mineral and austere Riesling, produced from low-yielding vines on ancient slate soils. Bone dry, with lime, flint, and exceptional aging potential; a benchmark for Australian Riesling.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Freshly shucked Pacific oysters with mignonette", "cleanse", "classic", "aperitif",
         "Bone-dry Riesling's citrus and mineral cut through oyster brine in the perfect aperitif pairing.")
    PAIR(prod3a, "Crispy whole snapper with green chilli, lime, and ginger", "complement", "established", "main",
         "Clare Valley Riesling's lime and acidity were born for Asian-influenced seafood preparations.")
    PAIR(prod3a, "Vietnamese-style tiger prawns with lemongrass and vermicelli", "complement", "established", "main",
         "Lime, lemongrass, and chilli in the dish echo Polish Hill's citrus and mineral character.")
    PAIR(prod3a, "Goat's cheese tart with herb crust and preserved lemon", "complement", "established", "starter",
         "Riesling's acidity and citrus amplify goat's cheese's tang while the lemon bridges both.")

prod3b, new3b = PROD("Jim Barry The Armagh Shiraz", "wine_still", prod3b_id, r3, "Australia",
    subcategory="Shiraz",
    description="A Clare Valley icon from a single 17-hectare vineyard planted in 1968 — old-vine Shiraz of extraordinary depth, combining eucalyptus, dark olive, dark chocolate, and ironstone mineral notes with decades of aging potential.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Wagyu beef fillet with truffle butter and crispy shallots", "complement", "classic", "main",
         "The Armagh's immense concentration and depth require Wagyu's extraordinary fat content and umami depth.")
    PAIR(prod3b, "Slow-cooked lamb shoulder with North African spice rub", "complement", "established", "main",
         "Eucalyptus and dark olive in the wine echo spiced lamb's aromatic complexity.")
    PAIR(prod3b, "Kangaroo loin with bush tomato chutney and roasted wattleseed", "complement", "adventurous", "main",
         "Australian native ingredients with a classic Clare Valley red — an indigenous terroir pairing.")
    PAIR(prod3b, "Aged Colby cheese with dried figs and toasted macadamia", "complement", "established", "cheese",
         "The Armagh's power handles aged hard cheese; macadamia and fig echo dark fruit and earthy concentration.")

# ── Region 4: Chablis Grand Cru ─────────────────────────────────────────────
print("\n=== Region 4: Chablis Grand Cru ===")
r4 = R("Chablis Grand Cru", "France", "wine",
    designation_type="AOC",
    designation_name="Chablis Grand Cru AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Seven Grand Cru vineyards totalling just 104 hectares on a single south-facing slope above the town of Chablis — Blanchot, Bougros, Les Clos, Grenouilles, Les Preuses, Valmur, and Vaudésir. These produce Chardonnay of unmatched mineral purity, Kimmeridgian limestone-chalk character, and extraordinary longevity. Chablis Grand Cru is the most restrained and mineral expression of Chardonnay in France.",
    key_producers="Raveneau, Dauvissat, William Fèvre, Domaine Billaud-Simon, La Chablisienne",
    historical_context="The Kimmeridgian subsoil — fossilised seabed from the Jurassic era containing tiny oyster shells — gives Chablis its signature saline, flinty character; the Romans planted vines here before the 12th century Cistercians expanded the vineyards.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Domaine François Raveneau", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="Raveneau is the most coveted Chablis domaine — Bernard Raveneau crafts benchmark Les Clos and Valmur Grand Crus alongside exceptional premier crus using large old oak vats that add texture without masking the wines' extraordinary mineral precision.",
    reputation_narrative="The most allocated Chablis domaine in the world; Grand Crus are among Burgundy's most sought-after bottles.",
    price_positioning="ultra_premium")

prod4b_id = P("Domaine René et Vincent Dauvissat", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="The other great Chablis domaine — Vincent Dauvissat produces wines of haunting mineral purity from Les Clos, Les Preuses, and premier cru La Forest, aging in old oak barrels to add minimal texture without fruit expression.",
    reputation_narrative="Paired with Raveneau as Chablis's two unreachable reference estates; Les Clos from Dauvissat is a profound wine.",
    price_positioning="ultra_premium")

prod4a, new4a = PROD("Raveneau Chablis Les Clos Grand Cru", "wine_still", prod4a_id, r4, "France",
    subcategory="Chardonnay",
    description="Les Clos is Chablis's most powerful and age-worthy Grand Cru — Raveneau's version is perhaps the greatest white wine produced anywhere in Burgundy: mineral, saline, austere, and extraordinarily long-lived.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Freshly shucked Belon oysters with frozen Champagne granita", "elevate", "classic", "aperitif",
         "Chablis and oysters is one of wine's transcendent pairings — the wine's Kimmeridgian oyster-fossil terroir reflected in the shellfish.")
    PAIR(prod4a, "Poached turbot with langoustine bisque and caviar", "elevate", "classic", "fish_course",
         "The greatest white fish with the greatest Chablis — bisque and caviar amplify the wine's oceanic mineral depth.")
    PAIR(prod4a, "Steamed sole with beurre blanc and samphire", "complement", "classic", "fish_course",
         "Pure white fish preparation allows Les Clos's mineral character to dominate — samphire echoes the salinity.")
    PAIR(prod4a, "Roasted langoustine with Roscoff onion cream", "complement", "established", "starter",
         "Brittany shellfish with Chablis — both express the same north Atlantic marine mineral vocabulary.")

prod4b, new4b = PROD("Dauvissat Chablis Les Preuses Grand Cru", "wine_still", prod4b_id, r4, "France",
    subcategory="Chardonnay",
    description="Les Preuses is Chablis's most aromatic Grand Cru — Dauvissat's version combines extraordinary floral delicacy with Kimmeridgian minerality; lighter and more feminine than Les Clos but no less profound.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "Crab thermidor with herb gratin and lemon verbena cream", "complement", "classic", "starter",
         "Chablis's citrus and mineral precision lifts rich crab preparation while floral Les Preuses echo the verbena.")
    PAIR(prod4b, "Grilled whole sea bream with fennel and white wine", "complement", "classic", "fish_course",
         "Mediterranean whole fish with northern mineral white — fennel's anise note bridges both beautifully.")
    PAIR(prod4b, "White asparagus velouté with Oscietra caviar", "elevate", "established", "starter",
         "Spring's finest white vegetable with Grand Cru Chablis — caviar's salinity amplifies both.")
    PAIR(prod4b, "Soumaintrain washed-rind cheese with toasted rye", "bridge", "established", "cheese",
         "Burgundian soft cheese with the region's finest white — regional pairing across appellations.")

# ── Region 5: Beaujolais Cru ─────────────────────────────────────────────────
print("\n=== Region 5: Moulin-à-Vent ===")
r5 = R("Moulin-à-Vent", "France", "wine",
    designation_type="AOC",
    designation_name="Moulin-à-Vent AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The most powerful and age-worthy of the ten Beaujolais crus, taking its name from an ancient 15th-century windmill on a granite plateau north of Romanèche-Thorins. Moulin-à-Vent Gamay from manganese-rich granite soils produces wines that age like Burgundy Pinot Noir — developing tertiary complexity, silky tannin, and remarkable elegance over 10-20 years. Often called the 'King of Beaujolais'.",
    key_producers="Château des Jacques, Domaine du Vissoux, Paul Janin, Heitz-Lochardet",
    historical_context="The windmill that names the appellation has stood since the 15th century; the AOC was granted in 1936 as one of Beaujolais's first crus; manganese in the Moulin-à-Vent granite uniquely tames Gamay's wild character.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Château des Jacques", "winery", r5, "France",
    production_philosophy="traditional",
    philosophy_description="Under Louis Jadot ownership since 1996, Château des Jacques applies Burgundian winemaking precision to Moulin-à-Vent — single-vineyard cuvées from Clos du Grand Carquelin, La Roche, and other parcels rival serious premier cru Pinot Noir.",
    reputation_narrative="The reference estate for quality Beaujolais; Louis Jadot's investment transformed perceptions of the cru's aging potential.",
    price_positioning="mid_range")

prod5b_id = P("Domaine du Vissoux", "winery", r5, "France",
    production_philosophy="natural",
    philosophy_description="Pierre-Marie Chermette produces some of Beaujolais's most authentic cru wines using minimal intervention — no added yeasts, no chaptalization, low sulphur — from old-vine Gamay on granite across multiple crus including Moulin-à-Vent.",
    reputation_narrative="One of natural Beaujolais's most respected voices; Vissoux wines have significant following in natural wine circles globally.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Château des Jacques Moulin-à-Vent Clos du Grand Carquelin", "wine_still", prod5a_id, r5, "France",
    subcategory="Gamay",
    description="A single-vineyard Moulin-à-Vent from Burgundian owners — Gamay from the Grand Carquelin parcel treated with Burgundian discipline: full destemming, cold soak, aging in Burgundy barrels. A wine that challenges assumptions about Beaujolais's potential.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Charcuterie board with rosette de Lyon, cornichons, and mustard", "complement", "classic", "casual",
         "The quintessential Lyon bouchon pairing — pork charcuterie with Beaujolais cru is the city's soul.")
    PAIR(prod5a, "Roasted chicken thighs with tarragon and whole garlic", "complement", "classic", "main",
         "Simple roasted chicken with an elegant Beaujolais cru — a timeless French lunch pairing.")
    PAIR(prod5a, "Duck terrine with pistachios and Cumberland sauce", "complement", "established", "starter",
         "Rich terrine with structured Moulin-à-Vent — the wine's aging potential suits the density of duck fat.")
    PAIR(prod5a, "Morbier with its ash line and crusty baguette", "complement", "established", "cheese",
         "The creamy-funky Jura cheese with a structured Beaujolais cru creates a cross-regional French harmony.")

prod5b, new5b = PROD("Domaine du Vissoux Moulin-à-Vent Les Trois Roches", "wine_still", prod5b_id, r5, "France",
    subcategory="Gamay",
    description="Old-vine Moulin-à-Vent from the Les Trois Roches parcel — Chermette's natural approach preserves every nuance of the granite terroir, producing a Gamay of unusual complexity, red-fruit purity, and earthy mineral depth.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Lyonnaise salad with frisée, lardons, and poached egg", "complement", "classic", "starter",
         "The Lyon bouchon's defining dish with a natural Beaujolais cru — a Rhône Valley cultural archetype.")
    PAIR(prod5b, "Rabbit saddle with Dijon mustard and thyme", "complement", "established", "main",
         "Delicate game with light-bodied Gamay — the wine's structure handles rabbit without overpowering.")
    PAIR(prod5b, "Saucisson en croûte with herb crust and grainy mustard", "complement", "established", "main",
         "Beaujolais and saucisson — two Lyon institutions that exist in perfect cultural and culinary alignment.")
    PAIR(prod5b, "Saint-Félicien cheese at room temperature", "complement", "established", "cheese",
         "Soft, creamy Rhône Valley cheese with a natural Beaujolais Gamay — regional harmony at its simplest.")

# ── Counts ────────────────────────────────────────────────────────────────────
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
print("Done.")
cur.close()
conn.close()
