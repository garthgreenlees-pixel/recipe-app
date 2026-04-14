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

# ── 1. Jura (France) ─────────────────────────────────────────────────────────
print("\n=== Jura (France) ===")
r1 = R("Jura", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Arbois / Côtes du Jura / Château-Chalon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's most distinctive and philosophically compelling wine region, a small enclave in eastern France near the Swiss border producing oxidative Vin Jaune from Savagnin, the unique Vin de Paille (straw wine), and natural-style Chardonnay and Poulsard/Trousseau reds. Jura has become a cult destination for natural wine enthusiasts worldwide, with its ancient oxidative winemaking traditions — particularly the Vin Jaune aged under flor yeast — creating wines of incomparable complexity and longevity.",
    key_producers="Domaine Henri Maire, Domaine Ganevat, Pierre Overnoy, Domaine Tissot, Domaine de la Pinte",
    historical_context="Jura's wine history stretches back 2,000 years to Roman times; the region was a major wine supplier to Paris before rail transport opened cheaper sources from the south. The unique Vin Jaune style — developed from the accidental discovery that flor yeast would protect wine left in unfilled barrels — became codified in the Château-Chalon AOC in 1936, the first French AOC. Pierre Overnoy's natural winemaking at Pupillin in the 1970s created the philosophical foundation for today's global natural wine movement.")

VIN(r1, 2023, "excellent", "stable", "Outstanding Jura vintage; Vin Jaune of exceptional concentration; Poulsard and Trousseau of fine elegance")
VIN(r1, 2022, "very_good", "stable", "Warm year with excellent Savagnin concentration; bold and generous Vin Jaune profile")
VIN(r1, 2021, "excellent", "stable", "Fresh and precise; elegant Chardonnay and vibrant Poulsard with fine natural acidity")
VIN(r1, 2020, "very_good", "stable", "Good ripeness with natural yeast fermentation conditions; excellent for oxidative styles")
VIN(r1, 2019, "exceptional", "rising", "One of the finest Jura vintages in decades; extraordinary concentration and flor development potential for Vin Jaune")

p1a = P("Domaine Ganevat", "France", r1, description="The most revered and cult estate in contemporary Jura wine, Jean-François Ganevat's small domain produces an extraordinary range of single-parcel, low-intervention wines from old-vine Chardonnay, Savagnin, Poulsard and Trousseau that have made Jura the world's most exciting natural wine pilgrimage destination.")
prod1a, new1a = PROD("Domaine Ganevat Chardonnay Grusse en Billat Jura AOC", "wine_still", p1a, r1, "France",
    subcategory="Chardonnay",
    description="A masterpiece of oxidative Jura Chardonnay from one of the appellation's most coveted producers — aged without topping under a film of flor yeast in old oak barrels to develop extraordinary walnut, citrus, curry spice and mineral complexity that can only come from the Jura's unique terroir and philosophy.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Comté cheese aged 24+ months with walnut bread", "complement", "classic", "cheese", "The most celebrated pairing in French gastronomy — oxidative Jura Chardonnay and the region's own great aged cheese, both sharing the same walnut-curry-mineral flavour signature from the same mountain terroir.")
    PAIR(prod1a, "Roasted chicken with Vin Jaune and morels", "complement", "classic", "main", "Poulet aux Morilles au Vin Jaune — Jura's greatest dish — is the definitive test of the oxidative Chardonnay's gastronomic power; the wine's complexity elevates the earthy mushrooms to transcendence.")
    PAIR(prod1a, "Crayfish gratin with Comté and cream", "complement", "established", "main", "River crayfish in cream and cheese sauce finds extraordinary harmony with oxidative Chardonnay's rich, complex character.")
    PAIR(prod1a, "Slow-cooked Bresse chicken with cream and tarragon", "complement", "established", "main", "The world's finest chicken from a region neighbouring Jura finds its most intellectually satisfying companion in this oxidative Chardonnay of profound complexity.")

