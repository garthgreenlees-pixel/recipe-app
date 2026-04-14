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

# ── REGION 1: Picpoul de Pinet (France) — already in DB, check ──────────────
# Actually targeting: Pouilly-sur-Loire, Quincy, Reuilly, Menetou-Salon, Coteaux du Giennois

print("=== Region 1: Pouilly-sur-Loire ===")
r1 = R("Pouilly-sur-Loire", "France", "wine",
        designation_type="AOC", designation_name="Pouilly-sur-Loire AOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Upper Loire appellation producing Chasselas-based whites alongside Sauvignon Blanc; lighter and more delicate than neighbouring Pouilly-Fumé, offering early-drinking freshness.",
        key_producers="Château de Tracy, Domaine Masson-Blondelet",
        historical_context="One of France's oldest AOCs for white wine; Chasselas fell from fashion but retains niche following for its gentle, neutral character ideal for casual bistro dining.")
VIN(r1, 2022, "very_good", "stable", "Warm summer with balanced acidity; Chasselas shows peachy softness and Sauvignon crisp minerality.")
VIN(r1, 2021, "good", "stable", "Difficult spring frosts reduced yields; remaining wines elegant and fine-boned.")
VIN(r1, 2020, "excellent", "rising", "Concentrated and expressive; one of the decade's finest Loire whites.")
VIN(r1, 2019, "very_good", "stable", "Ripe and generous with good depth; early drinking appeal.")
VIN(r1, 2018, "good", "stable", "Warm vintage; Chasselas rich but less crisp; Sauvignon performed well.")
p1a = P("Château de Tracy", "winery", r1, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Centuries-old estate producing elegant Sauvignon Blanc and traditional Chasselas from flint-rich soils above the Loire.",
        reputation_narrative="One of the Loire's most historic estates; Tracy holdings date to the 15th century and consistently deliver benchmark Pouilly appellation wines.",
        price_positioning="premium",
        authority_tier=2)
p1b = P("Domaine Masson-Blondelet", "winery", r1, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Family domaine working flint and clay soils to produce precise, mineral-driven whites from both Pouilly appellations.",
        reputation_narrative="Highly regarded for consistent quality across Pouilly-Fumé and Pouilly-sur-Loire; beloved by Loire specialists.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Château de Tracy Chasselas Pouilly-sur-Loire", "wine_still", p1a, r1, "France",
                  subcategory="Chasselas",
                  description="Delicate Chasselas with notes of white peach, melon and a soft mineral finish; ideal bistro white.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Gruyère and charcuterie board", "complement", "classic", "casual", "Chasselas neutrality amplifies dairy fat; soft acidity cuts through cured meats without overpowering.")
    PAIR(pr1a, "Steamed river trout with butter sauce", "complement", "established", "fish_course", "Delicate fish mirrors Chasselas lightness; butter sauce bridges the wine's gentle richness.")
    PAIR(pr1a, "Fresh goat's cheese crostini", "complement", "classic", "starter", "Loire goat cheese classic pairing; Chasselas softness balances tang without dominating.")
    PAIR(pr1a, "Quiche Lorraine", "complement", "established", "main", "Egg-cream richness met by refreshing Chasselas acidity; comfort food elevated.")
pr1b, n1b = PROD("Domaine Masson-Blondelet Pouilly-sur-Loire Tradition Cullus", "wine_still", p1b, r1, "France",
                  subcategory="Chasselas",
                  description="Mineral and fresh Chasselas from older vines; more structure and persistence than typical expressions.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Mussel escabèche with saffron", "complement", "established", "starter", "Saffron's floral warmth links to Chasselas fruitiness; briny mussels amplified by mineral finish.")
    PAIR(pr1b, "Salade Niçoise", "complement", "classic", "casual", "Versatile Loire white handles the diverse elements — tuna, olive, egg — with easy-drinking grace.")
    PAIR(pr1b, "Blanquette de veau", "complement", "established", "main", "Cream veal stew needs a wine with enough weight to match without overpowering; Chasselas delivers.")
    PAIR(pr1b, "Tarte flambée (flammekueche)", "complement", "classic", "casual", "Alsatian onion-cream tart loves a soft, non-aggressive white; perfect bistro match.")

