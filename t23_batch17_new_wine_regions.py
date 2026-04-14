#!/usr/bin/env python3
"""T23 Batch 17 — New wine regions: Santa Barbara County AVA (USA), Heathcote GI (Australia), Ribeiro DO (Spain), Calabria (Italy), Canary Islands DO (Spain)"""

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

# ── SANTA BARBARA COUNTY AVA (USA) ────────────────────────────────
print("\n=== Santa Barbara County AVA (USA) ===")
r_sba = R("Santa Barbara County", "USA", "wine",
           designation_type="AVA",
           designation_name="Santa Barbara County AVA",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="California's most dramatically cool wine county where the Transverse Ranges create east-west valleys that funnel Pacific Ocean fog and cold air inland, producing Pinot Noir, Chardonnay, and Syrah of surprising elegance in this southern California setting. The Santa Ynez Valley (including Sta. Rita Hills), Happy Canyon, and Santa Maria Valley sub-AVAs each create distinct microclimates. The region gained fame through the 2004 film 'Sideways' which made Santa Barbara Pinot Noir a household name.",
           key_producers="Au Bon Climat, Sanford Winery, Brewer-Clifton, Melville, Bien Nacido Estate",
           historical_context="Santa Barbara County's modern wine era began with Jim Clendenen and Bob Lindquist's discoveries in the 1980s of how cold the Santa Maria Valley was despite its southern latitude. The Transverse mountain range runs east-west (uniquely in California), creating ocean-influenced valleys that would otherwise be too warm for Burgundian varieties. The 2004 film 'Sideways' featuring the Santa Ynez Valley created a Pinot Noir gold rush from which the region still benefits.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Santa Barbara vintage; Sta. Rita Hills Pinot Noir of extraordinary elegance; Chardonnay of Burgundian precision."),
    (2021, "very_good", "stable", "Classic cool-climate vintage; Syrah from the Santa Ynez Valley showed exceptional Rhône-like pepper and dark fruit."),
    (2020, "excellent", "stable", "Benchmark year; Brewer-Clifton and Au Bon Climat produced the finest Pinot Noir and Chardonnay of the decade."),
    (2019, "excellent", "rising", "Outstanding vintage; Sta. Rita Hills Pinot achieved international scores previously unseen in Santa Barbara."),
    (2018, "very_good", "stable", "Solid vintage; Santa Maria Valley Chardonnay showed exceptional mineral freshness; Pinot Noir of good structure."),
]:
    VIN(r_sba, yr, qd, pt, sn)

p_abc = P("Au Bon Climat", "USA", r_sba,
           description="Jim Clendenen's Santa Maria Valley winery, widely credited with putting Santa Barbara County on the international wine map. Au Bon Climat's Isosceles Reserve and single-vineyard Pinot Noir and Chardonnay wines have achieved consistent critical acclaim for four decades. Clendenen's Burgundy-trained palate shaped the region's benchmark style.")
prod_abc, new = PROD("Au Bon Climat Isabelle Chardonnay", "wine_still", p_abc, r_sba, "USA",
                     subcategory="Chardonnay",
                     description="Jim Clendenen's benchmark Santa Barbara Chardonnay from multiple Santa Maria Valley sites — Burgundian in orientation with white peach, hazelnut, lemon curd, struck flint, and the cool coastal minerality that distinguishes Santa Barbara from warmer California regions. Oak-integrated and age-worthy.",
                     price_tier="premium")
if new:
    PAIR(prod_abc, "Butter-poached California Dungeness crab with tarragon and brioche", "complement", "classic", "main", "Santa Barbara Chardonnay and Pacific crab from the same coastal waters — the wine's hazelnut and lemon character mirrors the crab's sweetness; butter mirrors the wine's richness")
    PAIR(prod_abc, "Roasted California halibut with chanterelles, lemon beurre blanc, and chives", "complement", "classic", "main", "West Coast fish and West Coast Chardonnay — the wine's mineral precision and citrus character is the ideal foil for halibut's delicate flesh; chanterelles echo the hazelnut notes")

p_bcl = P("Brewer-Clifton", "USA", r_sba,
           description="Greg Brewer and Steve Clifton's Sta. Rita Hills focused winery producing some of California's most mineral and site-expressive Pinot Noir and Chardonnay. The Sta. Rita Hills' diatomaceous chalky soils and extreme cool climate create wines of startling precision and minerality unlike any other California appellation.")
