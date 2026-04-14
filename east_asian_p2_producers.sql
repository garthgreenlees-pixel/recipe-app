-- EAST ASIAN BEVERAGE SESSION — PHASE 2: PRODUCERS
-- Region IDs: Niigata=45, Nada=46, Fushimi=47, Yamaguchi=48, Yamagata=49, Fukui=50
--             Uji=51, Shizuoka=52, Kagoshima-tea=53, Kagoshima-spirits=54, Oita=55, Okinawa=56
--             Yunnan=57, Fujian=58, Zhejiang=59, Guangdong=60, Guizhou=61, Sichuan=62
--             Central-Taiwan=63, Dong-Ding=64, Darjeeling=65, Assam=66, Nilgiri=67

BEGIN;

-- ============================================================
-- SAKE BREWERIES — NIIGATA
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Asahi Shuzo (Kubota)', 'sake_brewery', 45, 'Japan',
 'pursuit_of_purity',
 'Asahi Shuzo''s Kubota line represents the distillation of Niigata philosophy: tanrei karakuchi (light and dry) with absolute clarity of expression. The brewery uses Niigata''s ultra-soft snow-melt water to allow the most delicate sake rice character to emerge without mineral interference. Every Kubota expression is designed to complement food rather than dominate it.',
 '[{"name": "Katsuyuki Sato", "role": "Toji (Master Brewer)", "notes": "Third-generation master brewer; trained in Niigata''s traditional slow-fermentation methods"}]',
 '{"rice_varieties": ["Gohyakumangoku", "Koshi Tanrei", "Yamada Nishiki"], "water_source": "Uono River snow-melt, Niigata — soft water below 50mg/L hardness", "polishing_range": "35-65% remaining", "fermentation_temperature": "5-8°C for ginjo production", "annual_output": "approx 1,800 koku", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1830"}',
 'reserve', 'Kubota Manju is one of Japan''s most recognised sake brands globally, synonymous with Niigata''s tanrei karakuchi (light-dry) movement. The brewery has consistently won top awards at national sake competitions while maintaining accessible price points for premium expressions.',
 'Kubota Manju (Junmai Daiginjo) available in limited quantities at BC Liquor stores; Wismettac supplies fine dining accounts. High turnover — typically no allocation waiting list for standard expressions.',
 'ultra_premium', 1, 'Asahi Shuzo official history; John Gauntner Japan Sake Guide', true, true),

('Hakkaisan Shuzo', 'sake_brewery', 45, 'Japan',
 'cold_water_purity',
 'Hakkaisan (Eight Peaks Mountain) draws its name from the sacred Mt. Hakkai that feeds the brewery with pristine snowmelt water. The brewery''s signature is the snow-ageing programme (Yukimuro) — storing sake for three years in a specially constructed snow warehouse where the natural refrigeration of compacted snow maintains a constant 3°C without mechanical intervention.',
 '[{"name": "Nozawa family", "role": "Founding family, fourth generation active", "notes": "The Nozawa family transformed Hakkaisan from a regional brewer to an international benchmark for snow-country sake"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Gohyakumangoku", "Koshi Ibuki"], "water_source": "Mt. Hakkai snowmelt, Minamiuonuma, Niigata — among Japan''s softest brewing waters", "snow_ageing": "Yukimuro snow warehouse holds 3,000 tonnes of natural snow; 3-year ageing at 3°C constant temperature", "annual_output": "approx 3,000 koku", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1922"}',
 'estate', 'Hakkaisan''s Yukimuro three-year snow-aged Junmai Ginjo is among the most visually distinctive sake presentations in the world — served in a washi-paper wrapped bottle that evokes the snow culture of Niigata. The brewery''s standard expressions are benchmarks for the Niigata tanrei style.',
 'Yukimuro expressions limited; most expressions available through Wismettac BC distribution without allocation.',
 'premium', 1, 'Hakkaisan Shuzo official materials; Sake World', true, true),

('Ishimoto Shuzo', 'sake_brewery', 45, 'Japan',
 'extreme_refinement',
 'Ishimoto Shuzo produces Koshi no Kanbai — a sake so esteemed in Japan that it remained virtually unavailable outside the prefecture for decades. The brewery''s philosophy centres on extreme refinement through polishing, temperature control, and restraint: every production decision serves the goal of perfect purity of expression.',
 '[{"name": "Ishimoto family", "role": "Multi-generation ownership", "notes": "The family maintained Koshi no Kanbai as a local treasure for generations before international demand made export inevitable"}]',
 '{"rice_varieties": ["Gohyakumangoku", "Yamada Nishiki"], "water_source": "Niigata city groundwater — ultra-soft", "flagship": "Koshi no Kanbai — the name means ''Cold Plum of Koshi'' (ancient name for Niigata)", "annual_output": "approx 800 koku — deliberately small production", "bc_importer": "Wismettac Asian Foods Canada (limited)", "founded": "1884"}',
 'reserve', 'Koshi no Kanbai was for decades almost exclusively a local Niigata treasure — the sake families and restaurants of Niigata drank it themselves and exported little. Its reputation spread via word-of-mouth among sake enthusiasts until demand forced limited export. Now considered one of the three pinnacle Niigata sakes alongside Kubota and Hakkaisan.',
 'Muku (Junmai Daiginjo) and Sai (Honjozo) expressions; limited BC availability through Wismettac fine dining programme. Recommend advance ordering.',
 'premium', 1, 'John Gauntner Sake World; Ishimoto Shuzo official materials', true, true),

('Yoshinogawa Shuzo', 'sake_brewery', 45, 'Japan',
 'tanrei_tradition',
 'Yoshinogawa (River of Yoshino) is one of Niigata''s oldest continuously operating sake breweries and a keeper of the traditional tanrei karakuchi (light-dry) style. While newer breweries chased premium recognition, Yoshinogawa maintained its commitment to producing sake that above all else serves as the ideal companion to Niigata''s exceptional cuisine.',
 '[{"name": "Nakamura family", "role": "Long-term ownership family", "notes": "One of Niigata''s most respected brewing families; known for their approachability and willingness to educate"}]',
 '{"rice_varieties": ["Gohyakumangoku", "Koshi Ibuki"], "water_source": "Nakatsu River watershed, Niigata", "style": "Gensen Karakuchi (source dry) — their signature designation for authentic Niigata dryness", "bc_importer": "Fujiya Japanese Market Vancouver (limited)", "founded": "1548"}',
 'market', 'Among the oldest sake breweries in Japan — founded 1548, in the Sengoku period — Yoshinogawa represents continuity over innovation. Their Gensen Karakuchi (Source Dry) designation signals the purest expression of Niigata dry style. A reliable benchmark for understanding what Niigata sake actually tastes like.',
 'Good BC availability for standard expressions; premium Ginjo limited.',
 'mid_range', 2, 'Yoshinogawa Shuzo official history; BC Sake importer records', true, true),

('Niigata Meijo', 'sake_brewery', 45, 'Japan',
 'refined_ginjo',
 'Niigata Meijo produces Kakurei — a sake whose name (Crane Chill) evokes the cold clarity of a crane in winter. The brewery focuses exclusively on premium production, using only Niigata-grown rice and the prefecture''s signature soft water to produce light, refined expressions appropriate to the finest dining contexts.',
 '[{"name": "Brewery collective management", "role": "Multi-family cooperative ownership", "notes": "Niigata Meijo was established as a premium cooperative to produce limited-volume, high-quality sake"}]',
 '{"rice_varieties": ["Gohyakumangoku", "Yamada Nishiki"], "water_source": "Niigata prefecture soft water", "brand": "Kakurei — meaning Crane Chill; the crane is a symbol of long life and pure water in Japanese culture", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1907"}',
 'estate', 'Kakurei is considered the most refined and restaurant-forward of Niigata''s major brands — its lightness and delicacy make it the preferred sake in Tokyo fine dining accounts that seek the tanrei style. A sommelier''s sake.',
 'Available through Wismettac BC; standard expressions consistently in stock.',
 'premium', 2, 'Sake World magazine; Niigata Sake Brewers Association', true, true);

-- ============================================================
-- SAKE BREWERIES — NADA
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Kiku-Masamune Sake Brewing', 'sake_brewery', 46, 'Japan',
 'kimoto_tradition',
 'Kiku-Masamune is Nada''s most traditional kimoto sake producer — using the original Edo-period method of creating the yeast starter (moto) by laboriously grinding steamed rice with wooden poles to promote natural lactic acid bacteria development. This labour-intensive method (abandoned by most breweries in favour of the faster sokujo method after 1909) produces sake of exceptional depth, acidity, and ageing potential.',
 '[{"name": "Ukita family", "role": "Founding family, 15th generation active", "notes": "The Ukita family are among the longest-continuously-operating sake brewing families in Japan''s history, maintaining the kimoto tradition through the 20th century''s rationalisation era"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Kikusui"], "water_source": "Miyamizu — Nada''s legendary hard water from the Nishinomiya aquifer", "signature_technique": "Kimoto method — wooden pole grinding (yamaoroshi) for natural lactic fermentation; 3x longer production time than modern sokujo method", "taru_sake": "Cedar barrel aged expression — another traditional Nada speciality", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1659"}',
 'estate', 'Kiku-Masamune stands apart from modern Nada''s more commercial producers by maintaining kimoto production as their primary method. Their sake has greater acidity, depth, and food-pairing versatility than most Nada expressions. The brewery''s 1659 founding makes it one of Japan''s oldest. Particularly valued in kaiseki and French fine dining for the kimoto''s natural umami backbone.',
 'Kimoto Junmai and Taru Sake most widely available; Grand Junmai Daiginjo limited.',
 'premium', 1, 'Kiku-Masamune official history; John Gauntner Sake World', true, true),

('Ozeki Sake', 'sake_brewery', 46, 'Japan',
 'accessibility_and_scale',
 'Ozeki is one of Japan''s largest sake producers, making them a benchmark for quality at accessible price points. While their volume production uses modern methods, Ozeki maintains a premium line that leverages Nada''s Miyamizu water and Yamada Nishiki rice to produce honest, food-friendly sake that represents Nada''s otokozake (man''s sake) character without pretension.',
 '[{"name": "Ozeki management team", "role": "Corporate structure with professional brewing management", "notes": "Ozeki employs some of Nada''s most experienced toji (master brewers) despite its corporate scale"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Gohyakumangoku"], "water_source": "Miyamizu — Nada hard water", "scale": "One of Japan''s 5 largest sake producers by volume", "bc_importer": "Wismettac Asian Foods Canada; available at T&T Supermarket", "founded": "1711"}',
 'market', 'Ozeki provides the most accessible entry point to authentic Nada sake — their Junmai is clean, honest, and unmistakably Nada in its mineral, slightly firm structure. A reliable house pour or introductory sake for guests new to the category.',
 'Widely available in BC through T&T Supermarket and Wismettac. No allocation required.',
 'mid_range', 2, 'Ozeki Sake official materials; Japan Sake and Shochu Makers Association', true, true),

('Sawanotsuru Sake Brewing', 'sake_brewery', 46, 'Japan',
 'nada_refinement',
 'Sawanotsuru (Swamp Crane) occupies a unique position in Nada: a large traditional brewery that has consistently invested in premium production while maintaining Nada''s Miyamizu-driven character. Their Junmai Daiginjo demonstrates that Nada''s assertive water profile need not preclude delicacy — when polished to extreme fineness, the Miyamizu''s mineral backbone supports rather than overwhelms.',
 '[{"name": "Nada Brewing Council representative", "role": "Collaborative management", "notes": "Long-established Nada family brewery, maintaining traditional production alongside modern premium line"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Gohyakumangoku"], "water_source": "Miyamizu — Nada''s defining hard water", "premium_line": "Junmai Daiginjo and Daiginjo expressions at 35-50% seimaibuai (polishing ratio)", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1717"}',
 'estate', 'Sawanotsuru demonstrates the capability of Nada''s Miyamizu water for producing premium sake — a common misconception is that Nada only produces the full-bodied mass-market style. Their Junmai Daiginjo achieves the mineral-backed elegance that defines Nada''s best.',
 'Junmai Daiginjo limited BC availability; standard expressions consistently stocked at Wismettac.',
 'premium', 2, 'Sawanotsuru official history; Sake World', true, true),

