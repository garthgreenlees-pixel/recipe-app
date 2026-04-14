#!/usr/bin/env python3
"""B147 — Kakheti (Georgia), Bekaa Valley (Lebanon), Maipo Valley (Chile), Casablanca Valley (Chile), Luján de Cuyo (Argentina)"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(WRITE_DSN)
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

# ── 1. Kakheti (Georgia) ─────────────────────────────────────────────────────
print("=== Kakheti Wine Region (Georgia) ===")
r1 = R("Kakheti Wine Region", "Georgia", "wine",
        designation_type="PDO", designation_name="Kakheti",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Georgia's primary wine region, Kakheti accounts for over 70% of the country's wine production from a landscape of ancient vineyards in the foothills of the Caucasus. Georgia is widely considered the cradle of wine civilisation, with viticultural traditions dating back 8,000 years. Kakheti is the home of qvevri winemaking — fermenting and ageing in large clay amphorae buried in the earth — and the ancient amber wine tradition of skin-contact whites.",
        key_producers="Pheasant's Tears, Château Mukhrani, Iago's Wine, Alaverdi Monastery",
        historical_context="Georgia's winemaking history, dating to approximately 6000 BC, makes it the world's oldest wine culture. The qvevri — large terracotta vessels buried in the earth — have been used continuously since antiquity for both fermentation and storage. After Soviet collectivisation devastated traditional methods, a renaissance of natural, qvevri-based winemaking began in the 1990s, led by Pheasant's Tears' John Wurdeman and Georgian winemakers, bringing global attention to Georgia's indigenous varieties and ancient methods.")

for yr, qd, pt in [
    (2019, "very_good", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "very_good", "rising"), (2023, "good", "rising")]:
    VIN(r1, yr, qd, pt)

p1a = P("Pheasant's Tears", "winery", r1, "Georgia",
         production_philosophy="minimal_intervention",
         philosophy_description="Founded by American artist John Wurdeman and winemaker Gela Patalishvili, Pheasant's Tears is the international face of Georgia's natural wine renaissance. Working exclusively with indigenous varieties and qvevri, they produce wines that express 8,000 years of unbroken Georgian wine tradition.",
         reputation_narrative="Pheasant's Tears has become synonymous with Georgia's wine renaissance, appearing in the world's finest natural wine lists and demonstrating that amber wines from ancient qvevri can achieve world-class complexity. Their work has inspired a generation of natural winemakers globally.",
         price_positioning="mid_range")

prod1a1, new1 = PROD("Pheasant's Tears Rkatsiteli Kakheti", "wine_still", p1a, r1, "Georgia",
                      subcategory="Rkatsiteli", price_tier="mid_range",
                      description="An amber wine made from Georgia's most ancient white grape, Rkatsiteli, fermented on skins in qvevri for six months. The result is a profound, tannic white wine with dried apricot, beeswax, walnut, and a long, structured finish of extraordinary complexity — arguably the world's most distinctive expression of amber wine tradition.")
if new1:
    PAIR(prod1a1, "Badrijani nigvzit (eggplant rolls with walnut paste)", "complement", "classic", "starter", "The amber wine's walnut and beeswax character creates a profound resonance with walnut paste; eggplant's earthy depth and the wine's tannin find a unique balance in this quintessential Georgian pairing.")
    PAIR(prod1a1, "Roasted chicken with walnut sauce (satsivi)", "complement", "classic", "main", "Satsivi's rich walnut sauce is the quintessential pairing for Georgian amber wine; the wine's walnut character creates a direct flavour bridge while its tannin cuts through the sauce's richness.")
    PAIR(prod1a1, "Aged hard cheese with walnuts and herb flatbread", "complement", "classic", "cheese", "Georgia's aged cheeses and amber wines have coexisted for millennia; walnuts deepen the resonance between wine and food while flatbread ground the pairing in genuine Georgian tradition.")
    PAIR(prod1a1, "Smoked trout with pomegranate and herb salad", "complement", "established", "fish_course", "The wine's tannic structure and oxidative complexity cut through smoked fish's oiliness; pomegranate's tartness echoes the wine's acidity while herbs add aromatic freshness.")

prod1a2, new2 = PROD("Pheasant's Tears Saperavi Kakheti", "wine_still", p1a, r1, "Georgia",
                      subcategory="Saperavi", price_tier="mid_range",
                      description="Made from Saperavi — the ink-berry grape that produces one of the world's darkest red wines — this qvevri-aged expression is intensely coloured, tannic, and deeply flavoured. Blackberry, plum, earth, and spice with remarkable freshness and ageing potential.")
if new2:
    PAIR(prod1a2, "Georgian lamb stew (chakapuli) with tarragon and plum sauce", "complement", "classic", "main", "Saperavi's dark intensity and tannin are ideal for this festive Georgian spring lamb dish; plum sauce echoes the wine's fruit while tarragon adds aromatic contrast.")
    PAIR(prod1a2, "Grilled beef mtsvadi (skewers) with tkemali plum sauce", "complement", "classic", "main", "The quintessential Georgian wine pairing: Saperavi's dark fruit and firm tannin frame grilled beef with precision; tkemali's tart plum mirrors the wine's own dark fruit character.")
    PAIR(prod1a2, "Walnut and herb flatbread (shotis puri) with aged cheese", "complement", "established", "casual", "The wine's power and dark fruit find an anchoring in Georgia's traditional flatbreads and aged cheeses; the combination is a snapshot of the country's ancient food and wine culture.")
    PAIR(prod1a2, "Wild mushroom khinkali (dumplings) with sour cream", "complement", "established", "main", "Saperavi's earthy depth and firm structure complement mushroom khinkali's rich filling; sour cream softens the wine's tannin while the dumpling's broth adds the savoury depth the wine demands.")

p1b = P("Alaverdi Monastery Winery", "winery", r1, "Georgia",
         production_philosophy="classical",
         philosophy_description="Alaverdi Monastery, founded in the 6th century, has been making wine in qvevri buried in the monastery cellar since medieval times. The monks maintain unbroken continuity with Georgia's ancient winemaking tradition, producing wines that are simultaneously liturgical objects and expressions of extraordinary terroir.",
         reputation_narrative="Alaverdi Monastery is one of the world's oldest continuously operating wineries, its 900-year-old cellar containing ancient qvevri that have produced wine without interruption. The monastery's wines are among Georgia's most culturally significant and are collected worldwide.",
         price_positioning="premium")

prod1b1, new3 = PROD("Alaverdi Monastery Mtsvane Kakheti Qvevri", "wine_still", p1b, r1, "Georgia",
                      subcategory="Mtsvane", price_tier="premium",
                      description="Monk-made amber wine from the ancient Mtsvane variety, fermented and aged in the monastery's centuries-old qvevri. Displaying quince, dried herbs, and walnut with a long, tannic finish — this wine carries 1,400 years of unbroken monastic winemaking tradition.")
if new3:
    PAIR(prod1b1, "Roasted suckling pig with pomegranate glaze and herbs", "complement", "established", "main", "The amber wine's tannic structure and dried-fruit character provide an ancient framework for roasted pork; pomegranate's tartness echoes the wine's acidity while herbs bridge its complexity.")
    PAIR(prod1b1, "Sulguni cheese with herbs and grilled flatbread", "complement", "classic", "casual", "Georgia's most beloved cheese and the monastery's amber wine share a cultural and geographic home; the wine's tannin cuts through the cheese's fresh acidity while herbs add aromatic depth.")
    PAIR(prod1b1, "Herb-spiced whole grilled fish with walnut sauce", "complement", "established", "fish_course", "The wine's walnut character creates an extraordinary bridge with walnut sauce; herbs echo the wine's dried-herb complexity while the fish's sweetness is framed by the wine's tannic structure.")
    PAIR(prod1b1, "Badrijani nigvzit with sour plum chutney", "complement", "classic", "starter", "This classic Georgian vegetable dish — eggplant rolled with walnut paste — resonates directly with the wine's own walnut character; sour plum chutney provides the acidity that keeps the pairing vibrant.")

prod1b2, new4 = PROD("Alaverdi Monastery Saperavi Kakheti Reserve", "wine_still", p1b, r1, "Georgia",
                      subcategory="Saperavi", price_tier="premium",
                      description="The monastery's flagship red, a Saperavi of extraordinary depth and complexity aged in the ancient cellar in qvevri. The wine's dark colour, intense tannin, and profound blackberry-earth character reflect both the variety's inherent power and the monastery's centuries of accumulated winemaking wisdom.")
if new4:
    PAIR(prod1b2, "Wild boar roast with pomegranate and plum sauce", "complement", "classic", "main", "Game meat of this intensity demands Saperavi's dark power; pomegranate and plum sauce echo the wine's fruit while providing the sweetness that balances its firm tannin.")
    PAIR(prod1b2, "Lamb shoulder cooked in clay pot with dried fruits and spices", "complement", "classic", "main", "The ancient method of clay-pot cooking creates a profound resonance with qvevri-aged wine; dried fruits mirror the wine's dark fruit while warming spices echo its earthy complexity.")
    PAIR(prod1b2, "Aged Tushuri Guda cheese (sheep's milk) with honey", "complement", "established", "cheese", "Georgia's strongest and most complex aged cheese matches Alaverdi Saperavi's power and depth; honey softens the intensity while creating a bridge between the wine's fruit and the cheese's crystalline richness.")
    PAIR(prod1b2, "Charcoal-grilled ribeye with Georgian spice rub and vegetables", "complement", "classic", "main", "The monastery Saperavi's power and structure demand charcoal-grilled beef; Georgian spice rub amplifies the wine's own earthy complexity while vegetables provide freshness.")

# ── 2. Bekaa Valley (Lebanon) ────────────────────────────────────────────────
print("=== Bekaa Valley (Lebanon) ===")
r2 = R("Bekaa Valley", "Lebanon", "wine",
        designation_type="region", designation_name="Bekaa Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="The Bekaa Valley, Lebanon's primary wine region, lies between the Mount Lebanon and Anti-Lebanon ranges at elevations of 900–1,100 metres. The high altitude, continental climate, and calcareous soils create conditions for wines of remarkable freshness and complexity. Lebanon has one of the oldest winemaking histories in the world, with Phoenician traders spreading viticulture across the Mediterranean.",
        key_producers="Château Musar, Domaine des Tourelles, Ksara, Massaya, Château Kefraya",
        historical_context="Lebanon's winemaking history traces to the Phoenicians, who carried wine from the Bekaa Valley across the ancient world. The Romans established vineyards near the temple at Baalbek. Modern Lebanese wine was largely established by Gaston Hochar at Château Musar in the 1930s, who continued producing wine through Lebanon's civil war — becoming one of the world's great stories of winemaking perseverance.")

for yr, qd, pt in [
    (2019, "excellent", "stable"), (2020, "very_good", "stable"), (2021, "very_good", "stable"),
    (2022, "good", "stable"), (2023, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Château Musar", "winery", r2, "Lebanon",
         production_philosophy="minimal_intervention",
         philosophy_description="Founded by Gaston Hochar in 1930 and elevated to global recognition by his son Serge, Château Musar produces one of the world's most distinctive red wines from old Cabernet Sauvignon, Cinsault, and Carignan vines in the Bekaa Valley. The wines are released only after seven years of ageing.",
         reputation_narrative="Château Musar is one of the wine world's most revered names, both for the extraordinary complexity and longevity of its wines and for the remarkable story of Serge Hochar, who continued making wine throughout Lebanon's devastating civil war. Musar Red is considered one of the world's great aged wines.",
         price_positioning="premium")

prod2a1, new5 = PROD("Château Musar Red Bekaa Valley", "wine_still", p2a, r2, "Lebanon",
                      subcategory="Cabernet Sauvignon blend", price_tier="premium",
                      description="A blend of Cabernet Sauvignon, Cinsault, and Carignan from old vines in the Bekaa Valley, released only after seven years of maturation. Musar Red is a wine of extraordinary complexity: dried fruit, leather, tobacco, and earth with a gossamer texture and a finish that evolves for decades in the bottle.")
if new5:
    PAIR(prod2a1, "Slow-braised lamb with cinnamon, allspice, and dried fruits", "complement", "classic", "main", "Musar Red's dried-fruit and spice complexity is profoundly resonant with this Levantine preparation; cinnamon and allspice echo the wine's warm spice while dried fruits mirror its concentrated fruit character.")
    PAIR(prod2a1, "Kibbeh nayyeh (raw lamb with bulgur and pine nuts)", "complement", "classic", "starter", "The wine's silken texture and iron-mineral depth are the traditional Lebanese companion to raw kibbeh; pine nuts add a savoury richness while bulgur grounds the delicate pairing.")
    PAIR(prod2a1, "Slow-roasted shoulder of goat with Lebanese seven-spice", "complement", "classic", "main", "Seven-spice (baharat) resonates with the wine's own complex spice profile; goat's rich intensity demands Musar's structure and aged complexity in this classic Lebanese pairing.")
    PAIR(prod2a1, "Aged Akkawi cheese with zaatar and olive oil flatbread", "complement", "established", "cheese", "The wine's earthy complexity and dried-fruit character find a profound partner in aged Akkawi; zaatar's herb blend echoes the wine's herbal notes while olive oil flatbread grounds the combination.")

prod2a2, new6 = PROD("Château Musar White Bekaa Valley", "wine_still", p2a, r2, "Lebanon",
                      subcategory="Obaideh and Merwah", price_tier="premium",
                      description="Made from the ancient indigenous varieties Obaideh and Merwah — possibly the ancestors of Chardonnay and Semillon — Musar White is vinified and aged like a red wine with extended oak ageing, producing a white of extraordinary oxidative complexity: honey, beeswax, spice, and a long savoury finish.")
if new6:
    PAIR(prod2a2, "Roasted whole cauliflower with tahini, lemon, and pine nuts", "complement", "established", "main", "The wine's oxidative complexity and nutty depth find resonance with roasted cauliflower; tahini's sesame richness bridges the wine's character while lemon cuts through the fat.")
    PAIR(prod2a2, "Grilled fish kafta with tomato and onion", "complement", "established", "fish_course", "Musar White's structured complexity and aged character can navigate spiced fish preparations with ease; tomato's acidity bridges the wine's oxidative depth while onion adds savoury depth.")
    PAIR(prod2a2, "Fatteh (toasted bread with chickpeas, yogurt, and tahini)", "complement", "established", "casual", "The wine's honey and beeswax character find unexpected harmony with fatteh's layered textures; yogurt's acidity echoes the wine's own while tahini deepens the savoury connection.")
    PAIR(prod2a2, "Aged Halloumi grilled with herbs and honey", "complement", "established", "cheese", "Musar White's aged complexity is well matched to grilled halloumi's caramelised saltiness; honey bridges the wine's sweet oxidative notes while herbs add aromatic freshness.")

p2b = P("Domaine des Tourelles", "winery", r2, "Lebanon",
         production_philosophy="classical",
         philosophy_description="One of Lebanon's oldest wineries, founded in 1868, Domaine des Tourelles produces a wide range of wines from Bekaa Valley grapes with a strong emphasis on indigenous and Mediterranean varieties including Cinsault, Obaideh, and Obeidy.",
         reputation_narrative="Domaine des Tourelles is Lebanon's most historic privately owned winery, its century of production providing continuity through the country's turbulent modern history. Their Cinsault is widely regarded as one of Lebanon's finest red wines.",
         price_positioning="mid_range")

prod2b1, new7 = PROD("Domaine des Tourelles Cinsault Bekaa Valley", "wine_still", p2b, r2, "Lebanon",
                      subcategory="Cinsault", price_tier="mid_range",
                      description="A pure Cinsault from old Bekaa Valley vines, displaying the variety's hallmark light body, red cherry, and dried herb character with an earthy, almost Mediterranean quality that speaks directly of the ancient Levantine landscape.")
if new7:
    PAIR(prod2b1, "Grilled lamb kofta with sumac onions and flatbread", "complement", "classic", "main", "Cinsault's light frame and dried-herb character are a natural complement to Lebanese kofta; sumac's tartness echoes the wine's acidity while flatbread grounds the combination.")
    PAIR(prod2b1, "Roasted eggplant with pomegranate and walnut (muhammara)", "complement", "established", "starter", "The wine's red cherry and earth resonate with roasted eggplant's smokiness; pomegranate's tartness bridges the wine's acidity while muhammara's walnut depth adds complexity.")
    PAIR(prod2b1, "Mezze board with kibbeh, hummus, and tabbouleh", "complement", "classic", "casual", "Cinsault's versatility and moderate tannin make it the ideal wine for a mezze spread; hummus's creaminess, tabbouleh's freshness, and kibbeh's spice each find traction against the wine's balanced character.")
    PAIR(prod2b1, "Cheese fatayer (pastry filled with white cheese and herbs)", "complement", "established", "casual", "The wine's light frame and herb character are well matched to herb-filled pastry; white cheese's mild saltiness is balanced by the wine's acidity.")

prod2b2, new8 = PROD("Domaine des Tourelles Marquis des Beys Red Bekaa", "wine_still", p2b, r2, "Lebanon",
                      subcategory="Cabernet Sauvignon blend", price_tier="mid_range",
                      description="The Tourelles flagship, a Syrah, Cabernet Sauvignon, and Cinsault blend from the Bekaa Valley, aged in French oak. More structured and internationally styled than the Cinsault, this wine demonstrates Lebanon's capacity for serious red wine at an accessible price point.")
if new8:
    PAIR(prod2b2, "Mansaf (lamb in jameed yogurt with rice and almonds)", "complement", "classic", "main", "Lebanon's most festive dish demands a wine of structure; the wine's dark fruit and oak character complement the lamb's intensity while the jameed's fermented sharpness is balanced by the wine's fruit.")
    PAIR(prod2b2, "Kafta with tomato and potato tray bake", "complement", "classic", "main", "The wine's accessible structure and dark fruit are perfectly calibrated for everyday Lebanese kafta; tomato's acidity bridges the wine while potato absorbs the rich meat juices.")
    PAIR(prod2b2, "Grilled chicken with garlic sauce (toum) and lemon", "complement", "established", "main", "The wine's fruit and moderate tannin frame grilled chicken without overwhelming it; toum's pungent garlic adds depth while lemon bridges the wine's acidity.")
    PAIR(prod2b2, "Labneh with za'atar and olive oil on flatbread", "complement", "classic", "casual", "The wine's fruit and gentle structure navigate labneh's creamy tang; za'atar's thyme and sesame add Mediterranean depth that echoes the wine's own character.")

# ── 3. Maipo Valley (Chile) ──────────────────────────────────────────────────
print("=== Maipo Valley (Chile) ===")
r3 = R("Maipo Valley", "Chile", "wine",
        designation_type="DO", designation_name="Valle del Maipo",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Maipo Valley, immediately south of Santiago and one of Chile's oldest wine regions, is the heartland of Chilean Cabernet Sauvignon. The region's warm days and cool nights, gravelly soils, and proximity to the Andes create conditions for Cabernet of remarkable structure and elegance. Maipo is home to Chile's most storied and prestigious wine estates.",
        key_producers="Concha y Toro (Don Melchor), Almaviva, Santa Rita, Cousiño-Macul, Casa Lapostolle",
        historical_context="Winemaking in the Maipo Valley dates to the 16th century Spanish colonisation, with serious viticulture established by French-educated Chilean families in the 1850s. The region's reputation as Chile's premier Cabernet zone was cemented in the late 20th century when estates like Almaviva and Don Melchor began competing with Bordeaux's finest for international recognition.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"), (2023, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Viña Almaviva", "winery", r3, "Chile",
         production_philosophy="classical",
         philosophy_description="A joint venture between Concha y Toro and Baron Philippe de Rothschild, Almaviva is Chile's prestige Bordeaux-style blend, made from Puente Alto Cabernet Sauvignon in the Maipo Valley. The two families' combined expertise represents the pinnacle of Chilean fine wine.",
         reputation_narrative="Almaviva is consistently Chile's most internationally recognised prestige wine, its deep Cabernet Sauvignon concentration and Bordeaux-inspired complexity placing it among the world's great red wines. Its price and critical standing are matched only by Concha y Toro's Don Melchor.",
         price_positioning="ultra_premium")

prod3a1, new9 = PROD("Almaviva Maipo Valley", "wine_still", p3a, r3, "Chile",
                      subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                      description="Chile's most prestigious wine, a Cabernet Sauvignon-led blend from Puente Alto in the Maipo Valley, made with Rothschild expertise. Almaviva displays profound cassis, graphite, and cedar with silken tannin and a finish of extraordinary length — one of the southern hemisphere's greatest red wines.")
if new9:
    PAIR(prod3a1, "Roasted rack of lamb with Dijon crust and red wine jus", "complement", "classic", "main", "Almaviva's Bordeaux character and concentration are the perfect companion for this classic preparation; Dijon's mustard echoes the wine's herbal notes while the red wine jus creates a direct bridge.")
    PAIR(prod3a1, "Beef tenderloin Wellington with mushroom duxelles and truffle butter", "complement", "classic", "main", "The wine's prestige demands preparation of equal standing; Wellington's mushroom duxelles and truffle butter amplify Almaviva's earthy complexity while the pastry adds luxury texture.")
    PAIR(prod3a1, "Aged Parmesan and Manchego cheese board with Andean truffle", "complement", "established", "cheese", "Almaviva's concentration and cedar character find resonance with aged hard cheeses; Andean truffle adds a distinctly South American luxury note that bridges continent and variety.")
    PAIR(prod3a1, "Chilean asado beef ribs with pebre and marraqueta bread", "complement", "classic", "main", "Almaviva over Chilean asado is the ultimate expression of the country's wine and food culture; pebre's fresh herb and chili character provides the contrast that keeps this luxury pairing vibrant.")

prod3a2, new10 = PROD("Concha y Toro Don Melchor Maipo Valley", "wine_still", p3a, r3, "Chile",
                       subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                       description="From Puente Alto's Quebrada de Macul vineyard, Don Melchor is Concha y Toro's single-vineyard icon: a pure Cabernet Sauvignon of extraordinary precision and ageing potential. Deep cassis, graphite, dried herb, and a tannin structure built for decades of development.")
if new10:
    PAIR(prod3a2, "Grilled wagyu T-bone with chimichurri and roasted garlic", "complement", "classic", "main", "Don Melchor's power and precision demand wagyu's extraordinary marbling; chimichurri's herb brightness provides the contrast that keeps the luxury pairing balanced.")
    PAIR(prod3a2, "Braised short rib with malbec reduction and root vegetable purée", "complement", "established", "main", "The wine's structure and concentration are ideal companions for long-braised short rib; the malbec reduction creates a wine-based bridge while root vegetable purée softens the tannic intensity.")
    PAIR(prod3a2, "Blue cheese and walnut tart with honey", "complement", "suggested", "cheese", "Don Melchor's power can stand opposite blue cheese's intensity; walnut bridges the wine's own earthy depth while honey softens the contrast to a harmonious balance.")
    PAIR(prod3a2, "Casado de campo (countryside stew with beef, vegetables, and corn)", "complement", "established", "main", "Don Melchor's Cabernet structure navigates this hearty Chilean country stew with ease; the wine's precision lifts the rustic combination into a compelling expression of Chilean terroir.")

p3b = P("Santa Rita 120", "winery", r3, "Chile",
         production_philosophy="sustainable",
         philosophy_description="Santa Rita is one of Chile's most historic estates, founded in 1880 and based in the Maipo Valley. Their Casa Real is one of Chile's most age-worthy Cabernets, while the 120 range named for Chilean independence fighters provides reliable quality at accessible prices.",
         reputation_narrative="Santa Rita's Casa Real Cabernet Sauvignon is consistently among Chile's finest expressions of the variety, combining Maipo Valley concentration with the elegance that comes from high-altitude, south-facing slopes.",
         price_positioning="mid_range")

prod3b1, new11 = PROD("Santa Rita Casa Real Cabernet Sauvignon Maipo", "wine_still", p3b, r3, "Chile",
                       subcategory="Cabernet Sauvignon", price_tier="premium",
                       description="Santa Rita's prestige bottling, from the estate's finest Maipo Valley vineyards. Casa Real is a concentrated, structured Cabernet of impressive depth and age-worthiness, displaying classic Maipo character: cassis, cedar, and graphite with firm tannin and excellent acidity.")
if new11:
    PAIR(prod3b1, "Grilled lamb with chimichurri and roasted potatoes", "complement", "classic", "main", "A classic Chilean pairing: Casa Real's structure and cassis depth are natural companions for grilled lamb; chimichurri's herb and vinegar brightness provides the contrast that keeps the pairing lively.")
    PAIR(prod3b1, "Asado de tira (short ribs) with pebre and Chilean bread", "complement", "classic", "main", "The Chilean national barbecue dish demands a Cabernet of this standing; pebre's fresh character contrasts with the wine's concentration while the bread absorbs the asado's rendered fat.")
    PAIR(prod3b1, "Empanadas de pino (beef, olive, egg, and raisin pastry)", "complement", "classic", "casual", "Chile's most beloved pastry and Maipo Cabernet is a national pairing; the empanada's olive and raisin filling echoes the wine's savoury-fruit complexity while the pastry's richness is balanced by the wine's tannin.")
    PAIR(prod3b1, "Aged Chanco cheese with fig jam and toasted nuts", "complement", "established", "cheese", "Chile's own aged cheese with Maipo Cabernet is a classic regional pairing; fig jam bridges the wine's fruit while toasted nuts add savoury complexity.")

prod3b2, new12 = PROD("Santa Rita Triple C Maipo Valley", "wine_still", p3b, r3, "Chile",
                       subcategory="Cabernet blend", price_tier="premium",
                       description="Triple C — Cabernet Sauvignon, Cabernet Franc, and Carménère — is Santa Rita's innovative three-variety blend from the Maipo Valley. The Carménère's green pepper and chocolate add distinctive Chilean character to the classic Bordeaux framework, creating a wine of complex individuality.")
if new12:
    PAIR(prod3b2, "Lomo a lo pobre (steak with fried eggs, onions, and fries)", "complement", "classic", "main", "Chile's most beloved steak dish demands Triple C's full complexity; the fried egg's richness is cut by the wine's tannin while onions and fries ground the pairing in Chilean tradition.")
    PAIR(prod3b2, "Charcoal-grilled chicken thighs with ají amarillo and lime", "complement", "established", "main", "The wine's Carménère green note and cassis depth navigate ají amarillo's complex chili heat; lime bridges the wine's acidity while the charcoal char complements its dark fruit.")
    PAIR(prod3b2, "Mushroom and Carménère ragù with fresh pasta", "bridge", "established", "main", "Triple C's Carménère component creates a direct bridge with this pasta sauce's wine character; mushroom's umami deepens the connection while pasta absorbs the complex ragù.")
    PAIR(prod3b2, "Smoked provoleta with oregano and chimichurri", "complement", "established", "casual", "Smoked provolone's caramelised crust and the wine's dark fruit are a classic Argentine-Chilean combination; chimichurri's freshness contrasts the wine's concentration while oregano bridges its herbal notes.")

# ── 4. Casablanca Valley (Chile) ─────────────────────────────────────────────
print("=== Casablanca Valley (Chile) ===")
r4 = R("Casablanca Valley", "Chile", "wine",
        designation_type="DO", designation_name="Valle de Casablanca",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Casablanca Valley, between Santiago and Valparaíso, pioneered cool-climate winemaking in Chile when Pablo Morande planted the first vineyards in 1982. The Pacific Ocean's cooling influence and morning fog create ideal conditions for aromatic whites — Sauvignon Blanc and Chardonnay — and elegant Pinot Noir, bringing international attention to Chile's cool-climate potential.",
        key_producers="Viña Casablanca, Concha y Toro (Amelia), Errázuriz (Aconcagua Costa), Casa Marin",
        historical_context="Before 1982, Chile's wine industry was concentrated in warm inland valleys. Pablo Morande's pioneering planting in Casablanca revealed that the cool coastal influence could produce wines of Burgundian character. The valley's rapid development in the 1990s transformed Chile's international wine reputation and opened a new chapter in South American winemaking.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"), (2023, "very_good", "rising")]:
    VIN(r4, yr, qd, pt)

p4a = P("Viña Casablanca", "winery", r4, "Chile",
         production_philosophy="terroir_expression",
         philosophy_description="The founding estate of the Casablanca Valley, established by Pablo Morande in 1992, Viña Casablanca continues to explore the valley's cool-climate potential with a focus on Sauvignon Blanc, Chardonnay, and Pinot Noir.",
         reputation_narrative="Viña Casablanca's pivotal role in establishing the valley's reputation makes it the region's landmark estate. Their wines consistently demonstrate the freshness and aromatic precision that have made Casablanca Chile's most respected cool-climate appellation.",
         price_positioning="mid_range")

prod4a1, new13 = PROD("Viña Casablanca Nimbus Sauvignon Blanc Casablanca", "wine_still", p4a, r4, "Chile",
                       subcategory="Sauvignon Blanc", price_tier="mid_range",
                       description="A cool-climate Casablanca Sauvignon Blanc of precision and focus, displaying fresh-cut grass, lime, and grapefruit with a long, mineral finish. The Casablanca Valley's fog-cooled mornings produce a natural acidity that makes this wine one of Chile's most food-friendly whites.")
if new13:
    PAIR(prod4a1, "Ceviche with lime, ají amarillo, and red onion", "complement", "classic", "starter", "Casablanca Sauvignon's lime acidity and grassy freshness echo ceviche's citrus-cured character; ají amarillo adds depth while red onion's sharpness bridges the wine's own vivid acidity.")
    PAIR(prod4a1, "Grilled sea bass with lemon herb butter and salsa verde", "complement", "classic", "fish_course", "The wine's precision and herb character are ideal complements for delicate grilled fish; herb salsa verde mirrors the wine's own grassiness while lemon amplifies its citrus.")
    PAIR(prod4a1, "Goat cheese tostadas with avocado and microgreens", "complement", "established", "starter", "Sauvignon Blanc and goat cheese is a classic pairing elevated by Chile's cool-climate precision; avocado's creaminess softens the wine's acidity while microgreens echo its fresh green character.")
    PAIR(prod4a1, "Oysters with Peruvian leche de tigre dressing", "complement", "classic", "aperitif", "The wine's mineral acidity and citrus depth are ideal for oysters; leche de tigre's citrus and chili character intensifies the pairing while the wine's freshness cleanses the palate.")

prod4a2, new14 = PROD("Viña Casablanca Nimbus Pinot Noir Casablanca", "wine_still", p4a, r4, "Chile",
                       subcategory="Pinot Noir", price_tier="mid_range",
                       description="From the cool Casablanca Valley, this Pinot Noir displays the delicacy and freshness characteristic of Chile's cool-climate regions: wild strawberry, cherry, and subtle earth with a light body and refreshing acidity that make it ideal for food.")
if new14:
    PAIR(prod4a2, "Salmon tartare with capers, shallots, and lemon crème fraîche", "complement", "established", "starter", "Cool-climate Casablanca Pinot and salmon is a Pacific Rim classic; the wine's strawberry freshness and light tannin complement the raw fish while capers echo its acidity.")
    PAIR(prod4a2, "Roasted mushroom and brie tart with thyme", "complement", "established", "starter", "The wine's earthy delicacy resonates with mushroom's umami; brie's creaminess is balanced by the wine's bright acidity while thyme echoes its forest-floor character.")
    PAIR(prod4a2, "Duck breast with cherry sauce and braised lentils", "complement", "classic", "main", "Casablanca Pinot's red-fruit freshness and light structure complement duck without overwhelming its delicacy; cherry sauce creates a direct flavour bridge while lentils add earthy depth.")
    PAIR(prod4a2, "Grilled salmon with pinot noir butter and roasted asparagus", "complement", "classic", "main", "The West Coast benchmark pairing translated to Chile: Casablanca Pinot and salmon is a natural marriage, the wine's fruit and acidity framing the fish's richness perfectly.")

p4b = P("Casa Marin", "winery", r4, "Chile",
         production_philosophy="terroir_expression",
         philosophy_description="María Luz Marín's estate in Lo Abarca is Casablanca Valley's extreme cool-climate site, closest to the Pacific Ocean. Her Sauvignon Blanc and Pinot Noir are among Chile's most distinctive cool-climate wines, reflecting a singular vision for the variety's expression in maritime conditions.",
         reputation_narrative="Casa Marin's extreme coastal location and María Luz Marín's pioneering spirit have produced some of Chile's most distinctive white wines, with her Sauvignon Blancs achieving international recognition for their mineral precision and cool-climate intensity.",
         price_positioning="premium")

prod4b1, new15 = PROD("Casa Marin Cipreses Sauvignon Blanc Casablanca", "wine_still", p4b, r4, "Chile",
                       subcategory="Sauvignon Blanc", price_tier="premium",
                       description="From the extreme coastal location of Casa Marin's Lo Abarca estate, Cipreses is one of Chile's most distinctive Sauvignon Blancs: intense mineral-citrus character, flint, white peach, and a salty coastal finish that reflects the Pacific's direct influence on the vineyard.")
if new15:
    PAIR(prod4b1, "Sea urchin with yuzu butter on toasted brioche", "complement", "classic", "starter", "The wine's oceanic salinity and mineral intensity are a natural companion for uni; yuzu's citrus mirrors the wine's own while brioche adds the richness that softens the wine's intensity.")
    PAIR(prod4b1, "Crab salad with avocado, lime, and fresh coriander", "complement", "classic", "starter", "Cipreses's coastal mineral character echoes the crab's oceanic sweetness; avocado's creaminess buffers the wine's acidity while lime reinforces its citrus depth.")
    PAIR(prod4b1, "Grilled langoustines with garlic, chili, and lemon", "complement", "classic", "fish_course", "The wine's mineral precision and citrus depth frame langoustine's sweetness perfectly; garlic adds savoury depth while chili provides a contrast note that the wine's acidity can absorb.")
    PAIR(prod4b1, "Oyster tartare with cucumber, mignonette, and sea herbs", "complement", "classic", "aperitif", "Cipreses's saline coastal mineral character makes it perhaps Chile's finest oyster wine; sea herbs echo the wine's maritime terroir in this elegant expression of place.")

prod4b2, new16 = PROD("Casa Marin Lo Abarca Pinot Noir Casablanca", "wine_still", p4b, r4, "Chile",
                       subcategory="Pinot Noir", price_tier="premium",
                       description="From the extreme Pacific-influenced Lo Abarca estate, this Pinot Noir is one of Chile's most distinctive reds: translucent red fruit, sea salt, forest floor, and a tightly wound mineral structure that reflects the vineyard's extreme coastal exposure.")
if new16:
    PAIR(prod4b2, "Grilled turbot with mushroom cream and caper butter", "complement", "established", "fish_course", "The wine's coastal mineral depth and translucent red fruit create an unusual but compelling match for turbot; mushroom cream bridges the earthy character while caper butter mirrors the wine's salt-mineral character.")
    PAIR(prod4b2, "Wild mushroom risotto with Parmesan and truffle oil", "complement", "established", "main", "Lo Abarca Pinot's earthy, mineral character finds resonance with truffle and wild mushroom; Parmesan's umami amplifies the savoury connection while risotto's creaminess buffers the wine's structure.")
    PAIR(prod4b2, "Duck confit with lentils du Puy and red wine reduction", "complement", "classic", "main", "The wine's coastal minerality and red-fruit freshness are ideal complements for duck confit; lentils add earthy depth while the reduction creates a wine-based bridge between plate and glass.")
    PAIR(prod4b2, "Aged Manchego with black cherry preserve and Marcona almonds", "complement", "established", "cheese", "The wine's cherry fruit and mineral depth find resonance with aged Manchego's nuttiness; black cherry preserve echoes the wine's fruit while almonds add savoury depth.")

# ── 5. Luján de Cuyo (Argentina) ─────────────────────────────────────────────
print("=== Luján de Cuyo (Argentina) ===")
r5 = R("Luján de Cuyo", "Argentina", "wine",
        designation_type="DO", designation_name="Luján de Cuyo",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Luján de Cuyo, in Argentina's Mendoza province, was the country's first designated Denominación de Origen Controlada. At elevations of 900–1,100 metres, this sub-zone of Mendoza produces Argentina's finest Malbec: wines of exceptional concentration, floral violet character, and velvety tannin that represent the pinnacle of the variety's expression outside France.",
        key_producers="Catena Zapata, Achaval Ferrer, Clos de los Siete, Terrazas de los Andes, Viña Cobos",
        historical_context="Luján de Cuyo's reputation as Argentina's premier Malbec zone was established in the 1990s when Nicolas Catena revolutionised Argentine winemaking by planting high-altitude Malbec vineyards and seeking international quality benchmarks. The subsequent investment by Michel Rolland (Clos de los Siete) and Paul Hobbs (Viña Cobos) confirmed the region's world-class potential.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r5, yr, qd, pt)

p5a = P("Catena Zapata", "winery", r5, "Argentina",
         production_philosophy="terroir_expression",
         philosophy_description="Nicolas Catena Zapata is Argentina's most significant wine figure, having revolutionised the country's wine industry by planting high-altitude vineyards and pursuing international quality standards from the 1980s. Catena Zapata's flagship Adrianna Vineyard is considered Argentina's greatest wine site.",
         reputation_narrative="Catena Zapata is Argentina's most internationally recognised winery, with Adrianna Vineyard wines consistently earning perfect scores and placing Argentina in conversation with the world's greatest wine regions. Nicolas and Laura Catena's scientific approach to terroir expression has defined modern Argentine wine.",
         price_positioning="ultra_premium")

prod5a1, new17 = PROD("Catena Zapata Adrianna Vineyard White Bones Chardonnay", "wine_still", p5a, r5, "Argentina",
                       subcategory="Chardonnay", price_tier="ultra_premium",
                       description="From the Adrianna Vineyard at 1,500 metres elevation in Gualtallary — considered Argentina's greatest wine site — White Bones is a Chardonnay of extraordinary mineral precision. Limestone-derived minerality, lemon curd, and hazelnut combine in a wine that challenges Burgundy's finest at a fraction of the price.")
if new17:
    PAIR(prod5a1, "Grilled langoustines with bone marrow butter and sea herbs", "complement", "classic", "fish_course", "The wine's extraordinary precision and mineral depth demand preparation of this luxury level; bone marrow butter's richness is balanced by the wine's acidity while sea herbs mirror its mineral character.")
    PAIR(prod5a1, "Roasted lobster with Adrianna Vineyard-inspired citrus butter", "complement", "classic", "main", "White Bones's limestone mineral depth and citrus precision are a natural companion for lobster; citrus butter creates a flavour echo between wine and food while amplifying the wine's acidity.")
    PAIR(prod5a1, "White asparagus with truffle vinaigrette and bottarga", "complement", "established", "starter", "The wine's mineral complexity and precision handle asparagus and truffle with equal confidence; bottarga's umami salinity amplifies the wine's limestone mineral character.")
    PAIR(prod5a1, "Aged Comté with white truffle and hazelnut", "complement", "established", "cheese", "White Bones's hazelnut complexity and mineral depth find a profound partner in aged Comté; white truffle deepens the earthy resonance while hazelnut creates a direct flavour bridge.")

prod5a2, new18 = PROD("Catena Zapata Nicolás Catena Zapata Luján de Cuyo", "wine_still", p5a, r5, "Argentina",
                       subcategory="Malbec", price_tier="ultra_premium",
                       description="Argentina's most iconic wine, a Malbec and Cabernet Sauvignon blend from the highest-elevation vineyards in Luján de Cuyo. Nicolás Catena Zapata is a wine of extraordinary intensity and elegance: violet, dark plum, graphite, and fine-grained tannin that places it among the world's great red wines.")
if new18:
    PAIR(prod5a2, "Argentine asado — whole rib roast over fire with chimichurri", "complement", "classic", "main", "The ultimate Argentine pairing: Nicolás Catena Zapata's power and elegance are the ideal companion for the country's national dish; chimichurri's herb brightness provides the contrast that keeps the luxury pairing vibrant.")
    PAIR(prod5a2, "Rack of lamb with Mendoza olive crust and red wine reduction", "complement", "classic", "main", "The wine's violet florality and dark-fruit concentration are a classic match for lamb; Mendoza olives echo the wine's terroir while red wine reduction deepens the connection between plate and glass.")
    PAIR(prod5a2, "Wagyu beef tartare with truffle and quail egg", "complement", "established", "starter", "The wine's prestige demands luxury preparation even at the starter course; truffle amplifies its earthy depth while wagyu's extraordinary fat mirrors the wine's velvety tannin.")
    PAIR(prod5a2, "Aged Sardo cheese with dulce de membrillo and Andean walnuts", "complement", "classic", "cheese", "The wine's power and complexity need an aged Argentine sheep's milk cheese; dulce de membrillo bridges its fruit while Andean walnuts echo its earthy depth.")

p5b = P("Achaval Ferrer", "winery", r5, "Argentina",
         production_philosophy="terroir_expression",
         philosophy_description="Founded in 1998 by Santiago Achaval and Roberto Cipresso, Achaval Ferrer produces single-vineyard Malbec wines from old Luján de Cuyo vines that are considered benchmarks of Argentine terroir expression. Their Finca Altamira, Bella Vista, and Mirador wines are among Argentina's most collected.",
         reputation_narrative="Achaval Ferrer's three single-vineyard Malbecs are routinely cited as Argentina's finest terroir-expressive wines, demonstrating that Argentine wine can achieve Burgundy-level site specificity. The estate's old vines are among Mendoza's most precious viticultural heritage.",
         price_positioning="premium")

prod5b1, new19 = PROD("Achaval Ferrer Finca Altamira Malbec Luján de Cuyo", "wine_still", p5b, r5, "Argentina",
                       subcategory="Malbec", price_tier="premium",
                       description="From a single vineyard in Perdriel, Altamira is Achaval Ferrer's most celebrated wine: old-vine Malbec of extraordinary concentration and mineral precision, with violet, dark plum, black chocolate, and a fine-grained tannic structure that rewards a decade of cellaring.")
if new19:
    PAIR(prod5b1, "Slow-roasted boneless leg of lamb with chimichurri rojo", "complement", "classic", "main", "Finca Altamira's concentration and elegance are perfectly calibrated for slow-roasted lamb; chimichurri rojo's red chili and herb character provides the bright contrast the wine demands.")
    PAIR(prod5b1, "Beef empanadas with olives, eggs, and spices", "complement", "classic", "casual", "The wine's dark-fruit concentration and Argentine character are ideal for empanadas; the olive filling echoes the wine's savoury depth while the spiced beef mirrors its complexity.")
    PAIR(prod5b1, "Grilled provoleta with oregano and crushed red chili", "complement", "classic", "casual", "Old-vine Malbec and provoleta is a classic Argentine pairing; the cheese's caramelised saltiness finds traction against the wine's dark fruit and fine tannin while oregano and chili add Mediterranean depth.")
    PAIR(prod5b1, "Wild mushroom and Malbec ragù with handmade pasta", "bridge", "established", "main", "The wine's dark fruit and earthy depth resonate profoundly with mushroom ragù; a Malbec reduction in the sauce creates a direct flavour bridge while pasta absorbs the intensity.")

prod5b2, new20 = PROD("Achaval Ferrer Malbec Mendoza", "wine_still", p5b, r5, "Argentina",
                       subcategory="Malbec", price_tier="mid_range",
                       description="Achaval Ferrer's estate Malbec, sourcing from multiple Luján de Cuyo vineyards, delivers the house's characteristically dense, violet-tinged fruit with supple tannin and impressive freshness. An excellent introduction to the estate's philosophy at an accessible price point.")
if new20:
    PAIR(prod5b2, "Grilled ribeye with chimichurri and roasted sweet peppers", "complement", "classic", "main", "Estate Malbec and ribeye is the quintessential Argentine steakhouse pairing; chimichurri's herb brightness contrasts the wine's dark fruit while roasted peppers add sweetness that softens the tannin.")
    PAIR(prod5b2, "Lamb kofta with harissa yogurt and flatbread", "complement", "established", "main", "The wine's violet florality and dark fruit find an unexpected harmony with Middle Eastern-spiced lamb; harissa's warmth amplifies the wine's own spice while yogurt provides the cool contrast.")
    PAIR(prod5b2, "Smoked provoleta with caramelised onion jam", "complement", "classic", "casual", "A benchmark Argentine pairing at the accessible level: the wine's approachable tannin and dark fruit navigate the cheese's salty caramelised crust; onion jam's sweetness bridges the wine's fruit.")
    PAIR(prod5b2, "Beef and vegetable locro (hearty stew)", "complement", "classic", "main", "Locro's warming spice and rich broth demand the depth of Argentine Malbec; the wine's dark fruit and supple tannin complement the stew's intensity while its acidity keeps the pairing fresh.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
print("B147 complete.")
conn.close()
