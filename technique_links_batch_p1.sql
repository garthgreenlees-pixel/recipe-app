BEGIN;

-- ============================================================
-- BEVERAGE TECHNIQUE PRODUCTS — BATCH LINK INSERT
-- Covers 166 products with no technique links
-- Part 1: Beer, Coffee, Sake, Shochu, Japanese Tea
-- ============================================================

INSERT INTO beverage_technique_products (technique_id, product_id, relevance_note) VALUES

-- ===== BEER ALE: Breakside IPA (66), Ecliptic IPA (68), Weihenstephan (187) =====
(1, 66, 'Breakside IPA demonstrates the weight-and-intensity axis of hoppy craft beer pairing — bitter, aromatic IPA demands equivalent bold food partners.'),
(2, 66, 'Breakside IPA: myrcene and alpha-acid bitterness illustrate hop chemistry and flavour science in craft ale production.'),
(13, 66, 'Breakside IPA is an Oregon craft IPA benchmark — demonstrates the American hop-forward style within the craft beer family taxonomy.'),
(14, 66, 'Breakside IPA relies on Saccharomyces cerevisiae top fermentation and dry-hop aromatic extraction — primary fermentation science case study.'),
(19, 66, 'Breakside IPA: all-grain brewing with Pacific Northwest hop varieties illustrates ingredient-driven beer production philosophy.'),
(82, 66, 'Breakside IPA demonstrates how fermentation temperature and yeast strain interact with hop timing to produce the IPA''s distinctive aromatic profile.'),

(1, 68, 'Ecliptic Starburst IPA: high IBU and aromatic intensity places it at the bold end of the pairing weight axis.'),
(2, 68, 'Ecliptic IPA illustrates how caryophyllene and humulene in Pacific Northwest hops produce distinctive flavour compounds.'),
(13, 68, 'Ecliptic Starburst IPA: benchmark Oregon West Coast IPA demonstrating clean bitterness and bright tropical hop character.'),
(14, 68, 'Ecliptic: cold-side dry hopping illustrates post-fermentation aromatic extraction and volatile compound preservation.'),
(19, 68, 'Ecliptic Starburst IPA: hop variety selection and addition timing illustrate key craft brewing production decisions.'),
(82, 68, 'Ecliptic IPA: yeast-hop interaction and fermentation temperature control produce the aromatic precision of the West Coast IPA style.'),

(1, 187, 'Weihenstephan Hefeweissbier: banana-clove duality demonstrates the complementary pairing axis between fermentation esters and traditional Bavarian food.'),
(2, 187, 'Weihenstephan Hefeweizen: isoamyl acetate (banana) and 4-vinylguaiacol (clove) are primary fermentation flavour science case studies.'),
(13, 187, 'Weihenstephan Hefeweissbier is the benchmark Bavarian Hefeweizen — the world''s oldest brewery demonstrates the Reinheitsgebot craft tradition.'),
(14, 187, 'Weihenstephan Hefeweizen: Weihenstephan WY3068 yeast produces the isoamyl acetate and guaiacol that define the style through fermentation science.'),
(19, 187, 'Weihenstephan: ferulic acid rest and open-top fermentation in copper vessels illustrates traditional Bavarian brewing technique.'),
(82, 187, 'Weihenstephan Hefeweizen: the ferulic acid rest and decoction mashing demonstrate how brewing science produces the iconic banana-clove phenolic spectrum.'),

-- ===== BEER LAGER: Bench Dark Lager (58), Standard Lager (59) =====
(1, 58, 'Bench Dark Lager: malt-forward lager illustrates how dark malts shift the pairing axis toward richer, roasted food combinations.'),
(2, 58, 'Naramata Bench Dark Lager: melanoidins and Maillard reaction compounds from dark malt roasting produce the characteristic flavour profile.'),
(13, 58, 'Bench Dark Lager represents the BC craft lager category — a style bridge between traditional dark European lager and Pacific Northwest craft sensibility.'),
(19, 58, 'Bench Dark Lager: cold lagering and dark malt selection illustrate bottom-fermentation production technique.'),
(82, 58, 'Bench Dark Lager: Saccharomyces pastorianus cold fermentation and extended lagering demonstrate the lager fermentation science.'),

(1, 59, 'Standard Lager: the category''s crisp, clean pairing neutrality demonstrates the principle of beverage as palate refresher.'),
(2, 59, 'Standard Lager: diacetyl reduction through conditioning and clean ester profile illustrate the flavour science of lager finishing.'),
(13, 59, 'Standard Lager is the approachable commercial lager style — teaches students how to recommend accessible options across the beer style spectrum.'),
(19, 59, 'Standard Lager: single-temperature cold conditioning and adjunct addition (if applicable) illustrate commercial lager production decisions.'),
(82, 59, 'Standard Lager: clean fermentation profile with minimal ester production demonstrates how lager yeast and temperature create crisp, neutral character.'),

-- ===== COFFEE: Worka Sidama (391), Bensa Bore (392) =====
(7, 391, 'Worka Sidama Washed Grade 1 demonstrates the washed process — fermentation tank removal of mucilage creates the clean, bright berry-jasmine profile.'),
(21, 391, 'Worka Sidama Washed: high altitude (1800-2200m) and small bean size require precise grind adjustment for optimal espresso or filter extraction.'),
(96, 391, 'Worka Sidama is a premier Ethiopian washing station — demonstrates how Sidama heirloom varieties and altitude express the Ethiopian coffee terroir.'),
(1, 391, 'Worka Sidama Washed: the pairing of Ethiopian washed coffee with delicate pastry or citrus desserts illustrates complementary flavour bridging.'),
(2, 391, 'Worka Sidama: malic acid and citric acid dominance in washed Ethiopian heirloom varieties teaches the organic acid basis of coffee flavour.'),
(71, 391, 'Worka Sidama: retronasal perception of jasmine, blueberry and citrus in washed Ethiopian coffee demonstrates olfactory dominance in beverage evaluation.'),

(7, 392, 'Bensa Bore Honey Process: partial mucilage retention during drying creates the characteristic between-washed-and-natural sweetness and body.'),
(21, 392, 'Bensa Bore Honey: medium-body and higher residual sweetness than washed requires grind and dosing adjustments for balanced filter extraction.'),
(96, 392, 'Bensa Bore Honey Process illustrates the Sidama sub-zone''s innovation in processing — how honey method creates a middle style between washed and natural.'),
(1, 392, 'Bensa Bore Honey: pairing with chocolate-based desserts demonstrates the complementary principle between coffee sweetness and confection richness.'),
(2, 392, 'Bensa Bore Honey: fructose-forward sweetness and enhanced mouthfeel from partial mucilage illustrate fermentation chemistry impact on coffee cup character.'),
(71, 392, 'Bensa Bore Honey: the aromatic complexity of honey-processed Ethiopian coffee demonstrates how processing method shapes retronasal aromatic perception.'),

-- ===== SAKE NIIGATA (112-121) =====
(5, 112, 'Kubota Manju Junmai Daiginjo: 40% seimaibuai (60% polished away) demonstrates top daiginjo classification and the premium quality standard.'),
(30, 112, 'Kubota Manju: served chilled at 10-12°C; the classic Niigata service protocol for premium junmai daiginjo.'),
(47, 112, 'Kubota uses Gohyakumangoku rice — the sake-specific variety with lower protein content that produces the clean, light Niigata tanrei style.'),
(79, 112, 'Kubota Manju: low umami and high acidity creates the classic Niigata pairing logic — cleansing rather than complementing rich umami dishes.'),
(1, 112, 'Kubota Manju: its delicate floral character requires elegant food partners — teaches how beverage weight dictates food pairing intensity.'),
(71, 112, 'Kubota Manju: ginjo-ka (fruity daiginjo aroma) from isoamyl acetate is the primary retronasal experience of premium Niigata sake.'),

