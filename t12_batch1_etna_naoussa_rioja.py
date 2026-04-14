#!/usr/bin/env python3
"""Terminal 12 — Batch 1: Etna DOC (new region) + Naoussa + Rioja + Soave depth"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

NAOUSSA = 180
RIOJA   = 175
SOAVE   = 173

def R(name, country, beverage_family, description, key_producers,
      designation_type=None, designation_name=None, reputation_tier="prestigious",
      quality_trajectory="ascending", historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, description, key_producers,
           designation_type, designation_name, reputation_tier, quality_trajectory,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, description, key_producers,
          designation_type, designation_name, reputation_tier, quality_trajectory,
          historical_context))
    row = cur.fetchone()
    print(f"  ✓ REGION: {name} (id={row[0]})")
    return row[0]

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          reputation_narrative, price_positioning, authority_tier))
    row = cur.fetchone()
    print(f"  ✓ {name} (id={row[0]})")
    return row[0]

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, producer_id, region_id, origin_country,
           subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, producer_id, region_id, origin_country,
          subcategory, description, price_tier))
    row = cur.fetchone()
    print(f"    ✓ {name} (id={row[0]})")
    return row[0]

def V(region_id, year, rating, descriptor, narrative, price_traj="rising", window_from=None, window_to=None):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory,
           drinking_window, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,1)
        ON CONFLICT (region_id, vintage_year) DO NOTHING
    """, (region_id, year, rating, descriptor, narrative, price_traj,
          json.dumps({"from": window_from, "to": window_to}) if window_from else None))
    action = "✓" if cur.rowcount else "~"
    print(f"  {action} {year} → region {region_id}: {descriptor} ({rating})")

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ═══════════════════════════════════════════════════════════════════════════
# ETNA DOC — SICILY (NEW REGION)
# ═══════════════════════════════════════════════════════════════════════════
print("=== ETNA DOC — SICILY (NEW REGION) ===")

ETNA = R("Etna DOC", "Italy", "wine",
    description="Europe's most dramatic wine region — terraced vineyards on the slopes of an active volcano at 400-1000m altitude. Etna DOC has become the world's most discussed emerging wine region since 2000. The ancient Nerello Mascalese grape — planted pre-phylloxera on ungrafted alberello (bush vine) plants on volcanic black basalt soils — produces wines of extraordinary mineral complexity, delicacy, and aging potential. The altitude extremes and volcanic soil chemistry create Nerello Mascalese of Pinot Noir-like refinement. Etna Bianco from Carricante adds a white wine of rare mineral tension.",
    key_producers="Benanti, Cornelissen, Terre Nere, Passopisciaro, Giulio Gambino, Ciro Biondi",
    designation_type="DOC",
    designation_name="Etna DOC (established 1968)",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    historical_context="Etna DOC was established in 1968 — one of Sicily's earliest appellations. For decades, the wines were consumed locally. Beginning with Benanti in the 1990s and accelerating through Cornelissen (2001), Terre Nere (2002), and Passopisciaro (2004), Etna became a global benchmark for volcanic terroir wine.")

print(f"\nEtna region ID: {ETNA}")

# Etna producers
terre_nere = P("Benanti", "winery", ETNA, "Italy",
    production_philosophy="Etna DOC pioneer — Nerello Mascalese from pre-phylloxera volcanic basalt",
    philosophy_description="Giuseppe Benanti founded the modern Etna DOC movement in 1988 when he restored ancient alberello vineyards on the volcano's north slope. The Benanti Serra della Contessa — from contrada (sub-district) vineyards at 800m — was the first Etna Rosso to attract international attention. The estate's research into Etna's distinct contrade (sub-districts equivalent to Burgundian lieux-dits) established the vocabulary of Etna terroir.",
    key_personnel=[{"name": "Giuseppe Benanti", "role": "Founder"}, {"name": "Antonio Benanti", "role": "Director"}],
    production_details={"altitude": "400-900m", "varieties": "Nerello Mascalese (red), Carricante (white)", "viticulture": "alberello pre-phylloxera vines"},
    reputation_narrative="Benanti is the founding estate of the modern Etna DOC movement — the first producer to demonstrate to the world that Nerello Mascalese from volcanic basalt could produce wines of international class. The Serra della Contessa is consistently one of Italy's most discussed emerging wines.",
    price_positioning="premium")

