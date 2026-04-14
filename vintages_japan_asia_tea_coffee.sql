BEGIN;

-- ============================================================
-- VINTAGE DATA: JAPAN (SAKE/SHOCHU/TEA), CHINA/TAIWAN/INDIA TEA,
--               ETHIOPIA COFFEE
-- Regions: 45-56 (Japan), 57-67 (China/Taiwan/India), 77-79 (Ethiopia)
-- ============================================================

INSERT INTO beverage_vintages
  (region_id, vintage_year, season_narrative, conditions, quality_rating,
   quality_descriptor, drinking_window, price_trajectory, value_assessment, authority_tier)
VALUES

-- ===== 45: NIIGATA (淡麗辛口 Sake) =====
(45, 2019, 'Typhoon Hagibis caused significant rice harvest damage in autumn; lower yields with reduced starch levels impacted junmai grades.',
 '{"spring": "good", "summer": "warm", "harvest": "typhoon_damage", "rice_quality": "below_average"}',
 68, 'average', '{"from": 2020, "to": 2024}', 'declining', 'Difficult year for Niigata; only the most skilled kura produced standout sake.', 1),

(45, 2020, 'Good Koshihikari rice harvest; classic Niigata tanrei karakuchi character with precise acidity and clean finish.',
 '{"spring": "warm", "summer": "mild", "harvest": "classic_niigata", "rice_quality": "good"}',
 79, 'good', '{"from": 2021, "to": 2025}', 'stable', 'Classic Niigata style; reliable tanrei karakuchi across all major kura.', 1),

(45, 2021, 'Excellent summer conditions; Koshihikari and Gohyakumangoku rice reached ideal starch development. Outstanding junmai daiginjo quality.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent_rice", "rice_quality": "outstanding"}',
 86, 'very_good', '{"from": 2022, "to": 2028}', 'stable', 'Fine Niigata vintage; junmai daiginjo from 2021 shows exceptional floral precision.', 1),

(45, 2022, 'Benchmark year; perfect warm summer with ideal rainfall balance. Finest Niigata sake in a decade.',
 '{"spring": "mild", "summer": "perfect_balance", "harvest": "benchmark", "rice_quality": "exceptional"}',
 93, 'exceptional', '{"from": 2022, "to": 2030}', 'rising', 'Landmark Niigata vintage; 2022 daiginjo is among the finest of the decade.', 1),

(45, 2023, 'Very good conditions; excellent Yamada Nishiki and Koshihikari rice. Classic Niigata elegance.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "rice_quality": "excellent"}',
 88, 'excellent', '{"from": 2023, "to": 2029}', 'stable', 'Excellent Niigata vintage; broad appeal across all grades.', 1),

-- ===== 46: NADA (神戸 Sake) =====
(46, 2019, 'Typhoon impact on Hyogo rice fields; Yamada Nishiki production reduced significantly.',
 '{"spring": "mild", "summer": "warm", "harvest": "typhoon_reduced", "rice_quality": "lower_yield"}',
 65, 'average', '{"from": 2020, "to": 2024}', 'declining', 'Challenging year; lower Yamada Nishiki yield affected premium sake production.', 1),

(46, 2020, 'Good Yamada Nishiki growing season; characteristic Nada kimoto and yamahai styles showed excellent structure.',
 '{"spring": "warm", "summer": "balanced", "harvest": "good_yamadanishiki", "rice_quality": "classic"}',
 79, 'good', '{"from": 2021, "to": 2027}', 'stable', 'Classic Nada quality; yamahai and kimoto expressions particularly impressive.', 1),

(46, 2021, 'Excellent Hyogo rice harvest; premium Yamada Nishiki at outstanding starch development. Fine junmai and daiginjo quality.',
 '{"spring": "good", "summer": "ideal_heat", "harvest": "premium_yamadanishiki", "rice_quality": "premium"}',
 85, 'very_good', '{"from": 2022, "to": 2029}', 'stable', 'Fine Nada vintage; traditionally styled sake from kimoto fermentation outstanding.', 1),

(46, 2022, 'Outstanding year; exceptional Yamada Nishiki quality from the Tojo and Yokawa districts — the finest rice in Japan.',
 '{"spring": "warm", "summer": "excellent_heat", "harvest": "exceptional_tojo", "rice_quality": "best_in_decade"}',
 92, 'exceptional', '{"from": 2022, "to": 2032}', 'rising', 'Benchmark Nada year; Tojo-produced Yamada Nishiki at peak; daiginjo outstanding.', 1),

(46, 2023, 'Very good conditions; consistent rice quality with classical Nada structured style.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "rice_quality": "very_good"}',
 87, 'excellent', '{"from": 2023, "to": 2030}', 'stable', 'Excellent Nada vintage; classic structured expression across all premier kura.', 1),

-- ===== 47: FUSHIMI (京都 Sake) =====
(47, 2019, 'Challenging harvest season; rice quality impacted by autumn weather.',
 '{"spring": "mild", "summer": "warm", "harvest": "challenging_autumn", "water": "fushimizu_stable"}',
 67, 'average', '{"from": 2020, "to": 2023}', 'stable', 'Difficult year; the Fushimizu water quality maintained some elegance despite challenging rice.', 1),

(47, 2020, 'Good season; characteristic Fushimi soft-water delicate style well expressed.',
 '{"spring": "mild", "summer": "moderate", "harvest": "good", "water": "fushimizu_excellent"}',
 78, 'good', '{"from": 2021, "to": 2026}', 'stable', 'Classic Fushimi character; soft-water elegance in all major producer lines.', 1),

(47, 2021, 'Excellent rice quality; Fushimizu spring water complemented the season''s precise rice character.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent", "water": "fushimizu_ideal"}',
 85, 'excellent', '{"from": 2021, "to": 2028}', 'stable', 'Fine Fushimi vintage; the soft-water elegance of Gekkeikan and Kizakura shines.', 1),

(47, 2022, 'Outstanding year across Kyoto sake production.',
 '{"spring": "warm", "summer": "excellent", "harvest": "outstanding", "water": "fushimizu_exceptional"}',
 90, 'excellent', '{"from": 2022, "to": 2030}', 'rising', 'Exceptional Fushimi year; the landmark combination of outstanding rice and spring water.', 1),

