-- East Asian Phase 10: India Tea — 15 beverage_products
-- Regions: Darjeeling=65, Assam=66, Nilgiri=67
-- Producers: Makaibari=143, Castleton=144, Glenburn=145, Jungpana=146,
--            Halmari=147, Kairbetta=148, Harney & Sons=149

BEGIN;

-- ============================================================
-- DARJEELING — First Flush, Second Flush, Autumn Flush
-- Producers: Makaibari=143, Castleton=144, Glenburn=145, Jungpana=146
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Makaibari Darjeeling First Flush Biodynamic', 'tea', 'darjeeling_first_flush', 143, 65, 'India',
 'Makaibari Tea Estate (est. 1859) in Kurseong, Darjeeling is the world''s oldest tea factory and a pioneer of biodynamic tea cultivation under the stewardship of Rajah Banerjee — who received Demeter biodynamic certification in 1988, the first tea estate in the world to do so. The first flush (February–April harvest) is Darjeeling''s most celebrated picking: green leaves emerge after winter dormancy with the highest concentration of the characteristic muscatel grape and fresh flower compounds. At only 15–20% oxidation, first flush Darjeeling is closer to white tea than black — the golden-green liquor and floral intensity are immediately distinctive. Best drunk plain, without milk.',
 'reserve', 'ultra_premium',
 ARRAY['muscatel grape', 'fresh orchid', 'spring grass', 'light astringency', 'green plum', 'citrus zest', 'mineral', 'delicate floral'],
 '{"style": "Darjeeling first flush (lightly oxidised)", "estate": "Makaibari, Kurseong, Darjeeling", "elevation_m": 2000, "harvest": "first flush (February-April)", "oxidation_pct": 18, "certification": "biodynamic (Demeter), organic", "character": "muscatel, floral, light astringency — drink plain, no milk"}',
 '{"brew_temp_c": 85, "steep_time_min": "2-3", "vessel": "white porcelain or glass", "leaf_to_water_g_per_ml": "3g per 200ml", "infusions": 2, "milk": "never — first flush Darjeeling must be drunk plain"}',
 '{"harvest_months": "February-April", "oxidation": "15-20%", "elevation_m": 2000, "certification": "Demeter biodynamic since 1988 — first in world", "estate": "Makaibari, Kurseong"}',
 true),

('Castleton Darjeeling Second Flush Muscatel', 'tea', 'darjeeling_second_flush', 144, 65, 'India',
 'Castleton Estate in Kurseong, Darjeeling is consistently ranked among the world''s great tea estates — its second flush (May–June harvest) muscatel grade is frequently the highest-priced Darjeeling at auction, with single-garden lots exceeding €1,000/kg in exceptional years. The second flush produces the most intense muscatel character of the Darjeeling calendar: full oxidation of the leaf creates a complex profile of Muscat grapes, apricot jam, rich flowers, and a characteristic warm finish. Unlike first flush, second flush Darjeeling has enough body to take a small splash of milk, though purists prefer it straight.',
 'reserve', 'ultra_premium',
 ARRAY['Muscat grape', 'apricot jam', 'rose', 'warm spice', 'full body', 'malty', 'dried stone fruit', 'long finish'],
 '{"style": "Darjeeling second flush (full oxidised, muscatel grade)", "estate": "Castleton, Kurseong, Darjeeling", "elevation_m": 1700, "harvest": "second flush (May-June)", "oxidation_pct": 80, "muscatel_grade": true, "character": "intense muscatel, apricot, full body — the apex of Darjeeling second flush"}',
 '{"brew_temp_c": 90, "steep_time_min": "3-4", "vessel": "white porcelain cup", "leaf_to_water_g_per_ml": "3g per 200ml", "infusions": 2, "milk": "optional — small splash acceptable; purists prefer straight"}',
 '{"harvest_months": "May-June", "oxidation": "75-85%", "elevation_m": 1700, "estate": "Castleton, Kurseong", "grade": "FTGFOP1 muscatel"}',
 true),

