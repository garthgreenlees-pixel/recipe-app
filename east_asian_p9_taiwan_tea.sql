-- East Asian Phase 9: Taiwan High Mountain Oolong — 10 beverage_products
-- Regions: Central Taiwan Highlands=63 (Alishan, Lishan, Dayuling), Dong Ding=64
-- Producers: Alishan Cooperative=140, Wang Family=141, Dong Ding Cooperative=142
-- Importer/curators: Floating Leaves=133, Rishi Tea=134 (already created)

BEGIN;

-- ============================================================
-- CENTRAL TAIWAN HIGHLANDS — High Mountain Oolong (region=63)
-- Producers: Alishan Cooperative=140, Wang Family=141, Floating Leaves=133
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Alishan High Mountain Oolong — Spring Harvest', 'tea', 'oolong_high_mountain', 140, 63, 'Taiwan',
 'Alishan (阿里山) is the most widely known of Taiwan''s high mountain tea regions, its tea gardens strung along ridges at 1,000–1,600m elevation above Chiayi County. The combination of high altitude (cold nights dramatically slow leaf development), mountain mist (natural shading), and volcanic soil produces the defining characteristics of Taiwanese gaoshan (高山, high mountain) oolong: a thick, creamy texture, vivid floral aroma, and a natural milk-like sweetness absent from lowland teas. The spring harvest (chun cha), picked in late March–April, is the prestige picking of the year. The Alishan Tea Cooperative works with over 200 small farm families to maintain traditional hand-harvesting and charcoal processing standards.',
 'estate', 'premium',
 ARRAY['cream', 'jasmine', 'lily', 'fresh butter', 'tropical melon', 'light honey', 'lingering milky sweetness'],
 '{"style": "lightly oxidised high mountain oolong (25-35% oxidation)", "origin": "Alishan, Chiayi County, Taiwan", "elevation_m": 1400, "harvest": "spring (chun cha, March-April)", "oxidation_pct": 30, "roast": "minimal", "character": "creamy texture, intense floral, natural milk sweetness"}',
 '{"brew_temp_c": 90, "steep_time_first": "45 seconds", "vessel": "porcelain gaiwan or small teapot 100-150ml", "leaf_to_water_ratio": "7g per 100ml", "infusions": "5-8", "notes": "each infusion reveals different character — floral peaks at 2nd, sweetness at 4th; do not squeeze leaves between infusions"}',
 '{"elevation_m": 1400, "oxidation": "25-35%", "roast": "minimal/none", "harvest_season": "spring", "cultivar": "Qingxin Oolong (most common) or Four Seasons", "processing": "hand-harvest, sun-wither, indoor wither, light tumbling"}',
 true),

('Alishan High Mountain Oolong — Winter Harvest', 'tea', 'oolong_high_mountain', 140, 63, 'Taiwan',
 'The winter harvest (dong cha, 冬茶) of Alishan oolong is prized by connoisseurs for a different quality than the spring: cooler temperatures produce slower-growing leaves with higher amino acid accumulation, resulting in a deeper sweetness, thicker texture, and a distinctive osmanthus-honey character. Less volume is produced than spring harvest, and the cold weather at altitude creates growing conditions that concentrate the leaf''s essential oils. For a seasonal beverage programme, spring and winter Alishan harvests represent complementary expressions — the same terroir at opposite ends of the year''s flavour arc.',
 'estate', 'premium',
 ARRAY['osmanthus flower', 'honey', 'winter melon', 'thick cream', 'brown sugar', 'tropical fruit', 'deep sweetness'],
 '{"style": "lightly oxidised high mountain oolong", "origin": "Alishan, Taiwan", "elevation_m": 1400, "harvest": "winter (dong cha, November-December)", "oxidation_pct": 30, "character": "deeper sweetness and honey character than spring harvest; osmanthus-dominant"}',
 '{"brew_temp_c": 90, "steep_time_first": "45 seconds", "vessel": "porcelain gaiwan 100ml", "leaf_to_water_ratio": "7g per 100ml", "infusions": "6-8"}',
 '{"harvest_season": "winter", "elevation_m": 1400, "oxidation": "25-35%", "character_vs_spring": "deeper, sweeter, honey-dominant vs spring floral"}',
 true),

