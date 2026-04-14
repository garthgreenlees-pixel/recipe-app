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

# ── 1. VALTELLINA (Italy) ─────────────────────────────────────────────────────
print("\n=== Valtellina (Italy) ===")
r = R("Valtellina", "Italy", "wine",
      designation_type="DOC/DOCG",
      designation_name="Valtellina Superiore DOCG / Sforzato di Valtellina DOCG",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="One of Italy's most dramatic and underrated wine regions, where Nebbiolo (locally called Chiavennasca) clings to near-vertical granite terraces above the Adda River in the Alps of Lombardy. Valtellina Superiore DOCG includes four subzones — Sassella, Grumello, Inferno, and Valgella — each producing a distinct character from the ancient hand-tended terraces. Sforzato di Valtellina DOCG (from semi-dried Nebbiolo) is Italy's most powerful Nebbiolo expression.",
      key_producers="Ar.Pe.Pe., Nino Negri, Conti Sertoli Salis, Aldo Rainoldi, Mamete Prevostini",
      historical_context="Valtellina's terraced viticulture dates back 2,000 years. The impossibly steep granite slopes were carved into terraces (ronchi) by generations of farmers, with the entire enterprise sustained by mule paths and intense manual labour. The Sforzato wine style — drying Chiavennasca grapes before pressing — was developed to concentrate the thin-skinned mountain grape's flavours and was awarded DOCG status in 2003. Valtellina was historically part of the Swiss Confederation before ceding to Lombardy.")

VIN(r, 2023, "excellent", "rising", "Outstanding Alpine growing season; Chiavennasca of exceptional concentration and granite-mineral character")
VIN(r, 2022, "very_good", "rising", "Good vintage; elegant, fragrant Valtellina Superiore with fine tannins and aging potential")
VIN(r, 2021, "good", "stable", "Cool Alpine year; wines of unusual freshness; Sforzato showed more restraint than usual")
VIN(r, 2020, "excellent", "rising", "Benchmark vintage; finest Valtellina Superiore and Sforzato in a generation")
VIN(r, 2019, "very_good", "stable", "Classic vintage; reliable quality across all four Superiore subzones")

p1 = P("Ar.Pe.Pe.", "Italy", r, "winery",
        "Articolo Pelizzatti Perego — one of Valtellina's most revered producers, farming steep granite terraces biodynamically without compromise. Their Sassella, Grumello, and Inferno single-vineyard Valtellina Superiore wines are considered the pinnacle of the appellation's traditional style, with extraordinary mineral precision and aging potential.")
prod1, new1 = PROD("Ar.Pe.Pe. Sassella Riserva Rocce Rosse Valtellina Superiore DOCG", "wine_still", p1, r, "Italy",
    subcategory="Chiavennasca",
    description="The benchmark Valtellina Superiore Riserva; Chiavennasca from ancient Sassella terraces — pale ruby, deeply perfumed with dried rose, cherry, iron mineral, and granite dust; remarkably long-lived and Burgundy-like",
    price_tier="premium")
if new1:
    PAIR(prod1, "Pizzoccheri della Valtellina (buckwheat pasta with Bitto cheese and chard)", "complement", "classic", "main", "The regional wine and the regional pasta: Alpine Nebbiolo and the buckwheat-cheese-potato combination of Valtellina is one of Italy's most perfectly matched regional pairings")
    PAIR(prod1, "Slow-braised lamb shoulder with polenta taragna", "complement", "classic", "main", "Mineral, elegant Valtellina Nebbiolo with the earthy richness of braised Alpine lamb and polenta")
    PAIR(prod1, "Bresaola della Valtellina with olive oil, lemon, and arugula", "complement", "classic", "starter", "The region's iconic cured beef and its own mountain Nebbiolo is the most natural of Alpine Italian pairings")
    PAIR(prod1, "Aged Bitto Storico cheese with local honey and walnuts", "bridge", "established", "cheese", "Mineral, perfumed Valtellina Nebbiolo bridges with the Alpine cheese that has been produced in this valley since Roman times")

