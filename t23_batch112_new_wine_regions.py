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

# ── REGION 1: Cerveteri ──────────────────────────────────────────────────────
print("=== Region 1: Cerveteri ===")
r1 = R("Cerveteri", "Italy", "wine",
        designation_type="DOC", designation_name="Cerveteri DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Lazio coastal DOC north of Rome producing Sangiovese-Montepulciano reds and Trebbiano-Malvasia whites from volcanic Etruscan hillsides; historically Rome's everyday table wine.",
        key_producers="Cantina di Cerveteri, Terre Etrusche",
        historical_context="Cerveteri was the wine of the Etruscan port city Caere and later ancient Rome's daily consumption; the cooperative still produces accessible wines from this storied hillside terroir.")
VIN(r1, 2022, "good", "stable", "Coastal warmth; whites fresh and aromatic; reds approachable and fruity.")
VIN(r1, 2021, "good", "stable", "Balanced season; consistent everyday expressions.")
VIN(r1, 2020, "very_good", "stable", "Excellent vintage for the appellation; best whites in recent memory.")
VIN(r1, 2019, "good", "stable", "Standard quality vintage; food-friendly and accessible.")
VIN(r1, 2018, "good", "stable", "Reliable vintage; consistent honest wines.")
p1a = P("Cantina di Cerveteri", "winery", r1, "Italy",
        production_philosophy="traditional",
        philosophy_description="Historic Etruscan coast cooperative producing the full range of Cerveteri DOC wines; reliable quality and excellent value.",
        reputation_narrative="Volume benchmark for the DOC; found widely in Rome's trattorias and local markets.",
        price_positioning="value",
        authority_tier=1)
p1b = P("Terre Etrusche", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Quality-focused Cerveteri producer working volcanic hillside soils to extract more character from the appellation's indigenous varieties.",
        reputation_narrative="Leading quality voice for the DOC; earns attention from Lazio wine specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Cantina di Cerveteri Cerveteri Bianco", "wine_still", p1a, r1, "Italy",
                  subcategory="Trebbiano Toscano blend",
                  description="Light, fresh Cerveteri white from Trebbiano and Malvasia; citrus, white flowers and a neutral mineral finish; everyday Roman table white.",
                  price_tier="value")
if n1a:
    PAIR(pr1a, "Carciofi alla romana (Roman artichokes)", "complement", "classic", "starter", "Roman vegetable classic with local white wine; artichoke bitterness balanced by Trebbiano freshness.")
    PAIR(pr1a, "Pasta cacio e pepe", "complement", "classic", "main", "Rome's canonical pasta dish; neutral white wine complements without competing.")
    PAIR(pr1a, "Supplì al telefono (fried rice balls)", "complement", "classic", "casual", "Roman street food classic; light white wine cleanses between crispy bites.")
    PAIR(pr1a, "Grilled branzino with capers", "complement", "established", "fish_course", "Coastal Roman fish with coastal Roman white; simple and delicious.")
pr1b, n1b = PROD("Terre Etrusche Cerveteri Rosso", "wine_still", p1b, r1, "Italy",
                  subcategory="Sangiovese-Montepulciano",
                  description="Volcanic Etruscan hillside red with dark cherry, dried herbs and earthy mineral; medium-bodied and food-friendly.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Saltimbocca alla Romana", "complement", "classic", "main", "Rome's veal and sage classic with a local red; the dish demands a medium-bodied Italian wine.")
    PAIR(pr1b, "Porchetta di Ariccia", "complement", "classic", "casual", "Roman pork roast tradition; Cerveteri red and porchetta at the roadside stall.")
    PAIR(pr1b, "Rigatoni alla pajata (veal intestine)", "complement", "classic", "main", "Rome's most traditional offal pasta with local Roman red; regional authenticity.")
    PAIR(pr1b, "Lamb scottadito with herbs", "complement", "established", "main", "Grilled lamb chops from the Lazio hills; Cerveteri's dark fruit and structure match.")

