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

# ── REGION 1: Bianco di Custoza DOCG ─────────────────────────────────────────
# Switch to new regions - targeting Central/Southern Italian and emerging areas

print("=== Region 1: Greco di Bianco ===")
r1 = R("Greco di Bianco", "Italy", "wine",
        designation_type="DOC", designation_name="Greco di Bianco DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Tiny Calabrian DOC near Bianco on the Ionian coast; produces a passito-style sweet wine from Greco Bianco dried in the sun; one of Italy's rarest and most extraordinary dessert wines.",
        key_producers="Umberto Ceratti, Cantine Lento",
        historical_context="Greco di Bianco has been made since antiquity; the drying process concentrates extraordinary honey, apricot and orange peel flavours; Umberto Ceratti's single-estate production is Italy's most artisanal wine.")
VIN(r1, 2022, "very_good", "stable", "Hot Ionian summer ideal for sun-drying; Greco shows exceptional sweetness and concentration.")
VIN(r1, 2021, "good", "stable", "Classic vintage; honey and dried apricot well balanced by natural acidity.")
VIN(r1, 2020, "very_good", "stable", "Good drying conditions; concentrated and aromatic passito.")
VIN(r1, 2019, "very_good", "stable", "Warm Calabrian year; Greco di Bianco shows excellent orange peel depth.")
VIN(r1, 2018, "good", "stable", "Standard vintage; reliable sweet expression of this ancient variety.")
p1a = P("Umberto Ceratti", "winery", r1, "Italy",
        production_philosophy="traditional",
        philosophy_description="The lone artisan producer making Greco di Bianco with complete traditional methods; sun-drying, ancient presses and minimal intervention.",
        reputation_narrative="Ceratti's Greco di Bianco is one of Italy's rarest wines; earns 95+ scores from all who discover it.",
        price_positioning="premium",
        authority_tier=2)
p1b = P("Cantine Lento", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Calabrian estate producing a small volume of Greco di Bianco passito alongside an extensive table wine range.",
        reputation_narrative="Most commercially accessible Greco di Bianco; reliable quality for the style.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Ceratti Greco di Bianco Passito", "wine_dessert", p1a, r1, "Italy",
                  subcategory="Greco Bianco",
                  description="Italy's rarest passito; extraordinary honey, apricot, orange peel and saffron with balancing acidity; 50+ year ageing potential from a single artisan producer.",
                  price_tier="ultra_premium")
if n1a:
    PAIR(pr1a, "Almond and citrus torrone", "complement", "classic", "dessert", "Torrone's almond-honey character mirrors Greco di Bianco's extraordinary richness and floral depth.")
    PAIR(pr1a, "Aged Pecorino di Crotonese with fig jam", "complement", "classic", "cheese", "Calabrian aged sheep's cheese with the region's dessert wine; honey and fig bridge the two.")
    PAIR(pr1a, "Fresh ricotta with chestnut honey", "complement", "established", "dessert", "Simple ricotta and complex dessert wine; honey links both and the contrast is beautiful.")
    PAIR(pr1a, "Foie gras terrine with brioche", "complement", "established", "starter", "Fatty richness balanced by the wine's acidity and sweet depth; an unusual Italian luxury pairing.")
pr1b, n1b = PROD("Cantine Lento Greco di Bianco Passito Calabria", "wine_dessert", p1b, r1, "Italy",
                  subcategory="Greco Bianco",
                  description="Accessible Greco di Bianco passito with honey, dried apricot and orange; good acidity and persistence; more approachable than artisan examples.",
                  price_tier="premium")
if n1b:
    PAIR(pr1b, "Sfinge di San Giuseppe (Sicilian cream puff)", "complement", "established", "dessert", "Southern Italian pastry tradition; the wine's honey and orange complement the cream filling.")
    PAIR(pr1b, "Dried fruit and nut panforte", "complement", "classic", "dessert", "Tuscan-style dense fruit cake and Italian passito; spice, honey and dried fruit echo in both.")
    PAIR(pr1b, "Semifreddo al pistacchio", "complement", "established", "dessert", "Pistachio ice cream cake and orange-honey passito; nut richness and citrus bridge.")
    PAIR(pr1b, "Cannoli con ricotta di pecora", "complement", "classic", "dessert", "Sicilian pastry tradition at the southern Italian table; orange and honey in wine and shell filling.")