('Glenburn Estate Darjeeling Second Flush', 'tea', 'darjeeling_second_flush', 145, 65, 'India',
 'Glenburn Tea Estate sits at 1,600–1,700m in the Rangeet River valley, Darjeeling, producing elegant second flush teas with a slightly softer, more floral character than the intense muscatel of Kurseong estates. Glenburn is also one of Darjeeling''s premier tea tourism destinations — a working estate with a boutique hotel where guests experience tea from field to cup. For a restaurant programme, Glenburn represents a compelling story beyond the tea itself: estate provenance, traceable harvest, and the human geography of a 19th-century plantation in transition to contemporary hospitality.',
 'estate', 'premium',
 ARRAY['muscatel', 'dried apricot', 'rose petal', 'malty', 'woody', 'light spice', 'warm finish'],
 '{"style": "Darjeeling second flush", "estate": "Glenburn, Rangeet River valley, Darjeeling", "elevation_m": 1650, "harvest": "second flush (May-June)", "oxidation_pct": 75, "character": "softer and more floral than Castleton; elegant muscatel"}',
 '{"brew_temp_c": 90, "steep_time_min": "3", "vessel": "white porcelain", "leaf_to_water_g_per_ml": "3g per 200ml", "infusions": 2}',
 '{"estate": "Glenburn, Rangeet valley", "elevation_m": 1650, "oxidation": "70-80%"}',
 true),

('Jungpana Estate Darjeeling Autumn Flush', 'tea', 'darjeeling_autumnal', 146, 65, 'India',
 'Jungpana Tea Estate, one of Darjeeling''s most venerable gardens at 1,800m elevation in Kurseong, produces a particularly noteworthy autumn flush (October–November harvest) — the third and final major picking of the Darjeeling year. Where first and second flush command the highest prices, the autumn flush (also called autumnal) offers full-oxidised character at a more accessible price point: the cooler temperatures of October produce a denser, more malty leaf with a characteristic dried fruit and woodsy character. Less muscatel intensity than second flush, but excellent structure for milk service — the autumnal is the Darjeeling for afternoon tea.',
 'estate', 'premium',
 ARRAY['malt', 'dried fruit', 'wood', 'earthy', 'warm spice', 'medium body', 'autumn apple', 'good with milk'],
 '{"style": "Darjeeling autumnal (autumn flush)", "estate": "Jungpana, Kurseong, Darjeeling", "elevation_m": 1800, "harvest": "autumnal (October-November)", "oxidation_pct": 85, "character": "malt-dominant, dried fruit, woodsy — excellent with milk"}',
 '{"brew_temp_c": 92, "steep_time_min": "4", "vessel": "white porcelain or mug", "leaf_to_water_g_per_ml": "3g per 200ml", "milk": "recommended — the autumnal is designed for milk service", "infusions": 2}',
 '{"harvest_months": "October-November", "oxidation": "80-90%", "elevation_m": 1800, "estate": "Jungpana, Kurseong"}',
 true),

('Jungpana Darjeeling White Tea Silver Tips', 'tea', 'white_tea', 146, 65, 'India',
 'Darjeeling white tea — made from only the unopened silver buds of the tea plant at Jungpana''s high-altitude gardens — is a rare and largely unknown category that bridges the Japanese gyokuro and Chinese white tea traditions through an Indian terroir. The silver buds are hand-picked in spring during the first flush window, sun-withered for 48 hours, and dried without rolling or oxidation. The result is entirely unlike black Darjeeling: a pale golden liquor with muscatel-honey character in a completely delicate, weightless form. For a beverage programme, Darjeeling white tea is a discovery piece — virtually unknown outside specialist circles.',
 'reserve', 'ultra_premium',
 ARRAY['muscatel honey', 'white peach', 'spring flowers', 'delicate sweetness', 'clean', 'no astringency', 'crystalline finish'],
 '{"style": "Darjeeling white tea (silver buds)", "estate": "Jungpana, Kurseong, Darjeeling", "elevation_m": 1800, "processing": "sun-wither, no rolling, no oxidation", "character": "muscatel character in delicate weightless form — no astringency"}',
 '{"brew_temp_c": 75, "steep_time_min": "3", "vessel": "glass or white porcelain", "leaf_to_water_g_per_ml": "4g per 200ml", "milk": "never", "infusions": 3}',
 '{"leaf_grade": "silver buds only", "processing": "sun-withered, natural dry", "oxidation": "minimal", "harvest": "spring first flush window"}',
 true);