# ── REGION 2: Frascati ───────────────────────────────────────────────────────
print("=== Region 2: Frascati ===")
r2 = R("Frascati", "Italy", "wine",
        designation_type="DOC", designation_name="Frascati DOC",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description="Castelli Romani volcanic hillside DOC southeast of Rome; Malvasia and Trebbiano white wines from ancient volcanic soils; quality revolution underway after decades of bulk wine reputation.",
        key_producers="Castel de Paolis, Villa Simone",
        historical_context="Frascati was Rome's most beloved summer wine since Renaissance popes retreated to the Castelli Romani hills; corrupted by industrial bulk production in the 20th century; artisan producers now restoring its dignity.")
VIN(r2, 2022, "very_good", "stable", "Volcanic soil freshness preserved even in warm year; aromatic and mineral.")
VIN(r2, 2021, "good", "stable", "Cool season; lean and fresh with classic Malvasia florality.")
VIN(r2, 2020, "very_good", "stable", "Excellent quality vintage; artisan producers deliver wines to be proud of.")
VIN(r2, 2019, "very_good", "stable", "Warm with good ripeness; best Frascati in recent years from top producers.")
VIN(r2, 2018, "good", "stable", "Standard vintage; good everyday drinking from reliable estates.")
p2a = P("Castel de Paolis", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Pioneer of the Frascati quality revolution; Giulio Santarelli produces single-vineyard wines that redefined the appellation's potential.",
        reputation_narrative="Universally acknowledged as Frascati's finest producer; Vigna Adriana is a benchmark Italian white.",
        price_positioning="premium",
        authority_tier=2)
p2b = P("Villa Simone", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Frascati estate producing Malvasia-based wines of genuine quality and character from volcanic Castelli Romani hillsides.",
        reputation_narrative="Alongside Castel de Paolis, Villa Simone leads Frascati's quality revival; consistently praised by Italian wine press.",
        price_positioning="mid_range",
        authority_tier=2)
pr2a, n2a = PROD("Castel de Paolis Frascati Superiore Vigna Adriana", "wine_still", p2a, r2, "Italy",
                  subcategory="Malvasia blend",
                  description="Single-vineyard Frascati of outstanding complexity; flowers, stone fruit, volcanic mineral and a long hazelnut finish — the wine that proves Frascati can be great.",
                  price_tier="premium")
if n2a:
    PAIR(pr2a, "Porchetta di Ariccia with herbs", "complement", "classic", "casual", "Rome's most famous pork and the Castelli Romani's most famous wine; regional inseparability.")
    PAIR(pr2a, "Carciofi alla giudia (Jewish-style fried artichoke)", "complement", "classic", "starter", "Rome's Jewish ghetto classic and volcanic Frascati; artichoke bitterness met by Malvasia's florality.")
    PAIR(pr2a, "Fritto di fiori di zucca (fried zucchini flowers)", "complement", "classic", "starter", "Delicate Roman antipasto and volcanic white; floral fragility matched.")
    PAIR(pr2a, "Spaghetti alle vongole veraci", "complement", "classic", "main", "Roman clam pasta and local volcanic white; a lunch in the Castelli Romani hills.")
pr2b, n2b = PROD("Villa Simone Frascati Superiore Vigneto Filonardi", "wine_still", p2b, r2, "Italy",
                  subcategory="Malvasia Puntinata",
                  description="Estate Frascati with rare Malvasia Puntinata; apricot, citrus blossom and distinctive volcanic stone mineral; medium body and good persistence.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Grilled spigola (sea bass) with capers", "complement", "established", "fish_course", "Coastal Roman fish with Castelli hillside white; mineral link across the short distance.")
    PAIR(pr2b, "Insalata di puntarelle (chicory salad)", "complement", "classic", "starter", "Bitter Roman winter salad with local white; bitterness and florality in Roman dialogue.")
    PAIR(pr2b, "Light pasta with butter and white truffle", "complement", "established", "main", "Volcano and truffle — both expressions of Italian terroir; elegant and precise match.")
    PAIR(pr2b, "Abbacchio scottadito (Roman lamb chops)", "complement", "established", "main", "Young Roman lamb and local white — unusual but works at Sunday lunch in the Castelli.")