('Nihonsakari', 'sake_brewery', 46, 'Japan',
 'nada_heritage',
 'Nihonsakari (Sakari of Japan) is a Nada institution, producing sake in the traditional Miyamizu tradition while embracing modern quality standards. The brewery''s range runs from accessible everyday sake to premium ginjo expressions, all demonstrating Nada''s characteristic mineral backbone and food-pairing versatility.',
 '[{"name": "Nihonsakari management", "role": "Professional brewing management", "notes": "Historic Nada brewer with consistent award performance at national sake competitions"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Nihonsakari proprietary rice varieties"], "water_source": "Miyamizu — Nada", "bc_importer": "Wismettac Asian Foods Canada (limited)", "founded": "1889"}',
 'market', 'Nihonsakari is a reliable reference point for the modern Nada style — approachable, consistent, and honest to Miyamizu''s mineral character. Their Junmai Ginjo represents excellent value for the quality achieved.',
 'Limited BC distribution; available through Wismettac and some Japanese restaurant wholesale accounts.',
 'mid_range', 2, 'Japan Sake and Shochu Makers Association; Nada Sake Brewers Association', true, true),

('Konishi Sake Brewing', 'sake_brewery', 46, 'Japan',
 'itami_refinement',
 'Konishi Sake Brewing produces Shirayuki (White Snow) — one of Japan''s oldest continuously produced sake brands, made in Itami (adjacent to Nada) using similar water profiles. The Shirayuki brand was historically the primary export sake of Japan, shipped to Dutch East India Company traders in the 17th century — the first Japanese sake to reach Europe.',
 '[{"name": "Konishi family", "role": "Multi-generation founding family", "notes": "One of Japan''s great sake brewing families; Konishi''s Itami location, just north of Nada, shares the same aquifer and stylistic tradition"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Gohyakumangoku"], "water_source": "Itami groundwater — Miyamizu adjacent, comparable mineral profile", "historical_note": "Shirayuki exported to the Netherlands via Dutch East India Company from the 17th century — the first Japanese sake to reach Europe", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1550"}',
 'market', 'Konishi''s Shirayuki is a living piece of Japanese brewing history — an unbroken production lineage of 470+ years. The modern expressions maintain the traditional Hyogo character while meeting contemporary quality standards. Excellent educational piece for sake history-minded sommeliers.',
 'Good BC availability; standard expressions stocked at Wismettac.',
 'mid_range', 1, 'Konishi Sake Brewing official history; Japan Sake and Shochu Makers Association', true, true);

-- ============================================================
-- SAKE BREWERIES — FUSHIMI
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Masuda Tokubee Shoten', 'sake_brewery', 47, 'Japan',
 'nigori_heritage',
 'Masuda Tokubee Shoten is the historic producer of Tsuki no Katsura — credited with reviving junmai (pure rice) sake and nigori (cloudy sake) as legitimate premium categories at a time when both had been largely abandoned for the commercially dominant added-alcohol styles. The brewery''s 1964 junmai revival was a turning point in modern sake history.',
 '[{"name": "Masuda Tokubee", "role": "Brewery founder and 8th generation toji", "notes": "Masuda Tokubee is credited with the pivotal 1964 decision to resume junmai (pure rice) production at a time when virtually all commercial sake contained added alcohol — a decision that helped spark the modern junmai movement"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Iwai — Fushimi''s local rice variety"], "water_source": "Fushimi Momoyama soft water", "historical_contribution": "1964: First commercial junmai sake revival; credited with saving nigori sake from extinction by registering it as a distinct category with tax authorities", "bc_importer": "Specialty Japanese sake importers via Wismettac", "founded": "1675"}',
 'reserve', 'Masuda Tokubee Shoten holds a unique place in modern sake history: as the reviver of junmai (pure rice) sake and the rescue of nigori from obscurity. Their Tsuki no Katsura Junmai Daiginjo using Iwai rice — Kyoto''s native sake rice — is among the most distinctive expressions in Fushimi. The brewery produces small volumes of extraordinary quality.',
 'Limited BC availability; primarily accessible through specialist sake retailers. Import on request through Wismettac fine dining programme.',
 'ultra_premium', 1, 'Masuda Tokubee Shoten official history; Philip Harper The Book of Sake; John Gauntner Sake World', true, true),

('Tamanohikari Sake Brewing', 'sake_brewery', 47, 'Japan',
 'junmai_purity',
 'Tamanohikari (Jewel of Light) produces exclusively junmai (pure rice) sake — no added alcohol in any expression. This makes them the most extreme exponent of Fushimi''s gentle, water-driven style without any concession to commercial alcohol enhancement. Their philosophy is that the rice and water alone must express everything.',
 '[{"name": "Kishida family", "role": "Founding family, modern management", "notes": "Tamanohikari''s commitment to 100% junmai production predates the modern junmai movement and has never wavered"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Bizen Omachi — the heritage rice of Okayama, producing earthy, rich sake"], "water_source": "Fushimi soft water from Momoyama Highland", "commitment": "100% junmai (pure rice) production — no added alcohol in any expression", "special_rice": "Bizen Omachi: an ancient heritage rice variety from Okayama that produces a richer, more earthy sake than modern varieties", "bc_importer": "Wismettac Asian Foods Canada (limited)", "founded": "1673"}',
 'estate', 'Tamanohikari''s exclusive junmai production and use of Bizen Omachi rice — an heirloom variety with deeper, earthier character than modern Yamada Nishiki — produces Fushimi sake of unusual depth and texture. A natural wine equivalent in the sake world: nothing added, nothing removed.',
 'Limited BC availability. Bizen Omachi Junmai Daiginjo primarily for fine dining accounts.',
 'premium', 1, 'Tamanohikari Sake Brewing official materials; Sake World', true, true),

('Saito Shuzo', 'sake_brewery', 47, 'Japan',
 'fushimi_elegance',
 'Saito Shuzo''s Tozai brand represents Fushimi''s gentle character made accessible to international markets. The brewery produces approachable, food-friendly sake with the onnazake (woman''s sake) elegance of Fushimi water, positioned for Western markets unfamiliar with traditional sake styles.',
 '[{"name": "Saito family", "role": "Traditional Fushimi brewing family", "notes": "One of Fushimi''s established sake families, maintaining traditional kura (brewery) in the historic district near Fushimi Inari"}]',
 '{"rice_varieties": ["Yamada Nishiki", "Gohyakumangoku"], "water_source": "Fushimi soft water — Momoyama aquifer", "export_brands": "Tozai (East Meets West) — positioned for Western markets", "bc_importer": "Wismettac Asian Foods Canada; available at specialty Japanese liquor stores in Metro Vancouver", "founded": "1895"}',
 'market', 'Saito Shuzo''s Tozai brand has been one of the most successful Japanese sake export brands in North America — approachable, well-priced, and consistently representative of Fushimi''s gentle, food-pairing style. Their Snow Maiden Nigori is a perennial best-seller.',
 'Good BC availability; Tozai expressions widely available at specialty stores and BC Liquor.',
 'mid_range', 2, 'Saito Shuzo official materials; BC Liquor product listings', true, true);

-- ============================================================
-- SAKE BREWERIES — OTHER REGIONS
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Asahi Shuzo (Dassai)', 'sake_brewery', 48, 'Japan',
 'relentless_refinement',
 'Asahi Shuzo (Yamaguchi) — entirely distinct from the Niigata brewery of the same name — produces Dassai, the sake that single-handedly redefined premium Japanese sake for international audiences. The brewery''s philosophy centres on continuous improvement: first 50%, then 39%, then 23% polishing ratios, then ''Beyond'' (the most refined sake ever produced commercially). Every production decision serves flavour, not tradition for its own sake.',
 '[{"name": "Hiroshi Sakurai", "role": "Third-generation owner, driving force of the Dassai transformation", "notes": "Sakurai''s 1990s decision to pivot from struggling regional brewery to ultra-premium production is one of Japan''s great business transformation stories"}, {"name": "Kazuhiro Nishida", "role": "Head Brewer", "notes": "Oversees polishing and fermentation precision that enables 23% and Beyond expressions"}]',
 '{"rice_varieties": ["Yamada Nishiki from premium Tojo district, Hyogo; Dassai Senbonishiki (proprietary variety)"], "water_source": "Nishiki River mountain water, Yamaguchi — granitic filtered, medium-soft", "polishing_ratios": {"Dassai_Beyond": "undisclosed — below 23%", "Dassai_23": "23% rice remaining (77% polished away)", "Dassai_39": "39% remaining", "Dassai_45": "45% remaining"}, "international_presence": "70+ countries; Dassai Blue brewery in Hyde Park, New York (opened 2023)", "bc_importer": "Wismettac Asian Foods Canada; available at BC Liquor stores and fine dining accounts", "founded": "1948"}',
 'reserve', 'Dassai is arguably the most internationally recognised Japanese sake brand — the sake that appears on Michelin-starred restaurant wine lists from Tokyo to Paris. The 23 expression (23% rice remaining after polishing) represents the outer edge of what is commercially producible: pure rice, pure water, extraordinary technique. Dassai Beyond is produced in tiny quantities and priced at $400+ CAD per 720ml — a collector''s item. The brewery''s strategic approach to international fine dining has transformed how the world understands premium sake.',
 'Dassai 23 and Beyond: allocation-based through Wismettac fine dining programme. Dassai 39 and 45 more readily available at BC Liquor and specialty stores.',
 'ultra_premium', 1, 'Dassai official materials; Sake: A Modern Guide by Melinda Joe; Asahi Shuzo Yamaguchi press materials', true, true),

('Takagi Shuzo', 'sake_brewery', 49, 'Japan',
 'divine_scarcity',
 'Takagi Shuzo produces Juyondai — the most coveted and least available sake in Japan. The brewery''s philosophy rejects export and large-volume production in favour of extreme quality control for a tiny domestic output distributed through a strict lottery system to selected retailers. Juyondai''s cult status derives from both its extraordinary quality and its deliberate scarcity.',
 '[{"name": "Akitsuna Takagi", "role": "Brewery owner and chief brewer", "notes": "Takagi has maintained absolute quality control and scarcity by refusing to expand production despite limitless demand — a deliberate choice that has only deepened Juyondai''s mythological status"}]',
 '{"rice_varieties": ["Yamada Nishiki from premium-contracted Hyogo farms", "Dewa Sansan — Yamagata''s proprietary rice variety"], "water_source": "Yamagata mountain water — soft, mineral-light", "distribution": "Japan-only; lottery allocation to approximately 100 selected retailers nationwide; zero official export programme", "scarcity": "International acquisition requires specialist import agents; grey-market imports significantly marked up; do not list as available at BC restaurants without confirmed allocation", "founded": "1872"}',
 'reserve', 'Juyondai (Fourteen Generations) is Japan''s most mythologised sake — the Petrus or DRC equivalent. Its quality is extraordinary by any measure, but its cult status has outpaced even its excellence: bottles sell at 3-10x retail price on the secondary market. For a sommelier, being able to source Juyondai for a guest is a significant relationship and knowledge signal. Extremely rare in BC; any listing should be verified with proof of allocation.',
 'Essentially unavailable through standard BC channels. Any appearance requires specialist import and direct Wismettac relationship. Verify before listing.',
 'ultra_premium', 1, 'John Gauntner Sake World; Sake: A Modern Guide by Melinda Joe; Takagi Shuzo profile', true, true),

