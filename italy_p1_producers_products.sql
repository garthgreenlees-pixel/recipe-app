-- Italy Phase 1: Producers + Products for empty Italian regions
-- Regions: Piedmont=160, Asti=163, Gavi=164, Vino Nobile=169, Vernaccia=170, Prosecco=174
-- Also adds: Fenocchio, Altare, Produttori for Barolo=161, Barbaresco=162
-- Max producer ID before this: 313 → new producers start at 314
-- Max product ID before this: 370 → new products start at 371

BEGIN;

-- ============================================================
-- NEW PRODUCERS
-- ============================================================
INSERT INTO beverage_producers
  (name, producer_type, region_id, country, philosophy_description,
   quality_tier, price_positioning, authority_tier, is_published) VALUES

-- Piedmont: Barbera, Dolcetto sub-regions
('Michele Chiarlo', 'winery', 160, 'Italy',
 'One of Piedmont''s most respected producers with holdings across Barolo, Barbaresco, Barbera d''Asti, and Moscato d''Asti. Family winery established 1956; sustainable viticulture across 100+ ha. The Moscato d''Asti Nivole is among Italy''s finest examples of the variety.',
 'estate', 'premium', 2, true),

('La Spinetta', 'winery', 160, 'Italy',
 'The Rivetti family''s estate (est. 1977) known internationally for single-vineyard Barolo and Barbaresco but equally celebrated for Moscato d''Asti (Bricco Quaglia) and Barbera d''Asti. The Moscato Bricco Quaglia defined the contemporary benchmark for the Asti appellation.',
 'estate', 'premium', 2, true),

('Braida di Giacomo Bologna', 'winery', 160, 'Italy',
 'The estate that transformed Barbera d''Asti from a workhorse variety into a world-class wine. Giacomo Bologna''s revolutionary oak-aging of Barbera (Bricco dell''Uccellone, 1982) proved the variety could achieve complexity and age-worthiness. His daughter Raffaella continues his work from Rocchetta Tanaro.',
 'estate', 'premium', 2, true),

-- Asti DOCG
('Bera', 'winery', 163, 'Italy',
 'A fourth-generation family winery in Canelli producing benchmark Moscato d''Asti and sparkling Asti Spumante from the steep Canelli hills where Moscato Bianco achieves its fullest aromatic intensity. One of the most respected names in the appellation.',
 'estate', 'mid_range', 2, true),

-- Gavi DOCG
('La Scolca', 'winery', 164, 'Italy',
 'The estate credited with establishing Gavi as a fine wine appellation. La Scolca''s Black Label Gavi di Gavi (Cortese grape) has been the benchmark since 1919. The winery owns 50ha in the Gavi commune — the most prestigious zone within the appellation.',
 'reserve', 'premium', 2, true),

('Broglia', 'winery', 164, 'Italy',
 'Leading Gavi producer from the La Meirana estate — a single large holding in the Gavi commune. The La Meirana Gavi di Gavi is consistently among the appellation''s finest: mineral, citrus-precise, built for seafood. A benchmark for the Cortese grape.',
 'estate', 'mid_range', 2, true),

-- Vino Nobile di Montepulciano
('Poliziano', 'winery', 169, 'Italy',
 'One of the great estates of Montepulciano, founded by Federico Carletti in 1961. Poliziano''s Vino Nobile Asinone single-vineyard is considered the reference wine of the appellation — Prugnolo Gentile (Sangiovese clone) from 25-year-old vines on red clay soils at 350m.',
 'estate', 'premium', 2, true),

('Avignonesi', 'winery', 169, 'Italy',
 'Historic Montepulciano estate (est. 1974) producing Vino Nobile alongside the legendary Occhio di Pernice Vin Santo from Prugnolo Gentile requiring 10 years of barrel aging. The estate converted to full biodynamic viticulture in 2009 under current owner Virginie Saverys.',
 'estate', 'premium', 2, true),

-- Vernaccia di San Gimignano
('Montenidoli', 'winery', 170, 'Italy',
 'Elisabetta Fagiuoli''s estate in San Gimignano is the spiritual home of Vernaccia di San Gimignano — producing wines of unusual depth and age-worthiness from a variety often dismissed as light and simple. The Tradizionale (skin contact) and Fiore (direct press) demonstrate the range the Vernaccia grape is capable of.',
 'estate', 'mid_range', 2, true),

