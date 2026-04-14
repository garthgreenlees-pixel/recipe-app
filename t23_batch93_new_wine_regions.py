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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
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

# ── Region 1: Grüner Veltliner heartland ─────────────────────────────────────
print("=== Region 1: Kremstal ===")
r = R("Kremstal", "Austria", "wine",
      designation_type="DAC", designation_name="Kremstal DAC",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Danube-carved valley producing Austria's most mineral Grüner Veltliner and Riesling; loess and primary rock soils yield wines of precision and length.",
      key_producers="Nikolaihof, Salomon Undhof, Stadt Krems",
      historical_context="Ancient wine culture dating to Roman times; Benedictine monastery Göttweig looms above the valley.")
VIN(r, 2022, "excellent", "rising", "Cool, long growing season; bright acidity and pure fruit expression.")
VIN(r, 2021, "very_good", "stable", "Moderate summer; well-structured wines with classic mineral finish.")
VIN(r, 2020, "excellent", "stable", "Ideal ripeness; textbook Grüner Veltliner showing white pepper and citrus.")
VIN(r, 2019, "exceptional", "rising", "Warm vintage; concentrated, ageworthy wines of great intensity.")
VIN(r, 2018, "very_good", "stable", "Hot summer balanced by cool nights; aromatic and food-friendly.")
p1 = P("Nikolaihof", "winery", r, "Austria",
       production_philosophy="biodynamic",
       philosophy_description="Austria's first certified biodynamic estate; centuries-old cellar carved from Roman ruins; minimal intervention vinification.",
       reputation_narrative="The spiritual home of Austrian biodynamic viticulture; Riesling Vinothek releases age for decades.",
       price_positioning="premium")
p2 = P("Salomon Undhof", "winery", r, "Austria",
       production_philosophy="sustainable",
       philosophy_description="Family estate with steep Danube terraces; whole-cluster pressing and extended lees contact for complexity.",
       reputation_narrative="Benchmark producer of Kremstal Riesling; wines show laser precision and mineral drive.",
       price_positioning="mid_range")
pr1, n1 = PROD("Nikolaihof Kremstal Riesling Vinothek", "wine_still", p1, r, "Austria",
               subcategory="Riesling", price_tier="premium",
               description="Barrel-aged Riesling released only after years in the ancient cellar; stony minerality, honeyed complexity and extraordinary length.")
if n1:
    PAIR(pr1, "River trout meunière with capers and lemon", "complement", "classic", "fish_course", "Mineral-citrus resonance; acidity cuts butter and amplifies delicate fish flavour.")
    PAIR(pr1, "White asparagus with hollandaise", "complement", "established", "starter", "Classic Austrian pairing; wine's steely backbone tempers the rich sauce.")
    PAIR(pr1, "Aged Gruyère with honey", "bridge", "suggested", "cheese", "Oxidative notes in aged wine echo nutty cheese; honey mediates sweetness.")
    PAIR(pr1, "Spiced langoustine bisque", "elevate", "adventurous", "starter", "Aged Riesling complexity lifts spiced bisque; mineral finish cleanses richness.")
pr2, n2 = PROD("Salomon Undhof Kögl Riesling", "wine_still", p2, r, "Austria",
               subcategory="Riesling", price_tier="mid_range",
               description="Single-vineyard Riesling from loess-over-gneiss; citrus blossom, slate minerality and rapier-sharp acidity.")
if n2:
    PAIR(pr2, "Freshwater crayfish with dill cream", "complement", "classic", "fish_course", "Mineral acidity and citrus notes echo crayfish sweetness; dill bridges herbal register.")
    PAIR(pr2, "Smoked salmon blinis with crème fraîche", "complement", "established", "starter", "Steely Riesling cuts smoke and richness; citrus lifts delicate salmon.")
    PAIR(pr2, "Veal medallions with morel cream sauce", "bridge", "suggested", "main", "Stone-fruit mid-palate bridges mushroom umami; acidity refreshes rich veal.")
    PAIR(pr2, "Vietnamese pho with herbs and chilli", "contrast", "adventurous", "main", "Bright acidity and citrus contrast rich broth; mineral finish counters chilli heat.")

