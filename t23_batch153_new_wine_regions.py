#!/usr/bin/env python3
"""B153 — Ribera del Duero DO (Spain), Malbec regions: Mendoza supplement,
   Uco Valley DO (Argentina), Priorat DOQ (Spain), Alentejo DOC (Portugal)"""

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

# ── 1. Ribera del Duero DO ────────────────────────────────────────────────────
print("=== Ribera del Duero DO ===")
r1 = R("Ribera del Duero DO", "Spain", "wine",
        designation_type="DO", designation_name="Ribera del Duero",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Spain's most prestigious red wine appellation after Rioja, Ribera del "
            "Duero sits on a high plateau at 850-1,000m elevation along the Duero River. "
            "Tempranillo (locally called Tinto Fino) dominates, producing wines of "
            "powerful concentration, high natural acidity, and remarkable aging potential. "
            "The extreme continental climate — scorching summers, bitterly cold winters — "
            "produces grapes with intensity rarely matched in Spain."
        ),
        key_producers="Vega Sicilia, Pingus, Aalto, Pesquera, Emilio Moro",
        historical_context=(
            "Vega Sicilia was producing serious wine here in the 1860s, but Ribera del "
            "Duero only received DO status in 1982. Peter Sisseck's Pingus (1995) became "
            "one of the world's most expensive wines. The region now rivals Burgundy and "
            "Bordeaux in prestige."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Classic Ribera vintage; ideal harvest conditions"),
    (2021, "very_good",  "stable",  "Balanced season; elegant structured wines"),
    (2020, "exceptional","rising",  "Widely considered one of the greatest vintages ever"),
    (2019, "excellent",  "stable",  "Outstanding year for structured, age-worthy wines"),
    (2018, "very_good",  "stable",  "Fresh and precise; earlier drinking style"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Aalto Winery", "winery", r1, "Spain",
        production_philosophy="old_vine_terroir",
        philosophy_description="Old-vine Tinto Fino from high-altitude plots; minimal intervention.",
        reputation_narrative="Co-founded by former Vega Sicilia winemaker; Aalto PS is a benchmark.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Aalto Ribera del Duero", "wine_still", p1a, r1, "Spain",
    subcategory="red",
    description="Flagship Tinto Fino; concentrated, structured, with remarkable aging potential.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "slow-roasted suckling pig (cochinillo)", "complement", "classic", "main",
         "Castilian suckling pig and Ribera Tempranillo is a classic regional pairing")
    PAIR(prod1a, "wood-roasted lamb chops", "complement", "classic", "main",
         "Castilian lamb and structured Tinto Fino")
    PAIR(prod1a, "manchego aged 12 months", "complement", "established", "cheese",
         "tannin structure balances aged cheese")
    PAIR(prod1a, "braised oxtail with mushrooms", "complement", "established", "main",
         "earthy richness and wine concentration")

prod1b, new1b = PROD("Aalto PS Pagos Seleccionados Ribera del Duero", "wine_still", p1a, r1, "Spain",
    subcategory="red",
    description="Single-vineyard selection from oldest vines; one of Spain's most complex reds.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "dry-aged Iberico beef tenderloin", "complement", "classic", "main",
         "profound Spanish beef with profound Spanish wine")
    PAIR(prod1b, "roast rack of lamb with romesco", "complement", "classic", "main",
         "Castilian lamb elevated with premium wine")
    PAIR(prod1b, "aged Manchego with membrillo", "complement", "established", "cheese",
         "classic Spanish cheese course pairing")
    PAIR(prod1b, "black truffle and egg croqueta", "bridge", "established", "amuse",
         "earthy mineral bridge to old-vine concentration")

p1b = P("Emilio Moro Winery", "winery", r1, "Spain",
        production_philosophy="family_tradition",
        philosophy_description="Four generations of family winemaking; low yields from old vines.",
        reputation_narrative="One of Ribera del Duero's most consistent and respected family estates.",
        price_positioning="premium")
prod1c, new1c = PROD("Emilio Moro Ribera del Duero", "wine_still", p1b, r1, "Spain",
    subcategory="red",
    description="Benchmark estate Tinto Fino; dark fruit, oak, and robust Castilian character.",
    price_tier="mid_range")
if new1c:
    PAIR(prod1c, "lamb cutlets with garlic and herbs", "complement", "classic", "main",
         "Castilian lamb and Tinto Fino")
    PAIR(prod1c, "chorizo and lentil stew", "complement", "established", "main",
         "rustic richness and wine concentration")
    PAIR(prod1c, "beef and mushroom croquetas", "complement", "classic", "amuse",
         "earthy richness bridge")
    PAIR(prod1c, "grilled Iberico pork secreto", "complement", "established", "main",
         "Spanish pork and Spanish Tempranillo")

prod1d, new1d = PROD("Emilio Moro Malleolus Ribera del Duero", "wine_still", p1b, r1, "Spain",
    subcategory="red",
    description="Single-vineyard old-vine selection; intense, age-worthy, and highly acclaimed.",
    price_tier="premium")
if new1d:
    PAIR(prod1d, "roast suckling pig with jus", "complement", "classic", "main",
         "Castilian suckling pig and old-vine Tinto Fino")
    PAIR(prod1d, "aged Idiazábal cheese", "complement", "established", "cheese",
         "smoky aged cheese with structured red")
    PAIR(prod1d, "venison medallions with berry sauce", "complement", "established", "main",
         "game and concentrated Spanish red")
    PAIR(prod1d, "black pudding and quail egg pintxo", "complement", "classic", "amuse",
         "Spanish bar snack elevation")

# ── 2. Uco Valley (Valle de Uco) ──────────────────────────────────────────────
print("=== Uco Valley (Valle de Uco) ===")
r2 = R("Valle de Uco", "Argentina", "wine",
        designation_type="GI", designation_name="Valle de Uco",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description=(
            "Argentina's most exciting wine sub-region, Valle de Uco sits at 900-1,500m "
            "elevation at the foot of the Andes southwest of Mendoza. The extreme altitude, "
            "intense sunshine, and dramatic diurnal temperature variation produce wines of "
            "exceptional concentration and natural acidity. Malbec reaches new heights here, "
            "alongside Cabernet Franc, Cabernet Sauvignon, and Chardonnay. Sub-zones "
            "Tunuyán, Tupungato, and San Carlos each have distinct terroir expressions."
        ),
        key_producers="Achaval Ferrer, Zuccardi, Clos de los Siete, Clos Apalta, Catena Zapata",
        historical_context=(
            "Largely undeveloped until the 1990s, Valle de Uco attracted major investment "
            "from Catena, Michel Rolland's Clos de los Siete consortium, and international "
            "investors recognizing the terroir potential. It has since become Argentina's "
            "most acclaimed wine zone, producing Malbecs that rival the world's finest."
        ))

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising",  "Outstanding vintage; intense altitude-driven fruit"),
    (2021, "excellent",   "rising",  "Fresh, elegant wines with remarkable depth"),
    (2020, "very_good",   "stable",  "Classic Uco vintage; balanced and age-worthy"),
    (2019, "excellent",   "stable",  "Concentrated and structured; great aging potential"),
    (2018, "very_good",   "stable",  "Consistent year; excellent value"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Zuccardi Valle de Uco", "winery", r2, "Argentina",
        production_philosophy="terroir_massal_selection",
        philosophy_description="Massal selection, minimal intervention, altitude terroir expression.",
        reputation_narrative="Best Winery in the World (Decanter 2019); Valle de Uco pioneers.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Zuccardi Finca Piedra Infinita Malbec Uco Valley", "wine_still", p2a, r2, "Argentina",
    subcategory="red",
    description="Flagship single-vineyard Malbec; extraordinary altitude-driven concentration and freshness.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "dry-aged Wagyu ribeye with chimichurri", "complement", "classic", "main",
         "premium Malbec and premium beef — the quintessential pairing")
    PAIR(prod2a, "asado de costillar (slow-grilled short rib)", "complement", "classic", "main",
         "traditional Argentine asado with flagship Malbec")
    PAIR(prod2a, "dark chocolate and raspberry tart", "complement", "established", "dessert",
         "chocolate echo and berry affinity")
    PAIR(prod2a, "empanada de carne with olives", "complement", "classic", "amuse",
         "Argentine tradition elevated")

prod2b, new2b = PROD("Zuccardi Valle de Uco Malbec", "wine_still", p2a, r2, "Argentina",
    subcategory="red",
    description="Estate Malbec showing the freshness and precision of high-altitude Uco terroir.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "grilled lamb chops with herbs", "complement", "classic", "main",
         "classic Malbec and lamb pairing")
    PAIR(prod2b, "bife de chorizo (Argentine sirloin)", "complement", "classic", "main",
         "Argentine steak and Malbec — the national pairing")
    PAIR(prod2b, "provoleta (grilled provolone)", "complement", "established", "starter",
         "Argentine tradition with rich wine")
    PAIR(prod2b, "chocolate and dulce de leche dessert", "bridge", "established", "dessert",
         "rich sweetness bridge")

p2b = P("Achaval Ferrer", "winery", r2, "Argentina",
        production_philosophy="single_vineyard_massal",
        philosophy_description="Old-vine single-vineyard Malbecs from historic parcels; massal selection.",
        reputation_narrative="Among Argentina's most acclaimed Malbec producers; Bella Vista is iconic.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("Achaval Ferrer Malbec Mendoza", "wine_still", p2b, r2, "Argentina",
    subcategory="red",
    description="Benchmark Mendoza Malbec from old vines; plush, structured, and age-worthy.",
    price_tier="premium")
if new2c:
    PAIR(prod2c, "rack of lamb with mint and garlic", "complement", "classic", "main",
         "Malbec and lamb — classic Argentine pairing")
    PAIR(prod2c, "grilled Wagyu skirt steak", "complement", "established", "main",
         "rich beef and structured Malbec")
    PAIR(prod2c, "blue cheese and walnut salad", "complement", "established", "starter",
         "tannin cuts blue cheese intensity")
    PAIR(prod2c, "mushroom and truffle empanada", "bridge", "established", "amuse",
         "earthy bridge to wine character")

prod2d, new2d = PROD("Achaval Ferrer Finca Bella Vista Malbec", "wine_still", p2b, r2, "Argentina",
    subcategory="red",
    description="Single-vineyard old-vine Malbec; one of Argentina's most celebrated wines.",
    price_tier="ultra_premium")
if new2d:
    PAIR(prod2d, "prime dry-aged beef with bone marrow", "complement", "classic", "main",
         "iconic Malbec with premium aged beef")
    PAIR(prod2d, "slow-roasted Patagonian lamb", "complement", "classic", "main",
         "Patagonian lamb and old-vine Malbec")
    PAIR(prod2d, "truffle-infused polenta", "complement", "established", "main",
         "earthiness and richness bridge")
    PAIR(prod2d, "aged sardo cheese with honey", "complement", "established", "cheese",
         "rich tannin and aged cheese")

# ── 3. Priorat DOQ ────────────────────────────────────────────────────────────
print("=== Priorat DOQ ===")
r3 = R("Priorat DOQ", "Spain", "wine",
        designation_type="DOQ", designation_name="Priorat",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Spain's only DOQ alongside Rioja, Priorat is a tiny, remote wine region "
            "in Catalonia producing some of the world's most intense and mineral wines. "
            "Ancient Garnacha and Cariñena vines grow in the distinctive llicorella "
            "schist soils, producing wines of extraordinary concentration, minerality, "
            "and complexity. The region's dramatic terraced vineyards and extreme yields "
            "(often under 1kg per vine) yield wines of unrivalled character."
        ),
        key_producers="Álvaro Palacios, Clos Mogador, Mas Doix, Cims de Porrera",
        historical_context=(
            "An almost abandoned wine region by the 1970s, Priorat was revived in the "
            "1980s by a group of winemakers including René Barbier and Álvaro Palacios. "
            "L'Ermita, first produced in 1993, became one of the world's most expensive "
            "wines and sparked a global fascination with the region."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "stable",  "Classic Priorat conditions; concentrated and fresh"),
    (2021, "very_good",  "stable",  "Elegant interpretation; fresh with good acidity"),
    (2020, "exceptional","rising",  "Outstanding vintage; wines of extraordinary depth"),
    (2019, "excellent",  "stable",  "Balanced year; wines for long-term aging"),
    (2018, "very_good",  "stable",  "Good freshness; approachable earlier"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Álvaro Palacios Priorat", "winery", r3, "Spain",
        production_philosophy="terroir_minimalist",
        philosophy_description="Minimal intervention; llicorella schist expression through old Garnacha.",
        reputation_narrative="Priorat's most celebrated winemaker; L'Ermita is Spain's most iconic wine.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Álvaro Palacios Camins del Priorat", "wine_still", p3a, r3, "Spain",
    subcategory="red",
    description="Entry to the Palacios Priorat range; mineral, concentrated, approachable.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "grilled lamb chops with romesco", "complement", "classic", "main",
         "Catalan lamb and Priorat Garnacha")
    PAIR(prod3a, "pa amb tomàquet with cured meats", "complement", "classic", "starter",
         "Catalan bread tradition")
    PAIR(prod3a, "braised rabbit with wild mushrooms", "complement", "established", "main",
         "game and earthy schist mineral notes")
    PAIR(prod3a, "aged Manchego with dried fruit", "complement", "established", "cheese",
         "concentrated fruit bridges aged cheese")

prod3b, new3b = PROD("Álvaro Palacios Les Terrasses Priorat DOQ", "wine_still", p3a, r3, "Spain",
    subcategory="red",
    description="Mid-tier Palacios Priorat; old-vine Garnacha and Cariñena with mineral intensity.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "slow-roasted suckling lamb (lechazo)", "complement", "classic", "main",
         "Spanish lechazo and mineral Garnacha")
    PAIR(prod3b, "black olive and anchovy tapenade crostini", "complement", "established", "amuse",
         "salty umami and mineral wine")
    PAIR(prod3b, "braised oxtail with saffron rice", "complement", "established", "main",
         "richness and concentration in harmony")
    PAIR(prod3b, "aged Manchego with quince", "complement", "classic", "cheese",
         "classic Spanish cheese pairing")

p3b = P("Clos Mogador", "winery", r3, "Spain",
        production_philosophy="biodynamic_old_vine",
        philosophy_description="Biodynamic pioneer in Priorat; single-estate old-vine Garnacha.",
        reputation_narrative="One of Priorat's founding estates; Clos Mogador is a benchmark wine.",
        price_positioning="ultra_premium")
prod3c, new3c = PROD("Clos Mogador Priorat DOQ", "wine_still", p3b, r3, "Spain",
    subcategory="red",
    description="Estate flagship; ancient Garnacha vines on llicorella of extraordinary minerality.",
    price_tier="ultra_premium")
if new3c:
    PAIR(prod3c, "roast leg of lamb with garlic and herbs", "complement", "classic", "main",
         "Priorat's classic lamb pairing")
    PAIR(prod3c, "grilled Iberico pork loin with romesco", "complement", "established", "main",
         "Catalan sauce and mineral wine")
    PAIR(prod3c, "dark chocolate and espresso tart", "complement", "established", "dessert",
         "mineral intensity and chocolate depth")
    PAIR(prod3c, "truffle and mushroom croqueta", "bridge", "established", "amuse",
         "earthy mineral bridge")

prod3d, new3d = PROD("Manyetes Priorat DOQ", "wine_still", p3b, r3, "Spain",
    subcategory="red",
    description="Sister wine to Clos Mogador; pure old-vine Cariñena of striking mineral intensity.",
    price_tier="ultra_premium")
if new3d:
    PAIR(prod3d, "wood-roasted lamb ribs", "complement", "classic", "main",
         "rustic lamb and structured Cariñena")
    PAIR(prod3d, "anchovies and capers on toast", "contrast", "established", "amuse",
         "mineral salinity contrast")
    PAIR(prod3d, "aged semi-firm cheese with honey", "complement", "established", "cheese",
         "structured tannin and aged dairy")
    PAIR(prod3d, "wild boar with juniper berry sauce", "complement", "established", "main",
         "game and old-vine Cariñena intensity")

# ── 4. Alentejo DOC ──────────────────────────────────────────────────────────
print("=== Alentejo DOC ===")
r4 = R("Alentejo DOC", "Portugal", "wine",
        designation_type="DOC", designation_name="Alentejo",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Portugal's largest wine region by volume and the country's most dynamic "
            "modern wine zone. Alentejo occupies the vast plains south of Lisbon, with "
            "a hot continental climate tempered by Atlantic influence. Indigenous varieties "
            "Aragonês (Tempranillo), Trincadeira, Alicante Bouschet, and Antão Vaz produce "
            "wines of rich fruit concentration, generous body, and increasing complexity. "
            "The Herdades (large estates) model has attracted significant investment."
        ),
        key_producers="Herdade do Esporão, Herdade do Mouchão, Cortes de Cima, João Portugal Ramos",
        historical_context=(
            "Alentejo's wine tradition dates to Roman times, but modernization only began "
            "in the 1990s after co-operatives were replaced by private investment. The region "
            "now accounts for the majority of Portugal's premium wine production by value, "
            "with Herdade do Esporão leading the quality revolution."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Long warm summer; wines of great concentration"),
    (2021, "very_good",  "stable",  "Balanced season; fresh and approachable"),
    (2020, "excellent",  "stable",  "Outstanding year; great aging potential"),
    (2019, "very_good",  "stable",  "Consistent and reliable vintage"),
    (2018, "very_good",  "stable",  "Good freshness despite warm conditions"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Herdade do Esporão", "winery", r4, "Portugal",
        production_philosophy="sustainable_organic",
        philosophy_description="Certified organic; extensive research into indigenous varieties.",
        reputation_narrative="Alentejo's most celebrated estate; private label is a global benchmark.",
        price_positioning="premium",
        authority_tier=1)
prod4a, new4a = PROD("Esporão Reserva Tinto Alentejo", "wine_still", p4a, r4, "Portugal",
    subcategory="red",
    description="Benchmark Alentejo red; blend of Aragonês and Trincadeira with remarkable balance.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "slow-roasted pork with migas (fried breadcrumbs)", "complement", "classic", "main",
         "Alentejo pork and regional wine — the classic pairing")
    PAIR(prod4a, "grilled lamb with coriander and garlic", "complement", "classic", "main",
         "Alentejo lamb tradition")
    PAIR(prod4a, "açorda de bacalhau (bread and salt cod soup)", "complement", "established", "main",
         "regional bread soup and local wine")
    PAIR(prod4a, "Serpa cheese with honey", "complement", "classic", "cheese",
         "Alentejo regional cheese pairing")

prod4b, new4b = PROD("Esporão Reserva Branco Alentejo", "wine_still", p4a, r4, "Portugal",
    subcategory="white",
    description="Complex Antão Vaz-based white; textured, mineral, age-worthy.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "grilled sea bass with lemon and olive oil", "complement", "classic", "main",
         "Mediterranean fish and regional white")
    PAIR(prod4b, "salt cod with chickpeas and olive oil", "complement", "classic", "main",
         "bacalhau and Alentejo white — quintessential Portuguese pairing")
    PAIR(prod4b, "asparagus risotto with local cheese", "complement", "established", "main",
         "richness and minerality in balance")
    PAIR(prod4b, "smoked almonds and olives", "complement", "classic", "amuse",
         "Alentejo snack tradition")

p4b = P("Herdade do Mouchão", "winery", r4, "Portugal",
        production_philosophy="traditional_estate",
        philosophy_description="Historic estate with century-old Alicante Bouschet vines; traditional methods.",
        reputation_narrative="Home of Portugal's most iconic Alicante Bouschet; Tonel No 3-4 is legendary.",
        price_positioning="ultra_premium")
prod4c, new4c = PROD("Herdade do Mouchão Tonel 3-4 Alentejo", "wine_still", p4b, r4, "Portugal",
    subcategory="red",
    description="Portugal's most celebrated Alicante Bouschet; ancient vines, extraordinary depth.",
    price_tier="ultra_premium")
if new4c:
    PAIR(prod4c, "slow-roasted suckling pig (leitão)", "complement", "classic", "main",
         "Portuguese suckling pig and powerful red wine")
    PAIR(prod4c, "black Alentejo pork (porco preto) loin", "complement", "classic", "main",
         "regional pork breed and estate wine")
    PAIR(prod4c, "aged Alentejo Serpa cheese", "complement", "established", "cheese",
         "powerful wine and robust aged cheese")
    PAIR(prod4c, "wild boar with orange and thyme", "complement", "established", "main",
         "game and Alicante Bouschet concentration")

prod4d, new4d = PROD("Herdade do Mouchão Dom Rafael Alentejo", "wine_still", p4b, r4, "Portugal",
    subcategory="red",
    description="Entry-tier Mouchão red; approachable Aragonês and Alicante Bouschet blend.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "grilled lamb chops with piri-piri", "complement", "classic", "main",
         "Alentejo lamb with local wine")
    PAIR(prod4d, "migas with pork and greens", "complement", "classic", "main",
         "traditional Alentejo comfort food")
    PAIR(prod4d, "Serra da Estrela cheese", "complement", "established", "cheese",
         "Portuguese cheese and red wine")
    PAIR(prod4d, "pork and chouriço tapas", "complement", "classic", "amuse",
         "Alentejo bar snack tradition")

# ── 5. Vougeot and Côte de Nuits supplement ────────────────────────────────────
print("=== Pomerol AOC ===")
r5 = R("Pomerol AOC", "France", "wine",
        designation_type="AOC", designation_name="Pomerol",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "Pomerol is the smallest of Bordeaux's great appellations, covering just "
            "800 hectares on the Right Bank plateau near Libourne. Merlot dominates on "
            "the distinctive clay-gravel soils, producing wines of velvet texture, "
            "extraordinary concentration, and haunting floral complexity. Pomerol has "
            "no official classification but Pétrus, Lafleur, and Le Pin are considered "
            "among the world's greatest wines."
        ),
        key_producers="Pétrus, Lafleur, Le Pin, Vieux Château Certan, Clos du Clocher",
        historical_context=(
            "Pomerol's reputation developed later than Médoc — it was excluded from the "
            "1855 Classification. Its rise to global prestige was driven by négociant "
            "Jean-Pierre Moueix, who bottled Pétrus and promoted Right Bank wines globally "
            "from the 1940s. Le Pin, first produced in 1979, became the world's most "
            "expensive wine by the tonne."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Right Bank year; Merlot superb"),
    (2021, "very_good",  "stable",  "Elegant, fresh vintage; early-drinking pleasure"),
    (2020, "exceptional","rising",  "Greatest Pomerol vintage in decades"),
    (2019, "excellent",  "stable",  "Opulent and generous; ready to drink earlier"),
    (2018, "excellent",  "rising",  "Rich and concentrated; long aging potential"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Vieux Château Certan", "winery", r5, "France",
        production_philosophy="bordeaux_traditional",
        philosophy_description="Cabernet Franc adds backbone to Merlot; traditional winemaking at historic estate.",
        reputation_narrative="Pomerol's most consistent estate; benchmark for elegance over power.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Vieux Château Certan Pomerol AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Pomerol's most consistently elegant wine; Merlot-Cabernet blend of haunting complexity.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "duck confit with cherry and lentil", "complement", "classic", "main",
         "Right Bank Merlot and duck — classic Bordeaux pairing")
    PAIR(prod5a, "roast lamb with truffle jus", "complement", "classic", "main",
         "velvet tannin and rich lamb")
    PAIR(prod5a, "beef fillet with Périgueux sauce", "complement", "classic", "main",
         "truffle sauce and Pomerol classic pairing")
    PAIR(prod5a, "aged Saint-Nectaire cheese", "complement", "established", "cheese",
         "velvet texture and semi-soft cheese")

prod5b, new5b = PROD("La Gravette de Certan Pomerol AOC", "wine_still", p5a, r5, "France",
    subcategory="red",
    description="Second wine of VCC; same terroir at accessible price with remarkable character.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "duck breast with plum sauce", "complement", "classic", "main",
         "Merlot and duck — Right Bank tradition")
    PAIR(prod5b, "mushroom and lentil terrine", "complement", "established", "starter",
         "earthy notes bridge to Pomerol clay")
    PAIR(prod5b, "lamb chops with rosemary jus", "complement", "classic", "main",
         "classic Bordeaux lamb pairing")
    PAIR(prod5b, "charcuterie and truffle selection", "bridge", "established", "amuse",
         "earthy richness and clay mineral notes")

p5b = P("Château Clinet", "winery", r5, "France",
        production_philosophy="modern_precision",
        philosophy_description="Modern Pomerol style; precise extraction and French oak integration.",
        reputation_narrative="Consistently excellent Pomerol; one of the appellation's most reliable estates.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Château Clinet Pomerol AOC", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Concentrated and structured Pomerol; dense Merlot with remarkable longevity.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "slow-braised beef short rib with truffle", "complement", "classic", "main",
         "concentrated Merlot and braised beef")
    PAIR(prod5c, "wild mushroom soup with cream", "complement", "established", "starter",
         "earthy Pomerol clay and mushroom")
    PAIR(prod5c, "roast duck with cherries and port", "complement", "classic", "main",
         "Right Bank duck tradition")
    PAIR(prod5c, "blue cheese and walnuts", "complement", "established", "cheese",
         "bold tannin and intense cheese")

prod5d, new5d = PROD("Fleur de Clinet Pomerol AOC", "wine_still", p5b, r5, "France",
    subcategory="red",
    description="Second wine of Clinet; plush and approachable with genuine Pomerol character.",
    price_tier="premium")
if new5d:
    PAIR(prod5d, "beef and mushroom bourguignon", "complement", "classic", "main",
         "braised beef and structured Merlot")
    PAIR(prod5d, "duck pâté with cornichons", "complement", "classic", "starter",
         "classic French starter with Pomerol")
    PAIR(prod5d, "veal chop with morel cream", "complement", "established", "main",
         "delicate veal and elegant Merlot")
    PAIR(prod5d, "mushroom and gruyère feuilleté", "complement", "established", "amuse",
         "earthy richness bridge")

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
print("B153 complete.")
cur.close()
conn.close()
