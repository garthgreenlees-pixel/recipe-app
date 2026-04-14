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
    print(f"  Region inserted: {name} ({rid})")
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
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B121 ─────────────────────────────────────────────────────────────────────
# Targets: Naoussa PDO (Greece), Muscat of Samos PDO (Greece),
#          Mantinia PDO (Greece), Bairrada DOC (Portugal), Kamptal DAC (Austria)

# 1. NAOUSSA PDO — Greece
print("=== Naoussa PDO ===")
r1 = R("Naoussa PDO", "Greece", "wine",
        designation_type="PDO",
        designation_name="Naoussa PDO",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Macedonia's most prestigious red wine appellation, south-west of Thessaloniki on the slopes of Mount Vermio. Exclusively Xinomavro grape, producing wines of extraordinary structure, high acidity, firm tannins and complex aromatics of tomato, olive, dried rose and spice. Greece's answer to Barolo; requires extended ageing to reveal its true potential.",
        key_producers="Thymiopoulos, Kir-Yianni, Boutari, Alpha Estate, Dalamara",
        historical_context="Naoussa received Greece's first appellation of origin in 1971. The Boutari family pioneered the region's quality revival in the 1970s. Apostolos Thymiopoulos established the modern benchmark in the 2000s, farming organically on old ungrafted vines.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","rising"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r1, yr, qd, pt, f"Naoussa {yr}: Vermio Mountain harvest; Xinomavro retains superb structure")

p1a = P("Thymiopoulos Vineyards", "winery", r1, "Greece",
        production_philosophy="organic",
        philosophy_description="Apostolos Thymiopoulos farms old ungrafted vines organically; single-parcel Xinomavro of extraordinary precision.",
        reputation_narrative="The defining voice of modern Naoussa; Uranos bottling from 90-year-old ungrafted vines is Greece's most sought-after red.",
        price_positioning="premium")
pr1a1, n = PROD("Thymiopoulos Naoussa Uranos Xinomavro", "wine_still", p1a, r1, "Greece",
                subcategory="Xinomavro", price_tier="premium",
                description="From 90-year-old ungrafted vines on clay-limestone; extraordinary structure with dried rose, tomato, tar and spice.")
if n:
    PAIR(pr1a1, "Braised lamb with tomato and herbs", "complement", "classic", "main", "Xinomavro's tomato-herb character mirrors the braised lamb sauce perfectly")
    PAIR(pr1a1, "Pastitsio (Greek pasta bake)", "complement", "established", "main", "Structured Naoussa cuts through the béchamel richness of pastitsio")
    PAIR(pr1a1, "Aged kefalograviera cheese", "complement", "established", "cheese", "Firm mountain cheese finds harmony with Xinomavro's structured tannins")
    PAIR(pr1a1, "Wild boar stew with juniper", "complement", "established", "main", "Game meat and juniper spice echo the wild, earthy dimension of old-vine Xinomavro")

pr1a2, n = PROD("Thymiopoulos Naoussa Earth and Sky", "wine_still", p1a, r1, "Greece",
                subcategory="Xinomavro", price_tier="mid_range",
                description="Entry Thymiopoulos Naoussa; fresh Xinomavro with vivid acidity, dried cherry and a savoury mineral edge.")
if n:
    PAIR(pr1a2, "Moussaka with beef", "complement", "classic", "main", "Naoussa Xinomavro is the classic companion to Greece's iconic meat dish")
    PAIR(pr1a2, "Slow-cooked lamb chops", "complement", "established", "main", "Bright acidity and firm tannins cut through rich slow-cooked lamb")
    PAIR(pr1a2, "Spanakopita with feta", "complement", "established", "starter", "Savoury-mineral Xinomavro pairs naturally with spinach-feta pastry")
    PAIR(pr1a2, "Grilled halloumi", "complement", "suggested", "starter", "Tart acidity and dried-fruit cut through the saltiness of grilled halloumi")

p1b = P("Kir-Yianni", "winery", r1, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Yiannis Boutari's estate; Diaporos single-vineyard and Ramnista are benchmark Naoussa references.",
        reputation_narrative="Kir-Yianni established by Yiannis Boutari in 1997 after leaving the family Boutari firm; Ramnista is one of Naoussa's most age-worthy reds.",
        price_positioning="premium")
