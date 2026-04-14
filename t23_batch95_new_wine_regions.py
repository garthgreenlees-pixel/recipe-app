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

# ── Region 1: Friuli-Venezia Giulia ─────────────────────────────────────────
print("=== Region 1: Friuli Colli Orientali ===")
r = R("Friuli Colli Orientali", "Italy", "wine",
      designation_type="DOC", designation_name="Friuli Colli Orientali DOC",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Eastern Friuli hillside DOC bordering Slovenia; Ponca (flysch) soils produce Italy's most complex Friulano, Ribolla Gialla and white blends; also the home of Ramato (skin-contact Pinot Grigio).",
      key_producers="Miani, Livio Felluga, Dorigo, Ronchi di Cialla",
      historical_context="Friuli's post-WWII white wine revolution, led by Mario Schiopetto, made it Italy's benchmark for crisp, precise whites in the 1970s-80s.")
VIN(r, 2022, "excellent", "rising", "Cool year; precise Friulano and Ribolla Gialla of great mineral definition.")
VIN(r, 2021, "very_good", "stable", "Balanced vintage; textbook Collio-style aromatics and acidity.")
VIN(r, 2020, "excellent", "stable", "Warm but well-ventilated; concentrated whites with good freshness.")
VIN(r, 2019, "exceptional", "rising", "Outstanding year; old-vine Friulano and Ribolla of extraordinary depth.")
VIN(r, 2018, "very_good", "stable", "Classic ponca expression; mineral, food-friendly whites.")
p1 = P("Livio Felluga", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Founding family of modern Friulian white wine; estate-grown across multiple hillside DOCs; Terre Alte is their prestige white blend of Friulano, Pinot Bianco and Sauvignon.",
       reputation_narrative="Livio Felluga's Terre Alte is Italy's most celebrated dry white blend; the estate defined modern Friulian viticulture.",
       price_positioning="premium")
p2 = P("Miani", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Enzo Pontoni's tiny cult estate; micro-yields from old vines; Friulano, Ribolla and Merlot of uncompromising depth; among Italy's most sought-after wines.",
       reputation_narrative="Miani is considered Italy's most sought-after white wine producer; allocations go to Italy's best restaurants.",
       price_positioning="premium")
pr1, n1 = PROD("Livio Felluga Terre Alte", "wine_still", p1, r, "Italy",
               subcategory="Friulano blend", price_tier="premium",
               description="Prestige Friulian white blend of Friulano, Pinot Bianco and Sauvignon; ponca mineral character with stone fruit, white flower and sustained, food-friendly acidity.")
if n1:
    PAIR(pr1, "Seared sea scallops with white truffle butter", "elevate", "established", "fish_course", "Premium Friulian white elevates scallop sweetness; ponca minerality mirrors sea character.")
    PAIR(pr1, "Prosciutto di San Daniele with melon", "complement", "classic", "starter", "Regional Friulian pairing; wine's mineral-stone fruit mirrors cured ham and sweet melon.")
    PAIR(pr1, "Risotto with asparagus and Montasio", "complement", "established", "main", "Friulano's vegetal note echoes asparagus; acidity cuts Montasio richness.")
    PAIR(pr1, "Grilled turbot with lemon and capers", "complement", "classic", "fish_course", "Mineral precision mirrors delicate turbot; acidity echoes lemon; capers bridge salinity.")
pr2, n2 = PROD("Miani Friulano", "wine_still", p2, r, "Italy",
               subcategory="Friulano", price_tier="premium",
               description="Cult micro-production Friulano from old ponca vines; extraordinary mineral depth, almond, white peach and extended finish of remarkable complexity.")
if n2:
    PAIR(pr2, "Grilled langoustine with herb butter", "complement", "classic", "fish_course", "Cult Friulano amplifies langoustine sweetness; almond note echoes crustacean richness.")
    PAIR(pr2, "Frico (Montasio cheese fritter with potatoes)", "complement", "classic", "starter", "Regional Friulian classic; wine's nutty-almond register mirrors fried Montasio.")
    PAIR(pr2, "White asparagus with Parmesan shavings", "complement", "established", "starter", "Vegetal depth and mineral acidity amplify asparagus; Parmesan bridges nuttiness.")
    PAIR(pr2, "Slow-roasted suckling pig with herbs", "bridge", "adventurous", "main", "White wine's mineral complexity bridges pork fat; almond finish echoes roasted herbs.")

