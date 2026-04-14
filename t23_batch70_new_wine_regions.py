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

# ── Batch 70 ──────────────────────────────────────────────────────────────────
# Regions: Rapel Valley, Colchagua Valley, Limarí Valley, Coastal Region (Chile), Río Negro

# ── Region 1: Rapel Valley ────────────────────────────────────────────────────
print("\n=== Region 1: Rapel Valley ===")
r1 = R("Rapel Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Rapel Valley DO",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Broad central valley zone encompassing Colchagua and Cachapoal, producing full-bodied reds including Carmenère, Merlot and Syrah with rich fruit and velvety texture.",
    key_producers="Viña MontGras, Viña Bisquertt, Viña Anakena",
    historical_context="Rapel Valley was one of Chile's first regions to demonstrate that Carmenère — long confused with Merlot — could produce wines of genuine complexity and identity."
)
VIN(r1, 2021, "very_good", "stable", "Warm, dry season ideal for Carmenère; wines show plum, pepper and silky tannins.")
VIN(r1, 2020, "good", "stable", "Reliable vintage; expressive fruit-forward reds with good approachability.")
VIN(r1, 2019, "excellent", "stable", "Classic Rapel year; Carmenère shows remarkable pepper, dark fruit and integrated acidity.")
VIN(r1, 2018, "very_good", "stable", "Warm growing season; rich, generous wines with early drinking appeal.")
VIN(r1, 2017, "good", "stable", "Consistent quality across the valley; easy-drinking reds with broad commercial appeal.")

p1a = P("Viña MontGras", "winery", r1, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Award-winning Rapel producer specialising in Carmenère with single-estate focus and commitment to Chile's flagship red variety.",
    reputation_narrative="MontGras's Quatro label and estate Carmenère are benchmarks for accessible yet characterful Rapel reds.",
    price_positioning="mid_range")
prod1a, new1a = PROD("MontGras Quatro Cabernet Sauvignon", "wine_still", p1a, r1, "Chile",
    subcategory="Cabernet Sauvignon",
    description="Full-bodied Rapel Cabernet with dark plum, tobacco, cedar and firm tannins; reliable and expressive at accessible price.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Grilled beef burger with aged cheddar and caramelised onion", "complement", "classic", "casual", "Rich Cabernet fruit handles the beef and cheese with ease; caramelised onion bridges sweetness.")
    PAIR(prod1a, "Beef and chorizo stew with smoked paprika", "complement", "established", "main", "Smoked spice echoes the wine's tobacco note; hearty stew matches tannin weight.")
    PAIR(prod1a, "Hard aged cheese board with dried fruit", "complement", "established", "cheese", "Crystalline cheese softens tannin; dried fig and apricot bridge the wine's dark fruit.")
    PAIR(prod1a, "Dark chocolate brownies", "contrast", "suggested", "dessert", "Bitter chocolate amplifies Cabernet's fruit; sweet brownie frames tannic grip.")

p1b = P("Viña Anakena", "winery", r1, "Chile",
    production_philosophy="traditional",
    philosophy_description="Mid-sized Rapel producer focused on Carmenère and Cabernet with strong export track record and consistent quality.",
    reputation_narrative="Anakena's Ona Carmenère is one of Chile's most acclaimed Carmenères at the premium level.",
    price_positioning="premium")
prod1b, new1b = PROD("Anakena Ona Carmenère", "wine_still", p1b, r1, "Chile",
    subcategory="Carmenère",
    description="Premium Rapel Carmenère showing dark plum, green peppercorn, mocha and spice with silky, ripe tannins and lingering finish.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Slow-braised beef short rib with mole sauce", "complement", "classic", "main", "Mole's complexity and richness mirrors the wine's layered dark fruit and spice.")
    PAIR(prod1b, "Duck leg confit with cherry sauce and lentils", "complement", "established", "main", "Gamey duck echoes Carmenère's dark fruit; cherry bridges the wine's plum notes.")
    PAIR(prod1b, "Roasted red pepper and walnut muhammara with flatbread", "bridge", "suggested", "starter", "Red pepper and walnut echo the wine's spiced, earthy character.")
    PAIR(prod1b, "Dark chocolate fondant with raspberry coulis", "complement", "suggested", "dessert", "Berry and chocolate align with Carmenère's signature profile.")

