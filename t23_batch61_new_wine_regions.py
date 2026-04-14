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

# ── REGION 1: Côte Rôtie AOC (France/Rhône) ────────────────────────────────
print("\n=== Region 1: Côte Rôtie ===")
r1 = R("Côte Rôtie", "France", "wine",
    designation_type="AOC", designation_name="Côte Rôtie AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Côte Rôtie ('roasted slope') is one of the world's most prestigious Syrah appellations, carved into vertiginous granite terraces above the Rhône at Ampuis. Syrah — here often co-fermented with up to 20% Viognier — produces wines of extraordinary perfume, finesse, and complexity: violet, olive tapenade, smoked meat, and mineral depth. The legendary Landonne, Mouline, and Turque lieux-dits command Burgundy-level prices.",
    key_producers="E. Guigal, René Rostaing, Michel Ogier, Stéphane Ogier, Yves Gangloff",
    historical_context="Côte Rôtie is one of France's oldest wine regions, with documented production since Roman times. Nearly extinct by the 1960s with fewer than 60 hectares planted, it was rescued by the passionate work of a handful of growers and by Marcel Guigal's extraordinary single-vineyard La La La wines in the 1970s-80s, which achieved legendary 100-point Parker scores and global fame.")

VIN(r1, 2023, "excellent", "rising", "Outstanding Northern Rhône vintage; aromatic complexity and freshness preserved with remarkable concentration")
VIN(r1, 2022, "exceptional", "rising", "Among the finest modern Côte Rôtie vintages; extraordinary floral depth, mineral precision, and aging potential")
VIN(r1, 2021, "good", "stable", "Cooler, elegant year with perfumed, lighter-bodied Syrah; excellent typicity if less concentration")
VIN(r1, 2020, "very_good", "rising", "Rich and powerful with exceptional violet and dark fruit character; structured for long aging")
VIN(r1, 2019, "excellent", "rising", "Classic Côte Rôtie vintage with perfect balance of fruit intensity, mineral depth, and aging structure")

prod1a_id = P("E. Guigal", "France", r1, "winery",
    "The defining producer of Côte Rôtie; Marcel Guigal's single-vineyard La La La wines (La Landonne, La Mouline, La Turque) are among the world's most coveted, regularly achieving 100 Parker points. No producer has done more to establish Côte Rôtie's global reputation.")
prod1a, new1a = PROD("Guigal Côte Rôtie Brune et Blonde", "wine_still", prod1a_id, r1, "France",
    subcategory="red", price_tier="premium",
    description="Guigal's multi-vineyard Côte Rôtie from the Brune (granite) and Blonde (limestone) slopes; the accessible introduction to the estate. Dark cherry, olive, violet, and smoked meat complexity — exceptional quality for the price and a benchmark for the appellation's character.")
if new1a:
    PAIR(prod1a, "Roasted rack of lamb with olive tapenade, rosemary, and jus", "complement", "classic", "main",
        "Côte Rôtie Syrah and lamb is the Northern Rhône's defining pairing; olive in tapenade mirrors the wine's savoury black olive character")
    PAIR(prod1a, "Grilled quail with black truffle butter and Périgueux sauce", "complement", "classic", "main",
        "Game bird's delicacy and truffle depth are a natural vehicle for Côte Rôtie's violet aromatics and earthy mineral character")
    PAIR(prod1a, "Duck breast with cherry reduction and duck liver parfait", "complement", "established", "main",
        "Duck's rich fat and cherry reduction mirror Côte Rôtie's dark fruit; liver parfait adds umami depth against the wine's mineral spine")
    PAIR(prod1a, "Aged Comté with black cherry jam and walnut bread", "bridge", "classic", "cheese",
        "Mountain cheese from the same Alpine arc as Côte Rôtie's granite soils; cherry jam bridges the wine's fruit and the cheese's complexity")

