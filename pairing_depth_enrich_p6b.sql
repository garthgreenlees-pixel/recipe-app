BEGIN;
INSERT INTO pairing_intelligence
  (beverage_product_id, food_flavour_profile, food_category, food_description, pairing_type, flavour_logic, meal_context, confidence, authority_tier)
VALUES
-- Japanese matcha (203-209)
(203,'matcha, Ippodo Ummon, ceremonial, premium','dessert','Matcha warabi mochi with kinako and kuromitsu syrup','complement','Ummon Ceremonial Matcha''s deep umami bridges the warabi mochi; the kinako and kuromitsu mirror the tea''s vegetal depth','dessert','classic',1),
(204,'matcha, Ippodo Kan-un, ceremonial','dessert','Sakura wagashi (spring flower sweet) with azuki bean paste','complement','Kan-un Ceremonial''s fine umami bridges the sakura wagashi; the spring sweet is the classic Japanese tea ceremony pairing','dessert','classic',1),
(205,'matcha, Marukyu Wako, ceremonial','dessert','Yokan (red bean jelly) with chestnut and matcha','complement','Wako Ceremonial''s precise vegetal depth bridges the yokan''s dense sweetness; a tea master''s pairing of depth and restraint','dessert','classic',1),
(206,'matcha, Marukyu Aoarashi, ceremonial, rare','dessert','Higashi (dry wagashi) with sugar chrysanthemum and mochi rice flour','complement','Aoarashi''s vibrant green bridges the dry higashi sugar sweet; the contrast of bright matcha and delicate sweet wagashi','dessert','classic',1),
(207,'matcha, Nakamura Tokichi, Uji, ceremonial','dessert','Matcha bavarois with white bean paste and gold leaf','complement','Tokichi Uji Matcha''s Uji terroir elevates the matcha bavarois; Uji matcha for a Uji confection is a direct regional loop','dessert','classic',1),
(208,'matcha, Kyoto Obubu, Okumidori, ceremonial','dessert','Nerikiri wagashi with plum blossom motif and white bean','complement','Obubu Okumidori''s single-cultivar intensity bridges the nerikiri; the sculptor''s wagashi meets the single-origin matcha','dessert','classic',1),
(209,'matcha, Yamamotoyama, culinary, accessible','casual','Matcha pancakes with azuki bean cream and maple syrup','complement','Yamamotoyama Culinary Matcha''s bold accessible character bridges the matcha pancakes; an everyday matcha for everyday cooking','casual','established',2),

-- Gyokuro (210-212)
(210,'gyokuro, Ippodo Sayamakaori, shaded, umami','casual','Dashimaki tamago (Japanese rolled omelette) with dashi','complement','Ippodo Gyokuro''s deep shaded umami bridges the dashimaki''s subtle sweetness; both are expressions of dashi culture','casual','classic',1),
(211,'gyokuro, Marukyu Unkaku, premium shaded','seafood','Kyoto tofu (kinu-dofu) with cold dashi and kombu gelée','complement','Marukyu Unkaku Gyokuro''s deep umami bridges the silken tofu''s delicacy; both are expressions of Kyoto''s quiet luxury','starter','classic',1),
(212,'gyokuro, Kyoto Obubu, shaded single origin','casual','Cold soba noodles (zaru soba) with dipping tsuyu and wasabi','complement','Obubu Gyokuro''s shaded depth bridges the cold soba''s mineral earthiness; both are cool-climate Japanese expressions','casual','established',2),

