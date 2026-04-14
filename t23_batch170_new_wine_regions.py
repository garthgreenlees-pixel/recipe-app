#!/usr/bin/env python3
"""B170 — Paso Robles AVA, Sta. Rita Hills AVA, Yamanashi Japan, Ningxia China, Dalmatia Croatia"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
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
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === PASO ROBLES AVA ===
print("=== Paso Robles AVA ===")
r1 = R("Paso Robles AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Paso Robles American Viticultural Area",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Paso Robles in San Luis Obispo County is California's most dynamic wine region, known for Rhône varieties (Grenache, Syrah, Mourvèdre), Zinfandel, and Cabernet Sauvignon. The Adelaida District's calcareous soils and the Willow Creek District's clay soils provide distinct sub-terroirs. Day-night temperature swings of up to 50°F preserve freshness despite the warm climate. Justin Winery's Isosceles blend and Tablas Creek's Rhône varieties have established Paso as a world-class Rhône-influenced region.",
       key_producers="Tablas Creek Vineyard, Justin Winery, Saxum Vineyards, L'Aventure Winery, Denner Vineyards",
       historical_context="Paso Robles wine production began in the 1790s at Mission San Miguel, but the modern era started in the 1970s. The region exploded in the 1990s-2000s when Tablas Creek imported Rhône cuttings directly from Château de Beaucastel and Saxum began producing Rhône blends that achieved national critical acclaim.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Outstanding Paso vintage — Rhône varieties of exceptional concentration and balance."),
    (2020,"very_good","stable","Good vintage despite regional challenges; Grenache and Syrah showing excellent quality."),
    (2021,"excellent","rising","Landmark year; calcareous Adelaida District wines achieving international recognition."),
    (2022,"very_good","stable","Warm vintage; rich, opulent GSM blends with the region's characteristic fruit density."),
    (2023,"excellent","rising","Exceptional conditions; Rhône blends of benchmark quality across the AVA."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Tablas Creek Vineyard Paso Robles", "winery", r1, "USA",
       production_philosophy="organic",
       philosophy_description="Tablas Creek was founded in 1989 as a partnership between Beaucastel and Robert Haas to establish California's finest Rhône variety producer. Using cuttings imported directly from Château de Beaucastel, the estate farms organically and produces Châteauneuf-du-Pape-inspired blends alongside single-variety expressions.",
       reputation_narrative="Tablas Creek has been the standard-bearer for California Rhône wines since its founding — their Esprit de Beaucastel red and white blends are California's most authentic expressions of the Châteauneuf style, and their variety importation programme has benefited the entire California wine industry.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Tablas Creek Esprit de Beaucastel Rouge Paso Robles", "wine_still", p1, r1, "USA",
                    subcategory="red", description="Mourvèdre-dominant Châteauneuf-inspired blend with Grenache, Syrah, and Counoise from calcareous soils. Dark fruit, lavender, garrigue, leather, and the structured tannins of old-vine Mourvèdre — California's most authentic Southern Rhône expression.", price_tier="premium")
if is_new:
    PAIR(prod, "Slow-roasted lamb shoulder with herbes de Provence", "complement", "classic", "main", "Mourvèdre's garrigue and dark fruit mirror Provençal lamb preparation — a California interpretation of the classic Southern Rhône match.")
    PAIR(prod, "Wild boar sausage with lentils and herbs", "complement", "established", "main", "The wine's Mourvèdre backbone handles boar's gaminess; lentils echo the dark, earthy character of the blend.")
    PAIR(prod, "Grilled beef ribs with black pepper and chimichurri", "complement", "classic", "main", "Paso Robles' warm-climate concentration stands up to grilled beef; chimichurri's herbs mirror the wine's garrigue notes.")
    PAIR(prod, "Aged Manchego with membrillo and rosemary crackers", "complement", "established", "cheese", "The wine's dark fruit and garrigue complement Manchego's nuttiness; rosemary bridges the herbal notes.")
prod, is_new = PROD("Saxum James Berry Vineyard Paso Robles Red", "wine_still", p1, r1, "USA",
                    subcategory="red", description="Saxum's flagship single-vineyard GSM from calcareous James Berry Vineyard in the Willow Creek District. Opulent — dark cherry, boysenberry, lavender, white pepper, and a mineral calcium backbone. One of California's most coveted cult wines with production under 1000 cases.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Grilled lamb chops with rosemary, garlic and olive oil", "complement", "classic", "main", "The quintessential Paso Rhône pairing — lamb's sweetness and rosemary mirror the wine's floral-spice complexity.")
    PAIR(prod, "Osso buco with gremolata and saffron risotto", "complement", "established", "main", "Opulent GSM handles braised veal shank's richness; gremolata's lemon-herb note echoes the wine's freshness.")
    PAIR(prod, "Pan-roasted duck breast with boysenberry jus", "complement", "classic", "main", "Boysenberry in the wine mirrors the reduction; duck's richness complements the GSM's warm-climate concentration.")
    PAIR(prod, "Aged sheep's milk cheese with dark honey", "complement", "established", "cheese", "The wine's lavender and dark fruit bridge to aged sheep cheese; honey ties both together.")

# === STA. RITA HILLS AVA ===
print("=== Sta. Rita Hills AVA ===")
r2 = R("Sta. Rita Hills AVA", "USA", "wine",
       designation_type="AVA",
       designation_name="Sta. Rita Hills American Viticultural Area",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="Sta. Rita Hills, west of Santa Barbara in the transverse mountain range, is California's most distinctive cool-climate Pinot Noir and Chardonnay region. The east-west orientation of the Santa Ynez Valley channels the Pacific's cold marine air directly inland, creating a natural wind tunnel that cools vineyards dramatically. Diatomaceous earth and sandy loam soils over calcareous subsoil give Sta. Rita Hills wines their extraordinary mineral precision and saline character. Sanford & Benedict, Sea Smoke, and Brewer-Clifton have defined the region's wine style.",
       key_producers="Sea Smoke Cellars, Brewer-Clifton, Loring Wine Company, Sta. Rita Hills, Hitching Post",
       historical_context="Sta. Rita Hills received AVA status in 2001 (spelled without the 'a' in 'Santa' to avoid confusion with Chile's Santa Rita). Richard Sanford pioneered the area in 1971 with the Sanford & Benedict vineyard, demonstrating that cool Pacific marine air could produce world-class Pinot Noir and Chardonnay in southern California.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Landmark Sta. Rita Hills vintage — Pinot Noir of exceptional mineral precision and cool-climate character."),
    (2020,"challenging","stable","Marine air moderated some smoke effects; Pacific-exposed sites produced excellent wines."),
    (2021,"very_good","stable","Fine conditions; consistent cool-climate elegance across the AVA."),
    (2022,"excellent","rising","Outstanding vintage; Pinot Noir and Chardonnay of benchmark saline mineral quality."),
    (2023,"excellent","rising","Exceptional year for Sta. Rita Hills — some of the finest cool-climate wine in California's recent history."),
]:
    VIN(r2, yr, qd, pt, sn)

p2 = P("Sea Smoke Cellars Santa Barbara", "winery", r2, "USA",
       production_philosophy="terroir_expression",
       philosophy_description="Sea Smoke produces estate Pinot Noir and Chardonnay from the Sta. Rita Hills' most fog-influenced sites, creating wines of extraordinary saline minerality and cool-climate precision. Their Ten, Southing, and Botella wines are California's most distinctive marine-influenced Pinot Noir.",
       reputation_narrative="Sea Smoke has defined the Sta. Rita Hills' identity as California's most Pacific-influenced Pinot Noir region — the saline, diatomaceous mineral character of their wines is unique in California and has drawn comparisons to Burgundy's finest coastal terroirs.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Sea Smoke Ten Pinot Noir Sta. Rita Hills", "wine_still", p2, r2, "USA",
                    subcategory="red", description="The estate's flagship Pinot Noir — 'Ten' because it's from the 10 best barrels of the vintage. Intensely saline and mineral, with dark cherry, smoked herbs, dried flowers, and a long, briny mineral finish from the Pacific's influence. Among California's most distinctive Pinot Noir.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Pan-roasted duck breast with cherry jus and Pacific sea salt", "complement", "classic", "main", "The wine's saline mineral notes echo Pacific sea salt on the duck; cherry jus mirrors the Pinot's dark fruit character.")
    PAIR(prod, "Grilled Pacific halibut with brown butter and capers", "complement", "established", "main", "Marine-influenced Pinot Noir and Pacific fish — the briny mineral character creates a natural coastal pairing.")
    PAIR(prod, "Roasted beets with burrata and pistachio", "complement", "established", "starter", "The wine's earthy mineral notes bridge to roasted beets; burrata's richness is cut by Pinot's salinity.")
    PAIR(prod, "Santa Barbara Channel spiny lobster with drawn butter", "complement", "classic", "main", "Local Santa Barbara lobster with local Sta. Rita Hills Pinot — the wine's marine character echoes the lobster's ocean sweetness.")
prod, is_new = PROD("Brewer-Clifton Chardonnay Sta. Rita Hills", "wine_still", p2, r2, "USA",
                    subcategory="white", description="Estate Sta. Rita Hills Chardonnay from diatomaceous earth soils — intensely mineral, saline, and restrained. Lemon zest, grapefruit, oyster shell, and a long, briny mineral finish. California's most mineral and austere Chardonnay style, requiring 3–5 years of cellaring.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Pacific oysters on the half shell with lemon", "complement", "classic", "amuse", "Oyster shell mineral Chardonnay and Pacific oysters share the same saline coastal DNA — one of California's great food-wine matches.")
    PAIR(prod, "Dungeness crab with drawn butter and sourdough", "complement", "classic", "main", "Saline, mineral Chardonnay and Pacific crab — the regional benchmark pairing of Sta. Rita Hills.")
    PAIR(prod, "Santa Barbara spot prawns with sea salt and lemon butter", "complement", "classic", "starter", "Local Santa Barbara prawns with local mineral Chardonnay — a perfect expression of California's coastal terroir.")
    PAIR(prod, "Whole-roasted turbot with herb butter and capers", "complement", "established", "main", "Austere mineral Chardonnay's precision matches turbot's delicacy; capers echo the wine's briny character.")

# === YAMANASHI WINE REGION ===
print("=== Yamanashi Wine Region ===")
r3 = R("Yamanashi Wine Region", "Japan", "wine",
       designation_type="region",
       designation_name="Yamanashi Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Yamanashi Prefecture, in the Kofu Basin surrounded by the Japanese Alps including Mount Fuji, is Japan's most important wine region, producing over 30% of Japan's domestic wine. The indigenous Koshu grape — a pink-skinned vinifera variety brought to Japan from Central Asia over 1,000 years ago — produces uniquely delicate, dry whites with citrus, white peach, and mineral character. The region also grows Muscat Bailey A for Japanese red wines. Yamanashi wines have achieved EU GI status and are gaining international recognition for their distinctive light, food-friendly style.",
       key_producers="Grace Winery, Suntory Tomi no Oka, Château Mercian, Lumiere, Marquis Wines",
       historical_context="Yamanashi's grape cultivation dates to the 8th century. The Koshu grape was believed to have been cultivated near Katsunuma since 718 AD — making it among the world's longest-continuously-cultivated wine grape areas. Western-style wine production began in 1874 when Yamanashi sent two students to France to learn winemaking.")
for yr, qd, pt, sn in [
    (2019,"excellent","rising","Landmark Yamanashi vintage — Koshu wines of exceptional delicacy and mineral precision."),
    (2020,"very_good","stable","Good vintage; Koshu showing classic light character with excellent freshness."),
    (2021,"excellent","rising","Outstanding conditions; both Koshu and Muscat Bailey A achieving high critical scores."),
    (2022,"very_good","stable","Fine vintage; Koshu wines of elegant aromatic intensity and refreshing acidity."),
    (2023,"excellent","rising","Exceptional year for Yamanashi — Koshu wines receiving international award recognition."),
]:
    VIN(r3, yr, qd, pt, sn)

p3 = P("Grace Winery Yamanashi", "winery", r3, "Japan",
       production_philosophy="terroir_expression",
       philosophy_description="Grace Winery (Chuo Budoshu) has been the leading advocate for quality Koshu wine since the 1990s, working to demonstrate that Yamanashi's indigenous grape can produce world-class wine. Winemaker Manabu Miyaji spent time in Burgundy and Bordeaux, returning to apply European precision to Japan's unique indigenous variety.",
       reputation_narrative="Grace Winery is Japan's most internationally acclaimed winery — their Koshu wines, particularly the Kayagatake and Private Reserve labels, have received international praise and helped establish Japan as a serious fine wine producing nation at London's Wine Fair.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Grace Winery Koshu Kayagatake Yamanashi", "wine_still", p3, r3, "Japan",
                    subcategory="white", description="Japan's most acclaimed Koshu from the Kayagatake single vineyard on Yamanashi's best granitic soils. Delicate and precise — white peach, lemon, grapefruit, yuzu zest, and a mineral saline finish. Perfectly calibrated for Japanese cuisine.", price_tier="premium")
if is_new:
    PAIR(prod, "Sashimi omakase — tuna, yellowtail, sea bream", "complement", "classic", "main", "Koshu's delicacy is calibrated for raw fish — the wine's citrus and mineral character echo the seafood without overwhelming its subtlety.")
    PAIR(prod, "Grilled ayu (sweetfish) with salt from Ise", "complement", "classic", "main", "Japan's most revered seasonal fish with Japan's finest indigenous wine — Koshu's mineral precision mirrors ayu's delicate sweetness.")
    PAIR(prod, "Tofu dengaku with white miso and sesame", "complement", "established", "starter", "Koshu's light body and mineral freshness complement tofu's delicacy; miso's umami bridges the wine's mineral dimension.")
    PAIR(prod, "Tempura of seasonal vegetables and prawn with dipping broth", "complement", "classic", "main", "The definitive Koshu pairing — delicate tempura needs a wine of equal delicacy; the wine's acidity cuts through the light frying.")
prod, is_new = PROD("Château Mercian Koshu Kiiroka Yamanashi", "wine_still", p3, r3, "Japan",
                    subcategory="white", description="Suntory's flagship Yamanashi Koshu — amber-tinged from brief skin contact, showing more texture and depth than conventional Koshu. Yuzu, white peach, bitter almond, and a slightly phenolic grip that increases food versatility. One of Japan's most distinctive wines.", price_tier="premium")
if is_new:
    PAIR(prod, "Yakitori chicken liver with ponzu and shichimi", "complement", "adventurous", "starter", "The wine's slight phenolic texture handles yakitori's char; ponzu's citrus echoes Koshu's yuzu character.")
    PAIR(prod, "Grilled turbot with yuzu butter and mitsuba", "complement", "classic", "main", "Yuzu notes in the wine mirror the butter sauce; mineral freshness echoes the fish's delicate marine character.")
    PAIR(prod, "Shabu-shabu with ponzu and sesame dipping sauces", "complement", "established", "main", "Skin-contact Koshu's slight texture handles thin-sliced beef; ponzu bridges the wine's citrus dimension.")
    PAIR(prod, "Chilled silken tofu with ginger, soy and sesame oil", "complement", "established", "starter", "Koshu's mineral delicacy matches silken tofu's pure subtlety — both are exercises in restraint and precision.")

# === NINGXIA WINE REGION ===
print("=== Ningxia Wine Region ===")
r4 = R("Ningxia Wine Region", "China", "wine",
       designation_type="region",
       designation_name="Ningxia Hui Autonomous Region Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Ningxia Hui Autonomous Region on the eastern slopes of the Helan Mountain in northwestern China is China's most prestigious wine region, producing increasingly acclaimed Cabernet Sauvignon, Merlot, and Cabernet Franc. At 1,100m altitude on gravelly, calcareous, and loess soils, with 3,000 hours of sunshine annually and dramatic diurnal temperature variation, Ningxia produces wines that have won awards at international competitions against established European producers. Château Changyu Moser and Pernod Ricard's Helan Mountain are key international joint ventures.",
       key_producers="Château Changyu Moser XV, Helan Qingxue (Silver Heights), Pernod Ricard Helan Mountain, COFCO Greatwall",
       historical_context="Ningxia's wine industry began in earnest in the 1980s with state investment, but it was the first decade of the 2000s when international attention arrived. Emma Gao Yuan's Silver Heights wines won international competitions, and Ningxia wines appearing in major London restaurants validated China as a serious wine producer. In 2023, Ningxia became China's first GI to receive EU recognition.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Ningxia vintage — Cabernet Sauvignon of unexpected elegance and mineral depth."),
    (2019,"very_good","stable","Good conditions; wines showing consistent quality improvement across the region."),
    (2020,"excellent","rising","Outstanding year; wines from leading estates achieving international competition success."),
    (2021,"very_good","stable","Fine vintage; warm conditions produced ripe, structured wines for ageing."),
    (2022,"excellent","rising","Exceptional conditions; Helan Mountain wines receiving critical international attention."),
    (2023,"very_good","stable","Good vintage; consistent quality from the region's established producers."),
]:
    VIN(r4, yr, qd, pt, sn)

p4 = P("Silver Heights Winery Ningxia", "winery", r4, "China",
       production_philosophy="minimal_intervention",
       philosophy_description="Emma Gao Yuan founded Silver Heights after studying at Château Calon Ségur and returning to her family vineyard in Ningxia. Her Summit and Family Reserve wines were among the first Chinese wines to win international blind tasting competitions, helping to establish China's credibility as a wine-producing nation.",
       reputation_narrative="Silver Heights is China's most internationally acclaimed artisan winery — Emma Gao's success in international competitions has made her the face of Chinese fine wine globally, and her wines have appeared in renowned international restaurants and wine lists.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Silver Heights Summit Cabernet Sauvignon Ningxia", "wine_still", p4, r4, "China",
                    subcategory="red", description="China's most acclaimed Cabernet Sauvignon from the Helan Mountain's eastern slopes. Elegant by Ningxia standards — dark cherry, cassis, graphite, cedar, and a mineral backbone from the calcareous gravel soils. International award-winning — proof that China can make world-class Cabernet.", price_tier="premium")
if is_new:
    PAIR(prod, "Peking duck with hoisin sauce and spring onion pancakes", "complement", "adventurous", "main", "An unexpected Chinese wine-food pairing — Ningxia Cabernet's cassis and cedar complement roasted duck; hoisin's sweetness bridges.")
    PAIR(prod, "Braised beef short rib with Sichuan peppercorn and soy", "complement", "established", "main", "Dark fruit Cabernet handles braised beef's richness; Sichuan peppercorn's numbing heat creates an adventurous bridge.")
    PAIR(prod, "Grilled lamb skewers with cumin and chilli (Xinjiang style)", "complement", "classic", "main", "Northwestern Chinese lamb preparation with northwestern Chinese wine — cumin and chilli echo the wine's spice dimension.")
    PAIR(prod, "Aged Comté or Cheddar with dried fruits", "complement", "established", "cheese", "Ningxia Cabernet's cassis and cedar work in Western cheese context; dried fruits bridge the wine's dark fruit character.")
prod, is_new = PROD("Changyu Moser XV Cabernet Sauvignon Ningxia", "wine_still", p4, r4, "China",
                    subcategory="red", description="The flagship collaboration between China's largest winery and Lenz Moser of Austria. Concentrated Ningxia Cabernet with international polish — dark plum, blackcurrant, vanilla, tobacco, and firm tannins. One of China's most internationally distributed premium wines.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Slow-braised pork belly (red-cooked) with rice", "complement", "established", "main", "Dark fruit and sweet oak in the Cabernet mirror red-braised pork's sweetness; the wine's tannins cut through the fat.")
    PAIR(prod, "Grilled beef hot pot with dipping sauces", "complement", "established", "main", "Cabernet's tannins and dark fruit complement beef hot pot's richness; varied dipping sauces create pairing diversity.")
    PAIR(prod, "Seared duck breast with five-spice and orange", "complement", "classic", "main", "Five-spice's complexity echoes the wine's spiced oak notes; orange bridges Cabernet's dark fruit character.")
    PAIR(prod, "Lamb rack with cumin-chilli crust and roasted garlic", "complement", "classic", "main", "Ningxia's regional lamb culture meets its wine — cumin mirrors the wine's warm-climate spice character.")

# === DALMATIA WINE REGION ===
print("=== Dalmatia Wine Region ===")
r5 = R("Dalmatia Wine Region", "Croatia", "wine",
       designation_type="region",
       designation_name="Dalmatia Wine Region",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Croatia's Dalmatian Coast — stretching from Split south to Dubrovnik and the islands of Hvar, Brač, and Korčula — produces some of the Mediterranean's most distinctive wines from indigenous varieties. Plavac Mali is the dominant red, grown on steep Dalmatian limestone terraces descending to the Adriatic. On the island of Hvar, old-vine Plavac Mali (related to Zinfandel and Primitivo) reaches extraordinary concentration. Postup from the Pelješac Peninsula is considered Croatia's finest Plavac Mali. Pošip (white) from Korčula is equally celebrated for its rich, full-bodied Mediterranean style.",
       key_producers="Saints Hills Winery, Mike's Winery, Korta Katarina, Radovčić Wines, Stina Winery",
       historical_context="Dalmatian wine history spans 2,500 years — Greek settlers planted vines on Hvar and Korčula in the 4th century BC. The connection between Zinfandel/Primitivo and Plavac Mali was proven by DNA analysis in 2001, establishing Croatian viticulture's importance in the history of global wine grape genetics.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","Landmark Dalmatia vintage — old-vine Plavac Mali of extraordinary concentration and structure."),
    (2019,"very_good","stable","Good vintage; island vineyards producing wines of typical Mediterranean intensity."),
    (2020,"excellent","rising","Outstanding year; Pelješac Postup wines of benchmark quality."),
    (2021,"very_good","stable","Fine conditions; Pošip whites particularly successful for aromatic richness."),
    (2022,"excellent","rising","Exceptional vintage for both Plavac Mali reds and Pošip whites across Dalmatia."),
    (2023,"very_good","stable","Good vintage; consistent quality from established Hvar and Korčula producers."),
]:
    VIN(r5, yr, qd, pt, sn)

p5 = P("Saints Hills Winery Dalmatia", "winery", r5, "Croatia",
       production_philosophy="terroir_expression",
       philosophy_description="Saints Hills, founded by Nenad Ferić and advised by Michel Rolland, produces premium Plavac Mali from old-vine Hvar vineyards and Dingač (the legendary steep limestone Pelješac site) alongside the white Pošip variety from Korčula. The collaboration with Rolland has elevated Croatian wine's international profile significantly.",
       reputation_narrative="Saints Hills is Croatia's most internationally recognised premium wine producer — with Michel Rolland's consultation and investment in quality viticulture on Croatia's most dramatic coastal terraces, they have produced Plavac Mali of world-class concentration and elegance.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Saints Hills Dingač Plavac Mali Pelješac", "wine_still", p5, r5, "Croatia",
                    subcategory="red", description="Dingač is Croatia's most celebrated wine — from the vertiginous, south-facing limestone cliffs of the Pelješac Peninsula, direct sun exposure produces intensely concentrated Plavac Mali. Deep ruby, powerful: dark cherry, dried fig, leather, garrigue, and high alcohol with firm tannins for cellaring.", price_tier="premium")
if is_new:
    PAIR(prod, "Braised lamb with Dalmatian herbs and white wine", "complement", "classic", "main", "The quintessential Dalmatian pairing — local lamb slow-braised with peka (under the bell) and the region's finest Plavac Mali.")
    PAIR(prod, "Grilled octopus with olive oil and Dalmatian capers", "complement", "classic", "main", "The Adriatic classic — Plavac Mali's concentration matches octopus's chewy richness; capers echo the wine's brightness.")
    PAIR(prod, "Pašticada (slow-cooked beef with prunes and vegetables)", "complement", "classic", "main", "Croatia's most famous beef preparation — the wine's dried fruit echoes the prunes; slow-cooking richness needs Plavac's structure.")
    PAIR(prod, "Aged Paški sir (Pag sheep's cheese) with Dalmatian olive oil", "complement", "classic", "cheese", "Croatia's most famous cheese with Croatia's finest wine — Pag Island sheep cheese's saltiness bridges Plavac's dark fruit.")
prod, is_new = PROD("Stina Pošip Brač Island Dalmatia", "wine_still", p5, r5, "Croatia",
                    subcategory="white", description="Pošip from Korčula Island's indigenous white grape — rich, full-bodied Mediterranean white with peach, almond, dried herbs, and a distinctive limestone-mineral backbone from the Dalmatian karst. One of the Adriatic's most food-compatible white wines.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled Adriatic sea bass with lemon and Croatian olive oil", "complement", "classic", "main", "Dalmatia's definitive fish and wine pairing — Pošip's richness and mineral depth match sea bass perfectly.")
    PAIR(prod, "Brudet (Dalmatian fish stew with polenta)", "complement", "classic", "main", "Croatia's beloved fish stew served with polenta — Pošip's body and herbs bridge to the stew's complexity.")
    PAIR(prod, "Shrimp buzara (Adriatic prawns in white wine and herbs)", "complement", "classic", "main", "Adriatic prawns with Adriatic white wine — the wine used in the dish creates perfect harmony with wine alongside.")
    PAIR(prod, "Grilled sardines with sea salt and lemon", "complement", "classic", "starter", "Dalmatian sardines with Dalmatian white — simplicity of preparation matched by the wine's clean mineral freshness.")

# === DB STATE ===
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
print("B170 complete.")
cur.close()
conn.close()