# ── REGION 2: Cirò ───────────────────────────────────────────────────────────
print("=== Region 2: Cirò ===")
r2 = R("Cirò", "Italy", "wine",
        designation_type="DOC", designation_name="Cirò DOC",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Ancient Calabrian DOC on the Ionian coast; produces Gaglioppo reds and Greco Bianco whites from the vine-land that once supplied the winners of the Olympic Games in ancient Kroton.",
        key_producers="Librandi, Scala",
        historical_context="Cirò is among the world's oldest continuously farmed wine zones; Gaglioppo was the Olympic wine given to victors from Kroton; modern producers are reviving Cirò's extraordinary ancient heritage with quality focus.")
VIN(r2, 2022, "very_good", "stable", "Hot Ionian season; Gaglioppo shows rich dark cherry and rustic depth.")
VIN(r2, 2021, "good", "stable", "Balanced year; Gaglioppo more elegant and aromatic than usual.")
VIN(r2, 2020, "very_good", "stable", "Good vintage; both Gaglioppo and Greco express fine Calabrian character.")
VIN(r2, 2019, "very_good", "stable", "Warm and expressive; Cirò's ancient character well delivered.")
VIN(r2, 2018, "good", "stable", "Standard vintage; honest and food-friendly ancient wines.")
p2a = P("Librandi", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Calabria's most internationally recognised producer; Librandi's research into indigenous varieties has defined modern Calabrian wine quality.",
        reputation_narrative="Librandi's Gravello and Magno Megonio are Italy's most acclaimed Calabrian reds; Cirò Rosso Duca San Felice is the appellation benchmark.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Scala", "winery", r2, "Italy",
        production_philosophy="traditional",
        philosophy_description="Small traditional Cirò estate producing honest Gaglioppo from ancient coastal vineyards with minimal intervention.",
        reputation_narrative="Respected for authentic, unmanipulated Cirò character; earns specialist attention.",
        price_positioning="value",
        authority_tier=1)
pr2a, n2a = PROD("Librandi Cirò Rosso Classico Superiore Duca San Felice", "wine_still", p2a, r2, "Italy",
                  subcategory="Gaglioppo",
                  description="Benchmark Cirò Rosso; wild cherry, dried plum, leather and Ionian mineral; medium body with rustic tannin and Southern Italian warmth.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Fileja con ragù di capra (goat pasta)", "complement", "classic", "main", "Calabrian pasta shape with goat ragù; ancient wine and ancient southern Italian cooking.")
    PAIR(pr2a, "Grilled kid (capretto) with wild herbs", "complement", "classic", "main", "Easter kid goat and Gaglioppo; the ancient Calabrian feast combination.")
    PAIR(pr2a, "Soppressata calabrese piccante", "complement", "classic", "casual", "Calabria's spiced cured pork with ancient wine; rustic unity.")
    PAIR(pr2a, "Pasta e fagioli con cotenna", "complement", "classic", "casual", "Southern Italian pork rind and bean pasta; Cirò's tannin cuts through the fat.")
pr2b, n2b = PROD("Librandi Critone Cirò Bianco Greco Bianco", "wine_still", p2b, r2, "Italy",
                  subcategory="Greco Bianco",
                  description="Crisp Cirò Bianco from Greco; citrus, sea mineral and a distinctive bitter almond note; refreshing coastal white.",
                  price_tier="value")
if n2b:
    PAIR(pr2b, "Alici di Calabria marinate", "complement", "classic", "starter", "Calabrian marinated anchovies and local white; coastal acidity and mineral in harmony.")
    PAIR(pr2b, "Grilled Calabrian swordfish with capers", "complement", "classic", "fish_course", "Ionian swordfish and Ionian wine; capers bridge the wine's almond bitterness.")
    PAIR(pr2b, "Peperoni ripieni (stuffed peppers)", "complement", "classic", "main", "Calabrian stuffed pepper tradition; the wine's freshness balances the sweet pepper richness.")
    PAIR(pr2b, "Pasta con 'nduja e pomodoro", "complement", "established", "main", "Spiced 'nduja and tomato pasta; Greco's acidity and mineral balance the intense heat.")

