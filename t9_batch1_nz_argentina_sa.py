#!/usr/bin/env python3
"""Terminal 9 — Batch 1: NZ Wine Depth + Argentina Mendoza + South Africa Swartland"""
import psycopg2, json, sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs (confirmed above)
MARLBOROUGH   = 87
CENTRAL_OTAGO = 88
MENDOZA       = 90
SWARTLAND     = 94
STELLENBOSCH  = 93

# ─── PRODUCER HELPER ────────────────────────────────────────────────────────
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

# ═══════════════════════════════════════════════════════════════════════════
# MARLBOROUGH — NEW ZEALAND SAUVIGNON BLANC + PINOT NOIR
# ═══════════════════════════════════════════════════════════════════════════
print("=== MARLBOROUGH — NEW ZEALAND ===")

greywacke = P("Greywacke Winery", "winery", MARLBOROUGH, "New Zealand",
    production_philosophy="Wild fermentation, minimal intervention Marlborough expression",
    philosophy_description="Kevin Judd founded Greywacke after 25 years as Cloudy Bay's winemaker. The estate pursues wild yeast fermentation and minimal sulphur addition to produce Marlborough wines of exceptional complexity and site fidelity. The Wild Sauvignon uses aged oak and wild fermentation to produce a textured, layered expression entirely unlike conventional Marlborough SB.",
    key_personnel=[{"name": "Kevin Judd", "role": "Founder/Winemaker"}],
    production_details={"fermentation": "Wild yeast (Sauvignon Blanc Wild)", "sulphur": "minimal", "vessels": "aged French oak + stainless"},
    reputation_narrative="Kevin Judd, former Cloudy Bay winemaker, created Greywacke as his personal statement on Marlborough. The Wild Sauvignon Blanc is considered the region's most complex expression — a benchmark for wild-fermented New Zealand SB that has changed the conversation about what Marlborough can produce.",
    price_positioning="premium")

PROD("Greywacke Wild Sauvignon Blanc", "wine_still", greywacke, MARLBOROUGH, "New Zealand",
    subcategory="sauvignon_blanc_wild_ferment",
    description="Kevin Judd's wild-fermented Sauvignon Blanc — fermented in aged French oak barriques and large format barrels with wild yeast. Full malolactic fermentation creates the creamy, complex texture that distinguishes this from conventional Marlborough SB. Dried herbs, wet stone, lanolin, preserved lemon, and white peach with extraordinary texture and length. Ages 5-8 years confidently. One of New Zealand's most complex white wines.",
    price_tier="premium")

PROD("Greywacke Sauvignon Blanc", "wine_still", greywacke, MARLBOROUGH, "New Zealand",
    subcategory="sauvignon_blanc_marlborough",
    description="Kevin Judd's standard release — the benchmark for Greywacke's house style. Cold fermentation in stainless steel preserves the intense passion fruit, grapefruit, gooseberry, cut grass, and fresh herb character of Marlborough. Cleaner and more precise than most Marlborough SB despite minimal intervention. Exceptional focus and length.",
    price_tier="mid_range")

dog_point = P("Dog Point Vineyard", "winery", MARLBOROUGH, "New Zealand",
    production_philosophy="Biodynamic viticulture; honest, site-expressive Marlborough",
    philosophy_description="James Healy and Ivan Sutherland (former Cloudy Bay winemakers) established Dog Point in 2002 on Marlborough's finest limestone-rich sites. The estate operates biodynamically, viewing the vineyard ecosystem as a unified organism. Section 94, their single-vineyard wine, is made without inoculated yeast or temperature control — one of New Zealand's most authentic terroir expressions.",
    key_personnel=[{"name": "James Healy", "role": "Co-Founder/Winemaker"}, {"name": "Ivan Sutherland", "role": "Co-Founder/Viticulturist"}],
    production_details={"viticulture": "biodynamic", "certification": "Demeter", "vineyards": "limestone Brancott Valley"},
    reputation_narrative="Dog Point is the Marlborough insider's choice: two former Cloudy Bay winemakers farming their own estate biodynamically. Section 94 is considered one of New Zealand's greatest Sauvignon Blancs — with the texture, complexity, and aging potential to rival white Burgundy.",
    price_positioning="premium")

