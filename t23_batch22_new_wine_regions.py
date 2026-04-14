#!/usr/bin/env python3
"""T23 Batch 22 — New wine regions: Casablanca Valley DO (Chile), Marcillac AOC (France), Maury AOC (France), Franschhoek WO (South Africa), Condrieu AOC (France)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
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

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
      (name, country, region_id, producer_type, reputation_narrative, authority_tier)
      VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── CASABLANCA VALLEY DO (CHILE) ──────────────────────────────────
print("\n=== Casablanca Valley DO (Chile) ===")
r_cas = R("Casablanca Valley", "Chile", "wine",
           designation_type="DO",
           designation_name="Casablanca Valley DO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Chile's first and most celebrated cool-climate wine valley in the Valparaíso region between Santiago and the coast, pioneered in the 1980s as Chile's answer to Burgundy and Bordeaux blanc. The Pacific Ocean's cold Humboldt Current creates regular morning fog and cool temperatures that allow Sauvignon Blanc, Chardonnay, Pinot Noir, and Gewürztraminer to ripen with extraordinary aromatic precision and natural acidity. Casablanca's wines transformed international perception of Chilean wine from big, warm-climate reds to elegant, precise whites.",
           key_producers="Casas del Bosque, Kingston Family Vineyards, Matetic, Concha y Toro Casablanca, Viña Mar",
           historical_context="Pablo Morandé of Concha y Toro planted the first modern Casablanca Valley vineyards in 1982, acting on intuition that the fog-laden valley could produce cool-climate wines Chile had never seen. The experiment was wildly successful. By the 1990s, Casablanca was the most talked-about wine region in South America. The valley's lack of water became a major challenge — irrigation relies entirely on subterranean aquifers — making the Casablanca model expensive but compelling.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Casablanca vintage; Sauvignon Blanc of razor-sharp precision and Chardonnay of Burgundian mineral elegance."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; the Humboldt Current's fog produced wines of exceptional natural freshness."),
    (2020, "excellent", "stable", "Benchmark year; Kingston Family and Casas del Bosque produced internationally acclaimed Pinot Noir and Chardonnay."),
    (2019, "excellent", "rising", "Outstanding vintage; Casablanca Pinot Noir reached its highest critical scores; Sauvignon Blanc of extraordinary mineral intensity."),
    (2018, "very_good", "stable", "Solid vintage; fog pattern was ideal; Gewürztraminer achieved excellent aromatic intensity from the cool valley conditions."),
]:
    VIN(r_cas, yr, qd, pt, sn)

p_kin = P("Kingston Family Vineyards", "Chile", r_cas,
           description="Carl and Courtney Kingston's Casablanca Valley family estate producing some of Chile's finest cool-climate wines — Pinot Noir, Chardonnay, and Sauvignon Blanc from the densely planted Bayo Oscuro vineyard on the valley's clay and granite soils. Kingston Family wines have been placed on the Wine Spectator Top 100 and are considered Chile's benchmark cool-climate producer.")
prod_kin, new = PROD("Kingston Family Bayo Oscuro Pinot Noir", "wine_still", p_kin, r_cas, "Chile",
                     subcategory="Pinot Noir",
                     description="Chile's most internationally acclaimed Casablanca Valley Pinot Noir — dense planting on clay and granite producing a wine of unusual depth and Burgundian character. Wild cherry, dried rose petal, mineral freshness, and the cool coastal fog influence that sets Casablanca Pinot apart from warmer Chilean examples. Chilean terroir at its most elegant.",
                     price_tier="premium")
if new:
    PAIR(prod_kin, "Grilled Pacific salmon with wild mushroom ragout and truffle oil", "complement", "classic", "main", "Pacific fish from Chile's coastal waters and Chile's most Burgundian Pinot Noir — the wine's cherry and mineral character mirrors the salmon; mushrooms echo the forest floor notes")
    PAIR(prod_kin, "Conger eel chowder (cazuela de congrio) with leek, cream, and coriander", "complement", "established", "main", "Chile's most beloved fish soup (Pablo Neruda wrote an ode to it) and its finest Pinot Noir — the wine's acidity cuts through the cream; coriander bridges the wine's herbal notes")

p_cdb = P("Casas del Bosque", "Chile", r_cas,
           description="Juan Ignacio Chadwick's Casablanca Valley estate dedicated exclusively to cool-climate varieties — Sauvignon Blanc, Chardonnay, Pinot Noir, and Syrah from the valley's clay and sandy loam soils. Casas del Bosque's Reserve and Gran Reserva wines consistently represent Chile's finest cool-climate expressions at accessible prices.")
prod_cdb, new = PROD("Casas del Bosque Gran Reserva Sauvignon Blanc", "wine_still", p_cdb, r_cas, "Chile",
                     subcategory="Sauvignon Blanc",
                     description="Casablanca Valley's benchmark Sauvignon Blanc — grapefruit, lime, gooseberry, and the cool maritime mineral freshness that makes Casablanca SB the rival of New Zealand and Loire Valley. Dry, precise, and with a mineral finish that rewards the Grand Reserva designation. Chile's most consistent cool-climate white wine.",
                     price_tier="mid_range")
if new:
    PAIR(prod_cdb, "Ceviche de corvina (sea bass) with leche de tigre, rocoto pepper, and sweet potato", "complement", "classic", "main", "Chile's Pacific ceviche and its finest coastal white — the wine's citrus and mineral character mirrors the leche de tigre; the wine's acidity amplifies the ceviche's brightness; rocoto's heat is tempered by the wine's freshness")
    PAIR(prod_cdb, "Empanadas al horno (baked empanadas) with pino (spiced beef, olive, egg)", "complement", "established", "aperitif", "Chile's national snack and its most food-friendly cool-climate white — the wine's citrus freshness cuts through the pastry; the spiced filling's complexity is complemented by the wine's mineral character")

# ── MARCILLAC AOC (FRANCE) ────────────────────────────────────────
print("\n=== Marcillac AOC (France) ===")
r_mac = R("Marcillac", "France", "wine",
           designation_type="AOC",
           designation_name="Marcillac AOC",
           reputation_tier="overlooked",
           quality_trajectory="ascending",
           description="France's most idiosyncratic and overlooked red wine appellation in the Massif Central foothills above the Lot Valley in Aveyron, producing wines exclusively from Fer Servadou (locally called Mansoi or Brun de Lot) — a variety related to no other known grape. The red sandstone and schist soils of the 'rougier' (red earth) impart an extraordinary iron-mineral character. Marcillac wines have a haunting transparency, wild raspberry character, and an almost medicinal mineral quality unlike any French wine.",
           key_producers="Jean-Luc Matha, Domaine du Cros, Cave de Valady, Nicole Lapouble-Laplace",
           historical_context="Marcillac's wine was essential fuel for the medieval Compostela pilgrims crossing the Massif Central. The Abbaye de Conques nearby produced and traded the wine throughout the Middle Ages. Phylloxera devastated the vineyards and they were largely abandoned until the 1980s revival. Fer Servadou's survival in Marcillac (and as Braucol in Gaillac) makes it one of France's most endangered yet most distinctive varieties. Jean-Luc Matha's biodynamic wines introduced the region to Paris's natural wine community.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Marcillac vintage; Fer Servadou from red sandstone showed extraordinary iron mineral character and wild raspberry transparency."),
    (2021, "very_good", "stable", "Elegant vintage; cool Massif Central conditions produced Mansoi wines of exceptional freshness and the characteristic iron mineral."),
    (2020, "excellent", "stable", "Benchmark year; Jean-Luc Matha and Domaine du Cros produced internationally acclaimed natural Marcillac wines."),
    (2019, "very_good", "rising", "Outstanding vintage; natural wine community's discovery of Marcillac in force; Fer Servadou's character celebrated internationally."),
    (2018, "very_good", "stable", "Solid vintage; the red sandstone rougier expressed itself with unusual clarity in the Mansoi wines of this year."),
]:
    VIN(r_mac, yr, qd, pt, sn)

p_mat = P("Jean-Luc Matha", "France", r_mac,
           description="The Massif Central's most celebrated natural wine producer — Jean-Luc Matha's biodynamic Marcillac estate introduced the appellation to Paris's natural wine scene and international collectors. His minimal-intervention Fer Servadou wines from the red sandstone rougier are considered the definitive expression of this strange, haunting, and irreplaceable variety.")
prod_mat, new = PROD("Jean-Luc Matha Marcillac Vieilles Vignes", "wine_still", p_mat, r_mac, "France",
                     subcategory="Fer Servadou",
                     description="The finest natural Marcillac — Fer Servadou (Mansoi) from old vines on the red sandstone rougier, biodynamically farmed and minimally intervened. Translucent ruby, wild raspberry, iron ore, dried herbs, and the haunting medicinal mineral character that makes Marcillac unlike any other wine on earth. Cooling and individual.",
                     price_tier="mid_range")
if new:
    PAIR(prod_mat, "Tripou d'Aveyron (stuffed sheep's stomach with herbs and garlic)", "complement", "classic", "main", "Aveyron's most traditional offal dish and its indigenous wine — Marcillac's iron mineral and raspberry character is one of the few wines that handles tripou's intensity; the wine's transparency prevents competing with the dish")
    PAIR(prod_mat, "Petit salé aux lentilles (salt-cured pork with Puy lentils and mustard)", "complement", "established", "main", "The central French rustic tradition meets its regional wine — Marcillac's wild raspberry and mineral character cuts through the salt-cured pork's richness; lentils' earthiness bridges the iron mineral")

p_cro = P("Domaine du Cros", "France", r_mac,
           description="Philippe Teulier's Marcillac estate producing Lo Sang del Pais (Blood of the Country) — the region's most commercially successful and widely distributed wine. Domaine du Cros has brought Marcillac to an international audience while maintaining the region's distinctive red sandstone character and traditional Fer Servadou style.")
prod_cro, new = PROD("Domaine du Cros Lo Sang del Pais Marcillac", "wine_still", p_cro, r_mac, "France",
                     subcategory="Fer Servadou",
                     description="The most internationally distributed Marcillac — 'Blood of the Country' in Occitan describes the red sandstone soil that gives Fer Servadou its unique iron character. Wild strawberry, raspberry, iron mineral, violet, and a refreshing acidity that makes this one of France's most food-friendly reds. Unapologetically regional and irreplaceable.",
                     price_tier="mid_range")
if new:
    PAIR(prod_cro, "Aligot (Aubrac potato and Laguiole cheese fondue) with sausage and garlic", "complement", "classic", "main", "The Massif Central's most comforting dish and its regional red — Marcillac's iron acidity cuts through the elastic cheese-potato fondue; wild raspberry mirrors the garlic's sweet transformation; sausage adds smoky depth")
    PAIR(prod_cro, "Grilled onglet (hanger steak) with shallot confit and pomme sarladaise", "complement", "established", "main", "The iron-rich wine and the iron-rich cut of beef — onglet's mineral intensity mirrors Marcillac's iron mineral; shallot's sweetness bridges the wine's wild fruit; pomme sarladaise's duck fat adds richness")

# ── MAURY AOC (FRANCE) ────────────────────────────────────────────
print("\n=== Maury AOC (France) ===")
r_mau = R("Maury", "France", "wine",
           designation_type="AOC",
           designation_name="Maury AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Roussillon's most distinctive appellation in the schist-covered Agly Valley northwest of Perpignan, producing Maury — a fortified vin doux naturel from Grenache Noir on dramatic black schist slopes — alongside increasingly important dry red wines under the Maury Sec appellation. The Maury VDN comes in two styles: Maury Vintage (aged in bottle, fresh and dark) and Maury Oxydatif (aged oxidatively in barrels, developing rancio complexity). The black schist's mineral intensity gives Maury wines an earthy, iron character unlike Banyuls or Rivesaltes.",
           key_producers="Mas Amiel, Domaine de la Coume du Roy, Cave de Maury, Domaine Pouderoux, Domaine des Schistes",
           historical_context="Maury's viticulture dates to the 11th century when the Knights Templar of the Château de Quéribus controlled the vineyards. The black schist soils — formed 400 million years ago — give Maury wines their distinctive dark mineral character. Mas Amiel's iconic 15-Year-Old Maury (oxidatively aged in glass bonbonnes outdoors through Roussillon summers) is France's most celebrated vin doux naturel outside Banyuls.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Maury vintage; Grenache Noir from black schist showed extraordinary dark fruit concentration for VDN and Maury Sec."),
    (2021, "very_good", "stable", "Classic vintage; the Agly Valley's schist soils produced wines of excellent mineral depth and dark cherry intensity."),
    (2020, "excellent", "stable", "Benchmark year; Mas Amiel 15-Year-Old and Domaine Pouderoux produced the finest Maury VDN of the decade."),
    (2019, "excellent", "rising", "Outstanding vintage; Maury Sec (dry red) received extraordinary attention from international natural wine critics."),
    (2018, "very_good", "stable", "Solid vintage; black schist Grenache produced wines of good mineral depth; rancio oxidative complexity developed magnificently."),
]:
    VIN(r_mau, yr, qd, pt, sn)

p_ama = P("Mas Amiel", "France", r_mau,
           description="The Maury appellation's iconic producer, producing France's most celebrated vin doux naturel outside Banyuls. The 15-Year-Old Maury — oxidatively aged in large glass bonbonnes outdoors through Roussillon's brutal summers — is considered France's greatest vin doux naturel for its complexity and accessibility. Mas Amiel also produces excellent dry Maury Sec and Côtes du Roussillon.")
prod_ama, new = PROD("Mas Amiel 15 Ans d'Age Maury", "wine_fortified", p_ama, r_mau, "France",
                     subcategory="Grenache Noir",
                     description="France's most celebrated vin doux naturel aged in glass bonbonnes outdoors for 15 years — the Roussillon sun transforms the wine into something extraordinary: chocolate, dried fig, coffee, walnut, iron, and rancio complexity. Sweet but profoundly complex; one of the world's great dessert wines and cheese pairings.",
                     price_tier="premium")
if new:
    PAIR(prod_ama, "Roquefort with dark chocolate, walnuts, and dried Agen prunes", "complement", "classic", "cheese", "France's most iconic blue cheese and France's most celebrated vin doux naturel — Roquefort's salty intensity is perfectly balanced by Maury's sweet chocolate and rancio complexity; walnut bridges both")
    PAIR(prod_ama, "Chocolate fondant with salted caramel, fleur de sel, and crème fraîche", "complement", "classic", "dessert", "The wine's chocolate and coffee rancio character finds direct resonance in the fondant; salted caramel bridges Maury's sweetness and the salt; crème fraîche's acidity provides contrast")

p_pou = P("Domaine Pouderoux", "France", r_mau,
           description="Robert Pouderoux's small Maury estate producing intensely mineral Maury Vintage and Maury Sec wines from the darkest black schist parcels of the Agly Valley. Pouderoux's minimal-intervention approach produces Maury wines of unusual freshness and mineral character — quite different from Mas Amiel's oxidative style.")
prod_pou, new = PROD("Pouderoux Maury Vintage", "wine_fortified", p_pou, r_mau, "France",
                     subcategory="Grenache Noir",
                     description="Maury in its freshest and most mineral expression — bottle-aged rather than oxidatively aged, preserving the dark fruit intensity of black schist Grenache. Dark cherry, blackberry, iron, schist mineral, violets, and a freshness uncommon for VDN. A revelation of what Grenache on ancient schist can be when treated with care.",
                     price_tier="mid_range")
if new:
    PAIR(prod_pou, "Wild boar terrine with cornichons, Dijon mustard, and toasted brioche", "complement", "established", "starter", "The wine's dark fruit and iron mineral character bridges the game terrine's richness; Dijon's heat is tempered by the wine's natural sweetness; brioche provides textural contrast")
    PAIR(prod_pou, "Catalan crème catalane with orange blossom and caramelized sugar", "complement", "classic", "dessert", "Roussillon's version of crème brûlée and the region's most distinctive wine — the wine's dark cherry and mineral character complements the custard's vanilla richness; caramelized sugar bridges the sweetness")

# ── FRANSCHHOEK WO (SOUTH AFRICA) ────────────────────────────────
print("\n=== Franschhoek WO (South Africa) ===")
r_fra = R("Franschhoek", "South Africa", "wine",
           designation_type="WO",
           designation_name="Franschhoek WO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="South Africa's most culinarily and historically significant wine valley — the 'French Corner' established by Huguenot refugees in 1688 who brought French viticulture and winemaking traditions to the Cape. Franschhoek produces exceptional Cap Classique (traditional method sparkling wine), Semillon from ancient vines (South Africa's oldest Semillon plantings dating to the early 19th century), Chardonnay, and Pinot Noir from the enclosed mountain valley's unique clay and shale soils. The valley's French heritage and culinary culture make it South Africa's gastronomic heartland.",
           key_producers="Graham Beck, Boekenhoutskloof, Haute Cabrière, La Motte, Plaisir de Merle",
           historical_context="In 1688, 200 French Huguenot refugees arrived at the Cape fleeing Louis XIV's religious persecution. Granted land in this valley, they named their farms with French names that survive today — La Motte, Haute Cabrière, Boschendal. Their Bordeaux and Burgundy winemaking traditions took root in the valley's unique enclosed mountain amphitheater, creating a wine culture distinct from the Cape's other regions. Graham Beck's flagship Blanc de Blancs Cap Classique has been served at multiple US Presidential inaugurations.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Franschhoek vintage; Cap Classique base wines and Semillon of extraordinary mineral complexity from clay-shale soils."),
    (2021, "very_good", "stable", "Classic vintage; the valley's enclosed mountain amphitheater produced wines of excellent precision and the characteristic Franschhoek freshness."),
    (2020, "excellent", "stable", "Benchmark year; Boekenhoutskloof and Graham Beck both produced wines of exceptional quality across all categories."),
    (2019, "exceptional", "rising", "Greatest Franschhoek vintage of the modern era; Cap Classique and old-vine Semillon received extraordinary international recognition."),
    (2018, "very_good", "stable", "Solid vintage; Chardonnay and Cap Classique base wine both excelled; old-vine Semillon of excellent mineral depth."),
]:
    VIN(r_fra, yr, qd, pt, sn)

p_boe = P("Boekenhoutskloof", "South Africa", r_fra,
           description="Marc Kent's iconic Franschhoek estate producing South Africa's most internationally acclaimed and sought-after wines — The Chocolate Block (Syrah blend), The Wolftrap, and the flagship Cabernet Sauvignon. Boekenhoutskloof has done more to elevate South African wine's international reputation in the past 25 years than any other single producer.")
prod_boe, new = PROD("Boekenhoutskloof Semillon Franschhoek", "wine_still", p_boe, r_fra, "South Africa",
                     subcategory="Semillon",
                     description="South Africa's most celebrated old-vine Semillon from ancient Franschhoek vines — a wine of extraordinary complexity and Burgundian character. Lanolin, beeswax, lemon curd, white peach, and the distinctive waxy mineral depth that only old-vine Semillon achieves. One of the Cape's most age-worthy whites; South Africa's greatest Semillon.",
                     price_tier="premium")
if new:
    PAIR(prod_boe, "Bouillabaisse-style West Coast seafood stew with rouille and saffron", "complement", "classic", "main", "Old-vine Semillon's waxy richness and mineral depth is the Cape's finest match for rich seafood stew; rouille's spice finds resonance in the wine's complexity")
    PAIR(prod_boe, "Grilled yellowtail with cape sambal, potato crush, and lemon butter", "complement", "classic", "main", "The Cape's prized pelagic fish and Franschhoek's finest Semillon — the wine's waxy texture and citrus depth bridges the fish's richness; cape sambal's spice is tempered by the wine's weight")

p_bec = P("Graham Beck", "South Africa", r_fra,
           description="The Robertson and Franschhoek estate producing South Africa's most internationally recognized Cap Classique — Graham Beck Blanc de Blancs was served at Nelson Mandela's inauguration and at Barack Obama's. The Brut Non-Vintage and Blanc de Blancs are South Africa's most exported and celebrated traditional method sparkling wines.")
prod_bec, new = PROD("Graham Beck Blanc de Blancs Cap Classique", "wine_sparkling", p_bec, r_fra, "South Africa",
                     subcategory="Chardonnay",
                     description="South Africa's most celebrated Cap Classique — 100% Chardonnay from Robertson limestone and Franschhoek clay soils, traditionally fermented and aged 18+ months on lees. Lemon curd, green apple, brioche, toasted almond, and the fine, persistent mousse of a great traditional method wine. Served at multiple Presidential inaugurations.",
                     price_tier="premium")
if new:
    PAIR(prod_bec, "Bobotie-spiced quail eggs with Cape Malay curry mayo and micro herbs", "complement", "established", "amuse", "South Africa's most celebratory sparkling wine meets Cape Malay inspired bites — the wine's citrus and brioche character bridges the curry's spice; lemon curd mirrors the egg's richness")
    PAIR(prod_bec, "Freshly shucked Knysna oysters with pink peppercorn mignonette and lemon", "complement", "classic", "aperitif", "Cap Classique and Cape oysters from the Garden Route — the wine's fine mousse and mineral character mirrors the oyster's brine; pink peppercorn adds aromatic complexity")

# ── CONDRIEU AOC (FRANCE) ─────────────────────────────────────────
print("\n=== Condrieu AOC (France) ===")
r_con_f = R("Condrieu", "France", "wine",
             designation_type="AOC",
             designation_name="Condrieu AOC",
             reputation_tier="iconic",
             quality_trajectory="established",
             description="The northern Rhône's most spectacular and singular white wine AOC producing exclusively Viognier from the granitic gneiss slopes above the village of Condrieu south of Lyon. Condrieu is the world's benchmark for Viognier — the variety that in lesser hands produces over-alcoholic, flabby wine but at Condrieu's best creates hauntingly aromatic, complex, and deceptively age-worthy wines of peach, apricot, violet, and mineral depth. The appellation includes the Château-Grillet single-estate sub-AOC.",
             key_producers="Yves Cuilleron, Pierre Gaillard, Georges Vernay, André Perret, Domaine du Monteillet",
             historical_context="Condrieu nearly disappeared in the 1960s when only 7 hectares remained in production and the Viognier variety was close to extinction. Georges Vernay's Coteau de Vernon remains the appellation's most historic and important single-parcel wine — his obsession with saving Viognier when the variety had been abandoned by all others is the primary reason Condrieu exists today. The appellation's production remains tiny — under 400 hectares — making its wines highly sought after worldwide.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Condrieu vintage; Viognier from granitic gneiss showed extraordinary aromatic precision and the rare mineral complexity of great years."),
    (2021, "very_good", "stable", "Classic vintage; cooler conditions produced Viognier with exceptional freshness — more restrained aromatics but greater longevity potential."),
    (2020, "excellent", "stable", "Benchmark year; Vernay Coteau de Vernon and Cuilleron Les Chaillets produced the most complex Condrieu in a decade."),
    (2019, "exceptional", "rising", "Greatest Condrieu vintage of the modern era; Viognier of legendary aromatic intensity and unusual ability to develop in bottle."),
    (2018, "excellent", "stable", "Excellent vintage; warm conditions produced Condrieu of maximum aromatic intensity; some of the finest Château-Grillet in years."),
]:
    VIN(r_con_f, yr, qd, pt, sn)

p_ver = P("Georges Vernay", "France", r_con_f,
           description="Christine Vernay's family estate — the producer that saved Condrieu and Viognier from extinction. Georges Vernay's decades of dedication to the variety when all others had abandoned it makes this estate wine history. The Coteau de Vernon is the appellation's most historically important and consistently greatest wine — from the steepest granitic gneiss terraces.")
prod_ver, new = PROD("Vernay Coteau de Vernon Condrieu", "wine_still", p_ver, r_con_f, "France",
                     subcategory="Viognier",
                     description="The wine that saved Viognier — Georges Vernay's historic Coteau de Vernon from the steepest granitic gneiss terraces. The world's benchmark Condrieu: white peach, apricot blossom, violet, crystallized ginger, mineral gneiss, and a haunting floral depth that develops magnificently in the cellar. One of France's most distinctive and irreplaceable wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_ver, "Roasted whole sea bass with apricot beurre blanc, fennel, and saffron", "complement", "classic", "main", "Condrieu's apricot and floral character finds direct resonance in the apricot beurre blanc; sea bass's delicacy allows the wine's aromatics to shine; fennel bridges the wine's anise notes")
    PAIR(prod_ver, "Foie gras terrine with Condrieu jelly, toasted brioche, and white pepper", "complement", "classic", "starter", "The wine appears in the jelly itself — a circular gastronomic statement; Viognier's apricot and floral character is the Rhône's classic foie gras partner; white pepper bridges the wine's spice")

p_cui = P("Yves Cuilleron", "France", r_con_f,
           description="Yves Cuilleron's Chavanay estate producing the most commercially accessible and stylistically diverse range of Condrieu — from the dry Les Chaillets to the late-harvest Les Ayguets and the dry Condrieu Les Esses. Cuilleron is considered the appellation's most technically precise and consistently excellent producer alongside Vernay.")
prod_cui, new = PROD("Cuilleron Les Chaillets Condrieu", "wine_still", p_cui, r_con_f, "France",
                     subcategory="Viognier",
                     description="Yves Cuilleron's benchmark dry Condrieu from old-vine granitic gneiss — more restrained and mineral than the late-harvest styles, with white peach, apricot, violet, and a mineral precision that demonstrates Viognier's ability to express terroir when yields are kept low. Drink in first 3-4 years for maximum aromatic intensity.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_cui, "Grilled langoustines with apricot and tarragon butter and brioche croutons", "complement", "classic", "main", "Condrieu and crustacean is one of France's great pairings — the wine's apricot character bridges the langoustine's sweetness; tarragon mirrors the wine's floral complexity; brioche provides textural contrast")
    PAIR(prod_cui, "Chicken fricassée with morels, tarragon cream, and puff pastry vol-au-vents", "complement", "classic", "main", "The Lyon region's finest traditional dish with the northern Rhône's greatest white — morels' earthy depth is bridged by the wine's floral aromatics; tarragon creates a botanical bridge; cream mirrors the wine's texture")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
