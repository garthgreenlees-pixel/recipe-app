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

# ── 1. MORELLINO DI SCANSANO (Italy) ─────────────────────────────────────────
print("\n=== Morellino di Scansano (Italy) ===")
r = R("Morellino di Scansano", "Italy", "wine",
      designation_type="DOCG",
      designation_name="Morellino di Scansano DOCG",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="A coastal Tuscan DOCG in the Maremma, producing approachable, fruit-forward Sangiovese (locally known as Morellino) with a distinctly Mediterranean character. The warm coastal climate, clay-limestone soils, and lower altitude compared to Chianti produce rounder, more accessible red wines with dark cherry, violets, and Mediterranean scrub. Elevated to DOCG in 2007 as recognition of the region's consistent quality.",
      key_producers="Moris Farms, Rocca di Frassinello, Fattoria Le Pupille, Erik Banti, Cantina Cooperativa di Scansano",
      historical_context="Morellino di Scansano takes its name from the Morellino clone of Sangiovese cultivated in the Scansano hills since Etruscan times. The coastal Maremma, once known as a malaria-ridden swamp, was drained and reclaimed in the postwar period. The region's wine revival accelerated in the 1990s when international investors including Frescobaldi and Antinori recognised its potential.")

VIN(r, 2023, "excellent", "rising", "Warm Maremma coastal season with excellent Sangiovese ripeness; dark fruit and violet expression")
VIN(r, 2022, "very_good", "rising", "Good vintage; round, plummy Morellino with approachable tannins and Mediterranean warmth")
VIN(r, 2021, "good", "stable", "Slightly cooler year producing more elegant, higher-acid style; ideal for food pairing")
VIN(r, 2020, "very_good", "stable", "Hot, dry season; concentrated wines with the coastal scrub character the region is known for")
VIN(r, 2019, "excellent", "rising", "Benchmark vintage for coastal Tuscany; finest Morellino in a generation")

p1 = P("Fattoria Le Pupille", "Italy", r, "winery",
        "One of Morellino di Scansano's most celebrated estates, Fattoria Le Pupille produces the appellation's most internationally acclaimed wine — the Saffredi, a Cabernet-Merlot blend. Their Morellino di Scansano Riserva is a benchmark for the DOCG's best Sangiovese expression.")
prod1, new1 = PROD("Le Pupille Morellino di Scansano Riserva DOCG", "wine_still", p1, r, "Italy",
    subcategory="Sangiovese",
    description="Reserve Morellino di Scansano from coastal Maremma; dark cherry, violets, Mediterranean herbs, and leather with rounded tannins and a warm, sun-drenched finish",
    price_tier="premium")
if new1:
    PAIR(prod1, "Wild boar pappardelle with Rosmarino and Pecorino", "complement", "classic", "main", "Coastal Sangiovese and its dark cherry, herbal character are a natural match for the rich wild boar ragu of Maremma")
    PAIR(prod1, "Grilled T-bone bistecca with rosemary salt", "complement", "established", "main", "Round, generous Morellino handles the richness of grilled beef with ease — a Tuscan classic")
    PAIR(prod1, "Pecorino Toscano semi-stagionato with truffle honey", "bridge", "established", "cheese", "The wine's cherry and herb notes bridge elegantly with semi-aged Pecorino and aromatic truffle honey")
    PAIR(prod1, "Slow-roasted pork loin with sage and garlic", "complement", "established", "main", "Warm, round Morellino pairs beautifully with aromatic roasted pork in the Tuscan tradition")

p2 = P("Moris Farms", "Italy", r, "winery",
        "A historic Maremma estate producing both the benchmark Morellino di Scansano and the famed Avvoltore Maremma Toscana IGT blend. Moris Farms combines traditional Maremma farming with modern winemaking to produce consistently reliable, terroir-honest wines at accessible prices.")
prod2, new2 = PROD("Moris Farms Morellino di Scansano DOCG", "wine_still", p2, r, "Italy",
    subcategory="Sangiovese",
    description="Estate Morellino; juicy, fragrant, and food-friendly with cherry, plum, Mediterranean scrub, and light tannins — one of the DOCG's most consistent and approachable expressions",
    price_tier="mid_range")
