-- France Phase 1c: Pairing backfill — Loire (299-306) + Alsace (307-316) + French Spirits (317-324)
-- All 1-pairing products: +4 each; all 2-pairing products: +3 each

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 299: Dagueneau Pouilly-Fumé Silex (2; need 3 more)
-- The flint Pouilly-Fumé; intense mineral, white flower, citrus
-- ============================================================
(299, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Silex — from the silex (flint) soils of St-Andelain; extraordinary white flower, citrus, and flint minerality; the most mineral expression of Sauvignon Blanc in the Loire',
 'seafood', 'salty_mineral', 'Fines de claires oysters with lemon and red wine mignonette — the most classic Sauvignon Blanc-oyster pairing at its finest level',
 'complement', 'Dagueneau Silex''s flint mineral character and the oyster''s brine-iodine create one of the world''s most rational pairings; the wine''s lemon-white flower provides the aromatic framework around the oyster''s minerality', 'aperitif', 'classic', 1, true),

(299, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Silex — from the silex (flint) soils of St-Andelain; extraordinary white flower, citrus, and flint minerality; the most mineral expression of Sauvignon Blanc in the Loire',
 'charcuterie_cheese', 'fermented_aged', 'Crottin de Chavignol AOP (3-week) with honey — the Sancerre goat cheese (15km from Pouilly) paired with its neighbouring wine',
 'complement', 'Crottin de Chavignol and Pouilly-Fumé is one of the world''s great regional food-wine pairings; the goat milk''s lactic tang and the Silex''s flint-citrus create complementary tension', 'cheese', 'classic', 1, true),

(299, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Silex — from the silex (flint) soils of St-Andelain; extraordinary white flower, citrus, and flint minerality; the most mineral expression of Sauvignon Blanc in the Loire',
 'seafood', 'delicate_fresh', 'Pike quenelles de brochet in Nantua sauce — the classic Loire Valley preparation of the river fish found in the same waters as the vineyards',
 'complement', 'Brochet (pike) from the Loire River and Pouilly-Fumé from the Loire''s vineyards are born in the same valley; the Nantua cream-crayfish sauce bridges the wine''s acidity while the fish''s delicacy matches its precision', 'main', 'classic', 1, true),

-- ============================================================
-- 300: Dagueneau Pouilly-Fumé Pur Sang (2; need 3 more)
-- More citrus-driven than Silex; white peach, floral
-- ============================================================
(300, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Pur Sang — from limestone soils; more citrus and floral than Silex; white peach, citrus blossom, pure Sauvignon Blanc character; extraordinary precision',
 'seafood', 'delicate_fresh', 'Sole meunière with lemon and capers — the Loire Valley preparation of the coastal flatfish with Dagueneau''s precision white',
 'complement', 'Pur Sang''s citrus blossom and white peach character are perfectly proportioned for sole meunière''s lemon-butter preparation; the wine''s precision mirrors the simplicity of the preparation', 'main', 'established', 1, true),

(300, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Pur Sang — from limestone soils; more citrus and floral than Silex; white peach, citrus blossom, pure Sauvignon Blanc character; extraordinary precision',
 'vegetables_legumes', 'delicate_fresh', 'Asperges blanches de la Sarthe with sauce mousseline — white asparagus from the Loire Valley with Pur Sang''s precision',
 'complement', 'Loire Valley white asparagus and Pur Sang are both products of the same limestone-rich valley; the asparagus''s vegetal-bitter character is bridged by the wine''s citrus while the mousseline''s richness finds its counterpoint', 'starter', 'classic', 1, true),

(300, 'wine_still', 'Pouilly-Fumé AOC', 'Didier Dagueneau Pouilly-Fumé Pur Sang — from limestone soils; more citrus and floral than Silex; white peach, citrus blossom, pure Sauvignon Blanc character; extraordinary precision',
 'charcuterie_cheese', 'fermented_aged', 'Chèvre frais (fresh goat''s cheese) with chives and lemon zest — the Loire''s most accessible goat preparation for the most accessible Dagueneau wine',
 'complement', 'Fresh goat''s cheese and Pur Sang is the classic Loire pairing; the wine''s citrus-blossom character lifts the cheese''s lactic freshness; chives add a green-herb bridge to the Sauvignon Blanc', 'aperitif', 'classic', 1, true),

-- ============================================================
-- 301: Huet Vouvray Le Mont Sec (2; need 3 more)
-- Dry Vouvray Chenin Blanc; mineral, quince, honeysuckle
-- ============================================================
(301, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Le Mont Sec — dry Vouvray Chenin Blanc from the Le Mont vineyard; mineral, quince, honeysuckle, and extraordinary aging potential; one of the Loire''s most serious dry whites',
 'seafood', 'delicate_fresh', 'Sandre de Loire (Loire River pike-perch) with beurre blanc and herbs — the classic Loire preparation of its freshwater fish',
 'complement', 'Sandre du Loire and Vouvray beurre blanc is the most regional possible preparation; the wine''s quince-mineral character provides the aromatic framework for the fish''s delicacy; beurre blanc''s butter bridges the wine''s richness', 'main', 'classic', 1, true),

(301, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Le Mont Sec — dry Vouvray Chenin Blanc from the Le Mont vineyard; mineral, quince, honeysuckle, and extraordinary aging potential; one of the Loire''s most serious dry whites',
 'meat_poultry', 'earthy_herbal', 'Rillettes de Tours (slow-cooked pork confit spread) with gherkins and Touraine bread — the famous Loire charcuterie for a Touraine white wine',
 'complement', 'Rillettes de Tours is the Loire''s most celebrated charcuterie preparation; the fatty pork confit and the wine''s acidity are a classic Loire pairing, cutting through the fat while the quince note adds complexity', 'aperitif', 'classic', 1, true),

(301, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Le Mont Sec — dry Vouvray Chenin Blanc from the Le Mont vineyard; mineral, quince, honeysuckle, and extraordinary aging potential; one of the Loire''s most serious dry whites',
 'meat_poultry', 'delicate_fresh', 'Poulet des Landes rôti avec champignons and sauce Vouvray — the Landes chicken in the simple Vouvray wine sauce preparation',
 'complement', 'Cooking with Vouvray and serving the same wine creates seamless integration; the chicken''s fat and the mushroom''s earthiness bridge the wine''s quince-mineral character', 'main', 'established', 1, true),

-- ============================================================
-- 302: Huet Vouvray Clos du Bourg Demi-Sec (2; need 3 more)
-- Off-dry Vouvray; quince, honey, mineral; versatile food wine
-- ============================================================
(302, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Clos du Bourg Demi-Sec — off-dry (15-25 g/L RS) from the Clos du Bourg monopole; quince, honey, mineral, extraordinary acidity balancing the sweetness; 20+ year aging',
 'meat_poultry', 'sweet_spiced', 'Foie gras de canard en terrine with Vouvray jelly and brioche — the demi-sec''s off-dry character is traditionally paired with foie gras in the Loire Valley',
 'complement', 'Vouvray demi-sec and foie gras is a classic Loire pairing: the wine''s off-dry sweetness enhances the foie gras''s fat without overwhelming it; the quince note bridges the terrine''s fruit accompaniment', 'starter', 'classic', 1, true),

(302, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Clos du Bourg Demi-Sec — off-dry (15-25 g/L RS) from the Clos du Bourg monopole; quince, honey, mineral, extraordinary acidity balancing the sweetness; 20+ year aging',
 'dessert_pastry', 'sweet_fruity', 'Tarte tatin aux poires (pear tarte tatin) — the off-dry wine''s quince-honey mirrors the caramelised pear preparation',
 'complement', 'Quince in the wine and caramelised pear in the tart share the same stone-fruit family; the demi-sec''s acidity prevents the pairing from becoming cloying while its mineral depth provides structure', 'dessert', 'classic', 1, true),

(302, 'wine_still', 'Vouvray AOC', 'Gaston Huet Vouvray Clos du Bourg Demi-Sec — off-dry (15-25 g/L RS) from the Clos du Bourg monopole; quince, honey, mineral, extraordinary acidity balancing the sweetness; 20+ year aging',
 'charcuterie_cheese', 'sweet_salty', 'Époisses de Bourgogne AOP with quince paste — the pungent washed-rind and the off-dry Vouvray create a classic sweet-savoury cheese pairing',
 'contrast', 'Demi-sec Vouvray and a pungent washed-rind cheese is a classic French contrast pairing: the wine''s sweetness tames the cheese''s pungency while its acidity lifts the fat; quince paste bridges both', 'cheese', 'established', 1, true),