('Katokichibee Shouten', 'sake_brewery', 50, 'Japan',
 'fukui_perfection',
 'Katokichibee Shouten produces Born — a brand that combines Fukui''s pristine snow-melt water, extreme polishing ratios, and traditional pressing methods to produce Junmai Daiginjo of international calibre. The brewery''s isolated Fukui location has paradoxically enabled innovation: free from Niigata or Nada tradition''s gravitational pull, Born pursues its own vision of sake perfection.',
 '[{"name": "Katokichibee Shouten family management", "role": "Traditional family brewing", "notes": "A small, highly focused brewery that produces exclusively premium and ultra-premium sake expressions; no volume or entry-level production"}]',
 '{"rice_varieties": ["Yamada Nishiki from Hyogo", "Gohyakumangoku from Fukui"], "water_source": "Echizen mountain snowmelt — Fukui''s extraordinary soft water", "polishing_ratios": "Born Gold: 35%; Born Dream: 50%", "pressing": "Fukurotsuri (bag hanging) for premium expressions — sake drips by gravity alone through cloth bags, no mechanical pressing", "bc_importer": "Wismettac Asian Foods Canada (limited)", "founded": "1848"}',
 'reserve', 'Born''s international success, particularly in Europe, made it one of the first truly premium sake exports to achieve recognition in French fine dining. Born Gold and Born Dream consistently appear on best-sake lists globally. The fukurotsuri pressing method — gravity-only, no mechanical pressure — produces the clearest, most refined sake possible from a given polishing ratio.',
 'Limited BC availability; Born Gold and Born Dream through Wismettac fine dining allocation.',
 'ultra_premium', 1, 'Katokichibee Shouten official materials; Born Sake international press', true, true),

('Dewazakura Shuzo', 'sake_brewery', 49, 'Japan',
 'ginjo_revolution',
 'Dewazakura Shuzo (Cherry Blossom of Dewa) is credited as a pioneer of the ginjo movement — producing refined, fragrant ginjo sake at a time when the style was considered too difficult and expensive for commercial production. Their 1981 Oka Ginjo (Cherry Bouquet) became one of Japan''s first widely distributed premium ginjo expressions.',
 '[{"name": "Ikeda family", "role": "Multi-generation ownership", "notes": "The Ikeda family''s commitment to ginjo production in the 1970s–80s was ahead of the market and helped establish the category''s commercial viability"}]',
 '{"rice_varieties": ["Dewa Sansan — Yamagata''s registered proprietary rice variety", "Yamada Nishiki"], "water_source": "Tendo city water — Yamagata mountain soft water", "historical_role": "Dewazakura''s Oka Ginjo (1981) is credited as one of Japan''s first commercially successful ginjo-class sakes, helping define the category''s quality standard", "bc_importer": "Wismettac Asian Foods Canada", "founded": "1892"}',
 'estate', 'Dewazakura''s Oka Cherry Bouquet Ginjo is a historically significant sake — one of the products that proved the ginjo style could reach mass market appreciation. A benchmark for understanding the ginjo category''s development. Modern expressions maintain the same elegant, floral character that made the brewery''s reputation.',
 'Good BC availability for Oka Ginjo through Wismettac; premium expressions limited.',
 'premium', 1, 'Dewazakura Shuzo official history; Japan''s Sake Renaissance by Stefan Persson', true, true),

('Aramasa Shuzo', 'sake_brewery', 49, 'Japan',
 'sixth_generation_revolution',
 'Aramasa Shuzo underwent a radical transformation when Yusuke Satou returned from a career in journalism to lead the brewery in 2009. Satou eliminated all modern additives, returned to kimoto fermentation using the brewery''s own naturally cultivated No. 6 yeast (the oldest sake yeast in Japan, isolated at Aramasa in 1935), and began producing what many consider Japan''s most philosophically coherent sake — a natural sake movement in amber.',
 '[{"name": "Yusuke Satou", "role": "Sixth-generation owner-brewer, brewery transformer", "notes": "Satou is the most written-about figure in contemporary Japanese sake — his abandonment of a journalism career to remake his family''s brewery into Japan''s most distinctive natural sake producer has inspired a generation of young sake brewers"}]',
 '{"rice_varieties": ["Exclusively Akita-grown rice: Akita Sake Komachi, Miyama Nishiki, Omachi, Shinshu Miyama"], "water_source": "Akita city groundwater — soft water of the Akita basin", "yeast": "No. 6 — the oldest classified sake yeast in Japan, isolated at Aramasa in 1935; lower fermentation temperature produces distinctive aromatic profile", "fermentation": "100% kimoto (traditional wooden pole moto) — eliminated all modern brewing aids including added lactic acid", "bottles": "All sake bottled in dark brown glass bottles that resemble Japanese craft beer — a deliberate aesthetic statement", "bc_importer": "Extremely limited; specialist import only", "founded": "1852"}',
 'reserve', 'Aramasa No. 6 is the most discussed and debated sake in contemporary Japan — a natural sake movement statement from a brewery that has chosen the hardest possible production path. The No. 6 yeast, isolated at Aramasa in 1935, produces distinctive lower-alcohol, complex expressions unlike any other Japanese sake. For sommeliers, understanding Aramasa requires understanding both sake history and the natural wine movement — it sits at their intersection. Extremely limited BC availability.',
 'Essentially no BC retail availability; requires specialist import relationship. A knowledge and relationship signal for sommeliers who can source it.',
 'ultra_premium', 1, 'Aramasa Shuzo official materials; Yusuke Satou interviews; Sake Today magazine', true, true);

-- ============================================================
-- SHOCHU / AWAMORI DISTILLERIES
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Kirishima Shuzo', 'distillery', 54, 'Japan',
 'imo_mastery',
 'Kirishima Shuzo is Japan''s largest imo (sweet potato) shochu producer, commanding the Kagoshima market with their Kuro Kirishima (Black Kirishima) flagship. Their use of Kogane Sengan sweet potatoes from Kagoshima''s volcanic soil and black koji (Aspergillus luchuensis) produces the definitive imo shochu character: earthy, sweet potato-forward, with a long aromatic finish.',
 '[{"name": "Kengo Enatsu", "role": "Master Distiller", "notes": "Leads the technical production team; oversees the black koji cultivation programme that defines Kirishima''s character"}]',
 '{"base_materials": "Kogane Sengan sweet potato from Kagoshima volcanic Shirasu soil", "koji": "Black koji (Aspergillus luchuensis var. awamori) — traditional Kyushu black koji", "distillation": "Single pot distillation at atmospheric pressure; preserves maximum sweet potato aromatic compounds", "expressions": ["Kuro Kirishima 25° (standard)", "Red Kirishima (lighter style)", "Gold Kirishima (premium aged)"], "bc_availability": "T&T Supermarket and specialty Asian liquor stores in Metro Vancouver", "founded": "1916"}',
 'market', 'Kirishima is the entry point for anyone seeking to understand imo shochu — ubiquitous in Kagoshima izakayas, produced in enormous volume without sacrificing the category''s essential character. Kuro Kirishima (Black Kirishima) is the standard against which other imo shochu are measured: earthy, clean, slightly sweet potato-forward with black koji''s characteristic tartness.',
 'Good BC availability at T&T Supermarket and specialty Asian liquor retailers. No allocation required.',
 'mid_range', 1, 'Japan Sake and Shochu Makers Association; Stefan Persson Shochu Guide', true, true),

('Nishi Shuzo', 'distillery', 54, 'Japan',
 'premium_imo_craft',
 'Nishi Shuzo produces Toko — one of Kagoshima''s most respected craft imo shochu brands. The distillery''s focus on small-batch production using carefully selected Kogane Sengan sweet potatoes, traditional black koji, and slow fermentation at controlled temperatures produces imo shochu of exceptional aromatic complexity and depth.',
 '[{"name": "Nishi family", "role": "Traditional Kagoshima distilling family", "notes": "One of the families that maintained craft imo shochu production through the mass-market era"}]',
 '{"base_materials": "Selected Kogane Sengan sweet potato, Kagoshima", "koji": "Black koji — traditional Kyushu method", "production_scale": "Small craft production; hand-selected potatoes, slow fermentation", "brand": "Toko — named for the sacred island of Toko in Kagoshima mythology", "bc_availability": "Specialty Japanese shochu retailers; limited BC availability", "founded": "1884"}',
 'estate', 'Toko represents the craft end of Kagoshima imo shochu — a level of hand-production and ingredient selection rarely found in the category''s larger producers. A benchmark for understanding what imo shochu can achieve at its best.',
 'Limited BC availability; recommend sourcing through specialist Japanese spirits importers.',
 'premium', 2, 'Nishi Shuzo official materials; Kagoshima Shochu Association', true, true),

('Sanwa Shurui', 'distillery', 55, 'Japan',
 'mugi_refinement',
 'Sanwa Shurui created the modern category of refined barley (mugi) shochu with their Iichiko brand, launched in 1979. The decision to market barley shochu in premium packaging to urban consumers transformed the category from a rough rural spirit to an aspirational lifestyle beverage. Iichiko Silhouette (the tall, distinctive bottle) became one of Japan''s most recognised spirits designs.',
 '[{"name": "Sanwa Shurui management", "role": "Corporate brewing management", "notes": "Sanwa Shurui''s marketing vision for Iichiko in the late 1970s revolutionised the shochu category''s image"}]',
 '{"base_materials": "Two-row barley from Oita and Fukuoka", "koji": "White koji (Aspergillus kawachii) — produces gentler acidity than black koji, allowing barley sweetness to dominate", "expressions": ["Iichiko Silhouette 25° (standard)", "Iichiko Frasco 30° (premium)", "Iichiko Special 43° (premium strength)"], "bc_availability": "T&T Supermarket, Japanese restaurants, Wismettac wholesale", "founded": "1958"}',
 'market', 'Iichiko is the most widely distributed and recognised mugi shochu brand globally. Its clean, approachable character — slightly sweet, mellow, infinitely mixable — makes it the ideal gateway into the shochu category. Particularly popular served on the rocks (on the rocks = ''rokku'' in Japanese) or with cold water.',
 'Widely available in BC at T&T and Japanese grocery stores. No allocation required.',
 'mid_range', 1, 'Sanwa Shurui official materials; Japan Sake and Shochu Makers Association', true, true),

('Komasa Jokamachi', 'distillery', 54, 'Japan',
 'artisan_imo',
 'Komasa Jokamachi is an artisan Kagoshima distillery producing small-batch imo shochu with exceptional attention to base material quality. Their Sakurajima brand references the iconic Kagoshima volcano — whose ash enriches the local sweet potato cultivation soils — as a statement of terroir-driven production.',
 '[{"name": "Komasa family", "role": "Traditional Kagoshima distilling family, several generations", "notes": "Komasa maintains traditional pot distillation and black koji methods in an era of increasing industrialisation"}]',
 '{"base_materials": "Kogane Sengan sweet potato from volcanic Shirasu soil near Sakurajima", "koji": "Black koji — traditional", "distillation": "Single pot at atmospheric pressure", "bc_availability": "Specialist Japanese spirits importers; very limited BC presence", "founded": "1883"}',
 'estate', 'Komasa''s Sakurajima imo shochu carries a genuine terroir story: sweet potatoes grown in volcanic soil at the foot of Japan''s most active volcano, fermented with black koji, and distilled in traditional copper pots. A serious imo shochu for guests interested in Japanese spirits provenance.',
 'Very limited BC availability. Recommend listing only when allocation confirmed.',
 'premium', 2, 'Komasa Jokamachi official materials; Kagoshima Shochu Association', true, true),

('Nikaido Shuzo', 'distillery', 55, 'Japan',
 'premium_mugi_craft',
 'Nikaido Shuzo is one of Oita''s premium craft barley shochu producers, making Naka Naka — a mugi shochu of unusual depth and character achieved through careful selection of local barley, white koji fermentation, and precise distillation control.',
 '[{"name": "Nikaido family", "role": "Traditional Oita distilling family", "notes": "Maintains craft production approach in Oita''s increasingly industrialised mugi shochu landscape"}]',
 '{"base_materials": "Two-row barley from Oita region", "koji": "White koji", "brand": "Naka Naka — meaning ''so-so'' in Japanese, an ironic understatement for a remarkably refined spirit", "bc_availability": "Very limited; specialist Japanese spirits importers", "founded": "1890"}',
 'estate', 'Naka Naka is one of the most sought-after premium mugi shochu expressions — its ironic name (meaning ''not bad'' / ''so-so'') belies the genuine complexity of the spirit. A favourite among shochu connoisseurs who have moved beyond introductory expressions.',
 'Very limited BC availability. Specialist import required.',
 'premium', 2, 'Japan Sake and Shochu Makers Association; shochu enthusiast community', true, true),

