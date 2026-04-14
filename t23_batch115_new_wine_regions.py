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

# ── REGION 1: Colline Teramane Montepulciano d'Abruzzo ─────────────────────
print("=== Region 1: Colline Teramane Montepulciano d'Abruzzo ===")
r1 = R("Colline Teramane Montepulciano d'Abruzzo", "Italy", "wine",
        designation_type="DOCG", designation_name="Colline Teramane Montepulciano d'Abruzzo DOCG",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Abruzzo's only DOCG; Montepulciano d'Abruzzo from the Teramo hills — more structured, tannic and age-worthy than regular Abruzzo DOC wines from coastal gravels and clay-limestone hillsides.",
        key_producers="Illuminati, Nicodemi",
        historical_context="The Teramo hills produce Montepulciano of greater concentration and ageing potential than the coastal plain; the DOCG was created in 2003 to differentiate this quality tier from ubiquitous Abruzzo DOC.")
VIN(r1, 2022, "very_good", "stable", "Classic Abruzzo hills vintage; Montepulciano shows excellent dark fruit and structure.")
VIN(r1, 2021, "good", "stable", "Balanced season; leaner Montepulciano with good acidity and aromatic freshness.")
VIN(r1, 2020, "excellent", "rising", "Outstanding vintage for Abruzzo; depth and concentration both exceptional.")
VIN(r1, 2019, "very_good", "stable", "Warm and generous; Montepulciano dark cherry and violet at their best.")
VIN(r1, 2018, "very_good", "stable", "Strong vintage; structured and age-worthy Teramo hills expression.")
p1a = P("Illuminati", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-generational Abruzzo estate; one of the DOCG's founding producers with Zanna single-vineyard Montepulciano as the benchmark.",
        reputation_narrative="Italy's most celebrated Montepulciano d'Abruzzo producer; Zanna earns consistent top scores internationally.",
        price_positioning="mid_range",
        authority_tier=2)
p1b = P("Nicodemi", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Organic-leaning Teramo hills estate producing elegant, mineral Montepulciano and Trebbiano from hillside terroir.",
        reputation_narrative="Growing reputation for organic-farming approach; wines earning national critical attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr1a, n1a = PROD("Illuminati Zanna Colline Teramane Montepulciano d'Abruzzo", "wine_still", p1a, r1, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Flagship DOCG Montepulciano with extraordinary concentration; dark cherry, violet, leather and Teramo mineral; 15+ year ageing potential.",
                  price_tier="mid_range")
if n1a:
    PAIR(pr1a, "Agnello alla brace con rosmarino", "complement", "classic", "main", "Abruzzo lamb and Montepulciano; the region's canonical match — both carry the mountain air.")
    PAIR(pr1a, "Arrosticini (Abruzzese mutton skewers)", "complement", "classic", "casual", "The iconic Abruzzo street food; char-grilled mutton fat met by dark Montepulciano.")
    PAIR(pr1a, "Wild boar with Adriatic herbs", "complement", "established", "main", "Game and Montepulciano's tannin; Adriatic herb notes bridge mountain and sea influence.")
    PAIR(pr1a, "Pecorino d'Abruzzo stagionato", "complement", "classic", "cheese", "Abruzzo aged sheep's cheese and the region's finest red; mountain terroir in both.")