(47, 2023, 'Very good conditions; refined Fushimi character with characteristic Kyoto subtlety.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "water": "fushimizu_very_good"}',
 86, 'very_good', '{"from": 2023, "to": 2029}', 'stable', 'Excellent Fushimi year; pure, refined sake appropriate for the imperial capital tradition.', 1),

-- ===== 48: YAMAGUCHI (獺祭 Sake) =====
(48, 2019, 'Challenging harvest; Yamada Nishiki quality reduced by weather events.',
 '{"spring": "mild", "summer": "warm", "harvest": "below_average", "rice_quality": "impacted"}',
 66, 'average', '{"from": 2020, "to": 2023}', 'stable', 'Difficult year; even Dassai managed lower grades with reduced rice quality.', 1),

(48, 2020, 'Good rice season; Asahi Shuzo''s rigorous quality standards maintained high-grade Dassai production.',
 '{"spring": "warm", "summer": "good", "harvest": "solid_quality", "rice_quality": "good"}',
 80, 'very_good', '{"from": 2021, "to": 2026}', 'stable', 'Good Yamaguchi year; Dassai 23 and 39 show their characteristic precision.', 1),

(48, 2021, 'Excellent Yamada Nishiki from premium contracted farms.',
 '{"spring": "ideal", "summer": "excellent", "harvest": "premium_contracted", "rice_quality": "premium"}',
 86, 'very_good', '{"from": 2022, "to": 2028}', 'stable', 'Fine Yamaguchi vintage; Dassai''s high-polishing technique at its most expressive.', 1),

(48, 2022, 'Benchmark year; outstanding Yamada Nishiki quality across Yamaguchi.',
 '{"spring": "warm", "summer": "ideal_heat", "harvest": "benchmark", "rice_quality": "exceptional"}',
 91, 'exceptional', '{"from": 2022, "to": 2032}', 'rising', 'Landmark Yamaguchi sake year; Dassai''s ultra-polished expressions at their absolute peak.', 1),

(48, 2023, 'Very good conditions; refined, precise daiginjo quality.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "rice_quality": "very_good"}',
 87, 'excellent', '{"from": 2023, "to": 2030}', 'stable', 'Excellent vintage; classic Yamaguchi precision in all expressions.', 1),

-- ===== 49: YAMAGATA =====
(49, 2019, 'Typhoon impact in autumn; reduced Dewasansan and Kamenoo rice yields.',
 '{"spring": "good", "summer": "warm", "harvest": "typhoon_affected", "rice_quality": "reduced"}',
 64, 'average', '{"from": 2020, "to": 2023}', 'declining', 'Challenging year; dedicated kura maintained some quality through careful selection.', 1),

(49, 2020, 'Good season; characteristic Yamagata fruity, approachable sake style well expressed.',
 '{"spring": "mild", "summer": "warm", "harvest": "good_dewasansan", "rice_quality": "solid"}',
 78, 'good', '{"from": 2021, "to": 2025}', 'stable', 'Classic Yamagata style; aromatic, fruit-forward sake at reasonable prices.', 1),

(49, 2021, 'Excellent harvest; Dewasansan and Kamenoo heirloom rice at outstanding quality.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent_heirloom", "rice_quality": "premium"}',
 84, 'very_good', '{"from": 2021, "to": 2027}', 'stable', 'Fine Yamagata vintage; heirloom rice varieties showing excellent character.', 1),

(49, 2022, 'Benchmark year; Yamagata rice at peak starch development.',
 '{"spring": "warm", "summer": "excellent", "harvest": "peak_quality", "rice_quality": "exceptional"}',
 91, 'exceptional', '{"from": 2022, "to": 2030}', 'rising', 'Outstanding Yamagata sake; benchmark year for the prefecture''s rising reputation.', 1),

(49, 2023, 'Very good conditions; solid across all Yamagata sake production.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "rice_quality": "excellent"}',
 86, 'very_good', '{"from": 2023, "to": 2028}', 'stable', 'Excellent year; Yamagata sake continues to establish its identity.', 1),

-- ===== 50: FUKUI =====
(50, 2020, 'Good Fukui sake season; Gohyakumangoku rice quality reliable.',
 '{"spring": "mild", "summer": "warm", "harvest": "good", "rice_quality": "gohyakumangoku_solid"}',
 75, 'very_good', '{"from": 2021, "to": 2025}', 'stable', 'Solid Fukui quality; reliable clean, dry sake expression.', 2),

(50, 2021, 'Excellent rice season; fine sake across Fukui producers.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent", "rice_quality": "premium"}',
 83, 'very_good', '{"from": 2021, "to": 2027}', 'stable', 'Fine Fukui vintage; clean, mineral sake quality at its regional best.', 2),

(50, 2022, 'Benchmark year; outstanding rice quality across the prefecture.',
 '{"spring": "warm", "summer": "excellent", "harvest": "benchmark", "rice_quality": "exceptional"}',
 88, 'excellent', '{"from": 2022, "to": 2028}', 'stable', 'Excellent Fukui year; production from top kura is very impressive.', 2),

(50, 2023, 'Good conditions; classic Fukui dry sake style.',
 '{"spring": "mild", "summer": "warm", "harvest": "good", "rice_quality": "good"}',
 82, 'very_good', '{"from": 2023, "to": 2027}', 'stable', 'Good year; reliable, clean Fukui sake production.', 2),

-- ===== 51: UJI (宇治 Tea) =====
(51, 2019, 'Early spring warmth accelerated first flush; some heat stress reduced umami in gyokuro. Adequate but not exceptional.',
 '{"spring": "warm_early", "first_flush": "moderate_umami", "second_flush": "good", "shade_growing": "effective"}',
 72, 'good', '{"from": 2019, "to": 2022}', 'stable', 'Decent Uji year; gyokuro showed less umami depth than peak vintages but sencha was solid.', 1),

(51, 2020, 'Late spring start with cool temperatures; excellent umami development in gyokuro and tencha. Classic Uji quality.',
 '{"spring": "cool_late", "first_flush": "excellent_umami", "tencha": "outstanding", "shade_growing": "optimal_response"}',
 82, 'very_good', '{"from": 2020, "to": 2023}', 'stable', 'Classic Uji quality; the cool spring produced outstanding theanine levels in gyokuro.', 1),