p2 = P("Nino Negri", "Italy", r, "winery",
        "Valtellina's most internationally distributed estate and the region's greatest ambassador on the world stage. Nino Negri's 5 Stelle Sforzato and Sassorosso Valtellina Superiore wines have achieved widespread critical acclaim and have introduced the region's unique Alpine Nebbiolo character to wine lovers across the globe.")
prod2, new2 = PROD("Nino Negri 5 Stelle Sforzato di Valtellina DOCG", "wine_still", p2, r, "Italy",
    subcategory="Chiavennasca",
    description="Italy's most celebrated Sforzato; passito-style Nebbiolo from semi-dried Alpine grapes — concentrated but still perfumed with dark cherry, dried tobacco, granite mineral, and the characteristic dried-fruit richness of the Sforzato style",
    price_tier="premium")
if new2:
    PAIR(prod2, "Venison saddle with juniper, cranberry, and potato gnocchi", "complement", "established", "main", "Concentrated Alpine Sforzato handles the gamey richness and tart cranberry of venison with its dried fruit and granite depth")
    PAIR(prod2, "Slow-roasted wild boar with chestnuts and rosemary", "complement", "classic", "main", "Powerful dried-grape Nebbiolo with Alpine wild boar and chestnuts — a deeply mountain Italian combination")
    PAIR(prod2, "Aged Castelmagno cheese with pear mostarda", "bridge", "established", "cheese", "The wine's dried fruit and mineral complexity bridges with Cuneo's unique crumbly mountain cheese and pungent mostarda")
    PAIR(prod2, "Dark chocolate and chestnut cake", "complement", "suggested", "dessert", "The wine's dried cherry and dark cocoa notes create an unexpected but beautiful match with chestnut-chocolate desserts")

# ── 2. VERDICCHIO DEI CASTELLI DI JESI (Italy) ───────────────────────────────
print("\n=== Verdicchio dei Castelli di Jesi (Italy) ===")
r2 = R("Verdicchio dei Castelli di Jesi", "Italy", "wine",
       designation_type="DOC/DOCG",
       designation_name="Verdicchio dei Castelli di Jesi DOC / Classico Superiore DOC",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The Marche region's greatest and most internationally recognised white wine, produced from the Verdicchio grape in the Castelli di Jesi hills near the Adriatic. Verdicchio is one of Italy's oldest and most distinctive indigenous whites — intensely mineral, bitter-almond finishing, and built for aging. The amphora-shaped bottle was a 1950s marketing gimmick that became iconic, but the wine inside is genuinely great: one of Italy's most age-worthy and food-versatile whites.",
       key_producers="Umani Ronchi, Bucci, Garofoli, Monte Schiavo, La Staffa",
       historical_context="Verdicchio's name ('little green one') refers to the grape's greenish tint at harvest. The DOC was established in 1968, but Verdicchio's quality reputation was long overshadowed by its distinctive amphora bottle — introduced in 1955 — which attracted mockery before the wine's quality was taken seriously. Bucci's Villa Bucci and Umani Ronchi's Casal di Serra have since demonstrated that Verdicchio can age for decades and develop extraordinary complexity.")

VIN(r2, 2023, "excellent", "rising", "Outstanding Adriatic Marche season; Verdicchio of exceptional mineral precision and bitter-almond complexity")
VIN(r2, 2022, "very_good", "rising", "Good vintage; wines of characteristic freshness and the bitter-mineral backbone ideal for aging")
VIN(r2, 2021, "good", "stable", "Cooler year; wines of unusual aromatics and high acid — best examples for cellaring")
VIN(r2, 2020, "very_good", "stable", "Hot summer; rich, concentrated Verdicchio with the typical apple and almond at full ripeness")
VIN(r2, 2019, "excellent", "rising", "Benchmark Marche vintage; finest Verdicchio in recent memory across all producers")

