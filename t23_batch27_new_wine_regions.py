#!/usr/bin/env python3
"""T23 Batch 27 — New wine regions: Moulin-à-Vent AOC (France), Saint-Émilion AOC (France), Abruzzo DOC (Italy), Rueda DO (Spain), Taurasi DOCG (Italy)"""

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

# ── MOULIN-À-VENT AOC (FRANCE) ────────────────────────────────────
print("\n=== Moulin-à-Vent AOC (France) ===")
r_mav = R("Moulin-à-Vent", "France", "wine",
           designation_type="AOC",
           designation_name="Moulin-à-Vent AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="The most structured, powerful, and age-worthy of the ten Beaujolais crus — the manganese-rich granite hillsides around the historic windmill (moulin-à-vent) on the Saône-et-Loire/Rhône border producing Gamay of extraordinary concentration and tannic structure. At its best, Moulin-à-Vent develops over 10-15 years into a wine that resembles aged Pinot Noir from the Côte d'Or — an observation made repeatedly by tasters who have confused it with Burgundy in blind tastings. The unique manganese content in the granitic soils is believed to be responsible for the variety's unusual weight and structure in this specific cru.",
           key_producers="Château du Moulin-à-Vent, Domaine des Terres Dorées (Jean-Paul Brun), Domaine de la Bruyère, Jacques Depagneux",
           historical_context="The actual windmill that gives the cru its name — the Moulin de Tremblay — dates from the 15th century and stands without its sails on the hill above the vineyards, visible from the TGV line and the Route Nationale 6. Alexandre Dumas père called Moulin-à-Vent 'the king of Beaujolais' in his Grand Dictionnaire de Cuisine in 1873, establishing its reputation as the region's most prestigious and serious wine. The appellation was the first Beaujolais cru to be delimited (1936), and has historically commanded the highest prices of all ten Beaujolais crus.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "Greatest Moulin-à-Vent vintage of the modern era; Gamay from manganese-rich granite showed legendary concentration and the tannic structure of wines destined for 15+ year development."),
    (2021, "very_good", "stable", "Classic vintage; cool conditions produced wines of excellent mineral freshness and the characteristic Moulin-à-Vent combination of power and elegance."),
    (2020, "excellent", "stable", "Benchmark year; Château du Moulin-à-Vent Clos du Grand Carquelin and Jean-Paul Brun both produced wines of historic depth."),
    (2019, "excellent", "rising", "Outstanding vintage; Gamay of extraordinary tannic structure and 20-year aging potential; Moulin-à-Vent's reputation as the most serious Beaujolais cru confirmed internationally."),
    (2018, "very_good", "stable", "Warm vintage producing generous Moulin-à-Vent of good concentration; manganese granite soils retained structure even in warm year; approachable with 5 years."),
]:
    VIN(r_mav, yr, qd, pt, sn)

p_mav = P("Château du Moulin-à-Vent", "France", r_mav,
           description="The most celebrated and historically important Moulin-à-Vent estate — adjacent to the actual windmill that gives the cru its name. The Château's range of single-parcel wines — Rochegrès, Champ de Cour, La Rochelle — are considered the definitive expressions of Moulin-à-Vent's different soil types, from the most structured manganese granite to the lighter sandy granites. The Château du Moulin-à-Vent Rochegrès is the benchmark for age-worthy Beaujolais.")
prod_mav, new = PROD("Château du Moulin-à-Vent Rochegrès", "wine_still", p_mav, r_mav, "France",
                     subcategory="Gamay",
                     description="The benchmark for Moulin-à-Vent's exceptional aging potential — Gamay from the Rochegrès parcel's deepest manganese-rich granite soils, aged in small oak barrels. Dark cherry, blackberry, iron mineral, crushed granite, violet, and a tannic structure that demands patience but rewards magnificently over 10-15 years. At its peak resembles aged Vosne-Romanée — the most Burgundian expression of Beaujolais.",
                     price_tier="premium")
