BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 154: Taki Mai Noble Kava — Waka Premium
(154, 'traditional_cultural', 'Fijian Noble Kava Waka',
 'Earthy, peppery, mild numbing, coconut earth, clean finish; Waka lateral root premium.',
 'grain', 'coconut starchy',
 'Fresh coconut water or ripe coconut flesh; the traditional Fijian accompaniment — cool, clean sweetness of coconut immediately tempers the kavalactone earthiness.',
 'bridge', 'Coconut fat tempers kavalactone absorption; natural sweetness bridges kava''s earthy-peppery bitterness; Pacific island cultural coherence.',
 'casual', 'classic', 3, true),

-- 171: Fortaleza Blanco Tequila (+1)
(171, 'spirits_agave', 'Fortaleza Blanco Tequila',
 'Agave-sweet, herbal, cooked agave, citrus, white pepper, floral, mineral; traditional Jalisco.',
 'meat', 'pork al pastor',
 'Pork al pastor with pineapple and cilantro; the tequila''s cooked-agave sweetness and citrus character complement the achiote-marinated pork in its most iconic Mexican street context.',
 'complement', 'Cooked agave sweetness mirrors the caramelised pork fat and pineapple; citrus-pepper in tequila echoes the achiote marinade; white pepper bridges the chilli seasoning.',
 'casual', 'classic', 1, true),

-- 172: Buffalo Trace Kentucky Bourbon
(172, 'spirits_whiskey', 'Kentucky Straight Bourbon Whiskey',
 'Vanilla, caramel, brown sugar, cherry, oak spice, gentle heat; Buffalo Trace mash bill.',
 'meat', 'BBQ brisket smoked',
 'Hickory-smoked beef brisket with Kansas City-style molasses BBQ sauce; the bourbon''s vanilla-caramel profile mirrors the molasses in the sauce while the cherry note resonates with the wood smoke.',
 'complement', 'Vanilla and caramel in bourbon echo the molasses BBQ sauce; cherry note bridges the wood smoke character; oak spice reinforces the hickory smoking aromatics.',
 'main', 'classic', 1, true),

-- 173: Uncle Nearest 1884 (+1)
(173, 'spirits_whiskey', 'Tennessee Whiskey Lincoln County Process',
 'Vanilla, maple, honey, butterscotch, dried fruit, silky, gentle spice.',
 'meat', 'smoked pulled pork',
 'Slow-smoked pulled pork with bourbon-apple cider baste; Uncle Nearest''s maple and honey profile creates a natural affinity with apple-glazed smoked pork and the broader Southern BBQ tradition.',
 'complement', 'Maple and honey in whiskey mirror the apple cider baste; butterscotch bridges the caramelised pork fat; gentle spice echoes the dry rub seasoning.',
 'main', 'classic', 2, true),

-- 174: Clairin Sajous (+1)
(174, 'spirits_rum', 'Clairin Artisanal Haitian',
 'Sugarcane fresh, citrus, tropical fruit, green herb, mineral, floral.',
 'meat', 'griot fried pork',
 'Griot (Haitian crispy fried marinated pork) with diri ak djon djon (black mushroom rice); the clairin''s green herb and citrus character mirrors the Scotch bonnet and lime in the griot marinade.',
 'complement', 'Green herb in clairin bridges the Scotch bonnet pepper character; citrus mirrors the sour orange in the marinade; mineral note grounds the tropical spice combination.',
 'main', 'established', 2, true),

-- 175: Opus One (+1)
(175, 'wine_still', 'Napa Valley Bordeaux Blend',
 'Cassis, blackcurrant, cedar, graphite, dark chocolate, violets, tobacco, plum.',
 'cheese', 'aged hard cave',
 'Montgomery''s Cheddar or Fiscalini Bandage Wrapped Cheddar; the wine''s cedar and graphite structure finds a worthy counterpart in the complex nutty-sharp depth of a fine aged American or English farmhouse Cheddar.',
 'complement', 'Graphite tannin integrates with aged Cheddar''s crystalline texture; cedar bridges the cheese''s butterscotch caramel depth; cassis provides fruit contrast against savoury cheese.',
 'cheese', 'established', 1, true),

