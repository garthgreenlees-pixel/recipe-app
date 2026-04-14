BEGIN;

-- ============================================================
-- BC CANADA: Gulf Islands (5), Lillooet (6), Shuswap (7),
-- Thompson Valley (8), Skaha Bench (11), Summerland (14)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Garry Oaks Winery', 'winery', 5, 'Canada',
   'Salt Spring Island Gulf Islands estate; BC''s most expressive island winery, farming biodynamically on volcanic basalt soils. Gewurztraminer, Pinot Gris and Zweigelt that reflect the Gulf Islands'' distinct microclimate.',
   'estate', 'premium', 2, true),
  ('Fort Berens Estate Winery', 'winery', 6, 'Canada',
   'Lillooet''s pioneering estate winery in BC''s driest wine region; leveraging the Fraser Canyon''s extreme continental climate to produce intense Riesling and Cabernet Franc from ancient river terraces.',
   'estate', 'premium', 2, true),
  ('Recline Ridge Vineyards & Winery', 'winery', 7, 'Canada',
   'BC''s most northerly estate winery in the Shuswap; cool-climate viticulture at 550m producing Maréchal Foch, Bacchus and Ortega varieties suited to the region''s short, intense growing season.',
   'estate', 'premium', 3, true),
  ('Hillside Winery', 'winery', 8, 'Canada',
   'Penticton''s Thompson Valley estate known for pioneering Muscat and Cabernet Franc; Hillside''s terraced vineyards on south-facing slopes produce concentrated, food-friendly wines at accessible price points.',
   'estate', 'premium', 2, true),
  ('Moon Curser Vineyards', 'winery', 11, 'Canada',
   'Osoyoos Skaha Bench estate producing BC''s most singular red varietals: Tannat, Arneis and the rare Touriga Nacional. The most experimental and varietally diverse winery on the Skaha Bench sub-AVA.',
   'estate', 'premium', 2, true),
  ('Thornhaven Estates Winery', 'winery', 14, 'Canada',
   'Summerland estate on the west bench of Okanagan Lake; benchmark Gewurztraminer and Pinot Noir from this historic Okanagan sub-region with established vineyards and a distinctly cooler lake influence.',
   'estate', 'premium', 2, true);

-- Gulf Islands product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Garry Oaks Gewurztraminer',
  'wine_still', 'white_gewurztraminer',
  5, (SELECT id FROM beverage_producers WHERE name = 'Garry Oaks Winery' LIMIT 1),
  'Gulf Islands Gewurztraminer from volcanic basalt soils on Salt Spring Island; lychee, rose petal, ginger and a clean mineral finish. BC''s most distinctly island-terroir Gewurz.',
  ARRAY['lychee', 'rose petal', 'ginger', 'litchi', 'floral spice', 'clean mineral'],
  'medium', 'estate', 'premium', true;

-- Lillooet product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Fort Berens Riesling',
  'wine_still', 'white_riesling',
  6, (SELECT id FROM beverage_producers WHERE name = 'Fort Berens Estate Winery' LIMIT 1),
  'Lillooet Riesling from the Fraser Canyon''s driest corridor; off-dry style with petrol, lime zest, white peach and a stony mineral finish. Among BC''s most distinctive high-desert Rieslings.',
  ARRAY['petrol', 'lime zest', 'white peach', 'stony mineral', 'honey', 'crisp acidity'],
  'light', 'estate', 'premium', true;

-- Shuswap product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Recline Ridge Bacchus',
  'wine_still', 'white_bacchus',
  7, (SELECT id FROM beverage_producers WHERE name = 'Recline Ridge Vineyards & Winery' LIMIT 1),
  'Shuswap Bacchus — a German Müller-Thurgau hybrid well-suited to BC''s northern cool-climate zones; peach blossom, apricot and gentle Muscat-like spice. Light and immediately appealing.',
  ARRAY['peach blossom', 'apricot', 'muscat spice', 'green apple', 'light floral'],
  'light', 'estate', 'premium', true;

-- Thompson Valley product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Hillside Estate Muscat Ottonel',
  'wine_still', 'white_muscat',
  8, (SELECT id FROM beverage_producers WHERE name = 'Hillside Winery' LIMIT 1),
  'Thompson Valley Muscat Ottonel; intensely aromatic with orange blossom, apricot and floral spice in a dry, mineral-driven style. One of BC''s best expressions of the perfumed Alsatian grape.',
  ARRAY['orange blossom', 'apricot', 'floral spice', 'citrus', 'dry mineral'],
  'light', 'estate', 'premium', true;

