#!/usr/bin/env python3
"""T23 Batch 20 — New wine regions: Kamptal DAC (Austria), Vinho Verde DOC (Portugal), Great Southern GI (Australia), Toro DO (Spain), Crozes-Hermitage AOC (France)"""

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

# ── KAMPTAL DAC (AUSTRIA) ─────────────────────────────────────────
print("\n=== Kamptal DAC (Austria) ===")
r_kam = R("Kamptal", "Austria", "wine",
           designation_type="DAC",
           designation_name="Kamptal DAC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Austria's most important wine DAC for Grüner Veltliner and Riesling in the Kamp River valley north of Vienna, centered on the town of Langenlois. The Kamptal's extraordinary terroir diversity — loess, volcanic basalt (Zöbing), and metamorphic schist (Kammern) — produces wines of distinct personalities from the same varieties. Bründlmayer's single-vineyard Lamm and Heiligenstein Rieslings are considered Austria's finest white wines alongside Wachau's best.",
           key_producers="Bründlmayer, Loimer, Hiedler, Schloss Gobelsburg, Allram",
           historical_context="Langenlois is Austria's largest wine town and the historical center of Austrian wine culture. The Cistercian monks of Stift Heiligenkreuz farmed the Heiligenstein (Holy Stone) vineyard from medieval times — its warm volcanic gneiss soils ripen Riesling to extraordinary complexity. Willi Bründlmayer's ascent in the 1980s-90s made Kamptal internationally recognized; his méthode champenoise sparkling Brut also established Austria's sparkling wine credentials.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Kamptal vintage; Heiligenstein Riesling and Lamm Grüner Veltliner from volcanic gneiss showed extraordinary mineral complexity."),
    (2021, "very_good", "stable", "Classic vintage; the Kamp Valley's diverse soils produced Grüner Veltliner of excellent white pepper character and Riesling of fine precision."),
    (2020, "excellent", "stable", "Benchmark year; Bründlmayer Lamm and Loimer Seeberg produced internationally acclaimed wines of exceptional quality."),
    (2019, "exceptional", "rising", "Greatest Kamptal vintage of the modern era; Heiligenstein Riesling GG reached legendary critical scores."),
    (2018, "excellent", "stable", "Excellent vintage; warm conditions produced Grüner Veltliner of unusual richness balanced by the loess soils' natural freshness."),
]:
    VIN(r_kam, yr, qd, pt, sn)

p_bru = P("Bründlmayer", "Austria", r_kam,
           description="Willi Bründlmayer's Langenlois estate — Austria's most internationally decorated and consistently acclaimed wine producer. The Heiligenstein Riesling, Lamm Grüner Veltliner GG, and Zöbinger Heiligenstein Riesling Alte Reben are consistently rated among Austria's five greatest wines. Bründlmayer also produces Austria's most acclaimed traditional method sparkling wine.")
