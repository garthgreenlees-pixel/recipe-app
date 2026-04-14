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

# ── REGION 1: Taurasi DOCG (Italy/Campania) ─────────────────────────────────
print("\n=== Region 1: Taurasi ===")
r1 = R("Taurasi", "Italy", "wine",
    designation_type="DOCG", designation_name="Taurasi DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Taurasi is Italy's most celebrated southern red wine, produced from Aglianico in the volcanic Irpinia hills of Campania. Known as the 'Barolo of the South', it demands long aging — minimum 3 years with 12 months in oak — and rewards patience with extraordinary complexity: tar, violets, dark cherry, leather, and mineral depth. The volcanic soils and altitude (400-700m) give a freshness that sets it apart from other southern Italian reds.",
    key_producers="Mastroberardino, Feudi di San Gregorio, Antonio Caggiano, Contrade di Taurasi",
    historical_context="Aglianico has been cultivated in Campania since Greek colonisation, and Taurasi has been considered the region's finest red since at least the 19th century. Mastroberardino's modernisation of the DOCG from the 1960s was fundamental to its international recognition. Taurasi received DOCG status in 1993.")

VIN(r1, 2022, "excellent", "rising", "Outstanding vintage for Aglianico; exceptional ripeness with dense tannins and great aging structure")
VIN(r1, 2021, "very_good", "stable", "Fine balanced year with classic Taurasi structure; firm tannins and concentrated dark fruit")
VIN(r1, 2020, "excellent", "rising", "Hot year producing powerful, concentrated Aglianico with excellent longevity potential")
VIN(r1, 2019, "very_good", "stable", "Benchmark vintage with fine tannin ripeness; tar and violet character beautifully expressed")
VIN(r1, 2018, "good", "stable", "More accessible vintage; tannins softening earlier than usual with good typicity")

prod1a_id = P("Mastroberardino", "Italy", r1, "winery",
    "The historic benchmark of Campanian wine; Mastroberardino's Taurasi Radici is the reference wine for the DOCG — powerful, age-worthy, and deeply expressive of the Aglianico variety and volcanic Irpinia terroir.")
prod1a, new1a = PROD("Mastroberardino Taurasi Radici", "wine_still", prod1a_id, r1, "Italy",
    subcategory="red", price_tier="premium",
    description="The Taurasi benchmark: single-vineyard Aglianico from the Radici estate, aged minimum 4 years before release. Tar, violet, dark cherry, leather, and volcanic mineral depth. Requires a decade of cellaring to begin revealing its full potential.")
if new1a:
    PAIR(prod1a, "Braised wild boar with Aglianico reduction and black truffle", "complement", "classic", "main",
        "Taurasi's tannic power and iron mineral depth meet their match in wild boar; Aglianico in the sauce creates perfect unity")
    PAIR(prod1a, "Grilled Fassona beef tagliata with rocket and Parmigiano", "complement", "classic", "main",
        "Premium beef's iron richness meets Aglianico's tannin and volcanic mineral precision; rocket bitterness refreshes between sips")
    PAIR(prod1a, "Aged Caciocavallo Podolico with black truffle honey", "bridge", "classic", "cheese",
        "Campanian cave-aged cheese with truffle honey bridges Taurasi's volcanic minerality and dark fruit through textural harmony")
    PAIR(prod1a, "Lamb abbacchio alla romana with artichokes and mint", "complement", "established", "main",
        "Young Roman lamb's delicate gaminess pairs with Taurasi's violet-tar complexity; artichoke bitterness meets the wine's mineral edge")

prod1b_id = P("Antonio Caggiano", "Italy", r1, "winery",
    "One of Taurasi's most acclaimed modern producers; Antonio Caggiano crafts powerful, polished Aglianico from prime Irpinia sites, combining traditional structure with modern precision to produce Taurasi of exceptional depth.")
prod1b, new1b = PROD("Caggiano Taurasi Vigna Macchia dei Goti", "wine_still", prod1b_id, r1, "Italy",
    subcategory="red", price_tier="premium",
    description="Caggiano's flagship single-vineyard Taurasi from Macchia dei Goti; concentrated and powerful Aglianico with extraordinary tannic depth, dark cherry, tar, violets, and 20+ year aging potential. A modern benchmark for the DOCG.")
