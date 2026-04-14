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

# ── Batch 72 ──────────────────────────────────────────────────────────────────
# Regions: Nemea, Dalmatia, Istria, Lugana, Franciacorta

# ── Region 1: Nemea ───────────────────────────────────────────────────────────
print("\n=== Region 1: Nemea ===")
r1 = R("Nemea", "Greece", "wine",
    designation_type="PDO",
    designation_name="Nemea PDO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Greece's most important red wine appellation in the northern Peloponnese, producing powerful yet elegant wines from the Agiorgitiko (St. George) grape — dubbed 'the Blood of Hercules'.",
    key_producers="Gaia Wines, Papaioannou, Semeli Estate, Skouras",
    historical_context="Nemea is ancient — wine was produced here before the Nemean Games of antiquity; Agiorgitiko is one of Greece's oldest and noblest indigenous varieties."
)
VIN(r1, 2021, "excellent", "rising", "Ideal Mediterranean vintage; Agiorgitiko shows superb ripe fruit, refined tannins and exceptional freshness.")
VIN(r1, 2020, "very_good", "stable", "Balanced season with good concentration and structure; excellent for medium-term ageing.")
VIN(r1, 2019, "good", "stable", "Slightly warm year; generous, approachable wines with immediate drinking pleasure.")
VIN(r1, 2018, "excellent", "rising", "Outstanding vintage for both rosé and structured red Nemea; wines of remarkable complexity.")
VIN(r1, 2017, "very_good", "stable", "Consistent quality across the appellation; Agiorgitiko shows its characteristic plum and spice.")

p1a = P("Gaia Wines", "winery", r1, "Greece",
    production_philosophy="terroir_expression",
    philosophy_description="Pioneering Nemea estate producing both single-vineyard serious Agiorgitiko and innovative approachable styles that helped define modern Greek wine.",
    reputation_narrative="Gaia's Notios and Agiorgitiko by Gaia labels are among Greece's most globally distributed premium wines; the estate set the standard for Nemea quality.",
    price_positioning="premium")
prod1a, new1a = PROD("Gaia Wines Agiorgitiko by Gaia", "wine_still", p1a, r1, "Greece",
    subcategory="Agiorgitiko",
    description="Benchmark Nemea Agiorgitiko — ripe plum, morello cherry, rose petal, clove and velvety tannins with Mediterranean warmth and vibrant acidity.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Moussaka with béchamel and spiced lamb", "complement", "classic", "main", "Greece's national dish with Greece's national red — lamb's spice and the wine's plum are natural partners.")
    PAIR(prod1a, "Lamb souvlaki with pita, tzatziki and tomato", "complement", "classic", "main", "Grilled lamb and Agiorgitiko is the quintessential Greek pairing; tzatziki cools both.")
    PAIR(prod1a, "Beef stifado (slow-cooked with pearl onions and cinnamon)", "complement", "established", "main", "Cinnamon-spiced stew resonates with Agiorgitiko's warm clove and plum character.")
    PAIR(prod1a, "Graviera cheese with honey and walnut", "bridge", "suggested", "cheese", "Greek hard cheese and indigenous red; honey bridges the fruit, walnut adds earthy weight.")

p1b = P("Papaioannou Winery", "winery", r1, "Greece",
    production_philosophy="terroir_expression",
    philosophy_description="Family estate producing some of Nemea's most elegant and age-worthy Agiorgitiko, with a particular focus on old-vine single-vineyard expressions.",
    reputation_narrative="Papaioannou's Palea Klimata old-vine Agiorgitiko is considered Nemea's most distinguished and age-worthy single-vineyard wine.",
    price_positioning="premium")
prod1b, new1b = PROD("Papaioannou Palea Klimata Agiorgitiko", "wine_still", p1b, r1, "Greece",
    subcategory="Agiorgitiko",
    description="Old-vine Nemea Agiorgitiko of great complexity — dark cherry, dried herbs, leather, warm spice and firm, well-integrated tannins with excellent ageing potential.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Braised lamb shanks with tomato, garlic and herbs (kleftiko)", "complement", "classic", "main", "Rich slow-braised lamb matches the wine's depth and structure perfectly.")
    PAIR(prod1b, "Venison stew with juniper and dark cherry", "complement", "established", "main", "Game meat's iron and herbs mirror the wine's leather and spice; dark cherry echoes its fruit.")
    PAIR(prod1b, "Stuffed red peppers with rice and minced lamb", "complement", "established", "main", "Herb-seasoned stuffed peppers amplify the wine's dried herb and warm spice character.")
    PAIR(prod1b, "Aged Kefalotyri cheese with dried figs", "bridge", "established", "cheese", "Hard salty Greek cheese mirrors the wine's firm structure; dried fig bridges the fruit profile.")

