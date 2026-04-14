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
        return (row[0], False)
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return (pid, True)

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 69 ──────────────────────────────────────────────────────────────────
# Regions: Maipo Valley, Casablanca Valley, Aconcagua Valley, San Juan, Cafayate

# ── Region 1: Maipo Valley ────────────────────────────────────────────────────
print("\n=== Region 1: Maipo Valley ===")
r1 = R("Maipo Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Maipo Valley DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's historic heartland for Cabernet Sauvignon, centred around Santiago with soils ranging from alluvial gravel to clay. Produces structured, cedar-scented reds that age with distinction.",
    key_producers="Concha y Toro, Santa Rita, Almaviva, Viña Carmen, Don Melchor",
    historical_context="Chile's oldest wine region, home to its most celebrated Cabernet and the birthplace of iconic blends like Almaviva and Don Melchor."
)
VIN(r1, 2020, "excellent", "stable", "Cool winter followed by warm, dry summer — ideal for Cabernet structure and concentration.")
VIN(r1, 2019, "exceptional", "rising", "Benchmark vintage: perfect temperature swings produced wines of rare elegance and depth.")
VIN(r1, 2018, "very_good", "stable", "Consistent growing season with good acidity retention; wines show balance and longevity.")
VIN(r1, 2017, "good", "stable", "Slightly warm season; riper style wines with generous fruit and soft tannins.")
VIN(r1, 2016, "excellent", "stable", "Outstanding year for Cabernet Sauvignon — firm structure with remarkable freshness.")

p1a = P("Almaviva", "winery", r1, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Rothschild–Concha y Toro joint venture producing Maipo's most prestigious Cabernet-dominant blend from Alto Maipo.",
    reputation_narrative="Almaviva is Chile's benchmark for Bordeaux-style elegance, consistently among South America's most sought-after reds.",
    price_positioning="ultra_premium")
prod1a, new1a = PROD("Almaviva", "wine_still", p1a, r1, "Chile",
    subcategory="Cabernet Sauvignon blend",
    description="Opulent Cabernet Sauvignon-led blend showing blackcurrant, cedar, graphite and silky tannins; built for 10–20 years of ageing.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Rack of lamb with herb crust and black olive tapenade", "complement", "classic", "main", "The cassis and cedar of Almaviva mirror the herbaceous lamb; olive amplifies savoury depth.")
    PAIR(prod1a, "Aged Manchego with quince paste", "bridge", "established", "cheese", "Firm cheese fat rounds Cabernet tannin; quince bridges the fruit profile.")
    PAIR(prod1a, "Beef tenderloin with truffle jus", "complement", "classic", "main", "Ultra-premium red beef demands equal gravity; truffle aligns with graphite minerality.")
    PAIR(prod1a, "Dark chocolate fondant", "contrast", "suggested", "pre_dessert", "Bitter chocolate amplifies red fruit; structured tannin frames sweetness.")

p1b = P("Viña Carmen", "winery", r1, "Chile",
    production_philosophy="traditional",
    philosophy_description="One of Chile's oldest wineries producing expressive Maipo Cabernet with a focus on single-vineyard terroir.",
    reputation_narrative="Viña Carmen's Gold Reserve remains a benchmark mid-range Maipo Cabernet, prized for its reliability and complexity.",
    price_positioning="mid_range")
prod1b, new1b = PROD("Carmen Gold Reserve Cabernet Sauvignon", "wine_still", p1b, r1, "Chile",
    subcategory="Cabernet Sauvignon",
    description="Full-bodied Maipo Cabernet with dark plum, tobacco leaf and firm but integrated tannins; excellent value for ageing.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled ribeye with chimichurri", "complement", "classic", "main", "Classic South American pairing: the herbal chimichurri echoes the wine's green pepper note.")
    PAIR(prod1b, "Empanadas de pino (beef and olive)", "complement", "established", "starter", "Savoury beef filling mirrors the wine's dark fruit; olives echo its earthy notes.")
    PAIR(prod1b, "Roasted red pepper and black bean stew", "bridge", "suggested", "main", "Earthy legumes and sweet pepper align with ripe Cabernet fruit.")
    PAIR(prod1b, "Hard aged gouda", "complement", "established", "cheese", "Crystalline cheese fat softens Cabernet structure; caramel notes complement dark fruit.")

