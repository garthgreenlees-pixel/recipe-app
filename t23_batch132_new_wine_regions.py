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

# ── B132 ──────────────────────────────────────────────────────────────────────
# Targets: Hemel-en-Aarde Valley WO (SA), Elgin WO (SA),
#          Hawke's Bay (New Zealand), Martinborough (New Zealand),
#          McLaren Vale (Australia)

# 1. HEMEL-EN-AARDE VALLEY WO — South Africa
print("=== Hemel-en-Aarde Valley WO ===")
r1 = R("Hemel-en-Aarde Valley WO", "South Africa", "wine",
        designation_type="WO",
        designation_name="Hemel-en-Aarde Valley WO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="South Africa's most acclaimed cool-climate wine ward; the 'Valley of Heaven and Earth' inland from Hermanus and Walker Bay; shale and clay soils; Pinot Noir and Chardonnay of international standing from three sub-wards — Valley, Ridge, and Upper. Hamilton Russell Vineyards pioneered the region; now home to boutique producers making some of Africa's greatest wines.",
        key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Storm Wines",
        historical_context="Tim Hamilton Russell planted the first vines in 1976 after extensive research identified the coolest possible spot in South Africa. His son Anthony took over and made Hamilton Russell Vineyards one of Africa's most acclaimed estates. The ward now has three sub-zones: Hemel-en-Aarde Valley (the original and warmest), Ridge (mid-altitude), and Upper (coolest). The Burgundy comparison is unavoidable — many producers in Hermanus studied in Beaune.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Excellent cool year; Valley Pinot Noir shows elegant red cherry and earthy depth; Chardonnay mineral and fine"),
    (2019, "very_good", "rising", "Good growing season; Pinot Noir shows fragrance and silky texture; Chardonnay shows limestone precision"),
    (2020, "exceptional", "rising", "Exceptional Valley vintage; Pinot Noir of Burgundian complexity; Chardonnay rivals premier cru; landmark year"),
    (2021, "excellent", "rising", "Excellent; cool conditions enhanced aromatics; Pinot Noir shows extraordinary elegance and mineral depth"),
    (2022, "very_good", "stable", "Good vintage; ocean influence preserved freshness; Pinot Noir fragrant and silky; Chardonnay crisp"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Bouchard Finlayson", "winery", r1, "South Africa",
        production_philosophy="terroir_driven",
        philosophy_description="The Burgundy-inspired estate founded by Peter Finlayson with Burgundy négociant Paul Bouchard; Galpin Peak Pinot Noir and Missionvale Chardonnay are benchmarks for the region.",
        reputation_narrative="One of South Africa's most internationally respected Pinot Noir producers; Bouchard Finlayson's Galpin Peak is consistently cited as Africa's finest Pinot Noir and competes with premier cru Burgundy.",
        price_positioning="premium")

pr1a1, n = PROD("Bouchard Finlayson Galpin Peak Pinot Noir", "wine_still", p1a, r1, "South Africa",
    subcategory="Pinot Noir", price_tier="ultra_premium",
    description="South Africa's most acclaimed Pinot Noir; shale soils at 200m in the Valley; red cherry, wild strawberry, earthy mushroom, spice; silky tannins; Burgundian precision with African sunshine richness.")
if n:
    PAIR(pr1a1, "Roast duck breast with sour cherry sauce and beet", "complement", "classic", "main", "Classic Pinot pairing; cherry sauce mirrors Galpin Peak's red fruit; beet earthiness echoes the shale mineral")
    PAIR(pr1a1, "Grilled springbok loin with wild herb jus", "complement", "classic", "main", "South African game; springbok's elegant gaminess perfectly matched by Pinot's silky structure; wild herbs bridge")
    PAIR(pr1a1, "Salmon trout with lentils and mushroom", "complement", "established", "fish_course", "Rich trout; Pinot's acidity cuts fat; lentil earthiness bridges forest floor; mushroom echoes earthy depth")
    PAIR(pr1a1, "Aged Camembert with strawberry jam", "complement", "established", "cheese", "Soft ripened cheese; Pinot's fruit and acidity balance the fat; strawberry echoes wine's red fruit notes")

pr1a2, n = PROD("Bouchard Finlayson Missionvale Chardonnay", "wine_still", p1a, r1, "South Africa",
    subcategory="Chardonnay", price_tier="premium",
    description="Benchmark Hemel-en-Aarde Chardonnay; citrus cream, white peach, chalk mineral; Burgundian influence in winemaking; excellent natural acidity; one of South Africa's finest white wines.")
if n:
    PAIR(pr1a2, "Linefish of the day with lemon butter sauce", "complement", "classic", "fish_course", "South African coastal tradition; Chardonnay's citrus and cream suit white fish; lemon butter bridges the mineral")
    PAIR(pr1a2, "Seared scallops with parsnip purée and crispy pancetta", "complement", "classic", "starter", "Luxury scallops; Chardonnay's weight and mineral frames the sweetness; pancetta saltiness balanced by acidity")
    PAIR(pr1a2, "Roasted chicken with preserved lemon and olives", "complement", "classic", "main", "South African kitchen classic; Chardonnay's citrus notes echo preserved lemon; olive adds Mediterranean bridge")
    PAIR(pr1a2, "Aged Cheddar with quince paste", "complement", "established", "cheese", "Aged English-style cheese; Chardonnay's acidity cuts the fat; quince bridges wine's stone fruit character")

