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

# ── B127 ─────────────────────────────────────────────────────────────────────
# Targets: Eger (Hungary), Eger Bikavér (Hungary),
#          Dealu Mare (Romania), Douro Superior (Portugal), Alentejo (Portugal)

# 1. EGER — Hungary
print("=== Eger ===")
r1 = R("Eger", "Hungary", "wine",
        designation_type="PDO",
        designation_name="Eger",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Hungary's most famous wine region, in the volcanic mountains of northern Hungary near the Czech border. Famous for Egri Bikavér (Bull's Blood) — a blend led by Kékfrankos (Blaufränkisch) and other varieties. Modern producers have elevated the appellation with single-vineyard expressions and the Egri Csillag white blend from indigenous varieties. Furmint, Olaszrizling and the aromatic Leányka grape produce interesting whites.",
        key_producers="Tibor Gál, GIA Winery, Thummerer, St. Andrea, Kovács Nimród",
        historical_context="Eger's wine history dates to the 13th century. The legend of 'Bull's Blood' comes from the 1552 Ottoman siege — Turks reportedly believed the defenders' red-stained beards came from drinking bull's blood rather than wine. The modern quality revival began in the 1990s with producers like Tibor Gál returning from Italian wine apprenticeships.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"very_good","rising"),(2022,"excellent","rising")]:
    VIN(r1, yr, qd, pt, f"Eger {yr}: volcanic northern Hungary; Kékfrankos and indigenous varieties showing freshness and mineral character")

p1a = P("St. Andrea Winery", "winery", r1, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="Eger's leading quality estate; Merengő and Áldás single-vineyard Egri Bikavér set the benchmark for the appellation.",
        reputation_narrative="György Lőrincz's St. Andrea is consistently Eger's finest producer; their single-vineyard Bikavér selections are internationally acclaimed.",
        price_positioning="premium")
pr1a1, n = PROD("St. Andrea Merengő Egri Bikavér", "wine_still", p1a, r1, "Hungary",
                subcategory="Kékfrankos-Cabernet Franc blend", price_tier="premium",
                description="Merengő single-vineyard Bikavér; Kékfrankos-led blend with dark cherry, volcanic mineral, iron and fine-grained tannins from volcanic tufa.")
if n:
    PAIR(pr1a1, "Mangalica pork chop with paprika sauce", "complement", "classic", "main", "Hungarian Mangalica heritage pig and Eger's finest red; the great local pairing")
    PAIR(pr1a1, "Beef pörkölt with egg noodles", "complement", "classic", "main", "Bull's Blood and the national paprika beef stew; an enduring Hungarian tradition")
    PAIR(pr1a1, "Wild boar goulash with sour cream", "complement", "established", "main", "Volcanic mineral Kékfrankos stands up beautifully to wild boar goulash")
    PAIR(pr1a1, "Grilled lamb ribs with paprika and cumin", "complement", "established", "main", "Iron-mineral Bikavér and spiced lamb; a satisfying Northern Hungarian combination")

pr1a2, n = PROD("St. Andrea Egri Csillag Blanc", "wine_still", p1a, r1, "Hungary",
                subcategory="Leányka-Olaszrizling-Hárslevelu blend", price_tier="mid_range",
                description="Egri Csillag white blend from indigenous Eger varieties; fresh apple, citrus and floral notes with mineral acidity from volcanic soils.")
if n:
    PAIR(pr1a2, "Halászlé (Eger-style spiced fish soup)", "complement", "classic", "main", "The Eger region's spiced freshwater fish soup meets its natural white wine companion")
    PAIR(pr1a2, "Fried catfish with dill sour cream", "complement", "established", "main", "Fresh mineral white lifts Hungarian freshwater catfish dishes with light acidity")
    PAIR(pr1a2, "Túrós rétes (cottage cheese strudel)", "complement", "established", "dessert", "Aromatic Eger white complements the creamy-sweet filling of Hungarian cheese strudel")
    PAIR(pr1a2, "Chicken paprikash white wine version", "complement", "established", "main", "Egri Csillag pairs naturally with white paprikash's cream and herb profile")

