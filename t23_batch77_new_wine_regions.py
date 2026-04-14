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

# ── Batch 77 ──────────────────────────────────────────────────────────────────
# Regions: Jumilla, Aglianico del Vulture, Lanzarote, Dealu Mare (Romania), Cappadocia (Turkey)

# ── Region 1: Jumilla ─────────────────────────────────────────────────────────
print("\n=== Region 1: Jumilla ===")
r1 = R("Jumilla", "Spain", "wine",
    designation_type="DO",
    designation_name="Jumilla DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Inland Murcian DO producing intense, sun-baked Monastrell (Mourvèdre) from centenarian ungrafted bush vines on limestone soils; wines of remarkable concentration, dark fruit and Mediterranean warmth.",
    key_producers="Bodegas Carchelo, Ego Bodegas, Juan Gil, Bodegas Casa de la Ermita, Luzon",
    historical_context="Jumilla's sandy limestone soils never succumbed to phylloxera; many of its centenarian Monastrell vines are ungrafted, producing concentrated wines of great authenticity and historical continuity."
)
VIN(r1, 2021, "excellent", "rising", "Outstanding Jumilla vintage; Monastrell shows extraordinary concentration and elegant tannin integration.")
VIN(r1, 2020, "very_good", "stable", "Good quality; classic Jumilla profile with deep colour, dark fruit and warming finish.")
VIN(r1, 2019, "exceptional", "rising", "Benchmark year; old-vine Monastrell of remarkable depth and ageing potential.")
VIN(r1, 2018, "good", "stable", "Consistent vintage; approachable, generous reds with immediate drinking appeal.")
VIN(r1, 2017, "very_good", "stable", "Good overall quality; Monastrell shows characteristic dark fruit, spice and earthy warmth.")

p1a = P("Juan Gil", "winery", r1, "Spain",
    production_philosophy="terroir_expression",
    philosophy_description="Family estate producing some of Jumilla's most internationally recognised Monastrell from old ungrafted vines; the Juan Gil Silver Label and Honoro Vera are benchmark Jumilla exports.",
    reputation_narrative="Juan Gil is Jumilla's most exported and internationally recognised producer; the estate defined the modern profile of quality Jumilla Monastrell.",
    price_positioning="value")
prod1a, new1a = PROD("Juan Gil Silver Label Monastrell", "wine_still", p1a, r1, "Spain",
    subcategory="Monastrell",
    description="Jumilla's benchmark accessible Monastrell — dark plum, blackberry, chocolate, warm spice and smooth tannins from old ungrafted bush vines; excellent value Mediterranean red.",
    price_tier="value")
if new1a:
    PAIR(prod1a, "Lamb kebabs with cumin, coriander and chilli", "complement", "classic", "main", "Spiced lamb and warm Monastrell share Mediterranean heritage; cumin and dark fruit align perfectly.")
    PAIR(prod1a, "Char-grilled chorizo with piquillo pepper sauce", "complement", "established", "main", "Spanish cured sausage and Spanish Monastrell; piquillo sweetness bridges the wine's dark spice.")
    PAIR(prod1a, "Beef and olive empanada with smoked paprika", "complement", "established", "starter", "The bold flavours of this savoury pastry are a natural match for Jumilla's full-bodied warmth.")
    PAIR(prod1a, "Dark chocolate and almond cake", "complement", "suggested", "dessert", "Chocolate and Monastrell's dark fruit align; almond mirrors the wine's Mediterranean warmth.")

p1b = P("Ego Bodegas", "winery", r1, "Spain",
    production_philosophy="terroir_expression",
    philosophy_description="Modern Jumilla estate producing elegantly structured Monastrell with a focus on freshness and balance rather than sheer power; Marenas and Goru are benchmark expressions.",
    reputation_narrative="Ego Bodegas Marenas is one of Spain's most critically acclaimed Monastrell expressions; the estate demonstrates Jumilla's capacity for elegance alongside power.",
    price_positioning="mid_range")
