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

# ── B130 ──────────────────────────────────────────────────────────────────────
# Targets: Taurasi DOCG (Italy), Greco di Tufo DOCG (Italy),
#          Fiano di Avellino DOCG (Italy), Aglianico del Vulture DOC (Italy),
#          Vermentino di Sardegna DOC (Italy)

# 1. TAURASI DOCG — Campania, Italy
print("=== Taurasi DOCG ===")
r1 = R("Taurasi DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Taurasi DOCG",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The greatest red wine of southern Italy; the 'Barolo of the South' from Aglianico grown on volcanic and clay soils in Campania's Irpinia hills at 400-700m altitude. Aglianico ripens very late (October), building extraordinary tannin and acidity; minimum 3 years aging required (4 for riserva). Mastroberardino dominated the DOCG for generations; Antonio Caggiano and Feudi di San Gregorio modernized it.",
        key_producers="Mastroberardino, Feudi di San Gregorio, Antonio Caggiano, Donnachiara, Quintodecimo",
        historical_context="Taurasi received DOC status in 1970 and DOCG in 1993, one of southern Italy's first. Mastroberardino almost singlehandedly preserved Aglianico during the phylloxera era and post-war period. The eruption of Vesuvius in 79AD destroyed the original vineyards; the current vines are planted on different volcanic soils. 'Barolo of the South' moniker came from Italian wine authority Luigi Veronelli.")
