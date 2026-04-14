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

# ── REGION 1: Ribera Sacra DO (Spain/Galicia) ────────────────────────────────
print("\n=== Region 1: Ribera Sacra ===")
r1 = R("Ribera Sacra", "Spain", "wine",
    designation_type="DO", designation_name="Ribera Sacra DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Ribera Sacra ('Sacred Riverbank') is one of Spain's most dramatic wine regions, carved into the steep schist terraces of the Sil and Miño river canyons in Galicia. Mencía grape produces wines of haunting elegance — light in colour but complex in aroma, with red cherry, wild herbs, floral lift, and mineral precision from the slate soils. The heroic viticulture on near-vertical slopes has attracted comparisons to the Mosel and Northern Rhône.",
    key_producers="Dominio do Bibei, Guímaro, Envínate, Regina Viarum",
    historical_context="The Ribera Sacra monasteries (Sacred Riverbanks) gave the region its name — Cistercian and Benedictine monks cultivated vines on the cliff terraces from the medieval period. The DO was established in 1996. The region gained sudden international attention in the 2010s when the natural wine movement highlighted Mencía's potential, and young producers like the Envínate collective transformed the perception of Galician red wines globally.")

VIN(r1, 2023, "excellent", "rising", "Outstanding Ribera Sacra vintage; Mencía on schist achieved exceptional aromatic complexity and mineral precision from the river canyon terroir")
VIN(r1, 2022, "very_good", "stable", "Fine balanced year with elegant, perfumed Mencía character; good typicity from the steep slate terraces")
VIN(r1, 2021, "good", "stable", "Cooler year with more restrained Mencía; excellent acidity and floral character with good varietal precision")
VIN(r1, 2020, "excellent", "rising", "Benchmark vintage; extraordinary schist mineral depth and Mencía aromatic complexity with excellent aging structure")
VIN(r1, 2019, "very_good", "rising", "Classic vintage with fine Mencía expression; wild herb, cherry, and river canyon mineral in fine harmony")

prod1a_id = P("Dominio do Bibei", "Spain", r1, "winery",
    "The benchmark estate of Ribera Sacra's quality revival; Sara Pérez and René Barbier Jr.'s Dominio do Bibei produces Mencía and indigenous white varieties from ancient schist terraces with the finesse and mineral precision that puts Ribera Sacra in conversation with Burgundy and the Northern Rhône.")
prod1a, new1a = PROD("Dominio do Bibei Lapola Ribera Sacra", "wine_still", prod1a_id, r1, "Spain",
    subcategory="red", price_tier="premium",
    description="Dominio do Bibei's flagship Mencía: Lapola from ancient schist terraces above the Sil River canyon. Elegant red cherry, wild violet, riverbed mineral, and subtle herb complexity. Among Spain's most refined and mineral reds — a wine that redefines what Galician red wine can achieve.")
if new1a:
    PAIR(prod1a, "Pimientos de Padrón fried in olive oil with sea salt", "complement", "classic", "aperitif",
        "Galicia's beloved blistered peppers with sea salt and olive oil are the region's defining aperitif food for Mencía; simple, honest, and perfect with the wine's freshness")
    PAIR(prod1a, "Lacón con grelos (cured pork shoulder with turnip tops and potatoes)", "complement", "classic", "main",
        "Galicia's most beloved traditional dish — cured pork with bitter greens — is the perfect regional match for Mencía's mineral freshness and gentle tannin")
    PAIR(prod1a, "Grilled lamprey with lemon, parsley, and olive oil", "complement", "established", "fish_course",
        "Lamprey is Galicia's traditional delicacy from the Miño and Sil rivers; Mencía's light body and mineral character make it one of the rare red wines that works with river lamprey")
    PAIR(prod1a, "Cocido gallego (Galician stew with chickpeas, pork, and greens)", "complement", "classic", "main",
        "Galicia's great sustaining stew with its smoky pork and bitter greens needs Mencía's freshness and mineral backbone to balance the richness")

prod1b_id = P("Guímaro", "Spain", r1, "winery",
    "One of Ribera Sacra's most respected artisan producers; Pedro Rodríguez's biodynamic estate produces Mencía of remarkable purity and mineral depth from terraced schist vineyards — wines that show what the variety can achieve when treated with the same reverence as Pinot Noir.")
