#!/usr/bin/env python3
"""B158 — Chinon AOC, Vouvray AOC, Bourgueil AOC,
   Gevrey-Chambertin AOC, Vosne-Romanée AOC — Loire Cabernet Franc and Burgundy Grands Crus"""

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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
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

# ── 1. Chinon AOC ─────────────────────────────────────────────────────────────
print("=== Chinon AOC ===")
r1 = R("Chinon AOC", "France", "wine",
        designation_type="AOC", designation_name="Chinon",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "The Loire Valley's most celebrated red wine appellation, Chinon produces "
            "Cabernet Franc on tufa limestone and gravel soils above the Vienne River. "
            "The wines combine red fruit, violet, and earthy pencil-shaving character "
            "with distinctive Loire freshness and mineral acidity. The best Chinon — "
            "from tuffeau soils — can age for decades and achieves a complexity "
            "rarely matched in Cabernet Franc worldwide."
        ),
        key_producers="Olga Raffault, Charles Joguet, Bernard Baudry, Philippe Alliet",
        historical_context=(
            "Chinon has produced wine since the 12th century; Rabelais, born nearby, "
            "celebrated the wines in his writings. The appellation gained AC status in "
            "1937. Charles Joguet's single-vineyard wines from the 1970s established "
            "Chinon's international reputation."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Chinon year; Cabernet Franc at its finest"),
    (2021, "very_good",  "stable",  "Fresh, elegant wines with classic Loire character"),
    (2020, "excellent",  "stable",  "Rich and structured; excellent aging potential"),
    (2019, "very_good",  "stable",  "Classic Chinon vintage; violet and pencil-shaving"),
    (2018, "very_good",  "stable",  "Warm year; riper style, accessible earlier"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Domaine Bernard Baudry", "winery", r1, "France",
        production_philosophy="terroir_precision",
        philosophy_description="Multiple single-vineyard Chinon; gravel and tuffeau distinction.",
        reputation_narrative="Among Chinon's most consistently celebrated producers; La Croix Boissée is iconic.",
        price_positioning="premium",
        authority_tier=1)
prod1a, new1a = PROD("Baudry Chinon La Croix Boissée", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Old-vine tuffeau Cabernet Franc; earthy, mineral, age-worthy — one of Chinon's greatest.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "roast rack of lamb with Loire herb butter", "complement", "classic", "main",
         "Loire lamb and Cabernet Franc — the classic regional pairing")
    PAIR(prod1a, "rillons de Tours (slow-cooked pork belly)", "complement", "classic", "main",
         "Touraine pork tradition and local red wine")
    PAIR(prod1a, "wild mushroom and lentil tart", "complement", "established", "main",
         "earthy pencil-shaving and mushroom")
    PAIR(prod1a, "aged Sainte-Maure de Touraine goat cheese", "complement", "classic", "cheese",
         "Loire Cabernet Franc and Loire goat cheese — regional harmony")

prod1b, new1b = PROD("Baudry Chinon Les Granges", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Gravel-terroir Chinon; lighter, earlier-drinking with vibrant red fruit character.",
    price_tier="mid_range")
if new1b:
    PAIR(prod1b, "grilled boudin noir with apple compote", "complement", "classic", "main",
         "Touraine blood sausage and local Cabernet Franc")
    PAIR(prod1b, "charcuterie selection with cornichons", "complement", "classic", "amuse",
         "bistro charcuterie and Loire red")
    PAIR(prod1b, "duck rillettes on toast", "complement", "classic", "amuse",
         "classic Loire starter with local wine")
    PAIR(prod1b, "grilled salmon with herb vinaigrette", "complement", "established", "main",
         "salmon and lighter Cabernet Franc")

p1b = P("Philippe Alliet", "winery", r1, "France",
        production_philosophy="old_vine_tuffeau",
        philosophy_description="Old-vine tuffeau Chinon; whole-bunch vinification; minimal intervention.",
        reputation_narrative="Chinon's most profound and sought-after small producer; Vieilles Vignes is legendary.",
        price_positioning="ultra_premium")
prod1c, new1c = PROD("Alliet Chinon Vieilles Vignes", "wine_still", p1c := None or p1b, r1, "France",
    subcategory="red",
    description="Old-vine tuffeau Cabernet Franc; one of France's greatest expressions of the variety.",
    price_tier="ultra_premium")
if new1c:
    PAIR(prod1c, "roast wild duck with black cherries", "complement", "classic", "main",
         "game duck and old-vine Loire Cabernet Franc")
    PAIR(prod1c, "braised lamb shank with olives and herbs", "complement", "classic", "main",
         "rich lamb and structured Cabernet Franc")
    PAIR(prod1c, "wild boar terrine with juniper", "complement", "established", "starter",
         "game and earthy mineral wine")
    PAIR(prod1c, "aged Crottin de Chavignol", "complement", "classic", "cheese",
         "aged goat cheese and old-vine Chinon")

prod1d, new1d = PROD("Alliet Chinon Coteau de Noiré", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Single-site tuffeau Chinon; slightly younger vines than Vieilles Vignes but exceptional.",
    price_tier="premium")
if new1d:
    PAIR(prod1d, "lamb cutlets with violet mustard", "complement", "classic", "main",
         "violet character in wine and violet mustard")
    PAIR(prod1d, "mushroom and chestnuts en croûte", "complement", "established", "main",
         "earthy Cabernet Franc and forest ingredients")
    PAIR(prod1d, "chicken liver parfait with Melba toast", "complement", "established", "starter",
         "iron mineral and liver richness")
    PAIR(prod1d, "aged Époisses cheese", "complement", "suggested", "cheese",
         "structured Loire red and washed-rind cheese")

# ── 2. Vouvray AOC ────────────────────────────────────────────────────────────
print("=== Vouvray AOC ===")
r2 = R("Vouvray AOC", "France", "wine",
        designation_type="AOC", designation_name="Vouvray",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Vouvray produces Chenin Blanc in every style — from bone-dry to honeyed "
            "Moelleux and Liquoreux, as well as traditional-method sparkling. The wines "
            "are made from tuffeau limestone soils east of Tours, producing wines of "
            "extraordinary longevity regardless of sweetness level. Dry Vouvray can "
            "age 30+ years; sweet Moelleux can age a century or more."
        ),
        key_producers="Domaine Huet, François Pinon, Philippe Foreau, Champalou, Marc Brédif",
        historical_context=(
            "Vouvray's tradition of making wine in diverse styles — dry, demi-sec, moelleux, "
            "pétillant, effervescent — reflects the vintage variation of the Loire Valley. "
            "Domaine Huet, led by Noël Pinguet until 2011, set the global standard for "
            "biodynamic Vouvray. The estate is now owned by Anthony Hwang."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding dry and demi-sec Vouvray"),
    (2021, "excellent",  "stable",  "Classic Vouvray; superb freshness and mineral"),
    (2020, "very_good",  "stable",  "Rich, textured; good moelleux potential"),
    (2019, "very_good",  "stable",  "Classic year; well-balanced across all styles"),
    (2018, "excellent",  "rising",  "Very warm; concentrated moelleux and rich dry wines"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Domaine Huet Vouvray", "winery", r2, "France",
        production_philosophy="biodynamic_single_vineyard",
        philosophy_description="Biodynamic; three single-vineyard monopoles: Le Haut-Lieu, Le Mont, Clos du Bourg.",
        reputation_narrative="The world benchmark for Vouvray and biodynamic Chenin Blanc; founded 1928.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Huet Vouvray Le Mont Demi-Sec", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Biodynamic Le Mont Chenin Blanc; demi-sec style with honey, quince, and extraordinary mineral.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "pan-seared foie gras with quince paste", "complement", "classic", "main",
         "quince in wine and foie gras preparation — classic Loire pairing")
    PAIR(prod2a, "roquefort with honey and walnuts", "complement", "classic", "cheese",
         "off-dry Chenin Blanc cuts blue cheese richness")
    PAIR(prod2a, "peach and almond tart", "complement", "classic", "dessert",
         "stone fruit echo to quince-honey wine")
    PAIR(prod2a, "aged Sainte-Maure de Touraine", "complement", "established", "cheese",
         "demi-sec Vouvray and Loire goat cheese")

prod2b, new2b = PROD("Huet Vouvray Clos du Bourg Sec", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Bone-dry Clos du Bourg; austere, mineral, structured — requires 5-10+ years of aging.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "grilled turbot with caper beurre blanc", "complement", "classic", "main",
         "bone-dry Chenin Blanc and flatfish — classic Loire pairing")
    PAIR(prod2b, "veal sweetbreads with lemon and capers", "complement", "established", "main",
         "mineral acidity and rich sweetbreads")
    PAIR(prod2b, "asparagus with sauce Maltaise", "complement", "classic", "starter",
         "Loire spring vegetable and dry Chenin Blanc")
    PAIR(prod2b, "fresh Valençay goat cheese", "complement", "classic", "cheese",
         "dry Vouvray and Loire goat cheese")

p2b = P("Domaine François Pinon", "winery", r2, "France",
        production_philosophy="organic_traditional",
        philosophy_description="Organic Vouvray; traditional methods; silex and tuffeau terroir distinction.",
        reputation_narrative="One of Vouvray's most respected producers; silex terroir specialist.",
        price_positioning="premium")
prod2c, new2c = PROD("Pinon Vouvray Cuvée Silex Blanc", "wine_still", p2b, r2, "France",
    subcategory="white",
    description="Dry Vouvray from silex soils; intense mineral, flint, and green apple — age-worthy.",
    price_tier="premium")
if new2c:
    PAIR(prod2c, "grilled pike-perch with herb butter", "complement", "classic", "main",
         "Loire river fish and Loire white wine")
    PAIR(prod2c, "tarte Tatin with crème fraîche", "contrast", "established", "dessert",
         "dry mineral wine contrasts with caramelized tart")
    PAIR(prod2c, "smoked eel with apple and horseradish", "complement", "established", "starter",
         "silex mineral and smoked fish")
    PAIR(prod2c, "chicken with cream and morel mushrooms", "complement", "established", "main",
         "structured Chenin Blanc and cream-based Loire preparation")

prod2d, new2d = PROD("Pinon Vouvray Moelleux", "wine_still", p2b, r2, "France",
    subcategory="sweet_white",
    description="Moelleux Vouvray; honeyed, apricot, quince with fine acidity — extraordinary aging.",
    price_tier="premium")
if new2d:
    PAIR(prod2d, "blue cheese and walnuts", "complement", "classic", "cheese",
         "honeyed Moelleux cuts through blue cheese")
    PAIR(prod2d, "apple and calvados soufflé", "complement", "established", "dessert",
         "apple and quince echo")
    PAIR(prod2d, "foie gras with Sauternes gelée and brioche", "complement", "classic", "starter",
         "Loire interpretation of the classic foie gras pairing")
    PAIR(prod2d, "apricot tart with almond cream", "complement", "classic", "dessert",
         "apricot echo in wine and tart")

# ── 3. Bourgueil AOC ──────────────────────────────────────────────────────────
print("=== Bourgueil AOC ===")
r3 = R("Bourgueil AOC", "France", "wine",
        designation_type="AOC", designation_name="Bourgueil",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Bourgueil and its satellite Saint-Nicolas-de-Bourgueil produce Cabernet "
            "Franc on the north bank of the Loire, opposite Chinon. The distinctive "
            "tuffeau and gravel terroirs produce wines of red fruit freshness and "
            "herbal character — lighter than Chinon but charming and food-friendly. "
            "The best old-vine tuffeau Bourgueil can rival Chinon in depth and longevity."
        ),
        key_producers="Pierre-Jacques Druet, Domaine de la Chevalerie, Yannick Amirault, Catherine et Pierre Breton",
        historical_context=(
            "Bourgueil received AOC status in 1937. The distinction between sandy gravel "
            "(graviers) and tuffeau soils creates fundamentally different wine styles — "
            "gravel gives lighter, earlier-drinking wines; tuffeau gives structure and "
            "aging potential. Pierre-Jacques Druet pioneered single-terroir bottlings."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Loire Cabernet Franc year"),
    (2021, "very_good",  "stable",  "Fresh and vibrant; classic Bourgueil character"),
    (2020, "excellent",  "stable",  "Structured and age-worthy from tuffeau terroirs"),
    (2019, "very_good",  "stable",  "Classic vintage; violet and fresh herbs"),
    (2018, "very_good",  "stable",  "Warm year; riper fruit, approachable"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Pierre-Jacques Druet", "winery", r3, "France",
        production_philosophy="terroir_old_vine",
        philosophy_description="Pioneer of single-terroir Bourgueil; old-vine tuffeau specialist.",
        reputation_narrative="Among Bourgueil's finest producers; Vaumoreau is the prestige tuffeau cuvée.",
        price_positioning="premium",
        authority_tier=1)
prod3a, new3a = PROD("Druet Bourgueil Vaumoreau", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Prestige tuffeau Bourgueil from Druet; structured, mineral, built for long aging.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "grilled duck breast with violet jus", "complement", "established", "main",
         "violet and Cabernet Franc affinity with duck")
    PAIR(prod3a, "lamb chops with rosemary and garlic", "complement", "classic", "main",
         "Loire lamb and Cabernet Franc tradition")
    PAIR(prod3a, "rabbit with mustard and herbs", "complement", "classic", "main",
         "classic Loire Valley rabbit preparation")
    PAIR(prod3a, "aged goat cheese selection", "complement", "classic", "cheese",
         "Loire Cabernet Franc and aged Loire goat cheese")

prod3b, new3b = PROD("Druet Bourgueil Grand Mont", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Mid-tier tuffeau Bourgueil; elegant, medium-bodied, excellent food-pairing wine.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "steak tartare with Dijon mustard", "complement", "established", "main",
         "fresh Cabernet Franc and raw beef")
    PAIR(prod3b, "rillons de Touraine (braised pork belly)", "complement", "classic", "main",
         "Touraine pork specialty and local wine")
    PAIR(prod3b, "mushroom omelette with fines herbes", "complement", "established", "main",
         "herbal freshness bridge")
    PAIR(prod3b, "Sainte-Maure de Touraine with ash rind", "complement", "classic", "cheese",
         "regional cheese and regional wine")

p3b = P("Yannick Amirault", "winery", r3, "France",
        production_philosophy="biodynamic_terroir",
        philosophy_description="Biodynamic Bourgueil; tuffeau old-vine specialist; La Coudraye is flagship.",
        reputation_narrative="One of Bourgueil's most dynamic producers; biodynamic pioneer in the Loire.",
        price_positioning="premium")
prod3c, new3c = PROD("Amirault Bourgueil La Coudraye", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Flagship biodynamic tuffeau Bourgueil; complex, mineral, long-lived.",
    price_tier="premium")
if new3c:
    PAIR(prod3c, "roast saddle of rabbit with prunes", "complement", "classic", "main",
         "Loire rabbit and Cabernet Franc with fruit")
    PAIR(prod3c, "braised boeuf à la mode", "complement", "established", "main",
         "braised beef and structured Loire red")
    PAIR(prod3c, "lentils with lardon and poached egg", "complement", "classic", "main",
         "classic bistro pairing with structured Loire red")
    PAIR(prod3c, "walnut and goat cheese salad", "complement", "established", "starter",
         "Loire goat cheese and local red")

prod3d, new3d = PROD("Amirault Bourgueil Les Quartiers", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Village Bourgueil from Amirault; fresh, vibrant, early-drinking Cabernet Franc.",
    price_tier="mid_range")
if new3d:
    PAIR(prod3d, "grilled boudin blanc with herbs", "complement", "established", "main",
         "Loire white sausage and Cabernet Franc")
    PAIR(prod3d, "tomato and basil tart", "complement", "established", "main",
         "herbal freshness and summer vegetables")
    PAIR(prod3d, "salmon gravlax with mustard dill sauce", "complement", "established", "starter",
         "lighter Cabernet Franc and cured salmon")
    PAIR(prod3d, "fromage blanc and herbs", "complement", "classic", "cheese",
         "fresh Loire cheese and local wine")

# ── 4. Gevrey-Chambertin AOC ──────────────────────────────────────────────────
print("=== Gevrey-Chambertin AOC ===")
r4 = R("Gevrey-Chambertin AOC", "France", "wine",
        designation_type="AOC", designation_name="Gevrey-Chambertin",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The Côte de Nuits' most productive Grand Cru commune, Gevrey-Chambertin "
            "is home to nine Grand Cru vineyards including Chambertin and Clos de Bèze "
            "— the two most prestigious. The commune's Pinot Noirs are characteristically "
            "structured, dark-fruited, and tannic in youth, requiring decades of aging "
            "to reveal their extraordinary complexity. Napoleon famously drank only "
            "Chambertin."
        ),
        key_producers="Rossignol-Trapet, Armand Rousseau, Denis Mortet, Fourrier, Rossignol",
        historical_context=(
            "Chambertin — 'Field of Bertin' — takes its name from a peasant who planted "
            "vines adjacent to Clos de Bèze in the 12th century. Armand Rousseau, whose "
            "estate was established in 1919, is the benchmark producer across multiple "
            "Grand Cru holdings. Denis Mortet's concentration and modernity transformed "
            "Gevrey's style in the 1990s."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Burgundy year; structure and freshness"),
    (2021, "very_good",  "stable",  "Elegant, fresh wines of great finesse"),
    (2020, "exceptional","rising",  "Greatest Gevrey vintage in decades; profound tannins"),
    (2019, "excellent",  "stable",  "Rich and generous; excellent structure"),
    (2018, "excellent",  "rising",  "Concentrated and powerful; age-worthy"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Domaine Rossignol-Trapet", "winery", r4, "France",
        production_philosophy="biodynamic_grand_cru",
        philosophy_description="Biodynamic; holdings in Chambertin, Latricières, Chapelle; whole-bunch.",
        reputation_narrative="One of Gevrey's most consistent Grand Cru producers; biodynamic pioneer.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Rossignol-Trapet Gevrey-Chambertin Vieilles Vignes", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Old-vine village Gevrey; powerful, structured Pinot Noir showing commune character.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "roast Bresse chicken with Burgundy sauce", "complement", "classic", "main",
         "Burgundy poulet de Bresse and Burgundy Pinot Noir — the regional pairing")
    PAIR(prod4a, "coq au vin with lardons and mushrooms", "complement", "classic", "main",
         "classic Burgundy preparation with Gevrey wine")
    PAIR(prod4a, "wild mushroom and lentil du Puy ragù", "complement", "established", "main",
         "earthy Pinot and earthy mushroom")
    PAIR(prod4a, "Époisses de Bourgogne cheese", "complement", "classic", "cheese",
         "Burgundy's great washed-rind cheese and Burgundy Pinot Noir")

prod4b, new4b = PROD("Rossignol-Trapet Chambertin Grand Cru", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Chambertin Grand Cru from biodynamic vines; profound, structured, generational wine.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "roasted côte de bœuf with bone marrow and Burgundy jus", "complement", "classic", "main",
         "Grand Cru Chambertin and aged French beef")
    PAIR(prod4b, "roast wild duck with cherry and black truffle", "complement", "established", "main",
         "game bird and profound Pinot Noir")
    PAIR(prod4b, "aged Époisses with Burgundy marc", "complement", "classic", "cheese",
         "Burgundy's most powerful cheese with Burgundy's most powerful red")
    PAIR(prod4b, "black truffle and potato gratin", "complement", "established", "main",
         "earthy truffle and structured Pinot Noir")

p4b = P("Domaine Fourrier", "winery", r4, "France",
        production_philosophy="traditional_old_vine",
        philosophy_description="Old-vine Gevrey from multiple premier and grand crus; whole-bunch specialist.",
        reputation_narrative="One of Gevrey's most beloved small producers; Clos Saint-Jacques is benchmark.",
        price_positioning="ultra_premium")
prod4c, new4c = PROD("Fourrier Gevrey-Chambertin Vieilles Vignes", "wine_still", p4b, r4, "France",
    subcategory="red",
    description="Old-vine village Gevrey from Fourrier; powerful, mineral, requiring time to open.",
    price_tier="premium")
if new4c:
    PAIR(prod4c, "braised venison with black pepper and juniper", "complement", "established", "main",
         "game and structured Burgundy Pinot Noir")
    PAIR(prod4c, "duck confit with Puy lentils and bacon", "complement", "classic", "main",
         "Burgundy bistro classic")
    PAIR(prod4c, "grilled Charolais beef with Dijon mustard", "complement", "classic", "main",
         "Burgundy beef and Burgundy red")
    PAIR(prod4c, "aged Cîteaux monastery cheese", "complement", "established", "cheese",
         "Cistercian Burgundy cheese and Gevrey wine")

prod4d, new4d = PROD("Fourrier Gevrey-Chambertin Premier Cru Clos Saint-Jacques", "wine_still", p4b, r4, "France",
    subcategory="red",
    description="Grand Cru quality Premier Cru; often considered Gevrey's finest wine outside Grand Cru.",
    price_tier="ultra_premium")
if new4d:
    PAIR(prod4d, "roast wild boar with game sauce and red cabbage", "complement", "classic", "main",
         "powerful Burgundy Pinot and game")
    PAIR(prod4d, "truffle-stuffed quail with lentils", "complement", "established", "main",
         "luxury game bird and complex Pinot Noir")
    PAIR(prod4d, "aged Comté 24 months with truffle honey", "complement", "established", "cheese",
         "Premier Cru Pinot and aged hard cheese")
    PAIR(prod4d, "pigeon with foie gras and truffles", "complement", "established", "main",
         "luxury preparation and Premier Cru wine")

# ── 5. Vosne-Romanée AOC ──────────────────────────────────────────────────────
print("=== Vosne-Romanée AOC ===")
r5 = R("Vosne-Romanée AOC", "France", "wine",
        designation_type="AOC", designation_name="Vosne-Romanée",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The most revered village in Burgundy, Vosne-Romanée is home to Romanée-"
            "Conti — the world's most expensive wine — as well as La Tâche, Richebourg, "
            "Romanée-Saint-Vivant, and other Grands Crus of almost equal prestige. "
            "The village's Pinot Noirs combine power with extraordinary silky elegance, "
            "red fruit complexity, and a haunting perfume of violet, truffle, and spice "
            "that no other terroir replicates."
        ),
        key_producers="Domaine de la Romanée-Conti, Méo-Camuzet, Lamarche, Gros, Leroy",
        historical_context=(
            "Prince de Conti purchased the La Romanée vineyard in 1760, renaming it "
            "Romanée-Conti. The domaine was reconstituted in 1942 by Aubert de Villaine's "
            "family. In 1946, American wine collector Joseph S. Drouhin purchased Romanée-"
            "Conti and the Domaine de la Romanée-Conti monopole was established. "
            "Aubert de Villaine leads the estate today."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Vosne year; silk and power in perfect balance"),
    (2021, "very_good",  "stable",  "Elegant, precise wines showing Village terroir beautifully"),
    (2020, "exceptional","rising",  "Among the greatest Vosne vintages ever; profound"),
    (2019, "excellent",  "rising",  "Rich, generous, powerful; classic Grand Cru year"),
    (2018, "excellent",  "rising",  "Structured and concentrated; age-worthy"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Domaine Méo-Camuzet", "winery", r5, "France",
        production_philosophy="biodynamic_grand_cru",
        philosophy_description="Biodynamic; holdings in Richebourg, Cros Parantoux, Vosne Premier Crus.",
        reputation_narrative="One of Vosne-Romanée's most celebrated estates; Cros Parantoux is a cult wine.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Méo-Camuzet Vosne-Romanée Premier Cru Cros Parantoux", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Legendary Premier Cru from old vines; silk, red fruit, and spice of extraordinary complexity.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "roasted wood pigeon with truffle jus and lentils", "complement", "classic", "main",
         "silky Vosne Pinot and game bird — classic Burgundy pairing")
    PAIR(prod5a, "roast Bresse chicken supreme with morel cream", "complement", "classic", "main",
         "Burgundy's greatest chicken and finest village wine")
    PAIR(prod5a, "aged Époisses de Bourgogne", "complement", "classic", "cheese",
         "Burgundy's great washed-rind cheese and great Burgundy wine")
    PAIR(prod5a, "truffled soft-boiled egg with toast soldiers", "complement", "established", "starter",
         "truffle and silky red Burgundy — luxury starter")

prod5b, new5b = PROD("Méo-Camuzet Vosne-Romanée Village", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Village Vosne from Méo-Camuzet; generous, silky, showing exceptional commune character.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "coq au vin with mushrooms and pearl onions", "complement", "classic", "main",
         "Burgundy's most famous dish and Burgundy's greatest village")
    PAIR(prod5b, "duck breast with red berry and spice sauce", "complement", "classic", "main",
         "silky Pinot and duck — Burgundy tradition")
    PAIR(prod5b, "wild mushroom risotto with parmesan", "complement", "established", "main",
         "earthy mushroom and silky Vosne Pinot")
    PAIR(prod5b, "Soumaintrain cheese", "complement", "established", "cheese",
         "Burgundy regional cheese and Burgundy wine")

p5b = P("Domaine Lamarche", "winery", r5, "France",
        production_philosophy="traditional_estate",
        philosophy_description="Historic Vosne estate; La Grande Rue Grand Cru is the prestige monopole.",
        reputation_narrative="Monopole holders of La Grande Rue Grand Cru, a narrow strip between DRC grands crus.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Lamarche Vosne-Romanée Les Gaudichots Premier Cru", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Premier Cru adjacent to La Tâche; structured, complex, showing Vosne commune character.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "roast partridge with bread sauce and game chips", "complement", "established", "main",
         "structured Vosne Pinot and game bird")
    PAIR(prod5c, "venison medallions with red fruit and juniper", "complement", "established", "main",
         "game and old-vine Pinot Noir")
    PAIR(prod5c, "warm truffle and potato tart", "complement", "established", "main",
         "earthy truffle and silky Burgundy")
    PAIR(prod5c, "aged Comté 36 months with truffle", "complement", "established", "cheese",
         "structured red and aged hard cheese")

prod5d, new5d = PROD("Lamarche La Grande Rue Grand Cru Vosne-Romanée", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Monopole Grand Cru between La Tâche and Romanée-Conti; extraordinary location and depth.",
    price_tier="ultra_premium")
if new5d:
    PAIR(prod5d, "whole roasted Bresse chicken with black truffle under the skin", "complement", "classic", "main",
         "Burgundy's ultimate luxury preparation with Grand Cru Vosne")
    PAIR(prod5d, "roasted côte de bœuf from Charolais with bone marrow", "complement", "classic", "main",
         "Burgundy beef and Grand Cru Pinot Noir")
    PAIR(prod5d, "braised wild hare à la royale", "complement", "classic", "main",
         "classic French game preparation with Grand Cru Burgundy")
    PAIR(prod5d, "aged Époisses with black truffle", "complement", "classic", "cheese",
         "Burgundy's luxury cheese elevated with truffle")

# ── Final counts ──────────────────────────────────────────────────────────────
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
print("B158 complete.")
cur.close()
conn.close()
