#!/usr/bin/env python3
"""B166 — Australian + NZ + German: Yarra Valley, McLaren Vale, Martinborough, Hawke's Bay, Württemberg QbA"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
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

# === YARRA VALLEY GI ===
print("=== Yarra Valley GI ===")
r1 = R("Yarra Valley GI", "Australia", "wine",
       designation_type="GI",
       designation_name="Yarra Valley Geographic Indication",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The Yarra Valley, one hour east of Melbourne, is Australia's most prestigious cool-climate wine region. The valley's diverse altitudes (50–400m) create two distinct zones: the warmer Lower Yarra (Chardonnay, sparkling) and cooler Upper Yarra (Pinot Noir, Chardonnay). Great Yarra Pinot Noir rivals top Burgundy in elegance and complexity, while Chardonnay shows restraint and mineral precision uncommon in Australian whites. Yering Station, Coldstream Hills, and Oakridge have defined the region's style since the 1980s.",
       key_producers="Yering Station, Coldstream Hills, Oakridge Wines, Mac Forbes, Seville Estate",
       historical_context="The Yarra Valley is one of Australia's oldest wine regions, established in the 1830s. After a period of dormancy in the early 20th century, the modern era was revived in the 1960s when producers recognised the valley's potential for cool-climate varieties. It is now Australia's most important Pinot Noir region.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Benchmark Upper Yarra Pinot Noir vintage — wines of Burgundian elegance and precision."),
    (2020,"challenging","stable","Bushfire smoke affected many wines; some producers in unaffected areas produced good quality."),
    (2021,"excellent","rising","Outstanding recovery vintage — Pinot and Chardonnay of exceptional freshness and depth."),
    (2022,"very_good","stable","Fine conditions; Upper Yarra particularly successful for structured, age-worthy Pinot Noir."),
    (2023,"excellent","rising","A landmark Yarra vintage — among the finest Chardonnay and Pinot Noir in recent memory."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Mac Forbes Wines Yarra Valley", "winery", r1, "Australia",
       production_philosophy="minimal_intervention",
       philosophy_description="Mac Forbes produces small-batch, single-vineyard Yarra Valley Pinot Noir and Chardonnay using minimal intervention and native yeasts. His village-style wines from different Yarra sub-regions demonstrate the valley's terroir diversity at a Burgundian level of precision.",
       reputation_narrative="Mac Forbes is Yarra Valley's most acclaimed artisan producer — his approach of site-specific, minimal intervention winemaking has helped define a new style of Australian Pinot Noir that prioritises elegance, restraint, and terroir expression over power.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Mac Forbes Upper Yarra Pinot Noir", "wine_still", p1, r1, "Australia",
                    subcategory="red", description="Site-specific Upper Yarra Pinot Noir from cool, high-altitude sites — elegant, Burgundian in profile. Red cherry, raspberry, violet, dried herbs, fine tannins, and a long mineral finish. Among Australia's finest Pinot expressions.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted duck breast with cherry jus and lentils", "complement", "classic", "main", "The wine's cherry and mineral finesse matches duck's richness; cherry jus echoes Pinot's fruit character.")
    PAIR(prod, "Mushroom and truffle risotto with parmesan", "bridge", "classic", "main", "Earthy Upper Yarra mineral notes bridge to truffle and mushroom; Pinot's red fruit brightens the earthy depth.")
    PAIR(prod, "Pan-roasted salmon fillet with pinot reduction", "complement", "established", "main", "One of the great fish-red wine pairings — Yarra Pinot's delicacy and acidity match salmon's richness perfectly.")
    PAIR(prod, "Aged Yarra Valley goat cheese with fig", "complement", "established", "cheese", "Local cheese with local Pinot Noir — the wine's mineral freshness complements goat cheese's tang; fig bridges the fruit.")
prod, is_new = PROD("Mac Forbes Woori Yallock Chardonnay Yarra Valley", "wine_still", p1, r1, "Australia",
                    subcategory="white", description="Cool-climate Yarra Chardonnay with natural fermentation and restrained oak. White peach, citrus, almond, ginger, and a mineral precision reminiscent of fine Burgundy. A far cry from typical Australian Chardonnay — subtle and age-worthy.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted whole chicken with butter and tarragon", "complement", "classic", "main", "Classic Burgundy-style Chardonnay pairing — the wine's almond and citrus notes echo the tarragon butter.")
    PAIR(prod, "Grilled half-shell scallops with lemon butter", "complement", "classic", "starter", "Mineral Chardonnay and sweet scallops share creamy depth; lemon mirrors the wine's citrus character.")
    PAIR(prod, "White asparagus with beurre blanc and chives", "complement", "established", "starter", "Restraint in the Chardonnay mirrors asparagus's delicacy; almond notes bridge the beurre blanc perfectly.")
    PAIR(prod, "Aged Comté or local mountain cheese with hazelnuts", "complement", "established", "cheese", "Almond and nutty notes in the Chardonnay bridge to Comté's nuttiness; hazelnuts deepen the connection.")

p2 = P("Yering Station Winery", "winery", r1, "Australia",
       production_philosophy="terroir_expression",
       philosophy_description="The Yarra Valley's oldest continuously operating winery (1838), Yering Station produces wines from multiple estate vineyards across the valley. Their Village and premium range demonstrates the breadth of Yarra Valley's cool-climate expression.",
       reputation_narrative="Yering Station is the Yarra Valley's founding estate and a benchmark for the region's style. Their sparkling and still Chardonnay wines are among Victoria's finest, and the estate's history makes it a cultural landmark in Australian wine.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Yering Station Village Chardonnay Yarra Valley", "wine_still", p2, r1, "Australia",
                    subcategory="white", description="Estate Chardonnay representing the Lower Yarra's warmer conditions — stone fruit, toasted almond, oak spice, and a creamy texture. More generously styled than Upper Yarra, with excellent balance and food versatility.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled coral trout with caper and lemon butter", "complement", "classic", "main", "The wine's stone fruit and oak bridge to the butter sauce; capers echo Chardonnay's natural acidity.")
    PAIR(prod, "Slow-roasted pork belly with fennel and apple", "complement", "established", "main", "Creamy Chardonnay matches pork's richness; apple echoes the stone fruit character; fennel bridges the oak.")
    PAIR(prod, "Lobster bisque with cream and brandy", "complement", "classic", "starter", "The wine's stone fruit and cream match bisque's richness; brandy's warmth echoes the Chardonnay's oak.")
    PAIR(prod, "Triple-cream brie with quince paste", "complement", "classic", "cheese", "The wine's creaminess mirrors brie's texture; oak spice bridges to the cheese's umami depth.")

# === MCLAREN VALE GI ===
print("=== McLaren Vale GI ===")
r2 = R("McLaren Vale GI", "Australia", "wine",
       designation_type="GI",
       designation_name="McLaren Vale Geographic Indication",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="McLaren Vale, 40km south of Adelaide on the Fleurieu Peninsula, is Australia's most Mediterranean-influenced wine region. Old-vine Grenache (some vines planted 1880s), Shiraz, and Mataro (Mourvèdre) grown on ancient soils — including kaolinised granite, ironstone, and black cracking clay — produce wines of extraordinary depth and diversity. The region pioneered old-vine GSM blends in Australia and now leads the world in old-vine Grenache complexity.",
       key_producers="d'Arenberg, Clarendon Hills, Mitolo, Wirra Wirra, Yangarra Estate",
       historical_context="McLaren Vale's most significant viticultural heritage is its pre-phylloxera old-vine Grenache, Shiraz, and Mataro from the 19th century. These ancient vines, farmed on their original roots, produce wines of concentrated complexity that have increasingly attracted international recognition.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark McLaren Vale vintage — old-vine Grenache and Shiraz of extraordinary depth."),
    (2019,"very_good","stable","Good vintage despite heat; old-vine sites maintained excellent quality."),
    (2020,"challenging","stable","Bushfire concerns but McLaren Vale largely spared; quality wines produced."),
    (2021,"excellent","rising","Outstanding conditions; Grenache and GSM blends of benchmark quality."),
    (2022,"very_good","stable","Warm Mediterranean conditions yielded rich, opulent Shiraz and concentrated Grenache."),
    (2023,"excellent","rising","Exceptional vintage; old-vine Grenache producing wines rivalling the Rhône's finest."),
]:
    VIN(r2, yr, qd, pt, sn)

p3 = P("Yangarra Estate McLaren Vale", "winery", r2, "Australia",
       production_philosophy="biodynamic",
       philosophy_description="Yangarra Estate is McLaren Vale's leading organic and biodynamic producer, farming 80-year-old Grenache, Shiraz, and Mourvèdre vines on ancient ironstone and sandy loam soils. Winemaker Peter Fraser's focus on old-vine Grenache has produced some of Australia's most celebrated single-vineyard expressions.",
       reputation_narrative="Yangarra's Old Vine Grenache is considered Australia's finest expression of this variety — complex, perfumed, and rivalling great Châteauneuf-du-Pape in style and substance. Their biodynamic viticulture has also inspired a wider sustainability movement in the region.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Yangarra Old Vine Grenache McLaren Vale", "wine_still", p3, r2, "Australia",
                    subcategory="red", description="Old-vine Grenache from 80-year-old vines on ironstone soils — Australia's most acclaimed Grenache. Intensely perfumed: red cherry, raspberry, dried flowers, garrigue, and the distinctive ironstone mineral character. Silky tannins and extraordinary length.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Slow-roasted lamb shoulder with herbs de Provence", "complement", "classic", "main", "Old-vine Grenache's garrigue and red fruit mirror the herb crust; the wine's elegance lifts the slow-cooked lamb.")
    PAIR(prod, "Roasted beet and goat cheese salad with walnut", "complement", "established", "starter", "The wine's red fruit and floral notes complement beet's earthiness; goat cheese's tang bridges the Grenache's fruit.")
    PAIR(prod, "Grilled quail with lavender honey and thyme", "complement", "established", "main", "Perfumed Grenache and lavender honey share floral complexity; thyme echoes the wine's garrigue notes.")
    PAIR(prod, "Dark chocolate with raspberry and violet", "complement", "adventurous", "dessert", "The wine's violet and raspberry notes mirror chocolate's dark fruit; the irony structure bridges bitter chocolate.")
prod, is_new = PROD("Yangarra High Sands Grenache McLaren Vale", "wine_still", p3, r2, "Australia",
                    subcategory="red", description="Single-vineyard Grenache from ancient sand over limestone — the 'High Sands' site produces an even more perfumed, ethereal style. Dried rose, wild strawberry, anise, white pepper, and incredible finesse from the sandy terroir.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roasted salmon with Mediterranean herbs and lemon", "complement", "adventurous", "main", "The ethereal elegance of High Sands Grenache crosses the red wine-fish boundary with rich salmon beautifully.")
    PAIR(prod, "Mushroom and hazelnut risotto with truffle oil", "bridge", "established", "main", "The wine's wild herb and white pepper notes bridge to mushroom earthiness; hazelnut echoes the wine's finesse.")
    PAIR(prod, "Aged sheep's milk cheese with fig and walnut", "complement", "established", "cheese", "Ethereal Grenache's dried rose and strawberry complement aged sheep's milk; fig bridges the wine's floral notes.")
    PAIR(prod, "Grilled pigeon breast with cherry jus and lavender", "complement", "classic", "main", "Delicate High Sands Grenache matches pigeon's subtle gaminess; cherry and lavender echo the wine's aromatics.")

# === MARTINBOROUGH WINE REGION ===
print("=== Martinborough Wine Region ===")
r3 = R("Martinborough Wine Region", "New Zealand", "wine",
       designation_type="region",
       designation_name="Martinborough Wine Region",
       reputation_tier="prestigious",
       quality_trajectory="established",
       description="Martinborough, at the southern tip of New Zealand's North Island, pioneered fine Pinot Noir in New Zealand and remains one of the country's most distinctive wine terroirs. The Martinborough Terrace — a raised gravel terrace from the ancient Ruamahanga River — provides exceptional free-draining conditions, and the region's dry, continental climate (rare for NZ) concentrates flavours and intensifies colour. Ata Rangi, Dry River, and Palliser Estate have produced Pinot Noir of international reference quality since the 1980s.",
       key_producers="Ata Rangi, Dry River, Palliser Estate, Te Kairanga, Escarpment",
       historical_context="Martinborough was identified as a potential fine wine region by Neil McCallum (Dry River) and Clive Paton (Ata Rangi) in the early 1980s. The Martinborough Terrace's similarity to Burgundy soils inspired the founding vision, and the region's subsequent Pinot Noir success has validated that early assessment entirely.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","A benchmark Martinborough vintage — Pinot Noir of unusual depth and freshness."),
    (2020,"very_good","stable","Fine conditions; Martinborough Pinot showing typical elegance with good concentration."),
    (2021,"excellent","rising","Outstanding North Island vintage — Pinot of extraordinary complexity and structure."),
    (2022,"very_good","stable","Good ripeness; more accessible style of Pinot Noir with soft tannins and generous fruit."),
    (2023,"excellent","rising","Exceptional vintage widely regarded as the finest in recent Martinborough history."),
]:
    VIN(r3, yr, qd, pt, sn)

p4 = P("Ata Rangi Vineyard", "winery", r3, "New Zealand",
       production_philosophy="organic",
       philosophy_description="Ata Rangi ('new beginning/dawn') was founded in 1980 by Clive and Phyll Paton on the Martinborough Terrace. Their Pinot Noir is considered New Zealand's finest, consistently earning international accolades. The estate has been certified organic since 2012.",
       reputation_narrative="Ata Rangi Pinot Noir is New Zealand's most internationally celebrated red wine — a consistent benchmark that has defined Martinborough's style and raised the profile of New Zealand Pinot Noir on the world stage. The Célèbre red blend is equally acclaimed.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Ata Rangi Pinot Noir Martinborough", "wine_still", p4, r3, "New Zealand",
                    subcategory="red", description="New Zealand's benchmark Pinot Noir from the gravelly Martinborough Terrace. Deep cherry colour, perfumed and complex — dark cherry, spice, violet, earth, and silky tannins with the minerality unique to these ancient gravels. Requires 5+ years for full expression.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Roast duck with cherry and star anise", "complement", "classic", "main", "Dark cherry and spice in the wine echo the cherry-star anise preparation; duck's richness balances the Pinot's elegance.")
    PAIR(prod, "Braised lamb shoulder with flageolet beans and thyme", "complement", "classic", "main", "The wine's earthy-spice complexity suits slow-braised lamb; flageolet beans echo the wine's mineral depth.")
    PAIR(prod, "Wild mushroom and truffle tart with gruyère", "bridge", "established", "main", "Earthy Martinborough mineral notes bridge to truffle and mushroom; Gruyère's nuttiness complements Pinot's complexity.")
    PAIR(prod, "Central Otago salmon with lentils and caper vinaigrette", "complement", "established", "main", "New Zealand salmon meets New Zealand's finest Pinot — mineral acidity bridges to the salmon's richness perfectly.")

p5 = P("Dry River Wines Martinborough", "winery", r3, "New Zealand",
       production_philosophy="minimal_intervention",
       philosophy_description="Founded by scientist Neil McCallum, Dry River produces tiny quantities of wine (less than 3000 cases per year) that are immediately allocated on release. Their Pinot Noir, Pinot Gris, and Gewürztraminer are New Zealand's most cult wines — obsessively detailed and deeply complex.",
       reputation_narrative="Dry River is New Zealand's most sought-after producer — releases sell out instantly to a mailing list. Neil McCallum's scientific precision and obsessive quality focus produced wines that have proven to age magnificently for 20+ years.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Dry River Pinot Gris Martinborough", "wine_still", p5, r3, "New Zealand",
                    subcategory="white", description="One of the world's great Pinot Gris — rich, textured, off-dry style with pear, quince, ginger, and spice complexity. More Alsatian than Antipodean in weight and character, showing the Martinborough Terrace's rare ability to produce age-worthy whites of world class.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Cured salmon gravlax with dill cream cheese", "complement", "classic", "starter", "Pinot Gris's stone fruit and spice complement salmon's richness; dill bridges the wine's herbal aromatic.")
    PAIR(prod, "Seared duck liver with quince paste and brioche", "complement", "classic", "starter", "Rich Pinot Gris matches liver's intensity; quince echoes the wine's pear and quince character.")
    PAIR(prod, "Aged gouda with pear and walnuts", "complement", "established", "cheese", "Pear and quince in the wine mirror the fruit accompaniment; aged Gouda's caramel echoes Pinot Gris's richness.")
    PAIR(prod, "Spiced pork belly with plum sauce and bao bun", "complement", "adventurous", "main", "Rich Pinot Gris handles pork belly's richness; spice notes bridge the Asian-influenced preparation.")

# === HAWKE'S BAY GI ===
print("=== Hawke's Bay GI ===")
r4 = R("Hawke's Bay GI", "New Zealand", "wine",
       designation_type="GI",
       designation_name="Hawke's Bay Geographic Indication",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Hawke's Bay on New Zealand's North Island east coast is the country's warmest and sunniest wine region, making it NZ's home for the most full-bodied reds. The Gimblett Gravels — a unique warm, free-draining shingle bed — is New Zealand's most prestigious sub-region for Syrah, Merlot, and Cabernet Sauvignon. The gravels' heat retention produces ripe, complex reds reminiscent of the Northern Rhône and Bordeaux. Chardonnay from cooler Bridge Pa Triangle is also world class.",
       key_producers="Craggy Range, Trinity Hill, Te Mata Estate, Unison Vineyard, Elephant Hill",
       historical_context="Hawke's Bay is New Zealand's second-oldest wine region, established in the 1850s by Christian Brothers at Mission Estate. The Gimblett Gravels' unique terroir was identified in the 1980s and is now New Zealand's most famous wine sub-region — a warm shingle bed deposited by the Ngaruroro River that was bulldozed for gravel in the 1980s and converted to vineyards instead.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark Hawke's Bay vintage — Gimblett Gravels Syrah of extraordinary concentration."),
    (2019,"excellent","rising","Outstanding conditions; Merlot-based blends and Syrah achieving international recognition."),
    (2020,"very_good","stable","Fine vintage; Chardonnay and Syrah both excellent across the region."),
    (2021,"excellent","rising","One of the finest Hawke's Bay vintages in recent history for all varieties."),
    (2022,"very_good","stable","Warm conditions; generous Syrah and Merlot with opulent fruit and ripe tannins."),
    (2023,"excellent","rising","Exceptional year for Gimblett Gravels Syrah — some calling it the vintage of the decade."),
]:
    VIN(r4, yr, qd, pt, sn)

p6 = P("Craggy Range Winery", "winery", r4, "New Zealand",
       production_philosophy="terroir_expression",
       philosophy_description="Craggy Range produces single-vineyard wines from Hawke's Bay and Marlborough using a terroir-first approach. Their Le Sol Syrah from the Gimblett Gravels is widely regarded as New Zealand's greatest Syrah, and the 'Sophia' Merlot blend is a benchmark for Hawke's Bay Bordeaux varieties.",
       reputation_narrative="Craggy Range has elevated Hawke's Bay's international profile through their Gimblett Gravels Syrah and Merlot wines. Le Sol Syrah, in particular, has proven that New Zealand can produce world-class Syrah that competes with the Northern Rhône's finest.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Craggy Range Le Sol Syrah Hawke's Bay", "wine_still", p6, r4, "New Zealand",
                    subcategory="red", description="New Zealand's most celebrated Syrah from the warm Gimblett Gravels shingle. Intense, Northern Rhône-inspired — dark cherry, black olive, smoked meat, violet, white pepper, and iron-mineral structure. Requires 8+ years ageing for full complexity.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled Canterbury lamb rack with olive tapenade", "complement", "classic", "main", "NZ Syrah and NZ lamb is a natural national pairing — dark fruit and pepper complement lamb's mineral sweetness.")
    PAIR(prod, "Wild venison haunch with roasted root vegetables", "complement", "established", "main", "Syrah's iron and dark fruit handle venison's gaminess; roasted roots echo the wine's earthy mineral depth.")
    PAIR(prod, "Duck confit with black olive and lentils du Puy", "complement", "classic", "main", "Olive notes in the wine bridge to the duck confit's richness; lentils mirror the Syrah's earthy mineral character.")
    PAIR(prod, "Aged hard sheep's milk cheese with dark chocolate", "complement", "adventurous", "cheese", "Iron and dark fruit in the wine bridge to aged sheep's cheese's intensity; dark chocolate deepens the connection.")
prod, is_new = PROD("Craggy Range Gimblett Gravels Merlot Blend Hawke's Bay", "wine_still", p6, r4, "New Zealand",
                    subcategory="red", description="'Sophia' — Merlot-dominated blend from the Gimblett Gravels with Cabernet Franc and Malbec. Rich, silky, and Pomerol-inspired: plum, dark cherry, mocha, cedar, and velvety tannins from the gravel warmth. NZ's most Bordeaux-like red.", price_tier="premium")
if is_new:
    PAIR(prod, "Braised short rib with mushrooms and port reduction", "complement", "classic", "main", "Plum and mocha notes in the Merlot blend echo the port reduction; collagen-rich rib meets the wine's silky tannins.")
    PAIR(prod, "Lamb rump with herb crust and flageolet beans", "complement", "established", "main", "Velvety Merlot tannins complement herb-crusted lamb; flageolet beans echo the wine's earthy depth.")
    PAIR(prod, "Beef fillet with truffle butter and wilted spinach", "complement", "classic", "main", "The wine's silky structure matches beef tenderloin's delicacy; truffle butter bridges the Merlot's oak complexity.")
    PAIR(prod, "Époisses washed rind with walnut bread", "complement", "established", "cheese", "Rich, washed rind needs structured Merlot — the wine's plum fruit softens the cheese's pungency.")

# === WÜRTTEMBERG QbA ===
print("=== Württemberg QbA ===")
r5 = R("Württemberg QbA", "Germany", "wine",
       designation_type="QbA",
       designation_name="Württemberg Qualitätswein bestimmter Anbaugebiete",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Württemberg in southwest Germany is the country's most important red wine region, historically famous for the indigenous Trollinger grape but now producing exciting Lemberger (Blaufränkisch), Spätburgunder, and Merlot from a new generation of quality-focused estates. The Remstaler region around Stuttgart and the Württemberg Unterland produce Germany's warmest red wines. The Limberger ('Lemberger' in German) grape reaches exceptional quality here, producing wines of dark fruit, spice, and structure unlike anything else in German viticulture.",
       key_producers="Weingut Graf von Neipperg, Weingut Schnaitmann, Weingut Aldinger, Jochen Beurer",
       historical_context="Württemberg has the highest per capita wine consumption in Germany — local Trollinger is drunk young from Besen (mobile taverns). The modern quality movement began in the 1990s when producers like Schnaitmann and Aldinger demonstrated that Württemberg could produce internationally competitive red wines from Lemberger and Spätburgunder.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark Württemberg vintage — Lemberger and Spätburgunder of unusual depth and concentration."),
    (2019,"very_good","stable","Good vintage; warm conditions suited Lemberger particularly well."),
    (2020,"excellent","rising","Outstanding red wine vintage; some of the region's finest Lemberger and Merlot in memory."),
    (2021,"very_good","stable","Cooler year produced more elegant, structured Spätburgunder with excellent ageing potential."),
    (2022,"excellent","rising","Very warm year; rich, opulent Lemberger with exceptional ripeness across the region."),
    (2023,"very_good","stable","Good vintage; quality-focused producers excelled with structured, age-worthy reds."),
]:
    VIN(r5, yr, qd, pt, sn)

p7 = P("Weingut Schnaitmann", "winery", r5, "Germany",
       production_philosophy="organic",
       philosophy_description="Rainer Schnaitmann is Württemberg's most celebrated winemaker, producing benchmark Lemberger, Spätburgunder, and white wines from organically farmed vineyards around Fellbach. His wines have transformed perceptions of what German red wine can achieve beyond Spätburgunder.",
       reputation_narrative="Schnaitmann's Lemberger Lämmler Grosses Gewächs has placed Württemberg on the serious German wine map — dark, spicy, and age-worthy, it demonstrates that Lemberger can rival Blaufränkisch from Burgenland in complexity and character.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Schnaitmann Lemberger Lämmler GG Württemberg", "wine_still", p7, r5, "Germany",
                    subcategory="red", description="Grosses Gewächs Lemberger from the Lämmler vineyard — Germany's most acclaimed Lemberger. Dark, spicy, and concentrated: black cherry, dark plum, pepper, earth, and firm tannins for extended ageing. Rivals the finest Austrian Blaufränkisch.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Wild boar ragù with pappardelle and parmesan", "complement", "classic", "main", "Dark, tannic Lemberger handles gamey wild boar's richness; pepper notes echo the wine's spice character.")
    PAIR(prod, "Swabian Maultaschen (pasta) in beef broth with herbs", "complement", "established", "main", "A regional pairing — Württemberg Lemberger GG with the region's most famous pasta is a local classic.")
    PAIR(prod, "Slow-roasted pork neck with sauerkraut and caraway", "complement", "classic", "main", "Dark fruit cuts through pork's richness; caraway echoes the wine's earthy pepper character.")
    PAIR(prod, "Aged Allgäuer Bergkäse (mountain cheese) with bread", "complement", "established", "cheese", "Southern German hard cheese with the region's finest red — earthiness bridges both; the wine's fruit softens the cheese.")
prod, is_new = PROD("Schnaitmann Simonroth Spätburgunder Württemberg", "wine_still", p7, r5, "Germany",
                    subcategory="red", description="Single-vineyard Spätburgunder from the Simonroth site — elegant and Burgundian in style. Red cherry, raspberry, soft earth, subtle oak, and fine tannins. Shows the warmer Württemberg conditions creating a richer, more generous Pinot Noir than the cool Pfalz.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted guinea fowl with mushroom and cream", "complement", "classic", "main", "Württemberg Spätburgunder's warmth suits this rich preparation; mushroom bridges the red fruit and earthy wine notes.")
    PAIR(prod, "Venison stew with juniper and cranberry", "complement", "established", "main", "The wine's fuller body handles venison's richness more than cool-climate Pinot; juniper echoes the wine's earthy depth.")
    PAIR(prod, "Brie de Meaux with red berry jam", "complement", "classic", "cheese", "Warmer-climate Spätburgunder and creamy brie — the wine's generous red fruit balances brie's rich fattiness.")
    PAIR(prod, "Sautéed calf's liver with onion and sage", "complement", "established", "main", "Württemberg's fuller Spätburgunder stands up to liver's intensity; sage bridges the wine's earthy complexity.")

# === DB STATE ===
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
print("B166 complete.")
cur.close()
conn.close()