p1b = P("Creation Wines", "winery", r1, "South Africa",
        production_philosophy="terroir_driven",
        philosophy_description="Swiss-South African collaboration in the Hemel-en-Aarde Ridge; Jean-Claude and Carolyn Martin produce Chardonnay and Pinot Noir from elevated shale sites; food pairing philosophy central to the estate.",
        reputation_narrative="The pairing-focused Hemel-en-Aarde estate; Creation's elevated Ridge terroir produces wines of great precision; their food and wine pairing philosophy has made them one of the Cape's most visited wineries.",
        price_positioning="premium")

pr1b1, n = PROD("Creation Reserve Pinot Noir Hemel-en-Aarde", "wine_still", p1b, r1, "South Africa",
    subcategory="Pinot Noir single vineyard", price_tier="ultra_premium",
    description="Reserve Pinot Noir from elevated Ridge parcels; dark cherry, violets, spice, forest earth; fine silky tannins; shows the depth and complexity of Hemel-en-Aarde's coolest sites.")
if n:
    PAIR(pr1b1, "Grilled West Coast rock lobster with herb butter", "complement", "classic", "main", "South African luxury seafood; Pinot's freshness and mineral frame the lobster's sweetness; unexpected but brilliant")
    PAIR(pr1b1, "Cape Malay lamb curry with yellow rice and raisins", "bridge", "adventurous", "main", "South African fusion; Pinot's fruit and spice notes bridge the aromatic curry; raisins echo wine's dried fruit")
    PAIR(pr1b1, "Slow-braised springbok with roasted root vegetables", "complement", "classic", "main", "Indigenous South African game with fine Pinot; roots earthiness bridges the forest floor; elegant pairing")
    PAIR(pr1b1, "Smoked salmon with dill crème fraîche and caperberries", "complement", "established", "starter", "Scandinavan-Cape fusion; Pinot's acidity cuts the smoke; dill echoes the wine's herbal notes")

pr1b2, n = PROD("Creation Chardonnay Hemel-en-Aarde Ridge", "wine_still", p1b, r1, "South Africa",
    subcategory="Chardonnay", price_tier="premium",
    description="Ridge-altitude Chardonnay; citrus, white peach, chalk, subtle oak; good freshness from the elevated site; one of Hemel-en-Aarde's most food-friendly Chardonnays.")
if n:
    PAIR(pr1b2, "Pan-fried yellowtail with olive tapenade", "complement", "classic", "fish_course", "South African coastal fish; Chardonnay's weight matches the meaty yellowtail; olive tapenade bridges mineral")
    PAIR(pr1b2, "Grilled oysters with champagne mignonette", "complement", "established", "amuse", "Warm oysters; Chardonnay's mineral and acidity echo raw oysters; champagne mignonette bridges the wine character")
    PAIR(pr1b2, "Boerewors with roasted corn and herb salsa", "complement", "suggested", "main", "South African sausage tradition; Chardonnay's weight handles; corn sweetness bridges the stone fruit notes")
    PAIR(pr1b2, "Aged Manchego with Cape honey", "complement", "established", "cheese", "Aged sheep cheese; Chardonnay's acidity cuts fat; local honey bridges wine's fruit character")

# 2. ELGIN WO — South Africa
print("=== Elgin WO ===")
r2 = R("Elgin WO", "South Africa", "wine",
        designation_type="WO",
        designation_name="Elgin WO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="South Africa's highest and coolest major wine ward; apple-growing region 50km from Cape Town at 200-400m altitude; Sauvignon Blanc, Pinot Noir, and Chardonnay of remarkable freshness and cool-climate character. The altitude and maritime influence from two oceans (Atlantic and Indian) create uniquely cool conditions. Paul Cluver was the pioneer; Shannon Vineyards and Iona produce world-class Sauvignon Blanc.",
        key_producers="Paul Cluver, Shannon Vineyards, Iona, Almenkerk",
        historical_context="Elgin was an apple farming region before wine arrived; the same cool conditions that produce premium apples create ideal cool-climate wine conditions. Paul Cluver began wine production in 1993 in partnership with the local community; Iona followed and showed that Sauvignon Blanc and Pinot Noir could reach New Zealand and Marlborough quality. The ward is now one of South Africa's most exciting regions for cool-climate varieties.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good cool year; Sauvignon Blanc shows vibrant citrus and green herb; Pinot Noir fragrant and precise"),
    (2019, "excellent", "rising", "Excellent vintage; altitude freshness impeccable; Sauvignon and Chardonnay both at their best"),
    (2020, "very_good", "rising", "Good growing season; cool nights preserved freshness; Pinot Noir shows red fruit elegance"),
    (2021, "excellent", "rising", "Ideal conditions; Elgin Sauvignon rivals Marlborough; Pinot shows Burgundian character; excellent year"),
    (2022, "very_good", "stable", "Good vintage; apple region harvested in cool conditions; Sauvignon vibrant and fresh; Pinot elegant"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Paul Cluver Estate Wines", "winery", r2, "South Africa",
        production_philosophy="terroir_driven",
        philosophy_description="The pioneering Elgin estate; Dr Paul Cluver's family estate farmed in partnership with employees and community; Pinot Noir and Riesling from the apple farming heartland; conservation-focused.",
        reputation_narrative="The founding producer of Elgin wine; Paul Cluver proved the ward's potential for cool-climate varieties and built one of South Africa's most respected estates in partnership with the local community.",
        price_positioning="premium")

