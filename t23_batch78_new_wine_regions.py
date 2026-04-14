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
        return (row[0], False)
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return (pid, True)

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 78 ──────────────────────────────────────────────────────────────────
# Regions: Hawke's Bay, Khao Yai, Valle de Guadalupe, Eden Valley, Gisborne

# ── Region 1: Hawke's Bay ─────────────────────────────────────────────────────
print("\n=== Region 1: Hawkes Bay ===")
r1 = R("Hawke's Bay", "New Zealand", "wine",
    designation_type="GI",
    designation_name="Hawke's Bay GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="New Zealand's second-largest wine region on the North Island's east coast, producing the country's finest Syrah, Merlot-dominant reds and Chardonnay from the Gimblett Gravels — a unique alluvial gravel deposit of unparalleled heat retention.",
    key_producers="Craggy Range, Te Mata Estate, Trinity Hill, Elephant Hill, Clearview Estate",
    historical_context="Hawke's Bay was settled by Marist missionaries who established the Mission Estate in 1851 — New Zealand's oldest winery; the discovery of the Gimblett Gravels in the 1980s unlocked the region's potential for world-class Bordeaux-variety reds."
)
VIN(r1, 2022, "excellent", "rising", "Outstanding Hawke's Bay vintage; Syrah of exceptional purity and Chardonnay of great mineral tension.")
VIN(r1, 2021, "very_good", "stable", "Good quality; wines show balance and the Gimblett Gravels' characteristic warmth and structure.")
VIN(r1, 2020, "excellent", "rising", "Benchmark year; Craggy Range Le Sol Syrah and Trinity Hill Homage both exceptional.")
VIN(r1, 2019, "very_good", "stable", "Good overall; consistent quality from both the Gimblett Gravels and Bridge Pa vineyards.")
VIN(r1, 2018, "good", "stable", "Reliable vintage; approachable reds with good early drinking pleasure.")

p1a = P("Craggy Range", "winery", r1, "New Zealand",
    production_philosophy="terroir_expression",
    philosophy_description="Hawke's Bay's most internationally acclaimed estate for Syrah and Merlot-blend Le Sol from the Gimblett Gravels, alongside exceptional Pinot Noir from Martinborough.",
    reputation_narrative="Craggy Range Le Sol Syrah is New Zealand's most acclaimed Syrah; the estate defines the Gimblett Gravels' potential for world-class red wine.",
    price_positioning="ultra_premium")
prod1a, new1a = PROD("Craggy Range Le Sol Syrah", "wine_still", p1a, r1, "New Zealand",
    subcategory="Syrah",
    description="New Zealand's greatest Syrah from Gimblett Gravels: violet, dark plum, smoked olive, white pepper and iron with Rhône-like elegance and Hawke's Bay sunshine — exceptional and age-worthy.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Roasted rack of lamb with rosemary and garlic jus", "complement", "classic", "main", "New Zealand's finest lamb with its finest Syrah is the ultimate expression of national terroir pride.")
    PAIR(prod1a, "Venison loin with beetroot, walnut and thyme", "complement", "established", "main", "New Zealand game and Gimblett Gravels Syrah; beetroot's iron echoes the wine's mineral depth.")
    PAIR(prod1a, "Slow-cooked beef short rib with bone marrow gremolata", "complement", "classic", "main", "Rich braised beef and Syrah's dark fruit and pepper form a classic northern Rhône-influenced pairing.")
    PAIR(prod1a, "Aged Kāpiti Kikorangi (NZ blue cheese) with manuka honey", "contrast", "established", "cheese", "Bold NZ blue and complex Syrah; manuka honey bridges the wine's dark fruit and the cheese's salt.")

p1b = P("Te Mata Estate", "winery", r1, "New Zealand",
    production_philosophy="traditional",
    philosophy_description="New Zealand's oldest operating winery (1896) producing the legendary Coleraine Cabernet-Merlot blend and Elston Chardonnay from Hawke's Bay's historic vineyards.",
    reputation_narrative="Te Mata Coleraine is New Zealand's most iconic Bordeaux-variety blend; it has defined Hawke's Bay for generations and remains the country's most age-worthy red.",
    price_positioning="ultra_premium")
