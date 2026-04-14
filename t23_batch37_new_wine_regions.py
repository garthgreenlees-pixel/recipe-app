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
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
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
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === SONOMA COUNTY (USA) ===
print("\n=== Sonoma County AVA (USA) ===")
r_sonoma = R(
    name="Sonoma County",
    country="USA",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Sonoma County AVA",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="California's most diverse wine region, stretching 60 miles from the Pacific coast to the Mayacamas mountains and encompassing 17 sub-AVAs with radically different terroirs. The cool, foggy Sonoma Coast and Green Valley produce benchmark Pinot Noir and Chardonnay rivalling Burgundy; Russian River Valley is California's coolest and most prestigious Pinot Noir heartland; Dry Creek Valley specialises in Zinfandel; Alexander Valley in Cabernet Sauvignon. The county's size and climatic diversity make it fundamentally more complex than Napa Valley — a region of specialists rather than one dominant style.",
    key_producers="Williams Selyem, Kosta Browne, Littorai, Rochioli, Ridge (Geyserville), Flowers",
    historical_context="Wine production in Sonoma predates Napa Valley — General Mariano Vallejo's rancho produced wine in the 1830s and Agoston Haraszthy established Buena Vista, California's first major winery, in Sonoma in 1857. The Russian River Valley emerged as a world-class Pinot Noir zone in the 1970s–80s, and Sonoma Coast's reputation for cool-climate excellence developed through the 1990s and 2000s."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding vintage — long cool season producing Pinot Noir and Chardonnay of extraordinary precision, free of the heat spike problems of 2020."),
    (2020, "very_good", "stable", "Challenging fire season but well-managed. Earlier-picked lots showed excellent quality, though smoke taint affected some vineyards."),
    (2019, "excellent", "stable", "Excellent across all sub-AVAs. Russian River Pinot Noir of great elegance and aging potential."),
    (2018, "very_good", "stable", "Good vintage with some fire impact. Wines that avoided smoke showed outstanding quality."),
    (2017, "excellent", "rising", "One of Sonoma's finest recent vintages — balanced, elegant wines across all sub-AVAs."),
]:
    VIN(r_sonoma, yr, qd, pt, sn)

