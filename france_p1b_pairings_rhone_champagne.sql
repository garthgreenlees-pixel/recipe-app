-- France Phase 1b: Pairing backfill — Rhône (233-240) + Champagne (241-246)
-- All 1-pairing products need 4 more; 2-pairing products need 3 more

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 233: Guigal La Mouline Côte-Rôtie (1; need 4 more)
-- Most elegant of the La La's; violets, white pepper, silky texture
-- ============================================================
(233, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Mouline — the most silk-textured and perfumed of the three La La Côte-Rôtie wines; 11% Viognier co-fermented with Syrah; violets, white pepper, apricot, smoke; 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Pigeon rôti avec jus aux olives de Nyons (roasted pigeon with Nyons olive jus) — the Provençal olive''s fruit bridges La Mouline''s violet-smoke character',
 'complement', 'La Mouline''s silky violet-smoke and the Rhône olive''s fat-fruit are natural companions; the black olive''s bitterness provides tension against the wine''s elegance; roasted pigeon''s game depth matches the Syrah', 'main', 'classic', 1, true),

(233, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Mouline — the most silk-textured and perfumed of the three La La Côte-Rôtie wines; 11% Viognier co-fermented with Syrah; violets, white pepper, apricot, smoke; 30+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Selle d''agneau des Alpilles à la lavande (Provençal lavender-lamb) — the perfumed lamb from the Alpilles mountains for the most perfumed Côte-Rôtie',
 'complement', 'La Mouline''s apricot-violet Viognier co-fermentation creates a floral character that resonates with lavender-herb lamb; the Syrah base provides the structure for the lamb''s fat', 'main', 'established', 1, true),

(233, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Mouline — the most silk-textured and perfumed of the three La La Côte-Rôtie wines; 11% Viognier co-fermented with Syrah; violets, white pepper, apricot, smoke; 30+ year potential',
 'charcuterie_cheese', 'fermented_aged', 'Aged Saint-Marcellin (extra-runny, 8-week from Lyon) — the Lyonnaise liquid-centre cheese for Lyon''s great wine appellation',
 'complement', 'Saint-Marcellin''s runny cream-fungus character and La Mouline''s silk texture create a textural bridge; the wine''s violet notes amplify the cheese''s earthy-floral character', 'cheese', 'established', 1, true),

(233, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Mouline — the most silk-textured and perfumed of the three La La Côte-Rôtie wines; 11% Viognier co-fermented with Syrah; violets, white pepper, apricot, smoke; 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Saucisse de Lyon grillée avec pommes à l''huile and dijon mustard — the Lyonnaise classic sausage preparation as a simpler match for this extraordinary wine',
 'complement', 'La Mouline''s proximity to Lyon makes the city''s classic charcuterie preparations natural companions; the sausage''s fatty pork and mustard''s sharpness contrast the wine''s silk and violet elegance', 'casual', 'suggested', 1, true),

-- ============================================================
-- 234: Guigal La Landonne Côte-Rôtie (1; need 4 more)
-- Most powerful of the La La's; pure Syrah, iron, tar, smoke
-- ============================================================
(234, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Landonne — the most powerful La La; pure Syrah from iron-oxide-rich brown schist soils; tar, iron, smoke, dark olive, pepper; requires 20+ years and matches maximum-intensity preparations',
 'meat_poultry', 'rich_fatty_smoky', 'Côte de boeuf sauvage (dry-aged prime rib, 60+ days) with bone marrow and Périgueux sauce — La Landonne''s iron-tar requires a beef of equivalent power',
 'complement', 'La Landonne''s extraordinary iron-tar is one of wine''s most powerful flavour experiences; only a 60-day dry-aged rib has the intensity to match; marrow''s fat softens the iron while Périgueux bridges the truffle note', 'main', 'classic', 1, true),

(234, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Landonne — the most powerful La La; pure Syrah from iron-oxide-rich brown schist soils; tar, iron, smoke, dark olive, pepper; requires 20+ years and matches maximum-intensity preparations',
 'meat_poultry', 'earthy_herbal', 'Sanglier (wild boar) rôti à la broche avec sauce Grand Veneur — spit-roasted wild boar with hunter''s red wine reduction sauce',
 'complement', 'Wild boar''s primitive intensity and the hunter''s sauce reduction are the only game preparations with the depth to match La Landonne''s iron-smoke at maturity', 'main', 'established', 1, true),

(234, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Landonne — the most powerful La La; pure Syrah from iron-oxide-rich brown schist soils; tar, iron, smoke, dark olive, pepper; requires 20+ years and matches maximum-intensity preparations',
 'charcuterie_cheese', 'fermented_aged', 'Gruyère de Comté (24-month) with black olive tapenade — the aged Comté''s hazelnut-iron notes bridge La Landonne''s iron character while black olive mirrors the wine''s olive note',
 'bridge', 'Black olive tapenade directly mirrors one of La Landonne''s most distinctive aromatic notes; Comté''s hazelnut-iron bridges the wine''s mineral iron; a powerful cheese pairing for a powerful wine', 'cheese', 'classic', 1, true),