(51, 2021, 'Ideal conditions; perfect April temperatures for slow, flavour-accumulating growth. Exceptional gyokuro and matcha.',
 '{"spring": "ideal_april", "first_flush": "exceptional", "tencha": "benchmark", "shade_growing": "perfect_conditions"}',
 88, 'excellent', '{"from": 2021, "to": 2024}', 'rising', 'Outstanding Uji vintage; gyokuro umami and matcha depth at their finest in years.', 1),

(51, 2022, 'Benchmark year; perfect spring temperature with optimal shade duration. Finest Uji tea in a decade.',
 '{"spring": "benchmark_cool", "first_flush": "finest_decade", "tencha": "exceptional_depth", "shade_growing": "ideal_20_day"}',
 94, 'exceptional', '{"from": 2022, "to": 2025}', 'rising', 'Landmark Uji vintage; 2022 gyokuro and ceremonial matcha are among the finest ever produced.', 1),

(51, 2023, 'Very good conditions; excellent gyokuro and tencha quality.',
 '{"spring": "good_temperatures", "first_flush": "very_good", "tencha": "excellent", "shade_growing": "effective"}',
 88, 'excellent', '{"from": 2023, "to": 2026}', 'stable', 'Excellent Uji year; outstanding value in both gyokuro and ceremonial matcha grades.', 1),

-- ===== 52: SHIZUOKA =====
(52, 2020, 'Good Shizuoka sencha season; Yabukita and Kanayamidori at reliable quality.',
 '{"spring": "mild", "first_flush": "good", "coastal_influence": "moderate", "mountain_teas": "strong"}',
 76, 'very_good', '{"from": 2020, "to": 2023}', 'stable', 'Reliable Shizuoka quality; the coastal mountain growing areas performed well.', 2),

(52, 2021, 'Excellent spring; fine sencha and shincha quality across the prefecture.',
 '{"spring": "ideal", "first_flush": "excellent_shincha", "coastal_influence": "positive", "mountain_teas": "outstanding"}',
 83, 'very_good', '{"from": 2021, "to": 2024}', 'stable', 'Fine Shizuoka year; shincha from the Oi River valley is particularly impressive.', 2),

(52, 2022, 'Outstanding; benchmark Shizuoka sencha vintage.',
 '{"spring": "benchmark", "first_flush": "exceptional", "coastal_influence": "ideal", "mountain_teas": "exceptional"}',
 89, 'excellent', '{"from": 2022, "to": 2025}', 'rising', 'Exceptional Shizuoka year; benchmark sencha from Kawane and Honyama areas.', 2),

(52, 2023, 'Very good conditions across the prefecture.',
 '{"spring": "warm_balanced", "first_flush": "very_good", "coastal_influence": "good", "mountain_teas": "good"}',
 85, 'very_good', '{"from": 2023, "to": 2026}', 'stable', 'Excellent Shizuoka vintage; broadly high quality across all growing zones.', 2),

-- ===== 53: KAGOSHIMA (Imo Shochu) =====
(53, 2020, 'Good sweet potato harvest across Kagoshima; Kogane Sengan and Murasaki Masari varieties at classic quality.',
 '{"spring": "warm", "summer": "hot", "harvest": "classic_imo", "sweet_potato": "good_yield"}',
 78, 'good', '{"from": 2021, "to": 2026}', 'stable', 'Solid Kagoshima imo shochu year; clean, umami-rich production from established kura.', 2),

(53, 2021, 'Excellent sweet potato season; characteristic rich, earthy-sweet shochu character.',
 '{"spring": "warm", "summer": "hot_sunny", "harvest": "excellent_imo", "sweet_potato": "premium_starch"}',
 83, 'very_good', '{"from": 2021, "to": 2027}', 'stable', 'Very good Kagoshima vintage; imo shochu showing classic regional character.', 2),

(53, 2022, 'Exceptional harvest; Kogane Sengan sweet potato at peak starch development.',
 '{"spring": "warm", "summer": "excellent_heat", "harvest": "exceptional_imo", "sweet_potato": "peak_quality"}',
 89, 'excellent', '{"from": 2022, "to": 2028}', 'stable', 'Outstanding Kagoshima year; benchmark imo shochu from leading kura like Satsuma Shuzo.', 2),

(53, 2023, 'Good harvest; reliable classic Kagoshima imo shochu production.',
 '{"spring": "mild", "summer": "warm", "harvest": "good_imo", "sweet_potato": "reliable_quality"}',
 83, 'very_good', '{"from": 2023, "to": 2027}', 'stable', 'Solid, reliable Kagoshima quality; good across all major imo shochu producers.', 2),

-- ===== 54: KAGOSHIMA SHOCHU (Honkaku) =====
(54, 2020, 'Good overall shochu production year; multiple base ingredients at reliable quality.',
 '{"spring": "warm", "summer": "hot", "harvest": "multi_ingredient", "quality": "solid"}',
 77, 'good', '{"from": 2021, "to": 2025}', 'stable', 'Solid year across the honkaku shochu category.', 2),

(54, 2021, 'Excellent conditions; rice and sweet potato shochu both performing at high level.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent_all_types", "quality": "premium"}',
 84, 'very_good', '{"from": 2021, "to": 2027}', 'stable', 'Very good multi-ingredient shochu year; clean and complex across all styles.', 2),

(54, 2022, 'Benchmark year; outstanding quality across all Kagoshima shochu production.',
 '{"spring": "warm", "summer": "exceptional_heat", "harvest": "benchmark", "quality": "exceptional"}',
 90, 'excellent', '{"from": 2022, "to": 2030}', 'rising', 'Landmark Kagoshima shochu year; aged expressions from 2022 will be highly prized.', 2),

(54, 2023, 'Very good conditions; reliable production from all major Kagoshima honkaku producers.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "quality": "excellent"}',
 85, 'very_good', '{"from": 2023, "to": 2028}', 'stable', 'Excellent Kagoshima vintage; broad quality across imo, rice and mugi styles.', 2),

