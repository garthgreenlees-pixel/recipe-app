BEGIN;
INSERT INTO pairing_intelligence (beverage_product_id, food_flavour_profile, food_category, food_description, pairing_type, flavour_logic, meal_context, confidence, authority_tier) VALUES

-- 557 Mac Forbes Woori Yallock Pinot Noir (Yarra Valley) — needs 6
(557,'savoury-umami','poultry','Roasted duck breast with Szechuan pepper and cherry jus','complement','Yarra Pinot lifts duck fat with bright acidity and silky tannins','main','classic',1),
(557,'earthy-umami','vegetable','Wild mushroom risotto with aged Parmesan','complement','Earthy Pinot harmonises with forest mushroom depth','main','classic',1),
(557,'fatty-savoury','pork','Slow-roasted pork belly with apple jus','complement','Bright red fruit cuts pork fat; soft tannins complement crackling','main','established',2),
(557,'marine-delicate','fish','Pan-seared Atlantic salmon with dill crème fraîche','complement','Silky Pinot texture mirrors salmon''s richness without overpowering','main','established',2),
(557,'earthy-creamy','starter','Chicken liver parfait with brioche toast','complement','Iron-rich parfait echoes Pinot''s dark fruit and forest floor notes','starter','established',2),
(557,'tangy-earthy','vegetable','Beetroot and goat cheese salad with candied walnuts','bridge','Earthy beetroot and tart cheese bridge wine''s red fruit and mineral spine','starter','suggested',2),

-- 558 Mac Forbes Chardonnay (Yarra Valley) — needs 6
(558,'delicate-marine','shellfish','Steamed Queensland mud crab with finger lime butter','complement','Precise Yarra Chardonnay mirrors crab sweetness with bright mineral finish','main','classic',1),
(558,'delicate-marine','fish','Pan-seared snapper with lemon beurre blanc','complement','Citrus and white stone fruit in wine echo beurre blanc acidity','main','classic',1),
(558,'mineral-creamy','vegetable','Roasted cauliflower with aged Gruyère gratin','complement','Nutty Chardonnay oak integrates with caramelised cauliflower','main','established',2),
(558,'herbaceous-delicate','vegetable','White asparagus with hollandaise and mimosa','complement','Mineral Chardonnay acidity cuts hollandaise richness elegantly','starter','established',2),
(558,'fatty-delicate','offal','Pan-fried veal sweetbreads with capers and brown butter','complement','Brioche-like mid-palate Chardonnay complements sweetbread richness','main','established',2),
(558,'creamy-mineral','egg','Soft-boiled egg with shaved black truffle on sourdough','bridge','Truffle and egg yolk amplify Chardonnay''s creamy texture and oak','amuse','suggested',2),

-- 559 De Bortoli Lusatia Park Vineyard Pinot Noir (Yarra Valley) — needs 6
(559,'fatty-savoury','poultry','Duck confit with puy lentils and Dijon mustard','complement','Rich Yarra Pinot tannins balance duck confit fat; red fruit lifts lentils','main','classic',1),
(559,'savoury-herbal','red_meat','Herb-crusted rack of lamb with jus','complement','Finesse tannins complement lamb without overpowering its delicacy','main','classic',1),
(559,'marine-fatty','fish','Pan-seared Atlantic salmon with pinot noir reduction','complement','Salmon fat matches Pinot texture; red fruit reduction ties the dish','main','established',2),
(559,'earthy-savoury','legume','Mushroom and Puy lentil ragù with herbs','complement','Earthy lentils and mushroom echo wine''s forest floor complexity','main','established',2),
(559,'savoury-smoky','charcuterie','Game bird terrine with pickled plum and brioche','complement','Spiced game terrine finds a natural partner in complex Pinot Noir','starter','established',2),
(559,'nutty-savoury','cheese','Aged Comté with walnut bread and quince paste','complement','Hazelnut notes in Comté mirror the wine''s oak-influenced complexity','cheese','established',2),

