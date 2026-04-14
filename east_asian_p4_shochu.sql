-- EAST ASIAN SESSION — PHASE 4: SHOCHU & AWAMORI PRODUCTS (15)
-- Producer IDs: Kirishima=112, Nishi-Shuzo=113, Sanwa-Shurui(Iichiko)=114
--               Komasa=115, Nikaido=116, Zuisen=117, Helios=118, Kumesen=119
-- Region IDs: Kagoshima-Shochu=54, Oita=55, Okinawa=56

BEGIN;

-- ============================================================
-- IMO SHOCHU — KAGOSHIMA (6 products)
-- ============================================================
INSERT INTO beverage_products (name, category, subcategory, producer_id, region_id, origin_country, description, is_vintage_specific, quality_tier, quality_hierarchy, deductive_profile, service_specs, flavour_markers, flavour_weight, flavour_profile_type, origin_brand, price_tier, price_range_cad, technical_specs, is_published) VALUES

('Kuro Kirishima Imo Jochu 25°', 'shochu', 'imo_shochu', 112, 54, 'Japan',
 'The benchmark imo (sweet potato) shochu — Japan''s most commercially successful expression of Kagoshima''s defining spirit. Kuro Kirishima (Black Kirishima) uses Kogane Sengan sweet potatoes from Kagoshima''s volcanic Shirasu soil and black koji (Aspergillus luchuensis) — the traditional Kyushu koji that produces strong citric acid and the characteristic tartness of authentic imo shochu. Single pot distillation preserves every aromatic compound from the sweet potato fermentation. This is the otaku standard against which all other imo shochu are measured.',
 false, 'market',
 '[{"tier": "Category Standard", "criteria": "Benchmark imo shochu; most widely available authentic expression"}, {"tier": "Entry to Premium", "criteria": "Gold Kirishima aged expression above this"}]',
 '{"appearance": "Clear; colourless as all standard shochu", "nose": "Immediately and distinctively imo: sweet potato, volcanic earth, black koji tartness, faint roasted grain. Nothing else smells like this — the Shirasu volcanic soil in the potato''s character is immediately apparent to anyone who has grown or cooked sweet potato in volcanic soil", "palate": "Medium body — much fuller than any sake or lighter spirit; the sweet potato''s natural sugars and starches create a viscous, warming character. Black koji''s tartness provides a refreshing counterpoint to the sweetness. Gentle alcohol warmth at 25%", "finish": "Medium-long; earthy sweet potato tail; the volcanic terroir''s mineral character lingers"}',
 '{"temperature_service": "On the rocks (rokku) — ice with 30-40ml shochu; with cold water (mizu wari) 1:1; with hot water (oyuwari) 6:4 in cold weather — oyuwari unlocks the earthy aromatic compounds", "glassware": "Tumbler or traditional shochu ceramic cup; the earthen character suits rustic glassware", "bc_source": "T&T Supermarket; Japanese specialty grocery stores in Metro Vancouver; Wismettac wholesale", "food_pairing": "Izakaya-style: yakitori, grilled fish, oden, karaage; any savoury umami dish — the earthiness bridges beautifully with savoury character"}',
 ARRAY['sweet potato', 'volcanic earth', 'black koji tartness', 'roasted grain', 'Shirasu mineral', 'warming umami'],
 'medium', 'earthy_warming', 'Kuro Kirishima',
 'mid_range', '$35-$50 CAD (720ml)',
 '{"base_material": "Kogane Sengan sweet potato from Kagoshima volcanic Shirasu soil", "koji": "Black koji (Aspergillus luchuensis) — traditional Kyushu method", "distillation": "Single pot atmospheric distillation — preserves maximum aromatic compounds", "alcohol": "25%", "nihonshu_do": "N/A — shochu classification different from sake", "water": "Kirishima mountain water", "gi_designation": "Satsuma Shochu GI — Kagoshima prefectural designation"}',
 true),

