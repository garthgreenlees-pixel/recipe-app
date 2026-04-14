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

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
        (name, country, region_id, producer_type, description))
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

# ── 1. PELJESAC PENINSULA / DINGAC (Croatia) ─────────────────────────────────
print("\n=== Peljesac Peninsula — Dingac (Croatia) ===")
r = R("Peljesac Peninsula", "Croatia", "wine",
      designation_type="PDO",
      designation_name="Dingac PDO / Postup PDO",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Croatia's most celebrated red wine zone, on the steep south-facing slopes of the Peljesac Peninsula in Dalmatia. The Dingac PDO was Croatia's first protected wine designation (1961), producing some of the country's most powerful and concentrated reds from the indigenous Plavac Mali grape — a close genetic relative of Zinfandel/Primitivo. The extreme south-facing cliffs drop directly to the Adriatic, concentrating heat and limiting yields dramatically.",
      key_producers="Matusko Winery, Saints Hills, Grgic Wines, Milos, Bartulovic",
      historical_context="Plavac Mali on the Peljesac Peninsula has been documented since the 15th century. Dingac was Croatia's first designated wine subregion (1961), predating the country's modern DOC system. Mike Grgic (Grgich Hills of Napa Valley fame) returned to his Croatian roots to produce Plavac Mali on Peljesac, bringing international attention to what he considered the ancestral home of Zinfandel.")

VIN(r, 2023, "excellent", "rising", "Exceptional Adriatic heat reflected off limestone cliffs; Plavac Mali of rare concentration and depth")
VIN(r, 2022, "very_good", "rising", "Very good Dalmatian vintage; deep, structured Dingac with excellent aging potential")
VIN(r, 2021, "good", "stable", "Slightly wetter year; lighter style but with the characteristic wild herbs and dark fruit character")
VIN(r, 2020, "excellent", "rising", "Outstanding vintage on Peljesac; greatest Plavac Mali concentration in recent years")
VIN(r, 2019, "very_good", "stable", "Classic Dalmatian vintage with good balance of power and freshness")

p1 = P("Saints Hills", "Croatia", r, "winery",
        "One of Croatia's most ambitious and quality-focused wineries, Saints Hills works with Plavac Mali on the Peljesac Peninsula alongside other Dalmatian varieties. Their Dingac and Nevina wines have won international critical acclaim and represent Croatia's finest expression of its indigenous grape heritage.")
prod1, new1 = PROD("Saints Hills Dingac Plavac Mali Peljesac", "wine_still", p1, r, "Croatia",
    subcategory="Plavac Mali",
    description="Benchmark Dingac from steep south-facing Peljesac cliffs; intense, concentrated Plavac Mali with dark blackberry, dried fig, licorice, and Mediterranean scrub — Croatia's most powerful and age-worthy red wine",
    price_tier="premium")
if new1:
    PAIR(prod1, "Lamb peka (slow-cooked lamb under peka bell with vegetables)", "complement", "classic", "main", "The peninsula's iconic dish and wine: concentrated Plavac Mali with slow-cooked Dalmatian lamb under cast iron is the definitive Croatian table experience")
    PAIR(prod1, "Grilled octopus with Peljesac olive oil and parsley", "complement", "established", "main", "Surprisingly, powerful Dalmatian red pairs well with chargrilled octopus in the local tradition — olive oil bridges the gap")
    PAIR(prod1, "Pasticada (slow-braised beef in prunes and wine sauce)", "complement", "classic", "main", "The Croatian national dish of braised beef with dried fruit and wine sauce resonates deeply with Plavac Mali's dark fruit and structure")
    PAIR(prod1, "Aged Pag cheese with prosciutto and olives", "bridge", "established", "starter", "The wine's dark intensity bridges naturally with the salty aged sheep's cheese of the Croatian islands")

p2 = P("Matusko Winery", "Croatia", r, "winery",
        "The most traditional and venerable producer of Dingac PDO, the Matusko family has been farming Plavac Mali on the Peljesac Peninsula since before Croatian independence. Their Dingac is widely considered the appellation's most authentic and consistent expression, made with minimal intervention to showcase the terroir.")
prod2, new2 = PROD("Matusko Dingac PDO Peljesac", "wine_still", p2, r, "Croatia",
    subcategory="Plavac Mali",
    description="The traditional benchmark Dingac; big, rustic, and genuine with blackberry jam, dried tobacco, wild herbs, and powerful tannic structure that demands cellaring — the authentic voice of Peljesac",
    price_tier="mid_range")
