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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
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
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Jura ──────────────────────────────────────────────────────────
print("=== Region 1: Jura ===")
r = R("Jura", "France", "wine",
      designation_type="AOC", designation_name="Jura AOC",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Remote French mountain region producing unique oxidative whites (Vin Jaune), Savagnin, Poulsard and Trousseau; cult natural wine destination.",
      key_producers="Overnoy-Houillon, Domaine Tissot, Ganevat, Château Chalon",
      historical_context="Vin Jaune aged 6 years in barrel without topping up — France's most unique wine; Château Chalon's AC covers only 50 hectares.")
VIN(r, 2020, "exceptional", "rising", "Warm year produced concentrated Vin Jaune and exceptional Savagnin; cellar classics in the making.")
VIN(r, 2019, "excellent", "rising", "Ideal conditions; precise Chardonnay and powerful Vin Jaune.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; generous, early-drinking whites and structured reds.")
VIN(r, 2017, "excellent", "stable", "Classic Jura year; mineral Savagnin and structured Poulsard.")
VIN(r, 2016, "very_good", "stable", "Challenging start; patient growers produced wines of fine balance.")
p1 = P("Domaine Tissot", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Stéphane Tissot's benchmark estate; full biodynamic since 2004; extraordinary range from pét-nat to Vin Jaune; amphora and barrel experiments.",
       reputation_narrative="The face of modern Jura viticulture; Tissot's Vin Jaune and Savagnin set the region's quality standard.",
       price_positioning="mid_range")
p2 = P("Jean-François Ganevat", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Cult natural producer with old-vine Chardonnay and Savagnin parcels; indigenous yeasts only; minimal sulphur; pét-nat pioneer.",
       reputation_narrative="Among the world's most sought-after natural wine producers; single-parcel bottlings of extraordinary character.",
       price_positioning="premium")
pr1, n1 = PROD("Tissot Vin Jaune Arbois", "wine_still", p1, r, "France",
               subcategory="Savagnin", price_tier="premium",
               description="Classic oxidative Vin Jaune; walnut, curry leaf, dry sherry, saffron and extraordinary persistence; ages for 50+ years.")
if n1:
    PAIR(pr1, "Comté aged 36 months with toasted walnuts", "complement", "classic", "cheese", "The iconic Jura pairing; oxidative wine mirrors aged Comté's nutty complexity perfectly.")
    PAIR(pr1, "Poulet aux morilles (chicken with morel cream)", "complement", "classic", "main", "Regional classic; oxidative weight matches cream sauce; morel bridges earthy register.")
    PAIR(pr1, "Braised sweetbreads with vin jaune reduction", "complement", "established", "main", "Wine and sauce echo each other; richness balanced by oxidative bite.")
    PAIR(pr1, "Fried curry-spiced cauliflower", "complement", "suggested", "starter", "Curry spice in wine resonates with actual curry; both share turmeric-saffron register.")
pr2, n2 = PROD("Ganevat Julien en Chalasse Chardonnay", "wine_still", p2, r, "France",
               subcategory="Chardonnay", price_tier="premium",
               description="Old-vine Chardonnay from Jura limestone; reductive and precise — wet stone, lemon curd, white truffle; vinified without sulphur.")
if n2:
    PAIR(pr2, "Slow-poached halibut with beurre blanc", "complement", "established", "fish_course", "Mineral precision and citrus notes elevate delicate halibut; butter sauce echoes wine's texture.")
    PAIR(pr2, "White truffle tagliatelle", "complement", "established", "main", "White truffle in wine mirrors real truffle; old-vine depth matches luxury ingredient.")
    PAIR(pr2, "Goat's cheese with fresh herbs and honey", "complement", "suggested", "cheese", "Limestone minerality and lemon acidity cut goat's cheese tang; honey bridges sweetness.")
    PAIR(pr2, "Seared scallops with pea purée and lardo", "elevate", "adventurous", "starter", "Natural wine's complexity elevates scallop's sweetness; lardo bridges richness.")

# ── Region 2: Châteauneuf-du-Pape ────────────────────────────────────────────
print("=== Region 2: Châteauneuf-du-Pape ===")
r = R("Châteauneuf-du-Pape", "France", "wine",
      designation_type="AOC", designation_name="Châteauneuf-du-Pape AOC",
      reputation_tier="iconic", quality_trajectory="established",
      description="Southern Rhône valley's most prestigious appellation; galets roulés (rounded stones) retain heat; Grenache-dominant blends of extraordinary concentration.",
      key_producers="Château Rayas, Château Beaucastel, Château Pégau, Vieux Télégraphe",
      historical_context="Popes of Avignon made wine here in the 14th century; France's first AOC laws drafted in 1923 by Baron Le Roy of Château Fortia.")
