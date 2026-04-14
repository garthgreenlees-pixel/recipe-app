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

# ── REGION 1: Hemel-en-Aarde Valley (South Africa) ──────────────────────────
print("\n=== Region 1: Hemel-en-Aarde Valley ===")
r1 = R("Hemel-en-Aarde Valley", "South Africa", "wine",
    designation_type="ward", designation_name="Hemel-en-Aarde Valley Ward",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Hemel-en-Aarde Valley ('Heaven and Earth Valley') is South Africa's most celebrated cool-climate wine ward, situated in the Walker Bay area near Hermanus on the Atlantic coast. The marine-influenced climate and decomposed granite-shale soils produce Pinot Noir and Chardonnay of extraordinary elegance, complexity, and Burgundian affinity — genuinely world-class expressions that command international recognition.",
    key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Storm Wines",
    historical_context="Tim Hamilton Russell pioneered Hemel-en-Aarde's Pinot Noir and Chardonnay in 1975, planting vines when this valley was considered too cold and marginal. His conviction that South Africa needed a cool-climate region proved prescient — the valley now produces some of the Southern Hemisphere's finest Pinot Noir and the world's most southerly serious Chardonnay. The ward designation was formalised in 1994.")

VIN(r1, 2023, "excellent", "rising", "Outstanding vintage; cool Atlantic influence produced exceptional Pinot concentration with Burgundian precision and mineral definition")
VIN(r1, 2022, "very_good", "stable", "Fine balanced year with elegant Pinot and rich Chardonnay; good typicity and aging potential")
VIN(r1, 2021, "good", "stable", "Cooler year with more restrained expression; fine acidity and mineral character in both varieties")
VIN(r1, 2020, "excellent", "rising", "Benchmark vintage; extraordinary Pinot Noir depth and Chardonnay complexity from the granite-shale terroir")
VIN(r1, 2019, "very_good", "rising", "Classic Hemel-en-Aarde vintage with excellent Atlantic-influenced freshness and mineral precision")

prod1a_id = P("Hamilton Russell Vineyards", "South Africa", r1, "winery",
    "The founding estate and enduring benchmark of Hemel-en-Aarde; Tim Hamilton Russell's Pinot Noir and Chardonnay — South Africa's most expensive and exported wines of their variety — consistently achieve world-class quality that regularly challenges Burgundy premier cru in blind tastings.")
prod1a, new1a = PROD("Hamilton Russell Pinot Noir", "wine_still", prod1a_id, r1, "South Africa",
    subcategory="red", price_tier="premium",
    description="South Africa's benchmark Pinot Noir; Hamilton Russell's estate Pinot from decomposed granite-shale soils under Atlantic maritime influence. Dark cherry, dried herb, earthy mineral, and silky tannin. The wine that proved South Africa's Pinot Noir potential to the world.")
if new1a:
    PAIR(prod1a, "Grilled salmon trout with dill beurre blanc and caperberries", "complement", "established", "fish_course",
        "Rich salmon trout with dairy beurre blanc and briny caperberry suits Pinot Noir's acidity and delicacy; the wine's mineral depth bridges to the fish's oceanic character")
    PAIR(prod1a, "Slow-roasted Karoo lamb with rosemary and lamb jus", "complement", "classic", "main",
        "Karoo lamb — South Africa's herb-grazed inland lamb — and Hemel-en-Aarde Pinot is the defining South African fine dining pairing")
    PAIR(prod1a, "Mushroom and truffle arancini with aged Parmigiano", "complement", "established", "starter",
        "Earthy truffle and mushroom amplify Hamilton Russell Pinot's earthy mineral depth; Parmigiano adds umami salinity")
    PAIR(prod1a, "Venison loin with blackberry reduction and root vegetable gratin", "complement", "classic", "main",
        "South African game with blackberry and root vegetable mirrors Pinot's dark fruit and mineral character — a classic Cape fine dining presentation")

prod1b_id = P("Storm Wines", "South Africa", r1, "winery",
    "The most critically acclaimed young estate in Hemel-en-Aarde; Hannes Storm's single-vineyard Pinot Noirs from the Moya (shale) and Vrede (granite) sites are among South Africa's most coveted and internationally recognised wines.")