prod1b, new1b = PROD("Ego Bodegas Marenas Monastrell", "wine_still", p1b, r1, "Spain",
    subcategory="Monastrell",
    description="Elegant Jumilla Monastrell with dark berry, violet, Provençal herb, smoke and refined tannins; more restrained than typical Jumilla with genuine ageing potential.",
    price_tier="mid_range")
if new1b:
    PAIR(prod1b, "Moussaka with béchamel and lamb ragù", "complement", "established", "main", "Mediterranean lamb dish and Mediterranean Monastrell; the wine's herb note mirrors the ragù's spice.")
    PAIR(prod1b, "Wild mushroom and thyme risotto", "bridge", "suggested", "main", "Earthy mushroom and Monastrell's dark fruit create a satisfying bridge; thyme echoes the wine's herb character.")
    PAIR(prod1b, "Slow-braised pork cheeks with prunes and red wine", "complement", "established", "main", "Prune and dark fruit in both dish and wine; slow-cooked pork fat matches the wine's weight beautifully.")
    PAIR(prod1b, "Aged Manchego with fig jam and walnuts", "complement", "established", "cheese", "Spanish hard cheese and structured Monastrell; fig bridges the wine's dark fruit, walnut adds earthy depth.")

# ── Region 2: Aglianico del Vulture ───────────────────────────────────────────
print("\n=== Region 2: Aglianico del Vulture ===")
r2 = R("Aglianico del Vulture", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Aglianico del Vulture Superiore DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Basilicata's volcanic wine region centred on Monte Vulture, producing some of Italy's most age-worthy and powerful reds from Aglianico grown on ancient volcanic soils at 300–700m altitude.",
    key_producers="Paternoster, Elena Fucci, Cantine del Notaio, Re Manfredi, D'Angelo",
    historical_context="Aglianico del Vulture is known as the 'Barolo of the South'; the volcanic soils of Monte Vulture give Aglianico extraordinary mineral complexity and ageing potential, with top wines rivalling Barolo in longevity."
)
VIN(r2, 2021, "excellent", "rising", "Outstanding volcanic vintage; Aglianico of remarkable depth, structured tannins and ageing potential.")
VIN(r2, 2020, "very_good", "stable", "Good quality; classic volcanic profile with dark cherry, iron and firm structure.")
VIN(r2, 2019, "exceptional", "rising", "Generational vintage; Aglianico del Vulture of extraordinary complexity and 20-year ageing capacity.")
VIN(r2, 2018, "very_good", "stable", "Consistent quality; wines show the volcano's characteristic mineral and tannic signature.")
VIN(r2, 2017, "good", "stable", "Reliable vintage; approachable Aglianico with good dark fruit and medium-term cellaring potential.")

p2a = P("Elena Fucci", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Young winemaker producing one single wine — Titolo — from a single vineyard on Monte Vulture's eastern slopes; the concentrated focus has produced one of Italy's most critically acclaimed emerging wines.",
    reputation_narrative="Elena Fucci's Titolo is consistently ranked among Italy's greatest red wines; it is considered the reference wine for modern Aglianico del Vulture.",
    price_positioning="premium")
prod2a, new2a = PROD("Elena Fucci Titolo Aglianico del Vulture", "wine_still", p2a, r2, "Italy",
    subcategory="Aglianico",
    description="Italy's most acclaimed Aglianico del Vulture from a single Monte Vulture vineyard: dark cherry, iron, violet, volcanic mineral, liquorice and formidable but beautifully structured tannins.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Braised wild boar ragù with handmade orecchiette", "complement", "classic", "main", "Southern Italian game pasta and the South's most powerful red; iron meets iron in magnificent rustic harmony.")
    PAIR(prod2a, "Slow-roasted leg of lamb with rosemary, garlic and anchovy", "complement", "classic", "main", "The anchovy adds umami that bridges Aglianico's tannic structure; lamb fat softens the wine's grip.")
    PAIR(prod2a, "T-bone Fiorentina steak, grilled over charcoal", "complement", "established", "main", "Massive steak demands massive wine; both are fundamentally Italian and both require time to be at their best.")
    PAIR(prod2a, "Aged Caciocavallo Silano with black truffle honey", "complement", "established", "cheese", "Southern Italian stretched-curd cheese and southern Aglianico; truffle honey bridges mineral depth.")

