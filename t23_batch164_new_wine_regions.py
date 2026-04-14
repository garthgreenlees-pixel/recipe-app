#!/usr/bin/env python3
"""B164 — Eastern + Caucasus + Levant wine regions: Naoussa PDO, Tokaj PDO, Kakheti, Bekaa Valley, Rheinhessen QbA"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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

# === NAOUSSA PDO ===
print("=== Naoussa PDO ===")
r1 = R("Naoussa PDO", "Greece", "wine",
       designation_type="PDO",
       designation_name="Naoussa Protected Designation of Origin",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Naoussa in northern Greece (Macedonia) is the birthplace of Xinomavro — Greece's most complex and age-worthy red grape. Called 'the Barolo of Greece', great Naoussa Xinomavro shows brick-red colour, intense tannins, high acidity, and flavours of tomato, olive, dried herbs, and red fruit evolving to leather and truffle with age. The terroir of Mount Vermio at 200–350m elevation, with sandy limestone soils, produces wines of exceptional structure and longevity.",
       key_producers="Kir-Yianni, Boutari, Thymiopoulos Vineyards, Alpha Estate",
       historical_context="Naoussa received Greece's first Appellation of Superior Quality status in 1971, recognizing the region's long history of producing structured red wines from Xinomavro — a grape name that translates as 'acid black'.")
for yr, qd, pt, sn in [
    (2017,"excellent","stable","A great Naoussa vintage — Xinomavro of exceptional structure and aromatic complexity."),
    (2018,"very_good","stable","Fine year with good fruit-acid balance and the typical tannic backbone of great Naoussa."),
    (2019,"excellent","rising","One of the finest recent Naoussa vintages — wines of extraordinary concentration and freshness."),
    (2020,"very_good","stable","Good ripeness; high-altitude vineyards yielded the most elegant, age-worthy wines."),
    (2021,"excellent","rising","Landmark year for Xinomavro — wines combining power with unusual finesse."),
    (2022,"very_good","stable","Warm vintage produced generous, accessible Naoussa with softer tannins than typical."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Kir-Yianni Estate", "winery", r1, "Greece",
       production_philosophy="terroir_expression",
       philosophy_description="Founded by Yiannis Boutaris after leaving the family Boutari business, Kir-Yianni is Naoussa's most prestigious estate. Their Ramnista single-vineyard Xinomavro is widely considered Greece's greatest red wine, showing extraordinary structure and longevity.",
       reputation_narrative="Kir-Yianni's Ramnista Xinomavro has placed Naoussa on the world wine map — this single-vineyard wine demonstrates that indigenous Greek grapes can produce wines of international reference quality.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Kir-Yianni Ramnista Naoussa Xinomavro", "wine_still", p1, r1, "Greece",
                    subcategory="red", description="Single-vineyard old-vine Xinomavro from the Ramnista parcel. Deep garnet, intense — tomato paste, dried herbs, red cherry, leather, cedar, and firm tannins requiring years of cellaring. Among Greece's most age-worthy reds.", price_tier="premium")
if is_new:
    PAIR(prod, "Braised lamb shanks with tomato, herbs and olives", "complement", "classic", "main", "Xinomavro's tomato and herb notes mirror the braised lamb's flavours — a deeply Greek pairing of wine and food.")
    PAIR(prod, "Moussaka with rich bechamel and spiced lamb", "complement", "classic", "main", "High acidity cuts bechamel richness; tomato character in the wine bridges to the spiced meat sauce perfectly.")
    PAIR(prod, "Wild boar stew with chestnuts and bay leaf", "complement", "established", "main", "Tannic Xinomavro needs gamey richness; chestnut's earthiness and bay bridge the wine's herbal complexity.")
    PAIR(prod, "Aged kefalograviera cheese with roasted peppers", "complement", "established", "cheese", "Hard Greek cheese's salt and tang are softened by Xinomavro's fruit; peppers echo the wine's pepper notes.")
prod, is_new = PROD("Kir-Yianni Yianakohori Hills Xinomavro Naoussa", "wine_still", p1, r1, "Greece",
                    subcategory="red", description="Estate Naoussa Xinomavro — more approachable than Ramnista but equally expressive. Red cherry, tomato leaf, dried oregano, soft herbs, and grippy tannins softened by careful winemaking. The gateway to serious Naoussa.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Roast chicken stuffed with herbs, garlic and lemon", "complement", "established", "main", "Lighter Xinomavro's herbal, red fruit character lifts roast chicken; lemon echoes the wine's acidity.")
    PAIR(prod, "Grilled vegetable mezze with feta and olive", "complement", "established", "main", "The wine's herbal, Mediterranean character mirrors a vegetable spread; feta's salt bridges perfectly.")
    PAIR(prod, "Spaghetti with lamb ragù and cinnamon", "complement", "established", "main", "Xinomavro's tomato and herb notes mirror lamb ragù; cinnamon bridges the wine's spice complexity.")
    PAIR(prod, "Kasseri cheese with green olives", "complement", "classic", "cheese", "Classic Greek pairing — mild kasseri softens Xinomavro's tannins; olive's bitterness bridges the wine's herbal depth.")

# === TOKAJ PDO ===
print("=== Tokaj PDO ===")
r2 = R("Tokaj PDO", "Hungary", "wine",
       designation_type="PDO",
       designation_name="Tokaj Protected Designation of Origin",
       reputation_tier="iconic",
       quality_trajectory="ascending",
       description="Tokaj, in northeastern Hungary, produces what Louis XIV called 'the wine of kings and the king of wines' — the legendary Tokaji Aszú, made from botrytis-affected (nobly rotten) Furmint and Hárslevelű grapes. The unique volcanic tufa and clay loam soils, combined with the Bodrog and Tisza rivers' autumn morning mists, create perfect conditions for Botrytis cinerea. Dry Furmint is now also increasingly recognised as a world-class white variety of tremendous ageing potential.",
       key_producers="Royal Tokaji, Oremus, Disznókő, Patricius, Sauska",
       historical_context="Tokaj's wine history dates to the 11th century, and Tokaji Aszú was the world's first classified wine (1700), predating Bordeaux's 1855 classification by 155 years. The region was declared a UNESCO World Heritage Site in 2002.")
for yr, qd, pt, sn in [
    (2013,"exceptional","speculative","A legendary botrytis vintage; Aszú of extraordinary concentration and balance."),
    (2016,"excellent","stable","A landmark dry Furmint vintage alongside fine Aszú production."),
    (2017,"very_good","stable","Good botrytis conditions produced fine Aszú; dry Furmint also excellent."),
    (2019,"excellent","rising","One of the greatest recent Tokaj vintages for both dry and sweet wines."),
    (2021,"very_good","stable","Fine conditions; excellent dry Furmint and classic Aszú of good concentration."),
    (2022,"excellent","rising","Exceptional dry Furmint vintage; Aszú also showing great promise."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Royal Tokaji Wine Company", "winery", r2, "Hungary",
       production_philosophy="terroir_expression",
       philosophy_description="Founded in 1990 with Hugh Johnson among the founders, Royal Tokaji was the first foreign investment in Hungarian wine after communism ended. Their single-vineyard Aszú wines from first-growth (First Class) vineyards like Mézes Mály and Nyulászó are world benchmarks.",
       reputation_narrative="Royal Tokaji set the standard for the post-communist revival of great Tokaji Aszú, producing single-vineyard wines that demonstrate the region's terroir diversity and the extraordinary potential of Furmint with botrytis.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Royal Tokaji Aszú 5 Puttonyos", "wine_dessert", p2, r2, "Hungary",
                    subcategory="botrytis_sweet", description="Multi-vineyard Aszú 5 Puttonyos — the classic Tokaji sweet wine at its most accessible. Apricot, mango, orange marmalade, honey, and saffron with a long, cleansing acid finish. Extraordinary food versatility.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roquefort with walnuts and honey", "contrast", "classic", "cheese", "The classic Tokaji pairing — Aszú's sweetness and acidity contrast the blue cheese's salt and funk in electrifying balance.")
    PAIR(prod, "Foie gras terrine with brioche and fig jam", "complement", "classic", "starter", "Sweet apricot and honey in the Aszú mirror foie's richness; acidity prevents cloying — a Sauternes-like pairing.")
    PAIR(prod, "Apricot tarte tatin with crème fraîche", "complement", "classic", "dessert", "Apricot and honey notes mirror the tart's fruit; the Aszú's acidity lifts the dessert beautifully.")
    PAIR(prod, "Spiced duck liver pâté with orange marmalade", "complement", "established", "starter", "Orange marmalade notes bridge to the pâté's richness; Aszú's acidity cuts through liver's fat.")
prod, is_new = PROD("Royal Tokaji Mézes Mály First Growth Aszú 6 Puttonyos", "wine_dessert", p2, r2, "Hungary",
                    subcategory="botrytis_sweet", description="Single First Growth vineyard Aszú 6 Puttonyos from the famous Mézes Mály ('honey meadow') — one of Tokaj's greatest terroirs. Extraordinary concentration: candied orange, mango, saffron, honey, and an almost infinite acid finish.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Seared foie gras with peach and Aszú reduction", "complement", "classic", "starter", "The pinnacle of Hungarian haute cuisine — Aszú's sweetness and intensity match foie's richness; shared stone fruit elevates both.")
    PAIR(prod, "Gorgonzola Dolce with pear and walnuts", "contrast", "classic", "cheese", "The sweetness contrasts blue cheese's salt-funk; pear bridges the wine's stone fruit character.")
    PAIR(prod, "Beeswax and honey ice cream with orange blossom", "complement", "adventurous", "dessert", "The wine's honey and beeswax notes mirror the ice cream; orange blossom echoes the Aszú's floral depth.")
    PAIR(prod, "Almond tart with saffron cream", "complement", "established", "dessert", "Saffron notes in the Aszú mirror the cream; almond bridges to Furmint's characteristic nuttiness.")

p3 = P("Disznókő Estate", "winery", r2, "Hungary",
       production_philosophy="terroir_expression",
       philosophy_description="AXA Millésimes' Tokaj estate, Disznókő ('pig stone') produces outstanding dry Furmint alongside Aszú wines of great precision. The estate's single-vineyard approach and innovative dry wine programme have been influential in Tokaj's modernisation.",
       reputation_narrative="Disznókő's dry Furmint has helped position Tokaj's still wine alongside great white Burgundy and German Riesling in international markets, demonstrating that Furmint is one of the world's great white grape varieties.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Disznókő Dry Furmint Tokaj", "wine_still", p3, r2, "Hungary",
                    subcategory="white", description="Dry Furmint from volcanic tufa and loess soils — bright, mineral, with lemon zest, green apple, white peach, and a distinctive volcanic-mineral backbone. Shows remarkable ageing potential for a dry white wine.", price_tier="premium")
if is_new:
    PAIR(prod, "Pike-perch (fogash) with dill and caper cream sauce", "complement", "classic", "main", "The quintessential Hungarian fish pairing — Furmint's acidity and mineral depth complement the delicate freshwater fish.")
    PAIR(prod, "Roasted goose liver with apple and sage", "complement", "established", "starter", "Dry Furmint's acidity cuts through liver richness; apple echoes the wine's fruit; sage bridges the mineral notes.")
    PAIR(prod, "Cheese strudel with sour cream — rétes", "complement", "established", "dessert", "Furmint's acidity cuts pastry richness; mineral freshness refreshes the palate between bites.")
    PAIR(prod, "Grilled freshwater trout with lemon and herbs", "complement", "classic", "main", "Classic central European freshwater fish pairing — mineral, acidic Furmint is the ideal match.")

# === KAKHETI ===
print("=== Kakheti ===")
r3 = R("Kakheti", "Georgia", "wine",
       designation_type="region",
       designation_name="Kakheti Wine Region",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Georgia's Kakheti region is the cradle of wine — the South Caucasus is where viticulture began 8,000 years ago, and Kakheti produces over 70% of Georgia's wine. The region is famous for its qvevri (clay amphora) winemaking tradition, producing both white 'amber wines' from skin contact and fresh 'European-style' whites. Rkatsiteli is the dominant white variety; Saperavi the great red — one of the world's few teinturier grapes with red flesh as well as skin.",
       key_producers="Alaverdi Monastery, Pheasant's Tears, Teliani Valley, Schuchmann Wines, Vinoterra",
       historical_context="Georgia has 8,000 years of continuous winemaking tradition — the world's oldest. The qvevri clay amphora method of fermenting and ageing wine with extended skin contact is a UNESCO Intangible Cultural Heritage. Georgia's 525+ indigenous varieties represent an unparalleled viticultural treasury.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","A landmark year for Kakheti — Rkatsiteli and Saperavi of exceptional concentration and freshness."),
    (2020,"very_good","stable","Good vintage; amber wines particularly successful for aromatic complexity."),
    (2021,"excellent","rising","One of the finest recent Georgian vintages — qvevri wines of extraordinary depth."),
    (2022,"very_good","stable","Warm year; Saperavi showing rich, concentrated fruit; amber wines slightly fuller than typical."),
    (2023,"excellent","rising","Outstanding conditions produced Georgian wines of great balance and aromatic complexity."),
]:
    VIN(r3, yr, qd, pt, sn)

p4 = P("Pheasant's Tears Winery", "winery", r3, "Georgia",
       production_philosophy="biodynamic",
       philosophy_description="Founded by American artist John Wurdeman and Georgian winemaker Gela Patalishvili, Pheasant's Tears makes wines using traditional qvevri methods with minimal intervention. Their commitment to Georgia's 500+ indigenous varieties and ancient winemaking traditions has brought international recognition to Kakheti.",
       reputation_narrative="Pheasant's Tears is the international face of Georgia's wine renaissance — their qvevri-fermented amber wines and natural Saperavi have introduced the world to one of viticulture's oldest and most distinctive traditions.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Pheasant's Tears Rkatsiteli Amber Kakheti", "wine_still", p4, r3, "Georgia",
                    subcategory="orange_amber", description="Qvevri-fermented Rkatsiteli with 6 months skin contact — the definitive amber wine. Deep golden-amber colour, intense tannins, dried apricot, chamomile, hazelnut, beeswax, and a long, saline mineral finish. Uniquely food-versatile.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Lamb shashlik with tkemali plum sauce", "complement", "classic", "main", "The wine's tannins handle lamb's richness; tkemali's acidity mirrors the amber wine's own tang — a quintessential Georgian pairing.")
    PAIR(prod, "Walnut-stuffed eggplant — badrijani nigvzit", "complement", "classic", "starter", "One of Georgia's signature pairings — amber wine's tannins and dried fruit complement walnut's richness and eggplant's earthy depth.")
    PAIR(prod, "Aged hard cheese with honey and walnuts", "complement", "established", "cheese", "The wine's tannins handle hard cheese; honey bridges the amber wine's dried fruit notes beautifully.")
    PAIR(prod, "Grilled spiced lamb kofta with yogurt sauce", "complement", "established", "main", "Amber wine's phenolic grip cuts through spiced lamb fat; dried herb notes in the wine echo the kofta's seasonings.")
prod, is_new = PROD("Pheasant's Tears Saperavi Kakheti", "wine_still", p4, r3, "Georgia",
                    subcategory="red", description="Traditional qvevri-fermented Saperavi — Georgia's great teinturier grape, with deep inky purple colour, wild blackberry, plum, iron, dried herbs, and firm tannins that demand food or cellaring.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled pork mtsvadi (Georgian shashlik)", "complement", "classic", "main", "The definitive Saperavi pairing — the wine's iron and dark fruit cut through grilled pork's richness perfectly.")
    PAIR(prod, "Beef khinkali (Georgian dumplings)", "complement", "classic", "main", "Dark, tannic Saperavi balances khinkali's rich meat filling; the wine's acidity cuts through dumpling dough.")
    PAIR(prod, "Slow-roasted lamb shoulder with fresh herbs", "complement", "established", "main", "Saperavi's iron and dark fruit complement lamb's richness; the wine's herbal notes mirror fresh herb accompaniment.")
    PAIR(prod, "Dark chocolate with dried cherry and hazelnut", "complement", "adventurous", "dessert", "The wine's dark cherry and iron notes bridge to bitter chocolate; hazelnut echoes Saperavi's earthy depth.")

p5 = P("Alaverdi Monastery Winery", "winery", r3, "Georgia",
       production_philosophy="traditional_methods",
       philosophy_description="The historic Alaverdi Cathedral has produced wine since the 11th century, making it one of the world's oldest continuously operating wineries. Their qvevri wines are made by the monastery's monks using ancient Georgian methods with little modification over centuries.",
       reputation_narrative="Alaverdi Monastery is Georgia's most historically significant winery — their Rkatsiteli and Mtsvane amber wines represent an unbroken thread of winemaking tradition stretching back nearly a millennium.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Alaverdi Monastery Rkatsiteli Mtsvane Amber", "wine_still", p5, r3, "Georgia",
                    subcategory="orange_amber", description="Traditional qvevri amber wine from Rkatsiteli and Mtsvane blended and fermented on skins for 6 months. Ancient style — golden amber, oxidative, with dried apricot, orange peel, walnut, and a long tannic finish.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Lobiani (bean-filled bread) with tkemali", "complement", "classic", "main", "A monastic Georgian pairing — amber wine's tannins balance the bread's richness; tkemali's acidity echoes the wine's tang.")
    PAIR(prod, "Grilled wild mushrooms with fresh coriander and garlic", "complement", "established", "starter", "Amber wine's oxidative, earthy notes bridge to wild mushrooms; coriander mirrors the wine's herbal character.")
    PAIR(prod, "Sulguni cheese with herbs and flatbread", "complement", "classic", "cheese", "Classic Georgian cheese pairing — sulguni's salt and tang are balanced by amber wine's tannins and dried fruit.")
    PAIR(prod, "Roasted chicken with walnut sauce — satsivi", "complement", "classic", "main", "Walnut notes in the wine bridge perfectly to satsivi's walnut sauce — one of Georgia's greatest food and wine matches.")

# === BEKAA VALLEY ===
print("=== Bekaa Valley ===")
r4 = R("Bekaa Valley", "Lebanon", "wine",
       designation_type="region",
       designation_name="Bekaa Valley Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Lebanon's Bekaa Valley, at 900–1100m altitude in the Anti-Lebanon Mountains, produces some of the Middle East's most celebrated wines. Warm days and cool nights, limestone soils, and low rainfall create ideal conditions for international and indigenous varieties. Château Musar, Lebanon's most famous producer, has made some of its greatest wines during the country's civil war, demonstrating the Bekaa's viticultural resilience. Cabernet Sauvignon, Cinsault, Merlot, Tempranillo, and indigenous Obaideh and Merwah thrive here.",
       key_producers="Château Musar, Château Ksara, Château Kefraya, Domaine des Tourelles, Massaya",
       historical_context="The Bekaa Valley has one of the world's oldest winemaking traditions — the Phoenicians exported wine from Lebanon across the ancient Mediterranean. Château Musar, founded in 1930, survived Lebanon's civil war (1975–1990) to produce some of the world's most distinctive and age-worthy wines.")
for yr, qd, pt, sn in [
    (2015,"excellent","stable","A landmark year for the Bekaa — wines of extraordinary concentration and balance."),
    (2016,"very_good","stable","Good vintage; Château Musar's blend showing typical complexity and idiosyncratic depth."),
    (2018,"excellent","rising","Fine conditions produced structured, age-worthy wines across the Bekaa."),
    (2019,"very_good","stable","Good ripeness despite challenging regional context; top estates excelled."),
    (2021,"excellent","rising","An outstanding vintage for Bekaa Valley despite ongoing national difficulties."),
]:
    VIN(r4, yr, qd, pt, sn)

p6 = P("Château Musar", "winery", r4, "Lebanon",
       production_philosophy="minimal_intervention",
       philosophy_description="Lebanon's most celebrated winery, founded in 1930 by Gaston Hochar and continued by his son Serge. The famous Château Musar red — a blend of Cabernet Sauvignon, Cinsault, and Carignan from 50+ year old vines — is one of the wine world's most idiosyncratic and age-worthy wines.",
       reputation_narrative="Château Musar is one of the wine world's great eccentrics — producing wines of extraordinary age-worthiness and flavour complexity that defy categorisation. The fact that they continued producing through Lebanon's civil war has become part of wine legend.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Château Musar Bekaa Valley Red", "wine_still", p6, r4, "Lebanon",
                    subcategory="red", description="The iconic blend of Cabernet Sauvignon, Cinsault, and Carignan from 50-year-old vines. Complex, idiosyncratic — tobacco, leather, dried rose, dark cherry, spice, and a haunting Middle Eastern mineral quality. Released 7 years after vintage.", price_tier="premium")
if is_new:
    PAIR(prod, "Slow-roasted lamb shoulder with baharat spice and pomegranate", "complement", "classic", "main", "The Musar's complex dried fruit and spice notes mirror Lebanese spiced lamb; pomegranate's acidity echoes the wine's freshness.")
    PAIR(prod, "Grilled quail with fattoush and sumac", "complement", "established", "main", "The wine's tobacco and dried herb complexity pairs with quail's delicate gaminess; sumac's acidity bridges perfectly.")
    PAIR(prod, "Aged hard Rumi cheese with dried figs", "complement", "established", "cheese", "Middle Eastern hard cheese meets Musar's dried fruit complexity in a naturally regional pairing.")
    PAIR(prod, "Beef kofta with tahini sauce and preserved lemon", "complement", "established", "main", "Spiced beef kofta mirrors the wine's complex spice notes; tahini's richness is balanced by Musar's acidity.")
prod, is_new = PROD("Château Musar White Bekaa Valley", "wine_still", p6, r4, "Lebanon",
                    subcategory="white", description="Rare blend of indigenous Obaideh and Merwah varieties — one of the world's most unusual white wines. Orange blossom, waxy yellow fruit, roasted nuts, and a distinctive oxidative complexity. Released 7 years after vintage alongside the red.", price_tier="premium")
if is_new:
    PAIR(prod, "Kibbeh nayyeh (raw spiced lamb tartare)", "complement", "adventurous", "starter", "A bold Lebanese pairing — the wine's oxidative complexity and spice affinity match kibbeh's herb-spiced raw lamb.")
    PAIR(prod, "Baked sea bass chermoula with preserved lemon", "complement", "established", "main", "The wine's waxy fruit and oxidative depth match sea bass's meaty texture; chermoula's herbs bridge the complexity.")
    PAIR(prod, "Hummus with warm flatbread and olive oil", "complement", "established", "starter", "The wine's oxidative, nutty character complements chickpea richness; olive oil bridges both beautifully.")
    PAIR(prod, "Aged halloumi with honey and za'atar", "complement", "established", "cheese", "Halloumi's salt and the wine's oxidative richness create a Middle Eastern-flavoured bridge; honey ties together.")

# === RHEINHESSEN QBA ===
print("=== Rheinhessen QbA ===")
r5 = R("Rheinhessen QbA", "Germany", "wine",
       designation_type="QbA",
       designation_name="Rheinhessen Qualitätswein bestimmter Anbaugebiete",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Germany's largest wine region by area, Rheinhessen has undergone a remarkable quality revolution. Once associated with simple Liebfraumilch, the region now produces exciting dry Riesling, Silvaner, and Spätburgunder (Pinot Noir) from a new generation of producers. The diverse soils — red slate, limestone, loess, and quartzite — and warm continental climate create genuine terroir diversity. The Rheinhessen Renaissance, led by producers like Keller and Wagner-Stempel, has made this one of Germany's most dynamic regions.",
       key_producers="Weingut Keller, Wagner-Stempel, Battenfeld-Spanier, Gunderloch, Heyl zu Herrnsheim",
       historical_context="Rheinhessen was historically the source of Germany's most commercial wine, but a new generation of producers beginning in the 1990s completely transformed the region's image through site-specific, low-yield viticulture and dry winemaking styles.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark vintage for Rheinhessen — warm, dry conditions produced Riesling and Spätburgunder of unusual concentration."),
    (2019,"very_good","stable","Fine vintage; particularly successful for dry Riesling Grosses Gewächs wines."),
    (2020,"excellent","rising","Outstanding conditions; Keller's G-Max and other top wines among the region's finest ever."),
    (2021,"very_good","stable","Cooler year produced elegant, racy Riesling with excellent acidity for long ageing."),
    (2022,"very_good","stable","Warm vintage; rich Spätburgunder and concentrated Riesling across the region."),
    (2023,"excellent","rising","Exceptional vintage across all varieties; Riesling GG wines of extraordinary precision."),
]:
    VIN(r5, yr, qd, pt, sn)

p7 = P("Weingut Keller Rheinhessen", "winery", r5, "Germany",
       production_philosophy="terroir_expression",
       philosophy_description="Klaus-Peter Keller is widely considered Germany's greatest living winemaker. His G-Max Riesling GG from the Westhofen vineyards commands extraordinary prices and critical acclaim, while the estate's range from village Riesling to GG demonstrates what Rheinhessen can achieve at the very highest level.",
       reputation_narrative="Keller is Germany's most celebrated white wine producer — the G-Max is consistently rated among the world's greatest white wines, and has single-handedly repositioned Rheinhessen from Germany's bulk wine source to a region capable of world-class Riesling.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Keller Riesling Trocken Rheinhessen", "wine_still", p7, r5, "Germany",
                    subcategory="white", description="Estate dry Riesling — the entry to Keller's range, but produced with the same obsessive care as the GG wines. Dry, mineral, with citrus zest, peach, white flowers, and the estate's characteristic slaty backbone. Extraordinary value from a legendary producer.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled asparagus with hollandaise and Westphalian ham", "complement", "classic", "main", "The quintessential German Riesling and asparagus pairing — mineral acidity mirrors asparagus's vegetal snap; hollandaise needs the wine's freshness.")
    PAIR(prod, "Sautéed chanterelles with parsley on toast", "complement", "established", "starter", "Mineral Rheinhessen Riesling bridges to earthy chanterelles; parsley echoes the wine's herbal dimension.")
    PAIR(prod, "Grilled Rhine salmon with lemon caper sauce", "complement", "classic", "main", "A regional classic — Riesling from the Rhine is the natural partner for Rhine salmon; capers echo the wine's acidity.")
    PAIR(prod, "Aged Münster cheese with cumin", "complement", "established", "cheese", "The bold Münster pairs with mineral, dry Riesling — a traditional Alsace-Rhine classic that crosses the border.")
prod, is_new = PROD("Keller Westhofen Kirchspiel Riesling GG", "wine_still", p7, r5, "Germany",
                    subcategory="white", description="Grand Cru-equivalent Grosses Gewächs Riesling from the prized Kirchspiel vineyard in Westhofen — limestone and loess over red slate. Profound depth: citrus blossom, white peach, honey, slate minerality, and decades of ageing potential.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Whole Dover sole meunière with browned butter and capers", "complement", "classic", "main", "The wine's profound minerality and freshness match Dover sole's delicate richness; browned butter bridges the GG's complexity.")
    PAIR(prod, "Lobster bisque with cream and cognac", "complement", "established", "starter", "GG depth and acidity stand up to the bisque's richness; the wine's stone fruit echoes the crustacean's sweetness.")
    PAIR(prod, "Seared scallops with truffle and cauliflower purée", "complement", "classic", "starter", "Slate minerality bridges to the truffle; the GG's precision mirrors the scallop's delicate sweetness.")
    PAIR(prod, "Vacherin Mont d'Or with truffle and crusty bread", "bridge", "adventurous", "cheese", "The runny, intensely flavoured cheese needs a wine of equivalent depth — GG Riesling's minerality creates an extraordinary bridge.")

p8 = P("Wagner-Stempel Rheinhessen", "winery", r5, "Germany",
       production_philosophy="organic",
       philosophy_description="Daniel Wagner is one of Rheinhessen's leading quality advocates, producing refined dry Riesling and Silvaner from biodynamically farmed vineyards in Siefersheim. His wines helped define the 'Rheinhessen Renaissance' and continue to demonstrate the region's potential for world-class whites.",
       reputation_narrative="Wagner-Stempel is a key figure in Rheinhessen's quality revolution — their Siefersheim Riesling GG and Silvaner GG wines consistently rank among Germany's finest, showing that alternatives to Mosel can produce Riesling of great complexity.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Wagner-Stempel Siefersheim Riesling Trocken GG", "wine_still", p8, r5, "Germany",
                    subcategory="white", description="Grosses Gewächs Riesling from the volcanic porphyry soils of Siefersheim — one of Rheinhessen's most distinctive terroirs. Intense, mineral, with grapefruit, white flowers, smoked rock, and extraordinary ageing potential.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled sea bass with fennel and saffron", "complement", "established", "main", "The volcanic mineral intensity of Siefersheim GG bridges to saffron's mineral-floral depth; fennel echoes the wine's herbal aromatic.")
    PAIR(prod, "Crab salad with citrus and fresh herbs", "complement", "classic", "starter", "Grapefruit notes mirror the citrus dressing; mineral freshness echoes crab's natural brininess.")
    PAIR(prod, "White asparagus in Riesling cream sauce", "complement", "classic", "main", "A German regional classic — Riesling with white asparagus in Riesling sauce is an entirely self-referential and delicious pairing.")
    PAIR(prod, "Époisses de Bourgogne washed rind cheese", "complement", "adventurous", "cheese", "Powerful washed rind needs powerful Riesling — the wine's acidity and mineral edge cut through the cheese's creamy intensity.")

# === DB STATE ===
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
print("B164 complete.")
cur.close()
conn.close()
