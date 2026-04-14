#!/usr/bin/env python3
"""B168 — Italian diversity: Etna DOC, Soave DOC, Amarone DOCG, Sagrantino DOCG, Taurasi DOCG"""
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

# === ETNA DOC ===
print("=== Etna DOC ===")
r1 = R("Etna DOC", "Italy", "wine",
       designation_type="DOC",
       designation_name="Etna Denominazione di Origine Controllata",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Mount Etna, Europe's most active volcano, produces wines of extraordinary mineral complexity and age-worthiness from the indigenous Nerello Mascalese (red) and Carricante (white) varieties. The high-altitude basalt and volcanic ash soils, combined with extreme day-night temperature variation at 400–1000m, create a unique terroir comparable to the greatest wine regions in the world. Pre-phylloxera old-vine alberello-trained Nerello Mascalese produces Pinot Noir-like elegance despite the extreme Mediterranean climate.",
       key_producers="Benanti, Cornelissen, Passopisciaro, Terre Nere, Cos, Franchetti",
       historical_context="Etna DOC was created in 1968 but the modern fine wine era began with Giuseppe Benanti in the 1990s and accelerated dramatically in the 2000s when international producers like Andrea Franchetti (Passopisciaro) and Frank Cornelissen recognised Etna's potential. The region has since become one of the wine world's most talked-about terroirs.")
