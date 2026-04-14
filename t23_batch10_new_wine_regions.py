#!/usr/bin/env python3
"""T23 Batch 10 — New wine regions: Cyprus, Romania (Dealu Mare), Vienna DAC, Istria, Eger (Hungary)"""

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

# ── CYPRUS (COMMANDARIA) ─────────────────────────────────────────
print("\n=== Cyprus (Commandaria) ===")
r_cyp = R("Cyprus", "Cyprus", "wine",
           designation_type="PDO",
           designation_name="Commandaria PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="One of the world's oldest wine regions with continuous production since at least 800 BCE. Commandaria — made from sun-dried Mavro and Xynisteri grapes on the southern slopes of the Troodos Mountains — is the world's oldest appellation wine still in production. Also producing modern dry wines from Maratheftiko and Xynisteri.",
           key_producers="Kyperounda, Tsiakkas, ETKO, SODAP, Vasilikon",
           historical_context="Commandaria was the wine Richard the Lionheart proclaimed 'the wine of kings and the king of wines' at his Cyprus wedding in 1191. It was the world's first wine with a named appellation — the Commanderie de l'Ordre du Temple in 1200. Production methods have remained essentially unchanged for 800 years.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding conditions on the Troodos foothills; both Commandaria and dry Maratheftiko showed exceptional quality."),
    (2021, "very_good", "stable", "Classic Mediterranean vintage; Xynisteri showed rare mineral freshness from high-altitude sites."),
    (2020, "excellent", "stable", "Benchmark year; Kyperounda and Tsiakkas produced Maratheftiko of extraordinary depth and aging potential."),
    (2019, "excellent", "stable", "Outstanding Troodos vintage; sun-dried Mavro achieved optimal concentration for Commandaria."),
    (2018, "very_good", "stable", "Solid vintage; modern dry wine producers continued to demonstrate the island's quality potential."),
]:
    VIN(r_cyp, yr, qd, pt, sn)

p_eto = P("ETKO Winery", "Cyprus", r_cyp,
           description="One of Cyprus' oldest and largest wine producers, ETKO produces Commandaria and modern varietal wines of consistent quality. Their Alasia Commandaria and varietal Maratheftiko are among the island's finest expressions.")
prod_eto, new = PROD("ETKO Commandaria St John", "wine_dessert", p_eto, r_cyp, "Cyprus",
                     subcategory="Commandaria",
                     description="Traditional sun-dried Commandaria from Mavro and Xynisteri — amber, rich, and complex. Dried fig, raisin, carob, honey, and the characteristic oxidative depth of this ancient wine. One of the Mediterranean's great sweet wines.",
                     price_tier="mid_range")
if new:
    PAIR(prod_eto, "Halloumi cheese with honey, walnuts, and dried fig", "complement", "classic", "cheese", "Cyprus' twin treasures — Commandaria and Halloumi — share the island's salty-sweet identity; honey bridges the wine's dried fruit complexity")
    PAIR(prod_eto, "Baklava with pistachios, orange blossom water, and honey", "complement", "classic", "dessert", "The wine's dried fig and honey character finds its natural partner in the nut pastry; orange blossom harmonizes with the wine's oxidative depth")

p_kyp = P("Kyperounda Winery", "Cyprus", r_cyp,
           description="High-altitude artisan estate at 1400m on the Troodos Mountains producing Cyprus' most refined dry wines. Kyperounda's Petritis Xynisteri and Epos Maratheftiko are considered the finest dry wines the island has produced.")
prod_kyp, new = PROD("Kyperounda Petritis Xynisteri", "wine_still", p_kyp, r_cyp, "Cyprus",
                     subcategory="Xynisteri",
                     description="High-altitude Xynisteri from the Troodos at 1400m — Cyprus' finest indigenous white grape producing wines of cool-climate precision. Citrus, green apple, herb, and the distinctive mountain minerality of the island's highest vineyards.",
                     price_tier="mid_range")
