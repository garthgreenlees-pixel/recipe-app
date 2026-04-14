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
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === NAOUSSA PDO (Greece) ===
print("\n=== Naoussa PDO (Greece) ===")
r_naoussa = R(
    name="Naoussa",
    country="Greece",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Naoussa PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The most prestigious red wine appellation in northern Greece, located in the Imathia regional unit of Central Macedonia at the foot of Mount Vermio. Naoussa produces wines exclusively from Xinomavro — Greece's greatest and most demanding red variety, whose name translates literally as 'acid-black'. On the sandy clay and limestone soils of the Naoussa plateau at 200–350m altitude, Xinomavro achieves remarkable complexity, earning comparisons to Nebbiolo for its tannic structure, high acidity, and capacity for long aging.",
    key_producers="Kir-Yianni, Boutari, Alpha Estate, Dalamara Estate",
    historical_context="Wine production in Naoussa dates to antiquity. The modern PDO was established in 1971, making it one of Greece's earliest quality wine designations. Yiannis Boutaris transformed the region's reputation in the 1970s and 1980s by vinifying Xinomavro with modern techniques while preserving its typicity. Kir-Yianni (established when Boutaris' son broke away) has since become the region's standard-bearer."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Long, cool ripening season produced Xinomavro of exceptional finesse and mineral precision. Among the decade's finest vintages."),
    (2020, "very_good", "stable", "Warm year with good natural acidity preserved by altitude. Rich, concentrated wines with good tannic structure."),
    (2019, "excellent", "rising", "Outstanding across all quality levels. Single-vineyard wines of Burgundy-like site expression."),
    (2018, "very_good", "stable", "Classic Naoussa vintage — powerful, tannic wines requiring extended cellaring."),
    (2017, "excellent", "stable", "Late spring frosts reduced yields significantly. Concentrated, complex survivors of exceptional quality."),
]:
    VIN(r_naoussa, yr, qd, pt, sn)

p_kiryianni = P(
    name="Kir-Yianni",
    country="Greece",
    region_id=r_naoussa,
    producer_type="winery",
    description="The reference estate of Naoussa, established in 1997 when Yiannis Boutaris left the family business. Kir-Yianni produces benchmark single-vineyard Naoussa from historic parcels including the Ramnista site — one of the appellation's finest — as well as innovative blends from Xinomavro. Their research into Xinomavro's sub-varieties and the ancient Naoussa terroir has contributed enormously to understanding Greece's greatest red variety."
)
prod_kiryianni, new = PROD(
    name="Kir-Yianni Ramnista Naoussa",
    category="wine_still",
    subcategory="Xinomavro",
    producer_id=p_kiryianni,
    region_id=r_naoussa,
    origin_country="Greece",
    description="The flagship single-vineyard Naoussa — from the historic Ramnista site on deep, water-retentive clay soils. The wine is the textbook expression of aged Xinomavro: faded ruby with garnet hints, aromas of dried tomato, sun-dried olive, sour cherry, rose petal, leather, and dried herbs. The tannins are firm and structured, the acidity electric. A wine that demands food and rewards patience — one of Greece's great reds.",
    price_tier="premium"
)
if new:
    PAIR(prod_kiryianni, "Braised lamb shanks with tomato, cinnamon, and orzo", "complement", "classic", "main", "The quintessential Naoussa pairing — Xinomavro's dried tomato and sour cherry character mirror the tomato braising liquid, its firm tannins support the lamb's richness, and cinnamon bridges the wine's warm spice.")
    PAIR(prod_kiryianni, "Moussaka with béchamel and roasted aubergine", "complement", "classic", "main", "Greece's iconic layered dish is a textbook companion for aged Naoussa. The wine's structure cuts through the rich béchamel while its acidity brightens the tomato and lamb. A national pairing of genuine logic.")
    PAIR(prod_kiryianni, "Aged Graviera with sun-dried tomatoes and olives", "complement", "established", "cheese", "Hard Greek sheep's milk cheese with Naoussa — the wine's olive and dried tomato character mirrors the accompaniments exactly, while its tannic structure complements the cheese's density.")
    PAIR(prod_kiryianni, "Venison stew with dried cherries, juniper, and root vegetables", "complement", "established", "main", "Xinomavro's sour cherry and leather notes bridge naturally to game. Juniper echoes its dried herb complexity while root vegetables provide earthy grounding.")