p1b = P("Kovács Nimród Winery", "winery", r1, "Hungary",
        production_philosophy="terroir_driven",
        philosophy_description="Modern Eger estate; Monopole single-vineyard and JK Egri Bikavér demonstrate the appellation's full potential.",
        reputation_narrative="Nimród Kovács is one of Eger's most exciting producers; his wines show how modern techniques enhance rather than diminish the region's volcanic character.",
        price_positioning="mid_range")
pr1b1, n = PROD("Kovács Nimród Monopole Egri Bikavér", "wine_still", p1b, r1, "Hungary",
                subcategory="Kékfrankos-Merlot-Cabernet Franc", price_tier="premium",
                description="Monopole Bikavér from a single hill in Eger; concentrated cherry, spice and volcanic mineral with a long structured finish.")
if n:
    PAIR(pr1b1, "Smoked pork knuckle with sauerkraut", "complement", "established", "main", "Structured Bikavér's dark fruit and iron cut through the rich smoked pork")
    PAIR(pr1b1, "Roast duck with braised red cabbage", "complement", "established", "main", "Medium-full Eger red and duck with red cabbage; a Central European autumn classic")
    PAIR(pr1b1, "Stuffed peppers with tomato sauce (töltött paprika)", "complement", "classic", "main", "The iconic Hungarian dish with an equally iconic Eger red wine")
    PAIR(pr1b1, "Aged Manchego or aged Gouda", "complement", "established", "cheese", "Structured volcanic Bikavér pairs with any medium-firm aged cheese")

pr1b2, n = PROD("Kovács Nimród JK Olaszrizling Eger", "wine_still", p1b, r1, "Hungary",
                subcategory="Olaszrizling", price_tier="mid_range",
                description="JK Olaszrizling from volcanic Eger soils; crisp apple, almond and mineral freshness — Hungary's most planted white grape at its best.")
if n:
    PAIR(pr1b2, "Fogas (Zander) in sour cream sauce", "complement", "classic", "main", "Hungary's great freshwater fish and the country's most traditional white wine")
    PAIR(pr1b2, "Fried breaded chicken (csirkemell rántva)", "complement", "established", "main", "Crisp fresh Olaszrizling and fried chicken; the everyday Hungarian table combination")
    PAIR(pr1b2, "Cucumber salad with vinegar and dill", "complement", "established", "starter", "Crisp mineral white mirrors the vinegar freshness of Hungarian uborka saláta")
    PAIR(pr1b2, "Lángos topped with sour cream and gouda", "complement", "suggested", "casual", "Refreshing Olaszrizling cleanses the richness of fried lángos with cheese")

