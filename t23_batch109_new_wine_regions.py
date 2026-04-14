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

# ── REGION 1: Südtirol / Alto Adige Weissburgunder ─────────────────────────
# (Alto Adige already exists — targeting a NEW sub-region: Trentino)
# Targeting fresh NEW regions this batch:
# 1. Teroldego Rotaliano (Italy) 2. Lagrein (Italy sub-variety DO) →
# Instead: Collio, Carso, Isonzo, Friuli Grave, and Friuli Annia

print("=== Region 1: Collio ===")
r1 = R("Collio", "Italy", "wine",
        designation_type="DOC", designation_name="Collio DOC",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Border DOC in Friuli Venezia Giulia on the Slovenian frontier; produces some of Italy's finest white wines from Pinot Grigio, Friulano, Ribolla Gialla and international varieties on flysch soils.",
        key_producers="Josko Gravner, Edi Keber, Mario Schiopetto",
        historical_context="Collio established Italy's white wine revolution in the 1970s; Schiopetto pioneered cold fermentation; today Gravner leads the amphora/skin-contact movement that spread globally.")
VIN(r1, 2022, "excellent", "rising", "Outstanding; flysch soils delivered exceptional mineral precision and aromatic intensity.")
VIN(r1, 2021, "very_good", "stable", "Cool vintage favoured whites; Ribolla Gialla and Friulano both outstanding.")
VIN(r1, 2020, "very_good", "stable", "Good ripeness with fine acidity; whites show excellent ageing potential.")
VIN(r1, 2019, "excellent", "rising", "Warm and concentrated; landmark vintage for Collio's top producers.")
VIN(r1, 2018, "good", "stable", "Solid vintage; wines accessible and expressive for early drinking.")
p1a = P("Edi Keber", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Legendary Collio producer making a single estate white blend of Friulano, Malvasia Istriana and Ribolla Gialla from the Brda hills flysch soils.",
        reputation_narrative="One of Collio's most revered names; Keber's single-cuvée approach is iconoclast and brilliant.",
        price_positioning="premium",
        authority_tier=2)
p1b = P("Mario Schiopetto", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The historic estate that launched Collio's white wine revolution; single-varietal bottlings of rare precision from the original Friulian terroir pioneer.",
        reputation_narrative="Mario Schiopetto is the founding father of modern Italian white wine; estate continues under family with unchanged commitment to precision.",
        price_positioning="premium",
        authority_tier=2)
pr1a, n1a = PROD("Edi Keber Collio Bianco", "wine_still", p1a, r1, "Italy",
                  subcategory="Friulano blend",
                  description="Single-estate Collio blend of Friulano, Malvasia and Ribolla; savoury, mineral and complex with almond, citrus and a long stony finish.",
                  price_tier="premium")
if n1a:
    PAIR(pr1a, "Prosciutto di San Daniele with melon", "complement", "classic", "starter", "Regional Friulian prosciutto with local white wine; almond and cured meat in natural harmony.")
    PAIR(pr1a, "Grilled turbot with lemon and capers", "complement", "established", "fish_course", "Noble flat fish demands a structured Italian white; Keber's mineral complexity is ideal.")
    PAIR(pr1a, "Risotto with asparagus and Montasio", "complement", "classic", "main", "Friulian risotto with local cheese; savoury richness matched by wine's mineral weight.")
    PAIR(pr1a, "Frico (Friulian cheese and potato cake)", "complement", "classic", "casual", "Traditional Friulian dish with the region's benchmark white wine; regional harmony.")
pr1b, n1b = PROD("Schiopetto Collio Friulano", "wine_still", p1b, r1, "Italy",
                  subcategory="Friulano",
                  description="Benchmark Friulano with classic bitter almond finish, white peach, citrus and mineral precision; medium-bodied and age-worthy.",
                  price_tier="premium")
if n1b:
    PAIR(pr1b, "Cured salmon with dill cream", "complement", "established", "starter", "Friulano's almond bitterness and citrus complement salmon richness; dill bridges herb notes.")
    PAIR(pr1b, "Tagliolini with white truffle", "complement", "classic", "main", "Truffle's earthy depth amplified by Friulano's mineral savoury character.")
    PAIR(pr1b, "Sea bass carpaccio with oil and salt", "complement", "established", "starter", "Delicate raw fish preserved by Friulano's precision; mineral finish echoes the sea.")
    PAIR(pr1b, "Aged Montasio DOP with honey", "complement", "classic", "cheese", "Regional cheese classic; bitter almond in wine matches aged Montasio's crystalline sweetness.")