prod1b, new1b = PROD("Te Mata Coleraine", "wine_still", p1b, r1, "New Zealand",
    subcategory="Cabernet Sauvignon blend",
    description="New Zealand's most iconic Bordeaux-style blend: Cabernet Sauvignon, Merlot and Cabernet Franc from historic Hawke's Bay vineyards — blackcurrant, cedar, olive, tobacco and silky, age-worthy tannins.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Rack of lamb with herb crust and flageolet beans", "complement", "classic", "main", "Classic Bordeaux-style wine with classic Bordeaux-style preparation; New Zealand lamb's quality matches the wine.")
    PAIR(prod1b, "Duck breast with cherry and five-spice sauce", "complement", "established", "main", "Dark fruit sauce mirrors the wine's cassis and cedar; five-spice adds an Asian bridge to NZ wine.")
    PAIR(prod1b, "Aged Cheddar (Mainland Vintage) with quince paste", "complement", "established", "cheese", "New Zealand's great aged Cheddar with its greatest Cabernet blend; quince bridges the wine's dark fruit.")
    PAIR(prod1b, "Beef Wellington with mushroom duxelles and Dijon", "complement", "classic", "main", "The ultimate special-occasion beef preparation with New Zealand's most special Bordeaux-style red.")

# ── Region 2: Khao Yai ────────────────────────────────────────────────────────
print("\n=== Region 2: Khao Yai ===")
r2 = R("Khao Yai", "Thailand", "wine",
    designation_type="GI",
    designation_name="Khao Yai GI",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Thailand's premier wine region in the Nakhon Ratchasima uplands at 300–500m, producing Shiraz, Chenin Blanc, Tempranillo and blends from a tropical continental climate moderated by altitude and monsoon cooling.",
    key_producers="GranMonte, Silverlake Vineyard, PB Valley Khao Yai Winery, Siam Winery",
    historical_context="Thailand's wine industry began in earnest with PB Valley in 1989; Khao Yai has emerged as Southeast Asia's premier wine destination, with GranMonte leading quality production at an internationally competitive level."
)
VIN(r2, 2023, "very_good", "rising", "Strong monsoon management; Shiraz and Chenin Blanc show improved freshness and balance.")
VIN(r2, 2022, "excellent", "rising", "Outstanding Thai vintage; GranMonte Family Reserve Shiraz earned international recognition.")
VIN(r2, 2021, "good", "stable", "Consistent quality; wine tourism and hospitality driving rapid quality improvement.")
VIN(r2, 2020, "very_good", "rising", "Good harvest; Thai wines demonstrating genuine terroir character for the first time at scale.")
VIN(r2, 2019, "good", "stable", "Reliable vintage; tropical climate management improving with technology investment.")

p2a = P("GranMonte", "winery", r2, "Thailand",
    production_philosophy="terroir_expression",
    philosophy_description="Khao Yai's most internationally acclaimed estate, led by Nikki Lohitnavy, producing the benchmark Family Reserve Syrah and Asoke Valley Chenin Blanc from Thailand's finest upland vineyards.",
    reputation_narrative="GranMonte is Southeast Asia's most award-winning winery; Nikki Lohitnavy has been named one of Asia's best winemakers; the estate represents Thai wine's best global argument.",
    price_positioning="premium")
prod2a, new2a = PROD("GranMonte Family Reserve Syrah", "wine_still", p2a, r2, "Thailand",
    subcategory="Syrah",
    description="Southeast Asia's most acclaimed red wine: Thai Syrah with violet, dark plum, white pepper and tropical spice from Khao Yai's altitude — proves that serious wine can come from tropical Asia.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Crying tiger beef salad with lime, fish sauce and chilli", "complement", "established", "main", "Thai beef salad is a natural expression of Southeast Asian terroir meeting the wine's dark fruit and pepper.")
    PAIR(prod2a, "Grilled lamb chops with lemongrass and galangal crust", "complement", "established", "main", "Herb-spiced lamb bridging Southeast Asian spice and the wine's pepper and fruit character.")
    PAIR(prod2a, "Duck larb with toasted rice, lime and herbs", "complement", "adventurous", "main", "Thai duck salad and Thai Syrah — shared terroir, shared spice, dramatically different styles in harmony.")
    PAIR(prod2a, "Massaman beef curry with coconut, peanut and potato", "complement", "established", "main", "Mild aromatic curry and medium-bodied Syrah; spice weight is similar, dark fruit bridges the coconut.")

