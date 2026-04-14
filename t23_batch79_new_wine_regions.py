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

# ── Batch 79 ──────────────────────────────────────────────────────────────────
# Regions: Finger Lakes, Morellino di Scansano, Valpolicella Classico, Galilee, Areni

# ── Region 1: Finger Lakes ────────────────────────────────────────────────────
print("\n=== Region 1: Finger Lakes ===")
r1 = R("Finger Lakes", "USA", "wine",
    designation_type="AVA",
    designation_name="Finger Lakes AVA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="New York State's premier wine region centred on eleven glacier-carved lakes, producing Germany-rivalling dry Riesling, elegant Pinot Noir and world-class Cabernet Franc from lakeside sites moderated by water temperature retention.",
    key_producers="Hermann J. Wiemer, Dr. Konstantin Frank, Ravines Wine Cellars, Red Newt Cellars, Anthony Road Wine Company",
    historical_context="The Finger Lakes wine tradition began with German and Swiss immigrants in the 19th century; Dr. Konstantin Frank proved in 1962 that vinifera could survive Finger Lakes winters, launching the modern era of serious American Riesling production."
)
VIN(r1, 2022, "excellent", "rising", "Outstanding Finger Lakes vintage; Riesling of extraordinary mineral precision and Pinot Noir of Burgundian delicacy.")
VIN(r1, 2021, "very_good", "stable", "Good quality; wines show the lakes' temperature-moderating influence and excellent acid retention.")
VIN(r1, 2020, "good", "stable", "Consistent vintage; reliable, food-friendly wines across all varieties.")
VIN(r1, 2019, "excellent", "rising", "Benchmark year; Hermann J. Wiemer Magdalena Vineyard and Dr. Frank Reserve both exceptional.")
VIN(r1, 2018, "very_good", "stable", "Good season; Riesling showed the variety's remarkable consistency in the lake-moderated climate.")

p1a = P("Hermann J. Wiemer Vineyard", "winery", r1, "USA",
    production_philosophy="terroir_expression",
    philosophy_description="The estate that transformed the Finger Lakes from a curiosity to a global Riesling destination; Hermann Wiemer's German-trained precision and Fred Merwarth's continuation have produced New York State's finest whites.",
    reputation_narrative="Hermann J. Wiemer Vineyard is universally recognised as the Finger Lakes' greatest estate; the Magdalena Vineyard Riesling is the most critically acclaimed Riesling in the eastern USA.",
    price_positioning="premium")
prod1a, new1a = PROD("Hermann J. Wiemer Magdalena Vineyard Riesling", "wine_still", p1a, r1, "USA",
    subcategory="Riesling",
    description="America's finest Riesling from a lakeside single vineyard: lime zest, white peach, slate, wildflower and the distinctive Seneca Lake mineral tension; dry, complex and can age 15+ years.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Pan-seared lake trout with brown butter and lemon", "complement", "classic", "fish_course", "Seneca Lake fish with Seneca Lake Riesling is the ultimate Finger Lakes terroir pairing.")
    PAIR(prod1a, "Riesling-braised mussels with garlic and parsley", "complement", "classic", "starter", "The wine goes into the broth and onto the table; garlic and parsley bridge the wine's mineral character.")
    PAIR(prod1a, "Sushi: halibut, fluke and uni nigiri", "complement", "adventurous", "fish_course", "The wine's mineral precision and clean acidity make it exceptional with delicate white-fish sushi.")
    PAIR(prod1a, "Upstate NY apple and sharp cheddar galette", "complement", "established", "casual", "Apple in both wine and dish; the region's great cheddar with its great Riesling is a local tradition.")

p1b = P("Ravines Wine Cellars", "winery", r1, "USA",
    production_philosophy="terroir_expression",
    philosophy_description="Morten Hallgren's acclaimed Keuka Lake estate producing some of the Finger Lakes' most precise and terroir-driven Riesling and Cabernet Franc from single-vineyard sites.",
    reputation_narrative="Ravines Argetsinger Vineyard Riesling and Argetsinger Cabernet Franc are consistently ranked among New York State's finest wines; the estate defines Keuka Lake's distinctive character.",
    price_positioning="premium")