if new:
    PAIR(prod_kyp, "Calamari with lemon, dill, and skordalia", "complement", "classic", "starter", "The wine's citrus and herb character mirrors the Mediterranean preparation; mountain mineral intensity echoes the oceanic squid")
    PAIR(prod_kyp, "Souvlaki chicken with tzatziki and flatbread", "complement", "established", "main", "Cyprus white wine and grilled souvlaki is the island's most natural food-wine pairing; the wine's acidity balances the yogurt garlic")

# ── DEALU MARE (ROMANIA) ─────────────────────────────────────────
print("\n=== Dealu Mare (Romania) ===")
r_dma = R("Dealu Mare", "Romania", "wine",
           designation_type="DO",
           designation_name="Dealu Mare DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Romania's premier red wine region on the southern Carpathian foothills northeast of Bucharest, producing powerful reds from Feteasca Neagra, Cabernet Sauvignon, Merlot, and Burgund Mare (Blaufrankisch). The sub-Carpathian hills with limestone and clay soils create wines of genuine depth.",
           key_producers="Serve, Davino, Budureasca, Cotnari, Stirbey",
           historical_context="Dealu Mare's wine history dates to Dacian times (200 BCE). The region's potential was recognized by French investors in the 19th century. Communist collectivization destroyed quality; since 1989, foreign investment and returning Romanian producers have rebuilt the region's reputation.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Feteasca Neagra showed its finest expression with extraordinary dark fruit complexity."),
    (2021, "very_good", "stable", "Elegant vintage with good acid structure; Davino and Budureasca produced their most refined Feteasca."),
    (2020, "excellent", "stable", "Benchmark year; sub-Carpathian limestone soils delivered wines of exceptional mineral depth."),
    (2019, "excellent", "rising", "Landmark vintage; international collectors discovered Romanian wine for the first time at scale."),
    (2018, "very_good", "stable", "Solid conditions; Cabernet Sauvignon and Merlot showed strong international variety character."),
]:
    VIN(r_dma, yr, qd, pt, sn)

p_dav = P("Davino", "Romania", r_dma,
           description="Romania's most internationally acclaimed estate, founded by Florin Bauer in 1998. Davino's Flamboyant, Purpura Valahica, and single-vineyard Feteasca Neagra wines have won major international competitions and placed Romania on the global wine map.")
prod_dav, new = PROD("Davino Flamboyant", "wine_still", p_dav, r_dma, "Romania",
                     subcategory="Feteasca Neagra",
                     description="Romania's most celebrated red wine — old-vine Feteasca Neagra from limestone-clay Dealu Mare soils. Dark plum, cherry preserve, warm spice, and leather with firm but ripe tannins and excellent aging potential.",
                     price_tier="premium")
if new:
    PAIR(prod_dav, "Slow-braised lamb with wild mushrooms, root vegetables, and sour cream", "complement", "classic", "main", "Romanian slow-cooked lamb and Feteasca Neagra is the region's classic pairing; the wine's dark fruit and spice complement the sour cream's tang")
    PAIR(prod_dav, "Stuffed cabbage rolls (sarmale) with smoked pork and rice", "complement", "classic", "main", "Romania's national dish and national red grape — a pairing of centuries; Feteasca's warm fruit handles the smoked pork intensity")

p_bud = P("Budureasca", "Romania", r_dma,
           description="Modern Dealu Mare estate producing both indigenous and international varieties with French technical expertise. Budureasca's Premium and Origini ranges demonstrate Romania's potential for world-class wine at competitive prices.")
prod_bud, new = PROD("Budureasca Premium Feteasca Neagra", "wine_still", p_bud, r_dma, "Romania",
                     subcategory="Feteasca Neagra",
                     description="Modern Feteasca Neagra aged in French oak — approachable yet complex with dark cherry, vanilla spice, and the variety's characteristic wild herb finish. Romania's most accessible quality expression.",
                     price_tier="mid_range")
if new:
    PAIR(prod_bud, "Mici (grilled minced meat rolls) with mustard and flatbread", "complement", "classic", "main", "Romanian street food and Romanian wine — the wine's fruit and herbs complement the spiced meat; a national pairing of simple authenticity")
    PAIR(prod_bud, "Venison medallions with juniper berry sauce and red currant jam", "complement", "established", "main", "Feteasca's dark fruit and spice character handles the game's intensity; juniper notes mirror the wine's wild herb character")

