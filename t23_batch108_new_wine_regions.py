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

# ── REGION 1: Txakoli de Álava (Arabako Txakolina) ─────────────────────────
print("=== Region 1: Txakoli de Álava ===")
r1 = R("Txakoli de Álava", "Spain", "wine",
        designation_type="DO", designation_name="Arabako Txakolina DO",
        reputation_tier="emerging",
        quality_trajectory="ascending",
        description="Inland Basque Txakoli from the Álava province; broader and rounder than coastal Bizkaiko Txakolina with slightly more body; primarily Hondarrabi Zuri with hints of Gross Manseng.",
        key_producers="Bodegas Señorío de Astobiza, Bodega Batán de Salas",
        historical_context="Smallest of the three Txakoli DOs; revived from near-extinction in the 1990s; Álava's continental microclimate gives more ripeness than coastal counterparts.")
VIN(r1, 2022, "very_good", "stable", "Warmer summer; rounder and more generous than typical; excellent Txakoli year.")
VIN(r1, 2021, "good", "stable", "Spring rains followed by dry summer; fresh and crisp with good acidity.")
VIN(r1, 2020, "excellent", "rising", "Outstanding vintage; concentration and aromatics both exceptional.")
VIN(r1, 2019, "very_good", "stable", "Ripe and expressive; good fruit weight balances natural tartness.")
VIN(r1, 2018, "good", "stable", "Typical vintage; light and sprightly with characteristic fizz.")
p1a = P("Señorío de Astobiza", "winery", r1, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Álava Txakoli estate producing broader, more structured expressions from continental inland soils.",
        reputation_narrative="Most decorated producer of Arabako Txakolina; earns consistent critical attention for broadening Txakoli's typicity.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Bodega Batán de Salas", "winery", r1, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Small family estate focused on traditional Hondarrabi Zuri from historic vineyards near Moreda de Álava.",
        reputation_narrative="Artisanal producer respected for honest, site-expressive Txakoli; found in Basque specialist lists.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Señorío de Astobiza Arabako Txakolina Blanco", "wine_still", p1a, r1, "Spain",
                  subcategory="Hondarrabi Zuri",
                  description="Rounder, more structured Txakoli with white peach, citrus zest and a lively natural pétillance; slightly longer finish than coastal styles.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Pintxos de anchoa con pimiento", "complement", "classic", "aperitif", "Anchovy salt and pepper heat are cut by Txakoli's tartness; classic Basque aperitif match.")
    PAIR(pr1a, "Grilled bacalao with pil-pil sauce", "complement", "classic", "fish_course", "Salt cod and Txakoli is a Basque canonical pairing; pil-pil emulsion balanced by acidity.")
    PAIR(pr1a, "Fried squid with aioli", "complement", "established", "starter", "Fried seafood lifted by sprightly acidity; aioli garlic softened by fruit freshness.")
    PAIR(pr1a, "Gambas al ajillo", "complement", "classic", "starter", "Garlic prawns and briny Txakoli; a natural Basque tapas pairing.")
pr1b, n1b = PROD("Bodega Batán de Salas Txakoli de Álava", "wine_still", p1b, r1, "Spain",
                  subcategory="Hondarrabi Zuri",
                  description="Artisanal Txakoli with citrus and green apple freshness; light and vibrant with characteristic spritz.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Oysters on the half shell", "complement", "classic", "starter", "Briny oysters amplified by Txakoli's natural salinity; acidity replaces lemon.")
    PAIR(pr1b, "Marinated anchovies (boquerones)", "complement", "classic", "aperitif", "Vinegar-marinated anchovies echo Txakoli's tartness; essential Basque combination.")
    PAIR(pr1b, "Crab croquettes with lemon mayo", "complement", "established", "starter", "Crispy crab richness cut by sprightly Txakoli; lemon mayo bridges citrus notes.")
    PAIR(pr1b, "Clam and white bean stew", "complement", "established", "main", "Briny clams and earthy beans find balance in Txakoli's freshness; coastal inland harmony.")

