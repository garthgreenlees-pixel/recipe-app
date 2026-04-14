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

# ── REGION 1: Colli Orientali del Friuli (already as Friuli Colli Orientali) ─
# Check and target fresh regions

print("=== Region 1: Valtellina Superiore ===")
r1 = R("Valtellina Superiore", "Italy", "wine",
        designation_type="DOCG", designation_name="Valtellina Superiore DOCG",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="High-altitude Alpine DOCG in Lombardy producing Nebbiolo (locally Chiavennasca) on dramatic south-facing terraced schist cliffs above the Adda river; produces five named crus including Sassella, Grumello, Inferno, Valgella and Maroggia.",
        key_producers="Arpepe, Rainoldi, Nino Negri",
        historical_context="Valtellina's terraced vineyards were carved by hand from solid rock; Nebbiolo here shows Alpine elegance — far more delicate than Barolo; nearly abandoned in the 20th century but revived by passionate artisans.")
VIN(r1, 2022, "very_good", "stable", "Warm summer; Nebbiolo shows excellent ripeness with refined tannins.")
VIN(r1, 2021, "good", "stable", "Cool Alpine year; wines lean and elegant with characteristic floral lift.")
VIN(r1, 2020, "excellent", "rising", "Outstanding vintage; concentration and complexity rival Barolo at fraction of price.")
VIN(r1, 2019, "very_good", "stable", "Classic Valtellina; roses, tar and Alpine herbs with fine structure.")
VIN(r1, 2018, "very_good", "stable", "Good ripeness; accessible tannins and long fruit-driven finish.")
p1a = P("Arpepe", "winery", r1, "Italy",
        production_philosophy="traditional",
        philosophy_description="Three-generation family estate using only indigenous Chiavennasca from estate-owned Sassella terraces; very long ageing in large Slavonian oak.",
        reputation_narrative="The definitive voice of Valtellina Superiore; Arpepe's Riservas age for decades and rank among Italy's great reds.",
        price_positioning="premium",
        authority_tier=2)
p1b = P("Rainoldi", "winery", r1, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic Valtellina estate producing all five cru designations with emphasis on single-vineyard character and Alpine freshness.",
        reputation_narrative="Highly respected across all five crus; Rainoldi's wines offer the best overview of Valtellina's terroir diversity.",
        price_positioning="mid_range",
        authority_tier=2)
pr1a, n1a = PROD("Arpepe Valtellina Superiore Sassella Rocce Rosse Riserva", "wine_still", p1a, r1, "Italy",
                  subcategory="Nebbiolo (Chiavennasca)",
                  description="Flagship Sassella cru Riserva aged 7+ years; extraordinary depth of dried rose, tar, mineral and Alpine herbs; fragile power unique to this terroir.",
                  price_tier="premium")
if n1a:
    PAIR(pr1a, "Bresaola della Valtellina with oil and lemon", "complement", "classic", "starter", "Regional cured beef with regional wine; the lean mineral red and air-dried beef are inseparable.")
    PAIR(pr1a, "Slow-braised venison with polenta", "complement", "classic", "main", "Alpine game and Alpine Nebbiolo; polenta bridges the rusticity while wine lifts the richness.")
    PAIR(pr1a, "Aged Bitto DOP cheese", "complement", "classic", "cheese", "Valtellina's great aged cheese with its great red wine; alpine herbs in both.")
    PAIR(pr1a, "Risotto with wild mushrooms and speck", "complement", "established", "main", "Earthy mushroom and smoked speck met by Nebbiolo's tar and roses; mountain harmony.")
pr1b, n1b = PROD("Rainoldi Valtellina Superiore Inferno", "wine_still", p1b, r1, "Italy",
                  subcategory="Nebbiolo (Chiavennasca)",
                  description="Inferno cru Valtellina with dark cherry, rose petal, iron mineral and firm Alpine tannins; medium-bodied with excellent ageing potential.",
                  price_tier="mid_range")
if n1b:
    PAIR(pr1b, "Pizzoccheri (buckwheat pasta with cabbage)", "complement", "classic", "main", "Valtellina's signature buckwheat pasta dish with Valtellina's signature wine; regional canon.")
    PAIR(pr1b, "Roast lamb with rosemary and garlic", "complement", "established", "main", "Nebbiolo's structure and lamb's richness; Alpine herbs in wine and on plate.")
    PAIR(pr1b, "Wild boar ragù with pappardelle", "complement", "established", "main", "Gamey wild boar needs tannin and acidity; Valtellina Nebbiolo delivers both.")
    PAIR(pr1b, "Grilled rabbit with polenta and herbs", "complement", "established", "main", "Delicate game and delicate Alpine Nebbiolo; polenta softens while wine adds complexity.")