prod1b, new1b = PROD("Ravines Argetsinger Vineyard Riesling", "wine_still", p1b, r1, "USA",
    subcategory="Riesling",
    description="Keuka Lake Riesling of fine mineral character: lemon, green apple, grapefruit, chalk and a slightly fuller texture than Seneca Lake expressions; dry, precise and ageworthy.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Vietnamese pho with beef, basil and lime", "complement", "adventurous", "main", "Riesling's aromatic tension and acidity manage complex broth spice; lime bridges the wine's citrus character.")
    PAIR(prod1b, "Smoked whitefish dip with rye crackers and pickled onion", "complement", "established", "starter", "Finger Lakes smoked fish tradition with the region's finest white wine; pickled onion mirrors acidity.")
    PAIR(prod1b, "Indian paneer tikka with green chutney", "complement", "classic", "starter", "Dry Riesling's structure and acidity manage mild spice beautifully; chutney echoes the wine's herb edge.")
    PAIR(prod1b, "Aged New York State sheep's milk cheese with walnut bread", "complement", "established", "cheese", "Artisan upstate cheese and the region's finest Riesling — a New York terroir pairing.")

# ── Region 2: Morellino di Scansano ───────────────────────────────────────────
print("\n=== Region 2: Morellino di Scansano ===")
r2 = R("Morellino di Scansano", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Morellino di Scansano DOCG",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Tuscan Maremma DOCG producing wines from Sangiovese (locally called Morellino) grown near the Tyrrhenian coast; warmer than Chianti, the wines show riper fruit, earthy Mediterranean character and good value.",
    key_producers="Moris Farms, Fattoria Le Pupille, Rocca di Frassinello, Erik Banti, Poggio Argentiera",
    historical_context="Morellino di Scansano is Sangiovese's coastal expression in the Maremma — once malarial marshland drained in the 20th century; the wines offer a more generous, sun-baked profile than their Chianti cousins."
)
VIN(r2, 2021, "excellent", "rising", "Outstanding coastal vintage; Morellino shows excellent ripeness, Mediterranean herb and balanced structure.")
VIN(r2, 2020, "very_good", "stable", "Good quality; wines show the warmth of coastal Tuscany with good food-friendly acidity.")
VIN(r2, 2019, "good", "stable", "Consistent vintage; reliable, expressive Morellino at excellent value for Sangiovese lovers.")
VIN(r2, 2018, "excellent", "rising", "Benchmark year; Le Pupille Poggio Valente and Moris Farms Avvoltore both exceptional.")
VIN(r2, 2017, "very_good", "stable", "Good season; wines show characteristic Maremma warmth and ripe Mediterranean fruit.")

p2a = P("Fattoria Le Pupille", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="The Maremma's most internationally acclaimed estate, producing the legendary Saffredi (Cabernet-Merlot) alongside the benchmark Poggio Valente Morellino from coastal Scansano.",
    reputation_narrative="Fattoria Le Pupille Saffredi is one of Italy's greatest Super Tuscan wines; Poggio Valente is the reference wine for top-level Morellino di Scansano.",
    price_positioning="premium")
prod2a, new2a = PROD("Le Pupille Poggio Valente Morellino di Scansano", "wine_still", p2a, r2, "Italy",
    subcategory="Sangiovese",
    description="Benchmark coastal Morellino from single vineyard: dark cherry, Mediterranean herbs, leather, earthy spice and good structure; warmer and richer than Chianti with excellent Maremma character.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Wild boar pappardelle with tomato, olives and rosemary", "complement", "classic", "main", "Coastal Tuscan Sangiovese with the region's traditional wild boar ragù is the Maremma's most authentic pairing.")
    PAIR(prod2a, "Grilled Florentine-style T-bone steak (bistecca di vitella)", "complement", "established", "main", "Tuscan beef with Tuscan Sangiovese; coastal warmth makes Morellino an excellent steak companion.")
    PAIR(prod2a, "Pecorino Toscano semi-stagionato with chestnut honey", "complement", "classic", "cheese", "Tuscan ewes' milk cheese and Tuscan Sangiovese; chestnut honey bridges the wine's dark fruit.")
    PAIR(prod2a, "Panzanella (Tuscan bread and tomato salad) with anchovy", "complement", "established", "starter", "The wine's acidity and dark cherry complement panzanella's fresh tomato and bread; anchovy adds umami depth.")