p1b = P("Domaine Tissot", "France", r1, description="André and Bénédicte Tissot's benchmark biodynamic estate produces the most comprehensive and consistently excellent range across all Jura AOCs — from entry-level Poulsard to profound Vin Jaune and Vin de Paille — setting the standard for quality-conscious natural winemaking across the entire appellation.")
prod1b, new1b = PROD("Domaine Tissot Vin Jaune Arbois AOC", "wine_still", p1b, r1, "France",
    subcategory="Savagnin",
    description="A benchmark biodynamic Vin Jaune from Savagnin aged for a minimum of 6 years and 3 months in unfilled barrels under protective flor yeast — developing its legendary complex character of walnuts, curry, dried fruit, beeswax and Jura terroir in a wine built to last a century.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Poulet de Bresse with morels and cream sauce", "complement", "classic", "main", "The canonical Jura pairing — flor-aged Savagnin and wild porcini mushroom cream sauce with premium French chicken — the wine's oxidative depth is inseparable from this preparation.")
    PAIR(prod1b, "Pan-fried foie gras with dried apricot and walnut", "complement", "established", "starter", "The wine's dried fruit and nut complexity mirror the foie gras's richness while its high acidity — retained through the Vin Jaune process — provides the essential counter-balance.")
    PAIR(prod1b, "Aged Comté Gruyere with toasted hazelnuts", "complement", "classic", "cheese", "Both Comté and Vin Jaune emerge from the same Jura mountain terroir and share the same flor-derived walnut-hazelnut character in one of the world's truly great wine-food regional pairings.")
    PAIR(prod1b, "Curry-spiced cauliflower with raisins and pine nuts", "complement", "adventurous", "main", "The wine's famous curry spice note — a signature of all Vin Jaune — creates an extraordinary bridge with curry-spiced vegetables in an unexpected but revelatory pairing.")

# ── 2. Savoie (France) ────────────────────────────────────────────────────────
print("\n=== Savoie (France) ===")
r2 = R("Savoie", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Vin de Savoie AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's Alpine wine region, straddling the French Alps near Geneva, Chambéry and Annecy, producing light, high-acid whites from the indigenous Jacquère, Roussette and Altesse grapes alongside the fresh Gamay and Mondeuse reds. Savoie wines are the quintessential Alpine accompaniment — crisp, mineral and food-versatile — gaining increasing attention from sommeliers worldwide seeking unique French whites beyond the well-known appellations.",
    key_producers="Domaine Belluard, Domaine Jean-Pierre & Philippe Grisard, Louis Magnin, Prieuré Saint-Christophe",
    historical_context="Savoie's wine history predates French sovereignty — the Duchy of Savoy maintained its own viticultural traditions before the region joined France in 1860. The mountains and lake system create a patchwork of microclimates; the Cru villages (Chignin, Abymes, Apremont) were codified in the 1973 AOC revision. Savoie wines remained predominantly local until the 1990s natural wine movement brought global interest to its mineral Jacquère whites and structured Mondeuse reds.")

VIN(r2, 2023, "excellent", "stable", "Exceptional Alpine vintage; Jacquère and Altesse of remarkable mineral precision and freshness")
VIN(r2, 2022, "very_good", "stable", "Warm year with good fruit ripeness; generous Roussette and concentrated Mondeuse")
VIN(r2, 2021, "excellent", "stable", "Fresh and linear; ideal conditions for high-acid Jacquère and elegant Mondeuse")
VIN(r2, 2020, "very_good", "stable", "Good fruit ripeness balanced by Alpine freshness; excellent across all Savoie crus")
VIN(r2, 2019, "excellent", "rising", "Outstanding year; the finest Savoie vintage of the decade for both whites and reds")

