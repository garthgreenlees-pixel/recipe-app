BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- 465: Tanna Noble Kava Borogu
(465, 'traditional_cultural', 'Vanuatu Noble Kava Ceremony',
 'Earthy, slightly bitter, peppery, nutty; numbing kavalactone effect; nakamal ceremony.',
 'grain', 'coconut starchy',
 'Laplap (Vanuatu root-vegetable and coconut dish) or cassava flatbread; the traditional accompaniment to kava ceremony — starchy food to moderate the absorption of kavalactones.',
 'complement', 'Starchy root vegetables slow kavalactone absorption; coconut fat tempers the earthy bitterness; sense-of-place: laplap and kava define Vanuatu''s ceremonial food culture.',
 'casual', 'classic', 2, true),

(465, 'traditional_cultural', 'Vanuatu Noble Kava Ceremony',
 'Earthy, slightly bitter, peppery, nutty; numbing kavalactone effect; nakamal ceremony.',
 'grain', 'breadfruit roasted',
 'Roasted breadfruit or uru (breadfruit) chips; the island''s most versatile staple pairs naturally with the pre-dinner kava session.',
 'complement', 'Earthy, starchy breadfruit tempers kava''s bitterness; the shared Pacific island origin creates cultural coherence; neutral starch resets the palate.',
 'casual', 'established', 2, true),

(465, 'traditional_cultural', 'Vanuatu Noble Kava Ceremony',
 'Earthy, slightly bitter, peppery, nutty; numbing kavalactone effect; nakamal ceremony.',
 'fruit', 'tropical fresh',
 'Fresh watermelon, papaya or pineapple; the traditional kava chaser — sweet tropical fruit immediately after the shell of kava to cleanse the bitterness and refresh the palate.',
 'cleanse', 'Sweet tropical fruit immediately neutralises kava''s earthy-bitter aftertaste; the high water content rinses the kavalactone residue.',
 'casual', 'classic', 2, true),

-- 466: Vanuatu Noble Kava Export — Nakamal
(466, 'traditional_cultural', 'Vanuatu Noble Kava Powder',
 'Pepper, earth, mild sweet, nutty undertone, kavalactone warmth; export micro-ground.',
 'grain', 'dark chocolate cocoa',
 'Dark chocolate (72%) or cacao nib; the earthy-peppery kava finds an unusual but harmonious pairing with high-quality dark chocolate''s bitterness.',
 'complement', 'Shared earthy-bitter register between kava and dark chocolate; cacao''s fat tempers kavalactone sharpness; pepper in kava bridges chocolate''s aromatic spice.',
 'digestif', 'adventurous', 1, true),

(466, 'traditional_cultural', 'Vanuatu Noble Kava Powder',
 'Pepper, earth, mild sweet, nutty undertone, kavalactone warmth; export micro-ground.',
 'grain', 'coconut cookies',
 'Coconut macaroons or coconut cream biscuits; fat and sweetness from coconut tempers the kava''s astringency while the tropical flavour creates sense-of-place.',
 'complement', 'Coconut fat moderates kavalactone intensity; sweetness bridges kava''s earthy-mild sweet undertone; tropical island coherence.',
 'casual', 'established', 1, true),

-- 467: Lehua Hawaiian Awa Mahakea
(467, 'traditional_cultural', 'Hawaiian Awa Ceremonial',
 'Earthy sweet, light floral, mild numbing, nutty, gentle pepper; Hawaiian ceremony tradition.',
 'grain', 'poi taro',
 'Poi (fermented taro paste) or kalo (taro) preparations; awa and poi are the twin ceremonial foods of Hawaiian culture — consumed together at ho''oponopono and luau traditions.',
 'complement', 'Sense-of-place: awa and poi define Hawaiian ceremonial food culture; earthy sweetness of awa mirrors poi''s fermented starch character; both are digestive in traditional use.',
 'casual', 'classic', 2, true),

(467, 'traditional_cultural', 'Hawaiian Awa Ceremonial',
 'Earthy sweet, light floral, mild numbing, nutty, gentle pepper; Hawaiian ceremony tradition.',
 'seafood', 'raw fish poke',
 'Ahi poke with sesame, sea salt and green onion; the mild numbing of awa and the fresh umami of raw fish create an ancient Hawaiian pairing of great subtlety.',
 'complement', 'Gentle pepper and earthiness in awa complement raw fish''s clean ocean character; light floral notes bridge the sesame oil''s nuttiness; sea salt emphasises both.',
 'casual', 'adventurous', 2, true),

