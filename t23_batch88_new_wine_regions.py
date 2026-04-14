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

# ── Region 1: Okanagan Valley ─────────────────────────────────────────────────
print("\n=== Region 1: Okanagan Valley ===")
r1 = R("Okanagan Valley", "Canada", "wine",
    designation_type="GI",
    designation_name="Okanagan Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="British Columbia's premier wine valley, a 250km north-south corridor of lakes, desert, and mountains in the province's interior. The extreme diurnal temperature variation between hot summer days and cold nights preserves natural acidity while achieving full phenolic ripeness — producing Riesling, Pinot Gris, and Pinot Noir in the cooler north, and Merlot, Syrah, and Cabernet Sauvignon in the hotter south around Osoyoos. The Okanagan is rapidly building an international reputation for quality.",
    key_producers="Blue Mountain, Quails' Gate, Burrowing Owl, Mission Hill, Nk'Mip Cellars",
    historical_context="European settlers planted the first commercial Okanagan vines in the 1930s; the wine quality revolution began in the late 1980s when the Canada-US Free Trade Agreement forced inferior hybrid-wine production to be uprooted and replaced with vinifera varieties.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Quails' Gate Estate Winery", "winery", r1, "Canada",
    production_philosophy="terroir_focused",
    philosophy_description="One of the Okanagan's founding quality estates on Westbank's west shore of Lake Okanagan, producing Old Vines Foch (one of BC's most distinctive wines from 50-year-old vines), Pinot Noir, and Chardonnay of international recognition.",
    reputation_narrative="Among BC's most consistently celebrated wineries; Old Vines Maréchal Foch is the Okanagan's most distinctive red wine.",
    price_positioning="premium")

prod1b_id = P("Burrowing Owl Estate Winery", "winery", r1, "Canada",
    production_philosophy="traditional",
    philosophy_description="South Okanagan Burrowing Owl produces some of BC's most structured reds from the hot Golden Mile Bench — Syrah, Cabernet Sauvignon, and Merlot from arid desert terroir with complex basalt and sandy loam soils.",
    reputation_narrative="A reference estate for serious South Okanagan red wine production; Syrah is the signature variety.",
    price_positioning="premium")

prod1a, new1a = PROD("Quails' Gate Old Vines Maréchal Foch", "wine_still", prod1a_id, r1, "Canada",
    subcategory="Maréchal Foch",
    description="BC's most distinctive red wine — from 50+ year-old Maréchal Foch vines on the west shore of Okanagan Lake. Deep, concentrated, dark chocolate and dried cherry with earthy complexity; showing that this humble French-American hybrid can produce wines of real character and age.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Roasted duck leg with wild blueberry gastrique and saskatoon berry", "complement", "classic", "main",
         "BC's native berries with BC's most distinctive red — wild blueberry mirrors the wine's dark-berry character.")
    PAIR(prod1a, "Bison short rib with Okanagan cherry reduction and root vegetable", "complement", "established", "main",
         "Canadian prairie bison with BC's heritage red wine — a genuinely Canadian luxury pairing of great authenticity.")
    PAIR(prod1a, "Smoked Sockeye salmon with birch syrup glaze", "bridge", "adventurous", "main",
         "Pacific Northwest salmon with an unexpected BC red — birch syrup's sweetness bridges the wine's fruit concentration.")
    PAIR(prod1a, "BC aged Cheddar (Farmhouse Natural Cheeses) with Okanagan apple chutney", "complement", "established", "cheese",
         "Local BC aged cheese with local BC wine — Okanagan apple chutney bridges both through regional terroir.")

