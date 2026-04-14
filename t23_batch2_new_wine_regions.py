"""
T23 Batch 2: More new wine regions
Targets: Ribeira Sacra DO (ES), Collio DOC (IT), Txakoli (ES),
         Mornington Peninsula Chardonnay depth, Eden Valley (AU)
"""
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

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""
        INSERT INTO beverage_vintages (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (region_id, year, quality_descriptor, price_trajectory, season_narrative))
    print(f"    ✓ Vintage {year}: {quality_descriptor}")

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

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence,
           meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T23 BATCH 2: MORE NEW WINE REGIONS ===\n")

# ── RIBEIRA SACRA DO (Spain) ──
print("── RIBEIRA SACRA DO — Spain ──")
rid = R(
    name="Ribeira Sacra DO",
    country="Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Ribeira Sacra DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description=(
        "Ribeira Sacra is one of Spain's most dramatically beautiful and viticulturally "
        "extreme wine regions, situated in the deep river canyons of the Sil and Miño rivers "
        "in Galicia's interior. The region's vineyards are planted on impossibly steep granite "
        "and slate terraces that drop nearly vertically to the river below — heroic viticulture "
        "that can only be worked by hand. The primary variety is Mencía, which on Ribeira Sacra's "
        "cool granite terraces produces wines of extraordinary minerality and aromatic elegance "
        "quite different from the richer Bierzo versions. The ancient monasteries that give the "
        "region its name (Sacred Riverbank) have been associated with winemaking since the Romans."
    ),
    key_producers="Dominio do Bibei, Algueira, Guímaro, Envínate, Ronsel do Sil",
    historical_context=(
        "Ribeira Sacra's monasteries maintained winemaking traditions through the Middle Ages, "
        "but commercial wine production collapsed in the 20th century as young Galicians emigrated. "
        "A revival began in the 1990s when producers recognised the exceptional quality potential "
        "of the abandoned granite terraces, and the DO was established in 1996. The region has "
        "attracted Spain's most innovative natural wine producers."
    )
)
for yr, q, t in [
    (2019, "excellent", "rising"),
    (2020, "very_good", "stable"),
    (2021, "excellent", "rising"),
    (2022, "exceptional", "rising"),
    (2023, "excellent", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Dominio do Bibei",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Ribeira Sacra's philosophical vanguard — Bibei's granite terraces and indigenous varieties",
    philosophy_description=(
        "Dominio do Bibei is one of Ribeira Sacra's most philosophically rigorous estates, "
        "farming certified biodynamic vineyards on the granite terraces of the Bibei River "
        "tributary. The estate has revived pre-phylloxera indigenous Galician varieties "
        "alongside Mencía, including Brancellao, Merenzao, Mouratón, and Garnacha Tintorera, "
        "all on their own roots (pre-phylloxera ungrafted vines). The estate's Lalama and "
        "Lacima bottlings represent some of Spain's most extraordinary and individual wines, "
        "showcasing the Bibei River canyon's unique granite terroir."
    ),
    reputation_narrative=(
        "Dominio do Bibei has become one of Spain's most acclaimed estates, with critical "
        "recognition for their ability to produce wines of genuine complexity and originality "
        "from Ribeira Sacra's extreme granite terraces and pre-phylloxera vine heritage."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod1 = PROD(
    name="Dominio do Bibei Lalama Ribeira Sacra DO",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Spain",
    subcategory="Mencía Blend",
    description=(
        "Lalama is Dominio do Bibei's signature red blend from the granite terraces of the "
        "Bibei River canyon in Ribeira Sacra. A multi-varietal field blend led by Mencía with "
        "Brancellao, Merenzao, and other indigenous Galician varieties from biodynamically "
        "farmed, often pre-phylloxera old vines. The wine's extraordinary character — floral, "
        "mineral, and deeply complex — comes from the combination of granite soils, river "
        "canyon microclimate, and the genetic diversity of Galicia's ancient vine heritage. "
        "Among Spain's most individual and sought-after wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod1, "Lamprey à la bordelaise — Ribeira Sacra's iconic lamprey and red wine preparation",
     "complement", "classic", "main",
     "Galicia's ancient pairing — lamprey cooked in red wine with the very Ribeira Sacra wine")
PAIR(prod1, "Grilled Padrón peppers with fleur de sel and aged Tetilla cheese",
     "complement", "established", "starter",
     "Ribeira Sacra mineral Mencía and Galician peppers and local cheese — pure northwest Spanish terroir")

pid2 = P(
    name="Guímaro",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Ribeira Sacra's most expressive Mencía — Guímaro's terraced granite and mica soils",
    philosophy_description=(
        "Guímaro is one of Ribeira Sacra's most celebrated and accessible producers, Pedro "
        "Rodríguez farming steep terraced vineyards above the Sil River canyon where mica-rich "
        "granite soils produce Mencía of extraordinary aromatic precision and mineral tension. "
        "The estate's Mencía wines capture Ribeira Sacra's unique character — floral, fine-boned, "
        "and intensely mineral — with a freshness that reflects the cool canyon microclimate and "
        "the Sil's proximity."
    ),
    reputation_narrative=(
        "Guímaro has earned international recognition as one of Ribeira Sacra's reference "
        "producers, with their single-parcel wines and approachable estate Mencía demonstrating "
        "the canyon's extraordinary potential for elegant, mineral-driven red wine."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Guímaro Mencía Ribeira Sacra DO",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Spain",
    subcategory="Mencía",
    description=(
        "Estate Mencía from Guímaro's steep granite terraces above the Sil River canyon in "
        "Ribeira Sacra. The mica-rich granite soils and cool, shaded microclimate of the "
        "river canyon produce Mencía of extraordinary floral intensity and mineral precision "
        "— violet, blueberry, and slate dominate, with a freshness and lightness of body "
        "that makes this very different from the richer, warmer Bierzo expressions. "
        "Guímaro's Mencía captures the pure essence of Ribeira Sacra's heroic viticulture."
    ),
    price_tier="premium"
)
PAIR(prod2, "Roasted pork belly with Galician turnip tops (grelos) and potatoes",
     "complement", "classic", "main",
     "Ribeira Sacra Mencía and lacón (Galician pork with grelos) — the region's classic matching")
PAIR(prod2, "Sardines à la plancha with crushed tomato and sea salt",
     "complement", "established", "main",
     "Cool-climate Mencía's bright acidity and mineral freshness lift grilled sardines beautifully")

# ── COLLIO DOC (Italy) ──
print("\n── COLLIO DOC — Italy ──")
rid = R(
    name="Collio DOC",
    country="Italy",
    beverage_family="wine",
    designation_type="DOC",
    designation_name="Collio Goriziano DOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Collio is Friuli-Venezia Giulia's most prestigious wine appellation, situated in "
        "the northeastern corner of Italy bordering Slovenia. The region's distinctive "
        "'ponca' soils — alternating layers of marl and sandstone — and its position "
        "between the Julian Alps and the Adriatic create ideal conditions for white wines "
        "of extraordinary mineral complexity and aromatic precision. Tocai Friulano (now "
        "called Friulano), Pinot Grigio, Pinot Bianco, Sauvignon, and Ribolla Gialla are "
        "the key varieties, with many producers also pioneering the macerated white wine "
        "movement (orange wines) that spread globally from Friuli in the 1990s."
    ),
    key_producers="Josko Gravner, Stanko Radikon, Marco Felluga, Ronco del Gnemiz, Venica & Venica",
    historical_context=(
        "Collio's modern wine identity was shaped by Josko Gravner and Stanko Radikon in the "
        "1990s, when both producers abandoned conventional winemaking and began extended "
        "skin-contact maceration of white grapes in terracotta amphora — creating the orange "
        "wine movement that would influence a generation of winemakers globally. Their radical "
        "approach transformed Collio from a producer of clean, modern whites to a cradle "
        "of artisanal innovation."
    )
)
for yr, q, t in [
    (2019, "excellent", "stable"),
    (2020, "excellent", "stable"),
    (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"),
    (2023, "very_good", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Josko Gravner",
    producer_type="winery",
    region_id=rid,
    country="Italy",
    production_philosophy="Collio's radical visionary — Gravner's amphora skin-contact Ribolla Gialla",
    philosophy_description=(
        "Josko Gravner is one of the world's most influential winemakers, having single-handedly "
        "created the global orange wine movement when he returned from a visit to Georgia in "
        "2000 and abandoned conventional winemaking for extended skin-contact fermentation in "
        "traditional Georgian qvevri (terracotta amphora). Gravner's Ribolla Gialla undergoes "
        "6-7 months of skin contact in qvevri, followed by years of aging in large Slavonian "
        "oak casks and extensive bottle aging before release. The wines are deeply coloured, "
        "profoundly complex, and uniquely unlike any other Italian white wine."
    ),
    reputation_narrative=(
        "Josko Gravner's influence on global wine culture is impossible to overstate — his "
        "radical embrace of ancient Georgian winemaking techniques launched the worldwide "
        "orange wine movement and fundamentally changed how a generation of winemakers "
        "think about white wine production and terroir expression."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod1 = PROD(
    name="Gravner Ribolla Gialla Collio DOC",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Italy",
    subcategory="Ribolla Gialla",
    description=(
        "Gravner's Ribolla Gialla from Collio DOC, one of the world's most distinctive and "
        "original wines — an extended skin-contact white fermented and aged in Georgian "
        "terracotta amphora (qvevri) for 6-7 months before extended aging in large Slavonian "
        "oak casks and years of bottle aging. The wine's amber colour, profound tannin "
        "structure, and extraordinary complexity challenge every conventional notion of white "
        "wine. Flavours of dried apricot, beeswax, nuts, amber, and earth combine with a "
        "savoury, almost oxidative complexity that is unlike anything in Italian wine. "
        "A world wine monument and the template for the global orange wine movement."
    ),
    price_tier="ultra_premium"
)
PAIR(prod1, "Whole roasted duck with walnut and fig stuffing and aged Friulano",
     "complement", "classic", "main",
     "Gravner's amber Ribolla has the tannin and complexity to match duck's richness and roasting depth")
PAIR(prod1, "Ossobuco alla milanese with saffron risotto and gremolata",
     "complement", "established", "main",
     "Skin-contact white's oxidative complexity bridges braised veal collagen and saffron's earthiness")

pid2 = P(
    name="Venica & Venica",
    producer_type="winery",
    region_id=rid,
    country="Italy",
    production_philosophy="Collio's consistent excellence — Venica's modern, precise Friulano and Sauvignon",
    philosophy_description=(
        "Venica & Venica is one of Collio's most consistently excellent and approachable "
        "estates, producing precise, modern white wines from the region's ponca soils that "
        "have earned consistent international acclaim. While Gravner and Radikon represent "
        "Collio's radical natural wine wing, Venica provides the region's most reliable "
        "and accessible quality benchmark for conventional Friulano, Sauvignon, and Pinot "
        "Grigio that showcase Collio's distinctive mineral character without the challenge "
        "of extended skin contact."
    ),
    reputation_narrative=(
        "Venica & Venica has maintained Collio's reputation for precision and consistency "
        "for over 40 years, providing the appellation's accessible face of quality and "
        "introducing international wine lovers to Friulian grape varieties."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Venica & Venica Ronco delle Cime Sauvignon Collio DOC",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Italy",
    subcategory="Sauvignon Blanc",
    description=(
        "Single-vineyard Sauvignon Blanc from Venica & Venica's Ronco delle Cime site "
        "in the Collio DOC, Friuli. The Collio's ponca soils — alternating marl and "
        "sandstone layers — produce Sauvignon of a distinctive Italian character: more "
        "mineral and less herbaceous than Sancerre or New Zealand, with the variety's "
        "characteristic grapefruit and elderflower aromatics given a distinctive textural "
        "quality and savoury mineral finish by the region's unique soil. A benchmark for "
        "northern Italian Sauvignon Blanc and the Collio appellation."
    ),
    price_tier="premium"
)
PAIR(prod2, "San Daniele prosciutto with Friulano cheese and freshly baked schiacciata",
     "complement", "classic", "starter",
     "Collio Sauvignon's mineral freshness and citrus notes cut through prosciutto's salt and fat")
PAIR(prod2, "Grilled langoustines with herb butter and lemon gel",
     "complement", "established", "main",
     "Collio Sauvignon's mineral citrus precision elevates sweet langoustine and herb butter")

# ── TXAKOLI (Spain) ──
print("\n── TXAKOLI (Getariako Txakolina) — Spain ──")
rid = R(
    name="Getariako Txakolina DO",
    country="Spain",
    beverage_family="wine",
    designation_type="DO",
    designation_name="Getariako Txakolina DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description=(
        "Getariako Txakolina is the Basque Country's most famous Txakoli appellation, "
        "situated on the steep hillsides above the fishing village of Getaria on Spain's "
        "Atlantic coast. Txakoli is a distinctive low-alcohol, high-acid, slightly "
        "effervescent white wine produced from the indigenous Hondarrabi Zuri grape, "
        "with a small amount of Hondarrabi Beltza red grape. The Atlantic climate — "
        "high rainfall, cool temperatures, and strong marine influence — creates wines "
        "of piercing acidity, saline mineral freshness, and delicate citrus character "
        "that are unique in the wine world. Txakoli is traditionally poured from height "
        "to aerate and create a fine effervescence."
    ),
    key_producers="Txomin Etxaniz, Ameztoi, Hiruzta, Rezabal, Baratza",
    historical_context=(
        "Txakoli nearly disappeared in the 20th century as Basque Country industrialised "
        "and wine consumption shifted to Rioja. The Getariako Txakolina DO was established "
        "in 1989 and Ameztoi's efforts to revive quality production in Getaria sparked a "
        "renaissance. Today Txakoli is celebrated globally as one of wine's great seafood "
        "companions and a symbol of Basque cultural identity."
    )
)
for yr, q, t in [
    (2019, "excellent", "stable"),
    (2020, "very_good", "stable"),
    (2021, "excellent", "rising"),
    (2022, "excellent", "rising"),
    (2023, "very_good", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Bodega Txomin Etxaniz",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Getaria's founding estate — Txomin Etxaniz's classic Txakoli since 1649",
    philosophy_description=(
        "Bodega Txomin Etxaniz is one of the oldest and most historically significant Txakoli "
        "producers, with records of the Etxaniz family farming the Getaria hillside vineyards "
        "dating to 1649. The estate farms Hondarrabi Zuri and Hondarrabi Beltza on steep "
        "Atlantic-facing terraces in Getaria, producing the classic Getariako Txakolina style: "
        "bone dry, searingly acidic, delicately effervescent, and profoundly saline. Txomin "
        "Etxaniz's consistency and quality across centuries of continuous production make it "
        "the definitive reference for Getariako Txakolina."
    ),
    reputation_narrative=(
        "Txomin Etxaniz is the benchmark Txakoli producer globally, responsible for much of "
        "the international awareness of this uniquely Basque wine style. Their estate's "
        "multi-century history and consistent quality make them the appellation's ambassador."
    ),
    price_positioning="mid_range",
    authority_tier=1
)
prod1 = PROD(
    name="Txomin Etxaniz Getariako Txakolina",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Spain",
    subcategory="Hondarrabi Zuri",
    description=(
        "Classic Getariako Txakolina from the historic Txomin Etxaniz estate in Getaria, "
        "produced from Hondarrabi Zuri vines on steep Atlantic-facing terraces above the "
        "fishing village. Low alcohol (10.5%), naturally effervescent, bone dry, and with "
        "a searingly saline acidity that is unique in the wine world. The Atlantic climate's "
        "high humidity and constant sea breeze give the wine its defining saline mineral "
        "quality — citrus, green apple, sea spray — while the natural fizz comes from "
        "bottling during primary fermentation. Traditionally poured from height to aerate."
    ),
    price_tier="mid_range"
)
PAIR(prod1, "Grilled wild Atlantic anchovies with Guindilla peppers in olive oil",
     "complement", "classic", "starter",
     "The Basque Country's greatest pairing — Txakoli's saline acidity is the perfect match for anchovies")
PAIR(prod1, "Pintxos of salt cod with romesco and crispy shallot on grilled bread",
     "complement", "established", "casual",
     "Txakoli's refreshing effervescence and acidity cleanse between pintxos and enhance salt cod")

pid2 = P(
    name="Bodega Ameztoi",
    producer_type="winery",
    region_id=rid,
    country="Spain",
    production_philosophy="Getaria's quality revival — Ameztoi's Rubentis and the rebirth of Txakoli",
    philosophy_description=(
        "Bodega Ameztoi is credited with leading the quality revival of Getariako Txakolina "
        "in the 1980s and 1990s, establishing that Txakoli could be a serious, internationally "
        "recognised wine rather than a simple local refreshment. The estate is particularly "
        "celebrated for Rubentis, their rosado version of Txakoli made from Hondarrabi Beltza, "
        "which has become one of Spain's most celebrated pink wines and introduced Txakoli's "
        "style to a global audience through its vivid colour and Atlantic freshness."
    ),
    reputation_narrative=(
        "Ameztoi's Rubentis is arguably Spain's most celebrated dry rosado, combining Txakoli's "
        "characteristic Atlantic freshness with the red-fruited vibrancy of Hondarrabi Beltza "
        "to create a wine of extraordinary personality and food affinity."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod2 = PROD(
    name="Ameztoi Rubentis Txakoli Rosado Getariako Txakolina",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Spain",
    subcategory="Hondarrabi Beltza Rosado",
    description=(
        "Rubentis is Ameztoi's celebrated rosado Txakoli produced from Hondarrabi Beltza "
        "(Red Txakoli) grapes, one of the Getariako Txakolina appellation's indigenous red "
        "varieties. The wine's vivid salmon-red colour and effervescent, refreshing character "
        "capture all of Txakoli's Atlantic personality — saline, crisp, low in alcohol — "
        "with the addition of Hondarrabi Beltza's wild strawberry and cherry fruit character. "
        "One of Spain's most distinctive and celebrated rosados, showing that Txakoli's "
        "extreme freshness and minerality works brilliantly in a rosado format."
    ),
    price_tier="mid_range"
)
PAIR(prod2, "Barbecued langoustines with aioli and grilled lemon",
     "complement", "classic", "main",
     "Basque seafood feast — Rubentis' Atlantic saline freshness is the ideal langoustine companion")
PAIR(prod2, "Jamón Ibérico de bellota with crusty pan con tomate",
     "complement", "established", "casual",
     "Txakoli rosado's effervescence and acidity cut through Ibérico fat while cherry notes complement")

# ── EDEN VALLEY (Australia) ──
print("\n── EDEN VALLEY — Australia ──")
rid = R(
    name="Eden Valley",
    country="Australia",
    beverage_family="wine",
    designation_type="GI",
    designation_name="Eden Valley GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description=(
        "Eden Valley is one of Australia's most important cool-climate wine regions, situated "
        "in the Mount Lofty Ranges east of the Barossa Valley in South Australia at elevations "
        "of 400-600m. The high elevation significantly cools the growing season compared to "
        "the adjacent Barossa Valley floor, making Eden Valley particularly suited to Riesling "
        "and cool-climate Shiraz. The Eden Valley's Riesling is considered Australia's finest "
        "and most age-worthy, developing extraordinary petrol, lime, and mineral character "
        "over decades. The High Eden sub-zone at the highest elevations is a distinct GI "
        "for the most cool-climate expressions."
    ),
    key_producers="Henschke, Pewsey Vale, Irvine, Hewitson, Mountadam",
    historical_context=(
        "Eden Valley's distinction from the Barossa Valley began to be recognised in the "
        "1980s when the elevation's cooling effect became understood as a key quality "
        "differentiator. Henschke's Hill of Grace vineyard — planted in the 1860s with "
        "Shiraz on own-root pre-phylloxera vines — is one of Australia's most celebrated "
        "single-vineyard wines and the Eden Valley's most iconic product."
    )
)
for yr, q, t in [
    (2019, "excellent", "stable"),
    (2020, "very_good", "stable"),
    (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"),
    (2023, "excellent", "stable"),
]:
    VIN(rid, yr, q, t)

pid = P(
    name="Henschke",
    producer_type="winery",
    region_id=rid,
    country="Australia",
    production_philosophy="Eden Valley's most revered estate — Hill of Grace and Australia's great pre-phylloxera Shiraz",
    philosophy_description=(
        "Henschke is one of Australia's most revered wine dynasties, farming Eden Valley "
        "and Keyneton vineyards with century-old vines on their own-root pre-phylloxera stocks. "
        "The estate's crown jewel is the Hill of Grace single vineyard — planted in the 1860s "
        "on Shiraz cuttings brought from the Bethany-Galilee area of Silesia by Henschke's "
        "ancestors — which produces one of Australia's most celebrated and expensive wines. "
        "Winemaker Stephen Henschke and viticulturist Prue Henschke have applied biodynamic "
        "principles to their Eden Valley estate for decades."
    ),
    reputation_narrative=(
        "Henschke's Hill of Grace is considered Australia's greatest single-vineyard wine "
        "and among the world's finest Shiraz, commanding prices and critical scores that "
        "place it alongside the greatest Hermitage and Côte-Rôtie. The estate's five "
        "generations of continuous family ownership and their pre-phylloxera vine heritage "
        "make Henschke a unique Australian wine institution."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)
prod1 = PROD(
    name="Henschke Henry's Seven Eden Valley Shiraz Cabernet",
    category="wine_still",
    producer_id=pid,
    region_id=rid,
    origin_country="Australia",
    subcategory="Shiraz Blend",
    description=(
        "Henry's Seven is Henschke's accessible introduction to their Eden Valley estate, "
        "a blend of Shiraz, Viognier, Grenache, and Cabernet Sauvignon named for seven "
        "generations of the Henschke family. While Hill of Grace and Mount Edelstone are "
        "beyond most collectors' reach, Henry's Seven captures Eden Valley's character — "
        "cool-climate elegance, spice, and mineral complexity — at an approachable level. "
        "The Viognier co-fermentation adds floral aromatics and perfume characteristic of "
        "the best Rhône-inspired Australian Shiraz blends."
    ),
    price_tier="premium"
)
PAIR(prod1, "Lamb rump with native thyme jus, roasted Jerusalem artichoke, and bush tomato",
     "complement", "classic", "main",
     "Eden Valley Shiraz's cool-climate elegance and spice match native Australian herb and lamb")
PAIR(prod1, "Char-grilled kangaroo with quandong reduction and Davidson plum gel",
     "complement", "established", "main",
     "Australian game and Australian cool-climate Shiraz — native ingredients with native wine")

pid2 = P(
    name="Pewsey Vale",
    producer_type="winery",
    region_id=rid,
    country="Australia",
    production_philosophy="Eden Valley Riesling specialist — High Eden's benchmark for Australia's greatest white",
    philosophy_description=(
        "Pewsey Vale is one of Eden Valley's founding Riesling estates, farming their historic "
        "vineyard in the High Eden sub-zone at the highest elevation in the GI. The vineyard "
        "was originally planted in the 1840s and re-established by S. Smith & Son (Yalumba) "
        "in 1961, making it one of Australia's most historically significant Riesling sites. "
        "The High Eden's elevation creates growing conditions ideal for Riesling of exceptional "
        "longevity — the wines develop the characteristic petrol, lime, and mineral character "
        "of great German Riesling over decades of cellaring."
    ),
    reputation_narrative=(
        "Pewsey Vale's The Contour Riesling is considered Australia's most ageworthy Riesling, "
        "developing extraordinary petrol and mineral complexity over 10-20 years that places "
        "it alongside the finest German and Alsatian examples of this great variety."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod2 = PROD(
    name="Pewsey Vale The Contour Riesling Eden Valley",
    category="wine_still",
    producer_id=pid2,
    region_id=rid,
    origin_country="Australia",
    subcategory="Riesling",
    description=(
        "The Contour is Pewsey Vale's reserve Riesling from their historic High Eden vineyard, "
        "one of Australia's most celebrated and age-worthy white wines. Produced from the "
        "highest-elevation, slowest-ripening sections of the vineyard, The Contour is only "
        "made in the finest vintages and develops extraordinary complexity over 10-20 years "
        "of cellaring — lime, petrol, mineral slate, and beeswax — in a style that invites "
        "comparison with the great German Riesling Spätlesen. The High Eden's cool elevation "
        "preserves natural acidity that provides the backbone for decades of evolution."
    ),
    price_tier="premium"
)
PAIR(prod2, "Seared scallops with lemon butter, pickled cucumber, and dill oil",
     "complement", "classic", "main",
     "Eden Valley Riesling's lime precision and mineral tension create perfect harmony with scallops")
PAIR(prod2, "Indian korma with cashew cream, saffron rice, and fresh coriander",
     "contrast", "established", "main",
     "Riesling's acidity and subtle off-dry character balance korma's rich cream and aromatic spices")

print("\n✅ T23 Batch 2 complete.")
print("  Ribeira Sacra DO: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Collio DOC: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Getariako Txakolina: +2 producers, +2 products, +4 pairings, +5 vintages")
print("  Eden Valley: +2 producers, +2 products, +4 pairings, +5 vintages")

cur.close()
conn.close()