prod_bcl, new = PROD("Brewer-Clifton Machado Pinot Noir", "wine_still", p_bcl, r_sba, "USA",
                     subcategory="Pinot Noir",
                     description="One of California's most mineral and transparent Pinot Noir from the Sta. Rita Hills' diatomaceous chalk soils — wild strawberry, cranberry, dried rose, chalk dust, and an almost Burgundian restraint that sets this apart from warmer California Pinot. Haunting, linear, and age-worthy.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_bcl, "Grilled Central Coast abalone with lemon brown butter and sea vegetables", "complement", "classic", "main", "Coastal California abalone and the most mineral Santa Barbara Pinot — the wine's chalk and strawberry character bridges the abalone's brine; sea vegetables echo the coastal mineral")
    PAIR(prod_bcl, "Roasted duck breast with fig jam, endive, and pomegranate reduction", "complement", "established", "main", "The wine's mineral precision and wild fruit character is the perfect match for duck's richness; fig provides sweetness to bridge the wine's acid; endive bitterness adds complexity")

# ── HEATHCOTE GI (AUSTRALIA) ──────────────────────────────────────
print("\n=== Heathcote GI (Australia) ===")
r_hea = R("Heathcote", "Australia", "wine",
           designation_type="GI",
           designation_name="Heathcote GI",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Central Victoria's most distinctive wine region at 150-300m altitude on the 550-million-year-old Cambrian-era volcanic Greenstone (metabasalt) and Silurian limestone soils that produce Shiraz of extraordinary distinctiveness. The Cambrian soils — among the world's oldest wine-growing soils — give Heathcote Shiraz a unique combination of dark plum intensity, ironstone minerality, and spice quite unlike Barossa or McLaren Vale expressions.",
           key_producers="Jasper Hill, Sanguine Estate, Greenstone Vineyard, Paul Osicka, Syrahmi",
           historical_context="Heathcote's wine history began in the 1860s gold rush era. The region was largely forgotten until Ron Laughton's Jasper Hill (established 1975) drew attention to the extraordinary character of Shiraz from the ancient Cambrian greenstone. When Jasper Hill's Emily's Paddock and Georgia's Paddock Shiraz began receiving international critical acclaim in the 1980s-90s, the Cambrian soil's uniqueness became a recognised phenomenon in the wine world.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Heathcote vintage; Shiraz from Cambrian Greenstone soils showed extraordinary ironstone mineral character."),
    (2021, "very_good", "stable", "Classic vintage; the ancient Cambrian soils' mineral intensity produced Shiraz of exceptional depth and individuality."),
    (2020, "excellent", "stable", "Benchmark year; Jasper Hill and Sanguine produced Cambrian Shiraz of the highest critical recognition."),
    (2019, "excellent", "rising", "Outstanding vintage; Heathcote's ancient soils produced Shiraz of extraordinary concentration and mineral distinction."),
    (2018, "very_good", "stable", "Solid vintage; the greenstone's iron and basalt minerals expressed themselves with great clarity in the Shiraz."),
]:
    VIN(r_hea, yr, qd, pt, sn)

p_jas = P("Jasper Hill", "Australia", r_hea,
           description="Ron and Elva Laughton's biodynamic Heathcote estate producing Emily's Paddock and Georgia's Paddock Shiraz from the ancient Cambrian greenstone — considered among Australia's finest single-vineyard red wines. The two paddocks produce distinctly different Shiraz styles from the same family of ancient soils; both demand 10-15 years of aging to reveal their full complexity.")
prod_jas, new = PROD("Jasper Hill Georgia's Paddock Shiraz", "wine_still", p_jas, r_hea, "Australia",
                     subcategory="Shiraz",
                     description="One of Australia's most distinctive and age-worthy Shiraz from the ancient Cambrian greenstone — dense, mineral, and unlike any other Australian red. Dark plum, ironstone, pepper, licorice, dark chocolate, and an earthy minerality that reflects 550 million years of volcanic history in every glass.",
                     price_tier="premium")