(5, 113, 'Kubota Senju Tokubetsu Honjozo: distilled alcohol addition to honjozo demonstrates how to legally enhance aroma without premium polishing.'),
(30, 113, 'Kubota Senju: versatile temperature range from chilled to warm — demonstrates the temperature flexibility of honjozo vs junmai.'),
(47, 113, 'Kubota Senju uses Gohyakumangoku rice at honjozo polishing; illustrates how rice variety and polish interact with alcohol addition.'),
(79, 113, 'Kubota Senju Tokubetsu Honjozo: the clean, slightly dry profile creates excellent food versatility — teaches beginner food pairing logic for sake.'),
(1, 113, 'Kubota Senju: as an entry-level Kubota, demonstrates accessible sake styles and how to build beverage literacy from approachable entry points.'),

(5, 114, 'Kubota Hyakuju Junmai Daiginjo: highest-polished Kubota product (35% seimaibuai) illustrates extreme daiginjo classification standards.'),
(30, 114, 'Kubota Hyakuju: served at 8-10°C maximum; the strictest chilling protocol for ultra-premium junmai daiginjo preservation.'),
(47, 114, 'Kubota Hyakuju: ultra-premium Yamada Nishiki (usually) at extreme polish demonstrates the rice variety hierarchy in top sake production.'),
(79, 114, 'Kubota Hyakuju: the ultra-delicate profile demands extremely subtle food partners or consumption without food — teaches restraint in pairing.'),
(1, 114, 'Kubota Hyakuju Junmai Daiginjo: pricing and positioning in a fine dining environment teaches beverage list architecture and the ultra-premium tier.'),

(5, 115, 'Hakkaisan Junmai Ginjo: 50% seimaibuai classifies as ginjo; illustrates the graduation between standard and premium sake grades.'),
(30, 115, 'Hakkaisan Junmai Ginjo: ideal chilled at 10°C; classic ginjo service protocol for premium sake service.'),
(47, 115, 'Hakkaisan uses Yamada Nishiki and Gohyakumangoku rice; demonstrates how blending sake rice varieties creates balanced ginjo character.'),
(79, 115, 'Hakkaisan Junmai Ginjo: the clean, balanced character demonstrates versatile sake food pairing across Japanese cuisine.'),
(1, 115, 'Hakkaisan Junmai Ginjo: approachable premium price point teaches how to position sake as an accessible luxury for table wine drinkers.'),

(5, 116, 'Hakkaisan Yukimuro Snow-Aged Junmai Ginjo: snow cave ageing at 0-1°C demonstrates unique traditional ageing technique.'),
(30, 116, 'Hakkaisan Yukimuro: serve straight from cold storage; the snow ageing maintains pristine cold-storage temperature throughout.'),
(47, 116, 'Hakkaisan Yukimuro demonstrates how extreme cold ageing suppresses maturation and preserves the pristine ginjo fresh fruit character.'),
(79, 116, 'Hakkaisan Yukimuro: the snow-cave freshness creates exceptional pairing with delicate sashimi — illustrates cold-preservation pairing logic.'),
(1, 116, 'Hakkaisan Yukimuro: the unique Niigata snow-cave tradition demonstrates how artisanal production techniques create premium positioning.'),

(5, 117, 'Koshi no Kanbai Honjozo Sai: demonstrates how a honjozo from a premium kura maintains quality positioning against junmai products.'),
(30, 117, 'Koshi no Kanbai Honjozo: slightly warm service (40°C) is appropriate; the honjozo structure supports warming without losing character.'),
(47, 117, 'Koshi no Kanbai uses premium rice at higher polish than typical honjozo, demonstrating how dedicated kura exceed minimum classification standards.'),
(79, 117, 'Koshi no Kanbai Honjozo: the classic Niigata dry, clean profile is the benchmark pairing companion for traditional Japanese cuisine.'),
(1, 117, 'Koshi no Kanbai Honjozo Sai: the prestigious kura name demonstrates sake brand hierarchy and how reputation affects list positioning.'),

(5, 118, 'Koshi no Kanbai Muku Junmai Daiginjo: the kura''s flagship ultra-premium product illustrates the apex daiginjo standard in Niigata.'),
(30, 118, 'Koshi no Kanbai Muku: strict chilled service at 8°C maximum preserves the ultra-delicate floral precision of the benchmark daiginjo.'),
(47, 118, 'Koshi no Kanbai Muku: uses the finest Yamada Nishiki at extreme polish; benchmark demonstration of rice quality and sake outcome.'),
(79, 118, 'Koshi no Kanbai Muku: the intensely delicate floral aroma demands pairing with the most subtle, clean ingredients — truffle, lily bulb, Kyoto kaiseki.'),
(1, 118, 'Koshi no Kanbai Muku Junmai Daiginjo: one of Japan''s most sought-after sake; teaches premium sake positioning and how scarcity affects list strategy.'),

(5, 119, 'Yoshinogawa Gensen Karakuchi Junmai: junmai designation with karakuchi (dry) style demonstrates the interplay of rice, polish, and brewing technique.'),
(30, 119, 'Yoshinogawa Karakuchi: excellent warm service potential at 40-45°C; dry junmai is the classic warming candidate in Niigata.'),
(47, 119, 'Yoshinogawa uses local Niigata rice for karakuchi production — demonstrates how regional ingredient loyalty supports sense-of-place positioning.'),
(79, 119, 'Yoshinogawa Karakuchi: the very dry, clean profile provides classic palate-cleansing function with richer Japanese and fusion cuisine.'),
(1, 119, 'Yoshinogawa Karakuchi: the tanrei karakuchi (elegant dry) style is the definitive Niigata identity — teaches regional sake character and house style.'),

(5, 120, 'Yoshinogawa Winter Warrior Junmai Ginjo: winter brewing (shizuori cold pressing) demonstrates how season and release timing affect sake character.'),
(30, 120, 'Yoshinogawa Winter Warrior: fresh namazake-adjacent character; serve chilled, consume soon after opening — demonstrates unpasteurised sake service.'),
(47, 120, 'Yoshinogawa Winter Warrior: winter rice brewing with slow cold fermentation demonstrates how temperature control creates the premium ginjo profile.'),
(79, 120, 'Yoshinogawa Winter Warrior: the fresh, lively winter character pairs exceptionally with oysters and delicate cold preparations.'),
(1, 120, 'Yoshinogawa Winter Warrior: seasonal release positioning demonstrates how time-limited sake products create list excitement and guest engagement.'),

(5, 121, 'Kakurei Tokubetsu Junmai: tokubetsu (special) designation with extra polishing demonstrates how kura create differentiated premium positioning.'),
(30, 121, 'Kakurei Tokubetsu Junmai: excellent both chilled and at room temperature; illustrates the versatile service range of quality tokubetsu junmai.'),
(47, 121, 'Kakurei uses Gohyakumangoku rice at above-standard polish, demonstrating how exceeding minimum classification standards builds quality reputation.'),
(79, 121, 'Kakurei Tokubetsu Junmai: the clean, umami-forward profile demonstrates classic umami-synergy pairing logic with dashi-based Japanese cooking.'),
(1, 121, 'Kakurei Tokubetsu Junmai: a premium regional sake from an established Niigata kura — illustrates price-quality positioning in a competitive sake category.'),

-- ===== SAKE NADA (122-128) =====
(5, 122, 'Kiku-Masamune Kimoto Junmai: kimoto (traditional hand-mashing) fermentation starter demonstrates the most labour-intensive and ancient sake production method.'),
(30, 122, 'Kiku-Masamune Kimoto: excellent warm service to 45°C; the lactic acid and rich umami structure of kimoto sake is enhanced by gentle warming.'),
(47, 122, 'Kiku-Masamune uses Nada''s Yamada Nishiki heartland rice — the Tojo Yamada Nishiki demonstrates why Nada is Japan''s premium sake region.'),
(79, 122, 'Kiku-Masamune Kimoto Junmai: the full umami, lactic depth of kimoto creates extraordinary food pairing — especially with aged cheese and rich protein.'),
(1, 122, 'Kiku-Masamune Kimoto: the traditional production method and complexity narrative creates premium storytelling for beverage professionals.'),
(71, 122, 'Kiku-Masamune Kimoto: the complex lactic acid esters and aged character demonstrate how retronasal analysis reveals traditional brewing technique.'),