-- 176: Ridge Monte Bello (+1, now has 3 already)
(176, 'wine_still', 'Santa Cruz Mountains Cabernet Sauvignon',
 'Cassis, mineral, eucalyptus, cedar, chalk, iron, dark fruit.',
 'meat', 'beef short ribs',
 'Braised beef short ribs with rosemary and garlic; Monte Bello''s mineral-eucalyptus structure integrates beautifully with the rich gelatinous short rib braising — a California terroir and cooking tradition pairing.',
 'complement', 'Iron mineral in wine mirrors the deep collagen richness of braised short rib; eucalyptus bridges the rosemary herb; cedar provides structural contrast to the richness.',
 'main', 'established', 1, true),

-- 177: Penfolds Grange (+1)
(177, 'wine_still', 'Penfolds Grange Barossa Shiraz',
 'Blackberry, blueberry, dark chocolate, American oak vanilla, iron, leather, tar, eucalyptus.',
 'cheese', 'aged hard sharp',
 'Aged Hunter Valley Cheddar or Milawa Cloth-Bound Cheddar; Australia''s most prestigious wine demands a domestic artisan cheese of comparable character — aged cheddar''s butterscotch and crystalline depth matches Grange''s oak-dark fruit structure.',
 'complement', 'American oak vanilla in Grange bridges the aged Cheddar''s butterscotch depth; iron and leather echo the cheese''s sharp, aged intensity; blackberry provides fruity counterpoint.',
 'cheese', 'established', 1, true),

-- 178: Henschke Hill of Grace (+1)
(178, 'wine_still', 'Eden Valley Shiraz Grand Vin',
 'Blueberry, violets, black pepper, iron-ore, licorice, eucalyptus, floral.',
 'cheese', 'blue_cheese washed',
 'King Island Roaring Forties Blue or Gorgonzola Piccante; the wine''s iron-mineral and violet aromatics create an unexpected but powerful match with bold blue cheese.',
 'contrast', 'Violet and blueberry contrast the pungent blue cheese; iron-ore tannin cleaves through the fat; eucalyptus provides a botanical bridge between wine and cheese character.',
 'cheese', 'adventurous', 2, true),

-- 180: Felton Road Block 3 Pinot Noir
(180, 'wine_still', 'Central Otago Single-Vineyard Pinot Noir',
 'Cherry, rose hip, thyme, iron-ore, fine tannin, earthy depth; Block 3 Bannockburn.',
 'meat', 'duck confit',
 'Duck confit with cherry jus and thyme; the wine''s iron-cherry character and thyme note find a natural partner in classic duck confit — the quintessential Pinot Noir meat pairing in a Central Otago context.',
 'complement', 'Cherry in wine mirrors the cherry jus reduction; thyme in wine echoes the confit herb aromatics; iron-ore tannin cuts through the duck fat richness.',
 'main', 'classic', 1, true),

-- 181: Catena Zapata Adrianna (+1)
(181, 'wine_still', 'Adrianna Vineyard High-Altitude Malbec',
 'Violets, blueberry, graphite, black pepper, mineral, licorice, fine tannin.',
 'cheese', 'aged hard Argentine',
 'Reggianito (Argentine Parmesan-style) aged 24 months or Cuartirolo Argentino; the wine''s violet-graphite depth demands a cheese of equivalent complexity — aged Argentine cheeses that reflect the terroir tradition.',
 'complement', 'Graphite fine tannin integrates with the crystalline texture of aged Reggianito; violet note bridges the cheese''s floral milk character; black pepper echoes aged cheese''s spice.',
 'cheese', 'established', 1, true),

