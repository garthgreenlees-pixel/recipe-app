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

# ── 1. ROERO (Italy) ─────────────────────────────────────────────────────────
print("\n=== Roero (Italy) ===")
r = R("Roero", "Italy", "wine",
      designation_type="DOCG",
      designation_name="Roero DOCG",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="The overlooked twin of Barolo and Barbaresco, Roero sits across the Tanaro River from the Langhe hills on sandy, lighter soils. Home to the Arneis white grape — rescued from near-extinction by Bruno Giacosa and Vietti — and to Nebbiolo-based reds of genuine elegance. Roero Arneis DOCG and Roero DOCG (red) offer Piedmont at more accessible prices with less tannic intensity than Barolo.",
      key_producers="Bruno Giacosa, Matteo Correggia, Malvira, Cascina Ca'Rossa, Cornarea",
      historical_context="Arneis ('little rascal' in Piemontese dialect) was nearly extinct by the 1970s, dismissed as a difficult, low-yield vine. Bruno Giacosa and Vietti revived it in the 1970s-80s, demonstrating its capacity for elegant, food-friendly white wines. The Roero Arneis was awarded DOCG status in 2005, while Roero Nebbiolo red wines have been DOCG since 2004.")

VIN(r, 2023, "excellent", "rising", "Warm Piemonte season; excellent ripeness in Arneis with tropical notes alongside fine Nebbiolo structure")
VIN(r, 2022, "very_good", "rising", "Good vintage; Arneis of unusual freshness and the Nebbiolo reds showed elegant structure")
VIN(r, 2021, "good", "stable", "Cooler year; Arneis with exceptional acid freshness and Nebbiolo built for long aging")
VIN(r, 2020, "very_good", "stable", "Hot, dry summer; concentrated Arneis and deep, powerful Roero reds")
VIN(r, 2019, "excellent", "rising", "Benchmark Piemonte vintage; outstanding Arneis and Roero red of exceptional complexity")

p1 = P("Malvira", "Italy", r, "winery",
        "One of Roero's leading family estates, Malvira has been pivotal in establishing Arneis as a serious white wine. Their Renesio and Trinita single-vineyard Arneis wines are considered the appellation's finest, showcasing the grape's peachy complexity and almond finish at its best.")
prod1, new1 = PROD("Malvira Trinita Roero Arneis DOCG", "wine_still", p1, r, "Italy",
    subcategory="Arneis",
    description="Single-vineyard Roero Arneis from sandy clay soils; fragrant, peachy, and mineral with white blossom, almonds, and a clean, lightly bitter finish — Piedmont's finest expression of the variety",
    price_tier="mid_range")
if new1:
    PAIR(prod1, "Vitello tonnato (cold veal with tuna sauce)", "complement", "classic", "main", "The wine's almond and peach notes are a natural foil for this classic Piemontese summer dish")
    PAIR(prod1, "Risotto al tartufo bianco d'Alba (white truffle risotto)", "complement", "classic", "main", "Fragrant Arneis with its delicate almond note is the traditional Piemontese choice for truffle risotto")
    PAIR(prod1, "Insalata di carne cruda (raw veal salad with lemon)", "complement", "established", "starter", "The wine's freshness and mineral lift complement the clean, lemon-dressed raw veal beautifully")
    PAIR(prod1, "Tajarin pasta with butter and sage", "complement", "established", "main", "Light, fragrant Arneis with its butter and almond notes resonates with Piedmont's egg-yolk pasta in sage butter")

p2 = P("Matteo Correggia", "Italy", r, "winery",
        "The estate that transformed Roero's international reputation for red wine, Matteo Correggia crafted Nebbiolo-based Roero reds of benchmark elegance and aging potential before his untimely death in 2001. The estate continues under his family, producing Roero Riserva wines that show the best of the sandy-soil Nebbiolo character.")
prod2, new2 = PROD("Matteo Correggia Roero Riserva DOCG", "wine_still", p2, r, "Italy",
    subcategory="Nebbiolo",
    description="Reserve Roero Nebbiolo from sandy Roero soils; lighter and more perfumed than Barolo with rose, cherry, dried herbs, and elegant, fine-grained tannins — the benchmark for the appellation",
    price_tier="premium")
