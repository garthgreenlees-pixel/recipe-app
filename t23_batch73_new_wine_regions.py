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

# ── Batch 73 ──────────────────────────────────────────────────────────────────
# Regions: Niagara Peninsula, Prince Edward County, Jura, Savoie, Cannonau di Sardegna

# ── Region 1: Niagara Peninsula ───────────────────────────────────────────────
print("\n=== Region 1: Niagara Peninsula ===")
r1 = R("Niagara Peninsula", "Canada", "wine",
    designation_type="VQA",
    designation_name="Niagara Peninsula VQA",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Ontario's premier wine region benefiting from Lake Ontario and Lake Erie moderation, producing world-class Icewine, age-worthy Riesling, Chardonnay and increasingly refined Pinot Noir and Cabernet Franc.",
    key_producers="Inniskillin, Jackson-Triggs, Flat Rock Cellars, Malivoire, Cave Spring, Tawse Winery",
    historical_context="Canada's most established wine region and the birthplace of Vidal Icewine; Niagara earned international recognition at the 1991 VinExpo when Inniskillin's Icewine won the Grand Prix d'Honneur."
)
VIN(r1, 2022, "excellent", "stable", "Excellent Ontario vintage; warm summer with cool harvest temperatures produced wines of great balance.")
VIN(r1, 2021, "very_good", "stable", "Good quality across all varieties; Riesling and Chardonnay particularly successful.")
VIN(r1, 2020, "good", "stable", "Reliable vintage; Pinot Noir and Cabernet Franc showed elegance from cooler conditions.")
VIN(r1, 2019, "excellent", "rising", "Near-perfect Niagara year; wines of exceptional concentration and freshness.")
VIN(r1, 2018, "very_good", "stable", "Classic Ontario season; Chardonnay and Riesling both outstanding.")

p1a = P("Tawse Winery", "winery", r1, "Canada",
    production_philosophy="biodynamic",
    philosophy_description="Multi-award-winning biodynamic Niagara estate producing benchmark Chardonnay, Pinot Noir and Riesling with a commitment to minimal intervention and terroir expression.",
    reputation_narrative="Tawse was Canada's Winery of the Year four times at the National Wine Awards; the Quarry Road Chardonnay is consistently ranked among Canada's finest whites.",
    price_positioning="premium")
prod1a, new1a = PROD("Tawse Quarry Road Chardonnay", "wine_still", p1a, r1, "Canada",
    subcategory="Chardonnay",
    description="Benchmark Niagara Chardonnay from biodynamic estate: white peach, lemon curd, grilled hazelnut, subtle oak and vibrant lake-influenced freshness.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Butter-poached Ontario lobster with tarragon", "complement", "classic", "main", "Rich crustacean and Chardonnay is a global classic; tarragon bridges the wine's herbal edge.")
    PAIR(prod1a, "Pan-roasted pickerel with lemon butter and capers", "complement", "classic", "fish_course", "Local Ontario freshwater fish and Niagara Chardonnay is the definitive regional pairing.")
    PAIR(prod1a, "Chicken breast stuffed with goat's cheese and herbs", "complement", "established", "main", "Tangy chèvre and herbed poultry align with Chardonnay's richness and acidity.")
    PAIR(prod1a, "Triple cream cheese with brioche and apple jelly", "bridge", "suggested", "cheese", "Cream cheese fat mirrors the wine's texture; apple jelly bridges with Chardonnay's fruit.")

p1b = P("Cave Spring Cellars", "winery", r1, "Canada",
    production_philosophy="terroir_expression",
    philosophy_description="Niagara's oldest and most venerated estate for Riesling; Cave Spring's Beamsville Bench vineyards produce Ontario's benchmark dry Riesling with striking lake-influenced freshness.",
    reputation_narrative="Cave Spring CSV Riesling is Canada's most celebrated Riesling and a consistent benchmark for cool-climate Riesling quality worldwide.",
    price_positioning="premium")
