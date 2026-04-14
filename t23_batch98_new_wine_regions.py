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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Beaujolais Villages ────────────────────────────────────────────
print("=== Region 1: Beaujolais Villages ===")
r = R("Beaujolais Villages", "France", "wine",
      designation_type="AOC", designation_name="Beaujolais Villages AOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Middle tier of Beaujolais between Beaujolais generic and the ten crus; granite and limestone soils; Gamay of more concentration and character than basic Beaujolais; excellent value.",
      key_producers="Jean-Paul Brun, Domaine des Nugues, Château des Jacques",
      historical_context="The Beaujolais Villages zone produces some 35% of all Beaujolais; the best examples from granite soils rival the lesser crus in quality.")
VIN(r, 2023, "excellent", "stable", "Classic Beaujolais year; vibrant, juicy Gamay with good concentration.")
VIN(r, 2022, "very_good", "stable", "Warm year; richer Gamay style with depth beyond the norm.")
VIN(r, 2021, "excellent", "stable", "Cool year; elegant, transparent Gamay with mineral freshness.")
VIN(r, 2020, "exceptional", "rising", "Outstanding year; Beaujolais Villages of unexpected depth and structure.")
VIN(r, 2019, "very_good", "stable", "Good balance; fruit-forward and approachable.")
p1 = P("Jean-Paul Brun Terres Dorées", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="Champion of carbonic-free, traditional Gamay vinification; estate Beaujolais Villages from limestone-clay; L'Ancien is his flagship; no added sulphur on some cuvées.",
       reputation_narrative="Jean-Paul Brun is Beaujolais's most awarded natural wine producer; L'Ancien redefined what old-vine Gamay could be.",
       price_positioning="value")
p2 = P("Domaine des Nugues", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Gilles Gelin's certified-organic Beaujolais Villages estate; granite soils in the northern zone; whole-cluster carbonic maceration; vibrant, aromatic Gamay.",
       reputation_narrative="One of Beaujolais Villages' most reliable estates; consistently expressive, food-friendly Gamay of real quality.",
       price_positioning="value")
pr1, n1 = PROD("Jean-Paul Brun L'Ancien Vieilles Vignes Gamay", "wine_still", p1, r, "France",
               subcategory="Gamay", price_tier="value",
               description="Old-vine Beaujolais from limestone-clay; traditional vinification (not carbonic); structured, mineral Gamay with cherry, violet and a firm, savoury finish.")
if n1:
    PAIR(pr1, "Charcuterie lyonnaise (rosette, saucisson sec)", "complement", "classic", "aperitif", "Classic Lyonnais pairing; mineral Gamay cuts pork fat; fruit mirrors cured meat spice.")
    PAIR(pr1, "Coq au vin with lardons and button mushrooms", "complement", "classic", "main", "Traditional Burgundy-adjacent pairing; Gamay's fruit and acid suit braised chicken.")
    PAIR(pr1, "Gruyère omelette with fresh herbs", "complement", "established", "main", "Café bistro classic; mineral Gamay suits eggs' richness; cherry fruit bridges cheese.")
    PAIR(pr1, "Tuna niçoise salad", "complement", "suggested", "main", "Light Gamay suits tuna's mild character; acidity bridges vinaigrette; cherry mirrors olive.")
pr2, n2 = PROD("Domaine des Nugues Beaujolais Villages", "wine_still", p2, r, "France",
               subcategory="Gamay", price_tier="value",
               description="Organic carbonic Gamay from northern granite soils; vivid cherry, wild strawberry and violet with classic Beaujolais freshness and soft, supple finish.")
if n2:
    PAIR(pr2, "Pan-fried duck liver (foie de canard) with herbs", "complement", "established", "starter", "Light Gamay and liver: a Lyonnais bouchon classic; fruit mirrors liver richness; herb bridges.")
    PAIR(pr2, "Quiche lorraine with Gruyère and lardons", "complement", "classic", "main", "Bistro pairing; fresh Gamay cuts egg and cheese richness; cherry mirrors smoky lardons.")
    PAIR(pr2, "Grilled merguez with ratatouille", "complement", "suggested", "main", "Gamay's freshness suits Mediterranean vegetables; cherry and violet bridge spiced sausage.")
    PAIR(pr2, "Cheese board with Époisses and Comté", "complement", "established", "cheese", "Beaujolais region pairing; vibrant Gamay suits rich washed-rind; cherry bridges Comté.")