PROD("Benanti Serra della Contessa Etna Rosso", "wine_still", terre_nere, ETNA, "Italy",
    subcategory="nerello_mascalese_etna",
    description="The founding expression of modern Etna DOC — from the Serra della Contessa contrada on Etna's north slope at 800m altitude. Ancient pre-phylloxera alberello Nerello Mascalese on volcanic black basalt. Wild fermentation; aged in large Slavonian oak. Pale garnet (Pinot Noir-like colour); dried rose, red cherry, volcanic mineral, dried herbs, and remarkable iron-saline finish from basalt soils. The Pinot Noir of Sicily — delicate, complex, age-worthy. Italy's most discussed emerging wine region's benchmark expression.",
    price_tier="premium")

cornelissen = P("Frank Cornelissen", "winery", ETNA, "Italy",
    production_philosophy="Extreme natural wine — no sulphur, no additions, Etna volcanic terroir unfiltered",
    philosophy_description="Belgian-born Frank Cornelissen arrived on Etna in 2001 and immediately began the most radical natural wine experiment on the volcano: no sulphur dioxide, no temperature control, no fining or filtration, no modern additions of any kind. MunJebel is the single-vineyard Nerello Mascalese expression series — each named for its altitude contour. Cornelissen's approach divides opinion but his Magma (from vines at 1000m) is consistently one of Italy's most discussed and collected wines.",
    key_personnel=[{"name": "Frank Cornelissen", "role": "Owner/Winemaker"}],
    production_details={"philosophy": "zero sulphur, zero additions, zero filtration", "altitude": "600-1000m", "flagship": "Magma from 1000m vines"},
    reputation_narrative="Frank Cornelissen is Etna's most controversial and internationally followed producer — his zero-intervention approach and MunJebel single-vineyard series have polarised critics while attracting collector interest globally. The Magma from 1000m alberello vines is consistently listed among Italy's most notable natural wines.",
    price_positioning="ultra_premium")

PROD("Cornelissen Munjebel Rosso Terre Siciliane", "wine_still", cornelissen, ETNA, "Italy",
    subcategory="nerello_mascalese_etna",
    description="Frank Cornelissen's flagship Nerello Mascalese from ancient alberello vines at 600-750m altitude on Etna's north slope. Zero sulphur, zero additions, unfiltered and unfined — among the most extreme natural wine expressions in Italy. Orange-tinged pale garnet; volcanic mineral, sour cherry, dried herbs, and an earthy, living complexity that evolves dramatically in the glass. Not for every palate — a wine that demands knowledge and commitment. Among Italy's most internationally collected natural wines.",
    price_tier="ultra_premium")

passopisciaro = P("Passopisciaro", "winery", ETNA, "Italy",
    production_philosophy="Contrade Etna: single-terroir Nerello Mascalese from five distinct volcanic sub-districts",
    philosophy_description="Andrea Franchetti established Passopisciaro in 2004 with the ambition of mapping Etna's contrade (sub-districts) in the manner of Burgundy's lieux-dits. Five contrade expressions — Chiappemacine, Guardiola, Porcaria, Rampante, Sciaranuova — each demonstrate dramatically different volcanic terroir characteristics from identical grape varieties at the same altitude. A definitive terroir experiment that established the vocabulary of Etna DOC sub-regional complexity.",
    key_personnel=[{"name": "Andrea Franchetti", "role": "Founder"}, {"name": "Benjamin Parodi", "role": "Winemaker"}],
    production_details={"system": "five single-contrada expressions", "variety": "Nerello Mascalese 100%", "altitude": "550-900m"},
    reputation_narrative="Passopisciaro's contrade single-vineyard series is the defining terroir experiment of the modern Etna DOC era — the five single-contrada bottlings demonstrate conclusively that volcanic sub-districts produce dramatically different wine characteristics. Consistently among Italy's most critically discussed wines: 93-97 points internationally.",
    price_positioning="ultra_premium")

