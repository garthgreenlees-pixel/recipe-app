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

# ── 1. Clare Valley (Australia/South Australia) ───────────────────────────────
print("\n=== Clare Valley (Australia) ===")
r1 = R("Clare Valley", "Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Clare Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Australia's most celebrated Riesling region and a benchmark for the variety worldwide, the Clare Valley sits in South Australia's Mount Lofty Ranges at 400–500m elevation north of the Barossa. The limestone-rich soils, warm days and cool nights produce Riesling of extraordinary mineral precision, lime-zest concentration and the capacity to age for 20–30+ years into complex petrol-and-toast character. Clare Valley Riesling — typically released in screw-cap — is widely regarded as Australia's finest and most internationally respected wine style.",
    key_producers="Grosset, Jim Barry, Wendouree, Kilikanoon, O'Leary Walker",
    historical_context="Clare Valley's first vineyards were planted by Jesuit priests at Sevenhill in 1851, making it one of Australia's oldest wine regions. Riesling's dominance dates from the 1970s when Polish Hill River was recognised for its distinctive slate soils. The introduction of Stelvin screw caps by Clare Valley producers in 2000 — led by Jeffrey Grosset — was a landmark moment in Australian wine history, demonstrating that premium wine could benefit from oxygen-free closure and helping normalise the screw cap globally.")

VIN(r1, 2023, "excellent", "stable", "Outstanding Clare Valley vintage; Riesling of exceptional citrus precision and mineral depth")
VIN(r1, 2022, "very_good", "stable", "Warm year with good acid retention; generous, approachable Clare Riesling")
VIN(r1, 2021, "excellent", "stable", "Fine balance of ripeness and acidity; benchmark Clare character with great aging potential")
VIN(r1, 2020, "very_good", "stable", "Reliable year; classic lime-mineral Riesling profile across the valley's sub-regions")
VIN(r1, 2019, "exceptional", "rising", "One of Clare Valley's finest Riesling vintages in memory; concentrated, structured wines built for 20+ years")

p1a = P("Grosset Wines", "Australia", r1, description="Australia's most celebrated Riesling producer and the pioneer of screw-cap closures for premium wine, Jeffrey Grosset's two benchmark Rieslings — Polish Hill (from slate soils) and Springvale (from limestone) — are considered the finest in Australia and rank among the world's best Rieslings alongside the greatest from Mosel and Alsace.")
prod1a, new1a = PROD("Grosset Polish Hill Riesling Clare Valley", "wine_still", p1a, r1, "Australia",
    subcategory="Riesling",
    description="Australia's most iconic Riesling — from the ancient Silurian slate soils of Polish Hill River, producing a wine of extraordinary mineral austerity, lime-zest precision and firm structure that needs 5–10 years to open fully and ages magnificently for 25+ years, developing classic Riesling petrol and toast complexity.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Sydney rock oysters with lemon and sea salt", "complement", "classic", "starter", "Australian oysters with Australia's greatest Riesling — the wine's citrus-mineral precision mirrors the bivalve's saline freshness in a pairing of pure regional logic.")
    PAIR(prod1a, "Thai green curry with jasmine rice", "contrast", "classic", "main", "The wine's high acidity and citrus precision cut through Thai coconut cream richness while the mineral backbone cools chilli heat in one of Riesling's most celebrated international pairings.")
    PAIR(prod1a, "Roasted barramundi with lemon myrtle butter", "complement", "established", "main", "Australian barramundi with a native botanical butter finds its perfect companion in the country's finest Riesling — regional identity expressed through both food and wine.")
    PAIR(prod1a, "Aged goat cheese with quince paste", "complement", "established", "cheese", "The wine's lime zest and mineral precision cut through the lactic tang of aged goat cheese while the quince bridges the fruit.")