if new2:
    PAIR(prod2, "Roasted red mullet with capers and lemon", "complement", "adventurous", "main", "A local tradition: big, rustic Dalmatian red with rich red mullet — an assertive pairing that works on the peninsula")
    PAIR(prod2, "Black risotto with cuttlefish ink", "complement", "established", "main", "The wine's dark, intense character finds an unusual but compelling match with the briny richness of crni rizot")
    PAIR(prod2, "Grilled lamb chops with garlic and rosemary", "complement", "classic", "main", "Powerful, tannic Plavac Mali is the natural partner for chargrilled Dalmatian lamb in the Croatian cooking tradition")
    PAIR(prod2, "Tuna carpaccio with capers and olive oil", "complement", "suggested", "starter", "The wine's concentrated fruit contrasts interestingly with the delicacy of fresh tuna in a modern Dalmatian starter")

# ── 2. CODRU (Moldova) ───────────────────────────────────────────────────────
print("\n=== Codru (Moldova) ===")
r2 = R("Codru", "Moldova", "wine",
       designation_type="PDO",
       designation_name="PDO Codru",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="Moldova's largest and most established wine PDO, covering the central forest-steppe hills of the country. Codru produces wines from both international varietals (Cabernet Sauvignon, Merlot, Chardonnay) and Eastern European varieties (Feteasca Neagra, Feteasca Alba, Rara Neagra). The region includes the legendary Purcari winery, whose Negru de Purcari was famously served at British royal events and is considered one of Eastern Europe's most historically significant wines.",
       key_producers="Purcari Winery, Cricova Winery, Chateau Vartely, Et Cetera Winery, Castel Mimi",
       historical_context="Moldova was the Soviet Union's primary wine-producing republic, supplying vast quantities to Russia. Post-independence, the industry struggled with two Russian wine embargos (2006 and 2013) that forced Moldovan producers to diversify westward. This pressure accelerated quality improvements, and Moldova now has a burgeoning fine wine culture with wines competing internationally. Purcari's Negru de Purcari was served at the coronations of Queen Elizabeth II and King Charles III.")

VIN(r2, 2023, "very_good", "rising", "Warm continental season; excellent ripeness in international and indigenous varietals")
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage across Moldova; finest Feteasca Neagra and Cabernet Sauvignon in recent memory")
VIN(r2, 2021, "good", "stable", "Good vintage with reliable quality; indigenous varieties particularly well balanced")
VIN(r2, 2020, "very_good", "rising", "Hot, productive season; concentrated reds with good aging potential")
VIN(r2, 2019, "excellent", "rising", "Benchmark Moldovan vintage; complex, age-worthy reds and fresh aromatic whites")

p3 = P("Purcari Winery", "Moldova", r2, "winery",
        "Moldova's most internationally celebrated winery and a producer of genuinely historic significance. Established in 1827 and once supplying the Russian Imperial Court, Purcari's Negru de Purcari and Alb de Purcari are Eastern Europe's most globally recognised fine wines and have been served at British royal coronations.")
prod3, new3 = PROD("Purcari Negru de Purcari Codru PDO", "wine_still", p3, r2, "Moldova",
    subcategory="Cabernet Sauvignon Feteasca Neagra Rara Neagra",
    description="Moldova's most celebrated wine; a regal blend of Cabernet Sauvignon, Feteasca Neagra, and Rara Neagra — dark, complex, and structured with blackberry, dried herbs, tobacco, and a long mineral finish",
    price_tier="premium")
if new3:
    PAIR(prod3, "Slow-braised lamb with Moldovan herbs and polenta", "complement", "classic", "main", "The region's dark, structured blend finds its natural partner in slow-braised lamb with local herbs")
    PAIR(prod3, "Romanian-style sarmale cabbage rolls with smoked pork", "complement", "classic", "main", "Earthy, structured Negru de Purcari and the region's most beloved dish: a natural Eastern European pairing")
    PAIR(prod3, "Grilled sturgeon with dill and lemon butter", "complement", "adventurous", "main", "Moldovan tradition pairs this structured wine with the Danube's prized fish in a bold regional combination")
    PAIR(prod3, "Aged Moldovan branza cheese with walnuts and honey", "bridge", "established", "cheese", "The wine's dark fruit and earthy complexity bridge naturally with pungent aged local cheese and bitter walnut")

