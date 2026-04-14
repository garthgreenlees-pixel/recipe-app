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
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 76 ──────────────────────────────────────────────────────────────────
# Regions: Jurançon, Soave Classico, Ningxia, Nashik, Brda (Slovenia)

# ── Region 1: Jurançon ────────────────────────────────────────────────────────
print("\n=== Region 1: Jurançon ===")
r1 = R("Jurançon", "France", "wine",
    designation_type="AOC",
    designation_name="Jurançon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Pyrenean AOC in southwest France producing both dry (Sec) and sweet (moelleux) wines from Gros Manseng and Petit Manseng; known for wines of remarkable complexity, tropical fruit and racy acidity.",
    key_producers="Domaine Cauhapé, Clos Lapeyre, Clos Uroulat, Château Jolys, Domaine Bru-Baché",
    historical_context="Henri IV was born in the Jurançon region in 1553 and his lips were reportedly moistened with Jurançon at his baptism; the region's wines have royal and historic significance in French wine culture."
)
VIN(r1, 2022, "excellent", "rising", "Outstanding Pyrenean vintage; Petit Manseng of extraordinary aromatic intensity and balanced sweetness.")
VIN(r1, 2021, "very_good", "stable", "Good quality; moelleux of genuine complexity and the dry Sec particularly crisp and food-friendly.")
VIN(r1, 2020, "good", "stable", "Consistent vintage; reliable wines at both dry and sweet levels.")
VIN(r1, 2019, "excellent", "rising", "Near-perfect Jurançon year; late-harvest Petit Manseng of exceptional concentration.")
VIN(r1, 2018, "very_good", "stable", "Balanced growing season; wines show the variety's characteristic tropical-acid tension.")

p1a = P("Domaine Cauhapé", "winery", r1, "France",
    production_philosophy="terroir_expression",
    philosophy_description="Henri Ramonteu's pioneering Jurançon estate that raised the appellation's quality ceiling and international profile; Symphonie de Novembre is the reference moelleux wine.",
    reputation_narrative="Cauhapé is universally considered Jurançon's greatest estate; Symphonie de Novembre and the dry Ballet d'Octobre are the appellation's most internationally admired wines.",
    price_positioning="premium")
prod1a, new1a = PROD("Cauhapé Noblesse du Petit Manseng Sec", "wine_still", p1a, r1, "France",
    subcategory="Petit Manseng",
    description="Dry Jurançon Petit Manseng of extraordinary complexity — white pineapple, grapefruit, lemon curd, ginger and a distinctive resinous-mineral finish with razor-sharp acidity.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Foie gras escalope with green apple and calvados", "complement", "established", "starter", "Dry Manseng's acidity cuts foie gras fat; apple and calvados bridge the wine's tropical-acid tension.")
    PAIR(prod1a, "Grilled lobster with béarnaise and lemon", "complement", "classic", "main", "Rich crustacean and Pyrenean dry white; béarnaise tarragon bridges the wine's tropical complexity.")
    PAIR(prod1a, "Chicken liver parfait with pickled grapes", "complement", "established", "starter", "Rich offal and racy Manseng; pickled grapes bridge the wine's acidity and the parfait's iron.")
    PAIR(prod1a, "Ossau-Iraty cheese with cherry jam", "complement", "classic", "cheese", "The Pyrenean ewes' milk cheese with the Pyrenean white wine — cherry jam bridges the wine's fruit.")

p1b = P("Clos Uroulat", "winery", r1, "France",
    production_philosophy="minimal_intervention",
    philosophy_description="Charles Hours' artisan Jurançon estate producing one of France's most singular dessert wines from Petit Manseng; the Clos Uroulat moelleux is celebrated for its combination of sweetness and precision.",
    reputation_narrative="Clos Uroulat's moelleux is considered one of France's finest dessert wines, prized for its combination of tropical richness and lightning acidity.",
    price_positioning="premium")