# ── Region 2: Xinomavro homeland — Goumenissa ────────────────────────────────
print("=== Region 2: Goumenissa ===")
r = R("Goumenissa", "Greece", "wine",
      designation_type="PDO", designation_name="Goumenissa PDO",
      reputation_tier="overlooked", quality_trajectory="ascending",
      description="Northern Greek PDO in Macedonia; Xinomavro blended with Negoska; produces softer, more approachable reds than Naoussa with elegant cherry and earthy character.",
      key_producers="Chatzivariti, Aigiokeros, Boutari Goumenissa",
      historical_context="One of Greece's oldest wine zones; the local Negoska adds a rounded character to Xinomavro's austerity; wines were exported to Constantinople during the Byzantine Empire.")
VIN(r, 2021, "excellent", "rising", "Good cool year; precise Xinomavro-Negoska with elegant cherry and earthy depth.")
VIN(r, 2020, "very_good", "stable", "Warm year; plush, approachable blend; good early drinking character.")
VIN(r, 2019, "excellent", "stable", "Classic Northern Greek profile; structured reds with Mediterranean herb notes.")
VIN(r, 2018, "very_good", "stable", "Good balance; food-friendly Goumenissa with characteristic earthy freshness.")
VIN(r, 2017, "very_good", "stable", "Reliable year; consistent, accessible Xinomavro-Negoska blends.")
p1 = P("Aigiokeros", "winery", r, "Greece",
       production_philosophy="terroir_focused",
       philosophy_description="Small estate in Goumenissa; estate-grown Xinomavro-Negoska from hillside vineyards; aged in French oak; benchmark for the appellation's lighter, elegant style.",
       reputation_narrative="Aigiokeros is among Goumenissa's most acclaimed boutique producers; elegant, food-friendly blends at accessible prices.",
       price_positioning="mid_range")
p2 = P("Chatzivariti Estate", "winery", r, "Greece",
       production_philosophy="sustainable",
       philosophy_description="Family estate with the oldest Goumenissa vines; traditional oak aging; Negoska adds a distinctive rounded quality to the blend; wines of local character and food affinity.",
       reputation_narrative="The reference estate for old-vine Goumenissa; Chatzivariti shows the PDO's potential when yields are controlled and traditional methods employed.",
       price_positioning="mid_range")
pr1, n1 = PROD("Aigiokeros Goumenissa Reserve", "wine_still", p1, r, "Greece",
               subcategory="Xinomavro Negoska", price_tier="mid_range",
               description="Oak-aged Xinomavro-Negoska blend; cherry, dried herb, earth, mild tannins and an elegant, savory finish; more approachable than Naoussa with good complexity.")
if n1:
    PAIR(pr1, "Grilled lamb kebabs with oregano and lemon", "complement", "classic", "main", "Greek regional pairing; earthy-cherry wine echoes lamb spice; oregano bridges herb notes.")
    PAIR(pr1, "Moussaka with béchamel and cinnamon", "complement", "classic", "main", "Classic Greek pairing; wine's earthy character mirrors spiced meat and cinnamon.")
    PAIR(pr1, "Grilled halloumi with roasted peppers", "complement", "established", "starter", "Savory wine suits grilled halloumi; dried herb notes echo roasted pepper sweetness.")
    PAIR(pr1, "Slow-braised lamb with tomatoes and herbs", "complement", "established", "main", "Northern Greek lamb tradition; wine's structure and cherry suit slow-braised richness.")
pr2, n2 = PROD("Chatzivariti Goumenissa", "wine_still", p2, r, "Greece",
               subcategory="Xinomavro Negoska", price_tier="mid_range",
               description="Traditional old-vine Goumenissa; sour cherry, dried tomato, thyme, leather and soft tannins from Negoska's rounding influence; expressive, earthy and food-friendly.")
if n2:
    PAIR(pr2, "Pastitsio (Greek lasagne with cinnamon)", "complement", "classic", "main", "Greek comfort food pairing; wine's earthy cherry mirrors spiced meat sauce; Negoska softness suits béchamel.")
    PAIR(pr2, "Grilled whole sea bream with capers and tomato", "complement", "established", "fish_course", "Light earthy red suits sea bream; capers bridge salinity; tomato echoes wine's dried tomato note.")
    PAIR(pr2, "Braised rabbit with olives and rosemary", "complement", "suggested", "main", "Earthy-herb wine suits delicate rabbit; olives and rosemary bridge Mediterranean character.")
    PAIR(pr2, "Aged graviera cheese with dried figs", "complement", "suggested", "cheese", "Greek regional pairing; cherry and dried herb echo aged graviera; figs bridge fruit notes.")

