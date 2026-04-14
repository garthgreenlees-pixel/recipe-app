#!/usr/bin/env python3
"""T23 Batch 13 — New wine regions: Chablis AOC (France), Sancerre AOC (France), Mosel (Germany), Clare Valley GI (Australia), Valpolicella DOC (Italy)"""

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

# ── CHABLIS AOC (FRANCE) ─────────────────────────────────────────
print("\n=== Chablis AOC (France) ===")
r_cha = R("Chablis", "France", "wine",
           designation_type="AOC",
           designation_name="Chablis AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Burgundy's northernmost appellation producing the world's most distinctive Chardonnay — unoaked, austere, and defined by the Kimmeridgian limestone and oyster-shell fossils of the Serein Valley. Chablis Grand Cru and Premier Cru wines from the seven Grand Cru vineyards (including Valmur, Les Clos, and Bougros) are among the world's greatest white wines. The region's extreme northern continental climate creates wines of pure mineral precision.",
           key_producers="William Fèvre, Domaine Raveneau, Vincent Dauvissat, Louis Michel, Domaine Laroche",
           historical_context="Chablis was established as an AOC in 1938. For much of the 20th century the region was plagued by frost — until frost control methods made viticulture viable in the 1970s and the region expanded dramatically. The debate over whether Premier Cru wines should use oak continues. Domaine Raveneau — never releasing enough wine to meet demand — is considered the region's greatest producer.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Chablis vintage; Grand Cru wines of extraordinary mineral intensity and Premier Cru of exceptional precision."),
    (2021, "very_good", "stable", "Classic Chablis vintage; Kimmeridgian minerality was pronounced; Les Clos and Valmur excelled."),
    (2020, "exceptional", "rising", "Greatest Chablis vintage of the modern era; Raveneau and Dauvissat produced wines of legendary mineral depth."),
    (2019, "excellent", "stable", "Benchmark year; the combination of warmth and minerality produced Grand Crus of extraordinary complexity."),
    (2018, "excellent", "stable", "Excellent vintage; warmer year produced Chablis of more generous fruit but still characteristic mineral backbone."),
]:
    VIN(r_cha, yr, qd, pt, sn)

p_rav = P("Domaine Raveneau", "France", r_cha,
           description="The most sought-after and rarely available Chablis producer — Jean-Marie Raveneau's tiny estate consistently produces the appellation's finest wines from Premier and Grand Cru parcels. Raveneau's wines, with decades of aging potential, are benchmarks for how profound Chablis can be.")