VIN(r, 2021, "excellent", "rising", "Cooler year; elegant, aromatic Grenache with fine tannins and aging potential.")
VIN(r, 2020, "exceptional", "rising", "Benchmark vintage; powerful yet balanced Grenache of extraordinary depth.")
VIN(r, 2019, "excellent", "stable", "Rich, concentrated year; wines of great generosity and long aging potential.")
VIN(r, 2018, "very_good", "stable", "Warm but not extreme; plush, accessible style with good depth.")
VIN(r, 2017, "excellent", "stable", "Classic Southern Rhône year; garrigue-scented Grenache in full expression.")
p1 = P("Château Beaucastel", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="The Perrin family's benchmark estate; uses all 13 permitted varieties; biodynamic since 2009; Mourvèdre emphasis sets it apart; Hommage à Jacques Perrin is their icon.",
       reputation_narrative="Châteauneuf's most complex and age-worthy producer; Hommage à Jacques Perrin is among France's greatest wines.",
       price_positioning="premium")
p2 = P("Vieux Télégraphe", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Brunier family estate on La Crau plateau; pure galets roulés terroir; Grenache-dominant blend of classic southern elegance.",
       reputation_narrative="La Crau benchmark; Vieux Télégraphe consistently expresses Châteauneuf's garrigue soul with great refinement.",
       price_positioning="premium")
pr1, n1 = PROD("Château Beaucastel Châteauneuf-du-Pape", "wine_still", p1, r, "France",
               subcategory="Grenache blend", price_tier="premium",
               description="Complex blend of all 13 varieties; Mourvèdre backbone with Grenache opulence; leather, garrigue, dark berry and decades of aging potential.")
if n1:
    PAIR(pr1, "Daube de boeuf Provençal with olives", "complement", "classic", "main", "Regional classic; wine's garrigue and leather echo Provençal herbs and braised beef.")
    PAIR(pr1, "Roast leg of lamb with herbes de Provence", "complement", "classic", "main", "Grenache and Mourvèdre mirror lamb's richness; Provençal herbs amplify garrigue notes.")
    PAIR(pr1, "Wild boar ragù with pappardelle", "complement", "established", "main", "Game depth matches Mourvèdre structure; tannins grip boar fat; herbs bridge.")
    PAIR(pr1, "Aged Manchego with dried figs and almonds", "bridge", "suggested", "cheese", "Leather and dried-fruit notes echo aged cheese; figs and almonds extend fruit register.")
pr2, n2 = PROD("Vieux Télégraphe Châteauneuf-du-Pape La Crau", "wine_still", p2, r, "France",
               subcategory="Grenache blend", price_tier="premium",
               description="La Crau galets roulés expression; Grenache-led with Mourvèdre and Syrah; garrigue, red fruit, kirsch and structured tannins with fine mineral finish.")
if n2:
    PAIR(pr2, "Rack of lamb with olive tapenade crust", "complement", "classic", "main", "Garrigue and olive mirror tapenade crust; Grenache fruit amplifies chargrilled lamb.")
    PAIR(pr2, "Duck confit with cherry and thyme jus", "complement", "established", "main", "Kirsch notes in wine resonate with cherry jus; tannins grip duck fat.")
    PAIR(pr2, "Grilled merguez sausages with harissa", "complement", "suggested", "casual", "Southern heat and spice suit Grenache's warm fruit; garrigue bridges herb notes.")
    PAIR(pr2, "Époisses washed-rind cheese", "contrast", "adventurous", "cheese", "Powerful wine stands up to pungent Époisses; fruit contrast cuts strong dairy.")

# ── Region 3: Finger Lakes ────────────────────────────────────────────────────
print("=== Region 3: Finger Lakes ===")
r = R("Finger Lakes", "USA", "wine",
      designation_type="AVA", designation_name="Finger Lakes AVA",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Deep glacial lakes in upstate New York moderate the harsh continental climate; Riesling of world-class quality alongside Cabernet Franc and hybrid varieties.",
      key_producers="Dr. Konstantin Frank, Ravines Wine Cellars, Boundary Breaks, Red Newt Cellars",
      historical_context="Dr. Konstantin Frank proved vinifera could thrive here in the 1960s; Riesling now rivals Alsace and Mosel in critical esteem.")