p3 = P("Umani Ronchi", "Italy", r2, "winery",
        "The Marche's most internationally celebrated producer and the estate most responsible for putting Verdicchio on the global wine map. Umani Ronchi's Casal di Serra remains the benchmark single-vineyard Verdicchio, while the Vecchie Vigne old-vine version has achieved critical scores that place it in Italy's white wine pantheon.")
prod3, new3 = PROD("Umani Ronchi Casal di Serra Vecchie Vigne Verdicchio dei Castelli di Jesi DOC", "wine_still", p3, r2, "Italy",
    subcategory="Verdicchio",
    description="Benchmark old-vine Verdicchio from Casal di Serra; complex, mineral, and textured with green apple, white almond, citrus pith, and a long saline-bitter finish that develops extraordinary complexity with 5-10 years' age",
    price_tier="premium")
if new3:
    PAIR(prod3, "Vincisgrassi (Marche-style baked pasta with offal ragu)", "complement", "classic", "main", "The regional wine and the regional dish: mineral Verdicchio cuts through the rich, slow-cooked Marche pasta with organ meat sauce")
    PAIR(prod3, "Grilled scampi with lemon and Adriatic herbs", "complement", "classic", "main", "Verdicchio's bitter mineral and lemon-citrus are the definitive accompaniment for Adriatic grilled crustaceans")
    PAIR(prod3, "Brodetto alla vastese (Marche Adriatic fish stew)", "complement", "classic", "main", "The wine's saline mineral precision frames the complex, multi-fish Adriatic stew of the Marche coast")
    PAIR(prod3, "Aged Pecorino dei Monti Sibillini with local honey", "bridge", "suggested", "cheese", "The wine's bitter almond and mineral complexity bridges with the sharpness of aged Marche sheep's cheese")

p4 = P("Bucci", "Italy", r2, "winery",
        "The prestige producer of Verdicchio dei Castelli di Jesi, Ampelio Bucci farms his historic estate with extraordinary care to produce two benchmark wines: the Villa Bucci Riserva — one of Italy's most age-worthy white wines — and the standard Bucci Verdicchio. Both demonstrate the grape's capacity for complexity, aging, and genuine terroir expression.")
prod4, new4 = PROD("Bucci Villa Bucci Riserva Verdicchio dei Castelli di Jesi DOC", "wine_still", p4, r2, "Italy",
    subcategory="Verdicchio",
    description="Italy's most age-worthy indigenous white wine; old-vine Verdicchio Riserva — intensely mineral, almond, and complex with a saline backbone that carries this wine through 15-20 years of bottle development",
    price_tier="premium")
if new4:
    PAIR(prod4, "Roasted turbot with capers, lemon, and Verdicchio sauce", "complement", "classic", "main", "The wine cooks into the sauce and is served alongside — a self-referential Marche pairing of elegant simplicity")
    PAIR(prod4, "Raw Adriatic red shrimp with olive oil, lemon, and sea salt", "complement", "classic", "starter", "The wine's saline mineral and citrus precision are the ideal frame for raw Adriatic crustaceans — a perfect Italian coastal pairing")
    PAIR(prod4, "Truffled scrambled eggs with sourdough", "complement", "established", "starter", "Mineral, complex Verdicchio Riserva with the earthy luxury of truffled eggs — surprising and beautiful")
    PAIR(prod4, "Mozzarella di Bufala with anchovies and Taggiasche olives", "complement", "established", "starter", "The wine's bitter almond and saline character resonate with the freshness of buffalo mozzarella and the brine of fine cured anchovies")

