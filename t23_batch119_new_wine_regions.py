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

# ── REGION 1: Locorotondo ─────────────────────────────────────────────────────
print("=== Region 1: Locorotondo ===")
r1 = R("Locorotondo", "Italy", "wine",
        designation_type="DOC", designation_name="Locorotondo DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Puglia Valley of Trulli DOC producing Verdeca and Bianco d'Alessano whites from the Itria valley; fresh, crisp and mineral with unusual citrus clarity for a southern Italian white.",
        key_producers="Cantina Locorotondo, Leone de Castris",
        historical_context="Locorotondo is the hilltop whitewashed town in Puglia's trulli country; the wines historically served the olive oil and pasta culture of the Itria valley; local cooperative produces the benchmark.")
VIN(r1, 2022, "very_good", "stable", "Itria valley cooling moderated hot season; Verdeca shows excellent citrus freshness.")
VIN(r1, 2021, "good", "stable", "Classic vintage; light and aromatic with clean mineral acidity.")
VIN(r1, 2020, "very_good", "stable", "Good vintage; more body and length than usual for the DOC.")
VIN(r1, 2019, "good", "stable", "Standard vintage; reliable and food-friendly Locorotondo character.")
VIN(r1, 2018, "good", "stable", "Consistent vintage; honest everyday Puglia white.")
p1a = P("Cantina Cooperativa di Locorotondo", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The local cooperative and benchmark producer of Locorotondo DOC; Verdeca and Bianco d'Alessano from the Itria valley's limestone and red clay soils.",
        reputation_narrative="The reference producer for the appellation; fresh, mineral whites that embody Puglia's white wine potential.",
        price_positioning="value",
        authority_tier=2)
p1b = P("Leone de Castris", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="One of Puglia's oldest and most historic estates; wide range including Locorotondo whites and Salice Salentino reds.",
        reputation_narrative="Leone de Castris is Puglia's most historic producer; Five Roses rosé was Italy's first commercially exported rosé (1943).",
        price_positioning="mid_range",
        authority_tier=2)
pr1a, n1a = PROD("Cantina di Locorotondo Verdeca Bianco", "wine_still", p1a, r1, "Italy",
                  subcategory="Verdeca-Bianco d'Alessano",
                  description="Benchmark Locorotondo with citrus, lemon grass and light mineral; crisp, clean and refreshing for the Puglia heat.",
                  price_tier="value")
if n1a:
    PAIR(pr1a, "Orecchiette al pomodoro fresco", "complement", "classic", "main", "Simple fresh tomato pasta and Puglia white; everyday Itria valley lunch tradition.")
    PAIR(pr1a, "Stracciatella con pomodori secchi", "complement", "established", "starter", "Puglia fresh cheese with sun-dried tomatoes; the wine's freshness balances the concentrated tomato.")
    PAIR(pr1a, "Grilled fish from the Adriatic", "complement", "established", "fish_course", "Coastal Puglia fish and the valley's white; a short journey from Adriatic to Itria hills.")
    PAIR(pr1a, "Focaccia barese con olive", "complement", "classic", "casual", "Bari-style thick focaccia with olives; Locorotondo's mineral white and salty olive-bread.")
pr1b, n1b = PROD("Leone de Castris Five Roses Salento Rosato", "wine_still", p1b, r1, "Italy",
                  subcategory="Negroamaro",
                  description="Italy's most historic rosé; pale salmon-pink with strawberry, citrus and Salento herb; dry and medium-bodied — one of Italy's most food-versatile wines.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Grilled octopus alla luciana", "complement", "classic", "starter", "Adriatic octopus and historic Puglia rosé; a southern Italian coastal pairing.")
    PAIR(pr1b, "Parmigiana di melanzane", "complement", "established", "main", "Aubergine parmigiana and dry rosé; tomato-eggplant richness met by rosé freshness.")
    PAIR(pr1b, "Caprese di bufala con basilico", "complement", "classic", "starter", "Buffalo mozzarella and dry Italian rosé; simplicity and elegance in tandem.")
    PAIR(pr1b, "Grilled swordfish with capers and lemon", "complement", "established", "fish_course", "Mediterranean swordfish and historic southern rosé; a generation of Puglia summer lunches.")