(5, 123, 'Kiku-Masamune Taru Sake: cedar barrel (taru) maturation is the traditional Nada shipping vessel; demonstrates how oak-adjacent ageing adds unique character.'),
(30, 123, 'Kiku-Masamune Taru: serve at room temperature or slightly warm; the cedar adds structural complexity that benefits from gentle temperature.'),
(47, 123, 'Kiku-Masamune Taru: demonstrates how traditional cedar barrel maturation influenced Nada sake style before glass shipping became standard.'),
(79, 123, 'Kiku-Masamune Taru Sake: the cedar note creates unique pairing with grilled and smoked preparations — demonstrates flavour bridging with smoke character.'),
(1, 123, 'Kiku-Masamune Taru: the most distinctive Nada style — teaches how production heritage creates unique product positioning.'),

(5, 124, 'Ozeki Junmai: a major Nada kura demonstrating how commercial-scale junmai production maintains quality standards across high volume.'),
(30, 124, 'Ozeki Junmai: temperature-versatile from chilled to warm; demonstrates the broad service flexibility of a reliable commercial junmai.'),
(47, 124, 'Ozeki uses Nada-sourced Yamada Nishiki for its core junmai; demonstrates how a large kura maintains rice sourcing standards.'),
(79, 124, 'Ozeki Junmai: the reliable, balanced profile demonstrates approachable sake pairing logic for guests new to sake and food pairing.'),
(1, 124, 'Ozeki Junmai: an entry-point into Nada commercial sake — teaches commercial scale and accessible sake positioning in beverage programmes.'),

(5, 125, 'Sawanotsuru Junmai Daiginjo: premium Nada daiginjo from a historic kura demonstrating how traditional producers succeed in premium categories.'),
(30, 125, 'Sawanotsuru Junmai Daiginjo: chilled service at 10°C; classic premium daiginjo service protocol.'),
(47, 125, 'Sawanotsuru: historic Nada kura using top-tier Yamada Nishiki; demonstrates the Nada emphasis on structured, mineral sake over floral Niigata style.'),
(79, 125, 'Sawanotsuru Junmai Daiginjo: the structured, mineral Nada style demonstrates contrasting pairing with richer, umami-intense preparations.'),
(1, 125, 'Sawanotsuru: a prestigious Nada heritage brand — teaches sake brand positioning and how historic kura maintain authority across market tiers.'),

(5, 126, 'Nihonsakari Junmai Ginjo: a major Nada commercial producer demonstrating how ginjo standards are maintained at scale.'),
(30, 126, 'Nihonsakari Junmai Ginjo: best served chilled at 10-12°C; illustrates standard ginjo chilled service protocol.'),
(47, 126, 'Nihonsakari uses Yamada Nishiki and secondary rice varieties; demonstrates how commercial kura balance quality and production economics.'),
(79, 126, 'Nihonsakari Junmai Ginjo: the reliable ginjo character demonstrates versatile food pairing as an everyday premium sake companion.'),
(1, 126, 'Nihonsakari: a commercially important Nada kura whose junmai ginjo teaches the middle market of Japanese sake positioning.'),

(5, 127, 'Konishi Shirayuki Junmai Ginjo: Shirayuki (White Snow) brand demonstrates Nada heritage naming and how kura brand traditions persist across centuries.'),
(30, 127, 'Konishi Shirayuki: serve chilled; demonstrates the Nada ginjo style with its characteristic structured, mineral-forward character.'),
(47, 127, 'Konishi Shirayuki uses premium Nada-sourced rice; demonstrates regional ingredient sourcing in Nada traditional production philosophy.'),
(79, 127, 'Konishi Shirayuki Junmai Ginjo: structured Nada ginjo character creates excellent pairing with stronger-flavoured Japanese cuisine.'),
(1, 127, 'Konishi Shirayuki: one of Japan''s oldest sake brands — teaching sake heritage and how multi-century kura brands create premium positioning.'),

(5, 128, 'Hakutsuru Tora no Ko Junmai Daiginjo: the Tiger''s Cub flagship from Hakutsuru demonstrates premium daiginjo positioning within a major commercial kura.'),
(30, 128, 'Hakutsuru Tora no Ko: strict chilled service at 8-10°C; premium daiginjo protocol from Nada''s largest producer.'),
(47, 128, 'Hakutsuru Tora no Ko: uses Hyogo Yamada Nishiki at extreme polish — demonstrates how Japan''s largest kura sources premium materials for flagship products.'),
(79, 128, 'Hakutsuru Tora no Ko Junmai Daiginjo: the refined, delicate premium daiginjo from Japan''s largest kura demonstrates peak Nada refinement.'),
(1, 128, 'Hakutsuru Tora no Ko: a premium product within the highest-volume Nada kura — teaches how commercial giants maintain premium product lines.'),

-- ===== SAKE FUSHIMI (129-133) =====
(5, 129, 'Tsuki no Katsura Iwai Junmai Daiginjo: uses Iwai rice (Kyoto) — a region-specific variety demonstrating how rice provenance shapes sake identity.'),
(30, 129, 'Tsuki no Katsura Iwai: serve chilled at 10-12°C; classic Fushimi service in traditional ceramics appropriate to Kyoto''s cultural context.'),
(47, 129, 'Tsuki no Katsura uses Iwai — Kyoto''s native sake rice — demonstrating how regional rice varieties create localised sake terroir.'),
(64, 129, 'Tsuki no Katsura Iwai Junmai Daiginjo: Fushimi''s proximity to Kyoto tea ceremony culture creates natural pairing context between sake and ceremonial aesthetics.'),
(79, 129, 'Tsuki no Katsura Iwai: the soft-water elegance of Fushimi sake creates delicate food pairing logic appropriate to Kyoto kaiseki cuisine.'),
(1, 129, 'Tsuki no Katsura Iwai Junmai Daiginjo: a regionally distinctive Kyoto sake demonstrating how prefecture-specific rice creates unique product identity.'),

(5, 130, 'Tsuki no Katsura Junmai Nigori: unfiltered (nigori) sake demonstrates the cloudy, rice-lees style with characteristic sweet-rich texture.'),
(30, 130, 'Tsuki no Katsura Nigori: shake gently before serving; nigori service protocol requires remixing the lees for even pour.'),
(47, 130, 'Tsuki no Katsura Nigori: coarser filtration retaining rice solids demonstrates how filtration level affects sake texture and flavour profile.'),
(64, 130, 'Tsuki no Katsura Nigori: the sweet, creamy texture in Kyoto context pairs naturally with traditional wagashi (Japanese confection) presentation.'),
(79, 130, 'Tsuki no Katsura Junmai Nigori: the creamy sweetness and rice character demonstrates unique pairing with spicy cuisine — the richness moderates heat.'),
(1, 130, 'Tsuki no Katsura Nigori: teaches the nigori style and how to position unfamiliar sake categories for guests unfamiliar with Japanese beverage culture.'),

(5, 131, 'Tamanohikari Bizen Omachi Junmai Daiginjo: uses Omachi, Japan''s oldest extant sake rice variety — demonstrates heirloom rice in premium production.'),
(30, 131, 'Tamanohikari Omachi Daiginjo: serve chilled; the complex, mineral Omachi character benefits from cold service preserving delicate earth notes.'),
(47, 131, 'Tamanohikari uses Bizen Omachi (Okayama) rice — demonstrating that premier Fushimi kura source specific regional rice for signature products.'),
(64, 131, 'Tamanohikari Omachi Daiginjo: the Kyoto kura''s connection to imperial tea culture creates natural education around sake-ceremony parallel.'),
(79, 131, 'Tamanohikari Bizen Omachi: the earthy, mineral complexity of Omachi pairs exceptionally with earthy dishes — matsutake, truffle, and wild mushroom.'),
(1, 131, 'Tamanohikari Omachi Daiginjo: Omachi rice storytelling teaches students about heirloom grain varieties and their premium positioning in sake lists.'),

(5, 132, 'Tamanohikari Junmai Ginjo: demonstrates how a Fushimi kura''s house style contrasts with Niigata tanrei through soft-water mineral character.'),
(30, 132, 'Tamanohikari Junmai Ginjo: serve chilled at 10°C; classic Fushimi service highlighting the soft, mineral water character.'),
(47, 132, 'Tamanohikari Junmai Ginjo: the Fushimi soft water (fushimizu) is the defining production ingredient — demonstrates water chemistry in sake character.'),
(1, 132, 'Tamanohikari Junmai Ginjo: a reliable Fushimi kura demonstrating how water character creates regional sake identity across the Nada-Fushimi axis.'),

