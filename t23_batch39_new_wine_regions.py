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
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
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
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
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
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === SANTA CRUZ MOUNTAINS AVA (USA) ===
print("\n=== Santa Cruz Mountains AVA (USA) ===")
r_scm = R(
    name="Santa Cruz Mountains",
    country="USA",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Santa Cruz Mountains AVA",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="One of California's oldest and most intellectually serious wine regions — the forested, fog-shrouded mountains rising between Silicon Valley and the Pacific Ocean south of San Francisco. The AVA's complex terrain and varied soils (limestone, sandstone, and serpentine in different zones) produce wines of genuine distinctiveness: Cabernet Sauvignon from the ridge-top Monte Bello limestone achieves Bordeaux-like structure and longevity, while cool Pacific-facing slopes produce Pinot Noir and Chardonnay of haunting delicacy. Ridge Vineyards' Monte Bello has been California's most consistent benchmark for Bordeaux varieties since the 1970s.",
    key_producers="Ridge Vineyards, Mount Eden Vineyards, Rhys Vineyards, Thomas Fogarty",
    historical_context="The Santa Cruz Mountains were established as California's first geographically defined wine region in 1981. Ridge Vineyards, established at Monte Bello in 1959, achieved international fame when its 1971 Monte Bello tied first with Petrus in the 'Judgment of Paris' retrospective tasting in 2006. Mount Eden (formerly Martin Ray) has produced old-vine estate Chardonnay from the same site since the 1940s."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding vintage with ideal balance — warm summer days, cool Pacific nights. Monte Bello Cabernet of exceptional structure."),
    (2020, "very_good", "stable", "Some wildfire smoke impact but well-managed. Mountain elevation provided advantage over valley floor."),
    (2019, "excellent", "rising", "One of the decade's finest — long ripening season producing wines of great complexity and aging potential."),
    (2018, "very_good", "stable", "Good vintage across the AVA. Ridge Monte Bello of excellent structure."),
    (2017, "excellent", "stable", "Outstanding — balanced, elegant wines with California's finest mountain-grown character."),
]:
    VIN(r_scm, yr, qd, pt, sn)

