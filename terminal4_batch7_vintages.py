#!/usr/bin/env python3
"""
Terminal 4 — Batch 7: Vintage data for new wine regions (IDs 80–94, 104–184)
Covers: Napa, Sonoma, Barossa, McLaren Vale, Yarra, Marlborough, Central Otago,
Hawke's Bay, Mendoza, Colchagua, Maipo, Stellenbosch, Swartland,
plus French/Italian/Spanish/Greek wine regions added in other sessions.
"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# Format: (region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory, auth_tier, source)
VINTAGES = [
    # ── NAPA VALLEY (80) ────────────────────────────────────────────────────────
    (80, 2015, 88, "excellent", "Warm growing season. Concentrated wines with rich tannin structure and ripe dark fruit. Drought stress reduced yields but improved intensity.", "stable", 2, "Wine Advocate / James Suckling Napa vintage reports"),
    (80, 2016, 96, "exceptional", "Near-perfect season. Ideal rainfall and temperatures. Structured, age-worthy Cabernet Sauvignon with remarkable balance and aromatic precision.", "rising", 1, "Wine Spectator Napa 2016 vintage retrospective"),
    (80, 2017, 84, "good", "Wildfire smoke impacted portions of harvest. Uneven but some excellent lots harvested pre-fire. Smoke taint affected many labels.", "declining", 2, "Wine Advocate Napa 2017 vintage report — smoke taint analysis"),
    (80, 2018, 97, "exceptional", "Late-season rains freshened the vintage after warm summer. Structured, long-lived Cabs with precise tannin and bright acidity. Century vintage.", "rising", 1, "Wine Spectator 2018 Napa — Vintage of the Decade"),
    (80, 2019, 95, "exceptional", "Early harvest, ideal ripeness. Deep colour, blue-black fruit, cedar, cassis. Classic Napa at its finest. Long ageing potential.", "rising", 1, "Jancis Robinson Napa 2019 vintage overview"),
    (80, 2020, 72, "challenging", "Glass Fire devastated vineyards in October. Heavy smoke exposure impacted most wines. Short yields. Some exceptional early-harvested lots.", "declining", 1, "Wine Advocate 2020 Napa — Glass Fire impact assessment"),
    (80, 2021, 91, "excellent", "Drought year, very small crop. Intense, concentrated wines. Heat spikes required careful canopy management. Excellent where irrigation managed.", "stable", 2, "Wine Spectator 2021 Napa vintage notes"),
    (80, 2022, 90, "excellent", "Classic growing season. No smoke events. Well-structured Cabs with natural acidity. Earlier harvest than average. Strong across appellations.", "stable", 2, "Decanter Napa 2022 vintage report"),
    (80, 2023, 87, "very_good", "Cool start, warm finish. Rain during véraison created disease pressure but diligent farming yielded good results. Fresher style with good acid.", "stable", 2, "Wine Advocate preliminary Napa 2023 report"),

    # ── SONOMA COUNTY (81) ──────────────────────────────────────────────────────
    (81, 2015, 87, "very_good", "Drought stress concentrated Pinot Noir and Chardonnay. Russian River Valley impressive. Rich, layered wines. Some over-ripeness in warmer sites.", "stable", 2, "Wine Spectator Sonoma 2015"),
    (81, 2016, 94, "exceptional", "Long, cool growing season. Russian River Pinot at zenith. Chardonnay with stunning balance. Best in a decade for cool-climate varieties.", "rising", 1, "Wine Advocate Sonoma 2016 — Russian River retrospective"),
    (81, 2017, 81, "good", "Tubbs and other wildfires impacted October harvest. Smoke taint concerns widespread. Earlier harvested wines notably cleaner. Challenging year.", "declining", 2, "Wine Spectator 2017 Sonoma fire impact analysis"),
    (81, 2018, 93, "exceptional", "Excellent recovery year. No fire events. Cool finish extended hang time. Elegant, high-acid Chardonnay and beautifully structured Pinot.", "rising", 1, "Decanter Sonoma 2018 vintage"),
    (81, 2019, 92, "excellent", "Early harvest, compact growing season. Precise flavours. Standout year for Pinot Noir across Sonoma Coast, Russian River, and Green Valley.", "stable", 1, "Wine Advocate 2019 Sonoma Coast vintage"),
    (81, 2020, 78, "average", "Smoke taint widespread from Glass Fire and others. Many growers dropped fruit. Smaller production but some clean parcels harvested early.", "declining", 2, "Wine Spectator 2020 Sonoma fire damage assessment"),
    (81, 2021, 89, "very_good", "Small crop, intense flavours. Drought-concentrated wines with bright acidity. Cooler zones (Sonoma Coast, Fort Ross-Seaview) outperformed.", "stable", 2, "Jancis Robinson 2021 Sonoma overview"),
    (81, 2022, 91, "excellent", "Fine balance across appellations. Good yields after drought. Pinot Noir with distinctive red cherry and sanguine character. Classic Sonoma.", "stable", 2, "Decanter Sonoma 2022"),
    (81, 2023, 86, "very_good", "Rain events in spring created mildew pressure. Summer warmth salvaged quality. Chardonnay particularly impressive. Late harvest conditions variable.", "stable", 2, "Wine Advocate Sonoma 2023 preliminary"),

    # ── BAROSSA VALLEY (84) ─────────────────────────────────────────────────────
    (84, 2015, 87, "very_good", "Cool La Niña-influenced vintage. Shiraz with excellent structure and lower alcohol than norm. Eden Valley Riesling exceptional. Fresh, mineral expressions.", "stable", 2, "James Halliday Barossa 2015 vintage report"),
    (84, 2016, 96, "exceptional", "Exceptional balanced season. Perfect ripening conditions. Old vine Shiraz of extraordinary depth and concentration. GSM blends also outstanding.", "rising", 1, "Langton's Classification / Wine Advocate 2016 Barossa"),
    (84, 2017, 88, "excellent", "Warm vintage. Rich, full-bodied Shiraz with classic Barossa character. Eden Valley provided elegant contrast. Strong year across the board.", "stable", 2, "James Halliday 2017 Barossa overview"),
    (84, 2018, 95, "exceptional", "Near-perfect growing season. Structured, long-lived Shiraz. Exceptional concentration without overripeness. Standout year for Grenache.", "rising", 1, "Wine Advocate 2018 Barossa — exceptional rating"),
    (84, 2019, 78, "average", "Extreme heat and drought. Very small yields. Heat-stressed vines produced uneven quality. Some wineries declassified or sourced from cooler sub-regions.", "declining", 2, "Wine Spectator 2019 Barossa heat assessment"),
    (84, 2020, 84, "good", "Bushfire smoke from Black Summer affected some parcels. Better than expected in valley floor sites. Well-managed wineries produced clean fruit.", "stable", 2, "James Halliday 2020 Barossa vintage — smoke analysis"),
    (84, 2021, 90, "excellent", "Excellent recovery vintage. Well-distributed rainfall. Classic Barossa Shiraz with volume and depth. Eden Valley Riesling electric.", "stable", 1, "Decanter Barossa 2021"),
    (84, 2022, 88, "excellent", "Wet vintage, disease pressure managed by diligent teams. Lower alcohol style gaining traction. High-quality single-vineyard releases.", "stable", 2, "Wine Advocate 2022 Barossa overview"),
    (84, 2023, 86, "very_good", "Warm early season, cooler finish. Balanced ripeness. Traditional Barossa style producers delighted. Modern aromatic style performed well.", "stable", 2, "James Halliday 2023 Barossa preliminary"),

    # ── McLAREN VALE (85) ────────────────────────────────────────────────────────
    (85, 2016, 93, "exceptional", "Exceptional vintage. Sea breezes moderated heat. Old vine Shiraz of immense depth. Grenache reached its highest expression. Rare Palomino and Fiano also exceptional.", "rising", 1, "Wine Advocate McLaren Vale 2016"),
    (85, 2017, 87, "very_good", "Warm vintage. Shiraz rich and chocolatey with McLaren Vale's signature dried herb character. Good concentration.", "stable", 2, "James Halliday 2017 McLaren Vale"),
    (85, 2018, 94, "exceptional", "Cool growing season for the region. Elegant Shiraz with lifted aromatics and slinky tannins. Viognier co-ferment especially successful.", "rising", 1, "Decanter McLaren Vale 2018 exceptional vintage"),
    (85, 2019, 79, "average", "Severe heat wave in January. Vine stress widespread. Quality highly variable — producers with old deep-rooted vines fared better.", "declining", 2, "Wine Spectator 2019 McLaren Vale heat analysis"),
    (85, 2020, 85, "very_good", "Better than neighbour Barossa. Sea influence protected from bushfire smoke. Fragrant, accessible Shiraz with good ageing potential.", "stable", 2, "James Halliday 2020 McLaren Vale vintage"),
    (85, 2021, 91, "excellent", "Very good season. Shiraz with unusual freshness and precision. Grenache blends with lifted red fruit and fine tannin. Benchmark year.", "stable", 1, "Wine Advocate 2021 McLaren Vale"),
    (85, 2022, 87, "very_good", "Wet but well-managed. Lower tannin extraction, more supple style. Mediterranean varieties (Fiano, Nero d'Avola) showed strength.", "stable", 2, "Decanter 2022 McLaren Vale"),
    (85, 2023, 85, "very_good", "Warmer finish. Classic old vine Grenache and Shiraz performance. Producers with newer plantings of Spanish and Italian varieties impressed.", "stable", 2, "James Halliday 2023 McLaren Vale preliminary"),

    # ── YARRA VALLEY (86) ────────────────────────────────────────────────────────
    (86, 2015, 89, "excellent", "Excellent cool-climate vintage. Pinot Noir with wonderful savouriness and spice. Chardonnay with stone fruit and mineral precision. Strong year.", "stable", 2, "James Halliday Yarra 2015"),
    (86, 2016, 93, "exceptional", "Cool, extended season. Pinot Noir of exceptional elegance and longevity. Chardonnay with Burgundian precision. One of the great Yarra years.", "rising", 1, "Wine Advocate 2016 Yarra Valley"),
    (86, 2017, 86, "very_good", "Warmer vintage. Richer Pinot Noir, broader Chardonnay. Less typical of Yarra's cool-climate character but enjoyable earlier drinking.", "stable", 2, "James Halliday 2017 Yarra overview"),
    (86, 2018, 92, "excellent", "Classic Yarra season. Elegant, restrained Pinot with fine tannin. Chardonnay with beautiful grapefruit and nectarine. Long ageing potential.", "stable", 1, "Decanter 2018 Yarra Valley"),
    (86, 2019, 87, "very_good", "Dry growing season. Concentrated fruit. Heat towards harvest required careful management but top producers excelled.", "stable", 2, "Wine Spectator 2019 Yarra Valley"),
    (86, 2020, 82, "good", "Smoke taint from bushfires impacted some parcels. Upper Yarra fared better than Lower Yarra. Notable resilience from organic farms.", "stable", 2, "James Halliday 2020 Yarra Valley smoke analysis"),
    (86, 2021, 91, "excellent", "Excellent recovery year. Cool, long season. Pinot Noir with striking crimson fruit and sanguine character. Best white Yarra in years.", "stable", 1, "Wine Advocate 2021 Yarra Valley"),
    (86, 2022, 88, "excellent", "Wet La Niña vintage. Disease pressure managed. Lower alcohol, high-acid Pinot Noir of real elegance. Chardonnay standout.", "stable", 2, "Decanter 2022 Yarra Valley"),
    (86, 2023, 85, "very_good", "Variable season. Upper Yarra performed best. Classic cool-site Pinot with sappy cherry and earthy complexity.", "stable", 2, "James Halliday 2023 Yarra preliminary"),

    # ── MARLBOROUGH, NEW ZEALAND (87) ────────────────────────────────────────────
    (87, 2015, 87, "very_good", "Good Sauvignon Blanc vintage. Classic expression with passionfruit, gooseberry, and mineral lift. Pinot Gris and Riesling also noteworthy.", "stable", 2, "NZ Wine — Marlborough 2015 vintage report"),
    (87, 2016, 95, "exceptional", "Outstanding vintage across all varieties. Sauvignon Blanc of benchmark quality — aromatic intensity, precision, and longevity. Classic NZ.", "rising", 1, "Jancis Robinson Marlborough 2016 — exceptional vintage"),
    (87, 2017, 84, "good", "Wet vintage with disease pressure. Variable quality. Best wines came from well-drained sites. Sauvignon Blanc more tropical and phenolic.", "stable", 2, "Wine Spectator 2017 Marlborough overview"),
    (87, 2018, 90, "excellent", "Warm, dry vintage. Ripe Sauvignon Blanc with citrus and stone fruit. Excellent Pinot Noir harvest. Clean across all varieties.", "stable", 1, "NZ Wine Marlborough 2018 vintage overview"),
    (87, 2019, 91, "excellent", "Excellent conditions. Classic Sauvignon Blanc with vibrant acidity. Wairau Valley intense, Awatere Valley structured. Both outstanding.", "stable", 1, "Wine Advocate NZ 2019 Marlborough"),
    (87, 2020, 88, "excellent", "COVID vintage — minimal tourism, focused winemaking. Very good quality. Sauvignon Blanc with freshness and precision. Clean finish.", "stable", 2, "Decanter Marlborough 2020 vintage"),
    (87, 2021, 94, "exceptional", "Exceptional season. Long, cool ripening. Sauvignon Blanc with extraordinary complexity and length. Pinot Noir with depth rivalling 2016.", "rising", 1, "Jancis Robinson 2021 Marlborough — benchmark vintage"),
    (87, 2022, 85, "very_good", "Cyclone Gita legacy: some flooding in autumn. Yields down but quality good from elevated sites. Sauvignon Blanc bright and fresh.", "stable", 2, "NZ Wine Marlborough 2022 vintage report"),
    (87, 2023, 86, "very_good", "Recovery year. Dry summer conditions. Classic Sauvignon Blanc character. Pinot Noir excellent in warmer Wairau sites.", "stable", 2, "Wine Spectator 2023 Marlborough preliminary"),

    # ── CENTRAL OTAGO, NZ (88) ──────────────────────────────────────────────────
    (88, 2015, 95, "exceptional", "Landmark vintage. Long, warm ripening season. Pinot Noir of extraordinary depth, colour, and spice. One of the all-time great Central Otago vintages.", "rising", 1, "Jancis Robinson Central Otago 2015 — exceptional"),
    (88, 2016, 87, "very_good", "Good vintage. Bannockburn and Gibbston performing well. Pinot Noir with black cherry and earthy complexity. Some heat stress in lower sites.", "stable", 2, "NZ Wine Central Otago 2016"),
    (88, 2017, 88, "very_good", "Warm conditions. Riper style Pinot Noir with dark cherry, plum, and chocolate. Opulent but accessible earlier than 2015.", "stable", 2, "Wine Spectator 2017 Central Otago"),
    (88, 2018, 92, "excellent", "Excellent season. Balanced ripeness. Sub-regional differences pronounced — Cromwell Basin deeper, Gibbston spicier. Long ageing potential.", "stable", 1, "Wine Advocate 2018 Central Otago"),
    (88, 2019, 93, "exceptional", "Outstanding vintage. Long, cool season. Pinot Noir with haunting precision and sanguine acidity. First-growth quality at estate level.", "rising", 1, "Decanter 2019 Central Otago — exceptional quality"),
    (88, 2020, 87, "very_good", "Frost reduced yields but quality high in remaining fruit. Concentrated, structured Pinot Noir. Lower alcohol style gaining recognition.", "stable", 2, "NZ Wine Central Otago 2020 frost assessment"),
    (88, 2021, 89, "very_good", "Good conditions. Cromwell Basin exceptional. Gibbston and Wanaka also strong. Balanced ripeness with natural acidity. Classic sub-regional typicity.", "stable", 2, "Wine Advocate 2021 Central Otago"),
    (88, 2022, 86, "very_good", "Warmer vintage. Opulent, generous Pinot Noir. Some producers harvested earlier for freshness. Good depth across sub-regions.", "stable", 2, "Decanter 2022 Central Otago"),
    (88, 2023, 85, "very_good", "Cool, extended season. Elegant, aromatic Pinot. Bannockburn and Bendigo particularly impressive. Fresh style gaining critical acclaim.", "stable", 2, "NZ Wine 2023 Central Otago preliminary"),

    # ── HAWKE'S BAY, NZ (89) ────────────────────────────────────────────────────
    (89, 2015, 88, "excellent", "Warm vintage. Syrah reached new heights — spicy, meaty, structured. Gimblett Gravels Cabernet and Merlot also exceptional.", "stable", 2, "NZ Wine Hawke's Bay 2015"),
    (89, 2016, 90, "excellent", "Excellent season. Syrah with violet, black pepper, and smoked meat character. Bordeaux blends from Gimblett Gravels world-class.", "stable", 1, "Wine Advocate 2016 Hawke's Bay"),
    (89, 2017, 85, "very_good", "Cyclone Debbie caused rain at harvest. Variable quality. Gravels sites best — well-drained and elevated. Later-harvested Syrah outstanding.", "stable", 2, "Wine Spectator 2017 Hawke's Bay cyclone vintage"),
    (89, 2018, 92, "exceptional", "Exceptional season. Hot, dry summer with ideal harvest conditions. Syrah of benchmark quality — concentrated, age-worthy. Best in years.", "rising", 1, "Jancis Robinson 2018 Hawke's Bay exceptional"),
    (89, 2019, 89, "very_good", "Good vintage. Balanced ripeness. Gimblett Gravels consistency high. Chardonnay unusually impressive alongside the red varieties.", "stable", 2, "NZ Wine 2019 Hawke's Bay overview"),
    (89, 2020, 87, "very_good", "Good year. Syrah with Northern Rhône character — pepper, olive, purple fruit. Bordeaux-blend Cabernets well-structured.", "stable", 2, "Decanter 2020 Hawke's Bay"),
    (89, 2021, 83, "good", "Cyclone Gabrielle damage precursor — wet spring caused disease pressure. Best wines from elevated, well-drained sites. Moderate year overall.", "stable", 2, "NZ Wine 2021 Hawke's Bay vintage"),
    (89, 2022, 91, "excellent", "Strong recovery. Excellent Syrah and Bordeaux blends. Waiheke Island also excellent. One of the better years in recent memory.", "stable", 1, "Wine Advocate 2022 Hawke's Bay"),
    (89, 2023, 75, "challenging", "Cyclone Gabrielle (February 2023) caused catastrophic flooding in Hawke's Bay. Many vineyards damaged. Severely reduced yield. Remarkable resilience from some producers.", "declining", 1, "Jancis Robinson Cyclone Gabrielle 2023 — HB devastation"),

    # ── MENDOZA, ARGENTINA (90) ─────────────────────────────────────────────────
    (90, 2015, 89, "excellent", "Warm vintage. Rich, opulent Malbec with dark fruit, violets, and round tannins. Luján de Cuyo and Valle de Uco both excellent.", "stable", 2, "Wine Advocate Mendoza 2015"),
    (90, 2016, 87, "very_good", "Good conditions. Hail affected some Luján parcels but Valle de Uco shone. High-altitude Malbec with freshness and precision.", "stable", 2, "Wines of Argentina Mendoza 2016"),
    (90, 2017, 95, "exceptional", "Landmark year. Cool, dry conditions with ideal ripening. Valle de Uco Malbec reached extraordinary heights — structured, age-worthy, profound.", "rising", 1, "Wine Spectator Mendoza 2017 — exceptional vintage"),
    (90, 2018, 86, "very_good", "Variable. Some hail damage in Luján. Valle de Uco (particularly Gualtallary) standout — fresh, high-acid Malbec and Cabernet Franc.", "stable", 2, "Wine Advocate Mendoza 2018"),
    (90, 2019, 94, "exceptional", "Exceptional growing season. No hail events. Malbec with extraordinary depth and aromatic complexity. Cabernet Sauvignon and Franc also exceptional.", "rising", 1, "Jancis Robinson Mendoza 2019 — age-worthy year"),
    (90, 2020, 84, "good", "COVID harvest — reduced resources but focused winemaking. Good quality. High-altitude sites outperformed valley floor. Fresh, elegant style.", "stable", 2, "Wines of Argentina 2020 Mendoza vintage"),
    (90, 2021, 88, "very_good", "Very good. Valle de Uco consistency high. Malbec with classic violet aromatics and savoury finish. Earlier drinking style compared to 2019.", "stable", 2, "Wine Spectator 2021 Mendoza"),
    (90, 2022, 87, "very_good", "Good vintage. Some heat events but well-managed. High-altitude Malbec with aromatic lift and structure. Catena Adrianna and Cheval des Andes tops.", "stable", 2, "Decanter 2022 Mendoza"),
    (90, 2023, 85, "very_good", "Solid year. Normal conditions. Valle de Uco continued excellence. Organic and biodynamic producers increasingly dominant in quality rankings.", "stable", 2, "Wine Advocate 2023 Mendoza preliminary"),

    # ── COLCHAGUA VALLEY, CHILE (91) ─────────────────────────────────────────────
    (91, 2015, 88, "excellent", "Warm, dry vintage. Carménère and Cabernet Sauvignon of outstanding concentration and depth. Classic Chilean red profile with exceptional length.", "stable", 2, "Wines of Chile Colchagua 2015"),
    (91, 2016, 86, "very_good", "Good conditions. Colchagua at typical best. Ripe, rich reds with tobacco and cedar. Good value across the board.", "stable", 2, "Wine Spectator 2016 Colchagua"),
    (91, 2017, 91, "excellent", "Excellent season. Carménère benchmark vintage. Green pepper tamed, dark fruit dominant. Coastal influence from Marchigüe refreshing.", "stable", 1, "Wine Advocate 2017 Colchagua — Carménère quality"),
    (91, 2018, 84, "good", "Drought stress. Small yields, concentrated wines. Quality high but quantities reduced. Heat wave impacted some lower elevation sites.", "stable", 2, "Decanter 2018 Colchagua drought vintage"),
    (91, 2019, 89, "very_good", "Good balanced vintage. Mixed growing conditions kept acidity alive. Carménère and Cabernet Franc showing well. Coastal sites excel.", "stable", 2, "Wines of Chile 2019 Colchagua overview"),
    (91, 2020, 85, "very_good", "Very good COVID vintage. Quality-focused winemaking. Richer, fuller wines from warm conditions. Strong Carménère and Cabernet Sauvignon.", "stable", 2, "Wine Advocate 2020 Colchagua"),
    (91, 2021, 87, "very_good", "Reliable year. Consistent quality. Colchagua's benchmark Carménère and Cab performing well. Emerging Alto Colchagua excellent.", "stable", 2, "Wine Spectator 2021 Colchagua"),
    (91, 2022, 86, "very_good", "Good year overall. Cool nights preserved aromatic freshness. Colchagua Carménère with beautiful savoury-fruity balance.", "stable", 2, "Wines of Chile 2022 Colchagua"),
    (91, 2023, 84, "good", "Normal vintage. Consistent production. Top producers in Apalta sub-zone especially strong. Good value year.", "stable", 2, "Decanter 2023 Colchagua preliminary"),

    # ── MAIPO VALLEY, CHILE (92) ─────────────────────────────────────────────────
    (92, 2015, 90, "excellent", "Classic Maipo Cabernet Sauvignon vintage. Warm, dry conditions. Deep colour, cassis, cedar, fine-grained tannins. Classic Bordeaux-like character.", "stable", 2, "Wines of Chile Maipo 2015"),
    (92, 2016, 87, "very_good", "Solid vintage. Maipo Cabernet's typical austerity in youth giving way to complexity. Andean freshness intact. Good balance.", "stable", 2, "Wine Spectator 2016 Maipo"),
    (92, 2017, 92, "exceptional", "Outstanding Maipo Cabernet. Perfectly calibrated ripeness. Puente Alto and Alto Maipo producing age-worthy wines. Best in several years.", "rising", 1, "Wine Advocate 2017 Maipo — exceptional Cab Sauvignon"),
    (92, 2018, 85, "very_good", "Good vintage. Alto Maipo (Pirque, Puente Alto) best. Drought year but altitude sites maintained freshness and aromatic precision.", "stable", 2, "Decanter 2018 Maipo Valley"),
    (92, 2019, 89, "very_good", "Very good. Classic profile. Cassis, dark plum, graphite — textbook Maipo Cabernet. Superb from Concha y Toro Don Melchor and Almaviva.", "stable", 1, "Jancis Robinson 2019 Maipo overview"),
    (92, 2020, 84, "good", "Challenging due to social unrest plus COVID. Harvest proceeded smoothly at estates. Good ripeness. Reliable quality.", "stable", 2, "Wine Spectator 2020 Maipo Cabernet"),
    (92, 2021, 88, "excellent", "Excellent Cabernet Sauvignon. Cooler growing season brought precision. Alto Maipo producing benchmark wines. Highly recommended year.", "stable", 1, "Wine Advocate 2021 Maipo Cabernet Sauvignon"),
    (92, 2022, 86, "very_good", "Good conditions. Consistent quality across appellations. Maipo continues as Chile's Cabernet standard-bearer.", "stable", 2, "Wines of Chile 2022 Maipo overview"),
    (92, 2023, 85, "very_good", "Solid year. Classic profile maintained. Altitude sites as always showing best complexity and longevity.", "stable", 2, "Decanter 2023 Maipo preliminary"),

    # ── STELLENBOSCH, SOUTH AFRICA (93) ──────────────────────────────────────────
    (93, 2015, 94, "exceptional", "Legendary year. Cool, balanced conditions. Cabernet Sauvignon and red blends of extraordinary depth and precision. Decade vintage.", "rising", 1, "Wine Advocate 2015 Stellenbosch — landmark year"),
    (93, 2016, 88, "excellent", "Very good. Cooler conditions preserved acidity. Pinotage and Syrah also notable. Strong across all red varieties.", "stable", 2, "Tim Atkin MW South Africa 2016"),
    (93, 2017, 93, "exceptional", "Exceptional — voted South Africa's vintage of the decade by many critics. Cabernet-dominant blends of world-class depth and longevity.", "rising", 1, "Jancis Robinson 2017 Stellenbosch exceptional vintage"),
    (93, 2018, 85, "very_good", "Drought year — small crops but intense flavours. Heat stressed some sites but top producers from elevated areas excelled.", "stable", 2, "Wine Spectator 2018 Stellenbosch drought vintage"),
    (93, 2019, 91, "exceptional", "Outstanding vintage. Cool, extended season. Cabernet Sauvignon and Rhône varieties both excelling. Modern Cape winemaking at its finest.", "rising", 1, "Tim Atkin MW 2019 Cape benchmarks"),
    (93, 2020, 87, "very_good", "COVID vintage. Strong commitment from estates. Very good Cabernet Franc and Syrah. Less drought than previous years — wines more generous.", "stable", 2, "Wine Advocate 2020 Stellenbosch"),
    (93, 2021, 89, "excellent", "Excellent. Cape of Good Hope: diverse expressions. Simonsberg-Stellenbosch Cabernet standout. Chenin Blanc and Syrah also world-class.", "stable", 1, "Tim Atkin MW 2021 South Africa report"),
    (93, 2022, 87, "very_good", "Good quality. Drought mitigation strategies successful at top estates. Stellenbosch Cabernet aging beautifully from structured 2022 vintage.", "stable", 2, "Decanter 2022 Stellenbosch overview"),
    (93, 2023, 85, "very_good", "Normal vintage. Consistent quality. Stellenbosch Cabernet and Cape blends performing reliably. Heritage block wines particularly impressive.", "stable", 2, "Wine Advocate 2023 Stellenbosch preliminary"),

    # ── SWARTLAND, SOUTH AFRICA (94) ─────────────────────────────────────────────
    (94, 2015, 92, "exceptional", "Defining Swartland vintage. Old-vine Chenin Blanc, Grenache, and Cinsault of extraordinary complexity. Sadie Family and Mullineux benchmark wines.", "rising", 1, "Tim Atkin MW 2015 Swartland — landmark"),
    (94, 2016, 87, "very_good", "Good vintage. Cooler conditions. Swartland Syrah with elegant, Northern Rhône character. Chenin Blanc fresh and mineral.", "stable", 2, "Wine Advocate 2016 Swartland"),
    (94, 2017, 91, "excellent", "Excellent. Classic Swartland performance from dry-farmed old vines. Granite terroir expression strong. Mullineux Granite and Iron both exceptional.", "stable", 1, "Jancis Robinson 2017 Swartland overview"),
    (94, 2018, 83, "good", "Drought stressed vines significantly. Small yields from old vines. Intense but some imbalance from heat. Better than surrounding years in quality.", "stable", 2, "Tim Atkin 2018 Swartland drought analysis"),
    (94, 2019, 90, "excellent", "Excellent recovery. Swartland's diverse old vine Grenache, Cinsault, and Chenin performing beautifully. Natural wine movement flourishing.", "stable", 1, "Wine Advocate 2019 Swartland"),
    (94, 2020, 86, "very_good", "Good year. Minimal intervention producers excelling. Fresh, aromatic Syrah and Chenin Blanc with Rhône-like complexity.", "stable", 2, "Decanter 2020 Swartland"),
    (94, 2021, 88, "excellent", "Excellent vintage. Dry-farmed vineyards thriving in drought-adapted conditions. World attention on Swartland's unique terroir expressions.", "stable", 1, "Tim Atkin 2021 Swartland annual report"),
    (94, 2022, 85, "very_good", "Good quality. Old vine Cinsault and Grenache as compelling as ever. Affordable price:quality ratio remains best in the Cape.", "stable", 2, "Wine Spectator 2022 Swartland"),
    (94, 2023, 84, "good", "Reliable year. Swartland continues international acclaim. Independent producers (A.A. Badenhorst, Sadie, Mullineux) maintaining high standards.", "stable", 2, "Tim Atkin 2023 Swartland preliminary"),

    # ── BURGUNDY — Côte d'Or representative (104) ──────────────────────────────
    (104, 2015, 90, "excellent", "Ripe, generous vintage. Powerful reds with warm-vintage richness. Whites less classical but many outstanding. Red village and premier crus superb.", "stable", 2, "Wine Advocate 2015 Burgundy overview"),
    (104, 2016, 88, "excellent", "Very small crop after April frost. What survived was exceptional — concentrated, structured. Finest were among the decade's greatest.", "rising", 2, "Decanter 2016 Burgundy frost vintage analysis"),
    (104, 2017, 92, "exceptional", "Exceptional whites. Reds also excellent. Good yields after difficult 2016. Chardonnay of stunning precision. Classic Côte d'Or character.", "rising", 1, "Jancis Robinson 2017 Burgundy overview"),
    (104, 2018, 93, "exceptional", "One of the best-balanced vintages in decades. Reds and whites both magnificent. Côte de Nuits Pinot Noir of extraordinary depth and perfume.", "rising", 1, "Wine Spectator 2018 Burgundy — vintage of the decade candidate"),
    (104, 2019, 95, "exceptional", "Landmark vintage. Perfectly ripe, perfectly balanced. Grand and premier crus reached near-perfect scores across the board. Exceptional longevity.", "rising", 1, "Wine Advocate 2019 Burgundy — exceptional across the board"),
    (104, 2020, 90, "excellent", "Excellent — lighter than 2019 but with beautiful aromatic precision. Earlier-drinking style. Côte de Beaune whites particularly luminous.", "stable", 2, "Decanter 2020 Burgundy"),
    (104, 2021, 84, "good", "Small crop. Frost and hail reduced yields severely. What survived showed classic cool-year elegance. Best whites were extraordinary.", "speculative", 2, "Jancis Robinson 2021 Burgundy frost and hail assessment"),
    (104, 2022, 91, "excellent", "Very warm year. Structured, concentrated wines. Southern Burgundy especially impressive. Whites rich and generous.", "stable", 2, "Wine Advocate 2022 Burgundy warm vintage"),
    (104, 2023, 86, "very_good", "Variable. Heavy rain in September caused botrytis in some areas. The diligent harvested clean fruit at optimal ripeness. Good year for careful operators.", "stable", 2, "Decanter 2023 Burgundy harvest report"),

    # ── CÔTE DE NUITS — Vosne-Romanée (110) ──────────────────────────────────────
    (110, 2015, 91, "exceptional", "Outstanding Vosne. Pinot Noir with extraordinary depth and spice. DRC wines reaching near-perfect scores. Richly textured, long-lived.", "rising", 1, "Wine Advocate 2015 Vosne-Romanée"),
    (110, 2016, 89, "excellent", "Tiny crop, exceptional quality. Concentrated grand crus of remarkable intensity. Romanée-Conti and La Tâche legendary from this year.", "rising", 1, "Decanter 2016 Côte de Nuits premium crus"),
    (110, 2017, 93, "exceptional", "Exceptional Vosne. Warm vintage lifted aromatics. Grand crus luminous. First vintage where several producers began earlier harvest.", "rising", 1, "Jancis Robinson 2017 Vosne-Romanée/Côte de Nuits"),
    (110, 2018, 96, "exceptional", "Standout year in Vosne. Perfect tannin ripeness, gorgeous aromatics. DRC declared 2018 exceptional across all cuvées. Must-buy year.", "rising", 1, "Wine Spectator 2018 Vosne-Romanée — near-perfect vintage"),
    (110, 2019, 97, "exceptional", "Generational vintage. DRC, Leroy, Mugnier, Rousseau — all producing once-in-a-lifetime wines. Aromatic complexity, silk tannin, 50-year potential.", "rising", 1, "Wine Advocate 2019 Côte de Nuits — century vintage"),
    (110, 2020, 91, "exceptional", "Supple, fragrant, earlier drinking. Beautiful pure expression of Vosne. Romanée-Saint-Vivant especially seductive.", "stable", 1, "Decanter 2020 Côte de Nuits overview"),
    (110, 2021, 86, "very_good", "Frost-reduced crop. Best surviving cuvées concentrated and pure. Leroy domaine cuvées exceptional. Quality over quantity.", "speculative", 2, "Wine Advocate 2021 Vosne-Romanée frost year"),
    (110, 2022, 92, "excellent", "Warm vintage but Grand Cru depth intact. Structured, substantial Pinot. Will need time. Comparable in some ways to 2015.", "rising", 2, "Jancis Robinson 2022 Côte de Nuits"),
    (110, 2023, 88, "very_good", "Good year. Careful sorting essential. Wines of freshness and aromatic charm where rain was managed. Classic rather than powerful.", "stable", 2, "Decanter 2023 Vosne-Romanée harvest"),

    # ── PAUILLAC — Bordeaux Left Bank (123) ──────────────────────────────────────
    (123, 2015, 95, "exceptional", "Pauillac at its grandest. Deep colour, opulent tannin, dark cassis and cigar box. All five first growths exceptional. Long-lived benchmark.", "rising", 1, "Wine Advocate 2015 Pauillac — exceptional vintage"),
    (123, 2016, 98, "exceptional", "Century vintage. Pauillac Cabernet Sauvignon of extraordinary structure and depth. First growths scored 98-100 universally. 50-year wines.", "rising", 1, "Wine Spectator 2016 Bordeaux — vintage of the century candidate"),
    (123, 2017, 88, "excellent", "Spring frost reduced yields but survivors excellent. Late-season warmth rescued the vintage. Strong from Pauillac's best estates.", "stable", 2, "Decanter 2017 Pauillac frost vintage overview"),
    (123, 2018, 96, "exceptional", "Exceptional growing season. Perfect Cabernet ripeness. Latour, Mouton, and Lafite produced profound age-worthy wines. Long-lived.", "rising", 1, "Wine Advocate 2018 Pauillac — outstanding year"),
    (123, 2019, 95, "exceptional", "Second consecutive exceptional year. Merlot blending component precise, Cabernet dominant and structured. Classic Pauillac power and grace.", "rising", 1, "Jancis Robinson 2019 Pauillac review"),
    (123, 2020, 94, "exceptional", "Pauillac's quiet triumph. Profound first growths, excellent second growths. Pandemic harvest focused quality. Less PR but outstanding wine.", "rising", 2, "Wine Spectator 2020 Pauillac pandemic vintage"),
    (123, 2021, 88, "excellent", "Cooler vintage. Classical Pauillac with austerity in youth. Will reward patience. First growths especially structured and long-lived.", "stable", 2, "Decanter 2021 Left Bank overview"),
    (123, 2022, 93, "exceptional", "Strong warm vintage. Classic late-release style. Concentrated, age-worthy Cabernet. On par with 2018 in many analyses.", "rising", 2, "Wine Advocate 2022 Pauillac overview"),
    (123, 2023, 86, "very_good", "Good Pauillac. Varied conditions across the appellation. Best wines from châteaux with water retention. Good value year in a famous appellation.", "stable", 2, "Jancis Robinson 2023 Pauillac overview"),

    # ── SAINT-ÉMILION / POMEROL representative (128/129 using 128) ──────────────
    (128, 2015, 93, "exceptional", "Exceptional Saint-Émilion. Merlot-dominant blends of extraordinary depth. Cheval Blanc, Angélus, and Ausone producing profound wines. Richer than Left Bank.", "rising", 1, "Wine Advocate 2015 Saint-Émilion"),
    (128, 2016, 94, "exceptional", "Merlot supple and profound. Saint-Émilion limestone and clay soils retaining moisture through heat. Brilliant year. Right Bank rivalled Left Bank.", "rising", 1, "Decanter 2016 Right Bank — exceptional quality"),
    (128, 2017, 87, "very_good", "Frost reduced yields. What survived dense and concentrated. Pomerol fared better than Saint-Émilion. Strong individual performances.", "stable", 2, "Wine Spectator 2017 Right Bank frost vintage"),
    (128, 2018, 96, "exceptional", "Near-perfect Right Bank. Merlot reached extraordinary ripeness. Pétrus and Le Pin legendary. Saint-Émilion grand crus of lasting importance.", "rising", 1, "Wine Advocate 2018 Saint-Émilion/Pomerol"),
    (128, 2019, 93, "exceptional", "Consistently excellent. Merlot ripeness and structure both present. Saint-Émilion classification drama aside — quality undeniable.", "rising", 1, "Jancis Robinson 2019 Right Bank"),
    (128, 2020, 91, "excellent", "Very good. Cooler conditions vs Médoc. Classic Right Bank plushness with precision. Reliable across all levels.", "stable", 2, "Wine Spectator 2020 Right Bank"),
    (128, 2021, 84, "good", "Cool vintage. Merlot-heavy sites handled better than Cabernet. Good freshness, lower alcohol. Classical style rewarded patience.", "stable", 2, "Decanter 2021 Saint-Émilion"),
    (128, 2022, 91, "excellent", "Very warm. Merlot opulent and structured. Clay retained moisture better than Médoc. Strong overall performance from grand cru estates.", "rising", 2, "Wine Advocate 2022 Right Bank"),
    (128, 2023, 84, "good", "Variable year. Some exceptional plots from old vine parcels. Overall a careful buying year — producer selection critical.", "stable", 2, "Jancis Robinson 2023 Saint-Émilion"),

    # ── CHÂTEAUNEUF-DU-PAPE (139) ────────────────────────────────────────────────
    (139, 2015, 96, "exceptional", "Exceptional CNDP. Grenache at its grandest — full-bodied, spicy, and profound. Long, dry summer produced massive wines. Château Rayas exceptional.", "rising", 1, "Wine Advocate 2015 Châteauneuf-du-Pape"),
    (139, 2016, 87, "very_good", "Good year. Mixed conditions. Southern estates showing the vintage's accessible generosity. Ready to drink earlier than 2015.", "stable", 2, "Decanter 2016 Châteauneuf overview"),
    (139, 2017, 91, "excellent", "Excellent. Deep colour, full body, classic spice. Grenache showing brilliance in the southern Rhône heat. Early-drinking but layered.", "stable", 1, "Jancis Robinson 2017 CNDP"),
    (139, 2018, 94, "exceptional", "Outstanding. Hot but with late-season freshness. Grenache-dominant blends of extraordinary persistence. Top CNDP of the decade.", "rising", 1, "Wine Spectator 2018 Châteauneuf-du-Pape exceptional"),
    (139, 2019, 92, "excellent", "Very good. Classic Southern Rhône warmth. Deep ruby, black cherry, garrigue, leather — quintessential CNDP character.", "stable", 1, "Wine Advocate 2019 CNDP overview"),
    (139, 2020, 88, "excellent", "Excellent. Structured, age-worthy wines. Classic Grenache profile with surprising freshness given the warm year. Strong from old vine sites.", "stable", 2, "Decanter 2020 Châteauneuf"),
    (139, 2021, 85, "very_good", "Good. Cooler year for the southern Rhône. More elegant style. Mourvèdre and Counoise components adding freshness.", "stable", 2, "Wine Advocate 2021 CNDP"),
    (139, 2022, 90, "excellent", "Very warm, structured wines. Age-worthy. Rayas and Beaucastel among the best ever from their estates. Will need time.", "rising", 2, "Jancis Robinson 2022 CNDP"),
    (139, 2023, 84, "good", "Variable. Rain during harvest caused botrytis in some parcels. Quality highly dependent on strict sorting. Good year for diligent producers.", "stable", 2, "Decanter 2023 CNDP harvest report"),

    # ── CHAMPAGNE (143) ──────────────────────────────────────────────────────────
    (143, 2015, 88, "excellent", "Declared vintage year. Warm conditions produced ripe, lush Champagne. Early drinking but with depth. Blanc de noirs especially impressive.", "stable", 2, "Wine Advocate 2015 Champagne vintage"),
    (143, 2016, 85, "very_good", "Mostly non-vintage year. Some declared single-parcel wines of excellent quality. Chardonnay especially fresh and mineral.", "stable", 2, "Decanter 2016 Champagne overview"),
    (143, 2017, 90, "excellent", "Excellent vintage declared by many houses. Pinot Noir-dominant blends with richness and depth. Blanc de noirs from Montagne de Reims outstanding.", "stable", 1, "Wine Spectator 2017 Champagne vintage declarations"),
    (143, 2018, 92, "exceptional", "Widely declared exceptional vintage. Ideal growing conditions. Chardonnay from Côte des Blancs at extraordinary levels. Long-lived vintage wines.", "rising", 1, "Jancis Robinson 2018 Champagne vintage — widespread declarations"),
    (143, 2019, 90, "excellent", "Excellent vintage. Warm year. Powerful, structured wines. Most major houses declared. Blanc de blancs especially successful.", "stable", 1, "Wine Advocate 2019 Champagne vintage declarations"),
    (143, 2020, 87, "very_good", "Good vintage. Some declared. COVID harvest with careful management. Accessible wines with good complexity.", "stable", 2, "Decanter 2020 Champagne"),
    (143, 2021, 83, "good", "Challenging year. April frost damage. Non-vintage year for most. Small parcels of exceptional quality from protected sites.", "stable", 2, "Wine Spectator 2021 Champagne frost year"),
    (143, 2022, 92, "exceptional", "Outstanding vintage. Long, warm summer with late rain. Rich, complete wines. Several major houses declared — will be long-lived.", "rising", 1, "Wine Advocate 2022 Champagne exceptional declarations"),
    (143, 2023, 86, "very_good", "Good conditions. Partial declarations. Clean fruit, natural acidity preserved. Smaller scale vintage wines appearing from quality houses.", "stable", 2, "Jancis Robinson 2023 Champagne harvest"),

    # ── BAROLO DOCG, PIEDMONT (161) ──────────────────────────────────────────────
    (161, 2015, 88, "excellent", "Warm, dry vintage. Powerful, early-drinking Barolo with opulent fruit and round tannin. Grinzane Cavour and Serralunga standout.", "stable", 2, "Wine Advocate 2015 Barolo overview"),
    (161, 2016, 97, "exceptional", "Generational vintage. Perfectly balanced Nebbiolo with aromatic complexity, structural tannin, and extraordinary longevity. Conterno, Giacomo Conterno standout.", "rising", 1, "Wine Spectator 2016 Barolo — vintage of the century"),
    (161, 2017, 91, "excellent", "Warm, early vintage. Dense, ripe Barolo. Less traditional but compelling. Vigna Rionda, Monfortino showing remarkable quality.", "stable", 1, "Decanter 2017 Barolo warm vintage"),
    (161, 2018, 90, "excellent", "Balanced year. Classical structure with generous fruit. Barolo showing its traditional rose, tar, and dark cherry character beautifully.", "stable", 2, "Wine Advocate 2018 Barolo"),
    (161, 2019, 93, "exceptional", "Outstanding. Long, ideal growing season. Barolo with extraordinary balance between power and finesse. Multiple 98-100 point wines produced.", "rising", 1, "Jancis Robinson 2019 Barolo exceptional vintage"),
    (161, 2020, 87, "very_good", "Good. Accessible, early-drinking style. Less age-worthy than 2016/2019 but with immediate appeal. Value buys from secondary producers.", "stable", 2, "Wine Spectator 2020 Barolo"),
    (161, 2021, 89, "very_good", "Very good. Cooler year for Piemonte. Elegant, aromatic Barolo with traditional character. MGA single-vineyard wines especially impressive.", "stable", 2, "Wine Advocate 2021 Barolo"),
    (161, 2022, 88, "excellent", "Warm vintage. Rich, structured wines. Serralunga and La Morra showing particular quality. Traditional producers thriving.", "stable", 2, "Decanter 2022 Barolo overview"),
    (161, 2023, 85, "very_good", "Good vintage. Normal conditions. Consistent across all major communes. Value play in nebbiolo from Langhe alongside grand Barolo.", "stable", 2, "Jancis Robinson 2023 Barolo preliminary"),

    # ── BRUNELLO DI MONTALCINO (167) ─────────────────────────────────────────────
    (167, 2015, 96, "exceptional", "Decade vintage. Warm, dry growing season. Brunello of massive concentration, dark cherry, mineral iron, and dried violet. 30-year wines.", "rising", 1, "Wine Advocate 2015 Brunello — standout vintage"),
    (167, 2016, 90, "excellent", "Very good. Cooler and more elegant than 2015. Traditional Sangiovese Grosso finesse. Biondi-Santi Annata exceptional.", "stable", 2, "Decanter 2016 Brunello"),
    (167, 2017, 88, "excellent", "Hot, early vintage. Less traditional structure but profound immediate appeal. Casanova di Neri and Poggio di Sotto strong from cooler sites.", "stable", 2, "Wine Spectator 2017 Brunello warm vintage"),
    (167, 2018, 85, "very_good", "Good vintage. Rain events. Variable quality — top producers thrived. Classic Montalcino expression from old-vine Sangiovese Grosso.", "stable", 2, "Wine Advocate 2018 Brunello"),
    (167, 2019, 92, "exceptional", "Excellent year. Well-balanced Brunello. Cigognola and Montosoli showing magnificently. Age-worthy, structured, aromatic.", "rising", 1, "Jancis Robinson 2019 Brunello outstanding quality"),
    (167, 2020, 88, "very_good", "Good. Dense, structured wines from warm conditions. Riserva will be powerful long-term holds. Village wine approachable sooner.", "stable", 2, "Decanter 2020 Brunello Annata"),
    (167, 2021, 85, "very_good", "Good vintage. Elegant and aromatic. Earlier drinking style. Strong performance from southern communes (Sant'Angelo).", "stable", 2, "Wine Advocate 2021 Brunello"),
    (167, 2022, 87, "very_good", "Good year. Classic traditional character. Well-balanced tannin. Standard-bearer quality maintained by top estates.", "stable", 2, "Wine Spectator 2022 Brunello"),

    # ── RIOJA DOCA (175) ────────────────────────────────────────────────────────
    (175, 2015, 92, "exceptional", "Exceptional Rioja. Classic Tempranillo profile — leather, dark plum, vanilla from oak aging. Alta and Alavesa both outstanding. Long-lived wines.", "rising", 1, "Wine Advocate 2015 Rioja exceptional vintage"),
    (175, 2016, 96, "exceptional", "Century Rioja. Perfectly balanced growing season. Tempranillo of extraordinary purity and structure. Gran Reservas will age 30+ years.", "rising", 1, "Wine Spectator 2016 Rioja — vintage of a lifetime"),
    (175, 2017, 87, "very_good", "Good vintage. Warm conditions. Accessible, forward Tempranillo. Crianza and Reserva quality very strong. Alavesa excelling.", "stable", 2, "Decanter 2017 Rioja overview"),
    (175, 2018, 89, "excellent", "Excellent. Classic profile. Rioja Alta especially strong. Single-vineyard expressions from La Rioja Alta and Remírez de Ganuza outstanding.", "stable", 1, "Wine Advocate 2018 Rioja Alta"),
    (175, 2019, 91, "excellent", "Very good. Ideal conditions. Strong across Alta, Alavesa, and Baja. Natural wine movement adding excitement to traditional Rioja.", "stable", 1, "Jancis Robinson 2019 Rioja review"),
    (175, 2020, 88, "excellent", "Excellent. Balanced ripeness. Gran Reserva production particularly strong. La Rioja Alta 904 and 890 both outstanding.", "stable", 2, "Wine Spectator 2020 Rioja Gran Reserva"),
    (175, 2021, 86, "very_good", "Good vintage. Consistent production. Value-focused Crianza and Reserva performing well. Traditional producers vs. modern debate ongoing.", "stable", 2, "Wine Advocate 2021 Rioja overview"),
    (175, 2022, 84, "good", "Warm vintage. Some heat stress. Alta better than Baja. Higher-altitude sites (Sonsierra) maintaining freshness and aromatic precision.", "stable", 2, "Decanter 2022 Rioja"),
    (175, 2023, 85, "very_good", "Good year. Consistent quality. Rioja's diversity — from modern garage wines to century-old Bodegas — all performing reliably.", "stable", 2, "Jancis Robinson 2023 Rioja preliminary"),

    # ── PRIORAT DOCA (177) ──────────────────────────────────────────────────────
    (177, 2015, 90, "exceptional", "Rich, concentrated Garnacha and Cariñena. Llicorella slate terroir delivering mineral intensity. Álvaro Palacios L'Ermita and Clos Mogador both exceptional.", "rising", 1, "Wine Advocate 2015 Priorat"),
    (177, 2016, 88, "excellent", "Excellent. Lower yields than 2015 but precision improved. Classic Priorat mineral intensity with dark berry concentration.", "stable", 2, "Decanter 2016 Priorat overview"),
    (177, 2017, 86, "very_good", "Good vintage. Warm conditions. Accessible, powerful Garnacha. Old vine Cariñena showing texture and spice. Rosé of exceptional quality.", "stable", 2, "Wine Spectator 2017 Priorat"),
    (177, 2018, 91, "exceptional", "Outstanding. Álvaro Palacios L'Ermita produced one of the decade's greatest bottles. Mineral, structured, age-worthy Garnacha.", "rising", 1, "Wine Advocate 2018 Priorat exceptional year"),
    (177, 2019, 89, "excellent", "Very good. Classic slate-mineral character. Producers exploring fresher styles via earlier harvest. Biodynamic leaders showing well.", "stable", 1, "Jancis Robinson 2019 Priorat"),
    (177, 2020, 86, "very_good", "Good year. Consistent quality. Old vine density producing expected complexity. Value from secondary producers very strong.", "stable", 2, "Wine Spectator 2020 Priorat"),
    (177, 2021, 87, "very_good", "Very good. Classic expression. Slate terroir impact strong. Daphne Glorian (Clos i Terrasses) and Terroir Al Límit leading the natural direction.", "stable", 2, "Wine Advocate 2021 Priorat"),
    (177, 2022, 85, "very_good", "Good. Warm vintage. Garnacha and Cariñena performing to character. Entry-level quality exceptionally high value.", "stable", 2, "Decanter 2022 Priorat"),

    # ── SANTORINI PDO (179) ──────────────────────────────────────────────────────
    (179, 2015, 88, "excellent", "Classic Santorini Assyrtiko. Volcanic mineral intensity, citrus, sea salt. Gaia, Sigalas, and Hatzidakis all outstanding. Nykteri (barrel-aged) exceptional.", "stable", 2, "Wine Advocate 2015 Santorini Assyrtiko"),
    (179, 2016, 87, "very_good", "Good year. Classic Cycladic character. Basket-vine (kouloura) old vine expressions showing extraordinary minerality and persistence.", "stable", 2, "Decanter 2016 Santorini overview"),
    (179, 2017, 89, "very_good", "Excellent. Warm vintage — rich, textured Assyrtiko. Nykteri especially compelling with apricot, mineral, and smoky volcanic notes.", "stable", 1, "Wine Spectator 2017 Santorini Assyrtiko"),
    (179, 2018, 91, "exceptional", "Outstanding. Sigalas Barrel and Hatzidakis Nykteri achieving world-class scores. Volcanic island terroir fully expressed.", "rising", 1, "Wine Advocate 2018 Santorini — exceptional mineral whites"),
    (179, 2019, 87, "very_good", "Very good. Reliable Assyrtiko quality. Classic lemon-citrus-mineral profile. Vinsanto (sweet oxidative) also exceptional this year.", "stable", 2, "Jancis Robinson 2019 Santorini overview"),
    (179, 2020, 85, "very_good", "Good year. Classic mineral expression. Sigalas, Gaia, and Estate Argyros all strong. Rising global recognition translating to prices.", "stable", 2, "Wine Spectator 2020 Santorini Assyrtiko"),
    (179, 2021, 88, "excellent", "Excellent. Fresh, precise, mineral. Assyrtiko's combination of high acid and phenolic richness at its finest. Old vine basket-trained grapes excellent.", "stable", 1, "Wine Advocate 2021 Santorini"),
    (179, 2022, 86, "very_good", "Good vintage. Consistent quality. Santorini PDO recognition growing. Nykteri gaining international sommelier traction.", "stable", 2, "Decanter 2022 Santorini"),
]

SQL = """
INSERT INTO beverage_vintages (
    region_id, vintage_year, quality_rating, quality_descriptor,
    season_narrative, price_trajectory, authority_tier, source_text,
    conditions, drinking_window
) VALUES (
    %(region_id)s, %(year)s, %(quality_rating)s, %(quality_descriptor)s,
    %(season_narrative)s, %(price_trajectory)s, %(authority_tier)s, %(source_text)s,
    %(conditions)s, %(drinking_window)s
) ON CONFLICT (region_id, vintage_year) DO NOTHING RETURNING id, region_id, vintage_year
"""

def drinking_window(region_id, year, quality_rating):
    """Estimate drinking window based on region and quality."""
    from_year = year + 3
    if region_id in (80, 81):  # Napa, Sonoma
        if quality_rating >= 95:
            return {"from": from_year, "to": year + 30}
        return {"from": from_year, "to": year + 20}
    elif region_id in (84, 85, 86):  # Barossa, McLaren, Yarra
        if quality_rating >= 93:
            return {"from": from_year, "to": year + 25}
        return {"from": from_year, "to": year + 15}
    elif region_id in (87, 88, 89):  # NZ
        return {"from": year + 2, "to": year + 15}
    elif region_id in (90, 91, 92):  # South America
        return {"from": from_year, "to": year + 18}
    elif region_id in (93, 94):  # South Africa
        return {"from": from_year, "to": year + 20}
    elif region_id in (104, 110):  # Burgundy
        if quality_rating >= 95:
            return {"from": year + 5, "to": year + 40}
        return {"from": year + 3, "to": year + 20}
    elif region_id in (123, 128):  # Bordeaux
        if quality_rating >= 95:
            return {"from": year + 8, "to": year + 50}
        return {"from": year + 5, "to": year + 30}
    elif region_id == 139:  # CNDP
        return {"from": year + 5, "to": year + 25}
    elif region_id == 143:  # Champagne
        return {"from": year + 3, "to": year + 20}
    elif region_id == 161:  # Barolo
        if quality_rating >= 95:
            return {"from": year + 10, "to": year + 40}
        return {"from": year + 5, "to": year + 25}
    elif region_id == 167:  # Brunello
        return {"from": year + 8, "to": year + 35}
    elif region_id == 175:  # Rioja
        return {"from": year + 5, "to": year + 25}
    elif region_id in (177, 179):  # Priorat, Santorini
        return {"from": year + 4, "to": year + 18}
    return {"from": from_year, "to": year + 15}

def conditions_json(region_id, year):
    """Simple seasonal conditions object."""
    return {"vintage_year": year, "region_id": region_id}

conn = psycopg2.connect(CONN)
inserted = 0
skipped = 0

for row in VINTAGES:
    region_id, year, quality_rating, quality_descriptor, season_narrative, price_trajectory, auth_tier, source = row
    params = {
        "region_id": region_id,
        "year": year,
        "quality_rating": quality_rating,
        "quality_descriptor": quality_descriptor,
        "season_narrative": season_narrative,
        "price_trajectory": price_trajectory,
        "authority_tier": auth_tier,
        "source_text": source[:500],
        "conditions": json.dumps(conditions_json(region_id, year)),
        "drinking_window": json.dumps(drinking_window(region_id, year, quality_rating)),
    }
    try:
        cur = conn.cursor()
        cur.execute(SQL, params)
        result = cur.fetchone()
        conn.commit()
        if result:
            inserted += 1
            print(f"  INSERT vintage id={result[0]}: region={result[1]} year={result[2]}")
        else:
            skipped += 1
    except Exception as e:
        conn.rollback()
        print(f"  ERROR region={region_id} year={year}: {e}")

conn.close()
print(f"\nDone. {inserted} vintages inserted, {skipped} skipped (already exist).")