('Zuisen Distillery', 'distillery', 56, 'Japan',
 'awamori_tradition',
 'Zuisen (Auspicious Spring) Distillery is one of Okinawa''s most traditional awamori producers, maintaining the clay pot (kame) ageing tradition that transforms young awamori into koshu (aged) expressions of extraordinary depth. The distillery''s aged stocks, accumulated over decades in their warehouse of traditional terracotta kame, represent irreplaceable liquid cultural heritage.',
 '[{"name": "Zuisen family management", "role": "Multi-generation Okinawan distilling family", "notes": "Zuisen maintains the traditional kame ageing programme at a time when many Okinawan distilleries have shifted to stainless steel tanks"}]',
 '{"base_materials": "100% long-grain Thai indica rice (imported from Thailand — traditional for all Okinawan awamori)", "koji": "Black koji (Aspergillus luchuensis) exclusively", "ageing": "Traditional terracotta clay kame (pot) ageing; 3, 5, 10-year expressions; long-aged koshu up to 25+ years", "abv_range": "25–43°, with some genshu (undiluted) expressions at 60°", "bc_availability": "Specialty Japanese spirits retailers; very limited BC presence", "founded": "1887"}',
 'estate', 'Zuisen''s koshu (aged awamori) represents one of the most compelling and underappreciated aged spirits categories in the world. The clay pot ageing produces a gentle oxidation that rounds the spirit and builds complexity without the wood tannins of barrel ageing — a uniquely Okinawan maturation signature. For spirits-literate guests, aged awamori is one of the world''s great hidden treasures.',
 'Very limited BC availability. Specialist import from Japanese spirits retailers.',
 'premium', 1, 'Okinawa Awamori Distillers Association; awamori.jp', true, true),

('Helios Distillery', 'distillery', 56, 'Japan',
 'okinawa_innovation',
 'Helios Distillery (named for the Greek sun god) is one of Okinawa''s most innovative producers, producing both traditional awamori and modern craft spirits including Okinawan rum and gin. Their Ryukyu Awamori represents an accessible, approachable expression of the category while their premium aged koshu competes with Zuisen at the top level.',
 '[{"name": "Helios management team", "role": "Multi-product craft distillery management", "notes": "Helios is among Okinawa''s most internationally oriented distilleries; their Masahiro Okinawa Gin has received Western awards"}]',
 '{"base_materials": "Thai indica rice for awamori; Okinawan botanicals for gin", "koji": "Black koji for awamori production", "product_range": "Awamori (young and aged koshu), Okinawan rum, Masahiro Okinawan Gin", "bc_availability": "Some BC availability through specialty Japanese spirits retailers", "founded": "1961"}',
 'market', 'Helios provides the most accessible entry point to Okinawan awamori — their standard Ryukyu expression is clean, approachable, and representative of the category without the intensity of aged koshu. A good introduction for guests curious about Japanese spirits beyond shochu and sake.',
 'Limited BC availability at specialty Japanese spirits stores.',
 'mid_range', 2, 'Helios Distillery official materials; Okinawa Awamori Distillers Association', true, true),

('Kumesen Shuzo', 'distillery', 56, 'Japan',
 'koshu_mastery',
 'Kumesen Shuzo (named for the sacred Kume Island off Okinawa''s coast) produces what many consider the finest aged awamori (koshu) available — their long-aged expressions, stored in traditional kame and aged for 25+ years, achieve a depth and complexity that places them among the world''s great aged spirits. Kume Island''s specific water and microclimate are considered terroir elements.',
 '[{"name": "Kumesen family", "role": "Traditional Okinawan distilling family", "notes": "Kumesen has maintained the longest aged stock programme of any Okinawan distillery — decades of patient kame ageing create a liquid archive of Okinawan spirits heritage"}]',
 '{"base_materials": "Thai indica rice", "koji": "Black koji exclusively", "water": "Kume Island coral limestone filtered water — unique mineral signature", "ageing": "Kame ageing programme; 3, 5, 10, 15, 25, and extended special releases", "bc_availability": "Very limited; specialist import", "founded": "1961"}',
 'reserve', 'Kumesen Kusu (the aged designation in Okinawa''s Ryukyuan dialect) is the standard against which all aged awamori is measured. Their 25-year Kusu is an extraordinary spirit — complex, smooth, with the clay pot''s oxidative influence producing notes of dried fruit, caramel, and mineral that no barrel-aged spirit can replicate. For a wine-literate sommelier, it pairs with aged Burgundy in terms of philosophical approach to time and terroir.',
 'Very limited BC availability. Requires specialist Japanese spirits import relationship.',
 'ultra_premium', 1, 'Okinawa Awamori Distillers Association; Kumesen Shuzo official materials', true, true);

-- ============================================================
-- TEA PRODUCERS — JAPAN
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Ippodo Tea Co.', 'tea_garden', 51, 'Japan',
 'three_centuries_of_uji',
 'Ippodo (One Sprig of Plum) has operated continuously in Kyoto''s Teramachi district since 1717, making it the oldest continuously operating tea shop in Japan. Their philosophy is the direct transmission of traditional Uji tea cultivation and preparation methods — they teach as much as they sell. Every product comes with exact brewing instructions; the shop''s consultants are among Japan''s most knowledgeable tea educators.',
 '[{"name": "Watanabe family", "role": "Multi-generation ownership family", "notes": "The Watanabe family has maintained Ippodo for over 300 years, through multiple periods of political upheaval, maintaining the same core product philosophy"}]',
 '{"specialties": ["Ceremonial matcha (multiple grades: Ummon, Kan-un)", "Gyokuro (Sayamakaori, Shōen)", "Sencha (Shogyokuro, Kinkaku)", "Hojicha, Genmaicha, Kyobancha"], "region": "Uji and surrounding Kyoto prefecture growing areas", "retail_locations": "Kyoto flagship (Teramachi, founded 1717); Tokyo store; online international", "bc_availability": "International online orders via ippodo-tea.co.jp; Fujiya Japanese Market Vancouver stocks limited range", "founded": "1717"}',
 'reserve', 'Ippodo is the standard reference for Japanese green tea quality internationally — when the New York Times, Wine Spectator, or international sommeliers seek an authoritative source for ceremonial matcha or gyokuro, Ippodo is consistently cited. Their three-century reputation is fully justified: quality control, product consistency, and educational materials are unmatched in the Japanese tea industry. A Ippodo matcha programme in a restaurant immediately signals serious beverage literacy.',
 'International online orders available year-round; Fujiya Vancouver stocks some expressions. No allocation required.',
 'ultra_premium', 1, 'Ippodo Tea Co. official history (founded 1717); New York Times tea reviews; Ippodo educational materials', true, true),

('Marukyu Koyamaen', 'tea_garden', 51, 'Japan',
 'ceremonial_precision',
 'Marukyu Koyamaen is Uji''s most ceremony-oriented tea producer, supplying matcha to Japanese tea schools including Urasenke and Omotesenke — the two main schools of traditional chanoyu (tea ceremony). Their matcha grades are calibrated specifically for ceremony use: particle size, colour, and umami balance are optimised for different temae (tea ceremony procedures).',
 '[{"name": "Koyama family", "role": "Traditional Uji tea family, multi-generation", "notes": "Marukyu Koyamaen''s long relationship with the main tea ceremony schools gives them unique insight into what ceremonial-grade matcha must achieve"}]',
 '{"specialties": "Ceremonial matcha grades for both koicha (thick tea) and usucha (thin tea) contexts; premium gyokuro; tencha (unground shade leaf)", "ceremony_relationships": "Official suppliers to Urasenke and Omotesenke tea ceremony schools", "region": "Uji, Kyoto prefecture", "bc_availability": "Online orders from marukyu-koyamaen.co.jp; specialty tea retailers", "founded": "1861"}',
 'reserve', 'Marukyu Koyamaen''s relationship with Japan''s official tea ceremony schools is the strongest institutional endorsement any tea producer can receive. When the Urasenke tradition prepares matcha for a state ceremony — receiving a head of state, performing at an international event — Marukyu Koyamaen typically supplies the matcha. This is not marketing; it is documented institutional trust.',
 'Online international orders; specialty tea retailers. Premium grades may require advance order.',
 'ultra_premium', 1, 'Marukyu Koyamaen official history; Urasenke school documentation; Japanese tea ceremony academic sources', true, true),

('Nakamura Tokichi Honten', 'tea_garden', 51, 'Japan',
 'uji_heritage_dining',
 'Nakamura Tokichi Honten, founded 1854 in Uji, is unique among serious tea producers in combining premium tea production with one of Japan''s most famous matcha-themed restaurants. Their Uji Tokichi restaurant serves matcha in every dish — soups, sweets, desserts — while the adjoining tea shop sells their premium cultivar teas. The integration of premium tea production with dining education is a model for the restaurant industry.',
 '[{"name": "Nakamura family", "role": "Founding family, seventh generation active", "notes": "The current generation has expanded the restaurant concept while maintaining production quality — a rare successful integration of tea production and hospitality"}]',
 '{"specialties": "Ceremonial matcha; gyokuro; kabuse sencha; matcha-based food integration", "restaurant": "Uji Tokichi — matcha cuisine experience; reservations typically required months in advance", "region": "Uji, Kyoto prefecture", "bc_availability": "Online orders; specialty Japanese retailers", "founded": "1854"}',
 'estate', 'Nakamura Tokichi Honten demonstrates how premium tea producers can build a hospitality dimension that educates customers while creating demand. Their restaurant model — using their own ceremonial matcha throughout the menu — is a direct inspiration for high-end restaurants seeking to build matcha programmes. The production quality matches their hospitality reputation.',
 'Online international orders. Premium grades limited.',
 'premium', 1, 'Nakamura Tokichi Honten official history; Uji tourism documentation', true, true),

('Kyoto Obubu Tea Farms', 'tea_garden', 51, 'Japan',
 'terroir_education',
 'Kyoto Obubu Tea Farms, based in Wazuka-cho (one of Uji''s finest growing villages), combines premium cultivation with active international education — running an internship programme that has hosted over 400 international tea professionals and students since 2007. Their products, ranging from ceremonial matcha to rare kabuse sencha and gyokuro, are accompanied by more detailed provenance information than any other Japanese tea producer.',
 '[{"name": "Akihiro Kita", "role": "Owner-farmer and educational director", "notes": "Kita''s dual role as farmer and educator has made Obubu one of the most internationally known Japanese tea farms; his transparent approach to production details is unusual in an industry that traditionally guards methods"}]',
 '{"specialties": "Ceremonial matcha; gyokuro; kabuse sencha; hojicha; unusual cultivar single-origin teas", "education": "International tea farm internship programme (2-week working stays); YouTube educational content; detailed online terroir information", "cultivars": "Multiple including Okumidori, Saemidori, Uji Hikari — named single-cultivar expressions available", "bc_availability": "Direct online orders via obubutea.com; some specialty tea retailers", "founded": "2007"}',
 'estate', 'Kyoto Obubu is the most transparency-oriented Japanese tea farm — an unusual distinction in an industry that traditionally guards cultivation and production information. For sommeliers seeking to understand Japanese tea provenance in depth, Obubu''s educational resources are invaluable. Their single-cultivar expressions allow direct comparison of Uji''s different tea cultivars — an educational exercise with no equivalent elsewhere.',
 'Online direct orders; specialty tea retailers.',
 'premium', 2, 'Kyoto Obubu Tea Farms official materials; international tea media coverage', true, true),

