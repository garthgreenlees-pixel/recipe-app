#!/usr/bin/env python3
"""T23 Batch 24 — New wine regions: Côte Chalonnaise (France), Madiran AOC (France), Saumur-Champigny AOC (France), Etna DOC (Italy), Vermentino di Sardegna DOC (Italy)"""

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

# ── CÔTE CHALONNAISE (FRANCE) ─────────────────────────────────────
print("\n=== Côte Chalonnaise (France) ===")
r_cha = R("Côte Chalonnaise", "France", "wine",
           designation_type="AOC",
           designation_name="Côte Chalonnaise",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Burgundy's most underrated sub-region — the transitional zone between the Côte de Beaune and the Mâconnais, comprising the five village appellations of Rully, Mercurey, Givry, Montagny, and Bouzeron. The Chalonnaise produces Pinot Noir and Chardonnay of genuine Burgundian character at prices far below the Côte d'Or, and Bouzeron is the world's sole dedicated Aligoté appellation. The clay and limestone soils of Mercurey produce the finest reds — structured, age-worthy Pinot Noir that rivals village-level Côte de Nuits at a fraction of the cost. Rully's Chardonnay and Crémant de Bourgogne base wines are also of exceptional quality.",
           key_producers="Domaine de Villaine, Michel Juillot, Faiveley, Domaine Joblot, Domaine Belleville",
           historical_context="The Côte Chalonnaise takes its name from the city of Chalon-sur-Saône, the major river port that shipped Burgundian wine north through the Middle Ages. The region was long dismissed as 'generic Burgundy' because its wines lacked the prestige of Gevrey-Chambertin or Meursault. Aubert de Villaine — co-director of Domaine de la Romanée-Conti — chose Bouzeron as the location for his personal estate Domaine de Villaine, producing wines that demonstrated the Chalonnaise's potential for serious quality. The critical rehabilitation of Mercurey in particular has been driven by Michel Juillot's single-vineyard bottlings.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Chalonnaise vintage; Mercurey Pinot Noir and Rully Chardonnay both showed excellent concentration and the regional mineral freshness."),
    (2021, "very_good", "stable", "Classic vintage; cool conditions produced wines of excellent acidity and the characteristic Chalonnaise translucency in both red and white."),
    (2020, "excellent", "stable", "Benchmark year; Domaine de Villaine Bouzeron and Juillot Mercurey received extraordinary critical attention; value-conscious Burgundy lovers took notice."),
    (2019, "excellent", "rising", "Outstanding vintage; Mercurey reds of exceptional structure and longevity potential; Chalonnaise's reputation for value continued to rise."),
    (2018, "very_good", "stable", "Warm, generous vintage; Mercurey produced Pinot Noir of unusual concentration; Rully Chardonnay of good body and mineral depth."),
]:
    VIN(r_cha, yr, qd, pt, sn)

p_vil = P("Domaine de Villaine", "France", r_cha,
           description="Aubert de Villaine's personal estate in Bouzeron — the co-director of Domaine de la Romanée-Conti chose this overlooked Chalonnaise village as the location for his own wines. The Bouzeron Aligoté, the Rully Les Saint-Jacques, and the Mercurey Les Montots demonstrate what the Chalonnaise can achieve in the hands of Burgundy's most legendary winemaker. The Aligoté is the world's definitive expression of the variety.")
prod_vil, new = PROD("Domaine de Villaine Bouzeron Aligoté", "wine_still", p_vil, r_cha, "France",
                     subcategory="Aligoté",
                     description="The world's definitive Aligoté — from the only appellation dedicated exclusively to Burgundy's second white grape, made by the co-director of Domaine de la Romanée-Conti. Lemon, green apple, chalky mineral, a hint of honey from the oldest vines, and the clean, vivacious acidity that makes Aligoté the traditional base for Kir. Demonstrates that Aligoté in the right hands is a serious wine.",
                     price_tier="mid_range")
if new:
    PAIR(prod_vil, "Gougères au fromage (Gruyère puff pastry) and Comté 18 months", "complement", "classic", "aperitif", "Burgundy's traditional aperitif combination — Aligoté's crisp acidity and mineral freshness cuts through the gougère's cheese richness; Comté's nutty depth bridges the wine's mineral character")
    PAIR(prod_vil, "Escargots de Bourgogne in parsley-garlic butter with crusty baguette", "complement", "classic", "starter", "Burgundy's most traditional first course and its most underrated wine — Aligoté's bright acidity cuts through the parsley-garlic butter; the wine's lemon character mirrors the citric freshness of the herb butter")