for yr, qd, pt, sn in [
    (2018, "very_good", "rising", "Warm harvest; rich Aglianico with superb concentration; tannic backbone will need decades to resolve"),
    (2019, "excellent", "rising", "Excellent balance; Aglianico ripened perfectly in October; structured wines of great aging potential"),
    (2020, "exceptional", "rising", "Exceptional vintage; classic expression with balance of power and elegance; landmark Taurasi year"),
    (2021, "very_good", "rising", "Good ripening season; firm tannins and fresh acidity; decade-plus aging required for top wines"),
    (2022, "excellent", "stable", "Warm but late-season cooling preserved Aglianico's natural acidity; excellent concentration"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Mastroberardino", "winery", r1, "Italy",
        production_philosophy="traditional",
        philosophy_description="The historic family estate that preserved Aglianico and Greco through the phylloxera era; Radici Taurasi is the benchmark wine; 10 generations of the same family.",
        reputation_narrative="The guardian of Campanian wine heritage; Mastroberardino's Radici Taurasi rediscovered ancient Roman vineyard sites on Mount Vesuvius and showed the world Aglianico's potential.",
        price_positioning="ultra_premium")

pr1a1, n = PROD("Mastroberardino Radici Taurasi DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="Aglianico", price_tier="ultra_premium",
    description="The benchmark Taurasi; Radici (meaning 'roots') from ancient vine sites including original Vesuvius terroir; dark cherry, iron, tar, chocolate; immense tannic structure; needs 10-15 years to open.")
if n:
    PAIR(pr1a1, "Ragù alla napoletana (Neapolitan slow-cooked beef ragù)", "complement", "classic", "main", "The definitive Taurasi pairing; 8-hour ragù creates gelatin richness that tames Aglianico's ferocious tannins; iron in wine mirrors tomato")
    PAIR(pr1a1, "Slow-braised short ribs with gremolata", "complement", "established", "main", "Collagen-rich braise handles Aglianico's tannic grip; gremolata's citrus echoes wine's acidity; modern interpretation")
    PAIR(pr1a1, "Aged Pecorino Romano with quince paste", "complement", "established", "cheese", "Hard sheep cheese; Aglianico's tannin and acidity cut the fat; quince sweetness bridges; southern Italian tradition")
    PAIR(pr1a1, "Grilled Campanian lamb chops with rosemary", "complement", "classic", "main", "Regional pairing tradition; lamb fat tames Aglianico's tannin; rosemary echoes wine's herbal iron mineral character")

pr1a2, n = PROD("Mastroberardino Naturalis Historia Taurasi DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="Aglianico single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Taurasi from ancient vine parcels; more concentrated than Radici; blueberry, chocolate, volcanic mineral, tar; extraordinary aging potential of 30+ years.")
if n:
    PAIR(pr1a2, "Cinghiale (wild boar) braised with porcini and chestnuts", "complement", "classic", "main", "Only rich game with earthy mushrooms can challenge Naturalis Historia's power; chestnut echoes volcanic terroir")
    PAIR(pr1a2, "Bistecca di manzo (Fiorentina-style) with olive oil", "complement", "established", "main", "Massive beef cut; Aglianico's tannin requires equally massive protein; olive oil bridges the fruit and iron")
    PAIR(pr1a2, "Aged Caciocavallo Podolico with chestnut honey", "complement", "established", "cheese", "Rare southern Italian cow's cheese with intense flavour; only Taurasi's power matches; honey bridges tannin")
    PAIR(pr1a2, "Lamb and eggplant parmigiana", "complement", "established", "main", "Campanian classic; eggplant absorbs the wine's tannin; tomato acidity resonates; lamb weight balances")

p1b = P("Feudi di San Gregorio", "winery", r1, "Italy",
        production_philosophy="modernist",
        philosophy_description="Modern Irpinia powerhouse; collaborations with Rioja's Remirez de Ganuza and Napa Valley's consultants brought global perspective to Campanian varieties; Serpico is the flagship.",
        reputation_narrative="The producer that gave southern Italy's indigenous varieties international glamour; Feudi's investments in quality and design made Aglianico, Fiano, and Greco household names among fine wine collectors.",
        price_positioning="premium")

pr1b1, n = PROD("Feudi di San Gregorio Piano di Montevergine Taurasi Riserva", "wine_still", p1b, r1, "Italy",
    subcategory="Aglianico riserva", price_tier="ultra_premium",
    description="Flagship single-vineyard Taurasi Riserva; aged 4 years minimum; dark fruit, tar, coffee, volcanic mineral; exceptional structure and depth; needs a decade of patience.")
if n:
    PAIR(pr1b1, "Soppressata di Calabria with crusty bread", "complement", "established", "starter", "Intense southern Italian cured pork with spice; Taurasi's tannin cuts the fat; regional tradition")
    PAIR(pr1b1, "Braised oxtail alla vaccinara with pine nuts and raisins", "complement", "classic", "main", "Roman-Neapolitan classic with sweet-savoury sauce; Aglianico's tannin and acidity balance the rich offal")
    PAIR(pr1b1, "Grilled sausage with broccoli rabe", "complement", "classic", "main", "Classic Campanian combination; bitter broccoli rabe echoes wine's herbal iron; sausage fat tames tannin")
    PAIR(pr1b1, "Aged Fior di Latte with balsamic reduction", "complement", "suggested", "cheese", "Fresh mozzarella aged; Taurasi's power suits the more intense flavour; balsamic bridges the tannin")

pr1b2, n = PROD("Feudi di San Gregorio Taurasi DOCG", "wine_still", p1b, r1, "Italy",
    subcategory="Aglianico", price_tier="premium",
    description="Entry Taurasi from Feudi; accessible introduction to Aglianico's character; dark cherry, herbs, firm tannins; more approachable than the Riserva but still needs 5+ years.")
if n:
    PAIR(pr1b2, "Pizza napoletana with buffalo mozzarella and anchovies", "complement", "suggested", "main", "Unorthodox but regional; Taurasi's acidity matches tomato; anchovies' salinity cuts the tannin")
    PAIR(pr1b2, "Penne all'arrabbiata with Gaeta olives", "complement", "classic", "main", "Spicy Campanian tomato pasta; Taurasi's acidity mirrors the tomato; heat tamed by the wine's richness")
    PAIR(pr1b2, "Grilled lamb meatballs with mint and feta", "complement", "established", "main", "Lamb and Aglianico; herb seasoning echoes wine's herbal notes; feta acidity bridges")
    PAIR(pr1b2, "Ricotta-stuffed peppers baked in tomato sauce", "complement", "established", "main", "Campanian classic; ricotta's lightness balances Taurasi's power; tomato acidity echoes wine's character")

# 2. GRECO DI TUFO DOCG — Campania, Italy
print("=== Greco di Tufo DOCG ===")
r2 = R("Greco di Tufo DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Greco di Tufo DOCG",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Campanian white DOCG from the ancient Greco grape around the town of Tufo; the town name derives from the yellow tuff volcanic rock that gives the wines their distinctive mineral character. Greco is one of Italy's oldest varieties, brought by Greek colonists; produces full-bodied, oxidation-resistant whites of mineral depth with almond, citrus and volcanic earth character. DOCG since 2003.",
        key_producers="Mastroberardino, Feudi di San Gregorio, Benito Ferrara, Di Meo",
        historical_context="Greco was the primary white grape of ancient Magna Graecia; Greek colonists planted it in the 8th century BC. The DOCG was granted in 2003 recognizing the quality potential. Tufo's sulfurous tuff soils give the wines a distinctive mineral pungency unique in Italian whites. The variety has extraordinary natural resistance to oxidation.")
for yr, qd, pt, sn in [
    (2019, "very_good", "stable", "Balanced harvest; Greco shows mineral precision and almond character; good natural acidity"),
    (2020, "excellent", "rising", "Excellent ripeness with natural acidity retained; sulfurous mineral notes particularly pronounced"),
    (2021, "very_good", "rising", "Good growing season; Greco's natural structure well-expressed; wines for medium-term aging"),
    (2022, "excellent", "rising", "Ideal conditions; Greco achieved perfect phenolic ripeness while retaining volcanic mineral character"),
    (2023, "very_good", "stable", "Hot summer moderated by mountain breezes; ripe fruit with characteristic almond and tuff minerality"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Mastroberardino", "winery", r2, "Italy",
        production_philosophy="traditional",
        philosophy_description="Mastroberardino produces benchmark Greco di Tufo from old vine parcels in the historic core of the DOCG; Nova Serra single vineyard shows the variety's full potential.",
        reputation_narrative="The historic champion of Campanian whites; Mastroberardino's Greco di Tufo demonstrates the variety's natural affinity for mineral tuff soils and its extraordinary aging potential.",
        price_positioning="premium")

pr2a1, n = PROD("Mastroberardino Nova Serra Greco di Tufo", "wine_still", p2a, r2, "Italy",
    subcategory="Greco", price_tier="premium",
    description="Single-vineyard Greco from 50+ year old vines on yellow tuff soils; citrus blossom, almond, peach, volcanic mineral, sulfurous depth; full body with firm acidity; ages magnificently for 10+ years.")
if n:
    PAIR(pr2a1, "Fritto misto di mare with lemon", "complement", "classic", "starter", "Mixed fried seafood; Greco's acidity and mineral depth cut the batter; almond notes echo the fritto")
    PAIR(pr2a1, "Spaghetti alle vongole (clams in white wine)", "complement", "classic", "main", "Classic Neapolitan pasta; Greco's mineral and citrus mirror the clam brine; white wine echo in the sauce")
    PAIR(pr2a1, "Baccalà mantecato (creamed salt cod)", "complement", "classic", "main", "Salt cod's intensity needs Greco's structure; almond notes mirror the fish's richness; volcanic mineral bridges")
    PAIR(pr2a1, "Provola affumicata (smoked buffalo cheese)", "complement", "established", "cheese", "Smoked Campanian cheese; Greco's sulfurous mineral character meets the smoke; almond bridges the fat")

pr2a2, n = PROD("Mastroberardino Greco di Tufo DOCG", "wine_still", p2a, r2, "Italy",
    subcategory="Greco", price_tier="mid_range",
    description="Estate Greco di Tufo; fresh and mineral with more immediate appeal than Nova Serra; white flowers, lemon, almond, light tuff mineral; vibrant acidity; excellent food wine.")
if n:
    PAIR(pr2a2, "Grilled calamari with herbs and olive oil", "complement", "classic", "starter", "Simple squid preparation; Greco's freshness and acidity complement; almond notes echo the char")
    PAIR(pr2a2, "Risotto ai frutti di mare", "complement", "established", "main", "Mixed seafood risotto; Greco's mineral weight matches the richness; acidity cuts the butter")
    PAIR(pr2a2, "Fried zucchini blossoms stuffed with ricotta", "complement", "classic", "starter", "Campanian summer dish; Greco's freshness complements the delicate flowers; ricotta's fat balanced by acidity")
    PAIR(pr2a2, "Mozzarella di bufala with tomato and basil", "complement", "classic", "starter", "Classic Campanian insalata caprese; Greco's acidity matches the tomato; mineral depth complements the buffalo")

p2b = P("Benito Ferrara", "winery", r2, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Small family estate making some of the most mineral and terroir-pure Greco di Tufo; Vigna Cicogna single parcel demonstrates the tuff soils' extraordinary character.",
        reputation_narrative="The artisan reference for Greco di Tufo; Benito Ferrara's single-vineyard wines show how volcanic tuff soils create uniquely mineral Italian whites of great aging potential.",
        price_positioning="premium")

pr2b1, n = PROD("Benito Ferrara Vigna Cicogna Greco di Tufo", "wine_still", p2b, r2, "Italy",
    subcategory="Greco single vineyard", price_tier="premium",
    description="The reference single-vineyard Greco di Tufo; from oldest vines on deepest tuff soils; extraordinary mineral depth with beeswax, almond, sulfurous earth, citrus; landmark Campanian white.")
if n:
    PAIR(pr2b1, "Roasted langoustines with sulfurous tuff herb oil", "complement", "classic", "starter", "Luxury seafood matches Greco's weight; sulfurous tuff character finds a bridge in herb-rich oil; Campanian luxury")
    PAIR(pr2b1, "Grilled swordfish with caper and olive sauce", "complement", "classic", "fish_course", "Mediterranean swordfish with brine; Greco's mineral depth matches; almond and caper echo in both wine and sauce")
    PAIR(pr2b1, "Aged Pecorino Carmasciano with honey", "complement", "established", "cheese", "Rare Irpinian sheep cheese; Greco's acidity cuts the fat; mineral depth complements the aged character")
    PAIR(pr2b1, "Zuppa di pesce (Campanian fish soup)", "complement", "established", "main", "Rich fish stew with tomato and herbs; Greco's structure handles the complexity; acidity lifts the tomato base")

pr2b2, n = PROD("Benito Ferrara Greco di Tufo DOCG", "wine_still", p2b, r2, "Italy",
    subcategory="Greco", price_tier="mid_range",
    description="Estate Greco di Tufo; excellent value expression of the variety's mineral character; white peach, almond, tuff mineral; crisp acidity; reliable food-friendly white.")
if n:
    PAIR(pr2b2, "Antipasto di mare (seafood antipasto)", "complement", "classic", "starter", "Mixed seafood antipasto; Greco's freshness refreshes between bites; mineral depth echoes the ocean")
    PAIR(pr2b2, "Pasta e fagioli (pasta with beans)", "complement", "established", "main", "Hearty Campanian bean pasta; Greco's acidity cuts through the thickness; earthy bean flavour bridges with mineral")
    PAIR(pr2b2, "Caponata siciliana with grilled bread", "bridge", "suggested", "starter", "Sweet-sour eggplant dish; Greco's acidity mirrors the capers and vinegar; mineral depth grounds the sweetness")
    PAIR(pr2b2, "Grilled octopus with lemon and parsley", "complement", "classic", "main", "Classic southern Italian preparation; Greco's mineral freshness cuts the octopus; citrus mirrors lemon")

# 3. FIANO DI AVELLINO DOCG — Campania, Italy
print("=== Fiano di Avellino DOCG ===")
r3 = R("Fiano di Avellino DOCG", "Italy", "wine",
        designation_type="DOCG",
        designation_name="Fiano di Avellino DOCG",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Campanian white DOCG from the ancient Fiano grape in the Avellino hills; one of Italy's most fascinating white wines with honeyed, complex character that develops magnificently over 5-15 years. Fiano's DNA traces to ancient Roman 'Apianum' (bee wine) due to its honeyed character attracting bees. Volcanic and limestone soils at 500-700m altitude give the wines mineral backbone to age. DOCG since 2003.",
        key_producers="Mastroberardino, Feudi di San Gregorio, Colli di Lapio, Quintodecimo",
        historical_context="Fiano was described by Roman authors Columella and Virgil as Apianum. Nearly extinct by the 1980s when only a few families maintained it, Mastroberardino revived commercial production. The DOCG was awarded in 2003. The variety's extraordinary aging potential (rivaling white Burgundy at its best) has attracted growing collector interest. Quintodecimo's Exultet (€100+) is now one of Italy's most sought-after whites.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Excellent vintage; Fiano shows complex honeyed depth with fine mineral backbone; will age 15+ years"),
    (2020, "very_good", "rising", "Good balance; Fiano's natural complexity well-expressed; hazelnut and honeysuckle character"),
    (2021, "excellent", "rising", "Ideal growing season; Fiano developed extraordinary aromatic complexity and mineral structure"),
    (2022, "very_good", "stable", "Hot summer; Fiano's natural oxidation resistance preserved freshness; rich and textured"),
    (2023, "excellent", "rising", "Mountain breezes preserved acidity; Fiano shows pristine aromatics and fine mineral character"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Colli di Lapio", "winery", r3, "Italy",
        production_philosophy="traditional",
        philosophy_description="Clelia Romano's estate producing arguably the purest expression of Fiano di Avellino; old vines on limestone and volcanic soils at 600m; no oak, indigenous yeasts; wines that age like white Burgundy.",
        reputation_narrative="The artisan benchmark for Fiano di Avellino; Clelia Romano's pure, unoaked approach reveals Fiano's natural complexity and extraordinary aging potential; frequently cited as Italy's greatest white wine producer.",
        price_positioning="premium")

pr3a1, n = PROD("Colli di Lapio Fiano di Avellino DOCG", "wine_still", p3a, r3, "Italy",
    subcategory="Fiano", price_tier="premium",
    description="The reference unoaked Fiano from limestone and volcanic soils at 600m; honeysuckle, hazelnut, white truffle, smoke, citrus; extraordinary texture and mineral precision; transforms over 10-15 years in bottle.")
if n:
    PAIR(pr3a1, "Risotto al tartufo bianco (white truffle risotto)", "complement", "classic", "main", "Fiano's truffle and hazelnut notes echo the white truffle; the wine's texture matches risotto's richness; Campanian luxury")
    PAIR(pr3a1, "Pan-seared Dover sole with brown butter and capers", "complement", "classic", "fish_course", "Delicate fish with buttery richness; Fiano's texture and hazelnut complement; caper acidity mirrors wine's brightness")
    PAIR(pr3a1, "Aged Cacio e Pepe pasta", "complement", "established", "main", "Roman classic; Fiano's texture handles the pecorino fat; pepper's heat echoes wine's mineral smoke")
    PAIR(pr3a1, "Grilled langoustines with fresh herbs", "complement", "classic", "starter", "Luxury shellfish; Fiano's mineral complexity frames langoustine sweetness; herbs echo wine's botanical depth")

pr3a2, n = PROD("Colli di Lapio Fiano di Avellino Riserva", "wine_still", p3a, r3, "Italy",
    subcategory="Fiano riserva", price_tier="ultra_premium",
    description="Riserva Fiano from oldest vines; aged for 2 years before release; deeper oxidative complexity; beeswax, roasted hazelnut, smoke, iodine mineral; one of Italy's most age-worthy whites.")
if n:
    PAIR(pr3a2, "Lobster bisque with cream and tarragon", "complement", "classic", "starter", "Rich bisque weight; Fiano Riserva's texture and hazelnut complement the cream; tarragon's herbs echo wine's botanical notes")
    PAIR(pr3a2, "Roasted white asparagus with hollandaise and truffle", "complement", "classic", "starter", "Fiano's natural affinity for asparagus and truffle; hollandaise's richness balanced by wine's acidity")
    PAIR(pr3a2, "Aged Provolone del Monaco with mostarda", "complement", "established", "cheese", "Strong Campanian cheese with pungent depth; Fiano Riserva's complexity and age handle it; mostarda bridges")
    PAIR(pr3a2, "Pasta alla Norma with aged ricotta salata", "complement", "established", "main", "Sicilian classic; Fiano's smoke notes echo the eggplant char; aged cheese's saltiness balanced by acidity")

p3b = P("Feudi di San Gregorio", "winery", r3, "Italy",
        production_philosophy="modernist",
        philosophy_description="Feudi's Fiano di Avellino wines show the modern face of Campanian whites; Pietracalda is the single-vineyard expression.",
        reputation_narrative="Key producer making Fiano accessible globally; Feudi's Pietracalda single-vineyard demonstrates the variety's mineral depth from the best Avellino hill sites.",
        price_positioning="premium")

pr3b1, n = PROD("Feudi di San Gregorio Pietracalda Fiano di Avellino", "wine_still", p3b, r3, "Italy",
    subcategory="Fiano single vineyard", price_tier="premium",
    description="Single-vineyard Fiano from Pietracalda site; honeysuckle, peach, hazelnut, volcanic mineral; fuller body and greater depth than the estate wine; ages beautifully for 5-10 years.")
if n:
    PAIR(pr3b1, "Gnocchi alla sorrentina with tomato and mozzarella", "complement", "established", "main", "Campanian classic; Fiano's freshness cuts the tomato acidity; mozzarella fat balanced by the wine's structure")
    PAIR(pr3b1, "Spaghetti al limone with prawns", "complement", "classic", "main", "Citrus pasta; Fiano's honeyed citrus character mirrors the lemon; prawn sweetness enhanced by the wine")
    PAIR(pr3b1, "Grilled sea bass with fennel and orange", "complement", "classic", "fish_course", "Fiano's botanical complexity matches fennel and orange; delicate fish elevated by the wine's depth")
    PAIR(pr3b1, "Burrata with roasted cherry tomatoes and basil", "complement", "classic", "starter", "Campanian summer classic; Fiano's freshness and slight fatness mirrors the burrata; basil echoes botanical notes")

pr3b2, n = PROD("Feudi di San Gregorio Fiano di Avellino DOCG", "wine_still", p3b, r3, "Italy",
    subcategory="Fiano", price_tier="mid_range",
    description="Estate Fiano di Avellino; approachable and versatile; honeysuckle, peach, light hazelnut, citrus; good acidity; excellent introduction to the variety.")
if n:
    PAIR(pr3b2, "Insalata di polpo (octopus salad with celery and olives)", "complement", "classic", "starter", "Southern Italian octopus salad; Fiano's mineral freshness echoes the olive brine; celery mirrors the wine's herbal note")
    PAIR(pr3b2, "Orecchiette with broccoli rabe and anchovies", "complement", "established", "main", "Pugliese classic; bitter broccoli rabe matches Fiano's mineral depth; anchovy salinity refreshed by acidity")
    PAIR(pr3b2, "Mozzarella in carrozza (fried mozzarella)", "complement", "established", "starter", "Fried Campanian cheese sandwich; Fiano's acidity cuts the fat; mineral freshness refreshes")
    PAIR(pr3b2, "Grilled swordfish with sicilian caponata", "complement", "established", "main", "Mediterranean fish with sweet-sour vegetable; Fiano's structure handles the caponata's complexity")

# 4. AGLIANICO DEL VULTURE DOC — Basilicata, Italy
print("=== Aglianico del Vulture DOC ===")
r4 = R("Aglianico del Vulture DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Aglianico del Vulture DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Basilicata's principal red wine appellation on the volcanic slopes of Monte Vulture at 400-700m altitude; Aglianico grown on ancient volcanic ash soils produces wines of extraordinary mineral depth, iron and dark fruit character. Often compared favourably to Barolo; the volcanic terroir adds a distinctive mineral pungency. Superiore and Riserva require extended aging; the region's isolation preserved authentic Aglianico. DOC since 1971.",
        key_producers="Paternoster, Elena Fucci, D'Angelo, Basilisco",
        historical_context="Monte Vulture is an extinct volcano whose ancient ash soils create unique conditions for Aglianico. The region received DOC in 1971 but remained obscure; Elena Fucci's single-vineyard Titolo brought international attention in the 2000s. The isolation of Basilicata (Italy's poorest region) preserved traditional farming; most vineyards are organically farmed by default. The nearby Matera UNESCO site adds cultural tourism driving wine interest.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Warm harvest on volcanic slopes; Aglianico achieved full ripeness; volcanic mineral character pronounced"),
    (2019, "very_good", "rising", "Good balance; late-ripening Aglianico showed complexity with firm tannin structure"),
    (2020, "exceptional", "rising", "Exceptional vintage; Monte Vulture Aglianico at its best; landmark wines for the DOC"),
    (2021, "excellent", "rising", "Ideal conditions; volcanic mineral character perfectly integrated; wines of great elegance and structure"),
    (2022, "very_good", "stable", "Good growing season; Aglianico's natural acid preserved; firm mineral-driven wines"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Elena Fucci", "winery", r4, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Elena Fucci produces one wine only — Titolo — from a single volcanic parcel; organic farming; indigenous yeasts; the Aglianico del Vulture that put Basilicata on the world wine map.",
        reputation_narrative="Italy's most celebrated 'one wine' producer; Elena Fucci's Titolo from volcanic Monte Vulture soils is consistently rated among Italy's greatest reds and changed the world's perception of southern Italian wine.",
        price_positioning="ultra_premium")

pr4a1, n = PROD("Elena Fucci Titolo Aglianico del Vulture", "wine_still", p4a, r4, "Italy",
    subcategory="Aglianico single vineyard", price_tier="ultra_premium",
    description="Single-vineyard Aglianico from volcanic Monte Vulture soils; dark cherry, iron, volcanic ash mineral, dried violet; immense but elegant structure; benchmark wine of Basilicata and one of Italy's greatest reds.")
if n:
    PAIR(pr4a1, "Agnello alla lucana (Basilicata lamb with peperoni cruschi)", "complement", "classic", "main", "The definitive Basilicata pairing; local lamb with crispy dried peppers; Aglianico's volcanic mineral mirrors the terroir")
    PAIR(pr4a1, "Braised oxtail with peperoni cruschi and potatoes", "complement", "established", "main", "Basilicata mountain tradition; rich offal tames Titolo's tannin; dried pepper's subtle heat echoes wine's iron")
    PAIR(pr4a1, "Aged Canestrato di Moliterno with walnut", "complement", "established", "cheese", "Basilicata's aged sheep cheese; Aglianico's power handles the pungency; walnut bridges wine's mineral depth")
    PAIR(pr4a1, "Cinghiale slow-braised with wild herbs and volcanic mineral salts", "complement", "classic", "main", "Wild boar from Vulture slopes; volcanic mineral in both food and wine; herbs echo Aglianico's complexity")

pr4a2, n = PROD("Elena Fucci Titolo Aglianico del Vulture Superiore", "wine_still", p4a, r4, "Italy",
    subcategory="Aglianico superiore", price_tier="ultra_premium",
    description="Superiore version of Titolo with longer aging; even greater concentration and depth; dark chocolate, volcanic iron, tar, dried cherry; requires 10+ years to show its full potential.")
if n:
    PAIR(pr4a2, "Filetto di manzo with truffle and aged Parmigiano", "complement", "classic", "main", "Premium beef with truffle; Titolo Superiore's depth handles the luxury ingredients; iron in wine echoes truffle's earthiness")
    PAIR(pr4a2, "Slow-roasted leg of lamb with wild herbs", "complement", "established", "main", "Hours of roasting creates intensity that matches Superiore's power; volcanic herbs echo the wine's complexity")
    PAIR(pr4a2, "Aged Pecorino di Filiano with truffle honey", "complement", "established", "cheese", "Basilicata's prestigious aged sheep cheese; Superiore's power and depth match; truffle honey bridges")
    PAIR(pr4a2, "Ribollita with Tuscan bread and black cabbage", "contrast", "suggested", "main", "Hearty vegetable stew; unexpected pairing but wine's power handles the dense rustic dish; earthy connection")

p4b = P("Paternoster", "winery", r4, "Italy",
        production_philosophy="traditional",
        philosophy_description="The historic Vulture producer maintaining traditional winemaking for Don Anselmo; founded 1925; one of Basilicata's oldest and most respected estates.",
        reputation_narrative="The traditional benchmark for Aglianico del Vulture; Paternoster's Don Anselmo demonstrates how long aging reveals the volcanic terroir's mineral depth; a century of winemaking on Monte Vulture.",
        price_positioning="premium")

pr4b1, n = PROD("Paternoster Don Anselmo Aglianico del Vulture", "wine_still", p4b, r4, "Italy",
    subcategory="Aglianico riserva", price_tier="ultra_premium",
    description="Top cuvée from Paternoster; named for the founder; aged in large Slovenian oak barrels; dark fruit, volcanic mineral, leather, tobacco; great structure; benchmark for the DOC's traditional style.")
if n:
    PAIR(pr4b1, "Ragù della domenica (Sunday meat ragù) with handmade pasta", "complement", "classic", "main", "Southern Italian Sunday tradition; slow-cooked meat creates the richness to handle Don Anselmo's power")
    PAIR(pr4b1, "Braised lamb shanks with tomato and rosemary", "complement", "classic", "main", "Lamb and Aglianico is the Basilicata tradition; rosemary echoes wine's herbal iron mineral character")
    PAIR(pr4b1, "Aged Caciocavallo Podolico with mostarda di fichi", "complement", "established", "cheese", "Rare southern Italian aged cheese; Don Anselmo's tannin handles the intensity; fig mostarda bridges")
    PAIR(pr4b1, "Porcini mushroom risotto with aged Parmigiano", "complement", "established", "main", "Earthy porcini echoes Aglianico's mineral depth; risotto richness tamed by tannin; Parmigiano bridges")

pr4b2, n = PROD("Paternoster Rotondo Aglianico del Vulture", "wine_still", p4b, r4, "Italy",
    subcategory="Aglianico", price_tier="mid_range",
    description="Entry Paternoster Aglianico; more approachable than Don Anselmo; red-dark cherry, herbs, volcanic mineral; good tannin structure; excellent introduction to the appellation's character.")
if n:
    PAIR(pr4b2, "Sausage and lentil stew with smoked paprika", "complement", "established", "main", "Earthy stew; Aglianico's mineral iron notes bridge with lentil earthiness; paprika echoes wine's volcanic character")
    PAIR(pr4b2, "Pasta al ragù with local sausage", "complement", "classic", "main", "Classic southern Italian meat pasta; Aglianico's acidity lifts the rich ragù; regional tradition")
    PAIR(pr4b2, "Grilled lamb kofta with herb yoghurt", "complement", "established", "main", "Middle Eastern preparation; Aglianico's mineral freshness suits the herbs; yoghurt bridges tannin")
    PAIR(pr4b2, "Aged Mozzarella di bufala with tomatoes", "complement", "established", "starter", "Campanian classic; Aglianico's freshness at this level suits buffalo milk; regional connection")

# 5. VERMENTINO DI SARDEGNA DOC — Sardinia, Italy
print("=== Vermentino di Sardegna DOC ===")
r5 = R("Vermentino di Sardegna DOC", "Italy", "wine",
        designation_type="DOC",
        designation_name="Vermentino di Sardegna DOC",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Sardinia's signature white wine from the Vermentino grape; granite and schist soils across the island produce aromatic, mineral whites with citrus, almond, Mediterranean herbs and sea-breeze character. The best wines come from Gallura in the northeast (which has its own DOCG) but the island-wide DOC produces excellent quality. Vermentino thrives in Sardinia's Mediterranean climate, producing fuller-bodied whites than on the Ligurian coast.",
        key_producers="Sella & Mosca, Capichera, Tenute Olbios, Argiolas",
        historical_context="Vermentino arrived in Sardinia from Spain via Corsica during the Aragonese period (14th-15th century). It adapted perfectly to the island's granite soils and Mediterranean climate. The DOC was established in 1988. Sardinian Vermentino is distinct from Ligurian Vermentino — the island's heat and granite give wines a fuller body and more pronounced mineral character. Capichera in Gallura produces Sardinia's most prestigious Vermentino.")
for yr, qd, pt, sn in [
    (2019, "very_good", "stable", "Classic Sardinian conditions; Vermentino shows crisp citrus and sea-breeze mineral; bright and food-friendly"),
    (2020, "excellent", "rising", "Excellent balance; granite soils delivered mineral precision; almond and citrus blossom fully expressed"),
    (2021, "very_good", "stable", "Good growing season; Mediterranean sea breezes preserved freshness; aromatic and food-friendly"),
    (2022, "excellent", "rising", "Ideal ripening; Vermentino's natural aromatics enhanced by cool nights; complex with fine acidity"),
    (2023, "very_good", "stable", "Warm summer moderated by island breezes; ripe aromatic Vermentino with characteristic bitter almond finish"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Capichera", "winery", r5, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="The prestige Gallura estate producing Sardinia's finest Vermentino from old granite-rooted vines; Capichera's barrel-fermented Vendemmia Tardiva shows the grape's extraordinary aging potential.",
        reputation_narrative="The reference for Sardinian Vermentino at the highest level; Capichera's old-vine Gallura wines rival white Burgundy in depth and show that Vermentino can age for 10+ years.",
        price_positioning="ultra_premium")

pr5a1, n = PROD("Capichera Vermentino di Gallura DOCG", "wine_still", p5a, r5, "Italy",
    subcategory="Vermentino Gallura", price_tier="ultra_premium",
    description="Flagship Vermentino from old vines on granite soils in Gallura; citrus blossom, white peach, almond, saline granite mineral; full body, rich texture; one of Italy's great whites; ages 10+ years.")
if n:
    PAIR(pr5a1, "Aragosta alla catalana (Sardinian lobster salad)", "complement", "classic", "main", "The definitive Sardinian pairing; lobster's sweetness enhanced by Capichera's richness; tomato and onion bridge")
    PAIR(pr5a1, "Bottarga di muggine (grey mullet roe) on pasta", "complement", "classic", "starter", "Sardinia's signature cured roe; Vermentino's mineral depth and almond notes complement the concentrated umami")
    PAIR(pr5a1, "Grilled dentice (dentex fish) with herbs", "complement", "classic", "fish_course", "Mediterranean sea fish; Capichera's weight and mineral match the meaty dentex; herbs echo wine's botanical notes")
    PAIR(pr5a1, "Aged Pecorino Sardo with Sardinian honey", "complement", "established", "cheese", "Island sheep cheese; Vermentino's almond and citrus balance the fat; local honey bridges to wine's sweetness")

pr5a2, n = PROD("Capichera Assajé Vermentino di Sardegna", "wine_still", p5a, r5, "Italy",
    subcategory="Vermentino", price_tier="premium",
    description="Entry Capichera Vermentino; fresh and aromatic with citrus, white flowers, almond; medium body; excellent everyday Sardinian white showing the estate's signature mineral precision.")
if n:
    PAIR(pr5a2, "Malloreddus with Sardinian sausage ragù", "bridge", "established", "main", "Sardinian pasta with pork ragù; unexpected but traditional; Vermentino's freshness cuts the richness")
    PAIR(pr5a2, "Clams steamed with Sardinian vernaccia", "complement", "classic", "starter", "Coastal shellfish with island wine; Vermentino's sea-breeze mineral matches brine; herb notes echo the vernaccia")
    PAIR(pr5a2, "Grilled sea bream with lemon and capers", "complement", "classic", "fish_course", "Classic Mediterranean fish; Assajé's freshness and citrus suit perfectly; capers bridge with mineral notes")
    PAIR(pr5a2, "Pane carasau with lardo and rosemary honey", "complement", "established", "starter", "Traditional Sardinian crispy bread; lardo's fat balanced by Vermentino's acidity; rosemary echoes botanical notes")

p5b = P("Sella & Mosca", "winery", r5, "Italy",
        production_philosophy="terroir_driven",
        philosophy_description="Sardinia's largest wine estate near Alghero; historic estate producing Vermentino and Cannonau; La Cala is the flagship accessible Vermentino.",
        reputation_narrative="The ambassador for Sardinian wine globally; Sella & Mosca's scale and quality have made Vermentino di Sardegna recognizable worldwide; the benchmark for accessible island wine.",
        price_positioning="mid_range")

pr5b1, n = PROD("Sella & Mosca La Cala Vermentino di Sardegna", "wine_still", p5b, r5, "Italy",
    subcategory="Vermentino", price_tier="mid_range",
    description="The benchmark accessible Sardinian Vermentino; fresh citrus, white flowers, light almond, sea salt; crisp acidity; iconic food-wine of the island; consistently excellent value.")
if n:
    PAIR(pr5b1, "Fritto misto with anchovy and zucchini", "complement", "classic", "starter", "Sardinian coastal fried mix; Vermentino's crisp acidity cuts the batter; sea salt mineral echoes the seafood")
    PAIR(pr5b1, "Grilled prawns with garlic and parsley", "complement", "classic", "starter", "Simple Mediterranean preparation; Vermentino's citrus and almond complement prawn sweetness; herbs bridge")
    PAIR(pr5b1, "Pecorino Sardo fresco with olives and almonds", "complement", "established", "starter", "Sardinian aperitivo spread; Vermentino's freshness refreshes between bites; almond in both wine and nuts")
    PAIR(pr5b1, "Tuna tartare with Sardinian citrus", "complement", "established", "starter", "Fresh tuna; Vermentino's citrus mineral character frames the fish; island connection in every element")

pr5b2, n = PROD("Sella & Mosca Terre Bianche Torbato Sardegna", "wine_still", p5b, r5, "Italy",
    subcategory="Torbato", price_tier="mid_range",
    description="Rare Torbato grape from Alghero; nearly extinct Spanish variety revived by Sella & Mosca; citrus, white flowers, almond, light smoke; crisp Sardinian white of unique character.")
if n:
    PAIR(pr5b2, "Impanadas (Sardinian meat pies)", "complement", "established", "starter", "Traditional Sardinian pastry; Torbato's crispness cuts through; almond notes echo the meat filling's warmth")
    PAIR(pr5b2, "Grilled calamari with herb oil", "complement", "classic", "starter", "Mediterranean squid; Torbato's freshness and mineral notes complement; citrus mirrors the lemon in the dish")
    PAIR(pr5b2, "Clam chowder Sardinian style", "complement", "suggested", "main", "Rich creamy clam; Torbato's acidity lifts the cream; mineral notes echo the brine")
    PAIR(pr5b2, "Ligurian pesto pasta with green beans and potato", "complement", "suggested", "main", "Classic Ligurian combination; Torbato's botanical notes echo basil; almond in wine echoes pesto's pine nuts")

# ── Summary ───────────────────────────────────────────────────────────────────
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
print("B130 complete.")
conn.close()
