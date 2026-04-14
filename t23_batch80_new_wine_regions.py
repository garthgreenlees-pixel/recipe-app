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
        return (row[0], False)
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return (pid, True)

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 80 ──────────────────────────────────────────────────────────────────
# Regions: Virginia, Irouléguy, Thrace (Bulgaria), Rheinhessen, Dão (depth)

# ── Region 1: Virginia ────────────────────────────────────────────────────────
print("\n=== Region 1: Virginia ===")
r1 = R("Virginia", "USA", "wine",
    designation_type="AVA",
    designation_name="Virginia AVA",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="USA's eastern seaboard wine region producing elegant Viognier, Petit Verdot, Cabernet Franc and Chardonnay; the state's continental climate and granite-clay soils give wines distinctive freshness and aromatic precision.",
    key_producers="Barboursville Vineyards, RdV Vineyards, Linden Vineyards, Boxwood Estate, King Family Vineyards",
    historical_context="Thomas Jefferson planted Virginia's first European vines at Monticello in 1807 and predicted it would become a great wine state; his vision is being realised 200 years later with international recognition for Viognier and Petit Verdot."
)
VIN(r1, 2022, "excellent", "rising", "Exceptional Virginia vintage; Viognier and Petit Verdot both showed extraordinary character and structure.")
VIN(r1, 2021, "very_good", "stable", "Good quality; wines show the state's characteristic freshness from Atlantic maritime influence.")
VIN(r1, 2020, "good", "stable", "Consistent vintage; reliable, food-friendly wines across the state's diverse AVAs.")
VIN(r1, 2019, "excellent", "rising", "Benchmark year; RdV Renard and Barboursville Paxxito both earned outstanding recognition.")
VIN(r1, 2018, "very_good", "stable", "Good growing season; Viognier particularly successful with aromatic intensity and good acidity.")

p1a = P("RdV Vineyards", "winery", r1, "USA",
    production_philosophy="terroir_expression",
    philosophy_description="Rutger de Vink's Delaplane estate producing Virginia's most internationally acclaimed and Bordeaux-inspired reds from granite-clay slopes; RdV Renard and Lost Mountain are the state's finest wines.",
    reputation_narrative="RdV Vineyards is Virginia's most critically acclaimed estate; Renard has been compared favourably to classified Bordeaux and has generated Virginia's highest international wine scores.",
    price_positioning="ultra_premium")
prod1a, new1a = PROD("RdV Vineyards Renard", "wine_still", p1a, r1, "USA",
    subcategory="Cabernet Franc blend",
    description="Virginia's most acclaimed wine: Cabernet Franc-dominant Bordeaux blend — blackcurrant, graphite, violet, cedar and the distinctive freshness of Virginia granite-clay; built for 15+ years of ageing.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Rack of lamb with herbs de Provence and flageolet beans", "complement", "classic", "main", "Classic Bordeaux pairing; Virginia Cabernet Franc's violet and cedar mirror the herb-crusted lamb.")
    PAIR(prod1a, "Dry-aged Wagyu ribeye with bone marrow butter", "complement", "classic", "main", "Ultra-premium beef for an ultra-premium Virginia red; bone marrow amplifies the wine's richness.")
    PAIR(prod1a, "Aged Virginia Gouda (Caromont Farm) with quince", "complement", "established", "cheese", "Virginia artisan cheese with Virginia's finest wine; quince bridges the wine's cassis and the cheese's caramel.")
    PAIR(prod1a, "Duck breast with cherry reduction and roasted baby beet", "complement", "established", "main", "Violet and dark cherry in the wine mirror both the cherry sauce and the Cabernet Franc's natural affinity with duck.")

p1b = P("Barboursville Vineyards", "winery", r1, "USA",
    production_philosophy="traditional",
    philosophy_description="Virginia's most historically significant Italian-owned estate (Zonin family), producing benchmark Viognier and the iconic Octagon Bordeaux blend since 1976 from Thomas Jefferson's historic Piedmont County.",
    reputation_narrative="Barboursville is Virginia's most important wine estate historically and one of its finest producers; Octagon is Virginia's most consistently acclaimed red and Paxxito its most celebrated sweet wine.",
    price_positioning="premium")