(5, 133, 'Tozai Snow Maiden Junmai Nigori: an export-positioned Fushimi nigori demonstrating how traditional styles are adapted for international markets.'),
(30, 133, 'Tozai Snow Maiden: well-chilled service with gentle shaking; demonstrates export nigori service to guests unfamiliar with the style.'),
(47, 133, 'Tozai Snow Maiden: Yamada Nishiki at standard polish demonstrates that even export-market nigori can use premium rice varieties.'),
(79, 133, 'Tozai Snow Maiden Nigori: the sweet, creamy character creates excellent pairing with mild spice, fruit-based sauces, and Asian fusion cuisine.'),
(1, 133, 'Tozai Snow Maiden: an international export product teaching how Japanese kura position sake for non-Japanese fine dining contexts.'),

-- ===== SAKE YAMAGUCHI, YAMAGATA, FUKUI (134-141) =====
(5, 134, 'Dassai 23 Junmai Daiginjo: 23% seimaibuai (77% polished away) — the most extreme polishing ratio demonstrates precision at the absolute apex of sake production.'),
(30, 134, 'Dassai 23: serve ice cold at 6-8°C; extreme ultra-premium daiginjo protocol preserving the most delicate aromas.'),
(47, 134, 'Dassai 23 uses only Yamada Nishiki polished to 23%; demonstrates how extreme rice polishing removes proteins and lipids for ultra-clean flavour.'),
(79, 134, 'Dassai 23 Junmai Daiginjo: the impossibly delicate profile demands consumption alone or with the most neutral, clean ingredients.'),
(1, 134, 'Dassai 23: perhaps the world''s most famous sake brand — the ultimate premium positioning case study for sake in fine dining.'),
(71, 134, 'Dassai 23: the retronasal floral precision of ultra-polished daiginjo demonstrates how seimaibuai creates the perception of flavour purity through aromatic focus.'),

(5, 135, 'Dassai 39 Junmai Daiginjo: 39% seimaibuai — demonstrates how Dassai''s standard daiginjo maintains extraordinary quality at a more accessible tier.'),
(30, 135, 'Dassai 39: serve chilled at 8-10°C; premium daiginjo service protocol for Asahi Shuzo''s flagship accessible ultra-premium product.'),
(47, 135, 'Dassai 39: Yamada Nishiki at 39% seimaibuai demonstrates that excellence is achievable without extreme polishing expense.'),
(79, 135, 'Dassai 39: the approachable yet refined daiginjo character creates broad food pairing logic from sashimi to mild French cuisine.'),
(1, 135, 'Dassai 39: the global ambassador for premium sake — teaches how a premium brand creates international awareness for an entire category.'),

(5, 136, 'Dassai Beyond Junmai Daiginjo: ultra-limited production without stated seimaibuai ratio; demonstrates concept-driven premium sake positioning.'),
(30, 136, 'Dassai Beyond: most precious service conditions — ice cold, appropriate crystal; the ultimate sake service demonstration.'),
(47, 136, 'Dassai Beyond: Yamada Nishiki polished to an undisclosed extreme ratio — demonstrates how concept sake transcends standard classification logic.'),
(79, 136, 'Dassai Beyond: the supreme delicacy demands contemplative consumption, not pairing — demonstrates that some premium beverages are stand-alone experiences.'),
(1, 136, 'Dassai Beyond: the rarest, most expensive sake — the ultimate premium beverage positioning case study in any global fine dining context.'),

(5, 137, 'Juyondai Honmaru Junmai: an extreme rarity from Yamagata — demonstrates how limited production and cultural mystique create legend-level sake positioning.'),
(30, 137, 'Juyondai Honmaru: chilled service with reverence; the cultural weight of this sake demands appropriate ceremony in its service presentation.'),
(47, 137, 'Juyondai uses premium Yamagata rice at exceptional polish; demonstrates how rarity and regional specificity create the ultimate premium sake positioning.'),
(79, 137, 'Juyondai Honmaru: the extraordinary quality demands no food — this is a sake for contemplative appreciation rather than food pairing.'),
(1, 137, 'Juyondai: Japan''s most sought-after sake — the definitive lesson in scarcity-driven premium beverage positioning and list prestige.'),

(5, 138, 'Born Gold Junmai Daiginjo: ultra-premium Fukui sake demonstrating how smaller regional kura achieve international recognition through excellence.'),
(30, 138, 'Born Gold: strict chilled service; the ultra-refined character requires cold preservation of delicate aromatic compounds.'),
(47, 138, 'Born Gold: Yamada Nishiki at premium polishing from Fukui; demonstrates how regional kura outside Nada and Niigata achieve premium positioning.'),
(79, 138, 'Born Gold Junmai Daiginjo: the ultra-refined profile creates exceptional pairing with Fukui''s regional cuisine — echizen crab, soba.'),
(1, 138, 'Born Gold: an internationally celebrated premium sake from Fukui — teaches how regional kura achieve global recognition through quality rather than brand scale.'),

(5, 139, 'Born Dream Junmai Daiginjo: Born''s flagship product demonstrating how a single-minded pursuit of quality creates international sake competition success.'),
(30, 139, 'Born Dream: ice-cold service at 6-8°C; the apex Born product demands the most pristine service conditions.'),
(47, 139, 'Born Dream uses ultra-premium Yamada Nishiki at extreme polishing; Fukui''s cold water creates a style distinct from Nada and Niigata.'),
(79, 139, 'Born Dream Junmai Daiginjo: an exceptional, stand-alone sake or pairing with the finest white fish preparations — tai sashimi, fugu.'),
(1, 139, 'Born Dream: a multiple international gold medal winner — demonstrates how competitive success creates premium positioning for a regional kura.'),

(5, 140, 'Dewazakura Oka Cherry Bouquet Ginjo: created the Yamagata Ginjo style; demonstrates how a single innovative sake defined a regional style identity.'),
(30, 140, 'Dewazakura Oka: the classic ginjo service at 12°C — the sake that taught Japan the meaning of ginjo-ka floral aromatics.'),
(47, 140, 'Dewazakura Oka uses Dewa Sansan — Yamagata''s native rice — demonstrating how regional rice varieties create distinctive prefectural sake identity.'),
(79, 140, 'Dewazakura Oka Cherry Bouquet: the delicate floral ginjo-ka aroma creates exceptional pairing with cherry blossom season kaiseki cuisine.'),
(1, 140, 'Dewazakura Oka: the sake that invented the ginjo boom — demonstrates how innovation and regional identity create lasting category influence.'),

(5, 141, 'Aramasa No. 6 X-type Junmai Ginjo: uses the oldest extant yeast strain (No. 6 from Akita) with traditional kimoto fermentation; a return to origin movement.'),
(30, 141, 'Aramasa No. 6: chilled service in appropriate vessels; Yoshinosugi cedar is the preferred pairing material for Aramasa''s natural production philosophy.'),
(47, 141, 'Aramasa No. 6: Miyama Nishiki rice with heritage yeast demonstrates the natural sake movement — no additives, minimal intervention.'),
(79, 141, 'Aramasa No. 6 X-type: the natural, lactic, complex character pairs exceptionally with aged cheese, fermented foods, and natural wine cuisine contexts.'),
(1, 141, 'Aramasa No. 6: the standard-bearer of Japan''s natural sake movement — demonstrates how heritage practices create extraordinary premium positioning.'),

-- ===== SHOCHU/AWAMORI (163, 164, 167, 169) =====
(140, 163, 'Iichiko Frasco 30° Mugi Jochu: premium barley shochu at reduced ABV demonstrates the delicate mugi (barley) style and how strength affects flavour expression.'),
(141, 163, 'Iichiko Frasco: Oita barley shochu with reduced alcohol demonstrates how honkaku (authentic) production creates the clean, light character of mugi style.'),
(38, 163, 'Iichiko Frasco: Japanese traditional distilled spirit with centuries of Oita cultural heritage demonstrates traditional beverage respect in service.'),
(1, 163, 'Iichiko Frasco 30°: the delicate mugi character creates exceptional pairing with clean, light Japanese cuisine — sashimi, chawanmushi, light sushi.'),
(2, 163, 'Iichiko Frasco: barley distillation creates characteristic 3-methylbutanal and pyrazine compounds contributing to the clean, cereal-forward shochu aroma.'),

