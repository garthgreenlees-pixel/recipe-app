-- East Asian Phase 8: Baijiu — 10 beverage_products
-- Regions: Guizhou=61 (Moutai), Sichuan=62 (Wuliangye, Luzhou Laojiao)
-- Producers: Kweichow Moutai=135, Wuliangye=136, Luzhou Laojiao=137, Fenjiu=138, Guilin Sanhua=139
-- Note: Fenjiu is from Shanxi (no Shanxi region created); use region_id=61 (Guizhou) for context,
--       or NULL region for Fenjiu. Guilin Sanhua from Guangxi.

BEGIN;

-- ============================================================
-- GUIZHOU — Moutai (Kweichow Moutai=135, region=61)
-- Sauce-aroma (jiangxiang) style
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Kweichow Moutai Feitian (Flying Fairy) Baijiu', 'baijiu', 'jiangxiang', 135, 61, 'China',
 'Moutai Feitian (飛天茅台) is the most iconic baijiu in the world — China''s national spirit, central to diplomacy, business relationships, and ceremonial toasting for more than a century. The "Flying Fairy" label was created in the 1950s for export and has become synonymous with Chinese prestige. Made from red sorghum (hongying) in Maotai Town, Guizhou, using a process of nine steaming cycles and eight fermentations over three years, it exemplifies the jiangxiang (sauce aroma) style: complex, fermented-grain intensity, profound umami, aged earth, and a finish that can persist for an hour. At 53% ABV, Feitian is consumed neat at room temperature — preferably in a series of ganbei (dry cup) toasts.',
 'reserve', 'ultra_premium',
 ARRAY['fermented grain', 'soy sauce umami', 'dried tropical fruit', 'aged wood', 'mushroom', 'smoke', 'medicinal herbs', 'long hot finish'],
 '{"style": "jiangxiang (sauce-aroma) baijiu", "origin": "Maotai Town, Renhuai, Guizhou", "abv": 53, "colour": "crystal clear", "character": "intense, complex, umami-rich, long finish", "cultural_significance": "national spirit of China; diplomatic protocol; ganbei tradition"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (jiu bei, 30-50ml)", "serve_size_ml": 50, "method": "neat only — no ice, no mixer", "ritual": "ganbei (dry cup): all drink simultaneously on call; host pours for guests, not oneself", "notes": "second pour often more revealing than first; warming in palm opens aromatics"}',
 '{"production_process": "nine steams, eight fermentations, seven distillations over 3 years", "grain": "Maotai town Hongying red sorghum", "water": "Chishui River", "aging": "minimum 3 years earthenware jar", "koji_type": "large daqu (高梁 sorghum substrate)", "abv": 53}',
 true),

('Kweichow Moutai 15-Year Aged Baijiu', 'baijiu', 'jiangxiang', 135, 61, 'China',
 'The 15-Year expression represents Moutai''s entry into declared aged statements — base spirit of the same jiangxiang process as Feitian but selected from lots aged a minimum of 15 years in traditional Guizhou earthenware jars. The additional aging rounds off the sharpest edges of the young Feitian and introduces deeper wood integration, dried fruit complexity, and a smoother entry. This is the expression for serious engagement with jiangxiang baijiu beyond the ceremonial: slower, more contemplative, more suitable for the Western-informed spirit enthusiast.',
 'reserve', 'ultra_premium',
 ARRAY['aged wood', 'dark chocolate', 'dried longan', 'fermented soy', 'incense', 'smoked plum', 'tobacco', 'exceptional length'],
 '{"style": "jiangxiang baijiu, 15-year aged", "origin": "Maotai Town, Guizhou", "abv": 53, "aging": "15+ years earthenware", "character": "rounder and deeper than Feitian — dried fruit, aged wood, incense"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (30-50ml)", "method": "neat only", "serve_size_ml": 50, "notes": "excellent candidate for cross-category pairing with aged shou pu-erh — both are complex, fermented, long-aged"}',
 '{"aging_years": 15, "grain": "Hongying red sorghum", "production": "same as Feitian, extended aging", "abv": 53}',
 true),

