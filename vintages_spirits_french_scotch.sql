BEGIN;

-- ============================================================
-- VINTAGE DATA: SPIRITS + FRENCH WINE + SCOTCH WHISKY
-- Regions: 156 Cognac, 157 Armagnac, 158 Normandy, 159 Provence
--          95 Speyside, 96 Islay, 97 Highland, 98 Campbeltown
--          82 Kentucky Bourbon, 83 Tennessee Whiskey
--          99 Oaxaca Mezcal, 100 Jalisco Tequila
--          101 Belgium, 102 Bavaria, 103 Rhine/Cologne
--          183 Morocco, 184 Turkey
-- ============================================================

INSERT INTO beverage_vintages
  (region_id, vintage_year, season_narrative, conditions, quality_rating,
   quality_descriptor, drinking_window, price_trajectory, value_assessment, authority_tier)
VALUES

-- ===== 156: COGNAC =====
(156, 2018, 'Hot, dry summer with ideal ripeness across Grande and Petite Champagne; high natural sugar accumulation produced eaux-de-vie of exceptional concentration and early aromatic complexity.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "early_ideal", "frost": "minimal"}',
 90, 'excellent', '{"from": 2033, "to": 2060}', 'rising', 'Exceptional distillation year; 2018 Cognac eaux-de-vie already showing outstanding character in young releases.', 1),

(156, 2019, 'Irregular season with some rain during harvest; yields lower than average but concentration high in the premier crus. Well-structured eaux-de-vie with good longevity potential.',
 '{"spring": "cool_wet", "summer": "variable", "harvest": "mixed", "frost": "none"}',
 82, 'very_good', '{"from": 2030, "to": 2055}', 'stable', 'Solid, classic vintage with good structure; not as showy as 2018 but reliable depth.', 1),

(156, 2020, 'Warm, generous summer; moderately dry conditions allowed full phenolic ripeness. Highly aromatic eaux-de-vie with notable floral and fruit character.',
 '{"spring": "warm", "summer": "warm_dry", "harvest": "generous", "frost": "none"}',
 86, 'very_good', '{"from": 2031, "to": 2056}', 'stable', 'Generous, approachable eaux-de-vie with strong aromatic appeal; excellent for younger expression blends.', 1),

(156, 2021, 'Cold spring with late frost damage reduced yields; summer recovered well. Small crop of highly concentrated eaux-de-vie with intense character.',
 '{"spring": "cold_frost", "summer": "good_recovery", "harvest": "small_concentrated", "frost": "late_spring"}',
 84, 'very_good', '{"from": 2032, "to": 2057}', 'rising', 'Low yields created intense concentration; 2021 will be sought after as it ages.', 1),

(156, 2022, 'Exceptional drought summer; highest heat accumulation in decades. Record sugar levels but some stress visible. Outstanding aromatic intensity in resulting eaux-de-vie.',
 '{"spring": "warm", "summer": "extreme_heat_drought", "harvest": "record_sugars", "frost": "none"}',
 88, 'excellent', '{"from": 2032, "to": 2058}', 'rising', 'Extreme vintage with powerful character; 2022 will be a landmark year for Cognac.', 1),

(156, 2023, 'More balanced season after 2022 extremes; moderate heat with adequate rainfall. Classic, well-proportioned eaux-de-vie with good natural acidity and fruit.',
 '{"spring": "mild", "summer": "moderate", "harvest": "classic_balanced", "frost": "light"}',
 85, 'very_good', '{"from": 2030, "to": 2055}', 'stable', 'A return to classic balance after 2022 extremes; dependable quality across all crus.', 1),

-- ===== 157: ARMAGNAC =====
(157, 2018, 'Hot dry summer across Bas-Armagnac and Ténarèze; Ugni Blanc and Folle Blanche achieved ideal ripeness. Rich, concentrated eaux-de-vie with characteristic Gascon depth.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "excellent", "frost": "none"}',
 91, 'exceptional', '{"from": 2028, "to": 2065}', 'rising', 'One of the finest Armagnac vintages of the decade; extraordinary concentration and complexity.', 1),

(157, 2019, 'Some rain during harvest but overall good quality; lighter, more elegant style than 2018. Good acidity preserved natural character.',
 '{"spring": "variable", "summer": "mixed", "harvest": "rain_at_harvest", "frost": "none"}',
 80, 'very_good', '{"from": 2026, "to": 2050}', 'stable', 'Lighter but elegant; approachable earlier than big vintages.', 1),

(157, 2020, 'Warm season with excellent conditions; generous yields in Bas-Armagnac. Classic character with good aromatic complexity.',
 '{"spring": "warm", "summer": "warm", "harvest": "generous", "frost": "none"}',
 85, 'very_good', '{"from": 2027, "to": 2052}', 'stable', 'Classic, generous Armagnac vintage with immediate appeal.', 1),

(157, 2021, 'Frost damage in spring reduced yields; concentrated, intensely flavoured eaux-de-vie as a result.',
 '{"spring": "cold_frost", "summer": "recovery", "harvest": "small_concentrated", "frost": "late_spring"}',
 83, 'very_good', '{"from": 2028, "to": 2053}', 'rising', 'Small but intense; concentration from low yields will reward patience.', 1),

