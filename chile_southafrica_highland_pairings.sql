BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 406: Clos Apalta (Colchagua Carmenère blend)
(406, 'wine_still', 'Colchagua Carmenère Blend',
 'Biodynamic; black cherry, tobacco, mocha and graphite from 80-year-old vines. 15-20 year horizon.',
 'meat', 'beef slow-braised',
 'Slow-braised beef short rib with mocha-chile mole; the wine''s tobacco-mocha depth is amplified by the dark, complex mole sauce.',
 'complement', 'Mocha note in both wine and mole creates depth; tobacco and chocolate in Carmenère align with slow-braised umami.',
 'main', 'classic', 1, true),

(406, 'wine_still', 'Colchagua Carmenère Blend',
 'Biodynamic; black cherry, tobacco, mocha and graphite from 80-year-old vines. 15-20 year horizon.',
 'meat', 'lamb herb-crusted',
 'Herb-crusted rack of lamb with black cherry reduction; the wine''s black cherry and cedar elegance pairs naturally with the classic lamb preparation.',
 'complement', 'Black cherry reduction echoes the wine''s primary fruit; herbs bridge the Carmenère''s tobacco register.',
 'main', 'established', 1, true),

(406, 'wine_still', 'Colchagua Carmenère Blend',
 'Biodynamic; black cherry, tobacco, mocha and graphite from 80-year-old vines. 15-20 year horizon.',
 'cheese', 'aged hard umami',
 'Aged Manchego or Comté; the wine''s graphite tannin and tobacco complexity find a complementary match in crystalline aged hard cheese.',
 'complement', 'Aged cheese protein and fat soften graphite tannin; umami depth mirrors tobacco complexity in the wine.',
 'cheese', 'established', 1, true),

(406, 'wine_still', 'Colchagua Carmenère Blend',
 'Biodynamic; black cherry, tobacco, mocha and graphite from 80-year-old vines. 15-20 year horizon.',
 'meat', 'duck confit',
 'Duck confit with dark cherry sauce and roasted root vegetables; the Carmenère''s dark fruit and smoky depth mirrors duck''s richness perfectly.',
 'complement', 'Carmenère''s dark cherry and earthy tobacco notes are ideal for duck''s fat richness; smoky graphite echoes the confit preparation.',
 'main', 'established', 1, true),

-- 407: Luis Felipe Edwards Gran Reserva Carmenère
(407, 'wine_still', 'Colchagua Gran Reserva Carmenère',
 'Ripe plum, cocoa, green pepper; medium tannin, approachable Colchagua Carmenère.',
 'meat', 'beef grilled',
 'Grilled sirloin with chimichurri; the wine''s ripe plum and vanilla warmth complements the char and herb of South American grilled beef.',
 'complement', 'Ripe fruit and vanilla in Carmenère balance the bitterness of char; chimichurri herb bridges the green pepper note in the wine.',
 'main', 'classic', 2, true),

(407, 'wine_still', 'Colchagua Gran Reserva Carmenère',
 'Ripe plum, cocoa, green pepper; medium tannin, approachable Colchagua Carmenère.',
 'meat', 'lamb meatballs',
 'Slow-cooked lamb meatballs in tomato-cumin sauce; the wine''s approachable tannin and cocoa warmth pair well with spiced lamb in a rustic sauce.',
 'complement', 'Cocoa note in wine mirrors tomato-cumin sauce''s earthy depth; medium tannin integrates with slow-cooked lamb protein.',
 'main', 'established', 2, true),

(407, 'wine_still', 'Colchagua Gran Reserva Carmenère',
 'Ripe plum, cocoa, green pepper; medium tannin, approachable Colchagua Carmenère.',
 'charcuterie', 'cured chorizo',
 'Ibérico chorizo or Spanish-style salami; the wine''s spiced-plum and green-pepper character harmonises naturally with paprika-cured charcuterie.',
 'complement', 'Paprika and smoked spice in chorizo echo the wine''s pepper and fruit warmth; shared Latin American-Iberian registers create cultural coherence.',
 'starter', 'established', 2, true),

