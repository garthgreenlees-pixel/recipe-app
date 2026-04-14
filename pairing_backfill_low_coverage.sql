BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 171: Fortaleza Blanco Tequila (needs 1 more)
(171, 'spirits_agave', 'Fortaleza Blanco Tequila',
 'Agave-sweet, herbal, cooked agave, citrus, white pepper, floral, mineral; traditional Jalisco.',
 'seafood', 'ceviche aguachile',
 'Aguachile with shrimp, cucumber and lime; the tequila''s cooked-agave sweetness and citrus-pepper character create Mexico''s most iconic spirits-seafood pairing.',
 'complement', 'Citrus and white pepper in tequila echo the lime and chilli of aguachile; agave sweetness balances the acid; mineral note bridges ocean-fresh shrimp.',
 'starter', 'classic', 1, true),

-- 173: Uncle Nearest 1884 (needs 1 more)
(173, 'spirits_whiskey', 'Tennessee Whiskey Lincoln County Process',
 'Vanilla, maple, honey, butterscotch, dried fruit, silky, gentle spice.',
 'pastry_dessert', 'pecan pie maple',
 'Pecan pie with maple syrup or bourbon-soaked sticky bun; the whiskey''s maple-vanilla profile finds an almost exact mirror in classic Southern baked confection.',
 'complement', 'Maple and vanilla in whiskey echo the sweetener and flavour of pecan pie directly; butterscotch bridges the caramelised nut richness; gentle spice adds depth.',
 'dessert', 'classic', 2, true),

-- 174: Clairin Sajous (needs 1 more)
(174, 'spirits_rum', 'Clairin Artisanal Haitian',
 'Sugarcane fresh, citrus, tropical fruit, green herb, mineral, floral.',
 'fruit', 'tropical citrus',
 'Fresh Haitian tropical fruit platter — mango, passion fruit, soursop — or griot (fried marinated pork) with pikliz (spiced pickled vegetables).',
 'complement', 'Tropical fruit in clairin mirrors fresh mango and passion fruit; mineral backbone grounds the sweetness; green herb note bridges pikliz''s herbal-spice character.',
 'casual', 'classic', 2, true),

-- 175: Opus One (needs 1 more)
(175, 'wine_still', 'Napa Valley Bordeaux Blend',
 'Cassis, blackcurrant, cedar, graphite, dark chocolate, violets, tobacco, plum.',
 'meat', 'wagyu beef',
 'A5 Wagyu ribeye or dry-aged prime rib; Opus One''s generous Napa richness demands the most luxurious beef — the definitive California wine-beef pairing.',
 'complement', 'Cassis and graphite tannin integrate with Wagyu''s extraordinary marbling; dark chocolate in wine bridges the umami depth of A5 fat; violets provide an aromatic lift.',
 'main', 'classic', 1, true),

-- 176: Ridge Monte Bello (needs 2 more)
(176, 'wine_still', 'Santa Cruz Mountains Cabernet Sauvignon',
 'Cassis, mineral, eucalyptus, cedar, chalk, iron, dark fruit.',
 'meat', 'lamb roasted',
 'Rack of lamb with Dijon and herbs; the wine''s chalk-mineral and eucalyptus finesse find a natural partner in herb-roasted California lamb.',
 'complement', 'Eucalyptus and cedar of Monte Bello echo Provençal herb crust; chalk mineral mirrors the lamb bone''s mineral character; cassis provides fruit structure.',
 'main', 'classic', 1, true),

(176, 'wine_still', 'Santa Cruz Mountains Cabernet Sauvignon',
 'Cassis, mineral, eucalyptus, cedar, chalk, iron, dark fruit.',
 'cheese', 'aged hard cave',
 'Cave-aged Comté or Montgomery''s Cheddar; the wine''s iron-mineral depth and chalk structure require a cheese of equivalent complexity and age.',
 'complement', 'Iron and chalk mineral in wine mirror the cave-aged complexity of Comté; cedar bridges the cheese''s caramelised crystalline notes; cassis provides fruit contrast.',
 'cheese', 'established', 1, true),

-- 177: Penfolds Grange (needs 1 more)
(177, 'wine_still', 'Penfolds Grange Barossa Shiraz',
 'Blackberry, blueberry, dark chocolate, American oak vanilla, iron, leather, tar, eucalyptus.',
 'meat', 'kangaroo game',
 'Kangaroo loin with juniper and native pepper berry; Australia''s most iconic wine paired with its most distinctive native protein — a sense-of-place celebration of rare pedigree.',
 'complement', 'Iron and leather in Grange mirror kangaroo''s iron-dense game character; native pepper berry echoes the wine''s spice; eucalyptus provides a botanical bridge.',
 'main', 'adventurous', 1, true),

