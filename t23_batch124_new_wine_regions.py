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
    print(f"  Region inserted: {name} ({rid})")
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
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B124 ─────────────────────────────────────────────────────────────────────
# Targets: Montsant DO (Spain), Terra Alta DO (Spain), Costers del Segre DO (Spain),
#          Condrieu AOC (France), Crozes-Hermitage AOC (France)

# 1. MONTSANT DO — Spain
print("=== Montsant DO ===")
r1 = R("Montsant DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Montsant DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="A horseshoe-shaped appellation surrounding Priorat in the Tarragona mountains, sharing similar Garnacha and Cariñena varieties on limestone, clay and granite soils (without llicorella slate). More accessible in price than Priorat but sharing the same old-vine Garnacha intensity and Mediterranean warmth. Montsant has emerged as an important appellation in its own right, with several producers achieving Priorat-level quality.",
        key_producers="Cellers de Can Blau, Venus La Universal, Acústic Celler, Celler Joan d'Anguera",
        historical_context="Montsant was carved from the former Falset-Tarragona region in 2001, the same year Priorat achieved DOQ. The region's lower land prices attracted a generation of ambitious winemakers seeking the quality terroir of the Priorat area without the associated costs.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","rising"),(2020,"excellent","rising"),(2021,"very_good","rising"),(2022,"excellent","rising")]:
    VIN(r1, yr, qd, pt, f"Montsant {yr}: limestone and granite hillsides; old-vine Garnacha with Mediterranean warmth and acidity")

p1a = P("Celler Joan d'Anguera", "winery", r1, "Spain",
        production_philosophy="organic",
        philosophy_description="Organic family estate in Darmós; old-vine Garnacha Negra and Syrah from limestone and granite soils.",
        reputation_narrative="Joan and Josep d'Anguera's estate is one of Montsant's quality leaders; La Planella old-vine Garnacha is the signature.",
        price_positioning="premium")
pr1a1, n = PROD("Joan d'Anguera La Planella Garnacha", "wine_still", p1a, r1, "Spain",
                subcategory="Garnacha Negra", price_tier="premium",
                description="Old-vine Garnacha from Darmós; ripe dark cherry, wild herbs, Mediterranean garrigue and structured mineral backbone.")
if n:
    PAIR(pr1a1, "Roast lamb shoulder with wild thyme", "complement", "classic", "main", "Old-vine Garnacha and herb-roasted lamb are inseparable in this landscape")
    PAIR(pr1a1, "Grilled lamb chops with aioli", "complement", "established", "main", "Mediterranean Garnacha is the natural companion for simple charred lamb")
    PAIR(pr1a1, "Catalan escudella (meat and pasta stew)", "complement", "established", "main", "Garnacha's depth and warmth frame the hearty Catalan one-pot tradition")
    PAIR(pr1a1, "Truffle-scented pecorino cheese", "complement", "established", "cheese", "Earthy old-vine Garnacha finds harmony with truffle-inflected hard cheese")

pr1a2, n = PROD("Joan d'Anguera Montsant Red", "wine_still", p1a, r1, "Spain",
                subcategory="Garnacha-Syrah", price_tier="mid_range",
                description="Entry Montsant red; organic Garnacha and Syrah with ripe cherry, spice and fresh herbal lift from the limestone soils.")
if n:
    PAIR(pr1a2, "Pizza with Ibérico chorizo and peppers", "complement", "established", "main", "Fruit-forward Garnacha blend complements spiced chorizo and sweet pepper")
    PAIR(pr1a2, "Grilled pork sausage with mustard", "complement", "established", "main", "Accessible Montsant red is the everyday companion for pork charcuterie")
    PAIR(pr1a2, "Pasta arrabbiata with pecorino", "complement", "established", "main", "Ripe cherry fruit of Garnacha tames the arrabbiata heat while matching the depth")
    PAIR(pr1a2, "Vegetable paella with romesco", "complement", "suggested", "main", "Mediterranean Garnacha complements vegetable paella's smoky-sweet character")

