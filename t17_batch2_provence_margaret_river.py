#!/usr/bin/env python3
"""Terminal 17 — Batch 2: Provence wine products + Margaret River (new region)
Fills the major gap: Provence has 0 wine products despite being France's
most important rosé region. Also adds Margaret River (Australia).
"""
import psycopg2
import json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    """Insert or return existing beverage_region id."""
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

print("=== T17 BATCH 2: PROVENCE WINE + MARGARET RIVER (NEW REGION) ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# PROVENCE (region 159) — WINE PRODUCTS
# France's most important rosé region: 0 wine products currently
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── CHÂTEAU D'ESCLANS (Provence, region 159) ──")
p_esclans = P(
    "Château d'Esclans",
    "winery", 159, "France",
    production_philosophy="Creator of the premium Provence rosé category: Sacha Lichine's estate producing Garrus — the world's most ambitious rosé",
    philosophy_description=(
        "Château d'Esclans was purchased by Sacha Lichine in 2006 with the singular ambition of creating "
        "the world's finest rosé. Working with Michel Rolland, Lichine transformed this Côtes de Provence "
        "estate into the benchmark for premium Provençale rosé — demonstrating that the category could "
        "achieve luxury wine status. Their Garrus cuvée is made from 80+ year old Grenache and Rolle vines, "
        "fermented and aged in new Burgundy barrique — the only Provence rosé to receive this treatment. "
        "The result is a wine of extraordinary texture, complexity, and aging potential that changed the "
        "global perception of rosé wine permanently."
    ),
    reputation_narrative=(
        "Château d'Esclans' Garrus is cited by Wine Spectator, Decanter, and Wine Advocate as the world's "
        "most important luxury rosé — the wine that proved Provence rosé could command Grand Cru white "
        "Burgundy pricing. Consistently scoring 93-97, Garrus challenged the notion that rosé is a simple "
        "summer wine and elevated the entire Provence category. The estate's success spawned a global "
        "premium rosé revolution."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_garrus = PROD(
    "Château d'Esclans Garrus Côtes de Provence Rosé",
    "wine_still", p_esclans, 159, "France",
    subcategory="rosé_grenache_rolle",
    description=(
        "Garrus is the world's most celebrated luxury rosé: old-vine Grenache (80+ years) and Rolle "
        "from Château d'Esclans' finest parcels, fermented and aged in new Burgundy barrique. "
        "Pale salmon with extraordinary complexity: white peach, citrus blossom, minerality, cream, "
        "and a subtle vanilla from the oak. The wine has a texture and depth that no other Provence "
        "rosé approaches. Ages beautifully over 5-10 years. The wine that redefined luxury rosé."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_garrus,
    "Lobster thermidor with gratin and baby fennel",
    "elevate", "established", "main",
    "Château d'Esclans Garrus's oak-aged complexity and white peach depth achieves what no other "
    "rosé can — elevating the luxury seafood pairing to Grand Cru Burgundy levels. The wine's "
    "creamy texture from barrel aging bridges lobster thermidor's béchamel richness; fennel "
    "amplifies the Rolle's aromatic dimension; the wine's structured acidity cuts through the gratin. "
    "A pairing that positions Provence rosé as a genuine fine dining luxury wine.")
PAIR(prod_garrus,
    "Pan-seared sea bream with Provençale ratatouille and tapenade",
    "complement", "classic", "fish_course",
    "Garrus's complex Provence character and white peach aromatics finds its most regional expression "
    "with sea bream and traditional ratatouille — the wine's oak-textured depth stands up to the "
    "dish's Mediterranean richness; tapenade bridges the wine's Grenache savouriness; ratatouille's "
    "vegetable complexity echoes the wine's aromatic Provençale character. A pairing of extraordinary "
    "Provence regional identity.")

print("\n── CHÂTEAU MIRAVAL (Provence, region 159) ──")
p_miraval = P(
    "Château Miraval",
    "winery", 159, "France",
    production_philosophy="Luxury Provence rosé from the Luberon hills: a historic estate revitalised by Brad Pitt and Quentin Perrin of Familles Perrin",
    philosophy_description=(
        "Château Miraval is a 500-hectare organic estate in the Luberon hills of Provence, owned by Brad Pitt "
        "and run in partnership with the Perrin family (Château de Beaucastel). The Perrins brought their "
        "Châteauneuf-du-Pape expertise to Miraval's terroir: organic viticulture, careful selection of "
        "Cinsault, Grenache, Syrah, and Rolle for the rosé blend, and a winemaking approach that maximises "
        "freshness and mineral precision. The result is a benchmark Côtes de Provence rosé with certified "
        "organic credentials and extraordinary consistent quality at its price point."
    ),
    reputation_narrative=(
        "Château Miraval is one of the world's best-selling luxury rosé brands — consistently scoring 91-93 "
        "from Wine Spectator and Decanter, and cited as the best-value premium Provence rosé for sommeliers. "
        "The Perrin family's involvement lends credibility that the celebrity ownership alone could not achieve. "
        "Their 'Studio by Miraval' and prestige cuvées demonstrate the estate's range from everyday premium "
        "to collector-level Provence rosé."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_miraval = PROD(
    "Château Miraval Côtes de Provence Rosé",
    "wine_still", p_miraval, 159, "France",
    subcategory="rosé_grenache_cinsault",
    description=(
        "Château Miraval is Provence rosé at its most precise and mineral: organically farmed Cinsault, "
        "Grenache, Syrah, and Rolle from the Luberon hills, vinified with the Perrin family's precision. "
        "Pale salmon-pink with white peach, citrus, rose petal, and a distinctive mineral freshness "
        "from the estate's limestone-dominated terroir. The wine is dry, elegant, and refreshing — "
        "one of Provence's most consistent expressions at premium price point."
    ),
    price_tier="premium"
)
PAIR(prod_miraval,
    "Grilled whole fish with herbs and lemon butter",
    "complement", "classic", "fish_course",
    "Château Miraval's mineral freshness and white peach character is the natural companion for "
    "grilled whole fish — the wine's Provençale precision bridges the fish's natural sweetness "
    "while the citrus character amplifies the lemon butter. The Cinsault's light structure "
    "prevents the pairing from becoming heavy; the wine's mineral length echoes the Luberon's "
    "limestone. A Provence fish and rosé pairing of effortless regional harmony.")
PAIR(prod_miraval,
    "Salade Niçoise with tuna, olives, and anchovies",
    "complement", "classic", "starter",
    "Château Miraval Rosé's mineral acidity and white peach character achieves the most iconic "
    "Provençale rosé pairing — Salade Niçoise. The wine's freshness amplifies the tuna's clean "
    "flavour; olive bitterness bridges the wine's mineral character; anchovies provide salt-umami "
    "that the wine's acidity balances. A pairing that captures why Provence rosé exists: "
    "the food and wine of the Côte d'Azur in complete harmony.")

print("\n── DOMAINE OTT (Provence, region 159) ──")
p_ott = P(
    "Domaine Ott",
    "winery", 159, "France",
    production_philosophy="Provence's most prestigious traditional rosé maison: century-old estates producing Château de Selle and Clos Mireille — the original fine-dining Provence rosés",
    philosophy_description=(
        "Domaine Ott is Provence's most historic fine rosé producer — Marcel Ott purchased Château de Selle "
        "in 1912, establishing the foundation for what became Provence rosé's most enduring luxury brand. "
        "Three estates (Château de Selle, Clos Mireille, Château Romassan) span Provence's diverse terroirs: "
        "limestone, clay-limestone, and schist. Their winemaking is precisely traditional: whole-cluster "
        "pressing, temperature-controlled fermentation, and no fining or filtration — preserving the "
        "terroir's mineral character. Domaine Ott rosés were served at the finest Côte d'Azur restaurants "
        "decades before Provence rosé became internationally fashionable."
    ),
    reputation_narrative=(
        "Domaine Ott is considered by Decanter and the French wine press to be Provence's most historically "
        "important rosé producer — their iconic bottle shape (the amphora flask) became the visual symbol "
        "of luxury Provence rosé. The estate was acquired by Champagne Louis Roederer in 2004, bringing "
        "precision investment to both viticulture and winemaking. Consistently scoring 91-94, Château de "
        "Selle Coeur de Grain is cited as Provence's most food-versatile rosé for serious restaurant lists."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_ott = PROD(
    "Domaine Ott Château de Selle Rosé Côtes de Provence",
    "wine_still", p_ott, 159, "France",
    subcategory="rosé_grenache_cinsault_syrah",
    description=(
        "Domaine Ott's Château de Selle is Provence's most historically prestigious rosé: Grenache, "
        "Cinsault, and Syrah from limestone-clay terroir at 400m altitude in the Var. The iconic "
        "amphora bottle contains a wine of genuine complexity: dry, mineral, and aromatic with "
        "wild strawberry, pink grapefruit, garrigue, and a distinctive saline mineral finish. "
        "The wine has exceptional food versatility — one of Provence's most structured rosés, "
        "developing additional complexity over 3-5 years."
    ),
    price_tier="premium"
)
PAIR(prod_ott,
    "Bouillabaisse with rouille, croutons, and gruyère",
    "complement", "classic", "main",
    "Domaine Ott Château de Selle's structured, mineral character is Provence's natural pairing "
    "for bouillabaisse — the wine's saline garrigue depth bridges the saffron-scented fish broth; "
    "rouille's garlic-pepper intensity is cut by the wine's acidity; the wine's structure supports "
    "the seafood medley's complexity. The pairing defines why Provence created structured rosé: "
    "for the region's great fish stew.")
PAIR(prod_ott,
    "Roasted Provençale chicken with olives, tomatoes, and herbes de Provence",
    "complement", "established", "main",
    "Château de Selle's wild strawberry and garrigue character finds its most natural food context "
    "with Provençale chicken — the wine's herb-mineral dimension mirrors the herbes de Provence "
    "rub; olive bitterness bridges the wine's saline minerality; roasted tomato's sweetness "
    "amplifies the wine's ripe fruit. A pairing of pure Provençale regional identity that "
    "demonstrates why structured rosé belongs at the fine dining table.")

# ═══════════════════════════════════════════════════════════════════════════════
# MARGARET RIVER — NEW REGION + VINTAGES + PRODUCERS + PRODUCTS
# Australia's finest Chardonnay and Cabernet Sauvignon region
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── MARGARET RIVER — NEW REGION ──")
r_margaret = R(
    "Margaret River",
    "Australia",
    "wine",
    designation_type="GI",
    designation_name="Margaret River GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "Margaret River is Australia's most distinguished wine region for fine table wines — a narrow "
        "peninsula 270km south of Perth in Western Australia, cooled by the Indian and Southern Oceans. "
        "The region produces Australia's greatest Chardonnay and Cabernet Sauvignon: the oceanic climate "
        "creates exceptional natural acidity alongside full phenolic ripeness, producing wines of "
        "extraordinary elegance and longevity. Pioneered in the 1960s by Dr John Gladstones, who "
        "identified the similarity between Margaret River's climate and Bordeaux's maritime conditions, "
        "the region has fulfilled his vision — producing Cabernet blends and Chardonnays that rival "
        "Europe's finest at their best."
    ),
    key_producers="Vasse Felix, Cullen Wines, Leeuwin Estate, Cape Mentelle, Moss Wood, Voyager Estate, Pierro",
    historical_context=(
        "Dr John Gladstones' 1965 research paper identifying Margaret River as ideal wine country "
        "launched one of Australia's most successful wine regions. Tom Cullity planted Vasse Felix in 1967 — "
        "the region's first commercial vineyard. By the 1980s, Leeuwin Estate's Art Series Chardonnay "
        "and Cullen's Diana Madeline Cabernet Merlot had established Margaret River's international "
        "reputation. The region now produces just 3% of Australia's wine but commands 20% of its "
        "premium wine sales — an extraordinary concentration of quality."
    )
)

print("\n  Adding Margaret River vintages...")
VIN(r_margaret, 2015, 92, "excellent",
    "Classic Margaret River season — long, dry summer with moderate Indian Ocean influence. "
    "Exceptional Chardonnay and Cabernet of great elegance and age-worthiness.",
    price_trajectory="rising")
VIN(r_margaret, 2016, 88, "very_good",
    "Slightly warmer vintage with early harvest. Generous, accessible wines with ripe fruit; "
    "Chardonnay particularly successful with good natural acidity.",
    price_trajectory="stable")
VIN(r_margaret, 2017, 94, "exceptional",
    "One of Margaret River's greatest vintages: perfect ripening conditions throughout, "
    "excellent acid retention. Outstanding Cabernet and Chardonnay with exceptional longevity.",
    price_trajectory="rising")
VIN(r_margaret, 2018, 86, "very_good",
    "Warm, dry conditions with some heat stress in January. Well-structured Cabernets; "
    "Chardonnay required careful harvest selection for freshness.",
    price_trajectory="stable")
VIN(r_margaret, 2020, 90, "excellent",
    "La Niña influence brought cooler conditions and good rainfall. Elegant, precise wines "
    "with fine natural acidity — excellent Chardonnay vintage with Chablis-like minerality.",
    price_trajectory="rising")

print("\n── VASSE FELIX (Margaret River) ──")
p_vasse = P(
    "Vasse Felix",
    "winery", r_margaret, "Australia",
    production_philosophy="Margaret River's founding estate: biodynamic viticulture producing the region's most comprehensive portfolio from entry to icon level",
    philosophy_description=(
        "Vasse Felix is Margaret River's founding estate — planted by Dr Tom Cullity in 1967, making it "
        "the first commercial vineyard in the region. Now owned by the Holmes à Court family, the estate "
        "covers 222 hectares of prime Margaret River red gravelly loam and converted to biodynamic "
        "viticulture in 2010 under chief winemaker Virginia Willcock. Their Heytesbury Chardonnay is "
        "the estate's icon: hand-harvested, whole-bunch pressed, fermented in French Burgundy barrique "
        "with indigenous yeasts, and aged 10 months in 40% new oak. The result is Margaret River "
        "Chardonnay of extraordinary precision, length, and mineral complexity."
    ),
    reputation_narrative=(
        "Vasse Felix is considered by James Halliday (5 Red Stars) and Wine Advocate (Neal Martin) to be "
        "one of Australia's most important wineries. Their Heytesbury Chardonnay consistently scores 95-98 "
        "and is placed alongside Giaconda and Leeuwin Art Series as Australia's greatest Chardonnay. "
        "The estate's biodynamic commitment and 50-year history gives it unique authority in Margaret River. "
        "A Wine Companion 'Five Star Winery' for 20 consecutive years."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_vasse = PROD(
    "Vasse Felix Heytesbury Chardonnay Margaret River",
    "wine_still", p_vasse, r_margaret, "Australia",
    subcategory="chardonnay_margaret_river",
    description=(
        "Vasse Felix's Heytesbury Chardonnay is one of Australia's greatest white wines: single-vineyard "
        "Margaret River Chardonnay from biodynamically farmed old-vine blocks, whole-bunch pressed and "
        "fermented in French Burgundy barrique. Pale gold with extraordinary complexity: white peach, "
        "preserved lemon, roasted hazelnut, struck flint mineral, and a cream-textured palate of "
        "great length. The wine has Burgundy's texture combined with Margaret River's natural acid "
        "precision. Ages beautifully over 10-15 years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_vasse,
    "Roasted half lobster with bisque butter and charred leek",
    "elevate", "established", "main",
    "Vasse Felix Heytesbury's extraordinary Chardonnay complexity and struck-flint mineral depth "
    "achieves a compelling elevation with roasted lobster — the wine's hazelnut and cream character "
    "bridges bisque butter's richness; charred leek provides a smoke dimension that echoes the "
    "wine's mineral complexity; the lobster's natural sweetness is amplified by the Chardonnay's "
    "stone fruit. A pairing that positions Margaret River Chardonnay at Australia's highest level.")
PAIR(prod_vasse,
    "Crab and corn velouté with chive crème fraîche",
    "complement", "classic", "starter",
    "Heytesbury Chardonnay's mineral precision and preserved lemon character achieves elegant "
    "harmony with crab velouté — the wine's struck flint mineral bridges the crab's sweetness "
    "while the preserved lemon amplifies the corn's natural sweetness; chive crème fraîche "
    "echoes the wine's herb-cream dimension. A starter pairing of outstanding Chardonnay and "
    "Australian seafood character.")

print("\n── CULLEN WINES (Margaret River) ──")
p_cullen = P(
    "Cullen Wines",
    "winery", r_margaret, "Australia",
    production_philosophy="Margaret River's biodynamic icon: Diana Madeline and Kevin John — Australia's most acclaimed Cabernet and Chardonnay from certified biodynamic viticulture",
    philosophy_description=(
        "Cullen Wines is one of Margaret River's founding estates — planted by Kevin and Diana Cullen "
        "in 1971, now run by their daughter Vanya Cullen with complete biodynamic and bioenergy commitment. "
        "Their Diana Madeline (Cabernet Sauvignon/Merlot) is considered Australia's greatest Bordeaux blend — "
        "named in honour of co-founder Diana Cullen. The estate is Australia's most decorated biodynamic "
        "producer: Demeter certified since 2004, carbon neutral since 2006, and producing wines of "
        "extraordinary terroir expression from a single 49-hectare estate. The wines have power and "
        "complexity that rivals Pauillac at their best."
    ),
    reputation_narrative=(
        "Cullen Wines' Diana Madeline is consistently named by James Halliday (Wine Companion), Wine Advocate, "
        "and Decanter as Australia's finest Cabernet-based wine — their 2010 vintage was awarded 100 points "
        "by James Halliday and is considered a national icon. Vanya Cullen is Australia's most acclaimed female "
        "winemaker. The estate holds 6 Red Stars (Wine Companion) — the highest award. Diana Madeline "
        "regularly fetches Penfolds Grange prices at auction, reflecting its status as Australia's greatest "
        "left-bank inspired wine."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_cullen = PROD(
    "Cullen Diana Madeline Cabernet Sauvignon Merlot",
    "wine_still", p_cullen, r_margaret, "Australia",
    subcategory="cabernet_sauvignon_margaret_river",
    description=(
        "Cullen Diana Madeline is Australia's most revered Cabernet Sauvignon blend: biodynamically farmed "
        "Cabernet Sauvignon with Merlot, Cabernet Franc, Petit Verdot, and Malbec from Cullen's 49-hectare "
        "estate in Wilyabrup. Deep ruby with blackcurrant, bay leaf, dark chocolate, graphite, and the "
        "distinctive dusty red gravelly loam mineral that defines Margaret River's finest Cabernet terroir. "
        "The wine has Pauillac's structural elegance combined with Margaret River's fruit intensity. "
        "Requires 10-20 years aging — exceptional for 25+ years."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_cullen,
    "Dry-aged sirloin on the bone with roasted bone marrow and gratin",
    "complement", "classic", "main",
    "Cullen Diana Madeline's graphite-mineral concentration and structured tannin demands "
    "the purest beef expression — dry-aged sirloin on the bone, where the Maillard char "
    "bridges the wine's dark fruit and the bone marrow's fat richness softens the tannin. "
    "Gratin provides the starchy base Diana Madeline's extraordinary structure requires. "
    "A pairing of Australia's greatest Cabernet with its natural food match.")
PAIR(prod_cullen,
    "Lamb rack with herb crust, jus réduit, and white bean purée",
    "complement", "established", "main",
    "Diana Madeline's Margaret River Cabernet character — with its blackcurrant, graphite, "
    "and bay leaf complexity — achieves a compelling harmony with rack of lamb. The wine's "
    "Bordeaux-like structure mirrors the natural affinity of left-bank Cabernet with lamb; "
    "herb crust bridges the wine's aromatic dimension; white bean purée provides the earthy, "
    "starchy base Diana Madeline's tannin integrates into perfectly.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T17 Batch 2 complete.")
print("  Provence: 3 producers (d'Esclans, Miraval, Ott), 3 products, 6 pairings")
print("  Margaret River: new region, 5 vintages, 2 producers (Vasse Felix, Cullen), 2 products, 4 pairings")
