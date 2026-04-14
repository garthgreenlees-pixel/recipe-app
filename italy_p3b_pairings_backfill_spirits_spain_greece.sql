-- Italy Phase 3b: Pairing backfill — Italian spirits, Spain, Greece, Lebanon, MENA
-- IDs 346-370: Grappa, Amaro, Limoncello, Spanish reds/sherry, Greek wines/ouzo, Lebanese/MENA
-- Target 4 pairings each for 1-pairing products; 3 for 2-pairing products

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 346: Nonino UE Grappa Monovitigno Moscato
-- Grappa from Moscato pomace; floral, fragrant, sweet, 41% abv
-- ============================================================
(346, 'spirits_liqueur', 'Grappa Monovitigno', 'Nonino UE Moscato Grappa — from single-variety Moscato grape pomace; preserves the variety''s extraordinary floral perfume in grappa form; 41% abv',
 'dessert_pastry', 'sweet_fruity', 'Moscato d''Asti panna cotta with peach compote — pairing the grape''s spirit with the grape''s wine''s traditional dessert companion',
 'complement', 'Nonino Moscato grappa retains the Moscato grape''s floral-peach aromatics in distilled form; serving it with a panna cotta that mirrors the wine''s dessert pairings creates full circle resonance', 'digestif', 'established', 2, true),

(346, 'spirits_liqueur', 'Grappa Monovitigno', 'Nonino UE Moscato Grappa — from single-variety Moscato grape pomace; preserves the variety''s extraordinary floral perfume in grappa form; 41% abv',
 'dessert_pastry', 'floral_perfumed', 'Shortbread with rose water and cardamom glaze — the floral notes in the grappa mirror the rose water''s perfume',
 'complement', 'Moscato Grappa''s preserved floral character (rose petal, orange blossom) resonates with rose water desserts; cardamom adds a warm spice bridge', 'digestif', 'suggested', 2, true),

(346, 'spirits_liqueur', 'Grappa Monovitigno', 'Nonino UE Moscato Grappa — from single-variety Moscato grape pomace; preserves the variety''s extraordinary floral perfume in grappa form; 41% abv',
 'dessert_pastry', 'sweet_spiced', 'Tiramisù — the canonical Italian digestif-dessert pairing; grappa is traditionally offered alongside or poured over tiramisù',
 'complement', 'Grappa and tiramisù is the Italian restaurant tradition: the coffee-mascarpone-chocolate combination needs the spirit''s intensity and warmth; a post-dessert ritual pairing', 'digestif', 'classic', 2, true),

(346, 'spirits_liqueur', 'Grappa Monovitigno', 'Nonino UE Moscato Grappa — from single-variety Moscato grape pomace; preserves the variety''s extraordinary floral perfume in grappa form; 41% abv',
 'charcuterie_cheese', 'fermented_aged', 'Aged Asiago or Grana Padano with walnut honey — grappa is the traditional accompaniment to the Italian cheese course finale',
 'complement', 'Friulian grappa (Nonino is from Friuli) and aged northern Italian cheeses is a regional tradition; honey bridges the grappa''s sweetness with the cheese''s crystalline richness', 'digestif', 'classic', 2, true),

-- ============================================================
-- 347: Fernet-Branca (already has 2 pairings; add 3 more)
-- Bitter Italian amaro; 27 herbs/spices; menthol, licorice, saffron; 39% abv
-- ============================================================
(347, 'spirits_liqueur', 'Amaro Fernet', 'Fernet-Branca — the bartenders'' handshake; 27 herbs and spices including myrrh, rhubarb, chamomile, cardamom, aloe; intense bitter-menthol-licorice; 39% abv',
 'dessert_pastry', 'sweet_spiced', 'Dark chocolate with mint — the menthol-chocolate combination mirrors Fernet''s minty-bitter character',
 'complement', 'Fernet''s menthol and bitter chocolate notes are a natural mirror for dark chocolate with mint; a sophisticated digestif dessert combination', 'digestif', 'established', 2, true),

(347, 'spirits_liqueur', 'Amaro Fernet', 'Fernet-Branca — the bartenders'' handshake; 27 herbs and spices including myrrh, rhubarb, chamomile, cardamom, aloe; intense bitter-menthol-licorice; 39% abv',
 'dessert_pastry', 'bitter_astringent', 'Espresso and Fernet — the classic bartender''s digestif: Fernet with a shot of espresso or mixed into the espresso',
 'bridge', 'Fernet''s bitter herbs and espresso''s bitter roast create an additive bitterness that is paradoxically refreshing after a heavy meal; a bar industry ritual worldwide', 'digestif', 'classic', 2, true),

(347, 'spirits_liqueur', 'Amaro Fernet', 'Fernet-Branca — the bartenders'' handshake; 27 herbs and spices including myrrh, rhubarb, chamomile, cardamom, aloe; intense bitter-menthol-licorice; 39% abv',
 'vegetables_legumes', 'umami_savoury', 'Argentinian asado with chimichurri — Fernet con Coca is Argentina''s national drink; serving at the asado is the local tradition',
 'complement', 'In Argentina, Fernet-Branca + Coca-Cola is consumed at asados (barbecues) as freely as beer; the herbal bitterness cuts through the meat fat and char', 'casual', 'classic', 2, true),

-- ============================================================
-- 348: Amaro Montenegro
-- Sweeter amaro; orange, dried flowers, vanilla, cinnamon; 23% abv
-- ============================================================
(348, 'spirits_liqueur', 'Amaro', 'Amaro Montenegro — Bologna''s beloved amaro; sweeter and more accessible than Fernet; orange peel, dried flowers, vanilla, cinnamon, anise; 23% abv; Dante''s ''liqueur of the virtues''',
 'dessert_pastry', 'sweet_spiced', 'Orange polenta cake with candied orange peel and vanilla cream — the orange-vanilla notes in Montenegro mirror the dessert''s primary flavours',
 'complement', 'Amaro Montenegro''s dominant orange peel and vanilla character resonates seamlessly with orange-vanilla desserts; the 23% abv makes it less overwhelming than higher-proof amaros', 'digestif', 'established', 2, true),

(348, 'spirits_liqueur', 'Amaro', 'Amaro Montenegro — Bologna''s beloved amaro; sweeter and more accessible than Fernet; orange peel, dried flowers, vanilla, cinnamon, anise; 23% abv; Dante''s ''liqueur of the virtues''',
 'charcuterie_cheese', 'sweet_salty', 'Prosciutto e melone aperitivo — Montenegro is increasingly served as an aperitivo on ice rather than solely as a digestif',
 'complement', 'Montenegro''s sweetness and orange character on ice (Amaro Montenegro Spritz format) is a perfect Italian aperitivo; its gentle bitterness contrasts the prosciutto-melon sweetness', 'aperitif', 'suggested', 2, true),

(348, 'spirits_liqueur', 'Amaro', 'Amaro Montenegro — Bologna''s beloved amaro; sweeter and more accessible than Fernet; orange peel, dried flowers, vanilla, cinnamon, anise; 23% abv; Dante''s ''liqueur of the virtues''',
 'dessert_pastry', 'sweet_fruity', 'Affogato (espresso over vanilla gelato) with a Montenegro pour — a three-layer coffee-vanilla-amaro experience',
 'complement', 'Montenegro''s vanilla and orange notes are a natural companion for affogato; pouring it over the espresso-gelato combination adds herbal complexity to the classic dessert', 'digestif', 'classic', 2, true),

(348, 'spirits_liqueur', 'Amaro', 'Amaro Montenegro — Bologna''s beloved amaro; sweeter and more accessible than Fernet; orange peel, dried flowers, vanilla, cinnamon, anise; 23% abv; Dante''s ''liqueur of the virtues''',
 'dessert_pastry', 'sweet_spiced', 'Cantucci and vin santo — in the absence of vin santo, Montenegro serves as an Italian dipping spirit for the almond biscotti',
 'complement', 'Montenegro''s approachable sweetness and anise note make it a viable vin santo substitute for cantucci dipping; its vanilla bridges with the almond biscotti character', 'digestif', 'suggested', 2, true),

-- ============================================================
-- 349: Limoncello di Capri
-- Lemon peel liqueur; intense citrus, sweet, 30% abv; Southern Italy
-- ============================================================
(349, 'spirits_liqueur', 'Limoncello', 'Limoncello di Capri — the authentic Campanian lemon liqueur from Capri; intense sfusato amalfitano or Sorrento lemon peel; electric citrus, sweet, 30% abv; served ice-cold',
 'dessert_pastry', 'sweet_fruity', 'Lemon tart (tarte au citron) with candied lemon and meringue — the lemon in both dessert and liqueur creates an intensifying citrus mirror',
 'complement', 'Limoncello and lemon tart is the definitive citrus-amplification pairing: both share the same Sorrento or Amalfi lemon character; the liqueur''s sweetness bridges the tart''s sharpness', 'digestif', 'classic', 2, true),