# ── Region 2: Colchagua Valley ────────────────────────────────────────────────
print("\n=== Region 2: Colchagua Valley ===")
r2 = R("Colchagua Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Colchagua Valley DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's premium red wine heartland within Rapel, producing internationally acclaimed Carmenère, Cabernet Sauvignon and Syrah with rich, concentrated flavours and excellent ageing potential.",
    key_producers="Casa Lapostolle, Montes, Viu Manent, Clos Apalta, Luis Felipe Edwards",
    historical_context="Colchagua rose to international fame in the 1990s as Chile's finest red wine zone; home to Clos Apalta, one of South America's most celebrated wines."
)
VIN(r2, 2021, "excellent", "rising", "Outstanding growing conditions; Carmenère and Syrah show superb concentration and freshness.")
VIN(r2, 2020, "very_good", "stable", "Reliable vintage; full-bodied reds with generous fruit and accessible tannins.")
VIN(r2, 2019, "exceptional", "rising", "One of Colchagua's greatest vintages; wines of remarkable structure, depth and longevity.")
VIN(r2, 2018, "very_good", "stable", "Warm season with good balance; powerful, generous reds with medium-term cellaring potential.")
VIN(r2, 2017, "good", "stable", "Consistent quality; approachable reds with good early drinking pleasure.")

p2a = P("Casa Lapostolle", "winery", r2, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="French-owned estate producing Clos Apalta — Chile's most critically acclaimed wine — alongside a premium range focused on Colchagua terroir.",
    reputation_narrative="Clos Apalta consistently scores among the world's top wines; Casa Lapostolle defines Colchagua's ceiling for quality.",
    price_positioning="ultra_premium")
prod2a, new2a = PROD("Clos Apalta", "wine_still", p2a, r2, "Chile",
    subcategory="Carmenère blend",
    description="Chile's most celebrated red: Carmenère-dominant blend with Merlot and Cabernet Franc — complex, velvety, with extraordinary depth and longevity.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Roasted saddle of venison with cherry and chocolate sauce", "complement", "classic", "main", "Game and dark fruit sauce mirror the wine's intensity; chocolate echoes Carmenère's mocha notes.")
    PAIR(prod2a, "Slow-braised wagyu short rib with truffle gremolata", "complement", "classic", "main", "Ultra-premium beef demands equal gravity; truffle aligns with wine's earthy complexity.")
    PAIR(prod2a, "Aged Gouda and black truffle grilled cheese", "bridge", "established", "cheese", "Crystalline cheese fat smooths tannin; truffle amplifies the wine's savoury depth.")
    PAIR(prod2a, "Dark chocolate and plum tart with sea salt", "complement", "suggested", "dessert", "Plum and chocolate align perfectly with Carmenère's signature flavour profile.")

p2b = P("Montes", "winery", r2, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Pioneer Colchagua estate that helped create the premium Chilean wine category; known for Montes Alpha and the iconic Montes Folly Syrah.",
    reputation_narrative="Montes is Chile's most internationally recognised wine brand in the premium segment; Montes Alpha M remains a Colchagua benchmark.",
    price_positioning="premium")
prod2b, new2b = PROD("Montes Alpha M", "wine_still", p2b, r2, "Chile",
    subcategory="Cabernet Sauvignon blend",
    description="Flagship Colchagua blend — Cabernet Sauvignon with Merlot, Cabernet Franc and Carmenère — showing blackcurrant, cedar, violet and silky mountain tannins.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Rack of lamb with garlic, rosemary and Dijon crust", "complement", "classic", "main", "Classic Cabernet pairing; the herb and garlic crust mirrors the wine's aromatic complexity.")
    PAIR(prod2b, "Beef tenderloin medallions with mushroom duxelles", "complement", "classic", "main", "Earthy mushroom resonates with the wine's cedar and tobacco layers.")
    PAIR(prod2b, "Manchego and Idiazábal cheese selection", "complement", "established", "cheese", "Spanish-style cheeses match the estate's wine focus; fat softens Cabernet tannin.")
    PAIR(prod2b, "Bitter orange and dark chocolate mousse", "contrast", "suggested", "dessert", "Orange bitterness amplifies red fruit; chocolate frames the wine's tannic structure.")