prod_bru, new = PROD("Bründlmayer Heiligenstein Riesling Alte Reben", "wine_still", p_bru, r_kam, "Austria",
                     subcategory="Riesling",
                     description="Austria's most celebrated Kamptal Riesling from old vines on the volcanic gneiss Heiligenstein — a wine of extraordinary complexity: peach, apricot, white pepper, volcanic mineral, and a long, haunting finish. Needs 10+ years of aging; develops extraordinary toasty complexity. One of Austria's greatest wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_bru, "Poached lobster with Riesling butter sauce, cucumber, and dill", "complement", "classic", "main", "Austria's finest Riesling with its finest crustacean — the wine's mineral peach character mirrors the lobster's sweetness; cucumber provides refreshing contrast; dill bridges the herbal notes")
    PAIR(prod_bru, "Zander (pike-perch) in Riesling cream with saffron and leeks", "complement", "classic", "main", "The wine appears in the sauce — a classic Austrian fine dining tradition; freshwater fish from the Danube and Kamptal Riesling sharing a circular culinary geography")

p_loi = P("Loimer", "Austria", r_kam,
           description="Fred Loimer's biodynamic Langenlois estate producing Kamptal Grüner Veltliner and Riesling of excellent mineral precision from multiple terroir expressions. Loimer's Seeberg Riesling and Langenlois Grüner Veltliner are considered excellent value expressions of the DAC's diverse soils.")
prod_loi, new = PROD("Loimer Seeberg Riesling Kamptal", "wine_still", p_loi, r_kam, "Austria",
                     subcategory="Riesling",
                     description="Kamptal Riesling from the limestone and metamorphic Seeberg vineyard — mineral, dry, and elegant with citrus, white flower, and stone fruit with a distinctive limestone mineral core. More accessible than Heiligenstein in youth; excellent with food and at table.",
                     price_tier="premium")
if new:
    PAIR(prod_loi, "Wiener Schnitzel with lingonberry jam, cucumber salad, and lemon wedge", "complement", "classic", "main", "Austria's most iconic dish and its most food-friendly Riesling — the wine's citrus and mineral freshness cuts through the breaded veal; lingonberry's tartness bridges the wine's acidity")
    PAIR(prod_loi, "Smoked trout Aufschnitt with horseradish cream, rye bread, and chives", "complement", "classic", "aperitif", "Austrian smoked fish and dry Riesling — a classic Alpine pairing; the wine's citrus and mineral character cuts through the smoked fish's richness; horseradish adds spicy contrast")

# ── VINHO VERDE DOC (PORTUGAL) ────────────────────────────────────
print("\n=== Vinho Verde DOC (Portugal) ===")
r_vvd = R("Vinho Verde", "Portugal", "wine",
           designation_type="DOC",
           designation_name="Vinho Verde DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Portugal's largest DOC in the lush, Atlantic-influenced Minho region of northwestern Portugal, producing vibrant, refreshing whites from Alvarinho, Loureiro, Trajadura, and Arinto at low to medium alcohol. The sub-region of Monção e Melgaço on the Spanish border produces the finest Alvarinho — mineral, aromatic, and with greater depth than the lighter spritzy styles. 'Vinho Verde' (green wine) refers to the wine's freshness and youth, not its color.",
           key_producers="Quinta de Soalheiro, Anselmo Mendes, Quinta da Raza, Niepoort, Palácio da Brejoeira",
           historical_context="Vinho Verde's ancient wine culture dates to before the Roman occupation — the Minho's Celtic and Roman traditions of viticulture merge in the 'verde' wines. The distinctive pergola training system (ramada or latada) that trains vines overhead on granite pillars was designed to maximize ground space for food crops underneath. The 2000s premium Alvarinho revolution transformed international perception from cheap spritz to serious single-varietal wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vinho Verde vintage; Monção e Melgaço Alvarinho showed extraordinary aromatic complexity and citrus mineral precision."),
    (2021, "very_good", "stable", "Classic Atlantic vintage; the Minho's high humidity produced wines of excellent natural freshness and vitality."),
    (2020, "excellent", "stable", "Benchmark year; Soalheiro and Anselmo Mendes produced Alvarinho of exceptional depth and aging potential."),
    (2019, "very_good", "rising", "Outstanding vintage; Alvarinho from Monção demonstrated world-class aromatic complexity for the first time internationally."),
    (2018, "very_good", "stable", "Solid vintage; Loureiro and Trajadura blends showed excellent aromatic character; Alvarinho of good structure."),
]:
    VIN(r_vvd, yr, qd, pt, sn)

p_soa = P("Quinta de Soalheiro", "Portugal", r_vvd,
           description="The Cerdeira family's Melgaço estate producing Portugal's most internationally acclaimed Alvarinho from the highest sub-region of Vinho Verde. Soalheiro's Primeiras Vinhas (old vines) and sparkling Soalheiro Espumante are considered Portugal's finest expressions of Alvarinho's potential outside the Rías Baixas comparison.")
prod_soa, new = PROD("Soalheiro Alvarinho", "wine_still", p_soa, r_vvd, "Portugal",
                     subcategory="Alvarinho",
                     description="Portugal's most celebrated Alvarinho from Melgaço's granite hillsides — aromatic, mineral, and surprisingly age-worthy for a 'green wine'. White peach, lime blossom, grapefruit, granite mineral, and the distinctive saline freshness of the Atlantic-influenced Minho. More complex and structured than Spanish Albariño.",
                     price_tier="mid_range")
