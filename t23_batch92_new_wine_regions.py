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

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Rioja Oriental / Rioja Alta ────────────────────────────────────
print("\n=== Region 1: Rioja Alta ===")
r1 = R("Rioja Alta", "Spain", "wine",
    designation_type="DOCa",
    designation_name="Rioja DOCa",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="The western sub-zone of Rioja DOCa, centred on Haro and the Ebro River — the highest altitude, coolest, and wettest part of the Rioja appellation. Calcareous clay soils over iron-rich limestone produce Tempranillo-dominant wines of the greatest elegance and aging potential in all of Rioja. La Rioja Alta, CVNE, Marqués de Murrieta, López de Heredia, and Muga are headquartered in or near Haro in the historic 'Barrio de la Estación' (railway station district) established in the 1890s.",
    key_producers="López de Heredia, La Rioja Alta, CVNE, Muga, Marqués de Murrieta",
    historical_context="Bordeaux négociants fleeing phylloxera in the 1870s established Rioja's wine industry at Haro's railway station — they brought their expertise and barrique-aging tradition that defined Rioja's Gran Reserva style; the Barrio de la Estación is now a UNESCO heritage site.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2019, "exceptional", "stable"), (2018, "excellent", "stable"), (2016, "excellent", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("López de Heredia", "winery", r1, "Spain",
    production_philosophy="traditional",
    philosophy_description="The most traditional bodega in Rioja — founded in 1877 at Haro's railway station, López de Heredia still uses 19th-century methods: American oak barriques, extended barrel aging (6-10 years for Reserva and Gran Reserva), and filtration through Burgundy basket presses. Their wines achieve a tertiary complexity unlike anything else in Spain.",
    reputation_narrative="Spain's most celebrated traditional winery; Viña Tondonia Gran Reserva is among Spain's most iconic wines.",
    price_positioning="ultra_premium")

prod1b_id = P("Muga", "winery", r1, "Spain",
    production_philosophy="traditional",
    philosophy_description="One of Haro's most respected family bodegas — Muga ages all wines in American and French oak made by in-house coopers. The Prado Enea Gran Reserva is one of Rioja's most traditional and consistent expressions of Tempranillo's aging potential.",
    reputation_narrative="One of Rioja's most beloved family estates; Prado Enea is a benchmark for traditional Rioja Gran Reserva.",
    price_positioning="premium")

prod1a, new1a = PROD("López de Heredia Viña Tondonia Gran Reserva", "wine_still", prod1a_id, r1, "Spain",
    subcategory="Tempranillo Blend",
    description="A living fossil of Spanish wine — Tondonia Gran Reserva spends 6+ years in American oak barrels at the Haro bodega before bottling, producing a wine of extraordinary tertiary complexity: dried cherry, orange peel, tobacco, cedar, and vanilla. Released only when the bodega deems it ready, often 15-20 years after harvest.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Roast lamb shoulder (lechazo) with garlic and herbs", "complement", "classic", "main",
         "The defining Castilian roast lamb pairing with traditional Rioja Gran Reserva — a Spanish haute cuisine archetype.")
    PAIR(prod1a, "Kokotxas (salt cod cheeks) al pil-pil with pimiento", "bridge", "established", "main",
         "Basque salt cod preparation bridges with Rioja's tertiary complexity through the olive oil emulsion sauce.")
    PAIR(prod1a, "Aged Idiazabal (3-year smoked) with quince jelly", "complement", "classic", "cheese",
         "The smoke of aged Idiazabal echoes Tondonia's tertiary oak; quince bridges the wine's dried-fruit character.")
    PAIR(prod1a, "Perdiz estofada (partridge stew) with picante pimientos", "complement", "established", "main",
         "Spanish game bird stew with Rioja's most traditional wine — the wine's age and complexity frame the partridge.")