(234, 'wine_still', 'Côte-Rôtie AOC', 'Guigal La Landonne — the most powerful La La; pure Syrah from iron-oxide-rich brown schist soils; tar, iron, smoke, dark olive, pepper; requires 20+ years and matches maximum-intensity preparations',
 'fungi_truffles', 'earthy_herbal', 'Cerf (venison) en cuisson longue avec sauce aux truffes noires — long-cooked venison with black truffle sauce; the iron-meets-truffle combination',
 'complement', 'Venison''s iron-red meat intensity and the black truffle sauce''s volatile earth create the dual-register flavour intensity that La Landonne''s tar-iron requires', 'main', 'established', 1, true),

-- ============================================================
-- 235: Chave Hermitage Rouge (1; need 4 more)
-- The benchmark Hermitage; structured Syrah, tar, pepper, iron, mineral
-- ============================================================
(235, 'wine_still', 'Hermitage AOC', 'Jean-Louis Chave Hermitage Rouge — the benchmark Hermitage Syrah; granite soils on the hill give extraordinary mineral depth; tar, black pepper, iron, smoke, dried flowers; 30+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Agneau de Drôme rôti (lamb from the Drôme, Hermitage''s neighbour) with anchovy and herbs — the local lamb preparation with local wine is a Rhône classic',
 'complement', 'Lamb from the hills surrounding Hermitage and Chave''s Hermitage Rouge represent a terroir pairing of extraordinary precision; anchovy''s saline intensity provides the mineral bridge to the wine''s granite character', 'main', 'classic', 1, true),

(235, 'wine_still', 'Hermitage AOC', 'Jean-Louis Chave Hermitage Rouge — the benchmark Hermitage Syrah; granite soils on the hill give extraordinary mineral depth; tar, black pepper, iron, smoke, dried flowers; 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Boeuf en daube provençale (Provençal beef stew with olives, orange zest, and herbs) — the slow-braised Provençal preparation for the Northern Rhône''s great Syrah',
 'complement', 'Daube Provençale''s olive-orange-thyme depth creates the garrigue-herb complexity that bridges Hermitage''s tar-pepper; the orange zest''s citrus brightens against the wine''s mineral character', 'main', 'established', 1, true),

(235, 'wine_still', 'Hermitage AOC', 'Jean-Louis Chave Hermitage Rouge — the benchmark Hermitage Syrah; granite soils on the hill give extraordinary mineral depth; tar, black pepper, iron, smoke, dried flowers; 30+ year potential',
 'charcuterie_cheese', 'fermented_aged', 'Reblochon de Savoie fermier (farm-produced, washed rind, 4-week) — the Alpine washed-rind cheese whose earthy-cream character bridges with Hermitage''s mineral depth',
 'complement', 'Reblochon''s earthy-cream-slightly-funky character is one of the few cheeses with the depth to match Hermitage Rouge at maturity; the wine''s tar-pepper provides the structural counterpoint', 'cheese', 'established', 1, true),

(235, 'wine_still', 'Hermitage AOC', 'Jean-Louis Chave Hermitage Rouge — the benchmark Hermitage Syrah; granite soils on the hill give extraordinary mineral depth; tar, black pepper, iron, smoke, dried flowers; 30+ year potential',
 'fungi_truffles', 'earthy_herbal', 'Cèpes en persillades (porcini with parsley, garlic, and duck fat) — the classic preparation of Périgord mushrooms for a Rhône wine of equal depth',
 'complement', 'Porcini''s concentrated earthy depth and the persillade''s garlic-herb intensity create a dual aromatic bridge to Chave''s granite-mineral-pepper character; duck fat provides the richness to match the wine''s power', 'main', 'classic', 1, true),

-- ============================================================
-- 236: Jaboulet La Chapelle Hermitage (2; need 3 more)
-- Historic Hermitage; legendary vintages (1961); more accessible than Chave
-- ============================================================
(236, 'wine_still', 'Hermitage AOC', 'Paul Jaboulet Aîné La Chapelle — the historic Hermitage; legendary vintages from 1961 to the mid-1990s; more accessible style than Chave; black pepper, tar, smoked meat, violet',
 'meat_poultry', 'rich_fatty_smoky', 'Cervelas lyonnais with pommes à l''huile and Dijon — the Lyon sausage for a Lyon-adjacent wine; accessible versions of La Chapelle with classic bouchon food',
 'complement', 'La Chapelle at more accessible quality levels pairs beautifully with Lyon''s great sausage tradition; the smoked meat note in the wine bridges the cervelas''s pork-spice character', 'main', 'classic', 2, true),

(236, 'wine_still', 'Hermitage AOC', 'Paul Jaboulet Aîné La Chapelle — the historic Hermitage; legendary vintages from 1961 to the mid-1990s; more accessible style than Chave; black pepper, tar, smoked meat, violet',
 'meat_poultry', 'earthy_herbal', 'Canard sauvage (wild duck) rôti with olive oil and herbes de Provence — the Rhône Valley game preparation',
 'complement', 'Wild duck''s gamey-iron character and the Provençal herb crust bridge La Chapelle''s smoked meat-pepper notes; the Rhône Valley herbs are a natural aromatic bridge to this northern Rhône wine', 'main', 'established', 2, true),