# ── Region 2: Marlborough ─────────────────────────────────────────────────────
print("=== Region 2: Marlborough ===")
r = R("Marlborough", "New Zealand", "wine",
      designation_type="GI", designation_name="Marlborough GI",
      reputation_tier="iconic", quality_trajectory="established",
      description="New Zealand's largest wine region at the top of the South Island; cool, sunny climate and free-draining gravels produce the world's benchmark Sauvignon Blanc.",
      key_producers="Cloudy Bay, Dog Point, Fromm, Seresin Estate",
      historical_context="Cloudy Bay's 1985 debut in London created a global frenzy for Marlborough Sauvignon Blanc; now produces 75% of New Zealand's wine.")
VIN(r, 2023, "excellent", "stable", "Classic cool year; vivid, precise Sauvignon with excellent freshness.")
VIN(r, 2022, "very_good", "stable", "Warmer year; riper tropical Sauvignon; Pinot Noir excelled.")
VIN(r, 2021, "exceptional", "rising", "Benchmark year; Sauvignon of rare elegance; Pinot Noir among the best ever.")
VIN(r, 2020, "very_good", "stable", "Dry year; concentrated, textured Sauvignon; Chardonnay shone.")
VIN(r, 2019, "excellent", "stable", "Balanced year; classic cool-climate Sauvignon with trademark passion fruit.")
p1 = P("Dog Point Vineyard", "winery", r, "New Zealand",
       production_philosophy="sustainable",
       philosophy_description="Ivan and Margaret Sutherland (ex-Cloudy Bay) focus on single-vineyard Sauvignon Blanc; Section 94 is wild-yeast fermented and barrel-aged — the region's most serious white.",
       reputation_narrative="Dog Point's Section 94 redefined what Marlborough Sauvignon could be; complex, age-worthy and utterly distinct.",
       price_positioning="mid_range")
p2 = P("Fromm Winery", "winery", r, "New Zealand",
       production_philosophy="terroir_focused",
       philosophy_description="Swiss-owned boutique focused on Pinot Noir, Malbec and Riesling rather than Sauvignon; Old World philosophy in Marlborough; certified biodynamic.",
       reputation_narrative="Fromm demonstrated that Marlborough is more than Sauvignon Blanc; their Pinot Noirs rival Central Otago for complexity.",
       price_positioning="premium")
pr1, n1 = PROD("Dog Point Section 94 Sauvignon Blanc", "wine_still", p1, r, "New Zealand",
               subcategory="Sauvignon Blanc", price_tier="mid_range",
               description="Wild-yeast, barrel-fermented Sauvignon Blanc; complex, textured and age-worthy — roasted herbs, white peach, brioche and long mineral finish; far beyond the regional stereotype.")
if n1:
    PAIR(pr1, "Grilled whole snapper with salsa verde", "complement", "established", "fish_course", "Herb complexity in wine mirrors salsa verde; mineral finish amplifies fresh fish.")
    PAIR(pr1, "Steamed Cloudy Bay clams with white wine", "complement", "classic", "starter", "Regional NZ pairing; wine's mineral-herb notes echo clam brine; texture bridges richness.")
    PAIR(pr1, "Roast chicken with preserved lemon and olives", "complement", "established", "main", "Roasted herb note and white peach bridge chicken and preserved lemon.")
    PAIR(pr1, "Brie de Meaux with herb crackers", "complement", "suggested", "cheese", "Barrel complexity softens Brie's funk; herb notes echo crackers.")
pr2, n2 = PROD("Fromm La Strada Pinot Noir", "wine_still", p2, r, "New Zealand",
               subcategory="Pinot Noir", price_tier="premium",
               description="Biodynamic Marlborough Pinot Noir; darker and spicier than Central Otago — dark cherry, forest floor, clove and silky tannins with considerable aging potential.")
if n2:
    PAIR(pr2, "Grilled salmon with mushroom duxelles", "complement", "established", "fish_course", "Dark Pinot echoes mushroom earthiness; silky tannins grip salmon fat without overpowering.")
    PAIR(pr2, "Duck breast with cherry compote and lentils", "complement", "established", "main", "Cherry-forest floor resonance with duck; clove spice bridges; lentils add earthy weight.")
    PAIR(pr2, "Venison tartare with capers and pickled beetroot", "complement", "adventurous", "starter", "Forest-floor Pinot mirrors raw venison; beetroot echoes wine's red-dark fruit.")
    PAIR(pr2, "Aged Manchego with dried cherries", "complement", "suggested", "cheese", "Dark cherry in wine mirrors dried cherries; silky tannins soften aged cheese.")