(157, 2022, 'Extreme heat and drought; record ripeness levels. Powerful, concentrated eaux-de-vie with exceptional ageing potential.',
 '{"spring": "warm", "summer": "extreme_heat", "harvest": "record_ripeness", "frost": "none"}',
 89, 'excellent', '{"from": 2030, "to": 2060}', 'rising', 'A landmark hot year; 2022 Armagnac will be highly sought after.', 1),

(157, 2023, 'Balanced recovery year; good natural acidity and approachable character.',
 '{"spring": "mild", "summer": "moderate_warm", "harvest": "balanced", "frost": "none"}',
 84, 'very_good', '{"from": 2026, "to": 2050}', 'stable', 'Solid, classic vintage with broad appeal and good value.', 1),

-- ===== 158: NORMANDY (CALVADOS) =====
(158, 2018, 'Excellent apple harvest; warm, dry summer encouraged full fruit development in Pays d''Auge orchards. Concentrated, intensely fruity Calvados with great ageing potential.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "excellent_concentration", "frost": "minimal"}',
 88, 'excellent', '{"from": 2028, "to": 2058}', 'stable', 'Outstanding Calvados vintage; 2018 will be a landmark year for Pays d''Auge producers.', 1),

(158, 2019, 'Cool, wet summer challenged growers but quality producers achieved good concentration through green harvesting. Good acidity, elegant style.',
 '{"spring": "cool", "summer": "cool_wet", "harvest": "selective_harvesting", "frost": "none"}',
 78, 'good', '{"from": 2025, "to": 2048}', 'stable', 'Leaner vintage; best results from producers who green-harvested for concentration.', 1),

(158, 2020, 'Warm, generous summer; excellent apple ripeness across Calvados regions. Full, rounded Calvados with characteristic Normandy apple richness.',
 '{"spring": "mild", "summer": "warm", "harvest": "generous_ripe", "frost": "none"}',
 84, 'very_good', '{"from": 2026, "to": 2052}', 'stable', 'Generous, approachable vintage with excellent early drinking character.', 1),

(158, 2021, 'Severe spring frosts in May devastated some orchards; very small crop of concentrated fruit. Intense, powerful distillate.',
 '{"spring": "severe_frost", "summer": "recovery", "harvest": "tiny_concentrated", "frost": "may_frost"}',
 82, 'very_good', '{"from": 2028, "to": 2055}', 'rising', 'Tiny crop of exceptional concentration; 2021 will be rare and sought after.', 1),

(158, 2022, 'Hot drought summer; richest Normandy apple harvest in many years. Record sugar and flavour concentration.',
 '{"spring": "dry", "summer": "hot_drought", "harvest": "record_richness", "frost": "none"}',
 87, 'excellent', '{"from": 2027, "to": 2055}', 'rising', 'Rich, powerful Calvados year; exceptional concentration and complexity.', 1),

(158, 2023, 'Balanced season with adequate rainfall; good natural apple acidity. Classic, well-structured Calvados.',
 '{"spring": "mild", "summer": "balanced", "harvest": "classic_balance", "frost": "none"}',
 83, 'very_good', '{"from": 2025, "to": 2050}', 'stable', 'Return to classic Calvados balance after two extreme years.', 1),

-- ===== 159: PROVENCE =====
(159, 2018, 'Near-perfect conditions; warm, dry summer with cooling Mistral winds preventing excess heat stress. Elegant, concentrated rosé and red wines of exceptional quality.',
 '{"spring": "warm", "summer": "warm_mistral", "harvest": "ideal", "frost": "none"}',
 92, 'exceptional', '{"from": 2019, "to": 2030}', 'rising', 'A benchmark Provence vintage; 2018 rosé and reds show unmatched elegance and depth.', 1),

(159, 2019, 'Warm season with some late summer heat; very good concentration and aromatic intensity. One of the finest rosé vintages of the decade.',
 '{"spring": "warm", "summer": "hot", "harvest": "excellent", "frost": "none"}',
 89, 'excellent', '{"from": 2019, "to": 2028}', 'stable', 'Outstanding rosé vintage; 2019 Bandol shows exceptional structure and ageing potential.', 1),

(159, 2020, 'Hot, dry conditions produced generous, full-bodied wines; highest quality in the Coteaux d''Aix. Bold red wines with good cellaring potential.',
 '{"spring": "dry", "summer": "hot_dry", "harvest": "generous_full", "frost": "none"}',
 87, 'excellent', '{"from": 2019, "to": 2030}', 'stable', 'Rich, generous style across the appellation; powerful Bandol reds for long ageing.', 1),

(159, 2021, 'Cooler, more classic season with good natural acidity; elegant, refined wines with characteristic Provence minerality.',
 '{"spring": "cool", "summer": "moderate", "harvest": "classic_elegant", "frost": "none"}',
 84, 'very_good', '{"from": 2019, "to": 2027}', 'stable', 'Classic, restrained Provence; lower alcohol with better freshness than recent hot years.', 1),

(159, 2022, 'Extreme drought and heat; lowest yields in decades but exceptional concentration in surviving fruit. Powerful, structured wines.',
 '{"spring": "warm", "summer": "extreme_drought", "harvest": "tiny_powerful", "frost": "none"}',
 86, 'very_good', '{"from": 2022, "to": 2035}', 'rising', 'Extreme vintage with powerful character; best Bandol reds will be remarkable.', 1),

