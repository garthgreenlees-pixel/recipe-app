-- France Phase 1a: Pairing backfill — Burgundy (191-202) + Bordeaux (223-232)
-- All products need 2-4 more pairings each

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 191: DRC La Romanée-Conti Grand Cru (has 3; need 2 more)
-- The world's most coveted wine; extraordinary complexity
-- ============================================================
(191, 'wine_still', 'Vosne-Romanée Grand Cru', 'DRC La Romanée-Conti — the world''s most coveted wine from a 1.8ha monopole in Vosne-Romanée; Pinot Noir of transcendent complexity: dried rose, forest floor, spice, mineral, violet',
 'meat_poultry', 'earthy_herbal', 'Roasted squab pigeon with liver sauce and black truffle — the most prestige-appropriate preparation for the most prestige-appropriate wine',
 'complement', 'DRC La Romanée-Conti demands a preparation of equal rarity; squab''s iron-gamey depth and the truffle''s volatile complexity are proportioned to the wine''s extraordinary multi-dimensional character', 'main', 'classic', 1, true),

(191, 'wine_still', 'Vosne-Romanée Grand Cru', 'DRC La Romanée-Conti — the world''s most coveted wine from a 1.8ha monopole in Vosne-Romanée; Pinot Noir of transcendent complexity: dried rose, forest floor, spice, mineral, violet',
 'fungi_truffles', 'earthy_herbal', 'Wild mushroom consommé with black truffle and a quenelle of pigeon liver mousse — the essence of prestige Burgundy cuisine for the essence of Burgundy',
 'complement', 'A consommé of forest mushrooms and black truffle creates the concentrated earthy register that DRC La Romanée-Conti''s complexity inhabits; both speak of the Côte d''Or''s forest and soil', 'main', 'established', 1, true),

-- ============================================================
-- 192: DRC La Tâche Grand Cru (2 pairings; need 3 more)
-- Slightly less famous than RC but arguably more complex
-- ============================================================
(192, 'wine_still', 'Vosne-Romanée Grand Cru', 'DRC La Tâche — a 6ha monopole in Vosne-Romanée; often considered even more complex than La Romanée-Conti; extraordinary spice, violet, and mineral depth; one of Burgundy''s two poles of perfection',
 'meat_poultry', 'earthy_herbal', 'Coq au vin de Bourgogne with lardons, pearl onions, and mushrooms — the most traditional Burgundian preparation that demands the region''s finest wine',
 'complement', 'Coq au vin prepared with the same appellation''s wine is the Burgundian culinary tradition; the reduction''s concentrated Pinot Noir character mirrors what''s in the glass at its most elevated', 'main', 'classic', 1, true),

(192, 'wine_still', 'Vosne-Romanée Grand Cru', 'DRC La Tâche — a 6ha monopole in Vosne-Romanée; often considered even more complex than La Romanée-Conti; extraordinary spice, violet, and mineral depth; one of Burgundy''s two poles of perfection',
 'fungi_truffles', 'earthy_herbal', 'Black truffle (Périgord) under the skin of a Bresse chicken roasted in butter — the highest expression of French poultry preparation matched with La Tâche''s violet-spice',
 'complement', 'Bresse chicken with black truffle under the skin is the defining luxury French preparation; the truffle''s earthy-volatile complexity bridges La Tâche''s forest floor and mineral depth', 'main', 'classic', 1, true),

(192, 'wine_still', 'Vosne-Romanée Grand Cru', 'DRC La Tâche — a 6ha monopole in Vosne-Romanée; often considered even more complex than La Romanée-Conti; extraordinary spice, violet, and mineral depth; one of Burgundy''s two poles of perfection',
 'charcuterie_cheese', 'fermented_aged', 'Époisses de Bourgogne AOP (washed-rind, 6-week aged) — Burgundy''s most pungent cheese; its terroir provenance creates the ultimate local pairing',
 'complement', 'Époisses is a washed-rind cheese from the Côte d''Or made in the same villages as La Tâche; its pungent-creamy character and the wine''s spice-mineral depth create an extraordinary local terroir pairing', 'cheese', 'classic', 1, true),

-- ============================================================
-- 193: Rousseau Chambertin Grand Cru (2; need 3 more)
-- "King of all vineyards"; structured, powerful, needs 15+ years
-- ============================================================
(193, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Armand Rousseau Chambertin — from the most celebrated grand cru in Gevrey; powerful, structured Pinot Noir: dark cherry, earth, spice, iron, dried flowers; requires 15+ years minimum',
 'meat_poultry', 'rich_fatty_smoky', 'Boeuf bourguignon (beef braised in Pinot Noir with lardons and mushrooms) — the dish created in the same Burgundy region as Chambertin, using the region''s wine in its preparation',
 'complement', 'Boeuf bourguignon braised in Gevrey Pinot Noir and served alongside Rousseau Chambertin is the pinnacle of Burgundian cuisine: the dish echoes and amplifies the wine''s cherry-earth-spice character', 'main', 'classic', 1, true),

(193, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Armand Rousseau Chambertin — from the most celebrated grand cru in Gevrey; powerful, structured Pinot Noir: dark cherry, earth, spice, iron, dried flowers; requires 15+ years minimum',
 'meat_poultry', 'earthy_herbal', 'Salmis de palombe (wood pigeon stew with foie gras and black truffle) — Périgord''s prestige game preparation for Burgundy''s most powerful red',
 'complement', 'Salmis de palombe''s reduction of game bird with foie gras and truffle creates the concentrated luxury flavour that Chambertin''s iron-earth structure requires; the wine''s power matches the dish''s intensity', 'main', 'established', 1, true),

(193, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Armand Rousseau Chambertin — from the most celebrated grand cru in Gevrey; powerful, structured Pinot Noir: dark cherry, earth, spice, iron, dried flowers; requires 15+ years minimum',
 'charcuterie_cheese', 'fermented_aged', 'Aged Comté (24-month ''alpages'' summer milk) — Comté''s deep, nutty, crystalline complexity is one of Chambertin''s few worthy cheese companions',
 'complement', 'A 24-month Comté from summer alpine milk has a butterscotch-hazelnut-earth complexity that bridges with Chambertin''s depth; the cheese''s crystalline texture and salt balance the wine''s iron and tannins', 'cheese', 'established', 1, true),

-- ============================================================
-- 194: Roumier Musigny Grand Cru (2; need 3 more)
-- Chambolle's finest; the most ethereally perfumed Pinot Noir
-- ============================================================
(194, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Georges Roumier Musigny — the most ethereally perfumed expression of Pinot Noir; Chambolle-Musigny''s limestone gives extraordinary floral delicacy: violet, rose petal, silk, red cherry, mineral',
 'meat_poultry', 'earthy_herbal', 'Caille rôtie au foie gras (roast quail stuffed with foie gras) — the most delicate game bird preparation for the most ethereal Burgundy',
 'complement', 'Musigny''s extraordinary delicacy demands food of equivalent refinement; quail''s mild gaminess and foie gras''s silky richness are perfectly proportioned for the wine''s floral-silk character', 'main', 'classic', 1, true),