if new:
    PAIR(prod_jas, "Braised Victorian lamb shank with root vegetables, thyme, and red wine reduction", "complement", "classic", "main", "Victoria's pastoral heritage and its most mineral Shiraz — the wine's ironstone and plum character mirrors the slow-braised lamb; thyme bridges the wine's herbal complexity")
    PAIR(prod_jas, "Wood-fired venison medallion with juniper, beetroot purée, and crispy kale", "complement", "established", "main", "Game and Cambrian Shiraz — the wine's mineral intensity handles venison's gaminess; juniper echoes the wine's spice; beetroot mirrors the iron mineral character")

p_san = P("Sanguine Estate", "Australia", r_hea,
           description="Mark and Linda Hunter's Heathcote estate producing benchmark Cambrian Greenstone Shiraz alongside the innovative Progeny Sangiovese. The Hunter family's commitment to the ancient Cambrian terroir has produced Heathcote Shiraz of consistent excellence and site expression.")
prod_san, new = PROD("Sanguine Estate Heathcote Shiraz", "wine_still", p_san, r_hea, "Australia",
                     subcategory="Shiraz",
                     description="Heathcote's most accessible Cambrian Greenstone Shiraz — dark plum, blackberry, ironstone mineral, and the characteristic earthy depth of ancient volcanic soils. More approachable than Jasper Hill in youth, with the same distinctive regional mineral character that makes Heathcote Shiraz unique in Australia.",
                     price_tier="mid_range")
if new:
    PAIR(prod_san, "Slow-cooked beef cheeks with potato mash, horseradish cream, and gremolata", "complement", "classic", "main", "Rich braised beef and mineral Shiraz — the wine's ironstone and plum character handles the gelatinous beef; horseradish cuts through the richness; gremolata bridges the herb notes")
    PAIR(prod_san, "Australian hard cheese (12-month Yarra Valley cheddar) with fruit paste", "complement", "established", "cheese", "The wine's dark mineral character finds resonance in aged cheddar; fruit paste bridges the Shiraz's plum notes; a distinctly Australian cheese board pairing")

# ── RIBEIRO DO (SPAIN) ────────────────────────────────────────────
print("\n=== Ribeiro DO (Spain) ===")
r_rib = R("Ribeiro", "Spain", "wine",
           designation_type="DO",
           designation_name="Ribeiro DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Galicia's oldest wine DO in the Miño and Avia river valleys, producing aromatic, mineral whites from the indigenous Treixadura, Godello, and Albariño varieties on granite and schist soils. Ribeiro whites — often more complex and less international in style than Rías Baixas Albariño — express the Galician coast's Atlantic influence with greater textural weight and indigenous character. The red variety Mencía produces lighter, floral wines of excellent food-pairing ability.",
           key_producers="Emilio Rojo, Viña Mein, Coto de Gomariz, Pazo do Mar, Adega do Moucho",
           historical_context="Ribeiro was Galicia's most important wine region before Rías Baixas gained international fame in the 1990s. The region's wines traveled from the Galician ports to Northern Europe during the medieval era — English merchants referred to 'wines of Ribadavia' (Ribeiro's capital). Emilio Rojo's obsession with indigenous varieties and estate wines in the 1990s triggered a quality revolution that continues today.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Ribeiro vintage; Treixadura and Godello from granite soils showed extraordinary aromatic complexity."),
    (2021, "very_good", "stable", "Elegant Atlantic vintage; the Miño Valley's river influence produced wines of exceptional freshness and mineral vitality."),
    (2020, "excellent", "stable", "Benchmark year; Emilio Rojo and Coto de Gomariz produced internationally acclaimed single-variety Treixadura."),
    (2019, "very_good", "rising", "Outstanding vintage; Treixadura's aromatic intensity and Godello's textural complexity both excelled."),
    (2018, "very_good", "stable", "Solid vintage; Ribeiro's Atlantic humidity produced wines of good freshness and the characteristic mineral vitality."),
]:
    VIN(r_rib, yr, qd, pt, sn)

p_emr = P("Emilio Rojo", "Spain", r_rib,
           description="Galicia's most obsessive and sought-after natural wine producer — Emilio Rojo's tiny estate in Arnoia produces a single Ribeiro Blanco from Treixadura, Lado, Torrontés, and Albariño of extraordinary complexity and aging potential. His wine is Spain's most sought-after white wine allocated globally to a tiny list of restaurants and collectors.")