p2b = P("Paternoster", "winery", r2, "Italy",
    production_philosophy="traditional",
    philosophy_description="The historic reference estate for Aglianico del Vulture, producing Rotondo and Don Anselmo since the 1920s — the wines that first brought international attention to Basilicata.",
    reputation_narrative="Paternoster Don Anselmo is the most celebrated traditional expression of Aglianico del Vulture; the estate is Basilicata's most historically important wine producer.",
    price_positioning="premium")
prod2b, new2b = PROD("Paternoster Don Anselmo Aglianico del Vulture", "wine_still", p2b, r2, "Italy",
    subcategory="Aglianico",
    description="The traditional benchmark Aglianico del Vulture — dark plum, cherry, volcanic earth, tobacco, dark chocolate and firm, age-worthy tannins; requires a decade of cellaring for its best expression.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Peposo (Tuscan beef tendon stew with black pepper)", "complement", "established", "main", "Long-cooked tough cut and a long-ageing southern Italian red; pepper in the dish mirrors the wine's spice.")
    PAIR(prod2b, "Lamb chops alla scottadito with lemon and oregano", "complement", "classic", "main", "Grilled lamb with southern herbs and southern Aglianico is a pure Italian meridional expression.")
    PAIR(prod2b, "Caponata with agrodolce and almonds on bruschetta", "bridge", "suggested", "starter", "Sweet-sour Sicilian aubergine bridges the wine's tannin with sugar and acidity.")
    PAIR(prod2b, "Pecorino Canestrato with chestnut honey", "complement", "established", "cheese", "Hard southern Italian cheese with structured southern Italian red; honey bridges the dark fruit and tannin.")

# ── Region 3: Lanzarote ───────────────────────────────────────────────────────
print("\n=== Region 3: Lanzarote ===")
r3 = R("Lanzarote", "Spain", "wine",
    designation_type="DO",
    designation_name="Lanzarote DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Canary Island DO producing one of the world's most extraordinary wines: Malvasía Volcánica grown in hand-dug volcanic ash pits (zocos) that harvest moisture from Atlantic mists; both dry and naturally sweet versions.",
    key_producers="El Grifo, Stratvs, Bodegas Barreto, La Geria",
    historical_context="Lanzarote's unique viticultural system — each vine planted in its own volcanic pit dug by hand — was developed after a volcanic eruption in 1730–36 buried the island's topsoil; this adversity produced one of viticulture's most unusual and beautiful landscapes, now a UNESCO Biosphere Reserve."
)
VIN(r3, 2022, "excellent", "rising", "Outstanding Canary vintage; Malvasía Volcánica shows extraordinary aromatic intensity and mineral precision.")
VIN(r3, 2021, "very_good", "stable", "Good quality; wines express the volcanic ash's distinctive mineral character.")
VIN(r3, 2020, "good", "stable", "Consistent vintage; reliable Malvasía with tropical fruit and volcanic mineral notes.")
VIN(r3, 2019, "excellent", "rising", "Benchmark year; both dry and sweet Malvasía of exceptional complexity.")
VIN(r3, 2018, "very_good", "stable", "Good season; the zocos' moisture-harvesting systems produced excellent fruit despite Atlantic winds.")

p3a = P("El Grifo", "winery", r3, "Spain",
    production_philosophy="traditional",
    philosophy_description="Lanzarote's oldest winery (1775) and most celebrated; El Grifo's Malvasía Seco and Malvasía Semidulce are Spain's most distinctive Canary Island wines and global ambassadors for this unique terroir.",
    reputation_narrative="El Grifo is Spain's oldest active winery and Lanzarote's iconic producer; the Malvasía Colección label is Spain's most internationally acclaimed Canary Island wine.",
    price_positioning="mid_range")