prod_rav, new = PROD("Raveneau Chablis Premier Cru Montee de Tonnerre", "wine_still", p_rav, r_cha, "France",
                     subcategory="Chardonnay",
                     description="One of France's most coveted white wines — Chablis Premier Cru from the south-facing Kimmeridgian slope above the Serein. Oyster shell, white flower, green apple, flint, and a saline intensity that seems to channel the ancient sea floor. Demands 10+ years of cellaring to reach its peak.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_rav, "Freshly shucked Gillardeau oysters with lemon and rye bread", "complement", "classic", "aperitif", "The most celebrated pairing in white wine — Chablis and oysters share Kimmeridgian fossils; the wine's saline mineral character is the oyster's perfect reflection")
    PAIR(prod_rav, "Sole meunière with brown butter, capers, and flat-leaf parsley", "complement", "classic", "main", "Chablis and sole is a Loire-Burgundy classic; the wine's mineral precision and citrus notes mirror the fish's delicate flavour; butter bridges the richness")

p_dau = P("Vincent Dauvissat", "France", r_cha,
           description="Vincent Dauvissat's biodynamically farmed Chablis estate is considered co-equal with Raveneau as the appellation's greatest producer. The Dauvissat style is more linear and austere than Raveneau — Les Clos Grand Cru is one of France's most profound white wines.")
prod_dau, new = PROD("Dauvissat Chablis Grand Cru Les Clos", "wine_still", p_dau, r_cha, "France",
                     subcategory="Chardonnay",
                     description="The pinnacle of Chablis — Grand Cru Les Clos from Dauvissat's biodynamic vines on pure Kimmeridgian limestone. A wine of extraordinary tension: flint, chalk, iodine, white fruit, and a finish that seems to last forever. One of the world's ten greatest white wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_dau, "Turbot en croute de sel with sauce Choron and wild sea herbs", "complement", "classic", "main", "The world's finest flatfish and one of the world's finest white wines — shared mineral tension; the sauce's tarragon complexity mirrors the wine's herbal nuance")
    PAIR(prod_dau, "Langoustines with seaweed butter and Chablis reduction", "complement", "classic", "starter", "A gastronomic statement — the wine appears in the sauce itself; Kimmeridgian minerals and crustacean sweetness in perfect dialogue")

# ── SANCERRE AOC (FRANCE) ─────────────────────────────────────────
print("\n=== Sancerre AOC (France) ===")
r_san = R("Sancerre", "France", "wine",
           designation_type="AOC",
           designation_name="Sancerre AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="The Loire Valley's most celebrated appellation producing the world's benchmark Sauvignon Blanc from three distinct soil types: Kimmeridgian limestone (terres blanches), flinty silex, and gravel (caillottes). Sancerre also produces small quantities of Pinot Noir of elegant cool-climate character. The wines' combination of citrus, gooseberry, and mineral character set the global standard for the Sauvignon Blanc variety.",
           key_producers="Henri Bourgeois, Domaine Vacheron, Didier Dagueneau, Henri Pellé, Alphonse Mellot",
           historical_context="Sancerre received AOC status in 1936. The appellation's fame spread globally through the 1970s when the combination of New World wine interest and French bistro culture made Sancerre synonymous with sophisticated white wine. Didier Dagueneau — who died in 2008 — raised the region's quality ceiling dramatically through his obsessive approach to low yields and old vines.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Sancerre vintage; Sauvignon Blanc from silex and terres blanches showed extraordinary mineral complexity."),
    (2021, "very_good", "stable", "Elegant cool-climate vintage; the Loire's acid freshness produced wines of compelling precision."),
    (2020, "excellent", "stable", "Benchmark year; Vacheron and Bourgeois produced Sancerre of exceptional depth and aging potential."),
    (2019, "exceptional", "rising", "Finest Sancerre vintage in a generation; Pinot Noir and Sauvignon Blanc both reached extraordinary quality."),
    (2018, "excellent", "stable", "Excellent vintage; the warmth produced generous, aromatic Sancerre with unusual concentration."),
]:
    VIN(r_san, yr, qd, pt, sn)

p_vach = P("Domaine Vacheron", "France", r_san,
            description="Jean-Laurent and Jean-Dominique Vacheron's biodynamic Sancerre estate is considered the appellation's finest producer alongside the late Didier Dagueneau. The Vacheron style emphasizes terroir expression from different soil types — their silex, terres blanches, and caillottes bottlings demonstrate the appellation's remarkable diversity.")
prod_vach, new = PROD("Vacheron Sancerre Blanc", "wine_still", p_vach, r_san, "France",
                      subcategory="Sauvignon Blanc",
                      description="The benchmark for Sancerre's mineral Sauvignon Blanc from biodynamic silex and terres blanches — grapefruit, gooseberry, cut grass, white flower, and a streak of flint that defines the appellation. Dry, precise, and beautifully balanced with genuine aging potential.",
                      price_tier="premium")
if new:
    PAIR(prod_vach, "Crottin de Chavignol (Loire goat's cheese) with walnut bread", "complement", "classic", "cheese", "The appellation's most celebrated pairing — Loire goat cheese and Sancerre from the same hillside; the wine's acidity and mineral freshness cuts through the cheese's tang")
    PAIR(prod_vach, "Grilled asparagus with Hollandaise and shaved Mimolette", "complement", "established", "starter", "Sauvignon Blanc and asparagus is a Loire spring classic; the wine's herbaceous character mirrors the vegetable; Hollandaise's richness is refreshed by the wine's acid")

p_bou = P("Henri Bourgeois", "France", r_san,
           description="The Bourgeois family's substantial Sancerre estate spanning multiple vineyard sites across all three soil types. La Bourgeoise and D'Antan cuvées are among Sancerre's finest wines; their Mondense Sancerre Rouge demonstrates the appellation's underrated Pinot Noir potential.")
prod_bou, new = PROD("Henri Bourgeois La Bourgeoise Sancerre", "wine_still", p_bou, r_san, "France",
                     subcategory="Sauvignon Blanc",
                     description="Old-vine Sancerre from the Bourgeois family's finest terres blanches parcels — more textural and complex than the entry-level, with greater mineral depth and aging potential. Grapefruit, white peach, flint, and a long, saline mineral finish.",
                     price_tier="premium")
if new:
    PAIR(prod_bou, "Moules marinières with shallots, white wine, and cream", "complement", "classic", "main", "The Breton-Loire pairing — Sancerre's acidity is perfect for mussels; the wine often appears in the sauce; cream bridges the wine's freshness")
    PAIR(prod_bou, "Seared scallops with pea purée, mint oil, and crispy capers", "complement", "established", "starter", "The wine's mineral precision and citrus notes complement the scallop's sweetness; pea purée echoes the Sauvignon's green herbal character")

# ── MOSEL (GERMANY) ───────────────────────────────────────────────
print("\n=== Mosel (Germany) ===")
r_mos = R("Mosel", "Germany", "wine",
           designation_type="Qualitätswein",
           designation_name="Mosel Qualitätswein",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Germany's most celebrated wine region tracing the serpentine Mosel River between Koblenz and Trier. The world's steepest commercial vineyards on Devonian slate slopes produce Riesling of unmatched aromatic intensity, mineral precision, and longevity at low alcohol. The Mosel's Spätlese, Auslese, Beerenauslese, and Trockenbeerenauslese wines are among the world's greatest dessert wines; the dry Grosses Gewächs Rieslings are equally profound.",
           key_producers="Egon Müller, JJ Prüm, Moselland, Clemens Busch, Markus Molitor",
           historical_context="The Mosel has produced wine for over 2,000 years — Roman amphoras have been found throughout the valley. The Bernkastel Doctor vineyard, reputedly responsible for curing a medieval elector's illness, became Germany's most famous single vineyard. Egon Müller's Scharzhofberger Trockenbeerenauslese consistently ranks among the world's most expensive wines at auction.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Mosel vintage; Riesling from slate vineyards showed extraordinary aromatic precision and mineral depth."),
    (2021, "very_good", "stable", "Classic Mosel vintage; cool conditions produced wines of haunting aromatic elegance and exceptional aging potential."),
    (2020, "excellent", "stable", "Benchmark year; JJ Prüm and Egon Müller produced Auslese and Spätlese of extraordinary complexity."),
    (2019, "exceptional", "rising", "Greatest Mosel vintage of the century so far; the combination of warmth and freshness produced Spätlese of legendary quality."),
    (2018, "excellent", "stable", "Excellent vintage; the warmth produced unusually concentrated Riesling with the characteristic Mosel slate minerality."),
]:
    VIN(r_mos, yr, qd, pt, sn)

