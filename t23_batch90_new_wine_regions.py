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

# ── Region 1: Emilia-Romagna ──────────────────────────────────────────────────
print("\n=== Region 1: Emilia-Romagna ===")
r1 = R("Emilia-Romagna", "Italy", "wine",
    designation_type="DOC",
    designation_name="Emilia-Romagna DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Italy's gastronomic heartland straddling the Po Valley from the Apennines to the Adriatic, producing some of Italy's most food-centric wines — Lambrusco (sparkling, dry or off-dry), Sangiovese di Romagna, Pignoletto, and Albana di Romagna. Emilia produces rich, fatty foods (Parmigiano, Prosciutto di Parma, Mortadella, Culatello) that demand Lambrusco's cleansing bubbles. Romagna's Sangiovese is increasingly serious, particularly from the Predappio sub-zone.",
    key_producers="Cavicchioli, Cleto Chiarli, Fattoria Zerbina, Tre Monti, Villa di Corlo",
    historical_context="Lambrusco's reputation was destroyed by sweet, mass-produced exports in the 1970s-80s; the craft Lambrusco revival of the 2010s has restored the wine's dignity with dry, terroir-specific expressions from the Sorbara, Grasparossa, and Salamino subzones.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "very_good", "stable"),
    (2021, "excellent", "stable"), (2020, "very_good", "stable"), (2019, "good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Cleto Chiarli", "winery", r1, "Italy",
    production_philosophy="traditional",
    philosophy_description="The oldest and most respected Lambrusco house in Modena — Chiarli's Lambrusco di Sorbara is the benchmark for the variety's finest expression: pale pink-red, delicate, floral, and bone-dry with extraordinary acidity and cherry fruit.",
    reputation_narrative="The reference traditional producer for quality Lambrusco; Prêt à Boire and Vigna del Cristo are the defining bottles.",
    price_positioning="mid_range")

prod1b_id = P("Fattoria Zerbina", "winery", r1, "Italy",
    production_philosophy="terroir_focused",
    philosophy_description="Cristina Geminiani's estate in Faenza is the standard-bearer for Romagna Sangiovese and Albana di Romagna — her Pietramora Sangiovese and Scaccomatto Albana Passito are among Emilia-Romagna's finest individual wines, challenging the region's bulk wine reputation.",
    reputation_narrative="Romagna's most internationally recognised quality estate; Scaccomatto is Italy's finest Albana dessert wine.",
    price_positioning="premium")

prod1a, new1a = PROD("Cleto Chiarli Lambrusco di Sorbara Vigna del Cristo", "wine_sparkling", prod1a_id, r1, "Italy",
    subcategory="Lambrusco di Sorbara",
    description="The finest Lambrusco from the Sorbara subzone — the palest and most delicate of all Lambruscos. Fragrant violet flowers, fresh cherry, and bone-dry, razor-sharp acidity with fine persistent fizz. The anti-Lambrusco Lambrusco: nothing sweet, nothing heavy.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Culatello di Zibello with grissini and unsalted butter", "complement", "classic", "starter",
         "Emilia's great cured meat with Emilia's great sparkling red — the wine's acidity cuts through culatello's extraordinary fat.")
    PAIR(prod1a, "Mortadella di Bologna with tigelle flatbread", "complement", "classic", "casual",
         "The quintessential Emilia street food with the quintessential Emilia sparkling wine — a regional institution.")
    PAIR(prod1a, "Parmigiano-Reggiano 36-month with balsamic vinegar di Modena", "complement", "classic", "cheese",
         "Three of Modena's greatest products together — aged Parmigiano, DOP balsamic, and Lambrusco in one plate.")
    PAIR(prod1a, "Salumi misti platter with giardiniera and bread", "complement", "classic", "casual",
         "Emilian charcuterie board — Lambrusco's bubbles cleanse through layers of cured pork fat with each bite.")

prod1b, new1b = PROD("Fattoria Zerbina Sangiovese di Romagna Pietramora Riserva", "wine_still", prod1b_id, r1, "Italy",
    subcategory="Sangiovese",
    description="Romagna's benchmark Sangiovese Riserva — from the Marzeno sub-zone on calcareous clay, this wine challenges Tuscany's monopoly on the variety: structured, complex, and mineral with dark cherry, tobacco, and earthy depth comparable to Chianti Classico Riserva.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Tagliatelle al ragù Bolognese (authentic version, no milk)", "complement", "classic", "main",
         "Bologna's defining dish with the region's finest Sangiovese — the classic Emiliano Sunday lunch in one pairing.")
    PAIR(prod1b, "Roast pork neck with rosemary, fennel, and soft polenta", "complement", "established", "main",
         "Emilian pork preparation with Romagna Sangiovese — the wine's acidity balances the fat with Italian precision.")
    PAIR(prod1b, "Torta di Tagliatelle (hazelnut-almond cake) with zabaglione", "contrast", "suggested", "dessert",
         "Emilian traditional dessert — the cake's nutty sweetness contrasts with the wine's dry Sangiovese character.")
    PAIR(prod1b, "Formaggio di Fossa aged in tufa pits", "complement", "established", "cheese",
         "Romagna's most distinctive cheese — pit-aged sheep's milk with a mineral, funky depth matching Pietramora's structure.")

# ── Region 2: Sagrantino di Montefalco ───────────────────────────────────────
print("\n=== Region 2: Sagrantino di Montefalco ===")
r2 = R("Sagrantino di Montefalco", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Sagrantino di Montefalco DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="An almost unknown grape variety exclusive to a tiny hillside appellation in Umbria — Sagrantino produces wines of astonishing tannic structure, perhaps the most tannin-rich grape in Italy. The small town of Montefalco and its surrounding hills produce concentrated, powerful reds that require extraordinary aging patience but reveal remarkable complexity of dark fruit, chocolate, and dried flowers after 10-20 years.",
    key_producers="Arnaldo Caprai, Paolo Bea, Colpetrone, Tabarrini",
    historical_context="Sagrantino was used for centuries as a Passito (sweet dried grape wine) for local church use; Arnaldo Caprai's championing of dry Sagrantino from the late 1980s created the modern DOCG and established international awareness of this obscure Umbrian variety.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2018, "excellent", "stable"),
    (2017, "very_good", "stable"), (2016, "excellent", "stable"), (2015, "excellent", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Arnaldo Caprai", "winery", r2, "Italy",
    production_philosophy="terroir_focused",
    philosophy_description="Marco Caprai transformed Sagrantino from a local curiosity to an internationally acclaimed DOCG through extensive research into viticultural and winemaking techniques. His 25 Anni is Italy's reference for the variety's potential.",
    reputation_narrative="The estate that put Sagrantino on the world wine map; 25 Anni is Italy's definitive Sagrantino bottling.",
    price_positioning="ultra_premium")

prod2b_id = P("Paolo Bea", "winery", r2, "Italy",
    production_philosophy="natural",
    philosophy_description="Giampiero Bea makes Montefalco's most traditional Sagrantino — extremely long macerations (often 90+ days), no added yeasts, minimal sulphur, and extended aging in large old casks. Bea's wines are austere, tannic, and often only drinkable after 15-20 years but reveal extraordinary complexity.",
    reputation_narrative="Italy's most radical Sagrantino producer; Bea's minimal-intervention approach has global natural wine cult following.",
    price_positioning="premium")

prod2a, new2a = PROD("Arnaldo Caprai Sagrantino di Montefalco 25 Anni", "wine_still", prod2a_id, r2, "Italy",
    subcategory="Sagrantino",
    description="The reference Sagrantino di Montefalco — 25 Anni celebrates the 25th anniversary of Caprai's winery. Concentrated, structured, and powerfully tannic from selected old-vine parcels; dark chocolate, dried violets, blackberry, and earth. Requires 10+ years of cellaring to resolve.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Slow-braised wild boar in red wine with black olives and bitter chocolate", "complement", "classic", "main",
         "Umbrian wild boar preparation with Umbria's most powerful red — both share the same dark, brooding intensity.")
    PAIR(prod2a, "Roasted wood pigeon with liver crostini and truffle sauce", "complement", "established", "main",
         "Game bird and offal preparation suited to extreme tannin structure — the liver echoes Sagrantino's iron depth.")
    PAIR(prod2a, "Aged Pecorino di Norcia with local black truffle and honey", "complement", "established", "cheese",
         "Umbrian aged sheep's cheese with truffle and honey — both local products bridge through earthy character.")
    PAIR(prod2a, "Stracotto di manzo (pot-roasted beef) with Sagrantino reduction", "complement", "classic", "main",
         "Regional cooking using the wine in the preparation mirrors the wine in the glass in an elegant Umbrian circle.")

prod2b, new2b = PROD("Paolo Bea Sagrantino di Montefalco Pagliaro", "wine_still", prod2b_id, r2, "Italy",
    subcategory="Sagrantino",
    description="Bea's flagship natural Sagrantino from the Pagliaro cru — fermented with natural yeasts, macerated for 70+ days, aged in old Slavonian oak for years. Almost impossibly structured in youth but reveals extraordinary complexity of mineral, dried cherry, and tobacco after 15+ years.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Cinghiale (wild boar) cacciatore with rosemary and juniper", "complement", "classic", "main",
         "Umbrian hunter-style wild boar is the classic Sagrantino pairing — the wine's tannin tames the game's wild character.")
    PAIR(prod2b, "Aged lardo di Colonnata on warm bread with black pepper", "complement", "established", "casual",
         "Cured Apennine fat on warm bread is a rare match for Sagrantino's extreme tannin — fat absorbs and softens.")
    PAIR(prod2b, "Spit-roasted whole pig with garlic and fennel pollen", "complement", "established", "main",
         "Central Italian porchetta — the whole pig's succulence and fat provide the buffer for Pagliaro's power.")
    PAIR(prod2b, "Dark bitter chocolate (85%) with sea salt and hazelnut", "complement", "adventurous", "dessert",
         "The most tannic wine with the most bitter chocolate — iron and tannin mirror each other in an austere pairing.")

# ── Region 3: Vermentino di Sardegna ─────────────────────────────────────────
print("\n=== Region 3: Vermentino di Sardegna ===")
r3 = R("Vermentino di Sardegna", "Italy", "wine",
    designation_type="DOC",
    designation_name="Vermentino di Sardegna DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Sardinia's most important white wine DOC, produced from the Vermentino grape across the island — though the finest expressions come from the Gallura sub-zone in the northeast (Vermentino di Gallura DOCG) on granite soils. Sardinian Vermentino is bone-dry, aromatic with bitter almond, citrus blossom, and a characteristic slightly bitter finish that makes it uniquely food-compatible with the island's seafood and rich meat traditions.",
    key_producers="Capichera, Sella & Mosca, Piero Mancini, Argiolas",
    historical_context="Vermentino arrived in Sardinia from Liguria or possibly Corsica in the 14th century; the grape's ability to produce high-quality wine in Sardinia's granite soils was not recognised internationally until the 1990s craft wine renaissance.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "very_good", "stable"),
    (2021, "excellent", "stable"), (2020, "very_good", "stable"), (2019, "good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Capichera", "winery", r3, "Italy",
    production_philosophy="terroir_focused",
    philosophy_description="The benchmark estate for Vermentino di Gallura — the Ragnedda family's Capichera produces the variety's most concentrated and age-worthy expression from granite soils above Arzachena in northeastern Sardinia. Also produces exceptional aged Isola dei Nuraghi IGT red blends.",
    reputation_narrative="Sardinia's most internationally acclaimed white wine estate; Capichera Vermentino is the variety's reference bottle.",
    price_positioning="premium")

prod3b_id = P("Argiolas", "winery", r3, "Italy",
    production_philosophy="traditional",
    philosophy_description="Sardinia's most celebrated multi-variety estate — Antonio Argiolas produces the iconic Turriga (Cannonau-dominant blend) alongside excellent Vermentino, Nuragus, and Nasco from vineyards across the southern island. Turriga is considered one of Italy's greatest red wines.",
    reputation_narrative="Sardinia's most complete and internationally recognised wine estate; Turriga is Italy's benchmark for Cannonau-based wines.",
    price_positioning="premium")

prod3a, new3a = PROD("Capichera Vermentino di Gallura DOCG", "wine_still", prod3a_id, r3, "Italy",
    subcategory="Vermentino",
    description="The finest Vermentino di Gallura — from granite hillsides above Arzachena in the Gallura DOCG, aged briefly in Slavonian oak for texture. Complex, mineral, and intensely aromatic with bitter almond, wild fennel, citrus blossom, and peach; one of Italy's most distinctive white wines.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Spaghetti alle arselle (razor clam pasta) with parsley and garlic", "complement", "classic", "main",
         "Sardinian razor clam pasta with the island's finest white wine — the wine's sea-salt mineral mirrors the clam.")
    PAIR(prod3a, "Bottarga di muggine (grey mullet roe) with warm bread and olive oil", "complement", "classic", "starter",
         "Sardinia's dried mullet roe with its signature white wine — one of the Mediterranean's great local food pairings.")
    PAIR(prod3a, "Grilled fresh tuna steak with caponata and lemon", "complement", "established", "main",
         "Mediterranean tuna with Sardinian white — the wine's bitter almond and citrus frame the tuna's richness.")
    PAIR(prod3a, "Pecorino Sardo with Sardinian honey and carta di musica", "complement", "classic", "cheese",
         "The island's sheep's cheese with its signature white wine and paper-thin flatbread — pure Sardinian identity.")

prod3b, new3b = PROD("Argiolas Turriga", "wine_still", prod3b_id, r3, "Italy",
    subcategory="Cannonau Blend",
    description="Sardinia's most celebrated red wine — a blend of Cannonau (Grenache), Carignano, Bovale Sardo, and Malvasia Nera aged 18 months in French barriques. Turriga is a complex, structured wine of extraordinary depth: dark fruit, leather, Mediterranean garrigue, and volcanic mineral from ancient Sardinian soils.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Roast leg of Sardinian kid (caprette) with myrtle and rosemary", "complement", "classic", "main",
         "Sardinian kid with myrtle — the island's defining roast with its most celebrated red wine in perfect harmony.")
    PAIR(prod3b, "Porcetto arrosto (Sardinian suckling pig) with myrtle branches", "complement", "classic", "main",
         "Sardinia's most iconic dish — whole roast pig with myrtle smoke and the island's greatest red wine.")
    PAIR(prod3b, "Wild mushroom porcini pasta with aged Pecorino Sardo", "complement", "established", "main",
         "Sardinian pasta with local mushrooms and aged sheep's cheese — Turriga's depth matches the earthy combination.")
    PAIR(prod3b, "Aged Fiore Sardo with raw honey and dried fig", "complement", "classic", "cheese",
         "Sardinia's oldest sheep's cheese — smoked Fiore Sardo with the island's wine is an ancient island pairing.")

# ── Region 4: Valtellina ─────────────────────────────────────────────────────
print("\n=== Region 4: Valtellina ===")
r4 = R("Valtellina", "Italy", "wine",
    designation_type="DOCG",
    designation_name="Valtellina Superiore DOCG",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="A narrow Alpine valley in Lombardy bordering Switzerland, producing Nebbiolo-based wines (called Chiavennasca locally) from impossibly steep terraced vineyards on south-facing granite slopes above the Adda River. Valtellina Superiore — divided into five subzones (Sassella, Grumello, Inferno, Valgella, Maroggia) — produces wines of extraordinary minerality, earthy depth, and aging potential. Also produces Sforzato di Valtellina DOCG from partially dried Nebbiolo grapes.",
    key_producers="Ar.Pe.Pe., Nino Negri, Rainoldi, Triacca, Sandro Fay",
    historical_context="Valtellina's terraced vineyards were carved by hand over centuries from solid granite; the region supplied Alpine Switzerland and Lombardy with wine for hundreds of years; the arrival of railway access in the 19th century opened international markets; today handpicking on 70-degree slopes makes Valtellina one of wine's most challenging terroirs.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "excellent", "stable"),
    (2020, "very_good", "stable"), (2019, "exceptional", "rising"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Ar.Pe.Pe.", "winery", r4, "Italy",
    production_philosophy="traditional",
    philosophy_description="The Pelizzatti Perego family's Ar.Pe.Pe. is Valtellina's most revered traditional producer — hand-harvesting on near-vertical terraces, using only native Nebbiolo, and aging in large old Slavonian casks without intervention. Their Sassella Rocce Rosse and Grumello Buon Consiglio Riservas are among Italy's most profound wines.",
    reputation_narrative="Valtellina's reference traditional estate; Rocce Rosse is one of Italy's most distinctive and original wines.",
    price_positioning="premium")

prod4b_id = P("Nino Negri", "winery", r4, "Italy",
    production_philosophy="traditional",
    philosophy_description="The largest and most internationally recognised Valtellina producer — Nino Negri's 5 Stelle Sforzato is the benchmark for the dried-grape Nebbiolo category, aged in French barriques and showing extraordinary richness and concentration from shrivelled Nebbiolo grapes.",
    reputation_narrative="Valtellina's most visible estate internationally; 5 Stelle Sforzato is the definitive expression of the DOCG.",
    price_positioning="premium")

prod4a, new4a = PROD("Ar.Pe.Pe. Valtellina Superiore Sassella Rocce Rosse Riserva", "wine_still", prod4a_id, r4, "Italy",
    subcategory="Chiavennasca (Nebbiolo)",
    description="From the Sassella subzone's finest granite terraces — Ar.Pe.Pe.'s flagship is one of Italy's most original wines. Aged 5+ years in large Slavonian casks, Rocce Rosse develops extraordinary complexity of dried roses, tobacco, iron, and mountain mineral over 20+ years.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Bresaola della Valtellina with rucola, Parmigiano, and lemon", "complement", "classic", "starter",
         "Valtellina's air-dried beef with its finest red wine — a regional pairing of extraordinary cultural depth.")
    PAIR(prod4a, "Pizzoccheri (buckwheat pasta with potatoes, cabbage, and Bitto)", "complement", "classic", "main",
         "Valtellina's defining mountain dish with its defining wine — Bitto cheese and buckwheat with Nebbiolo.")
    PAIR(prod4a, "Slow-braised venison with juniper, chocolate, and red wine", "complement", "established", "main",
         "Alpine game braised in the same wine region's terroir — juniper and chocolate echo the wine's mineral depth.")
    PAIR(prod4a, "Bitto aged 4 years with local honey and walnut bread", "complement", "classic", "cheese",
         "Valtellina's iconic Alpine cheese aged for years — aged Bitto with aged Sassella Nebbiolo is a mountain archetype.")

prod4b, new4b = PROD("Nino Negri 5 Stelle Sforzato di Valtellina DOCG", "wine_still", prod4b_id, r4, "Italy",
    subcategory="Sforzato (Dried Nebbiolo)",
    description="The benchmark Sforzato — partially dried Nebbiolo grapes producing 14%+ alcohol wine with extraordinary concentration. Dark plum, dried cherry, chocolate, and cedar with an intensity that belies its Alpine origins; one of Italy's most distinctive and powerful wines.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Roast venison with bitter chocolate sauce and red cabbage", "complement", "classic", "main",
         "5 Stelle's power and dark-fruit concentration match venison's richness with the chocolate sauce as bridge.")
    PAIR(prod4b, "Cassoeula (pork belly and savoy cabbage stew)", "complement", "established", "main",
         "Lombardy's winter pork and cabbage stew demands a powerful wine — Sforzato handles the fat and bitterness.")
    PAIR(prod4b, "Aged Casera Valtellina with polenta and mushrooms", "complement", "classic", "main",
         "Mountain cheese with mountain wine in the classic Lombard mountain table — simple and deeply satisfying.")
    PAIR(prod4b, "Dark chocolate torte with cherry compote and whipped cream", "complement", "adventurous", "dessert",
         "Sforzato's dried-cherry and chocolate character creates unexpected harmony with a chocolate cherry dessert.")

# ── Region 5: Txakoli (Getariako) ────────────────────────────────────────────
print("\n=== Region 5: Getariako Txakolina ===")
r5 = R("Getariako Txakolina", "Spain", "wine",
    designation_type="DO",
    designation_name="Getariako Txakolina DO",
    reputation_tier="respected",
    quality_trajectory="established",
    description="The most famous of the three Txakoli appellations in the Basque Country — from the coastal hills around the medieval fishing village of Getaria, producing bone-dry, lightly sparkling white wine from the indigenous Hondarrabi Zuri grape. Txakoli is the definitive aperitif of San Sebastián's pintxos culture: low alcohol (10-11%), high acid, saline-mineral, and best poured from height to aerate its natural carbonic freshness.",
    key_producers="Txomin Etxaniz, Ameztoi, Hiruzta, Rezabal",
    historical_context="Txakoli has been produced in the Basque Country since at least the 16th century; its natural light carbonation comes from completing fermentation in bottle like ancestral method; the wine nearly disappeared in the 20th century but was revived in the 1980s by Basque cultural pride and pintxos gastronomy tourism.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "very_good", "stable"),
    (2021, "excellent", "stable"), (2020, "very_good", "stable"), (2019, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Txomin Etxaniz", "winery", r5, "Spain",
    production_philosophy="traditional",
    philosophy_description="The defining estate of Getariako Txakolina — five generations of the Etxaniz family have produced the most internationally recognised Txakoli from vineyards overlooking the Bay of Biscay, just steps from Getaria's harbour. Traditional pour from height aerates the wine's natural fizz.",
    reputation_narrative="The reference Txakoli estate internationally; the definitive bottle for San Sebastián's pintxos culture.",
    price_positioning="mid_range")

prod5b_id = P("Ameztoi", "winery", r5, "Spain",
    production_philosophy="traditional",
    philosophy_description="Another top Getaria estate, Ameztoi produces a classic bone-dry Txakoli alongside the Rubentis rosé and a rare Txakoli Berezia late-harvest expression — all from vineyards facing the Cantabrian Sea.",
    reputation_narrative="One of Getaria's two reference estates; Ameztoi Rubentis is the benchmark for Txakoli rosé.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Txomin Etxaniz Txakoli Getariako", "wine_still", prod5a_id, r5, "Spain",
    subcategory="Hondarrabi Zuri",
    description="The definitive Txakoli — poured from height in the traditional Basque manner, Txomin Etxaniz's wine is bone-dry, lightly sparkling, intensely citrus-mineral, saline, and bracing. The aperitif of San Sebastián's pintxos bars and a wine with no equivalent elsewhere in the world.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Gilda pintxo (anchovy, olive, guindilla pepper on skewer)", "complement", "classic", "aperitif",
         "Txakoli and Gilda is the most quintessential pintxo pairing — the wine's brine mirrors the anchovy's salinity.")
    PAIR(prod5a, "Grilled Cantabrian anchovies with olive oil and sea salt", "complement", "classic", "starter",
         "The greatest anchovy in the world with the Bay of Biscay's own white wine — a Basque coastal identity pairing.")
    PAIR(prod5a, "Kokotxas al pil-pil (cod cheeks in olive oil emulsion)", "complement", "classic", "main",
         "Basque haute cuisine's defining dish with Txakoli's mineral acidity cutting through the gelatinous pil-pil sauce.")
    PAIR(prod5a, "Freshly shucked Galician oysters with lemon", "cleanse", "classic", "aperitif",
         "Atlantic oysters with Atlantic Txakoli — both carry brine, mineral, and the same Cantabrian coastal character.")

prod5b, new5b = PROD("Ameztoi Rubentis Txakoli Rosé", "wine_still", prod5b_id, r5, "Spain",
    subcategory="Hondarrabi Beltza",
    description="From red Hondarrabi Beltza grapes — the rare rosé Txakoli poured at height like the white. Pale salmon-pink with wild strawberry, citrus, and the same Atlantic mineral saline freshness as white Txakoli. One of Spain's most distinctive rosé wines.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Jamón Ibérico de Bellota with pan con tomate", "complement", "classic", "starter",
         "Spain's finest ham with the Basque Country's definitive rosé aperitif — simplicity and quality in balance.")
    PAIR(prod5b, "Spider crab (txangurro) gratin with tomato and brandy", "complement", "classic", "main",
         "Getaria's bay provides both the crab and the wine — Txangurro a Donostiarra is the signature local preparation.")
    PAIR(prod5b, "Gambas al ajillo with good Basque bread to mop the oil", "complement", "established", "starter",
         "Garlic prawns with rosé Txakoli — the wine's brine and citrus amplify the seafood while cutting the garlic oil.")
    PAIR(prod5b, "Baby squid in their ink (chipirones en su tinta) with white rice", "complement", "classic", "main",
         "The most dramatic Basque pairing — ink-black squid with blush-pink wine, but the flavours are in complete harmony.")

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
