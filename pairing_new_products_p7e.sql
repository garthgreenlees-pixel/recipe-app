BEGIN;
INSERT INTO pairing_intelligence (beverage_product_id, food_flavour_profile, food_category, food_description, pairing_type, flavour_logic, meal_context, confidence, authority_tier) VALUES

-- 590 Benanti Serra della Contessa Etna Rosso — needs 5
(590,'marine-savoury','fish','Grilled tuna steak with caponata and basil oil','complement','Nerello Mascalese acidity and mineral volcanic character match firm tuna texture','main','classic',1),
(590,'earthy-umami','pasta','Wild mushroom pasta with black truffle shavings','complement','Volcanic mineral notes and forest mushroom echo each other through the wine','main','established',2),
(590,'herbal-savoury','red_meat','Slow-roasted lamb with capers and anchovy tapenade','complement','Briny, herbaceous lamb pairing amplifies wine''s Etna minerality and lifted acidity','main','established',2),
(590,'sweet-savoury','vegetable','Caponata bruschetta with pine nuts and raisins','bridge','Sweet-sour aubergine and pine nut caponata bridge wine''s red fruit and mineral spine','starter','established',2),
(590,'sharp-savoury','cheese','Aged Ragusano DOP with crusty sesame bread','complement','Firm Sicilian cow''s cheese echoes the wine''s structure and savoury mineral finish','cheese','established',2),

-- 591 Cornelissen Munjebel Rosso Terre Siciliane — needs 6
(591,'smoky-savoury','fish','Swordfish alla ghiotta with olives and capers','complement','Natural wine minerality mirrors the Tyrrhenian umami of this Sicilian fish classic','main','established',2),
(591,'savoury-briny','pasta','Pasta con le sarde with fennel and pine nuts','complement','Sardine-fennel sauce complexity is matched by volcanic mineral and oxidative note','main','established',2),
(591,'earthy-spiced','legume','Lentil soup with nduja and smoked paprika','complement','Rustic, savoury intensity of nduja and lentil align with natural wine''s depth','main','established',2),
(591,'herbal-earthy','vegetable','Roasted aubergine, pepper and herb tian','complement','Sun-dried vegetable earthiness harmonises with Nerello''s volcanic, textured fruit','main','established',2),
(591,'sharp-savoury','cheese','Pecorino Siciliano with wild honey','complement','Salty, sharp sheep cheese is tamed by the wine''s natural acidity and tannin','cheese','established',2),
(591,'spiced-savoury','red_meat','Charcoal-grilled lamb skewers with cumin and mint yoghurt','complement','Smoky lamb and cumin find a partner in volcanic Etna mineral and lifted red fruit','main','established',2),

-- 592 Passopisciaro Chiappemacine Etna Rosso — needs 6
(592,'delicate-marine','fish','Branzino al cartoccio with lemon and herbs','complement','Single contrada precision mirrors the delicacy of branzino with herbal aromatics','main','established',2),
(592,'rich-savoury','pork','Pork braciole stuffed with hard-boiled egg and pine nuts','complement','Nerello Mascalese structure handles braciole richness; acidity cuts pork fat','main','established',2),
(592,'savoury-earthy','vegetable','Stuffed roasted aubergine with ricotta and tomato','complement','Volcanic earthiness in wine harmonises with aubergine and herbed ricotta','main','established',2),
(592,'savoury-acidic','pasta','Pasta alla Norma with fried aubergine and ricotta salata','complement','Classic Sicilian dish mirrors wine''s acidity and volcanic mineral notes precisely','main','classic',1),
(592,'sharp-savoury','cheese','Ricotta salata with cherry tomato and basil','complement','Briny, chalky ricotta salata echoes wine''s mineral structure and lifted finish','cheese','established',2),
(592,'marine-savoury','fish','Seared tuna carpaccio with caper berries and chilli','complement','Raw tuna''s iron note aligns with Nerello''s dark cherry and volcanic mineral edge','starter','established',2),