p2b = P("PB Valley Khao Yai Winery", "winery", r2, "Thailand",
    production_philosophy="traditional",
    philosophy_description="Thailand's pioneer wine estate, established 1989 by Piya Bhirombhakdi; the oldest and most historically significant wine producer in Southeast Asia, producing Chenin Blanc and Tempranillo.",
    reputation_narrative="PB Valley is Thailand's founding fine wine estate; its long track record of consistent production established credibility for Thai wine when few believed it possible.",
    price_positioning="mid_range")
prod2b, new2b = PROD("PB Valley Khao Yai Chenin Blanc", "wine_still", p2b, r2, "Thailand",
    subcategory="Chenin Blanc",
    description="Thailand's most established white wine: Khao Yai Chenin Blanc with tropical fruit, honey, lemongrass and fresh acidity — lively and expressive of Southeast Asia's unique growing conditions.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Steamed sea bass with ginger, soy and sesame oil", "complement", "established", "main", "Delicate steamed fish and fresh white wine; ginger bridges the wine's tropical fruit and aromatic complexity.")
    PAIR(prod2b, "Tom kha gai (coconut chicken soup with galangal)", "complement", "classic", "main", "Thailand's most beloved soup and a Thai wine with similar tropical aromatic notes — a unique national pairing.")
    PAIR(prod2b, "Spring rolls with sweet chilli dipping sauce", "complement", "established", "starter", "Light fried parcels with fresh Chenin Blanc; the wine's acidity and fruit bridge the dipping sauce's sweetness.")
    PAIR(prod2b, "Green mango salad with dried shrimp and lime", "complement", "established", "casual", "Green mango's tartness aligns with Chenin's acidity; tropical fruit in both wine and dish unite.")

# ── Region 3: Valle de Guadalupe ──────────────────────────────────────────────
print("\n=== Region 3: Valle de Guadalupe ===")
r3 = R("Valle de Guadalupe", "Mexico", "wine",
    designation_type="DO",
    designation_name="Valle de Guadalupe DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Baja California's premium wine valley 90km south of San Diego, producing diverse, bold Mediterranean varieties — Nebbiolo, Tempranillo, Grenache, Cabernet Sauvignon and Chardonnay — in a near-desert climate moderated by Pacific fog.",
    key_producers="Monte Xanic, L.A. Cetto, Vena Cava, Bodegas de Santo Tomás, Adobe Guadalupe",
    historical_context="Dominican missionaries planted Baja's first vines in 1791; the modern Valley emerged in the 1980s with Monte Xanic and L.A. Cetto leading the quality revolution; today Valle de Guadalupe is Latin America's most exciting emerging wine destination."
)
VIN(r3, 2022, "excellent", "rising", "Exceptional Baja California vintage; Mediterranean varieties show ideal concentration and freshness.")
VIN(r3, 2021, "very_good", "stable", "Good quality; wines from the valley continue to improve in elegance and food-friendliness.")
VIN(r3, 2020, "good", "stable", "Consistent vintage; bold, expressive wines with the valley's characteristic intensity.")
VIN(r3, 2019, "excellent", "rising", "Benchmark year; Vena Cava Big Blend and Monte Xanic Gran Ricardo both outstanding.")
VIN(r3, 2018, "very_good", "stable", "Good overall quality; the valley's wine tourism boom is driving quality investment.")

p3a = P("Monte Xanic", "winery", r3, "Mexico",
    production_philosophy="terroir_expression",
    philosophy_description="Baja California's pioneering quality estate founded 1987, producing the iconic Gran Ricardo blend and benchmark Chenin Blanc that define Mexican fine wine.",
    reputation_narrative="Monte Xanic is Mexico's most internationally recognised wine estate; Gran Ricardo is Latin America's most decorated Bordeaux-style blend outside Argentina.",
    price_positioning="premium")
