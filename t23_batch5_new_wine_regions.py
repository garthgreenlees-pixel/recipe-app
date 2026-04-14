#!/usr/bin/env python3
"""T23 Batch 5 — New wine regions: Beaujolais, Roussillon, Sardinia, Sicily, Friuli-Venezia Giulia"""

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

# ── BEAUJOLAIS AOC ───────────────────────────────────────────────
print("\n=== Beaujolais AOC ===")
r_bj = R("Beaujolais", "France", "wine",
          designation_type="AOC",
          designation_name="Beaujolais AOC",
          reputation_tier="respected",
          quality_trajectory="ascending",
          description="Southern Burgundy's Gamay country, stretching from Lyon to Macon. The ten Cru Beaujolais villages — Fleurie, Morgon, Moulin-a-Vent, Brouilly, and others — produce wines of serious depth and character that reward cellaring. Beaujolais Nouveau is a different beast.",
          key_producers="Marcel Lapierre, Jean-Paul Brun, Jean-Louis Dutraive, Chateau Thivin, Guy Breton",
          historical_context="Beaujolais suffered decades of industrial over-production and Nouveau-driven trivialisation. The natural wine pioneers (Lapierre, Foillard, Breton, Thevenet) reclaimed its granite terroirs in the 1980s and created the world's first generation of natural wine producers.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Beaujolais vintage; Gamay achieved exceptional depth and structure across all ten Crus."),
    (2021, "very_good", "stable", "Elegant, Burgundian vintage; Morgon and Moulin-a-Vent showed extraordinary refinement."),
    (2020, "exceptional", "rising", "The finest Beaujolais vintage in decades; Crus from this year will age 15-20 years."),
    (2019, "excellent", "stable", "Warm vintage producing rich, concentrated Gamay with excellent aging potential."),
    (2018, "very_good", "stable", "Ripe and accessible vintage; the natural wine producers' Crus showed exceptional terroir expression."),
]:
    VIN(r_bj, yr, qd, pt, sn)

p_lap = P("Marcel Lapierre", "France", r_bj,
           description="The father of natural Beaujolais, Marcel Lapierre (and now his son Mathieu) produces Morgon of extraordinary depth and transparency from old-vine Gamay with zero sulphur additions. A cult wine of the natural wine movement.")
prod_lap, new = PROD("Marcel Lapierre Morgon", "wine_still", p_lap, r_bj, "France",
                     subcategory="Gamay",
                     description="Old-vine Morgon from volcanic granite soils with zero sulphur — pure cherry, dark berry, granite minerality, and extraordinary depth. The defining wine of the natural Beaujolais movement.",
                     price_tier="premium")
if new:
    PAIR(prod_lap, "Charcuterie board with Lyon rosette, cornichons, and Dijon mustard", "complement", "classic", "aperitif", "Gamay's cherry fruit and tangy acidity cut through the cured meat fat; regional pairing of natural affinity")
    PAIR(prod_lap, "Roast chicken with tarragon and whole garlic cloves", "complement", "classic", "main", "Beaujolais Gamay is the classic French roast chicken partner; the wine's fruit and acidity lift the herb jus")

p_bru = P("Jean-Paul Brun Terres Dorees", "France", r_bj,
           description="Jean-Paul Brun's Terres Dorees estate produces Beaujolais of impeccable quality from calcareous soils in the southern appellation — lighter, mineral, and often overlooked in favour of the granite Crus.")
prod_bru, new = PROD("Jean-Paul Brun L'Ancien Vieilles Vignes", "wine_still", p_bru, r_bj, "France",
                     subcategory="Gamay",
                     description="Old-vine Gamay from limestone-clay soils — a more structured, mineral expression of Beaujolais than the granite Crus. Bright cherry, raspberry, earthy minerality, and surprising depth for the appellation.",
                     price_tier="mid_range")