p2a = P("Domaine Belluard", "France", r2, description="The most internationally celebrated Savoie producer, Dominique Belluard's biodynamic estate in Ayze focuses on the ultra-rare Gringet grape — a local relation of Traminer — producing wines of extraordinary mineral complexity and aromatic intensity that have made him one of France's most sought-after natural wine producers.")
prod2a, new2a = PROD("Domaine Belluard Ayze Brut Methode Traditionnelle Savoie", "wine_sparkling", p2a, r2, "France",
    subcategory="Gringet",
    description="A revelatory sparkling Savoie wine from the rare indigenous Gringet grape using traditional method — showing extraordinary Alpine minerality, white flower, citrus and mountain herb character in a wine that represents some of France's most unique and compelling bubbles outside Champagne.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Fondue Savoyarde with Beaufort and Gruyere", "complement", "classic", "main", "Savoie's most culturally embedded pairing — the region's sparkling wine cuts through molten cheese richness with Alpine mineral freshness that tradition has perfected over centuries.")
    PAIR(prod2a, "Raclette with Alpine charcuterie and pickled cornichons", "complement", "classic", "main", "The wine's crisp effervescence and mountain herb character provide the definitive digestive counterpoint to Raclette's rich melted cheese and cured meat.")
    PAIR(prod2a, "Omble chevalier lake fish with lemon butter", "complement", "classic", "main", "Lake Geneva's most prized fish — char-like Arctic char — with its own regional sparkling wine; the Alpine mineral character of both are inseparable.")
    PAIR(prod2a, "Oysters with Alpine herb mignonette", "complement", "established", "starter", "The wine's mineral precision and natural bubbles pair with oysters as elegantly as Champagne, at a fraction of the price and with more Alpine specificity.")

p2b = P("Louis Magnin", "France", r2, description="One of Savoie's most artisanal and revered producers, Louis Magnin and his wife Béatrice farm their Chignin vineyards without chemicals, producing exceptionally pure and site-expressive Chignin-Bergeron (Roussette/Marsanne) whites and Mondeuse reds that represent the pinnacle of traditional Savoie winemaking.")
prod2b, new2b = PROD("Louis Magnin Chignin-Bergeron Savoie AOC", "wine_still", p2b, r2, "France",
    subcategory="Roussanne",
    description="A benchmark Savoie white from Roussanne (called Bergeron locally) on the limestone slopes above Chignin — rich and textured with apricot, white flowers, Alpine mineral and honey character; one of France's most distinctive and undervalued whites with excellent aging potential.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Gratin dauphinois with Beaufort cheese", "complement", "classic", "main", "The wine's richness and Alpine mineral character match the cream-potato-cheese gratin that the adjacent Dauphiné region made famous, creating a cross-Alpine pairing of perfect regional logic.")
    PAIR(prod2b, "Seared scallops with saffron and cream", "complement", "established", "main", "Roussanne's rich apricot character and textural depth match scallop sweetness while the wine's underlying acidity cuts through cream and saffron.")
    PAIR(prod2b, "Chicken fricassee with morel mushrooms and cream", "complement", "classic", "main", "The wine's apricot and honey notes find natural harmony with cream sauce and earthy morels in this Alpine French classic preparation.")
    PAIR(prod2b, "Reblochon de Savoie cheese with mountain honey", "complement", "classic", "cheese", "Savoie's most celebrated washed-rind cheese with its most distinctive white wine — both products of the same Alpine pastures and mountain terroir — create one of France's most regionally coherent pairings.")

# ── 3. Saumur-Champigny (France/Loire) ────────────────────────────────────────
print("\n=== Saumur-Champigny (France) ===")
r3 = R("Saumur-Champigny", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Saumur-Champigny AOC",
    reputation_tier="respected",
    quality_trajectory="established",
    description="The Loire Valley's most celebrated red wine appellation, producing elegant and aromatic Cabernet Franc from the tuffeau limestone plateau and slopes above the Saumur valley. Saumur-Champigny Cabernet Franc expresses the Loire's most distinctive red wine character — precise red fruit, violet, graphite and the characteristic chalky mineral finish that comes from the region's unique tuffeau subsoil. At its best it rivals Chinon for Loire's finest Cab Franc title.",
    key_producers="Domaine Filliatreau, Clos Rougeard, Domaine des Roches Neuves, Domaine de la Paleine",
    historical_context="Saumur-Champigny has produced red wine from Cabernet Franc since at least the 17th century, when the tuffeau caves beneath the plateau were already used for cellaring. The AOC was established in 1967, distinguishing the finest red-wine villages from the generic Saumur appellation. The legendary estate Clos Rougeard — farmed by the Foucault brothers for decades with obsessive quality focus — established Saumur-Champigny's international reputation as one of France's great Cab Franc appellations before selling to the Bouygues group in 2017.")