p_jjp = P("JJ Prüm", "Germany", r_mos,
           description="The Prüm family's estate in Wehlen is one of the Mosel's most distinguished producers, with prime parcels in the Wehlener Sonnenuhr, Graacher Himmelreich, and Bernkasteler Lay vineyards. JJ Prüm's Auslese and Spätlese wines, bottled under green Mosel capsules, are benchmarks of German Riesling aged in old slate cellars.")
prod_jjp, new = PROD("JJ Prum Wehlener Sonnenuhr Spatlese", "wine_still", p_jjp, r_mos, "Germany",
                     subcategory="Riesling",
                     description="The classic Mosel Spätlese expression from the world-famous sundial vineyard on blue Devonian slate. Peach, apricot, lime zest, white flower, and the haunting slate mineral character — off-dry, intensely aromatic, and capable of developing for 30+ years in bottle.",
                     price_tier="premium")
if new:
    PAIR(prod_jjp, "Foie gras terrine with Riesling jelly, brioche, and Sauternes reduction", "complement", "classic", "starter", "The world's most classic sweet wine and foie gras dialogue in a Mosel key — the wine's residual sweetness and mineral acidity cuts through the fat; fruit resonance")
    PAIR(prod_jjp, "Asian-spiced pork belly with five-spice, ginger, and pickled cucumber", "complement", "established", "main", "Mosel Spätlese and Asian spice is one of gastronomy's great modern discoveries — the residual sugar and acidity handles chilli heat; fruit mirrors the five-spice")

