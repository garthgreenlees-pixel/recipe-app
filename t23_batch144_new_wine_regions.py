#!/usr/bin/env python3
"""B144 — Sonoma Coast AVA, Dry Creek Valley AVA, Alexander Valley AVA, Anderson Valley AVA, Lodi AVA"""
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

# ── 1. Sonoma Coast AVA ──────────────────────────────────────────────────────
print("=== Sonoma Coast AVA ===")
r1 = R("Sonoma Coast AVA", "USA", "wine",
        designation_type="AVA", designation_name="Sonoma Coast",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="One of California's most demanding appellations, Sonoma Coast stretches from the foggy Pacific coastline inland, producing Pinot Noir and Chardonnay of remarkable tension and complexity. The True Sonoma Coast sub-zone, pressed against the ocean, yields wines with singular mineral intensity.",
        key_producers="Hirsch Vineyards, Littorai, Peay Vineyards, Fort Ross-Seaview producers",
        historical_context="Defined as an AVA in 1987, Sonoma Coast's identity has sharpened around cool-climate sites near the ocean. The internal debate between 'true coast' and inland sites has driven viticultural precision and site selection to world-class standards.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "poor", "declining"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r1, yr, qd, pt)

p1a = P("Hirsch Vineyards", "winery", r1, "USA",
         production_philosophy="terroir_expression",
         philosophy_description="Family-owned estate on the True Sonoma Coast, farming biodynamically since 2014 at extreme elevations with direct Pacific influence. The Hirsch family's singular focus on their own vineyards defines one of California's most site-expressive Pinot Noirs.",
         reputation_narrative="David Hirsch's visionary identification of this remote coastal site in the 1980s has been validated by critics worldwide. Hirsch Estate Pinot Noir is among California's most collected and cellar-worthy wines.",
         price_positioning="ultra_premium")

prod1a1, new1 = PROD("Hirsch Vineyards Estate Pinot Noir Sonoma Coast", "wine_still", p1a, r1, "USA",
                      subcategory="Pinot Noir", price_tier="ultra_premium",
                      description="Grown at 1,200–1,700 feet on the extreme Sonoma Coast, this estate Pinot Noir delivers profound earth, wild strawberry, and sea-spray minerality. Fermented with indigenous yeasts in small open-top fermenters with extended maceration.")
if new1:
    PAIR(prod1a1, "Dungeness crab with brown butter and tarragon", "bridge", "classic", "fish_course", "The coastal salinity and red-fruit brightness of Hirsch Estate mirror the oceanic sweetness of Dungeness crab; brown butter bridges the wine's subtle oak spice.")
    PAIR(prod1a1, "Grilled wild king salmon with pinot noir reduction", "complement", "classic", "main", "A benchmark pairing: the wine's earthy depth and firm acidity complement wild salmon's rich oils while the pinot noir reduction creates a flavour continuum between plate and glass.")
    PAIR(prod1a1, "Duck breast with dried cherry and beet gastrique", "complement", "established", "main", "Hirsch's dried-fruit aromatics and iron-mineral finish echo the gastrique's sweet-sour tension while the wine's tannin structure cuts through duck fat.")
    PAIR(prod1a1, "Aged Humboldt Fog goat cheese with honeycomb", "bridge", "suggested", "cheese", "The wine's bright acidity and chalk-mineral character lifts the tangy creaminess of Humboldt Fog; honeycomb softens the contrast beautifully.")

prod1a2, new2 = PROD("Hirsch Vineyards San Andreas Fault Pinot Noir", "wine_still", p1a, r1, "USA",
                      subcategory="Pinot Noir", price_tier="ultra_premium",
                      description="Named for the San Andreas Fault running through the vineyard, this single-block wine from the fault-line soils delivers a more structured, age-worthy expression with dark fruit and profound mineral tension.")
if new2:
    PAIR(prod1a2, "Roasted venison loin with juniper berry jus", "complement", "established", "main", "The fault-line wine's darker fruit and firmer tannin structure finds its match in game meat's iron richness; juniper amplifies the wine's wild herbal character.")
    PAIR(prod1a2, "Black truffle and mushroom risotto", "complement", "classic", "main", "The earthy, mineral depth of this Pinot Noir resonates profoundly with truffle and porcini; the wine's acidity keeps the rich risotto from feeling heavy.")
    PAIR(prod1a2, "Roasted beet salad with walnut and aged balsamic", "bridge", "suggested", "starter", "The wine's iron-minerality and dark-fruit depth harmonise with roasted beet's earthiness; walnut adds textural richness that matches the wine's structure.")
    PAIR(prod1a2, "Lamb tartare with capers and preserved lemon", "contrast", "adventurous", "starter", "The wine's coastal salinity and bright acidity cut through raw lamb's richness; capers and preserved lemon amplify the contrast creating a vivid interplay.")

p1b = P("Littorai Wines", "winery", r1, "USA",
         production_philosophy="terroir_expression",
         philosophy_description="Ted Lemon established Littorai in 1993 after a formative career in Burgundy, applying Burgundian viticultural rigour to California's coolest coastal sites. Biodynamic farming across multiple vineyard sources on the Sonoma and Mendocino coasts.",
         reputation_narrative="Littorai is widely regarded as one of California's benchmark Pinot Noir and Chardonnay producers, with Ted Lemon's Burgundian background giving his wines a precision and restraint rare in the New World.",
         price_positioning="ultra_premium")

prod1b1, new3 = PROD("Littorai The Pivot Pinot Noir Sonoma Coast", "wine_still", p1b, r1, "USA",
                      subcategory="Pinot Noir", price_tier="ultra_premium",
                      description="From a single vineyard on the True Sonoma Coast, The Pivot displays the hallmark Littorai style: tensile acidity, translucent red fruit, and a long mineral finish that rewards patience in the cellar.")
if new3:
    PAIR(prod1b1, "Roasted squab with black garlic and thyme jus", "complement", "classic", "main", "Squab's gamey richness and umami depth call for a Pinot of this calibre; the wine's silk tannin and bright acidity cut through richness while complementing the dark-fruit notes.")
    PAIR(prod1b1, "Seared foie gras with cherry compote", "contrast", "adventurous", "starter", "Littorai's acidity and iron-mineral finish cut the unctuous fat of foie gras; the cherry compote harmonises with the wine's red-fruit core.")
    PAIR(prod1b1, "Poached halibut with wild mushroom velouté", "bridge", "established", "fish_course", "The wine's delicacy and savoury mineral character complement halibut's gentle sweetness; mushroom velouté deepens the earthy resonance between food and wine.")
    PAIR(prod1b1, "Époisses de Bourgogne with walnuts", "complement", "suggested", "cheese", "The wine's coastal terroir and firm acidity balance the pungent, washed-rind intensity of Époisses; walnuts add a bitter note that prolongs the finish.")

prod1b2, new4 = PROD("Littorai Mays Canyon Chardonnay Sonoma Coast", "wine_still", p1b, r1, "USA",
                      subcategory="Chardonnay", price_tier="ultra_premium",
                      description="A cool-climate Chardonnay of extraordinary precision from the Mays Canyon site, vinified with wild fermentation in French oak (30% new). The wine's citrus-mineral purity and saline finish are distinctively Littorai.")
if new4:
    PAIR(prod1b2, "Line-caught halibut with Meyer lemon beurre blanc", "complement", "classic", "fish_course", "The wine's citrus acidity and subtle oak spice mirror the beurre blanc's richness and lemon brightness; both share a saline coastal quality.")
    PAIR(prod1b2, "Sea urchin with yuzu crème fraîche on brioche", "bridge", "established", "starter", "Uni's briny sweetness finds a perfect counterpart in the wine's saline mineral finish; yuzu mirrors the wine's citrus notes while crème fraîche softens the acidity.")
    PAIR(prod1b2, "White asparagus with hollandaise and bottarga", "complement", "suggested", "starter", "The wine's precise acidity and creamy texture balance hollandaise's richness; bottarga's umami salinity amplifies the wine's ocean-derived mineral character.")
    PAIR(prod1b2, "Aged Gruyère with apple and fennel", "complement", "established", "cheese", "Gruyère's nutty complexity and long finish resonate with the wine's subtle oak and hazelnut notes; apple and fennel echo the wine's green-apple freshness.")

# ── 2. Dry Creek Valley AVA ──────────────────────────────────────────────────
print("=== Dry Creek Valley AVA ===")
r2 = R("Dry Creek Valley AVA", "USA", "wine",
        designation_type="AVA", designation_name="Dry Creek Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="One of Sonoma County's most distinctive appellations, Dry Creek Valley is a narrow valley hemmed by steep ridges that create a warm, dry microclimate ideal for Zinfandel and Cabernet Sauvignon. The valley's benchland soils and diurnal temperature swings produce wines of exceptional concentration and balance.",
        key_producers="Ridge Vineyards (Lytton Springs), Quivira Vineyards, Preston Farm & Winery, A. Rafanelli Winery",
        historical_context="Settled by Italian immigrants who planted Zinfandel in the late 19th century, Dry Creek Valley was granted AVA status in 1983. It remains California's spiritual home of old-vine Zinfandel, with some vines exceeding 100 years of age.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Ridge Vineyards Lytton Springs", "winery", r2, "USA",
         production_philosophy="minimal_intervention",
         philosophy_description="Ridge's Lytton Springs property in Dry Creek Valley houses some of California's most celebrated old-vine Zinfandel. The team practices dry farming and picks at optimal physiological maturity, vinifying with native yeasts and aging in American oak.",
         reputation_narrative="Lytton Springs is one of Ridge's crown jewels, producing Zinfandel-dominant blends of remarkable complexity and age-worthiness that challenge European benchmarks for the variety.",
         price_positioning="premium")

prod2a1, new5 = PROD("Ridge Lytton Springs Dry Creek Valley", "wine_still", p2a, r2, "USA",
                      subcategory="Zinfandel", price_tier="premium",
                      description="A blend of old-vine Zinfandel with Petite Sirah and Carignane from the Lytton Springs estate. Full-bodied yet structured, with black cherry, bramble, and leather, finishing with Ridge's signature American oak complexity.")
if new5:
    PAIR(prod2a1, "Slow-smoked beef brisket with chipotle barbecue sauce", "complement", "classic", "main", "The wine's bold bramble fruit and smoky American oak character are a natural companion to smoked brisket; the chipotle heat amplifies the wine's spice without overwhelming its fruit.")
    PAIR(prod2a1, "Lamb merguez sausage with harissa and flatbread", "complement", "established", "main", "Merguez spice and harissa heat find traction against the wine's juicy fruit and medium tannin; the flatbread absorbs the intensity, keeping the pairing balanced.")
    PAIR(prod2a1, "Aged cheddar with fig preserves and walnuts", "bridge", "classic", "cheese", "Ridge's rich fruit and oak spice harmonise with aged cheddar's sharpness; fig preserves echo the wine's dried-fruit character while walnuts add welcome bitterness.")
    PAIR(prod2a1, "Duck confit with pomegranate molasses and pistachios", "complement", "established", "main", "Duck confit's rendered fat and pomegranate's tartness call for the wine's acidity and fruit weight; pistachios bring a savoury richness that mirrors the wine's complexity.")

prod2a2, new6 = PROD("Ridge Lytton Springs Old Vine Zinfandel Dry Creek", "wine_still", p2a, r2, "USA",
                      subcategory="Zinfandel", price_tier="premium",
                      description="From the oldest blocks at Lytton Springs, this single-varietal bottling showcases the concentrated complexity achievable with centenarian Zinfandel vines — deeper, more structured, and more age-worthy than the estate blend.")
if new6:
    PAIR(prod2a2, "Braised short rib with red wine reduction and horseradish gremolata", "complement", "classic", "main", "The wine's power and structure demand an equally robust preparation; short rib's collagen richness and the reduction's acidity create a seamless pairing.")
    PAIR(prod2a2, "Grilled portobello with aged balsamic and truffle oil", "complement", "established", "main", "The wine's dark fruit and earthy depth resonate with portobello's umami; balsamic bridges the acidity while truffle oil adds the luxury element the wine's concentration demands.")
    PAIR(prod2a2, "Wild boar ragù with pappardelle", "complement", "classic", "main", "Old-vine Zinfandel's animal, spice-driven character is a natural match for game ragù; pappardelle's width holds the sauce's weight, keeping the pairing in proportion.")
    PAIR(prod2a2, "Dark chocolate and dried cherry bark with sea salt", "complement", "adventurous", "dessert", "The wine's dried-cherry depth and spice resonate with dark chocolate; sea salt amplifies both the wine's fruit and the chocolate's intensity in a classic contrast.")

p2b = P("Quivira Vineyards", "winery", r2, "USA",
         production_philosophy="sustainable",
         philosophy_description="Quivira farms biodynamically in Dry Creek Valley, producing old-vine Zinfandel and Rhône varieties with a strong commitment to biodiversity and minimal intervention. One of Sonoma's pioneering biodynamic estates.",
         reputation_narrative="Quivira is a respected voice for biodynamic viticulture in California, producing wines that express the valley's character with freshness and restraint unusual for Dry Creek Zinfandel.",
         price_positioning="mid_range")

prod2b1, new7 = PROD("Quivira Dry Creek Cuvée Zinfandel", "wine_still", p2b, r2, "USA",
                      subcategory="Zinfandel", price_tier="mid_range",
                      description="Biodynamically farmed old-vine Zinfandel from Dry Creek Valley, displaying the Quivira hallmark of freshness and balanced alcohol alongside the variety's characteristic brambly fruit and spice.")
if new7:
    PAIR(prod2b1, "Pork ribs with honey-mustard glaze and coleslaw", "complement", "classic", "main", "The wine's juicy bramble fruit and lively acidity cut through pork's sweet-fatty richness; mustard's tang amplifies the wine's spice character.")
    PAIR(prod2b1, "Charcuterie board with salami, olives, and pickled peppers", "bridge", "established", "casual", "The wine's red-fruit brightness and subtle tannin navigate the charcuterie board's varied saltiness and acidity; pickled peppers echo the wine's natural zip.")
    PAIR(prod2b1, "Grilled eggplant with tahini and pomegranate seeds", "complement", "suggested", "main", "Biodynamic Zinfandel's earthiness and fruit complement eggplant's smoky depth; tahini's creaminess buffers the acidity while pomegranate mirrors the wine's tartness.")
    PAIR(prod2b1, "Manchego with quince paste and marcona almonds", "bridge", "established", "cheese", "The wine's fruit and gentle spice find a harmonious match in manchego's sheep-milk nuttiness; quince paste bridges both while almonds add savoury depth.")

prod2b2, new8 = PROD("Quivira Benchmark Zinfandel Dry Creek Valley", "wine_still", p2b, r2, "USA",
                      subcategory="Zinfandel", price_tier="mid_range",
                      description="Quivira's reserve-level offering, from the oldest biodynamic vines on the estate. More concentrated and structured than the Dry Creek Cuvée, with greater depth of fruit and a longer, more mineral finish.")
if new8:
    PAIR(prod2b2, "Lamb shank braised with tomatoes and olives", "complement", "established", "main", "The wine's depth and tannin structure stand up to long-braised lamb; olives and tomatoes provide the acidity that keeps the pairing lively.")
    PAIR(prod2b2, "Grilled Italian sausage with roasted peppers", "complement", "classic", "main", "The wine's brambly spice and fruit weight match sausage's fennel and herb character; roasted peppers add sweetness that bridges meat and wine.")
    PAIR(prod2b2, "Aged Pecorino Toscano with truffle honey", "complement", "suggested", "cheese", "Pecorino's sharpness and truffle honey's earthiness resonate with the wine's old-vine complexity; the combination elongates the finish on both sides.")
    PAIR(prod2b2, "Beef and mushroom empanadas with chimichurri", "complement", "adventurous", "casual", "The wine's old-vine concentration and structure match the empanada's rich beef filling; chimichurri's herbaceous acidity keeps the pairing fresh.")

# ── 3. Alexander Valley AVA ──────────────────────────────────────────────────
print("=== Alexander Valley AVA ===")
r3 = R("Alexander Valley AVA", "USA", "wine",
        designation_type="AVA", designation_name="Alexander Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Alexander Valley, at the northern end of Sonoma County, is renowned for full-bodied Cabernet Sauvignon and Chardonnay of uncommon richness and approachability. The valley's warm days and cool nights, tempered by the Russian River, produce wines with generous fruit and supple tannins.",
        key_producers="Jordan Vineyard & Winery, Silver Oak Cellars, Stonestreet Estate, Clos du Bois",
        historical_context="Named after Cyrus Alexander, a settler who planted grapes in the 1840s, Alexander Valley was granted AVA status in 1984. It found its modern identity through Cabernet Sauvignon of Bordeaux inspiration, with Jordan and Silver Oak defining the style for generations of collectors.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"), (2023, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Jordan Vineyard & Winery", "winery", r3, "USA",
         production_philosophy="classical",
         philosophy_description="Jordan was established in 1972 with a singular mission: to produce a Sonoma Cabernet Sauvignon and Chardonnay in the classic European tradition. The estate's French-château aesthetic extends to the winery's hospitality and the wines' balance-driven philosophy.",
         reputation_narrative="Jordan has maintained consistent excellence for five decades, producing some of California's most food-friendly and age-worthy Cabernet Sauvignons. Its approachable style and reliable quality have made it a benchmark for Alexander Valley.",
         price_positioning="premium")

prod3a1, new9 = PROD("Jordan Cabernet Sauvignon Alexander Valley", "wine_still", p3a, r3, "USA",
                      subcategory="Cabernet Sauvignon", price_tier="premium",
                      description="A Bordeaux-inspired blend led by Cabernet Sauvignon, aged in French and American oak. Jordan's Alexander Valley Cab is known for its elegance, balance, and remarkable food-friendliness — wines that drink well on release yet reward a decade of cellaring.")
if new9:
    PAIR(prod3a1, "Roasted prime rib with au jus and Yorkshire pudding", "complement", "classic", "main", "A quintessential pairing: the wine's structured tannin and cassis fruit complement prime rib's marbled richness while the au jus bridges the savoury depth between plate and glass.")
    PAIR(prod3a1, "Rack of lamb with Dijon crust and red wine reduction", "complement", "classic", "main", "Jordan's Bordeaux character makes it a natural match for lamb; the Dijon crust's mustard spice complements the wine's herbal notes while the reduction deepens the connection.")
    PAIR(prod3a1, "Aged cheddar and Gruyère cheese board with Marcona almonds", "bridge", "established", "cheese", "The wine's cassis and cedar note harmonise with aged cheese complexity; almonds provide a savoury foil that extends the wine's finish.")
    PAIR(prod3a1, "Beef tenderloin with truffle butter and roasted garlic", "complement", "classic", "main", "Tenderloin's lean luxury and truffle butter's richness meet the wine's elegant tannin structure; roasted garlic adds the savoury depth that keeps the pairing grounded.")

prod3a2, new10 = PROD("Jordan Chardonnay Russian River Valley", "wine_still", p3a, r3, "USA",
                       subcategory="Chardonnay", price_tier="premium",
                       description="From Russian River Valley fruit, Jordan's Chardonnay is fermented in French oak with partial malolactic fermentation to preserve freshness. It displays ripe apple, pear, and toasty oak in a generous style that remains food-friendly.")
if new10:
    PAIR(prod3a2, "Lobster bisque with crème fraîche and chives", "complement", "classic", "starter", "The wine's creamy texture and ripe fruit match lobster bisque's richness; its acidity keeps the soup from feeling heavy while the oak adds a complementary toasted note.")
    PAIR(prod3a2, "Roasted chicken with tarragon and lemon butter", "complement", "classic", "main", "Jordan Chardonnay's generous fruit and balanced oak are ideally suited to roasted chicken; tarragon's anise note and lemon butter's acidity mirror the wine's freshness.")
    PAIR(prod3a2, "Corn bisque with smoked bacon and chipotle crema", "bridge", "established", "starter", "The wine's ripe apple and subtle oak echo the bisque's sweet corn character; smoked bacon adds the savoury contrast while chipotle's heat is buffered by the wine's fruit weight.")
    PAIR(prod3a2, "Brie en croûte with honey and toasted pecans", "complement", "established", "cheese", "The wine's creamy texture and toasty oak harmonise with warm brie; honey bridges the wine's ripe fruit while pecans add a savoury-bitter balance.")

p3b = P("Silver Oak Cellars Alexander Valley", "winery", r3, "USA",
         production_philosophy="classical",
         philosophy_description="Silver Oak's Alexander Valley Cabernet Sauvignon is one of California's most recognised labels, aged exclusively in American oak for a signature vanilla and coconut character that has defined a style for over 50 years. Their motto: 'Life is a Cabernet.'",
         reputation_narrative="Silver Oak is a touchstone of American Cabernet culture, its Alexander Valley bottling delivering consistent, food-friendly luxury at a prestige price point that has broadened the market for California Cab.",
         price_positioning="premium")

prod3b1, new11 = PROD("Silver Oak Cabernet Sauvignon Alexander Valley", "wine_still", p3b, r3, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="premium",
                       description="Silver Oak's signature wine, aged for over two years in American oak and further bottle-aged before release. The result is a plush, approachable Cabernet with blackberry, vanilla, and sweet oak — drinking beautifully on release yet capable of decades of ageing.")
if new11:
    PAIR(prod3b1, "New York strip steak with compound butter and fries", "complement", "classic", "main", "Silver Oak's vanilla and blackberry character is the quintessential American steakhouse pairing; the butter's richness mirrors the wine's generous oak while the steak's sear complements its fruit.")
    PAIR(prod3b1, "Smoked gouda and cheddar with barbecue pork ribs", "complement", "established", "main", "The wine's American oak and sweet fruit character harmonises with barbecue's smoke and sweetness; melted smoked gouda adds a creamy, savoury bridge.")
    PAIR(prod3b1, "Chocolate lava cake with vanilla ice cream", "complement", "suggested", "dessert", "Silver Oak's vanilla oak character creates an unexpected resonance with chocolate lava cake; the wine's fruit and sweetness complement the dessert without clashing.")
    PAIR(prod3b1, "Aged Tillamook cheddar with dried fig and walnut bread", "bridge", "established", "cheese", "The wine's American-oak vanilla and blackberry complement aged cheddar's sharpness; dried fig echoes the wine's fruit while walnut bread adds savoury bitterness.")

prod3b2, new12 = PROD("Silver Oak Cabernet Sauvignon Napa Valley", "wine_still", p3b, r3, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                       description="Silver Oak's Napa Valley Cabernet, also aged in American oak, offers greater structure and intensity than the Alexander Valley bottling while retaining the house's signature approachability. Considered the more age-worthy of the two.")
if new12:
    PAIR(prod3b2, "Wagyu beef short rib with red wine demi and bone marrow", "complement", "classic", "main", "The Napa bottling's greater concentration and tannin structure demand a preparation of this luxury level; bone marrow's richness and the demi's depth create a profound pairing.")
    PAIR(prod3b2, "Roasted rack of lamb with olive tapenade and rosemary", "complement", "classic", "main", "The wine's Cabernet structure and cassis fruit are natural partners for lamb; tapenade's olive brine adds Mediterranean complexity that echoes the wine's herbal notes.")
    PAIR(prod3b2, "Double cream brie with truffle and wild mushroom crostini", "complement", "established", "cheese", "The wine's richness and structure match double cream brie; truffle and mushroom add the umami depth that the Napa bottling's weight demands.")
    PAIR(prod3b2, "Dark chocolate tart with sea salt and caramelised hazelnuts", "complement", "suggested", "dessert", "The wine's structure and concentration can handle dark chocolate's bitterness; sea salt amplifies both while hazelnuts echo the wine's oak-derived nut notes.")

# ── 4. Anderson Valley AVA ───────────────────────────────────────────────────
print("=== Anderson Valley AVA ===")
r4 = R("Anderson Valley AVA", "USA", "wine",
        designation_type="AVA", designation_name="Anderson Valley",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Anderson Valley in Mendocino County is one of California's most distinctive cool-climate appellations, producing world-class Pinot Noir, Chardonnay, and sparkling wine. The valley's proximity to the Pacific coast creates a foggy, mild climate with extreme diurnal temperature variation that preserves exceptional natural acidity.",
        key_producers="Roederer Estate, Littorai, Navarro Vineyards, Husch Vineyards, Londer Vineyards",
        historical_context="Anderson Valley's wine history dates to the 1960s, but its global reputation was established when Champagne Louis Roederer chose the valley for its California sparkling wine venture in 1982. The subsequent recognition of Pinot Noir quality has made it one of the West Coast's most exciting appellations.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "very_good", "stable"), (2023, "excellent", "rising")]:
    VIN(r4, yr, qd, pt)

p4a = P("Roederer Estate", "winery", r4, "USA",
         production_philosophy="classical",
         philosophy_description="The California venture of Champagne Louis Roederer, established in Anderson Valley in 1982. Roederer Estate applies traditional méthode champenoise to Anderson Valley grapes, producing sparkling wines that are benchmarks of American sparkling wine quality.",
         reputation_narrative="Roederer Estate's L'Ermitage and Brut are among California's most awarded sparkling wines, often cited alongside Champagne in quality comparisons. The estate's commitment to reserve wine blending and extended lees ageing sets the standard.",
         price_positioning="premium")

prod4a1, new13 = PROD("Roederer Estate L'Ermitage Anderson Valley", "wine_sparkling", p4a, r4, "USA",
                       subcategory="Blanc de Blancs", price_tier="premium",
                       description="Roederer Estate's prestige cuvée, made from the finest Anderson Valley Chardonnay with extended lees ageing. L'Ermitage delivers extraordinary complexity, with toasted brioche, white peach, and subtle oxidative depth that rivals Champagne at a fraction of the price.")
if new13:
    PAIR(prod4a1, "Oysters on the half shell with mignonette and lemon", "complement", "classic", "aperitif", "The wine's bright acidity, mineral depth, and fine bubbles are the archetypal oyster companion; mignonette's vinegar sharpens the wine's acidity while amplifying the oyster's brine.")
    PAIR(prod4a1, "Caviar with blinis and crème fraîche", "complement", "classic", "amuse", "A classic luxury pairing: L'Ermitage's autolytic complexity and fine mousse provide the ideal textural contrast to caviar; crème fraîche bridges the wine's acidity and the roe's salinity.")
    PAIR(prod4a1, "Dungeness crab cakes with lemon aioli and microgreens", "complement", "established", "starter", "The wine's citrus and toasted brioche complement the sweet crabmeat; lemon aioli mirrors the wine's acidity while providing the richness that the wine's extended lees character can absorb.")
    PAIR(prod4a1, "White truffle and Parmesan risotto", "complement", "established", "main", "The wine's oxidative depth and complex autolysis are a natural match for white truffle; Parmesan's umami and the risotto's creaminess support the wine's considerable weight.")

prod4a2, new14 = PROD("Roederer Estate Brut Anderson Valley", "wine_sparkling", p4a, r4, "USA",
                       subcategory="Brut", price_tier="mid_range",
                       description="The estate's entry-level sparkling, blending Chardonnay and Pinot Noir from Anderson Valley with reserve wines. Consistently delivers fresh apple, cream, and yeast character with a long, refreshing finish — one of California's best value sparkling wines.")
if new14:
    PAIR(prod4a2, "Fried chicken with honey-butter biscuits", "contrast", "established", "casual", "The wine's persistent bubbles and lively acidity cut through fried chicken's oil; honey-butter biscuits add sweetness that contrasts the wine's dryness in a playful, crowd-pleasing pairing.")
    PAIR(prod4a2, "Smoked salmon with cream cheese on pumpernickel", "complement", "classic", "aperitif", "The wine's apple and yeast character complement smoked salmon's richness and smoke; cream cheese adds fat that buffers the wine's acidity while pumpernickel adds earthy depth.")
    PAIR(prod4a2, "Prawn cocktail with Marie Rose sauce", "complement", "classic", "starter", "The wine's acidity and bubbles refresh the palate between bites of prawn; Marie Rose's sweet-spicy character bridges the wine's fruit and the seafood's brine.")
    PAIR(prod4a2, "Poached pear and Gorgonzola crostini with honey", "bridge", "suggested", "aperitif", "The wine's apple fruit and gentle sweetness find a harmonious partner in poached pear; Gorgonzola's sharpness is softened by honey, keeping the pairing elegant.")

p4b = P("Navarro Vineyards", "winery", r4, "USA",
         production_philosophy="minimal_intervention",
         philosophy_description="Navarro is Anderson Valley's pioneering estate winery, established in 1974 by Ted Bennett and Deborah Cahn. Their focus on Alsatian varieties — Gewurztraminer, Riesling, and Pinot Gris — alongside Pinot Noir has defined a distinctive Anderson Valley style.",
         reputation_narrative="Navarro is beloved for its exceptional Gewurztraminer and Pinot Noir, sold largely direct-to-consumer. The winery's integrity and consistent quality over five decades have made it a cult favourite among California wine lovers.",
         price_positioning="mid_range")

prod4b1, new15 = PROD("Navarro Gewurztraminer Anderson Valley", "wine_still", p4b, r4, "USA",
                       subcategory="Gewurztraminer", price_tier="mid_range",
                       description="Arguably California's finest Gewurztraminer, grown in Anderson Valley's cool climate where the variety can develop full aromatic complexity without losing freshness. Classic lychee, rose petal, and ginger with a long, slightly spicy finish and off-dry balance.")
if new15:
    PAIR(prod4b1, "Spicy Thai green curry with jasmine rice and crispy tofu", "complement", "classic", "main", "The wine's aromatic intensity, residual sugar, and acidity are the ideal tools to navigate green curry heat; lychee and ginger character mirrors the curry's own aromatics.")
    PAIR(prod4b1, "Peking duck with hoisin pancakes and cucumber", "complement", "classic", "main", "Gewurztraminer and duck is a benchmark pairing; the wine's lychee and spice mirror the hoisin's sweetness while its acidity cuts through the duck's rich skin.")
    PAIR(prod4b1, "Indian butter chicken with naan and raita", "complement", "established", "main", "The wine's off-dry richness and aromatic power bridge butter chicken's cream-tomato sauce and warming spice; raita's cool yogurt parallels the wine's refreshing acidity.")
    PAIR(prod4b1, "Épices Alsatian cheese board with Munster and caraway", "complement", "classic", "cheese", "A classic regional pairing: Gewurztraminer's spice and rose petal lift the pungent Munster; caraway seeds echo the wine's own spice character in this quintessential Alsatian combination.")

prod4b2, new16 = PROD("Navarro Pinot Noir Anderson Valley", "wine_still", p4b, r4, "USA",
                       subcategory="Pinot Noir", price_tier="mid_range",
                       description="A benchmark Anderson Valley Pinot Noir from Navarro's estate vineyards, displaying the cool-climate character of the appellation: vibrant red cherry, forest floor, and a silky texture with remarkable natural acidity.")
if new16:
    PAIR(prod4b2, "Roasted salmon with pinot noir butter and herb crust", "complement", "classic", "main", "Anderson Valley Pinot and salmon is a West Coast benchmark; the butter sauce bridges the wine's red fruit and the fish's richness while the herb crust echoes the wine's forest-floor character.")
    PAIR(prod4b2, "Mushroom and fontina pizza with fresh thyme", "complement", "established", "casual", "The wine's earthy, red-fruit character resonates with mushroom's umami; fontina melts into a creamy base that the wine's acidity can cut through with ease.")
    PAIR(prod4b2, "Duck leg confit with lentils and lardon", "complement", "established", "main", "Duck confit's richness and lentils' earthiness demand the wine's silky tannin and bright acidity; lardon adds smoky depth that amplifies the wine's secondary character.")
    PAIR(prod4b2, "Comté with black cherry compote and chestnut bread", "complement", "established", "cheese", "The wine's cherry and forest-floor notes resonate with aged Comté's complexity; black cherry compote mirrors the wine's fruit while chestnut bread grounds the pairing.")

# ── 5. Lodi AVA ─────────────────────────────────────────────────────────────
print("=== Lodi AVA ===")
r5 = R("Lodi AVA", "USA", "wine",
        designation_type="AVA", designation_name="Lodi",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Lodi, in California's Central Valley, is home to some of the world's oldest surviving Zinfandel vines — centenarian head-trained bush vines that produce wines of remarkable concentration and character. The region's Mediterranean climate produces generous, fruit-forward wines at exceptional value.",
        key_producers="Turley Wine Cellars (Lodi), Michael David Winery, Jessie's Grove Winery, Lucas Winery",
        historical_context="Lodi's winemaking history stretches back to the 19th-century Italian immigrants who planted Zinfandel head-trained vines, many of which still produce today. The region's reputation was long overshadowed by its role as a bulk wine producer, but a quality revolution beginning in the 1990s has revealed Lodi's world-class old-vine potential.")

for yr, qd, pt in [
    (2019, "excellent", "stable"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r5, yr, qd, pt)

p5a = P("Turley Wine Cellars", "winery", r5, "USA",
         production_philosophy="terroir_expression",
         philosophy_description="Larry Turley is the champion of California's old-vine Zinfandel, sourcing from centenarian vineyards across Lodi, Napa, and Paso Robles. His commitment to dry farming and minimal intervention captures the full expressive potential of each site's ancient vines.",
         reputation_narrative="Turley is revered as the definitive voice of California Zinfandel, with wines that challenge perceptions of the variety's depth and age-worthiness. The Lodi old-vine bottlings are consistently among the region's most celebrated wines.",
         price_positioning="premium")

prod5a1, new17 = PROD("Turley Old Vines Zinfandel Lodi", "wine_still", p5a, r5, "USA",
                       subcategory="Zinfandel", price_tier="premium",
                       description="Sourced from ancient head-trained Zinfandel vines in Lodi, some approaching 130 years of age. The wine displays the old-vine hallmarks: concentrated black fruit, earth, spice, and surprising freshness, with structure to age a decade or more.")
if new17:
    PAIR(prod5a1, "Braised oxtail with polenta and gremolata", "complement", "classic", "main", "Old-vine Zinfandel's depth and spice are perfectly calibrated for oxtail's collagen richness; polenta absorbs the sauce while gremolata's citrus lifts the wine's dark fruit.")
    PAIR(prod5a1, "Smoked brisket with black bean chili and cornbread", "complement", "established", "main", "The wine's concentration and earthy depth meet smoked brisket's intensity; chili heat amplifies the wine's spice while cornbread provides the starchy relief the pairing needs.")
    PAIR(prod5a1, "Roasted leg of lamb with garlic and rosemary", "complement", "classic", "main", "Old-vine Zin's dried-fruit depth and robust tannin provide the ideal framework for lamb; rosemary echoes the wine's herbal character while garlic deepens the savoury connection.")
    PAIR(prod5a1, "Aged Grana Padano with soppressata and dried cherries", "bridge", "established", "cheese", "The wine's old-vine concentration and spice bridge Italian charcuterie's salty pungency and cheese's crystalline depth; dried cherries mirror the wine's fruit character.")

prod5a2, new18 = PROD("Turley Kirschenmann Vineyard Zinfandel Lodi", "wine_still", p5a, r5, "USA",
                       subcategory="Zinfandel", price_tier="premium",
                       description="The Kirschenmann Vineyard is one of Lodi's oldest and most celebrated sites, with vines planted in the early 1900s. This single-vineyard bottling offers extraordinary concentration and site specificity, showing why Lodi's ancient vines deserve global recognition.")
if new18:
    PAIR(prod5a2, "Short rib bourguignon with pearl onions and carrots", "complement", "classic", "main", "The Kirschenmann's depth and structure match braised short rib's intensity; bourguignon's Burgundian technique creates an unexpected bridge between Old and New World sensibilities.")
    PAIR(prod5a2, "Grilled T-bone steak with compound herb butter", "complement", "classic", "main", "The wine's old-vine power and structure demand a preparation this substantial; the herb butter's richness mirrors the wine's depth while the steak's char complements its dark-fruit character.")
    PAIR(prod5a2, "Dark chocolate mousse with raspberry coulis and sea salt", "complement", "adventurous", "dessert", "The Kirschenmann's intense fruit and spice create an unlikely but rewarding match with dark chocolate; raspberry echoes the wine's fruit and salt amplifies everything.")
    PAIR(prod5a2, "Aged Manchego with Lodi almonds and quince paste", "bridge", "suggested", "cheese", "Local almonds echo the wine's nut character; Manchego's tang and quince's sweetness create a bridge between the wine's old-vine depth and the cheese's crystalline richness.")

p5b = P("Michael David Winery", "winery", r5, "USA",
         production_philosophy="artisanal",
         philosophy_description="A sixth-generation family farm in Lodi's Phillips family tradition, Michael David produces a wide range of wines with a focus on Lodi's old-vine Zinfandel and diverse varietal lineup. Known for the iconic '7 Deadly Zins' that introduced many consumers to Lodi's quality.",
         reputation_narrative="Michael David is Lodi's most prolific quality ambassador, balancing high-volume production with genuine wine quality. Their Inkblot and Freakshow ranges offer serious quality at accessible price points.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Michael David Freakshow Cabernet Sauvignon Lodi", "wine_still", p5b, r5, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="mid_range",
                       description="Lodi Cabernet Sauvignon from Michael David's Freakshow range, delivering generous blackberry, cassis, and vanilla in an approachable, plush style that has earned a cult following for its dramatic label and excellent value.")
if new19:
    PAIR(prod5b1, "Bacon cheeseburger with caramelised onions and special sauce", "complement", "classic", "casual", "The wine's bold fruit and plush tannin are perfectly suited to a burger of this calibre; caramelised onions' sweetness bridges the wine's fruit while bacon's smoke complements its oak.")
    PAIR(prod5b1, "Pork tenderloin with blackberry BBQ sauce and corn succotash", "complement", "established", "main", "The wine's blackberry character creates a direct flavour echo with the BBQ sauce; pork tenderloin's lean richness provides the protein the wine's tannin needs.")
    PAIR(prod5b1, "Sharp cheddar and Gouda cheese board with Lodi almonds", "complement", "established", "cheese", "The wine's accessible structure and generous fruit pair well with sharp cheddar's pungency and Gouda's sweetness; almonds add savoury crunch.")
    PAIR(prod5b1, "Grilled portobello burger with smoked mozzarella and pesto", "complement", "suggested", "casual", "The wine's bold fruit and gentle tannin handle the portobello's earthy umami; smoked mozzarella bridges the wine's oak while pesto's herbaceousness adds aromatic lift.")

prod5b2, new20 = PROD("Michael David Inkblot Cabernet Franc Lodi", "wine_still", p5b, r5, "USA",
                       subcategory="Cabernet Franc", price_tier="mid_range",
                       description="From Lodi's warm Central Valley, Michael David's Inkblot Cabernet Franc offers ripe plum, violet, and graphite character with a distinctly warm-climate approachability and lingering herbal finish — an unusual but compelling Lodi expression.")
if new20:
    PAIR(prod5b2, "Roasted duck breast with plum sauce and bok choy", "complement", "established", "main", "The wine's plum and violet character mirrors the sauce's stone fruit; duck's richness is cut by the wine's firm acidity and herbaceous finish.")
    PAIR(prod5b2, "Pork belly with five-spice glaze and pickled daikon", "complement", "established", "main", "The wine's warm, spice-driven character resonates with five-spice glaze's complexity; pickled daikon's acidity echoes the wine's freshness and cuts through pork belly's fat.")
    PAIR(prod5b2, "Aged Camembert with dried plum and toasted baguette", "bridge", "suggested", "cheese", "The wine's plum and earthy graphite find a harmonious partner in ripe Camembert; dried plum bridges the wine's fruit while the baguette grounds the pairing.")
    PAIR(prod5b2, "Lamb meatballs with roasted tomato sauce and mint yogurt", "complement", "established", "main", "Cabernet Franc's herbal character and red-fruit depth find an ideal match in lamb; mint yogurt echoes the wine's herbaceousness while tomato sauce bridges its acidity.")

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
print("B144 complete.")
conn.close()