# ── REGION 2: Carso ─────────────────────────────────────────────────────────
print("=== Region 2: Carso ===")
r2 = R("Carso", "Italy", "wine",
        designation_type="DOC", designation_name="Carso DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Dramatic limestone karst plateau DOC above Trieste; produces unique Vitovska whites and Terrano reds from shallow red iron-rich soils; wines of fierce minerality and striking individuality.",
        key_producers="Zidarich, Skerk, Vodopivec",
        historical_context="Carso's ancient Vitovska grape nearly disappeared; revived by a small group of artisan producers in the 1990s who pioneered long skin-contact maceration methods now copied worldwide.")
VIN(r2, 2022, "very_good", "stable", "Wind-swept season; Vitovska shows classic intensity and mineral precision.")
VIN(r2, 2021, "good", "stable", "Bora wind stripped some fruit; leaner wines with striking mineral purity.")
VIN(r2, 2020, "excellent", "rising", "Outstanding vintage; Vitovska and Terrano both show exceptional depth.")
VIN(r2, 2019, "very_good", "stable", "Warm and concentrated; Terrano particularly impressive with good structure.")
VIN(r2, 2018, "good", "stable", "Accessible vintage; approachable wines showing good regional character.")
p2a = P("Zidarich", "winery", r2, "Italy",
        production_philosophy="minimal_intervention",
        philosophy_description="Pioneer of Carso's skin-contact and natural wine movement; caves dug into the karst rock hold extended maceration whites and barrel-aged Terrano.",
        reputation_narrative="Globally recognised as Carso's most iconic producer; Zidarich appears on the world's most progressive restaurant wine lists.",
        price_positioning="premium",
        authority_tier=2)
p2b = P("Skerk", "winery", r2, "Italy",
        production_philosophy="minimal_intervention",
        philosophy_description="Artisan Carso producer emphasising long skin-contact Vitovska and natural Terrano; stone karst cellars provide natural temperature control.",
        reputation_narrative="Alongside Zidarich, Skerk defines Carso's natural wine identity; highly sought by collectors.",
        price_positioning="premium",
        authority_tier=2)
pr2a, n2a = PROD("Zidarich Vitovska Carso", "wine_still", p2a, r2, "Italy",
                  subcategory="Vitovska",
                  description="Extended skin-contact Vitovska with amber colour; intense mineral, dried herb, orange peel and saline complexity; profound and unconventional.",
                  price_tier="premium")
if n2a:
    PAIR(pr2a, "Aged Stravecchio cheese with walnuts", "complement", "classic", "cheese", "Intense aged cheese matches Vitovska's depth; walnut bitterness echoes orange peel.")
    PAIR(pr2a, "Jota (Triestine bean and sauerkraut stew)", "complement", "classic", "main", "Regional dish meets regional wine; fermented vegetables mirror Vitovska's oxidative complexity.")
    PAIR(pr2a, "Smoked eel with horseradish cream", "complement", "established", "starter", "Smoky eel needs an assertive white; Vitovska's skin-contact intensity matches the challenge.")
    PAIR(pr2a, "Lamb tartare with capers and anchovy", "contrast", "adventurous", "starter", "Bold pairing: Vitovska's mineral salinity against raw lamb; shared anchovy thread unites.")
pr2b, n2b = PROD("Skerk Ograde Carso Bianco", "wine_still", p2b, r2, "Italy",
                  subcategory="Vitovska blend",
                  description="Skin-contact field blend from the Carso limestone plateau; amber-hued with herb, stone and mineral intensity; remarkable persistence.",
                  price_tier="premium")
if n2b:
    PAIR(pr2b, "Baccalà mantecato on grilled polenta", "complement", "classic", "starter", "Adriatic salt cod whipped with oil; mineral Carso white bridges the sea and land.")
    PAIR(pr2b, "Grilled razor clams with garlic and parsley", "complement", "established", "starter", "Briny clams match Carso's salinity; skin-contact texture adds unexpected depth.")
    PAIR(pr2b, "Salumi misti with pickled vegetables", "complement", "established", "casual", "Carso whites love cured meat; skin-contact tannin handles the fat.")
    PAIR(pr2b, "Octopus salad with potatoes and herbs", "complement", "classic", "starter", "Adriatic seafood and Carso wine; coastal mineral character in both plate and glass.")