('Yamamotoyama', 'tea_garden', 51, 'Japan',
 'accessible_heritage',
 'Yamamotoyama, founded in 1690 by the Yamamoto family in Edo (Tokyo), is Japan''s oldest tea company still in operation and one of the first to develop commercial nori (seaweed) products alongside tea. Today the company bridges traditional Japanese green tea education and accessible retail distribution — their matcha and genmaicha are widely available internationally while maintaining a commitment to authentic Uji-sourced tea.',
 '[{"name": "Yamamoto family", "role": "Founded 1690, current generation in management", "notes": "One of Japan''s great merchant tea families; pivoted from pure tea trading to production and now to international distribution while maintaining product integrity"}]',
 '{"specialties": "Gyokuro (Oi Ocha brand); matcha; genmaicha (rice tea); sencha; Japanese teas for North American retail", "distribution": "Wide North American retail distribution through Japanese and Asian grocery channels", "bc_availability": "T&T Supermarket, Japanese grocery stores, Amazon Canada", "founded": "1690"}',
 'market', 'Yamamotoyama provides the most accessible Japanese tea experience in BC — widely available, consistent quality, authentic Uji-sourced product at mid-range prices. Their genmaicha (green tea with toasted rice) and gyokuro are approachable introductions to Japanese green tea for guests new to the category.',
 'Widely available at T&T and Asian grocery stores throughout Metro Vancouver. No allocation required.',
 'entry', 1, 'Yamamotoyama official history (founded 1690); Japanese tea trade documentation', true, true),

('Kagoshima Chiran Tea Cooperative', 'tea_garden', 53, 'Japan',
 'volcanic_terroir',
 'The Chiran Tea Cooperative represents Kagoshima''s collective approach to premium tea production — multiple family farms sharing resources for quality control, stone-milling of matcha, and export development while maintaining individual farm identity in single-origin expressions. The volcanic Shirasu soil of Chiran produces sencha and tamaryokucha (guricha) with a distinctive mineral brightness.',
 '[{"name": "Cooperative management committee", "role": "Elected family farm representatives", "notes": "The cooperative model allows small Kagoshima tea farms to access export markets and premium processing equipment unavailable to individual small farms"}]',
 '{"specialties": "Kagoshima sencha; tamaryokucha (guricha — the pan-fired round-leaf style distinctive to southern Kyushu); matcha", "soil": "Volcanic Shirasu soil from Sakurajima eruptions — unique mineral character", "cultivars": "Saemidori (the most vivid green cultivar; high amino acid content), Yabukita", "bc_availability": "Specialty Japanese tea retailers online and in Metro Vancouver", "founded": "Cooperative structure established 1970s"}',
 'estate', 'Chiran represents Kagoshima''s best expression: bright, vivid green colour from Saemidori cultivar, mineral brightness from volcanic soil, and the natural sweetness that comes from the subtropical climate''s rapid amino acid synthesis. An excellent second step for guests who have discovered they enjoy Japanese green tea through Uji expressions.',
 'Online specialty retailers; some Vancouver Japanese grocery stores.',
 'premium', 2, 'Kagoshima Prefectural Tea Industry documentation; Saemidori cultivar research', true, true),

('Nishide Tea Garden', 'tea_garden', 52, 'Japan',
 'shizuoka_depth',
 'Nishide Tea Garden operates in Shizuoka''s premium Honyama sub-district, producing deep-steamed (fukamushi) sencha — a Shizuoka specialty where the leaves are steamed 2-3x longer than standard sencha, producing a distinctive jade-green liquor of body and intensity. The Honyama microclimate, in a narrow valley with morning mist from the Abe River, creates ideal conditions for this intensive style.',
 '[{"name": "Nishide family", "role": "Traditional Shizuoka farming family, multi-generation", "notes": "The Nishide family has farmed the Honyama valley for generations, developing expertise specific to the deep-steam (fukamushi) technique that characterises their sub-district"}]',
 '{"specialties": "Fukamushi sencha (deep-steamed — Shizuoka specialty); shincha (first flush spring harvest)", "technique": "Fukamushi — steaming time 2-3x standard; produces jade-green liquor with exceptional body, full flavour; some cloudy appearance from broken leaf particles", "region": "Honyama sub-district, Shizuoka — considered among Shizuoka''s finest microterroir", "bc_availability": "Online specialty tea retailers; O5 Tea in Vancouver carries Shizuoka expressions", "founded": "established multi-generation farm"}',
 'estate', 'Nishide''s fukamushi sencha demonstrates that Shizuoka''s volume reputation conceals pockets of extraordinary quality. The deep-steam technique produces a jade-green, body-rich tea that pairs perfectly with Japanese cuisine and shows well as a restaurant house tea for guests who find standard sencha too light.',
 'Online specialty retailers; some Vancouver specialty tea shops.',
 'premium', 2, 'Shizuoka Tea Association; fukamushi sencha production documentation', true, true);

-- ============================================================
-- TEA PRODUCERS — CHINA & IMPORTERS
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Menghai Tea Factory', 'tea_garden', 57, 'China',
 'puerh_institution',
 'Menghai Tea Factory (Da Yi brand) is the institutional standard for compressed pu-erh tea — the largest and most historically significant pu-erh producer in Yunnan. Founded in 1940 by the Chinese National Tea Company, the factory has produced cake recipes (7542 for sheng, 7572 for shou) that have become globally recognised quality benchmarks. Their numbered cake recipes encode the recipe year and harvest grade.',
 '[{"name": "Da Yi Tea Group management", "role": "State-enterprise structure with professional management since privatisation", "notes": "Originally a state-owned enterprise; privatised in 2004; now operates as a premium tea brand while maintaining its role as the institutional reference for pu-erh quality standards"}]',
 '{"specialties": "Sheng pu-erh (7542 recipe — benchmark sheng); Shou pu-erh (7572 recipe — benchmark shou); premium aged expressions; special edition collector cakes", "recipe_coding": "Da Yi''s numbered recipes: first two digits = year of recipe creation; third digit = leaf grade; fourth digit = factory code (1=Menghai)", "bc_availability": "Chinese tea shops and grocery stores; online from T&T and specialty tea retailers; Pacific Coast Tea (Vancouver)", "founded": "1940"}',
 'estate', 'Menghai Tea Factory''s 7542 and 7572 recipes are the global reference points for sheng and shou pu-erh — as foundational to pu-erh knowledge as Bordeaux''s first growths are to Bordeaux. Their vintage cakes, particularly pre-2004 state-enterprise productions, have achieved extraordinary collector prices at Hong Kong auction houses. The factory''s Da Yi brand is the most widely traded pu-erh label globally.',
 'Current production widely available at Chinese tea specialists and T&T; vintage cakes require specialist dealers.',
 'premium', 1, 'A Tea Lover Guide to Pu-erh by Scott Wilson; Da Yi Tea Group official materials; Hong Kong pu-erh auction records', true, true),

('Wuyi Xingcun Tea Industry', 'tea_garden', 58, 'China',
 'wuyi_rock_mastery',
 'Wuyi Xingcun (Xingcun Village) is the geographical heart of zhengyan (authentic rock area) yancha production — located within the Wuyi Mountain UNESCO Nature Reserve''s core growing zone. Their teas carry the maximum terroir premium possible for Wuyi oolong: rock soil mineral character that produces the yanwei (rock flavour/sensation) that distinguishes genuine Wuyi from imitations.',
 '[{"name": "Xingcun Village Tea Cooperative", "role": "Village-level collective with individual tea masters", "notes": "Wuyi Xingcun represents the collective expertise of the village that has produced the most prized rock oolongs for centuries"}]',
 '{"specialties": "Da Hong Pao (Great Red Robe — the most famous Wuyi variety); Rou Gui (Cinnamon Oolong); Shui Xian (Narcissus); charcoal-roasted yancha", "roasting": "Traditional charcoal roasting in ceramic jugs; multiple roasting sessions over months develop complexity without harsh char notes", "zhengyan": "Core UNESCO reserve rock area — maximum mineral terroir premium; distinguish from ban yan (half-rock) and zhou cha (outer area) teas", "bc_availability": "Song Tea Canada (San Francisco based, ships to Canada); specialty Chinese tea retailers", "founded": "Multi-century village tea tradition"}',
 'reserve', 'Wuyi Xingcun zhengyan production is the pinnacle of Chinese oolong — and arguably the most complex tea in the world. The rock terroir''s mineral signature (the yanwei, or rock flavour, which is both a taste and a sensation of extended finish) is not found in any non-rock-area Wuyi production. For sommeliers, understanding the difference between zhengyan (authentic rock), ban yan (half-rock), and zhou cha (outer area) in Wuyi is as important as understanding premier cru versus village Burgundy.',
 'Specialist import required. Song Tea is the premium North American source.',
 'ultra_premium', 1, 'Wuyi Mountain UNESCO documentation; Song Tea educational materials; A Tea Lover Guide to Chinese Tea', true, true),

('Yunnan Sourcing', 'multi_category', 57, 'China',
 'direct_yunnan_access',
 'Yunnan Sourcing (Scott Wilson) is the most transparent and educational direct-import pu-erh and Yunnan tea source available to the Western market. Scott Wilson has lived in Yunnan since 2004, maintaining direct relationships with specific farmers and factories, and provides more detailed provenance information (specific mountain, village, harvest date, processing notes) than any other source accessible to the North American market.',
 '[{"name": "Scott Wilson", "role": "Founder, direct-import specialist", "notes": "Wilson''s book A Tea Lover Guide to Pu-erh is the definitive English-language reference on the category; his direct farmer relationships and transparency are unique in the industry"}]',
 '{"specialties": "Sheng pu-erh from specific Yunnan mountains (Lao Ban Zhang, Yi Wu, Bing Dao, Jing Mai); aged shou pu-erh; Yunnan black teas (Dianhong); factory cakes and individual farmer maocha", "transparency": "Batch-specific provenance information; exact harvest dates; farmer identification", "bc_availability": "Online direct from yunnansourcing.com (US and EU warehouses); ships to Canada", "founded": "2004"}',
 'reserve', 'Yunnan Sourcing is the recommended source for any BC restaurant seeking genuine, provenance-documented pu-erh and Yunnan tea. The provenance information provided — specific mountain, village, harvest date, processing method — enables the kind of storytelling that distinguishes a serious beverage programme from a generic Asian tea offering. Scott Wilson''s book is an essential reference for any sommelier working with pu-erh.',
 'Online orders ship to Canada. No allocation — wide range of current and vintage productions.',
 'ultra_premium', 1, 'Yunnan Sourcing official materials; A Tea Lover Guide to Pu-erh by Scott Wilson', true, true),

('Song Tea & Ceramics', 'tea_garden', 58, 'China',
 'north_american_connoisseur',
 'Song Tea & Ceramics (San Francisco) is the premier North American source for connoisseur-level Wuyi rock oolong, Taiwan high-mountain oolong, and Yunnan pu-erh. Owner Peter Luong travels to origin annually to taste and select teas at source, then provides them with the kind of wine-like tasting notes and provenance documentation that Western beverage professionals understand. The accompanying ceramics collection reflects the gongfu cha aesthetic at the highest level.',
 '[{"name": "Peter Luong", "role": "Owner and chief selector", "notes": "Luong''s wine-informed approach to tea selection and documentation has made Song Tea the go-to source for Michelin-starred restaurant tea programmes in North America; his annual origin trips are extensively documented"}]',
 '{"specialties": "Wuyi rock oolongs (zhengyan Da Hong Pao, Rou Gui, Shui Xian); Taiwan high-mountain oolongs; Phoenix Dancong; aged sheng pu-erh", "north_american_role": "The premium reference source for gongfu cha in North America; supplies Michelin-starred restaurants", "bc_availability": "Online orders from songtea.com; ships to Canada", "founded": "2010"}',
 'reserve', 'Song Tea is the highest-tier North American tea sourcer for serious beverage programmes. Their Wuyi zhengyan teas in particular — selected annually at source and documented with wine-level provenance information — are appropriate for Michelin-starred and aspirational fine dining contexts. For any BC restaurant building a serious tea programme, Song Tea is the natural starting point.',
 'Online orders to Canada; some expressions limited quantity.',
 'ultra_premium', 1, 'Song Tea & Ceramics official materials; Eater SF coverage; Michelin restaurant tea programme documentation', true, true),