prod3a, new3a = PROD("Monte Xanic Gran Ricardo", "wine_still", p3a, r3, "Mexico",
    subcategory="Cabernet Sauvignon blend",
    description="Baja California's most celebrated wine: Cabernet Sauvignon, Merlot and Cabernet Franc from valley floor gravel — blackcurrant, chocolate, cedar and ripe Mexican sunshine tannins.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Carne asada tacos with guacamole, salsa roja and lime", "complement", "classic", "casual", "Mexico's most iconic street food with its most celebrated wine is the definitive Baja cultural pairing.")
    PAIR(prod3a, "Birria de res (beef stew with chilli consommé)", "complement", "established", "main", "Rich Mexican slow-cooked beef and structured Cabernet; the chilli consommé bridges the wine's dark fruit.")
    PAIR(prod3a, "Lamb barbacoa wrapped in maguey leaves", "complement", "established", "main", "Traditional Oaxacan-influenced slow-cook method with Central Mexican wine; smoky and deeply satisfying.")
    PAIR(prod3a, "Queso Oaxaca stretched cheese with mole negro", "bridge", "established", "main", "Mole's chocolate-chilli complexity bridges the wine's dark fruit; melted cheese adds richness.")

p3b = P("Vena Cava", "winery", r3, "Mexico",
    production_philosophy="minimal_intervention",
    philosophy_description="Phil Gregory's Valle de Guadalupe natural wine estate repurposing a retired boat as a fermentation vessel; producing biodynamic Big Blend and individual variety wines with strong Mexican identity.",
    reputation_narrative="Vena Cava is one of Latin America's most original wine producers; the Big Blend is Valle de Guadalupe's most critically discussed and tourism-driving wine.",
    price_positioning="mid_range")
prod3b, new3b = PROD("Vena Cava Big Blend", "wine_still", p3b, r3, "Mexico",
    subcategory="GSM blend",
    description="Valle de Guadalupe's most creative red: Grenache, Shiraz and Mourvèdre with Tempranillo and Nebbiolo — wild berries, dried herbs, smoked meat and Mediterranean character with Baja sunshine.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Grilled octopus tostada with chipotle aioli and pickled onion", "complement", "adventurous", "starter", "The Mediterranean blend with Mexican ingredients bridges Old and New World; chipotle adds smoky spice.")
    PAIR(prod3b, "Duck carnitas with orange, cumin and fresh tortilla", "complement", "established", "main", "Duck and Grenache-dominant blend is a natural pairing; orange bridges the wine's red fruit character.")
    PAIR(prod3b, "Lamb al pastor with pineapple and achiote", "complement", "established", "main", "Spiced rotating lamb with Mediterranean-influenced blend; pineapple's acidity bridges the wine's structure.")
    PAIR(prod3b, "Cotija cheese and epazote quesadilla", "bridge", "suggested", "casual", "Mexican aged cheese and the valley's most food-versatile red; epazote herbs bridge the wine's dried herb character.")

# ── Region 4: Eden Valley ─────────────────────────────────────────────────────
print("\n=== Region 4: Eden Valley ===")
r4 = R("Eden Valley", "Australia", "wine",
    designation_type="GI",
    designation_name="Eden Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="High-altitude subregion of the Barossa Valley at 400–550m, producing Australia's most age-worthy Riesling and distinctive Shiraz, including the iconic Henschke Hill of Grace from a vineyard planted in the 1860s.",
    key_producers="Henschke, Pewsey Vale, Eden Hall, Mountadam, Leo Buring",
    historical_context="Henschke Hill of Grace is planted with vines from the 1860s — among the world's oldest commercially producing Shiraz vines; Eden Valley gave the Barossa region its cool-climate Riesling credentials alongside its hot-climate Shiraz."
)
VIN(r4, 2022, "excellent", "rising", "Outstanding Eden Valley vintage; Riesling of extraordinary mineral precision and Shiraz of rare elegance.")
VIN(r4, 2021, "very_good", "stable", "Good quality; altitude moderation preserved freshness across both white and red varieties.")
VIN(r4, 2020, "excellent", "rising", "Benchmark year; Pewsey Vale Riesling and Henschke Hill of Grace both exceptional.")
VIN(r4, 2019, "very_good", "stable", "Good quality; Eden Valley Riesling showing exceptional cellaring potential.")
VIN(r4, 2018, "good", "stable", "Consistent vintage; reliable, food-friendly wines across the region.")

