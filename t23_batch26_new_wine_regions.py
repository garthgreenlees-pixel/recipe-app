#!/usr/bin/env python3
"""T23 Batch 26 — New wine regions: Morgon AOC (France), Rías Baixas DO (Spain), Pessac-Léognan AOC (France), Trentino-Alto Adige DOC (Italy), Cannonau di Sardegna DOC (Italy)"""

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

# ── MORGON AOC (FRANCE) ───────────────────────────────────────────
print("\n=== Morgon AOC (France) ===")
r_mor = R("Morgon", "France", "wine",
           designation_type="AOC",
           designation_name="Morgon AOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The most structured and age-worthy of the Beaujolais crus — the volcanic Côte du Py and schist soils of Morgon produce Gamay of extraordinary depth, iron mineral, and longevity that regularly develops into wine resembling mature Burgundian Pinot Noir. Morgon is the beating heart of the natural wine movement: Marcel Lapierre's minimal-intervention Gamay from the 1980s inspired a generation of natural winemakers worldwide, and Morgon's Gang of Four (Lapierre, Foillard, Breton, and Thévenet) created the template for carbonic maceration natural wine that now appears on bistro lists from Tokyo to New York.",
           key_producers="Marcel Lapierre, Jean Foillard, Guy Breton, Louis-Claude Desvignes, Jean-Paul Thévenet",
           historical_context="Jules Chauvet — the Beaujolais merchant and biochemist who died in 1989 — was the philosophical godfather of the natural wine movement. His rejection of chaptalization, sulphur, and industrial yeast, and his embrace of carbonic maceration for Gamay, was passed to Marcel Lapierre in the 1970s, who created the template for natural Beaujolais that Foillard, Breton, and Thévenet followed. When Robert Parker scored Lapierre Morgon 94 points in 1993, the international wine press discovered that serious natural wine existed. Today Morgon is the world's most cited Beaujolais cru for serious collectors, and the Côte du Py — the extinct volcanic hill at the appellation's heart — is considered the region's grand cru equivalent.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Morgon vintage; Gamay from Côte du Py volcanic schist showed extraordinary iron mineral depth and the rare structured tannin of a genuinely age-worthy Beaujolais."),
    (2021, "very_good", "stable", "Classic vintage; cool conditions produced wines of excellent freshness and transparency; natural winemakers particularly pleased with the carbonic maceration results."),
    (2020, "excellent", "stable", "Benchmark year; Lapierre and Foillard both produced Morgon of historic depth and longevity; Côte du Py wines destined for 10+ year development."),
    (2019, "exceptional", "rising", "Greatest Morgon vintage of the era; Gamay of legendary iron-mineral concentration and longevity; the cru's status as Beaujolais's finest confirmed internationally."),
    (2018, "very_good", "stable", "Warm vintage producing generous Morgon of good concentration; schist and volcanic soils retained freshness; natural wines of unusual immediate appeal."),
]:
    VIN(r_mor, yr, qd, pt, sn)

p_lap = P("Marcel Lapierre", "France", r_mor,
           description="The patron saint of natural Beaujolais — Marcel Lapierre's decision in the 1970s to follow Jules Chauvet's zero-sulphur, carbonic maceration methods created the template for natural wine that inspired a global movement. His son Mathieu continues the estate's biodynamic and minimal-intervention approach from the Côte du Py volcanic schist. Marcel Lapierre Morgon is the world's most recognizable natural Beaujolais and arguably the most influential natural wine producer in history.")
prod_lap, new = PROD("Marcel Lapierre Morgon", "wine_still", p_lap, r_mor, "France",
                     subcategory="Gamay",
                     description="The world's most influential natural Beaujolais — Gamay from the Côte du Py volcanic schist, carbonic maceration, zero sulphur, bottled unfined and unfiltered. Translucent red cherry, wild raspberry, iron mineral, violet, spring flowers, and the haunting purity that makes this wine the template for natural winemaking worldwide. Deceivingly delicate in youth; develops Pinot-like complexity over 5-10 years. The wine that started a movement.",
                     price_tier="mid_range")