# 2. DEALU MARE — Romania
print("=== Dealu Mare ===")
r2 = R("Dealu Mare", "Romania", "wine",
        designation_type="DOC",
        designation_name="Dealu Mare",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The most important wine region in Romania, in the sub-Carpathian hills north of Bucharest in Prahova County. The name means 'Great Hill' and the region's gently rolling slopes on clay and limestone produce some of Romania's best Fetească Neagră (indigenous black grape), Cabernet Sauvignon and Merlot. Fetească Neagră at its best produces wines of dark fruit, earthy complexity and ageing potential comparable to Côtes-du-Rhône or Languedoc. The region also produces whites from Fetească Albă and Fetească Regală.",
        key_producers="Davino, Licorna Winehouse, Lacerta, Cramele Halewood, Rhein Extra",
        historical_context="Dealu Mare has been documented as a wine region since the 15th century. Communist collectivisation damaged quality but the region has seen dramatic improvement since the 1990s. Davino and Licorna emerged as quality leaders in the 2000s. International interest in indigenous Romanian varieties is growing steadily.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"very_good","stable"),(2022,"excellent","rising")]:
    VIN(r2, yr, qd, pt, f"Dealu Mare {yr}: sub-Carpathian harvest; Fetească Neagră shows dark fruit and earthy mineral character")

p2a = P("Davino Winery", "winery", r2, "Romania",
        production_philosophy="terroir_driven",
        philosophy_description="Romania's most internationally recognised winery; Flamboyant and Revelație are benchmark Fetească Neagră expressions.",
        reputation_narrative="Florin Bauer's Davino estate has put Romanian wine on the international map; Revelație is Romania's most acclaimed and collected red wine.",
        price_positioning="premium")
pr2a1, n = PROD("Davino Revelație Fetească Neagră", "wine_still", p2a, r2, "Romania",
                subcategory="Fetească Neagră", price_tier="premium",
                description="Revelație from old Fetească Neagră vines; extraordinary dark plum, forest floor, black pepper and mineral depth — Romania's great indigenous red.")
if n:
    PAIR(pr2a1, "Sarmale (stuffed cabbage with pork and rice)", "complement", "classic", "main", "Romania's national dish finds its natural companion in the country's finest red")
    PAIR(pr2a1, "Miel la cuptor (oven-roasted lamb)", "complement", "established", "main", "Dark mineral Fetească Neagră and Romanian Easter lamb roast; a seasonal tradition")
    PAIR(pr2a1, "Grilled mici (Romanian spiced meatballs)", "complement", "classic", "main", "The beloved Romanian mici with Fetească Neagră is a summer terrace classic")
    PAIR(pr2a1, "Aged Cașcaval cheese with olives", "complement", "established", "cheese", "Romania's aged yellow cheese finds harmony with Fetească Neagră's dark fruit")

pr2a2, n = PROD("Davino Domaine Ceptura Rouge", "wine_still", p2a, r2, "Romania",
                subcategory="Fetească Neagră-Cabernet Sauvignon", price_tier="mid_range",
                description="Entry Davino red; Fetească Neagră and Cabernet Sauvignon with ripe cherry, dark plum and accessible tannins.")
if n:
    PAIR(pr2a2, "Tocăniță de porc (pork stew with vegetables)", "complement", "established", "main", "Approachable Fetească Neagră blend suits traditional Romanian pork stew")
    PAIR(pr2a2, "Grilled pork neck (ceafă de porc)", "complement", "classic", "main", "Pork neck steak and Dealu Mare red; Romania's favourite barbecue combination")
    PAIR(pr2a2, "Plăcintă cu carne (Romanian meat pie)", "complement", "established", "main", "Everyday Romanian red and the traditional savoury meat pastry")
    PAIR(pr2a2, "Grilled mushrooms with garlic and parsley", "complement", "established", "main", "Earth-forward Fetească Neagră and forest mushrooms; a natural pairing")

p2b = P("Lacerta Winery", "winery", r2, "Romania",
        production_philosophy="terroir_driven",
        philosophy_description="Dealu Mare estate in Ceptura; aged Fetească Neagră and Grand Vin are the flagship; also interesting white from Fetească Albă.",
        reputation_narrative="Lacerta produces some of Dealu Mare's most consistent quality wines; their Fetească Neagră is praised for its elegance rather than power.",
        price_positioning="mid_range")
pr2b1, n = PROD("Lacerta Fetească Neagră Dealu Mare", "wine_still", p2b, r2, "Romania",
                subcategory="Fetească Neagră", price_tier="mid_range",
                description="Elegant Dealu Mare Fetească Neagră; red cherry, plum, spice and a mineral backbone from clay-limestone soils.")
if n:
    PAIR(pr2b1, "Ciorba de burta (tripe soup with vinegar)", "complement", "suggested", "starter", "The regional tradition of strong flavours with local red wine")
    PAIR(pr2b1, "Roast chicken with vegetables and herbs", "complement", "established", "main", "Approachable red complements the simplicity of herb-roasted Romanian chicken")
    PAIR(pr2b1, "Pastramă de oaie (smoked mutton) with bread", "complement", "classic", "main", "Smoked mutton and Fetească Neagră; a classic Romanian alpine combination")
    PAIR(pr2b1, "Pizza with chorizo and peppers", "complement", "established", "casual", "Light Dealu Mare red is a versatile everyday pizza companion")

pr2b2, n = PROD("Lacerta Fetească Albă Dealu Mare", "wine_still", p2b, r2, "Romania",
                subcategory="Fetească Albă", price_tier="mid_range",
                description="Indigenous Fetească Albă white; aromatic with peach blossom, citrus and a gentle spice — Romania's best native white grape.")
if n:
    PAIR(pr2b2, "Ciorba de văcuță (beef vegetable soup)", "complement", "established", "starter", "Fresh Romanian white is the natural aperitif before the traditional soup course")
    PAIR(pr2b2, "Grilled trout from mountain streams", "complement", "established", "main", "Fresh indigenous white and Carpathian mountain trout; a pure Romanian pairing")
    PAIR(pr2b2, "Mämäligă (polenta) with bryndza cheese", "complement", "classic", "main", "The great Romanian comfort dish; cornmeal and sheep's cheese with local white wine")
    PAIR(pr2b2, "Stuffed mushrooms with herbs and cheese", "complement", "established", "main", "Aromatic Fetească Albă complements herb-stuffed mushrooms with gentle precision")

# 3. DOURO SUPERIOR — Portugal
print("=== Douro Superior ===")
r3 = R("Douro Superior", "Portugal", "wine",
        designation_type="DOC",
        designation_name="Douro Superior",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The driest and most remote of the three Douro sub-zones, stretching toward the Spanish border in the upper Douro valley. The extreme continental climate (scorching summers, freezing winters) produces the most concentrated and powerful Douro table wines. Indigenous varieties — Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca — on steep schist terraces. The sub-zone was long reserved for port production but table wine producers have revealed extraordinary dry wine potential.",
        key_producers="Quinta do Crasto, Quinta Vallado, Quinta de la Rosa, Niepoort (Dócil), Prats & Symington",
        historical_context="Douro Superior remained largely unexplored for table wines until the late 1990s. The demarcated Douro region (1756) was the world's first delimited wine region. The sub-zone's extreme conditions deterred table wine producers for decades; the discovery that indigenous varieties could produce complex dry reds has transformed this remote landscape.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r3, yr, qd, pt, f"Douro Superior {yr}: extreme continental climate; concentrated schist-grown reds of extraordinary depth")

p3a = P("Quinta do Crasto", "winery", r3, "Portugal",
        production_philosophy="terroir_driven",
        philosophy_description="Benchmark Douro Superior estate; Reserva and single-vineyard Vinha Maria Teresa are the prestige expressions.",
        reputation_narrative="The Roquette and Bergqvist families' Crasto is one of the Douro's most consistently excellent estates; Maria Teresa from ancient ungrafted vines is a world classic.",
        price_positioning="premium")
pr3a1, n = PROD("Quinta do Crasto Maria Teresa Vinha", "wine_still", p3a, r3, "Portugal",
                subcategory="Touriga Nacional-Tinta Roriz blend", price_tier="ultra_premium",
                description="From pre-phylloxera ungrafted vines in the Superior; extraordinary depth of dark fruit, mineral schist and a structure for 20+ years of ageing.")
if n:
    PAIR(pr3a1, "Roast kid (cabrito assado) with potatoes", "complement", "classic", "main", "Portugal's festive roasted kid with the Douro's great table wine; a national celebration")
    PAIR(pr3a1, "Bacalhau com natas (salt cod gratin)", "complement", "established", "main", "The great Portuguese salt cod and cream gratin finds its Douro red companion")
    PAIR(pr3a1, "Slow-roasted leg of lamb with rosemary", "complement", "established", "main", "Ungrafted Douro reds and slow-roasted lamb; the timeless Iberian tradition")
    PAIR(pr3a1, "Aged Serra da Estrela cheese", "complement", "classic", "cheese", "Portugal's great mountain cheese meets the Douro's most profound red wine")

pr3a2, n = PROD("Quinta do Crasto Reserva Old Vines Douro", "wine_still", p3a, r3, "Portugal",
                subcategory="Touriga Nacional-Touriga Franca blend", price_tier="premium",
                description="Old-vine Reserva from Douro Superior; intense dark fruit, mineral schist and structured tannins — the benchmark accessible Crasto expression.")
if n:
    PAIR(pr3a2, "Grilled chouriço with crusty broa bread", "complement", "classic", "main", "Smoked Portuguese sausage and Douro red; the most natural combination at any table")
    PAIR(pr3a2, "Roast pork loin with garlic and olive oil", "complement", "classic", "main", "Portuguese roast pork and Douro red; Sunday tradition across the Trás-os-Montes")
    PAIR(pr3a2, "Alheira sausage with grelos (turnip greens)", "complement", "established", "main", "The traditional northern Portuguese sausage plate with Douro red")
    PAIR(pr3a2, "Migas de pão (bread-based alentejana stew)", "complement", "established", "main", "Hearty Portuguese bread stew finds balance in concentrated Douro red")

p3b = P("Quinta de la Rosa", "winery", r3, "Portugal",
        production_philosophy="terroir_driven",
        philosophy_description="Family Douro estate; la Rosa Reserva and Finest Reserve Port are both benchmark; dry reds show concentrated schist character.",
        reputation_narrative="Sophia Bergqvist's family estate has produced both acclaimed port and Douro table wines for generations; consistently reliable quality.",
        price_positioning="premium")
pr3b1, n = PROD("Quinta de la Rosa Douro Reserva", "wine_still", p3b, r3, "Portugal",
                subcategory="Touriga Nacional-Tinta Roriz", price_tier="premium",
                description="La Rosa Reserva; dark cherry, plum, schist mineral and firm structure — a fine Douro Superior expression at accessible price.")
if n:
    PAIR(pr3b1, "Francesinha (Porto-style meat sandwich in sauce)", "complement", "classic", "main", "The iconic Porto street food sandwich meets its natural Douro red companion")
    PAIR(pr3b1, "Tripas à moda do Porto (tripe and bean stew)", "complement", "classic", "main", "The defining Porto dish and its traditional Douro red wine; inseparable")
    PAIR(pr3b1, "Grilled octopus with olive oil and paprika", "complement", "classic", "main", "Portuguese grilled polvo and Douro red; the coastal-meets-inland tradition")
    PAIR(pr3b1, "Bife à Portuguesa (sirloin with egg and ham)", "complement", "established", "main", "The classic Portuguese beef dish finds its natural Douro regional companion")

pr3b2, n = PROD("Quinta de la Rosa Finest Reserve Port", "wine_fortified", p3b, r3, "Portugal",
                subcategory="Finest Reserve Port", price_tier="mid_range",
                description="La Rosa Finest Reserve Ruby Port; ripe red and black fruit with chocolate and spice — approachable and warming.")
if n:
    PAIR(pr3b2, "Dark chocolate fondant with raspberries", "complement", "classic", "dessert", "Ruby Port and dark chocolate is one of the world's great dessert wine pairings")
    PAIR(pr3b2, "Stilton cheese with walnuts", "contrast", "classic", "cheese", "Port and Stilton; Britain's greatest wine and cheese tradition of two centuries")
    PAIR(pr3b2, "Christmas pudding with brandy butter", "complement", "classic", "dessert", "Fine Port's festive warmth is the traditional companion for Christmas pudding")
    PAIR(pr3b2, "Tarte de amêndoa (Portuguese almond tart)", "complement", "classic", "dessert", "Almond tart from the Algarve meets its natural Port companion")

# 4. ALENTEJO — Portugal
print("=== Alentejo ===")
r4 = R("Alentejo", "Portugal", "wine",
        designation_type="DOC",
        designation_name="Alentejo",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The vast cork oak plains of southern Portugal, between Lisbon and the Algarve. Eight sub-regions including Redondo, Reguengos, Évora and Borba; the best wines come from elevated vineyards and modern temperature-controlled estates. Alicante Bouschet (deep red colour), Aragonez (Tempranillo), Trincadeira and Antão Vaz for whites produce Portugal's most internationally successful wines after port. Remarkable value at all price levels; some prestige estates rival the Douro.",
        key_producers="Herdade do Esporão, Herdade da Malhadinha Nova, Quinta do Mouro, João Portugal Ramos, Cortes de Cima",
        historical_context="Alentejo winemaking was largely cooperative-based until the quality revolution of the 1980s-90s. Investment in modern technology transformed the appellation dramatically. Herdade do Esporão was the catalyst for quality wine, proving the region's potential internationally. The sub-region of Portalegre (Serra de São Mamede mountains) produces especially interesting wines.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"exceptional","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Alentejo {yr}: southern Portugal plains; ripe concentrated reds from ancient granitic and schist soils")

p4a = P("Herdade do Esporão", "winery", r4, "Portugal",
        production_philosophy="organic",
        philosophy_description="Organic Alentejo leader; Reserva and Vinha da Defesa are benchmarks; Monte Velho is Portugal's most exported brand.",
        reputation_narrative="João Roquette's Esporão is Portugal's most internationally recognised estate after the Port houses; certified organic across all production.",
        price_positioning="premium")
pr4a1, n = PROD("Herdade do Esporão Reserva Tinto", "wine_still", p4a, r4, "Portugal",
                subcategory="Aragonez-Trincadeira-Alicante Bouschet", price_tier="premium",
                description="Flagship Esporão Reserva; Aragonez and Alicante Bouschet with ripe plum, chocolate, mineral and a structure that rewards 10 years of ageing.")
if n:
    PAIR(pr4a1, "Carne de porco à alentejana (pork with clams)", "complement", "classic", "main", "Portugal's greatest surf-and-turf combination with its natural Alentejo companion")
    PAIR(pr4a1, "Migas alentejanas (bread porridge with pork)", "complement", "classic", "main", "The great Alentejo bread-and-pork dish and its natural regional wine")
    PAIR(pr4a1, "Grilled black pork (porco preto) entrecôte", "complement", "classic", "main", "The Alentejo's prized black ibérico pig and Esporão Reserva; the prestige pairing")
    PAIR(pr4a1, "Queijo de Évora (aged sheep's cheese)", "complement", "classic", "cheese", "The local hard sheep's cheese from Évora with the region's benchmark red")

pr4a2, n = PROD("Herdade do Esporão Monte Velho Branco", "wine_still", p4a, r4, "Portugal",
                subcategory="Antão Vaz-Roupeiro", price_tier="value",
                description="Approachable Alentejo white; Antão Vaz and Roupeiro with tropical fruit, citrus and a refreshing finish — Portugal's bestselling export white.")
if n:
    PAIR(pr4a2, "Açorda alentejana (bread soup with egg and coriander)", "complement", "classic", "main", "The fundamental Alentejo white wine accompaniment to the region's bread soup")
    PAIR(pr4a2, "Grilled fresh sardines", "complement", "classic", "main", "Portuguese white and grilled sardines; the most iconic national combination")
    PAIR(pr4a2, "Camarão com alho (garlic prawns)", "complement", "classic", "main", "Garlic prawns and fresh Alentejo white; the casual Portuguese seafood tradition")
    PAIR(pr4a2, "Ensopado de borrego (lamb stew with bread)", "complement", "established", "main", "Surprisingly good white-with-lamb: Monte Velho's freshness brightens lamb stew")

p4b = P("Herdade da Malhadinha Nova", "winery", r4, "Portugal",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Alentejo boutique estate; Monte da Peceguina and Malhadinha are prestige expressions from estate granite soils.",
        reputation_narrative="Paulo and Miguel Soares Franco's family estate produces some of Alentejo's most elegant and serious wines; biodynamic certification since 2007.",
        price_positioning="ultra_premium")
pr4b1, n = PROD("Malhadinha Nova Monte da Peceguina", "wine_still", p4b, r4, "Portugal",
                subcategory="Aragonez-Syrah blend", price_tier="ultra_premium",
                description="Flagship biodynamic Alentejo; Aragonez and Syrah from granite terraces — concentrated, mineral and among Portugal's finest modern expressions.")
if n:
    PAIR(pr4b1, "Suckling pig (leitão à Bairrada style)", "complement", "established", "main", "Portugal's prestige red with its finest roasted pork; a celebratory national pairing")
    PAIR(pr4b1, "Roast rack of lamb with garlic confit", "complement", "established", "main", "Biodynamic Alentejo and herb-roasted lamb; the prestige version of the classic")
    PAIR(pr4b1, "Venison loin with juniper and port jus", "complement", "established", "main", "Monte da Peceguina's depth and mineral suit venison's earthy game character")
    PAIR(pr4b1, "Serra da Estrela cheese fondue", "complement", "established", "main", "Portugal's great mountain cheese fondue meets its finest Alentejo red")

pr4b2, n = PROD("Malhadinha Nova Alentejo Branco", "wine_still", p4b, r4, "Portugal",
                subcategory="Antão Vaz-Arinto", price_tier="premium",
                description="Biodynamic Alentejo white; Antão Vaz and Arinto with tropical citrus, white peach and a refreshing mineral structure from granite soils.")
if n:
    PAIR(pr4b2, "Linguado grelhado (grilled sole) with butter", "complement", "established", "main", "Elegant biodynamic white and delicate sole; the prestige Alentejo fish pairing")
    PAIR(pr4b2, "Cataplana de marisco (seafood stew in copper pot)", "complement", "classic", "main", "The great Portuguese cataplana seafood stew and its natural Alentejo white")
    PAIR(pr4b2, "Bacalhau assado (oven-baked salt cod)", "complement", "established", "main", "Biodynamic white and the Portuguese salt cod tradition; a natural pairing")
    PAIR(pr4b2, "Ovos moles de Aveiro (egg yolk sweets)", "complement", "suggested", "dessert", "Tropical citrus Antão Vaz complements the rich egg-and-sugar pastry sweets")

# 5. RIAS BAIXAS — Spain
print("=== Rias Baixas ===")
r5 = R("Rias Baixas", "Spain", "wine",
        designation_type="DO",
        designation_name="Rias Baixas",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Galicia's Atlantic-influenced white wine appellation, home of Albariño — Spain's most internationally celebrated white variety. The ría (estuary) influence brings maritime humidity and sea breezes to vineyards grown on granite pergolas. Five sub-zones; Val do Salnés is the heartland. Albariño produces wines of vibrant citrus, peach blossom, saline mineral and bright acidity that are the ideal seafood companion. Rías Baixas whites age exceptionally well in top examples.",
        key_producers="Pazo de Señoráns, Domaine do Ferreiro, Lusco do Miño, Terras Gauda, Forjas del Salnés",
        historical_context="Rías Baixas was established as a DO in 1988. Albariño was nearly unknown outside Galicia before this point; its international breakthrough came rapidly through distribution in Spanish seafood restaurants globally. The variety's origin is disputed — local legend says Cistercian monks brought it from the Rhine valley, but DNA analysis suggests it is indigenous to Galicia.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","stable"),(2021,"very_good","stable"),(2022,"exceptional","rising")]:
    VIN(r5, yr, qd, pt, f"Rías Baixas {yr}: Atlantic Galicia harvest; Albariño shows vibrant citrus and saline mineral character")

p5a = P("Pazo de Señoráns", "winery", r5, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The reference Val do Salnés estate; Selección de Añada aged Albariño demonstrates the variety's exceptional ageing potential.",
        reputation_narrative="Marisol Bueno's estate is Rías Baixas's most celebrated; Selección de Añada aged 7 years showed Albariño's Burgundy-like ageing potential to the world.",
        price_positioning="premium")
pr5a1, n = PROD("Pazo de Señoráns Selección de Añada Albariño", "wine_still", p5a, r5, "Spain",
                subcategory="Albariño", price_tier="ultra_premium",
                description="Aged Albariño from multiple vintages; extraordinary complexity with saline mineral, citrus cream, honey and 10+ year potential — Galicia's greatest white.")
if n:
    PAIR(pr5a1, "Live lobster steamed with lemon butter", "complement", "classic", "main", "Rías Baixas aged Albariño and lobster is the definitive Atlantic luxury pairing")
    PAIR(pr5a1, "Centolla gallega (Galician spider crab)", "complement", "classic", "main", "The great Galician crab with the region's most celebrated Albariño; perfect resonance")
    PAIR(pr5a1, "Grilled turbot à la gallega", "complement", "classic", "main", "Turbot is Galicia's greatest fish and aged Señoráns Albariño is its finest companion")
    PAIR(pr5a1, "Sea urchin with butter sauce", "complement", "established", "main", "Saline mineral aged Albariño mirrors sea urchin's oceanic brine beautifully")

pr5a2, n = PROD("Pazo de Señoráns Albariño", "wine_still", p5a, r5, "Spain",
                subcategory="Albariño", price_tier="mid_range",
                description="Benchmark Val do Salnés Albariño; peach blossom, citrus, saline mineral and bright acidity — the textbook expression at its most elegant.")
if n:
    PAIR(pr5a2, "Pulpo a la gallega (octopus with paprika and olive oil)", "complement", "classic", "main", "The most classic of all Galician pairings: Albariño with pulpo a la gallega")
    PAIR(pr5a2, "Grilled sardinas with lemon", "complement", "classic", "main", "Atlantic Albariño and fresh grilled sardines; the taste of Galicia")
    PAIR(pr5a2, "Empanada gallega with tuna", "complement", "classic", "main", "Galician tuna-and-pepper pie meets the region's white wine; a local tradition")
    PAIR(pr5a2, "Salpicón de marisco (Galician shellfish salad)", "complement", "classic", "main", "Citrus-mineral Albariño is the ideal companion for this cold shellfish salad")

p5b = P("Forjas del Salnés", "winery", r5, "Spain",
        production_philosophy="natural",
        philosophy_description="Natural Rías Baixas; Rodrigo Méndez farms old-vine Albariño and Caiño with minimal intervention; Leirana is the benchmark.",
        reputation_narrative="Rodrigo Méndez's Forjas del Salnés produces Galicia's most nuanced natural wines; Leirana ages beautifully and Goliardo Caiño is a world-class rarity.",
        price_positioning="premium")
pr5b1, n = PROD("Forjas del Salnés Leirana Albariño", "wine_still", p5b, r5, "Spain",
                subcategory="Albariño", price_tier="premium",
                description="Natural Albariño from old granite vines; ethereal salinity, white peach and citrus with minimal intervention — one of Galicia's great originals.")
if n:
    PAIR(pr5b1, "Raw oysters with ponzu and shiso", "complement", "established", "starter", "Natural mineral Albariño's saline precision is extraordinary with raw oysters")
    PAIR(pr5b1, "Grilled razor clams with garlic and parsley", "complement", "classic", "main", "Galician navajas and Leirana Albariño; one of Spain's great simple pleasures")
    PAIR(pr5b1, "Grilled sea bass with herb oil and lemon", "complement", "classic", "main", "Natural Albariño mineral frames sea bass with delicate precision")
    PAIR(pr5b1, "Ceviche of sea bass with Galician citrus", "complement", "suggested", "starter", "The Galician citrus-mineral wine and lime-based ceviche mirror each other beautifully")

pr5b2, n = PROD("Forjas del Salnés Goliardo Caiño Tinto", "wine_still", p5b, r5, "Spain",
                subcategory="Caiño Tinto", price_tier="premium",
                description="Rare indigenous Galician red from Caiño Tinto; pale ruby with red cherry, Atlantic mineral and herbal notes — the authentic Rías Baixas red.")
if n:
    PAIR(pr5b2, "Grilled percebes (goose barnacles)", "complement", "classic", "main", "Atlantic mineral Caiño Tinto and goose barnacles; Galicia's most prized seafood")
    PAIR(pr5b2, "Octopus carpaccio with citrus", "complement", "established", "starter", "Pale Atlantic red works beautifully with raw octopus — unusual and compelling")
    PAIR(pr5b2, "Lacón con grelos (cured pork with turnip greens)", "complement", "classic", "main", "The traditional Galician Carnival dish and its most authentic indigenous wine")
    PAIR(pr5b2, "Steamed mussels with Galician wine and herbs", "complement", "classic", "main", "Self-referential classic: Galician red in the mussel broth, then drunk alongside")

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
print("B127 complete.")