PROD("Dog Point Section 94 Sauvignon Blanc", "wine_still", dog_point, MARLBOROUGH, "New Zealand",
    subcategory="sauvignon_blanc_wild_ferment",
    description="One of New Zealand's greatest white wines — wild fermented in old French oak puncheons from biodynamic estate fruit on limestone Brancott Valley soils. No temperature control, no fining, no filtration. Beeswax, flint, white grapefruit, green apple, oyster shell. The wild fermentation and old oak integration creates almost Burgundian weight alongside characteristic Marlborough purity. Ages 8-12 years confidently.",
    price_tier="premium")

PROD("Dog Point Vineyard Sauvignon Blanc", "wine_still", dog_point, MARLBOROUGH, "New Zealand",
    subcategory="sauvignon_blanc_marlborough",
    description="Estate biodynamic Sauvignon Blanc from limestone Brancott Valley blocks. Cold fermentation in stainless steel preserves the concentrated stone fruit, white peach, and citrus pith character. The limestone soils add a pronounced mineral spine. Impeccably clean and precise, with more weight and presence than typical Marlborough SB.",
    price_tier="mid_range")

seresin = P("Seresin Estate", "winery", MARLBOROUGH, "New Zealand",
    production_philosophy="Biodynamic farming, olive oil and wine from a single integrated estate",
    philosophy_description="Cinematographer Michael Seresin founded this Marlborough estate with a radical commitment: full biodynamic certification across vineyards, olive groves, and orchard. Winemaker Clive Dougall crafts wines of exceptional energy and definition using minimal intervention — including Pinot Noir that has established Marlborough as a serious Pinot region.",
    key_personnel=[{"name": "Michael Seresin", "role": "Founder"}, {"name": "Clive Dougall", "role": "Head Winemaker"}],
    production_details={"viticulture": "biodynamic Demeter", "estate": "olive oil + wine integrated", "fermentation": "wild yeast"},
    reputation_narrative="Seresin Estate has redefined what Marlborough can produce: their Pinot Noirs challenge Central Otago's dominance, and their biodynamic Sauvignon Blanc is among the most energy-filled in the region. A must-know estate for fine dining sommeliers.",
    price_positioning="premium")

