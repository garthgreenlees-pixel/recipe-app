"""
T21: French parent wine region depth
Targets: Bordeaux (121), Burgundy (104), Côte de Beaune (112), Côte de Nuits (105),
         Loire Valley (147), Médoc (122), Northern Rhône (132),
         Rhône Valley (131), Southern Rhône (138)
"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
conn.autocommit = True
cur = conn.cursor()

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

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence,
           meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T21: FRENCH PARENT WINE REGION DEPTH (9 REGIONS) ===\n")

# ── BORDEAUX (121) — Château Margaux ──
print("── BORDEAUX — Château Margaux ──")
pid = P(
    name="Château Margaux",
    producer_type="winery",
    region_id=121,
    country="France",
    production_philosophy="Premier Grand Cru Classé pinnacle — the most graceful of the Médoc first growths",
    philosophy_description=(
        "Château Margaux is the archetypal First Growth of the Margaux appellation, consistently "
        "producing Bordeaux's most perfumed, elegant, and aristocratic wines since the 18th century. "
        "The estate's unique gravelly soils over clay subsoil and the south-facing exposure of its "
        "vineyards produce Cabernet Sauvignon of extraordinary finesse and aromatic complexity. "
        "Château Margaux is also the only First Growth to produce a celebrated white wine, "
        "Pavillon Blanc, from 100% Sauvignon Blanc. Under André Mentzelopoulos' family since "
        "1977 and winemaker Paul Pontallier's legendary tenure, the estate reached new heights "
        "of quality and global recognition."
    ),
    reputation_narrative=(
        "Château Margaux is universally regarded as one of the world's greatest wines, combining "
        "First Growth authority with a distinctive feminine elegance that sets it apart from "
        "the power of Latour or the precision of Mouton. The 1900, 1961, 1982, and 2015 "
        "vintages are among the most celebrated in the history of Bordeaux."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Château Margaux Premier Grand Cru Classé",
    category="wine_still",
    producer_id=pid,
    region_id=121,
    origin_country="France",
    subcategory="Cabernet Sauvignon Blend",
    description=(
        "The Grand Vin of Château Margaux, a Premier Grand Cru Classé from the Margaux "
        "appellation in the Médoc. The estate's deep gravel over clay produces Cabernet "
        "Sauvignon of extraordinary aromatic complexity — violet, cassis, cedar, and graphite — "
        "with a silky texture and remarkable length that no other Bordeaux quite replicates. "
        "Typically 75–80% Cabernet Sauvignon blended with Merlot, Cabernet Franc, and Petit "
        "Verdot. Requires 10–20 years of cellaring to reveal its full potential and can age "
        "for 50+ years in exceptional vintages. Among the world's most iconic wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Roasted Pauillac lamb with garlic, rosemary, and Bordelaise sauce",
     "complement", "classic", "main",
     "Classic Médoc pairing — Margaux's perfume and elegance pair with the finest Pauillac lamb")
PAIR(prod,
     "Duck breast à l'orange with wild mushroom duxelles and truffle jus",
     "complement", "established", "main",
     "Margaux's silky tannins and violet character complement duck's richness and truffle's earthiness")

# ── BURGUNDY (104) — Domaine Leflaive ──
print("\n── BURGUNDY — Domaine Leflaive ──")
pid = P(
    name="Domaine Leflaive",
    producer_type="winery",
    region_id=104,
    country="France",
    production_philosophy="Burgundy's white wine soul — biodynamic Puligny-Montrachet of transcendent purity",
    philosophy_description=(
        "Domaine Leflaive is widely considered the standard-bearer for white Burgundy, producing "
        "Puligny-Montrachet from premier and grand cru vineyards including Chevalier-Montrachet, "
        "Bâtard-Montrachet, and Bienvenues-Bâtard-Montrachet. The domaine converted to biodynamic "
        "farming in the 1990s under the direction of Anne-Claude Leflaive, who believed that "
        "chemical-free viticulture was essential to expressing the full purity and mineral "
        "character of Puligny-Montrachet's limestone terroir. The result is Chardonnay of "
        "luminous clarity and incomparable mineral tension."
    ),
    reputation_narrative=(
        "Domaine Leflaive's Puligny-Montrachet represents the pinnacle of white Burgundy, "
        "with the grand crus Chevalier-Montrachet and Bâtard-Montrachet among the world's "
        "most sought-after and expensive white wines. The estate's commitment to biodynamics "
        "transformed Burgundy's approach to sustainable viticulture."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine Leflaive Bourgogne Blanc",
    category="wine_still",
    producer_id=pid,
    region_id=104,
    origin_country="France",
    subcategory="Chardonnay",
    description=(
        "The entry-level Bourgogne Blanc from Domaine Leflaive, produced from biodynamically "
        "farmed Chardonnay in the Côte de Beaune. While the domaine's fame rests on its grand "
        "cru Puligny-Montrachets, the Bourgogne Blanc offers a rare window into Leflaive's "
        "biodynamic philosophy at an accessible level. The wine shows the characteristic "
        "Leflaive purity — bright lemon curd, white flower, and mineral salinity — without "
        "the oak weight of the premier and grand crus. A benchmark for the Bourgogne appellation "
        "and an introduction to one of Burgundy's most revered domaines."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Pan-roasted turbot with brown butter, capers, and lemon",
     "complement", "classic", "main",
     "Leflaive's purity and mineral tension are the classic match for noble white fish preparations")
PAIR(prod,
     "Époisses de Bourgogne with walnuts and honey on sourdough toast",
     "complement", "established", "cheese",
     "White Burgundy and Époisses is Burgundy's greatest regional pairing — terroir synergy")

# ── CÔTE DE BEAUNE (112) — Domaine des Comtes Lafon ──
print("\n── CÔTE DE BEAUNE — Domaine des Comtes Lafon ──")
pid = P(
    name="Domaine des Comtes Lafon",
    producer_type="winery",
    region_id=112,
    country="France",
    production_philosophy="Meursault's pinnacle — Lafon's biodynamic Côte de Beaune whites define village character",
    philosophy_description=(
        "Domaine des Comtes Lafon is the reference point for Meursault, farming their celebrated "
        "premier cru vineyards (Les Perrières, Les Charmes, La Goutte d'Or) biodynamically "
        "since 1993 and producing Chardonnay of extraordinary richness, complexity, and longevity. "
        "Dominique Lafon's meticulous approach — late harvest, long barrel aging, minimal "
        "sulphur additions — produces wines that age magnificently for 15–30 years. The domaine "
        "also produces benchmark Volnay and Montrachet from its premier and grand cru holdings."
    ),
    reputation_narrative=(
        "Domaine des Comtes Lafon is universally ranked among Burgundy's élite, with their "
        "Meursault Perrières and Montrachet considered benchmark expressions of their respective "
        "terroirs. Dominique Lafon's biodynamic conversion influenced a generation of Burgundy "
        "producers toward sustainable viticulture."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine des Comtes Lafon Meursault Côte de Beaune",
    category="wine_still",
    producer_id=pid,
    region_id=112,
    origin_country="France",
    subcategory="Chardonnay",
    description=(
        "Village Meursault from Domaine des Comtes Lafon, the defining estate for this "
        "celebrated Côte de Beaune appellation. Dominated by its premier cru vineyards, "
        "the village Meursault demonstrates Lafon's signature style — rich, generous, and "
        "complex, with the characteristic Meursault personality of hazelnut, butter, and "
        "toasted oak balanced by the limestone minerality that gives the village its "
        "distinctive nutty character. Produced from biodynamically farmed vineyards and "
        "aged in French oak barrels for 18 months. An exceptional introduction to "
        "Meursault's famed golden character."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Roasted sea bass with beurre blanc, sautéed mushrooms, and chervil",
     "complement", "classic", "main",
     "Meursault's hazelnut and butter notes create seamless harmony with beurre blanc and bass")
PAIR(prod,
     "Lobster bisque with crème fraîche, cognac, and fresh tarragon",
     "complement", "established", "starter",
     "Lafon's richness and complexity match lobster bisque's cream and brandy intensity")

# ── CÔTE DE NUITS (105) — Domaine Armand Rousseau ──
print("\n── CÔTE DE NUITS — Domaine Armand Rousseau ──")
pid = P(
    name="Domaine Armand Rousseau Père et Fils",
    producer_type="winery",
    region_id=105,
    country="France",
    production_philosophy="Gevrey-Chambertin's legendary estate — the most authoritative Chambertin in Burgundy",
    philosophy_description=(
        "Domaine Armand Rousseau is the benchmark producer of Gevrey-Chambertin, holding some "
        "of the most coveted parcels in the Côte de Nuits including Chambertin, Chambertin "
        "Clos de Bèze, Clos St-Jacques, and several other premier and grand crus. Charles "
        "Rousseau's traditional approach — long fermentation with whole clusters, extended "
        "maceration, gentle handling — produces Pinot Noir of extraordinary depth, complexity, "
        "and age-worthiness. The domaine is widely regarded as Gevrey-Chambertin's finest "
        "address and one of Burgundy's great estates."
    ),
    reputation_narrative=(
        "Rousseau's Chambertin and Chambertin Clos de Bèze are among Burgundy's most "
        "celebrated and sought-after wines, regularly outperforming the Romanée-Conti in "
        "comparative tastings and fetching prices that reflect their unimpeachable quality "
        "and historical significance."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine Armand Rousseau Gevrey-Chambertin Côte de Nuits",
    category="wine_still",
    producer_id=pid,
    region_id=105,
    origin_country="France",
    subcategory="Pinot Noir",
    description=(
        "Village Gevrey-Chambertin from Domaine Armand Rousseau, the undisputed reference "
        "point for this prestigious Côte de Nuits appellation. While the domaine's grand "
        "crus command stratospheric prices, the village Gevrey-Chambertin offers entry to "
        "Rousseau's philosophy — structured, deeply coloured Pinot Noir with the characteristic "
        "Gevrey-Chambertin personality of dark fruit, iron, earth, and oak-derived spice. "
        "Requires 8–12 years of cellaring to fully reveal its complexity and can age "
        "magnificently for 20–30 years. A benchmark for the appellation's demanding style."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Coq au vin with lardons, mushrooms, pearl onions, and thyme",
     "complement", "classic", "main",
     "The great Burgundian recipe pairing — braised chicken in wine mirrors Gevrey's structure")
PAIR(prod,
     "Roasted pigeon breast with foie gras torchon and black truffle jus",
     "complement", "established", "main",
     "Rousseau Gevrey's iron and dark fruit complement pigeon's gaminess; truffle echoes the earthy notes")

# ── LOIRE VALLEY (147) — Domaine Huet ──
print("\n── LOIRE VALLEY — Domaine Huet ──")
pid = P(
    name="Domaine Huet",
    producer_type="winery",
    region_id=147,
    country="France",
    production_philosophy="Vouvray's biodynamic soul — Chenin Blanc across all styles from Huet's three clos",
    philosophy_description=(
        "Domaine Huet is the defining estate of Vouvray, farming their three clos vineyards "
        "(Le Haut-Lieu, Le Mont, Le Clos du Bourg) biodynamically and producing Chenin Blanc "
        "across the full stylistic spectrum — sec, demi-sec, moelleux, and pétillant — with "
        "a quality and longevity that rivals the world's greatest white wines. Gaston Huet's "
        "legacy continues under the Hwang family with winemaker Noël Pinguet maintaining "
        "the same biodynamic integrity and meticulous site selection that made Huet synonymous "
        "with great Vouvray Chenin Blanc."
    ),
    reputation_narrative=(
        "Domaine Huet's Vouvray moelleux vintages from great years (1947, 1959, 1989, 2002) "
        "are among the world's most celebrated dessert wines, while their sec and demi-sec "
        "wines demonstrate Chenin Blanc's extraordinary versatility and age-worthiness. "
        "No producer better captures the Loire's full potential."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine Huet Vouvray Le Mont Sec Loire Valley",
    category="wine_still",
    producer_id=pid,
    region_id=147,
    origin_country="France",
    subcategory="Chenin Blanc",
    description=(
        "Dry Chenin Blanc from Domaine Huet's Le Mont clos in Vouvray, one of the Loire "
        "Valley's most celebrated estates. The Le Mont vineyard's south-facing tuffeau limestone "
        "slopes create ideal conditions for Chenin Blanc of remarkable intensity and mineral "
        "complexity. The sec style showcases Chenin Blanc at its most austere and intellectual "
        "— quince, green apple, beeswax, and wet stone, with a linear acidity and mineral "
        "tension that allows the wine to age brilliantly for 20–40 years. From one of the "
        "Loire Valley's great biodynamic estates."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Steamed Breton lobster with drawn butter, tarragon, and lemon gremolata",
     "complement", "classic", "main",
     "Great Vouvray Chenin's mineral tension and beeswax richness create harmony with noble lobster")
PAIR(prod,
     "Rillettes de Tours with cornichons and grilled country bread",
     "complement", "established", "starter",
     "Loire Valley terroir synergy — Vouvray Chenin's acidity cuts through pork rillettes' richness")

# ── MÉDOC (122) — Château Mouton Rothschild ──
print("\n── MÉDOC — Château Mouton Rothschild ──")
pid = P(
    name="Château Mouton Rothschild",
    producer_type="winery",
    region_id=122,
    country="France",
    production_philosophy="Pauillac's most theatrical First Growth — art, ambition, and Cabernet Sauvignon",
    philosophy_description=(
        "Château Mouton Rothschild is Pauillac's most dramatically individual First Growth, "
        "elevated from Second to First Growth in 1973 through Baron Philippe de Rothschild's "
        "relentless quality crusade. Famous for its annual artist label series (Picasso, Miró, "
        "Warhol, Chagall) and the legendary assertion 'Premier je suis, Second je fus, Mouton "
        "ne change pas', the estate produces Cabernet Sauvignon-dominated wines of extraordinary "
        "power, spice, and age-worthiness. The estate's gravelly Pauillac soils and precise "
        "winemaking produce a distinctive cedar, pencil shaving, and cassis profile."
    ),
    reputation_narrative=(
        "Mouton Rothschild's mythical vintages — 1945 (Victory), 1982, 1986, 2000 — are among "
        "the most celebrated and expensive Bordeaux ever produced. The estate's combination "
        "of artistic patronage, theatrical presentation, and genuine First Growth quality "
        "makes it unique in the world of fine wine."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Château Mouton Rothschild Premier Cru Classé Pauillac",
    category="wine_still",
    producer_id=pid,
    region_id=122,
    origin_country="France",
    subcategory="Cabernet Sauvignon Blend",
    description=(
        "The Grand Vin of Château Mouton Rothschild, a Premier Grand Cru Classé from Pauillac "
        "in the Médoc. Typically 80–85% Cabernet Sauvignon with Merlot, Cabernet Franc, and "
        "Petit Verdot, the wine shows a distinctive style among the First Growths — powerful, "
        "opulent, and heady with the characteristic Pauillac notes of cedar, pencil shavings, "
        "cassis, and tobacco. The estate's deep gravel over iron-pan soils produce wines of "
        "extraordinary concentration that require 15–25 years of cellaring. Each vintage "
        "carries a commissioned artwork label from a world-renowned artist."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Lamb saddle with Provençal herbs, roasted garlic, and Périgueux sauce",
     "complement", "classic", "main",
     "Pauillac's defining pairing — Mouton's cedar-cassis power is the perfect match for Pauillac lamb")
PAIR(prod,
     "Grilled dry-aged côte de bœuf with bone marrow and bordelaise",
     "complement", "established", "main",
     "First Growth Pauillac's structure and power demand the richest cuts; bordelaise amplifies cassis")

# ── NORTHERN RHÔNE (132) — Alain Graillot ──
print("\n── NORTHERN RHÔNE — Alain Graillot ──")
pid = P(
    name="Domaine Alain Graillot",
    producer_type="winery",
    region_id=132,
    country="France",
    production_philosophy="Crozes-Hermitage's finest — classic Northern Rhône Syrah without grand cru pretension",
    philosophy_description=(
        "Alain Graillot is widely regarded as the greatest producer in Crozes-Hermitage, "
        "the large Northern Rhône appellation surrounding the famous Hermitage hill. Graillot "
        "established his domaine in 1985 with no prior winemaking background, studying under "
        "Marcel Guigal before creating wines that quickly became the reference point for "
        "Crozes-Hermitage. His Syrah combines Northern Rhône's characteristic olive, smoked "
        "meat, and black olive character with a freshness and food-friendliness that makes "
        "his wines uniquely accessible compared to the great Hermitage."
    ),
    reputation_narrative=(
        "Graillot transformed the reputation of Crozes-Hermitage from a lesser Northern Rhône "
        "appellation to a source of genuine quality, with his La Guiraude single-vineyard "
        "Crozes commanding prices approaching those of Hermitage. A founding figure in the "
        "Northern Rhône's quality revolution."
    ),
    price_positioning="premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine Alain Graillot Crozes-Hermitage Northern Rhône",
    category="wine_still",
    producer_id=pid,
    region_id=132,
    origin_country="France",
    subcategory="Syrah",
    description=(
        "Classic Crozes-Hermitage from Domaine Alain Graillot, widely regarded as the appellation's "
        "finest producer and a legend of the Northern Rhône. The estate Crozes-Hermitage shows "
        "the Northern Rhône's characteristic Syrah personality — black olive, smoked meat, "
        "violets, and cracked black pepper — with an additional freshness and accessibility "
        "that sets Graillot apart from the more austere style of Hermitage. Produced from "
        "estate vineyards across Crozes-Hermitage's diverse terroirs of granite, limestone, "
        "and alluvial soils. An exceptional value in the Northern Rhône pantheon."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Grilled merguez with roasted red peppers, harissa, and flatbread",
     "complement", "classic", "main",
     "Northern Rhône Syrah's olive, pepper, and smoked meat character echo spiced merguez perfectly")
PAIR(prod,
     "Rabbit confit with olives, sun-dried tomatoes, and Provençal herbs",
     "complement", "established", "main",
     "Graillot's Syrah and the classic Provence ingredients — olive and herb — create regional harmony")

# ── RHÔNE VALLEY (131) — Château Rayas ──
print("\n── RHÔNE VALLEY — Château Rayas ──")
pid = P(
    name="Château Rayas",
    producer_type="winery",
    region_id=131,
    country="France",
    production_philosophy="Châteauneuf-du-Pape's eccentric genius — 100% Grenache from shaded sandy soils",
    philosophy_description=(
        "Château Rayas is the most individual and sought-after Châteauneuf-du-Pape estate, "
        "producing 100% Grenache from shaded vineyards on sandy soils — the opposite of "
        "conventional Châteauneuf-du-Pape farming. The eccentric Reynaud family's philosophy "
        "of north-facing slopes, old vines, sandy drainage, and extreme density of planting "
        "produces Grenache of extraordinary freshness, elegance, and longevity quite unlike "
        "the usual power-driven Châteauneuf style. The wine is virtually unfindable and "
        "commands prices comparable to the greatest Burgundy grand crus."
    ),
    reputation_narrative=(
        "Château Rayas is a cult wine of the highest order, producing perhaps the world's "
        "most distinctive Grenache and demonstrating that Châteauneuf-du-Pape's potential "
        "extends far beyond its reputation for powerful, alcoholic wines. The estate's "
        "eccentric genius and impossibly limited production have made it a vinous legend."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Château Rayas Châteauneuf-du-Pape Réservé Rhône Valley",
    category="wine_still",
    producer_id=pid,
    region_id=131,
    origin_country="France",
    subcategory="Grenache",
    description=(
        "The legendary Châteauneuf-du-Pape from Château Rayas, one of the world's most sought-after "
        "and individual wines. Produced from 100% Grenache from the estate's unique north-facing "
        "vineyards on sandy soils — deliberately contrasting with the usual galets roulés and "
        "south-facing exposures of Châteauneuf-du-Pape. The result is Grenache of extraordinary "
        "finesse, with the characteristic raspberry and kirsch fruit of the variety elevated "
        "by unusual freshness, mineral tension, and aromatic complexity rarely encountered "
        "in the Southern Rhône. Among the world's great wines and virtually unobtainable."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Roasted rack of lamb with lavender honey glaze and ratatouille niçoise",
     "complement", "classic", "main",
     "Rayas' elegant Grenache and lavender-glazed lamb — the defining Rhône Valley flavour pairing")
PAIR(prod,
     "Wild hare à la royale with foie gras and black truffle sauce",
     "complement", "established", "main",
     "Rayas' extraordinary finesse and dark fruit complexity elevate the noblest game preparations")

# ── SOUTHERN RHÔNE (138) — Domaine du Vieux Télégraphe ──
print("\n── SOUTHERN RHÔNE — Domaine du Vieux Télégraphe ──")
pid = P(
    name="Domaine du Vieux Télégraphe",
    producer_type="winery",
    region_id=138,
    country="France",
    production_philosophy="Châteauneuf-du-Pape benchmark — La Crau plateau's galets roulés and Grenache tradition",
    philosophy_description=(
        "Domaine du Vieux Télégraphe is one of Châteauneuf-du-Pape's great estates, farming "
        "the La Crau plateau's distinctive galets roulés (large rounded stones) that give "
        "Châteauneuf-du-Pape wines their characteristic heat retention and mineral character. "
        "The Brunier family's commitment to traditional Grenache-dominant blending, minimal "
        "intervention, and respect for the appellation's ancient vine heritage produces "
        "Châteauneuf of genuine power, complexity, and age-worthiness. The domaine's La Crau "
        "single-vineyard bottling is among the appellation's most sought-after wines."
    ),
    reputation_narrative=(
        "Vieux Télégraphe is universally recognised as one of Châteauneuf-du-Pape's reference "
        "estates, producing wines of exceptional consistency and terroir expression from "
        "La Crau's unique galets roulés plateau. A benchmark for the Southern Rhône's "
        "greatest appellation."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod = PROD(
    name="Domaine du Vieux Télégraphe Châteauneuf-du-Pape La Crau",
    category="wine_still",
    producer_id=pid,
    region_id=138,
    origin_country="France",
    subcategory="Grenache Blend",
    description=(
        "The flagship Châteauneuf-du-Pape from Domaine du Vieux Télégraphe, produced from "
        "La Crau plateau's celebrated galets roulés vineyards where rounded river stones "
        "reflect heat and accelerate ripening while the gravelly, sandy soils beneath "
        "provide excellent drainage. The blend is dominated by old-vine Grenache (65%) "
        "with Mourvèdre, Syrah, and Cinsault contributing complexity and freshness. "
        "The wine shows Châteauneuf-du-Pape's classic profile — wild berries, garrigue, "
        "leather, smoked meat, and the distinctive mineral warmth of La Crau — with "
        "extraordinary concentration and age-worthiness."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Braised lamb shoulder with olives, tomatoes, capers, and Provençal herbs",
     "complement", "classic", "main",
     "Châteauneuf's garrigue, leather, and dark fruit create the definitive match with braised lamb")
PAIR(prod,
     "Wild boar daube with cèpes, bay leaves, orange peel, and Rhône wine reduction",
     "complement", "established", "main",
     "La Crau's power and complexity demand the depth of wild boar; Rhône wine in both")

print("\n✅ T21 complete — all French parent wine regions now have 2+ products.")
print("  Bordeaux (121): +1 producer (Château Margaux), +1 product, +2 pairings")
print("  Burgundy (104): +1 producer (Domaine Leflaive), +1 product, +2 pairings")
print("  Côte de Beaune (112): +1 producer (Comtes Lafon), +1 product, +2 pairings")
print("  Côte de Nuits (105): +1 producer (Armand Rousseau), +1 product, +2 pairings")
print("  Loire Valley (147): +1 producer (Domaine Huet), +1 product, +2 pairings")
print("  Médoc (122): +1 producer (Château Mouton Rothschild), +1 product, +2 pairings")
print("  Northern Rhône (132): +1 producer (Alain Graillot), +1 product, +2 pairings")
print("  Rhône Valley (131): +1 producer (Château Rayas), +1 product, +2 pairings")
print("  Southern Rhône (138): +1 producer (Vieux Télégraphe), +1 product, +2 pairings")

cur.close()
conn.close()