p2b = P("Moris Farms", "winery", r2, "Italy",
    production_philosophy="traditional",
    philosophy_description="The historic Maremma estate producing both Morellino and the Super Tuscan Avvoltore from coastal Scansano vineyards; one of the region's oldest family wine producers.",
    reputation_narrative="Moris Farms Avvoltore is one of Italy's most celebrated Super Tuscans; the estate's Morellino Riserva is the most reliable benchmark for traditional-style coastal Sangiovese.",
    price_positioning="mid_range")
prod2b, new2b = PROD("Moris Farms Morellino di Scansano Riserva", "wine_still", p2b, r2, "Italy",
    subcategory="Sangiovese",
    description="Traditional Maremma Morellino Riserva: cherry, leather, Mediterranean herb, tobacco and earthy warmth; medium-bodied with good structure and an authentic coastal Sangiovese identity.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Acquacotta (Maremma vegetable and bread soup)", "complement", "classic", "main", "The Maremma's traditional peasant soup with the region's accessible red wine is pure Italian comfort.")
    PAIR(prod2b, "Grilled lamb with rosemary, garlic and Maremma sea salt", "complement", "established", "main", "Coastal lamb with coastal Sangiovese; the wine's herb notes mirror the rosemary and salt crust.")
    PAIR(prod2b, "Pasta e fagioli with guanciale and sage", "complement", "established", "main", "Classic Italian one-pot dish with medium-bodied Morellino; guanciale fat and sage align with the wine's weight.")
    PAIR(prod2b, "Cacciotta Toscana fresh cheese with roasted cherry tomatoes", "complement", "suggested", "cheese", "Mild Tuscan cheese with the region's accessible red; roasted tomato acidity bridges both.")

# ── Region 3: Valpolicella Classico ───────────────────────────────────────────
print("\n=== Region 3: Valpolicella Classico ===")
r3 = R("Valpolicella Classico", "Italy", "wine",
    designation_type="DOC",
    designation_name="Valpolicella Classico DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The historic hillside core of Valpolicella, producing the full range of Corvina-based wines: fresh Valpolicella Classico, ripasso, Amarone and Recioto from the villages of Fumane, Marano and Negrar.",
    key_producers="Allegrini, Bertani, Dal Forno Romano, Quintarelli, Tedeschi",
    historical_context="Valpolicella Classico is the heartland of the world's most unusual wine family: from the fresh, light Classico to the formidable Amarone and sweet Recioto, all sharing the Corvina grape and the Veneto's dramatic hillside terroir."
)
VIN(r3, 2020, "excellent", "rising", "Outstanding vintage for all Valpolicella styles; Amarone producers received ideal appassimento conditions.")
VIN(r3, 2019, "very_good", "stable", "Good quality across styles; Classico shows freshness and Ripasso good depth.")
VIN(r3, 2018, "exceptional", "rising", "Benchmark vintage; Amarone of the highest order and fresh Classico of unusual complexity.")
VIN(r3, 2017, "very_good", "stable", "Consistent quality; warm season favouring ripe, generous Classico and Ripasso.")
VIN(r3, 2016, "excellent", "rising", "Excellent vintage widely considered among Valpolicella's finest of the decade.")

p3a = P("Allegrini", "winery", r3, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="The Veneto's most celebrated estate for both traditional Amarone and innovative Super Veronese La Poja (pure Corvina) from historic Fumane hillside vineyards.",
    reputation_narrative="Allegrini Amarone della Valpolicella Classico is one of Italy's most consistent benchmark reds; the estate defines quality in the Classico zone across all production levels.",
    price_positioning="premium")