prod1b_id = P("René Rostaing", "France", r1, "winery",
    "One of Côte Rôtie's most respected family estates; René Rostaing's wines from the Landonne and La Viaillère vineyards achieve precision and elegance without the power of Guigal's single-vineyards — a more restrained, Burgundian style.")
prod1b, new1b = PROD("Rostaing Côte Rôtie La Viaillère", "wine_still", prod1b_id, r1, "France",
    subcategory="red", price_tier="premium",
    description="Rostaing's single-lieu-dit Côte Rôtie from La Viaillère: elegant, perfumed Syrah with violet, raspberry, smoked olive, and granite mineral depth. More restrained than many peers — this is Côte Rôtie as finesse rather than power.")
if new1b:
    PAIR(prod1b, "Pigeon rôti with cèpe mushrooms and Périgord truffle jus", "complement", "classic", "main",
        "Wood pigeon's deep gaminess and truffle are perfect foils for Côte Rôtie's smoky violet complexity and mineral depth")
    PAIR(prod1b, "Venison loin with beetroot purée, blackberry, and juniper", "complement", "established", "main",
        "Venison's iron depth and blackberry sauce mirror La Viaillère's dark fruit; juniper amplifies Syrah's Northern Rhône spice")
    PAIR(prod1b, "Pan-seared foie gras with Muscat grape and Sauternes reduction", "complement", "adventurous", "starter",
        "Foie gras's richness and Sauternes sweetness contrast Côte Rôtie's dry power; Muscat grape creates aromatic bridge to the wine's floral lift")
    PAIR(prod1b, "Grilled lamb sweetbreads with capers and crispy sage", "complement", "adventurous", "starter",
        "Offal's richness and caper's brine meet the wine's savoury olive and iron character in a precise, classical French bistro register")

# ── REGION 2: Hermitage AOC (France/Rhône) ──────────────────────────────────
print("\n=== Region 2: Hermitage ===")
r2 = R("Hermitage", "France", "wine",
    designation_type="AOC", designation_name="Hermitage AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Hermitage is France's most majestic Syrah, produced from the single granite hill of Hermitage that rises dramatically from the Rhône at Tain l'Hermitage. The red wines achieve extraordinary power and longevity — 30-50 years for top examples — with tar, leather, dried violets, and mineral depth that no other Syrah appellation rivals. White Hermitage from Marsanne and Roussanne is one of France's greatest dry whites.",
    key_producers="M. Chapoutier, Paul Jaboulet Aîné (La Chapelle), J.L. Chave, E. Guigal",
    historical_context="Hermitage has been considered France's greatest red wine since at least the 18th century — Thomas Jefferson cited it as such. The estate bottling concept was pioneered here. The hill was first planted by a crusading knight in the 13th century according to legend. La Chapelle (Jaboulet) and La Sizeranne (Chapoutier) are among France's most legendary single-vineyard wines.")

VIN(r2, 2022, "exceptional", "rising", "One of the great modern Hermitage vintages; extraordinary depth, mineral precision, and longevity potential")
VIN(r2, 2021, "good", "stable", "Elegant, cooler year; lighter body but excellent typicity and mineral definition in the Syrah")
VIN(r2, 2020, "excellent", "rising", "Powerful and concentrated; structured for exceptional longevity with classic Hermitage tar and iron character")
VIN(r2, 2019, "very_good", "rising", "Fine vintage with classic Syrah intensity; La Chapelle-level concentration across the hill")
VIN(r2, 2018, "excellent", "rising", "Benchmark modern vintage; extraordinary red Hermitage with 40+ year cellaring potential")

prod2a_id = P("M. Chapoutier", "France", r2, "winery",
    "The biodynamic powerhouse of Hermitage and the Rhône Valley; Michel Chapoutier's single-parcel La Sizeranne and Méal bottlings have achieved legendary status, while the estate's biodynamic farming across thousands of Rhône hectares has been transformational.")
