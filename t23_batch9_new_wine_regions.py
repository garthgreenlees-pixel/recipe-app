#!/usr/bin/env python3
"""T23 Batch 9 — New wine regions: Valle de Guadalupe, Nashik, Dalmatia, Villany, Franciacorta"""

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

# ── VALLE DE GUADALUPE (MEXICO) ──────────────────────────────────
print("\n=== Valle de Guadalupe (Mexico) ===")
r_vdg = R("Valle de Guadalupe", "Mexico", "wine",
           designation_type="DO",
           designation_name="Valle de Guadalupe DO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Mexico's most celebrated wine region in Baja California's Ensenada valley, 100km south of San Diego. Mediterranean climate, granite soils, and a generation of adventurous winemakers have created one of the world's most exciting boutique wine destinations. Tempranillo, Nebbiolo, Grenache, and local blends are the signatures.",
           key_producers="Casa de Piedra, Monte Xanic, Adobe Guadalupe, Tres Valles, Vena Cava",
           historical_context="Spanish Dominicans planted the first vines in Baja California in 1701. Modern Valle de Guadalupe began with Cetto in the 1970s; the artisan revolution of the 2000s created boutique estates producing wines that compete internationally. The valley's gastronomy scene has made it a destination for culinary tourism.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Mediterranean conditions produced reds of exceptional concentration and whites of surprising freshness."),
    (2021, "very_good", "stable", "Balanced vintage; Nebbiolo and Tempranillo showed their finest expressions to date."),
    (2020, "excellent", "stable", "Classic Guadalupe conditions; the best artisan producers made wines that rivalled international benchmarks."),
    (2019, "excellent", "rising", "Benchmark vintage; the valley received international attention for the first time at major wine competitions."),
    (2018, "very_good", "stable", "Solid vintage; granite and clay sub-zones both performed well across all major varieties."),
]:
    VIN(r_vdg, yr, qd, pt, sn)

p_cdp = P("Casa de Piedra", "Mexico", r_vdg,
           description="Hugo d'Acosta's legendary estate, founded in 1997, is considered the intellectual heart of Valle de Guadalupe. His Vino de Piedra and Tempranillo blends defined what Mexican wine could be, inspiring a generation of winemakers.")
prod_cdp, new = PROD("Casa de Piedra Vino de Piedra", "wine_still", p_cdp, r_vdg, "Mexico",
                     subcategory="Tempranillo Blend",
                     description="Hugo d'Acosta's benchmark Valle de Guadalupe blend — Tempranillo with Nebbiolo and Grenache from granite soils. Dark cherry, dried fig, tobacco, and savoury spice with the valley's characteristic warmth and structure.",
                     price_tier="premium")
if new:
    PAIR(prod_cdp, "Birria de res tacos with consomme and salsa verde", "complement", "classic", "main", "Mexican red wine and slow-braised beef birria is the valley's quintessential pairing; the wine's structure handles the rich braising")
    PAIR(prod_cdp, "Grilled adobo lamb chops with nopales and queso fresco", "complement", "established", "main", "The wine's dark fruit and tobacco notes harmonize with the adobo-spiced lamb; nopales' acidity mirrors the wine's freshness")

p_mxr = P("Monte Xanic", "Mexico", r_vdg,
           description="One of Valle de Guadalupe's founding quality estates, Monte Xanic has produced consistently award-winning Chardonnay and Merlot since 1987. The estate's cool coastal sites and careful viticulture produce some of Mexico's most refined wines.")
prod_mxr, new = PROD("Monte Xanic Calixa Sauvignon Blanc", "wine_still", p_mxr, r_vdg, "Mexico",
                     subcategory="Sauvignon Blanc",
                     description="Cool-climate Sauvignon Blanc from Guadalupe's coastal sites — citrus, tropical fruit, and herbal freshness unusual in Mexico. One of the valley's finest whites.",
                     price_tier="mid_range")