if new2:
    PAIR(prod2, "Pizza al pomodoro with fior di latte and basil", "complement", "classic", "main", "Light, cherry-fruited Morellino is the classic Italian red pizza pairing — naturally complementary")
    PAIR(prod2, "Pasta al ragu di cinghiale (wild boar bolognese)", "complement", "classic", "main", "Sangiovese's acidity and dark fruit cut through the richness of wild boar ragu beautifully")
    PAIR(prod2, "Grilled salsiccia sausage with braised lentils", "complement", "established", "main", "The wine's warmth and plum fruit are a natural match for Italian pork sausage with earthy legumes")
    PAIR(prod2, "Bruschetta with chicken liver crostini (crostini neri)", "complement", "established", "starter", "Sangiovese's acidity cuts through the rich liver and amplifies the wine's dark fruit character")

# ── 2. TRENTO DOC (Italy) ────────────────────────────────────────────────────
print("\n=== Trento DOC (Italy) ===")
r2 = R("Trento DOC", "Italy", "wine",
       designation_type="DOC",
       designation_name="Trento DOC Trentodoc",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Italy's premier mountain sparkling wine appellation, produced exclusively by the traditional method (metodo classico) in the Dolomite foothills of Trentino. Chardonnay and Pinot Nero on high-altitude limestone vineyards produce sparkling wines of remarkable freshness, autolytic complexity, and alpine mineral precision. Ferrari Trento dominates internationally but a generation of small estates is raising the bar.",
       key_producers="Ferrari Trento, Methius — Rotari, Letrari, Endrizzi, Maso Martis",
       historical_context="Giulio Ferrari brought Chardonnay cuttings from Champagne to Trentino in 1902, planting the seeds of what would become Italy's finest traditional method sparkling wine. The Ferrari family winery grew to international prominence in the second half of the 20th century. Trento DOC was officially designated in 1993 as the first Italian DOC exclusively for traditional method sparkling wines.")

VIN(r2, 2023, "excellent", "rising", "Cool high-altitude season; exceptional freshness and autolytic potential in Chardonnay-based blends")
VIN(r2, 2022, "very_good", "rising", "Good vintage with fine balance of fruit and acidity for long lees aging")
VIN(r2, 2021, "excellent", "rising", "Standout alpine vintage; wines with exceptional structure and cellaring potential")
VIN(r2, 2020, "very_good", "stable", "Warm alpine season; approachable, fruit-forward style with good depth for aging")
VIN(r2, 2019, "excellent", "rising", "Benchmark vintage; complex base wines ideal for the extended lees aging of prestige cuvees")

p3 = P("Ferrari Trento", "Italy", r2, "winery",
        "Italy's most celebrated producer of traditional method sparkling wine, Ferrari Trento has been crafting Chardonnay-based sparkling wines from Trentino's Dolomite foothills since 1902. Their Giulio Ferrari Riserva del Fondatore is Italy's most iconic sparkling wine, consistently competing with top Champagne on the world stage.")
prod3, new3 = PROD("Ferrari Trento Brut Trentodoc", "wine_sparkling", p3, r2, "Italy",
    subcategory="Chardonnay",
    description="Italy's benchmark traditional method sparkling wine; Chardonnay-dominant with fine, persistent bubbles, green apple, toasted brioche, and alpine mineral — the national symbol of Italian celebrations",
    price_tier="mid_range")
if new3:
    PAIR(prod3, "Risotto allo zafferano (saffron risotto) with Parmesan", "complement", "classic", "main", "Fine Italian sparkling and creamy saffron risotto is one of the country's most elegant aperitivo-to-table pairings")
    PAIR(prod3, "Tempura langoustines with saffron aioli", "complement", "established", "starter", "The wine's fine bubbles and citrus mineral cut through fried batter and complement sweet crustacean")
    PAIR(prod3, "Trentino speck with horseradish cream and sourdough", "complement", "classic", "starter", "Local alpine cured ham and its smoky richness is the traditional Trentino pairing for Trentodoc")
    PAIR(prod3, "Sushi and sashimi assortment", "cleanse", "established", "main", "Fine Italian sparkling's acidity and bubbles cleanse and refresh between pieces of Japanese seafood")