p4 = P("Castel Mimi", "Moldova", r2, "winery",
        "One of Moldova's most dynamic modern wineries, Castel Mimi has invested heavily in vineyard management and cellar technology to produce internationally competitive wines at accessible price points. Their Blanc de Blancs and Rosé de Purcari have introduced Moldovan wine to new international audiences.")
prod4, new4 = PROD("Castel Mimi Feteasca Alba Codru PDO", "wine_still", p4, r2, "Moldova",
    subcategory="Feteasca Alba",
    description="Indigenous Moldovan white from the White Maiden grape; elegant, floral, and mineral with lime blossom, white peach, and a clean, crisp acidity — Moldova's most refined white wine variety",
    price_tier="mid_range")
if new4:
    PAIR(prod4, "Ciorba de burta (tripe and sour cream soup)", "complement", "established", "main", "The wine's bright acidity and floral freshness provide welcome counterpoint to the richness of this traditional Moldovan soured soup")
    PAIR(prod4, "Placinte cu branza (fried cheese pastries)", "complement", "classic", "starter", "Moldovan floral white and the country's most beloved fried pastry filled with salty fresh cheese is a natural table combination")
    PAIR(prod4, "Grilled river trout with wild herbs", "complement", "established", "main", "The wine's mineral freshness and floral lift are a natural match for freshwater trout from Moldovan rivers")
    PAIR(prod4, "Zacusca (roasted vegetable spread) on sourdough", "complement", "suggested", "starter", "Crisp, floral Feteasca Alba complements the smoky-sweet roasted pepper and eggplant spread")

# ── 3. MUSCAT OF SAMOS (Greece) ──────────────────────────────────────────────
print("\n=== Muscat of Samos (Greece) ===")
r3 = R("Muscat of Samos", "Greece", "wine",
       designation_type="PDO",
       designation_name="PDO Muscat of Samos",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="The Aegean island of Samos produces one of the world's most ancient and celebrated fortified sweet wines from Muscat Blanc a Petits Grains. The cooperative (Union of Wine Producers of Samos) dominates production and maintains remarkably consistent quality across its range — from the dry Samena to the classic Anthemis (semi-dry) and the sumptuous Nectar Samos (sun-dried berry TBA equivalent). UNESCO has recognised Samos winemaking as Intangible Cultural Heritage.",
       key_producers="Union of Wine Producers of Samos (Samos EOSS), Metaxa (Samos sourcing)",
       historical_context="Wine production on Samos dates to antiquity — Pythagorean manuscripts reference the island's Muscat vines. The wine was beloved by Hippocrates, Erasistratus, and Lord Byron ('fill high the cup with Samian wine'). The Union cooperative was established in 1934 to protect growers from middlemen exploitation and has maintained quality standards that make Samos Muscat a benchmark for Greek sweet wine.")

VIN(r3, 2023, "excellent", "stable", "Ideal Aegean growing conditions; exceptional Muscat aromatic intensity on the island's terraced vineyards")
VIN(r3, 2022, "very_good", "stable", "Good vintage with the classic orange blossom and dried apricot profile at full expression")
VIN(r3, 2021, "good", "stable", "Reliable vintage; consistent cooperative quality across all tiers of the Samos range")
VIN(r3, 2020, "very_good", "stable", "Warm Aegean season; Nectar sun-dried berries of exceptional concentration")
VIN(r3, 2019, "excellent", "stable", "Benchmark vintage for the island; finest Nectar Samos in recent years")

p5 = P("Union of Wine Producers of Samos", "Greece", r3, "winery",
        "The guardian of Samos Muscat, established in 1934 to protect island growers. The cooperative's three-tier range — Samena dry, Anthemis semi-dry, and Nectar (sun-dried) — are the benchmarks of Greek Muscat and among the world's finest fortified wines at every price point.")
prod5, new5 = PROD("Samos Nectar Muscat PDO", "wine_fortified", p5, r3, "Greece",
    subcategory="Muscat Blanc a Petits Grains",
    description="The pinnacle of Samos Muscat; sun-dried berry TBA equivalent — amber-gold with extraordinary concentration of orange marmalade, apricot jam, dried fig, and honey with a clean, bright acid finish that defies its richness",
    price_tier="mid_range")