prod3a, new3a = PROD("Allegrini Palazzo della Torre", "wine_still", p3a, r3, "Italy",
    subcategory="Corvina blend ripasso-style",
    description="Allegrini's bridge between fresh Valpolicella and Amarone: Corvina, Rondinella and Sangiovese ripasso-style — ripe cherry, plum, dried herbs, chocolate and velvety texture at an accessible price.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Beef ragu with wide pappardelle and Parmigiano", "complement", "classic", "main", "The Veneto's most loved pasta format with its most loved red wine style — a deeply satisfying Italian pairing.")
    PAIR(prod3a, "Osso buco milanese with gremolata and risotto giallo", "complement", "classic", "main", "Rich veal shank and structured Veneto red; gremolata lemon bridges the wine's acidity.")
    PAIR(prod3a, "Polenta pasticciata con funghi e formaggio (baked polenta with mushroom and cheese)", "complement", "established", "main", "Earthy mushroom and polenta richness align with the wine's texture and dark fruit character.")
    PAIR(prod3a, "Monte Veronese cheese with walnut honey", "complement", "established", "cheese", "Veronese cheese and Veronese wine; walnut honey bridges the wine's dried herb and dark fruit.")

p3b = P("Brigaldara", "winery", r3, "Italy",
    production_philosophy="traditional",
    philosophy_description="Negrar-based estate producing authentic, traditional Valpolicella Classico, Amarone and Recioto with minimal intervention and respect for the zone's historical winemaking approach.",
    reputation_narrative="Brigaldara is celebrated for producing some of Valpolicella's most authentic and honest expressions; the Amarone from 2011 onwards has earned exceptional critical recognition.",
    price_positioning="premium")
prod3b, new3b = PROD("Brigaldara Valpolicella Classico Superiore", "wine_still", p3b, r3, "Italy",
    subcategory="Corvina blend",
    description="Traditional Valpolicella Classico Superiore of genuine character: cherry, bitter almond, dried violet, fresh herbs and a distinctly Veronese bitter finish — medium-bodied and highly food-versatile.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Spaghetti al pomodoro fresco e basilico (fresh tomato and basil pasta)", "complement", "classic", "main", "The wine's cherry and herbs mirror the fresh tomato sauce; this is Italy's most classic simple pasta pairing.")
    PAIR(prod3b, "Bollito misto with salsa verde and mostarda", "complement", "classic", "main", "Northern Italian boiled meat with condiments; the wine's medium body and acidity are ideal for the format.")
    PAIR(prod3b, "Grilled salsiccia and braised radicchio", "complement", "established", "casual", "Veneto pork sausage and bitter radicchio mirror the wine's cherry and bitter almond notes.")
    PAIR(prod3b, "Fresh ricotta with honey and pistachios", "complement", "suggested", "cheese", "Gentle fresh dairy and light Valpolicella; honey bridges the wine's fruit, pistachio adds texture.")

# ── Region 4: Galilee ─────────────────────────────────────────────────────────
print("\n=== Region 4: Galilee ===")
r4 = R("Galilee", "Israel", "wine",
    designation_type="GI",
    designation_name="Galil GI",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Israel's premier wine region in the northern highlands at 600–900m, producing elegant Cabernet Sauvignon, Syrah and Sauvignon Blanc; the cool elevation and Mediterranean influence give wines freshness rare in the Middle East.",
    key_producers="Galil Mountain Winery, Dalton Winery, Yarden (Golan Heights), Chateau Golan, Pelter Winery",
    historical_context="Galilee is home to Israel's most internationally celebrated wines; the Golan Heights subregion, established after 1967, has transformed Israeli fine wine with high-altitude plantings and rigorous quality standards."
)
VIN(r4, 2022, "excellent", "rising", "Outstanding Galilee vintage; Cabernet and Syrah of remarkable freshness from elevated sites.")
VIN(r4, 2021, "very_good", "stable", "Good quality; wines show the region's characteristic Mediterranean-mountain balance.")
VIN(r4, 2020, "excellent", "rising", "Benchmark year; Yarden Katzrin and Dalton Matatia both scored exceptional ratings.")
VIN(r4, 2019, "good", "stable", "Consistent vintage; reliable, expressive wines at good value.")
VIN(r4, 2018, "very_good", "stable", "Good growing season; Syrah and Cabernet both showed fine balance and food-friendliness.")