-- Skaha Bench product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Moon Curser Tannat',
  'wine_still', 'red_tannat',
  11, (SELECT id FROM beverage_producers WHERE name = 'Moon Curser Vineyards' LIMIT 1),
  'BC''s benchmark Tannat from the Skaha Bench; adapted from Madiran, the Osoyoos heat produces an unusually approachable Tannat with dark cherry, leather and iron without the austere tannin of its French archetype.',
  ARRAY['dark cherry', 'leather', 'iron', 'dark plum', 'tobacco', 'firm tannin'],
  'full', 'estate', 'premium', true;

-- Summerland product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Thornhaven Gewurztraminer',
  'wine_still', 'white_gewurztraminer',
  14, (SELECT id FROM beverage_producers WHERE name = 'Thornhaven Estates Winery' LIMIT 1),
  'Summerland Gewurztraminer from the lake-cooled west bench; rose petal, lychee and grapefruit with a drier, more mineral style than Okanagan valley-floor expressions.',
  ARRAY['rose petal', 'lychee', 'grapefruit', 'dry mineral', 'gentle spice'],
  'light', 'estate', 'premium', true;

-- ============================================================
-- WASHINGTON STATE SUB-AVAs:
-- Rattlesnake Hills (24), Wahluke Slope (25), Ancient Lakes (26),
-- Lake Chelan (27), Naches Heights (28), Snipes Mountain (29)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Wilridge Winery — Rattlesnake Hills', 'winery', 24, 'USA',
   'Paul Beveridge''s Rattlesnake Hills estate on Yakima''s south-facing slopes; estate-grown Syrah and Cabernet Sauvignon from the AVA''s volcanic basalt and loess soils — some of Washington''s most complex reds.',
   'estate', 'premium', 2, true),
  ('Destiny Ridge Vineyard — Wahluke Slope', 'winery', 25, 'USA',
   'The Wahluke Slope''s premier estate vineyard at 800-1200m with Cabernet Sauvignon and Syrah from gravelly loam; exceptional growing conditions with 300+ sunshine days making this Columbia Basin''s hottest AVA.',
   'estate', 'premium', 2, true),
  ('Ancient Lakes Vineyard — Cave B', 'winery', 26, 'USA',
   'Ste. Michelle Wine Estates'' vineyards in the Ancient Lakes of Columbia Valley AVA; the area''s unique wind pattern and sandy soils produce particularly aromatic Riesling and Gewurztraminer at commercial scale.',
   'estate', 'premium', 2, true),
  ('Fielding Hills Winery — Lake Chelan', 'winery', 27, 'USA',
   'Lake Chelan''s premier estate on the rocky east side of the glacial lake; the thermal regulation of Chelan''s deep water creates uniquely cool-climate conditions for elegant Syrah and Cabernet Franc.',
   'estate', 'premium', 2, true),
  ('Natapat Cellars — Naches Heights', 'winery', 28, 'USA',
   'High-elevation Naches Heights estate at 1100-1400m on ancient lava flows; Washington''s newest and highest-elevation AVA with cooling afternoon winds producing structured Cabernet Franc and Tempranillo.',
   'estate', 'premium', 2, true),
  ('Snipes Family Winery', 'winery', 29, 'USA',
   'The Snipes Mountain AVA''s eponymous estate winery on Washington''s oldest continually-farmed vineyard (1917); old-vine Grenache, Syrah and Mourvèdre from Yakima Valley''s volcanic ridgeline soils.',
   'estate', 'premium', 2, true);

-- Rattlesnake Hills product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Wilridge Rattlesnake Hills Syrah',
  'wine_still', 'red_syrah',
  24, (SELECT id FROM beverage_producers WHERE name = 'Wilridge Winery — Rattlesnake Hills' LIMIT 1),
  'Rattlesnake Hills Syrah from volcanic basalt and loess; darker and more structured than Walla Walla Syrah, with iron, dark berry, olive tapenade and a peppery finish. One of Washington''s more mineral Syrahs.',
  ARRAY['iron', 'dark berry', 'olive tapenade', 'white pepper', 'dark cherry', 'smoked meat'],
  'full', 'estate', 'premium', true;