PROD("Seresin Leah Pinot Noir", "wine_still", seresin, MARLBOROUGH, "New Zealand",
    subcategory="pinot_noir_marlborough",
    description="Biodynamic Marlborough Pinot Noir from the Southern Valleys sub-region — the coolest, most structured part of Marlborough. Wild fermentation with 20-30% whole-bunch inclusion; 12 months in French oak (30% new); unfined. Dark cherry, dried rose petal, forest floor, and gentle spice. The Southern Valleys fruit delivers more structure and depth than Wairau Valley — a Marlborough Pinot of genuine complexity and elegance. Silky tannins and a long, mineral finish.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# CENTRAL OTAGO — NEW ZEALAND PINOT NOIR
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== CENTRAL OTAGO — NEW ZEALAND ===")

mt_difficulty = P("Mt Difficulty Wines", "winery", CENTRAL_OTAGO, "New Zealand",
    production_philosophy="Bannockburn's volcanic schist terroir — Pinot Noir of power and structure",
    philosophy_description="Mt Difficulty is the flagship producer of Bannockburn, Central Otago's most complex sub-region. The thin volcanic schist soils, continental climate, and extreme diurnal temperature variation create Pinot Noirs of exceptional intensity. Long Gully single-vineyard bottling represents the pinnacle of Bannockburn terroir expression.",
    key_personnel=[{"name": "Matt Dicey", "role": "Chief Winemaker"}],
    production_details={"sub_region": "Bannockburn", "soils": "volcanic schist and loess", "elevation": "280-320m"},
    reputation_narrative="Mt Difficulty Wines has been the benchmark for Bannockburn Pinot Noir since 1998. The estate's Long Gully single-vineyard wine has achieved international recognition as one of Central Otago's great terroir expressions — combining the sub-region's characteristic power with finesse.",
    price_positioning="premium")

PROD("Mt Difficulty Bannockburn Pinot Noir", "wine_still", mt_difficulty, CENTRAL_OTAGO, "New Zealand",
    subcategory="pinot_noir_central_otago",
    description="The flagship expression of Bannockburn, Central Otago's most celebrated sub-region. Hand-picked; 10-15% whole bunch; wild fermentation; 14 months in French oak (30% new). Dark plum, black cherry, cracked pepper, and dried herb with characteristic schist minerality. More structured and intense than Gibbston Valley — built for medium-term aging 5-10 years. Exceptional savory length from volcanic schist soils at 280-320m elevation.",
    price_tier="premium")

PROD("Mt Difficulty Long Gully Single Vineyard Pinot Noir", "wine_still", mt_difficulty, CENTRAL_OTAGO, "New Zealand",
    subcategory="pinot_noir_single_vineyard",
    description="Mt Difficulty's pinnacle single-vineyard expression from oldest schist-soiled vines in Long Gully. Extended maceration 28 days; 18 months in 40% new French oak. Concentrated black cherry, dark chocolate, iron-rich mineral schist, and complex savory depth. Dense and built for a decade of development — comparable in intensity to premier cru Gevrey-Chambertin. Among New Zealand's greatest Pinot Noirs.",
    price_tier="ultra_premium")

rippon = P("Rippon Vineyard", "winery", CENTRAL_OTAGO, "New Zealand",
    production_philosophy="Biodynamic viticulture on Central Otago's oldest vineyard site",
    philosophy_description="Rippon is Central Otago's most historic and romantically situated winery — overlooking Lake Wānaka since 1982. The Muller family farms biodynamically, producing Mature Vine Pinot Noir from their oldest biodynamic blocks. Wines of extraordinary purity and place that have elevated Central Otago's reputation globally.",
    key_personnel=[{"name": "Nicola Muller", "role": "Winemaker"}, {"name": "Lois Muller", "role": "Director"}],
    production_details={"viticulture": "biodynamic Demeter", "site": "lake edge Lake Wānaka", "established": "1974 plantings"},
    reputation_narrative="Rippon is the wine world's most photographed New Zealand vineyard — the lake-edge schist terroir and biodynamic farming produce Pinot Noirs of extraordinary delicacy and complexity. The Mature Vine bottling is considered one of New Zealand's greatest wines and is allocated internationally.",
    price_positioning="ultra_premium")

PROD("Rippon Mature Vine Pinot Noir", "wine_still", rippon, CENTRAL_OTAGO, "New Zealand",
    subcategory="pinot_noir_central_otago",
    description="From biodynamic vines planted 1982-1993 on the schist terraces above Lake Wānaka — New Zealand's most romantically situated vineyard. Wild fermentation; 50% whole bunch; 16 months in aged French oak only (no new oak); unfined and unfiltered. Sublime elegance: red cherry, orange peel, dried rose, iron-rich minerals, and crystalline clarity. Lighter in colour than Bannockburn but extraordinary in texture and length. One of New Zealand's greatest and most allocated wines.",
    price_tier="ultra_premium")

# ═══════════════════════════════════════════════════════════════════════════
# MENDOZA — ARGENTINA MALBEC DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== MENDOZA — ARGENTINA ===")

achaval_ferrer = P("Achaval Ferrer", "winery", MENDOZA, "Argentina",
    production_philosophy="Old-vine Malbec from Argentina's historic high-altitude vineyards",
    philosophy_description="Achaval Ferrer pioneered the single-vineyard, old-vine Malbec movement in Mendoza. Their Finca Altamira (in Altamira, La Consulta) and Finca Bella Vista (Luján de Cuyo) produce from ungrafted, pre-phylloxera Malbec vines planted 1890-1920 — among the oldest in the world. The wines are the benchmark for concentration and typicity of Argentine old-vine Malbec.",
    key_personnel=[{"name": "Santiago Achaval", "role": "Founder"}, {"name": "Roberto Cipresso", "role": "Consulting Winemaker"}],
    production_details={"flagship_vineyards": "Finca Altamira, Finca Bella Vista, Finca Mirador", "vine_age": "up to 130 years", "altitude": "900-1200m"},
    reputation_narrative="Achaval Ferrer's single-vineyard 'Fincas' are Argentina's most celebrated old-vine Malbec expressions — consistently rated 96-100 by Robert Parker and Wine Spectator. They demonstrated that Mendoza's century-old ungrafted vines could rival the world's greatest red wines.",
    price_positioning="ultra_premium")

PROD("Achaval Ferrer Malbec", "wine_still", achaval_ferrer, MENDOZA, "Argentina",
    subcategory="malbec_mendoza",
    description="Estate-level Mendoza Malbec from multiple sites in Luján de Cuyo and Maipú. Aged 14-16 months in French oak (30% new); gravity-fed winery. Dark plum, blackberry, violet, and mocha — plush, velvety texture with soft tannins. The classic Argentine Malbec profile at its most generous and complete. Exceptional quality-to-value for Achaval Ferrer's entry-level expression.",
    price_tier="mid_range")

PROD("Achaval Ferrer Finca Altamira Single Vineyard Malbec", "wine_still", achaval_ferrer, MENDOZA, "Argentina",
    subcategory="malbec_single_vineyard",
    description="Argentina's benchmark for old-vine Malbec — from ungrafted vines planted 1928 on limestone and alluvial soils in Altamira, La Consulta, at 1000m altitude. 18 months in new French oak (60%). Dark fruit preserve, graphite, tobacco, dark chocolate, and iron-rich minerals from limestone soils. Extraordinarily dense but balanced — requires 5-10 years to show full complexity. Consistently rated 97-100 by Robert Parker.",
    price_tier="ultra_premium")

clos_apalta = P("Clos de los Siete", "winery", MENDOZA, "Argentina",
    production_philosophy="Michel Rolland's Andean project: seven estates, one Malbec blend",
    philosophy_description="Clos de los Siete is Michel Rolland's signature South American project: seven investor partners each farming a distinct Mendoza Alta plot at 1050-1200m altitude near Valle de Uco. The blend draws from each partner's fruit — Malbec, Merlot, Syrah, Cabernet Sauvignon — to produce one of Mendoza's most consistent and accessible premium expressions.",
    key_personnel=[{"name": "Michel Rolland", "role": "Founding Winemaker"}, {"name": "Cecilia Baudron", "role": "Estate Director"}],
    production_details={"altitude": "1050-1200m Valle de Uco", "blend": "Malbec dominant + Merlot/Syrah/CabSauv", "founders": "7 investor partners"},
    reputation_narrative="Michel Rolland's Clos de los Siete demonstrated Valle de Uco's altitude potential at a scale that made Argentine premium wine internationally accessible. Consistently 92-94 points across all major critics — one of South America's most reliable value propositions in premium red wine.",
    price_positioning="premium")

PROD("Clos de los Siete Red Blend", "wine_still", clos_apalta, MENDOZA, "Argentina",
    subcategory="malbec_blend_alta_mendoza",
    description="Michel Rolland's signature Mendoza project — seven partner estates each farming distinct plots at 1050-1200m altitude in Valle de Uco. Malbec dominant (60%) blended with Merlot, Syrah, and Cabernet Sauvignon; 14 months in French oak. Plush and generously structured: black plum, dark cherry, vanilla, and gentle spice. The altitude adds freshness and elegance rarely found at this price. Consistently 92-94 points; ideal from year 2 through year 8.",
    price_tier="mid_range")

# ═══════════════════════════════════════════════════════════════════════════
# SWARTLAND — SOUTH AFRICA EXPANSION
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== SWARTLAND — SOUTH AFRICA ===")

mullineux = P("Mullineux & Leeu Family Wines", "winery", SWARTLAND, "South Africa",
    production_philosophy="Swartland old-vine Chenin Blanc and Syrah — South Africa's finest terroir",
    philosophy_description="Chris and Andrea Mullineux are the defining voices of the Swartland revolution. Their single-terroir Straw Wine, Granite, Schist, and Iron Chenin Blanc bottlings are South Africa's most celebrated terroir experiments — demonstrating that Swartland's ancient soils produce radically different wines. The Old Vines Syrah is considered South Africa's greatest Syrah expression.",
    key_personnel=[{"name": "Chris Mullineux", "role": "Winemaker/Co-Founder"}, {"name": "Andrea Mullineux", "role": "Winemaker/Co-Founder"}],
    production_details={"soils": "granite, schist, iron, clay", "viticulture": "organic/minimal intervention", "flagship": "single-terroir Chenin Blanc series"},
    reputation_narrative="Mullineux has achieved 100-point scores from Tim Atkin for their Straw Wine and consistently 96-98 for their single-terroir Chenin Blanc. Andrea Mullineux was named Winemaker of the Year by Wine Spectator — the first African winemaker to receive this honour. Allocated internationally.",
    price_positioning="ultra_premium")

PROD("Mullineux Signature White", "wine_still", mullineux, SWARTLAND, "South Africa",
    subcategory="chenin_blanc_swartland",
    description="South Africa's benchmark old-vine Chenin Blanc — from dry-farmed Swartland vines planted 1960s-70s across multiple ancient soil types (granite, schist, iron). Wild fermentation; aged in large French oak (20% new); minimal sulphur; unfined and unfiltered. Quince paste, beeswax, dry apricot, white pear, and a saline mineral spine from ancient granite. Old-vine concentration and wild fermentation create a wine of white Burgundy-level texture and length. Ages 8-15 years with confidence. Andrea Mullineux named Wine Spectator Winemaker of the Year.",
    price_tier="ultra_premium")

PROD("Mullineux Swartland Syrah", "wine_still", mullineux, SWARTLAND, "South Africa",
    subcategory="syrah_swartland",
    description="South Africa's finest Syrah from old-vine dry-farmed Swartland granite soils. Whole-cluster fermentation (40%); aged 18 months in large French oak and older barriques; no fining. Black olive, graphite, cured meat, dark blueberry, and white pepper. The granite terroir imparts remarkable minerality and cool-climate elegance — Northern Rhône in character, not Australian Shiraz. One of the Cape Winelands' most internationally collected red wines.",
    price_tier="premium")

# Stellenbosch addition
print("\n=== STELLENBOSCH — SOUTH AFRICA ===")

jordan_wine = P("Jordan Wine Estate", "winery", STELLENBOSCH, "South Africa",
    production_philosophy="Stellenbosch terroir diversity expressed through precise, food-friendly wines",
    philosophy_description="Gary and Kathy Jordan have farmed this exceptional Stellenbosch estate since 1993, developing one of the Cape Winelands' most diverse portfolios. The estate spans multiple soil types — granite, shale, sandstone — enabling excellent Chardonnay, Sauvignon Blanc, Cabernet, and Merlot. Consistent quality across all price points and exceptional terroir expression at the estate tier.",
    key_personnel=[{"name": "Gary Jordan", "role": "Winemaker/Co-Owner"}, {"name": "Kathy Jordan", "role": "Co-Owner"}],
    production_details={"soils": "granite, shale, sandstone", "estate": "full self-contained Stellenbosch"},
    reputation_narrative="Jordan Estate is one of South Africa's most consistent and critically admired producers across all tiers — from Chameleon (accessible) to The Prospector (reserve) and the Nine Yards Chardonnay (flagship). A Stellenbosch benchmark for balanced, terroir-driven wine.",
    price_positioning="premium")

PROD("Jordan Nine Yards Chardonnay", "wine_still", jordan_wine, STELLENBOSCH, "South Africa",
    subcategory="chardonnay_stellenbosch",
    description="Jordan Estate's flagship Chardonnay from highest-elevation granite blocks. Hand-picked; whole-bunch pressed; wild fermentation in French oak (40% new); 11 months on lees; unfined. White peach, citrus curd, hazelnut, and creamy lees texture with a granite mineral spine. The cool high-elevation vineyard delivers the acid structure for 5-8 years of development. Stellenbosch's benchmark Chardonnay — consistently compared to village Burgundy at half the price.",
    price_tier="premium")

cur.close()
conn.close()
print("\n✅ Terminal 9 Batch 1 — NZ + Argentina + South Africa complete.")