(349, 'spirits_liqueur', 'Limoncello', 'Limoncello di Capri — the authentic Campanian lemon liqueur from Capri; intense sfusato amalfitano or Sorrento lemon peel; electric citrus, sweet, 30% abv; served ice-cold',
 'seafood', 'delicate_fresh', 'Seafood crudo with yuzu dressing — limoncello''s citrus intensity bridges across cultural contexts with delicate raw seafood',
 'cleanse', 'A small pour of ice-cold Limoncello between seafood courses acts as a palate cleanser; its citrus acidity and cold temperature refresh without introducing competing flavours', 'pre_dessert', 'suggested', 2, true),

(349, 'spirits_liqueur', 'Limoncello', 'Limoncello di Capri — the authentic Campanian lemon liqueur from Capri; intense sfusato amalfitano or Sorrento lemon peel; electric citrus, sweet, 30% abv; served ice-cold',
 'dessert_pastry', 'sweet_fruity', 'Panna cotta al limone with limoncello granita — serving the liqueur as both an ingredient and an accompaniment',
 'complement', 'Panna cotta al limone and limoncello granita creates a multilayered citrus experience; the granita''s ice structure prevents the combination from becoming too sweet', 'dessert', 'established', 2, true),

(349, 'spirits_liqueur', 'Limoncello', 'Limoncello di Capri — the authentic Campanian lemon liqueur from Capri; intense sfusato amalfitano or Sorrento lemon peel; electric citrus, sweet, 30% abv; served ice-cold',
 'seafood', 'salty_mineral', 'Oysters with limoncello mignonette — substituting limoncello for vinegar in the classic accompaniment creates a Campanian twist',
 'elevate', 'Limoncello''s citrus-sweet character transforms the classic mignonette; the brine of fresh oysters contrasts the sweet lemon, creating a coastal Campanian pairing', 'amuse', 'adventurous', 2, true),

-- ============================================================
-- 350: Nardini Acquavite di Vinaccia (Grappa)
-- Classic Veneto grappa; more neutral and spirit-forward than Nonino Monovitigno
-- ============================================================
(350, 'spirits_liqueur', 'Grappa', 'Nardini Acquavite di Vinaccia — Bassano del Grappa''s historic distillery (est. 1779); classic Veneto grappa style; clean, direct, with grape and spirit character; 40% abv',
 'dessert_pastry', 'sweet_spiced', 'Sbrisolona (crumbly almond cake from Mantua) with grappa — the Northern Italian tradition of dunking crumbly cake in grappa',
 'complement', 'Sbrisolona and grappa is the Venetian and Lombardian tradition; the almond cake''s crumble is soaked in the spirit, creating a textural and flavour fusion', 'digestif', 'classic', 2, true),

(350, 'spirits_liqueur', 'Grappa', 'Nardini Acquavite di Vinaccia — Bassano del Grappa''s historic distillery (est. 1779); classic Veneto grappa style; clean, direct, with grape and spirit character; 40% abv',
 'dessert_pastry', 'sweet_spiced', 'Tiramisù with grappa — the original tiramisù recipe included grappa before the Venetian dessert was codified',
 'complement', 'Nardini and tiramisù is a regional tradition (Bassano del Grappa is Veneto, as is tiramisù''s home territory); the grappa''s spirit character amplifies the mascarpone and espresso', 'digestif', 'classic', 2, true),

(350, 'spirits_liqueur', 'Grappa', 'Nardini Acquavite di Vinaccia — Bassano del Grappa''s historic distillery (est. 1779); classic Veneto grappa style; clean, direct, with grape and spirit character; 40% abv',
 'charcuterie_cheese', 'fermented_aged', 'Monte Veronese or aged Asiago with walnut honey — Veneto cheese with Veneto grappa, a regional pairing of simple directness',
 'complement', 'Nardini''s clean Veneto style pairs without complexity against Veneto''s aged cow''s milk cheeses; the grappa''s spirit lifts the cheese''s richness without competing', 'digestif', 'established', 2, true),

(350, 'spirits_liqueur', 'Grappa', 'Nardini Acquavite di Vinaccia — Bassano del Grappa''s historic distillery (est. 1779); classic Veneto grappa style; clean, direct, with grape and spirit character; 40% abv',
 'dessert_pastry', 'bitter_astringent', 'Espresso ristretto — the resentin (rinsing the espresso cup with grappa) tradition of northeastern Italy',
 'bridge', 'The resentin tradition: pouring a small grappa into the empty espresso cup after drinking and swirling to collect the residual coffee creates a coffee-grappa fusion unique to the Veneto', 'digestif', 'classic', 2, true),

-- ============================================================
-- 351: Vega Sicilia Unico
-- Spain's most collectible wine; Tempranillo + Cabernet; 10 years in wood
-- ============================================================
(351, 'wine_still', 'Ribera del Duero DO', 'Vega Sicilia Unico — Spain''s most collectible wine; 10 years minimum in wood and bottle; Tinto Fino (Tempranillo) + Cabernet Sauvignon; extraordinary complexity at maturity; dried cherry, cedar, tobacco, dried flowers',
 'meat_poultry', 'rich_fatty_smoky', 'Lechazo asado (roasted suckling lamb from Castilla y León) — the iconic Castilian preparation; the young lamb''s delicacy and the wine''s maturity create a memorable contrast',
 'complement', 'Lechazo and Vega Sicilia Unico is one of Spain''s sacred food-wine pairings: the suckling lamb''s extraordinary tenderness and the 10-year-aged wine''s complexity are proportioned as equals', 'main', 'classic', 1, true),

(351, 'wine_still', 'Ribera del Duero DO', 'Vega Sicilia Unico — Spain''s most collectible wine; 10 years minimum in wood and bottle; Tinto Fino (Tempranillo) + Cabernet Sauvignon; extraordinary complexity at maturity; dried cherry, cedar, tobacco, dried flowers',
 'charcuterie_cheese', 'fermented_aged', 'Ibérico de bellota (acorn-fed Ibérico ham, 36-month Jamón Ibérico 5J) — Spain''s greatest meat product alongside Spain''s greatest wine',
 'complement', 'Jamón Ibérico de bellota and Vega Sicilia Unico is the apex of Spanish food-wine culture: both require years of development, both express the Castilian landscape''s extremes', 'starter', 'classic', 1, true),

(351, 'wine_still', 'Ribera del Duero DO', 'Vega Sicilia Unico — Spain''s most collectible wine; 10 years minimum in wood and bottle; Tinto Fino (Tempranillo) + Cabernet Sauvignon; extraordinary complexity at maturity; dried cherry, cedar, tobacco, dried flowers',
 'charcuterie_cheese', 'fermented_aged', 'Manchego Curado (6-month, La Mancha) with membrillo (quince paste) — the classic Spanish cheese board pairing that complements Unico''s dried fruit complexity',
 'complement', 'Manchego and membrillo is Spain''s canonical cheese board combination; at Unico''s level of complexity, the quince paste bridges the wine''s dried cherry character while the cheese''s sheep richness softens the tannins', 'cheese', 'classic', 1, true),

(351, 'wine_still', 'Ribera del Duero DO', 'Vega Sicilia Unico — Spain''s most collectible wine; 10 years minimum in wood and bottle; Tinto Fino (Tempranillo) + Cabernet Sauvignon; extraordinary complexity at maturity; dried cherry, cedar, tobacco, dried flowers',
 'meat_poultry', 'earthy_herbal', 'Cordero asado con hierbas (herb-roasted whole lamb shoulder) with romesco and roasted garlic — the Castilian approach to whole-animal celebration cooking',
 'complement', 'Vega Sicilia Unico demands celebration food of equivalent stature; whole roasted lamb shoulder''s herb-garlic complexity is proportioned for the wine''s extraordinary depth', 'main', 'established', 1, true),

-- ============================================================
-- 352: Dominio de Pingus Pingus (2 → 5 target; add 3)
-- Ultra-concentrated Ribera del Duero; Peter Sisseck''s masterpiece
-- ============================================================
(352, 'wine_still', 'Ribera del Duero DO', 'Dominio de Pingus — Peter Sisseck''s legendary micro-cuvée; ultra-concentrated Tinto Fino from centenarian vines; blackberry, cedar, violet, tobacco; extraordinary power and elegance',
 'meat_poultry', 'rich_fatty_smoky', 'Secreto ibérico a la brasa (grilled Ibérico pork secret cut) with Padron peppers — the hidden cut of Ibérico pork charred over vine wood',
 'complement', 'Pingus''s vine wood character (from old Tinto Fino) resonates with vine-charcoal grilled Ibérico; the pork''s exceptional fat quality bridges the wine''s concentration', 'main', 'established', 1, true),