p4 = P("Letrari", "Italy", r2, "winery",
        "A prestigious small estate in Trentino producing traditional method sparkling wines of exceptional quality and character from high-altitude vineyards. The Letrari family's Riserva Dosaggio Zero is considered one of Italy's finest small-production Trentodoc wines, combining alpine precision with remarkable depth.")
prod4, new4 = PROD("Letrari Riserva Dosaggio Zero Trentodoc", "wine_sparkling", p4, r2, "Italy",
    subcategory="Chardonnay Pinot Nero",
    description="Zero-dosage reserve Trentodoc; bone-dry with laser-precise Alpine mineral, green apple, lemon zest, and fine toasty autolytic complexity from extended lees aging",
    price_tier="premium")
if new4:
    PAIR(prod4, "Fresh oysters with lemon and sea salt", "complement", "classic", "starter", "Zero-dosage sparkling's bone-dry mineral precision is the ultimate companion for fresh bivalves")
    PAIR(prod4, "Caviar with blinis and creme fraiche", "complement", "classic", "starter", "Fine, dry Italian sparkling provides the perfect foil for the salt, fat, and brine of caviar")
    PAIR(prod4, "Grilled branzino with olive oil and capers", "complement", "established", "main", "Alpine mineral and zero dosage dryness frame delicate sea bass with Mediterranean garnish perfectly")
    PAIR(prod4, "Aged Trentingrana cheese with sourdough", "complement", "suggested", "cheese", "The wine's toasty autolytic notes and mineral precision bridge with nutty aged mountain cheese")

# ── 3. NEUSIEDLERSEE (Austria) ───────────────────────────────────────────────
print("\n=== Neusiedlersee (Austria) ===")
r3 = R("Neusiedlersee", "Austria", "wine",
       designation_type="DAC",
       designation_name="Neusiedlersee DAC",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Austria's most internationally celebrated wine region for one reason: the world's greatest sweet wines. The shallow Neusiedlersee lake on the Hungarian border creates a unique microclimate of mist and humidity that promotes Botrytis cinerea (noble rot) with extraordinary reliability. Alois Kracher and his Neue Welt estate transformed global perception of Austrian sweet wine in the 1990s. Also produces fine dry Zweigelt.",
       key_producers="Alois Kracher, Weinlaubenhof Kracher, Hans Tschida — Angerhof, Helmut Lang, Paul Achs",
       historical_context="The Neusiedlersee region's wine history dates to the Roman era, but its modern international reputation was built almost entirely by Alois Kracher (1959-2007), whose Trockenbeerenauslese wines achieved 100-point ratings and global acclaim. Kracher's success transformed Austrian sweet wine from a historical curiosity into an international benchmark, with his TBA Cuvee Beerenauslese labels commanding extraordinary prices worldwide.")

VIN(r3, 2023, "very_good", "stable", "Reliable Botrytis development from lake mist; excellent Beerenauslese and TBA quality")
VIN(r3, 2022, "excellent", "rising", "Exceptional noble rot season; outstanding concentration in both sweet and dry wines")
VIN(r3, 2021, "good", "stable", "Good vintage; moderate Botrytis producing elegant, not over-concentrated sweet wines")
VIN(r3, 2020, "very_good", "stable", "Warm season with excellent late-harvest concentration; fine Zweigelt red alongside superb stickies")
VIN(r3, 2019, "exceptional", "rising", "One of the great Neusiedlersee vintages; TBA of extraordinary concentration and complexity")

p5 = P("Weinlaubenhof Kracher", "Austria", r3, "winery",
        "The world's most celebrated producer of Trockenbeerenauslese and Beerenauslese sweet wines. Founded by Alois Kracher and continued by his son Gerhard, the estate produces Nouvelle Vague (new oak) and Zwischen den Seen (stainless steel) labeled TBA wines of legendary concentration and longevity.")
prod5, new5 = PROD("Kracher Grande Cuvee Trockenbeerenauslese Neusiedlersee", "wine_dessert", p5, r3, "Austria",
    subcategory="TBA blend",
    description="Austria's most iconic sweet wine; extraordinary Botrytis-affected TBA from the Neusiedlersee lakeside — apricot jam, saffron, honey, mango, and exotic spice of breathtaking concentration and infinite complexity",
    price_tier="ultra_premium")