if new:
    PAIR(prod_soa, "Bacalhau à brás (shredded salt cod with egg, olives, and crispy potato)", "complement", "classic", "main", "Portugal's most beloved dish and Portugal's finest white — Alvarinho's citrus and mineral character cuts through the salt cod's richness; olive bridges the wine's saline character")
    PAIR(prod_soa, "Freshly opened Galician berberechos (cockles) with lemon and olive oil", "complement", "classic", "aperitif", "Minho coast seafood and Minho Alvarinho — the wine's mineral freshness and citrus character mirrors the cockle's brine; the wine is the natural partner for small shellfish")

p_men = P("Anselmo Mendes", "Portugal", r_vvd,
           description="Anselmo Mendes's Monção estate is the Minho's most technically skilled and internationally exported Alvarinho specialist. Curtimenta (skin-contact Alvarinho), Contacto (minimal intervention), and Muros Antigos represent a range of Alvarinho styles from refreshing to profound, demonstrating the variety's versatility.")
prod_men, new = PROD("Anselmo Mendes Curtimenta Alvarinho", "wine_still", p_men, r_vvd, "Portugal",
                     subcategory="Alvarinho",
                     description="Skin-contact Alvarinho from Monção — a radical departure from the bright, fresh Vinho Verde style. Extended maceration produces a textural, amber-tinged wine of unusual complexity: dried apricot, orange peel, beeswax, granite, and a lingering saline mineral finish. One of Portugal's most intriguing natural wine expressions.",
                     price_tier="premium")
if new:
    PAIR(prod_men, "Chouriço and chouriça assados (grilled Portuguese sausages) with cornbread", "complement", "established", "main", "Skin-contact Alvarinho's textural complexity and dried fruit character handles the sausage's smoky fat; cornbread provides starchy balance; the wine's mineral freshness cuts through")
    PAIR(prod_men, "Bacalhau com broa (salt cod with cornbread crust, olive oil, and garlic)", "complement", "established", "main", "Aged skin-contact white and salt cod — the wine's dried fruit and mineral character mirrors the cod's preserved depth; olive oil bridges the wine's texture; garlic echoes the aromatic complexity")

# ── GREAT SOUTHERN GI (AUSTRALIA) ─────────────────────────────────
print("\n=== Great Southern GI (Australia) ===")
r_grs = R("Great Southern", "Australia", "wine",
           designation_type="GI",
           designation_name="Great Southern GI",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Western Australia's largest and most diverse wine region in the state's far south, encompassing five distinct sub-regions: Albany (maritime Pinot Noir), Denmark (maritime Chardonnay), Frankland River (Riesling and Cabernet), Mount Barker (Riesling and Shiraz), and Porongurup (Riesling on granite). The region's extreme isolation, ancient soils, and cool Southern Ocean influence create wines of uncommon mineral intensity and Australian uniqueness — some of the world's finest Riesling outside Germany.",
           key_producers="Howard Park, Ferngrove, Plantagenet, Forest Hill, Castelli Estate",
           historical_context="Great Southern's first modern winery was Plantagenet at Mount Barker in 1974, established by Tony Smith. The region's Riesling from Mount Barker was recognized as Australia's finest alternative to Clare and Eden Valley by the 1990s. Howard Park's Scotsdale and Abercrombie Riesling from Frankland River's ancient karri forests established Western Australia's potential for Riesling of the highest international quality.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Great Southern vintage; Mount Barker Riesling of extraordinary mineral precision; Frankland River Cabernet of great structure."),
    (2021, "very_good", "stable", "Classic vintage; the Southern Ocean's influence produced wines of excellent freshness; Porongurup Riesling from granite particularly fine."),
    (2020, "excellent", "stable", "Benchmark year; Forest Hill and Howard Park produced Great Southern wines of exceptional quality across all sub-regions."),
    (2019, "excellent", "rising", "Outstanding vintage; Mount Barker Riesling achieved its highest critical scores yet; Albany Pinot Noir showed Burgundian elegance."),
    (2018, "very_good", "stable", "Solid vintage; the Great Southern's isolation from eastern Australian weather produced wines of characteristic purity and mineral freshness."),
]:
    VIN(r_grs, yr, qd, pt, sn)

p_foh = P("Forest Hill Vineyard", "Australia", r_grs,
           description="Tim and Jane Lyons's Mount Barker estate — one of the Great Southern's oldest vineyards, planted in 1965 — producing benchmark Riesling and Cabernet Sauvignon from the ancient red laterite soils of the Mount Barker sub-region. Forest Hill's Block 1 Riesling is considered the Great Southern's most distinctive Riesling expression.")