print("=== Region 2: Sforzato di Valtellina ===")
r2 = R("Sforzato di Valtellina", "Italy", "wine",
        designation_type="DOCG", designation_name="Sforzato di Valtellina DOCG",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Rare Alpine DOCG producing passito-method Nebbiolo (Chiavennasca) dried on racks for 90+ days; resulting wine is 14%+ alcohol with extraordinary dried fruit, tar and iron concentration.",
        key_producers="Nino Negri, Mamete Prevostini",
        historical_context="Sforzato (sfursat in dialect) has Alpine origins as a warming high-calorie wine for mountain workers; elevated to DOCG in 2003; now a collector's wine rivalling Amarone in power.")
VIN(r2, 2022, "very_good", "stable", "Warm base vintage yielded excellent fruit for drying; complex Sforzato expected.")
VIN(r2, 2021, "good", "stable", "Drying process compensated for cooler season; elegant expressions.")
VIN(r2, 2020, "excellent", "rising", "Outstanding base material; exceptional dried fruit concentration and complexity.")
VIN(r2, 2019, "very_good", "stable", "Ripe and generous; Sforzato shows characteristic dried plum and tar.")
VIN(r2, 2018, "very_good", "stable", "Strong vintage for the passito style; rich and structured.")
p2a = P("Nino Negri", "winery", r2, "Italy",
        production_philosophy="traditional",
        philosophy_description="The largest and most historically important Valtellina producer; Sfursat 5 Stelle is the appellation's most celebrated wine.",
        reputation_narrative="Nino Negri's 5 Stelle is universally regarded as the benchmark Sforzato; regularly scores 95+ in international press.",
        price_positioning="premium",
        authority_tier=2)
p2b = P("Mamete Prevostini", "winery", r2, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Artisan Valtellina producer of growing reputation; Corte di Cama single-vineyard Sforzato gaining collector attention.",
        reputation_narrative="Rising star of Valtellina; earns consistent top marks for honest, site-specific wines.",
        price_positioning="premium",
        authority_tier=1)
pr2a, n2a = PROD("Nino Negri Sfursat 5 Stelle Sforzato di Valtellina", "wine_still", p2a, r2, "Italy",
                  subcategory="Nebbiolo (Chiavennasca) passito",
                  description="Benchmark Sforzato with extraordinary dried fruit concentration; dark plum, dried roses, tar, iron and a 30+ year ageing horizon.",
                  price_tier="premium")
if n2a:
    PAIR(pr2a, "Aged Castelmagno cheese with honey", "complement", "classic", "cheese", "Powerful aged cheese meets powerful dried-grape wine; honey bridges sweetness and intensity.")
    PAIR(pr2a, "Slow-braised wild boar with polenta", "complement", "classic", "main", "Rich game requires powerful wine; Sforzato's concentration stands up to wild boar perfectly.")
    PAIR(pr2a, "Dark chocolate fondant", "complement", "established", "dessert", "Bitter dark chocolate with dried-fruit intensity; tannin and cocoa in parallel.")
    PAIR(pr2a, "Beef shin osso buco with gremolata", "complement", "established", "main", "Collagen-rich slow braise needs full-bodied red; Sforzato power elevated by gremolata brightness.")
pr2b, n2b = PROD("Mamete Prevostini Corte di Cama Sforzato di Valtellina", "wine_still", p2b, r2, "Italy",
                  subcategory="Nebbiolo (Chiavennasca) passito",
                  description="Single-vineyard artisan Sforzato with complexity and precision; dried cherry, alpine herbs and iron with remarkable freshness for the style.",
                  price_tier="premium")
if n2b:
    PAIR(pr2b, "Venison medallions with juniper sauce", "complement", "classic", "main", "Alpine game and Alpine passito; juniper in the sauce echoes alpine herbs in the wine.")
    PAIR(pr2b, "Braised short rib with root vegetables", "complement", "established", "main", "Collagen-rich slow braise elevated by Sforzato's dried fruit intensity.")
    PAIR(pr2b, "Gorgonzola with walnut bread", "complement", "established", "cheese", "Blue cheese pungency met by Sforzato's fruit concentration; walnut bitterness links the two.")
    PAIR(pr2b, "Dark fruit tarte tatin", "complement", "suggested", "dessert", "Caramelised dark fruit echoes the passito drying character; bitter pastry balances the sweetness.")