prod1b, new1b = PROD("Muga Prado Enea Gran Reserva", "wine_still", prod1b_id, r1, "Spain",
    subcategory="Tempranillo Blend",
    description="Muga's flagship Gran Reserva from the oldest vine parcels — Tempranillo-dominant blend aged for 3 years in American and French oak then extensive bottle aging before release. Prado Enea shows classic Rioja elegance: tobacco, cherry, vanilla, and fine tannin with remarkable consistency across decades.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Chuletillas de cordero (baby lamb chops) with chimichurri", "complement", "classic", "main",
         "The simplest Rioja pairing — grilled lamb chops with a classic Gran Reserva is the region's fundamental combination.")
    PAIR(prod1b, "Duck confit with cherry jam and pommes sarladaises", "complement", "established", "main",
         "Bordeaux-influenced preparation echoes Rioja's French heritage and Tempranillo's cherry-fruit character.")
    PAIR(prod1b, "Txistorra (Basque cured sausage) with scrambled egg and truffle", "complement", "established", "casual",
         "Piquant Basque sausage with Gran Reserva Rioja — the wine's elegance tames the sausage's spice and fat.")
    PAIR(prod1b, "Manchego Curado with fig bread and hazelnuts", "complement", "classic", "cheese",
         "Classic Rioja cheese board — medium-aged Manchego with fig and hazelnut bridges Prado Enea's fruit and oak.")

# ── Region 2: Alentejo ───────────────────────────────────────────────────────
print("\n=== Region 2: Alentejo ===")
r2 = R("Alentejo", "Portugal", "wine",
    designation_type="DOC",
    designation_name="Alentejo DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Portugal's vast southern interior — the Alentejo covers a third of Portugal but produces just 8% of its wine. The dry, hot, Mediterranean climate and ancient granite and schist soils produce full-bodied, richly textured reds from Aragonez (Tempranillo), Trincadeira, Alicante Bouschet, and Touriga Nacional. Eight sub-regions including Évora, Reguengos, and Portalegre offer distinct expressions from cooler hillside vineyards to the hot plains.",
    key_producers="Esporão, Herdade do Mouchão, Eugénio de Almeida, Herdade das Servas, Cortes de Cima",
    historical_context="The Alentejo was Portugal's bread basket — wheat fields interrupted by cork oaks ('montado') that still define the landscape. The wine revolution began in the 1990s when Portuguese wine laws changed and investment poured into the region; the Alentejo is now Portugal's most commercially successful wine DOC.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Esporão", "winery", r2, "Portugal",
    production_philosophy="biodynamic",
    philosophy_description="One of Portugal's most important wine estates — Esporão in Reguengos de Monsaraz farms 450 hectares biodynamically across the Alentejo, producing a comprehensive range from entry-level Verdelho to their premium Torre do Esporão Reserva. The estate restaurant and visitor experience is Portugal's wine tourism benchmark.",
    reputation_narrative="Portugal's most complete wine estate; Esporão Monte Velho and Reserva are among Portugal's best-selling premium wines.",
    price_positioning="premium")

prod2b_id = P("Herdade do Mouchão", "winery", r2, "Portugal",
    production_philosophy="traditional",
    philosophy_description="The Reynolds family's estate near Aviz is the Alentejo's most historically significant and traditional producer — their Alicante Bouschet and Tonel single-barrel wines are aged in ancient cement tanks and old wood, producing Portugal's most distinctive and age-worthy Alentejo reds.",
    reputation_narrative="The Alentejo's most historically revered estate; Tonel series wines are among Portugal's rarest and most collectible.",
    price_positioning="ultra_premium")

prod2a, new2a = PROD("Esporão Reserva Tinto", "wine_still", prod2a_id, r2, "Portugal",
    subcategory="Aragonez-Touriga Nacional Blend",
    description="Esporão's flagship red — a blend of Aragonez, Touriga Nacional, Trincadeira, and Alicante Bouschet from the estate's best parcels. Rich, structured, and concentrated with dark plum, chocolate, and Mediterranean herb character, representing the Alentejo's warm-climate sophistication.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Migas com entrecosto (breadcrumb stew with pork ribs)", "complement", "classic", "main",
         "Alentejo's defining regional dish — bread-thickened pork preparation with the region's benchmark red wine.")
    PAIR(prod2a, "Ensopado de borrego (lamb stew with bread and coriander)", "complement", "classic", "main",
         "Alentejo's lamb bread-soup — coriander's freshness and lamb's richness bridge with the wine's Mediterranean depth.")
    PAIR(prod2a, "Grilled Ibérico secreto with piri piri marinade", "complement", "established", "main",
         "Ibérico pork's acorn-fat richness and heat from piri piri both find balance in Esporão's structured Alentejo red.")
    PAIR(prod2a, "Queijo de Évora (aged sheep's cheese) with fig preserve", "complement", "classic", "cheese",
         "The local sheep's cheese from Évora with fig jam mirrors the wine's dark fruit in a genuinely Alentejo pairing.")