prod1b, new1b = PROD("Cave Spring CSV Riesling", "wine_still", p1b, r1, "Canada",
    subcategory="Riesling",
    description="Ontario's benchmark Riesling: lime zest, green apple, white peach, slate minerality and crystalline acidity; dry, precise and built for 10+ years of ageing.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Peking duck with hoisin, cucumber and spring onion", "complement", "classic", "main", "Dry Riesling's acidity cuts through duck fat; citrus and mineral notes counterbalance hoisin richness.")
    PAIR(prod1b, "Thai green curry with coconut milk and jasmine rice", "complement", "classic", "main", "Riesling's natural acidity and residual tension manage spice heat while amplifying aromatic complexity.")
    PAIR(prod1b, "Smoked trout pâté with dill and rye crackers", "complement", "established", "starter", "Smoked fish and Riesling is a proven pairing; dill bridges the wine's green apple note.")
    PAIR(prod1b, "Alsatian-style pork and sauerkraut (choucroute)", "complement", "established", "main", "Classic Riesling pairing from its adopted European context; acidity cuts through pork fat.")

# ── Region 2: Prince Edward County ───────────────────────────────────────────
print("\n=== Region 2: Prince Edward County ===")
r2 = R("Prince Edward County", "Canada", "wine",
    designation_type="VQA",
    designation_name="Prince Edward County VQA",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Island wine region in Lake Ontario, Canada's fastest-growing appellation, producing Burgundy-inspired Pinot Noir and Chardonnay on limestone Hillier clay soils with cool lake-moderated climate.",
    key_producers="Norman Hardie Winery, Closson Chase, Grange of Prince Edward, Hinterland Wine Company",
    historical_context="Prince Edward County was granted VQA status in 2007 and has quickly earned a reputation as Canada's answer to Burgundy; the Hillier limestone soils produce Pinot Noir of striking Burgundian character."
)
VIN(r2, 2022, "excellent", "rising", "Outstanding PEC vintage; Pinot Noir of remarkable delicacy and Chardonnay of great mineral tension.")
VIN(r2, 2021, "very_good", "stable", "Good quality; limestone character clearly expressed in both reds and whites.")
VIN(r2, 2020, "good", "stable", "Reliable vintage; approachable Pinot with red cherry and earthy notes.")
VIN(r2, 2019, "excellent", "rising", "Benchmark County year; wines of exceptional aromatic purity and cool-climate elegance.")
VIN(r2, 2018, "very_good", "stable", "Good growing season; Chardonnay and Pinot Noir both showed Burgundian character.")

p2a = P("Norman Hardie Winery", "winery", r2, "Canada",
    production_philosophy="minimal_intervention",
    philosophy_description="Norm Hardie's benchmark County estate producing unoaked Chardonnay and delicate Pinot Noir from limestone Hillier soils using minimal sulphur and no additions.",
    reputation_narrative="Norman Hardie is PEC's most critically acclaimed producer; the County Pinot Noir is considered Canada's finest Burgundy-style red wine.",
    price_positioning="premium")
prod2a, new2a = PROD("Norman Hardie County Pinot Noir", "wine_still", p2a, r2, "Canada",
    subcategory="Pinot Noir",
    description="Canada's benchmark Pinot Noir from limestone County terroir — wild cherry, dried rose, iron, forest floor and fynbos-like dried herb with fine silky tannins and a long mineral finish.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Duck breast with cherry reduction and parsnip purée", "complement", "classic", "main", "Classic Pinot pairing; duck's gamey richness and cherry mirror the wine's profile exactly.")
    PAIR(prod2a, "Wild mushroom and truffle risotto", "complement", "established", "main", "Forest floor and earthy mushroom amplify the wine's Burgundian character.")
    PAIR(prod2a, "Roasted quail with lentils and bacon lardons", "complement", "established", "main", "Small gamey bird is the ideal weight for delicate County Pinot; lentil earth and bacon salt anchor the pairing.")
    PAIR(prod2a, "Aged Comté with wild honey and walnut", "complement", "established", "cheese", "Nutty aged Comté mirrors Pinot's earthy complexity; walnut and honey bridge fruit and mineral notes.")