print("=== Region 3: Valdichiana ===")
r3 = R("Valdichiana", "Italy", "wine",
        designation_type="DOC", designation_name="Valdichiana Toscana DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Tuscan DOC in the Chiana valley between Arezzo and Siena; produces Sangiovese-based reds, Trebbiano and Chardonnay whites; quality rising rapidly as Tuscany's overlooked inland alternative.",
        key_producers="Il Conventino, Tenuta il Corno",
        historical_context="Historically a source of bulk Trebbiano for blending; rising ambition from local producers focusing on Sangiovese and indigenous whites to compete with more famous Tuscan appellations.")
VIN(r3, 2022, "very_good", "stable", "Warm Tuscan vintage; Sangiovese shows excellent ripeness and ruby intensity.")
VIN(r3, 2021, "good", "stable", "Cooler season; lean reds with good acidity and lighter colour.")
VIN(r3, 2020, "very_good", "stable", "Classic Tuscan vintage; balanced and expressive across all varieties.")
VIN(r3, 2019, "very_good", "stable", "Warm and generous; Sangiovese shows deep fruit and fine tannin.")
VIN(r3, 2018, "good", "stable", "Solid vintage; accessible wines for earlier drinking.")
p3a = P("Il Conventino di Monteciello", "winery", r3, "Italy",
        production_philosophy="organic",
        philosophy_description="Organic Valdichiana estate producing serious Sangiovese and indigenous whites from converted monastery vineyards; pioneer of quality ambition in the DOC.",
        reputation_narrative="Leading voice for Valdichiana's quality potential; earns attention from Tuscan wine specialists.",
        price_positioning="mid_range",
        authority_tier=1)
p3b = P("Tenuta il Corno", "winery", r3, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Estate-grown Valdichiana reds and whites with emphasis on approachable Sangiovese and fresh Trebbiano for everyday Tuscan dining.",
        reputation_narrative="Reliable quality producer; benchmark for the DOC's accessible tier.",
        price_positioning="value",
        authority_tier=1)
pr3a, n3a = PROD("Il Conventino Valdichiana Sangiovese", "wine_still", p3a, r3, "Italy",
                  subcategory="Sangiovese",
                  description="Organic Valdichiana Sangiovese with cherry, dried herbs and Tuscan earth; medium-bodied with good structure and food-friendly acidity.",
                  price_tier="mid_range")
if n3a:
    PAIR(pr3a, "Bistecca alla Fiorentina", "complement", "classic", "main", "Tuscany's canonical steak pairing with Sangiovese; charred meat and cherry-herb acidity in harmony.")
    PAIR(pr3a, "Wild boar cinta senese ragù", "complement", "classic", "main", "Tuscan native pork breed in ragù; Sangiovese acidity and tannin balance the rich game.")
    PAIR(pr3a, "Pecorino di Pienza with chestnut honey", "complement", "classic", "cheese", "Sheep's cheese and Sangiovese is Tuscany's classic cheese pairing.")
    PAIR(pr3a, "Ribollita (Tuscan bread and bean stew)", "complement", "classic", "casual", "Hearty Tuscan peasant dish with local Sangiovese; the wine's acidity cuts through the richness.")
pr3b, n3b = PROD("Tenuta il Corno Valdichiana Trebbiano Toscano", "wine_still", p3b, r3, "Italy",
                  subcategory="Trebbiano Toscano",
                  description="Fresh, light Trebbiano with lemon, white flowers and a neutral mineral finish; everyday Tuscan white for simple seafood and antipasto.",
                  price_tier="value")
if n3b:
    PAIR(pr3b, "Crostini toscani with chicken liver pâté", "complement", "established", "starter", "Classic Tuscan antipasto with local white; liver richness balanced by Trebbiano's freshness.")
    PAIR(pr3b, "Grilled branzino with capers and lemon", "complement", "established", "fish_course", "Simple grilled sea bass lifted by Trebbiano's light citrus freshness.")
    PAIR(pr3b, "Fresh pasta with butter and sage", "complement", "classic", "main", "Simple pasta dish and neutral Trebbiano; sage bridges the herb character.")
    PAIR(pr3b, "Light vegetable soup (minestrone)", "complement", "classic", "casual", "Everyday Tuscan table wine for everyday Tuscan food; honest and reliable.")

