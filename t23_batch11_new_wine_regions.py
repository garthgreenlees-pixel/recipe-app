#!/usr/bin/env python3
"""T23 Batch 11 — New wine regions: Tasmania, Goriska Brda (Slovenia), Ararat Valley (Armenia), Thrace (Bulgaria), King Valley (Australia)"""

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

# ── TASMANIA GI (AUSTRALIA) ──────────────────────────────────────
print("\n=== Tasmania GI ===")
r_tas = R("Tasmania", "Australia", "wine",
           designation_type="GI",
           designation_name="Tasmania GI",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Australia's coolest and southernmost wine region, producing the country's finest Pinot Noir, Chardonnay, and traditional method sparkling wines. The maritime climate, ancient soils, and extreme cool temperatures create wines of European elegance that contrast sharply with mainland Australia's warm-climate styles.",
           key_producers="Tolpuddle, Bay of Fires, Domaine A, Stefano Lubiana, Josef Chromy",
           historical_context="Tasmania's wine history began with Diego Bernacchi in the 1880s. The modern era started with Andrew Pirie's Pipers Brook in 1974. The region's international recognition grew through the 2000s as mainland producers purchased Tasmania grapes for their sparkling wine blends.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Tasmanian vintage; Pinot Noir of extraordinary elegance and sparkling base wines of exceptional finesse."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; Chardonnay showed remarkable Burgundian character and precision."),
    (2020, "exceptional", "rising", "Finest Tasmanian vintage in the modern era; Tolpuddle and Domaine A produced internationally acclaimed Pinot Noir."),
    (2019, "excellent", "stable", "Benchmark year; continental critics placed Tasmanian Pinot among the world's finest cool-climate expressions."),
    (2018, "very_good", "stable", "Solid vintage; the maritime influence produced wines of haunting mineral freshness."),
]:
    VIN(r_tas, yr, qd, pt, sn)

p_tol = P("Tolpuddle Vineyard", "Australia", r_tas,
           description="The Coal River Valley's benchmark estate, owned by Shaw + Smith, producing Tasmania's most internationally acclaimed Pinot Noir and Chardonnay. Vineyard manager Carlos Souris's meticulous viticulture produces some of Australia's finest cool-climate wines.")
prod_tol, new = PROD("Tolpuddle Vineyard Pinot Noir", "wine_still", p_tol, r_tas, "Australia",
                     subcategory="Pinot Noir",
                     description="The pinnacle of Tasmanian Pinot Noir — haunting, transparent, and complex. Wild strawberry, forest floor, iron, and the distinctive cool-climate Tasmanian mineral character. Compared to the world's finest Burgundy.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_tol, "Duck breast with pomegranate reduction and wild mushroom ragout", "complement", "classic", "main", "Tasmanian Pinot's cherry and forest floor character is the perfect partner for duck; pomegranate acidity echoes the wine's transparency")
    PAIR(prod_tol, "Pan-roasted abalone with brown butter and Tasmanian sea vegetables", "complement", "classic", "main", "Island produce and island wine — abalone's umami intensity is lifted by Pinot's silky acidity; coastal mineral notes find resonance")

p_dom = P("Domaine A", "Australia", r_tas,
           description="Peter Althaus's Cabernet Sauvignon specialist in the Coal River Valley — the only significant Cabernet in Tasmania. Domaine A and Stony Vineyard Cabernet are considered Tasmania's most distinctive non-Pinot wines, demanding long cellaring.")
prod_dom, new = PROD("Domaine A Pinot Noir", "wine_still", p_dom, r_tas, "Australia",
                     subcategory="Pinot Noir",
                     description="Peter Althaus's cool-climate Pinot Noir from deep volcanic soils — delicate, complex, and age-worthy. Red cherry, dried herb, mineral depth, and the Tasmanian characteristic of extraordinary acid freshness.",
                     price_tier="premium")
if new:
    PAIR(prod_dom, "Ocean trout with dashi butter and shaved truffle", "complement", "established", "main", "The wine's delicate transparency complements rather than dominates the ocean trout; the truffle echoes the wine's earthy complexity")
    PAIR(prod_dom, "Roasted beet and goat cheese terrine with walnut vinaigrette", "complement", "established", "starter", "Cool-climate Pinot's wild strawberry and mineral transparency mirrors the beet's earthy sweetness; goat cheese acidity lifts both")

# ── GORISKA BRDA (SLOVENIA) ──────────────────────────────────────
print("\n=== Goriska Brda (Slovenia) ===")
r_brd = R("Goriska Brda", "Slovenia", "wine",
           designation_type="PDO",
           designation_name="Goriska Brda PDO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Slovenia's premier wine sub-region in the Brda hills bordering Collio DOC in Italy — indeed, the same producers sometimes work on both sides of the border. Rebula (Ribolla Gialla), Malvazija, Chardonnay, and Merlot thrive on marl and limestone terraces producing wines of European elegance and complexity.",
           key_producers="Movia, Edi Simcic, Marjan Simcic, Kabaj, Klinec",
           historical_context="Brda shares its terroir and winemaking culture with Italy's Collio — the border is political, not geological. Ales Kristancic of Movia became internationally famous for his pétillant naturel and amphora wines; Edi Simcic's Rebula proved the variety's world-class potential.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Brda vintage; Rebula and Malvazija showed extraordinary mineral precision from the marl-limestone terroirs."),
    (2021, "very_good", "stable", "Elegant vintage; the Brda hills' cooler conditions produced wines of refined aromatic character."),
    (2020, "exceptional", "rising", "Finest Goriska Brda vintage of the modern era; Movia and Edi Simcic produced internationally acclaimed wines."),
    (2019, "excellent", "stable", "Benchmark year; skin-contact Rebula attracted major international natural wine attention."),
    (2018, "very_good", "stable", "Solid vintage; the Brda's marl soils delivered mineral-driven whites of excellent aging potential."),
]:
    VIN(r_brd, yr, qd, pt, sn)