p2b = P("Closson Chase Vineyards", "winery", r2, "Canada",
    production_philosophy="terroir_expression",
    philosophy_description="One of Prince Edward County's pioneering estates, producing elegant County Chardonnay and Pinot Noir from the Hillier clay-limestone terroir.",
    reputation_narrative="Closson Chase South Clos Chardonnay is consistently considered one of Canada's most distinguished Chardonnays for its combination of richness and mineral precision.",
    price_positioning="premium")
prod2b, new2b = PROD("Closson Chase South Clos Chardonnay", "wine_still", p2b, r2, "Canada",
    subcategory="Chardonnay",
    description="PEC's benchmark Chardonnay from limestone South Clos vineyard — nectarine, white flowers, chalk, toasted brioche and a long saline finish; Burgundy-inspired in structure.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Seared scallops with pea purée and crispy pork belly", "complement", "classic", "fish_course", "Sweet scallop and Chardonnay; pork belly adds savoury richness that matches the wine's weight.")
    PAIR(prod2b, "Morel mushroom omelette with crème fraîche", "bridge", "established", "main", "Earthy spring morels and egg richness bridge the wine's chalk and stone fruit notes.")
    PAIR(prod2b, "Ontario corn-fed chicken roasted with tarragon and lemon", "complement", "established", "main", "Regional match: Ontario chicken with Ontario Chardonnay; tarragon bridges the wine's herbaceous edge.")
    PAIR(prod2b, "Époisses with toasted brioche", "bridge", "adventurous", "cheese", "Washed-rind cheese intensity is tamed by Chardonnay's fruit and acidity; brioche softens both.")

# ── Region 3: Jura ────────────────────────────────────────────────────────────
print("\n=== Region 3: Jura ===")
r3 = R("Jura", "France", "wine",
    designation_type="AOC",
    designation_name="Côtes du Jura AOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Small, distinctive eastern French wine region producing unique Vin Jaune, Savagnin, Chardonnay and Trousseau; Vin Jaune's oxidative nutty complexity rivals Fino Sherry and is unlike any other wine in the world.",
    key_producers="Henri Maire, Jean-François Ganevat, Domaine Overnoy, Jacques Puffeney, Domaine Tissot",
    historical_context="Jura's Vin Jaune is produced from Savagnin aged 6 years in barrels without topping up, developing a distinctive voile (veil) of yeast; the region's wines were beloved by Pasteur, who was born here."
)
VIN(r3, 2020, "excellent", "rising", "Exceptional Jura vintage; Savagnin and Chardonnay of remarkable freshness with good ageing potential.")
VIN(r3, 2019, "very_good", "stable", "Consistent quality; Vin Jaune candidates show good structure and walnut character.")
VIN(r3, 2018, "exceptional", "rising", "Outstanding year across all Jura appellations; Vin Jaune 2018 will be a benchmark.")
VIN(r3, 2017, "good", "stable", "Good vintage despite spring frost; wines show characteristic Jura restraint.")
VIN(r3, 2016, "very_good", "stable", "Solid Jura year; Savagnin and Chardonnay both produced wines of excellent longevity.")

p3a = P("Jean-François Ganevat", "winery", r3, "France",
    production_philosophy="biodynamic",
    philosophy_description="Jura's most celebrated natural wine producer; JF Ganevat farms biodynamically and makes some of the region's most singular and sought-after wines from indigenous varieties.",
    reputation_narrative="Ganevat's wines are among the most sought-after in the natural wine world; the Chalasse Ploussard and various Savagnin expressions command exceptional prices and following.",
    price_positioning="ultra_premium")