if new5:
    PAIR(prod5, "Fourme d'Ambert or Gorgonzola naturale blue cheese", "contrast", "classic", "cheese", "One of the world's great contrasts: luscious, honeyed TBA against pungent, salty blue cheese — timeless elegance")
    PAIR(prod5, "Foie gras torchon with sauternes gelee and brioche", "complement", "classic", "starter", "The noble sweet wine and foie gras pairing elevated to Austrian heights — saffron and apricot match the duck liver richness")
    PAIR(prod5, "Tarte tatin with creme fraiche", "complement", "established", "dessert", "The wine's caramelised apricot and honey notes create seamless harmony with warm apple tarte and cream")
    PAIR(prod5, "Aged Parmigiano-Reggiano with walnut and truffle honey", "complement", "adventurous", "cheese", "Crystalline aged Parmesan with sweet truffle honey creates an extraordinary counterpoint to the wine's exotic richness")

p6 = P("Hans Tschida Angerhof", "Austria", r3, "winery",
        "A renowned small Neusiedlersee estate producing exceptional Beerenauslese and Trockenbeerenauslese wines alongside fine dry Zweigelt. Tschida's sweet wines are celebrated for their clarity, precision, and extraordinary ageing potential, making them among Austria's most sought-after collectible bottles.")
prod6, new6 = PROD("Hans Tschida Angerhof Beerenauslese Neusiedlersee", "wine_dessert", p6, r3, "Austria",
    subcategory="Welschriesling",
    description="Benchmark Neusiedlersee Beerenauslese from Welschriesling; golden, honeyed, and complex with dried apricot, orange marmalade, beeswax, and a clean, bright acidity balancing the sweetness",
    price_tier="premium")
if new6:
    PAIR(prod6, "Apricot Linzer torte with Schlagobers cream", "complement", "classic", "dessert", "Apricot-dominated Beerenauslese mirrors the fruit and pastry of Austria's most iconic cake")
    PAIR(prod6, "Ricotta cheesecake with lemon curd and berries", "complement", "established", "dessert", "The wine's honey-orange complexity provides a luscious backdrop for fresh ricotta and tart citrus")
    PAIR(prod6, "Stilton or Roquefort with walnut bread", "contrast", "classic", "cheese", "Classic sweet wine and blue cheese pairing: the wine's sweetness cuts through saltiness magnificently")
    PAIR(prod6, "Grilled peaches with mascarpone and pistachios", "complement", "suggested", "dessert", "The wine's apricot-honey character resonates beautifully with caramelised stone fruit and rich cream cheese")

# ── 4. MUSCAT DE BEAUMES-DE-VENISE (France) ──────────────────────────────────
print("\n=== Muscat de Beaumes-de-Venise (France) ===")
r4 = R("Muscat de Beaumes-de-Venise", "France", "wine",
       designation_type="AOC",
       designation_name="Muscat de Beaumes-de-Venise AOC",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="The Rhone Valley's most celebrated fortified wine appellation, producing luscious, golden Muscat Blanc a Petits Grains vins doux naturels (naturally sweet wines, lightly fortified) from steep limestone and clay-limestone terraces below the Dentelles de Montmirail mountains. The wines are France's most aromatic and food-versatile sweet whites — fresh, floral, and irresistibly honeyed without the heaviness of full fortification.",
       key_producers="Domaine de Durban, Domaine de Fenouillet, Domaine des Bernardins, Beaumes-de-Venise Cooperative",
       historical_context="Muscat de Beaumes-de-Venise was one of France's first AOCs (1945), reflecting the region's pre-existing reputation for its naturally sweet Muscat. The wine enjoyed a golden era in 1970s-80s Britain, where it became fashionable as an aperitif and dessert wine. Modern production has refined the style toward greater freshness and lower alcohol, reviving international interest.")

VIN(r4, 2023, "excellent", "stable", "Warm Rhone summer with good acidity retention; exceptional aromatic intensity and freshness in Muscat")
VIN(r4, 2022, "very_good", "stable", "Good vintage; typical floral and honeyed character with pleasing freshness")
VIN(r4, 2021, "good", "stable", "Cooler year; wines show more citrus-bright character than usual, with elegant restraint")
VIN(r4, 2020, "very_good", "stable", "Hot season; rich, concentrated Muscat with the classic lychee and orange blossom notes")
VIN(r4, 2019, "excellent", "stable", "Benchmark vintage for the appellation; finest Muscat in recent years")

