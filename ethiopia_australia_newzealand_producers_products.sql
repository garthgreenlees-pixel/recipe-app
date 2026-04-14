BEGIN;

-- ============================================================
-- ETHIOPIA COFFEE: Yirgacheffe (77), Sidama (78), Harrar (79)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Yirgacheffe Coffee Farmers Cooperative Union', 'coffee_estate', 77, 'Ethiopia',
   'Multi-award-winning cooperative uniting smallholder farmers across the Yirgacheffe zone; rigorous wet-processing and shade-grown cultivation elevating Ethiopian specialty coffee globally.',
   'reserve', 'ultra_premium', 1, true),
  ('Konga Washing Station — Yirgacheffe', 'coffee_estate', 77, 'Ethiopia',
   'Renowned single-village washing station in the Konga kebele producing florally intense washed and natural lots; meticulous cherry selection and raised-bed drying define the house style.',
   'reserve', 'ultra_premium', 1, true),
  ('Worka Cooperative Washing Station', 'coffee_estate', 78, 'Ethiopia',
   'Premier Sidama cooperative washing station operating at 1900–2200m; produces vibrant washed coffees with trademark red-berry brightness and clean stone-fruit finish.',
   'estate', 'premium', 1, true),
  ('Bensa Bore Natural Processing Station', 'coffee_estate', 78, 'Ethiopia',
   'High-altitude Sidama estate specialising in natural and honey-process lots; slow cherry fermentation at 2000m+ yields deep dried-fruit complexity with rare florality.',
   'estate', 'premium', 1, true),
  ('Adinew Eshete Harrar Dry-Process Estate', 'coffee_estate', 79, 'Ethiopia',
   'Family-owned highland farm in the Harrar region practising traditional sun-drying on raised beds; wild-fermented naturals with wine-like blueberry and dark-chocolate character.',
   'estate', 'premium', 2, true),
  ('Harrar Farmers Cooperative Union', 'coffee_estate', 79, 'Ethiopia',
   'Umbrella cooperative aggregating Harrar dry-process lots from 65,000+ smallholders; champions the ancient heirloom Longberry and Shortberry cultivars at altitude.',
   'estate', 'premium', 2, true);

-- Yirgacheffe products
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Yirgacheffe YCFCU Grade 1 Washed',
  'coffee', 'washed_single_origin',
  77,
  (SELECT id FROM beverage_producers WHERE name = 'Yirgacheffe Coffee Farmers Cooperative Union'),
  'The benchmark Yirgacheffe washed; jasmine and bergamot florality over lemon verbena acidity with a silky body and clean white-tea finish. Grown at 1750–2200m across cooperative plots.',
  ARRAY['jasmine', 'bergamot', 'lemon verbena', 'white peach', 'clean tea finish'],
  'light',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Konga Natural Process Yirgacheffe',
  'coffee', 'natural_single_origin',
  77,
  (SELECT id FROM beverage_producers WHERE name = 'Konga Washing Station — Yirgacheffe'),
  'Natural-process Konga with extraordinary blueberry and rose-water intensity; syrupy body with hibiscus-tea acidity and a long winey finish. Very limited annual lot from the Konga kebele.',
  ARRAY['blueberry jam', 'rose water', 'hibiscus', 'dark plum', 'winey finish'],
  'medium',
  'reserve', 'ultra_premium', true;

-- Sidama products
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Worka Sidama Washed Grade 1',
  'coffee', 'washed_single_origin',
  78,
  (SELECT id FROM beverage_producers WHERE name = 'Worka Cooperative Washing Station'),
  'Flagship Sidama washed from the Worka cooperative; red currant and nectarine brightness over a sweet-cream body with a clean citrus-peel finish. Exceptional consistency across harvests.',
  ARRAY['red currant', 'nectarine', 'sweet cream', 'orange peel', 'brown sugar'],
  'light',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Bensa Bore Honey Process Sidama',
  'coffee', 'natural_single_origin',
  78,
  (SELECT id FROM beverage_producers WHERE name = 'Bensa Bore Natural Processing Station'),
  'Honey-process Sidama from Bensa Bore at 2100m; strawberry and dried apricot sweetness with cacao-nib depth and a lingering maple finish. One of Ethiopia''s most complex naturals.',
  ARRAY['strawberry', 'dried apricot', 'cacao nib', 'maple', 'tropical floral'],
  'medium',
  'estate', 'premium', true;

-- Harrar products
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Harrar Longberry Sun-Dried Natural',
  'coffee', 'natural_single_origin',
  79,
  (SELECT id FROM beverage_producers WHERE name = 'Adinew Eshete Harrar Dry-Process Estate'),
  'Wild-fermented Harrar Longberry dried on raised beds; intense blueberry wine, dark chocolate and tobacco complexity with a port-like finish. The archetype of Eastern Ethiopian coffee.',
  ARRAY['blueberry wine', 'dark chocolate', 'tobacco', 'port', 'earthy spice'],
  'full',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Harrar HFCU Cooperative Grade 1 Natural',
  'coffee', 'natural_single_origin',
  79,
  (SELECT id FROM beverage_producers WHERE name = 'Harrar Farmers Cooperative Union'),
  'Classic Harrar cooperative natural; dried cherry, mocha and black cardamom aromatics with full body and a sweet spice finish. Represents the traditional dry-process Harrar profile at scale.',
  ARRAY['dried cherry', 'mocha', 'black cardamom', 'molasses', 'spiced dark fruit'],
  'full',
  'estate', 'premium', true;

