#!/usr/bin/env python3
"""B167 — Australia + California + Canada: Coonawarra GI, Eden Valley GI, Sonoma Coast AVA, Anderson Valley AVA, Niagara Peninsula"""
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

# === COONAWARRA GI ===
print("=== Coonawarra GI ===")
r1 = R("Coonawarra GI", "Australia", "wine",
       designation_type="GI",
       designation_name="Coonawarra Geographic Indication",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Coonawarra in South Australia's Limestone Coast is Australia's most celebrated Cabernet Sauvignon region. The signature is 'terra rossa' — a strip of red iron-rich soil over white limestone — that gives Coonawarra Cabernet its distinctive combination of eucalyptus, dark cassis, and mineral precision. At just 15km long and 2km wide, the terra rossa is one of the world's most precisely defined terroirs. Penfolds Bin 707, Wynns Coonawarra Estate, and Hollick produce benchmark Cabernet Sauvignon here.",
       key_producers="Wynns Coonawarra Estate, Penfolds (Bin 707), Hollick Wines, Balnaves of Coonawarra, Parker Coonawarra Estate",
       historical_context="Coonawarra's terra rossa was first planted in 1891 by John Riddoch. The region's potential for Cabernet Sauvignon was recognised early, but its true quality era began in the 1950s when Wynns took over and began producing wines that would define Australian Cabernet for the next century.")
