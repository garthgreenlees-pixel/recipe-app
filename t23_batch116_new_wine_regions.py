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
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── REGION 1: Rosso Conero ────────────────────────────────────────────────────
print("=== Region 1: Rosso Conero ===")
r1 = R("Rosso Conero", "Italy", "wine",
        designation_type="DOC", designation_name="Rosso Conero DOC",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Marche coastal DOC on the Monte Conero promontory; Montepulciano d'Abruzzo from limestone and clay sea-cliff vineyards; structured and food-worthy with Adriatic mineral character.",
        key_producers="Umani Ronchi, Moroder",
        historical_context="Monte Conero's dramatic sea cliffs give Montepulciano a unique mineral-coastal character unlike inland Abruzzo expressions; Umani Ronchi's Pelago elevated the appellation internationally in the 1990s.")
VIN(r1, 2022, "very_good", "stable", "Coastal warmth; Montepulciano shows dark cherry richness and sea mineral.")
VIN(r1, 2021, "good", "stable", "Balanced year; elegant and aromatic coastal Montepulciano.")
VIN(r1, 2020, "excellent", "rising", "Outstanding vintage; concentration and mineral both exceptional.")
VIN(r1, 2019, "very_good", "stable", "Classic Conero expression; dark fruit and limestone mineral in harmony.")
VIN(r1, 2018, "good", "stable", "Solid vintage; consistent food-friendly expression.")
p1a = P("Umani Ronchi", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Marche's most commercially important and internationally visible winery; Pelago super-Marche and San Lorenzo Verdicchio are benchmark wines.",
        reputation_narrative="Umani Ronchi is Marche wine's global ambassador; consistently high quality across a wide range.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Moroder", "winery", r1, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Monte Conero estate producing structured, mineral Montepulciano from ancient limestone terraces above the Adriatic.",
        reputation_narrative="Respected for organic commitment and honest Monte Conero character; earns specialist attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Umani Ronchi Cùmaro Rosso Conero", "wine_still", p1a, r1, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Premium Rosso Conero with dark cherry, leather, sea mineral and fine Montepulciano tannin; aged in French oak for elegance and structure.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Brodetto marchigiano (Marche fish stew)", "complement", "classic", "main", "Adriatic fish stew with Monte Conero Montepulciano; sea mineral in both dish and glass.")
    PAIR(pr1a, "Grilled Adriatic sword fish with herbs", "complement", "established", "fish_course", "Robust swordfish and structured Montepulciano; dark fruit meets the meaty fish.")
    PAIR(pr1a, "Coniglio in porchetta marchigiano", "complement", "classic", "main", "Marche herb-stuffed rabbit with local red; fennel and wild herbs bridge the Conero spice.")
    PAIR(pr1a, "Vincisgrassi (Marche meat lasagne)", "complement", "classic", "main", "Marche's festive lasagne with local red; rich offal and meat sauce met by Montepulciano structure.")
pr1b, n1b = PROD("Moroder Dorico Rosso Conero", "wine_still", p1b, r1, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Organic Monte Conero Montepulciano with dark cherry, violet, limestone mineral and fine tannin; coastal freshness distinguishes it from inland styles.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Grilled lamb chops with rosemary", "complement", "classic", "main", "Lamb and Montepulciano — the Marche-Abruzzo mountain tradition along the Adriatic coast.")
    PAIR(pr1b, "Pasta al sugo di cinghiale", "complement", "established", "main", "Wild boar pasta and tannic Montepulciano; dark fruit and game in Marche tradition.")
    PAIR(pr1b, "Porchetta marchigiana con erbe", "complement", "classic", "casual", "Marche herb-stuffed pork roast with local red; the festive market tradition.")
    PAIR(pr1b, "Aged Pecorino di Fossa", "complement", "classic", "cheese", "Pit-aged Marche sheep's cheese with Rosso Conero; intense earthy cheese and mineral red.")

# ── REGION 2: Lacrima di Morro d'Alba ────────────────────────────────────────
print("=== Region 2: Lacrima di Morro d'Alba ===")
r2 = R("Lacrima di Morro d'Alba", "Italy", "wine",
        designation_type="DOC", designation_name="Lacrima di Morro d'Alba DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Tiny Marche DOC producing the unique Lacrima di Morro grape — one of Italy's most violet-aromatic varieties with intense floral fragrance, dark cherry and a distinctly short ageing profile.",
        key_producers="Stefano Mancinelli, Marotti Campi",
        historical_context="Lacrima (tear) refers to the juice that weeps from the thin-skinned berries; a grape grown only around Morro d'Alba in the Marche hills; nearly extinct and saved by local producers in the 1980s.")
VIN(r2, 2022, "very_good", "stable", "Warm Marche year; Lacrima's violet and cherry more intense than usual.")
VIN(r2, 2021, "good", "stable", "Classic aromatic vintage; floral freshness and light red fruit well expressed.")
VIN(r2, 2020, "very_good", "stable", "Good vintage; Lacrima shows best aromatic intensity in recent years.")
VIN(r2, 2019, "good", "stable", "Standard vintage; reliable Lacrima floral character.")
VIN(r2, 2018, "good", "stable", "Consistent vintage; pleasant and aromatic for early drinking.")
p2a = P("Stefano Mancinelli", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The champion of Lacrima di Morro d'Alba; Stefano Mancinelli's decades of dedication restored the variety from near-extinction to cult status.",
        reputation_narrative="Universally acknowledged as the definitive Lacrima producer; his single-vineyard wines are collector pieces.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Marotti Campi", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-varietal Marche estate with strong Lacrima and Verdicchio range; commercially important for spreading the variety's reputation.",
        reputation_narrative="Most commercially visible Lacrima producer; consistent quality and good distribution.",
        price_positioning="mid_range",
        authority_tier=1)
pr2a, n2a = PROD("Stefano Mancinelli Lacrima di Morro d'Alba Superiore", "wine_still", p2a, r2, "Italy",
                  subcategory="Lacrima di Morro",
                  description="Benchmark Lacrima with extraordinary violet perfume, dark cherry, rose petal and spice; medium-light body with velvet texture and a haunting floral finish.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Risotto with dried violets and duck", "complement", "classic", "main", "Floral wine with floral dish; violet risotto amplifies Lacrima's perfume signature.")
    PAIR(pr2a, "Tagliata di manzo con rucola", "complement", "established", "main", "Beef tagliata and aromatic red; the wine's light body and fragrance complement the lean beef.")
    PAIR(pr2a, "Pasta al ragù di coniglio", "complement", "classic", "main", "Rabbit ragù and Lacrima's aromatic character; a delicate combination for a delicate game.")
    PAIR(pr2a, "Fresh strawberries with balsamic and black pepper", "complement", "classic", "pre_dessert", "Strawberry and violet in resonance; Lacrima's floral fragrance echoes the fresh berry.")
pr2b, n2b = PROD("Marotti Campi Lacrima di Morro d'Alba Orgiolo", "wine_still", p2b, r2, "Italy",
                  subcategory="Lacrima di Morro",
                  description="Intense and structured Lacrima from old vines; violet, rose, dark cherry and spice with more body than typical expressions.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Prosciutto di Carpegna with melon", "complement", "classic", "starter", "Marche's finest cured ham and the region's most aromatic red; florality bridges sweet melon and salt.")
    PAIR(pr2b, "Pappardelle with hare ragù", "complement", "established", "main", "Game ragù and violet-aromatic red; hare's richness met by Lacrima's spice and cherry.")
    PAIR(pr2b, "Crostata with cherry jam", "complement", "classic", "dessert", "Cherry tart and Lacrima's cherry fruit; the wine bridges dessert and savoury courses.")
    PAIR(pr2b, "Grilled pigeon with black cherry sauce", "complement", "classic", "main", "Pigeon game and Lacrima violet; black cherry sauce links the wine's cherry character.")

# ── REGION 3: Rossese di Dolceacqua ──────────────────────────────────────────
print("=== Region 3: Rossese di Dolceacqua ===")
r3 = R("Rossese di Dolceacqua", "Italy", "wine",
        designation_type="DOC", designation_name="Rossese di Dolceacqua DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Tiny Ligurian Riviera DOC near the French border producing Rossese — a light, aromatic red with raspberry, rose and herb from ancient terraced hillside vineyards above the Nervia valley.",
        key_producers="Terre Bianche, Maccario Dringenberg",
        historical_context="Dolceacqua is the wine village that Napoleon reportedly loved; Rossese shares genetic links with Tibouren of Provence; its light, fragrant style anticipates modern fresh red trends by centuries.")
VIN(r3, 2022, "very_good", "stable", "Warm Ligurian vintage; Rossese shows excellent raspberry and herb definition.")
VIN(r3, 2021, "good", "stable", "Classic light Rossese with pale colour and delicate fragrance.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; aromatic precision and herb complexity both strong.")
VIN(r3, 2019, "good", "stable", "Standard vintage; pleasant and aromatic for early drinking.")
VIN(r3, 2018, "good", "stable", "Consistent vintage; honest Rossese character preserved.")
p3a = P("Terre Bianche", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The reference producer for Rossese di Dolceacqua; ancient terrace vineyards above the Nervia valley deliver wines of extraordinary aromatic complexity.",
        reputation_narrative="Unanimously regarded as Dolceacqua's finest; wines appear on the world's most progressive wine lists.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Maccario Dringenberg", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Family estate producing serious Rossese from single terraced plots above the medieval village; long maceration for more structure.",
        reputation_narrative="Increasingly recognised alongside Terre Bianche for the finest Dolceacqua expressions.",
        price_positioning="mid_range",
        authority_tier=1)
pr3a, n3a = PROD("Terre Bianche Rossese di Dolceacqua Arcana", "wine_still", p3a, r3, "Italy",
                  subcategory="Rossese",
                  description="Single-vineyard Rossese with extraordinary aromatic lift; raspberry, rose, herbes de Ligurie and mineral; pale ruby, silky and hauntingly persistent.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Grilled branzino al sale (sea salt-crusted)", "complement", "classic", "fish_course", "Light Rossese and delicate sea bass; the wine's raspberry freshness mirrors coastal salinity.")
    PAIR(pr3a, "Cima alla genovese (stuffed Ligurian veal)", "complement", "classic", "main", "Ligurian feast dish stuffed with herbs; Rossese's herb character is the natural companion.")
    PAIR(pr3a, "Pasta al pesto with green beans and potato", "complement", "classic", "main", "Ligurian pesto pasta and local Rossese; basil-herb bridge between wine and sauce.")
    PAIR(pr3a, "Funghi porcini trifolati con polenta", "complement", "established", "main", "Porcini mushrooms and Rossese's earthy herb character; light red and forest floor in dialogue.")
pr3b, n3b = PROD("Maccario Dringenberg Rossese di Dolceacqua Luvaira", "wine_still", p3b, r3, "Italy",
                  subcategory="Rossese",
                  description="Single-plot Rossese from ancient terrace above Dolceacqua; more structure and mineral depth than typical; raspberry, violet, herbs and sea mineral.",
                  price_tier="mid_range")
if n3b:
    PAIR(pr3b, "Rabbit with Ligurian olives and pine nuts", "complement", "classic", "main", "Ligurian rabbit with local red; olives and pine nuts link through the wine's herb character.")
    PAIR(pr3b, "Minestrone alla genovese", "complement", "classic", "casual", "Ligurian vegetable soup with local wine; honest regional harmony.")
    PAIR(pr3b, "Grilled octopus with Ligurian olive oil", "complement", "established", "starter", "Coastal Ligurian octopus with the riviera's signature red; light tannin handles the seafood.")
    PAIR(pr3b, "Focaccia col formaggio di Recco", "complement", "classic", "casual", "Ligurian cheese focaccia and local wine; the Riviera's most famous casual combination.")

# ── REGION 4: Cinque Terre ───────────────────────────────────────────────────
print("=== Region 4: Cinque Terre ===")
r4 = R("Cinque Terre", "Italy", "wine",
        designation_type="DOC", designation_name="Cinque Terre DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Liguria's most dramatic DOC; steep terraced vineyards above the five cliff-village towns produce Bosco, Albarola and Vermentino whites with intense salinity, citrus and sea mineral from precipitous coastal terraces.",
        key_producers="Walter De Battè, Buranco",
        historical_context="Cinque Terre's monorail vineyards are among Italy's most costly to farm; terraces maintained by a handful of heroic producers; the local Sciacchetrà passito is a rare sweet wine of extraordinary depth.")
VIN(r4, 2022, "very_good", "stable", "Sea-cooled year with good aromatic precision; mineral and citrus both excellent.")
VIN(r4, 2021, "good", "stable", "Classic Cinque Terre; lean, saline and precise with coastal freshness.")
VIN(r4, 2020, "very_good", "stable", "Good vintage; Bosco shows excellent texture and sea mineral intensity.")
VIN(r4, 2019, "good", "stable", "Standard vintage; reliable coastal freshness and mineral character.")
VIN(r4, 2018, "good", "stable", "Consistent vintage; honest sea-cliff Ligurian character.")
p4a = P("Walter De Battè", "winery", r4, "Italy",
        production_philosophy="minimal_intervention",
        philosophy_description="The artisan champion of Cinque Terre; De Battè's terrace wines are minimal-intervention expressions of the cliff vineyards' unique terroir.",
        reputation_narrative="Most internationally recognised Cinque Terre producer; wines appear in Italy's finest natural wine lists.",
        price_positioning="premium",
        authority_tier=2)
p4b = P("Buranco", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Family estate farming the most vertical terraces above Monterosso; produces Cinque Terre DOC and Sciacchetrà passito.",
        reputation_narrative="Respected local producer; honest expressions of a remarkably challenging appellation.",
        price_positioning="mid_range",
        authority_tier=1)
pr4a, n4a = PROD("Walter De Battè Cinque Terre Bianco", "wine_still", p4a, r4, "Italy",
                  subcategory="Bosco-Albarola-Vermentino",
                  description="Benchmark Cinque Terre with sea cliff intensity; saline mineral, citrus, white flowers and extraordinary persistence; low-intervention from terraced limestone.",
                  price_tier="premium")
if n4a:
    PAIR(pr4a, "Muscoli ripieni (stuffed Ligurian mussels)", "complement", "classic", "starter", "Cliff-gathered mussels and cliff-vineyard wine; the most local of all Ligurian pairings.")
    PAIR(pr4a, "Acciughe alla ligure (Ligurian anchovies)", "complement", "classic", "starter", "Anchovy is Liguria's defining flavour; the wine's salinity amplifies and its acidity cuts.")
    PAIR(pr4a, "Pansoti con salsa di noci", "complement", "classic", "main", "Ligurian herb-filled pasta with walnut sauce; Cinque Terre's mineral balances the nut richness.")
    PAIR(pr4a, "Steamed prawns with Ligurian olive oil", "complement", "established", "fish_course", "Delicate shellfish and mineral white; olive oil bridges coastal salinity.")
pr4b, n4b = PROD("Buranco Cinque Terre Bianco", "wine_still", p4b, r4, "Italy",
                  subcategory="Bosco-Vermentino",
                  description="Family terrace Cinque Terre with sea mineral, citrus and delicate herb; honest and briny with good freshness.",
                  price_tier="mid_range")
if n4b:
    PAIR(pr4b, "Pasta al pesto genovese", "complement", "classic", "main", "Ligurian pesto and Ligurian wine; basil, pine nut and Parmigiano met by sea mineral white.")
    PAIR(pr4b, "Fritto di paranza (small coastal fried fish)", "complement", "classic", "casual", "Cliff-village fried seafood tradition; the wine's acidity cuts through and refreshes.")
    PAIR(pr4b, "Farinata di ceci (Ligurian chickpea flatbread)", "complement", "classic", "casual", "Ligurian street food staple and local white; rosemary and chickpea with sea mineral.")
    PAIR(pr4b, "Grilled branzino with Ligurian herbs", "complement", "established", "fish_course", "Sea bass from the Ligurian sea with wine from its coastal cliff terraces; regional perfection.")

# ── REGION 5: Pigato Ligure ──────────────────────────────────────────────────
print("=== Region 5: Pigato Riviera Ligure di Ponente ===")
r5 = R("Pigato Riviera Ligure di Ponente", "Italy", "wine",
        designation_type="DOC", designation_name="Riviera Ligure di Ponente DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Western Ligurian Riviera DOC producing Pigato — a grape related to Vermentino but with more body, herb and almondine character; grown on terraced hillsides between Albenga and Imperia.",
        key_producers="Laura Aschero, Bruna",
        historical_context="Pigato is Liguria's hidden-gem white grape; slightly richer and more textured than Vermentino with a distinctive bitter herb finish; gaining following among Italian white wine specialists.")
VIN(r5, 2022, "very_good", "stable", "Warm western Riviera year; Pigato shows excellent aromatic concentration.")
VIN(r5, 2021, "good", "stable", "Balanced vintage; Pigato herb character and mineral both well expressed.")
VIN(r5, 2020, "very_good", "stable", "Good quality; Pigato at its most textured and complex.")
VIN(r5, 2019, "good", "stable", "Standard vintage; reliable herb-mineral Pigato character.")
VIN(r5, 2018, "good", "stable", "Consistent vintage; good everyday Ligurian white.")
p5a = P("Laura Aschero", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="The most celebrated female producer in Liguria; Laura Aschero's Pigato from hillside terraces above Imperia is the variety's benchmark.",
        reputation_narrative="Universally regarded as Liguria's finest Pigato producer; wines appear in all Italy's best restaurants.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Bruna", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Western Riviera estate producing textured Pigato from the Albenga plain and surrounding hills; consistent quality and good distribution.",
        reputation_narrative="Second most recognised Pigato name; reliable and widely distributed across Italy.",
        price_positioning="mid_range",
        authority_tier=1)
pr5a, n5a = PROD("Laura Aschero Pigato Riviera Ligure di Ponente", "wine_still", p5a, r5, "Italy",
                  subcategory="Pigato",
                  description="Benchmark Pigato with distinctive herbal complexity; white peach, thyme, almond and sea mineral with more body than Vermentino; excellent food versatility.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Cima alla genovese fredda (cold Ligurian veal)", "complement", "classic", "starter", "The classic Ligurian cold veal roast; herb filling mirrors Pigato's herbal complexity.")
    PAIR(pr5a, "Focaccia genovese con olive", "complement", "classic", "casual", "Ligurian focaccia tradition; olive oil richness and sea salt met by Pigato's herb and mineral.")
    PAIR(pr5a, "Grilled dentice (sea bream) Ligurian style", "complement", "established", "fish_course", "Western Riviera sea bream and hillside white; olive oil and herbs bridge.")
    PAIR(pr5a, "Pasta trofie al pesto", "complement", "classic", "main", "Ligurian pasta and Ligurian white; pesto's basil and pine nut complement Pigato's herbs.")
pr5b, n5b = PROD("Bruna Pigato Riviera Ponente U Baccan", "wine_still", p5b, r5, "Italy",
                  subcategory="Pigato",
                  description="Single-vineyard Pigato with citrus, peach, herbes de Provence and textured mineral; fuller-bodied and food-versatile.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Tonno in scatola con fagioli e cipolla", "complement", "classic", "casual", "Ligurian tuna and bean salad with local white; one of Italy's great simple combinations.")
    PAIR(pr5b, "Trenette with walnut sauce (salsa di noci)", "complement", "established", "main", "Ligurian pasta with walnut sauce; Pigato's texture and herb balance the nut richness.")
    PAIR(pr5b, "Frisceu di baccalà (Ligurian salt cod fritters)", "complement", "classic", "casual", "Salt cod fritters and coastal Pigato; Ligurian fried street food tradition.")
    PAIR(pr5b, "Insalata di polpo alla ligure", "complement", "established", "starter", "Ligurian octopus salad with local white; potatoes, olives and herb bridge the wine's character.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
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