(194, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Georges Roumier Musigny — the most ethereally perfumed expression of Pinot Noir; Chambolle-Musigny''s limestone gives extraordinary floral delicacy: violet, rose petal, silk, red cherry, mineral',
 'meat_poultry', 'delicate_fresh', 'Pintade en cocotte (guinea fowl in cocotte with herbs) — the subtle game bird''s delicacy is a natural match for Musigny''s refined florality',
 'complement', 'Guinea fowl''s refined, slightly gamey character is more delicate than squab; its herbal braise resonates with Musigny''s violet-rose petal without overpowering the wine''s delicacy', 'main', 'established', 1, true),

(194, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Georges Roumier Musigny — the most ethereally perfumed expression of Pinot Noir; Chambolle-Musigny''s limestone gives extraordinary floral delicacy: violet, rose petal, silk, red cherry, mineral',
 'fungi_truffles', 'earthy_herbal', 'Risotto au morilles et foie gras (morel mushroom risotto with shaved foie gras) — the French-influenced Italian preparation for a cross-border prestige pairing',
 'complement', 'Morel mushrooms'' extraordinary earthy-floral character (forest, soil, a hint of fruit) bridges with Musigny''s own floral-earth register; the foie gras''s richness complements the wine''s silk texture', 'main', 'suggested', 1, true),

-- ============================================================
-- 195: Leflaive Le Montrachet Grand Cru (2; need 3 more)
-- The world's greatest dry white wine; Chardonnay at its zenith
-- ============================================================
(195, 'wine_still', 'Puligny-Montrachet Grand Cru', 'Domaine Leflaive Le Montrachet — the world''s greatest dry white wine from the 8ha grand cru; Chardonnay of incomparable complexity: mineral, citrus, cream, hazelnut, dried flowers; extraordinary 20+ year aging',
 'seafood', 'delicate_fresh', 'Turbot rôti entier with lobster beurre blanc — the most prestigious preparation of France''s most prestigious white fish, paired with France''s most prestigious white wine',
 'complement', 'Le Montrachet and whole turbot is the defining French prestige white wine pairing: the fish''s extraordinary delicacy and the butter-lobster sauce''s richness are perfectly proportioned for the wine''s mineral-cream-hazelnut complexity', 'main', 'classic', 1, true),

(195, 'wine_still', 'Puligny-Montrachet Grand Cru', 'Domaine Leflaive Le Montrachet — the world''s greatest dry white wine from the 8ha grand cru; Chardonnay of incomparable complexity: mineral, citrus, cream, hazelnut, dried flowers; extraordinary 20+ year aging',
 'seafood', 'salty_mineral', 'Soufflé au Beaufort et homard (Beaufort cheese soufflé with lobster) — the Savoy cheese preparation that showcases alpine milk''s hazelnut character alongside Le Montrachet''s depth',
 'complement', 'Beaufort''s alpine hazelnut and the lobster''s sweet sea-cream create the perfect multi-layer pairing for Le Montrachet; the soufflé''s lightness echoes the wine''s ethereal texture', 'main', 'established', 1, true),

(195, 'wine_still', 'Puligny-Montrachet Grand Cru', 'Domaine Leflaive Le Montrachet — the world''s greatest dry white wine from the 8ha grand cru; Chardonnay of incomparable complexity: mineral, citrus, cream, hazelnut, dried flowers; extraordinary 20+ year aging',
 'seafood', 'umami_savoury', 'Langoustines rôties au beurre noisette with preserved lemon and tarragon — the most delicate French shellfish preparation',
 'complement', 'Langoustines'' sweet-sea delicacy and beurre noisette''s hazelnut mirror Le Montrachet''s own hazelnut character; preserved lemon bridges the wine''s citrus minerality; tarragon adds a floral-herbal note', 'starter', 'classic', 1, true),

-- ============================================================
-- 196: Coche-Dury Meursault Perrières Premier Cru (2; need 3 more)
-- The most sought Meursault; extraordinary mineral depth
-- ============================================================
(196, 'wine_still', 'Meursault Premier Cru', 'Coche-Dury Meursault Perrières — the most sought-after Meursault premier cru; extraordinary mineral depth from limestone-rich soils; hazelnut, smoke, cream, lemon, mineral; 20+ year aging potential',
 'seafood', 'delicate_fresh', 'Poulet de Bresse à la crème (Bresse chicken in cream sauce with morels) — the most prestigious French poultry served with the most prestigious Meursault',
 'complement', 'Bresse chicken''s extraordinary rich fat and the cream-morel sauce''s depth are calibrated for Coche-Dury''s Perrières; the wine''s hazelnut and mineral complexity bridges the cream''s richness and the morel''s earthiness', 'main', 'classic', 1, true),

(196, 'wine_still', 'Meursault Premier Cru', 'Coche-Dury Meursault Perrières — the most sought-after Meursault premier cru; extraordinary mineral depth from limestone-rich soils; hazelnut, smoke, cream, lemon, mineral; 20+ year aging potential',
 'seafood', 'umami_savoury', 'Risotto Bourgognonne (Burgundy-style risotto with butter and Comté instead of Parmesan) — the wine provides the mineral framework for the richness',
 'complement', 'Coche-Dury''s mineral depth and hazelnut character are reflected in the Comté-enriched risotto; the butter bridges the wine''s cream register; a sophisticated cross-regional preparation', 'main', 'established', 1, true),

(196, 'wine_still', 'Meursault Premier Cru', 'Coche-Dury Meursault Perrières — the most sought-after Meursault premier cru; extraordinary mineral depth from limestone-rich soils; hazelnut, smoke, cream, lemon, mineral; 20+ year aging potential',
 'seafood', 'salty_mineral', 'Noix de Saint-Jacques poêlées au beurre noisette (pan-seared scallops in hazelnut butter) — the most classic Burgundy white wine-scallop pairing',
 'complement', 'Scallops'' sweet sea-cream and the beurre noisette''s hazelnut mirror Coche-Dury''s hazelnut-cream-mineral profile precisely; a textbook Burgundy white wine pairing', 'main', 'classic', 1, true),