# ── REGION 3: Savuto ─────────────────────────────────────────────────────────
print("=== Region 3: Savuto ===")
r3 = R("Savuto", "Italy", "wine",
        designation_type="DOC", designation_name="Savuto DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Inland Calabrian DOC on the Savuto river valley; Gaglioppo-based reds with Greco and Malvasia whites from ancient hillside terraces; a discovery wine of the Italian south.",
        key_producers="Odoardi, Statti",
        historical_context="Savuto's ancient wines were celebrated in antiquity; the valley's cooler microclimate gives more structure and freshness than coastal Cirò; revived by a small group of committed producers in the 1990s.")
VIN(r3, 2022, "very_good", "stable", "Valley cooling moderated the hot season; wines show good freshness and structure.")
VIN(r3, 2021, "good", "stable", "Balanced Savuto vintage; Gaglioppo aromatic and elegant.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; valley terroir delivers mineral character alongside southern warmth.")
VIN(r3, 2019, "good", "stable", "Standard vintage; honest and food-friendly.")
VIN(r3, 2018, "good", "stable", "Reliable vintage; consistent Savuto character.")
p3a = P("Odoardi", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The most historically important Savuto producer; 400 years of Odoardi family viticulture in the Savuto valley; multiple cru bottlings including Vigna Mortilla.",
        reputation_narrative="Odoardi's Vigna Mortilla is Calabria's most awarded inland red; transformative for Savuto's reputation.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Statti", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Large Calabrian estate producing Savuto and other Calabrian varieties from extensive valley holdings.",
        reputation_narrative="Most widely distributed Calabrian estate; Gaglioppo and Greco wines consistently reliable.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Odoardi Savuto Superiore Vigna Mortilla", "wine_still", p3a, r3, "Italy",
                  subcategory="Gaglioppo blend",
                  description="Single-vineyard Savuto from Gaglioppo, Nerello and Magliocco; complex dark cherry, leather, mountain herbs and valley mineral; structured and age-worthy.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Roasted kid with mountain herbs", "complement", "classic", "main", "Calabrian mountain kid roast and valley Gaglioppo; ancient pastoral combination.")
    PAIR(pr3a, "Pasta al ragù di capra e pecorino", "complement", "classic", "main", "Goat ragù and Calabrian red; pecorino and mountain herbs bridge the wine's aromatics.")
    PAIR(pr3a, "Slow-roasted pork with 'nduja", "complement", "established", "main", "Calabrian spiced pork fat and tannic inland red; Southern Italian firepower.")
    PAIR(pr3a, "Aged Caciocavallo Silano", "complement", "classic", "cheese", "Ancient Calabrian cheese with ancient Calabrian wine; mountain terroir in both.")
pr3b, n3b = PROD("Statti Calabria Gaglioppo", "wine_still", p3b, r3, "Italy",
                  subcategory="Gaglioppo",
                  description="Accessible Calabrian Gaglioppo with dark cherry, tobacco and valley mineral; medium-bodied and food-driven.",
                  price_tier="value")
if n3b:
    PAIR(pr3b, "Grilled lamb sausages with herbs", "complement", "classic", "casual", "Southern Italian sausage tradition and accessible red; rustic harmony.")
    PAIR(pr3b, "Parmigiana di melanzane alla calabrese", "complement", "classic", "main", "Calabrian aubergine parmigiana; tomato and aubergine richness balanced by Gaglioppo's tannin.")
    PAIR(pr3b, "Pizza con 'nduja e fior di latte", "complement", "established", "casual", "Calabrian spiced pizza with local red; the 'nduja's heat and the wine's tannin create southern harmony.")
    PAIR(pr3b, "Pasta con pomodoro e peperoncino", "complement", "classic", "casual", "Simple Calabrian pasta; honest everyday wine and honest everyday cooking.")

