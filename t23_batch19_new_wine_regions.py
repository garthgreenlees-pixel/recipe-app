#!/usr/bin/env python3
"""T23 Batch 19 — New wine regions: Nahe (Germany), Hemel-en-Aarde Valley WO (South Africa), Hawkes Bay GI (New Zealand), Carnuntum DAC (Austria), Sonoma Coast AVA (USA)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, beverage_family, designation_type, designation_name,
       reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
      (name, country, region_id, producer_type, reputation_narrative, authority_tier)
      VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── NAHE (GERMANY) ────────────────────────────────────────────────
print("\n=== Nahe (Germany) ===")
r_nah = R("Nahe", "Germany", "wine",
           designation_type="Qualitätswein",
           designation_name="Nahe Qualitätswein",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Germany's most geologically diverse and fascinating wine region along the Nahe River between Mainz and Bingen, bridging the richness of the Pfalz and the mineral precision of the Mosel. The Nahe's extraordinary geological complexity — volcanic porphyry, blue slate, sandstone, quartzite, and copper deposits — creates wines of unusual mineral intensity and aromatic diversity that defy easy categorization. Schlossbockelheim and Niederhausen are the premium sub-zones producing Germany's most mineral and complex Rieslings.",
           key_producers="Dönnhoff, Emrich-Schönleber, Schäfer-Fröhlich, Gut Hermannsberg, Matthias Dostert",
           historical_context="The Nahe's Schlossbockelheim estate, owned by the Prussian state from 1902, was instrumental in establishing the region's reputation for world-class Riesling. Helmut Dönnhoff's ascent in the 1980s-90s brought the region to international attention — his Oberhäuser Brücke Riesling from copper and porphyry volcanic soils is considered by many Germany's finest single-vineyard wine. Emrich-Schönleber's Monzingen plots on blue-grey slate further expanded the region's critical acclaim.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Nahe vintage; Schlossbockelheim porphyry and blue slate produced Riesling of extraordinary mineral complexity."),
    (2021, "very_good", "stable", "Elegant vintage; the geological diversity of the Nahe produced wines of exceptional aromatic precision from each soil type."),
    (2020, "excellent", "stable", "Benchmark year; Dönnhoff Oberhäuser Brücke and Emrich-Schönleber Frühlingsplätzchen received Germany's highest critical scores."),
    (2019, "exceptional", "rising", "Greatest Nahe vintage of the modern era; copper-soil Riesling from Schlossbockelheim reached legendary complexity."),
    (2018, "excellent", "stable", "Excellent vintage; Nahe's diverse geology expressed itself with unusual clarity; volcanic porphyry wines were exceptional."),
]:
    VIN(r_nah, yr, qd, pt, sn)

p_don = P("Dönnhoff", "Germany", r_nah,
           description="Helmut and Cornelius Dönnhoff's Oberhausen estate producing Germany's most internationally acclaimed Nahe Riesling from volcanic porphyry and copper-rich soils. The Oberhäuser Brücke Auslese and GG Rieslings are considered benchmark expressions of German Riesling's mineral potential; Dönnhoff is consistently rated among Germany's five greatest wine estates.")
prod_don_r, new = PROD("Dönnhoff Oberhäuser Brücke Riesling Spätlese", "wine_still", p_don, r_nah, "Germany",
                        subcategory="Riesling",
                        description="Germany's most mineral and complex Spätlese from the volcanic porphyry and copper-rich Brücke vineyard — a wine of extraordinary tension between sweetness, acidity, and mineral intensity. Peach, apricot, mineral volcanic smoke, white flower, and copper — a wine that expresses its unique geological origins with unmatched clarity.",
                        price_tier="ultra_premium")
if new:
    PAIR(prod_don_r, "Freshwater trout (Forelle Müllerin) with almonds, brown butter, and lemon", "complement", "classic", "main", "Nahe's most prized freshwater fish and its finest Riesling — the wine's minerality and citrus character is perfect for the delicate trout; almond and brown butter mirror the wine's fruit")
    PAIR(prod_don_r, "Spicy Vietnamese bo bun with lemongrass beef, fresh herbs, and peanuts", "complement", "established", "main", "Off-dry Nahe Riesling and Southeast Asian spice — the wine's residual sugar and copper mineral character bridges lemongrass; acidity refreshes through the chilli heat")

p_esr = P("Emrich-Schönleber", "Germany", r_nah,
           description="Frank and Werner Schönleber's Monzingen estate producing benchmark Nahe Riesling from blue-grey slate Halenberg and Frühlingsplätzchen vineyards. Often described as the Nahe's 'Mosel in miniature', Emrich-Schönleber's wines have a more delicate, linear style than Dönnhoff's volcanic expression — together they represent the Nahe's full range.")
prod_esr, new = PROD("Emrich-Schönleber Halenberg Grosses Gewächs Riesling", "wine_still", p_esr, r_nah, "Germany",
                     subcategory="Riesling",
                     description="Bone-dry Nahe GG Riesling from the blue-grey slate Halenberg — one of Germany's most mineral and linear Grosses Gewächs. Lemon zest, white flower, slate, white pepper, and an elegant precision reminiscent of Mosel but with more textural weight from the Nahe's warmer microclimate.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_esr, "Steamed halibut with champagne foam, caviar, and chive butter", "complement", "classic", "main", "The wine's mineral precision and citrus character meets the luxury of halibut and caviar; the wine's GG weight provides structure without dominating the delicate fish")
    PAIR(prod_esr, "Prawn tempura with ponzu dipping sauce and daikon radish", "complement", "established", "starter", "Dry Nahe Riesling's mineral freshness and citrus character refreshes through the tempura batter; ponzu's citrus echoes the wine; the wine's mineral length complements the prawn's brine")

# ── HEMEL-EN-AARDE VALLEY WO (SOUTH AFRICA) ───────────────────────
print("\n=== Hemel-en-Aarde Valley WO (South Africa) ===")
r_hem = R("Hemel-en-Aarde Valley", "South Africa", "wine",
           designation_type="WO",
           designation_name="Hemel-en-Aarde Valley WO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="The 'Heaven and Earth Valley' near Hermanus on the Western Cape coast — South Africa's coolest and most Burgundian wine ward, producing Pinot Noir and Chardonnay of international distinction from decomposed shale, clay, and red clay soils at 200-400m altitude. The three wards (Hemel-en-Aarde Valley, Upper Hemel-en-Aarde Valley, and Hemel-en-Aarde Ridge) each express different aspects of the cool maritime climate influenced by Walker Bay.",
           key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Storm Wines, Newton Johnson",
           historical_context="Tim Hamilton Russell planted the valley's first vines in 1975 after years of argument with South Africa's Wine and Spirit Board, who believed grapes could not ripen this far south. Hamilton Russell's determination proved them wrong and established Hemel-en-Aarde as Africa's finest cool-climate wine ward. The valley's Burgundian reputation grew steadily through the 1990s as the Pinot Noir and Chardonnay demonstrated genuine terroir expression.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Hemel-en-Aarde vintage; Pinot Noir from decomposed shale soils showed extraordinary mineral transparency."),
    (2021, "very_good", "stable", "Classic vintage; the Walker Bay maritime influence produced wines of exceptional Burgundian elegance and precision."),
    (2020, "exceptional", "rising", "Finest Hemel-en-Aarde vintage in the modern era; Hamilton Russell and Newton Johnson produced internationally acclaimed Pinot."),
    (2019, "excellent", "stable", "Benchmark year; Storm Wines and Creation produced Chardonnay of exceptional mineral complexity and aging potential."),
    (2018, "very_good", "stable", "Solid vintage; the valley's cool maritime conditions produced Pinot Noir and Chardonnay of fine aromatic precision."),
]:
    VIN(r_hem, yr, qd, pt, sn)

p_hrv = P("Hamilton Russell Vineyards", "South Africa", r_hem,
           description="Tim and Anthony Hamilton Russell's Hemel-en-Aarde Valley estate — South Africa's most internationally recognized and influential cool-climate winery. The HRV Pinot Noir and Chardonnay, the only two wines produced, are consistently Africa's most critically acclaimed wines and ranked among the world's great Burgundian-style expressions.")
prod_hrv, new = PROD("Hamilton Russell Vineyards Pinot Noir", "wine_still", p_hrv, r_hem, "South Africa",
                     subcategory="Pinot Noir",
                     description="Africa's most celebrated Pinot Noir from the Hemel-en-Aarde Valley's decomposed shale and clay — silky, transparent, and genuinely Burgundian in character. Red cherry, dried rose petal, forest floor, iron, and the distinctive cool Walker Bay mineral freshness. Demands 5-10 years of aging to reveal its full complexity.",
                     price_tier="premium")
if new:
    PAIR(prod_hrv, "Springbok loin with black cherry jus, truffle oil, and celeriac purée", "complement", "classic", "main", "South Africa's most elegant game and its most elegant Pinot Noir — springbok's lean gaminess is lifted by the wine's cherry transparency; truffle mirrors the forest floor notes")
    PAIR(prod_hrv, "Roasted free-range chicken with wild mushroom cream sauce and new potatoes", "complement", "classic", "main", "Hemel-en-Aarde Pinot Noir and free-range poultry is a celebrated South African fine dining classic; the mushroom cream mirrors the wine's forest floor character")

p_new = P("Newton Johnson Wines", "South Africa", r_hem,
           description="Gordon and Nadia Newton Johnson's family estate in the Upper Hemel-en-Aarde Valley producing some of South Africa's most internationally acclaimed Pinot Noir and Chardonnay from decomposed shale soils. The Full Stop Rock and Felicite Pinot Noir are considered Hemel-en-Aarde's finest alongside Hamilton Russell.")
prod_new, new = PROD("Newton Johnson Family Vineyards Chardonnay", "wine_still", p_new, r_hem, "South Africa",
                     subcategory="Chardonnay",
                     description="Africa's most refined Chardonnay from Upper Hemel-en-Aarde shale — white peach, hazelnut, lemon blossom, struck flint, and the cool Walker Bay maritime minerality that sets this apart from South African warm-climate Chardonnay. Burgundian in orientation; genuinely age-worthy and profound.",
                     price_tier="premium")
if new:
    PAIR(prod_new, "Grilled Cape lobster with lemon butter, tarragon, and crusty sourdough", "complement", "classic", "main", "Walker Bay lobster and Walker Bay Chardonnay — one of South Africa's great regional pairings; the wine's hazelnut and lemon character mirrors the lobster's sweetness; butter bridges")
    PAIR(prod_new, "Line fish ceviche with leche de tigre, avocado, and micro herbs", "complement", "established", "starter", "South African line fish marinated in citrus and the valley's finest Chardonnay — the wine's mineral freshness and citrus notes bridge the ceviche; avocado mirrors the wine's texture")

# ── HAWKES BAY GI (NEW ZEALAND) ───────────────────────────────────
print("\n=== Hawkes Bay GI (New Zealand) ===")
r_haw = R("Hawkes Bay", "New Zealand", "wine",
           designation_type="GI",
           designation_name="Hawkes Bay GI",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="New Zealand's second largest wine region on the eastern coast of the North Island, producing the country's finest red wines from Cabernet Sauvignon, Merlot, Syrah, and Malbec alongside exceptional Chardonnay. The Gimblett Gravels sub-zone — a former riverbed of free-draining shingle and loam soils — is New Zealand's most distinctive red wine terroir, producing Bordeaux and Rhône-style reds of international quality. The maritime climate creates wines of greater warmth and structure than Marlborough.",
           key_producers="Craggy Range, Te Mata Estate, Trinity Hill, Elephant Hill, Church Road",
           historical_context="Hawkes Bay's Mission Estate (1851) is New Zealand's oldest winery, established by Marist Brothers. The region was the country's most important until Marlborough's Sauvignon Blanc surge in the 1980s. The discovery of the Gimblett Gravels' potential for premium red wines in the 1980s — particularly by John Buck at Te Mata — repositioned Hawkes Bay as New Zealand's red wine heartland. The Gimblett Gravels Winegrowers Association was established in 2001 to protect and market the distinctive sub-zone.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Hawkes Bay vintage; Gimblett Gravels Syrah and Cabernet showed extraordinary depth and Rhône-comparable complexity."),
    (2021, "very_good", "stable", "Classic vintage; the North Island's warmth produced Merlot and Syrah of excellent structure and dark fruit intensity."),
    (2020, "excellent", "stable", "Benchmark year; Craggy Range and Te Mata produced internationally acclaimed Gimblett Gravels reds of exceptional quality."),
    (2019, "exceptional", "rising", "Greatest Hawkes Bay vintage of the modern era; Syrah achieved New Zealand's highest critical scores from this sub-region."),
    (2018, "very_good", "stable", "Solid vintage; Chardonnay from Bridge Pa Triangle showed excellent mineral freshness; Cabernet of excellent structure."),
]:
    VIN(r_haw, yr, qd, pt, sn)

p_cra = P("Craggy Range Winery", "New Zealand", r_haw,
           description="Terry Peabody's flagship New Zealand estate spanning Hawkes Bay, Martinborough, and Marlborough, producing the country's most ambitious and critically acclaimed wines. The Gimblett Gravels Sophia (Merlot blend) and The Quarry (Cabernet blend) are New Zealand's most successful Bordeaux-style red wines; Le Sol Syrah is considered New Zealand's greatest Syrah.")
prod_cra, new = PROD("Craggy Range Le Sol Syrah", "wine_still", p_cra, r_haw, "New Zealand",
                     subcategory="Syrah",
                     description="New Zealand's most internationally acclaimed Syrah — Gimblett Gravels shingle soils producing a Syrah of extraordinary Northern Rhône character. Dark plum, white pepper, olive, smoked meat, and the distinctive cool-climate freshness that sets New Zealand Syrah apart. One of the Southern Hemisphere's finest Syrah expressions.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_cra, "New Zealand venison rack with spiced jus, kumara purée, and crispy sage", "complement", "classic", "main", "NZ game and NZ's finest Syrah — the wine's pepper and smoked meat character mirrors the venison's gaminess; kumara's earthiness bridges; sage echoes the wine's herb complexity")
    PAIR(prod_cra, "Char-grilled hanger steak with chimichurri, grilled corn, and aged cheddar", "complement", "established", "main", "Syrah's dark fruit and smoked meat character handles the char-grilled intensity; chimichurri's herb freshness mirrors the wine's complexity; aged cheddar adds structural resonance")

p_tem = P("Te Mata Estate", "New Zealand", r_haw,
           description="New Zealand's oldest wine estate (1892) and John Buck's lifelong project to prove that Hawkes Bay could produce great Cabernet Sauvignon-dominant red wines. Coleraine — Te Mata's flagship Cabernet Sauvignon, Merlot, and Cabernet Franc blend — is New Zealand's most age-worthy and consistently critically acclaimed red wine.")
prod_tem_n, new = PROD("Te Mata Coleraine", "wine_still", p_tem, r_haw, "New Zealand",
                        subcategory="Cabernet Sauvignon Blend",
                        description="New Zealand's most celebrated Bordeaux blend from Hawkes Bay's ancient river terraces — Cabernet Sauvignon, Merlot, and Cabernet Franc producing a wine of extraordinary elegance and aging potential. Blackcurrant, cedar, dark chocolate, tobacco leaf, and the distinctive NZ cool-climate freshness. Develops magnificently over 15-20 years.",
                        price_tier="ultra_premium")
if new:
    PAIR(prod_tem_n, "Roasted Canterbury lamb saddle with red wine jus, pomme dauphinoise, and wilted spinach", "complement", "classic", "main", "New Zealand's finest Bordeaux blend and NZ lamb — the wine's cedar and blackcurrant character handles the lamb's mineral depth; pomme dauphinoise's cream provides textural contrast")
    PAIR(prod_tem_n, "Aged Kapiti Aged Gouda with walnut, dried fig, and quince cheese", "complement", "established", "cheese", "The wine's cedar and tobacco complexity finds resonance in aged New Zealand gouda; walnut bridges the wine's tannins; dried fig mirrors the wine's dark fruit")

# ── CARNUNTUM DAC (AUSTRIA) ───────────────────────────────────────
print("\n=== Carnuntum DAC (Austria) ===")
r_car = R("Carnuntum", "Austria", "wine",
           designation_type="DAC",
           designation_name="Carnuntum DAC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Austria's most easterly wine DAC in the Pannonian plain east of Vienna, producing Austria's finest Zweigelt and distinctive Blaufränkisch from warm panonnian clay soils on the ancient Roman settlement of Carnuntum. The warm continental climate creates richer, more opulent wines than the Wachau or Kamptal — Austria's equivalent of Burgundy's Côte Chalonnaise with an emphasis on structured reds rather than whites.",
           key_producers="Gerhard Markowitsch, Dorli Muhr, Netzl, Artner, Schreibeis",
           historical_context="The ancient Roman city of Carnuntum was one of the empire's most important Danubian fortresses — Emperor Marcus Aurelius wrote part of his Meditations here. Wine was produced on these terraces for Roman legions stationed at the frontier. The modern DAC designation (2019) recognized Carnuntum's distinctiveness from Niederösterreich; Dorli Muhr-van der Niepoort's Spitzerberg Blaufränkisch established the region's international credentials.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Carnuntum vintage; Zweigelt from Pannonian clay showed extraordinary dark cherry intensity; Blaufränkisch of fine structure."),
    (2021, "very_good", "stable", "Classic vintage; the continental conditions produced Zweigelt of excellent varietal character and food-friendly freshness."),
    (2020, "excellent", "stable", "Benchmark year; Markowitsch and Muhr-van der Niepoort produced Zweigelt and Blaufränkisch of exceptional quality."),
    (2019, "very_good", "rising", "Outstanding vintage; first year of the DAC designation; Carnuntum's distinctive Pannonian character celebrated internationally."),
    (2018, "excellent", "stable", "Excellent vintage; warm conditions produced Zweigelt of unusual concentration and Blaufränkisch of impressive structure."),
]:
    VIN(r_car, yr, qd, pt, sn)

p_mar = P("Gerhard Markowitsch", "Austria", r_car,
           description="Carnuntum's most internationally visible producer, farming biodynamically and producing Zweigelt, Blaufränkisch, and Grüner Veltliner of excellent quality. Markowitsch's Carnuntum Cuvée and single-vineyard Götlesbrunn Zweigelt have established the region's reputation for world-class red wine.")
prod_mar, new = PROD("Markowitsch Carnuntum Zweigelt", "wine_still", p_mar, r_car, "Austria",
                     subcategory="Zweigelt",
                     description="Austria's most approachable and food-friendly red variety at its Carnuntum best — Zweigelt's characteristic sour cherry, dark plum, and peppery freshness from Pannonian clay soils. More structured than Vienna DAC's examples; excellent with Austrian cuisine and ideal for restaurant by-the-glass.",
                     price_tier="mid_range")
if new:
    PAIR(prod_mar, "Tafelspitz (boiled prime beef) with Apfelkren (apple horseradish) and chives", "complement", "classic", "main", "Austria's national boiled beef dish and its native red variety — Zweigelt's sour cherry acidity mirrors the Apfelkren's freshness; the wine's light tannins complement rather than fight the delicate beef")
    PAIR(prod_mar, "Grilled Wiener Bratwurst with potato salad, mustard, and bread roll", "complement", "classic", "aperitif", "The Vienna sausage and Carnuntum Zweigelt is a natural Austrian pub pairing; the wine's cherry freshness and light structure is ideal for the grilled pork sausage")

p_muh = P("Dorli Muhr", "Austria", r_car,
           description="Dorli Muhr's Carnuntum estate and Dirk van der Niepoort joint project producing the region's most internationally acclaimed Blaufränkisch from the Spitzerberg — a limestone and clay hillside producing Austria's most Burgundy-like red wines. Spitzerberg Blaufränkisch has won major international awards and established Carnuntum's credibility for fine wine.")
prod_muh, new = PROD("Muhr van der Niepoort Spitzerberg Blaufrankisch", "wine_still", p_muh, r_car, "Austria",
                     subcategory="Blaufrankisch",
                     description="Austria's most internationally acclaimed Blaufränkisch from Carnuntum's limestone Spitzerberg — elegant, cool-climate in style, with dark cherry, iron, forest floor, and a precision that recalls great Burgundy more than Pannonian red wine. One of Austria's finest red wines and a revelation of Blaufränkisch's world-class potential.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_muh, "Roasted duck breast with Rotkraut (red cabbage), Serviettenknödel, and red wine jus", "complement", "classic", "main", "The Pannonian tradition's most celebrated combination — duck and Blaufränkisch; the wine's iron and cherry character mirrors the red cabbage; the jus bridges the wine's complexity")
    PAIR(prod_muh, "Grilled venison with Preiselbeeren (lingonberries), celeriac, and aged Emmental", "complement", "established", "main", "Alpine game and Carnuntum's finest red — Blaufränkisch's cool mineral character and dark cherry lifts the venison's gaminess; lingonberry mirrors the wine's acidity")

# ── SONOMA COAST AVA (USA) ────────────────────────────────────────
print("\n=== Sonoma Coast AVA (USA) ===")
r_soc = R("Sonoma Coast", "USA", "wine",
           designation_type="AVA",
           designation_name="Sonoma Coast AVA",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="California's most diverse and dramatic coastal AVA stretching from the Petaluma Wind Gap in the south to Fort Ross on the Mendocino border — one of the world's most climatically complex wine regions. The 'True Sonoma Coast' or 'West Sonoma Coast' sub-zone directly influenced by Pacific Ocean fog produces Pinot Noir and Chardonnay of extraordinary mineral precision and Burgundian elegance. Producers like Peay, Hirsch, and Flowers work in conditions so cool they challenge ripeness annually.",
           key_producers="Peay Vineyards, Hirsch Vineyards, Flowers, Littorai, Williams Selyem",
           historical_context="The extreme True Sonoma Coast was not planted until the 1990s, when pioneers like David Hirsch recognized that direct Pacific exposure could produce Pinot Noir of unprecedented mineral complexity in California. The Sonoma Coast's reputation for ocean-influenced wines grew dramatically through the 2000s as critics recognized that the best True Sonoma Coast Pinot rivaled Burgundy's finest village wines. The term 'West Sonoma Coast' was proposed as a more precise sub-AVA to distinguish direct ocean-influenced sites.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Sonoma Coast vintage; True Coast Pinot Noir showed extraordinary ocean mineral transparency and Burgundian elegance."),
    (2021, "very_good", "stable", "Classic vintage; Peay and Hirsch vineyards produced cool-climate Pinot of exceptional freshness and mineral precision."),
    (2020, "very_good", "stable", "Challenging smoke-taint vintage for some; ocean-influenced True Coast sites with natural ventilation produced excellent wines."),
    (2019, "exceptional", "rising", "Greatest Sonoma Coast vintage of the modern era; Williams Selyem and Littorai produced wines of legendary quality."),
    (2018, "excellent", "stable", "Benchmark year; Peay's En Chamberlin and Hirsch's San Andreas Fault Pinot Noir received California's highest critical scores."),
]:
    VIN(r_soc, yr, qd, pt, sn)

p_pea = P("Peay Vineyards", "USA", r_soc,
           description="Nick and Vanessa Peay's extreme West Sonoma Coast estate at Annapolis — one of California's most remote and ocean-influenced wineries. Peay's Pinot Noir, Chardonnay, and Syrah from their fog-shrouded ridge vineyards are consistently California's most mineral and distinctive, with a freshness and transparency that recalls Burgundy and the Northern Rhône rather than warm-climate California.")
prod_pea, new = PROD("Peay En Chamberlin Pinot Noir", "wine_still", p_pea, r_soc, "USA",
                     subcategory="Pinot Noir",
                     description="California's most mineral and ocean-influenced Pinot Noir from Peay's coastal ridge above the fog line. Wild strawberry, cranberry, sea salt, iron, dried rose petal, and the haunting ocean freshness that makes this unlike any other California Pinot Noir. Genuinely transparent and age-worthy; Burgundy in Pacific terms.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_pea, "Grilled Pacific salmon with pinot reduction, chanterelles, and wild herbs", "complement", "classic", "main", "West Coast salmon from the same Pacific Ocean that defines this wine — the Pinot's ocean mineral character mirrors the salmon's freshness; chanterelles echo the forest floor notes")
    PAIR(prod_pea, "Seared California abalone with nori butter, dashi, and sea vegetables", "complement", "established", "main", "The ocean's finest shellfish and the ocean's most mineral California Pinot — the wine's sea salt and iron character bridges the abalone's brine; nori amplifies the ocean connection")

p_hir = P("Hirsch Vineyards", "USA", r_soc,
           description="David Hirsch's pioneer Sonoma Coast estate in the remote Fort Ross-Seaview territory — one of California's most extreme and influential wine properties. Hirsch's wines, now made by Jasmine Hirsch, are consistently California's most distinctive and mineral Pinot Noir from San Andreas Fault-influenced soils at 900-1200 feet with direct Pacific exposure.")
prod_hir, new = PROD("Hirsch San Andreas Fault Pinot Noir", "wine_still", p_hir, r_soc, "USA",
                     subcategory="Pinot Noir",
                     description="Named for the tectonic fault that runs through the estate — Hirsch's benchmark Sonoma Coast Pinot Noir from the most extreme ocean-influenced site in California. Cranberry, dried herbs, iron oxide, sea spray, and the mineral complexity of Franciscan Complex soils on the fault. One of California's most distinctive and terroir-expressive Pinot Noir wines.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_hir, "Dungeness crab with Meyer lemon aioli, fennel salad, and sourdough", "complement", "classic", "main", "Pacific coastal Pinot Noir and Pacific Dungeness crab — the wine's ocean mineral character and cranberry acidity mirrors the crab's sweetness; fennel bridges the wine's herbal complexity")
    PAIR(prod_hir, "Roasted beet salad with chevre, candied walnuts, and sherry vinaigrette", "complement", "established", "starter", "The wine's iron and mineral character finds natural resonance with earthy beets; chevre's tanginess bridges the Pinot's acidity; walnuts add textural contrast")

# ── FINAL COUNT ──────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nTotal regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")

cur.close()
conn.close()
print("\nDone.")
