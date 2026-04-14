-- East Asian Phase 7: China Gongfu Tea — 25 beverage_products
-- Regions: Yunnan=57, Fujian=58, Zhejiang=59, Guangdong=60
-- Producers: Menghai=127, Wuyi Xingcun=128, Yunnan Sourcing=129, Song Tea=130,
--            West Lake Longjing=131, Phoenix Village=132, Floating Leaves=133, Rishi Tea=134

BEGIN;

-- ============================================================
-- YUNNAN — Pu-erh & Black Tea (Menghai=127, Yunnan Sourcing=129)
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Dayi 7542 Sheng (Raw) Pu-erh Cake', 'tea', 'puerh_sheng', 127, 57, 'China',
 'The Menghai Tea Factory 7542 is the most widely recognised benchmark raw (sheng) pu-erh in the world — the recipe number (75=year created, 4=grade of leaf, 2=Menghai factory code) has been in continuous production since 1975. Made from Yunnan broad-leaf Da Ye varietal maocha, each 357g pressed cake is designed for long-term ageing: the young tea is astringent and grassy; after 10–20 years of dry-storage it transforms into something of profound complexity. A living document of terroir and time.',
 'estate', 'mid_range',
 ARRAY['young: green, grassy, astringent', 'stone fruits', 'camphor', 'aged: dried longan', 'mushroom', 'forest floor', 'dark chocolate', 'leather'],
 '{"style": "sheng puerh", "region": "Yunnan", "varietal": "Da Ye broad-leaf", "format": "357g pressed cake", "aging_potential": "10-30 years", "storage": "dry storage preferred", "puerh_type": "raw/sheng"}',
 '{"brew_temp_c": 95, "steep_time_first": "15-30 seconds", "vessel": "gaiwan or yixing zisha teapot", "leaf_to_water_ratio": "5-7g per 100ml", "water_hardness": "soft filtered", "rinse_recommended": true, "infusions": "8-12", "notes": "rinse 5 seconds; short flash infusions for young cake; longer for aged"}',
 '{"producer_code": "7542", "year_range": "1975-present", "factory_code": "2=Menghai", "weight": "357g cake", "compression": "stone-pressed", "oxidation": "minimal post-fermentation", "storage_notes": "dry storage; ventilated; no humidity control"}',
 true),

('Dayi 7572 Shou (Ripe) Pu-erh Tuocha', 'tea', 'puerh_shou', 127, 57, 'China',
 'The 7572 is the definitive benchmark ripe (shou) pu-erh — a recipe that established the standard for the post-fermentation (wodui) process developed at Menghai Tea Factory in 1973. Where the 7542 requires decades of patience, the 7572 delivers immediate drinking pleasure: dark, earthy, smooth, and warming. The tuo cha (bowl) format (100g) is the most common form for daily consumption. An essential reference point for understanding the full range of pu-erh styles.',
 'market', 'mid_range',
 ARRAY['earth', 'forest floor', 'dark chocolate', 'dried dates', 'aged wood', 'mushroom', 'smooth tannin'],
 '{"style": "shou puerh", "region": "Yunnan", "varietal": "Da Ye blend", "format": "100g tuo cha (bowl)", "aging_potential": "drinks well immediately; improves 5-10 years", "storage": "standard", "puerh_type": "ripe/shou"}',
 '{"brew_temp_c": 95, "steep_time_first": "20-30 seconds", "vessel": "gaiwan or dedicated pu-erh teapot", "leaf_to_water_ratio": "6-8g per 100ml", "rinse_recommended": true, "infusions": "8-15", "notes": "two rinses recommended for shou; temperature can go to 100°C"}',
 '{"producer_code": "7572", "factory_code": "2=Menghai", "weight": "100g tuo cha", "post_fermentation": "wodui pile fermentation 45-60 days", "oxidation": "heavily oxidised via microbial activity", "created": "1975"}',
 true),

