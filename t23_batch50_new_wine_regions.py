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

# ── 1. Frascati DOC (Italy/Lazio) ────────────────────────────────────────────
print("\n=== Frascati DOC (Italy) ===")
r1 = R("Frascati DOC", "Italy",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Frascati DOC",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Lazio's most famous white wine appellation in the Castelli Romani hills southeast of Rome, producing crisp Malvasia and Trebbiano blends with volcanic mineral character. Long associated with Roman trattoria culture and everyday drinking, the region has modernised significantly with quality-focused producers elevating Frascati's profile beyond its bistro reputation.",
    key_producers="Fontana Candida, Villa Simone, Castel de Paolis, Conte Zandotti",
    historical_context="Frascati's hillside vineyards on volcanic tufa soils were prized by Roman emperors and the medieval papacy. The wine became synonymous with simple Roman hospitality and 20th-century mass production; a quality renaissance since the 1990s led by Villa Simone has restored its reputation as a genuine expression of Lazio's terroir.")

VIN(r1, 2023, "very_good", "stable", "Fresh and citrus-driven with lively acidity; ideal drinking from release")
VIN(r1, 2022, "very_good", "stable", "Ripe and full with stone fruit and volcanic minerality; accessible and crowd-pleasing")
VIN(r1, 2021, "excellent", "stable", "Elegant and balanced with fine aromatic complexity; best vintage of recent years")
VIN(r1, 2020, "good", "stable", "Generous and approachable with good fruit concentration; straightforward and enjoyable")
VIN(r1, 2019, "excellent", "stable", "Crisp and precise with benchmark Frascati Superiore character; excellent value")

p1a = P("Fontana Candida", "Italy", r1, description="Italy's largest and most recognised Frascati producer, part of the GIV group, producing benchmark expressions of the appellation with consistent quality at scale and pioneering the Frascati Superiore DOCG category.")
prod1a, new1a = PROD("Fontana Candida Terre dei Grifi Frascati Superiore DOCG", "wine_still", p1a, r1, "Italy",
    subcategory="Malvasia Puntinata, Trebbiano",
    description="The flagship single-vineyard Frascati Superiore from Fontana Candida's oldest vines, showing remarkable depth of yellow fruit, white flowers and volcanic minerality rarely associated with the appellation.",
    price_tier="mid_range")
if new1a:
    PAIR(prod1a, "Roman-style cacio e pepe pasta", "bridge", "classic", "main", "The volcanic minerality and crisp acidity cut through the rich pecorino and pepper, while the textural weight matches the pasta's richness.")
    PAIR(prod1a, "Fried artichokes alla giudia", "complement", "classic", "starter", "Lazio's iconic Jewish-Roman dish finds its perfect local partner; the wine's herbal notes and fresh acidity lift the fried vegetable's richness.")
    PAIR(prod1a, "Prosciutto di Parma with melon", "complement", "established", "starter", "Gentle fruit sweetness and savoury minerality bridge the sweet melon and salty cured ham in a classic antipasto pairing.")
    PAIR(prod1a, "Grilled branzino with lemon and capers", "complement", "classic", "main", "Bright citrus acidity mirrors the lemon dressing while the mineral finish complements the delicate sea bass flesh.")

p1b = P("Villa Simone", "Italy", r1, description="The quality leader of modern Frascati, founded by Piero Costantini, whose meticulous vineyard work and single-vineyard selections transformed perceptions of the appellation and established Frascati as a serious white wine destination.")
prod1b, new1b = PROD("Villa Simone Vigneto Filonardi Frascati Superiore DOCG", "wine_still", p1b, r1, "Italy",
    subcategory="Malvasia Puntinata",
    description="A landmark single-vineyard Frascati from ancient low-yielding vines on volcanic tufa soils, expressing extraordinary mineral tension, complex almond and citrus aromas and a long saline finish that redefines the appellation.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Tagliatelle with white truffle", "elevate", "adventurous", "main", "The wine's profound mineral depth and almond notes create an unexpected but thrilling complement to white truffle's earthy, ethereal aromatics.")
    PAIR(prod1b, "Seared scallops with pea puree", "complement", "established", "main", "Rich saline minerality and fine acidity frame the sweet shellfish and spring vegetables with elegant precision.")
    PAIR(prod1b, "Burrata with green tomatoes", "complement", "classic", "starter", "The wine's creamy texture and bright acidity match the burrata's richness while echoing the green tomato's tart freshness.")
    PAIR(prod1b, "Mozzarella di bufala with olive oil", "bridge", "classic", "starter", "Campania's finest cheese meets Lazio's finest white in a simple yet profound pairing of volcanic terroir expressions.")