p1b = P("Wendouree Cellars", "Australia", r1, description="Clare Valley's most enigmatic and revered producer — a tiny, historic estate producing minuscule quantities of Shiraz, Cabernet, Malbec and Riesling from 130-year-old ungrafted vines in a style that has barely changed since the 1890s. Wendouree wines are among Australia's most sought-after and age-worthy, with a mailing list of decades' duration.")
prod1b, new1b = PROD("Wendouree Riesling Clare Valley", "wine_still", p1b, r1, "Australia",
    subcategory="Riesling",
    description="One of Australia's most historically significant wines — Riesling from pre-phylloxera ungrafted vines over 130 years old, produced in tiny quantities using unchanged 1890s techniques, creating a wine of extraordinary concentration, mineral depth and aging potential that is unique in the Australian wine landscape.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Steamed mud crab with chilli and ginger", "complement", "established", "main", "The wine's concentration and citrus intensity match the sweetness of Australian mud crab with a heat-and-ginger note that bridges the lime minerality.")
    PAIR(prod1b, "Salt-and-pepper squid with lemon aioli", "complement", "classic", "starter", "The wine's focused lime-mineral character is a classic partner for southern Australian calamari — crisp acidity cutting through the fried coating and echoing the lemon.")
    PAIR(prod1b, "Yabbies with herb butter and sourdough", "complement", "classic", "main", "Australia's native freshwater crayfish with its greatest white wine — both expressing Australian terroir in their finest forms.")
    PAIR(prod1b, "Aged Clare Valley cheddar with apple", "complement", "established", "cheese", "Local aged cheddar with the valley's most celebrated white — apple acidity and mineral depth bridge the sharp cheese beautifully.")

# ── 2. Mornington Peninsula (Australia/Victoria) ──────────────────────────────
print("\n=== Mornington Peninsula (Australia) ===")
r2 = R("Mornington Peninsula", "Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Mornington Peninsula GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Australia's most respected cool-climate fine wine region, the Mornington Peninsula southeast of Melbourne is a maritime-influenced peninsula between Port Phillip Bay and Bass Strait producing Pinot Noir, Chardonnay and Pinot Gris of Burgundian elegance and regional distinctiveness. The region's combination of ancient volcanic basalt and limestone soils, maritime cooling and long growing season enables Australia's most complex and age-worthy Pinot Noir and Chardonnay expressions, attracting comparison with great Burgundy at competitive prices.",
    key_producers="Stonier, Port Phillip Estate, Ten Minutes by Tractor, Paringa Estate, Kooyong",
    historical_context="The Mornington Peninsula's wine history began in earnest in the 1970s when Nat White established Main Ridge Estate and pioneers recognised the peninsula's Burgundy-like potential. The region attracted Melbourne's wealthy professional class who established boutique wineries as weekend escapes, building a culture of small-lot, quality-focused production. Today the Peninsula is home to 200+ producers on approximately 600 hectares — one of Australia's most densely planted premium regions — with a vibrant agritourism scene.")

VIN(r2, 2023, "excellent", "stable", "Outstanding maritime season; Pinot Noir of exceptional elegance and silky texture")
VIN(r2, 2022, "very_good", "stable", "Warm year with good fruit concentration; generous Chardonnay and structured Pinot")
VIN(r2, 2021, "excellent", "stable", "Fine balance; elegant Peninsula Pinot and mineral Chardonnay of great complexity")
VIN(r2, 2020, "very_good", "stable", "Good vintage; Peninsula character of red fruit finesse and maritime mineral preserved")
VIN(r2, 2019, "exceptional", "rising", "One of Mornington Peninsula's finest vintages; concentrated, complex Pinot Noir of benchmark quality")

