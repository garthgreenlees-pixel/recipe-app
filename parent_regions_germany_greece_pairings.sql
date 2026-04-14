BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 435: Bouchard Côte de Nuits-Villages
(435, 'wine_still', 'Côte de Nuits-Villages Pinot Noir',
 'Red cherry, earth, mild tannin, forest floor, gentle spice; village-level Burgundy.',
 'meat', 'chicken mushroom',
 'Chicken fricassée with wild mushrooms and cream; the wine''s earthy village Pinot character is at ease with this classic Burgundian preparation.',
 'complement', 'Forest floor and earth in wine mirror wild mushrooms; silk tannin matches the cream sauce''s gentle richness.',
 'main', 'classic', 1, true),

(435, 'wine_still', 'Côte de Nuits-Villages Pinot Noir',
 'Red cherry, earth, mild tannin, forest floor, gentle spice; village-level Burgundy.',
 'cheese', 'aged semi-soft',
 'Comté 12-month or aged Munster; the wine''s earthy, gentle spice character pairs well with the mild mineral depth of younger mountain cheese.',
 'complement', 'Gentle spice in wine bridges the Comté''s nutty character; earth and red cherry balance the cheese''s mild acidity.',
 'cheese', 'established', 1, true),

(435, 'wine_still', 'Côte de Nuits-Villages Pinot Noir',
 'Red cherry, earth, mild tannin, forest floor, gentle spice; village-level Burgundy.',
 'meat', 'pork roasted',
 'Roast pork loin with mustard and cherry sauce; the wine''s mild tannin and red cherry freshness suit pork''s neutral character.',
 'complement', 'Red cherry in wine echoed in cherry sauce; mild tannin integrates with pork''s lean protein; mustard''s tang lifts the wine''s gentle spice.',
 'main', 'established', 1, true),

-- 436: Drouhin Côte de Beaune-Villages
(436, 'wine_still', 'Côte de Beaune-Villages Pinot Noir',
 'Raspberry, light earth, silk tannin, red fruit, gentle mineral; Beaune village blend.',
 'meat', 'rabbit casserole',
 'Rabbit in white wine with tarragon and mustard; the wine''s silky lightness and red fruit freshness match lean rabbit''s delicate character.',
 'complement', 'Silk tannin and light earth match the delicacy of rabbit; tarragon bridges the wine''s gentle mineral and herbal registers.',
 'main', 'classic', 1, true),

(436, 'wine_still', 'Côte de Beaune-Villages Pinot Noir',
 'Raspberry, light earth, silk tannin, red fruit, gentle mineral; Beaune village blend.',
 'fish', 'salmon tuna',
 'Tuna tataki or roasted salmon; the wine''s raspberry acidity and silk structure make a surprisingly elegant partner for meaty fish.',
 'bridge', 'Light Pinot tannin acts as bridge between fish''s oiliness and the wine''s red fruit; silk texture mirrors the fish''s delicate flesh.',
 'main', 'adventurous', 1, true),

(436, 'wine_still', 'Côte de Beaune-Villages Pinot Noir',
 'Raspberry, light earth, silk tannin, red fruit, gentle mineral; Beaune village blend.',
 'charcuterie', 'pâté terrine',
 'Country pâté or chicken liver mousse with brioche; the wine''s gentle red fruit and silk tannin are a graceful match for French terrine.',
 'complement', 'Silk tannin balances the fat of pâté; raspberry brightness lifts the liver richness; gentle mineral provides a clean finish.',
 'starter', 'established', 1, true),

-- 437: Château Pichon Comtesse de Lalande
(437, 'wine_still', 'Pauillac Super-Second Bordeaux',
 'Cassis, cedar, violet floral, dark plum, graphite; unusually supple for Pauillac.',
 'meat', 'lamb slow-roasted',
 'Slow-roasted leg of lamb with rosemary and garlic; the supple Pichon Comtesse style with violet florality is ideal for herb-roasted lamb.',
 'complement', 'Cassis and cedar are the Bordeaux counterpart for lamb; violet florality adds elegance absent in more tannic Pauillac.',
 'main', 'classic', 1, true),