prod_emr, new = PROD("Emilio Rojo Ribeiro Blanco", "wine_still", p_emr, r_rib, "Spain",
                     subcategory="Treixadura Blend",
                     description="Spain's most sought-after and allocated white wine — a multi-vintage blend of Treixadura, Lado, Torrontés, and Albariño from old granite vines. Extraordinary complexity: apricot, dried herbs, beeswax, granite mineral, and a textural weight that develops magnificently over 10-15 years. One of Europe's natural wine treasures.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_emr, "Grilled Galician barnacles (percebes) with sea salt and lemon", "complement", "classic", "aperitif", "Galicia's most prized seafood delicacy and its rarest white wine — the wine's mineral precision and saline character mirrors the barnacle's brine; a pairing of pure regional identity")
    PAIR(prod_emr, "Caldo Gallego (Galician white bean and greens soup) with chorizo", "complement", "established", "main", "The Galician country kitchen's signature dish and its finest white wine — the wine's textural complexity handles the hearty soup; granite mineral mirrors the broth's depth")

p_mei = P("Viña Mein", "Spain", r_rib,
           description="Javier Alen's Ribeiro estate producing single-variety Treixadura and blended whites from estate granite vineyards. Viña Mein has been instrumental in demonstrating that Ribeiro's indigenous varieties — particularly Treixadura — can produce white wines of international quality and genuine aging potential.")
prod_mei, new = PROD("Viña Mein Blanco Ribeiro", "wine_still", p_mei, r_rib, "Spain",
                     subcategory="Treixadura Blend",
                     description="Ribeiro's most accessible benchmark white — Treixadura, Albariño, Godello, and Torrontés from estate granite soils. White peach, citrus, jasmine, mineral freshness, and the distinctive Atlantic character that makes Galician whites so compelling. More textural and complex than Rías Baixas Albariño.",
                     price_tier="mid_range")
if new:
    PAIR(prod_mei, "Empanada de berberechos (cockle pie) with onion and peppers", "complement", "classic", "main", "Galicia's most traditional savory pastry with the region's indigenous wine — the wine's mineral freshness and citrus notes complement the briny cockles; onion and pepper bridge the herbal character")
    PAIR(prod_mei, "Pulpo a feira (boiled octopus) with olive oil and sweet paprika on wood board", "complement", "classic", "aperitif", "The most iconic Galician tapa and the region's white wine — octopus and Galician white share the Atlantic terroir; the wine's acidity and mineral freshness mirrors the olive oil's freshness")

# ── CALABRIA (ITALY) ─────────────────────────────────────────────
print("\n=== Calabria (Italy) ===")
r_cal = R("Calabria", "Italy", "wine",
           designation_type="DOC",
           designation_name="Cirò DOC",
           reputation_tier="overlooked",
           quality_trajectory="ascending",
           description="Italy's southernmost mainland wine region — the 'toe' of the Italian boot — producing wines from the ancient Greek variety Gaglioppo (as Cirò Rosso DOC) and the equally ancient Greco Bianco from volcanic soils and Calabrian granite. Once dismissed as rustic, a new generation of producers is revealing Cirò's extraordinary potential for transparent, mineral red wines that recall Burgundy more than the Mezzogiorno. Calabria's wines are among Italy's most undervalued and exciting discoveries.",
           key_producers="Librandi, Luigi Viola, A'Vita, Ippolito 1845, Statti",
           historical_context="The ancient Greeks called Calabria 'Oenotria' — the land of wine — and Cirò's Gaglioppo is thought to be among the oldest continuously cultivated wine varieties on earth. The wines of Krimissa (the ancient Greek settlement at Cirò) were offered to victorious Olympians. After a century of anonymity as bulk wine for northern Italian blending, the quality revolution began in the 2000s with producers like Luigi Viola and A'Vita demonstrating Cirò's world-class potential.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Calabria vintage; Gaglioppo from volcanic soils showed extraordinary pale color and mineral transparency."),
    (2021, "very_good", "stable", "Elegant vintage; the coastal Cirò sites produced Gaglioppo wines of haunting finesse and fresh acidity."),
    (2020, "excellent", "stable", "Benchmark year; Luigi Viola and A'Vita produced Cirò Rosso of the highest critical recognition internationally."),
    (2019, "very_good", "rising", "Outstanding vintage; natural Gaglioppo wines from the Ionian coast gained major international natural wine attention."),
    (2018, "very_good", "stable", "Solid vintage; Gaglioppo's ancient heritage expressed itself with particular clarity from the volcanic granite soils."),
]:
    VIN(r_cal, yr, qd, pt, sn)