-- ============================================================
-- 197: Raveneau Chablis Grand Cru Les Clos (3; need 2 more)
-- Chablis's greatest: pure mineral, oyster-shell, chalk, lemon
-- ============================================================
(197, 'wine_still', 'Chablis Grand Cru', 'François & Jean-Marie Raveneau Chablis Grand Cru Les Clos — the benchmark Chablis Grand Cru; pure Kimmeridgian limestone minerality: oyster shell, chalk, lemon zest, white flower; extraordinary aging',
 'seafood', 'salty_mineral', 'Fine de claire oysters (Marennes-Oléron, 3-4 months claires finishing) — the quintessential Chablis Grand Cru pairing: two expressions of the same Kimmeridgian limestone origin',
 'complement', 'Chablis Grand Cru''s Kimmeridgian limestone soils are the ancient seafloor that gives the wine its oyster-shell minerality; serving it with oysters is completing the geological circle. The world''s most rational food-wine pairing', 'aperitif', 'classic', 1, true),

(197, 'wine_still', 'Chablis Grand Cru', 'François & Jean-Marie Raveneau Chablis Grand Cru Les Clos — the benchmark Chablis Grand Cru; pure Kimmeridgian limestone minerality: oyster shell, chalk, lemon zest, white flower; extraordinary aging',
 'seafood', 'umami_savoury', 'Soles meunière (Dover sole in butter and lemon) — the classic French preparation of the world''s most delicately flavoured flatfish paired with France''s most mineral white wine',
 'complement', 'Dover sole''s extraordinary delicacy and lemon-butter preparation are perfectly proportioned for Les Clos''s razor-sharp mineral acidity; the chalk note in the wine amplifies the lemon in the dish', 'main', 'classic', 1, true),

-- ============================================================
-- 198: Mugnier Musigny Grand Cru (2; need 3 more)
-- Equally ethereal to Roumier; silk, precision, longevity
-- ============================================================
(198, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Jacques-Frédéric Mugnier Musigny — another pole of Musigny''s perfection; silk-precise, violet, red cherry, dried flowers, mineral; both Mugnier and Roumier define the grand cru''s ethereal character',
 'meat_poultry', 'earthy_herbal', 'Filet de canard sauvage (wild duck fillet) with cherry reduction and endive — the game bird most proportioned to Musigny''s delicacy',
 'complement', 'Wild duck''s iron-red fruit character bridges Mugnier Musigny''s cherry-violet register; endive''s bitterness provides tension; cherry reduction mirrors the wine''s fruit directly', 'main', 'established', 1, true),

(198, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Jacques-Frédéric Mugnier Musigny — another pole of Musigny''s perfection; silk-precise, violet, red cherry, dried flowers, mineral; both Mugnier and Roumier define the grand cru''s ethereal character',
 'fungi_truffles', 'earthy_herbal', 'Oeuf parfait with black truffle shavings and Lardo di Colonnata — the perfectly cooked 63°C egg as a vehicle for truffle''s aromatic intensity alongside Musigny''s silk',
 'complement', 'The 63°C egg''s silky custard texture is a textural mirror for Mugnier Musigny''s silk palate; the truffle provides the earthy depth that bridges to the wine''s forest-floor character; Lardo adds fat to soften tannins', 'starter', 'established', 1, true),

(198, 'wine_still', 'Chambolle-Musigny Grand Cru', 'Jacques-Frédéric Mugnier Musigny — another pole of Musigny''s perfection; silk-precise, violet, red cherry, dried flowers, mineral; both Mugnier and Roumier define the grand cru''s ethereal character',
 'charcuterie_cheese', 'fermented_aged', 'Brie de Meaux AOP (wedge, room temperature, 6-week aged) — the most delicate of the great French cheeses for the most delicate of the great Burgundies',
 'complement', 'Brie de Meaux''s white mould rind, mushroom undertone, and cream-sweet interior are perfectly proportioned to Mugnier Musigny''s delicacy; the cheese''s gentle character doesn''t overwhelm the wine''s extraordinary finesse', 'cheese', 'classic', 1, true),

-- ============================================================
-- 199: Jadot Chambertin Clos de Bèze Grand Cru (2; need 3 more)
-- Gevrey's most prestigious cru; equal in law to Chambertin
-- ============================================================
(199, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Louis Jadot Chambertin Clos de Bèze — from Gevrey''s most prestigious individual cru (legally equivalent to Chambertin itself); powerful, structured Pinot Noir with extraordinary depth and longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Lievre à la royale (royale of hare, Alsatian style with foie gras and black truffle stuffing) — France''s most prestigious game preparation for one of Burgundy''s most prestigious wines',
 'complement', 'Lièvre à la royale''s extraordinary complexity (hare, foie gras, truffle, blood sauce) is the only preparation that fully matches Clos de Bèze''s depth; both require weeks of preparation and years of aging', 'main', 'classic', 1, true),

(199, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Louis Jadot Chambertin Clos de Bèze — from Gevrey''s most prestigious individual cru (legally equivalent to Chambertin itself); powerful, structured Pinot Noir with extraordinary depth and longevity',
 'meat_poultry', 'earthy_herbal', 'Canard à la presse (pressed duck, Tour d''Argent style) — the most theatrical French preparation; the blood-reduced sauce matched with a 20-year-old Clos de Bèze',
 'complement', 'Pressed duck''s iron-blood reduction is one of the most challenging but rewarding Burgundy pairings; a mature Clos de Bèze''s brick-dried fruit complexity manages the blood sauce''s iron intensity', 'main', 'established', 1, true),

(199, 'wine_still', 'Gevrey-Chambertin Grand Cru', 'Louis Jadot Chambertin Clos de Bèze — from Gevrey''s most prestigious individual cru (legally equivalent to Chambertin itself); powerful, structured Pinot Noir with extraordinary depth and longevity',
 'charcuterie_cheese', 'fermented_aged', 'Langres AOP (washed-rind cheese from the Langres plateau) — a less well-known Burgundian washed-rind that traditionally has Champagne or Burgundy poured into its top crater',
 'complement', 'Langres tradition involves pouring Marc de Bourgogne (grappa) or Chablis into the cheese''s hollow top to create a liquid-marinated interior; serving Clos de Bèze alongside extends this Burgundian ritual', 'cheese', 'suggested', 1, true),

-- ============================================================
-- 200: Dauvissat Chablis Premier Cru La Forest (2; need 3 more)
-- Intense mineral Chablis 1er Cru; saline, chalk, lemon
-- ============================================================
(200, 'wine_still', 'Chablis Premier Cru', 'René & Vincent Dauvissat Chablis La Forest 1er Cru — one of Chablis''s greatest premier crus; Kimmeridgian limestone intensity: chalk, saline mineral, lemon, white flower; equal to some Grand Crus',
 'seafood', 'salty_mineral', 'Marennes-Oléron oysters with shallot mignonette — Chablis and oysters is the world''s most rational food-wine pairing; Dauvissat''s intensity demands the finest oysters',
 'complement', 'Dauvissat La Forest''s Kimmeridgian limestone origin gives it the same ancient seafloor character as the oyster beds; the wine''s chalk-saline mirrors the oyster''s brine-shell in one of Chablis''s defining pairings', 'aperitif', 'classic', 1, true),