pr2a1, n = PROD("Paul Cluver Seven Flags Pinot Noir Elgin", "wine_still", p2a, r2, "South Africa",
    subcategory="Pinot Noir", price_tier="ultra_premium",
    description="Flagship Elgin Pinot Noir from coolest parcels; red cherry, raspberry, spice, earthy depth; silky tannins; fragrant and precise; one of South Africa's most acclaimed Pinot Noirs.")
if n:
    PAIR(pr2a1, "Grilled salmon trout with sorrel and capers", "complement", "classic", "fish_course", "Freshwater fish; Pinot's acidity cuts richness; sorrel mirrors wine's fresh acidity; capers add mineral note")
    PAIR(pr2a1, "Springbok carpaccio with rocket and Parmesan", "complement", "classic", "starter", "Raw game; Pinot's red fruit and light tannin suit the delicacy; rocket bitterness balanced by wine's fruit")
    PAIR(pr2a1, "Slow-roasted Karoo lamb with rosemary", "complement", "classic", "main", "South African classic; Elgin Pinot suits the elegant lamb; rosemary echoes wine's herbal character")
    PAIR(pr2a1, "Aged Gruyère with cherry preserve", "complement", "established", "cheese", "Nutty alpine-style cheese; Pinot's acidity and red fruit bridge; cherry preserve mirrors wine's fruit")

pr2a2, n = PROD("Paul Cluver Close Encounter Riesling Elgin", "wine_still", p2a, r2, "South Africa",
    subcategory="Riesling", price_tier="premium",
    description="Elgin Riesling from cool parcels; lime blossom, citrus, slate mineral; off-dry with balancing acidity; shows that Riesling thrives in Elgin's cool conditions; ages beautifully for 10+ years.")
if n:
    PAIR(pr2a2, "Cape Malay bobotie with yellow rice and chutney", "complement", "classic", "main", "South Africa's national dish; off-dry Riesling's sweetness handles the aromatic spice; chutney bridges")
    PAIR(pr2a2, "Thai-style prawn skewers with lemongrass and chilli", "complement", "classic", "starter", "Classic Riesling-Southeast Asian pairing; citrus in wine echoes lemongrass; sweetness tames the chilli heat")
    PAIR(pr2a2, "Smoked snoek pâté with Cape bread", "complement", "established", "starter", "Iconic Cape Fish; Riesling's acidity cuts the smoke and fat; citrus notes mirror the fish's fresh character")
    PAIR(pr2a2, "Roast pork belly with apple sauce", "complement", "classic", "main", "Elgin apple region tradition; Riesling's apple and citrus mirror the sauce; sweetness balances the pork fat")

p2b = P("Iona Vineyards", "winery", r2, "South Africa",
        production_philosophy="minimal_intervention",
        philosophy_description="Artisan Elgin estate producing South Africa's most celebrated Sauvignon Blanc; Andrew Gunn's Iona Sauvignon rivals New Zealand's finest; minimal intervention and site expression.",
        reputation_narrative="The producer that proved South African Sauvignon Blanc can rival Marlborough; Iona's cool-climate Elgin Sauvignon is consistently one of Africa's most awarded white wines.",
        price_positioning="premium")

pr2b1, n = PROD("Iona Sophie's Tear Sauvignon Blanc Elgin", "wine_still", p2b, r2, "South Africa",
    subcategory="Sauvignon Blanc", price_tier="ultra_premium",
    description="Flagship Elgin Sauvignon Blanc; gooseberry, passion fruit, citrus, green herbs, limestone mineral; vibrant acidity; cool-climate freshness rivaling Marlborough; one of South Africa's greatest whites.")
if n:
    PAIR(pr2b1, "West Coast crayfish (rock lobster) with garlic butter", "complement", "classic", "main", "South African coastal luxury; Sauvignon's citrus and acidity frames the rich crayfish; garlic bridges herb notes")
    PAIR(pr2b1, "Creamy goat cheese tart with cherry tomatoes", "complement", "classic", "starter", "Sauvignon and goat cheese — a timeless pairing; Loire tradition translocated to Elgin; citrus cuts the creaminess")
    PAIR(pr2b1, "Grilled yellowfin tuna with herb salsa verde", "complement", "classic", "fish_course", "Meaty tuna; Sauvignon's acidity and herb notes echo the salsa verde; freshness lifts the rich fish")
    PAIR(pr2b1, "Green asparagus with hollandaise sauce", "complement", "classic", "starter", "Classic Sauvignon pairing; asparagus's green herb echoes the wine; hollandaise fat balanced by acidity")