# ── 3. OAKVILLE AVA (USA) ────────────────────────────────────────────────────
print("\n=== Oakville AVA (USA) ===")
r3 = R("Oakville AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Oakville AVA",
       reputation_tier="iconic",
       quality_trajectory="established",
       description="Napa Valley's most prestigious sub-AVA and the spiritual heart of American fine wine. The Oakville benchland produces Cabernet Sauvignon of extraordinary power, complexity, and aging potential from its deep, well-drained gravelly loam soils. Home to Napa's most celebrated estates: Harlan, Screaming Eagle, Opus One, Robert Mondavi To Kalon, Far Niente, and Rudd. The combination of warm days, cool nights, and exceptional drainage creates conditions for Cabernet of Bordeaux First Growth comparison.",
       key_producers="Opus One, Harlan Estate, Far Niente, Robert Mondavi Winery, Rudd Estate, Dalla Valle",
       historical_context="Oakville's wine history begins with the founding of Robert Mondavi Winery in 1966 on the To Kalon Vineyard — the most historically significant site in American wine. The AVA was established in 1993. Screaming Eagle's 1992 vintage sold at auction for $500,000 a case, establishing Oakville as the home of America's most coveted wines. Opus One — founded jointly by Robert Mondavi and Baron Philippe de Rothschild — has been the region's symbolic collaboration between New and Old World since 1980.")

VIN(r3, 2023, "excellent", "rising", "Outstanding Napa growing season; Oakville Cabernet of exceptional concentration and structural precision")
VIN(r3, 2022, "very_good", "rising", "Good vintage; benchmark Oakville depth and structure with good aging potential")
VIN(r3, 2021, "good", "stable", "Smoke-affected harvest required careful selection; top estates produced wines of characteristic power")
VIN(r3, 2020, "good", "stable", "Challenging wildfire year; best Oakville sites showed remarkable resilience")
VIN(r3, 2019, "exceptional", "rising", "Benchmark Napa vintage; greatest Oakville Cabernet in a generation across the appellation")

p5 = P("Opus One Winery", "USA", r3, "winery",
        "The most iconic joint venture in world wine, Opus One was created in 1980 by Robert Mondavi and Baron Philippe de Rothschild as the definitive statement that California could produce wine of Bordeaux First Growth quality. Their Oakville Cabernet-dominant blend consistently ranks among America's finest and most internationally recognisable wines.")
prod5, new5 = PROD("Opus One Napa Valley Oakville", "wine_still", p5, r3, "USA",
    subcategory="Cabernet Sauvignon blend",
    description="The iconic Franco-Californian collaboration; Oakville Cabernet Sauvignon-dominant blend — dark cassis, graphite, cedar, and violets with the legendary Napa concentration and the structural elegance of Bordeaux",
    price_tier="ultra_premium")
if new5:
    PAIR(prod5, "Wagyu beef tenderloin with black truffle sauce and potato gratin", "complement", "classic", "main", "The wine's graphite, cassis, and cedar complexity is the ideal accompaniment for A5 Wagyu with truffle — the ultimate luxury pairing")
    PAIR(prod5, "Dry-aged bone-in ribeye with Bordelaise and bone marrow", "complement", "classic", "main", "Opus One and dry-aged prime beef is the Napa Valley's most celebrated fine dining pairing — powerful, structured, and magnificent")
    PAIR(prod5, "Aged Comte 24-month with black truffle paste", "bridge", "classic", "cheese", "The wine's graphite and cedar notes bridge with the nuttiness of aged Comte and the earthiness of black truffle")
    PAIR(prod5, "Roasted squab with cherry-Cabernet reduction and foie gras", "complement", "classic", "main", "Rich, structured Oakville Cabernet handles the game richness of squab with foie gras in a classic Napa wine country preparation")

p6 = P("Far Niente Winery", "USA", r3, "winery",
        "One of Oakville's most historic and beautifully maintained estates, Far Niente has produced benchmark Napa Cabernet and Chardonnay since its restoration in 1979. The estate's Oakville Cabernet Sauvignon is considered one of the appellation's finest for its consistency, elegance, and remarkable aging potential.")
prod6, new6 = PROD("Far Niente Estate Cabernet Sauvignon Oakville Napa Valley", "wine_still", p6, r3, "USA",
    subcategory="Cabernet Sauvignon",
    description="Benchmark estate Oakville Cabernet Sauvignon; concentrated and structured with dark blackcurrant, graphite, tobacco, and well-integrated oak — one of Napa's most reliable and age-worthy fine wines",
    price_tier="ultra_premium")