p2a = P("Paringa Estate", "Australia", r2, description="Mornington Peninsula's most celebrated and internationally recognised producer, Lindsay McCall's estate consistently achieves scores that place it among Australia's finest Pinot Noir producers, with meticulous small-lot winemaking from estate vineyards that have made Paringa Estate Pinot Noir one of the country's most coveted red wines.")
prod2a, new2a = PROD("Paringa Estate Estate Pinot Noir Mornington Peninsula", "wine_still", p2a, r2, "Australia",
    subcategory="Pinot Noir",
    description="One of Australia's most celebrated Pinot Noirs — Paringa Estate's flagship red from estate vineyards on the Mornington Peninsula's red volcanic basalt soils, showing extraordinary silky tannin, dark cherry, earth and iron mineral complexity that rewards 10–15 years of cellaring and rivals great Burgundy Premier Cru in its best vintages.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Crispy-skinned Barossa duck breast with cherry reduction", "complement", "classic", "main", "Australian duck with one of its finest Pinot Noirs — the wine's red cherry and iron mineral character frame the duck's rich fat with elegant Burgundian-style precision.")
    PAIR(prod2a, "Pan-roasted Victorian rabbit with mustard and tarragon", "complement", "established", "main", "Light-fleshed game with silky Peninsula Pinot — the wine's delicate tannins and red fruit complement rabbit without overwhelming its gentle character.")
    PAIR(prod2a, "Roasted King Island brie with truffle honey", "complement", "established", "cheese", "Australia's finest washed-rind cheese from Bass Strait's King Island with the Peninsula's greatest Pinot — a maritime pairing of extraordinary character.")
    PAIR(prod2a, "Wild mushroom and thyme tart with gruyere", "complement", "classic", "main", "Pinot Noir's affinity for forest mushroom earthiness is perfectly expressed here — the Peninsula's iron-mineral Pinot bridges the truffle-earthy mushroom tart.")

p2b = P("Ten Minutes by Tractor", "Australia", r2, description="One of Mornington Peninsula's most ambitious and internationally celebrated producers, combining three single-vineyard estate sites to produce benchmark Pinot Noir and Chardonnay that consistently earn top scores and have established the Peninsula as one of Australia's most exciting fine wine regions.")
prod2b, new2b = PROD("Ten Minutes by Tractor Estate Chardonnay Mornington Peninsula", "wine_still", p2b, r2, "Australia",
    subcategory="Chardonnay",
    description="A Burgundy-benchmark Chardonnay from Mornington Peninsula limestone and basalt — showing white peach, citrus, hazelnut and mineral complexity with fine oak integration and the linear acidity that distinguishes the Peninsula's finest Chardonnays and gives them 8–12 years of extraordinary aging potential.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Butter-poached South Australian king prawns with vermouth", "complement", "classic", "main", "The wine's texture and maritime mineral character frame Australian king prawns with elegant Burgundian-influenced precision.")
    PAIR(prod2b, "Crab linguine with chilli, lemon and parsley", "complement", "established", "main", "Mornington Peninsula's coastal setting makes local crab with its finest Chardonnay a natural pairing — the wine's citrus and hazelnut frame crab's sweetness and chilli heat.")
    PAIR(prod2b, "Roasted chicken with tarragon and cream sauce", "complement", "classic", "main", "Chardonnay's most universal food pairing is elevated here by the Peninsula's mineral-driven style — the wine's texture and acidity cut through cream while its fruit mirrors the chicken's richness.")
    PAIR(prod2b, "Aged King Island brie with toasted almonds", "complement", "established", "cheese", "The wine's hazelnut notes and creamy texture find a natural mirror in the washed-rind brie, with almonds linking both the wine and cheese's nutty character.")

# ── 3. Niagara Peninsula (Canada/Ontario) ─────────────────────────────────────
print("\n=== Niagara Peninsula (Canada) ===")
r3 = R("Niagara Peninsula", "Canada",
    beverage_family="wine",
    designation_type="VQA",
    designation_name="Niagara Peninsula VQA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Canada's most important wine region, situated between Lake Ontario and Lake Erie in southern Ontario, where the lakes moderate the harsh continental climate to enable fine vinifera cultivation. Niagara is world-famous for Icewine from Vidal and Riesling grapes — among the finest and most consistently produced sweet wines in the world — but also produces excellent Pinot Noir, Chardonnay, Cabernet Franc and Riesling table wines of international quality and recognition.",
    key_producers="Inniskillin, Jackson-Triggs, Peller Estates, Henry of Pelham, Tawse Winery",
    historical_context="Niagara's wine industry was established by Loyalists after the American Revolution, though serious vinifera viticulture only began in the 1970s. Karl Kaiser and Donald Ziraldo's Inniskillin received Canada's first post-Prohibition commercial winery licence in 1975. The 1991 gold medal for Inniskillin Icewine at Vinexpo in Bordeaux established Canada's international wine identity and created global demand for Canadian Icewine that continues to grow. Niagara's VQA (Vintners Quality Alliance) system, established in 1988, provides Canada's most rigorous wine appellation framework.")