# ── VIENNA DAC (AUSTRIA) ─────────────────────────────────────────
print("\n=== Vienna DAC (Austria) ===")
r_vie = R("Vienna", "Austria", "wine",
           designation_type="DAC",
           designation_name="Wien DAC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The world's only major capital city with a significant wine-producing area within its limits. The Wiener Gemischter Satz — a legally defined field blend of at least three white varieties grown together — is Vienna's signature contribution to world wine culture. Gruner Veltliner, Riesling, Pinot Blanc, and Chardonnay dominate the vineyards on Vienna's western slopes.",
           key_producers="Mayer am Pfarrplatz, Wieninger, Zahel, Christ, Cobenzl",
           historical_context="Vienna's wine tradition dates to the Roman legions planting vineyards on the Kahlenberg. The Gemischter Satz tradition maintained the city's 19th-century mixed-field planting through periods when varietally labeled wines dominated. Fritz Wieninger revived and championed quality Gemischter Satz in the 1990s, creating DAC status in 2013.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Gemischter Satz blends of extraordinary complexity from the city's finest slopes."),
    (2021, "very_good", "stable", "Elegant Vienna vintage; Riesling and Gruner Veltliner components showed exceptional acid structure."),
    (2020, "excellent", "stable", "Benchmark year; Wieninger and Mayer am Pfarrplatz produced Gemischter Satz of remarkable depth."),
    (2019, "excellent", "stable", "Classic conditions; the Bisamberg terraces delivered wines of distinctive mineral character."),
    (2018, "very_good", "stable", "Solid vintage; urban terroir influence particularly pronounced in the volcanic loess sub-zones."),
]:
    VIN(r_vie, yr, qd, pt, sn)

p_wie = P("Wieninger", "Austria", r_vie,
           description="Fritz Wieninger is the visionary winemaker who revived the Wiener Gemischter Satz tradition and created Vienna DAC. His Gemischter Satz and single-varietal Gruner Veltliner wines are considered Vienna's finest — served at the opera and collected internationally.")
prod_wie, new = PROD("Wieninger Wiener Gemischter Satz DAC", "wine_still", p_wie, r_vie, "Austria",
                     subcategory="Gemischter Satz",
                     description="The definitive Wiener Gemischter Satz from a field blend of Gruner Veltliner, Riesling, Weissburgunder, and Chardonnay grown together. Complex, harmonious, and uniquely Viennese — citrus, white pepper, herb, and mineral depth.",
                     price_tier="premium")
if new:
    PAIR(prod_wie, "Tafelspitz (boiled beef) with horseradish cream and chives", "complement", "classic", "main", "Vienna's most iconic dish and its defining wine — Gemischter Satz's herbal complexity and acidity lift the boiled beef; horseradish mirrors the white pepper")
    PAIR(prod_wie, "Schnitzel Wiener Art with lemon and lingonberry", "complement", "classic", "main", "The canonical Viennese pairing — Gemischter Satz's acidity and herbal character cut through the veal schnitzel's golden crust; lemon finds resonance")

p_may = P("Mayer am Pfarrplatz", "Austria", r_vie,
           description="The historic Vienna winery located in Beethoven's former home, producing traditional Gemischter Satz from ancient vineyards. The Heuriger (wine tavern) culture is preserved here — wine, food, and music in the Viennese tradition.")
prod_may, new = PROD("Mayer am Pfarrplatz Nussberg Reserve Gruner Veltliner", "wine_still", p_may, r_vie, "Austria",
                     subcategory="Gruner Veltliner",
                     description="Powerful reserve Gruner Veltliner from the Nussberg — Vienna's finest single-vineyard site on volcanic loess. White pepper, green herb, citrus, and spicy mineral length. A wine for Beethoven's table.",
                     price_tier="premium")
if new:
    PAIR(prod_may, "White asparagus with hollandaise and Viennese Schinken", "complement", "classic", "main", "Gruner Veltliner and white asparagus is Austria's most celebrated seasonal pairing; the wine's herbal bitterness echoes the asparagus")
    PAIR(prod_may, "Gulasch with beef, paprika, and dark bread", "complement", "established", "main", "Viennese Gruner Veltliner and gulasch — the wine's acidity and pepper character mirror the paprika; a Heuriger classic")