('West Lake Longjing Tea Cooperative', 'tea_garden', 59, 'China',
 'xi_hu_longjing_protection',
 'The West Lake Longjing Tea Cooperative manages and certifies production from the GI-protected Xi Hu (West Lake) designated growing zone around Hangzhou, Zhejiang. The cooperative''s certification is the only guarantee of authentic West Lake Longjing — distinguishing genuine zhengcha (authentic tea from the designated zone) from the much larger volume of Longjing-style teas produced throughout Zhejiang.',
 '[{"name": "Hangzhou government cooperative management", "role": "Government-supported producer collective", "notes": "The Xi Hu Longjing GI designation and its enforcement through the cooperative is modelled partly on European appellation systems"}]',
 '{"specialties": "Xi Hu Longjing (West Lake Dragon Well) — the authentic GI protected grade; pre-Qingming (Before Pure Brightness — early April) first harvest commands highest prices", "gi_zone": "18 specific mountain and hillside zones around West Lake, Hangzhou — strictly delineated by GI", "imperial_trees": "18 imperial tribute trees designated by Emperor Qianlong in the 18th century — still harvested; their ultra-limited production auctioned annually", "bc_availability": "Specialty Chinese tea retailers; some T&T locations", "founded": "GI formal establishment 2008; century-long cooperative tradition"}',
 'estate', 'West Lake Longjing is the Champagne of Chinese green tea — a GI-protected name that guarantees specific terroir (West Lake zone, Hangzhou), cultivar (Dragon Well varieties), and processing (hand pan-fired). Outside the GI zone, any Longjing-style tea must be labelled with its actual origin, not "West Lake." Understanding and communicating this distinction is essential for credible Chinese tea programming.',
 'Specialty Chinese tea retailers; online from dedicated Chinese tea importers. Pre-Qingming grades limited.',
 'premium', 1, 'Xi Hu Longjing GI documentation; Hangzhou Longjing Tea Research Institute', true, true),

('Phoenix Village Fenghuang Dancong', 'tea_garden', 60, 'China',
 'single_bush_excellence',
 'Phoenix Village (Fenghuang Cun) at the summit of Chaozhou''s Fenghuang Mountain is the origin of authentic Dan Cong oolong. The village''s individual farming families maintain named cultivar trees — some claimed to be hundreds of years old — producing the Mi Lan Xiang (Honey Orchid), Ya Shi Xiang (Duck Excrement), and other named varieties that are the pinnacle of Chinese oolong.',
 '[{"name": "Village collective — individual family farms", "role": "Traditional mountain farming families maintaining named cultivar trees", "notes": "Each Dan Cong variety is associated with specific families or tree lineages; the most prized old-tree examples command extraordinary prices"}]',
 '{"specialties": "Mi Lan Xiang (Honey Orchid Fragrance) — the most widely known Dan Cong; Ya Shi Xiang (Duck Excrement — honey, stone fruit, mineral); Ba Xian (Eight Immortals — complex multi-floral); Song Zhong (Song Dynasty — oldest surviving variety)", "cultivar_naming": "Dan Cong varieties named for aromatic characteristics or historical context; Ya Shi Xiang''s ironic name (referring to the earthy fertiliser smell of old tree soils) is a famous tea naming story", "bc_availability": "Floating Leaves Tea (Seattle, ships to BC); Song Tea; specialty Chinese tea retailers", "founded": "Multi-century cultivated tree tradition"}',
 'estate', 'Phoenix Dancong is the most complex oolong produced outside of the Wuyi Mountains — each named variety (Mi Lan Xiang, Ya Shi Xiang, Ba Xian) carries a distinct aromatic fingerprint, and the comparison of three or four varieties side-by-side is one of the world''s great comparative tasting experiences. For sommeliers, Dancong tasting is the Chinese tea equivalent of blind comparative vertical tasting: an exercise in aromatic identification and flavour memory.',
 'Floating Leaves Tea (Seattle, ships to BC); Song Tea. Some expressions limited.',
 'premium', 1, 'Chaozhou Tea Culture Research Institute; Gongfu Cha by Warren Peltier; Floating Leaves Tea educational materials', true, true),

('Floating Leaves Tea', 'tea_garden', 60, 'China',
 'seattle_pacific_gateway',
 'Floating Leaves Tea (Seattle) is the Pacific Northwest''s most respected tea importer for Taiwan oolong and Chinese connoisseur teas, positioned as the natural Pacific Rim gateway for BC restaurants and retailers. Owner Shiuwen Tai travels annually to Taiwan''s high-mountain tea regions, maintains direct relationships with specific Alishan and Lishan farmers, and provides the kind of harvest-specific and farmer-level documentation that supports serious restaurant tea programmes.',
 '[{"name": "Shiuwen Tai", "role": "Owner and head buyer, Taiwan tea specialist", "notes": "Tai''s annual trips to Taiwan''s high-mountain growing regions and direct farmer relationships make Floating Leaves the most reliable source for authentic gaoshan oolong; her educational approach mirrors wine importers of the finest calibre"}]',
 '{"specialties": "Taiwan high-mountain oolong (Alishan, Lishan, Dayuling, Shanlinxi); Taiwan Oriental Beauty; Phoenix Dancong; Wuyi rock oolong; seasonal first-flush purchases", "bc_proximity": "Seattle-based; ships to Canada; ideal Pacific Northwest tea source for BC restaurants", "harvest_specificity": "Harvest date, specific farm, and farmer documented for all Taiwan teas", "bc_availability": "Ships to Canada from floatingleavestea.com; ideal source for BC restaurant programmes", "founded": "2007"}',
 'estate', 'Floating Leaves Tea is the natural primary source for any BC restaurant building a Taiwan oolong or Chinese connoisseur tea programme. Shiuwen Tai''s annual direct-farm sourcing, combined with Seattle''s proximity to Vancouver, makes this the most logistically appropriate and quality-assured premium tea source in the Pacific Northwest. Every tea comes with the kind of origin documentation that enables genuine storytelling.',
 'Online orders to Canada; seasonal limited harvests require advance purchase notification signup.',
 'premium', 1, 'Floating Leaves Tea official materials; Pacific Northwest tea community; Taiwan Tea Promotion Center', true, true),

('Rishi Tea & Botanicals', 'multi_category', 57, 'China',
 'accessible_direct_trade',
 'Rishi Tea (Milwaukee, with Pacific Northwest distribution strength) pioneered certified organic and direct-trade tea in the North American market from 1997, maintaining relationships with certified growers in China, Japan, Taiwan, India, and beyond. Their extensive portfolio covers the breadth of the tea world at accessible price points without sacrificing authenticity or traceability.',
 '[{"name": "Joshua Kaiser", "role": "Founder", "notes": "Kaiser''s early commitment to direct trade and certified organic tea preceded the mainstream interest in food provenance — a pioneer whose standards have shaped the industry''s practices"}]',
 '{"specialties": "Certified organic teas across all categories; Phoenix Dancong; Wuyi rock oolong; Taiwan oolong; single-origin Japanese greens; herbals and botanicals", "bc_availability": "Whole Foods Market, specialty grocery, online; one of the most accessible premium tea brands in BC", "certifications": "Certified organic, direct trade; USDA organic", "founded": "1997"}',
 'market', 'Rishi Tea provides the most accessible entry point to authentic, provenance-documented tea in the BC market — wide retail availability at Whole Foods and specialty grocers, consistent quality, and genuine direct-trade relationships. Their Phoenix Dancong and Wuyi Rou Gui are excellent stepping stones from introductory Chinese tea into the connoisseur realm.',
 'Wide BC availability at Whole Foods, specialty grocers, and online. No allocation required.',
 'mid_range', 1, 'Rishi Tea official history; direct trade tea industry documentation', true, true);

-- ============================================================
-- BAIJIU PRODUCERS — CHINA
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Kweichow Moutai Group', 'distillery', 61, 'China',
 'jiangxiang_supremacy',
 'Kweichow Moutai is China''s national spirit brand, the diplomatic spirit of the People''s Republic, and by market capitalisation the world''s most valuable spirits company. The sauce aroma (jiangxiang) style produced in Maotai town''s river valley — through 8 rounds of fermentation, 9 rounds of distillation, and 3-5 years of barrel-free pot ageing — is fundamentally unlike any Western spirit. The Chishui River''s specific microbial ecology is considered essential terroir.',
 '[{"name": "Li Baofang", "role": "Chairman, Kweichow Moutai Group", "notes": "Leadership of the most strategically important spirits company in China''s diplomatic and commercial history"}, {"name": "Zhang Deqin", "role": "Chief Distiller", "notes": "Oversees the technical production team responsible for maintaining the consistency of China''s most scrutinised spirit"}]',
 '{"base_material": "Hong ying zi sorghum (small red kaoliang) from Guizhou, plus wheat for qu", "fermentation": "Solid-state in earthen pits; 8 rounds over 1 year; each round adds new sorghum while preserving prior round dregs", "distillation": "9 rounds of distillation; each round produces different character spirit blended for final product", "ageing": "3-5 years minimum in traditional ceramic jars; no wood contact", "bc_availability": "T&T Supermarket; specialty Chinese liquor stores (Burnaby, Richmond); Pacific Coast Cellars", "market_cap": "Largest spirits company globally by market capitalisation (2023: approximately USD 230 billion)", "founded": "1951 (modern state enterprise); claimed historical lineage to 200+ years of Maotai village production"}',
 'reserve', 'Kweichow Moutai is the most diplomatically important spirit in the world. Every significant event in China''s foreign policy — from Nixon''s 1972 Beijing visit to modern Belt and Road summits — has involved Moutai. For sommeliers, understanding Moutai is understanding Chinese culture at the deepest level: the spirit is not separate from Chinese business culture; it is inseparable from it. At BC restaurants serving Chinese business clientele, Moutai recognition and service knowledge is a significant commercial advantage.',
 'Flying Fairy (Fei Tian) widely available at T&T and Chinese liquor stores; Aged expressions (15-year, 30-year) require specialist sourcing.',
 'ultra_premium', 1, 'Derek Sandhaus Baijiu: The Essential Guide to Chinese Spirits; Kweichow Moutai official history; Chinese diplomatic records', true, true),

('Wuliangye Group', 'distillery', 62, 'China',
 'five_grain_complexity',
 'Wuliangye (Five Grain Liquor) is China''s second-most prestigious baijiu brand, producing the strong aroma (nongxiang) style with a unique five-grain blend: sorghum, rice, glutinous rice, wheat, and corn. Each grain contributes distinct fermentation compounds, creating a spirit of exceptional complexity — pineapple-forward ester character, rich body, and extended finish. The production involves earthen pit fermentation pits in continuous use for centuries.',
 '[{"name": "Wuliangye Group board", "role": "Corporate state-enterprise management structure", "notes": "One of China''s most strategically important spirits enterprises; Wuliangye''s five-grain recipe is its primary differentiator and is closely guarded"}]',
 '{"base_material": "Five grains: sorghum (36%), rice (22%), glutinous rice (18%), wheat (16%), corn (8%)", "fermentation": "Solid-state in earthen pits; some pits in continuous use since Ming Dynasty", "water": "Minjiang River, Yibin, Sichuan", "ageing": "Minimum 5 years; premium expressions 10-60 years", "bc_availability": "T&T Supermarket; Chinese specialty liquor stores; Pacific Wines & Spirits", "founded": "Documented to Ming Dynasty (1368–1644); modern enterprise structure 1959"}',
 'reserve', 'Wuliangye''s five-grain formula creates the definitive nongxiang (strong aroma) baijiu — a style accounting for over 70% of China''s total baijiu consumption. Its pineapple and tropical fruit ester character is the most recognisable Chinese spirit profile globally. Understanding the difference between Wuliangye''s complex five-grain nongxiang and Moutai''s austere sorghum-only jiangxiang is the foundational literacy of Chinese spirits.',
 'Classic and Premium expressions at T&T and Chinese liquor stores; aged expressions through specialist importers.',
 'ultra_premium', 1, 'Derek Sandhaus Baijiu: The Essential Guide; Wuliangye Group official history', true, true),

