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

# ── 1. Cahors (France/Southwest) ──────────────────────────────────────────────
print("\n=== Cahors (France) ===")
r1 = R("Cahors", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Cahors AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The birthplace of Malbec and producer of France's original 'Black Wine' — Cahors in the Lot Valley of southwest France produces inky, tannic reds from Cot (Malbec) on limestone cliffs and alluvial terraces that were exported throughout Europe long before Argentina adopted the grape. Cahors Malbec differs fundamentally from its Argentine descendant — more austere, structured and mineral, with lower alcohol and higher acidity from the continental French climate; a wine built for long ageing and serious gastronomy.",
    key_producers="Chateau Lagrézette, Chateau du Cèdre, Clos Triguedina, Mas del Perie",
    historical_context="Cahors wine has been celebrated since the Middle Ages when it was called 'Black Wine' for its extraordinary dark colour and tannin intensity. The Black Prince drank it; Pope John XXII planted it in Avignon; it was widely used to strengthen Bordeaux wines in centuries past. Phylloxera devastated the vineyards in the 1880s and the great flood of 1956 destroyed what remained; Cahors was rebuilt from scratch and received AOC status in 1971. Today the region benefits from Argentine Malbec's global popularity while asserting its distinct French identity.")

VIN(r1, 2023, "excellent", "stable", "Outstanding Cahors year; Malbec of remarkable mineral concentration and age-worthy tannic structure")
VIN(r1, 2022, "very_good", "stable", "Warm and concentrated; Cahors Malbec of good structure and typical limestone mineral character")
VIN(r1, 2021, "excellent", "stable", "Elegant and precise; fine tannic structure and mineral depth defining classic Cahors character")
VIN(r1, 2020, "very_good", "stable", "Good vintage; concentrated Lot Valley Malbec of authentic French character distinct from Argentine style")
VIN(r1, 2019, "exceptional", "rising", "One of Cahors finest recent vintages; powerful, structured Malbec of benchmark aging potential")

p1a = P("Chateau du Cedre", "France", r1, description="Cahors' most critically acclaimed and internationally celebrated estate, Pascal and Jean-Marc Verhaeghe's Château du Cèdre produces intensely mineral, complex Malbec wines from their Cot-dominant estate that consistently achieve the highest scores for Cahors and demonstrate the appellation's capacity for producing wines rivalling the world's greatest reds.")
prod1a, new1a = PROD("Chateau du Cedre Le Cedre Cahors AOC", "wine_still", p1a, r1, "France",
    subcategory="Malbec (Cot)",
    description="The benchmark prestige Cahors — Château du Cèdre's flagship wine from old-vine Malbec on the limestone causse plateau of the Lot Valley, showing inky dark fruit, graphite, iron mineral, violet and the characteristic austere tannic structure that distinguishes French Malbec from its Argentine counterpart and demands 10–15 years of cellaring.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Cassoulet de Castelnaudary with duck confit and pork", "complement", "classic", "main", "The southwest's most celebrated bean and meat casserole with the region's most intense red wine — Cahors Malbec and cassoulet have shared tables in Languedoc-Pyrénées since the Middle Ages.")
    PAIR(prod1a, "Confit de canard with Sarladaise potatoes", "complement", "classic", "main", "Duck confit with garlic-and-goose-fat potatoes from nearby Sarlat — the Périgord and Quercy's most revered dish meets Cahors' finest Malbec in a southwest French pairing of deep cultural resonance.")
    PAIR(prod1a, "Black Quercy truffle with scrambled eggs and toast", "complement", "adventurous", "main", "The Lot Valley's own black truffle (Tuber melanosporum) with its most powerful wine — the wine's earthy-mineral depth creates an extraordinary mirror for the truffle's subterranean intensity.")
    PAIR(prod1a, "Aged Cantal Entre-Deux cheese with walnut bread", "complement", "classic", "cheese", "The Massif Central's most venerable cheese — aged Cantal's crystalline nuttiness — with Cahors' mineral Malbec creates a profound Auvergne-Quercy pairing of rustic French grandeur.")