VIN(r3, 2023, "excellent", "stable", "Excellent Niagara vintage; fine Chardonnay and Cab Franc with outstanding Icewine harvest conditions")
VIN(r3, 2022, "very_good", "stable", "Good year with balanced ripeness; reliable Icewine conditions in January")
VIN(r3, 2021, "excellent", "stable", "Elegant and precise; benchmark Niagara Riesling and Chardonnay with excellent acidity")
VIN(r3, 2020, "very_good", "stable", "Consistent year with good Cab Franc concentration and classic Icewine conditions")
VIN(r3, 2019, "excellent", "rising", "Outstanding Niagara year; concentrated, age-worthy table wines and spectacular Icewine harvest")

p3a = P("Inniskillin Wines", "Canada", r3, description="The historic pioneer of Canadian fine wine and the estate that put Canadian Icewine on the world map, Karl Kaiser and Donald Ziraldo's Inniskillin established Canada's most iconic wine identity with their Vidal Icewine — which won the Grand Prix d'Honneur at Vinexpo 1991 — and remains the benchmark for Canadian dessert wine worldwide.")
prod3a, new3a = PROD("Inniskillin Vidal Icewine Niagara Peninsula VQA", "wine_dessert", p3a, r3, "Canada",
    subcategory="Vidal",
    description="Canada's most internationally celebrated wine — Vidal grapes harvested frozen at -10°C or colder, pressed immediately to extract the ultra-concentrated nectar of extraordinary apricot, peach, honey and tropical fruit intensity balanced by natural Vidal acidity that prevents cloyingness and gives the wine remarkable freshness and aging potential.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Foie gras terrine with brioche and fig compote", "complement", "classic", "starter", "Canada's greatest sweet wine with the world's greatest luxury liver — the Icewine's intense sweetness and high acidity create the perfect tension with foie gras richness in a pairing of extraordinary luxury.")
    PAIR(prod3a, "Aged Stilton with candied walnuts", "complement", "classic", "cheese", "The wine's intense sweetness and tropical fruit depth complement Stilton's pungent blue intensity in the classic sweet wine and blue cheese contrast pairing.")
    PAIR(prod3a, "Apple tarte tatin with creme fraiche", "complement", "established", "dessert", "The wine's apricot and peach fruit echo apple tart's caramelised richness while the high acidity balances the dessert's sweetness.")
    PAIR(prod3a, "Fresh pineapple with ginger cream", "complement", "established", "dessert", "The wine's tropical fruit character mirrors pineapple's sweetness while the ginger bridges the wine's spice notes in a dessert pairing of tropical abundance.")

p3b = P("Tawse Winery", "Canada", r3, description="Canada's most acclaimed organic and biodynamic winery, Tawse's Niagara Peninsula estate consistently produces the finest Chardonnay and Pinot Noir table wines in Canada, winning Canadian Winery of the Year multiple times with meticulous vineyard management and minimal-intervention winemaking that expresses the Peninsula's finest terroir.")
prod3b, new3b = PROD("Tawse Robyn's Block Chardonnay Niagara Peninsula VQA", "wine_still", p3b, r3, "Canada",
    subcategory="Chardonnay",
    description="Canada's most celebrated Chardonnay — from Tawse's organically farmed Robyn's Block vineyard on the Niagara Escarpment, showing extraordinary mineral precision, citrus, white peach and hazelnut complexity with impeccably integrated oak that rivals good Burgundy Premier Cru and represents the pinnacle of Canadian white wine achievement.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Ontario pickerel with brown butter and capers", "complement", "classic", "main", "The Great Lakes' most prized freshwater fish with Canada's finest Chardonnay — mineral precision and citrus acidity frame the delicate walleye with understated Canadian elegance.")
    PAIR(prod3b, "Lobster bisque with cognac and cream", "complement", "established", "starter", "The wine's texture and mineral depth handle lobster bisque richness with aplomb, the hazelnut notes bridging the bisque's nutty cognac base.")
    PAIR(prod3b, "Chicken supreme with morel mushroom cream sauce", "complement", "classic", "main", "Chardonnay's most classical pairing — cream, mushroom and chicken — executed with the Niagara's distinctive mineral freshness preventing heaviness.")
    PAIR(prod3b, "Aged Canadian cheddar from Balderson with Niagara pear", "complement", "classic", "cheese", "A proudly Canadian pairing — the country's finest white wine with aged domestic cheddar and local Niagara Peninsula pear in regional harmony.")