pr2b2, n = PROD("Iona Sauvignon Blanc Elgin", "wine_still", p2b, r2, "South Africa",
    subcategory="Sauvignon Blanc", price_tier="mid_range",
    description="Estate Elgin Sauvignon; vibrant and fresh with gooseberry, passion fruit, citrus; crisp acidity; excellent food wine showing Elgin's cool-climate character at accessible price.")
if n:
    PAIR(pr2b2, "Grilled fish tacos with mango salsa and lime", "complement", "classic", "main", "Coastal freshness; Sauvignon's citrus echoes lime; mango salsa sweetness balanced by wine's acidity")
    PAIR(pr2b2, "Vietnamese spring rolls with herb dipping sauce", "complement", "established", "starter", "Fresh rolls with herbs; Sauvignon's green herb notes mirror; acidity refreshes between bites")
    PAIR(pr2b2, "Salade Niçoise with canned tuna", "complement", "classic", "main", "Classic French salad; Sauvignon handles the anchovy and olive; green herb in wine mirrors the lettuce and herbs")
    PAIR(pr2b2, "Feta and watermelon salad with mint", "complement", "established", "starter", "Summer salad; Sauvignon's freshness suits; mint echoes wine's herbal notes; feta saltiness balanced by acidity")

# 3. HAWKE'S BAY — New Zealand
print("=== Hawke's Bay ===")
r3 = R("Hawke's Bay", "New Zealand", "wine",
        designation_type="GI",
        designation_name="Hawke's Bay GI",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="New Zealand's second largest wine region on the North Island's east coast; warmest and driest major wine region; famous for Gimblett Gravels sub-region producing world-class Bordeaux-style reds, Syrah, and Chardonnay. The ancient river gravel soils (Gimblett Gravels) create unique conditions for red wine in a country dominated by Sauvignon Blanc. Coleraine from Te Mata Estate is considered New Zealand's most collectible red wine.",
        key_producers="Te Mata Estate, Craggy Range, Trinity Hill, Elephant Hill",
        historical_context="Hawke's Bay has the longest continuous wine history in New Zealand; Mission Estate was established by Marist monks in 1851. The Gimblett Gravels discovery in the 1980s transformed the region; an ancient riverbed with extreme drainage produced wines of unexpected concentration and structure. Te Mata Estate's Coleraine is New Zealand's most awarded wine. The region has made Syrah a New Zealand specialty.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Exceptional warm dry year; Gimblett Gravels Syrah and Merlot show extraordinary concentration; Chardonnay excellent"),
    (2019, "very_good", "rising", "Good growing season; Bordeaux varieties well-structured; Syrah shows pepper and dark fruit elegance"),
    (2020, "excellent", "rising", "Excellent vintage; ideal ripening conditions; Gimblett Syrah and Merlot at their best; benchmark wines"),
    (2021, "very_good", "rising", "Good year; Hawke's Bay warmth delivered ripe structured reds; Chardonnay mineral and balanced"),
    (2022, "exceptional", "rising", "Exceptional; warm dry harvest; Gimblett Gravels produced some of New Zealand's greatest reds; landmark year"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Craggy Range", "winery", r3, "New Zealand",
        production_philosophy="terroir_driven",
        philosophy_description="New Zealand's most ambitious estate; Steve Smith MW and the Peabody family invested in single-vineyard wines across Hawke's Bay and Martinborough; Le Sol Syrah and Sophia are references.",
        reputation_narrative="The producer that transformed New Zealand's wine ambitions; Craggy Range's single-vineyard approach and Le Sol Syrah (New Zealand's most celebrated Syrah) showed the country could produce red wines of global significance.",
        price_positioning="ultra_premium")

pr3a1, n = PROD("Craggy Range Le Sol Gimblett Gravels Syrah", "wine_still", p3a, r3, "New Zealand",
    subcategory="Syrah single vineyard", price_tier="ultra_premium",
    description="New Zealand's most acclaimed Syrah; Gimblett Gravels ancient riverbed soils; dark cherry, black olive, white pepper, violets, iron mineral; silky tannins; consistently one of the Southern Hemisphere's finest Syrahs.")
if n:
    PAIR(pr3a1, "Slow-roasted lamb with rosemary and anchovy", "complement", "classic", "main", "New Zealand lamb and Syrah; anchovy adds umami depth; rosemary echoes wine's herbal notes; Hawke's Bay classic")
    PAIR(pr3a1, "Venison rack with black cherry jus and beetroot", "complement", "classic", "main", "New Zealand game; Le Sol's dark fruit mirrors cherry jus; beetroot earthiness bridges the iron mineral character")
    PAIR(pr3a1, "Aged beef short ribs with bone marrow gremolata", "complement", "established", "main", "Rich beef preparation; Syrah's structure handles; marrow richness tamed; gremolata citrus mirrors wine's fresh notes")
    PAIR(pr3a1, "Aged Manchego with olive tapenade", "complement", "established", "cheese", "Aged sheep cheese; Le Sol's olive and mineral notes echo the tapenade; Syrah's structure handles the aged fat")

pr3a2, n = PROD("Craggy Range Sophia Gimblett Gravels Merlot Cabernet", "wine_still", p3a, r3, "New Zealand",
    subcategory="Merlot Cabernet blend", price_tier="ultra_premium",
    description="Hawke's Bay's finest Bordeaux-style blend; Merlot and Cabernet Franc from Gimblett Gravels; cassis, dark plum, cedar, tobacco; structured with elegance; New Zealand's answer to Pomerol.")