if new:
    PAIR(prod_mxr, "Ceviche verde with avocado, tomatillo, and serrano", "complement", "classic", "starter", "Sauvignon Blanc's herbal-citrus character mirrors the tomatillo and serrano; the wine's acidity echoes the ceviche's lime")
    PAIR(prod_mxr, "Fish tacos with baja-style cabbage slaw and chipotle crema", "complement", "established", "main", "The wine's tropical fruit and citrus lift the fried fish; herbal notes mirror the cabbage slaw freshness")

# ── NASHIK (INDIA) ───────────────────────────────────────────────
print("\n=== Nashik (India) ===")
r_nas = R("Nashik", "India", "wine",
           designation_type="GI",
           designation_name="Nashik GI",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="India's premier wine region in Maharashtra state, 170km northeast of Mumbai at 600m altitude. Sula Vineyards pioneered premium Indian winemaking here in 1999 and the region now produces 80% of India's wine. Chenin Blanc, Sauvignon Blanc, and Shiraz are the key varieties.",
           key_producers="Sula Vineyards, Fratelli, York Winery, Grover Zampa, Vallonne",
           historical_context="Nashik's modern wine era began with Rajeev Samant and Kerry Damskey's Sula Vineyards in 1999 — a bold experiment that demonstrated Indian viticulture could produce world-competitive wine. The region's altitude, diurnal variation, and basalt soils are comparable to established wine zones globally.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Chenin Blanc and Shiraz showed exceptional aromatics and structure."),
    (2021, "very_good", "stable", "Good conditions despite early monsoon pressure; careful viticulture rewarded with quality results."),
    (2020, "very_good", "stable", "Solid vintage; Sula's vintage-dated Dindori Reserve Shiraz excelled."),
    (2019, "excellent", "rising", "Benchmark year for Indian wine; international recognition at wine competitions increased significantly."),
    (2018, "good", "stable", "Challenging monsoon season; experienced producers who managed canopy carefully made quality wines."),
]:
    VIN(r_nas, yr, qd, pt, sn)

p_sul = P("Sula Vineyards", "India", r_nas,
           description="India's largest and most internationally recognized wine producer, founded by Rajeev Samant in 1999. Sula's Nashik estate pioneered premium Indian wine and is now a major wine tourism destination with over 300,000 annual visitors.")
prod_sul, new = PROD("Sula Vineyards Dindori Reserve Shiraz", "wine_still", p_sul, r_nas, "India",
                     subcategory="Shiraz",
                     description="India's most acclaimed red wine — single-vineyard Shiraz from volcanic basalt soils aged in French oak. Dark plum, blackberry, spice, and tobacco with the warmth characteristic of Indian viticulture but with genuine structure.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sul, "Rogan josh with lamb, whole spices, and basmati rice", "complement", "established", "main", "Indian Shiraz and Indian cuisine is the natural partnership; the wine's spice notes mirror the rogan josh's cardamom and cinnamon")
    PAIR(prod_sul, "Tandoori chicken with mint raita and garlic naan", "complement", "established", "main", "The wine's warm fruit handles the tandoor smoke; Shiraz's plum character bridges the yogurt marinade's tang")

p_fra = P("Fratelli Wines", "India", r_nas,
           description="Italian-Indian joint venture producing premium Nashik wines with Italian winemaking expertise. Fratelli's Sette and Sangiovese from Nashik have demonstrated Indian wine's global ambition.")
prod_fra, new = PROD("Fratelli Sette", "wine_still", p_fra, r_nas, "India",
                     subcategory="Sangiovese Blend",
                     description="Indo-Italian red blend of Sangiovese and Cabernet Sauvignon from Nashik basalt — cherry, tomato leaf, tobacco, and the characteristic Indian warmth. An intriguing East-West wine identity.",
                     price_tier="mid_range")
if new:
    PAIR(prod_fra, "Lamb biryani with saffron, fried onion, and raita", "complement", "established", "main", "The wine's Italian-Indian identity bridges the subcontinent's cuisine; Sangiovese's acidity cuts through the biryani's richness")
    PAIR(prod_fra, "Butter chicken with fenugreek, cream, and tomato", "complement", "established", "main", "The wine's tomato leaf and cherry character finds affinity with the butter chicken's tomato base; acidity cuts the cream")

# ── DALMATIA (CROATIA) ───────────────────────────────────────────
print("\n=== Dalmatia (Croatia) ===")
r_dal = R("Dalmatia", "Croatia", "wine",
           designation_type="PDO",
           designation_name="Dalmatia PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Croatia's most celebrated wine region along the Adriatic coast and islands, producing powerful Plavac Mali (genetically related to Zinfandel) and distinctive indigenous varieties — Posip, Grk, and Bogdanusa from the islands. Ancient vineyards on limestone karst and Mediterranean island terraces.",
           key_producers="Mike Grgich, Saints Hills, Zlatan Otok, Korta Katarina, Tomic",
           historical_context="Dalmatia's wine history spans 2500 years from Greek colonization of Hvar and Vis. DNA analysis proved in 2001 that Zinfandel (California) and Primitivo (Puglia) are genetically identical to Plavac Mali's ancestor Crljenak Kastelanski, linking California's iconic variety to these Dalmatian shores.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Dalmatian vintage; Plavac Mali of exceptional concentration from the steep island terraces."),
    (2021, "very_good", "stable", "Elegant vintage; island wines of unusual freshness and mineral character."),
    (2020, "excellent", "stable", "Benchmark year; Mike Grgich's Plavac and Saints Hills Plavac both achieved international recognition."),
    (2019, "excellent", "stable", "Classic Adriatic conditions; old-vine Plavac from Hvar's south-facing slopes excelled."),
    (2018, "very_good", "stable", "Solid vintage; limestone karst yielded wines of characteristic Dalmatian power and freshness."),
]:
    VIN(r_dal, yr, qd, pt, sn)