if new6:
    PAIR(prod6, "Prime filet mignon with herb butter and roasted garlic jus", "complement", "classic", "main", "Classic Napa Cabernet and filet mignon — the combination that built California's fine dining reputation")
    PAIR(prod6, "Rack of Colorado lamb with rosemary and Dijon crust", "complement", "classic", "main", "Structured Oakville Cabernet with herb-crusted rack of lamb is the quintessential American wine country preparation")
    PAIR(prod6, "Wild mushroom and aged Gruyere tartlet", "complement", "established", "starter", "The wine's cedar and graphite notes resonate with the earthy richness of wild mushroom and aged cheese")
    PAIR(prod6, "Aged Vermont white cheddar with quince paste", "bridge", "suggested", "cheese", "The wine's cassis and cedar bridge naturally with sharp aged American cheddar and sweet quince preserves")

# ── 4. BIO-BIO VALLEY (Chile) ────────────────────────────────────────────────
print("\n=== Bio-Bio Valley (Chile) ===")
r4 = R("Bio-Bio Valley", "Chile", "wine",
       designation_type="DO",
       designation_name="DO Bio-Bio Valley",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="Chile's southernmost and coolest major wine valley, in the Region de Bio-Bio. Bio-Bio is the frontier of Chilean viticulture — where the continental climate gives way to maritime conditions from the Pacific and where temperatures are cool enough for Pinot Noir, Riesling, Gewurztraminer, and Muscat. The indigenous Pais grape (Mission) survives here in old-vine plantations dating to the 17th century Spanish missions. A new generation of natural wine producers is discovering the valley's potential.",
       key_producers="Clos des Fous, De Martino, Cacique Maravilla, Meli, Garage Wine Co",
       historical_context="Bio-Bio was one of Chile's earliest winemaking regions, with Spanish missionaries planting Pais vines in the 17th century. The region fell out of fashion as the industry focused on the warmer valleys of Maipo and Colchagua in the 20th century. The natural wine movement's rediscovery of old-vine Pais in the 2010s transformed Bio-Bio's profile, with producers like De Martino and Clos des Fous showcasing the valley's potential for cool-climate, organic production.")

VIN(r4, 2023, "very_good", "rising", "Cool Pacific-influenced season; exceptional Pais and Muscat freshness; emerging quality from the valley")
VIN(r4, 2022, "excellent", "rising", "Outstanding cool vintage for Bio-Bio; finest old-vine Pais and Riesling in recent memory")
VIN(r4, 2021, "good", "stable", "Good vintage with reliable cool-climate character; natural wine producers particularly rewarded")
VIN(r4, 2020, "very_good", "rising", "Long, cool season; exceptional freshness in all varietals planted in the valley")
VIN(r4, 2019, "excellent", "rising", "Benchmark Bio-Bio vintage; increasing critical attention as the valley's quality becomes undeniable")

p7 = P("De Martino", "Chile", r4, "winery",
        "One of Chile's most quality-focused and innovative producers, De Martino has been at the forefront of rediscovering the potential of Bio-Bio's old-vine Pais and cool-climate varieties. Their Viejas Tinajas old-vine Pais made in clay amphoras is one of Chile's most sought-after natural wines and has been instrumental in reviving international interest in the valley.")
prod7, new7 = PROD("De Martino Viejas Tinajas Pais Bio-Bio Valley DO", "wine_still", p7, r4, "Chile",
    subcategory="Pais",
    description="Revolutionary Bio-Bio old-vine Pais vinified in clay amphoras; pale, fragrant, and completely unique — cranberry, dried herbs, orange peel, and earthy spice from 17th-century mission vines; one of Chile's most distinctive wines",
    price_tier="premium")