prod1b, new1b = PROD("Clos Uroulat Moelleux Jurançon", "wine_dessert", p1b, r1, "France",
    subcategory="Petit Manseng moelleux",
    description="Jurançon's most individual sweet wine: Petit Manseng picked late with natural concentration — apricot jam, fresh pineapple, clementine zest, ginger and extraordinary acid-sweet balance.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Foie gras mi-cuit with gingerbread toast and quince paste", "complement", "classic", "starter", "Southwest France's greatest pairing: Jurançon moelleux and foie gras from the same region.")
    PAIR(prod1b, "Munster with caraway and baguette", "contrast", "established", "cheese", "Pungent washed-rind and sweet Manseng; a bold contrast pairing where each amplifies the other.")
    PAIR(prod1b, "Tropical fruit tart with passion fruit curd", "complement", "established", "dessert", "Tropical wine with tropical tart — pineapple, passionfruit and citrus in perfect alignment.")
    PAIR(prod1b, "Époisses de Bourgogne on sourdough", "contrast", "adventurous", "cheese", "The most pungent French cheese and the sweetest Pyrenean white in provocative harmony.")

# ── Region 2: Soave Classico ──────────────────────────────────────────────────
print("\n=== Region 2: Soave Classico ===")
r2 = R("Soave Classico", "Italy", "wine",
    designation_type="DOC",
    designation_name="Soave Classico DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The historic hillside core of Soave DOC in the Veneto, producing Italy's finest Garganega whites from volcanic basalt and limestone soils; long dismissed as neutral, serious Classico is now recognised as one of Italy's most age-worthy white wines.",
    key_producers="Pieropan, Gini, Prà, Inama, Coffele",
    historical_context="Soave's reputation collapsed in the 1970s–80s due to mass production on the plains; the Classico zone on the original medieval hills was preserved by a handful of quality estates who proved Garganega's true potential."
)
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage; volcanic Garganega of extraordinary mineral precision and aromatic purity.")
VIN(r2, 2021, "very_good", "stable", "Good quality; wines show the Classico zone's characteristic mineral drive and almond finish.")
VIN(r2, 2020, "good", "stable", "Reliable vintage; expressive, food-friendly whites at accessible prices.")
VIN(r2, 2019, "excellent", "rising", "Benchmark Soave Classico year; Pieropan Calvarino and Gini La Froscà both exceptional.")
VIN(r2, 2018, "very_good", "stable", "Good season; Garganega shows its characteristic bitter almond and mineral character.")

p2a = P("Pieropan", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Leonildo Pieropan's historic estate that single-handedly saved Soave Classico's reputation; Calvarino and La Rocca single vineyards are the benchmarks against which all Soave Classico is measured.",
    reputation_narrative="Pieropan is Soave's reference producer; Calvarino is considered Italy's greatest Garganega wine and a global benchmark for the variety's potential.",
    price_positioning="premium")
prod2a, new2a = PROD("Pieropan Calvarino Soave Classico", "wine_still", p2a, r2, "Italy",
    subcategory="Garganega",
    description="Italy's greatest Soave from Calvarino's volcanic basalt — lemon verbena, white peach, almond, volcanic mineral and a persistent bitter finish; deceptively ageworthy over a decade.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Baccalà alla vicentina (slow-cooked salt cod in milk and onion)", "complement", "classic", "main", "The Veneto's most beloved salt cod preparation with Veneto's finest white — a perfect regional marriage.")
    PAIR(prod2a, "Risotto all'Amarone with bone marrow and Parmigiano", "bridge", "established", "main", "Contrast pairing: mineral Garganega preceding the Veneto's most powerful red.")
    PAIR(prod2a, "Grilled Adriatic sole with lemon, capers and butter", "complement", "classic", "fish_course", "Delicate flatfish and mineral Soave; capers echo the wine's bitter mineral note.")
    PAIR(prod2a, "Monte Veronese cheese with Soave wine grape jelly", "complement", "classic", "cheese", "Veronese cheese with Veronese wine — grape jelly bridges the wine's almond and stone fruit character.")