# ── REGION 2: Salice Salentino ────────────────────────────────────────────────
print("=== Region 2: Salice Salentino ===")
r2 = R("Salice Salentino", "Italy", "wine",
        designation_type="DOC", designation_name="Salice Salentino DOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Puglia's Salento peninsula DOC producing Negroamaro-based reds of deep colour, dark fruit and Mediterranean warmth; excellent value from Italy's most sun-drenched wine zone.",
        key_producers="Leone de Castris, Candido",
        historical_context="Negroamaro ('black bitter') thrives on the flat Salento peninsula; historically sold in bulk to strengthen northern Italian and French wines; quality revolution led by Leone de Castris and Candido from the 1960s.")
VIN(r2, 2022, "very_good", "stable", "Hot Salento year; Negroamaro shows extraordinary dark fruit concentration.")
VIN(r2, 2021, "good", "stable", "Slightly cooler; Negroamaro more elegant and aromatic than usual.")
VIN(r2, 2020, "very_good", "stable", "Good vintage; classic Salento depth with good structure.")
VIN(r2, 2019, "very_good", "stable", "Warm and generous; dark cherry and bitter chocolate at their best.")
VIN(r2, 2018, "good", "stable", "Solid vintage; consistent and food-friendly Negroamaro.")
p2a = P("Candido", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Salice Salentino estate; Duca d'Aragona is one of the region's iconic reds; pioneer of single-variety Negroamaro quality.",
        reputation_narrative="Alongside Leone de Castris, Candido defined modern Salento wine quality; Duca d'Aragona is a legendary Italian red.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Masseria Li Veli", "winery", r2, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Salento estate owned by the Falvo family (Avignonesi); focused on indigenous varieties including Negroamaro and Verdeca.",
        reputation_narrative="Growing reputation for quality organic Salento wines; earns national critical attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr2a, n2a = PROD("Candido Duca d'Aragona Salice Salentino Riserva", "wine_still", p2a, r2, "Italy",
                  subcategory="Negroamaro-Montepulciano",
                  description="Iconic Salento Riserva; dark plum, dried fig, tobacco, dark chocolate and Mediterranean herbs; full-bodied with impressive structure and ageing potential.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Slow-braised lamb shoulder alla salentina", "complement", "classic", "main", "Salento lamb tradition; the land's most powerful red wine and the land's finest lamb.")
    PAIR(pr2a, "Horse meat ragù (ragù di cavallo)", "complement", "classic", "main", "Puglia's traditional horse meat ragù is the definitive Negroamaro pairing; dark and substantial.")
    PAIR(pr2a, "Aged Canestrato pugliese", "complement", "classic", "cheese", "Puglia's basket-moulded aged cheese with Negroamaro; Southern Italian dairy meets Southern Italian red.")
    PAIR(pr2a, "Wild boar with peppers and olives", "complement", "established", "main", "Mediterranean game stew; Negroamaro's tannin and dark fruit handle the bold flavours.")
pr2b, n2b = PROD("Masseria Li Veli Askos Salice Salentino Rosso", "wine_still", p2b, r2, "Italy",
                  subcategory="Negroamaro",
                  description="Organic Negroamaro with dark cherry, tobacco, Mediterranean herbs and bitter chocolate; medium-full body with coastal freshness.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Orecchiette con carne di cavallo", "complement", "classic", "main", "Puglia horse meat pasta with the Salento's defining red; bold and traditional.")
    PAIR(pr2b, "Grilled Puglia lamb chops with rosemary", "complement", "established", "main", "Salento lamb and organic Negroamaro; Mediterranean herbs bridge both.")
    PAIR(pr2b, "Pizza con salsiccia, olive e pomodoro", "complement", "established", "casual", "Southern Italian pizza with robust Negroamaro; dark fruit and sausage in casual harmony.")
    PAIR(pr2b, "Parmigiana di melanzane alla pugliese", "complement", "classic", "main", "Puglia's eggplant tradition with local red; tomato-cheese richness met by Negroamaro's weight.")