if new:
    PAIR(prod_mav, "Perdreaux rôtis (roasted partridge) with lardons, chestnuts, and game jus", "complement", "classic", "main", "Moulin-à-Vent's power and structure is built for game — partridge's delicate but gamey character is bridged by the wine's dark cherry and iron mineral; chestnuts mirror the manganese mineral depth; game jus amplifies the wine's dark fruit")
    PAIR(prod_mav, "Côte de veau aux cèpes (veal chop with porcini) and green peppercorn sauce", "complement", "classic", "main", "The most versatile application of Moulin-à-Vent — veal's gentle richness allows the wine's mineral complexity to lead; cèpes echo the granite-earth depth; green pepper bridges the wine's iron mineral")

p_bru2 = P("Domaine des Terres Dorées", "France", r_mav,
            description="Jean-Paul Brun's Villefrancher-sur-Saône estate — the most intellectually rigorous and critically acclaimed natural Beaujolais producer. Brun's commitment to zero sulphur, no chaptalization, and minimal intervention across his various crus (Moulin-à-Vent, Fleurie, Morgon, Brouilly) has made Terres Dorées the natural wine world's definitive address for serious Beaujolais. His Moulin-à-Vent Cuvée Anniversaire from very old vines is considered a rival to Château du Moulin-à-Vent for the appellation's finest wine.")
prod_bru2, new = PROD("Domaine des Terres Dorées Moulin-à-Vent", "wine_still", p_bru2, r_mav, "France",
                      subcategory="Gamay",
                      description="Jean-Paul Brun's natural Moulin-à-Vent from the manganese granite hillsides — zero sulphur, no chaptalization, Gamay treated with Burgundian seriousness. Dark cherry, iron, granite mineral, dried violet, and the structured tannin that makes Moulin-à-Vent the most age-worthy and serious of all the Beaujolais crus. The natural wine movement's benchmark for the appellation.",
                      price_tier="mid_range")
if new:
    PAIR(prod_bru2, "Jambon braisé au Moulin-à-Vent (ham braised in Moulin-à-Vent wine) with parsley", "complement", "classic", "main", "The wine appears in the preparation itself — Moulin-à-Vent's structure and dark fruit infuses the braised ham; parsley bridges the wine's herbal character; the circular Beaujolais-ham pairing at its most refined")
    PAIR(prod_bru2, "Gratin de queues d'écrevisses (freshwater crayfish gratin) with cream and Comté", "complement", "established", "main", "A surprising but classic Lyonnais pairing — Moulin-à-Vent's structured Gamay with rich crayfish gratin; the wine's cherry and mineral character bridges the freshwater sweetness; Comté's nuttiness bridges the granite mineral")

# ── SAINT-ÉMILION AOC (FRANCE) ────────────────────────────────────
print("\n=== Saint-Émilion AOC (France) ===")
r_sae = R("Saint-Émilion", "France", "wine",
           designation_type="AOC",
           designation_name="Saint-Émilion AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Bordeaux's most celebrated Right Bank appellation — the medieval hilltown and its surrounding limestone and clay-rich plateau producing Merlot-dominated blends with Cabernet Franc of extraordinary richness, complexity, and range. Saint-Émilion's classification system (Grand Cru Classé, Premier Grand Cru Classé B, and Premier Grand Cru Classé A — currently Cheval Blanc, Ausone, Angélus, and Figeac) is the only Bordeaux classification to be revised regularly (every 10 years). The limestone and clay soils around the town contrast with the iron-rich clay plateau of Pomerol across the valley, producing softer, more approachable wines than the Médoc's Cabernet Sauvignon-dominated chateaux.",
           key_producers="Château Cheval Blanc, Château Figeac, Château Ausone, Château Angélus, Château Troplong Mondot, Château Canon, Château Pavie",
           historical_context="Saint-Émilion's wine history stretches to the Gallo-Roman poet Ausonius (Decimus Magnus Ausonius, 310-395 AD) who owned a villa in the region — Château Ausone claims continuity from this classical estate, though historical records are imprecise. The town's medieval limestone underground network of cellars (monolithic church carved from living rock) have been used for wine storage for 1,000 years. The 1855 Bordeaux Classification excluded Saint-Émilion and the Right Bank entirely, prompting the creation of the Saint-Émilion classification in 1954 — the only one subject to regular revision and upgrade, creating a dynamic competitive system unique in Bordeaux.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "One of Saint-Émilion's greatest-ever vintages; Merlot of legendary richness and concentration; Premier Grand Cru wines of extraordinary longevity potential."),
    (2021, "excellent", "stable", "Outstanding vintage; Right Bank clay soils helped Merlot maintain freshness in warm conditions; Cabernet Franc added elegant structure."),
    (2020, "exceptional", "rising", "Legendary vintage; Cheval Blanc, Figeac, and Ausone produced wines of historic quality; Saint-Émilion's finest in a decade across all levels."),
    (2019, "excellent", "stable", "Outstanding vintage; Merlot of generous richness and freshness; limestone plateau wines particularly elegant; Premiers Grands Crus of 20+ year potential."),
    (2018, "excellent", "stable", "Warm vintage producing Saint-Émilion of unusual concentration; clay soils retained freshness; wines of good structure and dark plum richness."),
]:
    VIN(r_sae, yr, qd, pt, sn)