# ── Region 2: Ribera del Duero ───────────────────────────────────────────────
print("=== Region 2: Ribera del Duero ===")
r = R("Ribera del Duero", "Spain", "wine",
      designation_type="DO", designation_name="Ribera del Duero DO",
      reputation_tier="prestigious", quality_trajectory="established",
      description="High-altitude Castilian plateau producing Spain's most prestigious Tempranillo (Tinto Fino); extreme continental climate yields structured, age-worthy reds.",
      key_producers="Vega Sicilia, Pingus, Pesquera, Emilio Moro",
      historical_context="Modern appellation since 1982; Vega Sicilia established its international reputation decades earlier.")
VIN(r, 2022, "very_good", "stable", "Balanced year with good natural acidity; elegant, approachable style.")
VIN(r, 2021, "excellent", "rising", "Classic cool year; structured wines with fine tannins and excellent aging potential.")
VIN(r, 2020, "exceptional", "rising", "Perfect ripeness with preserved freshness; benchmark vintage for the DO.")
VIN(r, 2019, "excellent", "stable", "Warm but not excessive; concentrated reds with plush tannins.")
VIN(r, 2018, "very_good", "stable", "Variable but top producers excelled; freshness and depth in equal measure.")
p1 = P("Emilio Moro", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Family estate with 100-year-old Tinto Fino vines; gravity-fed cellar; minimal filtration to preserve vineyard character.",
       reputation_narrative="Benchmark Ribera producer with extraordinary old-vine holdings; consistently over-delivers at every price point.",
       price_positioning="mid_range")
p2 = P("Bodegas Pesquera", "winery", r, "Spain",
       production_philosophy="traditional",
       philosophy_description="Pioneer producer that helped define the modern Ribera style; American oak aging; concentrated, muscular reds.",
       reputation_narrative="Alejandro Fernández put Ribera del Duero on the world map; Pesquera remains the benchmark traditional style.",
       price_positioning="mid_range")
pr1, n1 = PROD("Emilio Moro Ribera del Duero Finca Resalso", "wine_still", p1, r, "Spain",
               subcategory="Tempranillo", price_tier="value",
               description="Entry-level from old vines; deep violet colour, blackberry and spice, soft tannins and excellent value.")
if n1:
    PAIR(pr1, "Roast lamb chops with rosemary and garlic", "complement", "classic", "main", "Tinto Fino mirrors lamb's gamey depth; rosemary bridges herbal spice notes.")
    PAIR(pr1, "Grilled chorizo and Manchego", "complement", "established", "casual", "Spanish regional pairing; smoky fat coats tannins and amplifies fruit.")
    PAIR(pr1, "Braised lentils with smoked paprika", "bridge", "suggested", "main", "Earthiness and spice align; wine's fruit softens lentil austerity.")
    PAIR(pr1, "Mushroom and truffle risotto", "complement", "suggested", "main", "Earthy tannins resonate with truffle; dark fruit elevates umami.")
pr2, n2 = PROD("Pesquera Ribera del Duero Reserva", "wine_still", p2, r, "Spain",
               subcategory="Tempranillo", price_tier="mid_range",
               description="Classic American oak-aged Reserva; vanilla, leather and blackcurrant with firm structure and long finish.")
if n2:
    PAIR(pr2, "Wood-roasted suckling pig with crackling", "complement", "classic", "main", "Regional icon pairing; oak vanilla mirrors pork fat; tannins grip crackling.")
    PAIR(pr2, "Aged Manchego with quince paste", "complement", "established", "cheese", "Firm tannins soften against aged cheese; quince echoes wine's dried-fruit notes.")
    PAIR(pr2, "Venison stew with juniper and red wine", "complement", "established", "main", "Game depth matches wine's structure; juniper bridges aromatic complexity.")
    PAIR(pr2, "Dark chocolate tart with salted caramel", "bridge", "suggested", "dessert", "Oak and vanilla mediate chocolate bitterness; caramel echoes fruit sweetness.")

