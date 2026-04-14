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
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B126 ─────────────────────────────────────────────────────────────────────
# Targets: Madiran AOC (France), Bergerac AOC (France),
#          Kakheti (Georgia), Tokaj (Hungary), Villány (Hungary)

# 1. MADIRAN AOC — France
print("=== Madiran AOC ===")
r1 = R("Madiran AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Madiran AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The most powerful red wine of Southwest France, from the Vic-Bilh hills near Tarbes in the Hautes-Pyrénées. Almost exclusively Tannat grape — one of the world's most tannic varieties — sometimes softened with Cabernet Franc and Cabernet Sauvignon. Producers like Brumont and Laplace have demonstrated that Tannat produces extraordinary wines when tamed by extended ageing and micro-oxygenation. Recent scientific interest in Tannat's resveratrol content (highest of any grape) has generated new attention.",
        key_producers="Alain Brumont, Vignobles Laplace, Château Barréjat, Domaine Berthoumieu",
        historical_context="Madiran wine was documented in the 11th century as sustaining pilgrims on the Camino de Santiago. Tannat was almost abandoned in the 1950s before Alain Brumont's Château Montus demonstrated its grandeur. Uruguay became a major Tannat country after Basque emigrants brought the grape in the 19th century.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r1, yr, qd, pt, f"Madiran {yr}: Vic-Bilh clay hills; powerful Tannat of extraordinary structure and ageing potential")

p1a = P("Alain Brumont", "winery", r1, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The master of Tannat; Château Montus and Château Bouscassé are the world reference for Madiran's potential.",
        reputation_narrative="Alain Brumont transformed Madiran from peasant wine to internationally acclaimed luxury; Montus Vieilles Vignes is France's finest Tannat.",
        price_positioning="ultra_premium")
pr1a1, n = PROD("Château Montus Madiran Vieilles Vignes", "wine_still", p1a, r1, "France",
                subcategory="Tannat", price_tier="ultra_premium",
                description="Old-vine Tannat from Montus; extraordinary concentration of black fruit, graphite, violets and tannins that demand 10-20 years of ageing.")
if n:
    PAIR(pr1a1, "Daube de boeuf Gasconne with prunes", "complement", "classic", "main", "Madiran Tannat and long-braised Gascon beef with Agen prunes is legendary")
    PAIR(pr1a1, "Cassoulet de Castelnaudary", "complement", "classic", "main", "The great Southwest pairing: powerful Tannat with the ultimate slow-braised bean dish")
    PAIR(pr1a1, "Wild boar chop with bitter chocolate sauce", "complement", "established", "main", "Tannat's power and graphite mirrors the depth of wild boar with dark chocolate")
    PAIR(pr1a1, "Aged Ossau-Iraty (Basque sheep's cheese)", "complement", "established", "cheese", "The Basque cheese pairing: powerful Tannat and mountain sheep's milk cheese")

pr1a2, n = PROD("Château Montus Madiran Prestige", "wine_still", p1a, r1, "France",
                subcategory="Tannat", price_tier="premium",
                description="Classic Montus Madiran; dark plum, leather, iron and structured Tannat tannins — accessible earlier than Vieilles Vignes.")
if n:
    PAIR(pr1a2, "Confit de canard (duck leg confit)", "complement", "classic", "main", "Duck confit and Madiran are the great pairing of the Gascony table")
    PAIR(pr1a2, "Entrecôte à la Bordelaise with bone marrow", "complement", "established", "main", "Rich grilled rib and powerful Tannat; the Gascony steakhouse tradition")
    PAIR(pr1a2, "Magret de canard with pepper sauce", "complement", "classic", "main", "Duck breast and Madiran is the classic expression of Southwest French cuisine")
    PAIR(pr1a2, "Axoa d'espalette (Basque veal pepper stew)", "complement", "classic", "main", "The Basque-Gascon boundary dish finds its perfect Madiran companion")

p1b = P("Vignobles Laplace", "winery", r1, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Family estate since 1850; Château d'Aydie is the leading Laplace cuvée; authentic Madiran from clay-limestone terraces.",
        reputation_narrative="The Laplace family has farmed Madiran for six generations; Château d'Aydie Tannat is one of the appellation's most consistent references.",
        price_positioning="premium")
pr1b1, n = PROD("Château d'Aydie Madiran", "wine_still", p1b, r1, "France",
                subcategory="Tannat", price_tier="premium",
                description="Classic Aydie Tannat; structured dark fruit, iron mineral and the firm tannins of this great appellation; excellent with 10+ years.")
if n:
    PAIR(pr1b1, "Slow-roasted pork shoulder with garlic and herbs", "complement", "established", "main", "Tannat's firm tannins find balance alongside slow-roasted pork fat and herbs")
    PAIR(pr1b1, "Pigeon rôti with lentils du Puy", "complement", "established", "main", "Dark Madiran complements pigeon's gaminess with firm structure and fruit")
    PAIR(pr1b1, "Foie gras entier de canard", "contrast", "established", "main", "Bold Tannat provides a powerful contrast to fatty foie gras richness")
    PAIR(pr1b1, "Grilled lamb with Piment d'Espelette", "complement", "classic", "main", "Basque spiced lamb and Madiran Tannat; the great Pyrenean food-wine combination")

pr1b2, n = PROD("Vignobles Laplace Pacherenc du Vic-Bilh Sec", "wine_still", p1b, r1, "France",
                subcategory="Arrufiac-Courbu-Manseng", price_tier="mid_range",
                description="Dry Pacherenc from Laplace; the lesser-known white of the Madiran region — fresh apple, citrus and mineral from indigenous Pyrénéan varieties.")
if n:
    PAIR(pr1b2, "Grilled trout with hazelnut butter", "complement", "established", "main", "Fresh dry Pacherenc is the local companion for freshwater Pyrénéan trout")
    PAIR(pr1b2, "Oysters with Basque black pepper mignonette", "complement", "established", "starter", "Citrus-mineral white lifts oysters with fresh mineral precision")
    PAIR(pr1b2, "Salade de gésiers de canard (duck gizzard salad)", "complement", "classic", "starter", "The Southwest starter salad meets its natural regional white wine companion")
    PAIR(pr1b2, "Asperges vertes à la sauce gribiche", "complement", "established", "main", "Fresh indigenous white suits green asparagus with egg-herb gribiche sauce")

# 2. BERGERAC AOC — France
print("=== Bergerac AOC ===")
r2 = R("Bergerac AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Bergerac AOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="A large and diverse appellation east of Bordeaux in the Dordogne valley, using identical Bordeaux varieties (Merlot, Cabernet Franc, Cabernet Sauvignon, Sauvignon Blanc, Sémillon). The parent appellation covers still reds, whites and rosés; sub-appellations include Pécharmant (finest reds), Monbazillac (sweet whites), Saussignac and Montravel. Bergerac wines offer Bordeaux variety at often dramatically lower prices; several top producers make wines of genuine quality.",
        key_producers="Château Tour des Gendres, Clos d'Yvigne, Château La Jaubertie, Domaine de l'Ancienne Cure",
        historical_context="Bergerac and Bordeaux have been rivals for centuries, with Bordeaux merchants historically blocking Bergerac wines from the sea trade route. The region's wines were praised by Cyrano de Bergerac (the real Cyrano, not Rostand's hero, who was born nearby). Dordogne tourism has revived the appellation.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","stable"),(2021,"very_good","stable"),(2022,"excellent","rising")]:
    VIN(r2, yr, qd, pt, f"Bergerac {yr}: Dordogne valley; Bordeaux varieties showing fresh, fruit-driven character at accessible prices")