-- ============================================================
-- 303: Coulée de Serrant Nicolas Joly (2; need 3 more)
-- Biodynamic Chenin; oxidative, intense, complex, polarising
-- ============================================================
(303, 'wine_still', 'Savennières AOC', 'Coulée de Serrant Nicolas Joly — the biodynamic 7ha monopole in Savennières; Chenin Blanc of extraordinary intensity and sometimes polarising oxidative character; quince, honey, wax, mineral, spice',
 'seafood', 'umami_savoury', 'Rillettes de saumon de Loire (Loire salmon rillettes) — the freshwater salmon spread, a Loire Valley classic with the region''s most intense Chenin',
 'complement', 'Coulée de Serrant''s intensity and Loire salmon rillettes share the same river terroir; the wine''s quince-wax character cuts through the fatty spread while mineral acidity lifts the fish', 'starter', 'established', 1, true),

(303, 'wine_still', 'Savennières AOC', 'Coulée de Serrant Nicolas Joly — the biodynamic 7ha monopole in Savennières; Chenin Blanc of extraordinary intensity and sometimes polarising oxidative character; quince, honey, wax, mineral, spice',
 'meat_poultry', 'delicate_fresh', 'Volaille pochée au bouillon avec légumes d''hiver (poached chicken in winter vegetable broth) — the purity of a simple braise for a wine of complex intensity',
 'bridge', 'Coulée de Serrant''s biodynamic intensity and the poached chicken''s purity create a bridge between power and simplicity; the root vegetables'' earthy sweetness bridges the wine''s honey-quince', 'main', 'suggested', 1, true),

(303, 'wine_still', 'Savennières AOC', 'Coulée de Serrant Nicolas Joly — the biodynamic 7ha monopole in Savennières; Chenin Blanc of extraordinary intensity and sometimes polarising oxidative character; quince, honey, wax, mineral, spice',
 'charcuterie_cheese', 'fermented_aged', 'Sainte-Maure de Touraine AOP (log-shaped goat''s cheese with straw, 4-week) — the Loire''s most distinctive goat''s cheese for its most distinctive Chenin',
 'complement', 'Sainte-Maure de Touraine''s distinctive goat-milk tang and the wine''s honey-quince create a classic Loire pairing; the straw''s earthy note bridges Joly''s biodynamic terroir character', 'cheese', 'classic', 1, true),

-- ============================================================
-- 304: Cotat Sancerre Les Monts Damnés (2; need 3 more)
-- Old-vine Sancerre; mineral, citrus, mineral precision
-- ============================================================
(304, 'wine_still', 'Sancerre AOC', 'Domaine Cotat Sancerre Les Monts Damnés — from the most celebrated vineyard in Sancerre; old-vine Sauvignon Blanc of extraordinary mineral precision; citrus, white currant, flint; requires 5+ years',
 'charcuterie_cheese', 'fermented_aged', 'Crottin de Chavignol AOP (4-week, slightly aged) — the town of Chavignol is within the Sancerre appellation; this is the most direct terroir cheese pairing in France',
 'complement', 'Chavignol is a hamlet within the Sancerre AOC; Crottin de Chavignol and Sancerre share the same commune''s limestone soils; the goat milk''s lactic precision and the wine''s flint-citrus are natural equals', 'cheese', 'classic', 1, true),

(304, 'wine_still', 'Sancerre AOC', 'Domaine Cotat Sancerre Les Monts Damnés — from the most celebrated vineyard in Sancerre; old-vine Sauvignon Blanc of extraordinary mineral precision; citrus, white currant, flint; requires 5+ years',
 'seafood', 'salty_mineral', 'Plateau de fruits de mer (oysters, langoustines, clams, whelks, shrimp) — Sancerre and a seafood plateau is a classic Loire Valley restaurant tradition',
 'complement', 'Les Monts Damnés'' mineral precision and the seafood plateau''s multiplied briny-iodine intensity create a pairing of accumulating complexity; the wine''s acidity refreshes between different species', 'main', 'classic', 1, true),

(304, 'wine_still', 'Sancerre AOC', 'Domaine Cotat Sancerre Les Monts Damnés — from the most celebrated vineyard in Sancerre; old-vine Sauvignon Blanc of extraordinary mineral precision; citrus, white currant, flint; requires 5+ years',
 'seafood', 'delicate_fresh', 'Gravlax de saumon de Loire with dill cream and pickled cucumber — the preserved salmon preparation for Loire''s great mineral Sauvignon',
 'complement', 'Gravlax''s cured salmon-dill-citrus combination bridges with Les Monts Damnés''s white currant-citrus-flint; the dill''s herb echoes the Sauvignon Blanc''s herbal character', 'starter', 'established', 1, true),

-- ============================================================
-- 305: Vacheron Sancerre Les Romains (2; need 3 more)
-- Biodynamic Sancerre; fresh, herbal, mineral
-- ============================================================
(305, 'wine_still', 'Sancerre AOC', 'Domaine Vacheron Sancerre Les Romains — biodynamic Sancerre from the limestone-clay Les Romains vineyard; fresh gooseberry, white flower, mineral, herbal; more accessible style than Cotat',
 'vegetables_legumes', 'bitter_astringent', 'Taboulé de légumes printaniers (spring vegetable tabbouleh with herbs) — the herbal-fresh character of Vacheron''s Sancerre bridges with the herb-dominated salad',
 'complement', 'Vacheron''s herbal Sauvignon Blanc character (gooseberry, green herb) resonates with tabbouleh''s parsley-mint-lemon; the biodynamic viticulture creates a green-herb intensity that bridges perfectly', 'starter', 'established', 1, true),

(305, 'wine_still', 'Sancerre AOC', 'Domaine Vacheron Sancerre Les Romains — biodynamic Sancerre from the limestone-clay Les Romains vineyard; fresh gooseberry, white flower, mineral, herbal; more accessible style than Cotat',
 'seafood', 'delicate_fresh', 'Truite de rivière à la meunière (river trout) — the Loire''s fresh river fish for a Sauvignon Blanc of mineral precision',
 'complement', 'River trout from the Loire tributaries and Sancerre from the Loire''s vineyards share a terroir context; the fish''s delicacy and the wine''s herbal-mineral are perfectly proportioned', 'main', 'classic', 1, true),

(305, 'wine_still', 'Sancerre AOC', 'Domaine Vacheron Sancerre Les Romains — biodynamic Sancerre from the limestone-clay Les Romains vineyard; fresh gooseberry, white flower, mineral, herbal; more accessible style than Cotat',
 'charcuterie_cheese', 'fermented_aged', 'Fromage de chèvre de la Loire (fresh-to-semi-aged) — any of the Loire''s goat cheeses with Sancerre is a classic pairing; this is the regional standard',
 'complement', 'Loire goat''s cheese and Sancerre Sauvignon Blanc is arguably the world''s most consistent food-wine match; the goat milk''s lactic tang and the Sauvignon''s citrus-mineral are complementary rather than competing', 'cheese', 'classic', 1, true),

-- ============================================================
-- 306: Pépière Muscadet Sèvre et Maine Clisson (2; need 3 more)
-- Top Muscadet; ultra-mineral, saline, sur lie; better than its reputation
-- ============================================================
(306, 'wine_still', 'Muscadet Sèvre et Maine AOC', 'Domaine de la Pépière Muscadet Clisson — the cru Communal of Muscadet; granite soils give remarkable mineral depth; saline, lemon zest, brioche (sur lie), extraordinary structure for the appellation',
 'seafood', 'salty_mineral', 'Huîtres de Bretagne (Breton oysters, fine de claires) with muscadet mignonette — the Loire estuary oyster for the Loire estuary wine',
 'complement', 'Muscadet and Breton oysters is the Atlantic-coast food-wine pairing par excellence; Clisson''s granite mineral character mirrors the oyster''s granite-influenced iodine; the estuary wine matches the estuary oysters', 'aperitif', 'classic', 1, true),

(306, 'wine_still', 'Muscadet Sèvre et Maine AOC', 'Domaine de la Pépière Muscadet Clisson — the cru Communal of Muscadet; granite soils give remarkable mineral depth; saline, lemon zest, brioche (sur lie), extraordinary structure for the appellation',
 'seafood', 'delicate_fresh', 'Moules marinières de Vendée (Vendée mussels in white wine, shallots, parsley) — the most traditional preparation of the Atlantic coast mussels',
 'complement', 'Moules marinières cooked with the wine serving alongside creates the most seamless wine-food continuity; Muscadet''s saline-lemon character perfectly mirrors the mussel''s brine and the shallot-parsley preparation', 'main', 'classic', 1, true),

