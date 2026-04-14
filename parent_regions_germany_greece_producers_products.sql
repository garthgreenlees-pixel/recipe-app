BEGIN;

-- ============================================================
-- FRENCH PARENT REGIONS (umbrellas with no direct products)
-- Côte de Nuits (105), Côte de Beaune (112), Bordeaux (121),
-- Médoc (122), Rhône Valley (131), Northern Rhône (132),
-- Southern Rhône (138), Loire Valley (147)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Maison Bouchard Père et Fils', 'winery', 105, 'France',
   'One of the Côte de Nuits'' great négoce-domaine houses; 130ha of estate vines including the monopole Beaune Grèves Vigne de l''Enfant Jésus. Benchmark Côte de Nuits village appellation wines.',
   'estate', 'premium', 1, true),
  ('Maison Drouhin — Côte de Beaune', 'winery', 112, 'France',
   'One of Burgundy''s most respected négoce houses with 93ha of estate vines; Maison Drouhin is the reference producer for accessible Côte de Beaune village wines with consistent quality and terroir expression.',
   'estate', 'premium', 1, true),
  ('Château Pichon Comtesse de Lalande', 'winery', 121, 'France',
   'Pauillac''s great super-second; under the Rouzaud family (2007), this estate now challenges the First Growths. A benchmark for understanding Bordeaux''s combination of elegance and power at the highest level.',
   'reserve', 'ultra_premium', 1, true),
  ('Château Lynch-Bages', 'winery', 122, 'France',
   'Pauillac''s most beloved Fifth Growth; consistently outperforming its classification since Jean-Charles Cazes took over. Generous, approachable and complex Médoc Cabernet at mid-market luxury pricing.',
   'reserve', 'ultra_premium', 1, true),
  ('E. Guigal — Côtes du Rhône', 'winery', 131, 'France',
   'Marcel Guigal''s regional Côtes du Rhône offers unmatched quality at its price point; a blend of Northern and Southern Rhône grapes expressing the full Rhône aromatic palette at accessible entry level.',
   'estate', 'premium', 1, true),
  ('Jean-Louis Chave Hermitage — Northern Rhône', 'winery', 132, 'France',
   'The defining Northern Rhône estate; Gérard and Jean-Louis Chave''s Hermitage blanc and rouge from multiple lieu-dits represent the apex of Marsanne and Syrah respectively.',
   'reserve', 'ultra_premium', 1, true),
  ('Château Beaucastel — Southern Rhône', 'winery', 138, 'France',
   'The Perrin family''s Châteauneuf-du-Pape estate planted to all 13 Rhône varieties; Beaucastel Blanc (old-vine Roussanne) is the reference white of the Southern Rhône alongside the great red.',
   'reserve', 'ultra_premium', 1, true),
  ('Domaine Henry Marionnet — Loire', 'winery', 147, 'France',
   'Touraine''s innovative estate; renowned for ungrafted pre-phylloxera vines and the First Vintage series. A benchmark for understanding the Loire Valley''s gamay and sauvignon potential beyond Sancerre.',
   'estate', 'premium', 2, true);

-- Côte de Nuits Villages (105)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Bouchard Père et Fils Côte de Nuits-Villages Rouge',
  'wine_still', 'pinot noir',
  105, (SELECT id FROM beverage_producers WHERE name = 'Maison Bouchard Père et Fils' LIMIT 1),
  'Classic Côte de Nuits-Villages appellation; red cherry, earth and mild tannin with genuine Pinot Noir delicacy at village level. A reliable entry into the famous Côte de Nuits vineyard hierarchy.',
  ARRAY['red cherry', 'earth', 'mild tannin', 'forest floor', 'gentle spice'],
  'medium', 'estate', 'premium', true;

-- Côte de Beaune (112)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Drouhin Côte de Beaune-Villages',
  'wine_still', 'pinot noir',
  112, (SELECT id FROM beverage_producers WHERE name = 'Maison Drouhin — Côte de Beaune' LIMIT 1),
  'Drouhin''s benchmark Côte de Beaune-Villages; a blend of village-level parcels producing elegant Pinot Noir with raspberry, light earth and characteristic Beaune silk. Reliable quality for everyday Burgundy.',
  ARRAY['raspberry', 'light earth', 'silk tannin', 'red fruit', 'gentle mineral'],
  'medium', 'estate', 'premium', true;