# ── 2. Luján de Cuyo (Argentina/Mendoza) ─────────────────────────────────────
print("\n=== Luján de Cuyo (Argentina) ===")
r2 = R("Luján de Cuyo", "Argentina",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Luján de Cuyo DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Argentina's first Denominación de Origen Controlada and Mendoza's most prestigious sub-region, situated at 900–1100m elevation on the Andean piedmont with ancient Malbec vines planted by immigrant families producing wines of remarkable concentration, complexity and longevity. The high altitude, diurnal temperature variation and alluvial soils create ideal conditions for Argentina's signature variety.",
    key_producers="Achaval Ferrer, Zuccardi, Catena Zapata, Vistalba, Clos de los Siete",
    historical_context="Italian and Spanish immigrants planted Malbec in Luján de Cuyo from the 1890s, establishing the old-vine heritage that defines the region today. Argentina's first DOC designation in 1989 recognised Luján de Cuyo's primacy; the global Malbec boom of the 2000s brought international attention and investment, though the best producers had always known the region's extraordinary potential.")

VIN(r2, 2023, "excellent", "stable", "Concentrated and powerful with exceptional fruit purity; Malbec showing its finest Andean character")
VIN(r2, 2022, "very_good", "stable", "Structured and age-worthy with fine tannins and depth; classic Luján profile")
VIN(r2, 2021, "exceptional", "rising", "Elegant and precise; widely considered one of Luján de Cuyo's finest vintages in a decade")
VIN(r2, 2020, "very_good", "stable", "Rich and generous with velvety tannins; approachable young but built to age")
VIN(r2, 2019, "excellent", "stable", "Classic Luján de Cuyo character; intense, mineral and destined for long cellaring")

p2a = P("Achaval Ferrer", "Argentina", r2, description="One of Argentina's most internationally acclaimed Malbec producers, founded in 1998 by a partnership including Roberto De la Mota. Their single-vineyard Finca series from old-vine Malbec parcels in Luján de Cuyo and Tupungato defined the benchmark for premium Argentine Malbec.")
prod2a, new2a = PROD("Achaval Ferrer Finca Mirador Malbec Luján de Cuyo", "wine_still", p2a, r2, "Argentina",
    subcategory="Malbec",
    description="A benchmark expression of a single old-vine Malbec parcel in Luján de Cuyo showing extraordinary violet concentration, dark fruit complexity, mineral tension and exceptional aging potential that established Argentine Malbec as a world-class variety.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Dry-aged Angus ribeye with chimichurri", "complement", "classic", "main", "The wine's intense dark fruit and firm tannin structure are the ideal partner for Argentina's definitive beef preparation, the vivid chimichurri herbs bridging the gap.")
    PAIR(prod2a, "Slow-braised short rib with Andean potato gratin", "complement", "classic", "main", "Rich braised beef collagen softens the wine's grippy tannins while the wine's concentration matches the dish's depth.")
    PAIR(prod2a, "Empanadas de carne with spiced beef filling", "complement", "established", "starter", "The wine's concentrated dark fruit and savoury depth mirror the richly spiced filling with authentic Argentine harmony.")
    PAIR(prod2a, "Asado-grilled lamb cutlets with salsa criolla", "complement", "established", "main", "Fire-kissed lamb fat and bright tomato salsa cleanse the palate between sips of this profound Malbec.")