-- ============================================================
-- ASSAM — Orthodox and CTC styles
-- Producer: Halmari=147, Harney & Sons=149
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Halmari Gold Assam Orthodox First Flush', 'tea', 'assam_orthodox', 147, 66, 'India',
 'Halmari Tea Estate in Dooars, Assam, has been rated the world''s best Assam estate multiple times at the Chai Awards and Tea Guild of America competitions. Unlike most Assam tea produced as CTC (cut-tear-curl) for mass market, Halmari produces traditional orthodox whole-leaf tea using slow, complete oxidation that creates the full complexity the Assam region is capable of. The first flush from Halmari (March–April) shows a lighter, more floral expression than the classic malty Assam character — an excellent illustration that "Assam" encompasses enormous internal diversity. The tea grows on the alluvial plains at relatively low elevation (60–120m), receiving extraordinary rainfall that produces the Assamica varietal''s characteristic muscular structure.',
 'reserve', 'premium',
 ARRAY['malt', 'caramel', 'light floral', 'honey', 'toast', 'warm earth', 'clean finish'],
 '{"style": "Assam orthodox black tea — first flush", "estate": "Halmari, Dooars, Assam", "elevation_m": 90, "harvest": "first flush (March-April)", "oxidation_pct": 85, "varietal": "Assamica", "character": "lighter and more floral than Assam second flush — malt with honey and flowers"}',
 '{"brew_temp_c": 95, "steep_time_min": "3-4", "vessel": "teapot or mug", "leaf_to_water_g_per_ml": "3-4g per 200ml", "milk": "excellent with milk — the structure supports it", "infusions": 2}',
 '{"estate": "Halmari, Dooars, Assam", "elevation_m": 90, "varietal": "Assamica", "harvest": "first flush", "processing": "orthodox whole-leaf"}',
 true),

('Halmari Estate Second Flush Assam Classic', 'tea', 'assam_orthodox', 147, 66, 'India',
 'The second flush Assam from Halmari (May–June) is the estate''s signature and the expression that has repeatedly won international recognition. Full oxidation of mature Assamica leaves produces the archetypal Assam character: dense malt, dark caramel, muscular tannin, and a robustness that welcomes milk without losing its identity. For the service professional, this is the essential benchmark Assam: the tea against which all other Assam teas are measured. A single-estate orthodox Assam drunk with good whole milk is one of the great everyday beverage pleasures in the world — no ceremony required.',
 'reserve', 'premium',
 ARRAY['dense malt', 'dark caramel', 'muscular tannin', 'honey', 'molasses', 'full body', 'long warming finish', 'excellent with milk'],
 '{"style": "Assam orthodox black tea — second flush", "estate": "Halmari, Dooars, Assam", "elevation_m": 90, "harvest": "second flush (May-June)", "oxidation_pct": 95, "character": "the benchmark Assam: full malt, caramel, muscular — ideal with milk", "award": "World''s Best Assam Tea multiple years"}',
 '{"brew_temp_c": 98, "steep_time_min": "4", "vessel": "teapot or mug", "leaf_to_water_g_per_ml": "4g per 200ml", "milk": "strongly recommended — pour milk into cup first (hotelier method)", "infusions": 2}',
 '{"estate": "Halmari, Dooars, Assam", "elevation_m": 90, "harvest": "second flush", "grade": "TGFOP1", "processing": "full orthodox oxidation"}',
 true),

('Harney & Sons Assam Irish Breakfast Blend', 'tea', 'assam_blend', 149, 66, 'India',
 'Harney & Sons (Millerton, NY) is North America''s most prestigious specialty tea house and a key supplier across BC and WA through direct and Sysco channels. Their Assam-dominant Irish Breakfast blend uses CTC Assam as its foundation — the industrial processing method that creates small, uniform particles with maximum extraction speed. Irish Breakfast is the daily-service benchmark for North American hospitality: robust, straight tea or with milk, brewed quickly, consistent batch to batch. For restaurants requiring reliable high-volume Assam service, this is the professionally positioned standard.',
 'market', 'mid_range',
 ARRAY['strong malt', 'caramel', 'full body', 'robust tannin', 'clean', 'consistent'],
 '{"style": "CTC Assam dominant blend", "origin": "Assam blend (Harney & Sons, NY)", "processing": "CTC (cut-tear-curl)", "character": "strong, consistent, quick-brewing — daily service standard", "availability": "Sysco, direct; widely available in BC and WA"}',
 '{"brew_temp_c": 98, "steep_time_min": "3", "vessel": "teapot or mug", "leaf_to_water_g_per_ml": "3g per 200ml", "milk": "the intended preparation"}',
 '{"processing": "CTC", "blend": true, "sourcing": "Assam dominant", "format": "loose and sachet options"}',
 true);