-- Bordeaux (121) — using Pichon Comtesse under the Bordeaux parent
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Château Pichon Comtesse de Lalande',
  'wine_still', 'red_bordeaux_blend',
  121, (SELECT id FROM beverage_producers WHERE name = 'Château Pichon Comtesse de Lalande' LIMIT 1),
  'Pauillac Super-Second consistently challenging the First Growths; Cabernet-Merlot with unusually high Merlot and Cabernet Franc percentages giving it remarkable suppleness for a Pauillac. Cassis, cedar, floral lift.',
  ARRAY['cassis', 'cedar', 'violet floral', 'dark plum', 'graphite', 'fine tannin'],
  'full', 'reserve', 'ultra_premium', true;

-- Médoc (122)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Château Lynch-Bages',
  'wine_still', 'red_cabernet_sauvignon',
  122, (SELECT id FROM beverage_producers WHERE name = 'Château Lynch-Bages' LIMIT 1),
  'The beloved Médoc Fifth Growth that tastes like a Second; Pauillac Cabernet Sauvignon with generous blackcurrant, cedar and savoury olive tapenade. Immediate and approachable without sacrificing depth.',
  ARRAY['blackcurrant', 'cedar', 'olive tapenade', 'dark plum', 'tobacco', 'spiced oak'],
  'full', 'reserve', 'ultra_premium', true;

-- Rhône Valley (131)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'E. Guigal Côtes du Rhône Rouge',
  'wine_still', 'red_grenache_syrah_blend',
  131, (SELECT id FROM beverage_producers WHERE name = 'E. Guigal — Côtes du Rhône' LIMIT 1),
  'The world''s reference Côtes du Rhône; Guigal''s regional blend of Grenache, Syrah and Mourvèdre delivers remarkable complexity at its price point — the benchmark for Rhône''s entry-level quality.',
  ARRAY['dark cherry', 'garrigue', 'black pepper', 'dried herb', 'warm spice', 'mineral'],
  'medium', 'estate', 'premium', true;

-- Northern Rhône (132)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Jean-Louis Chave Hermitage Rouge',
  'wine_still', 'red_syrah',
  132, (SELECT id FROM beverage_producers WHERE name = 'Jean-Louis Chave Hermitage — Northern Rhône' LIMIT 1),
  'The most celebrated Northern Rhône Syrah; a blend of multiple Hermitage lieux-dits by the Chave family since 1481. Smoked olive, dark berry, violet, iron and extraordinary ageing potential — 20-40+ years.',
  ARRAY['smoked olive', 'dark berry', 'violet', 'iron', 'white pepper', 'dark chocolate'],
  'full', 'reserve', 'ultra_premium', true;

-- Southern Rhône (138)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Château Beaucastel Châteauneuf-du-Pape Blanc',
  'wine_still', 'white_roussanne_marsanne',
  138, (SELECT id FROM beverage_producers WHERE name = 'Château Beaucastel — Southern Rhône' LIMIT 1),
  'The definitive Southern Rhône white; old-vine Roussanne producing a honeyed, mineral, remarkably ageworthy white. Beeswax, dried apricot, roasted hazelnut and an extraordinary 20-year evolution.',
  ARRAY['beeswax', 'dried apricot', 'roasted hazelnut', 'honey', 'savoury mineral', 'white flowers'],
  'medium-full', 'reserve', 'ultra_premium', true;

-- Loire Valley (147)
INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Henry Marionnet Touraine Sauvignon Blanc',
  'wine_still', 'white_sauvignon_blanc',
  147, (SELECT id FROM beverage_producers WHERE name = 'Domaine Henry Marionnet — Loire' LIMIT 1),
  'Loire Valley Touraine Sauvignon at its most expressive; crisp gooseberry, elder flower, white grapefruit and a clean chalky mineral finish. The ideal introductory Loire Sauvignon beyond Sancerre''s price point.',
  ARRAY['gooseberry', 'elder flower', 'white grapefruit', 'chalk mineral', 'cut grass', 'clean finish'],
  'light', 'estate', 'premium', true;