prod2b, new2b = PROD("Herdade do Mouchão Alicante Bouschet", "wine_still", prod2b_id, r2, "Portugal",
    subcategory="Alicante Bouschet",
    description="Portugal's most celebrated Alicante Bouschet — the variety's red-fleshed grapes produce ink-dark, massively structured wines from Mouchão's ancient terraces near Aviz. Complex, tannic, and extraordinarily age-worthy with dark plum, iron, chocolate, and a distinctive mineral depth from the ancient soils.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Javali (wild boar) slow-braised with orange, cinnamon, and olives", "complement", "classic", "main",
         "Alentejo's native wild boar with the region's most powerful red — the orange and cinnamon bridge the tannin.")
    PAIR(prod2b, "Carne de porco à Alentejana (pork with clams and coriander)", "complement", "classic", "main",
         "Portugal's most beloved pork-and-seafood dish from the Alentejo — regional cooking with its greatest regional red.")
    PAIR(prod2b, "Toucinho do céu (Alentejo almond and egg yolk cake)", "contrast", "adventurous", "dessert",
         "The Alentejo's traditional convent cake — sweet almond and yolk against Alicante Bouschet's powerful tannin.")
    PAIR(prod2b, "Aged Azeitão sheep's cheese with thyme honey", "complement", "established", "cheese",
         "Aged Setúbal sheep's cheese with thyme honey — earthy, runny Azeitão handles Mouchão's tannic power.")

# ── Region 3: Dao ────────────────────────────────────────────────────────────
print("\n=== Region 3: Dão ===")
r3 = R("Dão", "Portugal", "wine",
    designation_type="DOC",
    designation_name="Dão DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Portugal's most underrated premium wine region — the granite plateau of the Dão, surrounded by mountains in central Portugal, produces wines of extraordinary finesse and mineral elegance from Touriga Nacional, Jaen (Mencía), and Encruzado (white). The region's altitude (400-800m), well-distributed rainfall, and poor granite soils create wines more elegant than the Alentejo and structurally comparable to Barolo or Burgundy. Dão's potential has been masked by cooperative domination until a recent wave of quality-focused estates.",
    key_producers="Quinta dos Roques, Álvaro Castro, Quinta da Pellada, Boas Quintas",
    historical_context="The Dão was Portugal's most regulated wine region for decades — only co-operatives could buy grapes, suppressing quality. The regulation was lifted after Portugal joined the EU in 1986; the subsequent estate wine revolution is still unfolding, with the region now considered Portugal's most exciting for age-worthy fine wine.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Álvaro Castro", "winery", r3, "Portugal",
    production_philosophy="terroir_focused",
    philosophy_description="The Dão's most celebrated estate wine pioneer — Álvaro Castro's Quinta da Pellada and Primus wines have established Dão's international reputation through granite-grown Touriga Nacional and Encruzado of extraordinary precision and longevity.",
    reputation_narrative="The defining pioneer of quality Dão estate wine; Primus is Portugal's reference for Dão Touriga Nacional.",
    price_positioning="premium")

prod3b_id = P("Quinta dos Roques", "winery", r3, "Portugal",
    production_philosophy="traditional",
    philosophy_description="One of the Dão's largest and most consistent quality estates — Quinta dos Roques produces single-variety Touriga Nacional, Alfrocheiro, and Jaen wines of great precision alongside one of Portugal's most interesting white wines from Encruzado.",
    reputation_narrative="Among the Dão's most reliably excellent estates; Touriga Nacional Reserva is a reference for the variety.",
    price_positioning="premium")