p2a = P("Château Tour des Gendres", "winery", r2, "France",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Bergerac leader; La Gloire de Mon Père and Anthologia are benchmark Bergerac reds of real ambition.",
        reputation_narrative="Luc de Conti's estate is Bergerac's most quality-conscious; his biodynamic approach and old-vine selection produce wines rivalling fine Bordeaux.",
        price_positioning="premium")
pr2a1, n = PROD("Château Tour des Gendres La Gloire de Mon Père", "wine_still", p2a, r2, "France",
                subcategory="Merlot-Cabernet Franc", price_tier="premium",
                description="Flagship biodynamic Bergerac red; Merlot-led with ripe plum, cedar and a refined mineral structure — a serious Dordogne statement.")
if n:
    PAIR(pr2a1, "Magret de canard sauce aux cerises", "complement", "classic", "main", "Duck breast with cherry is the great Périgord tradition with Bergerac red")
    PAIR(pr2a1, "Sarlat-style potatoes with duck fat and garlic", "complement", "established", "main", "The classic Périgord potato and duck fat side finds its Bergerac companion")
    PAIR(pr2a1, "Grilled lamb with Périgord walnut pesto", "complement", "established", "main", "Refined Merlot and local lamb with walnut; the Dordogne table at its best")
    PAIR(pr2a1, "Truffle-stuffed roast chicken", "complement", "established", "main", "The Périgord luxury: local truffle chicken with the region's finest red wine")