-- ===== 55: OITA (Mugi Shochu) =====
(55, 2020, 'Good barley harvest in Oita; characteristic clean, mild mugi shochu.',
 '{"spring": "mild", "summer": "warm", "harvest": "good_barley", "quality": "classic_mild"}',
 76, 'very_good', '{"from": 2021, "to": 2025}', 'stable', 'Classic Oita mugi shochu; clean and light with characteristic barley softness.', 2),

(55, 2021, 'Excellent barley quality; outstanding clean, delicate mugi character.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent_barley", "quality": "premium_delicate"}',
 83, 'very_good', '{"from": 2021, "to": 2026}', 'stable', 'Very good Oita year; Iichiko and similar barley shochu showing fine light character.', 2),

(55, 2022, 'Exceptional barley year across Oita; finest mugi shochu in a decade.',
 '{"spring": "warm", "summer": "excellent", "harvest": "exceptional_barley", "quality": "finest_decade"}',
 88, 'excellent', '{"from": 2022, "to": 2028}', 'stable', 'Outstanding Oita vintage; Iichiko and Tantakatan at peak expression.', 2),

(55, 2023, 'Good barley production; solid classic mugi shochu style.',
 '{"spring": "mild", "summer": "warm", "harvest": "good", "quality": "solid_classic"}',
 82, 'very_good', '{"from": 2023, "to": 2027}', 'stable', 'Reliable Oita quality; classic mugi shochu at its characteristically approachable best.', 2),

-- ===== 56: OKINAWA (Awamori) =====
(56, 2020, 'Good Okinawan Indica rice year; classic Ryukyu-style awamori with characteristic long koji ageing potential.',
 '{"spring": "tropical_warm", "summer": "hot_humid", "harvest": "good_indica", "koji": "black_koji_active"}',
 75, 'very_good', '{"from": 2021, "to": 2030}', 'stable', 'Solid Okinawa awamori year; classic Ryukyu character with good kusu (aged) potential.', 2),

(56, 2021, 'Excellent conditions; Thai Indica rice at high quality for Okinawan distillation.',
 '{"spring": "tropical", "summer": "hot", "harvest": "excellent_indica", "koji": "optimal_black_koji"}',
 82, 'very_good', '{"from": 2022, "to": 2035}', 'stable', 'Fine Okinawa vintage; awamori will develop excellent kusu character with ageing.', 2),

(56, 2022, 'Outstanding awamori year; premium Indica rice with optimal black koji fermentation.',
 '{"spring": "warm_tropical", "summer": "excellent_tropical", "harvest": "premium_indica", "koji": "exceptional_black_koji"}',
 87, 'excellent', '{"from": 2022, "to": 2040}', 'rising', 'Exceptional Okinawa year; 2022 awamori will be outstanding as kusu after 10+ years.', 2),

(56, 2023, 'Good tropical conditions; reliable classic Okinawan awamori production.',
 '{"spring": "tropical", "summer": "warm_humid", "harvest": "good", "koji": "classic_black_koji"}',
 82, 'very_good', '{"from": 2024, "to": 2038}', 'stable', 'Solid Okinawa quality; reliable across all major awamori producers.', 2),

-- ===== 57: YUNNAN (Pu-erh Tea) =====
(57, 2019, 'Dry spring in Yunnan; lower first flush yield but ancient tree teas showed exceptional concentration.',
 '{"spring": "dry", "first_flush": "low_yield_concentrated", "gushu": "exceptional", "rain": "delayed"}',
 72, 'good', '{"from": 2024, "to": 2060}', 'rising', 'Lean but intense; 2019 Yunnan pu-erh from ancient trees will age exceptionally well.', 1),

(57, 2020, 'Excellent spring rains then dry harvest; benchmark conditions for Gushu ancient tree teas.',
 '{"spring": "good_rains", "first_flush": "excellent", "gushu": "benchmark", "rain": "ideal_timing"}',
 86, 'very_good', '{"from": 2024, "to": 2070}', 'rising', 'Outstanding 2020 Yunnan pu-erh; ancient tree teas showing remarkable complexity in early tastings.', 1),

(57, 2021, 'Good growing conditions; solid Yunnan pu-erh quality with characteristic earthy depth.',
 '{"spring": "adequate", "first_flush": "good", "gushu": "very_good", "rain": "sufficient"}',
 81, 'very_good', '{"from": 2023, "to": 2065}', 'stable', 'Reliable vintage; 2021 sheng pu-erh is developing well with good longevity.', 1),

(57, 2022, 'Outstanding ancient tree season; perfect spring moisture with dry late spring for concentration.',
 '{"spring": "excellent_rains", "first_flush": "concentrated", "gushu": "outstanding", "rain": "ideal_sequence"}',
 92, 'exceptional', '{"from": 2025, "to": 2080}', 'rising', 'Landmark Yunnan vintage; 2022 Gushu teas from Lao Banzhang and Bingdao will be legendary.', 1),

(57, 2023, 'Very good conditions; broad quality across Yunnan ancient tree regions.',
 '{"spring": "good", "first_flush": "very_good", "gushu": "excellent", "rain": "well_distributed"}',
 87, 'excellent', '{"from": 2024, "to": 2075}', 'stable', 'Excellent 2023 Yunnan; outstanding Gushu maocha from all key mountains.', 1),

-- ===== 58: FUJIAN (Oolong, White Tea) =====
(58, 2019, 'Good spring in Fujian; Tie Guan Yin and Da Hong Pao at classic quality.',
 '{"spring": "mild", "first_flush": "classic_quality", "yancha": "good", "white_tea": "good"}',
 79, 'good', '{"from": 2019, "to": 2025}', 'stable', 'Classic Fujian year; reliable Yancha rock oolong and Fujian white tea quality.', 1),

(58, 2020, 'Excellent spring temperatures; Wuyi rock oolong showing outstanding mineral character.',
 '{"spring": "cool_ideal", "first_flush": "excellent", "yancha": "exceptional_mineral", "white_tea": "very_good"}',
 86, 'very_good', '{"from": 2020, "to": 2028}', 'stable', 'Outstanding Fujian oolong year; Da Hong Pao and Rou Gui at their most mineral-complex.', 1),

