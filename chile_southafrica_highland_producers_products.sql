BEGIN;

-- ============================================================
-- CHILE: Colchagua Valley (91), Maipo Valley (92)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Casa Lapostolle — Clos Apalta', 'winery', 91, 'Chile',
   'Alexandra Marnier-Lapostolle''s biodynamic Colchagua estate; Clos Apalta is a 30ha amphitheatre of 80-year-old Carmenère, Merlot and Cabernet Franc producing Chile''s most internationally celebrated red.',
   'reserve', 'ultra_premium', 1, true),
  ('Luis Felipe Edwards', 'winery', 91, 'Chile',
   'Large Colchagua family estate with a 150-year history; benchmark Gran Reserva tiers produced from old-vine Carmenère and Syrah in the warmer sub-zones of the Colchagua Valley.',
   'estate', 'premium', 2, true),
  ('Almaviva Winery', 'winery', 92, 'Chile',
   'Joint venture between Concha y Toro and Baron Philippe de Rothschild; Maipo Valley''s definitive Bordeaux-style blend combining Chilean terroir with Médoc winemaking philosophy and Rothschild rigour.',
   'reserve', 'ultra_premium', 1, true),
  ('Don Melchor Estate', 'winery', 92, 'Chile',
   'Concha y Toro''s flagship single-vineyard Cabernet from Puente Alto, Maipo; Chile''s most age-worthy red, blending Andean mineral freshness with deep Cabernet structure — produced since 1987.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Clos Apalta',
  'wine_still', 'red_carmenere_blend',
  91,
  (SELECT id FROM beverage_producers WHERE name = 'Casa Lapostolle — Clos Apalta' LIMIT 1),
  'Chile''s most critically acclaimed red; biodynamic Carmenère-dominant blend from 80-year-old vines in a 30ha amphitheatre. Black cherry, tobacco, mocha and graphite with a 15-20 year horizon.',
  ARRAY['black cherry', 'tobacco', 'mocha', 'graphite', 'dark chocolate', 'cedar'],
  'full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Luis Felipe Edwards Gran Reserva Carmenère',
  'wine_still', 'red_carmenere',
  91,
  (SELECT id FROM beverage_producers WHERE name = 'Luis Felipe Edwards' LIMIT 1),
  'Benchmark Gran Reserva Carmenère from the warm Colchagua Valley; ripe plum, cocoa and green pepper with medium tannin and approachable structure. The definitive everyday Colchagua Carmenère.',
  ARRAY['ripe plum', 'cocoa', 'green pepper', 'dark cherry', 'vanilla'],
  'medium-full',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Almaviva',
  'wine_still', 'red_bordeaux_blend',
  92,
  (SELECT id FROM beverage_producers WHERE name = 'Almaviva Winery' LIMIT 1),
  'Maipo Valley''s most prestigious Bordeaux blend; Cabernet Sauvignon-dominant with Carmenère, Cabernet Franc and Petit Verdot. Cassis, cedar, graphite and long mineral finish. Rothschild-Concha y Toro joint venture.',
  ARRAY['cassis', 'cedar', 'graphite', 'red plum', 'tobacco', 'mineral'],
  'full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Don Melchor Cabernet Sauvignon Puente Alto',
  'wine_still', 'red_cabernet_sauvignon',
  92,
  (SELECT id FROM beverage_producers WHERE name = 'Don Melchor Estate' LIMIT 1),
  'Chile''s benchmark single-vineyard Cabernet from Puente Alto at the Andes foothills; pencil shaving, blackcurrant, mint and fine mineral tannin. One of South America''s definitive ageworthy reds.',
  ARRAY['blackcurrant', 'pencil shaving', 'mint', 'cedar', 'fine mineral tannin'],
  'full',
  'reserve', 'ultra_premium', true;

-- ============================================================
-- SOUTH AFRICA: Stellenbosch (93)
-- Kanonkop Wine Estate already exists as ID 177 — DO NOT insert again
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Meerlust Estate', 'winery', 93, 'South Africa',
   'One of South Africa''s oldest wine estates (1693); Rubicon is Stellenbosch''s reference Bordeaux blend — five generations of the Myburgh family crafting wines of Médoc elegance and local character.',
   'reserve', 'ultra_premium', 1, true),
  ('Boekenhoutskloof Winery', 'winery', 93, 'South Africa',
   'Stellenbosch and Franschhoek multi-estate producer; Syrah and The Chocolate Block are signature wines combining old-vine intensity with precise winemaking and Cape''s finest new-wave red-wine ambition.',
   'estate', 'premium', 1, true);