p_littorai = P(
    name="Littorai",
    country="USA",
    region_id=r_sonoma,
    producer_type="winery",
    description="Ted and Heidi Lemon's biodynamic estate producing California's most Burgundian Pinot Noir and Chardonnay — wines of ethereal delicacy, transparency, and site expression. Ted Lemon trained at DRC and brought that philosophy to Sonoma Coast and Anderson Valley, creating wines that demonstrate what extreme cool-climate viticulture can achieve. Their Ted Lemon Lander Ranch (Anderson Valley) and The Haven (Sonoma Coast) are among California's most sought-after single-vineyard wines."
)
prod_littorai, new = PROD(
    name="Littorai Sonoma Coast Pinot Noir",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_littorai,
    region_id=r_sonoma,
    origin_country="USA",
    description="The benchmark Sonoma Coast Pinot Noir from California's most Burgundian producer — biodynamic fruit from cool hillside vineyards near the Pacific coast, fermented with indigenous yeasts and aged in Burgundy cooperage. Translucent ruby with extraordinary delicacy: wild strawberry, sour cherry, fresh rose, dried herbs, silica mineral, and a sea breeze salinity unique to the Sonoma Coast. Among California's most elegant and age-worthy Pinot Noirs.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_littorai, "Pan-seared salmon with pinot noir butter sauce and chanterelles", "complement", "classic", "main", "The classic California Pinot Noir pairing — Pacific salmon with coastal Pinot. The wine's red fruit and mineral salinity echo the salmon's richness, chanterelles bridge its earthy depth, and the Pinot Noir butter mirrors its delicacy.")
    PAIR(prod_littorai, "Duck breast with cherry gastrique and farro", "complement", "established", "main", "Pinot Noir's affinity for duck is universal — the wine's sour cherry and dried herb character mirrors the gastrique while farro provides an earthy, nutty grounding.")
    PAIR(prod_littorai, "Dungeness crab cakes with tarragon aioli and lemon", "complement", "adventurous", "starter", "An adventurous California pairing — cool-climate Pinot Noir with Dungeness crab. The wine's salinity and delicate fruit complement the sweet crab while tarragon bridges its herbal notes.")
    PAIR(prod_littorai, "Aged Cowgirl Creamery Mt. Tam with honey and walnuts", "complement", "established", "cheese", "California artisan cheese with California Pinot — the wine's red fruit and mineral depth complement the triple cream's richness. Honey moderates its acidity while walnuts echo its earthy depth.")

p_williams_selyem = P(
    name="Williams Selyem",
    country="USA",
    region_id=r_sonoma,
    producer_type="winery",
    description="The founding estate of the California Pinot Noir renaissance — Burt Williams and Ed Selyem produced tiny quantities of extraordinary Russian River Valley Pinot Noir in the 1980s from a garage in Healdsburg, eventually commanding mailing list positions that defined California wine cult status. Now owned by John Dyson, the estate continues the tradition of vineyard-designate Pinot Noirs from the greatest Russian River and Sonoma Coast sites. Rochioli, Allen, Drake, and Precious Mountain remain benchmark designates."
)
prod_ws, new = PROD(
    name="Williams Selyem Rochioli Vineyard Pinot Noir Russian River Valley",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_williams_selyem,
    region_id=r_sonoma,
    origin_country="USA",
    description="One of California's most legendary vineyard-designate Pinot Noirs — from the Rochioli family's estate vineyards on the Westside Road in Russian River Valley, produced under the Williams Selyem label since the founding era of California fine Pinot. Deeply coloured for Pinot Noir, with extraordinary concentration and complexity: black cherry, plum, violet, espresso, dark chocolate, and the distinctive River Road mineral quality. Mailing list only. Defines Russian River Valley Pinot Noir.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_ws, "Grilled duck magret with blackberry reduction and lentilles du Puy", "complement", "classic", "main", "The wine's black cherry intensity and density can support duck magret — the blackberry reduction mirrors its dark fruit while lentils provide earthy ballast for this richly structured Pinot.")
    PAIR(prod_ws, "Braised short ribs with mushroom duxelles and thyme gremolata", "complement", "established", "main", "Russian River's richest Pinot Noir can handle beef preparations — braised short ribs' deep savoury notes are complemented by the wine's dark fruit while mushroom duxelles echoes its earthy depth.")
    PAIR(prod_ws, "Grilled whole quail with truffle vinaigrette and micro greens", "complement", "established", "main", "Quail's delicate gamey intensity pairs beautifully with concentrated Russian River Pinot. Truffle vinaigrette bridges the wine's earthy complexity while micro greens add freshness.")
    PAIR(prod_ws, "Humboldt Fog goat cheese with cherry preserves", "complement", "established", "cheese", "California artisan cheese with California cult Pinot — Humboldt Fog's distinctive blue-grey rind and goat tang bridge to the wine's red fruit. Cherry preserves echo its dark cherry concentration.")

# === GOLAN HEIGHTS (Israel) ===
print("\n=== Golan Heights (Israel) ===")
r_golan = R(
    name="Golan Heights",
    country="Israel",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Golan Heights",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Israel's most prestigious wine region, occupying the basalt plateau at 400–1,200m elevation in the north of the country, adjacent to the Syrian and Lebanese borders. The Golan Heights' volcanic soils, continental climate, and significant altitude produce wines of surprising freshness and complexity — the antithesis of what international audiences expect from Israeli wine. Golan Heights Winery (Yarden wines) established the region's reputation in the 1980s, demonstrating that serious fine wine could be produced from the volcanic basalt terroir.",
    key_producers="Golan Heights Winery (Yarden), Pelter Winery, Chateau Golan, Odem Mountain",
    historical_context="The Golan Heights was captured by Israel from Syria in the 1967 Six-Day War and formally annexed in 1981. The Golan Heights Winery was established in 1983 at Katzrin as a cooperative of four kibbutzim, with the explicit goal of producing internationally competitive wine. Their success — winning blind-tasting awards at major international competitions — transformed the perception of Israeli wine globally."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding vintage — long cool season producing wines of exceptional freshness for the region."),
    (2020, "very_good", "stable", "Good vintage with high natural acidity from altitude. Chardonnay and Cabernet of good structure."),
    (2019, "excellent", "rising", "One of the decade's finest vintages. Altitude wines of remarkable freshness and longevity."),
    (2018, "very_good", "stable", "Reliable vintage across all varieties. Syrah and Cabernet of good concentration."),
    (2017, "excellent", "stable", "Classic Golan Heights vintage — balanced wines with the volcanic basalt mineral character well expressed."),
]:
    VIN(r_golan, yr, qd, pt, sn)

p_yarden = P(
    name="Golan Heights Winery",
    country="Israel",
    region_id=r_golan,
    producer_type="winery",
    description="The founding and most important estate of modern Israeli fine wine — established in 1983 at Katzrin on the Golan Heights plateau. The Yarden label (top tier), Gamla, and Golan brands cover a comprehensive range from sparkling to dessert wine, all produced from high-altitude volcanic basalt vineyards. Yarden Chardonnay and Cabernet Sauvignon have repeatedly performed above expectation in international blind tastings, establishing the Golan Heights as Israel's most credible fine wine region."
)
prod_yarden_cab, new = PROD(
    name="Yarden Cabernet Sauvignon Golan Heights",
    category="wine_still",
    subcategory="Cabernet Sauvignon",
    producer_id=p_yarden,
    region_id=r_golan,
    origin_country="Israel",
    description="The benchmark Israeli Cabernet Sauvignon — from volcanic basalt vineyards at 900–1,100m altitude on the Golan Heights, aged in French and American oak. The wine combines Mediterranean ripeness with highland freshness: blackcurrant, dark plum, cedar, tobacco, and a distinctive basalt mineral note. More structured and age-worthy than the climate might suggest, with firm tannins and good natural acidity. One of the Middle East's most internationally credible red wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_yarden_cab, "Lamb kebabs with sumac, za'atar, and labneh", "complement", "classic", "main", "Israeli Cabernet with Levantine lamb preparation — the wine's structure supports the richness while sumac's tartness mirrors its acidity. Za'atar echoes the wine's herbal complexity.")
    PAIR(prod_yarden_cab, "Slow-braised beef with dates, pomegranate, and almonds (Persian-influenced)", "complement", "established", "main", "The wine's dark fruit and cedar notes bridge to the sweet-savory complexity of Persian-influenced beef. Pomegranate echoes its tartness while almonds bridge its mineral depth.")
    PAIR(prod_yarden_cab, "Grilled eggplant with tahini, pine nuts, and pomegranate molasses", "complement", "suggested", "starter", "The wine's dark fruit bridges to roasted eggplant's smokiness. Tahini adds richness while pomegranate molasses echoes the wine's tartness — a quintessential Levantine flavour bridge.")
    PAIR(prod_yarden_cab, "Aged Israeli sheep's milk cheese with date honey (silan)", "complement", "established", "cheese", "The wine's structure and dark fruit complement aged sheep's milk cheese. Date honey (silan) mirrors its dark fruit concentration in a pairing of obvious Israeli cultural logic.")

p_pelter = P(
    name="Pelter Winery",
    country="Israel",
    region_id=r_golan,
    producer_type="winery",
    description="One of the Golan Heights' most innovative boutique wineries, established by Tal Pelter with a focus on expressing the region's volcanic terroir through minimal intervention winemaking. Pelter's Syrah and T2 (Tempranillo-Tannat) have attracted international attention for their freshness and complexity — wines that convincingly transcend the expected profile of 'warm-climate wine' through altitude and terroir expression."
)
prod_pelter, new = PROD(
    name="Pelter Syrah Golan Heights",
    category="wine_still",
    subcategory="Syrah",
    producer_id=p_pelter,
    region_id=r_golan,
    origin_country="Israel",
    description="A cool-climate expression of Syrah from the volcanic plateau — using altitude to produce freshness and aromatics unexpected from an Israeli wine. Violet, black olive, smoked meat, white pepper, and volcanic mineral with a Northern Rhône-like elegance that challenges conventional expectations. The wine's relative lightness and freshness make it a compelling case for the Golan Heights' unique terroir potential beyond the obvious Cabernet pathway.",
    price_tier="premium"
)
if new:
    PAIR(prod_pelter, "Shawarma-spiced lamb shoulder with tehina, parsley, and flatbread", "complement", "established", "main", "Cool-climate Syrah with shawarma spicing — the wine's olive and pepper notes bridge to the Middle Eastern spice mix while its fresh acidity cuts through the lamb fat.")
    PAIR(prod_pelter, "Grilled whole chicken with za'atar, lemon, and olive oil (Shish tawook style)", "complement", "established", "main", "Fresh, herb-marinated chicken with elegant Golan Syrah — za'atar echoes the wine's herbal notes, lemon mirrors its acidity, and the chicken's moderate richness is well matched by its mineral depth.")
    PAIR(prod_pelter, "Merguez sausage with harissa, hummus, and grilled pita", "complement", "established", "main", "North African-influenced sausage with Israeli Syrah — harissa's pepper notes echo the wine's spice while hummus bridges its mineral depth. A cross-Mediterranean pairing of logical affinity.")
    PAIR(prod_pelter, "Goat's cheese from the Galilee with fig preserves", "bridge", "suggested", "cheese", "Israeli goat's cheese with Golan Syrah — the wine's violet and olive notes bridge to the tangy cheese. Fig preserves echo its dark fruit while the combination has obvious regional logic.")

# === SAINT-CHINIAN AOC (France) ===
print("\n=== Saint-Chinian AOC (France) ===")
r_sc = R(
    name="Saint-Chinian",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Saint-Chinian AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of Languedoc's most distinctive and under-appreciated appellations, situated in the foothills of the Cévennes north of Béziers where two radically different soil types meet: schist in the northern highlands and limestone-clay in the south. The contrast creates two distinct wine styles within the same appellation — schist-grown Syrah and Grenache produce elegant, aromatic wines with mineral freshness, while limestone Syrah produces fuller, richer wines with more tannic structure. Saint-Chinian represents some of the best value in French fine wine.",
    key_producers="Domaine Canet-Valette, Mas Champart, Domaine Navarre, Clos Bagatelle",
    historical_context="Saint-Chinian received its AOC in 1982, having previously been produced under the Coteaux du Languedoc designation. The appellation's most distinctive geological feature — the schist/limestone boundary — was recognised by subdividing the AOC in 2005: Saint-Chinian-Berlou (schist) and Saint-Chinian-Roquebrun (schist) were given their own designations, acknowledging that terroir matters here as much as in Burgundy."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, fresh vintage producing wines of exceptional elegance. Schist-based wines of remarkable mineral precision."),
    (2020, "very_good", "stable", "Warm year producing full, concentrated wines. Both schist and limestone terroirs performed well."),
    (2019, "excellent", "rising", "Outstanding vintage across the appellation. Syrah of exceptional depth and aging potential."),
    (2018, "very_good", "stable", "Classic Languedoc vintage with good concentration and Mediterranean character."),
    (2017, "excellent", "stable", "One of the appellation's finest recent vintages — complex, structured wines with good longevity."),
]:
    VIN(r_sc, yr, qd, pt, sn)

p_canet = P(
    name="Domaine Canet-Valette",
    country="France",
    region_id=r_sc,
    producer_type="winery",
    description="The reference producer of Saint-Chinian — Marc Valette's biodynamic estate on schist soils in the commune of Cessenon-sur-Orb, producing wines of extraordinary mineral purity and complexity. The estate's top wine, 'Une et Mille Nuits,' is a barrel-selected blend that has attracted international critical acclaim and brought Saint-Chinian to the attention of the global fine wine market. Valette's commitment to biodynamics and old-vine schist Syrah has shown what this overlooked appellation can achieve."
)
prod_canet, new = PROD(
    name="Domaine Canet-Valette Une et Mille Nuits Saint-Chinian",
    category="wine_still",
    subcategory="Syrah",
    producer_id=p_canet,
    region_id=r_sc,
    origin_country="France",
    description="The flagship wine of Saint-Chinian — a barrel selection from the finest schist parcels of Canet-Valette. Predominantly Syrah with Grenache and Mourvèdre, this wine demonstrates what Languedoc schist terroir can achieve with biodynamic farming and minimal intervention. Violet, black olive, garrigue, dark cherry, graphite mineral, and smoked meat. More mineral and structured than typical Languedoc, with genuine aging potential. One of southern France's most compelling wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_canet, "Roasted wild boar with juniper, dark chocolate sauce, and celeriac", "complement", "established", "main", "The wine's garrigue and mineral depth are natural companions for mountain game. Juniper echoes its wild herb character while dark chocolate bridges its schist mineral quality.")
    PAIR(prod_canet, "Slow-braised leg of lamb with herbes de Provence and aioli", "complement", "classic", "main", "Languedoc lamb with Languedoc Syrah — the wine's garrigue and violet notes mirror the Provençal herbs while its mineral backbone supports the lamb's richness.")
    PAIR(prod_canet, "Daube de boeuf with olives, orange peel, and thyme", "complement", "classic", "main", "Southern French beef stew with the region's finest red — olives echo the wine's olive notes, orange peel bridges its fruit, and thyme mirrors its garrigue complexity.")
    PAIR(prod_canet, "Pélardon (Languedoc goat's cheese) with honey and black pepper", "complement", "established", "cheese", "Regional goat cheese with regional Syrah — the wine's mineral depth and fruit complexity complement the cheese's tangy freshness. Black pepper echoes its spice while honey bridges the schist mineral.")

p_mas_champart = P(
    name="Mas Champart",
    country="France",
    region_id=r_sc,
    producer_type="winery",
    description="Isabelle and Matthieu Champart's biodynamic estate on the schist slopes above Berlou — producers of Saint-Chinian's most consistently elegant and mineral wines. The Causse du Bousquet — a pure Syrah from ancient schist slopes — is considered one of the finest examples of Languedoc Syrah's potential, showing the finesse that schist soils can impart to a variety more often associated with power. The estate has been a cornerstone of Saint-Chinian's quality revolution."
)
prod_champart, new = PROD(
    name="Mas Champart Causse du Bousquet Saint-Chinian Berlou",
    category="wine_still",
    subcategory="Syrah",
    producer_id=p_mas_champart,
    region_id=r_sc,
    origin_country="France",
    description="From the ancient schist plateau of Berlou — pure Syrah biodynamically farmed on the mineral-poor, well-drained schist that gives Saint-Chinian its most distinctive wines. Cool mountain influence at 400m combines with Mediterranean sun to produce a Syrah of remarkable freshness and aromatic intensity: violet, graphite, black olive, garrigue, smoked meat, and an iron-schist mineral note that is unmistakably of this extraordinary terroir.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_champart, "Grilled lamb chops with rosemary, garlic, and Puy lentils", "complement", "classic", "main", "Mountain Syrah with mountain lamb — the wine's violet and garrigue notes complement rosemary perfectly. Lentils provide earthy depth while the lamb's fat is balanced by Syrah's mineral precision.")
    PAIR(prod_champart, "Venison medallions with blackberry sauce and potato gratin", "complement", "established", "main", "The wine's schist mineral and dark fruit are well-matched to venison. Blackberry sauce echoes its fruit while potato gratin provides a rich, starchy complement to the lean game.")
    PAIR(prod_champart, "Roasted pepper and anchovy flatbread with olive tapenade", "complement", "established", "starter", "The wine's olive notes and garrigue character bridge naturally to tapenade and anchovy. Roasted pepper adds sweetness that mirrors its dark fruit.")
    PAIR(prod_champart, "Aged Manchego with olive oil and romesco", "complement", "suggested", "cheese", "The wine's mineral depth and dark fruit bridge to aged sheep's milk cheese. Romesco echoes the wine's pepper and olive character in a cross-Mediterranean pairing.")

# === MERCUREY AOC (France) ===
print("\n=== Mercurey AOC (France) ===")
r_merc = R(
    name="Mercurey",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Mercurey AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The most important appellation of the Côte Chalonnaise — the large, diverse zone south of the Côte de Beaune producing accessible Burgundy from Pinot Noir and Chardonnay at significantly lower prices than the famous northern communes. Mercurey covers around 670 hectares of mostly red wine production from clay-limestone soils, with 31 premier cru vineyards including Clos du Roi, Clos des Myglands, and Les Champs Martins. The best wines offer genuine Burgundian character — earthy, complex, and age-worthy — at prices that make serious Burgundy accessible.",
    key_producers="Château de Chamirey (Antonin Rodet), Domaine Faiveley, Domaine Lorenzon, Domaine du Meix-Foulot",
    historical_context="Mercury has one of Burgundy's longest continuous viticultural histories — its wines were among the first to be exported to northern European markets in the medieval period. The Côte Chalonnaise as a designated sub-region was only formally recognised in the 1990s, but Mercurey itself received its communal AOC in 1936. The appellation's relative accessibility has made it an important gateway to Burgundy for restaurants."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, elegant vintage producing Mercurey of exceptional finesse and mineral precision. Among the finest recent vintages for the appellation."),
    (2020, "very_good", "stable", "Warm year producing full, approachable wines with good fruit character."),
    (2019, "excellent", "rising", "Outstanding vintage — complex, age-worthy Pinot Noir with genuine Burgundian depth."),
    (2018, "very_good", "stable", "Rich, concentrated wines from the hot summer. Good early-drinking character."),
    (2017, "excellent", "stable", "Very good vintage with classic Burgundian balance — earthy, mineral wines of good structure."),
]:
    VIN(r_merc, yr, qd, pt, sn)

p_faiveley = P(
    name="Domaine Faiveley",
    country="France",
    region_id=r_merc,
    producer_type="winery",
    description="One of Burgundy's most important négociant-estates, with extensive holdings across the Côte de Nuits, Côte de Beaune, and Côte Chalonnaise. Faiveley's Mercurey holdings — particularly the Clos des Myglands and La Framboisière premiers crus — are considered the benchmark for the appellation. Under Erwan Faiveley, the domaine has embraced more natural winemaking while maintaining the Faiveley house style of precision and terroir clarity."
)
prod_faiveley_merc, new = PROD(
    name="Faiveley Mercurey La Framboisière Premier Cru",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_faiveley,
    region_id=r_merc,
    origin_country="France",
    description="A benchmark Mercurey Premier Cru from one of the appellation's finest sites — La Framboisière on clay-limestone soils of the plateau. The wine shows the classic Mercurey character: earthy red cherry and plum fruit, a distinctive farmyard complexity, good tannin structure, and a minerality that sets the Côte Chalonnaise apart from simpler Burgundy. Aged in Burgundy barrels, it develops excellent complexity over 5–10 years. Excellent value for a serious Burgundy Premier Cru.",
    price_tier="premium"
)
if new:
    PAIR(prod_faiveley_merc, "Poulet de Bresse rôti with tarragon jus and haricots verts", "complement", "classic", "main", "The definitive Burgundy pairing — Bresse poultry with regional Pinot Noir. Mercurey's earthy depth and red fruit complement the chicken without overwhelming it. Tarragon bridges the wine's herbal notes.")
    PAIR(prod_faiveley_merc, "Pan-fried duck liver with caramelised apple and chicory", "complement", "established", "starter", "Pinot Noir and duck liver is a classical French combination. Mercurey's structure and earthy depth support the rich liver while caramelised apple echoes its red fruit. Chicory's bitterness mirrors its tannin.")
    PAIR(prod_faiveley_merc, "Beef bourguignon with button mushrooms and lardons", "complement", "classic", "main", "Burgundy's iconic beef stew with its regional wine — the wine's earthy mushroom notes and red fruit complement the dish's deep, slow-cooked character. The Mercurey terroir echoes the bourguignon's essence.")
    PAIR(prod_faiveley_merc, "Époisses de Bourgogne washed-rind cheese with walnut bread", "complement", "classic", "cheese", "The great Burgundy pairing — Époisses with regional Pinot Noir. The wine's earthy, farmyard complexity mirrors the cheese's pungent washed rind while its acidity cuts through the runny richness.")

p_lorenzon = P(
    name="Domaine Lorenzon",
    country="France",
    region_id=r_merc,
    producer_type="winery",
    description="Bruno Lorenzon's small family domaine producing some of Mercurey's most natural and intellectually serious wines. Working without chemical intervention and with minimum sulphur, Lorenzon has demonstrated the depth achievable from Mercurey's best clay-limestone terroirs. His premier cru Veleys is considered one of the appellation's finest wines and has gained a devoted following among Burgundy enthusiasts seeking authentic, unmanipulated wines at reasonable prices."
)
prod_lorenzon, new = PROD(
    name="Domaine Lorenzon Mercurey Les Veleys Premier Cru",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_lorenzon,
    region_id=r_merc,
    origin_country="France",
    description="From the Les Veleys premier cru on deep clay-limestone soils — Bruno Lorenzon's benchmark Mercurey, produced with minimal intervention and low sulphur. The wine shows the authentic depth and complexity that Côte Chalonnaise clay-limestone can achieve: dark cherry, wild strawberry, earthy loam, mushroom, dried herbs, and a chalky mineral backbone that develops beautifully over 8–12 years. One of Mercurey's most compelling value propositions in fine Burgundy.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_lorenzon, "Wild mushroom ragout with polenta and aged Comté", "complement", "classic", "main", "The wine's mushroom and earthy notes are mirrored in the ragout — a natural Burgundian affinity. Polenta provides texture while Comté adds nutty depth that bridges to the wine's mineral complexity.")
    PAIR(prod_lorenzon, "Roasted guinea fowl with morel cream sauce and asparagus", "complement", "established", "main", "Côte Chalonnaise wine with guinea fowl — the wine's earthy depth and red fruit complement the bird's slight gaminess while morel cream mirrors its mushroom notes. Asparagus adds spring freshness.")
    PAIR(prod_lorenzon, "Rabbit terrine with pistachios, herbs, and Dijon mustard", "complement", "established", "starter", "Light-bodied Burgundy with rabbit terrine — the wine's red fruit and earthy complexity elevate the simple terrine. Pistachios mirror its earthy depth while mustard's sharpness contrasts its fruit.")
    PAIR(prod_lorenzon, "Saint-Marcellin with truffle honey", "complement", "suggested", "cheese", "Soft, runny Dauphiné cheese with Burgundy — the wine's earthy, farmyard notes bridge to Saint-Marcellin's pungency. Truffle honey connects to the wine's natural mushroom character.")

# === SUSSEX PDO (England) ===
print("\n=== Sussex PDO (England) ===")
r_sussex = R(
    name="Sussex",
    country="England",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Sussex PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="England's premier wine county and the heartland of the English sparkling wine revolution — the chalk Downs of East and West Sussex sharing the same geological formation as Champagne's Côte des Blancs, producing Chardonnay, Pinot Noir, and Pinot Meunier of surprising quality. The South Downs, Weald, and High Weald provide a diversity of soils and exposures, with south-facing chalk and greensand slopes providing the ideal cool-climate site selection. Sussex is home to the country's most celebrated estates including Nyetimber, Ridgeview, and Wiston, whose traditional method sparkling wines have begun competing at international level.",
    key_producers="Nyetimber, Ridgeview Wine Estate, Wiston Estate, Bolney Wine Estate",
    historical_context="Commercial sparkling wine production in Sussex effectively began with Nyetimber in 1988 when Christie's planted Chardonnay, Pinot Noir, and Pinot Meunier in a former apple orchard at West Chiltington. The Sussex PDO was granted in 2019 — the first English county PDO — following a precedent set by similar regional protection in established European wine regions. Climate change has steadily extended the growing season and improved ripeness, making English sparkling wine increasingly competitive."
)
for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "One of England's finest vintages — long, warm summer followed by cool autumn producing Chardonnay and Pinot of exceptional ripeness and acidity."),
    (2021, "very_good", "stable", "Challenging spring with good summer recovery. Sparkling base wines of good acid structure."),
    (2020, "excellent", "rising", "Outstanding vintage — warm, dry summer produced wines of remarkable ripeness for English conditions."),
    (2019, "very_good", "stable", "Good growing season. Traditional method wines of consistent quality."),
    (2018, "excellent", "rising", "The benchmark recent English vintage — exceptional ripeness and concentration, producing wines of real longevity."),
]:
    VIN(r_sussex, yr, qd, pt, sn)

p_nyetimber = P(
    name="Nyetimber",
    country="England",
    region_id=r_sussex,
    producer_type="winery",
    description="The founding and most celebrated estate of English fine sparkling wine — established in 1988 at West Chiltington on the chalk and greensand soils of the West Sussex Weald. Nyetimber's Blanc de Blancs and Classic Cuvée have repeatedly won international awards, with the 2003 Blanc de Blancs famously outperforming Champagnes at blind tasting. Now producing over 900,000 bottles annually, Nyetimber remains the most recognised English wine brand internationally and the estate that convinced the world to take English sparkling wine seriously."
)
prod_nyetimber, new = PROD(
    name="Nyetimber Classic Cuvée Multi-Vintage Sussex",
    category="wine_sparkling",
    subcategory="Chardonnay",
    producer_id=p_nyetimber,
    region_id=r_sussex,
    origin_country="England",
    description="The flagship wine of England's most celebrated sparkling producer — a multi-vintage blend of Chardonnay, Pinot Noir, and Pinot Meunier from Sussex chalk vineyards, traditionally fermented and aged on lees for a minimum of three years. Fine, persistent bubbles with aromas of green apple, lemon curd, fresh brioche, cream, chalk mineral, and a distinctive cool-climate freshness that no amount of winemaking could recreate in warmer regions. The definitive English sparkling wine.",
    price_tier="premium"
)
if new:
    PAIR(prod_nyetimber, "English oysters from Whitstable with shallot vinegar and lemon", "complement", "classic", "starter", "The ultimate English food and wine pairing — Whitstable oysters with English sparkling wine. The wine's chalk mineral and fine bubble precision mirror the oyster's briny mineral character. Both expressions of the same English geology.")
    PAIR(prod_nyetimber, "Smoked salmon with dill crème fraîche and cucumber on blinis", "complement", "classic", "starter", "English sparkling wine's classic aperitif pairing — Scottish smoked salmon's richness is cut by the wine's acidity while its brioche notes bridge the blini's yeastiness. Dill echoes the wine's fresh herbal character.")
    PAIR(prod_nyetimber, "Potted shrimp from Morecambe Bay with brown butter and mace", "complement", "established", "starter", "Traditional British seafood with English sparkling — the wine's chalk mineral and fine bubble cut through the butter's richness while its green apple freshness brightens the shrimp's sweetness.")
    PAIR(prod_nyetimber, "Fish and chips with tartare sauce and malt vinegar (fine dining version)", "complement", "adventurous", "main", "The quintessential British pairing for an adventurous sommelier — English sparkling wine's acidity and bubble lighten the batter while its chalk mineral quality bridges the fish's delicacy. Malt vinegar echoes the wine's high acidity.")

p_ridgeview = P(
    name="Ridgeview Wine Estate",
    country="England",
    region_id=r_sussex,
    producer_type="winery",
    description="The Roberts family estate in the South Downs near Ditchling, producing some of England's most consistent and age-worthy traditional method sparkling wines. Ridgeview was the second major English sparkling wine estate (after Nyetimber) to achieve international recognition — their Bloomsbury (Chardonnay-dominant) and Fitzrovia Rosé have won multiple international awards. The estate focuses on terroir expression and long lees aging, producing wines of genuine complexity and cellaring potential."
)
prod_ridgeview, new = PROD(
    name="Ridgeview Blanc de Blancs Sussex Brut",
    category="wine_sparkling",
    subcategory="Chardonnay",
    producer_id=p_ridgeview,
    region_id=r_sussex,
    origin_country="England",
    description="A 100% Chardonnay traditional method sparkling from the chalk soils of the South Downs — one of England's finest Blanc de Blancs. Exceptionally fine bubbles, aromas of white orchard fruit, lemon, chalk, oyster shell, brioche, and a saline freshness that unmistakably evokes the English coastal countryside. Extended lees aging produces a creamy autolytic complexity that rewards cellaring. Among the finest English sparkling wines for food pairing versatility.",
    price_tier="premium"
)
if new:
    PAIR(prod_ridgeview, "Dressed Cornish crab with avocado, lemon, and herb salad", "complement", "classic", "starter", "English sparkling Blanc de Blancs with British crab — the wine's chalk mineral and citrus precision complement the sweet crab perfectly. Avocado adds richness while lemon mirrors the wine's bright acidity.")
    PAIR(prod_ridgeview, "Native lobster thermidor with tarragon and gruyère", "complement", "established", "main", "Blanc de Blancs with lobster thermidor — the wine's autolytic creaminess bridges the rich sauce while its chalk mineral contrasts the gruyère. Tarragon echoes its herbal freshness.")
    PAIR(prod_ridgeview, "Coronation chicken with mango chutney on brioche", "complement", "established", "starter", "A quintessentially British pairing for a British sparkling wine — the wine's brioche notes connect to the bread while its acidity cuts through the spiced mayonnaise. Mango chutney echoes its orchard fruit.")
    PAIR(prod_ridgeview, "Aged Montgomery's Cheddar with Branston pickle and oatcakes", "complement", "established", "cheese", "A British cheese board with English sparkling — the wine's chalk mineral and fine bubble are surprisingly good companions to aged farmhouse Cheddar. Branston pickle bridges the wine's fruit while oatcakes provide a neutral base.")

# Final counts
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
print("\nDone.")
cur.close()
conn.close()