(236, 'wine_still', 'Hermitage AOC', 'Paul Jaboulet Aîné La Chapelle — the historic Hermitage; legendary vintages from 1961 to the mid-1990s; more accessible style than Chave; black pepper, tar, smoked meat, violet',
 'charcuterie_cheese', 'fermented_aged', 'Aged Cantal AOP (12-month ''entre-deux'') with charcuterie — the mountain cheese from the Massif Central for a wine of the adjacent Rhône slopes',
 'complement', 'Cantal''s medium-aged lactic character bridges La Chapelle''s violet-pepper with enough richness; the accompanying charcuterie adds the cured meat dimension that mirrors the wine''s smoked meat note', 'cheese', 'established', 2, true),

-- ============================================================
-- 237: Clape Cornas (1; need 4 more)
-- Auguste Clape's Cornas; the most austere Northern Rhône Syrah
-- ============================================================
(237, 'wine_still', 'Cornas AOC', 'Auguste Clape Cornas — the benchmark Cornas; pure Syrah from ancient granite terraces; the most austere and ''masculine'' northern Rhône appellation; black pepper, iron, tar, smoked black olive; 25+ years',
 'meat_poultry', 'rich_fatty_smoky', 'Andouillette 5A (Lyonnaise chitterling sausage, AAAA grade) with Dijon mustard and frites — the most challenging Lyon charcuterie for the most austere Rhône wine',
 'complement', 'Andouillette''s intense offal character and the mustard''s sharpness require a wine of Cornas''s iron-pepper austerity to provide structure; a pairing that rewards those who appreciate both without compromise', 'main', 'suggested', 1, true),

(237, 'wine_still', 'Cornas AOC', 'Auguste Clape Cornas — the benchmark Cornas; pure Syrah from ancient granite terraces; the most austere and ''masculine'' northern Rhône appellation; black pepper, iron, tar, smoked black olive; 25+ years',
 'meat_poultry', 'earthy_herbal', 'Gigot d''agneau d''Ardèche (Ardèche lamb) rôti with rosemary, thyme, and jus — the Ardèche lamb from Cornas''s immediate hinterland',
 'complement', 'Ardèche lamb raised near the Cornas vineyards and Clape''s Cornas create an immediate terroir connection; the herb crust bridges the wine''s Provence-adjacent aromatic character', 'main', 'classic', 1, true),

(237, 'wine_still', 'Cornas AOC', 'Auguste Clape Cornas — the benchmark Cornas; pure Syrah from ancient granite terraces; the most austere and ''masculine'' northern Rhône appellation; black pepper, iron, tar, smoked black olive; 25+ years',
 'meat_poultry', 'rich_fatty_smoky', 'Canard confit de Gascogne with flageolet beans and duck fat persillade — the confit duck for a wine of maximum Syrah power',
 'complement', 'Duck confit''s extraordinary fat depth and the flageolet beans'' earthy softness create the richness required to tame Cornas''s formidable tannins; duck fat bridges the smoked olive note in the wine', 'main', 'established', 1, true),

(237, 'wine_still', 'Cornas AOC', 'Auguste Clape Cornas — the benchmark Cornas; pure Syrah from ancient granite terraces; the most austere and ''masculine'' northern Rhône appellation; black pepper, iron, tar, smoked black olive; 25+ years',
 'charcuterie_cheese', 'fermented_aged', 'Aged Laguiole AOP (12-month from Aubrac) — the Auvergne mountain cheese with nutty, herbal complexity for the adjacent Rhône appellation',
 'complement', 'Laguiole''s herbal-mountain character from Aubrac pastures bridges with Cornas''s wild garrigue-pepper; the cheese''s nutty richness provides the fat to soften the tannins', 'cheese', 'established', 1, true),

-- ============================================================
-- 238: Château Rayas Châteauneuf-du-Pape Rouge (1; need 4 more)
-- The legendary CdP; 100% old-vine Grenache; kirsch, garrigue, spice
-- ============================================================
(238, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Rayas CdP Rouge — the most legendary Châteauneuf; 100% Grenache from old vines on sandy soils; kirsch, garrigue, dried thyme, lavender, warm spice; deceptively light colour but extraordinary depth',
 'meat_poultry', 'earthy_herbal', 'Agneau des Alpilles en gigot avec herbes de Provence — the classic Provençal lamb from the limestone hills of Les Alpilles near Arles',
 'complement', 'Rayas''s garrigue-lavender-thyme character is mirrored in the Alpilles lamb''s herb-pasture feeding; both express the wild Provençal landscape; kirsch bridges the lamb''s sweet roasted character', 'main', 'classic', 1, true),

(238, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Rayas CdP Rouge — the most legendary Châteauneuf; 100% Grenache from old vines on sandy soils; kirsch, garrigue, dried thyme, lavender, warm spice; deceptively light colour but extraordinary depth',
 'meat_poultry', 'rich_fatty_smoky', 'Daube de taureau camarguais (Camargue bull braised in red wine, olives, capers, orange) — the bull from the Rhône delta prepared in the traditional Provençal style',
 'complement', 'Camargue bull''s extraordinary flavour intensity and the daube''s orange-olive complexity are calibrated for Rayas''s garrigue-kirsch depth; the olive oil bridges directly with the wine''s Provençal character', 'main', 'classic', 1, true),

