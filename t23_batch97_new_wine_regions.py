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

# ── Region 1: Etna Bianco ─────────────────────────────────────────────────────
print("=== Region 1: Etna Bianco ===")
# Etna exists; add new producers/products focused on whites
r = R("Etna", "Italy", "wine",
      designation_type="DOC", designation_name="Etna DOC",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Volcanic Mount Etna producing Nerello Mascalese reds and Carricante whites on black lava soils; altitude, volcanic minerality and century-old vines create unique, compelling wines.",
      key_producers="Cornelissen, Benanti, Terre Nere, Passopisciaro",
      historical_context="Ancient Sicilian volcano; phylloxera never reached the high-altitude vineyards; 100-year-old bush vines survive on pre-phylloxera roots.")
VIN(r, 2022, "excellent", "rising", "Good volcanic year; precise Carricante whites and elegant Nerello reds.")
VIN(r, 2021, "exceptional", "rising", "Benchmark Etna vintage; Nerello of extraordinary finesse; Carricante at its best.")
VIN(r, 2020, "very_good", "stable", "Warm year; concentrated Nerello; Carricante showed tropical richness.")
VIN(r, 2019, "excellent", "stable", "Classic volcanic profile; structured reds and mineral whites of great precision.")
VIN(r, 2018, "very_good", "stable", "Good balance; food-friendly Etna reds and mineral-driven Carricante.")
p1 = P("Benanti", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Pioneer of the Etna fine wine renaissance (1988); Pietramarina Carricante from the eastern slopes is their landmark white; old-vine Nerello Mascalese from pre-phylloxera vines.",
       reputation_narrative="Giuseppe Benanti revived Etna as a serious wine destination; Pietramarina is still the benchmark Etna Bianco after decades.",
       price_positioning="premium")
p2 = P("Passopisciaro", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Andrea Franchetti's pioneering contrada-bottling project; Prephylloxera Nerello Mascalese from individual lava flows; introduced single-vineyard concept to Etna.",
       reputation_narrative="Passopisciaro proved that individual contrade on Etna have distinct personality; the estate that launched the single-vineyard revolution on the volcano.",
       price_positioning="premium")
pr1, n1 = PROD("Benanti Pietramarina Etna Bianco Superiore", "wine_still", p1, r, "Italy",
               subcategory="Carricante", price_tier="premium",
               description="Landmark Etna Bianco from old-vine Carricante on eastern Milo slopes; volcanic minerality, flint, citrus, white almond and a remarkable saline persistence; ages magnificently.")
if n1:
    PAIR(pr1, "Swordfish involtini with capers and raisins", "complement", "classic", "fish_course", "Sicilian regional pairing; volcanic mineral echoes sea character; capers bridge salinity.")
    PAIR(pr1, "Grilled prawns with lemon, garlic and herbs", "complement", "established", "starter", "Mineral-citrus wine amplifies prawn sweetness; volcanic flint adds smoky depth.")
    PAIR(pr1, "Linguine alle vongole with white wine", "complement", "classic", "main", "Saline volcanic mineral mirrors clam brine; citrus and herb echo the sauce.")
    PAIR(pr1, "Tuna carpaccio with capers and olive oil", "elevate", "established", "starter", "Volcanic minerality elevates tuna; capers bridge wine's salinity; olive oil mediates.")
pr2, n2 = PROD("Passopisciaro Contrada C Nerello Mascalese", "wine_still", p2, r, "Italy",
               subcategory="Nerello Mascalese", price_tier="premium",
               description="Single contrada Nerello Mascalese from volcanic lava; transparent red colour, strawberry, dried rose, iron and volcanic earth; Burgundian in weight, Etna in soul.")
if n2:
    PAIR(pr2, "Grilled tuna steak with caponata", "complement", "established", "main", "Nerello's iron and rose echo tuna's red meat character; caponata bridges sweet-sour.")
    PAIR(pr2, "Braised rabbit with olives and tomato", "complement", "established", "main", "Light volcanic red suits rabbit's delicacy; olives and tomato mirror Sicilian flavours.")
    PAIR(pr2, "Aged Piacentinu Ennese (saffron sheep cheese)", "complement", "suggested", "cheese", "Volcanic iron note echoes saffron in cheese; dried rose bridges.")
    PAIR(pr2, "Mushroom and truffle risotto al nero di seppia", "bridge", "adventurous", "main", "Iron-mineral Nerello bridges squid ink earthiness and mushroom umami.")

