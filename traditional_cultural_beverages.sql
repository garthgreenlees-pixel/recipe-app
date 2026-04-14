BEGIN;

-- ============================================================
-- TRADITIONAL CULTURAL BEVERAGES
-- Vanuatu Kava (68), Hawaii Awa (70), Samoa Ava (71),
-- Philippines Lambanog (72), Philippines Basi (73),
-- Nigeria Palm Wine (74), Cameroon Matango (75)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Tanna Kava Growers Cooperative', 'multi_category', 68, 'Vanuatu',
   'Tanna Island''s premier kava growers collective; producing Noble kava from ancient Piper methysticum cultivars including Borogu and Melomelo — cultivated for ceremonial use and export of the world''s most potent kava varieties.',
   'estate', 'premium', 2, true),
  ('Nakamal at Home — Vanuatu Kava', 'multi_category', 68, 'Vanuatu',
   'The leading exporter of traditional Vanuatu Noble kava; sourcing exclusively from small-island farms on Tanna, Santo and Pentecost where kava preparation follows ancient ceremonial methodology.',
   'reserve', 'ultra_premium', 1, true),
  ('Lehua Hawaiian Kava — Oahu', 'multi_category', 70, 'USA',
   'Oahu-based cultivator and preparer of traditional Hawaiian awa (kava) from the Mahakea, Hiwa and Nene cultivars. The most respected source of traditional Hawaiian awa prepared in the ancestral stone-ground method.',
   'estate', 'premium', 2, true),
  ('Samoa Traditional Kava Preparation', 'multi_category', 71, 'Samoa',
   'Traditional Samoan ava ceremony preparation from fa''afia kava roots; the formal ava ceremony remains central to Samoan chiefly culture and diplomatic reception with a complex social protocol.',
   'estate', 'premium', 3, true),
  ('Barako Lambanog Distillery — Quezon', 'distillery', 72, 'Philippines',
   'Quezon Province''s premier lambanog distillery; triple-distilled coconut palm wine spirit from the nipa palm, aged in clay pots. The Philippines'' oldest indigenous distilled spirit with a tradition of centuries.',
   'estate', 'premium', 3, true),
  ('Felicitas Winery — Ilocos Basi', 'multi_category', 73, 'Philippines',
   'Ilocos Region''s benchmark producer of Basi — fermented sugarcane wine with bark and herb additions. The Ilocano tradition of Basi-making goes back to pre-colonial times and is listed as a UNESCO intangible heritage practice.',
   'estate', 'premium', 3, true),
  ('Cross-River Palm Wine Tappers Collective', 'multi_category', 74, 'Nigeria',
   'Cross-River State''s premier palm wine collective; fresh-tapped Raphia palm wine (Emu) from old-growth forest palms, consumed within 24 hours of tapping for maximum effervescence and natural yeast complexity.',
   'estate', 'premium', 2, true),
  ('Bafoussam Matango Cooperative — Cameroon', 'multi_category', 75, 'Cameroon',
   'West Region Cameroon''s premier Matango (banana wine) producer; traditional fermented banana wine from the Bamileke highlands, prepared from over-ripe Pisang Mas bananas with a lightly carbonated, sweet-sour character.',
   'estate', 'premium', 3, true);

-- Vanuatu Kava product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Tanna Noble Kava Borogu',
  'traditional_cultural', 'kava_noble',
  68, (SELECT id FROM beverage_producers WHERE name = 'Tanna Kava Growers Cooperative' LIMIT 1),
  'Noble kava from Tanna Island''s Borogu cultivar; the most potent and revered of Vanuatu''s ceremonial kava varieties. Earthy, slightly bitter and peppery with a numbing sensation. Consumed in shells at dusk in the nakamal.',
  ARRAY['earthy', 'pepper', 'mild bitter', 'nutty', 'numbing', 'clay-mineral'],
  'medium', 'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Vanuatu Noble Kava Export — Nakamal',
  'traditional_cultural', 'kava_powder',
  68, (SELECT id FROM beverage_producers WHERE name = 'Nakamal at Home — Vanuatu Kava' LIMIT 1),
  'Micro-ground Noble kava from Santo and Tanna island farms; peppery-earthy with mild sweet undertone and a distinct numbing kavalactone effect. The most consistent export-quality Vanuatu kava available internationally.',
  ARRAY['pepper', 'earth', 'mild sweet', 'nutty undertone', 'kavalactone warmth'],
  'medium', 'reserve', 'ultra_premium', true;