('Moutai Prince (Ren Yi) Baijiu', 'baijiu', 'jiangxiang', 135, 61, 'China',
 'Moutai Prince (王子酒, Renyi Jiangxiang) is the accessible tier of the Kweichow Moutai family — a genuine jiangxiang baijiu produced at the same Maotai distillery using the same process as Feitian, but aged 3–5 years rather than 5+ years and selected from a different lot profile. It retains the characteristic sauce-aroma style at approximately one-tenth the price of Feitian. For a restaurant programme introducing baijiu to new guests, Moutai Prince is the ideal entry point: the style is authentic, the brand recognition is immediate, and the price allows for exploratory by-the-glass service.',
 'estate', 'premium',
 ARRAY['soy sauce', 'roasted grain', 'fermented fruit', 'mushroom', 'dried herbs', 'warming finish'],
 '{"style": "jiangxiang baijiu", "origin": "Maotai Town, Guizhou", "abv": 53, "character": "same style as Feitian, earlier in development", "positioning": "accessible entry to Moutai jiangxiang style"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup", "method": "neat", "serve_size_ml": 50}',
 '{"tier": "entry within Moutai family", "aging": "3-5 years", "grain": "Hongying sorghum", "abv": 53}',
 true);

-- ============================================================
-- SICHUAN — Wuliangye & Luzhou Laojiao (region=62)
-- Nongxiang (strong-aroma) style
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Wuliangye Classic Nongxiang Baijiu', 'baijiu', 'nongxiang', 136, 62, 'China',
 'Wuliangye (五粮液, Five Grain Liquid) is China''s largest-selling premium baijiu and the definitive expression of nongxiang (strong-aroma) style — a direct competitor to Moutai''s jiangxiang dominance. Made from five grains (sorghum, rice, glutinous rice, wheat, maize) in Yibin, Sichuan, using a centuries-old mud pit fermentation (jiaomu, pits some dating to the Ming dynasty), the spirit is sweeter, fruitier, and more immediately approachable than Moutai: anise, pear, and sweet grain with a clean, warming finish. At 52% ABV it remains a substantial spirit, but nongxiang is generally more accessible to Western spirits drinkers encountering baijiu for the first time.',
 'reserve', 'ultra_premium',
 ARRAY['anise', 'sweet pear', 'roasted grain', 'butterscotch', 'tropical fruit', 'warm spice', 'clean finish'],
 '{"style": "nongxiang (strong-aroma) baijiu", "origin": "Yibin, Sichuan", "abv": 52, "colour": "crystal clear", "grain_recipe": "five grains: sorghum, rice, glutinous rice, wheat, maize", "character": "sweeter and fruitier than Moutai; approachable for Western spirits drinkers"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (30-50ml)", "method": "neat only", "serve_size_ml": 50, "food_pairing": "Sichuan cuisine; fatty braised meats; dim sum"}',
 '{"grain": "five grains (wuliang)", "fermentation": "mud pit (jiaomu) — Ming dynasty pits", "production_city": "Yibin, Sichuan", "abv": 52, "style_type": "nongxiang"}',
 true),

('Luzhou Laojiao National Cellar 1573 Nongxiang', 'baijiu', 'nongxiang', 137, 62, 'China',
 'Luzhou Laojiao (泸州老窖, Old Cellar of Luzhou) produced the first officially recognised baijiu in Chinese history and owns the world''s oldest continuously used fermentation pits — the National Cellar (国窖) pits dating to 1573 during the Ming dynasty, now a UNESCO intangible cultural heritage site. National Cellar 1573 is the flagship expression, drawing from the oldest pits for a complexity that no new facility can replicate: the microbial ecosystem of a 450-year-old mud pit is the terroir of Chinese spirits. The style is nongxiang: softer, fruitier, and more petal-like than Moutai, with a floral complexity unique to the ancient pits.',
 'reserve', 'ultra_premium',
 ARRAY['jasmine', 'sweet pear', 'anise', 'orchid', 'butterscotch', 'roasted grain', 'ancient earth', 'delicate finish'],
 '{"style": "nongxiang (strong-aroma) baijiu", "origin": "Luzhou, Sichuan", "abv": 52, "fermentation_pits": "National Cellar 1573 pits (UNESCO heritage, Ming dynasty 1573)", "character": "floral, delicate, complex pit character"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (30-50ml)", "method": "neat only", "serve_size_ml": 50}',
 '{"pit_age_years": 450, "pit_designation": "National Cellar (国窖)", "heritage": "UNESCO intangible cultural heritage", "abv": 52, "grain": "sorghum"}',
 true),