prod3a, new3a = PROD("Ganevat La Combe Rotalier Chardonnay", "wine_still", p3a, r3, "France",
    subcategory="Chardonnay",
    description="Jura Chardonnay from biodynamic estate: nutty, oxidative and textural with lemon verbena, toasted almond, chamomile and a distinctive Jurassic mineral character.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Comté cheese (aged 24 months) with walnut bread", "complement", "classic", "cheese", "Jura's greatest wine with Jura's greatest cheese — the walnut and oxidative notes mirror each other perfectly.")
    PAIR(prod3a, "Poulet au Vin Jaune et morilles (chicken with Vin Jaune and morels)", "complement", "classic", "main", "The regional dish par excellence; morel earthiness and oxidative wine in perfect French terroir harmony.")
    PAIR(prod3a, "Seared foie gras with quince paste and toasted brioche", "complement", "established", "starter", "Rich foie and oxidative Chardonnay; quince bridges fruit and the wine's almond-walnut complexity.")
    PAIR(prod3a, "Crayfish bisque with cream and tarragon", "complement", "established", "starter", "River crayfish from Jura streams is the local match; tarragon and cream align with the wine's texture.")

p3b = P("Domaine André et Mireille Tissot", "winery", r3, "France",
    production_philosophy="biodynamic",
    philosophy_description="Arbois-based biodynamic estate producing the full range of Jura wines including Vin Jaune, Savagnin, Poulsard and Trousseau with singular quality and consistency.",
    reputation_narrative="Tissot is Jura's most reliable and widely distributed quality producer; the Arbois Vin Jaune is considered one of the appellation's finest.",
    price_positioning="premium")
prod3b, new3b = PROD("Domaine Tissot Arbois Vin Jaune", "wine_fortified", p3b, r3, "France",
    subcategory="Vin Jaune",
    description="Jura's iconic oxidative wine aged under voile for 6 years: walnuts, curry spice, dried mushroom, beeswax, quince and extraordinary saline-oxidative length; can age 50+ years.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Aged Comté (36 months) with Jura walnuts", "complement", "classic", "cheese", "The canonical Jura pairing — the wine's walnut character mirrors the cheese's aged nuttiness.")
    PAIR(prod3b, "Poulet de Bresse with morel and cream sauce", "complement", "classic", "main", "The dish was invented for Vin Jaune; Bresse chicken richness and mushroom bridge the wine's oxidative depth.")
    PAIR(prod3b, "Chicken liver parfait with Sauternes jelly and brioche", "complement", "established", "starter", "Oxidative richness of the wine handles liver's iron; sweetness in jelly contrasts beautifully.")
    PAIR(prod3b, "Langoustine bisque with saffron and cream", "complement", "adventurous", "starter", "Saffron's earthy-floral note aligns with Vin Jaune's curry spice; cream bridges richness to oxidation.")

# ── Region 4: Savoie ──────────────────────────────────────────────────────────
print("\n=== Region 4: Savoie ===")
r4 = R("Savoie", "France", "wine",
    designation_type="AOC",
    designation_name="Vin de Savoie AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Alpine wine region south-east of Geneva, producing crisp, mineral wines from Jacquère, Roussette de Savoie, Altesse and Mondeuse; wines of striking freshness and Alpine character for food and après-ski.",
    key_producers="Maison Genoux, Domaine Belluard, Château de Ripaille, Domaine Dupasquier, Louis Magnin",
    historical_context="Savoie was part of the Kingdom of Sardinia until 1860; the region's unique Alpine terroir and indigenous grape varieties produce wines unlike anything found elsewhere in France."
)
VIN(r4, 2022, "excellent", "rising", "Exceptional Alpine vintage; Altesse of great aromatic precision and Mondeuse of remarkable depth.")
VIN(r4, 2021, "very_good", "stable", "Good season; wines show the region's characteristic freshness and mineral precision.")
VIN(r4, 2020, "good", "stable", "Consistent quality; Alpine character well expressed across all varieties.")
VIN(r4, 2019, "excellent", "rising", "Outstanding Savoie year; Roussette of extraordinary complexity and Mondeuse of excellent ageing potential.")
VIN(r4, 2018, "very_good", "stable", "Balanced mountain season; elegant wines with remarkable food versatility.")