# ── REGION 3: Isonzo ────────────────────────────────────────────────────────
print("=== Region 3: Isonzo del Friuli ===")
r3 = R("Isonzo del Friuli", "Italy", "wine",
        designation_type="DOC", designation_name="Isonzo del Friuli DOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Gravel-rich flood plain DOC along the Isonzo river producing Pinot Grigio, Chardonnay, Merlot and Cabernet of great concentration and aromatic precision from well-drained alluvial soils.",
        key_producers="Lis Neris, Vie di Romans",
        historical_context="Isonzo's gravel soils were recognised as exceptional by pioneering producers in the 1980s; Vie di Romans and Lis Neris demonstrated the appellation could rival Collio's finest whites.")
VIN(r3, 2022, "excellent", "rising", "Gravel drainage perfect in a warm year; whites show exceptional concentration.")
VIN(r3, 2021, "very_good", "stable", "Cooler season; wines aromatic and precise with good mineral expression.")
VIN(r3, 2020, "very_good", "stable", "Well-balanced vintage; Pinot Grigio and Chardonnay both outstanding.")
VIN(r3, 2019, "excellent", "rising", "Landmark vintage for the appellation; concentrated and age-worthy.")
VIN(r3, 2018, "good", "stable", "Solid vintage; accessible wines with good fruit expression.")
p3a = P("Vie di Romans", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Benchmark Isonzo producer working gravel soils to produce single-vineyard whites of extraordinary depth; Gallo and Piere crus are iconic.",
        reputation_narrative="Considered Italy's finest Pinot Grigio producer; Vie di Romans transformed the variety's reputation.",
        price_positioning="premium",
        authority_tier=2)
p3b = P("Lis Neris", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Isonzo estate producing structured, barrel-fermented whites and clean varietal expressions; emphasis on texture and longevity.",
        reputation_narrative="Highly regarded for premium Friulian whites; Gris (Pinot Grigio) is a collector's wine.",
        price_positioning="premium",
        authority_tier=2)
pr3a, n3a = PROD("Vie di Romans Piere Sauvignon Blanc Isonzo", "wine_still", p3a, r3, "Italy",
                  subcategory="Sauvignon Blanc",
                  description="Single-vineyard Isonzo Sauvignon of great depth; smoke, elderflower, stone fruit and mineral precision — far removed from simple varietal styles.",
                  price_tier="premium")
if n3a:
    PAIR(pr3a, "Seared scallops with herb oil", "complement", "established", "fish_course", "Scallop sweetness and structured Sauvignon; smoke and herb bridge the two.")
    PAIR(pr3a, "Asparagus and smoked salmon quiche", "complement", "established", "starter", "Classic Sauvignon accompaniment; smoke echoes wine's stony character.")
    PAIR(pr3a, "Langoustines with butter and tarragon", "complement", "classic", "fish_course", "Delicate shellfish lifted by mineral Sauvignon; tarragon bridges the herb notes.")
    PAIR(pr3a, "Goat's cheese and roasted beet salad", "complement", "classic", "starter", "Sauvignon and goat cheese classic; beet earthiness adds depth to the pairing.")
pr3b, n3b = PROD("Lis Neris Gris Isonzo Pinot Grigio", "wine_still", p3b, r3, "Italy",
                  subcategory="Pinot Grigio",
                  description="Barrel-fermented single-vineyard Pinot Grigio of exceptional complexity; hazelnut, white peach, honey and mineral — redefines the variety.",
                  price_tier="premium")
if n3b:
    PAIR(pr3b, "Risotto with porcini and Parmigiano", "complement", "classic", "main", "Mushroom richness meets structured Pinot Grigio; Parmigiano bridges the mineral weight.")
    PAIR(pr3b, "Roasted veal with rosemary and garlic", "complement", "established", "main", "Full-bodied Pinot Grigio handles veal's mild richness; hazelnut and rosemary connect.")
    PAIR(pr3b, "Pan-seared foie gras with fig compote", "complement", "established", "starter", "Barrel fermentation gives the wine fat to match foie; fig sweetness bridges fruit notes.")
    PAIR(pr3b, "Tagliatelle with truffle butter", "complement", "classic", "main", "Truffle and hazelnut notes in both wine and dish; butter bridges the richness.")

