BEGIN;

-- ============================================================
-- VINTAGE DATA: TRADITIONAL CULTURAL BEVERAGE REGIONS
-- Regions: 68-76 (Kava, Awa, Ava, Lambanog, Basi, Palm Wine,
--                  Matango, Clairin, Yaqona)
-- These represent annual harvest/production quality assessments.
-- ============================================================

INSERT INTO beverage_vintages
  (region_id, vintage_year, season_narrative, conditions, quality_rating,
   quality_descriptor, drinking_window, price_trajectory, value_assessment, authority_tier)
VALUES

-- ===== 68: VANUATU KAVA =====
(68, 2019, 'Good Piper methysticum growing season on Tanna; adequate rainfall with dry harvest period. Borogu and Melomelo cultivars at reliable kavalactone levels.',
 '{"rainfall": "adequate", "harvest": "dry_good", "kavalactone": "reliable", "cultivar": "borogu_melomelo"}',
 79, 'good', '{"from": 2020, "to": 2022}', 'stable', 'Solid Vanuatu kava year; classic nakamal-ceremony quality from established farms.', 2),

(68, 2020, 'Excellent growing conditions on Tanna; extended dry period enhanced kavalactone concentration. Premium shell quality reported by leading nakamals.',
 '{"rainfall": "excellent_timing", "harvest": "extended_dry", "kavalactone": "high_concentration", "cultivar": "premium_noble"}',
 86, 'very_good', '{"from": 2021, "to": 2023}', 'rising', 'Outstanding Vanuatu kava harvest; 2020 Borogu showing exceptional potency and earthy depth.', 2),

(68, 2021, 'Very good conditions; noble cultivars at strong kavalactone levels with characteristic peppery profile.',
 '{"rainfall": "good", "harvest": "dry_ideal", "kavalactone": "very_good", "cultivar": "noble_quality"}',
 83, 'very_good', '{"from": 2022, "to": 2024}', 'stable', 'Fine Vanuatu year; shell quality consistently high across Santo and Tanna farms.', 2),

(68, 2022, 'Exceptional kava harvest; finest Tanna Noble cultivar quality in recent years.',
 '{"rainfall": "benchmark", "harvest": "exceptional_dry", "kavalactone": "exceptional", "cultivar": "finest_noble"}',
 90, 'excellent', '{"from": 2023, "to": 2025}', 'rising', 'Landmark Vanuatu harvest; 2022 Borogu recognised as exceptional by Pacific kava authorities.', 2),

(68, 2023, 'Good harvest conditions; reliable export-quality noble kava production.',
 '{"rainfall": "adequate", "harvest": "good", "kavalactone": "consistent_high", "cultivar": "noble_export"}',
 82, 'very_good', '{"from": 2024, "to": 2026}', 'stable', 'Solid year; Nakamal at Home and Tanna Kava Growers maintaining premium export standards.', 2),

-- ===== 69: FIJI YAQONA =====
(69, 2020, 'Good Fijian growing season; Waka (lateral root) kava of reliable quality across Viti Levu farms.',
 '{"rainfall": "adequate", "harvest": "good_waka", "kavalactone": "reliable_fiji", "ceremonial": "high_quality"}',
 76, 'very_good', '{"from": 2021, "to": 2023}', 'stable', 'Classic Fiji yaqona quality; ceremonial Waka root at reliable potency for traditional use.', 3),

(69, 2021, 'Excellent growing conditions; premium Waka and Lewena grades at strong kavalactone levels.',
 '{"rainfall": "excellent", "harvest": "excellent_waka", "kavalactone": "high", "ceremonial": "outstanding"}',
 83, 'very_good', '{"from": 2022, "to": 2024}', 'stable', 'Fine Fiji year; ceremonial-grade Waka at outstanding quality for diplomatic reception use.', 3),

(69, 2022, 'Very good conditions; solid yaqona production with consistent quality.',
 '{"rainfall": "good", "harvest": "very_good", "kavalactone": "solid", "ceremonial": "reliable"}',
 80, 'very_good', '{"from": 2023, "to": 2025}', 'stable', 'Reliable Fiji kava; yaqona ceremony tradition maintained at high standard.', 3),

(69, 2023, 'Good season; Waka root quality maintaining Fiji''s ceremonial standard.',
 '{"rainfall": "moderate", "harvest": "good_waka", "kavalactone": "good", "ceremonial": "traditional_quality"}',
 78, 'good', '{"from": 2024, "to": 2026}', 'stable', 'Solid Fiji yaqona year; ceremonial and export grades both at expected quality.', 3),

