#!/usr/bin/env python3
"""B149 — Aglianico del Vulture DOC (IT), Fiano di Avellino DOCG (IT), Greco di Tufo DOCG (IT), Egri Bikavér (HU), Valle de Uco (AR)"""
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

# ── 1. Aglianico del Vulture DOC ─────────────────────────────────────────────
print("=== Aglianico del Vulture DOC ===")
r1 = R("Aglianico del Vulture DOC", "Italy", "wine",
        designation_type="DOC", designation_name="Aglianico del Vulture",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Grown on the volcanic slopes of Mount Vulture in Basilicata, Aglianico del Vulture produces some of southern Italy's most impressive red wines. The Aglianico grape, grown on ancient volcanic soils at 400–700 metres elevation, produces wines of extraordinary structure: massive tannin, high acidity, and profound dark-fruit depth that requires years of ageing to reveal its complexity.",
        key_producers="Paternoster, D'Angelo, Elena Fucci, Cantine del Notaio, Grifalco",
        historical_context="Aglianico is believed to have been introduced to southern Italy by ancient Greek colonists, making it one of the peninsula's oldest cultivated varieties. Wine from the Vulture volcano has been prized since antiquity, and the DOC — established in 1971 — recognised this long tradition. The DOCG upgrade to Aglianico del Vulture Superiore in 2011 acknowledged the region's world-class potential.")

for yr, qd, pt in [
    (2017, "exceptional", "rising"), (2018, "excellent", "rising"), (2019, "exceptional", "rising"),
    (2020, "very_good", "stable"), (2021, "excellent", "rising")]:
    VIN(r1, yr, qd, pt)

p1a = P("Elena Fucci", "winery", r1, "Italy",
         production_philosophy="minimal_intervention",
         philosophy_description="Elena Fucci is the most acclaimed young producer in Basilicata, producing a single Aglianico del Vulture from her family's Titolo vineyard at 600 metres on the volcanic slopes of Mount Vulture. Her minimal intervention approach — indigenous ferments, large-format oak, minimal sulphur — captures Aglianico's full expressive potential.",
         reputation_narrative="Elena Fucci's Titolo has transformed Aglianico del Vulture's international reputation, earning consistent 95+ scores and appearing on the lists of Italy's finest restaurants. Her singular focus on one wine from one vineyard has become a model for Italian terroir expression.",
         price_positioning="premium")

prod1a1, new1 = PROD("Elena Fucci Titolo Aglianico del Vulture", "wine_still", p1a, r1, "Italy",
                      subcategory="Aglianico", price_tier="premium",
                      description="From a single plot at 600 metres on Mount Vulture's volcanic slopes, Titolo is one of southern Italy's greatest red wines: Aglianico of extraordinary depth and precision, with dark cherry, iron, dried herbs, and a mineral backbone that reflects the volcanic pumice soils. Structured to age for 20+ years.")
if new1:
    PAIR(prod1a1, "Slow-braised lamb ragù with handmade pasta and Pecorino", "complement", "classic", "main", "Aglianico's powerful tannin and acidity demand slow-cooked meat; the ragù's collagen richness softens the wine's structure while Pecorino's sharpness bridges the dark fruit with the sauce.")
    PAIR(prod1a1, "Grilled lamb chops with caponata and crusty bread", "complement", "classic", "main", "The volcanic-mineral Aglianico finds its most natural expression with grilled lamb; caponata's sweet-sour-savoury complexity echoes the wine's own layered character while bread absorbs the richness.")
    PAIR(prod1a1, "Wild boar ragù with pappardelle and Parmigiano", "complement", "established", "main", "Titolo's power and dark-fruit concentration demand game meat; wild boar's earthy intensity resonates with the wine's volcanic mineral depth while Parmigiano adds the umami bridge.")
    PAIR(prod1a1, "Aged Pecorino di Filiano with truffle honey and walnut", "complement", "classic", "cheese", "Basilicata's own aged sheep's milk cheese is the natural pairing for Aglianico; truffle honey bridges the wine's iron-mineral depth while walnut echoes its volcanic earthiness.")

prod1a2, new2 = PROD("Elena Fucci Titolo Superiore Aglianico del Vulture", "wine_still", p1a, r1, "Italy",
                      subcategory="Aglianico", price_tier="ultra_premium",
                      description="The reserve expression of Titolo, aged longer in large Slovenian oak botti, displaying the full measure of Aglianico's capacity: darker fruit, more profound mineral complexity, and a tannin architecture that will require a decade minimum to reveal its true character.")
if new2:
    PAIR(prod1a2, "Slow-roasted whole kid goat with herbs and black olives", "complement", "classic", "main", "The Superiore's Nebbiolo-level power demands this most traditional Basilicatan preparation; herbs echo the wine's complex herbaceous character while black olives add Mediterranean depth.")
    PAIR(prod1a2, "Braised oxtail with celery, carrot, and tomato sauce (coda alla vaccinara)", "complement", "established", "main", "The wine's power and complexity parallel the intense preparation of coda alla vaccinara; the braising liquid's acidity bridges the tannin while the collagen-rich tail softens the wine's structure.")
    PAIR(prod1a2, "Aged Canestrato Pugliese with black truffle and local honey", "complement", "established", "cheese", "Southern Italy's oldest DOC cheese matches Aglianico Superiore's power and depth; black truffle deepens the earthy connection while local honey bridges the wine's dark fruit.")
    PAIR(prod1a2, "Charcoal-grilled bistecca with olive oil and rosemary", "complement", "classic", "main", "Southern Italian Aglianico and a thick-cut grilled steak is the region's luxury table pairing; the wine's iron-mineral character resonates with the meat while rosemary echoes its herbal complexity.")