(58, 2021, 'Very good conditions; classic Fujian terroir expression across all major styles.',
 '{"spring": "mild_good", "first_flush": "very_good", "yancha": "very_good", "white_tea": "excellent"}',
 83, 'very_good', '{"from": 2021, "to": 2028}', 'stable', 'Fine Fujian vintage; aged white tea from 2021 developing beautifully.', 1),

(58, 2022, 'Exceptional year; finest Wuyi rock oolong in a generation.',
 '{"spring": "benchmark_cool", "first_flush": "finest_generation", "yancha": "landmark", "white_tea": "outstanding"}',
 93, 'exceptional', '{"from": 2022, "to": 2035}', 'rising', 'Landmark Fujian year; 2022 Da Hong Pao from Zhengyan area will be collector-grade.', 1),

(58, 2023, 'Very good spring; excellent Yancha and Fuding white tea.',
 '{"spring": "good", "first_flush": "very_good", "yancha": "excellent", "white_tea": "very_good"}',
 87, 'excellent', '{"from": 2023, "to": 2032}', 'stable', 'Excellent Fujian vintage; outstanding value across all major styles.', 1),

-- ===== 59: ZHEJIANG (Longjing Dragon Well) =====
(59, 2019, 'Good Longjing year; mild spring produced classic chestnut-vegetal character in Dragon Well.',
 '{"spring": "mild", "first_flush": "classic_longjing", "qingming": "good_quality", "weather": "appropriate"}',
 78, 'good', '{"from": 2019, "to": 2022}', 'stable', 'Classic Longjing year; good pre-Qingming Dragon Well with characteristic chestnut sweetness.', 1),

(59, 2020, 'Excellent pre-Qingming conditions; finest single-bud Longjing with exceptional sweetness.',
 '{"spring": "cool_ideal", "first_flush": "excellent_prequingming", "qingming": "exceptional", "weather": "perfect_slow_growth"}',
 87, 'excellent', '{"from": 2020, "to": 2023}', 'rising', 'Outstanding Dragon Well year; pre-Qingming Longjing of exceptional sweetness and umami.', 1),

(59, 2021, 'Very good conditions; classic West Lake Dragon Well character.',
 '{"spring": "mild_good", "first_flush": "very_good", "qingming": "good", "weather": "classic"}',
 83, 'very_good', '{"from": 2021, "to": 2024}', 'stable', 'Fine Longjing year; West Lake terroir expressing cleanly and clearly.', 1),

(59, 2022, 'Benchmark pre-Qingming season; finest Longjing in a decade.',
 '{"spring": "benchmark_cool", "first_flush": "finest_decade", "qingming": "landmark", "weather": "perfect"}',
 93, 'exceptional', '{"from": 2022, "to": 2025}', 'rising', 'Landmark Dragon Well year; 2022 pre-Qingming from Xi Hu core area is peerless.', 1),

(59, 2023, 'Good spring; solid Dragon Well quality with classic character.',
 '{"spring": "moderate", "first_flush": "good", "qingming": "solid", "weather": "variable"}',
 82, 'very_good', '{"from": 2023, "to": 2025}', 'stable', 'Good Longjing year; dependable classic character from established producers.', 1),

-- ===== 60: GUANGDONG (Dan Cong Oolong) =====
(60, 2019, 'Good Phoenix Mountain Dan Cong season; characteristic honey orchid and duck shit aroma cultivars at classic quality.',
 '{"spring": "mild", "first_flush": "classic", "dancong": "honey_orchid_excellent", "altitude": "optimal"}',
 79, 'good', '{"from": 2019, "to": 2024}', 'stable', 'Classic Guangdong Dan Cong year; Phoenix Dancong expressing the characteristic cultivar aromas.', 1),

(60, 2020, 'Excellent Phoenix Mountain conditions; outstanding oolongs with complex floral-honey-stone fruit layering.',
 '{"spring": "ideal_cool", "first_flush": "outstanding", "dancong": "complex_layering", "altitude": "cloud_mist_ideal"}',
 86, 'very_good', '{"from": 2020, "to": 2028}', 'stable', 'Fine Guangdong year; Da Wu Ye and Mi Lan Xiang at their characteristic best.', 1),

(60, 2021, 'Very good Dan Cong conditions; aged oolong from 2021 developing complex complexity.',
 '{"spring": "mild_good", "first_flush": "very_good", "dancong": "aging_potential", "altitude": "good"}',
 82, 'very_good', '{"from": 2021, "to": 2030}', 'stable', 'Reliable Guangdong year; excellent potential for aged Phoenix Dan Cong.', 1),

(60, 2022, 'Outstanding Phoenix Mountain oolong season; finest decade.',
 '{"spring": "benchmark", "first_flush": "exceptional", "dancong": "finest_decade", "altitude": "cloud_mist_perfect"}',
 90, 'excellent', '{"from": 2022, "to": 2035}', 'rising', 'Landmark Guangdong year; 2022 Dan Cong from high-altitude Phoenix Mountain is superb.', 1),

(60, 2023, 'Very good conditions; high-quality Dan Cong across Phoenix Mountain.',
 '{"spring": "good", "first_flush": "very_good", "dancong": "excellent", "altitude": "consistent"}',
 85, 'very_good', '{"from": 2023, "to": 2030}', 'stable', 'Excellent year; Phoenix Dancong showing broad appeal and excellent quality.', 1),

-- ===== 61: GUIZHOU (Moutai/Baijiu) =====
(61, 2019, 'Good sorghum harvest in Renhuai; classic sauce-aroma (Jiangxiang) Maotai base material.',
 '{"spring": "mild", "summer": "warm", "harvest": "good_sorghum", "fermentation": "classic_jiangxiang"}',
 80, 'very_good', '{"from": 2024, "to": 2040}', 'stable', 'Classic Guizhou sorghum year; Maotai-town baijiu from 2019 production will mature excellently.', 1),

(61, 2020, 'Excellent Guizhou sorghum conditions; particularly fine Renhuai "red tassel" sorghum.',
 '{"spring": "warm", "summer": "ideal", "harvest": "excellent_red_sorghum", "fermentation": "optimal_quxiangqu"}',
 86, 'very_good', '{"from": 2025, "to": 2045}', 'rising', 'Fine Guizhou year; Kweichow Moutai production from 2020 showing outstanding promise.', 1),