-- ===== 70: HAWAII AWA =====
(70, 2020, 'Good Hawaiian awa growing season; Mahakea cultivar at classic quality with characteristic gentle numbing and floral notes.',
 '{"rainfall": "adequate", "harvest": "classic_mahakea", "kavalactone": "gentle_mild", "cultivar": "mahakea_floral"}',
 78, 'good', '{"from": 2021, "to": 2023}', 'stable', 'Classic Hawaiian awa year; Mahakea cultivar at its characteristic mild, floral quality.', 2),

(70, 2021, 'Excellent Oahu growing conditions; outstanding Mahakea with premium floral and earthy character.',
 '{"rainfall": "excellent", "harvest": "premium_mahakea", "kavalactone": "excellent_profile", "cultivar": "certified_hawaiian"}',
 85, 'very_good', '{"from": 2022, "to": 2024}', 'rising', 'Outstanding Hawaiian awa year; Lehua Hawaiian Kava achieving exceptional traditional quality.', 2),

(70, 2022, 'Benchmark Hawaiian awa season; finest Mahakea quality in recent years.',
 '{"rainfall": "ideal", "harvest": "benchmark", "kavalactone": "exceptional_floral", "cultivar": "finest_mahakea"}',
 89, 'excellent', '{"from": 2023, "to": 2025}', 'rising', 'Landmark Hawaii awa harvest; 2022 ceremonial grade is among the finest produced in modern cultivation.', 2),

(70, 2023, 'Very good conditions; premium Hawaiian awa at traditional ceremonial standard.',
 '{"rainfall": "good", "harvest": "very_good", "kavalactone": "traditional_quality", "cultivar": "mahakea_solid"}',
 82, 'very_good', '{"from": 2024, "to": 2026}', 'stable', 'Excellent Hawaiian awa year; Lehua''s stone-ground ceremony preparations at high quality.', 2),

-- ===== 71: SAMOA AVA =====
(71, 2020, 'Good Samoan ava season; fa''afia root quality maintained for traditional ceremony.',
 '{"rainfall": "adequate", "harvest": "good_faafia", "preparation": "tanoa_classic", "ceremony": "high_standard"}',
 76, 'very_good', '{"from": 2021, "to": 2023}', 'stable', 'Classic Samoan ava year; fa''asamoa ceremonial preparation at traditional quality.', 3),

(71, 2021, 'Excellent growing conditions; premium ava root quality for chiefly ceremony.',
 '{"rainfall": "excellent", "harvest": "premium_root", "preparation": "fau_bark_optimal", "ceremony": "distinguished"}',
 83, 'very_good', '{"from": 2022, "to": 2024}', 'stable', 'Fine Samoa year; ava ceremony tradition maintained at distinguished ceremonial standard.', 3),

(71, 2022, 'Outstanding ava harvest; finest ceremonial root quality in recent years.',
 '{"rainfall": "ideal", "harvest": "exceptional_root", "preparation": "benchmark_ceremony", "ceremony": "outstanding"}',
 88, 'excellent', '{"from": 2023, "to": 2025}', 'stable', 'Landmark Samoan ava year; 2022 harvest supporting finest diplomatic and ceremonial preparations.', 3),

(71, 2023, 'Good ava growing season; consistent ceremonial quality across Upolu and Savai''i.',
 '{"rainfall": "good", "harvest": "solid_quality", "preparation": "traditional_standard", "ceremony": "reliable"}',
 79, 'good', '{"from": 2024, "to": 2026}', 'stable', 'Solid Samoa year; ava ceremony tradition strong across both main islands.', 3),

-- ===== 72: QUEZON PROVINCE LAMBANOG =====
(72, 2019, 'Good nipa palm sap season in Quezon Province; triple-distilled lambanog at classic coconut fresh character.',
 '{"rainfall": "adequate", "palm_sap": "good_yield", "distillation": "triple_classic", "abv": "40_45pct"}',
 77, 'good', '{"from": 2020, "to": 2023}', 'stable', 'Classic Quezon lambanog year; clean, fresh coconut character at traditional 40-45% ABV.', 3),

(72, 2020, 'Excellent nipa palm harvest; outstanding sap quality with elevated natural sugars for premium spirit.',
 '{"rainfall": "excellent", "palm_sap": "elevated_sugars", "distillation": "premium_triple", "abv": "premium_expression"}',
 85, 'very_good', '{"from": 2021, "to": 2024}', 'rising', 'Outstanding lambanog year; Barako Distillery''s 2020 production particularly clean and aromatic.', 3),