(238, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Rayas CdP Rouge — the most legendary Châteauneuf; 100% Grenache from old vines on sandy soils; kirsch, garrigue, dried thyme, lavender, warm spice; deceptively light colour but extraordinary depth',
 'charcuterie_cheese', 'fermented_aged', 'Pélardon AOP (aged Languedoc goat''s cheese) with lavender honey — the wild garrigue goat''s milk cheese for the most garrigue-expressive CdP',
 'complement', 'Pélardon''s wild garrigue character (from Languedoc scrubland goat grazing) resonates with Rayas''s lavender-thyme-garrigue; lavender honey mirrors both the wine''s floral notes and the region''s landscape', 'cheese', 'classic', 1, true),

(238, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Rayas CdP Rouge — the most legendary Châteauneuf; 100% Grenache from old vines on sandy soils; kirsch, garrigue, dried thyme, lavender, warm spice; deceptively light colour but extraordinary depth',
 'vegetables_legumes', 'earthy_herbal', 'Ratatouille Niçoise confite (slow-cooked tomato-pepper-aubergine-courgette) — the Provençal vegetable preparation for a wine born of the same sun',
 'complement', 'Ratatouille''s concentrated Provençal vegetable character — the tomato acidity, the aubergine''s earth, the pepper''s sweetness — mirrors Rayas''s garrigue-warm spice; both are expressions of southern French sunlight', 'main', 'classic', 1, true),

-- ============================================================
-- 239: Beaucastel Châteauneuf-du-Pape Rouge (1; need 4 more)
-- Mourvèdre-dominant (30%); complex, age-worthy, leather, game
-- ============================================================
(239, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Beaucastel CdP Rouge — the most age-worthy Châteauneuf; high Mourvèdre (30%) gives extraordinary complexity: leather, game, dark fruit, pepper, garrigue; biodynamic; 30+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Joue de boeuf braisée (braised beef cheek) with black olive and orange gremolata — the slow-cooked Provençal beef preparation that matches Beaucastel''s Mourvèdre-driven power',
 'complement', 'Beaucastel''s Mourvèdre leather-game character and the braised beef cheek''s collagen richness are calibrated for maximum richness; the black olive and orange gremolata bridges the wine''s olive-citrus notes directly', 'main', 'classic', 1, true),

(239, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Beaucastel CdP Rouge — the most age-worthy Châteauneuf; high Mourvèdre (30%) gives extraordinary complexity: leather, game, dark fruit, pepper, garrigue; biodynamic; 30+ year potential',
 'meat_poultry', 'earthy_herbal', 'Sanglier (wild boar) à la provençale with olives, capers, and tomatoes — Provence''s most powerful game preparation for its most powerful CdP',
 'complement', 'Wild boar''s primitive game intensity and the Provençal olive-caper-tomato sauce create the maximum Southern Rhône food pairing; Beaucastel''s Mourvèdre leather bridges the game''s character', 'main', 'classic', 1, true),

(239, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Beaucastel CdP Rouge — the most age-worthy Châteauneuf; high Mourvèdre (30%) gives extraordinary complexity: leather, game, dark fruit, pepper, garrigue; biodynamic; 30+ year potential',
 'charcuterie_cheese', 'fermented_aged', 'Banon AOP (Provençal goat''s cheese wrapped in chestnut leaves and tied with raffia) — the most Provençal of cheeses for the most Provençal of great wines',
 'complement', 'Banon''s chestnut-leaf-wrapped curing gives it a unique earthy-tannic character from the leaves that bridges Beaucastel''s Mourvèdre leather; the goat milk''s acidity provides tension', 'cheese', 'classic', 1, true),

(239, 'wine_still', 'Châteauneuf-du-Pape AOC', 'Château Beaucastel CdP Rouge — the most age-worthy Châteauneuf; high Mourvèdre (30%) gives extraordinary complexity: leather, game, dark fruit, pepper, garrigue; biodynamic; 30+ year potential',
 'fungi_truffles', 'earthy_herbal', 'Truffe noire en croûte sel gros (whole black truffle baked in salt crust) — the most dramatic Périgord truffle preparation for a wine of maximum depth',
 'complement', 'Beaucastel at 20+ years develops truffle notes from its Mourvèdre; serving a whole truffle baked in salt crust mirrors these evolving aromatics; a legendary pairing among southern Rhône wine enthusiasts', 'main', 'established', 1, true),

-- ============================================================
-- 240: Vernay Coteau de Vernon Condrieu (1; need 4 more)
-- The benchmark Condrieu; Viognier; extraordinary apricot-floral character
-- ============================================================
(240, 'wine_still', 'Condrieu AOC', 'Georges Vernay Coteau de Vernon — the benchmark Condrieu Viognier; from the steepest original terraces above the Rhône; extraordinary apricot, peach, honeysuckle, white flower, spice; 10+ year aging',
 'seafood', 'delicate_fresh', 'Homard thermidor (lobster in cream-Gruyère-mustard sauce) — the classic French preparation for the Rhône''s great white wine',
 'complement', 'Condrieu''s apricot-honeysuckle and the lobster thermidor''s cream-Gruyère richness create one of France''s great white wine-shellfish moments; the wine''s acidity cuts the cream while the floral character elevates it', 'main', 'established', 1, true),