('Red Kirishima Imo Jochu 25°', 'shochu', 'imo_shochu', 112, 54, 'Japan',
 'Red Kirishima uses the Beniharuka sweet potato variety — a different cultivar from the Kogane Sengan of Kuro Kirishima — producing a distinctly lighter, sweeter, and more floral imo shochu. The name references the ''red'' (beni) quality of the Beniharuka potato''s character rather than its appearance. A more approachable entry into the imo shochu world for guests who find Kuro Kirishima''s earthy intensity initially challenging.',
 false, 'market',
 '[{"tier": "Accessible Imo Shochu", "criteria": "Beniharuka cultivar; lighter, sweeter than Kuro Kirishima; gateway expression"}]',
 '{"appearance": "Clear, colourless", "nose": "Noticeably lighter and sweeter than Kuro Kirishima: sweet potato candy note, white flower, light honey, faint vanilla. The Beniharuka variety''s natural sweetness dominates", "palate": "Lighter body than Kuro Kirishima; the sweetness is more present; less volcanic earth character. Approachable and pleasant", "finish": "Clean, medium; light sweet potato tail; more accessible than the traditional Kuro"}',
 '{"temperature_service": "On the rocks; cold water mix (mizu wari); refreshing in summer", "bc_source": "T&T Supermarket; some specialty Japanese stores"}',
 ARRAY['sweet potato candy', 'white flower', 'light honey', 'vanilla', 'gentle sweetness', 'beniharuka character'],
 'medium-light', 'sweet_floral', 'Red Kirishima',
 'mid_range', '$35-$50 CAD (720ml)',
 '{"base_material": "Beniharuka sweet potato — lighter, sweeter cultivar vs. Kogane Sengan of Kuro Kirishima", "koji": "White koji — produces lighter acidity than black koji, allowing the Beniharuka''s sweetness to dominate", "distillation": "Single pot atmospheric", "alcohol": "25%"}',
 true),

('Toko Imo Shochu 25°', 'shochu', 'imo_shochu', 113, 54, 'Japan',
 'Toko is Nishi Shuzo''s signature imo shochu — a craft expression that prioritises depth and complexity over the clean accessibility of Kirishima''s commercial expressions. Small-batch production, carefully selected Kogane Sengan potatoes, traditional black koji, and slow fermentation at lower temperatures produce a shochu of greater aromatic complexity and terroir expression than the category''s volume leaders. The name Toko references a sacred mythological island in Kagoshima, anchoring the spirit in deep local identity.',
 false, 'estate',
 '[{"tier": "Craft Imo", "criteria": "Small batch; selected potato; greater complexity than commercial expressions"}, {"tier": "Above", "criteria": "Toko Premium Aged 40° — single pot, higher strength aged expression"}]',
 '{"appearance": "Clear, slight oiliness visible when swirled — characteristic of hand-selected high-quality potato shochu", "nose": "Complex imo character: earthy sweet potato, black koji tartness, faint roasted grain, something floral (the volcanic soil''s mineral expression in the potato coming through). More layers than the commercial Kirishima expressions", "palate": "Medium body with genuine complexity; the slow, cold fermentation adds dimension — more aromatic compounds preserved. Black koji''s tartness is balanced by the potato''s natural sweetness. Gentle warming rather than hot alcohol", "finish": "Long, 45+ seconds; layered earth and sweet potato; the craft difference is most apparent in the finish''s complexity"}',
 '{"temperature_service": "Best on the rocks (rokku) at 30:50ml ratio; also exceptional warm (oyuwari) with hot food — the warming unlocks the aromatic depth", "bc_source": "Specialty Japanese spirits retailers; limited BC availability — worth ordering", "pairing": "Outstanding with miso-based preparations, grilled pork, robust savoury dishes"}',
 ARRAY['earthy sweet potato', 'black koji tartness', 'roasted grain', 'volcanic mineral flower', 'craft complexity', 'Kagoshima terroir'],
 'medium', 'earthy_complex', 'Toko',
 'premium', '$55-$75 CAD (720ml)',
 '{"base_material": "Hand-selected Kogane Sengan sweet potato, Kagoshima volcanic Shirasu soil", "koji": "Black koji — traditional Kagoshima method", "production": "Small-batch; slow cold fermentation; single pot atmospheric distillation", "alcohol": "25%"}',
 true),

('Toko Premium Aged Imo Shochu 40°', 'shochu', 'aged_imo_shochu', 113, 54, 'Japan',
 'Toko Premium 40° represents the maximum expression of what imo shochu can become with extended ageing at full strength. Distilled at higher than standard proof and rested in stainless steel tanks for 3+ years, the spirit''s sweet potato and black koji character matures and integrates — becoming simultaneously more complex and smoother. This is imo shochu for spirits enthusiasts who have moved beyond the introductory expressions: a serious aged spirit in a distinctly Japanese idiom.',
 false, 'reserve',
 '[{"tier": "Aged Imo Premium", "criteria": "3+ year tank ageing; 40° higher strength; craft complexity"}, {"tier": "Comparison", "criteria": "Compare with aged rum or grappa at the same price tier"}]',
 '{"appearance": "Clear, slight golden tinge from ageing — not from wood but from natural ester development in steel", "nose": "The 3-year ageing is immediately apparent: the raw earthiness of young imo shochu has integrated and elevated into honey, dried sweet potato, faint miso umami, black koji''s tartness now like citrus peel. The volcanic terroir is still present but has been refined rather than dominated", "palate": "40% gives presence and warmth without heat — this is a spirit that can be sipped neat with genuine pleasure. The sweet potato character has become complex: honey, toffee, earth, citrus. The black koji contribution has evolved from tartness to citrus peel depth", "finish": "Long, 60+ seconds; honey and dried sweet potato; mineral tail from the Shirasu soil character preserved through ageing"}',
 '{"temperature_service": "Neat at 18-20°C, or on the rocks with minimal dilution; this expression benefits from a slow opening — leave 5 minutes in the glass before the first sip", "glassware": "Whisky tumbler or Glencairn glass; the 40° strength rewards nose nosing", "bc_source": "Very limited; specialist Japanese spirits import"}',
 ARRAY['dried sweet potato', 'honey', 'citrus peel', 'black koji depth', 'volcanic mineral', 'toffee', 'aged complexity'],
 'medium-full', 'aged_complex', 'Toko Premium',
 'premium', '$80-$110 CAD (720ml)',
 '{"base_material": "Selected Kogane Sengan sweet potato, volcanic Shirasu soil", "koji": "Black koji", "ageing": "3+ years tank rest at full strength; natural ester development", "alcohol": "40%", "production": "Craft small-batch; single pot distillation at higher proof"}',
 true),