if new7:
    PAIR(prod7, "Cazuela de Ave (Chilean chicken broth with corn and rice)", "complement", "classic", "main", "Pale, fragrant Pais with the clean broth richness of Chile's most beloved everyday soup is a deeply regional combination")
    PAIR(prod7, "Pollo al Ajillo (garlic chicken) with white rice and salsa verde", "complement", "established", "main", "The wine's herb and dried fruit character resonates with the garlicky, herbal chicken preparation")
    PAIR(prod7, "Smoked longaniza sausage with pebre (Chilean herb salsa)", "complement", "classic", "starter", "Old-vine Pais and the smoky spice of Chilean longaniza with fresh herb salsa — a mission-era food pairing updated")
    PAIR(prod7, "Empanadas de pino (meat and egg empanadas)", "complement", "classic", "main", "Chile's most beloved baked snack with its most historically significant grape variety — a deeply Chilean combination")

p8 = P("Clos des Fous", "Chile", r4, "winery",
        "A small natural wine project founded by Pedro Parra (one of the world's leading terroir consultants) and partners in Bio-Bio and Itata, Clos des Fous makes wines of extraordinary transparency and precision from old-vine Pais and cool-climate varieties. Their Locura range has attracted international critical attention to Chile's south.")
prod8, new8 = PROD("Clos des Fous Pinot Noir Locura Bio-Bio Valley DO", "wine_still", p8, r4, "Chile",
    subcategory="Pinot Noir",
    description="Cool-climate Bio-Bio Pinot Noir from one of Chile's pioneering natural wine estates; delicate, aromatic, and mineral with Pacific-influenced red cherry, dried rose, and earthy precision",
    price_tier="premium")
if new8:
    PAIR(prod8, "Congrio al horno (baked conger eel with papas a la criolla)", "complement", "adventurous", "main", "Chilean coastal tradition: cool-climate Pinot Noir with the delicacy of conger eel baked with creamy potato")
    PAIR(prod8, "Grilled salmon with merkén-spiced butter and quinoa", "complement", "established", "main", "Pacific salmon from southern Chile with Mapuche smoked chilli butter — and a Bio-Bio cool Pinot — is a genuinely Chilean pairing")
    PAIR(prod8, "Mushroom and truffle croquetas", "complement", "established", "starter", "The wine's earthy mineral notes resonate with mushroom and truffle in the crispy fried starter")
    PAIR(prod8, "Fresh goat's cheese from the Chilean south with roasted beet", "bridge", "suggested", "cheese", "The wine's delicacy and mineral precision bridge with fresh, tangy goat's cheese and earthy roasted beet from the fertile south")

# ── 5. TEXAS HILL COUNTRY (USA) ──────────────────────────────────────────────
print("\n=== Texas Hill Country (USA) ===")
r5 = R("Texas Hill Country", "USA", "wine",
       designation_type="AVA",
       designation_name="Texas Hill Country AVA",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="America's second-largest wine AVA by area and the heart of the Texas wine industry, in the limestone hills west of Austin. Texas Hill Country is pioneering Spanish and Mediterranean varieties in the American Southwest: Tempranillo, Garnacha, Mourvèdre, Viognier, and Rhone blends thrive in the limestone soils and warm, dry climate. The Hill Country has experienced explosive growth since the 1990s, transforming from a regional curiosity to a nationally recognised wine destination.",
       key_producers="Becker Vineyards, William Chris Vineyards, Duchman Family Winery, Pedernales Cellars, Lewis Wines",
       historical_context="Texas wine history predates California's — the first winery in the USA operated in Texas in the 1650s, run by Franciscan priests at Val Verde. The modern Texas wine industry began in the 1970s when Pheasant Ridge Winery planted the first commercial vineyards in the Hill Country. The boom of the 2000s-2010s saw Texas wineries multiply from 40 to over 400, driven by tourism and a growing appreciation for locally-sourced Spanish and Rhone varieties well-suited to the climate.")