# ── ISTRIA (CROATIA) ─────────────────────────────────────────────
print("\n=== Istria (Croatia) ===")
r_ist = R("Istria", "Croatia", "wine",
           designation_type="PDO",
           designation_name="Istra PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The heart-shaped Adriatic peninsula shared between Croatia and Slovenia, producing Istria's signature white wine — Malvazija Istarska — and compelling reds from Teran (Refosco) on red iron-rich soils. The combination of the Adriatic's moderating influence, red terra rossa soils, and elevated altitude produces wines of remarkable character.",
           key_producers="Roxanich, Damjanovic, Coronica, Clai, Kabola",
           historical_context="Istria's wine history spans 3000 years from Greek and Roman settlement. The peninsula's shared Italian-Croatian heritage is reflected in the varieties and cuisine. Malvazija Istarska became distinct from other Malvasia varieties over centuries of isolation; Teran is unique to these red Karst soils.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Malvazija of exceptional aromatic intensity and Teran showing remarkable depth."),
    (2021, "very_good", "stable", "Elegant Istrian vintage; both white and red varieties showed good acid structure and mineral character."),
    (2020, "excellent", "stable", "Benchmark year; Roxanich and Clai produced natural wines of extraordinary Istrian authenticity."),
    (2019, "excellent", "stable", "Classic Adriatic conditions; terra rossa soils delivered Teran of exceptional iron intensity."),
    (2018, "very_good", "stable", "Solid vintage; Malvazija's characteristic bitter almond and saline character particularly pronounced."),
]:
    VIN(r_ist, yr, qd, pt, sn)

p_rox = P("Roxanich", "Croatia", r_ist,
           description="Mladen Roxanich's unconventional Istrian estate producing extended skin-contact Malvazija and Teran that have made him one of Croatia's most internationally acclaimed natural wine producers. His wines age for years in clay amphorae and old barrels.")
prod_rox, new = PROD("Roxanich Malvazija Istarska", "wine_still", p_rox, r_ist, "Croatia",
                     subcategory="Malvazija Istarska",
                     description="Extended skin-contact Malvazija from Istrian terra rossa — amber, textured, and aromatic. Bitter almond, orange peel, dried apricot, and sea salt with remarkable tannic texture. A compelling natural wine expression.",
                     price_tier="premium")
if new:
    PAIR(prod_rox, "Truffle eggs with Istrian black truffle and aged Paski sir", "complement", "classic", "starter", "Istria's gastronomic treasures unite — the wine's bitter almond and saline character frames the truffle; Paski sir adds a sheep-milk accent")
    PAIR(prod_rox, "Fuzi pasta with wild boar ragu and Istrian truffle", "complement", "classic", "main", "Istrian pasta, Istrian truffle, and Istrian wine — the skin-contact texture handles the wild boar richness; truffle echoes the wine's earthy aromatic depth")

p_dam = P("Damjanovic Winery", "Croatia", r_ist,
           description="Family winery producing authentic Malvazija Istarska and Teran from limestone and terra rossa sub-zones of central Istria. Among Croatia's most consistent and food-friendly estate wines.")
prod_dam, new = PROD("Damjanovic Teran", "wine_still", p_dam, r_ist, "Croatia",
                     subcategory="Teran",
                     description="Powerful Istrian Teran from iron-rich red soils — dark cherry, blackberry, forest herbs, and the characteristic iron-mineral intensity of this unique variety. High acidity and firm tannins demand rich food pairing.",
                     price_tier="mid_range")
if new:
    PAIR(prod_dam, "Lamb shoulder slow-roasted with herbs under the peka", "complement", "classic", "main", "Teran's iron intensity and dark fruit is the traditional Istrian companion for rich roasted meat; the wine's tannins handle the fat")
    PAIR(prod_dam, "Njoki (gnocchi) with Istrian lamb ragu and Paski sir", "complement", "established", "main", "Regional pairing — Istrian gnocchi with lamb and Teran is a dish-wine combination of deep local authenticity")