('Komasa Sakurajima Imo Shochu 25°', 'shochu', 'imo_shochu', 115, 54, 'Japan',
 'Komasa Jokamachi''s Sakurajima expression is named for the most dramatic element of Kagoshima''s landscape: the Sakurajima volcano, whose periodic eruptions deposit mineral-rich ash onto the surrounding fields. The sweet potatoes used in Sakurajima shochu are grown in soil literally enriched by active volcanic activity — perhaps the most dramatic and literal terroir story in the Japanese spirits world. Single pot distillation, black koji, traditional method.',
 false, 'estate',
 '[{"tier": "Terroir Expression", "criteria": "Volcanic ash-enriched potato soil; most dramatic terroir story in imo shochu"}, {"tier": "Craft", "criteria": "Small-batch artisan production"}]',
 '{"appearance": "Clear, slight viscosity", "nose": "The Sakurajima terroir is immediately apparent to those who know it: more mineral than Kirishima expressions, a hot volcanic rock quality beneath the sweet potato earthiness. Bolder and more assertive than commercial expressions", "palate": "Medium-full body; the volcanic mineral character is the differentiating element — a distinct ashy-mineral quality beneath the black koji and sweet potato. This is imo shochu that tastes like its provenance in an unusually direct way", "finish": "Long; volcanic mineral and sweet potato; the Sakurajima mineral tail is the signature"}',
 '{"temperature_service": "Oyuwari (hot water mix 6:4) to fully open the volcanic mineral aromatic profile; also excellent on the rocks", "bc_source": "Very limited BC availability; specialist Japanese spirits importers"}',
 ARRAY['volcanic ash mineral', 'sweet potato depth', 'black koji', 'hot rock character', 'Sakurajima earth'],
 'medium', 'volcanic_earthy', 'Komasa Sakurajima',
 'premium', '$50-$70 CAD (720ml)',
 '{"base_material": "Kogane Sengan sweet potato grown in Sakurajima volcanic ash-enriched soil", "koji": "Black koji — traditional", "distillation": "Single pot atmospheric", "alcohol": "25%", "terroir_note": "Sweet potatoes grown in soil enriched by Sakurajima volcano''s periodic ash deposits — active volcanic terroir"}',
 true),

('Komasa Jozen Imo Shochu 25°', 'shochu', 'imo_shochu', 115, 54, 'Japan',
 'Komasa''s Jozen expression uses a distinctive white koji fermentation — departing from Kagoshima''s traditional black koji to produce a lighter, more elegant imo shochu. The white koji''s gentler acidity allows the sweet potato''s natural floral and fruity notes (usually overwhelmed by black koji''s assertive tartness) to emerge clearly. An unusual and sophisticated take on the imo shochu category — the Fushimi to Kirishima''s Nada, if the analogy is allowed.',
 false, 'estate',
 '[{"tier": "White Koji Innovation", "criteria": "Non-traditional white koji for imo shochu; lighter, more floral character"}, {"tier": "Style Contrast", "criteria": "Compare with Kuro Kirishima to demonstrate koji''s impact on character"}]',
 '{"appearance": "Crystal clear", "nose": "Completely different from standard imo shochu: lighter, more floral — sweet potato in a summery field rather than volcanic earth. The white koji''s gentleness reveals floral and fruit notes (white flower, light tropical) normally masked by black koji''s tartness", "palate": "Medium-light body; much more approachable than black koji imo expressions; the sweet potato character is present but framed by floral rather than earthy notes. A gateway imo shochu for guests who have found the category too intense", "finish": "Clean, 30-40 seconds; floral sweet potato; elegant"}',
 '{"temperature_service": "Cold water mix (mizu wari) or on the rocks; serve chilled to emphasise the floral character", "bc_source": "Very limited BC; specialist import", "pairing": "More versatile than black koji imo: light Japanese fish dishes, salads, delicate preparations"}',
 ARRAY['white flower', 'floral sweet potato', 'light tropical', 'gentle koji', 'summer elegance'],
 'medium-light', 'floral_elegant', 'Komasa Jozen',
 'premium', '$50-$70 CAD (720ml)',
 '{"base_material": "Kogane Sengan sweet potato, Kagoshima", "koji": "White koji (Aspergillus kawachii) — unusual for Kagoshima imo shochu; produces lighter acidity and reveals potato''s floral notes", "distillation": "Single pot atmospheric", "alcohol": "25%"}',
 true);