(72, 2021, 'Very good conditions; premium nipa palm sap with characteristic floral sweetness.',
 '{"rainfall": "good", "palm_sap": "floral_premium", "distillation": "excellent_triple", "abv": "classic_43pct"}',
 82, 'very_good', '{"from": 2022, "to": 2025}', 'stable', 'Fine Quezon lambanog year; exceptional botanical freshness and clean finish.', 3),

(72, 2022, 'Benchmark season; finest nipa palm sap quality in recent years.',
 '{"rainfall": "ideal", "palm_sap": "finest_sugars", "distillation": "benchmark_triple", "abv": "optimal"}',
 88, 'excellent', '{"from": 2023, "to": 2026}', 'rising', 'Landmark Quezon Province year; 2022 lambanog at the pinnacle of traditional coconut spirit production.', 3),

(72, 2023, 'Good nipa palm season; reliable classic lambanog production.',
 '{"rainfall": "adequate", "palm_sap": "reliable_quality", "distillation": "classic_triple", "abv": "traditional_range"}',
 80, 'very_good', '{"from": 2024, "to": 2026}', 'stable', 'Solid Quezon year; traditional lambanog craftsmanship maintained at high standard.', 3),

-- ===== 73: ILOCOS REGION BASI =====
(73, 2019, 'Good Ilocos sugarcane harvest; Basi fermentation with Duhat bark and native herbs at classic quality.',
 '{"rainfall": "adequate", "sugarcane": "classic_ilocos", "bark_herbs": "traditional_blend", "fermentation": "earthen_jar"}',
 76, 'very_good', '{"from": 2021, "to": 2026}', 'stable', 'Classic Ilocos Basi year; pre-colonial production tradition maintained by Felicitas Winery.', 3),

(73, 2020, 'Excellent sugarcane growing conditions; rich, complex Basi with deep dried-fig and bark character.',
 '{"rainfall": "excellent", "sugarcane": "high_brix", "bark_herbs": "premium_duhat", "fermentation": "extended_complex"}',
 84, 'very_good', '{"from": 2022, "to": 2028}', 'rising', 'Outstanding Ilocos Basi year; 2020 production showing exceptional complexity and longevity.', 3),

(73, 2021, 'Very good sugarcane season; characteristic deep garnet Basi with tamarind and dark fruit depth.',
 '{"rainfall": "good", "sugarcane": "premium_quality", "bark_herbs": "well_sourced", "fermentation": "classic_ilocano"}',
 81, 'very_good', '{"from": 2023, "to": 2027}', 'stable', 'Fine Basi year; traditional Ilocano fermentation technique producing complex character.', 3),

(73, 2022, 'Benchmark Basi season; finest Ilocos sugarcane and herb quality.',
 '{"rainfall": "ideal", "sugarcane": "finest_brix", "bark_herbs": "exceptional_duhat", "fermentation": "benchmark_earthen"}',
 88, 'excellent', '{"from": 2024, "to": 2032}', 'rising', 'Landmark Ilocos Basi year; 2022 production represents UNESCO intangible heritage at its finest.', 3),

(73, 2023, 'Good growing conditions; reliable traditional Basi quality.',
 '{"rainfall": "adequate", "sugarcane": "solid_yield", "bark_herbs": "traditional", "fermentation": "classic_quality"}',
 79, 'good', '{"from": 2025, "to": 2030}', 'stable', 'Solid Ilocos year; pre-colonial production tradition maintained at reliable quality.', 3),

-- ===== 74: NIGERIA PALM WINE BELT =====
(74, 2020, 'Good Raphia palm tapping season in Cross-River State; abundant natural fermentation with characteristic coconut sap sweetness.',
 '{"rainfall": "adequate", "palm_health": "good", "tapping": "traditional_seasonal", "freshness": "within_24h"}',
 78, 'good', '{"from": 2020, "to": 2020}', 'unavailable', 'Classic Nigerian palm wine year; natural effervescence and tropical freshness at traditional quality.', 3),

(74, 2021, 'Excellent palm growth conditions; abundant Raphia forest yield with outstanding natural carbonation.',
 '{"rainfall": "excellent", "palm_health": "very_good", "tapping": "peak_season", "freshness": "maximum_effervescence"}',
 83, 'very_good', '{"from": 2021, "to": 2021}', 'unavailable', 'Outstanding Cross-River palm wine; maximum natural carbonation and sweet-sour complexity.', 3),

(74, 2022, 'Good tapping season; reliable fresh palm wine production from old-growth forest palms.',
 '{"rainfall": "good", "palm_health": "healthy", "tapping": "established_trees", "freshness": "high_quality"}',
 80, 'very_good', '{"from": 2022, "to": 2022}', 'unavailable', 'Solid Nigerian year; fresh palm wine from Cross-River State at traditional quality.', 3),