if new:
    PAIR(prod_lap, "Andouillette de Troyes (tripe sausage) with Dijon mustard and pommes vapeur", "complement", "classic", "main", "France's most confrontational charcuterie and natural Beaujolais — Morgon's iron mineral and wild cherry cuts through the andouillette's intense offal richness; Dijon's heat is tempered by the wine's fruity transparency")
    PAIR(prod_lap, "Lyonnaise charcuterie board — saucisson à cuire, cervelas, and rosette with Beaujolais", "complement", "classic", "aperitif", "The Lyon bouchon tradition and its natural Beaujolais — Morgon's cherry and iron mineral cuts through varied pork textures; saucisson's black pepper bridges the wine's mineral depth")

p_foi = P("Jean Foillard", "France", r_mor,
           description="One of Morgon's Gang of Four — Jean Foillard's Côte du Py estate produces the most internationally sought-after and cellar-worthy natural Morgon. The Côte du Py cuvée from the volcanic schist heart of Morgon achieves iron-mineral depth and tannic structure that requires 5-10 years to reveal its full potential. Foillard's wines appear on the lists of the world's most prestigious natural wine restaurants from Paris to Tokyo.")
prod_foi, new = PROD("Jean Foillard Morgon Côte du Py", "wine_still", p_foi, r_mor, "France",
                     subcategory="Gamay",
                     description="The most age-worthy natural Morgon — Gamay from the Côte du Py's extinct volcano core, carbonic maceration, minimal sulphur. Iron, dark cherry, crushed schist mineral, violets, and the extraordinary tannic grip that distinguishes the Py from all other Morgon parcels. Needs 5-7 years to open; at 10 years resembles aged Vosne-Romanée. The definitive expression of Morgon's volcanic terroir.",
                     price_tier="mid_range")
if new:
    PAIR(prod_foi, "Pigeon rôti with lentilles du Puy, lardons fumés, and truffle vinaigrette", "complement", "classic", "main", "Game bird and volcanic Beaujolais — Morgon's iron mineral and dark cherry depth bridges the pigeon's rich, slightly gamey character; Puy lentils' earthy depth mirrors the schist mineral; truffle amplifies the wine's complexity")
    PAIR(prod_foi, "Pot-au-feu de canard with marrow bone, winter vegetables, and gros sel", "complement", "established", "main", "The great French pot-au-feu and natural Beaujolais — Morgon's cherry freshness and iron mineral cuts through the rich bone broth; duck adds gamey depth that bridges the wine's Pinot-like complexity; marrow mirrors the schist richness")