(240, 'wine_still', 'Condrieu AOC', 'Georges Vernay Coteau de Vernon — the benchmark Condrieu Viognier; from the steepest original terraces above the Rhône; extraordinary apricot, peach, honeysuckle, white flower, spice; 10+ year aging',
 'meat_poultry', 'earthy_herbal', 'Poulet de Bresse en cocotte avec abricots, gingembre, et miel (Bresse chicken with apricots, ginger, and honey) — the floral-spiced preparation that mirrors Condrieu''s apricot character',
 'complement', 'Condrieu''s apricot and floral character creates a seamless bridge with apricot-ginger poultry preparations; the honey bridges the wine''s natural sweetness while Bresse chicken''s fat supports the Viognier''s rich texture', 'main', 'classic', 1, true),

(240, 'wine_still', 'Condrieu AOC', 'Georges Vernay Coteau de Vernon — the benchmark Condrieu Viognier; from the steepest original terraces above the Rhône; extraordinary apricot, peach, honeysuckle, white flower, spice; 10+ year aging',
 'seafood', 'umami_savoury', 'Coquilles Saint-Jacques avec beurre d''abricot et safran (scallops with apricot butter and saffron) — the most sophisticated scallop preparation for Condrieu',
 'complement', 'Condrieu''s apricot and saffron-adjacent spice are mirrored in the abricot beurre and saffron preparation; scallops'' sweet sea-cream bridges the wine''s honeysuckle-cream character', 'starter', 'classic', 1, true),

(240, 'wine_still', 'Condrieu AOC', 'Georges Vernay Coteau de Vernon — the benchmark Condrieu Viognier; from the steepest original terraces above the Rhône; extraordinary apricot, peach, honeysuckle, white flower, spice; 10+ year aging',
 'dessert_pastry', 'sweet_fruity', 'Tarte aux abricots et fleurs de lavande (apricot-lavender tart) — Condrieu''s dominant fruit served in tart form alongside the wine that made it famous',
 'complement', 'Apricot''s stone fruit character is the defining aromatic of Condrieu; a tart built around fresh apricots and lavender creates the most direct possible food mirror for this wine; lavender adds the Provençal bridge', 'dessert', 'suggested', 1, true),

-- ============================================================
-- 241: Krug Grande Cuvée (1; need 4 more)
-- Champagne's most powerful multi-vintage cuvée; toasted bread, honey, cream
-- ============================================================
(241, 'wine_sparkling', 'Champagne AOC', 'Krug Grande Cuvée — Champagne''s most powerful and complex multi-vintage cuvée; 120+ reserve wines from multiple years; brioche, toasted hazelnut, cream, honey, ginger; extraordinary complexity and longevity',
 'seafood', 'salty_mineral', 'Beluga or Osciètre caviar (50g service) with toast and crème fraîche — the most classic prestige Champagne pairing',
 'complement', 'Krug Grande Cuvée and Beluga caviar is the world''s most iconic prestige pairing; the wine''s brioche-toasted complexity provides the structural counterpoint to caviar''s brine-sea; crème fraîche bridges the cream notes', 'aperitif', 'classic', 1, true),

(241, 'wine_sparkling', 'Champagne AOC', 'Krug Grande Cuvée — Champagne''s most powerful and complex multi-vintage cuvée; 120+ reserve wines from multiple years; brioche, toasted hazelnut, cream, honey, ginger; extraordinary complexity and longevity',
 'seafood', 'delicate_fresh', 'Homard rôti au four avec beurre Krug (lobster basted with the wine''s own lees-aged butter) — the most theatrical Champagne pairing',
 'complement', 'Krug''s toasted-cream power is one of the few Champagnes that can match a whole roasted lobster; the wine''s brioche and hazelnut echo a beurre noisette preparation; a prestige pairing of the highest level', 'main', 'classic', 1, true),

(241, 'wine_sparkling', 'Champagne AOC', 'Krug Grande Cuvée — Champagne''s most powerful and complex multi-vintage cuvée; 120+ reserve wines from multiple years; brioche, toasted hazelnut, cream, honey, ginger; extraordinary complexity and longevity',
 'seafood', 'umami_savoury', 'Fricassée de homard, Saint-Jacques, et langoustines (shellfish fricassée with cream and herbs) — three prestige shellfish in one preparation for Krug''s complexity',
 'complement', 'Krug''s exceptional complexity (representing multiple vintages) can handle a multi-shellfish preparation; the cream sauce bridges the wine''s own cream notes; the three shellfish create layered flavours that match the wine''s layers', 'main', 'established', 1, true),

(241, 'wine_sparkling', 'Champagne AOC', 'Krug Grande Cuvée — Champagne''s most powerful and complex multi-vintage cuvée; 120+ reserve wines from multiple years; brioche, toasted hazelnut, cream, honey, ginger; extraordinary complexity and longevity',
 'charcuterie_cheese', 'fermented_aged', 'Comté 36-month ''alpages'' with Périgord truffle shavings — the most complex cheese pairing for the most complex Champagne',
 'complement', 'Krug''s extraordinary depth and the 36-month Comté''s nutty-crystalline character create a multi-dimensional pairing; black truffle shavings bridge the wine''s earthy secondary complexity', 'cheese', 'established', 1, true),