p4a = P("Dalton Winery", "winery", r4, "Israel",
    production_philosophy="terroir_expression",
    philosophy_description="Upper Galilee estate at 900m altitude producing some of Israel's most elegant and food-friendly wines; Dalton Matatia is Israel's most critically acclaimed Cabernet Sauvignon blend.",
    reputation_narrative="Dalton Matatia is consistently Israel's highest-scoring wine internationally; the estate demonstrates that Israel can produce wines of genuine complexity and restraint.",
    price_positioning="premium")
prod4a, new4a = PROD("Dalton Matatia", "wine_still", p4a, r4, "Israel",
    subcategory="Cabernet Sauvignon blend",
    description="Israel's most acclaimed Cabernet blend from Upper Galilee altitude: blackcurrant, cedar, graphite, Middle Eastern dried herb and firmly structured but elegant tannins — can age a decade.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Slow-roasted lamb shoulder with za'atar and lemon (shawarma style)", "complement", "classic", "main", "Middle Eastern spiced lamb with Israel's finest red wine is the region's most authentic pairing.")
    PAIR(prod4a, "Grilled beef kebab with tahini, sumac and flatbread", "complement", "established", "main", "Classic Levantine grilled meat and structured Galilee Cabernet; tahini and sumac bridge the wine's cedar.")
    PAIR(prod4a, "Braised short rib with pomegranate molasses glaze", "complement", "established", "main", "Rich slow-cooked beef and Israel's premium red; pomegranate's sweet-tart bridges the wine's dark fruit.")
    PAIR(prod4a, "Aged Emek cheese with fig preserves", "complement", "established", "cheese", "Israeli hard cheese and premium Galilee red; fig bridges the wine's cassis and the cheese's milk sweetness.")

p4b = P("Galil Mountain Winery", "winery", r4, "Israel",
    production_philosophy="terroir_expression",
    philosophy_description="Upper Galilee cooperative estate at the foot of Mount Meron, producing accessible and characterful wines from Israel's coolest and most elevated wine terroir.",
    reputation_narrative="Galil Mountain Yiron is Israel's most award-winning accessible premium Bordeaux blend; the estate produces the most internationally distributed quality Israeli red wine.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Galil Mountain Yiron", "wine_still", p4b, r4, "Israel",
    subcategory="Cabernet Sauvignon blend",
    description="Israel's most internationally distributed premium red: Cabernet Sauvignon, Merlot and Syrah from Upper Galilee — dark plum, Mediterranean herb, tobacco and well-structured tannins.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled lamb chops with herbs and olive oil (grill mechaye)", "complement", "established", "main", "Israeli-style grilled lamb and accessible Galilee Cabernet blend is a straightforward terroir pairing.")
    PAIR(prod4b, "Beef shakshuka with peppers and eggs in tomato sauce", "complement", "suggested", "main", "The Israeli egg dish made with beef; tomato's acidity bridges the wine's structure in a bold brunch pairing.")
    PAIR(prod4b, "Brisket braised with onion, carrot and red wine", "complement", "classic", "main", "Shabbat brisket and Israeli premium red is a cultural and culinary tradition of the region.")
    PAIR(prod4b, "Aged Edam-style Israeli cheese with walnut and date", "complement", "suggested", "cheese", "Israeli firm cheese and Galilee red; date's sweetness bridges the wine's dark fruit and walnut adds depth.")

# ── Region 5: Areni ───────────────────────────────────────────────────────────
print("\n=== Region 5: Areni ===")
r5 = R("Areni", "Armenia", "wine",
    designation_type="PDO",
    designation_name="Areni PDO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Armenia's premier wine region in the Vayots Dzor province, producing wines from the ancient Areni Noir variety at 1,200–1,500m altitude; the world's oldest winery (6,100 years, discovered 2011) was found in the Areni cave system.",
    key_producers="Zorah Wines, Voskevaz, Armenia Wine, Trinity Canyon Vineyards, Karas",
    historical_context="Armenia's Areni cave contained the world's oldest known winery, predating Egyptian and Minoan wine cultures; Areni Noir is believed to be one of the world's oldest cultivated grape varieties and is potentially an ancestor of varieties across the Caucasus and Anatolia."
)
VIN(r5, 2021, "excellent", "rising", "Outstanding Armenian vintage; Areni Noir of extraordinary freshness, mineral depth and Pinot-like elegance.")
VIN(r5, 2020, "very_good", "stable", "Good quality; wines show the high-altitude's characteristic freshness and the grape's ancient character.")
VIN(r5, 2019, "good", "stable", "Consistent vintage; reliable, expressive wines from one of the world's oldest wine regions.")
VIN(r5, 2018, "excellent", "rising", "Benchmark Areni year; Zorah Karasi confirmed Armenia's claim to world fine wine attention.")
VIN(r5, 2017, "very_good", "stable", "Good season; Areni Noir shows its characteristic dried cherry, herb and mineral precision.")