VIN(r3, 2023, "excellent", "stable", "Outstanding Loire vintage; Cabernet Franc of exceptional aromatic finesse and graphite mineral precision")
VIN(r3, 2022, "very_good", "stable", "Warm and generous; rich Cab Franc with soft tannins and excellent drinking appeal")
VIN(r3, 2021, "excellent", "stable", "Precise and linear; one of the decade's finest Saumur-Champigny vintages")
VIN(r3, 2020, "very_good", "stable", "Good concentration with the Loire's characteristic fresh acidity preserved")
VIN(r3, 2019, "excellent", "rising", "Concentrated and structured; age-worthy Saumur-Champigny of genuine complexity")

p3a = P("Domaine des Roches Neuves", "France", r3, description="One of Saumur-Champigny's most celebrated and consistent estates, Thierry Germain produces meticulous biodynamic Cabernet Franc wines that combine elegance with depth, achieving international recognition as the appellation's benchmark producer alongside the legendary Clos Rougeard.")
prod3a, new3a = PROD("Domaine des Roches Neuves Terres Chaudes Saumur-Champigny AOC", "wine_still", p3a, r3, "France",
    subcategory="Cabernet Franc",
    description="The flagship cuvée from one of Saumur-Champigny's finest biodynamic estates — Terres Chaudes (warm soils) produces a concentrated, complex Cabernet Franc of violet, cassis and graphite character with the chalk-mineral backbone of the tuffeau terroir and genuine aging potential of 10–15 years.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Roasted Loire Valley pigeon with peas and lardons", "complement", "classic", "main", "The wine's violet and red fruit character finds its Loire partner in roasted pigeon — a classic Loire pairing of regional logic and classical French gastronomy.")
    PAIR(prod3a, "Grilled Anjou lamb chops with rosemary", "complement", "classic", "main", "Cabernet Franc's herbal character and graphite tannins with Loire lamb make one of France's most natural regional pairings — both products of the same river valley terroir.")
    PAIR(prod3a, "Duck confit with lentilles du Puy", "complement", "established", "main", "The wine's structured tannins and earthy depth handle duck confit's richness with aplomb while the lentil earthiness bridges the tuffeau mineral character.")
    PAIR(prod3a, "Aged Selles-sur-Cher goat cheese with honey", "complement", "classic", "cheese", "Loire's definitive cheese pairing — the regional Cabernet Franc with its most celebrated goat cheese, the wine's red fruit and mineral character complementing the chalky cheese's tang.")

p3b = P("Domaine Filliatreau", "France", r3, description="The most historically significant Saumur-Champigny producer and the estate that created modern Vieilles Vignes (old vine) quality standards for the appellation, Paul Filliatreau's estate farms some of the Loire Valley's oldest Cabernet Franc vines to produce wines of extraordinary concentration and longevity.")
prod3b, new3b = PROD("Domaine Filliatreau Vieilles Vignes Saumur-Champigny AOC", "wine_still", p3b, r3, "France",
    subcategory="Cabernet Franc",
    description="The benchmark old-vine Saumur-Champigny — from Filliatreau's 50–80 year old Cabernet Franc vines on prime tuffeau plateau soils — showing exceptional concentration, violet and cassis depth, silky tannins and the mineral chalk signature of the appellation at its most authentic and compelling.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Braised rabbit with mustard and tarragon", "complement", "classic", "main", "Loire's classic lapin a la moutarde with the valley's signature red grape — the wine's herbal Cab Franc character and bright acidity frame rabbit's delicate flesh and mustard's heat.")
    PAIR(prod3b, "Tarte aux champignons with Gruyere", "complement", "established", "main", "Savory mushroom and cheese tart finds its perfect Loire companion in the earthy, structured Cab Franc whose mineral depth completes the earthiness.")
    PAIR(prod3b, "Charcuterie platter with rillettes and cornichons", "complement", "classic", "starter", "Loire Valley charcuterie — pork rillettes, pate and cornichons — are the traditional companion to this style of Cab Franc; the wine's acidity cuts through fat while its fruit bridges the cured meat.")
    PAIR(prod3b, "Poulet roti with garlic and thyme", "complement", "classic", "main", "Simple roast chicken with the region's Cab Franc is the most universal and historically authentic Loire Valley pairing of all.")