# ── RÍAS BAIXAS DO (SPAIN) ────────────────────────────────────────
print("\n=== Rías Baixas DO (Spain) ===")
r_rib = R("Rías Baixas", "Spain", "wine",
           designation_type="DO",
           designation_name="Rías Baixas DO",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Galicia's most celebrated and internationally recognized white wine DO — the Atlantic coastal rias (estuaries) of the Pontevedra province producing Albariño (minimum 100% in Salnés Valley, the most important sub-zone) of extraordinary aromatic intensity, natural acidity, and the saline-citrus freshness that makes it Spain's most food-friendly and internationally distributed white wine. Rías Baixas's unique microclimate — the Atlantic's moisture, the granitic soils, and the pergola training system (pérgola gallega) — creates the conditions for Albariño's signature combination of stone fruit, lemon-lime citrus, white blossom, and saline mineral that distinguishes it from all other white grapes.",
           key_producers="Pazo de Señorans, Do Ferreiro, Terras Gauda, Martín Códax, Fillaboa, Paco & Lola",
           historical_context="Albariño's origins are disputed but most likely Galician — the variety may have been brought by Cluny monks from the Rhine in the 12th century (a persistent local legend), or more likely evolved from ancient indigenous vines. The Rías Baixas DO was created in 1988, and within a decade Albariño had become Spain's most exported premium white wine. The variety's association with the Camino de Santiago — the pilgrimage route that ends in Santiago de Compostela, just north of the Rías Baixas — made it the spiritual wine of the greatest pilgrimage in Christianity. Pazo de Señorans's Selection de Añada (single-vintage Albariño aged 7+ years on lees) demonstrated in the 1990s that the variety could age magnificently.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding Rías Baixas vintage; Albariño from Atlantic-facing granitic soils showed extraordinary aromatic intensity and saline mineral freshness."),
    (2022, "very_good", "stable", "Classic vintage; Atlantic humidity produced wines of excellent natural acidity and the characteristic stone fruit-citrus-saline character of great Albariño."),
    (2021, "excellent", "stable", "Benchmark year; Pazo de Señorans and Do Ferreiro both produced Albariño of unusual depth and the rarely seen aging potential of top Rías Baixas."),
    (2020, "excellent", "rising", "Outstanding vintage; Albariño of extraordinary aromatic complexity; the international natural wine community's discovery of age-worthy Rías Baixas accelerated."),
    (2019, "very_good", "stable", "Solid vintage; Atlantic influence well managed; Albariño of good aromatic intensity and the characteristic Rías Baixas combination of stone fruit and saline Atlantic mineral."),
]:
    VIN(r_rib, yr, qd, pt, sn)

p_sen = P("Pazo de Señorans", "Spain", r_rib,
           description="The Rías Baixas estate that demonstrated Albariño's aging potential — Marisol Bueno's Salnés Valley pazo produces the benchmark dry Albariño and the extraordinary Selección de Añada (single vintage aged 7+ years on lees), which has fundamentally changed international understanding of what Albariño can achieve with time. The estate's granitic terraced vineyards above the Ría de Arousa are considered the finest in the DO.")