prod_foh, new = PROD("Forest Hill Block 1 Riesling", "wine_still", p_foh, r_grs, "Australia",
                     subcategory="Riesling",
                     description="Great Southern's most celebrated single-block Riesling from ancient Mount Barker red laterite soils — bone dry, intensely mineral, and utterly individual. Lime zest, citrus blossom, red clay mineral, white flower, and a linearity that recalls great German Riesling in its precision. Develops magnificently over 20+ years.",
                     price_tier="premium")
if new:
    PAIR(prod_foh, "Freshly caught Western Australian rock lobster with drawn butter and lemon", "complement", "classic", "main", "WA seafood and WA Riesling — Great Southern's coastal proximity makes this a natural pairing; the wine's citrus and mineral character mirrors the lobster's sweetness; butter bridges")
    PAIR(prod_foh, "Barramundi with lemon myrtle, native sea purslane, and macadamia butter", "complement", "established", "main", "The wine's citrus and mineral character mirrors the lemon myrtle; the native ingredients add Australian botanical complexity; macadamia butter mirrors the wine's richness")

p_cas = P("Castelli Estate", "Australia", r_grs,
           description="Sam Castelli's Denmark and Frankland River estate producing critically acclaimed Chardonnay, Pinot Noir, and Riesling from the Great Southern's most southerly and maritime sites. The Il Liris range and Castelli single-vineyard wines have established Great Southern's credentials for world-class Chardonnay alongside its Riesling reputation.")
prod_cas, new = PROD("Castelli Il Liris Chardonnay", "wine_still", p_cas, r_grs, "Australia",
                     subcategory="Chardonnay",
                     description="Great Southern's most refined Chardonnay from the maritime Denmark sub-region — white peach, hazelnut, citrus blossom, and the cool Southern Ocean mineral freshness that distinguishes WA Chardonnay from warmer Margaret River expressions. Elegant, precise, and genuinely age-worthy.",
                     price_tier="premium")
if new:
    PAIR(prod_cas, "Grilled WA marron (freshwater crayfish) with wild herb butter and lemon", "complement", "classic", "main", "Western Australia's prized native freshwater crustacean and the state's finest Chardonnay — the wine's hazelnut and citrus character mirrors the marron's delicate sweetness; wild herbs bridge")
    PAIR(prod_cas, "Roasted free-range chicken with WA truffle, roasted garlic, and leek gratin", "complement", "established", "main", "Great Southern Chardonnay's hazelnut complexity finds natural resonance with WA truffle; roasted chicken provides the protein bridge; leek's sweetness complements the wine's fruit")

# ── TORO DO (SPAIN) ───────────────────────────────────────────────
print("\n=== Toro DO (Spain) ===")
r_tor = R("Toro", "Spain", "wine",
           designation_type="DO",
           designation_name="Toro DO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Castilla y León's most powerful and dramatic wine DO on the ancient Duero plateau at 620-750m altitude west of Valladolid, producing intensely concentrated Tinta de Toro (Tempranillo clone adapted to the extreme climate) from ungrafted sand-over-clay soils. The Toro's brutal continental climate — some of the hottest summers in Castile — creates wines of extraordinary dark fruit density and tannic structure. Many estates with ungrafted vines from pre-Phylloxera are over 100 years old.",
           key_producers="Numanthia, Maurodos (San Román), Pintia (Vega Sicilia), Elias Mora, Dominio de Atauta",
           historical_context="Toro's wines supplied the Spanish Armada and were drunk throughout medieval Spain. The region received DO status in 1987. Vega Sicilia's establishment of Pintia in 1999 and LVMH's Numanthia (sold to Torres in 2008) brought world attention to Toro's potential for wines as powerful as the finest Napa or Châteauneuf-du-Pape. The region's ancient ungrafted vines — surviving because the sandy soils could not support the Phylloxera louse — are among Spain's most remarkable wine heritage.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Toro vintage; Tinta de Toro from ungrafted sandy soils showed extraordinary dark fruit concentration and mineral depth."),
    (2021, "very_good", "stable", "Classic vintage; the Duero plateau's extreme continental climate produced wines of excellent structure and density."),
    (2020, "excellent", "stable", "Benchmark year; Numanthia Termanthia and Pintia produced wines of exceptional quality from ancient ungrafted vines."),
    (2019, "exceptional", "rising", "Greatest Toro vintage of the modern era; wines of legendary concentration from centenarian ungrafted Tinta de Toro vines."),
    (2018, "excellent", "stable", "Excellent vintage; the extreme altitude and sandy soils combined perfectly to produce wines of power with unusual freshness."),
]:
    VIN(r_tor, yr, qd, pt, sn)

