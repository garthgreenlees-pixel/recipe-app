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

# ── Batch 74 ──────────────────────────────────────────────────────────────────
# Regions: Châteauneuf-du-Pape (depth), Corsica, Verdicchio dei Castelli di Jesi,
#          Etna (depth), Collio

# ── Region 1: Corsica ─────────────────────────────────────────────────────────
print("\n=== Region 1: Corsica ===")
r1 = R("Corsica", "France", "wine",
    designation_type="AOC",
    designation_name="Vin de Corse AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Mediterranean island with indigenous varieties Nielluccio (Sangiovese clone), Sciaccarellu and Vermentino; wines are aromatic, sun-drenched and distinctively Corsican — between French and Italian in character.",
    key_producers="Clos Canarelli, Domaine Comte Abbatucci, Arena Antoine, Domaine Leccia",
    historical_context="Corsica has 8,000 years of wine history; the island's unique grape varieties and microterroirs produce wines that have no equivalent anywhere else in the Mediterranean."
)
VIN(r1, 2022, "excellent", "rising", "Outstanding Mediterranean vintage; Nielluccio and Vermentino show extraordinary aromatic definition.")
VIN(r1, 2021, "very_good", "stable", "Good quality; wines express the island's characteristic sea-herb-granite minerality.")
VIN(r1, 2020, "good", "stable", "Consistent vintage; approachable wines with Corsican aromatic identity.")
VIN(r1, 2019, "excellent", "rising", "Benchmark Corsican year; Patrimonio and Ajaccio appellations both produced exceptional wines.")
VIN(r1, 2018, "very_good", "stable", "Good season; Vermentino particularly successful with aromatic intensity and mineral precision.")

p1a = P("Domaine Comte Abbatucci", "winery", r1, "France",
    production_philosophy="biodynamic",
    philosophy_description="Jean-Charles Abbatucci's legendary biodynamic estate in the Taravo valley, conserving ancient Corsican grape varieties — over 30 indigenous clones — farmed without any inputs.",
    reputation_narrative="Abbatucci is considered Corsica's greatest wine estate; the Admiral wines and rare cuvées from ancient varieties are among France's most sought-after and collectable wines.",
    price_positioning="ultra_premium")
prod1a, new1a = PROD("Abbatucci Grand Cru Blanc", "wine_still", p1a, r1, "France",
    subcategory="Vermentino blend",
    description="Corsica's greatest white wine: Vermentino and ancient island varieties from biodynamic vines — white peach, wild flowers, garrigue, sea brine and extraordinary mineral depth.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Grilled line-caught sea bass with sea fennel and olive oil", "complement", "classic", "main", "Mediterranean fish with Corsican white — sea fennel bridges the wine's garrigue and brine notes.")
    PAIR(prod1a, "Corsican brocciu cheese with herbs and chestnut honey", "complement", "classic", "cheese", "The island's fresh sheep cheese with its greatest white wine is the definitive Corsican pairing.")
    PAIR(prod1a, "Langoustines with aioli and sea herbs", "complement", "established", "starter", "Briny crustacean and mineral island white; aioli richness balances the wine's acidity.")
    PAIR(prod1a, "White asparagus with mousseline sauce", "complement", "suggested", "starter", "The wine's floral complexity elevates delicate white asparagus; mousseline bridges richness.")

p1b = P("Clos Canarelli", "winery", r1, "France",
    production_philosophy="biodynamic",
    philosophy_description="Yves Canarelli's estate in the south of Corsica producing benchmark Figari wines including Sciaccarellu red and Vermentino white from granitic soils.",
    reputation_narrative="Canarelli is Corsica's most critically acclaimed producer for terroir-specific wines; the Sciaccarellu is considered the finest expression of this Corsican variety.",
    price_positioning="premium")