-- 182: Sadie Family Columella (+1)
(182, 'wine_still', 'Swartland Syrah-Mourvèdre Old Vine',
 'Iron-ore, dark olive, violets, black pepper, smoked meat, Provençal herbs, plum.',
 'cheese', 'aged hard cave',
 'Huguenot Cheese (South African cave-aged semi-hard) or aged Gruyère; the wine''s iron-ore and Provençal herb character demands a cheese of structural complexity that mirrors the Swartland''s mineral personality.',
 'complement', 'Iron-ore tannin integrates with aged cheese''s mineral crystalline texture; Provençal herbs bridge the cave-aged complexity; dark olive note mirrors the cheese''s earthy depth.',
 'cheese', 'established', 1, true),

-- 183: Macallan 12 Year Sherry Oak (+1)
(183, 'spirits_whiskey', 'Speyside Single Malt Sherry Cask',
 'Dried fruit, orange peel, Christmas cake, nutmeg, dark chocolate, butterscotch, ginger spice.',
 'cheese', 'blue_cheese creamy',
 'Stilton or Roquefort with dried figs; the whisky''s dried fruit and Christmas spice character creates a classic British pairing with blue cheese and fruit accompaniment — a natural digestif combination.',
 'complement', 'Dried fruit in whisky mirrors the Stilton accompaniment; butterscotch bridges the blue cheese''s creamy depth; orange peel provides acidic contrast to the salt and fat.',
 'digestif', 'established', 1, true),

-- 184: Ardbeg 10 Year (+1)
(184, 'spirits_whiskey', 'Islay Single Malt Heavily Peated',
 'Intense peat smoke, tar, seaweed, iodine, citrus, vanilla, medicinal; 46% ABV.',
 'cheese', 'smoked aged',
 'Smoked Dunlop or Inverloch smoked Cheddar from Scotland; the whisky''s peat and smoke profile finds a natural mirror in Scottish smoked cheese — smoke bridges smoke in the most direct pairing logic.',
 'bridge', 'Peat smoke in Ardbeg bridges directly to the smoked cheese character; iodine-seaweed note mirrors the brine in aged Scottish cheese; citrus provides acidity to refresh the palate.',
 'digestif', 'established', 1, true),

-- 185: Springbank 10 Year (+1)
(185, 'spirits_whiskey', 'Campbeltown Single Malt',
 'Sea salt, brine, orchard fruit, slight peat, vanilla, old cellar, mineral.',
 'cheese', 'aged hard Scottish',
 'Mature Dunlop Cheddar (Ayrshire) or Crowdie with oatcakes; Springbank''s coastal Campbeltown character finds its most natural pairing in the robust, slightly salty aged cheese of nearby Ayrshire — Scotland''s greatest coastal terroir combination.',
 'complement', 'Sea salt and brine in whisky echo the mineral character of mature Dunlop Cheddar; orchard fruit bridges the cheese''s lactate sweetness; slight peat adds depth to the combination.',
 'digestif', 'classic', 1, true),

-- 186: Cantillon Gueuze (+1)
(186, 'beer_wild', 'Brussels Traditional Spontaneous Lambic',
 'Sour lactic acid, horse blanket, citrus, green apple, brett funk, dry, effervescent.',
 'cheese', 'fresh soft bloomy',
 'Brie de Meaux or Camembert Normandie; the gueuze''s lactic acidity and brett funk creates an extraordinary match with bloomy rind cheese — the shared lactic fermentation creates mutual harmony.',
 'complement', 'Lactic acid in gueuze mirrors the lactic culture in Brie; brett funk bridges the cheese''s ammonia-mushroom rind; citrus acidity cuts through the cheese''s creamy richness.',
 'cheese', 'adventurous', 1, true),