('Yunnan Sourcing 2020 Yiwu Ancient Tree Sheng Pu-erh', 'tea', 'puerh_sheng', 129, 57, 'China',
 'Yunnan Sourcing is the most trusted English-language source for single-origin pu-erh, operating directly in Yunnan since 2004 with verifiable supply chains. This Yiwu production from 2020 uses leaf from ancient trees (gushu, 古樹) — trees over 100 years old whose deep root systems access mineral layers unavailable to plantation tea. Yiwu (易武) is the most celebrated of the Six Famous Tea Mountains of Xishuangbanna, producing sheng pu-erh of particular grace, soft sweetness, and honey-floral character. An ideal entry point for understanding single-origin terroir in pu-erh.',
 'estate', 'premium',
 ARRAY['wildflower honey', 'apricot', 'white grape', 'fresh hay', 'mineral', 'light camphor', 'persistent sweetness', 'elegant tannin'],
 '{"style": "single-origin sheng puerh", "origin": "Yiwu, Xishuangbanna, Yunnan", "tree_age": "ancient tree (gushu) 100+ years", "harvest": "spring 2020", "aging_potential": "15-30 years from harvest", "puerh_type": "raw/sheng"}',
 '{"brew_temp_c": 90, "steep_time_first": "20 seconds", "vessel": "gaiwan preferred (shows clarity)", "leaf_to_water_ratio": "5-6g per 100ml", "water": "soft filtered essential", "rinse_recommended": true, "infusions": "10-15", "notes": "lower temperature 90°C preserves floral character; short flash infusions"}',
 '{"origin_village": "Yiwu, Xishuangbanna", "tree_type": "gushu ancient tree", "harvest_season": "spring", "year": "2020", "format": "200g cake", "maocha_grade": "mixed young and old leaf"}',
 true),

('Yunnan Sourcing Crimson Flame Dianhong Gold Tips', 'tea', 'black_tea', 129, 57, 'China',
 'Dianhong (滇红, Yunnan Red) is China''s premium black tea — made from the same Da Ye varietal used for pu-erh, but fully oxidised. The golden-tipped version uses only the bud and first leaf at high elevation, producing a tea of extraordinary richness: malty, sweet, with a natural honey quality from the high proportion of golden buds (pekoe). Yunnan Sourcing''s Crimson Flame selection prioritises high-elevation (1,600–2,200m) farms with hand-processing. No milk, no sugar — this tea is complete.',
 'reserve', 'premium',
 ARRAY['golden malt', 'dark honey', 'dried apricot', 'cocoa', 'caramel', 'pepper', 'long finish'],
 '{"style": "full-oxidised black tea", "origin": "Yunnan", "varietal": "Da Ye Yunnan broad-leaf", "elevation_m": 1800, "character": "malty, honey, no astringency"}',
 '{"brew_temp_c": 90, "steep_time_first": "45 seconds", "vessel": "gaiwan or western teapot", "leaf_to_water_ratio": "3-4g per 150ml", "infusions": 4, "notes": "90°C not 100°C — full boil damages the golden buds"}',
 '{"oxidation": "full", "cultivar": "Da Ye", "processing": "hand-rolled, sun-dried, oxidised", "harvest": "spring first flush"}',
 true),

('Yunnan Sourcing 2012 Dry Storage Aged Sheng Pu-erh', 'tea', 'puerh_sheng', 129, 57, 'China',
 'Aged raw pu-erh (10+ years, dry storage) represents one of the most complex and sought-after tea experiences in the world — a genuinely age-transformable beverage comparable in depth to a fine aged Burgundy or single malt whisky. This 2012 Yunnan Sourcing production, stored in dry conditions for 12+ years, has transitioned from the sharp green astringency of youth into something of considerable finesse: dried stone fruit, camphor, aged wood, and mineral depth. The 12-year mark represents the beginning of full integration.',
 'reserve', 'ultra_premium',
 ARRAY['dried longan', 'camphor', 'dried plum', 'aged wood', 'incense', 'mineral', 'leather', 'tobacco leaf'],
 '{"style": "aged sheng puerh 12+ years", "origin": "Yunnan (production area unspecified)", "storage": "dry storage — no traditional warehouse humidity", "vintage": "2012", "aging_potential": "continues to improve 10-20 more years", "puerh_type": "raw/sheng aged"}',
 '{"brew_temp_c": 95, "steep_time_first": "20-30 seconds", "vessel": "dedicated aged puerh teapot (yixing zisha)", "leaf_to_water_ratio": "5-6g per 100ml", "infusions": "12-20", "notes": "aged sheng shows best in zisha teapot; rinse once only; long session drinking"}',
 '{"year": "2012", "storage_type": "dry storage", "age_years": 12, "format": "357g cake", "complexity_tier": "high"}',
 true);

