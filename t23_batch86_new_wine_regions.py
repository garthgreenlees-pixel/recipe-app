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

# ── Region 1: Piedmont — Barbaresco ─────────────────────────────────────────
print("\n=== Region 1: Barbaresco ===")
r1 = R("Barbaresco", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Barbaresco DOCG",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Nebbiolo's most elegant expression — a small DOCG of 800 hectares on the right bank of the Tanaro River producing wines of extraordinary finesse and complexity. Barbaresco is often counterposed with Barolo: both made from Nebbiolo, but Barbaresco's calcareous Tortonian marl soils and slightly warmer microclimate produce wines that open earlier and show greater floral delicacy. The finest sites — Asili, Rabajà, Martinenga, Gallina — produce wines of world-class complexity.",
    key_producers="Gaja, Bruno Giacosa, Produttori del Barbaresco, Roagna, Sottimano",
    historical_context="Barbaresco's independence from Barolo was championed by Domizio Cavazza in 1894; Angelo Gaja's innovations in the 1960s-80s transformed international perceptions of Italian wine entirely.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2018, "excellent", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Gaja", "winery", r1, "Italy",
    production_philosophy="terroir_focused",
    philosophy_description="Angelo Gaja is Italy's most influential winemaker — his single-vineyard Sorì San Lorenzo, Sorì Tildìn, and Costa Russi Barbaresco wines transformed global perceptions of Italian wine in the 1970s-80s. Gaja introduced Burgundian barrel aging and single-vineyard bottlings to Piedmont.",
    reputation_narrative="The most famous Italian winemaker; Gaja's name is synonymous with Piedmontese quality at the highest level.",
    price_positioning="ultra_premium")

prod1b_id = P("Produttori del Barbaresco", "winery", r1, "Italy",
    production_philosophy="traditional",
    philosophy_description="The cooperative that defined traditional Barbaresco — large old Slavonian oak botti, minimal intervention, site-specific crus released only in exceptional vintages. The cooperative's Riservas from Asili, Rabajà, and Pora are benchmarks of Nebbiolo's traditional expression.",
    reputation_narrative="The definitive traditional Barbaresco producer; Riserva single-cru releases are among Italy's most important wines.",
    price_positioning="premium")

prod1a, new1a = PROD("Gaja Sorì San Lorenzo Barbaresco", "wine_still", prod1a_id, r1, "Italy",
    subcategory="Nebbiolo",
    description="Gaja's most celebrated single-vineyard Barbaresco — from the Sorì San Lorenzo plot in Neive, this wine helped establish Italy's reputation for world-class fine wine in the 1970s. Silky, complex, and hauntingly mineral with extraordinary longevity.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "White truffle tagliolini with butter and Parmigiano", "elevate", "classic", "main",
         "Alba's greatest luxury — white truffle pasta with Piedmont's greatest wine; both express the same Langhe terroir.")
    PAIR(prod1a, "Roast rack of lamb with salsa verde and rosemary-scented jus", "complement", "classic", "main",
         "Delicate Nebbiolo tannin and rose-petal aroma frame spring lamb with Italian precision.")
    PAIR(prod1a, "Porcini mushroom risotto with aged Parmigiano and truffle oil", "complement", "classic", "main",
         "Langhe's forest flavours — porcini echoes Nebbiolo's tertiary earthiness in a perfect regional alignment.")
    PAIR(prod1a, "Castelmagno aged cheese with acacia honey", "complement", "established", "cheese",
         "Piedmont's most distinctive aged cheese with the region's greatest wine — regional nobility on the plate.")