prod1b, new1b = PROD("Guímaro Ribeira Sacra Tinto", "wine_still", prod1b_id, r1, "Spain",
    subcategory="red", price_tier="mid_range",
    description="Guímaro's benchmark Mencía: old vine schist terraces in Ribeira Sacra (Ourense side) producing elegant, perfumed Mencía with cherry, violet, wild herbs, and river slate mineral. The accessible introduction to Guímaro's quality — consistently among the region's finest values.")
if new1b:
    PAIR(prod1b, "Pulpo a feira (Galician octopus with olive oil, paprika, and sea salt)", "complement", "classic", "starter",
        "Galicia's most famous dish — boiled octopus with paprika — works beautifully with a light, mineral red like Guímaro's Mencía; the wine's freshness cuts through the olive oil richness")
    PAIR(prod1b, "Zamburiñas (Galician queen scallops) grilled in butter and garlic", "complement", "established", "starter",
        "Small Galician scallops with butter and garlic work with lighter Mencía in the same way Pinot works with scallops in Burgundy; the regional affinity is genuine")
    PAIR(prod1b, "Caldo gallego (Galician white bean and greens soup)", "complement", "classic", "casual",
        "Galicia's everyday white bean and greens soup is the casual, authentic pairing for Ribeira Sacra Mencía in a Galician restaurant or kitchen")
    PAIR(prod1b, "Grilled beef chuleta with Pimientos de Padrón and Galician potatoes", "complement", "established", "main",
        "Simple grilled beef with Galician peppers and potatoes is an honest regional meal that showcases Mencía's capacity to accompany both fish and red meat")

# ── REGION 2: Rueda DO (Spain/Castile-León) ──────────────────────────────────
print("\n=== Region 2: Rueda ===")
r2 = R("Rueda", "Spain", "wine",
    designation_type="DO", designation_name="Rueda DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Rueda is Spain's most celebrated white wine DO outside Rías Baixas, producing aromatic, mineral whites from the Verdejo grape on the high-altitude limestone and chalk plateau of Castile-León west of Valladolid. Verdejo at its finest shows fennel, white peach, herbs, and a characteristic bitter almond finish — Spain's answer to Sauvignon Blanc in freshness and food versatility.",
    key_producers="Marqués de Riscal (Rueda), Ossian, José Pariente, Naia",
    historical_context="Rueda's wine tradition dates to the medieval period when the Cistercian monastery of Santa María promoted cultivation of Verdejo, believed indigenous to the region. The DO was established in 1980 — Spain's first exclusively white wine appellation. The international Sauvignon Blanc craze of the 1990s initially threatened Verdejo's identity, but today the native variety is celebrated for its distinctive character superior to the international alternative.")

VIN(r2, 2023, "excellent", "stable", "Outstanding Rueda vintage; Verdejo achieved exceptional aromatic freshness and mineral precision from the limestone chalk plateau")
VIN(r2, 2022, "very_good", "stable", "Fine balanced year with classic Verdejo character; fennel, white peach, and bitter almond well expressed with good freshness")
VIN(r2, 2021, "good", "stable", "Cooler year with more restrained aromatics; excellent mineral acidity and good varietal typicity")
VIN(r2, 2020, "very_good", "stable", "Strong vintage with good Verdejo concentration; aromatic richness and mineral length from the high-altitude limestone")
VIN(r2, 2019, "excellent", "rising", "Benchmark Rueda vintage; extraordinary Verdejo depth with fennel-herb complexity and the distinctive bitter almond finish")

prod2a_id = P("Ossian", "Spain", r2, "winery",
    "The most prestigious and international producer of Rueda; Ossian's old vine Verdejo from pre-phylloxera Rueda vineyards (90+ year old vines) produces a wine that has single-handedly elevated the perception of Verdejo from simple fresh white to serious, age-worthy Spanish white wine.")
prod2a, new2a = PROD("Ossian Rueda Verdejo", "wine_still", prod2a_id, r2, "Spain",
    subcategory="white", price_tier="premium",
    description="The most celebrated Verdejo in the world: Ossian's old vine Rueda from pre-phylloxera vines on chalk-limestone soils. Fermented and aged in 600L barrels producing a richly textured, mineral Verdejo of extraordinary complexity — fennel, white peach, hazelnut, and chalk mineral. An age-worthy Spanish white that challenges top white Burgundy.")