-- 187: Weihenstephan Hefeweissbier (+1)
(187, 'beer_ale', 'Bavarian Hefeweizen',
 'Banana, clove, bubblegum, wheat, citrus, refreshing; world''s oldest brewery.',
 'fruit', 'citrus tropical',
 'Fresh orange segments or mango with a light salad; the Hefeweizen''s citrus and banana character creates refreshing harmony with fresh tropical fruit — a simple, classic summer pairing.',
 'complement', 'Banana ester in Hefeweizen mirrors the tropical fruit sweetness; citrus hop note bridges orange segments; effervescence refreshes between bites of fresh fruit.',
 'casual', 'established', 2, true),

-- 188: Leitz Eins Zwei Zero (+1)
(188, 'na_dealcoholised', 'Dealcoholised Riesling NA',
 'Citrus, slate mineral, lime, fresh apple, white peach; 0.0% alcohol.',
 'seafood', 'oysters briny',
 'Pacific oysters on the half shell with mignonette; the wine''s slate mineral and citrus precision mirrors the classic Muscadet-oyster pairing logic in a zero-alcohol context.',
 'complement', 'Slate mineral echoes the oyster''s oceanic terroir; lime acidity mirrors mignonette''s shallot-vinegar character; clean finish allows the oyster''s brine to linger.',
 'starter', 'established', 1, true),

-- 189: Seedlip Spice 94 (+1)
(189, 'na_crafted', 'Distilled NA Spirit — Spice',
 'Allspice, cardamom, oak bark, citrus peel, warm spice, dry bitter.',
 'meat', 'lamb spiced',
 'Moroccan spiced lamb tagine with preserved lemon and chickpeas; the spirit''s allspice and cardamom warmth mirrors the North African spice blend while the dry bitter finish balances the tagine''s richness.',
 'complement', 'Allspice in spirit bridges the Ras el Hanout spice blend of the tagine; cardamom mirrors the warm spice depth; dry bitter finish balances the slow-cooked lamb richness.',
 'main', 'adventurous', 1, true),

-- 190: GT's Synergy Kombucha (+1)
(190, 'na_fermented', 'Live Fermented Kombucha',
 'Ginger, acetic acid, tea, apple, effervescent, refreshing.',
 'fruit', 'tropical fresh',
 'Fresh papaya and lime or mango with chilli; the kombucha''s ginger and acetic brightness creates refreshing harmony with tropical fruit and chilli — the acidity bridges the lime while ginger echoes the spice.',
 'complement', 'Ginger in kombucha mirrors fresh chilli heat on tropical fruit; acetic acid bridges the lime tartness; apple effervescence lifts the tropical fruit sweetness.',
 'casual', 'established', 2, true),

-- 407: Luis Felipe Edwards Gran Reserva Carmenère
(407, 'wine_still', 'Colchagua Valley Carmenère Gran Reserva',
 'Dark plum, green pepper, chocolate, cedar, spice; Chile''s signature variety.',
 'meat', 'pork ribs smoky',
 'Smoked pork ribs with black bean sauce or char siu BBQ pork; Carmenère''s dark plum and green pepper character bridges the smoky char and sweet-savoury BBQ character of Chinese-inspired pork preparations.',
 'complement', 'Dark plum and chocolate in Carmenère mirror the hoisin-soy-plum sauce; green pepper bridges the char of the BBQ; cedar provides structural complexity.',
 'main', 'established', 2, true),

-- 409: Don Melchor Cabernet Sauvignon
(409, 'wine_still', 'Maipo Valley Cabernet Sauvignon Premier Vin',
 'Cassis, graphite, cedar, tobacco, dark cherry, mineral; Puente Alto benchmark.',
 'cheese', 'aged hard cave',
 'Aged Manchego 24-month or Pecorino di Fossa; Don Melchor''s graphite tannin and cedar demand a sheep''s milk cheese of equivalent structure — the crystalline depth of aged Manchego creates a classic Latin American-European crossover pairing.',
 'complement', 'Graphite tannin integrates with Manchego''s crystalline texture; cassis provides fruit contrast against sheep milk savouriness; cedar bridges the cheese''s dried herb rind character.',
 'cheese', 'established', 1, true),