(200, 'wine_still', 'Chablis Premier Cru', 'René & Vincent Dauvissat Chablis La Forest 1er Cru — one of Chablis''s greatest premier crus; Kimmeridgian limestone intensity: chalk, saline mineral, lemon, white flower; equal to some Grand Crus',
 'seafood', 'delicate_fresh', 'Langoustines en bellevue (cold poached langoustines with mayonnaise) — the delicate shellfish preparation that showcases Chablis''s acidity',
 'complement', 'Langoustines'' sweet-sea character is amplified by Dauvissat''s crisp lemon acidity and mineral depth; the cold presentation matches the wine''s coolness; mayonnaise''s fat bridges the wine''s cream notes', 'starter', 'established', 1, true),

(200, 'wine_still', 'Chablis Premier Cru', 'René & Vincent Dauvissat Chablis La Forest 1er Cru — one of Chablis''s greatest premier crus; Kimmeridgian limestone intensity: chalk, saline mineral, lemon, white flower; equal to some Grand Crus',
 'seafood', 'umami_savoury', 'Huîtres gratinées au Chablis (baked oysters with Chablis and cream gratin) — the Burgundian preparation that uses the wine in the dish',
 'complement', 'Cooking oysters in Chablis and serving Dauvissat alongside creates seamless integration; the cream-wine gratin mirrors the wine''s cream-mineral character while the oyster''s brine is preserved', 'starter', 'established', 1, true),

-- ============================================================
-- 201: Roulot Meursault Les Charmes Premier Cru (2; need 3 more)
-- Elegant, floral Meursault; less powerful than Coche-Dury but refined
-- ============================================================
(201, 'wine_still', 'Meursault Premier Cru', 'Jean-Marc Roulot Meursault Les Charmes 1er Cru — an elegant, more floral Meursault than Perrières; Chardonnay with cream, hazelnut, lemon zest, and delicate floral notes; exceptional precision',
 'seafood', 'delicate_fresh', 'Noix de Saint-Jacques with cauliflower purée and hazelnut butter — the hazelnut-cream combination mirrors the wine''s profile precisely',
 'complement', 'Scallops with hazelnut butter creates a flavour mirror for Roulot Charmes'' hazelnut-cream character; cauliflower purée''s mild earthiness provides gentle texture contrast to the wine''s crispness', 'main', 'classic', 1, true),

(201, 'wine_still', 'Meursault Premier Cru', 'Jean-Marc Roulot Meursault Les Charmes 1er Cru — an elegant, more floral Meursault than Perrières; Chardonnay with cream, hazelnut, lemon zest, and delicate floral notes; exceptional precision',
 'meat_poultry', 'earthy_herbal', 'Poulet de Bresse rôti en cocotte (Bresse chicken pot-roasted with herbs, butter, and Meursault) — the classic regional preparation',
 'complement', 'Bresse chicken rôtie with Meursault in the cooking jus and Meursault in the glass is Burgundy''s chicken preparation; the wine''s cream-hazelnut notes echo the butter-cream jus', 'main', 'classic', 1, true),

(201, 'wine_still', 'Meursault Premier Cru', 'Jean-Marc Roulot Meursault Les Charmes 1er Cru — an elegant, more floral Meursault than Perrières; Chardonnay with cream, hazelnut, lemon zest, and delicate floral notes; exceptional precision',
 'seafood', 'umami_savoury', 'Terrine de foie gras de canard with Meursault jelly and brioche — the Burgundian foie gras preparation using the local white wine in the terrine',
 'complement', 'Foie gras with Meursault jelly is a classic Burgundian preparation: the wine''s cream-hazelnut richness enhances the foie gras''s fat while its acidity prevents the combination from becoming cloying', 'starter', 'established', 1, true),

-- ============================================================
-- 202: Faiveley Corton-Charlemagne Grand Cru (2; need 3 more)
-- White Burgundy Grand Cru; more robust and mineral than Meursault
-- ============================================================
(202, 'wine_still', 'Aloxe-Corton Grand Cru', 'Faiveley Corton-Charlemagne Grand Cru — the largest white grand cru in Burgundy; more powerful than Meursault; toasted almond, cream, flint, mineral; extraordinary 15+ year aging potential',
 'seafood', 'umami_savoury', 'Homard rôti au four (oven-roasted whole lobster) with Corton butter and tarragon — the wine''s mineral power demands a shellfish of equal intensity',
 'complement', 'Lobster''s sweet-sea character and the Corton butter (Burgundian butter-shallot preparation) create the richness that Faiveley''s Corton-Charlemagne requires; tarragon bridges the floral notes', 'main', 'classic', 1, true),

(202, 'wine_still', 'Aloxe-Corton Grand Cru', 'Faiveley Corton-Charlemagne Grand Cru — the largest white grand cru in Burgundy; more powerful than Meursault; toasted almond, cream, flint, mineral; extraordinary 15+ year aging potential',
 'meat_poultry', 'earthy_herbal', 'Poulet de Bresse en sauce Albufera (cream, foie gras, and truffle sauce) — Escoffier''s great Burgundy poultry preparation',
 'complement', 'Sauce Albufera''s luxurious cream-foie gras-truffle reduction is one of the few preparations that can match Corton-Charlemagne''s power among white wines; the toasted almond notes bridge the foie gras', 'main', 'established', 1, true),

(202, 'wine_still', 'Aloxe-Corton Grand Cru', 'Faiveley Corton-Charlemagne Grand Cru — the largest white grand cru in Burgundy; more powerful than Meursault; toasted almond, cream, flint, mineral; extraordinary 15+ year aging potential',
 'seafood', 'delicate_fresh', 'Ravioli de langoustines en bouillon de crustacés — Michelin-level preparation: langoustine ravioli in a shell reduction',
 'complement', 'The shell reduction''s mineral-iodine intensity amplifies the wine''s flint character; langoustine''s sweetness bridges the cream notes; the ravioli''s pasta provides texture against the wine''s mineral precision', 'main', 'suggested', 1, true),

-- ============================================================
-- 223: Château Lafite Rothschild (2; need 3 more)
-- The most famous Bordeaux; Pauillac; cedar, cassis, tobacco
-- ============================================================
(223, 'wine_still', 'Pauillac AOC', 'Château Lafite Rothschild — the most famous Bordeaux; 1er Grand Cru Classé Pauillac; Cabernet Sauvignon dominant; cedar pencil, cassis, tobacco, graphite; extraordinary elegance and finesse',
 'meat_poultry', 'earthy_herbal', 'Agneau de Pauillac (lamb from the Pauillac estuary meadows) with rosemary jus — the lamb raised in the same Pauillac appellation as Lafite',
 'complement', 'Agneau de Pauillac is the lamb raised on the salt marshes at the tip of the Médoc peninsula, a local pairing of exceptional terroir specificity; the rosemary bridges the wine''s cedar and spice', 'main', 'classic', 1, true),