('Luzhou Laojiao', 'distillery', 62, 'China',
 'ancient_pit_fermentation',
 'Luzhou Laojiao (Old Cellar of Luzhou) is the holder of China''s most historically significant fermentation infrastructure: earthen pit cellars in continuous use since 1573 — over 450 years. These pits, registered as national intangible cultural heritage, have developed a unique microbial community in their clay walls that cannot be replicated elsewhere and is fundamental to the character of Luzhou Laojiao''s strong aroma baijiu.',
 '[{"name": "He Jianghua", "role": "Master Distiller, 23rd generation pit manager", "notes": "The role of pit manager at Luzhou Laojiao is passed generationally — the 23rd generation maintains pits whose microbial culture has been continuous for 450+ years"}]',
 '{"base_material": "Single-grain sorghum; wheat for qu", "fermentation_pits": "1,619 active pits registered; oldest date to 1573; pit mud is its own microbial ecosystem", "national_heritage": "1573 pits designated as National Intangible Cultural Heritage in 2006", "bc_availability": "T&T Supermarket; Chinese specialty liquor stores", "founded": "1573 (pit cellar history); modern enterprise 1952"}',
 'estate', 'Luzhou Laojiao''s 1573 heritage is the strongest terroir story in Chinese spirits — perhaps in any spirits category. The concept of earthen pit culture continuity (the microbial community in 450-year-old pit walls) is genuinely analogous to terroir in wine, and is equally irreproducible elsewhere. A compelling story for sophisticated spirits-literate guests and an essential reference for baijiu education.',
 'Special Grade (Teshu grade) and 1573 expression at T&T and Chinese liquor stores.',
 'premium', 1, 'Derek Sandhaus Baijiu: The Essential Guide; Luzhou Laojiao Heritage documentation; Chinese intangible cultural heritage registry', true, true),

('Fenjiu Group', 'distillery', 61, 'China',
 'qingxiang_clarity',
 'Fenjiu Group produces the definitive light aroma (qingxiang) baijiu — a fundamentally different philosophy from the sauce and strong aroma styles. Using pure sorghum in ceramic pots (rather than earthen pits), Fenjiu''s single-distillation method produces a clean, crisp spirit where grain character is maximally expressed without the microbial complexity of pit fermentation. This is baijiu at its most transparent.',
 '[{"name": "Fenjiu Group board", "role": "State enterprise management", "notes": "Fenjiu''s production in Shanxi province''s Xinghuacun (Apricot Blossom Village) has been documented since the sixth century; among the oldest distilling traditions in China"}]',
 '{"base_material": "Sorghum (qingcha variety)", "fermentation": "Underground ceramic pots (rather than earthen pits) — prevents the complex microbial development of pit fermentation", "distillation": "Clean, single-distillation; lower congener content than sauce or strong aroma styles", "bc_availability": "T&T Supermarket; Chinese specialty liquor stores", "region": "Xinghuacun, Shanxi Province — home of the qingxiang style", "zhuyeqing": "Fenjiu also produces Zhuyeqing — bamboo leaf green herb-infused baijiu; first herb-infused baijiu documented in Tang Dynasty imperial records", "founded": "Historical Xinghuacun distilling tradition documented to 6th century; modern enterprise 1949"}',
 'estate', 'Fenjiu provides the clearest introduction to baijiu for Western guests: its light aroma (qingxiang) style, cleaner and less intense than sauce or strong aroma, bridges the gap between familiar spirits and the challenging complexity of Moutai or Wuliangye. Fenjiu''s associated Zhuyeqing (bamboo leaf green, a herb-infused expression) has been produced since the Tang Dynasty and represents a remarkable historical continuity.',
 'Blue and White (Lan He Bai) expression and Zhuyeqing widely available at T&T.',
 'premium', 1, 'Derek Sandhaus Baijiu: The Essential Guide; Fenjiu Group official history', true, true),

('Guilin Sanhua', 'distillery', 60, 'China',
 'rice_aroma_elegance',
 'Guilin Sanhua produces the definitive rice aroma (mixiang) baijiu — the fourth major aroma style, using 100% rice (rather than sorghum) as the base. Made in Guangxi''s Guilin, using the region''s famous Lijiang River water and a small-jar semi-solid fermentation method, the result is a clean, slightly floral, rice-forward spirit that is the most approachable baijiu style for Western palates.',
 '[{"name": "Sanhua management", "role": "Traditional Guilin distilling management", "notes": "Guilin Sanhua maintains a 400+ year production history using the distinctive small ceramic jar fermentation method that produces the mixiang style"}]',
 '{"base_material": "100% rice — distinctly different base from sorghum-dominant baijiu styles", "fermentation": "Small ceramic jars (buried in the ground); semi-solid state", "water": "Lijiang River, Guilin — famous for clarity and low mineral content", "bc_availability": "Limited; specialty Chinese liquor stores; some T&T locations", "aroma_type": "Mixiang (rice aroma) — fourth of four major baijiu aroma categories; cleanest and most floral", "founded": "Over 400 years of documented production in Guilin"}',
 'market', 'Guilin Sanhua''s rice aroma (mixiang) baijiu is the natural starting point for guests who are curious about baijiu but intimidated by Moutai''s intensity. Rice as a base produces a cleaner, lighter, more floral spirit without the overwhelming complexity of sauce or strong aroma styles. An excellent educational next step after sake for guests exploring Asian fermented grains.',
 'Limited BC availability; some T&T and Chinese specialty stores.',
 'mid_range', 2, 'Derek Sandhaus Baijiu: The Essential Guide; Guilin Sanhua official history', true, true);

-- ============================================================
-- TEA PRODUCERS — TAIWAN
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Alishan Tea Cooperative', 'tea_garden', 63, 'Taiwan',
 'altitude_harvest',
 'The Alishan Tea Cooperative represents the collective production of Alishan mountain''s (1,000–1,800m) family farms, maintaining quality standards for the gaoshan (high mountain) designation while sharing processing facilities and export logistics. Alishan''s lower-altitude teas (1,000–1,300m) provide more volume and accessibility; the higher farms (1,500–1,800m) produce the most concentrated flavours.',
 '[{"name": "Alishan Farmers Association", "role": "Cooperative coordination and certification", "notes": "The Alishan Farmers Association conducts biannual tea competitions (spring and winter) that grade and price the cooperative''s output; competition-grade teas fetch premium prices"}]',
 '{"specialties": "Qingxin (Green Heart) oolong — the prestige Taiwan cultivar; Jinxuan (TRES #12) with natural milky note; Cuiyu (TRES #13) green floral", "elevation": "1,000–1,800m; gaoshan designation requires 1,000m minimum", "competition": "Biannual Alishan competition awards: Special Grade (金牌/gold), First Grade (銀牌/silver), etc.", "bc_availability": "Floating Leaves Tea (Seattle, ships to BC); online Taiwan tea retailers; some Vancouver tea shops", "founded": "Commercial high-mountain tea cultivation began 1980s–1990s"}',
 'estate', 'Alishan tea is the entry point to Taiwan''s high-mountain oolong world — the most accessible of the gaoshan elevations, offering the characteristic butter-cream sweetness, floral notes, and lingering finish that makes Taiwan oolong distinctive from Chinese oolong. For sommeliers new to Taiwan tea, Alishan Qingxin is the reference standard: clearly delicious, clearly distinctive, and clearly worth the premium over lower-altitude equivalents.',
 'Floating Leaves Tea (Seattle, ships to BC); online Taiwan tea retailers.',
 'premium', 1, 'Alishan Farmers Association documentation; Floating Leaves Tea educational materials', true, true),

('Wang Family Tea Farm', 'tea_garden', 63, 'Taiwan',
 'dayuling_supremacy',
 'Wang Family Tea Farm operates at Taiwan''s highest cultivated tea elevation — Dayuling, 2,200–2,600m — producing what many consider the world''s finest high-mountain oolong. At Dayuling''s extreme altitude, the growing season extends dramatically (each 100m of elevation adds approximately one week to bud development), concentrating amino acids, aromatic compounds, and polyphenols to extraordinary levels. The Wang family has farmed Dayuling for decades, maintaining old Qingxin cultivar plants.',
 '[{"name": "Wang family", "role": "Multi-generation Dayuling farming family", "notes": "The Wang family''s decision to farm at 2,200–2,600m elevation — the absolute limit of viable tea cultivation in Taiwan — has produced teas that regularly achieve the highest competition grades and the highest per-gram prices of any Taiwan oolong"}]',
 '{"specialties": "Dayuling gaoshan Qingxin oolong — the highest-elevation Taiwan tea available; also Lishan oolong (1,600–2,200m)", "elevation": "Dayuling: 2,200–2,600m; the highest viable tea cultivation in Taiwan", "cultivar": "Qingxin (Green Heart) — the traditional prestige cultivar; slower-growing, more complex than modern Jinxuan", "bc_availability": "Floating Leaves Tea (Seattle); Song Tea; specialist Taiwan tea importers", "production_note": "Extremely small annual production; entire annual harvest can sell in days through allocation systems"}',
 'reserve', 'Dayuling oolong from Wang Family Tea Farm is the pinnacle of what altitude can do to tea. The extreme elevation slows growth so dramatically that each bud develops over weeks rather than days, accumulating amino acids (theanine) and aromatic compounds to levels impossible at lower altitudes. The result is a tea of extraordinary sweetness, length, and complexity — genuinely comparable to first-growth wine in its combination of terroir uniqueness and quality peak.',
 'Floating Leaves Tea (Seattle, ships to BC); Song Tea. Seasonal harvest — sell out quickly. Pre-order recommended.',
 'ultra_premium', 1, 'Wang Family Tea Farm official materials; Floating Leaves Tea sourcing documentation; Taiwan tea competition records', true, true),

('Dong Ding Tea Cooperative', 'tea_garden', 64, 'Taiwan',
 'traditional_roast_mastery',
 'The Dong Ding Tea Cooperative represents the traditional Lugu-area production that gave Taiwan oolong its foundations. Their medium-roast, medium-oxidation traditional Dong Ding style — roasted over charcoal in cloth-wrapped balls, multiple sessions building complexity — is the classic reference for Taiwan''s historic tea tradition, now increasingly contrasted with the lighter high-mountain style.',
 '[{"name": "Lugu Farmers Association management", "role": "Competition administration and cooperative coordination", "notes": "The Lugu Farmers Association biannual Dong Ding competition (spring and winter) is Taiwan''s most prestigious and longest-running tea competition"}]',
 '{"specialties": "Traditional Dong Ding oolong — medium oxidation (25–40%), charcoal roasted; competition-grade (Special Grade) and standard grades", "competition": "Lugu Farmers Association competition: Special (金牌), First (頭等), Second (貳等), Third (參等) grades", "roasting": "Traditional charcoal roasting over multiple sessions; develops caramel, stone fruit notes without harsh char", "bc_availability": "Floating Leaves Tea; Taiwan tea specialists online", "founded": "Lugu competition established 1975; cooperative tradition older"}',
 'estate', 'Traditional Dong Ding represents a style that is genuinely distinct from the modern high-mountain oolong trend — deeper, richer, with roast complexity that high-mountain oolongs deliberately avoid. For sommeliers, comparing traditional Dong Ding (roasted, aged style) with modern Alishan gaoshan (fresh, floral, minimal roast) is one of the most educational comparative tastings in the Taiwan tea world. Both are superb; they serve different contexts.',
 'Floating Leaves Tea; online Taiwan tea specialists.',
 'premium', 1, 'Lugu Farmers Association documentation; A Tea Lover Guide to Taiwanese Tea; Floating Leaves Tea', true, true);

-- ============================================================
-- TEA PRODUCERS — INDIA
-- ============================================================
INSERT INTO beverage_producers (name, producer_type, region_id, country, production_philosophy, philosophy_description, key_personnel, production_details, quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier, source_text, is_verified, is_published) VALUES