# ── Region 2: Irpinia ─────────────────────────────────────────────────────────
print("=== Region 2: Irpinia ===")
r = R("Irpinia", "Italy", "wine",
      designation_type="DOCG", designation_name="Irpinia DOCG",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Campanian hillside zone inland from Naples; home of Taurasi (Aglianico), Greco di Tufo and Fiano di Avellino — three of Southern Italy's greatest wine denominations.",
      key_producers="Feudi di San Gregorio, Mastroberardino, Terredora di Paolo, Cantina del Barone",
      historical_context="Mastroberardino revived Aglianico and Greco when phylloxera had decimated the region; Taurasi DOCG (1993) is the south's most age-worthy red.")
VIN(r, 2021, "exceptional", "rising", "Outstanding year; Taurasi of extraordinary tannic structure; Fiano of laser precision.")
VIN(r, 2020, "excellent", "stable", "Classic warm year; concentrated Aglianico with great depth and aging potential.")
VIN(r, 2019, "excellent", "stable", "Good balance; textbook Fiano di Avellino with mineral purity.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; plush Taurasi; fragrant Greco di Tufo.")
VIN(r, 2017, "very_good", "stable", "Drought stress created small yields but intense Aglianico; Fiano showed focus.")
p1 = P("Mastroberardino", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Tenth-generation family estate that saved Campanian indigenous varieties from extinction; Radici Taurasi is their flagship; estate vines in all three DOCG zones.",
       reputation_narrative="The most important family in southern Italian wine history; without Mastroberardino, Taurasi, Greco and Fiano might have been lost.",
       price_positioning="mid_range")
p2 = P("Cantina del Barone", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Luigi Sarno's small natural estate; old-vine Fiano di Avellino on volcanic and calcareous soils; indigenous yeasts; minimal sulphur; benchmark for natural Campanian whites.",
       reputation_narrative="Cantina del Barone's Particella 928 Fiano is one of Italy's great natural whites; concentrated, mineral and age-worthy.",
       price_positioning="mid_range")
pr1, n1 = PROD("Mastroberardino Radici Taurasi Riserva", "wine_still", p1, r, "Italy",
               subcategory="Aglianico", price_tier="premium",
               description="Benchmark Taurasi Riserva from old-vine Aglianico on volcanic soils; black cherry, tar, iron, licorice and powerful tannins; needs a decade to open; ages 30+ years.")
if n1:
    PAIR(pr1, "Slow-braised osso buco with gremolata", "complement", "classic", "main", "Aglianico's iron and tar align with braised veal; gremolata echoes wine's citrus lift.")
    PAIR(pr1, "Wild boar ragù with handmade paccheri", "complement", "established", "main", "Game tannin alignment; tar and iron match boar's earthy richness; pasta bridges.")
    PAIR(pr1, "Aged Parmigiano-Reggiano with truffle honey", "complement", "suggested", "cheese", "Taurasi's tannins soften against hard cheese; truffle honey bridges tar and iron notes.")
    PAIR(pr1, "Grilled ribeye with rosemary and red wine reduction", "complement", "classic", "main", "Classic red wine and steak; Aglianico's structure grips beef fat; tannins grip char.")
pr2, n2 = PROD("Cantina del Barone Particella 928 Fiano di Avellino", "wine_still", p2, r, "Italy",
               subcategory="Fiano", price_tier="mid_range",
               description="Natural old-vine Fiano from volcanic tuff; toasted hazelnut, beeswax, smoke, fennel fronds and a saline volcanic finish; complex, age-worthy and singular.")
if n2:
    PAIR(pr2, "Spaghetti alle vongole veraci", "complement", "classic", "main", "Saline volcanic Fiano mirrors clam brine; toasted hazelnut bridges pasta richness.")
    PAIR(pr2, "Pan-fried gurnard with caper and lemon butter", "complement", "established", "fish_course", "Mineral smoke and beeswax echo gurnard's character; capers amplify wine's salinity.")
    PAIR(pr2, "Mozzarella di bufala with summer truffles", "complement", "established", "starter", "Hazelnut and smoke bridge truffle; Fiano's beeswax matches creamy buffalo mozzarella.")
    PAIR(pr2, "Grilled sea bream with wild fennel", "complement", "established", "fish_course", "Fennel note in wine resonates with wild fennel; volcanic mineral amplifies sea fish.")