# ── REGION 4: Campania Fiano di Avellino DOCG ── (already added, check)
# Targeting fresh: Primitivo di Manduria Dolce Naturale DOCG
print("=== Region 4: Primitivo di Manduria Dolce Naturale ===")
r4 = R("Primitivo di Manduria Dolce Naturale", "Italy", "wine",
        designation_type="DOCG", designation_name="Primitivo di Manduria Dolce Naturale DOCG",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Puglia's sweet Primitivo DOCG; naturally sweet wine from partially dried Primitivo (Zinfandel's ancestor) in the Manduria zone; extraordinary richness of dried fig, chocolate and spice with fortified-wine intensity.",
        key_producers="Pervini, Cantine San Marzano",
        historical_context="Primitivo di Manduria has been made since at least the 18th century; Primitivo (Zinfandel) thrives in Puglia's hot limestone plains; the dolce naturale style is fermentation-stopped by the wine's own sugar.")
VIN(r4, 2022, "very_good", "stable", "Hot Puglia season ideal for Primitivo concentration; dolce style excellent.")
VIN(r4, 2021, "good", "stable", "Balanced vintage; Primitivo shows good sugar concentration for the dolce style.")
VIN(r4, 2020, "very_good", "stable", "Good vintage; classic rich and sweet Primitivo character.")
VIN(r4, 2019, "very_good", "stable", "Warm and generous; exceptional sugar and alcohol concentration in the dolce style.")
VIN(r4, 2018, "good", "stable", "Reliable vintage; consistent dolce expression.")
p4a = P("Pervini", "winery", r4, "Italy",
        production_philosophy="traditional",
        philosophy_description="Benchmark Primitivo di Manduria Dolce Naturale producer; Archidamo is the appellation's most internationally recognised wine.",
        reputation_narrative="Most awarded Manduria Dolce Naturale producer; Archidamo earns consistent top scores internationally.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Cantine San Marzano", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Large Manduria cooperative producing commercially important Primitivo and Primitivo Dolce Naturale; quality focus across extensive range.",
        reputation_narrative="Most commercially significant Manduria producer; Sessantanni Primitivo is an internationally beloved wine.",
        price_positioning="mid_range",
        authority_tier=2)
pr4a, n4a = PROD("Pervini Archidamo Primitivo di Manduria Dolce Naturale", "wine_dessert", p4a, r4, "Italy",
                  subcategory="Primitivo",
                  description="Benchmark dolce naturale with extraordinary concentration; dried fig, dark chocolate, coffee, warm spice and remarkable persistence; naturally sweet with high alcohol.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Dark chocolate and espresso torta", "complement", "classic", "dessert", "Chocolate cake meets chocolate-fig wine; espresso intensity bridges the two southern Italian worlds.")
    PAIR(pr4a, "Crostata di fichi secchi (dried fig tart)", "complement", "classic", "dessert", "Dried fig in both wine and pastry; the wine's fig concentration and sweet pastry in harmony.")
    PAIR(pr4a, "Aged Pecorino di Taranto with honey", "complement", "established", "cheese", "Puglia aged sheep cheese and local sweet wine; honey bridges both.")
    PAIR(pr4a, "Panettone with dried fruit", "complement", "classic", "dessert", "Italian festive cake and southern sweet wine; Christmas table harmony.")
pr4b, n4b = PROD("Cantine San Marzano Primitivo di Manduria Dolce Naturale", "wine_dessert", p4b, r4, "Italy",
                  subcategory="Primitivo",
                  description="Accessible Manduria Dolce Naturale with dark fruit sweetness, mocha and dried spice; approachable and consistent expression.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Tiramisù al caffè", "complement", "classic", "dessert", "Italy's favourite dessert and southern Italy's sweet wine; espresso and mascarpone echo the wine.")
    PAIR(pr4b, "Cartellate pugliesi (fried Christmas pastry)", "complement", "classic", "dessert", "Puglia's traditional Christmas pastry with the region's dolce wine; southern festive unity.")
    PAIR(pr4b, "Gorgonzola naturale with walnut bread", "complement", "established", "cheese", "Blue cheese and sweet Primitivo; walnut bitterness bridges the wine's fruit and the cheese's funk.")
    PAIR(pr4b, "Pasticciotto leccese (Puglia pastry cream)", "complement", "classic", "dessert", "Lecce's custard-filled pastry and southern sweet wine; cream and fruit echo.")