(140, 164, 'Naka Naka Mugi Shochu 25°: demonstrates the standard ABV honkaku mugi shochu production with traditional Oita craftsmanship.'),
(141, 164, 'Naka Naka: single-distilled mugi shochu demonstrates how first-distillation preserves the ingredient character versus multiple distillation spirits.'),
(38, 164, 'Naka Naka Mugi Shochu: represents Oita''s barley shochu heritage as Japan''s designated mugi shochu heartland.'),
(1, 164, 'Naka Naka Mugi Shochu: the clean, accessible style creates broad food pairing versatility — teaches how approachable traditional spirits integrate into fine dining.'),
(2, 164, 'Naka Naka: single distillation preserves complex barley esters and Maillard compounds that multi-distillation spirits would remove.'),

(140, 167, 'Zuisen Awamori Koshu 5-Year: aged awamori (kusu) demonstrates how Okinawa''s traditional Indica rice distillate develops with extended cave ageing.'),
(38, 167, 'Zuisen Kusu Awamori: the Ryukyu Kingdom''s ancestral distillate — one of Asia''s oldest distilled spirits demonstrates traditional beverage heritage.'),
(1, 167, 'Zuisen Awamori Koshu: the aged, complex character creates pairing with Okinawan champuru cuisine and Asian fusion preparations.'),
(2, 167, 'Zuisen Kusu: 5-year clay pot ageing develops complex aldehyde-ester compounds from the black koji (Aspergillus awamori) fermentation unique to Okinawa.'),
(71, 167, 'Zuisen Awamori Kusu: retronasal analysis reveals how long ageing in clay pots creates distinctive aromatic complexity distinct from any other Asian spirit.'),

(140, 169, 'Kumesen Kusu 3-Year Awamori: demonstrates the entry-level kusu (aged) tier for Okinawan awamori — how 3-year ageing begins the characteristic complexity development.'),
(38, 169, 'Kumesen Kusu 3-Year: Okinawan cultural identity is inseparable from awamori — demonstrated through the role of kusu in Okinawan feast and ceremony traditions.'),
(1, 169, 'Kumesen Kusu 3-Year Awamori: the developing complexity creates pairing with rich Okinawan preparations — rafute braised pork, goya champuru.'),
(2, 169, 'Kumesen Kusu: black koji (Aspergillus luchuensis) fermentation creates citric acid-dominant wash; 3-year ageing demonstrates early development trajectory.'),
(71, 169, 'Kumesen Kusu Awamori: retronasal awareness of the developing aged character in awamori teaches comparative analysis against other Asian aged spirits.'),

-- ===== ITALIAN SPIRITS/LIQUEUR (349, 350) =====
(56, 349, 'Limoncello di Capri: the iconic Italian digestif liqueur demonstrates pomace-adjacent citrus distillation tradition; Capri lemons in neutral spirit base.'),
(119, 349, 'Limoncello di Capri: the benchmark Italian citrus digestif teaches the amaro and liqueur digestif family alongside Limoncello''s distinct serving protocol.'),
(51, 349, 'Limoncello di Capri: demonstrates the Italian liqueur category within the broader spirits overview — regional identity and traditional production.'),
(1, 349, 'Limoncello di Capri: the sweet-citrus profile creates pairing with citrus desserts and as a digestif after Italian seafood cuisine.'),
(2, 349, 'Limoncello di Capri: limonene extraction through cold maceration of Capri lemon zest demonstrates solvent extraction in flavour concentration.'),

(56, 350, 'Nardini Acquavite di Vinaccia: Italy''s benchmark grappa from Bassano del Grappa demonstrates premium pomace distillation from Venetian grape varieties.'),
(119, 350, 'Nardini Grappa: demonstrates the Italian digestif tradition — how grappa serves as the Italian meal''s natural conclusion and the sommelier''s digestif selection.'),
(51, 350, 'Nardini Acquavite: demonstrates the pomace spirit category within the spirits overview — history, production, and cultural significance in Italian dining.'),
(1, 350, 'Nardini Grappa: the intense, vinous character creates unique pairing with dark chocolate and aged cheese as an Italian dessert digestif.'),
(2, 350, 'Nardini Acquavite: copper pot distillation of fresh Venetian pomace demonstrates how fermentation substrate and still type create the grappa character.'),

-- ===== HIGHLAND SCOTCH WHISKY (413-416) =====
(6, 413, 'Glenmorangie 18 Year Extremely Rare: demonstrates the Highland single malt style — complex, heathery, lighter peat — and the 18-year ageing milestone.'),
(98, 413, 'Glenmorangie 18 Year: an exemplary Highland distillery demonstrating the three primary maturation cask types and how they affect flavour development.'),
(44, 413, 'Glenmorangie 18 Year: Glenmorangie''s innovative cask programme (ex-Burgundy, Sauternes, Madeira) demonstrates advanced spirit maturation science.'),
(1, 413, 'Glenmorangie 18 Year: the complex heathery, fruity profile creates elegant pairing with Highland game, smoked salmon, and aged cheese.'),
(2, 413, 'Glenmorangie 18 Year: beta-damascenone (rose and honey) from 18-year oak maturation demonstrates how long barrel time creates floral-spice compound development.'),
(71, 413, 'Glenmorangie 18 Year: retronasal analysis of the complex orange peel, nutmeg and heather honey bouquet demonstrates Highland single malt aromatic architecture.'),

(6, 414, 'GlenDronach 18 Year Allardice: demonstrates the Speyside-Highland border style with classic sherry cask maturation and the traditional rich, fruity character.'),
(98, 414, 'GlenDronach 18 Year: Oloroso and PX sherry cask maturation at 18 years demonstrates the relationship between fortified wine cask influence and whisky character.'),
(44, 414, 'GlenDronach 18 Year Allardice: 18-year Oloroso sherry butts demonstrate how sherry cask maturation creates dried fruit, dark chocolate and Christmas spice.'),
(1, 414, 'GlenDronach 18 Year: the rich sherry-cask profile creates exceptional pairing with dark chocolate, Christmas pudding, and aged blue cheese.'),
(2, 414, 'GlenDronach 18 Year Allardice: sherry cask-derived ellagic acid and tannin polyphenols from 18-year oak demonstrate the chemistry of sherry cask whisky development.'),

(6, 415, 'Dalmore 18 Year: demonstrates the Northern Highlands bold single malt style from the Alness Distillery — rich, sherried, with the citrus Dalmore character.'),
(98, 415, 'Dalmore 18 Year: complex multi-cask maturation (sherry, Bourbon, white wine) demonstrates the advanced blending of cask types in premium Highland production.'),
(44, 415, 'Dalmore 18 Year: the iconic Dalmore stag and multi-cask programme demonstrates how brand identity and production technique create premium positioning.'),
(1, 415, 'Dalmore 18 Year: the rich orange marmalade and dark chocolate profile creates pairing with chocolate tart, Stilton, and cured meat charcuterie.'),
(2, 415, 'Dalmore 18 Year: citrus-forward compound development (limonene, citral) from the Dalmore white wine finishing cask demonstrates post-maturation flavour addition.'),

(6, 416, 'Clynelish 14 Year: demonstrates the waxy, coastal Highland character — Clynelish''s unique fatty acid ester profile creates one of Scotland''s most distinctive single malts.'),
(98, 416, 'Clynelish 14 Year: the waxy mouthfeel and coastal brine of Clynelish demonstrates how northern Highland coastal conditions influence spirit character.'),
(44, 416, 'Clynelish 14 Year: ex-Bourbon cask maturation demonstrates how American oak creates vanilla-coconut-spice overlay on the natural waxy coastal character.'),
(1, 416, 'Clynelish 14 Year: the coastal brine and waxy character creates exceptional pairing with smoked fish, oysters, and coastal charcuterie.'),
(2, 416, 'Clynelish 14 Year: the waxy character from palmitic acid ethyl ester demonstrates how fatty acid production during distillation creates distinctive mouthfeel.'),