-- Hawaii Awa product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Lehua Hawaiian Awa — Mahakea Cultivar',
  'traditional_cultural', 'kava_awa_hawaiian',
  70, (SELECT id FROM beverage_producers WHERE name = 'Lehua Hawaiian Kava — Oahu' LIMIT 1),
  'Traditional Hawaiian awa prepared from the prized Mahakea cultivar; milder and more floral than Vanuatu kava with a gentle numbing effect, earthy sweetness and subtle floral notes. Central to Hawaiian ceremony and healing tradition.',
  ARRAY['earthy sweet', 'light floral', 'mild numbing', 'nutty', 'gentle pepper', 'clean finish'],
  'light', 'estate', 'premium', true;

-- Samoa Ava product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Samoan Ava Ceremony Preparation',
  'traditional_cultural', 'kava_ava_ceremony',
  71, (SELECT id FROM beverage_producers WHERE name = 'Samoa Traditional Kava Preparation' LIMIT 1),
  'Traditional Samoan ava prepared in the tanoa (ceremonial bowl); strained through the fau bark filter with precise water ratio. Mild, slightly sour-earthy with a cooling numbing sensation. Fundamental to Samoan fa''asamoa (custom).',
  ARRAY['mild earthy', 'slightly sour', 'cooling', 'light pepper', 'fresh root', 'clean'],
  'light', 'estate', 'premium', true;

-- Philippines Lambanog product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Barako Lambanog Triple-Distilled',
  'traditional_cultural', 'lambanog_coconut_spirit',
  72, (SELECT id FROM beverage_producers WHERE name = 'Barako Lambanog Distillery — Quezon' LIMIT 1),
  'Triple-distilled nipa palm spirit from Quezon Province; clear, 40-45% ABV with fresh coconut, slight sweetness, clean botanical notes and a warming finish. The Philippines'' ancestral distillate, centuries older than European spirits trade.',
  ARRAY['fresh coconut', 'light sweetness', 'clean floral', 'botanical warmth', 'white rum adjacent'],
  'medium', 'estate', 'premium', true;

-- Philippines Basi product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Ilocos Region Basi — Traditional Fermented Sugarcane',
  'traditional_cultural', 'basi_sugarcane_wine',
  73, (SELECT id FROM beverage_producers WHERE name = 'Felicitas Winery — Ilocos Basi' LIMIT 1),
  'Traditional Ilocano Basi; fermented sugarcane wine with Duhat (java plum) bark and native herb additions. Medium-bodied, deep garnet, with dried fig, bark tannin, brown sugar and a complex bitter-sweet finish. Pre-colonial in heritage.',
  ARRAY['dried fig', 'bark tannin', 'brown sugar', 'tamarind', 'dark fruit', 'herbal bitter'],
  'medium', 'estate', 'premium', true;

-- Nigeria Palm Wine product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Cross-River Raphia Palm Wine (Emu)',
  'traditional_cultural', 'palm_wine_fresh',
  74, (SELECT id FROM beverage_producers WHERE name = 'Cross-River Palm Wine Tappers Collective' LIMIT 1),
  'Fresh-tapped Raphia palm wine from Cross-River State; consumed within hours of harvest for maximum natural carbonation and sweetness. Lightly effervescent, mildly alcoholic with coconut sap sweetness, tropical yeast and a slightly vinous finish as fermentation progresses.',
  ARRAY['coconut sap', 'natural effervescence', 'tropical yeast', 'sweet-sour', 'mild ferment', 'fresh fruit'],
  'light', 'estate', 'premium', true;

-- Cameroon Matango product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Bafoussam Matango — Fermented Banana Wine',
  'traditional_cultural', 'matango_banana_wine',
  75, (SELECT id FROM beverage_producers WHERE name = 'Bafoussam Matango Cooperative — Cameroon' LIMIT 1),
  'Traditional Bamileke fermented banana wine from West Cameroon; made from over-ripe Pisang Mas bananas with natural yeast fermentation. Lightly carbonated, amber, with ripe banana, caramelised sugar, mild tartness and a clean dry finish.',
  ARRAY['ripe banana', 'caramelised sugar', 'mild tartness', 'light carbonation', 'tropical fruit', 'clean finish'],
  'medium', 'estate', 'premium', true;

COMMIT;