-- Kanonkop Paul Sauer — using existing producer ID 177
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
VALUES (
  'Kanonkop Paul Sauer',
  'wine_still', 'red_bordeaux_blend',
  93,
  177,
  'South Africa''s most celebrated Bordeaux blend; Cabernet Sauvignon/Cabernet Franc/Merlot from Simonsberg-Stellenbosch. Cassis, cedar, dried tobacco and exceptional longevity. A Cape First Growth.',
  ARRAY['cassis', 'cedar', 'dried tobacco', 'dark plum', 'graphite', 'fine tannin'],
  'full',
  'reserve', 'ultra_premium', true
);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Meerlust Rubicon',
  'wine_still', 'red_bordeaux_blend',
  93,
  (SELECT id FROM beverage_producers WHERE name = 'Meerlust Estate' LIMIT 1),
  'South Africa''s original Bordeaux blend (1980 debut); Cabernet Sauvignon-dominant with Merlot and Cabernet Franc. Cassis, violet, cedar and 20+ year ageing potential from Helderberg granite.',
  ARRAY['cassis', 'violet', 'cedar', 'dark cherry', 'tobacco leaf', 'mineral'],
  'medium-full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Boekenhoutskloof Syrah',
  'wine_still', 'red_syrah',
  93,
  (SELECT id FROM beverage_producers WHERE name = 'Boekenhoutskloof Winery' LIMIT 1),
  'South Africa''s benchmark Syrah; northern Rhône-inspired with violet, smoked meat, white pepper and dark berry concentration. Shows the Cape''s world-class potential with old-vine intensity.',
  ARRAY['violet', 'smoked meat', 'white pepper', 'dark berry', 'iron', 'olive'],
  'full',
  'estate', 'premium', true;

-- ============================================================
-- SCOTLAND: Highland (97)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Dalmore Distillery', 'distillery', 97, 'Scotland',
   'Alness, Ross-shire Highland distillery established 1839; signature sherry-maturation in Oloroso and González Byass casks producing rich, chocolatey whisky with citrus marmalade and walnut character.',
   'estate', 'premium', 2, true),
  ('Glenmorangie Distillery', 'distillery', 97, 'Scotland',
   'Tain, Ross-shire distillery with the tallest stills in Scotland; pioneering extra-maturation techniques including Burgundy, Sauternes and Madeira cask finishing producing exceptionally delicate, floral Highland malts.',
   'reserve', 'ultra_premium', 1, true),
  ('GlenDronach Distillery', 'distillery', 97, 'Scotland',
   'Aberdeenshire Highland distillery established 1826; exclusively sherry-matured in Oloroso and Pedro Ximénez casks producing richly spiced, fruit-cake Highland malts of extraordinary depth.',
   'estate', 'premium', 2, true),
  ('Clynelish Distillery', 'distillery', 97, 'Scotland',
   'Coastal Highland distillery on the Sutherland coast; home to the rare waxy, coastal Clynelish character — beeswax, sea salt, citrus and orchard fruit. Prized by blenders and collectors worldwide.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Glenmorangie 18 Year Extremely Rare',
  'spirits_whiskey', 'highland_single_malt',
  97,
  (SELECT id FROM beverage_producers WHERE name = 'Glenmorangie Distillery' LIMIT 1),
  'Glenmorangie''s prestige expression; 18 years in ex-bourbon then Oloroso sherry casks producing exceptional peach, mango and orange blossom complexity with walnut and chocolate on the finish.',
  ARRAY['peach', 'mango', 'orange blossom', 'walnut', 'chocolate', 'vanilla'],
  'medium-full',
  'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'GlenDronach 18 Year Allardice',
  'spirits_whiskey', 'highland_single_malt',
  97,
  (SELECT id FROM beverage_producers WHERE name = 'GlenDronach Distillery' LIMIT 1),
  'Named for the estate''s founder; 18 years exclusively in Oloroso sherry casks. Dark fruit cake, Christmas spice, black cherry, orange peel and a long mocha finish. The archetype of sherry-matured Highland.',
  ARRAY['fruit cake', 'Christmas spice', 'black cherry', 'orange peel', 'mocha', 'dark chocolate'],
  'full',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Dalmore 18 Year',
  'spirits_whiskey', 'highland_single_malt',
  97,
  (SELECT id FROM beverage_producers WHERE name = 'Dalmore Distillery' LIMIT 1),
  'Triple-sherry-matured Highland malt; Oloroso, Amoroso and Apostoles casks delivering dark chocolate, marmalade, rich walnut and coffee. Complex yet approachable; a benchmark for sherry-influenced Highland style.',
  ARRAY['dark chocolate', 'marmalade', 'walnut', 'coffee', 'vanilla', 'orange zest'],
  'full',
  'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT
  'Clynelish 14 Year',
  'spirits_whiskey', 'highland_single_malt',
  97,
  (SELECT id FROM beverage_producers WHERE name = 'Clynelish Distillery' LIMIT 1),
  'The canonical coastal Highland malt; waxy-textured with sea salt, lemon and orchard fruit, heather honey and a dry mineral finish. One of Scotland''s most distinctive blending malts bottled at source.',
  ARRAY['beeswax', 'sea salt', 'lemon', 'orchard fruit', 'heather honey', 'dry mineral'],
  'medium',
  'estate', 'premium', true;

COMMIT;