prod1b, new1b = PROD("Clos Canarelli Sciaccarellu", "wine_still", p1b, r1, "France",
    subcategory="Sciaccarellu",
    description="Corsica's most elegant red variety from granitic south-facing slopes — raspberry, wild herbs, smoked meat, garrigue and vivid silky acidity; Pinot Noir-esque in its delicacy.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Roasted Corsican suckling pig (porchetta corsa) with myrtle", "complement", "classic", "main", "Island pork and island wine; myrtle leaves in the Corsican tradition echo the wine's wild herb character.")
    PAIR(prod1b, "Charcuterie from Corsican cured pork with figs", "complement", "established", "starter", "Coppa, lonzu and figatellu with the island's red wine is the authentic Corsican aperitif.")
    PAIR(prod1b, "Grilled lamb chops with maquis herb crust", "complement", "classic", "main", "Lamb from the scrubland and wine from the same scrubland — pure terroir pairing.")
    PAIR(prod1b, "Tomme brebis Corse (fresh ewes' milk cheese) with chestnut jam", "bridge", "established", "cheese", "Island sheep cheese and Sciaccarellu; chestnut jam bridges the wine's dark berry note.")

# ── Region 2: Verdicchio dei Castelli di Jesi ─────────────────────────────────
print("\n=== Region 2: Verdicchio dei Castelli di Jesi ===")
r2 = R("Verdicchio dei Castelli di Jesi", "Italy", "wine",
    designation_type="DOC",
    designation_name="Verdicchio dei Castelli di Jesi DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Marche DOC producing Italy's finest expressions of Verdicchio — crisp, mineral, herb-edged whites of surprising depth and age-worthiness from the Apennine hills above the Adriatic.",
    key_producers="Garofoli, Umani Ronchi, Bucci, Sartarelli, La Staffa",
    historical_context="Verdicchio's iconic amphora bottle was designed in 1953 and became Italy's most recognisable wine bottle; beneath the marketing, the variety produces some of Italy's most underrated age-worthy whites."
)
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage for Verdicchio; wines of remarkable mineral tension and aromatic purity.")
VIN(r2, 2021, "very_good", "stable", "Good quality; classic Verdicchio profile with citrus, almond and good acidity.")
VIN(r2, 2020, "good", "stable", "Consistent vintage; reliable, food-friendly wines at accessible prices.")
VIN(r2, 2019, "excellent", "rising", "Near-perfect growing season; Verdicchio Classico Superiore of exceptional complexity.")
VIN(r2, 2018, "very_good", "stable", "Good season; wines show the variety's characteristic bitter almond finish and mineral drive.")

p2a = P("Bucci", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="The Marche's most prestigious Verdicchio estate, producing Villa Bucci Riserva — Italy's greatest age-worthy Verdicchio, capable of developing for 20+ years.",
    reputation_narrative="Bucci Villa Bucci Riserva is considered Italy's finest Verdicchio; it demonstrates that the variety can produce whites of Burgundian structure and longevity.",
    price_positioning="premium")
prod2a, new2a = PROD("Bucci Villa Bucci Riserva Verdicchio", "wine_still", p2a, r2, "Italy",
    subcategory="Verdicchio",
    description="Italy's benchmark age-worthy Verdicchio — green apple, lemon, almond, beeswax, fennel and a distinctive bitter mineral finish that develops complexity over a decade.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Grilled Adriatic branzino with fennel and lemon", "complement", "classic", "main", "Adriatic fish with Adriatic wine — fennel in the dish mirrors the wine's anise note perfectly.")
    PAIR(prod2a, "Vincisgrassi (Marche lasagne with giblets and béchamel)", "complement", "classic", "main", "The region's most complex pasta dish with the region's most age-worthy white.")
    PAIR(prod2a, "Risotto with clams and saffron", "complement", "established", "main", "Shellfish and mineral white is a classic; saffron's earthy-floral note aligns with Verdicchio's aromatic profile.")
    PAIR(prod2a, "Aged Pecorino from Le Marche with truffle honey", "bridge", "suggested", "cheese", "Regional cheese with regional wine; truffle honey bridges the wine's mineral depth.")