# ── Region 2: Casablanca Valley ───────────────────────────────────────────────
print("\n=== Region 2: Casablanca Valley ===")
r2 = R("Casablanca Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Casablanca Valley DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Cool coastal valley west of Santiago, pioneered in the 1980s for Chardonnay and Sauvignon Blanc. Pacific influence delivers crisp acidity and precise aromatics.",
    key_producers="Viña Casas del Bosque, Viña Indomita, William Fèvre Chile, Casa Marín, Concha y Toro",
    historical_context="Casablanca Valley transformed Chile's wine identity from red-only to world-class whites, opening cool-climate viticulture on the Pacific coast."
)
VIN(r2, 2022, "excellent", "stable", "Cool, foggy season ideal for Sauvignon Blanc and Chardonnay — bright acids and expressive aromatics.")
VIN(r2, 2021, "very_good", "stable", "Balanced season; wines show tropical and citrus notes with clean mineral finish.")
VIN(r2, 2020, "good", "stable", "Slightly warmer year; wines show rounder texture and more stone fruit character.")
VIN(r2, 2019, "excellent", "rising", "Classic cool year; taut Sauvignon Blanc with grapefruit and jalapeño precision.")
VIN(r2, 2018, "very_good", "stable", "Clean, aromatic growing season; consistent quality across white varieties.")

p2a = P("Viña Casas del Bosque", "winery", r2, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Leading Casablanca producer specialising in cool-climate whites and Pinot Noir from Pacific-influenced vineyards.",
    reputation_narrative="Consistently produces benchmark Casablanca Sauvignon Blanc and Chardonnay with great precision at accessible price points.",
    price_positioning="mid_range")
prod2a, new2a = PROD("Casas del Bosque Gran Reserva Sauvignon Blanc", "wine_still", p2a, r2, "Chile",
    subcategory="Sauvignon Blanc",
    description="Vivid Sauvignon Blanc with grapefruit, jalapeño, fresh herbs and a chalky mineral finish; ideal aperitif or seafood companion.",
    price_tier="mid_range")
if new2a:
    PAIR(prod2a, "Ceviche with lime, chilli and coriander", "complement", "classic", "starter", "Citrus and herb in the wine mirror the ceviche; acidity cuts through lime marinade.")
    PAIR(prod2a, "Grilled sea bass with salsa verde", "complement", "classic", "fish_course", "Herbal brightness in Sauvignon Blanc lifts salsa verde; both share sharp green character.")
    PAIR(prod2a, "Goat's cheese and rocket tartine", "bridge", "established", "starter", "Tangy chèvre aligns with grassy Sauvignon Blanc; peppery rocket adds structure.")
    PAIR(prod2a, "Asparagus and lemon risotto", "complement", "suggested", "main", "Green vegetal asparagus is a natural foil for herbaceous Sauvignon Blanc.")

p2b = P("Casa Marín", "winery", r2, "Chile",
    production_philosophy="minimal_intervention",
    philosophy_description="Pioneering small estate in Lo Abarca, the coldest corner of Casablanca, producing extreme cool-climate whites and Pinot Noir.",
    reputation_narrative="Casa Marín's Cipreses Vineyard Sauvignon Blanc is among Chile's most individual and terroir-driven whites.",
    price_positioning="premium")
prod2b, new2b = PROD("Casa Marín Cipreses Vineyard Sauvignon Blanc", "wine_still", p2b, r2, "Chile",
    subcategory="Sauvignon Blanc",
    description="Intensely mineral Sauvignon Blanc from extreme coastal exposure — flint, white peach, green herb and piercing acidity.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Oysters with mignonette", "complement", "classic", "aperitif", "Flint minerality and cutting acidity are the natural companion to raw oyster brine.")
    PAIR(prod2b, "Steamed mussels with white wine and shallots", "bridge", "established", "starter", "The wine's own acidity echoes the broth; mineral notes amplify shellfish sweetness.")
    PAIR(prod2b, "Seared scallop with cauliflower purée", "complement", "established", "fish_course", "Cauliflower earthiness grounds citrus-forward wine; sweet scallop flesh bridges both.")
    PAIR(prod2b, "Cucumber, dill and cream cheese canapés", "complement", "suggested", "amuse", "Fresh herb and cooling cucumber align with the wine's green precision.")