(306, 'wine_still', 'Muscadet Sèvre et Maine AOC', 'Domaine de la Pépière Muscadet Clisson — the cru Communal of Muscadet; granite soils give remarkable mineral depth; saline, lemon zest, brioche (sur lie), extraordinary structure for the appellation',
 'seafood', 'salty_mineral', 'Sardines fraîches grillées au sel avec câpres (freshly grilled sardines) — the simplest Atlantic fish preparation for the Atlantic coast''s white wine',
 'complement', 'Clisson Muscadet''s granite-saline character was made for fresh grilled sardines; the fish''s oiliness is cut by the wine''s lemon-mineral acidity; capers'' salt-acid bridges the wine''s saline character', 'main', 'established', 1, true),

-- ============================================================
-- 307: Trimbach Clos Sainte-Hune Riesling (1; need 4 more)
-- The benchmark Alsace Riesling; extraordinary mineral aging
-- ============================================================
(307, 'wine_still', 'Alsace Grand Cru', 'Trimbach Clos Sainte-Hune — the benchmark Alsace Riesling from a 1.67ha monopole in the Rosacker Grand Cru; extraordinary mineral depth, lime zest, petrol, mineral; requires 10-15 years minimum',
 'seafood', 'delicate_fresh', 'Truite au bleu (live-killed trout poached blue with vinegar) with beurre blanc — the classic Alsatian preparation of the Ill River trout',
 'complement', 'Truite au bleu is an Alsatian tradition; the river trout''s delicacy and the beurre blanc''s butter-acid bridge Clos Sainte-Hune''s mineral-lime; both speak of the same Alsatian river landscape', 'main', 'classic', 1, true),

(307, 'wine_still', 'Alsace Grand Cru', 'Trimbach Clos Sainte-Hune — the benchmark Alsace Riesling from a 1.67ha monopole in the Rosacker Grand Cru; extraordinary mineral depth, lime zest, petrol, mineral; requires 10-15 years minimum',
 'meat_poultry', 'earthy_herbal', 'Choucroute garnie (braised sauerkraut with pork, sausages, and Riesling) — Alsace''s most celebrated dish, prepared with the same grape variety as the drinking wine',
 'complement', 'Choucroute garnie cooked in Riesling and served alongside Clos Sainte-Hune is the apex of Alsatian food culture; the sauerkraut''s fermented acid mirrors the wine''s mineral acidity; the pork fat provides the bridge', 'main', 'classic', 1, true),

(307, 'wine_still', 'Alsace Grand Cru', 'Trimbach Clos Sainte-Hune — the benchmark Alsace Riesling from a 1.67ha monopole in the Rosacker Grand Cru; extraordinary mineral depth, lime zest, petrol, mineral; requires 10-15 years minimum',
 'charcuterie_cheese', 'fermented_aged', 'Munster AOP (Alsatian washed-rind, 3-week farm-produced) with caraway seeds — the Alsatian tradition of serving Munster with caraway seeds and Riesling',
 'complement', 'Munster and Riesling is the definitive Alsatian cheese-wine pairing: the strong washed-rind''s pungency requires a wine of Riesling''s mineral power; caraway seeds bridge the wine''s aromatics', 'cheese', 'classic', 1, true),

(307, 'wine_still', 'Alsace Grand Cru', 'Trimbach Clos Sainte-Hune — the benchmark Alsace Riesling from a 1.67ha monopole in the Rosacker Grand Cru; extraordinary mineral depth, lime zest, petrol, mineral; requires 10-15 years minimum',
 'seafood', 'umami_savoury', 'Homard à l''Alsacienne (lobster in Riesling and cream with chervil) — the Alsatian preparation of lobster using the region''s white wine as both cooking and drinking wine',
 'complement', 'Homard à l''Alsacienne uses Riesling in the sauce and is one of the finest regional wine-dish pairings; serving Clos Sainte-Hune alongside creates a three-tier Riesling experience: wine in sauce, wine in glass, wine in memory', 'main', 'classic', 1, true),

-- ============================================================
-- 308: Trimbach Cuvée Frédéric Émile Riesling (2; need 3 more)
-- From premier crus Osterberg and Geisberg; more accessible than CSH
-- ============================================================
(308, 'wine_still', 'Alsace AOC', 'Trimbach Riesling Cuvée Frédéric Émile — from Osterberg and Geisberg premier crus; more citrus-driven and accessible than Clos Sainte-Hune; lime, mineral, slate; requires 8+ years',
 'seafood', 'delicate_fresh', 'Tarte flambée (flammekueche) with crème fraîche, bacon, and onions — the Alsatian flatbread tart for a classic Alsace Riesling',
 'complement', 'Tarte flambée and Alsace Riesling is the quintessential regional aperitivo pairing: the crème fraîche''s acidity and the bacon''s salt are structured by Frédéric Émile''s mineral acidity', 'aperitif', 'classic', 2, true),

(308, 'wine_still', 'Alsace AOC', 'Trimbach Riesling Cuvée Frédéric Émile — from Osterberg and Geisberg premier crus; more citrus-driven and accessible than Clos Sainte-Hune; lime, mineral, slate; requires 8+ years',
 'seafood', 'umami_savoury', 'Quiche Lorraine (egg-bacon-Gruyère tart) — the Alsace-Lorraine border preparation for an Alsace Riesling',
 'complement', 'Quiche Lorraine''s cream-egg-bacon richness requires a wine of mineral acidity to cut through; Frédéric Émile''s lime-slate precision is perfectly proportioned for the quiche''s richness', 'main', 'classic', 2, true),

(308, 'wine_still', 'Alsace AOC', 'Trimbach Riesling Cuvée Frédéric Émile — from Osterberg and Geisberg premier crus; more citrus-driven and accessible than Clos Sainte-Hune; lime, mineral, slate; requires 8+ years',
 'meat_poultry', 'earthy_herbal', 'Baeckeoffe (Alsatian lamb, beef, and pork pot-baked with Riesling, vegetables, and herbs) — the Alsatian baker''s oven preparation using the same wine in the dish',
 'complement', 'Baeckeoffe traditionally uses Riesling in the slow-bake; serving Frédéric Émile alongside creates the classic Alsatian food-wine loop; the dish''s richness finds perfect counterpart in the wine''s acidity', 'main', 'classic', 2, true),

-- ============================================================
-- 309: Zind-Humbrecht Riesling Clos Windsbuhl (1; need 4 more)
-- Volcanic Vosgian sandstone Riesling; more voluptuous than limestone
-- ============================================================
(309, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Riesling Clos Windsbuhl — from volcanic Vosgian sandstone; more voluptuous and floral than limestone Riesling; orange blossom, lime, white peach; biodynamic from Olivier Humbrecht MW',
 'seafood', 'delicate_fresh', 'Saint-Pierre (John Dory) rôti avec fenouil et citron — the Alsatian preparation of the Mediterranean fish with fennel, for a Riesling of unusual floral depth',
 'complement', 'ZH Windsbuhl''s voluptuous florality and the John Dory''s lean-firm texture are in counterpoint; fennel''s anise note bridges the wine''s orange blossom while lemon sharpens its citrus', 'main', 'established', 1, true),

(309, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Riesling Clos Windsbuhl — from volcanic Vosgian sandstone; more voluptuous and floral than limestone Riesling; orange blossom, lime, white peach; biodynamic from Olivier Humbrecht MW',
 'meat_poultry', 'earthy_herbal', 'Poulet rôti au citron confit et herbes avec riz pilaf — the herbed lemon chicken for a floral Riesling',
 'complement', 'Windsbuhl''s orange blossom and lime create a citrus-floral character that bridges with preserved lemon and herb roasted chicken; the biodynamic farming amplifies the herbal notes in both', 'main', 'suggested', 1, true),

(309, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Riesling Clos Windsbuhl — from volcanic Vosgian sandstone; more voluptuous and floral than limestone Riesling; orange blossom, lime, white peach; biodynamic from Olivier Humbrecht MW',
 'charcuterie_cheese', 'fermented_aged', 'Munster au lait cru (raw milk Munster from Orbey) with caraway — the finest Munster with a Riesling of unusual depth',
 'complement', 'ZH Windsbuhl''s unusual florality creates a different Munster-Riesling dynamic: the wine''s white peach bridges the cheese''s cream while the orange blossom amplifies the caraway''s aromatic character', 'cheese', 'established', 1, true),