p4a = P("Henschke", "winery", r4, "Australia",
    production_philosophy="traditional",
    philosophy_description="The Henschke family estate producing Australia's most celebrated wine — Hill of Grace Shiraz — from 160-year-old vines in Eden Valley; also celebrated for Keyneton Euphonium and Cyrill Henschke Cabernet.",
    reputation_narrative="Henschke Hill of Grace is Australia's most prestigious wine; it consistently ranks with Penfolds Grange as one of the country's two greatest red wines, and its old-vine Shiraz pedigree is globally revered.",
    price_positioning="ultra_premium")
prod4a, new4a = PROD("Henschke Hill of Grace", "wine_still", p4a, r4, "Australia",
    subcategory="Shiraz",
    description="Australia's most legendary wine: old-vine Eden Valley Shiraz from pre-phylloxera 1860s plantings — blueberry, dark plum, smoked meat, eucalyptus, leather and an extraordinary mineral complexity that develops for 30+ years.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Roasted saddle of kangaroo with bush tomato and quandong", "complement", "classic", "main", "Australia's iconic indigenous game with Australia's most iconic wine — the ultimate expression of national terroir.")
    PAIR(prod4a, "Braised beef cheeks with bone marrow gremolata", "complement", "classic", "main", "Rich slow-cooked beef and old-vine Shiraz's complexity require each other to achieve their best expression.")
    PAIR(prod4a, "Aged King Island Cloth-Bound Cheddar with quince", "complement", "established", "cheese", "Australia's finest aged cheese with its finest wine; quince bridges the wine's dark fruit and leather.")
    PAIR(prod4a, "Dark chocolate soufflé with raspberry coulis", "complement", "suggested", "dessert", "The wine's dark fruit and complexity create an extraordinary mirror with bitter chocolate; a rare indulgence.")

p4b = P("Pewsey Vale Estate", "winery", r4, "Australia",
    production_philosophy="terroir_expression",
    philosophy_description="Yalumba-owned high-altitude Eden Valley estate dedicated to Riesling from a historic vineyard first planted in 1847; produces Australia's most celebrated and consistently age-worthy Riesling.",
    reputation_narrative="Pewsey Vale The Contour Riesling is Australia's benchmark for dry, mineral Riesling; it demonstrates the Eden Valley's capacity to rival German and Alsatian Riesling in complexity and longevity.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Pewsey Vale The Contour Riesling", "wine_still", p4b, r4, "Australia",
    subcategory="Riesling",
    description="Australia's benchmark aged Riesling from Eden Valley altitude: lime zest, apple, white flower, slate and emerging toast and honey character with age; consistently one of Australia's finest whites for 10+ years.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled barramundi with lemon myrtle and finger lime", "complement", "classic", "main", "Australian fish with Australian Riesling; finger lime's citrus mirrors the wine's lime and mineral drive.")
    PAIR(prod4b, "Green Thai curry with prawns and jasmine rice", "complement", "classic", "main", "Riesling's acidity and aromatic tension manage Thai herb-spice heat while amplifying the coconut sweetness.")
    PAIR(prod4b, "Smoked trout with horseradish crème fraîche and rye", "complement", "established", "starter", "Smoked fish and German-heritage Australian Riesling; horseradish's heat bridges the wine's mineral edge.")
    PAIR(prod4b, "Mild curry puffs with yoghurt dipping sauce", "complement", "suggested", "casual", "Australian multicultural street food with Australian Riesling; spice is tamed, freshness amplified.")

# ── Region 5: Gisborne ────────────────────────────────────────────────────────
print("\n=== Region 5: Gisborne ===")
r5 = R("Gisborne", "New Zealand", "wine",
    designation_type="GI",
    designation_name="Gisborne GI",
    reputation_tier="respected",
    quality_trajectory="established",
    description="New Zealand's easternmost wine region on the East Coast of the North Island, known as the Chardonnay Capital of New Zealand, producing rich, tropical Chardonnay, Gewürztraminer and Pinot Gris.",
    key_producers="Millton Vineyard, Matawhero, TW Wines, Indevin",
    historical_context="Gisborne is New Zealand's oldest European settlement and one of the first places in the world to see the new day; the warm, humid climate produces lush, tropical whites that contrast with Marlborough's crisp Sauvignon Blanc and Central Otago's elegant Pinot Noir."
)
VIN(r5, 2022, "very_good", "stable", "Good Gisborne vintage; Chardonnay shows tropical richness and Gewürztraminer excellent aromatic intensity.")
VIN(r5, 2021, "excellent", "rising", "Outstanding year; Millton La Cote Chardonnay and Matawhero Gewürztraminer both produced exceptional wines.")
VIN(r5, 2020, "good", "stable", "Consistent quality; tropical Chardonnay of immediate appeal and good food versatility.")
VIN(r5, 2019, "very_good", "stable", "Good season; Pinot Gris showed particular success with aromatic richness and texture.")
VIN(r5, 2018, "good", "stable", "Reliable vintage; Chardonnay producers delivered consistently appealing tropical-style wines.")