if new2a:
    PAIR(prod2a, "Grilled lubina (European sea bass) with fennel, lemon, and herb oil", "complement", "classic", "fish_course",
        "Sea bass with fennel mirrors Ossian's fennel aromatics precisely; lemon and herb oil amplify the wine's citrus brightness and mineral complexity")
    PAIR(prod2a, "Langostinos a la plancha with garlic alioli and lemon", "complement", "classic", "starter",
        "Grilled tiger prawns with garlic and lemon are the definitive Verdejo pairing in any Castilian fine dining setting; the wine's freshness and herb character complete the dish")
    PAIR(prod2a, "Cured Ibérico ham (Jamón Ibérico de Bellota) with melon and fig", "complement", "established", "starter",
        "Spain's greatest delicacy with its nutty fat and acorn sweetness is a natural pairing for mineral Verdejo; melon and fig add sweetness to balance the wine's bitter almond")
    PAIR(prod2a, "Tortilla española with fresh herbs and aged Manchego shavings", "complement", "established", "casual",
        "The Spanish omelette with fresh herbs and Manchego cheese is one of Spain's great comfort foods for Rueda Verdejo; the wine's herbal freshness cuts through the egg richness")

prod2b_id = P("José Pariente", "Spain", r2, "winery",
    "One of Rueda's most consistent and celebrated family estates; the Pariente family's biodynamic Verdejo wines from high-altitude chalk-limestone soils achieve benchmark freshness and mineral definition — consistently among Spain's finest white wines at accessible prices.")
prod2b, new2b = PROD("José Pariente Rueda Verdejo", "wine_still", prod2b_id, r2, "Spain",
    subcategory="white", price_tier="mid_range",
    description="José Pariente's benchmark organic Verdejo from Rueda's chalk-limestone plateau; clean, aromatic, and precise with grapefruit, fennel frond, white peach, and mineral freshness. The reference Rueda Verdejo at mid-range pricing — Spain's most reliable and versatile white wine for everyday fine dining.")
if new2b:
    PAIR(prod2b, "Espárragos de Navarra (white asparagus) with vinaigrette and jamón", "complement", "classic", "starter",
        "Spanish white asparagus from Navarra with cured ham is the Iberian spring classic that meets Verdejo's herbal character and bright acidity perfectly")
    PAIR(prod2b, "Ensaladilla rusa (Russian salad) with tuna, olive, and mayonnaise", "complement", "classic", "casual",
        "Spain's beloved potato salad with tuna and olives is the tapas bar classic for fresh Verdejo; the wine's acidity cuts through the mayonnaise richness")
    PAIR(prod2b, "Grilled cogote de merluza (hake collar) with pil-pil sauce", "complement", "classic", "fish_course",
        "Hake collar's rich gelatinous flesh with pil-pil emulsion needs Verdejo's freshness and mineral acidity to balance; a quintessential Spanish fish-white wine pairing")
    PAIR(prod2b, "Croquetas de jamón ibérico with aioli", "complement", "established", "casual",
        "Spain's most beloved tapas — crispy Ibérico ham croquetas — are refreshed by Verdejo's bright acidity and herbal freshness; the wine cuts through the béchamel richness")

# ── REGION 3: Bierzo DO (Spain/Castile-León) ─────────────────────────────────
print("\n=== Region 3: Bierzo ===")
r3 = R("Bierzo", "Spain", "wine",
    designation_type="DO", designation_name="Bierzo DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Bierzo occupies a transitional zone between Galicia and Castile in northwestern Spain, producing elegant, mineral reds from the indigenous Mencía grape on slate soils in a valley carved by the Sil River. The wines show greater depth and structure than Ribeira Sacra Mencía due to the continental climate influence, with dark cherry, floral lift, spice, and a distinctive mineral slate character. The region has attracted serious investment and international attention.",
    key_producers="Descendientes de J. Palacios, Pittacum, Dominio de Tares, Paixar",
    historical_context="Bierzo's wine tradition dates to Roman times when the Via Traiana crossed the region. The modern quality era began dramatically when Álvaro Palacios and his nephew Ricardo Pérez Palacios arrived in 1999, producing La Faraona and other single-vineyard Mencías from ancient slate vineyards that immediately attracted international attention and critical acclaim, transforming Bierzo's global perception overnight.")