# ── EGER (HUNGARY) ───────────────────────────────────────────────
print("\n=== Eger (Hungary) ===")
r_ege = R("Eger", "Hungary", "wine",
           designation_type="PDO",
           designation_name="Eger PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Northern Hungary's historic wine region beneath the Bukk mountains, home to Egri Bikaver (Bull's Blood) — Hungary's most famous red wine blend. Kekfrankos (Blaufrankisch), Kadarka, Kekoporto, and international varieties on limestone and volcanic tuff produce powerful, structured reds and elegant whites from Olaszrizling.",
           key_producers="Tamas Dula, Tibor Gal, Kovacs Nimrod, St. Andrea, Demeter Zoltan",
           historical_context="The legend holds that the Turkish besiegers of Eger Castle in 1552 thought the Hungarians' red wine was bull's blood — giving them superhuman strength. The communist era turned Bikaver into cheap red plonk exported throughout Eastern Europe. Since 1989, Tibor Gal, Kovacs Nimrod, and others have restored the wine's dignity.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Eger vintage; Kekfrankos showed exceptional structure and Bikaver blends of remarkable complexity."),
    (2021, "very_good", "stable", "Elegant northern vintage; volcanic tuff soils delivered wines of unusual mineral freshness."),
    (2020, "excellent", "stable", "Classic conditions; the best Egri Bikaver Superior wines needed 5+ years of cellaring."),
    (2019, "excellent", "stable", "Benchmark year; Tibor Gal and Kovacs Nimrod produced single-vineyard Kekfrankos of international quality."),
    (2018, "very_good", "stable", "Solid vintage; Olaszrizling and Pinot Gris whites showed excellent aromatic precision."),
]:
    VIN(r_ege, yr, qd, pt, sn)

p_kni = P("Kovacs Nimrod Winery", "Hungary", r_ege,
           description="Nimrod Kovacs' innovative Eger estate producing both traditional Egri Bikaver and modern varietal wines with contemporary winemaking precision. His GIO single-vineyard Kekfrankos has placed Eger on the international fine wine map.")
prod_kni, new = PROD("Kovacs Nimrod Egri Bikaver Superior", "wine_still", p_kni, r_ege, "Hungary",
                     subcategory="Egri Bikaver",
                     description="Superior-classified Egri Bikaver blending Kekfrankos, Kadarka, Kekoporto, and Merlot from volcanic tuff terraces — dark cherry, pepper, iron, and earthy complexity. Modern Bull's Blood at its finest.",
                     price_tier="mid_range")
if new:
    PAIR(prod_kni, "Beef porkolt with onion, paprika, and sour cream", "complement", "classic", "main", "Hungary's national stew and its national wine — Egri Bikaver's iron and pepper character mirrors the paprika-rich porkolt")
    PAIR(prod_kni, "Slow-roasted pork knuckle with pickled cabbage and horseradish", "complement", "established", "main", "The wine's tannic structure and dark fruit cut through the pork fat; pickled cabbage's acidity mirrors the wine's iron notes")

p_and = P("St. Andrea Winery", "Hungary", r_ege,
           description="George Lator's ambitious estate producing premium Egri Bikaver Superior and single-vineyard Kekfrankos that have attracted international attention. St. Andrea's wines have consistently placed Eger among Hungary's finest wine regions.")
prod_and, new = PROD("St. Andrea Merengeto Kekfrankos", "wine_still", p_and, r_ege, "Hungary",
                     subcategory="Kekfrankos",
                     description="Single-vineyard Kekfrankos (Blaufrankisch) from the Merengeto hillside — dark cherry, raspberry, pepper, and volcanic tuff mineral intensity with the variety's characteristic fresh acidity. Hungary's most elegant red variety.",
                     price_tier="premium")
if new:
    PAIR(prod_and, "Roasted duck with cherry sauce and red cabbage", "complement", "classic", "main", "Kekfrankos' cherry and pepper character finds natural resonance with the cherry sauce; the wine's acidity handles the duck fat")
    PAIR(prod_and, "Wild boar sausage with mustard and dark rye bread", "complement", "established", "main", "The wine's pepper intensity and dark fruit character complements the game sausage; volcanic mineral notes add complexity")

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