p1b = P("Clos Triguedina", "France", r1, description="One of Cahors' most historically significant and consistent family estates, Jean-Luc Baldès produces a remarkable range of Lot Valley Malbec wines — from approachable entry-level through the legendary New Black Wine — that represent the full spectrum of what Cahors can achieve when its indigenous Cot variety is taken to its full potential.")
prod1b, new1b = PROD("Clos Triguedina New Black Wine Cahors AOC", "wine_still", p1b, r1, "France",
    subcategory="Malbec (Cot)",
    description="The most internationally celebrated Cahors wine and a deliberate homage to the region's medieval Black Wine heritage — from oldest-vine Malbec on the limestone plateau with ultra-low yields, producing a wine of extraordinary concentration, minerality and structural authority that is unique in the French wine landscape.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Roasted black Quercy goose with prune stuffing", "complement", "classic", "main", "The region's heritage goose preparation — stuffed with Lot Valley prunes — with its most powerful wine; both products of the Quercy's ancient culinary and viticultural traditions.")
    PAIR(prod1b, "Wild venison pot-au-feu with root vegetables", "complement", "established", "main", "The wine's iron-mineral intensity and powerful tannic structure are ideally matched by the earthy richness of wild game slowly simmered with winter vegetables.")
    PAIR(prod1b, "Foie gras de canard poele with Sauternes reduction", "complement", "adventurous", "starter", "An unexpected but historically authentic Quercy pairing — the wine's fierce tannin and mineral depth provide extraordinary tension against foie gras richness.")
    PAIR(prod1b, "Rocquefort with honey and crushed walnuts", "complement", "classic", "cheese", "Roquefort's pungent blue intensity meets Cahors' most concentrated Malbec — the wine's tannic structure and dark fruit provide the ideal sweet-savoury counterpoint.")

# ── 2. Jurancon (France/Southwest) ────────────────────────────────────────────
print("\n=== Jurancon (France) ===")
r2 = R("Jurancon", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Jurançon AOC / Jurançon Sec AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of France's most unique and underappreciated white wine appellations, Jurançon in the Pyrenean foothills of Béarn produces complex dry and sweet whites from the indigenous Petit Manseng and Gros Manseng grapes on the steep slopes above Pau. The sweet Jurançon — made from late-harvest Petit Manseng dried by the warm Foehn wind on the vine — produces wines of extraordinary concentration, exotic spice and mountain mineral character that age magnificently for decades. The dry Jurançon Sec offers vibrant, aromatic dry whites of genuine complexity and food versatility.",
    key_producers="Domaine Cauhape, Chateau Jolys, Clos Uroulat, Domaine de Souch",
    historical_context="Jurançon's most famous moment was the baptism of Henri IV in 1553, when his lips were moistened with Jurançon wine and a clove of garlic — the future king of France's first taste. The wine was prized at the royal court and exported widely through Bayonne. The Petit Manseng grape's extraordinary capacity to concentrate in the vine while retaining acidity — even in warm Pyrenean harvests — was recognised early; the sweet Jurançon was described by Colette as 'a delightful, imperious and treacherous prince'.")

VIN(r2, 2023, "excellent", "stable", "Outstanding Béarn year; Petit Manseng of exceptional concentration and the classic Jurançon spice character")
VIN(r2, 2022, "very_good", "stable", "Good year with fine ripeness; both dry and sweet Jurançon showing Manseng's characteristic freshness")
VIN(r2, 2021, "excellent", "stable", "Elegant and precise; benchmark dry Jurançon Sec and fine sweet wine concentration")
VIN(r2, 2020, "very_good", "stable", "Reliable year; authentic Pyrenean character in both sec and demi-sec expressions")
VIN(r2, 2019, "exceptional", "rising", "One of Jurançon's finest vintages; extraordinary Moelleux concentration and dry wines of benchmark character")