-- 411: Meerlust Rubicon
(411, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, cedar, tobacco, graphite, dark cherry, plum, firm tannin; Cape First Growth.',
 'cheese', 'aged hard hard',
 'Aged Boerenkaas (South African farmhouse Gouda) or Montgomery''s Cheddar; the wine''s firm graphite tannin demands a cheese of equivalent structural complexity — aged South African farmhouse cheese brings the terroir coherence.',
 'complement', 'Graphite tannin integrates with aged Boerenkaas crystalline texture; cassis provides fruit contrast to the savoury cheese; cedar bridges the cheese''s butterscotch depth.',
 'cheese', 'established', 2, true),

-- 412: Boekenhoutskloof Syrah
(412, 'wine_still', 'Franschhoek Syrah Single Vineyard',
 'Black pepper, olive, iron, plum, dark fruit, smoke, violets; Cape Syrah benchmark.',
 'meat', 'springbok venison',
 'Springbok loin with berry reduction and Cape fynbos herb; Boekenhoutskloof Syrah and springbok is the definitive Cape wine-game pairing — iron-mineral and olive character mirrors the lean, mineral springbok protein.',
 'complement', 'Iron-mineral in Syrah bridges the springbok''s lean game mineral character; black pepper echoes the fynbos herb seasoning; olive note mirrors the berry reduction''s depth.',
 'main', 'established', 1, true),

-- 414: GlenDronach 18 Year Allardice (+1)
(414, 'spirits_whiskey', 'Speyside-Highland Single Malt Sherry Cask',
 'Dark fruit, Christmas cake, dark chocolate, hazelnut, pipe tobacco, dried orange; 18yo.',
 'cheese', 'blue_cheese aged',
 'Stilton or Gorgonzola Piccante with dark honeycomb; GlenDronach''s sherry-aged richness and dried fruit creates the classic Scotch whisky-Stilton pairing — Christmas cake meets Christmas cheese board.',
 'complement', 'Christmas cake aromatics in whisky mirror Stilton''s complex aged depth; dark chocolate bridges the blue cheese''s umami bitterness; dried orange contrasts the cheese''s salt.',
 'digestif', 'classic', 1, true),

-- 415: Dalmore 18 Year (+1)
(415, 'spirits_whiskey', 'Northern Highlands Single Malt Complex Cask',
 'Orange marmalade, dark chocolate, coffee, hazelnut, cinnamon, dried fruit; multi-cask.',
 'pastry_dessert', 'chocolate orange cake',
 'Chocolate orange torte or Jaffa cake (chocolate sponge and orange jelly); the Dalmore 18''s orange marmalade and dark chocolate profile finds a near-perfect mirror in classic British chocolate-orange confection.',
 'complement', 'Orange marmalade in whisky mirrors the orange jelly filling exactly; dark chocolate echo is reflected in the torte''s couverture; coffee note adds roast depth to the chocolate experience.',
 'dessert', 'classic', 1, true),

-- 417: Ponsot Clos de la Roche Vieilles Vignes Grand Cru
(417, 'wine_still', 'Morey-Saint-Denis Grand Cru Pinot Noir',
 'Cherry, iron-ore, spice, forest floor, mineral depth, fine tannin; vieilles vignes.',
 'meat', 'pigeon roasted',
 'Roasted squab pigeon with mushroom jus and cepe; the wine''s iron-cherry and forest floor character resonates with the mineral depth of roasted pigeon — the most classic Côte de Nuits pairing.',
 'complement', 'Iron-ore in wine mirrors the iron-mineral character of pigeon breast; cherry bridges the jus reduction; forest floor echoes the cepe mushroom garnish.',
 'main', 'classic', 1, true),