('Teruzzi', 'winery', 170, 'Italy',
 'The estate most responsible for Vernaccia di San Gimignano''s international reputation, established by Enrico Teruzzi in 1974. Their Carmen Riserva (barrel-fermented) and standard Vernaccia are the entry points for understanding the appellation''s range.',
 'estate', 'mid_range', 2, true),

-- Prosecco DOCG Valdobbiadene
('Bisol', 'winery', 174, 'Italy',
 'The historic Bisol family has farmed the steep Valdobbiadene hills since 1542. Their Cartizze (from the single Grand Cru hill) and Crede single-vineyard Prosecco Superiore are the benchmarks of the DOCG zone. Bisol defines what Prosecco can achieve at its finest.',
 'reserve', 'premium', 2, true),

('Ruggeri', 'winery', 174, 'Italy',
 'Valdobbiadene-based producer specialising in Prosecco Superiore DOCG from the Rive (single-village) system. The Giustino B. Extra Brut is one of the appellation''s most celebrated wines — made entirely from Cartizze-adjacent Glera with no residual sugar. A revelation for those who know only soft Prosecco.',
 'estate', 'mid_range', 2, true),

('Nino Franco', 'winery', 174, 'Italy',
 'Fourth-generation producer (est. 1919) in Valdobbiadene, producing among the most consistently excellent Prosecco Superiore in the region. The Rustico NV is the benchmark accessible Prosecco; the Grave di Stecca is among the finest single-vineyard expressions of the appellation.',
 'estate', 'mid_range', 2, true),

-- Barolo / Barbaresco new entries
('Giacomo Fenocchio', 'winery', 161, 'Italy',
 'Small traditional Barolo producer in Castiglione Falletto with exceptional parcels in Bussia. A traditionalist — long maceration, large Slavonian oak botti — producing Barolo of the classic northern Langhe style: austere in youth, profound with age.',
 'estate', 'premium', 2, true),

('Elio Altare', 'winery', 161, 'Italy',
 'One of the leaders of Barolo''s modernist revolution in the 1980s, introducing short maceration and French barrique aging. His Barolo Arborina and Brunate are among the most celebrated of the modern style — opulent, approachable young, compelling for decades.',
 'estate', 'ultra_premium', 1, true),

('Produttori del Barbaresco', 'winery', 162, 'Italy',
 'The cooperative that defines Barbaresco''s soul — 56 grower-members farming 100ha in the Barbaresco commune, releasing single-vineyard riserve from nine crus. No producer better demonstrates Barbaresco''s micro-terroir differences: compare the Rabajà (structured) with the Montestefano (floral) to understand the appellation.',
 'estate', 'mid_range', 2, true),

('Marchesi di Barolo', 'winery', 161, 'Italy',
 'One of Barolo''s oldest estates (est. 1807), historically responsible for naming the wine. The estate''s Sarmassa and Cannubi vineyard bottlings represent two contrasting expressions of Barolo from the central zone — a living archive of the appellation''s terroir diversity.',
 'estate', 'premium', 2, true),

('Parusso', 'winery', 161, 'Italy',
 'The Parusso family estate in Castiglione Falletto produces powerful, precise Barolo from Bussia and Mariondino vineyards. A modern-leaning style with excellent structure and age-worthiness. Their Barolo Mariondino is a critical favourite.',
 'estate', 'premium', 2, true);

-- ============================================================
-- PRODUCTS: Empty Italian Regions
-- ============================================================

-- PIEDMONT general (region 160) — Barbera d'Asti + Dolcetto
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('Braida Bricco dell''Uccellone Barbera d''Asti Superiore',
 'wine_still', 'Barbera d''Asti Superiore DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Braida di Giacomo Bologna'),
 160, 'Italy',
 'The wine that changed Barbera''s destiny. Giacomo Bologna''s decision to age Barbera in new French barriques (first vintage 1982) shocked the Piedmontese establishment and created a new paradigm. Deep ruby-violet; dark plum, coffee, cedar, violets; full-bodied with round tannins and driving acidity that will support 15+ years of aging. The reference point for the appellation.',
 'estate', 'premium', 'full',
 ARRAY['dark plum', 'coffee', 'cedar', 'violets', 'dark cherry', 'spice'],
 '{"grape": "Barbera d''Asti", "region": "Asti, Piedmont", "aging": "12 months French barriques", "abv": "14.0%", "style": "Barbera d''Asti Superiore DOCG"}'::jsonb,
 true),