('Lishan High Mountain Oolong — Wang Family 2,200m', 'tea', 'oolong_high_mountain', 141, 63, 'Taiwan',
 'Lishan (梨山, Pear Mountain) sits at 2,000–2,400m elevation in Taichung County, making it one of Taiwan''s highest tea-growing regions. At this altitude the growing season is compressed: frost risk is real, harvests are limited to twice a year, and the resulting leaves have an intensity that the lower Alishan gardens cannot match. The Wang Family tea farm at 2,200m produces only 400kg per year — a micro-scale operation where every harvest is personally supervised. The Lishan character is distinctive: less creamy and more crystalline than Alishan, with an almost mineral precision to the floral notes and a clean, sharp high-toned finish reminiscent of fresh spring water.',
 'reserve', 'ultra_premium',
 ARRAY['high-toned jasmine', 'crystal mineral', 'spring water', 'orchid', 'light honey', 'white grape', 'fresh and clean', 'sharper than Alishan'],
 '{"style": "lightly oxidised ultra-high mountain oolong", "origin": "Lishan, Taichung County, Taiwan", "elevation_m": 2200, "harvest": "spring and fall (two harvests only)", "oxidation_pct": 25, "roast": "none", "character": "crystalline, mineral-precise, high-toned — sharper and cleaner than Alishan"}',
 '{"brew_temp_c": 88, "steep_time_first": "40 seconds", "vessel": "porcelain gaiwan 100ml", "leaf_to_water_ratio": "6-7g per 100ml", "infusions": "5-7", "notes": "slightly lower temperature than Alishan — higher elevation teas are more delicate; no tumbling between infusions"}',
 '{"elevation_m": 2200, "farm": "Wang Family private estate", "annual_production_kg": 400, "oxidation": "20-25%", "harvests_per_year": 2}',
 true),

('Dayuling Ultra-High Mountain Oolong 2,500m', 'tea', 'oolong_high_mountain', 141, 63, 'Taiwan',
 'Dayuling (大禹嶺, Great Yu Ridge) is Taiwan''s most exalted and controversial tea origin — gardens at 2,400–2,600m elevation on a military road above Lishan, accessible only by permit due to the proximity to water reservoirs. At these heights, the growing season is 6 months shorter than lowland teas, frost comes in November, and yields are so small that authentic Dayuling commands prices exceeding Japanese gyokuro or high-grade Wuyi yancha. The character is the apotheosis of high-mountain oolong: impossibly clean, mineral, and floral, with a texture that coats the palate like silk and a finish lasting 20–30 minutes. For a serious tea programme, a single seasonal purchase of genuine Dayuling defines the programme''s ceiling.',
 'reserve', 'ultra_premium',
 ARRAY['glacial mineral', 'high-toned orchid', 'lily of the valley', 'silk texture', 'white peach', 'spring frost', 'impossibly long finish'],
 '{"style": "ultra-high mountain oolong", "origin": "Dayuling, Heping District, Taichung, Taiwan", "elevation_m": 2500, "access": "permit required (proximity to water reservoirs)", "oxidation_pct": 20, "character": "the apex of Taiwan high mountain oolong — mineral, silk, extraordinary length"}',
 '{"brew_temp_c": 85, "steep_time_first": "30 seconds", "vessel": "porcelain gaiwan 100ml — no zisha (clay would absorb the delicate aromatics)", "leaf_to_water_ratio": "6g per 100ml", "infusions": "5-7", "notes": "Dayuling reveals itself over many infusions — do not rush; the 4th and 5th infusions are often the most revealing"}',
 '{"elevation_m": 2500, "oxidation": "18-22%", "harvest_season": "fall only (spring at risk of frost)", "availability": "extremely limited — seasonal purchase required", "authentication": "request harvest certificate and altitude documentation"}',
 true),