prod3a, new3a = PROD("El Grifo Malvasía Seco", "wine_still", p3a, r3, "Spain",
    subcategory="Malvasía Volcánica",
    description="Lanzarote's benchmark dry Malvasía: volcanic mineral, white peach, passion fruit, sea spray and distinctive flint from the zocos; unlike any other white wine in the world.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Papas arrugadas with mojo verde (wrinkled potatoes with green sauce)", "complement", "classic", "casual", "The Canary Islands' most beloved food with its most beloved wine — a pure terroir pairing of island and sea.")
    PAIR(prod3a, "Grilled lapas (limpets) with garlic and lemon butter", "complement", "classic", "starter", "Canarian rock shellfish with Canarian volcanic white; lemon butter bridges the wine's mineral-citrus note.")
    PAIR(prod3a, "Fresh tuna tartare with avocado and lime", "complement", "established", "starter", "Atlantic tuna with Atlantic island wine; avocado's fat balances the wine's acidity and passion fruit note.")
    PAIR(prod3a, "Queso de Flor (Canarian flower cheese) with wild honey", "complement", "established", "cheese", "The island's rare flower-rennet cheese with its most celebrated wine is the definitive Canarian pairing.")

p3b = P("Stratvs", "winery", r3, "Spain",
    production_philosophy="terroir_expression",
    philosophy_description="Modern Lanzarote estate producing elegant dry and natural sweet Malvasía from the volcanic zoco vineyards, combining traditional farming with modern cellar precision.",
    reputation_narrative="Stratvs is Lanzarote's most dynamic modern producer; the Malvasía Naturalmente Dulce is considered one of Spain's finest naturally sweet wines.",
    price_positioning="premium")
prod3b, new3b = PROD("Stratvs Malvasía Naturalmente Dulce", "wine_dessert", p3b, r3, "Spain",
    subcategory="Malvasía Volcánica dulce",
    description="Lanzarote's finest naturally sweet Malvasía — dried apricot, tropical fruit, caramelised orange, volcanic mineral and vibrant acidity in balance; unique and deeply individual.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Bienmesabe (Canarian almond cream dessert)", "complement", "classic", "dessert", "The island's most traditional sweet with its most celebrated sweet wine; almond mirrors the wine's dried apricot.")
    PAIR(prod3b, "Canarian goat's cheese with guava jam", "bridge", "established", "cheese", "Local semi-hard cheese and naturally sweet Malvasía; guava's tropical note bridges the wine's fruit.")
    PAIR(prod3b, "Pineapple tarte Tatin with vanilla cream", "complement", "established", "dessert", "Tropical caramelised pineapple aligns with the wine's tropical and dried fruit character.")
    PAIR(prod3b, "Roquefort with candied walnut and pear", "contrast", "established", "cheese", "Bold blue cheese and sweet Malvasía in classic sweet-wine contrast; walnut and pear mediate the intensity.")

# ── Region 4: Dealu Mare ──────────────────────────────────────────────────────
print("\n=== Region 4: Dealu Mare ===")
r4 = R("Dealu Mare", "Romania", "wine",
    designation_type="DOC",
    designation_name="Dealu Mare DOC",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Romania's most prestigious wine region in the Subcarpathian foothills of Muntenia, producing full-bodied Fetească Neagră, Cabernet Sauvignon and Merlot alongside fragrant Fetească Regală and Tămâioasă Românească whites.",
    key_producers="Davino, SERVE, Cramele Recaș, Balla Géza, Prince Știrbey",
    historical_context="Dealu Mare (Big Hill) has been a wine region since Dacian times; Romania was the 5th largest wine producer in the world during the Communist era, and the post-1989 quality revolution led by estates like Davino has been transformative."
)
VIN(r4, 2021, "excellent", "rising", "Exceptional Romanian vintage; Fetească Neagră and Cabernet of remarkable depth and elegance.")
VIN(r4, 2020, "very_good", "stable", "Good quality; balanced season producing wines of good structure and food-friendly character.")
VIN(r4, 2019, "good", "stable", "Consistent vintage; reliable, expressive wines from Romania's finest region.")
VIN(r4, 2018, "excellent", "rising", "Benchmark Dealu Mare year; Davino Flamboyant and SERVE Cuvée Charlotte drew international attention.")
VIN(r4, 2017, "very_good", "stable", "Good season; Fetească Neagră showed characteristic plum, violet and structured tannins.")

