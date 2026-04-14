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

# ── REGION 1: Willamette Valley AVA (USA/Oregon) ─────────────────────────────
print("\n=== Region 1: Willamette Valley ===")
r1 = R("Willamette Valley", "USA", "wine",
    designation_type="AVA", designation_name="Willamette Valley AVA",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The Willamette Valley is Oregon's pre-eminent wine region and America's benchmark for cool-climate Pinot Noir, stretching 100 miles south from Portland between the Coast Range and the Cascades. The marine-influenced climate, volcanic Jory clay soil and ancient Missoula flood sediments create Pinot Noirs of extraordinary complexity, red fruit, earthy depth, and structural elegance that consistently challenge Burgundy in quality and ambition.",
    key_producers="Domaine Drouhin Oregon, Adelsheim, Elk Cove, Cristom, Ponzi",
    historical_context="Oregon's wine industry took off after David Lett (Eyrie Vineyards) proved Pinot Noir's potential in the early 1970s. The pivotal moment came at the Gault-Millau Wine Olympiades in 1979 when Eyrie's Pinot Noir finished second to Drouhin's Chambolle-Musigny, prompting Robert Drouhin to send his daughter Véronique to establish Domaine Drouhin Oregon in 1987. The Willamette Valley AVA was established in 1983.")

VIN(r1, 2023, "very_good", "rising", "Excellent Willamette vintage; Pinot Noir showed classic Oregonian red fruit and earth with good concentration and natural freshness")
VIN(r1, 2022, "excellent", "rising", "Outstanding vintage across the valley; benchmark Willamette Pinot with exceptional depth, structure, and 15-year aging potential")
VIN(r1, 2021, "excellent", "rising", "One of Oregon's finest recent vintages; extraordinary concentration and complexity from cool growing season and ideal harvest conditions")
VIN(r1, 2020, "good", "stable", "Smoke-affected vintage; clean sites showed good Pinot character with the valley's typical elegance despite challenging conditions")
VIN(r1, 2019, "excellent", "rising", "Benchmark vintage with classic Willamette character; red cherry, earth, and silky tannins in fine balance")

prod1a_id = P("Domaine Drouhin Oregon", "USA", r1, "winery",
    "The French house that validated Oregon's Pinot Noir potential; Véronique Drouhin-Boss has maintained Burgundian principles in the Willamette Valley for over 35 years, producing wines that are simultaneously distinctly Oregonian and profoundly Burgundian in their elegance and quality.")
prod1a, new1a = PROD("Domaine Drouhin Oregon Pinot Noir", "wine_still", prod1a_id, r1, "USA",
    subcategory="red", price_tier="premium",
    description="The reference Oregon Pinot Noir; Drouhin's estate wine from Dundee Hills Jory clay blended with select Willamette Valley parcels. Red cherry, raspberry, truffle earth, and silky Burgundian texture. More refined than most American Pinots — the benchmark for Willamette Valley elegance over power.")
if new1a:
    PAIR(prod1a, "Pan-roasted duck breast with Oregon wild mushroom reduction and beet purée", "complement", "classic", "main",
        "Pacific Northwest duck with local wild mushrooms and beet is Oregon's signature Pinot Noir food pairing; earthy depth meets the wine's red fruit and silky tannin")
    PAIR(prod1a, "Grilled wild salmon with pinot noir butter sauce and sorrel", "complement", "established", "fish_course",
        "Oregon's signature Willamette Valley pairing: Pacific wild salmon with a Pinot Noir beurre rouge — both Oregon's greatest products united on the plate")
    PAIR(prod1a, "Truffled mushroom risotto with aged Parmigiano and micro herbs", "complement", "classic", "main",
        "Oregon black truffle with mushroom risotto amplifies Drouhin's earthy Pinot complexity; Parmigiano adds umami salinity to match the wine's mineral depth")
    PAIR(prod1a, "Roasted Dungeness crab with drawn butter and sourdough", "complement", "adventurous", "main",
        "Pacific Northwest Dungeness crab with light Pinot Noir is an Oregon fine dining classic; the wine's acidity cuts crab's richness while red fruit complements the sweetness")

prod1b_id = P("Cristom Vineyards", "USA", r1, "winery",
    "One of the Willamette Valley's most acclaimed biodynamic estates; Paul Gerrie's Cristom produces single-vineyard Pinot Noirs named after women in the family (Jessie, Louise, Marjorie) from estate Jory clay vineyards in the Eola-Amity Hills sub-AVA — consistently among Oregon's finest.")