-- ============================================================
-- 242: Salon Blanc de Blancs Le Mesnil-sur-Oger (1; need 4 more)
-- Single-village, single-vintage, single-variety; razor mineral
-- ============================================================
(242, 'wine_sparkling', 'Champagne AOC', 'Salon Blanc de Blancs — the most minimalist Champagne: single-village (Le Mesnil-sur-Oger), single-vintage (only exceptional years), single variety (Chardonnay); pure chalk mineral, citrus precision, extraordinary longevity',
 'seafood', 'salty_mineral', 'Belons (flat oysters from Brittany) — the most mineral and complex oyster for the most mineral Champagne',
 'complement', 'Salon''s pure chalk-mineral character is the ideal match for Belon oysters'' extraordinary mineral-iodine intensity; both are expressions of pure minerality rather than fruit; a pairing of rare intellectual resonance', 'aperitif', 'classic', 1, true),

(242, 'wine_sparkling', 'Champagne AOC', 'Salon Blanc de Blancs — the most minimalist Champagne: single-village (Le Mesnil-sur-Oger), single-vintage (only exceptional years), single variety (Chardonnay); pure chalk mineral, citrus precision, extraordinary longevity',
 'seafood', 'delicate_fresh', 'Turbot de ligne poché avec caviar et citron (line-caught turbot poached with caviar) — the most delicate French fish preparation for the most precise Champagne',
 'complement', 'Salon''s lemon-chalk precision and turbot''s extraordinary delicacy are perfectly proportioned; caviar''s brine provides mineral depth while the white wine''s mineral echo creates seamless continuity', 'main', 'classic', 1, true),

(242, 'wine_sparkling', 'Champagne AOC', 'Salon Blanc de Blancs — the most minimalist Champagne: single-village (Le Mesnil-sur-Oger), single-vintage (only exceptional years), single variety (Chardonnay); pure chalk mineral, citrus precision, extraordinary longevity',
 'seafood', 'salty_mineral', 'Langoustines crues avec fleur de sel et citron vert — raw langoustines dressed only with fleur de sel and lime; the preparation that strips everything back to the ingredient',
 'complement', 'Salon''s minimalism (single-village, single-variety) demands a preparation of equivalent purity; raw langoustines dressed only with salt and lime mirrors the wine''s approach to showcasing single-terroir mineral purity', 'starter', 'established', 1, true),

(242, 'wine_sparkling', 'Champagne AOC', 'Salon Blanc de Blancs — the most minimalist Champagne: single-village (Le Mesnil-sur-Oger), single-vintage (only exceptional years), single variety (Chardonnay); pure chalk mineral, citrus precision, extraordinary longevity',
 'seafood', 'umami_savoury', 'Sea urchin (oursins) with lemon and toast — the sea urchin''s extraordinary mineral-sweet-iodine character for the most mineral Champagne',
 'complement', 'Sea urchin''s extraordinary combination of sweetness and intense marine mineral is one of wine''s great pairing challenges; Salon''s chalk-mineral and citrus precision are perfectly calibrated for the urchin''s character', 'aperitif', 'classic', 1, true),

-- ============================================================
-- 243: Dom Pérignon P1 Vintage (1; need 4 more)
-- The world's most famous vintage Champagne; balanced, complex, prestige
-- ============================================================
(243, 'wine_sparkling', 'Champagne AOC', 'Dom Pérignon P1 Vintage — Moët''s legendary vintage cuvée; Pinot Noir and Chardonnay from premier crus; the world''s most recognised Champagne; balanced, elegant, brioche, lemon cream, chalk',
 'seafood', 'salty_mineral', 'Smoked salmon blinis with crème fraîche, dill, and Osciètre caviar — the prestige aperitivo that showcases Dom Pérignon''s balanced character',
 'complement', 'Dom Pérignon and smoked salmon-caviar is a globally recognised pairing: the wine''s balanced cream-mineral and the salmon-caviar''s brine-smoke are in harmony; the crème fraîche bridges the cream notes', 'aperitif', 'classic', 1, true),

(243, 'wine_sparkling', 'Champagne AOC', 'Dom Pérignon P1 Vintage — Moët''s legendary vintage cuvée; Pinot Noir and Chardonnay from premier crus; the world''s most recognised Champagne; balanced, elegant, brioche, lemon cream, chalk',
 'seafood', 'delicate_fresh', 'Noix de Saint-Jacques with Granny Smith apple, celery, and caviar — the contemporary French fine-dining preparation using Dom Pérignon''s own flavour profile as inspiration',
 'complement', 'Dom Pérignon''s apple-chalk-cream profile is directly mirrored in a scallop preparation with Granny Smith apple and celery''s green crispness; caviar bridges the mineral depth', 'starter', 'established', 1, true),

