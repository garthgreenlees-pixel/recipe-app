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
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Puligny-Montrachet ─────────────────────────────────────────────
print("\n=== Region 1: Puligny-Montrachet ===")
r1 = R("Puligny-Montrachet", "France", "wine",
    designation_type="AOC",
    designation_name="Puligny-Montrachet AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="The white wine capital of Burgundy and arguably the world, sharing the Montrachet Grand Cru vineyard with Chassagne-Montrachet. Puligny's Chardonnays are defined by extraordinary precision, mineral tension, and a translucent golden purity that no other region can replicate. The village holds portions of Chevalier-Montrachet and Bâtard-Montrachet alongside a constellation of exceptional premier crus.",
    key_producers="Leflaive, Carillon, Sauzet, Ramonet, Coche-Dury",
    historical_context="Montrachet was so revered that Alexandre Dumas declared it should be drunk only kneeling, with head bowed; Thomas Jefferson reportedly ordered cases from Versailles in 1787.")

for yr, qd, pt in [
    (2023, "very_good", "rising"), (2022, "excellent", "rising"),
    (2021, "excellent", "stable"), (2020, "exceptional", "stable"), (2019, "very_good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Domaine Leflaive", "winery", r1, "France",
    production_philosophy="biodynamic",
    philosophy_description="Leflaive is the benchmark estate for white Burgundy — biodynamically farmed Grand Crus Chevalier-Montrachet, Bâtard-Montrachet, Bienvenues-Bâtard-Montrachet, and Le Montrachet itself. Under Anne-Claude Leflaive's leadership, the estate pioneered biodynamics in Burgundy.",
    reputation_narrative="Universally cited as Burgundy's greatest white wine estate; Chevalier-Montrachet is a benchmark of the Côte de Beaune.",
    price_positioning="ultra_premium")

prod1b_id = P("Domaine Etienne Sauzet", "winery", r1, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Sauzet's village and premier cru Puligny wines are paragons of the appellation's style — mineral, precise, and long-lived, crafted from old vines across the finest village and premier cru sites.",
    reputation_narrative="One of Puligny's most reliable quality estates; premier crus Combettes and Perrières are among the finest white Burgundies at their level.",
    price_positioning="ultra_premium")

prod1a, new1a = PROD("Domaine Leflaive Puligny-Montrachet Les Pucelles 1er Cru", "wine_still", prod1a_id, r1, "France",
    subcategory="Chardonnay",
    description="Les Pucelles is Puligny's most famous premier cru for Leflaive — adjacent to Chevalier-Montrachet with Grand Cru-adjacent complexity: white flowers, lemon cream, crushed limestone, and extraordinary length.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Dover sole meunière with capers and lemon brown butter", "complement", "classic", "fish_course",
         "The purest expression of white Burgundy with white fish — acid, cream, and mineral in perfect alignment.")
    PAIR(prod1a, "White asparagus with hollandaise and truffled egg yolk", "elevate", "classic", "starter",
         "Spring asparagus and biodynamic Chardonnay share the same mineral, floral, springtime vocabulary.")
    PAIR(prod1a, "Langoustine with cauliflower cream and Oscietra caviar", "elevate", "established", "starter",
         "Luxury marine pairing — the wine's precision and salinity mirror both shellfish and caviar.")
    PAIR(prod1a, "Vacherin Mont d'Or warm with garlic and white wine", "bridge", "classic", "cheese",
         "Classic Alpine fondue-adjacent pairing — rich melted cheese with crisp white Burgundy is a seasonal archetype.")

prod1b, new1b = PROD("Etienne Sauzet Puligny-Montrachet Village", "wine_still", prod1b_id, r1, "France",
    subcategory="Chardonnay",
    description="Sauzet's village Puligny is a benchmark for the appellation at the entry level — mineral, precise, with citrus blossom, white peach, and a long chalky finish that reflects the commune's limestone bedrock.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Moules marinières with white wine and shallots", "complement", "classic", "starter",
         "Classic French steamed mussels with a village white Burgundy — the wine that cooks the dish, also in the glass.")
    PAIR(prod1b, "Scallop with cauliflower purée and hazelnut beurre noisette", "complement", "classic", "starter",
         "Puligny's nutty-mineral character mirrors the hazelnut butter while the acid lifts the scallop's sweetness.")
    PAIR(prod1b, "Roast chicken with garlic cream and tarragon", "complement", "classic", "main",
         "The quintessential French lunch pairing — village white Burgundy with simple roasted chicken.")
    PAIR(prod1b, "Brillat-Savarin triple cream with lemon thyme", "complement", "established", "cheese",
         "Opulent triple cream with mineral Chardonnay — fat and acid in perfect equilibrium.")

# ── Region 2: Meursault ──────────────────────────────────────────────────────
print("\n=== Region 2: Meursault ===")
r2 = R("Meursault", "France", "wine",
    designation_type="AOC",
    designation_name="Meursault AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Burgundy's most celebrated village for white wine character at scale — Meursault Chardonnay is defined by its distinctive hazelnut, toasted almond, honey, and rich golden-fruit character alongside limestone-driven minerality. Unlike Puligny's razor precision, Meursault is rounder and more generous in texture. Perrières, Charmes, and Genevrières are the finest premier crus.",
    key_producers="Coche-Dury, Roulot, Comtes Lafon, Bouchard Père & Fils, Matrot",
    historical_context="Meursault's reputation predates its Côte de Beaune neighbours — the village was exporting wine to the English market in the 14th century; the annual Paulée de Meursault is one of Burgundy's great harvest celebrations.")

for yr, qd, pt in [
    (2023, "very_good", "rising"), (2022, "excellent", "rising"),
    (2021, "excellent", "stable"), (2020, "exceptional", "stable"), (2019, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Domaine Roulot", "winery", r2, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Jean-Marc Roulot produces Meursault's most precise and sought-after wines — his Perrières, Charmes, Genevrières, and village cuvées command cult status for their crystalline mineral purity and extraordinary aging potential.",
    reputation_narrative="Arguably Meursault's finest domaine today; Perrières allocation has collapsed to a tiny global waiting list.",
    price_positioning="ultra_premium")

prod2b_id = P("Comtes Lafon", "winery", r2, "France",
    production_philosophy="biodynamic",
    philosophy_description="Dominique Lafon's estate is Meursault's most complete — biodynamically farmed holdings across all the finest premier crus plus a parcel of Le Montrachet Grand Cru, with wines of extraordinary texture, richness, and mineral depth.",
    reputation_narrative="One of Burgundy's definitive estates for white wine; Montrachet parcel makes among the world's most coveted bottles.",
    price_positioning="ultra_premium")

prod2a, new2a = PROD("Domaine Roulot Meursault Perrières 1er Cru", "wine_still", prod2a_id, r2, "France",
    subcategory="Chardonnay",
    description="Roulot's Perrières is perhaps the most sought-after white Burgundy at the premier cru level — extraordinary mineral tension, golden citrus, flint, and toasted almonds with decades of aging potential from the appellation's finest site.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Lobster thermidor with tarragon and gruyère gratin", "elevate", "classic", "main",
         "Meursault's richness and length match lobster's luxury while Perrières' mineral precision cuts the cream.")
    PAIR(prod2a, "Roasted scallops with truffle beurre blanc and samphire", "complement", "classic", "starter",
         "Marine minerals mirror and amplify the wine's flint and oceanic depth in a luxury starter.")
    PAIR(prod2a, "Chicken roasted in cream with morels and Vin Jaune", "bridge", "classic", "main",
         "The classic Jura preparation echoes Meursault's toasted nut and cream character through the sauce.")
    PAIR(prod2a, "Comté 24-month with truffle and toasted bread", "complement", "classic", "cheese",
         "Aged Comté's hazelnut and long-ferment complexity mirrors Meursault's signature toasted almond note.")

prod2b, new2b = PROD("Comtes Lafon Meursault Charmes 1er Cru", "wine_still", prod2b_id, r2, "France",
    subcategory="Chardonnay",
    description="Lafon's Charmes is the most generous and hedonistic of Meursault's premier crus — lush, rounded, and honey-rich with a silky texture from biodynamic viticulture and old vines on the richest soils of the appellation.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Sautéed foie gras with peach compote and brioche", "complement", "established", "starter",
         "Charmes' honey and richness bridge with foie's fat while Chardonnay's acidity lifts and frames.")
    PAIR(prod2b, "Butter-poached Maine lobster with corn purée", "complement", "classic", "main",
         "Lafon's Charmes and lobster share a mutual opulence — corn's sweetness echoes the wine's fruit.")
    PAIR(prod2b, "Roasted halibut with celeriac cream and pickled grapes", "complement", "established", "fish_course",
         "Meaty fish with rich cream sauce and acidic grape garnish mirrors the wine's structure and depth.")
    PAIR(prod2b, "Soumaintrain aged cheese with local honey", "bridge", "established", "cheese",
         "Burgundian washed-rind cheese with floral honey finds a bridge in Charmes' aromatic richness.")

# ── Region 3: Côte de Beaune ─────────────────────────────────────────────────
print("\n=== Region 3: Corton-Charlemagne ===")
r3 = R("Corton-Charlemagne", "France", "wine",
    designation_type="AOC",
    designation_name="Corton-Charlemagne AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Burgundy's largest and most powerful white Grand Cru, covering the upper slopes of the Corton hill shared between Aloxe-Corton, Pernand-Vergelesses, and Ladoix-Serrigny. Corton-Charlemagne Chardonnay is more powerful and structured than Puligny or Meursault — mineral, spicy, and built for long aging. The legend traces back to Emperor Charlemagne planting white vines to keep his beard clean.",
    key_producers="Bonneau du Martray, Louis Latour, Coche-Dury, Faiveley",
    historical_context="Charlemagne reportedly ordered white vines planted on the south-facing slopes of the Corton hill in the 9th century; the name Corton-Charlemagne preserves this medieval legend across twelve centuries.")

for yr, qd, pt in [
    (2022, "exceptional", "rising"), (2021, "excellent", "stable"),
    (2020, "exceptional", "stable"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Bonneau du Martray", "winery", r3, "France",
    production_philosophy="biodynamic",
    philosophy_description="The sole estate dedicated exclusively to Corton-Charlemagne (and a parcel of red Corton), Bonneau du Martray produces the most structured and age-worthy expressions of this Grand Cru. Now under Standish family ownership with biodynamic certification.",
    reputation_narrative="The reference estate for Corton-Charlemagne; the Grand Cru requires a decade to open and rewards 30-year cellaring.",
    price_positioning="ultra_premium")

prod3b_id = P("Louis Latour", "winery", r3, "France",
    production_philosophy="traditional",
    philosophy_description="The most important négociant-éleveur in the Corton appellation, Louis Latour holds the largest single ownership of Corton-Charlemagne among any producer and has championed the Grand Cru internationally for over a century.",
    reputation_narrative="Iconic Beaune négociant; Corton-Charlemagne is their signature prestige bottling.",
    price_positioning="premium")

prod3a, new3a = PROD("Bonneau du Martray Corton-Charlemagne Grand Cru", "wine_still", prod3a_id, r3, "France",
    subcategory="Chardonnay",
    description="The definitive Corton-Charlemagne — from a continuous monopole parcel of 9.5 hectares on the upper hill. Powerful, spicy, and mineral with extraordinary aging potential; showing its best at 15-25 years.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Roasted turbot on the bone with beurre blanc and capers", "complement", "classic", "fish_course",
         "The classic pairing for powerful white Burgundy — turbot's dense flesh requires Grand Cru weight and acid.")
    PAIR(prod3a, "Spit-roasted Bresse capon with truffle and cream", "elevate", "classic", "main",
         "Corton-Charlemagne's power and depth match Bresse chicken's luxury and the cream sauce's richness.")
    PAIR(prod3a, "Braised veal cheek with a Chablis cream and chanterelles", "bridge", "established", "main",
         "Veal and white Burgundy share a classic Côte de Beaune connection; chanterelles echo the wine's earthiness.")
    PAIR(prod3a, "Époisses with walnut bread and dried apricots", "contrast", "established", "cheese",
         "Corton's power handles Époisses' extreme pungency while dried apricot bridges the wine's stone-fruit note.")

prod3b, new3b = PROD("Louis Latour Corton-Charlemagne Grand Cru", "wine_still", prod3b_id, r3, "France",
    subcategory="Chardonnay",
    description="Latour's Corton-Charlemagne is the most commercially available expression of this Grand Cru — a reliable, spicy, mineral Chardonnay with honey, citrus, and toasted bread notes from significant vineyard holdings on the Corton hill.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Grilled lobster with drawn butter and lemon", "complement", "classic", "main",
         "Corton-Charlemagne's power and mineral depth match lobster's oceanic richness with ease.")
    PAIR(prod3b, "Sole Véronique with grapes and cream", "bridge", "classic", "fish_course",
         "Classic French preparation — the grape garnish bridges with the wine's Chardonnay character.")
    PAIR(prod3b, "Gratinated oysters with herb butter and Gruyère", "complement", "established", "starter",
         "Warm, rich oysters suit the Grand Cru's weight and spice; cheese echoes the wine's toasted notes.")
    PAIR(prod3b, "Aged Mimolette with pear and walnut", "complement", "suggested", "cheese",
         "Hard aged cheese with pear and nut mirrors Corton-Charlemagne's rich, spicy, and nutty character.")

# ── Region 4: Rhône Valley North — Crozes-Hermitage ─────────────────────────
print("\n=== Region 4: Crozes-Hermitage ===")
r4 = R("Crozes-Hermitage", "France", "wine",
    designation_type="AOC",
    designation_name="Crozes-Hermitage AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The largest appellation of the Northern Rhône, surrounding the famous Hermitage hill on all sides. Crozes-Hermitage produces both red Syrah and white Marsanne/Roussanne wines from a range of soils — granite hillsides, river terraces, and clay plains — offering significant variation in style. At its best from granite sites, it approaches Hermitage quality at far more accessible prices.",
    key_producers="Chapoutier, Jaboulet, Tardieu-Laurent, Yann Chave, Delas",
    historical_context="The appellation was created in 1937, encompassing eleven communes around Tain-l'Hermitage; the name derives from the legend of a crusader knight who built a hermitage on the famous hill in the 13th century.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Yann Chave", "winery", r4, "France",
    production_philosophy="terroir_focused",
    philosophy_description="One of Crozes-Hermitage's brightest stars, Yann Chave produces Syrah and Marsanne of exceptional quality from granite and clay terraces — his Le Rouvre cuvée rivals many Hermitage expressions in depth and complexity.",
    reputation_narrative="Consistently cited as Crozes-Hermitage's most quality-focused family estate; Le Rouvre commands near-Hermitage prices.",
    price_positioning="premium")

prod4b_id = P("Alain Graillot", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="Alain Graillot transformed Crozes-Hermitage's reputation in the 1980s — his benchmark Syrahs from the La Guiraude parcel and village wine demonstrated that granite-sited Crozes could rival Hermitage for expression and longevity.",
    reputation_narrative="The founding father of modern Crozes-Hermitage quality; wines exported globally by négociant Marc Chapoutier from the beginning.",
    price_positioning="mid_range")

prod4a, new4a = PROD("Yann Chave Crozes-Hermitage Le Rouvre", "wine_still", prod4a_id, r4, "France",
    subcategory="Syrah",
    description="Chave's top cuvée from older-vine parcels on granite terraces — concentrated, peppery, and smoky Syrah with dark olive, bacon, and violet notes; the most compelling Crozes at the prestige level.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Grilled lamb chops with black olive tapenade and rosemary", "complement", "classic", "main",
         "Northern Rhône Syrah and lamb is the classic Provençal alliance — tapenade echoes the wine's olive character.")
    PAIR(prod4a, "Wild boar sausage with lentils du Puy and mustard", "complement", "established", "main",
         "Rustic game sausage with structured Syrah — Northern Rhône's traditional table in a single pairing.")
    PAIR(prod4a, "Smoked duck breast with cherry reduction and hazelnut", "bridge", "established", "main",
         "Smoke and dark fruit in both dish and wine; Syrah's violet note echoes cherry reduction.")
    PAIR(prod4a, "Saint-Marcellin at peak ripeness on walnut bread", "complement", "established", "cheese",
         "Rhône Valley's tiny local cheese — creamy, funky Saint-Marcellin with peppery Syrah is a regional archetype.")

prod4b, new4b = PROD("Alain Graillot Crozes-Hermitage Rouge", "wine_still", prod4b_id, r4, "France",
    subcategory="Syrah",
    description="Graillot's foundational Crozes-Hermitage rouge — peppery, olive-tinged Syrah with excellent structure and a signature Northern Rhône smokiness; the wine that put Crozes-Hermitage on the international map in the late 1980s.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Côtelettes d'agneau grillées with herbes de Provence", "complement", "classic", "main",
         "The quintessential Northern Rhône pairing — grilled lamb with Provençal herbs and a classic Syrah.")
    PAIR(prod4b, "Grilled beef entrecôte with pan jus and green peppercorn", "complement", "established", "main",
         "Peppercorn in the preparation echoes Syrah's characteristic white pepper spice in a simple, satisfying pairing.")
    PAIR(prod4b, "Charcuterie board with dried sausages and olives", "complement", "established", "casual",
         "A Rhône Valley bistro pairing — cured meats and olives with earthy, smoky Syrah is classic Southern France.")
    PAIR(prod4b, "Tomme de Savoie with dried cranberry", "complement", "established", "cheese",
         "Alpine pressed cheese's milk simplicity contrasts with Syrah's dark fruit and earthy complexity.")

# ── Region 5: Roussillon ─────────────────────────────────────────────────────
print("\n=== Region 5: Roussillon ===")
r5 = R("Roussillon", "France", "wine",
    designation_type="AOC",
    designation_name="Roussillon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's southernmost wine region at the foot of the Pyrenees bordering Spain, blessed with 300 days of sunshine, Mediterranean heat, tramontane winds, and extraordinarily old Grenache, Carignan, and Mourvèdre vines. The region is experiencing a renaissance driven by a generation of natural wine producers discovering centenarian vines on slate, granite, and schist soils that produce wines of remarkable concentration and authenticity.",
    key_producers="Gauby, Cazes, Mas Amiel, Les Terres de Fagayra, Clos du Moulin aux Moines",
    historical_context="Roussillon was part of Catalonia until 1659 when the Treaty of the Pyrenees ceded it to France; Catalan culture persists in language, food, and viticulture — the region produces France's greatest Grenache-based fortified wines in Maury and Banyuls.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Domaine Gauby", "winery", r5, "France",
    production_philosophy="biodynamic",
    philosophy_description="Gérard Gauby is the godfather of Roussillon's quality renaissance — his biodynamically farmed old Grenache and Carignan vines on schist and granite soils produce wines of extraordinary depth, freshness, and terroir expression from Les Calcinaires and Vieilles Vignes cuvées.",
    reputation_narrative="The defining estate of modern Roussillon; Gauby's influence has transformed the entire region's approach to quality.",
    price_positioning="premium")

prod5b_id = P("Mas Amiel", "winery", r5, "France",
    production_philosophy="traditional",
    philosophy_description="Mas Amiel is the iconic domaine of Maury, producing France's most celebrated fortified red wine through a unique outdoor oxidative aging process in glass bonbonnes exposed to the summer heat of the Agly Valley.",
    reputation_narrative="The definitive producer of Maury fortified wine; Vintage Maury is a benchmark of French vin doux naturel.",
    price_positioning="premium")

prod5a, new5a = PROD("Domaine Gauby Vieilles Vignes Rouge", "wine_still", prod5a_id, r5, "France",
    subcategory="Grenache-Carignan Blend",
    description="Gauby's pinnacle dry red — centenarian-vine Grenache and Carignan from schist and granite soils, aged in large old foudres. Concentrated, wild, and mineral with a unique terroir expression from some of France's oldest vines.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Catalan-braised short ribs with olives, capers, and anchovies", "complement", "classic", "main",
         "Cross-border culinary heritage — Catalan preparation with Roussillon wine sharing the same cultural identity.")
    PAIR(prod5a, "Grilled octopus with smoked paprika and romesco", "complement", "established", "main",
         "Mediterranean charred seafood with a structured Southern French red — Catalan tradition on both sides.")
    PAIR(prod5a, "Lamb belly with thyme, garlic, and black olives", "complement", "established", "main",
         "Garrigues-scented slow lamb with Grenache-dominant wine — Languedoc's defining pairing template.")
    PAIR(prod5a, "Aged Manchego with fig jam and almonds", "complement", "established", "cheese",
         "Cross-Pyrenees cheese pairing — Spanish Manchego with French Roussillon wine sharing Catalan roots.")

prod5b, new5b = PROD("Mas Amiel Vintage Maury", "wine_fortified", prod5b_id, r5, "France",
    subcategory="Grenache Noir",
    description="The definitive expression of Maury — 100% Grenache Noir aged for one year in glass bonbonnes under the southern sun, producing a fortified wine of extraordinary concentration: dark chocolate, figs, black cherry, and coffee with exceptional freshness.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Valrhona dark chocolate fondant with salted caramel", "complement", "classic", "dessert",
         "The definitive fortified wine and chocolate pairing — both share dark fruit and bitter chocolate character.")
    PAIR(prod5b, "Roquefort with honey and toasted walnuts", "complement", "classic", "cheese",
         "Salty, aged Roquefort with rich Maury — France's great blue cheese meets its most powerful dessert wine.")
    PAIR(prod5b, "Duck liver pâté with black cherry chutney", "bridge", "established", "starter",
         "Fortified Grenache's fruit concentration and slight sweetness bridge the rich liver and cherry accompaniment.")
    PAIR(prod5b, "Figues rôties with lavender honey ice cream", "complement", "established", "dessert",
         "Maury's fig and dried-fruit character amplified by roasted fresh figs with the region's aromatic lavender.")

# ── Counts ────────────────────────────────────────────────────────────────────
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
cur.close()
conn.close()