p_gri = P("Grgic Vina", "Croatia", r_dal,
           description="Mike Grgich — the Croatian-born winemaker who made the 1973 Chateau Montelena Chardonnay that won the Judgment of Paris — returned to his homeland to produce Plavac Mali and Posip of world-class quality from family vineyards on the Peljesac peninsula.")
prod_gri, new = PROD("Grgic Vina Plavac Mali", "wine_still", p_gri, r_dal, "Croatia",
                     subcategory="Plavac Mali",
                     description="Powerful, structured Plavac Mali from Peljesac's steep limestone terraces — dark cherry, plum, fig, dried herbs, and the saline mineral character of the Adriatic coast. Croatia's most internationally recognized red wine.",
                     price_tier="premium")
if new:
    PAIR(prod_gri, "Peka (lamb under the bell) with root vegetables and rosemary", "complement", "classic", "main", "Croatia's iconic slow-cook dish and Plavac Mali is the Dalmatian pairing of deepest tradition; the wine's power matches the lamb's richness")
    PAIR(prod_gri, "Grilled Adriatic fish (orada) with olive oil, garlic, and capers", "complement", "established", "main", "Despite Plavac's power, coastal wine and coastal fish is a Dalmatian tradition; saline notes in the wine mirror the Adriatic fish")

p_sai = P("Saints Hills Winery", "Croatia", r_dal,
           description="Ambitious Istrian and Dalmatian estate producing premium Plavac Mali from Peljesac and Malvazija from Istria. Internationally acclaimed winemaker Gianfranco Gallo (Vie di Romans) consults. One of Croatia's most exciting estates.")