(437, 'wine_still', 'Pauillac Super-Second Bordeaux',
 'Cassis, cedar, violet floral, dark plum, graphite; unusually supple for Pauillac.',
 'meat', 'beef wellington',
 'Beef Wellington or filet with sauce bordelaise; the wine''s graphite-cedar structure finds its most resonant partner in classic beef preparations.',
 'complement', 'Graphite tannin integrates with beef fat; sauce bordelaise echoes the wine''s own red wine reduction notes; cedar adds structural depth.',
 'main', 'established', 1, true),

(437, 'wine_still', 'Pauillac Super-Second Bordeaux',
 'Cassis, cedar, violet floral, dark plum, graphite; unusually supple for Pauillac.',
 'cheese', 'aged hard',
 'Aged Comté or vintage Cheddar; the wine''s graphite and cedar need a cheese of sufficient complexity and structure to match.',
 'complement', 'Graphite and cedar in wine mirror the mineral-nutty depth of aged hard cheese; violet florality brightens what could otherwise be a heavy pairing.',
 'cheese', 'established', 1, true),

-- 438: Château Lynch-Bages
(438, 'wine_still', 'Médoc Pauillac Fifth Growth',
 'Blackcurrant, cedar, olive tapenade, dark plum, tobacco, spiced oak.',
 'meat', 'lamb herb',
 'Herb-crusted rack of lamb; the wine''s olive tapenade and cassis notes find classic expression alongside herb-roasted lamb.',
 'complement', 'Olive tapenade character in wine bridges herb crust on lamb; blackcurrant and cedar are the classic Médoc-lamb pairing.',
 'main', 'classic', 1, true),

(438, 'wine_still', 'Médoc Pauillac Fifth Growth',
 'Blackcurrant, cedar, olive tapenade, dark plum, tobacco, spiced oak.',
 'meat', 'beef sirloin',
 'Grilled sirloin or rib-eye with horseradish cream; Lynch-Bages'' generous, approachable style suits confidently seasoned grilled beef.',
 'complement', 'Blackcurrant and dark plum of Lynch-Bages mirror the caramelised crust of grilled beef; horseradish''s spice echoes the wine''s tobacco-spice register.',
 'main', 'established', 1, true),

(438, 'wine_still', 'Médoc Pauillac Fifth Growth',
 'Blackcurrant, cedar, olive tapenade, dark plum, tobacco, spiced oak.',
 'cheese', 'aged cheddar',
 'Montgomery''s Cheddar or Lincolnshire Poacher; the wine''s generosity and approachability pair well with Britain''s great aged cheddar.',
 'complement', 'Tobacco and spiced oak in wine align with the nutty crystalline character of aged cheddar; blackcurrant cuts the cheese''s acidity.',
 'cheese', 'established', 1, true),

-- 439: E. Guigal Côtes du Rhône
(439, 'wine_still', 'Côtes du Rhône GSM Regional Blend',
 'Dark cherry, garrigue, black pepper, dried herb, warm spice, mineral; Grenache/Syrah/Mourvèdre.',
 'meat', 'grilled lamb merguez',
 'Merguez sausage or grilled lamb cutlets with harissa; the wine''s garrigue and pepper warmth are made for Southern French grilled meat.',
 'complement', 'Garrigue and pepper in wine echo the spice profile of merguez and harissa; dark cherry bridges the char of grilled lamb.',
 'casual', 'classic', 1, true),

(439, 'wine_still', 'Côtes du Rhône GSM Regional Blend',
 'Dark cherry, garrigue, black pepper, dried herb, warm spice, mineral; Grenache/Syrah/Mourvèdre.',
 'meat', 'pizza pissaladière',
 'Pissaladière (Provençal anchovy-onion tart) or pizza with caramelised onions and olives; the wine''s garrigue-olive character is a natural for Southern French/Italian baked dishes.',
 'complement', 'Garrigue in wine mirrors the olive and dried herb of pissaladière; dark cherry brightness contrasts the anchovy''s salty intensity.',
 'casual', 'established', 1, true),

(439, 'wine_still', 'Côtes du Rhône GSM Regional Blend',
 'Dark cherry, garrigue, black pepper, dried herb, warm spice, mineral; Grenache/Syrah/Mourvèdre.',
 'cheese', 'aged sheep goat',
 'Banon or aged Picodon (Ardèche); Rhône Valley wine and Provençal goat/sheep cheese share Southern French terroir and are natural partners.',
 'complement', 'Regional affinity: Rhône wine and Provençal cheese; garrigue note echoes the herb-influenced milk character of Provençal cheese.',
 'cheese', 'established', 1, true),