p2b = P("Sartarelli", "winery", r2, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Pure-play Verdicchio specialist producing only Castelli di Jesi wines, including the benchmark Balciana late-harvest Verdicchio — one of Italy's most individual white wines.",
    reputation_narrative="Sartarelli Balciana is the world's most acclaimed late-harvest Verdicchio; the estate produces nothing but Verdicchio and produces it at the highest level.",
    price_positioning="premium")
prod2b, new2b = PROD("Sartarelli Classico Verdicchio", "wine_still", p2b, r2, "Italy",
    subcategory="Verdicchio",
    description="Benchmark entry-level Verdicchio Classico — fresh apple, citrus blossom, almond paste and sea-mineral finish; crisp, precise and ideal for seafood.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Calamarata pasta with calamari and cherry tomatoes", "complement", "classic", "main", "Squid pasta with crisp Verdicchio is the Adriatic's most satisfying food-wine combination.")
    PAIR(prod2b, "Fritto misto di mare with lemon", "complement", "classic", "fish_course", "Deep-fried seafood and Verdicchio's acidity and bitterness create the ideal counterpoint.")
    PAIR(prod2b, "Olive ascolane (stuffed and fried olives) with aioli", "complement", "established", "amuse", "Le Marche's most beloved bar snack with its most beloved wine — an authentic regional pairing.")
    PAIR(prod2b, "Stracchino with herb flatbread", "complement", "suggested", "cheese", "Mild, creamy cheese with crisp Verdicchio; the wine's acidity lifts the cheese's gentle richness.")

# ── Region 3: Collio ──────────────────────────────────────────────────────────
print("\n=== Region 3: Collio ===")
r3 = R("Collio", "Italy", "wine",
    designation_type="DOC",
    designation_name="Collio Goriziano DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Italy's most prestigious white wine DOC in Friuli-Venezia Giulia, bordering Slovenia, producing exceptional Friulano, Ribolla Gialla, Pinot Grigio and Sauvignon Blanc from ponca marl-and-sandstone soils.",
    key_producers="Edi Keber, Josko Gravner, Marco Felluga, Schiopetto, Radikon",
    historical_context="Collio was pioneered in the 1960s and 70s by Mario Schiopetto, who transformed Italian white winemaking; today it is home to both Italy's most precise conventional whites and the world's most influential amber wine movement."
)
VIN(r3, 2022, "excellent", "rising", "Exceptional Collio vintage; Friulano and Ribolla Gialla of extraordinary mineral precision and freshness.")
VIN(r3, 2021, "very_good", "stable", "Good quality; wines show the ponca soil's characteristic mineral character.")
VIN(r3, 2020, "good", "stable", "Reliable vintage; expressive whites with food-friendly acidity.")
VIN(r3, 2019, "exceptional", "rising", "One of Collio's greatest vintages; wines of Burgundian structure and ageing potential.")
VIN(r3, 2018, "very_good", "stable", "Good season; Friulano and Pinot Grigio both produced wines of excellent balance.")

p3a = P("Edi Keber", "winery", r3, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Kristian Keber's Collio estate where all wines are blended into a single Collio white label — Friulano, Malvasia and Ribolla — with a focus on ponca soil expression over variety.",
    reputation_narrative="Edi Keber's single Collio white wine is one of Italy's most unique and admired wines; the insistence on one wine from one terroir has earned it global recognition.",
    price_positioning="premium")