p2a = P("Domaine Cauhape", "France", r2, description="Jurançon's most internationally celebrated and consistent producer, Henri Ramonteu's Domaine Cauhapé produces the region's benchmark dry and sweet Manseng wines — including the legendary Quintessence du Petit Manseng sweet wine — that have established Jurançon as one of France's most distinctive and underrated white wine appellations.")
prod2a, new2a = PROD("Domaine Cauhape Symphonie de Novembre Jurancon AOC", "wine_dessert", p2a, r2, "France",
    subcategory="Petit Manseng",
    description="A benchmark Jurançon Moelleux from Petit Manseng harvested in November by successive passes — showing extraordinary concentration of exotic spice, apricot, mango, ginger, cinnamon and mountain mineral character with the high natural acidity that prevents cloyingness and gives this wine remarkable freshness and multi-decade aging potential.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Foie gras de canard with fig confit and toast", "complement", "classic", "starter", "Gascony's greatest luxury product with its Pyrenean neighbour's most complex sweet wine — the wine's exotic spice and acidity create the definitive southwestern French foie gras pairing.")
    PAIR(prod2a, "Roquefort with Basque black cherry jam", "complement", "classic", "cheese", "The wine's intense sweetness and spice bridge the pungent blue cheese with the Basque cherry jam in a Pyrénées-Atlantic pairing of extraordinary complexity.")
    PAIR(prod2a, "Crème brulée with orange zest and ginger", "complement", "established", "dessert", "The wine's tropical fruit and ginger spice notes mirror the brulee's caramelised surface while the orange zest creates a citrus bridge to the wine's acid freshness.")
    PAIR(prod2a, "Tarte aux pommes with Armagnac and raisins", "complement", "established", "dessert", "Southwest France's signature spirit-laced apple tart finds its perfect companion in the Pyrenean mountains' most complex sweet wine — two expressions of the southwest's love of concentrated flavour.")

p2b = P("Clos Uroulat", "France", r2, description="One of Jurançon's most authentic and revered small estates, Charles Hours produces extraordinary Jurançon Sec and Moelleux from his Monein estate with minimal intervention philosophy and old-vine Petit and Gros Manseng, creating wines of remarkable purity, complexity and regional character that have been celebrated by critics worldwide.")
prod2b, new2b = PROD("Clos Uroulat Jurancon Sec AOC", "wine_still", p2b, r2, "France",
    subcategory="Petit Manseng, Gros Manseng",
    description="A benchmark dry Jurançon from Charles Hours' Monein estate — showing the dry expression of Manseng's remarkable aromatic complexity: white peach, pineapple, citrus zest, ginger and mountain mineral character with vibrant natural acidity that makes this one of France's most versatile and distinctive dry whites for food pairing.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Basque piperade with eggs and jambon de Bayonne", "complement", "classic", "main", "The Basque region's most celebrated egg preparation with jambon — the wine's exotic freshness and white pepper note complement the sweet pepper-tomato base and salty cured ham.")
    PAIR(prod2b, "Grilled Pyrenean trout with almond butter", "complement", "classic", "main", "Mountain trout from the Pyrenean rivers with the foothills' most distinctive white — mineral mountain freshness expressed simultaneously through fish and wine.")
    PAIR(prod2b, "Seared scallops with vanilla beurre blanc", "complement", "established", "main", "The wine's aromatic tropical notes and bright acidity create an unexpected but satisfying harmony with vanilla-scented butter and the sweet scallop flesh.")
    PAIR(prod2b, "Ossau-Iraty sheep cheese with black cherry jam", "complement", "classic", "cheese", "The Pyrenees' most celebrated cheese — aged Ossau-Iraty — with the mountain foothills' most distinctive dry white; both products of Béarn's unique mountain terroir create one of France's greatest regional cheese pairings.")

# ── 3. Muscadet (France/Loire) ────────────────────────────────────────────────
print("\n=== Muscadet (France) ===")
r3 = R("Muscadet", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Muscadet Sèvre et Maine sur Lie AOC",
    reputation_tier="respected",
    quality_trajectory="rediscovering",
    description="France's most celebrated seafood wine appellation, Muscadet in the Loire Atlantique near Nantes produces bone-dry, mineral whites from Melon de Bourgogne — a neutral variety transformed by the region's granite and gneiss soils into wines of saline precision and the natural yeast-lees aging (sur lie) creates a distinctive bready, creamy texture that makes Muscadet the definitive companion to the Atlantic's finest seafood. After decades of mass-produced decline, a quality renaissance led by passionate growers is restoring Muscadet's reputation for genuinely complex, terroir-expressive wines.",
    key_producers="Domaine de l'Ecu, Pepiere, Domaine Luneau-Papin, Bonnet-Huteau",
    historical_context="Muscadet has been produced near Nantes since the 17th century, when Dutch traders encouraged its planting as a high-volume neutral wine for shipping. The Melon de Bourgogne grape (related to Burgundy's early Melon cultivars) was established after the catastrophic 1709 winter freeze and thrived on the Loire Atlantique's maritime granite. The sur lie aging method — leaving the wine on its fine lees through the winter — was formalised in the 1994 AOC revision, creating a legal framework for the complexity-building technique that distinguishes serious Muscadet from mass-produced versions.")