(352, 'wine_still', 'Ribera del Duero DO', 'Dominio de Pingus — Peter Sisseck''s legendary micro-cuvée; ultra-concentrated Tinto Fino from centenarian vines; blackberry, cedar, violet, tobacco; extraordinary power and elegance',
 'charcuterie_cheese', 'fermented_aged', 'Aged Manchego (12-month DOP) with truffle honey and Marcona almonds — the premium Spanish cheese pairing at Pingus''s level demands extra aging and quality',
 'complement', 'Aged Manchego''s concentrated sheep-character and truffle honey bridge Pingus''s cedar-violet complexity; Marcona almonds add a textural element that structures the pairing', 'cheese', 'established', 1, true),

(352, 'wine_still', 'Ribera del Duero DO', 'Dominio de Pingus — Peter Sisseck''s legendary micro-cuvée; ultra-concentrated Tinto Fino from centenarian vines; blackberry, cedar, violet, tobacco; extraordinary power and elegance',
 'meat_poultry', 'earthy_herbal', 'Cochinillo asado (roasted suckling pig from Segovia) — the rival to Castilian lamb for Ribera del Duero''s great wines',
 'complement', 'Cochinillo asado''s crispy crackling and impossibly tender meat are calibrated for a wine of Pingus''s power; the fat and the tannins create the classic tension-release pairing structure', 'main', 'classic', 1, true),

-- ============================================================
-- 353: Muga Prado Enea Gran Reserva
-- Traditional Rioja Gran Reserva; Garnacha + Tempranillo; aged 3+ years
-- ============================================================
(353, 'wine_still', 'Rioja DOCa Gran Reserva', 'Muga Prado Enea Gran Reserva — one of Rioja''s most traditional Gran Reservas; Tempranillo-dominant with Garnacha, Graciano, and Mazuelo; 3 years oak + 3 years bottle; dried cherry, vanilla, leather, tobacco',
 'meat_poultry', 'earthy_herbal', 'Chuletillas de cordero al sarmiento (baby lamb chops grilled over vine shoots) — the classic Rioja preparation: lamb over vine wood',
 'complement', 'Lamb grilled over vine shoots is the defining Rioja preparation; the smoke from grape-vine wood bridges the wine''s grape character while the lamb''s fat balances the tannins', 'main', 'classic', 2, true),

(353, 'wine_still', 'Rioja DOCa Gran Reserva', 'Muga Prado Enea Gran Reserva — one of Rioja''s most traditional Gran Reservas; Tempranillo-dominant with Garnacha, Graciano, and Mazuelo; 3 years oak + 3 years bottle; dried cherry, vanilla, leather, tobacco',
 'charcuterie_cheese', 'fermented_aged', 'Chorizo a la sidra (chorizo cooked in cider) with pan con tomate — the Basque-Rioja charcuterie tradition',
 'complement', 'Chorizo''s paprika-pork-fat richness and Rioja Gran Reserva''s vanilla-leather character create one of Spain''s classic regional food-wine pairings', 'starter', 'classic', 2, true),

(353, 'wine_still', 'Rioja DOCa Gran Reserva', 'Muga Prado Enea Gran Reserva — one of Rioja''s most traditional Gran Reservas; Tempranillo-dominant with Garnacha, Graciano, and Mazuelo; 3 years oak + 3 years bottle; dried cherry, vanilla, leather, tobacco',
 'charcuterie_cheese', 'fermented_aged', 'Manchego Viejo (12-month) with membrillo and walnuts — Muga''s oak-aged vanilla and the aged Manchego''s caramel notes create a harmonious pairing',
 'complement', 'Rioja Gran Reserva''s oak-vanilla and Manchego''s sheep-caramel character are natural companions; the membrillo bridges both wines'' dried cherry and the cheese''s sweetness', 'cheese', 'classic', 2, true),

(353, 'wine_still', 'Rioja DOCa Gran Reserva', 'Muga Prado Enea Gran Reserva — one of Rioja''s most traditional Gran Reservas; Tempranillo-dominant with Garnacha, Graciano, and Mazuelo; 3 years oak + 3 years bottle; dried cherry, vanilla, leather, tobacco',
 'meat_poultry', 'rich_fatty_smoky', 'Rabo de toro (oxtail stew) — the slow-braised oxtail in wine sauce from Andalusia and Rioja country is a classic Spanish comfort food',
 'complement', 'Oxtail''s collagen-rich braised depth and Rioja Gran Reserva''s leather-dried cherry structure create a classic Spanish winter pairing; the braise''s wine reduction mirrors the drinking wine', 'main', 'established', 2, true),

-- ============================================================
-- 354: López de Heredia Viña Tondonia Gran Reserva
-- Spain's most traditional Rioja; 10+ years in oak; oxidative, amber
-- ============================================================
(354, 'wine_still', 'Rioja DOCa Gran Reserva', 'López de Heredia Viña Tondonia Gran Reserva — the ultimate traditional Rioja; 10+ years in American oak; amber-brick colour; hazelnut, dried cherry, leather, vanilla, oxidative complexity; extraordinary longevity',
 'meat_poultry', 'earthy_herbal', 'Cochinillo asado (roasted suckling pig) from Segovia — the Castilian suckling pig whose crackling and delicate meat are a Rioja tradition',
 'complement', 'Tondonia Gran Reserva''s amber-oxidative complexity demands a dish of equivalent age: the cochinillo''s roasting suckling pig provides fat to soften the tannins while the herbs echo the wine''s vanilla notes', 'main', 'classic', 1, true),

(354, 'wine_still', 'Rioja DOCa Gran Reserva', 'López de Heredia Viña Tondonia Gran Reserva — the ultimate traditional Rioja; 10+ years in American oak; amber-brick colour; hazelnut, dried cherry, leather, vanilla, oxidative complexity; extraordinary longevity',
 'charcuterie_cheese', 'fermented_aged', 'Idiazabal (Basque smoked sheep''s milk cheese, 3-month) — the Basque cheese''s smoke and fat note echoes the wine''s oxidative American oak character',
 'complement', 'Idiazabal''s smoky-sheep character resonates with Tondonia''s oxidative-vanilla-hazelnut complexity; a Basque-Rioja border pairing of deep regional significance', 'cheese', 'classic', 1, true),

(354, 'wine_still', 'Rioja DOCa Gran Reserva', 'López de Heredia Viña Tondonia Gran Reserva — the ultimate traditional Rioja; 10+ years in American oak; amber-brick colour; hazelnut, dried cherry, leather, vanilla, oxidative complexity; extraordinary longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Perdiz a la Riojana (Rioja-style partridge) with chorizo and piquillo peppers — the most Rioja-specific game preparation for the most Rioja wine',
 'complement', 'Perdiz a la Riojana''s paprika-chorizo-pepper richness is designed for traditional Rioja''s oxidative complexity; both are of the same territory and tradition', 'main', 'classic', 1, true),

(354, 'wine_still', 'Rioja DOCa Gran Reserva', 'López de Heredia Viña Tondonia Gran Reserva — the ultimate traditional Rioja; 10+ years in American oak; amber-brick colour; hazelnut, dried cherry, leather, vanilla, oxidative complexity; extraordinary longevity',
 'charcuterie_cheese', 'umami_savoury', 'Jamón Ibérico cebo (lower tier than de bellota but excellent quality) with pickled anchovies and piquillo peppers — traditional Basque pintxos',
 'complement', 'Tondonia''s hazelnut-leather maturity pairs with the complexity of traditional Basque pintxos; Jamón''s sweet-saline fat and anchovy''s umami find the wine''s structure an ideal partner', 'starter', 'classic', 1, true),

-- ============================================================
-- 355: Alvaro Palacios L'Ermita
-- Priorat's most prestigious wine; old Garnacha on llicorella slate
-- ============================================================
(355, 'wine_still', 'Priorat DOCa', 'Alvaro Palacios L''Ermita — Priorat''s most prestigious wine; old Garnacha vines on llicorella (black schist) slate soils; extraordinary mineral depth, black olive, dark cherry, mineral, licorice',
 'meat_poultry', 'rich_fatty_smoky', 'Cordero al chilindrón (lamb in pepper-tomato sauce) with saffron rice — the Aragonese-Catalan lamb preparation that is L''Ermita''s regional food match',
 'complement', 'L''Ermita''s Priorat terroir (Aragonese border) aligns with the lamb-pepper-saffron cooking tradition of the Ebro valley; the wine''s mineral-licorice depth balances the sauce''s richness', 'main', 'established', 1, true),