pr1b1, n = PROD("Kir-Yianni Ramnista Naoussa", "wine_still", p1b, r1, "Greece",
                subcategory="Xinomavro", price_tier="premium",
                description="Ramnista single-vineyard Naoussa; deeply structured with black cherry, tobacco, olive and fine-grained tannins.")
if n:
    PAIR(pr1b1, "Rack of lamb with dried herbs", "complement", "classic", "main", "Xinomavro's structured frame elevates herb-roasted rack of lamb perfectly")
    PAIR(pr1b1, "Stifado (cinnamon beef stew)", "complement", "established", "main", "The wine's spice complexity mirrors the cinnamon-clove depth of stifado")
    PAIR(pr1b1, "Aged kasseri cheese", "complement", "established", "cheese", "Semi-hard Greek cheese complements Ramnista's tannic texture")
    PAIR(pr1b1, "Beef with orzo (giouvetsi)", "complement", "classic", "main", "Naoussa's natural companion to the classic Greek baked beef-and-pasta dish")

pr1b2, n = PROD("Kir-Yianni Paranga Red", "wine_still", p1b, r1, "Greece",
                subcategory="Xinomavro-Merlot-Syrah", price_tier="mid_range",
                description="Everyday blend led by Xinomavro; approachable with red fruits, moderate tannins and a savory finish.")
if n:
    PAIR(pr1b2, "Pork souvlaki with tzatziki", "complement", "established", "main", "Fruit-forward blend complements grilled pork without overpowering")
    PAIR(pr1b2, "Grilled chicken with lemon-oregano marinade", "complement", "established", "main", "Xinomavro's acidity lifts the herb-lemon profile of roasted chicken")
    PAIR(pr1b2, "Pita gyros with tomato and onion", "complement", "classic", "main", "Approachable red matches the casual Greek street-food classic")
    PAIR(pr1b2, "Pizza with feta and olives", "complement", "suggested", "main", "Mediterranean toppings complement the savory fruit of this everyday blend")

# 2. MUSCAT OF SAMOS PDO — Greece
print("=== Muscat of Samos PDO ===")
r2 = R("Muscat of Samos PDO", "Greece", "wine",
        designation_type="PDO",
        designation_name="Muscat of Samos PDO",
        reputation_tier="respected",
        quality_trajectory="established",
        description="The Aegean island of Samos produces Greece's finest dessert Muscat wines from Muscat Blanc à Petits Grains. Vinified in several styles including Anthemis (naturally sweet), Nectar (sun-dried late harvest) and Vin Doux (fortified). High-altitude vineyards on steep terraced slopes capture cooling sea breezes while concentrating aromatics. France has long been the primary export market.",
        key_producers="Samos Union of Wine Producing Cooperatives, Kourtaki",
        historical_context="Samos Muscat has been produced since antiquity; the cooperative system established in 1934 united island growers. Napoleon reportedly enjoyed Samos wine. The island's cooperative is one of Greece's most important wine institutions.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","stable"),(2022,"very_good","stable")]:
    VIN(r2, yr, qd, pt, f"Samos {yr}: Aegean island harvest; concentrated Muscat aromatics from terraced vineyards")

p2a = P("Samos Union of Wine Cooperatives", "winery", r2, "Greece",
        production_philosophy="traditional",
        philosophy_description="The island cooperative uniting all Samos growers; benchmark Anthemis and Nectar Muscat.",
        reputation_narrative="The Samos cooperative is the sole producer of PDO Muscat of Samos; exporter of record to France and Europe.",
        price_positioning="mid_range")
pr2a1, n = PROD("Samos Nectar", "wine_dessert", p2a, r2, "Greece",
                subcategory="Muscat Blanc à Petits Grains", price_tier="premium",
                description="Sun-dried Muscat Nectar; extraordinary concentration of apricot jam, orange blossom, honey and warm spice.")
if n:
    PAIR(pr2a1, "Baklava with honey and pistachio", "complement", "classic", "dessert", "The island Muscat finds its natural companion in honey-drenched baklava")
    PAIR(pr2a1, "Melomakarona (honey spiced cookies)", "complement", "classic", "dessert", "Orange-blossom sweetness in both Muscat and the traditional Greek cookies")
    PAIR(pr2a1, "Roquefort or Stilton blue cheese", "contrast", "classic", "cheese", "Concentrated sweetness of Nectar cuts powerfully through pungent blue cheese")
    PAIR(pr2a1, "Fresh figs with clotted cream", "complement", "established", "dessert", "Sun-dried Muscat amplifies fresh fig's natural caramel sweetness")