(223, 'wine_still', 'Pauillac AOC', 'Château Lafite Rothschild — the most famous Bordeaux; 1er Grand Cru Classé Pauillac; Cabernet Sauvignon dominant; cedar pencil, cassis, tobacco, graphite; extraordinary elegance and finesse',
 'meat_poultry', 'rich_fatty_smoky', 'Carré d''agneau rôti (rack of lamb) with thyme jus and pommes dauphinoise — the classic Bordeaux food pairing executed with refinement',
 'complement', 'Rack of lamb is the defining Bordeaux red wine food pairing, especially for the Médoc''s Cabernet-dominant wines; Lafite''s exceptional elegance demands the finest cut and preparation', 'main', 'classic', 1, true),

(223, 'wine_still', 'Pauillac AOC', 'Château Lafite Rothschild — the most famous Bordeaux; 1er Grand Cru Classé Pauillac; Cabernet Sauvignon dominant; cedar pencil, cassis, tobacco, graphite; extraordinary elegance and finesse',
 'charcuterie_cheese', 'fermented_aged', 'Aged Mimolette Extra-Vieille (24-month, ''boule de Lille'') with walnut paste — the extraordinary French hard cheese whose crystalline-caramel character bridges Lafite''s complexity',
 'complement', 'Extra-Vieille Mimolette''s concentrated caramel-walnut character is one of the rare cheeses that can match Premier Cru Bordeaux''s complexity; the butterscotch notes bridge the wine''s cedar-tobacco', 'cheese', 'established', 1, true),

-- ============================================================
-- 224: Château Mouton Rothschild (2; need 3 more)
-- The most opulent First Growth; cassis, dark chocolate, cedar
-- ============================================================
(224, 'wine_still', 'Pauillac AOC', 'Château Mouton Rothschild — the most opulent of the First Growths; known for the most intense cassis and cedar character of the Médoc; the Rothschild art-label collection wine',
 'meat_poultry', 'rich_fatty_smoky', 'Entrecôte double (double rib steak, dry-aged 45 days) with bordelaise sauce — the classic Bordeaux steak preparation with the region''s most opulent wine',
 'complement', 'Mouton''s intense cassis-cedar and the 45-day aged beef''s concentrated umami are a match of equal intensity; bordelaise sauce (with Bordeaux wine reduction and marrow) mirrors the glass', 'main', 'classic', 1, true),

(224, 'wine_still', 'Pauillac AOC', 'Château Mouton Rothschild — the most opulent of the First Growths; known for the most intense cassis and cedar character of the Médoc; the Rothschild art-label collection wine',
 'fungi_truffles', 'earthy_herbal', 'Beef Wellington (filet de boeuf en croûte, mushroom duxelles, Périgord truffle) — the theatrical prestige preparation for a prestige wine occasion',
 'complement', 'Beef Wellington''s mushroom duxelles and truffle create the earthy depth that bridges Mouton''s cedar-cassis; the pastry provides the structural barrier that preserves the beef''s juice and the wine''s fruit', 'main', 'established', 1, true),

(224, 'wine_still', 'Pauillac AOC', 'Château Mouton Rothschild — the most opulent of the First Growths; known for the most intense cassis and cedar character of the Médoc; the Rothschild art-label collection wine',
 'charcuterie_cheese', 'fermented_aged', 'Aged Comté (30+ month ''grand cru'' Comté from Jura with Franche-Comté origin certificate) — the most complex expression of Comté for a wine of Mouton''s complexity',
 'complement', 'A 30-month Comté has developed extraordinary nutty-caramel-umami depth that bridges Mouton''s concentrated cassis-cedar; among the most intellectually satisfying red-cheese pairings in France', 'cheese', 'established', 1, true),

-- ============================================================
-- 225: Château Latour (1; need 4 more)
-- The most austere, age-requiring First Growth; iron, graphite
-- ============================================================
(225, 'wine_still', 'Pauillac AOC', 'Château Latour — the most austere and longest-aging of the First Growths; Cabernet Sauvignon from the gravel plateau beside the Gironde; iron, graphite, cassis, cedar; requires 25+ years minimum for great vintages',
 'meat_poultry', 'rich_fatty_smoky', 'Selle d''agneau rôtie (saddle of lamb) with morel jus and dauphine potatoes — the grandest lamb preparation for the grandest Pauillac',
 'complement', 'Latour demands the most serious lamb preparation; the saddle (the finest cut) and morel jus''s earthy richness match the wine''s graphite-iron austerity; dauphine potatoes provide textural richness', 'main', 'classic', 1, true),

(225, 'wine_still', 'Pauillac AOC', 'Château Latour — the most austere and longest-aging of the First Growths; Cabernet Sauvignon from the gravel plateau beside the Gironde; iron, graphite, cassis, cedar; requires 25+ years minimum for great vintages',
 'meat_poultry', 'earthy_herbal', 'Pigeon rôti with beetroot, red wine reduction, and foie gras parfait — the prestige game preparation at Latour''s level requires structured accompaniment',
 'complement', 'Pigeon''s iron-gamey character resonates with Latour''s iron and graphite; beetroot''s earthy sweetness provides a bridge; red wine reduction mirrors the glass; foie gras parfait''s fat softens the tannins', 'main', 'established', 1, true),

(225, 'wine_still', 'Pauillac AOC', 'Château Latour — the most austere and longest-aging of the First Growths; Cabernet Sauvignon from the gravel plateau beside the Gironde; iron, graphite, cassis, cedar; requires 25+ years minimum for great vintages',
 'charcuterie_cheese', 'fermented_aged', 'Montgomery''s Farmhouse Cheddar (2-year, raw milk, Somerset) — an Anglo approach to Bordeaux''s cheese pairing; the mature Cheddar''s crystalline sharpness against Latour''s austerity',
 'complement', 'Aged Cheddar''s lactic-sharp crystalline character is one of the few cheeses with the structure for Latour''s austerity; its acidity creates tension while the fat softens the tannins', 'cheese', 'suggested', 1, true),

(225, 'wine_still', 'Pauillac AOC', 'Château Latour — the most austere and longest-aging of the First Growths; Cabernet Sauvignon from the gravel plateau beside the Gironde; iron, graphite, cassis, cedar; requires 25+ years minimum for great vintages',
 'meat_poultry', 'rich_fatty_smoky', 'Magret de canard (duck breast from foie gras ducks) with Armagnac cherry sauce — the Gascony-Bordeaux preparation using both regions'' products',
 'complement', 'Magret de canard''s extraordinary fat depth (from Gascon foie gras ducks) and the cherry-Armagnac sauce bridge Latour''s cassis-cedar; the duck fat softens the wine''s powerful tannins', 'main', 'established', 1, true),