# ── Region 2: Dalmatia ────────────────────────────────────────────────────────
print("\n=== Region 2: Dalmatia ===")
r2 = R("Dalmatia", "Croatia", "wine",
    designation_type="PGI",
    designation_name="Dalmatinska vina",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Croatia's Adriatic coastal wine region producing bold red Plavac Mali (believed ancestor of California Zinfandel), crisp Pošip white and rosé; island vineyards including Hvar, Brač and Korčula.",
    key_producers="Miloš, Zlatan Otok, Korta Katarina, Grgić Vina, Saints Hills",
    historical_context="Dalmatia is one of the oldest wine regions in the world; DNA research proved Plavac Mali is the parent variety of Zinfandel/Primitivo, connecting Croatia to California's most characterful grape."
)
VIN(r2, 2022, "very_good", "rising", "Excellent Adriatic vintage; Plavac Mali shows deep colour and ripe fruit with good structure.")
VIN(r2, 2021, "good", "stable", "Consistent quality; whites particularly expressive with coastal mineral character.")
VIN(r2, 2020, "excellent", "rising", "Outstanding year for Dalmatian reds; Plavac Mali of remarkable concentration and ageing potential.")
VIN(r2, 2019, "very_good", "stable", "Balanced Mediterranean season; wines show the archipelago's distinctive brine and herb character.")
VIN(r2, 2018, "good", "stable", "Good quality with approachable fruit expression; Pošip particularly successful.")

p2a = P("Miloš Winery", "winery", r2, "Croatia",
    production_philosophy="terroir_expression",
    philosophy_description="Pelješac Peninsula estate producing some of Dalmatia's most serious and age-worthy Plavac Mali from old steep terraced vineyards.",
    reputation_narrative="Miloš Plavac Mali Grand Cru is considered Croatia's finest expression of the variety; the steep coastal terraces give wines of exceptional depth and mineral character.",
    price_positioning="premium")
prod2a, new2a = PROD("Miloš Plavac Mali Grand Cru", "wine_still", p2a, r2, "Croatia",
    subcategory="Plavac Mali",
    description="Dalmatia's benchmark Plavac Mali from Pelješac — blackberry, dried fig, smoked meat, Mediterranean herbs and sea salt with powerful but polished tannins.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Grilled Dalmatian lamb with rosemary and sea salt (janjetina)", "complement", "classic", "main", "Croatian lamb from the same landscape as the wine — herbs, brine and dark fruit in perfect alignment.")
    PAIR(prod2a, "Octopus slow-cooked under a peka (bell lid)", "bridge", "adventurous", "main", "Traditional Dalmatian method; smoky octopus and powerful red wine bridge coastal and inland flavours.")
    PAIR(prod2a, "Wild boar sausage with rosemary and juniper", "complement", "established", "main", "Gamey boar sausage with wild herbs aligns with the wine's Mediterranean herb and smoked meat character.")
    PAIR(prod2a, "Aged Paški sir (Pag Island sheep cheese)", "complement", "established", "cheese", "Croatia's most celebrated cheese with Croatia's finest red — salty, firm and harmonious.")

p2b = P("Korta Katarina", "winery", r2, "Croatia",
    production_philosophy="terroir_expression",
    philosophy_description="Modern Pelješac estate producing elegant Pošip white and Plavac Mali red with investment in quality that has helped elevate Dalmatian wine's international profile.",
    reputation_narrative="Korta Katarina is one of Dalmatia's most export-driven estates; their Pošip is one of Croatia's finest indigenous whites.",
    price_positioning="premium")
prod2b, new2b = PROD("Korta Katarina Pošip", "wine_still", p2b, r2, "Croatia",
    subcategory="Pošip",
    description="Elegant Korčula Island Pošip — peach, almond, Mediterranean herb, lemon curd and a saline coastal mineral finish with excellent food-friendly acidity.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Grilled Adriatic sea bass with lemon and olive oil", "complement", "classic", "main", "Coastal white wine with coastal fish — lemon and olive oil bridge the wine's herb and citrus notes.")
    PAIR(prod2b, "Black truffle and egg pappardelle (Istrian style)", "bridge", "established", "main", "Pošip's almond and herb notes create a bridge to truffle; egg pasta richness aligns with its weight.")
    PAIR(prod2b, "Dalmatian prosciutto with figs and melon", "complement", "established", "starter", "Cured coastal pork and stone fruit mirror the wine's peach and mineral character.")
    PAIR(prod2b, "Grilled cuttlefish with black risotto (crni rižot)", "bridge", "adventurous", "main", "Croatian coastal classic; cuttlefish ink's brine aligns with Pošip's saline finish.")

