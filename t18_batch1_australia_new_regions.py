#!/usr/bin/env python3
"""Terminal 18 — Batch 1: Clare Valley + Coonawarra (new Australian regions)
Clare Valley: Australia's greatest Riesling region (dry, mineral, ageworthy)
Coonawarra: Australia's greatest Cabernet Sauvignon region (terra rossa)
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS region: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers,
           historical_context, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  ✓ Region [{rid}]: {name}, {country}")
    return rid

def VIN(region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory="stable"):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory))
    print(f"    ✓ Vintage {year}: {quality_descriptor} ({quality_rating}/100)")

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
    print(f"  ✓ Producer [{pid}]: {name}")
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
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T18 BATCH 1: CLARE VALLEY + COONAWARRA (NEW AUSTRALIAN REGIONS) ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# CLARE VALLEY — Australia's Greatest Riesling Region
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CLARE VALLEY — NEW REGION ──")
r_clare = R(
    "Clare Valley",
    "Australia",
    "wine",
    designation_type="GI",
    designation_name="Clare Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Clare Valley is Australia's most celebrated Riesling region — a rugged, cool-climate valley "
        "in South Australia's northern Mount Lofty Ranges at 400-500m altitude. The region's distinctive "
        "dry, lean Riesling style — with extraordinary natural acidity, mineral precision, and the "
        "characteristic lime and citrus character — is uniquely Australian: no chaptalisation, no "
        "malolactic fermentation, and the wines are released with tight, austere youth then aged "
        "to extraordinary complexity over 5-20+ years. The screw cap revolution originated in Clare "
        "Valley in 2000, when its leading producers collectively switched to eliminate cork taint and "
        "preserve the Riesling's precise mineral freshness."
    ),
    key_producers="Grosset, Jim Barry, Kilikanoon, Pikes, Pauletts, Skillogalee, Sevenhill",
    historical_context=(
        "Clare Valley's winemaking history stretches to 1851 when Jesuit monks at Sevenhill Cellars planted "
        "the region's first commercial vines. The region's modern reputation was established by Jeffrey "
        "Grosset in the 1980s and 1990s — his Polish Hill and Watervale Rieslings became Australia's "
        "benchmark for the variety. The 2000 Clare Valley Riesling Producers' collective adoption of "
        "screwcap closures was a watershed moment in Australian wine history, proving that technical "
        "precision could override tradition when quality demanded it."
    )
)

print("\n  Adding Clare Valley vintages...")
VIN(r_clare, 2015, 89, "excellent",
    "Classic Clare season with good winter rainfall and cool summer. "
    "Elegant Riesling with excellent acid retention and mineral clarity.",
    price_trajectory="stable")
VIN(r_clare, 2016, 94, "exceptional",
    "Clare Valley's finest recent vintage — perfect season with long, cool summer. "
    "Outstanding Riesling with extraordinary acid structure and citrus intensity. Exceptional for aging.",
    price_trajectory="rising")
VIN(r_clare, 2018, 87, "very_good",
    "Warm, dry vintage requiring careful canopy management. "
    "Generous, accessible Riesling with ripe citrus; drink sooner than typical Clare.",
    price_trajectory="stable")
VIN(r_clare, 2020, 92, "excellent",
    "Cool season with excellent natural acidity. Precise, mineral Riesling "
    "with classic lime and slate character. Exceptional aging potential.",
    price_trajectory="rising")
VIN(r_clare, 2022, 88, "very_good",
    "Good season with balanced ripeness and acidity. "
    "Fresh, approachable Riesling with bright citrus and mineral freshness.",
    price_trajectory="stable")

print("\n── GROSSET (Clare Valley) ──")
p_grosset = P(
    "Grosset Wines",
    "winery", r_clare, "Australia",
    production_philosophy="Clare Valley's benchmark Riesling producer: Polish Hill and Watervale single-vineyard wines defining Australia's greatest dry Riesling style",
    philosophy_description=(
        "Grosset Wines is Australia's most celebrated Riesling producer — Jeffrey Grosset established his "
        "Clare Valley winery in 1981 with the singular focus of producing Australia's finest dry Riesling. "
        "His two benchmark wines — Polish Hill (intense, mineral, from ancient Silurian slate soils) and "
        "Watervale (richer, more citrus-driven, from limestone and red clay) — define the Clare Valley style "
        "that has influenced Riesling production globally. Grosset was a pioneer of screw cap adoption in "
        "2000 and of hand-harvesting and whole-bunch pressing of Riesling in Australia. The estate also "
        "produces exceptional Pinot Noir and Gaia (Bordeaux blend) from Clare's cooler sub-regions."
    ),
    reputation_narrative=(
        "Jeffrey Grosset is Australia's most acclaimed Riesling producer — Grosset Polish Hill is "
        "consistently ranked by James Halliday (Wine Companion), Wine Advocate, and Decanter among "
        "Australia's greatest white wines, scoring 95-99 in top vintages. The wine is benchmarked "
        "against Germany's greatest GG Rieslings and demonstrates that Clare Valley can produce dry "
        "Riesling of world-class complexity and aging potential. A Six Red Stars winery."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_grosset = PROD(
    "Grosset Polish Hill Riesling Clare Valley",
    "wine_still", p_grosset, r_clare, "Australia",
    subcategory="riesling_clare_valley",
    description=(
        "Grosset Polish Hill is Australia's greatest dry Riesling: from ancient Silurian slate soils on "
        "the steep Polish Hill sub-district, producing wine of extraordinary mineral intensity and longevity. "
        "Pale green-gold with lime zest, slate mineral, white flower, and a striking acidity that grips "
        "the palate. In youth the wine can seem austere — at 5-10 years it develops extraordinary complexity "
        "with kerosene, toast, and preserved citrus layers over the mineral spine. "
        "Australia's benchmark for Riesling aging potential."
    ),
    price_tier="premium"
)
PAIR(prod_grosset,
    "Panfried trout with lemon butter, capers, and dill",
    "complement", "classic", "fish_course",
    "Grosset Polish Hill's lime-mineral intensity and laser-sharp acidity achieves the classic "
    "Clare Valley fish pairing — freshwater trout with lemon butter. The wine's slate mineral "
    "bridges the fish's delicate flavour; lemon amplifies the Riesling's citrus character; "
    "capers provide salt that the wine's acidity integrates. A pairing that demonstrates "
    "why dry Clare Riesling is Australia's most versatile and food-compatible white wine.")
PAIR(prod_grosset,
    "Thai green curry with prawns and jasmine rice",
    "complement", "established", "main",
    "Grosset Polish Hill's high-acidity and lime character is the ideal foil for Thai green curry — "
    "the wine's citrus intensity amplifies the lime leaf in the curry paste; the slate mineral "
    "refreshes between spice-forward mouthfuls; the residual-sugar hint at young vintages "
    "bridges the chilli's heat. A pairing that reveals why Clare Riesling succeeds with Asian "
    "cuisine as well as German Spätlese, but with a distinctly Australian lime character.")

print("\n── JIM BARRY WINES (Clare Valley) ──")
p_jimbarry = P(
    "Jim Barry Wines",
    "winery", r_clare, "Australia",
    production_philosophy="Clare Valley's most acclaimed red wine producer: The Armagh Shiraz — Australia's most age-worthy single-vineyard Shiraz alongside Grange and Hill of Grace",
    philosophy_description=(
        "Jim Barry Wines is Clare Valley's most important red wine estate — founded in 1959 by Jim Barry, "
        "one of South Australia's first trained oenologists. The estate's crown jewel is The Armagh: a "
        "single-vineyard Shiraz from 30+ year old dry-grown vines on Clare's distinctive red Cambrian clay "
        "over limestone — a wine first produced in 1985 that has become one of Australia's most collectible "
        "icons. Unlike Barossa Shiraz's lush generosity, The Armagh is austere, structured, and mineral "
        "in youth — developing extraordinary iron-mineral and dark berry complexity over 20-30 years. "
        "Clare Valley Shiraz at its most profound."
    ),
    reputation_narrative=(
        "Jim Barry The Armagh is considered by James Halliday, Wine Advocate (Neal Martin), and Decanter "
        "to be one of Australia's three or four greatest Shiraz wines — alongside Penfolds Grange and "
        "Henschke Hill of Grace. The wine consistently scores 95-100 in top vintages and demonstrates "
        "that Clare Valley can produce structured, age-worthy Shiraz of a completely different style "
        "from Barossa's approachable generosity. The estate holds 5 Red Stars (Wine Companion)."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_jimbarry = PROD(
    "Jim Barry The Armagh Shiraz Clare Valley",
    "wine_still", p_jimbarry, r_clare, "Australia",
    subcategory="shiraz_clare_valley",
    description=(
        "The Armagh is Clare Valley's most profound Shiraz: a single-vineyard wine from 30+ year old "
        "dry-grown Shiraz vines on red Cambrian clay over limestone. Deep violet-black with extraordinary "
        "concentration: blackberry, iron ore, graphite, dark chocolate, pepper, and a mineral austerity "
        "that distinguishes Clare Shiraz from Barossa's more generous expressions. "
        "The wine requires 15-20 years' aging for full expression — at 25 years, The Armagh achieves "
        "complexity that rivals the greatest Northern Rhône Syrah. Exceptional and very limited."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_jimbarry,
    "Braised short rib with red wine jus and celeriac remoulade",
    "complement", "established", "main",
    "Jim Barry The Armagh's iron-mineral austerity and concentrated dark fruit demands the richest "
    "protein treatment — short rib braised to collagen richness. The wine's structured Clare Shiraz "
    "character is tamed by the slow-braise's fat while the dark fruit amplifies the red wine jus; "
    "celeriac remoulade provides earthy freshness that echoes The Armagh's mineral spine. "
    "A pairing of Australia's most structured Shiraz with its natural food match.")
PAIR(prod_jimbarry,
    "Kangaroo loin with native pepper berry, wattleseed, and bush tomato",
    "complement", "adventurous", "main",
    "Jim Barry The Armagh's Clare Valley iron-mineral Shiraz and Australian terroir character "
    "achieves its most indigenous expression with kangaroo — a lean, intensely flavoured game "
    "protein that mirrors the wine's mineral-dark fruit concentration. Native pepper berry echoes "
    "the Shiraz's peppery character; wattleseed provides the earthy nuttiness the wine's mineral "
    "complexity demands; bush tomato adds sweet-acid balance. A pairing of complete Australian identity.")

# ═══════════════════════════════════════════════════════════════════════════════
# COONAWARRA — Australia's Greatest Cabernet Sauvignon Region
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── COONAWARRA — NEW REGION ──")
r_coonawarra = R(
    "Coonawarra",
    "Australia",
    "wine",
    designation_type="GI",
    designation_name="Coonawarra GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Coonawarra is Australia's most celebrated Cabernet Sauvignon region — a narrow, flat strip "
        "of terra rossa (iron-rich red clay over ancient Jurassic limestone) in South Australia's "
        "far southeast Limestone Coast zone. The 15km by 2km terra rossa cigar is the most precisely "
        "defined premium wine terroir in Australia: the red clay-over-limestone combination produces "
        "Cabernet Sauvignon of extraordinary depth, structure, and eucalyptus-mint character that is "
        "distinctively Coonawarra. The region's cool maritime climate (moderated by Bass Strait) "
        "provides natural acid retention and extended hang time, producing wines that age beautifully "
        "for 20-30+ years from exceptional vintages."
    ),
    key_producers="Wynns Coonawarra Estate, Balnaves, Majella, Parker Coonawarra Estate, Penley Estate, Bowen Estate",
    historical_context=(
        "Coonawarra was first planted in 1891 by Scottish emigrant John Riddoch, who established the "
        "Riddoch Estate Winery on the terra rossa. The region's potential was not fully realised until "
        "Wynns acquired the estate in 1951 and began producing what became Australia's benchmark "
        "Cabernet Sauvignon. The 'terra rossa over limestone' story became Australia's most compelling "
        "terroir narrative — the visible red soil boundary is as stark as Burgundy's vineyard walls "
        "in its definition of wine quality."
    )
)

print("\n  Adding Coonawarra vintages...")
VIN(r_coonawarra, 2015, 90, "excellent",
    "Well-balanced season with consistent rainfall and moderate temperatures. "
    "Elegant, structured Cabernet with good acid retention and classic eucalyptus character.",
    price_trajectory="stable")
VIN(r_coonawarra, 2016, 88, "very_good",
    "Slightly warmer conditions with some heat events. Rich, approachable Cabernet "
    "with ripe tannin — drinking well earlier than typical Coonawarra.",
    price_trajectory="stable")
VIN(r_coonawarra, 2017, 95, "exceptional",
    "Outstanding vintage — cool, long ripening season produced Cabernet of extraordinary "
    "structure, mint-eucalyptus character, and aging potential. The benchmark recent vintage.",
    price_trajectory="rising")
VIN(r_coonawarra, 2019, 86, "very_good",
    "Dry, warm vintage with some smoke taint risk from bushfire season. "
    "Careful selection produced good wines despite challenging conditions.",
    price_trajectory="declining")
VIN(r_coonawarra, 2021, 92, "excellent",
    "Return to form after difficult 2019-2020 period. Cool, wet spring followed by perfect "
    "ripening — excellent Cabernet with classic structure and age-worthiness.",
    price_trajectory="rising")

print("\n── WYNNS COONAWARRA ESTATE (Coonawarra) ──")
p_wynns = P(
    "Wynns Coonawarra Estate",
    "winery", r_coonawarra, "Australia",
    production_philosophy="Coonawarra's founding estate: Australia's most important Cabernet Sauvignon producer from 200+ hectares of prime terra rossa terroir",
    philosophy_description=(
        "Wynns Coonawarra Estate is Australia's most important Cabernet Sauvignon producer — holding "
        "200+ hectares of the finest Coonawarra terra rossa in a single contiguous estate. The three-gabled "
        "winery is the most recognisable symbol of Coonawarra wine. Their range spans from the accessible "
        "estate Cabernet to the John Riddoch (ultra-premium, old-vine, single-vineyard selection) and the "
        "Michael Shiraz. Wynns exemplifies how Australian wine can achieve complexity and age-worthiness "
        "from a single region with distinctive terroir. Chief winemaker Sue Hodder's precision viticulture "
        "and winemaking has elevated quality to consistently 96-100 point territory."
    ),
    reputation_narrative=(
        "Wynns Coonawarra Estate is consistently ranked by James Halliday (5 Red Stars, Wine Companion) "
        "and Wine Advocate as one of Australia's most important producers. The John Riddoch Cabernet scores "
        "96-100 in exceptional vintages and is considered Australia's finest Coonawarra expression. "
        "Sue Hodder is Wine Advocate's Australian Winemaker of the Year 2021. Wynns demonstrates that "
        "consistency, terroir, and technical precision can produce world-class Cabernet from the terra rossa."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_wynns = PROD(
    "Wynns John Riddoch Cabernet Sauvignon Coonawarra",
    "wine_still", p_wynns, r_coonawarra, "Australia",
    subcategory="cabernet_sauvignon_coonawarra",
    description=(
        "Wynns John Riddoch is Coonawarra's most celebrated Cabernet Sauvignon: a selection of the estate's "
        "finest old-vine terra rossa blocks, made only in the best vintages. Deep ruby-garnet with classic "
        "Coonawarra character: blackcurrant, eucalyptus, mint, graphite, cedar, and the distinctive "
        "iron-oxide mineral of the terra rossa. The wine has extraordinary structure and requires 10-20 "
        "years' aging — at 20 years, John Riddoch rivals Cabernet from the world's greatest producers. "
        "Named in honour of Coonawarra's founder."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_wynns,
    "Grilled T-bone with herb butter, broccolini, and potato cake",
    "complement", "classic", "main",
    "Wynns John Riddoch's Coonawarra Cabernet — with its blackcurrant and eucalyptus character "
    "and firm terra rossa mineral tannin — achieves the most classic Australian steak pairing. "
    "The T-bone's combination of sirloin and fillet provides both richness and leanness that "
    "bridges the wine's structural complexity; herb butter integrates the tannin; broccolini's "
    "slight bitterness bridges the Cabernet's eucalyptus note. Classic Australian wine at its best.")
PAIR(prod_wynns,
    "Slow-braised lamb shoulder with garlic, rosemary, and white bean",
    "complement", "established", "main",
    "John Riddoch's structured Coonawarra Cabernet achieves a compelling harmony with slow-braised "
    "lamb — the classic Cabernet-lamb affinity demonstrated at its most austere and mineral Australian "
    "expression. The lamb's rendered fat softens the terra rossa tannin; rosemary bridges the wine's "
    "eucalyptus-herb dimension; white beans provide the earthy protein base the Cabernet's structure "
    "integrates into. A pairing of complete Coonawarra identity.")

print("\n── BALNAVES OF COONAWARRA (Coonawarra) ──")
p_balnaves = P(
    "Balnaves of Coonawarra",
    "winery", r_coonawarra, "Australia",
    production_philosophy="Family Coonawarra estate: biodynamic terra rossa viticulture producing The Tally — the region's most allocated reserve Cabernet",
    philosophy_description=(
        "Balnaves of Coonawarra is a family-owned estate founded in 1975 by Doug Balnaves on 58 hectares "
        "of prime Coonawarra terra rossa. The estate's crown jewel is The Tally — a single-vineyard, "
        "old-vine Cabernet Sauvignon made only in exceptional vintages from vines planted in 1975. "
        "Winemaker Pete Bissell crafts the wine with minimal intervention: hand-harvesting, open-ferment "
        "with extended maceration, and aging in 100% French Barriques for 18 months. The Tally has "
        "become one of Coonawarra's most sought-after and limited wines — demonstrating that family-scale "
        "production with exceptional site specificity can rival Wynns' scale advantage."
    ),
    reputation_narrative=(
        "Balnaves The Tally is cited by James Halliday (5 Red Stars) and Wine Advocate as one of "
        "Coonawarra's essential expressions — a single-vineyard, old-vine Cabernet that rivals John Riddoch "
        "in quality while demonstrating the personal, family-scale character that distinguishes it from "
        "the larger estate wines. Scoring 95-98 in exceptional vintages, The Tally is Coonawarra's most "
        "allocated collector's wine alongside Wynns John Riddoch."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_balnaves = PROD(
    "Balnaves The Tally Reserve Cabernet Sauvignon Coonawarra",
    "wine_still", p_balnaves, r_coonawarra, "Australia",
    subcategory="cabernet_sauvignon_coonawarra",
    description=(
        "Balnaves The Tally is Coonawarra's most personal icon: old-vine Cabernet Sauvignon from the "
        "1975 estate vines on prime terra rossa, made only in the best vintages. Intense ruby-garnet "
        "with blackcurrant, cassis, mint-eucalyptus, dark chocolate, and the iron-mineral precision "
        "of Coonawarra's finest blocks. The wine has a seamless texture that distinguishes it from "
        "Wynns' more structured approach — generous but structured, with 15-25 years' aging potential. "
        "Production is extremely limited: typically under 1,000 cases per vintage."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_balnaves,
    "Roasted prime rib with bordelaise sauce and potato dauphinoise",
    "complement", "classic", "main",
    "Balnaves The Tally's seamless Coonawarra Cabernet texture and blackcurrant depth achieves "
    "the ultimate fine dining beef pairing — prime rib roasted on the bone. The bone's marrow "
    "enriches the wine-beef interaction; bordelaise sauce bridges Coonawarra's Bordeaux aspirations; "
    "potato dauphinoise provides the rich starchy base The Tally's structured tannin requires. "
    "A pairing that positions Coonawarra at the international Cabernet fine dining table.")
PAIR(prod_balnaves,
    "Roasted duck with cherry jus and celeriac purée",
    "complement", "established", "main",
    "Balnaves The Tally's Coonawarra Cabernet—with its blackcurrant richness and mint-eucalyptus "
    "freshness—achieves an elegant harmony with roasted duck. The wine's generous texture bridges "
    "the duck's richness while the mint character lifts the cherry jus's sweetness; celeriac purée "
    "provides earthy balance. A pairing that demonstrates Coonawarra Cabernet's versatility "
    "beyond the classic beef-red wine dialogue.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T18 Batch 1 complete.")
print("  Clare Valley: new region, 5 vintages, 2 producers (Grosset, Jim Barry), 2 products, 4 pairings")
print("  Coonawarra: new region, 5 vintages, 2 producers (Wynns, Balnaves), 2 products, 4 pairings")