# ── Region 3: Galicia / Rías Baixas ──────────────────────────────────────────
print("=== Region 3: Rías Baixas ===")
r = R("Rías Baixas", "Spain", "wine",
      designation_type="DO", designation_name="Rías Baixas DO",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Atlantic Galician ría estuary zone; home of Albariño — Spain's most celebrated white grape; saline, citrus-driven, high-acid wines.",
      key_producers="Pazo de Señoráns, Bodegas Fillaboa, Marqués de Riscal (Albariño), Do Ferreiro",
      historical_context="DO status 1988; Albariño's explosive international rise in the 1990s transformed Spanish white wine's reputation.")
VIN(r, 2023, "excellent", "rising", "Cool Atlantic season; crystalline acidity and pristine aromatics.")
VIN(r, 2022, "very_good", "stable", "Warmer year; riper Albariño with tropical notes balanced by salinity.")
VIN(r, 2021, "excellent", "stable", "Classic cool year; textbook saline-citrus Rías Baixas profile.")
VIN(r, 2020, "very_good", "stable", "Balanced ripeness; versatile, food-friendly Albariño.")
VIN(r, 2019, "exceptional", "rising", "Exceptional freshness and concentration; top single-vineyard wines will age well.")
p1 = P("Pazo de Señoráns", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Estate from the Salnés subzone; granite-soil Albariño; extended lees aging on Selección de Añada for added complexity.",
       reputation_narrative="Reference producer for age-worthy Albariño; Selección de Añada among Spain's most compelling white wines.",
       price_positioning="mid_range")
p2 = P("Do Ferreiro", "winery", r, "Spain",
       production_philosophy="traditional",
       philosophy_description="Old vine Albariño from centenarian bush vines; low yields; pure expression of Salnés granite terroir.",
       reputation_narrative="Gerardo Méndez crafts benchmark Albariño from the oldest vines in the denomination; cult following worldwide.",
       price_positioning="mid_range")
pr1, n1 = PROD("Pazo de Señoráns Albariño", "wine_still", p1, r, "Spain",
               subcategory="Albariño", price_tier="mid_range",
               description="Estate Albariño; bright citrus, white flower and saline finish; crisp acidity and elegant stone-fruit mid-palate.")
if n1:
    PAIR(pr1, "Steamed mussels with white wine and herbs", "complement", "classic", "starter", "Classic Galician pairing; saline wine mirrors sea-mineral mussel flavour.")
    PAIR(pr1, "Grilled octopus with smoked paprika oil", "complement", "established", "starter", "Albariño's salinity and citrus amplify smoky paprika and tender octopus.")
    PAIR(pr1, "Sea bass ceviche with lime and chilli", "complement", "established", "starter", "Bright acidity echoes citrus marinade; freshness lifts delicate raw fish.")
    PAIR(pr1, "Oysters with mignonette", "complement", "classic", "aperitif", "Saline-mineral resonance; Albariño amplifies oyster's oceanic character.")
pr2, n2 = PROD("Do Ferreiro Cepas Vellas Albariño", "wine_still", p2, r, "Spain",
               subcategory="Albariño", price_tier="premium",
               description="Old-vine Albariño from centenarian granite bush vines; extraordinary depth — stone fruit, white tea, beeswax and sustained mineral salinity.")
if n2:
    PAIR(pr2, "Whole roasted turbot with sea herbs", "complement", "classic", "fish_course", "Old-vine depth matches turbot's richness; salinity and herb notes resonate.")
    PAIR(pr2, "Langoustine thermidor with tarragon butter", "complement", "established", "fish_course", "Beeswax and stone-fruit notes bridge rich butter sauce; acidity refreshes.")
    PAIR(pr2, "Aged Tetilla cheese with membrillo", "bridge", "suggested", "cheese", "Galician regional pairing; saline wine and mild cheese harmonise naturally.")
    PAIR(pr2, "Clam and saffron rice (arroz con almejas)", "complement", "established", "main", "Saffron echoes wine's floral notes; salinity amplifies clam minerality.")