p_edis = P("Edi Simcic", "Slovenia", r_brd,
            description="The benchmark Goriska Brda estate producing Rebula, Malvazija, and Chardonnay of extraordinary quality from marl and limestone terraces. Edi Simcic's wines are considered Slovenia's finest and are collected internationally.")
prod_edis, new = PROD("Edi Simcic Rebula", "wine_still", p_edis, r_brd, "Slovenia",
                      subcategory="Rebula",
                      description="Slovenia's finest Rebula (Ribolla Gialla) from old limestone-marl vines — golden, complex, and textural. Bitter almond, apricot, citrus, and the distinctive mineral precision of the Brda marl. Age-worthy and profound.",
                      price_tier="premium")
if new:
    PAIR(prod_edis, "Prosciutto Karst with melon and fresh basil", "complement", "classic", "aperitif", "Slovenian wine and local cured meat — Rebula's bitter almond and saline character cuts through the prosciutto fat; a cross-border regional tradition")
    PAIR(prod_edis, "Pan-roasted branzino with lemon, capers, and olive oil", "complement", "classic", "main", "Rebula's mineral intensity and bitter almond character is the ideal foil for Mediterranean fish; citrus notes mirror the lemon")

p_mov = P("Movia", "Slovenia", r_brd,
           description="Ales Kristancic's legendary and provocative Brda estate, producing natural, unfiltered wines including the famous pétillant naturel opened in the Adriatic Sea. Movia is Slovenia's most internationally known wine producer.")
prod_mov, new = PROD("Movia Lunar Rebula", "wine_still", p_mov, r_brd, "Slovenia",
                     subcategory="Rebula",
                     description="Ales Kristancic's skin-contact Rebula — amber, textured, and wildly complex. The extended maceration produces a wine of extraordinary character: dried apricot, walnut, orange peel, and the Brda marl's mineral core.",
                     price_tier="premium")
if new:
    PAIR(prod_mov, "Grilled octopus with olive oil, lemon, and wild herbs", "complement", "established", "main", "The amber wine's textural complexity and bitter character bridges the octopus's oceanic depth; wild herbs mirror the wine's aromatic complexity")
    PAIR(prod_mov, "Aged pecorino with truffle honey and walnuts", "complement", "established", "cheese", "Skin-contact Rebula's walnut and oxidative complexity is a natural partner for aged sheep's cheese; truffle honey bridges the bitter almond notes")