for yr, qd, pt, sn in [
    (2017,"excellent","rising","A landmark Etna vintage — old-vine Nerello Mascalese of extraordinary mineral depth."),
    (2018,"very_good","stable","Fine vintage; volcanic mineral character pronounced in both red and white wines."),
    (2019,"excellent","rising","Outstanding year; wines from high-altitude contrade showing exceptional freshness."),
    (2020,"very_good","stable","Good vintage; Carricante whites particularly successful for aromatic intensity."),
    (2021,"excellent","rising","One of the finest Etna vintages in recent memory — Nerello of Burgundian refinement."),
    (2022,"very_good","stable","Warm vintage; wines showing more immediate fruit character with classic volcanic backbone."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Passopisciaro Wines Etna", "winery", r1, "Italy",
       production_philosophy="terroir_expression",
       philosophy_description="Andrea Franchetti's Etna estate, producing single-contrada (sub-area) Nerello Mascalese wines that demonstrate the extraordinary diversity of Etna's volcanic terroir. Each contrada wine — Chiappemacine, Guardiola, Porcaria, Rampante, Sciaranuova — has a distinct mineral signature from different soil compositions and altitudes.",
       reputation_narrative="Passopisciaro's single-contrada Nerello Mascalese wines are Etna's most acclaimed bottles internationally, demonstrating that each volcanic parcel on the mountain produces genuinely distinct wine — a Burgundy-like classification of terroir on an Italian volcano.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Passopisciaro Nerello Mascalese Etna Rosso", "wine_still", p1, r1, "Italy",
                    subcategory="red", description="Benchmark Etna Rosso from old-vine Nerello Mascalese on volcanic basalt — pale ruby, Pinot-like in colour and elegance. Red cherry, pomegranate, dried rose, volcanic mineral, and fine silky tannins. Evolves magnificently over 10–15 years.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled red mullet with capers, tomato and olive", "complement", "classic", "main", "A Sicilian classic — Etna Rosso's bright acidity mirrors the capers; volcanic mineral matches the sea-scented fish.")
    PAIR(prod, "Wild boar ragù with home-made pappardelle", "complement", "established", "main", "The wine's bright acidity and mineral freshness handle gamey boar without being overwhelmed by the rich ragù.")
    PAIR(prod, "Grilled lamb chops with pistachio crust", "complement", "classic", "main", "Sicilian pistachio and Sicilian Nerello — a natural regional pairing; the wine's delicacy matches the lamb's sweetness.")
    PAIR(prod, "Aged Pecorino Siciliano with honey and walnuts", "complement", "established", "cheese", "The wine's acidity cuts through pecorino's fat; volcanic mineral bridges the cheese's earthy character.")
prod, is_new = PROD("Terre Nere Etna Bianco Carricante", "wine_still", p1, r1, "Italy",
                    subcategory="white", description="Carricante from Etna's eastern flank — the home of the variety. Steely, mineral, and saline: citrus, white flowers, volcanic rock, and a long, saline finish. The greatest Etna white, capable of ageing 10+ years.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled sea urchin pasta with bottarga and lemon", "complement", "classic", "main", "Etna Bianco's saline mineral and citrus mirror sea urchin's oceanic richness; bottarga deepens the sea character.")
    PAIR(prod, "Fresh mozzarella di bufala with cherry tomatoes and basil", "complement", "classic", "starter", "Pure Sicilian flavours — the wine's mineral freshness lifts the mozzarella; tomato acidity echoes the wine's citrus.")
    PAIR(prod, "Grilled swordfish with salmoriglio (lemon and herb sauce)", "complement", "classic", "main", "Salmoriglio and volcanic white — lemon echoes the wine's citrus; mineral depth mirrors swordfish's meaty ocean flavour.")
    PAIR(prod, "Fritto misto di mare with aioli", "complement", "classic", "main", "Saline mineral Carricante cuts through the fried batter; the wine's freshness makes it a perfect aperitivo-style match.")

# === SOAVE DOC ===
print("=== Soave DOC ===")
r2 = R("Soave DOC", "Italy", "wine",
       designation_type="DOC",
       designation_name="Soave Denominazione di Origine Controllata",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Soave, east of Verona in the Veneto, is one of Italy's most important white wine regions — though long associated with anonymous commercial production, the Classico zone (the historic original hills) produces wines of genuine quality and character from Garganega and Trebbiano di Soave. The volcanic basalt soils of the Classico's steep hillside vineyards give the best wines their characteristic volcanic-mineral backbone and potential for serious ageing. Pieropan and Anselmi are benchmarks for quality Soave.",
       key_producers="Pieropan, Anselmi, Inama Winery, Gini, Coffele",
       historical_context="Soave was one of Italy's first DOCs in 1968, and its commercialisation in the 1970s-80s nearly destroyed its reputation. The revival began with producers like Leonildo Pieropan who maintained hillside viticulture in the Classico zone when others moved to productive valley floors.")
for yr, qd, pt, sn in [
    (2019,"very_good","stable","Fine vintage for Classico Soave with good freshness and volcanic mineral character."),
    (2020,"excellent","rising","Outstanding year; Garganega wines of exceptional aromatic complexity and depth."),
    (2021,"very_good","stable","Good vintage; hillside Classico wines showing excellent balance and mineral precision."),
    (2022,"very_good","stable","Warm year; wines slightly richer than typical but retaining Soave's characteristic freshness."),
    (2023,"excellent","rising","Exceptional vintage for Soave Classico — benchmark aromatics and mineral intensity."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Pieropan Winery Soave", "winery", r2, "Italy",
       production_philosophy="terroir_expression",
       philosophy_description="Leonildo Pieropan is the father of quality Soave — his estate maintained quality hillside viticulture in the Classico zone through Soave's commercial decline. His single-vineyard Calvarino and La Rocca wines are the benchmark expressions of what Garganega can achieve.",
       reputation_narrative="Pieropan's Calvarino and La Rocca are Italy's most compelling white wines from Garganega — demonstrating that Soave Classico, from proper volcanic hillside sites, can produce wines of international reference quality and genuine ageing potential.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Pieropan Calvarino Soave Classico", "wine_still", p2, r2, "Italy",
                    subcategory="white", description="Single-vineyard Garganega and Trebbiano from basalt and clay soils — one of Italy's greatest white wines. Almond, white flowers, citrus, volcanic mineral, and a long, saline-mineral finish. Profound age-worthiness over 10+ years.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled lake perch (pesce persico) with butter and sage", "complement", "classic", "main", "A Veneto classic — Soave Classico and freshwater lake fish share the same territory; sage bridges the wine's almond notes.")
    PAIR(prod, "Risi e bisi (Venetian rice and pea soup)", "complement", "established", "main", "The wine's mineral freshness complements this delicate spring dish; almond notes bridge the peas' sweetness.")
    PAIR(prod, "Grilled zucchini flowers stuffed with ricotta and anchovy", "complement", "classic", "starter", "Floral Garganega mirrors zucchini flower's delicacy; anchovy's salt echoes the wine's mineral backbone.")
    PAIR(prod, "Aged Grana Padano with pear and walnuts", "complement", "established", "cheese", "Almond notes in the wine bridge to Grana Padano's nuttiness; pear echoes the wine's white fruit character.")
prod, is_new = PROD("Pieropan La Rocca Soave Classico", "wine_still", p2, r2, "Italy",
                    subcategory="white", description="Barrel-fermented single-vineyard Garganega from white clay soils of La Rocca — richer and more complex than Calvarino. Stone fruit, hazelnut, honey, and a deep volcanic-mineral structure. Among Italy's most age-worthy whites.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Seared scallops with truffle and cauliflower cream", "complement", "classic", "starter", "Barrel-fermented richness matches scallop's sweetness; truffle bridges the wine's hazelnut notes beautifully.")
    PAIR(prod, "Roasted white asparagus with hollandaise and prosciutto", "complement", "established", "starter", "A classic Venetian spring pairing — the wine's richness and mineral depth suit asparagus at its best.")
    PAIR(prod, "Turbot in cream sauce with capers and lemon", "complement", "classic", "main", "Stone fruit and barrel richness bridge to cream sauce; capers and lemon echo the wine's natural brightness.")
    PAIR(prod, "Monte Veronese cheese with honey comb", "complement", "classic", "cheese", "Local Veneto cheese with Soave Classico — hazelnut and honey in the wine bridge to Monte Veronese's character perfectly.")

# === AMARONE DELLA VALPOLICELLA DOCG ===
print("=== Amarone della Valpolicella DOCG ===")
r3 = R("Amarone della Valpolicella DOCG", "Italy", "wine",
       designation_type="DOCG",
       designation_name="Amarone della Valpolicella Denominazione di Origine Controllata e Garantita",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Amarone della Valpolicella is one of Italy's most distinctive and powerful wines, produced by drying Corvina, Corvinone, and Rondinella grapes for 90–120 days before pressing. The appassimento (drying) process concentrates sugars, flavours, and colour, producing wines of extraordinary richness, complexity, and ageing potential — 15%+ alcohol, intense dark fruit, bitter chocolate, leather, and tobacco. The Valpolicella Classica zone's limestone and clay hillside vineyards produce the finest expressions.",
       key_producers="Dal Forno Romano, Quintarelli, Allegrini, Bertani, Masi",
       historical_context="Amarone was 'discovered' accidentally in the 1930s when a barrel of Recioto (sweet dried grape wine) fermented fully dry. The name means 'the great bitter one' (from amaro = bitter). It is now one of Italy's most internationally prized wines, with the best examples from Dal Forno and Quintarelli selling for hundreds to thousands of euros.")
for yr, qd, pt, sn in [
    (2015,"exceptional","stable","A legendary Amarone vintage — wines of extraordinary concentration and perfect structure."),
    (2016,"excellent","rising","Outstanding year; particularly successful for the Classico Superiore wines from historic estates."),
    (2017,"very_good","stable","Good vintage with excellent fruit concentration; warm year suited the appassimento process."),
    (2019,"excellent","rising","One of the finest recent Amarone vintages — wines of benchmark complexity and ageing potential."),
    (2020,"very_good","stable","Fine conditions; Amarone showing typical richness with good freshness from cooler sites."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Dal Forno Romano Winery", "winery", r3, "Italy",
       production_philosophy="terroir_expression",
       philosophy_description="Romano Dal Forno produces what many consider the greatest Amarone — from his Illasi Valley estate at the eastern edge of the Valpolicella DOC. His obsessive quality pursuit (less than 3000 cases per year, 4+ years ageing before release) produces wines of almost impossible concentration and longevity.",
       reputation_narrative="Dal Forno Romano's Amarone is Italy's most sought-after wine alongside Sassicaia and Masseto — a 2000 or 2005 vintage commands extraordinary prices and demonstrates Amarone's potential for 30+ year ageing of the highest order.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Dal Forno Romano Amarone della Valpolicella", "wine_still", p3, r3, "Italy",
                    subcategory="red", description="The greatest Amarone — deeply concentrated dried-grape wine from Illasi Valley estate vines. Black cherry, dark chocolate, tar, tobacco, liquorice, and a monumental tannic structure requiring 15+ years for full expression. Among Italy's most age-worthy and sought-after wines.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Braised wild boar with juniper, bay and polenta", "complement", "classic", "main", "The definitive Amarone pairing — the wine's power and complexity demands equally powerful game preparation.")
    PAIR(prod, "Brasato al Barolo (beef braised in wine) — adapted with Amarone", "complement", "classic", "main", "Braised beef in rich Amarone sauce is one of Veneto's greatest dishes; the wine served alongside deepens the experience.")
    PAIR(prod, "Aged Parmigiano Reggiano 60-month with balsamic", "complement", "classic", "cheese", "The definitive Italian cheese pairing with Amarone — long-aged Parmesan's crystalline umami meets the wine's monumental depth.")
    PAIR(prod, "Dark chocolate fondant with amarena cherries", "complement", "classic", "dessert", "Black cherry and dark chocolate in the wine mirror the fondant's richness; amarena cherries echo Amarone's dried fruit character.")
prod, is_new = PROD("Allegrini Amarone della Valpolicella Classico", "wine_still", p3, r3, "Italy",
                    subcategory="red", description="Classico-zone Amarone from one of Valpolicella's leading estates — accessible compared to Dal Forno but still intense. Dried cherry, tobacco, chocolate, vanilla, and structured tannins for 15–20 year ageing. An excellent introduction to the style.", price_tier="premium")
if is_new:
    PAIR(prod, "Osso buco alla Milanese with gremolata and saffron risotto", "complement", "established", "main", "Rich braised veal shank meets Amarone's power; gremolata's acidity provides refreshment; saffron bridges the complexity.")
    PAIR(prod, "Grilled duck breast with black cherry sauce and polenta", "complement", "classic", "main", "Duck's richness matches Amarone's weight; black cherry echoes the wine's dried fruit; polenta provides starchy balance.")
    PAIR(prod, "Risotto all'Amarone (risotto cooked in Amarone)", "complement", "classic", "main", "One of Italy's greatest self-referential pairings — Amarone in the risotto creates complete harmony with wine alongside.")
    PAIR(prod, "Aged Asiago Stravecchio or Pecorino with truffle honey", "complement", "established", "cheese", "Hard aged Italian cheese with intense Amarone — truffle honey bridges both; the wine's dried fruit contrasts the salt.")

# === SAGRANTINO DI MONTEFALCO DOCG ===
print("=== Sagrantino di Montefalco DOCG ===")
r4 = R("Sagrantino di Montefalco DOCG", "Italy", "wine",
       designation_type="DOCG",
       designation_name="Sagrantino di Montefalco Denominazione di Origine Controllata e Garantita",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Sagrantino di Montefalco, from the Umbrian hill town of Montefalco, produces Italy's most tannic wine from the indigenous Sagrantino grape — a variety with higher tannin concentration than any other in the world. The small DOCG zone covers just 700 hectares, and wines require minimum 37 months ageing (12 in oak). When made well, Sagrantino is a wine of extraordinary power, concentration, and longevity — deep black fruit, bitter chocolate, tar, and earth that can age for 20–30 years.",
       key_producers="Arnaldo Caprai, Paolo Bea, Colpetrone, Lungarotti, Antonelli San Marco",
       historical_context="Sagrantino almost disappeared from Umbria in the 20th century, with just a few hundred hectares remaining. Marco Caprai of Arnaldo Caprai revived and modernised the variety in the 1970s–80s, researching the grape's genetics and developing new viticultural and winemaking approaches that transformed Sagrantino from an obscure local wine to an internationally recognised Italian powerhouse.")
for yr, qd, pt, sn in [
    (2016,"excellent","rising","Landmark Sagrantino vintage — wines of extraordinary depth and tannin integration."),
    (2017,"very_good","stable","Good vintage; slightly lighter style of Sagrantino with good fruit-tannin balance."),
    (2018,"excellent","rising","Outstanding year; wines from Montefalco showing benchmark power and complexity."),
    (2019,"very_good","stable","Fine conditions; modern-style producers particularly successful for approachable Sagrantino."),
    (2020,"excellent","rising","One of the finest Sagrantino vintages in recent memory — tannins well-integrated with rich fruit."),
]:
    VIN(r4, yr, qd, pt, sn)

p4 = P("Arnaldo Caprai Winery", "winery", r4, "Italy",
       production_philosophy="terroir_expression",
       philosophy_description="Marco Caprai revived Sagrantino in the 1970s and turned it into an internationally recognised Italian grape. His Collepiano and 25 Anni riserva wines are the benchmark Sagrantino di Montefalco expressions, combining the grape's inherent power with modern fruit and structure.",
       reputation_narrative="Arnaldo Caprai is inseparable from Sagrantino's modern identity — without Marco Caprai's research and advocacy, the grape might have disappeared. Their 25 Anni riserva is Italy's most celebrated Sagrantino and one of the wines that put Umbria on the international fine wine map.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Arnaldo Caprai 25 Anni Sagrantino di Montefalco DOCG", "wine_still", p4, r4, "Italy",
                    subcategory="red", description="The benchmark Sagrantino — 25 Anni ('25 Years') riserva from the estate's finest parcels. Intensely concentrated: dark plum, blackberry, bitter chocolate, leather, tar, and the highest tannin of any Italian variety. Requires 10–15 years minimum for full expression.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Wild boar ragù with dark chocolate and juniper on pappardelle", "complement", "classic", "main", "Sagrantino's power demands equally powerful game; bitter chocolate in both the dish and wine creates deep harmony.")
    PAIR(prod, "Braised lamb shank with black olives, rosemary and polenta", "complement", "established", "main", "Lamb's richness handles Sagrantino's tannins; black olives echo the wine's bitter character; polenta grounds both.")
    PAIR(prod, "Aged Pecorino di Fossa matured in travertine rock", "complement", "established", "cheese", "The most tannic Italian wine needs the most flavourful cheese — aged Pecorino buried in travertine has the intensity to match.")
    PAIR(prod, "Dark chocolate and hazelnut torte with espresso cream", "complement", "classic", "dessert", "Sagrantino's bitter chocolate notes and the torte share the same dark intensity; espresso deepens the connection.")
prod, is_new = PROD("Arnaldo Caprai Collepiano Sagrantino di Montefalco", "wine_still", p4, r4, "Italy",
                    subcategory="red", description="Estate Sagrantino from hillside Collepiano vineyards — powerful but slightly more approachable than 25 Anni. Black cherry, bitter chocolate, tar, and the variety's signature gripping tannins that soften to velvet with 7+ years ageing.", price_tier="premium")
if is_new:
    PAIR(prod, "Porchetta (Umbrian whole-roasted pork) with herbs", "complement", "classic", "main", "The definitive Umbrian pairing — Sagrantino from Montefalco with the region's most famous meat preparation.")
    PAIR(prod, "Lentil and sausage soup from Umbrian castelluccio lentils", "complement", "established", "main", "Earthy Umbrian lentils with earthy Sagrantino — shared terroir flavours create a rustic, satisfying regional match.")
    PAIR(prod, "Cinghiale in umido (slow-braised boar) with truffle", "complement", "classic", "main", "Another Umbrian wild boar preparation — the region's cuisine was built around this wine.")
    PAIR(prod, "Aged Parmigiano with truffle and balsamic pearls", "complement", "established", "cheese", "Powerful tannins need the highest quality aged cheese; truffle bridges Sagrantino's earthy complexity.")

# === TAURASI DOCG ===
print("=== Taurasi DOCG ===")
r5 = R("Taurasi DOCG", "Italy", "wine",
       designation_type="DOCG",
       designation_name="Taurasi Denominazione di Origine Controllata e Garantita",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Taurasi, from the Campanian hills east of Naples, is produced from Aglianico — Italy's great southern grape, sometimes called 'the Barolo of the south'. At 400–700m altitude on clay, volcanic, and calcareous soils, Aglianico ripens late (harvest often in October-November) and produces wines of enormous tannic structure, high acidity, and dark fruit concentration. Great Taurasi requires 10–15 years to reveal its full complexity of iron, tar, dark cherry, and volcanic mineral notes.",
       key_producers="Mastroberardino, Feudi di San Gregorio, Terredora di Paolo, Caggiano, Luigi Tecce",
       historical_context="Taurasi was granted DOCG status in 1993 — it was one of the first DOCGs in southern Italy. Antonio Mastroberardino is credited with 'saving' Aglianico and Taurasi from obscurity after the 1980 Campanian earthquake devastated many vineyards. His family's 150-year history is inseparable from the grape and region's modern identity.")
for yr, qd, pt, sn in [
    (2016,"excellent","rising","Landmark Taurasi vintage — Aglianico of extraordinary mineral depth and structural complexity."),
    (2017,"very_good","stable","Good vintage; slightly warmer conditions produced wines with softer tannins accessible earlier."),
    (2018,"excellent","rising","Outstanding year; old-vine Aglianico of exceptional concentration and mineral precision."),
    (2019,"very_good","stable","Fine vintage; wines showing the classic combination of high acidity, tannin, and dark fruit."),
    (2020,"excellent","rising","One of the finest recent Taurasi vintages — wines achieving benchmark scores across the region."),
    (2021,"very_good","stable","Good conditions; Taurasi wines showing excellent ageing potential with structured tannins."),
]:
    VIN(r5, yr, qd, pt, sn)

p5 = P("Mastroberardino Winery Taurasi", "winery", r5, "Italy",
       production_philosophy="terroir_expression",
       philosophy_description="The Mastroberardino family has produced Taurasi for 150+ years and is inseparable from Aglianico's modern identity. Their Radici and Naturalis Historia cru wines are the region's benchmarks, and the family's historical work recovering Campanian indigenous varieties — Fiano di Avellino, Greco di Tufo, alongside Taurasi — is one of Italian wine's greatest achievements.",
       reputation_narrative="Mastroberardino is Italy's most significant southern Italian winery — they kept Campanian indigenous varieties alive through decades of indifference and built an estate that now defines the highest quality benchmark for Taurasi and all of Campania.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Mastroberardino Radici Taurasi DOCG", "wine_still", p5, r5, "Italy",
                    subcategory="red", description="Benchmark Taurasi from Aglianico's finest parcels — 'Radici' means 'roots', reflecting the family's 150-year connection. Deep garnet, intense — dark cherry, iron, tar, volcanic mineral, and grippy tannins requiring 10+ years for full expression. Italy's greatest southern red.", price_tier="premium")
if is_new:
    PAIR(prod, "Braised lamb with oregano, tomato and Campanian olives", "complement", "classic", "main", "The definitive Campanian pairing — Taurasi's iron and dark fruit embrace the region's slow-cooked lamb tradition.")
    PAIR(prod, "Wild boar and black truffle ragù with rigatoni", "complement", "classic", "main", "Powerful Taurasi demands powerful game; truffle's earthiness bridges the wine's volcanic mineral depth.")
    PAIR(prod, "Grilled soppressata with aged Provolone del Monaco", "complement", "established", "cheese", "Hard southern Italian cheese and Campania's greatest red — shared regional DNA creates a natural harmony.")
    PAIR(prod, "Neapolitan ragù — seven-hour meat sauce with rigatoni", "complement", "classic", "main", "The most Campanian of all pairings — Taurasi with the iconic slow-cooked Neapolitan Sunday sauce is a regional imperative.")
prod, is_new = PROD("Feudi di San Gregorio Piano di Montevergine Taurasi DOCG", "wine_still", p5, r5, "Italy",
                    subcategory="red", description="Single-vineyard Aglianico from Piano di Montevergine at 500m — Feudi's flagship Taurasi. Intensely volcanic and mineral: dark cherry, iron, licorice, leather, and fine tannins that reveal extraordinary complexity over 15+ years of cellaring.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted suckling pork (porchetta) with rosemary and garlic", "complement", "classic", "main", "High-tannin Taurasi cuts through the suckling pork's fat; rosemary bridges the wine's herbal dimension.")
    PAIR(prod, "Grilled ribeye with Campanian olive oil and sea salt", "complement", "established", "main", "The wine's iron and volcanic mineral character stands up to quality beef; olive oil bridges both the wine and meat.")
    PAIR(prod, "Aged Fiore Sardo with dried figs and hazelnuts", "complement", "established", "cheese", "Hard aged sardinian/southern Italian sheep cheese with iron-mineral Taurasi — shared rustic power creates harmony.")
    PAIR(prod, "Chocolate and espresso torte with candied orange", "complement", "adventurous", "dessert", "Dark, bitter notes in the wine bridge to espresso; orange echoes Taurasi's bright acidity even in dessert context.")

# === DB STATE ===
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — vintages: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")
print("B168 complete.")
cur.close()
conn.close()