-- 560 Heitz Martha''s Vineyard Cabernet Sauvignon (Napa) — needs 6
(560,'savoury-rich','red_meat','Dry-aged prime rib with roasted marrow bone and jus','complement','Cedar and eucalyptus Cab lifts beefy umami; structured tannins meld with fat','main','classic',1),
(560,'savoury-herbal','red_meat','Herb-roasted standing rib roast with Yorkshire pudding','complement','Classic Napa Cab tannins integrate with slow-rendered rib fat and herbaceous crust','main','classic',1),
(560,'savoury-herbal','red_meat','Slow-roasted leg of lamb with garlic and rosemary','complement','Eucalyptus and cedar in wine mirrors herbaceous lamb seasoning','main','classic',1),
(560,'earthy-umami','vegetable','Wild mushroom ragù with hand-rolled pappardelle','complement','Deep umami of mushroom ragù aligns with wine''s earthy, complex tannins','main','established',2),
(560,'savoury-rich','game','Pan-seared venison medallions with juniper berry jus','complement','Gamey venison finds balance in wine''s structured tannins and dark fruit','main','established',2),
(560,'sharp-savoury','cheese','Five-year aged sharp cheddar with walnuts','complement','Calcium and protein in aged cheddar bind tannins; walnut echoes cedar note','cheese','established',2),

-- 561 Stag''s Leap CASK 23 Cabernet Sauvignon — needs 6
(561,'lean-savoury','red_meat','Filet mignon with truffle-infused demi-glace','complement','Iron-tannin bond with beef protein; truffle echoes wine''s earthy mid-palate','main','classic',1),
(561,'rich-savoury','red_meat','Dry-aged prime ribeye with bone marrow butter','complement','Classic CASK 23 tannin structure meets prime ribeye fat and mineral beef flavour','main','classic',1),
(561,'rich-fatty','red_meat','Braised short rib with celery root purée','complement','Slow-rendered collagen softens wine tannins; fruit concentration mirrors sauce','main','classic',1),
(561,'herbal-savoury','red_meat','Herb-grilled lamb chops with mint chimichurri','complement','Napa Cab cassis and herbaceous notes align with grilled lamb and fresh herbs','main','classic',1),
(561,'fatty-rich','starter','Roasted bone marrow with sourdough and parsley salad','complement','Marrow fat protein softens big tannins; parsley provides herbal lift','starter','established',2),
(561,'sharp-umami','cheese','Aged Parmigiano Reggiano with balsamic reduction','bridge','Crystalline umami notes in Parmesan bridge wine''s mineral backbone','cheese','established',2),

-- 562 Stag''s Leap S.L.V. Estate Cabernet Sauvignon — needs 6
(562,'rich-savoury','veal','Veal osso buco Milanese with gremolata','complement','Elegant SLV Cab complements tender veal collagen; gremolata provides citrus lift','main','classic',1),
(562,'lean-savoury','red_meat','Beef tenderloin with sauce périgueux','complement','Structured tannins bind lean tenderloin; black truffle deepens wine''s complexity','main','classic',1),
(562,'herbal-savoury','red_meat','Rack of lamb with herb crust and red wine jus','complement','Polished Cabernet tannins precisely match lamb protein and herbaceous crust','main','classic',1),
(562,'smoky-savoury','poultry','Smoked duck breast with cherry reduction','complement','Smoky duck fat meets wine''s dark cherry and pencil shaving character','main','established',2),
(562,'earthy-rich','pasta','Porcini mushroom risotto with aged Parmigiano','complement','Deep forest mushroom base aligns with wine''s earthy, well-structured tannins','main','established',2),
(562,'nutty-savoury','cheese','Aged Gruyère with crusty baguette','complement','Caramelised milk solids in aged Gruyère soften tannins and complement oak','cheese','established',2),