# ── Region 3: Nahe ────────────────────────────────────────────────────────────
print("=== Region 3: Nahe ===")
r = R("Nahe", "Germany", "wine",
      designation_type="Einzellage", designation_name="Nahe",
      reputation_tier="prestigious", quality_trajectory="ascending",
      description="Small tributary valley of the Rhine; volcanic and porphyry soils produce Germany's most diverse Riesling expression — from steely-mineral to exotic-spiced; a connoisseur's region.",
      key_producers="Dönnhoff, Emrich-Schönleber, Schäfer-Fröhlich, Kruger-Rumpf",
      historical_context="Dönnhoff's Oberhäuser Brücke GG is one of Germany's most sought-after wines; the volcanic Nahe terroir produces Riesling unlike anywhere else.")
VIN(r, 2021, "exceptional", "rising", "Outstanding cool vintage; Riesling of crystalline precision and remarkable longevity.")
VIN(r, 2020, "excellent", "stable", "Warm year retained freshness; concentrated, generous Riesling.")
VIN(r, 2019, "excellent", "stable", "Classic warm year; exotic spice notes and concentrated fruit.")
VIN(r, 2018, "exceptional", "rising", "Benchmark warm vintage; dry GGs of extraordinary depth and richness.")
VIN(r, 2017, "very_good", "stable", "Late frost reduced yields; surviving wines showed intense concentration.")
p1 = P("Dönnhoff", "winery", r, "Germany",
       production_philosophy="traditional",
       philosophy_description="Helmut and Cornelius Dönnhoff's benchmark Nahe estate; Oberhäuser Brücke and Hermannshöhle GGs; meticulous vineyard work and traditional cellar; benchmark for German Riesling.",
       reputation_narrative="Dönnhoff's Oberhäuser Brücke is Germany's most sublime and age-worthy Riesling; the Nahe's undisputed master.",
       price_positioning="premium")
p2 = P("Emrich-Schönleber", "winery", r, "Germany",
       production_philosophy="terroir_focused",
       philosophy_description="Frank Schönleber's volcanic-terroir estate; Monzinger Frühlingsplätzchen and Halenberg GGs on porphyry and slate; electrifying mineral wines of great aging potential.",
       reputation_narrative="Nahe's most volcanic expression; Emrich-Schönleber Halenberg is among Germany's most complex Rieslings.",
       price_positioning="premium")
pr1, n1 = PROD("Dönnhoff Oberhäuser Brücke Riesling Spätlese", "wine_still", p1, r, "Germany",
               subcategory="Riesling", price_tier="premium",
               description="Legendary off-dry Spätlese from blue-slate Brücke vineyard; apricot, peach, slate, ginger and electrifying acidity; one of Germany's most age-worthy Rieslings.")
if n1:
    PAIR(pr1, "Foie gras terrine with Sauternes gelée", "complement", "established", "starter", "Off-dry Riesling's fruit and acid mirror terrine richness; apricot echoes the gelée.")
    PAIR(pr1, "Roast pork loin with apple and ginger", "complement", "classic", "main", "Off-dry registers ginger note in wine; apple bridges wine's stone fruit and pork fat.")
    PAIR(pr1, "Asian-glazed duck with five-spice", "bridge", "established", "main", "Spätlese sweetness mediates five-spice; acidity cuts duck fat; ginger bridges.")
    PAIR(pr1, "Apricot tart with crème pâtissière", "complement", "suggested", "dessert", "Apricot in wine mirrors tart; off-dry sweetness harmonises without overpowering.")
pr2, n2 = PROD("Emrich-Schönleber Halenberg Riesling GG", "wine_still", p2, r, "Germany",
               subcategory="Riesling", price_tier="premium",
               description="Volcanic porphyry GG; dry and austere; smoke, white pepper, lime oil and an electrifying, seemingly endless mineral finish; needs years to open.")
if n2:
    PAIR(pr2, "Smoked eel with horseradish cream", "complement", "established", "starter", "Volcanic smoke note echoes smoked eel; acidity cuts oily fish richness; horseradish bridges.")
    PAIR(pr2, "River crayfish bisque with dill", "complement", "established", "starter", "Mineral-citrus GG amplifies crayfish sweetness; volcanic character adds complexity.")
    PAIR(pr2, "Japanese sashimi omakase", "complement", "adventurous", "fish_course", "White pepper and smoke pair with soy-dressed fish; mineral length mirrors umami.")
    PAIR(pr2, "Soft-shell crab tempura with ponzu", "complement", "suggested", "starter", "Volcanic minerality and citrus bridge tempura crunch and ponzu tang.")