prod_sen, new = PROD("Pazo de Señorans Albariño Rías Baixas", "wine_still", p_sen, r_rib, "Spain",
                     subcategory="Albariño",
                     description="The benchmark dry Albariño from the Salnés Valley's granitic soils — white peach, apricot, citrus blossom, lime, saline mineral, and the fresh Atlantic acidity that makes Rías Baixas Albariño the definitive Spanish seafood wine. Elegant structure, remarkable freshness, and the complexity that develops over 3-5 years in bottle. Spain's most consistently excellent Atlantic white wine.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sen, "Pulpo á feira (Galician-style boiled octopus with paprika, olive oil, and sea salt)", "complement", "classic", "main", "Galicia's most iconic dish and its most celebrated wine — Albariño's saline mineral and citrus character mirrors the octopus's oceanic depth; smoked paprika bridges the wine's stone fruit; sea salt amplifies the Atlantic mineral")
    PAIR(prod_sen, "Empanada gallega de atún (Galician tuna and tomato pastry pie)", "complement", "classic", "main", "Galicia's most beloved baked preparation and its Albariño — the wine's stone fruit and saline freshness cuts through the pastry richness; tuna's umami bridges the wine's mineral character; tomato's acidity mirrors the wine's citrus freshness")

p_fer = P("Do Ferreiro", "Spain", r_rib,
           description="Gerardo Méndez's 500-year-old Rías Baixas estate producing wines from the oldest ungrafted Albariño vines in the DO — some over 200 years old on their own Galician granite rootstocks. The old-vine Cepas Vellas from pre-phylloxera roots is considered Spain's most complex Albariño, developing extraordinary mineral depth and lemon-oil character over 10+ years.")
prod_fer, new = PROD("Do Ferreiro Cepas Vellas Albariño Rías Baixas", "wine_still", p_fer, r_rib, "Spain",
                     subcategory="Albariño",
                     description="Spain's most complex and age-worthy Albariño — pre-phylloxera old-vine Albariño from 200-year-old ungrafted vines on Galician granite, the oldest in Rías Baixas. Extraordinary mineral density: lemon oil, white peach, quince, granitic mineral, saline Atlantic depth, and a structure that develops over 8-10 years into something approaching white Burgundy complexity. A unique window into Albariño's authentic terroir potential.",
                     price_tier="premium")
if new:
    PAIR(prod_fer, "Vieiras de Santiago (scallops) with Galician cured ham, leek cream, and breadcrumbs", "complement", "classic", "main", "Galicia's iconic scallop pilgrim dish and its finest old-vine Albariño — the wine's lemon oil and granitic mineral bridges the scallop's sweet richness; cured ham adds savoury depth that mirrors the wine's complexity")
    PAIR(prod_fer, "Rodaballo a la gallega (turbot) with olive oil, paprika, and lemon on sliced potatoes", "complement", "classic", "main", "Galicia's most prized flatfish and its most age-worthy Albariño — the wine's extraordinary mineral depth and lemon oil character is one of the few whites that matches turbot's firmness; paprika bridges the wine's stone fruit; potatoes absorb the wine's mineral oils")

# ── PESSAC-LÉOGNAN AOC (FRANCE) ───────────────────────────────────
print("\n=== Pessac-Léognan AOC (France) ===")
r_pes = R("Pessac-Léognan", "France", "wine",
           designation_type="AOC",
           designation_name="Pessac-Léognan AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Bordeaux's most historically distinguished left bank appellation — the Graves sub-zone immediately south of the city of Bordeaux, producing both Cabernet Sauvignon-dominant reds and Sauvignon Blanc-Sémillon whites of extraordinary complexity and longevity. Château Haut-Brion is the only wine from outside the Médoc classified in the 1855 Bordeaux Classification, a testament to the appellation's historic pre-eminence. The warm gravel soils drain quickly, creating stress conditions that concentrate flavour in both red and white varieties. The thirteen classified growths include three of Bordeaux's most famous châteaux: Haut-Brion, La Mission Haut-Brion, and Pape Clément.",
           key_producers="Château Haut-Brion, Château La Mission Haut-Brion, Domaine de Chevalier, Château Pape Clément, Château Smith Haut Lafitte",
           historical_context="Samuel Pepys recorded in his diary in 1663 that he drank 'a sort of French wine called Ho Bryan that hath a good and most particular taste that I never met with' — the earliest recorded tasting note for a specific Bordeaux château, and the first mention of Haut-Brion in English literature. The château's president Thomas Jefferson (who served as US Ambassador to France from 1784-1789) ordered quantities for the White House. When the 1855 Bordeaux Classification was created, Haut-Brion was the only Graves estate included alongside the Médoc growths — its historical reputation was too great to ignore.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "One of Pessac-Léognan's greatest-ever vintages; both reds and whites of extraordinary concentration, mineral depth, and longevity potential."),
    (2021, "excellent", "stable", "Classic vintage; reds of excellent structure and mineral depth; Sauvignon Blanc-Sémillon whites of extraordinary aromatic complexity."),
    (2020, "exceptional", "rising", "Legendary vintage; Haut-Brion and La Mission both produced wines of historic concentration and longevity; Pessac-Léognan whites of rare mineral depth."),
    (2019, "excellent", "stable", "Outstanding vintage; the warm gravel soils produced reds of generous fruit concentration and mineral depth; whites of exceptional freshness."),
    (2018, "excellent", "stable", "Warm vintage producing Pessac-Léognan reds of unusual concentration; whites also successful with good body and Sauvignon aromatic intensity."),
]:
    VIN(r_pes, yr, qd, pt, sn)

p_che = P("Domaine de Chevalier", "France", r_pes,
           description="Olivier Bernard's Pessac-Léognan estate — producing both the classified red and the most internationally acclaimed dry white wine in Graves: Domaine de Chevalier Blanc, a Sauvignon Blanc and Sémillon blend aged in new French oak that is considered the finest non-Haut-Brion white Graves and among the greatest dry white wines produced anywhere in France. The red is also exceptional — structured, mineral, and requiring 15+ years to reveal its complexity.")
prod_che, new = PROD("Domaine de Chevalier Blanc Pessac-Léognan", "wine_still", p_che, r_pes, "France",
                     subcategory="Sauvignon Blanc",
                     description="The finest white Graves outside Haut-Brion — Sauvignon Blanc (70%) and Sémillon (30%) from the appellation's deepest gravel soils, fermented and aged in 100% new French oak. Extraordinary complexity: lemon curd, white peach, hazelnut, toasted oak, mineral gravel depth, and a structure that develops magnificently over 15-20 years. One of France's most age-worthy dry whites; regularly blind-tasted alongside white Burgundy's finest.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_che, "Homard à l'américaine (lobster in cognac-tomato sauce) with tarragon and cream", "complement", "classic", "main", "Bordeaux blanc's greatest pairing — the wine's toasted oak and citrus character bridges the lobster's sweet richness; cognac mirrors the wine's complexity; tarragon bridges the Sauvignon's herbal character")
    PAIR(prod_che, "Sole meunière (Dover sole) with brown butter, capers, and lemon over Paris mushrooms", "complement", "classic", "main", "The classic Bordeaux blanc preparation — sole meunière's brown butter richness is one of the finest pairings for aged white Pessac-Léognan; the wine's hazelnut and citrus character mirrors the beurre noisette")

p_smi = P("Château Smith Haut Lafitte", "France", r_pes,
           description="Daniel and Florence Cathiard's prestige Pessac-Léognan estate — producing both exceptional classified red and an outstanding white Sauvignon Blanc and Sémillon blend. Smith Haut Lafitte is also famous for the Caudalie spa and wine tourism complex at the château — one of the world's most celebrated wine tourism destinations. The red is a benchmark for modern, precise Pessac-Léognan; the white is considered among the appellation's finest.")
prod_smi, new = PROD("Château Smith Haut Lafitte Rouge Pessac-Léognan", "wine_still", p_smi, r_pes, "France",
                     subcategory="Cabernet Sauvignon",
                     description="The modern face of Pessac-Léognan excellence — Cabernet Sauvignon dominated blend from deep Graves gravel, aged with precise new oak. Blackcurrant, cedar, graphite, mineral gravel, dark chocolate, and the structured elegance of great Pessac-Léognan. Requires 10-15 years to reveal its full complexity; an alternative to Médoc classified growths at slightly more accessible prices.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_smi, "Agneau de Pauillac (Pauillac lamb rack) with Bordelaise sauce and pommes Sarladaises", "complement", "classic", "main", "The Left Bank's finest lamb and Pessac-Léognan's finest Cabernet — the wine's graphite and blackcurrant character bridges the lamb's delicate fat; Bordelaise sauce reinforces the dark fruit; pommes Sarladaises' duck fat richness is matched by the wine's structure")
    PAIR(prod_smi, "Médaillon de veau aux cèpes (veal medallion with porcini cream) and truffle shavings", "complement", "classic", "main", "The Bordeaux fine dining tradition and its classified growth — veal's gentle richness allows the wine's mineral depth and complexity to shine; cèpes mirror the wine's earthy graphite; truffle amplifies the wine's complexity")

# ── TRENTINO-ALTO ADIGE DOC (ITALY) ──────────────────────────────
print("\n=== Trentino-Alto Adige DOC (Italy) ===")
r_tre = R("Trentino-Alto Adige", "Italy", "wine",
           designation_type="DOC",
           designation_name="Trentino-Alto Adige DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Italy's most dramatically Alpine wine region — the Adige and Isarco valley systems from Bolzano (Bozen) south to Trento, producing wines of extraordinary variety and quality from Germanic (Gewurztraminer, Riesling, Müller-Thurgau, Sylvaner), French (Pinot Noir, Pinot Gris, Chardonnay, Lagrein), and indigenous (Teroldego, Marzemino, Nosiola) varieties. The Alto Adige (South Tyrol/Südtirol) sub-zone has a German-speaking majority and produces Italy's finest Pinot Grigio, Gewurztraminer, and Lagrein from steep hillside vineyards. The DOC's altitude (200-1000m) creates dramatic diurnal temperature variation that preserves aromatics and natural acidity.",
           key_producers="Foradori, Elena Walch, Hofstätter, Alois Lageder, San Michele Appiano cooperative, J. Hofstätter",
           historical_context="The region changed hands between Austria and Italy in 1919 after WWI — the Alto Adige's German-speaking culture, Tyrolean architecture, and Alpine viticulture traditions create Italy's most distinctive regional wine culture. The Gewurztraminer grape takes its name from the village of Tramin (Termeno) in the Alto Adige — making this the variety's ancestral homeland. Elisabetta Foradori's revolutionary work with Teroldego — the ancient indigenous red variety of the Campo Rotaliano alluvial plain — in the 1990s and 2000s transformed this overlooked grape into an internationally celebrated expression of Alpine Italy.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Trentino-Alto Adige vintage; Alpine varieties showed extraordinary aromatic precision; Lagrein and Teroldego of excellent concentration from warm season."),
    (2021, "very_good", "stable", "Classic vintage; cool Alpine conditions produced wines of excellent natural acidity and the characteristic freshness of high-altitude Italian whites and reds."),
    (2020, "excellent", "stable", "Benchmark year; Foradori Teroldego and Elena Walch Gewurztraminer both received extraordinary international attention."),
    (2019, "excellent", "rising", "Outstanding vintage; Gewurztraminer from Termeno (Tramin) showed exceptional aromatic intensity; Pinot Grigio from Colterenzio achieved rare mineral depth."),
    (2018, "very_good", "stable", "Warm vintage producing generous, aromatic wines; Lagrein of unusual concentration; Gewurztraminer of good aromatic intensity from the variety's ancestral homeland."),
]:
    VIN(r_tre, yr, qd, pt, sn)

p_for = P("Foradori", "Italy", r_tre,
           description="Elisabetta Foradori's revolutionary Trentino estate — the biodynamic winemaker who transformed Teroldego from an obscure local red into an internationally celebrated expression of Alpine Italy. The Granato (oak-aged) and the clay-amphora Sgarzon and Morei cuvées demonstrate that Teroldego from the volcanic alluvial Campo Rotaliano is one of Italy's most distinctive and terroir-specific varieties. Foradori is considered one of Italy's most important and influential winemakers.")
prod_for, new = PROD("Foradori Granato Teroldego Vigneti delle Dolomiti", "wine_still", p_for, r_tre, "Italy",
                     subcategory="Teroldego",
                     description="The wine that revealed Teroldego's world-class potential — Elisabetta Foradori's biodynamic Teroldego from the Campo Rotaliano volcanic alluvial soils, aged in large Austrian oak. Dark cherry, blackberry, violet, white pepper, iron mineral, and an Alpine freshness that distinguishes Teroldego from all other Italian reds. Complex, structured, and age-worthy over 10+ years. One of Italy's most distinctive terroir wines.",
                     price_tier="premium")
if new:
    PAIR(prod_for, "Canederli al formaggio (Tyrolean bread dumplings) in beef broth with chives", "complement", "established", "main", "The Trentino-Alto Adige tradition and its indigenous red — Teroldego's dark cherry and Alpine freshness bridges the dumpling's satisfying richness; the broth mirrors the wine's mineral depth; chives bridge the herbal notes")
    PAIR(prod_for, "Gulasch tirolese (Tyrolean beef goulash) with bread dumplings and lingonberry jam", "complement", "classic", "main", "The Alpine tradition's most warming dish and its indigenous wine — Teroldego's dark fruit and iron mineral bridges the goulash's paprika richness; lingonberry jam mirrors the wine's dark cherry; the structure of both complements perfectly")

p_wal = P("Elena Walch", "Italy", r_tre,
           description="The Walch family's prestige Alto Adige estate — Elena Walch's Castel Ringberg and Kastelaz single-vineyard wines from the steep lakeside terraces above Caldaro (Kaltern) are considered the finest single-vineyard Alto Adige wines. The Kastelaz Gewurztraminer — from the variety's ancestral homeland of Tramin/Termeno — is widely considered Italy's definitive Gewurztraminer and one of the world's finest expressions of the variety.")
prod_wal, new = PROD("Elena Walch Kastelaz Gewurztraminer Alto Adige", "wine_still", p_wal, r_tre, "Italy",
                     subcategory="Gewurztraminer",
                     description="Gewurztraminer from its ancestral village of Tramin/Termeno — Elena Walch's Kastelaz single-vineyard from steep volcanic soils at the variety's spiritual home. Rose petal, lychee, mango, ginger, exotic spice, and the distinctive off-dry mineral precision that distinguishes Alto Adige Gewurztraminer from Alsace's richer style. More restrained and mineral; develops elegantly over 5-7 years. The Gewurztraminer that shows where the grape originates.",
                     price_tier="premium")
if new:
    PAIR(prod_wal, "Speck Alto Adige IGP (Alpine smoked ham) with Tyrolean rye bread and horseradish", "complement", "classic", "aperitif", "The South Tyrol's most celebrated product and Gewurztraminer from its ancestral home — the wine's lychee and spice bridges the speck's smoky-salty depth; horseradish mirrors the wine's ginger note; rye bread provides textural contrast")
    PAIR(prod_wal, "Burrata fresca with roasted peaches, honey, toasted pistachios, and fresh basil", "complement", "classic", "starter", "Gewurztraminer's lychee and rose character finds direct resonance in the roasted peach; burrata's cream mirrors the wine's textural richness; honey bridges the wine's natural off-dry sweetness; basil bridges the floral note")

# ── CANNONAU DI SARDEGNA DOC (ITALY) ─────────────────────────────
print("\n=== Cannonau di Sardegna DOC (Italy) ===")
r_can = R("Cannonau di Sardegna", "Italy", "wine",
           designation_type="DOC",
           designation_name="Cannonau di Sardegna DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Sardinia's most important red wine DOC and the home of what is likely the world's oldest Grenache clone — Cannonau (the Sardinian name for Grenache) may have been cultivated on the island for over 3,000 years, predating its introduction to mainland Spain and France. The variety thrives on Sardinia's granite and basalt soils in the Nuoro province and the Ogliastra — the 'blue zone' associated with extraordinary longevity among its population. Sardinian scientists attribute the islanders' longevity partly to Cannonau's extraordinary polyphenol and resveratrol content — the highest of any red wine grape. Cannonau wines range from generous and accessible to complex, age-worthy expressions from specific sub-zones.",
           key_producers="Giuseppe Gabbas, Sella & Mosca, Argiolas, Pala, Agricola Punica, Giovanni Cherchi",
           historical_context="Cannonau's genetic testing has produced one of wine's most contentious origin disputes: Sardinian scientists and authorities maintain that Sardinian Cannonau is the parent of Spanish Garnacha and French Grenache, citing 3,000-year-old pottery shards containing Cannonau wine residue found in Bronze Age nuraghi (stone towers) on the island. Spanish authorities dispute this, claiming Grenache originated in Aragón. DNA analysis remains inconclusive. What is certain is that Sardinia's Cannonau is genetically distinct from both Grenache and Garnacha, and produces wines of a character unique to the island's granite and volcanic soils.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Cannonau vintage; Grenache from Sardinian granite showed extraordinary dark fruit concentration and the polyphenol richness that defines the island's red wine tradition."),
    (2021, "very_good", "stable", "Classic vintage; Mediterranean heat was tempered by island winds; Cannonau of excellent aromatic freshness and the characteristic dark cherry-dried herb character."),
    (2020, "excellent", "stable", "Benchmark year; Gabbas and Pala both produced wines of international acclaim; the 'blue zone' Cannonau received global health media attention."),
    (2019, "excellent", "rising", "Outstanding vintage; Cannonau from the Nuoro granite achieved record depth of colour and polyphenol concentration; longevity associations intensified international interest."),
    (2018, "very_good", "stable", "Warm vintage producing generous Cannonau of good concentration; dark cherry and Mediterranean herb character well expressed; approachable from release."),
]:
    VIN(r_can, yr, qd, pt, sn)

p_gab = P("Giuseppe Gabbas", "Italy", r_can,
           description="The most critically acclaimed small-production Cannonau producer — Giuseppe Gabbas's Nuoro estate produces Dule and Lillové from the oldest Cannonau vines on the island's granite-volcanic soils. Gabbas's wines are considered the most complex and age-worthy Cannonau produced anywhere in Sardinia, demonstrating the variety's genuine terroir expression rather than simple fruity generosity.")
prod_gab, new = PROD("Giuseppe Gabbas Dule Cannonau di Sardegna", "wine_still", p_gab, r_can, "Italy",
                     subcategory="Cannonau",
                     description="The most complex small-production Cannonau — old-vine Grenache from the Nuoro granite-volcanic soils, aged in large Slavonian oak. Dark cherry, dried Mediterranean herbs, orange peel, iron mineral, tobacco, and the extraordinary polyphenol depth that makes Sardinian Cannonau unique. Structured and age-worthy; develops magnificent complexity over 8-10 years. The definitive expression of Sardinian Grenache's distinctive character.",
                     price_tier="premium")
if new:
    PAIR(prod_gab, "Porceddu (roast suckling pig) with myrtle branches, sea salt, and Sardinian flatbread", "complement", "classic", "main", "The island's most iconic feast and its most complex red — Cannonau's dark fruit and iron mineral bridges the suckling pig's rich fat; myrtle's bitter herb character mirrors the wine's Mediterranean herb notes; flatbread provides textural contrast")
    PAIR(prod_gab, "Agnello con carciofi (lamb with Sardinian artichokes, garlic, and white wine)", "complement", "classic", "main", "Sardinian lamb with the island's indigenous red — Cannonau's dark cherry and iron mineral bridges the lamb's rich fat; artichoke's bitter edge is surprisingly bridged by the wine's Mediterranean herb character; garlic transforms to sweetness")

p_sel = P("Sella & Mosca", "Italy", r_can,
           description="The most internationally distributed and historically significant Sardinian wine producer — established by two Piedmontese lawyers in 1899 on the Alghero plain, producing Cannonau Riserva, Vermentino di Gallura, Monica, and the unique Anghelu Ruju (a Cannonau fortified wine aged oxidatively for decades). Sella & Mosca is the estate that introduced Sardinian wine to the world stage.")
prod_sel, new = PROD("Sella & Mosca Cannonau di Sardegna Riserva", "wine_still", p_sel, r_can, "Italy",
                     subcategory="Cannonau",
                     description="Sardinia's most internationally recognized Cannonau — aged Grenache from the Alghero district on clay-limestone, with extended oak maturation. Dark cherry, strawberry preserve, dried herbs, tobacco, vanilla from oak, and the characteristic Sardinian warmth and generosity. Accessible from release but develops well over 5-7 years. The gateway to understanding what Cannonau di Sardegna can achieve.",
                     price_tier="mid_range")
if new:
    PAIR(prod_sel, "Malloreddus alla campidanese (Sardinian gnocchi with sausage and saffron ragu)", "complement", "classic", "main", "Sardinia's most traditional pasta and its classic red — Cannonau's dark fruit and Mediterranean herb character bridges the sausage and saffron ragu; the wine's warmth mirrors the pasta's satisfying richness")
    PAIR(prod_sel, "Pecorino Sardo stagionato 12 months with wild boar salumi and Sardinian honey", "complement", "classic", "cheese", "The island's aged cheese board and its most accessible Cannonau — the wine's dark cherry and tobacco bridges pecorino's sharp tang; salumi adds savoury depth; honey mirrors the wine's ripe fruit")

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