-- 563 Caymus Special Selection Cabernet Sauvignon — needs 6
(563,'rich-fatty','red_meat','Wagyu strip loin A4 with wasabi and soy','complement','Dense Wagyu fat coats the palate; big Cab fruit and oak structure cut through','main','classic',1),
(563,'rich-savoury','red_meat','Slow-braised beef brisket with bourbon glaze','complement','Jammy Napa fruit echoes bourbon glaze; generous tannins integrate with collagen','main','classic',1),
(563,'smoky-savoury','pork','Smoked pulled pork with apple-bourbon BBQ sauce','complement','Full-bodied fruit and vanilla oak harmonise with smoky pork and sweet sauce','main','established',2),
(563,'herbal-savoury','red_meat','Slow-roasted lamb shoulder with merguez spices','complement','Generous Cabernet fruit lifts spiced lamb; structured tannins balance fat','main','classic',1),
(563,'fatty-savoury','casual','Blue cheese smash burger with caramelised onions','complement','Bold Napa tannins cut through cheese and fat; dark fruit lifts caramelised onion','casual','established',2),
(563,'bitter-sweet','dessert','Dark chocolate and sea salt ganache tart','contrast','Fruit-forward Cab contrasts bittersweet chocolate; sea salt bridges the two','dessert','adventurous',3),

-- 564 Caymus Napa Valley Cabernet Sauvignon — needs 6
(564,'savoury-rich','red_meat','Grilled bone-in ribeye with herb butter','complement','Classic Napa Cab tannins bind ribeye protein and fat; dark fruit echoes char','main','classic',1),
(564,'smoky-savoury','red_meat','BBQ beef back ribs with tangy sauce','complement','Jammy fruit and oak vanilla complements smoky beef and caramelised sauce','main','established',2),
(564,'savoury-earthy','pork','Mushroom-stuffed pork tenderloin with pan sauce','complement','Rich fruit profile softens pork tenderloin; mushroom stuffing adds earthy depth','main','established',2),
(564,'spiced-savoury','red_meat','Lamb kofta with tzatziki and flatbread','complement','Ripe Cabernet fruit balances spiced lamb; soft tannins suit kofta''s lean texture','main','established',2),
(564,'sharp-fatty','casual','Cheddar-topped beef burger with sharp pickles','complement','Plush Napa tannins handle cheddar fat; pickle acidity mirrors Cabernet freshness','casual','established',2),
(564,'sharp-savoury','cheese','Aged Manchego with membrillo paste','complement','Lanolin-rich Manchego and quince paste echo wine''s dried fruit and oak spice','cheese','established',2),

-- 565 Williams Selyem Allen Vineyard Pinot Noir (Russian River) — needs 6
(565,'marine-fatty','fish','Roasted king salmon with pinot reduction','complement','Silky Russian River Pinot matches salmon''s fattiness; red fruit reduction ties dish','main','classic',1),
(565,'fatty-savoury','poultry','Duck with orange and bitter marmalade sauce','complement','Complex Pinot fruit harmonises with duck fat; bittersweet orange lifts the wine','main','classic',1),
(565,'earthy-tangy','vegetable','Mushroom and fresh goat cheese tart','complement','Earthiness of mushroom and tang of goat cheese align with Pinot''s savouriness','starter','established',2),
(565,'fruity-savoury','pork','Pork tenderloin with Bing cherry sauce','complement','Cherry-rich Pinot mirrors the fruit sauce; delicate tannins suit tender pork','main','established',2),
(565,'earthy-sweet','vegetable','Roasted beetroot and walnut salad with feta','bridge','Earthy beet and walnut echo wine''s forest floor and spice notes','starter','established',2),
(565,'pungent-rich','cheese','Époisses washed-rind cheese with crusty bread','complement','Pungent, creamy Époisses is softened by complex, generous Pinot Noir fruit','cheese','established',2),