VIN(r, 2021, "exceptional", "rising", "Outstanding cool year; Riesling of rare precision and Kabinett-like elegance.")
VIN(r, 2020, "very_good", "stable", "Warm summer with late season cooling; ripe, concentrated Riesling.")
VIN(r, 2019, "excellent", "stable", "Balanced year; classic Finger Lakes Riesling with taut acidity and apple-citrus profile.")
VIN(r, 2018, "good", "stable", "Wet autumn challenged producers; early pickers succeeded; fresh, lighter style.")
VIN(r, 2017, "excellent", "stable", "Dry summer; concentrated Riesling with excellent acid backbone.")
p1 = P("Dr. Konstantin Frank", "winery", r, "USA",
       production_philosophy="traditional",
       philosophy_description="Founded by Ukrainian immigrant who pioneered vinifera in New York; estate vineyards on Keuka Lake; range from bone-dry to TBA-equivalent botrytis wines.",
       reputation_narrative="The founding estate of modern Finger Lakes viticulture; Dry Riesling remains the benchmark against which all others are measured.",
       price_positioning="mid_range")
p2 = P("Ravines Wine Cellars", "winery", r, "USA",
       production_philosophy="terroir_focused",
       philosophy_description="Morten Hallgren (son of Provence winemaker) applies Old World precision to Finger Lakes Riesling; lake-effect site selection; minimal intervention.",
       reputation_narrative="Ravines elevated Finger Lakes Riesling's international profile; Argetsinger Vineyard Riesling is a benchmark of the region.",
       price_positioning="mid_range")
pr1, n1 = PROD("Dr. Konstantin Frank Dry Riesling", "wine_still", p1, r, "USA",
               subcategory="Riesling", price_tier="mid_range",
               description="Bone-dry Finger Lakes Riesling; green apple, lime zest, slate minerality; lean, focused with laser-sharp acidity and long finish.")
if n1:
    PAIR(pr1, "Pan-seared trout with brown butter and herbs", "complement", "classic", "fish_course", "Mineral acidity and citrus echo freshwater trout; brown butter mirrors wine's richness.")
    PAIR(pr1, "Oysters on the half shell", "complement", "established", "aperitif", "Dry minerality amplifies oyster brine; citrus replaces lemon squeeze.")
    PAIR(pr1, "Thai green curry with jasmine rice", "contrast", "established", "main", "Acidity cuts coconut richness; citrus bridges lime in curry; bone-dry resists sweetness.")
    PAIR(pr1, "Smoked whitefish dip with crackers", "complement", "suggested", "aperitif", "Lake-region pairing; minerality and acidity cut smoked fish richness.")
pr2, n2 = PROD("Ravines Argetsinger Vineyard Riesling", "wine_still", p2, r, "USA",
               subcategory="Riesling", price_tier="mid_range",
               description="Single-vineyard Riesling from Seneca Lake; off-dry with piercing acidity; peach, lime, wet slate and a finish of uncommon length.")
if n2:
    PAIR(pr2, "Duck breast with cherry and five-spice", "bridge", "established", "main", "Off-dry Riesling bridges duck fat and fruit sauce; five-spice echoes wine's complexity.")
    PAIR(pr2, "Spiced pork belly with pickled cabbage", "complement", "classic", "main", "German-tradition pairing; residual sugar cuts spice; acidity refreshes pork fat.")
    PAIR(pr2, "Blue cheese and candied walnuts on endive", "contrast", "adventurous", "starter", "Off-dry sweetness contrasts blue cheese funk; acidity cuts rich walnut oil.")
    PAIR(pr2, "Thai papaya salad with lime and fish sauce", "complement", "suggested", "starter", "Citrus and slight sweetness echo salad's lime; acidity bridges fish sauce saltiness.")

# ── Region 4: Swartland ──────────────────────────────────────────────────────
print("=== Region 4: Swartland ===")
r = R("Swartland", "South Africa", "wine",
      designation_type="WO", designation_name="Swartland WO",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Hot, dry wheat and wine country north of Cape Town; dry-farmed old vines of Chenin Blanc, Syrah, Grenache and Carignan on granite and schist; the natural wine heartland of the southern hemisphere.",
      key_producers="Eben Sadie, Mullineux, Porseleinberg, Badenhorst Family",
      historical_context="The Swartland Revolution (2009–) of Eben Sadie and colleagues transformed a bulk-wine region into South Africa's most exciting fine wine destination.")