# ── 4. Constantia (South Africa) ─────────────────────────────────────────────
print("\n=== Constantia (South Africa) ===")
r4 = R("Constantia", "South Africa",
    beverage_family="wine",
    designation_type="WO",
    designation_name="Constantia WO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="South Africa's oldest wine-producing region and one of the world's most historic appellations, Constantia lies in the Southern Peninsula of Cape Town where the Atlantic and Indian Oceans moderate the warm South African climate. The granitic slopes below Table Mountain produce Sauvignon Blanc of extraordinary mineral precision, elegant Semillon and the legendary Vin de Constance — the sweet Muscat wine that made this the most celebrated wine in 18th-century Europe and is now being revived to world-class quality by Klein Constantia.",
    key_producers="Klein Constantia, Buitenverwachting, Groot Constantia, Steenberg, Constantia Uitsig",
    historical_context="Governor Simon van der Stel established the Constantia farm in 1685 on land granted by the Dutch East India Company. The estate's sweet Muscat wine — Vin de Constance — became the most coveted wine in Europe, sought by Napoleon Bonaparte, Frederick the Great and Jane Austen's heroines. After the estate's division and decline in the 19th century, Klein Constantia revived Vin de Constance in 1986 with meticulous historical research, creating a modern dessert wine of extraordinary historical resonance and genuine quality.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Cape vintage; Constantia Sauvignon Blanc and Semillon of remarkable mineral precision")
VIN(r4, 2022, "very_good", "stable", "Good year with characteristic mineral freshness; excellent Sauvignon Blanc acidity")
VIN(r4, 2021, "excellent", "stable", "Elegant and precise; benchmark Constantia dry white vintage and fine Vin de Constance conditions")
VIN(r4, 2020, "very_good", "stable", "Reliable year with the Peninsula's characteristic Atlantic freshness preserved")
VIN(r4, 2019, "exceptional", "rising", "One of Constantia's finest vintages in a decade; spectacular quality across all styles")

p4a = P("Klein Constantia Estate", "South Africa", r4, description="The most historically significant wine estate in the Southern Hemisphere, Klein Constantia revived Napoleon's favourite wine — Vin de Constance — in 1986 and now produces it to world-class standard, alongside excellent Sauvignon Blanc and Semillon table wines from their historic Cape Peninsula vineyards.")
prod4a, new4a = PROD("Klein Constantia Vin de Constance Constantia WO", "wine_dessert", p4a, r4, "South Africa",
    subcategory="Muscat de Frontignan",
    description="The revival of one of history's most famous wines — sweet Muscat from Klein Constantia's historic Cape Peninsula vineyards, made in the tradition that made Constantia wine the favourite of Napoleon, Bismarck and the courts of 18th-century Europe; showing extraordinary rose petal, apricot, orange blossom and honey character with balancing natural acidity that gives this dessert wine remarkable freshness and 20+ years of aging potential.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Foie gras torchon with brioche and quince", "complement", "classic", "starter", "Napoleon's favourite wine with France's greatest luxury product — Vin de Constance's perfumed sweetness and high acidity create the perfect counterpoint to foie gras in a pairing of historic European gastronomy.")
    PAIR(prod4a, "Stilton with port-soaked walnuts and dried apricots", "complement", "classic", "cheese", "The wine's rose petal and apricot aromatics find perfect complement in Stilton's pungent blue character, the dried apricot creating a flavour bridge between wine and cheese.")
    PAIR(prod4a, "Creme brulee with candied orange zest", "complement", "established", "dessert", "The wine's orange blossom and citrus zest character mirrors the caramelised brulee with extraordinary aromatic harmony.")
    PAIR(prod4a, "Almond tart with honey and lavender cream", "complement", "established", "dessert", "The wine's honey and floral notes echo the lavender cream and almond pastry in a dessert pairing of perfumed Mediterranean elegance.")