(309, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Riesling Clos Windsbuhl — from volcanic Vosgian sandstone; more voluptuous and floral than limestone Riesling; orange blossom, lime, white peach; biodynamic from Olivier Humbrecht MW',
 'seafood', 'umami_savoury', 'Poulpe confit à basse température avec écrasé de pommes de terre et herbes — slow-cooked octopus with potato and herbs for a wine of volcanic mineral depth',
 'complement', 'Windsbuhl''s volcanic mineral character is uniquely suited for octopus''s mineral-sea depth; the potato''s earthiness bridges the wine''s floral-volcanic character; a sophisticated cross-regional pairing', 'main', 'adventurous', 1, true),

-- ============================================================
-- 310: Zind-Humbrecht Pinot Gris Hengst Grand Cru (1; need 4 more)
-- Rich, smoky, complex Pinot Gris; the ''red wine'' of Alsace whites
-- ============================================================
(310, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Pinot Gris Hengst Grand Cru — biodynamic Pinot Gris from the Wintzenheim Grand Cru; smoky, rich, peach, honey, complex spice; the most food-versatile Alsatian wine',
 'meat_poultry', 'rich_fatty_smoky', 'Foie gras de canard poêlé avec compote de mirabelles (seared foie gras with Mirabelle plum compote) — Alsace''s famous mirabelle plum from the same region as the wine',
 'complement', 'Pinot Gris Hengst''s smoke-honey and the foie gras''s fat create a rich pairing; Mirabelle plum''s tart sweetness provides the essential acid contrast; biodynamic farming amplifies the fruit''s precision', 'starter', 'classic', 1, true),

(310, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Pinot Gris Hengst Grand Cru — biodynamic Pinot Gris from the Wintzenheim Grand Cru; smoky, rich, peach, honey, complex spice; the most food-versatile Alsatian wine',
 'meat_poultry', 'earthy_herbal', 'Cochon de lait à l''alsacienne (Alsatian roast suckling pig with sauerkraut and beer sauce) — the most traditional Alsatian pork preparation for the region''s richest white',
 'complement', 'Pinot Gris''s smoke and body handle pork fat with unusual ease among white wines; suckling pig''s roasted skin and the sauerkraut''s acid bridge the wine''s honey-smoke character', 'main', 'classic', 1, true),

(310, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Pinot Gris Hengst Grand Cru — biodynamic Pinot Gris from the Wintzenheim Grand Cru; smoky, rich, peach, honey, complex spice; the most food-versatile Alsatian wine',
 'charcuterie_cheese', 'fermented_aged', 'Colmar-style Munster with black pepper and caraway — Pinot Gris and Munster is an Alsatian alternative to the classic Riesling pairing',
 'complement', 'Pinot Gris Hengst''s smoke and body can handle Munster''s pungency through power rather than mineral acidity; the wine''s peach-honey provides a sweet counterpoint to the cheese''s salt', 'cheese', 'suggested', 1, true),

(310, 'wine_still', 'Alsace Grand Cru', 'Zind-Humbrecht Pinot Gris Hengst Grand Cru — biodynamic Pinot Gris from the Wintzenheim Grand Cru; smoky, rich, peach, honey, complex spice; the most food-versatile Alsatian wine',
 'seafood', 'umami_savoury', 'Terrine de foie gras au Pinot Gris et gelée de Mirabelle — Alsatian foie gras terrine prepared with the wine as cooking liquid',
 'complement', 'Preparing foie gras terrine with Pinot Gris and serving the same wine creates the quintessential Alsatian first course pairing; Mirabelle jelly bridges the wine''s stone fruit character and the terrine''s richness', 'starter', 'classic', 1, true),

-- ============================================================
-- 311: Weinbach Riesling Schlossberg Grand Cru Sainte-Catherine (1; need 4 more)
-- Granite Riesling; citrus, mineral, floral; Colette Faller's masterpiece
-- ============================================================
(311, 'wine_still', 'Alsace Grand Cru', 'Domaine Weinbach Riesling Schlossberg Sainte-Catherine — from the granite Schlossberg Grand Cru; extraordinary citrus-mineral precision, lime, white flower; Colette and Catherine Faller''s benchmark wine',
 'seafood', 'salty_mineral', 'Brochets du Rhin farcis au Riesling (Rhine pike stuffed with herbs and Riesling) — the historic preparation of the Rhine''s freshwater fish with Alsace Riesling',
 'complement', 'Rhine pike and Alsace Riesling is the most regional possible pairing; the fish''s firm texture and delicate flavour are bridged by the wine''s citrus precision; the stuffed preparation mirrors the wine''s complexity', 'main', 'classic', 1, true),

(311, 'wine_still', 'Alsace Grand Cru', 'Domaine Weinbach Riesling Schlossberg Sainte-Catherine — from the granite Schlossberg Grand Cru; extraordinary citrus-mineral precision, lime, white flower; Colette and Catherine Faller''s benchmark wine',
 'seafood', 'delicate_fresh', 'Assiette de crustacés (langoustines, crab, crevettes grises) with Schlossberg vinaigrette — using the wine in the dressing for the shellfish platter',
 'complement', 'Schlossberg''s granite-mineral and lime character creates a vinaigrette that bridges the shellfish platter''s varied flavours; serving the same wine amplifies the terroir expression', 'main', 'established', 1, true),

(311, 'wine_still', 'Alsace Grand Cru', 'Domaine Weinbach Riesling Schlossberg Sainte-Catherine — from the granite Schlossberg Grand Cru; extraordinary citrus-mineral precision, lime, white flower; Colette and Catherine Faller''s benchmark wine',
 'meat_poultry', 'earthy_herbal', 'Blanquette de veau à l''alsacienne with mushrooms and cream — the rich cream-veal stew for a Riesling of mineral power',
 'complement', 'Blanquette de veau''s cream-mushroom richness is cut by Schlossberg''s mineral acidity; the wine''s white flower adds an aromatic dimension that lifts the cream sauce''s potential heaviness', 'main', 'classic', 1, true),

(311, 'wine_still', 'Alsace Grand Cru', 'Domaine Weinbach Riesling Schlossberg Sainte-Catherine — from the granite Schlossberg Grand Cru; extraordinary citrus-mineral precision, lime, white flower; Colette and Catherine Faller''s benchmark wine',
 'charcuterie_cheese', 'fermented_aged', 'Chaource (Champagne soft cheese) with preserved lemon and white truffle honey — a cross-border cheese pairing for a wine of exceptional precision',
 'complement', 'Chaource''s delicate white mould cream is proportioned to Schlossberg''s precision; preserved lemon bridges the wine''s citrus while white truffle honey adds depth for a more complex experience', 'cheese', 'suggested', 1, true),

-- ============================================================
-- 312: Hugel Riesling Jubilee (1; need 4 more)
-- Premier cru Riesling; mature, textured, accessible
-- ============================================================
(312, 'wine_still', 'Alsace AOC', 'Hugel Riesling Jubilee — from premier cru parcels including Schoenenbourg; the most accessible expression of serious Alsace Riesling; lime, mineral, petrol notes with age; approachable',
 'seafood', 'delicate_fresh', 'Filet de sandre avec crème de ciboulette et Riesling — Loire pike-perch fillet with chive cream and Riesling-based sauce',
 'complement', 'Hugel Jubilee''s accessibility makes it the ideal everyday-luxury pairing wine; chive cream bridges Riesling''s herbal note while sandre''s delicate texture is perfectly proportioned for the wine''s approachable mineral', 'main', 'classic', 2, true),

(312, 'wine_still', 'Alsace AOC', 'Hugel Riesling Jubilee — from premier cru parcels including Schoenenbourg; the most accessible expression of serious Alsace Riesling; lime, mineral, petrol notes with age; approachable',
 'meat_poultry', 'earthy_herbal', 'Knepfles (Alsatian dumplings) with cream and smoked bacon — the Alsatian comfort pasta preparation for an approachable Riesling',
 'complement', 'Knepfles'' smoked bacon-cream richness and Jubilee''s mineral precision are a classic Alsatian comfort pairing; the dumplings'' wheat and the wine''s mineral provide a simple but effective bridge', 'main', 'established', 2, true),

(312, 'wine_still', 'Alsace AOC', 'Hugel Riesling Jubilee — from premier cru parcels including Schoenenbourg; the most accessible expression of serious Alsace Riesling; lime, mineral, petrol notes with age; approachable',
 'meat_poultry', 'delicate_fresh', 'Poulet fermier au Riesling (farm chicken in Riesling sauce with mushrooms and cream) — the Alsatian classic that uses the wine in the sauce',
 'complement', 'Poulet au Riesling is one of Alsace''s most celebrated dishes; using and serving Jubilee creates the classic Alsatian wine-food circle; the cream-mushroom sauce mirrors the wine''s own cream notes', 'main', 'classic', 2, true),