p5a = P("Zorah Wines", "winery", r5, "Armenia",
    production_philosophy="minimal_intervention",
    philosophy_description="Zorik Gharibian's Italian-Armenian estate that single-handedly brought Areni Noir to global attention; Karasi (meaning clay vessel) is fermented in ancient Armenian clay amphorae (karas) without sulphur.",
    reputation_narrative="Zorah Karasi is Armenia's most internationally acclaimed wine; it has earned scores from Wine Spectator and Decanter confirming Armenia's emergence as a serious fine wine country.",
    price_positioning="premium")
prod5a, new5a = PROD("Zorah Karasi Areni Noir", "wine_still", p5a, r5, "Armenia",
    subcategory="Areni Noir",
    description="Armenia's most celebrated wine: Areni Noir fermented in clay karas — dried cherry, pomegranate, dried herbs, iron, earth and a haunting mineral precision; extraordinarily light for its depth of character.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Lamb khorovats (Armenian charcoal-grilled lamb skewers)", "complement", "classic", "main", "Armenia's most beloved grilled preparation with Armenia's most celebrated wine; terroir and culture in harmony.")
    PAIR(prod5a, "Tolma (Armenian stuffed grape leaves with lamb and rice)", "complement", "classic", "main", "The grape vine's leaves stuffed with lamb, paired with wine from the same ancient vine — a 6,000-year tradition.")
    PAIR(prod5a, "Wild mushroom and walnut stew with herbs (vegetarian khorovats)", "complement", "established", "main", "Earthy mushroom and iron-mineral Areni Noir; walnut adds weight to this delicate but complex pairing.")
    PAIR(prod5a, "Aged Armenian Lori cheese with dried mulberry and walnut", "complement", "established", "cheese", "Armenian mountain cheese with Armenia's greatest wine; mulberry bridges the wine's dried cherry note.")

p5b = P("Trinity Canyon Vineyards", "winery", r5, "Armenia",
    production_philosophy="terroir_expression",
    philosophy_description="Vayots Dzor estate producing clean, internationally styled Areni Noir and Voskehat (white) that serve as accessible entry points into Armenian wine.",
    reputation_narrative="Trinity Canyon's wines are the most widely distributed internationally accessible Armenian wines; the estate has played a significant role in building global awareness of Armenian viticulture.",
    price_positioning="mid_range")
prod5b, new5b = PROD("Trinity Canyon Areni Noir", "wine_still", p5b, r5, "Armenia",
    subcategory="Areni Noir",
    description="Accessible Armenian Areni Noir from high-altitude Vayots Dzor: fresh cherry, pomegranate, dried herbs, light earth and refreshing Caucasian mountain acidity; approachable and food-friendly.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Lahmajun (Armenian flatbread with spiced lamb topping)", "complement", "classic", "casual", "Armenia's most beloved street food with its native red wine is a pure cultural pairing.")
    PAIR(prod5b, "Grilled chicken with Armenian herb marinade (tarragon, thyme, dill)", "complement", "established", "main", "Light-bodied Areni and herb-marinated poultry; the wine's herb notes mirror the marinade's complexity.")
    PAIR(prod5b, "Manti (Armenian lamb dumplings with yoghurt and butter)", "complement", "established", "main", "Traditional Armenian dumplings with tangy yoghurt and the country's accessible red wine — a home pairing.")
    PAIR(prod5b, "Fresh white cheese (chechil) with watermelon", "contrast", "adventurous", "casual", "A classic Caucasian summer pairing: fresh salty cheese and sweet watermelon with chilled light red wine.")

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