prod1b, new1b = PROD("Barboursville Viognier Reserve", "wine_still", p1b, r1, "USA",
    subcategory="Viognier",
    description="Virginia's benchmark Viognier: peach blossom, apricot, ginger, white pepper and the distinctive floral intensity of the variety; textured, dry and showing Virginia's particular gift for aromatic whites.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Seared sea scallops with peach beurre blanc and tarragon", "complement", "classic", "fish_course", "Peach in the wine mirrors the beurre blanc; Viognier's richness aligns with scallop's sweet fat.")
    PAIR(prod1b, "Grilled shrimp with mango, chilli and lime", "complement", "established", "starter", "Tropical Viognier and tropical flavour combinations; mango bridges the wine's stone fruit character.")
    PAIR(prod1b, "Massaman curry with chicken and sweet potato", "complement", "classic", "main", "Aromatic curry and floral Viognier; the wine's peach and ginger mirror the curry's aromatic complexity.")
    PAIR(prod1b, "Époisses with fig preserves and walnut bread", "complement", "established", "cheese", "Pungent washed-rind and aromatic Viognier is a classic bold contrast; fig bridges fruit to cheese.")

# ── Region 2: Irouléguy ───────────────────────────────────────────────────────
print("\n=== Region 2: Irouléguy ===")
r2 = R("Irouléguy", "France", "wine",
    designation_type="AOC",
    designation_name="Irouléguy AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's smallest and most remote wine AOC in the Basque Pyrenees, producing reds from Tannat, Cabernet Franc and Cabernet Sauvignon alongside distinctive rosé and Gros Manseng whites; mountain wines of rugged personality.",
    key_producers="Domaine Brana, Domaine Arretxea, Domaine Etxegaraia, Bodega Arretxea",
    historical_context="Irouléguy wines were historically made by Basque monks and farmers surviving on steep terraced vineyards at up to 400m altitude; the cooperative was revived in the 1950s and today small independent estates are driving a quality renaissance."
)
VIN(r2, 2022, "excellent", "rising", "Outstanding Pyrenean vintage; Tannat of exceptional depth and Gros Manseng of great freshness.")
VIN(r2, 2021, "very_good", "stable", "Good quality; wines show the mountain's characteristic power, freshness and individuality.")
VIN(r2, 2020, "good", "stable", "Consistent vintage; reliable mountain wines with strong Basque identity.")
VIN(r2, 2019, "excellent", "rising", "Benchmark year; Domaine Arretxea and Brana both produced wines of international quality.")
VIN(r2, 2018, "very_good", "stable", "Good season; Tannat-Cabernet blend showed excellent depth and ageing potential.")

p2a = P("Domaine Arretxea", "winery", r2, "France",
    production_philosophy="biodynamic",
    philosophy_description="Michel and Thérèse Riouspeyrous's biodynamic Basque estate producing the most internationally celebrated Irouléguy wines from steep Pyrenean terraces; Haitza red and Hegoxuri white are benchmark Basque wines.",
    reputation_narrative="Domaine Arretxea is Irouléguy's most critically acclaimed estate; Haitza is considered France's finest Tannat-based wine and a benchmark for the entire appellation.",
    price_positioning="premium")
prod2a, new2a = PROD("Domaine Arretxea Haitza", "wine_still", p2a, r2, "France",
    subcategory="Tannat blend",
    description="France's finest Irouléguy red: Tannat with Cabernet Franc from biodynamic Pyrenean terraces — dark plum, blackberry, iron, violets and mountain herbs with formidable but refined tannic grip.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Pyrenean lamb with Espelette pepper and rosemary", "complement", "classic", "main", "Mountain lamb with mountain Tannat from the same Pyrenean landscape; Espelette pepper bridges both.")
    PAIR(prod2a, "Slow-cooked duck confit with cassoulet beans", "complement", "classic", "main", "Southwest France's most beloved slow-cooked preparation with its most powerful regional red.")
    PAIR(prod2a, "Grilled Iberian pork chop with piment d'Espelette aioli", "complement", "established", "main", "Rich pork and tannic Tannat; Espelette pepper's warmth echoes the wine's dark spice character.")
    PAIR(prod2a, "Ossau-Iraty (Pyrenean sheep cheese) with black cherry jam", "complement", "classic", "cheese", "The canonical Basque pairing: the region's cheese with the region's wine; cherry jam bridges both.")