# ── Region 3: Aconcagua Valley ────────────────────────────────────────────────
print("\n=== Region 3: Aconcagua Valley ===")
r3 = R("Aconcagua Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Aconcagua Valley DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Long, narrow valley north of Santiago running east from the Pacific to the Andes, known for powerful Cabernet and pioneering Carmenère. Wide diurnal range preserves freshness in warm conditions.",
    key_producers="Errázuriz, Seña, Viñedo Chadwick",
    historical_context="Home to Errázuriz's iconic Don Maximiano estate and Seña, the joint venture with Robert Mondavi that helped establish Chilean fine wine on the global stage."
)
VIN(r3, 2021, "excellent", "rising", "Ideal growing season: warm days, cool nights preserved aromatic freshness and structure.")
VIN(r3, 2020, "very_good", "stable", "Solid vintage with good balance between concentration and acidity.")
VIN(r3, 2019, "exceptional", "rising", "Benchmark Aconcagua year: perfect Cabernet and Carmenère ripeness with striking freshness.")
VIN(r3, 2018, "good", "stable", "Warmer season; generous wines with approachable fruit and good early drinking pleasure.")
VIN(r3, 2017, "very_good", "stable", "Consistent quality; wines show elegance with medium-term ageing potential.")

p3a = P("Errázuriz", "winery", r3, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Historic Aconcagua estate founded 1870, producing Don Maximiano and the Seña joint venture — Chile's first grand cru concept wines.",
    reputation_narrative="Errázuriz defines Aconcagua Cabernet and was instrumental in elevating Chilean wine to international fine wine status.",
    price_positioning="premium")
prod3a, new3a = PROD("Errázuriz Don Maximiano Founder's Reserve", "wine_still", p3a, r3, "Chile",
    subcategory="Cabernet Sauvignon blend",
    description="Chile's most historic single-vineyard Cabernet — complex, layered and age-worthy, with blackcurrant, tobacco, cedar and firm mountain tannins.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Venison loin with juniper jus", "complement", "classic", "main", "Game meat's iron and gamey depth finds its match in cedar-inflected mountain Cabernet.")
    PAIR(prod3a, "Aged Manchego with membrillo", "bridge", "established", "cheese", "Firm ewes' milk cheese softens tannin; quince amplifies dark fruit.")
    PAIR(prod3a, "Charcoal-grilled beef asado", "complement", "classic", "main", "South American tradition; smoke and char harmonise with Cabernet's dark fruit backbone.")
    PAIR(prod3a, "Bitter chocolate truffles with sea salt", "contrast", "suggested", "digestif", "Bittersweet chocolate amplifies wine's fruit; salt draws out tannin structure.")

p3b = P("Seña", "winery", r3, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Errázuriz–Robert Mondavi joint venture, now independently produced, defining the apex of Chilean red wine with Cabernet-dominant blends.",
    reputation_narrative="Seña is consistently rated among South America's top five wines, representing the pinnacle of Chilean fine wine ambition.",
    price_positioning="ultra_premium")
prod3b, new3b = PROD("Seña", "wine_still", p3b, r3, "Chile",
    subcategory="Cabernet Sauvignon blend",
    description="Grand cru-level Chilean red; Cabernet Sauvignon with Merlot, Carmenère, Malbec and Cabernet Franc — silky, complete and built for decades.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Roasted lamb shoulder with black garlic and rosemary", "complement", "classic", "main", "Complex lamb aromatics mirror Seña's herbal Carmenère notes; black garlic adds umami depth.")
    PAIR(prod3b, "Truffle and parmesan risotto", "complement", "established", "main", "Earthy truffle resonates with wine's graphite and tobacco layers.")
    PAIR(prod3b, "Blue cheese and walnut on sourdough", "contrast", "adventurous", "cheese", "Bold cheese challenges tannin; walnut bitterness anchors the pairing.")
    PAIR(prod3b, "Dark chocolate and cardamom tart", "bridge", "suggested", "dessert", "Spice and bitter chocolate soften the wine's grand structure at table's end.")

