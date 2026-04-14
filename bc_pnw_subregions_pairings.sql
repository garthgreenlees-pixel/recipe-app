BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 447: Garry Oaks Gulf Islands Gewurztraminer
(447, 'wine_still', 'Gulf Islands Gewurztraminer',
 'Lychee, rose petal, ginger, litchi, floral spice, clean mineral; volcanic basalt soils.',
 'seafood', 'crab dungeness',
 'Dungeness crab with drawn butter and lemon; the wine''s lychee and floral spice create a beautiful Pacific Northwest sense-of-place pairing.',
 'complement', 'Lychee sweetness in wine echoes the natural sweetness of Dungeness crab; rose petal florality lifts the buttery richness; ginger bridges the lemon.',
 'main', 'classic', 2, true),

(447, 'wine_still', 'Gulf Islands Gewurztraminer',
 'Lychee, rose petal, ginger, litchi, floral spice, clean mineral; volcanic basalt soils.',
 'meat', 'pork asian-spiced',
 'Vietnamese pork salad with lychee and mint or Thai larb; the wine''s lychee-ginger profile finds a natural partner in Southeast Asian preparations.',
 'complement', 'Lychee appears in both wine and salad; ginger in wine bridges Vietnamese spice; rose petal floral lift suits mint and fresh herb.',
 'main', 'adventurous', 2, true),

(447, 'wine_still', 'Gulf Islands Gewurztraminer',
 'Lychee, rose petal, ginger, litchi, floral spice, clean mineral; volcanic basalt soils.',
 'cheese', 'soft-ripened floral',
 'Camembert or Brie with floral honey; the wine''s rose petal and spice character complements the creamy, earthy character of soft-ripened Brie.',
 'complement', 'Floral spice in wine bridges the earthy, mushroom character of Brie; lychee sweetness balances the cheese''s savoury richness.',
 'cheese', 'established', 2, true),

-- 448: Fort Berens Lillooet Riesling
(448, 'wine_still', 'Lillooet Riesling Off-Dry',
 'Petrol, lime zest, white peach, stony mineral, honey, crisp acidity; high-desert terroir.',
 'seafood', 'sushi sashimi',
 'Pacific salmon sashimi or spot prawn nigiri; the wine''s petrol-mineral and lime character creates a compelling Pacific Northwest Riesling-sashimi pairing.',
 'cleanse', 'Crisp acidity and citrus cut through fish fat; stony mineral mirrors the clean, cold ocean character of Pacific salmon; honey rounds the pairing.',
 'main', 'classic', 2, true),

(448, 'wine_still', 'Lillooet Riesling Off-Dry',
 'Petrol, lime zest, white peach, stony mineral, honey, crisp acidity; high-desert terroir.',
 'meat', 'pork spicy',
 'Korean pulled pork or spiced pork belly; Riesling''s off-dry honey and crisp acidity are ideal for cutting through fatty, spiced pork.',
 'cleanse', 'Off-dry honey in wine tames spice heat; crisp acidity cuts pork fat; petrol minerality adds an unexpected aromatic complexity.',
 'main', 'established', 2, true),

(448, 'wine_still', 'Lillooet Riesling Off-Dry',
 'Petrol, lime zest, white peach, stony mineral, honey, crisp acidity; high-desert terroir.',
 'cheese', 'aged chèvre hard',
 'Aged Crottin or hard goat''s milk cheese; Riesling''s mineral backbone and off-dry honey create an elegant match with aged chèvre.',
 'complement', 'Stony mineral echoes the chalky terroir character of aged chèvre; honey bridges the cheese''s lactic tang.',
 'cheese', 'established', 2, true),

-- 449: Recline Ridge Shuswap Bacchus
(449, 'wine_still', 'Shuswap Bacchus White',
 'Peach blossom, apricot, muscat spice, green apple, light floral; cool-climate BC.',
 'seafood', 'halibut steamed',
 'Steamed halibut with ginger and scallion; the wine''s light floral and stone fruit character complements the delicate, clean flavours of BC halibut.',
 'complement', 'Peach blossom and light floral lift the clean halibut; Muscat spice echoes ginger seasoning without overpowering the delicate fish.',
 'main', 'established', 3, true),