if n:
    PAIR(pr3a2, "Roasted leg of lamb with herbs and garlic", "complement", "classic", "main", "Bordeaux tradition translocated to NZ; Merlot's plum fruit suits lamb; cedar echoes rosemary; elegant pairing")
    PAIR(pr3a2, "Grilled free-range duck breast with plum sauce", "complement", "classic", "main", "Duck and Merlot; plum sauce mirrors wine's fruit; cedar and tobacco notes add complexity to the pairing")
    PAIR(pr3a2, "Aged Gruyère with walnut bread", "complement", "established", "cheese", "Nutty aged cheese; Sophia's Bordeaux DNA finds its fromage partner; walnut bridges cedar and tobacco")
    PAIR(pr3a2, "Beef tenderloin with truffle jus", "complement", "classic", "main", "Premium beef; Bordeaux blend handles luxury ingredients; truffle bridges the wine's earthy depth")

p3b = P("Trinity Hill", "winery", r3, "New Zealand",
        production_philosophy="terroir_driven",
        philosophy_description="Gimblett Gravels specialist producing benchmark Hawke's Bay reds; Homage Syrah and The Gimblett are the flagship wines showing the gravels' character.",
        reputation_narrative="Key Gimblett Gravels producer consistently making benchmark Syrah and Bordeaux blends; Trinity Hill's Homage Syrah is one of New Zealand's most awarded red wines.",
        price_positioning="premium")

pr3b1, n = PROD("Trinity Hill Homage Gimblett Gravels Syrah", "wine_still", p3b, r3, "New Zealand",
    subcategory="Syrah single vineyard", price_tier="ultra_premium",
    description="Flagship Gimblett Gravels Syrah; whole-bunch fermentation; dark cherry, pepper, violets, iron; fine tannins; shows the gravels' unique character; one of New Zealand's most consistently acclaimed Syrahs.")
if n:
    PAIR(pr3b1, "Lamb shoulder slow-roasted with za'atar and yoghurt", "complement", "established", "main", "Middle Eastern preparation; Syrah's pepper and dark fruit suit the spice; yoghurt bridges the tannin")
    PAIR(pr3b1, "Grilled quail with wild mushroom and thyme", "complement", "classic", "main", "Delicate game; Homage's finesse matches quail's delicacy; mushroom and thyme echo the earthy mineral depth")
    PAIR(pr3b1, "Charcuterie with pork rillette and cornichons", "complement", "established", "starter", "Pork fat and Syrah; rillette tames the tannin; cornichon's acidity mirrors wine's freshness")
    PAIR(pr3b1, "Manchego with membrillo and marcona almonds", "complement", "established", "cheese", "Aged sheep cheese; Syrah's olive and dark fruit echo the membrillo; almonds bridge the mineral notes")

pr3b2, n = PROD("Trinity Hill Gimblett Gravels Chardonnay", "wine_still", p3b, r3, "New Zealand",
    subcategory="Chardonnay", price_tier="premium",
    description="Gimblett Gravels Chardonnay showing the warm sub-region's white wine potential; white peach, citrus cream, oak spice; fuller body than typical NZ Chardonnay; excellent food wine.")
if n:
    PAIR(pr3b2, "Blue cod with lemon butter and capers", "complement", "classic", "fish_course", "Classic New Zealand fish; Chardonnay's citrus and butter mirror the sauce; capers add mineral note")
    PAIR(pr3b2, "Corn-fed chicken with tarragon cream sauce", "complement", "classic", "main", "Cream sauce and Chardonnay; tarragon echoes wine's botanical notes; chicken perfectly suited to the weight")
    PAIR(pr3b2, "Seared hapuku with roasted fennel", "complement", "established", "fish_course", "New Zealand's premium white fish; Chardonnay's weight matches; fennel's anise echoes wine's spice notes")
    PAIR(pr3b2, "Crayfish thermidor with gruyère", "complement", "classic", "main", "New Zealand rock lobster luxury; Chardonnay handles the cheese-rich preparation; citrus lifts the richness")