p4a = P("Domaine Belluard", "winery", r4, "France",
    production_philosophy="biodynamic",
    philosophy_description="Gringet specialist in Ayze producing some of France's most distinctive and sought-after sparkling and still Alpine wines from an ancient pre-phylloxera grape variety.",
    reputation_narrative="Belluard's Les Alpes Gringet is considered one of France's most exciting natural wine discoveries; the grape variety produces wines of extraordinary aromatic complexity and mineral precision.",
    price_positioning="premium")
prod4a, new4a = PROD("Domaine Belluard Les Alpes Gringet", "wine_sparkling", p4a, r4, "France",
    subcategory="Gringet",
    description="Ancient Savoie variety Gringet in sparkling form: meadow flowers, almond, green herb, lemon and vivid Alpine minerality with gentle mousse; distinctive and unlike anything outside Savoie.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Fondue Savoyarde with Comté, Emmental and white wine", "complement", "classic", "main", "The Alpine wine with the Alpine dish — Savoie bubbles and Savoie cheese fondue is the apogee of terroir pairing.")
    PAIR(prod4a, "Trout from mountain streams with almond butter", "complement", "classic", "fish_course", "Alpine freshwater trout with Alpine sparkling wine; almond butter echoes the wine's nutty character.")
    PAIR(prod4a, "Reblochon tart (tartiflette) with lardons and potato", "complement", "established", "main", "The region's quintessential dish with its quintessential sparkling wine; rich cheese and crisp bubbles in balance.")
    PAIR(prod4a, "Charcuterie of cured Alpine meats with gherkins", "complement", "established", "starter", "Cured meats from mountain tradition; sparkling freshness cuts through fat and salt.")

p4b = P("Louis Magnin", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="Benchmark Savoie producer specialising in Roussette de Savoie (Altesse) and Mondeuse with a focus on traditional winemaking and terroir expression from mountain vineyards.",
    reputation_narrative="Louis Magnin's Roussette de Savoie is considered the reference wine for the Altesse variety; the estate defines the category internationally.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Louis Magnin Roussette de Savoie", "wine_still", p4b, r4, "France",
    subcategory="Altesse",
    description="Benchmark Savoie Altesse (Roussette) — apricot, chamomile, hazelnut, white flower and firm Alpine acidity; structured, complex and age-worthy for an Alpine white.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Quenelles de brochet (pike dumplings) with cream sauce", "complement", "classic", "fish_course", "Classic Savoyard-Lyonnaise dish with Savoie white; cream sauce aligns with the wine's weight and texture.")
    PAIR(prod4b, "Ravioles du Dauphiné with brown butter and sage", "complement", "established", "main", "Alpine pasta with Alpine wine; sage echoes the wine's aromatic herbal notes.")
    PAIR(prod4b, "Salade Savoyarde with lardons, Emmental and potato", "complement", "classic", "casual", "Classic mountain salad and the region's white wine — a perfect alpine lunch combination.")
    PAIR(prod4b, "Beaufort cheese with wild honey and hazelnuts", "complement", "classic", "cheese", "Savoie's great alpine cheese with Savoie's benchmark white; hazelnut bridges both.")

# ── Region 5: Cannonau di Sardegna ────────────────────────────────────────────
print("\n=== Region 5: Cannonau di Sardegna ===")
r5 = R("Cannonau di Sardegna", "Italy", "wine",
    designation_type="DOC",
    designation_name="Cannonau di Sardegna DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Sardinia's signature red wine DOC from Cannonau (Grenache) grown on the island's rugged interior, producing full-bodied, sun-drenched reds with dark berry, Mediterranean herbs and distinctive earthy depth.",
    key_producers="Argiolas, Sella & Mosca, Cantina Oliena, Cantina di Orgosolo, Gabbas",
    historical_context="Cannonau is believed to be the oldest form of Grenache in the Mediterranean; DNA evidence suggests it originated in Sardinia before spreading to Spain and France, making it one of the world's most ancient cultivated vines."
)
VIN(r5, 2021, "excellent", "rising", "Exceptional Sardinian vintage; Cannonau shows deep colour and remarkable freshness despite the island's heat.")
VIN(r5, 2020, "very_good", "stable", "Good quality; classic Mediterranean warmth with dark fruit concentration.")
VIN(r5, 2019, "good", "stable", "Consistent vintage; generous, approachable wines with immediate drinking pleasure.")
VIN(r5, 2018, "excellent", "rising", "Outstanding Cannonau year; wines of exceptional depth, herbal complexity and ageing potential.")
VIN(r5, 2017, "very_good", "stable", "Good overall quality; earthy Cannonau with characteristic Mediterranean herbs and dark berry.")