p_jui = P("Michel Juillot", "France", r_cha,
           description="The Juillot family's Mercurey estate — the most committed and critically celebrated producer of serious Mercurey Pinot Noir. Laurent Juillot's single-vineyard wines from Les Champs Martins and La Cailloute demonstrate that Mercurey can produce structured, age-worthy Pinot Noir that rivals the Côte de Nuits at village level. The estate has done more than any other to elevate Mercurey's critical reputation.")
prod_jui, new = PROD("Michel Juillot Mercurey Premier Cru Les Champs Martins", "wine_still", p_jui, r_cha, "France",
                     subcategory="Pinot Noir",
                     description="Mercurey's benchmark Premier Cru Pinot Noir — from the clay-limestone Les Champs Martins parcel, aged with Burgundian precision. Dark cherry, raspberry, autumn leaves, iron mineral, and the structured elegance of a wine built for 10+ years of development. Demonstrates that Mercurey Premier Cru rivals Côte de Nuits village Burgundy at less than half the price.",
                     price_tier="mid_range")
if new:
    PAIR(prod_jui, "Poulet de Bresse en cocotte with morels, cream, and Mercurey vin jaune reduction", "complement", "classic", "main", "Burgundy's most celebrated poultry and Mercurey's finest red — the wine's iron mineral and dark cherry character bridges the Bresse chicken's extraordinary depth; morels echo the forest floor notes")
    PAIR(prod_jui, "Jambon persillé de Bourgogne (jellied ham with parsley and white wine) with cornichons", "complement", "classic", "starter", "Burgundy's most traditional charcuterie and its overlooked red — Mercurey's Pinot Noir acidity cuts through the jellied ham's richness; cornichons' acidity bridges the wine's freshness")

# ── MADIRAN AOC (FRANCE) ──────────────────────────────────────────
print("\n=== Madiran AOC (France) ===")
r_mad = R("Madiran", "France", "wine",
           designation_type="AOC",
           designation_name="Madiran AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Southwest France's most powerful and individual red wine AOC — the Pyrenean foothills of the Hautes-Pyrénées and Gers producing Tannat (minimum 60%, often 100%), the variety that produces the most tannic wines of any appellation in France. Madiran wines require years of cellaring to soften their extraordinary tannin structure, but at their best achieve a dark, profound, and unique character unlike any other French red. The appellation also produces Pacherenc du Vic-Bilh white wines from Petit Courbu, Arrufiac, and the Manseng varieties.",
           key_producers="Alain Brumont (Château Montus and Bouscassé), Château d'Aydie, Domaine Berthoumieu, Château Barréjat",
           historical_context="Tannat was the wine of the Pyrenean pilgrims on the Camino de Santiago — the Voie du Puy route passing directly through Madiran. The variety's extraordinary tannin content provided preservation and the iron-mineral character suited to long mountain journeys. Alain Brumont revolutionized the appellation in the 1980s by reducing yields dramatically, extending maceration, and introducing new oak — transforming rustic Madiran into an internationally celebrated wine of genuine complexity. Scientific research later confirmed Tannat has the highest resveratrol content of any wine grape, sparking health-focused interest. Uruguay adopted Tannat as its signature national variety.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Madiran vintage; Tannat from Pyrenean clay-limestone showed extraordinary concentration and the appellation's characteristic iron-mineral power."),
    (2021, "very_good", "stable", "Classic vintage; cool Pyrenean conditions produced Tannat wines of excellent structure and dark fruit concentration with more freshness than usual."),
    (2020, "excellent", "stable", "Benchmark year; Brumont's Château Montus produced a wine of historic concentration; the 2020 Madiran is destined for 20+ year aging."),
    (2019, "excellent", "rising", "Outstanding vintage; Tannat of extraordinary longevity potential; Madiran's rediscovery by Bordeaux-fatigued collectors accelerated."),
    (2018, "very_good", "stable", "Warm vintage; generous Tannat of good concentration; the clay-limestone parcels retained freshness and prevented overripeness."),
]:
    VIN(r_mad, yr, qd, pt, sn)