-- ============================================================
-- FUJIAN — Wuyi Rock Oolong, White Tea, Tieguanyin
-- Producers: Wuyi Xingcun=128, Song Tea=130
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Wuyi Xingcun Zhengyan Da Hong Pao Rock Oolong', 'tea', 'oolong_rock', 128, 58, 'China',
 'Da Hong Pao (大红袍, Big Red Robe) is the most celebrated of the Wuyi rock oolongs (yancha) and one of the most storied teas in Chinese history. The name refers to the legend of a Ming dynasty scholar cured of illness by tea from three ancient bushes on Jiulongke cliff — those original bushes still exist and are now protected state property. Wuyi Xingcun''s Zhengyan (正岩, "true rock") production uses leaves grown in the actual Wuyi rock zone (45km²), where mineral-rich volcanic soil and afternoon mist produce the characteristic "yan yun" (rock rhyme) — a lasting mineral sweetness after swallowing.',
 'reserve', 'ultra_premium',
 ARRAY['roasted orchid', 'dark caramel', 'mineral wet stone', 'dried longan', 'cinnamon', 'smoked plum', 'persistent rock rhyme finish'],
 '{"style": "heavy roast yancha (rock oolong)", "origin": "Wuyi Mountains, Fujian — Zhengyan zone", "roast_level": "heavy (multiple roastings)", "oxidation_pct": 50, "yan_yun": "pronounced rock mineral character", "character": "intense, roasted, mineral, long finish"}',
 '{"brew_temp_c": 100, "steep_time_first": "15 seconds", "vessel": "small zisha or porcelain gaiwan 100ml", "leaf_to_water_ratio": "7-8g per 100ml", "infusions": "8-12", "notes": "100°C essential; rock oolongs can take full boil; short flash infusions; patience — opens up after 3rd infusion"}',
 '{"origin_zone": "Zhengyan (core rock area, Wuyi)", "varietal": "Da Hong Pao cultivar", "roast_count": "3-4 seasons of charcoal roasting", "oxidation": "medium-heavy", "processing": "wilting, rolling, oxidation, charcoal roasting"}',
 true),

('Wuyi Xingcun Shui Xian (Water Sprite) Rock Oolong', 'tea', 'oolong_rock', 128, 58, 'China',
 'Shui Xian (水仙, Water Sprite) is one of the four great Wuyi rock oolong cultivars and the most widely planted in the Wuyi region. Where Da Hong Pao is roasted to intensity, Shui Xian is typically roasted more lightly and produces a more floral, orchid-forward profile — the name (water sprite or water narcissus) describes the scent of the fresh leaf. Wuyi Xingcun''s Zhengyan Shui Xian demonstrates the yan yun rock mineral character in a more approachable register than Da Hong Pao, making it an excellent introduction to Wuyi yancha for new guests.',
 'estate', 'premium',
 ARRAY['water narcissus', 'roasted orchid', 'creamy malt', 'mineral', 'vanilla', 'dry apricot', 'clean finish'],
 '{"style": "medium-heavy roast yancha", "origin": "Wuyi Mountains, Fujian", "varietal": "Shui Xian cultivar", "roast_level": "medium-heavy", "oxidation_pct": 40, "character": "floral, creamy, mineral — more approachable than Da Hong Pao"}',
 '{"brew_temp_c": 95, "steep_time_first": "20 seconds", "vessel": "gaiwan or zisha 100ml", "leaf_to_water_ratio": "7g per 100ml", "infusions": "8-10"}',
 '{"cultivar": "Shui Xian", "origin_zone": "Wuyi Zhengyan zone", "roast": "medium-heavy charcoal", "oxidation": "medium"}',
 true),

('Wuyi Xingcun Rou Gui (Cinnamon) Rock Oolong', 'tea', 'oolong_rock', 128, 58, 'China',
 'Rou Gui (肉桂, Cinnamon) is the most aromatic and spice-forward of the classic Wuyi rock oolongs — the cultivar produces a distinctive warm cinnamon and clove note that is immediately recognisable. In the last two decades Rou Gui has become the most sought-after cultivar in the Wuyi rock zone, displacing Shui Xian in status and price for premium Zhengyan material. The spice character is intrinsic to the cultivar, not a processing artefact — even at light roast levels it emerges clearly. For the beverage professional, Rou Gui is the most dramatic entry point into yancha.',
 'estate', 'premium',
 ARRAY['cinnamon bark', 'clove', 'roasted caramel', 'stone fruit', 'mineral', 'warm spice finish', 'orchid undertone'],
 '{"style": "medium roast yancha", "varietal": "Rou Gui", "origin": "Wuyi Mountains, Fujian", "roast_level": "medium", "oxidation_pct": 40, "character": "spice-dominant, aromatic, warming"}',
 '{"brew_temp_c": 98, "steep_time_first": "15-20 seconds", "vessel": "gaiwan or zisha", "leaf_to_water_ratio": "7g per 100ml", "infusions": "8-10"}',
 '{"cultivar": "Rou Gui", "roast": "medium charcoal", "oxidation": "medium", "origin_zone": "Wuyi Zhengyan zone"}',
 true),