-- ============================================================
-- MUGI SHOCHU — OITA (4 products)
-- ============================================================
INSERT INTO beverage_products (name, category, subcategory, producer_id, region_id, origin_country, description, is_vintage_specific, quality_tier, quality_hierarchy, deductive_profile, service_specs, flavour_markers, flavour_weight, flavour_profile_type, origin_brand, price_tier, price_range_cad, technical_specs, is_published) VALUES

('Iichiko Silhouette Mugi Jochu 25°', 'shochu', 'mugi_shochu', 114, 55, 'Japan',
 'Iichiko Silhouette is the product that created the modern category of refined barley (mugi) shochu in Japan. When Sanwa Shurui launched it in 1979 in its distinctive tall, slender bottle (the ''silhouette'' of the bottle itself is the brand''s primary design statement), they repositioned barley shochu from rough agricultural spirit to aspirational lifestyle drink. The spirit itself: clean, slightly sweet, mellow — the barley''s natural gentle character expressed through white koji fermentation and careful distillation. Japan''s most widely drunk shochu brand.',
 false, 'market',
 '[{"tier": "Category Benchmark", "criteria": "Most widely distributed mugi shochu globally; category-defining expression"}, {"tier": "Above", "criteria": "Iichiko Frasco 30° and Iichiko Special 43°"}]',
 '{"appearance": "Crystal clear; the clean distillation is evident", "nose": "Gentle and approachable: barley grain, light malt sweetness, faint white flower, clean alcohol note. Nothing of imo shochu''s earthiness — this is the light, mellow category counterpoint", "palate": "Light body; clean; the barley''s natural sweetness is the primary character without the complexity of imo''s volcanic terroir. White koji''s gentle acidity provides a clean finish without tartness. Very mixable", "finish": "Short-medium; clean barley; refreshing and neutral enough to serve with any Japanese food"}',
 '{"temperature_service": "The standard service: on the rocks (rokku); cold water mix (mizu wari) 1:1; or the classic izakaya serve — chilled Iichiko with soda water (shochu highball). The definitive summer drink of Japan", "bc_source": "T&T Supermarket; Japanese specialty grocery; Wismettac wholesale — widely available", "cocktail_note": "Excellent base for shochu cocktails: the clean, neutral character accommodates citrus, ginger, yuzu without competing"}',
 ARRAY['barley grain', 'light malt sweetness', 'white flower', 'clean alcohol', 'mild sweetness', 'neutral base'],
 'light', 'clean_mellow', 'Iichiko Silhouette',
 'mid_range', '$35-$50 CAD (720ml)',
 '{"base_material": "Two-row barley from Oita and Fukuoka", "koji": "White koji (Aspergillus kawachii) — standard for mugi shochu; gentler than black koji", "distillation": "Column distillation for ultra-clean expression; then blended with pot-still component for character", "alcohol": "25%", "bottle": "The tall silhouette bottle (designed 1979) is one of Japan''s most recognised spirits packaging designs"}',
 true),