p_fie = P("Château Figeac", "France", r_sae,
           description="The most distinctive and intellectually interesting Premier Grand Cru Classé A — Frédéric Fourcade's estate on the gravel and sand soils adjacent to Pomerol, planted with an unusual 35% Cabernet Sauvignon and 35% Cabernet Franc alongside 30% Merlot. Figeac's Cabernet-dominant blend sets it apart from all other Saint-Émilion estates, producing wines of an elegance and finesse that some critics compare to Pomerol's Pétrus in style. Elevated to Premier Grand Cru Classé A in the 2022 classification revision.")
prod_fie, new = PROD("Château Figeac Saint-Émilion Premier Grand Cru Classé A", "wine_still", p_fie, r_sae, "France",
                     subcategory="Cabernet Franc blend",
                     description="Saint-Émilion's most unique Grand Cru Classé A — the Cabernet-dominated blend from gravel soils adjacent to Pomerol. Black cherry, graphite, violet, cedar, truffle, and the extraordinary elegance that distinguishes Figeac from all other Saint-Émilion estates. More Médoc in structure, more Pomerol in richness; a wine of 30+ year aging potential that consistently rewards patience. Recently elevated to the appellation's highest tier.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_fie, "Lamproie à la bordelaise (lamprey in red wine sauce) with leeks and croutons", "complement", "classic", "main", "The Right Bank's most historic preparation — lamprey braised in Bordeaux wine; Figeac's graphite and cherry character bridges the lamprey's extraordinary richness; leeks provide a savoury bridge; the wine's elegance matches the dish's refinement")
    PAIR(prod_fie, "Tournedos Rossini (beef tenderloin with foie gras and black truffle) on brioche", "complement", "classic", "main", "The great Bordeaux fine dining tradition and Saint-Émilion's most elegant Grand Cru Classé A — truffle directly bridges the wine's earthy graphite; foie gras's richness meets the wine's plush Merlot; tenderloin's precision allows the wine's complexity to shine")

p_tro = P("Château Troplong Mondot", "France", r_sae,
           description="One of Saint-Émilion's most celebrated and recently risen Premier Grand Cru Classé B estates — Christine Valette's plateau estate at the highest point of the Saint-Émilion limestone plateau produces wines of extraordinary concentration and richness from old-vine Merlot on limestone and clay. The wine's combination of power, density, and the limestone mineral character of the plateau has made it one of the appellation's most sought-after wines among right bank collectors.")
prod_tro, new = PROD("Château Troplong Mondot Saint-Émilion Premier Grand Cru Classé", "wine_still", p_tro, r_sae, "France",
                     subcategory="Merlot",
                     description="Saint-Émilion's most powerful and concentrated Premier Grand Cru Classé B — Merlot from the highest-elevation limestone plateau at maximum concentration. Dark plum, blackberry, dark chocolate, cedar, limestone mineral, mocha, and a tannic structure that demands 10-15 years to reveal its full potential. One of the right bank's most consistently impressive and collectible wines — the plateau's character expressed at maximum density.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_tro, "Entrecôte à la bordelaise with bone marrow, shallot confit, and Périgueux truffle sauce", "complement", "classic", "main", "The Bordeaux classic preparation and Saint-Émilion's most powerful wine — the wine's density and dark plum matches the ribeye's rich fat; bone marrow bridges the Merlot's velvety texture; truffle amplifies the wine's limestone mineral")
    PAIR(prod_tro, "Canard à la presse (pressed duck) with blood sauce and pommes dauphine", "complement", "classic", "main", "Tour d'Argent's legendary preparation and a powerful Saint-Émilion — the wine's concentration and dark chocolate meets the duck blood sauce's intensity; the wine's limestone mineral bridges the richness of this extreme preparation")

# ── ABRUZZO DOC (ITALY) ───────────────────────────────────────────
print("\n=== Abruzzo DOC (Italy) ===")
r_abr = R("Abruzzo", "Italy", "wine",
           designation_type="DOC",
           designation_name="Abruzzo DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Central Italy's most dramatically contrasting wine region — the Apennine mountains descending to the Adriatic coast in Abruzzo producing both the structured Montepulciano d'Abruzzo DOC (a powerful, age-worthy red from one of Italy's most underappreciated varieties) and Trebbiano d'Abruzzo DOC (a white wine that in the hands of Valentini produces one of Italy's most distinctive and age-worthy whites from an unlikely variety). Abruzzo's diverse altitude range — from sea-level Adriatic vineyards to 700m+ mountain parcels — creates wines of dramatic contrast. The Colline Teramane sub-zone for Montepulciano and the high-altitude Pecorino variety are also achieving international recognition.",
           key_producers="Valentini, Emidio Pepe, Masciarelli, Montori, La Valentina, Illuminati",
           historical_context="Edoardo Valentini's Abruzzo estate — run with aristocratic obstinacy and genius from Loreto Aprutino — is considered by some critics to produce the world's greatest Trebbiano d'Abruzzo; wines that age for 30+ years into something resembling Burgundian Chardonnay, despite being made from the supposedly undistinguished Trebbiano grape. Valentini released only exceptional vintages, rejected modern winemaking technology entirely, and refused all interviews — creating a legendary mystique around wines that are among Italy's most sought-after. His Montepulciano d'Abruzzo is equally exceptional. The estate now managed by his son Francesco continues the tradition.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Abruzzo vintage; Montepulciano showed extraordinary dark fruit concentration; Trebbiano d'Abruzzo (in Valentini's hands) of rare aromatic complexity."),
    (2021, "very_good", "stable", "Classic vintage; Apennine altitude preserved freshness in hot Italian summer; Montepulciano of excellent structure and dark cherry depth."),
    (2020, "excellent", "stable", "Benchmark year; Valentini Trebbiano received extraordinary critical attention; Emidio Pepe Montepulciano confirmed as Italy's most distinctive Adriatic red."),
    (2019, "excellent", "rising", "Outstanding vintage; Montepulciano d'Abruzzo of historic concentration and longevity; Colline Teramane wines of exceptional structure."),
    (2018, "very_good", "stable", "Warm vintage producing generous Abruzzo; Montepulciano of good concentration and dark fruit richness; Pecorino white wines of excellent aromatic intensity."),
]:
    VIN(r_abr, yr, qd, pt, sn)

p_val = P("Valentini", "Italy", r_abr,
           description="Edoardo Valentini's legendary Abruzzo estate — managed with aristocratic genius and obstinacy from Loreto Aprutino. Valentini Trebbiano d'Abruzzo is considered by Jancis Robinson and Hugh Johnson to be among the world's most extraordinary white wines — ageable for 30+ years, made from a variety dismissed everywhere else as ordinary. The Montepulciano d'Abruzzo is equally exceptional. Valentini released only selected parcels from only excellent vintages, creating demand far exceeding supply. Now managed by son Francesco with identical philosophy.")
prod_val, new = PROD("Valentini Trebbiano d'Abruzzo", "wine_still", p_val, r_abr, "Italy",
                     subcategory="Trebbiano d'Abruzzo",
                     description="The wine that proved Trebbiano's potential for greatness — Edoardo Valentini's Trebbiano from the highest Abruzzo Apennine parcels, selected only in exceptional vintages, aged 4+ years before release. Extraordinary complexity: beeswax, white peach, hazelnut, toasted almond, mineral depth, and a development over 20-30 years that confounds those who dismiss Trebbiano. One of Italy's most legendary and sought-after white wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_val, "Chitarra all'abruzzese (Abruzzo guitar-cut pasta) with lamb ragu and pecorino", "complement", "classic", "main", "Abruzzo's most distinctive pasta shape with the region's most distinctive white — Valentini Trebbiano's complex, oxidative richness is unusual for a white wine but matches the depth of Abruzzo lamb ragu; pecorino's saltiness bridges the wine's mineral depth")
    PAIR(prod_val, "Baccalà mantecato (salt cod whipped with olive oil) on grilled polenta with herbs", "complement", "classic", "starter", "The Adriatic salted fish tradition and Abruzzo's extraordinary white — Valentini Trebbiano's beeswax and mineral depth is one of the few whites capable of matching salt cod's intensity; polenta's neutral richness allows the wine's complexity to shine")

p_pep = P("Emidio Pepe", "Italy", r_abr,
           description="The Pepe family's Torano Nuovo estate — producing Montepulciano d'Abruzzo and Trebbiano d'Abruzzo with an obsessive rejection of all modern winemaking technology. Wines are fermented in concrete, bottled without filtration, and aged for decades before release — Emidio Pepe Montepulciano from the 1980s is still available for purchase from the family. The wines are polarizing (volatile acidity is high by conventional standards) but for devotees represent some of Italy's most authentic and age-worthy expressions.")
prod_pep, new = PROD("Emidio Pepe Montepulciano d'Abruzzo", "wine_still", p_pep, r_abr, "Italy",
                     subcategory="Montepulciano",
                     description="Italy's most controversial and cult Montepulciano — unfined, unfiltered, concrete-aged, released only after years of development. Dark plum, dried cherry, leather, tar, iron, and a wild, volatile character that divides critics but enchants devotees. At 10-20 years it develops into something of extraordinary depth and individuality. The ultimate expression of artisan Abruzzo winemaking without compromise.",
                     price_tier="premium")
if new:
    PAIR(prod_pep, "Arrosticini (Abruzzo lamb skewers) with Pecorino di Farindola and flatbread", "complement", "classic", "main", "Abruzzo's most beloved street food and its most artisanal red — the wine's dark cherry and iron mineral bridges the lamb's charred fat; Pecorino di Farindola (made with pig's rennet) is one of Italy's rarest cheeses and bridges the wine's wild character")
    PAIR(prod_pep, "Agnello alla 'ndocca 'ndocca (slow-stewed lamb offal with chilli, rosemary, and vinegar)", "complement", "classic", "main", "Abruzzo's most ancient peasant preparation and its most peasant wine — Emidio Pepe's wild, natural character is one of the few wines that stands up to this assertive offal stew; vinegar's acidity bridges the wine's volatile character")

# ── RUEDA DO (SPAIN) ──────────────────────────────────────────────
print("\n=== Rueda DO (Spain) ===")
r_rue = R("Rueda", "Spain", "wine",
           designation_type="DO",
           designation_name="Rueda DO",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Spain's most important white wine DO for aromatic dry whites — the high-altitude plateau (750-850m) of Valladolid, Segovia, and Ávila in Castile-León producing Verdejo (Spain's finest aromatic white variety) and Sauvignon Blanc of extraordinary freshness, mineral precision, and character. Rueda's high-altitude, continental climate creates dramatic diurnal temperature variation that preserves Verdejo's signature anise, citrus, and bitter almond character while maintaining natural acidity. The finest single-vineyard Rueda Verdejo — particularly from Belondrade's centenarian vines — demonstrates that the variety can achieve a complexity and depth rivaling the world's greatest white wines.",
           key_producers="Belondrade y Lurton, Marqués de Riscal Rueda, Bodegas Naia, Javier Sanz, Hermanos Lurton, Ossian",
           historical_context="Verdejo is an ancient Iberian variety — possibly pre-Roman — that survived the Phylloxera devastation and the Franco-era preference for anonymous bulk wine by hiding in the sandy soils of Rueda's high plateau. The DO was created in 1980, the first white wine DO in Castile-León, as part of a government initiative to revitalize Spanish white wine. Marqués de Riscal's decision to produce Rueda Verdejo (hiring Émile Peynaud of Bordeaux to consult) in 1972 established the DO's fine wine credentials. Didier Belondrade's arrival from France in the 1990s and his obsessive focus on low-yield, centenarian-vine Verdejo transformed the DO's critical reputation internationally.")

for yr, qd, pt, sn in [
    (2023, "excellent", "rising", "Outstanding Rueda vintage; Verdejo from high-altitude plateau soils showed extraordinary aromatic precision and the characteristic anise-citrus mineral character."),
    (2022, "very_good", "stable", "Classic vintage; continental conditions produced wines of excellent natural acidity and the bitter almond finish that defines great Rueda Verdejo."),
    (2021, "excellent", "stable", "Benchmark year; Belondrade and Ossian both produced single-vineyard Verdejo of international acclaim; Rueda's reputation beyond Spain solidified."),
    (2020, "excellent", "rising", "Outstanding vintage; centenarian-vine Verdejo of extraordinary depth and the rare aging potential of the finest Rueda; critical re-evaluation of the DO underway."),
    (2019, "very_good", "stable", "Solid vintage; high-altitude plateau maintained freshness in warm Spanish conditions; Verdejo of good aromatic intensity and characteristic bitter almond complexity."),
]:
    VIN(r_rue, yr, qd, pt, sn)

p_bel = P("Belondrade y Lurton", "Spain", r_rue,
           description="Didier Belondrade's Rueda estate — the French winemaker who arrived in 1994 and transformed critical perception of Verdejo with obsessive focus on centenarian-vine Rueda from the estate's sandy-limestone soils. The flagship Belondrade y Lurton Rueda (aged in French oak) is considered Spain's finest Verdejo and one of the country's most internationally celebrated white wines — rivaling the finest Rías Baixas Albariño for Spain's premier white wine status.")
prod_bel, new = PROD("Belondrade y Lurton Rueda Verdejo", "wine_still", p_bel, r_rue, "Spain",
                     subcategory="Verdejo",
                     description="Spain's benchmark premium Verdejo — centenarian-vine Verdejo from sandy-limestone Rueda soils, fermented and aged in French oak with lees stirring. Anise, citrus blossom, fennel, white peach, toasted hazelnut, bitter almond, and the complex mineral depth that develops magnificently over 5-8 years. The wine that transformed international perception of Verdejo from simple aperitif to serious white wine. Spain's most ambitious Rueda.",
                     price_tier="premium")
if new:
    PAIR(prod_bel, "Judiones de La Granja (giant white beans) with jamón ibérico and saffron", "complement", "classic", "main", "Castile's most celebrated legume dish and its finest white wine — Verdejo's citrus and bitter almond character bridges the ibérico ham's depth; saffron bridges the wine's anise notes; beans' neutral richness allows the wine's complexity to shine")
    PAIR(prod_bel, "Cochinillo asado (Segovian roast suckling pig) with crispy crackling and natural juices", "complement", "classic", "main", "The DO's neighbour Segovia's most iconic dish and Rueda's finest white — Verdejo's bitter almond and citrus is one of the few whites that complements suckling pig's richness; crackling's crunch contrasts the wine's silky texture")

p_nai = P("Bodegas Naia", "Spain", r_rue,
           description="The Nieva family's Rueda estate — producing consistently excellent Verdejo across multiple price points, with the premium Las Brisas aged in French oak from old-vine Verdejo on sandy soils. Naia Las Brisas is considered one of Rueda's finest value-for-quality propositions and has done much to build the DO's reputation internationally for serious Verdejo at accessible prices.")
prod_nai, new = PROD("Naia Las Brisas Rueda Verdejo", "wine_still", p_nai, r_rue, "Spain",
                     subcategory="Verdejo",
                     description="Rueda's benchmark for elegant, oak-aged Verdejo at an approachable price — old-vine Verdejo from sandy Rueda soils, partially aged in French oak. Green apple, fennel, citrus blossom, white peach, anise, and the distinctive bitter almond mineral finish. Fresh, precise, and with enough structure to develop over 3-5 years. The introduction to understanding what Rueda Verdejo can achieve with proper production.",
                     price_tier="mid_range")
if new:
    PAIR(prod_nai, "Boquerones en vinagre (white anchovies marinated in vinegar) with olive oil and garlic", "complement", "classic", "aperitif", "The Spanish tapas tradition and the Castilian white — Verdejo's citrus and bitter almond character mirrors the anchovy's vinegar marinade; garlic bridges the wine's herbal anise note; olive oil's richness is cut by the wine's acidity")
    PAIR(prod_nai, "Trucha a la navarra (pan-fried trout with jamón ibérico and herbs)", "complement", "classic", "main", "The Castilian river trout tradition and its regional white wine — Verdejo's citrus and mineral freshness bridges the trout's delicate flesh; jamón ibérico adds savoury depth that bridges the wine's bitter almond complexity")

# ── TAURASI DOCG (ITALY) ──────────────────────────────────────────
print("\n=== Taurasi DOCG (Italy) ===")
r_tau = R("Taurasi", "Italy", "wine",
           designation_type="DOCG",
           designation_name="Taurasi DOCG",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Campania's most important red wine DOCG and one of Italy's most underappreciated great reds — the Calore River valley in the Campanian Apennines producing 100% Aglianico of extraordinary structure, mineral depth, and longevity. Taurasi is Italy's 'Barolo of the South' — sharing Barolo's thick skins, elevated tannins, high acidity, and exceptional aging potential (the finest examples develop over 20-30 years). The volcanic, clay, and limestone soils of the Irpinia hills at 400-700m elevation create ideal conditions for Aglianico's late ripening (harvested in November, long after most Italian reds). The DOCG requires a minimum of 3 years aging (4 for Riserva).",
           key_producers="Mastroberardino, Feudi di San Gregorio, Terredora di Paolo, Caggiano, Quintodecimo, Molettieri",
           historical_context="Aglianico's name derives from the Greek 'Hellenikos' — the Hellenic variety brought by Greek colonists to Magna Graecia in the 8th century BC. The Romans called the wine from this region 'Falernum,' considered among antiquity's finest. Mastroberardino preserved the ancient Aglianico clones through the 20th century when others planted more commercial varieties, and their single-vineyard Radici (released only in exceptional years) established Taurasi's modern fine wine identity. The Irpinia region is also home to Greco di Tufo and Fiano di Avellino — the 'Holy Trinity of Campanian wine' that has attracted international investment from Feudi di San Gregorio and northern Italian producers.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Taurasi vintage; Aglianico from Campanian Apennine volcanic clay showed extraordinary dark fruit concentration and the region's characteristic iron-mineral structure."),
    (2021, "very_good", "stable", "Classic vintage; Irpinia hills' altitude preserved freshness in warm Italian conditions; Aglianico of excellent structure and dark cherry depth."),
    (2020, "excellent", "stable", "Benchmark year; Mastroberardino Radici and Feudi di San Gregorio both produced wines of historic quality; Taurasi's 'Barolo del Sud' reputation confirmed internationally."),
    (2019, "exceptional", "rising", "Greatest Taurasi vintage of the modern era; Aglianico of legendary iron-mineral concentration and 30-year aging potential; DOCG prices rose dramatically."),
    (2018, "very_good", "stable", "Warm vintage producing generous Taurasi of good concentration; volcanic clay soils retained structure; accessible with 5 years but rewards patience over 15."),
]:
    VIN(r_tau, yr, qd, pt, sn)