-- Sencha/Shincha/Kabuse/Hojicha/Genmaicha/Tamaryokucha (213-222)
(213,'sencha, Ippodo Shogyokuro, premium green','seafood','Chilled tofu salad with sesame dressing and myoga ginger','complement','Ippodo Shogyokuro''s bright premium sencha bridges the chilled tofu; both are cool, delicate, and summer-facing','casual','established',2),
(214,'sencha, Marukyu Tsujikaze, premium, wind-named','casual','Tamagoyaki bento with pickled daikon and edamame','complement','Marukyu Tsujikaze''s elegant sencha bridges the tamagoyaki bento''s sweet omelette; a classic Japanese box lunch pairing','casual','classic',1),
(215,'sencha, Honyama Fukamushi, deep-steamed','casual','Onigiri with grilled salmon and shiso pickled plum','complement','Honyama Fukamushi''s deep-steamed richness bridges the onigiri; a Shizuoka deep-steamed sencha for a rice tradition','casual','classic',1),
(216,'sencha, Chiran Saemidori, Kagoshima, first flush','casual','Wagashi of the season with seasonal fruit paste','complement','Chiran Saemidori First Flush''s Kagoshima freshness bridges the seasonal wagashi; a first flush for a spring confection','casual','established',2),
(217,'sencha, Obubu Kabuse, shaded, rich','casual','Chilled chawanmushi with uni and seasonal herbs','complement','Obubu Kabuse''s shaded depth bridges the cold chawanmushi; both carry a cool, mineral, shaded quality','starter','established',2),
(218,'hojicha, Ippodo Uji, roasted, caramel','dessert','Hojicha panna cotta with caramel sauce and rice cracker','complement','Ippodo Hojicha''s roasted Uji character bridges the hojicha panna cotta; drinking the tea used in the dessert','dessert','classic',1),
(219,'genmaicha, Yamamotoyama, popcorn, rice','casual','Miso soup with tofu, wakame and rice with grilled onigiri','complement','Yamamotoyama Genmaicha''s toasted rice bridges the miso soup and grilled onigiri; a Japanese everyday table pairing','casual','classic',1),
(220,'tamaryokucha, Chiran, Kagoshima, curl-leaf','casual','Gyoza (pork and cabbage dumplings) with ponzu and chilli oil','complement','Chiran Tamaryokucha''s unique curl-leaf sencha bridges the gyoza; a Kagoshima tea for a casual Japanese izakaya bite','casual','established',2),
(221,'shincha, Nishide Shizuoka, first flush, new tea','casual','Sakura rice (cherry blossom steamed rice) with pickled sakura leaf','complement','Nishide Shincha''s first flush spring character bridges the spring sakura rice; new tea for the new spring harvest celebration','casual','classic',1),
(222,'tencha, Marukyu, raw matcha leaf, pre-grind','casual','Matcha ice cream with red bean paste and mochi ball','complement','Marukyu Tencha''s raw pre-grind leaf bridges the matcha ice cream; the same leaf family presents in different forms','dessert','classic',1),

-- Chinese pu-erh (247-251)
(247,'pu-erh, Dayi 7542, sheng, raw, classic','casual','Char siu (Cantonese BBQ pork) with steamed rice and pickled ginger','complement','Dayi 7542 Sheng bridges the char siu''s sweet-soy richness; raw pu-erh''s astringency cuts through the BBQ glaze','main','established',2),
(248,'pu-erh, Dayi 7572, shou, ripe, earthy','casual','Aged Chinese preserved duck (la ya) with steamed jasmine rice','complement','Dayi 7572 Shou''s earthy depth bridges the preserved duck''s intense aged character; both are Chinese preservation traditions','main','classic',1),
(249,'pu-erh, Yiwu Ancient Tree, sheng, complex','casual','Yunnan ham (Xuanwei ham) with steamed buns and chilli oil','complement','Yiwu Ancient Tree Sheng''s complex old-tree character bridges the Yunnan ham; both are Yunnan''s finest preserved expressions','casual','classic',1),
(250,'pu-erh, Dianhong Gold Tips, Yunnan, honeyed black','casual','Milk cake with rose jam and cardamom — Yunnan style','complement','Dianhong Gold Tips''s honeyed malty character bridges the Yunnan milk cake and rose jam; a sweet Yunnan tea for Yunnan dairy','casual','established',2),
(251,'pu-erh, 2012 dry storage aged sheng, complex','casual','Clay pot rice (bo jai fan) with chicken, mushroom and lap cheong','complement','2012 Aged Sheng''s complexity bridges the clay pot rice; a decade-aged tea for a slow clay-cooked rice tradition','casual','classic',2),