('Wuyi Xingcun Jin Jun Mei (Golden Horse Eyebrow) Black Tea', 'tea', 'black_tea', 128, 58, 'China',
 'Jin Jun Mei (金骏眉) is the most prestigious Chinese black tea, created in Wuyi in 2005 using only the tender unopened buds of wild Wuyi mountain tea harvested in spring. Each kilogram requires approximately 50,000–80,000 hand-picked buds — a labour that explains its position at the apex of Chinese black tea pricing. The result is entirely unlike Assam or Darjeeling: no astringency, no bitterness, and a natural sweetness reminiscent of sweet potato, honey, and floral notes. Wuyi Xingcun holds authentic Tongmuguan origin, distinguishing it from the many imitations produced across China.',
 'reserve', 'ultra_premium',
 ARRAY['roasted sweet potato', 'dark honey', 'dried chrysanthemum', 'pine smoke', 'caramel', 'light cocoa', 'lingering sweetness'],
 '{"style": "all-bud black tea (fully oxidised)", "origin": "Tongmuguan, Wuyi, Fujian", "leaf_standard": "unopened buds only", "production_kg": "50000-80000 buds per kg", "character": "zero astringency, intense sweetness, floral"}',
 '{"brew_temp_c": 85, "steep_time_first": "30 seconds", "vessel": "small porcelain gaiwan (shows liquor colour)", "leaf_to_water_ratio": "3-4g per 100ml", "infusions": 5, "notes": "do not use boiling water — buds are delicate; lower temperature preserves sweetness"}',
 '{"origin": "Tongmuguan, Wuyi Fujian", "processing": "pine-wood smoked during drying (lapsang origin)", "leaf_grade": "buds only", "created": "2005"}',
 true),

('Song Tea Fuding Bai Hao Yin Zhen (Silver Needle)', 'tea', 'white_tea', 130, 58, 'China',
 'Fuding Bai Hao Yin Zhen (白毫銀針, White Hair Silver Needle) is the king of Chinese white tea — produced only from the unopened buds of the Da Bai varietal in Fuding, Fujian. Song Tea & Ceramics (San Francisco) is one of the most respected American curators of Chinese tea, sourcing directly from known farmers with transparent provenance. Silver Needle undergoes minimal processing: buds are hand-picked in spring, spread in sunlight for 72 hours, and allowed to dry slowly without rolling or firing. The result is a tea of extraordinary delicacy: cool, floral, melon, and a characteristic white peach sweetness.',
 'reserve', 'ultra_premium',
 ARRAY['white peach', 'lily', 'melon rind', 'fresh hay', 'light honey', 'cucumber', 'cool mineral'],
 '{"style": "white tea — bud only", "origin": "Fuding, Fujian", "varietal": "Da Bai (Big White) cultivar", "harvest": "spring (pre-Qingming preferred)", "processing": "minimal — sun-wither 72h, natural dry", "aging_potential": "improves with age up to 15 years"}',
 '{"brew_temp_c": 80, "steep_time_first": "90 seconds", "vessel": "glass or white porcelain gaiwan", "leaf_to_water_ratio": "4-5g per 150ml", "infusions": 4, "notes": "white tea is underextracted by most people; use more leaf and longer time than instinct suggests; glass allows bud appreciation"}',
 '{"leaf_grade": "buds only", "cultivar": "Da Bai", "processing": "sun-withered, no rolling, natural dry", "oxidation_pct": 5, "harvest_season": "spring"}',
 true),

('Song Tea Fuding Bai Mu Dan (White Peony)', 'tea', 'white_tea', 130, 58, 'China',
 'Bai Mu Dan (白牡丹, White Peony) is the second tier of Fuding white tea, using one bud and two leaves rather than bud alone. Song Tea''s selection prioritises high-elevation Fuding farms producing leaves of exceptional quality. Where Silver Needle is all delicacy, White Peony has more body and depth — the two-leaf inclusion brings a slight grassiness, more honey weight, and a longer finish. An excellent everyday companion to Silver Needle, and a tea that ages beautifully: three to five years of proper storage deepens the honey and softens the vegetable notes.',
 'estate', 'premium',
 ARRAY['honeydew melon', 'fresh cut hay', 'light honey', 'cucumber', 'white peach', 'mild vegetable', 'clean finish'],
 '{"style": "white tea — bud and two leaves", "origin": "Fuding, Fujian", "varietal": "Da Bai cultivar", "character": "more body and depth than Silver Needle; honey, melon", "aging_potential": "3-8 years improves to darker, honey, dried fruit"}',
 '{"brew_temp_c": 80, "steep_time_first": "2 minutes", "vessel": "gaiwan or glass", "leaf_to_water_ratio": "4-5g per 150ml", "infusions": 3}',
 '{"leaf_grade": "one bud, two leaves", "processing": "sun-withered, natural dry", "oxidation_pct": 8}',
 true),