-- 408: Almaviva (Maipo Bordeaux blend)
(408, 'wine_still', 'Maipo Bordeaux Blend',
 'Cassis, cedar, graphite, tobacco; Rothschild-Concha y Toro; 15+ year ageworthy.',
 'meat', 'lamb roasted',
 'Roasted rack of lamb with rosemary and garlic; the classic Bordeaux-style structure and cassis of Almaviva find their natural counterpart in herb-roasted lamb.',
 'complement', 'Cassis and cedar of Almaviva are the textbook Bordeaux partner for herb-roasted lamb; graphite tannin integrates with roasted protein.',
 'main', 'classic', 1, true),

(408, 'wine_still', 'Maipo Bordeaux Blend',
 'Cassis, cedar, graphite, tobacco; Rothschild-Concha y Toro; 15+ year ageworthy.',
 'meat', 'beef wellington',
 'Beef Wellington or dry-aged sirloin; the wine''s graphite mineral and tannic authority demand quality aged beef at the table.',
 'complement', 'Graphite and cedar tannin integrate perfectly with beef''s fat and protein; the wine''s Médoc pedigree dictates classic pairings.',
 'main', 'established', 1, true),

(408, 'wine_still', 'Maipo Bordeaux Blend',
 'Cassis, cedar, graphite, tobacco; Rothschild-Concha y Toro; 15+ year ageworthy.',
 'cheese', 'aged comté hard',
 'Aged Comté or vintage Gruyère; cedar and mineral in Almaviva find the right match in mountain cheese with crystalline depth.',
 'complement', 'Cedar and mineral in wine echo the aged mountain cheese''s terroir complexity; tannic structure balanced by protein and fat.',
 'cheese', 'established', 1, true),

(408, 'wine_still', 'Maipo Bordeaux Blend',
 'Cassis, cedar, graphite, tobacco; Rothschild-Concha y Toro; 15+ year ageworthy.',
 'charcuterie', 'pâté en croûte',
 'Pâté en croûte or terrine with pickled cornichons; the wine''s structured Bordeaux tannin creates the classic Médoc-terrine partnership.',
 'complement', 'Classic bistro pairing: structured tannin binds with pâté fat and liver richness while cassis brightens the plate.',
 'starter', 'established', 1, true),

-- 409: Don Melchor (Maipo Cabernet Sauvignon)
(409, 'wine_still', 'Maipo Single-Vineyard Cabernet Sauvignon',
 'Blackcurrant, pencil shaving, mint, cedar, fine mineral tannin; Puente Alto, Andes foothills.',
 'meat', 'beef dry-aged',
 'Dry-aged côte de boeuf or bone-in ribeye; the wine''s mineral tannin authority and blackcurrant depth demand simplicity and quality at the plate.',
 'complement', 'Pencil-shaving tannin integrates with beef fat and protein; mineral Andean character enhanced by the Maillard crust of dry-aged beef.',
 'main', 'classic', 1, true),

(409, 'wine_still', 'Maipo Single-Vineyard Cabernet Sauvignon',
 'Blackcurrant, pencil shaving, mint, cedar, fine mineral tannin; Puente Alto, Andes foothills.',
 'meat', 'lamb herb',
 'Rack of lamb with mint sauce and rosemary-roasted vegetables; the wine''s mint note finds a deliberate echo in the classic accompaniment.',
 'complement', 'Mint in both wine and sauce creates direct flavour alignment; cedar structure mirrors the herb crust''s savoury depth.',
 'main', 'established', 1, true),

(409, 'wine_still', 'Maipo Single-Vineyard Cabernet Sauvignon',
 'Blackcurrant, pencil shaving, mint, cedar, fine mineral tannin; Puente Alto, Andes foothills.',
 'cheese', 'aged cheddar',
 'Aged Cheddar (3 year+) or aged Gouda; the wine''s cedary tannin and blackcurrant depth find their match in crystalline aged hard cheese.',
 'complement', 'Aged cheddar crystalline protein softens Cabernet tannin; blackcurrant complements the cheese''s complex lactic depth.',
 'cheese', 'established', 1, true),

-- 410: Kanonkop Paul Sauer (Stellenbosch Bordeaux blend)
(410, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, cedar, dried tobacco, dark plum, graphite; Cape First Growth ageworthy.',
 'meat', 'lamb roasted',
 'Slow-roasted leg of lamb with rosemary, garlic and Cape Malay spices; the wine''s cedar and cassis depth finds its most resonant partner in herb-spiced lamb.',
 'complement', 'Cassis and cedar are the Bordeaux-style natural partners for roasted lamb; Cape Malay spice bridges tobacco register in the wine.',
 'main', 'classic', 1, true),

