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

# ── REGION 1: Cilento ───────────────────────────────────────────────────────
print("=== Region 1: Cilento ===")
r1 = R("Cilento", "Italy", "wine",
        designation_type="DOC", designation_name="Cilento DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Remote southern Campanian DOC in the Cilento national park; produces Aglianico reds, Fiano and Greco whites from ancient coastal-mountain vineyards largely untouched by modernisation.",
        key_producers="Viticoltori De Conciliis, Maffini",
        historical_context="Cilento's ancient Greek settlers planted vines here 3,000 years ago; the region's isolation preserved rare indigenous varieties and traditional viticulture; now attracting quality-focused producers.")
VIN(r1, 2022, "very_good", "stable", "Mediterranean warmth with coastal influence; Aglianico rich and aromatic.")
VIN(r1, 2021, "good", "stable", "Balanced year; Fiano shows classic citrus and mineral precision.")
VIN(r1, 2020, "very_good", "stable", "Excellent ripeness; whites and reds both show southern depth.")
VIN(r1, 2019, "very_good", "stable", "Classic Cilento expression; warm coast-mountain character well delivered.")
VIN(r1, 2018, "good", "stable", "Good drinking vintage; accessible and food-friendly across the range.")
p1a = P("Viticoltori De Conciliis", "winery", r1, "Italy",
        production_philosophy="organic",
        philosophy_description="Pioneer of quality wine in Cilento; Bruno De Conciliis farms organically on ancient terraces and produces ambitious single-vineyard Aglianico and Fiano.",
        reputation_narrative="The most celebrated Cilento producer; Donnaluna Fiano and Naima Aglianico are collector wines.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Luigi Maffini", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Small Cilento estate producing elegant Fiano and Aglianico from coastal hillside vineyards above the Tyrrhenian Sea.",
        reputation_narrative="Growing reputation for precise, mineral wines from this underexplored appellation.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("De Conciliis Donnaluna Cilento Fiano", "wine_still", p1a, r1, "Italy",
                  subcategory="Fiano",
                  description="Coastal Cilento Fiano with hazelnut, lemon oil, white flowers and saline mineral; medium-bodied with excellent freshness and length.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Grilled swordfish with capers and tomato", "complement", "classic", "fish_course", "Southern Italian coastal tradition; Fiano's mineral salinity mirrors Tyrrhenian seafood.")
    PAIR(pr1a, "Fried anchovies with lemon", "complement", "classic", "starter", "Campanian anchovy tradition; Fiano's hazelnut and citrus complement the oily fish perfectly.")
    PAIR(pr1a, "Buffalo mozzarella with San Marzano tomato", "complement", "classic", "starter", "Campanian classic; Fiano's freshness and mineral elevate the simple dairy-tomato combination.")
    PAIR(pr1a, "Grilled prawns with wild herbs", "complement", "established", "fish_course", "Tyrrhenian seafood and coastal Fiano; wild herbs bridge the wine's floral character.")
pr1b, n1b = PROD("Luigi Maffini Kratos Cilento Aglianico", "wine_still", p1b, r1, "Italy",
                  subcategory="Aglianico",
                  description="Coastal Cilento Aglianico with dark cherry, Mediterranean herbs, leather and volcanic mineral; medium to full body with coastal freshness.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Grilled lamb with wild herbs", "complement", "established", "main", "Southern Italian lamb with Aglianico; herb and mineral in harmony.")
    PAIR(pr1b, "Pasta e fagioli (pasta and bean soup)", "complement", "classic", "casual", "Campanian peasant dish with regional Aglianico; rustic unity.")
    PAIR(pr1b, "Porchetta with rosemary", "complement", "established", "main", "Slow-roasted pork with herbs met by Aglianico's structure and dark fruit.")
    PAIR(pr1b, "Caponata with aged provolone", "complement", "established", "starter", "Sweet-sour aubergine and Aglianico's tannin create a surprising southern Italian harmony.")

