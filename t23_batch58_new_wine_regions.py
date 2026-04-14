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

# ── REGION 1: Madiran (France/Southwest — Tannat) ──────────────────────────
print("\n=== Region 1: Madiran ===")
r1 = R("Madiran", "France", "wine",
    designation_type="AOC", designation_name="Madiran AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Madiran produces some of France's most structured and age-worthy reds from the indigenous Tannat grape in the Pyrenean foothills. High tannin concentration is its hallmark, traditionally softened by micro-oxygenation — a technique pioneered here. The wines reward long cellaring.",
    key_producers="Château Montus, Château d'Aydie, Domaine Berthoumieu, Producteurs Plaimont",
    historical_context="Produced since the Middle Ages, Madiran earned AOC status in 1948. The region became internationally known through Patrick Ducournau's invention of micro-oxygenation in the 1990s, transforming the global winemaking landscape.")

VIN(r1, 2023, "very_good", "stable", "Warm summer with good Tannat phenolic development; tannins ripe but structured")
VIN(r1, 2022, "excellent", "rising", "Outstanding vintage with ideal ripening; concentrated and age-worthy Tannats")
VIN(r1, 2021, "good", "stable", "Cooler year; leaner style with fresh acidity balancing the tannin grip")
VIN(r1, 2020, "excellent", "rising", "Hot dry summer; powerful and dense wines with exceptional aging potential")
VIN(r1, 2019, "very_good", "stable", "Balanced vintage with good fruit concentration and fine tannic structure")

prod1a_id = P("Château Montus", "France", r1, "winery",
    "The benchmark Madiran estate; Alain Brumont's flagship property producing monumental Tannat-based reds renowned for power, depth, and extraordinary longevity.")
prod1a, new1a = PROD("Château Montus Madiran", "wine_still", prod1a_id, r1, "France",
    subcategory="red", price_tier="premium",
    description="The definitive Madiran: 100% Tannat from old vines, aged in new oak. Monumental tannins, dark fruit, and remarkable aging potential of 20+ years.")
if new1a:
    PAIR(prod1a, "Slow-braised lamb shoulder with Espelette pepper and flageolet beans", "complement", "classic", "main",
        "Tannat's iron-grip tannins cut through lamb fat while matching the protein weight; Espelette pepper mirrors the wine's spice")
    PAIR(prod1a, "Aged Ossau-Iraty with black cherry compote", "bridge", "classic", "cheese",
        "Regional Basque cheese with fruity accompaniment bridges Tannat's tannin with the wine's dark fruit core")
    PAIR(prod1a, "Cassoulet with Toulouse sausage and duck confit", "complement", "classic", "main",
        "The Southwest classic pairing: rich bean and meat stew meets Madiran's tannic spine and earthy depth")
    PAIR(prod1a, "Grilled Wagyu beef with bone marrow and truffle jus", "complement", "adventurous", "main",
        "Extreme tannin meets extreme fat; the marrow lubricates the tannin while truffle amplifies Tannat's earthiness")

prod1b_id = P("Château d'Aydie", "France", r1, "winery",
    "The Laplace family's historic Madiran estate; multi-generational producers crafting authentic, terroir-driven Tannat with both power and finesse.")
prod1b, new1b = PROD("Château d'Aydie Madiran", "wine_still", prod1b_id, r1, "France",
    subcategory="red", price_tier="mid_range",
    description="Classic Madiran from the Laplace family; predominantly Tannat with Cabernet Franc and Cabernet Sauvignon blended for aromatic lift and structure. Reliable and authentic.")