('G.D. Vajra Dolcetto d''Alba',
 'wine_still', 'Dolcetto d''Alba DOC',
 (SELECT id FROM beverage_producers WHERE name = 'G.D. Vajra'),
 160, 'Italy',
 'The quintessential everyday Barolo producer''s everyday wine — Vajra''s Dolcetto d''Alba is a masterclass in the variety: deep violet-purple, fresh blueberry and cherry, almond finish, soft tannins with notable but structured grip. Piedmont''s approachable genius, best within 3 years.',
 'market', 'mid_range', 'medium',
 ARRAY['blueberry', 'black cherry', 'almond', 'violet', 'cocoa'],
 '{"grape": "Dolcetto", "region": "Alba, Piedmont", "aging": "6 months stainless/large oak", "abv": "13.5%", "style": "Dolcetto d''Alba DOC"}'::jsonb,
 true),

('Michele Chiarlo Barbera d''Asti Superiore La Court',
 'wine_still', 'Nizza DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Michele Chiarlo'),
 160, 'Italy',
 'From Chiarlo''s historic La Court vineyard in Castelnuovo Calcea — one of the crus that petitioned for the Nizza sub-appellation. This Barbera is a benchmark for age-worthy Nizza: concentrated dark fruit, tobacco, mineral grip, and the signature bright acidity of Barbera balanced by barrel integration. The 2016-2019 vintages are particularly celebrated.',
 'estate', 'premium', 'full',
 ARRAY['blackberry', 'tobacco', 'dark cherry', 'mineral', 'spice', 'cedar'],
 '{"grape": "Barbera d''Asti", "region": "Nizza, Piedmont", "aging": "12 months barriques + 6 months bottle", "abv": "14.5%", "style": "Nizza DOCG"}'::jsonb,
 true);

-- ASTI DOCG (region 163) — Moscato d'Asti + Asti Spumante
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('La Spinetta Moscato d''Asti Bricco Quaglia',
 'wine_sparkling', 'Moscato d''Asti DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'La Spinetta'),
 163, 'Italy',
 'The benchmark Moscato d''Asti — from La Spinetta''s Bricco Quaglia vineyard in Canelli, where steep hillside exposure and sandy soils concentrate the Moscato Bianco grape''s aromatic intensity. Delicate fizz (frizzante), low alcohol (5.5%), intensely perfumed: apricot, orange blossom, peach, honey. The reference point for understanding Moscato d''Asti at its finest.',
 'estate', 'mid_range', 'light',
 ARRAY['apricot', 'orange blossom', 'white peach', 'honey', 'jasmine', 'ginger'],
 '{"grape": "Moscato Bianco", "region": "Canelli, Asti, Piedmont", "abv": "5.5%", "residual_sugar": "120 g/L", "style": "Moscato d''Asti DOCG frizzante"}'::jsonb,
 true),

('Bera Moscato d''Asti',
 'wine_sparkling', 'Moscato d''Asti DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Bera'),
 163, 'Italy',
 'Bera''s family Moscato d''Asti from Canelli''s steep hill vineyards — a wine of exceptional aromatic clarity and delicacy. Pale gold with fine persistent bubbles; fresh apricot, lemon blossom, white peach, and gentle honey sweetness with refreshing acidity. One of the most food-versatile dessert wines in the world.',
 'estate', 'mid_range', 'light',
 ARRAY['apricot', 'lemon blossom', 'white peach', 'honey', 'ginger snap'],
 '{"grape": "Moscato Bianco", "region": "Canelli, Asti", "abv": "5.5%", "residual_sugar": "115 g/L", "style": "Moscato d''Asti DOCG"}'::jsonb,
 true),