(355, 'wine_still', 'Priorat DOCa', 'Alvaro Palacios L''Ermita — Priorat''s most prestigious wine; old Garnacha on llicorella (black schist) slate soils; extraordinary mineral depth, black olive, dark cherry, mineral, licorice',
 'meat_poultry', 'earthy_herbal', 'Caza mayor (game: wild boar or venison) with romesco and Catalan mushrooms — the wild game of the Catalan mountains pairs with Priorat''s mineral intensity',
 'complement', 'L''Ermita''s mineral-licorice complexity and old-vine concentration are calibrated for Catalan mountain game; romesco''s nut-pepper-olive complexity bridges the wine''s character', 'main', 'classic', 1, true),

(355, 'wine_still', 'Priorat DOCa', 'Alvaro Palacios L''Ermita — Priorat''s most prestigious wine; old Garnacha on llicorella (black schist) slate soils; extraordinary mineral depth, black olive, dark cherry, mineral, licorice',
 'charcuterie_cheese', 'fermented_aged', 'Garrotxa (Catalan aged goat''s milk cheese, 3-month) with black olive tapenade — the mineral Catalan cheese matching the mineral Priorat wine',
 'complement', 'Garrotxa''s white mould rind and earthy-nuttiness bridge L''Ermita''s mineral character; the black olive tapenade directly mirrors the wine''s black olive note from llicorella soils', 'cheese', 'established', 1, true),

(355, 'wine_still', 'Priorat DOCa', 'Alvaro Palacios L''Ermita — Priorat''s most prestigious wine; old Garnacha on llicorella (black schist) slate soils; extraordinary mineral depth, black olive, dark cherry, mineral, licorice',
 'meat_poultry', 'rich_fatty_smoky', 'Grilled ibérico presa (shoulder primal) with escalivada (roasted vegetables) — the Catalan char-grilled approach to Ibérico pork',
 'complement', 'Ibérico presa''s extraordinary fat quality and the roasted pepper-aubergine escalivada create the Catalan flavour profile that L''Ermita''s Garnacha was cultivated alongside', 'main', 'established', 1, true),

-- ============================================================
-- 356: Hidalgo La Gitana Manzanilla
-- Palomino under flor; saline, chamomile, almonds; extreme bone-dry
-- ============================================================
(356, 'wine_fortified', 'Manzanilla', 'Hidalgo La Gitana Manzanilla — from Sanlúcar de Barrameda; Palomino under thick flor; extreme saline minerality, chamomile, Manzanilla character, almond; bone-dry; the seafood wine par excellence',
 'seafood', 'salty_mineral', 'Grilled gambas al ajillo (garlic prawns) on the Sanlúcar waterfront — the dish served in the same port town as La Gitana is produced',
 'complement', 'La Gitana and gambas al ajillo from Sanlúcar is one of Spain''s most perfect terroir pairings: the wine''s marine salinity mirrors the prawn''s sea character while garlic oil provides a flavour bridge', 'main', 'classic', 2, true),

(356, 'wine_fortified', 'Manzanilla', 'Hidalgo La Gitana Manzanilla — from Sanlúcar de Barrameda; Palomino under thick flor; extreme saline minerality, chamomile, Manzanilla character, almond; bone-dry; the seafood wine par excellence',
 'seafood', 'salty_mineral', 'Ortiguillas (sea anemones) fried in batter — Sanlúcar''s most unusual delicacy; the sea creature and the wine are born in the same Guadalquivir estuary',
 'complement', 'Ortiguillas'' intense marine-iodine character demands a wine of equal sea-minerality; La Gitana''s extreme saline character makes it the only appropriate accompaniment', 'starter', 'classic', 2, true),

(356, 'wine_fortified', 'Manzanilla', 'Hidalgo La Gitana Manzanilla — from Sanlúcar de Barrameda; Palomino under thick flor; extreme saline minerality, chamomile, Manzanilla character, almond; bone-dry; the seafood wine par excellence',
 'seafood', 'delicate_fresh', 'Boquerones en vinagre (white anchovies marinated in vinegar) with Arbequina olive oil and garlic — the classic Spanish tapas for Manzanilla',
 'complement', 'Manzanilla and boquerones is Spain''s most classic tapas-wine pairing: the wine''s salinity and the anchovy''s brine are in perfect resonance; acidity in both creates refreshing tension', 'aperitif', 'classic', 2, true),

(356, 'wine_fortified', 'Manzanilla', 'Hidalgo La Gitana Manzanilla — from Sanlúcar de Barrameda; Palomino under thick flor; extreme saline minerality, chamomile, Manzanilla character, almond; bone-dry; the seafood wine par excellence',
 'seafood', 'umami_savoury', 'Chanquetes (whitebait) fried with lemon and salt — the tiny fried fish of Andalusia that demand a wine of extreme acidity and salinity',
 'cleanse', 'Chanquetes'' oil and crispy batter are cut perfectly by La Gitana''s razor-sharp acidity; the wine''s saline character resonates with the fish''s brine', 'aperitif', 'classic', 2, true),

-- ============================================================
-- 357: González Byass Tío Pepe Fino
-- The world's most famous Fino; dry, almond, fresh, flor character
-- ============================================================
(357, 'wine_fortified', 'Fino', 'González Byass Tío Pepe Fino — the world''s most recognised Fino Sherry; Palomino under flor; almonds, fresh bread, green apple, chamomile; bone-dry; defining the style globally',
 'seafood', 'salty_mineral', 'Jamón Ibérico de bellota with Picos de Europa and Marcona almonds — the Spanish tapas master pairing: Fino, Jamón, olives, almonds',
 'complement', 'Tío Pepe and Jamón Ibérico is Spain''s most celebrated aperitivo: the Fino''s almond character mirrors the Marcona almonds; its salinity contrasts the sweet-saline Jamón fat', 'aperitif', 'classic', 2, true),

(357, 'wine_fortified', 'Fino', 'González Byass Tío Pepe Fino — the world''s most recognised Fino Sherry; Palomino under flor; almonds, fresh bread, green apple, chamomile; bone-dry; defining the style globally',
 'seafood', 'salty_mineral', 'Ceviche with avocado, corn, and lime — Fino Sherry''s citrus-almond dryness handles the ceviche''s acidity beautifully',
 'complement', 'Fino''s high acidity and saline minerality are a natural match for ceviche''s lime-marinated fish; the combination works across cultures as both share cleansing acidity', 'starter', 'suggested', 2, true),

(357, 'wine_fortified', 'Fino', 'González Byass Tío Pepe Fino — the world''s most recognised Fino Sherry; Palomino under flor; almonds, fresh bread, green apple, chamomile; bone-dry; defining the style globally',
 'vegetables_legumes', 'salty_mineral', 'Gazpacho andaluz with jamón crumble — the cold tomato soup from the same territory as Jerez finds its natural wine companion',
 'complement', 'Gazpacho and Fino Sherry share the same Andalusian soul: the tomato-cucumber-olive oil coldness resonates with the wine''s crispness; the jamón crumble bridges the saline notes', 'starter', 'classic', 2, true),

(357, 'wine_fortified', 'Fino', 'González Byass Tío Pepe Fino — the world''s most recognised Fino Sherry; Palomino under flor; almonds, fresh bread, green apple, chamomile; bone-dry; defining the style globally',
 'seafood', 'delicate_fresh', 'Almejas a la marinera (clams in white wine, garlic, parsley) — the classic Galician-Andalusian shellfish preparation that Fino was made for',
 'complement', 'Fino''s white wine-adjacent character (despite fortification) and almond-saline character make it ideal for clam preparations; the wine''s freshness prevents the garlic from dominating', 'starter', 'classic', 2, true),

-- ============================================================
-- 358: Lustau Los Arcos Dry Amontillado
-- Oxidative Sherry; hazelnut, dried orange, walnut, coffee notes; 18% abv
-- ============================================================
(358, 'wine_fortified', 'Amontillado', 'Lustau Los Arcos Dry Amontillado — a Fino that lost its flor and oxidised; nutty-hazelnut, dried orange, coffee, and walnut complexity; 18% abv; bone-dry',
 'charcuterie_cheese', 'fermented_aged', 'Manchego viejo (12-month) with walnut cake — the cheese''s nutty sweetness resonates with the Amontillado''s walnut-hazelnut character',
 'complement', 'Amontillado and aged Manchego is the classic Spanish cheese-sherry pairing: the wine''s hazelnut oxidative character mirrors the sheep''s milk cheese''s caramel-walnut notes', 'cheese', 'classic', 2, true),

(358, 'wine_fortified', 'Amontillado', 'Lustau Los Arcos Dry Amontillado — a Fino that lost its flor and oxidised; nutty-hazelnut, dried orange, coffee, and walnut complexity; 18% abv; bone-dry',
 'seafood', 'umami_savoury', 'Consommé de mariscos (shellfish consommé) with sherry — the Andalusian tradition of using Amontillado in cooking and at the table simultaneously',
 'complement', 'Amontillado''s oxidative depth enriches shellfish stock-based preparations; serving it at the table alongside the finished consommé creates seamless integration', 'starter', 'classic', 2, true),