if new1b:
    PAIR(prod1b, "Duck magret with cèpe mushrooms and Armagnac sauce", "complement", "classic", "main",
        "Regional synergy: Gascony duck and Madiran are inseparable; mushroom earthiness deepens the Tannat's dark fruit")
    PAIR(prod1b, "Grilled black pudding with apple and Madiran reduction", "complement", "classic", "starter",
        "Blood sausage's iron richness meets Tannat's mineral grip; classic Pyrenean bistro pairing")
    PAIR(prod1b, "Venison stew with chestnuts and juniper", "complement", "established", "main",
        "Wild game tannins match Tannat; chestnuts add autumnal sweetness to balance the wine's austerity")
    PAIR(prod1b, "Roquefort with walnut bread and honey", "contrast", "adventurous", "cheese",
        "Blue cheese intensity meets Tannat's tannin in a bold regional contrast; honey softens the collision")

# ── REGION 2: Condrieu (France/Rhône — Viognier) ───────────────────────────
print("\n=== Region 2: Condrieu ===")
r2 = R("Condrieu", "France", "wine",
    designation_type="AOC", designation_name="Condrieu AOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Condrieu is the world's benchmark Viognier appellation, producing lush, aromatic whites from steep granite terraces above the Rhône. The wines are defined by extraordinary perfume — peach, apricot, violet, and white flowers — with a rich, almost oily texture. Quantities are tiny and demand far exceeds supply.",
    key_producers="Yves Cuilleron, Georges Vernay, André Perret, E. Guigal",
    historical_context="Nearly extinct by the 1960s with fewer than 8 hectares remaining, Condrieu was rescued by Georges Vernay's dedication. The appellation expanded dramatically from the 1980s onward and today stands as one of France's most sought-after white wine appellations.")

VIN(r2, 2023, "excellent", "rising", "Aromatic concentration at peak; early harvest preserved freshness and floral intensity")
VIN(r2, 2022, "very_good", "stable", "Rich and opulent vintage; fuller body with stone fruit depth but excellent balance")
VIN(r2, 2021, "good", "stable", "Cooler year; more restrained aromatics but excellent acidity and mineral definition")
VIN(r2, 2020, "exceptional", "rising", "Magnificent vintage with extraordinary aromatic complexity and concentrated Viognier character")
VIN(r2, 2019, "excellent", "rising", "Benchmark year for Condrieu; textbook apricot and violet with silky texture")

prod2a_id = P("Yves Cuilleron", "France", r2, "winery",
    "Leading Condrieu producer and Rhône Valley ambassador; Cuilleron's Viogniers are celebrated for precision and terroir expression, ranging from powerful single-vineyard crus to fresh, early-picked styles.")