p2b = P("Gini", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Multi-generational estate farming pre-phylloxera Garganega vines up to 70 years old on volcanic Soave Classico hillsides; La Froscà is considered among the greatest single-vineyard Soave Classico wines.",
    reputation_narrative="Gini's old-vine Garganega wines are consistently among Italy's most acclaimed whites at their price point; La Froscà demonstrates the variety's capacity for texture and complexity.",
    price_positioning="premium")
prod2b, new2b = PROD("Gini La Froscà Soave Classico", "wine_still", p2b, r2, "Italy",
    subcategory="Garganega",
    description="Old-vine volcanic Soave Classico of remarkable texture — ripe apple, white peach, almond paste, volcanic mineral and a long, satisfying bitter-mineral finish from elderly bush vines.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Pasta e fagioli con pancetta (pasta and bean soup with pancetta)", "complement", "classic", "main", "Classic Veneto peasant dish with old-vine mineral white; almond in the wine bridges the bean's earthiness.")
    PAIR(prod2b, "Grilled squid (calamari grigliati) with lemon oil", "complement", "established", "starter", "Adriatic cephalopod and volcanic mineral Garganega — lemon oil bridges the wine's bitter almond.")
    PAIR(prod2b, "Tagliatelle con tartufo nero (black truffle pasta)", "bridge", "established", "main", "Old-vine Soave's texture handles the truffle's earthiness; almond in both wine and truffle align perfectly.")
    PAIR(prod2b, "Asiago stravecchio with Acacia honey", "complement", "established", "cheese", "Aged Veneto cheese and Veneto white wine; honey bridges the wine's stone fruit and the cheese's intensity.")

# ── Region 3: Ningxia ─────────────────────────────────────────────────────────
print("\n=== Region 3: Ningxia ===")
r3 = R("Ningxia", "China", "wine",
    designation_type="GI",
    designation_name="Ningxia GI",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="China's premier fine wine region at 1,100–1,200m on the eastern slopes of the Helan Mountains in north-central China, producing increasingly acclaimed Cabernet Sauvignon, Merlot and Marselan with strong diurnal variation.",
    key_producers="Helan Qingxue, Silver Heights, Château Changyu Moser XV, Domaine des Arômes, Pernod Ricard China",
    historical_context="Ningxia has transformed Chinese wine from international joke to serious contender; Helan Qingxue's Jia Bei Lan scored 95 points from Decanter in 2011, triggering global interest in Chinese fine wine."
)
VIN(r3, 2022, "very_good", "rising", "Good growing season; Cabernet Sauvignon and Marselan show improved balance from cooler autumn.")
VIN(r3, 2021, "excellent", "rising", "Outstanding Ningxia year; wines of remarkable concentration and freshness from ideal diurnal swings.")
VIN(r3, 2020, "good", "stable", "Consistent quality; solid reds with good fruit concentration and approachable tannins.")
VIN(r3, 2019, "very_good", "rising", "Strong vintage; increasingly refined Cabernet blends demonstrating Ningxia's improving winemaking.")
VIN(r3, 2018, "good", "stable", "Reliable year; wines show the characteristic dark fruit and herbal notes of Helan Mountain terroir.")

p3a = P("Helan Qingxue Vineyard", "winery", r3, "China",
    production_philosophy="terroir_expression",
    philosophy_description="The estate that put Ningxia on the world wine map; Zhang Jing's Jia Bei Lan (Cabernet Sauvignon blend) is China's most internationally acclaimed wine.",
    reputation_narrative="Helan Qingxue Jia Bei Lan scored 95 points from Decanter and won multiple international gold medals; the estate is synonymous with Chinese fine wine's emergence.",
    price_positioning="premium")