VIN(r3, 2022, "excellent", "rising", "Outstanding Bierzo vintage; Mencía on slate achieved exceptional concentration and mineral depth from the valley's ideal growing conditions")
VIN(r3, 2021, "very_good", "stable", "Fine balanced year with elegant, mineral Mencía character; floral lift and dark cherry with good aging structure")
VIN(r3, 2020, "excellent", "rising", "Benchmark vintage; extraordinary Mencía depth and slate mineral precision — among the decade's finest from the region")
VIN(r3, 2019, "very_good", "rising", "Classic Bierzo vintage with excellent varietal expression; dark cherry, violet, and mineral slate in fine balance")
VIN(r3, 2018, "good", "stable", "Accessible year with good Mencía typicity; softer tannins and approachable dark fruit for earlier drinking")

prod3a_id = P("Descendientes de J. Palacios", "Spain", r3, "winery",
    "The estate that transformed Bierzo into an internationally celebrated wine region; Ricardo Pérez Palacios and Álvaro Palacios's single-vineyard Mencías from ancient slate vineyards — particularly La Faraona — command prices rivalling the finest Burgundy and have brought Bierzo global prestige.")
prod3a, new3a = PROD("Descendientes de J. Palacios Pétalos Bierzo", "wine_still", prod3a_id, r3, "Spain",
    subcategory="red", price_tier="mid_range",
    description="The accessible introduction to the Palacios Bierzo estate: Pétalos del Bierzo from village-level Mencía with slate mineral character. Dark cherry, violet, floral lift, and mineral slate — extraordinary quality and value for a Palacios wine. The entry point to Bierzo's greatest producers.")
if new3a:
    PAIR(prod3a, "Botillo del Bierzo (stuffed pork intestines with ribs and spices, slow-cooked)", "complement", "classic", "main",
        "Bierzo's regional GI product — the botillo sausage — slow-cooked with potatoes and cabbage is the defining regional pairing for Mencía; the wine's freshness balances the richness")
    PAIR(prod3a, "Jamón serrano croquetas with roasted piquillo pepper sauce", "complement", "established", "casual",
        "Cured ham croquettes with sweet piquillo pepper sauce is a natural casual tapas pairing for Bierzo Mencía's cherry fruit and mineral freshness")
    PAIR(prod3a, "Roasted lamb shoulder with herbs, garlic, and Bierzo pimentón", "complement", "classic", "main",
        "Castilian lamb with smoked pimentón (paprika) is a natural match for Pétalos's dark cherry and mineral slate; the lamb's fat is tamed by the wine's vibrant acidity")
    PAIR(prod3a, "Lentil stew (lentejas) with chorizo, morcilla, and vegetables", "complement", "classic", "main",
        "Spanish lentil stew with sausage and black pudding is the everyday comfort food pairing for Bierzo Mencía; the wine's freshness and mineral cut through the rich legume depth")

prod3b_id = P("Pittacum", "Spain", r3, "winery",
    "One of Bierzo's most consistently excellent producers focusing entirely on old vine Mencía; Pittacum's organic estate wines from ancient slate-soil Mencía vines show the variety's capacity for elegance and longevity when crafted without the intervention that can mask terroir.")
prod3b, new3b = PROD("Pittacum Bierzo Mencía", "wine_still", prod3b_id, r3, "Spain",
    subcategory="red", price_tier="mid_range",
    description="Pittacum's benchmark organic Mencía from Bierzo's ancient slate vineyards; dark cherry, violet, spice, and mineral slate with firm but polished tannins. A reliable and authentic Bierzo expression at honest prices — showing the variety's depth without the Palacios price premium.")