# ── REGION 2: Aversa (Asprinio di Aversa) ───────────────────────────────────
print("=== Region 2: Asprinio di Aversa ===")
r2 = R("Asprinio di Aversa", "Italy", "wine",
        designation_type="DOC", designation_name="Asprinio di Aversa DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Ancient Campanian DOC near Caserta producing Asprinio — a uniquely tart, low-alcohol white grown in the alberata casertana system (vines trained up poplars to extraordinary heights); rare frizzante style.",
        key_producers="Grotta del Sole, Vestini Campagnano",
        historical_context="Asprinio has grown on the Aversa plain since antiquity; the alberata vine training system is one of Italy's most dramatic; the wine was historically valued for its extreme acidity and used as a digestif.")
VIN(r2, 2022, "good", "stable", "Warm year softens Asprinio's trademark bite; more approachable than usual.")
VIN(r2, 2021, "very_good", "stable", "Classic tart Asprinio; bracing acidity and mineral purity in fine form.")
VIN(r2, 2020, "very_good", "stable", "Excellent vintage for the variety; good balance of tartness and light fruit.")
VIN(r2, 2019, "good", "stable", "Reliable vintage; consistent and honest expression of the unique grape.")
VIN(r2, 2018, "good", "stable", "Standard vintage; Asprinio's acidity well preserved.")
p2a = P("Grotta del Sole", "winery", r2, "Italy",
        production_philosophy="traditional",
        philosophy_description="Largest and most commercially visible producer of Asprinio di Aversa; maintains traditional alberata training and produces both still and frizzante styles.",
        reputation_narrative="Reference producer for the variety; most widely distributed Asprinio internationally.",
        price_positioning="value",
        authority_tier=2)
p2b = P("Vestini Campagnano", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Artisan Aversa producer focused on preserving the alberata tradition and producing authentic, high-acid Asprinio.",
        reputation_narrative="Leading quality voice for the appellation; earns attention from Italian heritage variety specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr2a, n2a = PROD("Grotta del Sole Asprinio di Aversa Frizzante", "wine_sparkling", p2a, r2, "Italy",
                  subcategory="Asprinio",
                  description="Traditional frizzante Asprinio with electrifying acidity, lemon, green apple and chalk mineral; ultra-refreshing and unusual.",
                  price_tier="value")
if n2a:
    PAIR(pr2a, "Pizza Napoletana margherita", "complement", "classic", "casual", "Naples is just down the road; Asprinio's tartness and fizz is the traditional pizza companion.")
    PAIR(pr2a, "Fried pizza (pizza fritta)", "complement", "classic", "casual", "Oily fried dough needs extreme acidity to cut through; Asprinio's tartness is the solution.")
    PAIR(pr2a, "Mozzarella di bufala fritta", "complement", "established", "starter", "Fried mozzarella richness dissolved by Asprinio's bracing acidity; classic Campanian match.")
    PAIR(pr2a, "Spaghetti alle vongole", "complement", "classic", "main", "Clam pasta and tart southern Italian white; acidity and brine in resonance.")
pr2b, n2b = PROD("Vestini Campagnano Asprinio di Aversa Bianco", "wine_still", p2b, r2, "Italy",
                  subcategory="Asprinio",
                  description="Still Asprinio with searingly high acidity, citrus, green apple and mineral depth; one of Italy's most demanding and individual white wines.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Raw oysters with shallot mignonette", "complement", "classic", "starter", "Briny oysters demand bracing acidity; Asprinio's intensity is perfect.")
    PAIR(pr2b, "Lemon granita with brioche", "complement", "classic", "pre_dessert", "Sicily-adjacent palate cleanser; Asprinio's citrus tartness echoes lemon granita perfectly.")
    PAIR(pr2b, "Fried whitebait with lemon", "complement", "classic", "starter", "Tiny fried fish needs high-acid wine; Asprinio cuts through the oil and amplifies the lemon.")
    PAIR(pr2b, "Grilled calamari rings", "complement", "established", "starter", "Grilled squid and tart Campanian white; acidity cleans the palate between bites.")