# ── REGION 3: Primitivo di Manduria ──────────────────────────────────────────
print("=== Region 3: Primitivo di Manduria ===")
r3 = R("Primitivo di Manduria", "Italy", "wine",
        designation_type="DOC", designation_name="Primitivo di Manduria DOC",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Puglia's most powerful dry red DOC from the Taranto province; 100% Primitivo (Zinfandel) producing massive, full-bodied wines of dark fruit, alcohol and southern warmth; internationally one of Italy's best-known varieties.",
        key_producers="Pervini, Gianfranco Fino",
        historical_context="Primitivo's California cousin Zinfandel became famous first; Primitivo di Manduria followed as Italy's bold red ambassador globally; Gianfranco Fino's ES elevated the DOC to luxury collector status in the 2010s.")
VIN(r3, 2022, "excellent", "rising", "Exceptional hot vintage for Primitivo; dark fruit concentration extraordinary.")
VIN(r3, 2021, "very_good", "stable", "Good vintage; Primitivo shows excellent balance of fruit and structure.")
VIN(r3, 2020, "very_good", "stable", "Classic expression; rich and warm with good ageing potential.")
VIN(r3, 2019, "very_good", "stable", "Warm vintage; generous and powerful — classic Manduria style.")
VIN(r3, 2018, "good", "stable", "Solid vintage; consistent Primitivo character and good value.")
p3a = P("Gianfranco Fino", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Luxury Primitivo producer elevating old-vine Manduria Primitivo to collector wine status; ES is produced from 90-100 year old alberello vines.",
        reputation_narrative="ES Primitivo di Manduria is Italy's most acclaimed and collectible Puglia wine; consistently scores 95-100.",
        price_positioning="ultra_premium",
        authority_tier=2)
p3b = P("Cantine Due Palme", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Quality Salento cooperative producing exceptional value Primitivo di Manduria across a wide range.",
        reputation_narrative="Most decorated cooperative in Puglia; Primitivo di Manduria Selvarossa earns 90+ consistently.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Gianfranco Fino ES Primitivo di Manduria", "wine_still", p3a, r3, "Italy",
                  subcategory="Primitivo",
                  description="Italy's most celebrated Primitivo; dark chocolate, dried fig, espresso, tobacco and extraordinary concentration from 100-year-old alberello vines; 20+ year ageing horizon.",
                  price_tier="ultra_premium")
if n3a:
    PAIR(pr3a, "Aged dry-aged Chianina bistecca", "complement", "classic", "main", "Italy's greatest beef with Puglia's greatest wine; power meets power in southern Italian luxury.")
    PAIR(pr3a, "Slow-braised wild boar with figs", "complement", "established", "main", "Fig-braised boar echoes ES's fig concentration; a masterful Puglia game dish.")
    PAIR(pr3a, "Aged Pecorino di Fossa con miele", "complement", "classic", "cheese", "Pit-aged cheese intensity and ES's extraordinary concentration; honey bridges the earthiness.")
    PAIR(pr3a, "Dark chocolate with Puglia almonds", "complement", "suggested", "dessert", "70%+ chocolate and old-vine Primitivo; bitter almond and dark fruit in unlikely harmony.")
pr3b, n3b = PROD("Cantine Due Palme Selvarossa Primitivo di Manduria", "wine_still", p3b, r3, "Italy",
                  subcategory="Primitivo",
                  description="Exceptional value Manduria Primitivo; dark cherry, plum, tobacco and warm spice; full-bodied and approachable with good structure.",
                  price_tier="value")
if n3b:
    PAIR(pr3b, "Barbecued lamb ribs with Salento herbs", "complement", "classic", "main", "Southern Italian outdoor lamb cooking with powerful Primitivo; the Salento summer tradition.")
    PAIR(pr3b, "Pasta al forno con polpette", "complement", "established", "casual", "Baked pasta with meatballs; Southern Italian Sunday food with the Puglia's everyday great red.")
    PAIR(pr3b, "Grilled horse steak (cavallo alla brace)", "complement", "classic", "main", "Puglia horse meat tradition and dark Primitivo; both are quintessentially Salentino.")
    PAIR(pr3b, "Pizza al forno con pomodoro e salame", "complement", "classic", "casual", "Pizza and Primitivo; Italy's most popular casual international combination.")