(61, 2021, 'Very good Guizhou conditions; multi-round fermentation characteristic sauce aroma development.',
 '{"spring": "good", "summer": "warm", "harvest": "very_good", "fermentation": "multi_round_excellent"}',
 84, 'very_good', '{"from": 2026, "to": 2046}', 'stable', 'Reliable vintage; Guizhou baijiu from 2021 developing classic complex sauce-aroma.', 1),

(61, 2022, 'Outstanding sorghum year; finest red tassel sorghum quality from Renhuai terroir.',
 '{"spring": "warm", "summer": "excellent", "harvest": "outstanding_sorghum", "fermentation": "exceptional_environment"}',
 91, 'exceptional', '{"from": 2027, "to": 2060}', 'rising', 'Landmark Guizhou vintage; 2022-production Moutai will be outstanding at 5-15+ years.', 1),

(61, 2023, 'Very good conditions across Guizhou baijiu production region.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "fermentation": "classic_quality"}',
 86, 'very_good', '{"from": 2028, "to": 2048}', 'stable', 'Strong Guizhou year; reliable classic production across all Maotai-town distilleries.', 1),

-- ===== 62: SICHUAN (Luzhou/Wuliangye Baijiu) =====
(62, 2019, 'Good five-grain sorghum season in Luzhou; classic Nongxiang (strong aroma) character.',
 '{"spring": "warm", "summer": "hot", "harvest": "good_five_grain", "fermentation": "classic_nongxiang"}',
 79, 'good', '{"from": 2023, "to": 2038}', 'stable', 'Classic Sichuan nongxiang year; Wuliangye and Luzhou Laojiao production solid.', 1),

(62, 2020, 'Excellent five-grain harvest; particularly fine Luzhou pear-ester character development.',
 '{"spring": "good", "summer": "ideal", "harvest": "excellent_five_grain", "fermentation": "pear_ester_development"}',
 85, 'very_good', '{"from": 2024, "to": 2040}', 'stable', 'Fine Sichuan year; strong-aroma baijiu from 2020 showing excellent complexity.', 1),

(62, 2021, 'Very good season; consistent quality across Luzhou and Yibin baijiu production.',
 '{"spring": "mild", "summer": "warm", "harvest": "very_good", "fermentation": "consistent"}',
 83, 'very_good', '{"from": 2025, "to": 2042}', 'stable', 'Reliable Sichuan vintage; broad quality from Wuliangye to Jiannan Chun.', 1),

(62, 2022, 'Exceptional five-grain year; outstanding Wuliangye sorghum, wheat, corn, glutinous rice and rice blend.',
 '{"spring": "warm", "summer": "excellent", "harvest": "exceptional_all_grains", "fermentation": "outstanding_wupan"}',
 90, 'excellent', '{"from": 2026, "to": 2050}', 'rising', 'Landmark Sichuan year; 2022 Wuliangye production will be highly sought after at maturity.', 1),

(62, 2023, 'Good conditions; reliable nongxiang character across the baijiu belt.',
 '{"spring": "mild", "summer": "warm", "harvest": "good", "fermentation": "classic_nongxiang"}',
 83, 'very_good', '{"from": 2027, "to": 2043}', 'stable', 'Solid Sichuan year; dependable production from all major nongxiang producers.', 1),

-- ===== 63: CENTRAL TAIWAN HIGHLANDS (High Mountain Oolong) =====
(63, 2019, 'Good Ali Shan and Li Shan conditions; characteristic creamy, floral high mountain oolong.',
 '{"spring": "cool_highland", "first_flush": "good_floral", "altitude": "2000m_optimal", "cloud": "frequent_mist"}',
 74, 'very_good', '{"from": 2019, "to": 2025}', 'stable', 'Classic Taiwan high mountain oolong year; Ali Shan and Da Yu Ling at reliable quality.', 1),

(63, 2020, 'Excellent highland conditions; cool spring produced outstanding theanine-rich, buttery oolongs.',
 '{"spring": "ideal_cool", "first_flush": "exceptional_buttery", "altitude": "peak_expression", "cloud": "ideal_mist"}',
 88, 'excellent', '{"from": 2020, "to": 2028}', 'rising', 'Outstanding Taiwan high mountain year; Da Yu Ling and梨山 oolongs at their finest.', 1),

(63, 2021, 'Very good highland season; characteristic smooth, creamy texture in high elevation oolongs.',
 '{"spring": "mild_highland", "first_flush": "creamy_classic", "altitude": "very_good", "cloud": "good_coverage"}',
 84, 'very_good', '{"from": 2021, "to": 2027}', 'stable', 'Fine Taiwan vintage; high altitude oolong character expressing cleanly with good depth.', 1),

(63, 2022, 'Benchmark year; finest Taiwan high mountain oolong in a decade.',
 '{"spring": "benchmark_cool", "first_flush": "finest_decade", "altitude": "peak_performance", "cloud": "perfect_mist"}',
 94, 'exceptional', '{"from": 2022, "to": 2030}', 'rising', 'Landmark Taiwan vintage; 2022 Da Yu Ling and Ali Shan winter oolong will be legend.', 1),

(63, 2023, 'Excellent conditions; outstanding high mountain oolong across all key growing areas.',
 '{"spring": "good_highland", "first_flush": "very_good", "altitude": "very_good", "cloud": "regular_mist"}',
 89, 'excellent', '{"from": 2023, "to": 2030}', 'stable', 'Excellent Taiwan year; high mountain oolong at outstanding quality across all seasons.', 1),

-- ===== 64: DONG DING (Traditional Oolong) =====
(64, 2020, 'Good Dong Ding season; traditional jade oolong with characteristic chestnut-roasted character.',
 '{"spring": "mild", "first_flush": "classic_dongding", "roasting": "traditional_charcoal", "style": "classic"}',
 79, 'good', '{"from": 2020, "to": 2026}', 'stable', 'Classic Dong Ding year; traditional charcoal-roasted oolong expressing well.', 1),

(64, 2021, 'Very good conditions; excellent traditional style with characteristic Nantou County elegance.',
 '{"spring": "ideal", "first_flush": "excellent", "roasting": "optimal_charcoal", "style": "benchmark"}',
 84, 'very_good', '{"from": 2021, "to": 2028}', 'stable', 'Fine Dong Ding vintage; traditional charcoal roasting complementing excellent raw leaf.', 1),