(159, 2023, 'Balanced season; good Mistral influence during harvest kept freshness in the wines. Excellent aromatic precision in rosé.',
 '{"spring": "mild", "summer": "moderate_mistral", "harvest": "fresh_precise", "frost": "none"}',
 88, 'excellent', '{"from": 2023, "to": 2032}', 'stable', 'Elegant, precise Provence; 2023 rosé is particularly successful with superb freshness.', 1),

-- ===== 95: SPEYSIDE =====
(95, 2013, 'Warm, wet autumn; good barley quality with high starch levels. Speyside distilleries produced particularly floral, honeyed new-make spirit.',
 '{"spring": "variable", "summer": "mild", "harvest": "good_barley", "peat": "minimal"}',
 84, 'very_good', '{"from": 2023, "to": 2045}', 'stable', 'Classic Speyside character; now entering prime drinking window at 10+ years.', 1),

(95, 2015, 'Good harvest year; high-quality Scottish barley with excellent fermentable sugars. Well-balanced Speyside new make with characteristic fruit-forward character.',
 '{"spring": "mild", "summer": "warm", "harvest": "excellent_barley", "peat": "minimal"}',
 86, 'very_good', '{"from": 2025, "to": 2048}', 'stable', 'Excellent base materials; 10-year expressions from 2015 are showing fine quality.', 1),

(95, 2017, 'Exceptional Scottish barley harvest; warm summer with ideal moisture balance. One of the finest years for Speyside distillation in the decade.',
 '{"spring": "good", "summer": "warm_balanced", "harvest": "exceptional_barley", "peat": "light"}',
 91, 'exceptional', '{"from": 2027, "to": 2055}', 'rising', 'Landmark distillation year; 2017 spirit will be highly prized at 12-18 years.', 1),

(95, 2019, 'Cool, wet summer; lower barley sugar but excellent complex fermentation character. More restrained, elegant style.',
 '{"spring": "mild", "summer": "cool_wet", "harvest": "moderate_barley", "peat": "minimal"}',
 82, 'very_good', '{"from": 2029, "to": 2050}', 'stable', 'Elegant, nuanced spirit with good structure; will develop well in cask.', 1),

(95, 2021, 'Warm, dry summer produced high-quality barley with good starch levels. Classic, well-structured new make spirit.',
 '{"spring": "mild", "summer": "warm_dry", "harvest": "high_quality_barley", "peat": "minimal"}',
 85, 'very_good', '{"from": 2031, "to": 2052}', 'stable', 'Solid, classic Speyside year; good foundation material for long cask development.', 1),

-- ===== 96: ISLAY =====
(96, 2013, 'Good peat harvest conditions; high phenol levels in Islay barley with ideal Atlantic moisture influence. Rich, intensely smoky new make spirit.',
 '{"spring": "Atlantic_cool", "summer": "mild_moist", "harvest": "high_phenol_barley", "peat": "intense"}',
 87, 'excellent', '{"from": 2023, "to": 2048}', 'stable', '10-year expressions now showing excellent integration of peat and fruit; fine quality.', 1),

(96, 2015, 'Classic Islay season; balanced maritime conditions with good barley quality. Well-integrated peaty character in new make.',
 '{"spring": "maritime", "summer": "balanced_Atlantic", "harvest": "classic_barley", "peat": "classic"}',
 84, 'very_good', '{"from": 2025, "to": 2047}', 'stable', 'Classic, balanced Islay character; 10-year bottlings from 2015 are very good.', 1),

(96, 2017, 'Outstanding barley harvest; warm summer enabled high phenol extraction with excellent spirit character. One of the finest recent Islay vintages.',
 '{"spring": "good", "summer": "warm", "harvest": "outstanding_barley", "peat": "high"}',
 90, 'excellent', '{"from": 2027, "to": 2052}', 'rising', 'Excellent distillation year; 2017 Islay spirit promises outstanding 12-18 year expressions.', 1),

(96, 2019, 'Cool, Atlantic-influenced season; elegant, complex spirit with fine medicinal and maritime notes.',
 '{"spring": "cool_Atlantic", "summer": "cool_moist", "harvest": "elegant_barley", "peat": "moderate"}',
 83, 'very_good', '{"from": 2029, "to": 2050}', 'stable', 'More restrained, complex style; will develop beautifully with extended cask time.', 1),

(96, 2021, 'Good quality year; high phenol barley with classic Islay maritime influence.',
 '{"spring": "Atlantic_mild", "summer": "variable", "harvest": "good_quality", "peat": "classic"}',
 85, 'very_good', '{"from": 2031, "to": 2052}', 'stable', 'Reliable, classic Islay character; good foundation for long-aged expressions.', 1),

-- ===== 97: HIGHLAND =====
(97, 2013, 'Good Highland barley year; cooler conditions produced elegant, complex new make with characteristic Highland fruit and heather character.',
 '{"spring": "cool", "summer": "mild", "harvest": "classic_highland", "peat": "variable"}',
 83, 'very_good', '{"from": 2023, "to": 2045}', 'stable', 'Classic Highland character; 10-year expressions show good development.', 1),