('Oriental Beauty (Dong Fang Mei Ren) Oolong', 'tea', 'oolong_baozhong', 141, 63, 'Taiwan',
 'Oriental Beauty (東方美人, Dong Fang Mei Ren) is one of Taiwan''s most distinctive and celebrated oolongs — unlike any other tea in the world because its defining character comes from insect damage rather than human intervention. The tea leafhopper (Jacobiasca formosana) bites the young leaves and buds during summer; the plant responds by producing defence compounds that, when the leaf is then hand-picked and processed, create an extraordinary natural muscatel, honey, and ripe fruit character. Queen Elizabeth II named it "Oriental Beauty" when she tasted it in 1970. At 60–80% oxidation, it is the most heavily oxidised of Taiwan''s green oolongs and drinks more like a delicate red wine than a conventional tea.',
 'reserve', 'ultra_premium',
 ARRAY['muscatel grape', 'honey', 'ripe peach', 'cinnamon', 'vanilla', 'wild honey', 'beeswax', 'dried apricot', 'red wine character'],
 '{"style": "heavily oxidised oolong (unique insect bite process)", "origin": "Hsinchu and Miaoli counties, Taiwan (Wang Family source from Hsinchu)", "oxidation_pct": 70, "insect_bite": true, "character": "muscatel, honey, dried fruit — unlike all other Taiwan oolongs; closest to a light red wine in tea form", "historical_note": "named Oriental Beauty by Queen Elizabeth II, 1970"}',
 '{"brew_temp_c": 90, "steep_time_first": "60 seconds", "vessel": "glass or porcelain (colour appreciation)", "leaf_to_water_ratio": "5-6g per 150ml", "infusions": "4-6", "notes": "amber/red liquor colour distinguishes authentic Oriental Beauty; 60 second first steep — needs time to open"}',
 '{"oxidation": "60-80%", "insect_component": "Jacobiasca formosana leafhopper bite required", "harvest_season": "summer only (June-July when leafhoppers active)", "colour": "amber to red-orange", "cultivar": "Bai Hao (white-tipped varieties)"}',
 true);

-- ============================================================
-- DONG DING — Traditional Roasted Oolong (region=64)
-- Producer: Dong Ding Tea Cooperative=142
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Dong Ding Traditional Charcoal-Roasted Oolong', 'tea', 'oolong_dong_ding', 142, 64, 'Taiwan',
 'Dong Ding (凍頂, Frozen Summit) is the original prestige tea of Taiwan, introduced from Wuyi, Fujian by Lin Fengchi in 1855 via a seedling from Wuyi rock tea. The Dong Ding Cooperative in Lugu, Nantou County maintains the traditional style: medium oxidation (35–40%) followed by heavy charcoal roasting in multiple sessions over months. Where modern Dong Ding has moved toward lighter green oolongs, the traditional roasted style represents a link to the Wuyi rock oolong heritage of the cultivar''s origin. The result is complex: roasted honey, osmanthus, aged wood, and mineral that unfolds across 8–10 infusions. A serious tea for serious drinkers.',
 'reserve', 'ultra_premium',
 ARRAY['roasted honey', 'osmanthus flower', 'aged wood', 'dark caramel', 'warm mineral', 'dried apricot', 'lingering warmth'],
 '{"style": "traditional heavy-roast Dong Ding oolong", "origin": "Lugu Township, Nantou County, Taiwan", "elevation_m": 800, "oxidation_pct": 38, "roast": "heavy charcoal (multiple sessions)", "historical_origin": "Wuyi rock tea lineage introduced 1855", "character": "roasted, honey, mineral — the traditional roasted style"}',
 '{"brew_temp_c": 95, "steep_time_first": "30 seconds", "vessel": "small zisha or porcelain gaiwan 100ml", "leaf_to_water_ratio": "7-8g per 100ml", "infusions": "8-10", "notes": "rinse once; heavy roast Dong Ding improves dramatically after the 3rd infusion; pour fully between each infusion"}',
 '{"elevation_m": 800, "roast_level": "heavy charcoal", "roast_sessions": "multiple over 6 months", "oxidation": "35-40%", "cultivar": "Qingxin Oolong (original Wuyi lineage)", "historical_note": "introduced from Wuyi 1855 by Lin Fengchi"}',
 true),