prod3a, new3a = PROD("Edi Keber Collio Bianco", "wine_still", p3a, r3, "Italy",
    subcategory="Friulano blend",
    description="Italy's most singular Collio white: Friulano, Malvasia Istriana and Ribolla Gialla blended for ponca soil expression — almonds, white flowers, hay, lemon curd and saline mineral length.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Risotto with San Daniele prosciutto and asparagus", "complement", "classic", "main", "Friuli's greatest cured ham and asparagus with its definitive white wine — pure regional eloquence.")
    PAIR(prod3a, "Frico croccante (crispy Montasio cheese frico)", "complement", "classic", "starter", "Friuli's most beloved regional snack with its most singular white wine; cheese fat and mineral acidity.")
    PAIR(prod3a, "Pan-seared John Dory with capers and lemon butter", "complement", "established", "fish_course", "Delicate sea fish and precise Collio white; capers echo the wine's saline mineral character.")
    PAIR(prod3a, "Baked ricotta with herbs and lemon zest", "complement", "suggested", "starter", "Fresh dairy and aromatic herbs align with the wine's floral and mineral freshness.")

p3b = P("Radikon", "winery", r3, "Italy",
    production_philosophy="minimal_intervention",
    philosophy_description="Stanko Radikon's legendary Collio estate that pioneered the orange/amber wine movement globally; long skin maceration on Ribolla Gialla and other varieties produces wines of extraordinary complexity and longevity.",
    reputation_narrative="Radikon is one of the most influential wine estates in the world; their skin-contact Ribolla Gialla and Oslavje inspired an entire global natural wine movement.",
    price_positioning="ultra_premium")
prod3b, new3b = PROD("Radikon Ribolla Gialla", "wine_still", p3b, r3, "Italy",
    subcategory="Ribolla Gialla",
    description="The world's most celebrated amber wine: Ribolla Gialla macerated 3–6 months on skins — dried apricot, orange peel, walnut, chamomile and tannic structure that demands food; can age 20+ years.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Suckling pig with rosemary and garlic (porchetta)", "complement", "classic", "main", "Tannin from skin contact handles rich pork; rosemary and garlic align with amber wine's complexity.")
    PAIR(prod3b, "Aged Latteria Friulano cheese with fig jam", "complement", "established", "cheese", "Alpine dairy cheese and tannic amber wine; fig jam bridges the wine's dried fruit character.")
    PAIR(prod3b, "Braised rabbit with wild herbs and polenta", "complement", "established", "main", "Lean game and polenta's corn sweetness bridge amber wine's tannin and acidity beautifully.")
    PAIR(prod3b, "Smoked duck breast with pickled onion and pumpernickel", "complement", "adventurous", "starter", "Smoke, acidity and tannin in harmony; pickled onion's sharpness bridges the wine's oxidative depth.")

# ── Region 4: Txakoli ─────────────────────────────────────────────────────────
print("\n=== Region 4: Txakoli ===")
r4 = R("Txakoli", "Spain", "wine",
    designation_type="DO",
    designation_name="Getariako Txakolina DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Basque Country's crisp, low-alcohol, slightly effervescent white wine from Hondarrabi Zuri grown on steep coastal slopes above the Bay of Biscay; the quintessential partner for pintxos and seafood.",
    key_producers="Txomin Etxaniz, Ameztoi, Hiruzta, Rezabal, Gorka Izagirre",
    historical_context="Txakoli has been produced in the Basque Country for centuries; nearly extinct by the 1980s, the wine was saved by determined local producers and now represents one of Spain's most distinctive and lively regional styles."
)
VIN(r4, 2022, "excellent", "rising", "Outstanding Atlantic vintage; Txakoli of exceptional freshness and saline precision.")
VIN(r4, 2021, "very_good", "stable", "Good quality; wines show vibrant acidity and the characteristic salty finish.")
VIN(r4, 2020, "good", "stable", "Consistent vintage; reliable, lively Txakoli for early drinking.")
VIN(r4, 2019, "excellent", "rising", "Benchmark year; wines with remarkable aromatic intensity and length for the variety.")
VIN(r4, 2018, "very_good", "stable", "Balanced Atlantic season; Txakoli shows good concentration and characteristic bubbles.")