p_alpha = P(
    name="Alpha Estate",
    country="Greece",
    region_id=r_naoussa,
    producer_type="winery",
    description="A modern Amyndeon estate producing Xinomavro in a more polished, internationally minded style than the traditional Naoussa producers. Alpha Estate's single-vineyard expressions — Hedgehog, Wade, Axia — demonstrate Xinomavro's capacity for site-specific expression comparable to Nebbiolo's relationship to its Piedmontese terroirs. The estate also produces excellent Assyrtiko white from Amyndeon's cool, high-altitude vineyards."
)
prod_alpha, new = PROD(
    name="Alpha Estate Xinomavro Hedgehog Single Vineyard Amyndeon",
    category="wine_still",
    subcategory="Xinomavro",
    producer_id=p_alpha,
    region_id=r_naoussa,
    origin_country="Greece",
    description="A single-parcel Xinomavro from the Hedgehog vineyard in Amyndeon — one of Greece's highest-altitude wine regions at 700m. The cool, continental climate produces a more elegant, aromatic style than Naoussa — with red cherry, rose water, dried herbs, mineral earth, and silky tannins that age magnificently. Among the most internationally accessible expressions of Xinomavro.",
    price_tier="premium"
)
if new:
    PAIR(prod_alpha, "Roasted duck breast with cherry reduction and lentils", "complement", "established", "main", "The wine's cherry and dried rose character mirrors the cherry reduction precisely. Lentils provide earthy grounding while duck's richness is balanced by Xinomavro's firm acidity.")
    PAIR(prod_alpha, "Lamb kofta with tabbouleh and tahini yogurt", "complement", "established", "main", "Eastern Mediterranean spiced lamb with northern Greek Xinomavro — the wine's dried herb and mineral character bridges to the herb-rich kofta while tahini's richness is cut by its acidity.")
    PAIR(prod_alpha, "Beef carpaccio with Graviera shavings, capers, and truffle oil", "bridge", "suggested", "starter", "The wine's mineral depth and dried herb notes bridge to carpaccio. Capers echo its acidity, Graviera adds nutty depth, and truffle oil bridges to its earthy complexity.")
    PAIR(prod_alpha, "Spanakopita (spinach and feta pastry) with dill and lemon", "complement", "established", "starter", "Greek pastry with Greek wine — the wine's herbal character bridges to spinach and dill, its acidity mirrors the lemon, and feta's saltiness amplifies its mineral quality.")

# === IROULÉGUY AOC (France) ===
print("\n=== Irouléguy AOC (France) ===")
r_irouleguy = R(
    name="Irouléguy",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Irouléguy AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's smallest and most dramatically situated wine appellation, tucked into the steep, terraced slopes of the French Basque Country at the foot of the Pyrenees. The vineyards — planted on dramatic south-facing schist and sandstone terraces at 200–500m — produce wines from Tannat, Cabernet Franc, and Cabernet Sauvignon for reds, and Gros Manseng and Petit Manseng for whites. The wines have a fierce mountain character — dense, tannic reds and intensely aromatic whites — that reflects both the Basque temperament and the extreme terroir.",
    key_producers="Domaine Arretxea, Domaine Ilarria, Brana, Domaine Etxegaraya",
    historical_context="Viticulture in the Basque Pyrenees dates to at least the 12th century, sustained by Benedictine monks at the monastery of Roncevaux. The appellation was granted in 1970 and represents one of the last great surviving examples of traditional Basque mountain viticulture, with many vineyards accessible only on foot and harvested by hand due to the extreme gradient."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, wet spring followed by warm, dry summer. Tannat of exceptional depth and freshness."),
    (2020, "very_good", "stable", "Good growing season with some humidity challenges. Whites from Manseng grapes particularly successful."),
    (2019, "excellent", "rising", "Outstanding vintage — hot summer tempered by Atlantic influence. Dense, structured Tannat with excellent longevity."),
    (2018, "very_good", "stable", "Warm year producing ripe, full wines. Gros Manseng whites of tropical intensity."),
    (2017, "good", "stable", "Spring frosts affected some parcels. Survivors showed good concentration and character."),
]:
    VIN(r_irouleguy, yr, qd, pt, sn)