('Bera Asti Spumante DOCG',
 'wine_sparkling', 'Asti Spumante DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Bera'),
 163, 'Italy',
 'Bera''s fully sparkling Asti (as opposed to the semi-sparkling Moscato d''Asti) from the same Canelli Moscato Bianco vineyards. More exuberant fizz than Moscato d''Asti, equally aromatic, slightly higher alcohol (7%). The benchmark for Asti Spumante DOCG: a wine that predates Champagne''s global dominance and remains a landmark for sweet sparkling.',
 'market', 'mid_range', 'light',
 ARRAY['peach', 'apricot', 'orange zest', 'honey', 'lemon cream'],
 '{"grape": "Moscato Bianco", "region": "Canelli, Asti", "abv": "7.0%", "residual_sugar": "95 g/L", "style": "Asti Spumante DOCG"}'::jsonb,
 true),

('Michele Chiarlo Moscato d''Asti Nivole',
 'wine_sparkling', 'Moscato d''Asti DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Michele Chiarlo'),
 163, 'Italy',
 'Nivole (''clouds'' in Piedmontese dialect) is Chiarlo''s flagship Moscato d''Asti — from Santo Stefano Belbo, the historic heart of the Canelli Moscato zone. A wine of extraordinary perfume: intense white peach, apricot, jasmine, and rose petal on the nose; delicate sweetness and natural acidity on the palate. Arguably the finest value in Italian dessert wine.',
 'estate', 'mid_range', 'light',
 ARRAY['white peach', 'apricot', 'jasmine', 'rose petal', 'honey', 'orange blossom'],
 '{"grape": "Moscato Bianco", "region": "Santo Stefano Belbo, Asti", "abv": "5.5%", "residual_sugar": "118 g/L", "style": "Moscato d''Asti DOCG"}'::jsonb,
 true);

-- GAVI DOCG (region 164)
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('La Scolca Black Label Gavi di Gavi',
 'wine_still', 'Gavi di Gavi DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'La Scolca'),
 164, 'Italy',
 'The benchmark Gavi — from La Scolca''s estate in the Gavi commune itself, where the Cortese grape produces its most mineral and precise expression. Pale straw; white flower, lemon zest, green apple, almonds; crisp acidity, medium body, and a mineral-saline finish that makes it one of Italy''s greatest seafood wines. Benchmark for the Cortese grape since 1919.',
 'reserve', 'premium', 'medium-light',
 ARRAY['lemon zest', 'white flower', 'green apple', 'almond', 'mineral', 'saline'],
 '{"grape": "Cortese", "region": "Gavi commune, Piedmont", "aging": "stainless steel on lees", "abv": "12.5%", "style": "Gavi di Gavi DOCG"}'::jsonb,
 true),

('Broglia La Meirana Gavi di Gavi',
 'wine_still', 'Gavi di Gavi DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Broglia'),
 164, 'Italy',
 'From Broglia''s single La Meirana estate in the Gavi commune — 70ha of Cortese farmed without compromise. A more mineral and structured Gavi than most: citrus-precise, with a distinctive flint and white flower character that sets it apart from the broader Gavi appellation. The benchmark for single-estate Gavi di Gavi.',
 'estate', 'mid_range', 'medium-light',
 ARRAY['citrus', 'flint', 'white flower', 'green apple', 'almond', 'lemon cream'],
 '{"grape": "Cortese", "region": "Gavi commune, Piedmont", "abv": "12.0%", "style": "Gavi di Gavi DOCG"}'::jsonb,
 true);

-- VINO NOBILE DI MONTEPULCIANO DOCG (region 169)
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('Poliziano Vino Nobile di Montepulciano Asinone',
 'wine_still', 'Vino Nobile di Montepulciano DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Poliziano'),
 169, 'Italy',
 'The reference wine of the Vino Nobile di Montepulciano appellation — from Poliziano''s Asinone single vineyard at 350m on red clay (tufo) soils. 100% Prugnolo Gentile (the local Sangiovese clone); 24 months large oak plus 12 months bottle. Dense ruby; dark cherry, dried rose, tobacco, leather, mineral. Structured and austere in youth, it rewards a decade of cellaring.',
 'estate', 'premium', 'full',
 ARRAY['dark cherry', 'dried rose', 'tobacco', 'leather', 'mineral', 'spice'],
 '{"grape": "Prugnolo Gentile (Sangiovese)", "region": "Montepulciano, Tuscany", "vineyard": "Asinone", "aging": "24 months large oak + 12 months bottle", "abv": "14.0%", "style": "Vino Nobile DOCG"}'::jsonb,
 true),