p5a = P("Millton Vineyard", "winery", r5, "New Zealand",
    production_philosophy="biodynamic",
    philosophy_description="New Zealand's pioneering biodynamic estate, established 1984 by James and Annie Millton; the first certified biodynamic winery in NZ and among the first in the world, producing exceptional Chardonnay and Chenin Blanc.",
    reputation_narrative="Millton Vineyard is New Zealand's most respected natural/biodynamic producer; Te Arai Chardonnay and La Cote Viognier are considered among the country's most distinguished white wines.",
    price_positioning="premium")
prod5a, new5a = PROD("Millton Te Arai Chardonnay", "wine_still", p5a, r5, "New Zealand",
    subcategory="Chardonnay",
    description="New Zealand's benchmark biodynamic Chardonnay from Gisborne: ripe nectarine, citrus butter, hazelnuts, subtle oak and tropical richness with the precision that biodynamic farming delivers.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Crayfish (New Zealand rock lobster) with herb butter", "complement", "classic", "main", "New Zealand's finest crustacean with its finest biodynamic Chardonnay is the ultimate local luxury pairing.")
    PAIR(prod5a, "Smoked kahawai (NZ native fish) with aioli and watercress", "complement", "established", "main", "Indigenous New Zealand fish and biodynamic Gisborne Chardonnay — a native terroir pairing.")
    PAIR(prod5a, "Roast chicken with tarragon, lemon and cream sauce", "complement", "classic", "main", "Classic Chardonnay pairing; rich cream and herb sauce aligns perfectly with the wine's tropical richness.")
    PAIR(prod5a, "Triple cream brie with honeycomb and toasted brioche", "bridge", "established", "cheese", "Creamy cheese and tropical Chardonnay; honeycomb bridges the wine's fruit to the cheese's richness.")

p5b = P("Matawhero Wines", "winery", r5, "New Zealand",
    production_philosophy="terroir_expression",
    philosophy_description="Historic Gisborne estate, established 1969, that put Gisborne Gewürztraminer on the New Zealand map; the single-vineyard Church Block Gewürztraminer remains the country's benchmark for the variety.",
    reputation_narrative="Matawhero Church Block Gewürztraminer is New Zealand's most celebrated Gewürztraminer; the estate was Gisborne's first fine wine producer and remains its most historically significant.",
    price_positioning="mid_range")
prod5b, new5b = PROD("Matawhero Church Block Gewürztraminer", "wine_still", p5b, r5, "New Zealand",
    subcategory="Gewürztraminer",
    description="New Zealand's benchmark Gewürztraminer from Gisborne: rose petal, lychee, ginger, Turkish delight and a distinctive floral-spice intensity; dry, rich and uniquely New Zealand in character.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Fragrant Thai green curry with kumara and coconut", "complement", "classic", "main", "Aromatic curry and floral Gewürztraminer; lychee and ginger in the wine mirror the curry's aromatics.")
    PAIR(prod5b, "Smoked duck breast with lychee and five-spice glaze", "complement", "established", "main", "Lychee in the dish mirrors the wine's primary fruit; five-spice and duck's richness align with Gewürztraminer.")
    PAIR(prod5b, "Indian-spiced lamb samosa with mango chutney", "complement", "established", "casual", "Spiced pastry and aromatic white wine; mango bridges the wine's tropical fruit character.")
    PAIR(prod5b, "Époisses washed-rind cheese with toasted walnut bread", "complement", "classic", "cheese", "Pungent cheese and perfumed Gewürztraminer is the canonical Alsatian-inspired pairing, realised in New Zealand.")

# ── Final count ───────────────────────────────────────────────────────────────
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