if new5:
    PAIR(prod5, "Baklava with pistachios and rose water syrup", "complement", "classic", "dessert", "Samos Nectar and the Aegean's most beloved pastry: honeyed, rose-scented layers and the wine's orange blossom sweetness are inseparable")
    PAIR(prod5, "Sheep's milk ice cream with honey and walnuts", "complement", "classic", "dessert", "The wine's orange and apricot concentration creates a stunning match with Greek honey, ice cream, and bitter walnut")
    PAIR(prod5, "Roquefort or aged Gorgonzola", "contrast", "established", "cheese", "The world-class sweet-blue cheese contrast: Samos Nectar's honeyed complexity against pungent, salty blue")
    PAIR(prod5, "Karydopita walnut cake with orange syrup", "complement", "established", "dessert", "The wine's orange marmalade and walnut notes are naturally complementary to the Greek walnut cake drenched in citrus syrup")

p6 = P("Samos Anthemis Cooperative", "Greece", r3, "winery",
        "Part of the same Union of Wine Producers of Samos, the Anthemis label represents the cooperative's most internationally distributed semi-dry Muscat expression — lighter and more aromatic than the Nectar, and ideal as an aperitif or with fresh fruit desserts.")
prod6, new6 = PROD("Samos Anthemis Muscat PDO Semi-Dry", "wine_fortified", p6, r3, "Greece",
    subcategory="Muscat Blanc a Petits Grains",
    description="Semi-dry Samos Muscat; amber with orange blossom, fresh apricot, lychee, and honey — lighter and more aromatic than Nectar, the ideal introduction to Greek Muscat",
    price_tier="entry")
if new6:
    PAIR(prod6, "Fresh melon with prosciutto and mint", "complement", "classic", "starter", "Off-dry Muscat and melon is one of the great warm-weather pairings — the wine's floral sweetness echoes the fruit")
    PAIR(prod6, "Galaktoboureko custard pastry with orange syrup", "complement", "classic", "dessert", "The wine's citrus blossom and honey notes resonate with the Greek custard-filled pastry and its orange syrup")
    PAIR(prod6, "Fresh goat's cheese with thyme honey", "complement", "established", "cheese", "Semi-dry, floral Muscat with fresh tangy cheese and aromatic honey is a perfect Aegean meze")
    PAIR(prod6, "Loukoumades (Greek honey doughnuts with cinnamon)", "complement", "established", "dessert", "The wine's floral sweetness and honey character are naturally complementary to warm, honey-glazed doughnuts")

# ── 4. WÜRTTEMBERG (Germany) ─────────────────────────────────────────────────
print("\n=== Württemberg (Germany) ===")
r4 = R("Württemberg", "Germany", "wine",
       designation_type="Anbaugebiet",
       designation_name="Württemberg QbA/Pradikatswein",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Germany's largest red wine region by volume and one of the country's most culinarily-integrated wine zones, centred on Stuttgart and the Neckar Valley. Württemberg is home to Germany's most consumed red wine grape — Trollinger — as well as Lemberger (Blaufrankisch), Spätburgunder, and Schwarzriesling. The wines are typically lighter, fresher, and more food-friendly than Baden's more powerful Pinots, reflecting the region's deeply embedded tavern (Besenwirtschaft) culture.",
       key_producers="Weingut Aldinger, Weingut Graf Adelmann, Weingut Wachtstetter, Drautz-Able, Staatsweingut Weinsberg",
       historical_context="Württemberg has been producing wine since the Romans, but the region's distinctive character was shaped by Stuttgart's urban tavern culture — the Besenwirtschaft (broom-marked seasonal wine taverns) where local wines were drunk with local food. The region's preference for red wines predates the trend in all other German regions and reflects centuries of Swabian culinary tradition.")

VIN(r4, 2023, "very_good", "rising", "Warm Neckar Valley season; good Lemberger depth and Trollinger freshness")
VIN(r4, 2022, "excellent", "rising", "Outstanding vintage; finest Württemberg Lemberger in recent memory with exceptional structure")
VIN(r4, 2021, "good", "stable", "Cooler year; elegant, lighter style ideal for the region's food culture")
VIN(r4, 2020, "very_good", "stable", "Good hot vintage; concentrated Lemberger and Spatburgunder with good aging potential")
VIN(r4, 2019, "excellent", "rising", "Benchmark vintage; complex, food-friendly reds across all Württemberg varieties")