p_num = P("Numanthia", "Spain", r_tor,
           description="Originally established by the Eguren family and later acquired by Torres, Numanthia produces two benchmark Toro wines: the accessible Numanthia and the legendary Termanthia from the oldest ungrafted vines in the DO — some 200 years old. Termanthia is considered Spain's most powerful and concentrated wine alongside Pingus.")
prod_num, new = PROD("Numanthia Toro", "wine_still", p_num, r_tor, "Spain",
                     subcategory="Tinta de Toro",
                     description="Numanthia's benchmark Toro — old-vine Tinta de Toro from ungrafted sandy soils at altitude producing extraordinary dark fruit concentration: dark plum, chocolate, espresso, tobacco, and the characteristic Toro tannic power softened by the altitude's natural freshness. Demands significant cellaring.",
                     price_tier="premium")
if new:
    PAIR(prod_num, "Lechazo asado (milk-fed baby lamb, wood-roasted in a clay cazuela)", "complement", "classic", "main", "Castile's most celebrated dish — the region's baby lamb roasted in a wood-fired oven, served with the juices and crusty bread. Toro's power and dark fruit is the only wine that can stand alongside this intensity")
    PAIR(prod_num, "Cochinillo (suckling pig) with garlic and lemon, roasted in a clay pot", "complement", "classic", "main", "The Castilian suckling pig tradition meets Toro's most powerful wine — the wine's dark fruit and tannic power cuts through the pig's crispy skin fat; the clay pot's mineral character mirrors the wine's earthiness")

p_mos_t = P("Maurodos (San Román)", "Spain", r_tor,
             description="Mariano García's Toro estate — the legendary former winemaker of Vega Sicilia producing his benchmark Toro under the San Román label. García's precision and understanding of Tempranillo family wines translates into some of Toro's most elegant and food-friendly expressions without sacrificing the region's characteristic power.")
prod_mos_t, new = PROD("Maurodos San Román Toro", "wine_still", p_mos_t, r_tor, "Spain",
                        subcategory="Tinta de Toro",
                        description="Mariano García's (ex-Vega Sicilia) benchmark Toro — Tinta de Toro from ancient sandy soils treated with the elegance that characterized his Vega Sicilia work. More refined and food-friendly than Numanthia Termanthia, with dark cherry, plum, tobacco, cedar, and a long mineral finish from the high-altitude sandy soils.",
                        price_tier="premium")
if new:
    PAIR(prod_mos_t, "Estofado de cordero (Castilian lamb stew) with saffron, almonds, and vegetables", "complement", "classic", "main", "Old Castile's braised lamb and Toro's most elegant red — García's refined wine complements rather than overwhelms the stew; saffron bridges the wine's mineral depth; almonds echo the wine's cedar")
    PAIR(prod_mos_t, "Morcilla de Burgos (blood sausage with rice) with braised lentils and pimentón", "complement", "classic", "main", "Castilian blood sausage and Toro's structured red — the wine's dark fruit and tobacco handles the morcilla's iron intensity; pimentón bridges the wine's spice notes")