p4a = P("Davino Winery", "winery", r4, "Romania",
    production_philosophy="terroir_expression",
    philosophy_description="Romania's most internationally acclaimed estate, producing Flamboyant (Cabernet Sauvignon blend) and Revelatio (Fetească Neagră) that have earned Romania serious international wine recognition.",
    reputation_narrative="Davino Flamboyant has earned scores matching Bordeaux crus classés from leading critics; the estate is the global benchmark for Romanian fine wine.",
    price_positioning="premium")
prod4a, new4a = PROD("Davino Flamboyant", "wine_still", p4a, r4, "Romania",
    subcategory="Cabernet Sauvignon blend",
    description="Romania's most acclaimed wine: Cabernet Sauvignon with Merlot and Fetească Neagră — blackcurrant, violet, cedar, tobacco and fine tannins; demonstrates Dealu Mare's capacity for Bordeaux-class wines.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Roasted veal chop with morel cream and truffle oil", "complement", "classic", "main", "Romanian premium red wine demands an equivalent dish; morel and truffle amplify the wine's cedar and spice.")
    PAIR(prod4a, "Sarmale (Romanian cabbage rolls with pork and rice)", "complement", "classic", "main", "The national dish with the national wine — a pairing of Romanian culinary and viticultural identity.")
    PAIR(prod4a, "Lamb with wild garlic and spring herb crust", "complement", "established", "main", "Carpathian spring lamb and the Subcarpathian hills' finest red — a shared mountain terroir pairing.")
    PAIR(prod4a, "Aged Brânza de burduf (Romanian sheep cheese in fir bark)", "complement", "adventurous", "cheese", "Romania's most distinctive cheese and its finest wine; herbal fir bark wrapping bridges the wine's cedar note.")

p4b = P("SERVE Winery", "winery", r4, "Romania",
    production_philosophy="terroir_expression",
    philosophy_description="Guy and Catalina de Poix's Franco-Romanian estate producing the celebrated Cuvée Charlotte Fetească Regală and Fetească Neagră Ursu de Piatră from Dealu Mare's finest terroir.",
    reputation_narrative="SERVE's Cuvée Charlotte is Romania's most internationally distributed premium white wine; the estate combines French viticultural investment with Romanian indigenous varieties.",
    price_positioning="premium")
prod4b, new4b = PROD("SERVE Cuvée Charlotte Fetească Regală", "wine_still", p4b, r4, "Romania",
    subcategory="Fetească Regală",
    description="Romania's most elegant indigenous white: Fetească Regală (Royal Maiden) with white peach, jasmine, lemon and a distinctive mineral-aromatic finish; elegant and food-versatile.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Ciorba de perisoare (Romanian meatball soup with sour cream)", "complement", "established", "main", "The wine's freshness and acidity cut through the creamy soup; an authentically Romanian pairing.")
    PAIR(prod4b, "Grilled Danube carp with garlic and dill", "complement", "classic", "main", "Freshwater fish from Romania's great river with the country's finest white wine — a pure terroir expression.")
    PAIR(prod4b, "Mushroom and sour cream pastry (ciuperci cu smântână)", "complement", "established", "starter", "Romanian foraged mushroom preparation with aromatic white wine; sour cream bridges the acidity.")
    PAIR(prod4b, "Telemea (fresh Romanian sheep's feta) with tomatoes and herbs", "complement", "established", "cheese", "The most common Romanian fresh cheese with its finest white wine; tomato acidity bridges both.")

# ── Region 5: Cappadocia ──────────────────────────────────────────────────────
print("\n=== Region 5: Cappadocia ===")
r5 = R("Cappadocia", "Turkey", "wine",
    designation_type="GI",
    designation_name="Cappadocia GI",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Central Anatolian wine region at 1,000–1,200m altitude, one of the world's oldest wine-producing areas; producing Emir (dry white), Kalecik Karası (delicate red) and Öküzgözü from volcanic tuff soils.",
    key_producers="Kavaklıdere, Turasan, Ürgüp Bağları, Kocabağ",
    historical_context="Cappadocia's wine history stretches 5,000+ years; the Hittites worshipped wine gods here and the volcanic landscape's unique tuff formations have sheltered vineyards since antiquity. Modern Turkish wine's revival began in Cappadocia in the 1990s."
)
VIN(r5, 2022, "very_good", "rising", "Good Anatolian vintage; Emir shows freshness and Kalecik Karası elegant red fruit character.")
VIN(r5, 2021, "excellent", "rising", "Outstanding year at altitude; wines of remarkable aromatic purity and mineral definition.")
VIN(r5, 2020, "good", "stable", "Consistent quality; Emir particularly successful with crisp acidity from volcanic soils.")
VIN(r5, 2019, "very_good", "rising", "Good growing season; both red and white varieties produced wines of genuine character.")
VIN(r5, 2018, "good", "stable", "Reliable vintage; Turkish wine quality continues to improve across the region.")