if new3b:
    PAIR(prod3b, "Grilled chuletón (thick beef rib chop) with Padron peppers and sea salt", "complement", "established", "main",
        "A thick chuletón with blistered Padron peppers is the Galician-Castilian border steak experience; Pittacum's mineral Mencía handles both the beef's richness and the pepper's freshness")
    PAIR(prod3b, "Morcilla de Burgos (Castilian blood sausage) with roasted peppers", "complement", "classic", "starter",
        "Castilian blood pudding with roasted peppers is a classic northern Spanish tapas pairing for mineral Mencía; the iron richness meets the wine's dark fruit and slate mineral")
    PAIR(prod3b, "Slow-cooked oxtail with red wine, black olives, and root vegetables", "complement", "established", "main",
        "Oxtail rabo de toro with olives and root vegetables is the slow-food Spanish classic that requires Mencía's freshness and mineral backbone to lift the rich braising liquid")
    PAIR(prod3b, "Cabra cheese from Bierzo with quince paste and toasted pine nuts", "bridge", "established", "cheese",
        "Local Bierzo goat cheese with quince and pine nuts creates a direct regional cheese pairing for Pittacum's mineral Mencía — place-specific and authentic")

# ── REGION 4: Vinho Verde DOC (Portugal) ────────────────────────────────────
print("\n=== Region 4: Vinho Verde ===")
r4 = R("Vinho Verde", "Portugal", "wine",
    designation_type="DOC", designation_name="Vinho Verde DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Vinho Verde ('Green Wine') is Portugal's largest DOC, covering the cool, rainy Minho region of northwest Portugal where Alvarinho, Loureiro, Arinto, and Trajadura grapes produce wines of electric freshness, low alcohol, and mineral acidity. The best sub-regions — Monção e Melgaço (Alvarinho) and Lima (Loureiro) — produce wines of genuine complexity and distinction. The light pétillance (slight effervescence) is traditional and characterful.",
    key_producers="Quinta de Soalheiro, Anselmo Mendes, Palácio da Brejoeira, Niepoort",
    historical_context="Vinho Verde has been produced in the Minho since at least the medieval period. The DOC was established in 1908 — Portugal's first appellation. For decades it was exported primarily as cheap, slightly fizzy white wine, but the premium tier — particularly Alvarinho from the Monção e Melgaço sub-region near the Spanish border — has transformed the perception of Vinho Verde into a serious fine wine category internationally.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Vinho Verde vintage; exceptional Alvarinho freshness and mineral precision from the Monção e Melgaço granite soils")
VIN(r4, 2022, "very_good", "stable", "Fine balanced year with classic Vinho Verde freshness; good Loureiro and Alvarinho expression with mineral acidity")
VIN(r4, 2021, "good", "stable", "Rainy year with typical Minho challenges; careful viticulture yielded good aromatic freshness and light effervescence")
VIN(r4, 2020, "very_good", "stable", "Strong vintage with good concentration; Alvarinho from Monção showing exceptional complexity and mineral depth")
VIN(r4, 2019, "excellent", "rising", "Benchmark vintage; extraordinary Alvarinho concentration from the granite terroir with elegant pétillance and mineral salinity")

prod4a_id = P("Quinta de Soalheiro", "Portugal", r4, "winery",
    "The pioneering estate that revealed Alvarinho's potential as a serious fine wine variety; the Cerdeira family's Soalheiro estate near Melgaço produces Portugal's most celebrated Alvarinho from granite soils close to the Spanish border — wines that rival Galicia's best Albariño in complexity and mineral depth.")
prod4a, new4a = PROD("Soalheiro Alvarinho Vinho Verde", "wine_still", prod4a_id, r4, "Portugal",
    subcategory="white", price_tier="premium",
    description="The benchmark Portuguese Alvarinho: Soalheiro's estate wine from granite soils in Monção e Melgaço. White peach, apricot, citrus blossom, and granite mineral salinity — more textured and serious than typical Vinho Verde. The wine that established Alvarinho's premium identity and Portugal's answer to Galician Albariño.")
if new4a:
    PAIR(prod4a, "Lamprey (lampreia) à Bordalesa with blood sauce and rice", "complement", "classic", "main",
        "Portugal's most prized river delicacy — lamprey in its own blood — is the traditional Minho pairing for Alvarinho; a regional cuisine-wine unity of genuine authenticity")
    PAIR(prod4a, "Bacalhau à Gomes de Sá (salt cod with potatoes, eggs, and olives)", "complement", "classic", "main",
        "Portugal's most beloved salt cod preparation with its savoury, olive-rich sauce is refreshed perfectly by Soalheiro's mineral Alvarinho freshness")
    PAIR(prod4a, "Grilled percebes (goose barnacles) with lemon — as in Galicia", "complement", "classic", "aperitif",
        "The same Atlantic barnacles enjoyed in Galicia with Albariño apply to Alvarinho across the Portuguese border; saline oceanic character amplifies the wine's mineral salinity")
    PAIR(prod4a, "Caldo verde (Portuguese kale soup) with chouriço and cornbread", "complement", "established", "casual",
        "Portugal's most iconic soup with its spiced chouriço and hearty kale is the everyday Minho pairing for Alvarinho; the wine's freshness lightens the soup's richness")