if new2:
    PAIR(prod2, "Braised rabbit with Barolo and rosemary", "complement", "classic", "main", "Elegant, perfumed Roero Nebbiolo and braised rabbit is a traditional Piemontese pairing of sublime simplicity")
    PAIR(prod2, "Bollito misto with salsa verde (mixed boiled meats)", "complement", "classic", "main", "Elegant Nebbiolo's acidity and tannin are the classic match for this northern Italian celebration dish")
    PAIR(prod2, "Tajarin with hare ragu", "complement", "established", "main", "Roero's fine Nebbiolo and egg-pasta with rich hare sauce — the quintessential Piemontese combination")
    PAIR(prod2, "Aged Castelmagno cheese with honey and walnuts", "bridge", "established", "cheese", "The wine's rose and cherry lift bridge elegantly with the unique crumbly, spiced Cuneo mountain cheese")

# ── 2. AMYNDEON (Greece) ─────────────────────────────────────────────────────
print("\n=== Amyndeon (Greece) ===")
r2 = R("Amyndeon", "Greece", "wine",
       designation_type="PDO",
       designation_name="PDO Amyndeon",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Greece's highest and coolest wine PDO, in the mountains of western Macedonia near the Albanian border. Xinomavro — Greece's answer to Nebbiolo — achieves remarkable freshness, floral perfume, and aging potential at Amyndeon's altitude. The PDO also produces Greece's most celebrated sparkling wine (Amyndeon brut), making it unique in the country's wine landscape.",
       key_producers="Alpha Estate, Kir-Yianni, Karanika, Tsantali, Domaine Foundi",
       historical_context="Amyndeon's wine history is ancient, but its modern reputation was built by Alpha Estate and Kir-Yianni in the 1990s. The region's altitude (600-800m) and continental mountain climate attracted producers seeking freshness and complexity unavailable in Greece's warmer regions. Alpha Estate's Xinomavro and sparkling Amyndeon wines were among the first Greek wines to achieve consistent international critical acclaim.")

VIN(r2, 2023, "excellent", "rising", "Cool mountain season with exceptional Xinomavro freshness and floral intensity")
VIN(r2, 2022, "very_good", "rising", "Good vintage; elegant, aromatic Xinomavro with fine tannins and aging potential")
VIN(r2, 2021, "good", "stable", "Wet spring but good late summer; wines of freshness and restraint")
VIN(r2, 2020, "very_good", "stable", "Warm mountain summer with good concentration; structured, food-friendly reds")
VIN(r2, 2019, "excellent", "rising", "Benchmark Amyndeon vintage; Xinomavro of rare complexity and cellaring potential")

p3 = P("Alpha Estate", "Greece", r2, "winery",
        "The defining producer of Amyndeon's international reputation, Alpha Estate crafts benchmark Xinomavro and a celebrated sparkling wine from Greece's highest wine-growing zone. Their single-vineyard Xinomavro wines have drawn comparisons with top Nebbiolo, establishing Amyndeon as Greece's most exciting red wine appellation.")
prod3, new3 = PROD("Alpha Estate Xinomavro Amyndeon PDO", "wine_still", p3, r2, "Greece",
    subcategory="Xinomavro",
    description="Benchmark Amyndeon Xinomavro from high-altitude vineyards; rose petal, sun-dried tomato, olive tapenade, and firm tannins with a long, structured finish — Greece's most Barolo-like red wine",
    price_tier="premium")
if new3:
    PAIR(prod3, "Slow-braised lamb with garlic and oregano (arni kleftiko)", "complement", "classic", "main", "The wine's firm tannins and high acidity are a natural match for slow-cooked Greek lamb in the classic tradition")
    PAIR(prod3, "Moussaka with bechamel crust", "complement", "classic", "main", "Structured Xinomavro with its tomato and earthy notes resonates perfectly with rich layered moussaka")
    PAIR(prod3, "Stifado (rabbit or beef stew with pearl onions and cinnamon)", "complement", "established", "main", "The wine's dried-tomato and spice character mirrors the cinnamon-scented slow-cooked Greek stew beautifully")
    PAIR(prod3, "Aged Kefalograviera cheese with fresh figs", "bridge", "suggested", "cheese", "The wine's rose and cherry character bridges elegantly with sharp aged Greek cheese and sweet fresh figs")