VIN(r3, 2023, "excellent", "stable", "Outstanding Loire Atlantique year; Muscadet sur lie of exceptional mineral salinity and fresh Atlantic character")
VIN(r3, 2022, "very_good", "stable", "Good year; characteristic Muscadet mineral freshness with fine sur lie yeast complexity")
VIN(r3, 2021, "excellent", "stable", "Elegant and precise; benchmark vintage for serious Muscadet Crus Communaux")
VIN(r3, 2020, "very_good", "stable", "Reliable year; authentic sur lie character with the region's signature granite mineral and Atlantic salinity")
VIN(r3, 2019, "excellent", "rising", "Fine Muscadet year; concentrated mineral Melon with excellent sur lie aging potential")

p3a = P("Domaine de l'Ecu", "France", r3, description="Muscadet's most philosophically revered and internationally celebrated producer, Guy Bossard's biodynamic estate focuses on single-terroir Muscadet expressions — Gneiss, Orthogneiss, Granite — that demonstrate Melon de Bourgogne's extraordinary capacity to transmit geological character, establishing Muscadet as a genuinely mineral, terroir-specific white wine of international quality.")
prod3a, new3a = PROD("Domaine de l'Ecu Expression de Gneiss Muscadet Sevre et Maine", "wine_still", p3a, r3, "France",
    subcategory="Melon de Bourgogne",
    description="A landmark single-terroir Muscadet sur lie from biodynamic Gneiss vineyards — expressing the geological signature of ancient metamorphic rock in profound Atlantic salinity, mineral tension, lemon zest and yeast complexity; among France's most intellectually compelling mineral white wines.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Belon oysters from Brittany with lemon", "complement", "classic", "starter", "The most celebrated French wine-oyster pairing — Muscadet sur lie and flat Belon oysters; the wine's salinity and mineral precision create symbiosis with the oyster's oceanic character that has never been bettered.")
    PAIR(prod3a, "Steamed Bouchot mussels with white wine and herbs", "complement", "classic", "main", "The Loire Atlantique's definitive bivalve preparation — Muscadet steamed mussels with the same wine in the glass is a pairing of complete cultural and gastronomic logic.")
    PAIR(prod3a, "Coquilles Saint-Jacques en coquille with butter and garlic", "complement", "classic", "main", "The wine's mineral salinity and yeast complexity provide the perfect foil for scallops' delicate sweetness in the most refined Breton shellfish preparation.")
    PAIR(prod3a, "Sole meuniere with brown butter and lemon", "complement", "classic", "main", "Loire's most classic wine with France's most classic fish preparation — the wine's mineral precision and sur lie creaminess frame the sole and butter with elegant completeness.")

p3b = P("Domaine Pepiere", "France", r3, description="Marc Ollivier's revered Muscadet estate is considered one of the appellation's finest, producing a range of single-vineyard and Crus Communaux Muscadet that demonstrate the Melon de Bourgogne's extraordinary capacity for mineral complexity and age-worthiness when farmed with passion and bottled with minimal intervention after extended sur lie aging.")
prod3b, new3b = PROD("Domaine Pepiere Clos des Briords Muscadet Sevre et Maine sur Lie", "wine_still", p3b, r3, "France",
    subcategory="Melon de Bourgogne",
    description="A benchmark Muscadet Cru Communaux from Marc Ollivier's legendary Clos des Briords vineyard — from 50+ year old Melon vines on gneiss and mica schist, aged sur lie for over 18 months, producing a wine of extraordinary saline mineral depth, bready yeast complexity and the capacity to age magnificently for 10–15 years.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Langoustines grillees with herbed butter", "complement", "classic", "main", "The wine's sur lie yeast complexity and mineral precision frame grilled langoustines with an elegance that challenges wines of twice the price and reputation.")
    PAIR(prod3b, "Palourdes farcies with garlic butter and breadcrumbs", "complement", "classic", "starter", "Brittany-Loire stuffed clams with Muscadet — the wine's salinity mirrors the bivalve's ocean character while the sur lie yeast bridges the garlic butter.")
    PAIR(prod3b, "Seiches a la Basquaise with tomato and olive oil", "complement", "established", "main", "Cuttlefish in tomato sauce with a mineral Atlantic white — the wine's freshness cuts through the olive oil richness while its salinity amplifies the seafood.")
    PAIR(prod3b, "Grilled sardines with lemon and sea salt", "complement", "classic", "main", "Atlantic sardines with Loire's Atlantic wine — the most elemental possible maritime pairing of completely natural regional logic.")