# ── REGION 3: Falerno del Massico ────────────────────────────────────────────
print("=== Region 3: Falerno del Massico ===")
r3 = R("Falerno del Massico", "Italy", "wine",
        designation_type="DOC", designation_name="Falerno del Massico DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Ancient Campanian DOC on Monte Massico producing Falangina whites and Primitivo-Aglianico reds; the most celebrated wine of ancient Rome is being revived by quality-focused modern producers.",
        key_producers="Villa Matilde, Moio",
        historical_context="Falernian wine was the most prized wine of ancient Rome; Virgil, Horace and Pliny all celebrated it; modern Falerno del Massico revives this extraordinary heritage on Monte Massico's volcanic slopes.")
VIN(r3, 2022, "very_good", "stable", "Warm Mediterranean season; Falanghina rich and aromatic; reds full-bodied.")
VIN(r3, 2021, "good", "stable", "Balanced year; Falanghina shows classic mineral freshness.")
VIN(r3, 2020, "very_good", "stable", "Good ripeness across both colours; solid vintage.")
VIN(r3, 2019, "very_good", "stable", "Warm and expressive; Primitivo-Aglianico blend shows excellent depth.")
VIN(r3, 2018, "good", "stable", "Consistent vintage; good food-friendly expressions.")
p3a = P("Villa Matilde", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The premier revivalist of Falerno del Massico; Villa Matilde's research reconstructed the ancient appellation using ampelography and Roman texts.",
        reputation_narrative="Most celebrated Falerno producer; Vigna Caracci Falanghina and Rosso are benchmark wines of this historic appellation.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Michele Moio", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Small family estate producing Falerno del Massico whites and reds with emphasis on Monte Massico volcanic terroir expression.",
        reputation_narrative="Respected local producer contributing to the appellation's growing reputation.",
        price_positioning="mid_range",
        authority_tier=1)
pr3a, n3a = PROD("Villa Matilde Falerno del Massico Bianco Vigna Caracci", "wine_still", p3a, r3, "Italy",
                  subcategory="Falanghina",
                  description="Benchmark Falanghina from ancient Monte Massico vineyards; floral, citrus, mineral and a distinctive volcanic smoky note; excellent ageing potential.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Grilled sea bass with lemon and herbs", "complement", "classic", "fish_course", "Ancient coastal tradition; Falanghina's mineral and citrus complement Tyrrhenian fish.")
    PAIR(pr3a, "Clams with garlic and white wine", "complement", "classic", "starter", "Campanian shellfish classic; Falanghina in the pan and in the glass.")
    PAIR(pr3a, "Mozzarella di bufala with basil", "complement", "classic", "starter", "Campanian purity pairing; fresh dairy and mineral white in natural harmony.")
    PAIR(pr3a, "Frittura di paranza (mixed fried seafood)", "complement", "established", "casual", "Southern coastal tradition; Falanghina's mineral acidity cuts through the frying oil.")
pr3b, n3b = PROD("Villa Matilde Falerno del Massico Rosso Vigna Camarato", "wine_still", p3a, r3, "Italy",
                  subcategory="Aglianico-Primitivo blend",
                  description="Flagship Falerno rosso from Aglianico and Primitivo; concentrated dark fruit, volcanic mineral and excellent structure; the modern heir to Rome's most celebrated wine.",
                  price_tier="premium")
if n3b:
    PAIR(pr3b, "Slow-braised lamb shoulder with herbs", "complement", "classic", "main", "The ancient Roman banquet combination revived; lamb and volcanic Falernian red.")
    PAIR(pr3b, "Spit-roasted suckling pig", "complement", "established", "main", "Maiale al forno with structured Falerno; tannin and dark fruit balance the pork richness.")
    PAIR(pr3b, "Aged Pecorino Romano", "complement", "classic", "cheese", "Ancient Roman cheese and wine pairing; sharp Pecorino and tannic Falerno in historical harmony.")
    PAIR(pr3b, "Braised wild boar with polenta", "complement", "established", "main", "Southern Italian hunting tradition; Falerno's power meets gamey boar.")