PROD("Passopisciaro Chiappemacine Etna Rosso", "wine_still", passopisciaro, ETNA, "Italy",
    subcategory="nerello_mascalese_etna",
    description="One of five single-contrada Nerello Mascalese expressions from Passopisciaro — the Chiappemacine contrada at 600-700m altitude on Etna's north slope. 100% Nerello Mascalese from ancient ungrafted alberello vines on volcanic basalt. Aged 18 months in large oak. The Chiappemacine expression demonstrates the most accessible, aromatic side of Passopisciaro's range: red cherry, violet, graphite mineral, and delicate volcanic spice. A Burgundy-lover's Sicily: pale colour, supreme elegance, mineral-driven complexity.",
    price_tier="ultra_premium")

# Etna Bianco
PROD("Benanti Etna Bianco Superiore Pietramarina", "wine_still", terre_nere, ETNA, "Italy",
    subcategory="carricante_etna_bianco",
    description="The benchmark Etna Bianco Superiore — from ancient Carricante vines (the native white variety) in Milo on Etna's east slope, the only zone permitted to use 'Superiore' on the label. Volcanic basalt and altitude produce extraordinary mineral tension: white peach, lemon blossom, green almond, flint, and saline mineral. The most collectible white wine from an active volcano in Europe — ages 10-15 years with confidence. Italy's answer to Chablis Grand Cru mineral intensity.",
    price_tier="premium")

# Add Etna vintages
print("\n=== ETNA DOC VINTAGES ===")
V(ETNA, 2012, 96, "exceptional",
  "The vintage that confirmed Etna DOC's potential for long-lived wines: cool growing season "
  "with minimal heat stress produced Nerello Mascalese of extraordinary freshness and mineral "
  "definition. The 2012 vintage from the north-slope contrade (Passopisciaro, Terre Nere, Cornelissen) "
  "are still developing and considered the most age-worthy Etna wines produced.",
  "rising", 2017, 2035)

V(ETNA, 2015, 94, "exceptional",
  "Warm and generous 2015 produced Nerello Mascalese of more immediate richness and accessibility "
  "than the lean 2012. The volcanic mineral character remained intact. Best expressions from "
  "high-altitude contrade (Guardiola, Rampante at 800-900m) maintained freshness and acid structure.",
  "stable", 2018, 2030)

V(ETNA, 2018, 93, "excellent",
  "Excellent growing season on Etna: moderate temperatures throughout with a clean harvest. "
  "The Nerello Mascalese achieved perfect ripeness without over-ripening — the pale colour, "
  "delicate tannin, and volcanic mineral tension that defines Etna at its most Burgundian. "
  "Wines for 10+ years of development.",
  "rising", 2021, 2030)

V(ETNA, 2020, 91, "excellent",
  "Good Etna vintage with consistent quality across producers. The Carricante white wines "
  "from the east slope (Milo) are particularly successful — Etna Bianco Superiore from 2020 "
  "shows exceptional freshness and mineral tension. The Nerello Mascalese shows good structure.",
  "stable", 2023, 2030)

V(ETNA, 2021, 95, "exceptional",
  "One of the finest Etna vintages in the modern era: a long, cool growing season with "
  "moderate temperatures throughout. Nerello Mascalese achieved extraordinary delicacy and "
  "mineral definition — the closest vintage to classic Burgundy in character. "
  "Age 15-20 years with confidence from the best contrade.",
  "rising", 2024, 2040)

# ═══════════════════════════════════════════════════════════════════════════
# NAOUSSA PDO — GREECE (DEPTH)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== NAOUSSA PDO — GREECE ===")