prod1b, new1b = PROD("Storm Moya Pinot Noir", "wine_still", prod1b_id, r1, "South Africa",
    subcategory="red", price_tier="premium",
    description="Storm's shale-terroir single-vineyard Pinot Noir; Moya from Hemel-en-Aarde Valley's shale soils showing extraordinary red fruit purity, dried herb, and mineral precision. Whole-bunch fermentation adds complexity — among South Africa's most Burgundian expressions of Pinot Noir.")
if new1b:
    PAIR(prod1b, "Duck liver parfait with Sauternes jelly and sourdough toast", "complement", "adventurous", "starter",
        "Duck liver's richness meets Storm Moya's silky Pinot texture; Sauternes jelly's sweetness contrasts the wine's dry mineral precision")
    PAIR(prod1b, "Wild mushroom pappardelle with truffle oil and aged Pecorino", "complement", "established", "main",
        "Forest mushroom pasta with truffle amplifies the wine's earthy mineral shale character; aged Pecorino adds saline depth")
    PAIR(prod1b, "Roasted pigeon breast with black cherry and lentils du Puy", "complement", "classic", "main",
        "Game bird's delicacy and earthy lentils are a natural vehicle for Storm Moya's red fruit purity and whole-bunch complexity")
    PAIR(prod1b, "Aged Gruyère with fig jam and walnut bread", "bridge", "established", "cheese",
        "Mountain cheese with fig bridges Pinot's red fruit; walnut adds earthy bitterness to mirror the shale terroir")

# ── REGION 2: Elgin (South Africa) ──────────────────────────────────────────
print("\n=== Region 2: Elgin ===")
r2 = R("Elgin", "South Africa", "wine",
    designation_type="appellation", designation_name="Elgin Wine Valley",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Elgin is South Africa's coolest wine-producing appellation, situated on a high plateau (200-600m elevation) in the Western Cape near the Elgin Valley. The region was an apple-growing heartland and wine was a relatively recent addition, but the altitude and maritime influence from False Bay create ideal conditions for Sauvignon Blanc, Pinot Noir, Chardonnay, and Riesling with remarkable freshness and precision.",
    key_producers="Paul Cluver Wines, Shannon Vineyards, Iona, Neil Ellis",
    historical_context="Elgin's wine industry began in earnest only in the 1990s when apple farmers like the Cluver family began experimenting with wine grapes, recognising that the cool plateau climate was poorly suited to warm-variety ripening. Paul Cluver's pioneering plantings of Pinot Noir and Riesling proved the valley's cool-climate potential, and Elgin has grown rapidly into one of South Africa's most dynamic and quality-driven appellations.")

VIN(r2, 2023, "excellent", "rising", "Outstanding cool vintage; fresh, aromatic wines with exceptional acidity and mineral precision from the high-altitude plateau")
VIN(r2, 2022, "very_good", "stable", "Fine balanced year with excellent Sauvignon Blanc and Pinot Noir freshness; good typicity across all varieties")
VIN(r2, 2021, "good", "stable", "Lean, elegant year with fine acidity; more restrained fruit but excellent mineral and aromatic precision")
VIN(r2, 2020, "very_good", "rising", "Strong vintage with good concentration while retaining Elgin's signature freshness and mineral definition")
VIN(r2, 2019, "excellent", "rising", "Benchmark Elgin vintage; textbook cool-climate expression across varieties with excellent aging potential")

prod2a_id = P("Paul Cluver Wines", "South Africa", r2, "winery",
    "The pioneering estate that established Elgin's fine wine identity; the Cluver family's wine program from a base of apple farming has produced benchmark Pinot Noir, Riesling, and Chardonnay that prove Elgin's potential as South Africa's premier cool-climate appellation.")
