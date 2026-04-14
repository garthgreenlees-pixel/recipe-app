#!/usr/bin/env python3
"""Terminal 4 — Batch 1: New beverage_regions for Pacific, Africa, Americas, Europe, Oceania"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO beverage_regions
  (name, country, beverage_family, designation_type, designation_name,
   regulatory_framework, terroir_profile, quality_trajectory, reputation_tier,
   description, key_producers, historical_context, authority_tier, source_text,
   is_published, slug)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING RETURNING id, name"""

REGIONS = [

# ============================================================
# PACIFIC ISLANDS — TRADITIONAL / KAVA
# ============================================================
{
  "name": "Vanuatu — Kava",
  "country": "Vanuatu",
  "beverage_family": "traditional",
  "designation_type": "Cultural Heritage Region",
  "designation_name": "Melanesian Kava Origin",
  "regulatory_framework": json.dumps({"body": "Vanuatu Kava Act 2002", "noble_only_exports": True, "tudei_export_ban": True}),
  "terroir_profile": json.dumps({"soil": "volcanic", "climate": "tropical", "altitude_m": "0-800", "species": "Piper methysticum", "cultivar_diversity": "highest on Earth — 80+ named varieties"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Vanuatu is the birthplace and spiritual home of kava culture — the archipelago with the greatest cultivar diversity on Earth, where kava is both daily social lubricant and sacred ceremonial substance. The nakamal (kava bar) is the institution of Melanesian civil society. Vanuatu's Noble varieties — Borogu, Melomelo, Kelai — are the benchmark for quality; Tudei (two-day) varieties, which produce hangover-like effects, are banned from export under the 2002 Kava Act.",
  "key_producers": "Tanna Kava (South Vanuatu), Bia Kava, Pacific Elixir (export Noble varieties), Deep Nature Vanuatu",
  "historical_context": "Kava has been cultivated in Vanuatu for at least 3,000 years, spreading outward from the islands of Vanuatu and Fiji across Polynesia with the Lapita migrations. The nakamal predates European contact by millennia. Colonial suppression by Christian missionaries in the 19th-20th centuries was partially reversed after independence (1980), and kava culture has experienced a global renaissance since 2015.",
  "authority_tier": 1,
  "source_text": "Lebot, V., Merlin, M. & Lindstrom, L. — Kava: The Pacific Elixir (Yale University Press, 1992); Vanuatu Kava Act 2002",
  "slug": "vanuatu-kava"
},
{
  "name": "Fiji — Yaqona",
  "country": "Fiji",
  "beverage_family": "traditional",
  "designation_type": "Cultural Heritage Region",
  "designation_name": "Fijian Yaqona Tradition",
  "regulatory_framework": json.dumps({"body": "Fiji Kava Decree 2020", "grog_license": True}),
  "terroir_profile": json.dumps({"soil": "volcanic loam", "climate": "tropical", "primary_variety": "Vula Kasa Leka (Fijian Noble)", "ceremony_context": "Formal — chiefs, diplomacy, welcome"}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "In Fiji, kava is called yaqona (pronounced yang-gona) or grog. The Fijian ceremony is among the most formalised in the Pacific — a tabua (whale's tooth) may be presented with kava as an offering of respect, and the ceremony governs diplomatic relations, conflict resolution, and chiefly succession. The bilo (coconut shell cup), the tanoa (wooden mixing bowl), and the specific clapping sequence (cobo — one sharp clap before receiving, three claps after) are codified cultural knowledge.",
  "key_producers": "Taki Mai (export-grade Fijian kava), Fiji Kava Ltd (ASX-listed — largest commercial kava exporter), Wakaya Perfection (organic premium)",
  "historical_context": "Fiji's yaqona ceremony is documented by European traders from the 1790s. Captain Cook received kava ceremonies at multiple Pacific islands. The Fijian tradition is distinctive in its extreme formalisation and its integration with the mataqali (clan) social structure. Post-independence Fiji (1970) has seen yaqona ceremony codified as national cultural identity.",
  "authority_tier": 1,
  "source_text": "Tomlinson, M. — Ritual Textuality: Pattern and Motion in Performance (Oxford University Press, 2014); Fiji Kava Decree 2020",
  "slug": "fiji-yaqona"
},
{
  "name": "Hawaii — Awa",
  "country": "USA",
  "beverage_family": "traditional",
  "designation_type": "Cultural Revival Region",
  "designation_name": "Hawaiian Awa Revival",
  "regulatory_framework": json.dumps({"body": "Hawaii Department of Agriculture", "notes": "Cultural revival since 1970s Hawaiian Renaissance"}),
  "terroir_profile": json.dumps({"islands": ["Big Island", "Maui", "Kauai"], "varieties": ["Mahakea", "Mo'i (chiefly — for ali'i only historically)", "Hiwa (black stem, ceremonial)"], "climate": "tropical volcanic"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "respected",
  "description": "Awa (the Hawaiian pronunciation of kava) was brought to Hawaii by the original Polynesian voyagers, likely from the Marquesas, around 400-800 CE. In pre-contact Hawaii, awa was strictly regulated — certain varieties were reserved for ali'i (chiefs) and kahunas (priests). The Hawaiian Renaissance beginning in the 1970s has revived both language and cultural practices including awa ceremony. Hawaiian awa farms on the Big Island's Puna district grow some of the finest kava available commercially.",
  "key_producers": "Kona Kava Farm (Big Island), Hawaii Awa (Puna district), Mana Kava (cultural ceremony focus)",
  "historical_context": "Awa was brought to Hawaii by Polynesian voyagers from the Marquesas Islands. Pre-contact Hawaiian awa culture included the Hale 'Awa — the dedicated kava house — and specific protocols governing who could prepare and serve awa. Christian missionary suppression in the 19th century nearly eradicated the tradition. The Hawaiian Renaissance (1970s-present) has restored cultural practices including hula, language, voyaging, and awa ceremony.",
  "authority_tier": 2,
  "source_text": "Titcomb, M. — Kava in Hawaii (Journal of the Polynesian Society, 1948); Whistler, W.A. — The Ethnobotany of Tonga (Bishop Museum Bulletin, 1992)",
  "slug": "hawaii-awa"
},
{
  "name": "Samoa — Ava",
  "country": "Samoa",
  "beverage_family": "traditional",
  "designation_type": "Cultural Heritage Region",
  "designation_name": "Samoan Ava Ceremony",
  "regulatory_framework": json.dumps({"body": "Samoan Government / Traditional Fono system", "notes": "Most formalised ceremony in Polynesia"}),
  "terroir_profile": json.dumps({"primary_variety": "Loa (long stem)", "preparation": "Chewed root historically, now pounded", "setting": "Fale tele (ceremonial house)"}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "The Samoan ava ceremony is considered the most formalised of all Pacific kava traditions — governed by strict protocol including specific seating arrangements according to rank, prescribed speeches, a designated taupo (ceremonial hostess from the chief's family) who prepares and serves the ava, and a specific calling out of each recipient's title before their cup is presented. The ceremony is the mechanism by which Samoan social hierarchy is enacted and reaffirmed.",
  "key_producers": "Traditional village-level production — commercial export limited. Importers: Pacific Botanicals (Pacific NW), Bula Kava House (Portland, OR)",
  "historical_context": "Samoa's ava ceremony is documented in the earliest European accounts of Polynesia. The Rev. John Williams (London Missionary Society) documented it in the 1830s with a mixture of admiration for its order and anxiety about its social role. The ceremony survived Christianisation better than in some other island groups because it was embedded in the authority structure that missionaries needed to work through.",
  "authority_tier": 1,
  "source_text": "Mageo, J.M. — Spirit Girls and Marines: Possession and Ethnopsychiatry as Historical Discourse in Samoa (American Ethnologist, 1996)",
  "slug": "samoa-ava"
},

# ============================================================
# PHILIPPINES — SPIRITS (Lambanog / Tuba / Basi)
# ============================================================
{
  "name": "Quezon Province — Lambanog",
  "country": "Philippines",
  "beverage_family": "spirits",
  "designation_type": "Regional Spirit Origin",
  "designation_name": "Philippine Coconut Spirits",
  "regulatory_framework": json.dumps({"body": "Bureau of Internal Revenue Philippines", "notes": "Lambanog regulated as distilled spirits; home production widespread in provinces"}),
  "terroir_profile": json.dumps({"source": "Cocos nucifera sap (tubâ)", "distillation": "traditional copper pot stills", "abv_range": "40-45% (80-90 proof)", "terroir_note": "Coconut palm variety and soil composition affect sap sweetness"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "respected",
  "description": "Quezon Province on Luzon is the heartland of lambanog production — coconut vodka distilled from fermented coconut sap (tubâ). The mangangarit (coconut tapper) climbs the palm twice daily to collect fresh sap, which begins fermenting immediately upon collection. The mananguete (distiller) then double-distils the fermented tubâ in copper pot stills. Traditional lambanog is clear, slightly sweet, with a distinctive coconut character. Infused versions (pandan, fruits, flowers) have expanded the category.",
  "key_producers": "Lakan Lambanog (premium bottled, nationally distributed), Don Papa Rum (Negros — rum but same Austronesian tradition), RumX Philippines [NEEDS VERIFICATION]",
  "historical_context": "Lambanog production predates Spanish colonisation (1565). The Austronesian fermentation tradition — tapping coconut palms for sap across the Pacific and Southeast Asia — is one of humanity's oldest continuous beverage traditions. Spanish colonisers attempted to regulate and tax lambanog production from the 16th century. The distillation knowledge likely arrived with Chinese and Arab traders from the 13th-15th centuries.",
  "authority_tier": 2,
  "source_text": "Cariño, J. — Philippine Food, the Story Behind the Food (Anvil Publishing, 2007)",
  "slug": "quezon-lambanog"
},
{
  "name": "Ilocos Region — Basi",
  "country": "Philippines",
  "beverage_family": "spirits",
  "designation_type": "Regional Fermented Spirit",
  "designation_name": "Ilokano Sugarcane Wine",
  "regulatory_framework": json.dumps({"body": "National Commission for Culture and the Arts Philippines", "notes": "Basi Revolt of 1807 — Spanish monopoly sparked rebellion"}),
  "terroir_profile": json.dumps({"source": "Saccharum officinarum (sugarcane)", "additives": "Duhat (Java plum) bark, camias (bilimbi), anise", "ageing": "clay jar (burnay), months to years", "abv_range": "14-18%"}),
  "quality_trajectory": "rediscovering",
  "reputation_tier": "respected",
  "description": "Basi is the traditional sugarcane wine of the Ilocos region in Northern Luzon — fermented sugarcane juice aged in burnay clay jars with additions of duhat bark, camias, anise, and other local botanicals. It is red-brown, tannic, somewhat acidic, and deeply aromatic. The Basi Revolt of 1807, when the Spanish Crown monopolised basi production, is one of the key events in Philippine colonial history — demonstrating how deeply embedded this beverage was in Ilokano cultural identity.",
  "key_producers": "Basi Basi (Vigan-based traditional producer), Ilocos Norte craft producers [NEEDS VERIFICATION]",
  "historical_context": "Basi production is documented in Spanish colonial records from the 16th century. The 1807 Basi Revolt — a rebellion against the Spanish monopoly on basi production — is depicted in the famous Vigan tapestry paintings now in the National Museum of the Philippines. Basi is a UNESCO Intangible Cultural Heritage candidate.",
  "authority_tier": 2,
  "source_text": "Scott, W.H. — Cracks in the Parchment Curtain (New Day Publishers, 1982)",
  "slug": "ilocos-basi"
},

# ============================================================
# WEST AFRICA — PALM WINE / SPIRITS
# ============================================================
{
  "name": "Nigeria — Palm Wine Belt",
  "country": "Nigeria",
  "beverage_family": "traditional",
  "designation_type": "Traditional Beverage Region",
  "designation_name": "West African Palm Wine Culture",
  "regulatory_framework": json.dumps({"body": "National Agency for Food and Drug Administration and Control (NAFDAC)", "notes": "Traditional production largely unregulated"}),
  "terroir_profile": json.dumps({"palm_species": ["Raphia hookeri (Raphia palm)", "Elaeis guineensis (Oil palm)"], "tapping_season": "year-round in south, wet season peak", "fermentation_time": "fresh (sweet) to 24 hours (slightly alcoholic) to 3 days (sour/vinegar)"}),
  "quality_trajectory": "established",
  "reputation_tier": "respected",
  "description": "Nigeria is the world's largest palm wine consuming nation. Two palm species are tapped: the Raphia palm (oguro in Yoruba, nkwu enu in Igbo) for its high-quality, white sap, and the Oil palm (emu in Yoruba, nkwu in Igbo) which produces a sweeter, less nuanced wine. Fresh-tapped palm wine (emu tuntun in Yoruba) is sweet, effervescent, yeasty — often sold at dawn by the calabash or gallon before significant fermentation occurs. The microbiology: Saccharomyces cerevisiae, Lactobacillus, Acetobacter — the same organisms as in European fermented beverages, performing the same transformations on a different plant sugar.",
  "key_producers": "Traditional village-level production. No major commercial brands — the beverage is specifically anti-commercial: it must be consumed fresh or it becomes palm vinegar. This is a feature, not a bug — it creates community through necessity.",
  "historical_context": "Palm wine predates recorded history in West Africa. It features in Chinua Achebe's 'Things Fall Apart' (1958) as a social and ceremonial touchstone. The connection to Caribbean rum: enslaved Africans brought to the Caribbean from palm wine cultures understood fermentation of plant sugars, which was applied to sugarcane in the New World. The knowledge of fermentation crossed the Atlantic even when the trees did not.",
  "authority_tier": 1,
  "source_text": "Achebe, C. — Things Fall Apart (Heinemann, 1958); Ezeagu, I.E. et al. — Biochemical composition of Nigerian palm wine (Bioresource Technology, 1998)",
  "slug": "nigeria-palm-wine"
},
{
  "name": "Cameroon — Matango",
  "country": "Cameroon",
  "beverage_family": "traditional",
  "designation_type": "Traditional Beverage Region",
  "designation_name": "Cameroonian Palm Wine (Matango)",
  "regulatory_framework": json.dumps({"body": "Ministry of Agriculture and Rural Development Cameroon", "notes": "Matango bars (informal) are primary distribution"}),
  "terroir_profile": json.dumps({"local_name": "matango or 'white stuff'", "palm_species": "Raphia vinifera (Raphia palm)", "typical_abv": "3-8% depending on fermentation time", "serving_vessel": "plastic/metal container or calabash"}),
  "quality_trajectory": "established",
  "reputation_tier": "respected",
  "description": "In Cameroon, palm wine is called matango — the informal name universally used across the country. 'White stuff' is the English-speaking Cameroon term. Matango bars (informal drinking establishments) are central to Cameroonian social life. The Raphia vinifera palm of central Africa produces a wine with a distinctive earthier, more complex character than West African oil palm wine. Matango is deeply integrated with music culture — the Cameroonian highlife and Afrobeat scenes emerged from the same social spaces.",
  "key_producers": "Village-level production. Cameroon Breweries (Guinness franchise) sells commercial beer in the same social spaces, but matango remains the traditional alternative.",
  "historical_context": "Matango production in Cameroon is pre-colonial. The forced labour policies of both German colonial rule (1884-1916) and subsequent French/British administration disrupted traditional agricultural patterns while intensifying palm wine production as a social coping mechanism. The matango tradition survived colonisation and continues as a living practice.",
  "authority_tier": 2,
  "source_text": "Ayernor, G.S. — Cassava and Palm Wine — Traditional Fermented Beverages of West Africa (FAO, 1981)",
  "slug": "cameroon-matango"
},
{
  "name": "Haiti — Clairin Tradition",
  "country": "Haiti",
  "beverage_family": "spirits",
  "designation_type": "Artisanal Spirit Region",
  "designation_name": "Haitian Clairin Artisanal Zone",
  "regulatory_framework": json.dumps({"body": "Institut de Sauvegarde du Patrimoine National (ISPAN)", "notes": "Largely unregulated — individual small distillers operate independently"}),
  "terroir_profile": json.dumps({"source": "local Haitian sugarcane varieties (not mass plantation varieties)", "fermentation": "wild indigenous yeast", "distillation": "copper alembic or column still depending on distiller", "abv_range": "43-55%", "terroir_note": "Each distiller's local cane variety and wild yeast create distinct terroir expression"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "respected",
  "description": "Clairin is Haiti's artisanal unaged cane spirit — the last truly terroir-driven rum tradition in the Caribbean. Unlike industrial rum, clairin is made by small-scale distillers (clairins artisanaux) using local sugarcane varieties, wild yeast fermentation, and traditional copper stills. Each producer's clairin is as distinct as a grower Champagne is from a blended Champagne — the terroir, the cane variety, and the indigenous yeast are all specific to that piece of land. Key producers include Sajous (St-Michel de l'Attalaye), Vaval (Cavaillon), Le Rocher (Baradères), and Casimir (Léogâne). Luca Gargano of Velier (Genoa) has been instrumental in bringing clairin to international markets since 2012.",
  "key_producers": "Sajous, Vaval, Le Rocher, Casimir, Sureau — all single-producer, single-village. International importer: Velier (Italy). North American: Proof & Company, Cognac One [NEEDS VERIFICATION for Canada]",
  "historical_context": "Haiti was the world's most profitable colony (Saint-Domingue) before the 1791 slave revolution — the only successful slave revolution in history, creating the first free Black republic (1804). Clairin production continued through revolution, the French indemnity imposed on Haiti (1825), the US occupation (1915-1934), the Duvalier era, and the 2010 earthquake. The spirit carries the history of resistance in every sip.",
  "authority_tier": 1,
  "source_text": "Gargano, L. — Clairin: The Last Genuine Rum (Velier, 2014); James, C.L.R. — The Black Jacobins (Secker and Warburg, 1938)",
  "slug": "haiti-clairin"
},

# ============================================================
# ETHIOPIA — COFFEE
# ============================================================
{
  "name": "Yirgacheffe",
  "country": "Ethiopia",
  "beverage_family": "coffee",
  "designation_type": "Geographical Indication",
  "designation_name": "Yirgacheffe GI (Ethiopia Commodity Exchange)",
  "regulatory_framework": json.dumps({"body": "Ethiopian Coffee and Tea Authority (ECTA)", "exchange": "Ethiopia Commodity Exchange (ECX)", "gi_registered": True}),
  "terroir_profile": json.dumps({"altitude_m": "1700-2200", "soil": "deep, red clay-loam", "annual_rainfall_mm": "1200-2000", "processing": "washed (primary), natural (some lots)", "variety": "Ethiopian heirloom (JARC and wild-collected varieties)", "flavour_signature": "floral (jasmine, bergamot), citrus (lemon, bergamot), tea-like body"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Yirgacheffe is the benchmark for washed Ethiopian coffee — arguably the most recognisable single origin in the world. Located within the Sidama Zone in southern Ethiopia at 1,700-2,200m, Yirgacheffe coffees produced by the washed process express an unmistakeable floral-citrus-tea profile that no other origin replicates. The jasmine and bergamot aromatics are produced by the combination of heirloom variety genetics, altitude-driven slow cherry development, and clean washed processing that preserves fruit clarity. Key washing stations: Kochere, Konga, Aricha, Gedeb.",
  "key_producers": "Yirgacheffe Coffee Farmers Cooperative Union (YCFCU), Kochere Washing Station, Aricha Processing Station. International specialty roasters: Intelligentsia (direct trade), Counter Culture, George Howell, Onyx Coffee Lab. BC: 49th Parallel, Prototype Coffee, Dosiero Coffee",
  "historical_context": "Yirgacheffe sits at the southern edge of the Kaffa Forest region where Coffea arabica is indigenous. The washed processing method was introduced in the 1970s and transformed the region's global reputation. Ethiopia is the only country where coffee is truly indigenous — everywhere else on Earth, it was planted by humans. The trees in Ethiopia's forests are wild-growing descendants of the original species.",
  "authority_tier": 1,
  "source_text": "Weinberg, B. & Bealer, B. — The World of Caffeine (Routledge, 2001); Pendergrast, M. — Uncommon Grounds: The History of Coffee (Basic Books, 1999)",
  "slug": "yirgacheffe"
},
{
  "name": "Sidama",
  "country": "Ethiopia",
  "beverage_family": "coffee",
  "designation_type": "Geographical Indication",
  "designation_name": "Sidama GI (Ethiopia Commodity Exchange)",
  "regulatory_framework": json.dumps({"body": "Ethiopian Coffee and Tea Authority (ECTA)", "notes": "Sidama now has its own regional state (2020) — coffee is economic foundation", "gi_registered": True}),
  "terroir_profile": json.dumps({"altitude_m": "1400-2200", "soil": "black to red clay loam", "processing": "both washed and natural", "variety": "Ethiopian heirloom", "subregions": ["Aleta Wondo", "Bona Zuria", "Dale", "Arbegona"], "natural_flavour_signature": "blueberry, strawberry, tropical fruit, winey ferment"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "Sidama is the broader administrative region that encompasses Yirgacheffe as a microregion. Natural-processed Sidama coffees — the so-called 'blueberry bomb' — have become among the most sought-after in specialty coffee. In natural processing, the whole cherry dries on raised beds for 3-6 weeks, allowing the fruit sugars to ferment into the seed, creating intensely fruity, wine-like profiles. The contrast between washed Yirgacheffe (clean, floral, tea-like) and natural Sidama (fruit-forward, winey, full-body) demonstrates how processing method shapes flavour as powerfully as variety and terroir.",
  "key_producers": "Sidama Coffee Farmers Cooperative Union (SCFCU), Bensa Washing Station, Aleta Wondo Co-op. International: Heart Coffee Roasters, Stumptown (natural lot selections), Hario V60 competition lots",
  "historical_context": "Sidama region became Ethiopia's 10th regional state in 2020 following a regional referendum — coffee export revenue was central to the economic case for statehood. The region's 700,000+ smallholder coffee farmers produce on plots of 0.5-2 hectares each, typically intercropped with enset (false banana), shade trees, and food crops.",
  "authority_tier": 1,
  "source_text": "Scholze, I. — The Atlas of Coffee (Pavilion Books, 2020); Ethiopia Commodity Exchange documentation",
  "slug": "sidama"
},
{
  "name": "Harrar",
  "country": "Ethiopia",
  "beverage_family": "coffee",
  "designation_type": "Geographical Indication",
  "designation_name": "Harrar GI",
  "regulatory_framework": json.dumps({"body": "Ethiopian Coffee and Tea Authority (ECTA)", "notes": "Harrar is the oldest continuously-traded Ethiopian coffee export"}),
  "terroir_profile": json.dumps({"altitude_m": "1400-2000", "soil": "red clay", "processing": "natural/dry process exclusively", "climate": "semi-arid highland", "variety": "Harrar long-berry and short-berry heirloom varieties", "flavour_signature": "mocha, dark chocolate, blueberry, winey, gamey, wild"}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "Harrar (also spelled Harar) is Eastern Ethiopia's ancient walled city and the oldest continuously-traded Ethiopian coffee export. All Harrar coffee is naturally processed — dried in whole cherry form on elevated drying beds or ground surfaces in the dry highland climate. The result is among the most complex and polarising coffees in the world: intense blueberry and mocha character, a distinctive gamey/winey quality from the natural fermentation, and a full, almost syrupy body. The 'mocha' flavour descriptor that appears throughout coffee vocabulary derives from the port of Mocha (Yemen) through which Ethiopian and Yemeni coffee was historically exported.",
  "key_producers": "Oromia Coffee Farmers Cooperative Union (OCFCU), Harrar Coffee Export Co. International specialty: Kaffa Coffee, Elixr Coffee Roasters, Caffe Vita. Note: Harrar beans are also used in traditional Ethiopian buna ceremony.",
  "historical_context": "Harrar has been a coffee trading city since at least the 15th century. The trade route from Harrar through the port of Berbera (Somaliland) to the Arabian Peninsula and onwards to Mocha (Yemen) established 'mocha' as a synonym for coffee in European languages. Rimbaud lived in Harrar from 1880-1891 as a coffee and arms trader — the connection between the poet and this coffee persists in Ethiopian cultural memory.",
  "authority_tier": 1,
  "source_text": "Wild, A. — Coffee: A Dark History (Norton, 2004); Cambrony, H. — La culture du caféier (Maisonneuve et Larose, 1992)",
  "slug": "harrar"
},

# ============================================================
# USA NEW WORLD WINE
# ============================================================
{
  "name": "Napa Valley",
  "country": "USA",
  "beverage_family": "wine",
  "designation_type": "AVA",
  "designation_name": "Napa Valley AVA (1981)",
  "regulatory_framework": json.dumps({"body": "TTB / Napa Valley Vintners", "key_rule": "100% of grapes must come from Napa Valley AVA for label use", "sub_avas": 16, "napa_ag_preserve": "1968 — first agricultural preserve in USA"}),
  "terroir_profile": json.dumps({"valley_length_km": 50, "climate_range": "Carneros (coolest, marine fog) to Calistoga (hottest, inland)", "soils": ["Alluvial fans", "Volcanic", "Benchland clay-loam"], "elevation_range_m": "0-2600 (Howell Mountain)", "primary_variety": "Cabernet Sauvignon", "valley_floor_vs_mountain": "Mountain AVAs produce more concentrated, age-worthy wines; valley floor more approachable"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Napa Valley is the world's most commercially successful wine region per acre of vineyard — 4% of California's wine production generates 25% of its revenue. Cabernet Sauvignon is the definitive grape, but the valley's 16 sub-AVAs produce vastly different expressions: Oakville and Rutherford (the classic 'Rutherford Dust' — chalky mid-palate texture from benchland soils), Stags Leap District (elegant, Bordeaux-inspired), Howell Mountain (tannic, mountain-structured), Spring Mountain (powerful, age-worthy), and Calistoga (the hottest, most powerful expression). The 1976 Judgment of Paris — where California wines including Stag's Leap Wine Cellars 1973 Cabernet defeated the first growths in blind tasting — established Napa's global reputation.",
  "key_producers": "Opus One (Mondavi/Rothschild), Screaming Eagle (cult — $3000+/bottle), Harlan Estate (cult), Dominus (Christian Moueix), Stag's Leap Wine Cellars (1976 Paris winner), Caymus, Jordan, Heitz, Beringer, Far Niente, Duckhorn, Shafer",
  "historical_context": "Napa Valley's wine history begins with George Yount (1843) and Charles Krug (1861). Prohibition (1920-1933) devastated the industry. The post-WWII era saw Robert Mondavi (founded 1966) establish the modern Napa model — quality-focused, internationally marketed California wine. The 1976 Judgment of Paris (organised by British wine merchant Steven Spurrier) was the watershed moment. The 2020 Glass Fire, 2017 Atlas Fire, and ongoing drought pose existential challenges to the region.",
  "authority_tier": 1,
  "source_text": "Taber, G.M. — Judgment of Paris (Scribner, 2005); Mondavi, R. — Harvests of Joy (Harcourt, 1998)",
  "slug": "napa-valley"
},
{
  "name": "Sonoma County",
  "country": "USA",
  "beverage_family": "wine",
  "designation_type": "AVA",
  "designation_name": "Sonoma County AVA (1983)",
  "regulatory_framework": json.dumps({"body": "TTB / Sonoma County Vintners", "sub_avas": 19, "size_vs_napa": "Sonoma is larger but less densely planted — more agricultural diversity"}),
  "terroir_profile": json.dumps({"russian_river_valley": "Cold, foggy, Pinot Noir and Chardonnay benchmark", "dry_creek_valley": "Warm, Zinfandel heartland — head-trained old vines", "alexander_valley": "Warm, Cabernet Sauvignon", "sonoma_coast": "Extended coast-influenced AVA — cool-climate Pinot and Chardonnay", "soils": "Extremely diverse — 60+ soil types across county"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Sonoma County is Napa's larger, more diverse neighbour — often compared to Burgundy (multiple distinct terroirs and varieties) versus Napa's Bordeaux (one dominant variety, one dominant style). The Russian River Valley produces California's benchmark Pinot Noir and Chardonnay — the Goldridge sandy loam and the persistent morning fog from the Pacific create an extended growing season that produces wines of elegance rarely achieved elsewhere in California. Dry Creek Valley's old-vine Zinfandel (some vines 120+ years old) is a unique American wine identity. The Sonoma Coast's extended boundaries were contested but now produce the state's most exciting cool-climate expressions.",
  "key_producers": "Williams Selyem (Russian River Pinot — benchmark), Kistler (Chardonnay), Flowers (Sonoma Coast), Ridge Monte Bello and Lytton Springs (Dry Creek Zinfandel), Rochioli, Littorai, Wind Gap, DuMOL, Gary Farrell",
  "historical_context": "Sonoma predates Napa in wine history — Count Agoston Haraszthy planted Buena Vista Winery in 1857, considered California's first premium winery. The county's diversity made it harder to brand than Napa but also more resilient — when Cabernet fell out of fashion, Sonoma had Pinot Noir, Chardonnay, Zinfandel, and Syrah to showcase.",
  "authority_tier": 1,
  "source_text": "Laube, J. — California Wine (Wine Spectator Press, 1995); Sullivan, C.L. — Zinfandel: A History of a Grape and Its Wine (University of California Press, 2003)",
  "slug": "sonoma-county"
},
{
  "name": "Kentucky Bourbon Country",
  "country": "USA",
  "beverage_family": "spirits",
  "designation_type": "Geographic Spirit Region",
  "designation_name": "Kentucky Bourbon Trail",
  "regulatory_framework": json.dumps({"body": "Alcohol and Tobacco Tax and Trade Bureau (TTB)", "bourbon_requirements": {"corn_minimum_pct": 51, "new_charred_oak": True, "distillation_abv_max": 80, "barrel_entry_abv_max": 62.5, "bottling_abv_min": 40}, "straight_bourbon": "min 2 years ageing", "kentucky_bourbon": "must be aged in KY"}),
  "terroir_profile": json.dumps({"limestone_water": "Naturally filters out iron (turns whiskey black), high calcium content — ideal for yeast fermentation", "climate": "Four distinct seasons — winter cold halts ageing, summer heat expands barrel, creating the pumping action", "rickhouses": "Multi-story ageing warehouses — upper floors hotter, produce more intense bourbon", "key_counties": ["Bourbon County (historical namesake)", "Woodford County (Woodford Reserve)", "Nelson County (Jim Beam/Maker's Mark)", "Anderson County (Four Roses)"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Kentucky produces 95% of the world's bourbon. The state's limestone-filtered water, distinct four-season climate, and century-old rickhouse tradition create conditions that cannot be replicated elsewhere — even though bourbon can legally be made anywhere in the USA. The combination of corn sweetness, rye spice (in high-rye mash bills), charred oak vanilla and caramel, and the Kentucky weather cycle creates the world's most distinctive national spirit category. And behind that identity is a history that includes the contributions of enslaved Black Americans — particularly Nearest Green, whose whiskey-making knowledge built what became the Jack Daniel's Distillery.",
  "key_producers": "Buffalo Trace (Pappy Van Winkle, Eagle Rare, Blanton's, Stagg), Maker's Mark, Woodford Reserve, Four Roses, Wild Turkey (Jimmy Russell legacy), Heaven Hill (Elijah Craig, Larceny), Jim Beam, Uncle Nearest Premium Whiskey (Shelbyville, TN — Nearest Green's legacy)",
  "historical_context": "Bourbon County, Kentucky — named for the French royal family in gratitude for Revolutionary War support — gave the spirit its name, though it is now produced across many Kentucky counties. The Whiskey Rebellion (1794) established federal taxation of distilled spirits. The 19th century saw bourbon develop its distinctive charred oak character. Prohibition (1920-1933) created the 'medicinal whiskey' exception that kept six Kentucky distilleries operational. The 21st-century bourbon boom has created allocation scarcity and a secondary market.",
  "authority_tier": 1,
  "source_text": "Risen, C. — American Whiskey, Bourbon, and Rye (Sterling Epicure, 2013); Cecil, S. — The Bourbon King (Lyons Press, 2022)",
  "slug": "kentucky-bourbon-country"
},
{
  "name": "Tennessee Whiskey Region",
  "country": "USA",
  "beverage_family": "spirits",
  "designation_type": "Geographic Spirit Region",
  "designation_name": "Tennessee Whiskey (Lincoln County Process)",
  "regulatory_framework": json.dumps({"body": "TTB + Tennessee State Law (2013)", "lincoln_county_process": "Mandatory charcoal mellowing (maple charcoal) before barrel ageing distinguishes Tennessee Whiskey from Bourbon legally", "key_counties": ["Moore County (Jack Daniel's)", "Coffee County (George Dickel)"]}),
  "terroir_profile": json.dumps({"cave_spring_hollow": "Jack Daniel's limestone cave spring — mineral-rich, iron-free water", "maple_charcoal_mellowing": "Up to 10 days filtering through 10 feet of maple charcoal — removes fusel oils, softens spirit before barrelling"}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "Tennessee Whiskey is legally distinct from Bourbon by the Lincoln County Process — mandatory filtration of new-make spirit through maple charcoal before barrelling. The process was pioneered at what became Jack Daniel's Distillery in Lynchburg, Moore County, where the whiskey-making knowledge was held by Nearest Green, an enslaved man who taught Jack Daniel the craft. This history was suppressed for 150 years and only restored to public knowledge through the Uncle Nearest Premium Whiskey brand (founded 2017 by Fawn Weaver) and subsequent historical research.",
  "key_producers": "Jack Daniel's (world's best-selling American whiskey — now owned by Brown-Forman), Uncle Nearest Premium Whiskey (Shelbyville — Nearest Green's direct legacy), George Dickel (Cascade Hollow, Tullahoma), Nelson's Green Brier (Civil War-era distillery revived by the Nelson brothers)",
  "historical_context": "Nearest Green: an enslaved man owned by Dan Call, a preacher who operated a distillery in Moore County, Tennessee. Green taught the craft of distilling to Jasper Newton 'Jack' Daniel, who later purchased the distillery and founded what became the world's most famous whiskey brand. Green's contribution was unknown publicly until Fawn Weaver, researching Nearest Green's great-great-granddaughter's family history, discovered historical records and founded Uncle Nearest Premium Whiskey in 2016-17.",
  "authority_tier": 1,
  "source_text": "Weaver, F. — Love & Whiskey: The Remarkable True Story of Jack Daniel, His Master Distiller Nearest Green (2020); Risen, C. — American Whiskey, Bourbon, and Rye (Sterling Epicure, 2013)",
  "slug": "tennessee-whiskey-region"
},

# ============================================================
# AUSTRALIA
# ============================================================
{
  "name": "Barossa Valley",
  "country": "Australia",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Barossa Valley GI (Australian GI system)",
  "regulatory_framework": json.dumps({"body": "Wine Australia / Barossa Grape and Wine Association", "old_vine_charter": {"ancient_vine_60+": True, "old_vine_35+": True, "survivor_vine_70+": True, "centennial_vine_100+": True}}),
  "terroir_profile": json.dumps({"soils": ["Eden Valley — high-altitude sandy loam over clay", "Barossa Valley floor — alluvial, clay-loam, some silt"], "climate": "warm continental, dry summers", "rainfall_mm_annual": 350, "altitude_m": {"valley_floor": "270-350", "eden_valley": "400-600"}, "pre_phylloxera_vines": "Yes — some blocks planted 1843-1880, survived because phylloxera never reached South Australia"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "The Barossa Valley holds one of the most extraordinary viticultural assets in the world: pre-phylloxera Shiraz vines, some planted as early as 1843, now 150-180+ years old. South Australia was never reached by the phylloxera louse that destroyed European vineyards in the 1860s-1880s, meaning these vines grow on their own roots (ungrafted) — producing ultra-low yields of intensely concentrated fruit. The Barossa Grounds initiative has identified seven distinct terroir zones within the valley. Penfolds Grange, Australia's most collectable wine, is built primarily on old-vine Barossa Shiraz.",
  "key_producers": "Penfolds (Grange, Bin 707, RWT), Henschke (Hill of Grace — single vineyard, 150-year-old vines), Torbreck (RunRig, The Factor), Two Hands (Brave Faces, Lily's Garden), Langmeil (Freedom 1843 — oldest certified Shiraz vines), Yalumba, Peter Lehmann, St. Hallett (Old Block Shiraz), Seppeltsfield (100-year-old Tawny program)",
  "historical_context": "The Barossa was settled by Silesian Lutheran refugees fleeing religious persecution in Prussia in the 1840s — a fact that explains both the Lutheran churches that still dot the landscape and the cultural seriousness with which Barossa families have maintained their vine heritage across five generations. The community's collective decision never to replant with grafted vines (even when it would have been financially rational) is one of viticulture's defining acts of cultural preservation.",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006); Iland, P. — The Australian Wine Research Institute Technical Review",
  "slug": "barossa-valley"
},
{
  "name": "McLaren Vale",
  "country": "Australia",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "McLaren Vale GI",
  "regulatory_framework": json.dumps({"body": "Wine Australia / McLaren Vale Grape Wine and Tourism Association", "sustainable_winegrowing": "McLaren Vale Sustainable Winegrowing Australia program"}),
  "terroir_profile": json.dumps({"soils": ["Terra rossa over limestone", "Sandy soils near coast", "Black cracking clay"], "climate": "Mediterranean — warm days, cool nights, maritime influence from Gulf St. Vincent", "altitude_m": "50-300", "primary_varieties": ["Shiraz", "Grenache", "Cabernet Sauvignon", "Fiano", "Nero d'Avola"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "McLaren Vale sits just 40km south of Adelaide in South Australia, where the Mount Lofty Ranges meet the Gulf St. Vincent. The Mediterranean climate — warm, dry summers moderated by afternoon sea breezes and cool nights — creates conditions that are genuinely analogous to the southern Rhône or Sardinia. McLaren Vale's Shiraz tends toward dark chocolate and mocha character rather than the Barossa's more restrained approach, while Grenache from old vine material here is gaining a world reputation. The Southern Fleurieu blends are emerging as a distinct voice in Australian wine.",
  "key_producers": "Clarendon Hills (old-vine Grenache, Syrah — benchmark), Wirra Wirra, d'Arenberg (Chester Osborn — the iconoclast), Coriole, Hardys (historic), Yangarra Estate (biodynamic GSM), Chapel Hill, Fox Creek",
  "historical_context": "McLaren Vale's wine history begins with John Reynell (1838) and Thomas Hardy (1853) — Hardy's Tintara is the oldest continuously operating winery in South Australia. The region's proximity to Adelaide made it the wine capital of Australia before the Barossa's emergence as the premium destination. Today McLaren Vale's urban fringe is under constant development pressure — a challenge the wine community is actively resisting.",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006)",
  "slug": "mclaren-vale"
},
{
  "name": "Yarra Valley",
  "country": "Australia",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Yarra Valley GI",
  "regulatory_framework": json.dumps({"body": "Wine Australia", "notes": "Victoria's oldest wine region (1838)"}),
  "terroir_profile": json.dumps({"climate": "Cool continental — eastern ranges block maritime influence; significant temperature variation", "altitude_m": "50-400", "soils": ["Lower Yarra — grey sandy loam over clay", "Upper Yarra — red volcanic loam"], "primary_varieties": ["Pinot Noir", "Chardonnay", "Cabernet Sauvignon", "Syrah (Upper Yarra)"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "The Yarra Valley represents Australia's most credible Burgundian aspiration — cool-climate Pinot Noir and Chardonnay from volcanic soils in the ranges east of Melbourne. The distinction between Lower Yarra (warmer, richer, better for Cabernet) and Upper Yarra (cooler, more aromatic, better for Pinot and cool-climate Syrah) is as meaningful as any sub-regional division in Australia. Giants Steps and De Bortoli (Noble One botrytis Semillon) established the premium category, while newer producers like Toolangi and Levantine Hill push further quality boundaries.",
  "key_producers": "Giant Steps (Phil Sexton — benchmark Pinot and Chardonnay), De Bortoli (Noble One — iconic botrytis dessert wine; also premium Yarra range), Yering Station (historic, now premium), Oakridge (Dave Bicknell — progressive winemaking), Punt Road, Mac Forbes (terroir focus), Levantine Hill",
  "historical_context": "The Yarra Valley's first vines were planted in 1838 by the Ryrie brothers at Yering Station — the oldest wine region in Victoria. The industry collapsed during the Depression and was revived from the 1960s. Melbourne's proximity (45 minutes) has made the Yarra a tourism and cellar-door destination, which has enabled a premium pricing model that supports quality investment.",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006)",
  "slug": "yarra-valley"
},

# ============================================================
# NEW ZEALAND
# ============================================================
{
  "name": "Marlborough",
  "country": "New Zealand",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Marlborough GI",
  "regulatory_framework": json.dumps({"body": "New Zealand Winegrowers", "marlborough_wine": "Must use only Marlborough grapes for label", "sub_regions": ["Wairau Valley", "Awatere Valley", "Southern Valleys"]}),
  "terroir_profile": json.dumps({"climate": "Cool maritime — high sunshine hours, long cool growing season, significant diurnal range", "soils": {"wairau_valley": "Alluvial gravel (free-draining, deep)", "awatere_valley": "Clayey loam, more exposed, colder — higher acidity in wines", "southern_valleys": "Variable clay and loam"}, "pyrazine_character": "Methoxypyrazines — the green/herbaceous/capsicum compounds — are a feature of cool-climate Sauvignon Blanc; Marlborough's UV light and temperature regime maximise pyrazine expression", "primary_variety": "Sauvignon Blanc (85% of planting)"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Marlborough Sauvignon Blanc has defined a global style category. The pungent, herbaceous, passion-fruit and capsicum character — driven by methoxypyrazines and thiols — was unknown in the world wine lexicon until Cloudy Bay's inaugural 1985 vintage arrived in London. Within five years, New Zealand Sauvignon Blanc had become one of the defining trends in wine retail. The Wairau Valley produces the classic Marlborough style; the Awatere Valley (cooler, more exposed) produces leaner, more mineral expressions with higher acidity; the Southern Valleys produce riper, rounder styles.",
  "key_producers": "Cloudy Bay (the founder — now LVMH), Dog Point (founders of Cloudy Bay who departed to make their own wine), Greywacke (Kevin Judd — Cloudy Bay's original winemaker), Seresin (biodynamic), Fromm (Alsace-trained — Pinot Noir and late harvest specialties), Auntsfield, Spy Valley",
  "historical_context": "Marlborough's first commercial vineyard was planted by Montana Wines in 1973 in the Wairau Valley. The region's wine industry is 50 years old — extraordinarily young in wine terms — yet has achieved global icon status in that time. The story of how Kevin Judd and David Hohnen created Cloudy Bay and marketed it to London restaurants through Simon Loftus at Adnams is a marketing case study. Personal note: New Zealand's wine industry has a strong connection to professional kitchen culture — Wellington's food scene shaped my understanding of how wine integrates with food service.",
  "authority_tier": 1,
  "source_text": "Cooper, M. — Wine Atlas of New Zealand (Hodder Moa, 2008); Judd, K. — Pinot Noir: A New Zealand Odyssey (Random House NZ, 2008)",
  "slug": "marlborough"
},
{
  "name": "Central Otago",
  "country": "New Zealand",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Central Otago GI",
  "regulatory_framework": json.dumps({"body": "New Zealand Winegrowers / Central Otago Winegrowers Association", "sub_regions": ["Bannockburn", "Cromwell Basin", "Gibbston Valley", "Wanaka", "Alexandra"]}),
  "terroir_profile": json.dumps({"latitude": "45°S — world's southernmost commercial wine region", "climate": "Continental (NOT maritime) — extreme diurnal range (up to 20°C day/night differential), hot dry summers, cold winters with frost", "soils": "Schist — friable, grey-gold decomposed schist and loess over schist bedrock", "altitude_m": "200-450", "primary_variety": "Pinot Noir", "schist_character": "Mineral, fine-grained tannins, spice"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "Central Otago is among the most dramatic wine regions on Earth — high altitude continental viticulture on schist soils at 45° south latitude, beneath snow-capped mountains. The extreme diurnal temperature variation (hot days building phenolic ripeness, cold nights preserving acidity and aromatics) and the schist soils create a Pinot Noir of remarkable depth and distinctiveness: dark cherry, spice, mineral, and a fine-grained tannin structure that is unique to the region. Felton Road, Rippon, and Mt Difficulty have established that Central Otago Pinot Noir can age for 10-20 years and improve significantly.",
  "key_producers": "Felton Road (Bannockburn — biodynamic, benchmark), Rippon (Wanaka — lake-front old vines, biodynamic), Mt Difficulty (Bannockburn — range from accessible to serious), Peregrine (Gibbston), Two Paddocks (Sam Neill's vineyard — Gibbston), Carrick (Bannockburn), Amisfield",
  "historical_context": "Gold was discovered in the Clutha River at Dunstan (now Clyde) in 1862, creating one of the southern hemisphere's great gold rushes. When the gold was gone, the Chinese market gardens that fed the miners grew fruit — including early experimental wine grapes. Modern viticulture began in 1987 when Rippon planted the first serious post-war vineyard. The region's growth from zero to 2,000+ hectares in 35 years is extraordinary. My knowledge of this region comes from time spent in New Zealand — the schist landscape is unforgettable.",
  "authority_tier": 1,
  "source_text": "Cooper, M. — Wine Atlas of New Zealand (Hodder Moa, 2008); Central Otago Winegrowers Association documentation",
  "slug": "central-otago"
},
{
  "name": "Hawke's Bay",
  "country": "New Zealand",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Hawke's Bay GI",
  "regulatory_framework": json.dumps({"body": "New Zealand Winegrowers / Hawke's Bay Winegrowers", "gimblett_gravels": "Defined subregion — must meet strict soil criteria"}),
  "terroir_profile": json.dumps({"climate": "Warm maritime — NZ's sunniest wine region", "gimblett_gravels_soils": "Ancient river bed — free-draining, heat-retaining gravels produce full ripeness in red varieties", "primary_varieties": ["Cabernet Sauvignon", "Merlot", "Syrah", "Chardonnay", "Viognier"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "respected",
  "description": "Hawke's Bay on the North Island's east coast is New Zealand's second-largest wine region and its Bordeaux — warm, sunny conditions suit red Bordeaux varieties and Syrah. The Gimblett Gravels subregion (ancient Ngaruroro River bed) is NZ's most defined premium terroir for reds: free-draining gravels retain heat and produce Cabernet, Merlot, and Syrah with concentration and structure rarely achieved elsewhere in NZ.",
  "key_producers": "Craggy Range (Te Kahu, Quarry — benchmark Gimblett Gravels), Trinity Hill (The Gimblett — Syrah), Elephant Hill (beach estate), Villa Maria, Te Mata (Coleraine — NZ's most collectable red)",
  "historical_context": "Hawke's Bay's Mission Estate Winery (established 1851 by Marist Brothers) is New Zealand's oldest winery. The Gimblett Gravels district was almost lost to sand and gravel extraction in the 1980s — the winegrowing community's successful campaign to protect the land is a conservation milestone.",
  "authority_tier": 2,
  "source_text": "Cooper, M. — Wine Atlas of New Zealand (Hodder Moa, 2008)",
  "slug": "hawkes-bay"
},

# ============================================================
# ARGENTINA
# ============================================================
{
  "name": "Mendoza",
  "country": "Argentina",
  "beverage_family": "wine",
  "designation_type": "GI",
  "designation_name": "Mendoza GI / Denominación de Origen Controlada",
  "regulatory_framework": json.dumps({"body": "Instituto Nacional de Vitivinicultura (INV)", "sub_regions": ["Luján de Cuyo (DOC — first sub-DOC in Argentina)", "Uco Valley", "Maipú", "Valle de Uco sub-zones: Gualtallary, Los Árboles, Altamira, Vista Flores"]}),
  "terroir_profile": json.dumps({"altitude_m": "800-1500 (highest viticulture zone in the world)", "climate": "High-altitude desert continental — extreme UV, low humidity, diurnal range 20°C", "irrigation": "Meltwater from Andes (flood irrigation via acequia channels, increasingly drip)", "soils": {"lujan_de_cuyo": "Alluvial, gravelly, excellent drainage", "uco_valley": "Variable — limestone (Gualtallary), alluvial clay (Altamira)", "gualtallary_altitude": "1200-1500m — produces structured, elegant Malbec and Cabernet Franc"}, "primary_variety": "Malbec (Côt — originally from Bordeaux, thrives at altitude)"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Mendoza accounts for 75% of Argentina's wine production and produces the world's finest Malbec — a grape largely abandoned in its native Bordeaux that found its second identity at altitude. The altitude-UV-diurnal range combination creates a physiological phenomenon: thick grape skins (UV protection) = higher anthocyanins and polyphenols = deeper colour and more complex tannin. The Uco Valley's Gualtallary subzone at 1,200-1,500m has emerged as Argentina's most exciting wine address — Zuccardi's Valle Suizo, Clos de los Siete, and Cheval des Andes are produced here.",
  "key_producers": "Catena Zapata (Adrianna Vineyard at 1,500m — benchmark), Achaval-Ferrer (old vine Malbec, single parcels), Zuccardi (Valle Suizo, Julia — exceptional), Clos de los Siete (Michel Rolland collaboration), Cheval des Andes (Cheval Blanc/Terrazas joint venture), Viña Cobos (Paul Hobbs), Terrazas de los Andes, Trapiche (Iscay), Rutini (Trumpeter)",
  "historical_context": "Malbec vines were brought to Argentina in 1853 by French agronomist Michel Pouget, sent by the Argentine government to plant European varieties in Mendoza's agricultural colonies. The grape that was failing in Bordeaux due to coulure (poor fruit set) thrived at altitude. Argentina's wine industry modernised rapidly after the economic crisis of 2001 forced producers to focus on export quality. Nicolás Catena Zapata — studied at UC Berkeley, inspired by Napa — is widely credited with engineering the quality revolution.",
  "authority_tier": 1,
  "source_text": "Mujica Lainez, M. — Historia del vino argentino (Planeta, 2005); Clarke, O. — New World of Wine (Pavilion, 1999)",
  "slug": "mendoza"
},

# ============================================================
# CHILE
# ============================================================
{
  "name": "Colchagua Valley",
  "country": "Chile",
  "beverage_family": "wine",
  "designation_type": "DO",
  "designation_name": "Valle de Colchagua DO",
  "regulatory_framework": json.dumps({"body": "Servicio Agrícola y Ganadero (SAG)", "notes": "Part of the Valle Central macroregion; sub-zones include Marchigüe, Palmilla, Peralillo"}),
  "terroir_profile": json.dumps({"climate": "Mediterranean — warm, dry summers; pacific coastal influence in western zones", "soils": "Clay loam over gravel, some alluvial, decomposed granite in higher zones", "primary_varieties": ["Carmenère", "Cabernet Sauvignon", "Merlot", "Syrah", "Malbec"], "altitude_m": "200-500"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "Colchagua Valley is Chile's most celebrated red wine region — the concentration of quality-focused producers and the warmth of the valley floor create deep, full-bodied Carmenère, Cabernet, and Syrah with a distinctive chocolatey-herbal character. Casa Lapostolle's Clos Apalta (Parker's 100-point wine, the first 100 given to a South American wine) put Colchagua on the global map. The valley's high-altitude coastal sub-zones (Marchigüe) are producing the most exciting new styles.",
  "key_producers": "Casa Lapostolle (Clos Apalta), Montes (Folly — Syrah, Alpha M), Viu Manent (El Incienso), MontGras, Clos de Apalta, Hacienda Araucano, Laura Hartwig",
  "historical_context": "Colchagua's wine identity was built largely in the 1990s and 2000s when European investment (French, Spanish, Californian) arrived to exploit the combination of favourable climate, affordable land, and Chile's phylloxera-free status. The rediscovery of Carmenère in 1994 — when French ampelographer Jean-Michel Boursiquot identified the variety long thought to be Merlot — gave Chile a uniquely national variety.",
  "authority_tier": 1,
  "source_text": "Millon, M. — Wine Roads of Chile (Mitchell Beazley, 2001)",
  "slug": "colchagua-valley"
},
{
  "name": "Maipo Valley",
  "country": "Chile",
  "beverage_family": "wine",
  "designation_type": "DO",
  "designation_name": "Valle de Maipo DO",
  "regulatory_framework": json.dumps({"body": "SAG Chile", "sub_zones": ["Alto Maipo (Puente Alto, Pirque)", "Central Maipo", "Pacific Maipo (Isla de Maipo)"]}),
  "terroir_profile": json.dumps({"climate": "Mediterranean, moderated by Andes altitude", "soils": {"alto_maipo": "Alluvial gravel over bedrock — excellent drainage and heat retention", "notes": "Andes proximity = cold nights = preserved acidity in Cabernet"}, "altitude_m": "400-650", "primary_variety": "Cabernet Sauvignon"}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "Maipo Valley, immediately south of Santiago, is Chile's most historically prestigious wine region and the heartland of Chilean Cabernet Sauvignon. The Alto Maipo subzone — where the Andes rise sharply and Andean meltwater provides irrigation — produces Chile's most age-worthy Cabernets. Concha y Toro's Don Melchor and Almaviva (joint venture with Mouton Rothschild) are the benchmark expressions: structured, mineral, cedar-spiced, with a distinctively Andean freshness.",
  "key_producers": "Concha y Toro (Don Melchor, Almaviva), Errázuriz (Don Maximiano Founder's Reserve), Viña Aquitania (Sol de Sol — Alto Maipo), Perez Cruz (Cot — Malbec), Haras de Pirque, Santa Rita (Casa Real)",
  "historical_context": "Maipo was the first region to achieve premium status in Chile — Concha y Toro was founded in 1883 and has been the country's most important wine company for over a century. The 1995 Almaviva partnership with Baron Philippe de Rothschild validated Chilean Cabernet's place at the top of the global quality hierarchy.",
  "authority_tier": 1,
  "source_text": "Clarke, O. — New World of Wine (Pavilion, 1999)",
  "slug": "maipo-valley"
},

# ============================================================
# SOUTH AFRICA
# ============================================================
{
  "name": "Stellenbosch",
  "country": "South Africa",
  "beverage_family": "wine",
  "designation_type": "WO",
  "designation_name": "Stellenbosch Wine of Origin",
  "regulatory_framework": json.dumps({"body": "Wine and Spirit Board of South Africa", "wo_system": "Wine of Origin certification — guarantees origin, variety, vintage", "sub_wards": ["Simonsberg-Stellenbosch", "Jonkershoek Valley", "Banghoek", "Bottelary", "Devon Valley", "Papegaaiberg"]}),
  "terroir_profile": json.dumps({"climate": "Mediterranean — warm, wet winters, dry summers; Atlantic influence from False Bay", "soils": {"simonsberg_granite": "Decomposed granite — produces structured, mineral Cabernet Sauvignon", "jonkershoek_schist": "Schist and clay — produces powerful, age-worthy Cabernet", "bottelary_clay": "Heavy clay — Chenin Blanc and Pinotage", "False_Bay_cooling": "Maritime fog and wind cool the valley's lower reaches"}, "primary_varieties": ["Cabernet Sauvignon", "Chenin Blanc", "Pinotage", "Syrah", "Merlot"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "Stellenbosch is the Cape's wine capital — the home of Stellenbosch University's oenology department, the greatest concentration of premium wineries, and the most established wine tourism infrastructure. Cabernet Sauvignon from the granitic Simonsberg Mountain foothills competes with the world's best. Chenin Blanc — locally called Steen — is South Africa's most planted variety and in the hands of top producers produces a range from crisp and mineral to complex and barrel-fermented. Pinotage (a crossing of Pinot Noir and Cinsault created at Stellenbosch in 1925) is a South African original that polarises opinion.",
  "key_producers": "Kanonkop (benchmark Pinotage and Paul Sauer Bordeaux blend), Meerlust (Rubicon — benchmark Cape Bordeaux blend), Warwick (Three Cape Ladies, Old Bush Vine Pinotage), Rust en Vrede (Estate — concentrated Cabernet), Delaire Graff (luxury — Banghoek ridge), Ken Forrester (Old Vine Chenin Blanc — benchmark), Tokara, Thelema",
  "historical_context": "Stellenbosch was established in 1679 by Simon van der Stel of the Dutch East India Company (VOC) — making it one of the oldest European settlements in sub-Saharan Africa. The wine industry was built on enslaved labour (VOC imported slaves from Madagascar, Mozambique, India, and Indonesia). South Africa's wine industry was isolated during the apartheid era (1948-1994) by international sanctions and only re-entered global markets fully after 1994. The post-apartheid transformation of land ownership in the wine industry remains incomplete and contested.",
  "authority_tier": 1,
  "source_text": "Hands, P. & Hughes, B. — Complete Guide to South African Wine (Struik, 2006); Du Plessis, J. — Pinotage: Behind the Legends of South Africa's Own Wine (Cheviot, 2009)",
  "slug": "stellenbosch"
},
{
  "name": "Swartland",
  "country": "South Africa",
  "beverage_family": "wine",
  "designation_type": "WO",
  "designation_name": "Swartland Wine of Origin",
  "regulatory_framework": json.dumps({"body": "Wine and Spirit Board of South Africa", "swartland_independent_producers": "SIP Charter — organic/biodynamic commitment, natural winemaking, old vine preservation", "notes": "Swartland Revolution (annual tasting) was the flagship event for the natural wine movement in South Africa"}),
  "terroir_profile": json.dumps({"climate": "Hot, dry, minimal rainfall — requires dry-farmed old-vine material", "soils": {"granite": "Paardeberg Mountain — granitic decomposed rock, old-vine Grenache and Cinsault", "schist_slate": "Malmesbury shale — iron-rich, dark — Syrah specialist soils", "clay": "Old bush-vine Chenin Blanc"}, "old_vine_material": "Much of Swartland's value is in ungrafted, pre-phylloxera, dry-farmed bush vine material planted 60-120 years ago", "primary_varieties": ["Chenin Blanc", "Grenache Noir", "Syrah", "Cinsault", "Mourvèdre"]}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "The Swartland revolution was one of the most significant wine movements of the 21st century — a group of young producers (Eben Sadie, Andrea Mullineux, Chris and Andrea Mullineux, Callie Louw, Adi Badenhorst) deliberately turned away from the international Cabernet-Merlot template in the late 2000s and rediscovered the extraordinary old vine material sitting in the hot Swartland plains: dry-farmed Chenin Blanc, old bush-vine Grenache, Cinsault, and Syrah planted by farmers who had no commercial ambition for them. The result was a generation of wines with genuinely distinctive Cape identity.",
  "key_producers": "Sadie Family Wines (Eben Sadie — The Sadie Family Columella and Palladius are South Africa's most collectable wines), Mullineux (Chris and Andrea — Syrah specialists, Kloof Street), Badenhorst Family (Adi Badenhorst — Secateurs Chenin), Lammershoek, Testalonga (Craig Hawkins — natural wine pioneer), David & Nadia Sadie (biodynamic Chenin)",
  "historical_context": "Swartland ('Black Land' — named for the dark native renosterveld shrubland) was historically a wheat and livestock farming region. Wine growers planted old bush vines in the mid-20th century primarily for bulk wine production. The natural wine revolution discovered this forgotten material and brought it international attention from approximately 2007. The Swartland Independent Producers charter (2010) formalised the movement's values.",
  "authority_tier": 1,
  "source_text": "Waldin, M. — Biodynamic Wines (Mitchell Beazley, 2004); Sadie, E. — Vineyard of Distinction (privately published, 2015)",
  "slug": "swartland"
},

# ============================================================
# SCOTLAND — WHISKY REGIONS
# ============================================================
{
  "name": "Speyside",
  "country": "Scotland",
  "beverage_family": "spirits",
  "designation_type": "Scotch Whisky Region",
  "designation_name": "Speyside Scotch Whisky Region",
  "regulatory_framework": json.dumps({"body": "Scotch Whisky Association (SWA) / Scotch Whisky Regulations 2009", "still_type": "Pot still mandatory for single malt", "maturation_minimum_years": 3, "cask_types": "Oak casks only — ex-bourbon (American oak), ex-sherry (European oak), ex-wine increasingly"}),
  "terroir_profile": json.dumps({"distillery_count": "Over 50 — highest concentration of distilleries on Earth", "river_spey": "Scotland's fastest-flowing river — historically used for transportation of barley and whisky", "water_source": "Spring water from Cairngorm Mountains — soft, slightly peaty", "climate": "Cold, maritime-influenced continental — cold winters accelerate extraction from wood during temperature swings", "style_profile": "Elegant, fruity, approachable — less peated than Islay or Highland"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Speyside contains more whisky distilleries than any other region on Earth — over 50 active distilleries along the River Spey and its tributaries in northeast Scotland. The Speyside style is characterised by elegance, fruit, and accessibility: apple, pear, honey, toffee, and vanilla from ex-bourbon casks; dried fruit, Christmas cake, and spice from ex-sherry. The region's iconic distilleries (Glenfiddich, Macallan, Balvenie, Glenlivet) produce the world's best-selling single malts. Craigellachie, Mortlach, and Aberlour represent the weightier, more savoury face of Speyside.",
  "key_producers": "Macallan (sherry-dominant — benchmark luxury single malt), Glenfiddich (world's best-selling single malt), Balvenie (multiple wood expressions), Glenlivet (first legally licensed distillery 1824), Aberlour, Craigellachie, Mortlach (the 'Beast of Dufftown' — heavy, meaty), GlenDronach (sherry-forward), BenRiach, Cardhu",
  "historical_context": "Speyside's concentration of distilleries reflects its geography: fast-flowing rivers for water, Highlands barley for malt, peat from the nearby Cairngorms, oak from the Baltic trade. The 1823 Excise Act (responding to widespread illicit distillation) legalised and regulated production, and Speyside became the centre of the legal industry. Glenfiddich, founded 1887, became the world's first heavily exported single malt when Grant's decided to bottle and ship it internationally in 1963.",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003); Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014)",
  "slug": "speyside"
},
{
  "name": "Islay",
  "country": "Scotland",
  "beverage_family": "spirits",
  "designation_type": "Scotch Whisky Region",
  "designation_name": "Islay Single Malt Region",
  "regulatory_framework": json.dumps({"body": "Scotch Whisky Association", "active_distilleries": 9, "peat_specification": "Islay peat is seaweed-influenced — distinct iodine/brine character versus Highland peat"}),
  "terroir_profile": json.dumps({"island_area_km2": 620, "climate": "Maritime — strong westerly winds, high rainfall, salt spray", "peat_character": "Seaweed, kelp, iodine — Islay peat from the coastal blanket bog includes decomposed marine material, giving the distinct medicinal/brine character", "coastline_effect": "Laphroaig and Ardbeg warehouses on the coast — waves spray the walls — the sea salt is part of the ageing environment", "water": "Soft, peaty springs and lochs"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Islay (pronounced 'Eye-lah') produces the world's most distinctive whisky style: heavily peated, iodine-infused, brine-lashed single malts that divide opinion more decisively than any other spirit category. The three classic 'Kildalton' distilleries on the south coast — Laphroaig, Ardbeg, Lagavulin — produce the paradigmatic Islay style: medicinal iodine, tar, sea salt, smoked fish, then sweetness underneath. Bruichladdich's Octomore is the most heavily peated whisky commercially produced (200+ PPM phenols). Kilchoman is the newest distillery (2005) and the first farm distillery on Islay in 125 years.",
  "key_producers": "Laphroaig (Royal Warrant — Prince Charles's favourite), Ardbeg (cult status — Committee Reserve, Uigeadail, Corryvreckan), Lagavulin (16-year — the benchmark accessible Islay expression), Bruichladdich (Octomore, Port Charlotte, The Classic Laddie — unpeated), Bowmore (oldest distillery on Islay — 1779), Bunnahabhain (least peated Islay), Caol Ila (largest volume on Islay — much goes to blends), Kilchoman (farm distillery — Machir Bay), Ardnahoe (newest — 2019)",
  "historical_context": "Islay was producing whisky before records were kept — the island's location on the west coast of Scotland, accessible by sea from Ireland, made it a nexus of the Gaelic world's whisky tradition. The island's eight traditional distilleries (now nine with Ardnahoe) were essential to the Scotch blended whisky industry — Caol Ila and Bunnahabhain provide the 'backbone' to many major blends. Islay was also a major centre of the illegal distillation trade before the 1823 Act.",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Islay: The Land and Its Whiskies (Canongate, 1997); Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014)",
  "slug": "islay"
},
{
  "name": "Highland",
  "country": "Scotland",
  "beverage_family": "spirits",
  "designation_type": "Scotch Whisky Region",
  "designation_name": "Highland Scotch Whisky Region",
  "regulatory_framework": json.dumps({"body": "Scotch Whisky Association", "notes": "Largest region geographically — encompasses all of Scotland north of a line between Dundee and Greenock (except Speyside and Islands which are considered separate)"}),
  "terroir_profile": json.dumps({"distillery_count": "30+ active", "sub_styles": {"northern_highland": "Robust, full-bodied, sometimes smoky (Balblair, Old Pulteney, Clynelish)", "eastern_highland": "Lighter, fruity, elegant (Fettercairn, Glencadam)", "southern_highland": "Light, approachable (Glengoyne — no peat in production)", "perthshire": "Complex, varied (Blair Athol, Aberfeldy, Edradour)"}}),
  "quality_trajectory": "established",
  "reputation_tier": "prestigious",
  "description": "The Highland region is the largest and most internally diverse whisky region — spanning from Glenmorangie in the far north to Glengoyne south of the Highland Line, from the maritime Oban on the west coast to Old Pulteney in Caithness. The diversity defies a single style description. Key expressions: Glenmorangie 10-year (benchmark accessible Highland — honey, vanilla, citrus); Dalmore (sherry casks, chocolate, orange); Oban (maritime, gentle peat, fruit); Clynelish (waxy, honeyed coastal character); Edradour (Scotland's smallest distillery — sherry-bomb).",
  "key_producers": "Glenmorangie (Moët Hennessy — benchmark accessible premium, also Signet/18-year), Dalmore (Whyte and Mackay — sherry-dominant, range 12 to 60-year), Oban (Diageo — 14-year classic), Clynelish (coastal, waxy — legendary old vintage expressions), Balblair (Vintage expressions), Old Pulteney (maritime — 'the Maritime Malt'), Highland Park (Orkney — straddles Highland/Islands; peat + heather honey), Blair Athol, Aberfeldy, Edradour, Fettercairn",
  "historical_context": "The Highland region was the birthplace of the Scotch whisky tradition — distillation knowledge arrived from Ireland (via the Gaelic monastic network) to the Western Highlands. The Highland/Lowland distinction was originally a tax line: Highland whisky was taxed differently to encourage legal production. The 19th century saw the Highland style evolve into what we now recognise as single malt.",
  "authority_tier": 1,
  "source_text": "Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014); MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003)",
  "slug": "highland"
},
{
  "name": "Islay — Campbeltown",
  "country": "Scotland",
  "beverage_family": "spirits",
  "designation_type": "Scotch Whisky Region",
  "designation_name": "Campbeltown Scotch Whisky Region",
  "regulatory_framework": json.dumps({"body": "Scotch Whisky Association", "notes": "Recognised as a standalone region despite only 3 active distilleries — its historical importance warranted preservation of the designation", "active_distilleries": 3}),
  "terroir_profile": json.dumps({"location": "Kintyre Peninsula, Argyll", "historical_peak": "34 distilleries operating in late 19th century — the whisky capital of the world", "current_distilleries": ["Springbank", "Glengyle (Kilkerran)", "Glen Scotia"], "style": "Saline, briny, slightly smoky, distinctive damp cellar/old book character"}),
  "quality_trajectory": "rediscovering",
  "reputation_tier": "respected",
  "description": "Campbeltown at the tip of the Kintyre Peninsula once had 34 distilleries — at one point it was the whisky capital of the world, supplying Scotch to the United States and British Empire. Today only three remain. Springbank is the only distillery in Scotland that performs every production step — malting, mashing, fermenting, distilling, maturing, bottling — on site. Springbank's house style (a 2.5-times distillation creating a spirit between pot still weight and light column still character) is unlike any other Scotch.",
  "key_producers": "Springbank (benchmark — Campbeltown Loch 21-year, single cask expressions; also Longrow — heavily peated expression; Hazelburn — triple-distilled, unpeated), Glengyle (Kilkerran expression), Glen Scotia",
  "historical_context": "Campbeltown's decline from 34 distilleries to 2 (and near-zero) by the 1920s is a cautionary tale: overproduction, quality decline in the 1920s, Prohibition closing the US market, and economic depression combined to eliminate the industry. The fact that Springbank survived (owned continuously by the Mitchell family since 1828) and maintains its artisanal, on-site approach is one of Scotch whisky's great stories of integrity.",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003)",
  "slug": "campbeltown"
},

# ============================================================
# MEXICO — AGAVE SPIRITS
# ============================================================
{
  "name": "Oaxaca — Mezcal",
  "country": "Mexico",
  "beverage_family": "spirits",
  "designation_type": "DO",
  "designation_name": "Denominación de Origen Mezcal (DOM)",
  "regulatory_framework": json.dumps({"body": "Consejo Regulador del Mezcal (CRM)", "do_states": ["Oaxaca (primary)", "Guerrero", "Durango", "San Luis Potosí", "Tamaulipas", "Zacatecas", "Puebla", "Guanajuato", "Michoacán"], "categories": {"ancestral": "Most traditional — clay pot distillation, stone tahona milling", "artesanal": "Copper or clay pot still, stone or mechanical milling", "mezcal": "Industrial — column or diffuser permitted"}}),
  "terroir_profile": json.dumps({"agave_diversity": "Oaxaca has the highest agave species diversity — 30+ species legally permitted", "key_species": {"espadin": "Agave angustifolia — 85% of production; cultivated; 7-9 years maturity", "tobala": "Agave potatorum — wild, rare, sierra (hillside) native; 12-15 years", "tepextate": "Agave marmorata — wild, slow-growing; 20-30 years maturity", "madre_cuishe": "Agave karwinskii — tall, cylindrical; complex earthy character", "arroqueño": "Agave americana var. oaxacensis — massive plant, very low yield"}, "pit_roasting": "Earthen pit (palenque) lined with volcanic rock — mesquite or ocote (pine) fuel; 3-7 days roasting — THIS is the smoke source, the terroir expression"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "prestigious",
  "description": "Mezcal is to tequila what Armagnac is to Cognac — the artisanal, terroir-forward ancestor that preserves process the industrial version has abandoned. Any agave species, anywhere in the authorised states, distilled in the traditional way (pit roasting, stone milling, open fermentation, copper or clay pot distillation) is mezcal. Oaxaca produces 85% of all mezcal. The earthen pit roast — burying the piñas (agave hearts) with hot rocks for 3-7 days — is the source of mezcal's distinctive smoke character, which varies by fuel type (mesquite, ocote), pit depth, and duration. Each palenque (mezcal distillery) and maestro mezcalero produces a distinct expression.",
  "key_producers": "Del Maguey (Ron Cooper — pioneered single-village mezcal; Vino de Mezcal, San Luis del Rio, Tobalá — benchmark), El Jolgorio (Exportadora Universal — single-agave, single-producer series), Vago (Aquilino García López family — espadin and wild variety focus), Bozal (wild variety focus), Rey Campero (Romulo Sanchez Pareja — ancestral production, tobalá and cuishe focus), Ilegal (from Guatemala), Wahaka (San Baltazar Guelavila)",
  "historical_context": "Agave fermentation in Oaxaca predates Spanish colonisation by at least 3,000 years — indigenous Zapotec and Mixtec cultures produced pulque (fermented agave sap) and likely early distilled spirits. Spanish conquistadors brought copper distillation technology from the Philippine trade route (galleon trade — Manila to Acapulco), likely merging with existing agave fermentation knowledge to create distilled mezcal in the 16th century. The Filipino connection to mezcal's origins is documented but underrecognised.",
  "authority_tier": 1,
  "source_text": "Gaytán, M.S. — ¡Tequila! Distilling the Spirit of Mexico (Stanford University Press, 2014); Valenzuela-Zapata, A.G. — El Agave Tequilero (Monsanto, 1994)",
  "slug": "oaxaca-mezcal"
},
{
  "name": "Jalisco — Tequila",
  "country": "Mexico",
  "beverage_family": "spirits",
  "designation_type": "DO",
  "designation_name": "Denominación de Origen Tequila (DOT)",
  "regulatory_framework": json.dumps({"body": "Consejo Regulador del Tequila (CRT)", "blue_agave_only": "Agave tequilana Weber — only permitted agave species", "do_regions": ["Jalisco (all municipalities)", "Parts of: Guanajuato, Michoacán, Nayarit, Tamaulipas"], "categories": {"blanco_silver": "Unaged or maximum 60 days in stainless or oak", "reposado": "2 months to 1 year in oak", "anejo": "1 to 3 years in oak barrels max 600L", "extra_anejo": "3+ years in oak — created 2006"}}),
  "terroir_profile": json.dumps({"highland_lowland": {"lowland_valley": "Jalisco Valley around Tequila town — red volcanic soil (tatemate), lower altitude — fruitier, earthier, softer agave", "highland_los_altos": "Highlands (Los Altos) around Arandas — higher altitude (2000m+), red clay soil (barro rojo), cooler — sweeter, more floral, refined agave"}, "blue_agave_cultivation": "7-12 years to maturity; harvested by jimadores with coa (specialised cutting tool); piña (heart) can weigh 25-100kg"}),
  "quality_trajectory": "ascending",
  "reputation_tier": "iconic",
  "description": "Tequila is blue agave (Agave tequilana Weber) distilled in a legally defined geographic region. The industry spans from mass-production industrial column-still Tequila (Cuervo Gold, Sauza) to artisanal traditional expression using tahona stone mills and pot stills (Fortaleza, Siete Leguas). The Highland/Lowland distinction shapes flavour as decisively as any terroir division: Highland tequilas (Casamigos, Código, Tequila Ocho) tend toward citrus, floral, and sweetness; Lowland tequilas (Herradura, Cazadores) tend toward earthier, more vegetal character. The jimador (harvester) and the 'piña' harvesting cycle is one of agriculture's most skill-dependent traditions.",
  "key_producers": "Patrón (ultra-premium — copper alembic stills, hand production, acquired by Bacardí 2018), Don Julio (founded 1942 — LVMH now — premium benchmark), Fortaleza (Guillermo Sauza — traditional tahona stone, small batch — artisanal benchmark), Siete Leguas (traditional, patio cooking, independent), Casamigos (George Clooney — sold to Diageo 2017 for $1B), Tequila Ocho (single estate, vintage-dated), Tequila Altos, Cazadores, El Tesoro de Don Felipe",
  "historical_context": "The town of Tequila in Jalisco gives the spirit its name. The Cuervo family received the first legal permit to commercially produce tequila in 1795. The 19th century saw American cowboys and traders introduce tequila to the US market via border towns — its identity as 'Mexican' became central to US-Mexico cultural relations. The 1990s and 2000s premium tequila boom redefined the spirit from bar-shot to sipping category.",
  "authority_tier": 1,
  "source_text": "Gaytán, M.S. — ¡Tequila! Distilling the Spirit of Mexico (Stanford University Press, 2014)",
  "slug": "jalisco-tequila"
},

# ============================================================
# BELGIUM
# ============================================================
{
  "name": "Belgium — Trappist & Lambic",
  "country": "Belgium",
  "beverage_family": "beer",
  "designation_type": "Protected Designation",
  "designation_name": "Authentic Trappist Product (ATP) / Lambic GI",
  "regulatory_framework": json.dumps({"body": "International Trappist Association (ITA) / EFSA", "atp_requirements": "Brewed within monastery walls, under monastic supervision, monks direct production, profits to charitable causes", "lambic_protection": "Geographical Indication — spontaneous fermentation in Senne valley watershed area only"}),
  "terroir_profile": json.dumps({"trappist_monasteries": 6, "lambic_region": "Pajottenland — southwest Brussels, Senne River valley", "lambic_wild_yeast": "Brettanomyces bruxellensis, Pediococcus, Lactobacillus, seasonal Saccharomyces — airborne, specific to this microclimate", "lambic_season": "Spontaneous fermentation only possible October-April — summer heat brings undesirable bacteria", "turbid_mash": "Deliberately undermodified mash — retains dextrins for Brettanomyces nutrition during long ageing"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Belgium produces the world's most diverse and complex beer culture — from Trappist monastery ales of extraordinary depth to spontaneously fermented lambic that ages for 1-3 years in oak before blending into gueuze. Trappist brewing: six Belgian monasteries (Chimay, Orval, Rochefort, Westmalle, Westvleteren, Achel) produce ales under International Trappist Association certification, with profits directed to charitable works. Westvleteren 12 (produced in limited quantities at Sint-Sixtus Abbey) has repeatedly been named the world's best beer. Lambic culture: spontaneous fermentation in the Senne Valley produces the most wine-like of all beers — acidic, funky, dry, complex. Gueuze (blended lambic of multiple ages) is 'the Champagne of beers.' Kriek (lambic + whole cherries) is one of the great flavour pairings in beverage history.",
  "key_producers": "Cantillon (lambic, gueuze, kriek — the pilgrimage brewery in Brussels), 3 Fonteinen (gueuze — benchmark blending), Brasserie de la Senne (Brussels craft), Lindemans (mass-market lambic), Timmermans (oldest lambic brewery c.1702), Boon (Mariage Parfait Gueuze — aged blend), Chimay (Trappist), Rochefort (Trappist 8 and 10), Westmalle (Trappist — Dubbel and Tripel), Orval (unique single Trappist beer with Brett character from refermentation), Brasserie Dupont (Saison Dupont — benchmark farmhouse ale)",
  "historical_context": "Trappist brewing has roots in the 7th-century monastic tradition of self-sufficiency — monks brewed beer because it was safer than water and provided nutrition during fasting. The modern Trappist certification system dates from 1997. Lambic's spontaneous fermentation tradition is essentially pre-scientific — brewers were harnessing wild yeast before Pasteur identified its role in fermentation. The Cantillon Brewery in Brussels (founded 1900, still family-owned) is the definitive traditional lambic experience.",
  "authority_tier": 1,
  "source_text": "Hieronymus, S. — Brew Like a Monk (Brewers Publications, 2005); Beaumont, S. — The Great Beers of Belgium (Brewers Publications, 2008)",
  "slug": "belgium-trappist-lambic"
},

# ============================================================
# GERMANY
# ============================================================
{
  "name": "Bavaria — Reinheitsgebot",
  "country": "Germany",
  "beverage_family": "beer",
  "designation_type": "Regional Brewing Tradition",
  "designation_name": "Bayerische Reinheitsgebot Brewing Region",
  "regulatory_framework": json.dumps({"body": "Bayerische Brauerbund (Bavarian Brewers' Federation)", "reinheitsgebot_1516": "Water, barley, hops only (yeast not understood until 19th century — added to modern version)", "bavarian_festivals": "Oktoberfest (Munich) — 6.3M visitors annually, 7M litres consumed", "hefeweizen_protection": "Weissbierbrauereiprivileg — historically restricted Weizen brewing to ducal family"}),
  "terroir_profile": json.dumps({"munich_water": "Medium-hard — ideal for lager and Märzen production", "hallertau": "World's largest hop-growing region (in Bavaria) — Hallertauer Mittelfrüh the benchmark noble hop", "bavarian_yeast": "Weizen yeast produces isoamyl acetate (banana ester) and 4-vinylguaiacol (clove phenol) — the defining Hefeweizen character", "lagering_tradition": "Stored cold in mountain caves before refrigeration — caves at constant 2°C for months"}),
  "quality_trajectory": "established",
  "reputation_tier": "iconic",
  "description": "Bavaria is the homeland of the Reinheitsgebot (1516 Purity Law) — the world's oldest food regulation still in force. The Bavarian beer tradition encompasses: Hefeweizen/Weissbier (wheat beer, yeast-cloudy, banana-clove character — Schneider Weisse, Weihenstephan, Paulaner, Erdinger); Märzen/Oktoberfest (amber lager, traditionally brewed in March and lager-stored until autumn — the Oktoberfest style); Dunkel (dark lager); Bock and Doppelbock (strong lager — Paulaner Salvator, Ayinger Celebrator); Rauchbier (smoked malt, Bamberg — Schlenkerla Aecht Schlenkerla Märzen is the world's most distinctive beer). The Bavarian brauerei tradition is UNESCO-listed Intangible Cultural Heritage.",
  "key_producers": "Weihenstephan (world's oldest active brewery 1040 AD), Schneider Weisse (benchmark Weizen — Aventinus Doppelweizenbock), Paulaner (Munich — Hefeweizen and Salvator), Erdinger (volume Hefeweizen), Spaten (the original Oktoberfest), Augustiner (Munich — the local's choice), Franziskaner (Weizen), Schlenkerla (Bamberg — Rauchbier), Ayinger (village brewery — exceptional range)",
  "historical_context": "The 1516 Reinheitsgebot was a Bavarian law — it became German national law only in 1906 and was extended to Germany in 1919. The law was challenged in the EU courts in 1987 by foreign brewers who wanted to sell in Germany — the EU ruled it was an illegal trade barrier. Bavaria has maintained its own cultural interpretation of the law as a quality standard. The decoction mash — triple-boiling portions of the mash to extract maximum starch — is a distinctly Bavarian technique that produces the malty depth of Munich lagers.",
  "authority_tier": 1,
  "source_text": "Jackson, M. — The New World Guide to Beer (Running Press, 1988); Hieronymus, S. — For the Love of Hops (Brewers Publications, 2012)",
  "slug": "bavaria-reinheitsgebot"
},
{
  "name": "Rhine & Cologne — Kölsch/Altbier",
  "country": "Germany",
  "beverage_family": "beer",
  "designation_type": "Protected Designation",
  "designation_name": "Kölsch Konvention / Düsseldorf Altbier",
  "regulatory_framework": json.dumps({"body": "Kölner Brauerei-Verband (Cologne Brewers Federation)", "kolsch_protection": "Kölsch Konvention 1985 — Kölsch may only be brewed in the Cologne region", "eu_gi": "Kölsch received EU Protected Geographical Indication 1997"}),
  "terroir_profile": json.dumps({"kolsch": {"fermentation": "Top-fermented (ale yeast) then cold-conditioned (lagered) — hybrid ale-lager style", "glass": "Stange — tall, cylindrical, 0.2L", "character": "Pale golden, delicate — light malt, gentle hop bitterness, very clean, slight fruitiness", "serving": "Served by Köbes (traditional waiter) in rounds — keeps replacing until you cover glass with coaster"}, "altbier": {"location": "Düsseldorf", "fermentation": "Top-fermented, cold-conditioned", "character": "Amber to dark brown, firm bitterness, malt-forward, dry finish"}}),
  "quality_trajectory": "established",
  "reputation_tier": "respected",
  "description": "Kölsch (Cologne) and Altbier (Düsseldorf) are Germany's two locally protected top-fermented, cold-conditioned hybrid styles — the rivalry between the cities and their beers is one of Germany's great cultural debates. Kölsch is the more internationally known: pale, delicate, served in tiny 0.2L Stange glasses that are perpetually refilled. The Brauhaus (traditional brewery-restaurant) culture of Cologne — with the Köbes serving in perpetual rounds — is as formalised as any tea ceremony. Altbier is darker, more bitter, more assertive — Düsseldorf's answer to Munich's lager tradition.",
  "key_producers": "Kölsch: Früh (the tourist institution), Gaffel (volume Kölsch), Reissdorf, Päffgen (the local's choice), Dom, Mühlen. Altbier: Füchschen (traditional Altstadt Brauhaus), Im Uerige (benchmark Alt — bitter, earthy), Schumacher (oldest Alt brauhaus), Zum Schlüssel",
  "historical_context": "Kölsch's hybrid nature (ale yeast, lager cold conditioning) reflects Cologne's historical position as a crossroads between northern ale-brewing culture and southern Bavaria's lager tradition. The 1985 Kölsch Konvention was a political act of cultural self-preservation — limiting Kölsch production to Cologne ensured the style's local identity.",
  "authority_tier": 2,
  "source_text": "Jackson, M. — Beer (Dorling Kindersley, 1998)",
  "slug": "rhine-cologne-kolsch"
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for r in REGIONS:
        try:
            cur.execute(SQL, (
                r["name"], r["country"], r["beverage_family"],
                r.get("designation_type"), r.get("designation_name"),
                r.get("regulatory_framework"), r.get("terroir_profile"),
                r.get("quality_trajectory"), r.get("reputation_tier"),
                r.get("description"), r.get("key_producers"),
                r.get("historical_context"), r.get("authority_tier"),
                r.get("source_text"), True, r.get("slug")
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT region id={row[0]}: {row[1]}")
                inserted += 1
            else:
                print(f"  SKIP (exists): {r['name']}")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR {r['name']}: {e}")
    print(f"\nDone. {inserted} regions inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