(410, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, cedar, dried tobacco, dark plum, graphite; Cape First Growth ageworthy.',
 'meat', 'beef aged',
 'Dry-aged sirloin or beef fillet with bone marrow; the wine''s graphite tannin authority and tobacco depth require quality aged beef.',
 'complement', 'Dried tobacco complexity in wine aligns with dry-aged beef''s Maillard character; graphite tannin integrates with beef fat.',
 'main', 'established', 1, true),

(410, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, cedar, dried tobacco, dark plum, graphite; Cape First Growth ageworthy.',
 'cheese', 'aged hard cave',
 'Cave-aged Gruyère or aged Pecorino; the wine''s tobacco and graphite complexity benefits from the crystalline protein of aged hard cheese.',
 'complement', 'Cave-aged cheese''s mineral complexity echoes the wine''s graphite mineral; tobacco finds a savoury match in aged Pecorino''s nutty depth.',
 'cheese', 'established', 1, true),

(410, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, cedar, dried tobacco, dark plum, graphite; Cape First Growth ageworthy.',
 'charcuterie', 'biltong cured',
 'South African biltong or dry-cured bresaola; the wine''s tobacco and dark-plum character finds a cultural and flavour match in air-dried meat.',
 'complement', 'Tobacco and dried fruit in wine echo the spiced, cured character of biltong; shared South African heritage creates a sense-of-place pairing.',
 'starter', 'adventurous', 1, true),

-- 411: Meerlust Rubicon (Stellenbosch Bordeaux blend)
(411, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, violet, cedar, dark cherry, tobacco leaf, mineral; 20+ year ageworthy.',
 'meat', 'lamb slow',
 'Slow-roasted lamb shoulder with herbs and red wine reduction; the wine''s violet and cassis elegance is at its finest with slow-cooked lamb.',
 'complement', 'Violet florality in Rubicon lifts herb-roasted lamb; cassis and cedar are the natural Bordeaux counterpart.',
 'main', 'classic', 1, true),

(411, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, violet, cedar, dark cherry, tobacco leaf, mineral; 20+ year ageworthy.',
 'meat', 'venison',
 'Braised Springbok or venison with dark berry reduction; the wine''s tobacco leaf and mineral depth are ideal for lean, gamey Cape venison.',
 'complement', 'Tobacco leaf in wine matches the gamey mineral character of venison; dark cherry reduction echoes the wine''s cherry fruit.',
 'main', 'adventurous', 1, true),

(411, 'wine_still', 'Stellenbosch Bordeaux Blend',
 'Cassis, violet, cedar, dark cherry, tobacco leaf, mineral; 20+ year ageworthy.',
 'cheese', 'aged semi-hard',
 'Aged Gouda (5 year+) or aged Leerdammer; the wine''s violet and cassis elegance finds a gentle match in caramel-crystalline aged Gouda.',
 'complement', 'Aged Gouda''s butterscotch and caramel notes temper the wine''s tobacco tannin; cassis and violet remain prominent.',
 'cheese', 'established', 1, true),

-- 412: Boekenhoutskloof Syrah (Stellenbosch)
(412, 'wine_still', 'Cape Syrah',
 'Violet, smoked meat, white pepper, dark berry, iron, olive; old-vine Cape Rhône-inspired.',
 'meat', 'beef short rib smoked',
 'Smoked beef short rib or brisket; the wine''s smoked meat character finds direct expression in the preparation itself.',
 'complement', 'Smoked meat note in wine echoes the preparation method; iron and dark berry align with rendered beef fat and caramelised crust.',
 'main', 'classic', 1, true),

(412, 'wine_still', 'Cape Syrah',
 'Violet, smoked meat, white pepper, dark berry, iron, olive; old-vine Cape Rhône-inspired.',
 'meat', 'lamb kofta',
 'Lamb kofta with olive tapenade and roasted pepper; the wine''s olive and white pepper character mirrors classic Mediterranean-style lamb preparation.',
 'complement', 'Olive tapenade directly echoes the wine''s olive note; white pepper in the wine bridges the spiced lamb preparation.',
 'main', 'established', 1, true),