# ── 4. Casablanca Valley (Chile) ──────────────────────────────────────────────
print("\n=== Casablanca Valley (Chile) ===")
r4 = R("Casablanca Valley", "Chile",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Valle de Casablanca DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Chile's most celebrated cool-climate white wine region, the Casablanca Valley sits just 70km west of Santiago with direct Pacific Ocean access that generates cool morning fog and winds cooling the desert heat. The valley produces Chile's finest Sauvignon Blanc and Pinot Noir alongside excellent Chardonnay, establishing itself in the early 1990s as Chile's answer to California's cool-climate regions. The chalky clay and granite soils with Pacific influence create wines of notable freshness, mineral precision and elegant fruit character that helped create Chile's quality wine export revolution.",
    key_producers="Matetic, Vina Casablanca, Casa del Bosque, Indomita, Concha y Toro Amelia",
    historical_context="Casablanca Valley's commercial wine history began in 1982 when Pablo Morandé of Concha y Toro planted the first vinifera vines in what was considered an impossibly cold frost-prone valley. The gamble paid off spectacularly — by the 1990s Casablanca had become Chile's most fashionable wine region, attracting investment from Chilean giants and international producers drawn by the valley's unique Pacific climate. Today Casablanca is the starting point for understanding Chilean cool-climate wine and remains one of South America's most important white wine producing areas.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Pacific-influenced year; Casablanca Sauvignon Blanc and Pinot Noir of exceptional freshness")
VIN(r4, 2022, "very_good", "stable", "Good coastal cooling effect; aromatic Sauvignon and elegant Pinot Noir showing Pacific character")
VIN(r4, 2021, "excellent", "stable", "Classic Casablanca; fine Sauvignon Blanc mineral freshness and cool Pinot Noir elegance")
VIN(r4, 2020, "very_good", "stable", "Reliable Pacific-influenced year; authentic cool-climate character across all varieties")
VIN(r4, 2019, "excellent", "rising", "One of Casablanca's finest vintages; concentrated, mineral Sauvignon and age-worthy Pinot")

p4a = P("Matetic Vineyards", "Chile", r4, description="One of Casablanca Valley's most ambitious and internationally acclaimed producers, Matetic's biodynamic estate in the San Antonio coastal sub-region produces some of Chile's finest cool-climate Syrah, Sauvignon Blanc and Pinot Noir with a commitment to organic farming and indigenous yeast fermentation that has earned international recognition.")
prod4a, new4a = PROD("Matetic EQ Sauvignon Blanc Casablanca Valley DO", "wine_still", p4a, r4, "Chile",
    subcategory="Sauvignon Blanc",
    description="One of Chile's finest biodynamic Sauvignon Blancs — from coastal Casablanca Valley granite and clay vineyards with Pacific Ocean influence, showing extraordinary mineral precision, citrus, green herbs and the cool-climate freshness that distinguishes Chilean coastal Sauvignon from warmer inland expressions.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Ceviche de congrio with tiger's milk and corn", "complement", "classic", "starter", "Pacific Ocean conger eel cured in lime tiger's milk with Chile's finest coastal Sauvignon Blanc — both expressions of the Pacific's cool mineral energy.")
    PAIR(prod4a, "Steamed clams with white wine and herbs", "complement", "classic", "main", "Pacific clams with their coastal valley's Sauvignon Blanc — the wine's mineral salinity mirrors the clams' ocean character in a maritime pairing of complete geographic logic.")
    PAIR(prod4a, "Grilled salmon with lemon herb butter", "complement", "established", "main", "Chilean Pacific salmon with the valley's mineral Sauvignon Blanc creates one of South America's most commercially successful and gastronomically satisfying wine-fish pairings.")
    PAIR(prod4a, "Avocado and prawn tostadas with lime", "complement", "classic", "starter", "The wine's citrus precision and herbal freshness bridge Chile's beloved avocado and fresh Pacific prawn in a pairing of coastal Pacific cultural identity.")