-- 593 Benanti Etna Bianco Superiore Pietramarina — needs 6
(593,'sweet-briny','shellfish','Red prawn crudo with citrus, olive oil and sea salt','complement','Volcanic mineral white wine elevates raw prawn sweetness and briny sea character','starter','classic',1),
(593,'briny-umami','pasta','Sea urchin linguine with lemon and chilli','complement','Wine''s Carricante mineral spine amplifies sea urchin ocean depth and salinity','main','established',2),
(593,'tender-savoury','seafood','Chargrilled calamari with salsa verde','complement','Clean mineral acidity and stone fruit note complement smoky tender calamari','main','established',2),
(593,'umami-savoury','fish','Bottarga di muggine shaved over warm pasta','complement','Mineral and oxidative white wine mirrors the concentrated umami of dried mullet roe','amuse','established',2),
(593,'salty-savoury','fish','Fresh anchovies on crostini with olive oil','complement','Volcanic mineral wine cuts salt and oil of fresh anchovies with precision','starter','established',2),
(593,'bitter-fresh','vegetable','Roasted fennel and blood orange salad with almonds','bridge','Anise and citrus in salad bridge the wine''s stone fruit and mineral complexity','starter','established',2),

-- 594 Alpha Estate Hedgehog Vineyard Xinomavro — needs 6
(594,'herbal-savoury','red_meat','Lamb kleftiko with garlic and bay leaf','complement','Classic Greek Xinomavro partner: slow lamb and dark herbal wine are inseparable','main','classic',1),
(594,'savoury-rich','pasta','Moussaka with béchamel and Kefalotyri','complement','Layered lamb-eggplant and béchamel find structure and lift in Xinomavro tannins','main','classic',1),
(594,'gamey-herbal','game','Braised rabbit with olives and capers','complement','Lean game and olive bitterness echo Xinomavro''s savoury, herb-tinged dark fruit','main','established',2),
(594,'smoky-savoury','seafood','Chargrilled octopus with lemon and rigani','complement','Smoky char and brine find balance in Xinomavro''s acidity and fresh herb note','main','established',2),
(594,'sharp-savoury','cheese','Aged Kefalotyri with green olives and pita','complement','Hard sheep-goat cheese binds tannins and echoes wine''s savoury mineral depth','cheese','established',2),
(594,'smoky-spiced','pork','Loukaniko sausage with grilled peppers and pita','complement','Spiced pork sausage and charred pepper match Xinomavro''s smoky, tannic character','main','established',2),

-- 595 Thymiopoulos Earth and Sky Xinomavro — needs 5
(595,'herbal-savoury','red_meat','Slow-baked lamb with kritharaki orzo and tomato','complement','Accessible Xinomavro mirrors lamb and tomato acidity in this Greek baked classic','main','classic',1),
(595,'spiced-savoury','red_meat','Soutzoukakia (baked lamb meatballs in tomato sauce)','complement','Tomato-spiced meatballs echo wine''s acidity and herbal dark fruit complexity','main','established',2),
(595,'savoury-earthy','vegetable','Roasted aubergine and feta with oregano and olive oil','complement','Mediterranean vegetable earthiness and feta brine find a natural partner in Xinomavro','main','established',2),
(595,'herbal-savoury','red_meat','Grilled lamb chops with lemon and thyme','complement','Bright Xinomavro acidity and herbal notes mirror grilled lamb''s char and thyme','main','established',2),
(595,'sharp-savoury','cheese','Graviera Naxos cheese with thyme honey','complement','Lightly sweet aged cheese and honey complement Xinomavro''s tangy red fruit','cheese','established',2),

-- 596 La Rioja Alta Gran Reserva 904 — needs 6
(596,'herbal-savoury','red_meat','Cordero asado al horno (slow-roasted lamb)','complement','Classic Rioja Gran Reserva and roast lamb is Spain''s most iconic food pairing','main','classic',1),
(596,'fatty-crispy','pork','Cochinillo asado (Segovian roast suckling pig)','complement','Granulated pork crackling fat is tamed by Rioja''s acidity and old-vine tannins','main','classic',1),
(596,'sharp-savoury','cheese','Aged Manchego 24-month with quince paste','complement','Lanolin and buttery Manchego softens Tempranillo tannins; quince echoes red fruit','cheese','classic',1),
(596,'savoury-charred','red_meat','Chuletón de buey (aged beef chop) with salt','complement','Mineral aged beef and classic Rioja Gran Reserva are an eternal Spanish match','main','classic',1),
(596,'creamy-savoury','starter','Mushroom croquetas de Jamón with aioli','complement','Crispy croquette and mushroom-ham filling echo Rioja''s earthy, savoury depth','starter','established',2),
(596,'rich-savoury','red_meat','Rabo de toro (slow-braised oxtail) stew','complement','Long-cooked collagen and dark sauce mirror Rioja''s aged complexity and dark fruit','main','established',2),