(358, 'wine_fortified', 'Amontillado', 'Lustau Los Arcos Dry Amontillado — a Fino that lost its flor and oxidised; nutty-hazelnut, dried orange, coffee, and walnut complexity; 18% abv; bone-dry',
 'meat_poultry', 'earthy_herbal', 'Pollo en pepitoria (chicken in almond-saffron-sherry sauce) — the most traditional Castilian dish using Amontillado in its preparation',
 'complement', 'Pollo en pepitoria is cooked with Amontillado and almonds; serving the same wine at the table creates full circle continuity; the saffron bridges the wine''s amber complexity', 'main', 'classic', 2, true),

(358, 'wine_fortified', 'Amontillado', 'Lustau Los Arcos Dry Amontillado — a Fino that lost its flor and oxidised; nutty-hazelnut, dried orange, coffee, and walnut complexity; 18% abv; bone-dry',
 'charcuterie_cheese', 'sweet_salty', 'Sobrasada (Mallorcan spreadable chorizo) on pan de cristal with honey — the oxidative Sherry''s complexity handles the spiced-fatty sobrasada''s richness',
 'complement', 'Amontillado''s hazelnut-dried orange complexity is a natural companion to sobrasada''s spiced pork richness; honey bridges the wine''s dried citrus notes', 'aperitif', 'suggested', 2, true),

-- ============================================================
-- 359: Lustau Peninsula Palo Cortado (2 → 5 target; add 3)
-- Rare oxidative-plus-flor category; walnut, caramel, complexity
-- ============================================================
(359, 'wine_fortified', 'Palo Cortado', 'Lustau Peninsula Palo Cortado — a rare category: a Fino that partly retained flor then oxidised; complexity of Amontillado + richness of Oloroso; walnut, caramel, dried orange, tobacco; 19% abv',
 'meat_poultry', 'rich_fatty_smoky', 'Slow-roasted presa ibérica with Palo Cortado reduction — Palo Cortado reduced into a sauce creates the ultimate Sherry-pork synergy',
 'complement', 'Palo Cortado''s complexity bridges the Fino freshness and Oloroso richness of a reduction sauce; the Ibérico pork''s fat quality matches the wine''s own extraordinary complexity', 'main', 'established', 2, true),

(359, 'wine_fortified', 'Palo Cortado', 'Lustau Peninsula Palo Cortado — a rare category: a Fino that partly retained flor then oxidised; complexity of Amontillado + richness of Oloroso; walnut, caramel, dried orange, tobacco; 19% abv',
 'charcuterie_cheese', 'fermented_aged', 'Aged Zamorano (12-month sheep''s milk DOP from Zamora) — the most structured of Spanish aged sheep''s milk cheeses paired with the most structured Sherry category',
 'complement', 'Zamorano''s exceptional intensity and concentration demand the complexity of Palo Cortado; the wine''s dual character (Fino freshness + Oloroso richness) handles both the cheese''s sharpness and fat', 'cheese', 'established', 2, true),

(359, 'wine_fortified', 'Palo Cortado', 'Lustau Peninsula Palo Cortado — a rare category: a Fino that partly retained flor then oxidised; complexity of Amontillado + richness of Oloroso; walnut, caramel, dried orange, tobacco; 19% abv',
 'dessert_pastry', 'sweet_spiced', 'Tocino de cielo (caramel egg custard) — the Jerez dessert made from egg yolks (a by-product of flor fining); naturally aligned with Palo Cortado',
 'complement', 'Tocino de cielo originated in Jerez from egg yolk surplus; serving it with Palo Cortado creates a local cycle: the same production process (flor) produced both the wine''s character and the dessert ingredient', 'dessert', 'classic', 2, true),

-- ============================================================
-- 360: González Byass Noé Pedro Ximénez VORS
-- Ultra-sweet, 30-year average age PX; raisin, fig, molasses, chocolate
-- ============================================================
(360, 'wine_fortified', 'Pedro Ximénez', 'González Byass Noé PX VORS — 30-year average age Pedro Ximénez from sun-dried grapes; extraordinary concentration: molasses, raisin, fig, dark chocolate, coffee; 15.5% abv; poured over ice cream',
 'dessert_pastry', 'sweet_spiced', 'Vanilla gelato with Noé poured over (affogato-style) — the most famous PX application; the cold gelato vs. warm treacle complexity',
 'complement', 'PX poured over vanilla ice cream is one of Spain''s most celebrated dessert presentations: the contrast of cold cream and warm molasses-raisin creates a hot-cold textural pairing', 'dessert', 'classic', 2, true),

(360, 'wine_fortified', 'Pedro Ximénez', 'González Byass Noé PX VORS — 30-year average age Pedro Ximénez from sun-dried grapes; extraordinary concentration: molasses, raisin, fig, dark chocolate, coffee; 15.5% abv; poured over ice cream',
 'charcuterie_cheese', 'fermented_aged', 'Cabrales (Asturian cave-aged blue cheese) with walnut bread — PX''s sweetness creates a Sauternes-with-Roquefort type contrast pairing with Spain''s most powerful blue cheese',
 'contrast', 'Cabrales'' extreme, ammonia-sharp blue mould character is balanced by PX''s extraordinary sweetness; the sweetness-salt-umami triangle is one of wine''s most compelling contrast pairings', 'cheese', 'classic', 2, true),

(360, 'wine_fortified', 'Pedro Ximénez', 'González Byass Noé PX VORS — 30-year average age Pedro Ximénez from sun-dried grapes; extraordinary concentration: molasses, raisin, fig, dark chocolate, coffee; 15.5% abv; poured over ice cream',
 'dessert_pastry', 'sweet_spiced', 'Polvorones and mantecados (Christmas almond-lard shortbreads from Andalusia) — the traditional Spanish Christmas sweet for the region''s most celebrated dessert wine',
 'complement', 'Polvorones'' crumbling almond-lard richness dissolves against PX''s concentrated sweetness; a Christmas tradition in Jerez combining the region''s two great gift products', 'celebration', 'classic', 2, true),

(360, 'wine_fortified', 'Pedro Ximénez', 'González Byass Noé PX VORS — 30-year average age Pedro Ximénez from sun-dried grapes; extraordinary concentration: molasses, raisin, fig, dark chocolate, coffee; 15.5% abv; poured over ice cream',
 'dessert_pastry', 'sweet_spiced', 'Dark chocolate and salted caramel tart — the chocolate-caramel dessert and PX''s own coffee-chocolate-molasses are mirror images',
 'complement', 'PX VORS''s dark chocolate and coffee notes create a flavour mirror with dark chocolate tart; salted caramel adds the sweet-salt tension that keeps the pairing from becoming cloying', 'dessert', 'established', 2, true),

-- ============================================================
-- 361: Equipo Navazos La Bota de Amontillado (2 → 5 target; add 3)
-- Single-cask aged Amontillado; rare bottling, extreme complexity
-- ============================================================
(361, 'wine_fortified', 'Amontillado', 'Equipo Navazos La Bota de Amontillado — single-cask Amontillado from specific bota releases; extraordinary individual complexity; hazelnut, tobacco, dried orange peel, sea salt; artisan Sherry culture',
 'seafood', 'umami_savoury', 'Kokotxas al pil pil (salt cod cheeks in olive oil emulsion, Basque style) — the complexity of Amontillado meets the extraordinary technique of the Basque preparations',
 'complement', 'La Bota de Amontillado''s individual complexity demands a dish of equivalent technique; kokotxas al pil pil''s gelatinous-olive oil emulsion and the wine''s sea-salt-hazelnut create an extraordinary match', 'main', 'established', 1, true),

(361, 'wine_fortified', 'Amontillado', 'Equipo Navazos La Bota de Amontillado — single-cask Amontillado from specific bota releases; extraordinary individual complexity; hazelnut, tobacco, dried orange peel, sea salt; artisan Sherry culture',
 'charcuterie_cheese', 'fermented_aged', 'Torta del Casar (runny Extremeñan raw sheep''s milk cheese) — Spain''s most unusual cheese; its liquid-runny interior and bitter mould rind paired with the most complex Amontillado',
 'complement', 'Torta del Casar''s liquid-bitter-sheep complexity and La Bota''s individual hazelnut-tobacco depth create one of Spain''s most intellectually stimulating cheese-wine pairings', 'cheese', 'established', 1, true),