prod3a, new3a = PROD("Helan Qingxue Jia Bei Lan", "wine_still", p3a, r3, "China",
    subcategory="Cabernet Sauvignon blend",
    description="China's most acclaimed red wine: Cabernet Sauvignon with Merlot and Cabernet Franc from Helan Mountain slopes — blackcurrant, cedar, bay leaf, dark spice and firm tannins.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Braised red-cooked pork belly (hongshao rou)", "complement", "adventurous", "main", "Classic Chinese-Western bridge pairing: red-cooked pork's soy-star anise depth mirrors the wine's spiced dark fruit.")
    PAIR(prod3a, "Lamb skewers (mutton chuanr) with cumin and chilli", "complement", "established", "casual", "Northwestern Chinese lamb preparation is a natural match for Ningxia's most celebrated red.")
    PAIR(prod3a, "Peking duck with hoisin, scallion and cucumber", "bridge", "established", "main", "Chinese-Western crossover: duck's richness and Ningxia Cabernet are designed to meet at the table.")
    PAIR(prod3a, "Aged Manchego with quince", "complement", "established", "cheese", "International reference pairing for Cabernet; Ningxia wine is ready for Western cheese board service.")

p3b = P("Silver Heights", "winery", r3, "China",
    production_philosophy="terroir_expression",
    philosophy_description="Emma Gao's family estate — a Ningxia pioneer — producing Emma's Reserve Cabernet from high-altitude Helan Mountain vineyards with a European-trained winemaking approach.",
    reputation_narrative="Silver Heights Emma's Reserve is one of China's most critically acclaimed wines; Emma Gao is China's most celebrated winemaker and a figure of global wine significance.",
    price_positioning="premium")
prod3b, new3b = PROD("Silver Heights Emma's Reserve", "wine_still", p3b, r3, "China",
    subcategory="Cabernet Sauvignon",
    description="Ningxia Cabernet of genuine elegance: dark plum, cassis, tobacco, cedar and well-integrated mountain tannins; produced at one of China's most artisan estates.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Slow-roasted lamb shoulder with Mongolian spices", "complement", "established", "main", "High-altitude Ningxia Cabernet and Inner Mongolian lamb tradition meet in a shared northern China terroir.")
    PAIR(prod3b, "Beef and mushroom dumplings (jiaozi) pan-fried", "complement", "suggested", "casual", "Substantial dumplings and medium-bodied Cabernet; mushroom bridges the wine's earthy depth.")
    PAIR(prod3b, "Dark chocolate and five-spice truffles", "complement", "suggested", "digestif", "Five-spice's star anise, cinnamon and pepper bridge Chinese wine with familiar Western chocolate.")
    PAIR(prod3b, "Grilled beef tenderloin with black pepper sauce", "complement", "classic", "main", "Western-style preparation for increasingly Western-style wine; black pepper amplifies Cabernet's structure.")

# ── Region 4: Nashik ──────────────────────────────────────────────────────────
print("\n=== Region 4: Nashik ===")
r4 = R("Nashik", "India", "wine",
    designation_type="GI",
    designation_name="Nashik GI",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Maharashtra's Sahyadri Valley wine hub at 550–750m, producing 80% of India's fine wine from Chenin Blanc, Sauvignon Blanc, Viognier, Cabernet Sauvignon and Shiraz; India's answer to Napa Valley.",
    key_producers="Sula Vineyards, York Winery, Fratelli Wines, KRSMA Estates, Grover Zampa",
    historical_context="Indian wine production began seriously only in the 1990s; Sula Vineyards launched the Indian wine revolution from Nashik in 1999, and the region now hosts over 50 wineries producing increasingly sophisticated wines."
)
VIN(r4, 2023, "very_good", "rising", "Good harvest at altitude; Chenin Blanc shows tropical freshness and Cabernet Sauvignon good structure.")
VIN(r4, 2022, "good", "stable", "Consistent quality; India's viticulture is improving rapidly with investment in technology.")
VIN(r4, 2021, "very_good", "rising", "Excellent year; Nashik wines are demonstrating genuine terroir character for the first time.")
VIN(r4, 2020, "good", "stable", "Solid vintage; accessible, fruit-forward wines with Indian food versatility.")
VIN(r4, 2019, "good", "rising", "Good harvest; Sauvignon Blanc and Riesling both showed promising freshness and acidity.")