# ── Region 4: Tuscany — Vernaccia di San Gimignano ───────────────────────────
print("=== Region 4: Vernaccia di San Gimignano ===")
r = R("Vernaccia di San Gimignano", "Italy", "wine",
      designation_type="DOCG", designation_name="Vernaccia di San Gimignano DOCG",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Italy's first DOC (1966); medieval tower-town produces distinctive white Vernaccia with bitter almond finish and textured, food-friendly body.",
      key_producers="Panizzi, Teruzzi, San Quirico, Montenidoli",
      historical_context="Dante, Boccaccio and Michelangelo all praised Vernaccia; its terroir is among Tuscany's best-kept secrets for white wine.")
VIN(r, 2023, "very_good", "stable", "Warm year with good acid retention; textured, aromatic Vernaccia.")
VIN(r, 2022, "excellent", "stable", "Balanced ripeness; benchmark bitter-almond and citrus profile.")
VIN(r, 2021, "very_good", "stable", "Fresh, precise year; elegant Vernaccia with bright acidity.")
VIN(r, 2020, "good", "stable", "Heat stress in parts of the zone; top producers delivered clean, focused wines.")
VIN(r, 2019, "excellent", "stable", "Concentrated vintage; Vernaccia Riservas show impressive structure.")
p1 = P("Panizzi", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Hilltop estate above San Gimignano; clay-sand soils; Vernaccia Riserva aged in large oak for added complexity and longevity.",
       reputation_narrative="Standard-bearer for serious Vernaccia; demonstrates the DOCG's potential for age-worthy whites.",
       price_positioning="mid_range")
p2 = P("Montenidoli", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Biodynamic pioneer Elisabetta Fagiuoli; indigenous yeasts; long maceration on skins for Carato Vernaccia; no added sulphur.",
       reputation_narrative="Cult natural producer whose skin-contact Carato Vernaccia redefines the appellation's possibilities.",
       price_positioning="mid_range")
pr1, n1 = PROD("Panizzi Vernaccia di San Gimignano Riserva", "wine_still", p1, r, "Italy",
               subcategory="Vernaccia", price_tier="mid_range",
               description="Oak-aged Riserva; golden colour, hazelnut, almond, white peach and a characteristic bitter finish of remarkable persistence.")
if n1:
    PAIR(pr1, "Florentine bistecca with Tuscan white beans", "contrast", "established", "main", "White wine's almond bitterness cuts through steak fat; bean earthiness grounds the pairing.")
    PAIR(pr1, "Pappardelle with porcini and truffle", "complement", "established", "main", "Oak notes echo mushroom earthiness; bitter-almond finish contrasts truffle richness.")
    PAIR(pr1, "Pecorino Toscano with wildflower honey", "complement", "classic", "cheese", "Regional pairing; bitter almond and sheep's milk cheese create perfect harmony.")
    PAIR(pr1, "Grilled swordfish with capers and olives", "complement", "suggested", "fish_course", "Mediterranean herbs and briny olives resonate with wine's texture and bitter finish.")
pr2, n2 = PROD("Montenidoli Carato Vernaccia", "wine_still", p2, r, "Italy",
               subcategory="Vernaccia", price_tier="mid_range",
               description="Skin-macerated Vernaccia; amber-hued, tannic and complex — dried apricot, beeswax, chamomile and long savory-bitter finish.")
if n2:
    PAIR(pr2, "Pan-roasted calf's liver with sage and onion", "complement", "established", "main", "Tannin and bitterness align with liver's iron notes; sage bridges herbal register.")
    PAIR(pr2, "Charcuterie board with Tuscan salumi", "complement", "classic", "aperitif", "Skin tannins grip cured fat; oxidative notes echo salumi complexity.")
    PAIR(pr2, "Aged Pecorino with black truffle honey", "elevate", "adventurous", "cheese", "Amber wine's grip and complexity elevate aged cheese; truffle honey mediates bitterness.")
    PAIR(pr2, "Tempura vegetables with ponzu", "contrast", "adventurous", "starter", "Textured skin-contact wine contrasts light tempura; bitter finish mirrors ponzu citrus.")

