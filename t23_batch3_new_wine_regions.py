#!/usr/bin/env python3
"""T23 Batch 3 — New wine regions: Adelaide Hills, Valdeorras, Madiran, Etna DOC, Swartland
Fixes from prior attempts:
  - reputation_tier: iconic/prestigious/respected/emerging/overlooked
  - quality_descriptor: exceptional/excellent/very_good/good/average/challenging/poor
  - beverage_producers: uses reputation_narrative (not description)
"""

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
        return row[0]
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── ADELAIDE HILLS GI ────────────────────────────────────────────
print("\n=== Adelaide Hills GI ===")
r_adh = R("Adelaide Hills", "Australia", "wine",
           designation_type="GI",
           designation_name="Adelaide Hills GI",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="South Australia's premier cool-climate wine region in the Mount Lofty Ranges, celebrated for vibrant Sauvignon Blanc, textural Chardonnay, fragrant Pinot Gris, and elegant Pinot Noir. Altitude (400-710m) tempers the Australian heat.",
           key_producers="Shaw + Smith, Deviation Road, Bird in Hand, Petaluma, Ashton Hills",
           historical_context="Settled wine-growing tradition from the 1840s; cool-climate revival in the 1980s led by Shaw + Smith's founding in 1989 and Petaluma's pioneering work in Piccadilly Valley.")

for yr, qd, pt, sn in [
    (2023, "exceptional", "rising", "Cool growing season with late rains; crisp acids and intense aromatics across all varieties."),
    (2022, "excellent", "stable", "Near-perfect conditions; Shaw + Smith Sauvignon Blanc achieved benchmark status."),
    (2021, "very_good", "stable", "Moderate heat with good diurnal range; elegant whites with fine structure."),
    (2020, "good", "stable", "Bushfire smoke impacted some blocks; hand-sorted fruit yielded honest expressions."),
    (2019, "excellent", "stable", "Exceptional growing season; textbook Chardonnay and Pinot Noir vintage."),
]:
    VIN(r_adh, yr, qd, pt, sn)

p_ss = P("Shaw + Smith", "Australia", r_adh,
          description="Pioneering Adelaide Hills winery founded 1989 by cousins Martin Shaw MW and Michael Hill Smith MW. Benchmark Sauvignon Blanc and Chardonnay define the region's identity.")
prod_ss = PROD("Shaw + Smith M3 Chardonnay", "wine_still", p_ss, r_adh, "Australia",
               subcategory="Chardonnay",
               description="Single-vineyard Chardonnay from the M3 Vineyard at 500m altitude. Burgundian in spirit - fermented in French oak with restrained winemaking. Textural, saline, long.",
               price_tier="premium")
PAIR(prod_ss, "Pan-roasted abalone with brown butter and sea vegetables", "complement", "classic", "main", "Saline minerality mirrors coastal umami; creamy texture elevates the abalone's richness")
PAIR(prod_ss, "Whole roasted cauliflower with aged Comte and hazelnut", "complement", "established", "main", "Nutty oak integration aligns with roasted cauliflower and Comte's crystalline sharpness")

p_dr = P("Deviation Road Winery", "Australia", r_adh,
          description="Dedicated cool-climate specialist in the Adelaide Hills focused on methode traditionnelle sparkling wines and single-vineyard Pinot Noir, founded by the Longbottom family.")
prod_dr = PROD("Deviation Road Altair Blanc de Blancs", "wine_sparkling", p_dr, r_adh, "Australia",
               subcategory="Blanc de Blancs",
               description="Methode traditionnelle Blanc de Blancs from high-altitude Chardonnay. Toasty brioche, green apple, and citrus zest with fine persistent mousse.",
               price_tier="premium")
PAIR(prod_dr, "Sydney rock oysters with shallot mignonette", "complement", "classic", "aperitif", "Toasty autolysis cuts through brine; fine mousse lifts the oceanic minerality")
PAIR(prod_dr, "Kingfish crudo with yuzu kosho and shaved fennel", "complement", "established", "starter", "Fine mousse texture echoes the silky fish; citrus notes mirror yuzu brightness")

# ── VALDEORRAS DO ────────────────────────────────────────────────
print("\n=== Valdeorras DO ===")
r_vdo = R("Valdeorras", "Spain", "wine",
           designation_type="DO",
           designation_name="Valdeorras DO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Galician wine DO in the Sil River valley, internationally celebrated for Godello - one of Spain's finest white grapes. Schist and slate soils produce wines of mineral intensity and exceptional aging potential.",
           key_producers="Guitian, Rafael Palacios, A Tapada, Valdesil, Virxen dos Remedios",
           historical_context="Godello was nearly extinct in the 1970s; Horacio Fernandez Presa revived the variety in Valdeorras, and by the 2000s Rafael Palacios had placed the DO on the world map with As Sortes.")