prod1b, new1b = PROD("Cristom Louise Vineyard Pinot Noir", "wine_still", prod1b_id, r1, "USA",
    subcategory="red", price_tier="premium",
    description="Cristom's flagship Louise Vineyard Pinot Noir from Eola-Amity Hills Jory clay; whole-cluster fermented for complexity. Dark cherry, forest floor, dried herbs, volcanic mineral, and silky tannin. One of Oregon's most consistently excellent single-vineyard Pinots with remarkable aging potential.")
if new1b:
    PAIR(prod1b, "Roasted quail with Oregon chanterelles, pancetta, and thyme", "complement", "classic", "main",
        "Small game bird with Pacific Northwest chanterelles is a natural match for Louise Vineyard's forest floor and wild herb complexity")
    PAIR(prod1b, "Beef short rib with Oregon pinot noir jus and celery root gratin", "complement", "established", "main",
        "Short rib's rich collagen and Pinot-based jus create a self-referential culinary unity with Cristom's concentrated Pinot Noir")
    PAIR(prod1b, "Aged Tillamook Cheddar with Oregon honey and hazelnut", "bridge", "established", "cheese",
        "Oregon's celebrated Pacific Cheddar with local honey and hazelnuts — hazelnuts are the Willamette Valley's great agricultural product — bridges Louise's red fruit and earth")
    PAIR(prod1b, "Smoked Pacific salmon with crème fraîche and pickled red onion", "complement", "established", "starter",
        "Smoked Pacific salmon's richness and acidity from the pickled onion are excellent matches for Louise Vineyard's whole-cluster herbal complexity and bright acidity")

# ── REGION 2: Walla Walla Valley AVA (USA/Washington) ───────────────────────
print("\n=== Region 2: Walla Walla Valley ===")
r2 = R("Walla Walla Valley", "USA", "wine",
    designation_type="AVA", designation_name="Walla Walla Valley AVA",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Walla Walla Valley is Washington State's most prestigious wine appellation, a semi-arid inland valley that extends into Oregon. Bordeaux varieties — Cabernet Sauvignon, Merlot, and Cabernet Franc — are the focus for reds, with Syrah increasingly celebrated. The extreme diurnal temperature variation, volcanic basalt soils, and long dry growing season create wines of exceptional concentration, mineral depth, and elegance.",
    key_producers="Leonetti Cellar, L'Ecole No. 41, Cayuse Vineyards, Woodward Canyon",
    historical_context="Walla Walla's wine industry took off with Gary Figgins's Leonetti Cellar in 1978, which quickly gained national recognition for Merlot and Cabernet. The AVA was established in 1984. The 1990s saw a wave of new producers, and Cayuse Vineyards' volcanic basalt Syrah from the 2000s established the appellation's Syrah credentials internationally. Today Walla Walla commands Washington's highest wine prices.")

VIN(r2, 2022, "excellent", "rising", "Outstanding Walla Walla vintage; Cabernet and Syrah achieved exceptional concentration with the volcanic basalt soils providing fine mineral structure")
VIN(r2, 2021, "very_good", "stable", "Fine balanced year with classic Walla Walla character; dark fruit and mineral complexity with good tannic structure")
VIN(r2, 2020, "excellent", "rising", "Powerful vintage; concentrated and mineral Cabernet and Syrah with exceptional aging potential")
VIN(r2, 2019, "very_good", "rising", "Benchmark vintage with excellent depth and typical Walla Walla mineral precision from the volcanic basalt terroir")
VIN(r2, 2018, "good", "stable", "Accessible year with good varietal typicity; softer tannins and approachable dark fruit character for earlier drinking")

prod2a_id = P("Leonetti Cellar", "USA", r2, "winery",
    "The founding estate of Walla Walla's reputation; Gary Figgins established Leonetti in 1978 and produced Merlot that became Washington's first nationally celebrated wine. The family estate maintains allocations-only access — among the Pacific Northwest's most sought-after wines.")
