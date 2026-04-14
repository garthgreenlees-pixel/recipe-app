#!/usr/bin/env python3
"""Terminal 16 — Batch 2: Burgundy Reds + Rhône + Loire depth
Adds second producers/products to single-product French wine regions.
Regions: Beaune, Volnay, Pommard, Vougeot, Condrieu, Cornas,
         Gigondas, Vacqueyras, Tavel, Chinon, Bourgueil
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Producer [{pid}]: {name}")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T16 BATCH 2: BURGUNDY REDS + RHÔNE + LOIRE DEPTH ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# BURGUNDY REDS — filling single-product villages
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── BEAUNE ──")
p_bouchard = P(
    "Bouchard Père et Fils",
    "winery", 114, "France",
    production_philosophy="Beaune's oldest négociant-vigneron with exceptional monopole vineyard holdings in premier and grand cru sites",
    philosophy_description=(
        "Bouchard Père et Fils is one of Burgundy's most important domain-négociants, holding 130 hectares of "
        "vineyard including exceptional Beaune premier cru monopoles. Their Vigne de l'Enfant Jésus in Beaune "
        "Grèves is among Burgundy's most celebrated monopole sites — a 3.6-hectare parcel of old Pinot Noir "
        "producing wines of exceptional concentration and finesse. The estate was acquired by Champagne Joseph "
        "Henriot in 1995, bringing investment that transformed quality across the portfolio."
    ),
    reputation_narrative=(
        "Bouchard Père et Fils holds DRC and Leroy-level respect for their monopole Vigne de l'Enfant Jésus "
        "in Beaune Grèves. Wine Spectator and Decanter regularly award 95+ points for top vintages. "
        "Jancis Robinson and Neal Martin regard the Vigne de l'Enfant Jésus as one of Burgundy's great "
        "monopoles, rivalling Grand Cru wines in quality and cellar-worthiness."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)

prod_bouchard_beaune = PROD(
    "Bouchard Père et Fils Vigne de l'Enfant Jésus Beaune Grèves 1er Cru",
    "wine_still", p_bouchard, 114, "France",
    subcategory="pinot noir",
    description=(
        "Bouchard's extraordinary 3.6-hectare monopole in Beaune Grèves — one of Burgundy's most beloved "
        "premier cru monopoles. Old-vine Pinot Noir of exceptional concentration: deep ruby, violets, "
        "dark cherry, and sandalwood. The wine's silky but firm structure and seamless texture represent "
        "Beaune premier cru at its most compelling. Requires 8-12 years' aging for full expression."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_bouchard_beaune,
    "Roasted pigeon with cherry reduction and celeriac purée",
    "complement", "established", "main",
    "Bouchard Vigne de l'Enfant Jésus has a signature cherry and sandalwood character that "
    "finds precise resonance with roasted pigeon — one of Burgundy's great game bird pairings. "
    "The wine's silky Pinot tannin supports the pigeon's richness without overwhelming; cherry "
    "reduction amplifies the wine's primary fruit character; celeriac provides earthy sweetness "
    "that bridges wine and meat. A pairing of extraordinary Beaune elegance.")
PAIR(prod_bouchard_beaune,
    "Warm Époisses on sourdough with walnuts",
    "complement", "established", "cheese",
    "Bouchard Vigne de l'Enfant Jésus' ripe Pinot fruit and sandalwood complexity achieves the "
    "classic Burgundy-Époisses pairing at premier cru level. The wine's dark cherry richness "
    "cuts through the cheese's powerful washed-rind character; walnuts bridge the wine's "
    "mineral-oak complexity; sourdough provides neutral base. A regional pairing of Burgundy's "
    "most iconic wine-cheese combination.")

print("\n── VOLNAY ──")
p_lafarge = P(
    "Domaine Michel Lafarge",
    "winery", 116, "France",
    production_philosophy="Volnay's benchmark estate: biodynamic viticulture producing the village's most precise and long-lived Pinot Noir",
    philosophy_description=(
        "Domaine Michel Lafarge is Volnay's reference producer — an estate with roots in the 19th century "
        "that converted fully to biodynamics in 2000. Their 10-hectare Clos du Château des Ducs is a "
        "1er Cru monopole of exceptional quality: walled, perfectly exposed, producing Volnay of extreme "
        "elegance and longevity. Frédéric Lafarge continues his father's tradition of minimal-intervention "
        "winemaking: indigenous yeasts, long gentle extraction, and minimal new oak."
    ),
    reputation_narrative=(
        "Domaine Michel Lafarge is considered by Allen Meadows (Burghound) and Jasper Morris MW to be "
        "Volnay's essential producer — their Clos du Château des Ducs is rated alongside Premier Cru "
        "wines of significantly higher classification. Consistently scores 93-96 from top critics. "
        "The domaine exemplifies Volnay's celebrated perfume and finesse at the highest level."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_lafarge = PROD(
    "Domaine Lafarge Volnay Clos du Château des Ducs 1er Cru Monopole",
    "wine_still", p_lafarge, 116, "France",
    subcategory="pinot noir",
    description=(
        "Domaine Lafarge's monopole Clos du Château des Ducs is one of Volnay's greatest 1er Cru sites: "
        "biodynamically farmed old-vine Pinot Noir of extraordinary elegance. Pale ruby with violets, "
        "rose petals, wild strawberry, and mineral finesse. The wine exemplifies Volnay's signature "
        "perfume — lighter in body than Pommard but with extraordinary aromatic complexity and "
        "a silky texture that develops over 10-15 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_lafarge,
    "Roasted quail with grape and thyme jus",
    "complement", "classic", "main",
    "Domaine Lafarge Volnay's violet and wild strawberry perfume achieves its most natural expression "
    "with roasted quail — Volnay's traditional game bird pairing. The wine's silky elegance lifts "
    "rather than dominates the quail's delicate flavour; grape jus mirrors the Pinot Noir's primary "
    "fruit character; thyme bridges the wine's herbal aromatic complexity. A pairing that captures "
    "Volnay's celebrated feminine elegance.")
PAIR(prod_lafarge,
    "Chicken liver pâté with brioche and cornichons",
    "complement", "established", "starter",
    "Lafarge Volnay's precise acidity and wild berry character cuts perfectly through chicken liver "
    "pâté's richness — the wine's mineral spine prevents the pairing from becoming heavy. Brioche "
    "amplifies the Pinot's soft texture; cornichons' acidity echoes the wine's freshness. "
    "A classic Burgundy charcuterie pairing that showcases Volnay at its most versatile.")

print("\n── POMMARD ──")
p_boillot = P(
    "Domaine Jean-Marc Boillot",
    "winery", 115, "France",
    production_philosophy="Pommard's most versatile estate: exceptional red Pommard and white Puligny, made with obsessive precision and minimal intervention",
    philosophy_description=(
        "Domaine Jean-Marc Boillot is one of Burgundy's most talented winemakers — producing both "
        "exceptional Pommard premier cru reds and some of Puligny-Montrachet's finest whites. In Pommard, "
        "his Les Rugiens is considered the village's greatest 1er Cru: a steep, iron-rich marl site "
        "producing structured, concentrated Pinot Noir of extraordinary depth. Boillot's winemaking "
        "favours whole-cluster inclusion, extended maceration, and minimal new oak — resulting in wines "
        "of remarkable textural complexity and 20+ year aging potential."
    ),
    reputation_narrative=(
        "Jean-Marc Boillot is consistently cited by Allen Meadows (Burghound) and Wine Advocate as "
        "one of Burgundy's most gifted winemakers across both red and white wines. His Pommard Les Rugiens "
        "scores 93-97 in top vintages — frequently compared to Grand Cru quality. The domaine's "
        "biodynamic commitment from 2015 further elevated quality and critical recognition."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_boillot = PROD(
    "Jean-Marc Boillot Pommard 1er Cru Les Rugiens",
    "wine_still", p_boillot, 115, "France",
    subcategory="pinot noir",
    description=(
        "Jean-Marc Boillot's Les Rugiens is Pommard's greatest 1er Cru site: steep, iron-rich marl "
        "producing Pinot Noir of extraordinary depth and structure. Deep ruby with black cherry, iron, "
        "violets, and dark spice. The wine has Pommard's signature muscular structure alongside a "
        "precision that marks Boillot's hand. Requires 10-15 years' aging — at its peak, rivals "
        "many Côte de Nuits Grand Cru wines in concentration and complexity."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_boillot,
    "Daube de boeuf Provençale with olives and herbs",
    "complement", "classic", "main",
    "Boillot's Pommard Les Rugiens — with its iron mineral and black cherry concentration — "
    "achieves profound harmony with slow-braised Provençale beef daube. The wine's structured tannin "
    "is softened by the collagen-rich braise while amplifying the dark fruit character; olives bridge "
    "the wine's earthy mineral; herbs echo Les Rugiens' aromatic complexity. A pairing that reveals "
    "Pommard at its most powerful and complete.")
PAIR(prod_boillot,
    "Aged Comté (36 months) with quince paste",
    "complement", "established", "cheese",
    "Boillot Pommard Les Rugiens' iron-mineral structure and dark cherry depth finds a remarkable "
    "partner in aged Comté — the cheese's crystalline nuttiness and caramel depth mirrors the wine's "
    "concentrated complexity. Quince paste bridges the Pinot's fruit character with the cheese's "
    "slight sweetness. A pairing of profound French terroir synergy.")

print("\n── VOUGEOT ──")
p_chateau_tour = P(
    "Château de la Tour",
    "winery", 109, "France",
    production_philosophy="The largest single owner within Clos de Vougeot Grand Cru: old-vine biodynamic viticulture in Burgundy's most famous walled vineyard",
    philosophy_description=(
        "Château de la Tour is the dominant landowner within the historic Clos de Vougeot — holding "
        "5.5 hectares within the Grand Cru enclosure, including the most prized northern sector of "
        "old vines averaging 60+ years. The Vieilles Vignes cuvée represents their finest selection: "
        "exclusively old-vine fruit from the upper slopes near the wall, unified separately and aged "
        "in Allier oak. The estate converted to biodynamics in 2014 under François Labet's direction."
    ),
    reputation_narrative=(
        "Château de la Tour's Vieilles Vignes is considered by Allen Meadows (Burghound) and "
        "Jasper Morris MW to be among the finest Clos de Vougeot wines produced — consistently "
        "scoring 93-97 and outperforming many smaller-parcel Grand Cru holders in the enclosure. "
        "The estate's scale within Clos de Vougeot allows for selection that smaller producers cannot "
        "match, creating wine of extraordinary consistency and depth."
    ),
    price_positioning="ultra_premium",
    authority_tier=2
)

prod_chateau_tour = PROD(
    "Château de la Tour Clos de Vougeot Grand Cru Vieilles Vignes",
    "wine_still", p_chateau_tour, 109, "France",
    subcategory="pinot noir",
    description=(
        "Château de la Tour's Vieilles Vignes is one of Clos de Vougeot's finest expressions: "
        "60+ year old vines from the northern upper sector of Burgundy's most historic Grand Cru. "
        "Deep ruby with dark cherry, earthy spice, iron mineral, and violet complexity. "
        "The wine has Grand Cru concentration combined with the Vougeot terroir's characteristic "
        "mineral austerity. Requires 10-20 years' aging — exceptional at 15-25 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_chateau_tour,
    "Bresse chicken en cocotte with black truffle and cream",
    "elevate", "established", "main",
    "Château de la Tour Vieilles Vignes — with its Grand Cru depth and earthy mineral complexity — "
    "achieves a sublime elevation with Bresse chicken and black truffle. The wine's dark cherry and "
    "iron concentration matches the truffle's earthiness with perfect mirroring; the cream sauce "
    "bridges the Pinot's texture; Bresse chicken's exceptional fat content integrates the wine's "
    "structure. A Grand Cru pairing of complete Burgundy luxury.")
PAIR(prod_chateau_tour,
    "Braised Charolais beef cheek with sauce bordelaise",
    "complement", "classic", "main",
    "Château de la Tour Clos de Vougeot's earthy concentration and structured tannin achieves the "
    "classic Burgundy braised beef pairing at Grand Cru level. The beef cheek's collagen and rendered "
    "fat softens the wine's tannic structure while amplifying its dark fruit; bordelaise sauce creates "
    "a wine-sauce mirror; the slow-cook process creates profound textural harmony. A pairing of "
    "Burgundy's most traditional and satisfying wine-food marriage.")

# ═══════════════════════════════════════════════════════════════════════════════
# NORTHERN RHÔNE — Condrieu + Cornas depth
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CONDRIEU ──")
p_perret = P(
    "André Perret",
    "winery", 137, "France",
    production_philosophy="Condrieu's most complete Viognier estate: old granite-terraced vines producing both fragrant Condrieu and the benchmark Chéry single-vineyard",
    philosophy_description=(
        "André Perret is one of Condrieu's most important producers — holding vines on both the principal "
        "Chéry hillside and the grand cru Côteau de Chéry. His 8-hectare estate is farmed with meticulous "
        "attention to old granite-terraced vines: his oldest Viognier vines are 50+ years. The Chéry "
        "single-vineyard wine is the estate's reference: whole-cluster pressed, fermented in old 500L "
        "demi-muids with indigenous yeasts, aged without malolactic fermentation to preserve the "
        "Viognier's extraordinary aromatic precision. The result is benchmark Condrieu: rich but fresh."
    ),
    reputation_narrative=(
        "André Perret's Chéry is considered by Wine Advocate (Neal Martin) and Jancis Robinson to be "
        "a Condrieu benchmark alongside Vernay's Coteau de Vernon. Consistently scoring 93-96, the "
        "wine demonstrates that Condrieu can achieve complexity alongside its celebrated aromatic power. "
        "The estate is considered essential for any serious Rhône collection."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_perret = PROD(
    "André Perret Condrieu Chéry",
    "wine_still", p_perret, 137, "France",
    subcategory="viognier",
    description=(
        "André Perret's Chéry is Condrieu at its most precise: old-vine Viognier from the Chéry "
        "hillside's granite soils, preserved without malolactic fermentation for aromatic clarity. "
        "Pale gold with extraordinary apricot, white peach, violet, and orange blossom character. "
        "The wine has Condrieu's signature opulence alongside a freshness that marks the best "
        "single-vineyard expressions. A benchmark of the appellation."
    ),
    price_tier="premium"
)
PAIR(prod_perret,
    "Spiced lobster with saffron bisque and fennel",
    "complement", "established", "starter",
    "André Perret Chéry's opulent apricot and violet Viognier character finds an exotic pairing "
    "with spiced lobster and saffron. The Condrieu's stone fruit richness amplifies the saffron's "
    "aromatic depth; fennel bridges the wine's floral character with the bisque's sweetness; "
    "the lobster's natural sweetness is elevated by the wine's fruit concentration. A pairing "
    "that reveals Condrieu's extraordinary versatility with the finest seafood preparations.")
PAIR(prod_perret,
    "Pan-roasted foie gras with peach chutney and brioche",
    "complement", "classic", "starter",
    "André Perret Condrieu Chéry's ripe peach and apricot character is the textbook companion to "
    "pan-roasted foie gras — the Viognier's fruit sweetness balances the liver's richness while "
    "the wine's natural acidity cuts cleanly. Peach chutney creates a stone-fruit mirror between "
    "food and wine; brioche provides the rich neutral base. A classic Rhône luxury starter pairing.")

print("\n── CORNAS ──")
p_allemand = P(
    "Thierry Allemand",
    "winery", 135, "France",
    production_philosophy="Cornas's most sought-after producer: micro-scale biodynamic old-vine Syrah from Cornas's oldest granite terraces",
    philosophy_description=(
        "Thierry Allemand is Cornas's most revered producer — holding just 3 hectares of ancient terraced "
        "Syrah vines on Cornas's granite hillsides. His two wines, Chaillot (younger vines, 30-50 years) "
        "and Reynard (older vines, 60-80+ years), are among the Northern Rhône's most sought-after wines. "
        "Allemand farms biodynamically and vinifies with total respect for the terroir: indigenous yeasts, "
        "no fining or filtration, minimal sulphur. His old-vine Reynard represents what Cornas achieved "
        "before mechanisation — intense, pure, wild Syrah from vines that pre-date the modern appellation."
    ),
    reputation_narrative=(
        "Thierry Allemand is considered by Wine Advocate (Neal Martin and Eric Asimov), Jancis Robinson, "
        "and Allen Meadows to be among the Northern Rhône's greatest producers — his Reynard consistently "
        "scoring 95-100 points and becoming one of wine's most sought-after and allocated releases. "
        "Allocations are tightly held by top restaurants worldwide. The wines are considered cult icons "
        "of natural fine wine production."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_allemand = PROD(
    "Thierry Allemand Cornas Reynard",
    "wine_still", p_allemand, 135, "France",
    subcategory="syrah",
    description=(
        "Thierry Allemand's Reynard is among the Northern Rhône's most extraordinary wines: old-vine "
        "Syrah from 60-80+ year terraced granite vines in Cornas. Intense, wild, and profound — "
        "deep violet/black with black olive, graphite, smoked meat, violets, and concentrated dark "
        "fruit. The wine needs 10-15 years' aging but rewards extraordinary patience: at 20 years, "
        "Reynard achieves complexity rivalling the greatest Northern Rhône wines. Highly allocated."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_allemand,
    "Grilled côte de boeuf with bone marrow and black pepper",
    "complement", "classic", "main",
    "Thierry Allemand Reynard's graphite intensity and wild dark fruit demands the purest beef "
    "preparation — côte de boeuf grilled over charcoal, with no sauce to interrupt the wine-beef "
    "dialogue. The wine's smoked meat character mirrors the char; bone marrow amplifies the "
    "Syrah's fat integration; black pepper echoes Cornas's wild spice character. A pairing of "
    "elemental power between Cornas and the finest beef cut.")
PAIR(prod_allemand,
    "Slow-braised wild boar with dark berry sauce and celeriac",
    "complement", "established", "main",
    "Allemand Reynard's wild, concentrated Cornas character achieves its most fitting pairing with "
    "wild boar — the game's intensity matches the wine's power while the dark berry sauce echoes the "
    "Syrah's fruit concentration. Celeriac provides earthy starchy balance; the slow braise softens "
    "the wine's still-youthful tannin in earlier vintages. A pairing of wild Rhône terroir harmony.")

# ═══════════════════════════════════════════════════════════════════════════════
# SOUTHERN RHÔNE — Gigondas + Vacqueyras + Tavel depth
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── GIGONDAS ──")
p_raspail = P(
    "Château Raspail-Ay",
    "winery", 140, "France",
    production_philosophy="Gigondas's most traditional estate: old-vine Grenache-dominated blends from Gigondas's deepest limestone and clay terroirs",
    philosophy_description=(
        "Château Raspail-Ay is one of Gigondas's most respected traditional estates — run by the "
        "Ay family for generations, farming 20 hectares of old-vine Grenache, Syrah, and Mourvèdre "
        "on Gigondas's distinctive limestone-clay plateau. Their wines represent the classic Gigondas "
        "style: concentrated, earthy, deeply fruited, with the natural power of old-vine Grenache "
        "from the village's best terroirs. No new oak, indigenous fermentation, and extended aging in "
        "old foudres preserve the wine's southern character."
    ),
    reputation_narrative=(
        "Château Raspail-Ay is considered by Wine Advocate (Neal Martin) and Jancis Robinson to be "
        "one of Gigondas's essential producers — their wines demonstrating the appellation's potential "
        "for age-worthiness and complexity. Scoring consistently 90-94, the estate provides "
        "exceptional value for old-vine southern Rhône power from one of France's most exciting "
        "lesser-known appellations."
    ),
    price_positioning="mid_range",
    authority_tier=2
)

prod_raspail = PROD(
    "Château Raspail-Ay Gigondas",
    "wine_still", p_raspail, 140, "France",
    subcategory="red_grenache_blend",
    description=(
        "Château Raspail-Ay's Gigondas is a benchmark of the traditional appellation style: "
        "old-vine Grenache (80%) with Syrah and Mourvèdre from limestone-clay plateau vineyards. "
        "Deep ruby/garnet with ripe dark cherry, garrigue, wild herbs, leather, and earthy spice. "
        "The wine has Gigondas's characteristic power balanced by Grenache's natural finesse. "
        "Approachable young but develops extraordinary complexity over 10-15 years."
    ),
    price_tier="premium"
)
PAIR(prod_raspail,
    "Slow-roasted leg of lamb with herbes de Provence and white bean cassoulet",
    "complement", "classic", "main",
    "Château Raspail-Ay Gigondas's garrigue and dark cherry character achieves the Provençal "
    "region's most natural pairing: slow-roasted lamb perfumed with herbes de Provence. The wine's "
    "wild herb and earthy Grenache character mirrors the lamb's herb crust; white bean cassoulet "
    "provides the rustic, hearty base the Gigondas structure requires; the slow roast's rendered fat "
    "integrates the wine's generous tannin. A southern Rhône pairing of pure regional identity.")
PAIR(prod_raspail,
    "Provençale daube with olives, orange peel, and thyme",
    "complement", "established", "main",
    "Raspail-Ay Gigondas's concentrated Grenache and earthy garrigue is the natural companion to "
    "a classic Provençale beef daube — the slow braise's collagen richness tames the wine's "
    "structure while the orange peel echoes the Grenache's fruit complexity; olives bridge the "
    "wine's Mediterranean garrigue character; thyme amplifies the southern herb dimension. "
    "A pairing rooted in the cuisine of Gigondas's surrounding Provençale villages.")

print("\n── VACQUEYRAS ──")
p_monardiere = P(
    "Domaine de la Monardière",
    "winery", 141, "France",
    production_philosophy="Vacqueyras's quality benchmark: biodynamic old-vine Grenache producing the village's most age-worthy and complex wines",
    philosophy_description=(
        "Domaine de la Monardière is Vacqueyras's most distinguished producer — Christian and Martine "
        "Vache have farmed their 20+ hectare estate biodynamically since 2010. Their Les Deux Moines "
        "is the estate's top wine: a selection of 60-80 year old Grenache vines from Vacqueyras's "
        "finest clay-limestone plateau sites, co-fermented with Mourvèdre and Syrah for complexity. "
        "The wine is aged in old foudres and demi-muids to preserve the old-vine fruit concentration "
        "and avoid oak interference — representing Vacqueyras at its most authentic."
    ),
    reputation_narrative=(
        "Domaine de la Monardière's Les Deux Moines is considered by Wine Advocate and Revue du Vin "
        "de France to be Vacqueyras's finest wine — demonstrating the appellation's potential for "
        "age-worthy complexity at Gigondas-rivalling quality. Scoring 90-94 regularly, the estate "
        "makes the case for Vacqueyras as southern Rhône's most under-valued appellation."
    ),
    price_positioning="mid_range",
    authority_tier=2
)

prod_monardiere = PROD(
    "La Monardière Vacqueyras Les Deux Moines",
    "wine_still", p_monardiere, 141, "France",
    subcategory="red_grenache_blend",
    description=(
        "La Monardière's Les Deux Moines is Vacqueyras at its most concentrated: old-vine Grenache "
        "(70%) with Mourvèdre and Syrah from 60-80 year vines on clay-limestone plateau. Deep ruby "
        "with black cherry, garrigue, tapenade, wild herbs, and dark spice. The wine has impressive "
        "structure for the appellation — tighter and more complex than standard Vacqueyras — "
        "developing extraordinary secondary character over 8-12 years of aging."
    ),
    price_tier="premium"
)
PAIR(prod_monardiere,
    "Grilled rack of lamb with tapenade crust and ratatouille",
    "complement", "classic", "main",
    "La Monardière Les Deux Moines' garrigue and tapenade character achieves its most instinctive "
    "pairing with tapenade-crusted rack of lamb — the wine's olive-herb dimension mirrors the crust "
    "while the Grenache's dark fruit amplifies the lamb's richness. Ratatouille provides the full "
    "southern Provençale vegetable context; the wine's structure supports the lamb without dominating. "
    "A pairing of Vacqueyras terroir at its most complete.")
PAIR(prod_monardiere,
    "Pork tenderloin with black olive sauce and roasted peppers",
    "complement", "established", "main",
    "La Monardière Vacqueyras's Grenache fruit richness and olive-herb character finds a surprising "
    "but elegant match with pork tenderloin — a leaner protein that highlights the wine's fruit "
    "without being overwhelmed by the wine's structure. Black olive sauce bridges the wine's "
    "Mediterranean character; roasted peppers add a Provençale sweetness that amplifies the "
    "Grenache's ripe fruit. A pairing that proves Vacqueyras's versatility.")

print("\n── TAVEL ──")
p_trinquevedel = P(
    "Château Trinquevedel",
    "winery", 142, "France",
    production_philosophy="Tavel's historic estate: producing France's most celebrated rosé from old-vine Grenache and Cinsault on Tavel's distinctive sandy-limestone soils",
    philosophy_description=(
        "Château Trinquevedel is one of Tavel's most historic estates — the Demoulin family have "
        "farmed their 28 hectares since the 17th century, producing what many consider France's "
        "greatest rosé appellation. Unlike Provence rosé, Tavel is made entirely from red varieties "
        "(Grenache, Cinsault, Clairette, Mourvèdre) without restriction on colour extraction — "
        "Trinquevedel's traditional maceration produces a deep salmon-orange rosé of extraordinary "
        "body and complexity. The wine is one of France's few rosés capable of aging 5-10 years."
    ),
    reputation_narrative=(
        "Château Trinquevedel is cited by Jancis Robinson and Wine Advocate as Tavel's most consistent "
        "traditional producer — demonstrating why France's only entirely rosé appellation deserves serious "
        "attention from fine dining sommeliers. Their wines develop extraordinary secondary complexity "
        "over 5+ years, positioning Tavel as a serious food wine, not merely a summer aperitif."
    ),
    price_positioning="mid_range",
    authority_tier=2
)

prod_trinquevedel = PROD(
    "Château Trinquevedel Tavel Rosé",
    "wine_still", p_trinquevedel, 142, "France",
    subcategory="rosé_grenache_blend",
    description=(
        "Château Trinquevedel is Tavel at its most traditional: deep salmon-orange colour from "
        "skin-maceration of Grenache, Cinsault, and Mourvèdre on sandy-limestone soils. "
        "Full-bodied with ripe strawberry, orange zest, garrigue, and a savoury mineral depth "
        "that sets it apart from Provence rosé. Unlike pale rosés, Tavel carries enough body "
        "and structure to age — developing extraordinary complexity over 5-8 years."
    ),
    price_tier="mid_range"
)
PAIR(prod_trinquevedel,
    "Grilled red mullet with rouille and Provençale vegetables",
    "complement", "classic", "fish_course",
    "Château Trinquevedel Tavel's full-bodied garrigue and strawberry character is the natural "
    "companion to grilled red mullet — a fish with enough flavour to stand up to Tavel's power. "
    "Rouille's saffron and garlic intensity bridges the wine's Mediterranean character; Provençale "
    "vegetables echo the Grenache's herbal complexity. A pairing that demonstrates why Tavel was "
    "historically the great rosé of Provençale fish cookery.")
PAIR(prod_trinquevedel,
    "Charcuterie board with jambon cru, pâté, and olives",
    "complement", "established", "starter",
    "Tavel Trinquevedel's robust body and garrigue depth makes it an exceptional charcuterie wine — "
    "far more complete than light Provence rosé for cured meat pairings. The wine's fruit sweetness "
    "balances jambon's salt; olives bridge the Grenache's Mediterranean herb character; pâté's "
    "richness is cut by the wine's structured acidity. A southern French charcuterie pairing of "
    "outstanding versatility.")

# ═══════════════════════════════════════════════════════════════════════════════
# LOIRE — Chinon + Bourgueil depth
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CHINON ──")
p_baudry = P(
    "Domaine Bernard Baudry",
    "winery", 152, "France",
    production_philosophy="Chinon's benchmark estate: biodynamic Cabernet Franc from six distinct terroirs, from light sandy Clos Guillot to powerful limestone Croix Boissée",
    philosophy_description=(
        "Domaine Bernard Baudry is Chinon's most celebrated estate — now run by Matthieu Baudry with "
        "the same biodynamic commitment and terroir focus established by his father Bernard. The domaine "
        "holds 40 hectares across Chinon's full geological spectrum: sandy-gravel Les Granges, "
        "clay-limestone Grezeaux, and pure limestone Croix Boissée. Their Le Clos Guillot is a "
        "0.7-hectare monopole on sandy soil — producing Chinon of extraordinary aromatic intensity "
        "and classic Cabernet Franc freshness, emphasising elegance over power."
    ),
    reputation_narrative=(
        "Domaine Bernard Baudry is considered by Jancis Robinson, Wine Advocate (Neal Martin), and "
        "the French press to be Chinon's essential reference producer. Their wines demonstrate the full "
        "range of Chinon's terroir potential — from fresh, fragrant sandy-soil Clos Guillot to the "
        "profound, age-worthy Croix Boissée limestone cuvée. Consistently scoring 90-95, Baudry "
        "elevated Chinon's international reputation over two decades."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_baudry = PROD(
    "Bernard Baudry Chinon Le Clos Guillot",
    "wine_still", p_baudry, 152, "France",
    subcategory="red_cabernet_franc",
    description=(
        "Baudry's Clos Guillot is Chinon at its most aromatic: a 0.7-hectare monopole on sandy-gravel "
        "soil producing Cabernet Franc of extraordinary fragrance and finesse. Medium ruby with "
        "violet, raspberry, graphite, and fresh herb character — the classic 'pencil shaving' "
        "Cabernet Franc minerality fully expressed. Lighter in body than limestone-site Chinon, "
        "the Clos Guillot is accessible young but rewards 5-8 years' aging beautifully."
    ),
    price_tier="premium"
)
PAIR(prod_baudry,
    "Pork rillettes with cornichons and sourdough toast",
    "complement", "classic", "starter",
    "Bernard Baudry Clos Guillot's graphite freshness and raspberry character achieves the Loire "
    "valley's most instinctive charcuterie pairing — Cabernet Franc and pork rillettes. The wine's "
    "lively acidity cuts through the rillettes' rendered fat; cornichons echo the wine's freshness; "
    "sourdough provides neutral base. The classic Loire bistrot pairing, elevated by a monopole "
    "Chinon of extraordinary aromatic precision.")
PAIR(prod_baudry,
    "Roasted salmon with pinot vinegar butter and lentils du Puy",
    "complement", "established", "main",
    "Baudry Clos Guillot's light-bodied elegance and herb-mineral freshness makes it one of the "
    "Loire's finest salmon wines — the Cabernet Franc's violet and raspberry character bridges "
    "pinot vinegar's acidity while the lentils' earthy mineral provides the necessary weight. "
    "A pairing that demonstrates Loire Cabernet Franc's exceptional versatility with pink fish.")

print("\n── BOURGUEIL ──")
p_chevalerie = P(
    "Domaine de la Chevalerie",
    "winery", 153, "France",
    production_philosophy="Bourgueil's oldest estate: biodynamic old-vine Cabernet Franc from Bourgueil's deepest gravel and tuffeau terroirs",
    philosophy_description=(
        "Domaine de la Chevalerie is Bourgueil's oldest estate — the Caslot family have farmed their "
        "30 hectares since 1640, making this one of Loire's most historic continuous domaines. Their "
        "Galichets is a pure graviers (gravel) cuvée from 60+ year old vines on Bourgueil's deepest "
        "alluvial gravel terroirs — producing wine of extraordinary mineral freshness and Cabernet "
        "Franc purity. Fully biodynamic since 2008, the estate's minimal intervention approach "
        "preserves the unique character of each of their 8 single-plot cuvées."
    ),
    reputation_narrative=(
        "Domaine de la Chevalerie is considered by Jancis Robinson and Loire wine specialist Jacky "
        "Blot to be one of Bourgueil's essential estates — their Galichets demonstrating that gravel-soil "
        "Bourgueil can achieve extraordinary mineral elegance rivalling Chinon's finest expressions. "
        "The estate's 380-year history in Bourgueil gives it unique authority as the appellation's "
        "most enduring fine wine producer."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_chevalerie = PROD(
    "Domaine de la Chevalerie Bourgueil Galichets",
    "wine_still", p_chevalerie, 153, "France",
    subcategory="red_cabernet_franc",
    description=(
        "La Chevalerie's Galichets is Bourgueil from its purest gravel terroir: 60+ year old Cabernet "
        "Franc vines on deep alluvial gravel producing wine of mineral elegance and freshness. "
        "Medium ruby with blackcurrant leaf, violet, graphite, and a distinctive mineral salinity "
        "from the gravel soils. The wine is more structured than Loire's sandy-soil expressions — "
        "firm, vibrant, and age-worthy over 8-12 years. One of Bourgueil's finest."
    ),
    price_tier="premium"
)
PAIR(prod_chevalerie,
    "Duck terrine with pistachios and cornichons",
    "complement", "classic", "starter",
    "La Chevalerie Galichets' blackcurrant leaf and mineral freshness achieves the Loire's "
    "archetypal charcuterie pairing with duck terrine — the Cabernet Franc's structured acidity "
    "cuts through the terrine's richness while the graphite mineral echoes the pistachio's "
    "green herb note. Cornichons amplify the wine's freshness. A Loire bistrot pairing "
    "elevated by Bourgueil's most structured gravel cuvée.")
PAIR(prod_chevalerie,
    "Rabbit with mustard sauce and tarragon, served with gratin dauphinoise",
    "complement", "established", "main",
    "La Chevalerie Galichets' firm Cabernet Franc structure and herbal mineral character achieves "
    "excellent harmony with classic French rabbit in mustard sauce — the wine's blackcurrant "
    "freshness cuts through the cream-mustard richness; tarragon bridges the Cabernet Franc's "
    "herbal dimension; gratin dauphinoise provides the rich starchy base the wine's acidity "
    "requires. A Loire valley pairing of complete regional identity.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T16 Batch 2 complete — 11 producers, 11 products, 22 pairings.")
print("Regions covered: Beaune, Volnay, Pommard, Vougeot, Condrieu, Cornas,")
print("                 Gigondas, Vacqueyras, Tavel, Chinon, Bourgueil")