alpha_estate = P("Alpha Estate", "winery", NAOUSSA, "Greece",
    production_philosophy="Naoussa PDO precision viticulture — single-vineyard Xinomavro from volcanic foothills",
    philosophy_description="Alpha Estate was established in 1997 in Amyndeon (the other key PDO alongside Naoussa) but their Naoussa expression from their Xinomavro single-vineyard program is one of Greece's most internationally recognised. The estate pioneered precision viticulture in northern Greece — GPS mapping, micro-zoning, and individual vine selection — to demonstrate that Xinomavro's Barolo-like potential is fully realisable with modern viticultural methods.",
    key_personnel=[{"name": "Makis Mavridis", "role": "Owner/Viticulturist"}, {"name": "Angelos Iatridis", "role": "Winemaker"}],
    production_details={"sub_regions": "Naoussa and Amyndeon PDO", "approach": "precision viticulture GPS mapping", "flagship": "Xinomavro single vineyard"},
    reputation_narrative="Alpha Estate is one of Greece's most internationally awarded and consistently rated producers — their Xinomavro single-vineyard expression has demonstrated to the world that Greece's indigenous varieties can achieve complexity and ageability comparable to Italy's finest. Consistently 93-96 points from international critics.",
    price_positioning="premium")

PROD("Alpha Estate Hedgehog Vineyard Xinomavro", "wine_still", alpha_estate, NAOUSSA, "Greece",
    subcategory="xinomavro_naoussa",
    description="Alpha Estate's flagship single-vineyard Xinomavro from the Hedgehog vineyard in Naoussa PDO — one of Greece's most celebrated wine expressions. Xinomavro ('acid black') is Greece's greatest red grape: naturally high acid, high tannin, and extraordinary aging potential (sometimes compared to Barolo). The Hedgehog vineyard's volcanic foothills produce Xinomavro of exceptional complexity: sour cherry, dried tomato, olive, leather, and iron mineral. Aged 18 months in French oak. Requires 5-8 years to show full complexity.",
    price_tier="premium")

thymiopoulos = P("Domaine Thymiopoulos", "winery", NAOUSSA, "Greece",
    production_philosophy="Young vineyards, ancient variety — Naoussa Xinomavro rediscovered",
    philosophy_description="Apostolos Thymiopoulos is the young face of the Naoussa wine revolution — his Earth and Sky Xinomavro and Deeply Rooted expressions have attracted international critic attention to northern Greek wine that was previously ignored. The estate works with both young and old Xinomavro vines in Naoussa, producing accessible entry wines (Earth and Sky) and powerful Gran Reserve expressions from 60-year-old vines.",
    key_personnel=[{"name": "Apostolos Thymiopoulos", "role": "Owner/Winemaker"}],
    production_details={"style": "modern approach to traditional Xinomavro", "range": "Earth and Sky (accessible) to Deeply Rooted (reserve)"},
    reputation_narrative="Apostolos Thymiopoulos has been the most internationally recognised voice for Naoussa PDO's young generation — his Earth and Sky Xinomavro was the discovery wine that brought international sommelier attention to northern Greece. Consistently championed by Wine Advocate, Decanter, and Wine Spectator.",
    price_positioning="premium")

PROD("Thymiopoulos Earth and Sky Xinomavro", "wine_still", thymiopoulos, NAOUSSA, "Greece",
    subcategory="xinomavro_naoussa",
    description="Apostolos Thymiopoulos's discovery wine — the expression that introduced international sommeliers to Naoussa's Xinomavro. From younger vines in the appellation; no oak aging (concrete and stainless steel). Fresh and vibrant: sour cherry, dried tomato, olive tapenade, and the characteristic herbal, iron-mineral quality of Xinomavro without the heavy tannin of the barrel-aged expressions. The gateway wine for Greek red wine exploration — 91-94 points and consistent critical praise for value.",
    price_tier="mid_range")