p4a = P("Txomin Etxaniz", "winery", r4, "Spain",
    production_philosophy="traditional",
    philosophy_description="The oldest and most celebrated Txakoli estate in Getaria, defining the category for generations with wines of consistent quality, salinity and crisp Atlantic freshness.",
    reputation_narrative="Txomin Etxaniz is the reference producer for Getariako Txakolina; the estate defines what Txakoli tastes like and has brought the wine to international attention.",
    price_positioning="mid_range")
prod4a, new4a = PROD("Txomin Etxaniz Txakoli", "wine_still", p4a, r4, "Spain",
    subcategory="Hondarrabi Zuri",
    description="The quintessential Txakoli: green apple, lime, sea salt, white flowers and a slight natural pétillance; poured from height to accentuate the bubbles — vivid, light and thirst-quenching.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Anchoas del Cantábrico (Cantabrian anchovies) on bread", "complement", "classic", "aperitif", "The classic Basque bar combination: anchovy's brine and umami with the wine's salt and freshness.")
    PAIR(prod4a, "Gambas a la plancha (grilled prawns) with sea salt", "complement", "classic", "starter", "Simple grilled seafood demands simple wine; the wine's marine character mirrors the prawns.")
    PAIR(prod4a, "Pintxos board: boquerones, tortilla, jamón croquetas", "complement", "classic", "casual", "The quintessential Basque bar scenario — Txakoli is made for pintxos culture.")
    PAIR(prod4a, "Kokotxas al pil-pil (salt cod cheeks in olive oil)", "complement", "established", "main", "Basque classic: the gelatinous salt cod and pil-pil sauce align perfectly with the wine's salinity and acidity.")

p4b = P("Ameztoi", "winery", r4, "Spain",
    production_philosophy="terroir_expression",
    philosophy_description="Pioneering Getaria estate producing both traditional Txakoli and a revolutionary Rubentis rosé Txakoli that brought the variety international recognition.",
    reputation_narrative="Ameztoi Rubentis is one of Spain's most popular wine exports in the natural wine and fine restaurant market; the estate brought Txakoli to a new generation of wine lovers.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Ameztoi Rubentis Rosé Txakoli", "wine_still", p4b, r4, "Spain",
    subcategory="Hondarrabi Beltza rosé",
    description="Txakoli's most celebrated rosé: salmon pink from Hondarrabi Beltza with strawberry, sea spray, pink grapefruit and vibrant Atlantic acidity — lively, charming and food-ready.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled razor clams with lemon and parsley butter", "complement", "classic", "starter", "Atlantic bivalves and Atlantic rosé Txakoli — the shared terroir produces a perfect pairing.")
    PAIR(prod4b, "Tuna tataki with ponzu and microherbs", "bridge", "established", "starter", "The wine's acidity and salinity bridge the gap between its Spanish identity and Japanese-inspired preparation.")
    PAIR(prod4b, "Burrata with tomato, basil and sea salt", "complement", "suggested", "starter", "Simple summer starter; the rosé's strawberry and sea salt note mirrors the dish's freshness.")
    PAIR(prod4b, "Grilled octopus with paprika and olive oil", "complement", "established", "starter", "Classic Galician/Basque preparation with Basque rosé; paprika bridges the wine's pink fruit note.")