prod3a, new3a = PROD("Álvaro Castro Dão Primus", "wine_still", prod3a_id, r3, "Portugal",
    subcategory="Touriga Nacional",
    description="Castro's flagship Dão red from old-vine Touriga Nacional on granite — a wine of remarkable elegance and mineral precision, aging like a great Burgundy with rose petal, tobacco, iron mineral, and fine tannin. One of Portugal's most distinctive and undervalued red wines.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Roasted kid (cabrito assado) with garlic, lemon, and rosemary", "complement", "classic", "main",
         "Dão's regional roast kid with the plateau's finest red wine — a Portuguese highland pairing of great authenticity.")
    PAIR(prod3a, "Wild mushroom and Dão cheese (Queijo da Serra) soup", "complement", "established", "starter",
         "Granite plateau mushrooms and local mountain cheese with granite-grown Touriga Nacional — pure Dão terroir.")
    PAIR(prod3a, "Leitão da Bairrada (suckling pig) with orange salt", "complement", "established", "main",
         "Central Portugal's iconic suckling pig from neighboring Bairrada with Dão's finest red — regional affinity.")
    PAIR(prod3a, "Queijo da Serra da Estrela at room temperature on crusty bread", "complement", "classic", "cheese",
         "Portugal's greatest mountain cheese — the runny Serra da Estrela with Dão's finest wine is a highland pairing.")

prod3b, new3b = PROD("Quinta dos Roques Dão Encruzado Reserva", "wine_still", prod3b_id, r3, "Portugal",
    subcategory="Encruzado",
    description="Dão's finest indigenous white variety from granite soils — Encruzado produces wines of striking mineral freshness, citrus, almond, and a persistent saline finish that uniquely defines the granite plateau terroir. Quinta dos Roques's Reserva is Dão's benchmark for the variety.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Bacalhau com broa (salt cod with corn bread crust)", "complement", "classic", "main",
         "Portugal's defining salt cod preparation with its finest granite white wine — a uniquely Portuguese pairing.")
    PAIR(prod3b, "Trout from the Mondego River with almonds and lemon butter", "complement", "classic", "fish_course",
         "The Dão plateau's river trout with its native white variety — a genuinely local Portuguese river pairing.")
    PAIR(prod3b, "Grilled sea bass with fennel, white wine, and herb oil", "complement", "established", "fish_course",
         "Clean white fish with Dão's mineral-precise Encruzado — the wine's salinity bridges through the fennel.")
    PAIR(prod3b, "Fresh Queijo Fresco with olive oil and fresh oregano", "complement", "classic", "cheese",
         "Fresh Portuguese cheese drizzled with olive oil — the simplest and most authentic Dão wine pairing.")

# ── Region 4: Xinomavro — Amyndeon ────────────────────────────────────────────
print("\n=== Region 4: Amynteon ===")
r4 = R("Amynteon", "Greece", "wine",
    designation_type="PDO",
    designation_name="Amynteon PDO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Northern Greece's highest-altitude and coolest PDO for Xinomavro — located on a high plateau at 550-700m above sea level near the Macedonian town of Amynteon. The cooler, more continental climate produces Xinomavro of exceptional freshness and elegance compared to neighbouring Naoussa, with higher natural acidity, more delicate aromatics, and earlier-drinking structure. The region also produces Greece's finest sparkling wine from Xinomavro.",
    key_producers="Alpha Estate, Κir-Yianni, Boutari, Thymiopoulos (Amynteon),",
    historical_context="Amynteon's wine tradition dates to ancient Macedonian times; the PDO was one of Greece's first in 1972; the cool plateau climate was long considered marginal for wine but is now seen as an advantage in a warming world producing fresher, more mineral expressions of Xinomavro.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Alpha Estate", "winery", r4, "Greece",
    production_philosophy="terroir_focused",
    philosophy_description="Angelos Iatridis and Makis Mavridis founded Alpha Estate in Amynteon in 1997, quickly establishing it as Greece's most internationally acclaimed estate — producing single-vineyard Xinomavro of extraordinary precision, Syrah, Merlot, and exceptional sparkling from the cool plateau vineyards.",
    reputation_narrative="Greece's most internationally decorated estate wine producer; Alpha Estate's wines define modern Greek fine wine.",
    price_positioning="premium")