p2b = P("Domaine Brana", "winery", r2, "France",
    production_philosophy="traditional",
    philosophy_description="Historic Basque family estate producing benchmark Irouléguy red and the celebrated Xuri d'Ansa white alongside a noted Armagnac and Izarra liqueur tradition.",
    reputation_narrative="Domaine Brana Xuri d'Ansa is considered the finest white wine of the Irouléguy appellation; the estate represents the Basque wine tradition's quality flagship.",
    price_positioning="mid_range")
prod2b, new2b = PROD("Domaine Brana Xuri d'Ansa Irouléguy", "wine_still", p2b, r2, "France",
    subcategory="Gros Manseng blend",
    description="Irouléguy's finest white: Gros Manseng and Petit Manseng from mountain slopes — grapefruit, white flower, dried herb, mineral and a sharp Pyrenean freshness; unique and deeply characterful.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Ventrèche (Basque cured belly pork) with Espelette-spiced lentils", "complement", "established", "main", "Rich cured pork and Gros Manseng's acidity are natural Basque partners; lentils bridge the wine's mineral edge.")
    PAIR(prod2b, "Poached sea trout with beurre blanc and herb salad", "complement", "classic", "fish_course", "Fresh mountain stream fish and Pyrenean white; herb salad bridges the wine's dried herb character.")
    PAIR(prod2b, "Basque piperade with eggs and Bayonne ham", "complement", "classic", "casual", "The Basque Country's most iconic breakfast and lunch dish with its most distinctive white wine.")
    PAIR(prod2b, "Fresh goat's cheese with Basque black cherry jam", "complement", "established", "cheese", "Tangy young chèvre and the wine's acidity; Basque cherry jam bridges the wine's stone fruit and the cheese.")

# ── Region 3: Thrace ──────────────────────────────────────────────────────────
print("\n=== Region 3: Thrace ===")
r3 = R("Thrace", "Bulgaria", "wine",
    designation_type="PDO",
    designation_name="Thracian Valley PDO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Bulgaria's premier wine region in the Thracian Plain, producing bold Mavrud, Rubin and international varieties in a warm continental climate with fertile soils; known for excellent value and increasingly serious fine wine production.",
    key_producers="Bessa Valley, Edoardo Miroglio, Villa Yustina, Domaine Boyar, Katarzyna Estate",
    historical_context="Thrace is one of wine's most ancient regions — ancient Greek and Roman writers celebrated Thracian wine; today Bulgaria produces wines that challenge Western European perceptions of quality from the east."
)
VIN(r3, 2021, "excellent", "rising", "Outstanding Thracian vintage; Mavrud and Cabernet Sauvignon of remarkable depth at exceptional value.")
VIN(r3, 2020, "very_good", "stable", "Good quality; wines show Bulgaria's improving winemaking and the Thracian Plain's reliable fruit.")
VIN(r3, 2019, "good", "stable", "Consistent vintage; reliable, full-bodied reds for early drinking at strong value.")
VIN(r3, 2018, "excellent", "rising", "Benchmark year; Bessa Valley Enira and Katarzyna Estate both drew significant critical recognition.")
VIN(r3, 2017, "very_good", "stable", "Good season; international varieties showed good structure and Bulgarian character.")

p3a = P("Bessa Valley Winery", "winery", r3, "Bulgaria",
    production_philosophy="terroir_expression",
    philosophy_description="French-owned (Stephan von Neipperg) estate producing Bulgaria's most internationally acclaimed wine — Enira — from Merlot and Syrah on Thracian Plain soils with Bordeaux-trained precision.",
    reputation_narrative="Bessa Valley Enira has earned 90+ points from Wine Spectator and Decanter; it is Bulgaria's most internationally recognised fine wine and represents the country's ambition in the global market.",
    price_positioning="premium")