('Dong Ding Modern Lightly Roasted Oolong', 'tea', 'oolong_dong_ding', 142, 64, 'Taiwan',
 'The modern style of Dong Ding oolong, which emerged in the 1980s, uses significantly lighter oxidation (15–20%) and minimal roasting — a response to market demand for greener, more floral oolongs that appeal to a broader audience. The result is quite different from the traditional roasted style: butter, milk, and fresh flowers rather than roasted honey and mineral. The Dong Ding Cooperative produces both styles to capture the market for each. For a beverage programme, the modern and traditional styles served side by side provide a compelling illustration of how processing transforms a single origin and cultivar into dramatically different drinking experiences.',
 'estate', 'mid_range',
 ARRAY['fresh butter', 'lily', 'cream', 'light floral', 'mild sweetness', 'clean finish'],
 '{"style": "modern lightly-roasted Dong Ding oolong", "origin": "Lugu Township, Nantou County, Taiwan", "elevation_m": 800, "oxidation_pct": 18, "roast": "light", "character": "buttery, floral, clean — modern market style"}',
 '{"brew_temp_c": 90, "steep_time_first": "45 seconds", "vessel": "porcelain gaiwan 100ml", "leaf_to_water_ratio": "7g per 100ml", "infusions": "5-7"}',
 '{"oxidation": "15-20%", "roast": "minimal", "elevation_m": 800, "style": "modern/qingxiang approach to Dong Ding"}',
 true),

('Floating Leaves Taiwan Jin Xuan Milk Oolong', 'tea', 'oolong_high_mountain', 133, 63, 'Taiwan',
 'Jin Xuan (金萱, Golden Daylily, also called #12) is a cultivar developed by the Taiwan Tea Research and Extension Station in 1980, engineered specifically for high-mountain production. It naturally produces a distinctive creamy, milky character from the cultivar''s own biochemistry — not from any additive (authentic Jin Xuan needs no milk flavouring, which is added to inferior versions). Floating Leaves Tea (Seattle) sources Jin Xuan directly from farms in the Alishan region for their BC/WA market. The milky-floral character is the most immediately accessible of all Taiwan oolongs and an outstanding introduction to the category for new guests.',
 'estate', 'premium',
 ARRAY['fresh milk', 'cream', 'taro', 'lily', 'tropical butter', 'light floral', 'clean sweetness'],
 '{"style": "cultivar-specific lightly oxidised oolong", "origin": "Alishan region, Taiwan (Floating Leaves sourcing)", "cultivar": "Jin Xuan (#12)", "oxidation_pct": 25, "character": "natural milk-cream from cultivar; no additive — authentic natural creaminess", "caution": "many commercial Jin Xuan products use artificial milk flavouring; sourcing from Floating Leaves ensures authenticity"}',
 '{"brew_temp_c": 88, "steep_time_first": "45 seconds", "vessel": "porcelain gaiwan or small teapot", "leaf_to_water_ratio": "7g per 100ml", "infusions": "5-7"}',
 '{"cultivar": "Jin Xuan (TRES #12)", "developed": "1980 Taiwan Tea Research Station", "oxidation": "20-30%", "natural_milk_compound": "true — from cultivar; verify no artificial flavour"}',
 true),

('Floating Leaves Taiwan Baozhong (Pouchong) Oolong', 'tea', 'oolong_baozhong', 133, 63, 'Taiwan',
 'Baozhong (包種, wrapped kind) is the lightest of Taiwan''s oolongs — only 12–18% oxidation, it sits at the boundary between green tea and oolong. Grown primarily in Pinglin District, New Taipei City, and processed with a distinctive twisting (rather than rolling) that produces loosely furled leaves with extraordinary aromatic volatility. Floating Leaves Tea sources direct from Pinglin farms. The floral profile of Baozhong is among the most intense of any tea: fresh orchid, gardenia, and green flowers in a light, clean, almost weightless infusion. For a hospitality programme: Baozhong is the most delicate formal introduction to Taiwan tea, ideal before a meal.',
 'estate', 'premium',
 ARRAY['fresh orchid', 'gardenia', 'jasmine', 'light green flowers', 'spring dew', 'clean sweetness', 'weightless finish'],
 '{"style": "lightly oxidised baozhong oolong", "origin": "Pinglin, New Taipei City, Taiwan (Floating Leaves sourcing)", "oxidation_pct": 15, "shape": "loosely twisted (not rolled ball)", "character": "most floral and delicate of Taiwan oolongs; near green tea character"}',
 '{"brew_temp_c": 85, "steep_time_first": "60 seconds", "vessel": "porcelain gaiwan (no clay — delicate aromatics)", "leaf_to_water_ratio": "5-6g per 150ml", "infusions": "3-5", "notes": "very delicate — do not use above 90°C; use 85°C for first infusion"}',
 '{"oxidation": "12-18%", "shape": "loosely twisted", "origin": "Pinglin, New Taipei", "cultivar": "Qingxin Oolong"}',
 true);

COMMIT;