prod2a, new2a = PROD("Paul Cluver Pinot Noir", "wine_still", prod2a_id, r2, "South Africa",
    subcategory="red", price_tier="mid_range",
    description="Paul Cluver's cool-climate Elgin Pinot Noir: elegant, perfumed, and precise from high-altitude vineyards. Delicate red cherry, dried rose, and subtle mineral character — cooler and more restrained than Hemel-en-Aarde's style, with exceptional freshness and food versatility.")
if new2a:
    PAIR(prod2a, "Grilled springbok loin with waterblommetjie (Cape water flower) and quince", "complement", "classic", "main",
        "South African springbok is the country's great indigenous game meat; its lean delicacy and local fynbos herbs match Elgin Pinot's cool precision")
    PAIR(prod2a, "Beetroot and goat cheese salad with walnuts and honey dressing", "complement", "established", "starter",
        "Earthy beetroot and fresh goat cheese are Pinot Noir's natural salad pairing; the walnut dressing adds mineral bitterness to bridge the wine")
    PAIR(prod2a, "Roast chicken with thyme, garlic, and pan jus", "complement", "classic", "main",
        "The universal Pinot Noir food pairing — roast chicken with herbs — works beautifully with Elgin's cool, elegant style and natural freshness")
    PAIR(prod2a, "Trout almondine with lemon butter and fresh herbs", "complement", "established", "fish_course",
        "The classic Elgin fish pairing; farmed trout from local mountain streams with almond and lemon mirrors the wine's red fruit and fresh mineral acidity")

prod2b_id = P("Iona Vineyards", "South Africa", r2, "winery",
    "One of Elgin's most celebrated and focused estates; Andrew Gunn's Iona produces single-vineyard Sauvignon Blanc and Pinot Noir of exceptional precision and terroir expression from high-altitude vineyards planted with meticulous attention to clonal selection.")
prod2b, new2b = PROD("Iona Sauvignon Blanc", "wine_still", prod2b_id, r2, "South Africa",
    subcategory="white", price_tier="mid_range",
    description="Iona's benchmark cool-climate Elgin Sauvignon Blanc: restrained, mineral, and precise rather than the tropical exuberance of warmer South African examples. Grapefruit, nettle, white currant, and flinty mineral precision — among South Africa's most food-friendly and elegant Sauvignons.")
if new2b:
    PAIR(prod2b, "Grilled Cape line fish with lemon butter and green herb salsa", "complement", "classic", "fish_course",
        "South African grilled fish with citrus and herb is the definitive Western Cape food pairing for cool-climate Sauvignon Blanc's mineral precision")
    PAIR(prod2b, "Seared scallops with apple purée, sorrel, and crispy capers", "complement", "established", "fish_course",
        "Apple and sorrel are natural Sauvignon Blanc companions; the apple echoes Elgin's apple-growing heritage while sorrel mirrors the wine's herbal acidity")
    PAIR(prod2b, "Goat's cheese crottin with honey, thyme, and roasted grapes", "bridge", "classic", "cheese",
        "Fresh goat cheese and Sauvignon Blanc is the Loire-style cheese course pairing; honey and thyme bridge the wine's herbal mineral character")
    PAIR(prod2b, "Vegetable sushi with pickled ginger, wasabi, and soy", "complement", "established", "casual",
        "Sauvignon Blanc's green freshness and acidity match light vegetable sushi; pickled ginger and wasabi heat are tamed by the wine's citrus precision")

# ── REGION 3: Santorini PDO (Greece) ────────────────────────────────────────
print("\n=== Region 3: Santorini ===")
r3 = R("Santorini", "Greece", "wine",
    designation_type="PDO", designation_name="Santorini PDO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Santorini produces some of the world's most distinctive and mineral white wines from the Assyrtiko grape grown in volcanic ash (pumice) soil on the Aegean island. The unique 'kouloura' (basket) vine training keeps grapes close to the ground to protect from fierce Aegean winds. The wines show extraordinary mineral precision, electric acidity, saline character, and citrus concentration — some of the world's most distinctive terroir expressions.",
    key_producers="Domaine Sigalas, Gaia Wines, Hatzidakis, Argyros Estate",
    historical_context="Santorini's viticultural history stretches 3,500 years — among the oldest in the world. The island's unique geology (layers of volcanic pumice and ash from the Bronze Age Minoan eruption) and the ancient kouloura vine training method have remained fundamentally unchanged. Assyrtiko was nearly unknown internationally until the 1990s when Domaine Sigalas and Gaia began exporting; the variety is now considered Greece's finest white wine grape.")