# ── REGION 5: Castel del Monte Nero di Troia ─────────────────────────────────
print("=== Region 5: Castel del Monte Nero di Troia ===")
r5 = R("Castel del Monte Nero di Troia", "Italy", "wine",
        designation_type="DOCG", designation_name="Castel del Monte Nero di Troia DOCG",
        reputation_tier="overlooked",
        quality_trajectory="ascending",
        description="Puglia DOCG on the Murge plateau producing Nero di Troia — a noble, structured red variety of real depth and ageing potential; quite different from Primitivo in its Northern Rhône-like austerity and mineral character.",
        key_producers="Rivera, Torrevento",
        historical_context="Nero di Troia (also called Uva di Troia) is one of Puglia's most ancient varieties; Rivera's Puer Apuliae single-vineyard wine revealed the DOCG's exceptional potential in the 1990s; still undervalued internationally.")
VIN(r5, 2022, "very_good", "stable", "Warm Murge plateau; Nero di Troia shows excellent dark fruit and mineral depth.")
VIN(r5, 2021, "good", "stable", "Balanced year; elegant and aromatic Nero di Troia with refreshing acidity.")
VIN(r5, 2020, "excellent", "rising", "Outstanding vintage; depth and complexity both exceptional for the DOCG.")
VIN(r5, 2019, "very_good", "stable", "Classic expression; structured and mineral with dark cherry and iron.")
VIN(r5, 2018, "very_good", "stable", "Strong vintage; age-worthy Nero di Troia with good tannin management.")
p5a = P("Rivera", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Puglia's most quality-focused winery; De Corato family has led Castel del Monte's prestige for decades; Puer Apuliae is Italy's most awarded Nero di Troia.",
        reputation_narrative="Rivera is Puglia's most respected traditional winery; Puer Apuliae consistently earns 95+ points.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Torrevento", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Large Castel del Monte estate producing excellent Nero di Troia and Bombino Bianco from Murge plateau vineyards.",
        reputation_narrative="Most commercially important Castel del Monte producer; Torre del Falco is a widely available quality benchmark.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Rivera Puer Apuliae Castel del Monte Nero di Troia", "wine_still", p5a, r5, "Italy",
                  subcategory="Nero di Troia",
                  description="Landmark single-vineyard Nero di Troia; dark cherry, iron, leather and mineral with a structured austerity unusual in Puglia; 15+ year ageing horizon.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Braised orecchiette al ragù di carne", "complement", "classic", "main", "Puglia's ear-shaped pasta with meat ragù and the region's finest red; regional harmony.")
    PAIR(pr5a, "Slow-roasted lamb with wild fennel", "complement", "established", "main", "Southern Italian lamb and structured Nero di Troia; wild fennel bridges through the wine's herb.")
    PAIR(pr5a, "Pecorino di Foggia stagionato", "complement", "classic", "cheese", "Aged Puglia sheep's cheese and Nero di Troia mineral; iron and dairy in balance.")
    PAIR(pr5a, "Bombette pugliesi (pork involtini)", "complement", "classic", "casual", "Puglia's signature pork rolls with local red; the stuffed pancetta and wine — a Puglia institution.")
pr5b, n5b = PROD("Torrevento Torre del Falco Castel del Monte Nero di Troia", "wine_still", p5b, r5, "Italy",
                  subcategory="Nero di Troia",
                  description="Accessible Nero di Troia with dark cherry, tobacco, mineral and soft tannin; food-friendly and consistent.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Orecchiette con cime di rapa", "complement", "classic", "main", "Puglia's iconic pasta dish with bitter rape greens; Nero di Troia's tannin complements the bitterness.")
    PAIR(pr5b, "Grilled meat skewers with onion and bay", "complement", "classic", "casual", "Puglia barbecue tradition; accessible Nero di Troia handles the charred meat perfectly.")
    PAIR(pr5b, "Lampascioni in olio (wild onions in oil)", "complement", "classic", "casual", "Bitter Puglia wild onion antipasto and local red; bitterness echoes the wine's mineral tannin.")
    PAIR(pr5b, "Pizza al forno con salsiccia e friarielli", "complement", "established", "casual", "Sausage and broccoli pizza and structured red; the Puglia-Campania crossover dish.")

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
