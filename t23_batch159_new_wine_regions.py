#!/usr/bin/env python3
"""B159 — Chambolle-Musigny AOC, Nuits-Saint-Georges AOC, Pommard AOC,
   Meursault AOC, Pouilly-Fuissé AOC — Burgundy village deep dive"""

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

# ── 1. Chambolle-Musigny AOC ──────────────────────────────────────────────────
print("=== Chambolle-Musigny AOC ===")
r1 = R("Chambolle-Musigny AOC", "France", "wine",
        designation_type="AOC", designation_name="Chambolle-Musigny",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Chambolle-Musigny is Burgundy's most feminine and perfumed village, "
            "producing Pinot Noirs of extraordinary floral delicacy from limestone soils "
            "with a high proportion of active chalk. Musigny Grand Cru and Les Amoureuses "
            "Premier Cru are among Burgundy's most coveted wines. The village's Pinots are "
            "characterized by rose petal, red cherry, and sous bois aromatics of "
            "haunting elegance — the opposite of Gevrey's power."
        ),
        key_producers="Jacques-Frédéric Mugnier, Roumier, Ghislaine Barthod, Amiot-Servelle",
        historical_context=(
            "Musigny's reputation dates to medieval times — monks from Cîteaux Abbey "
            "cultivated it from the 12th century. Les Amoureuses ('The Lovers') is "
            "often considered Premier Cru in quality equal to Grand Cru. Mugnier and "
            "Roumier are considered the standard-bearers for the Chambolle style."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Chambolle year; rose petal and silk"),
    (2021, "very_good",  "stable",  "Ethereal, delicate wines of great finesse"),
    (2020, "exceptional","rising",  "Greatest Chambolle in decades; floral and profound"),
    (2019, "excellent",  "stable",  "Rich but retaining Chambolle elegance"),
    (2018, "excellent",  "rising",  "Structured; more weight than typical Chambolle"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Domaine Ghislaine Barthod", "winery", r1, "France",
        production_philosophy="traditional_terroir",
        philosophy_description="Traditional Chambolle; multiple Premier Cru cuvées; feminine, elegant style.",
        reputation_narrative="One of Chambolle's most beloved small estates; all Premier Cru, zero Grand Cru.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Barthod Chambolle-Musigny Village", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Village Chambolle from Barthod; delicate, floral, silk — the essence of the commune.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "roast Bresse chicken with cream and morel mushrooms", "complement", "classic", "main",
         "Burgundy's greatest chicken and most delicate village wine")
    PAIR(prod1a, "pan-seared quail with cherry sauce", "complement", "established", "main",
         "delicate game bird and silky Chambolle Pinot")
    PAIR(prod1a, "wild salmon with pinot noir beurre rouge", "complement", "established", "main",
         "wine used in sauce creates echo; classic preparation")
    PAIR(prod1a, "Soumaintrain cheese", "complement", "classic", "cheese",
         "Burgundy regional washed-rind and delicate village Pinot")

prod1b, new1b = PROD("Barthod Chambolle-Musigny Premier Cru Les Charmes", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Les Charmes Premier Cru; exceptionally silky with violet, red berry, and sous bois.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "roast pigeon with cherry and violet jus", "complement", "classic", "main",
         "violet and rose petal in wine mirror pigeon preparation")
    PAIR(prod1b, "veal medallions with morel cream", "complement", "established", "main",
         "delicate veal and silky Chambolle Premier Cru")
    PAIR(prod1b, "duck breast with cherry and black pepper", "complement", "classic", "main",
         "Chambolle elegance with duck")
    PAIR(prod1b, "aged Brillat-Savarin with truffle", "complement", "established", "cheese",
         "rich cheese and delicate red wine")

p1b = P("Domaine Amiot-Servelle", "winery", r1, "France",
        production_philosophy="traditional_family",
        philosophy_description="Multi-generation Chambolle estate; traditional vinification; Les Amoureuses holding.",
        reputation_narrative="Les Amoureuses is one of Burgundy's most sought-after Premier Crus.",
        price_positioning="ultra_premium")
prod1c, new1c = PROD("Amiot-Servelle Chambolle-Musigny Premier Cru Les Amoureuses", "wine_still", p1c := None or p1b, r1, "France",
    subcategory="red",
    description="Les Amoureuses — Premier Cru quality equal to Grand Cru; floral, silky, extraordinary.",
    price_tier="ultra_premium")
if new1c:
    PAIR(prod1c, "roast Bresse chicken with black truffle under the skin", "complement", "classic", "main",
         "Burgundy's greatest luxury chicken and Chambolle's finest wine")
    PAIR(prod1c, "roasted squab pigeon with Périgueux sauce", "complement", "classic", "main",
         "game bird and profound Chambolle Premier Cru")
    PAIR(prod1c, "venison with violet and raspberry sauce", "complement", "established", "main",
         "game and floral Pinot Noir")
    PAIR(prod1c, "Époisses de Bourgogne at room temperature", "complement", "classic", "cheese",
         "Burgundy's great washed-rind and great Chambolle wine")

prod1d, new1d = PROD("Amiot-Servelle Chambolle-Musigny Village", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Village Chambolle from Amiot-Servelle; elegant and accessible; rose petal and sous bois.",
    price_tier="premium")
if new1d:
    PAIR(prod1d, "grilled salmon with pinot noir sauce", "complement", "established", "main",
         "light Pinot Noir and salmon — Chambolle's delicacy suits this pairing")
    PAIR(prod1d, "mushroom risotto with parmesan", "complement", "established", "main",
         "earthy mushroom and silky Pinot")
    PAIR(prod1d, "chicken liver mousse with toast", "complement", "established", "starter",
         "iron mineral and liver richness")
    PAIR(prod1d, "mild goat cheese with fresh herbs", "complement", "established", "cheese",
         "delicate Pinot and mild cheese")

# ── 2. Nuits-Saint-Georges AOC ────────────────────────────────────────────────
print("=== Nuits-Saint-Georges AOC ===")
r2 = R("Nuits-Saint-Georges AOC", "France", "wine",
        designation_type="AOC", designation_name="Nuits-Saint-Georges",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "The commercial capital of the Côte de Nuits, Nuits-Saint-Georges has "
            "no Grand Crus but exceptional Premier Crus — Les Saint-Georges, Les Vaucrains, "
            "Clos de l'Arlot — that rival Grand Crus in other communes. The wines are "
            "characteristically firm, earthy, and structured in their youth, with flavors "
            "of dark cherry, iron, truffle, and game. They require patience but reward it."
        ),
        key_producers="Henri Gouges, Domaine de l'Arlot, Chevillon, Taupenot-Merme",
        historical_context=(
            "Nuits-Saint-Georges added its premier cru vineyard name (Saint-Georges) "
            "to its name in 1892, one of the first communes to do so. Henri Gouges "
            "was instrumental in establishing estate bottling in the 1920s-30s rather "
            "than selling bulk to négociants, pioneering a movement that transformed Burgundy."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Nuits year; structure and dark fruit"),
    (2021, "very_good",  "stable",  "Elegant, fresh wines showing Premier Cru character"),
    (2020, "exceptional","rising",  "Greatest Nuits vintage in decades; profound"),
    (2019, "excellent",  "stable",  "Rich and firm; built for long aging"),
    (2018, "excellent",  "rising",  "Concentrated and powerful; needs time"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Henri Gouges Domaine", "winery", r2, "France",
        production_philosophy="traditional_pioneer",
        philosophy_description="Estate bottling pioneer since 1920s; multiple Premier Cru holdings.",
        reputation_narrative="The reference estate of Nuits-Saint-Georges; Les Saint-Georges is the benchmark.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Gouges Nuits-Saint-Georges Premier Cru Les Saint-Georges", "wine_still", p2a, r2, "France",
    subcategory="red",
    description="The benchmark Nuits Premier Cru; dark fruit, iron, truffle — structured and age-worthy.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "roast venison with black pepper and game sauce", "complement", "classic", "main",
         "earthy, structured Nuits Pinot and game")
    PAIR(prod2a, "braised wild boar with mushrooms and red wine", "complement", "established", "main",
         "game and iron-mineral Nuits character")
    PAIR(prod2a, "aged Comté 24 months", "complement", "established", "cheese",
         "structured Premier Cru and aged hard cheese")
    PAIR(prod2a, "côte de bœuf from Charolais", "complement", "classic", "main",
         "Burgundy beef and Burgundy Premier Cru")

prod2b, new2b = PROD("Gouges Nuits-Saint-Georges Village", "wine_still", p2a, r2, "France",
    subcategory="red",
    description="Village Nuits from Gouges; firm, dark-fruited, showing commune's earthy character.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "duck confit with Puy lentils and smoked lardons", "complement", "classic", "main",
         "Burgundy bistro classic with structured village Pinot")
    PAIR(prod2b, "beef bourguignon with pearl onions", "complement", "classic", "main",
         "Burgundy's signature dish with Burgundy wine")
    PAIR(prod2b, "grilled Charolais steak with Dijon mustard sauce", "complement", "classic", "main",
         "Burgundy beef preparation")
    PAIR(prod2b, "camembert with walnut bread", "complement", "established", "cheese",
         "structured red and soft-ripened cheese")

p2b = P("Domaine de l'Arlot", "winery", r2, "France",
        production_philosophy="biodynamic_monopole",
        philosophy_description="Biodynamic; monopoles Clos de l'Arlot and Clos des Forêts; precise extraction.",
        reputation_narrative="One of Nuits's most refined producers; Clos de l'Arlot is an elegant monopole.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("Domaine de l'Arlot Nuits-Saint-Georges Premier Cru Clos de l'Arlot", "wine_still", p2b, r2, "France",
    subcategory="red",
    description="Monopole Premier Cru; elegantly structured Nuits with red fruit and mineral precision.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "roast partridge with game sauce and chicory", "complement", "established", "main",
         "game bird and structured Nuits Premier Cru")
    PAIR(prod2c, "truffle-stuffed chicken with black truffle jus", "complement", "established", "main",
         "earthy truffle and mineral Pinot Noir")
    PAIR(prod2c, "aged Mimolette cheese", "complement", "established", "cheese",
         "firm Nuits tannin and aged Dutch-style cheese")
    PAIR(prod2c, "wild mushroom and chestnut soup", "complement", "established", "starter",
         "earthy forest notes bridge to wine")

prod2d, new2d = PROD("Domaine de l'Arlot Nuits-Saint-Georges Premier Cru Clos des Forêts", "wine_still", p2b, r2, "France",
    subcategory="red",
    description="Second Arlot monopole; more structured and age-worthy; darker fruit expression.",
    price_tier="ultra_premium")
if new2d:
    PAIR(prod2d, "roast wild duck with cherry and smoked lardons", "complement", "established", "main",
         "game bird and Nuits Premier Cru")
    PAIR(prod2d, "grilled rib steak with bone marrow", "complement", "classic", "main",
         "Burgundy beef and firm Nuits Pinot")
    PAIR(prod2d, "venison tartare with juniper and herbs", "complement", "established", "starter",
         "game and earthy iron mineral")
    PAIR(prod2d, "aged Cîteaux monastery cheese", "complement", "established", "cheese",
         "Cistercian Burgundy cheese and firm Nuits Premier Cru")

# ── 3. Pommard AOC ────────────────────────────────────────────────────────────
print("=== Pommard AOC ===")
r3 = R("Pommard AOC", "France", "wine",
        designation_type="AOC", designation_name="Pommard",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "Pommard is the Côte de Beaune's most famous red wine village, producing "
            "Pinot Noirs of robust structure, dark fruit, and rustic earthiness — quite "
            "different from the delicacy of Chambolle or the elegance of Volnay just "
            "to the south. The iron-rich clay soils of the Premier Crus Rugiens and "
            "Epenots produce the commune's finest wines, built for long aging."
        ),
        key_producers="Domaine de Courcel, Comte Armand, Jaffelin, Du Pavillon, Mugnier",
        historical_context=(
            "Pommard was historically one of Burgundy's most commercially successful "
            "wines — its bold, robust style appealed to the British and American markets "
            "in the 19th and early 20th centuries. The name was frequently used for "
            "fraudulent imitations, leading to stricter appellation controls."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Pommard year; structure and dark fruit"),
    (2021, "very_good",  "stable",  "Fresh, elegant for Pommard; more accessible"),
    (2020, "exceptional","rising",  "Greatest Pommard in decades; profound structure"),
    (2019, "excellent",  "stable",  "Rich and muscular; classic Pommard style"),
    (2018, "excellent",  "rising",  "Dense and concentrated; needs long aging"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine Comte Armand", "winery", r3, "France",
        production_philosophy="single_vineyard_monopole",
        philosophy_description="Monopole of Clos des Epeneaux Premier Cru; traditional vinification.",
        reputation_narrative="Benchmark Pommard producer; Clos des Epeneaux is the commune's finest wine.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Comte Armand Pommard Premier Cru Clos des Epeneaux", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Monopole Premier Cru Clos des Epeneaux; powerful, structured, dark-fruited Pommard.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "roasted leg of Limousin lamb with thyme jus", "complement", "classic", "main",
         "muscular Pommard and robust lamb preparation")
    PAIR(prod3a, "braised venison with black truffle and lardons", "complement", "established", "main",
         "game and dark-fruited structured Burgundy")
    PAIR(prod3a, "côte de bœuf Charolais with bone marrow", "complement", "classic", "main",
         "Burgundy beef and robust Pommard Premier Cru")
    PAIR(prod3a, "aged Époisses de Bourgogne", "complement", "classic", "cheese",
         "powerful washed-rind and powerful red wine")

prod3b, new3b = PROD("Comte Armand Auxey-Duresses Rouge", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Village red from neighbouring Auxey-Duresses; robust, earthy, excellent value.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "beef stew with mushrooms and herbs", "complement", "established", "main",
         "earthy Burgundy red and braised beef")
    PAIR(prod3b, "grilled duck with cherry compote", "complement", "established", "main",
         "dark fruit and duck richness")
    PAIR(prod3b, "lentil soup with smoked ham hock", "complement", "established", "main",
         "rustic earthiness and robust wine")
    PAIR(prod3b, "aged Comté with bread and butter", "complement", "established", "cheese",
         "earthy red and aged French cheese")

p3b = P("Domaine de Courcel", "winery", r3, "France",
        production_philosophy="traditional_estate",
        philosophy_description="Multi-century Pommard estate; Grands Epenots and Rugiens are the top wines.",
        reputation_narrative="One of Pommard's oldest estates; Grand Clos des Epenots is the flagship.",
        price_positioning="ultra_premium")
prod3c, new3c = PROD("Courcel Pommard Premier Cru Grands Epenots", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Grand Epenots Premier Cru from de Courcel; dark, structured, age-worthy Pommard.",
    price_tier="ultra_premium")
if new3c:
    PAIR(prod3c, "slow-roasted Limousin beef with sauce au poivre", "complement", "classic", "main",
         "robust Pommard and pepper-sauced beef")
    PAIR(prod3c, "wild boar charcuterie with mustard", "complement", "established", "starter",
         "game and earthy dark-fruited wine")
    PAIR(prod3c, "duck magret with green pepper sauce", "complement", "established", "main",
         "dark fruit and peppery sauce bridge")
    PAIR(prod3c, "aged Comté 36 months with truffle honey", "complement", "established", "cheese",
         "intense mineral red and aged mountain cheese")

prod3d, new3d = PROD("Courcel Pommard Village", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Village Pommard from de Courcel; showing robust, earthy commune character.",
    price_tier="premium")
if new3d:
    PAIR(prod3d, "beef bourguignon with lardons and mushrooms", "complement", "classic", "main",
         "Burgundy's signature preparation and robust Pommard")
    PAIR(prod3d, "braised oxtail with root vegetables", "complement", "established", "main",
         "earthy richness and robust Pinot Noir")
    PAIR(prod3d, "grilled rib-eye with Dijon mustard", "complement", "classic", "main",
         "Pommard and Burgundy beef tradition")
    PAIR(prod3d, "Saint-Nectaire cheese", "complement", "established", "cheese",
         "semi-soft French cheese and earthy Pommard")

# ── 4. Meursault AOC ──────────────────────────────────────────────────────────
print("=== Meursault AOC ===")
r4 = R("Meursault AOC", "France", "wine",
        designation_type="AOC", designation_name="Meursault",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Meursault is Burgundy's greatest white wine village, producing Chardonnay "
            "of extraordinary richness and complexity from limestone soils. The wines "
            "combine hazelnut, butter, and cream with mineral freshness in a style that "
            "defines barrel-fermented Chardonnay globally. The Premier Crus Perrières, "
            "Genevrières, and Charmes are among the world's finest white wines and can "
            "age for two decades or more."
        ),
        key_producers="Coche-Dury, Roulot, Lafon, Pierre Morey, Boillot",
        historical_context=(
            "Meursault's fame dates to the 13th century when Cistercian monks cultivated "
            "the hillside vineyards. The La Paulée de Meursault — a legendary annual wine "
            "feast where growers bring their best bottles — has been held since 1932. "
            "Jean-François Coche-Dury's tiny production created a cult following and "
            "extraordinary secondary market prices."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Meursault year; richness with freshness"),
    (2021, "very_good",  "stable",  "Fresh, mineral Meursault; outstanding acidity"),
    (2020, "exceptional","rising",  "Greatest Meursault vintage in decades; profound"),
    (2019, "excellent",  "stable",  "Rich and generous; excellent aging potential"),
    (2018, "excellent",  "rising",  "Opulent and concentrated; needs aging"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Domaine Roulot", "winery", r4, "France",
        production_philosophy="traditional_precision",
        philosophy_description="Burgundy's most precise white wine producer; old-vine single-vineyard whites.",
        reputation_narrative="The Coche-Dury of accessibility; benchmark for traditional Meursault style.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Roulot Meursault Premier Cru Charmes", "wine_still", p4a, r4, "France",
    subcategory="white",
    description="Premier Cru Charmes from Roulot; richly textured, hazelnut, cream, and mineral precision.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "roast Bresse chicken with cream and morel sauce", "complement", "classic", "main",
         "richly textured Meursault and Burgundy cream preparations")
    PAIR(prod4a, "grilled turbot with beurre noisette", "complement", "classic", "main",
         "hazelnut butter in wine and sauce — perfect echo")
    PAIR(prod4a, "veal sweetbreads with hazelnut butter", "complement", "classic", "main",
         "hazelnut and cream in wine mirror preparation")
    PAIR(prod4a, "scallops with cauliflower purée and truffle", "complement", "classic", "main",
         "Premier Cru richness and luxury shellfish")

prod4b, new4b = PROD("Roulot Meursault Village", "wine_still", p4a, r4, "France",
    subcategory="white",
    description="Village Meursault from Roulot; genuine Premier Cru quality at village level; sought-after.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "grilled sole with caper butter", "complement", "classic", "main",
         "minerality and cream echo flatfish")
    PAIR(prod4b, "lobster bisque with cream and cognac", "complement", "established", "main",
         "rich texture and mineral acidity")
    PAIR(prod4b, "chicken with cream and mushrooms à la crème", "complement", "classic", "main",
         "Burgundy cream preparation and Meursault")
    PAIR(prod4b, "aged Comté with walnut bread", "complement", "established", "cheese",
         "rich textured white and nutty aged cheese")

p4b = P("Domaine Comte Lafon", "winery", r4, "France",
        production_philosophy="biodynamic_old_vine",
        philosophy_description="Biodynamic; multi-Premier Cru holdings including Perrières; old-vine precision.",
        reputation_narrative="One of Meursault's most prestigious estates; Perrières is world-class.",
        price_positioning="ultra_premium")
prod4c, new4c = PROD("Lafon Meursault Premier Cru Perrières", "wine_still", p4b, r4, "France",
    subcategory="white",
    description="Perrières Premier Cru from Lafon; the most mineral and age-worthy Meursault Premier Cru.",
    price_tier="ultra_premium")
if new4c:
    PAIR(prod4c, "grilled langoustine with lemon beurre blanc", "complement", "classic", "main",
         "mineral Perrières and delicate crustacean")
    PAIR(prod4c, "Dover sole meunière with lemon and parsley", "complement", "classic", "main",
         "the classic French flatfish preparation with Burgundy white")
    PAIR(prod4c, "white asparagus with hollandaise", "complement", "classic", "starter",
         "mineral Premier Cru and white asparagus")
    PAIR(prod4c, "aged Gruyère and walnut", "complement", "established", "cheese",
         "mineral and hazelnut bridge to aged Swiss-style cheese")

prod4d, new4d = PROD("Lafon Meursault Clos de la Barre", "wine_still", p4b, r4, "France",
    subcategory="white",
    description="Village-level Meursault monopole from Lafon; Premier Cru quality at village designation.",
    price_tier="ultra_premium")
if new4d:
    PAIR(prod4d, "roasted scallops with lemon beurre blanc", "complement", "classic", "main",
         "mineral white Burgundy and scallop")
    PAIR(prod4d, "poached salmon with cream sauce", "complement", "established", "main",
         "rich cream texture and salmon")
    PAIR(prod4d, "veal chop with morel cream", "complement", "classic", "main",
         "Burgundy cream preparation and white Burgundy")
    PAIR(prod4d, "Brillat-Savarin triple cream cheese", "complement", "established", "cheese",
         "rich textured white and triple cream")

# ── 5. Pouilly-Fuissé AOC ─────────────────────────────────────────────────────
print("=== Pouilly-Fuissé AOC ===")
r5 = R("Pouilly-Fuissé AOC", "France", "wine",
        designation_type="AOC", designation_name="Pouilly-Fuissé",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description=(
            "The Mâconnais region's finest appellation, Pouilly-Fuissé produces Chardonnay "
            "from dramatic limestone and clay hillsides below the Rock of Solutré. The "
            "wines are richer and more textured than basic Mâcon but have lighter oak and "
            "more freshness than Meursault. First Premier Crus were designated in 2020, "
            "recognizing sites like En France, Les Quarts, and Les Perrières."
        ),
        key_producers="Château Fuissé, Domaine Guffens-Heynen, Robert-Denogent, Domaine Ferret",
        historical_context=(
            "Pouilly-Fuissé received AOC status in 1936 and was historically overpriced "
            "relative to quality until a quality revolution in the 1990s-2000s. The "
            "first Premier Cru classification (2020) gave the appellation a quality "
            "framework it had long needed. Guffens-Heynen's Clos des Petits Croux "
            "established what the region could achieve at the highest level."
        ))

for yr, qd, pt, sn in [
    (2023, "excellent",  "rising",  "Outstanding Mâconnais vintage; freshness and richness"),
    (2022, "very_good",  "stable",  "Classic Pouilly-Fuissé character; textured and mineral"),
    (2021, "excellent",  "stable",  "Superb freshness from cool conditions; bright acidity"),
    (2020, "very_good",  "stable",  "Rich and ripe; Premier Cru launch vintage"),
    (2019, "very_good",  "stable",  "Consistent; accessible and food-friendly"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Château Fuissé", "winery", r5, "France",
        production_philosophy="traditional_estate",
        philosophy_description="Historic Pouilly-Fuissé estate; Vieilles Vignes is the benchmark cuvée.",
        reputation_narrative="Pouilly-Fuissé's most famous estate; Vieilles Vignes set regional standards.",
        price_positioning="premium",
        authority_tier=1)
prod5a, new5a = PROD("Château Fuissé Pouilly-Fuissé Vieilles Vignes", "wine_still", p5a, r5, "France",
    subcategory="white",
    description="Old-vine Pouilly-Fuissé; benchmark for the appellation; rich, textured, mineral.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "grilled turbot with beurre blanc", "complement", "classic", "main",
         "textured Mâconnais Chardonnay and flatfish")
    PAIR(prod5a, "roast Burgundy chicken with cream sauce", "complement", "established", "main",
         "rich Chardonnay and chicken in cream")
    PAIR(prod5a, "scallops with leek fondue and cream", "complement", "established", "main",
         "rich texture and delicate shellfish")
    PAIR(prod5a, "gruyère and mushroom tart", "complement", "established", "main",
         "mineral Chardonnay and nutty cheese tart")

prod5b, new5b = PROD("Château Fuissé Pouilly-Fuissé Premier Cru Le Clos", "wine_still", p5a, r5, "France",
    subcategory="white",
    description="Monopole Premier Cru Le Clos; the estate's finest wine; mineral, complex, age-worthy.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "grilled lobster with herb butter", "complement", "established", "main",
         "Premier Cru richness and luxury lobster")
    PAIR(prod5b, "poached turbot in Champagne sauce", "complement", "classic", "main",
         "elegant preparation for elegant wine")
    PAIR(prod5b, "white truffle risotto", "complement", "established", "main",
         "mineral and earthy truffle bridge")
    PAIR(prod5b, "Comté with truffle honey", "complement", "established", "cheese",
         "mineral Chardonnay and aged mountain cheese")

p5b = P("Domaine Guffens-Heynen", "winery", r5, "France",
        production_philosophy="low_yield_precision",
        philosophy_description="Ultra-low yields; barrel-fermented; obsessive terroir precision.",
        reputation_narrative="Considered by many to make Pouilly-Fuissé's greatest wines; Belgian-born perfectionist.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Guffens-Heynen Pouilly-Fuissé Clos des Petits Croux", "wine_still", p5b, r5, "France",
    subcategory="white",
    description="Benchmark single-site Pouilly-Fuissé; extraordinary mineral intensity and aging potential.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "Bresse chicken with Comté and morel", "complement", "classic", "main",
         "Burgundy's greatest chicken and mineral Chardonnay")
    PAIR(prod5c, "roasted langoustine with bisque cream", "complement", "established", "main",
         "mineral precision and crustacean richness")
    PAIR(prod5c, "sea bass with beurre blanc", "complement", "classic", "main",
         "mineral Chardonnay and white fish")
    PAIR(prod5c, "aged Comté 18-24 months", "complement", "established", "cheese",
         "mineral Mâconnais and mountain cheese")

prod5d, new5d = PROD("Guffens-Heynen Pouilly-Fuissé Premier Cru En France", "wine_still", p5b, r5, "France",
    subcategory="white",
    description="Premier Cru En France from Guffens; concentrated, structured, long aging.",
    price_tier="ultra_premium")
if new5d:
    PAIR(prod5d, "grilled Dover sole with lemon and parsley", "complement", "classic", "main",
         "classic flatfish preparation and mineral Chardonnay")
    PAIR(prod5d, "coquilles Saint-Jacques with sauce cardinal", "complement", "classic", "main",
         "classic French scallop preparation")
    PAIR(prod5d, "veal sweetbreads with cream and mushrooms", "complement", "established", "main",
         "rich cream and mineral Mâconnais")
    PAIR(prod5d, "burrata with truffled olive oil", "complement", "established", "starter",
         "rich mineral and creamy starter")

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
print("B159 complete.")
cur.close()
conn.close()