-- Wuyi Rock oolongs (252-254)
(252,'oolong, Da Hong Pao, Wuyi, roasted, mineral','casual','Braised tofu with fermented black bean and sesame oil','complement','Zhengyan Da Hong Pao''s mineral roast bridges the fermented black bean tofu; both draw deep umami from ancient rock','casual','classic',1),
(253,'oolong, Shui Xian, Wuyi rock, floral roast','casual','Pork and preserved vegetable (mei cai kou rou) steamed buns','complement','Shui Xian''s Wuyi orchid-mineral bridges the preserved vegetable pork bun; the tea''s floral note softens the salt','casual','established',2),
(254,'oolong, Rou Gui, Wuyi, cinnamon, spicy','casual','Smoked duck (Zhang tea duck) Sichuan style with camphor smoke','complement','Rou Gui''s spicy cinnamon mineral bridges the Sichuan smoked duck; both carry a warming deep spice character','main','established',2),

-- Jin Jun Mei (255) and white teas (256-257)
(255,'black tea, Jin Jun Mei, Wuyi, gold, honeyed','casual','Osmanthus and honey mooncake with lotus paste filling','complement','Jin Jun Mei''s golden honeyed sweetness bridges the osmanthus mooncake; both are China''s most precious tea-ceremony offerings','casual','classic',1),
(256,'white tea, Silver Needle, Fuding, minimal','casual','Jasmine rice congee with ginger, scallion and sesame oil','complement','Fuding Silver Needle''s delicate white tea bridges the rice congee''s clean simplicity; both express pure grain and water','casual','classic',1),
(257,'white tea, Bai Mu Dan, Fuding, floral','casual','Steamed egg with century egg, sesame oil and green onion','complement','Bai Mu Dan''s gentle floral character bridges the steamed egg''s delicacy; a soft tea for a silky Cantonese preparation','casual','established',2),

-- Tieguanyin (258-259)
(258,'oolong, Tieguanyin, charcoal roasted, Anxi','casual','Fujian crab rice with ginger and scallion (Minnan style)','complement','Traditional Tieguanyin''s roasted mineral bridges the Fujian crab rice; a Fujian tea for a Fujian coastal tradition','main','classic',1),
(259,'oolong, Tieguanyin, jade green, Anxi, light','casual','Dim sum — steamed shrimp har gow and crystal skin dumplings','complement','Jade Green Tieguanyin''s light oolong character bridges the har gow''s delicate shrimp; a Cantonese dim sum pairing','casual','classic',1),

-- Longjing (260-262)
(260,'green tea, Longjing Mingqian, tribute grade, spring','casual','West Lake vinegar fish (Xi Hu cu yu) with bamboo shoots','complement','Mingqian Longjing bridges the West Lake vinegar fish; both are Hangzhou''s most celebrated culinary expressions','main','classic',1),
(261,'green tea, Longjing Yuqian, spring grade A','casual','Spring bamboo shoot stir-fry with Longjing tea leaves','complement','Yuqian Longjing bridges the spring bamboo shoot; a Hangzhou tradition of cooking the new shoot with the new-picked tea','main','classic',1),
(262,'green tea, Longjing late spring, approachable','casual','Beggar''s chicken (wrapped clay-baked chicken) with aromatic rice','complement','Late Spring Longjing''s approachable green bridges the slow clay-baked chicken; a Hangzhou tea for a Hangzhou feast','main','established',2),