# ── Region 3: Limarí Valley ───────────────────────────────────────────────────
print("\n=== Region 3: Limarí Valley ===")
r3 = R("Limarí Valley", "Chile", "wine",
    designation_type="DO",
    designation_name="Limarí Valley DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Arid northern valley at latitude 30°S, producing Chile's most distinctive Chardonnay and Syrah on calcium carbonate-rich limestone soils with strong Pacific influence.",
    key_producers="Tabalí, Concha y Toro (Terrunyo), Casa Tamaya",
    historical_context="Limarí is Chile's most exciting emerging cool-climate region; its limestone soils produce wines with striking minerality that distinguish it from all other Chilean regions."
)
VIN(r3, 2022, "excellent", "rising", "Cool Pacific influence preserved aromatic intensity and acidity; benchmark year for Limarí Chardonnay.")
VIN(r3, 2021, "very_good", "stable", "Good balance with crisp acidity; whites show mineral focus and restraint.")
VIN(r3, 2020, "good", "stable", "Slightly warmer; wines show more rounded texture with good early drinking appeal.")
VIN(r3, 2019, "excellent", "rising", "Outstanding mineral Chardonnay vintage; wines show Chablis-like precision and tension.")
VIN(r3, 2018, "very_good", "stable", "Clean, aromatic season; consistent quality across white varieties.")

p3a = P("Tabalí", "winery", r3, "Chile",
    production_philosophy="terroir_expression",
    philosophy_description="Leading Limarí producer wholly focused on the valley's limestone terroir, producing Chile's most mineral and age-worthy Chardonnay.",
    reputation_narrative="Tabalí's Gran Reserva Chardonnay is consistently ranked among Chile's top whites, demonstrating Limarí's world-class cool-climate credentials.",
    price_positioning="premium")
prod3a, new3a = PROD("Tabalí Gran Reserva Chardonnay", "wine_still", p3a, r3, "Chile",
    subcategory="Chardonnay",
    description="Chile's benchmark cool-climate Chardonnay — limestone minerality, white peach, lemon zest, grilled hazelnut and a long, saline finish.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Grilled lobster with lemon butter and tarragon", "complement", "classic", "main", "Rich crustacean and butter mirror the wine's texture; lemon and tarragon align with its citrus edge.")
    PAIR(prod3a, "Seared scallop with cauliflower and hazelnut", "complement", "classic", "fish_course", "Hazelnut in the wine and dish reinforce each other; cauliflower's earthiness grounds the pairing.")
    PAIR(prod3a, "Poached turbot with beurre blanc and leeks", "complement", "established", "fish_course", "Beurre blanc richness mirrors Chardonnay texture; leek adds subtle sweetness.")
    PAIR(prod3a, "Triple cream brie with brioche", "bridge", "suggested", "cheese", "Creamy cheese fat aligns with the wine's texture; brioche sweetness bridges acidity.")

p3b = P("Casa Tamaya", "winery", r3, "Chile",
    production_philosophy="traditional",
    philosophy_description="Established Limarí producer offering excellent value wines that express the valley's distinctive limestone character.",
    reputation_narrative="Casa Tamaya's Winemaker Reserve Chardonnay offers Limarí's limestone character at accessible prices.",
    price_positioning="value")
prod3b, new3b = PROD("Casa Tamaya Winemaker Reserve Syrah", "wine_still", p3b, r3, "Chile",
    subcategory="Syrah",
    description="Cool-climate Limarí Syrah with dark berry, white pepper, smoked meat and floral violet; medium-bodied with refreshing acidity.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Lamb kebabs with zaatar and yoghurt dip", "complement", "established", "main", "Herb-crusted lamb aligns with cool-climate Syrah's floral and pepper notes.")
    PAIR(prod3b, "Grilled tuna steak with black olive tapenade", "bridge", "adventurous", "fish_course", "Meaty tuna handles the Syrah's weight; olive and pepper bridge the gap between fish and red wine.")
    PAIR(prod3b, "Merguez sausage flatbread with harissa yoghurt", "complement", "suggested", "casual", "Spiced sausage echoes the wine's pepper; harissa heat is balanced by fruit weight.")
    PAIR(prod3b, "Smoked duck breast with cherry compote", "complement", "established", "main", "Smoke and game align with Syrah's dark fruit; cherry bridges the floral note.")