prod2a, new2a = PROD("Chapoutier Hermitage La Sizeranne", "wine_still", prod2a_id, r2, "France",
    subcategory="red", price_tier="ultra_premium",
    description="Chapoutier's biodynamic flagship Hermitage red: single-vineyard La Sizeranne parcel on the granite hill. Tar, iron, leather, dark cherry, and mineral depth of extraordinary intensity. A wine requiring a decade minimum and capable of 40+ year evolution.")
if new2a:
    PAIR(prod2a, "Roasted Charolais beef côte de bœuf with marrow bones and jus gras", "complement", "classic", "main",
        "The finest French beef with bone marrow meets Hermitage's power and iron; a pairing of equals requiring cellared wine and aged beef")
    PAIR(prod2a, "Slow-roasted shoulder of lamb with anchovy, rosemary, and garlic", "complement", "classic", "main",
        "Lamb's delicate gaminess elevated by anchovy umami and herbs; Hermitage's mineral iron depth requires the richness to integrate")
    PAIR(prod2a, "Périgord black truffle with scrambled eggs and sourdough toast", "complement", "adventurous", "starter",
        "Fresh black truffle's earthy, aromatic intensity is the ideal luxury vehicle for mature Hermitage's tar and dried violet character")
    PAIR(prod2a, "Aged Cantal entre-deux with black olive tapenade", "bridge", "established", "cheese",
        "Semi-aged Auvergne cheese with savoury olive bridges Hermitage's mineral depth and dark fruit in the great French cheese course tradition")

prod2b_id = P("J.L. Chave", "France", r2, "winery",
    "The most celebrated artisan producer of Hermitage; Jean-Louis Chave's estate has farmed the hill biodynamically for centuries, and his blended red Hermitage — assembled from parcels across the entire hill — is considered the appellation's definitive expression.")
prod2b, new2b = PROD("J.L. Chave Hermitage Rouge", "wine_still", prod2b_id, r2, "France",
    subcategory="red", price_tier="ultra_premium",
    description="The benchmark Hermitage: Chave's estate red assembled from multiple parcels across the granite hill over many months. Among France's most complete red wines — extraordinary complexity of tar, iron, violet, and mineral depth with 50-year aging potential in exceptional vintages.")
if new2b:
    PAIR(prod2b, "Hare à la royale with foie gras, truffle, and Armagnac", "complement", "classic", "main",
        "France's most extravagant game preparation — whole hare stuffed with foie gras — is the only dish that matches Chave Hermitage's complexity and power")
    PAIR(prod2b, "Rack of Sisteron lamb with black olive, thyme, and lavender jus", "complement", "classic", "main",
        "Provençal herbs echo Hermitage's garrigue quality; Sisteron lamb's terroir intensity is the perfect regional match")
    PAIR(prod2b, "Grilled wild salmon with lentilles du Puy and smoky bacon", "complement", "adventurous", "fish_course",
        "Wild salmon's iron richness and lentil earthiness are unusual matches for Hermitage Syrah — mature bottles handle the oily fish with grace")
    PAIR(prod2b, "Roquefort with toasted walnut and aged Armagnac", "complement", "established", "cheese",
        "Blue cheese's intensity and walnut bitterness require Hermitage's depth and power; Armagnac adds spirit warmth to bridge the gap")

# ── REGION 3: Montepulciano d'Abruzzo DOC (Italy) ──────────────────────────
print("\n=== Region 3: Montepulciano d'Abruzzo ===")
r3 = R("Montepulciano d'Abruzzo", "Italy", "wine",
    designation_type="DOC", designation_name="Montepulciano d'Abruzzo DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Montepulciano d'Abruzzo produces vibrant, fruit-forward reds from the Montepulciano grape along the Adriatic coast and interior hills of Abruzzo. The variety (distinct from the Tuscan town of Montepulciano) produces deeply coloured wines with soft tannins, ripe dark cherry, chocolate, and herbs — one of Italy's most food-friendly and value-driven red DOCs. The Cerasuolo d'Abruzzo is a celebrated deeply coloured rosé from the same grape.",
    key_producers="Masciarelli, Valentini, Cataldi Madonna, Illuminati",
    historical_context="The Montepulciano grape has been cultivated in Abruzzo since at least the 15th century. The DOC was established in 1968. The region's reputation was transformed by Edoardo Valentini's quest for quality in the 1970s-80s, and later by Gianni Masciarelli's Villa Gemma, proving Abruzzo capable of world-class quality beyond its value-wine reputation.")