prod4b_id = P("Boutari", "winery", r4, "Greece",
    production_philosophy="traditional",
    philosophy_description="The Boutari family has shaped Greek wine for over a century — their Amynteon and Naoussa Xinomavro wines set the traditional benchmark, while the Grande Reserve remains one of Greece's most important historic bottlings from the PDO.",
    reputation_narrative="Greece's most historic wine dynasty; Boutari's Naoussa Grande Reserve is a reference for traditional Xinomavro.",
    price_positioning="mid_range")

prod4a, new4a = PROD("Alpha Estate Xinomavro Single Vineyard Hedgehog", "wine_still", prod4a_id, r4, "Greece",
    subcategory="Xinomavro",
    description="From the Hedgehog vineyard on Amynteon's high plateau — Alpha Estate's single-vineyard Xinomavro showing the cooler PDO's distinctive character: more fragrant, fresher, and more elegant than Naoussa, with red cherry, dried rose, and mineral precision from the volcanic plateau soils.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Arni me skordalia (roast lamb with garlic purée)", "complement", "classic", "main",
         "Greek roast lamb with garlic sauce and Amynteon Xinomavro — the cool freshness of the wine matches the delicate lamb.")
    PAIR(prod4a, "Spanakopita with wild greens, feta, and dill", "complement", "established", "starter",
         "Greece's defining pie with Amynteon's most precise Xinomavro — fresh acidity mirrors the pie's herbal freshness.")
    PAIR(prod4a, "Grilled lamb chops with lemon and Greek rigani", "complement", "classic", "main",
         "The simplest Greek preparation — grilled lamb with Amynteon Xinomavro is the plateau's defining pairing.")
    PAIR(prod4a, "Aged Graviera Agrafon from the Pindos mountains", "complement", "established", "cheese",
         "Hard aged Greek sheep's cheese from the Pindos mirrors the plateau's mineral character — Greek mountain pairing.")

prod4b, new4b = PROD("Boutari Naoussa Grande Reserve", "wine_still", prod4b_id, r4, "Greece",
    subcategory="Xinomavro",
    description="Boutari's historic Grand Reserve — extended barrel and bottle aging of Naoussa Xinomavro from exceptional vintages, producing Greece's most traditionally structured and age-worthy example of the variety. Tomato skin, iron, dried rose, and fine tannin with 20+ year potential.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Moussaka with béchamel and aged Kefalotyri", "complement", "classic", "main",
         "Greece's defining baked dish with its most traditional red wine — Xinomavro's acidity cuts the béchamel richness.")
    PAIR(prod4b, "Stifado (rabbit stew) with pearl onions and allspice", "complement", "classic", "main",
         "Allspice and onion stifado mirrors Xinomavro's characteristic dried-spice and acidity perfectly.")
    PAIR(prod4b, "Roasted red peppers with feta and Kalamata olives", "complement", "established", "starter",
         "Greek mezze platter with structured Xinomavro — the wine's acidity cuts through feta's brine and olive oil.")
    PAIR(prod4b, "Aged Kefalograviera cheese with local thyme honey", "complement", "established", "cheese",
         "Northern Greek aged hard cheese with Boutari's historic Naoussa — thyme honey bridges both through aromatics.")

# ── Region 5: Muscat de Beaumes-de-Venise ────────────────────────────────────
print("\n=== Region 5: Muscat de Beaumes-de-Venise ===")
r5 = R("Muscat de Beaumes-de-Venise", "France", "wine",
    designation_type="AOC",
    designation_name="Muscat de Beaumes-de-Venise AOC",
    reputation_tier="respected",
    quality_trajectory="established",
    description="The Southern Rhône's celebrated fortified Muscat (vin doux naturel) — from the Beaumes-de-Venise villages at the foot of the Dentelles de Montmirail, this appellation produces one of France's finest and most complex sweet Muscat wines. The combination of volcanic and limestone soils with the Mistral wind produces a Muscat Blanc à Petits Grains of extraordinary aromatic intensity: orange blossom, apricot, peach, lychee, and honey with refreshing acidity that prevents cloying.",
    key_producers="Domaine de Durban, Château Redortier, Cave des Vignerons, Jaboulet",
    historical_context="Beaumes-de-Venise was one of France's first Muscat appellations (1943) for vin doux naturel; the fortification process (adding grape spirit during fermentation) was introduced by the Church in the medieval period to preserve wine during transport; the appellation's revival in the 1990s was driven by quality estate producers moving away from cooperative production.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Domaine de Durban", "winery", r5, "France",
    production_philosophy="terroir_focused",
    philosophy_description="The leading estate for Muscat de Beaumes-de-Venise — the Leydier family's domaine consistently produces the appellation's most concentrated and complex vin doux naturel from old Muscat Blanc à Petits Grains vines on volcanic and limestone soils beneath the Dentelles de Montmirail.",
    reputation_narrative="The definitive estate for Muscat de Beaumes-de-Venise; consistently cited as the appellation's benchmark producer.",
    price_positioning="mid_range")