-- 597 Marqués de Riscal Gran Reserva — needs 6
(597,'herbal-savoury','red_meat','Lamb chops with rosemary and garlic','complement','Herbaceous Tempranillo Gran Reserva mirrors roasted lamb and fresh herb seasoning','main','classic',1),
(597,'savoury-herbal','poultry','Garlic roast chicken with bread and jus','complement','Classic Rioja pairing — roast chicken with garlic is a natural match for Tempranillo','main','established',2),
(597,'briny-marine','fish','Bonito del norte with piquillo and olive oil','complement','Firm tuna and acidic Rioja are a classic Basque Country partnership','starter','established',2),
(597,'fatty-savoury','charcuterie','Jamón ibérico de bellota with pan con tomate','complement','Silky acorn-fed ham and Rioja Gran Reserva is one of Spain''s great pairings','starter','established',2),
(597,'smoky-sharp','cheese','Idiazabal smoked sheep''s cheese with membrillo','complement','Smoked milk character and quince paste echo Rioja''s vanilla oak and dark fruit','cheese','established',2),
(597,'savoury-sweet','vegetable','Pisto manchego with egg and crusty bread','complement','Slow-cooked Castilian vegetable stew pairs with the warmth of Rioja Gran Reserva','main','established',2),

-- 598 Gini La Froscà Soave Classico — needs 5
(598,'delicate-mineral','fish','Grilled Dover sole with lemon and parsley butter','complement','Chalky Garganega mineral acidity mirrors sole''s delicacy with citrus precision','main','classic',1),
(598,'briny-sweet','shellfish','Steamed mussels with white wine and cream','complement','Wine''s stone fruit and mineral note mirror the wine-steamed broth beautifully','starter','established',2),
(598,'creamy-herbaceous','pasta','Risotto al limone with fresh peas and Parmigiano','complement','Garganega almond note and citrus spine complement lemon risotto creaminess','main','established',2),
(598,'fresh-creamy','starter','Fresh ricotta bruschetta with honey and black pepper','complement','Delicate lactic cheese and honey echo wine''s floral almond and citrus character','starter','established',2),
(598,'briny-savoury','fish','Marinated whitebait with lemon and sea salt','complement','Chalky Soave mineral acidity is perfect with crispy, briny small fried fish','starter','established',2),

-- 599 Houillon-Overnoy Arbois Poulsard — needs 6
(599,'salty-savoury','charcuterie','Jura charcuterie plateau with saucisse de Morteau','complement','Light Poulsard tannins suit cured Jura meats; smoke and spice echo wine character','starter','classic',1),
(599,'nutty-savoury','cheese','Comté 36-month with walnut bread and grape must','complement','Aged Comté''s hazelnut depth aligns with Poulsard''s earthy, oxidative complexity','cheese','classic',1),
(599,'earthy-savoury','poultry','Roast free-range chicken with morel mushroom cream','complement','Delicate Poulsard texture pairs with roast chicken and earthy morel cream sauce','main','established',2),
(599,'smoky-savoury','fish','Smoked trout, horseradish and crème fraîche on rye','bridge','Smoke and cream bridge Poulsard''s mineral acidity and light cherry fruit','starter','established',2),
(599,'earthy-savoury','legume','Lentils with lardon, Dijon mustard and poached egg','complement','Rustic Jura red is perfectly suited to earthy lentils with smoky pork lardon','main','established',2),
(599,'sweet-tangy','cheese','Quince paste with Comté or Morbier rind','complement','Sweet-tart quince paste echoes Poulsard''s red fruit and earthy savoury finish','cheese','suggested',3),

-- 600 Ganevat Cuvée Julien Chardonnay (Jura) — needs 6
(600,'nutty-savoury','cheese','Comté Jura 36-month with crusty bread','complement','Nutty, oxidative Jura Chardonnay and aged Comté are the region''s greatest pairing','cheese','classic',1),
(600,'fatty-savoury','poultry','Poulet de Bresse rôti with cream and morel sauce','complement','Premium Bresse chicken and Jura Chardonnay are a classic regional marriage','main','classic',1),
(600,'sweet-savoury','shellfish','Langoustine bisque with tarragon and crème fraîche','complement','Oxidative richness of wine mirrors langoustine bisque depth and sweetness','starter','established',2),
(600,'rich-earthy','egg','Truffled soft scrambled egg on brioche','complement','Wine''s savoury, oxidative complexity pairs exquisitely with truffle and egg yolk','amuse','established',2),
(600,'savoury-light','snack','Gougères au fromage fresh from the oven','complement','Choux pastry and Gruyère echo Jura Chardonnay''s nutty oxidative character','amuse','established',2),
(600,'rich-savoury','shellfish','Lobster thermidor with Gruyère and brandy cream','complement','Full-bodied Jura Chardonnay oxidation meets lobster cream sauce richness','main','established',2),