p4 = P("Karanika", "Greece", r2, "winery",
        "A boutique Amyndeon estate specialising in traditional method sparkling wine from Xinomavro, Karanika produces some of Greece's finest sparkling wines at altitude. Their Brut Amyndeon demonstrates Xinomavro's unexpected affinity for sparkling wine production, with autolytic complexity and fine, persistent bubbles.")
prod4, new4 = PROD("Karanika Brut Amyndeon PDO", "wine_sparkling", p4, r2, "Greece",
    subcategory="Xinomavro",
    description="Traditional method sparkling Xinomavro from Greece's highest wine zone; delicate salmon colour, fine persistent bubbles, dried rose, cherry, and toasted brioche with a long, bright finish",
    price_tier="premium")
if new4:
    PAIR(prod4, "Fresh oysters with lemon and dill", "complement", "established", "starter", "The sparkling's delicate rose-cherry character and fine bubbles make an elegant match for fresh bivalves")
    PAIR(prod4, "Taramosalata and dolmades mezze spread", "complement", "classic", "starter", "Greek sparkling Xinomavro with its acidity and bubbles cuts through the richness of traditional mezze spreads")
    PAIR(prod4, "Grilled octopus with capers and sea fennel", "complement", "established", "main", "Bright, mineral sparkling resonates with chargrilled octopus in a distinctly Greek coastal combination")
    PAIR(prod4, "Feta and watermelon skewers with mint", "complement", "suggested", "starter", "Delicate rose bubbles and cherry freshness pair naturally with the sweet-salty-herbal play of this Greek summer plate")

# ── 3. THERMENREGION (Austria) ───────────────────────────────────────────────
print("\n=== Thermenregion (Austria) ===")
r3 = R("Thermenregion", "Austria", "wine",
       designation_type="DAC",
       designation_name="Thermenregion DAC",
       reputation_tier="respected",
       quality_trajectory="rediscovering",
       description="Austria's most distinctive wine zone, south of Vienna near the famous spa towns of Baden bei Wien and Bad Vöslau. Home to two grape varieties found almost nowhere else on earth: Zierfandler (Spätrot) and Rotgipfler, which together make a blended white wine of extraordinary richness, spice, and aging potential. Also produces fine Pinot Noir under the name Blauburgunder.",
       key_producers="Weingut Reinisch, Albrecht Schweighofer, Karl Alphart, Weingut Richard Zahel",
       historical_context="The Thermenregion's wines were prized by the Habsburg court, with Gumpoldskirchen (the main village) shipping its Rotgipfler and Zierfandler wines as far as the German royal courts. The region fell into decline post-WWII but is experiencing a careful revival led by quality-focused estates who see the unique variety combination as a genuine competitive advantage on the world stage.")

VIN(r3, 2023, "very_good", "rising", "Warm thermal spa region season; excellent ripeness in both Rotgipfler and Zierfandler")
VIN(r3, 2022, "excellent", "rising", "Outstanding vintage; Rotgipfler-Zierfandler blend of exceptional spice and aging potential")
VIN(r3, 2021, "good", "stable", "Cooler year; wines of unusual freshness and elegance, more aromatic than usual")
VIN(r3, 2020, "very_good", "stable", "Good hot vintage; rich, structured whites and fine Pinot Noir")
VIN(r3, 2019, "excellent", "rising", "Benchmark vintage for the region; finest Rotgipfler-Zierfandler in a generation")

p5 = P("Weingut Reinisch", "Austria", r3, "winery",
        "The leading quality estate of the Thermenregion, Johann Reinisch produces benchmark Rotgipfler, Zierfandler, and their blended Gumpoldskirchner Spiegel — the definitive expression of this unique Austrian wine style. Their Pinot Noir (Blauburgunder) is also considered among the region's finest.")
prod5, new5 = PROD("Weingut Reinisch Gumpoldskirchner Spiegel Thermenregion", "wine_still", p5, r3, "Austria",
    subcategory="Rotgipfler Zierfandler blend",
    description="Benchmark Thermenregion blend of Rotgipfler and Zierfandler; lush, aromatic, and textured with ripe peach, almond, spice, and a distinctive honeyed weight — unlike any other Austrian white wine",
    price_tier="premium")