p_cbu = P("Clemens Busch", "Germany", r_mos,
           description="Biodynamic Mosel pioneer in the Pünderich and Marienburg vineyards producing dry and off-dry Riesling of extraordinary mineral intensity. Clemens Busch's Fahrlay and Marienburg Grosses Gewächs wines are considered the Mosel's finest dry Rieslings — rivaling Alsace and Austria in structural complexity.")
prod_cbu, new = PROD("Clemens Busch Marienburg Rothenpfad GG Riesling", "wine_still", p_cbu, r_mos, "Germany",
                     subcategory="Riesling",
                     description="The pinnacle of dry Mosel Riesling — Grosses Gewächs from the legendary red slate Rothenpfad parcel on the Marienburg. Entirely bone dry, intensely mineral, with lime, peach, white pepper, and a slate-driven mineral intensity that develops magnificently over decades.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_cbu, "Grilled pike-perch with Riesling butter sauce and green asparagus", "complement", "classic", "main", "German freshwater fish and Mosel Riesling is a centuries-old pairing; the wine appears in the sauce; mineral slate character mirrors the fish's clean flavour")
    PAIR(prod_cbu, "Tarte flambée with crème fraîche, smoked Schwarzwälder ham, and onion", "complement", "established", "aperitif", "Alsatian cross-border pairing — dry Riesling's mineral precision and citrus refreshes through the cream and smoky pork; onion caramelization bridges the wine's fruit")

# ── CLARE VALLEY GI (AUSTRALIA) ───────────────────────────────────
print("\n=== Clare Valley GI (Australia) ===")
r_cla = R("Clare Valley", "Australia", "wine",
           designation_type="GI",
           designation_name="Clare Valley GI",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="South Australia's premier cool-climate wine enclave at 400-500m altitude north of Adelaide, producing Australia's finest Riesling — steely, lime-driven, and capable of extraordinary development in bottle. The Polish Hill River and Watervale sub-regions on ancient limestone and sandy loam produce distinctly different Riesling styles. Clare Valley also excels with Shiraz and Cabernet Sauvignon of impressive structure.",
           key_producers="Grosset, Jim Barry, Knappstein, Pikes, Kilikanoon",
           historical_context="The Clare Valley's first vines were planted by Polish settlers (hence Polish Hill River) and Jesuits at Sevenhill in 1851. Jeffrey Grosset — who started his winery in 1981 — revolutionized Australian Riesling by pioneering screw cap closures in 2000, preventing premature oxidation. The Clare's Riesling under screw cap ages magnificently for 20-30 years.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Clare Valley vintage; Riesling from Polish Hill River showed extraordinary lime zest precision and mineral depth."),
    (2021, "very_good", "stable", "Classic cool South Australian vintage; Grosset Polish Hill achieved remarkable tension and aging potential."),
    (2020, "excellent", "stable", "Benchmark year; the combination of warmth and altitude produced Riesling of uncommon concentration and Shiraz of power."),
    (2019, "exceptional", "rising", "Greatest Clare Valley vintage of the decade; Riesling from all sub-regions reached extraordinary quality levels."),
    (2018, "excellent", "stable", "Excellent vintage; Watervale and Polish Hill Riesling showed distinct terroir expression at the highest quality."),
]:
    VIN(r_cla, yr, qd, pt, sn)