-- Wahluke Slope product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Destiny Ridge Wahluke Slope Cabernet Sauvignon',
  'wine_still', 'red_cabernet_sauvignon',
  25, (SELECT id FROM beverage_producers WHERE name = 'Destiny Ridge Vineyard — Wahluke Slope' LIMIT 1),
  'Washington''s warmest AVA Cabernet; ripe blackcurrant, cassis, dark chocolate and a long vanilla-cedar finish. Full-bodied, generous and consistently one of Columbia Basin''s richest Cabernets.',
  ARRAY['blackcurrant', 'cassis', 'dark chocolate', 'vanilla cedar', 'mocha', 'ripe plum'],
  'full', 'estate', 'premium', true;

-- Ancient Lakes product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Ancient Lakes of Columbia Valley Riesling',
  'wine_still', 'white_riesling',
  26, (SELECT id FROM beverage_producers WHERE name = 'Ancient Lakes Vineyard — Cave B' LIMIT 1),
  'Sandy-soil Ancient Lakes Riesling; off-dry, aromatic and precise with mandarin, lime zest, apricot and a stony mineral backbone. The unique sandy terroir produces an unusually delicate Washington Riesling.',
  ARRAY['mandarin', 'lime zest', 'apricot', 'stony mineral', 'honey', 'clean finish'],
  'light', 'estate', 'premium', true;

-- Lake Chelan product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Fielding Hills Lake Chelan Syrah',
  'wine_still', 'red_syrah',
  27, (SELECT id FROM beverage_producers WHERE name = 'Fielding Hills Winery — Lake Chelan' LIMIT 1),
  'Lake Chelan Syrah benefiting from the glacial lake''s thermal regulation; more elegant than Columbia Basin expressions with violet, smoked olive, red cherry and white pepper. Cool-climate precision.',
  ARRAY['violet', 'smoked olive', 'red cherry', 'white pepper', 'granite mineral', 'fine tannin'],
  'medium-full', 'estate', 'premium', true;

-- Naches Heights product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Naches Heights Cabernet Franc',
  'wine_still', 'red_cabernet_franc',
  28, (SELECT id FROM beverage_producers WHERE name = 'Natapat Cellars — Naches Heights' LIMIT 1),
  'High-altitude Naches Heights Cabernet Franc from ancient lava flows at 1200m; cassis, graphite, fresh herb and a silky mineral finish. Washington''s most Loire-like Cab Franc with genuine cool-climate tension.',
  ARRAY['cassis', 'graphite', 'fresh herb', 'red pepper', 'mineral', 'silk tannin'],
  'medium', 'estate', 'premium', true;

-- Snipes Mountain product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Snipes Family Winery Old Vine Grenache',
  'wine_still', 'red_grenache',
  29, (SELECT id FROM beverage_producers WHERE name = 'Snipes Family Winery' LIMIT 1),
  'Old-vine Grenache from Washington''s oldest continuously-farmed vineyard (1917 plantings) on Snipes Mountain; kirsch, garrigue, dried rose and a silky spiced finish. Remarkable purity from century-old vines.',
  ARRAY['kirsch', 'garrigue', 'dried rose', 'warm spice', 'silk texture', 'orange peel'],
  'medium', 'estate', 'premium', true;

-- ============================================================
-- OREGON SUB-AVAs:
-- Southern Oregon (32), McMinnville (37),
-- Van Duzer Corridor (39), Elkton Oregon (41),
-- Rogue Valley (42), Applegate Valley (43)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Ledger David Cellars — Southern Oregon', 'winery', 32, 'USA',
   'Southern Oregon''s Applegate Valley hybrid producer; estate-grown Bordeaux and Italian varieties benefiting from the region''s warmer, drier climate compared to the Willamette Valley.',
   'estate', 'premium', 2, true),
  ('Eyrie Vineyards — McMinnville', 'winery', 37, 'USA',
   'Oregon''s most historic winery, founded by David Lett in 1966; the McMinnville estate pioneering Pinot Noir and Pinot Gris in the New World. The Eyrie Original Vines Pinot Gris is the benchmark for this variety in Oregon.',
   'reserve', 'ultra_premium', 1, true),
  ('Cristom Vineyards — Van Duzer Corridor', 'winery', 39, 'USA',
   'Mark Feltz''s Van Duzer Corridor estate; the coastal wind gap''s powerful afternoon cooling creates unusually elegant, high-acid Pinot Noir with Burgundian restraint and exceptional ageing potential.',
   'estate', 'premium', 1, true),
  ('Bradley Vineyards — Elkton Oregon', 'winery', 41, 'USA',
   'Elkton Oregon''s coastal AVA pioneer; cool Umpqua Valley sub-region with maritime influence producing Pinot Gris and Tempranillo of unusual freshness and coastal mineral character.',
   'estate', 'premium', 3, true),
  ('Abacela Winery — Rogue Valley', 'winery', 42, 'USA',
   'Earl Jones'' Rogue Valley estate that pioneered Spanish varietals in Southern Oregon; Tempranillo and Malbec from the warm, dry Umpqua-Rogue intersection producing wines of remarkable Iberian character.',
   'estate', 'premium', 2, true),
  ('Cowhorn Vineyard — Applegate Valley', 'winery', 43, 'USA',
   'Bill and Barbara Steele''s biodynamic Applegate Valley estate; the warmest Oregon AVA with limestone terroir producing structured Rhône and Italian varieties at the southern frontier of Oregon wine.',
   'estate', 'premium', 2, true);