(312, 'wine_still', 'Alsace AOC', 'Hugel Riesling Jubilee — from premier cru parcels including Schoenenbourg; the most accessible expression of serious Alsace Riesling; lime, mineral, petrol notes with age; approachable',
 'charcuterie_cheese', 'fermented_aged', 'Carré de l''Est (Lorraine soft washed-rind) with crusty Kougelhopf bread — the Lorraine-Alsace border cheese for the border wine',
 'complement', 'Carré de l''Est is a gentler washed-rind from Alsace-Lorraine that bridges to Hugel''s more accessible Riesling; Kougelhopf''s butter-almond bread bridges the wine''s mineral depth', 'cheese', 'suggested', 2, true),

-- ============================================================
-- 313: Hugel Riesling Vendange Tardive (1; need 4 more)
-- Late harvest; off-dry to sweet; honey, apricot, mineral
-- ============================================================
(313, 'wine_dessert', 'Alsace Vendange Tardive', 'Hugel Riesling Vendange Tardive — Alsatian late harvest Riesling with natural concentration; honey, dried apricot, orange blossom, mineral; not always sweet — can be off-dry to medium-sweet; extraordinary aging',
 'dessert_pastry', 'sweet_fruity', 'Tarte tatin aux abricots avec crème de citron — apricot tarte tatin with lemon cream; stone fruit pairing for a late-harvest stone-fruit wine',
 'complement', 'VT Riesling''s dried apricot character resonates directly with baked apricot; the lemon cream''s acidity bridges the wine''s mineral character while preventing the combination from becoming cloying', 'dessert', 'classic', 2, true),

(313, 'wine_dessert', 'Alsace Vendange Tardive', 'Hugel Riesling Vendange Tardive — Alsatian late harvest Riesling with natural concentration; honey, dried apricot, orange blossom, mineral; not always sweet — can be off-dry to medium-sweet; extraordinary aging',
 'charcuterie_cheese', 'fermented_aged', 'Fourme d''Ambert (mild blue from Auvergne) with walnut bread — the sweetness contrasts the blue''s salt in a classic dessert-wine-cheese combination',
 'contrast', 'VT Riesling''s honey-apricot sweetness balances Fourme d''Ambert''s mild blue saltiness; the walnut bridges the wine''s mineral and the cheese''s nuttiness; a French take on the Sauternes-Roquefort dynamic', 'cheese', 'established', 2, true),

(313, 'wine_dessert', 'Alsace Vendange Tardive', 'Hugel Riesling Vendange Tardive — Alsatian late harvest Riesling with natural concentration; honey, dried apricot, orange blossom, mineral; not always sweet — can be off-dry to medium-sweet; extraordinary aging',
 'meat_poultry', 'earthy_herbal', 'Foie gras de canard en terrine with Riesling-apricot gelée — the most traditional Alsatian foie gras preparation',
 'complement', 'VT Riesling and foie gras is an Alsatian classic; the wine''s late-harvest concentration bridges the foie gras''s fat while its acidity prevents the pairing from becoming cloying; apricot gelée bridges the VT''s stone fruit', 'starter', 'classic', 2, true),

(313, 'wine_dessert', 'Alsace Vendange Tardive', 'Hugel Riesling Vendange Tardive — Alsatian late harvest Riesling with natural concentration; honey, dried apricot, orange blossom, mineral; not always sweet — can be off-dry to medium-sweet; extraordinary aging',
 'dessert_pastry', 'sweet_spiced', 'Bredele (Alsatian Christmas cookies) with cinnamon, anise, and honey — the traditional Alsatian Christmas preparation paired with the region''s most celebrated late harvest',
 'complement', 'Bredele''s spiced Christmas cookie character and VT Riesling''s honey-orange blossom create an Alsatian Christmas table tradition; the anise bridges the wine''s mineral while cinnamon amplifies the warm spice', 'celebration', 'classic', 2, true),

-- ============================================================
-- 314: Trimbach Gewurztraminer Seigneurs de Ribeaupierre (1; need 4 more)
-- Old-vine Gewurz; rose petal, lychee, spice; the apex of the variety
-- ============================================================
(314, 'wine_still', 'Alsace AOC', 'Trimbach Gewurztraminer Seigneurs de Ribeaupierre — from old-vine grand cru parcels; the apex of Gewurztraminer: rose petal, lychee, ginger, spice; extraordinary intensity without being fat',
 'meat_poultry', 'sweet_spiced', 'Canard laqué à l''alsacienne avec épices orientales — lacquered duck with five-spice, a contemporary Alsatian interpretation of Chinese influence',
 'complement', 'Gewurztraminer''s oriental spice-lychee character is an extraordinary bridge to five-spice duck preparations; the wine''s rose petal adds a floral dimension that lifts the lacquer''s sweetness', 'main', 'classic', 1, true),

(314, 'wine_still', 'Alsace AOC', 'Trimbach Gewurztraminer Seigneurs de Ribeaupierre — from old-vine grand cru parcels; the apex of Gewurztraminer: rose petal, lychee, ginger, spice; extraordinary intensity without being fat',
 'charcuterie_cheese', 'fermented_aged', 'Munster AOP (very ripe, 6-week) with caraway — Gewurztraminer and Munster is the alternative regional pairing alongside Riesling-Munster',
 'complement', 'Gewurztraminer''s aromatic intensity is one of the few styles that can match a very ripe Munster''s pungency through aromatic rather than acid power; rose petal bridges the cheese''s cream', 'cheese', 'classic', 1, true),

(314, 'wine_still', 'Alsace AOC', 'Trimbach Gewurztraminer Seigneurs de Ribeaupierre — from old-vine grand cru parcels; the apex of Gewurztraminer: rose petal, lychee, ginger, spice; extraordinary intensity without being fat',
 'meat_poultry', 'earthy_herbal', 'Dindonneau rôti aux épices de Noël avec marrons (Christmas turkey with chestnuts and spice) — the Alsatian Christmas celebration preparation',
 'complement', 'Gewurztraminer and Christmas turkey is the Alsatian holiday pairing; the wine''s spice-rose bridges the turkey''s mild flesh and chestnut stuffing; ginger echoes the Christmas spice blend', 'celebration', 'classic', 1, true),

(314, 'wine_still', 'Alsace AOC', 'Trimbach Gewurztraminer Seigneurs de Ribeaupierre — from old-vine grand cru parcels; the apex of Gewurztraminer: rose petal, lychee, ginger, spice; extraordinary intensity without being fat',
 'meat_poultry', 'sweet_spiced', 'Thai green curry with fragrant jasmine rice — the most celebrated cross-cultural Gewurztraminer pairing',
 'complement', 'Gewurztraminer and Thai curry is the most well-established cross-cultural pairing in wine education; the wine''s lychee-ginger-rose petal harmonises with the curry''s galangal-lemongrass-coconut; both are in the tropical-floral register', 'main', 'classic', 1, true),

-- ============================================================
-- 315: Ostertag Riesling Muenchberg Grand Cru (1; need 4 more)
-- Biodynamic volcanic Riesling; mineral, aromatic, complex
-- ============================================================
(315, 'wine_still', 'Alsace Grand Cru', 'Domaine Ostertag Riesling Muenchberg Grand Cru — biodynamic from the volcanic Muenchberg terroir; mineral depth with unusual aromatic intensity; orange peel, white peach, volcanic minerality',
 'seafood', 'delicate_fresh', 'Dorade royale (gilt-head sea bream) avec fenouil braisé et citron — the Mediterranean sea bream for a volcanic-mineral Riesling',
 'complement', 'Ostertag Muenchberg''s volcanic character and unusual orange peel note create a bridge to Mediterranean sea bream preparations; fennel''s anise mirrors the wine''s aromatic complexity', 'main', 'established', 1, true),

(315, 'wine_still', 'Alsace Grand Cru', 'Domaine Ostertag Riesling Muenchberg Grand Cru — biodynamic from the volcanic Muenchberg terroir; mineral depth with unusual aromatic intensity; orange peel, white peach, volcanic minerality',
 'seafood', 'umami_savoury', 'Tempura de legumes de saison avec sauce aux agrumes (vegetable tempura with citrus sauce) — the Japanese-influenced preparation for a wine with unusual aromatic depth',
 'bridge', 'Ostertag''s unusual aromatic depth (orange peel, white peach) bridges Japanese-influenced preparations; tempura''s light batter and citrus dipping sauce mirror the wine''s citrus-mineral character', 'starter', 'adventurous', 1, true),