# ── REGION 4: Friuli Grave ───────────────────────────────────────────────────
print("=== Region 4: Friuli Grave ===")
r4 = R("Friuli Grave", "Italy", "wine",
        designation_type="DOC", designation_name="Friuli Grave DOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Largest Friulian DOC across a vast gravel plain; reliable source of varietal Pinot Grigio, Merlot, Refosco and Sauvignon Blanc; quality ranges from commercial to excellent in top estates.",
        key_producers="Russiz Superiore, Plozner",
        historical_context="Friuli Grave produces the commercial bedrock of the region's wine economy; best producers deliver genuine quality from deep gravel soils; home to much of the Pinot Grigio world exports.")
VIN(r4, 2022, "very_good", "stable", "Warm and generous; Pinot Grigio and Merlot both approachable and expressive.")
VIN(r4, 2021, "good", "stable", "Cooler year; wines lean and fresh; best results from earlier varieties.")
VIN(r4, 2020, "very_good", "stable", "Balanced vintage; classic expressions of all major varieties.")
VIN(r4, 2019, "very_good", "stable", "Warm with excellent ripeness; Merlot and Refosco particularly strong.")
VIN(r4, 2018, "good", "stable", "Good commercial vintage; consistent quality across the appellation.")
p4a = P("Russiz Superiore", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Top-tier Friuli Grave estate owned by the Felluga family; single-vineyard whites and Bordeaux-variety reds of genuine complexity.",
        reputation_narrative="One of the Grave's finest producers; premium wines compete with Collio estates.",
        price_positioning="premium",
        authority_tier=2)
p4b = P("Plozner", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Consistent Friuli Grave producer focused on clean, aromatic varietal expressions with emphasis on freshness and food-friendliness.",
        reputation_narrative="Reliable quality benchmark for the DOC; widely distributed and consistently good.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Russiz Superiore Friuli Grave Sauvignon", "wine_still", p4a, r4, "Italy",
                  subcategory="Sauvignon Blanc",
                  description="Structured Friulian Sauvignon with elderflower, citrus, white pepper and mineral complexity; more texture than typical varietal style.",
                  price_tier="premium")
if n4a:
    PAIR(pr4a, "Vitello tonnato (veal with tuna sauce)", "complement", "classic", "starter", "Piedmontese classic meets Friulian white; mineral Sauvignon cuts through the rich tuna cream.")
    PAIR(pr4a, "Fresh pea and mint soup", "complement", "established", "starter", "Green freshness in both glass and bowl; pea sweetness balanced by Sauvignon's tartness.")
    PAIR(pr4a, "Grilled dover sole with lemon butter", "complement", "established", "fish_course", "Delicate flat fish meets mineral Sauvignon; lemon butter bridges the wine's citrus notes.")
    PAIR(pr4a, "Fresh ricotta with herbs and olive oil", "complement", "established", "starter", "Soft cheese and herb complement Sauvignon's aromatics; a light, refined aperitif match.")
pr4b, n4b = PROD("Plozner Friuli Grave Pinot Grigio", "wine_still", p4b, r4, "Italy",
                  subcategory="Pinot Grigio",
                  description="Clean, fresh Pinot Grigio with pear, citrus blossom and light mineral note; easy-drinking and consistently reliable.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Grilled sea bass fillet with herbs", "complement", "established", "fish_course", "Delicate bass and delicate Pinot Grigio; herb garnish bridges the wine's floral notes.")
    PAIR(pr4b, "Insalata Caprese with buffalo mozzarella", "complement", "classic", "starter", "Tomato, basil and mozzarella love a clean Italian white; Pinot Grigio's freshness ideal.")
    PAIR(pr4b, "Risotto alle vongole (clam risotto)", "complement", "established", "main", "Briny clam risotto matched by Pinot Grigio's mineral freshness; a natural Italian pairing.")
    PAIR(pr4b, "Light chicken piccata with capers", "complement", "classic", "main", "Lemony chicken piccata is the quintessential Pinot Grigio food match.")