if new1b:
    PAIR(prod1b, "Slow-roasted porchetta with wild fennel, rosemary, and garlic", "complement", "established", "main",
        "Pork belly's fat richness with aromatic herbs is tamed by Taurasi's firm tannin; fennel adds anise notes that complement the wine's tar")
    PAIR(prod1b, "Pasta al ragù napoletano (Sunday gravy) with meatballs", "complement", "classic", "main",
        "The Campanian Sunday table centrepiece: Neapolitan ragù's deep meat sauce and Taurasi are the region's great pairing")
    PAIR(prod1b, "Grilled lamb chops with rosemary, olives, and lemon", "complement", "established", "main",
        "Lamb's fat is structured by Taurasi's tannin; olive's savouriness mirrors the wine's mineral depth while lemon lifts the finish")
    PAIR(prod1b, "Smoked Scamorza with speck and roasted red peppers", "bridge", "established", "starter",
        "Smoked cheese and cured meat create layers of savouriness that bridge Taurasi's complexity; roasted pepper sweetness balances the tannin")

# ── REGION 2: Vermentino di Gallura DOCG (Italy/Sardinia) ──────────────────
print("\n=== Region 2: Vermentino di Gallura ===")
r2 = R("Vermentino di Gallura", "Italy", "wine",
    designation_type="DOCG", designation_name="Vermentino di Gallura DOCG",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Vermentino di Gallura is Sardinia's only white wine DOCG, produced from Vermentino grown on the granite soils of northern Sardinia's Gallura region. The wines show intense aromatic character — white flowers, citrus peel, peach, and bitter almond — with a distinctive saline bitterness and mineral freshness that reflect both the granite terroir and the Mediterranean sea breeze.",
    key_producers="Sella e Mosca, Capichera, CS Gallura, Masone Mannu",
    historical_context="Vermentino was likely introduced to Sardinia by traders from the Ligurian coast or Iberian Peninsula centuries ago. The Gallura DOCG, established in 1996, was the first DOCG in Sardinia, recognising the northern granite region's unique capacity to produce Vermentino of exceptional complexity compared to lighter styles from other Italian growing areas.")

VIN(r2, 2023, "excellent", "stable", "Outstanding aromatic freshness; saline mineral character and white flower intensity at peak expression")
VIN(r2, 2022, "very_good", "stable", "Rich and full vintage with excellent Vermentino depth; bitter almond and peach well developed")
VIN(r2, 2021, "good", "stable", "Elegant year with fine acidity and mineral definition; leaner style with authentic Gallura typicity")
VIN(r2, 2020, "very_good", "stable", "Strong vintage; aromatic concentration with granite mineral character prominent")
VIN(r2, 2019, "excellent", "rising", "Benchmark Gallura vintage; textbook Vermentino with white flowers, citrus peel, and saline bitter finish")

prod2a_id = P("Capichera", "Italy", r2, "winery",
    "The most prestigious Vermentino di Gallura producer; the Ragnedda family's estate crafts the appellation's benchmark wine — rich, complex, and capable of aging 5-10 years, shattering the notion that Vermentino is merely a simple aromatic white.")
prod2a, new2a = PROD("Capichera Vermentino di Gallura", "wine_still", prod2a_id, r2, "Italy",
    subcategory="white", price_tier="premium",
    description="The benchmark Vermentino di Gallura: old vines from Capichera's granite estate, partially aged in large oak. Intense white flower, peach, and bitter almond aromatics with extraordinary mineral depth and saline length. Defies the appellation's simple reputation.")
if new2a:
    PAIR(prod2a, "Grilled branzino with capers, lemon, and Sardinian olive oil", "complement", "classic", "fish_course",
        "Mediterranean sea bass from the same island terroir; caper's brine and lemon mirror Vermentino's saline bitter finish")
    PAIR(prod2a, "Bottarga di muggine shaved over pasta with olive oil and parsley", "complement", "classic", "starter",
        "Bottarga's intense sea umami amplifies Vermentino's mineral saline character; a Sardinian terroir unity")
    PAIR(prod2a, "Suckling pig (Porceddu) with myrtle and Sardinian herbs", "complement", "classic", "main",
        "Sardinia's iconic celebratory roast with myrtle — the island's defining aromatic herb — bridges perfectly to Vermentino's floral complexity")
    PAIR(prod2a, "Burrata with fresh sea urchin and Sicilian capers", "complement", "established", "starter",
        "Sea urchin's intense marine sweetness and dairy creaminess are anchored by Vermentino's saline mineral structure")