# ── Region 5: Ribolla Gialla / Friuli Colli Orientali ─────────────────────────
print("\n=== Region 5: Friuli Colli Orientali ===")
r5 = R("Friuli Colli Orientali", "Italy", "wine",
    designation_type="DOC",
    designation_name="Friuli Colli Orientali DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Friuli's eastern hills DOC bordering Slovenia, producing benchmark Friulano, Ribolla Gialla, Picolit dessert wine and indigenous reds including Refosco and Schioppettino from marl-and-sandstone ponca soils.",
    key_producers="Ronchi di Manzano, Livio Felluga, Dorigo, Le Vigne di Zamò, Bastianich",
    historical_context="Friuli Colli Orientali is the natural extension of Collio into the hills; the zone produces some of Italy's finest white wines and unique indigenous reds including the rare Schioppettino and Tazzelenghe."
)
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage; Friulano and Ribolla of remarkable freshness and ponca mineral character.")
VIN(r5, 2021, "very_good", "stable", "Good season; wines show the DOC's characteristic aromatic richness and food-friendly structure.")
VIN(r5, 2020, "good", "stable", "Consistent quality; indigenous varieties particularly expressive this year.")
VIN(r5, 2019, "excellent", "rising", "Benchmark year; wines of exceptional depth and ageing potential.")
VIN(r5, 2018, "very_good", "stable", "Good overall quality; Picolit and sweet wines of particular excellence.")

p5a = P("Livio Felluga", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Friuli's most historically important estate, producing benchmark Terre Alte blend and single-variety wines from Colli Orientali; considered the patriarch of modern Friulian wine.",
    reputation_narrative="Livio Felluga Terre Alte is considered Italy's greatest Friulian white wine blend; the estate defines the DOC internationally.",
    price_positioning="premium")
prod5a, new5a = PROD("Livio Felluga Terre Alte", "wine_still", p5a, r5, "Italy",
    subcategory="Friulano blend",
    description="Friuli's greatest white blend: Friulano, Pinot Bianco and Sauvignon from ponca soils — white peach, almond, acacia flower, mineral and extraordinary texturally rich mid-palate.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "San Daniele prosciutto with melon and fig", "complement", "classic", "starter", "Friuli's most celebrated cured ham with its greatest white wine is an unbreakable regional tradition.")
    PAIR(prod5a, "Risotto all'Onda with asparagus and lemon", "complement", "established", "main", "Creamy northern Italian risotto and Terre Alte's weight align; asparagus bridges the wine's green herb note.")
    PAIR(prod5a, "Grilled turbot with herb oil and caper sauce", "complement", "classic", "fish_course", "Premium white fish and premium Friulian white — the wine's richness matches the turbot's fat.")
    PAIR(prod5a, "Montasio aged cheese with local honey", "complement", "established", "cheese", "Friuli's great mountain cheese and its finest white blend; honey bridges the wine's almond and stone fruit.")

p5b = P("Dorigo Winery", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Estate specialising in both indigenous Friulian whites and the rare red variety Schioppettino, producing one of Italy's most individual and distinctive red wines from the Colli Orientali.",
    reputation_narrative="Dorigo Schioppettino di Prepotto is the world's benchmark expression of this rare, peppery Friulian grape; the estate has been its greatest champion.",
    price_positioning="premium")
prod5b, new5b = PROD("Dorigo Schioppettino di Prepotto", "wine_still", p5b, r5, "Italy",
    subcategory="Schioppettino",
    description="Friuli's rarest and most distinctive red: Schioppettino with violet, wild raspberry, black pepper, smoked olive and iron minerality — Syrah-like in pepper but uniquely Friulian in structure.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Wild boar salami with sourdough and grain mustard", "complement", "established", "starter", "Gamey salami and peppery Schioppettino are natural companions; mustard bridges the wine's bite.")
    PAIR(prod5b, "Braised hare with polenta and wild herbs (lepre in salmì)", "complement", "classic", "main", "Classic Friulian preparation for indigenous red wine; hare's iron and the wine's mineral pepper in harmony.")
    PAIR(prod5b, "Venison medallions with juniper cream sauce", "complement", "established", "main", "Game meat and peppery Schioppettino; juniper's gin-like note echoes the wine's wild berry.")
    PAIR(prod5b, "Aged Montasio stagionato with black truffle", "complement", "established", "cheese", "Hard Friulian mountain cheese and the region's most individualistic red; truffle amplifies mineral depth.")

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