p_vio = P("Luigi Viola", "Italy", r_cal,
           description="The most internationally acclaimed producer of Cirò — Francesco Viola's minimal-intervention, natural Gaglioppo from ancient Calabrian soils has transformed international perception of this overlooked region. The wines are allocated globally among natural wine specialists and are considered Italy's most exciting discovery of the 2010s.")
prod_vio, new = PROD("Luigi Viola Cirò Rosso Classico", "wine_still", p_vio, r_cal, "Italy",
                     subcategory="Gaglioppo",
                     description="Calabria's most internationally acclaimed natural wine — ancient Gaglioppo from volcanic granite, minimally intervened, producing a wine of extraordinary delicacy and mineral transparency. Pale ruby, wild cherry, dried flowers, iron, sea air, and the haunting mineral depth of ancient Greek vines. Reminiscent of great Burgundy in texture.",
                     price_tier="premium")
if new:
    PAIR(prod_vio, "Grilled pesce spada (swordfish) alla calabrese with capers, olives, and tomato", "complement", "established", "main", "Calabrian fish and Calabrian red — Gaglioppo's light body and mineral acidity handles swordfish elegantly; capers and olives bridge the wine's saline mineral character")
    PAIR(prod_vio, "Nduja bruschetta with fior di latte and fresh basil on grilled sourdough", "complement", "established", "main", "Calabria's fiery spreadable salami and its most transparent red — the wine's bright cherry and mineral freshness cuts through nduja's rich fat and chilli heat")

p_avi = P("A'Vita", "Italy", r_cal,
           description="Francesco Cataldo's Cirò estate producing natural Gaglioppo wines from the ancient coastal vineyards on volcanic sandy soils near the Ionian Sea. A'Vita's wines — minimal sulphur, no filtration — are considered among Italy's most authentic expressions of indigenous southern variety wine.")
prod_avi, new = PROD("A'Vita Cirò Rosso Classico Superiore", "wine_still", p_avi, r_cal, "Italy",
                     subcategory="Gaglioppo",
                     description="Slightly more structured than Luigi Viola's expression — A'Vita's Gaglioppo from coastal volcanic sandy soils shows more body and dark fruit concentration while maintaining the variety's characteristic mineral transparency and ancient character. Dark cherry, sea air, volcanic mineral, and dried fig.",
                     price_tier="mid_range")
if new:
    PAIR(prod_avi, "Pasta 'ncasciata (Calabrian baked pasta with eggplant and salami)", "complement", "classic", "main", "Calabria's celebratory pasta bake and the region's indigenous wine — the wine's bright cherry and mineral character cuts through the rich baked pasta; eggplant adds earthy depth")
    PAIR(prod_avi, "Murseddu (Calabrian braised offal with chilli, tomato, and bread)", "complement", "classic", "main", "Ancient Calabrian offal tradition and ancient Calabrian wine variety — Gaglioppo's mineral acidity handles the rich offal; chilli finds resonance in the wine's warm character")

