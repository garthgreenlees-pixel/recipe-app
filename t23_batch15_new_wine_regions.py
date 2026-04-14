#!/usr/bin/env python3
"""T23 Batch 15 — New wine regions: Wachau DAC (Austria), Côte Rôtie AOC (France), Bandol AOC (France), Nova Scotia (Canada), Savoie AOC (France)"""

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

# ── WACHAU DAC (AUSTRIA) ──────────────────────────────────────────
print("\n=== Wachau DAC (Austria) ===")
r_wac = R("Wachau", "Austria", "wine",
           designation_type="DAC",
           designation_name="Wachau DAC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Austria's most celebrated and scenic wine region tracing the Danube through a UNESCO World Heritage gorge between Melk and Krems. Riesling and Grüner Veltliner from dramatic granite and gneiss terraces produce wines of extraordinary mineral precision, aromatic intensity, and aging potential. Three quality levels — Steinfeder (light), Federspiel (medium), and Smaragd (full-bodied) — are unique to the Wachau and named after local wildlife.",
           key_producers="F.X. Pichler, Emmerich Knoll, Rudi Pichler, Domäne Wachau, Alzinger",
           historical_context="The Wachau's vineyard terraces were first cultivated by Celtic tribes and later by Roman legionnaires who established the first winemaking settlements along the Danube. The region's distinctive classification system was established by the Vinea Wachau association in 1983 — predating Austria's DAC system by 20 years. F.X. Pichler's wines are considered benchmarks for Austrian Riesling of international stature.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Wachau vintage; Riesling from Loibenberg and Kellerberg showed extraordinary granite mineral precision."),
    (2021, "very_good", "stable", "Elegant vintage; cooler season produced Smaragd Grüner Veltliner of remarkable finesse and aging potential."),
    (2020, "exceptional", "rising", "Greatest Wachau vintage of the modern era; F.X. Pichler and Knoll produced wines of legendary quality."),
    (2019, "excellent", "stable", "Benchmark year; Riesling Smaragd from granite terraces reached the finest critical scores in a generation."),
    (2018, "excellent", "stable", "Excellent vintage; warm year produced Smaragd Riesling of unusual concentration with the characteristic Wachau freshness."),
]:
    VIN(r_wac, yr, qd, pt, sn)

p_fxp = P("F.X. Pichler", "Austria", r_wac,
           description="Franz Xaver Pichler's Loiben estate is Austria's most celebrated and rarified Riesling and Grüner Veltliner producer. The iconic 'M' cuvée from the Dürnsteiner Kellerberg is considered Austria's greatest wine and one of the world's finest white wines — allocated to a small circle of international collectors and restaurants.")