('Iichiko Frasco 30° Mugi Jochu', 'shochu', 'mugi_shochu', 114, 55, 'Japan',
 'Iichiko Frasco is the premium tier of the Iichiko range — a higher-strength (30°), pot-still dominant expression that trades the Silhouette''s neutral cleanliness for greater barley character and complexity. The name ''Frasco'' (a Spanish/Portuguese flask) reflects the premium packaging that positions this above the standard range. For guests who have enjoyed Iichiko Silhouette and want more, Frasco is the natural next step.',
 false, 'estate',
 '[{"tier": "Premium Iichiko", "criteria": "30°; pot-still dominant; more barley character"}, {"tier": "Below", "criteria": "Iichiko Silhouette 25°"}, {"tier": "Above", "criteria": "Iichiko Special 43°"}]',
 '{"appearance": "Crystal clear", "nose": "More presence than Silhouette: stronger barley grain, malty sweetness, white flower amplified, faint honey from the pot-still contribution. The extra 5° is apparent without being harsh", "palate": "Medium-light body; noticeably more barley character — this reads as barley spirit rather than neutral shochu base. The white koji''s mellow sweetness frames a genuine grain spirit character", "finish": "Medium; barley malt and honey; cleaner and more distinguished than the Silhouette"}',
 '{"temperature_service": "On the rocks; with cold water; also excellent neat at room temperature — the pot-still character rewards straight sipping", "bc_source": "Wismettac; specialty Japanese spirits retailers"}',
 ARRAY['barley grain', 'malty sweetness', 'honey', 'white flower', 'pot-still grain depth'],
 'medium-light', 'grainy_sweet', 'Iichiko Frasco',
 'premium', '$55-$70 CAD (720ml)',
 '{"base_material": "Two-row barley, Oita", "koji": "White koji", "distillation": "Pot-still dominant for this expression; higher character retention than column-distilled Silhouette", "alcohol": "30%"}',
 true),

('Naka Naka Mugi Shochu 25°', 'shochu', 'mugi_shochu', 116, 55, 'Japan',
 'Naka Naka (whose ironic Japanese name means ''not bad'' or ''so-so,'' a classic understatement for a remarkably complex spirit) is Nikaido Shuzo''s flagship mugi shochu — and among connoisseurs of the category, one of the most sought-after expressions available. The small-batch production, careful selection of Oita-grown two-row barley, white koji fermentation, and traditional copper pot still distillation produce a mugi shochu of genuine depth and character that has nothing to do with Iichiko''s clean neutrality.',
 false, 'estate',
 '[{"tier": "Craft Mugi Premium", "criteria": "Small-batch; pot-still; among the most complexity-forward mugi expressions"}, {"tier": "Connoisseur Category", "criteria": "The expression sought by those who have moved beyond introductory shochu"}]',
 '{"appearance": "Clear, faint golden oiliness", "nose": "Rich barley: malt, honey, biscuit, faint stone fruit, white flower. Clearly a pot-still spirit rather than column-distilled; the aromatic complexity is immediately distinguishable from Iichiko''s clean neutrality", "palate": "Medium body — more viscosity than Iichiko, more extract from pot-still distillation. The barley''s natural sweetness is present alongside a savoury grain depth that recalls premium Single Malt Scotch (conceptually, not stylistically). Complex and interesting", "finish": "Long, 45-60 seconds; honey and grain; the pot-still character provides length that column-distilled shochu cannot achieve"}',
 '{"temperature_service": "Best neat or on the rocks; cold water mix also excellent. Unlike Iichiko, Naka Naka rewards slow sipping neat at room temperature", "glassware": "Tumbler or whisky glass; the aromatic complexity rewards nosing", "bc_source": "Very limited BC availability; specialist Japanese spirits import"}',
 ARRAY['malt barley', 'honey', 'biscuit', 'stone fruit', 'white flower', 'pot-still richness', 'grain depth'],
 'medium', 'rich_complex', 'Naka Naka',
 'premium', '$60-$80 CAD (720ml)',
 '{"base_material": "Selected two-row barley, Oita prefecture", "koji": "White koji", "distillation": "Traditional copper pot still — single pot atmospheric distillation; preserves maximum aromatic compounds from barley fermentation", "production": "Small-batch craft production", "alcohol": "25%"}',
 true),

('Iichiko Special Mugi Jochu 43°', 'shochu', 'mugi_shochu', 114, 55, 'Japan',
 'Iichiko Special (the ''Special'' designation marks full-strength, undiluted genshu production) is the apogee of the Iichiko range — the pot-still expression bottled at 43% without water dilution, presenting the full intensity of Oita barley character. This is the category transition point where mugi shochu begins to occupy the same space as premium Western spirits: genuine complexity, sufficient strength for neat sipping, and enough character to attract spirits enthusiasts beyond the shochu world.',
 false, 'estate',
 '[{"tier": "Iichiko Maximum", "criteria": "43°; undiluted genshu; full barley intensity"}, {"tier": "Crossover Appeal", "criteria": "Attracts whisky and brandy drinkers to the shochu category"}]',
 '{"appearance": "Clear; the additional presence of 43% is faintly visible in the viscosity", "nose": "The full Iichiko character unmasked by water dilution: rich barley grain, honey, malt, white flower, slight coastal mineral note. 43% provides aromatic presence without heat — a well-made spirit at this strength should not present as burning", "palate": "Medium-full body; the 43% adds genuine presence and warmth. The barley character is fully expressed: sweet grain, honey, faint stone fruit. More akin to premium whisky in weight than to shochu served at 25%", "finish": "Long, 50+ seconds; the undiluted strength allows the barley''s natural esters to persist; honey and grain tail"}',
 '{"temperature_service": "Neat at 18-20°C (room temperature, not warmed); or with a single large ice cube to slow dilution. Also excellent with hot water (oyuwari) in colder months", "glassware": "Whisky tumbler or Glencairn glass; this deserves proper whisky service", "bc_source": "Wismettac (limited); specialty Japanese spirits retailers"}',
 ARRAY['rich barley grain', 'honey', 'malt', 'white flower', 'coastal mineral', 'undiluted warmth'],
 'medium-full', 'rich_warming', 'Iichiko Special',
 'premium', '$70-$95 CAD (720ml)',
 '{"base_material": "Two-row barley, Oita", "koji": "White koji", "distillation": "Pot-still dominant; genshu (undiluted — no water added before bottling)", "alcohol": "43%", "genshu_note": "Genshu designation means no water dilution post-distillation — bottled at natural still strength"}',
 true);