p_bru = P("Château Montus", "France", r_mad,
           description="Alain Brumont's flagship Madiran estate — the winemaker who single-handedly transformed Madiran from rustic peasant wine to internationally celebrated appellation. Château Montus's 100% Tannat from the highest-elevation clay-limestone plots is considered France's greatest Tannat and one of southwest France's most age-worthy wines. The Prestige cuvée requires 10+ years before the legendary tannins soften to reveal extraordinary complexity.")
prod_bru, new = PROD("Château Montus Madiran Prestige", "wine_still", p_bru, r_mad, "France",
                     subcategory="Tannat",
                     description="Southwest France's most powerful and long-lived red — 100% Tannat from high-elevation Pyrenean clay-limestone, aged 18 months in new French oak. Extraordinary tannin structure, blackberry, dark plum, iron mineral, cedar, dark chocolate, and a Pyrenean austerity that demands a decade of patience. At 15+ years, transforms into something profound and deeply individual. The definitive Madiran.",
                     price_tier="premium")
if new:
    PAIR(prod_bru, "Confit de canard with flageolet beans, garlic confit, and Périgord truffles", "complement", "classic", "main", "The Pyrenean-Gascon tradition — duck confit's rich fat is one of the few dishes that matches Madiran's extraordinary tannin; garlic bridges the iron mineral; truffle amplifies the wine's complexity")
    PAIR(prod_bru, "Cassoulet de Castelnaudary with Toulouse sausage, duck confit, and white haricot beans", "complement", "classic", "main", "The southwest's greatest one-pot dish and its most powerful wine — Madiran's iron tannins cut through the cassoulet's accumulated fats; Toulouse sausage's spice bridges the dark fruit; haricot beans soften the encounter")

p_ayd = P("Château d'Aydie", "France", r_mad,
           description="The Laplace family's multi-generational Madiran estate producing both the serious Château d'Aydie Madiran and the more approachable Odé d'Aydie — consistently among the appellation's most reliable and quality-focused producers. The Château d'Aydie Madiran demonstrates Tannat's capacity for elegance without sacrificing its essential iron character.")
prod_ayd, new = PROD("Château d'Aydie Madiran", "wine_still", p_ayd, r_mad, "France",
                     subcategory="Tannat",
                     description="The appellation's benchmark for elegance within power — Tannat with a small proportion of Fer Servadou and Cabernet Franc from Pyrenean clay soils. Dark cherry, blackberry, violets, iron mineral, and a tannin structure more accessible than Montus but still demanding of 5-8 years' patience. Demonstrates Tannat's capacity for finesse alongside its natural power.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ayd, "Magret de canard grillé (grilled duck breast) with cèpes and Armagnac reduction", "complement", "classic", "main", "Duck breast and Madiran is the Gascony equation — the wine's iron tannin and dark fruit character bridges the duck's rich fat; cèpes' earthiness mirrors the wine's mineral depth; Armagnac reduction bridges the dark fruit")
    PAIR(prod_ayd, "Côte de boeuf grillée (rib of beef) with bone marrow butter and watercress salad", "complement", "established", "main", "Madiran's iron tannins and a prime cut of Gascon beef — the wine's power matches the beef's fat; bone marrow butter bridges the iron mineral; watercress' bitterness contrasts the dark fruit")

# ── SAUMUR-CHAMPIGNY AOC (FRANCE) ─────────────────────────────────
print("\n=== Saumur-Champigny AOC (France) ===")
r_sac = R("Saumur-Champigny", "France", "wine",
           designation_type="AOC",
           designation_name="Saumur-Champigny AOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The Loire Valley's most celebrated and age-worthy Cabernet Franc appellation — tuffeau limestone hillsides above the village of Saumur producing Cabernet Franc (minimum 100%) of extraordinary aromatic precision, mineral depth, and unexpected longevity. Saumur-Champigny's finest wines — especially from the Puy-Notre-Dame sub-zone and estates like Clos Rougeard — develop over 20+ years in bottle into wines that rival Chinon and Bourgeuil for Loire Cabernet Franc supremacy. The tuffeau limestone's chalk and quartz imparts a mineral freshness that makes Saumur-Champigny arguably the most elegant Cabernet Franc in France.",
           key_producers="Clos Rougeard, Domaine des Roches Neuves, Domaine Filliatreau, Château du Hureau, Domaine de la Paleine",
           historical_context="The Foucault brothers of Clos Rougeard — Charly and Nady, the most reclusive winemakers in France — produced Saumur-Champigny from tiny yields and perfect tuffeau limestone parcels from 1966 until their deaths, creating wines that became cult objects among Burgundy lovers seeking affordable age-worthy alternatives. Their wines never appeared in wine shops — sold exclusively to restaurant customers and mailing list collectors. Thierry Germain arrived from Bordeaux in 1991 and established Domaine des Roches Neuves, introducing biodynamics and single-vineyard precision that elevated the appellation's critical profile internationally.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Saumur-Champigny vintage; Cabernet Franc from tuffeau limestone showed extraordinary aromatic precision and mineral depth."),
    (2021, "very_good", "stable", "Classic vintage; cool Loire conditions produced wines of excellent fresh red fruit character and the tuffeau limestone mineral signature."),
    (2020, "excellent", "stable", "Benchmark year; Domaine des Roches Neuves and Filliatreau both produced exceptional single-vineyard wines of 15+ year aging potential."),
    (2019, "exceptional", "rising", "Greatest Saumur-Champigny vintage of the era; Cabernet Franc of extraordinary depth and the characteristic Loire pencil shavings and violet complexity."),
    (2018, "excellent", "stable", "Warm vintage producing generous Cabernet Franc of unusual concentration; tuffeau limestone maintained freshness in an otherwise hot Loire year."),
]:
    VIN(r_sac, yr, qd, pt, sn)