# ── REGION 4: Galatina ────────────────────────────────────────────────────────
print("=== Region 4: Galatina ===")
r4 = R("Galatina", "Italy", "wine",
        designation_type="DOC", designation_name="Galatina DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Southernmost Puglia DOC near Lecce producing Negroamaro reds, Chardonnay and Malvasia Bianca whites from deep red clay soils; one of Italy's most sun-intense wine zones.",
        key_producers="Cantele, Feudi di Guagnano",
        historical_context="Galatina occupies the heel of the Italian boot; ancient Greek and Messapian wine culture; the extreme heat produces Negroamaro of remarkable intensity; quality rising as producers shift from bulk to quality focus.")
VIN(r4, 2022, "very_good", "stable", "Intense heat; concentrated and powerful Negroamaro from this extreme terroir.")
VIN(r4, 2021, "good", "stable", "Marginally cooler; Negroamaro more approachable and aromatic.")
VIN(r4, 2020, "very_good", "stable", "Good vintage; classic Galatina depth and warmth.")
VIN(r4, 2019, "good", "stable", "Standard vintage; reliable southern Italian character.")
VIN(r4, 2018, "good", "stable", "Consistent vintage; honest and food-friendly.")
p4a = P("Cantele", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Family-owned Salento estate producing quality Negroamaro and Primitivo from deep red clay; Teresa Manara Negroamaro is a benchmark female-label wine.",
        reputation_narrative="One of Salento's most respected family wineries; Teresa Manara Negroamaro earns consistent top scores.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Feudi di Guagnano", "winery", r4, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Salento estate focused on indigenous varieties; Verdeca, Negroamaro and Malvasia Nera from the Galatina area.",
        reputation_narrative="Growing reputation for organic Salento wines; earns specialist attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Cantele Teresa Manara Negroamaro Salento", "wine_still", p4a, r4, "Italy",
                  subcategory="Negroamaro",
                  description="Medium-full Negroamaro rosso with dark cherry, tobacco, bitter chocolate and Mediterranean warmth; structured and food-friendly.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Pasta con ragù di agnello e peperoncino", "complement", "classic", "main", "Lamb ragù with chilli and dark Negroamaro; southern Italian heat and richness in harmony.")
    PAIR(pr4a, "Maccheronicini al forno con polpette", "complement", "established", "casual", "Baked pasta and meatballs; accessible Sunday cooking with regional red.")
    PAIR(pr4a, "Braciole (Puglia stuffed meat rolls)", "complement", "classic", "main", "Puglia's stuffed beef rolls in tomato sauce; Negroamaro's tannin and dark fruit handle the richness.")
    PAIR(pr4a, "Grilled horse sausages (salcicce di cavallo)", "complement", "classic", "casual", "Puglia's traditional horse sausage with local dark red; the Salento market tradition.")
pr4b, n4b = PROD("Feudi di Guagnano Negroamaro Rosato Organic Salento", "wine_still", p4b, r4, "Italy",
                  subcategory="Negroamaro",
                  description="Organic pale Negroamaro rosato with strawberry, herb and Salento warmth; dry and medium-bodied.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Grilled orata (sea bream) all'acqua pazza", "complement", "established", "fish_course", "Puglia coastal fish in tomato-herb broth; rosato bridges red and white wine elements.")
    PAIR(pr4b, "Mozzarella di bufala con pomodori", "complement", "classic", "starter", "Buffalo mozzarella and organic southern rosé; summer antipasto tradition.")
    PAIR(pr4b, "Polpette di tonno (tuna patties)", "complement", "established", "starter", "Tuna patties with capers and herbs; dry Negroamaro rosato handles the robust fish.")
    PAIR(pr4b, "Burrata con prosciutto crudo", "complement", "classic", "starter", "Creamy burrata and cured ham met by dry rosato; the Puglia summer aperitivo classic.")