(315, 'wine_still', 'Alsace Grand Cru', 'Domaine Ostertag Riesling Muenchberg Grand Cru — biodynamic from the volcanic Muenchberg terroir; mineral depth with unusual aromatic intensity; orange peel, white peach, volcanic minerality',
 'charcuterie_cheese', 'fermented_aged', 'Bergkäse (Alsatian Alpine cheese) with orange marmalade — the mountain cheese with citrus preserve matching the wine''s orange peel character',
 'complement', 'Ostertag''s orange peel character creates an unusual bridge to orange marmalade accompaniment; the Bergkäse''s Alpine milk richness is structured by the wine''s volcanic mineral depth', 'cheese', 'suggested', 1, true),

(315, 'wine_still', 'Alsace Grand Cru', 'Domaine Ostertag Riesling Muenchberg Grand Cru — biodynamic from the volcanic Muenchberg terroir; mineral depth with unusual aromatic intensity; orange peel, white peach, volcanic minerality',
 'seafood', 'salty_mineral', 'Huîtres pochées au Riesling avec gelée d''agrumes (poached oysters in Riesling with citrus jelly) — the contemporary Alsatian fine-dining oyster preparation',
 'complement', 'Poaching oysters in Muenchberg Riesling concentrates the wine''s citrus-mineral in the liquor; the citrus jelly mirrors the wine''s orange peel while the oyster''s brine creates mineral resonance', 'starter', 'established', 1, true),

-- ============================================================
-- 316: Marcel Deiss Bergheim (1; need 4 more)
-- Complantation (field blend); complex, orange wine-like, unique
-- ============================================================
(316, 'wine_still', 'Alsace AOC', 'Marcel Deiss Bergheim — Jean-Michel Deiss''s flagship complantation wine; all Alsatian varieties co-planted and co-harvested; orange wine-like complexity with extended skin contact; floral, spice, mineral, orange peel',
 'meat_poultry', 'earthy_herbal', 'Poulet fermier en crapaudine avec herbes sauvages (butterflied farm chicken with wild herbs) — the complex field-blend wine for a wild herb preparation',
 'complement', 'Bergheim''s complantation complexity (all varieties expressing simultaneously) creates an exceptional bridge to preparations using multiple wild herbs; the spice-floral-mineral bridge the varied herbs'' character', 'main', 'established', 1, true),

(316, 'wine_still', 'Alsace AOC', 'Marcel Deiss Bergheim — Jean-Michel Deiss''s flagship complantation wine; all Alsatian varieties co-planted and co-harvested; orange wine-like complexity with extended skin contact; floral, spice, mineral, orange peel',
 'charcuterie_cheese', 'fermented_aged', 'Tête de moine (Swiss rotating cheese) with honesty seeds and herb bread — the complex Swiss cheese for a complex Alsatian wine',
 'complement', 'Tête de moine''s rosette shavings and complex grassy-nutty character bridge Bergheim''s complantation complexity; the herb bread mirrors the wine''s herbal-spice character', 'cheese', 'suggested', 1, true),

(316, 'wine_still', 'Alsace AOC', 'Marcel Deiss Bergheim — Jean-Michel Deiss''s flagship complantation wine; all Alsatian varieties co-planted and co-harvested; orange wine-like complexity with extended skin contact; floral, spice, mineral, orange peel',
 'charcuterie_cheese', 'fermented_aged', 'Charcuterie alsacienne: Strasbourg sausage, presskopf, smoked lard — the full Alsatian charcuterie board for a wine of Alsatian cultural depth',
 'complement', 'Bergheim''s full expression of Alsatian variety character (all varieties in one wine) matches the full expression of Alsatian charcuterie culture; the smoked lard bridges the wine''s skin-contact tannic character', 'aperitif', 'classic', 1, true),

(316, 'wine_still', 'Alsace AOC', 'Marcel Deiss Bergheim — Jean-Michel Deiss''s flagship complantation wine; all Alsatian varieties co-planted and co-harvested; orange wine-like complexity with extended skin contact; floral, spice, mineral, orange peel',
 'seafood', 'umami_savoury', 'Salade niçoise revisitée avec thon mi-cuit, haricots verts, olives, et anchois — the orange wine character of Bergheim bridges cross-culturally to Mediterranean preparations',
 'bridge', 'Bergheim''s skin-contact complexity and orange peel note create bridges to Mediterranean dishes; the tuna''s richness, olive''s fat, and anchovy''s brine all find resonance with the wine''s tannic-aromatic character', 'main', 'adventurous', 1, true),

-- ============================================================
-- 317: Rémy Martin XO Excellence Cognac (1; need 4 more)
-- Premier Cru Cognac; dried fruit, vanilla, rancio, oak spice
-- ============================================================
(317, 'spirits_brandy', 'Cognac XO', 'Rémy Martin XO Excellence — Premier Cru Grande Champagne and Petite Champagne; dried fruit, vanilla, oak spice, rancio; the prestige tier that defines XO Cognac''s international benchmark',
 'dessert_pastry', 'sweet_spiced', 'Crème brûlée with vanilla — the most quintessential French dessert for the most quintessential French spirit',
 'complement', 'Cognac XO''s vanilla-cream character resonates perfectly with crème brûlée''s vanilla custard; the caramelised sugar top creates a bittersweet bridge to the spirit''s dried fruit complexity', 'digestif', 'classic', 2, true),

(317, 'spirits_brandy', 'Cognac XO', 'Rémy Martin XO Excellence — Premier Cru Grande Champagne and Petite Champagne; dried fruit, vanilla, oak spice, rancio; the prestige tier that defines XO Cognac''s international benchmark',
 'charcuterie_cheese', 'fermented_aged', 'Roquefort AOP with walnut bread and pear — the classic French digestif cheese pairing for Cognac',
 'complement', 'Cognac and Roquefort is a classic French after-dinner combination: the spirit''s sweetness tames the blue''s salt; dried fruit in the Cognac bridges the pear accompaniment; walnut bread adds textural contrast', 'digestif', 'classic', 2, true),

(317, 'spirits_brandy', 'Cognac XO', 'Rémy Martin XO Excellence — Premier Cru Grande Champagne and Petite Champagne; dried fruit, vanilla, oak spice, rancio; the prestige tier that defines XO Cognac''s international benchmark',
 'dessert_pastry', 'sweet_spiced', 'Financier au beurre noisette avec coulis d''abricot — the French teatime cake with hazelnut butter, a classic for Cognac',
 'complement', 'Cognac XO''s hazelnut-dried fruit character bridges with financier''s beurre noisette; apricot coulis directly mirrors the spirit''s dried fruit character; a classic French afternoon pairing', 'digestif', 'established', 2, true),

(317, 'spirits_brandy', 'Cognac XO', 'Rémy Martin XO Excellence — Premier Cru Grande Champagne and Petite Champagne; dried fruit, vanilla, oak spice, rancio; the prestige tier that defines XO Cognac''s international benchmark',
 'dessert_pastry', 'sweet_spiced', 'Dark chocolate truffle with Cognac filling — the literal food-spirit integration where the spirit is both inside and alongside the chocolate',
 'complement', 'A Cognac-filled chocolate truffle served alongside the same Cognac is both literal and conceptual: the chocolate''s bitter-sweet amplifies the spirit''s dried fruit and oak while the truffle''s interior mirrors the glass', 'digestif', 'classic', 2, true),

-- ============================================================
-- 318: Delamain Pale and Dry XO Grande Champagne (1; need 4 more)
-- The most elegant XO; pale, dry, refined
-- ============================================================
(318, 'spirits_brandy', 'Cognac XO', 'Delamain Pale and Dry XO Grande Champagne — from the best Cognac cru; the most elegant XO in Cognac; pale colour, delicate, dry-finish; exceptional restraint and finesse',
 'dessert_pastry', 'sweet_spiced', 'Tarte fine aux pommes (thin apple tart with calvados and cream) — the apple and Calvados preparation for a Cognac of apple-adjacent complexity',
 'complement', 'Delamain''s pale elegance and apple-fruit tertiary notes bridge with thin apple tart; the Calvados in the preparation echoes the apple-tree spirit family while the Cognac''s restraint matches the tart''s simplicity', 'digestif', 'established', 2, true),

(318, 'spirits_brandy', 'Cognac XO', 'Delamain Pale and Dry XO Grande Champagne — from the best Cognac cru; the most elegant XO in Cognac; pale colour, delicate, dry-finish; exceptional restraint and finesse',
 'charcuterie_cheese', 'fermented_aged', 'Aged Comté (18-month) with fig jam — the most elegant cheese for the most elegant Cognac',
 'complement', 'Delamain''s extraordinary restraint is matched by Comté''s subtle complexity; the cheese''s gentle nuttiness and fig jam''s sweetness mirror the spirit''s dried fruit without overpowering its delicacy', 'digestif', 'established', 2, true),