VIN(r, 2022, "excellent", "rising", "La Niña cooling effect; elegant Chenin and structured Syrah of exceptional freshness.")
VIN(r, 2021, "very_good", "stable", "Hot year; concentrated reds; top Chenin showed focused acidity.")
VIN(r, 2020, "exceptional", "rising", "Benchmark Swartland year; balanced heat; old-vine Chenin of extraordinary depth.")
VIN(r, 2019, "excellent", "stable", "Warm but dry; concentrated reds with good structure; Chenin showed tropical richness.")
VIN(r, 2018, "very_good", "stable", "Good balance; generous Syrah and precise Chenin.")
p1 = P("Mullineux Family Wines", "winery", r, "South Africa",
       production_philosophy="terroir_focused",
       philosophy_description="Chris and Andrea Mullineux champion individual terroir expressions; granite vs schist vs iron series; Syrah and old-vine Chenin are signatures.",
       reputation_narrative="Consistently South Africa's most celebrated estate; Mullineux Syrah and Straw Wine have won multiple Winemaker of the Year titles.",
       price_positioning="premium")
p2 = P("Sadie Family Wines", "winery", r, "South Africa",
       production_philosophy="terroir_focused",
       philosophy_description="Eben Sadie's pioneering old-vine project; Columella (Syrah) and Palladius (white blend) are South Africa's most iconic wines; dry-farmed granite-schist vineyards.",
       reputation_narrative="Eben Sadie's Columella and Palladius put Swartland on the world wine map; benchmark for South African fine wine.",
       price_positioning="premium")
pr1, n1 = PROD("Mullineux Kloof Street Rouge", "wine_still", p1, r, "South Africa",
               subcategory="Syrah blend", price_tier="mid_range",
               description="Swartland entry-level from old-vine Syrah, Grenache and Cinsault; garrigue, red plum, white pepper and a fresh Swartland finish.")
if n1:
    PAIR(pr1, "Braai-grilled lamb chops with boerekos", "complement", "classic", "main", "South African BBQ pairing; Swartland garrigue mirrors flame-char and lamb fat.")
    PAIR(pr1, "Lamb meatballs with North African spices", "complement", "established", "starter", "Cinnamon-cumin spice echoes wine's garrigue; red fruit bridges sweet spice.")
    PAIR(pr1, "Grilled merguez with harissa and couscous", "complement", "suggested", "main", "Red fruit and pepper notes echo harissa heat; Grenache freshness refreshes spice.")
    PAIR(pr1, "Aged Gouda with dried apricots", "bridge", "suggested", "cheese", "Gouda caramel notes echo wine's fruit; dried apricot bridges Rhône-style warmth.")
pr2, n2 = PROD("Sadie Family Palladius", "wine_still", p2, r, "South Africa",
               subcategory="Chenin Blanc blend", price_tier="premium",
               description="Iconic old-vine white blend of Chenin Blanc, Palomino and others; oxidative richness, beeswax, straw, white peach and saline mineral length.")
if n2:
    PAIR(pr2, "Abalone with butter and sea herbs", "complement", "classic", "fish_course", "Mineral salinity mirrors abalone's oceanic depth; oxidative richness matches butter.")
    PAIR(pr2, "Roasted Cape linefish with saffron butter", "complement", "established", "fish_course", "Old-vine complexity elevates delicate fish; saffron bridges wine's straw and spice.")
    PAIR(pr2, "Bone marrow with toasted sourdough and sea salt", "complement", "adventurous", "starter", "Oxidative weight matches marrow richness; saline mineral finish cuts fat.")
    PAIR(pr2, "Aged Parmigiano-Reggiano with aged balsamic", "elevate", "suggested", "cheese", "Oxidative beeswax notes elevate aged parmesan; balsamic bridges sweet-sour complexity.")

