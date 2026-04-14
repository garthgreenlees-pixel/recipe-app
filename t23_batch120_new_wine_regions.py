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

# ── B120 ─────────────────────────────────────────────────────────────────────
# Targets: Etna DOC, Cerasuolo di Vittoria DOCG, Marsala DOC (Sicily),
#          Santorini PDO, Nemea PDO (Greece)

# 1. ETNA DOC — Sicily, Italy
print("=== Etna DOC ===")
r1 = R("Etna DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Etna DOC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Volcanic appellation on the slopes of Mount Etna producing Nerello Mascalese reds and Carricante whites of extraordinary mineral intensity. Ancient massal-selection vines, often pre-phylloxera, grown in lava-rich soils at 400–1000m elevation. Etna's contrade (single-vineyard sites) rival Burgundy in site specificity.",
        key_producers="Benanti, Cornelissen, Passopisciaro, Terre Nere, Terre di Trente",
        historical_context="Etna wines date to ancient Greek colonisation but declined post-phylloxera. The modern renaissance began in the 1990s when Marco de Grazia and others recognised the terroir's exceptional potential. Now one of Italy's most exciting appellations.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"exceptional","rising"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r1, yr, qd, pt, f"Etna {yr}: volcanic harvest on steep lava terraces")

p1a = P("Benanti", "winery", r1, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Pioneer of the Etna renaissance; single-contrada bottlings showcase lava-soil minerality.",
        reputation_narrative="Giuseppe Benanti launched the modern Etna movement in 1988; benchmark Nerello Mascalese.",
        price_positioning="premium")
pr1a1, n = PROD("Benanti Etna Rosso Serra della Contessa", "wine_still", p1a, r1, "Italy",
                subcategory="Nerello Mascalese", price_tier="premium",
                description="Single-vineyard Nerello Mascalese from Serra della Contessa; silky tannins with volcanic smoke and red cherry.")
if n:
    PAIR(pr1a1, "Wood-roasted lamb with herbs", "complement", "classic", "main", "Volcanic mineral tannins frame herb-crusted lamb perfectly")
    PAIR(pr1a1, "Grilled swordfish with capers", "bridge", "established", "main", "Nerello's light body and acidity bridge land and sea ingredients")
    PAIR(pr1a1, "Aged pecorino siciliano", "complement", "classic", "cheese", "Tart pecorino echoes the wine's volcanic citrus edge")
    PAIR(pr1a1, "Braised rabbit with olives", "complement", "established", "main", "Silky tannins and bright acidity lift this classic Sicilian braise")

pr1a2, n = PROD("Benanti Etna Bianco Superiore Pietra Marina", "wine_still", p1a, r1, "Italy",
                subcategory="Carricante", price_tier="premium",
                description="Carricante from Milo on Etna's eastern flank; saline, mineral and age-worthy white of exceptional tension.")
if n:
    PAIR(pr1a2, "Raw sea urchin on brioche", "complement", "classic", "starter", "Carricante's saline minerality mirrors urchin's oceanic brine")
    PAIR(pr1a2, "Grilled langoustines with lemon", "complement", "classic", "main", "Laser-sharp acidity and citrus lift delicate crustacean sweetness")
    PAIR(pr1a2, "Spaghetti alle vongole", "complement", "established", "main", "Volcanic mineral whites are the classic pairing for clam pasta")
    PAIR(pr1a2, "Fried calamari with aioli", "cleanse", "established", "starter", "High acidity cleanses the palate between each crisp bite")

p1b = P("Terre Nere", "winery", r1, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Marco de Grazia's estate; contrada-specific bottlings from pre-phylloxera vines on black lava soils.",
        reputation_narrative="Reference producer for Etna reds; multiple contrada wines (Calderara, Feudo di Mezzo, Santo Spirito) define site differences.",
        price_positioning="premium")
pr1b1, n = PROD("Terre Nere Etna Rosso Calderara Sottana", "wine_still", p1b, r1, "Italy",
                subcategory="Nerello Mascalese", price_tier="premium",
                description="From the Calderara Sottana contrada on Etna's north slope; perfumed and precise with lava-stone minerality.")
if n:
    PAIR(pr1b1, "Roasted duck breast with cherry reduction", "complement", "classic", "main", "Perfumed Nerello lifts the richness of duck with bright red fruit")
    PAIR(pr1b1, "Wild mushroom risotto", "complement", "established", "main", "Earthy volcanic mineral notes mirror forest floor mushroom depth")
    PAIR(pr1b1, "Tuna tartare with citrus", "bridge", "suggested", "starter", "Light tannins bridge raw tuna without overwhelming delicate texture")
    PAIR(pr1b1, "Charcuterie with Sicilian olives", "complement", "established", "starter", "Savory charcuterie finds natural foil in volcanic-accented Nerello")

pr1b2, n = PROD("Terre Nere Etna Bianco", "wine_still", p1b, r1, "Italy",
                subcategory="Carricante", price_tier="mid_range",
                description="Entry-level Etna Bianco; Carricante-led blend with vivid citrus and almond, mineral and refreshing.")
if n:
    PAIR(pr1b2, "Baked whole fish with fennel", "complement", "classic", "main", "Classic Sicilian combination of white wine and Mediterranean fish")
    PAIR(pr1b2, "Insalata di mare", "complement", "established", "starter", "Citrus-driven Carricante mirrors the lemon dressing of seafood salad")
    PAIR(pr1b2, "Arancini with ragù", "complement", "suggested", "starter", "Almond notes and acidity cut through fried arancini richness")
    PAIR(pr1b2, "Caprese with buffalo mozzarella", "complement", "established", "starter", "Bright acidity and mineral finish refresh between creamy bites")

# 2. CERASUOLO DI VITTORIA DOCG — Sicily, Italy
print("=== Cerasuolo di Vittoria DOCG ===")
r2 = R("Cerasuolo di Vittoria DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Cerasuolo di Vittoria DOCG",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Sicily's only DOCG, from the south-east corner of the island. A mandatory blend of Nero d'Avola (50–70%) with Frappato (30–50%), yielding vibrant cherry-fruited reds with silky texture. Classico zone within Vittoria offers superior concentration from clay-limestone soils.",
        key_producers="COS, Valle dell'Acate, Planeta, Occhipinti",
        historical_context="Named for the cerise (cherry) colour of the traditional blend. The DOCG was established in 2005, recognising the unique blend formula that distinguishes these wines from heavier Sicilian reds.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r2, yr, qd, pt, f"Cerasuolo di Vittoria {yr}: warm season moderated by sea breeze")

p2a = P("COS", "winery", r2, "Italy",
        production_philosophy="biodynamic",
        philosophy_description="Founding Cerasuolo estate; amphora fermentation and biodynamic viticulture; minimal intervention winemaking.",
        reputation_narrative="COS founded 1980 by Giambattista Cilia and Cirino Strano; pioneers of natural Sicilian winemaking and amphora vinification.",
        price_positioning="premium")
pr2a1, n = PROD("COS Cerasuolo di Vittoria Classico", "wine_still", p2a, r2, "Italy",
                subcategory="Nero d'Avola-Frappato", price_tier="premium",
                description="Amphora-fermented Cerasuolo Classico; vibrant cherry, earthy spice and gentle tannins with exceptional freshness.")
if n:
    PAIR(pr2a1, "Pasta alla Norma with fried aubergine", "complement", "classic", "main", "Frappato's bright cherry and Nero d'Avola's depth match Sicilian pasta perfectly")
    PAIR(pr2a1, "Grilled pork sausages with fennel seeds", "complement", "established", "main", "Cherry-fruited blend brightens the anise-spice profile of fennel sausage")
    PAIR(pr2a1, "Caponata on bruschetta", "complement", "classic", "starter", "Sweet-sour caponata echoes the wine's bright acidity and fruit")
    PAIR(pr2a1, "Braised rabbit with capers", "complement", "classic", "main", "Traditional Sicilian braised rabbit finds its natural companion in Cerasuolo")

pr2a2, n = PROD("COS Frappato", "wine_still", p2a, r2, "Italy",
                subcategory="Frappato", price_tier="premium",
                description="Pure varietal Frappato; pale ruby, fragrant rose-petal and wild strawberry, featherweight and compelling.")
if n:
    PAIR(pr2a2, "Vitello tonnato", "complement", "established", "starter", "Light Frappato complements the delicate veal without overwhelming tuna sauce")
    PAIR(pr2a2, "Burrata with heirloom tomatoes", "complement", "classic", "starter", "Fragrant rose-petal notes mirror ripe summer tomato sweetness")
    PAIR(pr2a2, "Chilled antipasto spread", "complement", "established", "starter", "Light-bodied Frappato works across the variety of an antipasto table")
    PAIR(pr2a2, "Wild strawberry tart", "complement", "suggested", "dessert", "The wine's strawberry fragrance echoes the tart filling")

p2b = P("Valle dell'Acate", "winery", r2, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Family estate in Vittoria; benchmark Cerasuolo with multi-generational commitment to local varietals.",
        reputation_narrative="Giacomo Jacono's estate produces consistently outstanding Cerasuolo; one of the DOCG's most reliable references.",
        price_positioning="mid_range")
pr2b1, n = PROD("Valle dell'Acate Cerasuolo di Vittoria", "wine_still", p2b, r2, "Italy",
                subcategory="Nero d'Avola-Frappato", price_tier="mid_range",
                description="Classic Cerasuolo blend; polished cherry and pomegranate with silky tannins and Mediterranean herb finish.")
if n:
    PAIR(pr2b1, "Pizza with tomato and anchovies", "complement", "classic", "main", "Bright fruit and acidity cut through umami-rich anchovy pizza")
    PAIR(pr2b1, "Grilled tuna steak with olives", "complement", "established", "main", "Cerasuolo's cherry fruit complements tuna's meaty texture beautifully")
    PAIR(pr2b1, "Mozzarella in carrozza", "complement", "suggested", "starter", "Light tannins and acidity freshen this classic fried cheese")
    PAIR(pr2b1, "Lamb cutlets with rosemary", "complement", "established", "main", "Classic Mediterranean herb-and-lamb pairing with the Sicilian blend")

pr2b2, n = PROD("Valle dell'Acate Il Frappato", "wine_still", p2b, r2, "Italy",
                subcategory="Frappato", price_tier="mid_range",
                description="Single-varietal Frappato; pale ruby with strawberry, violets and a cooling mineral freshness.")
if n:
    PAIR(pr2b2, "Prosciutto with melon", "complement", "classic", "starter", "Fragrant Frappato echoes melon sweetness and cuts prosciutto's salt")
    PAIR(pr2b2, "Insalata caprese", "complement", "established", "starter", "Violet and strawberry fragrance mirrors the freshness of ripe tomato-basil")
    PAIR(pr2b2, "Chicken scallopini with lemon", "complement", "established", "main", "Light-bodied Frappato lifts lemony chicken without overpowering")
    PAIR(pr2b2, "Semifreddo al pistacchio", "bridge", "suggested", "dessert", "Pale fruit and mineral freshness bridge the nutty creaminess of the dessert")

# 3. MARSALA DOC — Sicily, Italy
print("=== Marsala DOC ===")
r3 = R("Marsala DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Marsala DOC",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description="Historic Sicilian fortified wine from the western tip of Sicily around the city of Marsala. Made from Grillo, Catarratto, and Inzolia grapes via a solera-like perpetuum system with cooked grape must (mosto cotto). Styles range from Fine (dry) to Vergine (bone dry, aged 5+ years) and Superiore. Used in classic Italian cookery but serious dry Vergine styles rival fine sherry.",
        key_producers="Florio, Marco De Bartoli, Pellegrino, Rallo",
        historical_context="Created in 1796 by English merchant John Woodhouse who discovered the wine could survive long sea voyages when fortified with grape spirit. Supplied to Nelson's fleet. De Bartoli revived the category with dry Vecchio Samperi in the 1980s.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"good","stable"),(2020,"very_good","stable"),(2021,"very_good","stable"),(2022,"good","stable")]:
    VIN(r3, yr, qd, pt, f"Marsala {yr}: hot western Sicily season, harvest early September")

p3a = P("Marco De Bartoli", "winery", r3, "Italy",
        production_philosophy="traditional",
        philosophy_description="Revivalist of serious dry Marsala; Vecchio Samperi non-fortified perpetuum challenges the DOC with authentic solera wines.",
        reputation_narrative="Marco De Bartoli almost single-handedly rehabilitated Marsala's reputation with benchmark dry Vergine and the perpetuum-aged Vecchio Samperi.",
        price_positioning="premium")
pr3a1, n = PROD("Marco De Bartoli Marsala Superiore Riserva 10 Anni", "wine_fortified", p3a, r3, "Italy",
                subcategory="Marsala Superiore Riserva", price_tier="premium",
                description="Amber Marsala aged 10 years in oak; hazelnut, dried fig, orange peel and caramel with bone-dry finish.")
if n:
    PAIR(pr3a1, "Zabaglione with fresh berries", "complement", "classic", "dessert", "The classic Marsala application; wine and egg custard are inseparable")
    PAIR(pr3a1, "Aged parmigiano reggiano", "complement", "classic", "cheese", "Nutty aged cheese mirrors the hazelnut and caramel of 10-year Marsala")
    PAIR(pr3a1, "Chicken Marsala (pollo alla Marsala)", "complement", "classic", "main", "The definitive culinary use of Marsala, reinforcing sauce with like flavours")
    PAIR(pr3a1, "Tiramisu", "complement", "classic", "dessert", "Marsala's caramel and dried-fruit depth deepens the mascarpone and coffee layers")

pr3a2, n = PROD("Marco De Bartoli Vecchio Samperi Ventennale", "wine_fortified", p3a, r3, "Italy",
                subcategory="Perpetuum Aged Grillo", price_tier="ultra_premium",
                description="20-year perpetuum-aged non-fortified Grillo; concentrated amber with walnut, dried apricot and extraordinary complexity.")
if n:
    PAIR(pr3a2, "Cantucci biscotti with almonds", "complement", "classic", "dessert", "Walnut and almond complexity in both wine and biscotto create resonant harmony")
    PAIR(pr3a2, "Foie gras terrine", "contrast", "established", "starter", "Bone-dry oxidative wine cuts through foie gras richness with nutty tension")
    PAIR(pr3a2, "Prune and walnut tart", "complement", "established", "dessert", "Dried fruit concentration mirrors the pastry's nut and prune filling")
    PAIR(pr3a2, "Aged Comté or Gruyère", "complement", "established", "cheese", "Long-aged cheeses share oxidative nuttiness with perpetuum-aged Grillo")

p3b = P("Florio", "winery", r3, "Italy",
        production_philosophy="traditional",
        philosophy_description="The great historic Marsala house; benchmark Vergine and Superiore from Grillo and Catarratto.",
        reputation_narrative="Founded 1833 by Vincenzo Florio; the defining commercial Marsala producer and custodian of the appellation's heritage.",
        price_positioning="mid_range")
pr3b1, n = PROD("Florio Marsala Vergine Riserva", "wine_fortified", p3b, r3, "Italy",
                subcategory="Marsala Vergine", price_tier="mid_range",
                description="Bone-dry Marsala Vergine aged 5+ years; amber gold with almonds, dried herbs and oxidative complexity.")
if n:
    PAIR(pr3b1, "Roasted almonds and salted pistachios", "complement", "classic", "amuse", "Almond-driven Vergine is the natural companion to roasted nuts")
    PAIR(pr3b1, "Grilled octopus with paprika", "bridge", "suggested", "starter", "Dry oxidative character bridges the charred marine quality of octopus")
    PAIR(pr3b1, "Crostini with olive tapenade", "complement", "established", "starter", "Salty-bitter olives find balance with dry herbal Marsala")
    PAIR(pr3b1, "Pan-fried liver with onions", "complement", "classic", "main", "Classic Venetian-Sicilian dish pairing; Marsala is the traditional sauce base")

pr3b2, n = PROD("Florio Marsala Superiore Dolce", "wine_fortified", p3b, r3, "Italy",
                subcategory="Marsala Superiore Dolce", price_tier="value",
                description="Sweet amber Marsala Superiore; caramel, dried orange and honey with a velvety texture.")
if n:
    PAIR(pr3b2, "Panettone with dried fruit", "complement", "classic", "dessert", "Sweet caramel Marsala echoes the dried fruit of festive panettone")
    PAIR(pr3b2, "Cannoli with ricotta", "complement", "classic", "dessert", "The quintessential Sicilian pairing of Marsala and cannoli")
    PAIR(pr3b2, "Cassata siciliana", "complement", "classic", "dessert", "Island tradition: sweet Marsala accompanies the elaborate marzipan cake")
    PAIR(pr3b2, "Ice cream affogato with espresso", "complement", "suggested", "dessert", "Caramel and coffee notes in Marsala amplify the affogato's bitter-sweet contrast")

# 4. SANTORINI PDO — Greece
print("=== Santorini PDO ===")
r4 = R("Santorini PDO", "Greece", "wine",
        designation_type="PDO",
        designation_name="Santorini PDO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Volcanic island appellation in the Cyclades producing Greece's most celebrated white wines from Assyrtiko. Vines trained in the traditional kouloura (basket) shape to protect from the fierce Aegean winds; grown in volcanic pumice and ash soils. Wines are intensely mineral, saline and acidic, with remarkable ageing potential. Also produces Nykteri (barrel-aged dry white) and Vinsanto (sun-dried dessert wine).",
        key_producers="Domaine Sigalas, Hatzidakis, Gaia Estate, Argyros, Santo Wines",
        historical_context="One of the world's oldest wine regions; Phoenicians introduced viticulture before 1000 BCE. The catastrophic volcanic eruption of c.1600 BCE shaped the caldera. Santorini's distinctive basket-trained vines have survived phylloxera due to volcanic soils.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Santorini {yr}: volcanic island harvest; Assyrtiko's natural acidity preserved by sea winds")

p4a = P("Domaine Sigalas", "winery", r4, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Reference Santorini estate; single-vineyard Assyrtiko showcasing caldera and inland terroir differences.",
        reputation_narrative="Paris Sigalas established the benchmark for modern Santorini Assyrtiko; internationally recognised for structured dry whites.",
        price_positioning="premium")
pr4a1, n = PROD("Sigalas Santorini Assyrtiko", "wine_still", p4a, r4, "Greece",
                subcategory="Assyrtiko", price_tier="premium",
                description="Flagship dry Assyrtiko; electric acidity, volcanic mineral and citrus zest with a crystalline, saline finish.")
if n:
    PAIR(pr4a1, "Grilled whole sea bream with lemon", "complement", "classic", "main", "The definitive Aegean pairing; Assyrtiko's acidity lifts any white fish beautifully")
    PAIR(pr4a1, "Fresh oysters with mignonette", "complement", "classic", "starter", "Saline volcanic mineral mirrors briny oyster; a near-perfect match")
    PAIR(pr4a1, "Fava dip (yellow split peas)", "complement", "classic", "starter", "Traditional Santorini fava dish finds its natural wine companion")
    PAIR(pr4a1, "Raw scallop with citrus vinaigrette", "complement", "established", "starter", "Citrus-mineral Assyrtiko amplifies the vinaigrette while lifting scallop sweetness")

pr4a2, n = PROD("Sigalas Nykteri Santorini", "wine_still", p4a, r4, "Greece",
                subcategory="Assyrtiko-Nykteri", price_tier="premium",
                description="Traditional Nykteri style; partially barrel-fermented Assyrtiko with rich texture yet preserved electric acidity.")
if n:
    PAIR(pr4a2, "Lobster with butter and tarragon", "complement", "established", "main", "Barrel-textured Nykteri matches lobster's richness with mineral precision")
    PAIR(pr4a2, "Grilled swordfish with caper-butter sauce", "complement", "classic", "main", "Richly textured white handles the meaty swordfish and caper butter")
    PAIR(pr4a2, "Aged graviera cheese", "complement", "established", "cheese", "Hard Greek mountain cheese meets the barrel-weight of Nykteri perfectly")
    PAIR(pr4a2, "Seafood risotto with saffron", "complement", "established", "main", "Golden Nykteri's texture meets the richness of a saffron-scented seafood risotto")

p4b = P("Argyros Estate", "winery", r4, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Multi-generational family estate; oldest vines on Santorini; benchmark Vinsanto and dry Assyrtiko.",
        reputation_narrative="Mathew Argyros farms centenarian kouloura vines; Argyros Vinsanto and single-vineyard Assyrtiko are island references.",
        price_positioning="premium")
pr4b1, n = PROD("Argyros Estate Assyrtiko", "wine_still", p4b, r4, "Greece",
                subcategory="Assyrtiko", price_tier="mid_range",
                description="Entry Argyros Assyrtiko; textbook caldera minerality with green citrus, white peach and steely salinity.")
if n:
    PAIR(pr4b1, "Grilled octopus with olive oil and oregano", "complement", "classic", "main", "Iconic Greek pairing; Assyrtiko mineral cuts through charred octopus")
    PAIR(pr4b1, "Taramasalata with pitta", "complement", "classic", "starter", "Briny roe dip finds its natural companion in saline Santorini white")
    PAIR(pr4b1, "Grilled calamari with lemon", "complement", "established", "starter", "Simple squid preparation amplified by Assyrtiko's electric citrus drive")
    PAIR(pr4b1, "Mussels in white wine and garlic", "complement", "classic", "starter", "The briny mussel liquor is mirrored and enhanced by volcanic mineral acidity")

pr4b2, n = PROD("Argyros Vinsanto", "wine_dessert", p4b, r4, "Greece",
                subcategory="Vinsanto", price_tier="ultra_premium",
                description="Sun-dried Assyrtiko Vinsanto aged 10+ years in oak; extraordinary concentration of dried fig, apricot, coffee and iodine.")
if n:
    PAIR(pr4b2, "Greek baklava with honey and pistachios", "complement", "classic", "dessert", "Honey-sweet Vinsanto echoes the syrup-soaked nuts of baklava")
    PAIR(pr4b2, "Blue cheese (Roquefort or similar)", "contrast", "established", "cheese", "Concentrated sweetness of Vinsanto contrasts powerfully with pungent blue")
    PAIR(pr4b2, "Chocolate and coffee desserts", "complement", "established", "dessert", "Coffee and dried-fruit notes in aged Vinsanto mirror chocolate patisserie")
    PAIR(pr4b2, "Foie gras with quince paste", "complement", "established", "starter", "Sun-dried sweetness and apricot concentrate mirror foie gras and quince")

# 5. NEMEA PDO — Greece
print("=== Nemea PDO ===")
r5 = R("Nemea PDO", "Greece", "wine",
        designation_type="PDO",
        designation_name="Nemea PDO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The most important red wine appellation in Greece, in the Peloponnese south of Corinth. Home of Agiorgitiko (St George) grape, producing wines from luscious, ripe mid-range reds to serious, age-worthy Grand Reserve bottlings. Soils of clay and limestone; altitude varies from 250m (valley floor) to 800m (Ancient Nemea). Higher altitude sites produce structured, tannic reds with dark fruit and spice.",
        key_producers="Gaia Wines, Skouras, Papaioannou, Domaine Helios, Economou",
        historical_context="The mythological site of Heracles' first labour (slaying the Nemean Lion). Ancient Nemea hosted the Nemean Games. Wine production documented since antiquity. Agiorgitiko named after the patron saint of the region.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","rising"),(2021,"very_good","rising"),(2022,"very_good","stable")]:
    VIN(r5, yr, qd, pt, f"Nemea {yr}: Peloponnese harvest; higher-altitude sites show best structure")

p5a = P("Gaia Wines", "winery", r5, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Dual-island estate (Nemea and Santorini); serious Agiorgitiko and Assyrtiko showcasing Greek terroir.",
        reputation_narrative="Yiannis Paraskevopoulos and Leon Karatsalos established Gaia as the modernising force in both Nemea and Santorini.",
        price_positioning="premium")
pr5a1, n = PROD("Gaia Estate Agiorgitiko", "wine_still", p5a, r5, "Greece",
                subcategory="Agiorgitiko", price_tier="premium",
                description="Flagship Gaia Nemea; dark cherry, black olive, spice and structured tannins with Mediterranean character.")
if n:
    PAIR(pr5a1, "Moussaka with béchamel", "complement", "classic", "main", "The defining Greek meat dish finds its ideal companion in Nemea Agiorgitiko")
    PAIR(pr5a1, "Grilled lamb souvlaki with tzatziki", "complement", "classic", "main", "Classic Greek barbecue pairing; Agiorgitiko's fruit amplifies lamb's richness")
    PAIR(pr5a1, "Beef stifado with cinnamon and cloves", "complement", "established", "main", "Spiced beef stew echoes the wine's dark-spice complexity beautifully")
    PAIR(pr5a1, "Aged kefalotiri cheese", "complement", "established", "cheese", "Hard Greek sheep's cheese matches Agiorgitiko's structured tannins")

pr5a2, n = PROD("Gaia Notios Red", "wine_still", p5a, r5, "Greece",
                subcategory="Agiorgitiko", price_tier="mid_range",
                description="Approachable Nemea Agiorgitiko; plum, cherry chocolate and soft tannins, ideal for everyday enjoyment.")
if n:
    PAIR(pr5a2, "Pork souvlaki with pita", "complement", "classic", "main", "Everyday Greek street food meets its ideal easy-drinking red companion")
    PAIR(pr5a2, "Pasta with meat ragù", "complement", "established", "main", "Soft tannins and ripe cherry fruit suit a simple tomato meat sauce")
    PAIR(pr5a2, "Cheese and charcuterie board", "complement", "established", "starter", "Versatile Notios works across a spread of cheeses and cured meats")
    PAIR(pr5a2, "Spanakopita", "complement", "suggested", "starter", "Plum fruit and soft structure complement the spinach-feta pastry")

p5b = P("Skouras Winery", "winery", r5, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Leading Nemea estate; single-vineyard Agiorgitiko and blends with international varieties showcase regional potential.",
        reputation_narrative="George Skouras pioneered quality winemaking in Nemea; Megas Oenos blends elevated the appellation internationally.",
        price_positioning="mid_range")
pr5b1, n = PROD("Skouras Megas Oenos", "wine_still", p5b, r5, "Greece",
                subcategory="Agiorgitiko-Cabernet Sauvignon", price_tier="premium",
                description="Benchmark Nemea blend of Agiorgitiko and Cabernet Sauvignon; structured, dark-fruited and age-worthy.")
if n:
    PAIR(pr5b1, "Slow-braised short rib", "complement", "classic", "main", "Cabernet structure and Agiorgitiko fruit elevate slow-braised beef")
    PAIR(pr5b1, "Herb-crusted rack of lamb", "complement", "classic", "main", "Full-bodied blend matches the richness of herb-crusted lamb impeccably")
    PAIR(pr5b1, "Grilled portobello mushrooms", "complement", "established", "main", "Earthy dark fruit and structure complement meaty mushroom umami")
    PAIR(pr5b1, "Aged graviera with walnuts", "complement", "established", "cheese", "Firm Greek cheese and walnut echo the wine's tannic texture and nutty notes")

pr5b2, n = PROD("Skouras Zoe Red", "wine_still", p5b, r5, "Greece",
                subcategory="Agiorgitiko", price_tier="value",
                description="Entry Skouras Agiorgitiko; fresh cherry and plum with light tannins, perfect for the Greek table.")
if n:
    PAIR(pr5b2, "Meatballs in tomato sauce (soutzoukakia)", "complement", "established", "main", "Bright cherry Agiorgitiko complements the spiced tomato sauce of soutzoukakia")
    PAIR(pr5b2, "Grilled chicken with lemon-oregano", "complement", "established", "main", "Herb-roasted chicken finds an everyday companion in accessible Agiorgitiko")
    PAIR(pr5b2, "Falafel with tahini and pita", "complement", "suggested", "main", "Light-bodied red complements the earthy falafel and sesame sauce")
    PAIR(pr5b2, "Antipasto of dolmades and olives", "complement", "established", "starter", "Greek meze table classics match with their natural regional wine")

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
print("B120 complete.")