# ── Region 4: Coastal Region (Chile) ──────────────────────────────────────────
print("\n=== Region 4: Coastal Region Chile ===")
r4 = R("Coastal Region", "Chile", "wine",
    designation_type="DO",
    designation_name="Coastal Region DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Cool Pacific coastal zone of Chile encompassing Itata, Bío-Bío and Malleco valleys, known for heritage grape varieties including País, Moscatel and Cinsault grown on granitic soils by small growers.",
    key_producers="De Martino, Garage Wine Co, Louis-Antoine Luyt",
    historical_context="Chile's southern coastal regions are experiencing a renaissance driven by natural wine producers rediscovering century-old dry-farmed País and Cinsault vineyards."
)
VIN(r4, 2022, "excellent", "rising", "Cool, wet season ideal for heritage varieties; País and Cinsault show remarkable freshness and elegance.")
VIN(r4, 2021, "very_good", "stable", "Good vintage; wines show aromatic purity and bright acidity characteristic of the coast.")
VIN(r4, 2020, "good", "stable", "Reliable quality; easy-drinking wines with good fruit expression.")
VIN(r4, 2019, "excellent", "rising", "Benchmark year for coastal heritage varieties; País of extraordinary freshness and depth.")
VIN(r4, 2018, "very_good", "stable", "Consistent quality across all coastal subregions; País and Cinsault show strong identity.")

p4a = P("De Martino", "winery", r4, "Chile",
    production_philosophy="minimal_intervention",
    philosophy_description="Pioneer of the coastal heritage wine movement in Chile, producing old-vine País and Muscat from centenarian dry-farmed vineyards in Itata and Bío-Bío.",
    reputation_narrative="De Martino's Vigno and Itata series redefined the perception of southern Chile, earning international critical acclaim for their purity and distinctiveness.",
    price_positioning="premium")
prod4a, new4a = PROD("De Martino Vigno Carignan", "wine_still", p4a, r4, "Chile",
    subcategory="Carignan",
    description="Old-vine Itata Carignan from dry-farmed centenarian vines — wild herbs, dark cherry, iron and granite minerality with food-friendly acidity.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Grilled pork neck with chimichurri and roasted potato", "complement", "established", "main", "Carignan's acidity cuts through pork fat; herb chimichurri mirrors the wine's wild herb character.")
    PAIR(prod4a, "Octopus a la gallega with paprika and olive oil", "complement", "adventurous", "starter", "Old-vine minerality aligns with coastal octopus; paprika bridges the wine's earthy notes.")
    PAIR(prod4a, "Lentil and merguez stew", "complement", "suggested", "main", "Earthy lentils echo the wine's iron and granite character; sausage spice amplifies dark fruit.")
    PAIR(prod4a, "Aged manchego with quince paste", "bridge", "established", "cheese", "Hard cheese fat softens Carignan's tannin; quince bridges the wine's tart cherry note.")

p4b = P("Garage Wine Co", "winery", r4, "Chile",
    production_philosophy="minimal_intervention",
    philosophy_description="Small-production natural wine producer working with heritage Itata vineyards to produce ultra-authentic País and field blends.",
    reputation_narrative="Garage Wine Co is one of Chile's most critically acclaimed natural wine producers, beloved by sommeliers worldwide for its purity and individuality.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Garage Wine Co Truquilemu País", "wine_still", p4b, r4, "Chile",
    subcategory="País",
    description="Wild, translucent País from century-old Itata vines — dried rose petals, sour cherry, iron, herbs and electric acidity; best served slightly cool.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Charcuterie board with jamón and aged olives", "complement", "established", "starter", "Light-bodied País handles cured pork without overpowering; acidity cuts through fat.")
    PAIR(prod4b, "Roasted whole chicken with garlic and lemon", "complement", "classic", "main", "Heritage variety's earthy freshness is the classic match for simple roast chicken.")
    PAIR(prod4b, "Tomato and anchovy bruschetta", "bridge", "suggested", "amuse", "País's iron and acidity echo anchovy's umami; tomato's acidity bridges the wine's tartness.")
    PAIR(prod4b, "Fresh goat's cheese with herbs", "complement", "established", "cheese", "Tangy chèvre and País's sour cherry profile are natural companions; herb bridges both.")