prod1b, new1b = PROD("Burrowing Owl Syrah", "wine_still", prod1b_id, r1, "Canada",
    subcategory="Syrah",
    description="South Okanagan Syrah from the hot Golden Mile Bench — desert terroir with Rhône-inspired concentration, dark olive, pepper, and iron character. One of BC's most compelling red wines, showing that the Okanagan's arid south can produce serious Syrah.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled BC lamb chops with chimichurri and roasted garlic", "complement", "classic", "main",
         "Okanagan Syrah's peppery, olive character frames BC lamb with the same Mediterranean vocabulary.")
    PAIR(prod1b, "Braised elk shoulder with wild mushrooms and herb polenta", "complement", "established", "main",
         "Pacific Northwest game with desert-terroir Syrah — both carry dark, earthy, powerful character.")
    PAIR(prod1b, "Grilled venison sausage with yellow mustard and sauerkraut", "complement", "established", "casual",
         "Peppery Syrah and game sausage is a reliable partnership — mustard's tang amplifies the wine's spice.")
    PAIR(prod1b, "Aged Gouda with Okanagan apricot preserve", "complement", "established", "cheese",
         "Aged Gouda's caramel richness against Syrah's dark fruit — local apricot jam bridges fruit and tannin.")

# ── Region 2: Willamette Valley — Dundee Hills ───────────────────────────────
print("\n=== Region 2: Dundee Hills ===")
r2 = R("Dundee Hills", "USA", "wine",
    designation_type="AVA",
    designation_name="Dundee Hills AVA",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The heart of Oregon's Willamette Valley and home to its most celebrated Pinot Noir vineyards — established in the 1960s by David Lett and Dick Erath, the Dundee Hills' iron-rich Jory soil (volcanic red clay) produces wines of extraordinary depth, black cherry, and earthy complexity. The first sub-AVA demarcated within the Willamette, it hosts Eyrie, Ponzi, Adelsheim, and the Domaine Drouhin Oregon winery that announced Burgundy's recognition of Oregon's potential.",
    key_producers="Eyrie Vineyards, Adelsheim, Domaine Drouhin Oregon, Argyle, Archery Summit",
    historical_context="David Lett planted Oregon's first Pinot Noir and Chardonnay vines here in 1965, convinced Oregon's cool climate was ideal for Burgundian varieties; his 1975 Eyrie Pinot Noir placed 2nd at the 1979 Wine Olympics, triggering Robert Drouhin's investment.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "very_good", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Domaine Drouhin Oregon", "winery", r2, "USA",
    production_philosophy="traditional",
    philosophy_description="Robert Drouhin's 1987 investment in the Dundee Hills confirmed Oregon's status as a serious Pinot Noir destination. Véronique Drouhin-Boss brings Burgundian winemaking precision to Oregon Pinot Noir — Laurène is the estate's flagship, named after Véronique's daughter.",
    reputation_narrative="The most Burgundian Oregon estate and a bridge between Old and New World fine wine; Laurène is a benchmark for American Pinot Noir.",
    price_positioning="ultra_premium")

prod2b_id = P("Eyrie Vineyards", "winery", r2, "USA",
    production_philosophy="traditional",
    philosophy_description="David Lett's founding Oregon estate — now run by son Jason, Eyrie continues to produce archetypal Dundee Hills Pinot Noir and the original Oregon Pinot Gris. The estate's Original Vines Pinot Noir represents living viticultural history from Oregon's pioneering plantings.",
    reputation_narrative="Oregon's founding estate; Eyrie's historical significance in establishing Oregon's fine wine identity is unparalleled.",
    price_positioning="premium")

prod2a, new2a = PROD("Domaine Drouhin Oregon Laurène Pinot Noir", "wine_still", prod2a_id, r2, "USA",
    subcategory="Pinot Noir",
    description="Domaine Drouhin Oregon's flagship — Burgundian-influenced Pinot Noir from Dundee Hills Jory soil, combining red cherry, violets, and earth with extraordinary precision and a structure that ages magnificently. Named after Véronique's daughter, it bridges Burgundy's heritage with Oregon's terroir.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Duck breast à la Bourguignonne with pinot noir reduction", "complement", "classic", "main",
         "Burgundian technique applied to Oregon duck — Pinot Noir in the sauce mirrors the glass in a regional echo.")
    PAIR(prod2a, "Oregon Dungeness crab with drawn butter and chervil", "complement", "adventurous", "main",
         "Pacific Northwest luxury — Oregon crab with Oregon Pinot Noir; a local-terroir pairing of unexpected harmony.")
    PAIR(prod2a, "Wild mushroom risotto with Willamette Valley hazelnut and truffle", "complement", "established", "main",
         "Oregon's native hazelnut and local wild mushrooms echo the wine's earthy forest-floor character.")
    PAIR(prod2a, "Roast pigeon with black cherry compote and celeriac purée", "complement", "established", "main",
         "Delicate game with Oregon Pinot's cherry and earth — a French-Oregon bridge in one dish.")