p7 = P("Weingut Aldinger", "Germany", r4, "winery",
        "One of Württemberg's most respected quality-focused estates, Aldinger crafts benchmark Lemberger and Spatburgunder from the Untertürkheimer Gips Köpfle vineyard in the heart of Stuttgart's wine hills. Their wines have helped elevate Württemberg's international reputation beyond its domestic market focus.")
prod7, new7 = PROD("Weingut Aldinger Lemberger GG Württemberg", "wine_still", p7, r4, "Germany",
    subcategory="Lemberger",
    description="Grosses Gewachs Lemberger (Blaufrankisch) from Stuttgart's best sites; fresh, structured red with dark cherry, pepper, and earthy mineral — Germany's finest expression of this underrated variety",
    price_tier="premium")
if new7:
    PAIR(prod7, "Maultaschen (Swabian stuffed pasta) with brown butter and chives", "complement", "classic", "main", "The regional wine and the regional pasta: Württemberg Lemberger with Swabian Maultaschen is the quintessential Stuttgart table combination")
    PAIR(prod7, "Sauerbraten mit Rosinen-Sosse (sweet-sour braised beef with raisin sauce)", "complement", "classic", "main", "Fresh, structured Lemberger's acidity cuts through the sweet-acid complexity of southern German braised beef")
    PAIR(prod7, "Württemberger Zwiebelrostbraten (pan-fried beef with onion rings)", "complement", "classic", "main", "The most Württemberger of pairings: local beef with caramelised onions and Lemberger from Stuttgart's hills")
    PAIR(prod7, "Aged Allgäuer Bergkäse with sourdough rye", "bridge", "established", "cheese", "The wine's pepper and earth notes bridge naturally with nutty aged Alpine cheese on dark bread")

p8 = P("Weingut Graf Adelmann", "Germany", r4, "winery",
        "One of Württemberg's most prestigious and internationally recognised estates, Graf Adelmann produces wines of exceptional quality from the Burg Schaubeck estate near Kleinbottwar. Their Bruderschaft and Sussmund Cuvees are regarded as the region's finest bottlings, combining Württemberg varieties with Bordeaux grapes in ambitious blends.")
prod8, new8 = PROD("Graf Adelmann Trollinger Württemberg Kabinett", "wine_still", p8, r4, "Germany",
    subcategory="Trollinger",
    description="Classic light-bodied Württemberg Trollinger (Schiava); fresh, bright red cherry, strawberry, and subtle herb notes with refreshing acidity and soft tannins — Germany's most uniquely regional red wine style",
    price_tier="entry")
if new8:
    PAIR(prod8, "Linsensuppe mit Saitenwürstle (lentil soup with Swabian sausage)", "complement", "classic", "main", "The regional classic: Trollinger's light body and fresh acidity are perfect with Stuttgart's beloved lentil and sausage soup")
    PAIR(prod8, "Vesper plate with Laugenbrot and Obatzda cheese spread", "complement", "classic", "starter", "The Württemberg tavern classic: Trollinger as the house wine with Swabian snack plate — beer-garden in spirit")
    PAIR(prod8, "Schwäbischer Zwiebelkuchen (onion tart with bacon and cream)", "complement", "classic", "starter", "Trollinger's fresh acidity is the traditional partner for Swabian onion tart, especially during the grape harvest season")
    PAIR(prod8, "Light charcuterie with Schinkensülze (pork head cheese)", "complement", "established", "starter", "The wine's freshness and light cherry character handles chilled pork preparations with characteristic Swabian simplicity")

# ── 5. COTNARI (Romania) ─────────────────────────────────────────────────────
print("\n=== Cotnari (Romania) ===")
r5 = R("Cotnari", "Romania", "wine",
       designation_type="DOC",
       designation_name="DOC-CMD Cotnari",
       reputation_tier="respected",
       quality_trajectory="rediscovering",
       description="Romania's most historically celebrated wine region, in Moldavia in northeastern Romania. Cotnari has been producing prized white wines since at least the 15th century, including the legendary Grasa de Cotnari — a naturally sweet, botrytised white wine from the Grasa grape that was once the most coveted wine of the Polish royal court and was prized alongside Tokaji. The unique continental-oceanic microclimate promotes reliable Botrytis development, and the indigenous Grasa, Feteasca Alba, Tamaioasa Romaneasca, and Francusa grapes are found almost nowhere else.",
       key_producers="Cotnari SA, Domenii Cotnari, Ceptura, Cramele Recas",
       historical_context="Cotnari's wines were first documented in 1448 under the reign of Stephen the Great of Moldavia, who used them as diplomatic gifts. The wine was praised by Polish King Sobieski in the 17th century and was imported to the courts of Warsaw, Vienna, and Versailles. Cotnari's reputation was destroyed during the communist era's focus on quantity, but modern producers are beginning the slow process of rebuilding the region's historic prestige.")