prod_sai, new = PROD("Saints Hills Nevina Posip", "wine_still", p_sai, r_dal, "Croatia",
                     subcategory="Posip",
                     description="Island white Posip from Korcula — a distinctive indigenous variety producing wines of bright citrus, stone fruit, herbal bitterness, and Adriatic saline mineral character. Croatia's finest white wine variety.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sai, "Grilled langoustines with garlic butter and local herbs", "complement", "classic", "starter", "Island Posip's saline mineral character and citrus acidity is the natural partner for Dalmatian shellfish")
    PAIR(prod_sai, "Black risotto (crni rizot) with cuttlefish and parsley oil", "complement", "established", "main", "Croatian white wine with Croatian seafood risotto — the wine's mineral intensity mirrors the oceanic depth of the cuttlefish ink")

# ── VILLANY (HUNGARY) ────────────────────────────────────────────
print("\n=== Villany (Hungary) ===")
r_vil = R("Villany", "Hungary", "wine",
           designation_type="PDO",
           designation_name="Villany PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Hungary's warmest wine region in the far south on the Croatian border, producing the country's finest reds from Cabernet Franc, Cabernet Sauvignon, Merlot, and the indigenous Portugieser. Deep limestone and clay soils produce wines of exceptional structure and aging potential.",
           key_producers="Attila Gere, Tamas Dula, Vylyan, Csanyi, Bock",
           historical_context="Villany was known for light Portugieser reds in the communist era. After 1989, producers like Attila Gere and Ede Tiffan introduced quality-focused production that transformed the region into Hungary's premier red wine appellation, producing Cabernet Franc that rivals the Loire.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Villany vintage; Cabernet Franc and Merlot achieved exceptional tannin ripeness in the warm southern conditions."),
    (2021, "very_good", "stable", "Elegant vintage; Cabernet Franc showed its most Loire-like expression."),
    (2020, "exceptional", "rising", "The finest Villany vintage in decades; Attila Gere Kopar and Vylyan Premier achieved cult status."),
    (2019, "excellent", "stable", "Benchmark conditions; deep clay soils yielded Cabernet Franc of extraordinary mineral depth."),
    (2018, "very_good", "stable", "Solid vintage; Portugieser and Blaufrankisch blends provided good counterpoint to the international varieties."),
]:
    VIN(r_vil, yr, qd, pt, sn)

p_ger = P("Attila Gere", "Hungary", r_vil,
           description="The godfather of modern Villany wine, Attila Gere has produced Cabernet Franc and Merlot blends of international quality since the early 1990s. His Kopar blend and Kopár single-vineyard wines are Hungary's most celebrated and collected reds.")
prod_ger, new = PROD("Attila Gere Kopar", "wine_still", p_ger, r_vil, "Hungary",
                     subcategory="Cabernet Franc",
                     description="Villany's benchmark Cabernet Franc blend from limestone and clay soils — cassis, dark cherry, graphite, and Mediterranean herbs with firm tannins and a decade of aging potential. Hungary's finest red wine.",
                     price_tier="premium")
if new:
    PAIR(prod_ger, "Slow-roasted Hungarian goose with red cabbage and dumplings", "complement", "classic", "main", "Villany Cabernet Franc and Hungarian festive goose is the region's most celebrated traditional pairing; the wine's structure handles the rich bird")
    PAIR(prod_ger, "Beef goulash with paprika, caraway, and sour cream", "complement", "classic", "main", "Hungarian red wine and Hungarian goulash — the wine's dark fruit mirrors the paprika's depth; its structure cuts through the sour cream")

p_vyl = P("Vylyan Winery", "Hungary", r_vil,
           description="Ambitious Villany estate producing premium Cabernet Franc, Merlot, and Portugieser blends of international quality. Vylyan's Premier cuvee and single-vineyard Brone have established the estate among Hungary's finest.")
prod_vyl, new = PROD("Vylyan Premier", "wine_still", p_vyl, r_vil, "Hungary",
                     subcategory="Cabernet Franc Blend",
                     description="Flagship Villany blend of Cabernet Franc, Merlot, and Cabernet Sauvignon from limestone terraces — structured, age-worthy, and complex. Dark berry, graphite, and Mediterranean spice.",
                     price_tier="premium")
if new:
    PAIR(prod_vyl, "Grilled wild boar with forest mushrooms and juniper berry sauce", "complement", "classic", "main", "Wild game and Villany red is Hungary's classic highland pairing; the wine's tannins and dark fruit handle the game's intensity")
    PAIR(prod_vyl, "Mangalitsa pork with paprika and pickled vegetables", "complement", "established", "main", "Hungary's prized Mangalitsa breed and local Villany red is a natural regional partnership; the wine's structure complements the fat richness")