p4b = P("Casa del Bosque", "Chile", r4, description="One of Casablanca Valley's most respected and consistently excellent producers, Casa del Bosque farms sustainably across the valley's finest blocks to produce benchmark Sauvignon Blanc, Pinot Noir and Gewurztraminer that have consistently achieved international recognition and established the Casablanca as Chile's most versatile cool-climate appellation.")
prod4b, new4b = PROD("Casa del Bosque Gran Reserva Pinot Noir Casablanca Valley DO", "wine_still", p4b, r4, "Chile",
    subcategory="Pinot Noir",
    description="A benchmark cool-climate Chilean Pinot Noir from Casa del Bosque's finest Casablanca Valley blocks — showing the light ruby colour, strawberry, wild cherry and earthy mineral character that Pacific-influenced viticulture delivers, with the elegant silky tannin structure that distinguishes coastal Chilean Pinot from warmer expressions.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Salmón a la plancha with quinoa and herbs", "complement", "established", "main", "Chile's finest Pacific salmon with its most elegant cool-climate Pinot — the wine's delicate fruit and silky texture match the salmon's oily richness without overwhelming it.")
    PAIR(prod4b, "Roasted chicken with garlic and thyme", "complement", "classic", "main", "Pinot Noir's most universal food pairing executed with Chilean cool-climate freshness — the wine's lightness and red fruit complement chicken without competing.")
    PAIR(prod4b, "Mushroom risotto with Parmesan and truffle oil", "complement", "established", "main", "Cool-climate Chilean Pinot's earthy character bridges mushroom umami and truffle in a pairing that demonstrates the variety's cross-cultural versatility.")
    PAIR(prod4b, "Brie-style cheese with quince and crackers", "complement", "classic", "cheese", "The wine's delicate fruit and fine acidity frame creamy triple-cream cheese in the classic soft cheese-Pinot pairing with quince providing the sweet bridge.")

# ── 5. Roussillon (France) ─────────────────────────────────────────────────────
print("\n=== Roussillon (France) ===")
r5 = R("Roussillon", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Côtes du Roussillon AOC / Roussillon VDN",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's most sunny and botanically ancient wine region, Roussillon — historically part of Catalonia — sits between the Pyrenees and the Mediterranean at the foot of France, producing powerful red blends from Grenache, Syrah and Mourvèdre alongside the world's finest Vins Doux Naturels (naturally sweet wines) from Muscat and Grenache Gris. Maury, Rivesaltes and Banyuls are Roussillon's legendary fortified wine appellations; the unfortified reds of Côtes du Roussillon Villages are increasingly recognised as providing outstanding value and terroir complexity from ancient Mediterranean landscape.",
    key_producers="Mas Amiel, Domaine Gauby, Casa Blanca, Gerard Gauby, Clos des Fees",
    historical_context="Roussillon's wine culture predates Roman colonisation — Greek settlers at Empúries and Phoenician traders brought viticulture to this rocky Mediterranean coast before the 3rd century BC. The region was part of the Kingdom of Majorca and the Kingdom of Aragon before becoming French in 1659; its Catalan cultural identity remains distinct. The Vin Doux Naturel tradition — created by Arnau de Vilanova in 1285 when he discovered that adding grape spirit to fermenting must preserved sweetness — established Roussillon as the world's most important sweet wine region for six centuries.")

VIN(r5, 2023, "excellent", "stable", "Outstanding Mediterranean year; Roussillon Grenache and Syrah of intense concentration and garrigue mineral depth")
VIN(r5, 2022, "very_good", "stable", "Hot year with good concentration; powerful schist reds and excellent Muscat VDN conditions")
VIN(r5, 2021, "excellent", "stable", "Fine balance; elegant Côtes du Roussillon Villages with characteristic mineral depth and good freshness")
VIN(r5, 2020, "very_good", "stable", "Reliable Mediterranean year; authentic Catalan character across all Roussillon wine styles")
VIN(r5, 2019, "exceptional", "rising", "One of Roussillon's finest vintages; concentrated, age-worthy Grenache of extraordinary character")