# ── Region 3: Commandaria ─────────────────────────────────────────────────────
print("=== Region 3: Commandaria ===")
r = R("Commandaria", "Cyprus", "wine",
      designation_type="PDO", designation_name="Commandaria PDO",
      reputation_tier="prestigious", quality_trajectory="rediscovering",
      description="Cyprus's ancient sweet wine; Xynisteri and Mavro grapes sun-dried before fermentation; aged by solera; one of the world's oldest continuously produced wines; amber, rich and extraordinarily complex.",
      key_producers="KEO, Loel, SODAP, Tsiakkas",
      historical_context="Commandaria is named after the Knights Hospitallers who ruled Cyprus in the 12th century; Richard the Great called it 'the wine of kings'; produced since at least 800 BC.")
VIN(r, 2020, "excellent", "stable", "Good year for both Xynisteri and Mavro; concentrated sun-dried fruit of great sweetness.")
VIN(r, 2019, "exceptional", "rising", "Ideal conditions; Commandaria of outstanding sweetness, acidity and aging potential.")
VIN(r, 2018, "very_good", "stable", "Classic Commandaria profile; balanced sweetness and acidity from sun-dried grapes.")
VIN(r, 2017, "very_good", "stable", "Good concentration; rich amber wine with characteristic dried-fruit depth.")
VIN(r, 2016, "excellent", "stable", "Well-balanced year; Commandaria of fine complexity and persistent finish.")
p1 = P("Tsiakkas Winery", "winery", r, "Cyprus",
       production_philosophy="traditional",
       philosophy_description="Mountain winery near Troodos; boutique Commandaria producer alongside still wines from indigenous varieties; traditional sun-drying and extended barrel aging.",
       reputation_narrative="One of Cyprus's leading quality producers; Tsiakkas Commandaria is among the most praised modern interpretations of this ancient wine.",
       price_positioning="mid_range")
p2 = P("Kyperounda Winery", "winery", r, "Cyprus",
       production_philosophy="terroir_focused",
       philosophy_description="High-altitude Troodos winery (1350m); uses indigenous Xynisteri for both dry and sweet wines; Commandaria from estate-grown grapes; focused and aromatic.",
       reputation_narrative="Kyperounda produces Cyprus's most aromatic dry Xynisteri and a refined, modern-style Commandaria of unusual elegance.",
       price_positioning="mid_range")
pr1, n1 = PROD("Tsiakkas Commandaria", "wine_dessert", p1, r, "Cyprus",
               subcategory="Xynisteri Mavro blend", price_tier="mid_range",
               description="Traditional amber Commandaria; sun-dried Xynisteri and Mavro; dried fig, raisin, carob, honey, orange peel and extraordinary length; an ancient wine of rare complexity.")
if n1:
    PAIR(pr1, "Baklava with pistachio and rosewater syrup", "complement", "classic", "dessert", "Cyprus classic pairing; wine's dried fruit and honey mirror baklava sweetness; rosewater bridges.")
    PAIR(pr1, "Aged Halloumi with dried figs and almonds", "complement", "classic", "cheese", "Cypriot regional pairing; wine's amber complexity and dried fruit mirror aged halloumi.")
    PAIR(pr1, "Dark chocolate and carob mousse", "complement", "established", "dessert", "Carob note in wine mirrors carob dessert; dried fruit sweetness elevates dark chocolate.")
    PAIR(pr1, "Foie gras terrine with fig jam", "elevate", "adventurous", "starter", "Sweet wine's acidity and dried fruit balance foie richness; fig jam echoes wine's figs.")
pr2, n2 = PROD("Kyperounda Petritis Xynisteri", "wine_still", p2, r, "Cyprus",
               subcategory="Xynisteri", price_tier="mid_range",
               description="High-altitude dry Xynisteri from Troodos; floral, mineral and precise — jasmine, citrus blossom, green herb and a refreshing Alpine-like acidity; Cyprus's finest dry white.")
if n2:
    PAIR(pr2, "Grilled sea bass with lemon and capers", "complement", "established", "fish_course", "Mountain freshness meets coastal fish; citrus blossom echoes lemon; mineral mirrors sea character.")
    PAIR(pr2, "Fattoush salad with herbs and pomegranate", "complement", "suggested", "starter", "Floral-citrus wine echoes fresh herb salad; pomegranate bridges wine's sweet mineral note.")
    PAIR(pr2, "Grilled halloumi with watermelon and mint", "complement", "classic", "starter", "Classic Cypriot pairing; wine's freshness and floral notes echo mint and watermelon.")
    PAIR(pr2, "Mezze spread with hummus, tzatziki and flatbreads", "complement", "classic", "aperitif", "Mediterranean aperitif pairing; mineral white suits dips and flatbreads perfectly.")