prod3a, new3a = PROD("Bessa Valley Enira", "wine_still", p3a, r3, "Bulgaria",
    subcategory="Merlot blend",
    description="Bulgaria's most acclaimed wine: Merlot, Syrah and Petit Verdot from Thracian Plains — dark plum, violet, cedar, chocolate and silky Bordeaux-influenced tannins at surprisingly accessible prices.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Slow-braised lamb with aromatic vegetables and polenta", "complement", "established", "main", "Rich braised lamb and Thracian Merlot blend; the wine's dark fruit and cedar suit slow-cooked preparations.")
    PAIR(prod3a, "Grilled Bulgarian kebapche sausage with shopska salad", "complement", "classic", "main", "Bulgaria's national grilled meat with its finest Thracian red is the definitive local pairing.")
    PAIR(prod3a, "Beef and mushroom kavurma (slow-cooked stew)", "complement", "established", "main", "Bulgarian slow-cooked beef with mushroom and the wine's depth in earthy harmony.")
    PAIR(prod3a, "Kashkaval cheese (Bulgarian yellow cheese) with fig jam", "complement", "established", "cheese", "Bulgaria's most widespread cheese with its finest wine; fig jam bridges the wine's plum and the cheese's mild sweetness.")

p3b = P("Katarzyna Estate", "winery", r3, "Bulgaria",
    production_philosophy="terroir_expression",
    philosophy_description="Belgian-owned Thrace estate producing both international varieties and indigenous Mavrud from Haskovo vineyards; the Mavrud is Bulgaria's most interesting traditional variety expression.",
    reputation_narrative="Katarzyna Estate Synergy is one of Bulgaria's most ambitious wines; the estate demonstrates that Thrace can produce genuinely international-quality reds at compelling prices.",
    price_positioning="mid_range")
prod3b, new3b = PROD("Katarzyna Estate Synergy", "wine_still", p3b, r3, "Bulgaria",
    subcategory="Cabernet Sauvignon blend",
    description="Thracian Cabernet Sauvignon with Merlot and Petit Verdot: dark plum, cassis, cedar, tobacco and firm structure at exceptional value; Bulgaria's best answer to mid-range Bordeaux.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Roasted pork with juniper, rosemary and root vegetables", "complement", "established", "main", "Hearty Balkan pork preparation with the region's structured Cabernet blend; rosemary bridges the wine's cedar.")
    PAIR(prod3b, "Gyuvech (Bulgarian clay pot stew with mixed vegetables and meat)", "complement", "classic", "main", "Bulgaria's most beloved slow-cooked clay pot dish with its finest red wine — a deeply satisfying local pairing.")
    PAIR(prod3b, "Grilled lamb chops with Plovdiv herb chimichurri", "complement", "established", "main", "Balkan lamb with Thracian red wine; chimichurri bridges the wine's structure with the lamb's herb character.")
    PAIR(prod3b, "Aged Brie with grape jam and walnut bread", "complement", "suggested", "cheese", "International cheese reference for the region's increasingly international wine style.")

# ── Region 4: Rheinhessen ─────────────────────────────────────────────────────
print("\n=== Region 4: Rheinhessen ===")
r4 = R("Rheinhessen", "Germany", "wine",
    designation_type="Anbaugebiet",
    designation_name="Rheinhessen Anbaugebiet",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Germany's largest wine region producing diverse wines from the Rhine Terrasse — including world-class Riesling from Nierstein's famous red-slate sites — alongside Silvaner, Spätburgunder and increasingly exciting Grüner Veltliner.",
    key_producers="Weingut Kühling-Gillot, Wagner-Stempel, Wittmann, Battenfeld-Spanier, Gunderloch",
    historical_context="Rheinhessen's reputation was damaged by Liebfraumilch mass production in the 20th century; the quality revolution led by a new generation of passionate growers has restored the Rhine Terrasse Riesling and Silvaner to world-class status."
)
VIN(r4, 2021, "excellent", "rising", "Outstanding vintage; Rheinhessen Riesling and Silvaner of extraordinary mineral definition.")
VIN(r4, 2020, "very_good", "stable", "Good quality; wines show the region's improving quality and diverse terroir expression.")
VIN(r4, 2019, "exceptional", "rising", "Benchmark year; Wittmann Kirchspiel and Battenfeld-Spanier Zellerweg both exceptional.")
VIN(r4, 2018, "excellent", "rising", "Outstanding warm year producing powerful, age-worthy wines across all varieties.")
VIN(r4, 2017, "very_good", "stable", "Good overall quality; wines show the region's characteristic balance of fruit and mineral.")