pr1b, n1b = PROD("Nicodemi Montepulciano d'Abruzzo Colline Teramane Neromoro", "wine_still", p1b, r1, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Organic hillside Montepulciano with precise mineral character; dark plum, violet, iron and Teramo clay; more elegant than typical Abruzzo DOC.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Pasta alla chitarra con ragù d'agnello", "complement", "classic", "main", "Abruzzo's square-cut pasta with lamb ragù is the iconic regional dish; Montepulciano completes it.")
    PAIR(pr1b, "Grilled pork sausages with pepperoncino", "complement", "established", "casual", "Spiced Abruzzo pork sausage and dark Montepulciano; chilli heat tempered by dark fruit.")
    PAIR(pr1b, "Slow-braised lamb shank with fennel", "complement", "established", "main", "Mountain lamb and structured Montepulciano; fennel bridges the wine's violet aromatics.")
    PAIR(pr1b, "Maccheroni al sugo di cinghiale", "complement", "established", "main", "Wild boar pasta and tannic Montepulciano; dark fruit and wild game in Abruzzo harmony.")

# ── REGION 2: Cerasuolo d'Abruzzo ────────────────────────────────────────────
print("=== Region 2: Cerasuolo d'Abruzzo ===")
r2 = R("Cerasuolo d'Abruzzo", "Italy", "wine",
        designation_type="DOC", designation_name="Cerasuolo d'Abruzzo DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Abruzzo's cherry-red rosato DOC; Montepulciano d'Abruzzo briefly macerated for vivid colour and body; one of Italy's most serious and food-worthy rosé styles.",
        key_producers="Cataldi Madonna, Masciarelli",
        historical_context="Cerasuolo (meaning 'cherry-like') is the world's most serious rosé in terms of body and structure; unlike Provence rosé it can age well; recently upgraded to its own DOC separate from Montepulciano d'Abruzzo.")
VIN(r2, 2022, "excellent", "rising", "Outstanding Cerasuolo vintage; cherry concentration and freshness both superb.")
VIN(r2, 2021, "very_good", "stable", "Classic expression; vibrant cherry-red colour and excellent savoury depth.")
VIN(r2, 2020, "very_good", "stable", "Good vintage; Cerasuolo at its most food-versatile.")
VIN(r2, 2019, "very_good", "stable", "Warm Abruzzo expression; rich and structured for a rosé.")
VIN(r2, 2018, "good", "stable", "Standard vintage; consistent cherry freshness and medium body.")
p2a = P("Cataldi Madonna", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Sulmona valley estate producing Cerasuolo of extraordinary seriousness; Luigi Cataldi Madonna is Abruzzo's most respected winemaker.",
        reputation_narrative="Cataldi Madonna's Cerasuolo is universally acknowledged as Italy's finest rosé; earns 90-95+ points consistently.",
        price_positioning="mid_range",
        authority_tier=2)
p2b = P("Masciarelli", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Abruzzo's most celebrated winery; Marina Cvetic's range from Cerasuolo to single-vineyard Montepulciano defines the region's premium quality.",
        reputation_narrative="Masciarelli's Villa Gemma Cerasuolo and Montepulciano are Abruzzo's most internationally recognised wines.",
        price_positioning="mid_range",
        authority_tier=2)
pr2a, n2a = PROD("Cataldi Madonna Cerasuolo d'Abruzzo Piè delle Vigne", "wine_still", p2a, r2, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Italy's most serious rosé; deep cherry-red with wild cherry, dark berry, dried rose and savoury mineral; almost medium-bodied with real ageing potential.",
                  price_tier="mid_range")
if n2a:
    PAIR(pr2a, "Arrosticini di pecora", "complement", "classic", "casual", "Abruzzo mutton skewers and Cerasuolo; the region's most iconic casual food-wine pairing.")
    PAIR(pr2a, "Grilled tuna with capers and olives", "complement", "established", "fish_course", "Tuna is robust enough for serious rosé; caper and olive link to Cerasuolo's dark berry.")
    PAIR(pr2a, "Grilled octopus with herbs", "complement", "established", "starter", "Adriatic octopus and Abruzzo rosé; serious seafood for serious rosé.")
    PAIR(pr2a, "Pizza with salame piccante", "complement", "established", "casual", "Spiced salami and structured rosé; Cerasuolo's cherry fruit tames the heat.")
pr2b, n2b = PROD("Masciarelli Villa Gemma Cerasuolo d'Abruzzo", "wine_still", p2b, r2, "Italy",
                  subcategory="Montepulciano d'Abruzzo",
                  description="Premium Cerasuolo with vivid cherry-red depth; ripe cherry, raspberry, violet and savoury mineral; full-bodied for a rosé with impressive length.",
                  price_tier="mid_range")
if n2b:
    PAIR(pr2b, "Pasta alla chitarra with lamb ragù", "complement", "classic", "main", "The classic Abruzzo pasta dish matches the region's finest rosé; cherry and lamb.")
    PAIR(pr2b, "Grilled sea bass with lemon and herbs", "complement", "established", "fish_course", "Full-bodied rosé handles substantial fish; Cerasuolo's fruit and mineral complement bass.")
    PAIR(pr2b, "Grilled duck sausages", "complement", "established", "casual", "Poultry sausage and Cerasuolo's cherry-dark fruit; both serious and food-driven.")
    PAIR(pr2b, "Bruschetta with tomato and anchovy", "complement", "classic", "starter", "Anchovy salinity and tomato acidity met by Cerasuolo's fruit and mineral.")

# ── REGION 3: Pecorino d'Abruzzo ─────────────────────────────────────────────
print("=== Region 3: Pecorino d'Abruzzo ===")
r3 = R("Pecorino d'Abruzzo", "Italy", "wine",
        designation_type="DOC", designation_name="Pecorino d'Abruzzo DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Abruzzo and Marche DOC producing the ancient Pecorino grape — not related to the cheese; high-acid, aromatic white with apricot, herb and mineral from mountain and coastal vineyards; rising global recognition.",
        key_producers="Tiberio, Fattoria Dezi",
        historical_context="Pecorino grape was nearly extinct; revived in the 1990s after being rediscovered by Giulio Ferretti of Offida; now one of Italy's most fashionable whites with growing international following.")
VIN(r3, 2022, "excellent", "rising", "Outstanding; Pecorino shows extraordinary aromatic concentration and mineral depth.")
VIN(r3, 2021, "very_good", "stable", "Classic expression; herbaceous citrus and mountain mineral in fine form.")
VIN(r3, 2020, "very_good", "stable", "Good vintage; consistent quality across both Abruzzo and Marche producers.")
VIN(r3, 2019, "very_good", "stable", "Warm and expressive; tropical richness balanced by natural high acidity.")
VIN(r3, 2018, "good", "stable", "Reliable vintage; clean and aromatic for easy drinking.")
p3a = P("Tiberio", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Young Abruzzo estate founded by Cristiana Tiberio; Pecorino from high-altitude Navelli plateau vineyards shows uncommon mineral intensity.",
        reputation_narrative="Tiberio's Pecorino is widely considered Abruzzo's finest; earns 95+ scores and top restaurant listings.",
        price_positioning="mid_range",
        authority_tier=2)
p3b = P("Valle Reale", "winery", r3, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Abruzzo estate in the national park; Pecorino and Trebbiano from high-altitude Popoli vineyards with clean mountain air influence.",
        reputation_narrative="Leading organic Abruzzo producer; Valle Reale Pecorino earns consistent specialist attention.",
        price_positioning="mid_range",
        authority_tier=1)
pr3a, n3a = PROD("Tiberio Pecorino d'Abruzzo Colle Vota", "wine_still", p3a, r3, "Italy",
                  subcategory="Pecorino",
                  description="Single-vineyard Navelli plateau Pecorino with apricot, Mediterranean herbs, almond and extraordinary mineral precision; one of Italy's great whites.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Grilled Adriatic sardines with lemon", "complement", "classic", "fish_course", "Adriatic fish and Abruzzo mountain white; acidity cuts the oil while herb notes bridge.")
    PAIR(pr3a, "Spaghetti alle vongole veraci", "complement", "classic", "main", "Clam pasta and Pecorino's mineral salinity; high acidity amplifies the seafood brine.")
    PAIR(pr3a, "Grilled sea bream with wild herbs", "complement", "established", "fish_course", "Delicate grill fish and complex Pecorino; mountain herb notes bridge through the wine.")
    PAIR(pr3a, "Fettuccine con tartufo nero di Norcia", "complement", "classic", "main", "Black truffle pasta and mountain Pecorino; terroir proximity creates natural harmony.")
pr3b, n3b = PROD("Valle Reale Pecorino d'Abruzzo San Calisto", "wine_still", p3b, r3, "Italy",
                  subcategory="Pecorino",
                  description="Organic national park Pecorino with floral herbs, citrus and crisp mountain mineral; clean and precise with excellent freshness.",
                  price_tier="mid_range")
if n3b:
    PAIR(pr3b, "Mozzarella di bufala fresca", "complement", "established", "starter", "Fresh dairy and crisp organic Pecorino; the wine's acidity lifts the cream.")
    PAIR(pr3b, "Steamed mussels with white wine", "complement", "classic", "starter", "Briny mussels and high-acid Pecorino; the wine in the pan mirrors the wine in the glass.")
    PAIR(pr3b, "Insalata di polpo con olive", "complement", "established", "starter", "Octopus salad with olives; Pecorino's herb and mineral notes complement the Adriatic character.")
    PAIR(pr3b, "Light pasta with cherry tomatoes and basil", "complement", "classic", "main", "Simple summer pasta with crisp Italian white; Pecorino's freshness elevates the simplicity.")

# ── REGION 4: Offida Pecorino ─────────────────────────────────────────────────
print("=== Region 4: Offida Pecorino ===")
r4 = R("Offida Pecorino", "Italy", "wine",
        designation_type="DOCG", designation_name="Offida Pecorino DOCG",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Marche DOCG near Ascoli Piceno producing 100% Pecorino whites from clay-limestone hillsides; the Marche expression of this ancient variety — richer and more textured than Abruzzo's mountain style.",
        key_producers="Fattoria Dezi, Cantine di Castignano",
        historical_context="Offida is where the Pecorino grape's modern revival began; Giulio Ferretti first isolated and commercialised it here in the 1980s; the DOCG honours Offida as the variety's spiritual home.")
VIN(r4, 2022, "very_good", "stable", "Excellent Marche vintage; Offida Pecorino shows good richness and depth.")
VIN(r4, 2021, "good", "stable", "Balanced season; Pecorino shows aromatic precision and good acidity.")
VIN(r4, 2020, "excellent", "rising", "Outstanding vintage for Marche; Offida Pecorino at its most complex.")
VIN(r4, 2019, "very_good", "stable", "Classic expression; apricot, herb and mineral in fine balance.")
VIN(r4, 2018, "good", "stable", "Reliable vintage; consistent quality from better producers.")
p4a = P("Fattoria Dezi", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Offida's leading quality estate; pioneer of the Pecorino revival in Marche; single-vineyard wines of real ambition.",
        reputation_narrative="Most respected Offida Pecorino producer; wines earn consistent top scores.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Cantine di Castignano", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Piceno cooperative producing reliable quality Offida Pecorino and Rosso Piceno; important for the region's commercial bedrock.",
        reputation_narrative="Volume benchmark for Piceno DOC and Offida DOCG; consistent and well-distributed.",
        price_positioning="value",
        authority_tier=1)
pr4a, n4a = PROD("Fattoria Dezi Offida Pecorino Superiore", "wine_still", p4a, r4, "Italy",
                  subcategory="Pecorino",
                  description="Benchmark Offida Pecorino; richer and more textured than Abruzzo equivalents; apricot, white peach, herb and mineral with substantial body and length.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Brodetto di pesce all'anconetana", "complement", "classic", "main", "Adriatic fish stew from Ancona; Offida Pecorino's richness and acidity match the complex seafood.")
    PAIR(pr4a, "Scamorza alla brace (grilled scamorza)", "complement", "established", "starter", "Smoked grilled cheese and Offida Pecorino; the wine's texture handles the rich dairy.")
    PAIR(pr4a, "Vincigrassi (Marche lasagne with offal)", "complement", "classic", "main", "Marche's festive pasta with rich offal sauce; Pecorino's body and acidity balance the richness.")
    PAIR(pr4a, "Olive all'ascolana (stuffed fried olives)", "complement", "classic", "casual", "Marche's most famous antipasto with local white; the Ascoli Piceno classic.")
pr4b, n4b = PROD("Cantine di Castignano Offida Pecorino", "wine_still", p4b, r4, "Italy",
                  subcategory="Pecorino",
                  description="Accessible Offida Pecorino with citrus, peach and herb freshness; medium-bodied and versatile.",
                  price_tier="value")
if n4b:
    PAIR(pr4b, "Pasta al forno con mozzarella e sugo", "complement", "classic", "casual", "Baked pasta with tomato and mozzarella; Pecorino's freshness cuts through the richness.")
    PAIR(pr4b, "Grilled scampi with garlic and herbs", "complement", "established", "fish_course", "Adriatic scampi and local white; herb notes bridge the shellfish sweetness.")
    PAIR(pr4b, "Fresh ricotta with local honey", "complement", "established", "dessert", "Marche ricotta and slightly sweet Pecorino finish; honey bridges both wine and cheese.")
    PAIR(pr4b, "Fritto misto all'italiana", "complement", "classic", "casual", "Mixed Italian fry-up; Pecorino's acidity cuts oil and refreshes between bites.")

# ── REGION 5: Verdicchio dei Castelli di Jesi Classico Superiore ─────────────
print("=== Region 5: Verdicchio di Matelica ===")
r5 = R("Verdicchio di Matelica", "Italy", "wine",
        designation_type="DOC", designation_name="Verdicchio di Matelica DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Inland Marche Verdicchio DOC in the mountain valley of Matelica; cooler, more structured and mineral than coastal Castelli di Jesi; considered by specialists as Verdicchio's finest expression.",
        key_producers="Bisci, Belisario",
        historical_context="Matelica's Verdicchio is the connoisseur's choice; the inland mountain valley gives more acidity, structure and mineral depth than the coastal Jesi hills; long considered superior by wine specialists despite lower commercial profile.")
VIN(r5, 2022, "very_good", "stable", "Mountain cool preserved freshness; Verdicchio shows classic bitter almond and mineral.")
VIN(r5, 2021, "good", "stable", "Cooler season; lean and precise Verdicchio with excellent mineral tension.")
VIN(r5, 2020, "excellent", "rising", "Outstanding mountain vintage; depth and complexity rarely seen in this DOC.")
VIN(r5, 2019, "very_good", "stable", "Classic Matelica expression; citrus, bitter almond and crisp mineral.")
VIN(r5, 2018, "good", "stable", "Reliable vintage; clean and mineral for early drinking.")
p5a = P("Bisci", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Multi-generational Matelica estate; the most respected voice for Verdicchio di Matelica's quality potential.",
        reputation_narrative="Vigneto Fogliano is universally considered Matelica's benchmark Verdicchio; earns national critical attention.",
        price_positioning="mid_range",
        authority_tier=2)
p5b = P("Belisario", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Matelica cooperative and the largest producer of Verdicchio di Matelica; reliable quality benchmark for the mountain DOC.",
        reputation_narrative="Consistent quality standard for the DOC; Cambrugiano Riserva earns specialist respect.",
        price_positioning="value",
        authority_tier=1)
pr5a, n5a = PROD("Bisci Verdicchio di Matelica Vigneto Fogliano", "wine_still", p5a, r5, "Italy",
                  subcategory="Verdicchio",
                  description="Single-vineyard Matelica Verdicchio of outstanding complexity; bitter almond, citrus zest, white flowers and mountain mineral with a 10+ year ageing trajectory.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Brodetto di San Benedetto (Adriatic fish stew)", "complement", "classic", "main", "Adriatic fish stew and the Marche's great white; mineral salinity and seafood complexity.")
    PAIR(pr5a, "Maccheroni al ragù di pesce", "complement", "established", "main", "Fish ragù pasta and structured Verdicchio; the wine's bitter almond holds the richness.")
    PAIR(pr5a, "Tagliatelle con tartufo bianco di Acqualagna", "complement", "classic", "main", "Marche white truffle and mountain Verdicchio; mineral and earth in remarkable proximity.")
    PAIR(pr5a, "Baccalà in bianco con patate", "complement", "established", "main", "Salt cod with potatoes; Verdicchio's mineral bitterness is the traditional Marche match.")
pr5b, n5b = PROD("Belisario Cambrugiano Verdicchio di Matelica Riserva", "wine_still", p5b, r5, "Italy",
                  subcategory="Verdicchio",
                  description="Riserva Matelica Verdicchio with more structure and depth; aged 12 months before release; bitter almond, honeyed citrus and persistent mineral.",
                  price_tier="mid_range")
if n5b:
    PAIR(pr5b, "Grilled whole sea bass with Marche olive oil", "complement", "established", "fish_course", "Noble fish and noble Marche white; olive oil bridges the wine's bitter almond finish.")
    PAIR(pr5b, "Risotto con asparagi e Parmigiano", "complement", "established", "main", "Asparagus risotto and structured Verdicchio; the bitter almond works with asparagus's vegetal note.")
    PAIR(pr5b, "Pollo alla cacciatora con olive", "complement", "classic", "main", "Hunter's chicken with olives; Verdicchio's mineral freshness balances the rich tomato sauce.")
    PAIR(pr5b, "Aged Pecorino di Macerata with walnut bread", "complement", "classic", "cheese", "Aged sheep's cheese and structured mountain Verdicchio; Marche regional harmony.")

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