-- 468: Samoan Ava Ceremony
(468, 'traditional_cultural', 'Samoan Ava Ceremony',
 'Mild earthy, slightly sour, cooling, light pepper; Samoan fa''asamoa custom.',
 'grain', 'palusami coconut',
 'Palusami (taro leaves in coconut cream) or fa''alifu dishes; the traditional Samoan feast accompaniment to ava ceremony — coconut-rich preparations that complement the ava''s cooling character.',
 'complement', 'Coconut cream fat in palusami moderates ava''s mild sourness; taro''s earthiness mirrors ava''s root character; sense-of-place: Samoan ceremony food and ava are inseparable.',
 'casual', 'classic', 3, true),

(468, 'traditional_cultural', 'Samoan Ava Ceremony',
 'Mild earthy, slightly sour, cooling, light pepper; Samoan fa''asamoa custom.',
 'meat', 'umu pork',
 'Umu-roasted pork or lu (pork in taro leaves); the ava ceremony traditionally precedes the umu feast — smoked pork from the earth oven pairs with the mild, cooling character of ava.',
 'bridge', 'Cooling effect of ava prepares the palate for the rich fat of umu pork; slight sourness acts as a palate cleanser between bites of rich slow-cooked meat.',
 'casual', 'established', 3, true),

-- 469: Barako Lambanog Philippines
(469, 'traditional_cultural', 'Lambanog Coconut Palm Spirit',
 'Fresh coconut, light sweetness, clean floral, botanical warmth; triple-distilled 40-45% ABV.',
 'seafood', 'kinilaw ceviche',
 'Kinilaw (Philippine ceviche with cane vinegar and coconut) or fresh seafood; the spirit''s coconut freshness and botanical warmth complement the bright acidic character of kinilaw.',
 'complement', 'Fresh coconut in lambanog mirrors the coconut milk used in kinilaw; botanical warmth bridges the cane vinegar''s acidity; clean floral adds aromatic complexity.',
 'starter', 'classic', 3, true),

(469, 'traditional_cultural', 'Lambanog Coconut Palm Spirit',
 'Fresh coconut, light sweetness, clean floral, botanical warmth; triple-distilled 40-45% ABV.',
 'meat', 'lechon roasted pork',
 'Lechon (Philippine roasted suckling pig) or crispy pork belly; the spirit''s clean sweetness and botanical warmth pair with the Philippines'' most festive food.',
 'complement', 'Botanical warmth of lambanog cuts through the richness of lechon fat; clean coconut sweetness echoes the pork''s caramelised skin character.',
 'main', 'established', 3, true),

(469, 'traditional_cultural', 'Lambanog Coconut Palm Spirit',
 'Fresh coconut, light sweetness, clean floral, botanical warmth; triple-distilled 40-45% ABV.',
 'fruit', 'tropical fresh fruits',
 'Fresh mango, calamansi or green papaya salad; the spirit''s clean coconut profile is an ideal base for tropical fruit cocktail applications or consumed neat alongside fresh tropical fruit.',
 'complement', 'Fresh coconut sweetness in spirit echoes tropical fruit''s natural sweetness; botanical warmth bridges the citrus acidity of calamansi; clean finish allows fruit to dominate.',
 'casual', 'adventurous', 3, true),

-- 470: Ilocos Basi Philippines
(470, 'traditional_cultural', 'Ilocos Basi Sugarcane Wine',
 'Dried fig, bark tannin, brown sugar, tamarind, dark fruit, herbal bitter; pre-colonial.',
 'meat', 'adobo pork',
 'Ilocano pork adobo (vinegar and soy slow-braise); the wine''s bark tannin and tamarind-fig character mirror the Ilocano adobo''s sour-savoury depth.',
 'complement', 'Bark tannin in Basi bridges the vinegar acidity of adobo; tamarind note echoes the marinade''s sour depth; dried fig sweetness contrasts the soy saltiness.',
 'main', 'classic', 3, true),