print("=== Region 4: Morellino di Scansano ===")
r4 = R("Morellino di Scansano", "Italy", "wine",
        designation_type="DOCG", designation_name="Morellino di Scansano DOCG",
        reputation_tier="respected",
        quality_trajectory="established",
        description="Maremma coastal DOCG producing approachable, fruit-forward Sangiovese (Morellino) with Mediterranean warmth; softer tannins and richer fruit than inland Chianti.",
        key_producers="Erik Banti, Fattoria Le Pupille",
        historical_context="Morellino (local Sangiovese clone) has been grown on Maremma's coastal hills since Roman times; the appellation rose to prominence in the 1990s as Maremma became Tuscany's quality frontier.")
VIN(r4, 2022, "very_good", "stable", "Mediterranean warmth; dark cherry richness and Mediterranean herbs well expressed.")
VIN(r4, 2021, "good", "stable", "Slightly cooler; wines show more acidity and less colour than usual but elegant.")
VIN(r4, 2020, "excellent", "rising", "Outstanding; Morellino at peak ripeness — plum, dark cherry and garrigue.")
VIN(r4, 2019, "very_good", "stable", "Classic Maremma expression; generous fruit and soft tannins.")
VIN(r4, 2018, "good", "stable", "Good everyday drinking; approachable and aromatic.")
p4a = P("Erik Banti", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Leading Morellino producer combining modern winemaking with Maremma's coastal warmth; wide range from entry to premium.",
        reputation_narrative="Most widely distributed Morellino producer internationally; benchmark for the appellation.",
        price_positioning="mid_range",
        authority_tier=2)
p4b = P("Fattoria Le Pupille", "winery", r4, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Prestigious Maremma estate producing both Morellino and the renowned super-Tuscan Saffredi; pioneer of premium Maremma wine.",
        reputation_narrative="Le Pupille's Saffredi is one of Tuscany's great reds; Morellino Poggio Valente is a benchmark DOCG wine.",
        price_positioning="premium",
        authority_tier=2)
pr4a, n4a = PROD("Erik Banti Morellino di Scansano Ciabatta", "wine_still", p4a, r4, "Italy",
                  subcategory="Sangiovese (Morellino)",
                  description="Ripe and accessible Morellino with dark cherry, Mediterranean herbs, leather and a soft tannic finish; great value Maremma expression.",
                  price_tier="mid_range")
if n4a:
    PAIR(pr4a, "Wild boar sausage with polenta", "complement", "classic", "main", "Maremma hunting tradition; wild boar and Morellino is the regional classic.")
    PAIR(pr4a, "Grilled lamb chops with rosemary", "complement", "established", "main", "Mediterranean herbs and Morellino cherry fruit; rosemary bridges wine and plate.")
    PAIR(pr4a, "Pasta all'Amatriciana", "complement", "classic", "main", "Guanciale and tomato richness balanced by Sangiovese acidity; Italian canon.")
    PAIR(pr4a, "Cured meats with fig jam", "complement", "classic", "casual", "Mediterranean charcuterie and Morellino; fig sweetness bridges wine's dried fruit notes.")
pr4b, n4b = PROD("Fattoria Le Pupille Morellino di Scansano Poggio Valente", "wine_still", p4b, r4, "Italy",
                  subcategory="Sangiovese (Morellino)",
                  description="Single-vineyard Morellino of real depth; concentrated dark cherry, leather, Mediterranean scrub and fine tannins; Maremma at its most ambitious.",
                  price_tier="premium")
if n4b:
    PAIR(pr4b, "Slow-braised wild boar with pappardelle", "complement", "classic", "main", "The great Maremma pairing; the region's wild boar hunts and the DOC's finest red.")
    PAIR(pr4b, "Grilled bistecca with Chianina beef", "complement", "classic", "main", "Tuscan beef and Tuscan Sangiovese; Le Pupille's structure matches the meat's richness.")
    PAIR(pr4b, "Pecorino stagionato with truffle honey", "complement", "classic", "cheese", "Aged Tuscan sheep's cheese with premium Morellino; regional terroir harmony.")
    PAIR(pr4b, "Rabbit cacciatore with olives", "complement", "established", "main", "Hunter's rabbit stew with Mediterranean herbs mirrors wine's garrigue character.")

