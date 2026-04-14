#!/usr/bin/env python3
"""Terminal 13 — Batch 1: Rias Baixas DO + Georgia (country) wine"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, description, key_producers,
      designation_type=None, designation_name=None, reputation_tier="prestigious",
      quality_trajectory="established", historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS region: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, description, key_producers,
           designation_type, designation_name, reputation_tier, quality_trajectory,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, description,
          json.dumps(key_producers) if isinstance(key_producers, list) else key_producers,
          designation_type, designation_name, reputation_tier, quality_trajectory,
          historical_context))
    rid = cur.fetchone()[0]
    print(f"  ✓ NEW region: {name} (id={rid})")
    return rid

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ NEW producer: {name} (id={pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ NEW product: {name} (id={pid})")
    return pid

def V(region_id, year, rating, descriptor, narrative, price_traj="stable", window_from=None, window_to=None):
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

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ─── RIAS BAIXAS DO ──────────────────────────────────────────────────────────
print("=== RIAS BAIXAS DO ===")

RIAS = R(
    name="Rias Baixas DO",
    country="Spain",
    beverage_family="wine",
    description=(
        "Spain's premier white wine appellation on the Atlantic coast of Galicia — the spiritual home "
        "of Albariño. The rias (coastal inlets) moderate the Atlantic maritime climate, delivering cool "
        "growing conditions with high rainfall and humidity. The Val do Salnés subzone produces Albariño "
        "of extraordinary aromatic intensity: white peach, apricot, citrus zest, jasmine, and a saline "
        "mineral freshness from the granite soils and Atlantic influence. Rias Baixas transformed Spanish "
        "white wine internationally from the 1980s onward and remains the benchmark for Iberian aromatic "
        "whites. Alcohol is naturally restrained (12-13%), acidity is vibrant, and the wines are among "
        "the world's great food wines — inseparable from Galician seafood culture."
    ),
    key_producers=["Do Ferreiro", "Pazo de Señorans", "Granbazan", "Fillaboa", "Pazo Barrantes", "Zárate"],
    designation_type="DO",
    designation_name="Rias Baixas DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    historical_context=(
        "Albariño's Galician origins are ancient — the variety was established in monasteries along the "
        "Camino de Santiago pilgrimage route. Modern Rias Baixas DO was established in 1988, transforming "
        "fragmented smallholder viticulture into an internationally recognised appellation. The pergola "
        "training system (parral) lifts vines above the humid granite soils, preventing disease while "
        "maximising the Atlantic air circulation that gives Albariño its characteristic freshness."
    )
)

print("\n--- Rias Baixas Producers ---")
DO_FERREIRO = P(
    "Do Ferreiro", "winery", RIAS, "Spain",
    production_philosophy="Biodynamic old-vine Albariño, pre-phylloxera ungrafted vines",
    philosophy_description=(
        "Gerardo Méndez's Do Ferreiro is the reference producer of Rias Baixas — the estate that "
        "defines old-vine Albariño from the Val do Salnés subzone. The Cepas Vellas bottling (from "
        "vines over 200 years old) is considered the finest Albariño expression in the world: a wine "
        "of extraordinary mineral complexity, saline depth, and 20+ year aging potential. Méndez "
        "farms biodynamically on the original ungrafted pre-phylloxera vines — a living archive of "
        "Galician viticultural heritage."
    ),
    reputation_narrative=(
        "The world's most revered Albariño producer. Do Ferreiro Cepas Vellas appears on the lists of "
        "the world's great white wines alongside Montrachet, Chablis Grand Cru, and Egon Müller Riesling."
    ),
    price_positioning="ultra_premium"
)

SENHORANS = P(
    "Pazo de Señorans", "winery", RIAS, "Spain",
    production_philosophy="Estate Albariño from historic Val do Salnés pazo, Galicia",
    philosophy_description=(
        "One of the founding estates of modern Rias Baixas DO and the producer most responsible for "
        "establishing Albariño's international reputation. The pazo (Galician manor house) and its "
        "surroundings form one of the appellation's great terroir sites in Val do Salnés. The Selección "
        "de Añada late-harvest single-vineyard Albariño is among the most age-worthy expressions of "
        "the variety, demonstrating that great Albariño can rival white Burgundy in longevity."
    ),
    reputation_narrative=(
        "A founding producer of modern Rias Baixas DO and primary ambassador for Albariño internationally. "
        "Pazo de Señorans wines appear on fine dining lists across Europe and the Americas."
    ),
    price_positioning="premium"
)

GRANBAZAN = P(
    "Granbazan", "winery", RIAS, "Spain",
    production_philosophy="Technically accomplished Albariño across multiple expressions",
    philosophy_description=(
        "Granbazan (Agro de Bazán) is among the most technically accomplished producers in Rias Baixas, "
        "producing three distinct Albariño expressions at different price points. The Ambar label offers "
        "benchmark fresh-style Albariño while the Limousin bottling demonstrates the variety's capacity "
        "for complexity. A key ambassador for the appellation in export markets."
    ),
    reputation_narrative=(
        "Granbazan Ambar introduced thousands of restaurants worldwide to Rias Baixas Albariño. "
        "One of the appellation's most important export producers."
    ),
    price_positioning="mid_range"
)

FILLABOA = P(
    "Fillaboa", "winery", RIAS, "Spain",
    production_philosophy="Single-estate Albariño from the Condado do Tea subzone, elevated terroir",
    philosophy_description=(
        "One of Rias Baixas's finest single-estate producers, Fillaboa farms the exceptional Monte "
        "Alto single vineyard in the Condado do Tea subzone. The estate's naturally higher-altitude "
        "Albariño shows greater structure and mineral tension than the coastal Val do Salnés style — "
        "a food-wine of remarkable precision and aging capacity."
    ),
    reputation_narrative=(
        "Fillaboa Monte Alto is a benchmark for the structured, mineral style of Albariño from "
        "elevated interior Rias Baixas sites. Highly regarded on fine dining wine lists."
    ),
    price_positioning="premium"
)

print("\n--- Rias Baixas Products ---")
FERREIRO_CV = PROD(
    "Do Ferreiro Cepas Vellas Albariño",
    "wine_still", DO_FERREIRO, RIAS, "Spain",
    subcategory="white",
    description=(
        "The world's greatest Albariño: from ungrafted pre-phylloxera vines over 200 years old in Val do "
        "Salnés. Do Ferreiro Cepas Vellas transcends the 'drink young' perception of Rias Baixas — this is "
        "a wine of extraordinary depth, saline mineral complexity, and decades of aging potential. The nose "
        "shows white peach, dried citrus peel, chamomile, and deep granite minerality; the palate has the "
        "weight of great white wine with the precision of Atlantic salinity. Production is minuscule. "
        "Considered the benchmark against which all Albariño is measured."
    ),
    price_tier="ultra_premium"
)

FERREIRO_ESTATE = PROD(
    "Do Ferreiro Albariño",
    "wine_still", DO_FERREIRO, RIAS, "Spain",
    subcategory="white",
    description=(
        "Do Ferreiro's estate Albariño from Val do Salnés granite soils. Gerardo Méndez's meticulous "
        "biodynamic farming produces a wine of vivid aromatic intensity (white peach, lemon blossom, "
        "jasmine), vibrant acidity, and characteristic saline Atlantic minerality. Drink fresh at 1-2 "
        "years or age confidently to 8-10 years."
    ),
    price_tier="premium"
)

SENHORANS_ESTATE = PROD(
    "Pazo de Señorans Albariño",
    "wine_still", SENHORANS, RIAS, "Spain",
    subcategory="white",
    description=(
        "The estate Albariño that helped establish Rias Baixas internationally. From the Val do Salnés "
        "pazo's granite terroir: white peach, apricot, citrus zest, and the distinctive salinity of "
        "Atlantic Galicia. A benchmark of the fresh, aromatic Rias Baixas style — vivid, food-friendly, "
        "displaying remarkable consistency across vintages."
    ),
    price_tier="premium"
)

SENHORANS_SEL = PROD(
    "Pazo de Señorans Selección de Añada Albariño",
    "wine_still", SENHORANS, RIAS, "Spain",
    subcategory="white",
    description=(
        "Among the most age-worthy Albariño expressions — a single-vineyard, late-harvest selection "
        "released with 3-4 years of age and capable of 15+ years in the cellar. This wine dismantles "
        "the myth that Albariño cannot age: complex dried fruit, oxidative depth, honeyed mineral "
        "concentration, and extraordinary salinity. A collector's wine from one of Galicia's great estates."
    ),
    price_tier="ultra_premium"
)

GRANBAZAN_AMB = PROD(
    "Granbazan Ambar Albariño",
    "wine_still", GRANBAZAN, RIAS, "Spain",
    subcategory="white",
    description=(
        "Granbazan's flagship Albariño — the wine that introduced thousands of restaurants globally "
        "to Rias Baixas. The Ambar label delivers the archetype of fresh, vivid, aromatic Albariño: "
        "white stone fruit, citrus zest, floral notes, and the clean Atlantic salinity that makes "
        "this variety irresistible with shellfish. Excellent value for a prestigious appellation."
    ),
    price_tier="mid_range"
)

FILLABOA_MA = PROD(
    "Fillaboa Monte Alto Single Vineyard Albariño",
    "wine_still", FILLABOA, RIAS, "Spain",
    subcategory="white",
    description=(
        "From the elevated Monte Alto vineyard in Condado do Tea — the most structured and mineral "
        "expression of Albariño in the Fillaboa range. Greater altitude and inland influence produce "
        "a wine of additional tension and longevity compared to coastal Val do Salnés: citrus, "
        "green apple, mineral precision, and a stony grip that rewards 5-8 years of cellaring."
    ),
    price_tier="premium"
)

# ─── GEORGIA (COUNTRY) WINE ──────────────────────────────────────────────────
print("\n=== GEORGIA WINE ===")

GEORGIA = R(
    name="Georgia Wine Regions",
    country="Georgia",
    beverage_family="wine",
    description=(
        "Georgia is the world's oldest wine-producing nation — archaeological evidence places viticulture "
        "in the South Caucasus from 8,000 BCE. The qvevri (clay amphora) wine-making tradition, where "
        "grapes ferment and age in underground clay vessels, was inscribed on UNESCO's Intangible Cultural "
        "Heritage list in 2013. The two primary fine wine regions are Kakheti (eastern Georgia's primary "
        "wine zone, home to Rkatsiteli and Saperavi) and Kartli/Imereti (western regions with extended "
        "skin-contact whites). Georgia's amber/orange wines — qvevri-fermented Rkatsiteli with extended "
        "skin contact — are among the most influential fine dining wine trends of the 21st century, "
        "inspiring the global natural wine movement and skin-contact wine renaissance."
    ),
    key_producers=["Pheasant's Tears", "Iago's Wine", "Château Mukhrani", "Okro's Wines", "Jakeli Wines"],
    designation_type="GI",
    designation_name="Protected Designation of Origin",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    historical_context=(
        "The 8,000-year viticultural history of Georgia's South Caucasus makes it humanity's oldest wine "
        "culture. The qvevri tradition survived Soviet collectivisation through small family producers in "
        "Kakheti's villages. Post-Soviet independence saw a renaissance of traditional qvevri wine — "
        "leading producers (Pheasant's Tears, Iago's Wine) became catalysts for the global natural wine "
        "and amphora wine movement. Georgia is now a major fine dining pilgrimage destination and its "
        "amber wines appear on Michelin restaurant wine lists worldwide."
    )
)

print("\n--- Georgia Wine Producers ---")
PHEASANTS = P(
    "Pheasant's Tears", "winery", GEORGIA, "Georgia",
    production_philosophy="Traditional qvevri vinification of indigenous Georgian varieties, biodynamic",
    philosophy_description=(
        "John Wurdeman (American painter) and Gela Patalishvili founded Pheasant's Tears in Signagi, "
        "Kakheti in 2007 — now the most internationally recognised Georgia wine producer and the primary "
        "ambassador for qvevri wine culture globally. The project revived nearly extinct indigenous "
        "varieties (Kisi, Chinuri, Krakhuna, Rkatsiteli) and demonstrated that traditional qvevri "
        "fermentation could produce wines of world-class quality. Their wines appear on Noma, Mugaritz, "
        "and leading natural wine restaurant lists worldwide."
    ),
    reputation_narrative=(
        "Pheasant's Tears is the most internationally recognised Georgian wine producer and the primary "
        "catalyst for the global amber wine movement. Featured on the world's most forward-thinking "
        "restaurant wine lists from Copenhagen to Tokyo."
    ),
    price_positioning="premium"
)

IAGOS = P(
    "Iago's Wine", "winery", GEORGIA, "Georgia",
    production_philosophy="Traditional qvevri Chinuri from Kartli region, minimal intervention",
    philosophy_description=(
        "Iago Bitarishvili is one of Georgia's most influential natural winemakers — farming Chinuri "
        "(a rare indigenous variety) in the Kartli region using exclusively traditional qvevri methods. "
        "His skin-contact Chinuri is a defining expression of amber wine: copper-hued, phenolic, "
        "tannic, with walnut skin, dried apricot, and haunting mineral precision. A small production "
        "cult wine sought by the world's top natural wine lists."
    ),
    reputation_narrative=(
        "Iago Bitarishvili is a cult figure in the global natural wine world. His qvevri Chinuri is "
        "one of the most sought-after amber wines, appearing on the finest natural wine lists worldwide."
    ),
    price_positioning="premium"
)

MUKHRANI = P(
    "Château Mukhrani", "winery", GEORGIA, "Georgia",
    production_philosophy="Historic royal estate bridging Georgian tradition and international wine culture",
    philosophy_description=(
        "The historic royal estate of the Mukhranbatoni dynasty, restored to world-class production "
        "after independence. Château Mukhrani bridges Georgian tradition and international wine culture — "
        "producing both qvevri-fermented indigenous wines and European-style varietals from the Kartli "
        "plateau's exceptional terroir. The estate is Georgia's most prestigious address and produces "
        "wines served at state dinners and top international hotels."
    ),
    reputation_narrative=(
        "Georgia's most prestigious historic estate. Château Mukhrani wines are served at state banquets "
        "and appear on leading international hotel wine lists. The estate is Georgia's most important "
        "fine wine ambassador for visitors and institutions."
    ),
    price_positioning="premium"
)

print("\n--- Georgia Wine Products ---")
PT_RKATSITELI = PROD(
    "Pheasant's Tears Rkatsiteli",
    "wine_still", PHEASANTS, GEORGIA, "Georgia",
    subcategory="orange",
    description=(
        "The defining expression of qvevri-fermented Rkatsiteli — Pheasant's Tears' flagship wine and "
        "a touchstone of the global amber wine movement. Whole clusters ferment in underground qvevri for "
        "6 months of skin contact, producing a wine of extraordinary phenolic structure: deep amber-copper "
        "hue, intense dried apricot, walnut, saffron, quince, and mineral depth from Kakheti's volcanic "
        "soils. The long skin contact gives tannin structure unusual for a white grape — this is a food "
        "wine of remarkable versatility and aging potential (10-15 years)."
    ),
    price_tier="premium"
)

PT_KISI = PROD(
    "Pheasant's Tears Kisi",
    "wine_still", PHEASANTS, GEORGIA, "Georgia",
    subcategory="orange",
    description=(
        "Kisi is a rare indigenous Kakhetian variety revived by Pheasant's Tears. The qvevri-fermented "
        "Kisi shows a more aromatic, floral profile than Rkatsiteli: dried rose petal, orange blossom, "
        "quince, and a distinctive spice note from extended skin contact. The palate has bright acidity "
        "balanced by phenolic structure — more elegant and approachable than Rkatsiteli, with 6-10 "
        "years of aging potential."
    ),
    price_tier="premium"
)

PT_SAPERAVI = PROD(
    "Pheasant's Tears Saperavi",
    "wine_still", PHEASANTS, GEORGIA, "Georgia",
    subcategory="red",
    description=(
        "Saperavi ('paint' in Georgian) is one of the world's only naturally teinturier grape varieties "
        "— with red flesh as well as red skin — producing wines of intense colour, dark fruit concentration, "
        "and remarkable tannin structure. Pheasant's Tears' qvevri-fermented Saperavi shows extraordinary "
        "depth: blackberry, dark cherry, pomegranate, tobacco, and iron mineral. Traditional qvevri "
        "vinification gives complexity and longevity that modern Georgian wine rarely achieves. "
        "Age 8-15 years with confidence."
    ),
    price_tier="premium"
)

IAGOS_CHINURI = PROD(
    "Iago's Wine Chinuri",
    "wine_still", IAGOS, GEORGIA, "Georgia",
    subcategory="orange",
    description=(
        "The world's defining expression of Chinuri — a rare indigenous Georgian variety from the Kartli "
        "region that produces skin-contact wines of haunting precision. Iago Bitarishvili's traditional "
        "qvevri Chinuri: copper-amber, with dried apricot, walnut skin, chamomile, and a saline mineral "
        "precision from the Kartli plateau soils. The phenolic structure is present but finer than "
        "Rkatsiteli — an ethereal amber wine that has influenced natural winemakers from Copenhagen "
        "to San Francisco."
    ),
    price_tier="premium"
)

MUKHRANI_RK = PROD(
    "Château Mukhrani Rkatsiteli",
    "wine_still", MUKHRANI, GEORGIA, "Georgia",
    subcategory="white",
    description=(
        "Château Mukhrani's estate Rkatsiteli bridges traditional Georgian practice and accessibility — "
        "a qvevri-influenced white (shorter skin contact than traditional amber wines) that expresses "
        "the variety's characteristic dried stone fruit, quince, and mineral character in a more "
        "approachable style. From the historic royal estate's Kartli terroir. An ideal introduction "
        "to Georgian indigenous white varieties for fine dining guests."
    ),
    price_tier="mid_range"
)

# ─── RIAS BAIXAS VINTAGES ─────────────────────────────────────────────────────
print("\n=== RIAS BAIXAS VINTAGES ===")
V(RIAS, 2015, 94, "exceptional",
  "The greatest Rias Baixas vintage in a decade: perfect Atlantic growing season with sufficient "
  "rainfall to prevent stress, warm summer, and a dry September harvest. The Val do Salnés Albariño "
  "achieved extraordinary aromatic intensity and natural acidity. Do Ferreiro Cepas Vellas 2015 is "
  "considered one of the great white wine bottles of the decade. Outstanding age-worthiness.",
  "rising", 2017, 2030)

V(RIAS, 2017, 90, "excellent",
  "A warm, dry year in Galicia — atypical conditions for this Atlantic appellation. The heat "
  "challenged the usual freshness of Albariño, but producers with older vines and granite soils "
  "maintained acidity. Best drunk young (2-4 years); less age-worthy than cool-climate vintages "
  "but offering richer, rounder fruit expression.",
  "stable", 2018, 2023)

V(RIAS, 2019, 93, "exceptional",
  "A pristine cool-climate Rias Baixas vintage — the Atlantic conditions that define the appellation "
  "at their most expressive. Perfect balance between the rainfall and sunshine of the Galician coast "
  "produced Albariño of crystalline clarity: intense white peach, jasmine, lemon zest, and that "
  "defining saline Atlantic minerality. Excellent aging potential for 8-12 years.",
  "stable", 2021, 2030)

V(RIAS, 2021, 92, "excellent",
  "Classic Atlantic Rias Baixas vintage: cool and maritime with excellent natural acidity. The Val "
  "do Salnés granite terroir expressed its mineral character beautifully. Albariño of pristine "
  "freshness and aromatic precision — ideal food wine style with 5-8 year aging potential.",
  "stable", 2022, 2028)

V(RIAS, 2022, 91, "excellent",
  "Consistent Rias Baixas vintage with good quality across the appellation. Warmer than 2021 but "
  "the Atlantic influence maintained characteristic freshness. Albariño shows approachable fruit "
  "and good mineral expression — drink 2023-2026 for maximum freshness.",
  "stable", 2023, 2026)

# ─── GEORGIA VINTAGES ─────────────────────────────────────────────────────────
print("\n=== GEORGIA WINE VINTAGES ===")
V(GEORGIA, 2015, 95, "exceptional",
  "The standout modern Georgian vintage — a perfect Kakhetian growing season produced qvevri wines "
  "of extraordinary concentration and mineral depth. Pheasant's Tears and Iago's Wine 2015 releases "
  "are benchmark expressions of Georgian amber wine: rich, phenolic, with exceptional aging potential. "
  "The Saperavi 2015 from top producers ranks among the great red wines of Eastern Europe.",
  "rising", 2017, 2035)

V(GEORGIA, 2017, 91, "excellent",
  "Warm Georgian vintage with concentrated fruit and generous structure in both Rkatsiteli and "
  "Saperavi. The qvevri fermentation balanced the vintage's richness. Best drunk 2020-2025; "
  "less mineral tension than cool-climate years but offering immediate pleasure.",
  "stable", 2019, 2025)

V(GEORGIA, 2019, 93, "excellent",
  "An excellent Georgian vintage with ideal conditions in Kakheti for indigenous varieties. "
  "The balance of warm days and cool nights produced Rkatsiteli and Saperavi of fine structure "
  "and mineral precision. Pheasant's Tears 2019 is among the finest expressions of their range. "
  "Age-worthy for 10-15 years.",
  "stable", 2021, 2032)

V(GEORGIA, 2021, 90, "excellent",
  "Good Georgia vintage — consistent quality across Kakheti's top producers. The qvevri whites "
  "show classic dried stone fruit and mineral character; Saperavi reds have firm structure "
  "and longevity. Drink 2023-2028.",
  "stable", 2023, 2028)

V(GEORGIA, 2022, 89, "very_good",
  "Solid Georgia vintage with above-average quality. Slightly warmer summer affected the "
  "freshness of lighter whites but the skin-contact amber wines and Saperavi reds benefited "
  "from additional ripeness. Approachable from 2024.",
  "stable", 2024, 2027)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Rias Baixas Albariño pairings
PAIR(FERREIRO_CV, "Percebes (barnacles) with sea salt and hot water",
    "complement", "classic", "starter",
    "Do Ferreiro Cepas Vellas is the supreme expression of the classic Galician pairing: "
    "Albariño and percebes. These extraordinarily fresh barnacles — simply cooked in salted sea "
    "water — demand a wine of pristine saline minerality and acidity. The 200-year-old vine "
    "Albariño's oceanic mineral depth mirrors the barnacle's briny, mineral flavour with uncanny "
    "precision. The most profound wine-food pairing of the Atlantic coast.")

PAIR(FERREIRO_CV, "Sea urchin (uni) with Galician bread and olive oil",
    "elevate", "established", "amuse",
    "Cepas Vellas Albariño and sea urchin: the wine's extraordinary mineral depth and saline "
    "complexity elevates the urchin's oceanic sweetness and iodine character. The 200-year-old "
    "vine concentration provides the weight to stand alongside sea urchin's intensity without "
    "overwhelming its delicate oceanic flavour. One of the transcendent luxury pairings.")

PAIR(FERREIRO_CV, "Steamed razor clams with garlic and parsley",
    "complement", "classic", "starter",
    "Cepas Vellas Albariño and razor clams: the wine's saline depth amplifies the clams' oceanic "
    "sweetness while the garlic and parsley mirror the wine's aromatic precision. The old-vine "
    "concentration bridges the richness of the butter without losing the marine freshness.")

PAIR(FERREIRO_ESTATE, "Galician octopus (pulpo a la gallega) with smoked paprika and olive oil",
    "complement", "classic", "starter",
    "The definitive regional pairing: Galician octopus and Albariño are inseparable in Galician "
    "culinary culture. The wine's bright acidity, white stone fruit, and Atlantic salinity cut "
    "through the octopus's smoky, rich texture while the smoked paprika amplifies the wine's "
    "mineral depth. A pairing rooted in hundreds of years of Galician table tradition.")

PAIR(FERREIRO_ESTATE, "Steamed clams with garlic, white wine, and parsley",
    "complement", "classic", "starter",
    "Albariño and clams: a Galician archetype. Do Ferreiro's estate wine provides the "
    "perfect combination of acidity to cut the clams' brine, aromatic intensity to match "
    "the garlic and parsley, and that characteristic saline minerality that amplifies the "
    "clams' oceanic flavour. One of the world's great shellfish pairings.")

PAIR(SENHORANS_ESTATE, "Grilled turbot with lemon butter and capers",
    "elevate", "established", "fish_course",
    "Pazo de Señorans Albariño and whole roasted turbot — the Galician dream. The wine's "
    "aromatic precision and saline acidity pairs magnificently with turbot's firm, white flesh. "
    "Lemon butter amplifies the wine's citrus character; capers bridge the wine's briny salinity "
    "with the fish's richness. A pairing that defined fine dining in Galicia's paradores.")

PAIR(SENHORANS_ESTATE, "Razor clams with garlic and olive oil",
    "complement", "classic", "starter",
    "The iconic Galician shellfish pairing: Pazo de Señorans Albariño and razor clams. "
    "The wine's vivid acidity and saline Atlantic minerality is the natural companion for "
    "these supremely fresh bivalves. Garlic amplifies the wine's aromatic character while "
    "olive oil bridges the wine's texture with the clam's sweetness.")

PAIR(SENHORANS_SEL, "Aged Galician tetilla cheese with quince paste",
    "elevate", "established", "cheese",
    "Pazo de Señorans Selección de Añada — the most age-worthy Albariño — meets Galicia's "
    "signature cheese. At 5-8 years old, the wine shows honeyed complexity and oxidative depth "
    "that pairs beautifully with the mild, buttery tetilla and the sweet acidity of quince. "
    "A regional pairing demonstrating Albariño's unexpected aging capacity.")

PAIR(GRANBAZAN_AMB, "Salt cod fritters (croquetas de bacalao) with aioli",
    "complement", "classic", "amuse",
    "Granbazan Ambar's vivid, fresh Albariño character is the perfect aperitif match for "
    "salt cod fritters — the wine's bright acidity cuts through the crispy coating and "
    "salt cod richness while the garlic aioli amplifies the wine's mineral saline character. "
    "A Galician-Catalan fusion pairing at its most accessible.")

PAIR(FILLABOA_MA, "Grilled langoustines with herb butter",
    "elevate", "classic", "main",
    "Fillaboa Monte Alto's structured, mineral Albariño from the elevated Condado do Tea site "
    "provides the weight and acidity for grilled langoustines — the king of crustaceans. "
    "The herb butter mirrors the wine's aromatic precision; the langoustine's sweet, firm flesh "
    "is amplified by the wine's granite mineral backbone. A pairing of equal nobility.")

# Georgia wine pairings
PAIR(PT_RKATSITELI, "Roasted whole chicken with walnut and coriander sauce (satsivi)",
    "complement", "classic", "main",
    "Pheasant's Tears Rkatsiteli is the definitive pairing for satsivi — Georgia's iconic "
    "cold chicken in walnut sauce. The wine's phenolic structure and tannic grip from 6-month "
    "skin contact cuts through the dense walnut cream, while the dried fruit and spice character "
    "of qvevri Rkatsiteli amplifies the coriander-fenugreek spice profile. A pairing of deep "
    "cultural resonance — both wine and dish are expressions of Kakhetian identity.")

PAIR(PT_RKATSITELI, "Aged sheep's milk cheese with walnut bread",
    "complement", "classic", "cheese",
    "Pheasant's Tears Rkatsiteli's phenolic structure and oxidative complexity is the natural "
    "companion for aged sheep's milk cheese. The wine's tannic grip cuts through the fat while "
    "the dried stone fruit character amplifies the cheese's caramel depth. Walnut bread echoes "
    "the wine's walnut-skin phenolic note.")

PAIR(PT_RKATSITELI, "Duck confit with pomegranate molasses and coriander",
    "complement", "established", "main",
    "Qvevri Rkatsiteli's tannic structure and oxidative depth makes it one of the rare white "
    "wines that can stand alongside rich duck preparations. The pomegranate molasses amplifies "
    "the wine's dried fruit character; coriander echoes its spice notes. A pairing that "
    "demonstrates why extended skin-contact whites belong at the centre of the dinner table.")

PAIR(PT_KISI, "Smoked trout with horseradish crème fraîche and dill",
    "complement", "established", "starter",
    "Pheasant's Tears Kisi — the more aromatic, floral amber wine — pairs beautifully with "
    "smoked trout. The wine's dried rose, orange blossom, and quince character bridges the "
    "smoke and the cream; its phenolic grip cuts through the crème fraîche richness while "
    "amplifying the trout's delicate smokiness.")

PAIR(PT_KISI, "Georgian cheese bread (khachapuri) with egg and butter",
    "bridge", "classic", "main",
    "Pheasant's Tears Kisi and khachapuri: the quintessential Georgian food pairing. "
    "The wine's floral aromatics, fruit character, and phenolic structure navigate the "
    "rich, cheesy, eggy bread perfectly — bridging the dish's fat-forward profile with "
    "the wine's natural acidity and tannin. A pairing that belongs in any fine dining "
    "education about Georgian cuisine and wine culture.")

PAIR(PT_SAPERAVI, "Slow-braised lamb shoulder with walnut, plum, and herbs (chakapuli)",
    "complement", "classic", "main",
    "Pheasant's Tears Saperavi meets the lamb herb stew that defines Georgian spring feasting. "
    "The wine's inky concentration, pomegranate, dark cherry, and iron mineral structure is the "
    "natural companion for slow-braised lamb with sour plums, tarragon, and coriander. A pairing "
    "of absolute cultural authenticity and flavour harmony.")

PAIR(PT_SAPERAVI, "Grilled aged beef with chimichurri and smoked salt",
    "complement", "established", "main",
    "Saperavi — one of the world's most teinturier red grapes — produces wines of extraordinary "
    "concentration and tannin, natural partners for grilled beef. Pheasant's Tears Saperavi's "
    "dark fruit, tobacco, and iron mineral character stand alongside aged beef with confidence; "
    "chimichurri's herb freshness amplifies the wine's character while smoked salt bridges "
    "the wine's structure with the beef's char.")

PAIR(IAGOS_CHINURI, "Raw oysters on the half shell",
    "elevate", "established", "amuse",
    "Iago's Wine Chinuri — the haunting, mineral qvevri amber — creates an extraordinary pairing "
    "with raw oysters. The wine's saline, briny mineral precision mirrors the oyster's oceanic "
    "character while its phenolic structure provides contrast to the oyster's slick texture. "
    "An unexpected but revelatory combination — demonstrating that qvevri wine's mineral depth "
    "can rival Champagne and Chablis for oyster pairing prestige.")

PAIR(IAGOS_CHINURI, "Burrata with tomato, basil, and aged balsamic",
    "complement", "suggested", "starter",
    "Iago's Wine Chinuri's ethereal mineral precision and phenolic structure finds an unexpected "
    "partner in burrata — the wine's dried fruit and walnut character amplifies the cream's "
    "richness while the acidity cuts through it. Tomato's acidity bridges the wine's structure; "
    "basil echoes its herbal character. A pairing that brings Georgian amber wine into "
    "contemporary Italian-influenced fine dining.")

PAIR(MUKHRANI_RK, "Salmon gravlax with dill, mustard, and rye bread",
    "complement", "established", "starter",
    "Château Mukhrani Rkatsiteli — in its more accessible, shorter skin-contact style — "
    "pairs beautifully with gravlax. The wine's quince and dried stone fruit character "
    "bridges the salmon's salt cure; dill echoes the wine's herbal note; the phenolic "
    "structure cuts through the fatty fish richness. An ideal gateway pairing for diners "
    "discovering Georgian wine through familiar Nordic-inspired food.")

PAIR(MUKHRANI_RK, "Georgian cheese board with churchkhela (walnut grape must candy)",
    "bridge", "classic", "cheese",
    "Château Mukhrani Rkatsiteli and a Georgian cheese board with churchkhela — the chewy, "
    "walnut-filled candy made from concentrated grape must — is the most authentically Georgian "
    "wine and food experience. The wine's dried fruit and gentle phenolic character bridges "
    "the cheese's salt and fat with the sweet walnut candy's concentrated grape character.")

cur.close()
conn.close()
print("\n✅ Terminal 13 Batch 1 — Rias Baixas DO + Georgia Wine complete.")