-- ============================================================
-- AWAMORI — OKINAWA (5 products)
-- ============================================================
INSERT INTO beverage_products (name, category, subcategory, producer_id, region_id, origin_country, description, is_vintage_specific, quality_tier, quality_hierarchy, deductive_profile, service_specs, flavour_markers, flavour_weight, flavour_profile_type, origin_brand, price_tier, price_range_cad, technical_specs, is_published) VALUES

('Helios Ryukyu Awamori 25°', 'shochu', 'awamori', 118, 56, 'Japan',
 'Helios Distillery''s Ryukyu Awamori is the most accessible entry to Okinawa''s indigenous spirit category — a clean, approachable expression of the island spirit made from 100% Thai indica rice fermented with Okinawa''s traditional black koji (Aspergillus luchuensis). The name Ryukyu references the ancient Ryukyu Kingdom that ruled Okinawa before Japanese annexation — an acknowledgment of the spirit''s pre-Japanese cultural origins.',
 false, 'market',
 '[{"tier": "Awamori Introduction", "criteria": "Most accessible awamori expression; entry to the category"}, {"tier": "Above", "criteria": "Zuisen and Kumesen aged koshu expressions"}]',
 '{"appearance": "Crystal clear", "nose": "Different from shochu immediately: the Thai indica rice base produces a lighter, slightly floral character; black koji''s tartness is present but less assertive than Kagoshima imo; faint tropical fruit note from the indica rice", "palate": "Medium-light body; the indica rice''s lighter starch structure compared to Japanese japonica rice produces a cleaner, less dense spirit. Gentle black koji character. The Okinawan water''s coral limestone filtration adds a slight mineral quality distinct from Kyushu shochu", "finish": "Clean, medium; light rice and black koji; refreshing"}',
 '{"temperature_service": "On the rocks (traditionally); cold water mix; also appropriate mixed with Awamori soda (the Okinawan equivalent of the shochu highball)", "bc_source": "Some BC availability at specialty Japanese spirits retailers", "cultural_context": "Present as: Japan''s oldest distilled spirit; arrived from Southeast Asia 600 years ago; predates shochu; made exclusively in Okinawa from Thai indica rice"}',
 ARRAY['Thai indica rice', 'light tropical flower', 'black koji tartness', 'coral limestone mineral', 'clean rice spirit'],
 'medium-light', 'clean_tropical', 'Helios Ryukyu',
 'mid_range', '$35-$50 CAD (720ml)',
 '{"base_material": "100% Thai long-grain indica rice (imported from Thailand)", "koji": "Black koji (Aspergillus luchuensis) exclusively — original home of black koji; arrived in Okinawa from Southeast Asia before spreading to Kyushu", "water": "Okinawa coral limestone filtered water", "distillation": "Single pot atmospheric", "alcohol": "25%", "category_note": "Awamori is distinct from mainland shochu: different rice (indica vs japonica), different koji strain history, different ageing tradition (clay kame)"}',
 true),

