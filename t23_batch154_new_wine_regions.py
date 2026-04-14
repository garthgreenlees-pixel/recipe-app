#!/usr/bin/env python3
"""B154 — Saint-Émilion Grand Cru AOC, Pauillac AOC, Pessac-Léognan AOC,
   Saint-Julien AOC, Margaux AOC — Bordeaux Left Bank Deep Dive"""

import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
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
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region inserted: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
        (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Saint-Émilion Grand Cru AOC ────────────────────────────────────────────
print("=== Saint-Émilion Grand Cru AOC ===")
r1 = R("Saint-Émilion Grand Cru AOC", "France", "wine",
        designation_type="AOC", designation_name="Saint-Émilion Grand Cru",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The Right Bank's most extensive and diverse appellation, Saint-Émilion "
            "Grand Cru covers the hilltop town and surrounding plateau. Merlot and "
            "Cabernet Franc dominate on limestone and clay soils, producing wines of "
            "extraordinary variety from approachable early-drinkers to wines of "
            "Olympian stature. The Premier Grand Cru Classé A tier includes Pétrus's "
            "rival Cheval Blanc and Ausone."
        ),
        key_producers="Cheval Blanc, Ausone, Angélus, Pavie, Canon, Figeac",
        historical_context=(
            "Saint-Émilion's classification system was established in 1955 and revised "
            "every decade, creating controversy and litigation. Angélus and Pavie were "
            "elevated to Premier Grand Cru Classé A in 2012. The appellation produces "
            "some of the world's most sought-after wines despite its sprawling size."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Right Bank year; Merlot and Cab Franc both superb"),
    (2021, "very_good",  "stable",  "Elegant, fresh wines showing precision"),
    (2020, "exceptional","rising",  "Greatest Saint-Émilion vintage in a generation"),
    (2019, "excellent",  "stable",  "Opulent and generous with good structure"),
    (2018, "excellent",  "rising",  "Powerful and concentrated; long aging required"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Château Canon Saint-Émilion", "winery", r1, "France",
        production_philosophy="bordeaux_traditional",
        philosophy_description="Classic Saint-Émilion style; limestone plateau Merlot-Cabernet Franc.",
        reputation_narrative="Premier Grand Cru Classé B; one of Saint-Émilion's most reliable estates.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Château Canon Saint-Émilion Grand Cru AOC", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Premier Grand Cru Classé B; elegant limestone-driven Merlot-Cabernet Franc.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "roast lamb with rosemary and garlic", "complement", "classic", "main",
         "classic Bordeaux lamb pairing; tannin and richness balance")
    PAIR(prod1a, "beef fillet with bordelaise sauce", "complement", "classic", "main",
         "red wine sauce echoes wine character")
    PAIR(prod1a, "duck confit with lentils", "complement", "established", "main",
         "Right Bank duck and Merlot tradition")
    PAIR(prod1a, "Saint-Nectaire cheese", "complement", "established", "cheese",
         "semi-soft French cheese with structured red")

prod1b, new1b = PROD("Clos Canon Saint-Émilion Grand Cru AOC", "wine_still", p1a, r1, "France",
    subcategory="red",
    description="Second wine of Canon; same terroir with more accessible style.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "lamb shoulder with vegetables", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod1b, "mushroom and Cognac terrine", "complement", "established", "starter",
         "earthy richness bridge")
    PAIR(prod1b, "veal medallions with morel cream", "complement", "established", "main",
         "elegant veal and structured Merlot")
    PAIR(prod1b, "black truffle crostini", "bridge", "established", "amuse",
         "earthy truffle and clay mineral notes")

p1b = P("Château Figeac", "winery", r1, "France",
        production_philosophy="cabernet_dominant_right_bank",
        philosophy_description="Unusually high Cabernet Sauvignon and Franc for Right Bank; gravel soils.",
        reputation_narrative="Premier Grand Cru Classé A (2022 elevation); Saint-Émilion's most Médoc-like estate.",
        price_positioning="ultra_premium")
prod1c, new1c = PROD("Château Figeac Saint-Émilion Grand Cru AOC", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Unique right-bank Cabernet Sauvignon dominant; elegant, age-worthy, complex.",
    price_tier="ultra_premium")
if new1c:
    PAIR(prod1c, "roast rack of lamb with herb crust", "complement", "classic", "main",
         "structured Cabernet blend with lamb")
    PAIR(prod1c, "aged beef tenderloin with truffle", "complement", "classic", "main",
         "Cabernet structure and aged beef")
    PAIR(prod1c, "grouse with bread sauce", "complement", "established", "main",
         "game bird and Cabernet dominant blend")
    PAIR(prod1c, "aged Comté cheese", "complement", "established", "cheese",
         "structured tannin and aged hard cheese")

prod1d, new1d = PROD("La Grange Neuve de Figeac Saint-Émilion AOC", "wine_still", p1b, r1, "France",
    subcategory="red",
    description="Second wine of Figeac; approachable interpretation of the estate's distinctive style.",
    price_tier="premium")
if new1d:
    PAIR(prod1d, "duck breast with fig compote", "complement", "classic", "main",
         "Cabernet Franc and fig echo")
    PAIR(prod1d, "lamb chops with mint jus", "complement", "classic", "main",
         "classic Right Bank lamb pairing")
    PAIR(prod1d, "mushroom and walnut salad", "complement", "established", "starter",
         "earthy richness bridge to wine")
    PAIR(prod1d, "aged cheddar with chutney", "complement", "established", "cheese",
         "structured red and aged cheese")

# ── 2. Pauillac AOC ───────────────────────────────────────────────────────────
print("=== Pauillac AOC ===")
r2 = R("Pauillac AOC", "France", "wine",
        designation_type="AOC", designation_name="Pauillac",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Pauillac is the most prestigious commune in the Médoc, home to three of "
            "Bordeaux's five First Growth châteaux: Lafite-Rothschild, Latour, and "
            "Mouton-Rothschild. Cabernet Sauvignon dominates on deep gravel soils, "
            "producing wines of extraordinary structure, concentration, and longevity. "
            "The wines of Pauillac are synonymous with classic claret — cedary, "
            "blackcurrant-driven, and built for decades of aging."
        ),
        key_producers="Lafite-Rothschild, Latour, Mouton-Rothschild, Pichon Baron, Lynch-Bages",
        historical_context=(
            "Three First Growths — more than any other commune — define Pauillac's "
            "exceptional status in the 1855 Classification. Lynch-Bages, consistently "
            "overperforming its Fifth Growth status, coined the phrase 'the poor man's "
            "Mouton'. Pichon Comtesse de Lalande and Pichon Baron are considered "
            "Super Seconds."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb Pauillac year; structured and pure"),
    (2021, "very_good",  "stable",  "Fresh, elegant Cabernet with lovely precision"),
    (2020, "exceptional","rising",  "Greatest Pauillac in a generation; profound tannins"),
    (2019, "excellent",  "rising",  "Opulent and powerful; long aging required"),
    (2018, "excellent",  "rising",  "Dense and structured; exceptional aging potential"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Château Lynch-Bages", "winery", r2, "France",
        production_philosophy="bordeaux_traditional_modern",
        philosophy_description="Fifth Growth consistently outperforming classification; modern cellar.",
        reputation_narrative="Often called 'poor man's Mouton' — consistent quality overdeliverer.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Château Lynch-Bages Pauillac AOC", "wine_still", p2a, r2, "France",
    subcategory="red",
    description="Benchmark Pauillac; Cabernet Sauvignon dominant with cedary, blackcurrant depth.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "roast rack of lamb with jus", "complement", "classic", "main",
         "classic Pauillac Cabernet and lamb")
    PAIR(prod2a, "aged beef rib with bone marrow and béarnaise", "complement", "classic", "main",
         "Cabernet structure and rich beef")
    PAIR(prod2a, "pheasant with mushroom and chestnut", "complement", "established", "main",
         "game bird and structured Cabernet")
    PAIR(prod2a, "aged Cantal cheese", "complement", "established", "cheese",
         "structured red and aged French cheese")

prod2b, new2b = PROD("Echo de Lynch-Bages Pauillac AOC", "wine_still", p2a, r2, "France",
    subcategory="red",
    description="Second wine of Lynch-Bages; genuine Pauillac character at accessible entry point.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "lamb chops with herb butter", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod2b, "beef and mushroom pie", "complement", "established", "main",
         "rich pastry and structured Cabernet")
    PAIR(prod2b, "duck terrine with cornichons", "complement", "classic", "starter",
         "classic French starter")
    PAIR(prod2b, "walnut and blue cheese crostini", "complement", "suggested", "amuse",
         "Cabernet and blue cheese contrast")

p2b = P("Château Pichon Baron", "winery", r2, "France",
        production_philosophy="super_second_precision",
        philosophy_description="Second Growth precision winemaking; gravity-flow cellar, meticulous selection.",
        reputation_narrative="Consistently one of Pauillac's finest; Super Second quality at estate prices.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("Château Pichon Baron Pauillac AOC", "wine_still", p2b, r2, "France",
    subcategory="red",
    description="Super Second Pauillac; powerful and precise with extraordinary aging potential.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "venison medallions with red wine sauce", "complement", "established", "main",
         "game and structured Cabernet Sauvignon")
    PAIR(prod2c, "roast leg of lamb with Pauillac designation", "complement", "classic", "main",
         "Pauillac lamb AOC and Pauillac wine — regional harmony")
    PAIR(prod2c, "aged Comté 24 months", "complement", "established", "cheese",
         "structured tannin and aged hard cheese")
    PAIR(prod2c, "cedar-planked salmon with herb butter", "complement", "suggested", "main",
         "cedar notes echo cedar-smoked fish")

prod2d, new2d = PROD("Les Tourelles de Longueville Pauillac AOC", "wine_still", p2b, r2, "France",
    subcategory="red",
    description="Second wine of Pichon Baron; approachable Pauillac with genuine structure.",
    price_tier="premium")
if new2d:
    PAIR(prod2d, "roast chicken with garlic and herbs", "complement", "classic", "main",
         "structured Cabernet with roast poultry")
    PAIR(prod2d, "lamb shoulder slow-braised", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod2d, "beef bourguignon", "complement", "classic", "main",
         "braised beef and structured red wine")
    PAIR(prod2d, "mushroom and herb crostini", "bridge", "established", "amuse",
         "earthy bridge to cedar and blackcurrant")

# ── 3. Pessac-Léognan AOC ─────────────────────────────────────────────────────
print("=== Pessac-Léognan AOC ===")
r3 = R("Pessac-Léognan AOC", "France", "wine",
        designation_type="AOC", designation_name="Pessac-Léognan",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The northern Graves sub-appellation surrounding the city of Bordeaux "
            "produces both the world's most celebrated dry white Bordeaux and some of "
            "its finest reds. Château Haut-Brion — Bordeaux's only First Growth outside "
            "the Médoc — anchors the appellation. Sauvignon Blanc and Sémillon create "
            "whites of extraordinary complexity and longevity; Cabernet Sauvignon and "
            "Merlot produce earthy, tobacco-laced reds of haunting character."
        ),
        key_producers="Haut-Brion, Mission Haut-Brion, Domaine de Chevalier, Smith Haut Lafitte",
        historical_context=(
            "Haut-Brion was making serious wine in the 17th century — Samuel Pepys recorded "
            "drinking 'Ho Bryen' in 1663. It is the only non-Médoc château in the 1855 "
            "Classification's First Growth tier. The appellation was created in 1987 to "
            "differentiate these northern Graves estates."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb vintage for both reds and whites"),
    (2021, "very_good",  "stable",  "Elegant, precise wines with excellent freshness"),
    (2020, "exceptional","rising",  "Greatest Pessac-Léognan in decades for reds and whites"),
    (2019, "excellent",  "stable",  "Rich and generous; outstanding whites"),
    (2018, "excellent",  "rising",  "Concentrated reds with long aging potential"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine de Chevalier", "winery", r3, "France",
        production_philosophy="bordeaux_traditional_precision",
        philosophy_description="Precise winemaking; barrel-fermented whites of extraordinary longevity.",
        reputation_narrative="Among Pessac-Léognan's finest; white is arguably the world's greatest Bordeaux blanc.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Domaine de Chevalier Pessac-Léognan Grand Cru Classé Rouge", "wine_still", p3a, r3, "France",
    subcategory="red",
    description="Classified Pessac-Léognan red; earthy, tobacco-laced Cabernet Sauvignon dominant.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "roast grouse with bread sauce and bacon lardons", "complement", "classic", "main",
         "earthy Graves and game bird — classic pairing")
    PAIR(prod3a, "lamb cutlets with rosemary and Pauillac sauce", "complement", "classic", "main",
         "classic Bordeaux lamb")
    PAIR(prod3a, "aged Ossau-Iraty sheep's cheese", "complement", "established", "cheese",
         "earthy red and aged sheep's cheese")
    PAIR(prod3a, "wild mushroom and truffle cromesquis", "bridge", "established", "amuse",
         "earthy tobacco notes and mushroom")

prod3b, new3b = PROD("Domaine de Chevalier Pessac-Léognan Grand Cru Classé Blanc", "wine_still", p3a, r3, "France",
    subcategory="white",
    description="Benchmark Bordeaux Blanc; barrel-fermented Sauvignon Blanc of extraordinary longevity.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "grilled langoustine with herb butter", "complement", "classic", "main",
         "Pessac-Léognan blanc and crustaceans — the benchmark pairing")
    PAIR(prod3b, "roast lobster with beurre blanc", "complement", "classic", "main",
         "classic white Bordeaux and lobster")
    PAIR(prod3b, "veal sweetbreads with lemon and caper", "complement", "established", "main",
         "rich texture and mineral acidity")
    PAIR(prod3b, "smoked salmon and crème fraîche",  "complement", "established", "starter",
         "smoky mineral bridge")

p3b = P("Château Smith Haut Lafitte", "winery", r3, "France",
        production_philosophy="biodynamic_precision",
        philosophy_description="Biodynamic viticulture; gravity-flow cellar, sauna-style barrel chai.",
        reputation_narrative="Consistently outstanding Pessac-Léognan; spa/hotel adds to estate prestige.",
        price_positioning="ultra_premium")
prod3c, new3c = PROD("Château Smith Haut Lafitte Pessac-Léognan Rouge", "wine_still", p3b, r3, "France",
    subcategory="red",
    description="Biodynamic Pessac-Léognan red; earthy, structured, with excellent aging potential.",
    price_tier="ultra_premium")
if new3c:
    PAIR(prod3c, "rack of lamb with garlic and thyme", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod3c, "roast wood pigeon with lentil cassoulet", "complement", "established", "main",
         "earthy Graves and game bird")
    PAIR(prod3c, "aged Mimolette cheese", "complement", "established", "cheese",
         "structured red and aged French cheese")
    PAIR(prod3c, "mushroom and foie gras terrine", "complement", "established", "starter",
         "earthy richness bridge")

prod3d, new3d = PROD("Château Smith Haut Lafitte Pessac-Léognan Blanc", "wine_still", p3b, r3, "France",
    subcategory="white",
    description="Excellent biodynamic Pessac-Léognan blanc; mineral, textured, age-worthy.",
    price_tier="ultra_premium")
if new3d:
    PAIR(prod3d, "grilled turbot with lemon butter", "complement", "classic", "main",
         "minerality and cream echoes flatfish")
    PAIR(prod3d, "lobster bisque with cream and cognac", "complement", "established", "main",
         "rich texture and mineral acidity")
    PAIR(prod3d, "asparagus with hollandaise", "complement", "classic", "starter",
         "classic white Bordeaux and asparagus")
    PAIR(prod3d, "smoked cod roe on toasted brioche", "complement", "established", "amuse",
         "mineral and smoke bridge")

# ── 4. Saint-Julien AOC ───────────────────────────────────────────────────────
print("=== Saint-Julien AOC ===")
r4 = R("Saint-Julien AOC", "France", "wine",
        designation_type="AOC", designation_name="Saint-Julien",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Often considered Bordeaux's most consistently reliable commune, Saint-Julien "
            "has no First Growths but five Second Growths and some of Bordeaux's most "
            "consistent overperformers. Its wines balance power and elegance, combining "
            "Pauillac's structure with Margaux's perfume. Léoville-Las Cases and Ducru-"
            "Beaucaillou are widely considered 'Super Seconds' rivaling First Growths."
        ),
        key_producers="Léoville-Las Cases, Ducru-Beaucaillou, Léoville-Barton, Branaire-Ducru",
        historical_context=(
            "Saint-Julien was divided from the original Léoville estate — one of "
            "Bordeaux's largest — in the early 19th century. The resulting three Léoville "
            "châteaux (Las Cases, Barton, Poyferré) dominate the north of the appellation. "
            "Ducru-Beaucaillou — 'beautiful pebbles' — takes its name from its distinctive "
            "gravel terroir on the Gironde riverside."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Saint-Julien year; perfect balance"),
    (2021, "very_good",  "stable",  "Fresh and precise; beautiful early-drinking pleasure"),
    (2020, "exceptional","rising",  "Greatest Saint-Julien in decades"),
    (2019, "excellent",  "stable",  "Opulent and generous; excellent aging"),
    (2018, "excellent",  "rising",  "Structured and powerful; long-term wine"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Château Léoville-Barton", "winery", r4, "France",
        production_philosophy="traditional_no_second_wine",
        philosophy_description="Classic Saint-Julien; low prices relative to quality; no second wine philosophy.",
        reputation_narrative="Super Second quality at accessible prices; one of Bordeaux's great overperformers.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Château Léoville-Barton Saint-Julien AOC", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Classic Saint-Julien; structured Cabernet Sauvignon with remarkable value for quality.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "roast lamb with rosemary and garlic jus", "complement", "classic", "main",
         "classic Médoc Cabernet and lamb")
    PAIR(prod4a, "grouse and bread sauce", "complement", "established", "main",
         "game bird and classic claret")
    PAIR(prod4a, "aged cheddar and piccalilli", "complement", "established", "cheese",
         "British estate wine and aged cheddar — historical Barton connection")
    PAIR(prod4a, "beef Wellington with mushroom duxelle", "complement", "classic", "main",
         "structured Cabernet and pastry-wrapped beef")

prod4b, new4b = PROD("La Réserve de Léoville-Barton Saint-Julien AOC", "wine_still", p4a, r4, "France",
    subcategory="red",
    description="Second selection from Léoville-Barton; classic Saint-Julien character, earlier drinking.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "lamb chops with mint and peas", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod4b, "duck confit with Puy lentils", "complement", "established", "main",
         "classic bistro Bordeaux pairing")
    PAIR(prod4b, "mushroom tartine with herbs", "complement", "established", "starter",
         "earthy bridge to cedar notes")
    PAIR(prod4b, "Brillat-Savarin cheese", "complement", "suggested", "cheese",
         "rich cheese and structured Cabernet")

p4b = P("Château Branaire-Ducru", "winery", r4, "France",
        production_philosophy="bordeaux_modern_precision",
        philosophy_description="Fourth Growth; modern cellar with precision extraction and aging.",
        reputation_narrative="Consistently reliable Fourth Growth; fragrant, elegant Saint-Julien style.",
        price_positioning="premium")
prod4c, new4c = PROD("Château Branaire-Ducru Saint-Julien AOC", "wine_still", p4b, r4, "France",
    subcategory="red",
    description="Fourth Growth Saint-Julien; fragrant, elegant style with cedary Cabernet character.",
    price_tier="premium")
if new4c:
    PAIR(prod4c, "rack of lamb with herbs", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod4c, "pheasant with chestnuts and cream", "complement", "established", "main",
         "game bird and Médoc Cabernet")
    PAIR(prod4c, "roast duck with orange sauce", "complement", "established", "main",
         "Right Bank-style pairing with fragrant red")
    PAIR(prod4c, "aged Gouda and walnut", "complement", "established", "cheese",
         "structured tannin and aged Dutch cheese")

prod4d, new4d = PROD("Duluc de Branaire-Ducru Saint-Julien AOC", "wine_still", p4b, r4, "France",
    subcategory="red",
    description="Second wine of Branaire-Ducru; approachable, fragrant Saint-Julien character.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "grilled lamb cutlets with fines herbes", "complement", "classic", "main",
         "classic Médoc lamb pairing")
    PAIR(prod4d, "chicken liver parfait with toast", "complement", "established", "starter",
         "richness and tannin in balance")
    PAIR(prod4d, "boeuf bourguignon", "complement", "classic", "main",
         "braised beef and Cabernet classic")
    PAIR(prod4d, "camembert with chutney", "complement", "established", "cheese",
         "soft cheese and structured red")

# ── 5. Margaux AOC ────────────────────────────────────────────────────────────
print("=== Margaux AOC ===")
r5 = R("Margaux AOC", "France", "wine",
        designation_type="AOC", designation_name="Margaux",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The southernmost and most aromatic of the great Médoc communes, Margaux "
            "produces Bordeaux's most perfumed and feminine reds. Château Margaux leads "
            "the appellation with wines of extraordinary floral complexity. The distinctive "
            "thin, sandy gravel soils drain perfectly and produce wines of remarkable "
            "delicacy and longevity. Cabernet Sauvignon dominates but yields here are "
            "naturally low due to poor soils."
        ),
        key_producers="Château Margaux, Palmer, Brane-Cantenac, Rauzan-Ségla, Lascombes",
        historical_context=(
            "Château Margaux's status as a First Growth dates to 1855. The estate fell "
            "into decline in the 1960s-70s before André Mentzelopoulos purchased it in "
            "1977, initiating a complete renaissance. Palmer — a Third Growth — is "
            "considered by many critics to equal or exceed First Growth quality."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Margaux year; perfume and elegance"),
    (2021, "very_good",  "stable",  "Delicate, fragrant wines showing Margaux character"),
    (2020, "exceptional","rising",  "Greatest Margaux vintage in a generation; profound"),
    (2019, "excellent",  "stable",  "Fragrant and generous; excellent across the appellation"),
    (2018, "excellent",  "rising",  "Structured and age-worthy; needs time"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Château Palmer", "winery", r5, "France",
        production_philosophy="biodynamic_traditional",
        philosophy_description="Biodynamic viticulture; traditional winemaking elevating Third Growth to First status.",
        reputation_narrative="Third Growth that consistently rivals First Growths; Alter Ego is benchmark second wine.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Château Palmer Margaux AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Third Growth quality matching First Growths; biodynamic, fragrant, extraordinary.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "roast lamb rack with violet jus", "complement", "classic", "main",
         "Margaux perfume and fragrant lamb preparation")
    PAIR(prod5a, "roast pigeon with cherry and shallot", "complement", "established", "main",
         "delicate game bird and elegant Margaux")
    PAIR(prod5a, "aged Comté with rose petal honey", "complement", "established", "cheese",
         "floral wine and aged French cheese")
    PAIR(prod5a, "duck breast with lavender sauce", "complement", "suggested", "main",
         "floral herbal bridge to Margaux perfume")

prod5b, new5b = PROD("Alter Ego de Palmer Margaux AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Second wine of Palmer; genuine Margaux character with more approachable style.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "lamb chops with herbs and violet mustard", "complement", "classic", "main",
         "Margaux fragrance and herb-crusted lamb")
    PAIR(prod5b, "duck terrine with dried fruits", "complement", "established", "starter",
         "rich pâté and fragrant red wine")
    PAIR(prod5b, "brie with truffle and honey", "complement", "established", "cheese",
         "fragrant wine and truffle-brie")
    PAIR(prod5b, "rose petal and raspberry macaron", "bridge", "suggested", "pre_dessert",
         "floral rose bridge to Margaux perfume")

p5b = P("Château Rauzan-Ségla", "winery", r5, "France",
        production_philosophy="bordeaux_precision_modern",
        philosophy_description="Second Growth; Chanel-owned since 1994; precision viticulture and winemaking.",
        reputation_narrative="Consistently one of Margaux's finest; Ségla second wine offers estate access.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Château Rauzan-Ségla Margaux AOC", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Second Growth Margaux; aromatic, structured, age-worthy with fine-grained tannin.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "roast saddle of lamb with truffle and jus", "complement", "classic", "main",
         "classic Margaux lamb pairing with truffle")
    PAIR(prod5c, "roast woodcock on toast", "complement", "established", "main",
         "French game bird and elegant claret")
    PAIR(prod5c, "Brillat-Savarin truffle cheese", "complement", "established", "cheese",
         "floral wine and truffle-studded cheese")
    PAIR(prod5c, "foie gras with Sauternes gelée", "contrast", "established", "starter",
         "fragrant red with contrast to sweet gelée")

prod5d, new5d = PROD("Ségla Margaux AOC", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Second wine of Rauzan-Ségla; approachable Margaux with genuine estate character.",
    price_tier="premium")
if new5d:
    PAIR(prod5d, "lamb chops with rosemary and garlic", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod5d, "chicken breast with mushroom cream sauce", "complement", "established", "main",
         "elegant red with poultry")
    PAIR(prod5d, "aged Époisses cheese", "complement", "suggested", "cheese",
         "fragrant wine and pungent washed-rind cheese")
    PAIR(prod5d, "mushroom velouté with truffle oil", "bridge", "established", "starter",
         "earthy bridge to cedar notes")

# ── Final counts ──────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")
print("B154 complete.")
cur.close()
conn.close()