for yr, qd, pt, sn in [
    (2023, "exceptional", "rising", "Cool Atlantic-influenced growing season; Godello achieved extraordinary aromatic complexity and crystalline minerality."),
    (2022, "excellent", "rising", "Excellent ripeness balanced by Galician rainfall; benchmark vintage for age-worthy Godello."),
    (2021, "very_good", "stable", "Classic Valdeorras vintage with bracing acidity and slate-driven minerality."),
    (2020, "excellent", "stable", "Warm summer followed by cooling rains; full-bodied yet precise Godello expressions."),
    (2019, "good", "stable", "Variable conditions; top producers made elegant, food-friendly whites."),
]:
    VIN(r_vdo, yr, qd, pt, sn)

p_gui = P("Guitian", "Spain", r_vdo,
           description="One of Galicia's most admired Godello producers, crafting mineral-driven whites from old vines on steep schist terraces in the Sil River valley.")
prod_gui = PROD("Guitian Godello Sobre Lias", "wine_still", p_gui, r_vdo, "Spain",
                subcategory="Godello",
                description="Godello aged on fine lees for six months, building texture and complexity while preserving the variety's signature minerality. Citrus, white peach, and wet slate with a long saline finish.",
                price_tier="mid_range")
PAIR(prod_gui, "Grilled percebes with sea salt and lemon", "complement", "classic", "starter", "Mineral salinity of Godello mirrors the oceanic intensity of percebes; lees texture complements the shellfish")
PAIR(prod_gui, "Pulpo a la gallega with paprika and olive oil", "complement", "classic", "main", "Regional affinity - Galician seafood and Galician Godello are canonical partners; smoky paprika lifted by citrus notes")

p_rp = P("Rafael Palacios", "Spain", r_vdo,
          description="The winemaker who elevated Valdeorras to international prominence, producing single-vineyard Godellos of extraordinary mineral depth and aging potential from old vines on slate and quartzite soils.")
prod_rp = PROD("Rafael Palacios As Sortes", "wine_still", p_rp, r_vdo, "Spain",
               subcategory="Godello",
               description="Flagship single-vineyard Godello from pre-phylloxera vines on slate and quartzite soils. Complex and age-worthy - roasted nuts, stone fruit, iodine minerality, extraordinary length.",
               price_tier="ultra_premium")
PAIR(prod_rp, "Salt cod brandade with black truffle and potato", "complement", "classic", "main", "Godello's mineral depth and lees richness integrates with the salt cod's intensity; truffle echoes earthy complexity")
PAIR(prod_rp, "Pan-seared turbot with brown butter and capers", "complement", "established", "main", "Classic Galician pairing - the wine's weight matches the turbot's density; citrus acidity balances the butter richness")

# ── MADIRAN AOC ──────────────────────────────────────────────────
print("\n=== Madiran AOC ===")
r_mad = R("Madiran", "France", "wine",
           designation_type="AOC",
           designation_name="Madiran AOC",
           reputation_tier="respected",
           quality_trajectory="established",
           description="Southwest French AOC in the Pyrenees foothills, producing powerful, structured red wines from Tannat - a grape nearly exclusive to this appellation. At its best, Madiran produces wines of extraordinary longevity requiring years of cellaring.",
           key_producers="Chateau Montus, Domaine Berthoumieu, Chateau d'Aydie, Producteurs Plaimont",
           historical_context="Tannat's heartland since medieval times; Alain Brumont's Chateau Montus in the 1980s transformed perceptions with barrel-aged Tannat of world-class ambition and international acclaim.")

for yr, qd, pt, sn in [
    (2022, "excellent", "stable", "Warm growing season with ideal ripeness; Tannat achieved exceptional tannin ripeness and dark fruit density."),
    (2021, "very_good", "stable", "Cooler vintage producing more classical structured Madiran with firm tannins and impressive longevity potential."),
    (2020, "exceptional", "rising", "The finest Madiran vintage in a generation; concentrated, powerful wines with extraordinary aging potential."),
    (2019, "excellent", "stable", "Excellent ripeness with good freshness; approachable early but built for long cellaring."),
    (2018, "good", "stable", "Solid vintage; some blocks yielded outstanding fruit despite uneven conditions."),
]:
    VIN(r_mad, yr, qd, pt, sn)

p_mon = P("Chateau Montus", "France", r_mad,
           description="Alain Brumont's flagship estate and the domaine that transformed Madiran's international reputation. The Cuvee Prestige - 100% Tannat aged in new oak - is the appellation's benchmark wine of extraordinary longevity.")