('Zuisen Awamori Koshu 5-Year', 'shochu', 'koshu_awamori', 117, 56, 'Japan',
 'Zuisen''s 5-year Koshu (aged awamori) demonstrates the first stage of what clay pot ageing does to awamori. After five years in traditional terracotta kame, the young awamori''s slightly rough edges have been rounded, the aromas have integrated and deepened, and the first signs of the extraordinary complexity that longer ageing produces are visible. This is the gateway aged awamori — accessible in price, educational in character, essential as an introduction to the koshu tradition.',
 false, 'estate',
 '[{"tier": "Entry Koshu", "criteria": "5-year clay pot ageing; first demonstration of awamori''s ageing potential"}, {"tier": "Above", "criteria": "Zuisen 10-year and Kumesen 25-year for deeper aged expressions"}]',
 '{"appearance": "Clear to very faint gold — the clay pot ageing has added microscopic colour over 5 years without wood contact", "nose": "The transformation from young awamori is apparent: the raw rice spirit character has mellowed into dried fruit (lychee, faint peach), honey, and a subtle earthy note from the clay pot. The black koji''s tartness has softened into citrus peel depth", "palate": "Medium body; rounder and fuller than young Ryukyu awamori; the clay pot''s mineral influence provides a gentle tertiary character. The 5-year integration shows as general harmony rather than specific complexity", "finish": "Medium-long; honey and dried lychee; clay mineral tail — the kame''s contribution is clearest in the finish"}',
 '{"temperature_service": "On the rocks with the minimum ice possible — the aged character deserves slow dilution; also excellent neat at room temperature", "bc_source": "Very limited BC; specialist Japanese spirits import", "service_note": "Compare side-by-side with young Helios Ryukyu to demonstrate the transformation 5 years of kame ageing produces — it is a compelling educational exercise"}',
 ARRAY['dried lychee', 'honey', 'citrus peel', 'clay mineral', 'rounded rice', 'faint tropical'],
 'medium', 'aged_tropical', 'Zuisen Koshu 5-Year',
 'premium', '$55-$75 CAD (720ml)',
 '{"base_material": "100% Thai indica rice", "koji": "Black koji", "ageing": "5 years in traditional terracotta kame (clay pot) at ambient Okinawan temperature", "water": "Coral limestone filtered Okinawan water", "alcohol": "25%", "koshu_designation": "Koshu = aged awamori (at least 3 years); this expression 5 years kame ageing"}',
 true),

('Zuisen Awamori Koshu 10-Year', 'shochu', 'koshu_awamori', 117, 56, 'Japan',
 'Zuisen''s 10-year Koshu represents a genuine departure from anything the Western spirits world typically offers: a 10-year aged spirit with no wood contact whatsoever — the aromas and complexity derive entirely from the terracotta clay pot''s mineral interaction and the slow oxidation through its porous walls. At this age, the awamori has developed a depth that challenges the most experienced spirits palate to categorise. There is nothing quite like this anywhere else in world spirits.',
 false, 'reserve',
 '[{"tier": "Serious Aged Awamori", "criteria": "10-year kame ageing; genuine complexity without wood"}, {"tier": "Category Pinnacle", "criteria": "Reference expression for understanding what clay pot ageing achieves"}]',
 '{"appearance": "Very faint amber — 10 years of clay pot oxidation produces gentle colour from natural ester development", "nose": "Genuinely complex: dried tropical fruit (lychee, longan, dried mango), honey, caramel, faint leather, the clay''s mineral character as a throughline. This does not smell like whisky or brandy or rum — it is its own aromatic universe. The black koji''s tartness has fully transformed into a citrus and leather depth", "palate": "Medium-full body; remarkable for 25% alcohol — the 10-year ageing has added apparent density without strength. The tropical fruit and honey are now integrated with savoury-mineral notes from the clay. A spirit for slow, contemplative sipping", "finish": "60+ seconds; slowly unfolding dried tropical fruit and mineral; no harsh exit — the clay ageing produces a uniquely smooth finish with no wood tannin edge"}',
 '{"temperature_service": "Neat, room temperature; or on the rocks with a single large ice sphere. This deserves the same respect as a premium aged whisky or aged rum", "glassware": "Glencairn whisky glass; the nosing experience at 10 years justifies proper whisky glassware", "bc_source": "Very limited; specialist Japanese spirits import; advance order", "service_narrative": "This is 10 years in clay, not oak. No wood. No barrel. The Okinawan distillers were ageing spirits in clay pots before Scotland had whisky — this is the older tradition."}',
 ARRAY['dried lychee', 'longan', 'dried mango', 'honey', 'caramel', 'clay mineral', 'leather depth', '10-year integration'],
 'medium-full', 'aged_complex', 'Zuisen Koshu 10-Year',
 'premium', '$80-$120 CAD (720ml)',
 '{"base_material": "100% Thai indica rice", "koji": "Black koji", "ageing": "10 years in traditional terracotta kame (clay pot) — no wood contact; oxidation through clay walls", "water": "Coral limestone Okinawan water", "alcohol": "25%", "note": "Zero wood contact throughout 10-year ageing — all complexity derives from clay pot mineralogy and slow oxidation"}',
 true),