# ═══════════════════════════════════════════════════════════════════════════
# RIOJA DOCa — DEPTH (La Rioja Alta, Marqués de Riscal)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== RIOJA DOCa — SPAIN ===")

la_rioja_alta = P("La Rioja Alta S.A.", "winery", RIOJA, "Spain",
    production_philosophy="Classic Rioja tradition — extended aging, American oak, Gran Reserva craft",
    philosophy_description="La Rioja Alta is the standard-bearer for traditional Rioja Gran Reserva — the 904 (nine hundred and four) and 890 expressions represent over a century of dedication to the Bordón style: extended American oak aging, multiple vintage blending in exceptional years, and release only when fully ready. The 904 Gran Reserva spends a minimum of 4 years in American oak; the 890 spends 4+ years and is released only in outstanding vintages. This is Rioja as the classics intended.",
    key_personnel=[{"name": "María José López de Heredia", "role": "Family Director"}],
    production_details={"flagship": "Gran Reserva 904, Gran Reserva 890", "oak": "American oak, extended aging", "style": "traditional Rioja Gran Reserva"},
    reputation_narrative="La Rioja Alta 904 and 890 Gran Reservas are the benchmarks for traditional Rioja at its finest — the 890 in particular is considered one of Spain's greatest wines, released only in exceptional years after 5+ years of aging. The 904 is the most accessible entry to traditional gran reserva Rioja and consistently the best-value fine Rioja.",
    price_positioning="premium")

PROD("La Rioja Alta Gran Reserva 904", "wine_still", la_rioja_alta, RIOJA, "Spain",
    subcategory="tempranillo_gran_reserva_rioja",
    description="The benchmark for traditional Rioja Gran Reserva — La Rioja Alta's 904 spends minimum 4 years in American oak (in the classic Rioja tradition) before release. Tempranillo-dominant; the extended oak aging creates vanilla, coconut, dried strawberry, leather, and tobacco notes that are entirely different from modern international-style Rioja. Released only after minimum 6 years total aging. Consistently considered the best-value Gran Reserva in Rioja — 93-96 points at premium pricing.",
    price_tier="premium")

riscal = P("Marqués de Riscal", "winery", RIOJA, "Spain",
    production_philosophy="Rioja's oldest continuously operating producer — Médoc tradition since 1858",
    philosophy_description="Marqués de Riscal established the modern Rioja wine industry in 1858, importing Bordeaux winemaking techniques from the Médoc — including Cabernet Sauvignon (which remains unique to Riscal's estate wines today). The Barón de Chirel — from old Tempranillo and Cabernet vines — is the estate's great wine, demonstrating Rioja's capacity for a Bordeaux-influenced style while maintaining the traditional Gran Reserva aging requirement.",
    key_personnel=[{"name": "Francisco Hurtado de Amézaga", "role": "Owner"}],
    production_details={"established": "1858", "heritage": "introduced Médoc techniques to Rioja", "distinction": "unique Cabernet Sauvignon in estate range"},
    reputation_narrative="Marqués de Riscal is Rioja's founding estate — their 1860 vintage is in the Guggenheim Museum collection. The estate's Barón de Chirel demonstrates Rioja's Bordeaux-inspired heritage and is consistently one of Spain's most internationally collected wines from a traditional producer.",
    price_positioning="ultra_premium")

PROD("Marqués de Riscal Gran Reserva", "wine_still", riscal, RIOJA, "Spain",
    subcategory="tempranillo_gran_reserva_rioja",
    description="The estate expression of Rioja's founding producer — Tempranillo with Graciano and Mazuelo from Riscal's own vineyards; minimum 3 years in American oak plus extended bottle aging before release. The Riscal house style shows the Médoc influence: cedar, dried red fruit, leather, tobacco, and the characteristic vanilla-coconut of American oak. More structured and Bordeaux-influenced than other traditional Rioja Gran Reservas — a reflection of Riscal's 165-year old heritage.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# SOAVE DOC — ITALY (ADD DEPTH)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== SOAVE DOC — ITALY ===")