if new5:
    PAIR(prod5, "Wiener Schnitzel with potato salad and lemon", "complement", "classic", "main", "The regional wine and the national dish: rich, spiced Thermenregion white with veal schnitzel is an Austrian table tradition")
    PAIR(prod5, "Tafelspitz (boiled beef) with horseradish cream and chive sauce", "complement", "classic", "main", "Textured, aromatic Austrian white pairs classically with the gentle richness of Vienna's most iconic boiled beef dish")
    PAIR(prod5, "Fried carp with dill and cucumber salad", "complement", "established", "main", "Weighty, spiced white holds up to the richness of freshwater carp while the wine's acidity provides freshness")
    PAIR(prod5, "Aged Emmentaler with caraway seed bread", "complement", "suggested", "cheese", "The wine's spice and almond notes resonate with the nutty complexity of aged Emmentaler and caraway rye")

p6 = P("Karl Alphart", "Austria", r3, "winery",
        "A smaller artisan estate producing some of the Thermenregion's most age-worthy and complex Rotgipfler and Zierfandler wines. Karl Alphart works with old vines and extended maceration to produce wines of unusual depth and longevity for this underrated Austrian appellation.")
prod6, new6 = PROD("Karl Alphart Rotgipfler Spatlese Thermenregion", "wine_still", p6, r3, "Austria",
    subcategory="Rotgipfler",
    description="Late-harvest Rotgipfler from old vines; off-dry, rich, and complex with beeswax, apricot, spice, and a distinctive mineral saline finish — one of Austria's most characterful and unusual whites",
    price_tier="mid_range")
if new6:
    PAIR(prod6, "Foie gras with brioche and Muskat-Traminer jelly", "complement", "established", "starter", "Off-dry, rich, spiced Rotgipfler and foie gras are a natural combination — the wine's honeyed weight mirrors the duck liver richness")
    PAIR(prod6, "Roasted goose with red cabbage and dumplings (Gansl)", "complement", "classic", "main", "The wine's rich fruit and spice handle the festive richness of roast goose — a traditional Austrian Christmas pairing")
    PAIR(prod6, "Pumpkin cream soup with toasted seeds and creme fraiche", "complement", "established", "starter", "The wine's spiced, honeyed character creates a natural resonance with sweet pumpkin and toasted seed")
    PAIR(prod6, "Apple strudel with Schlagobers cream", "complement", "classic", "dessert", "Off-dry, spiced Austrian white with apple strudel — one of the country's great regional table combinations")

# ── 4. LIRAC (France) ────────────────────────────────────────────────────────
print("\n=== Lirac (France) ===")
r4 = R("Lirac", "France", "wine",
       designation_type="AOC",
       designation_name="Lirac AOC",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="A small, underrated southern Rhone AOC on the Gard side of the river, opposite Chateauneuf-du-Pape. Lirac produces excellent red, white, and rose wines from Grenache, Mourvedre, Syrah, Clairette, and Bourboulenc. Once overshadowed by its famous Tavel neighbour for rose, Lirac is increasingly recognised for its serious, age-worthy reds at prices significantly below Chateauneuf.",
       key_producers="Domaine de la Mordoree, Chateau d'Aqueria, Domaine Maby, Chateau de Bouchassy",
       historical_context="Lirac was awarded AOC status in 1947, one of the first southern Rhone appellations to receive recognition. The region's proximity to Avignon (just 15km) once made it a popular table wine for the Papal court. Today it remains one of the Rhone's best-value appellations, with several top producers making wines that rival Chateauneuf at half the price.")

VIN(r4, 2023, "excellent", "rising", "Hot Rhone season with excellent Grenache ripeness; reds of unusual depth and white wines of surprising freshness")
VIN(r4, 2022, "very_good", "rising", "Very good southern Rhone vintage; reds of structure and fruit with aging potential")
VIN(r4, 2021, "good", "stable", "Cooler year; fine whites and elegant rosés, reds slightly lighter than typical")
VIN(r4, 2020, "excellent", "rising", "Outstanding Rhone vintage; finest Lirac reds in recent memory with exceptional concentration")
VIN(r4, 2019, "very_good", "stable", "Classic vintage with good balance; food-friendly across all colours")