(318, 'spirits_brandy', 'Cognac XO', 'Delamain Pale and Dry XO Grande Champagne — from the best Cognac cru; the most elegant XO in Cognac; pale colour, delicate, dry-finish; exceptional restraint and finesse',
 'dessert_pastry', 'sweet_fruity', 'Madeleine au miel et citron — the iconic French cake with honey and lemon; Proust''s universal dipping vehicle now applied to Cognac',
 'complement', 'Madeleine and Cognac is an elegant French after-dinner ritual: the honey-lemon madeleine''s delicacy mirrors Delamain''s pale restraint; dipping the madeleine creates an intimate tea-Cognac moment', 'digestif', 'classic', 2, true),

(318, 'spirits_brandy', 'Cognac XO', 'Delamain Pale and Dry XO Grande Champagne — from the best Cognac cru; the most elegant XO in Cognac; pale colour, delicate, dry-finish; exceptional restraint and finesse',
 'dessert_pastry', 'sweet_spiced', 'Baba au rhum revisité en baba au Cognac — the baba soaked in Delamain Cognac rather than rum creates an all-French version of the classic',
 'complement', 'A baba soaked in Delamain creates a spirited dessert-digestif combination unique in French pastry; the spirit''s delicacy prevents the baba from becoming too heavy; served warm with Chantilly and the same Cognac in a glass', 'dessert', 'suggested', 2, true),

-- ============================================================
-- 319: Hine Antique XO Premier Cru (2; need 3 more)
-- From the oldest Hine cellars; complex, rancio, aged character
-- ============================================================
(319, 'spirits_brandy', 'Cognac XO', 'Hine Antique XO Premier Cru Grande Champagne — from the oldest Hine cellars; complex rancio character, dried fruit, walnut, spice; one of Cognac''s most respected houses',
 'dessert_pastry', 'sweet_spiced', 'Quatre-quarts breton (Brittany pound cake) with salted caramel — the French butter cake for a butter-aged Cognac',
 'complement', 'Hine Antique''s rancio-dried fruit character resonates with the quatre-quarts''s butter richness; salted caramel bridges the spirit''s dried fruit while providing the sweet-salt tension that animated Cognac requires', 'digestif', 'established', 2, true),

(319, 'spirits_brandy', 'Cognac XO', 'Hine Antique XO Premier Cru Grande Champagne — from the oldest Hine cellars; complex rancio character, dried fruit, walnut, spice; one of Cognac''s most respected houses',
 'charcuterie_cheese', 'fermented_aged', 'Gorgonzola naturale (aged, not dolce) with dried pear and walnut — the aged Gorgonzola''s rancio-like complexity matched with Hine''s own rancio character',
 'complement', 'Aged Gorgonzola naturale develops a rancio-like oxidative quality that mirrors Hine Antique''s own rancio character; dried pear and walnut bridge the spirit''s dried fruit and nutty notes', 'digestif', 'suggested', 2, true),

(319, 'spirits_brandy', 'Cognac XO', 'Hine Antique XO Premier Cru Grande Champagne — from the oldest Hine cellars; complex rancio character, dried fruit, walnut, spice; one of Cognac''s most respected houses',
 'dessert_pastry', 'sweet_spiced', 'Nougat de Montélimar (Provençal white nougat with honey and almonds) — the southern French confection for a northern French spirit',
 'complement', 'Nougat''s honey-almond sweetness and texture provide a contrast to Hine''s complexity; the spirit''s dried fruit bridges the honey while the almond echoes the walnut character', 'digestif', 'established', 2, true),

-- ============================================================
-- 320: Francis Darroze Bas-Armagnac 10 Year (1; need 4 more)
-- The most rustic and earthy brandy; dried prune, fig, earth
-- ============================================================
(320, 'spirits_brandy', 'Bas-Armagnac', 'Francis Darroze Bas-Armagnac 10 Year — from single-estate Bas-Armagnac; continuous column still distillation gives more rustic character than Cognac; dried prune, fig, earth, vanilla; the peasant''s prestige spirit',
 'dessert_pastry', 'sweet_fruity', 'Pruneaux à l''Armagnac (Agen prunes preserved in Armagnac) — the most iconic Armagnac preparation; the prunes soaked in the spirit from the same region',
 'complement', 'Pruneaux à l''Armagnac and serving the same spirit is the most circular pairing in French food culture; the prune''s dried fruit has been preserved in Armagnac; serving it alongside creates a flavour loop of full circle elegance', 'digestif', 'classic', 2, true),

(320, 'spirits_brandy', 'Bas-Armagnac', 'Francis Darroze Bas-Armagnac 10 Year — from single-estate Bas-Armagnac; continuous column still distillation gives more rustic character than Cognac; dried prune, fig, earth, vanilla; the peasant''s prestige spirit',
 'meat_poultry', 'rich_fatty_smoky', 'Magret de canard à la sauce Armagnac et pruneaux — the Gascogne duck breast with Armagnac-prune sauce; the spirit in both the dish and the glass',
 'complement', 'Magret de canard with Armagnac-prune sauce is the defining Gascogne preparation; serving Darroze alongside the dish creates the ultimate terroir pairing — the same spirit used in cooking is served in the glass', 'main', 'classic', 2, true),

(320, 'spirits_brandy', 'Bas-Armagnac', 'Francis Darroze Bas-Armagnac 10 Year — from single-estate Bas-Armagnac; continuous column still distillation gives more rustic character than Cognac; dried prune, fig, earth, vanilla; the peasant''s prestige spirit',
 'dessert_pastry', 'sweet_spiced', 'Pastis gascon (Gascony filo pastry with apples, Armagnac, and prunes) — Gascony''s traditional pastry using the local spirit',
 'complement', 'Pastis gascon is the traditional Armagnac-Apple-Prune filo preparation; serving Darroze alongside creates the most Gascon possible pairing; the apple''s freshness bridges the spirit''s dried fruit', 'dessert', 'classic', 2, true),

(320, 'spirits_brandy', 'Bas-Armagnac', 'Francis Darroze Bas-Armagnac 10 Year — from single-estate Bas-Armagnac; continuous column still distillation gives more rustic character than Cognac; dried prune, fig, earth, vanilla; the peasant''s prestige spirit',
 'charcuterie_cheese', 'fermented_aged', 'Roquefort AOP with Armagnac-soaked raisins and walnut bread — the classic Gasconne cheese and Armagnac pairing',
 'complement', 'Roquefort and Armagnac is Gascony''s great digestif combination; the spirit''s rustic character handles the blue''s pungency through character rather than delicacy; Armagnac raisins bridge the dried fruit notes', 'digestif', 'classic', 2, true),

-- ============================================================
-- 321: Dupont Calvados Pays d'Auge VSOP (1; need 4 more)
-- Apple brandy; orchard apples, vanilla, spice; 4-8 years oak
-- ============================================================
(321, 'spirits_brandy', 'Calvados', 'Domaine Dupont Calvados Pays d''Auge VSOP — double-distilled in pot still from Pays d''Auge apples; 4-8 years oak; fresh apple, vanilla, spice, toffee; the benchmark entry to quality Calvados',
 'dessert_pastry', 'sweet_fruity', 'Tarte normande aux pommes (Norman apple tart with crème fraîche) — the regional tart for the regional spirit from the same Pays d''Auge orchards',
 'complement', 'Calvados and Norman apple tart is the most direct possible food-spirit pairing: both are made from the same Pays d''Auge apples; serving the spirit alongside the tart creates full circle Norman terroir', 'dessert', 'classic', 2, true),

(321, 'spirits_brandy', 'Calvados', 'Domaine Dupont Calvados Pays d''Auge VSOP — double-distilled in pot still from Pays d''Auge apples; 4-8 years oak; fresh apple, vanilla, spice, toffee; the benchmark entry to quality Calvados',
 'meat_poultry', 'earthy_herbal', 'Poulet Vallée d''Auge (chicken in Calvados, cream, and apple sauce) — the iconic Norman preparation that defines the trou normand tradition',
 'complement', 'Poulet Vallée d''Auge is cooked with Calvados and served with the same spirit; it is the definitive Norman dish and Calvados pairing; the trou normand (small Calvados between courses) is Norman tradition', 'main', 'classic', 2, true),

(321, 'spirits_brandy', 'Calvados', 'Domaine Dupont Calvados Pays d''Auge VSOP — double-distilled in pot still from Pays d''Auge apples; 4-8 years oak; fresh apple, vanilla, spice, toffee; the benchmark entry to quality Calvados',
 'dessert_pastry', 'sweet_spiced', 'Trou normand (a glass of Calvados between courses with apple sorbet) — the traditional Norman tradition of a mid-meal digestif break',
 'complement', 'Trou normand is the Norman tradition of serving Calvados with apple sorbet between the fish course and meat course; Dupont VSOP''s fresh apple character is perfectly calibrated for this palate-cleansing tradition', 'pre_dessert', 'classic', 2, true),