pr2a2, n = PROD("Samos Anthemis", "wine_dessert", p2a, r2, "Greece",
                subcategory="Muscat Blanc à Petits Grains", price_tier="mid_range",
                description="Naturally sweet Samos Muscat; lychee, peach blossom, apricot and a fresh finish — lighter than Nectar.")
if n:
    PAIR(pr2a2, "Fresh fruit tart with pastry cream", "complement", "established", "dessert", "Floral Muscat complements the creamy sweetness of a classic fruit tart")
    PAIR(pr2a2, "Galaktoboureko (semolina custard pastry)", "complement", "classic", "dessert", "The island Muscat is the natural companion to creamy Greek custard pastry")
    PAIR(pr2a2, "Loukoumades (honey doughnuts)", "complement", "classic", "dessert", "Traditional Greek honey doughnuts meet their natural Muscat companion")
    PAIR(pr2a2, "Crème brûlée", "complement", "established", "dessert", "Floral freshness of Anthemis lifts the caramel-cream richness of crème brûlée")

p2b = P("Kourtaki Winery", "winery", r2, "Greece",
        production_philosophy="traditional",
        philosophy_description="Major Greek négociant; benchmark affordable Muscat of Samos for everyday enjoyment.",
        reputation_narrative="Kourtaki is the most widely distributed Greek wine brand; their Samos Muscat introduced the world to Greek dessert wine.",
        price_positioning="value")
pr2b1, n = PROD("Kourtaki Muscat of Samos", "wine_dessert", p2b, r2, "Greece",
                subcategory="Muscat Blanc à Petits Grains", price_tier="value",
                description="Classic everyday Samos Muscat; peach, apricot and orange blossom with a clean, refreshing sweetness.")
if n:
    PAIR(pr2b1, "Greek yoghurt with honey and walnuts", "complement", "classic", "dessert", "Muscat's floral sweetness amplifies honey-drizzled yoghurt")
    PAIR(pr2b1, "Almond cake (amygdalota)", "complement", "classic", "dessert", "The wine's almond-blossom fragrance echoes the almond cake")
    PAIR(pr2b1, "Peach tarte tatin", "complement", "established", "dessert", "Peach-scented Muscat mirrors and amplifies the caramelised fruit of the tart")
    PAIR(pr2b1, "Vanilla panna cotta", "complement", "established", "dessert", "Floral freshness of Samos Muscat lifts the cream-vanilla simplicity of panna cotta")

pr2b2, n = PROD("Kourtaki Samos Grand Cru", "wine_dessert", p2b, r2, "Greece",
                subcategory="Muscat Blanc à Petits Grains", price_tier="mid_range",
                description="Grand Cru selection from highest-altitude terraces; more concentrated and complex than the standard cuvée.")
if n:
    PAIR(pr2b2, "Pain d'épices with foie gras", "complement", "established", "starter", "Concentrated floral sweetness bridges spiced gingerbread and rich foie gras")
    PAIR(pr2b2, "Tarte aux fruits exotiques", "complement", "established", "dessert", "Tropical fruit concentration mirrors exotic fruit tart flavours")
    PAIR(pr2b2, "Mimolette or aged Gouda", "complement", "suggested", "cheese", "Caramel sweetness of aged cheese echoes the honeyed Muscat")
    PAIR(pr2b2, "Apricot and almond tart", "complement", "classic", "dessert", "Apricot-driven Muscat is the natural pairing for apricot-almond pastry")

# 3. MANTINIA PDO — Greece
print("=== Mantinia PDO ===")
r3 = R("Mantinia PDO", "Greece", "wine",
        designation_type="PDO",
        designation_name="Mantinia PDO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="High-altitude plateau appellation in the central Peloponnese at 600–650m, dedicated to the rare Moschofilero grape. Pale pink-skinned and intensely aromatic, Moschofilero produces crisp, floral, spicy whites with natural freshness from the elevation. Often compared to Pinot Grigio in body but with far more exotic perfume. Also produces rosé from the same grape.",
        key_producers="Tselepos, Spiropoulos, Domaine Skouras",
        historical_context="Mantinia was established as PDO in 1971, recognising the ancient wine culture of the Arcadian plateau. The plateau's altitude gives Greece's warmest lowland regions a cool-climate equivalent, preserving Moschofilero's natural perfume and acidity.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","stable"),(2022,"very_good","stable")]:
    VIN(r3, yr, qd, pt, f"Mantinia {yr}: Arcadian plateau harvest; high altitude preserves Moschofilero freshness")