print("=== Region 2: Quincy ===")
r2 = R("Quincy", "France", "wine",
        designation_type="AOC", designation_name="Quincy AOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Small Loire appellation near Bourges producing 100% Sauvignon Blanc from gravelly, sandy soils; known for vibrancy, nettle-herb character and stony minerality.",
        key_producers="Domaine Jaumier, Domaine Mardon",
        historical_context="One of France's first Sauvignon Blanc AOCs (1936); long overshadowed by Sancerre but gaining renewed attention for excellent value and distinctive terroir character.")
VIN(r2, 2022, "very_good", "stable", "Bright and expressive; punchy herbaceous character with citrus clarity.")
VIN(r2, 2021, "good", "stable", "Frost-affected yields but remaining wines show elegant restraint.")
VIN(r2, 2020, "excellent", "rising", "Exceptional vintage; depth and concentration unusual for the appellation.")
VIN(r2, 2019, "very_good", "stable", "Ripe tropical notes balanced by trademark stony finish.")
VIN(r2, 2018, "good", "stable", "Warm and generous; slightly less acidic than typical but pleasant drinking.")
p2a = P("Domaine Jaumier", "winery", r2, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Small estate working gravelly soils with minimal intervention to express Quincy's distinctive stony Sauvignon character.",
        reputation_narrative="Reference producer for the appellation; wines consistently cited in Loire specialist press.",
        price_positioning="mid_range",
        authority_tier=1)
p2b = P("Domaine Mardon", "winery", r2, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Family-owned estate producing fresh, direct Sauvignon Blanc with emphasis on purity of fruit and precise winemaking.",
        reputation_narrative="Well-regarded in Loire wine circles; reliable quality across all vintages.",
        price_positioning="mid_range",
        authority_tier=1)
pr2a, n2a = PROD("Domaine Jaumier Quincy Blanc", "wine_still", p2a, r2, "France",
                  subcategory="Sauvignon Blanc",
                  description="Stony, herb-driven Sauvignon Blanc with fresh nettle, flint and grapefruit; quintessential Loire blanc.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Chèvre chaud salad with walnuts", "complement", "classic", "starter", "Loire Sauvignon and goat cheese is a canonical pairing; walnut bitterness adds complexity.")
    PAIR(pr2a, "Asparagus with hollandaise", "complement", "established", "starter", "Herbaceous asparagus mirrors nettle notes; rich hollandaise balanced by vibrant acidity.")
    PAIR(pr2a, "Grilled sardines with lemon", "complement", "classic", "fish_course", "Punchy fish matches punchy wine; citrus bridges and acidity cuts oiliness cleanly.")
    PAIR(pr2a, "Sushi and sashimi assortment", "bridge", "suggested", "fish_course", "Fresh seafood cleaned by crisp minerality; Loire Sauvignon brings unexpected elegance to Japanese fare.")
pr2b, n2b = PROD("Domaine Mardon Quincy Clos des Victoires", "wine_still", p2b, r2, "France",
                  subcategory="Sauvignon Blanc",
                  description="Single-vineyard Quincy with gravel intensity; more structured and persistent than standard cuvée.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Smoked salmon blinis with crème fraîche", "complement", "classic", "starter", "Sauvignon's acidity cuts through smoke and fat; minerality echoes the salinity.")
    PAIR(pr2b, "Herb-crusted sea bass", "complement", "established", "fish_course", "Herb crust links to wine's herbaceous character; flint minerality emphasises sea bass delicacy.")
    PAIR(pr2b, "Green gazpacho with cucumber and basil", "complement", "classic", "starter", "Vivid herb-vegetal soup echoes wine's grassy freshness; shared acidity creates harmony.")
    PAIR(pr2b, "Vegetable tempura with dipping sauce", "bridge", "suggested", "casual", "Crisp batter and delicate vegetables match Loire Sauvignon's crispness and herb notes.")