# ── Region 3: Istria ──────────────────────────────────────────────────────────
print("\n=== Region 3: Istria ===")
r3 = R("Istria", "Croatia", "wine",
    designation_type="PGI",
    designation_name="Istarska vina",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Croatia's Adriatic peninsula bordering Italy and Slovenia, known for Malvazija Istarska (Malvasia Istriana), Teran red and some of Europe's finest white truffles grown alongside the vineyards.",
    key_producers="Kozlović, Moreno Coronica, Clai, Trapan, Kabola",
    historical_context="Istria's Malvazija has been cultivated since Roman times; the region's white truffle and wine culture are inseparable, making it one of the most celebrated food-wine destinations in the Adriatic."
)
VIN(r3, 2022, "excellent", "rising", "Ideal Istrian season; Malvazija shows striking aromatic intensity and mineral freshness.")
VIN(r3, 2021, "very_good", "stable", "Good quality; wines express the peninsula's characteristic aromatic and textural profile.")
VIN(r3, 2020, "good", "stable", "Consistent vintage; reliable Malvazija with peach and almond character.")
VIN(r3, 2019, "excellent", "rising", "Outstanding vintage for both Malvazija and Teran; wines of notable complexity.")
VIN(r3, 2018, "very_good", "stable", "Balanced Mediterranean season; wines show food-friendly acidity and mineral precision.")

p3a = P("Kozlović Winery", "winery", r3, "Croatia",
    production_philosophy="terroir_expression",
    philosophy_description="Leading Istrian producer crafting benchmark Malvazija and Teran from coastal and red-soil vineyard sites with a strong focus on indigenous variety expression.",
    reputation_narrative="Kozlović Santa Lucia Malvazija is Istria's most celebrated white wine, consistently earning top ratings for its balance, complexity and food affinity.",
    price_positioning="premium")
prod3a, new3a = PROD("Kozlović Santa Lucia Malvazija", "wine_still", p3a, r3, "Croatia",
    subcategory="Malvazija Istarska",
    description="Istria's benchmark Malvazija — white peach, almond, chamomile, beeswax and a distinctive mineral-salty finish; textured, aromatic and distinctively Croatian.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Fresh white truffle shaved over tagliatelle with butter", "complement", "classic", "main", "The truffle-and-Malvazija pairing is Istria's culinary signature; almond and truffle amplify each other.")
    PAIR(prod3a, "Grilled Adriatic sea bream with wild herbs", "complement", "classic", "fish_course", "Coastal white wine with coastal fish; herb notes in wine and dish align perfectly.")
    PAIR(prod3a, "Asparagus risotto with Parmesan and lemon", "complement", "established", "main", "The wine's almond and chamomile notes resonate with asparagus; lemon bridges the acidity.")
    PAIR(prod3a, "Istrian prosciutto (pršut) with fresh figs", "complement", "established", "starter", "Cured Istrian meat with Istrian wine is the quintessential local pairing.")

p3b = P("Clai Bijele Zemlje", "winery", r3, "Croatia",
    production_philosophy="biodynamic",
    philosophy_description="Istria's most individualistic producer making amber-style skin-contact Malvazija and minimal-intervention Teran with strong biodynamic farming principles.",
    reputation_narrative="Clai's Sv. Jakov skin-contact Malvazija has earned a global cult following among natural wine enthusiasts for its complexity and distinctive amber character.",
    price_positioning="premium")
prod3b, new3b = PROD("Clai Sv. Jakov Malvazija", "wine_still", p3b, r3, "Croatia",
    subcategory="Malvazija Istarska",
    description="Skin-contact amber Malvazija — dried apricot, chamomile tea, walnut, orange peel and tannin from maceration; complex, textural and distinctively Istrian in character.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Roasted pork with fennel, garlic and rosemary", "complement", "established", "main", "Tannin from skin contact handles the pork fat; fennel and herbs bridge the wine's chamomile note.")
    PAIR(prod3b, "Aged Pecorino with chestnut honey", "bridge", "established", "cheese", "Hard ewes' milk and orange-amber wine; chestnut honey bridges tannin and dried fruit.")
    PAIR(prod3b, "Grilled lamb chops with za'atar crust", "complement", "adventurous", "main", "The wine's tannin and dried herb character can handle lamb; za'atar mirrors its aromatic complexity.")
    PAIR(prod3b, "Charcuterie and vegetable mezze (antipasto)", "complement", "suggested", "starter", "Amber wine's tannic structure and acidity make it ideal for a broad spread of antipasto.")