# ── 4. Ribeiro (Spain/Galicia) ────────────────────────────────────────────────
print("\n=== Ribeiro (Spain) ===")
r4 = R("Ribeiro", "Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Ribeiro DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="One of Galicia's most ancient wine appellations in northwest Spain, producing crisp, aromatic whites from indigenous varieties Treixadura, Torrontés, Godello and Lado — making Ribeiro one of Spain's most exciting white wine regions alongside Rías Baixas. The Miño River valley's granitic soils, Atlantic influence and indigenous varieties create wines of mineral precision and aromatic complexity that are gaining significant international attention from sommeliers seeking alternatives to Albariño.",
    key_producers="Emilio Rojo, Coto de Gomariz, Viña Mein, Pazo do Mar",
    historical_context="Ribeiro's wine tradition extends to pre-Roman Celtic settlements in Galicia. In the Middle Ages, Ribeiro wines were exported from the port of Vigo throughout northern Europe, rivalling Rioja in prestige. The 20th century saw the region fall victim to the same mass-production spiral as many Spanish appellations; a quality renaissance since the 1990s led by producers recovering native varieties has restored Ribeiro to international relevance and established it as Galicia's most authentic indigenous white wine heritage.")

VIN(r4, 2023, "excellent", "stable", "Outstanding Atlantic vintage; Treixadura of exceptional mineral precision and aromatic complexity")
VIN(r4, 2022, "very_good", "stable", "Good year with balanced ripeness; aromatic Godello and textured Treixadura")
VIN(r4, 2021, "excellent", "stable", "Precise and mineral; excellent acidity retention across all indigenous white varieties")
VIN(r4, 2020, "very_good", "stable", "Ripe and generous with the characteristic Galician freshness preserved")
VIN(r4, 2019, "excellent", "rising", "One of Ribeiro's finest vintages; concentrated, mineral whites of genuine aging potential")

p4a = P("Emilio Rojo", "Spain", r4, description="The legendary artisan producer who single-handedly elevated Ribeiro's international profile, Emilio Rojo farms biodynamically without chemicals and produces tiny quantities of a single wine — his pure Treixadura-based blend — that is considered one of Galicia's greatest white wines and has inspired a generation of indigenous variety revival across northwest Spain.")
prod4a, new4a = PROD("Emilio Rojo Ribeiro DO", "wine_still", p4a, r4, "Spain",
    subcategory="Treixadura, Torrontés, Lado, Godello, Loureira",
    description="One of Spain's most sought-after and cult white wines — Emilio Rojo's single bottling from organically farmed indigenous Galician varieties showing extraordinary mineral tension, Atlantic salinity, citrus peel, white flower and granite mineral character; produced in tiny quantities from old vines at yields that make most vignerons weep.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Pulpo a la gallega with smoked paprika and potatoes", "complement", "classic", "main", "Galicia's most iconic dish — tender octopus on potato with smoked paprika — and its most celebrated white wine; Atlantic mineral character and saline freshness form an inseparable regional bond.")
    PAIR(prod4a, "Percebes barnacles steamed with sea water", "complement", "classic", "starter", "The wine's oceanic mineral precision and Atlantic salinity are the natural partner for Galicia's most extraordinary and expensive crustacean product.")
    PAIR(prod4a, "Caldo gallego with white beans and turnip greens", "complement", "established", "main", "The wine's mineral freshness and aromatic lift contrast the earthy warmth of Galicia's most comforting traditional soup in an authentic regional pairing.")
    PAIR(prod4a, "Grilled sole with lemon and olive oil", "complement", "classic", "main", "Atlantic flatfish with Galicia's most mineral white — both expressing the ocean in different registers — create one of northwest Spain's most elemental and harmonious pairings.")