-- ============================================================
-- 226: Château Margaux Grand Vin (2; need 3 more)
-- The most perfumed First Growth; violets, cassis, mineral elegance
-- ============================================================
(226, 'wine_still', 'Margaux AOC', 'Château Margaux Grand Vin — the most perfumed of the First Growths; exceptional violet-cassis-cedar elegance; the ''feminine'' pole of the Médoc; extraordinary finesse and longevity',
 'meat_poultry', 'earthy_herbal', 'Pigeonneau en croûte avec sauce Périgueux (squab en croûte with truffle sauce) — the prestige game preparation for a wine of Margaux''s extraordinary perfume',
 'complement', 'Château Margaux''s violet and cassis elegance are mirrored in squab''s floral-gamey character; the truffle sauce bridges the wine''s earthy register while the pastry crust provides structure', 'main', 'classic', 1, true),

(226, 'wine_still', 'Margaux AOC', 'Château Margaux Grand Vin — the most perfumed of the First Growths; exceptional violet-cassis-cedar elegance; the ''feminine'' pole of the Médoc; extraordinary finesse and longevity',
 'meat_poultry', 'earthy_herbal', 'Filet de boeuf au poivre vert avec bordelaise — the most elegant beef preparation for the most elegant First Growth',
 'complement', 'Beef fillet''s lean tenderness and green pepper''s aromatic heat create complexity for Château Margaux''s perfumed character; bordelaise mirrors the Bordeaux in the glass; the wine''s violet notes amplify the pepper', 'main', 'established', 1, true),

(226, 'wine_still', 'Margaux AOC', 'Château Margaux Grand Vin — the most perfumed of the First Growths; exceptional violet-cassis-cedar elegance; the ''feminine'' pole of the Médoc; extraordinary finesse and longevity',
 'charcuterie_cheese', 'fermented_aged', 'Saint-Nectaire fermier (farm-produced, washed rind from Auvergne) with black truffle honey — the earthy-mushroom cheese against Margaux''s floral complexity',
 'complement', 'Saint-Nectaire fermier''s earthy-mushroom undertones and hazelnut rind resonates with Margaux''s forest floor complexity at maturity; truffle honey bridges both the cheese''s earthiness and the wine''s violets', 'cheese', 'established', 1, true),

-- ============================================================
-- 227: Château Haut-Brion (1; need 4 more)
-- The only non-Médoc First Growth; smoky, mineral, tobacco-earthy
-- ============================================================
(227, 'wine_still', 'Pessac-Léognan AOC', 'Château Haut-Brion — the only First Growth outside the Médoc; from Pessac-Léognan''s gravel; unique smoky-earthy-tobacco character; Cabernet Sauvignon + Merlot + Cabernet Franc; extraordinary 30+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Palombe rôtie avec salmis sauce (roasted wood pigeon with game reduction) — the Pyrenean game bird that the Bordeaux merchants have hunted for centuries',
 'complement', 'Haut-Brion''s smoky-tobacco uniqueness is mirrored in roasted wood pigeon''s naturally smoky-gamey character; the salmis reduction concentrates the game bird''s depth to match the wine''s extraordinary complexity', 'main', 'classic', 1, true),

(227, 'wine_still', 'Pessac-Léognan AOC', 'Château Haut-Brion — the only First Growth outside the Médoc; from Pessac-Léognan''s gravel; unique smoky-earthy-tobacco character; Cabernet Sauvignon + Merlot + Cabernet Franc; extraordinary 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Cèpes bordelaise (porcini in the Bordeaux style with shallots, parsley, and duck fat) — the Bordeaux speciality mushroom preparation for a Bordeaux wine',
 'complement', 'Cèpes (porcini) cooked in the Bordeaux style with duck fat and shallots is a classic regional match for Haut-Brion; the mushroom''s earthiness bridges the wine''s smoky-tobacco-mineral character', 'main', 'classic', 1, true),

(227, 'wine_still', 'Pessac-Léognan AOC', 'Château Haut-Brion — the only First Growth outside the Médoc; from Pessac-Léognan''s gravel; unique smoky-earthy-tobacco character; Cabernet Sauvignon + Merlot + Cabernet Franc; extraordinary 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Carré d''agneau des Pyrénées (Pyrenean lamb) with herbs and flageolet beans — the southwestern lamb breed''s herbal-milk character bridges with Haut-Brion''s complexity',
 'complement', 'Pyrenean lamb''s herbs-and-fat character and the flageolet beans'' earthy softness create the southwestern French flavour profile that Haut-Brion responds to; the flageolet provides texture to soften tannins', 'main', 'established', 1, true),

(227, 'wine_still', 'Pessac-Léognan AOC', 'Château Haut-Brion — the only First Growth outside the Médoc; from Pessac-Léognan''s gravel; unique smoky-earthy-tobacco character; Cabernet Sauvignon + Merlot + Cabernet Franc; extraordinary 30+ year potential',
 'charcuterie_cheese', 'fermented_aged', 'Aged Ossau-Iraty AOP (18-month Basque sheep''s milk) with dark cherry jam — the Basque-Béarnaise sheep''s milk cheese with Bordeaux''s most distinctive First Growth',
 'complement', 'Ossau-Iraty''s nuttiness and Basque sheep''s milk character bridge with Haut-Brion''s smoky-tobacco complexity; dark cherry jam mirrors the wine''s fruit intensity at maturity', 'cheese', 'established', 1, true),

-- ============================================================
-- 228: Château Pétrus (2; need 3 more)
-- The most sought Pomerol; 100% Merlot on blue clay; extraordinary richness
-- ============================================================
(228, 'wine_still', 'Pomerol AOC', 'Château Pétrus — the most sought Pomerol; 100% Merlot on the plateau''s exceptional blue clay ''buttonhole''; extraordinary richness: black cherry, plum, chocolate, truffle, iron; 30+ year aging',
 'meat_poultry', 'rich_fatty_smoky', 'Côte de boeuf rôtie (rib of beef, aged 60 days) with morel cream and bone marrow — the most prestigious beef cut for the most prestigious Merlot',
 'complement', 'Pétrus''s extraordinary Merlot richness (black cherry, plum, iron) demands a beef preparation of equal luxury; bone marrow''s fat softens the tannins while morel cream''s earthiness bridges the truffle notes', 'main', 'classic', 1, true),