VIN(r5, 2023, "good", "rising", "Good Moldavian continental season; reliable Botrytis in Grasa; improving Cotnari quality")
VIN(r5, 2022, "very_good", "rising", "Excellent Botrytis development; finest Grasa de Cotnari in recent years; age-worthy quality")
VIN(r5, 2021, "average", "stable", "Variable year; dry conditions limited Botrytis but clean, fragrant dry styles emerged")
VIN(r5, 2020, "good", "stable", "Good vintage; Grasa and Tamaioasa Romaneasca with typical floral sweetness")
VIN(r5, 2019, "very_good", "rising", "Outstanding vintage for Romanian whites; Grasa de Cotnari of exceptional honeyed complexity")

p9 = P("Cotnari SA", "Romania", r5, "winery",
        "The main commercial producer of Cotnari, responsible for maintaining production continuity through the communist era and the difficult post-communist decades. Their Grasa de Cotnari and Grasa Botrytizata represent the accessible face of Romania's most historically significant wine region.")
prod9, new9 = PROD("Cotnari Grasa de Cotnari Botrytizata DOC", "wine_dessert", p9, r5, "Romania",
    subcategory="Grasa",
    description="Romania's most historic sweet wine; naturally botrytised Grasa from Moldavian hills — golden, honeyed, and aromatic with dried apricot, orange peel, beeswax, and a bright acid backbone that promises long aging",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "Romanian cozonac (sweet bread with walnuts and cocoa)", "complement", "classic", "dessert", "The traditional pairing: Cotnari's honeyed, orange-scented sweetness with the walnut-cocoa festive bread of Moldova and Wallachia")
    PAIR(prod9, "Pate de foie gras with fig jam and brioche", "complement", "established", "starter", "Historic sweet wine and foie gras — a pairing as old as Romania's trade with Western Europe; the wine's acidity cuts through the richness elegantly")
    PAIR(prod9, "Salted Pecorino Sardo or Roquefort blue cheese", "contrast", "established", "cheese", "Botrytised Grasa's sweet-acid complexity provides stunning contrast to intensely salty, pungent blue cheese")
    PAIR(prod9, "Clatite cu branza si stafide (crepes with cheese and raisins)", "complement", "classic", "dessert", "The wine's raisin and honey notes mirror the sweet cheese crepes of the Romanian table in a deeply regional pairing")

p10 = P("Domenii Cotnari", "Romania", r5, "winery",
         "A modern estate reviving quality production in the Cotnari DOC with indigenous varieties, particularly Tamaioasa Romaneasca (Romanian Frankincense) — one of Romania's most distinctive and aromatic white grapes producing lightly sweet, floral wines with a characteristic incense-rose character.")
prod10, new10 = PROD("Domenii Cotnari Tamaioasa Romaneasca DOC", "wine_still", p10, r5, "Romania",
    subcategory="Tamaioasa Romaneasca",
    description="Romania's most aromatic indigenous white; semi-sweet with intense rose petal, incense, dried apricot, and floral spice — a completely unique varietal character found almost nowhere outside Moldova and Wallachia",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Baklava with rose water and pistachios", "complement", "classic", "dessert", "The wine's intense rose and incense character creates perfect harmony with the floral-sweet layers of baklava")
    PAIR(prod10, "Spiced pumpkin pie with cinnamon and cloves", "complement", "established", "dessert", "Aromatic, off-dry Tamaioasa resonates with the warm spice and sweetness of a Romanian pumpkin pastry")
    PAIR(prod10, "Fresh cherry and almond tart", "complement", "suggested", "dessert", "The wine's floral intensity and sweet fruit complement cherry and almond in a delicate fruit tart")
    PAIR(prod10, "Fresh Kashkaval cheese with rose-hip jam", "bridge", "suggested", "cheese", "The wine's rose and incense character bridges with the mild young cheese and sweet-tart rose jam in a uniquely Romanian combination")

# ── COUNTS ───────────────────────────────────────────────────────────────────
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
conn.close()