p3a = P("Tselepos Estate", "winery", r3, "Greece",
        production_philosophy="terroir_driven",
        philosophy_description="Reference Mantinia producer; Amalia Moschofilero is the benchmark for the appellation's floral potential.",
        reputation_narrative="Yiannis Tselepos established the modern benchmark for Mantinia; also produces excellent Xinomavro from Naoussa.",
        price_positioning="premium")
pr3a1, n = PROD("Tselepos Amalia Moschofilero", "wine_still", p3a, r3, "Greece",
                subcategory="Moschofilero", price_tier="premium",
                description="Benchmark Mantinia Moschofilero; rose petal, spice, citrus zest and a nervy, refreshing finish.")
if n:
    PAIR(pr3a1, "Grilled prawns with garlic and lemon", "complement", "classic", "main", "Floral-citrus Moschofilero lifts grilled prawns with aromatic precision")
    PAIR(pr3a1, "Greek village salad (horiatiki)", "complement", "classic", "starter", "Moschofilero's refreshing acidity makes it the perfect taverna white")
    PAIR(pr3a1, "Spanakopita with lemon zest", "complement", "established", "starter", "Floral white complements the herb-and-feta savouriness of spinach pie")
    PAIR(pr3a1, "Lemon sole in butter", "complement", "established", "main", "Delicate floral wine lifts butter-basted sole without overwhelming it")

pr3a2, n = PROD("Tselepos Mantinia Moschofilero", "wine_still", p3a, r3, "Greece",
                subcategory="Moschofilero", price_tier="mid_range",
                description="Entry Tselepos Mantinia; bright peach blossom and rose water with crisp citrus and a clean finish.")
if n:
    PAIR(pr3a2, "Taramasalata with crudités", "complement", "established", "starter", "Citrus-fresh Moschofilero cleanses the palate between bites of briny roe dip")
    PAIR(pr3a2, "Mezze of dolmades and tzatziki", "complement", "classic", "starter", "Floral Arcadian white is the natural aperitif for a Greek meze spread")
    PAIR(pr3a2, "Lemon-herb baked chicken", "complement", "established", "main", "Aromatic white mirrors the lemon-herb of a simple baked chicken")
    PAIR(pr3a2, "Grilled sea bass fillet", "complement", "established", "main", "Lightweight Moschofilero lifts delicate fish without competing")

p3b = P("Spiropoulos Winery", "winery", r3, "Greece",
        production_philosophy="organic",
        philosophy_description="Organic Peloponnese estate; certified Mantinia Moschofilero and Nemea Agiorgitiko.",
        reputation_narrative="Nikos Spiropoulos converted to organic farming in the early 2000s; one of the region's most committed quality producers.",
        price_positioning="mid_range")
pr3b1, n = PROD("Spiropoulos Mantinia White", "wine_still", p3b, r3, "Greece",
                subcategory="Moschofilero", price_tier="mid_range",
                description="Organic Mantinia Moschofilero; crisp, floral and mineral with a clean tangerine and white flower character.")
if n:
    PAIR(pr3b1, "Zucchini fritters with yoghurt dip", "complement", "established", "starter", "Crisp floral white complements herb-scented vegetable fritters")
    PAIR(pr3b1, "Grilled sardines with lemon", "complement", "established", "starter", "Citrus-driven white cuts through oily sardines with refreshing lift")
    PAIR(pr3b1, "White bean salad with olive oil", "complement", "established", "starter", "Mineral white complements the simple, clean flavours of a bean salad")
    PAIR(pr3b1, "Linguine with clams and white wine", "complement", "classic", "main", "The wine's citrus-mineral profile is naturally suited to clam pasta")

pr3b2, n = PROD("Spiropoulos Orinos Ilios Red", "wine_still", p3b, r3, "Greece",
                subcategory="Agiorgitiko", price_tier="mid_range",
                description="Organic Peloponnese red from Agiorgitiko; ripe cherry and spice with smooth tannins and Mediterranean warmth.")