p5a = P("Kavaklıdere Winery", "winery", r5, "Turkey",
    production_philosophy="traditional",
    philosophy_description="Turkey's most historically significant and largest quality wine producer, founded 1929; Kavaklıdere's Côtes d'Avanos range pioneered Cappadocian wine at the national level.",
    reputation_narrative="Kavaklıdere is Turkey's most internationally recognised wine brand; the Prestige and Angora ranges have introduced Turkish wine to export markets worldwide.",
    price_positioning="mid_range")
prod5a, new5a = PROD("Kavaklıdere Angora Emir", "wine_still", p5a, r5, "Turkey",
    subcategory="Emir",
    description="Turkey's benchmark Emir from Cappadocian volcanic soils: apple blossom, green apple, lemon, volcanic mineral and fresh acidity; crisp, food-friendly and distinctively Anatolian.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Mezze of white bean purée, hummus and roasted red pepper", "complement", "established", "starter", "Anatolian mezze tradition with Turkey's indigenous white wine — an authentic regional starting point.")
    PAIR(prod5a, "Grilled sea bream with lemon, olive oil and herbs (levrek)", "complement", "classic", "main", "Turkish Mediterranean coastal fish with Turkish white wine; herbs and lemon bridge the wine's mineral acidity.")
    PAIR(prod5a, "Börek with feta and herbs (su böreği)", "complement", "established", "casual", "Turkey's most beloved pastry with its indigenous white wine — a cultural and culinary pairing.")
    PAIR(prod5a, "Stuffed vine leaves with rice and lemon (dolma)", "complement", "established", "starter", "The grape vine provides both the wrapping and the wine; lemon bridges the wine's acidity.")

p5b = P("Turasan Winery", "winery", r5, "Turkey",
    production_philosophy="terroir_expression",
    philosophy_description="Ürgüp-based Cappadocian estate producing serious expressions of Kalecik Karası and Emir from volcanic tuff soils; one of Turkey's most artisan producers with a strong focus on indigenous varieties.",
    reputation_narrative="Turasan is one of Turkey's most critically appreciated quality producers; the Kalecik Karası is among Turkey's finest indigenous red wine expressions.",
    price_positioning="mid_range")
prod5b, new5b = PROD("Turasan Kalecik Karası", "wine_still", p5b, r5, "Turkey",
    subcategory="Kalecik Karası",
    description="Turkey's most elegant indigenous red variety from Cappadocian volcanic soils: wild strawberry, dried cherry, violet, soft tannins and remarkable lightness — Turkey's answer to Pinot Noir in weight and charm.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Adana kebab with grilled tomato, pepper and flatbread", "complement", "classic", "main", "Turkey's most beloved grilled meat with its most food-friendly red wine is the quintessential Turkish pairing.")
    PAIR(prod5b, "Slow-braised lamb shanks with apricot and saffron", "complement", "established", "main", "Turkish spiced lamb and the wine's gentle dark fruit and softness make a satisfying Anatolian combination.")
    PAIR(prod5b, "Chicken pilav with pine nuts, currants and herbs", "complement", "established", "main", "Delicate poultry and light-bodied Kalecik Karası; pine nuts and currants bridge the wine's strawberry note.")
    PAIR(prod5b, "Aged Tulum peyniri cheese with walnuts and grape molasses", "complement", "established", "cheese", "Turkish cave-aged cheese with Turkish red wine; grape molasses bridges the wine's fruity character.")

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
