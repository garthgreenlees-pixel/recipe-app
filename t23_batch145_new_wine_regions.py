#!/usr/bin/env python3
"""B145 — Stellenbosch WO, Swartland WO, Constantia WO, Walker Bay WO, Franschhoek WO (South Africa)"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(WRITE_DSN)
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
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Stellenbosch WO ───────────────────────────────────────────────────────
print("=== Stellenbosch WO ===")
r1 = R("Stellenbosch WO", "South Africa", "wine",
        designation_type="WO", designation_name="Stellenbosch",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Stellenbosch is South Africa's most prestigious wine region, producing world-class Cabernet Sauvignon, Merlot, and Chenin Blanc from diverse mountain soils. The region's granitic and sandstone slopes generate wines of remarkable complexity and ageing potential that have brought South Africa global recognition.",
        key_producers="Kanonkop, Meerlust, Rust en Vrede, Warwick Estate, Vergelegen, Waterford Estate",
        historical_context="Wine has been made around Stellenbosch since Dutch settlement in the 1680s when Simon van der Stel founded the town. The region's modern era began with post-apartheid investment in the 1990s, with estates like Meerlust and Kanonkop demonstrating that South African red wine could compete at the highest international level.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"), (2023, "very_good", "stable")]:
    VIN(r1, yr, qd, pt)

p1a = P("Kanonkop Wine Estate", "winery", r1, "South Africa",
         production_philosophy="terroir_expression",
         philosophy_description="Kanonkop is South Africa's most celebrated red wine estate, focused exclusively on Pinotage — the variety bred in South Africa from Pinot Noir and Cinsault — and Bordeaux blends. Their Paul Sauer is South Africa's most collected wine.",
         reputation_narrative="Kanonkop consistently produces South Africa's finest Pinotage and Bordeaux blends, with Paul Sauer earning placement among the world's top wines. The estate's commitment to traditional methods and Stellenbosch's mountain terroir has produced wines of extraordinary longevity.",
         price_positioning="premium")

prod1a1, new1 = PROD("Kanonkop Paul Sauer Stellenbosch", "wine_still", p1a, r1, "South Africa",
                      subcategory="Bordeaux Blend", price_tier="premium",
                      description="South Africa's most iconic wine, a Cabernet Sauvignon-led blend with Merlot and Cabernet Franc from Kanonkop's Simonsberg slopes. Paul Sauer displays profound cassis, graphite, and dried herb with the tannin structure to age gracefully for 20+ years.")
if new1:
    PAIR(prod1a1, "Grilled springbok loin with juniper berry reduction and roasted root vegetables", "complement", "classic", "main", "Paul Sauer's Bordeaux structure and dried-herb character are a natural match for game; juniper amplifies the wine's herbal depth while the root vegetable sweetness balances the tannin.")
    PAIR(prod1a1, "Kudu steak with biltong butter and mielie pap", "complement", "classic", "main", "South African game and Kanonkop's flagship is the benchmark regional pairing; biltong butter adds cured intensity while mielie pap grounds the wine's powerful tannin structure.")
    PAIR(prod1a1, "Aged Gruyère with truffle and black walnut", "complement", "established", "cheese", "Paul Sauer's graphite and cassis find resonance with aged Gruyère's nutty complexity; truffle deepens the earthy connection while black walnut mirrors the wine's tannin.")
    PAIR(prod1a1, "Lamb rack with rosemary crust and Stellenbosch olive tapenade", "complement", "classic", "main", "The wine's Bordeaux character and Stellenbosch terroir create a profound connection with lamb; local olive tapenade adds Mediterranean complexity that mirrors the wine's herb notes.")

prod1a2, new2 = PROD("Kanonkop Pinotage Stellenbosch", "wine_still", p1a, r1, "South Africa",
                      subcategory="Pinotage", price_tier="premium",
                      description="The definitive South African Pinotage, showcasing the variety's full potential: concentrated mulberry, mocha, and spice with a firm tannin structure and lengthy finish. Kanonkop's Pinotage defines what the variety can achieve at its highest level.")
if new2:
    PAIR(prod1a2, "Braai-smoked lamb chops with apricot chutney", "complement", "classic", "main", "The quintessential South African pairing: braai smoke and Pinotage's mocha character are symbiotic; apricot chutney's sweetness bridges the wine's fruit with the smoky meat.")
    PAIR(prod1a2, "Bobotie with yellow rice and peach atchar", "complement", "classic", "main", "Bobotie's Cape Malay spice and sweet-savoury character find an ideal partner in Pinotage's warm, spice-driven fruit; atchar's acidity keeps the wine's richness in balance.")
    PAIR(prod1a2, "Smoked pork ribs with chakalaka and braai bread", "complement", "established", "main", "Pinotage's robustness handles the full force of braai-smoked pork; chakalaka's spiced tomato character mirrors the wine's earthy depth while bread absorbs the intensity.")
    PAIR(prod1a2, "Dark chocolate fondant with cream and Cape gooseberry coulis", "complement", "suggested", "dessert", "The wine's mocha and dark-fruit character resonate with dark chocolate; Cape gooseberry coulis adds a tart, tropical note that lifts the pairing and mirrors South African terroir.")

p1b = P("Meerlust Estate", "winery", r1, "South Africa",
         production_philosophy="classical",
         philosophy_description="Meerlust has been in the Myburgh family for eight generations since 1756, producing Rubicon — South Africa's first Bordeaux-style blend — since 1980. The estate represents the pinnacle of South African wine tradition, combining European classical sensibility with Stellenbosch terroir.",
         reputation_narrative="Meerlust's Rubicon is one of South Africa's founding prestige wines, demonstrating as early as 1980 that the Cape could produce world-class Bordeaux blends. The estate's consistency across decades is a benchmark for South African wine heritage.",
         price_positioning="premium")

prod1b1, new3 = PROD("Meerlust Rubicon Stellenbosch", "wine_still", p1b, r1, "South Africa",
                      subcategory="Bordeaux Blend", price_tier="premium",
                      description="South Africa's original prestige Bordeaux blend, first made in 1980 by Nico Myburgh. Rubicon is a Merlot-led blend with Cabernet Sauvignon and Cabernet Franc, displaying the distinctive Meerlust character: silky texture, dark fruit, and a savoury, cedar finish of remarkable elegance.")
if new3:
    PAIR(prod1b1, "Slow-roasted beef fillet with wild mushroom sauce and truffle potato gratin", "complement", "classic", "main", "Rubicon's Merlot-driven silkiness and cedar character are ideal companions for beef fillet at this level of preparation; truffle potato gratin amplifies the wine's earthy complexity.")
    PAIR(prod1b1, "Venison pie with root vegetable gravy and puff pastry", "complement", "established", "main", "The wine's elegant structure and dark fruit complement venison's gamey richness; root vegetable gravy grounds the pairing while puff pastry adds a buttery luxury.")
    PAIR(prod1b1, "Camembert with fig jam and toasted sourdough", "bridge", "established", "cheese", "Rubicon's silk tannin and dark fruit harmonise with ripe Camembert; fig jam echoes the wine's fruit while sourdough's acidity refreshes the palate.")
    PAIR(prod1b1, "Grilled tuna with olive tapenade and anchovy butter", "contrast", "adventurous", "fish_course", "Rubicon's silk and cassis provide a compelling contrast to tuna's meaty richness; olive tapenade and anchovy butter add the savoury depth that bridges fish and red wine.")

prod1b2, new4 = PROD("Meerlust Pinot Noir Stellenbosch", "wine_still", p1b, r1, "South Africa",
                      subcategory="Pinot Noir", price_tier="premium",
                      description="A surprising achievement for Stellenbosch, Meerlust's Pinot Noir demonstrates that certain Simonsberg slopes can produce elegant, Burgundy-inflected Pinot of real depth. Displaying cherry, earth, and subtle oak with a silky texture and refreshing acidity.")
if new4:
    PAIR(prod1b2, "Pan-seared salmon with lentils and a light red wine reduction", "complement", "established", "fish_course", "Meerlust Pinot's silkiness and red-fruit character bridge the gap between fish and red wine; lentils add earthy depth while the reduction echoes the wine's character.")
    PAIR(prod1b2, "Duck breast with spiced plum sauce and roasted butternut", "complement", "established", "main", "The wine's Burgundian sensibility and cherry depth complement duck's richness; spiced plum sauce mirrors the wine's fruit while butternut adds sweetness that balances the tannin.")
    PAIR(prod1b2, "Grilled mushrooms with aged Pecorino and truffle oil", "complement", "classic", "starter", "Meerlust Pinot's earthy, cherry character resonates with mushrooms and truffle oil; Pecorino's sharp saltiness amplifies the wine's savoury depth.")
    PAIR(prod1b2, "Aged Gruyère with cherry compote and walnut bread", "complement", "established", "cheese", "The wine's cherry fruit and earthy depth find resonance with aged Gruyère's nutty complexity; cherry compote creates a direct flavour bridge between glass and board.")

# ── 2. Swartland WO ──────────────────────────────────────────────────────────
print("=== Swartland WO ===")
r2 = R("Swartland WO", "South Africa", "wine",
        designation_type="WO", designation_name="Swartland",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Swartland is South Africa's most exciting wine region, where a generation of independent producers has transformed an area of old bush-vine Chenin Blanc, Grenache, and Syrah into one of the world's most talked-about wine regions. The Swartland Revolution, sparked by Eben Sadie and colleagues, prioritises minimal intervention, dry farming, and old vines.",
        key_producers="Sadie Family Wines, Mullineux & Leeu, Intellego Wines, Leeuwenkuil Heritage Estate",
        historical_context="Swartland was historically known as bulk wine country, its ancient bush vines used for anonymous co-operative blends. The Swartland Revolution, launched by Eben Sadie around 2000, reframed the region's old vines as a world-class asset. The annual Swartland Revolution festival has attracted global attention to these wines.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r2, yr, qd, pt)

p2a = P("Sadie Family Wines", "winery", r2, "South Africa",
         production_philosophy="minimal_intervention",
         philosophy_description="Eben Sadie is the architect of the Swartland Revolution, producing single-vineyard wines from ancient Swartland bush vines with absolute minimal intervention: wild ferments, no additions, long élevage in old barrels. His Columella and Palladius are South Africa's most internationally collected wines.",
         reputation_narrative="Sadie Family Wines has achieved global cult status for Columella (Syrah/Mourvèdre) and Palladius (Chenin/Grenache Blanc blend), which consistently appear on lists of the world's greatest wines. Eben Sadie's influence on South African winemaking philosophy cannot be overstated.",
         price_positioning="ultra_premium")

prod2a1, new5 = PROD("Sadie Columella Swartland", "wine_still", p2a, r2, "South Africa",
                      subcategory="Syrah", price_tier="ultra_premium",
                      description="Sadie's flagship red, a Syrah-dominant blend with Mourvèdre from old bush vines across Swartland. Columella is one of the southern hemisphere's great wines: profound, mineral, and long-lived, combining the spice and darkness of Rhône with unmistakably South African character.")
if new5:
    PAIR(prod2a1, "Braised lamb shoulder with ras el hanout and preserved lemon couscous", "complement", "classic", "main", "Columella's Rhône-inspired depth and spice find a natural partner in North African-spiced lamb; ras el hanout mirrors the wine's complex spice profile while preserved lemon bridges its acidity.")
    PAIR(prod2a1, "Slow-roasted venison shank with truffle jus and celeriac purée", "complement", "classic", "main", "The wine's profound mineral depth and dark-fruit concentration demand this level of preparation; truffle deepens the earthy connection while celeriac purée provides textural relief.")
    PAIR(prod2a1, "Grilled ostrich fillet with blackberry reduction and sweet potato", "complement", "established", "main", "Ostrich's lean intensity and iron character resonate with Columella's dark fruit and mineral spine; blackberry reduction bridges the wine's fruit while sweet potato softens the tannin.")
    PAIR(prod2a1, "Aged Époisses with crusty bread and black walnut", "complement", "adventurous", "cheese", "Columella's power and complexity can stand up to pungent washed-rind cheese; black walnut's bitterness mirrors the wine's tannin while Époisses' richness softens both.")

prod2a2, new6 = PROD("Sadie Palladius Swartland", "wine_still", p2a, r2, "South Africa",
                      subcategory="Chenin Blanc", price_tier="ultra_premium",
                      description="Sadie's flagship white, a multi-variety blend led by old-vine Chenin Blanc with Grenache Blanc, Clairette, and other field varieties from Swartland's ancient bush vines. Palladius is one of the world's most complex white wines: oxidative depth, saline minerality, and extraordinary persistence.")
if new6:
    PAIR(prod2a2, "Abalone with lemon butter, parsley, and toasted brioche", "complement", "classic", "fish_course", "Palladius's saline mineral depth and oxidative complexity are a profound match for abalone's oceanic richness; lemon butter bridges the wine's acidity while brioche adds the luxury texture the wine demands.")
    PAIR(prod2a2, "Cape Malay curried crayfish with saffron rice and sambals", "complement", "established", "main", "The wine's aromatic complexity and textural richness navigate Cape Malay spice beautifully; saffron adds a mineral note that echoes Palladius's distinctive character.")
    PAIR(prod2a2, "White truffle pasta with Parmesan and brown butter", "complement", "classic", "main", "Palladius's oxidative depth and savoury complexity are one of the few white wines that can support white truffle; Parmesan and brown butter amplify the wine's nutty, rich character.")
    PAIR(prod2a2, "Aged Comté with honeycomb and pear", "complement", "established", "cheese", "The wine's complexity and saline depth find resonance with aged Comté's crystalline richness; honeycomb bridges the wine's subtle residual glycerol while pear echoes its fruit.")

p2b = P("Mullineux & Leeu Family Wines", "winery", r2, "South Africa",
         production_philosophy="terroir_expression",
         philosophy_description="Chris and Andrea Mullineux are Swartland's most celebrated winemaking couple, producing single-terroir Syrah, Chenin Blanc, and Straw Wine from old bush vines across the region's diverse granite, schist, and iron soils.",
         reputation_narrative="Mullineux & Leeu have achieved global recognition with their single-terroir range, demonstrating that Swartland's different soil types produce distinctly different wines. Their Straw Wine is one of South Africa's most awarded wines.",
         price_positioning="premium")

prod2b1, new7 = PROD("Mullineux Granite Syrah Swartland", "wine_still", p2b, r2, "South Africa",
                      subcategory="Syrah", price_tier="premium",
                      description="From granite soils in the Paardeberg, this single-terroir Syrah displays the elegance and floral lift characteristic of granite-grown Syrah worldwide. Violet, white pepper, and red fruit with a long, mineral finish that distinguishes it from the richer schist-grown expression.")
if new7:
    PAIR(prod2b1, "Roasted duck breast with cherry compote and lavender jus", "complement", "classic", "main", "Granite Syrah's violet and red-fruit character is a natural companion for duck; cherry compote creates a direct flavour bridge while lavender echoes the wine's floral lift.")
    PAIR(prod2b1, "Lamb loin with olive tapenade and roasted root vegetables", "complement", "established", "main", "The wine's elegant structure and Rhône character find a natural partner in lamb with olive; root vegetables add sweetness that balances the wine's mineral acidity.")
    PAIR(prod2b1, "Grilled quail with truffle butter and wild mushroom ragù", "complement", "established", "main", "Granite Syrah's delicacy and floral lift suit the lightness of quail; truffle butter deepens the earthy character while wild mushroom ragù resonates with the wine's Rhône heritage.")
    PAIR(prod2b1, "Aged Manchego with dried fig and rosemary crackers", "complement", "established", "cheese", "The wine's red fruit and violet find harmony with aged Manchego's nuttiness; dried fig mirrors the wine's fruit while rosemary echoes its herbal character.")

prod2b2, new8 = PROD("Mullineux Chenin Blanc Old Vines Swartland", "wine_still", p2b, r2, "South Africa",
                      subcategory="Chenin Blanc", price_tier="premium",
                      description="From ancient Swartland bush vines across granite, schist, and iron soils, this Chenin Blanc captures the full complexity of old-vine fruit: quince, beeswax, and hay with a rich mid-palate and a long, saline mineral finish. A benchmark for the variety outside the Loire.")
if new8:
    PAIR(prod2b2, "Roasted chicken with honey-mustard glaze and roasted stone fruit", "complement", "classic", "main", "Old-vine Chenin's honeyed richness and acidity are an ideal complement to roasted chicken; honey-mustard mirrors the wine's beeswax character while stone fruit bridges its fruit profile.")
    PAIR(prod2b2, "Pan-fried sole with lemon caper butter and sautéed greens", "complement", "established", "fish_course", "The wine's saline depth and textural richness bridge sole's delicacy without overwhelming it; lemon caper butter mirrors the wine's acidity while amplifying its mineral character.")
    PAIR(prod2b2, "Thai fish cakes with green papaya salad and sweet chili", "complement", "established", "starter", "Old-vine Chenin's aromatic complexity and off-dry richness navigate Thai spice and sweetness beautifully; papaya's acidity echoes the wine's freshness.")
    PAIR(prod2b2, "Aged Gruyère with quince paste and walnut bread", "bridge", "established", "cheese", "The wine's quince and beeswax character creates a direct flavour bridge with the cheese board; walnut bread's depth resonates with the wine's rich, old-vine complexity.")

# ── 3. Constantia WO ─────────────────────────────────────────────────────────
print("=== Constantia WO ===")
r3 = R("Constantia WO", "South Africa", "wine",
        designation_type="WO", designation_name="Constantia",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Constantia is South Africa's oldest wine region and the birthplace of Vin de Constance, the legendary sweet Muscat wine that captivated Napoleon, Baudelaire, and Jane Austen. The cool, maritime climate on the Cape Peninsula produces elegant whites, Sauvignon Blanc, and dessert wines of world significance.",
        key_producers="Klein Constantia, Buitenverwachting, Groot Constantia, Steenberg Vineyards",
        historical_context="Simon van der Stel established the Constantia estate in 1685, and by the 18th century its sweet Muscat de Frontignan — Vin de Constance — was considered one of the world's greatest wines, traded across Europe and mentioned by Austen, Dickens, and Baudelaire. Klein Constantia revived Vin de Constance in 1986 and re-established Constantia's global reputation.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "stable"),
    (2022, "very_good", "stable"), (2023, "excellent", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Klein Constantia", "winery", r3, "South Africa",
         production_philosophy="classical",
         philosophy_description="Klein Constantia revived the historic Vin de Constance in 1986 using the original Muscat de Frontignan variety from the estate's original 17th-century planting sites. The estate also produces exceptional Sauvignon Blanc under the KC label.",
         reputation_narrative="Klein Constantia's revival of Vin de Constance is one of South African wine's great achievements, restoring a wine that had been absent for over a century. The wine's global acclaim — it appears on lists of the world's greatest dessert wines — has elevated the entire Constantia region.",
         price_positioning="premium")

prod3a1, new9 = PROD("Klein Constantia Vin de Constance", "wine_still", p3a, r3, "South Africa",
                      subcategory="Muscat", price_tier="premium",
                      description="The revival of one of the world's great dessert wines, made from Muscat de Frontignan picked at extreme ripeness. Vin de Constance is gloriously complex: orange blossom, apricot jam, marmalade, and honey with a crystalline acidity that prevents any sense of cloying sweetness. Ageable for decades.")
if new9:
    PAIR(prod3a1, "Foie gras terrine with brioche and spiced orange marmalade", "complement", "classic", "starter", "The wine's orange blossom and marmalade character creates a direct flavour bridge with spiced orange; foie gras's richness is cut by the wine's acidity, making this a classic sweet pairing.")
    PAIR(prod3a1, "Blue cheese with honeycomb and dried apricot", "complement", "classic", "cheese", "Sweet wine and blue cheese is a classic of the dessert table; Vin de Constance's floral sweetness contrasts with Roquefort-style intensity while honeycomb echoes the wine's own character.")
    PAIR(prod3a1, "Peach tarte tatin with crème fraîche and vanilla", "complement", "established", "dessert", "The wine's apricot and peach character mirrors the tarte tatin's stone fruit; crème fraîche bridges the wine's acidity while vanilla resonates with its floral depth.")
    PAIR(prod3a1, "Cured duck prosciutto with fig and pistachio", "bridge", "adventurous", "pre_dessert", "An unconventional but compelling match: the wine's sweetness and acidity navigate cured duck's salty intensity; fig echoes its fruit while pistachio adds a savoury bitter note.")

prod3a2, new10 = PROD("Klein Constantia Sauvignon Blanc Constantia", "wine_still", p3a, r3, "South Africa",
                       subcategory="Sauvignon Blanc", price_tier="mid_range",
                       description="Klein Constantia's Sauvignon Blanc is one of South Africa's finest, benefiting from the cool maritime climate and well-drained granite soils. Displaying vibrant gooseberry, passion fruit, and fresh herb with a long, mineral finish of impressive persistence.")
if new10:
    PAIR(prod3a2, "Grilled asparagus with hollandaise and lemon zest", "complement", "classic", "starter", "Constantia Sauvignon's green herb and citrus character are a classic match for asparagus; hollandaise's richness is balanced by the wine's crisp acidity.")
    PAIR(prod3a2, "Seared sea bass with salsa verde and crushed peas", "complement", "classic", "fish_course", "The wine's passion fruit and herb character complement sea bass's delicate sweetness; salsa verde's herbaceous acidity mirrors the wine's own herb-driven character.")
    PAIR(prod3a2, "Cape Malay pickled fish with pickled vegetables and bread", "complement", "established", "starter", "Constantia Sauvignon's vibrant acidity and citrus character are the ideal partner for pickled fish; the wine's fruit weight handles the spiced vinegar marinade with ease.")
    PAIR(prod3a2, "Fresh goat cheese with herb salad and lemon vinaigrette", "complement", "classic", "starter", "A benchmark pairing: Sauvignon Blanc's herbaceous acidity mirrors fresh goat cheese's tang; lemon vinaigrette amplifies both while herb salad creates a green, aromatic connection.")

p3b = P("Buitenverwachting", "winery", r3, "South Africa",
         production_philosophy="sustainable",
         philosophy_description="Buitenverwachting is one of Constantia's largest estates, farming sustainably in the valley with a focus on Sauvignon Blanc, red blends, and the occasional dessert wine from their historic Constantia soils.",
         reputation_narrative="Buitenverwachting is respected for consistent quality across its range and for being one of Constantia's most visitor-friendly estates, maintaining a strong restaurant on the property that has served as an ambassador for South African wine and food culture.",
         price_positioning="mid_range")

prod3b1, new11 = PROD("Buitenverwachting Christine Constantia", "wine_still", p3b, r3, "South Africa",
                       subcategory="Bordeaux Blend", price_tier="premium",
                       description="Buitenverwachting's flagship red, a Cabernet Sauvignon-led Bordeaux blend named after Christine Müller. Christine displays the cool-climate Constantia character in red wine: restrained cassis, cedar, and graphite with elegant tannin structure and impressive longevity.")
if new11:
    PAIR(prod3b1, "Lamb rack with mint and pistachio crust and red wine jus", "complement", "classic", "main", "Christine's Bordeaux character and cool-climate restraint are a natural match for lamb rack; mint and pistachio add aromatic complexity while red wine jus bridges the savoury depth.")
    PAIR(prod3b1, "Pan-seared duck breast with cherry reduction and potato dauphinoise", "complement", "established", "main", "The wine's cassis and cedar find resonance with duck and cherry; potato dauphinoise's cream richness is balanced by the wine's elegant acidity.")
    PAIR(prod3b1, "Aged Cheddar with quince paste and toasted almonds", "complement", "established", "cheese", "Christine's cassis and graphite harmonise with aged cheddar's sharpness; quince paste bridges the wine's fruit while almonds add savoury texture.")
    PAIR(prod3b1, "Beef tenderloin Wellington with wild mushroom duxelles", "complement", "classic", "main", "The wine's Bordeaux structure and restrained power suit the elegance of beef Wellington; mushroom duxelles deepens the earthy connection between pastry and wine.")

prod3b2, new12 = PROD("Buitenverwachting Sauvignon Blanc Constantia", "wine_still", p3b, r3, "South Africa",
                       subcategory="Sauvignon Blanc", price_tier="mid_range",
                       description="A vibrant Constantia Sauvignon Blanc with gooseberry, lime, and fresh-cut grass character, vinified in stainless steel to preserve its energetic freshness and natural acidity. One of the Cape's most consistent, food-friendly whites.")
if new12:
    PAIR(prod3b2, "Grilled prawns with garlic butter and lemon wedges", "complement", "classic", "starter", "The wine's citrus acidity and herbaceous lift are ideal complements to garlic butter prawns; lemon reinforces the wine's freshness while the garlic adds savoury depth.")
    PAIR(prod3b2, "Thai prawn salad with lime dressing and fresh coriander", "complement", "established", "starter", "The wine's lime and herb character mirrors the Thai dressing's freshness; prawn's sweetness is highlighted by the wine's vivid acidity.")
    PAIR(prod3b2, "Grilled hake with lemon butter and roasted Cape vegetables", "complement", "classic", "fish_course", "Constantia Sauvignon is the Cape's go-to white with local fish; the wine's herb and citrus notes frame hake's sweetness perfectly while the vegetable roast adds depth.")
    PAIR(prod3b2, "Fresh chèvre with herb oil and Cape sourdough", "complement", "classic", "aperitif", "The quintessential Sauvignon Blanc and goat cheese pairing works as well in South Africa as in the Loire; herb oil bridges the wine's aromatic character while sourdough grounds the combination.")

# ── 4. Walker Bay WO ─────────────────────────────────────────────────────────
print("=== Walker Bay WO ===")
r4 = R("Walker Bay WO", "South Africa", "wine",
        designation_type="WO", designation_name="Walker Bay",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Walker Bay, centred on the coastal town of Hermanus, is South Africa's coolest wine-producing region, generating Pinot Noir and Chardonnay of world-class quality. The Hemel-en-Aarde Valley within Walker Bay has emerged as South Africa's Burgundy, producing wines of extraordinary elegance and minerality.",
        key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Newton Johnson Wines",
        historical_context="Tim Hamilton Russell was the pioneer who identified Walker Bay's Burgundian potential in the 1970s, establishing what would become Hamilton Russell Vineyards in 1975. The difficulty of growing Pinot Noir in the Cape was solved not by temperature manipulation but by site selection — the cool maritime Walker Bay climate proved ideal. Today, the Hemel-en-Aarde Valley attracts global attention as Africa's answer to Burgundy.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "excellent", "rising")]:
    VIN(r4, yr, qd, pt)

p4a = P("Hamilton Russell Vineyards", "winery", r4, "South Africa",
         production_philosophy="terroir_expression",
         philosophy_description="Hamilton Russell is South Africa's Burgundy benchmark, producing Pinot Noir and Chardonnay exclusively from the Hemel-en-Aarde Valley since 1975. Tim Hamilton Russell's visionary site selection and his son Anthony's continuation of the estate's Burgundian philosophy have created Africa's most internationally respected Pinot Noir.",
         reputation_narrative="Hamilton Russell Vineyards Pinot Noir and Chardonnay consistently appear among the New World's finest expressions of these Burgundian varieties. The wines are collected globally and demonstrate that Africa can produce world-class cool-climate wine.",
         price_positioning="premium")

prod4a1, new13 = PROD("Hamilton Russell Pinot Noir Hemel-en-Aarde", "wine_still", p4a, r4, "South Africa",
                       subcategory="Pinot Noir", price_tier="premium",
                       description="South Africa's benchmark Pinot Noir, grown on the clay-rich soils of the Hemel-en-Aarde Valley with direct Atlantic Ocean influence. The wine displays Burgundian restraint and precision: wild strawberry, earth, and graphite with a silky texture and long, mineral finish that improves over 10+ years.")
if new13:
    PAIR(prod4a1, "Seared salmon with beetroot purée and dill crème fraîche", "complement", "classic", "fish_course", "Hamilton Russell Pinot's silk tannin and red-fruit brightness are the Cape's benchmark salmon pairing; beetroot purée mirrors the wine's earth while dill crème fraîche adds a refreshing contrast.")
    PAIR(prod4a1, "Roasted guinea fowl with mushroom fricassee and thyme jus", "complement", "established", "main", "Guinea fowl's delicacy and earthy mushroom fricassee call for this level of Pinot; the wine's silk tannin and forest-floor character create a seamless connection.")
    PAIR(prod4a1, "Duck breast with cherry and cassis sauce and root vegetables", "complement", "classic", "main", "The wine's cherry and earth find natural resonance with duck; cassis sauce deepens the fruit connection while root vegetables add the sweetness that balances the tannin.")
    PAIR(prod4a1, "Aged Comté with dried cherry and dark chocolate", "complement", "established", "cheese", "Comté's nutty complexity and the wine's forest-floor earthiness are a classic pairing; dried cherry bridges the wine's fruit while dark chocolate adds a luxurious bitter note.")

prod4a2, new14 = PROD("Hamilton Russell Chardonnay Hemel-en-Aarde", "wine_still", p4a, r4, "South Africa",
                       subcategory="Chardonnay", price_tier="premium",
                       description="Matched in acclaim with the estate's Pinot Noir, Hamilton Russell Chardonnay is South Africa's most Burgundian white wine. Fermented with wild yeasts in French oak, it displays lemon curd, toasted hazelnut, and a saline mineral finish of remarkable length and precision.")
if new14:
    PAIR(prod4a2, "Line fish with lemon butter, capers, and herb salad", "complement", "classic", "fish_course", "The wine's lemon curd and mineral depth are ideal for fresh Cape fish; capers amplify the wine's acidity while herb salad echoes its subtle herbaceous lift.")
    PAIR(prod4a2, "Abalone with garlic butter and parsley", "complement", "established", "fish_course", "South Africa's prized abalone demands the depth of Hamilton Russell Chardonnay; the wine's saline minerality mirrors the shellfish's oceanic character while the garlic butter bridges its richness.")
    PAIR(prod4a2, "Roasted lobster with champagne beurre blanc and tarragon", "complement", "classic", "main", "The wine's hazelnut depth and creamy texture create a natural partnership with lobster; champagne beurre blanc mirrors the wine's fermentation character while tarragon adds aromatic lift.")
    PAIR(prod4a2, "Aged Gruyère and white truffle tasting with crackers", "complement", "established", "cheese", "The wine's hazelnut complexity and mineral depth are uniquely equipped to handle white truffle; Gruyère's crystalline richness extends the wine's complex finish.")

p4b = P("Bouchard Finlayson", "winery", r4, "South Africa",
         production_philosophy="classical",
         philosophy_description="Founded by Peter Finlayson in the Hemel-en-Aarde Valley in 1989, Bouchard Finlayson produces Pinot Noir and Chardonnay under the guidance of one of South Africa's most experienced Pinot specialists. A Burgundian philosophy applied with Cape precision.",
         reputation_narrative="Bouchard Finlayson is one of Walker Bay's founding estates, with Peter Finlayson's decades of experience producing Pinot Noir in the Cape reflected in wines of consistent elegance and increasing quality. Their Galpin Peak Pinot Noir is among South Africa's finest.",
         price_positioning="premium")

prod4b1, new15 = PROD("Bouchard Finlayson Galpin Peak Pinot Noir Walker Bay", "wine_still", p4b, r4, "South Africa",
                       subcategory="Pinot Noir", price_tier="premium",
                       description="Named after the rocky Galpin Peak above the Hemel-en-Aarde estate, this Pinot Noir is Bouchard Finlayson's flagship: concentrated wild cherry, dark plum, and truffle with a firm, age-worthy structure and long mineral finish.")
if new15:
    PAIR(prod4b1, "Venison medallions with wild mushroom cream and polenta", "complement", "established", "main", "The wine's depth and dark-fruit concentration demand game meat; wild mushroom cream deepens the earthy resonance while polenta adds the textural base the wine's structure requires.")
    PAIR(prod4b1, "Pan-roasted duck with spiced fig compote and lentils", "complement", "established", "main", "Galpin Peak's dark-plum depth and truffle character find an ideal companion in duck with fig; spiced compote mirrors the wine's fruit while lentils add the earthy counterpoint.")
    PAIR(prod4b1, "Aged Manchego with truffle honey and roasted pistachios", "complement", "established", "cheese", "The wine's truffle character creates a direct bridge with truffle honey; Manchego's aged nuttiness and pistachios add the savoury complexity the wine's depth demands.")
    PAIR(prod4b1, "Lamb loin with olive and anchovy butter and ratatouille", "complement", "classic", "main", "Galpin Peak's structure and dark fruit suit lamb's richness; olive and anchovy butter add Mediterranean depth while ratatouille's acidity keeps the pairing lively.")

prod4b2, new16 = PROD("Bouchard Finlayson Missionvale Chardonnay Walker Bay", "wine_still", p4b, r4, "South Africa",
                       subcategory="Chardonnay", price_tier="mid_range",
                       description="A pure, mineral expression of Walker Bay Chardonnay from Bouchard Finlayson's Missionvale label, offering the cool-climate freshness of the Hemel-en-Aarde without the weight of fuller-bodied expressions. Citrus, stone fruit, and a clean mineral finish.")
if new16:
    PAIR(prod4b2, "Grilled Cape salmon with herb butter and roasted asparagus", "complement", "classic", "fish_course", "The wine's citrus freshness and mineral lift are a natural complement to grilled fish; herb butter adds richness that the wine's acidity can cut through with ease.")
    PAIR(prod4b2, "Prawn and avocado salad with lime dressing", "complement", "classic", "starter", "Walker Bay Chardonnay's freshness and stone-fruit character are ideal for prawn and avocado; lime dressing echoes the wine's citrus acidity.")
    PAIR(prod4b2, "Crab linguine with lemon, chili, and parsley", "complement", "established", "main", "The wine's citrus acidity and clean mineral finish are perfectly calibrated for seafood pasta; the lemon and parsley echo the wine's own freshness while chili adds a contrast note.")
    PAIR(prod4b2, "Fresh ricotta with lemon zest and Cape honey on sourdough", "complement", "suggested", "aperitif", "The wine's citrus and stone-fruit character find a gentle match in fresh ricotta; Cape honey bridges the wine's subtle sweetness while sourdough grounds the combination.")

# ── 5. Franschhoek WO ────────────────────────────────────────────────────────
print("=== Franschhoek WO ===")
r5 = R("Franschhoek WO", "South Africa", "wine",
        designation_type="WO", designation_name="Franschhoek",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Franschhoek — 'French Corner' — was settled by French Huguenot refugees in the 1680s, who brought their winemaking traditions to this picturesque valley east of Stellenbosch. Today it produces excellent Semillon, Cabernet Sauvignon, and blends from mountain vineyards, and is South Africa's culinary capital with an extraordinary concentration of top restaurants.",
        key_producers="Boekenhoutskloof, La Motte, Môreson, Stony Brook, Chamonix Wine Farm",
        historical_context="The Huguenot settlers who arrived in Franschhoek in 1688 established a winemaking tradition that persisted through various ownership changes. The valley's culinary reputation grew alongside its wine quality in the post-apartheid era, making it South Africa's most visited wine tourism destination and home to some of the country's best restaurants.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r5, yr, qd, pt)

p5a = P("Boekenhoutskloof Winery", "winery", r5, "South Africa",
         production_philosophy="artisanal",
         philosophy_description="Boekenhoutskloof, founded in 1776 and relaunched by Marc Kent in 1994, has become one of South Africa's most dynamic wine producers, with a portfolio ranging from the ultra-premium flagship Boekenhoutskloof Syrah and Cabernet to the hugely popular Wolftrap and Porcupine Ridge ranges.",
         reputation_narrative="Boekenhoutskloof's Syrah is consistently rated as one of South Africa's finest red wines, while its Semillon demonstrates what the variety can achieve in Franschhoek. Marc Kent's commitment to quality across all price points has made Boekenhoutskloof one of South Africa's most influential wine estates.",
         price_positioning="premium")

prod5a1, new17 = PROD("Boekenhoutskloof Syrah Franschhoek", "wine_still", p5a, r5, "South Africa",
                       subcategory="Syrah", price_tier="premium",
                       description="Boekenhoutskloof's flagship, one of South Africa's greatest Syrhas: from cooler, high-altitude Franschhoek vineyards, it displays the Northern Rhône character of violet, white pepper, and dark olive alongside dense black fruit and a remarkable mineral finish. Consistently among South Africa's top-rated wines.")
if new17:
    PAIR(prod5a1, "Braised lamb neck with Moroccan spices and couscous", "complement", "classic", "main", "The wine's Northern Rhône character and Syrah spice are at home with Moroccan-spiced lamb; couscous absorbs the sauce while the spice blend echoes the wine's own complexity.")
    PAIR(prod5a1, "Grilled kudu steak with smoked bone marrow and roasted garlic", "complement", "classic", "main", "South African game demands this level of Syrah; bone marrow's luxury richness and roasted garlic's depth create a pairing of extraordinary intensity and coherence.")
    PAIR(prod5a1, "Venison cassoulet with duck confit and white beans", "complement", "established", "main", "The wine's power and spice can stand up to the full richness of cassoulet; white beans soften the tannin while duck confit and venison provide the protein depth the wine demands.")
    PAIR(prod5a1, "Aged Époisses with walnut bread and quince paste", "complement", "adventurous", "cheese", "Boekenhoutskloof Syrah's power and complexity can stand up to pungent washed-rind cheese; quince paste bridges the wine's fruit while walnut bread grounds the pairing.")

prod5a2, new18 = PROD("Boekenhoutskloof Semillon Franschhoek", "wine_still", p5a, r5, "South Africa",
                       subcategory="Semillon", price_tier="premium",
                       description="Franschhoek's signature white variety at its finest, from old Semillon vines vinified with wild fermentation and extended oak élevage. Boekenhoutskloof Semillon displays lemon curd, beeswax, and lanolin with a luscious texture and a finish of extraordinary complexity and persistence.")
if new18:
    PAIR(prod5a2, "Pan-roasted crayfish with saffron butter and fennel", "complement", "classic", "main", "Old-vine Semillon's texture and lemon-beeswax character are a profound match for crayfish; saffron's minerality echoes the wine's complexity while fennel bridges its anise-like depth.")
    PAIR(prod5a2, "Sole meunière with brown butter, lemon, and capers", "complement", "classic", "fish_course", "Sole meunière's butter-lemon simplicity showcases the wine's lush texture and citrus depth; the brown butter's nuttiness echoes the Semillon's beeswax character in a classic pairing.")
    PAIR(prod5a2, "White asparagus with smoked salmon and hollandaise", "complement", "established", "starter", "The wine's textural richness and citrus character navigate hollandaise's richness while echoing asparagus's subtle bitterness; smoked salmon adds the saline note that amplifies the wine's mineral depth.")
    PAIR(prod5a2, "Aged Gruyère with honeycomb and fig", "complement", "established", "cheese", "Old-vine Semillon's beeswax and honey notes create a direct bridge with honeycomb; Gruyère's crystalline nuttiness extends the wine's complex finish while fig adds fruity depth.")

p5b = P("La Motte Wine Estate", "winery", r5, "South Africa",
         production_philosophy="sustainable",
         philosophy_description="La Motte is one of Franschhoek's oldest estates, owned by the Rupert family, producing a wide range of wines with a focus on Shiraz, Cabernet Sauvignon, and Chardonnay. The estate combines winemaking excellence with a strong cultural and culinary programme.",
         reputation_narrative="La Motte is Franschhoek's largest producer and one of the valley's most respected names, known for consistent quality across its range and for the estate's investment in South African cultural heritage through its museum and art collection.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("La Motte Shiraz Franschhoek", "wine_still", p5b, r5, "South Africa",
                       subcategory="Shiraz", price_tier="mid_range",
                       description="La Motte's flagship red, a consistently excellent Franschhoek Shiraz with black cherry, dark chocolate, and warm spice character. Aged in French oak for 12 months, it offers exceptional value for the complexity and structure it delivers.")
if new19:
    PAIR(prod5b1, "Slow-roasted lamb shoulder with spiced plum chutney", "complement", "classic", "main", "La Motte Shiraz's warm spice and black-fruit character are a natural match for South African braised lamb; spiced plum chutney creates a direct flavour bridge between wine and food.")
    PAIR(prod5b1, "Pork belly with five-spice and apple compote", "complement", "established", "main", "The wine's warm spice and dark fruit suit pork belly's richness; five-spice echoes the wine's own spice profile while apple compote provides the bright acidity the pairing needs.")
    PAIR(prod5b1, "Beef and mushroom pie with rich gravy", "complement", "classic", "main", "The wine's medium weight and dark-fruit character are ideal for a well-made pie; mushroom's umami and the gravy's richness deepen the wine's own savoury character.")
    PAIR(prod5b1, "Aged Cheddar with biltong and dried fruit", "complement", "established", "cheese", "The wine's South African character is perfectly reflected in a local cheese board with biltong; the cured meat's intensity and the cheese's sharpness find traction against the wine's fruit.")

prod5b2, new20 = PROD("La Motte Chardonnay Franschhoek", "wine_still", p5b, r5, "South Africa",
                       subcategory="Chardonnay", price_tier="mid_range",
                       description="A well-made Franschhoek Chardonnay with ripe peach, citrus, and subtle oak character, fermented partly in French barrique to add complexity without heaviness. Consistent, food-friendly, and excellent value for a Cape Chardonnay.")
if new20:
    PAIR(prod5b2, "Grilled chicken Caesar salad with aged Parmesan and anchovies", "complement", "classic", "casual", "The wine's ripe fruit and subtle oak are ideal for a substantial salad of this type; Parmesan and anchovies add the umami depth that lifts the wine's character.")
    PAIR(prod5b2, "Roasted butternut soup with crème fraîche and toasted seeds", "complement", "established", "starter", "The wine's peach and subtle oak character resonate with butternut's sweetness; crème fraîche bridges the wine's acidity while toasted seeds add textural contrast.")
    PAIR(prod5b2, "Pan-fried yellowtail with herb butter and roasted vegetables", "complement", "classic", "fish_course", "Yellowtail is a Cape favourite well matched by Franschhoek Chardonnay; the wine's ripe fruit and subtle richness frame the fish's flavour without overwhelming its delicacy.")
    PAIR(prod5b2, "Brie with Cape gooseberry jam and water crackers", "bridge", "established", "cheese", "The wine's stone-fruit character bridges the brie's creaminess and gooseberry's tartness; the combination is a quintessentially Cape cheese experience.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
print("B145 complete.")
conn.close()