prod5b_id = P("Paul Jaboulet Aîné", "winery", r5, "France",
    production_philosophy="traditional",
    philosophy_description="The Hermitage-based négociant-éleveur has produced a celebrated Muscat de Beaumes-de-Venise alongside their famous northern Rhône wines — their Beaumes-de-Venise is one of the most widely distributed and consistently excellent expressions of the appellation.",
    reputation_narrative="One of the Rhône Valley's most important négociant houses; La Chapelle Hermitage and Beaumes-de-Venise are flagship wines.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Domaine de Durban Muscat de Beaumes-de-Venise", "wine_fortified", prod5a_id, r5, "France",
    subcategory="Muscat Blanc à Petits Grains",
    description="The benchmark Muscat de Beaumes-de-Venise — from old Muscat Blanc vines on blue clay and volcanic soils. Intensely aromatic orange blossom, apricot, and peach with great concentration and a mineral freshness from the Dentelles microclimate that distinguishes it from the richer Languedoc Muscats.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Tarte Tatin aux poires with crème fraîche and vanilla", "complement", "classic", "dessert",
         "Caramelised pear tart with chilled Muscat — the wine's orange blossom and apricot mirror the pear's sweetness.")
    PAIR(prod5a, "Roquefort with walnuts and crusty bread", "complement", "classic", "cheese",
         "The great blue cheese and sweet wine pairing — Roquefort's salt and Muscat's sweetness are in eternal harmony.")
    PAIR(prod5a, "Foie gras au torchon with fig compote and brioche", "complement", "established", "starter",
         "Sweet Rhône Muscat with foie gras — the wine's tropical and apricot character bridges the liver's richness.")
    PAIR(prod5a, "Apricot clafoutis with Provençal lavender cream", "complement", "classic", "dessert",
         "Stone-fruit clafoutis from Provence with the Rhône's great stone-fruit Muscat — a perfect regional echo.")

prod5b, new5b = PROD("Jaboulet Muscat de Beaumes-de-Venise", "wine_fortified", prod5b_id, r5, "France",
    subcategory="Muscat Blanc à Petits Grains",
    description="Jaboulet's Beaumes-de-Venise — a consistently excellent vin doux naturel of great aromatic purity, combining lychee, orange blossom, and honey with the Dentelles' mineral freshness. The most widely available benchmark for the appellation's style.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Lemon tart with Italian meringue and lemon sorbet", "contrast", "established", "dessert",
         "Lemon's citrus acidity contrasts with Muscat's sweetness while sharing the citrus vocabulary in a lively contrast.")
    PAIR(prod5b, "Fresh figs with honey, Provençal lavender, and cream", "complement", "classic", "dessert",
         "Provençal fresh figs are the Muscat grape's great seasonal companion — lavender and honey amplify both.")
    PAIR(prod5b, "Gorgonzola Dolce with walnut bread and Bartlett pear", "complement", "classic", "cheese",
         "Soft Italian blue with sweet Muscat — the classic blue cheese and sweet wine pairing with pear as bridge.")
    PAIR(prod5b, "Peach Melba with vanilla ice cream and raspberry coulis", "complement", "established", "dessert",
         "The classic peach dessert with a peach-and-apricot-scented Muscat — both celebrate the stone-fruit season.")

# ── Counts ────────────────────────────────────────────────────────────────────
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
cur.close()
conn.close()
