#!/usr/bin/env python3
"""B137 — Bierzo DO revisit supplement + Txakoli (Getariako Txakolina DO, Spain),
   Ribeira Sacra DO (Spain), Mencia DO (Spain generics), Alentejo DOC (Portugal),
   Dao DOC (Portugal)
Constraints confirmed:
  quality_descriptor: exceptional/excellent/very_good/good/average/challenging/poor
  price_trajectory: rising/stable/declining/speculative/unavailable
  reputation_tier: iconic/prestigious/respected/emerging/overlooked
  quality_trajectory: ascending/established/declining/emerging/rediscovering
  producer_type: winery/distillery/brewery/tea_garden/coffee_estate/sake_brewery/cidery/meadery/kombucha_brewery/multi_category
  meal_context: aperitif/amuse/starter/fish_course/main/cheese/pre_dessert/dessert/digestif/celebration/casual/any
  pairing_type: complement/contrast/bridge/cleanse/elevate
  confidence: classic/established/suggested/adventurous/experimental
  price_tier: ultra_premium/premium/mid_range/value/entry
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
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_regions
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, country, beverage_family, designation_type, designation_name,
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── GETARIAKO TXAKOLINA DO (Spain) ─────────────────────────────────────────────
print("=== Getariako Txakolina DO ===")
r = R("Getariako Txakolina DO", "Spain", "wine",
      designation_type="DO",
      designation_name="Getariako Txakolina DO",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="The Basque Country's most celebrated Txakoli appellation, producing high-acid, lightly sparkling white wines from Hondarrabi Zuri on coastal Atlantic slopes. The wines' characteristic pour from height creates a natural perlé effervescence. Quintessential aperitif wines for Basque pintxos culture.",
      key_producers="Txomin Etxaniz, Ameztoi, Itsasmendi",
      historical_context="Txakoli wine culture is inextricably linked to Basque identity. The vineyards of Getaria survived phylloxera and nearly disappeared in the 20th century before a revival in the 1980s restored the appellation. DO status granted 1990. Txomin Etxaniz was the pioneer of modern quality Txakoli.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Ideal Atlantic conditions for Hondarrabi Zuri; vibrant freshness and aromatic lift."),
    (2020, "very_good", "stable", "Consistent coastal vintage with characteristic effervescence and citrus-brine character."),
    (2021, "excellent", "rising", "Cool, wet Atlantic conditions produced textbook Txakoli with green apple and sea spray minerality."),
    (2022, "very_good", "stable", "Good balance of fruit and acidity; wines showing slightly more roundness than typical."),
    (2023, "excellent", "rising", "Outstanding Txakoli vintage with great aromatic complexity and signature acid tension."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Txomin Etxaniz", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="The founding estate of modern Txakoli, Txomin Etxaniz farms Hondarrabi Zuri on the coastal slopes above Getaria, producing wines of the highest purity and expression of Basque coastal terroir. The estate's methods set the benchmark for the entire appellation.",
       reputation_narrative="Txomin Etxaniz created modern Txakoli, transforming a dying tradition into an internationally recognised wine style. The estate remains the appellation's defining reference point.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Txomin Etxaniz Getariako Txakolina", "wine_still", p1, r, "Spain",
    subcategory="white", price_tier="mid_range",
    description="The benchmark Txakoli — lightly sparkling Hondarrabi Zuri with electric acidity, green apple, citrus blossom and sea-salt minerality. Poured from height to create natural effervescence.")
if is_new:
    PAIR(prod, "Anchoa de Getaria with pan con tomate", "complement", "classic", "casual", "Getaria's famous anchovies with tomato bread are the quintessential Txakoli pairing.")
    PAIR(prod, "Grilled salt cod (bacalao a la plancha) with pil-pil", "complement", "classic", "main", "Basque salt cod and its emulsified olive-garlic sauce find the perfect acid counterpart in Txakoli.")
    PAIR(prod, "Pintxos bar selection — jamón, anchovy, tortilla", "complement", "classic", "casual", "Txakoli is the defining aperitif wine for San Sebastián pintxos culture.")
    PAIR(prod, "Grilled gambas a la plancha with lemon and olive oil", "cleanse", "classic", "casual", "Electric acid and sea-salt minerality cleanse the grilled prawn richness with coastal freshness.")

prod, is_new = PROD("Txomin Etxaniz Rosé Txakolina", "wine_still", p1, r, "Spain",
    subcategory="rosé", price_tier="mid_range",
    description="Rare Txakoli rosé from Hondarrabi Belza; delicate coral with the signature Txakoli effervescence, red berry and sea-salt freshness of the Getaria coast.")
if is_new:
    PAIR(prod, "Chipirones (baby squid) a la plancha", "complement", "classic", "casual", "Coastal rosé Txakoli matches the delicate sweetness of chargrilled baby squid with its brine minerality.")
    PAIR(prod, "Jamón ibérico with fresh melon", "complement", "established", "casual", "Effervescent rosé's red berry freshness balances the salt intensity of ibérico ham and melon sweetness.")
    PAIR(prod, "Tuna tataki with sesame and ponzu", "complement", "established", "starter", "Txakoli rosé effervescence and sea-salt character mirror the ocean freshness of tuna tataki.")
    PAIR(prod, "Gazpacho with croutons and Ibérico ham", "complement", "suggested", "casual", "Sparkling rosé acidity cuts through gazpacho richness and complements the tomato-pepper freshness.")

p2 = P("Ameztoi", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Ignacio Ameztoi farms steep coastal Txakoli vineyards above the Bay of Biscay, producing wines that capture the extreme expression of Atlantic Basque terroir. The estate is particularly known for its Rubentis rosé and Primus aged white.",
       reputation_narrative="One of Getariako Txakolina's most respected estates, Ameztoi's Rubentis rosé is among Spain's most distinctive and sought-after rosé wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Ameztoi Rubentis Txakolina Rosé", "wine_still", p2, r, "Spain",
    subcategory="rosé", price_tier="premium",
    description="Benchmark Txakoli rosé from Hondarrabi Belza on coastal slate; vivid coral, with vibrant red berry, sea-salt mineral and the characteristic Txakoli effervescence of the Basque coast.")
if is_new:
    PAIR(prod, "Grilled kokotxas (salt cod cheeks) a la Vizcaína", "complement", "classic", "main", "Basque cod cheeks with their silken gelatin and sweet flesh are elevated by this coastal rosé's freshness.")
    PAIR(prod, "Pulpo a la gallega with paprika and potatoes", "complement", "established", "casual", "Sea-mineral Txakoli rosé mirrors the ocean octopus with paprika's smoky complement to effervescence.")
    PAIR(prod, "Tosta de anchoa y tomate cherry", "complement", "classic", "casual", "Anchovy toast with cherry tomato is the definitive Basque bar snack for this rosé Txakoli.")
    PAIR(prod, "Seared scallops with pea purée and pancetta", "complement", "established", "starter", "Effervescent coastal rosé lifts sweet scallop and pea freshness while pancetta salt echoes sea-mineral notes.")

prod, is_new = PROD("Ameztoi Primus Getariako Txakolina", "wine_still", p2, r, "Spain",
    subcategory="white", price_tier="premium",
    description="Aged Txakoli from Hondarrabi Zuri with lees aging; broader, more textured than the classic style with citrus, stone fruit and mineral complexity developed over time.")
if is_new:
    PAIR(prod, "Grilled sole with lemon butter and capers", "complement", "classic", "main", "Aged Txakoli's texture and citrus-mineral character suits the delicacy of Dover sole.")
    PAIR(prod, "Langostinos a la plancha with garlic and parsley", "complement", "classic", "main", "Textured Primus handles grilled langoustine sweetness with mineral precision and lees depth.")
    PAIR(prod, "Risotto al azafrán (saffron risotto)", "complement", "established", "main", "Aged Txakoli's texture and mineral freshness bridges saffron's complexity and the creamy rice.")
    PAIR(prod, "Sea urchin on toasted sourdough with olive oil", "complement", "established", "casual", "Ocean umami intensity of sea urchin is the perfect mineral match for aged, textured Txakoli blanc.")

# ── RIBEIRA SACRA DO (Spain) ──────────────────────────────────────────────────
print("=== Ribeira Sacra DO ===")
r = R("Ribeira Sacra DO", "Spain", "wine",
      designation_type="DO",
      designation_name="Ribeira Sacra DO",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Galicia's most dramatic wine region, where terraced vineyards plunge to the river gorges of the Sil and Miño on impossibly steep slate and granite slopes. Mencía produces deeply mineral, elegant reds of remarkable complexity; Godello and Albariño whites show extraordinary tension and freshness from the altitude and river influence.",
      key_producers="Dominio do Bibei, Guímaro, Envínate",
      historical_context="Ribeira Sacra's monasteries and churches gave the region its name (Sacred River Bank). Viticulture was established by Roman legions and maintained by Benedictine monks for centuries. The extreme terraced viticulture nearly disappeared but was saved by the DO designation in 1996 and championed by a new generation of winemakers.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Outstanding Mencía vintage; cool river gorge conditions produced wines of deep mineral complexity."),
    (2019, "very_good", "stable", "Well-balanced year; Mencía with vivid fruit and slate mineral character throughout."),
    (2020, "very_good", "stable", "Consistent quality; Godello whites of particular freshness from the steep terraced sites."),
    (2021, "excellent", "rising", "Benchmark vintage — long cool season produced Mencía of exceptional freshness and terroir precision."),
    (2022, "very_good", "stable", "Good ripeness with characteristic Galician freshness; Mencía and Godello both performing well."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Dominio do Bibei", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Sara Pérez and René Barbier Jr. at Dominio do Bibei farm extreme terraced vineyards in Ribeira Sacra's Bibei sub-zone, producing wines of extraordinary mineral depth and complexity from old Mencía, Grenache Tintorera and Godello vines on schist and slate.",
       reputation_narrative="The most internationally acclaimed producer of Ribeira Sacra, Dominio do Bibei's wines demonstrate the region's capacity for world-class terroir wine from its extreme slate-terraced vineyards.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Dominio do Bibei Lalama Ribeira Sacra", "wine_still", p1, r, "Spain",
    subcategory="red", price_tier="ultra_premium",
    description="Flagship Mencía from old vines on slate terraces above the Bibei river gorge; profound mineral depth, dark berry, violet and floral complexity with silky tannins and a decade of aging potential.")
if is_new:
    PAIR(prod, "Roasted lacón (pork shoulder) with grelos (turnip greens)", "complement", "classic", "main", "Galicia's most iconic dish — pork and turnip greens — finds its natural partner in slate-mineral Mencía.")
    PAIR(prod, "Slow-roasted lamb with garlic, rosemary and white wine", "complement", "classic", "main", "Slate-mineral Mencía's silky tannins and floral complexity suit slow-roasted Galician lamb beautifully.")
    PAIR(prod, "Duck magret with cherry and red wine reduction", "complement", "established", "main", "Dark berry and violet Mencía mirrors the cherry reduction while handling duck's richness with elegance.")
    PAIR(prod, "Aged Tetilla or San Simón cheese with quince paste", "complement", "established", "cheese", "Galician cow's milk cheese and quince sweetness are the natural regional partners for mineral Mencía.")

prod, is_new = PROD("Dominio do Bibei Lacima Godello Ribeira Sacra", "wine_still", p1, r, "Spain",
    subcategory="white", price_tier="ultra_premium",
    description="Benchmark Godello from Bibei's slate terraces; tense, mineral and complex with stone fruit, white flower and a saline finish from altitude and river-gorge conditions. Among Spain's finest whites.")
if is_new:
    PAIR(prod, "Centolla gallega (Galician spider crab) with mayonnaise", "complement", "classic", "main", "Slate-mineral Godello is the quintessential Galician match for spider crab's sweet delicate flesh.")
    PAIR(prod, "Turbot a la gallega with potatoes and olive oil", "complement", "classic", "main", "Galicia's classic fish preparation demands a white wine of this mineral precision and structural depth.")
    PAIR(prod, "Grilled barnacles (percebes) with sea salt", "complement", "classic", "casual", "Mineral, saline Godello is the ultimate companion for Galicia's prized percebes with their ocean intensity.")
    PAIR(prod, "Eel in parsley sauce (angulas al ajillo)", "complement", "established", "main", "Mineral Godello precision suits the delicate richness of elver in garlic-parsley emulsion.")

p2 = P("Guímaro", "winery", r, "Spain",
       production_philosophy="terroir_focused",
       philosophy_description="Pedro Rodríguez at Guímaro farms old-vine Mencía on the steep slate terraces of Ribeira Sacra's Amandi sub-zone, producing wines that showcase the variety's capacity for floral elegance and mineral depth.",
       reputation_narrative="Guímaro's single-vineyard Finca Meixeman is one of Ribeira Sacra's most acclaimed wines, demonstrating that Spanish Mencía can rival Pinot Noir in complexity and finesse.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Guímaro Finca Meixeman Mencía Ribeira Sacra", "wine_still", p2, r, "Spain",
    subcategory="red", price_tier="ultra_premium",
    description="Single-vineyard Mencía from centenarian vines on Amandi slate; ethereal, floral and deeply mineral with violet, cherry and pencil-shaving complexity from an exceptional site above the Sil river gorge.")
if is_new:
    PAIR(prod, "Roast suckling pig (cochinillo) with herbs", "complement", "established", "main", "Floral, mineral Mencía from old vines suits the crisp skin and delicate pork richness of suckling pig.")
    PAIR(prod, "Grilled pichón (squab) with cherry and lentils", "complement", "classic", "main", "Pigeon's delicate game character and cherry sauce mirror the floral violet intensity of old-vine Mencía.")
    PAIR(prod, "Ceps and truffle pasta with Parmesan", "complement", "established", "main", "Pencil-shaving and forest floor mineral character of Mencía elevate the truffle depth of the pasta.")
    PAIR(prod, "Arzúa-Ulloa or Tetilla cheese with honey", "complement", "established", "cheese", "Galician cow's milk cheese with honey sweetness finds perfect balance with the floral mineral Mencía.")

prod, is_new = PROD("Guímaro Tinto Ribeira Sacra", "wine_still", p2, r, "Spain",
    subcategory="red", price_tier="premium",
    description="Estate Mencía from Guímaro's Amandi terraces; violet, mineral and elegant with cherry fruit and characteristic slate mineral precision — excellent entry to Ribeira Sacra Mencía.")
if is_new:
    PAIR(prod, "Caldo galego (Galician bean and greens soup)", "complement", "classic", "casual", "The everyday mineral Mencía finds its natural companion in Galicia's warming white bean and vegetable soup.")
    PAIR(prod, "Chorizo and bean stew with smoked paprika", "complement", "established", "casual", "Earthy, mineral Mencía handles smoked chorizo and the hearty bean stew with structured freshness.")
    PAIR(prod, "Pulpo a feira (Galician octopus with paprika and olive oil)", "bridge", "established", "casual", "Slate-mineral red wine bridges the ocean character of octopus and the smoky paprika spice.")
    PAIR(prod, "Grilled sardines with Galician sea salt and lemon", "complement", "suggested", "casual", "Mineral, lighter Mencía suits the oily freshness of grilled sardines with Galician sea salt.")

# ── ALENTEJO DOC (Portugal) ───────────────────────────────────────────────────
print("=== Alentejo DOC ===")
r = R("Alentejo DOC", "Portugal", "wine",
      designation_type="DOC",
      designation_name="Alentejo DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Portugal's most commercially successful wine region, covering the vast sun-baked plains south of Lisbon. Alentejo produces warm, richly textured reds from Aragonez (Tempranillo), Trincadeira, Alicante Bouschet and Touriga Nacional, alongside aromatic whites from Antão Vaz and Arinto. The quality from leading sub-regions like Reguengos and Borba rivals Portugal's finest.",
      key_producers="Herdade do Esporão, Herdade Grande, Quinta do Mouro",
      historical_context="Roman viticulture in Alentejo predates modern Portugal. The vast herdades (landed estates) of the region shaped both wine production and social history. Modern Alentejo wine began in the 1990s with investment in temperature-controlled fermentation. Today the region accounts for nearly 20% of Portuguese wine exports.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Superb vintage; warm conditions with cool nights produced Alentejo reds of exceptional depth and freshness."),
    (2019, "very_good", "stable", "Balanced warm year; rich, full-bodied reds with characteristic Alentejo warmth and fruit concentration."),
    (2020, "good", "stable", "Heat and drought stressed some vineyards; irrigated estates produced better results."),
    (2021, "excellent", "rising", "Outstanding vintage — reduced yields and good temperature variation produced Alentejo of remarkable quality."),
    (2022, "very_good", "stable", "Good ripening with characteristic warmth; Aragonez and Alicante Bouschet showing excellent concentration."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Herdade do Esporão", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="The benchmark Alentejo estate, Herdade do Esporão produces the full range of Alentejo wine styles from a vast historic herdade in Reguengos. The estate's commitment to indigenous varieties and sustainable viticulture sets the standard for the region.",
       reputation_narrative="Esporão is the reference point for understanding Alentejo wine at the highest level. Its Reserva red is one of Portugal's most consistently excellent and internationally recognised wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Esporão Reserva Red Alentejo", "wine_still", p1, r, "Portugal",
    subcategory="red", price_tier="premium",
    description="Benchmark Alentejo red from Aragonez, Trincadeira and Cabernet Sauvignon; rich, warm and structured with dark plum, vanilla oak and Mediterranean spice from granite and schist soils of Reguengos.")
if is_new:
    PAIR(prod, "Black Iberian pork secreto with garlic and olive oil", "complement", "classic", "main", "Alentejo's most celebrated meat — Iberian black pig from the cork oak forests — with its fat richness needs warm, structured Esporão.")
    PAIR(prod, "Migas com carne de porco (bread and pork Alentejo stew)", "complement", "classic", "main", "Regional Alentejo dish of fried pork with migas bread finds its ideal regional wine match.")
    PAIR(prod, "Roast leg of lamb with herbs and lemon", "complement", "established", "main", "Warm, structured Alentejo red suits the richness of slow-roasted lamb with Iberian herb seasoning.")
    PAIR(prod, "Queijo Serpa (Alentejo sheep cheese)", "complement", "established", "cheese", "Pungent, creamy Alentejo sheep cheese is the defining regional cheese pairing for this benchmark red.")

prod, is_new = PROD("Esporão Verdelho Alentejo", "wine_still", p1, r, "Portugal",
    subcategory="white", price_tier="mid_range",
    description="Dry Verdelho-based Alentejo white; tropical, rich and aromatic with good acidity retained despite the warm climate. Food-friendly and distinctive from the Reguengos sub-region.")
if is_new:
    PAIR(prod, "Açorda de marisco (Alentejo seafood bread soup)", "complement", "classic", "main", "Tropical, aromatic Verdelho suits this rich Alentejo seafood-bread soup with its garlic and coriander depth.")
    PAIR(prod, "Gambas al pil-pil with garlic and olive oil", "complement", "established", "casual", "Warm Alentejo white's tropical fruit handles garlic-chilli prawn richness with enough structure.")
    PAIR(prod, "Grilled sea bass with grilled tomato and basil", "complement", "established", "main", "Aromatic, tropical white suits the Mediterranean simplicity of grilled sea bass with summer tomato.")
    PAIR(prod, "Queijo fresco (fresh Portuguese cheese) with olive oil", "complement", "suggested", "casual", "Fresh cheese and olive oil are the natural everyday companion to this aromatic Alentejo white.")

p2 = P("Quinta do Mouro", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="Luis Louro at Quinta do Mouro produces one of Alentejo's most distinctive wines from old-vine Aragonez and Trincadeira at Estremoz, applying traditional Bordeaux-influenced techniques to indigenous varieties with remarkable results.",
       reputation_narrative="Quinta do Mouro's flagship red is among Alentejo's most acclaimed and age-worthy wines, demonstrating that the region's indigenous varieties can achieve complexity rivalling Portugal's finest Douro reds.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Quinta do Mouro Alentejo Tinto", "wine_still", p2, r, "Portugal",
    subcategory="red", price_tier="ultra_premium",
    description="Icon of Alentejo from old Aragonez and Trincadeira at Estremoz; concentrated, structured and age-worthy with dark berry, tobacco and mineral depth that can develop for 15+ years.")
if is_new:
    PAIR(prod, "Cordeiro assado (Alentejo roast lamb) with olive oil and garlic", "complement", "classic", "main", "Old-vine Aragonez power and structure handles the full richness of Alentejo's slow-roasted lamb tradition.")
    PAIR(prod, "Carne de porco Alentejana with clams (pork and clams)", "complement", "classic", "main", "Portugal's most distinctive pork-clam combination finds structural support in this powerful Alentejo icon.")
    PAIR(prod, "Wild mushroom and truffle risotto", "complement", "established", "main", "Structured, complex Alentejo handles earthy mushroom and truffle depth with its tobacco-mineral notes.")
    PAIR(prod, "Azeitão or Évora sheep cheese, aged", "complement", "established", "cheese", "Aged Alentejo sheep cheese's pungent intensity is matched by the depth and structure of this icon.")

prod, is_new = PROD("Quinta do Mouro Branco Alentejo", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Premium Alentejo white from Antão Vaz and Roupeiro at Estremoz; rich, textured and mineral with stone fruit, herbal notes and good balancing acidity for the warm climate.")
if is_new:
    PAIR(prod, "Grilled turbot with virgin olive oil and fleur de sel", "complement", "classic", "main", "Textured, mineral Alentejo white suits the pure sweetness of turbot with Iberian olive oil.")
    PAIR(prod, "Sopa de cação (dogfish soup with coriander and bread)", "complement", "established", "main", "Rich, textured white suits this Alentejo fish soup with its distinctive coriander and vinegar depth.")
    PAIR(prod, "Lobster with butter and tarragon", "elevate", "established", "main", "Antão Vaz richness and mineral structure elevates sweet lobster with tarragon into a memorable pairing.")
    PAIR(prod, "Grilled asparagus with aged Serrano ham", "complement", "suggested", "casual", "Herbal, textured white suits the asparagus-ham combination with mineral freshness and structure.")

# ── DÃO DOC (Portugal) ────────────────────────────────────────────────────────
print("=== Dão DOC ===")
r = R("Dão DOC", "Portugal", "wine",
      designation_type="DOC",
      designation_name="Dão DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Portugal's most elegant red wine appellation in the granitic highlands of central Portugal. Touriga Nacional, Tinta Roriz and Alfrocheiro produce refined, mineral reds with natural freshness from altitude; Encruzado whites are among Portugal's most distinctive, with Burgundian texture and aging potential. Once dismissed as rustic, Dão is now recognised as Portugal's answer to Burgundy.",
      key_producers="Quinta dos Roques, Quinta da Pellada, Álvaro Castro",
      historical_context="Dão was one of Portugal's original DOC regions (1908). For decades the cooperative system dominated and suppressed quality. The privatisation of cooperatives in the 1980s allowed pioneering estates to emerge, led by Álvaro Castro whose wines transformed perceptions of Dão's potential from the 1990s onwards.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Cool granite highlands provided freshness; Touriga Nacional of exceptional elegance and mineral precision."),
    (2019, "very_good", "stable", "Balanced year with characteristic Dão freshness from altitude; reds of fine structure and Encruzado whites of texture."),
    (2020, "very_good", "stable", "Consistent quality; Encruzado whites showed particular complexity with good aging structure."),
    (2021, "excellent", "rising", "Outstanding vintage — cool, long season produced Dão reds of benchmark minerality and Burgundian finesse."),
    (2022, "very_good", "stable", "Good balance of ripe fruit and highland freshness; Touriga Nacional of genuine complexity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Álvaro Castro", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Álvaro Castro transformed Dão's reputation single-handedly through meticulous single-vineyard work with Touriga Nacional and Encruzado, demonstrating the region's capacity for wines of genuine elegance, mineral depth and age-worthiness.",
       reputation_narrative="The founding father of modern Dão wine, Álvaro Castro's Pelada and Quinta da Pellada wines are responsible for placing Dão among Portugal's most respected appellations internationally.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Álvaro Castro Pelada Dão Tinto", "wine_still", p1, r, "Portugal",
    subcategory="red", price_tier="ultra_premium",
    description="Flagship single-vineyard Dão from old Touriga Nacional and Tinta Roriz on granite; ethereal, mineral and complex with violet, red berry, herbal notes and extraordinary finesse for a southern European red.")
if is_new:
    PAIR(prod, "Roast suckling kid (cabrito assado) with potatoes", "complement", "classic", "main", "Dão's most celebrated dish — roast kid goat — is inseparable from the mineral elegance of Touriga Nacional.")
    PAIR(prod, "Roast grouse with bread sauce and game jus", "complement", "established", "main", "The wine's haunting violet and mineral complexity suits delicate game birds with traditional accompaniments.")
    PAIR(prod, "Mushroom and truffle ravioli with sage butter", "complement", "established", "main", "Violet and mineral Dão Touriga Nacional resonates beautifully with earthy truffle and wild mushroom pasta.")
    PAIR(prod, "Serra da Estrela cheese with honey and walnuts", "complement", "established", "cheese", "Portugal's finest sheep cheese with runny texture and strong character finds balance in mineral, elegant Dão.")

prod, is_new = PROD("Álvaro Castro Encruzado Dão Branco", "wine_still", p1, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Benchmark Encruzado from Quinta da Pellada's granite soils; textured, mineral and complex with stone fruit, hazelnut, floral notes and Burgundian structure — Portugal's finest white variety at its peak.")
if is_new:
    PAIR(prod, "Grilled sea bass with green herb sauce", "complement", "classic", "main", "Mineral, textured Encruzado suits sea bass with herbal sauce matching the wine's floral-mineral complexity.")
    PAIR(prod, "Sopa de castanha com couve (chestnut and cabbage soup)", "complement", "established", "main", "Mineral, hazelnut-textured white suits this Dão mountain soup with its earthy chestnut depth.")
    PAIR(prod, "Grilled sole with lemon butter and almonds", "complement", "established", "main", "Encruzado's hazelnut texture and stone fruit suit sole with almond butter beautifully.")
    PAIR(prod, "Aged Castelo Branco cheese with fig preserve", "complement", "established", "cheese", "Aged semi-hard Portuguese cheese and fig sweetness find the right mineral frame in textured Encruzado.")

p2 = P("Quinta dos Roques", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="One of Dão's leading estate wineries, Quinta dos Roques produces single-variety expressions of Dão's indigenous grapes — Touriga Nacional, Alfrocheiro, Encruzado, Tinta Roriz — that showcase the region's granite terroir and highland freshness.",
       reputation_narrative="Quinta dos Roques's approach to varietal transparency and granite-terroir expression has made it one of the most respected references for Dão's diverse indigenous variety portfolio.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Quinta dos Roques Touriga Nacional Dão", "wine_still", p2, r, "Portugal",
    subcategory="red", price_tier="premium",
    description="Single-varietal Touriga Nacional from Dão granite; floral, mineral and structured with violet, dark cherry and herbal complexity that defines Dão's unique take on Portugal's greatest red grape.")
if is_new:
    PAIR(prod, "Roast rack of lamb with herbes de Provence and potato gratin", "complement", "classic", "main", "Touriga Nacional's violet-herbal complexity and fine tannins are a natural match for rack of lamb.")
    PAIR(prod, "Alheira de Mirandela (Dão-style game sausage) with fried egg", "complement", "classic", "main", "Regional smoked game sausage is the traditional Dão companion for single-varietal Touriga Nacional.")
    PAIR(prod, "Venison medallions with port and berry reduction", "complement", "established", "main", "Dark game and port-berry reduction find structural support in the violet-mineral depth of Dão Touriga.")
    PAIR(prod, "Champalimaud (aged Dão sheep cheese) or similar", "complement", "established", "cheese", "Regional aged sheep cheese with the mineral, floral structure of single-varietal Touriga Nacional.")

prod, is_new = PROD("Quinta dos Roques Encruzado Dão Branco", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="premium",
    description="Textured, mineral Encruzado from Quinta dos Roques granite; stone fruit, hazelnut and floral character with genuine aging potential from Dão's cool granite highlands.")
if is_new:
    PAIR(prod, "Bacalhau com grão (salt cod with chickpeas and olive oil)", "complement", "classic", "main", "Textured, mineral Encruzado provides the acid freshness and mineral frame for this Portuguese classic.")
    PAIR(prod, "Grilled squid with coriander and lemon oil", "complement", "established", "main", "Mineral, stone-fruit white suits the sweetness of grilled squid with herb brightness.")
    PAIR(prod, "Papas de sarrabulho (Dão pork blood rice)", "complement", "classic", "main", "Dão's rich regional offal preparation finds the mineral structure and freshness of Encruzado essential.")
    PAIR(prod, "Aged Mealhada cheese with quince paste", "complement", "suggested", "cheese", "Aged Portuguese cow's milk cheese and quince sweetness find the right mineral frame in textured Encruzado.")

# ── FINAL COUNTS ──────────────────────────────────────────────────────────────
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
print("B137 complete.")
conn.close()