-- 178: Henschke Hill of Grace (needs 1 more)
(178, 'wine_still', 'Eden Valley Shiraz Grand Vin',
 'Blueberry, violets, black pepper, iron-ore, licorice, eucalyptus, floral.',
 'meat', 'venison loganberry',
 'Venison loin with loganberry reduction and root vegetables; the wine''s violet and blueberry-iron character finds a natural partner in fine game preparations.',
 'complement', 'Violet and blueberry in wine mirror the loganberry jus; iron-ore resonates with venison''s game mineral character; eucalyptus adds a distinctive aromatic bridge.',
 'main', 'adventurous', 1, true),

-- 181: Catena Zapata Adrianna Malbec (needs 1 more)
(181, 'wine_still', 'Adrianna Vineyard High-Altitude Malbec',
 'Violets, blueberry, graphite, black pepper, mineral, licorice, fine tannin.',
 'meat', 'asado beef',
 'Argentine asado — short ribs or flank steak cooked over wood coals; the wine''s violet-blueberry intensity and fine tannin are the apex of the Argentine asado-Malbec tradition.',
 'complement', 'Violet and blueberry of Adrianna Malbec are the definitive asado pairing; graphite fine tannin integrates with wood-char richness; black pepper echoes the seasoning.',
 'main', 'classic', 1, true),

-- 182: Sadie Family Columella (needs 1 more)
(182, 'wine_still', 'Swartland Syrah-Mourvèdre Old Vine',
 'Iron-ore, dark olive, violets, black pepper, smoked meat, Provençal herbs, plum.',
 'meat', 'lamb slow-braised',
 'Slow-braised Cape Karoo lamb with olives and herbs; the wine''s smoked-meat, iron and Provençal herb character mirrors the Swartland''s natural affinity with braised lamb.',
 'complement', 'Provençal herbs in wine echo the olive and herb braising base; iron-ore bridges the lamb''s mineral character; dark olive note mirrors the tapenade garnish.',
 'main', 'classic', 1, true),

-- 183: Macallan 12 Year Sherry Oak (needs 1 more)
(183, 'spirits_whiskey', 'Speyside Single Malt Sherry Cask',
 'Dried fruit, orange peel, Christmas cake, nutmeg, dark chocolate, butterscotch, ginger spice.',
 'pastry_dessert', 'Christmas pudding',
 'Christmas pudding with brandy butter or Stollen; the Macallan''s Christmas-cake profile finds a literal match in the festive dessert.',
 'complement', 'Christmas cake aromatic in whisky mirrors the spiced dried fruit of Christmas pudding exactly; butterscotch bridges the brandy butter richness; ginger spice echoes cinnamon-nutmeg.',
 'dessert', 'classic', 1, true),

-- 185: Springbank 10 Year Campbeltown (needs 1 more)
(185, 'spirits_whiskey', 'Campbeltown Single Malt',
 'Sea salt, brine, orchard fruit, slight peat, vanilla, old cellar, mineral.',
 'seafood', 'smoked kippers',
 'Smoked kippers or Arbroath Smokies; the whisky''s brine and slight peat character find their most natural Scottish coastal partner.',
 'complement', 'Sea salt and brine in whisky echo the cured, smoked fish character; slight peat mirrors the smoking process; vanilla softens the pairing''s saline intensity.',
 'starter', 'classic', 2, true),

-- 187: Weihenstephan Hefeweissbier (needs 1 more)
(187, 'beer_ale', 'Bavarian Hefeweizen',
 'Banana, clove, bubblegum, wheat, citrus, refreshing; world''s oldest brewery.',
 'grain', 'pretzel bavarian',
 'Bavarian pretzel with weisswurst (veal sausage) and sweet mustard; the definitive Bavarian breakfast combination — beer, sausage and pretzel in their original context.',
 'complement', 'Banana ester in Hefeweizen complements the veal sweetness of Weisswurst; clove spice bridges the caraway in pretzel; carbonation cuts the sausage richness.',
 'casual', 'classic', 2, true),

-- 188: Leitz Eins Zwei Zero Riesling (needs 1 more)
(188, 'na_dealcoholised', 'Dealcoholised Riesling NA',
 'Citrus, slate mineral, lime, fresh apple, white peach; 0.0% alcohol.',
 'seafood', 'scallops seared',
 'Seared scallops with cauliflower purée; the wine''s citrus mineral precision pairs elegantly with delicate seared scallop — ideal for non-alcohol contexts.',
 'complement', 'Slate mineral echoes the scallop''s clean oceanic character; lime and citrus acidity cut through the sweet scallop and cauliflower richness.',
 'main', 'established', 1, true),