-- 566 Nigl Privat Grüner Veltliner (Kremstal) — needs 6
(566,'crispy-savoury','veal','Wiener Schnitzel with cranberry and lemon wedge','complement','Top Austrian GV acidity cuts fried veal crust; peppery finish amplifies lemon','main','classic',1),
(566,'herbaceous-delicate','vegetable','White asparagus with brown butter and Mimosa','complement','Mineral GV spine cuts hollandaise; peppery character matches asparagus earth','main','classic',1),
(566,'sweet-delicate','shellfish','Steamed whole lobster with drawn butter','complement','Precise mineral acidity balances lobster sweetness and butter richness','main','classic',1),
(566,'delicate-mineral','fish','Pan-fried pike-perch with dill and lemon','complement','Austrian river fish is a classic GV partner; fresh herbs echo wine''s herbal note','main','established',2),
(566,'tangy-fresh','vegetable','Goat cheese and herb salad with citrus dressing','complement','Citrus and peppery GV note harmonises with fresh goat cheese tang','starter','established',2),
(566,'smoky-fatty','fish','House-cured salmon blini with crème fraîche and chive','complement','Smoke and fat of cured salmon complement GV''s freshness and mineral backbone','starter','established',2),

-- 567 Nigl Kremstal Grüner Veltliner — needs 5
(567,'delicate-mineral','fish','Grilled brook trout with herbs and lemon butter','complement','Clean mineral GV acidity lifts freshwater trout and amplifies herb flavour','main','classic',1),
(567,'herbaceous-earthy','vegetable','Rustic vegetable tart with gruyère and thyme','complement','Herbal GV character mirrors thyme and earthy vegetable filling','main','established',2),
(567,'crispy-savoury','poultry','Chicken schnitzel with radish and cucumber salad','complement','Zesty GV cuts fried coating; peppery note refreshes the palate','main','established',2),
(567,'fresh-crisp','vegetable','Cucumber, dill and crème fraîche salad','complement','Refreshing GV vegetal note pairs naturally with dill and cool cucumber','starter','established',2),
(567,'tangy-fresh','cheese','Fresh chèvre with herbs and olive oil','complement','Lactic tang of young goat cheese mirrors GV''s bright acidity and mineral finish','cheese','established',2),

-- 568 Salomon Steiner Hund Riesling (Kremstal) — needs 6
(568,'delicate-mineral','fish','Pike-perch with brown butter and capers','complement','Mineral Kremstal Riesling pairs classically with central European river fish','main','classic',1),
(568,'sweet-mineral','shellfish','Freshwater crayfish bisque with tarragon cream','complement','Wine''s mineral slate notes and stone fruit lift shellfish bisque sweetness','starter','established',2),
(568,'fatty-savoury','charcuterie','Pork rillettes with cornichons and sourdough','complement','Petrol-tinged dry Riesling cuts pork fat; cornichon acidity echoes wine''s bite','starter','established',2),
(568,'fatty-spiced','pork','Five-spice pork belly with pickled ginger','complement','Dry Riesling acidity cuts spiced pork fat; stone fruit mirrors pickling brine','main','established',2),
(568,'sweet-sharp','cheese','Aged Gouda with mustard and rye bread','complement','Caramel notes in aged Gouda complement Riesling''s petrol and stone fruit character','cheese','established',2),
(568,'sweet-buttery','dessert','Classic apple strudel with vanilla cream','complement','Apple and pastry in strudel mirror Riesling''s ripe stone fruit and mineral finish','dessert','suggested',3),

-- 569 Quinta da Pellada Primus Dão Red — needs 6
(569,'fatty-crispy','pork','Roast suckling pig with crackling and lemon','complement','Tangy Dão acidity cuts pork fat; Touriga Nacional fruit lifts crispy crackling','main','classic',1),
(569,'gamey-rich','game','Braised wild boar with chestnuts and rosemary','complement','Wild boar intensity matches Dão''s tannin structure and dark herbal character','main','classic',1),
(569,'savoury-rich','fish','Bacalhau com natas gratinado (salt cod gratin)','complement','Bold Dão red fruit and tannin structure complement the richness of salt cod cream','main','established',2),
(569,'savoury-rich','poultry','Slow-roasted duck with rice (arroz de pato)','complement','Complex Dão fruit mirrors duck richness; tannins balance rendered fat','main','established',2),
(569,'sharp-rich','cheese','Serra da Estrela sheep''s milk cheese (raw)','complement','Pungent, buttery Serra cheese is tamed by structured Dão tannins and fruit','cheese','established',2),
(569,'herbal-savoury','red_meat','Lamb stew with coriander and tomato','complement','Herbal lamb stew aligns with Dão''s dark-fruited, mineral backbone','main','established',2),