(412, 'wine_still', 'Cape Syrah',
 'Violet, smoked meat, white pepper, dark berry, iron, olive; old-vine Cape Rhône-inspired.',
 'cheese', 'washed rind assertive',
 'Époisses or aged Limburger; the wine''s iron and smoked character creates an assertive contrast pairing with pungent washed-rind cheese.',
 'contrast', 'Pungent ferment character of washed-rind cheese contrasts with wine''s smoky mineral clarity; violet florality lifts and softens the cheese.',
 'cheese', 'adventurous', 1, true),

-- 413: Glenmorangie 18 Year Extremely Rare
(413, 'spirits_whiskey', 'Highland Single Malt 18 Year',
 'Peach, mango, orange blossom, walnut, chocolate; ex-bourbon + Oloroso finish.',
 'pastry_dessert', 'orange-chocolate',
 'Chocolate orange tart or orange blossom crème brûlée; the whisky''s orange blossom and chocolate notes find a natural dessert partner.',
 'complement', 'Orange blossom and chocolate in whisky mirror the dessert''s dominant flavours; peach and mango create a tropical-citrus bridge.',
 'dessert', 'classic', 1, true),

(413, 'spirits_whiskey', 'Highland Single Malt 18 Year',
 'Peach, mango, orange blossom, walnut, chocolate; ex-bourbon + Oloroso finish.',
 'cheese', 'blue strong',
 'Stilton or Gorgonzola with honeycomb; the whisky''s tropical fruit and walnut sweetness creates a classic Scotch-cheese pairing.',
 'complement', 'Walnut in whisky aligns with blue cheese''s nutty, earthy depth; fruit-forward character cuts through the pungency; honey bridges both.',
 'cheese', 'classic', 1, true),

(413, 'spirits_whiskey', 'Highland Single Malt 18 Year',
 'Peach, mango, orange blossom, walnut, chocolate; ex-bourbon + Oloroso finish.',
 'chocolate', 'milk chocolate hazelnut',
 'Milk chocolate hazelnut praline or Ferrero Rocher style; walnut and chocolate in the whisky find exact expression in the confection.',
 'complement', 'Walnut-chocolate combination in whisky mirrors hazelnut praline directly; tropical fruit adds a lifting contrast.',
 'digestif', 'established', 1, true),

(413, 'spirits_whiskey', 'Highland Single Malt 18 Year',
 'Peach, mango, orange blossom, walnut, chocolate; ex-bourbon + Oloroso finish.',
 'pastry_dessert', 'peach mango tropical',
 'Mango pavlova or peach tarte Tatin; the whisky''s dominant stone-and-tropical-fruit register finds an elegant dessert partner.',
 'complement', 'Peach and mango in whisky echo directly in the dessert; vanilla from oak structure bridges meringue or pastry cream.',
 'dessert', 'adventurous', 1, true),

-- 414: GlenDronach 18 Year Allardice
(414, 'spirits_whiskey', 'Highland Single Malt Sherry-Matured',
 'Fruit cake, Christmas spice, black cherry, orange peel, mocha, dark chocolate; Oloroso casks.',
 'chocolate', 'dark chocolate cherries',
 'Dark chocolate cherry bonbons or Black Forest torte; the whisky''s black cherry and mocha core find a classical confection partner.',
 'complement', 'Black cherry and mocha appear in both whisky and dessert; dark chocolate amplifies the sherry-cask depth.',
 'digestif', 'classic', 2, true),

(414, 'spirits_whiskey', 'Highland Single Malt Sherry-Matured',
 'Fruit cake, Christmas spice, black cherry, orange peel, mocha, dark chocolate; Oloroso casks.',
 'cheese', 'aged hard stilton',
 'Aged Stilton or aged Roquefort with dried fig; the whisky''s fruit-cake complexity creates the definitive Scotch-Stilton pairing.',
 'complement', 'Fruit cake spice in whisky aligns with blue cheese''s ferment complexity; dried fig bridges cherry note with sweet contrast.',
 'cheese', 'classic', 2, true),

(414, 'spirits_whiskey', 'Highland Single Malt Sherry-Matured',
 'Fruit cake, Christmas spice, black cherry, orange peel, mocha, dark chocolate; Oloroso casks.',
 'pastry_dessert', 'Christmas cake dark fruit',
 'Christmas cake or sticky toffee pudding; the whisky''s fruit-cake aromatic is almost literal in combination with dark fruit baked goods.',
 'complement', 'Fruit cake and Christmas spice in whisky mirror the dessert literally; mocha in whisky bridges the toffee sauce.',
 'dessert', 'established', 2, true),