p2b = P("Zuccardi Valle de Uco", "Argentina", r2, description="The Zuccardi family's pursuit of terroir expression in Mendoza's sub-regions culminated in their Valle de Uco project, achieving international recognition as one of Argentina's finest wine estates and winning the title of Best Winery in the World from Wine Enthusiast.")
prod2b, new2b = PROD("Zuccardi Concreto Malbec Luján de Cuyo", "wine_still", p2b, r2, "Argentina",
    subcategory="Malbec",
    description="A radical winemaking statement from Zuccardi, fermenting and ageing Malbec entirely in concrete tanks to express pure Luján de Cuyo terroir without oak influence — showing remarkable mineral precision, textural richness and the purest expression of Andean Malbec character.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Grilled provoleta cheese with oregano and chilli", "complement", "established", "starter", "The wine's mineral freshness and restrained fruit complement the smoky melted cheese without overwhelming its delicate flavour.")
    PAIR(prod2b, "Rack of pork with Andean herbs and quinoa", "complement", "established", "main", "The concrete-aged Malbec's purity and freshness cut through pork richness while the herbal notes link beautifully.")
    PAIR(prod2b, "Wild boar ragu with pappardelle", "complement", "adventurous", "main", "The gamey intensity of wild boar finds a precise mineral counterpart in this pure-fruited, unoaked Malbec.")
    PAIR(prod2b, "Aged Manchego with quince paste", "bridge", "established", "cheese", "Nutty aged cheese and sweet-tart quince bridge the wine's mineral fruit in a classic cheese board pairing.")
# Ensure 4th pairing exists (inserted outside if block in case of re-run after partial failure)
cur.execute("SELECT COUNT(*) FROM pairing_intelligence WHERE beverage_product_id=%s", (prod2b,))
if cur.fetchone()[0] < 4:
    PAIR(prod2b, "Aged Manchego with quince paste", "bridge", "established", "cheese", "Nutty aged cheese and sweet-tart quince bridge the wine's mineral fruit in a classic cheese board pairing.")

# ── 3. Virginia AVA (USA) ─────────────────────────────────────────────────────
print("\n=== Virginia AVA (USA) ===")
r3 = R("Virginia AVA", "USA",
    beverage_family="wine",
    designation_type="AVA",
    designation_name="Virginia",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="America's oldest wine-producing state has become one of its most exciting emerging regions, with Bordeaux varieties, Viognier and Petit Manseng thriving in the Blue Ridge foothills and Shenandoah Valley. Virginia's continental climate with humid summers demands careful canopy management; the finest estates have achieved international recognition producing wines of genuine complexity and aging potential.",
    key_producers="RdV Vineyards, Barboursville Vineyards, Linden Vineyards, Michael Shaps",
    historical_context="Thomas Jefferson planted European vinifera at Monticello from 1774, dreaming of great American wine but battling phylloxera and fungal disease. Modern Virginia wine began in earnest in the 1970s; Gabriele Rausse's work establishing Barboursville and Jim Law at Linden proved the region's potential, while RdV's world-class debut in 2011 announced Virginia had arrived on the global stage.")

VIN(r3, 2023, "very_good", "stable", "Vibrant and fresh with excellent varietal expression across Virginia's diverse appellations")
VIN(r3, 2022, "excellent", "stable", "Concentrated and structured; widely regarded as a benchmark Virginia vintage")
VIN(r3, 2021, "excellent", "stable", "Elegant and precise with fine balance and exceptional aging potential")
VIN(r3, 2020, "good", "stable", "Rich and generous; producers navigated harvest challenges to produce solid wines")
VIN(r3, 2019, "very_good", "stable", "Classic Virginia character; complex, structured and age-worthy across all varieties")

p3a = P("RdV Vineyards", "USA", r3, description="Virginia's most acclaimed winery, producing small-lot Bordeaux blends from its Delaplane estate that have garnered international recognition and established Virginia as a world-class wine region. Founded by Rutger de Vink, RdV is Virginia's most sought-after and consistently top-rated producer.")
prod3a, new3a = PROD("RdV Vineyards Lost Mountain Red Blend Virginia", "wine_still", p3a, r3, "USA",
    subcategory="Cabernet Franc, Merlot, Cabernet Sauvignon",
    description="Virginia's most celebrated red wine — a Bordeaux-inspired blend from RdV's Delaplane estate showing extraordinary complexity, graphite minerality, cassis depth and silky tannin structure that rivals top Napa and Pomerol producers at their level.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Braised duck leg with black cherry reduction", "complement", "classic", "main", "The wine's Cab Franc-driven red fruit and fine tannins elevate braised duck in a pairing of classical Bordelais inspiration adapted to Virginia's terroir.")
    PAIR(prod3a, "Herb-crusted rack of lamb with rosemary jus", "complement", "classic", "main", "Virginia's premier red finds its natural companion in lamb — the wine's herbal Cab Franc notes and elegant structure frame the meat with aristocratic precision.")
    PAIR(prod3a, "Venison tenderloin with roasted root vegetables", "complement", "adventurous", "main", "The wine's earthy complexity and firm tannins match Virginia venison's wild gamey character in a regionally authentic pairing.")
    PAIR(prod3a, "Aged Virginia cheddar with fig jam", "bridge", "established", "cheese", "Local aged cheddar's nutty sharpness and sweet fig bridge the wine's dark fruit and savouriness in a Virginia-proud pairing.")