VIN(r3, 2023, "very_good", "stable", "Excellent vintage for Abruzzo; ripe dark fruit with good structure and typical varietal generosity")
VIN(r3, 2022, "excellent", "rising", "Outstanding year; concentrated and dense Montepulciano with depth exceeding typical DOC ambition")
VIN(r3, 2021, "good", "stable", "Balanced, approachable year with characteristic soft tannins and fresh cherry fruit")
VIN(r3, 2020, "excellent", "rising", "Hot year producing powerful, concentrated Montepulciano with excellent aging potential")
VIN(r3, 2019, "very_good", "stable", "Classic Abruzzo vintage with excellent varietal expression; dark cherry, chocolate, and herb in harmony")

prod3a_id = P("Masciarelli", "Italy", r3, "winery",
    "The great moderniser of Abruzzo wine; Gianni Masciarelli transformed the region's reputation with Villa Gemma, a Montepulciano d'Abruzzo capable of matching Tuscany's finest. His estate continues under Marina Cvetic's leadership.")
prod3a, new3a = PROD("Masciarelli Villa Gemma Montepulciano d'Abruzzo", "wine_still", prod3a_id, r3, "Italy",
    subcategory="red", price_tier="premium",
    description="Abruzzo's most celebrated Montepulciano; Villa Gemma from Masciarelli's finest hillside sites aged in French barriques. Deep concentration, dark cherry, chocolate, and Mediterranean herbs with a structure that challenges Tuscany's finest at a fraction of the price.")
if new3a:
    PAIR(prod3a, "Arrosticini (Abruzzese lamb skewers) with bread and olive oil", "complement", "classic", "main",
        "Abruzzo's iconic street food — small lamb pieces on skewers over charcoal — is the defining regional pairing for Montepulciano; elemental and perfect")
    PAIR(prod3a, "Lasagne al ragù with slow-cooked Abruzzese lamb", "complement", "classic", "main",
        "Slow-cooked lamb ragù with pasta is the Abruzzese Sunday tradition; Montepulciano's soft tannins and dark fruit are the natural accompaniment")
    PAIR(prod3a, "Grilled lamb chops with chilli, garlic, and rosemary aglio e olio", "complement", "classic", "main",
        "Simple grilled lamb with Southern Italian aromatics meets Montepulciano's fruit generosity and soft tannic structure")
    PAIR(prod3a, "Pecorino stagionato with fig preserves and walnuts", "bridge", "established", "cheese",
        "Aged Abruzzo sheep cheese with fig creates the regional cheese course pairing for Villa Gemma's dark fruit and earthy depth")

prod3b_id = P("Cataldi Madonna", "Italy", r3, "winery",
    "One of Abruzzo's most quality-focused organic estates; Luigi Cataldi Madonna's Montepulciano, Pecorino, and Cerasuolo from high-altitude sites in Ofena achieve balance, freshness, and elegance rare in the region.")