gini = P("Azienda Agricola Gini", "winery", SOAVE, "Italy",
    production_philosophy="Classico zone Garganega — the benchmark for Soave's volcanic complexity",
    philosophy_description="The Gini family has farmed the volcanic basalt hillsides of Soave Classico for four generations. Their La Froscà — from a single volcanic-soil vineyard at 150m — is considered alongside Pieropan's Calvarino as the finest expression of indigenous Garganega. The estate works exclusively with old-vine Garganega (70+ years) on pergola Veronese training, producing wines that demonstrate Soave's potential for complexity, mineral depth, and longevity.",
    key_personnel=[{"name": "Sandro and Claudio Gini", "role": "Owners/Winemakers"}],
    production_details={"zone": "Soave Classico", "soils": "volcanic basalt", "vine_age": "70+ years Garganega"},
    reputation_narrative="Gini La Froscà is consistently considered one of Italy's greatest white wines — the volcanic Soave Classico terroir and ancient Garganega vines produce a wine of Burgundy-level complexity and a 10-year aging curve. Decanter's Soave coverage consistently rates Gini as the region's benchmark alongside Pieropan.",
    price_positioning="premium")

PROD("Gini La Froscà Soave Classico", "wine_still", gini, SOAVE, "Italy",
    subcategory="garganega_soave_classico",
    description="One of Italy's greatest white wines from the Soave Classico zone — single-vineyard La Froscà from 70+ year old Garganega vines on volcanic basalt. Aged on lees in stainless steel; no oak. White almond, lemon blossom, white peach, and volcanic mineral tension — the hallmarks of Garganega at its most complex. The mineral spine from volcanic basalt allows confident aging for 8-12 years. Consistently 93-96 points from Decanter and Gambero Rosso. Demonstrates that Soave Classico is one of Italy's great white wine zones.",
    price_tier="premium")

# ─── PAIRINGS ─────────────────────────────────────────────────────────────
print("\n=== PAIRINGS ===")

def get_product(name):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Product not found: {name}")

BEN_SERRA = get_product("Benanti Serra della Contessa Etna Rosso")
CORN_MUN  = get_product("Cornelissen Munjebel Rosso Terre Siciliane")
PASS_CH   = get_product("Passopisciaro Chiappemacine Etna Rosso")
BEN_BIANC = get_product("Benanti Etna Bianco Superiore Pietramarina")
ALPHA_HH  = get_product("Alpha Estate Hedgehog Vineyard Xinomavro")
THYMP_ES  = get_product("Thymiopoulos Earth and Sky Xinomavro")
LRA_904   = get_product("La Rioja Alta Gran Reserva 904")
RISC_GR   = get_product("Marqués de Riscal Gran Reserva")
GINI_FR   = get_product("Gini La Froscà Soave Classico")

PAIR(BEN_SERRA, "Grilled swordfish with capers, olives, and lemon",
    "complement", "established", "main",
    "Benanti Etna Rosso's pale, delicate Nerello Mascalese structure pairs beautifully with swordfish — the Sicilian fish preparation echoes the wine's island terroir while the capers and olives amplify the volcanic mineral and olive notes. A classic Etna DOC pairing.")

PAIR(BEN_SERRA, "Roasted rabbit with rosemary, olive oil, and wild herbs",
    "complement", "classic", "main",
    "Nerello Mascalese's silky tannin and sour cherry character pairs naturally with roasted rabbit — the wine's lightness doesn't overwhelm the delicate meat while the rosemary and wild herbs echo the volcanic island garrigue character of the wine.")

PAIR(CORN_MUN, "Raw sea urchin (ricci di mare) with toasted bread",
    "complement", "adventurous", "amuse",
    "Frank Cornelissen's zero-sulphur Nerello Mascalese — oxidative, bretty, mineral — creates an adventurous pairing with raw sea urchin. The wine's marine, mineral quality amplifies the ocean brine of the ricci while the brett complexity adds an unexpected dimension. A pairing for natural wine-focused tasting menus.")