prod4b_id = P("Anselmo Mendes", "Portugal", r4, "winery",
    "Vinho Verde's most prolific and talented winemaker; Anselmo Mendes consults across the region while producing his own benchmark Alvarinho and Loureiro wines that show the full range of Vinho Verde's potential — from simple pétillant freshness to complex, age-worthy single-vineyard expressions.")
prod4b, new4b = PROD("Anselmo Mendes Parcela Única Alvarinho", "wine_still", prod4b_id, r4, "Portugal",
    subcategory="white", price_tier="mid_range",
    description="Anselmo Mendes's single-parcel Alvarinho from Monção e Melgaço; aromatic and precise with apricot, white flowers, citrus peel, and granite mineral. The accessible expression of premium Vinho Verde Alvarinho — bridging everyday refreshment with the serious mineral complexity of the sub-region's finest wines.")
if new4b:
    PAIR(prod4b, "Sarrabulho (Minho pork rice with blood and offal)", "complement", "established", "main",
        "The Minho's distinctive rice dish with pork blood is an authentic regional pairing for Alvarinho; the wine's freshness cuts through the rich, iron-heavy preparation")
    PAIR(prod4b, "Grilled sardines with sea salt, lemon, and bread", "complement", "classic", "casual",
        "Portugal's national summer food — grilled sardines eaten with bread and lemon — is the most honest and authentic Vinho Verde pairing; the wine's acidity and freshness are designed for this")
    PAIR(prod4b, "Ameijoas à Bulhão Pato (clams with coriander, garlic, and white wine)", "complement", "classic", "starter",
        "This celebrated Portuguese clam preparation with coriander and white wine creates culinary continuity with Alvarinho's mineral freshness; the wine used in cooking bridges beautifully")
    PAIR(prod4b, "Queijo de Terrincho (Trás-os-Montes sheep cheese) with honey", "bridge", "established", "cheese",
        "Northern Portuguese sheep cheese with wild honey bridges Alvarinho's stone fruit and mineral character — a simple, authentic Minho cheese pairing")

# ── REGION 5: Martinborough (New Zealand) ────────────────────────────────────
print("\n=== Region 5: Martinborough ===")
r5 = R("Martinborough", "New Zealand", "wine",
    designation_type="appellation", designation_name="Martinborough GI",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Martinborough is one of New Zealand's most distinctive wine regions, a small wine-producing enclave on the southern tip of the North Island, sheltered from rain by the Rimutaka and Tararua Ranges. The free-draining Martinborough Terrace — ancient river gravels over clay — and warm, dry autumn conditions create Pinot Noir and Pinot Gris of remarkable elegance, concentration, and mineral depth that compete with Central Otago for New Zealand's finest Pinot.",
    key_producers="Ata Rangi, Dry River, Te Kairanga, Martinborough Vineyard",
    historical_context="Martinborough's wine industry began in 1980 when Dr. Neil McCallum's Dry River and Clive Paton's Ata Rangi simultaneously planted Pinot Noir on the Martinborough Terrace. A 1980 scientific study identified the terrace's soil and climate similarity to Burgundy, attracting those first serious plantings. The appellation grew slowly but consistently, gaining a reputation for elegance and food-friendliness that distinguishes it from Central Otago's more concentrated style.")

VIN(r5, 2023, "very_good", "stable", "Fine Martinborough vintage; Pinot Noir showed excellent red fruit purity and gravel mineral character from the terrace terroir")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage; exceptional Pinot Noir concentration and mineral depth from the Martinborough Terrace's ancient river gravels")
VIN(r5, 2021, "very_good", "stable", "Excellent balanced year with elegant, mineral Pinot and fine aromatic Pinot Gris; good typicity and aging structure")
VIN(r5, 2020, "good", "stable", "Accessible year with classic Martinborough character; red cherry and mineral freshness with good food versatility")
VIN(r5, 2019, "excellent", "rising", "Benchmark Martinborough vintage; extraordinary gravel-mineral Pinot Noir with 10-year aging potential")

