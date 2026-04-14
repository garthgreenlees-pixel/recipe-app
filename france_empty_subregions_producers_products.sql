BEGIN;

-- ============================================================
-- FRENCH EMPTY SUB-REGIONS: Morey-Saint-Denis (107),
-- Vougeot (109), Nuits-Saint-Georges (111), Beaune (114),
-- Pommard (115), Volnay (116), Chassagne-Montrachet (119),
-- Saint-Joseph (136), Gigondas (140), Vacqueyras (141),
-- Tavel (142), Chinon (152), Bourgueil (153),
-- Parent regions: Burgundy (104), Côte de Nuits (105),
-- Côte de Beaune (112), Bordeaux (121), Médoc (122),
-- Fronsac (130), Rhône Valley (131), Northern Rhône (132),
-- Southern Rhône (138), Loire Valley (147), Vallée de la Marne (146)
-- ============================================================

-- MOREY-SAINT-DENIS (107)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Ponsot', 'winery', 107, 'France',
   'Laurent Ponsot''s Morey estate; home to Clos de la Roche Vieilles Vignes — possibly Burgundy''s most intellectually honest Grand Cru. No new oak; terroir purity above all.',
   'reserve', 'ultra_premium', 1, true),
  ('Clos de Tart — Mommessin', 'winery', 107, 'France',
   'The only Grand Cru monopole in Morey-Saint-Denis; 7.5ha of unbroken vines since 1141. The Pinault family (2017) now invest heavily in sustainable viticulture for this deeply expressive, structured red.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Ponsot Clos de la Roche Vieilles Vignes Grand Cru',
  'wine_still', 'pinot noir',
  107, (SELECT id FROM beverage_producers WHERE name = 'Domaine Ponsot' LIMIT 1),
  'The greatest expression of Clos de la Roche; century-old vines, zero new oak, extraordinary terroir transparency. Iron, red cherry, wild mushroom and spice. Requires 15+ years to open.',
  ARRAY['iron', 'red cherry', 'wild mushroom', 'spice', 'truffle', 'wet stone'],
  'medium-full', 'reserve', 'ultra_premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Clos de Tart Grand Cru',
  'wine_still', 'pinot noir',
  107, (SELECT id FROM beverage_producers WHERE name = 'Clos de Tart — Mommessin' LIMIT 1),
  'The sole Grand Cru monopole of Morey-Saint-Denis; structured, mineral Pinot Noir with savoury dark cherry, iron and a silkier profile than its Gevrey neighbours. Exceptional longevity.',
  ARRAY['dark cherry', 'iron', 'forest floor', 'fine tannin', 'mineral spice'],
  'medium-full', 'reserve', 'ultra_premium', true;

-- VOUGEOT (109)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Château du Clos de Vougeot — Domaine Leroy', 'winery', 109, 'France',
   'Lalou Bize-Leroy''s biodynamic parcels within Clos de Vougeot Grand Cru; farmed to the same exacting biodynamic standards as Domaine Leroy. Extraordinary mineral intensity from specific low-yielding plots.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Leroy Clos de Vougeot Grand Cru',
  'wine_still', 'pinot noir',
  109, (SELECT id FROM beverage_producers WHERE name = 'Château du Clos de Vougeot — Domaine Leroy' LIMIT 1),
  'Lalou Bize-Leroy''s Clos de Vougeot parcel; biodynamic viticulture, tiny yields, extraordinary concentration. Dark berry, rose, iron mineral and a structural depth that demands two decades of cellaring.',
  ARRAY['dark berry', 'rose', 'iron mineral', 'truffle', 'dark spice', 'graphite'],
  'full', 'reserve', 'ultra_premium', true;

-- NUITS-SAINT-GEORGES (111)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Henri Gouges', 'winery', 111, 'France',
   'The reference domaine for Nuits-Saint-Georges since 1919; progenitor of the rare Pinot Meunier blanc mutation (Pinot Gouges). Structured, mineral, traditionally made wines that speak of their specific plots.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Henri Gouges Nuits-Saint-Georges Les Saint-Georges 1er Cru',
  'wine_still', 'pinot noir',
  111, (SELECT id FROM beverage_producers WHERE name = 'Domaine Henri Gouges' LIMIT 1),
  'The benchmark Nuits-Saint-Georges Premier Cru; iron-mineral, savoury and structured with dark cherry and dried herbs. Less showy than Gevrey or Chambolle but deeply expressive of the commune''s earthy character.',
  ARRAY['dark cherry', 'iron', 'dried herbs', 'earth', 'game', 'fine tannin'],
  'medium-full', 'reserve', 'ultra_premium', true;

-- BEAUNE (114)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine des Croix', 'winery', 114, 'France',
   'David Croix''s Beaune-based domaine built on exceptional Premier Cru and Grand Cru plots across the Côte de Beaune; elegant, precise Pinot Noir with a contemporary biodynamic approach.',
   'estate', 'premium', 2, true),
  ('Maison Louis Jadot — Beaune', 'winery', 114, 'France',
   'One of Burgundy''s great négociants and estate producers; the Beaune Clos des Ursules is Jadot''s flagship Monopole, providing consistent access to benchmark Premier Cru Beaune.',
   'estate', 'premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Louis Jadot Beaune Clos des Ursules 1er Cru',
  'wine_still', 'pinot noir',
  114, (SELECT id FROM beverage_producers WHERE name = 'Maison Louis Jadot — Beaune' LIMIT 1),
  'Jadot''s Beaune monopole; textbook Côte de Beaune Pinot Noir with red cherry, raspberry, light earthy spice and gentle tannin. One of the most approachable and consistent Premier Cru Burgundies.',
  ARRAY['red cherry', 'raspberry', 'light earth', 'gentle spice', 'silk tannin'],
  'medium', 'estate', 'premium', true;

-- POMMARD (115)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine du Comte Armand', 'winery', 115, 'France',
   'Pommard''s most celebrated estate; the 5.3ha Clos des Epeneaux monopole is consistently the appellation''s finest wine. Benjamin Leroux''s tenure (2004–2014) raised quality to Grand Cru equivalence.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Comte Armand Pommard Clos des Epeneaux Monopole 1er Cru',
  'wine_still', 'pinot noir',
  115, (SELECT id FROM beverage_producers WHERE name = 'Domaine du Comte Armand' LIMIT 1),
  'The definitive Pommard; 5.3ha monopole that consistently rivals Grand Cru quality. Structured, powerful dark cherry and iron with savoury spice and remarkable ageing potential. 15-25 year horizon.',
  ARRAY['dark cherry', 'iron', 'leather', 'dark spice', 'earthy mineral', 'fine structure'],
  'full', 'reserve', 'ultra_premium', true;

-- VOLNAY (116)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Marquis d''Angerville', 'winery', 116, 'France',
   'The great Volnay estate; Guillaume d''Angerville''s holdings include the Clos des Ducs monopole and legendary Champans. The reference point for Volnay''s quintessential elegance and floral delicacy.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Marquis d''Angerville Volnay Clos des Ducs 1er Cru Monopole',
  'wine_still', 'pinot noir',
  116, (SELECT id FROM beverage_producers WHERE name = 'Domaine Marquis d''Angerville' LIMIT 1),
  'Volnay''s most celebrated wine; d''Angerville monopole with ethereal red-cherry florality, violet, silky tannin and an unmistakable savoury mineral finish. The apex of Volnay''s feminine character.',
  ARRAY['red cherry', 'violet', 'raspberry', 'silk tannin', 'mineral', 'dried rose'],
  'medium', 'reserve', 'ultra_premium', true;

-- CHASSAGNE-MONTRACHET (119)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Marc Colin et Fils', 'winery', 119, 'France',
   'The great Chassagne-Montrachet domaine with exceptional Premier Cru whites and the coveted Montrachet Grand Cru parcel; precision vinification capturing the appellation''s mineral-stone-fruit intensity.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Marc Colin Chassagne-Montrachet Les Caillerets 1er Cru',
  'wine_still', 'white_chardonnay',
  119, (SELECT id FROM beverage_producers WHERE name = 'Domaine Marc Colin et Fils' LIMIT 1),
  'The reference Premier Cru Chassagne white; limestone-mineral Chardonnay with grilled almond, white peach, hazelnut and a steely acid backbone. Less opulent than Meursault; more structured than Puligny.',
  ARRAY['grilled almond', 'white peach', 'hazelnut', 'flint', 'limestone mineral', 'lemon cream'],
  'medium-full', 'reserve', 'ultra_premium', true;

-- SAINT-JOSEPH (136)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Pierre Gonon', 'winery', 136, 'France',
   'The reference domaine for Saint-Joseph; Pierre and Jean Gonon''s biodynamic Syrah and Marsanne from granite Mauves terroir are benchmark Northern Rhône wines at accessible prices.',
   'estate', 'premium', 1, true),
  ('Jean-Louis Chave Saint-Joseph', 'winery', 136, 'France',
   'The Chave family''s Saint-Joseph holding; while Hermitage is the crown jewel, the Chave Saint-Joseph rouge offers northern Rhône precision and depth at a fraction of the price.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Pierre Gonon Saint-Joseph Rouge',
  'wine_still', 'red_syrah',
  136, (SELECT id FROM beverage_producers WHERE name = 'Pierre Gonon' LIMIT 1),
  'The benchmark Saint-Joseph; biodynamic Syrah from granite Mauves hillsides. Violet florality, smoked olive, white pepper and clean dark berry with a mineral-dry finish. Benchmark for the appellation.',
  ARRAY['violet', 'smoked olive', 'white pepper', 'dark berry', 'iron', 'granite mineral'],
  'medium-full', 'estate', 'premium', true;

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Domaine Gonon Saint-Joseph Blanc',
  'wine_still', 'white_marsanne_roussanne',
  136, (SELECT id FROM beverage_producers WHERE name = 'Pierre Gonon' LIMIT 1),
  'Gonon''s Saint-Joseph Blanc from old-vine Marsanne; floral, waxy and mineral with white blossom, peach stone and a distinctive lanolin texture. Ages magnificently over 10+ years.',
  ARRAY['white blossom', 'peach stone', 'lanolin', 'beeswax', 'mineral', 'dried apricot'],
  'medium', 'estate', 'premium', true;

-- GIGONDAS (140)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Santa Duc', 'winery', 140, 'France',
   'Yves Gras''s biodynamic Gigondas estate; the Aux Grandes Vignes cuvée from 80-year-old Grenache vines represents the pinnacle of this lesser-known Southern Rhône appellation.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Santa Duc Gigondas Aux Grandes Vignes',
  'wine_still', 'red_grenache_blend',
  140, (SELECT id FROM beverage_producers WHERE name = 'Domaine Santa Duc' LIMIT 1),
  'The finest Gigondas; 80-year-old Grenache-dominant blend from the limestone limestone plateau of the Dentelles de Montmirail. Garrigue, kirsch, leather and a warm spiced finish.',
  ARRAY['kirsch', 'garrigue', 'leather', 'warm spice', 'black olive', 'dark fruit'],
  'full', 'estate', 'premium', true;

-- VACQUEYRAS (141)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Le Sang des Cailloux', 'winery', 141, 'France',
   'Serge Férigoule''s celebrated Vacqueyras domaine — "Blood of the Stones" — producing old-vine Grenache/Syrah/Mourvèdre of remarkable concentration and garrigue expression.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Le Sang des Cailloux Vacqueyras',
  'wine_still', 'red_grenache_blend',
  141, (SELECT id FROM beverage_producers WHERE name = 'Domaine Le Sang des Cailloux' LIMIT 1),
  'The benchmark Vacqueyras; old-vine GSM blend from stony terraces at the base of the Dentelles de Montmirail. Dark berry, dried thyme, garrigue and a long peppery finish.',
  ARRAY['dark berry', 'dried thyme', 'garrigue', 'black pepper', 'iron', 'savoury earth'],
  'full', 'estate', 'premium', true;

-- TAVEL (142)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Château d''Aquéria', 'winery', 142, 'France',
   'The reference estate for Tavel rosé; France''s only appellation dedicated exclusively to rosé production. Grenache-dominant with Clairette and Cinsault for structure, red fruit and garrigue complexity.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Château d''Aquéria Tavel Rosé',
  'wine_still', 'rosé_grenache_blend',
  142, (SELECT id FROM beverage_producers WHERE name = 'Château d''Aquéria' LIMIT 1),
  'The benchmark Tavel; France''s most structured rosé from the only AOC dedicated to it. Grenache-dominant with red cherry, strawberry, garrigue and a surprising savoury mineral finish that ages 3-5 years.',
  ARRAY['red cherry', 'strawberry', 'garrigue', 'fresh herb', 'savoury mineral', 'white pepper'],
  'medium', 'estate', 'premium', true;

-- CHINON (152)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Charles Joguet', 'winery', 152, 'France',
   'The estate that defined modern Chinon Cabernet Franc; individual-vineyard wines from limestone tuffs and sand-gravel terroirs expressing the extraordinary range of this versatile red grape.',
   'estate', 'premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Charles Joguet Chinon Clos de la Dioterie',
  'wine_still', 'red_cabernet_franc',
  152, (SELECT id FROM beverage_producers WHERE name = 'Domaine Charles Joguet' LIMIT 1),
  'The Chinon reference; old-vine Cabernet Franc from tuffeau limestone. Cassis, graphite pencil, violet and a savoury-herbal finish. Exceptional elegance and age-worthiness for a mid-weight Loire red.',
  ARRAY['cassis', 'graphite', 'violet', 'fresh herb', 'red pepper', 'earthy mineral'],
  'medium', 'estate', 'premium', true;

-- BOURGUEIL (153)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine Pierre Breton', 'winery', 153, 'France',
   'Catherine and Pierre Breton''s biodynamic Bourgueil estate; the Beauvais and Franc de Pied cuvées from ungrafted Cabernet Franc vines capture the appellation''s most precise sandy-gravel and tuffeau expression.',
   'estate', 'premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Pierre Breton Bourgueil Franc de Pied',
  'wine_still', 'red_cabernet_franc',
  153, (SELECT id FROM beverage_producers WHERE name = 'Domaine Pierre Breton' LIMIT 1),
  'Ungrafted pre-phylloxera Cabernet Franc vines on sandy Bourgueil soils; biodynamic. Cranberry, violet, graphite and Loire''s classic green-herbal lift on a silky frame. Uniquely mineral and precise.',
  ARRAY['cranberry', 'violet', 'graphite', 'green herb', 'red berry', 'sandy mineral'],
  'medium', 'estate', 'premium', true;

-- VALLÉE DE LA MARNE (146)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Chartogne-Taillet', 'winery', 146, 'France',
   'Alexandre Chartogne''s Merfy-based grower Champagne house in the Vallée de la Marne; single-village and single-plot wines expressing the Pinot Meunier terroir of the western Marne with artisanal rigour.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Chartogne-Taillet Cuvée Sainte-Anne',
  'wine_sparkling', 'champagne_blanc_de_meunier',
  146, (SELECT id FROM beverage_producers WHERE name = 'Chartogne-Taillet' LIMIT 1),
  'Benchmark Vallée de la Marne grower Champagne from Meunier-dominant Merfy village; wild strawberry, red apple, pastry cream and a mineral-chalky backbone. Expressive, approachable artisan Champagne.',
  ARRAY['wild strawberry', 'red apple', 'pastry cream', 'chalk mineral', 'brioche', 'fresh berry'],
  'medium', 'estate', 'premium', true;

-- BURGUNDY PARENT (104) — generic regional Bourgogne
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Domaine de la Romanée-Conti — Bourgogne', 'winery', 104, 'France',
   'DRC''s regional Bourgogne AOC bottling; declassified fruit from young vines and village parcels. The entry-level access point to the DRC house style — and the world''s most sought-after Bourgogne appellation wine.',
   'reserve', 'ultra_premium', 1, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'DRC Bourgogne Rouge',
  'wine_still', 'pinot noir',
  104, (SELECT id FROM beverage_producers WHERE name = 'Domaine de la Romanée-Conti — Bourgogne' LIMIT 1),
  'The world''s most sought-after Bourgogne; DRC''s declassified village wine offering DRC house style — spice, red cherry and mineral purity — at village appellation level. Extremely limited.',
  ARRAY['red cherry', 'spice', 'mineral', 'violet', 'forest floor', 'silk tannin'],
  'medium', 'reserve', 'ultra_premium', true;

-- FRONSAC (130)
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published)
VALUES
  ('Château Moulin Haut-Laroque', 'winery', 130, 'France',
   'Jean-Noël Hervé''s biodynamic Fronsac estate; the benchmark for this overlooked Right Bank appellation. Old-vine Merlot and Cabernet Franc on molasse limestone producing wines of Pomerol-like richness.',
   'estate', 'premium', 2, true);

INSERT INTO beverage_products
  (name, category, subcategory, region_id, producer_id,
   description, flavour_markers, flavour_weight,
   quality_tier, price_tier, is_published)
SELECT 'Château Moulin Haut-Laroque Fronsac',
  'wine_still', 'red_merlot_blend',
  130, (SELECT id FROM beverage_producers WHERE name = 'Château Moulin Haut-Laroque' LIMIT 1),
  'The reference Fronsac; biodynamic Merlot-Cabernet Franc from limestone terroir. Plum, cedar, dried herbs and a savoury mineral finish. Pomerol quality at a fraction of the price.',
  ARRAY['dark plum', 'cedar', 'dried herbs', 'limestone mineral', 'dark cherry', 'iron'],
  'medium-full', 'estate', 'premium', true;

COMMIT;