prod3b, new3b = PROD("Cataldi Madonna Montepulciano d'Abruzzo Malandrino", "wine_still", prod3b_id, r3, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Cataldi Madonna's signature Montepulciano from the Ofena valley floor; ripe, generous dark cherry and plum with soft tannins, a touch of chocolate, and fresh herb character. Consistently excellent value — Abruzzo's most reliable everyday red.")
if new3b:
    PAIR(prod3b, "Pizza with salsiccia, friarielli (broccoli rabe), and smoked mozzarella", "complement", "classic", "casual",
        "Southern Italian pizza with broccoli rabe's bitterness is a natural vehicle for Montepulciano's fruit generosity and soft approachability")
    PAIR(prod3b, "Pasta alla chitarra with porcini ragù and Pecorino", "complement", "classic", "main",
        "Abruzzo's guitar-string pasta with mushroom ragù is the regional classic; earthy porcini amplifies Montepulciano's dark fruit depth")
    PAIR(prod3b, "Polpette (meatballs) in tomato sauce with fresh basil", "complement", "classic", "main",
        "The Italian comfort classic — meatballs in tomato — pairs effortlessly with Montepulciano's soft tannins and dark berry fruit")
    PAIR(prod3b, "Porchetta sandwich with rocket and aged Pecorino", "complement", "established", "casual",
        "Central Italian street food staple; roast pork with rocket bitterness meets Montepulciano's easygoing richness and herb notes")

# ── REGION 4: Bandol AOC (France/Provence) ──────────────────────────────────
print("\n=== Region 4: Bandol ===")
r4 = R("Bandol", "France", "wine",
    designation_type="AOC", designation_name="Bandol AOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Bandol is France's most celebrated Mourvèdre appellation, producing wines of extraordinary depth and aging potential from terraced vineyards above the Mediterranean coast west of Toulon. The red wines — minimum 50% Mourvèdre, often 100% — show black olive, leather, wild herbs (garrigue), game, and mineral complexity that develops magnificently over 10-20 years. The rosé, from the same varieties, is one of Provence's most serious and structured.",
    key_producers="Domaine Tempier, Château Pibarnon, Domaine de la Bégude, Château Pradeaux",
    historical_context="Bandol received AOC status in 1941, one of France's earliest, reflecting its long history of wine excellence. The region's reputation was transformed by Lucien Peyraud at Domaine Tempier from the 1940s, who championed Mourvèdre when fashionable opinion favoured its removal. Alice Waters of Chez Panisse was fundamental in bringing Tempier's wines to American attention in the 1970s.")

VIN(r4, 2023, "excellent", "rising", "Outstanding Bandol vintage; Mourvèdre achieved exceptional ripeness with garrigue complexity at its finest")
VIN(r4, 2022, "very_good", "stable", "Fine balanced year; classic Bandol character with excellent tannic structure and aging potential")
VIN(r4, 2021, "good", "stable", "Cooler year with more restrained Mourvèdre; elegant, herbal style with good typicity")
VIN(r4, 2020, "excellent", "rising", "Exceptional vintage; powerful, concentrated Mourvèdre with 20+ year aging potential")
VIN(r4, 2019, "very_good", "rising", "Benchmark Bandol vintage; textbook garrigue, black olive, and leather complexity with fine mineral depth")

prod4a_id = P("Domaine Tempier", "France", r4, "winery",
    "The most celebrated Bandol estate; Lucien Peyraud's legacy lives on in the wines crafted by his family — complex, age-worthy Mourvèdre reds and a structured rosé that defined what Provence could achieve beyond pale party wine.")
prod4a, new4a = PROD("Tempier Bandol Rouge La Tourtine", "wine_still", prod4a_id, r4, "France",
    subcategory="red", price_tier="premium",
    description="Tempier's single-vineyard La Tourtine: 100% Mourvèdre from a sun-exposed terraced limestone site. Black olive, leather, wild herbs, game, and extraordinary mineral depth. Requires 10 years minimum and rewards 20+ year cellaring. A reference for Provence's aging potential.")
if new4a:
    PAIR(prod4a, "Slow-braised lamb daube with black olives, thyme, and orange zest", "complement", "classic", "main",
        "The Provençal daube and Bandol Mourvèdre is the region's defining pairing; black olive mirrors the wine's savoury character exactly")
    PAIR(prod4a, "Wild boar civet with juniper, lardons, and mushrooms", "complement", "classic", "main",
        "Game stew's iron depth and juniper spice match Mourvèdre's gamey complexity and tannic power; mushroom adds earthy depth")
    PAIR(prod4a, "Grilled Camargue bull with garrigue herbs and tapenade", "complement", "established", "main",
        "Provençal wild bull's lean gaminess and herb landscape matches Bandol's garrigue quality; tapenade is a direct flavour echo")
    PAIR(prod4a, "Aged Banon with chestnut honey and walnuts", "bridge", "classic", "cheese",
        "Provence's wrapped chèvre with chestnut honey bridges Mourvèdre's wild herb and mineral depth; a regional hillside pairing")

prod4b_id = P("Château Pibarnon", "France", r4, "winery",
    "One of Bandol's most consistent and elegant producers; Henri de Saint-Victor's Pibarnon occupies one of the appellation's highest and most limestone-rich sites, producing Mourvèdre of exceptional finesse and mineral definition.")
prod4b, new4b = PROD("Château Pibarnon Bandol Rouge", "wine_still", prod4b_id, r4, "France",
    subcategory="red", price_tier="premium",
    description="Pibarnon's limestone-terroir Bandol: 95% Mourvèdre aged in large oak producing a more elegant, mineral style than many Bandol peers. Refined leather, olive, and garrigue with remarkable freshness from the limestone and altitude — among the appellation's most age-worthy reds.")
if new4b:
    PAIR(prod4b, "Rabbit en cocotte with mustard, rosemary, and cream", "complement", "established", "main",
        "Rabbit's delicate lean meat with Provençal herbs and cream richness is tamed and complemented by Pibarnon's mineral Mourvèdre")
    PAIR(prod4b, "Duck confit with cèpe mushrooms and sarladaise potatoes", "complement", "classic", "main",
        "Duck confit's rich fat and earthiness meet Bandol's tannic structure; mushroom adds a forest-floor depth to echo the wine's complexity")
    PAIR(prod4b, "Grilled sea bass with fennel, pastis, and aioli", "complement", "adventurous", "fish_course",
        "Unusual red wine with fish — but Bandol's garrigue herbs and mineral depth work with sea bass when paired with strong Provençal flavours")
    PAIR(prod4b, "Roquefort with poached pear and bitter walnut oil", "contrast", "adventurous", "cheese",
        "Blue cheese's salt and intensity contrast Mourvèdre's savoury depth; pear adds sweetness and walnut bridges the wine's mineral tannin")

# ── REGION 5: Saint-Joseph AOC (France/Rhône) ──────────────────────────────
print("\n=== Region 5: Saint-Joseph ===")
r5 = R("Saint-Joseph", "France", "wine",
    designation_type="AOC", designation_name="Saint-Joseph AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Saint-Joseph is the Northern Rhône's most extensive appellation, spanning granite slopes and flatter alluvial terraces along the Rhône's west bank. At its finest — from granite hillside sites around Mauves and Tournon — it produces Syrah of haunting elegance and violet-mineral complexity that rivals Hermitage at a fraction of the price. White Saint-Joseph from Marsanne and Roussanne can age magnificently.",
    key_producers="Jean-Louis Chave, Louis Chèze, Pierre Gaillard, André Perret",
    historical_context="Saint-Joseph received AOC status in 1956, initially covering only a few select hillside sites. The appellation was controversially expanded in 1969 to include flatter, less distinguished terroir, diluting its reputation. The finest producers have responded by focusing on steep hillside parcels, and Saint-Joseph's quality tier has risen substantially in recent decades with growing critical attention.")

VIN(r5, 2023, "excellent", "stable", "Very good Northern Rhône year; aromatic Syrah with violet and pepper character well expressed")
VIN(r5, 2022, "excellent", "rising", "Outstanding vintage across the Northern Rhône; concentrated Saint-Joseph with excellent mineral precision")
VIN(r5, 2021, "good", "stable", "Cooler, elegant year; perfumed lighter-bodied Syrah with good acidity and varietal typicity")
VIN(r5, 2020, "very_good", "rising", "Fine vintage with good ripeness and classic Northern Rhône Syrah complexity")
VIN(r5, 2019, "excellent", "rising", "Benchmark year for Saint-Joseph; dark fruit, violet, olive, and pepper in excellent harmony")

prod5a_id = P("Louis Chèze", "France", r5, "winery",
    "One of Saint-Joseph's most acclaimed producers; Chèze's biodynamic estate produces concentrated, elegant Syrah from steep hillside parcels that regularly outperform their appellation classification — genuine Northern Rhône quality at approachable prices.")
prod5a, new5a = PROD("Chèze Saint-Joseph Cuvée Prestige de Caroline", "wine_still", prod5a_id, r5, "France",
    subcategory="red", price_tier="mid_range",
    description="Louis Chèze's flagship Saint-Joseph from steep hillside Syrah; concentrated and mineral with violet, dark cherry, olive, and Northern Rhône pepper complexity. Aged in large oak for texture without masking the granite terroir — among the appellation's finest expressions.")
if new5a:
    PAIR(prod5a, "Grilled lamb cutlets with herb salsa verde and white beans", "complement", "classic", "main",
        "Northern Rhône Syrah and lamb is the regional classic; herb salsa verde amplifies the wine's violet and herb aromatics while beans add earthy weight")
    PAIR(prod5a, "Saucisson de Lyon with Dijon mustard and cornichons", "complement", "classic", "starter",
        "Lyon's famous pork sausage with mustard is the Rhône Valley bistro classic; Syrah's pepper and dark fruit complement the cured meat's richness")
    PAIR(prod5a, "Charcoal-grilled entrecôte with bone marrow butter and green peppercorn sauce", "complement", "established", "main",
        "Beef's char and bone marrow richness meet Saint-Joseph's mineral Syrah; green peppercorn sauce amplifies the wine's pepper signature")
    PAIR(prod5a, "Mushroom and Comté tart with thyme and crème fraîche", "complement", "established", "main",
        "Earthy mushroom and aged Comté bridge Saint-Joseph's mineral depth and dark fruit; crème fraîche adds richness without weight")

prod5b_id = P("Pierre Gaillard", "France", r5, "winery",
    "A highly regarded Northern Rhône producer with estates across multiple appellations; Pierre Gaillard's Saint-Joseph reds from steep Mauves granite sites show the appellation at its most concentrated and age-worthy.")
prod5b, new5b = PROD("Gaillard Saint-Joseph Rouge", "wine_still", prod5b_id, r5, "France",
    subcategory="red", price_tier="mid_range",
    description="Pierre Gaillard's benchmark Saint-Joseph: Syrah from steep hillside sites around Mauves — the appellation's finest granite terroir. Violet, dark berry, smoked olive, and mineral precision. Excellent value for Northern Rhône quality and structure.")
if new5b:
    PAIR(prod5b, "Confit de canard with lentilles du Puy and lardon salad", "complement", "classic", "main",
        "Duck confit's rendered fat and lentil earthiness are natural partners for Northern Rhône Syrah's dark fruit and mineral depth")
    PAIR(prod5b, "Terrine de campagne with cornichons and crusty bread", "complement", "classic", "starter",
        "Country pork terrine's richness and cured texture is lifted by Saint-Joseph's pepper and dark fruit; the classic French bistro opening")
    PAIR(prod5b, "Braised rabbit with olive, tomato, and herbes de Provence", "complement", "established", "main",
        "Rhône Valley rabbit with Mediterranean herbs and olive is a regional pairing; the wine's olive and herb character mirrors the dish directly")
    PAIR(prod5b, "Saint-Marcellin with local honey and walnuts", "bridge", "established", "cheese",
        "Soft Dauphiné cheese from the Rhône region with honey bridges Gaillard's Saint-Joseph — a local cheese table pairing of genuine authenticity")

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