p4b = P("Coto de Gomariz", "Spain", r4, description="One of Ribeiro's most innovative and quality-focused estates, producing an impressive range of single-vineyard and blended whites that have helped establish the DO as a serious fine wine region, with meticulous work recovering near-extinct indigenous Galician varieties alongside Treixadura and Godello.")
prod4b, new4b = PROD("Coto de Gomariz Treixadura Ribeiro DO", "wine_still", p4b, r4, "Spain",
    subcategory="Treixadura",
    description="A benchmark single-varietal expression of Treixadura — Ribeiro's most noble indigenous grape — showing citrus, white peach, chamomile and distinctive granite mineral character that makes Ribeiro's finest whites unique in the world of Spanish wine.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Empanada gallega de atun with piquillo peppers", "complement", "classic", "main", "The wine's citrus freshness and mineral lift complement the tuna-filled Galician pastry with bright acidity that cuts through the buttery pastry crust.")
    PAIR(prod4b, "Grilled scallops with Galician butter and herbs", "complement", "classic", "main", "Atlantic scallops with local Galician herb butter find their most authentic regional companion in the mineral, fresh Treixadura.")
    PAIR(prod4b, "Vieiras gratinadas with jamón and breadcrumbs", "complement", "established", "main", "Galicia's classic baked scallop preparation with cured ham and breadcrumbs — the wine's freshness cuts through the richness while its mineral character amplifies the scallop sweetness.")
    PAIR(prod4b, "Tetilla cheese with membrillo quince paste", "complement", "classic", "cheese", "Galicia's famous mild, creamy cow's milk cheese and quince paste find their natural companion in the fresh, mineral Treixadura whose acidity balances the cheese's richness perfectly.")

# ── 5. Limari Valley (Chile) ──────────────────────────────────────────────────
print("\n=== Limari Valley (Chile) ===")
r5 = R("Limari Valley", "Chile",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Valle del Limarí DO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="Chile's most exciting cool-climate wine discovery — a coastal desert valley in Coquimbo Region, 400km north of Santiago, where Pacific Ocean fog and cooling breezes penetrate 75km inland to moderate the desert heat. Limarí's calcium carbonate (limestone) soils are unique in Chile, producing Chardonnay and Pinot Noir of extraordinary mineral precision that has drawn comparison with Burgundy. The region is Chile's most internationally celebrated emerging white wine frontier.",
    key_producers="Casa Tamaya, Hacienda Araucano, Tabali, Concha y Toro Limarí Project",
    historical_context="Limarí was considered too dry and hot for fine wine until the late 1990s when researchers discovered that coastal fog and cold ocean currents could dramatically moderate daytime temperatures. The limestone soils — rare in Chile where granite and alluvial soils dominate — proved ideal for mineral-driven Chardonnay and aromatic varieties. The region's first commercial vineyard was planted in 1998; by 2010 Limarí Chardonnay had attracted global attention and established Chile's most unexpected wine success story.")

VIN(r5, 2023, "excellent", "stable", "Outstanding Pacific-influenced year; Chardonnay of exceptional mineral precision and Burgundian tension")
VIN(r5, 2022, "very_good", "stable", "Good coastal cooling; aromatic white varieties and elegant Pinot Noir showing Limarí character")
VIN(r5, 2021, "excellent", "stable", "Benchmark Limarí vintage; concentrated, mineral Chardonnay of remarkable complexity and freshness")
VIN(r5, 2020, "very_good", "stable", "Reliable year with good limestone mineral character preserved across whites and reds")
VIN(r5, 2019, "excellent", "rising", "One of Limarí's finest vintages; Pacific-influenced Chardonnay of world-class precision")