pr2a2, n = PROD("Château Tour des Gendres Bergerac Blanc", "wine_still", p2a, r2, "France",
                subcategory="Sauvignon Blanc-Sémillon", price_tier="mid_range",
                description="Biodynamic Bergerac blanc; Sauvignon and Sémillon with citrus, white currant and a chalky mineral freshness — textbook Dordogne white.")
if n:
    PAIR(pr2a2, "Walnut and Roquefort salad with honey", "complement", "established", "starter", "The Périgord salad tradition: white wine with walnut, blue cheese and sweet contrast")
    PAIR(pr2a2, "Grilled sole with capers and lemon butter", "complement", "established", "main", "Classic Dordogne white and simple grilled sole is always satisfying")
    PAIR(pr2a2, "Foie gras poêlé with grapes and verjuice", "complement", "classic", "main", "Bergerac white with fried foie gras is the everyday Périgord luxury pairing")
    PAIR(pr2a2, "Oysters gratin with leeks", "complement", "established", "starter", "Sauvignon mineral and baked oyster-leek is an elegant bistro combination")

p2b = P("Château l'Ancienne Cure", "winery", r2, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Leading Bergerac and Monbazillac estate; L'Extase Monbazillac sweet wine is the appellation's most celebrated bottle.",
        reputation_narrative="Christian Roche's estate produces consistently excellent Bergerac red and the extraordinary Monbazillac sweet wine L'Extase from botrytised Sémillon.",
        price_positioning="mid_range")
pr2b1, n = PROD("Château l'Ancienne Cure L'Extase Monbazillac", "wine_dessert", p2b, r2, "France",
                subcategory="Sémillon-Sauvignon Blanc", price_tier="premium",
                description="L'Extase Monbazillac; botrytised Sémillon and Sauvignon with orange marmalade, honey and beeswax — the great Dordogne sweet wine.")
if n:
    PAIR(pr2b1, "Foie gras de canard au torchon", "complement", "classic", "starter", "Monbazillac and foie gras is the great Périgord tradition — parallel to Sauternes")
    PAIR(pr2b1, "Roquefort cheese with walnut bread", "contrast", "classic", "cheese", "Botrytised sweetness of Monbazillac contrasts powerfully with salty Roquefort")
    PAIR(pr2b1, "Crème brûlée with vanilla", "complement", "established", "dessert", "Beeswax-honey Monbazillac mirrors and elevates a classic vanilla crème brûlée")
    PAIR(pr2b1, "Tarte aux noix (walnut tart)", "complement", "established", "dessert", "Dordogne walnut tart with Périgord's great sweet wine; a regional celebration")

pr2b2, n = PROD("Château l'Ancienne Cure Bergerac Rouge Cuvée Abbaye", "wine_still", p2b, r2, "France",
                subcategory="Merlot-Cabernet Franc-Cabernet Sauvignon", price_tier="mid_range",
                description="Cuvée Abbaye Bergerac red; classic Bordeaux blend with ripe cherry, subtle oak and a gentle mineral freshness from Dordogne soils.")