p7 = P("Domaine de la Mordoree", "France", r4, "winery",
        "The benchmark estate of Lirac AOC and also a Tavel producer of the highest quality. Domaine de la Mordoree's Cuvee de la Reine des Bois Lirac is widely considered the appellation's greatest wine — complex, concentrated, and age-worthy in a way that places it firmly in southern Rhone's top tier.")
prod7, new7 = PROD("Domaine de la Mordoree Cuvee Reine des Bois Lirac Rouge", "wine_still", p7, r4, "France",
    subcategory="Grenache Mourvedre Syrah",
    description="Lirac's benchmark red wine; complex, structured blend of Grenache, Mourvedre, and Syrah with garrigue, dark cherry, leather, and a long mineral finish — the appellation's finest expression",
    price_tier="premium")
if new7:
    PAIR(prod7, "Daube de boeuf Provencale with black olives and thyme", "complement", "classic", "main", "The wine's garrigue and dark fruit are inseparable from slow-braised Provencal beef stew — a perfect regional match")
    PAIR(prod7, "Grilled lamb cutlets with herbes de Provence", "complement", "classic", "main", "Southern Rhone red blend and grilled lamb with wild herbs is one of France's great regional pairings")
    PAIR(prod7, "Roasted wild boar with juniper and rosemary", "complement", "established", "main", "Concentrated, structured Lirac has the depth and grip to handle the richness of wild game")
    PAIR(prod7, "Aged Comté with walnut bread and truffle honey", "bridge", "suggested", "cheese", "The wine's earthy complexity and dark fruit bridge naturally with nutty aged mountain cheese and honey")

p8 = P("Chateau d'Aqueria", "France", r4, "winery",
        "A historic Lirac estate with roots in the 17th century, Chateau d'Aqueria produces benchmark Lirac red, white, and an exceptional Tavel rose. Their Lirac red is one of the appellation's most consistent and age-worthy wines, representing exceptional value in the southern Rhone landscape.")
prod8, new8 = PROD("Chateau d'Aqueria Lirac Blanc", "wine_still", p8, r4, "France",
    subcategory="Clairette Grenache Blanc",
    description="Lirac's most celebrated white wine; Clairette and Grenache Blanc blend with fresh pear, white blossom, garrigue, and a mineral, saline finish — one of the southern Rhone's most overlooked white wine treasures",
    price_tier="mid_range")
if new8:
    PAIR(prod8, "Bouillabaisse with rouille and grilled croutons", "complement", "classic", "main", "Mineral, textured southern Rhone white with the Provencal fish stew is the obvious regional pairing")
    PAIR(prod8, "Grilled whole sea bream with fennel and pastis", "complement", "established", "main", "The wine's herbaceous garrigue notes resonate with fennel-scented whole fish and anise liqueur")
    PAIR(prod8, "Tapenade bruschetta with goat's cheese", "complement", "established", "starter", "The wine's saline minerality and white blossom echo tapenade's olive brine and the fresh acidity of goat's cheese")
    PAIR(prod8, "Brandade de morue (whipped salt cod with potato)", "complement", "established", "main", "Textured, mineral southern white with the Languedoc's most iconic salt cod dish — a natural Rhone table pairing")

# ── 5. BINISSALEM-MALLORCA (Spain) ────────────────────────────────────────────
print("\n=== Binissalem-Mallorca (Spain) ===")
r5 = R("Binissalem-Mallorca", "Spain", "wine",
       designation_type="DO",
       designation_name="DO Binissalem-Mallorca",
       reputation_tier="emerging",
       quality_trajectory="ascending",
       description="The Balearic island of Mallorca's leading wine DO, centred in the Raiguer region inland from Palma. Binissalem is defined by indigenous grape varieties unique to the island: Manto Negro and Callet (reds) and Prensal Blanc (white). The Mediterranean island climate produces wines of warmth, generosity, and distinctive local character — increasingly recognised internationally as Spain's most intriguing island wine region.",
       key_producers="Bodega Ribas, Jose L. Ferrer, Vins Nadal, Bodegas Biniagual, Can Majoral",
       historical_context="Mallorca's wine history dates to the Phoenicians, with the Romans expanding viticulture significantly. The island's wine industry collapsed during the phylloxera epidemic and never fully recovered until DO Binissalem was established in 1990 — Spain's first island wine DO. A quality revival in the 2000s-2010s saw international recognition for the island's unique indigenous varieties.")