# ── Region 3: Txakoli / Bizkaiko Txakolina ───────────────────────────────────
print("=== Region 3: Bizkaiko Txakolina ===")
r = R("Bizkaiko Txakolina", "Spain", "wine",
      designation_type="DO", designation_name="Bizkaiko Txakolina DO",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Basque Country's Atlantic coastal denomination; Hondarrabi Zuri produces Spain's most electrifying, bracingly acidic white wine; slight pétillance and intense marine salinity.",
      key_producers="Itsasmendi, Berroja, Doniene Gorrondona",
      historical_context="Txakoli (also Chacolí) is the indigenous wine of Basque Country; Getariako Txakolina is more famous but Bizkaiko is the largest DO; consumed with pintxos throughout Bilbao.")
VIN(r, 2023, "excellent", "rising", "Cool Atlantic year; pristine Hondarrabi Zuri with electric acidity.")
VIN(r, 2022, "very_good", "stable", "Warm year; riper Txakoli with more body than usual; slight tropical notes.")
VIN(r, 2021, "excellent", "stable", "Classic Basque profile; lean, saline, vibrant Hondarrabi Zuri.")
VIN(r, 2020, "very_good", "stable", "Good balance; food-friendly Txakoli with characteristic spritz and salinity.")
VIN(r, 2019, "excellent", "stable", "Fine Atlantic year; typical lean, citrus-driven Txakoli.")
p1 = P("Itsasmendi", "winery", r, "Spain",
       production_philosophy="sustainable",
       philosophy_description="Premium Bizkaiko Txakolina producer; Artizar (Basque for star) is their amphora-aged Hondarrabi Zuri; also produces Hondarrabi Beltza red Txakoli.",
       reputation_narrative="The benchmark estate for serious Bizkaiko Txakolina; Artizar proves Hondarrabi Zuri can produce complex, age-worthy white wine.",
       price_positioning="mid_range")
p2 = P("Berroja", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Small boutique Txakoli estate; estate-bottled Hondarrabi Zuri from slate and limestone; low yields; benchmark for the appellation's Atlantic mineral character.",
       reputation_narrative="Berroja's focused, mineral Txakoli is among the DO's most acclaimed; demonstrates the appellation's overlooked quality potential.",
       price_positioning="mid_range")
pr1, n1 = PROD("Itsasmendi Artizar Txakoli", "wine_still", p1, r, "Spain",
               subcategory="Hondarrabi Zuri", price_tier="mid_range",
               description="Amphora-aged Hondarrabi Zuri; textured and complex far beyond the regional norm — lemon curd, white clay, sea spray and a beeswax-tinged finish; the most serious Txakoli made.")
if n1:
    PAIR(pr1, "Grilled spider crab with lemon and herbs", "complement", "classic", "fish_course", "Atlantic mineral echoes crab's sea character; lemon-citrus bridge; texture matches richness.")
    PAIR(pr1, "Angulas (baby eels) with garlic and chilli", "complement", "classic", "starter", "Basque regional delicacy pairing; saline mineral wine amplifies baby eel's oceanic character.")
    PAIR(pr1, "Kokotxas al pil-pil (cod cheeks in garlic emulsion)", "complement", "classic", "main", "The great Basque seafood pairing; wine's texture matches emulsion; minerality echoes cod.")
    PAIR(pr1, "Oysters with Txakoli mignonette", "complement", "classic", "aperitif", "Perfect Basque marriage; wine used in mignonette and drunk alongside oysters; pure Atlantic.")
pr2, n2 = PROD("Berroja Txakoli Bizkaiko", "wine_still", p2, r, "Spain",
               subcategory="Hondarrabi Zuri", price_tier="mid_range",
               description="Classic Bizkaiko Txakoli; electric acidity, sea spray, lemon zest and green apple with a brisk natural spritz; the quintessential pintxos wine.")
if n2:
    PAIR(pr2, "Pintxos assortment with anchovies and peppers", "complement", "classic", "aperitif", "The defining Basque pairing; Txakoli's acidity and spritz match bite-sized pintxos perfectly.")
    PAIR(pr2, "Grilled sardines with sea salt and olive oil", "complement", "classic", "starter", "Atlantic affinity; saline wine echoes grilled sardine's ocean character.")
    PAIR(pr2, "Tuna belly marmitako (potato and tuna stew)", "complement", "established", "main", "Basque regional classic; wine's acidity and spritz refresh hearty tuna stew.")
    PAIR(pr2, "Grilled sea bass with roasted peppers", "complement", "established", "fish_course", "Marine mineral amplifies sea bass; pepper sweetness bridges wine's fresh acidity.")