('Kumesen Kusu 3-Year Awamori', 'shochu', 'koshu_awamori', 119, 56, 'Japan',
 'Kumesen''s Kusu (the Ryukyuan dialect word for aged awamori — the original name for the category before ''koshu'' was standardised) represents the beginning of Kumesen''s extraordinary ageing programme. At 3 years in traditional kame on Kume Island, the spirit shows the first integration of Okinawa''s coral limestone water character with clay pot ageing — a different mineral signature from the mainland Zuisen expressions. The Kume Island water is considered among Okinawa''s finest for awamori production.',
 false, 'market',
 '[{"tier": "Entry to Kumesen Kusu Range", "criteria": "3-year kame ageing; Kume Island mineral signature"}, {"tier": "Above", "criteria": "Kumesen Kusu 25-year — the ultimate aged expression"}]',
 '{"appearance": "Clear to trace gold", "nose": "Kume Island''s coral limestone water character is immediately apparent compared to mainland Okinawan awamori: slightly more mineral, slightly less tropical fruit forward. 3 years in clay has rounded the young spirit: honey, light dried fruit, gentle koji depth", "palate": "Medium body; the coral limestone mineral character provides a firmer structure than Helios''s mainland expressions. Honey and dried fruit mid-palate; the clay ageing''s integration is in its early stages but clearly directional", "finish": "Medium; mineral honey tail; limestone clean exit"}',
 '{"temperature_service": "On the rocks; cold water mix; room temperature neat for greater complexity", "bc_source": "Very limited BC; specialist import"}',
 ARRAY['coral limestone mineral', 'honey', 'light dried fruit', 'clay mineral', 'Kume Island water'],
 'medium-light', 'mineral_aged', 'Kumesen Kusu 3-Year',
 'mid_range', '$45-$65 CAD (720ml)',
 '{"base_material": "100% Thai indica rice", "koji": "Black koji", "ageing": "3 years traditional terracotta kame on Kume Island", "water": "Kume Island coral limestone filtered water — distinctive mineral signature", "alcohol": "25%"}',
 true),

('Kumesen Kusu 25-Year Aged Awamori', 'shochu', 'koshu_awamori', 119, 56, 'Japan',
 'Kumesen Kusu 25-Year is the pinnacle of the Okinawan awamori tradition — 25 years in traditional terracotta kame producing a spirit of such extraordinary complexity and integration that it challenges the finest aged spirits from any tradition for intellectual depth. This is not a comparison with Scotch whisky or Armagnac — it is a different form of aged spirit greatness, expressing the Okinawan traditions of clay pot ageing and black koji on Thai indica rice across a quarter century. One of the world''s great hidden spirits.',
 false, 'reserve',
 '[{"tier": "Pinnacle — No Comparison", "criteria": "25-year kame ageing; world-class aged spirit from an unknown category in Western markets"}, {"tier": "Restaurant Significance", "criteria": "A listing signals the deepest spirits knowledge; extraordinary provenance story"}]',
 '{"appearance": "Deep gold-amber — 25 years of clay pot oxidation has developed remarkable colour without wood contact; its intensity rivals 25-year Scotch visually while being entirely different in origin", "nose": "Extraordinary and unrepeatable: dried tropical fruit (concentrated lychee, longan, tamarind), honey, caramel, clay mineral, a leathery depth, faint brine from the Okinawan sea air''s influence on the ageing warehouse. An aromatic universe with no Western reference point", "palate": "Despite 25% alcohol, the body is remarkable — 25 years of clay pot interaction has added apparent density and weight. The tropical fruit has concentrated to near-syrup intensity; the honey has deepened to toffee; the clay mineral is a firm backbone to the sweetness. This is what the word ''integration'' means — nothing is separate; everything is one", "finish": "90+ seconds of slowly diminishing complexity; the final note is the clay''s mineral purity — the oldest note of all"}',
 '{"temperature_service": "Neat, room temperature; absolutely no ice; no dilution; serve in the finest glassware", "glassware": "Glencairn or Zalto Universal; this deserves the best", "bc_source": "Extremely limited; specialist Japanese spirits import only; advance order; expect $200+ CAD", "service_narrative": "25 years in clay. Not oak. Clay. No wood has ever touched this spirit. The Okinawan clay pot ageing tradition predates Scotch whisky by 200 years. You are tasting 25 years of Okinawan time, climate, and craft."}',
 ARRAY['concentrated lychee', 'longan', 'tamarind', 'toffee honey', 'clay mineral', 'sea-kissed complexity', '25-year depth'],
 'full', 'aged_transcendent', 'Kumesen Kusu 25-Year',
 'ultra_premium', '$200+ CAD (720ml)',
 '{"base_material": "100% Thai indica rice", "koji": "Black koji", "ageing": "25 years in traditional terracotta kame on Kume Island, Okinawa; no wood contact throughout", "water": "Kume Island coral limestone water", "alcohol": "43% (genshu — undiluted before bottling)", "annual_production": "Very limited — the 25-year stock was established decades ago and is finite", "wood_contact": "Zero — all complexity from clay mineral interaction and long-term oxidation through kame walls"}',
 true);

COMMIT;