p4b = P("Buitenverwachting", "South Africa", r4, description="One of Constantia's finest and most consistent producers, Buitenverwachting (Beyond Expectation) produces a superb range of table wines — particularly their benchmark Sauvignon Blanc and Christine Bordeaux blend — that represent some of South Africa's finest quality alongside the historic estate's conservation-minded farming practices.")
prod4b, new4b = PROD("Buitenverwachting Sauvignon Blanc Constantia WO", "wine_still", p4b, r4, "South Africa",
    subcategory="Sauvignon Blanc",
    description="One of South Africa's finest Sauvignon Blancs — from Constantia's Peninsula granitic slopes with Atlantic Ocean influence, producing a wine of extraordinary mineral-textural complexity, flinty mineral, citrus peel, Cape gooseberry and gentle Atlantic salinity that places it among the world's finest expressions of the variety.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Saldanha Bay oysters with lemon and sea salt", "complement", "classic", "starter", "South African oysters from the cold Atlantic with the Cape Peninsula's finest white — oceanic mineral character shared between wine and shellfish in pure geographic logic.")
    PAIR(prod4b, "Cape Malay fish curry with turmeric and coriander", "complement", "established", "main", "The wine's bright citrus-mineral character and natural freshness provide the perfect counterpoint to Cape Malay curry's warm spice profile in a South African cultural pairing.")
    PAIR(prod4b, "Grilled linefish with lemon butter and samphire", "complement", "classic", "main", "Cape linefish — snoek, yellowtail or kabeljou — with the Peninsula's finest Sauvignon Blanc create South Africa's most natural coastal wine-food pairing.")
    PAIR(prod4b, "Crottin de Chavignol goat cheese with herb salad", "complement", "classic", "cheese", "Sauvignon Blanc's classic cheese pairing — Loire-style goat cheese mirrors the wine's mineral freshness and citrus character even at the tip of Africa.")

# ── 5. Hunter Valley (Australia/NSW) ─────────────────────────────────────────
print("\n=== Hunter Valley (Australia) ===")
r5 = R("Hunter Valley", "Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Hunter Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Australia's most historic wine region and one of the world's most distinctive, the Hunter Valley north of Sydney produces Semillon of extraordinary ageability and Shiraz of unmistakable earthy character. Hunter Valley Semillon — released young but at only 10–11% alcohol, bone dry and intensely citrus-mineral — undergoes a remarkable transformation in bottle, developing honey, toast, lanolin and petrol complexity over 10–20 years into one of the world's most unique and compelling aged white wine experiences. Old-vine Hunter Shiraz produces earthy, leathery wines of genuine terroir character.",
    key_producers="Tyrrell's Wines, Brokenwood, McWilliam's Mount Pleasant, Keith Tulloch, De Luliis",
    historical_context="The Hunter Valley's wine history began in 1820 when John Macarthur planted the first vines, making it one of Australia's oldest wine regions. George Wyndham's Dalwood estate (1828) established the commercial foundation. The Semillon style was codified in the late 19th century and Hunter Semillon became Australia's most distinctive regional wine identity — a style found nowhere else in the world. The Hunter suffered from declining quality in the mid-20th century but a quality renaissance from the 1970s — led by Tyrrell's and McWilliam's — restored its reputation as one of Australia's great wine regions.")

VIN(r5, 2023, "very_good", "stable", "Good Hunter season; Semillon of fine citrus precision and classic aging potential")
VIN(r5, 2022, "excellent", "stable", "Outstanding vintage; Semillon of exceptional mineral focus and structure for long ageing")
VIN(r5, 2021, "good", "stable", "Challenging but good; skilled producers made authentic Hunter Semillon and earthy Shiraz")
VIN(r5, 2020, "very_good", "stable", "Reliable year; classic Hunter character preserved despite warm growing conditions")
VIN(r5, 2019, "excellent", "rising", "One of Hunter's finest recent vintages; concentrated, structured Semillon built for 15–20 years")