-- ============================================================
-- AUSTRALIA: McLaren Vale (85), Yarra Valley (86)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('d''Arenberg Wines', 'winery', 85, 'Australia',
   'Chester Osborn''s iconoclast McLaren Vale estate; biodynamic viticulture across 450ha of old-vine Shiraz, Grenache and Mourvèdre producing Australia''s most collectible Rhône-inspired blends.',
   'reserve', 'ultra_premium', 1, true),
  ('Clarendon Hills', 'winery', 85, 'Australia',
   'Roman Bratasiuk''s micro-estate sourcing from century-old dry-grown vines across McLaren Vale sub-zones; hand-harvested, minimal-intervention wines of extraordinary concentration.',
   'reserve', 'ultra_premium', 1, true),
  ('Yering Station', 'winery', 86, 'Australia',
   'Historic Yarra Valley estate established 1838; benchmark cool-climate Pinot Noir and Chardonnay from lower Yarra with characteristic restraint, forest spice and Burgundian precision.',
   'estate', 'premium', 2, true),
  ('Coldstream Hills', 'winery', 86, 'Australia',
   'James Halliday''s original Yarra Valley estate; pioneering cool-climate Pinot Noir and Chardonnay demonstrating the Yarra''s Burgundian potential since 1985.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'd''Arenberg The Dead Arm Shiraz',
  'wine_still', 'red_shiraz',
  85,
  (SELECT id FROM beverage_producers WHERE name = 'd''Arenberg Wines'),
  'Iconic McLaren Vale Shiraz from century-old dry-grown vines; liqueur plum, dark chocolate and anise concentration with supple tannins and a 20-year ageing trajectory. A national benchmark.',
  ARRAY['liqueur plum', 'dark chocolate', 'anise', 'mocha', 'graphite'],
  'full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Clarendon Hills Astralis Shiraz',
  'wine_still', 'red_shiraz',
  85,
  (SELECT id FROM beverage_producers WHERE name = 'Clarendon Hills'),
  'Australia''s most celebrated single-vineyard Shiraz; 80-year-old Clarendon vines yielding extraordinary concentration of black fruit, violet, pepper and iron-rich earth. Age 10–30 years.',
  ARRAY['black olive', 'blackberry', 'violet', 'white pepper', 'iron', 'smoked meat'],
  'full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Yering Station Reserve Pinot Noir',
  'wine_still', 'red_pinot_noir',
  86,
  (SELECT id FROM beverage_producers WHERE name = 'Yering Station'),
  'Lower Yarra Valley reserve Pinot Noir; cherry-red fruits with silky spice, forest floor and a cool-climate savoury lift. Shows textbook Yarra restraint and elegance.',
  ARRAY['red cherry', 'forest floor', 'five-spice', 'rose hip', 'savoury mineral'],
  'medium',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Coldstream Hills Reserve Chardonnay',
  'wine_still', 'white_chardonnay',
  86,
  (SELECT id FROM beverage_producers WHERE name = 'Coldstream Hills'),
  'Halliday''s benchmark Yarra Valley Chardonnay; white peach and nectarine with toasted hazelnut, lemon curd and precise acidity. One of Australia''s finest cool-climate Chardonnays.',
  ARRAY['white peach', 'nectarine', 'hazelnut', 'lemon curd', 'creamy oak'],
  'medium-full',
  'estate', 'premium', true;

-- ============================================================
-- NEW ZEALAND: Hawke''s Bay (89)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Te Mata Estate', 'winery', 89, 'New Zealand',
   'New Zealand''s oldest winery (1895); Havelock North home to iconic Coleraine Bordeaux blend and Elston Chardonnay — the benchmark references for Hawke''s Bay fine wine at any price.',
   'reserve', 'ultra_premium', 1, true),
  ('Craggy Range Winery', 'winery', 89, 'New Zealand',
   'Terry Peabody''s benchmark Hawke''s Bay estate; Gimblett Gravels Syrah demonstrating New Zealand''s world-class red wine potential with northern Rhône inspiration.',
   'estate', 'premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Te Mata Coleraine',
  'wine_still', 'red_bordeaux_blend',
  89,
  (SELECT id FROM beverage_producers WHERE name = 'Te Mata Estate'),
  'New Zealand''s most celebrated red wine; Gimblett Gravels Cabernet Sauvignon/Merlot/Cabernet Franc blend of remarkable restraint, pencil shaving, cassis and cedar. Ages 15+ years.',
  ARRAY['cassis', 'pencil shaving', 'cedar', 'black plum', 'dried herb', 'mineral'],
  'medium-full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Craggy Range Le Sol Gimblett Gravels Syrah',
  'wine_still', 'red_syrah',
  89,
  (SELECT id FROM beverage_producers WHERE name = 'Craggy Range Winery'),
  'Flagship Hawke''s Bay Syrah from the Gimblett Gravels; northern Rhône in character with violet florality, smoked olive, pepper and exceptional length. The benchmark for NZ Syrah.',
  ARRAY['violet', 'smoked olive', 'white pepper', 'dark berry', 'iron', 'fine tannin'],
  'full',
  'estate', 'premium', true;

COMMIT;