p_mas = P("Mastroberardino", "France", r_tau,  # Note: Italy
           description="The ancient Campanian dynasty that preserved Aglianico and the Irpinia wine culture through the 20th century — Antonio Mastroberardino's reconstruction of ancient Pompeii vineyard varieties for the Pompeii Winery Project alongside the estate's ongoing Taurasi production has made this the most historically significant wine family in southern Italy. The Radici Riserva (released only in exceptional years) is considered Italy's greatest Aglianico.")
prod_mas, new = PROD("Mastroberardino Radici Taurasi Riserva DOCG", "wine_still", p_mas, r_tau, "Italy",
                     subcategory="Aglianico",
                     description="Italy's most celebrated Aglianico and southern Italy's finest red wine — from the volcanic clay and limestone Irpinia hills at 500m elevation, aged 4 years before release (minimum 2 in large oak). Dark cherry, tar, iron mineral, dried violet, cedar, dark chocolate, and the extraordinary tannic structure that rewards 15-20 years of patience. At peak, one of Italy's 5 greatest wines. The 'Barolo of the South' at its most compelling.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mas, "Ragù alla genovese napoletana (Naples-style slow-cooked beef and onion pasta sauce)", "complement", "classic", "main", "Naples's most ancient pasta sauce (6+ hours of onion-beef braise) and Campania's greatest red — Taurasi's iron tannin and dark cherry is perfectly matched by the genovese's incredible depth; the wine's structure supports the sauce's extraordinary richness")
    PAIR(prod_mas, "Agnello al forno con patate (Campanian roast lamb with potatoes, olives, and herbs)", "complement", "classic", "main", "Campanian lamb and Campanian Aglianico — the wine's iron tannins and dark fruit bridges the roast lamb's richness; olives' bitterness mirrors the wine's mineral depth; Irpinia herbs bridge the wine's herbal complexity")

p_feu = P("Feudi di San Gregorio", "Italy", r_tau,
           description="The most internationally successful and commercially innovative Campanian producer — Enzo Ercolino's Irpinia estate transformed Campanian wine from local curiosity to internationally distributed fine wine category. The flagship Taurasi DOCG, Patrimo (Merlot), Serpico (Aglianico blend), and the white wine portfolio of Greco di Tufo and Fiano di Avellino have established Feudi as southern Italy's most globally recognized premium wine brand.")
prod_feu, new = PROD("Feudi di San Gregorio Taurasi DOCG", "wine_still", p_feu, r_tau, "Italy",
                     subcategory="Aglianico",
                     description="The accessible face of serious Taurasi — Feudi di San Gregorio's benchmark Aglianico from the Irpinia volcanic clay hills, aged 24+ months in oak. Dark cherry, blackberry, iron mineral, tobacco, and the structured elegance that makes Feudi's wine the best introduction to Taurasi DOCG for international collectors. More approachable than Mastroberardino's Radici but develops beautifully over 10 years.",
                     price_tier="premium")
if new:
    PAIR(prod_feu, "Maccheroni al ragu napoletano (Sunday ragu with short ribs, pork, and sausage)", "complement", "classic", "main", "The Neapolitan Sunday tradition of all-day ragu and Campania's finest red — Taurasi's iron tannin structure matches the extraordinary depth of a 4-hour ragu; the wine's dark cherry mirrors the ragu's concentrated tomato-meat fusion")
    PAIR(prod_feu, "Capretto all'ischitana (Ischia-style goat braised in white wine with herbs and tomato)", "complement", "classic", "main", "The Campanian islands' goat tradition and mainland Campania's finest red — Taurasi's iron and dark cherry bridges the goat's distinctive flavour; white wine braise mirrors the wine's acidity; tomato and herbs bridge the wine's complexity")

# Fix the country typo for Mastroberardino
cur.execute("UPDATE beverage_producers SET country='Italy' WHERE name='Mastroberardino' AND country='France'")

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