('Avignonesi Vino Nobile di Montepulciano',
 'wine_still', 'Vino Nobile di Montepulciano DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Avignonesi'),
 169, 'Italy',
 'Avignonesi''s flagship Vino Nobile from the estate''s biodynamic-farmed vineyards around Montepulciano. Since Virginie Saverys'' 2009 conversion to biodynamics, the wines have gained precision and purity without losing their Tuscan character. Dark cherry, dried herbs, spice, and earthy minerality — a benchmark for the appellation with strong age potential.',
 'estate', 'premium', 'full',
 ARRAY['dark cherry', 'dried herbs', 'spice', 'earth', 'tobacco', 'violet'],
 '{"grape": "Prugnolo Gentile (Sangiovese)", "region": "Montepulciano, Tuscany", "farming": "certified biodynamic", "aging": "18 months large oak", "abv": "14.0%", "style": "Vino Nobile DOCG"}'::jsonb,
 true),

('Poliziano Rosso di Montepulciano',
 'wine_still', 'Rosso di Montepulciano DOC',
 (SELECT id FROM beverage_producers WHERE name = 'Poliziano'),
 169, 'Italy',
 'Poliziano''s second wine, declassified from younger vines and some Vino Nobile parcels. A wine of tremendous value: bright cherry, fresh herbs, and the distinctive Prugnolo Gentile character in an approachable, food-friendly format. The ideal entry point to Montepulciano''s wine culture — best within 5 years.',
 'market', 'mid_range', 'medium',
 ARRAY['fresh cherry', 'herbs', 'dried tomato', 'spice', 'earth'],
 '{"grape": "Prugnolo Gentile + Merlot", "region": "Montepulciano, Tuscany", "aging": "12 months large oak", "abv": "13.5%", "style": "Rosso di Montepulciano DOC"}'::jsonb,
 true);

-- VERNACCIA DI SAN GIMIGNANO DOCG (region 170)
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('Montenidoli Vernaccia di San Gimignano Tradizionale',
 'wine_still', 'Vernaccia di San Gimignano DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Montenidoli'),
 170, 'Italy',
 'Elisabetta Fagiuoli''s skin-contact Vernaccia — the wine that redefined what the variety could be. Extended maceration on skins gives golden colour, tannic grip, and extraordinary aromatic complexity: quince, dried apricot, almond, beeswax, and a saline mineral finish. An orange wine before orange wines were fashionable. The benchmark for ambitious Vernaccia.',
 'estate', 'premium', 'medium',
 ARRAY['quince', 'dried apricot', 'almond', 'beeswax', 'saline', 'chamomile'],
 '{"grape": "Vernaccia di San Gimignano", "region": "San Gimignano, Tuscany", "method": "skin contact maceration", "abv": "13.0%", "style": "Vernaccia DOCG Tradizionale"}'::jsonb,
 true),

('Teruzzi Vernaccia di San Gimignano',
 'wine_still', 'Vernaccia di San Gimignano DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Teruzzi'),
 170, 'Italy',
 'Teruzzi''s standard Vernaccia — the wine that introduced the appellation to international markets in the 1970s. Pale straw; white flowers, lemon, almond, and a characteristic bitter almond finish that is the Vernaccia signature. Fresh and precise, built for Tuscan cuisine. The accessible benchmark for the appellation.',
 'market', 'mid_range', 'light',
 ARRAY['lemon', 'white flower', 'almond', 'bitter almond', 'green herb', 'saline'],
 '{"grape": "Vernaccia di San Gimignano", "region": "San Gimignano, Tuscany", "aging": "stainless steel", "abv": "12.5%", "style": "Vernaccia di San Gimignano DOCG"}'::jsonb,
 true);

-- PROSECCO DOCG Valdobbiadene (region 174)
INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, price_tier, flavour_weight, flavour_markers,
   technical_specs, is_published) VALUES