# ── Region 4: Vin de Savoie ──────────────────────────────────────────────────
print("=== Region 4: Vin de Savoie ===")
r = R("Vin de Savoie", "France", "wine",
      designation_type="AOC", designation_name="Vin de Savoie AOC",
      reputation_tier="overlooked", quality_trajectory="ascending",
      description="Alpine French wine region between Annecy and Chambéry; Jacquère, Chasselas, Mondeuse and Altesse produce wines of herbal freshness, mineral precision and remarkable alpine character.",
      key_producers="André Quénard, Louis Magnin, Domaine Dupasquier, Domaine des Ardoisières",
      historical_context="Savoie's alpine wines were once more famous than Burgundy; phylloxera, then world wars, reduced the region to near-obscurity; a new generation is reviving its reputation.")
VIN(r, 2022, "very_good", "stable", "Good alpine year; Jacquère of notable freshness and floral character.")
VIN(r, 2021, "excellent", "stable", "Cool year; mineral, precise alpine whites and structured Mondeuse.")
VIN(r, 2020, "excellent", "stable", "Warm but mountain freshness preserved; Jacquère and Altesse of depth.")
VIN(r, 2019, "very_good", "stable", "Classic Savoie profile; food-friendly whites and elegant Mondeuse.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; generous Mondeuse with good tannin and fruit.")
p1 = P("Domaine des Ardoisières", "winery", r, "France",
       production_philosophy="biodynamic",
       philosophy_description="Brice Omont's revival of the Cevins schist terroir (abandoned for 50 years); biodynamic; indigenous varieties including Mondeuse Blanche, Persan and Verdesse; natural wines of great character.",
       reputation_narrative="The most exciting producer in modern Savoie; Ardoisières' rediscovered schist vineyards produce France's most surprising alpine wines.",
       price_positioning="mid_range")
p2 = P("André et Michel Quénard", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Multi-generational Chignin estate; Bergeron (Roussanne) from south-facing limestone is their landmark white; Mondeuse Vieilles Vignes from century-old vines.",
       reputation_narrative="The definitive Chignin estate; Quénard's Bergeron is Savoie's most respected white and one of France's great overlooked Roussannes.",
       price_positioning="mid_range")
pr1, n1 = PROD("Domaine des Ardoisières Schiste Blanc", "wine_still", p1, r, "France",
               subcategory="Jacquère blend", price_tier="mid_range",
               description="Biodynamic white blend from rediscovered schist terroir; Jacquère, Roussette and Mondeuse Blanche; electric mineral energy, wild herbs, citrus blossom and stony precision.")
if n1:
    PAIR(pr1, "Fera du Lac meunière (Lake Geneva whitefish)", "complement", "classic", "fish_course", "Alpine lake classic; mineral-herbal wine mirrors delicate lake fish; butter echoes wine's texture.")
    PAIR(pr1, "Fondue Savoyarde with Abondance and Comté", "complement", "classic", "main", "Definitive Savoie fondue pairing; mineral acidity cuts rich cheese; herbal notes amplify.")
    PAIR(pr1, "Raclette with mountain potatoes and charcuterie", "complement", "established", "main", "Alpine classic; wine's acidity cuts melted cheese; wild herb notes echo mountain character.")
    PAIR(pr1, "Smoked trout pâté with cornichons", "complement", "suggested", "starter", "Mineral energy echoes smoked fish; citrus blossom bridges herb cream; acidity refreshes.")
pr2, n2 = PROD("André Quénard Chignin Bergeron Roussanne", "wine_still", p2, r, "France",
               subcategory="Roussanne", price_tier="mid_range",
               description="Savoie's most celebrated white; south-facing limestone Bergeron Roussanne; apricot, white truffle, almond, wild honey and a remarkable length that develops with age.")
if n2:
    PAIR(pr2, "Gratin Dauphinois with cream and Gruyère", "complement", "classic", "main", "Alpine cream and potato dish; wine's apricot and almond bridge cream richness.")
    PAIR(pr2, "Whole roasted chicken with morel cream sauce", "complement", "established", "main", "Truffle-almond register echoes morel earthiness; apricot bridges cream sauce richness.")
    PAIR(pr2, "Scallops in white wine and cream with herbs", "complement", "suggested", "fish_course", "Roussanne's apricot and texture mirrors scallop sweetness; cream bridges richness.")
    PAIR(pr2, "Aged Abondance cheese with mountain honey", "complement", "classic", "cheese", "Regional pairing; wine's almond and honey echo aged alpine cheese; apricot bridges.")