# ── Region 4: Penedès — Cava production zone ─────────────────────────────────
print("=== Region 4: Cava DO ===")
r = R("Cava DO", "Spain", "wine",
      designation_type="DO", designation_name="Cava DO",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Spain's traditional method sparkling wine denomination centred in Penedès; Xarel·lo, Macabeu and Parellada grapes; new Cava de Paraje Calificado category raises quality ceiling.",
      key_producers="Recaredo, Gramona, Raventós i Blanc, Castellroig",
      historical_context="Método tradicional Cava begun by Josep Raventós at Codorníu in 1872; now produces 250 million bottles annually; top Reserva and Gran Reserva rival Champagne for complexity.")
VIN(r, 2019, "exceptional", "rising", "Outstanding base wine vintage; top Gran Reserva Cavas of extraordinary depth.")
VIN(r, 2018, "excellent", "rising", "Classic year; benchmark Gran Reserva Cavas aging beautifully.")
VIN(r, 2017, "excellent", "stable", "Good base wines; Recaredo and Gramona Gran Reservas show fine aging character.")
VIN(r, 2016, "very_good", "stable", "Solid vintage; reliable Reserva and Gran Reserva Cava of consistent quality.")
VIN(r, 2015, "excellent", "rising", "Excellent year; Cava de Paraje Calificado from this vintage are now showing remarkable complexity.")
p1 = P("Recaredo", "winery", r, "Spain",
       production_philosophy="biodynamic",
       philosophy_description="Certified biodynamic Cava producer; minimum 30 months on lees for Reserva Particular; Terrers is their single-vineyard icon; zero dosage; indigenous yeasts throughout.",
       reputation_narrative="The reference house for serious, terroir-driven Cava; Recaredo's Terrers is Spain's most critically acclaimed sparkling wine.",
       price_positioning="premium")
p2 = P("Raventós i Blanc", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="The Raventós family left the Cava DO to focus on the new Conca del Riu Anoia terroir classification; biodynamic; Blanc de Blancs from Xarel·lo-dominant old vines; L'Hereu is their classic.",
       reputation_narrative="Josep Maria Raventós i Blanc elevated Spanish sparkling wine's credibility; L'Hereu is a benchmark for Penedès method-traditionnelle sparkling.",
       price_positioning="mid_range")
pr1, n1 = PROD("Recaredo Terrers Brut Nature Gran Reserva Cava", "wine_sparkling", p1, r, "Spain",
               subcategory="Xarel·lo blend", price_tier="premium",
               description="Iconic single-vineyard Gran Reserva Cava; 60+ months on lees; toasted bread, lemon curd, chalk mineral and a fine, persistent mousse; Spain's finest sparkling wine.")
if n1:
    PAIR(pr1, "Grilled langoustines with sea salt and alioli", "complement", "classic", "fish_course", "Mineral-toasted Cava elevates langoustine sweetness; fine bubbles amplify crustacean delicacy.")
    PAIR(pr1, "Aged Ibérico ham with pan amb tomàquet", "complement", "classic", "aperitif", "Classic Catalan aperitif; Cava's fine mousse and toast mirror Ibérico fat.")
    PAIR(pr1, "Seared foie gras with quince reduction", "complement", "established", "starter", "Toasted complexity and acidity cut foie richness; quince mirrors wine's stone fruit.")
    PAIR(pr1, "Oysters with yuzu mignonette", "complement", "established", "aperitif", "Mineral mousse and fine bead suit oysters; yuzu echoes wine's citrus.")
pr2, n2 = PROD("Raventós i Blanc L'Hereu Blanc de Blancs", "wine_sparkling", p2, r, "Spain",
               subcategory="Xarel·lo blend", price_tier="mid_range",
               description="Xarel·lo, Macabeu and Parellada Blanc de Blancs; mineral, precise and food-friendly; lemon, fresh brioche, chalk and an elegant persistent bead; benchmark entry sparkling.")
if n2:
    PAIR(pr2, "Catalan escalivada crostini with anchovies", "complement", "classic", "aperitif", "Fine bubbles lift roasted pepper and anchovy; mineral acidity bridges salinity.")
    PAIR(pr2, "Jamón ibérico de bellota with fresh figs", "complement", "classic", "aperitif", "The definitive Spanish aperitif pairing; Blanc de Blancs minerality mirrors cured fat.")
    PAIR(pr2, "Steamed mussels with white wine and saffron", "complement", "established", "starter", "Mineral bubbles echo mussel brine; saffron bridges wine's warm spice note.")
    PAIR(pr2, "Grilled white asparagus with romesco", "complement", "suggested", "starter", "Catalan pairing; wine's mineral freshness amplifies asparagus; romesco adds earthiness.")