('Bisol Cartizze Dry',
 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze',
 (SELECT id FROM beverage_producers WHERE name = 'Bisol'),
 174, 'Italy',
 'Bisol''s Cartizze — from the 107-hectare single Grand Cru hill within Valdobbiadene, where the steepest slopes and south-facing exposure concentrate the Glera grape to exceptional intensity. The ''Dry'' designation (17-32 g/L RS) is traditional for Cartizze: delicate sweetness, fine persistent mousse, and intense white peach, apple blossom, and mineral character. The pinnacle of the Prosecco appellation.',
 'reserve', 'ultra_premium', 'medium-light',
 ARRAY['white peach', 'apple blossom', 'pear', 'honey', 'mineral', 'cream'],
 '{"grape": "Glera", "region": "Cartizze Grand Cru, Valdobbiadene", "method": "Charmat (Martinotti)", "abv": "11.5%", "residual_sugar": "25 g/L", "style": "Prosecco Superiore DOCG Cartizze Dry"}'::jsonb,
 true),

('Ruggeri Giustino B. Extra Brut Valdobbiadene Superiore',
 'wine_sparkling', 'Prosecco Superiore DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Ruggeri'),
 174, 'Italy',
 'Named after founder Giustino Bisol, this Extra Brut (< 6 g/L RS) is a revelation for those who associate Prosecco only with sweetness. From Cartizze-adjacent vineyards in Valdobbiadene, the wine offers: fine mousse, fresh green apple, lemon zest, white pear, and a dry, mineral, almost saline finish. Demonstrates that Glera can produce wine of true gastronomic ambition.',
 'estate', 'premium', 'medium-light',
 ARRAY['green apple', 'lemon zest', 'white pear', 'mineral', 'yeast', 'white flower'],
 '{"grape": "Glera", "region": "Valdobbiadene Superiore DOCG", "method": "Charmat (Martinotti)", "abv": "11.0%", "residual_sugar": "4 g/L", "style": "Prosecco Superiore DOCG Extra Brut"}'::jsonb,
 true),

('Nino Franco Rustico Valdobbiadene Prosecco Superiore',
 'wine_sparkling', 'Prosecco Superiore DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Nino Franco'),
 174, 'Italy',
 'The benchmark accessible Prosecco Superiore — Nino Franco''s Rustico NV from estate and contract Glera vineyards across the Valdobbiadene hills. Extra Dry (17-32 g/L RS), with a generous fine mousse, fresh apple and pear fruit, floral notes, and clean finish. The textbook introduction to quality Prosecco Superiore DOCG. Consistently excellent value.',
 'market', 'mid_range', 'light',
 ARRAY['fresh apple', 'white pear', 'white flower', 'lemon', 'cream'],
 '{"grape": "Glera", "region": "Valdobbiadene, Veneto", "method": "Charmat (Martinotti)", "abv": "11.5%", "residual_sugar": "20 g/L", "style": "Prosecco Superiore DOCG Extra Dry"}'::jsonb,
 true),

('Bisol Crede Valdobbiadene Prosecco Superiore',
 'wine_sparkling', 'Prosecco Superiore DOCG',
 (SELECT id FROM beverage_producers WHERE name = 'Bisol'),
 174, 'Italy',
 'Bisol''s single-vineyard Crede Prosecco — from ''crede'' (clay-rich glacial deposits) soils in the Valdobbiadene hillside. Brut (0-12 g/L RS), with more mineral tension and citrus precision than most Prosecco: fine mousse, white flower, green apple, pear, almond, and a distinctive chalky mineral finish. The wine that proves Prosecco''s terroir can matter as much as any appellation.',
 'estate', 'premium', 'medium-light',
 ARRAY['white flower', 'green apple', 'pear', 'almond', 'mineral', 'citrus'],
 '{"grape": "Glera", "region": "Valdobbiadene, Veneto", "vineyard": "Crede (clay-glacial soils)", "method": "Charmat", "abv": "11.0%", "residual_sugar": "8 g/L", "style": "Prosecco Superiore DOCG Brut"}'::jsonb,
 true);

COMMIT;