# ── ARARAT VALLEY (ARMENIA) ──────────────────────────────────────
print("\n=== Ararat Valley (Armenia) ===")
r_ara = R("Ararat Valley", "Armenia", "wine",
           designation_type="PDO",
           designation_name="Ararat Valley PDO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="The cradle of wine civilization, with archaeological evidence of winemaking dating to 6100 BCE (Areni-1 cave). Armenia's Ararat Valley and Vayots Dzor produce wines from the world's oldest winemaking traditions — Areni Noir, Kangun, and other ancient varieties grown on volcanic basalt and limestone at 900-1800m altitude.",
           key_producers="Zorah Wines, Voskevaz, Van Ardi, Karas, Armenia Wine",
           historical_context="The Areni-1 cave in the Vayots Dzor mountains yielded evidence of the world's oldest wine press (6100 BCE) — predating Georgia's ceramic evidence by 600 years. Armenian wine was suppressed under Soviet rule when the country specialized in brandy production. Post-independence revival since 2000 has brought ancient Areni Noir to international attention.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding vintage; Areni Noir from the ancient Vayots Dzor slopes showed extraordinary transparency and mineral depth."),
    (2021, "very_good", "stable", "Elegant high-altitude vintage; volcanic basalt soils delivered wines of haunting aromatic precision."),
    (2020, "excellent", "stable", "Benchmark year; Zorah Karasi and Van Ardi Areni attracted international critical acclaim."),
    (2019, "excellent", "rising", "Landmark vintage for Armenian wine; international sommeliers discovered Areni Noir for the first time."),
    (2018, "very_good", "stable", "Solid vintage; the ancient vine material produced wines of distinctive character at all quality levels."),
]:
    VIN(r_ara, yr, qd, pt, sn)

p_zor = P("Zorah Wines", "Armenia", r_ara,
           description="Italian fashion designer Alberto Zarinian's pioneering estate that introduced Armenian wine to the world. Zorah's Karasi Areni Noir — made in ancient qvevri clay jars — is considered Armenia's greatest wine and one of the world's most distinctive reds.")
prod_zor, new = PROD("Zorah Karasi Areni Noir", "wine_still", p_zor, r_ara, "Armenia",
                     subcategory="Areni Noir",
                     description="Ancient qvevri-fermented Areni Noir from 80-year-old vines on volcanic basalt at 1400m — translucent ruby, wild cherry, pomegranate, dried herbs, and volcanic mineral intensity. One of the world's most unique red wines.",
                     price_tier="premium")
if new:
    PAIR(prod_zor, "Lamb khorovats (barbecue) with herbs and lavash bread", "complement", "classic", "main", "Armenia's prized barbecue tradition and its finest wine — the lamb's char echoes the wine's smoky volcanic character; pomegranate finds resonance")
    PAIR(prod_zor, "Manti (lamb dumplings) with yogurt, butter, and sumac", "complement", "established", "main", "The wine's transparency and pomegranate acidity complement the dumpling's lamb richness; yogurt mirrors the wine's tangy mineral edge")

p_van = P("Van Ardi Winery", "Armenia", r_ara,
           description="Artisan Armenian estate producing Areni Noir and Kangun from ancient high-altitude vineyards. Van Ardi's commitment to indigenous varieties and traditional techniques makes it one of Armenia's most authentic wine producers.")