p1b = P("Acústic Celler", "winery", r1, "Spain",
        production_philosophy="organic",
        philosophy_description="Organic Montsant producer; Garnatxa Blanca white and Garnacha reds from old limestone and granite parcels.",
        reputation_narrative="Albert Jane's Acústic project makes wines of freshness and precision unusual for the region; the white Acústic is a standout.",
        price_positioning="mid_range")
pr1b1, n = PROD("Acústic Blanc Garnatxa Blanca", "wine_still", p1b, r1, "Spain",
                subcategory="Garnatxa Blanca", price_tier="mid_range",
                description="Old-vine Montsant Garnacha Blanca; fresh peach, almond, citrus and mineral from limestone soils — unusually elegant for the warm region.")
if n:
    PAIR(pr1b1, "Grilled prawn heads with garlic oil", "complement", "classic", "main", "Mineral Garnacha Blanca and grilled prawns is a classic Catalan combination")
    PAIR(pr1b1, "White asparagus with aioli", "complement", "established", "starter", "Fresh mineral white complements the delicate bitter-sweetness of white asparagus")
    PAIR(pr1b1, "Arroz a banda (Catalan seafood rice)", "complement", "classic", "main", "The Catalan seaside rice dish finds its natural white wine companion")
    PAIR(pr1b1, "Steamed mussels with wine and saffron", "complement", "established", "main", "Mineral citrus white mirrors saffron-wine broth of steamed mussels")

pr1b2, n = PROD("Acústic Montsant Garnacha", "wine_still", p1b, r1, "Spain",
                subcategory="Garnacha Negra", price_tier="mid_range",
                description="Entry Acústic red; old-vine Garnacha with bright cherry, herbal freshness and a mineral limestone backbone.")
if n:
    PAIR(pr1b2, "Slow-cooked lamb with dried fruits", "complement", "established", "main", "Bright Garnacha cherry and herb lift slow-cooked lamb with dried apricot")
    PAIR(pr1b2, "Escalivada with anchovies on toast", "complement", "classic", "starter", "Mediterranean Garnacha and the salt-sweet anchovy-vegetable combination shine together")
    PAIR(pr1b2, "Grilled sardines with lemon and parsley", "complement", "established", "starter", "Refreshing Garnacha acidity lifts oily sardines and complements the herb")
    PAIR(pr1b2, "Tomato bread (pa amb tomàquet)", "complement", "classic", "amuse", "Montsant Garnacha and the Catalan bread-tomato-oil combination are inseparable")

# 2. TERRA ALTA DO — Spain
print("=== Terra Alta DO ===")
r2 = R("Terra Alta DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Terra Alta DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Remote high-altitude plateau in the Tarragona-Aragon border zone, with some of Spain's oldest Garnacha Blanca vines. The high elevation (400–700m) combined with a semi-continental climate produces fresh, mineral whites from old-vine Garnacha Blanca — unusually aromatic and complex for a warm Mediterranean region. Red wines from Garnacha and Cariñena also benefit from altitude freshness. Terra Alta is establishing a global identity through its distinctive Garnacha Blanca.",
        key_producers="Vinos de Arganza, Celler Cooperatiu Gandesa, Xavier Clua, Bàrbara Forés",
        historical_context="Terra Alta received DO status in 1972. The region was long an anonymous bulk producer; the quality revolution began in the 2000s when producers recognised the potential of old-vine Garnacha Blanca. The high plateau was historically a stronghold of the Aragonese and a battleground of the Spanish Civil War.")