VIN(r5, 2023, "very_good", "rising", "Warm Mediterranean island season; concentrated Manto Negro with excellent color and dark fruit expression")
VIN(r5, 2022, "excellent", "rising", "Standout vintage for the island; finest Manto Negro and Callet in recent memory")
VIN(r5, 2021, "good", "stable", "Reliable island vintage; approachable, fruit-forward style with the typical Mediterranean warmth")
VIN(r5, 2020, "very_good", "stable", "Hot, dry Mediterranean summer; concentrated, generous reds and fresh island whites")
VIN(r5, 2019, "very_good", "stable", "Classic island vintage with balanced ripeness and characteristic warmth across all varietals")

p9 = P("Bodega Ribas", "Spain", r5, "winery",
        "Mallorca's most prestigious wine estate, Bodega Ribas has been producing wine since 1711 — making it one of Spain's oldest continuously operating wineries. Their Sio and Ribas de Cabrera wines are acclaimed internationally, blending indigenous varieties with international grapes in limited-production bottlings that represent the pinnacle of Mallorcan wine.")
prod9, new9 = PROD("Bodega Ribas Sio Binissalem-Mallorca DO", "wine_still", p9, r5, "Spain",
    subcategory="Manto Negro",
    description="Mallorca's benchmark indigenous Manto Negro; dark cherry, dried fig, warm Mediterranean spice, and smooth tannins with an island character unlike any other Spanish wine",
    price_tier="premium")
if new9:
    PAIR(prod9, "Slow-roasted Mallorcan suckling pig porcella", "complement", "classic", "main", "The island's most iconic dish paired with its most celebrated red wine — a Mallorcan feast combination")
    PAIR(prod9, "Lamb shoulder sobrasada rice (arros brut)", "complement", "classic", "main", "The wine's warm spice and dark fruit resonate with the island's traditional rice dish with cured sausage")
    PAIR(prod9, "Tumbet (Mallorcan ratatouille with potato and eggplant)", "complement", "established", "main", "Mediterranean-warm Manto Negro and the island's signature vegetable dish are a natural combination")
    PAIR(prod9, "Aged Mahon cheese with fig preserves", "bridge", "established", "cheese", "Warm, dark-fruited island red bridges with the sharp, salty aged cheese of the Balearics")

p10 = P("Jose Luis Ferrer", "Spain", r5, "winery",
         "The most widely distributed and historically important producer of Binissalem-Mallorca DO, Jose Luis Ferrer was instrumental in establishing the DO and building awareness of Mallorcan wine internationally. Their accessible Veritas Manto Negro and Gran Coleccion are the island's most recognisable wine labels.")
prod10, new10 = PROD("Jose Luis Ferrer Veritas Manto Negro Binissalem DO", "wine_still", p10, r5, "Spain",
    subcategory="Manto Negro",
    description="Approachable estate Manto Negro; cherry, plum, and Mediterranean herbs with soft tannins and good freshness — the most widely known Mallorcan red wine",
    price_tier="mid_range")
if new10:
    PAIR(prod10, "Pa amb oli with tomato and Mallorcan olive oil", "complement", "classic", "starter", "The island's simplest and most beloved dish paired with its most familiar red wine — pure Mallorcan table culture")
    PAIR(prod10, "Grilled bream with capers and fresh herbs", "complement", "established", "main", "Soft, cherry-fruited Manto Negro handles delicate Mediterranean fish with its warm, approachable character")
    PAIR(prod10, "Sobrasada on toasted bread with honey", "complement", "classic", "starter", "The island's signature spiced red pork sausage spread and its local red wine is one of Spain's most distinctive regional pairings")
    PAIR(prod10, "Cocarroi pastries with Swiss chard and pine nuts", "complement", "established", "starter", "The wine's gentle warmth and herb notes resonate with the island's traditional stuffed pastry")

# ── COUNTS ───────────────────────────────────────────────────────────────────
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
conn.close()
