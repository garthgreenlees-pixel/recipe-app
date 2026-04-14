#!/usr/bin/env python3
"""T23 Batch 25 — New wine regions: Chinon AOC (France), Alsace AOC (France), Cahors AOC (France), Fleurie AOC (France), Friuli Venezia Giulia DOC (Italy)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── CHINON AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Chinon AOC (France) ===")
r_chi = R("Chinon", "France", "wine",
           designation_type="AOC",
           designation_name="Chinon AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="The Loire Valley's greatest Cabernet Franc appellation and France's most versatile red wine AOC — the Vienne River confluence east of the Touraine, producing Cabernet Franc from three distinct terroirs: the gravel riverside alluvial soils (lighter, early-drinking), the tuffeau limestone hillside soils (structured, age-worthy), and the clay-plateau soils (rich, powerful). Chinon whites from Chenin Blanc are also produced. The appellation is inextricably linked with Rabelais — the 16th-century humanist author who was born in Chinon and celebrated the wine with unrestrained joy. The finest Chinon tuffeau wines age for 20+ years.",
           key_producers="Bernard Baudry, Charles Joguet, Couly-Dutheil, Domaine du Roncée, Philippe Alliet",
           historical_context="Rabelais called Chinon 'le premier vin du monde' (the world's finest wine) in Gargantua and Pantagruel in 1534, and the medieval Château de Chinon — perched above the Vienne — consumed vast quantities of local wine through the Hundred Years War. Joan of Arc first met the Dauphin Charles VII at Chinon in 1429. Charles Joguet's single-parcel Chinon bottlings in the 1970s — Clos de la Dioterie, Clos du Chêne Vert — established Chinon's fine wine credentials and introduced the concept of Loire premier cru to an international audience.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Chinon vintage; Cabernet Franc from tuffeau limestone showed extraordinary aromatic precision, structure, and long-term aging potential."),
    (2021, "very_good", "stable", "Classic Loire vintage; cool conditions produced Cabernet Franc of excellent freshness and the characteristic violet-pencil shavings complexity of great Chinon."),
    (2020, "excellent", "stable", "Benchmark year; Baudry and Alliet both produced wines of extraordinary depth from the tuffeau hillside parcels; ageability confirmed."),
    (2019, "exceptional", "rising", "Greatest Chinon vintage of the era; Cabernet Franc of legendary concentration and longevity; tuffeau limestone wines destined for 20+ year development."),
    (2018, "excellent", "stable", "Warm vintage producing generous, accessible Chinon of good concentration; gravel soils particularly successful; some tuffeau wines overripe but finest elegant."),
]:
    VIN(r_chi, yr, qd, pt, sn)

p_bau = P("Bernard Baudry", "France", r_chi,
           description="Mathieu Baudry's family estate — the benchmark for serious Chinon tuffeau limestone Cabernet Franc. The Les Grezeaux, La Croix Boissée, and Clos Guillot single-parcel wines are considered the finest Chinon produced today, demonstrating that Loire Cabernet Franc on tuffeau limestone can develop Burgundian complexity over 15+ years. Baudry's wines appear on France's finest restaurant wine lists.")
prod_bau, new = PROD("Bernard Baudry Les Grezeaux Chinon", "wine_still", p_bau, r_chi, "France",
                     subcategory="Cabernet Franc",
                     description="The benchmark for Chinon's tuffeau limestone terroir — old-vine Cabernet Franc from the Les Grezeaux parcel above the Vienne, aged in used Burgundy barrels. Red cherry, raspberry, violet, crushed chalk, pencil shavings, and a linear mineral precision that develops magnificently over 10-15 years. The definitive expression of what Chinon's finest limestone can achieve — elegant, complex, and irreplaceable.",
                     price_tier="mid_range")
if new:
    PAIR(prod_bau, "Rillons de Tours (crispy braised pork belly cubes) with Dijon mustard and lentils", "complement", "classic", "main", "The Touraine's most traditional pork preparation and its greatest Cabernet Franc — the wine's violet and chalk mineral cuts through the pork belly's rich fat; Dijon mirrors the wine's acidity; lentils bridge the mineral depth")
    PAIR(prod_bau, "Coq au Chinon (chicken braised in Chinon wine) with lardons, mushrooms, and thyme", "complement", "classic", "main", "The wine appears in the dish itself — the ultimate Chinon pairing; Cabernet Franc's acidity and red fruit character infuses the chicken braise; lardons add a savoury bridge; thyme mirrors the wine's herbal complexity")

p_jog = P("Charles Joguet", "France", r_chi,
           description="The estate that established Chinon as a fine wine region — Charles Joguet's single-parcel bottlings from the 1970s (Clos de la Dioterie from the oldest vines, Clos du Chêne Vert) introduced Burgundian precision to Loire Cabernet Franc. Now managed with the same care, Joguet's wines remain Chinon's most iconic and internationally recognized producer — particularly the Clos de la Dioterie from pre-phylloxera vines.")
prod_jog, new = PROD("Charles Joguet Clos de la Dioterie Chinon", "wine_still", p_jog, r_chi, "France",
                     subcategory="Cabernet Franc",
                     description="Chinon's most historic single-vineyard wine — Cabernet Franc from pre-phylloxera old vines on the tuffeau-clay Clos de la Dioterie parcel, enclosed by ancient stone walls. Dark cherry, dried rose, violet, earthen tuffeau mineral, cedar, and a structure built for 20 years of development. The wine that proved Loire Cabernet Franc could rival Burgundy's finest for longevity and complexity.",
                     price_tier="premium")
if new:
    PAIR(prod_jog, "Gigot d'agneau de 7 heures (7-hour braised leg of lamb) with flageolets and garlic", "complement", "classic", "main", "The great French slow-roast and Loire's greatest Cabernet Franc — the wine's structure and dark cherry supports the lamb's extraordinary gelatin depth; flageolets' earthiness bridges the tuffeau mineral")
    PAIR(prod_jog, "Crottin de Chavignol affiné (aged Loire chèvre) with fig jam and toasted walnuts", "complement", "classic", "cheese", "The Loire's famous aged goat cheese and its finest Cabernet Franc — the wine's chalk mineral mirrors the aged chèvre's concentrated lactic depth; fig jam bridges the wine's dark fruit; walnuts bridge the tannin")

# ── ALSACE AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Alsace AOC (France) ===")
r_als = R("Alsace", "France", "wine",
           designation_type="AOC",
           designation_name="Alsace AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="France's most distinctive and aromatic wine region — the long narrow valley between the Vosges mountains and the Rhine, producing Riesling, Gewurztraminer, Pinot Gris, Muscat, Sylvaner, Pinot Blanc, and Pinot Noir from 51 classified Grand Cru vineyards on granite, limestone, sandstone, schist, and volcanic soils. Alsace wines are vinified dry (or off-dry) in contrast to their German counterparts across the Rhine, and the tall flûte bottle identifies the region's distinctive varietal style. The Alsace Grand Cru system recognizes the finest terroirs; Riesling from Grand Cru Schlossberg, Brand, Schoenenbourg, and Rangen produces France's most Germanic and age-worthy white wines.",
           key_producers="Trimbach, Zind-Humbrecht, Weinbach, Hugel, Marcel Deiss, Domaine Ostertag, Albert Mann",
           historical_context="Alsace changed hands between France and Germany four times between 1870 and 1945, and the region's wine culture reflects this dual heritage — German grape varieties vinified in the French tradition of dryness. The Trimbach family has been producing wine in Ribeauvillé since 1626, making them one of France's oldest wine dynasties. Léonard Humbrecht's Clos Windsbuhl, Rangen de Thann, and Clos Häuserer single-vineyard wines, produced by his son Olivier, transformed Alsace Grand Cru into international cult wine in the 1980s. The 2001 introduction of Alsace Grand Cru Riesling at auction in New York at prices rivaling premier cru Burgundy marked the region's international arrival.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Alsace vintage; Riesling Grand Cru from granite and limestone showed extraordinary aromatic complexity; Gewurztraminer of rare mineral precision."),
    (2021, "very_good", "stable", "Classic vintage; cooler conditions produced Alsace Riesling of exceptional freshness and the Germanic mineral depth that makes great Alsace wines age-worthy."),
    (2020, "excellent", "stable", "Benchmark year; Zind-Humbrecht Rangen de Thann and Trimbach Clos Sainte Hune both produced wines of historic quality; cellar-worthy for 20+ years."),
    (2019, "exceptional", "rising", "Greatest Alsace vintage of the modern era; Riesling Grand Cru of legendary concentration and longevity; Gewurztraminer of rare mineral restraint."),
    (2018, "excellent", "stable", "Warm vintage producing generous Alsace of unusual concentration; Pinot Gris and Gewurztraminer particularly successful; some Riesling overripe but finest exceptional."),
]:
    VIN(r_als, yr, qd, pt, sn)

p_tri = P("Trimbach", "France", r_als,
           description="France's most internationally recognized Alsace producer — the Trimbach family has been producing wine since 1626 in Ribeauvillé. The Clos Sainte Hune (Riesling from a single parcel in the Rosacker Grand Cru) is considered France's greatest Riesling and one of the world's most age-worthy white wines. Trimbach's Riesling Réserve Personnelle and Gewurztraminer Cuvée des Seigneurs de Ribeaupierre are the benchmarks for their respective varieties.")
prod_tri, new = PROD("Trimbach Riesling Clos Sainte Hune", "wine_still", p_tri, r_als, "France",
                     subcategory="Riesling",
                     description="France's most revered Riesling and one of the world's great white wines — from a tiny 1.67-hectare parcel within the Rosacker Grand Cru, producing Riesling of extraordinary mineral precision, longevity (30+ years), and crystalline complexity. Petrol, lime, grapefruit, white peach, slate mineral, and a laser-like acidity that integrates over decades. At peak (15-25 years), rivals the world's finest white Burgundy.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_tri, "Choucroute garnie alsacienne with smoked pork, Strasbourg sausage, and juniper", "complement", "classic", "main", "Alsace's most iconic dish and its most iconic wine — Riesling's acidity cuts through the sauerkraut's richness and the smoked pork fat; juniper bridges the wine's mineral character; Strasbourg sausage's smoky depth finds resonance in the petrol development")
    PAIR(prod_tri, "Tarte flambée (Flammekueche) with crème fraîche, lardons, and caramelized onion", "complement", "classic", "aperitif", "Alsace's most beloved informal dish and its greatest wine — Riesling's razor acidity cuts through the crème fraîche; onion's sweetness is contrasted by the wine's mineral freshness; lardons' smoke bridges the wine's complexity")

p_zin = P("Zind-Humbrecht", "France", r_als,
           description="Olivier Humbrecht's biodynamic Alsace estate — considered by many critics the world's greatest Riesling producer outside Germany. The Grand Cru single-vineyard wines (Rangen de Thann, Clos Windsbuhl, Brand, Clos Häuserer) are internationally celebrated cult wines of extraordinary mineral complexity. Humbrecht's precision in Grand Cru terroir expression transformed Alsace's critical reputation in the 1980s and 1990s.")
prod_zin, new = PROD("Zind-Humbrecht Gewurztraminer Hengst Grand Cru", "wine_still", p_zin, r_als, "France",
                     subcategory="Gewurztraminer",
                     description="The world's benchmark for serious, mineral Gewurztraminer — from the Hengst Grand Cru's limestone and marl, biodynamically farmed. Rose petal, lychee, ginger, cinnamon, mango, and the extraordinary mineral depth that restrains Gewurztraminer's natural exuberance into something profound and age-worthy. Off-dry but with an acidity that balances the natural richness. One of France's most distinctive wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_zin, "Foie gras d'Alsace mi-cuit with Gewurztraminer gelée, pain d'épices, and mango chutney", "complement", "classic", "starter", "Alsace's most luxurious pairing — the wine appears in the gelée; Gewurztraminer's lychee and rose mirror the foie gras's floral richness; mango chutney bridges the tropical fruit; pain d'épices bridges the ginger spice")
    PAIR(prod_zin, "Munster fermier (washed-rind Alsatian cheese) with caraway seeds and rye bread", "complement", "classic", "cheese", "France's most pungent cheese and its traditional Alsatian pairing — Gewurztraminer's aromatic intensity is one of the few wines that stands up to Munster's assertiveness; caraway bridges the wine's spice; the cheese's richness is tempered by the wine's off-dry sweetness")

# ── CAHORS AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Cahors AOC (France) ===")
r_cah = R("Cahors", "France", "wine",
           designation_type="AOC",
           designation_name="Cahors AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Southwest France's 'Black Wine' AOC — the Lot River valley beneath the medieval city of Cahors, producing wines from Malbec (locally called Côt or Auxerrois, minimum 70%) on the limestone causses plateaux and alluvial gravel terraces. Cahors Malbec is the original and most characterful expression of the variety — darker, more tannic, more mineral, and more age-worthy than the Mendoza versions that made Malbec globally famous. The distinction between causses limestone (deeper, more mineral) and terrasse alluvial (richer, more approachable) parallels Chinon's tuffeau-gravel distinction.",
           key_producers="Clos Triguedina, Château du Cèdre, Château Lamartine, Clos de Gamot, Château Lagrezette",
           historical_context="Cahors was one of medieval Europe's most celebrated wines — exported from Cahors port along the Lot and Garonne rivers to Bordeaux and then to England, where it was known as 'Black Wine of Cahors.' The Black Prince and Richard II both ordered quantities for English consumption. The variety called Malbec (a corruption of 'Mal Bec' — badly named — in French) was planted in Bordeaux from Cahors cuttings. When Michel Poussel of Clos Gamot and Jean-Luc Baldès of Clos Triguedina began serious single-vineyard Malbec in the 1970s, Cahors began its modern rehabilitation. Argentina's Mendoza adopted Cahors Malbec cuttings in the 1860s — making Cahors the grandmother of Argentina's most famous export.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Cahors vintage; Malbec from limestone causses showed extraordinary dark fruit concentration and the iron-mineral depth of the finest parcels."),
    (2021, "very_good", "stable", "Classic vintage; cool Lot Valley conditions produced Malbec of excellent structure and dark cherry depth with more freshness than the warmer years."),
    (2020, "excellent", "stable", "Benchmark year; Clos Triguedina and Château du Cèdre both produced wines of historic quality; causses limestone wines destined for 15+ year aging."),
    (2019, "excellent", "rising", "Outstanding vintage; Cahors Malbec of extraordinary concentration and longevity; renewed international interest in the 'original Malbec' accelerated."),
    (2018, "very_good", "stable", "Warm vintage producing generous, accessible Cahors of good concentration; terrasse alluvial wines particularly approachable; causses wines still structured."),
]:
    VIN(r_cah, yr, qd, pt, sn)

p_tri = P("Clos Triguedina", "France", r_cah,
           description="Jean-Luc Baldès's family estate — the most internationally recognized and critically acclaimed Cahors producer. The Prince Probus cuvée from the highest-elevation limestone causses is considered France's finest Malbec and one of southwest France's most age-worthy wines. Baldès has championed Cahors's cause internationally for four decades, demonstrating that Malbec on its native Lot Valley limestone is categorically different — and arguably superior — to its Argentine descendants.")
prod_tri_c, new = PROD("Clos Triguedina Prince Probus Cahors", "wine_still", p_tri, r_cah, "France",
                        subcategory="Malbec",
                        description="The finest expression of Cahors Malbec — from the highest limestone causses parcels, this is France's benchmark for what Malbec achieves on its native terroir. Black cherry, blueberry, iron mineral, dark chocolate, cedar, and a tannin structure of extraordinary precision. Requires 10+ years to reveal its full complexity; at 15 years develops the kind of depth that makes Cahors's Black Wine legend entirely comprehensible.",
                        price_tier="premium")
if new:
    PAIR(prod_tri_c, "Cassoulet de Castelnaudary with duck confit, Toulouse sausage, and haricot beans", "complement", "classic", "main", "Southwest France's great one-pot dish and its Black Wine — Cahors Malbec's iron tannin and dark fruit stands up to cassoulet's accumulated richness; the dish's complexity meets the wine's depth")
    PAIR(prod_tri_c, "Truffade auvergnate (potato cake with Cantal and lardons) and green salad", "complement", "established", "main", "The Massif Central's comfort dish and Cahors's iron wine — Malbec's dark fruit and mineral depth bridges the potato-cheese richness; lardons' smoke mirrors the wine's complexity; green salad's acidity contrasts the tannin")

p_ced = P("Château du Cèdre", "France", r_cah,
           description="The Verhaeghe family's causses limestone Cahors estate — producing the prestigious Le Cèdre and GC (Grand Vin du Cèdre) cuvées that have transformed critical opinion of Cahors. Pascal Verhaeghe's meticulous viniculture on the limestone plateau demonstrates that Cahors Malbec on native limestone achieves a complexity and mineral depth that Mendoza cannot replicate. Château du Cèdre's wines have been placed on Parisian three-star restaurant lists.")
prod_ced, new = PROD("Château du Cèdre Le Cèdre Cahors", "wine_still", p_ced, r_cah, "France",
                     subcategory="Malbec",
                     description="The modern face of Cahors prestige — Malbec from the causse limestone plateau, aged in French oak with care and precision. Dark plum, blackberry, violets, graphite, iron ore, and a structured elegance that demonstrates why Cahors Malbec on its native limestone is fundamentally different to its Argentine offspring. More austere, more mineral, and ultimately more profound than any Mendoza equivalent.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ced, "Confit de canard avec sarladaises (duck confit with potato and garlic gratin)", "complement", "classic", "main", "Périgord's most celebrated preparation and Cahors's iron wine — the wine's dark fruit and mineral tannin is perfectly matched by the duck confit's extraordinary richness; sarladaises' garlic bridges the wine's complexity")
    PAIR(prod_ced, "Magret de canard fumé (smoked duck breast) with walnut oil, mâche, and Périgord walnut", "complement", "classic", "starter", "The Dordogne tradition and the Lot Valley wine — Cahors Malbec's dark fruit and iron character bridges smoked duck's intensity; walnut bridges the wine's mineral depth; mâche's nuttiness complements the oak")

# ── FLEURIE AOC (FRANCE) ──────────────────────────────────────────
print("\n=== Fleurie AOC (France) ===")
r_fle = R("Fleurie", "France", "wine",
           designation_type="AOC",
           designation_name="Fleurie AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Beaujolais's most feminine and internationally beloved cru — the granite hillsides of Fleurie in the heart of the Haut-Beaujolais producing Gamay of extraordinary aromatic delicacy, floral intensity, and silky texture. Fleurie wines smell of violets, peony, wild strawberry, and red cherry, with a mid-palate richness from the pink granite soils that sets them apart from other Beaujolais crus. Unlike Moulin-à-Vent's structured, age-worthy style, Fleurie prioritizes freshness and aromatic vibrancy — the most hedonistic of the Beaujolais crus at their best.",
           key_producers="Domaine Chignard, Château des Deduits, Château du Grand Pré, Domaine de la Madone, Clos de la Roilette",
           historical_context="Fleurie's 'feminine' reputation — established by generations of négociant marketing — initially undervalued the appellation's capacity for serious wine. The creation of the La Madone chapel at the hill's summit in 1875 (dedicated to the local patroness) gave the appellation its most iconic landmark. Domaine Chignard's meticulous single-parcel approach in the 1980s demonstrated that Fleurie granite could produce structured, age-worthy Gamay rather than simple early-drinking red. The natural wine movement's embrace of Beaujolais crus — particularly at Paris bistros like Le Verre Volé — transformed Fleurie's image from mass-market rosé alternative to serious terroir wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Fleurie vintage; Gamay from pink granite showed extraordinary aromatic intensity and the characteristic Fleurie violet-peony floral complexity."),
    (2021, "very_good", "stable", "Classic vintage; cool Beaujolais conditions produced Fleurie of excellent freshness, silky texture, and the delicate floral character that defines the cru."),
    (2020, "excellent", "stable", "Benchmark year; Chignard and Clos de la Roilette both produced wines of unusual depth for Fleurie; granite soils expressed themselves with rare mineral clarity."),
    (2019, "exceptional", "rising", "Greatest Fleurie vintage of the era; Gamay of extraordinary aromatic complexity and rare ageability; the cru's international reputation reached new heights."),
    (2018, "very_good", "stable", "Warm vintage producing generous Fleurie of good concentration; floral character intact despite heat; easy-drinking style particularly appealing."),
]:
    VIN(r_fle, yr, qd, pt, sn)

p_chi = P("Domaine Chignard", "France", r_fle,
           description="Michaël Chignard's small estate — the producer that established Fleurie's credibility as a serious cru wine. The Clos des Moriers single-parcel wine from the oldest pink granite vines is considered Fleurie's most age-worthy and complex wine. Chignard's disciplined approach to low yields and precise harvesting has produced Gamay wines that develop magnificent complexity over 5-8 years — quite unlike the simple, early-drinking stereotype of the appellation.")
prod_chi, new = PROD("Domaine Chignard Fleurie Clos des Moriers", "wine_still", p_chi, r_fle, "France",
                     subcategory="Gamay",
                     description="Fleurie's most serious and age-worthy expression — old-vine Gamay from the pink granite Clos des Moriers parcel, aged in used oak. Violet, wild strawberry, raspberry, rose petal, and the granitic mineral freshness that gives Fleurie its ethereal quality. More structured and age-worthy than typical Fleurie; develops magnificently over 5-7 years into something resembling light Pinot Noir from Burgundy. The definitive argument that Beaujolais cru is serious wine.",
                     price_tier="mid_range")
if new:
    PAIR(prod_chi, "Quenelles de brochet (pike dumplings) with Nantua sauce and freshwater crayfish", "complement", "classic", "main", "Lyon's most celebrated preparation and its Beaujolais cru — Fleurie's silky texture and floral character bridges the quenelle's delicate richness; crayfish amplify the freshwater character; Nantua's cream is cut by the wine's granite freshness")
    PAIR(prod_chi, "Charcuterie lyonnaise — saucisson de Lyon, rosette, and groin de cochon with cornichons", "complement", "classic", "starter", "The Lyonnais tradition of charcuterie and Beaujolais — Fleurie's violet and wild strawberry character bridges the various pork preparations; cornichons' acidity mirrors the wine's fresh acidity")

p_roi = P("Clos de la Roilette", "France", r_fle,
           description="The Coudert family's Fleurie estate producing one of the cru's most internationally recognized wines — the Clos de la Roilette from the highest-elevation pink granite parcels. The wine demonstrates Fleurie's capacity for both immediate pleasure and 5-8 years of development, combining the appellation's characteristic floral vibrancy with genuine mineral structure from the granitic soils.")
prod_roi, new = PROD("Clos de la Roilette Fleurie", "wine_still", p_roi, r_fle, "France",
                     subcategory="Gamay",
                     description="One of Fleurie's most beloved and internationally distributed wines — old-vine Gamay from the high-altitude pink granite Clos de la Roilette. Raspberry, violet, peony, red cherry, and the granite mineral freshness that makes this the ideal demonstration of what makes Fleurie's pink granite unique in the Beaujolais crus. Approachable from vintage but with the structure to develop over 5 years.",
                     price_tier="mid_range")
if new:
    PAIR(prod_roi, "Poulet de Bresse rôti (roast Bresse chicken) with tarragon jus and haricots verts", "complement", "classic", "main", "France's finest chicken and Beaujolais's most floral wine — Fleurie's delicate violet and raspberry character bridges the Bresse chicken's extraordinary depth without overwhelming it; tarragon mirrors the wine's herbal complexity")
    PAIR(prod_roi, "Terrine de campagne with lard, cornichons, and Mâcon bread", "complement", "classic", "starter", "The Lyonnais bistro's most traditional first course and its natural Beaujolais partner — Fleurie's raspberry freshness cuts through the terrine's porky richness; cornichons' acidity bridges the wine's freshness")

# ── FRIULI VENEZIA GIULIA DOC (ITALY) ────────────────────────────
print("\n=== Friuli Venezia Giulia DOC (Italy) ===")
r_fri = R("Friuli Venezia Giulia", "Italy", "wine",
           designation_type="DOC",
           designation_name="Friuli Venezia Giulia DOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Italy's most complex and internationally celebrated white wine region — the northeastern Italian border zone between the Alps, the Adriatic, and Slovenia, producing an extraordinary diversity of indigenous and international white varieties from the Collio, Colli Orientali, and Isonzo sub-zones. Friulano (formerly Tocai), Ribolla Gialla, Malvasia Istriana, Verduzzo, and Picolit are the key indigenous whites; Pinot Grigio, Sauvignon Blanc, Chardonnay, and Pinot Bianco are also produced at high quality. The region is also the global birthplace of the orange wine movement — Stanko Radikon and Josko Gravner's skin-contact Ribolla Gialla wines in the 1990s sparked a worldwide phenomenon.",
           key_producers="Jermann, Livio Felluga, Gravner, Radikon, Vie di Romans, Attems, Primosic",
           historical_context="Friuli's wine history is defined by its cultural complexity — the region was successively ruled by Rome, Venice, Austria, Napoleon, and Italy, with a Slovenian minority community maintaining cultural and culinary traditions. The Collio DOC's proximity to the Slovenian border — where Brda produces wines of similar quality — creates the world's most intriguing cross-border wine culture. Josko Gravner's decision in 1997 to return to Georgian clay qvevri for Ribolla Gialla fermentation, and Stanko Radikon's parallel experiments with skin-contact wines, sparked the global orange wine movement — now one of the world's most significant natural wine trends. Silvio Jermann's Vintage Tunina remains Italy's most celebrated multi-varietal white wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Friuli vintage; Collio and Colli Orientali whites showed extraordinary aromatic complexity and the mineral freshness of the ponca limestone marl soils."),
    (2021, "very_good", "stable", "Classic vintage; Alpine influence produced whites of excellent natural acidity and the characteristic fresh herb-mineral character of great Friulano and Ribolla."),
    (2020, "excellent", "stable", "Benchmark year; Gravner and Radikon orange wines received extraordinary international attention; Jermann Vintage Tunina of unusual concentration."),
    (2019, "excellent", "rising", "Outstanding vintage; Friulano from ponca marl showed extraordinary complexity; orange wine movement's international explosion drove Collio prices higher."),
    (2018, "very_good", "stable", "Warm vintage producing generous Friuli of good body; skin-contact wines particularly successful; ponca marl maintained freshness in the heat."),
]:
    VIN(r_fri, yr, qd, pt, sn)

p_jer = P("Jermann", "Italy", r_fri,
           description="Silvio Jermann's Friuli Collio estate — the producer that gave Italian white wine its first international cult status with Vintage Tunina (a multi-varietal blend from Chardonnay, Sauvignon, Ribolla, Malvasia, and Picolit). Jermann's Was Dreams... (Chardonnay) and Capo Martino (Friulano with Ribolla, Malvasia, and Picolit) are also internationally celebrated. The estate has done more than any other producer to demonstrate Friuli's capacity for white wines of international fine wine status.")
prod_jer, new = PROD("Jermann Vintage Tunina Bianco", "wine_still", p_jer, r_fri, "Italy",
                     subcategory="Friulano blend",
                     description="Italy's most famous multi-varietal white blend — Chardonnay, Sauvignon Blanc, Ribolla Gialla, Malvasia Istriana, and Picolit from the Collio's ponca marl soils. Extraordinary complexity: white peach, apricot, citrus blossom, mineral depth, honeyed richness, and a persistence that develops magnificently over 8+ years. The wine that proved Italian whites could achieve Burgundian complexity and longevity. Italy's most iconic white wine.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_jer, "Risotto all'onda with white truffle, Frico croccante, and aged Montasio", "complement", "classic", "main", "Friuli's most celebrated dish and its most celebrated wine — Vintage Tunina's extraordinary complexity matches white truffle's depth; Frico's fried cheese bridges the wine's mineral richness; Montasio's aged character mirrors the wine's development")
    PAIR(prod_jer, "San Daniele prosciutto (18-month aged) with grissini, fig, and melon", "complement", "classic", "aperitif", "The Friuli province's most famous product and its benchmark white wine — Vintage Tunina's peach and mineral character bridges the prosciutto's sweet-salt depth; fig's sweetness mirrors the wine's apricot note; melon amplifies the floral character")

p_gra = P("Gravner", "Italy", r_fri,
           description="Josko Gravner's Oslavia estate — the producer who sparked the global orange wine movement by returning to Georgian qvevri (clay amphorae) for skin-contact Ribolla Gialla fermentation in 1997. Gravner's Ribolla Gialla wines — amber-coloured from 6+ months of skin contact, aged in qvevri then in large Slavonian oak — are the most discussed and polarizing white wines in Italy: profound, tannic, complex, and requiring years of development. A pilgrimage destination for natural wine enthusiasts worldwide.")
prod_gra, new = PROD("Gravner Ribolla Gialla Anfora", "wine_still", p_gra, r_fri, "Italy",
                     subcategory="Ribolla Gialla",
                     description="The wine that birthed the global orange wine movement — Ribolla Gialla fermented on skins for 6 months in Georgian clay qvevri, then aged 6 years in large Slavonian oak and 2 years in bottle before release. Deep amber, chamomile, dried apricot, quince, beeswax, dried herb, walnut skin, and tannins that demand patience. A wine of philosophical intention — Gravner's rejection of modern winemaking in pursuit of ancient truth. Profoundly individual.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_gra, "Frico morbido (soft fried potato and Montasio cheese) with wild mushrooms and herbs", "complement", "classic", "main", "Friuli's most traditional dish and its most radical wine — Gravner's amber wine's tannin and oxidative complexity bridges the Frico's rich potato-cheese; wild mushrooms mirror the wine's earthy depth; herbs bridge the chamomile character")
    PAIR(prod_gra, "Aged Parmigiano-Reggiano 36 months with acacia honey and toasted hazelnuts", "complement", "classic", "cheese", "The orange wine and aged cheese pairing — Gravner's tannic depth and oxidative complexity bridges Parmigiano's crystalline amino acids; honey mirrors the wine's beeswax; hazelnuts bridge the walnut-skin tannin")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