('Makaibari Tea Estate', 'tea_garden', 65, 'India',
 'biodynamic_darjeeling',
 'Makaibari, established 1859 by the Banerjee family, is the world''s oldest tea estate and Darjeeling''s most philosophically ambitious producer. Under the visionary fourth-generation Rajah Banerjee (now continued by the next generation), Makaibari pioneered biodynamic tea cultivation in India, creating an estate where wild forest, tea, and community coexist in what has become the model for sustainable luxury tea production globally.',
 '[{"name": "Rajah Banerjee", "role": "Fourth-generation estate leader, biodynamic pioneer", "notes": "Banerjee''s transformation of Makaibari into a biodynamic estate in the 1980s — decades before ''sustainability'' became a marketing term — represents one of the great acts of agricultural vision in tea history"}, {"name": "Makaibari management", "role": "Estate management and export division", "notes": "The estate is now managed with Rajah''s guidance and successive generation involvement"}]',
 '{"estate_size": "2,500 acres including 600 acres of tea and 1,900 acres of wild forest — the forest is considered essential to the biodynamic system", "certifications": "Demeter biodynamic certified; Fairtrade; organic", "specialties": "First flush Darjeeling; Second flush muscatel (Silver Tips Imperial is the ultimate expression); autumnal flush; aged leaf collections", "bc_availability": "Specialty tea retailers; Camellia Sinensis (Montreal) ships to BC; online through Makaibari.com", "founded": "1859"}',
 'reserve', 'Makaibari is the Darjeeling estate against which all others are measured. Their Silver Tips Imperial — the rarest first flush expression, harvested only in the brief window before dawn on specific days determined by biodynamic calendar — is among the world''s most expensive teas by weight. The combination of genuine biodynamic production, oldest estate pedigree, and extraordinary quality makes Makaibari the definitive Darjeeling story for fine dining.',
 'Seasonal limited release; pre-order required for first flush and Silver Tips Imperial. Camellia Sinensis Montreal ships to BC.',
 'ultra_premium', 1, 'Makaibari Tea Estate official history; Tea Board of India; Jeff Koehler Darjeeling', true, true),

('Castleton Tea Estate', 'tea_garden', 65, 'India',
 'muscatel_pinnacle',
 'Castleton Tea Estate, high in the Kurseong sub-district of Darjeeling, produces what experts consistently consider the finest second flush muscatel character in the district. Their Moonlight and Castleton Vintage expressions command the highest prices of any Darjeeling tea at international auction, with the muscatel character — floral, grape-like, honied, with extraordinary length — reaching its greatest expression at Castleton''s specific microterrroir.',
 '[{"name": "Goodricke Group", "role": "Estate management (part of the Camellia PLC portfolio)", "notes": "Castleton is managed under the Goodricke umbrella — one of the professional tea estate management companies that has maintained production quality and international distribution"}]',
 '{"elevation": "1,700–2,100m — among Darjeeling''s highest elevations", "specialties": "Second flush muscatel (peak production June; limited quantity); first flush; autumnal", "auction": "Castleton second flush regularly achieves highest prices at Kolkata Tea Auction; international buyers compete for allocation", "bc_availability": "Specialty tea retailers; online from specialty India tea importers", "founded": "1885"}',
 'reserve', 'Castleton Moonlight and Castleton Vintage second flush are the most auctioned and collector-sought Darjeeling teas — the estate whose name appears in the same sentence as ''highest price per kg at auction'' with regularity. The muscatel character at Castleton''s elevation reaches a level of floral-grape intensity that wine sommeliers immediately recognise as analogous to Muscat de Beaume-de-Venise or aged Riesling: aromatic concentration through slow development.',
 'Allocation-based; pre-order through specialty India tea importers.',
 'ultra_premium', 1, 'Tea Board of India; Castleton Tea Estate records; Darjeeling auction house documentation', true, true),

('Glenburn Tea Estate', 'tea_garden', 65, 'India',
 'darjeeling_hospitality',
 'Glenburn Tea Estate, operated as a luxury tea bungalow destination by the Prakash family since 1997, combines premium tea production with one of India''s finest boutique hospitality experiences. Their first and second flush teas are considered among Darjeeling''s finest; their guest programme — working tea estate visits, plucking participation, and bungalow accommodation — has become a model for agritourism in India.',
 '[{"name": "Husna-Tara Prakash", "role": "Owner, hospitality visionary", "notes": "Prakash transformed Glenburn from a purely commercial estate to India''s most celebrated tea tourism destination without sacrificing production quality — a rare achievement"}]',
 '{"elevation": "1,600–2,000m", "specialties": "First flush; second flush muscatel; clonal teas from specific cultivar blocks", "hospitality": "Glenburn Tea Bungalows — luxury accommodation on the working estate; guided plucking, factory tours, curated tea courses for guests", "bc_availability": "Specialty tea retailers; direct from Glenburn estate; Camellia Sinensis ships to BC", "founded": "1860 (estate); hospitality programme 1997"}',
 'estate', 'Glenburn offers the rare combination of genuine premium production quality with the best tea tourism experience in the world. For restaurant professionals, a visit to Glenburn is the equivalent of a winery visit to a premier Burgundy estate — you return with direct producer knowledge and provenance stories that no import sheet can provide. Their teas are excellent; their story is better.',
 'Direct from Glenburn online; Camellia Sinensis Montreal ships to BC.',
 'premium', 1, 'Glenburn Tea Estate official materials; Condé Nast Traveller India luxury tea feature', true, true),

('Jungpana Tea Estate', 'tea_garden', 65, 'India',
 'clonal_muscatel',
 'Jungpana Tea Estate''s distinctive contribution to Darjeeling is their focus on clonal variety tea plants — specific cultivar selections (AV2, B157, TV1) chosen for exceptional muscatel character expression. Their second flush clonal muscatel, produced from specific cultivar blocks at optimal elevation, achieves a precision of character impossible with the more variable Chinese-type (sinensis) seed-grown plants.',
 '[{"name": "Damayanti Mazumdar family", "role": "Owner family, multi-generation", "notes": "The Jungpana family has maintained independent ownership in an era of increasing corporate consolidation of Darjeeling estates — their independence enables quality-focused production decisions"}]',
 '{"elevation": "1,400–2,000m", "specialties": "Second flush clonal muscatel; AV2 and B157 clonal single-variety expressions; first flush", "clonal_focus": "Specific cultivar blocks documented separately: AV2 (high muscatel), B157 (floral-forward), TV1 (body and depth)", "bc_availability": "Specialty tea retailers; online from India tea importers", "founded": "1899"}',
 'estate', 'Jungpana''s clonal expressions represent a kind of precision that is unique in the Darjeeling landscape — rather than blending across the estate, they produce cultivar-specific teas that demonstrate how individual plant genetics shape character within a single terroir. For sommeliers, this maps directly to the concept of clonal selection in viticulture.',
 'Limited quantities; specialty tea importers.',
 'premium', 2, 'Jungpana Tea Estate official materials; Tea Board of India clonal development records', true, true),

('Halmari Tea Estate', 'tea_garden', 66, 'India',
 'assam_premium',
 'Halmari Tea Estate (Jorhat district, Assam) consistently produces what the international specialty tea community considers the finest orthodox Assam tea available — earning the highest prices at the Kolkata Auction for premium Assam and achieving international recognition that few Assam estates reach. Their second flush orthodox teas, with golden tip content and malty depth, define the premium end of the Assam category.',
 '[{"name": "Dhanuka family", "role": "Owner family, modern management", "notes": "The Dhanuka family''s investment in premium orthodox production — at a time when most Assam estates converted to higher-volume CTC — has been vindicated by Halmari''s premium auction results"}]',
 '{"elevation": "70–100m — Assam river plain, classic terroir", "specialties": "Second flush golden tippy orthodox (TGBOP, TGFOP grade designations); Ruby Red Assam (new cultivar); first flush orthodox", "processing": "Orthodox rolling and fermentation; not CTC — intentional choice for premium character", "bc_availability": "Specialty tea retailers online; Camellia Sinensis ships to BC", "founded": "1905"}',
 'reserve', 'Halmari is Assam''s answer to those who claim the region cannot produce premium orthodox tea — their golden tip TGFOP (Tippy Golden Flowery Orange Pekoe) second flush consistently achieves the category''s highest prices and demonstrates that Assam''s natural richness and malt can be elevated to the same plateau as Darjeeling when handled with the same care.',
 'Limited quantities; specialty India tea importers; Camellia Sinensis ships to BC.',
 'ultra_premium', 1, 'Halmari Tea Estate official materials; Kolkata Tea Auction records; specialty tea community documentation', true, true),

('Kairbetta Tea Estate', 'tea_garden', 67, 'India',
 'nilgiri_frost_rarity',
 'Kairbetta Tea Estate, high in the Ooty plateau of Tamil Nadu''s Nilgiri Hills, is the most celebrated producer of frost tea — the extraordinary winter phenomenon (rare December/January nights when frost damages the tea leaves, triggering flavour compound concentration analogous to Botrytis in wine). The estate''s high elevation and exposure make it particularly susceptible to frost events, and the resulting teas achieve a complexity uncharacteristic of the Nilgiri region.',
 '[{"name": "Kairbetta management", "role": "Traditional Nilgiri estate management", "notes": "Kairbetta''s frost tea programme has become internationally recognised as one of the world''s most extraordinary seasonal tea phenomena"}]',
 '{"elevation": "1,800–2,000m — high Ooty plateau", "specialties": "Frost tea (December–January, production dependent on annual frost events); standard Nilgiri BOP (Broken Orange Pekoe); orthodox specialty expressions", "frost_phenomenon": "Overnight frost causes ice crystal damage to leaf cells; upon thawing, enzymatic activity produces aromatic compounds (including geraniol) analogous to Darjeeling muscatel; character cannot be replicated without actual frost", "bc_availability": "Specialty tea retailers; limited online availability", "founded": "1890s"}',
 'estate', 'Kairbetta''s frost tea is one of the world''s most compelling wine-analogous tea stories: a natural phenomenon (frost cell damage) that triggers specific biochemical changes producing extraordinary aromatic compounds — exactly as Botrytis cinerea does to grapes for Sauternes. The rarity is genuine: frost events significant enough to trigger the effect are unpredictable and not every year produces suitable conditions. A small annual quantity of an extraordinary tea.',
 'Very limited; specialty import. Annual production varies with frost events.',
 'premium', 1, 'Nilgiri Tea Association; Kairbetta Estate materials; Journal of Agricultural and Food Chemistry Nilgiri frost tea research', true, true),

('Harney & Sons Fine Teas', 'multi_category', 65, 'India',
 'premium_accessibility',
 'Harney & Sons (Millerton, New York) has become the most widely distributed premium tea brand in North American fine dining and retail, while maintaining genuine sourcing relationships with producing estates across Darjeeling, Assam, China, Japan, and Taiwan. Their vertically curated range covers both estate single-origins and signature blends, providing accessible entry points to all major tea categories.',
 '[{"name": "John Harney", "role": "Founder", "notes": "John Harney''s vision of premium tea in a fine dining context — launched when specialty tea in North American restaurants was virtually non-existent — created the category standard that persists today"}, {"name": "Michael Harney", "role": "Current tea director", "notes": "Michael Harney''s The Harney & Sons Guide to Tea is the most widely used educational text for North American hospitality professionals learning tea"}]',
 '{"specialties": "Darjeeling estate teas (Makaibari, Castleton seasonal); Assam; Ceylon; China green and oolong; Japanese green; signature blends (Hot Cinnamon Spice — best-selling tea blend in US fine dining)", "bc_availability": "Premium grocery (Whole Foods, Save-On), specialty tea shops, restaurant wholesale; most accessible premium tea brand in BC", "educational": "Harney & Sons Guide to Tea by Michael Harney — standard hospitality reference", "founded": "1983"}',
 'market', 'Harney & Sons is the pragmatic starting point for BC restaurants building a tea programme — widely available, consistently reliable quality, understood by guests who have encountered it in other contexts, and supported by comprehensive educational materials (Michael Harney''s Guide to Tea). Their estate Darjeeling and Assam expressions provide genuine quality at accessible prices without requiring specialist import.',
 'Wide BC availability: Whole Foods, Save-On Foods, restaurant wholesale. No allocation required.',
 'mid_range', 1, 'Harney & Sons official history; The Harney & Sons Guide to Tea by Michael Harney', true, true);

COMMIT;