# ── Region 4: Wairau Valley ──────────────────────────────────────────────────
print("=== Region 4: Wairau Valley ===")
r = R("Wairau Valley", "New Zealand", "wine",
      designation_type="GI", designation_name="Wairau Valley GI",
      reputation_tier="respected", quality_trajectory="established",
      description="The heart of Marlborough; flat, gravelly valley floor of the Wairau River producing classic, vibrant Sauvignon Blanc and increasingly serious Pinot Noir.",
      key_producers="Cloudy Bay, Villa Maria, Huia, Yealands",
      historical_context="The original Marlborough planting site (1973); Cloudy Bay's first vintage here (1985) launched the global Sauvignon Blanc revolution.")
VIN(r, 2023, "very_good", "stable", "Cool, classic year; vivid Sauvignon with green herb and passion fruit.")
VIN(r, 2022, "excellent", "stable", "Warm year; riper tropical-style Sauvignon; excellent Pinot Gris.")
VIN(r, 2021, "exceptional", "rising", "Outstanding year across both red and white; freshness and depth in balance.")
VIN(r, 2020, "very_good", "stable", "Drought stress created concentrated Sauvignon; intense, focused style.")
VIN(r, 2019, "excellent", "stable", "Balanced year; classic passion fruit and herb profile; Pinot Noir excelled.")
p1 = P("Cloudy Bay Vineyards", "winery", r, "New Zealand",
       production_philosophy="sustainable",
       philosophy_description="The estate that launched Marlborough's global reputation; wide range from vibrant estate Sauvignon to Te Koko (barrel-fermented) and Pelorus sparkling.",
       reputation_narrative="Cloudy Bay's debut in 1985 created one of wine's most storied success stories; still one of the world's most recognised wine brands.",
       price_positioning="mid_range")
p2 = P("Huia Vineyards", "winery", r, "New Zealand",
       production_philosophy="sustainable",
       philosophy_description="Claire and Mike Allan's biodynamic-aspiring estate; certified sustainable; Méthode Traditionnelle sparkling and serious Pinot Noir alongside benchmark Sauvignon.",
       reputation_narrative="Huia produces Marlborough's most serious sparkling wines alongside complex Pinot Noir and Gewurztraminer of cult following.",
       price_positioning="mid_range")
pr1, n1 = PROD("Cloudy Bay Sauvignon Blanc", "wine_still", p1, r, "New Zealand",
               subcategory="Sauvignon Blanc", price_tier="mid_range",
               description="The original benchmark Marlborough Sauvignon; passion fruit, gooseberry, fresh herb and vibrant citrus; crisp, clean and immediately appealing.")
if n1:
    PAIR(pr1, "Marlborough green-lipped mussels with herb butter", "complement", "classic", "starter", "Regional NZ pairing; wine's grassiness mirrors mussel brine; herb notes align.")
    PAIR(pr1, "Goat's cheese bruschetta with fresh herbs", "complement", "classic", "starter", "Classic Sauvignon pairing; grassiness cuts goat's cheese tang; herbs bridge.")
    PAIR(pr1, "Grilled asparagus with lemon and Parmesan", "complement", "established", "starter", "Vegetal-citrus wine mirrors asparagus character; Parmesan bridges mineral-umami.")
    PAIR(pr1, "Thai fish cakes with sweet chilli sauce", "complement", "suggested", "starter", "Herbaceous notes echo Thai herbs; citrus acidity cuts fish fat; sweetness bridges chilli.")
pr2, n2 = PROD("Huia Marlborough Gewurztraminer", "wine_still", p2, r, "New Zealand",
               subcategory="Gewurztraminer", price_tier="mid_range",
               description="Aromatic Marlborough Gewurztraminer; lychee, rose petal, ginger and Turkish delight; off-dry with excellent acidity and considerable food versatility.")
if n2:
    PAIR(pr2, "Peking duck pancakes with hoisin", "complement", "classic", "main", "Lychee and rose mirror hoisin sweetness; ginger bridges duck fat and spice.")
    PAIR(pr2, "Moroccan lamb tagine with preserved lemon", "bridge", "established", "main", "Aromatic wine bridges spiced lamb and preserved lemon; off-dry sweetness mediates heat.")
    PAIR(pr2, "Spiced butternut squash soup with coconut", "complement", "suggested", "starter", "Rose and ginger echo warming spices; off-dry sweetness mirrors squash's natural sugar.")
    PAIR(pr2, "Mango and chilli prawn salad", "complement", "adventurous", "starter", "Lychee-mango resonance; acidity bridges chilli heat; off-dry sweetness lifts shellfish.")