prod2b, new2b = PROD("Eyrie Vineyards South Block Reserve Pinot Noir", "wine_still", prod2b_id, r2, "USA",
    subcategory="Pinot Noir",
    description="Oregon's most historically significant estate wine — the South Block Reserve from vines planted by David Lett in 1966. Old-vine Dundee Hills Pinot Noir of great complexity: translucent red cherry, dried flowers, iron mineral, and extraordinary longevity.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Roasted wild salmon with pinot reduction, hazelnut, and dill", "complement", "classic", "main",
         "Oregon's two great terroir expressions — Pacific Northwest Chinook salmon with Willamette Pinot Noir.")
    PAIR(prod2b, "Marinated roasted beets with Oregon chèvre and walnut dressing", "complement", "established", "starter",
         "Earthy beet's iron character mirrors Eyrie's mineral depth; local goat's cheese adds dairy contrast.")
    PAIR(prod2b, "Chanterelle mushroom tart with thyme and Gruyère", "complement", "classic", "starter",
         "Willamette Valley chanterelles with Dundee Pinot — local forest flavours mirror the wine's earthy complexity.")
    PAIR(prod2b, "Brillat-Savarin triple cream with dried cherry and almond", "complement", "established", "cheese",
         "Opulent triple cream with Oregon Pinot — the wine's acidity cuts the fat while cherry echoes the fruit.")

# ── Region 3: Carneros ───────────────────────────────────────────────────────
print("\n=== Region 3: Carneros ===")
r3 = R("Carneros", "USA", "wine",
    designation_type="AVA",
    designation_name="Los Carneros AVA",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="A cool, windswept AVA straddling the southern ends of Napa and Sonoma counties at the northern tip of San Francisco Bay. The consistent fog and breeze from San Pablo Bay creates California's coolest growing conditions — ideal for Pinot Noir, Chardonnay, and sparkling wine. Carneros is the source of base wines for California's finest sparkling programs (Domaine Carneros/Taittinger, Domaine Chandon) and produces some of the state's most elegant still Pinot Noir.",
    key_producers="Domaine Carneros, Acacia, Saintsbury, Hyde de Villaine, Cline Cellars",
    historical_context="The Carneros AVA was one of California's first in 1983; Louis Martini planted Pinot Noir here in 1942 recognising the maritime cooling influence; Taittinger's Champagne house investment in Domaine Carneros in 1987 confirmed the area's potential for world-class sparkling wine.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Domaine Carneros", "winery", r3, "USA",
    production_philosophy="traditional",
    philosophy_description="Taittinger's California estate produces Carneros's finest sparkling wine using traditional Champagne méthode with Pinot Noir and Chardonnay. Domaine Carneros Le Rêve is California's most celebrated blanc de blancs sparkling wine.",
    reputation_narrative="California's definitive Champagne-method sparkling producer; Le Rêve is a California sparkling wine icon.",
    price_positioning="ultra_premium")

prod3b_id = P("Hyde de Villaine", "winery", r3, "USA",
    production_philosophy="terroir_focused",
    philosophy_description="A collaboration between Aubert de Villaine (DRC co-director) and the Hyde family of Carneros — Hyde de Villaine produces terroir-driven Chardonnay and Syrah from the legendary Hyde Vineyard, bringing Burgundian philosophy to California's coolest growing region.",
    reputation_narrative="One of California's most prestigious limited-production wineries; Aubert de Villaine's involvement adds instant credibility.",
    price_positioning="ultra_premium")