-- ===== JAPANESE TEA - UJI (204-209, 211, 212, 214, 217, 222) =====
(31, 204, 'Ippodo Kan-un Ceremonial Matcha: demonstrates the highest ceremonial grade of shade-grown, stone-ground tencha — the apex of Japanese green tea craftsmanship.'),
(32, 204, 'Ippodo Kan-un: Ippodo''s flagship ceremonial product is central to the chado (tea ceremony) tradition from Kyoto''s most prestigious traditional tea house.'),
(64, 204, 'Ippodo Kan-un Ceremonial Matcha: used in formal cha-no-yu ceremony — teaches the complete philosophical and aesthetic framework of Japanese tea service.'),
(131, 204, 'Ippodo Kan-un: demonstrates the pinnacle of shade cultivation (okumidori/samidori), stone grinding, and ceremonial grade standards in Japanese green tea.'),
(1, 204, 'Ippodo Kan-un: the umami and vegetal intensity of ceremonial matcha pairs with Japanese confections (wagashi) as the traditional ceremony food.'),
(2, 204, 'Ippodo Kan-un: the theanine (amino acid) and EGCG catechin balance in ceremonial matcha demonstrates the flavour chemistry of umami in green tea.'),

(31, 205, 'Marukyu Koyamaen Wako Matcha: demonstrates the benchmark Uji ceremonial matcha from one of Japan''s oldest and most prestigious tea houses (est. 1704).'),
(32, 205, 'Marukyu Koyamaen Wako: a revered ura-senke school ceremony matcha — illustrates how specific tea houses supply specific ceremony schools.'),
(64, 205, 'Marukyu Koyamaen Wako: teaches students the ceremonial matcha hierarchy from usucha to koicha (thin to thick) preparation styles.'),
(131, 205, 'Marukyu Koyamaen Wako: the first flush shade cultivation and slow stone grinding demonstrates how time and temperature control create premium matcha flavour.'),
(1, 205, 'Marukyu Koyamaen Wako Matcha: the umami-forward, bitter-sweet balance of premium ceremonial matcha is the definitive flavour model for matcha appreciation.'),

(31, 206, 'Marukyu Koyamaen Aoarashi Matcha: demonstrates a culinary-adjacent ceremonial grade — how premium houses offer tiered products for different ceremony contexts.'),
(64, 206, 'Marukyu Koyamaen Aoarashi: a lower ceremonial tier that teaches students the shade-grown quality spectrum from ceremony to culinary applications.'),
(131, 206, 'Marukyu Koyamaen Aoarashi: illustrates how different harvests and shade intensities create the quality gradient within the Uji ceremonial matcha category.'),
(1, 206, 'Marukyu Koyamaen Aoarashi: the slightly more astringent character creates broad culinary pairing — from ceremony context to matcha cuisine integration.'),

(31, 207, 'Nakamura Tokichi Uji Ceremonial Matcha: demonstrates the traditional Kyoto tea house model — retailing both ceremonial tea and wagashi confections together.'),
(64, 207, 'Nakamura Tokichi: a benchmark Kyoto tea experience — the tea house and confection relationship teaches the complete Japanese afternoon tea service model.'),
(131, 207, 'Nakamura Tokichi Uji Matcha: teaches the Uji terroir distinctiveness — how the Uji River mist and soil create the characteristic umami-rich flavour signature.'),
(1, 207, 'Nakamura Tokichi Matcha: the sweet-umami-bitter balance demands the accompanying wagashi — demonstrates the essential matcha-sweet confection pairing principle.'),

(31, 208, 'Kyoto Obubu Okumidori Ceremonial Matcha: single-cultivar matcha demonstrates how specific tea plant variety shapes the flavour profile independently of processing.'),
(131, 208, 'Kyoto Obubu Okumidori: the Okumidori cultivar (late-harvest, higher theanine) demonstrates how cultivar selection impacts the umami intensity in shade-grown tea.'),
(64, 208, 'Kyoto Obubu Okumidori: the producer''s transparency about cultivar demonstrates modern tea education — teaching single-origin, single-cultivar premium positioning.'),
(1, 208, 'Kyoto Obubu Okumidori Ceremonial Matcha: the deep umami character creates exceptional pairing with simple onigiri or savoury wagashi beyond the sweet tradition.'),

(31, 209, 'Yamamotoyama Culinary Matcha: demonstrates the quality gradient from ceremonial to culinary — how different grades are appropriately positioned in beverage programmes.'),
(131, 209, 'Yamamotoyama Culinary Matcha: teaches students how culinary-grade matcha is used in cooking, cocktails, and matcha lattes — different from ceremony service.'),
(64, 209, 'Yamamotoyama Culinary: demonstrates how culinary matcha extends the ceremony ingredient into modern beverage programme applications.'),
(1, 209, 'Yamamotoyama Culinary Matcha: versatile food pairing base — teaches how culinary-grade tea ingredients create a range of modern beverage programme applications.'),

(31, 211, 'Marukyu Koyamaen Gyokuro Unkaku: premium gyokuro demonstrates the shading technique''s effect — 20+ days under shade nets creates the theanine-umami intensity.'),
(32, 211, 'Marukyu Koyamaen Gyokuro Unkaku: the pinnacle of loose-leaf Japanese tea demonstrates how gyokuro service differs from matcha ceremony.'),
(131, 211, 'Marukyu Koyamaen Gyokuro Unkaku: illustrates how slow leaf unfurling in 50°C water releases the maximum theanine and amino acid content.'),
(64, 211, 'Marukyu Koyamaen Gyokuro: the concentrated umami of shade-grown gyokuro is the loose-leaf parallel to ceremonial matcha — teaches the shade cultivation spectrum.'),
(79, 211, 'Marukyu Koyamaen Gyokuro: the extraordinary umami demonstrates the same glutamate synergy principle that applies to sake and umami food pairing.'),
(1, 211, 'Marukyu Koyamaen Gyokuro Unkaku: the intense umami character pairs with the most delicate Japanese cuisine — white fish sashimi, tofu, delicate dashi preparations.'),

(31, 212, 'Kyoto Obubu Gyokuro: demonstrates how a smaller specialty producer approaches gyokuro education — teaching single-origin premium tea with farmer transparency.'),
(131, 212, 'Kyoto Obubu Gyokuro: illustrates the emerging artisan tea producer model in Japan — smaller farms with direct-to-consumer premium positioning.'),
(64, 212, 'Kyoto Obubu Gyokuro: the producer''s educational approach to gyokuro demonstrates the growing role of tea in specialty beverage programme development.'),
(1, 212, 'Kyoto Obubu Gyokuro: the delicate, umami-forward character creates refined pairing with seasonal Japanese vegetables and delicate fish preparations.'),

(31, 214, 'Marukyu Koyamaen Sencha Tsujikaze: demonstrates premium unshaded sencha — how the sun-grown approach creates the brisk acidity contrasting with shade-grown umami.'),
(131, 214, 'Marukyu Koyamaen Sencha Tsujikaze: teaches students the sencha-gyokuro spectrum and how sun exposure determines the balance between catechin bitterness and theanine sweetness.'),
(64, 214, 'Marukyu Koyamaen Sencha: the everyday Uji sencha demonstrates how premium cultivation applies to non-ceremonial formats — the versatile table tea of Japan.'),
(1, 214, 'Marukyu Koyamaen Sencha Tsujikaze: the brisk, refreshing character creates excellent table-tea pairing with tempura, light sushi, and vegetable preparations.'),

(31, 217, 'Kyoto Obubu Kabuse Sencha: demonstrates kabuse (half-shade) cultivation — the intermediate style between fully unshaded sencha and gyokuro.'),
(131, 217, 'Kyoto Obubu Kabuse Sencha: kabuse represents the middle point of the shade cultivation spectrum — teaches students how partial shading creates intermediate flavour profiles.'),
(64, 217, 'Kyoto Obubu Kabuse: the producer''s transparent approach to partial-shade cultivation demonstrates modern premium tea education methodology.'),
(1, 217, 'Kyoto Obubu Kabuse Sencha: the balance of umami and fresh green note creates versatile pairing with both delicate Japanese and Asian fusion preparations.'),