p7 = P("Domaine de Durban", "France", r4, "winery",
        "The leading private estate of Muscat de Beaumes-de-Venise, Domaine de Durban produces wines of exceptional aromatic purity and freshness from steep limestone terraces below the Dentelles de Montmirail. Their Muscat is consistently one of the finest examples of the appellation, retaining vibrant freshness alongside honeyed complexity.")
prod7, new7 = PROD("Domaine de Durban Muscat de Beaumes-de-Venise AOC", "wine_fortified", p7, r4, "France",
    subcategory="Muscat Blanc a Petits Grains",
    description="Benchmark Beaumes-de-Venise Muscat; golden, floral, and irresistible with orange blossom, lychee, dried apricot, and honey — one of France's most food-versatile sweet wines",
    price_tier="mid_range")
if new7:
    PAIR(prod7, "Fresh melon with Bayonne ham", "complement", "classic", "starter", "The iconic Provencal opener: chilled Muscat de Beaumes-de-Venise with ripe melon and salty cured ham is one of France's great summer pleasures")
    PAIR(prod7, "Tarte aux abricots with creme patissiere", "complement", "classic", "dessert", "Apricot and honey in the wine create perfect harmony with a classic French apricot tart")
    PAIR(prod7, "Roquefort or Saint-Agur blue cheese with walnuts", "contrast", "established", "cheese", "The wine's sweetness and floral freshness provide brilliant contrast to pungent, salty blue cheese")
    PAIR(prod7, "Mango and passion fruit pavlova", "complement", "established", "dessert", "Tropical floral Muscat and lychee-passion fruit dessert create a seamlessly aromatic pairing")

p8 = P("Domaine des Bernardins", "France", r4, "winery",
        "A respected family estate in Beaumes-de-Venise producing traditional Muscat alongside fine dry Grenache-based reds. Their Muscat is noted for its orange peel and spice complexity alongside the typical floral character, offering a slightly richer style than the Domaine de Durban model.")
prod8, new8 = PROD("Domaine des Bernardins Muscat de Beaumes-de-Venise AOC", "wine_fortified", p8, r4, "France",
    subcategory="Muscat Blanc a Petits Grains",
    description="Richer, spiced interpretation of Beaumes-de-Venise Muscat; orange peel, dried apricot, ginger, and honey with good freshness cutting through the sweetness",
    price_tier="mid_range")
if new8:
    PAIR(prod8, "Moroccan bastilla (pigeon pastilla with almonds and cinnamon)", "complement", "adventurous", "main", "The wine's orange, spice, and honey character creates a fascinating resonance with the sweet-savoury spiced pigeon pastry")
    PAIR(prod8, "Christmas stollen with marzipan and candied peel", "complement", "established", "dessert", "The wine's dried orange peel and spice notes mirror the flavours of the German Christmas bread")
    PAIR(prod8, "Chevre chaud salad with honey and walnuts", "complement", "established", "starter", "Floral, honeyed Muscat pairs naturally with warm goat's cheese, honey, and bitter greens")
    PAIR(prod8, "Pain d'epices with foie gras and fig jam", "complement", "classic", "starter", "Spiced Muscat and the sweetness of pain d'epices complement foie gras in an Alsace-Rhone inspired pairing")

# ── 5. SOMONTANO (Spain) ─────────────────────────────────────────────────────
print("\n=== Somontano (Spain) ===")
r5 = R("Somontano", "Spain", "wine",
       designation_type="DO",
       designation_name="DO Somontano",
       reputation_tier="respected",
       quality_trajectory="established",
       description="Aragon's most internationally recognised wine region, at the foot of the Pyrenean foothills between Huesca and Barbastro. Unlike most Spanish DOs, Somontano permits a wide range of international varieties (Cabernet Sauvignon, Merlot, Syrah, Chardonnay) alongside indigenous Moristel and Parraleta. The result is a diverse, modern-oriented wine region producing some of Spain's most approachable and elegant wines.",
       key_producers="Vinas del Vero, Bodega Enate, Bodegas Olvena, Blecua",
       historical_context="Somontano was awarded DO status in 1984, one of the first Spanish regions to invite international variety investment. The region was developed largely through cooperative production before private investment transformed its quality profile in the 1990s. Vinas del Vero and Enate became internationally recognised names that put Somontano on the global wine map.")

