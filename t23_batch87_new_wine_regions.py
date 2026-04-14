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

# ── Region 1: Mosel — Bernkastel ────────────────────────────────────────────
print("\n=== Region 1: Bernkastel (Mosel) ===")
r1 = R("Bernkastel", "Germany", "wine",
    designation_type="Grosslage",
    designation_name="Bernkastel Grosslage",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="The heart of the Mittelmosel, centred on the medieval town of Bernkastel-Kues and its famous Doctor vineyard — one of Germany's most expensive per-hectare parcels. The steep slate terraces along the Mosel River produce Rieslings of extraordinary mineral complexity, feather-light body, and piercing acidity with the characteristic petrol, lime, and slate character of the Mosel's finest expressions. Prädikats from Auslese to Trockenbeerenauslese achieve unrivalled complexity.",
    key_producers="Dr. Loosen, JJ Prüm, Fritz Haag, Markus Molitor, Selbach-Oster",
    historical_context="The Bernkasteler Doctor vineyard gained its name in 1360 when Archbishop Boemund II of Trier reportedly recovered from illness after drinking its wine; the vineyard has been disputed legally and politically for centuries as a symbol of the Mosel's prestige.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "excellent", "stable"), (2019, "exceptional", "stable"), (2018, "very_good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("JJ Prüm", "winery", r1, "Germany",
    production_philosophy="traditional",
    philosophy_description="The most revered estate on the Mosel — Katharina Prüm continues her family's tradition of producing Riesling Spätlese, Auslese, and Beerenauslese from the Wehlener Sonnenuhr and Graacher Himmelreich that define Mosel elegance. The wines require extraordinary patience, often opening only after 20-30 years.",
    reputation_narrative="One of Germany's most iconic wine estates; JJ Prüm Auslese is among the world's most collectable Rieslings.",
    price_positioning="ultra_premium")

prod1b_id = P("Dr. Loosen", "winery", r1, "Germany",
    production_philosophy="terroir_focused",
    philosophy_description="Ernst Loosen revived and expanded his family's old-vine estate in the 1980s, becoming the most internationally successful Mosel ambassador. His Erdener Treppchen, Wehlener Sonnenuhr, and Ürziger Würzgarten Rieslings from 50-100+ year vines are benchmarks of Mosel expression.",
    reputation_narrative="The most internationally recognised Mosel estate; Ernst Loosen's advocacy transformed global awareness of German Riesling.",
    price_positioning="premium")

prod1a, new1a = PROD("JJ Prüm Wehlener Sonnenuhr Riesling Auslese", "wine_dessert", prod1a_id, r1, "Germany",
    subcategory="Riesling Auslese",
    description="From the famous Sundial vineyard of Wehlen — Prüm's Auslese is among Mosel's most mythologised wines: feather-light, honeyed yet acidic, with lime, slate, and white peach character. Closed for 10-15 years then remarkable for 40+.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Foie gras with Sauternes gelée and brioche toast", "complement", "classic", "starter",
         "Sweet German Riesling's acidity cuts foie's fat while honeyed botrytis mirrors the liver's richness.")
    PAIR(prod1a, "Blue lobster with Thai-style lemongrass cream", "complement", "established", "main",
         "Riesling's tropical and citrus dimension suits Asian-inflected shellfish preparation with floral lemongrass.")
    PAIR(prod1a, "Roquefort with honey comb and walnuts on pain d'épices", "complement", "classic", "cheese",
         "Sweet Riesling and blue cheese is a classic German pairing — the spiced bread bridges both with warm aromatics.")
    PAIR(prod1a, "Peach and almond tart with crème pâtissière", "complement", "established", "dessert",
         "Prüm's stone-fruit and almond character mirrors the tart's filling in a food-in-the-wine alignment.")

prod1b, new1b = PROD("Dr. Loosen Erdener Treppchen Riesling Spätlese", "wine_still", prod1b_id, r1, "Germany",
    subcategory="Riesling Spätlese",
    description="From the red slate Treppchen (step) terraces of Erden — a classic Mosel Spätlese of off-dry character with crisp apple, citrus, and distinctive slate-mineral character. Shows the range's elegance and approachability without sacrificing complexity.",
    price_tier="mid_range")
if new1b:
    PAIR(prod1b, "Braised pork belly with apple, ginger, and five-spice", "complement", "classic", "main",
         "Riesling's apple character and residual sweetness balance pork belly's fat with five-spice's aromatic complexity.")
    PAIR(prod1b, "Thai green curry with jasmine rice and coconut cream", "bridge", "established", "main",
         "Mosel Spätlese's off-dry residual sweetness is the ideal foil for green curry's chilli heat and coconut richness.")
    PAIR(prod1b, "Duck liver pâté with riesling aspic and cornichons", "complement", "established", "starter",
         "German regional harmony — duck liver with Riesling aspic mirrors the wine in the glass through the jelly.")
    PAIR(prod1b, "Munster with caraway seeds and rye bread", "complement", "classic", "cheese",
         "The Alsace pairing that crosses the Rhine — pungent Munster tamed by Riesling's off-dry sweetness and acid.")

# ── Region 2: Saar (Mosel-Saar-Ruwer) ───────────────────────────────────────
print("\n=== Region 2: Saar ===")
r2 = R("Saar", "Germany", "wine",
    designation_type="Bereich",
    designation_name="Saar Bereich",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The most austere and mineral expression of German Riesling — the Saar tributary of the Mosel produces wines of extreme acidity, stony minerality, and steely precision from blue-grey Devonian slate. In challenging vintages the wines are aggressively tart; in great years they achieve a crystalline perfection found nowhere else in Germany. The finest single vineyards — Scharzhofberg, Ockfener Bockstein, Wiltinger Braune Kupp — are considered Riesling's most mineral and precise sites.",
    key_producers="Egon Müller, Van Volxem, Zilliken, Von Hövel",
    historical_context="The Saar was the source of some of the most expensive German wines in the 19th century when Prussian aristocrats prized its razor-mineral Rieslings above all others; Egon Müller at Scharzhofberg maintains this tradition, producing Germany's most expensive wines today.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "excellent", "stable"), (2019, "exceptional", "rising"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Egon Müller", "winery", r2, "Germany",
    production_philosophy="traditional",
    philosophy_description="The Müller family has owned Scharzhofberg since 1797 — Egon Müller IV produces Germany's most expensive wines, with Scharzhofberg Trockenbeerenauslese fetching auction prices comparable to DRC. The estate's precision and mineral purity are unmatched in German viticulture.",
    reputation_narrative="Germany's most prestigious estate; Scharzhofberg TBA is the world's most expensive German wine.",
    price_positioning="ultra_premium")

prod2b_id = P("Van Volxem", "winery", r2, "Germany",
    production_philosophy="terroir_focused",
    philosophy_description="Roman Niewodniczanski revived the Van Volxem estate in the late 1990s, acquiring some of the Saar's finest old-vine parcels and producing dry (trocken) Saar Rieslings of extraordinary mineral precision and complexity, challenging the traditional off-dry style.",
    reputation_narrative="The defining estate for dry Saar Riesling; Perpetus and Scharzhofberger Pergentsknopp are benchmarks.",
    price_positioning="premium")

prod2a, new2a = PROD("Egon Müller Scharzhofberger Riesling Spätlese", "wine_still", prod2a_id, r2, "Germany",
    subcategory="Riesling Spätlese",
    description="Scharzhofberg's classic expression at the Spätlese level — slate-mineral, citrus, and apple with barely perceptible residual sweetness balanced by piercing Saar acidity. A transcendent mineral experience that defines German Riesling precision.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "River Rhine salmon gravlax with dill crème fraîche and cucumber", "complement", "classic", "starter",
         "Saar's mineral precision and delicate off-dry sweetness are perfect foils for cured salmon's fat and dill.")
    PAIR(prod2a, "Sole with lemon beurre blanc and chive butter", "complement", "classic", "fish_course",
         "Pure white fish with Germany's purest mineral white — simplicity meeting mineral precision in equal measure.")
    PAIR(prod2a, "Scallop ceviche with lime, chilli, and coconut", "complement", "established", "starter",
         "Saar acidity and citrus echo the ceviche marinade while the wine's mineral cuts through coconut's richness.")
    PAIR(prod2a, "Munster Géromé washed-rind with cumin bread", "complement", "established", "cheese",
         "Strong washed-rind cheese handled by Riesling's off-dry sweetness — the classic German wine and cheese pairing.")

prod2b, new2b = PROD("Van Volxem Scharzhofberger Riesling GG", "wine_still", prod2b_id, r2, "Germany",
    subcategory="Riesling Grosses Gewächs",
    description="Van Volxem's dry Grosses Gewächs from Scharzhofberg — a bone-dry mineral Riesling of exceptional concentration and precise stony character from old vines. A landmark of modern dry German Riesling and a riposte to Alsatian Grand Cru.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "White asparagus with hollandaise, Mosel Riesling, and ham", "complement", "classic", "starter",
         "Germany's definitive spring vegetable pairing — Spargel and dry Riesling is the German haute cuisine archetype.")
    PAIR(prod2b, "Roasted Bresse pigeon with slate reduction and spring vegetables", "complement", "established", "main",
         "Dry Saar GG's precision and mineral depth bridge the delicate poultry and root vegetable combination.")
    PAIR(prod2b, "Quenelles de brochet with lobster bisque", "complement", "established", "main",
         "Classic Franco-German table — pike quenelles with rich bisque counterbalanced by bone-dry Riesling minerality.")
    PAIR(prod2b, "Affiné Camembert at perfect ripeness with apple chutney", "complement", "established", "cheese",
         "Ripe Camembert's ammonia and fat handled by GG Riesling's slate precision — apple chutney bridges both.")

# ── Region 3: Napa Valley — Stags Leap ──────────────────────────────────────
print("\n=== Region 3: Stags Leap District ===")
r3 = R("Stags Leap District", "USA", "wine",
    designation_type="AVA",
    designation_name="Stags Leap District AVA",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="A small AVA within southern Napa Valley defined by the Palisades — dramatic basalt cliffs that radiate heat and shelter the valley floor, creating a distinctive microclimate for Cabernet Sauvignon. Stags Leap's softer, more elegant Cabernet style was made famous when Warren Winiarski's Stag's Leap Wine Cellars SLV defeated Bordeaux First Growths at the 1976 Paris Tasting. The volcanic basalt and red volcanic tuffs produce Cabernet of unusual finesse and cassis-dominant fruit.",
    key_producers="Stag's Leap Wine Cellars, Shafer, Silverado Vineyards, Clos du Val, Pine Ridge",
    historical_context="The 1976 Paris Tasting (Judgement of Paris), in which SLV Cabernet defeated Mouton-Rothschild, Montrose, and Haut-Brion, transformed the global perception of California wine and established Napa Valley's international credentials.")

for yr, qd, pt in [
    (2022, "excellent", "stable"), (2021, "excellent", "stable"),
    (2019, "exceptional", "rising"), (2018, "excellent", "stable"), (2016, "excellent", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Stag's Leap Wine Cellars", "winery", r3, "USA",
    production_philosophy="terroir_focused",
    philosophy_description="Warren Winiarski's estate, now under Ste. Michelle Wine Estates and Antinori ownership, continues to produce the SLV and Cask 23 Cabernets that defined Stags Leap's reputation — structured, elegant, and age-worthy.",
    reputation_narrative="The estate that defeated Bordeaux in 1976; SLV and Cask 23 remain Napa Valley reference wines.",
    price_positioning="ultra_premium")

prod3b_id = P("Shafer Vineyards", "winery", r3, "USA",
    production_philosophy="terroir_focused",
    philosophy_description="The Shafer family has farmed Stags Leap since 1972 — their Hillside Select Cabernet Sauvignon from steep volcanic hillside vineyards is one of Napa's most consistently celebrated single-vineyard wines, combining power and elegant Stags Leap finesse.",
    reputation_narrative="One of Napa Valley's most admired family estates; Hillside Select is consistently among California's top Cabernets.",
    price_positioning="ultra_premium")

prod3a, new3a = PROD("Stag's Leap Wine Cellars Cask 23 Cabernet Sauvignon", "wine_still", prod3a_id, r3, "USA",
    subcategory="Cabernet Sauvignon",
    description="The estate's pinnacle — a blend of SLV and Fay Vineyard fruit representing the best lots from each harvest. Cask 23 is a California collector's icon: cassis, cedar, tobacco, and the characteristic volcanic minerality of Stags Leap District.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Dry-aged prime rib with au jus and creamed horseradish", "complement", "classic", "main",
         "California's great Cabernet with California's great beef cut — dry-aged umami meets cassis and cedar.")
    PAIR(prod3a, "Lamb rack with Bordelaise sauce and gratin dauphinois", "complement", "classic", "main",
         "Napa's homage to Bordeaux — the wine that defeated First Growths with a Franco-Californian lamb preparation.")
    PAIR(prod3a, "Duck confit with cherry mostarda and polenta", "complement", "established", "main",
         "The cassis-fruit dimension of Stags Leap Cabernet finds a natural bridge in cherry mostarda alongside duck.")
    PAIR(prod3a, "Aged Vella Dry Jack with walnut and dried apricot", "complement", "established", "cheese",
         "California's own aged dry cheese with Napa's reference Cabernet — a genuine California terroir pairing.")

prod3b, new3b = PROD("Shafer Hillside Select Cabernet Sauvignon", "wine_still", prod3b_id, r3, "USA",
    subcategory="Cabernet Sauvignon",
    description="From steep Stags Leap hillside vineyards planted on volcanic tuff — a powerfully concentrated yet elegant single-vineyard Cabernet of legendary status. Hillside Select requires a decade of cellaring but rewards 25+ years with extraordinary complexity.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Bone-in Wagyu ribeye with compound butter and roasted bone marrow", "complement", "classic", "main",
         "California's premium Cabernet with premium California beef — an expression of West Coast luxury in one pairing.")
    PAIR(prod3b, "Venison loin with blackberry gastrique and celery root", "complement", "established", "main",
         "Game's iron and dark berry paired with Hillside Select's blackberry fruit and volcanic mineral intensity.")
    PAIR(prod3b, "Truffle burgers on brioche with aged Gruyère", "complement", "established", "casual",
         "California's iconic luxury casual dining — truffle and beef with a flagship Napa Cabernet.")
    PAIR(prod3b, "Clothbound Cheddar with quince paste and roasted almonds", "complement", "established", "cheese",
         "English-style aged Cheddar provides the tannin-taming fat and complexity to match Hillside Select's power.")

# ── Region 4: Priorat ────────────────────────────────────────────────────────
print("\n=== Region 4: Priorat ===")
r4 = R("Priorat", "Spain", "wine",
    designation_type="DOQ",
    designation_name="Priorat DOQ",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="One of Spain's two DOCa/DOQ regions (with Rioja), Priorat occupies a remote mountain amphitheatre in southern Catalonia, producing wines of extraordinary concentration from Grenache and Carignan vines grown on the unique llicorella — volcanic black slate with flakes of mica that drain perfectly and reflect heat onto old vines. Priorat wines are among Spain's most powerful and sought-after, combining rich dark fruit with a distinctive iron-mineral quality.",
    key_producers="Álvaro Palacios, Clos Mogador, Mas Doix, Terroir al Límit",
    historical_context="Priorat was virtually abandoned by the 1980s with only a handful of small producers; the arrival of Álvaro Palacios, Dafne Glorian, René Barbier, and Carlos Pastrana in 1989 — the 'Priorat Pioneers' — transformed it into Spain's most expensive wine region within 15 years.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "excellent", "stable"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2017, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Álvaro Palacios", "winery", r4, "Spain",
    production_philosophy="terroir_focused",
    philosophy_description="The most important figure in Priorat's renaissance — Álvaro Palacios produces L'Ermita (Spain's most expensive wine), Finca Dofí, and Les Terrasses from old Grenache and Carignan vines on llicorella slate. Palacios also revived Bierzo (Pétalos) and La Rioja Oriental.",
    reputation_narrative="Spain's most celebrated winemaker; L'Ermita is one of Europe's most coveted wines.",
    price_positioning="ultra_premium")

prod4b_id = P("Clos Mogador", "winery", r4, "Spain",
    production_philosophy="biodynamic",
    philosophy_description="René Barbier's Clos Mogador is the founding estate of modern Priorat — biodynamically farmed old-vine Grenache and Carignan on the finest llicorella terraces, producing wines of extraordinary depth, complexity, and longevity.",
    reputation_narrative="One of the five Priorat pioneers; Clos Mogador is the appellation's reference biodynamic estate.",
    price_positioning="ultra_premium")

prod4a, new4a = PROD("Álvaro Palacios Les Terrasses Priorat", "wine_still", prod4a_id, r4, "Spain",
    subcategory="Grenache-Carignan Blend",
    description="Palacios's entry-point to Priorat — old-vine Grenache and Carignan from llicorella slate across multiple parcels. Les Terrasses expresses Priorat's iron-mineral character with rich dark fruit and Mediterranean warmth at a more accessible level.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Slow-braised lamb shoulder with romesco and charred calcots", "complement", "classic", "main",
         "Catalan-style lamb with romesco sauce — the region's culinary signature matched with its most celebrated wine.")
    PAIR(prod4a, "Wild boar with pine nuts, prunes, and chocolate", "complement", "established", "main",
         "Catalan agrodolce wild boar — pine nuts and prunes mirror the wine's iron-mineral and dried-fruit character.")
    PAIR(prod4a, "Grilled Ibérico presa with Maldon salt and lemon", "complement", "established", "main",
         "Ibérico's acorn-fat complexity and Priorat's slate mineral character create an Iberian luxury pairing.")
    PAIR(prod4a, "Manchego Viejo with quince and toasted almonds", "complement", "classic", "cheese",
         "Spain's iconic cheese board with a structured Priorat — quince and almonds bridge the wine's dark fruit.")

prod4b, new4b = PROD("Clos Mogador Priorat", "wine_still", prod4b_id, r4, "Spain",
    subcategory="Grenache-Carignan Blend",
    description="René Barbier's flagship biodynamic Priorat — old-vine Grenache and Carignan from ancient llicorella terraces producing one of Spain's most profound and complex wines: dark olive, iron, liquorice, and dried herbs with extraordinary density and mineral depth.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "Roasted Ibérico suckling pig with honey glaze and wild herbs", "complement", "classic", "main",
         "Spain's most prized pig with its most celebrated mountain wine — both share immense concentration and depth.")
    PAIR(prod4b, "Venison ragù with pappardelle and aged Manchego", "complement", "established", "main",
         "Robust game ragù with Clos Mogador's structure — Manchego adds the Iberian dimension to the Italian-format dish.")
    PAIR(prod4b, "Duck with cherry and cava reduction, lentil purée", "complement", "established", "main",
         "Biodynamic Grenache and dark cherry mirror each other; duck's richness frames the wine's power.")
    PAIR(prod4b, "Torta del Casar at room temperature with quince jelly", "complement", "established", "cheese",
         "Spain's liquid sheep's cheese with a structured mountain red — regional Spanish pairing of enormous character.")

# ── Region 5: Penedès ────────────────────────────────────────────────────────
print("\n=== Region 5: Penedès ===")
r5 = R("Penedès", "Spain", "wine",
    designation_type="DO",
    designation_name="Penedès DO",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Catalonia's largest and most diverse wine DO, stretching from the Mediterranean coast inland to the foothills of the Pyrenees. The region produces a remarkable range — from the finest Cava sparkling wines and elegant whites from Xarel·lo and Muscat, to substantial reds from Garnacha and Tempranillo. Torres, headquartered here, is Spain's most globally recognisable wine company and a pioneer of international varieties in Catalan viticulture.",
    key_producers="Torres, Jean León, Can Feixes, Parés Baltà, Albet i Noya",
    historical_context="Penedès has been at the centre of Catalan viticulture since the Phoenicians; the Cava industry grew here in the 1870s when Josep Raventós planted the first méthode champenoise vines; Torres's international expansion began the same year Robert Mondavi opened in Napa — both changed the global wine map.")

for yr, qd, pt in [
    (2022, "excellent", "stable"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Torres", "winery", r5, "Spain",
    production_philosophy="terroir_focused",
    philosophy_description="Spain's most global wine family — Miguel Torres pioneered climate-sensitive viticulture in Spain and has led the industry in sustainability. Their flagship Mas La Plana Cabernet Sauvignon famously defeated Château Latour at the 1979 Gault Millau Wine Olympiad.",
    reputation_narrative="Spain's most influential wine company; Mas La Plana's 1979 Paris victory mirrors the 1976 California triumph.",
    price_positioning="ultra_premium")

prod5b_id = P("Jean León", "winery", r5, "Spain",
    production_philosophy="traditional",
    philosophy_description="Founded by Catalan emigrant Jean León who worked as a busboy in Los Angeles before becoming Frank Sinatra's favourite restaurateur. He brought Cabernet Sauvignon and Chardonnay cuttings from Napa to Penedès in the 1960s — a pioneering act that shaped Catalan viticulture.",
    reputation_narrative="A historic Penedès estate with an extraordinary backstory; Vinya Le Havre Cabernet is a benchmark.",
    price_positioning="premium")

prod5a, new5a = PROD("Torres Mas La Plana Cabernet Sauvignon", "wine_still", prod5a_id, r5, "Spain",
    subcategory="Cabernet Sauvignon",
    description="The wine that defeated Château Latour in 1979 — Torres's flagship single-vineyard Cabernet from high-altitude Penedès soils, producing a structured, cedar-accented wine of great precision and aging potential at a fraction of comparable Bordeaux prices.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Roast rack of lamb with Catalan romesco and escalivada", "complement", "classic", "main",
         "Catalan Cabernet with Catalan roasted vegetable traditions — romesco bridges both through its almond-tomato structure.")
    PAIR(prod5a, "Grilled beef sirloin with Pedro Ximénez reduction and bone marrow", "complement", "established", "main",
         "Structured Catalan Cabernet's cedar and cassis frame aged beef with authority; PX bridges through sweetness.")
    PAIR(prod5a, "Wild mushroom croquetas with Ibérico ham and truffle aioli", "complement", "established", "starter",
         "Catalan tapas luxury with structured Cabernet — earthy mushroom echoes the wine's forest-floor character.")
    PAIR(prod5a, "Aged Idiazabal with quince and smoked paprika oil", "complement", "established", "cheese",
         "Basque smoked sheep's cheese with Catalan Cabernet — the smoke echoes cedar and oak in the wine.")

prod5b, new5b = PROD("Jean León Vinya Gigi Chardonnay", "wine_still", prod5b_id, r5, "Spain",
    subcategory="Chardonnay",
    description="Named after Jean León's mother, this Penedès Chardonnay is aged in French oak barrels — showing the warmth and richness of Catalan Chardonnay with apple, peach, hazelnut, and subtle oak integration. A pioneering expression of Penedès white wine potential.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Catalan fish soup (suquet de peix) with alioli and bread", "complement", "established", "main",
         "Catalan Mediterranean fish stew with Catalan Chardonnay — the wine's warmth matches the suquet's saffron richness.")
    PAIR(prod5b, "Roast chicken with escalivada (roasted vegetables) and alioli", "complement", "classic", "main",
         "Simple Catalan roasted poultry with oak-aged Chardonnay — warm, generous, and deeply regional.")
    PAIR(prod5b, "Creamy white asparagus with saffron butter and Ibérico", "complement", "established", "starter",
         "Catalan spring asparagus with warm Chardonnay — saffron and hazelnut echo the wine's aromatics.")
    PAIR(prod5b, "Aged Mahón cheese with honey and toasted pine nuts", "complement", "established", "cheese",
         "Balearic aged cow's cheese with Penedès Chardonnay — the oak and hazelnut bridge through pine nut and honey.")

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