if new:
    PAIR(prod_bru, "Salade Lyonnaise with lardons, soft-boiled egg, and croutons", "complement", "classic", "starter", "Beaujolais Gamay is the canonical Lyon bistro wine; the wine's acidity lifts the warm bacon vinaigrette")
    PAIR(prod_bru, "Grilled salmon with lentils and herb vinaigrette", "complement", "established", "main", "Gamay's lower tannin and bright acidity work exceptionally well with salmon; the wine mirrors the lentil earthiness")

# ── ROUSSILLON AOP ───────────────────────────────────────────────
print("\n=== Roussillon AOP ===")
r_rou = R("Roussillon", "France", "wine",
           designation_type="AOP",
           designation_name="Cotes du Roussillon AOP",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Sun-drenched Catalan region of southern France bordering Spain, producing powerful Grenache-dominated reds, rare white varieties, and France's finest fortified wines (Banyuls, Maury). Old schist vines and extreme sun create wines of extraordinary concentration.",
           key_producers="Domaine Gauby, Domaine de la Rectorie, Domaine du Mas Blanc, Bila-Haut, Coume del Mas",
           historical_context="Roussillon was absorbed into France in 1659 — culturally Catalan, gastronomically Spanish. The region's old schist vines survived because they were too steep to mechanize; the natural wine renaissance discovered extraordinary terroirs here in the 2000s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage in Roussillon; old schist vines produced Grenache of extraordinary concentration and complexity."),
    (2021, "very_good", "stable", "Cooler season with Atlantic influence; the most elegant Roussillon vintage of the decade."),
    (2020, "excellent", "stable", "Classic Roussillon vintage with powerful, ripe reds and benchmark Banyuls fortified wines."),
    (2019, "excellent", "stable", "Very good conditions; Grenache Blanc and Grenache Gris in the whites showed unexpected freshness."),
    (2018, "very_good", "stable", "Warm but balanced vintage; Maury sec and old-vine Carignan particularly successful."),
]:
    VIN(r_rou, yr, qd, pt, sn)

p_gau = P("Domaine Gauby", "France", r_rou,
           description="Gerard Gauby's legendary biodynamic estate in Calce produces Roussillon's most complex and age-worthy wines from old schist vines. Vieilles Vignes and Muntada are benchmark expressions of what Roussillon can achieve.")
prod_gau, new = PROD("Domaine Gauby Vieilles Vignes Rouge", "wine_still", p_gau, r_rou, "France",
                     subcategory="Grenache Blend",
                     description="Old-vine Grenache, Syrah, Mourverdre, and Carignan from schist terraces — dense, complex, and alive. Black olive, garrigue, volcanic minerality, and a finish that evolves for minutes. Needs years of cellaring.",
                     price_tier="premium")
if new:
    PAIR(prod_gau, "Slow-braised ox cheeks with black olive and anchovy tapenade", "complement", "classic", "main", "The wine's olive and dark fruit character finds deep resonance with the tapenade; Grenache structure embraces the collagen richness")
    PAIR(prod_gau, "Aged Manchego with membrillo and marcona almonds", "complement", "established", "cheese", "The wine's earthy complexity finds affinity with the sheep's milk cheese; Catalan ingredients speak to the regional soul")

p_rec = P("Domaine de la Rectorie", "France", r_rou,
           description="Marc Parcé's iconic estate producing Banyuls and Collioure of world-class quality from ancient terraced schist vines above the Mediterranean. The family has farmed these terraces for generations without mechanization.")
prod_rec, new = PROD("Domaine de la Rectorie Banyuls Cuvee Leon Parcé", "wine_fortified", p_rec, r_rou, "France",
                     subcategory="Banyuls",
                     description="Biologically oxidized Banyuls from old schist vines — rancio character, dried fig, chocolate, orange peel, and roasted nuts. One of France's greatest fortified wines, aged in glass demijohns under the Mediterranean sun.",
                     price_tier="premium")