prod_mon = PROD("Chateau Montus Cuvee Prestige", "wine_still", p_mon, r_mad, "France",
                subcategory="Tannat",
                description="100% Tannat from old vines, aged 18 months in new French oak. Monolithic structure, dark berry intensity, graphite tannins, and a finish lasting over a minute. Demands 10+ years of cellaring.",
                price_tier="premium")
PAIR(prod_mon, "Cassoulet with confit duck and Toulouse sausage", "complement", "classic", "main", "Tannat's structure and dark fruit power through the richness of confit duck; regional pairing of historic depth")
PAIR(prod_mon, "Aged Manchego with quince paste and walnuts", "complement", "established", "cheese", "Firm tannins are softened by the cheese fat; quince sweetness bridges the wine's dark fruit intensity")

p_ber = P("Domaine Berthoumieu", "France", r_mad,
           description="Family domaine producing authentic Madiran with traditional sensibility. Didier Barre's vineyards include very old Tannat vines producing wines of earthy complexity and honest regional character.")
prod_ber = PROD("Domaine Berthoumieu Charles de Batz", "wine_still", p_ber, r_mad, "France",
                subcategory="Tannat",
                description="Named for the real d'Artagnan, this cuvee represents Madiran at its most authentic - rustic power, dark plum and blackberry, firm tannins, and a hint of violets and iron minerality.",
                price_tier="mid_range")
PAIR(prod_ber, "Magret de canard with roasted garlic and thyme jus", "complement", "classic", "main", "Duck fat richness tames Tannat's tannins; herb jus mirrors the wine's earthy complexity")
PAIR(prod_ber, "Venison stew with forest mushrooms and root vegetables", "complement", "established", "main", "Wild game's iron notes resonate with Tannat's ferrous intensity; mushrooms amplify earthy depth")

# ── ETNA DOC ─────────────────────────────────────────────────────
print("\n=== Etna DOC ===")
r_etna = R("Etna", "Italy", "wine",
            designation_type="DOC",
            designation_name="Etna DOC",
            reputation_tier="prestigious",
            quality_trajectory="ascending",
            description="Sicily's most exciting wine DOC on the slopes of Europe's highest active volcano. Nerello Mascalese produces wines of extraordinary elegance - often compared to Burgundy for their terroir transparency and aging potential. Ancient pre-phylloxera vines on lava soils.",
            key_producers="Frank Cornelissen, Passopisciaro, Benanti, Terre Nere, Tornatore",
            historical_context="Ancient wine tradition from Phoenician times; modern fine wine era began with Benanti in the 1990s, followed by Frank Cornelissen's biodynamic revolution and Andrea Franchetti's Passopisciaro in the 2000s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Excellent volcanic growing season; Nerello Mascalese showed exceptional finesse and mineral depth."),
    (2021, "very_good", "stable", "Cooler than average; wines with classic Etna elegance and high-toned red fruit."),
    (2020, "exceptional", "rising", "Benchmark Etna vintage; contrada wines showed extraordinary terroir differentiation."),
    (2019, "excellent", "stable", "Ideal ripeness with volcanic mineral intensity; transparent expressions of individual contrade."),
    (2018, "good", "stable", "Some challenges from uneven rainfall; top producers delivered focused, mineral wines."),
]:
    VIN(r_etna, yr, qd, pt, sn)

p_corn = P("Frank Cornelissen", "Italy", r_etna,
            description="Maverick Belgian winemaker who moved to Etna in 2001, farming biodynamically and making unfiltered, non-interventionist wines from ancient pre-phylloxera vines at altitude. Magma and Munjebel are internationally acclaimed cult wines.")
prod_corn = PROD("Frank Cornelissen Munjebel Rosso", "wine_still", p_corn, r_etna, "Italy",
                  subcategory="Nerello Mascalese",
                  description="Blended from multiple volcanic contrade, this is Cornelissen's accessible expression of Etna - vivid cherry, volcanic minerality, iron and orange peel, with characteristic transparency and energy.",
                  price_tier="premium")
PAIR(prod_corn, "Grilled swordfish with caponata and pine nuts", "complement", "established", "main", "Nerello's translucent red fruit and volcanic minerality complements the fish; caponata's sweet-sour mirrors the wine's energy")
PAIR(prod_corn, "Roasted wild mushrooms with polenta and truffle oil", "complement", "classic", "main", "Volcanic earth notes resonate with mushroom intensity; the wine's transparency allows the truffle to shine")

p_pass = P("Passopisciaro", "Italy", r_etna,
            description="Andrea Franchetti's benchmark Etna estate, producing single-contrada Nerello Mascalese wines that demonstrate Etna's extraordinary terroir diversity. Considered among Italy's finest modern wine estates.")