# ── REGION 5: Lamezia ────────────────────────────────────────────────────────
print("=== Region 5: Lamezia ===")
r5 = R("Lamezia", "Italy", "wine",
        designation_type="DOC", designation_name="Lamezia DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Coastal Calabrian DOC in the Lamezia plain; diverse varieties including Nerello Cappuccio, Gaglioppo, Greco Bianco and Chardonnay from sea-level coastal alluvial soils; production dominated by the local cooperative.",
        key_producers="Cantine Lamezia, Cantina Caccamo",
        historical_context="Lamezia is Calabria's second wine zone after Cirò; ancient Greek wine culture in this Tyrrhenian coastal plain; the DOC encompasses Lamezia Terme and its surrounding agricultural hinterland.")
VIN(r5, 2022, "very_good", "stable", "Tyrrhenian coastal influence moderates; fresh whites and full-bodied reds.")
VIN(r5, 2021, "good", "stable", "Balanced vintage; good aromatic expression across red and white varieties.")
VIN(r5, 2020, "very_good", "stable", "Good quality vintage; better than typical for this underappreciated zone.")
VIN(r5, 2019, "good", "stable", "Standard vintage; honest Calabrian coastal character.")
VIN(r5, 2018, "good", "stable", "Consistent vintage; reliable and food-friendly.")
p5a = P("Cantine Lamezia", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Lamezia DOC producer; full range of Calabrian varieties from the coastal plain; benchmark for the appellation.",
        reputation_narrative="The reference producer for Lamezia; honest, authentic wines representing Calabrian coastal terroir.",
        price_positioning="value",
        authority_tier=1)
p5b = P("Cantina Caccamo", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Small Lamezia estate focused on indigenous Calabrian varieties with quality-first approach.",
        reputation_narrative="Emerging artisan voice for the DOC; earns attention from Calabrian wine specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Cantine Lamezia Rosso Calabria Nerello Cappuccio", "wine_still", p5a, r5, "Italy",
                  subcategory="Nerello Cappuccio",
                  description="Coastal Lamezia Nerello Cappuccio; pale ruby with wild cherry, herbs and Tyrrhenian mineral; light to medium body and food-friendly.",
                  price_tier="value")
if n5a:
    PAIR(pr5a, "Pasta al sugo di capra", "complement", "classic", "main", "Goat pasta and Calabrian light red; mountain-and-coast Calabrian tradition.")
    PAIR(pr5a, "Grilled sardines with wild herbs", "complement", "established", "fish_course", "Coastal Calabrian sardine tradition; light red and briny fish — unusual but works here.")
    PAIR(pr5a, "'Nduja and ricotta bruschetta", "complement", "established", "casual", "Spiced Calabrian pork spread on bread; the wine's light tannin balances the 'nduja heat.")
    PAIR(pr5a, "Peperoni cruschi (Calabrian dried peppers)", "complement", "classic", "casual", "Calabria's iconic dried sweet pepper with local red; a traditional Lamezia antipasto.")
pr5b, n5b = PROD("Cantina Caccamo Lamezia Greco Bianco", "wine_still", p5b, r5, "Italy",
                  subcategory="Greco Bianco",
                  description="Coastal Lamezia Greco with citrus, herb and sea mineral; crisp and refreshing with characteristic southern Italian warmth.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Fritto di paranza calabrese", "complement", "classic", "casual", "Calabrian coastal fried fish tradition; Greco's acidity cuts through and refreshes.")
    PAIR(pr5b, "Grilled swordfish alla calabrese", "complement", "established", "fish_course", "Tyrrhenian swordfish and coastal Greco; Mediterranean herb link between wine and fish.")
    PAIR(pr5b, "Pitta 'mpigliata (Calabrian pastry)", "complement", "suggested", "dessert", "Traditional Calabrian honey and nut pastry; Greco's freshness cuts the sweetness pleasantly.")
    PAIR(pr5b, "Pasta con alici e finocchietto", "complement", "classic", "main", "Anchovy and wild fennel pasta; the wine's citrus and herb complement the intense flavours.")

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