(97, 2015, 'Warm summer for the Highlands; higher-than-usual sugar levels in barley. Rich, fruit-forward style with excellent ageing potential.',
 '{"spring": "mild", "summer": "warm_highland", "harvest": "rich_barley", "peat": "light_variable"}',
 86, 'very_good', '{"from": 2025, "to": 2048}', 'stable', 'Warmer-than-usual year produced richer, more generous Highland character.', 1),

(97, 2017, 'Exceptional harvest; warm, dry summer with ideal barley development. Outstanding new make across Highland distilleries.',
 '{"spring": "good", "summer": "warm_dry", "harvest": "exceptional", "peat": "variable"}',
 89, 'excellent', '{"from": 2027, "to": 2055}', 'rising', 'Outstanding Highland vintage; 2017 spirit across the region shows exceptional promise.', 1),

(97, 2019, 'Classic cool Highland season; elegant, nuanced spirit with good natural acidity and complexity.',
 '{"spring": "cool", "summer": "mild_wet", "harvest": "moderate", "peat": "light"}',
 81, 'very_good', '{"from": 2029, "to": 2048}', 'stable', 'More restrained, classical style; elegant and understated.', 1),

(97, 2021, 'Good barley year with solid spirit quality across the region.',
 '{"spring": "mild", "summer": "moderate", "harvest": "good_highland", "peat": "variable"}',
 84, 'very_good', '{"from": 2031, "to": 2052}', 'stable', 'Reliable Highland quality; solid foundation for all expression styles.', 1),

-- ===== 98: CAMPBELTOWN =====
(98, 2013, 'Classic Campbeltown conditions; briny Atlantic influence with good barley. Characteristic sea-salt and old cellar notes in new make.',
 '{"spring": "maritime", "summer": "cool_Atlantic", "harvest": "classic_barley", "peat": "moderate"}',
 84, 'very_good', '{"from": 2023, "to": 2045}', 'stable', 'Classic Campbeltown brine and orchard character; 10-year expressions are excellent.', 1),

(98, 2015, 'Warm, dry summer unusual for Campbeltown; produced richer, sweeter new make than typical.',
 '{"spring": "mild", "summer": "warm_dry", "harvest": "richer_than_usual", "peat": "light"}',
 85, 'very_good', '{"from": 2025, "to": 2048}', 'stable', 'Atypically rich, generous Campbeltown; interesting contrast to the classic briny style.', 1),

(98, 2017, 'Outstanding barley harvest; excellent spirit across Springbank and Glen Scotia.',
 '{"spring": "good", "summer": "warm", "harvest": "outstanding", "peat": "moderate"}',
 88, 'excellent', '{"from": 2027, "to": 2052}', 'rising', 'One of the finest recent Campbeltown vintages; highly anticipated at maturity.', 1),

(98, 2019, 'Classic cool, briny season; archetypal Campbeltown character with fine saline and orchard notes.',
 '{"spring": "Atlantic_cool", "summer": "cool_moist", "harvest": "classic_campbeltown", "peat": "moderate"}',
 83, 'very_good', '{"from": 2029, "to": 2050}', 'stable', 'Textbook Campbeltown; the definitive expression of the region''s maritime character.', 1),

(98, 2021, 'Good quality year; consistent spirit character across the small number of active distilleries.',
 '{"spring": "mild", "summer": "variable", "harvest": "solid_quality", "peat": "moderate"}',
 82, 'very_good', '{"from": 2031, "to": 2050}', 'stable', 'Reliable, solid Campbeltown; good foundation for aged expressions.', 1),

-- ===== 82: KENTUCKY BOURBON =====
(82, 2018, 'Hot, dry Kentucky summer; exceptional corn crop with high starch and sugar levels. Bourbon new make of remarkable richness and sweet character.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "exceptional_corn", "frost": "minimal"}',
 91, 'exceptional', '{"from": 2022, "to": 2035}', 'rising', 'Outstanding corn quality; 4-year and 8-year expressions from 2018 are excellent.', 1),

(82, 2019, 'Good harvest with balanced moisture; classic Kentucky bourbon character with excellent vanilla and caramel development.',
 '{"spring": "warm", "summer": "warm_balanced", "harvest": "classic_corn", "frost": "none"}',
 85, 'very_good', '{"from": 2023, "to": 2033}', 'stable', 'Classic, well-balanced Kentucky bourbon vintage; broad appeal.', 1),

(82, 2020, 'Warm, wet summer produced high-yielding corn crop with good fermentable sugar; reliable bourbon quality.',
 '{"spring": "warm", "summer": "humid", "harvest": "high_yield", "frost": "none"}',
 83, 'very_good', '{"from": 2024, "to": 2032}', 'stable', 'Consistent, dependable quality; excellent for high-proof expressions.', 1),

(82, 2021, 'Dry summer with excellent heat accumulation; concentrated grain flavour in new make bourbon.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "concentrated_grain", "frost": "none"}',
 87, 'excellent', '{"from": 2025, "to": 2034}', 'stable', 'Excellent grain concentration; 4-6 year releases from 2021 show rich character.', 1),

(82, 2022, 'Record summer temperatures; highest-ever sugar concentration in Kentucky corn. Exceptionally rich, sweet new make.',
 '{"spring": "dry", "summer": "record_heat", "harvest": "record_corn_sugars", "frost": "none"}',
 89, 'excellent', '{"from": 2026, "to": 2037}', 'rising', 'Record corn quality year; 2022 bourbon distillates will be prized at 6-10 years.', 1),