# ── REGION 2: Txakoli de Getaria (Getariako Txakolina) ─────────────────────
print("=== Region 2: Txakoli de Getaria ===")
r2 = R("Txakoli de Getaria", "Spain", "wine",
        designation_type="DO", designation_name="Getariako Txakolina DO",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Original coastal Basque Txakoli DO from the fishing village of Getaria; the most internationally recognised style — intensely salty, ultra-tart and spritz-filled; pure Hondarrabi Zuri.",
        key_producers="Txomin Etxaniz, Ameztoi",
        historical_context="Getaria is Txakoli's spiritual home; the wine historically drunk from height to create froth; Txomin Etxaniz established the modern benchmark; exports grew dramatically post-2000.")
VIN(r2, 2022, "very_good", "stable", "Sea-cooled summer with perfect balance of ripeness and acidity; exceptional purity.")
VIN(r2, 2021, "good", "stable", "Challenging spring; surviving wines lean and mineral with great freshness.")
VIN(r2, 2020, "excellent", "rising", "Best vintage in a decade; aromatic intensity and salinity both outstanding.")
VIN(r2, 2019, "very_good", "stable", "Classic coastal expression; crisp with green apple and brine.")
VIN(r2, 2018, "good", "stable", "Early harvest due to heat; wines lighter but appealing for immediate drinking.")
p2a = P("Txomin Etxaniz", "winery", r2, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Benchmark Getariako Txakolina producer working historic coastal vineyards to create the definitive salty, spritz expression.",
        reputation_narrative="Widely considered the definitive Txakoli producer; found in top restaurants across Spain and globally.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Ameztoi", "winery", r2, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-generational Getaria estate producing traditional Txakoli with emphasis on sea-influenced terroir and natural fermentation character.",
        reputation_narrative="Highly regarded alongside Txomin Etxaniz as the appellation's two leading names; also produces an acclaimed rosado.",
        price_positioning="mid_range",
        authority_tier=2)
pr2a, n2a = PROD("Txomin Etxaniz Getariako Txakolina", "wine_still", p2a, r2, "Spain",
                  subcategory="Hondarrabi Zuri",
                  description="Benchmark coastal Txakoli with intense marine salinity, green apple, citrus peel and effervescent spritz; thrillingly tart and refreshing.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Fresh anchovies with olive oil", "complement", "classic", "aperitif", "Maritime anchovies and maritime wine; salinity doubles and acidity cuts through oil perfectly.")
    PAIR(pr2a, "Steamed mussels with white wine", "complement", "classic", "starter", "Briny mussels love briny Txakoli; the wine's spritz adds festive lightness.")
    PAIR(pr2a, "Merluza en salsa verde", "complement", "classic", "fish_course", "Basque hake in green sauce is the canonical Txakoli pairing; herb-parsley sauce bridges.")
    PAIR(pr2a, "Squid ink rice (arroz negro)", "bridge", "established", "main", "Txakoli's salinity bridges the sea flavours; acidity cuts through the rich ink sauce.")
pr2b, n2b = PROD("Ameztoi Getariako Txakolina Rubentis Rosado", "wine_still", p2b, r2, "Spain",
                  subcategory="Hondarrabi Beltza",
                  description="Distinctive copper-pink rosado from red-skin Hondarrabi Beltza; floral, strawberry and saline with the appellation's characteristic pétillance.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Grilled octopus with pimentón", "complement", "established", "starter", "Smoked paprika and octopus sweetness complemented by rosado's floral salinity.")
    PAIR(pr2b, "Grilled red tuna with sea salt", "complement", "classic", "fish_course", "Tuna's meaty character needs a rosé with backbone; Ameztoi's salt and fruit deliver.")
    PAIR(pr2b, "Crab salad with citrus vinaigrette", "complement", "established", "starter", "Delicate crab sweetness lifted by rosado freshness; citrus vinaigrette echoes wine's tartness.")
    PAIR(pr2b, "Charcoal-grilled sea bream (dorada)", "complement", "classic", "fish_course", "Classic Basque coastal preparation; the wine's salinity mirrors the sea and char.")