VIN(r3, 2023, "excellent", "rising", "Outstanding Santorini vintage; Assyrtiko achieved exceptional mineral concentration and electric acidity under ideal Aegean conditions")
VIN(r3, 2022, "very_good", "stable", "Fine balanced year with characteristic volcanic mineral intensity and citrus freshness")
VIN(r3, 2021, "good", "stable", "Consistent year with good typicity; saline mineral and lemon zest character well expressed")
VIN(r3, 2020, "excellent", "rising", "Benchmark vintage with extraordinary Assyrtiko concentration and the finest volcanic mineral expression in years")
VIN(r3, 2019, "very_good", "rising", "Classic Santorini vintage; textbook dry Assyrtiko with volcanic mineral depth and extraordinary saline length")

prod3a_id = P("Domaine Sigalas", "Greece", r3, "winery",
    "The pioneering estate that put Santorini Assyrtiko on the world stage; Paris Sigalas's biodynamic estate produces benchmark single-vineyard Assyrtiko of extraordinary mineral precision and complexity — among the world's most exciting white wine terroir expressions.")
prod3a, new3a = PROD("Sigalas Santorini Assyrtiko", "wine_still", prod3a_id, r3, "Greece",
    subcategory="white", price_tier="premium",
    description="The benchmark Santorini Assyrtiko from Domaine Sigalas: volcanic pumice terroir expressing electric acidity, white grapefruit, sea salt, and extraordinary mineral depth. Biodynamic and unfined. One of the world's great terroir wines — pure, saline, and incomparably fresh.")
if new3a:
    PAIR(prod3a, "Freshly grilled octopus with lemon, capers, and fava (yellow split pea purée)", "complement", "classic", "starter",
        "Santorini's iconic food-wine pairing: grilled octopus with the island's famous fava meets Assyrtiko's saline mineral character — a true terroir unity")
    PAIR(prod3a, "Fried kefalos (mullet) with sea salt and lemon", "complement", "classic", "fish_course",
        "Simple fried island fish — the fishermen's lunch — is the most authentic pairing for Santorini's mineral Assyrtiko and its volcanic precision")
    PAIR(prod3a, "Tomato keftedes (Santorini tomato fritters) with tzatziki", "complement", "classic", "starter",
        "Santorini's tiny, intensely sweet tomatoes fried in fritter form with cooling yoghurt is the island's most beloved meze for local Assyrtiko")
    PAIR(prod3a, "Sea bass ceviche with lime, jalapeño, and cucumber", "complement", "established", "starter",
        "Assyrtiko's electric acidity and saline mineral is a natural match for ceviche's lime-marinated freshness; the wine mirrors the dish's brightness")

prod3b_id = P("Argyros Estate", "Greece", r3, "winery",
    "One of Santorini's oldest and most respected family estates; Mathew Argyros has elevated the family's historic vineyards — including some of Greece's oldest vines (100+ years) — into one of Assyrtiko's most acclaimed ranges, including the extraordinary Cuvée Monsignori single-vineyard.")
prod3b, new3b = PROD("Argyros Estate Santorini Assyrtiko", "wine_still", prod3b_id, r3, "Greece",
    subcategory="white", price_tier="premium",
    description="Argyros Estate's flagship dry Assyrtiko from ancient kouloura vines on volcanic pumice; extraordinary concentration, saline minerality, and white grapefruit depth. One of the most compelling expressions of the variety's terroir — combining the old-vine intensity with the island's volcanic precision.")