if new:
    PAIR(prod_rec, "Catalan crema brulee with orange and cinnamon", "complement", "classic", "dessert", "Rancio and oxidative character echoes the caramelized sugar; regional pairing — Banyuls and Catalan desserts are ancient partners")
    PAIR(prod_rec, "Dark chocolate tart with fleur de sel and hazelnut praline", "complement", "classic", "dessert", "The wine's chocolate and roasted nut intensity finds its natural partner; salt amplifies the dried fruit complexity")

# ── SARDINIA ─────────────────────────────────────────────────────
print("\n=== Sardinia ===")
r_sar = R("Sardinia", "Italy", "wine",
           designation_type="DOC",
           designation_name="Sardegna DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Italy's second largest island, home to Cannonau (Grenache's oldest ancestor), Vermentino di Gallura DOCG, Vernaccia di Oristano, and Carignano del Sulcis. Ancient vines, diverse terroirs, and a winemaking culture distinct from the Italian mainland.",
           key_producers="Argiolas, Santadi, Giovanni Montisci, Siddura, Capichera",
           historical_context="Sardinia's indigenous varieties are among the Mediterranean's most ancient — Cannonau shows genetic similarities to Bronze Age wine culture. The island maintained its traditions through centuries of Spanish and Italian rule; modern quality focus began in the 1990s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Sardinian vintage; Cannonau showed remarkable depth and Vermentino exceptional aromatic intensity."),
    (2021, "very_good", "stable", "Elegant, balanced vintage; old-vine Cannonau from Oliena and Mamoiada achieved exceptional complexity."),
    (2020, "excellent", "stable", "Classic Sardinian conditions; Carignano del Sulcis in the south produced particularly deep, structured reds."),
    (2019, "excellent", "stable", "Benchmark vintage; Vermentino di Gallura DOCG wines showed extraordinary mineral freshness."),
    (2018, "good", "stable", "Challenging drought conditions; bush-vine old Cannonau excelled from natural stress."),
]:
    VIN(r_sar, yr, qd, pt, sn)

p_arg = P("Argiolas", "Italy", r_sar,
           description="Sardinia's most important wine estate, founded in 1938. The Argiolas family preserves and celebrates indigenous varieties — their Turriga Cannonau is considered one of Italy's finest reds.")
prod_arg, new = PROD("Argiolas Turriga", "wine_still", p_arg, r_sar, "Italy",
                     subcategory="Cannonau",
                     description="Sardinia's most celebrated red — old-vine Cannonau (Grenache) with Carignano and Malvasia Nera, aged in French oak. Dark cherry, maquis scrub, tobacco, and iron minerality with extraordinary structure and aging potential.",
                     price_tier="premium")
if new:
    PAIR(prod_arg, "Roasted suckling pig (porceddu) with myrtle and sea salt", "complement", "classic", "main", "Sardinia's iconic pork dish and Cannonau are ancient regional partners; myrtle's herbal character echoes the maquis notes")
    PAIR(prod_arg, "Slow-braised lamb with fennel, tomato, and Pecorino Sardo", "complement", "classic", "main", "Cannonau's cherry and iron complexity harmonizes with lamb; Pecorino Sardo adds a regional accent")

p_san = P("Cantina di Santadi", "Italy", r_sar,
           description="The landmark cooperative of Sulcis in southwest Sardinia, producing Carignano del Sulcis of extraordinary depth from ancient bush vines. Their Terre Brune is Sardinia's most internationally acclaimed wine.")
prod_san, new = PROD("Santadi Terre Brune", "wine_still", p_san, r_sar, "Italy",
                     subcategory="Carignano",
                     description="Benchmark Carignano del Sulcis from old ungrafted bush vines on sandy soils — dark cherry, dried herbs, tobacco, and volcanic minerals. Dense, complex, and very long. Sardinia's great red wine.",
                     price_tier="premium")