('Luzhou Laojiao Zisha Touqu 68° Nongxiang', 'baijiu', 'nongxiang', 137, 62, 'China',
 'The Zisha Touqu (紫砂頭曲) is Luzhou Laojiao''s high-proof raw distillate expression at 68% ABV — the first-run (tou qu) spirit taken from the earliest fraction of each distillation, before dilution to standard proof. At this strength it is an intense, almost overwhelming encounter with nongxiang baijiu''s character in concentrated form: anise, pear, and fermented grain amplified to the point of sensory saturation. For the beverage professional, this is an educational tool as much as a drinking spirit — understanding the raw distillate explains the softened commercial expression.',
 'estate', 'premium',
 ARRAY['concentrated anise', 'overripe pear', 'ethanol heat', 'roasted grain', 'medicinal herbs', 'floral esters'],
 '{"style": "nongxiang baijiu (raw high-proof expression)", "origin": "Luzhou, Sichuan", "abv": 68, "fraction": "first run (tou qu) — highest ester fraction", "serving_note": "dilute 1:1 with mineral water is acceptable"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (20-30ml)", "method": "neat or diluted 1:1", "serve_size_ml": 30, "notes": "educational pairing with standard 1573 to demonstrate the distillation arc"}',
 '{"abv": 68, "fraction": "tou qu (first run)", "style": "nongxiang", "note": "often diluted for service"}',
 true);

-- ============================================================
-- SHANXI (no Shanxi region — using Guizhou=61 as placeholder) — Fenjiu (Fenxiang style)
-- GUANGXI (no region) — Guilin Sanhua (Milder style)
-- Producer: Fenjiu=138, Guilin Sanhua=139
-- Use NULL region for Fenjiu (Shanxi); Guangdong=60 region for Guilin Sanhua (approximation)
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Fenjiu Blue and White Porcelain 20-Year Fenxiang Baijiu', 'baijiu', 'qingxiang', 138, NULL, 'China',
 'Fenjiu (汾酒) is China''s oldest documented baijiu, with written records of its production in Xinghua Village, Fenyang, Shanxi dating to the 1,500-year-old Northern Qi dynasty records. The fenxiang (light-aroma) style it exemplifies is the cleanest, most elegant, and least confrontational of the major baijiu categories — clear and pure without the heavy fermented intensity of jiangxiang or the sweetness of nongxiang. The 20-year Blue and White Porcelain (Qinghua Ci) expression, named for the classic Ming ceramic style, is the prestige statement from this ancient distillery: twice-distilled, extended aging, exceptional clarity. An extraordinary entry point for the Western spirits professional exploring baijiu.',
 'reserve', 'premium',
 ARRAY['fresh grain', 'light pear', 'clean flowers', 'mild anise', 'delicate sweetness', 'elegant finish', 'no heavy earthiness'],
 '{"style": "fenxiang (light-aroma/pure-aroma) baijiu", "origin": "Xinghua Village, Fenyang, Shanxi", "abv": 53, "colour": "crystal clear", "character": "the lightest and most elegant major baijiu style — ideal gateway for spirits professionals", "historical_note": "China''s oldest documented baijiu production site"}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup (30-50ml)", "method": "neat only", "serve_size_ml": 50, "notes": "fenxiang is the most accessible style for Western spirits drinkers — comparison to clear grain spirits (vodka, pisco) is useful but undersells the depth"}',
 '{"style": "qingxiang/fenxiang", "aging": "20 years", "origin": "Xinghua Village, Fenyang, Shanxi", "abv": 53, "fermentation": "ceramic jar (not mud pit)", "historical_record": "Northern Qi dynasty documents 1500 years ago"}',
 true),

('Guilin Sanhua Baijiu (Three-Flower)', 'baijiu', 'mioxiang', 139, 60, 'China',
 'Guilin Sanhua (桂林三花酒, Three-Flower of Guilin) is produced along the Li River in Guilin, Guangxi, using the local rice as the primary grain — a regional anomaly that produces a lighter, softer, and distinctively floral-rice character entirely unlike the sorghum-based styles of Guizhou and Sichuan. The "three flowers" refers to the three layers of bubbles that form when the bottle is shaken — a traditional quality test. Stored in caves beneath the karst limestone mountains for 2–3 years, it absorbs a subtle mineral quality from the rock. A gateway baijiu that bridges toward Japanese shochu and Taiwanese grain spirits for guests navigating the category.',
 'estate', 'mid_range',
 ARRAY['rice sweetness', 'jasmine', 'light grain', 'floral', 'mild sweetness', 'clean mineral', 'soft finish'],
 '{"style": "rice-based baijiu (mioxiang/rice-aroma)", "origin": "Guilin, Guangxi", "abv": 57, "grain": "rice (not sorghum)", "character": "softest and most floral major baijiu style; rice-dominant", "cave_aging": true}',
 '{"serve_temp_c": 20, "vessel": "small baijiu cup or sake cup", "method": "neat or lightly chilled", "serve_size_ml": 50, "notes": "the softest introduction to baijiu; suitable as a rice-wine bridge between sake and full baijiu"}',
 '{"grain": "rice", "aging_location": "karst limestone caves", "aging_years": "2-3", "abv": 57, "style": "mioxiang (rice aroma)"}',
 true);

COMMIT;