(449, 'wine_still', 'Shuswap Bacchus White',
 'Peach blossom, apricot, muscat spice, green apple, light floral; cool-climate BC.',
 'cheese', 'fresh mild',
 'Fresh chèvre or young ricotta with honey; the wine''s light apricot and floral sweetness are at ease with mild, fresh dairy.',
 'complement', 'Apricot and peach blossom in wine complement the fresh lactic quality of chèvre; honey bridges the wine''s delicate sweetness.',
 'casual', 'established', 3, true),

-- 450: Hillside Thompson Valley Muscat Ottonel
(450, 'wine_still', 'Thompson Valley Muscat Ottonel Dry',
 'Orange blossom, apricot, floral spice, citrus, dry mineral; aromatic Alsatian grape.',
 'seafood', 'spot prawns',
 'BC spot prawns with garlic butter or prawn ceviche with citrus; the wine''s orange blossom and citrus complement the natural sweetness of spot prawns.',
 'complement', 'Orange blossom floral mirrors the delicate sweetness of spot prawn; citrus in wine bridges the lemon or citrus accompaniment; dry finish cleanses.',
 'main', 'classic', 2, true),

(450, 'wine_still', 'Thompson Valley Muscat Ottonel Dry',
 'Orange blossom, apricot, floral spice, citrus, dry mineral; aromatic Alsatian grape.',
 'meat', 'tagine Moroccan',
 'Moroccan chicken tagine with preserved lemon and olives; the wine''s floral spice and citrus profile bridges North African aromatics.',
 'bridge', 'Floral spice in wine bridges the warm spice of a tagine; orange blossom mirrors the preserved lemon''s citrus-brine character; dry mineral holds against the complexity.',
 'main', 'adventurous', 2, true),

-- 451: Moon Curser Skaha Bench Tannat
(451, 'wine_still', 'Skaha Bench Tannat',
 'Dark cherry, leather, iron, dark plum, tobacco; firm tannin; adapted from Madiran.',
 'meat', 'beef grilled short ribs',
 'Grilled beef short ribs or brisket; Tannat''s firm tannin and iron density are best tempered by fatty, protein-rich beef preparations.',
 'complement', 'Iron and dark cherry in Tannat align with short rib''s rich flavour; firm tannin integrates with rendered fat; tobacco adds savoury depth.',
 'main', 'classic', 2, true),

(451, 'wine_still', 'Skaha Bench Tannat',
 'Dark cherry, leather, iron, dark plum, tobacco; firm tannin; adapted from Madiran.',
 'meat', 'duck confit rich',
 'Duck confit with lentils and rendered fat; Tannat''s powerful tannin requires the fat and richness of slow-cooked duck to fully integrate.',
 'complement', 'Duck fat softens Tannat''s firm tannin; dark cherry and leather match the confit''s deep savoury richness; tobacco adds complexity.',
 'main', 'established', 2, true),

(451, 'wine_still', 'Skaha Bench Tannat',
 'Dark cherry, leather, iron, dark plum, tobacco; firm tannin; adapted from Madiran.',
 'cheese', 'aged hard cow',
 'Aged Manchego or cloth-bound Cheddar; Tannat''s structural tannin and tobacco depth require a cheese with enough protein to tame it.',
 'complement', 'Firm tannin integrated by crystalline cheese protein; tobacco aligns with aged cheese''s savoury complexity.',
 'cheese', 'adventurous', 2, true),

-- 452: Thornhaven Summerland Gewurztraminer
(452, 'wine_still', 'Summerland Gewurztraminer Dry',
 'Rose petal, lychee, grapefruit, dry mineral, gentle spice; lake-cooled west bench.',
 'seafood', 'salmon grilled',
 'Grilled BC salmon with ginger butter and bok choy; the wine''s dry rose-grapefruit character handles rich salmon without being overpowered.',
 'complement', 'Rose petal and ginger spice in wine mirror the ginger butter; grapefruit acidity cuts salmon oil while lychee adds aromatic lift.',
 'main', 'classic', 2, true),