p4a = P("Wittmann", "winery", r4, "Germany",
    production_philosophy="biodynamic",
    philosophy_description="Westhofen-based biodynamic estate led by Philipp Wittmann, producing some of Germany's greatest Riesling GGs and a celebrated Silvaner from red-slate limestone slopes.",
    reputation_narrative="Wittmann Kirchspiel GG is consistently Germany's most acclaimed Rheinhessen Riesling; the estate's biodynamic quality has been compared to top Nahe and Mosel estates.",
    price_positioning="ultra_premium")
prod4a, new4a = PROD("Wittmann Kirchspiel GG Riesling", "wine_still", p4a, r4, "Germany",
    subcategory="Riesling",
    description="Germany's greatest Rheinhessen Riesling from red-slate limestone Kirchspiel: white peach, lime, mineral chalk, ginger and extraordinary vinosity; dry, complex and capable of 20+ years of development.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Roasted pike-perch (Zander) with butter, lemon and dill", "complement", "classic", "fish_course", "Rheinhessen's Rhine fish with Rheinhessen's greatest Riesling is the regional culinary tradition.")
    PAIR(prod4a, "Asparagus (Spargel) with hollandaise and Westphalian ham", "complement", "classic", "main", "Germany's most beloved spring dish canonically pairs with the Rhine region's great Riesling.")
    PAIR(prod4a, "Sauerkraut-braised pork knuckle with caraway and mustard", "complement", "established", "main", "Classic German pork preparation and Rheinhessen Riesling's acidity cut through the fat effortlessly.")
    PAIR(prod4a, "Appenzeller cheese with toasted caraway bread", "complement", "established", "cheese", "Spiced alpine cheese and mineral Riesling; caraway in the bread bridges the wine's mineral drive.")

p4b = P("Battenfeld-Spanier", "winery", r4, "Germany",
    production_philosophy="biodynamic",
    philosophy_description="Hohen-Sülzen estate producing exceptional biodynamic Riesling and Silvaner GGs from limestone-rich Zellerweg and Frauenberg vineyards; one of Rheinhessen's most rapidly rising estates.",
    reputation_narrative="Battenfeld-Spanier Zellerweg am Schwarzen Herrgott GG is Rheinhessen's most critically debated great Riesling; the estate's wines combine power with genuine mineral precision.",
    price_positioning="premium")
prod4b, new4b = PROD("Battenfeld-Spanier Hohen-Sülzen Silvaner GG", "wine_still", p4b, r4, "Germany",
    subcategory="Silvaner",
    description="Germany's most serious Silvaner: Rheinhessen limestone Silvaner — herbal, mineral, with green herb, lemon, white asparagus and earthy depth; complex, dry and capable of surprising development.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Wiesensalat mit Radieschen (spring meadow salad with radish)", "complement", "classic", "starter", "Silvaner's herbal precision and fresh acidity are ideal for light, herb-driven spring salads.")
    PAIR(prod4b, "Weisser Spargel mit Sauce hollandaise (white asparagus)", "complement", "classic", "main", "White asparagus and Silvaner is Germany's most traditional and respected spring pairing.")
    PAIR(prod4b, "Quark-Kräuter-Aufstrich (herbed quark spread) on rye bread", "complement", "established", "casual", "Fresh dairy and herbs on dark bread with mineral Silvaner is the quintessential German light lunch.")
    PAIR(prod4b, "Camembert with apple butter and hazelnuts", "bridge", "suggested", "cheese", "Soft cheese and Silvaner's herbal acidity; apple butter bridges the wine's citrus-herb character.")

# ── Region 5: Luján de Cuyo ───────────────────────────────────────────────────
print("\n=== Region 5: Lujan de Cuyo ===")
r5 = R("Luján de Cuyo", "Argentina", "wine",
    designation_type="DO",
    designation_name="Luján de Cuyo DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Mendoza's most prestigious subregion at 900–1,100m, producing Argentina's finest Malbec from alluvial gravel and clay soils with unparalleled concentration, violet aromatics and structured tannins.",
    key_producers="Achaval Ferrer, Clos de los Siete, Ruca Malén, Zuccardi, Viña Cobos",
    historical_context="Luján de Cuyo received Argentina's first Denominación de Origen in 1993; it is the heartland of Argentine Malbec's global rise, home to Mendoza's most famous single vineyards including Adrianna, Finca Altamira and Bella Vista."
)
VIN(r5, 2021, "excellent", "rising", "Outstanding Luján vintage; Malbec of extraordinary violet, mineral precision and structured elegance.")
VIN(r5, 2020, "very_good", "stable", "Good quality; classic Luján profile with concentration and freshness in balance.")
VIN(r5, 2019, "exceptional", "rising", "Benchmark Argentine vintage; wines of generational depth from top single vineyards.")
VIN(r5, 2018, "very_good", "stable", "Consistent quality; elegant Malbec with good structure and ageing potential.")
VIN(r5, 2017, "excellent", "rising", "Excellent growing conditions; wines of unusual freshness for such concentration.")