# 4. MARTINBOROUGH — New Zealand
print("=== Martinborough ===")
r4 = R("Martinborough", "New Zealand", "wine",
        designation_type="GI",
        designation_name="Martinborough GI",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="New Zealand's most celebrated Pinot Noir region; remote southern North Island beyond the Rimutaka Ranges; free-draining river terrace soils, cool and dry climate with strong winds that stress the vines. Martinborough's Pinot Noir has a distinctive earthy, spicy character different from Marlborough or Central Otago. Ata Rangi and Dry River are the legendary estates that established the region's reputation.",
        key_producers="Ata Rangi, Dry River, Palliser Estate, Te Kairanga",
        historical_context="Martinborough was identified as a potential wine region by a soil scientist in 1978 using data matching Burgundy's conditions. Ata Rangi was first planted in 1980; Dry River in 1979. The region experienced rapid reputation-building in the 1990s as Ata Rangi and Dry River became globally collected. The 'Golden Triangle' of Martinborough, Wairarapa, and Gladstone has collectively made this New Zealand's most Burgundy-like wine zone.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Good Martinborough vintage; Pinot Noir shows earthy spice and red fruit; dry conditions produced concentration"),
    (2019, "excellent", "rising", "Excellent growing season; Pinot Noir of great complexity; earthy mineral character particularly pronounced"),
    (2020, "very_good", "rising", "Good year; wind stress created excellent vine balance; Pinot fragrant and structured with aging potential"),
    (2021, "exceptional", "rising", "Exceptional; Martinborough's finest in a decade; Pinot Noir of extraordinary depth; benchmark wines produced"),
    (2022, "excellent", "rising", "Excellent; cool dry conditions ideal for Pinot; earthy spice character in wine; Ata Rangi and Dry River excelled"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Ata Rangi", "winery", r4, "New Zealand",
        production_philosophy="biodynamic",
        philosophy_description="New Zealand's most revered Pinot Noir estate; Clive Paton and Phyll Paton-Brown planted the first vines in 1980; biodynamically farmed; Célèbre Pinot Noir from old vines is a national treasure.",
        reputation_narrative="The founding estate of Martinborough Pinot Noir; Ata Rangi's old vine Célèbre is New Zealand's most celebrated Pinot Noir and consistently earns comparisons to premier cru Burgundy.",
        price_positioning="ultra_premium")

pr4a1, n = PROD("Ata Rangi Célèbre Pinot Noir Martinborough", "wine_still", p4a, r4, "New Zealand",
    subcategory="Pinot Noir", price_tier="ultra_premium",
    description="New Zealand's most collected Pinot Noir; old vine Pinot from original 1980 plantings; dark cherry, spice, forest earth, truffle hints; extraordinary depth and silky texture; ages for 15+ years.")
if n:
    PAIR(pr4a1, "Slow-roasted Wairarapa duck with sour cherry sauce", "complement", "classic", "main", "Local duck with the estate wine; sour cherry mirrors Célèbre's dark cherry; slow roast creates matching richness")
    PAIR(pr4a1, "Seared beef tenderloin with mushroom duxelles", "complement", "classic", "main", "Delicate beef; old vine Pinot's depth and earthiness bridges mushroom duxelles; Burgundian tradition in NZ")
    PAIR(pr4a1, "Wild venison with blackberry reduction and turnip", "complement", "established", "main", "New Zealand game; Célèbre's dark fruit mirrors blackberry; earthy turnip bridges forest floor notes")
    PAIR(pr4a1, "Aged Époisses with crusty sourdough", "complement", "adventurous", "cheese", "Pungent Burgundian cheese; Ata Rangi's elegance and acidity handles it; the most Burgundian of NZ pairings")

pr4a2, n = PROD("Ata Rangi Pinot Noir Martinborough", "wine_still", p4a, r4, "New Zealand",
    subcategory="Pinot Noir estate", price_tier="premium",
    description="Estate Pinot Noir showing Ata Rangi's house style; red cherry, raspberry, spice, earthy mineral; silky tannins; excellent introduction to Martinborough's character at an accessible price.")
if n:
    PAIR(pr4a2, "Grilled salmon with lemon and herb butter", "complement", "classic", "fish_course", "Pacific salmon with Martinborough Pinot; acidity cuts richness; herb butter echoes wine's botanical notes")
    PAIR(pr4a2, "Roast chicken with thyme and garlic butter", "complement", "classic", "main", "Classic Pinot and chicken; thyme echoes wine's herbal spice; garlic butter richness tamed by acidity")
    PAIR(pr4a2, "Mushroom and truffle risotto", "complement", "classic", "main", "Earthy risotto; Pinot's forest floor character bridges mushrooms; truffle echoes wine's earthy depth")
    PAIR(pr4a2, "Aged Brie with black cherry jam", "complement", "established", "cheese", "Soft ripened cheese; Pinot's fruit and acidity balance the fat; cherry jam mirrors wine's red fruit")

p4b = P("Dry River", "winery", r4, "New Zealand",
        production_philosophy="traditional",
        philosophy_description="Martinborough's legendary boutique estate; Neil McCallum's pioneering work with Pinot Noir, Chardonnay, and Gewürztraminer from the 1970s set the standard; wines of extraordinary longevity.",
        reputation_narrative="The mysterious and collectible Martinborough estate; Dry River produces tiny quantities of exceptional Pinot Noir and Chardonnay released only with 3 years of aging; allocation is near-impossible to obtain.",
        price_positioning="ultra_premium")

pr4b1, n = PROD("Dry River Pinot Noir Martinborough", "wine_still", p4b, r4, "New Zealand",
    subcategory="Pinot Noir", price_tier="ultra_premium",
    description="One of New Zealand's most collectible Pinot Noirs; released after 3 years of aging; complex dark cherry, spice, earth, forest floor, leather; extraordinary texture; age-worthy for 20+ years.")