# ── REGION 4: Caserta / Terra di Lavoro ──────────────────────────────────────
print("=== Region 4: Terre del Volturno ===")
r4 = R("Terre del Volturno", "Italy", "wine",
        designation_type="IGT", designation_name="Terre del Volturno IGT",
        reputation_tier="emerging",
        quality_trajectory="ascending",
        description="Campanian IGT in the Volturno river valley near Caserta; home to Galardi's Terra di Lavoro — one of Italy's most celebrated cult reds combining Aglianico and Piedirosso on volcanic Monte Massico slopes.",
        key_producers="Galardi, Nanni Copé",
        historical_context="The Galardi family's Terra di Lavoro transformed this obscure IGT into one of Italy's most sought collector wines; the ancient Campanian variety Piedirosso adds complexity to Aglianico's power.")
VIN(r4, 2022, "excellent", "rising", "Outstanding vintage; Terra di Lavoro achieves extraordinary depth and concentration.")
VIN(r4, 2021, "very_good", "stable", "Classic expression; Aglianico and Piedirosso in elegant balance.")
VIN(r4, 2020, "excellent", "rising", "One of the greatest vintages for Campania's top reds; exceptional ageing potential.")
VIN(r4, 2019, "very_good", "stable", "Rich and generous; Terra di Lavoro shows volcanic intensity and depth.")
VIN(r4, 2018, "very_good", "stable", "Strong vintage; complex and structured with good length.")
p4a = P("Galardi", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Tiny family estate producing a single wine — Terra di Lavoro — from Aglianico and Piedirosso on volcanic Monte Massico; production is a few thousand cases.",
        reputation_narrative="Terra di Lavoro is universally acknowledged as one of Italy's great reds; scores 95-100 in all major publications.",
        price_positioning="ultra_premium",
        authority_tier=2)
p4b = P("Nanni Copé", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Rising Campanian producer working indigenous Pallagrello and Casavecchia varieties from ancient volcanic soils near Caserta.",
        reputation_narrative="Rapidly gaining critical attention for reviving lost Campanian varieties; Sabbie di Sopra il Bosco gaining collector status.",
        price_positioning="premium",
        authority_tier=1)
pr4a, n4a = PROD("Galardi Terra di Lavoro Terre del Volturno", "wine_still", p4a, r4, "Italy",
                  subcategory="Aglianico-Piedirosso",
                  description="Cult Campanian red of immense power and complexity; volcanic mineral, dark plum, leather, tar and tobacco with a 20+ year ageing horizon.",
                  price_tier="ultra_premium")
if n4a:
    PAIR(pr4a, "Dry-aged Chianina tagliata", "complement", "classic", "main", "Italy's greatest red beef deserves Italy's most powerful red; volcanic mineral meets Chianina depth.")
    PAIR(pr4a, "Roasted wild boar with juniper and bay", "complement", "classic", "main", "Gamey wild boar and volcanic Campanian red; power meets power in southern Italian tradition.")
    PAIR(pr4a, "Aged Caciocavallo Silano", "complement", "classic", "cheese", "Ancient southern Italian cheese with ancient Campanian wine; volcanic mineral in both.")
    PAIR(pr4a, "Braised osso buco Napoletano", "complement", "established", "main", "Slow-braised collagen-rich veal shin met by Terra di Lavoro's full body and structure.")
pr4b, n4b = PROD("Nanni Copé Sabbie di Sopra il Bosco Casavecchia", "wine_still", p4b, r4, "Italy",
                  subcategory="Casavecchia",
                  description="Single-variety Casavecchia IGT with red cherry, tobacco, pepper and volcanic mineral; medium-full body with unexpected elegance for a southern Italian red.",
                  price_tier="premium")
if n4b:
    PAIR(pr4b, "Salsicce e friarielli (sausage and broccoli)", "complement", "classic", "main", "Campanian classic combination; bitter greens and pork sausage with indigenous Casavecchia.")
    PAIR(pr4b, "Slow-cooked ragù Napoletano", "complement", "classic", "main", "Sunday Naples ragù cooked for hours; Casavecchia's tannin and fruit absorb the richness.")
    PAIR(pr4b, "Grilled Campanian lamb chops", "complement", "established", "main", "Southern lamb with indigenous red variety; regional tradition in modern form.")
    PAIR(pr4b, "Meatballs in tomato sauce (polpette)", "complement", "classic", "casual", "Classic Campanian home cooking with local red wine; unpretentious southern harmony.")