p3b = P("Barboursville Vineyards", "USA", r3, description="Virginia's historic benchmark winery founded on land once owned by Thomas Jefferson's friend Governor James Barbour, now owned by the Italian Zonin family. Winemaker Luca Paschina's Italian-Virginia synthesis has produced some of the state's most consistent and complex wines for four decades.")
prod3b, new3b = PROD("Barboursville Vineyards Octagon Red Virginia", "wine_still", p3b, r3, "USA",
    subcategory="Merlot, Cabernet Franc, Petit Verdot",
    description="Virginia's original iconic red blend and benchmark for the state, produced continuously since 1999 from Barboursville's estate vineyards, showing Merlot-led richness, Cab Franc spice and a distinctive Virginia minerality that has inspired a generation of winemakers.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Seared duck breast with cherry and thyme", "complement", "classic", "main", "Merlot-dominant richness and Cab Franc spice find their mirror in duck's rich fat and cherry-based sauce in a Bordelais-inspired pairing.")
    PAIR(prod3b, "Pork tenderloin with apple and sage", "complement", "established", "main", "The wine's rounded fruit and herbal spice complement the pork's sweetness and sage's aromatic earthiness.")
    PAIR(prod3b, "Mushroom and truffle risotto", "bridge", "established", "main", "Merlot's earthy depth bridges beautifully with truffle and porcini mushroom's umami richness in a satisfying vegetarian pairing.")
    PAIR(prod3b, "Hard cheese board with Virginia honey", "bridge", "classic", "cheese", "Local aged cheeses and wildflower honey echo the wine's complexity while its tannins cleanse the palate between bites.")

# ── 4. Txakoli de Getaria (Spain/Basque Country) ──────────────────────────────
print("\n=== Txakoli de Getaria (Spain) ===")
r4 = R("Txakoli de Getaria", "Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Getariako Txakolina DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The Basque Country's most distinctive wine appellation producing ferociously crisp, low-alcohol, lightly sparkling white and rosé wines from the indigenous Hondarrabi Zuri grape grown on steep Atlantic-facing slopes above the Bay of Biscay. Txakoli's bracing acidity, saline minerality and gentle effervescence make it the definitive aperitif for pintxos culture and fresh seafood.",
    key_producers="Txomin Etxaniz, Ameztoi, Bodega Talai-Berri, Hiruzta",
    historical_context="Txakoli has been produced in the Basque Country for centuries, nearly disappearing in the 20th century before a revival in the 1980s led by dedicated producers who established the Getariako Txakolina DO in 1990. The wine's unique character — so tied to Basque culinary identity and the txotx pouring ritual — has made it a symbol of regional pride and gastronomic culture worldwide.")

VIN(r4, 2023, "excellent", "stable", "Exceptionally fresh and saline with vibrant citrus energy; one of the finest recent Txakoli vintages")
VIN(r4, 2022, "very_good", "stable", "Ripe and aromatic with fine effervescence and characteristic Atlantic minerality")
VIN(r4, 2021, "very_good", "stable", "Precise and linear with intense salinity and green apple; classic Txakoli profile")
VIN(r4, 2020, "good", "stable", "Full-bodied for Txakoli with fine acidity and peach notes; a warmer year than usual")
VIN(r4, 2019, "excellent", "stable", "Classic vintage; focused and mineral with long saline finish; benchmark Txakolina")