-- 440: Jean-Louis Chave Hermitage Rouge
(440, 'wine_still', 'Hermitage Northern Rhône Grand Vin Syrah',
 'Smoked olive, dark berry, violet, iron, white pepper, dark chocolate; 20-40 year wine.',
 'meat', 'beef dry-aged',
 'Dry-aged côte de boeuf or bone-in ribeye; Hermitage''s iron-mineral density and tannic authority demand the highest quality aged beef.',
 'complement', 'Iron mineral in Chave Hermitage aligns with dry-aged beef''s iron-rich myoglobin; white pepper mirrors the char crust''s spice.',
 'main', 'classic', 1, true),

(440, 'wine_still', 'Hermitage Northern Rhône Grand Vin Syrah',
 'Smoked olive, dark berry, violet, iron, white pepper, dark chocolate; 20-40 year wine.',
 'meat', 'lamb braised',
 'Braised lamb shank with black olive tapenade and rosemary; the wine''s smoked olive and pepper create an immediate affinity with Provençal lamb.',
 'complement', 'Smoked olive in wine mirrors black olive tapenade; white pepper and rosemary bridge the wine''s Northern Rhône spice.',
 'main', 'established', 1, true),

(440, 'wine_still', 'Hermitage Northern Rhône Grand Vin Syrah',
 'Smoked olive, dark berry, violet, iron, white pepper, dark chocolate; 20-40 year wine.',
 'cheese', 'aged hard hard',
 'Aged Comté (36-month) or Gruyère de Cave; the wine''s iron and mineral depth require a cheese of equivalent complexity.',
 'complement', 'Mineral iron core of Chave echoes the 36-month Comté''s extraordinary mineral depth; dark chocolate in wine bridges the cheese''s bitter crystalline notes.',
 'cheese', 'established', 1, true),

(440, 'wine_still', 'Hermitage Northern Rhône Grand Vin Syrah',
 'Smoked olive, dark berry, violet, iron, white pepper, dark chocolate; 20-40 year wine.',
 'meat', 'venison game',
 'Roasted venison loin with dark berry reduction; the wine''s iron density and dark berry depth find their most noble partner in red game.',
 'complement', 'Dark berry reduction echoes the wine''s fruit; iron in both wine and venison creates alignment; white pepper adds spice bridge.',
 'main', 'adventurous', 1, true),

-- 441: Château Beaucastel CdP Blanc
(441, 'wine_still', 'Châteauneuf-du-Pape Blanc Old-Vine Roussanne',
 'Beeswax, dried apricot, roasted hazelnut, honey, savoury mineral; ages 20 years.',
 'fish', 'lobster homard',
 'Lobster thermidor or homard grillé with herb butter; the wine''s beeswax-hazelnut richness creates an extraordinary match for the finest crustacean preparations.',
 'complement', 'Beeswax and hazelnut in Beaucastel Blanc mirror the richness of lobster thermidor; dried apricot provides a sweetness bridge.',
 'main', 'classic', 1, true),

(441, 'wine_still', 'Châteauneuf-du-Pape Blanc Old-Vine Roussanne',
 'Beeswax, dried apricot, roasted hazelnut, honey, savoury mineral; ages 20 years.',
 'poultry', 'chicken cream sauce',
 'Poulet à la crème with morels or chicken suprême with truffle; the wine''s honeyed richness and mineral depth suit luxurious cream-sauce preparations.',
 'complement', 'Honey and beeswax in wine echo the cream sauce richness; savoury mineral bridges the truffle or morel umami.',
 'main', 'established', 1, true),

(441, 'wine_still', 'Châteauneuf-du-Pape Blanc Old-Vine Roussanne',
 'Beeswax, dried apricot, roasted hazelnut, honey, savoury mineral; ages 20 years.',
 'cheese', 'aged sheep hard',
 'Aged Ossau-Iraty or Manchego (3 year); the wine''s lanolin-beeswax character aligns with the sheep''s milk fat and nutty complexity of aged ewes'' cheese.',
 'complement', 'Beeswax and lanolin in wine mirror the sheep''s milk fat character; dried apricot echoes the fruity nutty complexity of aged Ossau-Iraty.',
 'cheese', 'established', 1, true),