('Song Tea Anxi Tieguanyin Traditional Charcoal Roasted', 'tea', 'oolong_tieguanyin', 130, 58, 'China',
 'Tieguanyin (鐵觀音, Iron Goddess of Mercy) is the most celebrated tea of Anxi County, Fujian, and one of the Ten Famous Teas of China. The traditional roasted style (zhongbei cha) has roots in the Song dynasty and represents the historical expression of this cultivar before the lighter green Tieguanyin style emerged in the 1980s. Song Tea''s charcoal-roasted selection uses a multi-month roasting process that transforms the tea: the characteristic orchid-floral aroma remains but is supplemented by warm roasted honey, dried apricot, and a clean, deep mineral finish. Longer-lived and more complex than the green style.',
 'estate', 'premium',
 ARRAY['roasted orchid', 'baked honey', 'dried apricot', 'cinnamon', 'mineral', 'warm finish', 'clean tannin'],
 '{"style": "traditional roasted Tieguanyin", "origin": "Anxi, Fujian", "varietal": "Tieguanyin cultivar", "roast_level": "medium-heavy charcoal", "oxidation_pct": 30, "character": "orchid base with roast complexity"}',
 '{"brew_temp_c": 95, "steep_time_first": "30 seconds", "vessel": "gaiwan or zisha teapot", "leaf_to_water_ratio": "7g per 100ml", "infusions": "7-10"}',
 '{"cultivar": "Tieguanyin", "roast": "multiple charcoal sessions", "style": "traditional/baked (not green)", "origin": "Anxi County"}',
 true),

('Song Tea Anxi Tieguanyin Jade Green (Light Oxidised)', 'tea', 'oolong_tieguanyin', 130, 58, 'China',
 'The jade green (qingxiang) style of Tieguanyin emerged in the 1980s and became the dominant commercial form: lightly oxidised (10–15%), minimally roasted, with a vivid green appearance and strong floral character. Refrigerated to preserve freshness, it represents the contemporary face of Tieguanyin and is the style most commonly encountered in Taiwanese and Southeast Asian tea culture. Song Tea''s selection emphasises the "yin yun" (sound of the goddess) aftertaste — a floral sweetness that lingers 10–15 minutes after the final sip. This is the style served at traditional gongfu tea ceremonies in Fujian homes.',
 'estate', 'mid_range',
 ARRAY['gardenia', 'lily', 'fresh orchid', 'sweet pea', 'butter', 'green grape', 'persistent floral aftertaste'],
 '{"style": "qingxiang (jade green) Tieguanyin", "origin": "Anxi, Fujian", "varietal": "Tieguanyin cultivar", "oxidation_pct": 12, "roast": "minimal", "character": "intensely floral, buttery, light body", "storage": "refrigerated essential"}',
 '{"brew_temp_c": 90, "steep_time_first": "30-45 seconds", "vessel": "porcelain gaiwan preferred (no competing aromas)", "leaf_to_water_ratio": "7g per 100ml", "infusions": "5-7", "notes": "refrigerate until service; bring to room temp 30 min before opening"}',
 '{"cultivar": "Tieguanyin", "oxidation": "10-15%", "roast": "minimal", "style": "qingxiang (fragrant/green)", "storage": "refrigerated"}',
 true);

-- ============================================================
-- ZHEJIANG — Longjing (Dragon Well)
-- Producer: West Lake Longjing Tea Cooperative=131
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('West Lake Longjing Mingqian Pre-Qingming Tribute Grade', 'tea', 'green_tea_china', 131, 59, 'China',
 'Longjing (龍井, Dragon Well) is China''s most celebrated green tea, grown exclusively within a designated zone on the west side of West Lake, Hangzhou, Zhejiang. The Mingqian (明前, before Qingming) grade is harvested before April 4–6 (Qingming Festival) — the earliest and most prized picking of the year, using only the bud and first leaf. The West Lake Longjing Tea Cooperative protects the original production area (Shifeng, Longjing, Yunhe, Hupao, Meijia Wu villages) from the vastly larger generic Zhejiang longjing. Tribute grade Mingqian Longjing is what was historically presented to the Emperor — the sweet, nutty, chestnut character has no equal among green teas.',
 'reserve', 'ultra_premium',
 ARRAY['roasted chestnut', 'fresh sweet pea', 'spring grass', 'toasted sesame', 'light honey', 'crisp mineral', 'no astringency'],
 '{"style": "Chinese pan-fired green tea", "origin": "West Lake Longjing zone, Hangzhou, Zhejiang", "harvest_grade": "Mingqian (pre-Qingming, before April 5)", "leaf_standard": "bud + first leaf (da xi, big finch tongue)", "varietal": "Longjing 43 and Qunti cultivars", "protected_origin": "West Lake designated zone (8km²)"}',
 '{"brew_temp_c": 75, "steep_time_first": "60-90 seconds", "vessel": "glass tumbler (traditional — allows leaf appreciation)", "leaf_to_water_ratio": "3g per 150ml", "infusions": 3, "notes": "pour hot water into glass first, then add leaves; or use standing-pour method; glass is preferred to appreciate the standing leaves"}',
 '{"harvest": "pre-Qingming", "grade": "tribute/mingqian", "processing": "pan-fired in iron wok by hand", "shape": "flat, sword-shaped leaf", "cultivar": "Longjing 43 or Qunti", "colour": "jade green"}',
 true),

