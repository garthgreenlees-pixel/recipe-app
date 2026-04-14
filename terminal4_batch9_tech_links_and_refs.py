#!/usr/bin/env python3
"""
Terminal 4 — Batch 9: beverage_technique_products links for refs 92-106,
plus additional beverage_references for: Australia, NZ, South Africa, Germany,
kombucha/kefir, Mate, Cacao, Italian wine, Spanish wine, Japanese tea.
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# ────────────────────────────────────────────────────────────────────────────────
# TECHNIQUE_PRODUCT LINKS
# technique_id = beverage_reference id; product_id = beverage_product id
# Format: (technique_id, product_id, relevance_note)
# ────────────────────────────────────────────────────────────────────────────────
TECH_LINKS = [
    # ref 92 — Kava (Piper methysticum)
    (92, 154, "Primary product for kava reference — Taki Mai Noble Kava Waka"),

    # ref 93 — Lambanog / Coconut Toddy
    # (no lambanog product inserted yet — skip for now)

    # ref 94 — Palm Wine and Atlantic Crossing
    (94, 174, "Clairin Sajous — rum tradition traceable to palm wine fermentation knowledge"),

    # ref 95 — Bourbon / Nearest Green
    (95, 172, "Buffalo Trace Bourbon — primary product for Bourbon reference"),
    (95, 173, "Uncle Nearest 1884 — central product for African American distilling heritage"),

    # ref 96 — Ethiopian Coffee
    # (Ethiopian coffee producers exist but no coffee product inserted — will add link when product exists)

    # ref 97 — Napa Valley
    (97, 175, "Opus One 2019 — flagship Napa Valley Cabernet Sauvignon"),
    (97, 176, "Ridge Monte Bello — Santa Cruz Mountains but emblematic California quality"),

    # ref 98 — Scotch Single Malt
    (98, 183, "Macallan 12 Sherry Oak — Speyside reference product"),
    (98, 184, "Ardbeg 10 — Islay reference product, peat spectrum"),
    (98, 185, "Springbank 10 — Campbeltown reference product"),

    # ref 99 — Mezcal vs Tequila
    (99, 161, "Del Maguey Vida — primary mezcal reference product"),
    (99, 171, "Fortaleza Blanco — primary tequila reference product"),

    # ref 100 — Belgian Lambic
    (100, 186, "Cantillon Gueuze — primary lambic reference product"),

    # ref 101 — Dealcoholised Wine
    (101, 188, "Leitz Eins Zwei Zero — primary NA dealcoholised reference product"),
    (101, 189, "Seedlip Spice 94 — NA crafted spirits reference product"),

    # ref 102 — Bordeaux 1855 Classification
    (102, 223, "Château Lafite Rothschild — first growth Bordeaux, 1855 classement"),
    (102, 225, "Château Latour — first growth Pauillac"),
    (102, 227, "Château Haut-Brion — only non-Médoc first growth"),
    (102, 224, "Château Mouton Rothschild — promoted to first growth 1973"),

    # ref 103 — Bordeaux Left vs Right Bank
    (103, 228, "Château Pétrus — quintessential Right Bank Merlot-dominant"),
    (103, 229, "Château Cheval Blanc — Right Bank, Cabernet Franc-dominant"),
    (103, 225, "Château Latour — quintessential Left Bank Cabernet Sauvignon-dominant"),

    # ref 104 — Northern Rhône Syrah
    (104, 233, "Guigal La Mouline — flagship Northern Rhône Côte-Rôtie"),
    (104, 235, "Chave Hermitage Rouge — Hermitage Syrah benchmark"),
    (104, 237, "Clape Cornas — Cornas reference product"),
    (104, 236, "Jaboulet La Chapelle — Hermitage La Chapelle historic benchmark"),

    # ref 105 — Châteauneuf-du-Pape
    (105, 238, "Château Rayas — quintessential Grenache CNDP"),
    (105, 239, "Beaucastel CNDP — 13-variety complexity benchmark"),

    # ref 106 — Champagne
    (106, 241, "Krug Grande Cuvée — non-vintage prestige Champagne reference"),
    (106, 242, "Salon Blanc de Blancs — single vineyard vintage blanc de blancs reference"),
    (106, 243, "Dom Pérignon — vintage prestige cuvée reference"),
    (106, 244, "Pierre Péters Les Chétillons — grower Champagne reference"),
    (106, 245, "Bollinger Special Cuvée — house style Pinot Noir dominated NV"),
    (106, 246, "Egly-Ouriet Blanc de Noirs — Ambonnay Pinot Noir Champagne"),
]

SQL_TECH = """
INSERT INTO beverage_technique_products (technique_id, product_id, relevance_note)
VALUES (%s, %s, %s)
ON CONFLICT (technique_id, product_id) DO NOTHING
RETURNING id, technique_id, product_id
"""

# ────────────────────────────────────────────────────────────────────────────────
# NEW BEVERAGE REFERENCES
# ────────────────────────────────────────────────────────────────────────────────
REFERENCES = [
    {
        "name": "Australian Wine — Barossa Old Vine Philosophy and Penfolds Grange Standard",
        "slug": "australia-barossa-old-vine-penfolds-grange",
        "category": "wine_regions",
        "origin": "Australia",
        "description": (
            "The Barossa Valley's pre-phylloxera old vine heritage — Shiraz, Grenache, Mourvèdre vines dating "
            "to the 1840s and 1850s, untouched by the root louse that devastated European viticulture — constitutes "
            "one of the world's most irreplaceable viticultural assets. The Old Vine Charter (established 2008) "
            "classifies: Old Vine (35+ years), Survivor Vine (70+ years), Centenarian Vine (100+ years), Ancestor "
            "Vine (125+ years). Penfolds Grange, first made by Max Schubert in 1951, established the Barossa's "
            "ambitions as a fine wine region. Using a multi-vintage, multi-vineyard philosophy with maturation in "
            "American oak, Grange set the standard for Australian icon wine. Henschke's Hill of Grace (1958, single "
            "vineyard Eden Valley Shiraz from pre-1860 Shiraz vines) represents the counter-tradition — terroir "
            "expression over blending. Together they define the dual Australian premium idiom: assemblage power "
            "vs. single-site precision. McLaren Vale's Old Vine register mirrors Barossa's, with Grenache-dominant "
            "wines and Mediterranean varieties (Fiano, Nero d'Avola) gaining prestige as the region redefines its identity."
        ),
        "authority_tier": 1,
        "source_text": "Barossa Old Vine Charter; Penfolds Grange technical notes; James Halliday Australia Wine Companion",
    },
    {
        "name": "New Zealand Wine — Marlborough Sauvignon Blanc Identity and Central Otago Pinot Noir Emergence",
        "slug": "new-zealand-wine-marlborough-central-otago",
        "category": "wine_regions",
        "origin": "New Zealand",
        "description": (
            "New Zealand's wine identity divides into two great narratives. Marlborough Sauvignon Blanc: when "
            "Cloudy Bay's first vintage (1985) reached UK and US markets, it redefined what Sauvignon Blanc "
            "could be — the pungent, passionfruit-capsicum-citrus profile became a signature and commercial "
            "phenomenon. Marlborough now produces 77% of New Zealand's wine and is the world's reference "
            "for Sauvignon Blanc. The Wairau Valley (warmer, richer) and Awatere Valley (cooler, more "
            "austere) provide sub-regional diversity. Single-vineyard premium expressions from Seresin, "
            "Fromm, and Dog Point now challenge the image of commodity Sauvignon.\n\n"
            "Central Otago: at 45°S, the world's southernmost wine region, and the only South Island "
            "region with a continental (not maritime) climate. Annual temperature swings of 40°C enable "
            "Pinot Noir of extraordinary colour, structure, and aromatic complexity. Sub-regional identity "
            "has emerged: Bannockburn (schist-based, structured, dark cherry), Gibbston (high altitude, "
            "spice and aromatics), Cromwell Basin (volume and depth), Bendigo (warmth and opulence). "
            "Felton Road, Mt Difficulty, Ata Rangi (Martinborough), and Rippon define the benchmark style."
        ),
        "authority_tier": 1,
        "source_text": "NZ Wine; Jancis Robinson Oxford Companion to Wine; Bob Campbell MW NZ Wine Companion",
    },
    {
        "name": "South African Wine — The Cape Revolution: Post-Apartheid Diversity and Swartland Independence",
        "slug": "south-africa-cape-revolution-swartland",
        "category": "wine_regions",
        "origin": "South Africa",
        "description": (
            "South African wine carries the weight of its history. The first vines were planted at the Cape "
            "in 1655 by Jan van Riebeeck of the Dutch East India Company. Constantia dessert wine (18th-19th "
            "century) was the world's most celebrated sweet wine — Napoleon called for it on St. Helena. Post-"
            "apartheid, wine exports opened to the world (1994+), revealing a transformed, diversifying industry.\n\n"
            "Stellenbosch is the Cape's prestige red wine region — Cabernet Sauvignon, Cape blends (with "
            "Pinotage), and Syrah of world-class depth. The 2015 and 2017 vintages established Stellenbosch "
            "on par with global fine wine peers. Chenin Blanc is South Africa's most planted variety "
            "(20%+ of plantings) — old-vine Swartland Chenin from granite and schist soils competes "
            "with the Loire's best. The Swartland Revolution (2010+): Eben Sadie (Sadie Family Wines), "
            "Chris and Andrea Mullineux, and A.A. Badenhorst pioneered minimal-intervention, dry-farmed "
            "old vine wines from Grenache, Cinsault, Chenin Blanc. Tim Atkin MW's annual South Africa "
            "report has elevated the Cape's global profile. Pinotage (Pinot Noir × Cinsault cross, 1925) "
            "remains the Cape's most controversial and distinctive variety — rubber and smoke when poor, "
            "dark chocolate and mocha when masterful."
        ),
        "authority_tier": 1,
        "source_text": "Tim Atkin MW South Africa Annual Report; Wine & Spirit Education Trust South Africa module; Jancis Robinson Cape notes",
    },
    {
        "name": "German Wine — Riesling's Vertical Axis: VDP Classification, Prädikat System, and the Mosel Standard",
        "slug": "germany-riesling-vdp-pradikat-mosel",
        "category": "wine_regions",
        "origin": "Germany",
        "description": (
            "German Riesling is defined by two overlapping classification systems: the traditional Prädikat "
            "(ripeness-based, 1971 wine law) and the modern VDP (Verband Deutscher Prädikatsweingüter, estate "
            "quality pyramid, revised 2012).\n\n"
            "Prädikat levels: Kabinett (lightest, lowest sugar), Spätlese (late harvest), Auslese (selected "
            "bunches), Beerenauslese (individual berry selection), Trockenbeerenauslese (dried berry — "
            "Germany's equivalent of Sauternes ice cream), Eiswein (freeze-concentration). Alcohol ranges "
            "from 7.5% (Kabinett) to 8.5% (TBA). The off-dry 'halbtrocken' and bone-dry 'trocken' style "
            "debate has driven a generation of winemaker evolution.\n\n"
            "VDP pyramid: Gutswein (estate), Ortswein (village), Erste Lage (first cru, village wines with "
            "specific site), Grosse Lage / Grosses Gewächs (GG — equivalent to grand cru, dry only). "
            "The Mosel (Slate-based, steep — Bernkastel-Kues, Piesport, Wehlen, Ürziger, Brauneberger) "
            "produces the lightest, most racy Riesling (7.5-9% abv). Rheingau (south-facing Rhine slopes), "
            "Nahe, Pfalz (warmer), and Rheinhessen (Wittmann, Keller) constitute Germany's other top regions. "
            "Egon Müller, Prüm, Mosel estates define the benchmark. Leitz Eins Zwei Zero represents the "
            "benchmark dealcoholised Riesling — Germany's wine technology leadership."
        ),
        "authority_tier": 1,
        "source_text": "VDP Germany; Jancis Robinson German Wine; Wine & Spirit Education Trust WSET Diploma Germany module",
    },
    {
        "name": "Kombucha, Kefir, Tepache, and Jun: The Wild Fermentation Spectrum in Modern Beverage Service",
        "slug": "kombucha-kefir-tepache-jun-wild-fermentation",
        "category": "fermentation_knowledge",
        "origin": "Global",
        "description": (
            "The contemporary non-alcoholic fermented beverage movement draws on millennial-old traditions "
            "across cultures, now formalized for restaurant service:\n\n"
            "Kombucha (origin: China/Manchuria ~220 BCE): Sweetened tea fermented by a SCOBY "
            "(symbiotic culture of bacteria and yeast). Produces organic acids (acetic, glucuronic), B "
            "vitamins, and trace alcohol (<0.5% ABV — above 1.25% requires licensing). Categories: "
            "first fermentation (plain), second fermentation (carbonated, flavoured). GT's Synergy "
            "(original commercial US brand, 1995) and Jun (honey/green tea variant) define the "
            "mainstream segment.\n\n"
            "Milk Kefir (origin: Caucasus/Turkey): Kefir grains ferment milk producing a probiotic "
            "drink — lactic acid bacteria and yeasts. Distinct from yoghurt in having both bacterial "
            "and yeast populations. Water kefir (tibicos): sugar water fermented by water kefir grains — "
            "a lighter, non-dairy alternative.\n\n"
            "Tepache (origin: pre-Columbian Mexico): pineapple rind fermented with piloncillo and "
            "spices — 2-3 day fermentation. Traditional street drink now appearing on craft menus.\n\n"
            "Service considerations: most raw fermented drinks are pressure-sensitive. Serve at 2–6°C. "
            "Stack flavour pairings using fermented acidity similarly to wine — high acid = clean food "
            "bridge, umami-rich = amplification. GT's Gingerade: synergy pairing with raw fish, sashimi, "
            "and umami-forward Southeast Asian dishes."
        ),
        "authority_tier": 2,
        "source_text": "Sandor Katz — The Art of Fermentation (Chelsea Green, 2012); Wild Fermentation; Fermentation Science journal",
    },
    {
        "name": "Mate and Yerba Mate — The South American Shared Cup: Pharmacology, Culture, and Modern Service",
        "slug": "mate-yerba-mate-south-american-culture",
        "category": "traditional_cultural",
        "origin": "South America",
        "description": (
            "Yerba mate (Ilex paraguariensis) is the most consumed stimulant beverage in South America "
            "(Argentina, Uruguay, Paraguay, southern Brazil). Its cultural centrality rivals coffee in "
            "Europe — shared from a single gourd (mate) through a metal straw (bombilla), passed in a "
            "circle in ceremonies ranging from family morning rituals to gaucho fieldwork breaks.\n\n"
            "Pharmacology: Mate contains caffeine (~80mg per 250ml — similar to espresso), theobromine "
            "(mood elevation, found also in cacao), and theophylline. The combination is known anecdotally "
            "as 'clean energy' — stimulating without coffee's crash. L-theanine content (found also in "
            "green tea) may moderate anxiety. Mate has the highest antioxidant density of any common "
            "beverage by polyphenol count.\n\n"
            "Ceremony: The cebador (preparer) pours water at 70-75°C (never boiling — bitterness "
            "control) and serves each participant sequentially. The bombilla filters the loose leaf. "
            "Traditional forms: amargo (plain, bitter), dulce (sweetened — considered less authentic "
            "by traditionalists). Modern café culture in Buenos Aires has extended mate into cold-brew "
            "and cocktail applications.\n\n"
            "Service adaptation: As a restaurant offering, mate's sharing ceremony can be adapted for "
            "communal welcome service, digestif, or a cultural tasting flight alongside South American "
            "wine programmes. Pair with dulce de leche alfajores, facturas (pastries), and empanadas."
        ),
        "authority_tier": 2,
        "source_text": "Elvira González de Mejía — Mate tea review, Journal of Food Science; UNESCO intangible heritage; Argentine Mate Institute",
    },
    {
        "name": "Ceremonial Cacao — The Mesoamerican Liquid Gold: Theobroma cacao, Ceremony, and Modern Revival",
        "slug": "ceremonial-cacao-mesoamerican-theobroma",
        "category": "traditional_cultural",
        "origin": "Mesoamerica",
        "description": (
            "Theobroma cacao — 'food of the gods' — has been cultivated for over 4,000 years. The earliest "
            "evidence of cacao consumption dates to ~1900 BCE (Olmec, pre-Mayan Mesoamerica). The Maya "
            "word kakaw becomes the Spanish cacao, the French chocolat, the English chocolate.\n\n"
            "Traditional ceremonial cacao: cold-ground 100% cacao paste (no sugar, no dairy) prepared "
            "as a warm beverage with water, chili, vanilla, achiote (annatto for red colour), and "
            "occasionally honey or agave. The Ka'Kau ceremony (Guatemala, contemporary revival led by "
            "Keith Wilson/Cacao Shaman from San Marcos La Laguna, Lake Atitlán) uses whole-bean Guatemalan "
            "cacao in circles of 25-50 people for meditative, heart-opening intentions.\n\n"
            "Pharmacology: Theobromine (cardiovascular vasodilator — gentle, long-duration stimulant), "
            "anandamide (endocannabinoid, 'bliss molecule'), PEA (phenylethylamine — mood elevation), "
            "magnesium (highest plant source), iron, flavanols (cardiovascular protection).\n\n"
            "Restaurant application: Ceremonial cacao service as a beverage course — replaces coffee "
            "for guests avoiding caffeine or seeking a spiritual-cultural dimension to dining. Prepared "
            "tableside from whole bean or paste. Temperature: 60-65°C. Traditional serving vessel: "
            "jícara gourd. Pair with cacao-origin foods: chili-chocolate mole, cacao nib tuile, vanilla. "
            "Suitable as a pre-meditation amuse or closing digestif course in wellness-oriented venues."
        ),
        "authority_tier": 2,
        "source_text": "Michael Coe — The True History of Chocolate; Sophie Coe; Keith Wilson/Cacao Shaman Guatemala; Harv. T.H. Chan cacao research",
    },
    {
        "name": "Barolo and Barbaresco — Nebbiolo's Vertical Expression: Communes, Crus, and the Modernist-Traditionalist Debate",
        "slug": "barolo-barbaresco-nebbiolo-communes-crus",
        "category": "wine_regions",
        "origin": "Italy",
        "description": (
            "Barolo and Barbaresco, both in Piedmont's Langhe hills, are made exclusively from Nebbiolo — "
            "Italy's most aristocratic grape variety. Tar and roses: the conventional description of "
            "Nebbiolo's aromatic profile. In youth: violet, red cherry, dried rose; with age: truffle, "
            "tobacco, tar, leather, balsam.\n\n"
            "Barolo communes (MGA — Menzione Geografica Aggiuntiva, established 2010, 181 crus): "
            "Barolo village (clay-calcium, feminine, earlier), Castiglione Falletto (mid-weight, "
            "elegant), La Morra (sand-clay, perfumed, accessible), Serralunga d'Alba (compact Helvetian "
            "soil, masculine, structured, 50-year wines), Monforte d'Alba (structured, complex). "
            "Vigna Rionda (Serralunga), Cannubi (Barolo village), Brunate (La Morra) are the most "
            "celebrated single vineyards.\n\n"
            "Barbaresco communes: Barbaresco, Neive, Treiso, San Rocco Seno d'Elvio. Barbaresco "
            "wines are lighter in style, earlier drinking — ageing requirement: 2 years (vs. Barolo's 3); "
            "Riserva: 4 years (vs. 5). Riserva must from single vineyard = exceptional product.\n\n"
            "The debate: Traditionalists (extended maceration, large Slavonian oak botti — wines that "
            "need 10+ years) vs. Modernists (shorter maceration, French barriques — approachable earlier). "
            "Today most producers use hybrid approaches. Giacomo Conterno, Bruno Giacosa, Bartolo Mascarello "
            "(traditionalist icons). Angelo Gaja (introduced barrique ageing 1960s, controversial but "
            "propelled Barbaresco to international fame at premium prices)."
        ),
        "authority_tier": 1,
        "source_text": "Ian d'Agata — Native Wine Grapes of Italy; Wine Spectator Barolo deep-dives; Wine & Spirit Education Trust Italy module",
    },
    {
        "name": "Brunello di Montalcino — Sangiovese Grosso and the Biondi-Santi Legacy",
        "slug": "brunello-montalcino-sangiovese-grosso-biondi-santi",
        "category": "wine_regions",
        "origin": "Italy",
        "description": (
            "Brunello di Montalcino is Italy's longest-lived and most age-worthy wine — legally required "
            "to age 5 years before release (Riserva: 6 years), with Sangiovese Grosso (Brunello clone) "
            "producing wines that can age 30-50 years.\n\n"
            "The origin: Ferruccio Biondi-Santi identified a local Sangiovese clone (Grosso) in the "
            "late 19th century producing superior structure compared to standard Sangiovese. His 1888 "
            "and 1891 bottles were still drank in the 20th century. Today, Biondi-Santi Riserva from "
            "the Greppo estate (and the Annata) remain the benchmarks.\n\n"
            "The territory: 3,500 hectares of vineyards around the hill town of Montalcino (DOCG "
            "established 1980). The town sits at 564m, with significant variation: northern slopes "
            "(cooler, more elegant), southern (Sant'Angelo in Colle — warmer, more opulent). Key "
            "sub-zones gaining official recognition: Montosoli, Colombaio di Cencio, Canalicchio, "
            "Madonna delle Grazie.\n\n"
            "Modern production: Casanova di Neri (Cerretalto Riserva), Poggio di Sotto, Salvioni, "
            "Soldera (Case Basse — biodynamic, minimalist), Ciacci Piccolomini represent the modern elite. "
            "Rosso di Montalcino DOC: the shorter-aged (1 year) earlier-drinking version using declassified "
            "lots — excellent value gateway to the appellation."
        ),
        "authority_tier": 1,
        "source_text": "Ian d'Agata Brunello chapter; Burton Anderson — Vino; Wine Spectator Brunello vintage analysis",
    },
    {
        "name": "Rioja — Tempranillo's Spanish Heartland: Ageing Classification and the Alta/Alavesa/Baja Diversity",
        "slug": "rioja-tempranillo-ageing-classification",
        "category": "wine_regions",
        "origin": "Spain",
        "description": (
            "Rioja DOCa (Denominación de Origen Calificada, 1991) produces Spain's most internationally "
            "recognised wines. Tempranillo (Tinto Fino, Ull de Llebre elsewhere) dominates plantings, "
            "with Garnacha, Mazuelo, and Graciano as blending varieties.\n\n"
            "The ageing classification system (revised 2018): Genérico (young, no minimum ageing), "
            "Crianza (2 years total, min 1 in oak), Reserva (3 years, min 1 in oak), Gran Reserva "
            "(5 years, min 2 in oak). A new village-level classification (Rioja de Municipio) and "
            "single-vineyard wines (Viñedo Singular) were introduced 2018 — a Burgundy-inspired move.\n\n"
            "Sub-zones: Rioja Alta (Haro, Logroño — higher altitude, Atlantic influence, Tempranillo "
            "with freshness and spice); Rioja Alavesa (Basque Country, mostly Tempranillo, limestone "
            "soils, elegant earlier-drinking wines); Rioja Oriental / Baja (warmer, Garnacha-dominant, "
            "fuller body, lower altitude).\n\n"
            "The oak debate: Traditional American oak (vanilla, coconut, dill) vs. French oak (more "
            "restrained, fruit-forward) vs. no oak (natural movement). The Spanish 'modern Rioja' "
            "movement (Artadi, Muga Torre Muga, Telmo Rodríguez) led a shift toward single-vineyard, "
            "French oak, earlier-harvested, more terroir-expressive wines. La Rioja Alta, López de "
            "Heredia (Viña Tondonia) and CVNE Viña Real define the traditional style benchmark."
        ),
        "authority_tier": 1,
        "source_text": "José Peñín Guide to Spanish Wine; WSET Diploma Spain module; Jancis Robinson Rioja overview",
    },
    {
        "name": "Japanese Green Tea — Matcha, Gyokuro, Sencha: Cultivation, Shading, and the Umami Spectrum",
        "slug": "japanese-green-tea-matcha-gyokuro-sencha",
        "category": "tea_knowledge",
        "origin": "Japan",
        "description": (
            "Japanese green tea culture divides primarily by shading technique and processing method:\n\n"
            "MATCHA: Stone-ground tencha leaves into fine powder. Tencha cultivation: shaded 20-30 days "
            "before harvest using tana (shading structures). Shading increases chlorophyll (vivid green) "
            "and L-theanine (umami/sweetness) while reducing catechins (bitterness). Ceremonial grade "
            "matcha (koicha — thick tea; usucha — thin tea) vs. culinary grade. Ippodo Tea Co. (Kyoto, "
            "est. 1717) and Marukyu Koyamaen are the highest-prestige Uji producers.\n\n"
            "GYOKURO: Highest grade of loose-leaf green tea. Shaded 3-6 weeks before harvest (longer "
            "than matcha tencha). Needle-shaped leaves brewed at 40-50°C (much lower than sencha). "
            "Extreme umami, almost no bitterness, sweet and ocean-like. Kyoto Uji's Okumidori and "
            "Samidori cultivars dominate premium gyokuro.\n\n"
            "SENCHA: The everyday Japanese green tea (75% of production). Full sun or partial shade. "
            "Steamed immediately after harvest (prevents oxidation). Fukamushi (deep-steamed, 30-60+ "
            "sec) vs. Asamushi (standard, 20-30 sec). First flush (Shincha, late April) = peak quality. "
            "Grassy, marine, balanced astringency. Shizuoka (Honyama, Kawane) and Kyoto Uji define "
            "premium sencha.\n\n"
            "HOJICHA: Roasted green tea (bancha or stems). Low caffeine, caramel-toasty. The most "
            "versatile food-pairing tea in Japanese cuisine — accessible to all palates."
        ),
        "authority_tier": 1,
        "source_text": "Ippodo Tea Co. educational materials; NHK World Tea Journey; World Green Tea Association; Tea Research Association of Japan",
    },
    {
        "name": "Chinese Tea — Pu-erh, Rock Oolong (Yancha), and Phoenix Dancong: The Fermented and Roasted Traditions",
        "slug": "chinese-tea-puerh-yancha-dancong",
        "category": "tea_knowledge",
        "origin": "China",
        "description": (
            "Three categories define China's most complex and collectible teas:\n\n"
            "PU-ERH (Yunnan): Post-fermented tea stored in compressed cakes, bricks, or tuocha. "
            "Two styles: Sheng (raw) — ages naturally over decades, transitioning from green/bitter "
            "to soft/earthy/complex; Shou (ripe) — accelerated 'wet pile' (wo dui) fermentation "
            "producing immediately earthy, smooth character (invented 1975 by CNNP/Kunming Tea Factory). "
            "Ancient tree (gushu) pu-erh from trees 300-1,000+ years (Yiwu, Bingdao, Bulang, Lao Banzhang) "
            "commands the highest prices in the world of tea — comparable to fine wine speculation. "
            "Dayi (大益) 7542 Sheng and 7572 Shou are the market benchmarks.\n\n"
            "ROCK OOLONG / YANCHA (Wuyi Shan, Fujian): Grown in the UNESCO World Heritage Jiuqu "
            "Stream area. 'Yanhua' (rock charm/mineral character) — the defining quality. High-fire "
            "charcoal roasting creates complex toasty-mineral notes. Key cultivars: Da Hong Pao "
            "(Big Red Robe — from the original six 'mother trees'), Rou Gui (Cinnamon), Shui Xian "
            "(Water Sprite), Jin Jun Mei (premium black tea from the same region).\n\n"
            "PHOENIX DANCONG (Chaozhou, Guangdong): Single-bush (dancong) oolongs, each bush "
            "expressing a distinct aroma type (xiang xing). Mi Lan Xiang (Honey Orchid), Ya Shi Xiang "
            "(Duck Shit — deliberately humble name to deter theft), Zhi Lan Xiang (Orchid). "
            "Medium oxidation, distinctive floral-fruity perfume. Brewed Chaozhou-style in "
            "tiny clay Yixing pots, multiple infusions."
        ),
        "authority_tier": 1,
        "source_text": "Bret Hinsch — A History of Tea; Global Tea Hut; Yunnan Sourcing educational resources; Hobbes The Half-Dipper pu-erh reviews",
    },
]

SQL_REF = """
INSERT INTO beverage_references (name, category, origin, description, authority_tier, source_text)
VALUES (%(name)s, %(category)s, %(origin)s, %(description)s, %(authority_tier)s, %(source_text)s)
RETURNING id, name
"""

conn = psycopg2.connect(CONN)

# 1. Insert technique_product links
tech_inserted = 0
print("=== TECHNIQUE PRODUCT LINKS ===")
for technique_id, product_id, note in TECH_LINKS:
    try:
        cur = conn.cursor()
        cur.execute(SQL_TECH, (technique_id, product_id, note))
        result = cur.fetchone()
        conn.commit()
        if result:
            tech_inserted += 1
            print(f"  LINK id={result[0]}: ref={result[1]} → product={result[2]}")
        else:
            print(f"  SKIP (exists): ref={technique_id} → product={product_id}")
    except Exception as e:
        conn.rollback()
        print(f"  ERROR ref={technique_id} product={product_id}: {e}")

print(f"\n{tech_inserted} technique_product links inserted.\n")

# 2. Insert references
ref_inserted = 0
print("=== BEVERAGE REFERENCES ===")
for ref in REFERENCES:
    try:
        cur = conn.cursor()
        cur.execute(SQL_REF, ref)
        result = cur.fetchone()
        conn.commit()
        if result:
            ref_inserted += 1
            print(f"  INSERT ref id={result[0]}: {result[1][:70]}")
        else:
            print(f"  SKIP (exists slug): {ref['slug']}")
    except Exception as e:
        conn.rollback()
        print(f"  ERROR {ref['slug']}: {e}")

print(f"\n{ref_inserted} references inserted.")
conn.close()