-- 418: Clos de Tart Grand Cru
(418, 'wine_still', 'Morey-Saint-Denis Grand Cru Monopole Pinot Noir',
 'Cherry, rose, iron, mineral depth, silky tannin, earthy spice; monopole Grand Cru.',
 'cheese', 'washed rind',
 'Époisses de Bourgogne (washed rind); the wine''s cherry-mineral character and the cheese''s pungent washed-rind depth create the most Burgundian of all cheese pairings — terroir coherence defines the match.',
 'bridge', 'Cherry fruit bridges the pungent salt of washed rind; mineral depth in wine mirrors the cheese''s earthy terroir character; silky tannin is not overwhelmed by the strong cheese.',
 'cheese', 'classic', 1, true),

-- 419: Leroy Clos de Vougeot Grand Cru
(419, 'wine_still', 'Vougeot Grand Cru Pinot Noir',
 'Rose, cherry, violet, iron, complex mineral, spice; Leroy biodynamic Grand Cru.',
 'meat', 'hare royale',
 'Lièvre à la royale (royal hare stuffed with foie gras and truffles); Leroy''s grand Cru complexity demands the most lavish Burgundian preparation — the hare royale is the region''s ultimate game dish.',
 'complement', 'Iron-ore in wine mirrors the mineral depth of game; rose and violet bridge the truffle garnish''s earthy floral aromatics; complex mineral matches the foie gras richness.',
 'main', 'adventurous', 1, true),

-- 420: Henri Gouges NSG Les Saint-Georges
(420, 'wine_still', 'Nuits-Saint-Georges Premier Cru Pinot Noir',
 'Dark cherry, iron-ore, earthy, structured tannin, spice; the most masculine NSG style.',
 'meat', 'boeuf bourguignon',
 'Boeuf Bourguignon braised with Nuits-Saint-Georges and lardons; the wine''s dark cherry and iron structure creates the definitive slow-cooked Burgundy beef pairing — wine and food from the same appellation.',
 'complement', 'Dark cherry mirrors the reduction sauce; iron-ore tannin integrates with the braised beef richness; the lardons'' smoke bridges the wine''s earthy depth.',
 'main', 'classic', 1, true),

-- 421: Louis Jadot Beaune Clos des Ursules
(421, 'wine_still', 'Beaune Premier Cru Monopole Pinot Noir',
 'Red cherry, strawberry, floral, silky tannin, mineral, elegant Beaune character.',
 'meat', 'quail roasted',
 'Roasted quail with cherry relish and watercress; the wine''s delicate red cherry and floral character demands a light game bird — quail''s elegant mineral flesh mirrors Beaune''s graceful style.',
 'complement', 'Red cherry mirrors the cherry relish; floral note resonates with the watercress freshness; silky tannin integrates with the delicate quail flesh without overpowering.',
 'main', 'classic', 1, true),

-- 422: Comte Armand Pommard Clos des Epeneaux
(422, 'wine_still', 'Pommard Premier Cru Monopole Pinot Noir',
 'Dark cherry, iron, earth, structured firm tannin; the most powerful Pommard style.',
 'meat', 'beef entrecote',
 'Entrecôte bordelaise with bone marrow and shallot reduction; Pommard''s firm iron tannin demands the richest cut — the marrow richness and shallot reduction creates the classic Burgundy-beef entente.',
 'complement', 'Iron tannin integrates with the bone marrow richness; dark cherry bridges the shallot reduction; earthy depth mirrors the meat''s umami character.',
 'main', 'classic', 1, true),

-- 423: d'Angerville Volnay Clos des Ducs
(423, 'wine_still', 'Volnay Premier Cru Monopole Pinot Noir',
 'Rose, red cherry, silky, violet, perfumed, elegant tannin; the most feminine Côte de Beaune.',
 'meat', 'rabbit saddle',
 'Saddle of rabbit with mustard and tarragon; Volnay''s perfumed, silky elegance demands an equally delicate preparation — rabbit''s mild sweetness and tarragon herb create the perfect light game pairing.',
 'complement', 'Rose and violet in wine bridge the tarragon''s anise-floral character; red cherry mirrors the mustard''s sweet acidity; silky tannin integrates with the delicate rabbit flesh.',
 'main', 'established', 1, true),

