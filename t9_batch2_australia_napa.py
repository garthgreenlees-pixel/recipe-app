#!/usr/bin/env python3
"""Terminal 9 — Batch 2: Australian Wine Depth + Napa Valley Expansion"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

BAROSSA    = 84
MCLAREN    = 85
YARRA      = 86
NAPA       = 80
SONOMA     = 81

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
# BAROSSA VALLEY — AUSTRALIAN SHIRAZ DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("=== BAROSSA VALLEY — AUSTRALIA ===")

torbreck = P("Torbreck Vintners", "winery", BAROSSA, "Australia",
    production_philosophy="Old-vine Barossa Grenache, Shiraz, Mataro — Rhône varieties at their Antipodean peak",
    philosophy_description="David Powell established Torbreck in 1994, building a portfolio from ancient Barossa Valley dry-farmed bushvines — some among the world's oldest Grenache plantings (1860s). The RunRig is Australia's most celebrated Shiraz-Viognier co-fermentation, inspired by Côte-Rôtie. The Descendant — Shiraz from the same clone as RunRig vines — is the estate's most precious bottling.",
    key_personnel=[{"name": "David Powell", "role": "Founder/Winemaker"}],
    production_details={"flagship": "RunRig Shiraz/Viognier", "vine_age": "some Grenache to 1860s", "style": "co-fermented Rhône varieties"},
    reputation_narrative="Torbreck's RunRig is one of Australia's most internationally collected wines — consistently 98-100 from James Halliday, Parker, and Wine Spectator. The estate demonstrated that Barossa's ancient dry-farmed bushvines could rival the world's greatest Rhône expressions.",
    price_positioning="ultra_premium")

PROD("Torbreck RunRig Shiraz Viognier", "wine_still", torbreck, BAROSSA, "Australia",
    subcategory="shiraz_barossa_valley",
    description="Australia's benchmark Shiraz-Viognier co-fermentation — inspired by Côte-Rôtie, produced from century-old dry-farmed Barossa Shiraz with 2-3% Viognier co-fermented in open vats. The Viognier co-fermentation adds perfume, lifted fruit, and tannin stability. Dark chocolate, black plum, violets, licorice, and a signature floral lift from Viognier. One of Australia's most collected wines; consistently 98-100 points. Allocated globally.",
    price_tier="ultra_premium")

PROD("Torbreck The Steading", "wine_still", torbreck, BAROSSA, "Australia",
    subcategory="grenache_shiraz_mataro",
    description="Torbreck's benchmark GSM blend from ancient Barossa bushvines — Grenache dominant (from 1910s plantings) with Shiraz and Mataro (Mourvèdre). Aged 18 months in large format oak. Red cherry, dark plum, dried herbs, and white pepper. The ancient Grenache delivers a silkiness and purity rare in Australian reds. Consistently 93-95 points; the accessible entry to Torbreck's old-vine program.",
    price_tier="premium")

two_hands = P("Two Hands Wines", "winery", BAROSSA, "Australia",
    production_philosophy="Single-vineyard Barossa Shiraz showcasing the full spectrum of sub-regional expression",
    philosophy_description="Two Hands was established to prove that Barossa Valley Shiraz could be as site-specific and complex as Burgundy Pinot Noir. Their Ares (Marananga), Aphrodite (Ebenezer), and Lily's Garden (Seppeltsfield) bottlings each demonstrate dramatically different Barossa sub-regional characters — the world's first single-vineyard Barossa Shiraz program to achieve international critical consensus.",
    key_personnel=[{"name": "Michael Twelftree", "role": "Founder"}, {"name": "Richard Mintz", "role": "Co-Founder"}],
    production_details={"program": "single-vineyard sub-regional Shiraz", "sub_regions": "Marananga, Ebenezer, Seppeltsfield, Greenock"},
    reputation_narrative="Two Hands Wines demonstrated conclusively that Barossa Valley sub-regional terroir differences are real and measurable — their single-vineyard program educated a generation of Australian wine drinkers and buyers about Barossa's internal complexity.",
    price_positioning="ultra_premium")

PROD("Two Hands Ares Shiraz", "wine_still", two_hands, BAROSSA, "Australia",
    subcategory="shiraz_barossa_valley",
    description="Two Hands' flagship Marananga sub-regional Shiraz — from the Eden Valley foothills where cooler temperatures and loam/clay soils create a more refined, detailed Barossa Shiraz than the warmer valley floor. Dark plum, licorice, mocha, and iron-rich mineral notes. More structured and elegant than classic Barossa Shiraz — built for 10-15 years of development. Consistently 96-99 points from James Halliday.",
    price_tier="ultra_premium")

# ═══════════════════════════════════════════════════════════════════════════
# McLAREN VALE — SOUTH AUSTRALIA
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== McLAREN VALE — AUSTRALIA ===")

yangarra = P("Yangarra Estate Vineyard", "winery", MCLAREN, "Australia",
    production_philosophy="Ancient McShane Vineyard old-vine Grenache — McLaren Vale at its most authentic",
    philosophy_description="Yangarra Estate sits on 180 acres of McLaren Vale including the McShane Vineyard block of ancient Grenache (planted circa 1946). Peter Fraser crafts biodynamic McLaren Vale wines of exceptional restraint and elegance — far from the blockbuster style. High Sands is produced from pre-phylloxera Grenache on rare deep sand over limestone, creating some of Australia's most delicate and complex Grenache expressions.",
    key_personnel=[{"name": "Peter Fraser", "role": "Chief Winemaker"}],
    production_details={"flagship": "High Sands Grenache", "key_vineyard": "McShane Vineyard 1946 Grenache", "viticulture": "biodynamic"},
    reputation_narrative="Yangarra's High Sands Grenache is considered Australia's greatest Grenache expression — consistently scoring 96-98 from James Halliday. The biodynamic farming and ancient McShane Vineyard fruit has elevated McLaren Vale's Grenache reputation internationally.",
    price_positioning="ultra_premium")

PROD("Yangarra High Sands Grenache", "wine_still", yangarra, MCLAREN, "Australia",
    subcategory="grenache_mclaren_vale",
    description="Australia's benchmark Grenache — from pre-phylloxera Grenache vines (planted circa 1900s) on deep sand over limestone in McLaren Vale's Kangarilla sub-region. Biodynamic farming; wild fermentation; whole-bunch inclusion; aged in large format old French oak. Fresh red cherry, orange peel, dried rose, white pepper, and extraordinary delicacy. The sandy soils create a lightness and purity that challenges all assumptions about Australian Grenache. Australia's most elegant red wine. 96-98 points consistently.",
    price_tier="ultra_premium")

PROD("Yangarra Estate Shiraz", "wine_still", yangarra, MCLAREN, "Australia",
    subcategory="shiraz_mclaren_vale",
    description="Yangarra's estate-level McLaren Vale Shiraz from biodynamic vines across multiple sub-blocks. Wild fermentation with whole-bunch inclusion (15-20%); aged in large format French oak. More restrained and peppery than typical McLaren Vale Shiraz — dark plum, licorice, cracked pepper, and graphite. Peter Fraser's biodynamic approach delivers freshness and complexity unusual for the region. Exceptional food wine and one of McLaren Vale's most consistent values.",
    price_tier="premium")

chapel_hill = P("Chapel Hill Winery", "winery", MCLAREN, "Australia",
    production_philosophy="McLaren Vale's benchmark for accessible Shiraz with Bushard Vineyard depth",
    philosophy_description="Chapel Hill was established in a converted 1865 chapel and has been McLaren Vale's most consistent quality-to-value producer for three decades. The Bushard Vineyard Shiraz — from centenarian vines — is the estate's benchmark, and the multi-regional The Vicar blend demonstrates McLaren Vale's capacity for Cabernet-Shiraz integration.",
    key_personnel=[{"name": "Michael Fragos", "role": "Chief Winemaker"}],
    production_details={"flagship": "Bushard Vineyard Shiraz", "established": "1987", "heritage": "converted 1865 chapel"},
    reputation_narrative="Chapel Hill has delivered consistently excellent McLaren Vale Shiraz for thirty years — the Bushard Vineyard expression is one of Australia's great values in aged Shiraz, demonstrating the quality ceiling of McLaren Vale's centenarian vineyard material.",
    price_positioning="premium")

PROD("Chapel Hill Bushard Vineyard Shiraz", "wine_still", chapel_hill, MCLAREN, "Australia",
    subcategory="shiraz_mclaren_vale",
    description="Single-vineyard McLaren Vale Shiraz from centenarian vines in the Bushard Vineyard — one of the oldest continuously harvested Shiraz sites in Australia. Deeply concentrated blackberry, dark chocolate, licorice, and leather with characteristic McLaren Vale richness. Aged 18 months in French oak (40% new). An extraordinary quality-to-value proposition that rewards 5-10 years of cellaring.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# YARRA VALLEY — VICTORIA WINE
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== YARRA VALLEY — AUSTRALIA ===")

mac_forbes = P("Mac Forbes", "winery", YARRA, "Australia",
    production_philosophy="Single-vineyard, sub-regional Yarra Valley — Australia's most Burgundian Pinot producer",
    philosophy_description="Mac Forbes produces the most vineyard-specific wines in the Yarra Valley — each bottling from a named sub-regional site (Woori Yallock, Hoddles Creek, Healesville, Yering) to demonstrate the dramatic terroir differences within this diverse valley. The approach — whole bunch, wild yeast, unfined — is purely Burgundian in philosophy, applied to Yarra's cool-climate Pinot Noir and Chardonnay.",
    key_personnel=[{"name": "Mac Forbes", "role": "Founder/Winemaker"}],
    production_details={"approach": "sub-regional single-vineyard", "fermentation": "wild yeast, whole bunch", "style": "minimal intervention"},
    reputation_narrative="Mac Forbes is considered Australia's most intellectually rigorous Pinot Noir producer — the sub-regional program has demonstrated that Yarra Valley's 30km east-west width contains dramatically different expressions. The Woori Yallock bottling is considered Yarra's most Vosne-Romanée-like expression.",
    price_positioning="premium")

PROD("Mac Forbes Woori Yallock Pinot Noir", "wine_still", mac_forbes, YARRA, "Australia",
    subcategory="pinot_noir_yarra_valley",
    description="Sub-regional Pinot Noir from Woori Yallock — the warmest, richest Yarra Valley sub-region. Wild fermentation; 40-50% whole bunch; aged 10 months in French oak (25% new). Dark cherry, spice, forest floor, and dark herb with more flesh and richness than the cooler Healesville parcels. Consistently Mac Forbes' most immediately accessible and richly flavoured Pinot. 93-95 points regularly from James Halliday.",
    price_tier="premium")

PROD("Mac Forbes Chardonnay", "wine_still", mac_forbes, YARRA, "Australia",
    subcategory="chardonnay_yarra_valley",
    description="Mac Forbes' multi-site Yarra Valley Chardonnay — whole-bunch pressed; wild fermented in aged French oak; 10 months on lees; no fining. White peach, lemon curd, almond meal, and subtle struck-match reduction from wild fermentation. The restrained oak use and elevated acid from Yarra's cool climate create a wine of Côte de Beaune elegance. Australia's most Burgundian Chardonnay at the accessible price tier.",
    price_tier="mid_range")

de_bortoli_yarra = P("De Bortoli Wines Yarra Valley", "winery", YARRA, "Australia",
    production_philosophy="Yarra Valley prestige estate — Gulf Station and Melba Vineyard Pinot and Chardonnay",
    philosophy_description="De Bortoli's Yarra Valley estate at Gulf Station (established 1987 by the De Bortoli family) produces the estate's premium Victorian wines under Chief Winemaker Steve Webber. The single-vineyard Lusatia Park Vineyard Pinot Noir and the Village Chardonnay are among Yarra's most consistent expressions at their respective price points.",
    key_personnel=[{"name": "Steve Webber", "role": "Chief Winemaker"}],
    production_details={"estate": "Gulf Station, Yering, Melba Vineyard", "established": "1987"},
    reputation_narrative="De Bortoli Yarra Valley has been one of the valley's benchmark estates for three decades — Steve Webber's Pinot Noir and Chardonnay programs consistently deliver among Yarra's best expressions, and the estate's Lusatia Park single-vineyard Pinot is consistently one of Australia's most elegant.",
    price_positioning="premium")

PROD("De Bortoli Lusatia Park Vineyard Pinot Noir", "wine_still", de_bortoli_yarra, YARRA, "Australia",
    subcategory="pinot_noir_yarra_valley",
    description="Single-vineyard Pinot Noir from the Lusatia Park Vineyard in the upper Yarra — one of the valley's coolest sites. Hand-picked; whole bunch (20%); wild fermentation; 10 months in French oak (20% new). Red cherry, dried rose petal, spice, and fine silky tannins. The cool Lusatia Park site produces Pinot of exceptional delicacy and elegance — consistently considered Yarra Valley's most refined Pinot Noir expression. 94-96 points from James Halliday annually.",
    price_tier="ultra_premium")

# ═══════════════════════════════════════════════════════════════════════════
# NAPA VALLEY — CALIFORNIA EXPANSION
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== NAPA VALLEY — CALIFORNIA ===")

heitz = P("Heitz Wine Cellars", "winery", NAPA, "USA",
    production_philosophy="Napa Valley's historic benchmark — Martha's Vineyard Cabernet since 1966",
    philosophy_description="Heitz Wine Cellars is one of Napa Valley's founding estates — Joe Heitz purchased the Spring Mountain property in 1961 and released the first Martha's Vineyard Cabernet Sauvignon in 1966. The eucalyptus character of Martha's Vineyard (from trees bordering the vineyard) became the most discussed terroir signature in California wine history. Under the Heitz family, the wines have been made without compromise since the beginning.",
    key_personnel=[{"name": "Brittany Heitz", "role": "Owner/Director"}, {"name": "Dave Heitz", "role": "Winemaker"}],
    production_details={"flagship": "Martha's Vineyard Cabernet Sauvignon", "established": "1961", "heritage": "founding Napa estate"},
    reputation_narrative="Heitz Martha's Vineyard is one of California's most historically significant wines — the 1974 vintage was arguably the first Napa Cabernet to achieve world-class recognition. The distinctive eucalyptus mint character from Martha's Vineyard remains one of California's most recognizable and discussed terroir signatures.",
    price_positioning="ultra_premium")

PROD("Heitz Martha's Vineyard Cabernet Sauvignon", "wine_still", heitz, NAPA, "USA",
    subcategory="cabernet_sauvignon_napa",
    description="California's most historically significant single-vineyard Cabernet Sauvignon — from the Martha's Vineyard site in Oakville, Napa Valley, first released in 1966. The distinctive eucalyptus and mint character (from trees bordering the vineyard) combined with blackcurrant, cedar, and tobacco is among California wine's most recognizable and debated terroir signatures. Aged 3+ years in American oak; requires a decade of cellaring. A California icon.",
    price_tier="ultra_premium")

stag_leap = P("Stag's Leap Wine Cellars", "winery", NAPA, "USA",
    production_philosophy="Stags Leap District Cabernet — the wine that won the 1976 Paris Tasting",
    philosophy_description="Stag's Leap Wine Cellars became the world's most famous Napa Valley producer when its 1973 Cabernet Sauvignon S.L.V. finished first in the 1976 Paris Tasting, defeating Château Mouton Rothschild and Château Haut-Brion in a blind tasting. Winemaker Warren Winiarski's vision was of elegant, structured Napa Cabernet — the antithesis of the fruit-bomb style. The CASK 23 represents the pinnacle of the estate's selection.",
    key_personnel=[{"name": "Marcus Notaro", "role": "Head Winemaker"}],
    production_details={"historic": "won 1976 Judgment of Paris", "flagship": "CASK 23", "sub_region": "Stags Leap District"},
    reputation_narrative="Stag's Leap Wine Cellars is permanently in California wine history as the 1976 Paris Tasting winner. The estate's Stags Leap District location — with its distinctive palisades and cooler afternoon winds — produces Cabernet of exceptional elegance and aging potential. CASK 23 has been California's benchmark for structured, age-worthy Napa Cabernet for 50 years.",
    price_positioning="ultra_premium")

PROD("Stag's Leap CASK 23 Cabernet Sauvignon", "wine_still", stag_leap, NAPA, "USA",
    subcategory="cabernet_sauvignon_napa",
    description="The apex of Stag's Leap Wine Cellars — the estate's finest selection from SLV and FAY vineyards in the Stags Leap District. Warren Winiarski's vision of elegant, structured Napa Cabernet made famous at the 1976 Paris Tasting. Blackcurrant, dark cherry, cedar, tobacco, and graphite with the signature Stags Leap District purity and restraint. Requires 10-15 years to reach peak complexity. One of California's greatest age-worthy Cabernet Sauvignons.",
    price_tier="ultra_premium")

PROD("Stag's Leap S.L.V. Estate Cabernet Sauvignon", "wine_still", stag_leap, NAPA, "USA",
    subcategory="cabernet_sauvignon_napa",
    description="The original vineyard that made Stag's Leap famous — the SLV (Stag's Leap Vineyard) Cabernet Sauvignon from the estate's founding blocks in the Stags Leap District palisades. Cooler than the Oakville floor, the SLV produces Cabernet of exceptional precision and mineral definition. Cedar, blackcurrant, dusty tannins, and remarkable longevity. The 1973 vintage of this wine won the 1976 Judgment of Paris.",
    price_tier="ultra_premium")

caymus = P("Caymus Vineyards", "winery", NAPA, "USA",
    production_philosophy="Rutherford Napa Cabernet — America's most recognised fine wine brand",
    philosophy_description="Chuck Wagner began making Caymus Vineyards Cabernet Sauvignon in 1972 from the family's Rutherford ranching property. The Special Selection — made only in exceptional years — has achieved consistent 96-100 ratings and is arguably America's most widely recognised luxury wine. The standard Napa Cabernet delivers the Caymus house style of lush, generous, immediately accessible Rutherford Cabernet.",
    key_personnel=[{"name": "Chuck Wagner", "role": "Founder/Owner"}, {"name": "Charlie Wagner", "role": "President"}],
    production_details={"flagship": "Special Selection Cabernet Sauvignon", "sub_region": "Rutherford Bench", "style": "rich, plush, accessible"},
    reputation_narrative="Caymus Special Selection is America's most widely allocated luxury wine — achieving 100-point scores from Wine Spectator twice (1984 and 1990 — the only wine to win Wine of the Year twice). The consistent house style of plush, generous Rutherford Cabernet has made Caymus the benchmark for accessible Napa luxury.",
    price_positioning="ultra_premium")

PROD("Caymus Special Selection Cabernet Sauvignon", "wine_still", caymus, NAPA, "USA",
    subcategory="cabernet_sauvignon_napa",
    description="America's most famous luxury Cabernet Sauvignon — made only in exceptional Napa Valley vintages from the Wagner family's Rutherford estate. Aged 22 months in American oak. Blackberry jam, cassis, dark chocolate, vanilla, and mocha with the plush Rutherford texture that defines the Caymus style. The only wine in history to be named Wine Spectator Wine of the Year twice (1984, 1990). Immediately approachable but rewards 5-10 years of cellaring.",
    price_tier="ultra_premium")

PROD("Caymus Napa Valley Cabernet Sauvignon", "wine_still", caymus, NAPA, "USA",
    subcategory="cabernet_sauvignon_napa",
    description="Caymus's flagship multi-regional Napa Valley Cabernet — the style that made the estate globally famous. Rutherford-dominated with fruit from 5 Napa sub-regions; aged 14 months in American oak. Lush blackberry, cassis, mocha, and vanilla — the benchmark for accessible, generous California Cabernet. America's most recognizable luxury wine style at the premium tier.",
    price_tier="premium")

# Sonoma addition
print("\n=== SONOMA COUNTY — CALIFORNIA ===")

williams_selyem = P("Williams Selyem Winery", "winery", SONOMA, "USA",
    production_philosophy="Russian River Valley Pinot Noir — California's Burgundy from a backyard garage",
    philosophy_description="Burt Williams and Ed Selyem began making Pinot Noir in a garage in 1981, creating what became California's most sought-after cult Pinot Noir mailing list. The Allen Vineyard, Rochioli Vineyard, and Hirsch Vineyard bottlings defined the Russian River Valley Pinot style — rich, deeply coloured, intense, and layered. Williams Selyem remains the archetypal California Pinot cult producer.",
    key_personnel=[{"name": "Bob Cabral", "role": "Winemaker (1998-2014)"}, {"name": "Ulises Valdez", "role": "Current Winemaker"}],
    production_details={"region": "Russian River Valley, Sonoma Coast", "flagship": "Allen Vineyard Pinot Noir", "allocation": "mailing list only"},
    reputation_narrative="Williams Selyem is California's original cult Pinot Noir producer — the Russian River Valley style they developed in the 1980s influenced every California Pinot producer that followed. The estate's single-vineyard bottlings from Rochioli, Allen, and Hirsch Vineyards are among California's most allocated and sought-after wines.",
    price_positioning="ultra_premium")

PROD("Williams Selyem Allen Vineyard Pinot Noir", "wine_still", williams_selyem, SONOMA, "USA",
    subcategory="pinot_noir_russian_river",
    description="California's benchmark Russian River Valley single-vineyard Pinot Noir — from the Allen Vineyard in the heart of the Russian River Valley appellation. Wild fermentation; 35-40% whole bunch; 12 months in French oak (40% new). Dark cherry, plum, cola, baking spice, and forest floor with the signature Russian River weight and complexity. Allocated exclusively through the Williams Selyem mailing list. Consistently 96-100 points from California critics.",
    price_tier="ultra_premium")

cur.close()
conn.close()
print("\n✅ Terminal 9 Batch 2 — Australia + Napa + Sonoma complete.")