p1b = P("Paternoster", "winery", r1, "Italy",
         production_philosophy="classical",
         philosophy_description="Paternoster is one of the oldest and most established producers in Aglianico del Vulture, with the Antico and Don Anselmo cuvées representing the pinnacle of traditional Basilicatan winemaking with extended oak ageing and long bottle maturation.",
         reputation_narrative="Paternoster's Don Anselmo is one of southern Italy's most age-worthy wines, demonstrating Aglianico del Vulture's capacity for extraordinary longevity. The estate's decades of production have established the benchmark style for the DOC.",
         price_positioning="premium")

prod1b1, new3 = PROD("Paternoster Don Anselmo Aglianico del Vulture", "wine_still", p1b, r1, "Italy",
                      subcategory="Aglianico", price_tier="premium",
                      description="Paternoster's prestige Aglianico, aged three years in small oak barrels, displaying the traditional interpretation of the variety: concentrated dark fruit, leather, tobacco, and volcanic mineral with assertive tannin that mellows slowly over decades in the cellar.")
if new3:
    PAIR(prod1b1, "Roasted leg of lamb with capers, olives, and anchovies", "complement", "established", "main", "Don Anselmo's traditional power finds resonance with this classic southern Italian lamb preparation; capers and anchovies add the salty-umami depth that bridges the wine's mineral character.")
    PAIR(prod1b1, "Braised beef shin with tomato, herbs, and polenta", "complement", "classic", "main", "The wine's structure and dark fruit are ideal for slow-braised beef; the polenta absorbs the sauce's richness while tomato's acidity bridges the wine's own high-acid character.")
    PAIR(prod1b1, "Aged Caciocavallo Podolico with wild fig jam", "complement", "classic", "cheese", "Caciocavallo Podolico — southern Italy's most prized aged cheese — demands a wine of Don Anselmo's standing; wild fig jam bridges the wine's dark fruit while the cheese's stretched-curd character resonates with the volcanic terroir.")
    PAIR(prod1b1, "Lamb sausages with roasted peppers and crusty bread", "complement", "classic", "main", "Traditional Basilicatan sausages and aged Aglianico is the region's defining food pairing; roasted peppers add sweetness that softens the wine's tannin while bread absorbs the intensity.")

prod1b2, new4 = PROD("Paternoster Rotondo Aglianico del Vulture", "wine_still", p1b, r1, "Italy",
                      subcategory="Aglianico", price_tier="mid_range",
                      description="The more approachable expression from Paternoster, with shorter oak ageing, displaying Aglianico's essential character — dark cherry, iron, and volcanic earth — in a slightly softer frame that allows earlier enjoyment without sacrificing the variety's essential structure.")
if new4:
    PAIR(prod1b2, "Pasta al ragù with Italian sausage and Pecorino", "complement", "classic", "main", "Aglianico's acidity and fruit are natural companions for a robust meat sauce; Pecorino's sharpness and the sausage's spice create the savoury depth the wine demands.")
    PAIR(prod1b2, "Grilled pork ribs with chili and herb marinade", "complement", "established", "main", "The wine's accessible structure and dark fruit handle spiced pork with ease; chili's heat amplifies the wine's own warm character while herbs echo its herbal depth.")
    PAIR(prod1b2, "Pizza diavola with spicy salami and mozzarella", "complement", "classic", "casual", "A casual but genuine pairing: Aglianico's acidity cuts through mozzarella's fat while the wine's dark fruit complements the spicy salami's heat.")
    PAIR(prod1b2, "Aged Pecorino Romano with Calabrian chili honey", "complement", "established", "cheese", "The wine's iron and dark cherry character resonate with sharp Pecorino Romano; Calabrian chili honey adds both sweetness and heat that bridge the wine's natural spice.")

# ── 2. Fiano di Avellino DOCG ────────────────────────────────────────────────
print("=== Fiano di Avellino DOCG ===")
r2 = R("Fiano di Avellino DOCG", "Italy", "wine",
        designation_type="DOCG", designation_name="Fiano di Avellino",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Grown in the volcanic hills of Campania's Irpinia zone, Fiano di Avellino produces one of southern Italy's greatest white wines. The ancient Fiano grape, with roots tracing to Roman times, produces wines of extraordinary complexity: honey, hazelnut, dried herbs, and smoky mineral from the volcanic tufa soils, with a natural acidity that allows exceptional ageing for a southern Italian white.",
        key_producers="Feudi di San Gregorio, Mastroberardino, Marisa Cuomo, Villa Raiano, Cantine Lonardo",
        historical_context="Fiano is believed to be one of Italy's most ancient grape varieties, referenced by Pliny the Elder as 'Vitis apiana' (the grape beloved by bees) for the sweetness of its fruit. The variety survived the phylloxera epidemic through its remote Irpinian hillside cultivation and was instrumental in the post-WWII revival of southern Italian fine wine, earning DOCG status in 2003.")

for yr, qd, pt in [
    (2018, "excellent", "rising"), (2019, "exceptional", "rising"), (2020, "very_good", "stable"),
    (2021, "excellent", "rising"), (2022, "very_good", "rising")]:
    VIN(r2, yr, qd, pt)

p2a = P("Feudi di San Gregorio", "winery", r2, "Italy",
         production_philosophy="terroir_expression",
         philosophy_description="Feudi di San Gregorio is Campania's most internationally visible wine estate, producing Fiano di Avellino, Greco di Tufo, and Taurasi from indigenous varieties with world-class consistency. Their Pietracalda Fiano is one of southern Italy's benchmark whites.",
         reputation_narrative="Feudi di San Gregorio has been instrumental in bringing Campanian wine to the international stage, with their Fiano and Greco consistently earning critical acclaim and appearing in the world's finest Italian wine restaurants. Their investment in indigenous varieties has redefined southern Italian winemaking quality.",
         price_positioning="premium")