# ── REGION 3: Est! Est!! Est!!! di Montefiascone ────────────────────────────
print("=== Region 3: Est Est Est di Montefiascone ===")
r3 = R("Est Est Est di Montefiascone", "Italy", "wine",
        designation_type="DOC", designation_name="Est! Est!! Est!!! di Montefiascone DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Lazio volcanic lake DOC on Lake Bolsena's rim producing Trebbiano and Malvasia whites from ancient volcanic tufa soils; more famous for its legendary name than its wine quality.",
        key_producers="Falesco, Rosi Montefiascone",
        historical_context="Named from a medieval legend where a bishop's servant scrawled 'Est!' (good wine is here) repeatedly; the tale is better than most 20th-century wines were; quality revival now underway from ambitious producers.")
VIN(r3, 2022, "very_good", "stable", "Volcanic lake microclimate preserved freshness; best whites in recent memory.")
VIN(r3, 2021, "good", "stable", "Cooler season; lean and aromatic with lake-breeze freshness.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; volcanic tufa mineral well expressed.")
VIN(r3, 2019, "good", "stable", "Standard quality vintage; pleasant everyday drinking.")
VIN(r3, 2018, "good", "stable", "Reliable vintage; consistent quality from better producers.")
p3a = P("Falesco", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Lazio's most celebrated winery, founded by sommelier Riccardo Cotarella; produces both international-style super-Lazio wines and quality Est!Est!!Est!!!.",
        reputation_narrative="Falesco is Lazio's most important quality producer; their Montiano Merlot is Italy's most awarded Merlot.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Rosi Montefiascone", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Small estate committed to producing quality Est!Est!!Est!!! from volcanic tufa vineyards above Lake Bolsena.",
        reputation_narrative="Leading quality voice for the appellation's revived ambition.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Falesco Est Est Est di Montefiascone", "wine_still", p3a, r3, "Italy",
                  subcategory="Trebbiano-Malvasia",
                  description="Clean, fruit-forward volcanic white with citrus, melon and volcanic mineral; fresh and food-friendly with persistent finish.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Acquacotta dell'Alto Lazio (peasant vegetable soup)", "complement", "classic", "casual", "Ancient Lazio peasant soup with the lake district's local white wine; regional continuity.")
    PAIR(pr3a, "Grilled lake whitefish (coregone)", "complement", "classic", "fish_course", "Lake Bolsena fish and Lake Bolsena wine; freshwater fish matches the wine's mineral freshness.")
    PAIR(pr3a, "Bruschetta with summer tomatoes", "complement", "classic", "casual", "Simple Lazio antipasto with a crisp local white; honest summer lunch.")
    PAIR(pr3a, "Fresh ricotta with herbs and olive oil", "complement", "established", "starter", "Soft Lazio dairy and volcanic white; mineral freshness lifts the cream.")
pr3b, n3b = PROD("Rosi Montefiascone Est Est Est Bianco Vulcanico", "wine_still", p3b, r3, "Italy",
                  subcategory="Trebbiano Giallo",
                  description="Small-production volcanic Est!Est!!Est!!! from Trebbiano Giallo; distinctive tufa mineral, citrus and white flower with unusual texture for the appellation.",
                  price_tier="value")
if n3b:
    PAIR(pr3b, "Anguilla arrosto (roasted lake eel)", "complement", "classic", "main", "Lake Bolsena eel with the lake's wine; rich eel fat balanced by volcanic minerality.")
    PAIR(pr3b, "Pasta with lake shrimp and tomato", "complement", "established", "main", "Freshwater shrimp and local DOC white; lake-to-table regional Italian cooking.")
    PAIR(pr3b, "Fiori di zucca in tempura", "complement", "established", "starter", "Delicate fried zucchini flowers with a light volcanic white; Lazio summer tradition.")
    PAIR(pr3b, "Insalata caprese con burrata", "complement", "established", "starter", "Tomato and burrata demand a crisp Italian white with enough freshness; volcanic mineral ideal.")