-- 601 Tissot Arbois Vin Jaune — needs 5
(601,'savoury-earthy','poultry','Poulet au Vin Jaune with Comté and morel mushrooms','complement','The defining dish of Arbois Vin Jaune — regional wine and chicken with morel','main','classic',1),
(601,'nutty-savoury','cheese','Comté 36-month with walnuts and dried fruit','complement','Aged Comté''s nutty, crystalline depth mirrors Vin Jaune''s oxidative complexity','cheese','classic',1),
(601,'bitter-savoury','snack','Roasted walnuts with coarse sea salt','complement','Bitter walnut tannin echoes Vin Jaune''s oxidative walnut and almond character','casual','classic',1),
(601,'rich-savoury','shellfish','Lobster with Vin Jaune cream and tarragon','complement','Classic elevated pairing: lobster sweetness is lifted by wine''s oxidative richness','main','established',2),
(601,'fatty-rich','starter','Foie gras terrine with brioche and Sauternes jelly','complement','Vin Jaune''s walnut and honey note beautifully echoes foie gras richness and brioche','starter','established',2),

-- 602 Tissot Arbois Trousseau — needs 6
(602,'salty-savoury','charcuterie','Jura charcuterie with dried sausage and ham','complement','Light Trousseau tannins and bright acidity are natural partners for Jura cured meats','starter','classic',1),
(602,'earthy-savoury','poultry','Roasted quail with grape and thyme stuffing','complement','Delicate Trousseau texture matches small game bird sweetness and earthy herbs','main','established',2),
(602,'earthy-savoury','vegetable','Mushroom and tarragon tart with Gruyère','complement','Earthy mushroom and herb mirror Trousseau''s light, forest-floor complexity','starter','established',2),
(602,'pungent-savoury','cheese','Bleu de Gex blue cheese with honey and walnuts','complement','Mellow Jura blue cheese is a natural partner for the region''s light Trousseau red','cheese','established',2),
(602,'smoky-fatty','fish','Salmon gravlax with mustard dill sauce','bridge','Smoke and dill in cured salmon bridge Trousseau''s delicate acidity and berry note','starter','established',2),
(602,'earthy-savoury','legume','Lentils beluga with smoked sausage and Dijon','complement','Hearty Jura dish of lentils and sausage is an ideal match for structured Trousseau','main','established',2),

-- 603 Domaine Tempier Bandol Rouge Cuvée Classique — needs 5
(603,'savoury-rich','red_meat','Daube de boeuf Provençale with olives and thyme','complement','Mourvèdre-based Bandol is designed for this regional slow-beef stew','main','classic',1),
(603,'herbal-savoury','red_meat','Grilled lamb with tapenade and Provençal herbs','complement','Herbed lamb and black olive tapenade mirror the wine''s garrigue and dark fruit','main','classic',1),
(603,'gamey-rich','game','Wild boar stew with root vegetables and rosemary','complement','Mourvèdre''s tannic structure and dark fruit can handle wild boar''s intensity','main','established',2),
(603,'sharp-savoury','cheese','Aged Crottin de Chavignol with thyme honey','complement','Sharp goat cheese fat and honey complement the wine''s dark mineral character','cheese','established',2),
(603,'fatty-rich','legume','Duck confit cassoulet with Toulouse sausage','complement','Rich cassoulet fat needs Mourvèdre''s tannic structure and dark savoury depth','main','established',2),