print("=== Region 5: Pitigliano ===")
r5 = R("Pitigliano", "Italy", "wine",
        designation_type="DOC", designation_name="Pitigliano DOC",
        reputation_tier="overlooked",
        quality_trajectory="emerging",
        description="Southern Maremma DOC near the dramatic tuff stone town of Pitigliano; produces Trebbiano-based whites with volcanic mineral character from ancient tuff soils; unique and underrated.",
        key_producers="Il Tufo Rosso, Cantina Cooperativa di Pitigliano",
        historical_context="Pitigliano's ancient Jewish community historically produced kosher wine here; the tuff volcanic soils give a mineral signature unlike anything else in Tuscany; still largely undiscovered.")
VIN(r5, 2022, "very_good", "stable", "Volcanic soils retain freshness even in warm years; mineral precision excellent.")
VIN(r5, 2021, "good", "stable", "Aromatic and crisp; tuff minerality well expressed in cooler conditions.")
VIN(r5, 2020, "very_good", "stable", "Good concentration and length; best Pitigliano in recent years.")
VIN(r5, 2019, "good", "stable", "Pleasant and food-friendly; reliable everyday white.")
VIN(r5, 2018, "good", "stable", "Warm vintage; slightly less mineral precision but good fresh drinking.")
p5a = P("Il Tufo Rosso", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Artisan Pitigliano producer emphasising the ancient tuff terroir; small-production wines with genuine volcanic mineral character.",
        reputation_narrative="Pioneer of quality ambition in Pitigliano; wines appear in Maremma specialist selections.",
        price_positioning="mid_range",
        authority_tier=1)
p5b = P("Cantina Cooperativa di Pitigliano", "winery", r5, "Italy",
        production_philosophy="terroir_expression",
        philosophy_description="Historic cooperative ensuring the continuation of traditional Pitigliano white wine production from the tuff plateau vineyards.",
        reputation_narrative="Volume benchmark for the DOC; reliable and affordable expressions of Pitigliano's unique terroir.",
        price_positioning="value",
        authority_tier=1)
pr5a, n5a = PROD("Il Tufo Rosso Pitigliano Superiore Bianco", "wine_still", p5a, r5, "Italy",
                  subcategory="Trebbiano Toscano",
                  description="Volcanic tuff Pitigliano white with distinctive mineral salinity, citrus and white flowers; unusually structured for a Trebbiano-based wine.",
                  price_tier="mid_range")
if n5a:
    PAIR(pr5a, "Acquacotta (Maremma vegetable soup)", "complement", "classic", "casual", "Regional Maremma peasant soup with local white wine; the tuff mineral character elevates simplicity.")
    PAIR(pr5a, "Grilled orata (sea bream) whole", "complement", "established", "fish_course", "Coastal Maremma fish and inland mineral white; tuff volcanic character mirrors the sea mineral.")
    PAIR(pr5a, "Pecorino fresco with crudités", "complement", "established", "starter", "Fresh sheep's cheese and mineral white; simple and expressive regional match.")
    PAIR(pr5a, "Crostini with local black truffle", "complement", "classic", "starter", "Maremma truffle on bread with the region's mineral white; volcanic terroir complements earthy truffle.")
pr5b, n5b = PROD("Cantina di Pitigliano Bianco di Pitigliano", "wine_still", p5b, r5, "Italy",
                  subcategory="Trebbiano Toscano",
                  description="Light, fresh cooperative Pitigliano white; delicate citrus and white flower; easy-drinking table wine with mineral undertone.",
                  price_tier="value")
if n5b:
    PAIR(pr5b, "Light pasta with clam sauce (vongole)", "complement", "classic", "main", "Everyday Italian pairing; white wine in both the sauce and the glass.")
    PAIR(pr5b, "Fritto misto di mare", "complement", "classic", "casual", "Fried mixed seafood cleaned by the wine's light acidity; Tuscan coastal tradition.")
    PAIR(pr5b, "Bruschetta with fresh tomato and basil", "complement", "classic", "casual", "Simple antipasto and simple local white; honest Tuscan table pleasure.")
    PAIR(pr5b, "Light vegetable frittata", "complement", "established", "casual", "Egg dish loves a neutral, fresh Italian white; Pitigliano's mineral note adds interest.")

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