if n:
    PAIR(pr2b2, "Grilled entrecôte with Béarnaise sauce", "complement", "established", "main", "Classic rib steak with Béarnaise finds a natural companion in accessible Bergerac red")
    PAIR(pr2b2, "Cassoulet with duck and sausage", "complement", "established", "main", "Hearty Southwest cassoulet and mid-range Bergerac; a satisfying regional match")
    PAIR(pr2b2, "Burger with Périgord truffle shavings", "complement", "suggested", "casual", "Indulgent truffle-elevated burger meets an affordable Dordogne Merlot blend")
    PAIR(pr2b2, "Lamb shepherd's pie with root vegetables", "complement", "established", "main", "Approachable Bordeaux-style red complements the comfort of shepherd's pie")

# 3. KAKHETI — Georgia
print("=== Kakheti ===")
r3 = R("Kakheti", "Georgia", "wine",
        designation_type="PDO",
        designation_name="Kakheti",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The primary wine region of Georgia, in the fertile Alazani valley at the foot of the Greater Caucasus mountains east of Tbilisi. Home to over 500 indigenous grape varieties and the world's oldest wine culture (8,000-year-old evidence of winemaking in clay qvevri). The distinctive Kakhetian winemaking method involves extended skin maceration of whites in qvevri (buried terracotta amphora) producing rich, tannic, amber-coloured whites. Rkatsiteli, Saperavi and Mtsvane are the key varieties.",
        key_producers="Pheasant's Tears, Teliani Valley, Château Mukhrani, Schuchmann, Iago's Wine",
        historical_context="Georgia is widely recognised as the birthplace of wine, with archaeological evidence dating to 6000 BCE. The qvevri winemaking method is UNESCO Intangible Cultural Heritage. Soviet collectivisation almost destroyed traditional winemaking; the natural wine renaissance from the 2000s returned producers to indigenous methods. Kakheti produces 70% of Georgia's wine.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"exceptional","rising"),(2022,"excellent","rising")]:
    VIN(r3, yr, qd, pt, f"Kakheti {yr}: Alazani valley harvest; qvevri winemaking produces amber whites and powerful Saperavi reds")

p3a = P("Pheasant's Tears", "winery", r3, "Georgia",
        production_philosophy="natural",
        philosophy_description="John Wurdeman and Gela Patalishvili's natural qvevri winery; benchmark amber Rkatsiteli and Saperavi from Kakheti tradition.",
        reputation_narrative="Pheasant's Tears is the world's most celebrated Georgian wine producer; their amber wines introduced global audiences to qvevri winemaking.",
        price_positioning="premium")
pr3a1, n = PROD("Pheasant's Tears Rkatsiteli Kakheti", "wine_still", p3a, r3, "Georgia",
                subcategory="Rkatsiteli", price_tier="premium",
                description="Qvevri-fermented Rkatsiteli; 6 months on skins producing an amber wine of extraordinary tannic structure, walnut, quince and dried apricot.")
if n:
    PAIR(pr3a1, "Lamb chakapuli (with tarragon and tkemali)", "complement", "classic", "main", "The definitive Georgian pairing: amber Rkatsiteli with the spring lamb stew")
    PAIR(pr3a1, "Grilled chicken satsivi (walnut sauce)", "complement", "classic", "main", "Walnut-tannic amber wine mirrors the walnut cream sauce of satsivi chicken")
    PAIR(pr3a1, "Khinkali (Georgian soup dumplings)", "complement", "classic", "main", "Amber Rkatsiteli and khinkali is the standard Georgian restaurant table combination")
    PAIR(pr3a1, "Aged Georgian sheep's cheese (Tusheti)", "complement", "established", "cheese", "Tannic amber wine and aged mountain sheep's cheese; the Caucasian cheese tradition")

pr3a2, n = PROD("Pheasant's Tears Saperavi Kakheti", "wine_still", p3a, r3, "Georgia",
                subcategory="Saperavi", price_tier="premium",
                description="Qvevri-fermented Saperavi; deep crimson with blackberry, dark plum, graphite and a firm tannic structure — Georgia's great indigenous red.")
if n:
    PAIR(pr3a2, "Mtsvadi (Georgian pork or lamb skewer)", "complement", "classic", "main", "Saperavi and grilled mtsvadi is the essential Georgian barbecue combination")
    PAIR(pr3a2, "Walnut-stuffed eggplant rolls (badrijani nigvzit)", "complement", "classic", "main", "The dark fruit of Saperavi mirrors and amplifies the walnut-stuffed aubergine")
    PAIR(pr3a2, "Slow-braised beef with Georgian herbs", "complement", "established", "main", "Powerful Saperavi tannins and structure suit slow-braised beef dishes perfectly")
    PAIR(pr3a2, "Churchkhela (walnut-grape candy)", "complement", "classic", "dessert", "The traditional Georgian sweet of grape and walnuts echoes Saperavi's flavours")

p3b = P("Iago's Wine", "winery", r3, "Georgia",
        production_philosophy="natural",
        philosophy_description="Iago Bitarishvili's minimal-intervention qvevri winery; Chinuri skin-contact white is a world reference for natural qvevri.",
        reputation_narrative="Iago Bitarishvili farms Chinuri in Kartli and produces some of Georgia's most minimalist and pure expressions of qvevri winemaking.",
        price_positioning="mid_range")
pr3b1, n = PROD("Iago's Wine Chinuri Kakheti", "wine_still", p3b, r3, "Georgia",
                subcategory="Chinuri", price_tier="mid_range",
                description="Qvevri Chinuri; Georgian skin-contact white with orange peel, dried herbs, walnut and a distinctive tannic grip — authentic and elemental.")
if n:
    PAIR(pr3b1, "Lobiani (bean-filled Georgian bread)", "complement", "classic", "main", "Earthy amber wine and Georgian bean bread is the most traditional Kartvelian combination")
    PAIR(pr3b1, "Grilled fish with pomegranate and herbs", "complement", "established", "main", "Tannic orange wine complements grilled fish garnished with Caucasian pomegranate")
    PAIR(pr3b1, "Pkhali (walnut-herb vegetable rolls)", "complement", "classic", "starter", "Walnut-inflected amber wine and the classic Georgian walnut-herb vegetable starter")
    PAIR(pr3b1, "Aged cheddar or farmhouse cheese", "complement", "established", "cheese", "Tannic skin-contact white finds harmony with firm aged farmhouse cheese")

pr3b2, n = PROD("Iago's Wine Rkatsiteli Natural", "wine_still", p3b, r3, "Georgia",
                subcategory="Rkatsiteli", price_tier="mid_range",
                description="Minimal-intervention Rkatsiteli qvevri; raw and elemental with tea tannins, dried citrus peel and an austere mineral backbone.")
if n:
    PAIR(pr3b2, "Cheese bread (khachapuri Adjaruli)", "complement", "classic", "main", "Georgia's iconic egg-and-cheese bread with its natural amber wine companion")
    PAIR(pr3b2, "Grilled aubergine with pomegranate seeds", "complement", "established", "starter", "Earthy amber wine mirrors the char of grilled aubergine with tart pomegranate")
    PAIR(pr3b2, "Mezze of hummus, olives and flatbread", "complement", "established", "starter", "Tannic amber Rkatsiteli is a revelatory match for Levantine mezze spreads")
    PAIR(pr3b2, "Slow-roasted lamb shoulder with cumin", "complement", "established", "main", "The ancient Caucasian tradition: amber wine and slow-cooked seasoned lamb")

# 4. TOKAJ — Hungary
print("=== Tokaj ===")
r4 = R("Tokaj", "Hungary", "wine",
        designation_type="PDO",
        designation_name="Tokaj",
        reputation_tier="iconic",
        quality_trajectory="ascending",
        description="The legendary Hungarian wine region at the confluence of the Bodrog and Tisza rivers, famous for Tokaji Aszú — the world's first classified botrytised wine (1730). The unique puttonyos system grades sweetness of Aszú wines; Eszencia (too sweet to ferment fully) is arguably the world's most extraordinary wine. Furmint and Hárslevelu are the primary grapes; dry Furmint is now establishing global recognition. Volcanic soils (rhyolite and andesite) contribute mineral tension to both sweet and dry expressions.",
        key_producers="Disznókő, Royal Tokaji, Oremus, István Szepsy, Dobogó",
        historical_context="Tokaj was the world's first region to classify its wines by sweetness and botrytis level, established by royal decree in 1730 — a century before Bordeaux's 1855 classification. Louis XIV called Tokaji 'the wine of kings; the king of wines.' The region fell to Communist collectivisation but has seen a quality renaissance since 1990 with international investment.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"exceptional","rising")]:
    VIN(r4, yr, qd, pt, f"Tokaj {yr}: Bodrog river mists encourage botrytis; Furmint of exceptional mineral tension")

p4a = P("István Szepsy", "winery", r4, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="The greatest living Tokaj producer; single-vineyard dry Furmint and Aszú from Mád's volcanic first-growth sites.",
        reputation_narrative="István Szepsy produces Tokaj's most celebrated wines; his 6 Puttonyos Aszú and dry St Tamás Furmint are international reference points for the region.",
        price_positioning="ultra_premium")
pr4a1, n = PROD("Szepsy Tokaji Aszú 6 Puttonyos", "wine_dessert", p4a, r4, "Hungary",
                subcategory="Furmint-Hárslevelu Aszú", price_tier="ultra_premium",
                description="6 Puttonyos Aszú from Mád; botrytised nectar of apricot jam, orange peel, ginger and extraordinary mineral tension from volcanic soils.")
if n:
    PAIR(pr4a1, "Foie gras with brioche and orange marmalade", "complement", "classic", "starter", "Tokaji Aszú and foie gras is one of the great sweet wine and rich food combinations")
    PAIR(pr4a1, "Stilton or mature Roquefort blue cheese", "contrast", "classic", "cheese", "The traditional sweet-salty pairing: Tokaji Aszú with powerful blue cheese")
    PAIR(pr4a1, "Peach and apricot tarte Tatin", "complement", "established", "dessert", "Stone fruit Aszú mirrors the caramelised peach and apricot of the tart")
    PAIR(pr4a1, "Crème brûlée with ginger", "complement", "established", "dessert", "Ginger-apricot Aszú and ginger-spiced crème brûlée; a harmonious luxury")

pr4a2, n = PROD("Szepsy Tokaj Dry Furmint St Tamás", "wine_still", p4a, r4, "Hungary",
                subcategory="Furmint", price_tier="ultra_premium",
                description="Dry St Tamás single-vineyard Furmint; volcanic mineral, citrus and extraordinary grip — one of Europe's most exciting dry whites.")
if n:
    PAIR(pr4a2, "Fogas (pike-perch) in paprika cream sauce", "complement", "classic", "main", "Hungary's freshwater fish speciality paired with the great dry Tokaj Furmint")
    PAIR(pr4a2, "Langoustines with lemon butter", "complement", "established", "main", "Dry volcanic Furmint's mineral precision lifts crustacean sweetness beautifully")
    PAIR(pr4a2, "Smoked salmon with cream cheese and dill", "complement", "established", "starter", "Mineral dry Furmint complements smoked salmon's richness with citrus acidity")
    PAIR(pr4a2, "Aged Manchego or Comté cheese", "complement", "established", "cheese", "Dry volcanic Furmint's mineral and citrus grip complements firm aged cheese")

p4b = P("Royal Tokaji", "winery", r4, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="The prestige Tokaj producer; formed by Hugh Johnson et al. in 1990 to restore single-vineyard classification; Mézes Mály and Nyulászó are First Growths.",
        reputation_narrative="Royal Tokaji restored the pre-Communist single-vineyard system; their 5 and 6 Puttonyos cuvées from classified sites are the most reliable Aszú expressions.",
        price_positioning="premium")
pr4b1, n = PROD("Royal Tokaji Mézes Mály 6 Puttonyos Aszú", "wine_dessert", p4b, r4, "Hungary",
                subcategory="Furmint Aszú", price_tier="ultra_premium",
                description="Mézes Mály First Growth 6 Puttonyos; honey (mézes = honey, mály = petal) in the name; extraordinary sweetness with elegant mineral backbone.")
if n:
    PAIR(pr4b1, "Roquefort with dried apricots and walnuts", "contrast", "classic", "cheese", "Mézes Mály's honey-sweetness contrasts the pungent blue perfectly")
    PAIR(pr4b1, "Warm gingerbread with orange custard", "complement", "established", "dessert", "Ginger-apricot Aszú perfectly mirrors gingerbread's warm spice and citrus custard")
    PAIR(pr4b1, "Crème caramel with Hungarian sour cherry", "complement", "established", "dessert", "Caramel sweetness of Aszú deepens the sour cherry note on the classic custard")
    PAIR(pr4b1, "Hungarian chimney cake (kürtőskalács)", "complement", "classic", "dessert", "The traditional festive rolled cake finds its natural Tokaj Aszú companion")

pr4b2, n = PROD("Royal Tokaji Dry Furmint", "wine_still", p4b, r4, "Hungary",
                subcategory="Furmint", price_tier="mid_range",
                description="Entry dry Tokaj Furmint; crisp grapefruit, green apple and volcanic mineral — a fresh, food-friendly introduction to dry Tokaj.")
if n:
    PAIR(pr4b2, "Chicken paprikash with egg noodles (csirkepaprikás)", "complement", "classic", "main", "Dry Furmint is Hungary's natural companion for the national paprika chicken dish")
    PAIR(pr4b2, "Grilled trout with dill and capers", "complement", "established", "main", "Fresh mineral Furmint and river trout is the classic Hungarian white wine pairing")
    PAIR(pr4b2, "Stuffed cabbage rolls (töltött káposzta)", "complement", "established", "main", "Mineral Furmint's acidity cuts through the richness of Hungarian stuffed cabbage")
    PAIR(pr4b2, "Lángos (fried dough with sour cream)", "complement", "suggested", "casual", "Fresh Furmint acidity cuts through the richness of fried lángos dough")

# 5. VILLÁNY — Hungary
print("=== Villány ===")
r5 = R("Villány", "Hungary", "wine",
        designation_type="PDO",
        designation_name="Villány",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Hungary's warmest wine region, on limestone and red clay soils at the foot of the Villány mountains near the Croatian border. Famous for producing Hungary's finest red wines from Cabernet Franc, Cabernet Sauvignon, Merlot and the indigenous Kadarka. Villány-Siklós also produces white wines. The Villány Wine District was the first in Hungary to receive classification in 1994. Attila Gere and Ede Tiffán pioneered the region's international recognition.",
        key_producers="Attila Gere, Vylyan, Bock, Sauska, Tiffán",
        historical_context="Villány's winemaking dates to Roman times. The region attracted German settlers in the 18th century after Ottoman occupation. The modern quality revolution began in the 1990s when producers like Attila Gere adopted modern techniques alongside the indigenous Kadarka grape. Villány wines now represent Hungary's best red wine region.")
for yr, qd, pt in [(2018,"exceptional","rising"),(2019,"excellent","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r5, yr, qd, pt, f"Villány {yr}: limestone and red clay harvest; Cabernet Franc and indigenous reds show exceptional ripeness")

p5a = P("Attila Gere", "winery", r5, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="The pioneer of modern Villány; Kopár single-vineyard and Attila Gere Cabernet Franc are Hungary's most celebrated reds.",
        reputation_narrative="Attila Gere transformed Villány from a bulk producer to Hungary's finest red wine region; his Kopár is one of Central Europe's most acclaimed wines.",
        price_positioning="premium")
pr5a1, n = PROD("Attila Gere Kopár Villány", "wine_still", p5a, r5, "Hungary",
                subcategory="Cabernet Franc-Merlot blend", price_tier="premium",
                description="Kopár from limestone hilltops; Cabernet Franc-dominated blend of great elegance, dark fruit, mineral and refined tannins — Villány's finest.")
if n:
    PAIR(pr5a1, "Beef tenderloin with forest mushroom ragù", "complement", "established", "main", "Villány's finest red and elegant beef tenderloin with mushrooms; Hungary's luxury pairing")
    PAIR(pr5a1, "Roast lamb with Hungarian herbs and paprika", "complement", "established", "main", "Central European lamb and Villány Cabernet Franc; the Hungarian prestige pairing")
    PAIR(pr5a1, "Wild boar goulash with bread dumplings", "complement", "established", "main", "Villány Cabernet's structure and dark fruit hold their own against wild boar goulash")
    PAIR(pr5a1, "Aged sheep's cheese with walnut and quince", "complement", "established", "cheese", "Refined Villány red and aged sheep's cheese with walnut is an elegant cheese course")

pr5a2, n = PROD("Attila Gere Villány Cabernet Franc", "wine_still", p5a, r5, "Hungary",
                subcategory="Cabernet Franc", price_tier="mid_range",
                description="Single-varietal Cabernet Franc; red cherry, violet, graphite and refined limestone mineral — the pure Villány expression.")
if n:
    PAIR(pr5a2, "Pörkölt (Hungarian beef stew with paprika)", "complement", "classic", "main", "Villány Cabernet Franc and Hungarian pörkölt beef stew; the national wine-food match")
    PAIR(pr5a2, "Roast duck with red cabbage", "complement", "established", "main", "Red-fruited Cabernet Franc and duck with braised red cabbage; classic Hungarian")
    PAIR(pr5a2, "Grilled pork chop with Hungarian pepper sauce", "complement", "established", "main", "Hungarian pepper sauce and Villány red; the local paprika-wine harmony")
    PAIR(pr5a2, "Mushroom-stuffed chicken thigh with tarragon", "complement", "established", "main", "Elegant Cabernet Franc suits mushroom-stuffed chicken with fresh herb")

p5b = P("Vylyan Winery", "winery", r5, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="Villány estate known for Cabernet Franc-led blends and the indigenous Kadarka revival; Montenuovo is the prestige cuvée.",
        reputation_narrative="Péter Szabó's Vylyan estate produces consistently outstanding Villány reds; their Montenuovo is one of Hungary's most sought-after collectible wines.",
        price_positioning="premium")
pr5b1, n = PROD("Vylyan Montenuovo Villány", "wine_still", p5b, r5, "Hungary",
                subcategory="Cabernet Franc-Cabernet Sauvignon-Merlot", price_tier="premium",
                description="Montenuovo prestige blend; full-bodied with dark fruit, cedar, spice and structured tannins — Villány's most serious expression.")
if n:
    PAIR(pr5b1, "Roast shoulder of venison with juniper and red wine", "complement", "established", "main", "Full-bodied Villány prestige blend and roasted venison; the great Hungarian game pairing")
    PAIR(pr5b1, "Grilled côte de boeuf with marrow butter", "complement", "established", "main", "Structured Montenuovo holds up to the richest beef cuts with mineral grace")
    PAIR(pr5b1, "Slow-braised beef short rib with polenta", "complement", "established", "main", "Layered Villány blend and slow-braised beef; a satisfying central European combination")
    PAIR(pr5b1, "Aged hard cheese (Manchego, Gruyère)", "complement", "established", "cheese", "Structured Montenuovo's dark fruit and mineral pair beautifully with aged hard cheese")

pr5b2, n = PROD("Vylyan Villány Cabernet Franc Classic", "wine_still", p5b, r5, "Hungary",
                subcategory="Cabernet Franc", price_tier="mid_range",
                description="Entry Vylyan Cabernet Franc; red cherry, graphite and gentle herb with medium body and fresh acidity — approachable Villány.")
if n:
    PAIR(pr5b2, "Chicken paprikash with buttered noodles", "complement", "classic", "main", "Hungarian Cabernet Franc and the national paprika chicken dish; a natural match")
    PAIR(pr5b2, "Grilled sausages with sauerkraut", "complement", "established", "main", "Central European tradition: Cabernet Franc and fermented cabbage with sausage")
    PAIR(pr5b2, "Langos with sour cream and cheese", "complement", "established", "casual", "Light Villány red works alongside casual Hungarian fried bread snack")
    PAIR(pr5b2, "Beef goulash soup (gulyásleves)", "complement", "classic", "main", "The essential Hungarian soup-stew finds its natural Villány companion")

# Final counts
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

cur.close()
conn.close()
print("B126 complete.")