p5a = P("Domaine Gauby", "France", r5, description="Roussillon's most internationally celebrated and philosophically revered producer, Gérard and Ghislaine Gauby farm biodynamically in the Fenouillèdes hills to produce some of France's most profound and complex wines from old-vine Grenache, Mourvèdre and indigenous Catalan varieties — internationally recognised as among the finest expressions of Mediterranean France.")
prod5a, new5a = PROD("Domaine Gauby Vieilles Vignes Rouge Cotes du Roussillon Villages", "wine_still", p5a, r5, "France",
    subcategory="Grenache, Mourvèdre, Syrah, Carignan",
    description="One of southern France's most acclaimed old-vine blends — from Gauby's ancient biodynamic vineyards on granite and schist above the Agly Valley, showing extraordinary dark fruit concentration, garrigue, graphite and mineral depth that rivals the finest Rhône wines and demonstrates Roussillon's capacity for world-class Mediterranean terroir expression.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Braised Catalan-style oxtail with ceps and thyme", "complement", "classic", "main", "Roussillon's Catalan cultural heritage expressed through long-braised beef and wild mushrooms — the wine's dark concentration and mineral depth match the dish's profound earthy richness.")
    PAIR(prod5a, "Roasted Pyrenean lamb with anchoiade and Provencal herbs", "complement", "established", "main", "Mountain lamb with anchovy-herb paste from the Mediterranean and the region's most complex Grenache blend — a pairing of Mediterranean France at its most authentic.")
    PAIR(prod5a, "Boeuf en daube with black olives and orange peel", "complement", "classic", "main", "The Provencal-Roussillon braised beef daube with its Catalan-influenced orange peel — old-vine Roussillon Grenache with complex Mediterranean stew is one of southern France's most satisfying pairings.")
    PAIR(prod5a, "Aged Catalan Tomme Cerdagne sheep cheese", "complement", "classic", "cheese", "Pyrenean sheep cheese from the Cerdagne plateau with Roussillon's most complex red — mountain pastoral tradition expressed through both cheese and vine in authentic Catalan cultural pairing.")

p5b = P("Mas Amiel", "France", r5, description="The most internationally celebrated Maury estate and one of the world's finest Vin Doux Naturel producers, Mas Amiel's extraordinary Grenache Noir-based fortified wines — aged in bonbonnes (glass demi-johns) outdoors for deliberate oxidation — produce wines of extreme complexity, aged dried fruit, coffee, leather and cocoa character that are unique in the world of wine.")
prod5b, new5b = PROD("Mas Amiel Maury Sec Roussillon AOC", "wine_still", p5b, r5, "France",
    subcategory="Grenache Noir",
    description="The dry red expression from Maury's most famous estate — old-vine Grenache Noir from ancient Maury schist in an unfortified style that expresses the appellation's extraordinary mineral character in a profound dry red of dark cherry, cocoa, garrigue, schist mineral and the complexity that comes from decades of experience with the region's most ancient vineyards.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Confit d'oie with Sarladaise potatoes", "complement", "established", "main", "The southwest's goose preparation with Roussillon's schist Grenache — rich preserved poultry fat and concentrated dark fruit in a cross-regional southern French pairing of depth.")
    PAIR(prod5b, "Catalan botifarra negra blood sausage with wild mushrooms", "complement", "classic", "main", "Catalonia's emblematic blood sausage with Roussillon's most characteristic red — the wine's dark intensity and mineral depth provide the definitive Catalan cultural accompaniment.")
    PAIR(prod5b, "Roasted suckling pig a la catalana with romesco", "complement", "classic", "main", "Catalan-style roasted suckling pig with romesco sauce and Roussillon Grenache — the region's cultural identity expressed through both pork and vine in a Mediterranean pairing of historic resonance.")
    PAIR(prod5b, "Banyuls-washed Epoisses cheese with walnut bread", "complement", "adventurous", "cheese", "A provocative Roussillon pairing — the wine's dark schist character with an Epoisses washed in the region's famous fortified wine, creating layers of Grenache-derived flavour.")

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
print("\nDone.")
conn.close()