('West Lake Longjing Yuqian Spring Grade A', 'tea', 'green_tea_china', 131, 59, 'China',
 'Yuqian (雨前, before Grain Rain) Longjing is harvested between Qingming (April 5) and Grain Rain (April 20) — the second-grade picking that follows the Mingqian. While not as rare as Mingqian, high-quality Yuqian from the West Lake zone is a genuinely exceptional green tea offering more body and depth than the bud-only Mingqian while retaining the signature chestnut and spring grass character. This is the everyday working grade of West Lake Longjing — still from the protected zone, still pan-fired by hand, but more accessible in price.',
 'estate', 'premium',
 ARRAY['roasted chestnut', 'butter', 'spring grass', 'sweet pea', 'light vegetal', 'clean', 'gentle tannin'],
 '{"style": "Chinese pan-fired green tea", "origin": "West Lake Longjing zone, Hangzhou, Zhejiang", "harvest_grade": "Yuqian (pre-Grain Rain)", "leaf_standard": "bud + 1-2 leaves"}',
 '{"brew_temp_c": 75, "steep_time_first": "90 seconds", "vessel": "glass or porcelain gaiwan", "leaf_to_water_ratio": "3-4g per 150ml", "infusions": 3}',
 '{"harvest": "Yuqian (pre-Grain Rain)", "processing": "pan-fired", "shape": "flat sword", "origin": "West Lake zone"}',
 true),

('West Lake Longjing Late Spring Grade B', 'tea', 'green_tea_china', 131, 59, 'China',
 'Third-grade West Lake Longjing, harvested after Grain Rain (April 20) through May — a fuller leaf with more body and a stronger vegetable character. Where Mingqian and Yuqian are delicate, this grade shows more structure: still the characteristic chestnut and buttery notes, but with more tannin presence and a slightly rounder profile. An excellent everyday green tea for high-volume restaurant use where the top-grade cost is prohibitive, while maintaining authentic West Lake protected origin.',
 'market', 'mid_range',
 ARRAY['chestnut', 'butter', 'fresh grass', 'light tannin', 'clean vegetable', 'pleasant finish'],
 '{"style": "pan-fired green tea", "origin": "West Lake Longjing zone", "harvest_grade": "late spring — post-Grain Rain", "character": "more body and tannin than Mingqian"}',
 '{"brew_temp_c": 80, "steep_time_first": "60 seconds", "vessel": "glass or gaiwan", "leaf_to_water_ratio": "4g per 150ml", "infusions": 3}',
 '{"harvest": "post-Grain Rain (May)", "processing": "pan-fired", "grade": "C/everyday"}',
 true);

-- ============================================================
-- GUANGDONG — Fenghuang Dancong Oolong
-- Producers: Phoenix Village=132, Floating Leaves=133
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Phoenix Village Mi Lan Xiang (Honey Orchid) Dancong', 'tea', 'oolong_dancong', 132, 60, 'China',
 'Fenghuang Dancong (鳳凰單叢, Phoenix Single Bush) oolongs are grown on the slopes of Phoenix Mountain (Fenghuang Shan) in Chaozhou, Guangdong — ancient tea trees cultivated individually, each producing its own distinctive aromatic profile. The Mi Lan Xiang (蜜蘭香, Honey Orchid Fragrance) is the most beloved and widely recognised type: an unmistakable combination of tropical honey and fresh orchid that develops from the specific aromatic compounds produced by these mountain trees. Each tree is harvested separately (dancong = single-bush), ensuring flavour consistency. An extraordinary demonstration of terroir as individual genetic expression.',
 'reserve', 'ultra_premium',
 ARRAY['tropical honey', 'fresh orchid', 'ripe lychee', 'apricot jam', 'spiced honey', 'roasted finish', 'lingering floral sweetness'],
 '{"style": "dancong oolong (medium-heavy oxidised, lightly roasted)", "origin": "Phoenix Mountain (Fenghuang Shan), Chaozhou, Guangdong", "tree_type": "single ancient bush (dancong)", "aromatic_type": "Mi Lan Xiang (Honey Orchid)", "oxidation_pct": 50, "character": "intense floral-honey, no bitterness"}',
 '{"brew_temp_c": 95, "steep_time_first": "15-20 seconds", "vessel": "small zisha or porcelain gaiwan (80-100ml)", "leaf_to_water_ratio": "8-9g per 100ml", "infusions": "8-12", "notes": "use very high leaf-to-water ratio; flash infusions only; dancong opens exponentially after 3rd infusion"}',
 '{"cultivar": "Mi Lan Xiang phoenix mountain variety", "tree_age": "old bush (50+ years)", "roast": "light-medium charcoal", "oxidation": "medium-heavy", "origin": "Fenghuang Shan, Chaozhou"}',
 true),