p4a = P("Sula Vineyards", "winery", r4, "India",
    production_philosophy="traditional",
    philosophy_description="India's largest and most internationally recognised wine producer, founded by Rajeev Samant in 1999; Sula launched India's wine revolution from Nashik and remains the category leader.",
    reputation_narrative="Sula Vineyards is India's wine ambassador; Sula Brut sparkling and Chenin Blanc are the most widely distributed Indian wines internationally.",
    price_positioning="value")
prod4a, new4a = PROD("Sula Vineyards The Source Sauvignon Blanc", "wine_still", p4a, r4, "India",
    subcategory="Sauvignon Blanc",
    description="India's most characterful Sauvignon Blanc from Nashik's Dindori vineyard — tropical fruit, passion fruit, green herb and a fresh, vibrant finish; India's most internationally recognised white wine.",
    price_tier="value")
if new4a:
    PAIR(prod4a, "Tandoori fish tikka with mint chutney and lime", "complement", "established", "main", "Indian spiced fish and Indian Sauvignon Blanc — a natural pairing from the same terroir and culture.")
    PAIR(prod4a, "Prawn and mango salad with chilli-lime dressing", "complement", "classic", "starter", "Tropical Sauvignon Blanc and tropical ingredients in the dressing and mango; vivid and refreshing.")
    PAIR(prod4a, "Paneer tikka with green chutney and onion", "complement", "established", "starter", "India's most popular appetiser with India's most versatile white wine.")
    PAIR(prod4a, "Steamed fish momos with ginger-soy dipping sauce", "complement", "suggested", "starter", "South Asian dumplings and crisp Sauvignon; ginger bridges the wine's herbal freshness.")

p4b = P("Fratelli Wines", "winery", r4, "India",
    production_philosophy="terroir_expression",
    philosophy_description="Italian-Indian joint venture producing some of India's most refined and internationally competitive wines; the Sette Cabernet blend demonstrates Nashik's potential for serious reds.",
    reputation_narrative="Fratelli's Sette is consistently awarded India's most critical recognition; the estate represents the crossover of Italian winemaking expertise with Indian terroir.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Fratelli Sette", "wine_still", p4b, r4, "India",
    subcategory="Cabernet Sauvignon blend",
    description="India's most internationally acclaimed Cabernet blend: Cabernet Sauvignon with Sangiovese — dark cherry, plum, cedar, herb and medium-plus tannins; India's answer to a serious Tuscan-influenced red.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Rogan josh (Kashmiri spiced lamb curry)", "bridge", "adventurous", "main", "Spiced red meat curry with red wine is a cross-cultural adventure; the wine's structure handles the spice.")
    PAIR(prod4b, "Mutton seekh kebab with pomegranate raita", "complement", "established", "main", "Spiced ground lamb on skewer and Nashik red; pomegranate bridges the wine's dark fruit character.")
    PAIR(prod4b, "Wood-fired margherita pizza", "complement", "established", "casual", "Italian-influenced wine with Italian dish — mozzarella and tomato align with the Sangiovese component.")
    PAIR(prod4b, "Grilled lamb chops with rosemary and garlic", "complement", "classic", "main", "Western preparation meets Indian-Italian wine; herbs mirror the wine's cedar and aromatic complexity.")

# ── Region 5: Brda ────────────────────────────────────────────────────────────
print("\n=== Region 5: Brda ===")
r5 = R("Brda", "Slovenia", "wine",
    designation_type="PDO",
    designation_name="Goriška Brda PDO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Slovenia's westernmost wine region bordering Italy's Collio, producing distinctive Rebula (Ribolla Gialla), Pinot Gris and skin-contact whites; the 'Tuscany of Slovenia' with Mediterranean climate and marl-clay ponca soils.",
    key_producers="Movia, Ščurek, Kabaj, Marjan Simčič, Klinec",
    historical_context="Brda shares its terroir and grape varieties with Italian Collio across an arbitrary political border drawn after WWII; Slovenian Brda and Italian Collio are in many ways the same wine region producing the same wines from the same soils."
)
VIN(r5, 2022, "excellent", "rising", "Outstanding Brda vintage; Rebula and skin-contact whites of exceptional mineral precision.")
VIN(r5, 2021, "very_good", "stable", "Good quality; wines express the ponca soil's characteristic mineral character.")
VIN(r5, 2020, "good", "stable", "Consistent vintage; expressive whites with good food-friendly acidity.")
VIN(r5, 2019, "excellent", "rising", "Benchmark Brda year; wines of great depth across all styles including amber wines.")
VIN(r5, 2018, "very_good", "stable", "Good season; Rebula and Pinot Gris both showed excellent balance and mineral drive.")