(452, 'wine_still', 'Summerland Gewurztraminer Dry',
 'Rose petal, lychee, grapefruit, dry mineral, gentle spice; lake-cooled west bench.',
 'meat', 'chicken lemongrass',
 'Lemongrass and coconut chicken or Thai green curry; the wine''s floral-spice profile creates a natural bridge with Southeast Asian aromatics.',
 'bridge', 'Gentle spice in wine bridges lemongrass and coconut; rose petal florality lifts the curry''s complexity; dry finish prevents the pairing from becoming too rich.',
 'main', 'established', 2, true),

-- 453: Wilridge Rattlesnake Hills Syrah
(453, 'wine_still', 'Rattlesnake Hills Washington Syrah',
 'Iron, dark berry, olive tapenade, white pepper, smoked meat; volcanic basalt.',
 'meat', 'lamb braised',
 'Braised lamb shoulder with olive tapenade and rosemary; the wine''s smoked olive and iron character find their most natural partner in long-braised lamb.',
 'complement', 'Olive tapenade in wine mirrors the dish garnish directly; iron aligns with lamb''s mineral richness; white pepper bridges rosemary spice.',
 'main', 'classic', 2, true),

(453, 'wine_still', 'Rattlesnake Hills Washington Syrah',
 'Iron, dark berry, olive tapenade, white pepper, smoked meat; volcanic basalt.',
 'meat', 'beef grilled char',
 'Dry-aged ribeye or char-grilled flank steak; the wine''s smoked meat character finds a direct partner in heavily charred beef.',
 'complement', 'Smoked meat in wine echoes the Maillard-charred crust; iron mineral aligns with dry-aged beef''s myoglobin; dark berry provides fruit contrast.',
 'main', 'established', 2, true),

(453, 'wine_still', 'Rattlesnake Hills Washington Syrah',
 'Iron, dark berry, olive tapenade, white pepper, smoked meat; volcanic basalt.',
 'cheese', 'aged hard cave',
 'Cave-aged Gruyère or aged Comté; the wine''s mineral iron and smoked character find a natural match in aged mountain cheese.',
 'complement', 'Iron mineral in wine mirrors mineral depth of cave-aged Gruyère; smoked character bridges the cheese''s caramelised notes.',
 'cheese', 'established', 2, true),

-- 454: Destiny Ridge Wahluke Slope Cabernet Sauvignon
(454, 'wine_still', 'Wahluke Slope Washington Cabernet Sauvignon',
 'Blackcurrant, cassis, dark chocolate, vanilla cedar, mocha, ripe plum; Washington''s hottest AVA.',
 'meat', 'beef short rib',
 'Slow-braised beef short rib with mocha-red wine reduction; the wine''s dark chocolate and mocha markers find exact expression in this preparation.',
 'complement', 'Dark chocolate and mocha in wine mirror the reduction''s flavour; ripe plum and cassis provide fruit depth; vanilla cedar bridges the braise.',
 'main', 'classic', 2, true),

(454, 'wine_still', 'Wahluke Slope Washington Cabernet Sauvignon',
 'Blackcurrant, cassis, dark chocolate, vanilla cedar, mocha, ripe plum; Washington''s hottest AVA.',
 'meat', 'lamb roasted',
 'Roasted rack of lamb with cassis reduction and rosemary; the wine''s rich cassis-cedar structure creates a generous, modern Cabernet-lamb pairing.',
 'complement', 'Cassis in both wine and reduction creates an echo; vanilla cedar structure matches herb-roasted lamb''s savoury richness.',
 'main', 'established', 2, true),

(454, 'wine_still', 'Wahluke Slope Washington Cabernet Sauvignon',
 'Blackcurrant, cassis, dark chocolate, vanilla cedar, mocha, ripe plum; Washington''s hottest AVA.',
 'cheese', 'aged hard sharp',
 'Aged cheddar or aged Gouda; the wine''s generous fruit and vanilla oak need a cheese with enough structure to stand up to its warmth.',
 'complement', 'Vanilla cedar in wine bridges aged cheese''s caramel crystalline character; dark chocolate complements the savoury nuttiness of aged Gouda.',
 'cheese', 'established', 2, true),