prod2a, new2a = PROD("Cuilleron Condrieu Les Chaillets", "wine_still", prod2a_id, r2, "France",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Condrieu from old Viognier vines; dense and concentrated with exceptional peach, apricot, and violet aromatics. Late harvest adds weight without losing freshness.")
if new2a:
    PAIR(prod2a, "Pan-seared scallops with saffron cream and fennel fronds", "complement", "classic", "fish_course",
        "Scallop's natural sweetness and ocean salinity mirrors Viognier's stone fruit richness; saffron amplifies the wine's exotic spice")
    PAIR(prod2a, "Foie gras terrine with peach chutney and brioche", "complement", "classic", "starter",
        "Classic Rhône pairing: Viognier's opulence and residual richness complements foie gras weight; peach chutney is a flavour echo")
    PAIR(prod2a, "Thai green curry with prawns and jasmine rice", "bridge", "established", "main",
        "Condrieu's exotic floral notes and stone fruit bridge across to Southeast Asian spice; the richness tames the heat")
    PAIR(prod2a, "Roasted apricot and lavender tarte tatin", "complement", "adventurous", "dessert",
        "Provençal aromatics mirror Viognier precisely; stone fruit dessert amplifies the wine's apricot core")

prod2b_id = P("Georges Vernay", "France", r2, "winery",
    "The founding guardian of Condrieu; Christine Vernay continues her father's legacy of producing benchmark Viognier that saved the appellation from extinction. The reference estate for the appellation.")
prod2b, new2b = PROD("Vernay Condrieu Coteau de Vernon", "wine_still", prod2b_id, r2, "France",
    subcategory="white", price_tier="ultra_premium",
    description="Vernay's flagship Condrieu from the historic Coteau de Vernon vineyard — the steepest and oldest parcel. Produced only in exceptional years; deep, complex Viognier with astonishing longevity for a white wine.")
if new2b:
    PAIR(prod2b, "Steamed lobster with vanilla-Viognier beurre blanc", "complement", "classic", "fish_course",
        "Vernay's vanilla oak and stone fruit matches lobster's sweetness; the wine's own variety in the sauce creates seamless unity")
    PAIR(prod2b, "Poularde de Bresse roasted with herbs under the skin", "complement", "classic", "main",
        "The finest French chicken meets Condrieu's greatest expression; richness of Bresse breeds meets floral Viognier weight")
    PAIR(prod2b, "Fresh white peach with mascarpone and orange blossom", "complement", "adventurous", "dessert",
        "Direct aromatic echo of the wine's core flavour profile; mascarpone adds cream to match Viognier's texture")
    PAIR(prod2b, "Lightly curried crab bisque with coconut cream", "bridge", "established", "starter",
        "Exotic spice and sweet shellfish amplify Viognier's tropical floral character; coconut mirrors the wine's richness")

# ── REGION 3: Crozes-Hermitage (France/Rhône) ──────────────────────────────
print("\n=== Region 3: Crozes-Hermitage ===")
r3 = R("Crozes-Hermitage", "France", "wine",
    designation_type="AOC", designation_name="Crozes-Hermitage AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Crozes-Hermitage surrounds the famous Hermitage hill and represents the Northern Rhône's most extensive appellation. Syrah dominates the reds with characteristic black olive, violet, and black pepper notes over a mineral backbone. Whites from Marsanne and Roussanne offer honeyed complexity.",
    key_producers="M. Chapoutier, Paul Jaboulet Aîné, Alain Graillot, Cave de Tain",
    historical_context="Crozes-Hermitage received AOC recognition in 1937 and has grown considerably in both area and ambition. The appellation offers a more accessible entry point to Northern Rhône Syrah character, with top producers achieving quality approaching Hermitage itself at a fraction of the cost.")

VIN(r3, 2023, "very_good", "stable", "Excellent Syrah expression with classic Northern Rhône character; good freshness preserved")
VIN(r3, 2022, "excellent", "rising", "Outstanding vintage across the Northern Rhône; concentrated, age-worthy Syrahs with remarkable depth")
VIN(r3, 2021, "good", "stable", "Cooler year with elegant, perfumed Syrahs; lighter body but excellent typicity")
VIN(r3, 2020, "excellent", "rising", "Hot year producing rich, powerful Syrahs with exceptional depth and aging potential")
VIN(r3, 2019, "very_good", "stable", "Classic vintage with Northern Rhône character; violet, black pepper, and olive notes in harmony")

prod3a_id = P("Alain Graillot", "France", r3, "winery",
    "The artisan benchmark of Crozes-Hermitage; Graillot's family estate produces the appellation's most sought-after wines — pure, mineral Syrahs with extraordinary finesse and longevity.")
prod3a, new3a = PROD("Graillot Crozes-Hermitage Rouge", "wine_still", prod3a_id, r3, "France",
    subcategory="red", price_tier="premium",
    description="Alain Graillot's flagship red: pure Syrah from the Les Chênes vineyard. A benchmark for Northern Rhône typicity — violet, black olive, and smoked meat complexity with mineral length and cellaring ability.")
if new3a:
    PAIR(prod3a, "Roasted rack of lamb with olive tapenade crust and rosemary jus", "complement", "classic", "main",
        "Northern Rhône Syrah's black olive character mirrors the tapenade; lamb's iron richness meets Syrah's mineral backbone")
    PAIR(prod3a, "Grilled wild boar sausages with herbed polenta", "complement", "classic", "main",
        "Rustic game matches Syrah's earthiness and spice; polenta provides textural contrast to the wine's weight")
    PAIR(prod3a, "Duck liver pâté with cornichons and sourdough", "complement", "established", "starter",
        "Liver's richness meets Syrah's iron and smoke; acidity of cornichons cuts through and refreshes the palate")
    PAIR(prod3a, "Aged Cheddar with fig jam and walnuts", "bridge", "established", "cheese",
        "Northern Rhône Syrah's savouriness and dark fruit bridge to aged cheese; fig jam amplifies the wine's fruit")

prod3b_id = P("Cave de Tain", "France", r3, "winery",
    "The Tain l'Hermitage cooperative — one of France's finest — producing exceptional Crozes-Hermitage and Hermitage across both colours. Their Grand Classique delivers benchmark quality at accessible prices.")
prod3b, new3b = PROD("Cave de Tain Crozes-Hermitage Nobles Rives", "wine_still", prod3b_id, r3, "France",
    subcategory="red", price_tier="mid_range",
    description="Cave de Tain's flagship Crozes-Hermitage: a single-vineyard Syrah from the Nobles Rives plot showing classic Northern Rhône character — violet, black pepper, smoked meat — with excellent structure and value.")
if new3b:
    PAIR(prod3b, "Magret de canard with cherry reduction and green peppercorn", "complement", "classic", "main",
        "Duck's fat richness is balanced by Syrah's tannin; cherry reduction mirrors the wine's red fruit while green pepper amplifies its peppery signature")
    PAIR(prod3b, "Charcuterie board with cured meats, olives, and Dijon mustard", "complement", "established", "starter",
        "Cured meat umami and salt amplifies Syrah's savoury complexity; olives create a regional harmony")
    PAIR(prod3b, "Mushroom ragù with pappardelle and shaved truffle", "bridge", "established", "main",
        "Earthy mushroom and truffle deepen Syrah's mineral terroir expression; pasta weight matches the wine's body")
    PAIR(prod3b, "Côte de bœuf with béarnaise sauce", "complement", "classic", "main",
        "Côte de bœuf and Crozes-Hermitage is the Rhône bistro classic; beef's fat and char meet Syrah's spice and depth")

# ── REGION 4: Coteaux du Layon (France/Loire sweet Chenin) ─────────────────
print("\n=== Region 4: Coteaux du Layon ===")
r4 = R("Coteaux du Layon", "France", "wine",
    designation_type="AOC", designation_name="Coteaux du Layon AOC",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Coteaux du Layon produces some of France's greatest sweet wines from Chenin Blanc, benefiting from botrytis cinerea (noble rot) concentration in the Layon Valley. Honey, quince, saffron, and beeswax notes develop extraordinary complexity with age, with top wines lasting decades.",
    key_producers="Domaine des Baumard, Château Pierre-Bise, Moulin Touchais, Château Soucherie",
    historical_context="The Layon Valley's humid microclimate has favoured Chenin Blanc and botrytis since medieval times. The Coteaux du Layon AOC was established in 1950, with six villages permitted to add their name to the label. The finest sites — Quarts de Chaume and Bonnezeaux — have their own Grand Cru appellations.")

VIN(r4, 2023, "very_good", "stable", "Good botrytis development; concentrated and balanced with excellent residual sugar levels")
VIN(r4, 2022, "excellent", "rising", "Outstanding noble rot year; exceptional concentration and honeyed complexity")
VIN(r4, 2021, "good", "stable", "Modest botrytis; lighter style with more freshness than concentration but good typicity")
VIN(r4, 2020, "excellent", "rising", "Benchmark Layon vintage; extraordinary botrytis concentration and remarkable balance")
VIN(r4, 2019, "very_good", "stable", "Classic vintage with excellent Chenin character; honey, quince, and saffron in fine balance")

prod4a_id = P("Domaine des Baumard", "France", r4, "winery",
    "The reference estate of Coteaux du Layon and the Loire sweet wine tradition; the Baumard family has produced elegant, age-worthy Chenin Blanc dessert wines for generations, achieving a perfect balance of sweetness and acidity.")
prod4a, new4a = PROD("Baumard Coteaux du Layon", "wine_dessert", prod4a_id, r4, "France",
    subcategory="sweet_white", price_tier="premium",
    description="The Baumard estate's benchmark Layon: botrytis-affected Chenin Blanc with honey, quince, apricot, and saffron. The extraordinary acidity ensures balance and longevity of 20-30+ years.")
if new4a:
    PAIR(prod4a, "Tarte Tatin with crème fraîche and vanilla ice cream", "complement", "classic", "dessert",
        "Caramelised apple and quince echo the wine's oxidative honey notes; crème fraîche acidity mirrors Chenin's freshness")
    PAIR(prod4a, "Roquefort with honeycomb and walnuts", "contrast", "classic", "cheese",
        "Classic sweet-salty contrast: Layon's honeyed sweetness against Roquefort's salt and blue funk; the Loire's great cheese pairing")
    PAIR(prod4a, "Pear and almond frangipane with saffron cream", "complement", "established", "dessert",
        "Pear and almond are flavour echoes of the wine; saffron is the perfect aromatic bridge to Layon's spice notes")
    PAIR(prod4a, "Pan-seared duck liver with caramelised fig and Sauternes reduction", "complement", "classic", "starter",
        "The Loire's answer to Sauternes and foie gras: Layon's sweetness and acidity cut through liver richness; fig deepens the fruit")

prod4b_id = P("Château Pierre-Bise", "France", r4, "winery",
    "One of the Loire's most passionate biodynamic producers; Claude Papin's Coteaux du Layon wines from multiple terroir-specific sites achieve extraordinary depth and minerality alongside botrytis sweetness.")
prod4b, new4b = PROD("Pierre-Bise Coteaux du Layon Beaulieu", "wine_dessert", prod4b_id, r4, "France",
    subcategory="sweet_white", price_tier="mid_range",
    description="Biodynamic Coteaux du Layon from the Beaulieu lieu-dit; expressive botrytis with outstanding mineral precision. Honey, quince, and beeswax with a saline finish that elevates the sweetness.")
if new4b:
    PAIR(prod4b, "Époisses with toasted brioche and fruit chutney", "contrast", "adventurous", "cheese",
        "Washed-rind Époisses's barnyard pungency is tamed by Layon's honeyed sweetness; an audacious regional pairing")
    PAIR(prod4b, "Mango and passionfruit pavlova with lime zest", "complement", "established", "dessert",
        "Tropical fruit intensity mirrors the wine's exotic botrytis notes; lime acidity echoes Chenin's racy freshness")
    PAIR(prod4b, "Crème brûlée with orange blossom and vanilla", "complement", "classic", "dessert",
        "Custard sweetness meets Layon's honeyed weight; orange blossom amplifies Chenin's floral signature")
    PAIR(prod4b, "Smoked duck breast with golden raisin gastrique", "bridge", "established", "main",
        "Smoke and sweet-sour gastrique bridge the wine's botrytis richness with savoury food; a sophisticated match")

# ── REGION 5: Sagrantino di Montefalco (Italy/Umbria) ──────────────────────
print("\n=== Region 5: Sagrantino di Montefalco ===")
r5 = R("Sagrantino di Montefalco", "Italy", "wine",
    designation_type="DOCG", designation_name="Sagrantino di Montefalco DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Sagrantino di Montefalco produces Italy's most tannic wines from the indigenous Sagrantino grape, grown in the hills of Umbria around Montefalco. Intense black fruit, dried fig, leather, and tobacco complexity develop over decades. The DOCG requires a minimum of 37 months aging.",
    key_producers="Arnaldo Caprai, Pardi, Antonelli San Marco, Perticaia",
    historical_context="Sagrantino was historically produced only as a sweet passito wine for religious ceremonies. The pioneering work of Marco Caprai in the 1970s-90s transformed it into a prestigious dry red DOCG, gaining full recognition in 1992. Now considered one of Italy's great indigenous variety success stories.")

VIN(r5, 2022, "excellent", "rising", "Outstanding Umbrian vintage; deep concentration with extraordinary tannic structure and aging potential")
VIN(r5, 2021, "very_good", "stable", "Balanced year with classic Sagrantino structure; firm tannins and good fruit depth")
VIN(r5, 2020, "excellent", "rising", "Hot year producing densely concentrated Sagrantino; exceptional longevity expected")
VIN(r5, 2019, "very_good", "stable", "Benchmark vintage with fine tannin ripeness and aromatic complexity; traditional character")
VIN(r5, 2018, "good", "stable", "More accessible vintage; tannins integrated earlier but with good varietal typicity")

prod5a_id = P("Arnaldo Caprai", "Italy", r5, "winery",
    "The producer who put Sagrantino on the world map; Marco Caprai's ambitious estate has driven quality and recognition for the DOCG since the 1980s, producing benchmark Sagrantino of immense power and complexity.")
prod5a, new5a = PROD("Caprai Sagrantino di Montefalco 25 Anni", "wine_still", prod5a_id, r5, "Italy",
    subcategory="red", price_tier="premium",
    description="Caprai's benchmark Sagrantino: 25 anni (25 years) edition celebrating the estate's anniversary — 100% Sagrantino aged in barrique and large oak. Massive tannic structure, black fruit intensity, and leather complexity requiring a decade of cellaring.")
if new5a:
    PAIR(prod5a, "Wild boar slow-braised with black truffle and Umbrian lentils", "complement", "classic", "main",
        "Regional perfection: Umbrian wild boar's iron richness meets Sagrantino's massive tannin; truffle amplifies the wine's earthy depth")
    PAIR(prod5a, "Aged Pecorino di Fossa with fig and honey", "bridge", "classic", "cheese",
        "Cave-aged sheep cheese with sweet accompaniments bridges Sagrantino's austerity; fig echoes the wine's dried fruit core")
    PAIR(prod5a, "Tagliata di manzo with rocket, Parmigiano, and black truffle", "complement", "established", "main",
        "Bistecca cut with bitter rocket tames Sagrantino's tannin; Parmigiano adds umami depth while truffle provides aromatic bridge")
    PAIR(prod5a, "Braised lamb shank with black olive tapenade and polenta", "complement", "classic", "main",
        "Long-cooked lamb fat softens Sagrantino's grip; black olive mirrors the wine's savoury depth; polenta's starch balances")

prod5b_id = P("Antonelli San Marco", "Italy", r5, "winery",
    "One of Montefalco's most respected organic estates; the Antonelli family crafts Sagrantino with excellent balance between power and elegance, often more approachable than peers without sacrificing the variety's character.")
prod5b, new5b = PROD("Antonelli Sagrantino di Montefalco", "wine_still", prod5b_id, r5, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Organic Sagrantino from the Antonelli estate; balances the variety's characteristic tannin intensity with dark cherry, dried fig, and tobacco complexity. More approachable in youth than many peers while retaining authentic DOCG character.")
if new5b:
    PAIR(prod5b, "Cinghiale (wild boar) ragu with pappardelle and Pecorino", "complement", "classic", "main",
        "The quintessential Umbrian pairing: wild boar ragu's fat and iron richness softens Sagrantino's tannin; Pecorino adds saline depth")
    PAIR(prod5b, "Roasted pigeon with bitter chocolate sauce and candied chestnuts", "complement", "established", "main",
        "Game bird's lean richness pairs with Sagrantino; bitter chocolate mirrors the wine's dark tannin while chestnut sweetens")
    PAIR(prod5b, "Salumi platter with Norcia prosciutto and Umbrian truffles", "complement", "established", "starter",
        "Regional cured meats with truffle are a natural vehicle for Sagrantino's savouriness and earthy depth")
    PAIR(prod5b, "Aged Grana Padano with dried figs and walnuts", "bridge", "classic", "cheese",
        "Hard cheese umami meets Sagrantino's tannin; dried figs echo the wine's characteristic dried fruit notes — a Montefalco classic")

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