p5a = P("Argiolas", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Sardinia's most celebrated winery, producing the legendary Turriga (barrique-aged Cannonau blend) alongside the appellation-defining Costera Cannonau.",
    reputation_narrative="Argiolas Turriga is considered one of Italy's greatest red wines; the estate put Sardinian wine on the international map and remains its most globally recognised ambassador.",
    price_positioning="premium")
prod5a, new5a = PROD("Argiolas Costera Cannonau di Sardegna", "wine_still", p5a, r5, "Italy",
    subcategory="Cannonau",
    description="Benchmark appellation Cannonau — dark cherry, dried fig, myrtle, rosemary and warm earthy spice; full-bodied, generous and authentically Sardinian.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Roasted suckling pig (porceddu) with rosemary and myrtle", "complement", "classic", "main", "Sardinia's most celebrated dish with its most celebrated grape — myrtle and rosemary echo the wine's wild herb note.")
    PAIR(prod5a, "Lamb with wild herbs on a wood fire (agnello arrosto)", "complement", "classic", "main", "Herb-scented grilled lamb and Cannonau is the definitive Sardinian wine pairing.")
    PAIR(prod5a, "Pasta with bottarga (cured fish roe) and olive oil", "bridge", "adventurous", "main", "Sardinian island ingredient bottarga bridges the gap between seafood and full-bodied red through umami depth.")
    PAIR(prod5a, "Pecorino Sardo aged cheese with chestnut honey", "complement", "established", "cheese", "Sardinian hard ewes' milk cheese with Sardinian red — chestnut honey bridges the fruit and salt.")

p5b = P("Cantina Gabbas", "winery", r5, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Small family estate in Nuoro producing some of Sardinia's most authentic and age-worthy Cannonau from old bush vines in the island's mountainous interior.",
    reputation_narrative="Gabbas Dule Cannonau is celebrated as one of the most individual and terroir-expressive Sardinian wines, prized by critics for its complexity and longevity.",
    price_positioning="premium")
prod5b, new5b = PROD("Gabbas Dule Cannonau di Sardegna", "wine_still", p5b, r5, "Italy",
    subcategory="Cannonau",
    description="Old-vine Nuoro Cannonau of remarkable complexity — dried cherry, wild herbs, Mediterranean garrigue, iron and dark earth; firm, concentrated and built for decade-long ageing.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Wild boar ragù with malloreddus pasta (Sardinian gnocchetti)", "complement", "classic", "main", "The island's traditional pasta with wild game is the quintessential Cannonau partner; tomato and herb bridge beautifully.")
    PAIR(prod5b, "Slow-roasted lamb shoulder with caramelised onion and garlic", "complement", "established", "main", "Rich braised lamb and serious Cannonau — concentrated dark fruit and earthy wine in harmony.")
    PAIR(prod5b, "Grilled beef tagliata with rocket, Parmigiano and truffle oil", "complement", "suggested", "main", "Lean beef and the wine's iron and dark fruit; truffle oil amplifies earthy depth.")
    PAIR(prod5b, "Aged Pecorino Romano with dried figs and walnuts", "complement", "established", "cheese", "Hard ewes' milk cheese with deep Mediterranean red wine — figs bridge the fruit and salt.")

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