(82, 2023, 'Balanced return to normal conditions; good moisture with warm summer. Classic Kentucky bourbon quality.',
 '{"spring": "mild", "summer": "warm_balanced", "harvest": "classic_quality", "frost": "none"}',
 84, 'very_good', '{"from": 2027, "to": 2035}', 'stable', 'Classic vintage; dependable Kentucky bourbon character across all distilleries.', 1),

-- ===== 83: TENNESSEE WHISKEY =====
(83, 2018, 'Excellent Tennessee grain harvest; hot, dry summer produced exceptional corn with high fermentable sugar. Lincoln County Process filtering enhanced the already superior base.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "excellent_grain", "lincoln_county": "optimal_filtering"}',
 90, 'excellent', '{"from": 2022, "to": 2034}', 'stable', 'Outstanding grain year; Tennessee whiskey from 2018 showing exceptional mellowness at 5+ years.', 1),

(83, 2019, 'Good Tennessee summer; classic corn and rye crop quality. Well-balanced new make with characteristic Tennessee smoothness.',
 '{"spring": "warm", "summer": "warm", "harvest": "classic_quality", "lincoln_county": "standard_filtering"}',
 84, 'very_good', '{"from": 2023, "to": 2032}', 'stable', 'Classic Tennessee character; smooth and approachable in the Jack Daniel''s tradition.', 1),

(83, 2020, 'Hot, humid summer; reliable grain quality. Consistent Tennessee whiskey production.',
 '{"spring": "warm", "summer": "hot_humid", "harvest": "reliable", "lincoln_county": "effective"}',
 82, 'very_good', '{"from": 2024, "to": 2031}', 'stable', 'Dependable quality; good value across all Tennessee whiskey expressions.', 1),

(83, 2021, 'Warm, dry Tennessee summer; excellent corn concentration. One of the finer recent grain harvests.',
 '{"spring": "mild", "summer": "warm_dry", "harvest": "concentrated_corn", "lincoln_county": "charcoal_excellent"}',
 86, 'very_good', '{"from": 2025, "to": 2033}', 'stable', 'Fine grain quality; 2021 Tennessee whiskey shows exceptional maple-vanilla development.', 1),

(83, 2022, 'Extreme heat year; record grain sugar levels. Tennessee whiskey distillates of exceptional richness.',
 '{"spring": "dry", "summer": "extreme_heat", "harvest": "record_sugars", "lincoln_county": "filtering_optimal"}',
 88, 'excellent', '{"from": 2026, "to": 2036}', 'rising', 'Outstanding grain year; 2022 will be a landmark Tennessee whiskey vintage.', 1),

(83, 2023, 'Return to more balanced conditions; good natural grain quality with classic Tennessee character.',
 '{"spring": "mild", "summer": "warm", "harvest": "classic_balanced", "lincoln_county": "standard"}',
 83, 'very_good', '{"from": 2027, "to": 2034}', 'stable', 'Classic, dependable vintage; broad commercial and quality appeal.', 1),

-- ===== 99: OAXACA MEZCAL =====
(99, 2018, 'Strong rainy season followed by dry harvest; ideal for Espadín and wild agave maturation. Exceptional batch quality across small Oaxacan palenques.',
 '{"rainy_season": "strong", "dry_season": "ideal_harvest", "agave_maturity": "excellent", "wild_agave": "high_quality"}',
 89, 'excellent', '{"from": 2018, "to": 2030}', 'rising', 'Outstanding palenque year; artisanal mezcal from 2018 batches shows exceptional terroir expression.', 1),

(99, 2019, 'Moderate rainfall; good agave development with characteristic Oaxacan minerality. Solid production year for artisanal producers.',
 '{"rainy_season": "moderate", "dry_season": "good", "agave_maturity": "good", "wild_agave": "adequate"}',
 84, 'very_good', '{"from": 2019, "to": 2028}', 'stable', 'Classic Oaxacan mezcal character; reliable quality across all production styles.', 1),

(99, 2020, 'Excellent growing conditions; agave reached exceptional maturity levels. Many wild varietals at peak ripeness.',
 '{"rainy_season": "excellent", "dry_season": "long", "agave_maturity": "peak", "wild_agave": "exceptional"}',
 91, 'exceptional', '{"from": 2020, "to": 2032}', 'rising', 'Exceptional wild agave year; 2020 Tepeztate and Tobalá expressions are outstanding.', 1),

(99, 2021, 'Irregular rainfall challenged wild agave producers; cultivated Espadín more reliable. Variable quality.',
 '{"rainy_season": "irregular", "dry_season": "variable", "agave_maturity": "variable", "wild_agave": "challenged"}',
 78, 'good', '{"from": 2021, "to": 2026}', 'stable', 'Variable year; best results from experienced palenqueros with wild agave expertise.', 1),

(99, 2022, 'Good conditions overall; solid Espadín maturity and interesting wild variety production.',
 '{"rainy_season": "good", "dry_season": "adequate", "agave_maturity": "good", "wild_agave": "solid"}',
 85, 'very_good', '{"from": 2022, "to": 2030}', 'stable', 'Good Oaxacan vintage; reliable quality from established producers.', 1),