print("=== Region 3: Reuilly ===")
r3 = R("Reuilly", "France", "wine",
        designation_type="AOC", designation_name="Reuilly AOC",
        reputation_tier="respected",
        quality_trajectory="emerging",
        description="Small Loire appellation producing Sauvignon Blanc whites, Pinot Gris rosés and Pinot Noir reds; soils of marl, sand and flint deliver wines of freshness and aromatic precision.",
        key_producers="Domaine Claude Lafond, Domaine de Reuilly Henri Beurdin",
        historical_context="Ancient appellation revived in the 20th century; overshadowed by Sancerre but increasingly recognised for individual character and competitive value pricing.")
VIN(r3, 2022, "very_good", "stable", "Aromatics lifted and fresh; reds show pretty Pinot character with soft tannins.")
VIN(r3, 2021, "good", "stable", "Challenging year; whites maintained freshness better than reds.")
VIN(r3, 2020, "excellent", "rising", "Exceptional across all three colours; best vintage in a decade.")
VIN(r3, 2019, "very_good", "stable", "Generous and expressive; Sauvignon particularly vibrant.")
VIN(r3, 2018, "good", "stable", "Warm vintage; reds richer than usual, whites slightly softer.")
p3a = P("Domaine Claude Lafond", "winery", r3, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Reuilly estate producing all three appellations colours with emphasis on site-specific expression and minimal intervention.",
        reputation_narrative="The most widely recognised name in Reuilly; wines appear regularly in Loire specialist selections.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Domaine Henri Beurdin", "winery", r3, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Family estate focusing on Reuilly Sauvignon Blanc and Pinot Gris rosé from marl and clay soils.",
        reputation_narrative="Respected local producer; wines offer direct, honest expression of Reuilly terroir.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Domaine Claude Lafond Reuilly Blanc Les Grandes Vignes", "wine_still", p3a, r3, "France",
                  subcategory="Sauvignon Blanc",
                  description="Single-vineyard Reuilly Sauvignon with grassy citrus aromatics, grapefruit and flint; bright and persistent.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Crottin de Chavignol warm salad", "complement", "classic", "starter", "Loire Sauvignon and local goat cheese is an iconic regional pairing.")
    PAIR(pr3a, "Pan-fried pike perch with beurre blanc", "complement", "established", "fish_course", "Classic Loire fish preparation; beurre blanc links butter richness to wine's acidity.")
    PAIR(pr3a, "Cucumber and dill tart", "complement", "established", "starter", "Herb-green freshness mirrors wine's aromatics; a natural fit for garden-to-table dining.")
    PAIR(pr3a, "White asparagus with mousseline sauce", "complement", "classic", "starter", "White asparagus's bitter sweetness amplified by Loire Sauvignon minerality.")
pr3b, n3b = PROD("Domaine Henri Beurdin Reuilly Rosé de Pinot Gris", "wine_still", p3b, r3, "France",
                  subcategory="Pinot Gris",
                  description="Pale copper rosé from Pinot Gris; delicate and dry with peach, spice and mineral freshness.",
                  price_tier="mid_range")
if n3b:
    PAIR(pr3b, "Tuna tartare with sesame", "complement", "established", "starter", "Pinot Gris rosé's spice notes complement sesame; delicate tuna preserved by wine's gentle weight.")
    PAIR(pr3b, "Charcuterie and cornichon platter", "complement", "classic", "casual", "Dry rosé's freshness cuts through cured meats; ideal aperitif or casual board companion.")
    PAIR(pr3b, "Grilled peaches with honey and almonds", "complement", "established", "dessert", "Stone fruit in both glass and plate; honey links sweetness while almonds echo mineral dryness.")
    PAIR(pr3b, "Prawn and avocado cocktail", "complement", "established", "starter", "Classic starter lifted by rosé's gentle freshness and spice; versatile match.")