p5a = P("Movia", "winery", r5, "Slovenia",
    production_philosophy="biodynamic",
    philosophy_description="Aleš Kristančič's legendary biodynamic estate — one of the most original wine producers in the world — making no-sulphur Rebula, Merlot and the extraordinary Puro (disgorgement in the glass) sparkling wine.",
    reputation_narrative="Movia is Slovenia's most internationally celebrated wine estate; the estate's philosophy of natural intervention and Aleš's theatrical flair have made it a cult among sommeliers worldwide.",
    price_positioning="premium")
prod5a, new5a = PROD("Movia Lunar Rebula", "wine_still", p5a, r5, "Slovenia",
    subcategory="Rebula",
    description="Movia's skin-contact Rebula aged in old oak without sulphur: amber, complex, tannic — dried apricot, chamomile, orange peel and a long oxidative-mineral finish; unique and polarising.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Aged Tolminc cheese with wild honey and walnuts", "complement", "established", "cheese", "Slovenian mountain cheese with Slovenian amber wine; walnut bridges the wine's oxidative-nutty character.")
    PAIR(prod5a, "Slow-roasted pork neck with sauerkraut and caraway", "complement", "established", "main", "Skin-contact tannin handles pork fat; caraway and sauerkraut's acidity bridge the wine's oxidative depth.")
    PAIR(prod5a, "Cured prosciutto (kraški pršut) with figs and melon", "complement", "classic", "starter", "Karst prosciutto with Brda amber wine is the quintessential Slovenian-Italian border pairing.")
    PAIR(prod5a, "Chargrilled octopus with roasted peppers and sea salt", "complement", "adventurous", "main", "Tannin from skin contact can handle octopus; the wine's oxidative character bridges salt and smoke.")

p5b = P("Marjan Simčič", "winery", r5, "Slovenia",
    production_philosophy="terroir_expression",
    philosophy_description="Ceglo-based estate producing some of Brda's most refined and internationally competitive wines including the benchmark Opoka Rebula and elegant Pinot Gris.",
    reputation_narrative="Marjan Simčič is one of Slovenia's most acclaimed producers; Opoka Rebula is considered the reference wine for Slovenia's most important indigenous white variety.",
    price_positioning="premium")
prod5b, new5b = PROD("Marjan Simčič Opoka Rebula", "wine_still", p5b, r5, "Slovenia",
    subcategory="Rebula",
    description="Slovenia's benchmark Rebula from opoka (marl-limestone) soil: white peach, almond, lemon, stone mineral and fresh herbal notes; structured, precise and food-friendly.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Fresh white truffle shaved over egg tagliatelle", "complement", "classic", "main", "Cross-border pairing: Brda Rebula with Collio's (shared) truffle tradition; almond and truffle amplify each other.")
    PAIR(prod5b, "Adriatic branzino baked with fennel and lemon", "complement", "classic", "main", "Mediterranean fish from the shared coast; fennel echoes the wine's aromatic herbal note.")
    PAIR(prod5b, "Idrija žlikrofi (Slovenian filled pasta with herb potato)", "complement", "classic", "main", "Slovenia's famous PDO pasta with its finest white wine is the definitive national pairing.")
    PAIR(prod5b, "Brie de Meaux with apricot jam", "complement", "established", "cheese", "Soft creamy cheese aligns with the wine's texture; apricot jam bridges the wine's stone fruit and almond.")

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