# ── REGION 4: Cesanese del Piglio ─────────────────────────────────────────
print("=== Region 4: Cesanese del Piglio ===")
r4 = R("Cesanese del Piglio", "Italy", "wine",
        designation_type="DOCG", designation_name="Cesanese del Piglio DOCG",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Small Lazio DOCG in the Ciociaria hills south of Rome; produces the native Cesanese grape — a compelling medium-bodied red with wild cherry, spice and mineral — Italy's most overlooked DOCG.",
        key_producers="Damiano Ciolli, Coletti Conti",
        historical_context="Cesanese is Lazio's great native red variety, celebrated by Popes in the Renaissance but nearly forgotten in the 20th century; a small band of dedicated producers is reviving its extraordinary potential.")
VIN(r4, 2022, "very_good", "stable", "Warm Lazio hills; Cesanese shows excellent dark cherry and spice.")
VIN(r4, 2021, "good", "stable", "Cooler year; elegant and aromatic Cesanese with good freshness.")
VIN(r4, 2020, "excellent", "rising", "Outstanding vintage; Cesanese shows unprecedented concentration and complexity.")
VIN(r4, 2019, "very_good", "stable", "Classic expression; wild cherry, pepper and mineral in fine balance.")
VIN(r4, 2018, "good", "stable", "Reliable vintage; approachable Cesanese for early drinking.")
p4a = P("Damiano Ciolli", "winery", r4, "Italy",
        production_philosophy="minimal_intervention",
        philosophy_description="The most passionate and quality-focused Cesanese del Piglio producer; single-vineyard Silene is the wine that convinced Italy Cesanese was a great variety.",
        reputation_narrative="Internationally recognised as Cesanese's champion; Ciolli's wines appear in the world's best natural wine lists.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Coletti Conti", "winery", r4, "Italy",
        production_philosophy="traditional",
        philosophy_description="Historic Piglio estate producing traditional Cesanese with emphasis on long ageing and the variety's natural spice and mineral character.",
        reputation_narrative="One of the oldest Cesanese names; wines show the variety's ageing potential and complexity.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Damiano Ciolli Silene Cesanese del Piglio", "wine_still", p4a, r4, "Italy",
                  subcategory="Cesanese di Affile",
                  description="Single-vineyard benchmark Cesanese; wild cherry, dried violet, black pepper, clay mineral and a haunting smoky finish; the wine that defines the DOCG's potential.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Lamb alla cacciatora with peppers", "complement", "classic", "main", "Lazio hunter's lamb stew; Cesanese's spice and cherry are the natural regional match.")
    PAIR(pr4a, "Porchetta di Ariccia con sale e rosmarino", "complement", "classic", "casual", "Roman pork tradition with Lazio's most characterful red; regional unity.")
    PAIR(pr4a, "Pasta al ragù di cinghiale (wild boar)", "complement", "established", "main", "Wild boar ragù and Cesanese's spice and cherry; Lazio inland tradition.")
    PAIR(pr4a, "Pecorino Romano with honey and walnuts", "complement", "classic", "cheese", "Sharp Lazio sheep's cheese and the region's great red; walnut bitterness bridges the spice.")
pr4b, n4b = PROD("Coletti Conti Hernicus Cesanese del Piglio", "wine_still", p4b, r4, "Italy",
                  subcategory="Cesanese",
                  description="Traditional Cesanese del Piglio with cherry, leather, dried spice and mineral; medium body with good structure and honest character.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Abbacchio alla romana (Roman spring lamb)", "complement", "classic", "main", "Rome's Easter lamb dish with local Cesanese; the DOCG's signature pairing.")
    PAIR(pr4b, "Grilled sausages with bitter greens", "complement", "established", "casual", "Country Lazio cooking; Cesanese's tannin tames the sausage fat.")
    PAIR(pr4b, "Pasta e fagioli with rosemary", "complement", "classic", "casual", "Lazio peasant classic; medium Cesanese and bean soup — rustic winter unity.")
    PAIR(pr4b, "Braised oxtail alla vaccinara", "complement", "classic", "main", "Rome's iconic quinto quarto dish with Lazio's best red; the definitive city and country union.")