prod2b_id = P("CS Gallura", "Italy", r2, "winery",
    "The Gallura cooperative — Cantina Sociale di Gallura — producing the most widely available and accessible expressions of Vermentino di Gallura DOCG; their Canayli label is a benchmark for the region's fresh, vibrant style.")
prod2b, new2b = PROD("CS Gallura Canayli Vermentino di Gallura", "wine_still", prod2b_id, r2, "Italy",
    subcategory="white", price_tier="mid_range",
    description="The accessible benchmark Vermentino di Gallura from the Gallura cooperative's Canayli label; citrus freshness, white flowers, and mineral saline precision. The reference for everyday Sardinian white wine at honest prices.")
if new2b:
    PAIR(prod2b, "Fresh clams with white wine, garlic, and chilli over spaghetti", "complement", "classic", "main",
        "Clam's natural brine and saline character echo Vermentino's mineral finish; garlic and chilli add aromatic depth")
    PAIR(prod2b, "Pecorino Sardo fresco with Sardinian honey and carasau bread", "complement", "classic", "cheese",
        "Fresh Sardinian sheep cheese and the island's floral honey are natural vehicles for Vermentino's aromatic character")
    PAIR(prod2b, "Grilled prawns marinated with lemon, herbs, and Sardinian olive oil", "complement", "classic", "starter",
        "Prawn sweetness and herb aromatics are a natural match for Vermentino's floral freshness and saline bite")
    PAIR(prod2b, "Arancini di riso with saffron and Pecorino", "complement", "established", "casual",
        "Saffron's exotic spice and Pecorino's salt echo Vermentino's bitter-saline character; a relaxed island bar snack pairing")

# ── REGION 3: Falanghina del Sannio DOC (Italy/Campania) ───────────────────
print("\n=== Region 3: Falanghina del Sannio ===")
r3 = R("Falanghina del Sannio", "Italy", "wine",
    designation_type="DOC", designation_name="Falanghina del Sannio DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Falanghina del Sannio produces wines from one of Italy's oldest grape varieties, cultivated in the Sannio hills of Campania. Falanghina was likely the grape behind Falernian wine — antiquity's most celebrated wine. The modern dry whites show floral aromatics, ripe citrus, stone fruit, and a refreshing mineral finish. Versatile and food-friendly.",
    key_producers="Mastroberardino, Feudi di San Gregorio, Fontanavecchia, La Rivolta",
    historical_context="Falanghina is thought to derive from 'falange' (stake) — the ancient vine-training post used in the Campania Felice. The grape is likely related to the legendary Falernian wine of ancient Rome, cited by Pliny and Horace. After centuries of obscurity, Falanghina was revived in the 1990s and has become one of Italy's most planted white varieties.")

VIN(r3, 2023, "very_good", "stable", "Excellent aromatic freshness; floral and citrus character well expressed with clean acidity")
VIN(r3, 2022, "excellent", "rising", "Full and concentrated vintage; stone fruit depth and mineral complexity at best in years")
VIN(r3, 2021, "good", "stable", "Cooler year with more restrained aromatics but fine acidity and good varietal character")
VIN(r3, 2020, "very_good", "stable", "Strong vintage with good Falanghina aromatic concentration; balanced and food-friendly")
VIN(r3, 2019, "excellent", "rising", "Outstanding vintage; benchmark Falanghina with textbook floral, citrus, and stone fruit profile")

prod3a_id = P("Fontanavecchia", "Italy", r3, "winery",
    "One of Sannio's most dedicated Falanghina specialists; Orazio Rillo's estate focuses almost entirely on the native variety, producing wines that show the grape's full range from fresh and immediate to structured and age-worthy.")
prod3a, new3a = PROD("Fontanavecchia Falanghina del Sannio", "wine_still", prod3a_id, r3, "Italy",
    subcategory="white", price_tier="mid_range",
    description="The Fontanavecchia benchmark Falanghina: fresh and aromatic with white peach, lemon blossom, and mineral finish. Unoaked and immediate, this expresses the variety's natural freshness and food-friendly versatility.")
if new3a:
    PAIR(prod3a, "Caprese salad with buffalo mozzarella, San Marzano tomatoes, and basil", "complement", "classic", "starter",
        "Campanian buffalo mozzarella and Falanghina share the same geographical heritage; tomato acidity meets the wine's citrus freshness")
    PAIR(prod3a, "Zuppa di frutti di mare with chilli and garlic", "complement", "classic", "main",
        "Mixed seafood soup's brine and spice are brightened by Falanghina's lemon freshness and mineral finish")
    PAIR(prod3a, "Grilled orata (gilt-head bream) with lemon and wild herbs", "complement", "classic", "fish_course",
        "Delicate white fish with lemon and herbs is the quintessential Campanian fish pairing for fresh, unoaked Falanghina")
    PAIR(prod3a, "Bruschetta al pomodoro with local olive oil and sea salt", "complement", "classic", "aperitif",
        "The simplest Campanian apéritif — ripe tomato on toasted bread — perfectly matched by Falanghina's refreshing floral character")