# ── Region 5: Bergerac ───────────────────────────────────────────────────────
print("=== Region 5: Bergerac ===")
r = R("Bergerac", "France", "wine",
      designation_type="AOC", designation_name="Bergerac AOC",
      reputation_tier="overlooked", quality_trajectory="ascending",
      description="Dordogne river appellation east of Bordeaux; Cabernet Sauvignon, Merlot and Semillon in Bordeaux varieties; Pécharmant (red) and Monbazillac (sweet) are its finest sub-appellations.",
      key_producers="Château Tirecul la Gravière, Domaine de l'Ancienne Cure, Château Tour des Gendres",
      historical_context="Bergerac wines were famously sold as Bordeaux when river access allowed; post-1776, when Bordeaux merchants enforced their monopoly, Bergerac's reputation suffered for two centuries.")
VIN(r, 2022, "excellent", "stable", "Good Dordogne year; structured Pécharmant reds and rich Monbazillac.")
VIN(r, 2021, "very_good", "stable", "Cooler year; elegant, food-friendly reds; Monbazillac showed fine botrytis.")
VIN(r, 2020, "excellent", "rising", "Outstanding vintage; Pécharmant of Bordeaux quality; Monbazillac extraordinary.")
VIN(r, 2019, "very_good", "stable", "Classic year; generous reds and complex sweet whites.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; accessible Bergerac reds and rich Monbazillac.")
p1 = P("Domaine de l'Ancienne Cure", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Christian Roche's biodynamic-transitioning estate; L'Abbaye de Pécharmant is their prestige red; Jour de Fruit Monbazillac from botrytised Semillon.",
       reputation_narrative="L'Ancienne Cure is Bergerac's most acclaimed modern estate; Pécharmant showing Bordeaux-rival quality at a fraction of the price.",
       price_positioning="mid_range")
p2 = P("Château Tour des Gendres", "winery", r, "France",
       production_philosophy="natural",
       philosophy_description="de Conti family; certified biodynamic; Moulin des Dames (Semillon white) and Gloire de mon Père (red blend) are their prestige wines; pioneers of Bergerac's quality revolution.",
       reputation_narrative="Tour des Gendres and the late Luc de Conti proved Bergerac could produce serious, age-worthy wines of genuine terroir expression.",
       price_positioning="mid_range")
pr1, n1 = PROD("Ancienne Cure L'Abbaye Pécharmant Rouge", "wine_still", p1, r, "France",
               subcategory="Cabernet Sauvignon Merlot", price_tier="mid_range",
               description="Prestige Pécharmant from biodynamic vines; Cabernet Sauvignon-led; blackcurrant, cedar, tobacco and firm tannins with a long Bordeaux-like finish; excellent value.")
if n1:
    PAIR(pr1, "Confit de canard with sarladaise potatoes", "complement", "classic", "main", "Southwest French regional classic; wine's cedar and dark fruit mirror duck confit richness.")
    PAIR(pr1, "Rack of lamb with herbed crust and red wine jus", "complement", "established", "main", "Bordeaux-style pairing; cassis and cedar suit lamb; herbed crust bridges herb notes.")
    PAIR(pr1, "Foie gras mi-cuit with fig and black pepper", "complement", "established", "starter", "Périgord pairing; wine's structure bridges foie richness; fig echoes dark fruit.")
    PAIR(pr1, "Truffled brie de Meaux with toasted walnuts", "complement", "suggested", "cheese", "Dordogne regional pairing; cedar and cassis suit rich brie; truffle bridges earthiness.")
pr2, n2 = PROD("Tour des Gendres Moulin des Dames Blanc", "wine_still", p2, r, "France",
               subcategory="Semillon blend", price_tier="mid_range",
               description="Biodynamic Semillon-Sauvignon Blanc-Muscadelle blend; barrel-fermented; beeswax, lanolin, lemon curd and toasted hazelnut; textured, complex and age-worthy; rivals many white Bordeaux.")
if n2:
    PAIR(pr2, "Oysters from Arcachon Bay with mignonette", "complement", "classic", "aperitif", "Dordogne-coast pairing; barrel-textured Semillon suits oyster richness; acidity amplifies brine.")
    PAIR(pr2, "Pan-roasted scallops with cauliflower purée and hazelnut", "complement", "established", "fish_course", "Toasted hazelnut in wine echoes hazelnut garnish; beeswax and scallop sweetness align.")
    PAIR(pr2, "Terrine de foie gras with Sauternes aspic", "complement", "classic", "starter", "Périgord classic; Semillon beeswax and lemon cut foie richness; aspic bridges wine's structure.")
    PAIR(pr2, "Roast chicken with tarragon and cream", "complement", "established", "main", "Barrel texture matches cream; lemon curd and beeswax echo tarragon's anise character.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
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