# ── Region 4: Lugana DOC ──────────────────────────────────────────────────────
print("\n=== Region 4: Lugana ===")
r4 = R("Lugana", "Italy", "wine",
    designation_type="DOC",
    designation_name="Lugana DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Small DOC on the southern shore of Lake Garda in Lombardy and Veneto, producing Italy's finest expressions of Trebbiano di Lugana (Turbiana) — floral, textured and minerally distinctive.",
    key_producers="Zenato, Ca' dei Frati, Cà Maiol, Ottella, Pasini San Giovanni",
    historical_context="Lugana is one of northern Italy's best-kept secrets; the unique Turbiana grape grown on glacially-deposited clay soils around Lake Garda produces wines of extraordinary complexity and ageing potential."
)
VIN(r4, 2022, "excellent", "rising", "Lake Garda's moderating influence created ideal conditions; Turbiana of extraordinary aromatic definition.")
VIN(r4, 2021, "very_good", "stable", "Balanced vintage; wines show floral character and food-friendly acidity.")
VIN(r4, 2020, "good", "stable", "Consistent quality; approachable whites with stone fruit and almond.")
VIN(r4, 2019, "excellent", "rising", "Benchmark Lugana vintage; wines of exceptional concentration and mineral drive.")
VIN(r4, 2018, "very_good", "stable", "Good overall; Lugana Superiore from this vintage is developing beautifully.")

p4a = P("Ca' dei Frati", "winery", r4, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Lugana's most celebrated producer, crafting the benchmark I Frati Lugana and the singular late-harvest Tre Filer from pure Turbiana on Lake Garda's glacial clay soils.",
    reputation_narrative="Ca' dei Frati I Frati Lugana is Italy's reference point for the Turbiana variety; the estate defines Lugana's international reputation.",
    price_positioning="mid_range")
prod4a, new4a = PROD("Ca' dei Frati I Frati Lugana", "wine_still", p4a, r4, "Italy",
    subcategory="Turbiana",
    description="Italy's benchmark Lugana — white flower, almond, lemon, hay, subtle mineral and an elegant lingering finish; unoaked and expressive of Lake Garda's unique terroir.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Lake Garda whitefish in carpione (marinated in vinegar and aromatics)", "complement", "classic", "fish_course", "Regional pairing: Lake Garda fish with Lake Garda wine; the vinegar marinade bridges the wine's acidity.")
    PAIR(prod4a, "Grilled Dover sole with brown butter and capers", "complement", "established", "fish_course", "Delicate fish and textured white; butter aligns with Lugana's richness, capers with its mineral drive.")
    PAIR(prod4a, "Risotto di lago (freshwater fish risotto)", "complement", "classic", "main", "Northern Italian lake-fish risotto and Lugana is the definitive terroir-match of the region.")
    PAIR(prod4a, "Taleggio cheese with pear and walnut", "bridge", "suggested", "cheese", "Washed-rind cheese's pungency is tamed by Lugana's floral freshness; pear bridges fruit and acidity.")

p4b = P("Zenato Winery", "winery", r4, "Italy",
    production_philosophy="traditional",
    philosophy_description="Multi-generational family estate spanning Lugana and Valpolicella, producing some of the region's most reliable and age-worthy Lugana alongside impressive Amarone.",
    reputation_narrative="Zenato Lugana Superiore is consistently considered one of the appellation's finest age-worthy whites; the estate is equally celebrated in both Lugana and Amarone.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Zenato Lugana Superiore", "wine_still", p4b, r4, "Italy",
    subcategory="Turbiana",
    description="Lugana Superiore aged 9 months on lees — richer, more complex expression with dried citrus, almond, beeswax and textural depth; can age 5–8 years.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Roasted chicken with sage, lemon and garlic (pollo alla salvia)", "complement", "established", "main", "Classic northern Italian preparation; sage echoes the wine's aromatic herbal notes.")
    PAIR(prod4b, "Creamy burrata with roasted peach and basil", "complement", "suggested", "starter", "Stone fruit and almond in the wine mirror peach; burrata richness aligns with the wine's lees texture.")
    PAIR(prod4b, "Bresaola with rocket, Parmigiano and lemon", "complement", "established", "starter", "Lean cured beef and mineral white; lemon in the dish mirrors the wine's citrus drive.")
    PAIR(prod4b, "Grilled swordfish with caponata", "bridge", "suggested", "main", "Meaty fish can handle the wine's weight; caponata's sweet-sour bridges the wine's acidity.")