(99, 2023, 'Classic Oaxacan season; excellent agave ripeness across Santiago Matatlán and surrounding areas.',
 '{"rainy_season": "classic", "dry_season": "ideal", "agave_maturity": "excellent", "wild_agave": "high_quality"}',
 87, 'excellent', '{"from": 2023, "to": 2032}', 'stable', 'Excellent quality across the Oaxacan mezcal heartland; artisanal production shines.', 1),

-- ===== 100: JALISCO TEQUILA =====
(100, 2018, 'Excellent agave year in the Jalisco highlands; warm summer with adequate rainfall produced agave at peak sugar concentration (28+ Brix). Highland producers particularly benefited.',
 '{"rainfall": "adequate", "temperature": "warm_highland", "brix_level": "high_28plus", "highland_quality": "exceptional"}',
 91, 'exceptional', '{"from": 2019, "to": 2030}', 'rising', 'Landmark tequila year; 2018 highland blue agave reached exceptional maturity and concentration.', 1),

(100, 2019, 'Good conditions in both highland and lowland regions; classic tequila character with balanced fruit and mineral character.',
 '{"rainfall": "moderate", "temperature": "warm", "brix_level": "good_26", "highland_quality": "excellent"}',
 86, 'very_good', '{"from": 2019, "to": 2028}', 'stable', 'Classic, balanced Jalisco vintage; reliable quality across all major producers.', 1),

(100, 2020, 'Warm, dry Jalisco summer; high sugar concentration in agave. Rich, cooked-agave character in resulting tequilas.',
 '{"rainfall": "below_average", "temperature": "hot_dry", "brix_level": "very_high_27", "highland_quality": "excellent"}',
 88, 'excellent', '{"from": 2020, "to": 2030}', 'stable', 'Rich, concentrated agave year; cooked-agave sweetness particularly prominent.', 1),

(100, 2021, 'Irregular rainfall in some subregions; highland areas maintained quality while lowland producers had variable results.',
 '{"rainfall": "irregular", "temperature": "variable", "brix_level": "moderate_24", "highland_quality": "good"}',
 82, 'very_good', '{"from": 2021, "to": 2028}', 'stable', 'Variable year; highland producers outperformed lowland counterparts.', 1),

(100, 2022, 'Strong summer with good agave development; solid across the region.',
 '{"rainfall": "adequate", "temperature": "warm", "brix_level": "good_26", "highland_quality": "very_good"}',
 85, 'very_good', '{"from": 2022, "to": 2030}', 'stable', 'Good, classic Jalisco quality; broad commercial appeal.', 1),

(100, 2023, 'Excellent conditions; high-altitude agave ripened beautifully with characteristic minerality and citrus.',
 '{"rainfall": "good", "temperature": "warm_highland", "brix_level": "high_27", "highland_quality": "outstanding"}',
 89, 'excellent', '{"from": 2023, "to": 2032}', 'rising', 'Outstanding recent vintage; 2023 highland tequila is particularly impressive.', 1),

-- ===== 101: BELGIUM =====
(101, 2018, 'Warm Belgian summer; Trappist abbeys and lambic producers reported excellent fermentation conditions. Spontaneous fermentation of lambic wort particularly active.',
 '{"spring": "warm", "summer": "hot_dry", "fermentation": "excellent_spontaneous", "hop_quality": "good"}',
 89, 'excellent', '{"from": 2021, "to": 2035}', 'stable', 'Landmark Belgian year; 2018 lambic vintages are exceptional, 2018 Trappist ales outstanding.', 1),

(101, 2019, 'Cool summer moderated fermentation; elegant, complex lambic character with fine acidity.',
 '{"spring": "mild", "summer": "cool", "fermentation": "slow_complex", "hop_quality": "classic"}',
 83, 'very_good', '{"from": 2022, "to": 2033}', 'stable', 'Elegant, nuanced Belgian year; excellent for traditional gueuze development.', 1),

(101, 2020, 'Very warm Belgian summer; unusual intensity in spontaneous fermentations. Bold, complex lambic and strong ale character.',
 '{"spring": "warm", "summer": "hot", "fermentation": "vigorous_complex", "hop_quality": "very_good"}',
 87, 'excellent', '{"from": 2023, "to": 2036}', 'stable', 'Rich, intense Belgian vintage; 2020 lambic will be exceptional at 5-10 years.', 1),

(101, 2021, 'Classic, balanced Belgian season; good conditions for both Trappist and lambic production.',
 '{"spring": "mild", "summer": "moderate", "fermentation": "classic_balanced", "hop_quality": "good"}',
 84, 'very_good', '{"from": 2024, "to": 2034}', 'stable', 'Reliable, classic Belgian year; excellent across all styles.', 1),

(101, 2022, 'Hot, dry summer; remarkable fermentation intensity with high attenuation and complex wild yeast activity.',
 '{"spring": "warm", "summer": "hot_dry", "fermentation": "intense_attenuation", "hop_quality": "very_good"}',
 88, 'excellent', '{"from": 2025, "to": 2038}', 'rising', 'Outstanding fermentation year; 2022 Belgian lambic will be a collector''s item.', 1),