p_roc = P("Domaine des Roches Neuves", "France", r_sac,
           description="Thierry Germain's biodynamic Saumur-Champigny estate — the Bordelais who came to the Loire and discovered what Cabernet Franc could achieve on tuffeau limestone. His L'Insolite Saumur Blanc and Marginale single-vineyard red are considered the appellation's finest wines alongside Clos Rougeard. Germain's biodynamic commitment and precision viticulture have been instrumental in the appellation's critical rehabilitation.")
prod_roc, new = PROD("Domaine des Roches Neuves Terre Chaude Saumur-Champigny", "wine_still", p_roc, r_sac, "France",
                     subcategory="Cabernet Franc",
                     description="The benchmark for modern Saumur-Champigny — 100% Cabernet Franc from ancient tuffeau limestone and volcanic basalt, biodynamically farmed. Wild strawberry, raspberry, violet, pencil shavings, crushed chalk mineral, and a luminous freshness that makes this one of the Loire's most compelling reds. Approachable young but develops magnificently over 10+ years. The definitive entry into serious Saumur-Champigny.",
                     price_tier="mid_range")
if new:
    PAIR(prod_roc, "Lotte rôtie (monkfish) with lardons, tomato confit, and tapenade croûtons", "complement", "established", "main", "The Loire's surprising red-with-fish pairing — Cabernet Franc's light body and high acidity handles monkfish's firm flesh; lardons add a savoury bridge; tapenade's olive bitterness contrasts the violet freshness")
    PAIR(prod_roc, "Rillettes de Tours (slow-cooked pork rillettes) with cornichons and pain de campagne", "complement", "classic", "starter", "The Touraine's most traditional charcuterie and its Cabernet Franc — the wine's bright acidity cuts through the rillettes' fat; cornichons' acidity bridges the wine's freshness; pencil shavings mirror the pork's smokiness")

p_hure = P("Château du Hureau", "France", r_sac,
           description="The Vatan family's tuffeau-carved Saumur-Champigny estate — producing wines from parcels some of the appellation's oldest Cabernet Franc vines on pure tuffeau limestone. The Château du Hureau Saumur-Champigny and the single-vineyard Lisagathe and Fours à Chaux cuvées are considered among the appellation's finest expressions of the tuffeau limestone terroir.")
prod_hure, new = PROD("Château du Hureau Saumur-Champigny Cuvée Lisagathe", "wine_still", p_hure, r_sac, "France",
                      subcategory="Cabernet Franc",
                      description="The Vatan family's single-vineyard Saumur-Champigny from the oldest tuffeau limestone parcels — Cabernet Franc of extraordinary mineral precision and aromatic complexity. Crushed raspberry, violet, Saumur tuffeau chalk, cedarwood, and a delicate structure that develops over 15 years into a wine rivaling the finest Chinon. One of the Loire Valley's most underrated treasures.",
                      price_tier="mid_range")