# ── REGION 3: Ribeiro ───────────────────────────────────────────────────────
print("=== Region 3: Ribeiro ===")
r3 = R("Ribeiro", "Spain", "wine",
        designation_type="DO", designation_name="Ribeiro DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Galician appellation in the Miño valley producing whites from Treixadura, Loureira and Torrontés blends; mineral-driven, aromatic and medium-bodied — Galicia's overlooked alternative to Rías Baixas.",
        key_producers="Coto de Gomariz, Viña Mein",
        historical_context="Historic Galician wine centre pre-dating Rías Baixas fame; Ribeiro wines once served at Spanish royal court; revival led by focus on indigenous varieties and old vines.")
VIN(r3, 2022, "very_good", "stable", "Atlantic-influenced vintage; whites show precise aromatics and minerality.")
VIN(r3, 2021, "good", "stable", "Cool and wet spring; wines lean and aromatic with refreshing acidity.")
VIN(r3, 2020, "excellent", "rising", "Outstanding vintage for Ribeiro whites; depth and texture both impressive.")
VIN(r3, 2019, "very_good", "stable", "Ripe and expressive; Treixadura shows tropical notes balanced by mineral finish.")
VIN(r3, 2018, "good", "stable", "Warm vintage; generous fruit but slightly less acidity than ideal.")
p3a = P("Coto de Gomariz", "winery", r3, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Ribeiro estate working granite and schist soils to produce complex, age-worthy white and red wines from indigenous Galician varieties.",
        reputation_narrative="The most internationally recognised Ribeiro producer; earns consistent top scores in Spanish wine media.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Viña Mein", "winery", r3, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Estate-grown Ribeiro whites emphasising Treixadura and Loureira from old vines on granitic slopes above the Avia river.",
        reputation_narrative="Respected for consistent quality and strong aromatic expression; widely available in Spanish restaurant wine lists.",
        price_positioning="mid_range",
        authority_tier=1)
pr3a, n3a = PROD("Coto de Gomariz Ribeiro Blanco", "wine_still", p3a, r3, "Spain",
                  subcategory="Treixadura blend",
                  description="Aromatic Galician white from Treixadura, Loureira and Torrontés; citrus blossom, stone fruit and a distinctive mineral granite finish.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Pulpo a la gallega (Galician octopus)", "complement", "classic", "starter", "Canonical Galician pairing; paprika-dressed octopus perfectly matched by regional white.")
    PAIR(pr3a, "Grilled percebes (barnacles)", "complement", "classic", "starter", "Intensely briny barnacles need an equally mineral, aromatic white; Ribeiro is ideal.")
    PAIR(pr3a, "Steamed clams with white wine and garlic", "complement", "classic", "starter", "Clam broth and Ribeiro share mineral salinity; garlic and citrus create harmony.")
    PAIR(pr3a, "Bacalao al pil-pil", "complement", "established", "fish_course", "Salt cod and Galician white is a natural Iberian pairing; mineral wine cuts emulsified oil.")
pr3b, n3b = PROD("Viña Mein Ribeiro Blanco", "wine_still", p3b, r3, "Spain",
                  subcategory="Treixadura blend",
                  description="Elegant Ribeiro white with jasmine, white peach and citrus notes; medium-bodied with good structure and persistent minerality.",
                  price_tier="mid_range")
if n3b:
    PAIR(pr3b, "Empanada gallega de atún", "complement", "established", "casual", "Galician tuna pastry matched by local wine; a traditional regional combination.")
    PAIR(pr3b, "Grilled razor clams with lemon", "complement", "classic", "starter", "Delicate clam sweetness amplified by Ribeiro's aromatics; lemon bridges acidity.")
    PAIR(pr3b, "White asparagus with romesco sauce", "complement", "established", "starter", "Asparagus sweetness meets Ribeiro florality; nutty romesco links to wine's stone fruit.")
    PAIR(pr3b, "Turbot on the bone with potatoes", "complement", "classic", "fish_course", "Noble flat fish deserves a noble Galician white; mineral finish and fish sweetness in harmony.")