# ── CANARY ISLANDS DO (SPAIN) ─────────────────────────────────────
print("\n=== Canary Islands DO (Spain) ===")
r_can = R("Canary Islands", "Spain", "wine",
           designation_type="DO",
           designation_name="Canary Islands DO",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Spain's volcanic Atlantic archipelago off the Moroccan coast, producing wines of extraordinary uniqueness from pre-Phylloxera vines on volcanic basalt and pumice at altitudes from sea level to 1,700m. The indigenous Listán Negro (red) and Listán Blanco (white) — both pre-Phylloxera survivors — produce wines of haunting transparency and mineral character. Tenerife's Etna-like conditions (Teide volcano, altitude, Atlantic winds) and Lanzarote's surreal vine-in-hollow basalt landscape make these among the world's most distinctive wine environments.",
           key_producers="Envínate, Suertes del Marqués, Bodegas Monje, El Lomo, Matías i Torres",
           historical_context="The Canary Islands supplied wine to Shakespeare's England ('Canary sack') and the Spanish American colonies throughout the 16th-18th centuries, when the islands were a major wine export hub. Phylloxera (which cannot survive in volcanic ash soils) never reached the islands, so all vines are ungrafted — some 200-400 years old. The natural wine movement's discovery of these ancient vines in the 2010s transformed the islands' international reputation overnight.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Canary Islands vintage; Listán Negro from Tenerife volcanic soils showed extraordinary translucency and mineral depth."),
    (2021, "very_good", "stable", "Elegant Atlantic vintage; the altitude sites on Tenerife produced wines of exceptional freshness despite the latitude."),
    (2020, "excellent", "stable", "Benchmark year; Envínate and Suertes del Marqués produced internationally acclaimed volcanic wines of global recognition."),
    (2019, "excellent", "rising", "Outstanding vintage; Listán Negro's delicate, transparent character gained major international natural wine press attention."),
    (2018, "very_good", "stable", "Solid vintage; ungrafted ancient vine Listán Negro showed extraordinary mineral purity from the volcanic basalt soils."),
]:
    VIN(r_can, yr, qd, pt, sn)

p_env = P("Envínate", "Spain", r_can,
           description="The four friends' project — Roberto Santana, Alfonso Torrente, Laura Ramos, and José Martínez — working across multiple Spanish regions but most celebrated for their Tenerife Canary Islands wines from ancient volcanic vines. Táganan (from ancient Mencía-like vines on Anaga mountains) is considered one of Spain's most exciting and distinctive natural red wines.")
prod_env, new = PROD("Envínate Táganan Tinto", "wine_still", p_env, r_can, "Spain",
                     subcategory="Listan Negro Blend",
                     description="One of Spain's most extraordinary and sought-after wines — Listán Negro, Tintilla, and other ancient Canarian varieties from ungrafted 200-year-old vines on steep Anaga volcanic terraces at altitude. Translucent ruby, wild cherry, volcanic mineral, Atlantic sea air, and dried herbs with a haunting transparency reminiscent of Burgundy.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_env, "Grilled Canarian papas arrugadas (wrinkled potatoes) with mojo rojo sauce", "complement", "classic", "aperitif", "The Canary Islands' most iconic dish and its most sought-after wine — the volcanic potato's salinity mirrors the wine's mineral sea-air character; mojo rojo's chilli bridges")
    PAIR(prod_env, "Tuna tartare with avocado, soy, sesame, and pickled ginger", "complement", "established", "starter", "The wine's mineral transparency and Atlantic freshness complements tuna's rich sashimi-grade quality; the wine's delicacy prevents dominating the fish's nuance")

p_sue_c = P("Suertes del Marqués", "Spain", r_can,
             description="Jonatan García Lima's Tenerife Valle de La Orotava estate producing Listán Negro and Listán Blanco of extraordinary precision from ancient volcanic vineyards on the slopes of Mount Teide. Each single-parcel Listán Negro wine expresses a different aspect of the volcano's diverse soils.")
prod_sue_c, new = PROD("Suertes del Marqués 7 Fuentes Listan Negro", "wine_still", p_sue_c, r_can, "Spain",
                        subcategory="Listan Negro",
                        description="Tenerife's most mineral and site-expressive Listán Negro from seven ancient volcanic springs (fuentes) on Teide's slopes — lighter than Valle de La Orotava's other expressions, with wild cherry, volcanic mineral, fresh herbs, and the Atlantic sea breeze character that distinguishes Canarian wine. One of the most individual red wines in Spain.",
                        price_tier="premium")
if new:
    PAIR(prod_sue_c, "Conejo en salmorejo (rabbit braised in Canarian red wine and garlic)", "complement", "classic", "main", "The islands' traditional rabbit preparation with Canarian Listán Negro is a pairing of centuries; the wine appears in the sauce; garlic and herbs bridge the wine's aromatic character")
    PAIR(prod_sue_c, "Fresh tuna loin with chimichurri, grilled peppers, and Canarian wrinkled potatoes", "complement", "established", "main", "Atlantic tuna from Canarian waters and Canarian volcanic red — the wine's mineral sea-air character mirrors the tuna's oceanic freshness; chimichurri bridges the herb notes")

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