('Phoenix Village Ya Shi Xiang (Duck Shit) Dancong', 'tea', 'oolong_dancong', 132, 60, 'China',
 'Ya Shi Xiang (鴨屎香, Duck Shit Fragrance) is Fenghuang Dancong''s most memorably named variety — a name reportedly invented by a farmer to discourage theft of his prized trees by making them sound undesirable. The tea itself is entirely unlike its name: a fragrance profile of exotic flowers, fresh gardenia, and spiced lychee with a distinctive cool menthol finish. In recent years Ya Shi Xiang has become the most internationally sought-after Dancong type, prized by tea collectors for its unusual combination of floral intensity and mineral freshness.',
 'reserve', 'ultra_premium',
 ARRAY['gardenia', 'fresh lychee', 'spiced orchid', 'cool menthol', 'tropical flower', 'mineral', 'long clean finish'],
 '{"style": "dancong oolong", "origin": "Phoenix Mountain, Chaozhou, Guangdong", "aromatic_type": "Ya Shi Xiang (Duck Shit Fragrance)", "oxidation_pct": 45, "character": "floral, exotic, cool menthol finish"}',
 '{"brew_temp_c": 95, "steep_time_first": "15 seconds", "vessel": "small gaiwan 80-100ml", "leaf_to_water_ratio": "8-9g per 100ml", "infusions": "10-15"}',
 '{"cultivar": "Ya Shi Xiang", "tree_age": "old bush 50+ years", "roast": "light-medium", "oxidation": "medium"}',
 true),

('Phoenix Village Xing Ren Xiang (Almond Orchid) Dancong', 'tea', 'oolong_dancong', 132, 60, 'China',
 'Xing Ren Xiang (杏仁香, Almond Fragrance) is one of the ten classic aromatic types of Fenghuang Dancong, producing a warm, nutty-floral character distinct from the honey-orchid types. The almond note is intrinsic to the specific genetic lineage of these Phoenix Mountain trees, not a processing artefact. A deeper, warmer, and slightly more accessible Dancong type than Ya Shi Xiang — excellent for introduction to the Dancong category, particularly for guests whose palate is calibrated to nut-forward wine (aged Burgundy, Vin Jaune) or aged spirits.',
 'estate', 'premium',
 ARRAY['almond blossom', 'warm orchid', 'marzipan', 'spiced honey', 'roasted nut', 'dried apricot', 'mineral finish'],
 '{"style": "dancong oolong", "origin": "Phoenix Mountain, Chaozhou, Guangdong", "aromatic_type": "Xing Ren Xiang (Almond Fragrance)", "oxidation_pct": 45, "character": "warm, nutty-floral, spiced honey"}',
 '{"brew_temp_c": 95, "steep_time_first": "20 seconds", "vessel": "small gaiwan or zisha 100ml", "leaf_to_water_ratio": "8g per 100ml", "infusions": "8-10"}',
 '{"cultivar": "Xing Ren Xiang", "roast": "medium charcoal", "oxidation": "medium"}',
 true),

('Floating Leaves Tea Fenghuang Old Bush Dancong Selection', 'tea', 'oolong_dancong', 133, 60, 'China',
 'Floating Leaves Tea (Seattle, Washington) is one of the Pacific Northwest''s most respected tea retailers, founded by Shiuwen Tai with a focus on Taiwanese and Chinese oolongs sourced directly from small producers. This Old Bush Dancong selection represents Floating Leaves'' curated approach: high-elevation Phoenix Mountain trees of 50–80 years, selected for aromatic complexity over volume. For a PNW restaurant programme, Floating Leaves offers the advantage of local relationships, direct sourcing knowledge, and BC/WA availability — an ideal supplier for a serious tea programme.',
 'estate', 'premium',
 ARRAY['tropical flowers', 'ripe peach', 'warm honey', 'light roast', 'mineral stone', 'lingering sweetness'],
 '{"style": "curated dancong oolong selection", "origin": "Phoenix Mountain, Chaozhou, Guangdong", "sourcing": "direct from small producers via Floating Leaves Tea (Seattle)", "tree_age": "old bush 50-80 years", "character": "complex aromatic, floral-fruity-mineral"}',
 '{"brew_temp_c": 95, "steep_time_first": "15-20 seconds", "vessel": "small gaiwan 100ml", "leaf_to_water_ratio": "8g per 100ml", "infusions": "8-12"}',
 '{"supplier_region": "Seattle WA; ships to BC Canada", "sourcing": "direct producer", "selection": "curated seasonal"}',
 true);