p4a = P("Txomin Etxaniz", "Spain", r4, description="The most internationally recognised Txakoli producer and the benchmark for Getariako Txakolina, a multi-generational Basque family estate whose meticulous Atlantic-slope viticulture and consistent quality helped establish the DO and bring global attention to this unique white wine tradition.")
prod4a, new4a = PROD("Txomin Etxaniz Txakoli de Getaria", "wine_still", p4a, r4, "Spain",
    subcategory="Hondarrabi Zuri",
    description="The definitive expression of Getariako Txakolina — an explosively fresh, lightly effervescent Basque white with bracing Atlantic acidity, intense saline minerality, green apple and citrus character and a piercing finish that cleanses the palate perfectly for the next pintxo.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Anchoas del Cantabrico on toast", "complement", "classic", "starter", "Briny Cantabrian anchovies and the wine's saline Atlantic minerality create one of Basque cuisine's most elemental and thrilling pairings.")
    PAIR(prod4a, "Gambas al ajillo with crusty bread", "complement", "classic", "starter", "The wine's vibrant acidity and citrus freshness cut through garlic-infused olive oil while complementing the sweet prawn flesh.")
    PAIR(prod4a, "Oysters with lemon and mignonette", "complement", "classic", "starter", "The wine's natural effervescence, saline mineral character and crisp acidity are a near-perfect match for fresh oysters.")
    PAIR(prod4a, "Bonito del Norte tuna with piquillo peppers", "complement", "classic", "main", "Basque tuna and its defining wine appellation create an expression of regional identity — the wine's freshness perfectly frames the tuna's richness.")

p4b = P("Ameztoi", "Spain", r4, description="One of the most exciting and innovative Txakoli producers, known for their Rubentis rosé Txakoli made from the rare Hondarrabi Beltza red grape — a pioneering wine that brought new attention to Basque rosé production and demonstrated Txakoli's versatility beyond the classic white style.")
prod4b, new4b = PROD("Ameztoi Rubentis Txakoli Rosado Getariako Txakolina", "wine_still", p4b, r4, "Spain",
    subcategory="Hondarrabi Beltza",
    description="A groundbreaking pink Txakoli from the rare indigenous Hondarrabi Beltza variety, showing vibrant strawberry and cherry fruit alongside the appellation's signature bracing acidity and saline minerality — a wine that redefined what Basque Txakoli could be.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Jamón Ibérico de bellota with pan con tomate", "complement", "established", "starter", "The rosé Txakoli's berry freshness and saline snap complement the acorn-fed ham's intense nutty savouriness with Basque-Castilian harmony.")
    PAIR(prod4b, "Octopus a la gallega with smoked paprika", "complement", "established", "starter", "The wine's vibrant acidity and fruity freshness lift the earthy smoked paprika and tender octopus in a classic Iberian pairing.")
    PAIR(prod4b, "Bacalao al pil-pil with garlic", "bridge", "established", "main", "The wine's emulsifying acidity bridges the richly gelatinous salt cod sauce while refreshing the palate with each sip.")
    PAIR(prod4b, "Grilled fresh sardines with sea salt", "complement", "classic", "main", "The rosé's berry brightness and Atlantic mineral character enhance sardine's oily richness and ocean salinity.")

# ── 5. Anjou (France/Loire Valley) ───────────────────────────────────────────
print("\n=== Anjou (France) ===")
r5 = R("Anjou", "France",
    beverage_family="wine",
    designation_type="AOC",
    designation_name="Anjou AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The historic heart of the Loire Valley wine country, centred on Angers and encompassing the Layon, Aubance and Saumur sub-regions. Anjou produces an extraordinary range of styles — bone-dry to lusciously sweet whites from Chenin Blanc, elegant reds from Cabernet Franc, and some of France's finest sweet wines from the Coteaux du Layon. The diversity of schist, tuffeau and volcanic soils creates remarkable terroir variation.",
    key_producers="Domaine des Baumard, Château Pierre Bise, Domaine de la Bergerie, Patrick Baudouin",
    historical_context="Anjou's wine heritage stretches back to the 9th century monastic vineyards; the sweet whites of the Layon were prized at the courts of Europe. The 20th century saw decline and overproduction, but a generation of quality-focused producers from the 1990s onwards — many practising biodynamics — restored Anjou's reputation as one of France's most diverse and exciting wine regions.")