prod3b_id = P("La Rivolta", "Italy", r3, "winery",
    "A biodynamic pioneer in Sannio producing serious, terroir-driven Falanghina alongside Aglianico; their Falanghina shows what extended aging can bring to the variety — unexpected depth, honeyed complexity, and mineral structure.")
prod3b, new3b = PROD("La Rivolta Falanghina del Sannio Taburno", "wine_still", prod3b_id, r3, "Italy",
    subcategory="white", price_tier="mid_range",
    description="Biodynamic Falanghina from the Taburno hills in Sannio; more structured and mineral than typical expressions, with white peach, hazelnut, and a persistent saline finish. Shows what the variety can achieve with serious winemaking attention.")
if new3b:
    PAIR(prod3b, "Linguine con astice (lobster linguine) with tomato, chilli, and parsley", "complement", "established", "main",
        "Lobster's sweetness and tomato acidity are elevated by Falanghina's stone fruit richness; structured Taburno version holds up to the dish's weight")
    PAIR(prod3b, "Ricotta-stuffed zucchini flowers with anchovy sauce", "complement", "established", "starter",
        "Delicate ricotta with savoury anchovy creates a balance of richness and brine that Falanghina's mineral freshness completes")
    PAIR(prod3b, "Vitello alla pizzaiola with olives, capers, and tomatoes", "complement", "classic", "main",
        "The Neapolitan veal classic with its Mediterranean sauce is a natural vehicle for structured Falanghina's mineral acidity")
    PAIR(prod3b, "Lemon tart with candied citrus and meringue", "contrast", "adventurous", "dessert",
        "Dessert's sweetness and sharp lemon are balanced against a dry Falanghina in a citrus echo with contrasting sweetness levels")

# ── REGION 4: Primitivo di Manduria DOCG (Italy/Puglia) ────────────────────
print("\n=== Region 4: Primitivo di Manduria ===")
r4 = R("Primitivo di Manduria", "Italy", "wine",
    designation_type="DOCG", designation_name="Primitivo di Manduria DOCG",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Primitivo di Manduria produces Puglia's most celebrated red from the Primitivo grape — genetically identical to California's Zinfandel — grown on the Ionian coast of the Salento peninsula. The wines are rich, powerful, and intensely fruited with ripe dark berry, dried fig, chocolate, and spice. Both dry and Dolce Naturale (naturally sweet) styles are produced.",
    key_producers="Gianfranco Fino, Pervini (Armentino), Felline, Varvaglione",
    historical_context="Primitivo arrived in Puglia from Croatia (as Crljenak Kaštelanski or Tribidrag) centuries ago. DNA analysis in 2001 confirmed its genetic identity to Zinfandel, sparking international interest. Primitivo di Manduria received DOC in 1974 and DOCG for the Dolce Naturale style in 2011, recognising the Salento's special capacity for producing intense, sun-ripened reds.")

VIN(r4, 2023, "very_good", "stable", "Good vintage with typical Primitivo richness; dark fruit intensity with balanced alcohol and good structure")
VIN(r4, 2022, "excellent", "rising", "Outstanding Salento vintage; exceptional concentration, dark fruit depth, and impressive tannic structure")
VIN(r4, 2021, "good", "stable", "Slightly cooler year; more balanced style with better freshness and elegance than typical hot vintages")
VIN(r4, 2020, "excellent", "rising", "Hot year producing densely concentrated Primitivo; powerful and age-worthy with dark chocolate depth")
VIN(r4, 2019, "very_good", "stable", "Classic vintage with excellent varietal typicity; dried fig, chocolate, and Mediterranean spice well expressed")

prod4a_id = P("Gianfranco Fino", "Italy", r4, "winery",
    "The cult producer of Primitivo di Manduria; his single-vineyard Es from 60-80 year old bush vines is the DOCG's most sought-after and expensive wine, achieving Barolo-level prices. Fino transformed the reputation of Manduria from bulk to prestige.")
