#!/usr/bin/env python3
"""Terminal 12 — Batch 2: Jura + Bandol + Casablanca Valley (new regions)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, description, key_producers,
      designation_type=None, designation_name=None, reputation_tier="prestigious",
      quality_trajectory="established", historical_context=None):
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

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ═══════════════════════════════════════════════════════════════════════════
# JURA — FRANCE (NEW REGION)
# ═══════════════════════════════════════════════════════════════════════════
print("=== JURA — FRANCE (NEW REGION) ===")

JURA = R("Jura", "France", "wine",
    description="France's most distinctive wine region — the Jura plateau between Burgundy and the Swiss Alps produces the world's only Vin Jaune (yellow wine) from Savagnin grape, oxidatively aged under a film of yeast (voile) for a minimum 6 years 3 months in barrels that are never topped up. The resulting wine — bottled in the unique 62cl clavelin — resembles dry Fino Sherry in its oxidative character but with French terroir complexity. Poulsard and Trousseau red grapes, Chardonnay, and the rare Savagnin white complete Jura's unique palette. Ouillé (non-oxidative) Chardonnay from Jura — the 'ouillé' style — is one of France's greatest white wine values.",
    key_producers="Henri Maire, Jacques Puffeney, Domaine Ganevat, Emmanuel Houillon-Overnoy, Château d'Arlay",
    designation_type="AOC",
    designation_name="Côtes du Jura, Arbois, Château-Chalon, L'Étoile",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    historical_context="Jura wine has been produced since Roman times. Pasteur discovered fermentation while studying Jura wines at his home in Arbois. Château-Chalon is the most prestigious Jura appellation — Vin Jaune from the chalky-clay Château-Chalon plateau is the definitive expression of the style.")

print(f"Jura region ID: {JURA}")

houillon = P("Emmanuel Houillon-Overnoy", "winery", JURA, "France",
    production_philosophy="Pure Jura expression — no sulphur, biodynamic, the most sought-after Jura wines",
    philosophy_description="Emmanuel Houillon inherited the Overnoy domaine from Pierre Overnoy — the founding father of natural wine in Jura. The Houillon-Overnoy wines are made without any sulphur addition at any stage: the result, in optimal vintages, is Poulsard, Trousseau, and Chardonnay of crystalline purity. Allocated exclusively to long-term clients; the estate's wines are among the world's most sought-after natural wines.",
    key_personnel=[{"name": "Emmanuel Houillon", "role": "Owner/Winemaker"}],
    production_details={"philosophy": "zero sulphur, biodynamic farming", "grapes": "Poulsard, Trousseau, Chardonnay", "allocation": "mailing list only"},
    reputation_narrative="Houillon-Overnoy is the most influential and sought-after Jura producer — the estate's zero-sulphur philosophy and natural winemaking approach established Jura as a pilgrimage destination for natural wine sommeliers globally. The wines are extraordinarily rare and allocated internationally.",
    price_positioning="ultra_premium")

PROD("Houillon-Overnoy Arbois Poulsard", "wine_still", houillon, JURA, "France",
    subcategory="poulsard_jura",
    description="The most sought-after natural wine from Jura's pioneer estate — zero sulphur, biodynamic Poulsard from old vines in Arbois. Pale orange-red (almost rosé in colour); pure and ethereal: red cherry, rose hip, dried cranberry, orange peel, and chalky mineral. The most extreme natural wine of the traditional Jura style — crystalline purity that ages extraordinarily well. Allocated to international mailing list; one of the world's most coveted natural wines.",
    price_tier="ultra_premium")

ganevat = P("Domaine Ganevat", "winery", JURA, "France",
    production_philosophy="Jura's most prolific single-vineyard program — 40+ bottlings from the Côtes du Jura plateau",
    philosophy_description="Jean-François Ganevat produces the most site-specific wines of the Jura: 40+ individual vineyard and varietal bottlings that map the Côtes du Jura's extraordinary diversity. The Julien's et Julien's — named for the two Juliens — is the cornerstone; the Mémorial dedicated to Ganevat's father in Burgundy demonstrates the estate's emotional depth. Biodynamic farming; wild yeast; no fining or filtration.",
    key_personnel=[{"name": "Jean-François Ganevat", "role": "Owner/Winemaker"}],
    production_details={"number_of_wines": "40+ individual bottlings", "viticulture": "biodynamic", "grapes": "full Jura range including Jaubertes and Savagnin"},
    reputation_narrative="Domaine Ganevat is considered Jura's most intellectually ambitious producer — the 40+ single-vineyard bottlings have mapped the Côtes du Jura terroir in a manner comparable to a Burgundy domaine. Ganevat is consistently among France's most discussed and sought-after natural wine producers.",
    price_positioning="ultra_premium")

PROD("Ganevat Cuvée Julien Chardonnay", "wine_still", ganevat, JURA, "France",
    subcategory="chardonnay_jura_ouille",
    description="One of Jura's landmark Chardonnay expressions — the ouillé (non-oxidative) style from old-vine Chardonnay on the Côtes du Jura blue and grey clay. Wild fermentation; aged under controlled conditions in old barrels; unfined, unfiltered. Lemon curd, white peach, hazelnut, and the characteristic Jura mineral tension from chalky-clay soils. At its best, rivals village Meursault in depth and complexity at a fraction of the price. One of France's greatest undervalued white wines.",
    price_tier="ultra_premium")

puffeney = P("Jacques Puffeney", "winery", JURA, "France",
    production_philosophy="Arbois master — Vin Jaune and Trousseau from the traditional Jura school",
    philosophy_description="Jacques Puffeney (retired 2014, now produced by Bénédicte and Stéphane Tissot) was the greatest traditional-style Arbois producer — his Vin Jaune and Savagnin were the benchmarks for the oxidative Jura style. The Tissot family continues the Puffeney legacy with the same old vineyards in Arbois.",
    key_personnel=[{"name": "Bénédicte Tissot", "role": "Continuation/Winemaker"}],
    production_details={"estate": "Arbois appellation", "flagship": "Vin Jaune", "tradition": "traditional oxidative Savagnin aging"},
    reputation_narrative="Jacques Puffeney was the ambassador of authentic Jura winemaking for 40 years — his Vin Jaune and Trousseau d'Arbois became the reference expressions for traditional Jura. Now continued by the Tissot family with the same vineyards and philosophy.",
    price_positioning="premium")

PROD("Tissot (Puffeney Vineyards) Arbois Vin Jaune", "wine_still", puffeney, JURA, "France",
    subcategory="vin_jaune_arbois",
    description="Jura's most distinctive wine style — Vin Jaune from Savagnin grape aged under a yeast voile (flor) in never-topped barrels for a minimum 6 years 3 months. Bottled in the unique 62cl clavelin. Walnut, curry leaf, dry apricot, miso, and the extraordinary oxidative rancio of Jura's traditional wine. Unlike Sherry: it is aged still, not fortified. One of France's most gastronomically versatile wines — pairs with dishes that defeat Burgundy and Bordeaux (foie gras, mature Comté, curry, lobster bisque).",
    price_tier="premium")

PROD("Tissot Arbois Trousseau", "wine_still", puffeney, JURA, "France",
    subcategory="trousseau_jura",
    description="Jura's indigenous red grape — Trousseau from Arbois. Deeply coloured despite naturally low tannin; iron-mineral, red berry, violet, and the distinctive chalky-clay terroir of Arbois. Aged in old barrels without oxidation (ouillé style). One of France's most original red wines: more structured than Poulsard but lighter than Pinot Noir — the ideal somm's choice for difficult food pairings requiring red wine with fish or offal.",
    price_tier="premium")

# Jura vintages
print("\n=== JURA VINTAGES ===")
V(JURA, 2015, 95, "exceptional",
  "The most celebrated recent Jura vintage: warm, dry summer produced exceptional concentration "
  "in Savagnin, Chardonnay, and both red grapes. The Vin Jaune from 2015 is considered "
  "among the finest of the decade — the high sugar levels produced Vin Jaune of "
  "extraordinary depth and rancio development. Best ouillé Chardonnay in 10 years.",
  "rising", 2022, 2040)

V(JURA, 2017, 92, "excellent",
  "Excellent Jura vintage: early ripening with consistent quality across all varieties. "
  "The Chardonnay shows generous fruit and accessible structure; the Savagnin for Vin Jaune "
  "shows good concentration. Poulsard and Trousseau produced vivid, early-drinking reds.",
  "stable", 2019, 2028)

V(JURA, 2019, 93, "excellent",
  "A beautiful Jura growing season — cool spring followed by warm summer and clean harvest. "
  "The ouillé Chardonnay is at its most mineral and precise. Trousseau shows exceptional "
  "colour and structure. Savagnin for Vin Jaune achieved perfect balance between richness "
  "and natural acidity.",
  "rising", 2021, 2030)

V(JURA, 2021, 91, "excellent",
  "Classic cool Jura vintage: the chalky clay terroir delivered mineral tension and freshness "
  "across all varieties. The Chardonnay is lean and precise — excellent for aging. "
  "Vin Jaune from 2021 will require the full voile period to show its full complexity.",
  "stable", 2027, 2040)

V(JURA, 2022, 92, "excellent",
  "Good Jura vintage with warm conditions: the Chardonnay and Savagnin achieved ripe, "
  "generous characters. Excellent for immediately approachable ouillé styles. The oxidative "
  "wines from 2022 will develop quickly under voile.",
  "stable", 2024, 2030)

# ═══════════════════════════════════════════════════════════════════════════
# BANDOL — PROVENCE, FRANCE (NEW REGION)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== BANDOL — PROVENCE, FRANCE (NEW REGION) ===")

BANDOL = R("Bandol", "France", "wine",
    description="France's most serious red wine appellation on the Mediterranean — the Bandol AOC on the limestone hillsides above the Var coastline requires minimum 50% Mourvèdre, a grape that struggles elsewhere but thrives in Bandol's heat and maritime influence. The result is one of France's most age-worthy red wines: dark, tannic, structured Mourvèdre-based wines that require 10-15 years of development to reveal their extraordinary complexity of olive, dried herb, leather, and dark fruit. Bandol rosé (the 'cru' of Provence rosé) is the definitive gastronomic rosé — deeper, more complex, and more age-worthy than any other Provence rosé.",
    key_producers="Château Pibarnon, Domaine Tempier, Château Pradeaux, Domaine de la Bégude, Château la Rouvière",
    designation_type="AOC",
    designation_name="Bandol AOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    historical_context="Bandol was a major wine port in the 18th century — one of the first French wines exported to America and northern Europe. The AOC was established in 1941. Lulu Peyraud of Domaine Tempier is credited with defining the modern Bandol identity through her advocacy and cooking.")

print(f"Bandol region ID: {BANDOL}")

tempier = P("Domaine Tempier", "winery", BANDOL, "France",
    production_philosophy="Bandol's founding estate — Mourvèdre rediscovered, Provence's most celebrated winery",
    philosophy_description="Lulu and Lucien Peyraud established Domaine Tempier as Bandol's defining estate beginning in the 1950s. Lulu Peyraud's legendary Provençal cooking — documented in Kermit Lynch's Lulu's Provençal Table — made Domaine Tempier the most culinarily connected wine estate in France. The single-vineyard La Tourtine, La Migoua, and Cabassaou bottlings are Bandol's most celebrated expressions.",
    key_personnel=[{"name": "Lulu Peyraud", "role": "Matriarch"}, {"name": "Jean-Marie and François Peyraud", "role": "Current Winemakers"}],
    production_details={"flagship": "La Tourtine, La Migoua, Cabassaou", "varieties": "Mourvèdre dominant, Grenache, Cinsault"},
    reputation_narrative="Domaine Tempier is the most historically celebrated Bandol producer — the estate's association with Lulu Peyraud's legendary Provençal cuisine made it the most culinarily influential French wine estate not in Burgundy or Bordeaux. The Cuvée Classique is the benchmark for understanding Bandol; La Tourtine is the pinnacle.",
    price_positioning="premium")

PROD("Domaine Tempier Bandol Rouge Cuvée Classique", "wine_still", tempier, BANDOL, "France",
    subcategory="mourvedre_bandol_rouge",
    description="The benchmark expression of Bandol AOC red wine — Mourvèdre dominant (60-80%) with Grenache and Cinsault from Domaine Tempier's Castellet estate. Aged 18 months in large old Burgundy barrels. Deep dark colour; dark olive, dried herbs, leather, blackberry, licorice, and the distinctive iron-rich garrigue mineral of Bandol. Requires 8-12 years to integrate its considerable tannin structure. France's most age-worthy Provençal red wine and the reference for Mediterranean Mourvèdre.",
    price_tier="premium")

PROD("Domaine Tempier Bandol Rosé", "wine_still", tempier, BANDOL, "France",
    subcategory="rose_bandol_provence",
    description="The definitive gastronomic Provence rosé — Domaine Tempier's Bandol Rosé from Mourvèdre (40%), Grenache, and Cinsault. Direct press; cold fermentation; no oak. Salmon-orange; white peach, dried herbs, violet, and the distinctive mineral depth that separates Bandol rosé from the pale, neutral styles of generic Provence. Richer, more complex, and more food-friendly than any other Provence rosé — a wine that works with the fish courses and charcuterie that defeat pale rosé. Ages 2-5 years.",
    price_tier="premium")

pibarnon = P("Château Pibarnon", "winery", BANDOL, "France",
    production_philosophy="Bandol's highest terroir — Mourvèdre from 600m altitude limestone plateaux",
    philosophy_description="Château Pibarnon sits at the highest elevation in the Bandol AOC — 300m above the sea on limestone plateaux overlooking the coast near La Cadière d'Azur. The altitude creates a cooler microclimate than other Bandol estates, producing Mourvèdre of remarkable freshness and longevity. The Pibarnon Rouge is consistently considered alongside Domaine Tempier La Tourtine as Bandol's greatest red wine expression.",
    key_personnel=[{"name": "Éric de Saint-Victor", "role": "Owner/Director"}],
    production_details={"altitude": "300m on limestone", "distinction": "highest elevation in Bandol AOC", "Mourvèdre": "90%+ in flagship red"},
    reputation_narrative="Château Pibarnon is Bandol's other great estate alongside Domaine Tempier — the high-altitude limestone terroir produces Mourvèdre of extraordinary structure and longevity. The Pibarnon Rouge at 20 years demonstrates the extraordinary cellarability of the great Bandol estates.",
    price_positioning="premium")

PROD("Château Pibarnon Bandol Rouge", "wine_still", pibarnon, BANDOL, "France",
    subcategory="mourvedre_bandol_rouge",
    description="Château Pibarnon's flagship Bandol Rouge — 90%+ Mourvèdre from high-altitude limestone plateaux at 300m above sea level. Aged 18-24 months in old barrels. The most structured and age-worthy of all Bandol expressions: dark cherry, licorice, black olive, graphite, Provençal garrigue, and iron-mineral limestone. Requires 10-15 years minimum to show its full complexity — at 20 years, rivalling aged Barolo in its complexity and length. France's most underappreciated great red wine.",
    price_tier="premium")

# Bandol vintages
print("\n=== BANDOL VINTAGES ===")
V(BANDOL, 2015, 96, "exceptional",
  "One of the greatest Bandol vintages in a generation: warm, dry Mediterranean summer "
  "produced Mourvèdre of extraordinary concentration and ripeness. The high tannin of "
  "exceptional years requires 15-20 years; the 2015 Bandol Rouge from Tempier and Pibarnon "
  "are already considered legends of the appellation.",
  "rising", 2025, 2045)

V(BANDOL, 2017, 93, "excellent",
  "An excellent, accessible Bandol vintage — warm conditions produced approachable Mourvèdre "
  "with more immediate charm than the structured 2015. The rosé is exceptional; the rouge "
  "will drink well from year 8-20. Good expression of Bandol's Mediterranean character.",
  "stable", 2022, 2035)

V(BANDOL, 2019, 94, "exceptional",
  "Another outstanding Bandol vintage: the Mediterranean climate delivered full Mourvèdre "
  "ripeness with excellent acid balance. The 2019 rouge bottlings from Tempier and Pibarnon "
  "are structured and complex — beginning to drink 2024 but best from 2028.",
  "rising", 2026, 2040)

V(BANDOL, 2021, 91, "excellent",
  "Good Bandol vintage — reliable quality across the appellation. The rosé is particularly "
  "successful: aromatic, structured, and complex. The rouge shows good Mourvèdre concentration "
  "and will reward patience.",
  "stable", 2025, 2035)

V(BANDOL, 2022, 92, "excellent",
  "Hot Mediterranean vintage producing generous Bandol rosé of exceptional body and depth. "
  "The rouge shows ripe, concentrated Mourvèdre with a plush approachability unusual for "
  "the appellation. Excellent early drinking (from 2025) without the full power of great years.",
  "stable", 2025, 2033)

# ═══════════════════════════════════════════════════════════════════════════
# CASABLANCA VALLEY — CHILE (NEW REGION)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== CASABLANCA VALLEY — CHILE (NEW REGION) ===")

CASABLANCA = R("Casablanca Valley", "Chile", "wine",
    description="Chile's benchmark cool-climate wine region — the Casablanca Valley between Santiago and the Pacific coast. The maritime influence from the cold Humboldt Current creates growing conditions ideal for Sauvignon Blanc, Chardonnay, and Pinot Noir. Established commercially in the 1980s by Viña Casablanca and Concha y Toro, the valley quickly became Chile's reference for white wine and the country's most credible Pinot Noir zone. The diurnal temperature variation (up to 25°C day-to-night) preserves acid and aromatic freshness.",
    key_producers="Concha y Toro Casillero, Viña Casablanca, William Cole, Kingston Family Vineyards, Amayna",
    designation_type="DO",
    designation_name="Valle de Casablanca DO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    historical_context="Pablo Morandé of Concha y Toro planted the first modern Casablanca Valley vines in 1982. The valley proved immediately superior for white wines and Pinot Noir, establishing a new Chilean wine identity beyond the red-dominated Maipo and Colchagua valleys.")

print(f"Casablanca region ID: {CASABLANCA}")

concha_cas = P("Concha y Toro Casablanca", "winery", CASABLANCA, "Chile",
    production_philosophy="Chile's coolest valley — Pacific influence Chardonnay and Pinot Noir",
    philosophy_description="Concha y Toro's Casablanca Valley operations produce the estate's finest white wines and Pinot Noir — the Marques de Casa Concha Chardonnay and the Terrunyo Sauvignon Blanc demonstrate that Chile's greatest white wine potential lies in the Pacific-influenced cool valleys, not the warmer inland. The winery's research into Casablanca sub-regional terroir has expanded since 2000.",
    key_personnel=[{"name": "Marcelo Papa", "role": "Chief Winemaker"}],
    production_details={"varieties": "Sauvignon Blanc, Chardonnay, Pinot Noir", "influence": "Pacific maritime Humboldt Current"},
    reputation_narrative="Concha y Toro's Casablanca operations have been central to establishing Chile's cool-climate wine identity — the Terrunyo Sauvignon Blanc demonstrated that Chile could produce SB of international class, and the Marques Chardonnay remains the benchmark for the variety in the country.",
    price_positioning="premium")

PROD("Concha y Toro Marques de Casa Concha Chardonnay", "wine_still", concha_cas, CASABLANCA, "Chile",
    subcategory="chardonnay_casablanca",
    description="Chile's benchmark cool-climate Chardonnay — from Casablanca Valley fruit at 250-350m altitude with direct Pacific maritime influence. Whole-cluster pressed; partial fermentation in French oak (30% new); sur lies aging 8 months. White peach, citrus zest, grilled almond, and the characteristic mineral freshness of Casablanca's fog-cooled mornings. The best-value serious Chardonnay in South America — consistently 92-94 points from international critics at premium price.",
    price_tier="premium")

kingston = P("Kingston Family Vineyards", "winery", CASABLANCA, "Chile",
    production_philosophy="Pacific-influenced Casablanca Pinot Noir — Chile's Burgundy equivalent",
    philosophy_description="Carl John Kingston's family has farmed the Casablanca Valley since 1898 — originally cattle ranching, converted to vines in 1990s when the Humboldt Current's cooling influence was understood. Kingston Family produces the most Burgundy-influenced Chilean Pinot Noir: individual vineyard expressions (Alazan, Tobiano, Lucero) from different Casablanca sub-terroirs demonstrate that Chilean Pinot Noir has genuine place-specificity. Biodynamic farming since 2015.",
    key_personnel=[{"name": "Carl John Kingston III", "role": "Owner"}, {"name": "Byron Kosuge", "role": "Consulting Winemaker"}],
    production_details={"viticulture": "biodynamic Casablanca estate", "flagship": "single-vineyard Pinot Noirs (Alazan, Tobiano)", "history": "family farming since 1898"},
    reputation_narrative="Kingston Family Vineyards has been the most internationally discussed Chilean Pinot Noir producer since the early 2010s — the biodynamic estate single-vineyard program has demonstrated that Casablanca Valley Pinot Noir can achieve complexity and site-specificity comparable to cooler Burgundy appellations. Allocated internationally.",
    price_positioning="ultra_premium")

PROD("Kingston Family Alazan Pinot Noir", "wine_still", kingston, CASABLANCA, "Chile",
    subcategory="pinot_noir_casablanca",
    description="Kingston Family's flagship single-vineyard Pinot Noir from the Alazan block — biodynamic Casablanca Valley fruit with Pacific maritime influence. Wild fermentation; whole-bunch inclusion (20%); aged 12 months in French oak (25% new). Red cherry, dried rose petal, orange peel, and the characteristic maritime mineral freshness of Casablanca Pinot. Chile's most internationally celebrated Pinot Noir — consistently compared to premier cru level Burgundy at the price. Allocated globally.",
    price_tier="ultra_premium")

# Casablanca vintages
print("\n=== CASABLANCA VALLEY VINTAGES ===")
V(CASABLANCA, 2015, 94, "exceptional",
  "Outstanding Casablanca vintage: cooler than typical with extended Pacific fog influence "
  "through January. The Chardonnay and Sauvignon Blanc show extraordinary mineral freshness; "
  "Pinot Noir achieved perfect ripeness with preserved acidity. Best year in recent memory "
  "for age-worthy Casablanca whites.",
  "rising", 2017, 2028)

V(CASABLANCA, 2018, 92, "excellent",
  "Good Casablanca vintage with the characteristic maritime influence well-expressed. "
  "The Chardonnay is generous and approachable; Pinot Noir shows good structure and freshness. "
  "The 2018 vintage demonstrates the reliable quality of the Pacific-cooled valley.",
  "stable", 2020, 2026)

V(CASABLANCA, 2020, 93, "excellent",
  "A vintage with ideal conditions for Casablanca's cool-climate varieties: extended fog "
  "influence and moderate temperatures preserved the natural acidity that distinguishes "
  "Casablanca from warmer Chilean valleys. Excellent Pinot Noir and Chardonnay.",
  "stable", 2022, 2028)

V(CASABLANCA, 2021, 91, "excellent",
  "Good standard vintage in Casablanca: the maritime influence delivered consistent quality "
  "across all varieties. The Sauvignon Blanc is particularly successful — fresh, mineral, "
  "and expressive. Reliable year-in, year-out quality from the valley.",
  "stable", 2022, 2027)

V(CASABLANCA, 2022, 93, "excellent",
  "Another strong Casablanca vintage with the Pacific influence well-expressed. The Chardonnay "
  "shows exceptional freshness and citrus precision; Pinot Noir achieved excellent colour "
  "and red fruit intensity. One of the valley's most consistent recent years.",
  "rising", 2023, 2029)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────
print("\n=== PAIRINGS ===")

def get_product(name):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Product not found: {name}")

HOU_POU  = get_product("Houillon-Overnoy Arbois Poulsard")
GAN_CHARD = get_product("Ganevat Cuvée Julien Chardonnay")
VIN_JAUNE = get_product("Tissot (Puffeney Vineyards) Arbois Vin Jaune")
TRO_ARB  = get_product("Tissot Arbois Trousseau")
TEMP_ROU = get_product("Domaine Tempier Bandol Rouge Cuvée Classique")
TEMP_ROS = get_product("Domaine Tempier Bandol Rosé")
PIB_ROU  = get_product("Château Pibarnon Bandol Rouge")
CCT_CHARD = get_product("Concha y Toro Marques de Casa Concha Chardonnay")
KING_ALA = get_product("Kingston Family Alazan Pinot Noir")

# Jura pairings
PAIR(HOU_POU, "Charcuterie de Jura — comté, morteau saucisse, jambon du Jura",
    "complement", "classic", "casual",
    "Houillon-Overnoy Poulsard's pale, ethereal red berry and chalky mineral character pairs perfectly with the Jura's own charcuterie — the regional affinity is total. Comté cheese, Morteau smoked sausage, and jambon du Jura are the natural partners for Poulsard from the same hillsides.")

PAIR(GAN_CHARD, "Braised morels with Jura cream and fresh tarragon",
    "elevate", "established", "starter",
    "Ganevat Chardonnay's mineral precision and hazelnut-lemon character pairs magnificently with morel mushrooms — the earthy, forested depth of Morchella mirrors the wine's chalky mineral while Jura cream provides the textural richness to match the Chardonnay's weight and complexity.")

PAIR(VIN_JAUNE, "Poulet au Vin Jaune with morels and cream",
    "complement", "classic", "main",
    "The most classic Jura pairing — Poulet au Vin Jaune is literally made with Vin Jaune. The wine's walnut, curry, and oxidative rancio character permeates the cream sauce; the morels amplify the earthiness. A dish that cannot be made without the wine, and cannot be drunk without the dish.")

PAIR(VIN_JAUNE, "Aged Comté (24-36 months) with walnut bread",
    "complement", "classic", "cheese",
    "Vin Jaune and aged Comté — the most famous Jura pairing and one of the world's great cheese and wine combinations. Both develop the same nutty, oxidative character over time (Comté in its cave-aged wheels, Vin Jaune under its voile). Walnut bread amplifies the walnut notes in both.")

PAIR(TRO_ARB, "Pan-fried veal liver with balsamic shallots and sage",
    "complement", "established", "main",
    "Jura Trousseau's iron-mineral, red fruit character makes it one of France's finest pairings for offal — the wine's natural iron echoes the liver's minerality while the balsamic and sage provide the acidity and herb character that bridge the wine's savoury depth.")

# Bandol pairings
PAIR(TEMP_ROU, "Slow-roasted leg of lamb with Provençal herbs and ratatouille",
    "complement", "classic", "main",
    "The most classic Bandol pairing: Mourvèdre-based Bandol Rouge and Mediterranean herb-roasted lamb. The wine's dark olive, dried herb, and leather character mirrors Provençal thyme, rosemary, and bay; ratatouille's sweet-savoury character provides the vegetable depth to complement the wine's structured complexity.")

PAIR(TEMP_ROU, "Daube de boeuf Provençale with black olives and orange peel",
    "complement", "classic", "main",
    "The Provençal beef daube and Bandol Rouge: a pairing documented in Lulu Peyraud's legendary Provençal table. The wine's dark olive and leather character is literally echoed in the daube's ingredients; the orange peel amplifies the wine's orange-tinged garrigue note. One of France's great regional wine-and-food pairings.")

PAIR(TEMP_ROS, "Grilled rouget (red mullet) with olive tapenade and fennel",
    "complement", "classic", "main",
    "Domaine Tempier Bandol Rosé's Mediterranean depth and white peach-mineral character pairs perfectly with rouget — the fish's delicate sweetness and Mediterranean character mirrors the wine's Provençal origins. Olive tapenade and fennel amplify the wine's distinctive olive and anise notes.")

PAIR(TEMP_ROS, "Bouillabaisse with rouille and croutons",
    "complement", "classic", "main",
    "The most Provençal pairing imaginable: Bandol Rosé and bouillabaisse. The wine's structure and complexity is one of the few rosés that can hold against the rich saffron broth and rouille garlic intensity. Tempier Rosé's body and depth were designed for this pairing — the definitive expression of Provence's gastronomic tradition.")

PAIR(PIB_ROU, "Lamb shoulder slow-braised with black olive tapenade and anchovies",
    "elevate", "established", "main",
    "Château Pibarnon's high-altitude limestone Mourvèdre creates the most structured Bandol experience — the extraordinary tannin and dark fruit needs the richest lamb preparations to integrate. Anchovy and olive tapenade amplify the wine's characteristic Mediterranean olive and iron-mineral character.")

# Casablanca pairings
PAIR(CCT_CHARD, "Roasted half chicken with leek fondue and mushroom sauce",
    "complement", "established", "main",
    "Concha y Toro Marques Chardonnay's fresh acidity and almond-citrus character pairs naturally with roasted chicken — the wine's cool-climate precision is more food-friendly than warmer-climate Chardonnay. Leek fondue mirrors the wine's lees richness; mushroom sauce adds the earthy depth the Casablanca terroir can handle.")

PAIR(KING_ALA, "Pan-roasted duck breast with cherry sauce and potato gratin",
    "complement", "classic", "main",
    "Kingston Family Alazan's maritime Casablanca Pinot Noir pairs classically with duck — the red cherry and rose petal character mirrors the cherry sauce preparation while potato gratin provides the neutral starchy base for the wine's mineral freshness to shine against.")

cur.close()
conn.close()
print("\n✅ Terminal 12 Batch 2 — Jura + Bandol + Casablanca complete.")