(228, 'wine_still', 'Pomerol AOC', 'Château Pétrus — the most sought Pomerol; 100% Merlot on the plateau''s exceptional blue clay ''buttonhole''; extraordinary richness: black cherry, plum, chocolate, truffle, iron; 30+ year aging',
 'fungi_truffles', 'earthy_herbal', 'Black truffle risotto with Périgueux sauce (truffle-Madeira) — the combination of two luxury ingredients from adjacent regions',
 'complement', 'Pétrus''s truffle note and chocolate depth resonate with a black truffle preparation of equal luxury; the Madeira sauce''s nutty-wine character bridges the Merlot''s plum-cherry depth', 'main', 'established', 1, true),

(228, 'wine_still', 'Pomerol AOC', 'Château Pétrus — the most sought Pomerol; 100% Merlot on the plateau''s exceptional blue clay ''buttonhole''; extraordinary richness: black cherry, plum, chocolate, truffle, iron; 30+ year aging',
 'charcuterie_cheese', 'fermented_aged', 'Vacherin Mont d''Or AOP (seasonal, October-March; runny pine-banded Jura cheese) — the extraordinary seasonal cheese for an extraordinary wine',
 'complement', 'Vacherin Mont d''Or''s extraordinary pine-cream-runny character is one of the most seductive wine pairings in France; served in its spruce box alongside Pétrus at maturity it is a rare pairing of equals', 'cheese', 'suggested', 1, true),

-- ============================================================
-- 229: Château Cheval Blanc (1; need 4 more)
-- Saint-Émilion premier; Cabernet Franc dominant; spice, floral, opulence
-- ============================================================
(229, 'wine_still', 'Saint-Émilion Grand Cru AOC', 'Château Cheval Blanc — Saint-Émilion''s most revered wine; majority Cabernet Franc with Merlot; unique opulent-yet-spicy character: raspberry, graphite, violet, spice, extraordinary complexity',
 'meat_poultry', 'earthy_herbal', 'Magret de canard avec sauce aux cerises et herbes (duck breast with cherry-herb sauce) — the Gascon preparation that bridges Cheval Blanc''s fruit character',
 'complement', 'Cheval Blanc''s Cabernet Franc-driven raspberry-violet and the cherry sauce''s fruit create a seamless bridge; the duck''s fat depth provides structure for the wine''s opulence', 'main', 'classic', 1, true),

(229, 'wine_still', 'Saint-Émilion Grand Cru AOC', 'Château Cheval Blanc — Saint-Émilion''s most revered wine; majority Cabernet Franc with Merlot; unique opulent-yet-spicy character: raspberry, graphite, violet, spice, extraordinary complexity',
 'meat_poultry', 'rich_fatty_smoky', 'Salmis de bécasse (woodcock stew, the traditional Bordeaux game preparation) — the most prized game bird of the Gironde prepared in the classic Bordeaux style',
 'complement', 'Bécasse (woodcock) is the most coveted game bird in France; the innard-enriched salmis preparation''s iron-game intensity is the most fitting match for Cheval Blanc''s complexity', 'main', 'established', 1, true),

(229, 'wine_still', 'Saint-Émilion Grand Cru AOC', 'Château Cheval Blanc — Saint-Émilion''s most revered wine; majority Cabernet Franc with Merlot; unique opulent-yet-spicy character: raspberry, graphite, violet, spice, extraordinary complexity',
 'fungi_truffles', 'earthy_herbal', 'Foie gras de canard poêlé avec compotée de figues noires (seared foie gras with black fig compote) — the richest Gascon preparation for the region''s most complex wine',
 'complement', 'Foie gras''s extraordinary fat and the fig''s rich sweetness are calibrated for Cheval Blanc''s opulence; the wine''s violet-spice notes cut through the fat while the raspberry bridges the fig', 'main', 'established', 1, true),

(229, 'wine_still', 'Saint-Émilion Grand Cru AOC', 'Château Cheval Blanc — Saint-Émilion''s most revered wine; majority Cabernet Franc with Merlot; unique opulent-yet-spicy character: raspberry, graphite, violet, spice, extraordinary complexity',
 'charcuterie_cheese', 'fermented_aged', 'Fourme d''Ambert AOP with pear and walnut — the mildest of France''s great blue cheeses for Cheval Blanc''s elegance',
 'complement', 'Fourme d''Ambert''s mild blue character is proportioned to Cheval Blanc''s spicy elegance; pear bridges the wine''s raspberry-violet fruit; walnut provides textural contrast', 'cheese', 'suggested', 1, true),

-- ============================================================
-- 230: Pavillon Blanc de Château Margaux (1; need 4 more)
-- 100% Sauvignon Blanc from Margaux; rare Bordeaux dry white
-- ============================================================
(230, 'wine_still', 'Bordeaux AOC Blanc', 'Pavillon Blanc de Château Margaux — 100% Sauvignon Blanc from the Margaux estate; one of Bordeaux''s rarest and most prestigious dry whites; mineral, citrus, gooseberry, white flower, extraordinary depth',
 'seafood', 'delicate_fresh', 'Langoustines avec sauce Nantua (langoustine in cream-crayfish sauce) — the prestige Lyonnaise preparation elevated to match a prestige Bordeaux white',
 'complement', 'Langoustine''s sweet sea-cream and sauce Nantua''s crayfish-cream create the multi-layered richness that Pavillon Blanc''s mineral-citrus structure can cut through; the wine''s Sauvignon Blanc precision is essential for this dish''s richness', 'main', 'classic', 1, true),

(230, 'wine_still', 'Bordeaux AOC Blanc', 'Pavillon Blanc de Château Margaux — 100% Sauvignon Blanc from the Margaux estate; one of Bordeaux''s rarest and most prestigious dry whites; mineral, citrus, gooseberry, white flower, extraordinary depth',
 'seafood', 'salty_mineral', 'Tartare de turbot avec caviar osciètre and lemon cream — the most prestige-appropriate raw fish preparation for a prestige dry Bordeaux white',
 'complement', 'Turbot tartare''s delicate mineral character and osciètre caviar''s brine-sea intensity are calibrated for Pavillon Blanc''s mineral depth and Sauvignon precision; lemon cream bridges the wine''s citrus character', 'starter', 'established', 1, true),

(230, 'wine_still', 'Bordeaux AOC Blanc', 'Pavillon Blanc de Château Margaux — 100% Sauvignon Blanc from the Margaux estate; one of Bordeaux''s rarest and most prestigious dry whites; mineral, citrus, gooseberry, white flower, extraordinary depth',
 'vegetables_legumes', 'bitter_astringent', 'Asperges blanches de la Gironde avec sauce hollandaise — white asparagus from the Gironde region, the same soil as the grapes',
 'complement', 'Gironde white asparagus and Pavillon Blanc share the same terroir; the asparagus''s mineral-bitter character bridges the Sauvignon Blanc''s gooseberry-white flower; Hollandaise''s butter softens the wine''s precision', 'starter', 'classic', 1, true),