-- ============================================================
-- GERMANY: Rhine & Cologne — Kölsch/Altbier (103)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Gaffel Kölsch', 'brewery', 103, 'Germany',
   'One of Cologne''s 12 remaining Kölsch breweries; Gaffel produces the freshest, most widely distributed Kölsch with a meticulous cold-conditioning process that preserves the style''s delicate fruit-hop balance.',
   'estate', 'premium', 2, true),
  ('Uerige Obergärige Hausbrauerei — Altbier', 'brewery', 103, 'Germany',
   'The reference house for Düsseldorf Altbier; Uerige''s copper-coloured, top-fermented Altbier is served directly from the cask at 8°C in traditional Stangengläser. The definitive expression of Rhine Altbier tradition.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Gaffel Kölsch',
  'beer_ale', 'kolsch',
  103, (SELECT id FROM beverage_producers WHERE name = 'Gaffel Kölsch' LIMIT 1),
  'The benchmark Kölsch; pale straw, light-bodied top-fermented ale brewed under the Kölsch Konvention exclusively in Cologne. Subtle apple-pear ester, gentle hop bitterness and a bone-dry finish. Served at 8°C in Stangen.',
  ARRAY['pale apple', 'pear ester', 'gentle hops', 'dry finish', 'light biscuit', 'clean'],
  'light', 'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Uerige Altbier',
  'beer_ale', 'altbier',
  103, (SELECT id FROM beverage_producers WHERE name = 'Uerige Obergärige Hausbrauerei — Altbier' LIMIT 1),
  'The definitive Düsseldorf Altbier; copper-amber, top-fermented with German hops. Assertive hop bitterness, roasted malt, caramel and a dry mineral finish. The most savoury and complex of the Rhine''s indigenous styles.',
  ARRAY['caramel malt', 'assertive hops', 'roasted grain', 'dry mineral', 'dark fruit', 'copper character'],
  'medium', 'estate', 'premium', true;

-- ============================================================
-- GREECE: Crete (181)
-- ============================================================

INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Lyrarakis Winery', 'winery', 181, 'Greece',
   'The leading Crete winery championing indigenous varieties including Dafni, Plyto and Vidiano; estate vineyards at altitude in the Psiloritis mountains producing some of Greece''s most distinctive terroir-driven whites.',
   'estate', 'premium', 2, true),
  ('Douloufakis Winery', 'winery', 181, 'Greece',
   'Crete''s benchmark red wine estate; Kotsifali and Mandilari-dominant blends from the Peza appellation with traditional and modern techniques — producing Crete''s most structured, age-worthy reds.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Lyrarakis Dafni',
  'wine_still', 'white_dafni',
  181, (SELECT id FROM beverage_producers WHERE name = 'Lyrarakis Winery' LIMIT 1),
  'Crete''s most distinctive indigenous white grape; Dafni produces an extraordinary aromatic white with intense bay laurel, lemon thyme, citrus and a dry, saline mineral finish. Unique in the world.',
  ARRAY['bay laurel', 'lemon thyme', 'citrus zest', 'white floral', 'saline mineral', 'dried herb'],
  'light', 'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Douloufakis Dafnios Red',
  'wine_still', 'red_kotsifali_mandilari',
  181, (SELECT id FROM beverage_producers WHERE name = 'Douloufakis Winery' LIMIT 1),
  'Crete''s benchmark red blend from indigenous Kotsifali and Mandilari; soft dark cherry, dried herbs, warm earth and a Mediterranean garrigue character. Shows Crete''s capacity for structured, aromatic red wine.',
  ARRAY['dark cherry', 'dried herbs', 'warm earth', 'garrigue', 'cinnamon', 'savoury mineral'],
  'medium-full', 'estate', 'premium', true;

COMMIT;