(31, 222, 'Marukyu Koyamaen Tencha: demonstrates the raw material for matcha — tencha leaves before stone grinding, illustrating the intermediate ingredient stage.'),
(131, 222, 'Marukyu Koyamaen Tencha: teaching tencha (un-ground shade-grown leaf) illustrates the matcha production chain and how stone grinding transforms the ingredient.'),
(64, 222, 'Marukyu Koyamaen Tencha Raw Matcha Leaf: the rarely-seen intermediate product teaches students the complete Japanese green tea production pathway.'),
(1, 222, 'Marukyu Koyamaen Tencha: consumed as a loose leaf alternative to matcha, demonstrating how the same shade-grown leaf creates two distinct beverage formats.'),

-- ===== JAPAN TEA - SHIZUOKA & KAGOSHIMA (215, 216, 220, 221) =====
(31, 215, 'Nishide Honyama Fukamushi Sencha: demonstrates fukamushi (deep steaming) style — longer steaming creates the characteristic dark, rich, sediment-dense cup profile.'),
(131, 215, 'Nishide Honyama Fukamushi Sencha: Shizuoka''s Honyama tea growing area produces the benchmark fukamushi style — deep steaming contrasts with Uji''s asamushi.'),
(1, 215, 'Nishide Honyama Fukamushi: the rich, full-bodied style creates pairing with stronger-flavoured Japanese cuisine beyond delicate Kyoto preparations.'),

(31, 216, 'Kagoshima Chiran Saemidori Sencha: demonstrates Japan''s fastest-growing tea region — warm Kagoshima climate creates an earlier first flush than northern growing areas.'),
(131, 216, 'Kagoshima Chiran Saemidori: the Saemidori cultivar (vivid green) demonstrates how cultivar breeding programmes create distinctive flavour profiles in green tea.'),
(1, 216, 'Kagoshima Chiran Saemidori: the bright, clean sweetness creates excellent everyday table pairing with straightforward Japanese cuisine and snacks.'),

(31, 220, 'Kagoshima Chiran Tamaryokucha: tamaryokucha (guricha) demonstrates the curled-leaf alternative to needle-shaped sencha — same process, different cultivar and rolling.'),
(131, 220, 'Kagoshima Chiran Tamaryokucha: the curled-leaf style demonstrates how tea rolling technique creates different release rates for flavour compounds during steeping.'),
(1, 220, 'Kagoshima Chiran Tamaryokucha: the smooth, rounded character creates excellent food pairing with simple, clean Japanese dishes without demanding precision pairing.'),

(31, 221, 'Nishide Shizuoka Shincha: first-flush new tea (shincha) demonstrates the seasonal harvest tradition — the most anticipated Japanese tea event of spring.'),
(131, 221, 'Nishide Shizuoka Shincha: the ultra-fresh, spring first-flush character demonstrates how minimal time from harvest to cup creates the maximum fresh green character.'),
(1, 221, 'Nishide Shizuoka Shincha: consumed fresh with minimal accompaniment — demonstrates how some premium seasonal teas are stand-alone sensory experiences.'),

-- ===== CHINA TEA - YUNNAN PU-ERH (249, 250, 251, 267) =====
(31, 249, 'Yunnan Sourcing 2020 Yiwu Ancient Tree Sheng Pu-erh: demonstrates the rare ancient tree (gushu) category — 100+ year old trees producing age-worthy raw pu-erh.'),
(132, 249, 'Yunnan Sourcing Yiwu Sheng: the Yiwu mountain origin demonstrates how terroir within Yunnan creates distinct flavour profiles in single-mountain pu-erh.'),
(38, 249, 'Yunnan Sourcing Yiwu Sheng Pu-erh: demonstrates the living tradition of pu-erh tea as a storable, ageing commodity in Chinese cultural practice.'),
(1, 249, 'Yunnan Sourcing 2020 Yiwu Sheng: the complex tannin and evolving character creates pairing with aged dim sum preparations and Yunnan mountain cuisine.'),
(2, 249, 'Yunnan Sourcing Yiwu Sheng: the microbial post-fermentation chemistry of sheng pu-erh demonstrates how secondary fermentation creates age-worthiness.'),

(31, 250, 'Yunnan Sourcing Crimson Flame Dianhong: premium Yunnan black tea with golden tips demonstrates the tippy black tea style distinct from pu-erh production.'),
(132, 250, 'Yunnan Sourcing Dianhong: demonstrates how Yunnan produces both pu-erh (post-fermented) and premium black tea (fully oxidised) from the same ancient tea gardens.'),
(1, 250, 'Yunnan Sourcing Dianhong Gold Tips: the malty, cocoa-rich character creates natural pairing with dark chocolate, honey-based desserts, and mild spiced foods.'),
(2, 250, 'Yunnan Sourcing Dianhong: the golden buds (theaflavin-rich) demonstrate how bud selection and full oxidation create the characteristic Yunnan black tea flavour.'),

(31, 251, 'Yunnan Sourcing 2012 Dry Storage Aged Sheng: demonstrates 10+ year aged sheng pu-erh — shows how long dry-storage ageing transforms the fresh, astringent young tea.'),
(132, 251, 'Yunnan Sourcing 2012 Aged Sheng: demonstrates the primary difference between wet-storage (wet humid aging) and dry-storage (slower, cleaner ageing) pu-erh philosophies.'),
(38, 251, 'Yunnan Sourcing 2012 Aged Sheng: demonstrates pu-erh as an investment-grade aged beverage — the parallel to aged wine in Chinese connoisseurship culture.'),
(1, 251, 'Yunnan Sourcing 2012 Aged Sheng: the complex, evolving camphor and plum character creates refined pairing with dim sum, roasted duck, and fermented foods.'),

(31, 267, 'Rishi Tea Pu-erh Dante Blend: demonstrates how specialty tea importers translate traditional pu-erh for Western markets — the gateway pu-erh product.'),
(132, 267, 'Rishi Pu-erh Dante: demonstrates the blended versus single-origin pu-erh distinction — how blending creates consistency in a complex and variable category.'),
(1, 267, 'Rishi Pu-erh Dante Blend: the approachable earth and mushroom character creates excellent everyday pairing with dim sum, Asian mushroom preparations, and dark chocolate.'),

-- ===== CHINA TEA - FUJIAN (253, 255, 256, 257, 258, 259, 269) =====
(31, 253, 'Wuyi Shui Xian Rock Oolong: demonstrates the Yancha (rock oolong) category — how Wuyi Mountain mineral basalt soil creates the''yan yun'' (rocky mineral) character.'),
(132, 253, 'Wuyi Shui Xian: Water Sprite demonstrates how different Dan Cong cultivars within the same mountain terroir produce vastly different aromatic profiles.'),
(1, 253, 'Wuyi Shui Xian Rock Oolong: the roasted, mineral, orchid-floral character creates exceptional pairing with aged cheese, roasted meats, and umami-rich preparations.'),
(2, 253, 'Wuyi Shui Xian: charcoal roasting of oolong creates distinctive pyrazine and furanone aromatic compounds demonstrating thermal processing flavour chemistry.'),

(31, 255, 'Wuyi Jin Jun Mei Black Tea: demonstrates that Fujian also produces fine black teas — the golden horse eyebrow bud-only picking creates an extraordinarily rich black tea.'),
(132, 255, 'Wuyi Jin Jun Mei: demonstrates how premium bud-only picking from Da Hong Pao territory creates a luxury black tea parallel to the Wuyi oolong tradition.'),
(1, 255, 'Wuyi Jin Jun Mei: the sweet, potato-honey richness creates exceptional pairing with honey desserts, warm breakfast preparations, and mild milk-based confections.'),
(2, 255, 'Wuyi Jin Jun Mei: bud-only harvesting maximises polyphenol content from young growth — demonstrates how harvest specification determines flavour intensity.'),

(31, 256, 'Song Tea Fuding Bai Hao Yin Zhen Silver Needle: demonstrates premium white tea — minimal processing preserves the natural silver bud character of Fuding Baihao variety.'),
(132, 256, 'Song Tea Fuding Silver Needle: demonstrates the least-processed category of Chinese tea — only wilting and drying creates the delicate honey-floral character.'),
(1, 256, 'Song Tea Silver Needle: the delicate honey and cucumber freshness creates refined pairing with white fish, delicate salads, and mild fruit preparations.'),
(2, 256, 'Song Tea Silver Needle: minimal oxidation and processing demonstrates how heat avoidance preserves the natural polyphenol and flavour compound integrity.'),