p_gro = P("Grosset Wines", "Australia", r_cla,
           description="Jeffrey Grosset's Clare Valley estate is Australia's most important Riesling producer and a pioneer of the screw cap revolution. Grosset Polish Hill and Springvale Rieslings are regularly placed among the world's finest, demonstrating that Australian Riesling can age as magnificently as German or Alsatian counterparts.")
prod_gro, new = PROD("Grosset Polish Hill Riesling", "wine_still", p_gro, r_cla, "Australia",
                     subcategory="Riesling",
                     description="Australia's greatest Riesling from the stony Polish Hill River sub-region — bone dry, taut, and almost forbiddingly austere when young. Lime zest, crushed stone, white flower, and minerality that recalls Mosel slate. Under screw cap, develops magnificently for 20+ years into a complex, toasty, kerosene-tinged marvel.",
                     price_tier="premium")
if new:
    PAIR(prod_gro, "Garlic and chilli prawns with lemon and sourdough croutons", "complement", "classic", "main", "Australia's Riesling and Southeast Queensland prawns — the wine's citrus precision and mineral freshness cuts through the garlic butter; chilli heat is tempered by the wine's linearity")
    PAIR(prod_gro, "Salt and pepper calamari with aioli and lemon", "complement", "classic", "aperitif", "A great Australian pub pairing elevated — Riesling's citrus and mineral character mirrors lemon; the wine's austerity refreshes through the batter's richness")

p_jim = P("Jim Barry Wines", "Australia", r_cla,
           description="The Barry family's substantial Clare Valley estate encompassing multiple sub-regions and producing both definitive Riesling and one of Australia's most celebrated Shiraz — The Armagh, produced from a single parcel of ancient Clare Shiraz vines considered Australia's equivalent to a Rhône Grand Cru.")
prod_jim, new = PROD("Jim Barry The Lodge Hill Riesling", "wine_still", p_jim, r_cla, "Australia",
                     subcategory="Riesling",
                     description="Jim Barry's benchmark entry-level Clare Riesling from the higher-altitude Lodge Hill vineyard — pure, dry, and minerally expressive. Lime juice, green apple, citrus blossom, and the characteristic Clare Valley steeliness. Outstanding value and genuine aging potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_jim, "Thai green curry with chicken, coconut milk, and kaffir lime", "complement", "established", "main", "Riesling's lime and mineral character finds direct resonance in the kaffir lime; the wine's steeliness handles coconut richness; dry Clare style prevents over-sweetness")
    PAIR(prod_jim, "Yum cha dumplings — har gow, siu mai, and char siu bao", "complement", "established", "main", "Australian Riesling and Asian dim sum is a celebrated modern pairing; the wine's citrus and mineral character refreshes through the varied dumpling flavours")

# ── VALPOLICELLA DOC (ITALY) ─────────────────────────────────────
print("\n=== Valpolicella DOC (Italy) ===")
r_val = R("Valpolicella", "Italy", "wine",
           designation_type="DOC",
           designation_name="Valpolicella DOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="The Veneto's most important red wine appellation in the hills northwest of Verona, producing Valpolicella from Corvina, Rondinella, and Molinara grapes in multiple styles: the light, fresh DOC Classico; the dried-grape Amarone della Valpolicella DOCG (one of Italy's greatest red wines); the semi-sweet Recioto; and the rich Ripasso method (re-fermented on Amarone skins). The appellation's range from light luncheon wine to the world's most powerful dry red is unique.",
           key_producers="Romano Dal Forno, Giuseppe Quintarelli, Allegrini, Masi, Zenato",
           historical_context="Valpolicella has been produced since Roman times; Virgil mentioned wines from the Veronese hills. The appassimento (grape drying) technique that creates Amarone was formalized in the 1950s when a Recioto fermented too dry — the winemaker reportedly called it 'amaro' (bitter), hence Amarone. Romano Dal Forno and Giuseppe Quintarelli elevated the category to international cult status.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Valpolicella vintage; Amarone of extraordinary concentration and Ripasso of elegant depth."),
    (2021, "very_good", "stable", "Classic vintage; the Classico zone produced Corvina of exceptional varietal purity and Amarone of great structure."),
    (2020, "excellent", "stable", "Benchmark year; Dal Forno and Quintarelli Amarone from this vintage will require decades of aging."),
    (2019, "exceptional", "rising", "Finest Valpolicella vintage of the modern era; Amarone of legendary concentration and complexity at all quality levels."),
    (2018, "excellent", "stable", "Excellent vintage; the appassimento conditions were ideal, producing Amarone of perfect balance between power and freshness."),
]:
    VIN(r_val, yr, qd, pt, sn)