prod4a, new4a = PROD("Gianfranco Fino Es Primitivo di Manduria", "wine_still", prod4a_id, r4, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="The cult Primitivo: single-vineyard Es from 60-80 year old alberello (bush-trained) Primitivo vines. Extraordinary concentration — dark cherry jam, dried fig, cacao, Mediterranean spice — with surprising freshness and structure for the variety. 100 Parker points in exceptional years.")
if new4a:
    PAIR(prod4a, "Slow-braised oxtail with dark chocolate, orange, and juniper", "complement", "classic", "main",
        "Oxtail's rich gelatinous depth meets Es Primitivo's fruit intensity; dark chocolate echoes the wine's cacao and amplifies the savoury-sweet register")
    PAIR(prod4a, "Wagyu beef short rib with truffle polenta and bone marrow jus", "complement", "adventurous", "main",
        "Extreme fat richness from both Wagyu and bone marrow meets Es's tannic power; truffle amplifies the wine's earthy Mediterranean depth")
    PAIR(prod4a, "Aged Canestrato Pugliese with cherry mostarda", "bridge", "classic", "cheese",
        "Pugliese aged sheep cheese with cherry preserve bridges Primitivo's dark fruit intensity; a Salento regional classic")
    PAIR(prod4a, "Dark chocolate fondant with espresso and sea salt caramel", "complement", "adventurous", "dessert",
        "Dark chocolate's bitterness echoes the wine's cacao notes; sea salt amplifies the fruit and the espresso deepens the savoury register")

prod4b_id = P("Felline", "Italy", r4, "winery",
    "One of Manduria's most respected artisan producers; Gregory Perrucci's Felline estate produces honest, terroir-faithful Primitivo that balances the variety's natural richness with freshness and aging capability without reaching cult prices.")