# ── REGION 4: Valdeorras ────────────────────────────────────────────────────
print("=== Region 4: Valdeorras ===")
r4 = R("Valdeorras", "Spain", "wine",
        designation_type="DO", designation_name="Valdeorras DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Eastern Galician appellation in the Sil river valley producing Godello whites of exceptional complexity and age-worthiness; also notable Mencía reds from schist and slate soils.",
        key_producers="Rafael Palacios, Godeval",
        historical_context="Valdeorras was the birthplace of the Godello renaissance; Rafael Palacios revived the region's top crus in the 2000s, establishing it as Spain's finest Godello source.")
VIN(r4, 2022, "excellent", "rising", "Exceptional Godello vintage; concentration and mineral precision both outstanding.")
VIN(r4, 2021, "very_good", "stable", "Atlantic cooling; Godello shows aromatic intensity and fine acidity.")
VIN(r4, 2020, "excellent", "rising", "One of the decade's defining Galician vintages; age-worthy whites and reds.")
VIN(r4, 2019, "very_good", "stable", "Warm and generous; Godello shows tropical richness alongside slate minerality.")
VIN(r4, 2018, "good", "stable", "Good rather than great; Godello lacked typical freshness but pleasant drinking.")
p4a = P("Rafael Palacios", "winery", r4, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Master winemaker Rafael Palacios (brother of Álvaro) produces single-vineyard Godello from ancient slate terraces above the Sil; established Valdeorras as world-class white wine territory.",
        reputation_narrative="Spain's most celebrated Godello producer; As Sortes cru ranks among Spain's greatest whites.",
        price_positioning="premium",
        authority_tier=2)
p4b = P("Godeval", "winery", r4, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Valdeorras producer credited with rescuing the Godello grape from near-extinction in the 1970s; estate vineyards on original slate slopes.",
        reputation_narrative="Pioneer of modern Godello revival; wines are benchmarks for the variety's mineral precision.",
        price_positioning="mid_range",
        authority_tier=2)
pr4a, n4a = PROD("Rafael Palacios As Sortes Val do Bibei Godello", "wine_still", p4a, r4, "Spain",
                  subcategory="Godello",
                  description="Single-vineyard Godello from ancient schist terraces; extraordinary complexity of mineral, smoke, white flowers and citrus with weight and persistence rarely found in Spain.",
                  price_tier="premium")
if n4a:
    PAIR(pr4a, "Lobster with drawn butter", "complement", "classic", "fish_course", "Great Godello matches great shellfish; mineral complexity meets lobster sweetness.")
    PAIR(pr4a, "Turbot with roasted garlic and herbs", "complement", "established", "fish_course", "Noble flat fish deserves Spain's finest white; weight and persistence match turbot's richness.")
    PAIR(pr4a, "Roasted white asparagus with Ibérico fat", "complement", "established", "starter", "Asparagus bitterness and Ibérico richness need a white with texture; Godello delivers.")
    PAIR(pr4a, "Aged Tetilla cheese", "complement", "classic", "cheese", "Galician cow's milk cheese and local Godello; cream and mineral in natural balance.")
pr4b, n4b = PROD("Godeval Valdeorras Godello", "wine_still", p4b, r4, "Spain",
                  subcategory="Godello",
                  description="Estate Godello from original revival vineyards; citrus, apricot, fennel and a distinctive slate mineral finish; medium-bodied with good length.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Grilled sardines with lemon and herbs", "complement", "established", "fish_course", "Sardine oiliness balanced by Godello's citrus acidity and mineral freshness.")
    PAIR(pr4b, "Pulpo a la gallega", "complement", "classic", "starter", "Canonical Galician octopus pairing; paprika-herb dressing matched by white wine's aromatics.")
    PAIR(pr4b, "Clam chowder Galicia-style", "complement", "established", "starter", "Creamy clam broth finds balance in Godello's weight and acidity.")
    PAIR(pr4b, "Roasted chicken with Padrón peppers", "complement", "established", "main", "Simple roast poultry lifted by Godello's aromatic complexity; pepper heat balanced by fruit.")