-- Dancong Phoenix oolongs (263-266)
(263,'oolong, Mi Lan Xiang Dancong, honey orchid','casual','Steamed rice roll (cheung fun) with sesame paste and soy','complement','Mi Lan Xiang''s honey orchid bridges the rice roll''s rice softness; the floral note lifts the simple dim sum character','casual','classic',1),
(264,'oolong, Ya Shi Xiang Dancong, duck shit, complex','casual','Cantonese suckling pig (ru zhu) with plum sauce and pancake','complement','Ya Shi Xiang''s complex floral mineral bridges the suckling pig; both have intense aromatic depth beneath apparent simplicity','casual','established',2),
(265,'oolong, Xing Ren Xiang Dancong, almond orchid','casual','Egg tart (dan ta) from Hong Kong bakery style, warm','complement','Xing Ren Xiang''s almond orchid bridges the warm egg tart''s custard; the almond note connects directly to the pastry','casual','established',2),
(266,'oolong, Fenghuang Old Bush Dancong, aged','casual','Preserved Chinese turnip cake (lo bak go) with chilli oil','complement','Floating Leaves Fenghuang Old Bush''s aged complexity bridges the crispy turnip cake; aged tea for aged preservation','casual','established',2),

-- Rishi blends (267-269)
(267,'pu-erh, Rishi Dante blend, approachable','casual','Vietnamese pho bo (beef pho) with basil, bean sprouts and lime','bridge','Rishi Pu-erh Dante''s earthy complexity bridges the pho''s star anise broth; both share a deep aromatic warmth','main','suggested',2),
(268,'green tea, Rishi Dragon Well, Longjing, China','casual','Steamed vegetable gyoza with ginger soy and rice vinegar','complement','Rishi Dragon Well''s clean Longjing character bridges the vegetable gyoza; a Chinese green for a Chinese-Japanese dumpling','casual','established',2),
(269,'black tea, Rishi Wuyi, Lapsang, smoky','casual','Smoked cheese (smoked Gruyère) on dark bread with cornichons','complement','Rishi Wuyi Black''s Lapsang smokiness bridges the smoked Gruyère; smoke in the tea and smoke in the cheese align','casual','established',2),

-- Taiwan high mountain oolongs (279-287)
(279,'oolong, Alishan, high mountain, spring','casual','Taiwanese three-cup chicken (san bei ji) with basil and sesame','complement','Alishan Spring''s high mountain freshness bridges the three-cup chicken''s fragrant basil; a mountain tea for a mountain spirit','main','classic',1),
(280,'oolong, Alishan, high mountain, winter','casual','Lu rou fan (Taiwanese braised pork rice) with pickled mustard greens','complement','Alishan Winter''s creamy oolong character bridges the slow-braised pork rice; Taiwan''s national snack and Taiwan''s tea','casual','classic',1),
(281,'oolong, Lishan, Wang Family, 2200m, ultra-high','casual','Steamed Taiwanese sticky rice (zongzi) with peanut and pork filling','complement','Lishan Wang Family''s elevation complexity bridges the sticky rice dumpling; the highest mountain for a deeply layered dish','casual','classic',1),
(282,'oolong, Dayuling, 2500m, ultra-high, butter','casual','Scallion pancake (cong you bing) with egg and sesame paste','complement','Dayuling 2500m''s buttery creaminess bridges the scallion pancake''s flaky softness; both carry warmth and satisfaction','casual','established',2),
(283,'oolong, Oriental Beauty, heavy oxidised, insect-nibbled','casual','Taiwanese sesame dessert soup (tang yuan) with black sesame','complement','Oriental Beauty''s honeyed fruit complexity bridges the black sesame tang yuan; both carry a deep sweet aromatic warmth','dessert','established',2),
(284,'oolong, Dong Ding, charcoal roasted, traditional','casual','Tofu with preserved soy (doubanjiang-style) and fried garlic','complement','Dong Ding Charcoal Roast''s deep mineral bridges the fermented preserved tofu; roasted tea for fermented food tradition','casual','classic',1),
(285,'oolong, Dong Ding, lightly roasted, modern','casual','Cold tofu with preserved egg (pidan) and sesame oil','complement','Modern Lightly Roasted Dong Ding''s freshness bridges the cold tofu and century egg; light roast for a delicate preparation','casual','established',2),
(286,'oolong, Jin Xuan Milk Oolong, creamy, floral','dessert','Pineapple cake (fengli su) with buttery pastry and pineapple jam','complement','Jin Xuan Milk Oolong''s creamy natural sweetness bridges the pineapple cake; Taiwan''s signature tea for Taiwan''s signature pastry','dessert','classic',1),
(287,'oolong, Baozhong, Pouchong, floral, light','casual','Spring rolls (chun juan) with vermicelli and dipping sauce','complement','Baozhong''s lightly twisted floral oolong bridges the fresh spring roll; both express delicate green freshness','casual','established',2),

