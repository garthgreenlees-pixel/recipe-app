#!/usr/bin/env python3
"""Terminal 19 — Batch 1: Constantia (SA) + Ahr (Germany) + Burgenland dessert
New regions: Constantia Ward (South Africa), Ahr (Germany)
Additions: Weingut Kracher dessert wine for Burgenland
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS region: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  ✓ Region [{rid}]: {name}, {country}")
    return rid

def VIN(region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory="stable"):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory))
    print(f"    ✓ Vintage {year}: {quality_descriptor} ({quality_rating}/100)")

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Producer [{pid}]: {name}")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T19 BATCH 1: CONSTANTIA + AHR + BURGENLAND DESSERT ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTIA WARD — South Africa's Oldest Wine Ward
# Home of Vin de Constance — one of the world's legendary dessert wines
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CONSTANTIA WARD — NEW REGION ──")
r_constantia = R(
    "Constantia Ward",
    "South Africa",
    "wine",
    designation_type="ward",
    designation_name="Constantia Ward",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Constantia Ward is South Africa's oldest wine-producing area — the cradle of Cape winemaking, "
        "established by Governor Simon van der Stel in 1685 on the south-facing slopes of the "
        "Constantiaberg above Cape Town. The ward's distinctive terroir of decomposed Capeite granite "
        "and weathered sandstone at 50-300m altitude, cooled by Atlantic Ocean breezes from both "
        "False Bay and the open Atlantic, creates conditions ideal for Sauvignon Blanc, Semillon, "
        "and the legendary sweet Muscat wines that made Constantia world-famous in the 18th century. "
        "The Vin de Constance (Klein Constantia) is historically one of the world's most celebrated "
        "dessert wines — mentioned by Napoleon, Jane Austen, and Baudelaire."
    ),
    key_producers="Klein Constantia, Groot Constantia, Buitenverwachting, Steenberg, Constantia Glen, Eagles' Nest",
    historical_context=(
        "Governor Simon van der Stel established Constantia Estate in 1685 — making it the Cape's first "
        "wine farm. The estate's Constantia wine achieved international fame in the 18th century when its "
        "sweet Muscat de Frontignan wine was transported to European courts as a luxury commodity. "
        "Napoleon reportedly consoled himself with Vin de Constance during his St Helena exile. Jane Austen "
        "prescribed it as medicine in Sense and Sensibility. After a 170-year hiatus following phylloxera, "
        "Klein Constantia revived the historic wine in 1986 using original Muscat de Frontignan vines — "
        "recreating one of the world's most storied wine traditions."
    )
)

print("\n  Adding Constantia vintages...")
VIN(r_constantia, 2016, 92, "excellent",
    "Long, cool growing season with Atlantic breeze influence. Exceptional Sauvignon Blanc "
    "and Muscat concentration for Vin de Constance. Very good balance of sugar and acidity.",
    price_trajectory="rising")
VIN(r_constantia, 2017, 88, "very_good",
    "Slightly warmer vintage. Good Sauvignon Blanc with tropical notes; "
    "Vin de Constance production slightly reduced due to selective harvest requirements.",
    price_trajectory="stable")
VIN(r_constantia, 2019, 90, "excellent",
    "Classic Constantia season — cool nights and good Atlantic influence. "
    "Excellent Muscat botrytis development for Vin de Constance; fine natural acidity.",
    price_trajectory="rising")
VIN(r_constantia, 2020, 87, "very_good",
    "Challenging harvest conditions with variable weather. Good wines from careful selection; "
    "Sauvignon Blanc particularly successful with fresh herbal character.",
    price_trajectory="stable")
VIN(r_constantia, 2022, 93, "exceptional",
    "Outstanding vintage — perfect botrytis conditions for Vin de Constance. "
    "Exceptional natural acidity alongside concentrated Muscat sweetness. Benchmark year.",
    price_trajectory="rising")

print("\n── KLEIN CONSTANTIA (Constantia Ward) ──")
p_klein = P(
    "Klein Constantia",
    "winery", r_constantia, "South Africa",
    production_philosophy="Keeper of South Africa's most legendary wine tradition: reviving the 18th-century Vin de Constance from historic Muscat de Frontignan vines",
    philosophy_description=(
        "Klein Constantia is one of South Africa's most historically significant wine estates — the property "
        "that revived the legendary 18th-century Constantia dessert wine tradition after a 170-year hiatus. "
        "Their Vin de Constance, first released in 1986 by Duggie Jooste, is made from late-harvest Muscat "
        "de Frontignan (Muscat Blanc à Petits Grains) — the same variety planted by the original 17th-century "
        "estate. The wine is harvested in multiple passes to select only the most botrytis-affected berries "
        "at extreme sugar concentration, then fermented and aged in French oak for extraordinary complexity. "
        "Klein Constantia also produces exceptional dry Sauvignon Blanc and Semillon from the ward's "
        "granite-sandstone slopes."
    ),
    reputation_narrative=(
        "Klein Constantia's Vin de Constance is cited by Wine Advocate (Jancis Robinson and Neal Martin), "
        "Decanter, and Wine Spectator as one of the world's most historically significant dessert wines. "
        "The recreation of the 18th-century Napoleon-era wine is considered one of South Africa's greatest "
        "winemaking achievements. Consistently scoring 94-98, Vin de Constance is placed alongside "
        "Château d'Yquem, Tokaji Aszú, and Trockenbeerenauslese as the world's greatest sweet wines."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_vdc = PROD(
    "Klein Constantia Vin de Constance",
    "wine_dessert", p_klein, r_constantia, "South Africa",
    subcategory="sweet_muscat_frontignan",
    description=(
        "Klein Constantia's Vin de Constance is one of the world's most legendary dessert wines — a "
        "recreation of the 18th-century Constantia wine that captivated Napoleon and European courts. "
        "Made from late-harvest botrytised Muscat de Frontignan (Muscat Blanc à Petits Grains) on "
        "Constantia's granite-sandstone slopes. Luminous gold with extraordinary complexity: "
        "apricot jam, orange marmalade, honey, ginger, quince, and a saline mineral freshness "
        "that prevents cloying sweetness. The wine ages magnificently over 20-30+ years. "
        "Sold in 500ml bottles with the historic 18th-century label design."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_vdc,
    "Tarte Tatin with crème fraîche and Calvados caramel",
    "complement", "classic", "dessert",
    "Klein Constantia Vin de Constance's apricot and honey character achieves a classic "
    "dessert pairing with warm Tarte Tatin — the wine's stone fruit sweetness mirrors the "
    "caramelised apple's complexity; Calvados caramel bridges the wine's hint of brandy-like "
    "richness; crème fraîche's tang cuts through the wine's sweetness. A pairing that balances "
    "the legendary wine's sweetness with the dessert's buttery richness.")
PAIR(prod_vdc,
    "Stilton with fig and walnut cake and pear",
    "complement", "classic", "cheese",
    "Vin de Constance's apricot and honey intensity achieves one of fine dining's great "
    "dessert pairings — blue cheese and sweet wine. The wine's sweetness contrasts Stilton's "
    "pungent saltiness; fig cake bridges the wine's fruit character with the cheese's "
    "complexity; pear amplifies the wine's gentle floral note. A pairing of the 18th-century "
    "dessert wine tradition at its most timeless.")

print("\n── GROOT CONSTANTIA (Constantia Ward) ──")
p_groot = P(
    "Groot Constantia",
    "winery", r_constantia, "South Africa",
    production_philosophy="South Africa's oldest wine estate: the original Simon van der Stel Constantia, now a historic National Monument producing premium Cape wine and Grand Constance",
    philosophy_description=(
        "Groot Constantia is South Africa's oldest wine estate — the original Constantia granted to "
        "Governor Simon van der Stel in 1685, now a National Heritage Site managed by the Groot Constantia "
        "Trust. The estate's 150 hectares include the original historic manor house and wine cellars, "
        "alongside modern production facilities producing Gouverneurs Reserve (flagship Bordeaux blend), "
        "Grand Constance (dessert Muscat), and a range of varietal wines. The estate's historical "
        "significance as South Africa's first commercial wine farm gives it unique cultural authority, "
        "while ongoing quality investment has restored its wine reputation to modern standards."
    ),
    reputation_narrative=(
        "Groot Constantia is one of South Africa's most visited wine destinations — as the original estate "
        "and a National Monument, its wines carry extraordinary historical context. Their Gouverneurs Reserve "
        "Cabernet-based blend scores consistently 88-92 and represents the original Constantia terroir's "
        "capacity for serious red wine production. The Grand Constance sweet Muscat pays direct homage to "
        "the historic 18th-century wine that made Constantia world-famous."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_groot = PROD(
    "Groot Constantia Gouverneurs Reserve Red Constantia",
    "wine_still", p_groot, r_constantia, "South Africa",
    subcategory="red_bordeaux_blend",
    description=(
        "Groot Constantia's Gouverneurs Reserve is the flagship red from South Africa's oldest estate — "
        "a Cabernet Sauvignon-dominant blend with Merlot, Cabernet Franc, and Petit Verdot from the "
        "estate's Constantia Ward granite-sandstone slopes. Deep ruby with blackcurrant, tobacco, "
        "cedar, and the distinctive mineral freshness of Constantia's Atlantic-cooled terroir. "
        "The wine has elegant structure rather than Stellenbosch's power — a Bordeaux-inspired style "
        "that reflects the historic estate's Old World aspirations. Develops well over 8-12 years."
    ),
    price_tier="premium"
)
PAIR(prod_groot,
    "Cape Malay lamb curry with flatbread and yoghurt raita",
    "complement", "adventurous", "main",
    "Groot Constantia Gouverneurs Reserve's Atlantic-mineral Cabernet character finds an unexpected "
    "but compelling South African cultural pairing with Cape Malay lamb curry — the wine's freshness "
    "cuts through the rich spiced coconut base; its blackcurrant fruit amplifies the lamb's richness; "
    "yoghurt raita bridges the wine's acidity with the curry's spice. A pairing of South Africa's "
    "dual heritage: Cape Dutch wine estate meets Cape Malay culinary tradition.")
PAIR(prod_groot,
    "Braised oxtail with root vegetables and maize pap",
    "complement", "established", "main",
    "Gouverneurs Reserve's structured Constantia Cabernet achieves a classic Cape fine dining pairing "
    "with braised oxtail — the wine's mineral freshness cuts through the oxtail's collagen richness "
    "while the dark fruit amplifies the deep beef character; maize pap provides the traditional "
    "South African starch base. A pairing that bridges Groot Constantia's European wine heritage "
    "with South Africa's deeply local culinary tradition.")

# ═══════════════════════════════════════════════════════════════════════════════
# AHR — Germany's Premier Pinot Noir (Spätburgunder) Region
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── AHR — NEW GERMAN REGION ──")
r_ahr = R(
    "Ahr",
    "Germany",
    "wine",
    designation_type="QbA",
    designation_name="Ahr Qualitätswein bestimmter Anbaugebiete",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "The Ahr is Germany's most celebrated Spätburgunder (Pinot Noir) region — a narrow, south-facing "
        "river valley carved through volcanic slate and greywacke, 50km south of Cologne. Despite being "
        "Germany's smallest quality wine region (600 hectares), the Ahr produces Pinot Noir of extraordinary "
        "elegance and mineral depth: the volcanic slate terroir provides the natural drainage and heat "
        "retention that Pinot Noir requires, while the steep south-facing valley sides moderate the "
        "continental climate. Meyer-Näkel, the region's most celebrated producer, helped establish the Ahr "
        "as Germany's answer to Chambolle-Musigny — producing Spätburgunder that rivals Burgundy for "
        "delicacy and mineral precision."
    ),
    key_producers="Meyer-Näkel, J.J. Adeneuer, Kreuzberg, Stodden, Deutzerhof, Jean Stodden",
    historical_context=(
        "The Ahr has been cultivating vines since Roman times — the steep slate slopes were ideal for "
        "early viticulture. Red wine dominated the region throughout its history: Spätburgunder has been "
        "planted here since the 19th century, but it was Werner Näkel and his daughters at Meyer-Näkel "
        "who elevated the Ahr to international attention in the 1980s-90s with Pinot Noir of genuine "
        "Burgundian character. The region suffered devastating floods in July 2021 (Ahrtal flood disaster) "
        "that destroyed much of the valley infrastructure, but producers are rebuilding with remarkable determination."
    )
)

print("\n  Adding Ahr vintages...")
VIN(r_ahr, 2016, 88, "very_good",
    "Excellent vintage for Ahr Spätburgunder — warm, long summer with good ripeness. "
    "Classic elegant Pinot Noir with red berry intensity and slate mineral.",
    price_trajectory="stable")
VIN(r_ahr, 2017, 94, "exceptional",
    "Exceptional Ahr vintage — perfect Spätburgunder season with extraordinary mineral precision. "
    "Wines of Burgundy-level elegance and long-term aging potential. Best recent vintage.",
    price_trajectory="rising")
VIN(r_ahr, 2018, 90, "excellent",
    "Hot, dry vintage producing rich, concentrated Spätburgunder. Powerful wines that will "
    "need extended cellaring; less classic elegance but considerable depth.",
    price_trajectory="stable")
VIN(r_ahr, 2019, 88, "very_good",
    "Good season despite heat. Elegant Pinot Noir with good freshness preserved by "
    "the Ahr Valley's moderate temperatures. Good medium-term aging wines.",
    price_trajectory="stable")
VIN(r_ahr, 2022, 86, "very_good",
    "Post-flood recovery vintage. The region's resilience demonstrated: good Spätburgunder "
    "despite reduced production from rebuilding vineyards. Positive trajectory.",
    price_trajectory="rising")

print("\n── MEYER-NÄKEL (Ahr) ──")
p_nakel = P(
    "Weingut Meyer-Näkel",
    "winery", r_ahr, "Germany",
    production_philosophy="Germany's premier Spätburgunder producer: three sisters making Ahr Pinot Noir with Burgundian precision and extraordinary regional authenticity",
    philosophy_description=(
        "Weingut Meyer-Näkel is Germany's most celebrated Spätburgunder producer — founded by Werner Näkel "
        "in 1980 and now run by his three daughters (Dörte, Meike, Silke) who have taken the estate to "
        "new heights of international recognition. Their 18 hectares of steep Ahr valley vineyards — on "
        "blue Devon Slate (Devonschiefer) soils at 150-300m altitude — produce Pinot Noir of extraordinary "
        "elegance and mineral precision. The estate's flagship Spätburgunder Goldschatz (Grosses Gewächs) "
        "is Germany's most allocated Pinot Noir — made with whole-cluster fermentation, indigenous yeasts, "
        "and 16 months aging in 30% new French Burgundy oak. Production under 5,000 bottles annually."
    ),
    reputation_narrative=(
        "Meyer-Näkel is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Decanter as Germany's "
        "most important Spätburgunder producer — their Goldschatz Grosses Gewächs consistently scores 94-98 "
        "and is placed alongside Burgundy premier cru wines for elegance and mineral complexity. "
        "The estate was awarded Wine Advocate's German Winery of the Year 2019. The three Näkel sisters' "
        "commitment to rebuilding the Ahr valley after the 2021 flood disaster has been internationally "
        "recognised as a model of wine community resilience."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_nakel = PROD(
    "Meyer-Näkel Spätburgunder Grosses Gewächs Ahr",
    "wine_still", p_nakel, r_ahr, "Germany",
    subcategory="pinot_noir_ahr",
    description=(
        "Meyer-Näkel's Spätburgunder Grosses Gewächs is Germany's most important Pinot Noir: from steep "
        "blue Devon Slate vineyards in the Ahr Valley, made with whole-cluster fermentation and indigenous "
        "yeasts. Pale ruby with extraordinary aromatic complexity: red cherry, violet, dried rose, volcanic "
        "slate mineral, and a haunting spice from whole-cluster inclusion. The wine has Chambolle-Musigny's "
        "delicacy combined with the Ahr's distinctive volcanic mineral spine. Requires 8-15 years' aging. "
        "Very limited production; one of Germany's most allocated wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_nakel,
    "Roasted pigeon breast with sour cherry and beet",
    "complement", "established", "main",
    "Meyer-Näkel Spätburgunder's delicate Ahr Pinot character and violet-cherry aromatics "
    "achieves a compelling Burgundian pairing with roasted pigeon — the game bird's richness "
    "is elevated rather than overwhelmed by the wine's elegant structure. Sour cherry amplifies "
    "the Pinot's primary fruit character; beetroot bridges the wine's earthy slate mineral "
    "dimension. A pairing that positions German Spätburgunder at the international Pinot fine dining table.")
PAIR(prod_nakel,
    "Mushroom tart with Comté and fresh herbs",
    "complement", "classic", "starter",
    "Meyer-Näkel's whole-cluster Spätburgunder complexity and slate mineral character achieves "
    "an elegant match with a mushroom tart — the wine's earth-spice dimension amplifies the "
    "mushroom's umami depth; Comté's nutty character bridges the wine's whole-cluster aromatic "
    "complexity; fresh herbs echo the Pinot's aromatic freshness. A starter pairing that showcases "
    "Ahr Spätburgunder's Burgundian versatility.")

print("\n── J.J. ADENEUER (Ahr) ──")
p_adeneuer = P(
    "Weingut J.J. Adeneuer",
    "winery", r_ahr, "Germany",
    production_philosophy="Historic Ahr estate: old-vine Spätburgunder from the Großes Gewächs site Frühmesse demonstrating the Ahr's oldest and most structured Pinot Noir terroir",
    philosophy_description=(
        "Weingut J.J. Adeneuer is one of the Ahr's oldest wine estates — founded in 1850 by the Adeneuer "
        "family in Bad Neuenahr-Ahrweiler. The estate holds 10 hectares of steep Ahr valley vineyards "
        "including prime parcels in the Frühmesse (Großes Gewächs) and Burggarten sites on ancient "
        "Devonian slate. Their No.1 Spätburgunder (from the Frühmesse GG site) is made with minimal "
        "intervention: indigenous yeasts, 30% whole-cluster, and 18 months in used French Burgundy barrique. "
        "The estate's approach emphasises terroir over winemaking technique — producing Spätburgunder of "
        "quiet power, structure, and extraordinary aging potential that distinguishes it from Meyer-Näkel's "
        "more approachable aromatic style."
    ),
    reputation_narrative=(
        "J.J. Adeneuer's Spätburgunder Frühmesse GG is cited by Jancis Robinson and the German wine press "
        "(Weinwirtschaft, Gault & Millau Weinguide) as one of the Ahr's most structured and age-worthy "
        "expressions — a wine of unusual power and mineral depth for the typically elegant Ahr style. "
        "Scoring 90-94 regularly, the estate demonstrates that the Ahr's full range extends from "
        "Meyer-Näkel's aromatic delicacy to Adeneuer's more structured, Gevrey-like character."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_adeneuer = PROD(
    "J.J. Adeneuer Spätburgunder No.1 Frühmesse Ahr",
    "wine_still", p_adeneuer, r_ahr, "Germany",
    subcategory="pinot_noir_ahr",
    description=(
        "J.J. Adeneuer's No.1 Spätburgunder is one of the Ahr's most structured wines: from the Frühmesse "
        "Großes Gewächs site on blue Devon Slate, made with 30% whole-cluster and indigenous yeasts. "
        "Medium-deep ruby with red cherry, plum, graphite, spice, and the Ahr's characteristic "
        "volcanic slate mineral. The wine has more structure and tannin than Meyer-Näkel's more aromatic "
        "style — a Pinot with the architecture of Gevrey-Chambertin rather than Chambolle-Musigny. "
        "Requires 8-12 years' aging for full expression."
    ),
    price_tier="premium"
)
PAIR(prod_adeneuer,
    "Duck confit with lentils du Puy and mustard vinaigrette",
    "complement", "established", "main",
    "J.J. Adeneuer No.1's structured Ahr Spätburgunder character and graphite mineral finds "
    "a compelling pairing with duck confit — the wine's firmer tannin structure supports the "
    "duck's rendered fat richness while the red cherry amplifies the mustard vinaigrette's acidity. "
    "Lentils du Puy provide earthy mineral depth that echoes the wine's volcanic slate character. "
    "A pairing of German Pinot at its most structured and food-compatible.")
PAIR(prod_adeneuer,
    "Venison tartare with pickled mushrooms and juniper oil",
    "complement", "established", "starter",
    "Adeneuer No.1's structured Spätburgunder and graphite mineral character achieves an elegant "
    "match with venison tartare — the raw game's intensity is met by the wine's firm Pinot structure; "
    "pickled mushrooms bridge the wine's earthy complexity; juniper oil amplifies the wine's "
    "aromatic spice dimension. A starter pairing that positions Ahr Spätburgunder as a serious "
    "fine dining wine capable of handling the most challenging food preparations.")

# ═══════════════════════════════════════════════════════════════════════════════
# BURGENLAND — Weingut Kracher dessert wine (3rd product for region 229)
# Austria's legendary dessert wine producer
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── BURGENLAND — WEINGUT KRACHER (sweet wine, region 229) ──")
p_kracher = P(
    "Weingut Kracher",
    "winery", 229, "Austria",
    production_philosophy="Austria's most celebrated dessert wine producer: Alois Kracher's Neusiedlersee Trockenbeerenauslese — one of the world's great sweet wine traditions",
    philosophy_description=(
        "Weingut Kracher is Austria's most internationally celebrated sweet wine estate — founded by "
        "Alois Kracher Sr and elevated to global prominence by Alois Kracher Jr (1959-2007), who became "
        "the world's most recognised producer of Neusiedlersee botrytis wines. The estate's vineyards "
        "on the shores of Lake Neusiedl in Burgenland create ideal conditions for noble rot: the warm, "
        "shallow lake generates autumn mists that encourage Botrytis cinerea development on Welschriesling "
        "and Scheurebe. Kracher's numbered TBA (Trockenbeerenauslese) series represents the world's "
        "most ambitious botrytis wines outside Sauternes — produced in 11 different cuvées from "
        "different plots, varieties, and oak treatments annually."
    ),
    reputation_narrative=(
        "Weingut Kracher's Trockenbeerenauslese wines are cited by Wine Advocate (Robert Parker, Antonio "
        "Galloni), Jancis Robinson, and Decanter as among the world's greatest dessert wines. Parker awarded "
        "100 points to multiple Kracher TBAs in the 1990s and 2000s — placing them alongside Château d'Yquem "
        "and Egon Müller Trockenbeerenauslese as the world's three greatest sweet wine producers. "
        "Alois Kracher's legacy continues under his son Gerhard, who maintains the numbered TBA tradition "
        "with equal precision and passion."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_kracher = PROD(
    "Kracher Trockenbeerenauslese Cuvée Beerenauslese Burgenland",
    "wine_dessert", p_kracher, 229, "Austria",
    subcategory="sweet_welschriesling_scheurebe",
    description=(
        "Weingut Kracher's TBA Cuvée is one of Austria's most extraordinary dessert wines: botrytised "
        "Welschriesling and Scheurebe from the shores of Lake Neusiedl in Burgenland, produced only "
        "in exceptional botrytis vintages. Luminous amber-gold with extraordinary concentration: "
        "apricot jam, honey, ginger, orange blossom, saffron, and a stunning natural acid "
        "that provides balance against the near-overwhelming sweetness. The wine's residual sugar "
        "can exceed 300g/L while the acidity prevents any cloying sensation. Ages magnificently "
        "for 30-50+ years — one of the world's most long-lived dessert wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_kracher,
    "Foie gras parfait with sauternes jelly and brioche",
    "complement", "classic", "starter",
    "Kracher TBA's concentrated apricot honey and saffron complexity achieves one of fine dining's "
    "great sweet wine pairings — the classic foie gras and Sauternes-style TBA combination. "
    "The wine's intense sweetness is the perfect counterpoint to foie gras's fat richness; "
    "sauternes jelly bridges wine and food; brioche provides the buttery vehicle. A pairing "
    "of Austrian dessert wine tradition at its most luxurious.")
PAIR(prod_kracher,
    "Roquefort with honeycomb and toasted walnuts",
    "contrast", "classic", "cheese",
    "Kracher TBA's extraordinary sweetness and saffron-apricot complexity achieves the classic "
    "sweet wine-blue cheese contrast at its most extreme — Roquefort's aggressive salt and pungency "
    "is perfectly balanced by the TBA's intense sweetness. Honeycomb amplifies the wine's "
    "natural honey character; walnuts bridge the contrast with earthy bitterness. "
    "A pairing of complete contrast achieving the highest harmony.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T19 Batch 1 complete.")
print("  Constantia: new region, 5 vintages, 2 producers (Klein Constantia, Groot Constantia), 2 products, 4 pairings")
print("  Ahr: new region, 5 vintages, 2 producers (Meyer-Näkel, J.J. Adeneuer), 2 products, 4 pairings")
print("  Burgenland: 1 new producer (Kracher), 1 product (TBA), 2 pairings")
