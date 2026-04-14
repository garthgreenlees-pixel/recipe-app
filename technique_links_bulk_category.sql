BEGIN;

-- ============================================================
-- BULK TECHNIQUE LINKS BY CATEGORY AND REGION
-- Uses INSERT ... SELECT to efficiently link all products
-- ON CONFLICT DO NOTHING skips existing links
-- ============================================================

-- ===== UNIVERSAL LINKS: pairing theory + flavour science for ALL products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[1, 2, 71]) AS ref_id) t
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SAKE: all sake products get sake-specific refs =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[5, 30, 47, 79]) AS ref_id) t
WHERE bp.category = 'sake'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SHOCHU/AWAMORI: all shochu products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[140, 38]) AS ref_id) t
WHERE bp.category = 'shochu'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== COFFEE: all coffee products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[7, 21, 46]) AS ref_id) t
WHERE bp.category = 'coffee'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Ethiopian coffee specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 96, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'coffee' AND br.country = 'Ethiopia'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== TEA: all tea products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[31, 72]) AS ref_id) t
WHERE bp.category = 'tea'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Japanese tea (Uji, Shizuoka, Kagoshima, etc.) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[131, 64]) AS ref_id) t
WHERE bp.category = 'tea' AND br.country = 'Japan'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Chinese tea (Yunnan, Fujian, Zhejiang, Guangdong, Guizhou, Sichuan) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 132, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'tea' AND br.country = 'China'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Taiwan tea =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 142, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'tea' AND br.country = 'Taiwan'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Indian tea (Darjeeling, Assam, Nilgiri) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[143, 144]) AS ref_id) t
WHERE bp.category = 'tea' AND br.country = 'India'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== BEER: all beer products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[13, 14, 19, 82]) AS ref_id) t
WHERE bp.category IN ('beer_ale', 'beer_lager', 'wild_beer')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Belgian beer specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 100, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category IN ('beer_ale', 'beer_lager') AND br.country = 'Belgium'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SPIRITS WHISKEY: all whisky products =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[6, 44, 72]) AS ref_id) t
WHERE bp.category = 'spirits_whiskey'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Scotch whisky specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 98, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'spirits_whiskey' AND br.country = 'Scotland'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- American whiskey (Bourbon + Tennessee) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 95, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'spirits_whiskey' AND br.country = 'USA'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SPIRITS LIQUEUR/BRANDY =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[56, 119, 51]) AS ref_id) t
WHERE bp.category IN ('spirits_liqueur', 'spirits_brandy')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Cognac/Armagnac specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[111, 112]) AS ref_id) t
WHERE bp.category = 'spirits_brandy' AND br.country = 'France'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SPIRITS AGAVE: mezcal + tequila =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[61, 99]) AS ref_id) t
WHERE bp.category = 'spirits_agave'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SPIRITS RUM/CLAIRIN =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[94, 38, 51]) AS ref_id) t
WHERE bp.category IN ('spirits_rum', 'spirits_cane')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== SPIRITS GIN =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[20, 51]) AS ref_id) t
WHERE bp.category = 'spirits_gin'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== NA BEVERAGES =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[10, 49, 85]) AS ref_id) t
WHERE bp.category IN ('na_dealcoholised', 'na_crafted', 'na_fermented', 'na_spirit')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Kombucha/fermented NA specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[57, 82, 126]) AS ref_id) t
WHERE bp.category = 'na_fermented'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== TRADITIONAL CULTURAL =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[38, 14, 82]) AS ref_id) t
WHERE bp.category = 'traditional_cultural'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Kava specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 92, bp.id
FROM beverage_products bp
WHERE bp.subcategory IN ('kava_noble', 'kava_powder', 'kava_awa_hawaiian', 'kava_ava_ceremony', 'kava_yaqona')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Lambanog/basi/palm wine =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 93, bp.id
FROM beverage_products bp
WHERE bp.subcategory IN ('lambanog_coconut_spirit', 'basi_sugarcane_wine')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Nigerian palm wine =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 94, bp.id
FROM beverage_products bp
WHERE bp.subcategory = 'palm_wine_fresh'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- ===== WINE STILL: all still wine gets universal wine refs =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[3, 4, 54, 72, 76]) AS ref_id) t
WHERE bp.category = 'wine_still'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- BC wine regions (Canada) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[9, 23, 65]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'Canada'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- WA/OR wine regions (USA PNW) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[9, 24]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'USA'
  AND br.id BETWEEN 20 AND 43
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- WA AVAs specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 75, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'USA'
  AND br.name NOT ILIKE '%Oregon%' AND br.name NOT ILIKE '%Willamette%'
  AND br.name NOT ILIKE '%Chehalem%' AND br.name NOT ILIKE '%Eola%'
  AND br.name NOT ILIKE '%Dundee%' AND br.name NOT ILIKE '%McMinnville%'
  AND br.id BETWEEN 20 AND 43
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Oregon wine regions =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 77, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'USA'
  AND (br.name ILIKE '%Oregon%' OR br.name ILIKE '%Willamette%'
    OR br.name ILIKE '%Chehalem%' OR br.name ILIKE '%Eola%'
    OR br.name ILIKE '%Dundee%' OR br.name ILIKE '%McMinnville%'
    OR br.name ILIKE '%Van Duzer%' OR br.name ILIKE '%Elkton%'
    OR br.name ILIKE '%Applegate%' OR br.name ILIKE '%Rogue%'
    OR br.name ILIKE '%Southern Oregon%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Burgundy wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[86, 87]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'France'
  AND (br.name ILIKE '%Burgundy%' OR br.name ILIKE '%Beaune%'
    OR br.name ILIKE '%Pommard%' OR br.name ILIKE '%Volnay%'
    OR br.name ILIKE '%Meursault%' OR br.name ILIKE '%Chassagne%'
    OR br.name ILIKE '%Vosne%' OR br.name ILIKE '%Vougeot%'
    OR br.name ILIKE '%Morey%' OR br.name ILIKE '%Nuits%'
    OR br.name ILIKE '%Côte de Nuits%' OR br.name ILIKE '%Côte de Beaune%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Bordeaux wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[102, 103]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'France'
  AND (br.name ILIKE '%Bordeaux%' OR br.name ILIKE '%Médoc%'
    OR br.name ILIKE '%Margaux%' OR br.name ILIKE '%Saint-Julien%'
    OR br.name ILIKE '%Saint-Estèphe%' OR br.name ILIKE '%Pauillac%'
    OR br.name ILIKE '%Saint-Émilion%' OR br.name ILIKE '%Pomerol%'
    OR br.name ILIKE '%Fronsac%' OR br.name ILIKE '%Graves%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Rhône wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[104, 105]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'France'
  AND (br.name ILIKE '%Rhône%' OR br.name ILIKE '%Côte-Rôtie%'
    OR br.name ILIKE '%Hermitage%' OR br.name ILIKE '%Condrieu%'
    OR br.name ILIKE '%Gigondas%' OR br.name ILIKE '%Vacqueyras%'
    OR br.name ILIKE '%Tavel%' OR br.name ILIKE '%Châteauneuf%'
    OR br.name ILIKE '%Saint-Joseph%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Loire wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[107, 108]) AS ref_id) t
WHERE bp.category IN ('wine_still', 'wine_sparkling') AND br.country = 'France'
  AND (br.name ILIKE '%Loire%' OR br.name ILIKE '%Sancerre%'
    OR br.name ILIKE '%Pouilly%' OR br.name ILIKE '%Vouvray%'
    OR br.name ILIKE '%Chinon%' OR br.name ILIKE '%Bourgueil%'
    OR br.name ILIKE '%Savennières%' OR br.name ILIKE '%Marne%'
    OR br.name ILIKE '%Muscadet%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Alsace wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[109, 110]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'France'
  AND br.name ILIKE '%Alsace%'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- French Champagne/sparkling =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[62, 106]) AS ref_id) t
WHERE bp.category = 'wine_sparkling' AND br.country = 'France'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Italian Piedmont wines (Barolo, Barbaresco, Gavi, Barbera) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[114, 115, 129]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'Italy'
  AND (br.name ILIKE '%Piedmont%' OR br.name ILIKE '%Barolo%'
    OR br.name ILIKE '%Barbaresco%' OR br.name ILIKE '%Gavi%'
    OR br.name ILIKE '%Asti%' OR br.name ILIKE '%Alba%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Italian Tuscany wines (Super Tuscans, Brunello, Vernaccia, Vino Nobile) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[116, 117, 133]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'Italy'
  AND (br.name ILIKE '%Tuscany%' OR br.name ILIKE '%Montalcino%'
    OR br.name ILIKE '%Montepulciano%' OR br.name ILIKE '%San Gimignano%'
    OR br.name ILIKE '%Chianti%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Italian Veneto wines (Soave, Amarone, Prosecco, Valpolicella) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[118]) AS ref_id) t
WHERE bp.category IN ('wine_still', 'wine_sparkling') AND br.country = 'Italy'
  AND (br.name ILIKE '%Veneto%' OR br.name ILIKE '%Soave%'
    OR br.name ILIKE '%Valpolicella%' OR br.name ILIKE '%Prosecco%'
    OR br.name ILIKE '%Valdobbiadene%')
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Italian Asti Spumante/Moscato =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[62, 129]) AS ref_id) t
WHERE bp.category = 'wine_sparkling' AND br.country = 'Italy'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Spanish wines (Rioja, Priorat, Jerez) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[121, 130]) AS ref_id) t
WHERE bp.category IN ('wine_still', 'wine_fortified') AND br.country = 'Spain'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Spanish Sherry specifically =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[63, 120]) AS ref_id) t
WHERE bp.category = 'wine_fortified'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Greek wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 134, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'Greece'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Lebanese wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[38, 76]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'Lebanon'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Australian wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 122, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'Australia'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- New Zealand wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 123, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'New Zealand'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- South African wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 124, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'South Africa'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Argentine wines =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
CROSS JOIN (SELECT unnest(ARRAY[54, 76]) AS ref_id) t
WHERE bp.category = 'wine_still' AND br.country = 'Argentina'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Napa Valley wines (USA wine non-PNW) =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT 97, bp.id
FROM beverage_products bp
JOIN beverage_regions br ON br.id = bp.region_id
WHERE bp.category = 'wine_still' AND br.country = 'USA'
  AND br.name ILIKE '%Napa%'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Wine sparkling: all sparkling wine gets sparkling refs =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[62, 72]) AS ref_id) t
WHERE bp.category = 'wine_sparkling'
ON CONFLICT (technique_id, product_id) DO NOTHING;

-- Cellar-worthy premium wines get cellar management refs =====
INSERT INTO beverage_technique_products (technique_id, product_id)
SELECT t.ref_id, bp.id
FROM beverage_products bp
CROSS JOIN (SELECT unnest(ARRAY[36, 59, 78]) AS ref_id) t
WHERE bp.category = 'wine_still' AND bp.quality_tier IN ('reserve', 'estate')
ON CONFLICT (technique_id, product_id) DO NOTHING;

COMMIT;