if new:
    PAIR(prod_hure, "Rôti de porc au lait (milk-braised pork loin) with morel mushrooms and cream", "complement", "classic", "main", "The Touraine's traditional celebration roast and its Cabernet Franc — the wine's red fruit and chalk mineral bridges the milk-braised pork's subtle sweetness; morels' earthiness mirrors the wine's depth")
    PAIR(prod_hure, "Goat cheese crottin de Chavignol (Loire valley chèvre) with honey and walnuts", "complement", "classic", "cheese", "The Loire valley's famous goat cheese and its Cabernet Franc — the wine's chalk mineral mirrors the chèvre's lactic freshness; honey's sweetness bridges the wine's red fruit; walnuts bridge the tannin structure")

# ── ETNA DOC (ITALY) ──────────────────────────────────────────────
print("\n=== Etna DOC (Italy) ===")
r_etn = R("Etna", "Italy", "wine",
           designation_type="DOC",
           designation_name="Etna DOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Sicily's most exciting and internationally celebrated wine DOC — the volcanic basalt slopes of Mount Etna at 500-1000m elevation, producing Nerello Mascalese (red) and Carricante (white) of extraordinary complexity and transparency from pre-phylloxera old vines on black volcanic soils. Etna wines have been compared to Burgundy for their translucency, mineral depth, and the way they express the specific altitude and aspect of the volcano's diverse contrade (named plots). The Etna revolution — triggered by Andrea Franchetti's Passopisciaro in 2000 — has transformed Mount Etna into one of the world's most sought-after and discussed wine regions.",
           key_producers="Benanti, Passopisciaro, Terre Nere, Cornelissen, Biondi, Cos, Occhipinti (nearby), Tornatore",
           historical_context="Etna's wine history stretches back 3,000 years — Greek colonists planted vines on the volcano's fertile volcanic soils in the 8th century BC, and Etna wine was traded throughout the Mediterranean. Phylloxera never reached most of Etna's high-altitude vineyards (the lava soil acts as a barrier), so pre-phylloxera centenarian vines — some over 150 years old — still produce grapes on their own rootstocks. Giuseppe Benanti began the Etna revival in the 1990s, and Andrea Franchetti's arrival in 2000 with Passopisciaro triggered the international explosion of interest. The concept of Etna's contrade — named plots comparable to Burgundian lieux-dits — now drives the region's fine wine narrative.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Etna vintage; Nerello Mascalese from volcanic basalt showed extraordinary transparency and the characteristic smoky mineral depth of the best contrade."),
    (2021, "very_good", "stable", "Classic vintage; cooler Etna conditions produced wines of excellent freshness and the delicate, transparent Pinot-like character that defines Nerello at altitude."),
    (2020, "excellent", "stable", "Benchmark year; Terre Nere and Passopisciaro contrade wines received extraordinary international attention; Etna's status as Italy's most exciting wine region confirmed."),
    (2019, "exceptional", "rising", "Greatest Etna vintage of the modern era; Nerello Mascalese of historic transparency and volcanic mineral depth; contrade wines achieved record prices."),
    (2018, "excellent", "stable", "Excellent vintage; volcanic basalt expressed itself with unusual clarity; old-vine Nerello of extraordinary aromatic complexity and subtle smoky minerality."),
]:
    VIN(r_etn, yr, qd, pt, sn)

p_ben = P("Benanti", "Italy", r_etn,
           description="Giuseppe Benanti's family estate — the pioneer of the Etna wine revival who began bottling single-vineyard Nerello Mascalese from pre-phylloxera old vines in the 1990s, decades before the international wine world discovered the volcano. Benanti's Serra della Contessa and Rovittello contrade wines are considered among Etna's most historically significant and consistently excellent expressions of Nerello Mascalese.")
prod_ben, new = PROD("Benanti Serra della Contessa Etna Rosso", "wine_still", p_ben, r_etn, "Italy",
                     subcategory="Nerello Mascalese",
                     description="The wine that began the Etna revolution — Giuseppe Benanti's pre-phylloxera old-vine Nerello Mascalese from the Serra della Contessa contrada on the volcano's northeast flank. Translucent ruby, dried cherry, wild strawberry, lava rock mineral, volcanic smoke, and a delicacy of structure that has led to inevitable Pinot Noir comparisons. Age-worthy and hauntingly individual.",
                     price_tier="premium")