(321, 'spirits_brandy', 'Calvados', 'Domaine Dupont Calvados Pays d''Auge VSOP — double-distilled in pot still from Pays d''Auge apples; 4-8 years oak; fresh apple, vanilla, spice, toffee; the benchmark entry to quality Calvados',
 'charcuterie_cheese', 'fermented_aged', 'Camembert de Normandie AOP (raw milk, 4-week) with apple slices and cider vinegar dressing — the most Norman possible cheese pairing',
 'complement', 'Camembert de Normandie and Calvados is the ultimate Norman terroir pairing: both are made within the same Pays d''Auge countryside; the cheese''s cream-mushroom note bridges the spirit''s apple-vanilla', 'digestif', 'classic', 2, true),

-- ============================================================
-- 322: Ricard Pastis de Marseille (2; need 3 more)
-- The original anise spirit; licorice, star anise, herbes de Provence
-- ============================================================
(322, 'spirits_liqueur', 'Pastis', 'Ricard Pastis de Marseille — the original French pastis; star anise and licorice with herbes de Provence; louched with water (5:1); 45% abv; the aperitivo of the South of France',
 'seafood', 'salty_mineral', 'Tapenade and anchoiade on croutons — the Provençal olive and anchovy preparations for the South''s most famous spirit',
 'complement', 'Ricard and Provençal spreads is the most quintessential Southern French aperitivo: the anise-licorice refreshes between bites of intensely flavoured tapenade and anchoiade; ice-cold louchée contrasts the room-temperature spreads', 'aperitif', 'classic', 2, true),

(322, 'spirits_liqueur', 'Pastis', 'Ricard Pastis de Marseille — the original French pastis; star anise and licorice with herbes de Provence; louched with water (5:1); 45% abv; the aperitivo of the South of France',
 'seafood', 'umami_savoury', 'Bouillabaisse (Marseille fish stew with rouille, gruyère, and croutons) — the city''s greatest dish paired with the city''s greatest spirit',
 'complement', 'Ricard is from Marseille and so is bouillabaisse; drinking pastis before the fish stew is Marseille''s aperitivo tradition; the anise bridges the saffron''s aromatic character while the pastis refreshes before the rich fish broth', 'aperitif', 'classic', 2, true),

(322, 'spirits_liqueur', 'Pastis', 'Ricard Pastis de Marseille — the original French pastis; star anise and licorice with herbes de Provence; louched with water (5:1); 45% abv; the aperitivo of the South of France',
 'vegetables_legumes', 'earthy_herbal', 'Tian de légumes provençaux (Provençal vegetable gratin with tomatoes, zucchini, and herbes de Provence) — the vegetable preparation that mirrors pastis''s aromatic profile',
 'complement', 'Pastis''s herbes de Provence character and the tian''s vegetable-herb preparation share the same Southern French aromatic landscape; serving a pastis before eating the tian extends the garrigue-herb experience', 'aperitif', 'established', 2, true),

-- ============================================================
-- 323: Henri Bardouin Pastis (1; need 4 more)
-- Artisan pastis; more complex than Ricard; 65 herbs and spices
-- ============================================================
(323, 'spirits_liqueur', 'Pastis', 'Henri Bardouin Pastis de Forcalquier — artisan pastis from Haute-Provence; 65 herbs and spices; more complex and bitter than Ricard; star anise, thyme, lavender, gentian; 45% abv',
 'seafood', 'salty_mineral', 'Soupe de poisson (Provençal fish soup) with rouille and Gruyère croutons — the lighter alternative to bouillabaisse; a pastis aperitivo before the soup',
 'complement', 'Henri Bardouin''s complexity (65 herbs including lavender and thyme from Haute-Provence) bridges with soupe de poisson''s saffron-orange-tomato character; the anise bridges the fennel-anise notes in the soup', 'aperitif', 'classic', 2, true),

(323, 'spirits_liqueur', 'Pastis', 'Henri Bardouin Pastis de Forcalquier — artisan pastis from Haute-Provence; 65 herbs and spices; more complex and bitter than Ricard; star anise, thyme, lavender, gentian; 45% abv',
 'vegetables_legumes', 'salty_mineral', 'Salade niçoise with tuna, olives, egg, and anchovies — the Provençal salad for a Provençal spirit aperitivo',
 'complement', 'Henri Bardouin''s herbal complexity and the Salade Niçoise''s multi-component Mediterranean flavours are natural companions; the lavender note in the pastis echoes the Provençal landscape that grew the salad''s ingredients', 'aperitif', 'established', 2, true),

(323, 'spirits_liqueur', 'Pastis', 'Henri Bardouin Pastis de Forcalquier — artisan pastis from Haute-Provence; 65 herbs and spices; more complex and bitter than Ricard; star anise, thyme, lavender, gentian; 45% abv',
 'seafood', 'umami_savoury', 'Brandade de morue (salt cod and olive oil purée) with toasted bread — the Provençal salt cod preparation for a herbal aperitivo spirit',
 'complement', 'Bardouin''s complexity and bitter character cuts through brandade''s rich olive oil base; the thyme in the pastis bridges the preparation''s herbal character; a sophisticated Southern French combination', 'aperitif', 'suggested', 2, true),

(323, 'spirits_liqueur', 'Pastis', 'Henri Bardouin Pastis de Forcalquier — artisan pastis from Haute-Provence; 65 herbs and spices; more complex and bitter than Ricard; star anise, thyme, lavender, gentian; 45% abv',
 'vegetables_legumes', 'earthy_herbal', 'Pistou de légumes (Provençal basil-tomato soup) with Gruyère and Bardouin croutons — the summer vegetable soup for the summer aperitivo spirit',
 'complement', 'Pistou''s basil-garlic-tomato character and Henri Bardouin''s 65-herb complexity are both expressions of Provence''s aromatic landscape; the lavender bridges the basil; thyme bridges the garlic-herb base', 'aperitif', 'classic', 2, true),

-- ============================================================
-- 324: Lemorton Calvados Domfrontais 15 Year (2; need 3 more)
-- Pear-dominant Calvados (30% pear); more floral, lighter than Pays d'Auge
-- ============================================================
(324, 'spirits_brandy', 'Calvados', 'Lemorton Calvados Domfrontais 15 Year — 30% minimum pear (Domfrontais regulation); more floral and lighter than Pays d''Auge; pear blossom, apple, vanilla, toffee; 15 years in old oak; biodynamic',
 'dessert_pastry', 'sweet_fruity', 'Poire Belle Hélène (poached pear with chocolate sauce and chantilly) — the pear preparation for a pear-dominant Calvados',
 'complement', 'Lemorton''s pear-dominant character makes Poire Belle Hélène its most direct food pairing; the poached pear mirrors the spirit''s pear blossom; chocolate adds bitterness to contrast the pear''s sweetness', 'dessert', 'classic', 2, true),

(324, 'spirits_brandy', 'Calvados', 'Lemorton Calvados Domfrontais 15 Year — 30% minimum pear (Domfrontais regulation); more floral and lighter than Pays d''Auge; pear blossom, apple, vanilla, toffee; 15 years in old oak; biodynamic',
 'charcuterie_cheese', 'fermented_aged', 'Livarot AOP (Normandy washed-rind, ''Colonel'') with sliced pear and caraway crackers — the strong Norman cheese for a 15-year Norman pear Calvados',
 'complement', 'Livarot''s pungent washed-rind is the Norman alternative to Camembert for strong pairings; the 15-year Calvados''s depth handles the cheese''s character; sliced pear bridges the spirit''s pear-dominant nature', 'digestif', 'established', 2, true),

(324, 'spirits_brandy', 'Calvados', 'Lemorton Calvados Domfrontais 15 Year — 30% minimum pear (Domfrontais regulation); more floral and lighter than Pays d''Auge; pear blossom, apple, vanilla, toffee; 15 years in old oak; biodynamic',
 'dessert_pastry', 'sweet_fruity', 'Clafoutis aux poires et amandes (pear-almond clafoutis) — the custard-baked pear preparation for Calvados that is pear-heavy',
 'complement', 'Clafoutis with pears and almonds mirrors Lemorton''s pear-vanilla character; the almond adds a nutty bridge to the oak-aged spirit''s complexity; the custard''s warmth invites a small pour of the Calvados alongside', 'dessert', 'classic', 2, true);

COMMIT;