# ── Region 5: Río Negro ───────────────────────────────────────────────────────
print("\n=== Region 5: Río Negro ===")
r5 = R("Río Negro", "Argentina", "wine",
    designation_type="IG",
    designation_name="Río Negro IG",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Patagonian wine region in northern Argentina at 39°S, producing elegant cool-climate Pinot Noir, Malbec, Riesling and Sauvignon Blanc with remarkable freshness and aromatic intensity.",
    key_producers="Chacra, Humberto Canale, Noemia de Patagonia",
    historical_context="Río Negro is Argentina's coolest wine region, pioneered by Humberto Canale and transformed by Piero Incisa della Rocchetta's Chacra project into a Burgundy-inspired Pinot Noir destination."
)
VIN(r5, 2022, "excellent", "rising", "Cool Patagonian season; Pinot Noir shows remarkable aromatic delicacy and Burgundian elegance.")
VIN(r5, 2021, "very_good", "stable", "Consistent quality; wines show freshness and definition typical of the region's cool climate.")
VIN(r5, 2020, "good", "stable", "Reliable vintage; approachable wines with good aromatic expression.")
VIN(r5, 2019, "exceptional", "rising", "Benchmark Río Negro vintage; Pinot Noir of extraordinary delicacy and longevity.")
VIN(r5, 2018, "very_good", "stable", "Good growing season; elegant wines with Burgundian-influenced restraint.")

p5a = P("Bodega Chacra", "winery", r5, "Argentina",
    production_philosophy="biodynamic",
    philosophy_description="Piero Incisa della Rocchetta's Patagonian estate producing Argentina's most elegant Pinot Noir from centenarian ungrafted vines, biodynamically farmed.",
    reputation_narrative="Chacra is globally recognised as one of the New World's great Pinot Noir producers; Treinta y Dos (planted 1932) is considered Argentina's finest Pinot Noir.",
    price_positioning="ultra_premium")
prod5a, new5a = PROD("Chacra Treinta y Dos Pinot Noir", "wine_still", p5a, r5, "Argentina",
    subcategory="Pinot Noir",
    description="Argentina's greatest Pinot Noir from ungrafted 1932-planted vines — transparent, Burgundian in spirit, with dried rose, wild cherry, earth and extraordinary length.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Roasted duck breast with wild cherry sauce", "complement", "classic", "main", "Wild cherry in the wine mirrors the sauce; gamey duck resonates with Pinot's earthy character.")
    PAIR(prod5a, "Pinot Noir-braised mushroom and lentil ragout", "complement", "established", "main", "Earth and umami amplify the wine's forest floor notes; lentil weight matches its body.")
    PAIR(prod5a, "Grilled whole fish with beurre noisette", "bridge", "adventurous", "fish_course", "Delicate Pinot handles rich fish with grace; nutty butter bridges wine's red fruit to seafood.")
    PAIR(prod5a, "Aged Comté with wild honey", "complement", "established", "cheese", "Nutty Comté mirrors the wine's earthy complexity; honey bridges the wine's fruit.")

p5b = P("Noemia de Patagonia", "winery", r5, "Argentina",
    production_philosophy="minimal_intervention",
    philosophy_description="Danish-Italian venture in Río Negro producing elegant, restrained Malbec and Pinot Noir from old Patagonian vines with minimal intervention.",
    reputation_narrative="Noemia A Lisa Malbec is considered one of Argentina's most distinctive and terroir-expressive Malbecs, renowned for its cool-climate elegance.",
    price_positioning="premium")
prod5b, new5b = PROD("Noemia A Lisa Malbec", "wine_still", p5b, r5, "Argentina",
    subcategory="Malbec",
    description="Cool-climate Patagonian Malbec with violet, blueberry, iron, dried herbs and refreshing acidity — the antithesis of Mendoza's power, built for finesse.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Herb-crusted Patagonian lamb chops", "complement", "classic", "main", "Patagonian lamb with Patagonian Malbec is a terroir-driven pairing; herbs mirror the wine's floral note.")
    PAIR(prod5b, "Venison tartare with capers and shallot", "complement", "established", "starter", "Cool-climate Malbec's iron and acidity are ideal for raw game; capers add savoury spark.")
    PAIR(prod5b, "Mushroom and blue cheese risotto", "bridge", "suggested", "main", "Earthy risotto grounds the wine's delicate violet; blue cheese adds a bold counterpoint.")
    PAIR(prod5b, "Grilled duck breast with blueberry reduction", "complement", "established", "main", "Blueberry echoes Malbec's primary fruit; duck's gamey fat is balanced by the wine's cool-climate acidity.")

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