-- 424: Marc Colin Chassagne-Montrachet Les Caillerets
(424, 'wine_still', 'Chassagne-Montrachet Premier Cru Chardonnay',
 'White stone fruit, hazelnut, cream, mineral, fine acidity; Les Caillerets terroir.',
 'fish_course', 'sole meuniere',
 'Sole meunière with brown butter and lemon; the wine''s hazelnut-cream and mineral character mirrors the brown butter exactly — Chassagne white Burgundy and sole meunière is a legendary Burgundian partnership.',
 'complement', 'Hazelnut in wine mirrors the brown butter exactly; mineral acidity bridges the lemon; stone fruit sweetness complements the delicate sole flesh.',
 'fish_course', 'classic', 1, true),

-- 425: Pierre Gonon Saint-Joseph Rouge
(425, 'wine_still', 'Saint-Joseph Rouge Syrah',
 'Dark cherry, black pepper, olive, violet, iron, Northern Rhône mineral.',
 'meat', 'lamb provencal',
 'Provençal lamb with olives, herbs and tomatoes; the wine''s olive note and Provençal herb character mirrors the braised lamb preparation in its most natural Northern Rhône context.',
 'complement', 'Olive note in wine mirrors the olive braising ingredient directly; black pepper bridges the herb de Provence; iron-mineral resonates with the lamb''s bone character.',
 'main', 'classic', 1, true),

-- 426: Domaine Gonon Saint-Joseph Blanc
(426, 'wine_still', 'Saint-Joseph Blanc Marsanne',
 'White flowers, almond, peach, mineral, rich texture; Marsanne from Northern Rhône granite.',
 'fish_course', 'freshwater trout',
 'River trout en papillote with almonds and herbs; the wine''s almond and floral character creates an exceptional match with freshwater trout — matching the Ardeche rivers of the Saint-Joseph appellation.',
 'complement', 'Almond note in wine mirrors the toasted almond garnish directly; white flower character bridges the fresh herb; mineral granite terroir mirrors the trout''s clean freshwater character.',
 'fish_course', 'established', 1, true),

-- 427: Santa Duc Gigondas Aux Grandes Vignes
(427, 'wine_still', 'Gigondas Grenache-Syrah Southern Rhône',
 'Dark fruit, garrigue, herbs, black pepper, warm spice, firm tannin; Dentelles de Montmirail.',
 'meat', 'daube provencal',
 'Daube de bœuf Provençal (beef stewed with red wine, olives and herbes de Provence); Gigondas''s garrigue herb and dark fruit intensity creates the ultimate Southern Rhône braised beef pairing.',
 'complement', 'Garrigue herbs in wine mirror the herbes de Provence in the daube; dark fruit integrates with the wine-braised reduction; black pepper echoes the spice profile.',
 'main', 'classic', 2, true),

-- 428: Le Sang des Cailloux Vacqueyras
(428, 'wine_still', 'Vacqueyras Grenache-Syrah-Mourvèdre',
 'Plum, garrigue, thyme, pepper, mineral, rustic depth; Vacqueyras terroir.',
 'meat', 'wild boar',
 'Wild boar stew with juniper and mushrooms; the wine''s rustic depth and garrigue character finds a natural partner in the robust wildness of slow-cooked sanglier — the most authentic Provençal game pairing.',
 'complement', 'Garrigue and thyme in wine bridge the juniper seasoning; plum fruit mirrors the braising liquid reduction; mineral depth resonates with the wild game character.',
 'main', 'adventurous', 2, true),

-- 429: Château d'Aquéria Tavel Rosé
(429, 'wine_still', 'Tavel Appellation Controlled Grenache Rosé',
 'Wild strawberry, orange peel, herbes de Provence, structured, dry rosé appellation.',
 'meat', 'charcuterie provencal',
 'Provençal charcuterie — saucisson d''Arles, pâté en croûte, tapenade — the wine''s structured dry rosé character is the definitive aperitif companion to the Southern French cold cut tradition.',
 'complement', 'Wild strawberry echoes the cured meat''s sweet-salt character; herbes de Provence bridge the pâté''s herb crust; structure and acidity cleanse the fat.',
 'aperitif', 'classic', 2, true),