if new:
    PAIR(prod_san, "Wild boar ragu with house-made malloreddus pasta", "complement", "classic", "main", "Regional pairing — Sardinian pasta with island game is the natural home for Carignano; the wine's dark fruit and herb notes integrate perfectly")
    PAIR(prod_san, "Aged Pecorino Fiore Sardo with local honey and walnuts", "complement", "established", "cheese", "Carignano's tannic structure is softened by the aged sheep's cheese fat; honey bridges the wine's dark fruit")

# ── SICILIA DOC ──────────────────────────────────────────────────
print("\n=== Sicilia DOC ===")
r_sic = R("Sicily", "Italy", "wine",
           designation_type="DOC",
           designation_name="Sicilia DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Italy's largest wine region, transformed from bulk wine producer to quality powerhouse. Native varieties — Nero d'Avola, Nerello Mascalese, Grillo, Catarratto, Zibibbo — thrive on volcanic soils and sun-drenched terraces. The Etna DOC is Sicily's most celebrated sub-zone.",
           key_producers="Planeta, Donnafugata, Benanti, Marco de Bartoli, Cos",
           historical_context="Sicily produced more wine than all of Australia for centuries — mostly going to France and northern Italy to add colour and alcohol. The quality revolution began with Diego Planeta in the 1990s; native varieties have since reclaimed their international reputation.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Nero d'Avola and Grillo showed exceptional concentration and freshness across the island."),
    (2021, "very_good", "stable", "Elegant, balanced vintage; coastal whites particularly successful with excellent aromatic precision."),
    (2020, "excellent", "stable", "Classic Sicilian conditions; Marsala and Zibibbo passito wines of extraordinary richness."),
    (2019, "excellent", "stable", "Benchmark vintage with ideal ripeness and acid balance across all varieties."),
    (2018, "very_good", "stable", "Good vintage; Nero d'Avola from the south showed the most character and depth."),
]:
    VIN(r_sic, yr, qd, pt, sn)

p_mdb = P("Marco de Bartoli", "Italy", r_sic,
           description="The legendary Marsala producer who rescued the appellation's reputation — Marco de Bartoli's Vecchio Samperi and Vigna La Miccia are considered the finest Marsala and Zibibbo wines in Sicily, made without caramelized grape juice addition.")
prod_mdb, new = PROD("Marco de Bartoli Vecchio Samperi", "wine_fortified", p_mdb, r_sic, "Italy",
                     subcategory="Marsala",
                     description="Unfortified solera Marsala Superiore — amber, complex, and oxidative. Dried fig, walnut, orange peel, and ancient wood. An anti-Marsala that proves what the appellation should always have been.",
                     price_tier="premium")
if new:
    PAIR(prod_mdb, "Cannoli Siciliani with fresh ricotta and pistachios", "complement", "classic", "dessert", "Marsala's oxidative fig character and nut complexity echoes the cannoli's ricotta sweetness; regional pairing of deep authenticity")
    PAIR(prod_mdb, "Arancini with ragu and peas", "complement", "established", "amuse", "The wine's nutty, oxidative richness bridges the fried crust and ragu; a classic Sicilian aperitivo pairing")

p_pla = P("Planeta", "Italy", r_sic,
           description="The estate that transformed Sicily's international reputation. Diego Planeta's family winery proved that Sicily could produce world-class wines from both international and indigenous varieties. Now the island's most important quality ambassador.")
prod_pla, new = PROD("Planeta Nero d'Avola", "wine_still", p_pla, r_sic, "Italy",
                     subcategory="Nero d'Avola",
                     description="Benchmark Sicilian red from the variety that defines the island's character — dark cherry, wild herbs, leather, and Mediterranean warmth with firm tannins and a long finish.",
                     price_tier="mid_range")
if new:
    PAIR(prod_pla, "Grilled tuna steak with caponata and basil oil", "complement", "classic", "main", "Sicilian tradition pairs Nero d'Avola with tuna; the wine's dark fruit and herb notes complement the caponata's sweet-sour character")
    PAIR(prod_pla, "Pasta alla Norma with fried eggplant and ricotta salata", "complement", "classic", "main", "Regional pairing of deep authenticity — the wine's dark fruit and warmth mirrors this Catanese classic")