prod2a, new2a = PROD("Leonetti Cellar Walla Walla Cabernet Sauvignon", "wine_still", prod2a_id, r2, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Leonetti's flagship Walla Walla Cabernet Sauvignon: estate fruit from volcanic basalt soils with small amounts of Merlot and Cabernet Franc. Dark cassis, cedar, graphite, tobacco, and mineral precision. Allocation-only with extraordinary demand — one of Washington's most historically significant wines.")
if new2a:
    PAIR(prod2a, "Bone-in dry-aged ribeye with bone marrow compound butter and roasted garlic", "complement", "classic", "main",
        "The ultimate steakhouse pairing for a serious Walla Walla Cabernet; bone marrow fat and dry-aged beef intensity match Leonetti's concentration and cedar depth")
    PAIR(prod2a, "Slow-braised prime short rib with truffle polenta and bordelaise", "complement", "classic", "main",
        "Braised short rib with truffle polenta is the Northwest fine dining classic for Washington's greatest Cabernet; bordelaise sauce mirrors the wine's cedar structure")
    PAIR(prod2a, "Aged Beecher's Flagship Cheddar with fig preserve and walnut", "bridge", "established", "cheese",
        "Washington's celebrated artisan Cheddar with fig and walnut bridges Leonetti's dark fruit; a Pacific Northwest cheese course pairing of genuine local authenticity")
    PAIR(prod2a, "Venison loin with huckleberry reduction and celeriac purée", "complement", "established", "main",
        "Pacific Northwest venison with local huckleberry mirrors the wine's dark berry fruit; the mineral celeriac bridges to Leonetti's volcanic basalt terroir")

prod2b_id = P("Cayuse Vineyards", "USA", r2, "winery",
    "The cult producer that established Walla Walla's Syrah credentials; Christophe Baron's biodynamic estate on volcanic basalt cobblestone terraces produces some of America's most critically acclaimed and expensive Syrah — single-vineyard wines that achieve Rhône Valley complexity in a distinctly Pacific Northwest context.")
prod2b, new2b = PROD("Cayuse En Chamberlin Syrah", "wine_still", prod2b_id, r2, "USA",
    subcategory="red", price_tier="ultra_premium",
    description="Cayuse's single-vineyard Syrah from the basalt cobblestone En Chamberlin site — America's most Rhône-like vineyard condition. Black cherry, smoked meat, violet, iron mineral, and volcanic depth. Biodynamic; unfined and unfiltered. Among America's most sought-after and expensive Syrahs with extraordinary aging potential.")
if new2b:
    PAIR(prod2b, "Grilled leg of lamb with rosemary, lavender, and Pacific Northwest olive oil", "complement", "classic", "main",
        "Washington lamb with Provençal herbs and local olive oil meets Cayuse's Rhône-influenced Syrah character; the pairing mirrors a Côte Rôtie lamb combination in a Pacific Northwest context")
    PAIR(prod2b, "Wild boar sausage with pickled peppers and grilled polenta", "complement", "established", "main",
        "Pacific Northwest wild boar with its earthy richness and char matches Cayuse Syrah's smoked meat character; pickled peppers add brightness to cut the weight")
    PAIR(prod2b, "Roasted duck with cherry-Syrah reduction and root vegetable hash", "complement", "classic", "main",
        "Duck with Syrah reduction creates culinary continuity with Cayuse's wine; cherry mirrors the dark fruit while root vegetables add earthy Pacific Northwest character")
    PAIR(prod2b, "Smoked brisket with Korean BBQ glaze and pickled daikon", "complement", "adventurous", "casual",
        "The smoke and umami of Korean-influenced smoked brisket creates a bold match for Cayuse's smoked meat character; the pickled daikon cuts through both")

# ── REGION 3: McLaren Vale (Australia) ───────────────────────────────────────
print("\n=== Region 3: McLaren Vale ===")
r3 = R("McLaren Vale", "Australia", "wine",
    designation_type="GI", designation_name="McLaren Vale GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="McLaren Vale is South Australia's most distinctive wine region, situated between the Mount Lofty Ranges and Gulf St Vincent on the Fleurieu Peninsula. The Mediterranean climate, ancient schist and ironstone soils, and proximity to the cooling sea create Shiraz and Grenache of remarkable complexity — dense, spiced, and chocolatey with Mediterranean herb character. The region is also home to some of Australia's finest Cabernet Sauvignon and old-vine Grenache.",
    key_producers="d'Arenberg, Wirra Wirra, Kay Brothers, Yangarra Estate",
    historical_context="McLaren Vale's first vineyards were planted in 1838 by John Reynell. By the 1900s the region was producing significant volumes for the British market. The modern quality era began in the 1980s-90s when producers like Chester d'Arenberg focused on terroir-specific wines. The region's 150-year-old Shiraz and Grenache vines (among Australia's oldest) have become internationally recognised as irreplaceable viticultural heritage.")

VIN(r3, 2022, "excellent", "rising", "Outstanding McLaren Vale vintage; Shiraz achieved exceptional depth and Mediterranean complexity with the ironstone terroir providing fine mineral structure")
VIN(r3, 2021, "very_good", "stable", "Fine balanced year with classic McLaren Vale character; dark chocolate, black olive, and spiced Shiraz well expressed")
VIN(r3, 2020, "good", "stable", "Slightly challenging year; bush fire smoke affected some parcels but clean sites showed excellent typicity")
VIN(r3, 2019, "excellent", "rising", "Benchmark vintage; extraordinary old-vine Shiraz depth and Mediterranean herb complexity from the ancient schist terroir")
VIN(r3, 2018, "very_good", "stable", "Classic vintage with excellent aging potential; old vine Grenache and Shiraz showing remarkable concentration and balance")

prod3a_id = P("d'Arenberg", "Australia", r3, "winery",
    "McLaren Vale's most celebrated and internationally recognised estate; Chester d'Arenberg's eccentric, passionate estate produces a vast range of terroir-specific single-vineyard wines from the region's oldest Shiraz and Grenache vines — including the legendary Dead Arm Shiraz from ancient 80-year-old vines.")
prod3a, new3a = PROD("d'Arenberg Dead Arm Shiraz", "wine_still", prod3a_id, r3, "Australia",
    subcategory="red", price_tier="premium",
    description="d'Arenberg's iconic Dead Arm Shiraz from 80-year-old vines affected by the 'dead arm' viticultural disease that concentrates berries. Dark chocolate, black cherry, dried herbs, coffee, and ironstone mineral depth. One of Australia's most consistent and celebrated Shiraz benchmarks — 20+ year aging potential.")
if new3a:
    PAIR(prod3a, "Slow-braised lamb shoulder with harissa, preserved lemon, and couscous", "complement", "classic", "main",
        "North African-influenced slow lamb with harissa matches Dead Arm's spiced dark fruit and Mediterranean herb; preserved lemon's acidity brightens the pairing")
    PAIR(prod3a, "Grilled beef short rib with dark chocolate mole and grilled corn", "complement", "adventurous", "main",
        "Dark chocolate mole's bitterness echoes Dead Arm's chocolate note precisely; the beef's fat richness meets the wine's tannic concentration")
    PAIR(prod3a, "Aged Barossa Shiraz Cheddar with quince paste and pecan", "bridge", "established", "cheese",
        "Australian artisan Shiraz-washed Cheddar with quince bridges Dead Arm's dark fruit; pecans add Southern Hemisphere nuttiness")
    PAIR(prod3a, "Kangaroo loin with native pepperberry, bush tomato, and wattleseed jus", "complement", "adventurous", "main",
        "Native Australian ingredients with kangaroo's lean iron richness create an indigenous Australian pairing for Dead Arm's McLaren Vale terroir")

prod3b_id = P("Yangarra Estate", "Australia", r3, "winery",
    "One of McLaren Vale's most celebrated Grenache and Rhône-variety specialists; Yangarra's biodynamic estate from ancient Grenache vines produces some of Australia's most elegant and mineral expressions of the variety — a counterpoint to the region's typical rich, dense Shiraz style.")
prod3b, new3b = PROD("Yangarra High Sands Grenache", "wine_still", prod3b_id, r3, "Australia",
    subcategory="red", price_tier="premium",
    description="Yangarra's flagship old-vine McLaren Vale Grenache from the High Sands sandy soils where the oldest Grenache vines (90+ years) grow. Delicate, silky, and profoundly mineral — raspberry, dried rose, earth, and ironstone precision. Australia's most elegant and Burgundian expression of old-vine Grenache.")
if new3b:
    PAIR(prod3b, "Roasted lamb rump with za'atar, pomegranate, and tabbouleh", "complement", "established", "main",
        "Middle Eastern-inspired lamb with tabbouleh's fresh herbs and pomegranate's sweet-tart character bridges old-vine Grenache's delicate raspberry and mineral depth")
    PAIR(prod3b, "Duck confit with cherry conserve and Provençal vegetables", "complement", "classic", "main",
        "Old vine Grenache and duck confit with cherry — the Southern Rhône's classic pairing translated to McLaren Vale — works perfectly with Yangarra's silky, mineral style")
    PAIR(prod3b, "Warm wild mushroom salad with goat cheese, pine nuts, and truffle oil", "complement", "established", "starter",
        "Wild mushroom's earthy depth with truffle oil mirrors the wine's mineral soil character; goat cheese adds dairy freshness to match Grenache's silky texture")
    PAIR(prod3b, "Aged Manchego with fig jam and toasted almonds", "bridge", "classic", "cheese",
        "Manchego's sheep milk richness and fig's sweetness bridge Yangarra's red fruit; almonds add Mediterranean nuttiness to echo the old vine Grenache's mineral depth")

# ── REGION 4: Uco Valley (Argentina) ─────────────────────────────────────────
print("\n=== Region 4: Uco Valley ===")
r4 = R("Uco Valley", "Argentina", "wine",
    designation_type="appellation", designation_name="Valle de Uco",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The Uco Valley is Argentina's most exciting and rapidly evolving wine region, situated at high altitude (900-1500m) in the Andes foothills south of Mendoza. The extreme altitude, dramatic diurnal temperature variation, limestone and alluvial terroir, and intense Andean sunlight produce Argentina's finest Malbec alongside excellent Cabernet Franc, Chardonnay, and other varieties. The sub-zones of Gualtallary, Altamira, and Tupungato are increasingly internationally recognised.",
    key_producers="Zuccardi Valle de Uco, Achaval Ferrer, Clos de los Siete, Viña Cobos",
    historical_context="The Uco Valley's viticultural potential was recognised in the 1990s when producers sought higher altitudes to escape Mendoza's increasing heat. Zuccardi's move to the valley in 1999 was transformative; their Concreto wine from La Consulta's alluvial limestone soils achieved international benchmark status. The valley's success has driven a property boom, with many international producers establishing estates in Gualtallary's rocky, high-altitude terrain.")

VIN(r4, 2022, "excellent", "rising", "Outstanding Uco Valley vintage; altitude and Andean conditions allowed exceptional Malbec concentration with fine aromatic freshness")
VIN(r4, 2021, "very_good", "stable", "Fine balanced year with excellent Malbec depth and characteristic Uco mineral precision from the limestone-alluvial terroir")
VIN(r4, 2020, "excellent", "rising", "Benchmark vintage; extraordinary high-altitude Malbec concentration with remarkable violet aromatics and mineral structure")
VIN(r4, 2019, "very_good", "rising", "Classic Uco Valley vintage with excellent depth and the distinctive mineral freshness that distinguishes high-altitude Malbec")
VIN(r4, 2018, "good", "stable", "Good year with accessible Malbec character; some of the valley's highest sites showing excellent freshness and mineral definition")

prod4a_id = P("Zuccardi Valle de Uco", "Argentina", r4, "winery",
    "The most celebrated estate of the Uco Valley and increasingly recognised as Argentina's finest winery; Sebastian Zuccardi's earthquake-designed, gravity-fed winery produces single-village, single-vineyard Malbec and other varieties from across the valley's diverse terroirs — wines achieving global benchmark status.")
prod4a, new4a = PROD("Zuccardi Concreto Malbec", "wine_still", prod4a_id, r4, "Argentina",
    subcategory="red", price_tier="premium",
    description="Zuccardi's concrete-fermented Malbec from La Consulta's alluvial limestone soils in the Uco Valley; mineral, fresh, and precise — a counterpoint to the typical plush Malbec style. Violet, dark cherry, limestone mineral, and extraordinary freshness. One of Argentina's most internationally celebrated and innovative Malbec expressions.")
if new4a:
    PAIR(prod4a, "Asado de tira (Argentinian short rib over wood fire) with chimichurri", "complement", "classic", "main",
        "Argentina's defining food-wine pairing: short rib over wood fire with chimichurri and Malbec is the country's cultural identity; Zuccardi's freshness cuts the fat beautifully")
    PAIR(prod4a, "Empanadas de carne with cumin, olive, and hard-boiled egg", "complement", "classic", "casual",
        "Argentina's iconic hand pies with spiced beef filling are the casual pairing for Uco Valley Malbec; the wine's freshness and dark fruit complement the warm spice")
    PAIR(prod4a, "Matambre arrollado (rolled beef flank) with roasted peppers and chimichurri", "complement", "established", "starter",
        "Argentina's famous stuffed rolled beef with peppers and herbs is the elegant starter pairing for the Concreto's mineral freshness and violet depth")
    PAIR(prod4a, "Grilled lamb chops with Andean herb salsa and roasted vegetables", "complement", "classic", "main",
        "High Andean lamb's delicacy and herb salsa are natural matches for Concreto's fresh, mineral Malbec character — a Mendoza mountain pairing of pure terroir")

prod4b_id = P("Viña Cobos", "Argentina", r4, "winery",
    "The collaboration between Paul Hobbs and the Peña family producing some of the Uco Valley's most internationally acclaimed Malbec; Marchiori Vineyard's Malbec from ancient pre-phylloxera vines in Luján de Cuyo has achieved cult status while the Uco Valley operation focuses on high-altitude precision.")
prod4b, new4b = PROD("Viña Cobos Felino Malbec Uco Valley", "wine_still", prod4b_id, r4, "Argentina",
    subcategory="red", price_tier="mid_range",
    description="Viña Cobos's accessible Uco Valley Malbec: high-altitude fruit from multiple sub-zones producing violet, dark cherry, and chocolate depth with the valley's characteristic mineral freshness. Outstanding value for the quality — the entry point to Paul Hobbs's Argentina project.")
if new4b:
    PAIR(prod4b, "Choripán (Argentine chorizo sandwich) with chimichurri and salsa criolla", "complement", "classic", "casual",
        "Argentina's greatest street food — grilled chorizo in a crusty roll with chimichurri — and Malbec is the country's most iconic casual food-wine pairing")
    PAIR(prod4b, "Milanesa napolitana (breaded veal with tomato, ham, and mozzarella)", "complement", "classic", "main",
        "Argentina's beloved Italian-Argentine fusion dish with its rich tomato and cheese topping pairs effortlessly with Felino Malbec's soft tannins and dark fruit")
    PAIR(prod4b, "Papas al horno with roasted garlic, rosemary, and Chimichurri", "complement", "established", "casual",
        "Simple Argentinian roasted potatoes with herbs and garlic amplify Malbec's dark fruit in the most straightforward and honest South American pairing")
    PAIR(prod4b, "Slow-roasted lamb shoulder with Mendoza mountain herbs and merquén", "complement", "classic", "main",
        "Andean lamb with merquén (Chilean smoked chilli) and mountain herbs is the high-altitude South American pairing for Uco Valley's fresh, mineral Malbec")

# ── REGION 5: San Antonio Valley (Chile) ────────────────────────────────────
print("\n=== Region 5: San Antonio Valley ===")
r5 = R("San Antonio Valley", "Chile", "wine",
    designation_type="appellation", designation_name="Valle de San Antonio DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The San Antonio Valley is Chile's most exciting cool-climate wine region, situated close to the Pacific coast south of Santiago where the Humboldt Current's cold influence creates ideal conditions for Pinot Noir, Chardonnay, and Sauvignon Blanc. The sub-zones of Leyda (the coolest) and Lo Abarca produce wines of extraordinary freshness and mineral precision that rival Burgundy and Marlborough in aromatic intensity.",
    key_producers="Casa Marin, Matetic Vineyards, Viñedo Chadwick (Leyda label), Amayna",
    historical_context="The San Antonio Valley's wine industry is remarkably young — Maria Luz Marin planted the first vines at Casa Marin in 1999, having to build an aqueduct to irrigate the fog-draped hills. The Leyda sub-zone was officially recognised as a separate denomination in 2002. The region has grown rapidly as Chile's answer to cool-climate Burgundian varieties, with international producers recognising the unique coastal influence on wine quality.")

VIN(r5, 2023, "excellent", "rising", "Outstanding San Antonio vintage; cool Pacific influence produced exceptional Pinot and Sauvignon freshness with remarkable mineral precision")
VIN(r5, 2022, "very_good", "stable", "Fine balanced year with characteristic coastal freshness; Sauvignon Blanc and Pinot Noir showing excellent typicity")
VIN(r5, 2021, "good", "stable", "Good year with classic coastal character; fresh, aromatic wines with fine acidity and mineral definition")
VIN(r5, 2020, "excellent", "rising", "Benchmark vintage; extraordinary Leyda mineral precision and cool-climate complexity across all varieties")
VIN(r5, 2019, "very_good", "rising", "Classic San Antonio vintage with excellent Pinot Noir depth and saline mineral freshness from the Pacific influence")

prod5a_id = P("Casa Marin", "Chile", r5, "winery",
    "The pioneering estate that established Chile's cool-coastal wine potential; Maria Luz Marin's visionary Leyda estate proved that Chile's best whites and Pinot Noirs come from the Pacific coast, not the warm Central Valley — a paradigm-shifting discovery that reshaped Chilean wine geography.")
prod5a, new5a = PROD("Casa Marin Sauvignon Blanc Cipreses Vineyard", "wine_still", prod5a_id, r5, "Chile",
    subcategory="white", price_tier="premium",
    description="Casa Marin's flagship Sauvignon Blanc from the Leyda Valley's Cipreses Vineyard; intense and mineral with grapefruit, passion fruit, fresh herbs, and a distinctive salinity from the Humboldt Current's coastal fog. Among Chile's finest Sauvignon Blanc — rivalling Sancerre and Marlborough in mineral freshness.")
if new5a:
    PAIR(prod5a, "Ceviche de corvina with ají amarillo, lime, and choclo (Peruvian-style)", "complement", "classic", "starter",
        "Pacific coastal ceviche — Peru's great contribution — with its lime acid and chilli heat is perfectly mirrored by San Antonio Sauvignon's citrus mineral character")
    PAIR(prod5a, "Clams casino with white wine, bacon, and lemon", "complement", "established", "starter",
        "Pacific clams with bacon and white wine echo San Antonio Sauvignon's salinity and citrus; the coastal terroir connection is direct and genuine")
    PAIR(prod5a, "Grilled sea bass (lubina) with capers, herb oil, and roasted fennel", "complement", "classic", "fish_course",
        "Pacific sea bass with caper brine and fennel frond amplifies Sauvignon Blanc's green herb and mineral character; the coastal pairing is archetypal")
    PAIR(prod5a, "Fresh goat cheese with cucumber, dill, and lemon zest", "bridge", "classic", "starter",
        "Fresh chèvre with green herb and cucumber bridges San Antonio Sauvignon's Loire-like freshness; dill adds Nordic herb contrast to the Pacific coastal character")

prod5b_id = P("Matetic Vineyards", "Chile", r5, "winery",
    "One of San Antonio Valley's most ambitious and quality-focused organic estates; the Matetic family's coastal estate produces excellent Pinot Noir, Sauvignon Blanc, and Syrah from Leyda sub-zone vineyards that show the valley's capacity for genuine cool-climate complexity.")
prod5b, new5b = PROD("Matetic EQ Pinot Noir", "wine_still", prod5b_id, r5, "Chile",
    subcategory="red", price_tier="mid_range",
    description="Matetic's organic coastal Pinot Noir from Leyda; fresh red cherry, dried herbs, and saline mineral precision from the Pacific-influenced San Antonio Valley. More restrained and mineral than most Chilean reds — closer to an Oregon or Burgundy style than typical Chilean Pinot. Excellent value for cool-climate Pinot of genuine character.")
if new5b:
    PAIR(prod5b, "Grilled salmon with lemon herb butter and quinoa salad", "complement", "established", "fish_course",
        "Pacific salmon and cool-climate Chilean Pinot Noir is the San Antonio Valley answer to Oregon's salmon-Pinot pairing; mineral freshness and light tannin make it work")
    PAIR(prod5b, "Roasted free-range chicken with herbs, white wine, and potato gratin", "complement", "classic", "main",
        "Free-range chicken with herb and wine pan sauce is the universal cool-climate Pinot pairing; Matetic's freshness and mineral precision are ideal companions")
    PAIR(prod5b, "Mushroom and leek tart with aged Gruyère and thyme", "complement", "established", "main",
        "Earthy mushroom and leek tart with alpine cheese amplifies the Leyda Pinot's delicate forest floor notes and mineral depth")
    PAIR(prod5b, "Pulled duck with hoisin, cucumber, and micro herbs in rice paper", "complement", "adventurous", "casual",
        "Duck with hoisin's sweet-sour complexity is an unusual but effective pairing for light Pinot Noir; the Asian-inspired wrap format suits the wine's freshness")

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
print("Done.")
conn.close()