prod_pass = PROD("Passopisciaro Passorosso", "wine_still", p_pass, r_etna, "Italy",
                  subcategory="Nerello Mascalese",
                  description="Entry-level Passopisciaro blending multiple contrade - pale ruby, floral, vibrant cherry, iron minerality, and silky tannins showing the estate's signature elegance.",
                  price_tier="premium")
PAIR(prod_pass, "Braised rabbit with olives, capers, and Sicilian tomatoes", "complement", "classic", "main", "Nerello's cherry and iron notes harmonize with rabbit's sweetness; Sicilian flavours find regional resonance")
PAIR(prod_pass, "Pork cheeks slow-braised with red wine reduction", "complement", "established", "main", "Silky tannins embrace the collagen richness; volcanic mineral intensity carries through the braising notes")

# ── SWARTLAND WO ─────────────────────────────────────────────────
print("\n=== Swartland WO ===")
r_swt = R("Swartland", "South Africa", "wine",
           designation_type="WO",
           designation_name="Swartland WO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="South Africa's most exciting wine region in the Western Cape, celebrated for old-vine Chenin Blanc, Rhone-variety Syrah and Grenache, and a generation of boundary-pushing producers. The Swartland Revolution redefined South African fine wine.",
           key_producers="Sadie Family Wines, Mullineux and Leeu, Badenhorst, Lammershoek, Intellego",
           historical_context="The Swartland Revolution (2010 onwards) led by Eben Sadie, Andrea Mullineux, and Adi Badenhorst transformed this grain-farming region into South Africa's most celebrated fine wine appellation.")

for yr, qd, pt, sn in [
    (2023, "very_good", "stable", "Moderate growing season; old-vine Chenin Blanc showed exceptional mineral intensity and precision."),
    (2022, "excellent", "rising", "Excellent conditions for both Chenin Blanc and Rhone varieties; benchmark Swartland vintage."),
    (2021, "exceptional", "rising", "Perhaps the finest Swartland vintage; Syrah and old-vine Chenin of extraordinary complexity."),
    (2020, "good", "stable", "Drought conditions challenged many; old-vine dry-farmed plots excelled under stress."),
    (2019, "very_good", "stable", "Balanced vintage with good acid retention; Mullineux Syrah achieved icon status."),
]:
    VIN(r_swt, yr, qd, pt, sn)

p_sad = P("Sadie Family Wines", "South Africa", r_swt,
           description="Eben Sadie is the founding genius of the Swartland Renaissance. His old-vine Chenin Blanc (Palladius) and blended red (Columella) are South Africa's most internationally acclaimed wines.")
prod_sad = PROD("Sadie Family Wines Palladius", "wine_still", p_sad, r_swt, "South Africa",
                 subcategory="Chenin Blanc",
                 description="Landmark white blend anchored by old-vine Chenin Blanc with Grenache Blanc, Palomino, Clairette, and heritage varieties. Rich, complex, and age-worthy - beeswax, yellow orchard fruit, and volcanic stone.",
                 price_tier="ultra_premium")
PAIR(prod_sad, "Whole roasted yellowtail with preserved lemon and harissa", "complement", "classic", "main", "The wine's weight matches the robust fish; preserved lemon echoes oxidative complexity; harissa finds resonance in the spice notes")
PAIR(prod_sad, "Cape Malay chicken curry with apricots and basmati", "complement", "established", "main", "Regional pairing - old-vine Chenin's tropical richness harmonizes with the fruity curry; beeswax texture embraces the coconut")

p_mul = P("Mullineux and Leeu Family Wines", "South Africa", r_swt,
           description="Andrea and Chris Mullineux produce Swartland's most celebrated Syrah and old-vine Chenin Blanc. Single-terroir Schist and Granite Syrahs are benchmark expressions of Swartland's volcanic and geological diversity.")
prod_mul = PROD("Mullineux Kloof Street Rouge", "wine_still", p_mul, r_swt, "South Africa",
                 subcategory="Syrah Blend",
                 description="Entry-level Swartland red blend - Syrah with Grenache, Cinsault, and Carignan from old bush vines. Vivid red and dark berry, fragrant with olive tapenade and fresh herbs, approachable yet authentic.",
                 price_tier="mid_range")
PAIR(prod_mul, "Lamb sosaties with dried apricot and Cape spices", "complement", "classic", "main", "South African braai culture and Rhone varieties are natural partners; the wine's herb notes mirror the lamb marinade")
PAIR(prod_mul, "Roasted beetroot with aged feta, dukkah, and pomegranate", "complement", "established", "starter", "Juicy red-fruit character mirrors the beetroot's earthiness; olive notes in the wine resonate with the dukkah")

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