p_arretxea = P(
    name="Domaine Arretxea",
    country="France",
    region_id=r_irouleguy,
    producer_type="winery",
    description="The most celebrated estate in Irouléguy — Michel and Thérèse Riouspeyrous's biodynamic domain on steep schist terraces above the village of Irouléguy. Their Tannat-based Haitza and Hegoxuri reds are among the finest expressions of mountain Tannat in France, showing the variety's capacity for complexity and elegance when grown on schist at altitude. The estate is a benchmark for natural, terroir-driven wine in the Basque Pyrenees."
)
prod_arretxea, new = PROD(
    name="Domaine Arretxea Haitza Irouléguy Rouge",
    category="wine_still",
    subcategory="Tannat",
    producer_id=p_arretxea,
    region_id=r_irouleguy,
    origin_country="France",
    description="The flagship red from Irouléguy's most prestigious estate — Tannat with Cabernet Franc from steep schist terraces above 400m. Biodynamically farmed and vinified with minimal intervention. Dense, aromatic, and structured with black cherry, dried violets, iron mineral, graphite, and the massive yet refined tannins that Tannat achieves at altitude on schist soils. Haitza is a wine of mountain nobility — severe in youth, magnificent with 10+ years of age.",
    price_tier="premium"
)
if new:
    PAIR(prod_arretxea, "Slow-braised Basque axoa (veal with Espelette pepper and herbs)", "complement", "classic", "main", "The quintessential regional pairing — Basque veal stew with Irouléguy Tannat. The wine's dense tannins support the rich stew, Espelette pepper bridges to its dark fruit, and herbs echo its aromatic complexity.")
    PAIR(prod_arretxea, "Txistorra (Basque chorizo) with pimientos de padrón and aioli", "complement", "classic", "starter", "Mountain charcuterie with mountain wine — Tannat's structure and dark fruit complement the spiced chorizo. Pimientos provide sweetness that bridges to the wine's fruit.")
    PAIR(prod_arretxea, "Roasted leg of Pyrenean lamb with garlic and fresh thyme", "complement", "established", "main", "Mountain lamb with mountain Tannat — both products of the Pyrenees. The wine's massive tannins and dark fruit are the ideal accompaniment to roasted lamb of similar character and provenance.")
    PAIR(prod_arretxea, "Aged Ossau-Iraty with black cherry preserve", "complement", "established", "cheese", "The most celebrated Basque cheese with the region's most celebrated wine — a pairing of obvious cultural and terroir logic. The cheese's nutty richness is balanced by Tannat's acidity, cherry preserve echoes its fruit.")