# ── Region 5: Hawke's Bay ────────────────────────────────────────────────────
print("=== Region 5: Hawke's Bay ===")
r = R("Hawke's Bay", "New Zealand", "wine",
      designation_type="GI", designation_name="Hawke's Bay GI",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="New Zealand's oldest wine region on the eastern North Island; Gimblett Gravels sub-region is a warm, free-draining gravel bench producing Bordeaux-style reds and Chardonnay.",
      key_producers="Craggy Range, Te Mata Estate, Trinity Hill, Elephant Hill",
      historical_context="Te Mata Estate (est. 1892) is New Zealand's oldest winery; the Gimblett Gravels discovery in the 1980s transformed the region's red wine potential.")
VIN(r, 2022, "exceptional", "rising", "Ideal warm, dry growing season; Gimblett reds of extraordinary depth and structure.")
VIN(r, 2021, "excellent", "stable", "Classic year; Chardonnay of great precision; reds with excellent concentration.")
VIN(r, 2020, "very_good", "stable", "Moderate year; fresh, elegant style; Chardonnay and Syrah excelled.")
VIN(r, 2019, "excellent", "stable", "Warm, dry year; concentrated Bordeaux blends with good structure.")
VIN(r, 2018, "very_good", "stable", "Good balance; approachable reds and textured Chardonnay.")
p1 = P("Craggy Range", "winery", r, "New Zealand",
       production_philosophy="terroir_focused",
       philosophy_description="Premium single-vineyard estate across multiple NZ regions; Sophia (Gimblett Gravels Bordeaux blend) is their icon; meticulous site selection and minimal intervention.",
       reputation_narrative="Craggy Range's Sophia set a new benchmark for New Zealand Bordeaux blends; Terraces Chardonnay rivals top Burgundy.",
       price_positioning="premium")
p2 = P("Te Mata Estate", "winery", r, "New Zealand",
       production_philosophy="traditional",
       philosophy_description="New Zealand's oldest winery (est. 1892); Coleraine is the flagship Cabernet-Merlot; estate vineyards in both Havelock North and Gimblett Gravels.",
       reputation_narrative="Te Mata Coleraine pioneered New Zealand's Bordeaux-blend reputation; among the southern hemisphere's most age-worthy reds.",
       price_positioning="premium")
pr1, n1 = PROD("Craggy Range Sophia Gimblett Gravels", "wine_still", p1, r, "New Zealand",
               subcategory="Cabernet Merlot blend", price_tier="premium",
               description="Icon Bordeaux blend from Gimblett Gravels; Cabernet Sauvignon-led with Merlot and Malbec; cassis, graphite, cedar and fine-grained tannins of great structure.")
if n1:
    PAIR(pr1, "Grilled grass-fed beef fillet with chimichurri", "complement", "classic", "main", "Cassis and graphite mirror beef char; fine tannins grip grass-fed fat; herbs bridge.")
    PAIR(pr1, "Braised short rib with red wine reduction", "complement", "established", "main", "Bordeaux structure matches slow-braised richness; cedar notes echo reduction complexity.")
    PAIR(pr1, "Aged cheddar from Hawke's Bay with quince", "complement", "established", "cheese", "Regional pairing; cassis and cedar echo aged cheddar; quince bridges fruit notes.")
    PAIR(pr1, "Venison loin with blackberry and juniper", "complement", "established", "main", "Game tannin alignment; blackberry echoes cassis; juniper bridges herbal complexity.")
pr2, n2 = PROD("Te Mata Coleraine Cabernet Merlot", "wine_still", p2, r, "New Zealand",
               subcategory="Cabernet Merlot blend", price_tier="premium",
               description="New Zealand's most celebrated Bordeaux blend; Cabernet Sauvignon, Merlot, Cabernet Franc; cedar, tobacco, blackcurrant and remarkable longevity.")
if n2:
    PAIR(pr2, "Roast lamb with mint and anchovy", "complement", "classic", "main", "New Zealand classic pairing; Cabernet structure grips lamb fat; mint and anchovy bridge.")
    PAIR(pr2, "Grilled lamb cutlets with rosemary and garlic", "complement", "established", "main", "Cassis and cedar echo charred lamb; tannins align with lean meat.")
    PAIR(pr2, "Duck liver pâté with cornichons and brioche", "complement", "established", "starter", "Tobacco and cedar notes echo pâté complexity; tannins grip rich liver fat.")
    PAIR(pr2, "Dark chocolate fondant with raspberry coulis", "bridge", "adventurous", "dessert", "Mature cassis bridges dark chocolate; raspberry echoes red fruit; tannins grip bitter cocoa.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("Done.")
conn.close()