prod5a_id = P("Ata Rangi", "New Zealand", r5, "winery",
    "The founding estate and international benchmark of Martinborough Pinot Noir; Clive and Phyll Paton's Ata Rangi ('New Beginning') has produced New Zealand's most consistently acclaimed and age-worthy Pinot Noir from the Martinborough Terrace since 1980 — one of the Southern Hemisphere's great wine estates.")
prod5a, new5a = PROD("Ata Rangi Pinot Noir", "wine_still", prod5a_id, r5, "New Zealand",
    subcategory="red", price_tier="premium",
    description="Ata Rangi's estate Pinot Noir from the Martinborough Terrace: a blend of multiple clones on river gravel over clay. Red cherry, spice, dried herb, and mineral gravel complexity with remarkable aging potential — one of New Zealand's most consistently excellent Pinot Noirs and a Martinborough benchmark since 1980.")
if new5a:
    PAIR(prod5a, "Rack of New Zealand lamb with mint, rosemary, and natural jus", "complement", "classic", "main",
        "New Zealand's world-famous lamb with mint is the definitive Martinborough Pinot Noir pairing; the wine's delicacy and mineral freshness perfectly complements lamb's sweet gaminess")
    PAIR(prod5a, "Seared duck breast with cherry compote and beetroot purée", "complement", "classic", "main",
        "Duck with cherry is Pinot's universal luxury pairing; Ata Rangi's gravel mineral character and red fruit depth make this the premium Martinborough version")
    PAIR(prod5a, "Wild mushroom and truffle crostini with Parmigiano and chervil", "complement", "established", "starter",
        "Wild mushroom and truffle amplify Martinborough Pinot's earthy, mineral depth; Parmigiano adds umami salinity to echo the wine's complexity")
    PAIR(prod5a, "Aged Kapiti Kikorangi blue cheese with quince paste and walnut", "contrast", "established", "cheese",
        "New Zealand's premium blue cheese with quince and walnut creates the domestic cheese pairing for Ata Rangi's Pinot — a contrast of creamy intensity against the wine's mineral freshness")

prod5b_id = P("Dry River", "New Zealand", r5, "winery",
    "Martinborough's most prestigious and allocated estate; Neil McCallum's founding winery produces Pinot Noir, Pinot Gris, and Chardonnay of extraordinary depth and longevity from the Martinborough Terrace — wines that require years of cellaring and are released only when ready, achieving cult status internationally.")
prod5b, new5b = PROD("Dry River Pinot Gris", "wine_still", prod5b_id, r5, "New Zealand",
    subcategory="white", price_tier="premium",
    description="Dry River's benchmark Pinot Gris: arguably New Zealand's finest, this Martinborough Terrace Pinot Gris is whole-bunch pressed with skin contact, aged in old oak. White peach, ginger, honey, and mineral gravel complexity — more Alsatian grand cru in ambition than the typical fresh New Zealand style. Exceptional and rare.")
if new5b:
    PAIR(prod5b, "Roasted poussin with spiced Moroccan chermoula and couscous", "complement", "established", "main",
        "Moroccan-spiced small chicken with chermoula's herbs and spice match Dry River Pinot Gris's textured richness and ginger-honey depth — an aromatic pairing of genuine interest")
    PAIR(prod5b, "Seared scallops with golden raisin purée and smoked almonds", "complement", "established", "fish_course",
        "Scallop sweetness with golden raisin echoes the wine's honey and stone fruit; smoked almonds add a savoury mineral note to bridge the Pinot Gris's rich texture")
    PAIR(prod5b, "Foie gras mi-cuit with Gewürztraminer jelly and brioche toast", "complement", "classic", "starter",
        "Foie gras with aromatic wine jelly is the Alsatian luxury pairing translated to Martinborough; Dry River's Alsatian-style Pinot Gris is the natural vehicle")
    PAIR(prod5b, "Thai green curry with prawns, coconut, and lemongrass", "bridge", "established", "main",
        "Aromatic Thai curry with coconut richness and lemongrass is a natural match for off-dry style Pinot Gris; the wine's ginger and honey bridge across to Southeast Asian spice")

# ── Summary ──────────────────────────────────────────────────────────────────
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
conn.close()