prod1b, new1b = PROD("Produttori del Barbaresco Riserva Asili", "wine_still", prod1b_id, r1, "Italy",
    subcategory="Nebbiolo",
    description="The cooperative's Asili Riserva is one of Barbaresco's most profound site expressions — from the finest north-south-exposed cru in the commune, producing wines of hauntingly floral, mineral Nebbiolo only in exceptional vintages after extended Slavonian oak aging.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Braised beef short rib in Barolo with gremolata", "complement", "classic", "main",
         "The Piedmontese Sunday lunch — braised beef in Nebbiolo wine matched with the region's finest red.")
    PAIR(prod1b, "Venison tartare with capers, mustard, and rocket", "complement", "established", "starter",
         "Raw game with structured Nebbiolo — the variety's tannin and acidity frame the tartare's mineral character.")
    PAIR(prod1b, "Truffle-scented agnolotti del plin in roasted meat jus", "complement", "classic", "main",
         "Piedmont's most refined pasta — small, meat-filled parcels in roasting jus with DOCG Barbaresco.")
    PAIR(prod1b, "Raschera with chestnut honey and hazelnut", "complement", "established", "cheese",
         "Alpine pressed Piedmontese cheese with chestnut honey mirrors Asili's silky depth and earthy complexity.")

# ── Region 2: Moravia / Czech Republic ──────────────────────────────────────
print("\n=== Region 2: Moravian Wine Region ===")
r2 = R("Moravian Wine Region", "Czech Republic", "wine",
    designation_type="PDO",
    designation_name="Moravian Wine Region PDO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="The Czech Republic's wine heartland, producing 96% of the country's wine across the Mikulov, Velkopavlovická, Slovácká, and Znojmo sub-regions. Moravia's continental climate — cold winters, warm summers — and loess-limestone soils produce distinctive Welschriesling, Müller-Thurgau, Blaufränkisch, and Pinot Noir. A new generation of biodynamic and natural winemakers is transforming the region's international profile.",
    key_producers="Sonberk, Stapleton-Springer, Dobrá Vinice, Nové Vinařství",
    historical_context="Viticulture in Moravia dates to Roman times; the region was a major wine producer for the Austro-Hungarian Empire; communist collectivisation destroyed estate wine culture, which is now being rebuilt by private producers since 1989.")