# ── Region 5: Rheingau ───────────────────────────────────────────────────────
print("=== Region 5: Rheingau ===")
r = R("Rheingau", "Germany", "wine",
      designation_type="Einzellage", designation_name="Rheingau",
      reputation_tier="iconic", quality_trajectory="rediscovering",
      description="South-facing bend of the Rhine; birthplace of the Spätlese style; Riesling vineyards include Schloss Johannisberg, Rauenthaler Baiken and Rüdesheimer Berg.",
      key_producers="Weil, Georg Breuer, Leitz, Schloss Johannisberg",
      historical_context="Monks at Johannisberg accidentally discovered botrytis in 1775, creating Spätlese; Rheingau was Germany's most celebrated wine region for two centuries.")
VIN(r, 2021, "exceptional", "rising", "Textbook cool vintage; Riesling of extraordinary precision and aging potential.")
VIN(r, 2020, "excellent", "stable", "Warm year with freshness retained; concentrated, generous Riesling.")
VIN(r, 2019, "excellent", "stable", "Rich, ripe year; Spätlesen and Auslesen of classic richness.")
VIN(r, 2018, "exceptional", "rising", "Legendary vintage; dry Rieslings of rare depth and concentration.")
VIN(r, 2017, "very_good", "stable", "Late frost damage reduced yields but survivors showed impressive intensity.")
p1 = P("Robert Weil", "winery", r, "Germany",
       production_philosophy="traditional",
       philosophy_description="Historic estate revitalised by Japanese investment; Kiedrich Gräfenberg GG flagship; QmP range from Kabinett to Trockenbeerenauslese.",
       reputation_narrative="Rheingau's most celebrated modern estate; Kiedrich Gräfenberg Riesling sets the standard for the region.",
       price_positioning="premium")
p2 = P("Georg Breuer", "winery", r, "Germany",
       production_philosophy="terroir_focused",
       philosophy_description="Pioneer of dry Rheingau Riesling; Rüdesheimer Berg Schlossberg GG showcases basalt-slate minerality; estate-grown only.",
       reputation_narrative="Bernhard Breuer championed dry Rheingau Riesling before it was fashionable; now benchmark for the style.",
       price_positioning="premium")
pr1, n1 = PROD("Robert Weil Kiedrich Gräfenberg Riesling GG", "wine_still", p1, r, "Germany",
               subcategory="Riesling", price_tier="premium",
               description="Grand Cru-equivalent dry Riesling from blue-slate soils; citrus oil, white stone fruit, electrifying acidity and decades of aging potential.")
if n1:
    PAIR(pr1, "Lobster with bisque and tarragon butter", "elevate", "classic", "fish_course", "Grand Cru Riesling elevates lobster; acidity cuts butter richness while citrus mirrors sweetness.")
    PAIR(pr1, "Roasted white asparagus with brown butter", "complement", "classic", "starter", "Classic German pairing; minerality amplifies asparagus; acidity balances butter.")
    PAIR(pr1, "Seared foie gras with Riesling reduction", "complement", "established", "starter", "Wine's vibrant acidity lifts foie richness; citrus notes echo sauce's brightness.")
    PAIR(pr1, "Aged Comté with Alsatian mustard", "bridge", "suggested", "cheese", "Mineral Riesling and nutty cheese align; mustard mediates bitter-citrus notes.")
pr2, n2 = PROD("Georg Breuer Rüdesheimer Berg Schlossberg Riesling", "wine_still", p2, r, "Germany",
               subcategory="Riesling", price_tier="premium",
               description="Basalt-slate GG; smoky, volcanic minerality with lime, grapefruit and a saline-driven finish; dry and austere in youth.")
if n2:
    PAIR(pr2, "Cured trout with cucumber and horseradish", "complement", "established", "starter", "Smoky minerality echoes smoked fish; horseradish bridges acidity and pungency.")
    PAIR(pr2, "Japanese sashimi platter with ponzu", "complement", "suggested", "fish_course", "Volcanic minerality resonates with umami; citrus acidity replaces ponzu's role.")
    PAIR(pr2, "Wiener Schnitzel with potato salad", "complement", "classic", "main", "Classic German pairing; acidity cuts fried breadcrumb fat; citrus brightens veal.")
    PAIR(pr2, "Miso-glazed black cod", "bridge", "adventurous", "fish_course", "Volcanic slate note bridges miso umami; acidity refreshes rich lacquered glaze.")

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