-- 415: Dalmore 18 Year
(415, 'spirits_whiskey', 'Highland Single Malt Triple-Sherry',
 'Dark chocolate, marmalade, walnut, coffee, vanilla, orange zest; triple sherry casks.',
 'chocolate', 'dark orange chocolate',
 'Chocolate orange truffles or pain d''épices with marmalade; the whisky''s marmalade-dark chocolate character finds exact expression in bitter citrus-chocolate confection.',
 'complement', 'Marmalade and dark chocolate in whisky mirror the confection''s flavour profile precisely; orange zest amplifies bitter-citrus register.',
 'digestif', 'classic', 2, true),

(415, 'spirits_whiskey', 'Highland Single Malt Triple-Sherry',
 'Dark chocolate, marmalade, walnut, coffee, vanilla, orange zest; triple sherry casks.',
 'cheese', 'aged cheddar cloth',
 'Cloth-bound Cheddar (Montgomery''s or Lincolnshire Poacher); the whisky''s walnut and vanilla depth complement the crystalline nuttiness of aged cheddar.',
 'complement', 'Walnut note in whisky aligns with aged cheddar''s nutty crystalline depth; vanilla oak structure softens the cheese''s sharp acidity.',
 'cheese', 'established', 2, true),

(415, 'spirits_whiskey', 'Highland Single Malt Triple-Sherry',
 'Dark chocolate, marmalade, walnut, coffee, vanilla, orange zest; triple sherry casks.',
 'pastry_dessert', 'walnut coffee cake',
 'Walnut and coffee cake or espresso financier; the whisky''s coffee and walnut notes find their exact counterpart in this classic afternoon pairing.',
 'complement', 'Coffee and walnut appear in both whisky and cake creating a unified aromatic whole; vanilla bridges the oak and the bake.',
 'dessert', 'classic', 2, true),

-- 416: Clynelish 14 Year
(416, 'spirits_whiskey', 'Highland Coastal Single Malt',
 'Beeswax, sea salt, lemon, orchard fruit, heather honey, dry mineral; Sutherland coast.',
 'cheese', 'aged hard lactic',
 'Aged Gouda or Aged Cheddar with honey; the whisky''s beeswax and heather honey character creates an exceptional pairing with aged hard cheese.',
 'complement', 'Beeswax note in Clynelish mirrors the natural wax coating and texture of aged Gouda; honey bridges both.',
 'cheese', 'classic', 2, true),

(416, 'spirits_whiskey', 'Highland Coastal Single Malt',
 'Beeswax, sea salt, lemon, orchard fruit, heather honey, dry mineral; Sutherland coast.',
 'shellfish', 'oysters coastal',
 'Oysters on the half shell with lemon and sea salt; the whisky''s coastal minerality and sea salt character create a perfect sense-of-place pairing.',
 'complement', 'Sea salt and coastal mineral in whisky echo the oyster''s brine; lemon in the whisky matches the classic oyster accompaniment.',
 'starter', 'classic', 2, true),

(416, 'spirits_whiskey', 'Highland Coastal Single Malt',
 'Beeswax, sea salt, lemon, orchard fruit, heather honey, dry mineral; Sutherland coast.',
 'fish', 'smoked salmon',
 'Hot-smoked salmon or gravlax with dill and lemon crème fraîche; the whisky''s coastal mineral and citrus character pairs elegantly with cured salmon.',
 'complement', 'Sea salt in whisky echoes salt-cure in salmon; lemon note bridges the crème fraîche; beeswax adds textural richness.',
 'starter', 'established', 2, true),

(416, 'spirits_whiskey', 'Highland Coastal Single Malt',
 'Beeswax, sea salt, lemon, orchard fruit, heather honey, dry mineral; Sutherland coast.',
 'pastry_dessert', 'honey heather',
 'Heather honey shortbread or Scottish tablet; the whisky''s heather honey and wax register finds a direct cultural and flavour mirror in Scottish confection.',
 'complement', 'Heather honey appears in both whisky and confection; beeswax texture of Clynelish aligns with the buttery shortbread mouthfeel.',
 'dessert', 'classic', 2, true);

COMMIT;