(470, 'traditional_cultural', 'Ilocos Basi Sugarcane Wine',
 'Dried fig, bark tannin, brown sugar, tamarind, dark fruit, herbal bitter; pre-colonial.',
 'cheese', 'aged hard Filipino',
 'Kesong Puti (fresh Filipino white cheese) or aged gouda; the wine''s tannic-bitter character and dried fruit sweetness find a complementary dairy pairing.',
 'complement', 'Brown sugar sweetness in Basi bridges the lactic freshness of Kesong Puti; bark tannin provides structural contrast; herbal bitter lifts the pairing.',
 'casual', 'adventurous', 3, true),

-- 471: Cross-River Palm Wine Nigeria
(471, 'traditional_cultural', 'Nigerian Raphia Palm Wine Fresh',
 'Coconut sap, natural effervescence, tropical yeast, sweet-sour, fresh fruit; consumed within 24h.',
 'meat', 'suya grilled',
 'Suya (Northern Nigerian spiced beef skewers) or grilled goat; the wine''s natural carbonation and sweet-sour character refreshes between bites of spiced grilled meat.',
 'cleanse', 'Natural effervescence cleanses spice heat of suya; coconut sap sweetness tempers the Yaji spice rub; tropical freshness resets the palate.',
 'casual', 'classic', 2, true),

(471, 'traditional_cultural', 'Nigerian Raphia Palm Wine Fresh',
 'Coconut sap, natural effervescence, tropical yeast, sweet-sour, fresh fruit; consumed within 24h.',
 'seafood', 'pepper soup catfish',
 'Catfish pepper soup or fresh fish grilled on coal; the wine''s effervescence and sweet-sour character complement the intense pepper and aromatic herb of Nigerian pepper soup.',
 'complement', 'Natural effervescence bridges the pepper soup''s intense spice; coconut sap sweetness tempers Camerounensis pepper''s heat; tropical yeast adds fermented complexity.',
 'main', 'established', 2, true),

(471, 'traditional_cultural', 'Nigerian Raphia Palm Wine Fresh',
 'Coconut sap, natural effervescence, tropical yeast, sweet-sour, fresh fruit; consumed within 24h.',
 'grain', 'puff puff fried',
 'Puff puff (deep-fried dough) or chin-chin; the sweet, fresh palm wine is the traditional accompaniment to Nigerian fried snacks at gatherings.',
 'complement', 'Natural sweetness of palm wine mirrors the fried dough''s sugar; effervescence cuts through the oil; tropical freshness contrasts the richness.',
 'casual', 'classic', 2, true),

-- 472: Bafoussam Matango Cameroon
(472, 'traditional_cultural', 'Cameroon Matango Banana Wine',
 'Ripe banana, caramelised sugar, mild tartness, light carbonation, tropical fruit, clean finish.',
 'meat', 'poulet DG braised',
 'Poulet DG (Directeur Général — braised chicken with plantain and vegetables) or ndolé; Cameroon''s national dish matches its traditional banana wine with regional authenticity.',
 'complement', 'Sense-of-place: Matango and Poulet DG are both Cameroonian cultural icons; ripe banana and caramelised sugar in the wine bridge the plantain in the dish.',
 'main', 'classic', 3, true),

(472, 'traditional_cultural', 'Cameroon Matango Banana Wine',
 'Ripe banana, caramelised sugar, mild tartness, light carbonation, tropical fruit, clean finish.',
 'meat', 'goat grilled braised',
 'Grilled goat or achu (pounded cocoyam with yellow soup); the wine''s mild tartness and carbonation complement the rich, savoury depth of West Cameroonian goat preparations.',
 'complement', 'Mild tartness in wine acts as refreshing counterpoint to goat''s richness; caramelised banana sweetness bridges any palm oil in the preparation; carbonation cleanses the palate.',
 'main', 'established', 3, true),

(472, 'traditional_cultural', 'Cameroon Matango Banana Wine',
 'Ripe banana, caramelised sugar, mild tartness, light carbonation, tropical fruit, clean finish.',
 'fruit', 'tropical sweet ripe',
 'Fresh mango, pineapple or papaya; the wine''s ripe tropical fruit character finds a natural partner in fresh Central African tropical fruit.',
 'complement', 'Ripe banana in wine echoes the tropical sweetness of mango and pineapple; mild tartness bridges the fruit''s natural acidity; carbonation lifts the combination.',
 'casual', 'established', 3, true);

COMMIT;