# ── Region 5: Vinho Verde ────────────────────────────────────────────────────
print("=== Region 5: Vinho Verde ===")
r = R("Vinho Verde", "Portugal", "wine",
      designation_type="DOC", designation_name="Vinho Verde DOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Northwestern Portugal's Atlantic wine region; Loureiro, Alvarinho and Arinto produce Portugal's most refreshing whites; Melgaço and Monção sub-regions produce world-class Alvarinho.",
      key_producers="Quinta do Ameal, Anselmo Mendes, Soalheiro, Adega de Monção",
      historical_context="'Vinho Verde' means 'young wine'; historically consumed young and slightly sparkling; now top Alvarinho rivals Rías Baixas for seriousness and longevity.")
VIN(r, 2023, "excellent", "rising", "Cool Atlantic year; pristine acidity and aromatic intensity in Alvarinho.")
VIN(r, 2022, "very_good", "stable", "Warmer year; rounder Loureiro; concentrated Alvarinho from Monção.")
VIN(r, 2021, "excellent", "stable", "Classic Atlantic profile; bright, mineral Alvarinho with exceptional freshness.")
VIN(r, 2020, "very_good", "stable", "Balanced year; top sub-regional Alvarinho showed impressive depth.")
VIN(r, 2019, "exceptional", "rising", "Outstanding year; Alvarinho of great concentration and aging potential.")
p1 = P("Soalheiro", "winery", r, "Portugal",
       production_philosophy="sustainable",
       philosophy_description="João Esteves da Silva's pioneering Monção Alvarinho estate; granite soils; stainless steel and barrel-aged expressions; Primeiras Vinhas from old vines is their flagship.",
       reputation_narrative="Soalheiro put Alvarinho on the world stage; Primeiras Vinhas is Portugal's benchmark single-variety Alvarinho.",
       price_positioning="mid_range")
p2 = P("Anselmo Mendes", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Top Vinho Verde winemaker known for single-vineyard Alvarinho bottlings; Parcela Única shows the variety's limestone and granite terroir contrasts.",
       reputation_narrative="Portugal's leading Alvarinho specialist; Parcela Única bottlings are among the denomination's most sought-after whites.",
       price_positioning="mid_range")
pr1, n1 = PROD("Soalheiro Alvarinho", "wine_still", p1, r, "Portugal",
               subcategory="Alvarinho", price_tier="mid_range",
               description="Benchmark Monção Alvarinho; lime blossom, peach, mineral granite and saline finish; vibrant acidity and versatile food pairing potential.")
if n1:
    PAIR(pr1, "Grilled sardines with piri-piri and lemon", "complement", "classic", "main", "Portuguese regional pairing; saline-citrus wine echoes chargrilled sardine richness.")
    PAIR(pr1, "Octopus à la lagareiro (roasted with olive oil)", "complement", "classic", "main", "Granite mineral and citrus amplify tender octopus; olive oil richness balanced by acidity.")
    PAIR(pr1, "Tempura prawns with yuzu mayo", "complement", "suggested", "starter", "Citrus notes echo yuzu; mineral finish cuts tempura fat; acidity refreshes.")
    PAIR(pr1, "Salt cod fritters (pastéis de bacalhau)", "complement", "classic", "starter", "Classic Portuguese pairing; saline wine mirrors salt cod; acidity cuts frying oil.")
pr2, n2 = PROD("Anselmo Mendes Parcela Única Alvarinho", "wine_still", p2, r, "Portugal",
               subcategory="Alvarinho", price_tier="mid_range",
               description="Single-parcel old-vine Alvarinho from granite; stone fruit, jasmine, quince and a mineral-saline persistence; more structured and complex than the regional norm.")
if n2:
    PAIR(pr2, "Grilled lobster with garlic and herbs", "complement", "established", "fish_course", "Structured Alvarinho matches lobster richness; mineral-saline amplifies sweetness.")
    PAIR(pr2, "Barnacle (percebes) with sea salt", "complement", "classic", "aperitif", "Saline mineral Alvarinho and briny barnacles: the ultimate Atlantic pairing.")
    PAIR(pr2, "Sea bream in salt crust with capers", "complement", "established", "fish_course", "Mineral-saline wine echoes salt-crust seasoning; acidity amplifies delicate fish.")
    PAIR(pr2, "Thai green papaya salad with dried shrimp", "complement", "adventurous", "starter", "Saline umami notes bridge dried shrimp; citrus and herb echo Thai herb dressing.")

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