prod2a1, new5 = PROD("Feudi di San Gregorio Pietracalda Fiano di Avellino", "wine_still", p2a, r2, "Italy",
                      subcategory="Fiano", price_tier="premium",
                      description="Feudi's flagship Fiano, from a single vineyard on volcanic tufa soils in Lapio. Pietracalda (meaning 'hot stone') displays Fiano's full complexity: hazelnut, white peach, honey, dried chamomile, and a smoky volcanic mineral finish of extraordinary length and ageing potential.")
if new5:
    PAIR(prod2a1, "Spaghetti alle vongole with white wine and parsley", "complement", "classic", "main", "Fiano's mineral depth and honey-hazelnut character are a revelation with vongole; the wine's smoky volcanic character bridges the clam's brine while parsley adds the herbaceous note that echoes Fiano's dried-herb complexity.")
    PAIR(prod2a1, "Zuppa di pesce (mixed fish soup) with bruschetta", "complement", "classic", "fish_course", "Southern Italy's white wine standard for fish soup: Fiano's mineral depth and textural richness navigate the soup's complex seafood character while the bruschetta absorbs the rich broth.")
    PAIR(prod2a1, "Roasted whole branzino with lemon, capers, and olives", "complement", "classic", "fish_course", "The wine's mineral precision and honey depth are ideal for whole roasted sea bass; capers echo the wine's saline character while olives add the Mediterranean depth that bridges Campanian wine and table.")
    PAIR(prod2a1, "Aged Provola affumicata with roasted tomatoes and basil", "complement", "established", "cheese", "Campania's smoked Provola resonates with Fiano's own smoky volcanic character; roasted tomatoes add the acidity that bridges the wine's mineral depth while basil provides aromatic freshness.")

prod2a2, new6 = PROD("Feudi di San Gregorio Fiano di Avellino DOC", "wine_still", p2a, r2, "Italy",
                      subcategory="Fiano", price_tier="mid_range",
                      description="The estate Fiano, sourcing from multiple Irpinian vineyards, delivers the variety's essential character in a slightly more accessible style: floral, with white peach, hazelnut, and herb notes and a clean mineral finish that makes it one of southern Italy's most food-friendly whites.")
if new6:
    PAIR(prod2a2, "Grilled calamari with lemon and olive oil", "complement", "classic", "fish_course", "Fiano's delicacy and mineral lift are ideal for simply prepared calamari; lemon amplifies the wine's citrus acidity while olive oil bridges its texture.")
    PAIR(prod2a2, "Mozzarella di bufala with tomatoes and basil (Insalata Caprese)", "complement", "classic", "starter", "The wine's creamy texture and subtle mineral character resonate with buffalo mozzarella; ripe tomatoes add the acidity that bridges the wine's own character while basil provides aromatic echo.")
    PAIR(prod2a2, "Pasta con cozze e vongole (mussels and clams)", "complement", "classic", "main", "Fiano's mineral depth and herb character are natural companions for southern Italian shellfish pasta; the wine's acidity cuts through the molluscs' richness while its mineral note echoes their brine.")
    PAIR(prod2a2, "Fresh ricotta with lemon zest and Campanian honey", "complement", "established", "cheese", "Fresh ricotta's clean dairy sweetness and Fiano's honey and herb character are a Campanian classic; lemon zest echoes the wine's citrus while local honey creates a direct flavour bridge.")

p2b = P("Mastroberardino", "winery", r2, "Italy",
         production_philosophy="classical",
         philosophy_description="Mastroberardino is the historic family that preserved Campania's indigenous varieties through the phylloxera era and postwar challenges, making them the most important custodian of Fiano, Greco, and Aglianico in southern Italy.",
         reputation_narrative="Without Mastroberardino's tenacious preservation of Campanian indigenous varieties, Fiano, Greco, and Aglianico might have disappeared. The family's decades of advocacy and quality production have made them the paternal figure of southern Italian wine revival.",
         price_positioning="premium")

prod2b1, new7 = PROD("Mastroberardino Radici Fiano di Avellino", "wine_still", p2b, r2, "Italy",
                      subcategory="Fiano", price_tier="premium",
                      description="Mastroberardino's flagship Fiano from their oldest Irpinian vineyards, displaying the variety's full complexity with the authority that comes from decades of expertise: toasted hazelnut, dried chamomile, honey, and a profoundly mineral, smoky finish.")
if new7:
    PAIR(prod2b1, "Grilled scampi with garlic, white wine, and parsley", "complement", "classic", "fish_course", "Radici Fiano's mineral depth and toasted hazelnut character are a sophisticated match for scampi; garlic and white wine add depth while parsley echoes the wine's herbaceous complexity.")
    PAIR(prod2b1, "Risotto ai frutti di mare with saffron", "complement", "established", "main", "The wine's textural richness and mineral depth navigate the complexity of a seafood risotto; saffron's mineral-floral character echoes Fiano's own mineral profile while the risotto's cream absorbs the wine's richness.")
    PAIR(prod2b1, "Vitello tonnato (veal with tuna sauce and capers)", "complement", "established", "starter", "The wine's savoury complexity and mineral depth are uniquely equipped for vitello tonnato's tuna-umami character; capers mirror the wine's saline mineral note while the veal provides the protein that grounds the pairing.")
    PAIR(prod2b1, "Scamorza affumicata (smoked mozzarella) grilled with herbs", "complement", "classic", "starter", "Fiano's smoky volcanic mineral character creates a fascinating resonance with grilled smoked scamorza; herbs add aromatic complexity while the wine's acidity cuts through the melted cheese's richness.")