(361, 'wine_fortified', 'Amontillado', 'Equipo Navazos La Bota de Amontillado — single-cask Amontillado from specific bota releases; extraordinary individual complexity; hazelnut, tobacco, dried orange peel, sea salt; artisan Sherry culture',
 'meat_poultry', 'earthy_herbal', 'Mollejas de ternera (veal sweetbreads) with Amontillado reduction and capers — sweetbreads'' rich-delicate character amplified by the wine''s complexity',
 'complement', 'Veal sweetbreads'' extraordinary delicacy demands a wine of complexity rather than power; La Bota''s individual character and hazelnut depth match the offal''s richness without overwhelming it', 'main', 'suggested', 1, true),

-- ============================================================
-- 362: Domaine Sigalas Santorini Assyrtiko
-- Greece's finest white; volcanic, saline, citrus, extraordinary minerality
-- ============================================================
(362, 'wine_still', 'Santorini PDO', 'Domaine Sigalas Assyrtiko — Santorini''s caldera terroir; old Assyrtiko basket-trained vines (koulouri) in volcanic pumice-ash soil; lemon, white mineral, saline, citrus precision',
 'seafood', 'salty_mineral', 'Ktapodi (grilled octopus) on the marble terrace with lemon, capers, and olive oil — the definitive Santorini taverna experience',
 'complement', 'Sigalas Assyrtiko and grilled octopus over lava rock is Santorini''s defining food-wine experience: the wine''s volcanic mineral character and the octopus''s sea-char are born from the same volcanic landscape', 'main', 'classic', 2, true),

(362, 'wine_still', 'Santorini PDO', 'Domaine Sigalas Assyrtiko — Santorini''s caldera terroir; old Assyrtiko basket-trained vines (koulouri) in volcanic pumice-ash soil; lemon, white mineral, saline, citrus precision',
 'seafood', 'salty_mineral', 'Psari plaki (baked sea bream with tomatoes, onions, and herbs) — the traditional Greek oven-baked fish preparation with Greece''s finest white wine',
 'complement', 'Assyrtiko''s powerful acidity and volcanic mineral character were made for Greek oven-baked fish; the herb-tomato base bridges the wine''s citrus-mineral character', 'main', 'classic', 2, true),

(362, 'wine_still', 'Santorini PDO', 'Domaine Sigalas Assyrtiko — Santorini''s caldera terroir; old Assyrtiko basket-trained vines (koulouri) in volcanic pumice-ash soil; lemon, white mineral, saline, citrus precision',
 'vegetables_legumes', 'salty_mineral', 'Taramosalata with warm pita and olives — the Greek fish roe appetiser that requires a wine of mineral weight and acidity',
 'complement', 'Taramosalata''s briny, oily fish roe needs Assyrtiko''s powerful acidity and saline mineral character to cut through; the wine''s volcanic mineral echoes the seafood''s depth', 'aperitif', 'classic', 2, true),

(362, 'wine_still', 'Santorini PDO', 'Domaine Sigalas Assyrtiko — Santorini''s caldera terroir; old Assyrtiko basket-trained vines (koulouri) in volcanic pumice-ash soil; lemon, white mineral, saline, citrus precision',
 'seafood', 'delicate_fresh', 'Saganaki (pan-fried Graviera cheese) with honey and sesame — the Greek cheese-frying tradition; the wine''s acidity cuts through the frying while mineral character bridges the honey',
 'complement', 'Saganaki''s crispy-melting cheese needs a wine of acidity; Assyrtiko''s lemony precision and mineral depth cleanse the frying fat while the volcanic character bridges with honey', 'amuse', 'established', 2, true),

-- ============================================================
-- 363: Domaine Sigalas Nykteri
-- Skin-contact/barrel-aged Assyrtiko; richer, textured, complex
-- ============================================================
(363, 'wine_still', 'Santorini PDO', 'Sigalas Nykteri — Santorini''s historic ''night harvest'' white; Assyrtiko barrel-aged; richer and more textured than the standard; mineral, citrus zest, dried apricot, cream, saline',
 'seafood', 'umami_savoury', 'Lobster yiouvetsi (lobster baked in tomato and orzo) — the Aegean luxury preparation for Santorini''s most ambitious white wine',
 'complement', 'Nykteri''s barrel-aged richness and mineral depth are the only Santorini white with the structure for lobster''s sweetness and the orzo''s starch; a prestige island pairing', 'main', 'established', 2, true),

(363, 'wine_still', 'Santorini PDO', 'Sigalas Nykteri — Santorini''s historic ''night harvest'' white; Assyrtiko barrel-aged; richer and more textured than the standard; mineral, citrus zest, dried apricot, cream, saline',
 'charcuterie_cheese', 'fermented_aged', 'Aged Graviera Santorinis (island-produced aged Graviera) with dried figs and walnuts — using the island''s own cheese with the island''s most ambitious wine',
 'complement', 'Graviera Santorinis is produced on the same volcanic island as Nykteri; the cheese''s sweet-nutty caramel character bridges with the wine''s dried apricot and cream; a true island terroir pairing', 'cheese', 'established', 2, true),

(363, 'wine_still', 'Santorini PDO', 'Sigalas Nykteri — Santorini''s historic ''night harvest'' white; Assyrtiko barrel-aged; richer and more textured than the standard; mineral, citrus zest, dried apricot, cream, saline',
 'seafood', 'rich_fatty_smoky', 'Fried salt cod (bakaliaros skordalia) with garlic-potato sauce — the ancient Greek Lenten preparation; the wine''s structure matches the cod''s salt and the skordalia''s garlic',
 'complement', 'Nykteri''s barrel-aged weight handles salt cod''s intensity better than the lighter Assyrtiko; the skordalia''s garlic is countered by the wine''s mineral acidity', 'main', 'established', 2, true),

(363, 'wine_still', 'Santorini PDO', 'Sigalas Nykteri — Santorini''s historic ''night harvest'' white; Assyrtiko barrel-aged; richer and more textured than the standard; mineral, citrus zest, dried apricot, cream, saline',
 'meat_poultry', 'delicate_fresh', 'Kotopoulo lemonato (lemon-roasted chicken with herbs) — Nykteri''s texture and citrus character bridge to the lemon-herb chicken preparation',
 'complement', 'Nykteri is one of the few Greek whites with the barrel-aged structure for chicken dishes; its citrus-cream character mirrors the lemon marinade while its mineral acidity cuts the fat', 'main', 'suggested', 2, true),

-- ============================================================
-- 364: Kir-Yianni Ramnista Naoussa
-- Xinomavro; Greece's Barolo; tar, roses, tomato, leather, high acidity
-- ============================================================
(364, 'wine_still', 'Naoussa PDO', 'Kir-Yianni Ramnista — Naoussa''s most celebrated Xinomavro; aged 18 months oak; tar, dried roses, tomato skin, leather, and extraordinary structure; Greece''s Barolo',
 'meat_poultry', 'earthy_herbal', 'Arni kleftiko (slow-cooked lamb sealed in parchment with herbs and vegetables) — the most beloved Greek slow-cook lamb technique for Greece''s most structured red',
 'complement', 'Xinomavro''s Nebbiolo-like tannins and acid structure are designed for slow-cooked lamb; the kleftiko''s herb-parchment aromas bridge the wine''s dried rose and leather character', 'main', 'classic', 2, true),

(364, 'wine_still', 'Naoussa PDO', 'Kir-Yianni Ramnista — Naoussa''s most celebrated Xinomavro; aged 18 months oak; tar, dried roses, tomato skin, leather, and extraordinary structure; Greece''s Barolo',
 'meat_poultry', 'rich_fatty_smoky', 'Stifado (beef and onion stew with cinnamon, cloves, and red wine) — the Greek spiced braised beef that demands a wine of Ramnista''s depth',
 'complement', 'Stifado''s cinnamon-clove-beef reduction creates an aromatic bridge to Xinomavro''s complex dried fruit and spice; the onion''s sweetness softens the wine''s firm tannins', 'main', 'classic', 2, true),

(364, 'wine_still', 'Naoussa PDO', 'Kir-Yianni Ramnista — Naoussa''s most celebrated Xinomavro; aged 18 months oak; tar, dried roses, tomato skin, leather, and extraordinary structure; Greece''s Barolo',
 'charcuterie_cheese', 'fermented_aged', 'Aged Kefalograviera (12-month hard sheep/cow mix) with kalamata olives — the northern Greek cheese from the same Macedonian region as Naoussa',
 'complement', 'Kefalograviera''s hard, salty-nutty character from the Greek mountains bridges with Ramnista''s tar-rose structure; the olives'' brine echoes the wine''s saline minerality', 'cheese', 'established', 2, true),