prod4b, new4b = PROD("Felline Primitivo di Manduria", "wine_still", prod4b_id, r4, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Felline's benchmark Primitivo di Manduria: dark berry fruit, dried fig, chocolate, and Mediterranean herb complexity from old bush-trained vines. Richer and more concentrated than many peers but retaining excellent drinkability without excessive heat.")
if new4b:
    PAIR(prod4b, "Lamb spiedini with Pugliese herbs, fresh ricotta, and grilled vegetables", "complement", "classic", "main",
        "Grilled lamb skewers with fresh ricotta are a Pugliese speciality that meets Primitivo's dark fruit and tannic depth")
    PAIR(prod4b, "Pizza with nduja sausage, smoked mozzarella, and roasted peppers", "complement", "established", "casual",
        "Spicy nduja's heat and richness are tamed by Primitivo's fruit sweetness; smoked mozzarella adds depth to echo the wine's body")
    PAIR(prod4b, "Orecchiette with broccoli rabe, anchovies, and chilli", "complement", "established", "main",
        "Puglia's iconic pasta with the region's wine: broccoli rabe's bitterness and anchovy's umami are bridged by Primitivo's dark fruit")
    PAIR(prod4b, "Grilled sausages with roasted peppers and caponata", "complement", "classic", "main",
        "Southern Italian sausage with Primitivo is a straightforward regional pairing; sweet peppers and caponata balance the wine's richness")

# ── REGION 5: Vino Nobile di Montepulciano DOCG (Italy/Tuscany) ────────────
print("\n=== Region 5: Vino Nobile di Montepulciano ===")
r5 = R("Vino Nobile di Montepulciano", "Italy", "wine",
    designation_type="DOCG", designation_name="Vino Nobile di Montepulciano DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Vino Nobile di Montepulciano is one of Tuscany's most historic DOCGs, produced from Prugnolo Gentile (a Sangiovese clone) in the hilltop town of Montepulciano. The wines occupy a quality tier between Chianti Classico and Brunello di Montalcino — sharing Sangiovese's cherry, herb, and earthy complexity with a distinctive floral lift. The elevated site (250-600m) and unique soils provide elegance that distinguishes it from its Sienese neighbours.",
    key_producers="Avignonesi, Poliziano, Contucci, Boscarelli",
    historical_context="Montepulciano has been producing wine since at least the 14th century. Francesco Redi's 1685 poem 'Bacco in Toscana' praised it as 'king of all wines'. It was among Italy's first DOCGs (1980), predating even Brunello's DOCG elevation. Formerly blended with white grapes, the DOCG moved to 100% red variety production in 2010, significantly improving quality.")

VIN(r5, 2022, "excellent", "rising", "Outstanding Tuscan vintage; benchmark Vino Nobile with excellent concentration and classical structure")
VIN(r5, 2021, "very_good", "stable", "Fine balanced year with elegant, aromatic Prugnolo Gentile; less concentration but beautiful finesse")
VIN(r5, 2020, "excellent", "rising", "Hot year with powerful, deeply concentrated Vino Nobile; tannic and age-worthy")
VIN(r5, 2019, "very_good", "stable", "Classic Montepulciano vintage with fine Sangiovese typicity; cherry, herb, and earthy depth in harmony")
VIN(r5, 2018, "good", "stable", "More approachable vintage; good Prugnolo Gentile character with earlier drinking pleasure")

prod5a_id = P("Poliziano", "Italy", r5, "winery",
    "One of Vino Nobile's most celebrated and ambitious estates; Federico Carletti has elevated Poliziano to international prestige with a range spanning from elegant entry-level Rosso di Montepulciano to the legendary Asinone single-vineyard DOCG.")
prod5a, new5a = PROD("Poliziano Vino Nobile di Montepulciano", "wine_still", prod5a_id, r5, "Italy",
    subcategory="red", price_tier="premium",
    description="Poliziano's benchmark Vino Nobile: Prugnolo Gentile from prime Montepulciano sites aged 2 years in large Slavonian oak. Classic Sangiovese profile — cherry, violet, leather, herb — with the estate's signature elegance and mineral precision.")
if new5a:
    PAIR(prod5a, "Bistecca alla fiorentina with rosemary salt and Tuscan olive oil", "complement", "classic", "main",
        "The great Tuscan pairing: Florence-cut T-bone with Sangiovese-based wine; beef's iron and char meet the wine's acidity and cherry depth")
    PAIR(prod5a, "Pappardelle with wild boar ragù and fresh Pecorino", "complement", "classic", "main",
        "Wild boar ragù is the quintessential Tuscan pasta for Sangiovese-based wines; Pecorino's saline depth adds complexity")
    PAIR(prod5a, "Aged Pecorino di Pienza with fig preserve and walnuts", "bridge", "classic", "cheese",
        "The regional sheep cheese from Pienza (adjacent to Montepulciano) with fig preserves bridges Vino Nobile's cherry and earthy depth")
    PAIR(prod5a, "Roasted pigeon with black olive, sage, and Vin Santo glaze", "complement", "established", "main",
        "Game bird's earthy richness and olive savouriness meet Prugnolo Gentile's mineral complexity; Vin Santo glaze adds Tuscan sweetness")

prod5b_id = P("Boscarelli", "Italy", r5, "winery",
    "A historic family estate producing some of Vino Nobile's most precise and elegant expressions; the De Ferrari family's Boscarelli is consistently among Montepulciano's finest, with the Nocio dei Boscarelli single-vineyard among the DOCG's most celebrated wines.")
prod5b, new5b = PROD("Boscarelli Vino Nobile di Montepulciano", "wine_still", prod5b_id, r5, "Italy",
    subcategory="red", price_tier="premium",
    description="Boscarelli's flagship Vino Nobile: elegant Prugnolo Gentile with fine cherry and violet aromatics, earthy complexity, and vibrant Sangiovese acidity. Among the DOCG's most consistent and refined expressions — approachable in youth but structured to age gracefully.")
if new5b:
    PAIR(prod5b, "Cinghiale (wild boar) stew with juniper, rosemary, and red wine", "complement", "classic", "main",
        "Wild boar slow-cooked with Tuscan aromatics is the natural partner for Vino Nobile's earthy complexity and cherry fruit")
    PAIR(prod5b, "Chicken liver crostini with capers and anchovies", "complement", "classic", "starter",
        "The Tuscan antipasto classic — fegato on bread — matches Prugnolo Gentile's acidity with the liver's richness; caper brine amplifies the wine's mineral edge")
    PAIR(prod5b, "Ribollita (Tuscan bread soup with cannellini beans and cavolo nero)", "complement", "classic", "main",
        "Rustic Tuscan peasant soup with Vino Nobile is the hilltown classic; the soup's earthiness and beans meet the wine's mineral acidity")
    PAIR(prod5b, "Grilled lamb chops with rosemary, garlic, and salsa verde", "complement", "established", "main",
        "Lamb's delicate gaminess and herb salsa verde are natural partners for Prugnolo Gentile's violet-cherry character and mineral length")

# ── Summary ──────────────────────────────────────────────────────────────────
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
conn.close()