prod3a, new3a = PROD("Domaine Carneros Le Rêve Blanc de Blancs", "wine_sparkling", prod3a_id, r3, "USA",
    subcategory="Traditional Method Sparkling",
    description="California's finest blanc de blancs sparkling wine — 100% Carneros Chardonnay from old-vine estate vineyards, aged for 5+ years on lees before disgorgement. Hauntingly precise, brioche-rich, with green apple, lemon cream, and extraordinary mineral depth.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Freshly shucked Marin Miyagi oysters with champagne mignonette", "cleanse", "classic", "aperitif",
         "California oysters from the same bay with California's finest sparkling — coastal terroir in both glass and shell.")
    PAIR(prod3a, "Dungeness crab cocktail with California avocado and citrus", "complement", "classic", "starter",
         "Pacific crab with Carneros blanc de blancs — the wine's citrus and mineral elevate the crab's sweetness.")
    PAIR(prod3a, "Smoked Pacific sturgeon with crème fraîche and paddlefish caviar", "complement", "established", "starter",
         "California's own caviar service — sparkling's yeast character and acidity frame smoked fish and caviar perfectly.")
    PAIR(prod3a, "Almond financiers with lemon curd and Meyer lemon zest", "complement", "established", "dessert",
         "Le Rêve's almond-brioche character mirrors the financier; Meyer lemon echoes the wine's citrus brightness.")

prod3b, new3b = PROD("Hyde de Villaine Chardonnay HdV", "wine_still", prod3b_id, r3, "USA",
    subcategory="Chardonnay",
    description="Aubert de Villaine's California Chardonnay from the Hyde Vineyard — a Burgundian-informed expression of Carneros Chardonnay: restrained, mineral, and complex with citrus blossom, white peach, and crushed limestone character unlike most California Chardonnay.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Pan-seared California halibut with hazelnut beurre noisette", "complement", "classic", "fish_course",
         "Pacific halibut with a Burgundian-inspired California Chardonnay — hazelnut bridges both in classic fashion.")
    PAIR(prod3b, "Butter-poached Maine lobster with tarragon cream and caviar", "elevate", "classic", "main",
         "California luxury — HdV's mineral Chardonnay elevates the lobster through the wine's acidity and precision.")
    PAIR(prod3b, "Spring pea velouté with crème fraîche and lemon oil", "complement", "established", "starter",
         "Carneros Chardonnay's citrus and freshness mirror spring pea's sweetness in an elegant seasonal starter.")
    PAIR(prod3b, "Aged Télème California cheese with honeycomb", "complement", "established", "cheese",
         "California's own aged cheese with its most Burgundian Chardonnay — a genuinely California terroir pairing.")