(364, 'wine_still', 'Naoussa PDO', 'Kir-Yianni Ramnista — Naoussa''s most celebrated Xinomavro; aged 18 months oak; tar, dried roses, tomato skin, leather, and extraordinary structure; Greece''s Barolo',
 'pasta_grain', 'umami_savoury', 'Pastitsio (Greek baked pasta with meat ragù and béchamel) — the Greek comfort classic; its tomato-meat depth bridges with Xinomavro''s tomato-skin character',
 'complement', 'Xinomavro''s tomato skin note (a distinctive characteristic of the variety) resonates with pastitsio''s tomato-meat sauce; the béchamel''s fat softens the wine''s firm tannins', 'main', 'classic', 2, true),

-- ============================================================
-- 365: Barbayanni Blue Label Ouzo
-- Premium Lesvos ouzo; anise, herbs, clean; the benchmark style
-- ============================================================
(365, 'spirits_liqueur', 'Ouzo', 'Barbayanni Blue Label Ouzo — Lesvos (Mytilene) ouzo; multiple distillations with star anise, aniseed, and Greek mountain herbs; clean, complex, benchmark style; 46% abv; louched with water and ice',
 'seafood', 'salty_mineral', 'Grilled octopus with lemon and olive oil, or fried calamari — the defining ouzo meze of the Greek islands',
 'complement', 'Ouzo and seafood is Greece''s foundational food-drink pairing; the anise character cuts through the char of grilled octopus while the spirit''s ice-loucheing refreshes between bites', 'aperitif', 'classic', 2, true),

(365, 'spirits_liqueur', 'Ouzo', 'Barbayanni Blue Label Ouzo — Lesvos (Mytilene) ouzo; multiple distillations with star anise, aniseed, and Greek mountain herbs; clean, complex, benchmark style; 46% abv; louched with water and ice',
 'vegetables_legumes', 'salty_mineral', 'Mezedes spread: taramosalata, tzatziki, fava, spanakopita — the complete Greek meze table for a long afternoon of ouzo',
 'complement', 'Ouzo''s ice-cold, anise-refreshing character is designed for the rhythm of mezedes: sip, eat, sip, eat. The anise cuts through tzatziki''s yoghurt, the fava''s bean earthiness, and the spanakopita''s pastry fat', 'aperitif', 'classic', 2, true),

(365, 'spirits_liqueur', 'Ouzo', 'Barbayanni Blue Label Ouzo — Lesvos (Mytilene) ouzo; multiple distillations with star anise, aniseed, and Greek mountain herbs; clean, complex, benchmark style; 46% abv; louched with water and ice',
 'seafood', 'delicate_fresh', 'Garides saganaki (prawns baked with tomatoes, ouzo, and feta) — the dish cooked with ouzo served alongside ouzo',
 'complement', 'Garides saganaki is traditionally flambéed with ouzo; serving the same spirit in the glass creates the ''wine in the dish + wine in the glass'' parallel unique to this preparation', 'main', 'classic', 2, true),

(365, 'spirits_liqueur', 'Ouzo', 'Barbayanni Blue Label Ouzo — Lesvos (Mytilene) ouzo; multiple distillations with star anise, aniseed, and Greek mountain herbs; clean, complex, benchmark style; 46% abv; louched with water and ice',
 'charcuterie_cheese', 'salty_mineral', 'Feta PDO with watermelon and kalamata olives — the Greek summer combination that defines the country''s food identity alongside its most iconic spirit',
 'complement', 'Feta''s salt-acid character and the watermelon''s sweet contrast find the ouzo''s anise a surprisingly harmonious bridge; the ice-cold louchée refreshes against the summer flavours', 'aperitif', 'established', 2, true),

-- ============================================================
-- 366: Plomari Original Ouzo (2 → 5 target; add 3)
-- Lesvos ouzo; established benchmark; mastic and anise notes
-- ============================================================
(366, 'spirits_liqueur', 'Ouzo', 'Plomari Original Ouzo — Isidoros Arvanitis distillery from Plomari, Lesvos; a classic ouzo with mastic and anise; more aromatic complexity than simpler styles; 40% abv',
 'seafood', 'salty_mineral', 'Kalamari tiganito (fried squid) with skordalia — the crispy-fried squid and garlic potato sauce that is the ouzo companion par excellence',
 'complement', 'Plomari''s anise and mastic complexity is uniquely suited for fried squid''s light batter-oil character; the mastic note echoes the garlic-olive oil skordalia', 'aperitif', 'classic', 2, true),

(366, 'spirits_liqueur', 'Ouzo', 'Plomari Original Ouzo — Isidoros Arvanitis distillery from Plomari, Lesvos; a classic ouzo with mastic and anise; more aromatic complexity than simpler styles; 40% abv',
 'charcuterie_cheese', 'fermented_aged', 'Loukaniko (Greek pork sausage with orange peel) with grilled pita — the cured pork''s orange peel character bridges with the ouzo''s citrus-anise notes',
 'bridge', 'Loukaniko''s orange peel and the ouzo''s anise-citrus complexity create an aromatic bridge; the grilled pita''s char provides a welcome bitterness to the combination', 'aperitif', 'established', 2, true),

(366, 'spirits_liqueur', 'Ouzo', 'Plomari Original Ouzo — Isidoros Arvanitis distillery from Plomari, Lesvos; a classic ouzo with mastic and anise; more aromatic complexity than simpler styles; 40% abv',
 'seafood', 'umami_savoury', 'Htapodi stifado (octopus stewed in wine with cinnamon and pearl onions) — the braised octopus preparation that matches the complexity of Plomari''s more aromatic style',
 'complement', 'Htapodi stifado''s cinnamon-wine-onion complexity demands an ouzo of Plomari''s aromatic depth; the mastic note bridges the wine''s sweet spice and the octopus''s sea character', 'main', 'established', 2, true),

-- ============================================================
-- 367: Chateau Musar Rouge
-- Lebanon's legendary red; Cabernet, Cinsault, Carignan; extraordinary complexity
-- ============================================================
(367, 'wine_still', 'Bekaa Valley', 'Chateau Musar Rouge — Lebanon''s legendary wine; Cabernet Sauvignon, Cinsault, Carignan from Bekaa Valley; Serge Hochar''s creation; extraordinary complexity: cedar, dried rose, earth, exotic spice, leather',
 'meat_poultry', 'earthy_herbal', 'Kibbeh bil saniyeh (baked lamb and bulgur wheat cake with pine nuts and spices) — Lebanon''s most celebrated dish for Lebanon''s most celebrated wine',
 'complement', 'Musar Rouge''s exotic spice and cedar character resonate with kibbeh''s cinnamon-allspice-pine nut lamb filling; the bulgur''s earthiness bridges the wine''s terroir complexity', 'main', 'classic', 1, true),

(367, 'wine_still', 'Bekaa Valley', 'Chateau Musar Rouge — Lebanon''s legendary wine; Cabernet Sauvignon, Cinsault, Carignan from Bekaa Valley; Serge Hochar''s creation; extraordinary complexity: cedar, dried rose, earth, exotic spice, leather',
 'meat_poultry', 'rich_fatty_smoky', 'Slow-roasted leg of lamb with baharat spice blend, pomegranate molasses, and roasted garlic — the Middle Eastern luxury lamb preparation',
 'complement', 'Baharat''s warming spice blend (allspice, cinnamon, black pepper, coriander) creates an aromatic bridge to Musar''s exotic complexity; pomegranate''s acidity mirrors the wine''s natural acidity from high altitude Bekaa', 'main', 'established', 1, true),

(367, 'wine_still', 'Bekaa Valley', 'Chateau Musar Rouge — Lebanon''s legendary wine; Cabernet Sauvignon, Cinsault, Carignan from Bekaa Valley; Serge Hochar''s creation; extraordinary complexity: cedar, dried rose, earth, exotic spice, leather',
 'charcuterie_cheese', 'fermented_aged', 'Jibneh (Lebanese aged cheese) with dried figs, walnuts, and za''atar flatbread — Middle Eastern cheese board pairing',
 'complement', 'Lebanese aged cheese''s sharp-salty character and the za''atar flatbread''s herbal-sesame notes bridge with Musar''s exotic complexity; dried figs mirror the wine''s fruit at maturity', 'cheese', 'established', 1, true),

(367, 'wine_still', 'Bekaa Valley', 'Chateau Musar Rouge — Lebanon''s legendary wine; Cabernet Sauvignon, Cinsault, Carignan from Bekaa Valley; Serge Hochar''s creation; extraordinary complexity: cedar, dried rose, earth, exotic spice, leather',
 'meat_poultry', 'earthy_herbal', 'Mansaf (Jordanian-Levantine slow-cooked lamb in fermented dried yoghurt with rice and pine nuts) — the Levantine prestige dish for a Levantine prestige wine',
 'complement', 'Mansaf''s jameed yoghurt (fermented and dried) creates a complex tangy-lamb-fat character that bridges with Musar''s cedar-spice depth; the pine nuts add textural contrast', 'main', 'suggested', 1, true),