# ── REGION 5: Guardiolo ─────────────────────────────────────────────────────
print("=== Region 5: Guardiolo ===")
r5 = R("Guardiolo", "Italy", "wine",
        designation_type="DOC", designation_name="Guardiolo DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Small Sannio DOC in Benevento province producing Aglianico, Falanghina and Greco from inland Campanian hills; wines of rustic character and excellent local food compatibility.",
        key_producers="Cantina del Taburno, Fattoria La Rivolta",
        historical_context="Guardiolo occupies the ancient Samnite wine lands of inland Campania; Falanghina del Sannio here shows a more structured, mineral character than coastal equivalents.")
VIN(r5, 2022, "very_good", "stable", "Inland continental warmth; Aglianico shows excellent ripeness and depth.")
VIN(r5, 2021, "good", "stable", "Balanced season; Falanghina and Greco both show good freshness.")
VIN(r5, 2020, "very_good", "stable", "Classic Sannio vintage; reliable and expressive across the range.")
VIN(r5, 2019, "good", "stable", "Good everyday drinking vintage; accessible and food-friendly.")
VIN(r5, 2018, "good", "stable", "Solid vintage; honest expressions of local varieties.")
p5a = P("Cantina del Taburno", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Cooperative winery and leading Sannio producer; wide range from Falanghina del Sannio to Aglianico del Taburno; benchmark for the Benevento hills.",
        reputation_narrative="Most widely distributed Sannio producer; consistent quality across an extensive range.",
        price_positioning="value",
        authority_tier=1)
p5b = P("Fattoria La Rivolta", "winery", r5, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic family estate in Sannio producing Falanghina and Aglianico with emphasis on clean, food-friendly expressions.",
        reputation_narrative="Growing reputation for quality organic Sannio wines; earns attention from Italian specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Cantina del Taburno Falanghina del Sannio", "wine_still", p5a, r5, "Italy",
                  subcategory="Falanghina",
                  description="Inland Sannio Falanghina with more structure than coastal versions; citrus, white peach and mineral freshness with good weight.",
                  price_tier="value")
if n5a:
    PAIR(pr5a, "Maccheroni al ragù di agnello", "complement", "classic", "main", "Sannio lamb ragù with local Falanghina; regional Campanian table tradition.")
    PAIR(pr5a, "Grilled sausage with Friarielli", "complement", "established", "main", "Pork sausage and bitter greens lifted by Falanghina's freshness.")
    PAIR(pr5a, "Pasta e ceci (pasta and chickpea)", "complement", "classic", "casual", "Peasant Campanian cooking with food-friendly local white; simple harmony.")
    PAIR(pr5a, "Aged provolone with honey", "complement", "established", "cheese", "Southern Italian cheese course; Falanghina's freshness balances provolone's sharpness.")
pr5b, n5b = PROD("Fattoria La Rivolta Sannio Aglianico", "wine_still", p5b, r5, "Italy",
                  subcategory="Aglianico",
                  description="Organic inland Aglianico with dark cherry, tobacco, iron mineral and firm tannins; honest and food-driven.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Braised lamb with peppers (agnello con peperoni)", "complement", "classic", "main", "Campanian feast dish; pepper sweetness and lamb richness met by Aglianico's structure.")
    PAIR(pr5b, "Soppressata calabrese with olives", "complement", "established", "casual", "Spiced cured pork and tannic southern red; the tannin tames the fat.")
    PAIR(pr5b, "Grilled lamb ribs with herbs", "complement", "classic", "main", "Southern Italian grilling tradition; Aglianico's acidity and tannin elevate the lamb richness.")
    PAIR(pr5b, "Parmigiana di melanzane", "complement", "classic", "main", "Aubergine parmigiana is a pan-southern Italian classic; Aglianico's fruit and acid balance the tomato richness.")

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