(101, 2023, 'Good, classic Belgian summer; solid fermentation conditions across all abbey and lambic producers.',
 '{"spring": "mild", "summer": "warm", "fermentation": "good_classic", "hop_quality": "very_good"}',
 85, 'very_good', '{"from": 2026, "to": 2035}', 'stable', 'Classic Belgian quality; dependable excellence across all styles.', 1),

-- ===== 102: BAVARIA =====
(102, 2018, 'Excellent Bavarian barley and hop harvest; warm summer produced high-quality Hallertau hops with rich aromatic profile. Outstanding year for Helles, Märzen and Weissbier.',
 '{"spring": "warm", "summer": "hot_dry", "barley_quality": "excellent", "hop_quality": "hallertau_exceptional"}',
 90, 'excellent', '{"from": 2018, "to": 2023}', 'stable', 'Outstanding Bavarian brewing year; 2018 vintage beers from major Munich breweries are benchmark.', 1),

(102, 2019, 'Good Bavarian season; classic hop and barley quality with characteristic Reinheitsgebot purity.',
 '{"spring": "mild", "summer": "warm", "barley_quality": "good", "hop_quality": "classic_hallertau"}',
 84, 'very_good', '{"from": 2019, "to": 2023}', 'stable', 'Classic Bavarian quality; excellent across all styles from Weihenstephan to Paulaner.', 1),

(102, 2020, 'Warm, productive summer; high-quality Hallertau aroma hops with excellent myrcene and linalool content.',
 '{"spring": "warm", "summer": "warm", "barley_quality": "very_good", "hop_quality": "high_aromatic_oils"}',
 86, 'very_good', '{"from": 2020, "to": 2024}', 'stable', 'Very good brewing year; highly aromatic hops produced exceptional Hefeweizen and lager.', 1),

(102, 2021, 'Cool, wet summer reduced hop yields but quality remained high; elegant, aromatic character.',
 '{"spring": "cool", "summer": "cool_wet", "barley_quality": "good", "hop_quality": "lower_yield_high_quality"}',
 82, 'very_good', '{"from": 2021, "to": 2025}', 'stable', 'Lighter, more delicate Bavarian year; refined hop aromatics.', 1),

(102, 2022, 'Extreme heat damaged some hop yards; lower hop yield but intense aromatic concentration in survivors.',
 '{"spring": "warm", "summer": "extreme_heat", "barley_quality": "good", "hop_quality": "low_yield_intense"}',
 83, 'very_good', '{"from": 2022, "to": 2025}', 'stable', 'Challenging hop year managed well by experienced Bavarian maltsters.', 1),

(102, 2023, 'Good recovery year; excellent Hallertau hop harvest with classic aromatic profile.',
 '{"spring": "mild", "summer": "warm_balanced", "barley_quality": "excellent", "hop_quality": "classic_excellent"}',
 87, 'excellent', '{"from": 2023, "to": 2026}', 'stable', 'Excellent return to form; 2023 will be a benchmark year for Bavarian brewing.', 1),

-- ===== 103: RHINE & COLOGNE =====
(103, 2018, 'Hot Rhine summer; excellent brewing conditions for Kölsch and Altbier. Pilsner malt quality outstanding; Hallertau and Tettnang hops showed exceptional character.',
 '{"spring": "warm", "summer": "hot", "rye_quality": "excellent", "hop_quality": "tettnang_exceptional"}',
 88, 'excellent', '{"from": 2018, "to": 2023}', 'stable', 'Outstanding Cologne/Düsseldorf brewing year; classic Kölsch and Altbier at their finest.', 1),

(103, 2019, 'Classic Rhine season; reliable hop and barley quality. Good Kölsch and Altbier character.',
 '{"spring": "mild", "summer": "moderate", "rye_quality": "good", "hop_quality": "classic_tettnang"}',
 83, 'very_good', '{"from": 2019, "to": 2023}', 'stable', 'Reliable quality; classic Rhine brewing character across all Cologne breweries.', 1),

(103, 2020, 'Warm, productive summer; rich hop character with excellent brewing conditions.',
 '{"spring": "warm", "summer": "warm", "rye_quality": "very_good", "hop_quality": "aromatic_rich"}',
 85, 'very_good', '{"from": 2020, "to": 2024}', 'stable', 'Very good Rhine brewing vintage; aromatic hop expression particularly notable.', 1),

(103, 2021, 'Cooler season with more moderate character; elegant, refined Kölsch style.',
 '{"spring": "cool", "summer": "mild", "rye_quality": "good", "hop_quality": "delicate_classic"}',
 81, 'very_good', '{"from": 2021, "to": 2024}', 'stable', 'Delicate, refined Rhine beer year; classic Kölsch at its most elegant.', 1),

(103, 2022, 'Extreme heat stress on hop yards; challenging year managed by experienced brewers.',
 '{"spring": "warm", "summer": "extreme_heat", "rye_quality": "good", "hop_quality": "stressed_lower_yield"}',
 80, 'good', '{"from": 2022, "to": 2024}', 'stable', 'Challenging year; experienced Cologne brewers maintained quality through skill.', 1),

(103, 2023, 'Excellent recovery; good Rhine hop and malt quality across the region.',
 '{"spring": "mild", "summer": "warm", "rye_quality": "excellent", "hop_quality": "classic_excellent"}',
 86, 'very_good', '{"from": 2023, "to": 2026}', 'stable', 'Fine return to form; 2023 Kölsch and Altbier show excellent freshness and character.', 1),