-- 189: Seedlip Spice 94 (needs 2 more)
(189, 'na_crafted', 'Distilled NA Spirit — Spice',
 'Allspice, cardamom, oak bark, citrus peel, warm spice, dry bitter.',
 'seafood', 'spiced seafood',
 'Spiced crab cakes with remoulade or grilled shrimp with allspice; the spirit''s allspice-cardamom warmth creates an unexpected but highly functional pairing with spiced seafood.',
 'complement', 'Allspice in spirit mirrors allspice in crab cake seasoning directly; cardamom bridges the remoulade''s aromatic complexity; dry bitter finish cleanses fried coating.',
 'starter', 'adventurous', 1, true),

(189, 'na_crafted', 'Distilled NA Spirit — Spice',
 'Allspice, cardamom, oak bark, citrus peel, warm spice, dry bitter.',
 'cheese', 'aged hard spiced',
 'Aged Manchego with quince paste or aged Gouda with black pepper; the spirit''s warm spice and dry bitter profile complements aged hard cheese with accompaniments.',
 'complement', 'Allspice and cardamom in spirit bridge the warm spice of quince paste; oak bark mirrors the Manchego''s aged tannin; dry bitter finish cleanses the palate.',
 'casual', 'established', 1, true),

-- 190: GT's Synergy Kombucha Gingerade (needs 1 more)
(190, 'na_fermented', 'Live Fermented Kombucha',
 'Ginger, acetic acid, tea, apple, effervescent, refreshing.',
 'grain', 'sushi rolls',
 'Vegetable sushi rolls or onigiri; the kombucha''s ginger and acetic character mirror the traditional accompaniments to Japanese rice preparations.',
 'complement', 'Ginger in kombucha echoes pickled ginger sushi condiment; acetic acid mirrors rice vinegar in sushi rice; apple brightness lifts the savoury nori-rice combination.',
 'casual', 'established', 1, true),

-- 466: Vanuatu Noble Kava Export (needs 1 more)
(466, 'traditional_cultural', 'Vanuatu Noble Kava Powder',
 'Pepper, earth, mild sweet, nutty undertone, kavalactone warmth.',
 'grain', 'nuts roasted',
 'Roasted macadamia nuts or salted roasted cashews; the kava''s nutty undertone finds a direct mirror in roasted tree nuts while the fat moderates kavalactone intensity.',
 'complement', 'Nutty undertone in kava echoes the roasted macadamia character directly; fat content of tree nuts moderates kavalactone absorption; salt amplifies the kava''s mineral undertone.',
 'casual', 'established', 1, true),

-- 467: Lehua Hawaiian Awa (needs 1 more)
(467, 'traditional_cultural', 'Hawaiian Awa Ceremonial',
 'Earthy sweet, light floral, mild numbing, nutty, gentle pepper.',
 'grain', 'haupia coconut pudding',
 'Haupia (Hawaiian coconut pudding) or sweet potato mochi; light coconut sweetness tempers awa''s earthiness while anchoring the Hawaiian cultural context.',
 'complement', 'Earthy sweetness in awa bridges the gentle coconut sweetness of haupia; light floral note harmonises with vanilla in mochi; gentle pepper is refreshed by the clean dairy fat.',
 'dessert', 'established', 2, true),

-- 468: Samoan Ava (needs 1 more)
(468, 'traditional_cultural', 'Samoan Ava Ceremony',
 'Mild earthy, slightly sour, cooling, light pepper; fa''asamoa custom.',
 'fruit', 'coconut fresh',
 'Fresh green coconut water or coconut cream desserts; ava and fresh coconut are both central to Samoan ceremony and refreshment culture.',
 'complement', 'Coconut water''s fresh sweetness contrasts ava''s mild sourness; cooling effect of both creates a sense of refreshment and ceremony; cultural coherence of Pacific island tradition.',
 'casual', 'classic', 3, true),

-- 470: Ilocos Basi (needs 1 more)
(470, 'traditional_cultural', 'Ilocos Basi Sugarcane Wine',
 'Dried fig, bark tannin, brown sugar, tamarind, dark fruit, herbal bitter.',
 'meat', 'dinuguan pork blood',
 'Dinuguan (Filipino pork blood stew) or sizzling sisig; the wine''s dark fruit and herbal-bitter character complement the richly savory, fatty Filipino pork preparations.',
 'complement', 'Dark fruit and bark tannin in Basi bridge the deep savoury richness of dinuguan; brown sugar and tamarind echo the stew''s sweet-sour pork character; herbal bitter cleanses the fat.',
 'main', 'adventurous', 3, true);

COMMIT;