(243, 'wine_sparkling', 'Champagne AOC', 'Dom Pérignon P1 Vintage — Moët''s legendary vintage cuvée; Pinot Noir and Chardonnay from premier crus; the world''s most recognised Champagne; balanced, elegant, brioche, lemon cream, chalk',
 'meat_poultry', 'delicate_fresh', 'Poularde pochée au Champagne (hen poached in Champagne) — the classic French preparation of poultry in sparkling wine',
 'complement', 'Poularde pochée au Champagne uses the wine in the cooking liquid; serving Dom Pérignon alongside creates full circle integration; the hen''s rich fat is balanced by the wine''s acidity and bubbles', 'main', 'classic', 1, true),

(243, 'wine_sparkling', 'Champagne AOC', 'Dom Pérignon P1 Vintage — Moët''s legendary vintage cuvée; Pinot Noir and Chardonnay from premier crus; the world''s most recognised Champagne; balanced, elegant, brioche, lemon cream, chalk',
 'seafood', 'umami_savoury', 'Risotto au Champagne et langoustines (Champagne risotto with langoustines) — cooking with and serving the same wine creates seamless integration',
 'complement', 'Risotto cooked with Dom Pérignon and served alongside it creates a wine-food integration where the cooking wine''s reduction concentrates the Champagne''s apple-cream notes in the rice', 'main', 'established', 1, true),

-- ============================================================
-- 244: Pierre Péters Les Chétillons Blanc de Blancs (1; need 4 more)
-- Grower Champagne; single vineyard; chalk mineral, lemon, precise
-- ============================================================
(244, 'wine_sparkling', 'Champagne AOC', 'Pierre Péters Les Chétillons — the benchmark single-vineyard grower Champagne from Le Mesnil-sur-Oger; pure chalk minerality, lemon zest, white peach, extraordinarily precise; Chardonnay only',
 'seafood', 'salty_mineral', 'Marennes-Oléron claires (Grade 3 oysters, 3-month claires finishing) with eschalot mignonette — the terroir oyster for a terroir Champagne',
 'complement', 'Les Chétillons'' pure chalk mineral is the ideal frame for fines de claires oysters; both speak of a specific terroir; the claires finishing gives the oyster a salinity that the wine''s lemon-chalk amplifies', 'aperitif', 'classic', 1, true),

(244, 'wine_sparkling', 'Champagne AOC', 'Pierre Péters Les Chétillons — the benchmark single-vineyard grower Champagne from Le Mesnil-sur-Oger; pure chalk minerality, lemon zest, white peach, extraordinarily precise; Chardonnay only',
 'seafood', 'delicate_fresh', 'Carpaccio de bar avec citron vert, huile d''olive, et fleur de sel — sea bass carpaccio at its most minimal for the most mineral Champagne',
 'complement', 'Les Chétillons'' mineral precision demands the most delicate raw fish preparation; sea bass carpaccio dressed only with lime and olive oil creates a flavour purity that matches the wine''s single-vineyard character', 'starter', 'established', 1, true),

(244, 'wine_sparkling', 'Champagne AOC', 'Pierre Péters Les Chétillons — the benchmark single-vineyard grower Champagne from Le Mesnil-sur-Oger; pure chalk minerality, lemon zest, white peach, extraordinarily precise; Chardonnay only',
 'charcuterie_cheese', 'fermented_aged', 'Crottin de Chavignol (fresh-to-mature, 3-week) with honey and walnuts — goat cheese and Blanc de Blancs is a classic French pairing',
 'complement', 'Blanc de Blancs Champagne and goat''s cheese is a well-established French pairing; Les Chétillons'' chalk and lemon character complement the Crottin''s lactic sharpness and mineral character', 'cheese', 'established', 1, true),

(244, 'wine_sparkling', 'Champagne AOC', 'Pierre Péters Les Chétillons — the benchmark single-vineyard grower Champagne from Le Mesnil-sur-Oger; pure chalk minerality, lemon zest, white peach, extraordinarily precise; Chardonnay only',
 'seafood', 'umami_savoury', 'Crème de petits pois avec des saint-Jacques poêlées et truffe blanche — pea cream soup with seared scallops and white truffle',
 'complement', 'The pea cream''s green-sweet character provides an aromatic bridge to Les Chétillons'' white peach note; scallops'' sea-cream mirrors the wine''s mineral-cream; white truffle amplifies the earthy depth', 'starter', 'suggested', 1, true),

-- ============================================================
-- 245: Bollinger Special Cuvée (1; need 4 more)
-- Pinot Noir dominant NV; full-bodied, brioche, red fruit, firm
-- ============================================================
(245, 'wine_sparkling', 'Champagne AOC', 'Bollinger Special Cuvée NV — Pinot Noir dominant (60%+) from grand and premier crus; the most full-bodied major NV Champagne; toasted brioche, red apple, red cherry, firm mousse; the James Bond Champagne',
 'seafood', 'umami_savoury', 'Fish and chips with malt vinegar and mushy peas — Bollinger''s full body and firm mousse make it the world''s greatest fish and chips Champagne',
 'complement', 'Bollinger and fish and chips is an established Anglo-French pairing: the wine''s Pinot Noir backbone provides the structure for the frying batter while the mousse refreshes; the malt vinegar''s acidity contrasts the wine''s richness', 'casual', 'classic', 2, true),