if n:
    PAIR(pr3b2, "Roast chicken with herbs", "complement", "established", "main", "Soft-tannin Agiorgitiko complements roast chicken across the herb spectrum")
    PAIR(pr3b2, "Grilled lamb burgers with tzatziki", "complement", "classic", "main", "Greek lamb and Peloponnese red are natural companions at any table")
    PAIR(pr3b2, "Aubergine stuffed with meat (papoutsakia)", "complement", "classic", "main", "Rich stuffed aubergine finds balance in fruit-forward Agiorgitiko")
    PAIR(pr3b2, "Hard cheese and cured meats board", "complement", "established", "starter", "Versatile Peloponnese red works across an antipasto-style board")

# 4. BAIRRADA DOC — Portugal
print("=== Bairrada DOC ===")
r4 = R("Bairrada DOC", "Portugal", "wine",
        designation_type="DOC",
        designation_name="Bairrada DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Atlantic-influenced appellation on heavy clay soils between Coimbra and Aveiro. The Baga grape dominates — producing high-acid, high-tannin reds of extraordinary ageing potential when made by masters. The region also produces Portugal's finest traditional-method sparkling wine. Baga's demanding nature rewards patience; great vintages develop for decades. Maria Gomes (Fernão Pires) provides fresh, aromatic whites.",
        key_producers="Luís Pato, Quinta das Bágeiras, Filipa Pato, Caves São João",
        historical_context="Bairrada's roasted suckling pig (leitão à Bairrada) is deeply entwined with the region's wine identity. Baga was long considered too harsh for modern tastes until producers like Luís Pato demonstrated its greatness. Received DOC status 1981.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r4, yr, qd, pt, f"Bairrada {yr}: Atlantic clay soils; Baga structure enhanced by the season")

p4a = P("Luís Pato", "winery", r4, "Portugal",
        production_philosophy="terroir_driven",
        philosophy_description="The master of Baga; estate and old-vine single-parcel bottlings redefined Bairrada's reputation internationally.",
        reputation_narrative="Luís Pato is Portugal's most important ambassador for Baga; his old-vine 'Vinho Branco de Baga' rewrote the region's history.",
        price_positioning="premium")
pr4a1, n = PROD("Luís Pato Quinta do Ribeirinho Pé Franco Baga", "wine_still", p4a, r4, "Portugal",
                subcategory="Baga", price_tier="ultra_premium",
                description="Pre-phylloxera ungrafted Baga; extraordinary depth with black cherry, iron, mineral and tannic architecture.")
if n:
    PAIR(pr4a1, "Roasted suckling pig (leitão)", "complement", "classic", "main", "The definitive Bairrada pairing — Baga's tannins cut through crackling-rich suckling pig")
    PAIR(pr4a1, "Aged Serra da Estrela cheese", "complement", "established", "cheese", "Portugal's great mountain cheese matches the mineral intensity of old-vine Baga")
    PAIR(pr4a1, "Slow-braised wild boar", "complement", "established", "main", "Ungrafted Baga's iron-mineral depth is the natural companion for rich game")
    PAIR(pr4a1, "Chouriço assado with crusty bread", "complement", "established", "starter", "Smoky Portuguese sausage finds its natural regional wine partner")

pr4a2, n = PROD("Luís Pato Baga Vinhas Velhas", "wine_still", p4a, r4, "Portugal",
                subcategory="Baga", price_tier="premium",
                description="Old-vine Baga from Luís Pato's prime parcels; structured and age-worthy with violet, black fruit and mineral backbone.")
if n:
    PAIR(pr4a2, "Roast duck with orange and port", "complement", "established", "main", "Baga's high acidity cuts through duck fat while fruit echoes the orange")
    PAIR(pr4a2, "Grilled chouriço and black pudding", "complement", "classic", "main", "Smoked pork products are the classic table companion to Atlantic-coast Baga")
    PAIR(pr4a2, "Slow-roasted shoulder of lamb", "complement", "established", "main", "Old-vine Baga structure frames slowly-roasted lamb to perfection")
    PAIR(pr4a2, "Açorda (bread and coriander soup)", "complement", "suggested", "main", "Bairrada's rustic bread-and-coriander soup finds its regional wine companion")

p4b = P("Quinta das Bágeiras", "winery", r4, "Portugal",
        production_philosophy="terroir_driven",
        philosophy_description="Traditional Bairrada estate; single-estate Baga and sparkling Bairrada from estate clay vineyards.",
        reputation_narrative="Mário Sergio Nuno's estate; Garrafeira and Grande Reserva Baga demonstrate the region's long ageing potential.",
        price_positioning="premium")
pr4b1, n = PROD("Quinta das Bágeiras Garrafeira Baga", "wine_still", p4b, r4, "Portugal",
                subcategory="Baga", price_tier="premium",
                description="Traditional Garrafeira Baga aged in old oak; savoury, mineral and complex with dried flowers and iron mineral character.")
if n:
    PAIR(pr4b1, "Bacalhau à Brás (salt cod and eggs)", "complement", "established", "main", "Atlantic Baga's mineral acidity is the perfect foil for Portugal's salt cod dish")
    PAIR(pr4b1, "Roast pork loin with garlic", "complement", "classic", "main", "Traditional Bairrada pork matches complement Garrafeira Baga's rustic depth")
    PAIR(pr4b1, "Queijo da Serra (aged sheep's cheese)", "complement", "established", "cheese", "Atlantic Portugal's great aged sheep's cheese pairs naturally with mineral Baga")
    PAIR(pr4b1, "Alheira (bread sausage) with greens", "complement", "classic", "main", "The traditional Portuguese sausage of the north finds regional Bairrada harmony")

pr4b2, n = PROD("Quinta das Bágeiras Bairrada Espumante Bruto", "wine_sparkling", p4b, r4, "Portugal",
                subcategory="Bairrada Espumante", price_tier="premium",
                description="Traditional-method Bairrada sparkling from Bical and Maria Gomes; crisp, yeasty and refreshing with fine persistent bubbles.")
if n:
    PAIR(pr4b2, "Roasted suckling pig skin (torresmos)", "complement", "classic", "main", "Bairrada sparkling is the local tradition with crispy pork crackling")
    PAIR(pr4b2, "Caldeirada (fish stew)", "complement", "established", "main", "Traditional sparkling cleanses each bite of rich Atlantic fish stew")
    PAIR(pr4b2, "Ovos moles de Aveiro (egg yolk sweets)", "complement", "classic", "dessert", "The regional egg sweet finds its natural sparkling companion")
    PAIR(pr4b2, "Fried bacalhau (salt cod fritters)", "cleanse", "established", "starter", "Sparkling acidity cleanses the richness of fried salt cod perfectly")

# 5. KAMPTAL DAC — Austria
print("=== Kamptal DAC ===")
r5 = R("Kamptal DAC", "Austria", "wine",
        designation_type="DAC",
        designation_name="Kamptal DAC",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The Kamp river valley north-west of Vienna produces Austria's most exciting Grüner Veltliner and Riesling. The unique Heiligenstein and Gaisberg single-vineyard sites on volcanic gneiss and sandstone soils produce benchmark wines of extraordinary mineral precision and longevity. The DAC hierarchy (Klassik, Reserve, Erste Lage) mirrors Burgundy's premier and grand cru system.",
        key_producers="Bründlmayer, Hirsch, Schloss Gobelsburg, Loimer, Allram",
        historical_context="Kamptal was established as one of Austria's first DAC appellations in 2008. The Kamptal Erste Lage classification formalised single-vineyard hierarchy. Willi Bründlmayer's estate is the region's flagship and has driven international recognition since the 1980s.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r5, yr, qd, pt, f"Kamptal {yr}: Kamp Valley continental season; Grüner Veltliner shows superb mineral precision")

p5a = P("Bründlmayer", "winery", r5, "Austria",
        production_philosophy="terroir_driven",
        philosophy_description="The flagship Kamptal estate; Heiligenstein and Gaisberg Riesling; old-vine Grüner Veltliner Lamm is an Austrian icon.",
        reputation_narrative="Willi Bründlmayer's estate is the benchmark for Austrian Riesling and Grüner Veltliner; internationally the most celebrated Kamptal producer.",
        price_positioning="premium")
pr5a1, n = PROD("Bründlmayer Heiligenstein Alte Reben Riesling", "wine_still", p5a, r5, "Austria",
                subcategory="Riesling", price_tier="ultra_premium",
                description="Alte Reben (old vine) Riesling from the volcanic Heiligenstein site; electrifying mineral precision with stone fruit and slate.")
if n:
    PAIR(pr5a1, "Steamed Danube crayfish", "complement", "classic", "main", "Austrians pair fine Kamptal Riesling with freshwater crayfish as a tradition")
    PAIR(pr5a1, "Wiener Schnitzel with lemon", "complement", "classic", "main", "Austria's national dish finds its finest companion in Heiligenstein Riesling")
    PAIR(pr5a1, "Cured trout with horseradish cream", "complement", "classic", "starter", "Riesling's acidity and mineral notes echo cured trout's delicate brine")
    PAIR(pr5a1, "Leek and potato gratin", "complement", "established", "main", "Old vine mineral precision cuts through potato-cream richness beautifully")

pr5a2, n = PROD("Bründlmayer Grüner Veltliner Lamm", "wine_still", p5a, r5, "Austria",
                subcategory="Grüner Veltliner", price_tier="ultra_premium",
                description="Lamm single-vineyard Grüner Veltliner; the Austrian benchmark — white pepper, mineral, pear and extraordinary longevity.")
if n:
    PAIR(pr5a2, "Tafelspitz (boiled beef with horseradish)", "complement", "classic", "main", "The ultimate Austrian wine-and-food pairing; Grüner Veltliner and Tafelspitz are inseparable")
    PAIR(pr5a2, "White asparagus with hollandaise", "complement", "classic", "main", "Grüner Veltliner's pepper-mineral suits white asparagus better than almost any wine")
    PAIR(pr5a2, "Zander (pike-perch) with butter sauce", "complement", "classic", "main", "Austrian freshwater fish with Kamptal white is the definitive regional tradition")
    PAIR(pr5a2, "Erdäpfelsalat (potato salad with vinegar)", "complement", "classic", "starter", "Acidity-driven Grüner mirrors the vinegar dressing of classic Austrian potato salad")

p5b = P("Schloss Gobelsburg", "winery", r5, "Austria",
        production_philosophy="traditional",
        philosophy_description="Historic monastic estate; Cistercian wine tradition dating to 1171; benchmark single-vineyard Kamptal whites.",
        reputation_narrative="Michael Moosbrugger revived Gobelsburg from 1996; now one of Austria's most acclaimed estates with ancient cellar tradition.",
        price_positioning="premium")
pr5b1, n = PROD("Schloss Gobelsburg Grüner Veltliner Renner", "wine_still", p5b, r5, "Austria",
                subcategory="Grüner Veltliner", price_tier="premium",
                description="Renner single-vineyard Grüner Veltliner; classic white pepper, mineral and citrus with firm acidity and elegant structure.")
if n:
    PAIR(pr5b1, "Veal escalope with lemon and capers", "complement", "classic", "main", "White pepper Grüner mirrors the acidic-mineral notes of veal piccata")
    PAIR(pr5b1, "Sushi and sashimi", "complement", "established", "main", "Austrian winemakers have championed Grüner as a versatile sushi companion")
    PAIR(pr5b1, "Butternut squash soup with cream", "complement", "established", "starter", "Mineral and pepper Grüner cuts through the velvet sweetness of squash soup")
    PAIR(pr5b1, "Grilled trout with almonds", "complement", "established", "main", "A classic Alpine combination: fresh trout and mineral Kamptal white")

pr5b2, n = PROD("Schloss Gobelsburg Riesling Steinsetz", "wine_still", p5b, r5, "Austria",
                subcategory="Riesling", price_tier="premium",
                description="Steinsetz Riesling from Kamptal's primary sandy gneiss soils; fine mineral with grapefruit, apricot and focused acidity.")
if n:
    PAIR(pr5b2, "Smoked salmon with cream cheese on rye", "complement", "classic", "starter", "Riesling's citrus-mineral cuts through the richness of smoked salmon")
    PAIR(pr5b2, "Pad Thai with prawns", "complement", "established", "main", "Austrian Riesling's mineral-acidity is the classic pairing for Thai noodle dishes")
    PAIR(pr5b2, "Vietnamese spring rolls with nuoc cham", "complement", "suggested", "starter", "Citrus-driven Riesling complements the herbaceous freshness of spring rolls")
    PAIR(pr5b2, "Duck confit with braised red cabbage", "complement", "established", "main", "Kamptal Riesling's acidity cuts through duck richness with mineral precision")

# Final counts
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")

cur.close()
conn.close()
print("B121 complete.")
