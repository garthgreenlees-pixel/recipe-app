BEGIN;
INSERT INTO pairing_intelligence
  (beverage_product_id, food_flavour_profile, food_category, food_description, pairing_type, flavour_logic, meal_context, confidence, authority_tier)
VALUES
-- 175 Opus One 2019
(175,'prime beef, truffle, jus','beef','Dry-aged beef tenderloin with black truffle jus and roasted asparagus','elevate','Opus One''s Margaux-style elegance elevates prime Napa beef; the truffle bridges Bordeaux earthiness with California opulence','main','classic',1),
(175,'rack of lamb, rosemary, Napa','lamb','Colorado rack of lamb with rosemary crust and natural jus','complement','The Cabernet Franc in Opus One bridges to herb-crusted lamb; a Napa Valley luxury dinner classic','main','classic',1),
-- 176 Ridge Monte Bello
(176,'short ribs, cipollini, braised','beef','Santa Cruz braised short ribs with cipollini onions and polenta','complement','Monte Bello''s mountain tannin structure handles slow-braised short ribs; cipollini''s sweetness mirrors the Cabernet fruit','main','classic',1),
(176,'Bay Blue, honeycomb, walnut','cheese','Pt. Reyes Farmstead Bay Blue with honeycomb and candied walnut','complement','Ridge''s California gravity and the local Bay Blue share Sonoma provenance; the blue''s salinity bridges the Cabernet structure','cheese','established',2),
-- 177 Penfolds Grange
(177,'wagyu, native pepper, Barossa','beef','Barossa dry-aged wagyu striploin with native mountain pepper berry','complement','Grange''s Barossa Shiraz icon belongs with Australia''s finest beef; native pepper berry bridges the wine''s powerful spice','main','classic',1),
(177,'aged cheddar, quince, Mount Barker','cheese','Aged clothbound Cheddar from Mount Barker with quince paste','complement','Grange''s complexity and weight matches the sharpness of aged Australian clothbound cheddar; quince bridges the dark fruit','cheese','classic',2),
-- 178 Henschke Hill of Grace
(178,'pork shoulder, crackling, Barossa','pork','Slow-roasted Barossa pork shoulder with crackling and apple sauce','complement','Hill of Grace Shiraz''s depth and warmth suits a whole-roasted pork; crackling provides textural contrast to the silky wine','main','classic',1),
(178,'clothbound cheddar, clothbound, Pyengana','cheese','Aged Pyengana clothbound Cheddar from Tasmania with fig paste','complement','The Hill of Grace''s sophistication pairs with Tasmania''s finest aged clothbound; both represent Australian artisan pinnacle','cheese','established',2),
-- 179 Cloudy Bay Sauvignon Blanc
(179,'mussels, white wine, herbs','shellfish','Green-lipped mussels in white wine, garlic and parsley cream','complement','Marlborough Sauvignon Blanc and New Zealand green-lipped mussels are twin icons; the wine is even used in the broth','fish_course','classic',1),
(179,'oysters, lemon, mignonette','seafood','Bluff oysters on half-shell with lemon and shallot mignonette','cleanse','Cloudy Bay''s bracing acidity cleanses the briny Bluff oyster; a New Zealand national terroir pairing','starter','classic',1),
-- 180 Felton Road Block 3
(180,'lamb rack, herb crust, Central Otago','lamb','Central Otago lamb rack with herb crust and pinot jus','complement','Felton Road and Central Otago lamb grow in the same schist-and-loess landscape; a true terroir pairing','main','classic',1),
(180,'Windsor Blue, honey, New Zealand','cheese','Aged Whitestone Windsor Blue with manuka honey and crackers','complement','The silky Block 3 tannins bridge the bold blue; manuka honey softens the cheese''s sharpness and mirrors the wine''s fruit','cheese','established',2),
-- 181 Catena Zapata Adrianna Malbec
(181,'asado, chimichurri, Mendoza','beef','Mendoza asado beef short ribs with chimichurri and Malbec reduction','complement','The Adrianna vineyard''s extreme altitude and the Mendoza asado tradition belong together; chimichurri bridges the herbal notes','main','classic',1),
(181,'harvest dinner, Luján de Cuyo, celebration','multi-course','Luján de Cuyo harvest dinner with regional wine and food pairing','elevate','The Fortuna Terrae is Catena''s showcase wine; it deserves the stage of a formal harvest dinner in the vineyard','celebration','classic',1),
-- 182 Sadie Columella
(182,'Karoo lamb, Cape spice, slow-roasted','lamb','Karoo lamb slow-roasted with Cape Malay spice and apricot jam glaze','complement','Columella''s Swartland warmth and the Karoo lamb share a wild, dusty South African terroir; spice mirrors the Grenache component','main','classic',1),
(182,'Boerenkaas, apricot, aged gouda','cheese','Aged Boerenkaas gouda with dried apricot and almond','complement','The Swartland red''s structure bridges aged Dutch-style Boerenkaas; apricot echoes the wine''s warm dried fruit notes','cheese','established',2);
COMMIT;