# ── Region 5: Franciacorta DOCG ───────────────────────────────────────────────
print("\n=== Region 5: Franciacorta ===")
r5 = R("Franciacorta", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Franciacorta DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Italy's premier traditional-method sparkling wine appellation in Lombardy, producing Chardonnay, Pinot Nero and Pinot Bianco sparkling wines with complexity and age-worthiness rivalling Champagne.",
    key_producers="Ca' del Bosco, Bellavista, Berlucchi, Contadi Castaldi, Monte Rossa",
    historical_context="Franciacorta received DOCG status in 1995 and has emerged as Italy's answer to Champagne; the use of 'Franciacorta' alone (without method description) is reserved exclusively for this prestige sparkling appellation."
)
VIN(r5, 2019, "exceptional", "rising", "Benchmark vintage for Franciacorta; wines of extraordinary depth, tension and ageing potential.")
VIN(r5, 2018, "excellent", "rising", "Outstanding growing season; exceptional Chardonnay that has produced wines of great complexity.")
VIN(r5, 2017, "very_good", "stable", "Good vintage; wines show the region's characteristic richness and persistent mousse.")
VIN(r5, 2016, "excellent", "rising", "Near-perfect Franciacorta vintage; wines of Champagne-like precision and finesse.")
VIN(r5, 2015, "good", "stable", "Warm year; generous, full-bodied Franciacorta with immediate appeal.")

p5a = P("Ca' del Bosco", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Maurizio Zanella's landmark Franciacorta estate that pioneered the appellation's ascent to world-class status; the Annamaria Clementi prestige cuvée is Italy's finest traditional-method wine.",
    reputation_narrative="Ca' del Bosco is universally recognised as Franciacorta's leading estate; Annamaria Clementi is Italy's most celebrated sparkling wine.",
    price_positioning="ultra_premium")
prod5a, new5a = PROD("Ca' del Bosco Annamaria Clementi", "wine_sparkling", p5a, r5, "Italy",
    subcategory="Blanc de Blancs style Franciacorta",
    description="Italy's greatest traditional-method sparkling wine: Chardonnay, Pinot Nero and Pinot Bianco aged 8+ years on lees — brioche, dried citrus, almond, chalk and extraordinary bubble finesse.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Osso buco with gremolata and saffron risotto", "complement", "classic", "main", "Franciacorta's most celebratory pairing with Lombardy's most iconic dish; gremolata bridges the wine's citrus.")
    PAIR(prod5a, "Seared scallops with cauliflower purée and truffle", "complement", "classic", "fish_course", "Scallop sweetness and Franciacorta richness; truffle aligns with the wine's autolytic depth.")
    PAIR(prod5a, "Caviar with crème fraîche and blini", "complement", "classic", "aperitif", "The world's most luxurious aperitif combination; salt, richness and fine bubbles in perfect balance.")
    PAIR(prod5a, "Aged Parmigiano-Reggiano with a drizzle of aged balsamic", "complement", "classic", "cheese", "Lombardy-Emilia crossover: Parmigiano's crystal granules and aged balsamic mirror Franciacorta's depth.")

p5b = P("Bellavista", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Premier Franciacorta estate under Vittorio Moretti, producing exceptional vintage Satèn and Pas Operé sparkling wines of consistent prestige.",
    reputation_narrative="Bellavista's Victoria and Alma Grande Cuvée are among Italy's most acclaimed traditional-method sparkling wines; the estate is Franciacorta's most internationally recognised name.",
    price_positioning="premium")
prod5b, new5b = PROD("Bellavista Satèn Franciacorta", "wine_sparkling", p5b, r5, "Italy",
    subcategory="Satèn Franciacorta",
    description="Franciacorta's most seductive category: pure Chardonnay with lower dosage and gentle pression — creamy, silky bubbles with white flower, fresh brioche, pear and delicate chalk minerality.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Risotto al Franciacorta (Franciacorta sparkling wine risotto)", "complement", "classic", "main", "The wine goes into the dish and onto the table — the ultimate Lombardy self-referential pairing.")
    PAIR(prod5b, "Smoked salmon carpaccio with capers and lemon cream", "complement", "established", "starter", "Silky Satèn texture mirrors salmon fat; capers and lemon bridge the wine's acidity and mineral note.")
    PAIR(prod5b, "Mascarpone and strawberry millefeuille", "complement", "established", "dessert", "Mascarpone richness aligns with Satèn's creamy texture; strawberry and pastry complete the pairing.")
    PAIR(prod5b, "Burrata with San Daniele prosciutto and melon", "complement", "established", "starter", "Creamy burrata and silky bubbles; sweet melon and cured pork contrast the wine's gentle mineral edge.")

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