# ── FRANCIACORTA DOCG ────────────────────────────────────────────
print("\n=== Franciacorta DOCG ===")
r_fra2 = R("Franciacorta", "Italy", "wine",
            designation_type="DOCG",
            designation_name="Franciacorta DOCG",
            reputation_tier="prestigious",
            quality_trajectory="ascending",
            description="Italy's finest sparkling wine appellation in Lombardy south of Lake Iseo, producing traditional method wines from Chardonnay, Pinot Nero, and Pinot Bianco on glacially deposited morainic soils. Italy's answer to Champagne — and increasingly its equal.",
            key_producers="Ca' del Bosco, Bellavista, Guido Berlucchi, Ferghettina, Contadi Castaldi",
            historical_context="Franciacorta's modern wine history begins with Guido Berlucchi's first Italian metodo classico in 1961. DOCG status was granted in 1995 — the only sparkling wine in Italy to achieve this designation. The region's proximity to Milan has made it Italy's prestige celebration wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Chardonnay of exceptional complexity and Pinot Nero showing remarkable depth and color."),
    (2021, "very_good", "stable", "Elegant, classic vintage; morainic minerality particularly pronounced in the top estates."),
    (2020, "exceptional", "rising", "Finest Franciacorta vintage of the decade; Ca' del Bosco and Bellavista produced epochal wines."),
    (2019, "excellent", "stable", "Benchmark year; the morainic soils delivered the most mineral-driven Chardonnay of the decade."),
    (2018, "very_good", "stable", "Solid vintage; non-vintage blends benefited enormously from the reserve wine quality."),
]:
    VIN(r_fra2, yr, qd, pt, sn)

p_cdb = P("Ca' del Bosco", "Italy", r_fra2,
           description="Maurizio Zanella's flagship Franciacorta estate, producing the most internationally recognized Italian sparkling wines. Cuvee Prestige and Dosage Zero are Franciacorta benchmarks; Annamaria Clementi is among Italy's finest sparkling wines.")
prod_cdb, new = PROD("Ca' del Bosco Cuvee Prestige", "wine_sparkling", p_cdb, r_fra2, "Italy",
                     subcategory="Franciacorta Brut",
                     description="Italy's most recognized Franciacorta — Chardonnay, Pinot Bianco, and Pinot Nero from morainic soils. Toasty brioche, green apple, lemon cream, and the distinctive mineral freshness of Italian sparkling wine. Benchmarks Italian quality.",
                     price_tier="premium")
if new:
    PAIR(prod_cdb, "Risotto alla Milanese with saffron and bone marrow", "complement", "classic", "main", "Franciacorta's acidity and mousse cut through the saffron-butter richness; the wine's toasty notes complement the marrow")
    PAIR(prod_cdb, "Lobster alla griglia with burro e salvia (browned butter and sage)", "complement", "classic", "main", "Italian sparkling wine and Italian luxury seafood — the wine's mousse and citrus lift the browned butter; a Milanese special occasion pairing")

p_bel = P("Bellavista", "Italy", r_fra2,
           description="The Moretti family's prestige Franciacorta estate producing long-aged vintage and non-vintage sparkling wines of extraordinary complexity. The Vittorio Moretti Riserva is considered Italy's finest sparkling wine.")
prod_bel, new = PROD("Bellavista Alma Gran Cuvee Brut", "wine_sparkling", p_bel, r_fra2, "Italy",
                     subcategory="Franciacorta Brut",
                     description="Bellavista's non-vintage flagship — predominantly Chardonnay from the estate's finest parcels, aged 30 months minimum. Refined, complex, and mineral — brioche, white flower, citrus zest, and morainic chalk.",
                     price_tier="premium")
if new:
    PAIR(prod_bel, "Bresaola della Valtellina with arugula and Parmigiano shavings", "complement", "classic", "aperitif", "Lombardy's finest sparkling wine with Lombardy's finest cured beef — a regional celebration pairing; the wine's acidity cuts the bresaola's concentration")
    PAIR(prod_bel, "Tartare di branzino with bottarga, lemon, and capers", "complement", "established", "starter", "Franciacorta's mineral precision and fine mousse texture complement the delicate sea bass; bottarga's brininess finds resonance in the wine's saline notes")

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