if n:
    PAIR(pr4b1, "Wild hare ragù with handmade pappardelle", "complement", "classic", "main", "Game ragù with aged Pinot; hare's intensity handled by Dry River's complexity; pasta richness matches wine's texture")
    PAIR(pr4b1, "Roasted pigeon with lentils and foie gras", "complement", "classic", "main", "Luxury game; aged Pinot's earthiness echoes the pigeon; foie gras richness tamed by acidity; Burgundian luxury")
    PAIR(pr4b1, "Aged Camembert de Normandie with walnut bread", "complement", "established", "cheese", "Classic French cheese; aged Martinborough Pinot and aged soft cheese; walnut bridges the earthy depth")
    PAIR(pr4b1, "Grilled lamb kidneys with mustard and parsley", "complement", "adventurous", "main", "Offal and aged Pinot; Dry River's complexity handles the intensity; mustard heat balanced by the wine's acidity")

pr4b2, n = PROD("Dry River Chardonnay Martinborough", "wine_still", p4b, r4, "New Zealand",
    subcategory="Chardonnay", price_tier="ultra_premium",
    description="Aged-release Martinborough Chardonnay; 3 years minimum before release; white peach, toast, chalk mineral, complex secondary development; rivals premier cru Burgundy; extremely rare.")
if n:
    PAIR(pr4b2, "Roasted crayfish with butter and tarragon", "complement", "classic", "main", "New Zealand rock lobster; aged Chardonnay's butter and mineral mirrors the preparation; tarragon echoes botanical notes")
    PAIR(pr4b2, "Seared foie gras with apple and ginger", "complement", "established", "starter", "Luxury liver; aged Chardonnay's acidity cuts the fat; apple echoes fruit in the wine; ginger adds spice bridge")
    PAIR(pr4b2, "Aged Comté with honey and walnuts", "complement", "established", "cheese", "Aged French cheese and aged NZ Chardonnay; nutty echoes align; honey bridges the stone fruit; walnuts add depth")
    PAIR(pr4b2, "Pan-seared blue cod with beurre blanc", "complement", "classic", "fish_course", "New Zealand's finest white fish; aged Chardonnay's depth and texture match; beurre blanc mirrors wine's creaminess")

# 5. MCLAREN VALE — South Australia, Australia
print("=== McLaren Vale ===")
r5 = R("McLaren Vale", "Australia", "wine",
        designation_type="GI",
        designation_name="McLaren Vale GI",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Mediterranean-influenced South Australian wine region 35km south of Adelaide; diverse soils from sand over clay to ancient schist; old vine Grenache, Shiraz, and Mourvèdre of international standing alongside Cabernet Sauvignon and Chardonnay. The 'Basso Profundo' of Australian wine — rich, full-bodied, generous. d'Arenberg's Chester Osborn and Clarendon Hills produce McLaren's most acclaimed wines.",
        key_producers="d'Arenberg, Clarendon Hills, Wirra Wirra, Chapel Hill, Yangarra Estate",
        historical_context="McLaren Vale has been planted since 1838 making it one of Australia's oldest wine regions. Old vine Grenache from 100+ year old vines is the region's most prized resource; some ancient Shiraz vines survive from the 19th century. The Mediterranean climate (dry summers, mild winters) with ocean influence from Gulf St Vincent produces wines of generous richness without excessive heat. d'Arenberg has brought eccentric artistry to McLaren; Chester Osborn's wild creativity mirrors the region's exuberant wines.")