for yr, qd, pt in [(2018,"very_good","rising"),(2019,"excellent","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r2, yr, qd, pt, f"Terra Alta {yr}: high plateau harvest; Garnacha Blanca shows exceptional freshness from altitude")

p2a = P("Bàrbara Forés", "winery", r2, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Terra Alta estate specialising in old-vine Garnacha Blanca; El Quintà single-vineyard is the benchmark.",
        reputation_narrative="Bàrbara Forés produces the reference Terra Alta Garnacha Blanca; El Quintà from 50-year-old vines has put the appellation on the international map.",
        price_positioning="mid_range")
pr2a1, n = PROD("Bàrbara Forés El Quintà Garnacha Blanca", "wine_still", p2a, r2, "Spain",
                subcategory="Garnacha Blanca", price_tier="premium",
                description="Single-vineyard 50-year-old Garnacha Blanca; complex white with peach, anise, mineral and a long oxidative texture from altitude.")
if n:
    PAIR(pr2a1, "Grilled salt cod with honey and pine nuts", "complement", "established", "main", "Terra Alta white's mineral complexity complements the sweet-salt-cod combination")
    PAIR(pr2a1, "Baked turbot with garlic and parsley", "complement", "classic", "main", "Old-vine Garnacha Blanca's weight and mineral suits firm-fleshed turbot")
    PAIR(pr2a1, "Grilled squid with black ink vinaigrette", "complement", "established", "main", "Mineral white complements the depth of squid with black ink")
    PAIR(pr2a1, "Aged manchego with quince paste", "complement", "established", "cheese", "Complex Garnacha Blanca texture mirrors aged sheep's cheese with membrillo")

pr2a2, n = PROD("Bàrbara Forés Blanc Terra Alta", "wine_still", p2a, r2, "Spain",
                subcategory="Garnacha Blanca", price_tier="mid_range",
                description="Entry Bàrbara Forés white; fresh Garnacha Blanca with peach blossom, citrus and a gentle mineral finish.")
if n:
    PAIR(pr2a2, "Salad with anchovies and olives", "complement", "established", "starter", "Fresh white complements the salt-acid character of anchovy-dressed salad")
    PAIR(pr2a2, "Ceviche with citrus and herbs", "complement", "suggested", "starter", "Citrus-mineral Garnacha Blanca mirrors ceviche's bright acid-herb profile")
    PAIR(pr2a2, "Grilled sea bass fillet with herbs", "complement", "established", "main", "Fresh Mediterranean white lifts sea bass with aromatic precision")
    PAIR(pr2a2, "Gazpacho with croutons", "complement", "established", "starter", "Chilled Garnacha Blanca complements the tomato-herb freshness of gazpacho")

p2b = P("Xavier Clua", "winery", r2, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Old-vine Terra Alta specialist; natural and minimal intervention wines from old Garnacha Blanca and Garnacha Negra parcels.",
        reputation_narrative="Xavier Clua's Mas d'en Pol is a rising star of Terra Alta, producing fresh and precise wines that defy the region's warm climate stereotype.",
        price_positioning="mid_range")
pr2b1, n = PROD("Xavier Clua Mas d'en Pol Garnacha Blanca", "wine_still", p2b, r2, "Spain",
                subcategory="Garnacha Blanca", price_tier="mid_range",
                description="Old-vine Mas d'en Pol Garnacha Blanca; saline mineral, white peach and anise from high-altitude limestone soils.")
if n:
    PAIR(pr2b1, "Tempura of seasonal vegetables with dipping sauce", "complement", "suggested", "starter", "Saline mineral Garnacha Blanca cleanses between bites of crisp vegetable tempura")
    PAIR(pr2b1, "Oysters with mignonette and lemon", "complement", "established", "starter", "Saline Terra Alta white mirrors briny oyster with mineral precision")
    PAIR(pr2b1, "Prawn dumplings with ginger dipping sauce", "complement", "suggested", "starter", "Fresh mineral white lifts prawn dumpling sweetness with citrus precision")
    PAIR(pr2b1, "Bacalhau à brás (salt cod with eggs and potato)", "complement", "established", "main", "Mineral Garnacha Blanca's acidity frames the salt-and-richness of bacalhau")

pr2b2, n = PROD("Xavier Clua Mas d'en Pol Red", "wine_still", p2b, r2, "Spain",
                subcategory="Garnacha Negra", price_tier="mid_range",
                description="Old-vine Terra Alta Garnacha Negra; fresh cherry, red fruit and Mediterranean herb from high-plateau limestone soils.")
if n:
    PAIR(pr2b2, "Grilled lamb cutlets with herbs", "complement", "established", "main", "Fresh Garnacha Negra lifts herb-grilled lamb with bright fruit acidity")
    PAIR(pr2b2, "Pork escalope with capers and lemon", "complement", "established", "main", "Light-bodied red complements the acid-savoury notes of capered pork")
    PAIR(pr2b2, "Rabbit with rosemary and garlic", "complement", "classic", "main", "Fresh Mediterranean Garnacha and rabbit with herbs is a regional classic")
    PAIR(pr2b2, "Cheese platter with cured meats", "complement", "established", "starter", "Accessible fresh Garnacha works across a mixed charcuterie and cheese board")

# 3. COSTERS DEL SEGRE DO — Spain
print("=== Costers del Segre DO ===")
r3 = R("Costers del Segre DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Costers del Segre DO",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Continental Catalan appellation in the Lleida province, centred on the Segre river and its irrigation canals. A widely dispersed appellation with six sub-zones; most famous for Raimat estate and its pioneering use of international varieties alongside indigenous grapes. Tempranillo, Cabernet Sauvignon, Chardonnay and Garnacha all thrive here in a hot dry climate moderated by altitude and cold nights.",
        key_producers="Raimat, Clos Pons, L'Olivera, Cérvoles",
        historical_context="Costers del Segre was created in 1988 largely to accommodate the Raimat estate, which had pioneered modern irrigation viticulture in the region in the early 20th century. The appellation's diversity of climates and varieties reflects its geographical spread across the Lleida plateau.")
for yr, qd, pt in [(2018,"excellent","stable"),(2019,"very_good","stable"),(2020,"excellent","stable"),(2021,"very_good","stable"),(2022,"excellent","stable")]:
    VIN(r3, yr, qd, pt, f"Costers del Segre {yr}: continental Lleida plateau; warm days and cold nights produce balance in reds and whites")

p3a = P("Clos Pons", "winery", r3, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Noguera sub-zone estate; Garnacha, Rara Negra and Sauvignon Blanc from ancient soils showcase Costers del Segre's diversity.",
        reputation_narrative="The Pons family estate produces wines of unexpected freshness and character in this arid plateau zone; benchmark for the appellation's potential.",
        price_positioning="premium")
pr3a1, n = PROD("Clos Pons Roc Nu Garnacha", "wine_still", p3a, r3, "Spain",
                subcategory="Garnacha", price_tier="premium",
                description="Old-vine Garnacha from Noguera on rocky calcareous soils; concentrated with dark cherry, spice and mineral structure.")
if n:
    PAIR(pr3a1, "Roast pork with local herbs", "complement", "established", "main", "Concentrated Garnacha's dark fruit and spice suit herb-roasted pork beautifully")
    PAIR(pr3a1, "Grilled lamb ribs with chimichurri", "complement", "established", "main", "Dark Garnacha tannins and fruit complement charred lamb with herb sauce")
    PAIR(pr3a1, "Lentil and chorizo stew", "complement", "established", "main", "Warm Segre Garnacha is the natural companion for hearty Spanish legume stew")
    PAIR(pr3a1, "Aged Idiazábal smoked sheep's cheese", "complement", "established", "cheese", "Concentrated Garnacha finds harmony with the smoke and nuttiness of aged Idiazábal")

pr3a2, n = PROD("Clos Pons Alges Blanc", "wine_still", p3a, r3, "Spain",
                subcategory="Sauvignon Blanc-Macabeo", price_tier="mid_range",
                description="Aromatic Costers del Segre white; Sauvignon Blanc-led with citrus, green herb and a refreshing mineral freshness from altitude.")
if n:
    PAIR(pr3a2, "Grilled asparagus with Hollandaise", "complement", "established", "main", "Sauvignon's citrus-herb character is the natural match for asparagus dishes")
    PAIR(pr3a2, "Goat's cheese salad with walnuts", "complement", "established", "starter", "Sauvignon Blanc and fresh goat's cheese is a globally beloved pairing")
    PAIR(pr3a2, "Grilled sea bream with lemon and herbs", "complement", "established", "main", "Citrus-mineral white suits Mediterranean fish preparations naturally")
    PAIR(pr3a2, "Gazpacho andaluz", "complement", "established", "starter", "Fresh herb-citrus white complements the cold tomato and vegetable of gazpacho")

p3b = P("L'Olivera", "winery", r3, "Spain",
        production_philosophy="organic",
        philosophy_description="Cooperativa L'Olivera in Vallbona de les Monges; organic Macabeo, Chardonnay and Cabernet Sauvignon from monastic landscape.",
        reputation_narrative="The cooperative at the medieval monastery of Vallbona de les Monges produces some of Costers del Segre's most distinctive wines; Blanc Missenyora is the benchmark white.",
        price_positioning="mid_range")
pr3b1, n = PROD("L'Olivera Blanc de Serè Macabeo", "wine_still", p3b, r3, "Spain",
                subcategory="Macabeo", price_tier="mid_range",
                description="Organic high-altitude Macabeo; fresh citrus, green apple and mineral freshness from the monastery's elevated limestone vineyards.")
if n:
    PAIR(pr3b1, "Grilled vegetables with romesco sauce", "complement", "established", "main", "Fresh Macabeo complements the sweet-smoky character of romesco with vegetable")
    PAIR(pr3b1, "White bean salad with lemon and herbs", "complement", "established", "starter", "Mineral citrus Macabeo brings freshness to a simple legume salad")
    PAIR(pr3b1, "Poached chicken with salsa verde", "complement", "established", "main", "Clean mineral white complements poached chicken's delicate flavours")
    PAIR(pr3b1, "Spaghetti aglio olio with lemon", "complement", "established", "main", "Citrus-mineral white is a natural match for simple garlic-olive oil pasta")

pr3b2, n = PROD("L'Olivera Petit Alts Quarters Red", "wine_still", p3b, r3, "Spain",
                subcategory="Garnacha-Tempranillo", price_tier="mid_range",
                description="Entry Costers del Segre red; organic Garnacha and Tempranillo with cherry fruit, soft tannins and an accessible Mediterranean warmth.")
if n:
    PAIR(pr3b2, "Botifarra sausage with white beans", "complement", "classic", "main", "Catalan sausage and bean stew finds its natural regional wine companion")
    PAIR(pr3b2, "Hamburger with caramelised onions", "complement", "established", "casual", "Accessible Mediterranean red suits casual burger eating")
    PAIR(pr3b2, "Pizza Margherita with fresh basil", "complement", "established", "main", "Light red with tomato-basil pizza is an easy, satisfying combination")
    PAIR(pr3b2, "Chicken thighs with paprika and potatoes", "complement", "established", "main", "Everyday Garnacha-Tempranillo and paprika-braised chicken; simple and satisfying")

# 4. CONDRIEU AOC — France
print("=== Condrieu AOC ===")
r4 = R("Condrieu AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Condrieu AOC",
        reputation_tier="iconic",
        quality_trajectory="established",
        description="The most celebrated appellation for Viognier in the world, on steep granite terraces above the Rhône south of Lyon. Exclusively Viognier — producing wines of extraordinary floral intensity (apricot, peach blossom, violet) with a richly textured, almost oily mouthfeel. The combination of extreme mineral tension on granite with the grape's natural opulence creates wines unlike anything else. Production is tiny; prices are high. Château Grillet is a single-estate appellation within Condrieu.",
        key_producers="Guigal, Georges Vernay, Yves Cuilleron, André Perret, Pierre Gaillard",
        historical_context="Condrieu nearly became extinct by the 1960s when only 8 hectares remained. Georges Vernay single-handedly preserved the appellation. The AOC was created in 1940 and covers six communes; the co-planted Coteau du Vernon is Vernay's most celebrated site.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Condrieu {yr}: granite terrace Viognier; extraordinary aromatic intensity and textured richness")

p4a = P("Georges Vernay", "winery", r4, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The saviour of Condrieu; Coteau du Vernon and Chaillées de l'Enfer are the appellation's defining wines.",
        reputation_narrative="Georges Vernay preserved Condrieu from extinction and his daughter Christine now produces the benchmark for the world's finest Viognier.",
        price_positioning="ultra_premium")
pr4a1, n = PROD("Vernay Condrieu Coteau du Vernon", "wine_still", p4a, r4, "France",
                subcategory="Viognier", price_tier="ultra_premium",
                description="The reference Condrieu; from the precipitous Coteau du Vernon on primary granite — apricot, violet, white truffle and extraordinary tension.")
if n:
    PAIR(pr4a1, "Seared foie gras with apricot gastrique", "complement", "classic", "main", "Condrieu's apricot-richness and Viognier texture are the natural partner for foie gras")
    PAIR(pr4a1, "Langoustines in bisque with tarragon", "complement", "classic", "main", "Granite-mineral Viognier and langoustine is a great Northern Rhône combination")
    PAIR(pr4a1, "Truite au bleu with herb butter", "complement", "established", "main", "The Rhône tradition: Condrieu Viognier with trout and herb butter")
    PAIR(pr4a1, "Spiced quail with peach compote", "complement", "established", "main", "Viognier's peach-apricot mirrors the fruit compote beside spiced game bird")

pr4a2, n = PROD("Vernay Condrieu Les Chaillées de l'Enfer", "wine_still", p4a, r4, "France",
                subcategory="Viognier", price_tier="premium",
                description="Les Chaillées de l'Enfer from schist and gneiss terraces; structured Condrieu with peach, orange blossom and mineral depth.")
if n:
    PAIR(pr4a2, "Lobster bisque with cream and cognac", "complement", "established", "main", "Structured Viognier's richness and mineral mirrors lobster cream bisque")
    PAIR(pr4a2, "Chicken fricassee with morels", "complement", "established", "main", "Viognier's textural richness complements the cream and earth of morel chicken")
    PAIR(pr4a2, "Grilled monkfish with saffron cream", "complement", "established", "main", "Rich white wine and meaty monkfish with saffron; a complementary weight match")
    PAIR(pr4a2, "Ripe peach and almond tart", "complement", "suggested", "dessert", "Off-dry Condrieu character mirrors the stone fruit and almond of the tart")

p4b = P("Yves Cuilleron", "winery", r4, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Condrieu and Saint-Joseph producer; Les Chaillets single-vineyard Viognier and multiple Syrah from granite terraces.",
        reputation_narrative="Yves Cuilleron is one of the Northern Rhône's most prolific and celebrated producers; consistently excellent across Condrieu and the Syrah appellations.",
        price_positioning="premium")
pr4b1, n = PROD("Cuilleron Condrieu Les Chaillets", "wine_still", p4b, r4, "France",
                subcategory="Viognier", price_tier="premium",
                description="Les Chaillets Condrieu; apricot-rich Viognier with white truffle, orange blossom and an opulent, mineral-framed finish.")
if n:
    PAIR(pr4b1, "Scallops in cream sauce with saffron", "complement", "classic", "main", "Viognier's opulent texture frames scallop cream with saffron beautifully")
    PAIR(pr4b1, "Roast pork loin with apricot stuffing", "complement", "classic", "main", "The wine's apricot intensity mirrors and echoes the stuffing flavour")
    PAIR(pr4b1, "Soft-shell crab with citrus butter", "complement", "established", "main", "Rich Viognier texture supports the richness of soft-shell crab")
    PAIR(pr4b1, "Tandoori prawn with mango chutney", "complement", "suggested", "main", "Viognier's tropical stone-fruit meets Indian spice and mango in exotic harmony")

pr4b2, n = PROD("Cuilleron Condrieu La Petite Côte", "wine_still", p4b, r4, "France",
                subcategory="Viognier", price_tier="mid_range",
                description="Entry Cuilleron Condrieu; fresh peach, apricot and floral Viognier character with a lighter, more accessible style.")
if n:
    PAIR(pr4b2, "Thai red curry with coconut milk", "complement", "established", "main", "Fresh aromatic Viognier is a surprising delight with coconut-milk curry")
    PAIR(pr4b2, "Grilled peach salad with burrata", "complement", "established", "starter", "Peach-floral Viognier mirrors fresh peach and creamy burrata in summer")
    PAIR(pr4b2, "Smoked chicken with herb cream cheese", "complement", "established", "starter", "Aromatic white lifts the richness of smoked chicken and cream cheese")
    PAIR(pr4b2, "Shrimp pad thai with lime and peanuts", "complement", "established", "main", "Fresh Viognier's aromatic fruit bridges spice and sweetness of Thai noodles")

# 5. CROZES-HERMITAGE AOC — France
print("=== Crozes-Hermitage AOC ===")
r5 = R("Crozes-Hermitage AOC", "France", "wine",
        designation_type="AOC",
        designation_name="Crozes-Hermitage AOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="The largest Northern Rhône appellation, surrounding the famed Hermitage hill. Syrah dominates reds on granite soils (north) and alluvial clay-limestone plains (south); Marsanne and Roussanne produce characterful whites. Quality varies enormously but the granite-zone wines from producers like Alain Graillot approach Hermitage quality. The appellation has seen a wave of natural wine producers raising the quality ceiling significantly.",
        key_producers="Alain Graillot, Belle, Domaine du Colombier, Combier, Delas",
        historical_context="Crozes-Hermitage was recognised as an appellation in 1937, surrounding the legendary Hermitage hill without including it. The appellation expanded dramatically in the 1950s-60s onto inferior plains soils, diluting quality. The current quality revival centres on the granite northern plateau around Mercurol and Gervans.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"very_good","stable"),(2020,"excellent","rising"),(2021,"very_good","rising"),(2022,"excellent","rising")]:
    VIN(r5, yr, qd, pt, f"Crozes-Hermitage {yr}: Northern Rhône granite plateau; Syrah shows floral and mineral character")

p5a = P("Domaine Alain Graillot", "winery", r5, "France",
        production_philosophy="terroir_driven",
        philosophy_description="The reference producer of Crozes-Hermitage; uncompromising Syrah from Beaumont-Monteux showing Northern Rhône precision.",
        reputation_narrative="Alain Graillot established the Crozes-Hermitage benchmark in the 1980s; his wines consistently outperform the appellation at a fraction of Hermitage prices.",
        price_positioning="premium")
pr5a1, n = PROD("Graillot Crozes-Hermitage Rouge", "wine_still", p5a, r5, "France",
                subcategory="Syrah", price_tier="premium",
                description="The benchmark Crozes Syrah; violet, blackcurrant, olives and smoked meat with granite mineral and a firm tannic backbone.")
if n:
    PAIR(pr5a1, "Roast leg of lamb with rosemary", "complement", "classic", "main", "Northern Rhône Syrah and roasted lamb is one of France's great wine pairings")
    PAIR(pr5a1, "Grilled Côtes de boeuf with bone marrow", "complement", "classic", "main", "Full-bodied Syrah and grilled beef rib is a Rhône region tradition")
    PAIR(pr5a1, "Duck leg confit with puy lentils", "complement", "established", "main", "Syrah's dark fruit and tannins complement rich confit duck beautifully")
    PAIR(pr5a1, "Tapenade and charcuterie on sourdough", "complement", "established", "starter", "Olive-inflected Syrah mirrors the Provençal character of olive tapenade")

pr5a2, n = PROD("Graillot Crozes-Hermitage Blanc", "wine_still", p5a, r5, "France",
                subcategory="Marsanne-Roussanne", price_tier="premium",
                description="Marsanne-Roussanne Crozes blanc; rich and waxy with acacia, white peach and mineral that rewards ageing.")
if n:
    PAIR(pr5a2, "Gratin dauphinois with cream and Gruyère", "complement", "established", "main", "Rich waxy Marsanne-Roussanne is the ideal companion for cream potato gratin")
    PAIR(pr5a2, "Roast chicken with tarragon and cream", "complement", "classic", "main", "Rhône white and Bresse chicken in tarragon cream sauce is a French classic")
    PAIR(pr5a2, "Langoustine bisque with herbs", "complement", "established", "main", "Waxy Marsanne texture mirrors the richness of crustacean bisque")
    PAIR(pr5a2, "Aged Saint-Marcellin cheese", "complement", "established", "cheese", "The great local cheese of Lyon finds natural harmony with waxy Rhône white")

p5b = P("Domaine Belle", "winery", r5, "France",
        production_philosophy="terroir_driven",
        philosophy_description="Family Crozes estate in Larnage; single-parcel Syrah Les Pierrelles and Les Terres Blanches are among the appellation's finest.",
        reputation_narrative="Philippe Belle's estate consistently produces Crozes-Hermitage of exceptional quality; Les Pierrelles on granite shows the appellation's true Syrah potential.",
        price_positioning="premium")
pr5b1, n = PROD("Domaine Belle Crozes-Hermitage Les Pierrelles", "wine_still", p5b, r5, "France",
                subcategory="Syrah", price_tier="premium",
                description="Les Pierrelles Syrah from granite soils; polished violet, smoked meat and blackberry with mineral precision and long structure.")
if n:
    PAIR(pr5b1, "Magret de canard with cherry sauce", "complement", "classic", "main", "Northern Rhône Syrah and duck magret is a great French table combination")
    PAIR(pr5b1, "Daube de boeuf Provençale with olives", "complement", "classic", "main", "Syrah's olive-and-herb character mirrors the classic Provençal beef daube")
    PAIR(pr5b1, "Venison stew with mushrooms", "complement", "established", "main", "Dark mineral Syrah frames game and mushroom stew with Rhône precision")
    PAIR(pr5b1, "Pork cheeks braised in Syrah", "complement", "classic", "main", "The Rhône tradition of braising pork in local Syrah then drinking the same wine")

pr5b2, n = PROD("Domaine Belle Crozes-Hermitage Blanc", "wine_still", p5b, r5, "France",
                subcategory="Marsanne", price_tier="mid_range",
                description="Marsanne-dominated Crozes blanc; round and expressive with honeysuckle, white peach and almond — fresh in youth, complex with age.")
if n:
    PAIR(pr5b2, "Quenelles de brochet sauce Nantua", "complement", "classic", "main", "The great Lyon classic pairing: Rhône white with pike quenelles in crayfish sauce")
    PAIR(pr5b2, "Chicken liver parfait with brioche", "complement", "established", "starter", "Rich waxy Marsanne complements chicken liver richness with textural harmony")
    PAIR(pr5b2, "Roast monkfish with saffron butter sauce", "complement", "established", "main", "Marsanne's weight and richness match meaty monkfish and saffron beautifully")
    PAIR(pr5b2, "Tarte Tatin with crème fraîche", "complement", "established", "dessert", "Almond-honeysuckle Marsanne complements the caramelised apple of Tarte Tatin")

# Final counts
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")

cur.close()
conn.close()
print("B124 complete.")