p_ridge = P(
    name="Ridge Vineyards",
    country="USA",
    region_id=r_scm,
    producer_type="winery",
    description="One of California's most historically significant and philosophically consistent wine estates — founded in 1959 at Monte Bello in the Santa Cruz Mountains by Stanford Research Institute scientists who sought to make Bordeaux-style wine from limestone ridges. Paul Draper's 50-year tenure as winemaker (1969–2016) established Ridge's philosophy of transparency, minimal intervention, and American oak maturation. Monte Bello is California's most age-worthy Cabernet Sauvignon and the state's most internationally respected wine. Geyserville (Zinfandel from Alexander Valley) is equally celebrated."
)
prod_monte_bello, new = PROD(
    name="Ridge Monte Bello Santa Cruz Mountains",
    category="wine_still",
    subcategory="Cabernet Sauvignon",
    producer_id=p_ridge,
    region_id=r_scm,
    origin_country="USA",
    description="California's most celebrated and age-worthy Cabernet Sauvignon — from the 2,600ft Monte Bello ridge on limestone soils, a blend dominated by Cabernet Sauvignon with Merlot, Petit Verdot, and Cabernet Franc. Fermented with indigenous yeasts, aged in American oak (Ridge uses no new French oak) with ingredient labelling transparency that is unique in the wine world. The wine aged 30+ years shows extraordinary elegance, dried herb complexity, and mineral depth that rivals classified Bordeaux. Named number one wine in the 2006 retrospective Judgment of Paris.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_monte_bello, "Rack of Colorado lamb with herbed crust and mushroom duxelles", "complement", "classic", "main", "California's finest Bordeaux-style wine with lamb — the classic pairing. The wine's dried herb complexity and firm limestone tannins support the lamb's richness while mushroom echoes its earthy depth.")
    PAIR(prod_monte_bello, "Dry-aged prime beef tenderloin with truffle jus and asparagus", "complement", "established", "main", "Monte Bello's structure and mineral complexity are ideal for dry-aged beef. Truffle bridges its earthy depth while asparagus provides freshness. The wine's age-worthy tannins support the richness.")
    PAIR(prod_monte_bello, "Braised short ribs with bordelaise sauce and potato purée", "complement", "established", "main", "The wine's Bordeaux-like structure bridges naturally to the French braising tradition. Bordelaise sauce mirrors its red wine complexity while potato purée absorbs the richness.")
    PAIR(prod_monte_bello, "Aged Fiscalini Bandaged Cheddar with Zinfandel jelly", "complement", "suggested", "cheese", "California artisan cheese with California's finest Cabernet — the cheddar's sharp, crystalline character complements the wine's structure while Zinfandel jelly echoes its red fruit complexity.")

p_mount_eden = P(
    name="Mount Eden Vineyards",
    country="USA",
    region_id=r_scm,
    producer_type="winery",
    description="The oldest continuously producing estate in the Santa Cruz Mountains — founded by Martin Ray in 1943 and home to some of California's oldest Chardonnay and Pinot Noir vines. Mount Eden's 'Old Vine Reserve' Chardonnay from estate vines planted in the 1940s–60s is California's most age-worthy Chardonnay, developing extraordinary complexity — mineral, reductive, and Burgundian in character — over 10–30 years. The estate also produces benchmark Santa Cruz Mountains Pinot Noir and Cabernet Sauvignon."
)
prod_mount_eden, new = PROD(
    name="Mount Eden Estate Chardonnay Santa Cruz Mountains",
    category="wine_still",
    subcategory="Chardonnay",
    producer_id=p_mount_eden,
    region_id=r_scm,
    origin_country="USA",
    description="California's most Burgundian Chardonnay — from estate vines at 2,000ft elevation on limestone-influenced soils, some planted in the 1960s. Fermented with indigenous yeasts in Burgundy barrels and aged on lees for 15 months without fining or filtration. The wine is deliberately reductive and mineral in youth, developing extraordinary complexity over a decade: Dijon mustard, white truffle, toasted hazelnut, lemon curd, crushed limestone, and the rare combination of California richness and Burgundian structure. California's greatest age-worthy Chardonnay.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_mount_eden, "Roasted lobster with truffle butter, pearl onions, and pea shoots", "complement", "classic", "main", "Age-worthy California Chardonnay with lobster — the wine's truffle and hazelnut complexity bridge to the richness of roasted lobster. Truffle butter connects its secondary notes while pea shoots add spring freshness.")
    PAIR(prod_mount_eden, "Pan-seared Dover sole with beurre noisette and fine herbs", "complement", "classic", "main", "The wine's hazelnut (noisette) notes create a direct bridge to beurre noisette — an elegant pairing where the sauce and wine share the same aromatic compound. Delicate sole allows the wine's complexity to shine.")
    PAIR(prod_mount_eden, "Veal sweetbreads with morel cream sauce and asparagus", "complement", "established", "main", "Limestone Chardonnay's mineral richness supports the complexity of sweetbreads. Morel cream bridges its earthy secondary notes while asparagus provides the classic white wine complement.")
    PAIR(prod_mount_eden, "Aged Époisses with walnut bread and honeycomb", "complement", "established", "cheese", "A bold pairing — the wine's richness and oxidative complexity can support even Époisses's intense washed-rind character. Honeycomb moderates the wine's acidity while walnuts echo its hazelnut complexity.")

# === VILLÁNY (Hungary) ===
print("\n=== Villány (Hungary) ===")
r_villany = R(
    name="Villány",
    country="Hungary",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Villányi Borvidék",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Hungary's warmest and most southerly wine region, occupying the limestone and loess slopes of the Villány Mountains near the Croatian border in Baranya county. Villány is Hungary's premier red wine region, specialising in Cabernet Franc — a variety that achieves an extraordinary depth and mineral complexity on Villány's limestone soils that has drawn comparisons to the finest expressions from Saint-Emilion and the Loire. The region also produces excellent Merlot, Portugieser, and the indigenous Kadarka, but it is Cabernet Franc that has established Hungary's international fine wine reputation.",
    key_producers="Gere Attila, Vylyan, Bock Winery, Csányi Winery",
    historical_context="Villány's viticultural history dates to at least the Ottoman period, when wine production continued despite the Islamic prohibition because of the region's Austrian-Habsburg administration. The post-communist wine revival from the 1990s saw a wave of quality-focused investment, with producers like Attila Gere and the Bock family demonstrating Villány's potential for internationally competitive Cabernet Franc and Merlot. The region now hosts Hungary's most prestigious wine auction, the Villány Franc competition."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Long, warm season with limestone soils preserving freshness. Cabernet Franc of exceptional aromatic precision."),
    (2020, "very_good", "stable", "Good vintage across the region. Merlot and Cabernet Franc of reliable concentration."),
    (2019, "excellent", "rising", "Outstanding vintage — Cabernet Franc of extraordinary complexity and aging potential. Among the decade's finest."),
    (2018, "very_good", "stable", "Classic Villány vintage with characteristic limestone mineral quality."),
    (2017, "excellent", "stable", "One of the region's finest recent vintages — structured, complex wines with excellent longevity."),
]:
    VIN(r_villany, yr, qd, pt, sn)

p_gere = P(
    name="Gere Attila",
    country="Hungary",
    region_id=r_villany,
    producer_type="winery",
    description="The most internationally celebrated producer in Villány — Attila Gere's estate has pioneered the concept of premium Hungarian Cabernet Franc and Merlot since the early 1990s, when he was among the first to demonstrate that Villány's limestone soils could produce wines competitive with the best of Bordeaux and Loire. The flagship Kopar cuvée (Cabernet Franc, Merlot, Cabernet Sauvignon) is Hungary's most internationally recognised red wine and has changed the perception of Hungarian fine wine globally."
)
prod_gere, new = PROD(
    name="Gere Attila Kopar Villány",
    category="wine_still",
    subcategory="Cabernet Franc",
    producer_id=p_gere,
    region_id=r_villany,
    origin_country="Hungary",
    description="Hungary's most internationally acclaimed wine — a Bordeaux blend dominated by Cabernet Franc and Merlot from Villány's limestone terraces, aged in French barriques. The wine shows why Villány's limestone soils are exceptional for Cabernet Franc: violet, red cherry, cedar, graphite, and the distinctive pencil shaving mineral note of great limestone Cab Franc. Structured, elegant, and genuine — Hungary's first wine to compete convincingly with French Bordeaux on the international market.",
    price_tier="premium"
)
if new:
    PAIR(prod_gere, "Mangalica pork tenderloin with braised red cabbage and apple", "complement", "classic", "main", "Hungary's heritage pork breed with its finest wine — Mangalica's exceptional fat quality and flavour complexity are matched by the wine's limestone mineral depth. Red cabbage echoes its violet notes while apple bridges its fruit.")
    PAIR(prod_gere, "Roasted guinea fowl with wild mushroom stuffing and Tokaj sauce", "complement", "established", "main", "Central European game bird with Villány Cabernet Franc — the wine's cedar and red fruit are ideal for the delicate guinea fowl. Wild mushroom bridges its earthy depth and Tokaj sauce adds the regional sweet-savoury complexity.")
    PAIR(prod_gere, "Slow-braised wild boar with juniper, caraway, and red wine reduction", "complement", "established", "main", "Hungarian forest game with the country's finest red wine — wild boar's gaminess and richness are matched by the wine's limestone tannin. Juniper echoes its cedar notes while caraway adds Central European spice.")
    PAIR(prod_gere, "Aged Hungarian sheep's milk cheese (Juhsajt) with cherry preserve", "complement", "established", "cheese", "The wine's red cherry and mineral depth complement aged sheep's milk cheese. Cherry preserve echoes its fruit while the wine's limestone character provides the mineral counterpoint.")

p_vylyan = P(
    name="Vylyan",
    country="Hungary",
    region_id=r_villany,
    producer_type="winery",
    description="One of Villány's most innovative estates, producing single-vineyard wines from named parcels with a strong emphasis on expressing limestone terroir through Cabernet Franc. Vylyan's Mandolás and Platina single-vineyard wines have demonstrated that Villány has the limestone complexity for truly site-specific wine in the Burgundy sense. The estate's organic and biodynamic approach ensures the authenticity of terroir expression."
)
prod_vylyan, new = PROD(
    name="Vylyan Mandolás Cabernet Franc Villány",
    category="wine_still",
    subcategory="Cabernet Franc",
    producer_id=p_vylyan,
    region_id=r_villany,
    origin_country="Hungary",
    description="A single-vineyard Cabernet Franc from the Mandolás site on pure limestone soils — one of Villány's most compelling single-parcel expressions. The wine shows the Loire-meets-Bordeaux character that Villány's finest Cabernet Franc achieves: green pepper, violet, red cherry, graphite, pencil lead, and a limestone minerality that gives the wine extraordinary freshness despite the southern Hungarian warmth. Organic, minimal intervention, aged in used French oak.",
    price_tier="premium"
)
if new:
    PAIR(prod_vylyan, "Grilled lamb rack with roasted pepper coulis and herb oil", "complement", "established", "main", "Limestone Cabernet Franc with lamb — a Loire-Villány parallel. The wine's violet and red cherry bridge to lamb's character while its limestone mineral freshness prevents heaviness.")
    PAIR(prod_vylyan, "Duck confit with lentilles du Puy and Dijon vinaigrette", "complement", "classic", "main", "Cabernet Franc's affinity for duck is consistent across terroirs — Villány's limestone expression brings additional freshness to this classic combination. Lentils provide earthy grounding while Dijon bridges the wine's sharp mineral edge.")
    PAIR(prod_vylyan, "Stuffed pepper (töltött paprika) with tomato sauce and sour cream", "complement", "classic", "main", "The most Hungarian of pairings — the national stuffed pepper dish with the country's most important wine variety. The wine's red fruit and mineral freshness complement the tomato sauce while its structure supports the meat filling.")
    PAIR(prod_vylyan, "Brie de Meaux with walnut and fig preserve", "complement", "suggested", "cheese", "The wine's pencil shaving mineral and red cherry notes bridge to soft-rind cheese. Walnut echoes its graphite complexity while fig preserve mirrors its dark fruit.")

# === SZEKSZÁRD (Hungary) ===
print("\n=== Szekszárd (Hungary) ===")
r_szekszard = R(
    name="Szekszárd",
    country="Hungary",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Szekszárdi Borvidék",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Hungary's second-most prestigious red wine region, occupying the loess bluffs above the Danube in the southern Tolna county. Where Villány focuses on Bordeaux varieties, Szekszárd is defined by Kadarka — Hungary's most important indigenous red variety — and the Szekszárdi Bikavér ('Bull's Blood') blend. The loess-clay soils and continental climate produce reds of a distinctive rustic depth and earthy character, with Kadarka achieving an almost Pinot Noir-like translucency and spice. The region also produces excellent Kékfrankos (Blaufränkisch) that rivals the best from Austria and Burgenland.",
    key_producers="Takler Winery, Heimann and Sons, Franz Weninger, Schieber",
    historical_context="Szekszárd is one of Hungary's oldest wine regions, with viticulture documented here since the Romans planted vines on the Danube loess bluffs. The region's fame in the 19th century was considerable — Franz Liszt and Miklós Ybl were among its admirers. The communist-era focus on bulk production largely destroyed the quality tradition, which has been painstakingly rebuilt since the 1990s by producers committed to indigenous varieties and traditional methods."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Outstanding Kadarka vintage — cool, long season producing wines of exceptional aromatic purity and elegance."),
    (2020, "very_good", "stable", "Good vintage across the region. Bikavér blends of reliable complexity."),
    (2019, "excellent", "rising", "One of the decade's finest — Kadarka of extraordinary delicacy and Kékfrankos of great structure."),
    (2018, "very_good", "stable", "Classic Szekszárd vintage with characteristic loess mineral quality."),
    (2017, "very_good", "stable", "Reliable vintage with good concentration. Indigenous varieties performed particularly well."),
]:
    VIN(r_szekszard, yr, qd, pt, sn)

p_takler = P(
    name="Takler Winery",
    country="Hungary",
    region_id=r_szekszard,
    producer_type="winery",
    description="One of Szekszárd's most respected family estates, producing benchmark Bikavér and Kadarka from loess-clay slopes above the Danube. The Takler family has been instrumental in the revival of Szekszárdi Bikavér as a serious, age-worthy wine — their Primarius (top selection) demonstrates that the Bull's Blood blend, once dismissed as tourist fare, can achieve genuine complexity and longevity when produced from low yields and quality fruit. The estate also produces excellent single-variety Kadarka and Kékfrankos."
)
prod_takler, new = PROD(
    name="Takler Primarius Szekszárdi Bikavér",
    category="wine_still",
    subcategory="Kadarka",
    producer_id=p_takler,
    region_id=r_szekszard,
    origin_country="Hungary",
    description="The prestige Szekszárdi Bikavér ('Bull's Blood') — a Kadarka-dominated blend with Kékfrankos, Cabernet Sauvignon, and Merlot from the loess terraces above the Danube. Deeply coloured with earthy complexity: dried cherry, leather, tobacco, dried herbs, dark chocolate, and a distinctive loess mineral quality. More elegant and complex than the infamous Eger Bikavér, this wine demonstrates the Szekszárd style at its finest — rich, earthy, and distinctly Hungarian. Ages magnificently over 10+ years.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_takler, "Pörkölt (Hungarian beef and paprika stew) with nokedli dumplings", "complement", "classic", "main", "The ultimate Hungarian pairing — beef pörkölt with Szekszárdi Bikavér. The wine's earthy depth and red fruit mirror the paprika-rich stew while nokedli absorbs the rich sauce. A pairing of obvious cultural and flavour logic.")
    PAIR(prod_takler, "Mangalica sausage with pickled cabbage and horseradish cream", "complement", "classic", "main", "Hungary's heritage pork sausage with the region's Bikavér — earthy, spiced sausage with earthy, tannic wine. Pickled cabbage echoes the wine's acidity while horseradish cream adds sharp contrast.")
    PAIR(prod_takler, "Wild mushroom paprikás with sour cream and egg noodles", "complement", "established", "main", "Szekszárd earthy Bikavér with earthy mushroom paprikás — the wine's dried herb and tobacco notes bridge to the umami depth of wild mushrooms. Sour cream moderates the wine's tannins.")
    PAIR(prod_takler, "Aged Trappista cheese with cherry jam and dark bread", "complement", "established", "cheese", "Hungary's semi-hard monastery cheese with the country's Bikavér — the wine's earthy complexity and dried cherry notes are balanced by the cheese's mild richness. Cherry jam echoes its fruit.")

p_heimann = P(
    name="Heimann and Sons",
    country="Hungary",
    region_id=r_szekszard,
    producer_type="winery",
    description="A forward-looking Szekszárd estate focused on indigenous varieties and sustainable viticulture. Heimann and Sons have championed pure Kadarka — often at the expense of the more marketable Bikavér blends — demonstrating the variety's unique character: translucent ruby, highly aromatic, with red cherry, fresh herbs, and a distinctive spice that makes it one of Central Europe's most interesting native varieties. Their Kadarka single-variety wines have attracted international natural wine attention."
)
prod_heimann, new = PROD(
    name="Heimann and Sons Kadarka Szekszárd",
    category="wine_still",
    subcategory="Kadarka",
    producer_id=p_heimann,
    region_id=r_szekszard,
    origin_country="Hungary",
    description="A pure Kadarka from sustainable loess vineyards in the heart of Szekszárd — one of Hungary's most ancient and important native red varieties vinified without compromise. Translucent ruby-garnet with aromas of sour cherry, dried rose, fresh herbs, wild pepper, and earthy loam. Silky, light-textured with good acidity and only moderate tannin — a wine of delicacy and aromatic interest unlike any other Central European red. The quintessential food wine of the Pannonian tradition.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_heimann, "Töltött káposzta (stuffed cabbage with pork and rice in tomato paprika sauce)", "complement", "classic", "main", "The most Hungarian of Hungarian dishes with the country's most Hungarian grape — Kadarka's light body and bright acidity lift the rich, paprika-sauced stuffed cabbage without competing with its complexity.")
    PAIR(prod_heimann, "Roasted duck legs with sour cherry sauce and potato gnocchi", "complement", "classic", "main", "Kadarka's sour cherry and dried herb notes mirror the cherry sauce precisely. Duck's moderate richness is well-matched to the wine's light-medium body while gnocchi absorbs the sauce.")
    PAIR(prod_heimann, "Grilled lamb kebabs with yogurt, cucumber, and fresh mint", "complement", "established", "main", "The wine's delicate aromatic character and fresh herb notes bridge to the mint and cucumber accompaniments. Its light body suits the freshness of yogurt-marinated lamb.")
    PAIR(prod_heimann, "Camembert with red currant jelly and walnut", "complement", "suggested", "cheese", "Kadarka's red fruit and light tannin are natural companions for soft-rind cheese. Red currant jelly echoes its sour cherry character while walnuts bridge its earthy depth.")

# === MANTINIA PDO (Greece) ===
print("\n=== Mantinia PDO (Greece) ===")
r_mantinia = R(
    name="Mantinia",
    country="Greece",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Mantinia PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Greece's highest altitude wine appellation — an extinct volcanic plateau in the Arcadian Mountains of the central Peloponnese at 600–650m elevation, where the indigenous Moschofilero grape produces some of Greece's most distinctive and aromatic dry whites. Moschofilero is one of the wine world's most individual varieties: pink-skinned (producing a faintly pink tinge in white wine), intensely perfumed with rose petal, violet, citrus, and spice — with a bone-dry, high-acidity structure that makes it uniquely food-friendly. The altitude provides remarkable freshness rarely found in Greek whites.",
    key_producers="Tselepos Estate, Domaine Spiropoulos, Boutari Naoussa",
    historical_context="The Mantinia plateau — associated with the pastoral myths of ancient Arcadia — has been cultivated since antiquity. The Moschofilero variety may be one of the most ancient indigenous varieties in Greece, preserved by the plateau's isolation and cool altitude. The modern wine PDO was established in 1971. Tselepos Estate has been the primary force in establishing Mantinia Moschofilero as an internationally recognised quality white wine."
)
for yr, qd, pt, sn in [
    (2022, "very_good", "stable", "Good growing season with characteristic plateau freshness. Moschofilero of excellent aromatic precision."),
    (2021, "excellent", "rising", "Outstanding vintage — cool conditions preserving extraordinary aromatic freshness and mineral tension."),
    (2020, "very_good", "stable", "Good vintage with characteristic rose petal and citrus aromatics well preserved by altitude."),
    (2019, "excellent", "rising", "One of the finest recent Mantinia vintages — complex, mineral Moschofilero with genuine aging potential."),
    (2018, "very_good", "stable", "Reliable vintage with the classic altitude freshness that defines the appellation."),
]:
    VIN(r_mantinia, yr, qd, pt, sn)

p_tselepos = P(
    name="Tselepos Estate",
    country="Greece",
    region_id=r_mantinia,
    producer_type="winery",
    description="The reference estate of Mantinia — Yiannis Tselepos's biodynamic property on the volcanic plateau, producing the benchmark expression of Moschofilero and the wine most responsible for establishing Mantinia's international reputation. Tselepos's Mantinia Moschofilero is consistently cited as one of Greece's finest white wines, demonstrating the variety's unique aromatic complexity, high natural acidity, and genuine aging potential when grown at altitude on volcanic soils."
)
prod_tselepos, new = PROD(
    name="Tselepos Mantinia Moschofilero",
    category="wine_still",
    subcategory="Moschofilero",
    producer_id=p_tselepos,
    region_id=r_mantinia,
    origin_country="Greece",
    description="The definitive expression of Mantinia's extraordinary indigenous white variety — Moschofilero from biodynamic vineyards at 650m on the Arcadian volcanic plateau. The wine shows why Moschofilero is one of Greece's greatest treasures: intensely aromatic with rose petal, violet, orange blossom, citrus zest, white pepper, and a mineral freshness that no warmer-climate wine could replicate. Bone dry with electrifying acidity and light-textured body — one of the Mediterranean's most versatile and aromatic food wines.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_tselepos, "Grilled whole sea bream with lemon, oregano, and capers", "complement", "classic", "main", "Mediterranean fish with Mantinia's aromatic white — the wine's floral complexity and citrus freshness complement sea bream's delicacy. Oregano echoes its herb notes while capers mirror its mineral acidity.")
    PAIR(prod_tselepos, "Prawn saganaki with ouzo, tomato, and feta", "complement", "classic", "main", "A quintessential Greek pairing — the wine's rose petal and orange blossom complement ouzo's anise, tomato bridges its acidity, and feta's salt amplifies its mineral quality.")
    PAIR(prod_tselepos, "Dolmades (vine leaf parcels) with tzatziki and lemon", "complement", "classic", "starter", "The wine's floral aromatics and citrus freshness are ideal for the herb and rice stuffed vine leaves. Tzatziki adds creaminess while lemon connects to the wine's bright acidity.")
    PAIR(prod_tselepos, "Tiropita (cheese pastry) with spinach and dill", "complement", "established", "starter", "Mantinia Moschofilero with Greek cheese pastry — the wine's aromatic complexity and acidity cut through the feta richness while dill and spinach echo its herbal notes. A natural everyday Greek pairing.")

p_spiropoulos = P(
    name="Domaine Spiropoulos",
    country="Greece",
    region_id=r_mantinia,
    producer_type="winery",
    description="An organic estate in Mantinia producing both still and sparkling Moschofilero — one of the few producers exploring the variety's potential for traditional method sparkling wine. The Ode Panos sparkling Moschofilero has attracted significant attention as a uniquely aromatic alternative to Champagne, while the still Mantinia remains a reliable expression of the plateau's freshness and floral character."
)
prod_spiropoulos, new = PROD(
    name="Domaine Spiropoulos Ode Panos Sparkling Moschofilero Mantinia",
    category="wine_sparkling",
    subcategory="Moschofilero",
    producer_id=p_spiropoulos,
    region_id=r_mantinia,
    origin_country="Greece",
    description="A traditional method sparkling wine from Moschofilero — one of the wine world's most aromatic sparkling wine varieties. The elevated plateau and the grape's natural high acidity provide ideal base wine for traditional method sparkling. Fine persistent bubbles with an extraordinary aromatic profile: fresh rose, violet, citrus blossom, green apple, white pepper, and toasted brioche from the lees aging. Bone dry, mineral, and intensely characterful — Greece's most original sparkling wine.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_spiropoulos, "Taramasalata with warm pita and cucumber", "complement", "classic", "starter", "Greek sparkling wine with Greece's iconic smoked roe dip — the wine's fine bubble and mineral freshness cut through the taramasalata's richness while its citrus notes echo the lemon juice. An apéritif pairing of pure Mediterranean logic.")
    PAIR(prod_spiropoulos, "Grilled octopus with fava (yellow split pea purée) and capers", "complement", "established", "starter", "The wine's aromatic freshness and fine bubble complement octopus's charred Mediterranean character. Fava's creaminess provides textural contrast while capers echo the wine's mineral salinity.")
    PAIR(prod_spiropoulos, "Fresh labneh with olive oil, zaatar, and flatbread", "complement", "established", "starter", "The wine's floral freshness and acidity lift the creamy labneh. Za'atar echoes its herb notes while olive oil connects to the Mediterranean table's essential ingredient.")
    PAIR(prod_spiropoulos, "Light cheese saganaki (fried cheese) with honey and sesame", "complement", "classic", "starter", "Sparkling Moschofilero with fried cheese — the wine's bubble cuts through the fat while its floral character complements the honey. Sesame echoes its toasted brioche note from lees aging.")

# === PATAGONIA (Argentina) ===
print("\n=== Patagonia (Argentina) ===")
r_patagonia = R(
    name="Patagonia",
    country="Argentina",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Patagonia",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Argentina's southernmost wine frontier — the windswept, arid steppe of Neuquén and Río Negro provinces stretching toward Tierra del Fuego, where extreme desert conditions and intense Patagonian winds produce wines of surprising elegance and freshness. The dominant winegrowing areas are centred on the Neuquén River valley (Barda and Añelo), the Río Negro valley, and the Alto Valle. At 39°S latitude, the region is among the world's southernmost commercial wine zones. Malbec, Pinot Noir, and Merlot for reds; Sauvignon Blanc, Chardonnay, and the versatile Torrontés for whites — all show remarkable freshness from the extreme winds and desert cold.",
    key_producers="Bodega Chacra, Familia Schroeder, NQN (Neuquén), Bodegas del Fin del Mundo",
    historical_context="Wine production in Patagonia dates to the early 20th century when Welsh and Italian immigrants planted vines in the Río Negro valley. The modern fine wine era began with Piero Incisa della Rocchetta (of Sassicaia fame) establishing Chacra in 2004, seeking pre-phylloxera old-vine Pinot Noir planted in 1932 — and discovering some of the Southern Hemisphere's oldest surviving vines. The region's profile has grown rapidly as the natural wine world recognized its extreme terroir potential."
)
for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Patagonia vintage — long, cool growing season producing wines of extraordinary freshness. Pinot Noir of particular finesse."),
    (2021, "very_good", "stable", "Good conditions across the region. Malbec and Pinot Noir showing the characteristic Patagonian freshness."),
    (2020, "excellent", "rising", "One of the decade's finest — cool conditions producing wines of great complexity and aging potential."),
    (2019, "very_good", "stable", "Reliable vintage with excellent natural acidity from the desert cold."),
    (2018, "excellent", "stable", "Classic Patagonia vintage — concentrated yet fresh wines that challenge assumptions about the region."),
]:
    VIN(r_patagonia, yr, qd, pt, sn)

p_chacra = P(
    name="Bodega Chacra",
    country="Argentina",
    region_id=r_patagonia,
    producer_type="winery",
    description="Patagonia's most celebrated estate and one of the wine world's most remarkable stories — Piero Incisa della Rocchetta (of Sassicaia) identified old-vine Pinot Noir planted in 1932 and 1955 in the Río Negro desert and established Chacra in 2004. The estate produces Pinot Noir from these ancient ungrafted vines with assistance from Hans-Peter Weidmann and consultation from Château Pétrus's Jean-Claude Berrouet — wines of extraordinary elegance, mineral precision, and longevity that have established Patagonia as a world-class Pinot Noir source."
)
prod_chacra, new = PROD(
    name="Chacra Treinta y Dos Río Negro Pinot Noir",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_chacra,
    region_id=r_patagonia,
    origin_country="Argentina",
    description="From vines planted in 1932 in the Río Negro desert — the '32' designating the planting year of these ancient ungrafted Pinot Noir vines. One of the Southern Hemisphere's most compelling Pinot Noirs: translucent ruby, ethereally perfumed with fresh cherry, dried rose, graphite, iron mineral, and an almost meditative purity that comes from extreme old-vine desert conditions. Minimal intervention, indigenous yeasts, aged in old Burgundy barrels. Patagonia's most internationally celebrated wine.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_chacra, "Grilled Patagonian lamb with chimichurri negro and roasted root vegetables", "complement", "classic", "main", "The definitive Patagonian pairing — the region's iconic lamb with its finest wine. Chacra's mineral Pinot Noir perfectly complements Patagonian lamb's delicate yet deep character. Chimichurri negro's charred herb intensity bridges the wine's graphite mineral.")
    PAIR(prod_chacra, "Pan-seared Patagonian trout with caramelised fennel and dill oil", "complement", "established", "main", "River fish from the Río Negro valley with its most celebrated wine — Pinot Noir's mineral freshness and delicacy bridge to trout's subtle character. Fennel echoes the wine's floral notes while dill adds herbal freshness.")
    PAIR(prod_chacra, "Duck confit with morello cherry reduction and red quinoa", "complement", "established", "main", "Old-vine Pinot Noir with duck — one of the world's classic combinations. Cherry reduction bridges the wine's fruit while quinoa (a South American native) adds earthy depth and regional relevance.")
    PAIR(prod_chacra, "Tierra del Fuego king crab with lemon butter and herbs", "complement", "adventurous", "main", "An adventurous Patagonian pairing — the region's extraordinary king crab with its finest Pinot Noir. The wine's mineral salinity and delicacy bridge to the crab's sweetness in an unexpected combination that works through shared terroir.")

p_schroeder = P(
    name="Familia Schroeder",
    country="Argentina",
    region_id=r_patagonia,
    producer_type="winery",
    description="A German-Argentine family estate in Neuquén province, producing some of Patagonia's most consistently excellent Malbec, Pinot Noir, and sparkling wines from the volcanic basalt soils of the Andean foothills. Familia Schroeder's Saurus range — particularly the Saurus Reserve Pinot Noir and the traditional method sparkling Saurus Patagonian Select — have established the estate as one of the region's most reliable quality producers. The estate also produces an excellent brut nature pétillant that showcases the region's natural freshness."
)
prod_schroeder, new = PROD(
    name="Familia Schroeder Saurus Select Pinot Noir Patagonia",
    category="wine_still",
    subcategory="Pinot Noir",
    producer_id=p_schroeder,
    region_id=r_patagonia,
    origin_country="Argentina",
    description="From volcanic basalt soils in the Neuquén River valley — Pinot Noir grown in conditions of desert aridity, strong winds, and extreme diurnal temperature variation (20°C+). The result is a Pinot Noir of surprising elegance and freshness: transparent ruby, with fresh cherry, red rose, subtle earth, and a volcanic mineral character that sets it apart from warmer-climate examples. One of South America's most approachable and food-versatile Pinot Noirs.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_schroeder, "Asado de cordero patagónico with salsa criolla and roasted peppers", "complement", "classic", "main", "Patagonian lamb asado with Patagonian Pinot Noir — the region's iconic open-air cooking tradition with its most approachable wine. The wine's freshness cuts through lamb fat while its mineral depth bridges the salsa criolla.")
    PAIR(prod_schroeder, "Grilled rainbow trout with lemon, capers, and parsley butter", "complement", "established", "main", "The region's freshwater fish with its most versatile red wine — the Pinot Noir's mineral freshness and light body are the ideal complement to trout. The classical French sauce preparation bridges the wine's European variety heritage.")
    PAIR(prod_schroeder, "Smoked Patagonian trout rillettes with cornichons and rye crispbread", "complement", "established", "starter", "Preserved river fish with Patagonian Pinot — the wine's mineral freshness and fruit cut through the richness of rillettes. Cornichons echo its acidity while rye provides a nutty, earthy base.")
    PAIR(prod_schroeder, "Queso de cabra curado (aged goat's cheese) with membrillo", "complement", "suggested", "cheese", "The wine's red fruit and mineral freshness bridge to aged goat's milk cheese. Membrillo echoes its cherry fruit character while the cheese's tang complements its light tannin.")

# Final counts
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
print("\nDone.")
cur.close()
conn.close()