-- 604 Domaine Tempier Bandol Rosé — needs 5
(604,'rich-savoury','stew','Classic bouillabaisse with rouille and croutons','complement','Provençal fish stew and Bandol rosé is one of the South of France''s greatest matches','main','classic',1),
(604,'delicate-mineral','fish','Whole grilled sea bream with fennel and lemon','complement','Elegant, structured rosé mirrors Mediterranean grilled fish with herb aromatics','main','classic',1),
(604,'earthy-savoury','vegetable','Ratatouille with fresh herbs and olive oil','complement','Provençal vegetable stew and Bandol rosé is a deeply regional, instinctive match','main','established',2),
(604,'savoury-fresh','salad','Salade niçoise with seared tuna and anchovies','complement','Saline, herby composition of niçoise echoes the wine''s mineral acidity and fruit','starter','established',2),
(604,'salty-savory','starter','Tapenade bruschetta with caperberries and herbs','complement','Black olive tapenade complements rosé''s Mourvèdre fruit and garrigue note','aperitif','established',2),

-- 605 Château Pibarnon Bandol Rouge — needs 6
(605,'herbal-savoury','red_meat','Slow-roasted leg of lamb with Provençal herbs','complement','Mourvèdre structure and dark fruit are the natural partner to herb-roasted lamb','main','classic',1),
(605,'savoury-rich','red_meat','Provençal lamb daube with olives and orange zest','complement','Regional slow-cooked lamb stew mirrors Pibarnon''s dark garrigue and olive note','main','classic',1),
(605,'roasted-earthy','vegetable','Roasted Mediterranean vegetables with herbes de Provence','complement','Roasted vegetable caramelisation echoes wine''s dark fruit and earthy tannins','main','established',2),
(605,'smoky-savoury','pork','Merguez and fennel sausages with charred peppers','complement','Spiced lamb sausage and charred pepper align with Mourvèdre''s power and spice','main','established',2),
(605,'sharp-savoury','cheese','Aged Banon wrapped in chestnut leaves','complement','Earthy, goat-forward Banon echoes wine''s garrigue and mineral tannic depth','cheese','established',2),
(605,'gamey-rich','game','Venison stew with wild mushrooms and bitter chocolate','complement','Game intensity and dark stew complexity are matched by Mourvèdre''s structure','main','established',2),

-- 606 Concha y Toro Marques de Casa Concha Chardonnay (Chile) — needs 6
(606,'delicate-mineral','fish','Pan-seared halibut with lemon beurre blanc','complement','Chilean Chardonnay''s clean citrus and oak complement white halibut delicacy','main','classic',1),
(606,'sweet-savoury','shellfish','Steamed Dungeness crab with drawn butter','complement','Ripe fruit and oak mirror crab sweetness and butter richness','main','established',2),
(606,'rich-savoury','shellfish','Lobster bisque with tarragon and cream','complement','Creamy Chardonnay texture and vanilla oak harmonise with lobster bisque richness','starter','established',2),
(606,'sweet-savoury','soup','Corn chowder with smoked paprika and chive','complement','Sweet corn and cream echo Chardonnay''s ripe fruit and smooth mid-palate','starter','established',2),
(606,'creamy-herbal','poultry','Chicken with cream, tarragon and mushroom sauce','complement','Classic cream-herb chicken is naturally suited to this polished Chilean Chardonnay','main','established',2),
(606,'tangy-fresh','cheese','Soft fresh goat cheese with herbs and cracker','complement','Lactic tang of goat cheese mirrors Chardonnay''s bright acidity and stone fruit','cheese','established',2),

-- 607 Kingston Family Alazan Pinot Noir (Casablanca) — needs 6
(607,'marine-fatty','fish','Whole roasted salmon with herbs and lemon','complement','Casablanca Pinot mirrors salmon''s fatty texture with fresh red fruit and acidity','main','classic',1),
(607,'fatty-savoury','poultry','Duck breast with cherry and port reduction','complement','Red fruit and silky Pinot texture harmonise with duck fat and cherry reduction','main','established',2),
(607,'earthy-umami','pasta','Mushroom risotto with truffle oil and Parmesan','complement','Earthy Casablanca Pinot and mushroom risotto share forest floor and umami depth','main','established',2),
(607,'savoury-fruity','pork','Pork loin with plum and hoisin glaze','complement','Sweet-savoury glaze echoes Pinot''s red fruit; wine acidity balances richness','main','established',2),
(607,'earthy-sweet','vegetable','Roasted beetroot salad with walnuts and feta','bridge','Earthy beet and walnut echo Pinot''s forest-floor earthiness and spice notes','starter','established',2),
(607,'rich-creamy','cheese','Camembert de Normandie with crusty baguette','complement','Buttery, earthy Camembert complements Pinot''s fruit and gentle tannic structure','cheese','established',2);

COMMIT;