VIN(r5, 2023, "very_good", "stable", "Fresh and vibrant for drier styles; excellent botrytis development for Coteaux du Layon")
VIN(r5, 2022, "excellent", "stable", "Concentrated and rich with fine natural sugar in sweet cuvées; superb across all Anjou styles")
VIN(r5, 2021, "excellent", "stable", "Elegant and precise; a benchmark for dry Anjou Blanc and Savennières")
VIN(r5, 2020, "exceptional", "rising", "Outstanding sweet wine year with superb noble rot concentration; among Anjou's finest for Coteaux du Layon")
VIN(r5, 2019, "excellent", "stable", "Classic balance of richness and acidity across all styles from dry to lusciously sweet")

p5a = P("Domaine des Baumard", "France", r5, description="Anjou's most prestigious estate and the benchmark for the appellation's finest sweet wines, particularly the legendary Quarts de Chaume and Coteaux du Layon. Jean Baumard and son Florent produce wines of exceptional longevity and elegance that rank among France's greatest dessert wines.")
prod5a, new5a = PROD("Domaine des Baumard Clos de Papillon Savennieres AOC", "wine_still", p5a, r5, "France",
    subcategory="Chenin Blanc",
    description="A landmark dry Chenin Blanc from the Savennières appellation within Anjou — from the Clos de Papillon vineyard on volcanic schist soils, producing a wine of extraordinary tension, mineral depth, beeswax complexity and piercing acidity that ages magnificently for decades.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Pan-roasted foie gras with apple and verjus", "complement", "established", "starter", "The wine's powerful acidity and mineral tension cut through foie gras richness while the apple notes link beautifully with the fruit accompaniment.")
    PAIR(prod5a, "Quenelles de brochet with sauce Nantaise", "complement", "classic", "main", "This Loire Valley classic — delicate pike dumplings in butter sauce — finds its perfect regional companion in the minerally intense Savennières.")
    PAIR(prod5a, "Aged Comté cheese at full maturity", "complement", "established", "cheese", "The wine's beeswax and oxidative complexity mirror aged Comté's nutty depth in a profoundly satisfying French classic pairing.")
    PAIR(prod5a, "Roasted turbot with beurre blanc", "complement", "classic", "main", "Loire's definitive wine-food pairing — the region's finest white with its most celebrated butter sauce preparation — a marriage of perfect harmony.")

p5b = P("Chateau Pierre Bise", "France", r5, description="One of Anjou's finest biodynamic estates run by Claude Papin, producing a remarkable range of terroir-expressive Chenin Blancs from different soils across the Anjou-Layon appellation, as well as exceptional Quarts de Chaume and Coteaux du Layon sweet wines of extraordinary concentration and elegance.")
prod5b, new5b = PROD("Chateau Pierre Bise Anjou Blanc Haut de la Garde", "wine_still", p5b, r5, "France",
    subcategory="Chenin Blanc",
    description="A benchmark expression of off-dry Anjou Chenin Blanc from ancient schist vineyards in the Layon, showing the Loire Valley's most complex white grape at its most versatile — quince, beeswax, saline mineral tension and just a whisper of natural sweetness providing extraordinary gastronomic flexibility.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "River crayfish gratin with cream and tarragon", "complement", "classic", "main", "The wine's gentle residual sweetness and mineral acidity perfectly frame the delicate crayfish and aromatic tarragon cream.")
    PAIR(prod5b, "Rillettes du Mans de Tours with cornichons", "contrast", "established", "starter", "The wine's crisp mineral acidity and touch of sweetness provide a refreshing contrast to the rich, fatty pork rillettes.")
    PAIR(prod5b, "Goats cheese from Selles-sur-Cher with walnut bread", "complement", "classic", "cheese", "Loire's most beloved pairing — the region's mineral Chenin with its most famous cheese, a textbook expression of local terroir harmony.")
    PAIR(prod5b, "Warm tarte tatin with crème fraiche", "complement", "established", "dessert", "The wine's gentle sweetness and quince fruit notes match the caramelised apple tart while the acidity prevents cloyingness.")

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