# ── REGION 5: Orvieto ────────────────────────────────────────────────────────
print("=== Region 5: Orvieto ===")
r5 = R("Orvieto", "Italy", "wine",
        designation_type="DOC", designation_name="Orvieto DOC",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description="Ancient Umbrian-Lazio DOC around the dramatic clifftop city of Orvieto; Trebbiano and Grechetto whites from tufa volcanic soils; quality revolution underway led by producers abandoning bulk production.",
        key_producers="Barberani, Palazzone",
        historical_context="Orvieto was Papal wine in the Renaissance; the Popes of Avignon drank it; the 20th century reduced it to bland commercial white; artisan producers now restoring quality through Grechetto and native varieties.")
VIN(r5, 2022, "very_good", "stable", "Volcanic tufa soils retained freshness in warm season; excellent mineral quality.")
VIN(r5, 2021, "good", "stable", "Cooler Umbrian year; Grechetto shows characteristic bitter almond and citrus.")
VIN(r5, 2020, "very_good", "stable", "Balanced vintage; Grechetto-Trebbiano blends show real character and length.")
VIN(r5, 2019, "very_good", "stable", "Warm and expressive; best Orvieto whites in a generation from top producers.")
VIN(r5, 2018, "good", "stable", "Good vintage; consistent and food-friendly expressions.")
p5a = P("Barberani", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-generational Orvieto estate producing the full range from dry to Muffa Nobile botrytis; benchmark for the DOC's quality revival.",
        reputation_narrative="Universally acknowledged as Orvieto's leading producer; Calcaia botrytised Orvieto is one of Italy's great dessert wines.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Palazzone", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Quality-focused Orvieto estate run by Giovanni Dubini; single-vineyard Terre Vineate shows what Grechetto can achieve on tufa soils.",
        reputation_narrative="Alongside Barberani, Palazzone leads the Orvieto quality renaissance; consistent critical praise.",
        price_positioning="mid_range",
        authority_tier=2)
pr5a, n5a = PROD("Barberani Orvieto Classico Superiore Castagnolo", "wine_still", p5a, r5, "Italy",
                  subcategory="Grechetto-Trebbiano",
                  description="Single-vineyard Orvieto from old tufa vines; bitter almond, pear, citrus and volcanic mineral with remarkable structure for the appellation.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Umbricelli pasta with black truffle (tartufo nero)", "complement", "classic", "main", "Umbrian truffle pasta with local white; tufa volcanic mineral and truffle earth in dialogue.")
    PAIR(pr5a, "Grilled lake perch with herbs", "complement", "established", "fish_course", "Lake Corbara (nearby) freshwater perch with Orvieto; lake microclimate link.")
    PAIR(pr5a, "White bean bruschetta with sage", "complement", "classic", "casual", "Umbrian pulse tradition with local white wine; simple and regionally authentic.")
    PAIR(pr5a, "Pecorino di Norcia with chestnut honey", "complement", "classic", "cheese", "Umbrian sheep cheese and Orvieto white; Grechetto's bitter almond meets aged pecorino.")
pr5b, n5b = PROD("Palazzone Orvieto Classico Superiore Terre Vineate", "wine_still", p5b, r5, "Italy",
                  subcategory="Grechetto-Procanico",
                  description="Flagship Orvieto with Grechetto and ancient Procanico (local Trebbiano); white flowers, stone fruit, tufa mineral and impressive length for the DOC.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Sformato di ricotta con tartufo", "complement", "established", "starter", "Ricotta soufflé with Umbrian truffle and Orvieto white; volcanic mineral and earthy truffle.")
    PAIR(pr5b, "Tortelli di Norcia con fonduta", "complement", "established", "main", "Truffle-stuffed pasta with cheese fondue; structured Grechetto handles both the richness and the earth.")
    PAIR(pr5b, "Colombaccio arrosto (roast woodpigeon)", "complement", "established", "main", "Umbrian game tradition; Orvieto's Grechetto bitter almond works with the slight gaminess.")
    PAIR(pr5b, "Fried stuffed olives all'ascolana", "complement", "classic", "starter", "Marchigian-Umbrian classic antipasto; the wine's freshness and bitter almond clean the frying oil.")

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