-- 455: Ancient Lakes Columbia Valley Riesling
(455, 'wine_still', 'Ancient Lakes Columbia Valley Riesling',
 'Mandarin, lime zest, apricot, stony mineral, honey, clean finish; sandy soils.',
 'seafood', 'dungeness crab',
 'Dungeness crab legs with lemon butter; the wine''s mandarin and lime zest acidity and mineral precision create an outstanding Pacific Northwest pairing.',
 'complement', 'Mandarin and lime zest brightness lifts Dungeness crab''s sweet flesh; stony mineral echoes the cold ocean character; honey rounds the finish.',
 'main', 'classic', 2, true),

(455, 'wine_still', 'Ancient Lakes Columbia Valley Riesling',
 'Mandarin, lime zest, apricot, stony mineral, honey, clean finish; sandy soils.',
 'meat', 'pork belly asian',
 'Taiwanese pork belly bao or char siu; Riesling''s off-dry profile and bright acidity are the ideal counterpart to sticky-sweet Chinese pork preparations.',
 'cleanse', 'Honey off-dry sweetness complements char siu glaze; lime zest acidity cuts pork fat; stony mineral provides a clean finish after each bite.',
 'casual', 'established', 2, true),

-- 456: Fielding Hills Lake Chelan Syrah
(456, 'wine_still', 'Lake Chelan Syrah Cool-Climate',
 'Violet, smoked olive, red cherry, white pepper, granite mineral, fine tannin.',
 'meat', 'salmon cedar-plank',
 'Cedar-plank roasted salmon; the wine''s violet and granite mineral create an unexpectedly elegant Syrah-salmon pairing from the Pacific Northwest.',
 'complement', 'Cedar-plank smoke echoes the wine''s smoked olive note; red cherry''s acidity bridges salmon''s richness; fine tannin provides light structure.',
 'main', 'adventurous', 2, true),

(456, 'wine_still', 'Lake Chelan Syrah Cool-Climate',
 'Violet, smoked olive, red cherry, white pepper, granite mineral, fine tannin.',
 'meat', 'lamb herb-crusted',
 'Herb-crusted rack of lamb with olive jus; the wine''s smoked olive and pepper character mirror a classic Rhône-inspired lamb preparation.',
 'complement', 'Smoked olive in wine mirrors olive jus; white pepper echoes herb crust seasoning; violet adds aromatic elegance.',
 'main', 'established', 2, true),

(456, 'wine_still', 'Lake Chelan Syrah Cool-Climate',
 'Violet, smoked olive, red cherry, white pepper, granite mineral, fine tannin.',
 'cheese', 'aged hard alpine',
 'Raclette or Appenzeller; the wine''s granite mineral and violet finesse pair well with Swiss mountain cheese''s balanced complexity.',
 'complement', 'Granite mineral in wine mirrors Alpine cheese terroir; violet florality lightens what could otherwise be a heavy cheese-Syrah pairing.',
 'cheese', 'established', 2, true),

-- 457: Naches Heights Cabernet Franc
(457, 'wine_still', 'Naches Heights Cabernet Franc High-Altitude',
 'Cassis, graphite, fresh herb, red pepper, mineral, silk tannin; 1200m ancient lava.',
 'meat', 'pork rillons',
 'Rillons de Tours or confit pork belly; the wine''s graphite-cassis structure and herbal lift make a Loire-inspired classic match for pork.',
 'complement', 'Cassis and fresh herb mirror the Loire-style Cab Franc character; graphite integrates with pork fat.',
 'starter', 'classic', 2, true),