-- 570 Quinta da Pellada Dão Red — needs 6
(570,'herbal-savoury','red_meat','Roast lamb with rosemary, garlic and roasted potatoes','complement','Herbaceous Dão red pairs classically with herb-roasted lamb','main','classic',1),
(570,'savoury-earthy','pork','Pork loin with chestnut stuffing and port sauce','complement','Dão dark fruit and earthy tannins complement sweet chestnut and port sauce','main','established',2),
(570,'spiced-savoury','poultry','Piri-piri roast chicken with lemon','complement','Bright Dão acidity cuts spiced chicken; fruit mirrors chilli heat','main','established',2),
(570,'smoky-rich','vegetable','Caldo verde soup with smoked chouriço','complement','Earthy kale and smoky sausage are lifted by wine''s dark fruit and mineral spine','starter','established',2),
(570,'earthy-umami','pasta','Wild mushroom and thyme risotto with Dão wine jus','complement','Forest mushroom and herb echo wine''s earthy, complex character','main','established',2),
(570,'sharp-savoury','cheese','Aged sheep''s milk cheese with quince paste','complement','Lanolin and caramel in aged sheep cheese complement Dão red fruit and spice','cheese','established',2),

-- 571 Niepoort Dialogo Dão Red — needs 6
(571,'smoky-savoury','fish','Grilled whole sardines with parsley and lemon','complement','Robust Dão fruit handles the oiliness of fresh sardines with aplomb','main','established',2),
(571,'savoury-briny','pork','Pork and clams Alentejana style','complement','Classic Portuguese pairing; Dão acidity bridges pork fat and briny clams','main','classic',1),
(571,'savoury-herbal','pastry','Galician-style empanadas with tuna and peppers','complement','Accessible Dão fruit and acidity complement savoury pastry and tuna filling','starter','established',2),
(571,'creamy-savoury','snack','Mushroom croquettes with aioli','complement','Crispy croquette and earthy mushroom echo wine''s dark fruit and mineral note','starter','established',2),
(571,'savoury-herbal','poultry','Roast chicken with garlic and lemon','complement','Everyday Dão red is a natural partner to roast chicken — a classic match','main','established',2),
(571,'sharp-savoury','cheese','Semi-cured sheep''s cheese with honey','complement','Mild sheep''s cheese pairs effortlessly with this approachable Dão red','cheese','established',2),

-- 573 Jack Daniel''s Old No. 7 Tennessee Whiskey — needs 1
(573,'sweet-nutty','dessert','Pecan pralines with bourbon caramel sauce','complement','Tennessee charcoal-filtered sweetness mirrors caramelised pecan and bourbon notes','dessert','classic',1),

-- 574 George Dickel No. 12 Superior Grade Tennessee Whisky — needs 1
(574,'smoky-savoury','pork','Pulled pork BBQ sandwich with tangy coleslaw','complement','Mellow Tennessee character and vanilla oak harmonise with smoky pulled pork','casual','established',2),

-- 575 Antinori Badia a Passignano CCGS — needs 6
(575,'savoury-charred','red_meat','Bistecca alla Fiorentina with sea salt and olive oil','complement','Quintessential Tuscan pairing: structured Sangiovese tannins integrate with T-bone','main','classic',1),
(575,'gamey-rich','game','Wild boar ragù with hand-rolled pappardelle','complement','Sangiovese acidity cuts wild boar fat; cherry fruit mirrors rich tomato ragù','main','classic',1),
(575,'sharp-savoury','cheese','Pecorino stagionato with chestnut honey','complement','Aged sheep cheese fat and protein bind Sangiovese tannins gracefully','cheese','classic',1),
(575,'earthy-umami','pasta','Porcini mushroom risotto with Parmigiano Reggiano','complement','Forest mushroom earthiness mirrors Gran Selezione depth and mineral complexity','main','established',2),
(575,'fatty-savoury','poultry','Slow-roasted duck with Chianti reduction and olives','complement','Duck fat is balanced by Sangiovese acidity; olive bitterness lifts cherry fruit','main','established',2),
(575,'herbal-savoury','red_meat','Grilled lamb chops with olive tapenade and herbs','complement','Herbal lamb and Sangiovese are a natural partnership reinforced by olive bitterness','main','established',2),