(74, 2023, 'Very good growing conditions; exceptional Raphia palm health with abundant sap.',
 '{"rainfall": "very_good", "palm_health": "exceptional", "tapping": "peak_yield", "freshness": "outstanding"}',
 85, 'very_good', '{"from": 2023, "to": 2023}', 'unavailable', 'Fine Nigerian palm wine year; outstanding natural effervescence and fresh tropical character.', 3),

-- ===== 75: CAMEROON MATANGO =====
(75, 2020, 'Good Pisang Mas banana growing season in West Cameroon Highlands; Matango of classic ripe banana and mild tartness.',
 '{"rainfall": "adequate", "banana_ripeness": "classic_overripe", "fermentation": "natural_yeast", "region": "bamileke_highlands"}',
 77, 'good', '{"from": 2020, "to": 2022}', 'stable', 'Classic Cameroon Matango year; traditional Bamileke banana wine at characteristic ripe-fruit quality.', 3),

(75, 2021, 'Excellent growing conditions; outstanding Pisang Mas ripeness with elevated sugar concentration.',
 '{"rainfall": "excellent", "banana_ripeness": "peak_overripe", "fermentation": "active_natural", "region": "bafoussam_optimal"}',
 83, 'very_good', '{"from": 2021, "to": 2023}', 'stable', 'Fine Matango year; exceptional sugar development producing richer banana wine character.', 3),

(75, 2022, 'Very good banana season; characteristic caramelised sweetness and light tartness well balanced.',
 '{"rainfall": "good", "banana_ripeness": "very_good", "fermentation": "well_balanced", "region": "consistent_highlands"}',
 80, 'very_good', '{"from": 2022, "to": 2024}', 'stable', 'Solid Cameroon year; Matango expressing the Bamileke highland tradition reliably.', 3),

(75, 2023, 'Outstanding Pisang Mas harvest; benchmark Matango quality with exceptional aromatic complexity.',
 '{"rainfall": "ideal", "banana_ripeness": "exceptional", "fermentation": "benchmark_natural", "region": "west_cameroon_peak"}',
 87, 'excellent', '{"from": 2023, "to": 2025}', 'rising', 'Landmark Cameroon Matango year; 2023 production recognised for outstanding quality and authenticity.', 3),

-- ===== 76: HAITI CLAIRIN =====
(76, 2019, 'Good sugarcane harvest in rural Haiti; artisanal clairin of classic fresh, grassy, wild-fermented character.',
 '{"rainfall": "adequate", "sugarcane": "traditional_varieties", "fermentation": "wild_open_vat", "distillation": "direct_fire"}',
 78, 'good', '{"from": 2020, "to": 2025}', 'stable', 'Classic Haitian clairin year; artisanal production from Sajous and Casimir at characteristic quality.', 2),

(76, 2020, 'Excellent Haitian growing season; premium sugarcane juice with exceptional wild fermentation complexity.',
 '{"rainfall": "excellent", "sugarcane": "premium_juice", "fermentation": "complex_wild", "distillation": "artisanal_excellence"}',
 87, 'excellent', '{"from": 2021, "to": 2028}', 'rising', 'Outstanding Clairin year; 2020 production showing remarkable terroir expression and wild complexity.', 2),

(76, 2021, 'Very good conditions; distinctive regional terroir expressions from Clairin Sajous, Casimir and Vaval.',
 '{"rainfall": "good", "sugarcane": "very_good_quality", "fermentation": "complex_regional", "distillation": "traditional"}',
 83, 'very_good', '{"from": 2022, "to": 2027}', 'stable', 'Fine Haitian clairin year; regional terroir distinctions increasingly apparent.', 2),

(76, 2022, 'Benchmark clairin season; finest artisanal production quality in recent years.',
 '{"rainfall": "ideal", "sugarcane": "exceptional_terroir", "fermentation": "exceptional_wild", "distillation": "benchmark"}',
 91, 'exceptional', '{"from": 2023, "to": 2032}', 'rising', 'Landmark Haitian year; 2022 clairin is extraordinary — finest production from all three major producers.', 2),

(76, 2023, 'Good sugarcane growing season; reliable artisanal clairin production.',
 '{"rainfall": "adequate", "sugarcane": "solid_quality", "fermentation": "reliable_wild", "distillation": "traditional_quality"}',
 82, 'very_good', '{"from": 2024, "to": 2029}', 'stable', 'Solid Haitian clairin year; artisanal production maintaining quality and regional distinctiveness.', 2);

COMMIT;