(457, 'wine_still', 'Naches Heights Cabernet Franc High-Altitude',
 'Cassis, graphite, fresh herb, red pepper, mineral, silk tannin; 1200m ancient lava.',
 'cheese', 'chèvre aged',
 'Aged chèvre or Crottin; the wine''s mineral acidity and herb character create the classic Loire Cab Franc-goat cheese pairing in a Pacific Northwest setting.',
 'complement', 'Graphite acidity and fresh herb mirror the classic Loire combination; silk tannin matches chèvre''s delicate protein without overwhelming.',
 'cheese', 'classic', 2, true),

(457, 'wine_still', 'Naches Heights Cabernet Franc High-Altitude',
 'Cassis, graphite, fresh herb, red pepper, mineral, silk tannin; 1200m ancient lava.',
 'meat', 'duck breast',
 'Duck breast with cherry reduction and roasted beets; the wine''s cassis-graphite tension and red pepper lift create an elegant partner for duck.',
 'complement', 'Cassis in wine bridges cherry reduction; graphite structure handles duck fat; red pepper note mirrors the beet''s earthy sweetness.',
 'main', 'established', 2, true),

-- 458: Snipes Family Old Vine Grenache
(458, 'wine_still', 'Snipes Mountain Old-Vine Grenache',
 'Kirsch, garrigue, dried rose, warm spice, silk texture, orange peel; 1917 plantings.',
 'meat', 'lamb provençal',
 'Provençal-style rack of lamb with herbes and tapenade; the wine''s garrigue and kirsch are perfectly aligned with Provençal lamb cookery.',
 'complement', 'Garrigue and dried rose in wine mirror herbes de Provence; kirsch bridges the red fruit in a lamb jus; warm spice rounds the preparation.',
 'main', 'classic', 2, true),

(458, 'wine_still', 'Snipes Mountain Old-Vine Grenache',
 'Kirsch, garrigue, dried rose, warm spice, silk texture, orange peel; 1917 plantings.',
 'cheese', 'aged sheep pecorino',
 'Aged Pecorino Toscano or aged Manchego; the wine''s warm spice and silk texture find harmony with the nutty richness of aged sheep''s milk cheese.',
 'complement', 'Kirsch and warm spice of Grenache align with aged Pecorino''s savoury complexity; orange peel provides a brightening finish.',
 'cheese', 'established', 2, true),

(458, 'wine_still', 'Snipes Mountain Old-Vine Grenache',
 'Kirsch, garrigue, dried rose, warm spice, silk texture, orange peel; 1917 plantings.',
 'meat', 'pork sausage spiced',
 'Merguez or Toulouse sausage with mustard; the wine''s warm spice and garrigue character are naturally suited to sausage with spiced character.',
 'complement', 'Warm spice bridges spiced sausage seasoning; garrigue echoes herb components; kirsch and orange peel provide aromatic brightness against cured meat.',
 'casual', 'established', 2, true),

-- 459: Ledger David Southern Oregon Merlot
(459, 'wine_still', 'Southern Oregon Merlot',
 'Plum, mocha, cedar, dark cherry, soft tannin, vanilla; accessible Southern Oregon red.',
 'meat', 'beef burger',
 'Gourmet burger with aged cheddar and caramelised onions; the wine''s generous plum-mocha warmth and soft tannin make it the ideal companion for a quality burger.',
 'complement', 'Plum and dark cherry bridge the beef''s Maillard richness; mocha echoes the caramelised onion''s sweetness; soft tannin matches medium-cooked beef.',
 'casual', 'classic', 2, true),

(459, 'wine_still', 'Southern Oregon Merlot',
 'Plum, mocha, cedar, dark cherry, soft tannin, vanilla; accessible Southern Oregon red.',
 'meat', 'chicken roasted mushroom',
 'Roasted chicken thighs with mushroom cream sauce; the wine''s mocha-plum character provides accessible richness suited to casual chicken preparations.',
 'complement', 'Mocha and dark cherry in wine complement mushroom cream sauce''s earthy richness; soft tannin and vanilla oak suit chicken''s mild flavour.',
 'main', 'established', 2, true),