-- Southern Oregon product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Ledger David Southern Oregon Merlot',
  'wine_still', 'red_merlot',
  32, (SELECT id FROM beverage_producers WHERE name = 'Ledger David Cellars — Southern Oregon' LIMIT 1),
  'Southern Oregon Merlot benefiting from the warmer Siskiyou mountain climate; plum, mocha, cedar and a smooth mid-palate. Fuller and warmer than Willamette expressions — the accessible face of Oregon red wine.',
  ARRAY['plum', 'mocha', 'cedar', 'dark cherry', 'soft tannin', 'vanilla'],
  'medium-full', 'estate', 'premium', true;

-- McMinnville product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Eyrie Vineyards Original Vines Pinot Gris',
  'wine_still', 'white_pinot_gris',
  37, (SELECT id FROM beverage_producers WHERE name = 'Eyrie Vineyards — McMinnville' LIMIT 1),
  'The original Oregon Pinot Gris from 1966 plantings; melon, pear, creamy texture and a clean mineral finish with genuine depth from 50-year-old vines. The benchmark for Willamette Pinot Gris.',
  ARRAY['melon', 'pear', 'cream', 'mineral', 'citrus', 'toasted almond'],
  'medium', 'reserve', 'ultra_premium', true;

-- Van Duzer Corridor product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Cristom Mt. Jefferson Cuvée Pinot Noir',
  'wine_still', 'red_pinot_noir',
  39, (SELECT id FROM beverage_producers WHERE name = 'Cristom Vineyards — Van Duzer Corridor' LIMIT 1),
  'Cristom''s benchmark Pinot Noir from Van Duzer Corridor; coastal wind-gap cooling produces high-acid, elegant Pinot with red cherry, forest floor, spice and silky mineral tannin. Reliable, age-worthy Oregon.',
  ARRAY['red cherry', 'forest floor', 'spice', 'silk tannin', 'mineral', 'dried rose'],
  'medium', 'estate', 'premium', true;

-- Elkton Oregon product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Bradley Vineyards Elkton Pinot Gris',
  'wine_still', 'white_pinot_gris',
  41, (SELECT id FROM beverage_producers WHERE name = 'Bradley Vineyards — Elkton Oregon' LIMIT 1),
  'Coastal Elkton Oregon Pinot Gris with maritime mineral influence; pear, apple, mild citrus and a fresh mineral finish. Lighter and more coastal in character than Willamette Valley expressions.',
  ARRAY['pear', 'green apple', 'mild citrus', 'coastal mineral', 'white floral'],
  'light', 'estate', 'premium', true;

-- Rogue Valley product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Abacela Tempranillo Estate',
  'wine_still', 'red_tempranillo',
  42, (SELECT id FROM beverage_producers WHERE name = 'Abacela Winery — Rogue Valley' LIMIT 1),
  'Oregon''s most celebrated Tempranillo; Rogue Valley warmth produces dark cherry, leather, tobacco and dried herb in the Ribera del Duero idiom — remarkable for the Pacific Northwest.',
  ARRAY['dark cherry', 'leather', 'tobacco', 'dried herb', 'cedar', 'fine tannin'],
  'medium-full', 'estate', 'premium', true;

-- Applegate Valley product
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Cowhorn Spiral 36 Rhône Blend',
  'wine_still', 'red_grenache_syrah_blend',
  43, (SELECT id FROM beverage_producers WHERE name = 'Cowhorn Vineyard — Applegate Valley' LIMIT 1),
  'Biodynamic Applegate Valley Rhône blend; Grenache and Syrah from limestone soils with Provençal garrigue, kirsch and white pepper character. Oregon''s most convincing Rhône-style blend from the warm south.',
  ARRAY['kirsch', 'garrigue', 'white pepper', 'dark berry', 'warm spice', 'limestone mineral'],
  'medium-full', 'estate', 'premium', true;

COMMIT;
