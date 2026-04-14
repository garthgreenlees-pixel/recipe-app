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
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Elqui Valley ────────────────────────────────────────────────────
print("\n=== Region 1: Elqui Valley ===")
r1 = R("Elqui Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Elqui Valley DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Chile's northernmost wine region, close to the Atacama Desert, at extreme altitude (between 2,000m and 2,800m in the Andes foothills), surrounded by one of the clearest skies on Earth — home to multiple international observatories. The Elqui produces intensely mineral, high-acidity wines from Syrah, Carménère, and Muscat in an unlikely terroir that is attracting global attention for its extreme viticultural conditions.",
    key_producers="Viña Falernia, De Martino, Tamaya",
    historical_context="Elqui's wine history is intertwined with Pisco production — Chile's national spirit is distilled from the valley's Muscat grapes; the shift to premium table wines began in the 1990s when Falernia brought Italian winemaking expertise to this remote high-altitude desert valley.")

for yr, qd, pt in [
    (2022, "very_good", "rising"), (2021, "excellent", "rising"),
    (2020, "good", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Viña Falernia", "winery", r1, "Chile",
    production_philosophy="terroir_focused",
    philosophy_description="Italian-Chilean collaboration bringing Piedmontese winemaking expertise to Chile's most extreme wine region — Falernia's high-altitude Syrah and Carménère from the Elqui are among Chile's most distinctive wines, with a mineral intensity and freshness unlike anything from Chile's cooler central valleys.",
    reputation_narrative="The pioneer of Elqui Valley quality wine; Falernia's Syrah is one of Chile's most original terroir expressions.",
    price_positioning="mid_range")

prod1b_id = P("De Martino", "winery", r1, "Chile",
    production_philosophy="natural",
    philosophy_description="De Martino's pioneering exploration of Chile's extreme terroirs includes high-altitude Elqui alongside Atacama Desert and volcanic Limarí wines — their Natural Wine approach and field blend philosophy have produced some of Chile's most individual expressions.",
    reputation_narrative="Chile's most adventurous natural wine producer; De Martino Elqui bottlings are among Chile's most distinctive.",
    price_positioning="premium")

prod1a, new1a = PROD("Falernia Syrah Reserva Elqui Valley", "wine_still", prod1a_id, r1, "Chile",
    subcategory="Syrah",
    description="High-altitude Elqui Valley Syrah from 1,400m — intense violet, dark olive, and iron mineral with a freshness impossible in Chile's warmer central valleys. A genuinely original Chilean wine from a desert landscape of extraordinary viticultural character.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Grilled alpaca loin with chimichurri and Andean potato", "complement", "adventurous", "main",
         "Andean altitude meat with Andean altitude wine — chimichurri's herbs echo Syrah's olive and herbal notes.")
    PAIR(prod1a, "Lamb asado with merquén (smoked Andean chilli) rub", "complement", "established", "main",
         "Chilean smoked chilli and high-altitude Syrah — the wine's dark olive and iron mineral handles the smoke.")
    PAIR(prod1a, "Goat's cheese from the Atacama with dried figs and honey", "complement", "established", "cheese",
         "Desert goat's cheese with desert wine — both carry the intensity and mineral focus of extreme terroir.")
    PAIR(prod1a, "Patagonian lamb ribs with wild herb crust and quinoa", "complement", "established", "main",
         "South American lamb with high-altitude Chilean Syrah — the wine's freshness and mineral frame the lamb's richness.")

prod1b, new1b = PROD("De Martino Viejas Tinajas Elqui Muscat of Alexandria", "wine_still", prod1b_id, r1, "Chile",
    subcategory="Muscat of Alexandria",
    description="Natural, skin-fermented Muscat of Alexandria from Elqui's oldest tinajas (clay amphora) — a radical departure from any traditional Chilean wine. Orange-amber coloured, aromatic, mineral, and dry with rosewater, spice, and desert-mineral character from extreme altitude.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Hummus with preserved lemon, sumac, and pine nuts", "complement", "established", "starter",
         "Middle Eastern aromatic food with a skin-contact Muscat — rosewater and citrus bridge the tahini's richness.")
    PAIR(prod1b, "Grilled halloumi with pomegranate and fresh mint", "complement", "established", "starter",
         "The wine's rosewater and spice complement the squeaky halloumi's fat and pomegranate's tart sweetness.")
    PAIR(prod1b, "Moroccan chicken pastilla with cinnamon, almonds, and icing sugar", "bridge", "adventurous", "main",
         "Aromatic Muscat's complexity bridges the sweet-savoury Moroccan pastilla — spice and floral mirror each other.")
    PAIR(prod1b, "Aged manchego with orange blossom honey and Marcona almonds", "complement", "established", "cheese",
         "Orange blossom in the honey mirrors the Muscat's floral character; Manchego's fat handles the tannin.")

# ── Region 2: Itata Valley ────────────────────────────────────────────────────
print("\n=== Region 2: Itata Valley ===")
r2 = R("Itata Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Itata Valley DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Chile's oldest wine valley, 500km south of Santiago, where 16th-century Spanish missionaries planted the first Chilean vines that survived centuries of isolation to produce extraordinary old-vine Cinsault and País (Mission grape). A new generation of natural wine producers has discovered Itata's centenarian vines on granite and schist soils — producing wines of extraordinary purity, freshness, and historical resonance unlike anything from Chile's more celebrated central valleys.",
    key_producers="De Martino, Garage Wine Co, Cacique Maravilla, Viñedos Alcohuaz",
    historical_context="Jesuits planted the first vines in Itata in 1548; the region supplied Chile for centuries while Santiago-region wineries modernised; Itata's remoteness meant its old vines survived phylloxera and industrialisation — making it Chile's viticultural heritage heartland.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "rising"),
    (2020, "good", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Garage Wine Co", "winery", r2, "Chile",
    production_philosophy="natural",
    philosophy_description="Canadian-Chilean team Derek Mossman Knapp and Pilar Miranda produce Chile's most internationally acclaimed natural wines from Itata's old-vine Cinsault and País — minimal intervention, old amphorae, and exceptional respect for centenarian vines that survived because of Itata's isolation.",
    reputation_narrative="Chile's most internationally celebrated natural wine producer; Lot series Cinsault is a benchmark for South American natural wine.",
    price_positioning="premium")

prod2b_id = P("Cacique Maravilla", "winery", r2, "Chile",
    production_philosophy="traditional",
    philosophy_description="Patricio Toro preserves Itata's 500-year-old winemaking traditions — using ancient cement fermenters, old neutral oak, and native Mapuche winemaking knowledge to produce authentic País and Cinsault from century-old dry-farmed vines.",
    reputation_narrative="The most authentic traditional Itata producer; Cacique Maravilla preserves Chile's oldest winemaking heritage.",
    price_positioning="mid_range")

prod2a, new2a = PROD("Garage Wine Co Truquilemu Cinsault", "wine_still", prod2a_id, r2, "Chile",
    subcategory="Cinsault",
    description="Old-vine Cinsault from the Truquilemu sector of Itata — centenarian vines on granite producing a wine of haunting lightness, red-fruit purity, and mineral freshness unlike any other Chilean wine. Natural, unoaked, and a reference for the global rediscovery of Cinsault's quality potential.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Grilled sardines with charred lemon and sea salt", "complement", "established", "main",
         "Cinsault's delicate, fresh red-fruit character handles the sardines' richness while the acid cuts the fat.")
    PAIR(prod2a, "Chilean empanada de pino (beef, olive, egg) baked version", "complement", "classic", "casual",
         "Chile's defining snack food with Chile's most original old-vine red — a heritage Chilean pairing.")
    PAIR(prod2a, "Roasted beet and goat's cheese salad with walnuts", "complement", "established", "starter",
         "Old-vine Cinsault's earthy mineral character bridges with beet's iron note and goat's cheese freshness.")
    PAIR(prod2a, "Chilled charcuterie with olives and pickled peppers", "complement", "classic", "casual",
         "Garage Cinsault's light, fresh style suits the simplicity of charcuterie — a natural wine bistro pairing.")

prod2b, new2b = PROD("Cacique Maravilla País Antiguas Viñas", "wine_still", prod2b_id, r2, "Chile",
    subcategory="País",
    description="The oldest Chilean vine variety, brought by Spanish missionaries in 1548 — Cacique Maravilla's old-vine País is fermented in ancient cement and aged with minimal intervention. Light-coloured, aromatic, and historically unique; a direct connection to Chile's 500-year-old wine heritage.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Cazuela de vacuno (Chilean beef and vegetable stew)", "complement", "classic", "main",
         "Chile's most traditional beef stew with Chile's oldest grape variety — 500 years of cultural alignment.")
    PAIR(prod2b, "Pebre (Chilean salsa) with bread and charqui (dried llama)", "complement", "classic", "casual",
         "Traditional Chilean condiments and dried Andean meat with the country's oldest wine grape — cultural heritage.")
    PAIR(prod2b, "Grilled merken-spiced pork ribs with potato salad", "complement", "established", "main",
         "Chilean smoked chilli (merken) with old-vine País — both carry indigenous heritage and smoky character.")
    PAIR(prod2b, "Mild aged goat's cheese with local wildflower honey", "complement", "established", "cheese",
         "Simple aged artisan cheese from rural Chile with the oldest surviving vine variety — tradition meets tradition.")

# ── Region 3: Limari Valley ───────────────────────────────────────────────────
print("\n=== Region 3: Limarí Valley revisit ===")
r3 = R("Limarí Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Limarí Valley DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="A semi-desert coastal valley 400km north of Santiago influenced by Pacific fog from the Humboldt Current — one of Chile's most exciting emerging regions for Chardonnay, Pinot Noir, and Syrah. Limarí's calcium carbonate soils over sedimentary limestone create wines of remarkable minerality and freshness in a climate that would otherwise seem too warm for quality wine. The combination of desert aridity and coastal cooling creates a unique terroir.",
    key_producers="Concha y Toro Terrunyo, Tabalí, Falernia, Casa Tamaya",
    historical_context="Limarí's mining history dominated the valley until the 1990s; Concha y Toro's discovery of limestone-rich soils at Quebrada Seca sparked the quality wine revolution; the valley now competes with Casablanca for Chile's finest cool-climate Chardonnay.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Tabalí Winery", "winery", r3, "Chile",
    production_philosophy="terroir_focused",
    philosophy_description="One of Limarí's leading quality producers — Tabalí farms calcareous limestone vineyards with Pacific fog influence, producing Chardonnay, Pinot Noir, and Syrah of remarkable mineral precision and freshness for this semi-desert latitude.",
    reputation_narrative="Consistently cited as Limarí's benchmark producer; Tabalí Pinot Noir and Chardonnay have established the region internationally.",
    price_positioning="premium")

prod3b_id = P("Casa Tamaya", "winery", r3, "Chile",
    production_philosophy="traditional",
    philosophy_description="A coastal Limarí producer using Pacific fog cooling and limestone soils to produce a range of fine wines from Chardonnay, Viognier, and Syrah — Casa Tamaya has been instrumental in establishing Limarí's reputation for mineral white wines.",
    reputation_narrative="An important quality producer in establishing Limarí's white wine credentials internationally.",
    price_positioning="mid_range")

prod3a, new3a = PROD("Tabalí Talinay Chardonnay", "wine_still", prod3a_id, r3, "Chile",
    subcategory="Chardonnay",
    description="From the Talinay sector of Limarí on pure white limestone soils — one of Chile's most mineral and age-worthy Chardonnays. Oyster shell, citrus blossom, and white mineral with Pacific-fog freshness and a salinity that suggests Chablis more than California.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Pacific oysters with fresh lemon and mignonette", "cleanse", "classic", "aperitif",
         "Limestone Chardonnay's oyster-shell character mirrors Pacific oysters from the same coastal latitude.")
    PAIR(prod3a, "Grilled Pacific sole with capers and herb butter", "complement", "established", "fish_course",
         "Simple white fish with Chile's most mineral Chardonnay — a clean, precise pairing of pure terroir.")
    PAIR(prod3a, "Ceviche de corvina with ají amarillo and corn", "complement", "established", "starter",
         "Chile's citrus-marinated fish with a citrus-mineral Chilean white — the acidity of both align perfectly.")
    PAIR(prod3a, "White asparagus with maltaise sauce (blood orange hollandaise)", "complement", "established", "starter",
         "Spring asparagus with a mineral Chilean Chardonnay — the citrus hollandaise bridges through acidity.")

prod3b, new3b = PROD("Casa Tamaya Reserva Viognier", "wine_still", prod3b_id, r3, "Chile",
    subcategory="Viognier",
    description="Limarí Valley Viognier from Pacific-cooled limestone terraces — stone fruit, apricot, and jasmine character with better freshness and mineral precision than most warm-climate Viognier, showing the Humboldt Current's moderating effect.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Grilled tiger prawns with mango, chilli, and lime salsa", "complement", "established", "starter",
         "Viognier's stone-fruit aromatics harmonise with the mango salsa while acidity frames the chilli heat.")
    PAIR(prod3b, "Slow-cooked North African chicken tagine with preserved lemon and olives", "bridge", "established", "main",
         "Viognier's apricot and jasmine character bridges North African spice and preserved lemon's citrus notes.")
    PAIR(prod3b, "Thai-style fish cakes with sweet chilli dipping sauce", "complement", "established", "starter",
         "Aromatic Viognier and fragrant fish cakes share a tropical-floral vocabulary in this Pacific-influenced pairing.")
    PAIR(prod3b, "Fresh chèvre with roasted apricot and lavender honey", "complement", "established", "cheese",
         "Viognier's apricot and floral character mirrors the fresh goat's cheese, roasted stone fruit, and lavender.")

# ── Region 4: San Juan (Argentina revisit) ────────────────────────────────────
print("\n=== Region 4: Bio Bio Valley ===")
r4 = R("Bio Bio Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Bio Bio Valley DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Chile's southernmost wine region and a frontier for cool-climate varieties — Bio Bio (and neighbouring Malleco) produce Riesling, Pinot Noir, Gewürztraminer, and Chardonnay from some of Chile's most challenging, rain-soaked, volcanic terrain. German immigrants planted the first commercial vines in the 19th century; today a small group of determined producers is exploring the potential for elegant wines from Chile's least hospitable wine landscape.",
    key_producers="Santa Barbara Winery, Viña Maquis, Cono Sur Bio Bio",
    historical_context="German settlers established Brewery and winemaking traditions in Bio Bio in the 1850s; the region's proximity to the Mapuche heartland means that some of Chile's oldest tradition-holders still influence viticulture; Cono Sur's investment established international interest.")

for yr, qd, pt in [
    (2022, "very_good", "rising"), (2021, "good", "stable"),
    (2020, "very_good", "stable"), (2019, "good", "stable"), (2018, "average", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Cono Sur Vineyards and Winery", "winery", r4, "Chile",
    production_philosophy="terroir_focused",
    philosophy_description="Chile's most adventurous large producer — Cono Sur's exploration of extreme terroirs includes Bio Bio and Malleco, producing Pinot Noir and Riesling from Chile's coolest and most challenging wine landscapes. Their bicycle label democratised Chilean Pinot Noir globally.",
    reputation_narrative="The most successful Chilean wine brand internationally at mid-range; pioneer of Chilean cool-climate exploration.",
    price_positioning="mid_range")

prod4b_id = P("Santa Barbara Winery Bio Bio", "winery", r4, "Chile",
    production_philosophy="traditional",
    philosophy_description="A pioneer of Bio Bio Valley quality wine production from German-heritage families who settled the region in the 19th century — Santa Barbara produces Riesling and Gewürztraminer of unusual freshness and character from volcanic and clay soils in this rainy southern region.",
    reputation_narrative="Bio Bio's founding quality estate for aromatic white varieties; increasingly recognised by European importers.",
    price_positioning="mid_range")

prod4a, new4a = PROD("Cono Sur Ocio Pinot Noir", "wine_still", prod4a_id, r4, "Chile",
    subcategory="Pinot Noir",
    description="Cono Sur's flagship from the coolest Chilean vineyards — Bio Bio and Casablanca Valley selection, producing Chile's most serious Pinot Noir. Elegant, complex, and structured with red cherry, dried flowers, and a mineral freshness that places it among South America's best cool-climate Pinots.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Roasted duck breast with cherry reduction and beetroot purée", "complement", "classic", "main",
         "Chile's finest Pinot Noir with duck's richness — cherry and dark fruit in both the wine and the reduction.")
    PAIR(prod4a, "Pan-seared salmon with lentils and smoked paprika oil", "complement", "established", "fish_course",
         "Cool-climate Chilean Pinot bridges salmon's fat and the smoky paprika through its red-fruit acidity.")
    PAIR(prod4a, "Wild mushroom risotto with aged Parmigiano and white truffle oil", "complement", "established", "main",
         "Earthy mushroom risotto echoes Bio Bio Pinot's forest character in a classic contemporary pairing.")
    PAIR(prod4a, "Aged Queso de Oaxaca with chile verde and tortilla chips", "complement", "adventurous", "casual",
         "South American cheese and chilli with a cool-climate South American Pinot — an unusual cross-cultural pairing.")

prod4b, new4b = PROD("Santa Barbara Bio Bio Riesling", "wine_still", prod4b_id, r4, "Chile",
    subcategory="Riesling",
    description="Riesling from Bio Bio's volcanic and granite soils — Chile's most unexpected white wine: slate-mineral, bone-dry, and citrus-focused with a freshness that echoes Alsatian terroir from Chile's southernmost wine frontier.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled Patagonian trout with lemon, dill, and potato", "complement", "classic", "fish_course",
         "Southern Chilean freshwater trout with southern Chilean Riesling — the simplest and most authentic regional pairing.")
    PAIR(prod4b, "Mapuche curanto (shellfish and meat smoked in an earth oven)", "complement", "adventurous", "main",
         "The most traditional Chilean food with the most unusual Chilean white — Mapuche heritage meets German grape variety.")
    PAIR(prod4b, "Japalache (smoked Chilean sausage) with sauerkraut", "complement", "established", "casual",
         "German-heritage food traditions in Chile — sauerkraut sausage with Riesling bridges old and new world.")
    PAIR(prod4b, "Aged Gauda-style Chilean cheese with pear and walnut", "complement", "established", "cheese",
         "Southern Chilean aged cheese with the valley's most distinctive white — mineral Riesling and nutty aged Gauda.")

# ── Region 5: Colchagua Valley (new producers) ───────────────────────────────
print("\n=== Region 5: Rapel Valley ===")
r5 = R("Colchagua Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Colchagua Valley DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's most celebrated red wine valley, 200km south of Santiago — a warm Mediterranean microclimate sheltered by the Coastal and Andes mountain ranges, producing Cabernet Sauvignon, Carménère, and Syrah of extraordinary concentration and depth. Colchagua's star appellations — Apalta (home to Lapostolle's Clos Apalta), Marchigüe, and Los Lingues — each express the valley's exceptional terroir with distinct styles.",
    key_producers="Lapostolle, Casa Silva, Montes, Viu Manent, Luis Felipe Edwards",
    historical_context="Colchagua was primarily a bulk wine region until the 1990s when Chilean wine's export revolution began; Alexandra Marnier-Lapostolle's investment in Clos Apalta's hillside Apalta terroir in 1994 was the watershed moment that established international recognition.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "excellent", "stable"),
    (2020, "very_good", "stable"), (2019, "exceptional", "stable"), (2018, "excellent", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Montes Wines", "winery", r5, "Chile",
    production_philosophy="terroir_focused",
    philosophy_description="Aurelio Montes pioneered Chile's premium quality movement in 1988 — his Montes Alpha, Montes Purple Angel, and Taita are benchmarks for Chilean Carménère and Cabernet Sauvignon. Montes farms across multiple Chilean valleys and has expanded to Argentina, Napa, and Spain.",
    reputation_narrative="One of Chile's most internationally recognised quality brands; Montes Purple Angel is Chile's reference Carménère.",
    price_positioning="ultra_premium")

prod5b_id = P("Casa Silva", "winery", r5, "Chile",
    production_philosophy="traditional",
    philosophy_description="The Silva family has farmed Colchagua since 1892 — Casa Silva's Cool Coast Pinot Noir and Carménère Gran Terroir are made from estate vineyards across the valley's finest zones, representing one of Chile's most complete wine portfolios.",
    reputation_narrative="One of Colchagua's founding family estates; the Quinta Generación wines are collecting international attention.",
    price_positioning="premium")

prod5a, new5a = PROD("Montes Purple Angel Carménère", "wine_still", prod5a_id, r5, "Chile",
    subcategory="Carménère",
    description="Chile's most celebrated single-variety Carménère — from the Apalta hillside and Marchigüe sub-regions, showing the variety at its most complex: dark plum, chocolate, coffee, green pepper, and a silky texture that defines premium Chilean Carménère. Purple Angel is the variety's global ambassador.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Slow-roasted leg of lamb with chimichurri and roasted garlic", "complement", "classic", "main",
         "Chile's definitive lamb preparation with its most celebrated red variety — chimichurri echoes the wine's herbal edge.")
    PAIR(prod5a, "Braised short rib with dark chocolate mole and plantain", "complement", "established", "main",
         "Carménère's chocolate and coffee dimension mirrors the mole — an unexpected South American-Mexican harmony.")
    PAIR(prod5a, "Grilled Wagyu sirloin with bone marrow butter and truffle salt", "complement", "established", "main",
         "Colchagua's premium red handles Wagyu's extraordinary fat with tannin and dark-fruit concentration.")
    PAIR(prod5a, "Aged Manchego with piquillo pepper and black truffle honey", "complement", "established", "cheese",
         "Purple Angel's green pepper and dark fruit dimension bridge through the piquillo pepper's sweetness.")

prod5b, new5b = PROD("Casa Silva Cool Coast Pinot Noir", "wine_still", prod5b_id, r5, "Chile",
    subcategory="Pinot Noir",
    description="From the cool fog-influenced coastal Paredones sub-region within Colchagua — Casa Silva's Pinot Noir shows unexpected elegance and freshness, with red cherry, dried herbs, and mineral precision that challenges the valley's reputation for big reds.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Grilled Pacific salmon with herb crust and salsa verde", "complement", "established", "main",
         "Pacific salmon with a coastal Chilean Pinot — cool-climate freshness frames the salmon's fat with precision.")
    PAIR(prod5b, "Smoked duck breast with cherry mostarda and polenta", "complement", "established", "main",
         "Pinot's cherry and smoke connection through smoked duck — mostarda bridges the wine's fruit and the preparation.")
    PAIR(prod5b, "Beet and goat's cheese tart with walnut pastry", "complement", "established", "starter",
         "Earthy beet with light Colchagua Pinot — goat's cheese tangs while the wine's acid cuts through the cream.")
    PAIR(prod5b, "Parmigiano-Reggiano 24-month with truffle honey and walnuts", "complement", "established", "cheese",
         "Aged hard Italian cheese with Chilean Pinot — an unexpected cross-cultural pairing that works through umami and fruit.")

# ── Counts ────────────────────────────────────────────────────────────────────
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
cur.close()
conn.close()