-- ===== 183: MOROCCO =====
(183, 2018, 'Excellent Moroccan vintage; warm summer with Mediterranean influence along northern coast. Cabernet Sauvignon and Syrah from Meknes reached outstanding ripeness.',
 '{"spring": "warm", "summer": "hot_mediterranean", "harvest": "excellent_ripeness", "altitude": "optimal_cooling"}',
 87, 'excellent', '{"from": 2020, "to": 2030}', 'stable', 'Outstanding Moroccan vintage; 2018 Meknes reds show exceptional depth and Atlas foothill character.', 2),

(183, 2019, 'Good harvest conditions; Atlas mountain-cooled vineyards performed well with characteristic freshness.',
 '{"spring": "mild", "summer": "warm", "harvest": "good_balance", "altitude": "good_cooling"}',
 82, 'very_good', '{"from": 2021, "to": 2028}', 'stable', 'Solid Moroccan vintage; high-altitude producers led quality.', 2),

(183, 2020, 'Warm, dry Moroccan summer; rich, generous wines with good fruit concentration.',
 '{"spring": "warm", "summer": "hot_dry", "harvest": "concentrated", "altitude": "beneficial"}',
 84, 'very_good', '{"from": 2022, "to": 2030}', 'stable', 'Rich, generous vintage; good value from Meknes and Guerrouane appellations.', 2),

(183, 2021, 'Variable vintage; coastal regions outperformed interior. Good but not exceptional.',
 '{"spring": "variable", "summer": "hot_interior", "harvest": "variable_by_zone", "altitude": "important"}',
 79, 'good', '{"from": 2022, "to": 2027}', 'stable', 'Variable quality; coastal and high-altitude producers outperformed interior zones.', 2),

(183, 2022, 'Exceptional heat year; record temperatures challenged all regions but concentrated fruit quality was outstanding.',
 '{"spring": "hot", "summer": "extreme_heat", "harvest": "concentrated_challenged", "altitude": "critical_cooling"}',
 83, 'very_good', '{"from": 2023, "to": 2032}', 'stable', 'Heat year managed well by experienced Atlas foothill producers.', 2),

(183, 2023, 'Good, classic Moroccan vintage; solid conditions across the northern wine belt.',
 '{"spring": "mild", "summer": "warm", "harvest": "classic_quality", "altitude": "good"}',
 83, 'very_good', '{"from": 2024, "to": 2030}', 'stable', 'Solid, reliable Moroccan quality; good value from Meknes producers.', 2),

-- ===== 184: TURKEY =====
(184, 2018, 'Exceptional Turkish vintage; Thrace and Aegean regions benefited from Mediterranean heat moderated by sea breezes. Indigenous varieties Öküzgözü and Boğazkere at peak ripeness.',
 '{"spring": "warm", "summer": "hot_sea_moderated", "harvest": "exceptional_indigenous", "region": "thrace_aegean_optimal"}',
 89, 'excellent', '{"from": 2020, "to": 2033}', 'rising', 'Landmark Turkish vintage; 2018 Öküzgözü and Boğazkere show extraordinary depth and complexity.', 2),

(184, 2019, 'Good conditions across major wine regions; consistent quality from Thrace, Cappadocia and Aegean.',
 '{"spring": "mild", "summer": "warm", "harvest": "consistent_good", "region": "multi_region_balance"}',
 83, 'very_good', '{"from": 2021, "to": 2028}', 'stable', 'Reliable Turkish quality; indigenous varieties showing increasing refinement.', 2),

(184, 2020, 'Warm, productive Turkish summer; rich, full-bodied reds from Cappadocia and Eastern Anatolia.',
 '{"spring": "warm", "summer": "hot", "harvest": "full_bodied", "region": "cappadocia_excellent"}',
 85, 'very_good', '{"from": 2022, "to": 2030}', 'stable', 'Strong vintage across regions; Cappadocian Kalecik Karası particularly impressive.', 2),

(184, 2021, 'Classic, balanced Turkish season; good across all wine-growing areas.',
 '{"spring": "mild", "summer": "warm_balanced", "harvest": "classic_balance", "region": "consistent_all"}',
 82, 'very_good', '{"from": 2023, "to": 2028}', 'stable', 'Classic Turkish year; balanced expression of indigenous varieties.', 2),

(184, 2022, 'Hot, dry year across Turkey; powerful, concentrated wines especially from eastern Anatolia.',
 '{"spring": "dry", "summer": "hot_drought", "harvest": "powerful_concentrated", "region": "eastern_anatolia_strong"}',
 86, 'very_good', '{"from": 2024, "to": 2035}', 'rising', 'Powerful, concentrated vintage; 2022 Boğazkere will be exceptional at 5+ years.', 2),

(184, 2023, 'Good balance of heat and moisture; classic Turkish character with good natural acidity.',
 '{"spring": "mild", "summer": "warm", "harvest": "classic_balanced", "region": "all_regions_good"}',
 84, 'very_good', '{"from": 2024, "to": 2030}', 'stable', 'Solid, reliable vintage; Turkish wine quality continues to rise across all regions.', 2);

COMMIT;