prod_van, new = PROD("Van Ardi Areni Noir Reserve", "wine_still", p_van, r_ara, "Armenia",
                     subcategory="Areni Noir",
                     description="Oak-aged Areni Noir from ancient vineyards — darker and more structured than the qvevri style. Dark cherry, dried rose petal, volcanic mineral, and earthy tannins with good aging potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_van, "Tolma (stuffed grape leaves) with lamb and rice in tomato broth", "complement", "classic", "main", "Grape leaf-wrapped lamb and Areni Noir — a poetic Armenian pairing; the wine's cherry and herb notes mirror the stuffed leaves' aromatics")
    PAIR(prod_van, "Roasted eggplant with pomegranate molasses, garlic, and walnuts", "complement", "established", "starter", "The wine's pomegranate character finds direct resonance; volcanic minerals mirror the eggplant's smoky depth")

# ── THRACE (BULGARIA) ────────────────────────────────────────────
print("\n=== Thrace (Bulgaria) ===")
r_thr = R("Thrace", "Bulgaria", "wine",
           designation_type="PDO",
           designation_name="Thrace Valley PDO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Bulgaria's premier wine region in the Thracian plain between the Balkan and Rhodope mountains, producing powerful reds from Mavrud, Rubin, Cabernet Sauvignon, and Merlot. The fertile plains and continental climate create wines of dark fruit intensity and good structure.",
           key_producers="Bessa Valley, Villa Yustina, Angel's Estate, Zagreus, Todoroff",
           historical_context="Thrace was the heartland of Dionysus — ancient Greek mythology placed wine's divine patron in these lands. Communist-era Bulgaria exported vast quantities of cheap Cabernet Sauvignon to the UK; post-1989 investment from international buyers including Stephan von Neipperg (Bessa Valley) transformed quality.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Thrace vintage; Mavrud and Cabernet Sauvignon of exceptional depth and structure."),
    (2021, "very_good", "stable", "Elegant vintage; the Rhodope foothills produced wines of greater refinement than usual."),
    (2020, "excellent", "stable", "Benchmark year; Bessa Valley's Enira achieved cult status at international wine auctions."),
    (2019, "excellent", "rising", "Landmark vintage for Bulgarian wine; international recognition grew significantly."),
    (2018, "very_good", "stable", "Solid vintage; indigenous Mavrud showed its best expression in years."),
]:
    VIN(r_thr, yr, qd, pt, sn)

p_bel = P("Bessa Valley Winery", "Bulgaria", r_thr,
           description="The estate that transformed Bulgaria's international wine reputation, founded with investment from Stephan von Neipperg (owner of Canon-la-Gaffeliere in Saint-Emilion). Enira and Enira Reserva are considered Bulgaria's finest wines.")
prod_bel, new = PROD("Bessa Valley Enira Reserva", "wine_still", p_bel, r_thr, "Bulgaria",
                     subcategory="Mavrud Blend",
                     description="Bulgaria's most internationally acclaimed red wine — Mavrud, Merlot, Cabernet Sauvignon, and Syrah from Thrace's deep clay soils. Dark plum, blackberry, tobacco, and earthy complexity with structured tannins and genuine aging potential.",
                     price_tier="premium")
if new:
    PAIR(prod_bel, "Slow-braised veal with wild mushrooms and butter polenta", "complement", "classic", "main", "The wine's dark fruit and tobacco complexity handles the veal richness; wild mushrooms echo the Mavrud's earthy depth")
    PAIR(prod_bel, "Shopska salad with feta, tomato, and cucumber", "complement", "established", "starter", "Bulgarian red wine and Bulgarian national salad — the wine's dark fruit contrasts with the fresh vegetables; feta's salt lifts the wine's depth")

p_tod = P("Todoroff Wines", "Bulgaria", r_thr,
           description="Kaloyan Todoroff's premium Thrace estate dedicated to both indigenous Bulgarian varieties and international grapes. Todoroff's Rubin and Reserve Mavrud have established the producer as one of Bulgaria's finest.")
prod_tod, new = PROD("Todoroff Reserve Mavrud", "wine_still", p_tod, r_thr, "Bulgaria",
                     subcategory="Mavrud",
                     description="Bulgaria's ancient indigenous variety at its finest — Mavrud produces wines of dark color, high tannin, and earthy complexity reminiscent of the great southern Italian varieties. Blackberry, dried plum, herbs, and iron minerality.",
                     price_tier="mid_range")
if new:
    PAIR(prod_tod, "Kavarma (slow-cooked pork with peppers and onions)", "complement", "classic", "main", "Bulgaria's traditional clay-pot pork dish and indigenous Mavrud is a pairing of centuries; the wine's tannins handle the rich braising")
    PAIR(prod_tod, "Grilled lamb chops with red pepper lutenitsa and flatbread", "complement", "established", "main", "Mavrud's dark fruit and earthy character mirrors the roasted pepper condiment; the wine's structure matches the lamb")