-- 442: Henry Marionnet Touraine Sauvignon Blanc
(442, 'wine_still', 'Loire Valley Touraine Sauvignon Blanc',
 'Gooseberry, elder flower, white grapefruit, chalk mineral, cut grass, clean finish.',
 'shellfish', 'oysters clams',
 'Fines de Claire oysters or clams with shallot vinaigrette; the wine''s chalk mineral and gooseberry freshness create a classic Loire-oyster pairing.',
 'complement', 'Chalk mineral echoes oyster shell brine; gooseberry acidity lifts the saline character; elder flower adds a subtle aromatic lift.',
 'aperitif', 'classic', 2, true),

(442, 'wine_still', 'Loire Valley Touraine Sauvignon Blanc',
 'Gooseberry, elder flower, white grapefruit, chalk mineral, cut grass, clean finish.',
 'cheese', 'chèvre fresh',
 'Fresh chèvre log or Crottin de Chavignol; the Loire Valley''s canonical white wine and goat''s cheese pairing — a sense-of-place classic.',
 'complement', 'Classic Loire affinity: gooseberry acidity matches lactic tang of chèvre; elder flower adds a floral lift to the pairing.',
 'cheese', 'classic', 2, true),

(442, 'wine_still', 'Loire Valley Touraine Sauvignon Blanc',
 'Gooseberry, elder flower, white grapefruit, chalk mineral, cut grass, clean finish.',
 'fish', 'white fish herb',
 'Grilled cod or sea bass with herb butter and capers; the wine''s citrus-herb character and crisp mineral acidity cut through white fish preparations.',
 'cleanse', 'White grapefruit acidity cleanses fish fat; cut grass and elder flower echo herb butter aromatics; chalk mineral amplifies the briny fish character.',
 'main', 'established', 2, true),

-- 443: Gaffel Kölsch
(443, 'beer_ale', 'Kölsch — Cologne Top-Fermented',
 'Pale apple, pear ester, gentle hops, bone-dry finish, light biscuit; served cold in Stangen.',
 'fish', 'fried white fish',
 'Fried plaice or schnitzel with lemon; Kölsch''s dry, clean carbonation cuts through fried coating while apple ester echoes the lemon.',
 'cleanse', 'Bone-dry finish and carbonation cut fried coating; gentle ester echoes lemon; light biscuit matches the breaded crust.',
 'main', 'classic', 2, true),

(443, 'beer_ale', 'Kölsch — Cologne Top-Fermented',
 'Pale apple, pear ester, gentle hops, bone-dry finish, light biscuit; served cold in Stangen.',
 'cheese', 'mild fresh',
 'Quark with chives or Frischkäse on bread; the bone-dry Kölsch''s clean profile pairs effortlessly with mild dairy.',
 'complement', 'Bone-dry, clean character of Kölsch does not compete with mild dairy; gentle hop bitterness lifts the cheese''s lactic freshness.',
 'casual', 'established', 2, true),

(443, 'beer_ale', 'Kölsch — Cologne Top-Fermented',
 'Pale apple, pear ester, gentle hops, bone-dry finish, light biscuit; served cold in Stangen.',
 'grain', 'pretzel bread',
 'Bavarian pretzel or Laugenbrötchen with butter; the classic German beer-and-bread pairing elevated by Kölsch''s apple-dry refinement.',
 'complement', 'Light biscuit malt in Kölsch echoes the pretzel''s baked grain; bone-dry finish resets the palate for each bite.',
 'amuse', 'classic', 2, true),

-- 444: Uerige Altbier
(444, 'beer_ale', 'Düsseldorf Altbier Top-Fermented',
 'Caramel malt, assertive hops, roasted grain, dry mineral, dark fruit, copper character.',
 'meat', 'sauerbraten',
 'Sauerbraten (Rhenish pot roast) with red cabbage and potato dumpling; Altbier is the canonical accompaniment to Düsseldorf''s national dish.',
 'complement', 'Sense-of-place perfection: Altbier and Sauerbraten are Düsseldorf''s signature combination; caramel malt bridges the sweet-sour sauce while hops cut through the richness.',
 'main', 'classic', 2, true),

(444, 'beer_ale', 'Düsseldorf Altbier Top-Fermented',
 'Caramel malt, assertive hops, roasted grain, dry mineral, dark fruit, copper character.',
 'meat', 'grilled sausage',
 'Rheinische Bratwurst or Mettwurst with mustard; the beer''s assertive hop bitterness and roasted grain character suit pork sausage with Germanic directness.',
 'complement', 'Assertive hops cut through sausage fat; roasted grain bridges the char; dry mineral finish cleanses the palate.',
 'casual', 'established', 2, true),