VIN(r5, 2023, "very_good", "rising", "Good Hill Country growing season; Tempranillo and Viognier of reliable character and improving quality")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage for Texas; finest Tempranillo and Rhone blends in recent memory")
VIN(r5, 2021, "good", "stable", "Winter storm Uri disrupted early season but warm summer recovery produced reliable fruit")
VIN(r5, 2020, "very_good", "stable", "Good growing season; Hill Country Spanish varieties at confident, food-friendly quality")
VIN(r5, 2019, "excellent", "rising", "Benchmark Texas vintage; critical recognition growing for Hill Country as a serious wine region")

p9 = P("Becker Vineyards", "USA", r5, "winery",
        "The founding family of premium Texas wine, Richard and Bunny Becker established their Hill Country estate in 1992 and have been the most consistent and respected producers in the state ever since. Their Iconoclast Cabernet and Prairie Rotie Rhone blend have won national competitions and established Texas Hill Country on the American wine map.")
prod9, new9 = PROD("Becker Vineyards Prairie Rotie Texas Hill Country AVA", "wine_still", p9, r5, "USA",
    subcategory="Mourvedre Grenache Syrah",
    description="Texas's most celebrated Rhone blend; limestone Hill Country Mourvedre, Grenache, and Syrah — dark plum, smoked meat, dried herbs, and warm Texas spice with a long, structured finish",
    price_tier="mid_range")
if new9:
    PAIR(prod9, "BBQ beef brisket with Hill Country oak smoke and jalapeño", "complement", "classic", "main", "The ultimate Texas pairing: Hill Country Rhone blend with slow-smoked Hill Country beef brisket — smoke, herbs, and dark fruit in perfect harmony")
    PAIR(prod9, "Venison sausage with Texas red chili and cornbread", "complement", "classic", "main", "Dark, rustic Texas Rhone blend and local game sausage with Lone Star State chili — the most Texas combination imaginable")
    PAIR(prod9, "Grilled lamb chops with Texas honey and herbs", "complement", "established", "main", "Warm, herbal Rhone blend from limestone soils and grilled Hill Country lamb with local honey — a naturally complementary combination")
    PAIR(prod9, "Aged Texas cheddar or Veldhuizen Bosque Blue cheese", "bridge", "established", "cheese", "The wine's dark fruit and herbs bridge with Texas artisan cheese — supporting the growing local cheese culture")

p10 = P("William Chris Vineyards", "USA", r5, "winery",
         "One of Texas's most respected artisan wine estates, William Chris Vineyards focuses exclusively on Texas-grown grapes and has been instrumental in developing Texas-specific varietals and blends. Their Halo blend and varietal Tempranillo have attracted national attention and are considered among the finest expressions of Hill Country terroir.")
prod10, new10 = PROD("William Chris Vineyards Halo Tempranillo Texas Hill Country", "wine_still", p10, r5, "USA",
    subcategory="Tempranillo",
    description="Texas's benchmark Tempranillo from limestone Hill Country; dark cherry, tobacco, leather, and earthy warmth with the grape's characteristic firm acidity — demonstrating that Texas has found its ideal red variety",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Smoked brisket tacos al pastor with salsa verde", "complement", "classic", "main", "Texas Tempranillo with smoked taco filling is the quintessential Texas-Mexico border food-wine combination — barbecue meets Spain via Austin")
    PAIR(prod10, "Carne asada with black beans and lime crema", "complement", "classic", "main", "The wine's cherry fruit and tobacco notes are a natural match for grilled skirt steak with classic Tex-Mex accompaniments")
    PAIR(prod10, "Lamb barbacoa with flour tortilla and pickled red onion", "complement", "established", "main", "Tempranillo's firm acidity and dark fruit hold up to the rich fattiness of slow-cooked lamb barbacoa")
    PAIR(prod10, "Texas charcuterie with bresaola, aged cheddar, and jalapeño honey", "complement", "established", "starter", "The wine's leather and cherry character makes it the natural choice for a Texas artisan charcuterie spread")

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