-- ============================================================
-- 368: Massaya Arak Silver
-- Lebanese arak; grape spirit with anise; louche with water; 53% abv
-- ============================================================
(368, 'spirits_liqueur', 'Arak', 'Massaya Arak Silver — Lebanese arak from grape spirit triple-distilled with star anise; the national drink of Lebanon; louche (''lion''s milk'') when mixed with water; 53% abv',
 'vegetables_legumes', 'salty_mineral', 'Lebanese mezze spread: hummus, baba ganoush, fattoush, kibbeh nayeh — arak''s traditional role as the mezze companion',
 'complement', 'Arak is the foundational Lebanese mezze companion: its anise character cuts through hummus''s sesame-olive oil richness, refreshes between dishes, and pairs with the smoke of baba ganoush', 'aperitif', 'classic', 2, true),

(368, 'spirits_liqueur', 'Arak', 'Massaya Arak Silver — Lebanese arak from grape spirit triple-distilled with star anise; the national drink of Lebanon; louche (''lion''s milk'') when mixed with water; 53% abv',
 'meat_poultry', 'earthy_herbal', 'Mixed grill (kafta, shish taouk, lamb chops) with flatbread and pickles — the Lebanese grill tradition with its canonical spirit',
 'complement', 'Arak''s cool anise refreshes the palate between the smoky, spiced, charred meats of a Lebanese mixed grill; the cold louchée (with water) contrasts the heat', 'main', 'classic', 2, true),

(368, 'spirits_liqueur', 'Arak', 'Massaya Arak Silver — Lebanese arak from grape spirit triple-distilled with star anise; the national drink of Lebanon; louche (''lion''s milk'') when mixed with water; 53% abv',
 'seafood', 'salty_mineral', 'Sayadieh (spiced fish over rice with caramelised onions and pine nuts) — the Lebanese fish-rice preparation that pairs well with diluted arak',
 'complement', 'Sayadieh''s complex spice profile (cumin, coriander, turmeric) and the caramelised onion sweetness find the anise''s coolness a natural contrast; the fish''s delicacy is not overwhelmed', 'main', 'established', 2, true),

(368, 'spirits_liqueur', 'Arak', 'Massaya Arak Silver — Lebanese arak from grape spirit triple-distilled with star anise; the national drink of Lebanon; louche (''lion''s milk'') when mixed with water; 53% abv',
 'charcuterie_cheese', 'salty_mineral', 'Shanklish (aged and herbed Lebanese cheese) with tomato, onion, and olive oil — the traditional arak meze cheese',
 'complement', 'Shanklish''s fermented, herb-rolled, intensely flavoured character is the classic arak meze cheese; its sharpness is softened by the spirit''s anise and the tomato-onion freshness', 'aperitif', 'classic', 2, true),

-- ============================================================
-- 369: Moroccan Atay — Gunpowder Green Tea with Nana Mint
-- Ceremonial sweet mint tea; ritual preparation; no alcohol
-- ============================================================
(369, 'na_crafted', 'Ceremonial Mint Tea', 'Moroccan Atay — gunpowder green tea steeped with fresh nana (spearmint) and sugar; poured from height to create froth; three glasses traditionally; the hospitality ritual of the Maghreb',
 'dessert_pastry', 'sweet_spiced', 'Cornes de gazelle (gazelle horn pastries) with orange blossom and almond — the classic Moroccan pastry served with mint tea',
 'complement', 'Cornes de gazelle and Atay is Morocco''s most fundamental hospitality ritual: the flaky almond-orange blossom crescent and the mint-sweet tea were designed together', 'dessert', 'classic', 2, true),

(369, 'na_crafted', 'Ceremonial Mint Tea', 'Moroccan Atay — gunpowder green tea steeped with fresh nana (spearmint) and sugar; poured from height to create froth; three glasses traditionally; the hospitality ritual of the Maghreb',
 'dessert_pastry', 'sweet_spiced', 'Baklava with pistachio and honey — the pan-Arab pastry with layered filo, nut filling, and honey syrup finds the mint tea''s sweetness its natural companion',
 'complement', 'Baklava''s honey-pistachio richness is cut by the mint tea''s fresh herbal clarity; the tea''s own sweetness prevents the pastry''s sugar from feeling excessive', 'dessert', 'classic', 2, true),

(369, 'na_crafted', 'Ceremonial Mint Tea', 'Moroccan Atay — gunpowder green tea steeped with fresh nana (spearmint) and sugar; poured from height to create froth; three glasses traditionally; the hospitality ritual of the Maghreb',
 'meat_poultry', 'sweet_spiced', 'Tagine de poulet au citron confit et olives (chicken tagine with preserved lemon and green olives) — the tea is served before and after the tagine in traditional Moroccan hospitality',
 'bridge', 'The mint tea''s sweetness and herb freshness creates a palate bridge between the tagine''s preserved lemon acidity and the meal''s finale; traditionally poured before and after food', 'main', 'classic', 2, true),

(369, 'na_crafted', 'Ceremonial Mint Tea', 'Moroccan Atay — gunpowder green tea steeped with fresh nana (spearmint) and sugar; poured from height to create froth; three glasses traditionally; the hospitality ritual of the Maghreb',
 'dessert_pastry', 'sweet_fruity', 'M''hancha (Moroccan snake pastry) with almond paste, cinnamon, and orange blossom — the coiled pastry that requires a glass of hot sweet mint tea',
 'complement', 'M''hancha''s cinnamon-almond-orange blossom filling and the tea''s mint-sugar aromatics are complementary: the pastry''s sweetness is balanced by the tea''s herbal freshness', 'dessert', 'classic', 2, true),

-- ============================================================
-- 370: Kurukahveci Mehmet Efendi Turkish Coffee
-- The definitive Turkish coffee; dark roast, unfiltered, prepared in cezve
-- ============================================================
(370, 'coffee', 'Turkish Cezve', 'Kurukahveci Mehmet Efendi Turkish Coffee — Istanbul''s most famous coffee brand (est. 1871); dark-roasted Arabica blend ground to powder, prepared in cezve/ibrik; thick, unfiltered, served with Turkish delight',
 'dessert_pastry', 'sweet_spiced', 'Turkish delight (lokum) — rose, pistachio, or mastic varieties; the traditional accompaniment served with every Turkish coffee',
 'complement', 'Turkish coffee and lokum is the defining hospitality pairing of Ottoman culture: the bitter-sweet coffee and the sweet-floral lokum create a sweet-bitter contrast ritual', 'digestif', 'classic', 2, true),

(370, 'coffee', 'Turkish Cezve', 'Kurukahveci Mehmet Efendi Turkish Coffee — Istanbul''s most famous coffee brand (est. 1871); dark-roasted Arabica blend ground to powder, prepared in cezve/ibrik; thick, unfiltered, served with Turkish delight',
 'dessert_pastry', 'sweet_spiced', 'Baklava with pistachio (Gaziantep style) — the densely sweet nut pastry with the intensely bitter-thick coffee creates the classic sweet-bitter balance',
 'contrast', 'Turkish coffee''s intense bitterness is the perfect counter to baklava''s overwhelming sweetness; both are consumed at the same occasion as complementary contrasts in the Ottoman dessert tradition', 'digestif', 'classic', 2, true),

(370, 'coffee', 'Turkish Cezve', 'Kurukahveci Mehmet Efendi Turkish Coffee — Istanbul''s most famous coffee brand (est. 1871); dark-roasted Arabica blend ground to powder, prepared in cezve/ibrik; thick, unfiltered, served with Turkish delight',
 'charcuterie_cheese', 'sweet_salty', 'Beyaz peynir (Turkish white cheese, similar to feta) with olives, tomatoes, and egg — the traditional Turkish breakfast board followed by Turkish coffee',
 'bridge', 'Turkish breakfast (kahvaltı) culminates with coffee; the transition from salty-fatty cheese-egg-olive to the sweet-bitter coffee creates the morning''s flavour arc in Turkish culture', 'any', 'classic', 2, true),

(370, 'coffee', 'Turkish Cezve', 'Kurukahveci Mehmet Efendi Turkish Coffee — Istanbul''s most famous coffee brand (est. 1871); dark-roasted Arabica blend ground to powder, prepared in cezve/ibrik; thick, unfiltered, served with Turkish delight',
 'dessert_pastry', 'sweet_spiced', 'Künefe (Hatay cheese pastry soaked in syrup) — the famous hot-sweet-stringy cheese dessert from southern Turkey that demands the bitter counterpoint of coffee',
 'contrast', 'Künefe''s hot, sweet, stretchy cheese-pastry-syrup combination is overwhelming without the bitter contrast of Turkish coffee; they are traditionally served together in the region', 'digestif', 'established', 2, true);

COMMIT;