# ── Region 4: San Juan ────────────────────────────────────────────────────────
print("\n=== Region 4: San Juan ===")
r4 = R("San Juan", "Argentina", "wine",
    designation_type="IG",
    designation_name="San Juan IG",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Argentina's second-largest wine region, north of Mendoza, known for intense Syrah, Bonarda, and bold Malbec grown at altitude under extreme sun and low humidity.",
    key_producers="Zuccardi Valle de Uco, Finca Las Moras, Santiago Graffigna",
    historical_context="Historically known for bulk production, San Juan is rapidly emerging as a quality region with Syrah and Bonarda gaining international recognition."
)
VIN(r4, 2022, "good", "stable", "Hot, dry season typical of San Juan; concentrated wines with high natural alcohol and deep colour.")
VIN(r4, 2021, "very_good", "rising", "Slightly cooler than average; wines show better balance and more aromatic freshness than prior years.")
VIN(r4, 2020, "good", "stable", "Classic San Juan vintage: powerful, full-bodied reds with ripe tannins.")
VIN(r4, 2019, "excellent", "rising", "Exceptional diurnal variation preserved freshness; standout year for San Juan Syrah.")
VIN(r4, 2018, "good", "stable", "Reliable production year; expressive Bonarda with plum and violet notes.")

p4a = P("Finca Las Moras", "winery", r4, "Argentina",
    production_philosophy="terroir_expression",
    philosophy_description="Leading San Juan estate producing expressive Syrah and Bonarda from high-altitude vineyards with intense solar radiation.",
    reputation_narrative="Finca Las Moras has been instrumental in demonstrating San Juan's potential for quality red wines beyond bulk production.",
    price_positioning="value")
prod4a, new4a = PROD("Finca Las Moras Intis Syrah", "wine_still", p4a, r4, "Argentina",
    subcategory="Syrah",
    description="Bold San Juan Syrah with dark berry, cracked pepper, smoked meat and violet; full-bodied with ripe, velvety tannins.",
    price_tier="value")
if new4a:
    PAIR(prod4a, "BBQ pork ribs with smoky chipotle glaze", "complement", "classic", "main", "Smoked meat in wine mirrors the charred ribs; pepper cuts through sweet glaze.")
    PAIR(prod4a, "Lamb merguez sausage with harissa and flatbread", "complement", "established", "main", "Spiced lamb amplifies the peppery Syrah; harissa heat is balanced by fruit weight.")
    PAIR(prod4a, "Grilled aubergine with pomegranate molasses", "bridge", "suggested", "main", "Smoky aubergine echoes wine's dark fruit; molasses adds sweet-tart contrast.")
    PAIR(prod4a, "Manchego with smoked paprika crackers", "complement", "suggested", "cheese", "Smoked paprika aligns with Syrah's pepper and dark berry character.")

p4b = P("Santiago Graffigna", "winery", r4, "Argentina",
    production_philosophy="traditional",
    philosophy_description="One of San Juan's oldest estates, blending traditional production with modern quality focus on Bonarda and Malbec.",
    reputation_narrative="Graffigna's Centenario range offers accessible, characterful San Juan reds with a strong track record for value.",
    price_positioning="value")
prod4b, new4b = PROD("Graffigna Centenario Bonarda", "wine_still", p4b, r4, "Argentina",
    subcategory="Bonarda",
    description="Juicy San Juan Bonarda with plum, violet, dark chocolate and spice; medium-bodied with velvety tannins and lively acidity.",
    price_tier="value")
if new4b:
    PAIR(prod4b, "Beef empanadas with olives and hard-boiled egg", "complement", "classic", "starter", "Savoury beef and olives echo Bonarda's earthy dark fruit; a classic Argentine pairing.")
    PAIR(prod4b, "Grilled chorizo with chimichurri", "complement", "established", "main", "Spiced pork sausage and herbal chimichurri align with Bonarda's juicy fruit and violet notes.")
    PAIR(prod4b, "Mushroom and thyme flatbread", "bridge", "suggested", "casual", "Earthy mushroom resonates with Bonarda's dark spice; thyme bridges the herbal quality.")
    PAIR(prod4b, "Milk chocolate and hazelnut dessert", "complement", "suggested", "dessert", "The wine's violet and chocolate notes mirror the dessert's profile exactly.")