# ── Region 4: Central Otago ──────────────────────────────────────────────────
print("\n=== Region 4: Central Otago ===")
r4 = R("Central Otago", "New Zealand", "wine",
    designation_type="GI",
    designation_name="Central Otago GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="The world's southernmost wine region and New Zealand's most dramatic viticultural landscape — a remote interior plateau of the South Island ringed by snow-capped mountains, producing exclusively Pinot Noir and small quantities of white varieties. The extreme continental climate (New Zealand's only), schist and loess soils, and intense UV light at altitude create Pinot Noir of extraordinary concentration, silky texture, and dark cherry intensity. Sub-regions Bannockburn, Cromwell Basin, and Gibbston Valley each produce distinctive styles.",
    key_producers="Felton Road, Mt. Difficulty, Rippon, Amisfield, Two Paddocks",
    historical_context="Gold rush prospectors reported 'good wine grapes' in Central Otago in the 1860s; the modern industry began in the 1970s with Ann Pinckney's Mt. Difficulty planting; Felton Road's arrival in 1997 established international recognition for the region's extraordinary Pinot Noir.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "very_good", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Felton Road", "winery", r4, "New Zealand",
    production_philosophy="biodynamic",
    philosophy_description="Central Otago's benchmark estate — biodynamically farmed from the Bannockburn sub-region, Felton Road's Block 3, Block 5, and Calvert Pinot Noirs have defined the region's international reputation. Minimal intervention, whole-bunch inclusion, and old-vine viticulture produce wines of extraordinary purity.",
    reputation_narrative="New Zealand's most internationally celebrated wine estate; Block 3 and Block 5 are allocated globally to collectors.",
    price_positioning="ultra_premium")

prod4b_id = P("Rippon Vineyard", "winery", r4, "New Zealand",
    production_philosophy="biodynamic",
    philosophy_description="A biodynamically certified lakeside vineyard on the shores of Lake Wānaka — one of the world's most photographed vineyards. Rippon's Mature Vine Pinot Noir from 30-year-old vines produces some of Central Otago's most complex and age-worthy expressions.",
    reputation_narrative="One of New Zealand's most visually iconic and qualitatively significant wine estates; Mature Vine is a collector benchmark.",
    price_positioning="ultra_premium")

prod4a, new4a = PROD("Felton Road Block 3 Pinot Noir", "wine_still", prod4a_id, r4, "New Zealand",
    subcategory="Pinot Noir",
    description="Felton Road's most celebrated single-block Pinot Noir — from old schist-rooted vines in Bannockburn, biodynamically farmed and minimally vinified. Block 3 produces Central Otago's most structured and complex expression: concentrated dark cherry, iron mineral, and extraordinary aging potential.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Canterbury lamb rack with manuka honey and herbs", "complement", "classic", "main",
         "New Zealand's finest lamb with its greatest Pinot Noir — Central Otago's defining food-wine identity.")
    PAIR(prod4a, "Seared cervena venison with blackcurrant reduction and root vegetables", "complement", "established", "main",
         "NZ farmed venison with NZ Pinot — blackcurrant echoes Block 3's dark fruit while the tannin handles game.")
    PAIR(prod4a, "Wild South Island salmon with hazelnut butter and lemon", "complement", "established", "main",
         "South Island salmon with South Island's finest Pinot — Central Otago's luxury combination.")
    PAIR(prod4a, "Aged Whitestone Vintner's Reserve Cheese with quince paste", "complement", "established", "cheese",
         "New Zealand's finest aged hard cheese with its most collected Pinot — a rare New Zealand terroir pairing.")

prod4b, new4b = PROD("Rippon Mature Vine Pinot Noir", "wine_still", prod4b_id, r4, "New Zealand",
    subcategory="Pinot Noir",
    description="From 30-year-old biodynamic vines on the shores of Lake Wānaka at 340m altitude — Rippon's flagship combines ethereal transparency with concentrated complexity. The lake-facing exposure creates a unique microclimate producing Pinot Noir of gossamer texture and haunting red-fruit purity.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "Roasted duck breast with Otago cherry compote and lemon thyme", "complement", "classic", "main",
         "Biodynamic Pinot's cherry and silky texture frame the duck with precision — cherry compote echoes the fruit.")
    PAIR(prod4b, "Grilled Lake Wānaka trout with dill, capers, and crème fraîche", "complement", "classic", "fish_course",
         "The lake in the glass meets the fish from the lake — Rippon's lakeside terroir and local trout in one pairing.")
    PAIR(prod4b, "Wild rabbit with chanterelles, thyme, and Dijon cream", "complement", "established", "main",
         "Delicate game with silky Wānaka Pinot — chanterelles echo the wine's forest and mineral complexity.")
    PAIR(prod4b, "Whitestone Brie with Wānaka rosehip jelly", "complement", "established", "cheese",
         "New Zealand soft cheese with a local fruit jelly and NZ's most elegant Pinot — a high-country terroir moment.")

# ── Region 5: Mendocino County ───────────────────────────────────────────────
print("\n=== Region 5: Mendocino County ===")
r5 = R("Mendocino County", "USA", "wine",
    designation_type="AVA",
    designation_name="Mendocino County AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="California's most northerly wine county and its organic wine heartland — Mendocino produces a diverse range of varieties from the warm inland Redwood Valley and Potter Valley to the cool, fog-influenced Anderson Valley near the Pacific coast. The county has the highest proportion of certified organic and biodynamic viticulture in the USA. Anderson Valley is Mendocino's most celebrated sub-region for cool-climate Pinot Noir, Chardonnay, and sparkling wine.",
    key_producers="Navarro Vineyards, Husch Vineyards, Roederer Estate, Bonterra, Goldeneye",
    historical_context="Italian immigrant families settled Mendocino for farming and logging in the 19th century; wine production began on a commercial scale in the 1960s; Roederer Estate (Louis Roederer's California outpost) arrived in 1982 and established Anderson Valley's sparkling wine credentials.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Roederer Estate", "winery", r5, "USA",
    production_philosophy="traditional",
    philosophy_description="Louis Roederer's California outpost in Anderson Valley produces Champagne-method sparkling wine of the highest quality — the NV Brut and vintage L'Ermitage bottlings are consistently ranked among California's finest sparkling wines, using estate-grown Chardonnay and Pinot Noir from Anderson Valley.",
    reputation_narrative="California's most respected sparkling wine producer after Schramsberg; L'Ermitage is among the state's finest sparkling wines.",
    price_positioning="premium")

prod5b_id = P("Navarro Vineyards", "winery", r5, "USA",
    production_philosophy="natural",
    philosophy_description="Ted Bennett and Deborah Cahn established Navarro as Anderson Valley's quality benchmark in 1974 — their Gewürztraminer, Pinot Gris, and Pinot Noir are consistently among the AVA's finest expressions, produced with minimal intervention from certified organic estate vineyards.",
    reputation_narrative="Anderson Valley's founding quality estate; Gewürztraminer is one of California's most distinctive white wines.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Roederer Estate L'Ermitage Brut", "wine_sparkling", prod5a_id, r5, "USA",
    subcategory="Traditional Method Sparkling",
    description="Roederer Estate's prestige cuvée from Anderson Valley — equal parts Pinot Noir and Chardonnay from selected old-vine parcels, aged 5+ years on lees. L'Ermitage is one of California's most serious sparkling wines: creamy, complex, and mineral with exceptional aging potential.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Freshly shucked Pacific oysters with vodka-cucumber granita", "cleanse", "classic", "aperitif",
         "California sparkling with Pacific Coast oysters — the wine's acidity and brine mirror the ocean's character.")
    PAIR(prod5a, "Dungeness crab salad with tarragon mayo on sourdough", "complement", "established", "starter",
         "California's best crab with California's finest sparkling — a West Coast luxury pairing of real authenticity.")
    PAIR(prod5a, "Truffle arancini with saffron and Parmigiano", "complement", "established", "starter",
         "L'Ermitage's yeast complexity and mineral depth bridge the fried truffle rice ball's earthiness and richness.")
    PAIR(prod5a, "Lemon posset with candied kumquat and shortbread", "complement", "established", "dessert",
         "The wine's citrus precision and fine bead complement the posset's cream and acidity without clashing.")

prod5b, new5b = PROD("Navarro Vineyards Gewürztraminer", "wine_still", prod5b_id, r5, "USA",
    subcategory="Gewürztraminer",
    description="Anderson Valley's most distinctive white wine — estate Gewürztraminer from cool coastal fog-influenced vineyards producing lychee, rose petal, ginger, and spice with characteristic off-dry balance and refreshing acidity. One of California's most individual and food-friendly white wines.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Dungeness crab cakes with mango salsa and cilantro crème fraîche", "complement", "established", "starter",
         "Gewürztraminer's tropical and floral character bridge the mango and crab with the same aromatic vocabulary.")
    PAIR(prod5b, "Thai red curry with lemongrass, coconut, and jasmine rice", "bridge", "classic", "main",
         "Spicy Thai curry's classic match — Gewürztraminer's off-dry sweetness and aromatic spice tame the chilli heat.")
    PAIR(prod5b, "Alsatian-style onion tart (Flammkuchen) with crème fraîche and bacon", "complement", "classic", "casual",
         "Gewürztraminer and Flammkuchen is an Alsatian archetype transplanted to Mendocino's cool coastal terroir.")
    PAIR(prod5b, "Epoisses at room temperature with crusty baguette", "complement", "classic", "cheese",
         "The classic Alsatian pairing — pungent washed-rind Epoisses with fragrant Gewürztraminer from a cool region.")

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