prod_fxp, new = PROD("FX Pichler Loibner Steinertal Smaragd Riesling", "wine_still", p_fxp, r_wac, "Austria",
                     subcategory="Riesling",
                     description="F.X. Pichler's Smaragd Riesling from the ancient granite Steinertal vineyard on the Danube's north bank — bone dry, intensely mineral, and hauntingly complex. Yellow peach, white flower, granite dust, white pepper, and the long mineral finish that only great Riesling achieves. Age for 20+ years.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_fxp, "Wachauer Marillenknödel (apricot dumplings) with brown butter and breadcrumbs", "complement", "classic", "dessert", "The Wachau's most famous food and its finest wine — apricot notes in the Riesling find direct resonance in the Wachau's legendary apricots; a circular, regional pairing of great beauty")
    PAIR(prod_fxp, "Poached Austrian pike-perch with chive cream, lemon, and dill", "complement", "classic", "main", "Danube fish and Danube wine — the Riesling's mineral precision and citrus character is the ideal partner for the delicate freshwater fish; chive and dill bridge the herbal notes")

p_kno = P("Emmerich Knoll", "Austria", r_wac,
           description="The Knoll family's Unterloiben estate is considered co-equal with F.X. Pichler as the Wachau's greatest producer. Emmerich Knoll's Riesling and Grüner Veltliner from the Loibenberg and Schütt vineyards are wines of extraordinary elegance, precision, and longevity — sought by collectors worldwide.")
prod_kno, new = PROD("Knoll Loibner Loibenberg Smaragd Gruner Veltliner", "wine_still", p_kno, r_wac, "Austria",
                     subcategory="Gruner Veltliner",
                     description="The Wachau's finest Grüner Veltliner from the Loibenberg's prime terraces — Smaragd weight with extraordinary mineral freshness. White pepper, citrus, green herbs, hazelnuts, and the distinctive Grüner Veltliner white pepper finish on ancient granite. Age-worthy and complex.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_kno, "Wiener Schnitzel (veal, not pork) with lingonberry jam and potato salad", "complement", "classic", "main", "Austria's national dish and its national wine variety — the Grüner's crisp acidity cuts through the breaded veal; white pepper mirrors the wine's characteristic spice; lingonberry provides fruity contrast")
    PAIR(prod_kno, "Asparagus (Spargel) with hollandaise, new potatoes, and prosciutto crudo", "complement", "classic", "starter", "Austrian spring asparagus and Grüner Veltliner is a Vienna restaurant tradition of decades; the wine's herbaceous character mirrors the vegetable; hollandaise is refreshed by the acid")

# ── CÔTE RÔTIE AOC (FRANCE) ───────────────────────────────────────
print("\n=== Côte Rôtie AOC (France) ===")
r_cro = R("Côte Rôtie", "France", "wine",
           designation_type="AOC",
           designation_name="Côte Rôtie AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="The northern Rhône's most prestigious appellation producing the world's most refined and age-worthy Syrah from impossibly steep granite slopes above Ampuis, south of Lyon. The 'Côte Brune' and 'Côte Blonde' sub-zones — named for the hair color of two medieval sisters — produce distinct styles: Côte Brune's iron-rich schist creates darker, more tannic wines while Côte Blonde's lighter granite produces more floral, aromatic Syrah. Up to 20% Viognier may be co-fermented.",
           key_producers="Guigal, René Rostaing, Stéphane Ogier, Clusel-Roch, Christophe Roumier",
           historical_context="Côte Rôtie's wines were described by Pliny the Elder as among Rome's finest. The appellation nearly disappeared by the 1960s when only 70 hectares remained under vine. Marcel Guigal's legendary single-vineyard wines — La Mouline, La Landonne, and La Turque (the 'La-Las') — saved the appellation's reputation in the 1970s. These three wines consistently receive the world's highest critical scores.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Côte Rôtie vintage; Syrah from the granite Côte Blonde showed extraordinary floral intensity; Côte Brune produced wines of exceptional dark power."),
    (2021, "very_good", "stable", "Classic northern Rhône vintage; cooler conditions produced elegant, aromatic Syrah with violet and olive complexity."),
    (2020, "excellent", "stable", "Benchmark year; Guigal La Mouline and Rostaing produced internationally acclaimed wines of legendary structure."),
    (2019, "exceptional", "rising", "Greatest Côte Rôtie vintage of the modern era; La Mouline and La Landonne achieved mythological status among collectors."),
    (2018, "excellent", "stable", "Excellent vintage; the heat ripened Syrah of extraordinary concentration balanced by the granite's natural freshness."),
]:
    VIN(r_cro, yr, qd, pt, sn)

p_rog = P("René Rostaing", "France", r_cro,
           description="René Rostaing's family estate in Ampuis produces Côte Rôtie of extraordinary purity and precision from the Côte Blonde and La Landonne parcels. The Rostaing style emphasizes transparency and aromatic finesse over power — considered among the appellation's most elegant and food-friendly expressions.")
prod_rog, new = PROD("Rostaing Côte Blonde Côte Rôtie", "wine_still", p_rog, r_cro, "France",
                     subcategory="Syrah",
                     description="The Côte Rôtie's most floral and perfumed expression — Syrah from the lighter granite Côte Blonde with a small percentage of co-fermented Viognier. Violet, white pepper, raspberry, olives, and a silky texture that belies the wine's underlying structure. The most feminine and accessible of the great Côte Rôtie wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_rog, "Roasted rack of lamb with lavender, thyme, and Provençal ratatouille", "complement", "classic", "main", "Syrah and roasted lamb is the northern Rhône's defining pairing; the wine's violet and herb character mirrors the lavender-thyme crust; ratatouille's Mediterranean vegetables bridge")
    PAIR(prod_rog, "Seared foie gras with quince paste and toasted brioche", "complement", "established", "starter", "Co-fermented Viognier gives the wine a rare apricot note that bridges foie gras; the wine's tannins cut through the fat; quince acidity lifts both")

p_ogi = P("Stéphane Ogier", "France", r_cro,
           description="The young Ogier family's Ampuis estate producing Côte Rôtie of modern precision and international acclaim. Michel Ogier's Réserve and Lancement wines established the family's reputation; son Stéphane's single-parcel bottlings have elevated the estate to Côte Rôtie's top tier.")
prod_ogi, new = PROD("Ogier Lancement Côte Rôtie", "wine_still", p_ogi, r_cro, "France",
                     subcategory="Syrah",
                     description="Stéphane Ogier's benchmark Côte Rôtie from the family's finest Côte Brune parcels — darker, more iron-driven, and more structured than Côte Blonde expressions. Black olive, iron, blackberry, smoked meat, and the northern Rhône granite mineral character. Exceptional aging potential.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_ogi, "Wild duck breast with tapenade, roasted beets, and black olive jus", "complement", "classic", "main", "The northern Rhône's greatest Syrah and game bird is a pairing of French gastronomic tradition; black olive in the tapenade mirrors the wine's olive character; beet echoes the iron mineral")
    PAIR(prod_ogi, "Char-grilled côte de boeuf with bone marrow butter and shallot confit", "complement", "established", "main", "Côte Rôtie's structured tannins and dark fruit demand the richest cut of beef; bone marrow mirrors the wine's body; shallot confit bridges the wine's violet aromatics")

# ── BANDOL AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Bandol AOC (France) ===")
r_ban = R("Bandol", "France", "wine",
           designation_type="AOC",
           designation_name="Bandol AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Provence's most serious and age-worthy wine appellation on limestone terraces above the fishing village of Bandol between Marseille and Toulon. Bandol Rouge requires minimum 50% Mourvèdre — one of the world's most demanding and rewarding red varieties — producing wines of extraordinary complexity, structure, and longevity that develop over 20+ years. The rare Bandol Blanc from Clairette, Ugni Blanc, and Bourboulenc is one of France's most individual dry whites.",
           key_producers="Domaine Tempier, Domaine de Pibarnon, Château Pradeaux, Domaine Ott, La Suffrène",
           historical_context="Mourvèdre — the grape that defines Bandol — is thought to have arrived from Valencia, Spain (as 'Monastrell') with medieval Spanish monks. Bandol received AOC status in 1941. Lucien Peyraud of Domaine Tempier — a friend of Richard Olney and Alice Waters — almost single-handedly saved Mourvèdre from extinction in the 1960s and established Bandol as a serious appellation worthy of cellaring.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Bandol vintage; Mourvèdre from limestone terraces showed extraordinary dark fruit depth and age-worthy structure."),
    (2021, "very_good", "stable", "Elegant Bandol vintage; cooler conditions produced more restrained Mourvèdre with excellent freshness and aging potential."),
    (2020, "excellent", "stable", "Benchmark year; Tempier La Migoua and Pibarnon both produced wines of the highest order."),
    (2019, "exceptional", "rising", "Greatest Bandol vintage of the modern era; wines of legendary Mourvèdre concentration and Mediterranean spice."),
    (2018, "excellent", "stable", "Excellent vintage; Mourvèdre's unique gamey, tar, and dark fruit character was more pronounced than any year this decade."),
]:
    VIN(r_ban, yr, qd, pt, sn)

p_tem = P("Domaine Tempier", "France", r_ban,
           description="The Peyraud family's legendary Bandol estate — the appellation's greatest ambassador and the wine that inspired a generation of American chefs through its association with Alice Waters and Kermit Lynch. Lulu Peyraud's kitchen at the domaine was one of France's most celebrated; the wines, particularly single-parcel La Migoua and La Tourtine, are benchmarks for age-worthy Mourvèdre.")
prod_tem, new = PROD("Domaine Tempier Bandol Rouge", "wine_still", p_tem, r_ban, "France",
                     subcategory="Mourvèdre",
                     description="The most celebrated Bandol rouge — predominantly Mourvèdre with Grenache and Cinsault from the Peyraud family's limestone terraces. Dark olive, tar, Mediterranean garrigue, blackberry, dried herbs, and a firm tannic structure that rewards 10-15 years of cellaring. Quintessentially Provençal.",
                     price_tier="premium")
if new:
    PAIR(prod_tem, "Bouillabaisse with rouille, Gruyère croûtons, and saffron broth", "complement", "classic", "main", "Provence's greatest fish stew and Provence's finest red — Mourvèdre's Mediterranean garrigue character mirrors the saffron; the wine's structure handles the rouille's richness")
    PAIR(prod_tem, "Grilled lamb chops with herbes de Provence, anchovies, and roasted garlic", "complement", "classic", "main", "Bandol and Provençal lamb is a pairing of centuries; the wine's garrigue character mirrors the herbes de Provence; anchovies add saline depth the Mourvèdre can handle")

p_pib = P("Domaine de Pibarnon", "France", r_ban,
           description="Henri de Saint-Victor's high-altitude Bandol estate at 300m on pure Triassic limestone produces the appellation's most elegant and age-worthy Mourvèdre. Pibarnon's elevation — unusually cool for Bandol — creates wines of finer tannin and greater aromatic complexity than lower-lying estates.")
prod_pib, new = PROD("Pibarnon Bandol Rouge", "wine_still", p_pib, r_ban, "France",
                     subcategory="Mourvèdre",
                     description="The most elegant Bandol from high-altitude limestone — less immediately powerful than Tempier but more aromatic and precise. Violet, Mediterranean herbs, black olive, plum, and the distinctive peppery Mourvèdre character with a long, mineral finish. Develops magnificently over 15-20 years.",
                     price_tier="premium")
if new:
    PAIR(prod_pib, "Wild boar daube with olives, orange zest, and Provençal herbs", "complement", "established", "main", "Provençal wild game stew and Bandol Mourvèdre — the wine's gamey character mirrors the boar; black olive finds direct resonance; orange zest bridges the wine's violet aromatics")
    PAIR(prod_pib, "Roasted leg of lamb with tapenade crust and gratin dauphinois", "complement", "classic", "main", "The Provençal celebration dish with the appellation's finest wine — tapenade's olive intensity mirrors the wine's olive character; the gratin's cream is structured by the Mourvèdre's tannins")

# ── NOVA SCOTIA (CANADA) ─────────────────────────────────────────
print("\n=== Nova Scotia (Canada) ===")
r_nos = R("Nova Scotia", "Canada", "wine",
           designation_type="GI",
           designation_name="Nova Scotia GI",
           reputation_tier="emerging",
           quality_trajectory="ascending",
           description="Canada's Atlantic coast wine region producing cool-climate wines from L'Acadie Blanc, Tidal Bay, Seyval Blanc, and Marquette from the Annapolis Valley, Malagash Peninsula, and Bear River sub-regions. Tidal Bay — a Nova Scotia-specific wine style defined by maximum 11% alcohol, residual sugar under 17g/L, and mandatory local grape content — is Canada's first appellation-specific wine style, celebrating the region's unique maritime terroir and tidal influence.",
           key_producers="Benjamin Bridge, Lightfoot & Wolfville, Blomidon Estate, Gaspereau Vineyards, L'Acadie Vineyards",
           historical_context="Nova Scotia's wine history began with Acadian French settlers in the 17th century. The modern era started with Roger Dial's pioneering plantings in the 1970s. Benjamin Bridge — founded by Gerry McConnell and Dara Gordon in 1999 — produced Nova Scotia's first serious sparkling wine and Tidal Bay, establishing the province's international reputation. Climate change is gradually expanding what varieties can ripen here.")

for yr, qd, pt, sn in [
    (2022, "very_good", "rising", "Outstanding Nova Scotia vintage; Tidal Bay and L'Acadie Blanc from the Annapolis Valley showed extraordinary maritime freshness."),
    (2021, "good", "stable", "Challenging cool vintage; Benjamin Bridge sparkling wines showed exceptional base wine quality from the adversity."),
    (2020, "very_good", "stable", "Benchmark year; Tidal Bay from multiple producers captured international attention for the first time."),
    (2019, "very_good", "rising", "Outstanding vintage; Benjamin Bridge Nova 7 and Tidal Bay both gained major international wine press coverage."),
    (2018, "good", "stable", "Solid vintage; L'Acadie Blanc and Seyval Blanc wines showed good varietal character; sparkling base wine excellent."),
]:
    VIN(r_nos, yr, qd, pt, sn)

p_ben = P("Benjamin Bridge", "Canada", r_nos,
           description="Nova Scotia's most internationally acclaimed winery, producing Canada's Atlantic coast benchmark sparkling wines and Tidal Bay from organic L'Acadie Blanc, Vidal, and Chardonnay in the Gaspereau Valley. Nova 7 — a barely sparkling muscat-style pét-nat — became Canada's most sought-after white wine and a cult item in restaurants globally.")
prod_ben, new = PROD("Benjamin Bridge Nova 7", "wine_sparkling", p_ben, r_nos, "Canada",
                     subcategory="L'Acadie Blanc Blend",
                     description="Nova Scotia's most celebrated wine — a slightly sparkling, off-dry blend of L'Acadie Blanc, Muscat, and Vidal from organic Gaspereau Valley vineyards. Peach, apricot, orange blossom, and the sea air of the Atlantic coast. Light, joyful, and utterly distinctive. Canada's most sought-after summer wine.",
                     price_tier="mid_range")
if new:
    PAIR(prod_ben, "Digby scallops with lemon brown butter and sea beans", "complement", "classic", "main", "Nova Scotia's finest shellfish and Nova Scotia's finest wine — the wine's peach and sea-air character bridges the scallop's sweetness; sea beans add briny resonance")
    PAIR(prod_ben, "Chilled lobster salad with tarragon mayonnaise and buttered brioche", "complement", "classic", "aperitif", "Atlantic Canadian lobster and the province's benchmark sparkling wine — the wine's effervescence and tropical fruit lifts the lobster richness; tarragon bridges the wine's herb notes")

p_lig = P("Lightfoot & Wolfville", "Canada", r_nos,
           description="Jost Vineyards family's boutique Wolfville estate producing organic and biodynamic Tidal Bay and Pinot Noir from the Annapolis Valley's unique clay-loam and sandstone soils. Lightfoot & Wolfville is considered one of Nova Scotia's most quality-focused producers, with wines that reflect the Valley's maritime terroir with clarity.")
prod_lig, new = PROD("Lightfoot and Wolfville Tidal Bay", "wine_still", p_lig, r_nos, "Canada",
                     subcategory="Tidal Bay",
                     description="Nova Scotia's signature wine style from L'Acadie Blanc and Seyval Blanc — crisp, mineral, and distinctly maritime. Lemon, green apple, sea air, mineral freshness, and the characteristic Atlantic freshness that defines this uniquely Canadian wine style. Under 11% alcohol, perfectly fresh.",
                     price_tier="mid_range")
if new:
    PAIR(prod_lig, "Steamed Mahone Bay mussels with white wine, shallots, and parsley", "complement", "classic", "main", "Nova Scotia mussels and Nova Scotia Tidal Bay is a pairing of shared terroir — the wine often appears in the cooking liquid; sea air and minerality mirror the mussels' brine")
    PAIR(prod_lig, "Smoked salmon with cream cheese, dill, capers, and rye crispbread", "complement", "established", "aperitif", "Atlantic smoked salmon and Atlantic white wine — the wine's crisp acidity cuts through the cream cheese; lemon and dill in the garnish echo the wine's citrus character")

# ── SAVOIE AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Savoie AOC (France) ===")
r_sav = R("Savoie", "France", "wine",
           designation_type="AOC",
           designation_name="Savoie AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="France's alpine wine region producing intensely mineral, refreshing whites from indigenous Jacquère, Altesse (Roussette), and Chasselas from lakeside and mountain terroir at 200-600m altitude in the Savoie and Haute-Savoie departments. The wines of Savoie — electric, low-alcohol, and distinctly alpine — are the ideal partner for the region's famous raclette, fondue, and charcuterie traditions. Mondeuse, Savoie's red variety, produces a distinctive peppery, tannic wine unique to the alpine environment.",
           key_producers="Domaine Belluard, Michel Grisard, André and Michel Quenard, Domaine Prieuré Saint Christophe, Labbé",
           historical_context="Savoie wines were traded across the Alps with Geneva and Turin for centuries. The vineyards survived the Phylloxera crisis largely because the grafting of vines onto American rootstock was slow and expensive in the steep alpine terrain. The late 20th century rediscovery of indigenous varieties — particularly Gringet (at Ayze) and Altesse — has driven a quality renaissance led by natural wine producers like Dominique Belluard.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Savoie vintage; Jacquère and Altesse from lakeside and alpine terroir showed extraordinary mineral precision."),
    (2021, "very_good", "stable", "Elegant alpine vintage; Mondeuse and Jacquère produced wines of exceptional freshness and mineral vitality."),
    (2020, "excellent", "stable", "Benchmark year; Belluard Gringet and Quenard Chignin-Bergeron received major international natural wine attention."),
    (2019, "very_good", "rising", "Outstanding vintage; the combination of warmth and alpine freshness produced Altesse of unusual richness and mineral depth."),
    (2018, "very_good", "stable", "Solid vintage; Roussette de Savoie and Chignin-Bergeron both excelled in the alpine conditions."),
]:
    VIN(r_sav, yr, qd, pt, sn)

p_bel = P("Domaine Belluard", "France", r_sav,
           description="Dominique Belluard's biodynamic Ayze estate producing the most sought-after Gringet (the ancient alpine white variety) and Jacquère wines in Savoie. Le Feu and Mont-Blanc sparkling Gringet are cult items in Paris's natural wine scene; Belluard's work has single-handedly saved Gringet from extinction.")
prod_bel, new = PROD("Belluard Mont Blanc Gringet", "wine_sparkling", p_bel, r_sav, "France",
                     subcategory="Gringet",
                     description="The rarest and most sought-after alpine sparkling wine — ancient Gringet variety from high-altitude Ayze terraces made pétillant naturel. Alpine flowers, lemon, mineral freshness, and a wild, electric character unique to this forgotten variety. One of France's most distinctive and unrepeatable wines.",
                     price_tier="premium")
if new:
    PAIR(prod_bel, "Fondue Savoyarde with Comté, Beaufort, and Abondance with crusty bread", "complement", "classic", "main", "The Savoie's supreme pairing — alpine wine and alpine cheese fondue from the same mountain culture; the wine's mineral freshness and acidity cuts through the melted cheese")
    PAIR(prod_bel, "Raclette with cornichons, pickled onions, charcuterie, and boiled potatoes", "complement", "classic", "main", "The Valais and Savoie's shared mountain tradition — alpine sparkling wine and melted raclette cheese; the wine's electric acidity and bubbles refresh through every rich bite")

p_que = P("André et Michel Quenard", "France", r_sav,
           description="The Quenard family's Chignin estate has produced Savoie's benchmark Bergeron (Roussanne from the Chignin village) for generations. Chignin-Bergeron is Savoie's most complex and age-worthy white wine; the Quenard family's old vines produce a wine that rivals white Hermitage for Roussanne depth.")
prod_que, new = PROD("Quenard Chignin-Bergeron Roussanne", "wine_still", p_que, r_sav, "France",
                     subcategory="Roussanne",
                     description="Savoie's most complex white wine from old-vine Roussanne (locally called Bergeron) from the south-facing Chignin slope — white peach, almond, mountain herbs, honey, and the distinctive alpine mineral freshness. More textural and generous than Jacquère; shows Burgundian white wine influence with alpine character.",
                     price_tier="premium")
if new:
    PAIR(prod_que, "Gratin de crozets (buckwheat pasta gratin with Reblochon and lardons)", "complement", "classic", "main", "The Savoie's winter mountain classic and its finest white wine — Roussanne's texture and almond richness complements the gratin; Reblochon's earthy character bridges the wine's mineral depth")
    PAIR(prod_que, "Omble chevalier (Arctic char) with brown butter and wild alpine herbs", "complement", "classic", "main", "Savoie's prized alpine lake fish and the region's finest white — Roussanne's peach and almond character mirrors the char's delicate flesh; alpine herbs create regional harmony")

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