if new3b:
    PAIR(prod3b, "Grilled whole bream with sea salt, olive oil, and lemon (alla griglia)", "complement", "classic", "fish_course",
        "The simplest Greek grilling method produces a perfect match for Santorini Assyrtiko's purity; the wine's mineral salinity reflects the fish's oceanic nature")
    PAIR(prod3b, "Lobster with lemon butter, chervil, and sea vegetables", "complement", "established", "fish_course",
        "Lobster's sweetness and sea brine find their Greek island expression with Assyrtiko's saline mineral depth; lemon butter matches the wine's citrus")
    PAIR(prod3b, "Graviera cheese with Santorini tomatoes and fresh oregano", "complement", "classic", "cheese",
        "Crete's aged Graviera cheese with the island's famous sweet tomatoes creates a purely Aegean pairing for Argyros's mineral Assyrtiko")
    PAIR(prod3b, "Fried calamari with aioli and preserved lemon", "complement", "classic", "starter",
        "Fried squid's light batter and oceanic sweetness are refreshed by Assyrtiko's acidity and mineral bite; a quintessential Mediterranean taverna pairing")

# ── REGION 4: Alentejo (Portugal) ───────────────────────────────────────────
print("\n=== Region 4: Alentejo ===")
r4 = R("Alentejo", "Portugal", "wine",
    designation_type="DOC", designation_name="Alentejo DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Alentejo is Portugal's largest and most productive wine region, spanning the vast rolling cork-oak plains south of Lisbon. Despite the hot continental climate, the elevated subregions produce rich, full-bodied reds from indigenous varieties — Aragonez (Tempranillo), Alicante Bouschet, Touriga Nacional, and Trincadeira — with dark fruit, spice, and earthy complexity. The region also produces excellent aromatic whites.",
    key_producers="Esporão, Herdade do Mouchão, Quinta do Crasto (in Alentejo), Malhadinha Nova",
    historical_context="Alentejo has produced wine since Roman times — the area's archaeological record shows Roman wine production at multiple sites. Modern commercial viticulture accelerated after Portugal joined the EU in 1986, with major investment in technology and international varieties. The region transformed from bulk wine production to quality-focused DOC status wines through the 1990s and 2000s, now competing internationally.")

VIN(r4, 2022, "excellent", "rising", "Outstanding Alentejo vintage; ideal growing season for Aragonez and Alicante Bouschet with exceptional concentration")
VIN(r4, 2021, "very_good", "stable", "Fine balanced year with good freshness despite warm conditions; aromatic whites particularly successful")
VIN(r4, 2020, "excellent", "rising", "Powerful vintage; deeply concentrated Alentejo reds with strong dark fruit and structured tannins")
VIN(r4, 2019, "very_good", "stable", "Classic vintage with excellent varietal typicity across indigenous red varieties; good aging potential")
VIN(r4, 2018, "good", "stable", "Accessible year with softer tannins; more approachable style with good Portuguese character")

prod4a_id = P("Esporão", "Portugal", r4, "winery",
    "Alentejo's most internationally recognised and awarded estate; Esporão's extensive biodynamic vineyards at Herdade do Esporão produce a complete range from everyday table wine to prestigious single-variety single-vineyard bottlings that represent Alentejo's finest.")
prod4a, new4a = PROD("Esporão Reserva Tinto", "wine_still", prod4a_id, r4, "Portugal",
    subcategory="red", price_tier="mid_range",
    description="Esporão's flagship Alentejo red: a blend of Aragonez, Alicante Bouschet, and Touriga Nacional aged in French and American oak. Dark cherry, blackberry, chocolate, and earthy complexity — the reference Alentejo wine and one of Portugal's most exported and recognised bottles.")
if new4a:
    PAIR(prod4a, "Ensopado de borrego (Alentejo lamb stew with bread and mint)", "complement", "classic", "main",
        "The regional lamb bread-stew is Alentejo's defining dish; the wine's dark fruit and earth mirrors the slow-cooked lamb's depth")
    PAIR(prod4a, "Grilled black pork (Porco Preto) with potato gratin and herb salad", "complement", "classic", "main",
        "Alentejo Black Pork — Portugal's Iberian breed raised on acorns — is the region's luxury product; its nutty richness meets Esporão's dark fruit and oak")
    PAIR(prod4a, "Carne de porco à Alentejana (pork with clams and coriander)", "complement", "classic", "main",
        "Portugal's classic surf-and-turf dish from Alentejo; the briny clams and rich pork are elevated by the wine's earthy dark fruit complexity")
    PAIR(prod4a, "Aged Queijo de Évora with tomato jam", "bridge", "classic", "cheese",
        "Alentejo's aged sheep cheese with regional tomato jam bridges the wine's dark fruit and earthy depth in a classic Portuguese cheese course")