p_ilarria = P(
    name="Domaine Ilarria",
    country="France",
    region_id=r_irouleguy,
    producer_type="winery",
    description="Peio Espil's small biodynamic estate on the French-Spanish Basque border, producing intensely mineral Irouléguy from ancient schist terraces. Ilarria's wines are some of the appellation's most traditional and intense — long maceration Tannat reds and pure, aromatic Manseng whites that reflect the extreme altitude and Atlantic maritime influence of the Pyrenean foothills."
)
prod_ilarria, new = PROD(
    name="Domaine Ilarria Blanc Irouléguy",
    category="wine_still",
    subcategory="Gros Manseng",
    producer_id=p_ilarria,
    region_id=r_irouleguy,
    origin_country="France",
    description="A rare white from the Basque Pyrenees — Gros Manseng from schist terraces on the French-Spanish border. Bone dry with vivid tropical aromatics (guava, passion fruit, mango), lemon zest, Pyrenean herbs, and a schist mineral freshness that prevents any sense of heaviness. An intensely aromatic, site-specific white that has no equivalent elsewhere in France.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_ilarria, "Grilled dorade with chimichurri herbs and citrus salsa", "complement", "established", "main", "The wine's tropical fruit and herb freshness bridge perfectly to grilled Mediterranean fish. Chimichurri echoes its herbal notes while citrus mirrors its acidic brightness.")
    PAIR(prod_ilarria, "Ttoro (Basque fish stew with peppers, tomato, and saffron)", "complement", "classic", "main", "The traditional Basque fish stew from Saint-Jean-de-Luz with the appellation's white — a pairing of regional logic. The wine's tropical freshness cuts through the rich tomato-saffron broth.")
    PAIR(prod_ilarria, "Anchovies from Getaria with roasted peppers and olive oil", "complement", "established", "starter", "Basque anchovies with Basque white — the wine's mineral freshness and tropical acidity lift the salt-cured fish while roasted peppers echo its subtle sweetness.")
    PAIR(prod_ilarria, "Idiazabal cream with honey and walnuts", "bridge", "suggested", "cheese", "The wine's tropical fruit and herbal complexity bridge to Basque smoked sheep's milk cheese. Honey moderates the acidity while walnuts echo its mineral depth.")

# === DOURO DOC (Portugal) — dry table wines ===
print("\n=== Douro DOC (Portugal) ===")
r_douro = R(
    name="Douro",
    country="Portugal",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Douro DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="One of the world's great wine regions — the steep schist terraces above the Douro river in northern Portugal where Port wine has been produced for three centuries. The Douro is now equally celebrated for its unfortified table wines — dense, complex blends of indigenous varieties (Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca) that represent some of Portugal's finest dry reds. The region's extreme continental climate, poor schist soils, and ancient vine stocks create wines of extraordinary concentration, complexity, and longevity.",
    key_producers="Quinta do Crasto, Quinta do Vale Meão, Niepoort, Ramos Pinto, Quinta da Romaneira",
    historical_context="The Douro Valley received its first demarcation for Port production in 1756 under the Marquis of Pombal — making it one of the world's first officially demarcated wine regions. Unfortified table wines from the Douro only gained serious international attention from the 1990s, when the Barca Velha (Ferreira) and then Niepoort's Redoma and Charme demonstrated the region's potential for world-class dry wine."
)
for yr, qd, pt, sn in [
    (2020, "exceptional", "rising", "One of the Douro's great decades-defining vintages. Touriga Nacional of extraordinary depth and structure. Top wines will age 30+ years."),
    (2019, "excellent", "rising", "Long, warm growing season producing wines of great concentration and freshness. Outstanding across all categories."),
    (2017, "excellent", "rising", "Exceptional vintage — concentrated, structured wines of great complexity."),
    (2016, "excellent", "stable", "Balanced, elegant vintage with natural freshness. Wines of great mid-term aging potential."),
    (2015, "very_good", "stable", "Hot year producing powerful, full-bodied wines. Some lack the freshness of cooler vintages."),
]:
    VIN(r_douro, yr, qd, pt, sn)

p_crasto = P(
    name="Quinta do Crasto",
    country="Portugal",
    region_id=r_douro,
    producer_type="winery",
    description="One of the Douro's most consistently excellent table wine estates, owned by the Roquette family (also behind Herdade do Esporão in Alentejo). Quinta do Crasto's vineyards on steep schist terraces above Régua produce benchmark Douro reds — the regular Crasto, the Reserva, and the Vinha Maria Teresa and Vinha da Ponte single-vineyard old-vine wines. The estate has been a leading force in establishing the Douro as a serious fine wine region beyond Port."
)
prod_crasto, new = PROD(
    name="Quinta do Crasto Douro Reserva Old Vines Tinto",
    category="wine_still",
    subcategory="Touriga Nacional",
    producer_id=p_crasto,
    region_id=r_douro,
    origin_country="Portugal",
    description="From old-vine parcels on steep schist terraces — Touriga Nacional, Touriga Franca, Tinta Roriz, and Tinta Barroca fermented traditionally in granite lagares and aged in French oak. Dense, complex, and structured with blackberry, blueberry, violets, dark chocolate, graphite, and the signature Douro schist minerality. A wine of commanding presence that ages magnificently over 10–20 years — the textbook Douro red.",
    price_tier="premium"
)
if new:
    PAIR(prod_crasto, "Slow-braised kid goat with onion, garlic, and olive oil (chanfana)", "complement", "classic", "main", "The quintessential Douro pairing — slow-cooked kid goat from the same schist landscape as the wine. The wine's dense tannins and dark fruit complement the goat's richness while olive oil bridges its mineral quality.")
    PAIR(prod_crasto, "Grilled Iberian pork secreto with migas and roasted peppers", "complement", "established", "main", "Portuguese pork with Douro red — the wine's structure and dark fruit support the fatty richness of Iberian pork. Migas absorb the juices while peppers add sweetness.")
    PAIR(prod_crasto, "Duck rice with black olives and smoked paprika (arroz de pato)", "complement", "classic", "main", "One of Portugal's great dishes with one of Portugal's greatest wine regions — duck's richness is matched by Touriga Nacional's dark fruit and structure. Black olive echoes the wine's mineral schist character.")
    PAIR(prod_crasto, "Aged Queijo da Serra with wildflower honey", "complement", "established", "cheese", "Portugal's greatest mountain cheese with a wine of equal stature — the wine's density and dark fruit balance the cheese's pungent, runny richness. Honey moderates the wine's tannins.")

p_vale_meao = P(
    name="Quinta do Vale Meão",
    country="Portugal",
    region_id=r_douro,
    producer_type="winery",
    description="The historic estate in the Douro Superior that produced the grapes for Barca Velha — Portugal's most iconic wine — for decades under the Ferreira family. Now owned by Francisco Olazabal, Vale Meão produces the estate wine under its own label: a concentrated, powerful Douro red from ancient vines on extreme schist terraces in the high, dry Upper Douro. The wine is considered one of Portugal's finest and has established its own legendary reputation independent of the Ferreira/Barca Velha connection."
)
prod_vale_meao, new = PROD(
    name="Quinta do Vale Meão Douro Tinto",
    category="wine_still",
    subcategory="Touriga Franca",
    producer_id=p_vale_meao,
    region_id=r_douro,
    origin_country="Portugal",
    description="From the ancient Douro Superior estate — a blend of all five classic Douro varieties including Touriga Nacional, Touriga Franca, Tinta Amarela, Tinto Cão, and Tinta Roriz, fermented in traditional granite lagares. Remarkable concentration and complexity from extreme schist soils and decades-old vines. Blackberry, graphite, violet, cedar, leather, and dried herbs with a structural power that ages for 20+ years. One of the Douro's defining benchmark wines.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_vale_meao, "Whole roasted suckling pig (leitão da Bairrada) with herb salt and crackling", "complement", "classic", "main", "Portugal's most celebrated festive dish with its most prestigious dry wine — the wine's massive structure and dark complexity support the richness of suckling pig. A pairing of national significance.")
    PAIR(prod_vale_meao, "Roasted wild boar with chestnuts, dried fruit, and red wine reduction", "complement", "established", "main", "The Douro's mountain game and its greatest red — wild boar's gaminess and richness are matched by the wine's density and dark fruit. Chestnuts bridge to its earthy depth, dried fruit echoes its complexity.")
    PAIR(prod_vale_meao, "Black truffle risotto with Parmigiano and aged port reduction", "elevate", "adventurous", "main", "Port reduction bridges the wine to truffle — the wine's schist mineral depth elevates the earthy truffle, aged Parmigiano adds complexity, and the two wines complement each other through the food.")
    PAIR(prod_vale_meao, "Manchego aged 12 months with membrillo and almonds", "complement", "suggested", "cheese", "The wine's massive structure and dried fruit complexity is balanced by dense aged cheese. Membrillo echoes its dark fruit while almonds bridge its mineral depth.")

# === CANELONES (Uruguay) ===
print("\n=== Canelones (Uruguay) ===")
r_canelones = R(
    name="Canelones",
    country="Uruguay",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Canelones",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The heart of Uruguayan wine, a flat coastal department south of Montevideo where maritime influence from the Atlantic and Río de la Plata estuary moderates the subtropical climate. Canelones produces around 60% of Uruguay's wine from predominantly clay-limestone soils, and is home to the country's most celebrated estate, Bodega Garzon. Uruguay's signature grape Tannat — originally from southwest France — achieves a distinctive New World character here: fuller, rounder, and more accessible than its Madiran origins, while retaining the grape's characteristic tannic backbone and deep colour.",
    key_producers="Bodega Garzón, Bouza, Alto de la Ballena, Juanicó",
    historical_context="Basque immigrants introduced winemaking to Uruguay in the late 19th century, and Tannat arrived with them from the Pyrénées-Atlantiques. The modern wine industry only developed in the 1990s when quality-focused producers began producing internationally viable wines. Bodega Garzón's emergence as an internationally acclaimed estate brought global attention to Uruguay as a serious fine wine country."
)
for yr, qd, pt, sn in [
    (2021, "very_good", "rising", "Good vintage across Canelones. Maritime influence preserved freshness in the warm conditions."),
    (2020, "excellent", "rising", "Outstanding Tannat with remarkable depth and structure. Recognised internationally as a top Uruguayan vintage."),
    (2019, "very_good", "stable", "Balanced conditions producing wines of good structure and freshness."),
    (2018, "excellent", "stable", "Warm, dry season producing concentrated, complex Tannat with excellent aging potential."),
    (2017, "very_good", "stable", "Classic Canelones vintage — medium-bodied, fresh Tannat with good regional typicity."),
]:
    VIN(r_canelones, yr, qd, pt, sn)

p_garzon = P(
    name="Bodega Garzón",
    country="Uruguay",
    region_id=r_canelones,
    producer_type="winery",
    description="The most internationally celebrated Uruguayan wine estate, established by entrepreneur Alejandro Bulgheroni on a vast property in Maldonado department near the Atlantic coast. Bodega Garzón produces Tannat and Albariño from ancient, windswept soils with an emphasis on freshness and elegance rather than the heavy extraction common in earlier Uruguayan wines. Their Single Vineyard Tannat has been rated among South America's finest wines, and the estate's biodynamic commitment sets a standard for Uruguayan winemaking."
)
prod_garzon, new = PROD(
    name="Bodega Garzón Single Vineyard Tannat Uruguay",
    category="wine_still",
    subcategory="Tannat",
    producer_id=p_garzon,
    region_id=r_canelones,
    origin_country="Uruguay",
    description="The benchmark Uruguayan Tannat — single-vineyard selection from estate parcels on granite-influenced soils near the Atlantic coast. The wine shows how Atlantic maritime influence transforms Tannat: the massive tannins of Madiran become rounder and more approachable, yet the grape's signature dark fruit, graphite, and iron mineral remain. Blackberry, dark plum, violets, oak spice, and a distinctive coastal salinity set this apart as world-class Tannat.",
    price_tier="premium"
)
if new:
    PAIR(prod_garzon, "Asado de tira (grilled short ribs) with chimichurri and provençal salad", "complement", "classic", "main", "The most natural pairing in Uruguayan wine culture — the country's iconic barbecued beef with its signature grape variety. Chimichurri's herb and garlic echo the wine's complexity while the ribs' richness is supported by Tannat's massive tannins.")
    PAIR(prod_garzon, "Lamb chops with salsa criolla and wood-roasted vegetables", "complement", "established", "main", "Atlantic-influenced Tannat with Uruguayan lamb — the wine's rounded tannins support the lamb's richness while salsa criolla's freshness bridges to its mineral quality.")
    PAIR(prod_garzon, "Empanadas de carne with olives, hard egg, and raisins", "complement", "established", "starter", "Uruguayan filled pastry with the country's signature wine — the filling's savoury richness is matched by Tannat's dark fruit and structure. Raisins echo the wine's dried fruit complexity.")
    PAIR(prod_garzon, "Dark chocolate mousse with dulce de leche and sea salt", "complement", "suggested", "dessert", "The wine's dark fruit and graphite depth bridges to dark chocolate. Dulce de leche echoes its sweet concentration while sea salt mirrors its coastal mineral character.")

p_bouza = P(
    name="Bodega Bouza",
    country="Uruguay",
    region_id=r_canelones,
    producer_type="winery",
    description="A family winery in Canelones producing some of Uruguay's most complex and age-worthy Tannat from old-vine parcels on clay-limestone soils. The Bouza family has farmed these vineyards for three generations and the estate's old vines (planted in the 1940s–60s) produce wines of unusual depth and complexity. Their Monte Vide Eu Tannat — a prestige selection from the oldest parcels — is considered among Uruguay's most serious wines."
)
prod_bouza, new = PROD(
    name="Bodega Bouza Monte Vide Eu Tannat Uruguay",
    category="wine_still",
    subcategory="Tannat",
    producer_id=p_bouza,
    region_id=r_canelones,
    origin_country="Uruguay",
    description="The prestige Tannat from Bouza's oldest vines — planted in the 1940s on clay-limestone Canelones soils. Old-vine concentration combined with traditional winemaking (indigenous yeasts, long maceration, large French oak aging) produces a wine of unusual depth and complexity. Blackberry, cedar, dark chocolate, iron mineral, dried violets, and a structural power that ages magnificently. One of the most authentic expressions of old-vine Tannat outside Madiran.",
    price_tier="premium"
)
if new:
    PAIR(prod_bouza, "Whole roasted rack of lamb with charred herbs and aioli", "complement", "classic", "main", "Old-vine Tannat with roasted lamb is a cross-continental classic — the same pairing logic as Madiran, transferred to the Atlantic coast of South America. The wine's massive structure supports the lamb's richness.")
    PAIR(prod_bouza, "Boeuf bourguignon-style beef cheeks with root vegetables and bone marrow toast", "complement", "established", "main", "Rich braised beef demands structured tannins — old-vine Canelones Tannat provides exactly the backbone needed, while its dark fruit complexity bridges the red wine braising flavours.")
    PAIR(prod_bouza, "Aged Colonia cheese with guayabo paste and toasted almonds", "complement", "established", "cheese", "Uruguayan hard cheese with old-vine Tannat — the wine's density and dark fruit are balanced by the cheese's firm, nutty character. Guayabo paste echoes its dark fruit concentration.")
    PAIR(prod_bouza, "Morcilla (blood sausage) with caramelised onions and pine nuts", "complement", "established", "main", "Iron-rich blood sausage with iron-mineral old-vine Tannat — a pairing of obvious affinity. The wine's dark fruit and graphite cut through the sausage's richness while pine nuts bridge its mineral complexity.")

# === RIBEIRA SACRA DO (Spain) ===
print("\n=== Ribeira Sacra DO (Spain) ===")
r_ribeira_sacra = R(
    name="Ribeira Sacra",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Ribeira Sacra DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The most dramatic wine region in Spain — vertiginous slate terraces carved into the gorges of the Sil and Miño rivers in Galicia, where 70-degree slopes have been cultivated since Roman times. Ribeira Sacra produces Mencía reds of unique character: lighter in body than Bierzo, more perfumed and silky, with an earthy-floral quality that has drawn comparisons to Burgundy Pinot Noir. Godello is the white variety of note. The region's extreme viticulture — heroic, terraced, and often accessible only by boat — results in wines of genuine character from some of Spain's most striking landscape.",
    key_producers="Dominio do Bibei, Guímaro, Ronsel do Sil, Algueira",
    historical_context="The name Ribeira Sacra ('Sacred Riverbank') refers to the many Romanesque monasteries that sustained viticulture in these river gorges through the medieval period. Wine production here is documented from the Roman era, and the region's extreme terraced vineyards represent one of Europe's greatest examples of human landscape modification in pursuit of wine. The DO was established in 1996."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool vintage producing the most elegant, aromatic Mencías of recent memory. Extraordinary precision and aging potential."),
    (2020, "very_good", "stable", "Warm year with some rain challenges. Best wines showed excellent freshness from the river gorge microclimate."),
    (2019, "excellent", "rising", "Outstanding vintage — long, cool ripening season produced Mencía of extraordinary perfume and mineral depth."),
    (2018, "very_good", "stable", "Classic Ribeira Sacra vintage — medium-bodied, perfumed wines for earlier drinking."),
    (2017, "excellent", "stable", "Reduced yields from spring frost produced concentrated, site-specific wines of excellent quality."),
]:
    VIN(r_ribeira_sacra, yr, qd, pt, sn)

p_bibei = P(
    name="Dominio do Bibei",
    country="Spain",
    region_id=r_ribeira_sacra,
    producer_type="winery",
    description="The most internationally celebrated estate in Ribeira Sacra — Javier Domínguez's recovery project in the remote Bibei valley, replanting ancient terraced vineyards abandoned after phylloxera and the rural depopulation of the 20th century. Working biodynamically with old vines of Garnacha Tintorera, Mencía, and indigenous whites, Dominio do Bibei produces wines of extraordinary concentration and mineral depth. The prestige Lalama blends multiple varieties from the highest granite and schist terraces."
)
prod_bibei, new = PROD(
    name="Dominio do Bibei Lalama Ribeira Sacra",
    category="wine_still",
    subcategory="Mencía",
    producer_id=p_bibei,
    region_id=r_ribeira_sacra,
    origin_country="Spain",
    description="The flagship wine from Ribeira Sacra's most prestigious estate — a blend of Mencía, Garnacha Tintorera, Mouratón, and Brancellao from ancient terraced vineyards on granite and schist soils in the Bibei valley. Dark, complex, and mineral with black cherry, dried flowers, iron mineral, graphite, and an earthy depth that speaks of very old vines and extreme terroir. Fermented with indigenous yeasts in traditional open vessels, aged in French oak. A wine of rare authenticity.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_bibei, "Slow-roasted lamb with garlic scapes and roasted root vegetables", "complement", "classic", "main", "Galician lamb from the same mountain landscape as the vineyard — the wine's floral, mineral character elevates delicate mountain lamb. Garlic scapes add aromatic depth without competing.")
    PAIR(prod_bibei, "Grilled Galician octopus with olive oil, smoked paprika, and potato", "complement", "classic", "main", "Pulpo a la gallega is Galicia's most iconic dish — matched with one of its finest wines. The wine's mineral slate quality and iron notes bridge the octopus's oceanic character while paprika echoes its spice.")
    PAIR(prod_bibei, "Wild mushroom fricassee with polenta and truffle oil", "complement", "established", "main", "The wine's earthy, mineral depth mirrors the forest mushroom character. Truffle oil bridges to its aromatic complexity while polenta provides a base that absorbs both.")
    PAIR(prod_bibei, "Tetilla (Galician fresh cheese) with quince and walnuts", "bridge", "suggested", "cheese", "Galician fresh cow's milk cheese with Galician red wine — the wine's freshness and mineral quality complement Tetilla's mild creaminess. Quince echoes its cherry fruit while walnuts mirror its mineral depth.")

p_guimaro = P(
    name="Guímaro",
    country="Spain",
    region_id=r_ribeira_sacra,
    producer_type="winery",
    description="Pedro Rodríguez Pérez's family estate on the steep slate terraces of the Ribeira Sacra sub-zone of Chantada, producing some of the appellation's most precise and aromatic Mencías. Guímaro's wines are celebrated for their combination of elegance and depth — the result of old vines (50–80 years), slate soils, and winemaking that emphasises freshness over extraction. The Pezas da Portela single-vineyard wine from 80-year-old vines is considered one of Spain's great underrated single-vineyard reds."
)
prod_guimaro, new = PROD(
    name="Guímaro Mencía Ribeira Sacra",
    category="wine_still",
    subcategory="Mencía",
    producer_id=p_guimaro,
    region_id=r_ribeira_sacra,
    origin_country="Spain",
    description="The benchmark entry-level expression of Ribeira Sacra Mencía — from 50-year-old vines on steep slate terraces above the Sil river. Light ruby with a brilliant translucency that belies its depth. Aromatic and perfumed with red cherry, violets, iron mineral, slate, and wild herbs. Light-textured, silky tannins, and electric acidity that speaks of the slate soils and river gorge microclimate. One of Spain's most approachable yet genuinely interesting reds.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_guimaro, "Chilled patatas con chorizo and Padrón peppers", "complement", "classic", "starter", "The wine's freshness and light body suit simple, rustic Galician tapas. Chorizo's spice echoes Mencía's red fruit while Padrón peppers add vegetal freshness that mirrors the wine's herbal notes.")
    PAIR(prod_guimaro, "Steamed Galician mussels with white wine and parsley", "complement", "established", "starter", "The wine's mineral slate character and light body are ideal for delicate shellfish — a counterintuitive but classically Galician pairing. The oceanic mussels amplify the wine's mineral quality.")
    PAIR(prod_guimaro, "Caldo gallego (Galician white bean and turnip greens soup)", "complement", "established", "main", "Regional soup with regional wine — the wine's earthy depth and mineral freshness complement the soup's humble, hearty character. Turnip greens bridge to the wine's herbal notes.")
    PAIR(prod_guimaro, "Roasted chicken with lemon, thyme, and Galician potatoes", "complement", "established", "main", "Light-bodied Mencía is ideal for chicken — the wine's red fruit and herbal character complement roasted poultry without overwhelming it. Lemon brightens the pairing while thyme echoes the wine's herb notes.")

# Final counts
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
print("\nDone.")
cur.close()
conn.close()