print("=== Region 4: Menetou-Salon ===")
r4 = R("Menetou-Salon", "France", "wine",
        designation_type="AOC", designation_name="Menetou-Salon AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Limestone and Kimmeridgian clay appellation near Bourges producing elegant Sauvignon Blanc whites and Pinot Noir reds; quality rising rapidly as alternatives to Sancerre.",
        key_producers="Domaine Henry Pellé, Domaine de Chatenoy",
        historical_context="Ancient vine history revived in the 20th century; now firmly establishing itself as the value alternative to Sancerre with shared soil profiles and growing critical acclaim.")
VIN(r4, 2022, "excellent", "rising", "Outstanding vintage; Sauvignon shows Kimmeridgian minerality with intensity and length.")
VIN(r4, 2021, "good", "stable", "Frost damage limited yields; surviving wines elegant and fine.")
VIN(r4, 2020, "very_good", "rising", "Ripe and concentrated; best reds of the decade from this appellation.")
VIN(r4, 2019, "very_good", "stable", "Expressive and generous; Pinot Noir shows surprising depth and colour.")
VIN(r4, 2018, "good", "stable", "Warm vintage; whites rich, reds approachable and fruity.")
p4a = P("Domaine Henry Pellé", "winery", r4, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Menetou-Salon estate working Kimmeridgian clay soils to produce wines that rival Sancerre in quality and complexity.",
        reputation_narrative="Benchmark producer for the appellation; consistently earns scores comparable to Sancerre at lower price points.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Domaine de Chatenoy", "winery", r4, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Menetou-Salon estate with substantial plantings of both Sauvignon Blanc and Pinot Noir; traditional approach with modern precision.",
        reputation_narrative="One of the appellation's oldest names; reliable quality and good distribution.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Domaine Henry Pellé Menetou-Salon Morogues Blanc", "wine_still", p4a, r4, "France",
                  subcategory="Sauvignon Blanc",
                  description="Single-village Sauvignon from Kimmeridgian clay; citrus, white flowers, flint and great persistence.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Sancerre-style goat cheese platter", "complement", "classic", "cheese", "Shared Kimmeridgian terroir with Sancerre; goat cheese is the canonical regional companion.")
    PAIR(pr4a, "Sea scallops with cauliflower purée", "complement", "established", "fish_course", "Scallop sweetness lifted by mineral Sauvignon; cauliflower bridges the wine's texture.")
    PAIR(pr4a, "Oysters with mignonette", "complement", "classic", "starter", "Briny oysters love Kimmeridgian minerality; mignonette acidity in harmony with the wine.")
    PAIR(pr4a, "Poached chicken in cream sauce", "complement", "established", "main", "Loire white's acidity and freshness cuts through cream while matching chicken's delicacy.")
pr4b, n4b = PROD("Domaine de Chatenoy Menetou-Salon Rouge", "wine_still", p4b, r4, "France",
                  subcategory="Pinot Noir",
                  description="Light to medium-bodied Pinot Noir with red cherry, earthiness and a delicate floral note; Loire red at its most charming.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Rabbit terrine with Dijon mustard", "complement", "established", "starter", "Loire Pinot's lightness and earthiness complement rabbit's delicate gaminess; mustard bridges.")
    PAIR(pr4b, "Roasted duck breast with cherries", "complement", "classic", "main", "Cherry fruit in both wine and dish; Loire Pinot lifts duck without overwhelming.")
    PAIR(pr4b, "Mushroom risotto with aged Comté", "complement", "established", "main", "Earthy Pinot loves mushroom; Comté's nuttiness bridges wine's light tannin.")
    PAIR(pr4b, "Charcuterie with Burgundy mustard", "complement", "classic", "casual", "Light Loire red is ideal charcuterie wine; mustard's heat tempered by gentle fruit.")