prod4b_id = P("Malhadinha Nova", "Portugal", r4, "winery",
    "One of Alentejo's most ambitious and quality-focused boutique estates; the Soares family's Malhadinha Nova produces a range of single-variety wines that showcase the depth of Alentejo's indigenous varieties — particularly Aragonez and Alicante Bouschet — at premium quality.")
prod4b, new4b = PROD("Malhadinha Nova Alicante Bouschet", "wine_still", prod4b_id, r4, "Portugal",
    subcategory="red", price_tier="premium",
    description="Malhadinha Nova's single-variety Alicante Bouschet — Alentejo's most planted and celebrated teinturier variety. Deeply coloured, inky and powerful with blackberry, dark chocolate, Mediterranean herb, and earthy Alentejo mineral character. Increasingly recognised as a world-class variety in the right hands.")
if new4b:
    PAIR(prod4b, "Wild boar slow-braised with prunes, chocolate, and red wine", "complement", "classic", "main",
        "Wild boar's iron richness and prune-chocolate sauce are the natural match for Alicante Bouschet's dark inky concentration and herb depth")
    PAIR(prod4b, "Migas à Alentejana (bread, garlic, coriander, and black pork fat)", "complement", "classic", "main",
        "Alentejo's rustic bread dish with pork fat and coriander is the most authentic regional food for an inky Alicante Bouschet")
    PAIR(prod4b, "Churrasqueira lamb chops with piri piri and salsa verde", "complement", "established", "main",
        "Portuguese-style charcoal lamb with piri piri meets Alicante's dark fruit and herb character; salsa verde's acidity refreshes the wine's weight")
    PAIR(prod4b, "Dark chocolate fondant with fleur de sel and raspberry coulis", "complement", "adventurous", "dessert",
        "Alicante Bouschet's almost chocolate-inky character makes dark chocolate fondant a natural match; raspberry's acidity lifts the pairing")

# ── REGION 5: Bairrada DOC (Portugal) ───────────────────────────────────────
print("\n=== Region 5: Bairrada ===")
r5 = R("Bairrada", "Portugal", "wine",
    designation_type="DOC", designation_name="Bairrada DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Bairrada is one of Portugal's most distinctive wine regions, producing powerful, tannic reds from the indigenous Baga grape on the Atlantic-influenced clay-limestone soils between Coimbra and the coast. The wines are high acid, high tannin, and age magnificently — Portugal's most Barolo-like red wine structure. The region also produces excellent sparkling wines and aromatic whites from Bical and Maria Gomes.",
    key_producers="Luís Pato, Quinta das Bágeiras, Casa de Saima, Sidónio de Sousa",
    historical_context="Bairrada has produced wine since Roman times and was one of Portugal's most important wine regions until a 19th-century phylloxera disaster and subsequent regulatory battles (Baga was banned for decades in favour of more popular varieties). Luís Pato's tireless championing of Baga from the 1980s onward rescued the variety's reputation and established Bairrada as one of Portugal's most authentically distinctive wine regions.")

VIN(r5, 2022, "excellent", "rising", "Outstanding Bairrada vintage; Baga achieved exceptional tannin ripeness and aromatic complexity from the clay-limestone soils")
VIN(r5, 2021, "very_good", "stable", "Fine balanced year with classic Baga structure; good acidity and firm tannins for extended aging")
VIN(r5, 2020, "good", "stable", "Accessible year with softer-than-typical Baga tannins; good fruit and moderate structure")
VIN(r5, 2019, "excellent", "rising", "Benchmark Bairrada vintage; extraordinary Baga with iron mineral depth and exceptional 15-20 year aging potential")
VIN(r5, 2018, "very_good", "stable", "Classic vintage with excellent varietal typicity; high acid, firm tannin, and blackberry depth")