# ── CROZES-HERMITAGE AOC (FRANCE) ─────────────────────────────────
print("\n=== Crozes-Hermitage AOC (France) ===")
r_crh = R("Crozes-Hermitage", "France", "wine",
           designation_type="AOC",
           designation_name="Crozes-Hermitage AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="The northern Rhône's largest AOC surrounding the famous Hermitage hill, producing Syrah reds and Marsanne/Roussanne whites from diverse soils including granite, clay, and alluvial terraces. Crozes-Hermitage offers the northern Rhône character at far more accessible prices than Hermitage or Côte Rôtie — the best domaines produce wines that rival the northern Rhône's finest at a fraction of the cost. Key producers work in the granitic Les Chassis and Larnage sub-zones.",
           key_producers="Alain Graillot, Yann Chave, Domaine du Murinais, Delas Frères, Ferraton Père et Fils",
           historical_context="Crozes-Hermitage received AOC status in 1937. For most of its history it was considered merely the mass-market alternative to Hermitage. Alain Graillot's arrival in 1985 — producing Syrah of extraordinary concentration and elegance from a converted barn — demonstrated that Crozes-Hermitage could be taken seriously. Graillot's Crozes-Hermitage La Guiraude became France's most overachieving wine of the late 1980s and sparked a quality revolution in the appellation.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Crozes-Hermitage vintage; granite Larnage Syrah of extraordinary pepper and mineral intensity; Marsanne of excellent texture."),
    (2021, "very_good", "stable", "Classic northern Rhône vintage; Syrah showed excellent aromatic precision and the characteristic olive and pepper character."),
    (2020, "excellent", "stable", "Benchmark year; Graillot La Guiraude and Yann Chave Mon Coeur produced internationally acclaimed wines."),
    (2019, "exceptional", "rising", "Greatest Crozes-Hermitage vintage of the modern era; Syrah of extraordinary depth from all quality producers."),
    (2018, "excellent", "stable", "Excellent vintage; warm conditions produced Syrah of unusual richness; Marsanne whites of exceptional honeyed complexity."),
]:
    VIN(r_crh, yr, qd, pt, sn)

p_gra = P("Alain Graillot", "France", r_crh,
           description="The producer who single-handedly transformed Crozes-Hermitage's reputation — Alain Graillot's converted barn winery produces the most consistently acclaimed and internationally collected Crozes-Hermitage. La Guiraude (the top cuvée) achieves Hermitage quality at Crozes prices; the classic Crozes-Hermitage is a benchmark for the appellation's food-friendly Syrah style.")
prod_gra, new = PROD("Graillot Crozes-Hermitage Rouge", "wine_still", p_gra, r_crh, "France",
                     subcategory="Syrah",
                     description="The benchmark Crozes-Hermitage Syrah — black olive, white pepper, violets, dark plum, and the northern Rhône mineral freshness that makes Graillot's wine one of France's greatest value experiences. The style is more elegant and food-friendly than Hermitage itself; age 5-10 years for full complexity.",
                     price_tier="mid_range")
if new:
    PAIR(prod_gra, "Slow-roasted leg of lamb with rosemary, thyme, and whole garlic cloves", "complement", "classic", "main", "Northern Rhône Syrah and roasted lamb is France's most enduring pairing — the wine's olive and pepper character mirrors the Provençal herbs; the wine's tannins handle the lamb's fat")
    PAIR(prod_gra, "Wild boar sausage with chestnut purée, lardons, and Puy lentils", "complement", "established", "main", "Rhône Syrah and game is a French tradition; the wine's dark plum and mineral character handles the sausage's intensity; chestnut echoes the wine's earthy complexity")

p_cha = P("Yann Chave", "France", r_crh,
           description="Yann Chave's family domaine in Mercurol is considered Crozes-Hermitage's second finest producer after Graillot, with Le Rouvre and Mon Coeur Syrah wines that consistently receive the highest scores from French and international wine media. The Chave family's meticulous farming and barrel selections produce wines of unusual depth for the appellation.")
prod_cha, new = PROD("Yann Chave Crozes-Hermitage Le Rouvre", "wine_still", p_cha, r_crh, "France",
                     subcategory="Syrah",
                     description="Yann Chave's single-vineyard Crozes-Hermitage from the Les Chassis granite terraces — more concentrated and mineral than the standard cuvée, rivaling Hermitage in density. Dark fruit, smoked meat, olive brine, mineral granite, and the long finish of granite-grown Syrah. Outstanding value for the quality.",
                     price_tier="premium")
if new:
    PAIR(prod_cha, "Duck magret grillé with green peppercorn sauce and sautéed chanterelles", "complement", "classic", "main", "Northern Rhône Syrah and duck confit or grilled duck breast is France's classic pairing; green peppercorn mirrors the wine's pepper character; chanterelles echo the granite mineral")
    PAIR(prod_cha, "Andouillette (tripe sausage) with Dijon mustard, pomme frites, and green salad", "complement", "established", "main", "France's most challenging traditional sausage and its most approachable northern Rhône Syrah — the wine's structure and dark fruit handles the tripe's intensity; mustard cuts through the richness")

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