PAIR(PASS_CH, "Slow-braised lamb with eggplant, tomato, and Pecorino Siciliano",
    "complement", "established", "main",
    "Passopisciaro Chiappemacine's elegant Nerello Mascalese character pairs beautifully with the classic Sicilian lamb preparation — the wine's delicate tannin and sour cherry character is amplified by eggplant's savory depth while tomato's acidity mirrors the wine's natural acid structure.")

PAIR(BEN_BIANC, "Grilled whole sea bass with lemon, herbs, and extra virgin olive oil",
    "complement", "classic", "main",
    "Etna Bianco Superiore Pietramarina's volcanic mineral tension and white stone fruit character is the definitive match for simply grilled whole fish. The wine's saline mineral spine mirrors the Mediterranean sea while the lemon amplifies the Carricante's characteristic citrus brightness.")

PAIR(ALPHA_HH, "Braised lamb shank with sour cherry and oregano",
    "complement", "classic", "main",
    "Alpha Estate Xinomavro's Barolo-like structure — sour cherry, dried tomato, iron tannin — pairs perfectly with lamb. The sour cherry in the preparation echoes the wine's most distinctive fruit marker; oregano amplifies the herbal Mediterranean character; the slow-braise softens the wine's firm tannin structure.")

PAIR(THYMP_ES, "Grilled lamb souvlaki with tzatziki and flatbread",
    "complement", "classic", "main",
    "Thymiopoulos Earth and Sky's unoaked freshness and herbal Xinomavro character pairs naturally with grilled lamb souvlaki — the most classically Greek pairing. The unoaked style's bright acidity cuts through the meat's fat while the tzatziki's yoghurt bridges the wine's freshness. The gateway to Greek wine and food culture.")

PAIR(THYMP_ES, "Moussaka with béchamel",
    "complement", "classic", "main",
    "The most classically Greek pairing: Xinomavro and moussaka. The wine's high acidity cuts through the béchamel richness; the sour cherry and dried tomato character mirrors the tomato and lamb filling; the herbal character amplifies the cinnamon-spiced meat.")

PAIR(LRA_904, "Roasted leg of lamb with herbs, garlic, and roasted vegetables",
    "complement", "classic", "main",
    "La Rioja Alta 904 Gran Reserva's traditional Tempranillo character — vanilla, leather, dried strawberry, American oak coconut — pairs perfectly with herb-roasted lamb, the classic Spanish pairing. The extended American oak aging creates the vanilla-spice bridge that makes traditional Gran Reserva one of the world's most versatile wine styles with roasted meats.")

PAIR(RISC_GR, "Braised short rib with Rioja reduction and celeriac purée",
    "complement", "established", "main",
    "Marqués de Riscal Gran Reserva's Bordeaux-influenced structure — cedar, dried red fruit, leather — pairs beautifully with braised short rib. A Rioja reduction bridges the wine and the preparation while celeriac purée's earthy, mineral character amplifies the wine's Cabernet-influenced depth.")

PAIR(GINI_FR, "Grilled asparagus with white truffle and lemon",
    "elevate", "established", "starter",
    "Gini La Froscà's volcanic mineral tension and white almond character creates the ideal match for asparagus with white truffle — the wine's mineral spine amplifies truffle's earthy depth while lemon bridges the Garganega's citrus character. One of Italy's great white wine and asparagus pairings.")

PAIR(GINI_FR, "Risotto ai funghi porcini with Parmigiano Reggiano",
    "elevate", "established", "main",
    "La Froscà's volcanic complexity and lees texture pairs beautifully with mushroom risotto — the wine's mineral depth amplifies the porcini's earthiness while the Garganega's natural almond note complements Parmigiano's nutty depth. The wine's structure holds against the risotto's starchy richness.")

cur.close()
conn.close()
print("\n✅ Terminal 12 Batch 1 — Etna DOC + Naoussa + Rioja + Soave complete.")