for yr, qd, pt in [
    (2022, "very_good", "rising"), (2021, "excellent", "rising"),
    (2020, "good", "stable"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Sonberk", "winery", r2, "Czech Republic",
    production_philosophy="terroir_focused",
    philosophy_description="The Czech Republic's most internationally visible estate, Sonberk produces Welschriesling, Pinot Blanc, and red varieties from Pouzdřany limestone and loess soils south of Brno — wines of unexpected precision and mineral clarity.",
    reputation_narrative="Regularly cited in international wine media as the Czech Republic's leading estate; Sonberk is transforming perceptions of Moravian wine.",
    price_positioning="mid_range")

prod2b_id = P("Dobrá Vinice", "winery", r2, "Czech Republic",
    production_philosophy="biodynamic",
    philosophy_description="A pioneering biodynamic estate in the Znojmo sub-region, producing precise, terroir-driven Welschriesling, Riesling, and Müller-Thurgau wines with very low yields and minimal intervention winemaking.",
    reputation_narrative="A reference for quality Moravian white wines; increasingly recognised by natural wine importers in Germany and Austria.",
    price_positioning="mid_range")

prod2a, new2a = PROD("Sonberk Welschriesling", "wine_still", prod2a_id, r2, "Czech Republic",
    subcategory="Welschriesling",
    description="The Czech Republic's signature variety from Pouzdřany limestone — crisp, mineral, and citrus-fresh with distinctive Czech terroir expression. A reference for Welschriesling's potential when farmed well on mineral soils.",
    price_tier="mid_range")
if new2a:
    PAIR(prod2a, "Smažený sýr (fried cheese) with tartare sauce and fries", "complement", "classic", "casual",
         "The Czech Republic's beloved fried cheese dish with a crisp local Welschriesling — a national pairing archetype.")
    PAIR(prod2a, "Grilled river trout with lemon butter and dill", "complement", "classic", "fish_course",
         "Moravian freshwater trout with Moravian white wine — a simple regional pairing of great authenticity.")
    PAIR(prod2a, "Roasted pork knuckle with caraway-sauerkraut and mustard", "complement", "established", "main",
         "Central European pork tradition with a crisp Welschriesling — the acidity cuts through pork fat perfectly.")
    PAIR(prod2a, "Olomoucké tvarůžky (aged fermented cheese) with rye bread", "contrast", "adventurous", "cheese",
         "Czech pungent aged cheese is challenging but the wine's acidity handles the extreme character with aplomb.")

prod2b, new2b = PROD("Dobrá Vinice Müller-Thurgau", "wine_still", prod2b_id, r2, "Czech Republic",
    subcategory="Müller-Thurgau",
    description="Biodynamic Müller-Thurgau from Znojmo loess soils — floral, delicate, and gently spiced, a Czech take on this often-maligned variety that shows unexpected elegance and terroir expression at low yields.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Asparagus soup with chervil and soft-boiled quail egg", "complement", "established", "starter",
         "Delicate Müller-Thurgau's floral character amplifies spring asparagus in a gentle, elegant pairing.")
    PAIR(prod2b, "Zander (pike-perch) fillet with Beurre blanc and parsley", "complement", "established", "fish_course",
         "Moravian freshwater fish with a floral local white — Central European riverine terroir in the glass and plate.")
    PAIR(prod2b, "Vegetable strudel with herb crème fraîche", "complement", "established", "starter",
         "Light pastry with delicate filling suits the variety's gentle aromatics without either overwhelming.")
    PAIR(prod2b, "Camembert with cranberry sauce and crusty rye", "bridge", "established", "cheese",
         "Soft bloomy-rind cheese with a gentle floral white — the cranberry's acidity bridges wine and rind.")

# ── Region 3: Tokaj ──────────────────────────────────────────────────────────
print("\n=== Region 3: Tokaj ===")
r3 = R("Tokaj", "Hungary", "wine",
    designation_type="PDO",
    designation_name="Tokaj PDO",
    reputation_tier="iconic",
    quality_trajectory="ascending",
    description="Hungary's most celebrated wine region, stretching along the Bodrog River near the Slovak border. Tokaj is renowned for Aszú — one of the world's greatest botrytised sweet wines, made from shrivelled Furmint and Hárslevelű grapes and classified by puttonyos sweetness level. But modern Tokaj is also producing remarkable dry Furmint of exciting complexity. UNESCO World Heritage status recognises the region's extraordinary cultural and viticultural significance.",
    key_producers="Royal Tokaji, Disznókő, Oremus, Szepsy, Kikelet",
    historical_context="Tokaji Aszú was described as the 'wine of kings and the king of wines' by Louis XIV; the region was the first demarcated wine appellation in the world, classified in 1730 by Maria Theresa — predating Porto, Bordeaux, and Burgundy classifications.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "exceptional", "rising"), (2017, "excellent", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Royal Tokaji Company", "winery", r3, "Hungary",
    production_philosophy="traditional",
    philosophy_description="Founded in 1990 by Hugh Johnson and a consortium to revive Tokaj's great estate tradition after communism — Royal Tokaji produces exceptional Aszú from classified First Growth vineyards Mézes Mály, Nyulászó, and Betsek, alongside a remarkable dry Furmint.",
    reputation_narrative="The most internationally recognised Tokaj estate; instrumental in the post-1989 renaissance of Hungary's greatest wine.",
    price_positioning="ultra_premium")

prod3b_id = P("Szepsy", "winery", r3, "Hungary",
    production_philosophy="terroir_focused",
    philosophy_description="István Szepsy is Hungary's most revered winemaker — his single-vineyard dry Furmint Úrágya and Aszú wines are considered the pinnacle of Tokaj, combining extraordinary mineral precision with the region's classic richness and longevity.",
    reputation_narrative="Hungary's reference winemaker; Szepsy's Aszú and dry Furmint are the most sought-after Tokaj wines.",
    price_positioning="ultra_premium")

prod3a, new3a = PROD("Royal Tokaji Aszú 5 Puttonyos", "wine_dessert", prod3a_id, r3, "Hungary",
    subcategory="Furmint-Hárslevelű Aszú",
    description="Royal Tokaji's flagship Aszú — five puttonyos sweetness with botrytis Furmint and Hárslevelű grapes producing apricot, honey, saffron, and orange peel complexity with the region's characteristic acidity that prevents cloying sweetness.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Foie gras au torchon with brioche and fig compote", "complement", "classic", "starter",
         "France's great liver with Hungary's great sweet wine — both are luxurious, both require the other's contrast.")
    PAIR(prod3a, "Roquefort with walnuts and pear on rye crispbread", "complement", "classic", "cheese",
         "The great sweet wine and blue cheese pairing — Tokaj Aszú's honeyed acidity against Roquefort's fierce salt.")
    PAIR(prod3a, "Apricot tart Tatin with vanilla crème fraîche", "complement", "classic", "dessert",
         "Aszú's signature apricot character mirrored in the tart itself — an elegant fruit-on-fruit harmony.")
    PAIR(prod3a, "Pan-seared duck liver with caramelised orange and ginger", "elevate", "established", "starter",
         "Duck liver's richness is lifted and framed by Aszú's sweet acidity and botrytis complexity.")

prod3b, new3b = PROD("Szepsy Tokaj Dry Furmint Úrágya", "wine_still", prod3b_id, r3, "Hungary",
    subcategory="Furmint",
    description="Szepsy's single-vineyard dry Furmint from the Úrágya first growth — volcanic tuff soils producing a mineral, precise, and complex dry white of extraordinary character. Shows Furmint's potential as a world-class dry variety: electric acidity, citrus, mineral, and great aging potential.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Lake Balaton pike-perch with dill cream and potato", "complement", "established", "fish_course",
         "Hungarian freshwater fish with Tokaj's finest dry white — a rare regional luxury pairing of native terroir.")
    PAIR(prod3b, "Chicken paprikash with egg noodles and sour cream", "bridge", "classic", "main",
         "Hungary's defining dish with Hungarian wine — paprika's richness is framed by Furmint's electric acidity.")
    PAIR(prod3b, "Lángos with sour cream, dill, and smoked trout", "complement", "established", "casual",
         "Hungarian fried flatbread with toppings — Furmint's acid cuts the frying fat while echoing the dill.")
    PAIR(prod3b, "Aged Pálpusztai cheese with honey and walnuts", "complement", "established", "cheese",
         "Hungary's pungent aged cheese with dry Furmint's mineral precision — a challenging but authentic regional pairing.")

# ── Region 4: Etna ──────────────────────────────────────────────────────────
print("\n=== Region 4: Etna ===")
r4 = R("Etna", "Italy", "wine",
    designation_type="DOC",
    designation_name="Etna DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The slopes of Sicily's active volcano are one of Italy's most exciting wine frontiers — altitude (up to 1,000m), black volcanic basalt and ash soils, old ungrafted pre-phylloxera vines, and extreme diurnal temperature variation produce wines of extraordinary mineral intensity and freshness. Etna Rosso from Nerello Mascalese rivals the finest Pinot Noir and Nebbiolo in elegance; Etna Bianco from Carricante achieves haunting salinity and precision. The 'Barolo of Sicily' is now among Europe's most discussed wine appellations.",
    key_producers="Benanti, Passopisciaro, Cornelissen, Terre Nere, Calabretta",
    historical_context="Etna's volcanic wines have been traded since Phoenician times; the appellation was created in 1968 but remained obscure until Andrea Franchetti (Passopisciaro) and Marc Cornelissen arrived in the 2000s, sparking a renaissance that drew investment from across Italy.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Passopisciaro", "winery", r4, "Italy",
    production_philosophy="terroir_focused",
    philosophy_description="Andrea Franchetti's Etna estate pioneered the contrada (single-vineyard parcel) movement on the volcano's north slope. Passopisciaro's single-contrada Nerello Mascalese wines from Chiappemacine, Rampante, Sciaranuova, and others rival Grand Cru Burgundy in site specificity and mineral complexity.",
    reputation_narrative="The estate that defined modern Etna fine wine; Franchetti's contrada wines are benchmarks of Sicilian viniculture.",
    price_positioning="ultra_premium")

prod4b_id = P("Benanti", "winery", r4, "Italy",
    production_philosophy="traditional",
    philosophy_description="The pioneer of Etna quality wine — Giuseppe Benanti began bottling single-vineyard Etna wines in the 1980s when the appellation was unknown. Benanti's Serra della Contessa red and Pietramarina white Carricante are the region's founding benchmarks.",
    reputation_narrative="The father of modern Etna wine; Benanti's decades of work established the DOC's credibility.",
    price_positioning="premium")

prod4a, new4a = PROD("Passopisciaro Etna Rosso Chiappemacine", "wine_still", prod4a_id, r4, "Italy",
    subcategory="Nerello Mascalese",
    description="Single-contrada Nerello Mascalese from the Chiappemacine parcel on Etna's north slope — volcanic basalt and ancient vines producing a wine of haunting mineral precision, red cherry, dried flowers, and iron-smoke character with Pinot Noir-like delicacy.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Grilled swordfish with caponata and salted ricotta", "complement", "classic", "main",
         "Sicilian grilled swordfish with volcanic island Nerello — the wine's iron minerality mirrors the fish's marine depth.")
    PAIR(prod4a, "Slow-braised rabbit with olives, capers, and sun-dried tomato", "complement", "established", "main",
         "Classic Sicilian agrodolce rabbit preparation with Etna's light-bodied red — regional symbiosis.")
    PAIR(prod4a, "Salumi board with Nebbrodi pork products and pistachio", "complement", "established", "casual",
         "Sicilian charcuterie from black Nebbrodi pigs with Etna's Nerello — Sicilian artisan terroir pairing.")
    PAIR(prod4a, "Aged Pecorino Siciliano with dried Sicilian oregano and olive oil", "complement", "classic", "cheese",
         "Sicily's aged sheep's cheese with Etna's volcanic red — dried oregano bridges both through Mediterranean herbs.")

prod4b, new4b = PROD("Benanti Etna Bianco Superiore Pietramarina", "wine_still", prod4b_id, r4, "Italy",
    subcategory="Carricante",
    description="Benanti's flagship white — Carricante from the Milo area on Etna's eastern flank, aged in large old casks. Pietramarina is one of Italy's greatest white wines: saline, mineral, citrus-driven, and hauntingly long with extreme aging potential.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Spaghetti alle vongole with white wine, garlic, and parsley", "complement", "classic", "main",
         "Sicily's clam pasta with Etna's finest white — volcanic saline mineral mirrors the vongole's ocean brine.")
    PAIR(prod4b, "Grilled red prawn (gambero rosso) with lemon and sea salt", "complement", "classic", "starter",
         "Sicilian red prawn's sweetness is elevated by Pietramarina's citrus and mineral precision.")
    PAIR(prod4b, "Seared tuna in sesame crust with caponata", "complement", "established", "main",
         "Sicilian tuna with Etna Bianco's saline character — the wine's acidity cuts through sesame oil richness.")
    PAIR(prod4b, "Ricotta with pistachio pesto and Sicilian honey", "complement", "established", "cheese",
         "Fresh Sicilian ricotta with pistachio echoes the wine's cream and mineral notes through island-specific ingredients.")

# ── Region 5: Abruzzo ────────────────────────────────────────────────────────
print("\n=== Region 5: Abruzzo ===")
r5 = R("Abruzzo", "Italy", "wine",
    designation_type="DOC",
    designation_name="Abruzzo DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="An underrated Adriatic wine region east of Rome, producing Montepulciano d'Abruzzo (powerful, dark, and structured) and Trebbiano d'Abruzzo (Italy's most elegant expression of this otherwise ordinary variety in the hands of Valentini). The region's dramatic Apennine landscape and Gran Sasso mountains create extreme terroir variation; the best producers farm at altitude for freshness and complexity.",
    key_producers="Valentini, Emidio Pepe, Cataldi Madonna, Masciarelli",
    historical_context="Abruzzo was historically a wine-producing region supplying bulk to northern Italy; Edoardo Valentini's arrival in the 1970s as an artisanal winemaker of international calibre forced a reassessment of the region's potential.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Valentini", "winery", r5, "Italy",
    production_philosophy="traditional",
    philosophy_description="The most eccentric and celebrated estate in central Italy — Francesco Paolo and Francesco Valentini produce extraordinarily long-lived Trebbiano d'Abruzzo and Montepulciano d'Abruzzo from old vines using old-fashioned techniques, releasing wines years after harvest only in exceptional vintages.",
    reputation_narrative="Among Italy's most mythologised wine estates; Valentini Trebbiano is one of Italy's greatest white wines.",
    price_positioning="ultra_premium")

prod5b_id = P("Emidio Pepe", "winery", r5, "Italy",
    production_philosophy="natural",
    philosophy_description="One of Italy's natural wine pioneers — Emidio Pepe produces Montepulciano d'Abruzzo using foot-treading, no added sulphur, no filtration, and decades of bottle aging. His wines are eccentric, alive, and evolve magnificently over 30-40 years.",
    reputation_narrative="Italy's most revered natural wine estate; Emidio Pepe Montepulciano is a reference for natural wine philosophy globally.",
    price_positioning="premium")

prod5a, new5a = PROD("Valentini Trebbiano d'Abruzzo", "wine_still", prod5a_id, r5, "Italy",
    subcategory="Trebbiano d'Abruzzo",
    description="Italy's most unexpected white wine — Trebbiano d'Abruzzo from very old vines, released only in exceptional vintages after years of aging. Shows nothing of the variety's ordinary reputation: mineral, complex, herbal, and extraordinarily age-worthy over 20+ years.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Brodetto di pesce Abruzzese with saffron and local seafood", "complement", "classic", "main",
         "Abruzzo's Adriatic fish stew with its most celebrated white wine — a rare regional luxury pairing.")
    PAIR(prod5a, "Grilled scallop with 'nduja butter and lemon", "complement", "established", "starter",
         "The wine's mineral depth and acidity handle the spicy 'nduja fat while lifting the scallop's sweetness.")
    PAIR(prod5a, "White truffle with scrambled eggs and aged Parmigiano", "elevate", "established", "starter",
         "Simple luxury — white truffle's earthiness is elevated by the wine's mineral complexity and age.")
    PAIR(prod5a, "Maccheroni alla chitarra with lamb ragù and pecorino", "bridge", "classic", "main",
         "Abruzzo's iconic pasta shape with regional lamb ragù — the wine's structure bridges lamb richness and pasta.")

prod5b, new5b = PROD("Emidio Pepe Montepulciano d'Abruzzo", "wine_still", prod5b_id, r5, "Italy",
    subcategory="Montepulciano",
    description="One of Italy's most extraordinary natural wines — Montepulciano foot-trodden, unfiltered, and unsulphured, evolving in bottle for decades. Deep, earthy, dark-fruited, and alive with natural fermentation complexity; requires 10-20 years to show its best.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Arrosticini (grilled lamb skewers) with Abruzzese herbs", "complement", "classic", "main",
         "Abruzzo's defining street food with its most authentic natural red — a genuinely regional pairing archetype.")
    PAIR(prod5b, "Slow-braised wild boar with Apennine herbs and polenta", "complement", "established", "main",
         "Mountain game with mountain wine — both carry the same wild, earthy, Apennine character.")
    PAIR(prod5b, "Porchetta di Ariccia with rosemary and fennel seed", "complement", "established", "main",
         "Central Italian whole-roasted pork with natural Montepulciano's earthy, dark-fruit depth.")
    PAIR(prod5b, "Aged Pecorino di Farindola with local chestnut honey", "complement", "established", "cheese",
         "Abruzzo's distinctive goat-and-sheep Pecorino with mountain honey — a rare regional cheese of great character.")

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