# ── KING VALLEY (AUSTRALIA) ──────────────────────────────────────
print("\n=== King Valley (Australia) ===")
r_kng = R("King Valley", "Australia", "wine",
           designation_type="GI",
           designation_name="King Valley GI",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Victoria's alpine wine region at 150-900m altitude northeast of Melbourne, populated largely by Italian immigrant families who planted indigenous Italian varieties. The region is unique in Australia for producing Prosecco, Sangiovese, Barbera, and Verduzzo from traditional Italian varieties — often described as 'little Italy in the mountains'.",
           key_producers="Dal Zotto, Pizzini, Brown Brothers, Sam Miranda, King River Estate",
           historical_context="Italian immigrants arrived in the King Valley in the 1890s to work in tobacco farming. When tobacco collapsed in the 1980s, families like the Dal Zottos and Pizzinis turned to winemaking with Italian varieties from their heritage. The region pioneered Australian Prosecco and now produces some of Australia's most distinctive varietal wines.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding high-altitude vintage; Italian varieties showed exceptional varietal character and freshness."),
    (2021, "very_good", "stable", "Classic cool-mountain vintage; Prosecco and Sangiovese both excelled."),
    (2020, "excellent", "stable", "Benchmark year; Dal Zotto and Pizzini produced their finest Italian varietal wines."),
    (2019, "excellent", "stable", "Outstanding vintage; Verduzzo and Barbera from this year showed remarkable depth."),
    (2018, "very_good", "stable", "Solid vintage; the alpine conditions produced the most elegant Sangiovese the region had achieved."),
]:
    VIN(r_kng, yr, qd, pt, sn)

p_dal = P("Dal Zotto Wines", "Australia", r_kng,
           description="The Dal Zotto family's Italian heritage shines through their King Valley winery — Australia's benchmark producer of Prosecco, Barbera, and Arneis. Their Col Fondo Prosecco pioneered the traditional pet-nat style in Australia.")
prod_dal, new = PROD("Dal Zotto Pucino Prosecco Col Fondo", "wine_sparkling", p_dal, r_kng, "Australia",
                     subcategory="Prosecco",
                     description="Australia's finest Col Fondo (pet-nat) Prosecco from the King Valley — cloudy, textural, and lively. Green apple, pear, lemon, and a gentle yeasty complexity that distinguishes it from filtered Prosecco. True to Italian heritage.",
                     price_tier="mid_range")
if new:
    PAIR(prod_dal, "Prosciutto crudo with fresh figs and burrata", "complement", "classic", "aperitif", "Italian-Australian Prosecco and Italian-style charcuterie — the wine's fine bubbles and pear character lifts the prosciutto fat; fig's sweetness bridges")
    PAIR(prod_dal, "Antipasto board with grilled zucchini, olives, and buffalo mozzarella", "complement", "established", "amuse", "The wine's lively acidity and green fruit character refresh through each antipasto element; yeasty complexity adds depth")

p_piz = P("Pizzini Wines", "Australia", r_kng,
           description="Alfred and Katrina Pizzini's estate is the heart of Italian winemaking culture in the King Valley. Their Sangiovese, Barbera, and Verduzzo express the Italian grape varieties in Australian conditions with genuine authenticity.")
prod_piz, new = PROD("Pizzini Sangiovese", "wine_still", p_piz, r_kng, "Australia",
                     subcategory="Sangiovese",
                     description="Australia's benchmark Sangiovese from the alpine King Valley — bright cherry, dried herbs, and the characteristic Italian acidity of this noble variety. Lighter than Tuscan counterparts but with genuine varietal character.",
                     price_tier="mid_range")
if new:
    PAIR(prod_piz, "Spaghetti alla Bolognese with Parmigiano Reggiano", "complement", "classic", "main", "Australian-Italian Sangiovese and the Emilian ragu — the wine's acidity cuts through the meat sauce; cherry fruit mirrors the tomato's brightness")
    PAIR(prod_piz, "Pizza Margherita with San Marzano tomato and buffalo mozzarella", "complement", "classic", "main", "Sangiovese and Neapolitan pizza — acidity mirrors the tomato; cherry fruit and herbs complement the basil; a pan-Italian pairing")

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