(444, 'beer_ale', 'Düsseldorf Altbier Top-Fermented',
 'Caramel malt, assertive hops, roasted grain, dry mineral, dark fruit, copper character.',
 'cheese', 'aged hard ripe',
 'Aged Gouda or Maasdam; the beer''s caramel malt and hop bitterness are natural partners for the sweet-crystalline richness of aged Dutch cheese.',
 'complement', 'Caramel malt in Altbier mirrors the caramel-butterscotch notes of aged Gouda; hop bitterness cuts the cheese''s sweetness.',
 'casual', 'established', 2, true),

-- 445: Lyrarakis Dafni (Crete)
(445, 'wine_still', 'Crete Indigenous White Dafni',
 'Bay laurel, lemon thyme, citrus zest, white floral, saline mineral, dried herb.',
 'fish', 'Mediterranean grilled',
 'Grilled whole sea bream or sea bass with lemon and herbs; the wine''s herbal-saline-citrus character was made for simple Mediterranean fish preparations.',
 'complement', 'Bay laurel and lemon thyme in wine echo the herb stuffing of whole grilled fish; saline mineral mirrors the briny freshness of Mediterranean sea bass.',
 'main', 'classic', 2, true),

(445, 'wine_still', 'Crete Indigenous White Dafni',
 'Bay laurel, lemon thyme, citrus zest, white floral, saline mineral, dried herb.',
 'shellfish', 'octopus squid',
 'Grilled octopus with lemon and olive oil or squid ink pasta; the wine''s saline mineral and citrus-herb notes create a natural Aegean pairing.',
 'complement', 'Saline mineral echoes octopus'' brininess; lemon thyme bridges olive oil dressing; dried herb character mirrors Cretan culinary aromatics.',
 'main', 'established', 2, true),

(445, 'wine_still', 'Crete Indigenous White Dafni',
 'Bay laurel, lemon thyme, citrus zest, white floral, saline mineral, dried herb.',
 'cheese', 'white brine sheep',
 'Graviera Kritis or Cretan Anthotyros; the wine''s saline mineral finds a natural partner in Crete''s own sheep''s milk cheeses.',
 'complement', 'Sense-of-place: Cretan wine and Cretan cheese share the same salty herb-mineral character of the island''s limestone terroir.',
 'cheese', 'established', 2, true),

-- 446: Douloufakis Dafnios Red (Crete)
(446, 'wine_still', 'Crete Indigenous Red Blend Kotsifali-Mandilari',
 'Dark cherry, dried herbs, warm earth, garrigue, cinnamon, savoury mineral.',
 'meat', 'lamb stewed',
 'Stifado (Cretan braised lamb with cinnamon and olives) or kleftiko; the wine''s cinnamon and dried herb character mirrors Cretan slow-cooked lamb.',
 'complement', 'Cinnamon appears in both wine and Cretan stifado spice; dark cherry provides a fruit anchor for the slow-braised lamb; garrigue bridges the herb character.',
 'main', 'classic', 2, true),

(446, 'wine_still', 'Crete Indigenous Red Blend Kotsifali-Mandilari',
 'Dark cherry, dried herbs, warm earth, garrigue, cinnamon, savoury mineral.',
 'meat', 'grilled pork',
 'Souvlaki or grilled pork with tzatziki and flatbread; the wine''s warm, spiced dark cherry character suits Cretan grilled meat with yoghurt accompaniment.',
 'complement', 'Warm spice and dark cherry of the wine bridge the charred pork; garrigue and dried herbs echo the oregano seasoning of Cretan souvlaki.',
 'casual', 'established', 2, true),

(446, 'wine_still', 'Crete Indigenous Red Blend Kotsifali-Mandilari',
 'Dark cherry, dried herbs, warm earth, garrigue, cinnamon, savoury mineral.',
 'cheese', 'aged Graviera hard',
 'Graviera Kritis or Kefalograviera; the wine''s warm earth and savoury mineral make a regional sense-of-place pairing with Crete''s aged sheep''s milk cheese.',
 'complement', 'Cretan wine and Cretan cheese: shared island terroir; cinnamon and warm spice of the wine complement the Graviera''s nutty, slightly sweet depth.',
 'cheese', 'classic', 2, true);

COMMIT;