prod2b2, new8 = PROD("Mastroberardino Mastro Fiano di Avellino", "wine_still", p2b, r2, "Italy",
                      subcategory="Fiano", price_tier="mid_range",
                      description="Mastroberardino's accessible Fiano, displaying the variety's signature floral and hazelnut character in a fresh, approachable style for early drinking — an excellent introduction to one of southern Italy's most distinctive white wine personalities.")
if new8:
    PAIR(prod2b2, "Bruschetta with fresh tomatoes, basil, and olive oil", "complement", "classic", "starter", "Fiano's fresh character and mineral lift are ideal for bruschetta's tomato freshness; basil echoes the wine's herbaceous notes while olive oil bridges its textural richness.")
    PAIR(prod2b2, "Fritto misto di pesce (mixed fried seafood)", "complement", "classic", "starter", "The wine's acidity and mineral precision cut through fried seafood's oil while its citrus character echoes the traditional squeeze of lemon; this is the Campanian seafood bar's house pairing.")
    PAIR(prod2b2, "Panzanella with fresh tuna and cherry tomatoes", "complement", "established", "casual", "Fiano's herb and citrus character are natural companions for a summer panzanella; fresh tuna adds protein richness while cherry tomatoes provide the acidity that bridges the wine.")
    PAIR(prod2b2, "Buffalo mozzarella pizza with fresh basil and San Marzano tomatoes", "complement", "classic", "casual", "The quintessential Campanian combination: Fiano's mineral freshness and herb character are the natural wine companion for authentic Neapolitan pizza; mozzarella's creaminess is lifted by the wine's acidity.")

# ── 3. Greco di Tufo DOCG ────────────────────────────────────────────────────
print("=== Greco di Tufo DOCG ===")
r3 = R("Greco di Tufo DOCG", "Italy", "wine",
        designation_type="DOCG", designation_name="Greco di Tufo",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Greco di Tufo, grown on the tufa soils of the Irpinia hills northeast of Naples, produces one of Campania's most distinctive white wines. The Greco grape, of Greek origin, produces wines of notable structure and mineral depth: citrus, stone fruit, almond, and a distinctive volcanic-mineral finish with natural acidity that allows development in the bottle.",
        key_producers="Feudi di San Gregorio, Mastroberardino, Di Meo, Vesevo, Villa Raiano",
        historical_context="Greco di Tufo's name reflects both its Greek origins and its distinctive tufa (volcanic tuff) soils. The variety was brought to Campania by Greek colonists of Magna Graecia and has been cultivated in the Irpinia hills for over 2,000 years. The DOCG, granted in 2003 alongside Fiano di Avellino, recognised Greco's importance as one of Italy's great indigenous white varieties.")