for yr, qd, pt, sn in [
    (2018, "very_good", "stable", "Good McLaren year; old vine Grenache shows red fruit and spice; Shiraz rich and full; Mourvèdre excellent"),
    (2019, "excellent", "rising", "Excellent vintage; old vine Grenache of extraordinary depth; Shiraz concentrated and structured"),
    (2020, "very_good", "rising", "Good growing season; Mediterranean warmth balanced by sea breezes; rich and generous reds"),
    (2021, "excellent", "rising", "Excellent; old vine Grenache at its most expressive; Shiraz shows McLaren's signature richness and spice"),
    (2022, "very_good", "stable", "Good year; heat moderated by sea breezes; Grenache fragrant; Shiraz plush and full-bodied"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("d'Arenberg", "winery", r5, "Australia",
        production_philosophy="natural",
        philosophy_description="McLaren Vale's most eccentric and creative producer; Chester Osborn's boundary-pushing winemaking ranges from traditional old vine Grenache to innovative blends; The Dead Arm Shiraz is the flagship.",
        reputation_narrative="Australia's most colourfully named and creatively marketed winery; d'Arenberg's Dead Arm Shiraz and The Footbolt have built a global following; Chester Osborn's Cube tasting room is a landmark.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("d'Arenberg The Dead Arm Shiraz McLaren Vale", "wine_still", p5a, r5, "Australia",
    subcategory="Shiraz single vineyard", price_tier="ultra_premium",
    description="Named for the 'dead arm' fungal disease that reduces yield on old vines; extraordinary concentration from low-yielding old vine Shiraz; dark chocolate, blackberry, licorice, eucalyptus, iron; massive but elegant.")
if n:
    PAIR(pr5a1, "Slow-braised beef cheeks with root vegetables", "complement", "classic", "main", "Rich gelatinous beef; Dead Arm's tannin handled by collagen; root vegetables bridge the earthy mineral character")
    PAIR(pr5a1, "Grilled kangaroo loin with native pepper and quandong", "complement", "classic", "main", "Native Australian ingredients; kangaroo's iron-rich meat echoes Shiraz's iron mineral; native pepper amplifies spice")
    PAIR(pr5a1, "Aged Cheddar with Barossa dried fruit paste", "complement", "established", "cheese", "McLaren meets Barossa; aged cheese and rich Shiraz; dried fruit paste bridges dark fruit; local tradition")
    PAIR(pr5a1, "Wild boar sausage with roasted capsicum and olive oil", "complement", "established", "main", "Mediterranean preparation; Shiraz's richness suits; capsicum sweetness bridges; Mediterranean soul of McLaren")

pr5a2, n = PROD("d'Arenberg The Footbolt Shiraz McLaren Vale", "wine_still", p5a, r5, "Australia",
    subcategory="Shiraz", price_tier="mid_range",
    description="Named for the horse that won the money to buy the original vineyard; rich and accessible McLaren Shiraz; dark plum, chocolate, spice, gentle eucalyptus; velvety tannins; excellent everyday McLaren wine.")
if n:
    PAIR(pr5a2, "BBQ lamb chops with rosemary and garlic", "complement", "classic", "main", "Australian backyard classic; Footbolt's plum and spice suit grilled lamb; rosemary echoes wine's herbal notes")
    PAIR(pr5a2, "Pizza with sausage and roasted vegetables", "complement", "established", "main", "Casual dining Shiraz; wine's richness suits; roasted capsicum's sweetness bridges; accessible pairing")
    PAIR(pr5a2, "Beef and vegetable pie with tomato sauce", "complement", "established", "main", "Australian pub classic; Footbolt's plum fruit and spice mirror tomato; tannins handle the beef filling")
    PAIR(pr5a2, "Grilled halloumi with roasted cherry tomatoes", "complement", "suggested", "starter", "Mediterranean-Australian; Shiraz's fruit handles salty halloumi; tomatoes bridge acidity; unexpected but pleasant")

p5b = P("Clarendon Hills", "winery", r5, "Australia",
        production_philosophy="minimal_intervention",
        philosophy_description="Roman Bratasiuk's extreme low-yield old vine McLaren Vale; multiple single-vineyard Grenache and Syrah wines; Astralis Syrah is consistently one of Australia's most awarded and collected wines.",
        reputation_narrative="The producer who showed McLaren Vale could produce world-class Syrah; Astralis has earned 100-point scores and is allocated only; Clarendon Hills' old vine single-vineyard approach is unique in Australia.",
        price_positioning="ultra_premium")

pr5b1, n = PROD("Clarendon Hills Astralis McLaren Vale Syrah", "wine_still", p5b, r5, "Australia",
    subcategory="Syrah single vineyard", price_tier="ultra_premium",
    description="Australia's most acclaimed McLaren Vale Syrah; low-yield old vine Syrah from Clarendon sub-zone; dark cherry, black olive, iron, graphite; extraordinary concentration and elegance; multiple 100-point scores.")
if n:
    PAIR(pr5b1, "Bone-in rib-eye dry aged 45 days with compound butter", "complement", "classic", "main", "Premium beef aged to match Astralis's complexity; dry-aged funk bridges wine's iron and dark fruit")
    PAIR(pr5b1, "Whole roasted rack of lamb with anchovy and rosemary", "complement", "classic", "main", "Classic Syrah and lamb; anchovy deepens the umami; rosemary echoes wine's herbal character; luxury pairing")
    PAIR(pr5b1, "Aged Manchego with black olive tapenade", "complement", "established", "cheese", "Astralis's black olive notes echo the tapenade; aged sheep cheese handles the power; regional Mediterranean connection")
    PAIR(pr5b1, "Venison medallions with truffle and lentils", "complement", "classic", "main", "Game and truffle; Astralis's iron mineral echoes truffle's earthiness; lentil grounds the dish; luxurious match")

pr5b2, n = PROD("Clarendon Hills Blewitt Springs Old Vine Grenache", "wine_still", p5b, r5, "Australia",
    subcategory="Grenache old vine", price_tier="ultra_premium",
    description="Old vine Grenache from Blewitt Springs sand over clay; bright red cherry, raspberry, dried herbs, spice, iron; silky texture; shows McLaren Vale Grenache at its most elegant and pure.")
if n:
    PAIR(pr5b2, "Roast pork with sage and onion stuffing", "complement", "classic", "main", "Traditional pork; Grenache's silky fruit complements the sage; herbs echo wine's dried herb character")
    PAIR(pr5b2, "Lamb and pine nut flatbread with herb oil", "complement", "established", "main", "Mediterranean preparation; Grenache's herbs and fruit echo the herbs; olive oil bridges the Mediterranean soul")
    PAIR(pr5b2, "Grilled chicken with harissa and roasted peppers", "complement", "established", "main", "Spiced chicken; Grenache's fruit handles the harissa; pepper sweetness bridges wine's spice notes")
    PAIR(pr5b2, "Manchego aged 12 months with membrillo", "complement", "classic", "cheese", "Aged sheep cheese; Grenache's fruit and acidity balance the fat; membrillo bridges wine's red fruit")

# ── Summary ───────────────────────────────────────────────────────────────────
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
print("B132 complete.")
conn.close()