# ── Region 5: Cafayate ────────────────────────────────────────────────────────
print("\n=== Region 5: Cafayate ===")
r5 = R("Cafayate", "Argentina", "wine",
    designation_type="DO",
    designation_name="Cafayate DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Remote high-altitude valley in Salta province at 1,700–2,200m, producing Argentina's finest Torrontés and expressive high-altitude Malbec with singular aromatic intensity.",
    key_producers="Bodega Colomé, El Esteco, Achaval-Ferrer, Etchart, El Porvenir de Los Andes",
    historical_context="Cafayate's extreme altitude and desert conditions produce some of the world's most aromatic whites; Torrontés here is Argentina's most distinctive native grape expression."
)
VIN(r5, 2022, "excellent", "rising", "Excellent growing season at altitude; Torrontés shows brilliant aromatic purity and freshness.")
VIN(r5, 2021, "very_good", "stable", "Good balance between aromatic intensity and acidity; clean, expressive wines.")
VIN(r5, 2020, "good", "stable", "Consistent quality; Malbec shows elegant structure from high-altitude UV exposure.")
VIN(r5, 2019, "exceptional", "rising", "Near-perfect altitude vintage; Torrontés of extraordinary aromatic precision and acidity.")
VIN(r5, 2018, "very_good", "stable", "Classic Cafayate profile: intense aromatics and firm backbone in both reds and whites.")

p5a = P("El Esteco", "winery", r5, "Argentina",
    production_philosophy="terroir_expression",
    philosophy_description="Historic Cafayate estate dating to 1892, producing benchmark high-altitude Torrontés and Malbec with Andean terroir as the defining factor.",
    reputation_narrative="El Esteco's Don David Torrontés is the reference wine for Argentine Torrontés, combining floral intensity with genuine vinous structure.",
    price_positioning="mid_range")
prod5a, new5a = PROD("El Esteco Don David Torrontés", "wine_still", p5a, r5, "Argentina",
    subcategory="Torrontés",
    description="Benchmark Cafayate Torrontés: explosive rose, jasmine, white peach and apricot aromatics with bright acidity and a crisp, dry finish.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Prawn ceviche with lime and rocoto chilli", "complement", "classic", "starter", "Floral Torrontés lifts the prawn's sweetness; lime and chilli balance the aromatic intensity.")
    PAIR(prod5a, "Tandoori chicken with mango raita", "bridge", "established", "main", "Spice and fruit in the dish match the wine's aromatic exuberance; raita cools both.")
    PAIR(prod5a, "Spiced vegetable pakora with tamarind chutney", "complement", "suggested", "starter", "Aromatic spices in the fritter resonate with Torrontés's floral top notes.")
    PAIR(prod5a, "Apricot and almond tart", "complement", "suggested", "dessert", "Stone fruit in the wine mirrors the apricot filling; almond grounds floral intensity.")

p5b = P("Bodega Colomé", "winery", r5, "Argentina",
    production_philosophy="biodynamic",
    philosophy_description="Hess Family-owned historic estate at 2,200m+, biodynamically farmed, producing some of the world's highest-altitude wines including legendary Malbec and singular Torrontés.",
    reputation_narrative="Colomé's Estate Malbec and Auténtico are globally recognised as benchmarks for extreme-altitude Argentine winemaking.",
    price_positioning="premium")
prod5b, new5b = PROD("Colomé Estate Malbec", "wine_still", p5b, r5, "Argentina",
    subcategory="Malbec",
    description="Extreme high-altitude Malbec (2,200m) with violet, blueberry, graphite and dried lavender; elegant, silky and distinctly Andean in character.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Slow-roasted lamb with cumin and coriander", "complement", "classic", "main", "The lamb's spiced richness finds its equal in Colomé's violet-edged, silky Malbec.")
    PAIR(prod5b, "Llama asado with Andean herbs (or venison substitute)", "complement", "adventurous", "main", "High-altitude terroir pairing: Andean protein with Andean wine, herb and altitude in harmony.")
    PAIR(prod5b, "Wild mushroom and truffle polenta", "bridge", "established", "main", "Earthy mushroom and truffle draw out the graphite and floral notes in extreme-altitude Malbec.")
    PAIR(prod5b, "Dark plum and rose tart", "complement", "suggested", "dessert", "The wine's plum and violet mirror the dessert's flavour profile almost exactly.")

# ── Final count ───────────────────────────────────────────────────────────────
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