-- Darjeeling 1st/2nd flush and Indian teas (288-298)
(288,'tea, Makaibari Darjeeling, first flush, biodynamic','starter','Cucumber and mint tea sandwiches with cream cheese on white bread','complement','Makaibari First Flush''s delicate muscatel bridges the cucumber and cream cheese; a Darjeeling for an English tea sandwich','casual','classic',1),
(289,'tea, Castleton second flush, muscatel, Darjeeling','casual','Victoria sponge with strawberry jam and clotted cream','complement','Castleton Second Flush Muscatel''s grape character bridges the Victoria sponge; a muscatel Darjeeling for the classic English tea','casual','classic',1),
(290,'tea, Glenburn Darjeeling second flush, floral','casual','Scones with clotted cream and Seville orange marmalade','complement','Glenburn Second Flush''s floral character bridges the scone and orange marmalade; an afternoon tea pairing of Darjeeling and cream','casual','classic',1),
(291,'tea, Jungpana autumn flush, Darjeeling, mellow','casual','Earl Grey shortbread with lemon zest and dark chocolate dip','complement','Jungpana Autumn Flush''s mellower character bridges the citrus shortbread; an autumnal tea for an autumnal biscuit','casual','established',2),
(292,'tea, Jungpana Darjeeling white, silver tips','casual','Delicate almond financier with lavender and white chocolate','complement','Jungpana Silver Tips white tea''s delicacy bridges the lavender almond financier; both are refined and floral','casual','established',2),
(293,'tea, Halmari Gold Assam, first flush, premium','casual','Scottish porridge with Assam cream and soft brown sugar','complement','Halmari Gold First Flush''s premium character bridges the porridge with Assam cream; an Assam tea for a morning grain','casual','classic',1),
(294,'tea, Halmari Assam second flush, classic, malty','casual','Full English breakfast with back bacon, fried egg and grilled tomato','complement','Halmari Second Flush''s classic malty Assam bridges the full English breakfast; the strongest tea tradition for the most complete meal','casual','classic',1),
(295,'tea, Harney & Sons Assam, Irish breakfast blend','casual','Brown bread toast with butter and Kerrygold alongside strong milk','complement','Harney Assam Irish Breakfast''s full-bodied character bridges the buttered brown bread with milk; the classic Irish morning ritual','casual','classic',1),
(296,'tea, Kairbetta Nilgiri frost tea, tippy','casual','Masala chai biscuits (nankhatai) with cardamom and pistachios','complement','Kairbetta Frost Tea''s Nilgiri brightness bridges the nankhatai cardamom; both come from the same South Indian hill tradition','casual','established',2),
(297,'tea, Harney Nilgiri black, South India, clean','casual','Butter biscuits with rose water and pistachio (nankhatai style)','complement','Harney Nilgiri''s clean South Indian character bridges the butter rose biscuit; both are light and aromatic','casual','established',2),
(298,'tea, Glenburn Darjeeling oolong, spring harvest','casual','Peach galette with frangipane and fresh thyme','complement','Glenburn Darjeeling Oolong''s spring character bridges the peach galette; a hybrid tea for a hybrid French-Indian spring pairing','casual','established',2),

-- Moroccan tea (369)
(369,'tea, Moroccan atay, gunpowder, mint, traditional','casual','Bastilla (b''stilla) pigeon pastilla with cinnamon and almond','complement','Moroccan Atay''s fresh mint bridges the bastilla''s contrasting sweet-savoury layers; the tea ceremony and the feast course belong together','main','classic',1)
;
COMMIT;