# ── Region 5: Bierzo ──────────────────────────────────────────────────────────
print("=== Region 5: Bierzo ===")
r = R("Bierzo", "Spain", "wine",
      designation_type="DO", designation_name="Bierzo DO",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Northwest Spanish valley on the Camino de Santiago; Mencía grape on slate and quartzite soils produces wines of Burgundian elegance — light colour, wild red fruit and mineral precision.",
      key_producers="Álvaro Palacios, Bodegas Estefanía, Dominio de Tares, Descendientes de J. Palacios",
      historical_context="Álvaro Palacios's nephew Ricardo Pérez Palacios revealed Bierzo's potential in the late 1990s; Corullón old vines became Spain's most discussed emerging terroir.")
VIN(r, 2022, "excellent", "rising", "Cool year; Mencía of Burgundian precision and fresh red fruit character.")
VIN(r, 2021, "very_good", "stable", "Good balance; elegant, aromatic Mencía with classic slate-mineral finish.")
VIN(r, 2020, "exceptional", "rising", "Benchmark Bierzo year; old-vine Mencía of extraordinary concentration and finesse.")
VIN(r, 2019, "excellent", "stable", "Classic cool-climate character; Mencía showing wild red cherry and iron minerality.")
VIN(r, 2018, "very_good", "stable", "Warm vintage; richer, plush Mencía; top single-vineyards excelled.")
p1 = P("Descendientes de J. Palacios", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Ricardo Pérez Palacios and Álvaro Palacios's project; single-vineyard Mencías from Corullón; El Bierzo (entry), Corullón, Las Lamas and Moncerbal are their progression.",
       reputation_narrative="Descendientes put Bierzo on the world wine map; Las Lamas and Moncerbal single vineyards are among Spain's most sought-after red wines.",
       price_positioning="premium")
p2 = P("Bodegas Estefanía", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Boutique Bierzo estate; Tilenus Mencía from slate vineyards at 800m altitude; Pagos de Posada is their single-parcel flagship from 80-year-old vines.",
       reputation_narrative="Estefanía's Tilenus demonstrates Bierzo's altitude-driven elegance; benchmark estate wines at accessible prices.",
       price_positioning="mid_range")
pr1, n1 = PROD("Descendientes de J. Palacios Las Lamas Mencía", "wine_still", p1, r, "Spain",
               subcategory="Mencía", price_tier="premium",
               description="Single-vineyard Las Lamas from pre-phylloxera Mencía on slate; red cherry, wild raspberry, iron, graphite and a silky, Pinot-like lightness; among Spain's most elegant reds.")
if n1:
    PAIR(pr1, "Roast suckling pig (cochinillo) with herbs", "complement", "classic", "main", "Galician regional tradition; Mencía's silky tannins suit delicate suckling pig skin.")
    PAIR(pr1, "Grilled salmon with sorrel and capers", "complement", "established", "fish_course", "Light Mencía suits oily salmon; iron note echoes fish's mineral character; sorrel bridges acidity.")
    PAIR(pr1, "Wild mushroom risotto with Manchego", "complement", "established", "main", "Iron-mineral Mencía resonates with wild mushroom; silky tannins suit creamy risotto.")
    PAIR(pr1, "Rabbit braised in white wine with thyme", "complement", "suggested", "main", "Burgundian-style pairing; light red suits delicate rabbit; thyme bridges herbal notes.")
pr2, n2 = PROD("Tilenus Pagos de Posada Mencía", "wine_still", p2, r, "Spain",
               subcategory="Mencía", price_tier="mid_range",
               description="Old-vine single-parcel Mencía at 800m altitude on blue slate; transparent ruby, wild strawberry, violet, iron and an elegant mineral finish of great persistence.")
if n2:
    PAIR(pr2, "Empanada gallega (Galician meat pie)", "complement", "classic", "main", "Northwest Spanish pairing; light Mencía suits pastry-enclosed filling; iron echoes meat filling.")
    PAIR(pr2, "Grilled octopus with paprika and potatoes", "complement", "established", "main", "Galician classic; wine's iron and mineral suit smoked paprika; light body matches octopus.")
    PAIR(pr2, "Lacón con grelos (salt pork with turnip tops)", "complement", "classic", "main", "Classic Galician dish; Mencía's acidity and freshness cut pork fat; greens bridge bitterness.")
    PAIR(pr2, "Steak tartare with shallots and Dijon mustard", "complement", "adventurous", "starter", "Light Mencía suits raw beef's delicacy; iron resonates; mustard bridges mineral notes.")

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
