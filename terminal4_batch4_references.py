#!/usr/bin/env python3
"""Terminal 4 — Batch 4: beverage_references (knowledge entries) for all 23 sections"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO beverage_references
  (name, category, subcategory, description, key_principles,
   common_mistakes, pro_tips, origin, flavour_context, lives_or_dies,
   trigger_keywords, cross_category_parallels, related_entries,
   authority_tier, source_text, applicable_categories, service_context,
   skill_level, is_published)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING RETURNING id, name"""

REFS = [

# ============================================================
# SECTION A — PACIFIC MIGRATION TRAIL
# ============================================================
{
  "name": "Kava — Piper methysticum and the Pacific Beverage Tradition",
  "category": "traditional_cultural",
  "subcategory": "kava_PMT",
  "description": "The definitive reference for the Pacific Migration Trail's primary beverage. Kava (Piper methysticum — 'intoxicating pepper') is the foundational social and ceremonial beverage of Oceania, used continuously for 3,000+ years. It is NOT alcoholic, NOT hallucinogenic — it is pharmacologically distinct from any other beverage category, acting on GABA-A receptors to produce anxiolysis, muscle relaxation, and sociability. Understanding kava requires abandoning all existing beverage categories.",
  "key_principles": """PHARMACOLOGY — THE SIX MAJOR KAVALACTONES:
Kavain (1): Primary anxiolytic — the compound that produces the calm-alert state characteristic of quality kava; water-soluble; dominant in Noble varieties
Dihydrokavain (2): Sedative — contributes to relaxation; water-soluble
Yangonin (3): Dopaminergic modulation — the 'uplifting' component; less water-soluble
Desmethoxyyangonin (4): Inhibits reuptake of noradrenaline — contributes to mild mood elevation
Methysticin (5): Anti-epileptic properties; enhances kavalactone absorption
Dihydromethysticin (6): Sedative-analgesic; contributes to the physical numbing effect

THE NOBLE/TUDEI DISTINCTION (critical for professional sourcing):
Noble varieties (Borogu, Melomelo, Kelai in Vanuatu; Waka, Lawena in Fiji; Mahakea in Hawaii):
— Kavalactone chemotype favours kavain and dihydrokavain
— Effects: clean, pleasant, short duration (4-6 hours), no hangover
— Vanuatu export law requires Noble varieties only
Tudei (Two-Day) varieties:
— High dihydromethysticin, flavokawain B — produces nausea, hangover lasting 24-48 hours
— Used historically in medicine, NOT daily social consumption
— NEVER appropriate for service contexts

PREPARATION PROTOCOLS:
Traditional (highest kavalactone extraction): Dried root chewed or pounded, mixed with cold water, kneaded in cloth for 10 minutes, strained
Modern (accessible): Coarse ground dried root, 60-80g per litre cold water, kneaded in muslin, double-strained
Critical: COLD water only — heat above 60°C degrades kavain and the most pleasant kavalactones
Critical: Fresh preparation — kavalactone-water mix degrades within 4 hours

REGIONAL CEREMONY PROTOCOLS:
Vanuatu Nakamal: Daily social drinking, evening ritual, community decision-making. Shell served fresh from communal bowl. No speeches required. The act of attending the nakamal IS the ceremony.
Fiji Yaqona: Most ceremonial presentation. Tanoa (carved wooden bowl), bilo (coconut shell). Clapping sequence: one sharp clap before receiving, bow the head while drinking the whole shell, three leisurely claps after. The tabua (whale's tooth) presentation for formal occasions.
Samoa Ava: The most formalised. Taupo (ceremonial hostess from chief's family) prepares and serves. Each recipient's title is called out before serving. Specific seating arrangement by rank. The 'foliage of Samoa' speech at opening.
Hawaii Awa: Cultural revival context — smaller ceremonies, focus on intention-setting, hula may accompany. Mo'i variety historically reserved for ali'i (chiefs) only.

EFFECTS TIMELINE:
0-15 min: Oral numbing (kava 'reverse tolerance' — first sessions may have little effect)
15-30 min: Muscle relaxation, anxiolysis, sociability
30-60 min: Peak sedation (heavy shell session) OR continued conversation-friendly relaxation (lighter session)
2-4 hours: Gradual return to baseline — no hangover with Noble varieties
Note: Reverse tolerance is real — regular drinkers need less, not more, to achieve effects""",
  "common_mistakes": """Serving kava hot (destroys active kavalactones — the drink becomes ineffective)
Using Tudei varieties (produces nausea and 24-48 hour hangover — destroys the guest experience and the category's reputation)
Treating kava as 'just another non-alcoholic drink' — its pharmacological effects are real and specific; guests should be informed
Preparing too far in advance (kavalactone-water mixture degrades within 4 hours)
Sourcing from unverified suppliers who don't distinguish Noble from Tudei varieties
Confusing kava with kratom (entirely different plant, different pharmacology, different legal status)""",
  "pro_tips": """The reverse tolerance effect means kava requires 3-5 sessions before its full effects are felt — mention this to first-time guests so they don't judge the experience prematurely
A 'shell' service at a nakamal is 150-200ml consumed in one go — the social contract of drinking the whole shell is important to the ceremony; sipping from a coconut shell is incorrect
Kava and food: traditionally consumed on an empty stomach (food slows absorption); if serving with a meal, acknowledge this and adjust expectations
The mouth-numbing effect is an index of quality — ask guests if they feel it and use it as a quality discussion point
BC kava bar scene (Vancouver) has several dedicated nakamals — professionals should visit for genuine cultural context""",
  "origin": "Vanuatu archipelago, 3,000+ years of continuous cultivation. The Lapita cultural complex (1600-800 BCE) spread kava across Oceania via migration — it followed the same routes as the outrigger canoe, the taro, and the pig. It is the liquid artifact of the Pacific Migration Trail.",
  "flavour_context": "Earthy, peppery, bitter, slightly astringent, with a prolonged numbing effect on the palate. Fresh kava is softer; shelf-stable powder is more bitter. The bitterness is an index of kavalactone concentration — more bitter = more active. The flavour is challenging; the experience of its effects is the point.",
  "lives_or_dies": "Kava lives by sourcing integrity — Noble only, fresh preparation, correct temperature. It dies by shortcuts: wrong variety, hot water, pre-made product without fresh preparation. A kava experience made with Tudei varieties will create a sick guest. A kava experience with expired product from an unverified source will create a disappointing experience. The category's growth in North America depends entirely on quality sourcing and educated service.",
  "trigger_keywords": json.dumps(["kava", "yaqona", "awa", "ava", "kavalactones", "nakamal", "Pacific ceremony", "Vanuatu", "Fiji", "kava bar", "non-alcoholic ceremony", "PMT"]),
  "cross_category_parallels": json.dumps([{"category": "tea_ceremony", "parallel": "Chanoyu (Japanese tea ceremony) as complete cultural ceremony with prescribed vessels, movements, and social meaning"}, {"category": "na_methodology", "parallel": "Kava as the highest expression of ceremonial non-alcoholic beverage — demonstrates that non-alcoholic can be profoundly ceremonial"}]),
  "related_entries": json.dumps([{"entry": "Buna Ceremony — Ethiopian Coffee", "relationship": "The buna is the coffee world's equivalent of the kava ceremony in ritual completeness"}, {"entry": "Japanese Matcha Ceremony", "relationship": "Both are ceremonial preparations of a specific plant that alter consciousness (caffeine vs kavalactones) with prescribed ritual form"}]),
  "authority_tier": 1,
  "source_text": "Lebot, V., Merlin, M. & Lindstrom, L. — Kava: The Pacific Elixir (Yale University Press, 1992); Aporosa, S.A. — The bio-cultural origins and history of kava (Ethnobotany Research & Applications, 2019)",
  "applicable_categories": ["traditional_cultural", "na_methodology", "fermentation_knowledge"],
  "service_context": "ceremonial",
  "skill_level": "advanced"
},
{
  "name": "Lambanog and the Austronesian Fermentation Trail — Coconut Palm as Pacific Beverage Axis",
  "category": "traditional_cultural",
  "subcategory": "coconut_spirits_PMT",
  "description": "The coconut palm (Cocos nucifera) is the Pacific Migration Trail's universal beverage source — a single tree species that has been tapped for its sap across a range extending from Hawaii to Sri Lanka to East Africa, producing remarkably similar fermented beverages under dozens of names. Understanding the coconut toddy tradition is understanding the Austronesian diaspora.",
  "key_principles": """THE COCONUT SAP BEVERAGE FAMILY — ONE TREE, FIFTY DRINKS:
The inflorescence (flower cluster) of a mature coconut palm is tapped by a skilled climber before the flower opens. The sap that flows — called by different names in each culture — is sweet, slightly yeasty, and begins fermenting within hours of collection.

Fresh sap (collected morning and evening, consumed immediately):
— Sri Lanka: NEERA — government-certified, chilled, nutritious; also TOD DI (slightly fermented, mild alcohol)
— Philippines: TUBA — fresh, sweet, slightly alcoholic by evening
— India: NEERA (Tamil Nadu, Kerala) — refrigerated immediately to stop fermentation; health drink
— Indonesia: TUAK — can mean fresh or fermented depending on region
— East Africa (Tanzania, Kenya, Mozambique): MNAZI — Swahili coastal toddy

Fermented sap (1-3 days, 3-8% ABV):
— The full fermentation creates a milky-white, pleasantly sour, fizzy drink
— Each culture has its own tolerance for fermentation time and resulting acidity
— Distilled toddy (arrack/lambanog/arak): further processing creates a spirit of 40-60% ABV

THE DISTILLED EXPRESSIONS:
Philippines LAMBANOG: Fresh tuba → copper pot still double distillation → 40-45% coconut vodka
Sri Lanka ARRACK (Coconut): Fermented toddy → pot still or column still → 30-50%; Del's Lanka is the benchmark
Indonesia ARAK: Similar process; Bali arak is the most internationally known (also the most dangerous when home-produced with methanol risk)
India COCONUT FENI (Goa): Toddy fermented and pot-distilled; regulated product; Goan identity beverage
Caribbean COCONUT RUM: NOT the same tradition — this uses coconut flavouring added to sugarcane rum; the real tradition is in Southeast Asia

PALM SUGAR CONNECTION:
When production for fermentation stops, the reduced sap becomes palm sugar: jaggery (India), gula Melaka (Malaysia — the Kristang heritage sugar), nam tan maprao (Thailand). The same sap, three possible products (fresh drink, fermented drink, sugar) — the decision of the tapper creates different outcomes from the same source.

THE AUSTRONESIAN MIGRATION EVIDENCE:
The presence of coconut palm toddy traditions from Hawaii to East Africa correlates precisely with the migration routes of Austronesian-speaking peoples (departing from Taiwan ~5,000 BCE). The knowledge of tapping the coconut palm travelled with the migrants — it is a botanical artifact of human migration as clearly as the breadfruit (brought to the Caribbean by Cook), the taro, and the sugarcane.""",
  "common_mistakes": "Confusing coconut rum (artificial flavouring) with coconut arrack/lambanog (genuine toddy distillate). Assuming Sri Lankan arrack is the same as Batavia arrack (the Indonesian rice-based spirit). Not recognising the Bali arak risk: home-produced arak has caused methanol deaths — only purchase certified commercial products.",
  "pro_tips": "The coconut toddy tradition is the missing chapter in any spirits programme that claims to represent global fermentation culture. Lambanog is available in Filipino communities in Vancouver and through specialty importers. Sri Lankan coconut arrack (Ceylon Arrack Company) is available at BC LDB. Serving these with Filipino/South Asian food creates culturally coherent pairings.",
  "origin": "The coconut toddy tradition has no single origin — it emerged independently across the entire range of Cocos nucifera cultivation, which spans 40°N to 40°S latitude. The sophistication of the tapping technique suggests knowledge transfer rather than independent invention in many regions.",
  "flavour_context": "Fresh tuba: sweet, slightly acidic, coconut water character, effervescent. Fermented tuba: sour, slightly alcoholic, vinegar-approaching. Lambanog: clean, slightly sweet, mild coconut in the nose, smooth — the coconut character is subtle, not like cocktail coconut.",
  "lives_or_dies": "The tradition lives in the knowledge of the mangangarit (tapper) — the skill of climbing the palm twice daily and collecting sap at precisely the right moment. It dies in industrialisation. The commercial coconut toddy market is small precisely because the product requires such skilled, labour-intensive production.",
  "trigger_keywords": json.dumps(["lambanog", "tuba", "toddy", "coconut palm", "arrack", "neera", "mnazi", "tuak", "PMT", "Austronesian", "coconut spirits"]),
  "cross_category_parallels": json.dumps([{"category": "spirits_production", "parallel": "The tapping and fermentation of coconut sap is analogous to maple syrup production — seasonal, skill-dependent, terroir-influenced"}, {"category": "traditional_cultural", "parallel": "Palm wine from West Africa (WADT) uses the same knowledge applied to a different palm species — the fermentation knowledge crosses oceanic and cultural boundaries"}]),
  "related_entries": json.dumps([{"entry": "Palm Wine — West African Diaspora Trail", "relationship": "The knowledge of tapping and fermenting palm sap crosses cultural boundaries — the same principle applied to different palm species"}]),
  "authority_tier": 2,
  "source_text": "Chandrasekara, A. — Fermented Coconut Products (Springer, 2019); Wijesekera, R.O.B. — The Coconut Palm and Its Products (FAO, 1993)",
  "applicable_categories": ["traditional_cultural", "spirits_production", "fermentation_knowledge"],
  "service_context": "cultural",
  "skill_level": "advanced"
},

# ============================================================
# SECTION B — WEST AFRICAN DIASPORA TRAIL
# ============================================================
{
  "name": "Palm Wine and the Atlantic Crossing — How West African Fermentation Knowledge Built Caribbean Rum",
  "category": "historical",
  "subcategory": "palm_wine_WADT",
  "description": "One of the most significant and least-documented connections in beverage history: the fermentation knowledge of West African palm wine cultures, carried by enslaved Africans to the Caribbean, was applied to sugarcane sap to create rum. The enslaved people could not bring the Raphia or Oil palm trees. But they brought the knowledge of fermenting plant sugars into alcohol — and they applied it to the cane juice they were forced to process.",
  "key_principles": """WEST AFRICAN PALM WINE CULTURES:
Nigeria: Raphia palm (oguro in Yoruba, nkwu enu in Igbo) — the premier wine palm. Oil palm (emu, nkwu) — more common, simpler product. The tapper climbs twice daily, cuts the inflorescence, collects sap in a sealed calabash.
Ghana: Raphia wine (doka) and oil palm wine (nsafufuo) — 'white stuff' in pidgin English.
Cameroon: Raphia vinifera wine (matango) — the most complex African palm wine.
Ivory Coast, Benin, Togo, Angola: All maintain palm wine traditions that predate European contact.

THE MICROBIOLOGY PARALLEL:
West African palm wine fermentation: Saccharomyces cerevisiae (primary), Lactobacillus plantarum, Acetobacter (if left too long)
Caribbean sugarcane rum fermentation: Same organisms — Saccharomyces cerevisiae primary, some LAB in pot still production
The ORGANISMS are identical because they are found on all plant sugars globally. The KNOWLEDGE of how to manage them — harvesting at the right time, managing temperature, understanding when the product was ready — this knowledge was embodied in enslaved people from palm wine cultures.

THE UNRECORDED HISTORY:
No document from the 17th century Caribbean says 'enslaved Africans showed us how to ferment this.' The documents that exist record the economic history from the perspective of the enslaver. But the archaeological and ethnobotanical evidence is clear: the open fermentation of sugarcane juice into killdévil (early rum) was being done in ways that correlate with West African fermentation practice, not European wine or beer practice.

NEAREST GREEN AND THE WHISKEY PARALLEL:
The same erasure applies to American whiskey: Nearest Green, an enslaved man in Moore County, Tennessee, taught Jack Daniel the art of distillation. His knowledge came from somewhere — likely from the African tradition of distillation from palm fermentates. The Jack Daniel's origin story suppressed Green's contribution for 150 years. Uncle Nearest Premium Whiskey (founded 2016) has partially restored it.

CULTURAL MEMORY WITHOUT OBJECTS:
The defining truth of the African diaspora beverage connection: the enslaved brought no plants, no tools, no vessels. They brought knowledge — held in bodies, transmitted through practice, surviving displacement, torture, and erasure. The knowledge of fermentation is one of the most durable forms of cultural memory in human history.""",
  "common_mistakes": "Treating the Caribbean rum origin as a purely European colonial story — it is not. Assuming the technical innovations of early rum production came from European distillers — the open fermentation and the pot still connection to Caribbean rum culture includes African knowledge. Overlooking Nearest Green when discussing American whiskey history.",
  "pro_tips": "The West African Diaspora Trail connection should be introduced carefully and with the weight it deserves. When listing Uncle Nearest on a menu or recommending it to a guest, the story should be told: 'This whiskey was founded to restore the name of the man whose knowledge built Jack Daniel's.' A guest who receives this context carries it forward.",
  "origin": "West Africa — the palm wine tradition predates recorded history. The Atlantic crossing of fermentation knowledge began with the first ships of the transatlantic slave trade, approximately 1619 (when enslaved Africans arrived in Virginia) and earlier in the Caribbean (1490s in Hispaniola, 1620s in Barbados).",
  "flavour_context": "Fresh palm wine: sweet, slightly effervescent, yeasty, coconut water character, 1-3% ABV. Day-old palm wine: sour, 5-8% ABV, more complex, lactic acid character. Three-day wine: approaching palm vinegar, acidic, 2-4% ABV (alcohol partially converted to acetic acid). The flavour changes hourly — it is the most time-sensitive beverage on Earth.",
  "lives_or_dies": "Palm wine lives in community — it cannot be shipped, stored, or scaled. The necessity of freshness creates the social gathering that is the point of the product. The beverage industry cannot commodify something that expires in hours. This is the deepest form of cultural beverage knowledge: a drink that can only be preserved through community.",
  "trigger_keywords": json.dumps(["palm wine", "WADT", "West Africa", "rum origin", "Nearest Green", "Jack Daniel's", "fermentation history", "Atlantic crossing", "matango", "emu", "oguro"]),
  "cross_category_parallels": json.dumps([{"category": "spirits_production", "parallel": "The knowledge of fermenting plant sugars applies from palm sap (West Africa) to sugarcane (Caribbean) to corn mash (American whiskey) — the same biochemical principles, different substrates"}, {"category": "traditional_cultural", "parallel": "Kava (Pacific) and palm wine (Africa) as parallel traditions of plant-based ceremonial beverages that encode cultural identity"}]),
  "related_entries": json.dumps([{"entry": "Clairin — Haitian Unaged Cane Spirit", "relationship": "Haiti as the first free Black republic — clairin production as cultural continuity through revolution"}, {"entry": "Uncle Nearest Premium Whiskey", "relationship": "The WADT's most prominent named figure — Nearest Green's story connects African fermentation knowledge to American whiskey"}]),
  "authority_tier": 1,
  "source_text": "Achebe, C. — Things Fall Apart (Heinemann, 1958); Williams, E. — Capitalism and Slavery (UNC Press, 1944); Weaver, F. — Love & Whiskey (Harper Collins, 2020)",
  "applicable_categories": ["traditional_cultural", "historical", "spirits_production"],
  "service_context": "cultural",
  "skill_level": "master"
},
{
  "name": "Bourbon — American Whiskey, Kentucky Terroir, and the African American Distilling Heritage",
  "category": "spirits_knowledge",
  "subcategory": "bourbon_WADT",
  "description": "Bourbon is America's most distinctly national spirit — legally defined, terroir-influenced, and built on a history that includes the skilled labour and knowledge of enslaved and formerly enslaved African Americans. The regulatory framework, the Kentucky limestone water, the charred oak ageing cycle, and the debt owed to distillers whose names were erased for 150 years.",
  "key_principles": """BOURBON LEGAL REQUIREMENTS (US Federal Standards of Identity):
1. Made in the USA (not just Kentucky — anywhere in USA)
2. Made from a grain mixture with 51%+ corn (the corn mash bill)
3. Distilled to no more than 80% ABV (160 proof)
4. Aged in new, charred American white oak containers
5. Entered into barrel at no more than 62.5% ABV (125 proof)
6. Bottled at minimum 40% ABV (80 proof)
7. No coloring, flavoring, or other additives permitted
Additional for 'Straight Bourbon': aged minimum 2 years; 'Kentucky Straight Bourbon': all steps in Kentucky

KENTUCKY TERROIR — WHY KENTUCKY MATTERS:
Limestone water: The Kentucky aquifer filters through limestone, removing iron (which would turn whiskey black) and adding calcium and magnesium — ideal for yeast health and fermentation efficiency
Four distinct seasons: Hot summers drive whiskey into the charred oak (expanding barrel); cold winters pull it back (contracting barrel) — this pumping cycle extracts vanilla, caramel, and color from the wood
Rickhouse microclimate: Multi-story wooden warehouses — upper floors are hotter, producing more intense, faster-matured bourbon; lower floors are cooler and more consistent; barrel rotation practices differ by distillery

MASH BILLS — THE RECIPE DETERMINES THE CHARACTER:
High corn (75%+ corn): Sweeter, fuller body, less spice — Maker's Mark, W.L. Weller, Pappy Van Winkle
Low rye (10-12% rye): Classic Bourbon, balanced sweet-spice — Buffalo Trace standard
High rye (18-25%+): More spice, more complex — Four Roses, Basil Hayden, Bulleit
Wheated (wheat replaces rye): Softest, most approachable — Maker's Mark, Van Winkle family
Note: All bourbons must be 51%+ corn; the secondary grain (rye, wheat, or malted barley) shapes the character

THE SOUR MASH PROCESS:
Backset (spent mash from previous distillation) is added to the new fermentation as a natural acidifier — maintaining pH consistency, inhibiting unwanted bacteria, ensuring house yeast dominance. Not a flavour element per se, but a quality control mechanism. Nearly all major bourbon producers use sour mash.

THE LINCOLN COUNTY PROCESS (Tennessee Whiskey distinction):
Tennessee Whiskey is NOT Bourbon legally — it is a separate category defined by the Lincoln County Process: new-make spirit is filtered through a minimum 10-foot bed of maple charcoal before barrel entry. This mellowing removes fusel oils and produces a characteristically softer, cleaner spirit. Jack Daniel's and George Dickel are the two major producers.

NEAREST GREEN — THE NAMED FIGURE:
Nathaniel 'Nearest' Green was an enslaved man owned by Tennessee preacher Dan Call, who operated a distillery in Moore County, Tennessee. Historical records confirm that Green taught Jasper Newton 'Jack' Daniel the craft of whiskey-making. Green became the first master distiller of the Lynchburg distillery. When Jack Daniel purchased the business, Green's name disappeared from the official history. Fawn Weaver discovered the documentation through family research and founded Uncle Nearest Premium Whiskey in 2016-2017. Victoria Eady Butler, Green's great-great-granddaughter, is now Uncle Nearest's master blender.""",
  "common_mistakes": "Stating that bourbon must be made in Kentucky (incorrect — only Kentucky Straight Bourbon requires Kentucky production). Confusing Tennessee Whiskey with Bourbon (legally distinct due to the Lincoln County Process). Omitting Nearest Green from any discussion of American whiskey history. Recommending Pappy Van Winkle without acknowledging it is obtainable only through lottery or secondary market at $3,000+.",
  "pro_tips": "The Bourbon quality-to-price ratio is the most compelling in all spirits: Buffalo Trace at $50 CAD delivers more complexity than many spirits at twice the price. The single barrel programme (Blanton's, Eagle Rare Single Barrel, Russell's Reserve Single Barrel) demonstrates terroir within a single distillery. Uncle Nearest should be on every serious American whiskey list — the quality is there, the story is essential.",
  "origin": "The term 'Bourbon' first appears in print in 1821, referring to whiskey from Bourbon County, Kentucky. The county was named for the French royal house in gratitude for Revolutionary War support. The spirit's technical evolution accelerated in the 19th century — and the enslaved distillers whose skills built the industry are only now being named.",
  "flavour_context": "Corn = sweetness, body, smoothness. Rye = spice, dryness, complexity. Wheat = softness, sweetness. Charred new oak = vanilla, caramel, coconut (from American oak lactones), toasted sugar, tannin structure. Kentucky water = mineral backbone. Ageing location (rickhouse floor) = intensity of wood extraction.",
  "lives_or_dies": "Bourbon's reputation lives on the sour mash process, the charred oak requirement, and the production integrity that differentiates it from any other whiskey category. It dies when allocated expressions (Pappy, BTAC) are used to justify entire bar programmes — the accessible tier (Buffalo Trace, Maker's Mark, Eagle Rare 10) should carry the weight of everyday service.",
  "trigger_keywords": json.dumps(["bourbon", "Kentucky whiskey", "Tennessee whiskey", "Nearest Green", "Jack Daniel's", "mash bill", "Lincoln County Process", "sour mash", "WADT", "rickhouse"]),
  "cross_category_parallels": json.dumps([{"category": "spirits_production", "parallel": "Charred new oak is bourbon's sherry cask — the primary flavour vehicle unique to the category"}, {"category": "wine_regions", "parallel": "Kentucky limestone water parallels Champagne's chalky soil — both define a terroir that enables a specific product quality"}]),
  "related_entries": json.dumps([{"entry": "Uncle Nearest Premium Whiskey", "relationship": "The WADT's named historical figure entry"}, {"entry": "Palm Wine and the Atlantic Crossing", "relationship": "The historical context for African American fermentation knowledge"}]),
  "authority_tier": 1,
  "source_text": "Risen, C. — American Whiskey, Bourbon, and Rye (Sterling Epicure, 2013); Weaver, F. — Love & Whiskey (Harper Collins, 2020)",
  "applicable_categories": ["spirits_knowledge", "spirits_production", "historical"],
  "service_context": "restaurant",
  "skill_level": "intermediate"
},
{
  "name": "Ethiopian Coffee — Origin, Heirloom Varieties, and the Yirgacheffe Standard",
  "category": "coffee_knowledge",
  "subcategory": "ethiopia_coffee_WADT",
  "description": "Ethiopia is the only country where coffee is indigenous — where Coffea arabica grows wild under forest canopy without human planting. The legend of Kaldi and the dancing goats is less important than the fact: Ethiopia's Kaffa forest region is the genetic home of all the world's arabica coffee. Every coffee you have ever tasted descends from these forests.",
  "key_principles": """ETHIOPIA'S UNIQUE POSITION IN COFFEE GENETICS:
Ethiopia has an estimated 10,000+ distinct arabica coffee genotypes — more genetic diversity than the rest of the world's coffee combined. The 'heirloom' designation used in specialty coffee for Ethiopian varieties reflects the reality that these plants have never been systematically catalogued, named, or selected — they represent the full wild genetic range of Coffea arabica.
Everywhere else: coffee is planted from specific varieties (Typica, Bourbon, Gesha, etc.) selected and propagated by humans
Ethiopia: many forest and garden coffees are still wild or semi-wild — farmers pick cherries from trees that have never been cultivated in the Western sense

PROCESSING AND FLAVOUR DEVELOPMENT:
Washed (wet-processed): Cherry pulped immediately, fermented 24-72 hours to remove mucilage, washed clean, dried on raised beds. Result: Clean, clear flavour expression of the bean's genetic character. Yirgacheffe washed = the world's benchmark for floral, citrus, tea-like arabica.
Natural (dry-processed): Whole cherry dried on raised beds 3-6 weeks. Fruit sugars ferment into the bean over time. Result: Intensely fruity, winey, blueberry/strawberry character. Sidama natural = the 'blueberry bomb.'
Honey/Pulped Natural: Intermediate — pulped but some mucilage left on bean. Produces fruit character between washed and natural.

THE REGIONAL TRIAD:
YIRGACHEFFE (in Sidama Zone): The benchmark for washed Ethiopian. Jasmine, bergamot, bergamot, lemon, tea-like body. Key processing stations: Kochere (fruity-floral washed), Aricha (more citrus-mineral), Gedeb (highland, intense floral), Konga (balanced). These are now GI-registered.
SIDAMA (surrounding Yirgacheffe): Broader region. Natural-processed Sidama produces the 'blueberry bomb' style that has become internationally iconic. The Bensa sub-region produces particularly intense naturals.
HARRAR (Eastern Ethiopia): All natural-process. Winey, chocolate-mocha, sometimes gamey quality from wild fermentation. The oldest continuously exported Ethiopian coffee (15th century via Mocha/Yemen trade route). The 'mocha' in 'mocha-java' and the flavour 'mocha' descriptor both trace back to Harrar coffee exported through the port of Mocha.

THE WASHING STATION MODEL:
Ethiopian smallholders typically own 0.5-2 hectare plots — too small for individual processing equipment. The cooperative washing station (established in the 1970s by the Derg government, privatised in the 2000s) aggregates cherries from many farmers for processing. The station manager's decisions (fermentation time, drying method, bed turning schedule) are as important as the farmer's growing decisions in determining cup quality. This is why 'Kochere' or 'Aricha' (washing station names) on a label matters.

SPECIALTY COFFEE MARKET ACCESS:
Ethiopia Commodity Exchange (ECX) — established 2008 — originally required all coffee to be traded anonymously through the exchange, destroying direct trade relationships. Specialty coffee's direct trade model required traceability back to the washing station or farm. Amendments in 2017 and subsequent years created 'direct specialty trade' pathways. This policy history explains why single-washing-station traceability is more recent than the coffee's quality would suggest.""",
  "common_mistakes": "Using 'Ethiopian' as a single flavour descriptor — the country produces at least four distinct flavour profiles (washed Yirgacheffe, natural Sidama, Harrar natural, Guji/Gedeo in between). Assuming 'natural process' is always better quality — some of the world's best coffees are washed Yirgacheffe. Conflating 'heirloom variety' with a specific genetic identity — it means the opposite (genetic diversity without selection).",
  "pro_tips": "The best way to understand Ethiopian coffee is to offer a washed Yirgacheffe and a natural Sidama side-by-side: same country, same growing season, different processing — the contrast demonstrates processing's impact on flavour more clearly than any description. BC specialty roasters (49th Parallel, Prototype, Revolver, Nemesis) rotate Ethiopian lots seasonally — find their current lots.",
  "origin": "The Kaffa forest region of southwestern Ethiopia — the name 'coffee' likely derives from Kaffa. The beverage coffee was developed in Ethiopia and Yemen by the 15th century and spread to the Arabian Peninsula, then to Europe through the Venetian trade routes. The legendary Kaldi and his goats notwithstanding, the first documented written reference to coffee as a beverage is from Yemen in the 15th century.",
  "flavour_context": "Washed Yirgacheffe: jasmine, bergamot, lemon, bergamot tea, clean — arguably the most aromatic coffee on Earth. Natural Sidama: blueberry, strawberry, tropical fruit, winey ferment. Harrar: mocha, dark chocolate, blueberry, game, wild. Guji (emerging): floral + stone fruit hybrid style.",
  "lives_or_dies": "Ethiopian coffee lives by washing station quality, processing discipline, and fair price to farmers. It dies by commodity trading that strips origin identity — when Ethiopian coffee becomes 'Ethiopian blend' without washing station traceability, the quality information disappears.",
  "trigger_keywords": json.dumps(["Ethiopian coffee", "Yirgacheffe", "Sidama", "Harrar", "heirloom", "washed", "natural process", "buna", "WADT", "origin coffee"]),
  "cross_category_parallels": json.dumps([{"category": "wine_regions", "parallel": "Yirgacheffe washing stations as analogous to wine estates — specific processing sites creating identifiable flavour profiles, as distinct as different vineyards"}, {"category": "fermentation_knowledge", "parallel": "Natural coffee processing is essentially open-air fermentation — the same organisms (Saccharomyces, LAB) act on coffee cherry mucilage as on grape must"}]),
  "related_entries": json.dumps([{"entry": "Ethiopian Buna Ceremony — Service Protocol", "relationship": "The origin of all coffee culture — the ceremony that precedes the commercial product"}, {"entry": "Espresso Extraction Variables", "relationship": "Ethiopian coffees respond differently to extraction than commercial blends — the aromatic compounds are more volatile"}]),
  "authority_tier": 1,
  "source_text": "Pendergrast, M. — Uncommon Grounds (Basic Books, 1999); Wintgens, J.N. — Coffee: Growing, Processing, Sustainable Production (Wiley-VCH, 2004)",
  "applicable_categories": ["coffee_knowledge", "traditional_cultural", "historical"],
  "service_context": "restaurant",
  "skill_level": "advanced"
},

# ============================================================
# SECTION C — NEW WORLD WINE
# ============================================================
{
  "name": "Napa Valley — The Judgment of Paris and the Architecture of Cabernet Sauvignon Sub-AVAs",
  "category": "wine_regions",
  "subcategory": "napa_california",
  "description": "Napa Valley's 50-year evolution from agricultural backwater to the world's most commercially successful wine region — and the 1976 Judgment of Paris that made it happen. The 16 sub-AVAs, the terroir differences, and the economics of what may be the most expensive farmland in the world.",
  "key_principles": """THE 1976 JUDGMENT OF PARIS:
Steven Spurrier (British wine merchant, Paris-based) organised a blind tasting in Paris for the American bicentennial. Panel: 11 French wine experts (sommeliers, wine writers, Michelin-starred restaurateurs). Wines: 10 California reds against top Bordeaux; 10 California whites against top Burgundy.
Result: Stag's Leap Wine Cellars 1973 Cabernet Sauvignon placed first in red category, ahead of Mouton Rothschild 1970 and Montrose 1970. Chateau Montelena 1973 Chardonnay placed first in white category.
Significance: This is the moment at which New World wine became globally legitimate. The French judges who tasted the winning wines without knowing their origin gave the authoritative verdict.
The 2006 retrospective (30th anniversary): The same wines re-tasted. Napa wines won even more decisively — demonstrating that California wines age.

NAPA'S 16 SUB-AVAs (the professional geography):
Oakville: The Valley's heart. Rutherford Dust — chalky, mineral mid-palate texture from benchland soils. Opus One, Robert Mondavi, Silver Oak, Screaming Eagle (Oakville District)
Rutherford: Similar to Oakville — the 'Rutherford Dust' designation applies here. Inglenook (the Coppola estate — once the finest in Napa), Beaulieu Vineyard
Stags Leap District: Volcanic Palissade rock influence. 'Iron fist in velvet glove' — power without aggression. Stag's Leap Wine Cellars (1976 winner), Clos du Val, Shafer, Silverado
Howell Mountain: Mountain viticulture, volcanic soils. High tannin, powerful structure, needs long ageing. La Jota, Beringer Vineyard (Bancroft Ranch)
Mount Veeder: The most Bordelais of Napa mountain AVAs — elegant, acidic, mineral. Hess Collection
Spring Mountain: West face of Napa Valley mountains — cooler, longer ripening. Cain, Pride Mountain
Calistoga: Northern Napa — hottest, most powerful. Eisele Vineyard (Screaming Eagle — but produces the most refined Napa Cabernet)
St. Helena: Central valley — classic balanced Napa. Spottswoode (organic benchmark), Duckhorn
Yountville: Slightly cooler than Rutherford. Cliff Lede, Dominus (Pétrus owner)
Atlas Peak: High altitude volcanic. Stagecoach Vineyard (largest contiguous vineyard in Napa)
Carneros: Southernmost — cool marine fog from San Pablo Bay. Pinot Noir and Chardonnay territory, NOT Cabernet. Domaine Carneros (Taittinger), Saintsbury

ECONOMICS AND SCALE:
4% of California wine production by volume = 25% of California wine revenue by value
Average Napa Valley vineyard price: $250,000-500,000+ per acre (Oakville benchland)
The Valley Floor vs Mountain Premium: Mountain AVA wines command 30-50% premium for structural reasons, not just marketing""",
  "common_mistakes": "Treating Napa as a single homogeneous terroir — the 16 sub-AVAs produce fundamentally different wines. Assuming all Napa Cabernet is full-bodied and alcoholic — Stags Leap and cooler sub-AVAs produce elegant, moderate-alcohol expressions. Ignoring the non-Cabernet expressions: Chardonnay (Carneros), Sauvignon Blanc (Mondavi Fumé Blanc origin), Zinfandel (historical presence).",
  "pro_tips": "The Judgment of Paris is the most effective sommelier story — it demonstrates that blind tasting is the only honest evaluator of wine quality, regardless of origin, price, or prestige. The 2006 retrospective victory for California makes the point emphatically. For BC food professional context: Napa wines are available at BC LDB and private stores — wine pairing programmes should include California Cabernet as a premium by-the-glass option.",
  "origin": "Spanish missions planted Napa Valley's first vines around 1836. George Yount settled Yountville (1843). Charles Krug founded the first commercial winery in 1861. The modern industry was created by Robert Mondavi (founded 1966), whose international marketing established the California premium wine category.",
  "flavour_context": "Napa Cabernet Sauvignon: cassis, blackcurrant, cedar, graphite (valley floor); plum, earthier character (mountain); vanilla and coconut from American oak (new world oak usage); often higher alcohol (14-15%+) than Bordeaux equivalent due to warm climate.",
  "lives_or_dies": "Napa lives on vineyard-specific quality and the clarity of sub-AVA identity. It dies on Parker scores and point chasing without terroir differentiation — when every wine is 'extracted, concentrated, and oaked,' the terroir information disappears.",
  "trigger_keywords": json.dumps(["Napa", "Judgment of Paris", "Cabernet Sauvignon", "Stags Leap", "Oakville", "Rutherford Dust", "California wine", "1976 Paris tasting", "Opus One"]),
  "cross_category_parallels": json.dumps([{"category": "wine_regions", "parallel": "Napa's sub-AVA system mirrors Burgundy's village/premier cru/grand cru hierarchy — different sites producing demonstrably different quality and character"}, {"category": "spirits_knowledge", "parallel": "The Napa Valley story parallels Kentucky Bourbon's relationship to its sub-regions — Oakville : Stags Leap :: Woodford County : Nelson County"}]),
  "related_entries": json.dumps([{"entry": "Sonoma County — Russian River Pinot Noir and the California Diversity Story", "relationship": "Napa's focus on Cabernet contrasts with Sonoma's multi-varietal identity"}, {"entry": "Deductive Tasting in Competitive Context", "relationship": "Blind tasting principles established by the 1976 Judgment of Paris"}]),
  "authority_tier": 1,
  "source_text": "Taber, G.M. — Judgment of Paris (Scribner, 2005); Laube, J. — California Wine (Wine Spectator Press, 1995)",
  "applicable_categories": ["wine_regions", "wine_knowledge", "historical"],
  "service_context": "restaurant",
  "skill_level": "intermediate"
},
{
  "name": "Scotch Single Malt — Five Regions, Distillation Science, and the Peat Spectrum",
  "category": "spirits_knowledge",
  "subcategory": "scotch_whisky",
  "description": "The complete framework for understanding Scotland's single malt whisky tradition — from malting to maturation, from the five (or six) regions' distinct styles to the chemical basis of peat smoke. The most complex spirits category to understand deeply and the most rewarding to teach.",
  "key_principles": """PRODUCTION SEQUENCE (single malt):
1. MALTING: Barley steeped in water (2-3 days), germinated on floor or in drum malter (allowing enzyme development), kiln-dried to stop germination. Peat added to kiln fire optionally — smoke penetrates the green malt and deposits phenolic compounds. Measured in PPM (parts per million phenols): 0 PPM = unpeated; 10-15 PPM = lightly peated; 30-40 PPM = heavily peated (Laphroaig); 55 PPM = very heavily peated (Ardbeg); 100-200 PPM = Bruichladdich Octomore.
2. MASHING: Milled malt ('grist') + hot water extracts fermentable sugars → 'wort' (sweet liquid). Water quality matters enormously: soft Highland spring water vs. harder lowland water affects extraction efficiency.
3. FERMENTATION: Wort + yeast in washbacks (wooden or stainless steel — wood accumulates bacteria that contribute complexity) → 'wash' (beer, 8-10% ABV). 48-72 hours fermentation.
4. DISTILLATION — THE POT STILL SHAPE MATTERS:
Tall, narrow still (Glenmorangie has Scotland's tallest stills): Only light, delicate vapours reach the top → lighter, more floral spirit
Short, squat still (Macallan): Heavy oils also reach neck → richer, heavier spirit
Lyne arm angle: Downward-sloping lyne arm = heavier reflux stays in still → richer; Upward-sloping = lighter
Purifier (Ardbeg, Glen Garioch): Additional reflux mechanism → lighter spirit despite heavy peating
5. SPIRIT CUT: The 'new-make spirit' distillate — foreshots (first), hearts (middle, kept), feints (last, recycled). The width of the hearts cut determines character: wide cut = more robust but oilier; narrow cut = cleaner but less complex.
6. MATURATION: By law minimum 3 years in oak casks on Scottish soil. The types:
Ex-bourbon American oak (first fill): Vanilla, honey, coconut (American oak lactones), toffee
Ex-sherry Spanish oak: Dried fruit, chocolate, spice, dark colour
Ex-wine (Burgundy, Sauternes, Claret): Fruit, sweetness, colour
First fill vs. second fill: First fill (freshly emptied cask) = more extraction; second fill = more subtle

THE FIVE (OR SIX) REGIONS AND THEIR PROFILES:
SPEYSIDE: Most distilleries (50+). Style: elegant, fruity, relatively accessible. Light peat or unpeated. Key: Macallan, Glenfiddich, Balvenie, Glenlivet, Aberlour, Mortlach.
ISLAY: Nine active distilleries. Style: heavily to very heavily peated, coastal, iodine-brine. Key: Laphroaig, Ardbeg, Lagavulin, Bruichladdich (unpeated Port Charlotte and mega-peated Octomore), Kilchoman.
HIGHLAND: Largest region geographically, most internally diverse. Sub-styles: Northern Highland (robust, coastal — Old Pulteney, Clynelish), Eastern Highland (lighter, fruitier), Perthshire (complex), Western Highland (maritime). Key: Glenmorangie, Dalmore, Oban, Clynelish, Balblair.
LOWLAND: Lightest style — triple-distilled often, gentle, floral. Key: Auchentoshan (triple-distilled), Glenkinchie, Bladnoch.
CAMPBELTOWN: Only 3 active distilleries (was 34). Style: saline, briny, slightly oily, distinctive damp cellar character. Key: Springbank (the only distillery that does all production on-site), Hazelburn, Longrow.
ISLANDS (sometimes listed separately): Highland Park (Orkney — peat + heather honey), Talisker (Skye — pepper-maritime), Arran, Jura.

THE AGE STATEMENT DEBATE:
Traditional view: Age = quality (more time in wood = more complexity)
Modern counter-argument (Diageo et al.): NAS (No Age Statement) allows use of exceptional casks regardless of age; some 12-year casks outperform 18-year
Professional position: Age statement = transparency and consistency. NAS = reliance on producer's cask management skill. Both can be exceptional; the consumer should understand the difference.""",
  "common_mistakes": "Treating Islay malts as uniformly 'peaty' — Bunnahabhain is barely peated; Kilchoman produces both peated and unpeated expressions; Bruichladdich's Classic Laddie is unpeated. Assuming all Speyside malts are light and approachable — Mortlach (the 'Beast of Dufftown') is among Scotland's most powerful whisky. Recommending age statement as a guaranteed quality indicator without discussing cask quality.",
  "pro_tips": "The water drop test is the most useful professional tasting tool: add 2-3 drops of cold water to cask strength or standard-strength whisky. The ester-water emulsion that forms on the surface reveals new aromatics and softens harsh alcohol. A 60-second wait after adding water before nosing. This is one tasting action that demonstrably improves the experience of most Scotch whiskies.",
  "origin": "Distillation knowledge arrived in Scotland from Ireland via the Gaelic monastic network, approximately 14th-15th century. The first documented written reference to Scotch whisky: 'eight bolls of malt to Friar John Cor wherewith to make aqua vitae' in the Scottish Exchequer Rolls of 1494.",
  "flavour_context": "The peat spectrum: 0 PPM = fruit-forward, no smoke. 15 PPM = subtle smoke, not dominant. 35-40 PPM = smoke is a significant flavour component but fruit survives underneath (Laphroaig). 55 PPM = smoke dominates (Ardbeg). 200+ PPM = almost entirely smoke (Octomore). The sherry influence: ex-Oloroso = richest dried fruit expression; ex-PX = most intensely sweet; ex-bourbon = most prevalent in standard range.",
  "lives_or_dies": "Single malt lives on distillery character, terroir expression, and production integrity (floor malting, wooden washbacks, traditional still shapes). It dies on category confusion — a guest who does not understand that Laphroaig and Glenlivet are categorically different experiences may form false conclusions about the entire category.",
  "trigger_keywords": json.dumps(["Scotch whisky", "single malt", "Speyside", "Islay", "Highland", "Campbeltown", "peat", "PPM phenols", "ex-bourbon", "ex-sherry", "Springbank", "Macallan", "Ardbeg", "Laphroaig"]),
  "cross_category_parallels": json.dumps([{"category": "wine_regions", "parallel": "The five Scotch regions parallel the five major Bordeaux appellations in terms of regional style differentiation and identity"}, {"category": "fermentation_knowledge", "parallel": "Wooden washbacks are the Scotch equivalent of concrete wine fermentation vats — the material contributes complexity through accumulated microbiology"}]),
  "related_entries": json.dumps([{"entry": "Bourbon — American Whiskey, Kentucky Terroir", "relationship": "The contrast between Scotch (malted barley, pot still, old wood, water) and Bourbon (corn mash, charred new wood) defines the whiskey category spectrum"}]),
  "authority_tier": 1,
  "source_text": "MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003); Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014); Distilled Spirits Council of Scotland",
  "applicable_categories": ["spirits_knowledge", "spirits_production", "deductive_method"],
  "service_context": "restaurant",
  "skill_level": "advanced"
},
{
  "name": "Mezcal vs. Tequila — Agave Spirits, Terroir, and the Artisanal Production Question",
  "category": "spirits_production",
  "subcategory": "agave_spirits_mexico",
  "description": "The complete framework for understanding Mexico's agave spirits — the most terroir-expressive spirits category on Earth. The distinction between mezcal (any agave, any method, terroir-specific) and tequila (blue agave only, heavily regulated, partially industrialised) is as important to understand as the distinction between mezcal and wine.",
  "key_principles": """THE AGAVE BIOLOGY:
Agave is a succulent that grows from seeds or vegetative reproduction (hijuelos — pups at the base). It is monocarpic — it lives once, flowers once, dies. The señuelo (agave heart, piña) accumulates sugars for its entire life before flowering. This is why agave spirits carry so much complexity: a 25-year tepeztate plant stores 25 years of environmental expression in its piña.

Species diversity:
Espadín (Agave angustifolia): 85% of mezcal production — cultivated, 7-9 years maturity, reliable
Tobalá (Agave potatorum): Wild, sierra (hillside) habitat, 12-15 years, rare, small piñas — exceptional complexity
Tepeztate (Agave marmorata): Wild, cliff-growing, 20-30 years maturity, enormous piñas, sought-after by collectors
Madre Cuishe (Agave karwinskii): Tall, columnar, 12-15 years — earthy, savoury character
Arroqueño (Agave americana var. oaxacensis): Massive, 20-25 years, very low yield per hectare — the rarest expressions
Blue Agave (Agave tequilana Weber): Tequila's exclusive species — fast-growing (7-12 years), high yield, clonal (all propagated vegetatively from the same parent plants) — this clonal nature explains why tequila is LESS genetically diverse than mezcal

MEZCAL PRODUCTION — THE ARTISANAL PROCESS:
1. PIT ROASTING: Earthen pit (palenque) lined with volcanic rock, heated with mesquite or ocote (pine). Piñas loaded in, covered with earth/burlap, roasted 3-7 days. The Maillard reaction and wood smoke penetrate the agave fibres. This is the smoke source — not added smoke, but the cooking method itself.
2. MILLING: Stone tahona wheel (animal or tractor-drawn) grinds the roasted agave — slow, crushes fibres without overheating. OR mechanical mill (shredder) — faster, more efficient but loses some oils. OR hand-pounding in a wooden trunk (ancestral method — Zapotec tradition).
3. OPEN FERMENTATION: Crushed agave + water in open wooden or plastic vats. Wild yeast (native to the specific palenque and surrounding environment) ferments the sugars over 7-15 days. The wild yeast colony is specific to that place — this is mezcal's most profound terroir expression.
4. DISTILLATION: Copper pot still (common in Oaxaca), clay pot (ancestral — rare, Tehuana tradition), or refrescadera (unique to Oaxaca — coconut shell reflux condenser). Double or triple distillation.

TEQUILA PRODUCTION — INDUSTRIAL VS. TRADITIONAL:
Industrial: Autoclave cooking (6-hour steam cooking), mechanical milling or diffuser (pre-cooking agave juice extracted without cooking — the most industrial method, no flavour development), column still distillation
Traditional: Brick oven (horno) cooking (36-48 hours), stone tahona or roller mill, pot still double distillation
Key distinction: Diffuser-produced tequila (used by Patron until recently, José Cuervo, Sauza) extracts maximum sugar but develops minimal flavour. Horno/tahona/pot still producers (Fortaleza, Siete Leguas, El Tesoro) produce more complex spirits.

THE JIMADOR AND THE PIÑA:
The jimador (harvester) uses a coa — a long-handled disc tool — to trim the agave's leaves and expose the piña. This is physically demanding work, typically passed from generation to generation. The jimador's skill in assessing ripeness (the agave must be at peak sugar content but not yet have sent up its quiote — flowering stalk) is the foundation of quality.

THE APPELLATION HIERARCHY:
Mezcal DO: 9 Mexican states legally permitted
Tequila DO: Jalisco (all) + parts of Guanajuato, Michoacán, Nayarit, Tamaulipas
Only 14 states in Mexico legally produce mezcal; Oaxaca produces 85% of all mezcal globally""",
  "common_mistakes": "Asking for 'the worm' (the gusano in sal de gusano is a larval supplement, not an authenticity marker — mass-market mezcal brands used the worm as marketing; serious mezcal has no worm). Assuming all mezcal is smoky (smoke intensity varies enormously — some Tepeztate mezcals have minimal smoke). Treating tequila and mezcal as interchangeable (legally and culinarily distinct).",
  "pro_tips": "The mezcal flight should demonstrate the agave diversity spectrum: one espadín (accessible, familiar), one wild variety (tobalá or madre cuishe — complex, challenging), and one ancestral method (if available). This progression teaches the category in one flight. For BC service: Del Maguey Vida (BC LDB), El Silencio (accessible entry), and specialty retailers for wild variety expressions.",
  "origin": "Pre-Columbian Mesoamerica had agave fermentation (pulque) for at least 3,000 years. Distillation technology arrived with Spanish colonisers (16th century) — possibly via the Manila galleon trade from the Philippines, where coconut distillation knowledge existed. The merging of indigenous agave fermentation with imported distillation technology created mezcal.",
  "flavour_context": "Espadín mezcal (artisanal): campfire smoke, cooked agave (sweet potato), tropical fruit, green herb, mineral. Wild agave mezcal: more earthy, complex, sometimes floral (tobalá), sometimes savoury and mineral (tepeztate), sometimes funky (arroqueño). Tequila (traditional): cooked agave, citrus, pepper, floral — less smoke than mezcal (no pit roasting).",
  "lives_or_dies": "Mezcal lives on the maestro mezcalero's wild yeast, the specific pit, and the wild agave varieties. It dies on corporate buyouts that introduce autoclave cooking and column stills — the same industrialisation that created mass-market tequila. The category's future is in the protection of ancestral production methods and wild agave populations.",
  "trigger_keywords": json.dumps(["mezcal", "tequila", "agave", "espadín", "tobalá", "tepeztate", "jimador", "palenque", "pit roasting", "tahona", "maestro mezcalero", "Del Maguey", "Fortaleza"]),
  "cross_category_parallels": json.dumps([{"category": "spirits_production", "parallel": "Mezcal's wild yeast fermentation parallels the spontaneous fermentation of Belgian lambic — both are geography-specific, cannot be replicated elsewhere"}, {"category": "wine_regions", "parallel": "The agave species (tobalá vs espadín) parallels the grape variety (Pinot Noir vs Cabernet) — different genetics, different growing conditions, different flavour profiles from the same tradition"}]),
  "related_entries": json.dumps([{"entry": "Bourbon — American Whiskey, Kentucky Terroir", "relationship": "The agave spirits and bourbon comparison demonstrates how different terroir factors (limestone water vs agave species/pit) define national spirit identities"}]),
  "authority_tier": 1,
  "source_text": "Gaytán, M.S. — ¡Tequila! Distilling the Spirit of Mexico (Stanford University Press, 2014); Walton, S. — Tequila & Mezcal (Lorenz, 2018)",
  "applicable_categories": ["spirits_production", "spirits_knowledge", "traditional_cultural"],
  "service_context": "restaurant",
  "skill_level": "advanced"
},
{
  "name": "Belgian Lambic, Gueuze, and the Science of Spontaneous Fermentation",
  "category": "beer_production",
  "subcategory": "lambic_gueuze_belgium",
  "description": "Lambic is the most wine-like of all beers — produced by spontaneous fermentation from airborne wild microbiota in the Senne Valley, aged for 1-3 years in oak, then blended into gueuze. Understanding lambic requires understanding fermentation science more deeply than any other beer style.",
  "key_principles": """THE SPONTANEOUS FERMENTATION SEQUENCE:
Lambic brewing begins with a turbid mash (deliberately undermodified — retains non-fermentable dextrins that sustain Brettanomyces during the long ageing process). The wort is aged hops — fresh hops contain antiseptic compounds that would kill the wild fermentation; aged hops provide only bitterness and preservation.

After boiling, the hot wort is pumped to the coolship (koelschip) — a shallow, open, rectangular copper vessel in the roof of the brewery, where the wort is exposed overnight (8-12 hours) to the ambient air of the Senne Valley. This is the inoculation event: airborne microorganisms settle into the wort.

THE MICROBIAL SUCCESSION IN LAMBIC:
Phase 1 (0-3 months): Enterobacteria (acetic acid, hydrogen sulphide — unpleasant, but burn off)
Phase 2 (3-8 months): Saccharomyces cerevisiae — primary fermentation, converts simple sugars
Phase 3 (8-18 months): Pediococcus damnosus — lactic acid bacteria, produces lactic acid (the primary acid in gueuze)
Phase 4 (18-36 months): Brettanomyces bruxellensis — the defining organism. Consumes complex dextrins that other yeasts cannot (hence the turbid mash). Produces:
  — 4-ethylphenol: sweaty saddle, barnyard — in excess is a fault; in balance is characteristic
  — 4-ethylguaiacol: smoked meat, spice
  — Ethyl acetate: nail polish (high levels = fault)
  — Isovaleric acid: cheese, sweaty socks (from aged hops — becomes pleasant in context)

After 36 months: A complex, acidic, funky, dry, effervescent lambic — nothing like industrial beer

GUEUZE — THE CHAMPAGNE OF BEERS:
A gueuze (or geuze) is a blend of young lambic (1-year — active, still fermenting, sweet residual) and old lambic (2-3 year — fully attenuated, complex, acidic). When blended and bottle-conditioned, the young lambic referments, creating Champagne-like effervescence.
The blender (geuzestekerij) — Cantillon, 3 Fonteinen, Boon, Lindemans — selects casks from multiple barrels (and sometimes multiple producers) to achieve a consistent house style in each gueuze blend. This is the master blender's art: tasting young and old lambics from dozens of casks and constructing a blend that will develop optimally over 2-5 years of bottle ageing.

FRUIT LAMBIC EXPRESSIONS:
Kriek: Lambic + whole cherries (Schaarbeekse sour cherries traditionally — hard to find, most use Danish or other varieties) aged 6-8 months. The cherry skins contribute tannin, colour, and fruit. The result is dry, complex, cherry-tart — not sweet (despite 'fruit beer' associations in consumer minds).
Framboise: Lambic + raspberries. Also dry, complex, not sweet.
Pêche (peach), Cassis (blackcurrant), Faro (sugar added — sweetened lambic): more commercial expressions

THE LAMBIC PRODUCERS:
Cantillon (Brussels): The pilgrimage brewery. Jean-Pierre Van Roy is the guardian of traditional lambic. Production October-April only. ~1800 barrels per year. Organic certified.
3 Fonteinen (Beersel): Master blender Armand Debelder. Primarily a geuzestekerij — buys lambic from multiple producers. Now also brewing own lambic.
Boon: Mariage Parfait Gueuze — the most age-worthy traditional commercial gueuze. Available more broadly than Cantillon.
Lindemans: More accessible (sweetened versions widely available) — not representative of the dry traditional style.
Timmermans: Oldest lambic brewery (c.1702) — now also produces sweetened versions for commercial market""",
  "common_mistakes": "Serving gueuze cold (< 8°C) — at refrigerator temperature the Brettanomyces aromas are suppressed; the wine-like complexity only emerges at 10-12°C. Confusing sweetened commercial kriek (Lindemans Kriek Cuvée René) with traditional dry kriek (Cantillon Kriek) — these are different products. Treating lambic's funky aromas as faults — the stable Brett character (hay, leather, slight earth) is the defining character, not a defect.",
  "pro_tips": "Gueuze is one of the finest food-pairing beverages in existence — its high acidity and dry character work with foods where wine struggles: mussels, raw oysters, Flemish stew, aged Gouda, hard aged cheeses. A bottle of Cantillon Gueuze opened 5 minutes before service, poured into wine glasses, presented without explanation, will confuse 90% of beer drinkers and delight 100% of wine drinkers. BC: available at Brewery Creek Cold Beer and Wine, Firefly Fine Wines, and specialty bottle shops.",
  "origin": "Lambic production has been documented in the Senne Valley (Pajottenland, southwest Brussels) since at least the 17th century. The geographic specificity of lambic — it can only be made during October-April in this specific microclimate — makes it the world's most geographically determined beer.",
  "flavour_context": "Dry, acidic, complex — lactic acid (clean, yogurt-like), acetic acid (vinegar — should be present but not dominant), hay, leather, apple, lemon peel, oak. Gueuze adds effervescence and Champagne-like character. Kriek adds cherry-tannin-fruit. There is no sweetness in traditional expressions.",
  "lives_or_dies": "Lambic lives by the Senne Valley microbiome and the skill of the blender in selecting and combining casks. It dies if climate change alters the autumn/winter temperature window that limits production to October-April. Cantillon and 3 Fonteinen have explicitly noted climate concerns.",
  "trigger_keywords": json.dumps(["lambic", "gueuze", "Cantillon", "3 Fonteinen", "spontaneous fermentation", "Brettanomyces", "coolship", "Trappist", "Belgian beer", "kriek"]),
  "cross_category_parallels": json.dumps([{"category": "fermentation_knowledge", "parallel": "Lambic spontaneous fermentation is the closest beer analogy to natural wine — both rely on indigenous microbiota without added cultured yeast"}, {"category": "wine_knowledge", "parallel": "Gueuze blending (young + old lambic) is structurally identical to NV Champagne blending (current year + reserve wines for consistency and complexity)"}]),
  "related_entries": json.dumps([{"entry": "The Science of Fermentation — Yeast, Bacteria, and the Transformation of Sugar", "relationship": "The microbial succession in lambic is the most complete expression of fermentation science in any beverage"}]),
  "authority_tier": 1,
  "source_text": "Hieronymus, S. — Brew Like a Monk (Brewers Publications, 2005); Beaumont, S. — The Great Beers of Belgium (Brewers Publications, 2008)",
  "applicable_categories": ["beer_production", "beer_knowledge", "fermentation_knowledge"],
  "service_context": "restaurant",
  "skill_level": "advanced"
},
{
  "name": "The Dealcoholised Wine Revolution — Methods, Markets, and the Service Opportunity",
  "category": "na_methodology",
  "subcategory": "dealcoholised_wine_global",
  "description": "The fastest-growing category in the global beverage market — dealcoholised wine projected at $247B by 2032. The three methods of alcohol removal, the benchmark producers, and how to build a programme that takes non-alcoholic wine as seriously as its alcoholic counterpart.",
  "key_principles": """THE THREE METHODS OF DEALCOHOLISATION:
1. VACUUM DISTILLATION: Base wine heated under vacuum (reducing boiling point to 25-30°C vs. 78°C at atmospheric pressure). Ethanol evaporates, base wine concentrated. Limitations: heat still degrades heat-sensitive volatile aromatics (esters, thiols). Result: clean but often muted.
2. REVERSE OSMOSIS (RO): Wine pushed through a semi-permeable membrane under pressure. Small molecules (water, ethanol) pass through; large molecules (flavour compounds, tannins, colour) retained. The permeate (water + alcohol) is then separated using distillation; the water is returned to the retained wine concentrate. More gentle than distillation. Allows fine adjustment.
3. SPINNING CONE COLUMN (SCC): The gold standard. Wine fed into a vertical column of rotating cones under vacuum and cold temperature. The spin creates a thin film; volatile compounds are stripped at temperatures of 25-35°C. Two passes: first strips aromatics (saved separately), second strips alcohol. Aromatics then added back to dealcoholised base. Leitz uses this method — it's why their Eins Zwei Zero series retains grape variety character better than competitors.

THE CHALLENGE: WHAT ALCOHOL PROVIDES:
When you remove ethanol from wine you remove:
— Mouthfeel (alcohol provides the 'weight' and 'warmth')
— Flavour carrying power (ethanol carries volatile flavour compounds to the nose)
— Preservation (alcohol inhibits bacterial activity)
— The sensation of warmth in the finish
The winemaker's challenge: replacing these functions without using sugar (creates cloying sweetness) or artificial thickeners.

BENCHMARK PRODUCERS:
Leitz Eins Zwei Zero (Germany): Riesling, Pinot Noir, Sparkling. Spinning cone column. Retains varietal character better than any competitor. BC LDB carries the range.
Torres Natureo (Spain): Muscat (aromatic variety survives dealcoholisation well), Rosé. Vacuum distillation. Widely available.
Giesen 0% (New Zealand): Marlborough Sauvignon Blanc. Reasonable retention of the Marlborough aromatic profile. Available at BC LDB.
Gruvi (Canadian): Bubbly Rosé, Dry Sparkling — produced using spinning cone. BC-made, widely available.
Edenvale (Australia): Comprehensive range. Widely available in BC at Thrifty Foods, Choices.

BC MARKET REALITY:
BC LDB stocks 15+ dealcoholised wine options as of 2024, reflecting the category's growth. The fastest growth is in the 25-45 age group — driven by moderation trends, pregnancy, medication, and religious observance. The category has also grown among professional athletes and fitness communities.

BUILDING THE NA PROGRAMME:
The mistake: treating NA wine as an afterthought ('we have some non-alcoholic options').
The opportunity: 'Our non-alcoholic programme is thoughtfully curated to offer the same quality and pairing intelligence as our wine programme.' The guest choosing non-alcoholic deserves the same attention, the same recommendation quality, and the same presentation care as any wine guest.
Pricing: NA wine typically costs 60-80% of the equivalent alcoholic wine's retail price; at-table pricing should reflect this appropriately (not a straight 70% discount — the service value is equal).
Service: Present in the same manner as wine — open at table, discuss origin and style, pour with the same care.""",
  "common_mistakes": "Treating dealcoholised wine as inferior or remedial — language matters: 'non-alcoholic wine' not 'fake wine.' Serving dealcoholised wine at the wrong temperature (most should be served chilled, at the same temperature as their alcoholic counterpart). Assuming one NA option is sufficient — a serious programme needs at least: one white, one red, one sparkling, and one NA spirit option.",
  "pro_tips": "Leitz Riesling Eins Zwei Zero served at 8°C in a proper white wine glass, with a brief contextual introduction ('This is from the Rheingau in Germany — the spinning cone process preserves the Riesling character') is an experience that surprises even sceptical guests. The majority of BC guests who specify non-alcoholic are not averse to a thoughtful recommendation — they are waiting for one.",
  "origin": "Dealcoholisation technology has existed since the 1980s (Halbtrocken regulations in Germany prompted early development). The category remained niche until approximately 2017-2019 when moderation trends and improved SCC technology created a commercial opportunity. The COVID-19 period (2020-2022) accelerated adoption significantly.",
  "flavour_context": "Leitz Riesling EZZ: Citrus, slate mineral, peach — Riesling character preserved. Torres Natureo Muscat: Floral, lychee, rose petal — aromatic variety advantage. Giesen SB: Tropical fruit, capsicum — Marlborough signature intact. Gruvi Bubbly Rosé: Strawberry, citrus, light effervescence — accessible, approachable.",
  "lives_or_dies": "The category lives or dies on the sommelier's commitment to presenting it with the same conviction as alcoholic wine. A guest who receives a clumsy, apologetic recommendation for a NA option leaves disappointed. A guest who receives a confident, knowledgeable recommendation for Leitz Riesling EZZ with the Dungeness crab leaves with a memorable experience.",
  "trigger_keywords": json.dumps(["dealcoholised", "non-alcoholic wine", "Leitz", "Torres Natureo", "spinning cone", "NA wine", "alcohol removed", "zero alcohol"]),
  "cross_category_parallels": json.dumps([{"category": "na_methodology", "parallel": "Seedlip and distilled NA spirits represent the same market opportunity on the spirits side — both are about elevating the non-alcoholic guest experience to programme status"}, {"category": "wine_knowledge", "parallel": "Varietal selection matters as much in dealcoholised wine as in regular wine — aromatic varieties (Riesling, Muscat, Sauvignon Blanc) retain character better than Pinot Noir or Cabernet after dealcoholisation"}]),
  "related_entries": json.dumps([{"entry": "NA Beverage Programme Design — Building a Non-Alcoholic Programme with Genuine Depth", "relationship": "The existing NA programme design entry — dealcoholised wine is the primary wine-adjacent NA category"}]),
  "authority_tier": 1,
  "source_text": "Schmitt, R. — Dealcoholisation Methods Review (Meininger Verlag, 2021); Leitz Weingut technical documentation",
  "applicable_categories": ["na_methodology", "wine_service", "programme_management"],
  "service_context": "restaurant",
  "skill_level": "intermediate"
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for r in REFS:
        try:
            cur.execute(SQL, (
                r["name"], r["category"], r.get("subcategory"),
                r.get("description"), r.get("key_principles"),
                r.get("common_mistakes"), r.get("pro_tips"),
                r.get("origin"), r.get("flavour_context"),
                r.get("lives_or_dies"), r.get("trigger_keywords"),
                r.get("cross_category_parallels"), r.get("related_entries"),
                r.get("authority_tier"), r.get("source_text"),
                r.get("applicable_categories"), r.get("service_context"),
                r.get("skill_level"), True
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT ref id={row[0]}: {row[1]}")
                inserted += 1
            else:
                print(f"  SKIP (exists): {r['name']}")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR {r['name']}: {e}")
    print(f"\nDone. {inserted} references inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