VIN(r5, 2023, "very_good", "stable", "Warm Pyrenean foothills season; good ripeness across all varieties planted in the DO")
VIN(r5, 2022, "excellent", "stable", "Outstanding vintage for both international and indigenous varieties; exceptional structure and balance")
VIN(r5, 2021, "good", "stable", "Slightly cooler year; wines show more elegance and freshness than power")
VIN(r5, 2020, "very_good", "stable", "Classic Somontano vintage; reliable quality across the full range from entry to reserve level")
VIN(r5, 2019, "excellent", "rising", "Benchmark vintage for the region; finest wines in recent memory across all varietals")

p9 = P("Bodega Enate", "Spain", r5, "winery",
        "Somontano's most artistically celebrated estate, Enate commissions a new label artwork from a contemporary Spanish artist for each vintage. Beyond aesthetics, the wines are among the region's finest — their Tempranillo-Cabernet and Chardonnay fermentado en barrica are Aragon's most internationally recognised labels.")
prod9, new9 = PROD("Bodega Enate Reserva Somontano DO", "wine_still", p9, r5, "Spain",
    subcategory="Tempranillo Cabernet Sauvignon",
    description="Somontano's flagship red blend; dark cherry, blackcurrant, cedar, and vanilla with structured tannins and a long, well-integrated finish — elegant Spanish mountain wine with international appeal",
    price_tier="premium")
if new9:
    PAIR(prod9, "Roasted lamb ribs with garlic and Aragonese herbs", "complement", "classic", "main", "The structured Tempranillo-Cabernet blend mirrors the region's classic grilled lamb pairing naturally")
    PAIR(prod9, "Morcilla de Burgos with caramelised onion", "complement", "established", "starter", "The wine's dark fruit and cedar notes pair naturally with the spiced blood sausage of Aragon")
    PAIR(prod9, "Slow-cooked ternasco (Aragonese lamb stew) with vegetables", "complement", "classic", "main", "The regional wine and the regional lamb stew: Somontano and ternasco Aragones are inseparable")
    PAIR(prod9, "Aged Manchego with quince paste", "bridge", "established", "cheese", "The wine's structured dark fruit and oak bridge elegantly with aged Spanish cheese and sweet membrillo")

p10 = P("Vinas del Vero", "Spain", r5, "winery",
         "One of Somontano's largest and most exported producers, Vinas del Vero makes a comprehensive range of varietally-focused wines including benchmark Chardonnay, Gewurztraminer, and Garnacha. Their wines offer consistent quality and remarkable value, representing some of Aragon's most internationally competitive bottles.")
prod10, new10 = PROD("Vinas del Vero Gewurztraminer Somontano DO", "wine_still", p10, r5, "Spain",
    subcategory="Gewurztraminer",
    description="One of Spain's finest Gewurztraminers; grown at altitude in the Pyrenean foothills with intense rose petal, lychee, and ginger aromatics — fresh and moderately off-dry with a lingering exotic finish",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Aragon-style roast lamb with saffron and peppers", "complement", "established", "main", "The wine's exotic spice and aromatic character complement the warm saffron and pepper notes of the regional preparation")
    PAIR(prod10, "Thai green papaya salad with prawns", "complement", "classic", "starter", "Gewurztraminer's aromatic spice and slight sweetness are the classic match for vibrant Asian salad and chilli heat")
    PAIR(prod10, "Aged Torta del Casar cheese (runny sheep's cheese)", "complement", "established", "cheese", "Powerfully aromatic Gewurztraminer handles the intense pungency of runny aged Spanish sheep's cheese")
    PAIR(prod10, "Pulled pork baos with hoisin and pickled cucumber", "bridge", "suggested", "main", "Lychee and rose aromatics bridge Asian-influenced slow-cooked pork with sweet hoisin and sharp pickle")

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