-- 460: Eyrie Vineyards McMinnville Pinot Gris
(460, 'wine_still', 'McMinnville Oregon Pinot Gris',
 'Melon, pear, cream, mineral, citrus, toasted almond; 50-year-old vines.',
 'shellfish', 'oysters razor clams',
 'Razor clams or Pacific oysters with lemon; the wine''s mineral precision and citrus-cream character are a natural Oregon coastal pairing.',
 'complement', 'Mineral and citrus in wine mirror the briny, clean character of Pacific razor clams; cream texture provides a gentle body against the clean shellfish.',
 'starter', 'classic', 1, true),

(460, 'wine_still', 'McMinnville Oregon Pinot Gris',
 'Melon, pear, cream, mineral, citrus, toasted almond; 50-year-old vines.',
 'seafood', 'halibut grilled',
 'Grilled halibut with brown butter and capers; the wine''s toasted almond and citrus notes mirror the meunière preparation.',
 'complement', 'Toasted almond in wine echoes brown butter nuttiness; citrus bridges caper acidity; cream texture matches halibut''s firm, delicate flesh.',
 'main', 'established', 1, true),

(460, 'wine_still', 'McMinnville Oregon Pinot Gris',
 'Melon, pear, cream, mineral, citrus, toasted almond; 50-year-old vines.',
 'cheese', 'soft-ripened mild',
 'Oregon Brie or Camembert-style; the wine''s cream texture and toasted almond lift create an elegant match with soft-ripened Pacific Northwest cheese.',
 'complement', 'Cream texture of wine mirrors the soft-ripened richness; toasted almond bridges the mushroomy character of the rind.',
 'cheese', 'established', 1, true),

-- 461: Cristom Van Duzer Corridor Pinot Noir
(461, 'wine_still', 'Van Duzer Corridor Willamette Pinot Noir',
 'Red cherry, forest floor, spice, silk tannin, mineral, dried rose; coastal wind cooling.',
 'meat', 'duck roasted oregon',
 'Oregon duck breast with Pinot reduction and Willamette Valley hazelnuts; a sense-of-place celebration of Oregon''s finest pairing.',
 'complement', 'Red cherry and dried rose mirror cherry reduction; hazelnuts bridge toasted almond notes; silk tannin suits the delicacy of duck breast.',
 'main', 'classic', 1, true),

(461, 'wine_still', 'Van Duzer Corridor Willamette Pinot Noir',
 'Red cherry, forest floor, spice, silk tannin, mineral, dried rose; coastal wind cooling.',
 'mushroom', 'chanterelles',
 'Willamette Valley chanterelles with thyme butter and polenta; Oregon''s golden chanterelles are the definitive sense-of-place partner for Willamette Pinot.',
 'complement', 'Forest floor in wine mirrors chanterelle earthiness; silk tannin matches butter sauce''s richness; spice echoes thyme seasoning.',
 'main', 'classic', 1, true),

(461, 'wine_still', 'Van Duzer Corridor Willamette Pinot Noir',
 'Red cherry, forest floor, spice, silk tannin, mineral, dried rose; coastal wind cooling.',
 'fish', 'salmon wild caught',
 'Wild Pacific salmon with hazelnut beurre noisette; Willamette Pinot Noir is the classic Oregon wine for wild salmon — a regional pairing of true pedigree.',
 'complement', 'Red cherry acidity lifts the salmon richness without overpowering; silk tannin creates a gentle grip against oil; hazelnut echoes the wine''s forest depth.',
 'main', 'established', 1, true),

-- 462: Bradley Vineyards Elkton Pinot Gris
(462, 'wine_still', 'Elkton Oregon Coastal Pinot Gris',
 'Pear, green apple, mild citrus, coastal mineral, white floral; maritime cool.',
 'seafood', 'oysters pacific',
 'Pacific oysters or Kumamoto oysters with lemon; the wine''s coastal mineral and gentle pear character create a sense-of-place Elkton coastal pairing.',
 'complement', 'Coastal mineral echoes ocean character of Pacific oysters; mild citrus mirrors lemon accompaniment; white floral adds aromatic lift.',
 'aperitif', 'classic', 3, true),