-- ============================================================
-- NILGIRI — Blue Mountain and frost tea
-- Producer: Kairbetta=148, Harney & Sons=149
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Kairbetta Estate Nilgiri Frost Tea (Tippy)', 'tea', 'nilgiri_frost', 148, 67, 'India',
 'Nilgiri (meaning "Blue Mountains" in Tamil) tea is the least internationally known of India''s three great tea regions despite producing some of its most distinctive flavour profiles. Kairbetta Estate at 1,800m in the Ooty district produces an exceptional frost tea — a late-season harvest (December–January) when temperature drops damage the leaf and trigger the same biochemical response as the leafhoppers in Oriental Beauty oolong: defence compounds that, when oxidised, create a naturally sweet, floral character entirely different from the standard Nilgiri profile. The frost tea is Nilgiri''s premium expression and one of India''s most genuinely distinctive specialty teas.',
 'reserve', 'premium',
 ARRAY['natural sweetness', 'eucalyptus', 'menthol', 'light floral', 'bright citrus', 'clean malt', 'no astringency', 'long finish'],
 '{"style": "Nilgiri frost tea (winter harvest)", "estate": "Kairbetta, Ooty District, Tamil Nadu, India", "elevation_m": 1800, "harvest": "frost tea (December-January)", "oxidation_pct": 80, "character": "natural sweetness from frost-stress response; menthol, eucalyptus, clean"}',
 '{"brew_temp_c": 92, "steep_time_min": "3", "vessel": "white porcelain", "leaf_to_water_g_per_ml": "3g per 200ml", "milk": "optional — works either way", "notes": "the natural sweetness is self-contained; less demanding than Darjeeling but equally distinctive"}',
 '{"harvest_months": "December-January", "oxidation": "75-85%", "estate": "Kairbetta, Nilgiris", "elevation_m": 1800, "frost_mechanism": "cold damage triggers terpene compounds similar to leafhopper bite in Oriental Beauty"}',
 true),

('Harney & Sons Nilgiri Black Tea', 'tea', 'nilgiri_orthodox', 149, 67, 'India',
 'Harney & Sons Nilgiri represents the accessible and consistent face of Blue Mountain tea in North American hospitality — a blended orthodox Nilgiri that captures the region''s characteristic brightness, clean citrus-adjacent character, and smooth body without the complexity and price of a single-estate frost tea. Nilgiri orthodox teas are exceptionally well-suited to iced tea preparation: the bright, clean character that reads slightly thin when hot becomes vivid and refreshing over ice. For a BC restaurant programme: the ideal candidate for house iced tea — more interesting than standard commodity Ceylon but as straightforward to prepare.',
 'market', 'mid_range',
 ARRAY['bright citrus', 'light malt', 'clean', 'mild floral', 'smooth tannin', 'refreshing'],
 '{"style": "Nilgiri orthodox black tea", "origin": "Nilgiri district blend (Harney & Sons)", "elevation_m_approx": 1500, "oxidation_pct": 80, "character": "bright, clean, citrus-adjacent — excellent for iced tea", "availability": "Sysco, direct; BC and WA distribution"}',
 '{"brew_temp_c": 95, "steep_time_min": "3", "vessel": "teapot or iced tea pitcher", "leaf_to_water_g_per_ml": "4g per 200ml", "iced_tea_note": "excellent iced — brew double strength, pour over ice immediately"}',
 '{"processing": "orthodox", "blend": "Nilgiri district", "format": "loose leaf", "best_use": "iced tea; everyday service"}',
 true),

('Glenburn Darjeeling Oolong Spring Harvest', 'tea', 'oolong_darjeeling', 145, 65, 'India',
 'Glenburn Estate''s Darjeeling oolong occupies a fascinating position: processed to 40–50% oxidation — full oolong range — from Darjeeling''s AV2 cultivar, which was bred specifically to deliver the muscatel character. The result sits precisely between a Taiwan high mountain oolong and a classic Darjeeling first flush: the muscatel and floral notes of Darjeeling combined with the thick, creamy texture and multiple-infusion character of oolong processing. Very few estates produce Darjeeling oolong at this quality level. For a tea-forward hospitality programme, this is a genuinely unique discovery piece for guests who know both categories.',
 'estate', 'premium',
 ARRAY['muscatel', 'fresh orchid', 'cream', 'stone fruit', 'light malt', 'medium body', 'clean finish'],
 '{"style": "Darjeeling oolong (unique hybrid processing)", "estate": "Glenburn, Darjeeling", "elevation_m": 1650, "oxidation_pct": 45, "character": "muscatel-floral Darjeeling character in oolong-style processing — multiple infusions, creamy texture"}',
 '{"brew_temp_c": 88, "steep_time_first": "60 seconds", "vessel": "porcelain gaiwan 100-150ml", "leaf_to_water_ratio": "5-6g per 100ml", "infusions": "4-6"}',
 '{"oxidation": "40-50%", "cultivar": "AV2 Darjeeling", "estate": "Glenburn", "style": "oolong processing applied to Darjeeling leaf"}',
 true);

COMMIT;