if new:
    PAIR(prod_ben, "Grilled swordfish alla ghiotta (with olives, capers, tomato, and pine nuts)", "complement", "established", "main", "Sicily's most prized fish and Etna's founding wine — the wine's delicacy and volcanic mineral matches the swordfish's firm flesh; olives and capers bridge the lava mineral; tomato's acidity mirrors the wine's freshness")
    PAIR(prod_ben, "Arancini di riso with ragù di maiale, peas, and aged caciocavallo", "complement", "classic", "starter", "Sicily's most beloved street food and Etna's pioneering red — the wine's dried cherry and mineral character bridges the rice ball's savoury filling; caciocavallo's aged depth mirrors the wine's complexity")

p_pas = P("Passopisciaro", "Italy", r_etn,
           description="Andrea Franchetti's Etna estate — the Tuscan visionary who recognized Nerello Mascalese's extraordinary potential and established Passopisciaro in 2000 on the volcano's north face contrade. Franchetti's contrade bottlings — Chiappemacine, Guardiola, Porcaria, Rampante, and Sciaranuova — introduced the concept of Etna cru wines comparable to Burgundian premier crus. Passopisciaro's influence on the Etna wine narrative cannot be overstated.")
prod_pas, new = PROD("Passopisciaro Contrada G Etna Rosso", "wine_still", p_pas, r_etn, "Italy",
                     subcategory="Nerello Mascalese",
                     description="Andrea Franchetti's Guardiola contrada wine — Nerello Mascalese from 80-year-old vines on the volcano's north face at 700m elevation on black volcanic basalt. One of Etna's most internationally celebrated contrade wines: vibrant red cherry, wild herb, volcanic smoke, iron mineral, and the extraordinary transparency that has made Passopisciaro the reference for Etna's Burgundian ambitions.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_pas, "Agnello al forno (roasted lamb) with wild Sicilian herbs, capers, and lemon", "complement", "classic", "main", "Etna's volcanic terroir and Sicilian mountain lamb — the wine's translucent cherry and mineral character bridges the herb-roasted lamb; capers' acidity mirrors the wine's freshness; lemon bridges the citric note in the Nerello")
    PAIR(prod_pas, "Ricotta di pecora fresca with Sicilian chestnut honey, toasted almonds, and wild thyme", "complement", "established", "dessert", "The Etna pastoral tradition — Nerello's delicate cherry and herbal character bridges the sheep's milk ricotta's lactic freshness; honey's sweetness mirrors the wine's fruit; thyme bridges the wild herb notes of high-altitude Etna")

# ── VERMENTINO DI SARDEGNA DOC (ITALY) ───────────────────────────
print("\n=== Vermentino di Sardegna DOC (Italy) ===")
r_ver = R("Vermentino di Sardegna", "Italy", "wine",
           designation_type="DOC",
           designation_name="Vermentino di Sardegna DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Sardinia's most important white wine DOC and the definitive expression of Vermentino — the aromatic white variety planted across the island's granite and limestone hills, producing wines of extraordinary aromatic intensity, bitter almond finish, and the briny Mediterranean minerality that reflects Sardinia's coastal culture. Vermentino di Gallura DOCG (the island's highest designation) from the granite soils of northeastern Sardinia produces the most concentrated and age-worthy expressions. Sardinia's wines have been shaped by centuries of Catalan, Pisan, and Arab influence — a unique Mediterranean crossroads of viticulture.",
           key_producers="Sella & Mosca, Argiolas, Pala, Santadi, Capichera, Cantina di Gallura",
           historical_context="Sardinia's Vermentino is likely descended from vines brought by the Genoese in the 13th century (the variety is also found in Liguria as Pigato and in Corsica as Malvoisie de Corse). The Sella & Mosca estate — established by two Piedmontese lawyers in 1899 — was the first to bottle and market Vermentino di Sardegna nationally, establishing the wine's commercial identity. The granite soils of the Gallura region in the northeast — Europe's oldest geological formation at over 500 million years — give Vermentino di Gallura DOCG a mineral depth unmatched elsewhere. Argiolas's Costamolino remains the island's most internationally distributed Vermentino and the gateway to Sardinian white wine for much of the world.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding Vermentino vintage; Sardinian granite soils produced Vermentino of exceptional aromatic intensity and the characteristic bitter almond-Mediterranean mineral finish."),
    (2022, "very_good", "stable", "Classic vintage; Mediterranean heat was tempered by island winds; Vermentino wines of excellent aromatic freshness and bitter almond character."),
    (2021, "excellent", "stable", "Benchmark year; Argiolas and Capichera both produced Vermentino of international acclaim; Gallura DOCG wines of extraordinary granite mineral depth."),
    (2020, "excellent", "rising", "Outstanding vintage; Vermentino di Gallura achieved record critical scores; Sardinian white wine's international discovery accelerated."),
    (2019, "very_good", "stable", "Solid vintage; island winds maintained freshness in warm Mediterranean conditions; Vermentino of good aromatic intensity and the characteristic citrus-bitter almond finish."),
]:
    VIN(r_ver, yr, qd, pt, sn)