prod5a_id = P("Luís Pato", "Portugal", r5, "winery",
    "The champion and saviour of Baga and Bairrada; Luís Pato's passionate advocacy for the indigenous variety against regulatory attempts to ban it has transformed Bairrada's international reputation. His single-vineyard Baga wines are Portugal's most underrated serious reds.")
prod5a, new5a = PROD("Luís Pato Quinta do Ribeirinho Pé Franco Baga", "wine_still", prod5a_id, r5, "Portugal",
    subcategory="red", price_tier="premium",
    description="Luís Pato's ultimate Baga: ungrafted pre-phylloxera Baga vines ('pé franco' = own-rooted) from the Quinta do Ribeirinho clay vineyard. Extraordinary concentration of black cherry, iron, herb, and tannic depth — Portugal's most structured and age-worthy indigenous red with a 20-30 year horizon.")
if new5a:
    PAIR(prod5a, "Leitão à Bairrada (Bairrada roast suckling pig with crackling)", "complement", "classic", "main",
        "Bairrada's culinary icon — roast suckling pig — is inseparable from local Baga wine; the pig's fat and crackling soften the tannic grip while the wine cuts richness")
    PAIR(prod5a, "Braised hare with dark chocolate, juniper, and Bairrada red reduction", "complement", "classic", "main",
        "Game of this depth — hare with chocolate reduction — is the perfect match for Pê Franco's massive tannin and iron mineral character")
    PAIR(prod5a, "Aged Queijo da Serra da Estrela with quince and walnut", "bridge", "classic", "cheese",
        "Portugal's greatest mountain cheese — rich, runny Serra da Estrela sheep cheese — with quince bridges Baga's tannic depth and dark fruit")
    PAIR(prod5a, "Charcoal-grilled Angus beef with bone marrow and chimichurri", "complement", "established", "main",
        "Premium beef with bone marrow's fat concentration softens Baga's tannin grip; chimichurri's herb acidity provides refreshing contrast")

prod5b_id = P("Quinta das Bágeiras", "Portugal", r5, "winery",
    "One of Bairrada's most traditional and authentic estates; Mário Sérgio Nuno's Quinta das Bágeiras produces Baga of genuine depth and aging potential from old vines on clay soils — the most faithful expression of Bairrada's traditional winemaking identity.")
prod5b, new5b = PROD("Bágeiras Garrafeira Baga", "wine_still", prod5b_id, r5, "Portugal",
    subcategory="red", price_tier="mid_range",
    description="Quinta das Bágeiras's traditional Garrafeira Baga: aged minimum 3 years in bottle before release following traditional Bairrada practice. Black cherry, dried herb, iron mineral, and firm tannin from old-vine clay-limestone Baga. Authentic and food-demanding — a wine of genuine regional identity.")
if new5b:
    PAIR(prod5b, "Suckling pig sandwich (bifanas) with piri piri sauce", "complement", "established", "casual",
        "The more casual expression of Bairrada's great pork tradition; warm pulled pork in bread with piri piri meets Baga's acidity and dark fruit")
    PAIR(prod5b, "Bacalhau à Brás (salt cod with fried potatoes and scrambled eggs)", "complement", "established", "main",
        "Portugal's beloved salt cod scramble with its rich egg-potato base works surprisingly well with Bairrada Baga's high acidity cutting through the richness")
    PAIR(prod5b, "Slow-roasted lamb shoulder with coriander, garlic, and lemon", "complement", "classic", "main",
        "Portuguese-style roasted lamb with coriander and lemon is a reliable match for Baga's tannic structure and dark fruit depth")
    PAIR(prod5b, "Grilled sardines with tomato salad and cornbread", "complement", "classic", "casual",
        "Atlantic sardines are Portugal's summer classic; unusual with red wine but Bairrada's Baga tradition includes this regional pairing with fresh sardines")

# ── Summary ──────────────────────────────────────────────────────────────────
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
print("Done.")
conn.close()