p5a = P("Tyrrell's Wines", "Australia", r5, description="Hunter Valley's most internationally celebrated winery and the pioneering force behind aged Hunter Semillon's global recognition, Murray Tyrrell's estate has been producing benchmark Vat 1 Semillon since 1962 — a wine widely regarded as Australia's most unique and historically significant white wine that demonstrates like no other the rewards of extended cellaring.")
prod5a, new5a = PROD("Tyrrell's Vat 1 Hunter Valley Semillon", "wine_still", p5a, r5, "Australia",
    subcategory="Semillon",
    description="Australia's most historically significant and distinctive white wine — Hunter Valley Semillon released at 10.5% alcohol and just 6 months after harvest, bone dry, intensely citrus-mineral and searingly austere when young; after 10–15 years in bottle it transforms into a golden, honeyed, toasty complexity unlike any other white wine in the world.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Aged Tyrrell's Vat 1 Semillon (10+ years) with grilled prawns", "complement", "classic", "main", "Mature Hunter Semillon's honey-toast complexity and preserved acidity create the definitive partnership with Australian prawns — a wine-food pairing of national cultural significance.")
    PAIR(prod5a, "Sydney rock oysters with aged Semillon and verjus", "complement", "classic", "starter", "Hunter Valley's most beloved local pairing — aged Semillon from the lower Hunter with Sydney Basin oysters, the wine's toasty lanolin complexity perfectly matching the oyster's saline ocean character.")
    PAIR(prod5a, "Grilled John Dory with lemon butter and asparagus", "complement", "established", "main", "The wine's citrus-mineral precision (young) or honeyed toast complexity (aged) creates the definitive partnership with Australia's most prized flatfish.")
    PAIR(prod5a, "Gouda aged 2 years with mustard and rye", "complement", "established", "cheese", "Aged Semillon's developed complexity and nutty-toasty character mirrors aged Gouda's caramel-crystalline depth in a pairing of parallel transformation.")

p5b = P("Brokenwood Wines", "Australia", r5, description="One of the Hunter Valley's most respected estates and a pioneer of quality winemaking in the region, Brokenwood produces the iconic Graveyard Vineyard Shiraz — Australia's most celebrated Hunter Shiraz — alongside benchmark Semillon and the ILR Reserve that demonstrate the Hunter's capacity for both white and red wines of extraordinary complexity and longevity.")
prod5b, new5b = PROD("Brokenwood Graveyard Vineyard Shiraz Hunter Valley", "wine_still", p5b, r5, "Australia",
    subcategory="Shiraz",
    description="Australia's most celebrated Hunter Valley Shiraz and one of the country's most iconic red wines — from the legendary Graveyard Vineyard's ancient vines on red volcanic basalt, producing a wine of extraordinary earthy complexity, leather, dark plum and iron mineral character with the soft, dusty tannins that define great Hunter Shiraz and age magnificently for 25+ years.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "Hunter Valley lamb rack with rosemary and garlic jus", "complement", "classic", "main", "The wine's earthy, iron-mineral character with fine Hunter tannins frames lamb with aristocratic restraint that rewards both young and mature drinking.")
    PAIR(prod5b, "Twice-cooked duck leg with beetroot and walnuts", "complement", "established", "main", "Duck's rich fat and the earthy iron-mineral character of Hunter Shiraz create a pairing of remarkable depth and regional authenticity.")
    PAIR(prod5b, "Braised oxtail with Hunter red wine and mushrooms", "complement", "classic", "main", "Gelatinous braised oxtail's richness and the wine's deep earthy complexity create the Hunter Valley's most satisfying red wine-food pairing.")
    PAIR(prod5b, "Aged Australian cheddar with quince and crackers", "complement", "established", "cheese", "The wine's earthy depth and fine tannin structure frame aged cheddar's sharpness while quince bridges the Hunter Shiraz's plummy fruit.")

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