p5a = P("Tabali", "Chile", r5, description="One of the Limarí Valley's most committed and internationally recognised producers, Tabali's focus on the valley's unique limestone terroir and Pacific Ocean influence has produced benchmark Chardonnay and Pinot Noir that established Limarí as Chile's most exciting emerging white wine region and earned international critical acclaim.")
prod5a, new5a = PROD("Tabali Talinay Vineyard Chardonnay Limari Valley DO", "wine_still", p5a, r5, "Chile",
    subcategory="Chardonnay",
    description="Chile's most celebrated Chardonnay — from Tabali's Talinay Vineyard on pure limestone 55km from the Pacific — showing the astonishing mineral precision, citrus, green apple and Burgundy-like tension that has established Limarí as Chile's most credible destination for world-class Chardonnay.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Pacific ceviche with tiger's milk and corn", "complement", "classic", "starter", "The wine's Pacific-influenced mineral acidity and citrus character perfectly mirror the lime-cured seafood of Chilean ceviche in a pairing of coastal geographic logic.")
    PAIR(prod5a, "Grilled halibut with beurre blanc and capers", "complement", "established", "main", "The wine's Burgundy-like precision and mineral tension frame Pacific halibut with classical European elegance transposed to the Chilean coast.")
    PAIR(prod5a, "Butter-poached Chilean king crab with tarragon", "complement", "classic", "main", "Cold Pacific crab from Chile's southern waters and the coastal Chardonnay of Limarí create a wine-food pairing of stunning natural synergy.")
    PAIR(prod5a, "Aged Chilean goat cheese with honey", "complement", "established", "cheese", "The wine's mineral precision and citrus drive complement the goat milk's lactic tang while the honey bridges the wine's stone fruit notes.")

p5b = P("Hacienda Araucano", "Chile", r5, description="François Lurton's Chilean venture in the Limarí Valley, bringing Bordeaux expertise to the production of mineral-driven whites that have helped establish the valley's international reputation, with particular success in elegant Chardonnay and aromatic white varieties from limestone-rich coastal vineyards.")
prod5b, new5b = PROD("Hacienda Araucano Clos de Lolol Chardonnay Limari Valley", "wine_still", p5b, r5, "Chile",
    subcategory="Chardonnay",
    description="François Lurton's Chilean flagship Chardonnay from Limarí limestone vineyards — combining French winemaking precision with Chile's unique Pacific-cooled limestone terroir to produce an elegant, mineral-driven Chardonnay of international quality and distinctive Chilean coastal character.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Grilled Patagonian sea bass with citrus butter", "complement", "classic", "main", "Chilean sea bass from cold southern waters with the country's finest coastal Chardonnay — Pacific mineral character shared between wine and fish creates outstanding harmony.")
    PAIR(prod5b, "Loco abalone with garlic and parsley", "complement", "classic", "main", "Chile's prized coastal abalone with the Limarí's most minerally precise white — both expressions of the Pacific in their respective registers.")
    PAIR(prod5b, "Steamed mussels with white wine and saffron cream", "complement", "established", "main", "Atlantic bivalves and the wine's mineral acidity create a Franco-Chilean coastal pairing with the saffron cream bridging the wine's stone fruit notes.")
    PAIR(prod5b, "Avocado tostadas with Chilean sea salt and lime", "complement", "suggested", "casual", "Chile's beloved avocado with a mineral white from the same coastal region — the wine's citrus freshness bridges the creamy avocado while the mineral finish mirrors the sea salt.")
# Ensure 4th pairing exists in case of re-run after partial failure
cur.execute("SELECT COUNT(*) FROM pairing_intelligence WHERE beverage_product_id=%s", (prod5b,))
if cur.fetchone()[0] < 4:
    PAIR(prod5b, "Avocado tostadas with Chilean sea salt and lime", "complement", "suggested", "casual", "Chile's beloved avocado with a mineral white from the same coastal region — the wine's citrus freshness bridges the creamy avocado while the mineral finish mirrors the sea salt.")

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