p_arg = P("Argiolas", "Italy", r_ver,
           description="The Argiolas family's landmark Sardinian estate — the island's most internationally successful winery, producing Costamolino (the world's best-selling Vermentino di Sardegna), Is Argiolas, and the exceptional Angialis dessert wine from Nasco. Argiolas has done more than any other producer to introduce the world to Sardinian wine, and Costamolino remains the benchmark entry-level Vermentino for international markets.")
prod_arg, new = PROD("Argiolas Costamolino Vermentino di Sardegna", "wine_still", p_arg, r_ver, "Italy",
                     subcategory="Vermentino",
                     description="The world's most recognized Vermentino di Sardegna — Argiolas's benchmark white from the Campidano plain's varied soils. White peach, citrus blossom, lime, fennel, and the characteristic bitter almond finish that defines great Sardinian Vermentino. Dry, aromatic, and with the saline Mediterranean mineral character that makes this wine the island's most perfect seafood companion. 1.5 million bottles sold annually worldwide.",
                     price_tier="mid_range")
if new:
    PAIR(prod_arg, "Aragosta arrosto (roasted Sardinian lobster) with olive oil, lemon, and capers", "complement", "classic", "main", "Sardinia's most prized crustacean and its benchmark white — the wine's citrus and bitter almond character bridges the lobster's sweet richness; capers add a saline bridge to the Mediterranean mineral")
    PAIR(prod_arg, "Culurgiones (Sardinian stuffed pasta) with potato, mint, and pecorino sardo", "complement", "classic", "main", "Sardinia's most distinctive pasta and its signature white wine — Vermentino's aromatic freshness and bitter almond bridges the potato-mint filling's delicate flavours; pecorino's saltiness bridges the wine's saline mineral")

p_cap = P("Capichera", "Italy", r_ver,
           description="The Ragnedda family's Gallura estate — producing the island's most critically acclaimed and internationally sought-after Vermentino di Gallura DOCG from ancient granite soils. Capichera's various Vermentino cuvées (Capichera, Vigna Ngena, Santigaini) demonstrate the granite soils of the Gallura DOCG's capacity to produce white wines of extraordinary mineral complexity and aging potential.")
prod_cap, new = PROD("Capichera Vermentino di Gallura DOCG Tardiva", "wine_still", p_cap, r_ver, "Italy",
                     subcategory="Vermentino",
                     description="Sardinia's most complex and age-worthy Vermentino — late-harvested Vermentino di Gallura from ancient Gallura granite, fermented and aged in oak. Extraordinary depth: white peach jam, apricot, exotic spice, almond blossom, granite mineral, and a richness that transforms over 5-8 years in bottle. The wine that demonstrates Vermentino's ability to age and develop genuine complexity. One of Italy's most distinctive and underrated whites.",
                     price_tier="premium")
if new:
    PAIR(prod_cap, "Porceddu (Sardinian roast suckling pig) with myrtle, fennel, and sea salt", "complement", "classic", "main", "The most iconic Sardinian feast dish with the island's most complex white — the wine's apricot richness and almond depth bridges the succulent pig; myrtle's aromatic bitterness mirrors the wine's bitter almond finish; fennel bridges the Vermentino's herbal character")
    PAIR(prod_cap, "Pecorino sardo stagionato with Sardinian chestnut honey, quince, and toasted walnuts", "complement", "classic", "cheese", "The island's aged sheep cheese and its most complex white — Vermentino Tardiva's richness and almond depth bridges pecorino's sharp mineral tang; chestnut honey mirrors the wine's fruit; walnuts bridge the oak")

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