-- ============================================================
-- RISHI TEA (national US/CA importer) across multiple regions
-- Producer: Rishi Tea & Botanicals=134
-- ============================================================
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_markers,
   deductive_profile, service_specs, technical_specs, is_published)
VALUES

('Rishi Tea Pu-erh Dante Pu-erh Blend', 'tea', 'puerh_shou', 134, 57, 'China',
 'Rishi Tea & Botanicals (Milwaukee/Portland) is the largest certified organic tea importer in North America and a leading B Corp in the specialty tea industry. The Pu-erh Dante is their flagship ripe pu-erh blend — a consistent, approachable entry point to pu-erh for North American restaurant programmes. Made from a blend of shou pu-erh from multiple Yunnan gardens, it delivers the characteristic earthiness and smooth body of ripe pu-erh in a format designed for commercial hospitality use. Widely available through Sysco, PFG, and directly — the most accessible serious pu-erh for a BC restaurant.',
 'market', 'mid_range',
 ARRAY['earth', 'dark chocolate', 'aged wood', 'mushroom', 'smooth tannin', 'mild finish'],
 '{"style": "ripe shou pu-erh blend", "producer": "Rishi Tea & Botanicals", "origin": "Yunnan blend", "availability": "Sysco, PFG distribution; widely available in BC and WA"}',
 '{"brew_temp_c": 95, "steep_time_first": "30 seconds", "vessel": "teapot or gaiwan", "leaf_to_water_ratio": "5-6g per 150ml", "infusions": 5}',
 '{"blend": true, "sourcing": "multiple Yunnan gardens, certified organic", "format": "loose leaf and teabag options"}',
 true),

('Rishi Tea Organic Dragon Well (Longjing) Zhejiang', 'tea', 'green_tea_china', 134, 59, 'China',
 'Rishi Tea''s Organic Dragon Well is sourced from certified organic farms in Zhejiang province — not within the West Lake protected zone, but from high-quality Zhejiang longjing-style production that delivers the characteristic pan-fired chestnut and butter profile at an accessible price point appropriate for by-the-cup restaurant service. For a BC restaurant programme, this represents the practical entry into Chinese green tea: certified organic, available through major distributors, and produced with the same pan-firing method as authentic West Lake longjing.',
 'market', 'mid_range',
 ARRAY['pan-roasted chestnut', 'butter', 'fresh grass', 'clean vegetable', 'mild tannin'],
 '{"style": "pan-fired green tea (longjing style)", "origin": "Zhejiang province (not West Lake protected zone)", "certification": "certified organic", "availability": "Sysco, PFG; BC and WA distribution"}',
 '{"brew_temp_c": 75, "steep_time_first": "90 seconds", "vessel": "glass or gaiwan", "leaf_to_water_ratio": "3g per 150ml", "infusions": 3}',
 '{"certification": "USDA organic", "style": "longjing pan-fired", "format": "loose leaf"}',
 true),

('Rishi Tea Organic Wuyi Black (Lapsang Souchong)', 'tea', 'black_tea', 134, 58, 'China',
 'Lapsang Souchong (正山小種) is the world''s first black tea, originating in the Wuyi Mountains of Fujian in the 17th century. The traditional version is dried over pine wood fires, producing the characteristic smoky, resinous, camphor character that defined the European market for China tea through the 18th century. Rishi''s Organic Wuyi Black uses a lightly smoked version that preserves the pine-smoke character without overwhelming it — an ideal entry for guests new to smoked tea, and a compelling beverage pairing with smoked charcuterie, aged cheeses, and cold-weather dishes.',
 'market', 'mid_range',
 ARRAY['pine smoke', 'camphor', 'dried longan', 'caramel', 'earth', 'light tannin', 'warming finish'],
 '{"style": "lapsang souchong (pine-smoked black tea)", "origin": "Wuyi Mountains, Fujian", "smoke_level": "medium (lightly smoked)", "character": "pine smoke, dried fruit, warming"}',
 '{"brew_temp_c": 90, "steep_time_first": "2 minutes", "vessel": "teapot", "leaf_to_water_ratio": "3-4g per 150ml", "infusions": 3, "food_pairing": "smoked meats, aged cheese, pâté"}',
 '{"certification": "certified organic", "smoking_method": "pine wood", "origin": "Wuyi Tongmuguan"}',
 true);

COMMIT;