-- 430: Charles Joguet Chinon Clos de la Dioterie
(430, 'wine_still', 'Chinon Cabernet Franc Vieilles Vignes',
 'Red currant, pencil shavings, violet, herbs, fine Loire tannin; old vine Cabernet Franc.',
 'meat', 'rillettes de Tours',
 'Rillettes de Tours (Loire pork rillettes) with crusty baguette; the wine''s pencil shavings and herb character is the definitive Touraine aperitif pairing — pork fat tempered by Cabernet Franc''s bright acidity.',
 'bridge', 'Pencil shavings tannin cleaves through the pork fat richness; violet and red currant provide aromatic contrast; herbal character bridges the pork''s herb curing.',
 'aperitif', 'classic', 1, true),

-- 431: Pierre Breton Bourgueil Franc de Pied
(431, 'wine_still', 'Bourgueil Ungrafted Cabernet Franc Biodynamic',
 'Wild strawberry, iron, herbs, mineral, pure fruit; ungrafted pre-phylloxera character.',
 'meat', 'rabbit terrine',
 'Rabbit and herb terrine with cornichons; Bourgueil''s wild strawberry and mineral character creates an elegant pairing with rabbit terrine — Loire valley terroir and charcuterie tradition.',
 'complement', 'Wild strawberry echoes the terrine''s cured meat sweetness; iron mineral integrates with the rabbit''s lean flavour; herb character bridges the terrine''s herb crust.',
 'starter', 'established', 2, true),

-- 432: Chartogne-Taillet Cuvée Sainte-Anne Champagne
(432, 'wine_sparkling', 'Vallée de la Marne Grower Champagne',
 'Green apple, brioche, chalk mineral, lemon curd, fine bead; grower parcels Merfy.',
 'main', 'roast chicken',
 'Poulet rôti au Champagne with cream sauce; the champagne''s chalk mineral and brioche character integrates beautifully with the cream-wine roasting sauce in the most classic French marriage of food and wine.',
 'complement', 'Brioche autolytic note mirrors the roasting butter; chalk mineral integrates with the cream sauce acidity; fine bead provides textural contrast to the rich chicken.',
 'main', 'classic', 1, true),

-- 433: DRC Bourgogne Rouge
(433, 'wine_still', 'Domaine de la Romanée-Conti Bourgogne Rouge',
 'Cherry, forest floor, mineral, silky, subtle DRC character in appellation Bourgogne.',
 'meat', 'jambon persille',
 'Jambon persillé de Bourgogne (parsleyed ham terrine); the DRC entry-level wine''s subtle cherry and mineral character pairs with this traditional Burgundian charcuterie — the most accessible DRC expression in its natural home context.',
 'complement', 'Cherry fruit bridges the cured ham''s sweetness; mineral depth mirrors the parsley''s freshness; forest floor echoes the terrine''s earthy depth.',
 'starter', 'established', 1, true),

-- 434: Château Moulin Haut-Laroque Fronsac
(434, 'wine_still', 'Fronsac Merlot-Cabernet Franc Right Bank',
 'Plum, iron, earthy, herbs, rustic Right Bank character; Fronsac limestone-clay.',
 'meat', 'magret duck',
 'Magret de canard (duck breast) with Périgueux sauce and black truffles; the wine''s plum and iron character creates a natural Dordogne food corridor pairing with rich duck breast and truffle.',
 'complement', 'Plum mirrors the magret''s rich duck fat; iron tannin integrates with the meat''s mineral depth; earthy note bridges the Périgueux truffle sauce.',
 'main', 'established', 2, true);

COMMIT;