(230, 'wine_still', 'Bordeaux AOC Blanc', 'Pavillon Blanc de Château Margaux — 100% Sauvignon Blanc from the Margaux estate; one of Bordeaux''s rarest and most prestigious dry whites; mineral, citrus, gooseberry, white flower, extraordinary depth',
 'charcuterie_cheese', 'fermented_aged', 'Crottin de Chavignol AOP (aged Loire goat''s cheese) — Sauvignon Blanc and goat''s cheese is the world''s most classic white wine-cheese combination',
 'complement', 'Crottin de Chavignol and Sauvignon Blanc is one of the world''s most rational pairings: the goat''s milk''s lactic tang resonates with the wine''s citrus-mineral precision; Loire origin mirrors the grape variety''s homeland', 'cheese', 'classic', 1, true),

-- ============================================================
-- 231: Léoville Las Cases Grand Clos (1; need 4 more)
-- Saint-Julien's finest; the ''super second''; finesse and structure
-- ============================================================
(231, 'wine_still', 'Saint-Julien AOC', 'Léoville Las Cases Grand Clos — the greatest ''super second'' and arguably a First Growth in quality; Saint-Julien precision and cedar-cassis depth; extraordinary structure and longevity',
 'meat_poultry', 'earthy_herbal', 'Noisettes d''agneau (lamb cutlets) with sauce bordelaise and haricots verts — the most refined lamb preparation for Saint-Julien''s precision',
 'complement', 'Noisettes d''agneau''s precision and the classic bordelaise sauce mirror Las Cases''s own finesse; haricots verts'' fresh-bitter notes create gentle tension with the wine''s cedar-cassis', 'main', 'classic', 1, true),

(231, 'wine_still', 'Saint-Julien AOC', 'Léoville Las Cases Grand Clos — the greatest ''super second'' and arguably a First Growth in quality; Saint-Julien precision and cedar-cassis depth; extraordinary structure and longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Côtelettes de veau Orloff (veal chops with soubise and Gruyère) — the classic French veal preparation for a wine of Las Cases''s structure',
 'complement', 'Veal Orloff''s cream-onion-Gruyère richness provides the fat and dairy depth that Las Cases''s structured tannins require; the wine''s Saint-Julien precision cuts through the cream elegantly', 'main', 'established', 1, true),

(231, 'wine_still', 'Saint-Julien AOC', 'Léoville Las Cases Grand Clos — the greatest ''super second'' and arguably a First Growth in quality; Saint-Julien precision and cedar-cassis depth; extraordinary structure and longevity',
 'fungi_truffles', 'earthy_herbal', 'Duxelles de champignons des bois en croûte (wild mushroom duxelles en croûte) — the classic French pastry-mushroom preparation as a stand-alone course',
 'complement', 'Wild mushroom duxelles in pastry concentrates the earthy fungal notes that bridge Las Cases''s cedar-earth; the pastry''s butter provides fat to soften the wine''s structure', 'starter', 'suggested', 1, true),

(231, 'wine_still', 'Saint-Julien AOC', 'Léoville Las Cases Grand Clos — the greatest ''super second'' and arguably a First Growth in quality; Saint-Julien precision and cedar-cassis depth; extraordinary structure and longevity',
 'charcuterie_cheese', 'fermented_aged', 'Aged Gouda (36-month, ''extra old'') with quince paste — the Dutch crystalline aged cheese''s caramel-butterscotch character against Las Cases''s precision',
 'complement', 'Aged Gouda''s caramel-butterscotch and the wine''s cedar-cassis are unexpected harmonious pairings; quince paste bridges both the cheese''s sweetness and the wine''s dark fruit', 'cheese', 'suggested', 1, true),

-- ============================================================
-- 232: Cos d'Estournel (1; need 4 more)
-- Saint-Estèphe's finest; structured, dark, mineral depth
-- ============================================================
(232, 'wine_still', 'Saint-Estèphe AOC', 'Château Cos d''Estournel — Saint-Estèphe''s most celebrated château; the ''Oriental'' château with its exotic pagoda-style chai; structured, dark-fruited Cabernet with mineral depth and exceptional aging potential',
 'meat_poultry', 'rich_fatty_smoky', 'Carré de porc noir de Bigorre (Gascon heritage pork rack) with prune-Armagnac sauce — the southwestern French luxury pork for a powerful Bordeaux',
 'complement', 'Noir de Bigorre pork''s extraordinary fat quality and the prune-Armagnac sauce''s dried fruit-spirit character bridge Cos d''Estournel''s dark fruit-mineral structure', 'main', 'established', 1, true),

(232, 'wine_still', 'Saint-Estèphe AOC', 'Château Cos d''Estournel — Saint-Estèphe''s most celebrated château; the ''Oriental'' château with its exotic pagoda-style chai; structured, dark-fruited Cabernet with mineral depth and exceptional aging potential',
 'meat_poultry', 'earthy_herbal', 'Gigot de sept heures (seven-hour braised leg of lamb with herbs and garlic) — the most forgiving and generous lamb preparation for a wine of Cos''s power',
 'complement', 'Seven-hour braised lamb''s extraordinary tenderness and herb-garlic depth are perfectly proportioned for Cos d''Estournel''s mineral-structured power; the extended braise''s fat richness softens the tannins', 'main', 'classic', 1, true),

(232, 'wine_still', 'Saint-Estèphe AOC', 'Château Cos d''Estournel — Saint-Estèphe''s most celebrated château; the ''Oriental'' château with its exotic pagoda-style chai; structured, dark-fruited Cabernet with mineral depth and exceptional aging potential',
 'charcuterie_cheese', 'fermented_aged', 'Roquefort AOP with honey-walnut crackers — the sharp blue character of France''s most famous sheep''s milk blue against the wine''s dark structure',
 'complement', 'Cos d''Estournel''s structured dark-mineral character has the tannin-acid balance to work with Roquefort''s pungency; walnut crackers bridge the wine''s mineral notes; honey balances the cheese''s salt', 'cheese', 'suggested', 1, true),

(232, 'wine_still', 'Saint-Estèphe AOC', 'Château Cos d''Estournel — Saint-Estèphe''s most celebrated château; the ''Oriental'' château with its exotic pagoda-style chai; structured, dark-fruited Cabernet with mineral depth and exceptional aging potential',
 'fungi_truffles', 'earthy_herbal', 'Cépes bordelaises en papillote (porcini in parchment with duck fat, shallots, and herbs) — the Bordeaux classic mushroom preparation for a Bordeaux wine',
 'complement', 'Cépes bordelaises in parchment concentrates the earthy-fat-herb notes that bridge Cos d''Estournel''s mineral-earthy structure; duck fat provides the richness to match the wine''s power', 'main', 'classic', 1, true);

COMMIT;