(31, 257, 'Song Tea Fuding Bai Mu Dan White Peony: demonstrates the second-tier white tea — two leaves and a bud creates a fuller body than Silver Needle.'),
(132, 257, 'Song Tea Bai Mu Dan: the two-leaf-one-bud harvest demonstrates how leaf inclusion creates richer body and more complex flavour in the white tea category.'),
(1, 257, 'Song Tea Bai Mu Dan: the fuller, honeyed character with floral note creates excellent everyday pairing with light salads, mild cheese, and rice preparations.'),

(31, 258, 'Song Tea Anxi Tieguanyin Traditional Charcoal Roasted: demonstrates the traditional Anxi Tieguanyin style before modern light-oxidised processing dominated.'),
(132, 258, 'Song Tea Tieguanyin Charcoal Roasted: the traditional style demonstrates how charcoal roasting creates the darker, roasted, orchid-spice character contrasting with modern green-style TGY.'),
(1, 258, 'Song Tea Traditional Tieguanyin: the roasted complexity creates excellent pairing with barbecued meats, aged cheese, and Cantonese dim sum.'),
(2, 258, 'Song Tea Traditional Tieguanyin: charcoal roasting demonstrates how pyrazine and lactone formation through heat creates the roasted-orchid aromatic signature.'),

(31, 259, 'Song Tea Anxi Tieguanyin Jade Green Light Oxidised: demonstrates the modern Tieguanyin style — light oxidation for floral, creamy, almost green-tea character.'),
(132, 259, 'Song Tea Jade Tieguanyin: the modern jade style demonstrates the contemporary Anxi approach contrasting with Song''s traditional charcoal roasted offering.'),
(1, 259, 'Song Tea Jade Tieguanyin: the creamy, floral character creates excellent pairing with seafood dumplings, cream-based preparations, and delicate Asian desserts.'),

(31, 269, 'Rishi Organic Wuyi Black (Lapsang Souchong): demonstrates the smoked black tea tradition — pine smoke kiln drying creating the iconic smoky-malty character.'),
(132, 269, 'Rishi Lapsang Souchong: demonstrates how Wuyi''s tradition of pine smoke drying (originally to preserve tea for long transport) became a celebrated flavour profile.'),
(1, 269, 'Rishi Lapsang Souchong: the smoky, malty character creates exceptional pairing with smoked meats, aged cheese, and as a savoury cooking ingredient.'),
(2, 269, 'Rishi Lapsang Souchong: pine smoke guaiacol infusion demonstrates how external aromatisation can dominate and redefine a tea''s flavour identity.'),

-- ===== CHINA TEA - ZHEJIANG LONGJING (260, 261, 262, 268) =====
(31, 260, 'West Lake Longjing Mingqian Pre-Qingming: demonstrates the most prized harvest tier — pre-Qingming (before April 5th) creates the finest, most delicate Dragon Well.'),
(132, 260, 'West Lake Longjing Mingqian: demonstrates the Chinese seasonal harvest hierarchy — pre-Qingming is the apex of the Longjing production calendar.'),
(1, 260, 'West Lake Longjing Mingqian: the delicate chestnut-vegetal-sweet character demands gentle food pairing — spring rolls, light seafood, vegetarian dim sum.'),
(2, 260, 'West Lake Longjing Mingqian: the pan-fired flat leaf demonstrates how wok pan-firing (shaoguo) creates the distinctive chestnut Maillard flavour in Longjing.'),

(31, 261, 'West Lake Longjing Yuqian Spring Grade A: demonstrates the secondary spring harvest immediately after Qingming — excellent quality at more accessible volume.'),
(132, 261, 'West Lake Longjing Yuqian: demonstrates how a two-week harvest window shift creates measurable differences in flavour between the Longjing quality grades.'),
(1, 261, 'West Lake Longjing Yuqian Grade A: the reliable spring freshness creates excellent everyday green tea pairing with light Chinese and Japanese cuisine.'),

(31, 262, 'West Lake Longjing Late Spring Grade B: demonstrates the late spring harvest — showing how seasonal progression creates the quality gradient within Longjing.'),
(132, 262, 'West Lake Longjing Late Spring: the later harvest demonstrates how temperature accumulation and leaf maturity create progressively richer, less delicate character.'),
(1, 262, 'West Lake Longjing Late Spring Grade B: the fuller body and richer character creates pairing with stronger-flavoured preparations than pre-Qingming grades.'),

(31, 268, 'Rishi Organic Dragon Well (Longjing) Zhejiang: demonstrates how specialty importers create accessible Longjing positioning for North American and European markets.'),
(132, 268, 'Rishi Dragon Well: demonstrates how premium Chinese green tea importers select and position single-origin teas for Western specialty food and beverage markets.'),
(1, 268, 'Rishi Dragon Well: the clean, accessible chestnut sweetness creates broad food pairing versatility — the gateway product to premium Chinese green tea appreciation.'),

-- ===== CHINA TEA - GUANGDONG DANCONG (265, 266) =====
(31, 265, 'Phoenix Village Xing Ren Xiang Almond Orchid Dancong: demonstrates a specific Dan Cong cultivar — each Phoenix Mountain variety is named for its unique aromatic profile.'),
(132, 265, 'Phoenix Village Almond Orchid Dancong: demonstrates how Phoenix Mountain microbial environment, altitude and cultivar selection creates Guangdong''s unique oolong identity.'),
(1, 265, 'Phoenix Xing Ren Xiang: the distinctive almond-orchid character creates rare pairing with almond-based confections and Asian pâtisserie using stone fruit.'),
(2, 265, 'Phoenix Almond Orchid Dancong: benzaldehyde (almond) aromatic dominance demonstrates how specific cultivar biochemistry creates the characteristic Dan Cong aroma type.'),

(31, 266, 'Floating Leaves Tea Fenghuang Old Bush Dancong: old bush (lao cong) plants produce deeper, more complex character — demonstrates how plant age affects tea quality.'),
(132, 266, 'Floating Leaves Fenghuang Old Bush: lao cong (old trees 50+ years) demonstrates the parallel to vine age in wine — how older plants produce more concentrated character.'),
(1, 266, 'Floating Leaves Old Bush Dancong: the deep, layered complexity of old bush tea creates exceptional pairing with aged Chinese cuisine — Peking duck, dim sum, fermented preparations.'),

-- ===== TRADITIONAL CULTURAL (466, 471) =====
(92, 466, 'Vanuatu Noble Kava Export Nakamal: demonstrates the export-grade kavalactone-standardised version of the traditional Vanuatu nakamal shell ceremony.'),
(38, 466, 'Vanuatu Noble Kava Export: the nakamal (kava drinking house) tradition demonstrates traditional beverage culture in its original ceremonial Pacific island context.'),
(1, 466, 'Vanuatu Noble Kava Export: the earthy-peppery profile creates functional pairing with fat-moderating foods (coconut, nuts) that slow kavalactone absorption.'),
(2, 466, 'Vanuatu Noble Kava Export: kavalactone chemistry (kavain, dihydrokavain) demonstrates how non-traditional alkaloids create beverage psychoactivity different from alcohol.'),

(94, 471, 'Cross-River Raphia Palm Wine: demonstrates the West African palm wine tradition as the source material for Caribbean rum — an essential historical beverage link.'),
(38, 471, 'Cross-River Palm Wine: demonstrates how traditional West African fermentation knowledge crossed the Atlantic and formed the basis of Caribbean rum production.'),
(1, 471, 'Cross-River Raphia Palm Wine: the natural effervescence and tropical sweetness creates pairing with West African spiced meats and tropical fruit preparations.'),
(2, 471, 'Cross-River Palm Wine: wild Saccharomyces and Lactobacillus co-fermentation of Raphia palm sap demonstrates wild fermentation science in a traditional context.')
ON CONFLICT (technique_id, product_id) DO NOTHING;

COMMIT;