-- 576 Fontodi CCGS Vigna del Sorbo — needs 6
(576,'savoury-charred','red_meat','Florentine T-bone with Tuscan olive oil','complement','Biodynamic Sangiovese tannin structure aligns precisely with T-bone mineral beef','main','classic',1),
(576,'gamey-rich','game','Slow-roasted cinghiale (wild boar) with polenta','complement','Wild boar intensity is matched by concentrated Fontodi fruit and firm tannins','main','classic',1),
(576,'sharp-savoury','cheese','Aged Pecorino Toscano with truffle honey','complement','Crystalline aged sheep cheese softens tannins and echoes wine''s earthy spice','cheese','classic',1),
(576,'earthy-umami','pasta','Black truffle pasta with Parmigiano butter sauce','complement','Truffle earthiness deepens the wine''s Sangiovese complexity and mineral edge','main','established',2),
(576,'rich-savoury','red_meat','Braised oxtail (coda alla vaccinara) with pine nuts','complement','Long-cooked collagen rounds tannin structure; sweet-sour sauce mirrors Sangiovese','main','established',2),
(576,'gamey-herbal','game','Venison haunch with juniper berry and red wine jus','complement','Game and Sangiovese are a classic combination; dark fruit mirrors reduction sauce','main','established',2),

-- 577 Fontodi Chianti Classico — needs 5
(577,'savoury-herbal','pasta','Classic pasta Bolognese with Parmigiano','complement','Sangiovese acidity cuts meat sauce richness; cherry fruit mirrors tomato sweetness','main','classic',1),
(577,'savoury-charred','pizza','Margherita pizza with fresh basil and fior di latte','complement','Tomato and mozzarella echo Sangiovese''s cherry and herb profile','main','classic',1),
(577,'herbal-savoury','red_meat','Grilled lamb chops with salsa verde','complement','Fresh herb salsa verde and grilled lamb harmonise with vibrant Chianti acidity','main','established',2),
(577,'salty-savoury','charcuterie','Prosciutto di Parma with melon','contrast','Sweet melon and silky prosciutto contrast with refreshing Sangiovese acidity','starter','established',2),
(577,'sharp-savoury','cheese','Parmigiano Reggiano 24-month with crusty bread','complement','Umami-rich Parmesan binds Sangiovese tannins and amplifies cherry fruit','cheese','established',2),

-- 578 Clos Mogador Priorat — needs 6
(578,'spiced-savoury','red_meat','Slow-cooked lamb tagine with preserved lemon','complement','Grenache-led Priorat dark fruit harmonises with spiced braised lamb','main','classic',1),
(578,'fatty-crispy','pork','Roasted suckling pig with roasted garlic','complement','Priorat mineral intensity and tannin structure handle suckling pig richness','main','established',2),
(578,'fatty-rich','poultry','Duck confit with Puy lentils and Dijon','complement','Generous Priorat fruit and structured tannins balance duck confit fat','main','established',2),
(578,'bitter-sweet','dessert','Dark chocolate and raspberry tart with sea salt','contrast','Bold Priorat fruit and acidity contrast sweet-bitter dark chocolate and tart berries','dessert','adventurous',3),
(578,'smoky-briny','seafood','Chargrilled octopus with paprika oil and pickled peppers','complement','Llicorella mineral backbone echoes charred octopus and smoky paprika oil','main','established',2),
(578,'sharp-savoury','cheese','Aged Manchego with membrillo and almonds','complement','Manchego lanolin and quince paste echo wine''s dark fruit and mineral structure','cheese','established',2),

-- 589 Tariquet Folle Blanche Armagnac — needs 1
(589,'sweet-fruity','dessert','Poached pear tart with almond frangipane','complement','Light floral Folle Blanche single-grape armagnac lifts poached pear sweetness','dessert','suggested',3);

COMMIT;