p5a = P("Achaval Ferrer", "winery", r5, "Argentina",
    production_philosophy="terroir_expression",
    philosophy_description="Multi-national partnership producing Mendoza's most internationally decorated single-vineyard Malbec series — Finca Bella Vista, Finca Altamira and Finca Mirador — from Luján de Cuyo's finest terroirs.",
    reputation_narrative="Achaval Ferrer Finca Bella Vista is consistently Argentina's highest-scoring Malbec; the estate's single-vineyard series represents the apex of Argentine fine wine ambition.",
    price_positioning="ultra_premium")
prod5a, new5a = PROD("Achaval Ferrer Finca Bella Vista Malbec", "wine_still", p5a, r5, "Argentina",
    subcategory="Malbec",
    description="One of Argentina's greatest single-vineyard Malbec: from Luján de Cuyo's historic Bella Vista old vines — violet, blueberry, graphite, rose petal and extraordinary silky tannin from centenarian vines.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Grilled wagyu asado with chimichurri de hierbas", "complement", "classic", "main", "Argentina's finest beef with Argentina's finest wine is the most natural luxury pairing in the country.")
    PAIR(prod5a, "Slow-roasted suckling lamb with Andean herbs", "complement", "classic", "main", "Andean tradition: slow-cooked mountain lamb with Mendoza's greatest violet-rich Malbec.")
    PAIR(prod5a, "Duck magret with cherry jus and root vegetable gratin", "complement", "established", "main", "French-inspired preparation with Argentine variety; cherry jus bridges Malbec's violet and plum character.")
    PAIR(prod5a, "Manchego curado with membrillo and walnut", "complement", "established", "cheese", "Classic Spanish cheese reference for this globally celebrated Argentine variety.")

p5b = P("Viña Cobos", "winery", r5, "Argentina",
    production_philosophy="terroir_expression",
    philosophy_description="Paul Hobbs-led Mendoza estate producing the legendary Cobos Malbec from old-vine Luján de Cuyo sources; Cobos is consistently one of Argentina's highest-scoring wines.",
    reputation_narrative="Cobos Malbec has received 100-point scores from Robert Parker; the estate defines the pinnacle of concentrated, powerful Luján de Cuyo Malbec.",
    price_positioning="ultra_premium")
prod5b, new5b = PROD("Cobos Malbec", "wine_still", p5b, r5, "Argentina",
    subcategory="Malbec",
    description="Argentina's most Parker-celebrated Malbec: old-vine Luján Malbec of extraordinary concentration — violet, blackberry, mocha, dark chocolate and plush tannins from high-altitude gravelly alluvial soils.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "Prime Angus beef with roasted bone marrow and sea salt", "complement", "classic", "main", "Intense concentrated Malbec needs equally intense beef; bone marrow's richness amplifies the wine's depth.")
    PAIR(prod5b, "Braised oxtail with tomato, olives and polenta", "complement", "established", "main", "Long-cooked collagen-rich beef tail and powerful Malbec; tomato bridges acidity, olive adds savoury depth.")
    PAIR(prod5b, "70% Valrhona dark chocolate and sea salt caramel", "complement", "suggested", "digestif", "The wine's chocolate and mocha notes make it extraordinary with intensely bitter dark chocolate.")
    PAIR(prod5b, "Aged Manchego with Pedro Ximénez reduction", "complement", "established", "cheese", "Hard cheese and rich sweet reduction bridge the wine's concentrated fruit and structure at a celebration's end.")

# ── Final count ───────────────────────────────────────────────────────────────
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