(64, 2022, 'Exceptional year; finest Dong Ding quality in recent memory.',
 '{"spring": "benchmark", "first_flush": "exceptional", "roasting": "perfect_expression", "style": "landmark"}',
 90, 'excellent', '{"from": 2022, "to": 2032}', 'rising', 'Landmark Dong Ding year; traditional competition-grade oolong at its absolute peak.', 1),

(64, 2023, 'Good conditions; solid classic Dong Ding oolong production.',
 '{"spring": "moderate_good", "first_flush": "good", "roasting": "classic", "style": "traditional"}',
 82, 'very_good', '{"from": 2023, "to": 2028}', 'stable', 'Reliable year; classic Dong Ding at accessible quality and value.', 1),

-- ===== 65: DARJEELING =====
(65, 2019, 'Good first flush conditions; characteristic muscatel second flush.',
 '{"spring": "cool_mist", "first_flush": "good", "second_flush": "muscatel_good", "monsoon": "adequate"}',
 76, 'very_good', '{"from": 2019, "to": 2023}', 'stable', 'Classic Darjeeling year; first flush floral and second flush muscatel both at expected quality.', 1),

(65, 2020, 'Excellent first flush conditions; outstanding silver tip and white tea quality with fine floral character.',
 '{"spring": "ideal_cool", "first_flush": "exceptional", "second_flush": "very_good_muscatel", "monsoon": "ideal_timing"}',
 87, 'excellent', '{"from": 2020, "to": 2025}', 'rising', 'Outstanding Darjeeling year; 2020 first flush from top estates like Castleton and Makaibari exceptional.', 1),

(65, 2021, 'Very good conditions; solid first and second flush quality across the district.',
 '{"spring": "mild_mist", "first_flush": "very_good", "second_flush": "good_muscatel", "monsoon": "moderate"}',
 82, 'very_good', '{"from": 2021, "to": 2024}', 'stable', 'Fine Darjeeling vintage; broad quality across first and second flush production.', 1),

(65, 2022, 'Exceptional first flush; finest Darjeeling spring tea in a decade.',
 '{"spring": "benchmark_mist", "first_flush": "finest_decade", "second_flush": "exceptional_muscatel", "monsoon": "ideal"}',
 92, 'exceptional', '{"from": 2022, "to": 2026}', 'rising', 'Landmark Darjeeling year; 2022 first flush from upper Makaibari and Sungma is benchmark.', 1),

(65, 2023, 'Very good conditions across Darjeeling district.',
 '{"spring": "good_mist", "first_flush": "very_good", "second_flush": "strong_muscatel", "monsoon": "good_timing"}',
 86, 'very_good', '{"from": 2023, "to": 2026}', 'stable', 'Excellent Darjeeling year; very good first flush and outstanding muscatel second flush.', 1),

-- ===== 66: ASSAM =====
(66, 2020, 'Good Assam season; classic malty CTC and orthodox styles at reliable quality.',
 '{"spring": "warm", "first_flush": "classic_malty", "monsoon": "adequate", "orthodox": "good"}',
 76, 'very_good', '{"from": 2020, "to": 2024}', 'stable', 'Classic Assam year; reliable malty, robust character across CTC and orthodox production.', 1),

(66, 2021, 'Very good conditions; excellent tippy golden flowery orthodox quality.',
 '{"spring": "warm_humid", "first_flush": "excellent_tgfop", "monsoon": "good", "orthodox": "premium"}',
 83, 'very_good', '{"from": 2021, "to": 2025}', 'stable', 'Fine Assam year; TGFOP orthodox from Mokalbari and Mangalam outstanding.', 1),

(66, 2022, 'Exceptional Assam season; finest FTGFOP quality in recent years.',
 '{"spring": "ideal", "first_flush": "exceptional_ftgfop", "monsoon": "ideal_timing", "orthodox": "landmark"}',
 88, 'excellent', '{"from": 2022, "to": 2026}', 'rising', 'Outstanding Assam vintage; fine-tippy golden flowery from top estates exceptional.', 1),

(66, 2023, 'Good monsoon-season balance; solid Assam quality across all grades.',
 '{"spring": "warm", "first_flush": "good", "monsoon": "well_timed", "orthodox": "solid"}',
 83, 'very_good', '{"from": 2023, "to": 2026}', 'stable', 'Reliable Assam year; consistent quality from commercial to fine grades.', 1),

-- ===== 67: NILGIRI =====
(67, 2020, 'Good Nilgiri season; characteristic bright, citrus-fresh blue mountain character.',
 '{"spring": "cool_highland", "harvest": "good_bright", "monsoon": "adequate", "altitude": "optimal_cooling"}',
 75, 'very_good', '{"from": 2020, "to": 2024}', 'stable', 'Classic Nilgiri year; bright, refreshing blue mountain character.', 2),

(67, 2021, 'Very good highland conditions; fresh, floral Nilgiri with characteristic brightness.',
 '{"spring": "cool_mist", "harvest": "very_good", "monsoon": "good", "altitude": "ideal"}',
 81, 'very_good', '{"from": 2021, "to": 2024}', 'stable', 'Fine Nilgiri vintage; characteristic brightness and freshness well expressed.', 2),

(67, 2022, 'Excellent season; finest Nilgiri quality with outstanding citrus freshness.',
 '{"spring": "benchmark_cool", "harvest": "excellent", "monsoon": "ideal", "altitude": "optimal"}',
 86, 'very_good', '{"from": 2022, "to": 2025}', 'stable', 'Outstanding Nilgiri year; 2022 frost tea and winter flush showing exceptional brightness.', 2),

(67, 2023, 'Good conditions across the Nilgiri highlands.',
 '{"spring": "mild_highland", "harvest": "good", "monsoon": "moderate", "altitude": "good"}',
 80, 'very_good', '{"from": 2023, "to": 2025}', 'stable', 'Solid Nilgiri quality; reliable fresh, bright character.', 2),