# ── REGION 5: Monterrei ─────────────────────────────────────────────────────
print("=== Region 5: Monterrei ===")
r5 = R("Monterrei", "Spain", "wine",
        designation_type="DO", designation_name="Monterrei DO",
        reputation_tier="emerging",
        quality_trajectory="ascending",
        description="Southernmost Galician appellation on the Portuguese border; continental climate moderates Atlantic influence producing fuller-bodied Godello whites and Mencía reds with more ripeness than coastal Galicia.",
        key_producers="Quinta da Muradella, Gargalo",
        historical_context="Revived from near-obscurity in the 1990s; Monterrei's warmer, drier conditions produce the most structured Galician whites; proximity to Trás-os-Montes adds Iberian personality.")
VIN(r5, 2022, "very_good", "stable", "Continental warmth; fuller-bodied Godello with excellent ripeness and structure.")
VIN(r5, 2021, "good", "stable", "Cooler year; whites more aromatic and less textured than usual but elegant.")
VIN(r5, 2020, "excellent", "rising", "Outstanding vintage; concentration and complexity rival Valdeorras.")
VIN(r5, 2019, "very_good", "stable", "Warm and generous; Godello shows tropical weight balanced by mineral finish.")
VIN(r5, 2018, "good", "stable", "Good drinking vintage; accessible and ripe but less complexity than top years.")
p5a = P("Quinta da Muradella", "winery", r5, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Pioneer of Monterrei quality producing single-vineyard whites and reds from ancient terraced vineyards on granite and schist near the Portuguese border.",
        reputation_narrative="The reference producer for Monterrei excellence; earned national attention for complex, structured Godello.",
        price_positioning="premium",
        authority_tier=2)
p5b = P("Gargalo", "winery", r5, "Spain",
        production_philosophy="terroir_expression",
        philosophy_description="Modern Monterrei winery focused on expressing the appellation's distinctive continental character through Godello, Treixadura and Mencía.",
        reputation_narrative="Strong presence in Spanish restaurant wine lists; Monterrei's most commercially visible producer.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Quinta da Muradella Monterrei Gorvia Branco", "wine_still", p5a, r5, "Spain",
                  subcategory="Godello blend",
                  description="Single-vineyard Monterrei white from Godello, Treixadura and Doña Blanca; rich, textured and complex with stone fruit, fennel and granite mineral.",
                  price_tier="premium")
if n5a:
    PAIR(pr5a, "Suckling pig roast (cochinillo)", "complement", "established", "main", "Rich roast pork needs a full-bodied Galician white; Muradella's texture matches the fat.")
    PAIR(pr5a, "Confit duck leg with turnip greens", "complement", "suggested", "main", "Duck richness complemented by Godello's weight; bitter greens bridge wine's freshness.")
    PAIR(pr5a, "Aged Manchego with quince paste", "complement", "established", "cheese", "Rich aged cheese balanced by structured Godello; quince sweetness links to wine's stone fruit.")
    PAIR(pr5a, "White bean and chorizo stew", "bridge", "established", "main", "Hearty Galician stew met by substantial Godello; fruit bridges smoky paprika.")
pr5b, n5b = PROD("Gargalo Monterrei Blanco Treixadura", "wine_still", p5b, r5, "Spain",
                  subcategory="Treixadura",
                  description="Aromatic Monterrei white from Treixadura; floral, stone fruit and herb notes with a fuller body than coastal Galician whites.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Grilled dorada (sea bream) with herbs", "complement", "established", "fish_course", "Delicate grilled fish lifted by Treixadura's aromatics; herb garnish bridges.")
    PAIR(pr5b, "Galician caldo with grelos (turnip broth)", "complement", "classic", "casual", "Regional soup and regional wine; the white's floral character softens the bitter greens.")
    PAIR(pr5b, "Empanada de berberechos (cockle pie)", "complement", "established", "casual", "Traditional Galician pastry and local white; cockle brine amplified by mineral finish.")
    PAIR(pr5b, "Roasted red peppers with Ibérico ham", "complement", "established", "starter", "Sweet pepper and cured meat sweetness matched by Treixadura's fruit and body.")

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