# ── REGION 5: Teroldego Rotaliano ───────────────────────────────────────────
print("=== Region 5: Teroldego Rotaliano ===")
r5 = R("Teroldego Rotaliano", "Italy", "wine",
        designation_type="DOC", designation_name="Teroldego Rotaliano DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Small Trentino DOC on the Campo Rotaliano alluvial plain; home to the Teroldego grape — a rich, dark-fruited red unique to this gravelly plateau between the Alps.",
        key_producers="Foradori, Mezzacorona",
        historical_context="Teroldego was Trentino's anonymous workhorse red until Elisabetta Foradori revived it through biodynamics and amphora work in the 1990s; now internationally recognised as one of Italy's great native varieties.")
VIN(r5, 2022, "very_good", "stable", "Warm summer; Teroldego shows rich dark fruit and supple tannins.")
VIN(r5, 2021, "good", "stable", "Cooler year; reds more aromatic and lighter than usual; elegant expressions.")
VIN(r5, 2020, "excellent", "rising", "Outstanding vintage; concentrated and age-worthy Teroldego.")
VIN(r5, 2019, "very_good", "stable", "Ripe and generous; deep colour and plum complexity.")
VIN(r5, 2018, "very_good", "stable", "Excellent ripeness; Teroldego shows characteristic bitter chocolate and violet.")
p5a = P("Foradori", "winery", r5, "Italy",
        production_philosophy="biodynamic",
        philosophy_description="Elisabetta Foradori revolutionised Teroldego through biodynamics and clay amphora fermentation; her work transformed Italy's understanding of native grapes.",
        reputation_narrative="One of Italy's most celebrated winemakers; Foradori's Granato is a benchmark Italian red.",
        price_positioning="premium",
        authority_tier=2)
p5b = P("Mezzacorona", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Large cooperative producing reliable, commercially important Teroldego from Campo Rotaliano; accessible quality across the range.",
        reputation_narrative="The volume producer that made Teroldego known internationally; quality tier wines are genuinely impressive.",
        price_positioning="value",
        authority_tier=1)
pr5a, n5a = PROD("Foradori Granato Teroldego Vigneti delle Dolomiti", "wine_still", p5a, r5, "Italy",
                  subcategory="Teroldego",
                  description="Benchmark Teroldego aged in clay amphora and large casks; intense violet, dark cherry, bitter chocolate and volcanic mineral; profound and age-worthy.",
                  price_tier="premium")
if n5a:
    PAIR(pr5a, "Braised venison with dark berry sauce", "complement", "classic", "main", "Dark fruit and game are made for each other; Teroldego's bitterness complements the richness.")
    PAIR(pr5a, "Speck Alto Adige with rye bread", "complement", "classic", "casual", "Smoked Trentino speck and regional Teroldego; smoke, juniper and dark fruit in harmony.")
    PAIR(pr5a, "Slow-roasted lamb shoulder with herbs", "complement", "established", "main", "Lamb's richness matched by Teroldego's structural depth; herb bridge through the wine's violet.")
    PAIR(pr5a, "Aged Trentingrana with truffle honey", "complement", "classic", "cheese", "Regional aged cheese with local red wine; bitter chocolate and crystalline cheese in balance.")
pr5b, n5b = PROD("Mezzacorona Teroldego Rotaliano Classico", "wine_still", p5b, r5, "Italy",
                  subcategory="Teroldego",
                  description="Accessible Teroldego with dark cherry, blueberry and light bitter chocolate; medium-bodied and versatile.",
                  price_tier="value")
if n5b:
    PAIR(pr5b, "Sausage and lentil stew", "complement", "established", "main", "Hearty Italian country food matched by food-friendly Teroldego; rustic harmony.")
    PAIR(pr5b, "Mushroom and potato gnocchi", "complement", "classic", "main", "Earthy mushroom notes echo Teroldego's forest fruit; potato softness balanced by acidity.")
    PAIR(pr5b, "Pizza with wild mushroom and truffle oil", "complement", "established", "casual", "Casual pizza needs an accessible red with dark fruit; Teroldego delivers.")
    PAIR(pr5b, "Grilled pork ribs with rosemary and garlic", "complement", "classic", "main", "Rich pork fat balanced by Teroldego's acidity and tannin; rosemary bridges the violet note.")

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