print("=== Region 5: Coteaux du Giennois ===")
r5 = R("Coteaux du Giennois", "France", "wine",
        designation_type="AOC", designation_name="Coteaux du Giennois AOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Small northerly Loire appellation near Gien producing Sauvignon Blanc whites and Pinot Noir reds from chalk and flint soils; cool climate delivers high-acid, precise wines of great freshness.",
        key_producers="Domaine Poupart, Domaine Poupat & Fils",
        historical_context="Ancient vine culture near Gien; the appellation nearly disappeared in the 20th century but has been revived by quality-focused producers seeking alternatives to Sancerre's prices.")
VIN(r5, 2022, "very_good", "stable", "Bright, crisp vintage; Sauvignon shows pronounced acidity and citrus clarity.")
VIN(r5, 2021, "good", "stable", "Spring frosts; lean whites and light reds from reduced yields.")
VIN(r5, 2020, "excellent", "stable", "Warm autumn; unexpected richness and depth for the appellation.")
VIN(r5, 2019, "very_good", "stable", "Fresh and aromatic; Pinot Noir shows delightful raspberry and chalk.")
VIN(r5, 2018, "good", "stable", "Warm vintage; good drinking wine but less typicity than cooler years.")
p5a = P("Domaine Poupart", "winery", r5, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Small estate dedicated to reviving Coteaux du Giennois identity through careful viticulture on chalk-flint soils.",
        reputation_narrative="Pioneer of modern Coteaux du Giennois quality; wines appear in Loire specialist lists.",
        price_positioning="value",
        authority_tier=1)
p5b = P("Domaine Poupat et Fils", "winery", r5, "France",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-generational family estate covering both colours; focused on expressing the cool-climate chalk character of this understated appellation.",
        reputation_narrative="Reliable local producer; wines offer honest value and regional character.",
        price_positioning="value",
        authority_tier=1)
pr5a, n5a = PROD("Domaine Poupart Coteaux du Giennois Blanc", "wine_still", p5a, r5, "France",
                  subcategory="Sauvignon Blanc",
                  description="Crisp, racy Sauvignon with chalk minerality, lemon zest and fresh herbs; high acidity and fine length.",
                  price_tier="value")
if n5a:
    PAIR(pr5a, "Freshwater crayfish bisque", "complement", "established", "starter", "Regional Loire crustacean tradition; chalk minerality mirrors the freshwater character.")
    PAIR(pr5a, "Fresh chèvre with herbs", "complement", "classic", "starter", "Canonical Loire Sauvignon pairing; chalk soils echo the minerality found in goat milk.")
    PAIR(pr5a, "Grilled white fish with capers", "complement", "established", "fish_course", "Caper acidity mirrors wine's tartness; delicate white fish preserved by Sauvignon's freshness.")
    PAIR(pr5a, "Green salad with vinaigrette", "complement", "classic", "casual", "High-acid wine loves vinegar-dressed salads; a simple but perfect Loire lunch match.")
pr5b, n5b = PROD("Domaine Poupat et Fils Coteaux du Giennois Rouge", "wine_still", p5b, r5, "France",
                  subcategory="Pinot Noir",
                  description="Pale ruby Pinot Noir with raspberry, chalk dust and a delicate herbal edge; light-bodied and refreshing.",
                  price_tier="value")
if n5b:
    PAIR(pr5b, "Rabbit stew with herbs de Provence", "complement", "established", "main", "Light Loire Pinot loves delicate white meat; herbs bridge the wine's aromatic complexity.")
    PAIR(pr5b, "Lentil salad with smoked duck", "complement", "suggested", "starter", "Earthy lentils and light duck complement Pinot's chalk-fruit character.")
    PAIR(pr5b, "Grilled pigeon with wild mushrooms", "complement", "established", "main", "Game bird and earthy mushrooms echo Loire Pinot's rusticity and red fruit.")
    PAIR(pr5b, "Aged Chavignol with crusty baguette", "complement", "classic", "cheese", "Sancerre-adjacent cheese with Loire Pinot from nearby hills; regional harmony.")

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