(462, 'wine_still', 'Elkton Oregon Coastal Pinot Gris',
 'Pear, green apple, mild citrus, coastal mineral, white floral; maritime cool.',
 'fish', 'smoked trout',
 'Smoked trout pâté or smoked steelhead; the wine''s coastal mineral and pear freshness complement smoke-cured Pacific fish.',
 'complement', 'Coastal mineral bridges the briny character of smoked fish; pear freshness contrasts the smoke''s intensity; white floral adds aromatic elegance.',
 'starter', 'established', 3, true),

-- 463: Abacela Rogue Valley Tempranillo
(463, 'wine_still', 'Rogue Valley Oregon Tempranillo',
 'Dark cherry, leather, tobacco, dried herb, cedar, fine tannin; Iberian character.',
 'meat', 'lamb slow-braised',
 'Slow-braised lamb with saffron and almonds or Rogue Valley lamb chops; the wine''s Iberian character finds a natural match in lamb — Tempranillo''s most classic partner.',
 'complement', 'Dark cherry and tobacco of Tempranillo are the Spanish archetype for lamb; dried herb in wine echoes the lamb seasoning; fine tannin integrates with slow-braised collagen.',
 'main', 'classic', 2, true),

(463, 'wine_still', 'Rogue Valley Oregon Tempranillo',
 'Dark cherry, leather, tobacco, dried herb, cedar, fine tannin; Iberian character.',
 'charcuterie', 'jamón ibérico',
 'Jamón Ibérico or Spanish-style cured ham; the wine''s Iberian pedigree creates a sense-of-place connection with the world''s finest cured ham.',
 'complement', 'Tobacco and leather of Tempranillo are the natural Spanish counterpart to Ibérico; cedar and dried herb bridge the nutty, savoury complexity of the ham.',
 'starter', 'classic', 2, true),

(463, 'wine_still', 'Rogue Valley Oregon Tempranillo',
 'Dark cherry, leather, tobacco, dried herb, cedar, fine tannin; Iberian character.',
 'meat', 'beef grilled chuletón',
 'Grilled chuletón or T-bone steak with chimichurri; the wine''s fine tannin and cherry depth make it a natural for quality grilled beef in the Iberian tradition.',
 'complement', 'Fine tannin integrates with beef fat; dark cherry provides fruit structure; chimichurri''s herb mirrors dried herb note in wine.',
 'main', 'established', 2, true),

-- 464: Cowhorn Applegate Valley Rhône Blend
(464, 'wine_still', 'Applegate Valley Biodynamic Rhône Blend',
 'Kirsch, garrigue, white pepper, dark berry, warm spice, limestone mineral.',
 'meat', 'lamb daube',
 'Daube provençale or slow-braised lamb with olives and tomatoes; the wine''s garrigue and kirsch character mirror Provençal slow-cooked lamb.',
 'complement', 'Garrigue in wine mirrors the herbed tomato base of daube; kirsch echoes the lamb''s sweet braised character; limestone mineral provides clean finish.',
 'main', 'classic', 2, true),

(464, 'wine_still', 'Applegate Valley Biodynamic Rhône Blend',
 'Kirsch, garrigue, white pepper, dark berry, warm spice, limestone mineral.',
 'meat', 'pork grilled spiced',
 'Grilled merguez or Moroccan-spiced pork ribs; the wine''s warm spice and pepper character suit smoky, spiced preparations.',
 'complement', 'White pepper and warm spice in wine bridge the grilled meat''s char and spice seasoning; kirsch provides fruit contrast to the smoky richness.',
 'casual', 'established', 2, true),

(464, 'wine_still', 'Applegate Valley Biodynamic Rhône Blend',
 'Kirsch, garrigue, white pepper, dark berry, warm spice, limestone mineral.',
 'cheese', 'aged sheep',
 'Aged Manchego or aged Ossau-Iraty; the wine''s warm spice and limestone mineral create a natural affinity with aged sheep''s milk cheese.',
 'complement', 'Limestone mineral in wine mirrors the mountain sheep terroir of Ossau-Iraty; garrigue and warm spice complement the cheese''s nutty fruity depth.',
 'cheese', 'established', 2, true);

COMMIT;