for yr, qd, pt, sn in [
    (2018,"exceptional","stable","A legendary Coonawarra vintage — terra rossa Cabernet of extraordinary concentration and minerality."),
    (2019,"excellent","stable","Fine vintage with excellent freshness; Cabernet showing classic eucalyptus and cassis character."),
    (2020,"very_good","stable","Good vintage; some smoke impact on peripheral sites but terra rossa largely unaffected."),
    (2021,"excellent","rising","Outstanding vintage; Coonawarra Cabernet of exceptional structure for extended ageing."),
    (2022,"very_good","stable","Warm conditions; richer, more opulent Cabernet with concentrated dark fruit."),
    (2023,"excellent","rising","Benchmark vintage for terra rossa Cabernet — mineral precision and dark fruit in perfect balance."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Wynns Coonawarra Estate", "winery", r1, "Australia",
       production_philosophy="terroir_expression",
       philosophy_description="Coonawarra's historic founding estate, established 1897, producing benchmark Cabernet Sauvignon, Shiraz, and Riesling from terra rossa and deep sandy loam soils. Wynns Black Label Cabernet Sauvignon is Australia's most historic estate-grown Cabernet.",
       reputation_narrative="Wynns Coonawarra Estate is Australia's most significant Cabernet Sauvignon producer — the Black Label has defined the Coonawarra style for 70 years and remains a reference point for the Australian wine industry's identity.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Wynns Coonawarra Estate Black Label Cabernet Sauvignon", "wine_still", p1, r1, "Australia",
                    subcategory="red", description="Australia's most iconic estate Cabernet Sauvignon — deep garnet, cassis, dark cherry, cedary oak, eucalyptus, and the terra rossa's distinctive mineral precision. Structured for 10–20 years ageing, consistently Australia's best-value Cabernet Sauvignon.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Char-grilled bone-in ribeye with herb butter", "complement", "classic", "main", "Terra rossa Cabernet and Australian beef — the national pairing. Cassis and eucalyptus cut through beef fat; the wine's structure demands a quality cut.")
    PAIR(prod, "Roasted lamb rack with rosemary and garlic", "complement", "classic", "main", "A classic Australian pairing — Coonawarra Cab's eucalyptus and mint notes have a natural affinity with lamb's sweetness.")
    PAIR(prod, "Aged cheddar with quince paste and walnuts", "complement", "established", "cheese", "Terra rossa mineral notes bridge to aged cheddar's sharpness; cassis fruit contrasts the quince sweetness beautifully.")
    PAIR(prod, "Slow-cooked beef short rib with bush tomato relish", "complement", "established", "main", "Structured Cabernet handles braised beef's collagen richness; bush tomato's earthiness bridges Coonawarra's mineral character.")
prod, is_new = PROD("Wynns John Riddoch Limited Release Cabernet Sauvignon Coonawarra", "wine_still", p1, r1, "Australia",
                    subcategory="red", description="The estate's flagship — named for Coonawarra's founder. Only made in exceptional vintages, the John Riddoch is from the finest terra rossa parcels. Deep, concentrated: dark cassis, cigar box, pencil shaving, eucalyptus, and monumental tannins for 20+ year ageing.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Double-aged beef fillet with mushroom duxelles and truffle jus", "complement", "classic", "main", "The wine's power demands premium beef preparation; truffle bridges the eucalyptus mineral notes beautifully.")
    PAIR(prod, "Braised lamb shoulder with eggplant and preserved lemon", "complement", "established", "main", "Concentrated Coonawarra needs slow-cooked, collagen-rich lamb; preserved lemon echoes the wine's freshness.")
    PAIR(prod, "Aged Parmigiano Reggiano 36-month", "complement", "established", "cheese", "Hard aged Italian cheese and monumental Australian Cabernet — umami bridges to cassis; the wine's tannins cut through fat.")
    PAIR(prod, "Dark chocolate soufflé with raspberry coulis", "complement", "adventurous", "dessert", "The wine's cassis and structure bridge to dark chocolate; raspberry echoes Cabernet's red fruit dimension.")

# === EDEN VALLEY GI ===
print("=== Eden Valley GI ===")
r2 = R("Eden Valley GI", "Australia", "wine",
       designation_type="GI",
       designation_name="Eden Valley Geographic Indication",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Eden Valley sits at 400–550m altitude in the Mt Lofty Ranges above the Barossa Valley, producing two of Australia's greatest wines: Riesling and Shiraz. The cool altitude gives Eden Valley Riesling extraordinary finesse and lime-mineral precision — the grape equivalent of the Clare Valley's benchmark style. The High Eden sub-region is even cooler, producing linear, laser-like Riesling that ages magnificently. Henschke's Hill of Grace Shiraz from the Eden Valley is one of Australia's most historic single-vineyard wines.",
       key_producers="Henschke, Pewsey Vale Estate, Eden Hall, Mountadam, Irvine Wines",
       historical_context="Eden Valley wine production dates to the 1840s, settled by German immigrants alongside the Barossa Valley below. Henschke's Hill of Grace vineyard, with vines dating to the 1860s, is Australia's most historically significant single vineyard, producing a Shiraz that has sold for over $1000 per bottle.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Eden Valley vintage — Riesling and Hill of Grace Shiraz of extraordinary quality."),
    (2019,"very_good","stable","Fine year; altitude freshness preserved in both Riesling and cool-climate Shiraz."),
    (2020,"very_good","stable","Good vintage; Eden Valley largely unaffected by smoke that impacted other SA regions."),
    (2021,"excellent","rising","Outstanding conditions; Riesling of exceptional mineral precision and ageing potential."),
    (2022,"very_good","stable","Warm conditions produced richer Shiraz and more opulent Riesling than typical."),
    (2023,"excellent","rising","Exceptional vintage; Hill of Grace considered among the finest recent releases."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Henschke Winery Eden Valley", "winery", r2, "Australia",
       production_philosophy="biodynamic",
       philosophy_description="Australia's most historic family winery, continuously operated since 1868, now in its fifth generation under Stephen and Prue Henschke. Hill of Grace — from 1860s-planted Shiraz vines — is Australia's most revered single-vineyard wine and one of the most sought-after in the world.",
       reputation_narrative="Henschke's Hill of Grace Shiraz is Australia's equivalent of Penfolds Grange — an icon, a national treasure, and one of the Southern Hemisphere's greatest wines from vines dating to the 1860s. The estate's biodynamic conversion has also deepened the wines' expressiveness.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Henschke Hill of Grace Shiraz Eden Valley", "wine_still", p2, r2, "Australia",
                    subcategory="red", description="Australia's most revered single-vineyard wine from 1860s-planted Shiraz ('Shiraz-Mataro') vines. Profound complexity: dark fruit, truffle, leather, black olive, violets, and a mineral backbone from ancient soil. Requires 10–15 years minimum for full expression.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted prime rib with bone marrow and horseradish", "complement", "classic", "main", "Australia's greatest Shiraz demands the finest beef preparation — shared earthiness and power elevate both.")
    PAIR(prod, "Whole-roasted wild duck with olive and lemon thyme", "complement", "established", "main", "The wine's dark fruit, olive, and truffle notes mirror duck's richness; lemon thyme bridges the freshness.")
    PAIR(prod, "Truffle pasta with aged Parmigiano and black truffle", "bridge", "adventurous", "main", "Truffle notes in the wine create a self-referential bridge; Parmigiano's umami amplifies the Shiraz's depth.")
    PAIR(prod, "Aged Barossa Valley Parmigiano-style hard cheese", "complement", "established", "cheese", "Regional Australia pairing — local hard cheese with the Barossa's greatest wine, sharing earthy mineral depth.")
prod, is_new = PROD("Pewsey Vale Estate Riesling Eden Valley", "wine_still", p2, r2, "Australia",
                    subcategory="white", description="Classic Eden Valley Riesling from the high-altitude Pewsey Vale Vineyard — owned by Yalumba. Lime zest, slate, green apple, and a crisp minerality that develops toast and petrol complexity over 10+ years. One of Australia's most age-worthy whites.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled barramundi with lime, capers and parsley", "complement", "classic", "main", "Eden Valley Riesling's lime and mineral freshness mirror barramundi's delicate white flesh — a natural Australian pairing.")
    PAIR(prod, "Thai-style green papaya salad with prawns and lime", "complement", "established", "starter", "Riesling's citrus and mineral freshness stand up to Thai spice; lime echoes the wine's core fruit character.")
    PAIR(prod, "Salt and pepper squid with lime aioli", "complement", "classic", "starter", "High-acid Riesling cuts through fried coating; lime echoes the citrus in the wine; mineral depth matches squid's brininess.")
    PAIR(prod, "Riesling-marinated chicken schnitzel with lemon", "complement", "established", "main", "A wine-forward pairing — Riesling in the marinade creates harmony; lemon and mineral freshness refresh between bites.")

# === SONOMA COAST AVA ===
print("=== Sonoma Coast AVA ===")
r3 = R("Sonoma Coast AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Sonoma Coast American Viticultural Area",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The Sonoma Coast AVA encompasses both the warmer Sonoma Valley areas and the dramatically cooler, fog-influenced coastal sites directly adjacent to the Pacific. The 'true' or 'extreme' Sonoma Coast — Petaluma Gap, Fort Ross-Seaview, West Sonoma Coast — produces Chardonnay and Pinot Noir of extraordinary cool-climate complexity, comparable to grand cru Burgundy in mineral precision and longevity. Producers like Littorai, Hirsch, and Williams Selyem have defined this coastal terroir as California's most intellectually compelling wine region.",
       key_producers="Littorai Wines, Hirsch Vineyards, Williams Selyem, Flowers Vineyard, Peay Vineyards",
       historical_context="The extreme coastal vineyards of Sonoma Coast were pioneered in the 1980s and 1990s by growers who believed the Pacific's cooling influence could produce world-class Pinot Noir and Chardonnay. Ted Lemon at Littorai and David Hirsch at Hirsch Vineyards were among the first to demonstrate this potential.")
for yr, qd, pt, sn in [
    (2018,"very_good","stable","Good vintage; coastal fog moderated the warm year, preserving Pinot Noir's elegance."),
    (2019,"excellent","rising","Outstanding Sonoma Coast vintage — Pinot and Chardonnay of exceptional mineral freshness."),
    (2020,"challenging","stable","Wildfire smoke affected some producers; careful selection produced excellent coastal wines."),
    (2021,"very_good","stable","Fine vintage; West Sonoma Coast particularly successful for structured, age-worthy Pinot."),
    (2022,"excellent","rising","Benchmark vintage for extreme coastal sites — wines of Burgundian precision and complexity."),
    (2023,"excellent","rising","Outstanding conditions; Fort Ross-Seaview and Petaluma Gap wines garnering critical acclaim."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Littorai Wines Sonoma Coast", "winery", r3, "USA",
       production_philosophy="biodynamic",
       philosophy_description="Ted Lemon established Littorai in 1993 after working at Burgundy's Domaine Dujac, bringing Burgundian biodynamic principles to the California coast. His single-vineyard Sonoma and Mendocino coast Pinot Noir and Chardonnay are California's most Burgundy-influenced wines.",
       reputation_narrative="Littorai is California's most intellectually rigorous producer — Ted Lemon's biodynamic farming, minimal intervention, and deep Burgundian philosophy have created wines of extraordinary restraint and mineral complexity that challenge California's reputation for rich, opulent wines.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Littorai The Haven Vineyard Pinot Noir Sonoma Coast", "wine_still", p3, r3, "USA",
                    subcategory="red", description="Single-vineyard Pinot Noir from The Haven's Goldridge sandy loam on the extreme Sonoma Coast. Intensely mineral and restrained — cranberry, raspberry, sea stone, dried herbs, and silky tannins. Burgundian in its restraint and longevity.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted wild salmon with lemon beurre blanc", "complement", "classic", "main", "Sonoma Coast Pinot and Pacific salmon — two coastal treasures. Mineral freshness mirrors salmon's ocean character; the wine's delicacy doesn't overpower.")
    PAIR(prod, "Roasted guinea fowl with chanterelles and cream", "complement", "classic", "main", "The wine's Burgundian restraint suits this classic French preparation; chanterelles bridge the mineral-earthy notes.")
    PAIR(prod, "Duck breast with huckleberry reduction and wild rice", "complement", "established", "main", "Coastal Pinot's cranberry and dried herb notes echo wild huckleberry; wild rice's earthiness bridges the mineral character.")
    PAIR(prod, "Aged Humboldt Fog goat cheese with herbs", "complement", "classic", "cheese", "The California coastal connection — mineral Pinot Noir with California's most distinctive goat cheese, both shaped by coastal cool air.")
prod, is_new = PROD("Littorai Mays Canyon Chardonnay Sonoma Coast", "wine_still", p3, r3, "USA",
                    subcategory="white", description="Single-vineyard coastal Chardonnay from the cool Mays Canyon site — lean, mineral, and Burgundian in profile. Citrus, stone fruit, saline sea breeze, and a chalky mineral finish that recalls Chablis. California's most restrained and age-worthy Chardonnay style.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Dungeness crab with drawn butter and lemon", "complement", "classic", "main", "The quintessential Pacific Coast pairing — mineral coastal Chardonnay and Pacific Dungeness crab share briny oceanic depth.")
    PAIR(prod, "Grilled Monterey Bay abalone with herb butter", "complement", "established", "main", "The wine's saline minerality mirrors abalone's oceanic richness; herb butter bridges the Chardonnay's freshness.")
    PAIR(prod, "Halibut ceviche with citrus and jalapeño", "complement", "established", "starter", "Coastal mineral Chardonnay's citrus acidity mirrors the ceviche's lime; mineral depth bridges to halibut's ocean character.")
    PAIR(prod, "Dry-aged triple cream brie with sourdough", "complement", "established", "cheese", "The wine's restraint handles triple cream without being overwhelmed; mineral freshness cuts through the fat.")

# === ANDERSON VALLEY AVA ===
print("=== Anderson Valley AVA ===")
r4 = R("Anderson Valley AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Anderson Valley American Viticultural Area",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Anderson Valley in Mendocino County is California's coolest wine region, with coastal fog from the Pacific pushing 15 miles inland through the Navarro River canyon. The region is dual-acclaimed: for world-class sparkling wine (Roederer Estate, Scharffenberger) and for benchmark Pinot Noir and Alsatian varieties (Gewürztraminer, Pinot Gris). The deep Mendocino fog and cool Pacific air allow grapes to ripen slowly, building flavour complexity while retaining bright natural acidity.",
       key_producers="Roederer Estate, Breggo Cellars, Handley Cellars, Lula Cellars, Goldeneye Winery",
       historical_context="Anderson Valley gained AVA status in 1983. Champagne Louis Roederer's 1982 decision to establish Roederer Estate here for California's finest traditional method sparkling wine validated the valley's cool-climate potential. The region's Alsatian variety success was pioneered by Navarro Vineyards.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Landmark Anderson Valley vintage — Pinot Noir of exceptional freshness and complexity."),
    (2020,"very_good","stable","Good vintage; fog moderated California heat, preserving acidity and delicacy."),
    (2021,"excellent","rising","Outstanding conditions; Pinot Noir and Gewürztraminer of exceptional aromatic intensity."),
    (2022,"very_good","stable","Warm year; more accessible Pinot Noir with generous fruit, plus fine sparkling base wine."),
    (2023,"excellent","rising","Exceptional vintage for Anderson Valley Pinot Noir — some comparing it to Burgundy's finest."),
]:
    VIN(r4, yr, qd, pt, sn)

p4 = P("Roederer Estate Anderson Valley", "winery", r4, "USA",
       production_philosophy="traditional_methods",
       philosophy_description="The California offshoot of Champagne Louis Roederer, established 1982 to produce California's finest traditional method sparkling wine. Roederer Estate Brut and the vintage L'Ermitage are made from estate-grown Chardonnay and Pinot Noir using Champagne's traditional méthode champenoise.",
       reputation_narrative="Roederer Estate is California's most celebrated sparkling wine producer, consistently producing bubbles that rival Champagne at half the price. Their L'Ermitage vintage sparkling is considered America's finest traditional method sparkling wine.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Roederer Estate Brut Anderson Valley", "wine_sparkling", p4, r4, "USA",
                    subcategory="sparkling_traditional_method", description="California's benchmark traditional method sparkling wine — Chardonnay and Pinot Noir from cool Anderson Valley estate vineyards. Elegant, precise: green apple, brioche, lemon cream, and a fine persistent mousse. Rivals Champagne NV at its price point.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled Pacific oysters with lemon and tabasco", "complement", "classic", "amuse", "The West Coast answer to Champagne and oysters — cool Anderson Valley sparkle and Pacific oysters share oceanic minerality.")
    PAIR(prod, "Dungeness crab cakes with remoulade", "complement", "classic", "starter", "California coastal sparkling and Pacific Dungeness — the quintessential California celebratory pairing.")
    PAIR(prod, "Seared ahi tuna with sesame crust and wasabi", "complement", "established", "starter", "Bubbles cleanse sesame and fish oil; the wine's citrus brightness mirrors the wasabi's freshness.")
    PAIR(prod, "Fromage blanc with smoked salmon and chives", "complement", "established", "starter", "Autolytic brioche notes bridge to smoked salmon; bubbles cut through the cream cheese richness.")
prod, is_new = PROD("Goldeneye Pinot Noir Anderson Valley", "wine_still", p4, r4, "USA",
                    subcategory="red", description="Estate Anderson Valley Pinot Noir from Goldeneye Winery (Duckhorn Portfolio) — bright, fog-driven cool-climate style. Red cherry, raspberry, cranberry, dried herbs, and a mineral freshness that recalls the region's proximity to the Pacific. Approachable yet age-worthy.", price_tier="premium")
if is_new:
    PAIR(prod, "Pan-roasted duck confit with cherry compote", "complement", "classic", "main", "Cool-climate Pinot's cherry brightness mirrors the compote; fog-driven freshness cuts through the confit's richness.")
    PAIR(prod, "Wild mushroom risotto with Parmesan and thyme", "bridge", "classic", "main", "Mineral earthy Pinot bridges to mushroom depth; thyme echoes the wine's dried herb character.")
    PAIR(prod, "Grilled Pacific salmon with lemon herb butter", "complement", "classic", "main", "California's classic salmon-Pinot pairing — fog-driven lightness of this Pinot makes it the ideal salmon companion.")
    PAIR(prod, "Aged Point Reyes Blue with honey and walnuts", "complement", "established", "cheese", "Cool coastal Pinot and Northern California blue cheese — both shaped by Pacific coastal influence.")

# === NIAGARA PENINSULA ===
print("=== Niagara Peninsula ===")
r5 = R("Niagara Peninsula", "Canada", "wine",
       designation_type="VQA",
       designation_name="Niagara Peninsula Vintners Quality Alliance",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Canada's most important wine region, the Niagara Peninsula in Ontario benefits from the moderating influence of Lake Ontario and Lake Erie, creating a microclimate that extends the growing season and enables Riesling, Chardonnay, Pinot Noir, and Cabernet Franc to ripen fully. The region is world-famous for Icewine — Ontario produces more icewine than any other region on earth. The escarpment's diverse soils and lake-tempered climate also produce world-class dry wines from Inniskillin and Tawse.",
       key_producers="Inniskillin Winery, Tawse Winery, Hidden Bench Estate, Cave Spring Cellars, Stratus Vineyards",
       historical_context="Niagara wine production dates to the 1860s, but the modern era began in 1975 when Karl Kaiser and Don Ziraldo founded Inniskillin. Their 1991 Vidal Icewine won Vinexpo's Grand Prix d'Honneur in 1991, launching Ontario icewine to international fame. Niagara received VQA status in 1988.")
for yr, qd, pt, sn in [
    (2017,"excellent","rising","A landmark Niagara vintage — Chardonnay and Riesling of exceptional balance and mineral depth."),
    (2018,"very_good","stable","Good vintage; Pinot Noir and Cabernet Franc particularly successful in the warm summer."),
    (2019,"excellent","rising","Outstanding year — Riesling and Chardonnay of benchmark acidity and aromatic intensity."),
    (2020,"very_good","stable","Fine conditions; excellent icewine harvest with natural freeze occurring in late January."),
    (2021,"excellent","rising","Exceptional vintage; Niagara Pinot Noir achieving international critical recognition."),
    (2022,"very_good","stable","Good ripeness; Cabernet Franc showing excellent pepper and dark fruit character."),
]:
    VIN(r5, yr, qd, pt, sn)

p5 = P("Tawse Winery Niagara", "winery", r5, "Canada",
       production_philosophy="biodynamic",
       philosophy_description="Canada's most award-winning winery, Tawse is biodynamically certified and produces benchmark Chardonnay, Pinot Noir, and Riesling from multiple Niagara sub-appellations. Their Quarry Road Vineyard Pinot Noir and Robyn's Block Chardonnay are consistently Ontario's finest expressions of these varieties.",
       reputation_narrative="Tawse has won Canadian Winery of the Year from Wine Access magazine multiple times and is the most critically acclaimed producer in Ontario. Their biodynamic approach and commitment to Burgundian varieties has positioned Niagara as a serious cool-climate wine region.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Tawse Quarry Road Vineyard Pinot Noir Niagara", "wine_still", p5, r5, "Canada",
                    subcategory="red", description="Single-vineyard Pinot Noir from Quarry Road's clay-rich soils — elegant, cool-climate style with red cherry, cranberry, dried rose, and a fine mineral acidity from the Escarpment's limestone. Ontario's most acclaimed Pinot Noir.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted duck breast with sour cherry reduction", "complement", "classic", "main", "Cool Ontario Pinot's cherry and dried rose echo the sour cherry preparation; duck's richness is balanced by the wine's acidity.")
    PAIR(prod, "Mushroom and leek tart with aged Gruyère", "bridge", "established", "main", "The wine's mineral earthiness bridges to mushroom and leek; Gruyère's nuttiness complements Pinot's fruit.")
    PAIR(prod, "Grilled Ontario rainbow trout with lemon and dill", "complement", "classic", "main", "Local Ontario fish with local Ontario Pinot Noir — mineral freshness mirrors the trout's delicate flavour.")
    PAIR(prod, "Aged Thunder Oak Gouda from Ontario", "complement", "established", "cheese", "Ontario terroir pairing — local aged Gouda's caramel meets the Quarry Road Pinot's cherry fruit and mineral freshness.")
prod, is_new = PROD("Inniskillin Vidal Icewine Niagara", "wine_dessert", p5, r5, "Canada",
                    subcategory="sweet_white", description="Canada's most celebrated icewine, made from Vidal grapes naturally frozen on the vine in Ontario's deep winter. Intensely sweet yet vibrant — peach, mango, honey, and bright apricot acidity. The wine that put Canada on the world wine map when it won Vinexpo's Grand Prix d'Honneur.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Foie gras terrine with apricot and brioche", "complement", "classic", "starter", "Icewine's apricot and peach mirror the accompaniment's fruit; the wine's acidity cuts through foie's richness.")
    PAIR(prod, "Aged Stilton with dried apricot and walnut", "contrast", "classic", "cheese", "Classic sweet wine and blue cheese contrast — icewine's fruit sweetness meets Stilton's salt-funk in perfect balance.")
    PAIR(prod, "Fresh peach tart with vanilla cream", "complement", "classic", "dessert", "Peach and honey in the icewine echo the tart's fruit; the wine's acidity keeps the pairing from cloying.")
    PAIR(prod, "Roasted goose with apple and thyme stuffing", "complement", "adventurous", "main", "Surprisingly versatile — Icewine's sweetness and acidity can contrast with savoury goose; apple bridges both.")

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
print("B167 complete.")
cur.close()
conn.close()