for yr, qd, pt in [
    (2018, "very_good", "stable"), (2019, "excellent", "rising"), (2020, "very_good", "stable"),
    (2021, "excellent", "rising"), (2022, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Feudi di San Gregorio Greco", "winery", r3, "Italy",
         production_philosophy="terroir_expression",
         philosophy_description="Feudi's Greco di Tufo production focuses on the Cutizzi single vineyard, one of the DOCG's most celebrated sites, producing a Greco of remarkable mineral precision and concentration.",
         reputation_narrative="Feudi's Cutizzi Greco di Tufo is consistently cited as the DOCG's benchmark wine, demonstrating how volcanic tufa soils can produce whites of extraordinary mineral depth and longevity alongside Fiano di Avellino.",
         price_positioning="premium")

prod3a1, new9 = PROD("Feudi di San Gregorio Cutizzi Greco di Tufo", "wine_still", p3a, r3, "Italy",
                      subcategory="Greco", price_tier="premium",
                      description="From the Cutizzi single vineyard on tufa soils in Santa Paolina, this is one of Greco di Tufo's most complex expressions: citrus pith, white peach, almond, and a profound volcanic-mineral finish of exceptional persistence and ageing potential.")
if new9:
    PAIR(prod3a1, "Spaghetti con ricci di mare (sea urchin pasta) with parsley", "complement", "classic", "main", "Greco's mineral depth and almond character are uniquely equipped for sea urchin's oceanic intensity; parsley adds fresh herb contrast while the volcanic mineral note echoes the urchin's natural sea-mineral quality.")
    PAIR(prod3a1, "Grilled octopus with potato, capers, and lemon", "complement", "classic", "starter", "The wine's citrus and mineral character frame octopus's earthy-oceanic quality; capers echo the wine's saline mineral note while potato provides the starchy foil the combination needs.")
    PAIR(prod3a1, "White anchovy bruschetta with buffalo mozzarella and basil", "complement", "established", "starter", "Greco's structure and mineral depth can handle anchovy's intense umami; buffalo mozzarella softens the contrast while basil adds the aromatic lift that bridges wine and topping.")
    PAIR(prod3a1, "Insalata di polpo con olive e capperi", "complement", "classic", "starter", "Octopus salad with olives and capers is a classic southern Italian pairing for Greco; the wine's mineral depth bridges the octopus's brine while olives and capers add the savoury depth that amplifies its character.")

prod3a2, new10 = PROD("Feudi di San Gregorio Greco di Tufo DOCG Estate", "wine_still", p3a, r3, "Italy",
                       subcategory="Greco", price_tier="mid_range",
                       description="Feudi's estate Greco di Tufo, from multiple Irpinian tufa sites, delivering the variety's essential character: fresh citrus, peach, and almond with the distinctive chalky-volcanic mineral finish that defines authentic Greco di Tufo.")
if new10:
    PAIR(prod3a2, "Grilled fish with lemon, olive oil, and Sicilian capers", "complement", "classic", "fish_course", "Greco's citrus and mineral freshness are ideal for simply grilled Mediterranean fish; Sicilian capers add the umami-saline complexity that amplifies the wine's mineral character.")
    PAIR(prod3a2, "Frittura di paranza (small fried fish) with lemon", "complement", "classic", "starter", "The wine's acidity and mineral precision cut through fried fish's oil while echoing the traditional lemon squeeze; this is the Campanian seafood taverna's natural pairing.")
    PAIR(prod3a2, "Insalata caprese with buffalo mozzarella and local tomatoes", "complement", "classic", "starter", "Greco's citrus freshness and mineral character are a pure Campanian pairing for the region's most iconic salad; mozzarella's creaminess is lifted by the wine's acidity.")
    PAIR(prod3a2, "Steamed mussels with white wine, garlic, and tomato broth", "complement", "classic", "starter", "The wine's mineral and citrus character mirror the steaming broth while the mussels' brine is bridged by Greco's own saline depth — the wine's acidity making each sip a palette-refresher.")

p3b = P("Mastroberardino Greco", "winery", r3, "Italy",
         production_philosophy="classical",
         philosophy_description="Mastroberardino's Greco di Tufo production is anchored by the Nova Serra cuvée from their historic Irpinian vineyards, representing decades of expertise with this ancient variety.",
         reputation_narrative="Mastroberardino's Nova Serra Greco di Tufo has long been a benchmark for the DOCG, demonstrating the variety's capacity for structure and ageing potential in the hands of its most experienced custodian.",
         price_positioning="mid_range")

prod3b1, new11 = PROD("Mastroberardino Nova Serra Greco di Tufo", "wine_still", p3b, r3, "Italy",
                       subcategory="Greco", price_tier="mid_range",
                       description="Mastroberardino's flagship Greco, from their highest elevation Irpinian sites. Nova Serra delivers Greco's full structural complexity: more austere and mineral than Fiano, with citrus pith, white almond, and volcanic mineral in a tight, age-worthy frame.")
if new11:
    PAIR(prod3b1, "Grilled branzino al sale (salt-baked sea bass) with lemon and herbs", "complement", "classic", "fish_course", "Nova Serra's mineral precision and citrus depth frame salt-baked sea bass with perfect alignment; the salt crust amplifies the wine's mineral character while lemon bridges its citrus acidity.")
    PAIR(prod3b1, "Tagliolini ai gamberi (prawn pasta) with cherry tomatoes", "complement", "classic", "main", "The wine's structure and mineral depth navigate prawn pasta's sweetness and tomato acidity; the grape's almond character adds an unexpected textural bridge between wine and pasta.")
    PAIR(prod3b1, "Vitello tonnato with capers and anchovy", "complement", "established", "starter", "Nova Serra's mineral backbone and citrus precision are ideal for the complex umami of vitello tonnato; capers mirror the wine's saline mineral while the veal's delicacy is complemented by Greco's structure.")
    PAIR(prod3b1, "Aged Caciocavallo with local honey and hazelnuts", "complement", "established", "cheese", "Greco's almond character and mineral depth resonate with aged Caciocavallo's intense nuttiness; local honey bridges the wine's citrus-mineral depth while hazelnuts echo its own almond note.")

prod3b2, new12 = PROD("Mastroberardino Greco di Tufo", "wine_still", p3b, r3, "Italy",
                       subcategory="Greco", price_tier="mid_range",
                       description="The accessible expression of Mastroberardino Greco, offering the variety's characteristic mineral-citrus profile in a fresh, food-friendly style — an excellent ambassador for one of Campania's most distinctive white wine personalities.")
if new12:
    PAIR(prod3b2, "Pizza Margherita with San Marzano tomatoes and fior di latte", "complement", "classic", "casual", "Greco's mineral freshness and citrus character are a Campanian classic with pizza; fior di latte's creaminess is refreshed by the wine's acidity while San Marzano's sweetness bridges its mineral depth.")
    PAIR(prod3b2, "Fritto misto di verdure con salsa di mare", "complement", "established", "starter", "The wine's acidity and citrus freshness cut through fried vegetables while the seafood sauce's mineral depth resonates with Greco's own character.")
    PAIR(prod3b2, "Mozzarella fritta (fried mozzarella) with tomato sauce", "complement", "classic", "casual", "Greco's acidity is precisely calibrated to cut through fried mozzarella's oil; the tomato sauce adds the acidity that bridges the wine's own freshness.")
    PAIR(prod3b2, "Grilled swordfish with salsa verde and roasted peppers", "complement", "established", "fish_course", "Swordfish's meaty density demands the structure of Greco; salsa verde's herb-vinegar character echoes the wine's herbaceous minerality while roasted peppers add sweetness.")

# ── 4. Egri Bikavér PDO (Hungary) ────────────────────────────────────────────
print("=== Egri Bikavér PDO ===")
r4 = R("Egri Bikavér PDO", "Hungary", "wine",
        designation_type="PDO", designation_name="Egri Bikavér",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description="Egri Bikavér — Bull's Blood of Eger — is Hungary's most internationally recognised red wine, a multi-variety blend from the volcanic hills of Eger in northern Hungary. The historic blend, led by Kékfrankos (Blaufränkisch) with up to eight other varieties, produces wines of considerable depth and character that are finding renewed international respect after decades of bulk production during the communist era.",
        key_producers="St. Andrea Winery, GIA Winery, Tibor Gál, Kovács Nimród Winery, Tóth Ferenc",
        historical_context="Egri Bikavér's legend dates to the 1552 siege of Eger, when Hungarian defenders reportedly drank the dark red wine with such ferocity that Turkish attackers believed it was bull's blood. The wine's modern decline came during communist collectivisation when quality was sacrificed for volume. A renaissance began in the 2000s when private producers reestablished individual quality standards, and in 2004 the Egri Bikavér Superior category was created to identify the finest expressions.")

for yr, qd, pt in [
    (2018, "very_good", "rising"), (2019, "excellent", "rising"), (2020, "good", "stable"),
    (2021, "very_good", "rising"), (2022, "good", "rising")]:
    VIN(r4, yr, qd, pt)

p4a = P("St. Andrea Winery", "winery", r4, "Hungary",
         production_philosophy="terroir_expression",
         philosophy_description="St. Andrea is one of Eger's most innovative wineries, producing single-vineyard Egri Bikavér wines that demonstrate the historic appellation's capacity for world-class quality when grown on the volcanic Bükk hillsides with genuine site specificity.",
         reputation_narrative="St. Andrea's Merengő single-vineyard Egri Bikavér has transformed international perceptions of Hungarian red wine, earning recognition alongside Central European benchmarks and demonstrating that Eger can produce world-class wines at fair prices.",
         price_positioning="mid_range")

prod4a1, new13 = PROD("St. Andrea Merengő Egri Bikavér Superior", "wine_still", p4a, r4, "Hungary",
                       subcategory="Kékfrankos blend", price_tier="mid_range",
                       description="From a single volcanic-soil vineyard in Eger, Merengő is one of Hungary's finest red wines: a Bikavér Superior of depth and complexity, led by Kékfrankos with Cabernet Franc and Merlot. Dark cherry, spice, mineral, and a long, structured finish that challenges European benchmarks at its price point.")
if new13:
    PAIR(prod4a1, "Hungarian gulyás (goulash) with egg noodles and sour cream", "complement", "classic", "main", "Egri Bikavér's warm spice and dark cherry character are the natural companion for Hungary's national dish; sour cream's acidity echoes the wine's own tartness while egg noodles absorb the rich stew.")
    PAIR(prod4a1, "Slow-roasted pork neck with paprika and caraway sauerkraut", "complement", "classic", "main", "Paprika's warmth and caraway's spice resonate with Bikavér's own spice character; pork's richness is cut by the wine's acidity while sauerkraut adds the fermented tartness that bridges the wine.")
    PAIR(prod4a1, "Grilled lamb chops with roasted peppers and herb yogurt", "complement", "established", "main", "The wine's structure and fruit depth are well-matched to grilled lamb; roasted peppers add Mediterranean sweetness while herb yogurt provides the cool contrast that balances the wine's tannin.")
    PAIR(prod4a1, "Aged Hungarian sheep's milk cheese with quince paste", "complement", "established", "cheese", "Hungarian tradition connects Bull's Blood with the country's aged sheep's milk cheeses; quince paste bridges the wine's dark-fruit character while the cheese's sharpness provides the contrast that extends the finish.")

prod4a2, new14 = PROD("St. Andrea Nagy-Eged Egri Bikavér Superior", "wine_still", p4a, r4, "Hungary",
                       subcategory="Kékfrankos blend", price_tier="mid_range",
                       description="From the Nagy-Eged volcanic hill above Eger, this Bikavér Superior displays the site's distinctive mineral character alongside the blend's characteristic dark cherry and spice, demonstrating Eger's diversity of terroir expression within a single appellation.")
if new14:
    PAIR(prod4a2, "Braised veal with paprika cream sauce and egg noodles (pörkölt)", "complement", "classic", "main", "Pörkölt is Hungary's most beloved braised dish; the wine's structure and paprika-like spice character find direct resonance with the dish's rich sauce while egg noodles absorb the wine's intensity.")
    PAIR(prod4a2, "Stuffed cabbage rolls (töltött káposzta) with sour cream", "complement", "classic", "main", "Töltött káposzta is one of Hungary's most deeply traditional dishes; the wine's dark fruit and acidity navigate the rich cabbage rolls and sour cream with ease, the fermented cabbage bridging the wine's own tart character.")
    PAIR(prod4a2, "Grilled mangalitsa pork with roasted vegetables", "complement", "established", "main", "Hungary's prized Mangalitsa (woolly pig) breed produces exceptionally marbled pork that demands the structure of a Bikavér Superior; roasted vegetables add the natural sweetness that softens the wine's firm tannin.")
    PAIR(prod4a2, "Aged Trappista cheese with Hungarian mustard and dark bread", "complement", "established", "cheese", "Hungary's most widely produced aged cheese finds its natural companion in Bull's Blood; Hungarian mustard adds pungent spice that echoes the wine's character while dark bread grounds the combination.")

p4b = P("Kovács Nimród Winery", "winery", r4, "Hungary",
         production_philosophy="artisanal",
         philosophy_description="Kovács Nimród produces Egri Bikavér and single-variety wines from Eger with a focus on modern winemaking techniques applied to traditional Hungarian varieties, balancing international accessibility with genuine local character.",
         reputation_narrative="Kovács Nimród is one of Eger's most respected private producers, demonstrating that Kékfrankos and the Bull's Blood blend can achieve international recognition through careful viticulture and modern cellar technique.",
         price_positioning="mid_range")

prod4b1, new15 = PROD("Kovács Nimród Monopole Egri Bikavér", "wine_still", p4b, r4, "Hungary",
                       subcategory="Kékfrankos blend", price_tier="mid_range",
                       description="Kovács Nimród's flagship Egri Bikavér, a full-spectrum blend showcasing the appellation's potential: deep, spicy, and structured with dark cherry, tobacco, and volcanic mineral character in a style that bridges traditional Hungarian wine culture and modern international quality.")
if new15:
    PAIR(prod4b1, "Chicken paprikash with sour cream dumplings (galuska)", "complement", "classic", "main", "Bikavér's paprika-like warmth and dark fruit are uniquely resonant with chicken paprikash; sour cream dumplings absorb the wine's richness while the paprika sauce creates a direct flavour connection.")
    PAIR(prod4b1, "Wild boar ragù with tagliatelle and truffle shavings", "complement", "established", "main", "The wine's depth and structure are well-matched to wild boar's earthy intensity; truffle adds the luxury dimension that amplifies the volcanic mineral character of the Eger terroir.")
    PAIR(prod4b1, "Lamb and potato stew with rosemary and garlic", "complement", "established", "main", "The wine's medium-weight structure and dark cherry character complement lamb stew without overwhelming the dish's rustic simplicity; rosemary echoes the wine's herbal depth while garlic adds savoury depth.")
    PAIR(prod4b1, "Blue cheese with Tokaji Aszú-sweetened onion marmalade", "complement", "adventurous", "cheese", "An unconventional but fascinating Hungarian pairing: the wine's dark fruit and spice contrast with blue cheese while the Tokaji-sweetened onion marmalade creates an unexpected bridge between Hungarian wine cultures.")

prod4b2, new16 = PROD("Kovács Nimród Kékfrankos Eger", "wine_still", p4b, r4, "Hungary",
                       subcategory="Kékfrankos", price_tier="mid_range",
                       description="A pure single-variety Kékfrankos (Blaufränkisch) from Eger, displaying the variety's hallmark: vibrant acidity, dark cherry, and spice in a lighter frame than the Bikavér blend, with considerable freshness and food versatility.")
if new16:
    PAIR(prod4b2, "Grilled pork sausages with roasted peppers and mustard", "complement", "classic", "main", "Kékfrankos's bright acidity and cherry character are ideal companions for grilled pork sausage; roasted peppers add sweetness while mustard's pungency amplifies the wine's spice.")
    PAIR(prod4b2, "Roasted duck with red cabbage and potato dumplings", "complement", "established", "main", "The wine's acidity and cherry fruit navigate duck's richness and red cabbage's tartness; potato dumplings absorb the rich duck fat while the wine's freshness keeps the combination lively.")
    PAIR(prod4b2, "Lentil soup with smoked ham hock and caraway", "complement", "established", "main", "Kékfrankos's light frame and cherry character are ideal for hearty lentil soup; smoked ham hock's intensity is balanced by the wine's acidity while caraway's spice echoes the wine's own character.")
    PAIR(prod4b2, "Aged Gouda with fig mustard and rye bread", "complement", "established", "cheese", "Kékfrankos's cherry and spice find resonance with aged Gouda's caramel sweetness; fig mustard bridges the wine's fruit while rye bread's earthiness grounds the pairing.")

# ── 5. Valle de Uco (Argentina) ──────────────────────────────────────────────
print("=== Valle de Uco (Argentina) ===")
r5 = R("Valle de Uco", "Argentina", "wine",
        designation_type="DO", designation_name="Valle de Uco",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Valle de Uco, south of Mendoza city at elevations of 900–1,500 metres, has emerged as Argentina's most exciting wine zone. The extreme altitude, calcareous soils, and significant diurnal temperature variation produce Malbec and Cabernet Franc of extraordinary precision and freshness — wines that challenge the perception of Argentine wine as uniformly rich and warm. The Gualtallary sub-zone has been called Argentina's greatest wine terroir.",
        key_producers="Zuccardi Valle de Uco, Catena Zapata (Adrianna Vineyard), Clos de los Siete, Domaine Bousquet",
        historical_context="Valle de Uco's viticultural history began only in the 1980s when Mendoza's most forward-thinking producers identified altitude as the key to freshness and precision in Argentine wine. The zone's rapid ascent from agricultural region to Argentina's most talked-about wine area was driven by international investment, critical acclaim, and the discovery of sites like Gualtallary and Los Árboles that produce wines of extraordinary complexity.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r5, yr, qd, pt)

p5a = P("Zuccardi Valle de Uco", "winery", r5, "Argentina",
         production_philosophy="terroir_expression",
         philosophy_description="Sebastián Zuccardi has transformed his family's winery into one of Argentina's most admired, producing single-terroir Malbec wines from Valle de Uco that won the title of World's Best Winery in 2019 and 2020. His obsession with calcareous soil expression has defined a new aesthetic for Argentine Malbec.",
         reputation_narrative="Zuccardi Valle de Uco is the most decorated winery in Argentina's history, with consecutive World's Best Winery awards and wines that challenge the world's finest at every price point. Sebastián Zuccardi's terroir-first philosophy has influenced a generation of Argentine winemakers.",
         price_positioning="ultra_premium")

prod5a1, new17 = PROD("Zuccardi Concreto Malbec Valle de Uco", "wine_still", p5a, r5, "Argentina",
                       subcategory="Malbec", price_tier="premium",
                       description="Fermented in concrete eggs without oak to showcase pure calcareous terroir, Concreto is one of Argentina's most distinctive Malbecs: violet, dark plum, and chalk-mineral precision in a style that is simultaneously powerful and ethereally fine-grained. A wine that changed how Argentina thinks about Malbec.")
if new17:
    PAIR(prod5a1, "Rack of lamb with herb crust and Mendoza olive tapenade", "complement", "classic", "main", "Concreto's violet and mineral precision demand lamb's complementary richness; herb crust echoes the wine's complex aromatic character while Mendoza olive tapenade grounds the pairing in local terroir.")
    PAIR(prod5a1, "Beef tenderloin with chimichurri rojo and potato purée", "complement", "classic", "main", "The wine's precision and violet character are ideal for the finest cut of Argentine beef; chimichurri rojo's red chili and herb brightness provides the contrast that keeps the luxury pairing vibrant.")
    PAIR(prod5a1, "Burrata with roasted beets, walnuts, and Andean herb oil", "complement", "established", "starter", "Concreto's mineral freshness and violet lift find an unexpected harmony with burrata and beets; Andean herb oil echoes the wine's aromatic complexity while walnuts add earthiness.")
    PAIR(prod5a1, "Aged Sardo with dulce de membrillo and Andean almonds", "complement", "established", "cheese", "The wine's precision and mineral depth find resonance with Argentine aged sheep's cheese; dulce de membrillo bridges its fruit while Andean almonds echo the calcareous mineral character.")

prod5a2, new18 = PROD("Zuccardi Finca Piedra Infinita Malbec Gualtallary", "wine_still", p5a, r5, "Argentina",
                       subcategory="Malbec", price_tier="ultra_premium",
                       description="From the Piedra Infinita estate in Gualtallary at 1,400 metres, this single-vineyard Malbec is one of Argentina's most profound wines: extreme concentration, violet florality, and chalk-limestone mineral character that places it among the world's great terroir-expressive reds.")
if new18:
    PAIR(prod5a2, "Dry-aged Argentine ribeye with bone marrow and Andean salt", "complement", "classic", "main", "Gualtallary's most profound Malbec and dry-aged Argentine beef is the country's supreme luxury pairing; bone marrow mirrors the wine's concentration while Andean salt amplifies both the meat's minerality and the wine's limestone character.")
    PAIR(prod5a2, "Wagyu short rib with Mendoza red wine reduction and truffle", "complement", "classic", "main", "Piedra Infinita's power and complexity demand wagyu's extraordinary marbling; Mendoza wine reduction creates a direct regional bridge while truffle deepens the earthy resonance.")
    PAIR(prod5a2, "Venison tartare with quail egg, capers, and pickled shallots", "complement", "established", "starter", "The wine's intensity and mineral precision are uniquely equipped to complement venison tartare; capers and pickled shallots provide the acidity contrast that keeps the luxury pairing balanced.")
    PAIR(prod5a2, "Aged Manchego with Andean truffle honey and black walnut", "complement", "established", "cheese", "Piedra Infinita's limestone mineral depth demands aged hard cheese; Andean truffle honey bridges the wine's florality while black walnut echoes the wine's earthy complexity.")

p5b = P("Clos de los Siete", "winery", r5, "Argentina",
         production_philosophy="classical",
         philosophy_description="Clos de los Siete is a unique collective winemaking project in Valle de Uco, involving Michel Rolland and seven prestigious French wine families who each established their own winery on a shared estate, with the 'Clos de los Siete' blend creating a unified whole from each member's contribution.",
         reputation_narrative="Clos de los Siete is Argentina's most ambitious collaborative wine project, combining the expertise of European fine wine families with Valle de Uco's emerging prestige. The resulting wine is consistently one of Argentina's most reliable, complex value propositions.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Clos de los Siete Valle de Uco", "wine_still", p5b, r5, "Argentina",
                       subcategory="Malbec blend", price_tier="mid_range",
                       description="Michel Rolland's flagship Argentine blend, combining Malbec with Merlot, Cabernet Sauvignon, and Syrah from seven member wineries in Valle de Uco. The wine delivers consistent complexity and depth: dark plum, violet, herbs, and supple tannin in a polished, internationally appealing style.")
if new19:
    PAIR(prod5b1, "Argentine asado — prime rib and short ribs over wood fire", "complement", "classic", "main", "Clos de los Siete's polished dark fruit and supple tannin are ideal for the complexity of an Argentine asado; the wood fire's smokiness adds depth while the wine's structure cuts through the abundant fat.")
    PAIR(prod5b1, "Grilled provoleta with Mendoza olives and oregano", "complement", "classic", "casual", "Argentina's beloved grilled cheese and Malbec blend is a national casual pairing; the wine's dark fruit and gentle structure navigate the cheese's caramelised saltiness while olives add Mediterranean depth.")
    PAIR(prod5b1, "Empanadas tucumanas (beef, egg, and spice in pastry)", "complement", "classic", "casual", "The blend's accessible structure and dark fruit complement Argentine empanadas perfectly; spiced beef filling's complexity is matched by the wine's own layered character.")
    PAIR(prod5b1, "Braised short ribs with Malbec reduction and polenta", "complement", "established", "main", "A Malbec reduction with Malbec wine creates a complete circle of flavour; short rib's collagen richness is bridged by the wine's fruit while polenta absorbs the intensity.")

prod5b2, new20 = PROD("Monteviejo Lindaflor Malbec Valle de Uco", "wine_still", p5b, r5, "Argentina",
                       subcategory="Malbec", price_tier="mid_range",
                       description="From Monteviejo — one of the Clos de los Siete member estates — Lindaflor is a high-altitude Malbec of impressive freshness and floral character from Valle de Uco's cool Vistalba zone. Violet, plum, and fresh herb with a lively acidity that makes it one of Argentina's most food-friendly Malbecs.")
if new20:
    PAIR(prod5b2, "Grilled lamb cutlets with salsa criolla and roasted potatoes", "complement", "classic", "main", "Lindaflor's freshness and violet character are ideal for grilled lamb; salsa criolla's tomato and herb brightness provides the lively contrast the wine's acidity demands.")
    PAIR(prod5b2, "Pork tenderloin with plum sauce and wilted greens", "complement", "established", "main", "The wine's plum and violet character create a direct flavour bridge with plum sauce; pork tenderloin's lean richness provides the protein the wine's fresh tannin needs while greens add herbaceous contrast.")
    PAIR(prod5b2, "Beef empanadas with chimichurri dipping sauce", "complement", "classic", "casual", "Valle de Uco freshness in a Malbec with Argentina's most beloved pastry; chimichurri's herb and vinegar brightness echoes the wine's acidity while empanadas' spiced filling provides the meaty depth.")
    PAIR(prod5b2, "Provolone and roasted pepper sandwich (choripán-style)", "complement", "classic", "casual", "A casual Argentine pairing for an everyday wine of quality; the sandwich's roasted pepper sweetness and cheese richness are balanced by Lindaflor's acidity and violet freshness.")

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
print("B149 complete.")
conn.close()