(245, 'wine_sparkling', 'Champagne AOC', 'Bollinger Special Cuvée NV — Pinot Noir dominant (60%+) from grand and premier crus; the most full-bodied major NV Champagne; toasted brioche, red apple, red cherry, firm mousse; the James Bond Champagne',
 'charcuterie_cheese', 'fermented_aged', 'Jambon de Paris (French ham hock) with cornichons and Dijon beurre blanc — the most Parisian ham preparation for a Pinot Noir-dominant Champagne',
 'complement', 'Bollinger''s Pinot Noir red-fruit character bridges with ham''s sweet pork; cornichons'' acidity creates tension against the firm mousse; a Parisian bistro pairing of unexpected elegance', 'aperitif', 'established', 2, true),

(245, 'wine_sparkling', 'Champagne AOC', 'Bollinger Special Cuvée NV — Pinot Noir dominant (60%+) from grand and premier crus; the most full-bodied major NV Champagne; toasted brioche, red apple, red cherry, firm mousse; the James Bond Champagne',
 'charcuterie_cheese', 'fermented_aged', 'Chaource AOP (Champagne region soft cheese, 4-week) — the cheese from the Aube department of Champagne itself',
 'complement', 'Chaource is produced in the Aube, one of Bollinger''s source villages; the soft white-mould cheese''s cream-mushroom character resonates with the Special Cuvée''s brioche and depth', 'cheese', 'classic', 2, true),

(245, 'wine_sparkling', 'Champagne AOC', 'Bollinger Special Cuvée NV — Pinot Noir dominant (60%+) from grand and premier crus; the most full-bodied major NV Champagne; toasted brioche, red apple, red cherry, firm mousse; the James Bond Champagne',
 'meat_poultry', 'earthy_herbal', 'Boudin noir (blood sausage) with apple compote and lardons — the classic Parisian preparation using Bollinger''s Pinot Noir character to bridge the blood sausage''s iron',
 'bridge', 'Blood sausage''s iron-pork character bridges with Bollinger''s Pinot Noir backbone; the apple compote mirrors the wine''s red apple note; a sophisticated bistro pairing that shows Champagne''s food range', 'main', 'adventurous', 2, true),

-- ============================================================
-- 246: Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru (1; need 4 more)
-- 100% Pinot Noir from Ambonnay; the most structured blanc de noirs
-- ============================================================
(246, 'wine_sparkling', 'Champagne AOC', 'Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru — 100% Pinot Noir vinified as white from the village of Ambonnay; extraordinary depth and structure; red cherry, minerals, brioche; the most wine-like Champagne',
 'meat_poultry', 'earthy_herbal', 'Poulet rôti aux champignons sauvages (roasted chicken with wild mushrooms) — the blanc de noirs'' Pinot Noir structure can approach poultry with earthy accompaniment',
 'complement', 'Egly-Ouriet''s Pinot Noir-dominant structure makes it one of the few Champagnes that works with roasted poultry; wild mushrooms bridge the wine''s earthy secondary notes; the bubbles lift the cream jus', 'main', 'established', 1, true),

(246, 'wine_sparkling', 'Champagne AOC', 'Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru — 100% Pinot Noir vinified as white from the village of Ambonnay; extraordinary depth and structure; red cherry, minerals, brioche; the most wine-like Champagne',
 'charcuterie_cheese', 'fermented_aged', 'Reblochon fermier de Savoie (farm-produced, 6-week) — the structured Pinot Noir base of the Blanc de Noirs can handle the earthy washed-rind',
 'complement', 'Egly-Ouriet''s Pinot Noir structure and earthy secondary notes are proportioned for a mild washed-rind; Reblochon fermier''s cream-mushroom provides the bridge; a sophisticated Champagne-cheese combination', 'cheese', 'established', 1, true),

(246, 'wine_sparkling', 'Champagne AOC', 'Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru — 100% Pinot Noir vinified as white from the village of Ambonnay; extraordinary depth and structure; red cherry, minerals, brioche; the most wine-like Champagne',
 'seafood', 'salty_mineral', 'Caviar de Neuvic (French sturgeon caviar from Périgord) with potato blinis — the French-produced alternative to Russian caviar for a grower Champagne',
 'complement', 'French sturgeon caviar from Périgord and a grower Champagne of artisan integrity are both expressions of French product quality; the Blanc de Noirs'' structure bridges the caviar''s brine while its depth matches the eggs'' richness', 'aperitif', 'established', 1, true),

(246, 'wine_sparkling', 'Champagne AOC', 'Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru — 100% Pinot Noir vinified as white from the village of Ambonnay; extraordinary depth and structure; red cherry, minerals, brioche; the most wine-like Champagne',
 'meat_poultry', 'rich_fatty_smoky', 'Terrine de foie gras de canard with Champagne jelly and brioche grillée — the Champagne region''s traditional foie gras preparation',
 'complement', 'Foie gras with Champagne jelly uses the wine as both cooking liquid and companion; Egly-Ouriet''s Pinot Noir base and depth make it one of the finest Champagnes for foie gras; brioche mirrors the wine''s own toasted brioche notes', 'starter', 'classic', 1, true);

COMMIT;