-- ===== 77: YIRGACHEFFE (Ethiopian Coffee) =====
(77, 2019, 'Irregular rainfall timing in Yirgacheffe; cherry development delayed. Good but not exceptional crop.',
 '{"rainfall": "irregular_timing", "cherry_maturity": "adequate", "washing": "good_wet_process", "altitude": "1700_1900m"}',
 72, 'good', '{"from": 2020, "to": 2021}', 'stable', 'Adequate Yirgacheffe year; reliable jasmine-bergamot character in washed grades.', 1),

(77, 2020, 'Excellent growing season; precise rainfall timing produced exceptional cherry concentration.',
 '{"rainfall": "ideal_timing", "cherry_maturity": "excellent", "washing": "optimal_wet_process", "altitude": "peak_expression"}',
 88, 'excellent', '{"from": 2021, "to": 2022}', 'rising', 'Outstanding Yirgacheffe year; washed grades showing benchmark jasmine and bergamot character.', 1),

(77, 2021, 'Very good conditions; classic Yirgacheffe floral-citrus precision.',
 '{"rainfall": "good_timing", "cherry_maturity": "very_good", "washing": "classic_quality", "altitude": "consistent"}',
 84, 'very_good', '{"from": 2022, "to": 2023}', 'stable', 'Fine Yirgacheffe year; characteristic white flower and lemon verbena expression.', 1),

(77, 2022, 'Benchmark Yirgacheffe season; finest cherry quality in a decade.',
 '{"rainfall": "benchmark_timing", "cherry_maturity": "exceptional", "washing": "peak_quality", "altitude": "full_expression"}',
 93, 'exceptional', '{"from": 2023, "to": 2024}', 'rising', 'Landmark Yirgacheffe year; 2022 crop from Kochere and Gedeb washing stations is extraordinary.', 1),

(77, 2023, 'Excellent conditions; outstanding washed and natural Yirgacheffe across key cooperatives.',
 '{"rainfall": "ideal", "cherry_maturity": "excellent", "washing": "very_good_quality", "altitude": "high_expression"}',
 89, 'excellent', '{"from": 2024, "to": 2025}', 'stable', 'Excellent Yirgacheffe crop; YCFCU cooperatives producing benchmark specialty grade.', 1),

-- ===== 78: SIDAMA =====
(78, 2019, 'Good Sidama harvest; classic Bensa and Banko Gotiti washing stations at reliable quality.',
 '{"rainfall": "adequate", "cherry_maturity": "good", "washing": "classic_sidama", "altitude": "1500_2200m"}',
 71, 'good', '{"from": 2020, "to": 2021}', 'stable', 'Classic Sidama year; reliable berry and citrus character in washed grades.', 1),

(78, 2020, 'Excellent Sidama conditions; outstanding Ardi natural and washed Sidamo production.',
 '{"rainfall": "excellent_timing", "cherry_maturity": "outstanding", "washing": "peak_natural_washed", "altitude": "optimal"}',
 87, 'excellent', '{"from": 2021, "to": 2022}', 'rising', 'Outstanding Sidama year; Guji and Sidama naturals exceptional; washed clean and complex.', 1),

(78, 2021, 'Very good conditions across Sidama Zone.',
 '{"rainfall": "good", "cherry_maturity": "very_good", "washing": "very_good_quality", "altitude": "consistent"}',
 83, 'very_good', '{"from": 2022, "to": 2023}', 'stable', 'Fine Sidama vintage; characteristic blueberry and jasmine character in top lots.', 1),

(78, 2022, 'Benchmark year; finest Sidama specialty coffee in recent memory.',
 '{"rainfall": "benchmark", "cherry_maturity": "finest_recent", "washing": "exceptional", "altitude": "full_expression"}',
 91, 'exceptional', '{"from": 2023, "to": 2024}', 'rising', 'Landmark Sidama crop; 2022 Bensa and Shantawene washing stations producing extraordinary coffee.', 1),

(78, 2023, 'Excellent Sidama harvest; outstanding quality from multiple washing stations.',
 '{"rainfall": "ideal", "cherry_maturity": "excellent", "washing": "high_quality", "altitude": "good_expression"}',
 87, 'excellent', '{"from": 2024, "to": 2025}', 'stable', 'Excellent Sidama year; natural and washed both performing at high quality.', 1),

-- ===== 79: HARRAR =====
(79, 2019, 'Good wild-harvested Harrar crop; characteristic wild blueberry and mocha dry-processed character.',
 '{"rainfall": "adequate", "wild_harvest": "good", "natural_process": "classic_harrar", "altitude": "1500_2100m"}',
 73, 'good', '{"from": 2020, "to": 2021}', 'stable', 'Classic Harrar year; dry-processed wild coffee at characteristic blueberry-mocha quality.', 1),

(79, 2020, 'Excellent growing conditions; outstanding wild Harrar cherry with exceptional natural fermentation.',
 '{"rainfall": "ideal", "wild_harvest": "exceptional", "natural_process": "outstanding_ferment", "altitude": "high_altitude_prime"}',
 86, 'very_good', '{"from": 2021, "to": 2022}', 'rising', 'Outstanding Harrar year; wild-harvested Long Berry Harrar at its finest character.', 1),

(79, 2021, 'Very good Harrar season; reliable wild blueberry and dark chocolate notes.',
 '{"rainfall": "good", "wild_harvest": "very_good", "natural_process": "classic_quality", "altitude": "consistent"}',
 82, 'very_good', '{"from": 2022, "to": 2023}', 'stable', 'Fine Harrar year; classic dry-processed wild coffee at expected high quality.', 1),

(79, 2022, 'Benchmark year; finest Long Berry Harrar in a decade.',
 '{"rainfall": "benchmark", "wild_harvest": "finest_decade", "natural_process": "exceptional_ferment", "altitude": "full_expression"}',
 90, 'excellent', '{"from": 2023, "to": 2024}', 'rising', 'Landmark Harrar crop; 2022 natural process Long Berry from Harrar highlands is extraordinary.', 1),

(79, 2023, 'Excellent conditions; outstanding dry-processed Harrar across the growing region.',
 '{"rainfall": "ideal_timing", "wild_harvest": "excellent", "natural_process": "very_good_clean", "altitude": "high_expression"}',
 87, 'excellent', '{"from": 2024, "to": 2025}', 'stable', 'Excellent Harrar year; classic wild-fermented blueberry character at its best.', 1);

COMMIT;