# ── FRIULI-VENEZIA GIULIA ────────────────────────────────────────
print("\n=== Friuli-Venezia Giulia ===")
r_fri = R("Friuli-Venezia Giulia", "Italy", "wine",
           designation_type="DOC",
           designation_name="Friuli DOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Northeast Italian wine region bordering Slovenia and Austria, producing Italy's most refined white wines from Friulano, Malvasia Istriana, Ribolla Gialla, and Pinot Grigio. Also birthplace of the modern orange wine movement through Josko Gravner and Stanko Radikon.",
           key_producers="Josko Gravner, Radikon, Livio Felluga, Marco Felluga, Edi Keber",
           historical_context="Friuli was divided between Italy and Yugoslavia until 1947; the Collio and Carso sub-zones touch Slovenia. Livio Felluga created the iconic map-label Friulano in the 1960s; Gravner and Radikon pioneered skin-contact white wines in the 1990s that created a global movement.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Ribolla Gialla and skin-contact whites of extraordinary complexity."),
    (2021, "very_good", "stable", "Elegant vintage with good acid retention; Friulano and Malvasia showed exceptional aromatic finesse."),
    (2020, "exceptional", "rising", "The finest Friuli vintage of the decade; Gravner and Radikon produced epochal orange wines."),
    (2019, "excellent", "stable", "Benchmark vintage; Collio whites showed the region at its most precise and mineral."),
    (2018, "very_good", "stable", "Good conditions; all sub-zones produced characterful, site-expressive wines."),
]:
    VIN(r_fri, yr, qd, pt, sn)

p_rad = P("Radikon", "Italy", r_fri,
           description="Stanko Radikon's legendary estate in Oslavia producing radical, uncompromising skin-contact white wines from Ribolla Gialla and Oslavia blend. His wines require years of aging and challenge every white wine assumption.")
prod_rad, new = PROD("Radikon Ribolla Gialla", "wine_still", p_rad, r_fri, "Italy",
                     subcategory="Ribolla Gialla",
                     description="Extended skin-contact Ribolla Gialla — amber, tannic, and deeply complex. Dried apricot, orange peel, tea tannins, and volcanic mineral intensity. Requires 5-10 years of cellaring.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_rad, "Roasted pork with fennel and apple sauerkraut", "complement", "classic", "main", "The wine's tannins cut through the pork fat; oxidative complexity embraces the fermented cabbage acidity")
    PAIR(prod_rad, "Frico Friulano (cheese and potato cake) with aged Montasio", "complement", "classic", "main", "Regional pairing of perfect affinity — Oslavia Ribolla and the FVG cheese cake are ancient neighbours; tannins cut the richness")

p_lf = P("Livio Felluga", "Italy", r_fri,
          description="The historic family estate that helped define modern Friulian white wine identity. The iconic map-label Terre Alte blend remains one of Italy's finest whites — Friulano, Sauvignon Blanc, and Pinot Bianco from prized Collio terraces.")
prod_lf, new = PROD("Livio Felluga Terre Alte", "wine_still", p_lf, r_fri, "Italy",
                    subcategory="Friulano",
                    description="Benchmark white blend of Friulano, Sauvignon Blanc, and Pinot Bianco from limestone-marl Collio terraces. Complex, age-worthy, and quintessentially Friulian — white stone fruit, bitter almond, citrus, and mineral length.",
                    price_tier="premium")
if new:
    PAIR(prod_lf, "San Daniele prosciutto with figs and grissini", "complement", "classic", "aperitif", "Friulano's bitter almond character and mineral length make it the classic partner for the region's prized cured ham")
    PAIR(prod_lf, "Pan-roasted sea scallops with brown butter and capers", "complement", "established", "starter", "The wine's citrus-mineral precision cuts through the butter; bitter almond echoes the scallop's natural sweetness")

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