p_all = P("Allegrini", "Italy", r_val,
           description="One of Valpolicella's most commercially significant and critically respected estates, producing Amarone, Ripasso, and the innovative single-variety 'La Poja' Corvina. The Allegrini family has been instrumental in raising Valpolicella's international reputation since the 1980s.")
prod_all, new = PROD("Allegrini Amarone della Valpolicella Classico", "wine_still", p_all, r_val, "Italy",
                     subcategory="Amarone",
                     description="One of Italy's most celebrated red wines — Corvina, Rondinella, and Oseleta dried for 90 days before pressing, creating extraordinary concentration: dried cherry, chocolate, coffee, bitter herb, and cedar with 15-16% alcohol balanced by the variety's natural acidity. One of the world's most powerful dry red wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_all, "Brasato all'Amarone (beef braised in Amarone) with polenta", "complement", "classic", "main", "The wine appears in the cooking liquid of Verona's most famous dish — Amarone's concentrated dark fruit and spice infuses the braising; a circular, self-reinforcing pairing of extraordinary depth")
    PAIR(prod_all, "Aged Monte Veronese cheese with bitter honey and toasted pine nuts", "complement", "classic", "cheese", "The wine's bittersweet chocolate and coffee character finds resonance in the bitter honey; aged Veronese cheese's intensity is matched by the wine's power")

p_zen = P("Zenato", "Italy", r_val,
           description="The Zenato family's Peschiera del Garda estate spanning both Valpolicella and Soave, producing Ripasso della Valpolicella Superiore and Amarone of excellent consistency and value. Zenato's Ripasso — re-fermented on dried Corvina skins — is one of Italy's best-selling premium reds.")
prod_zen, new = PROD("Zenato Ripassa Valpolicella Superiore", "wine_still", p_zen, r_val, "Italy",
                     subcategory="Ripasso",
                     description="The benchmark for Ripasso della Valpolicella — Corvina and Rondinella re-fermented on dried Amarone pomace, gaining concentration, complexity, and richness without full Amarone weight. Dried cherry, cocoa, vanilla, and spice with the Corvina variety's characteristic sour cherry core.",
                     price_tier="mid_range")
if new:
    PAIR(prod_zen, "Osso buco alla Milanese with gremolata and saffron risotto", "complement", "established", "main", "The Ripasso's dried-fruit richness and vanilla complement the braised veal's gelatin depth; saffron's bitterness is bridged by the wine's cocoa notes")
    PAIR(prod_zen, "Pappardelle al ragù di cinghiale (wild boar) with Parmigiano", "complement", "classic", "main", "Northern Italian game pasta and the Veneto's signature dried-grape wine — the Ripasso's concentration handles the boar's intensity; dried cherry echoes the ragù's richness")

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
