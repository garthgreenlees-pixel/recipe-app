import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Azores (Terceira Island Biscoitos Wine, Atlantic Volcanic Terroir, Arabização Cultural Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=90,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Adega Cooperativa da Terceira',
    'location': 'Angra do Heroísmo, Terceira Island, Azores, Portugal',
    'country': 'Portugal',
    'region': 'Terceira Island — Biscoitos sub-zone, northwest volcanic coast',
    'key_person': 'Cooperative winemaking team; the Biscoitos growers are the primary custodians of the Verdelho and Arinto dos Açores varieties on basalt currais terraces',
    'founded': '1949 — established in the post-war era to consolidate Terceira Island wine production under cooperative management',
    'production_volume': 'Approximately 200,000–350,000 litres per year from cooperative members across the island; Biscoitos sub-zone accounts for the majority of the quality-tier production',
    'notable_products': [
        'Biscoitos Verdelho (white, dry — the flagship Terceira variety)',
        'Biscoitos Arinto dos Açores (white, dry — the Atlantic aromatic variety)',
        'Biscoitos Red (Bastardo and Terrantez do Pico blended red)',
        'DOC Biscoitos classification wines (the sub-zone appellation for Terceira)',
    ],
    'certifications': ['DOC Biscoitos (Denominação de Origem Controlada, Terceira sub-zone)'],
    'website': 'www.adegadaterceira.com',
    'philosophy': (
        'The Adega Cooperativa da Terceira preserves the basalt currais viticulture '
        'of Terceira Island — the stone-wall enclosure system that protects vines '
        'from Atlantic wind and retains volcanic basalt heat in the coastal growing '
        'zones of Biscoitos. The cooperative manages varieties that exist nowhere else '
        'on the planet outside the Azores archipelago.'
    ),
    'trail_connection': 'PCT (Portugal — Azores colonial node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Terceira Island Biscoitos Verdelho — Atlantic Volcanic Currais Viticulture, '
        'DOC Biscoitos, Adega Cooperativa da Terceira, Portuguese Atlantic Heritage'
    ),
    'tradition': 'wine',
    'sub_tradition': 'still white — Atlantic volcanic island, DOC Biscoitos, basalt currais enclosure viticulture',
    'region': 'Portugal — Azores (Terceira Island Biscoitos Wine, Atlantic Volcanic Terroir, Arabização Cultural Heritage)',
    'terroir_origin': (
        'Terceira is the third-largest island of the Azores archipelago, '
        'located at 38°43\'N in the mid-Atlantic, approximately 1,800km '
        'west of Lisbon. The island\'s geology is entirely volcanic — '
        'basalt lava flows from the Serreta volcanic system on the '
        'northwest coast created the Biscoitos viticulture zone, '
        'named for the characteristic biscuit-coloured basalt rock '
        'of the coastal lava plain. The Biscoitos vineyards occupy '
        'a 2–5km coastal strip on the northwest coast, growing '
        'in small enclosures called currais — dry-stone walls '
        'of black basalt built by hand to protect individual vine '
        'rows from the prevailing Atlantic trade winds. The basalt '
        'currais system is classified as an UNESCO-adjacent landscape '
        '(the Pico Island currais across the channel are UNESCO '
        'World Heritage); the Terceira currais are the same '
        'technology applied to a different volcanic island. '
        'Soils are thin, volcanic, iron-rich basalt with virtually '
        'no clay fraction — excellent drainage and intense '
        'mineral character. The Atlantic climate produces '
        'cool growing temperatures (16–22°C summer), '
        'high humidity (75–85% RH), and consistent '
        'Atlantic-driven rainfall (1,200mm/year). '
        'Verdelho is the dominant variety — an early-ripening, '
        'high-acid white grape that was historically central '
        'to the Madeira wine trade and which thrives in '
        'the Atlantic volcanic conditions of Terceira. '
        'The Biscoitos DOC was established in 1994.'
    ),
    'production_technique': (
        'Terceira Biscoitos Verdelho is produced using the '
        'classic Atlantic island white wine method: hand '
        'harvest in late August to early September (earlier '
        'than mainland Portugal due to the Atlantic island '
        'climate warming effect of the surrounding ocean), '
        'with selective sorting to remove Atlantic humidity-damaged '
        'bunches. The basalt currais create a micro-thermal '
        'environment where the black basalt stone walls absorb '
        'daytime solar radiation and re-emit heat to the vines '
        'at night — extending the effective thermal sum for '
        'ripening in the cool Atlantic climate. Pressing is '
        'pneumatic; fermentation at controlled temperature '
        '(16–18°C) in stainless steel to preserve the '
        'volatile aromatic compounds of the Verdelho variety '
        '(linalool, geraniol — the Muscat-adjacent floral '
        'register of the grape) that would be lost at '
        'higher fermentation temperatures. The wine is '
        'bottled young (March–May following harvest) to '
        'preserve primary fruit character and Atlantic '
        'mineral freshness. No oak contact — the Biscoitos '
        'style is defined by the reductive freshness of '
        'inert-vessel winemaking, not wood structure. '
        'The DOC Biscoitos regulations require minimum '
        'alcoholic strength of 10.5% ABV and prohibit '
        'enrichment — the Atlantic climate naturally '
        'delivers sufficient sugar accumulation in the '
        'basalt-retained heat of the currais. Sustainable '
        'viticulture practices are standard given the '
        'UNESCO-landscape sensitivity of the currais system; '
        'certified organic production is emerging in '
        'the cooperative\'s premium tier.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'wine — Pico Island Verdelho (Azores, UNESCO basalt currais)',
            'beverage': 'Pico Island Verdelho — UNESCO Landscape Basalt Currais Viticulture',
            'connection': (
                'Terceira Biscoitos Verdelho and Pico Island Verdelho '
                'are the two poles of the Azorean currais viticulture '
                'tradition — the same stone-wall enclosure system '
                'protecting the same Verdelho variety in the same '
                'Atlantic volcanic climate. The difference is geological: '
                'Pico\'s currais sit on the basalt fields at the foot '
                'of Pico volcano (the highest peak in Portugal) while '
                'Terceira\'s Biscoitos currais occupy a coastal lava '
                'plain from the Serreta volcanic system. Both produce '
                'Atlantic-mineral, high-acid white wines from Verdelho '
                'with an iodine-salt-citrus character derived from the '
                'Atlantic wind exposure through the currais walls. '
                'Pico holds the UNESCO designation; Terceira has the '
                'older cooperative infrastructure. Together they '
                'constitute the complete Atlantic volcanic Verdelho canon.'
            )
        },
        {
            'tradition': 'wine — Canary Islands (Lanzarote volcanic hoyo viticulture)',
            'beverage': 'Lanzarote Malvasía Volcánica — Hoyo Pit Viticulture, La Geria, Atlantic Volcanic',
            'connection': (
                'Terceira Biscoitos currais viticulture and Lanzarote '
                'hoyo pit viticulture represent the two architectural '
                'responses to Atlantic island volcanic viticulture: '
                'Terceira uses stone wall enclosures (currais) to '
                'protect against Atlantic wind while retaining basalt '
                'heat; Lanzarote uses individual pit depressions '
                'dug into the black lapilli (picón) volcanic ash '
                'to shelter each vine from the persistent trade '
                'winds while the dark volcanic ash absorbs heat '
                'and the low-growing vines access the volcanic '
                'moisture below the ash layer. Both systems produce '
                'mineral-intense Atlantic island white wines from '
                'varieties (Verdelho on Terceira; Malvasía Volcánica '
                'on Lanzarote) that express the volcanic mineral '
                'character of the basalt through the roots. The '
                'currais-hoyo parallel is the most important '
                'architectural comparison in Atlantic island '
                'viticulture and defines the PCT volcanic wine arc.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale lemon-gold with a green tinge from the high-acid '
            'Verdelho variety and the cool Atlantic fermentation; '
            'brilliant clarity from the pneumatic pressing and '
            'cold settling before fermentation; the colour depth '
            'is lighter than mainland Portuguese white wines due '
            'to the Atlantic climate reducing phenolic extraction '
            'during ripening; no oxidative tawny tones — '
            'the wine is a reductive, freshness-driven style.'
        ),
        'nose': (
            'The defining character of Terceira Biscoitos Verdelho '
            'on the nose is the Atlantic-mineral iodine register — '
            'a saline, sea-spray quality from the ocean wind exposure '
            'through the basalt currais walls, carried as volatile '
            'marine-mineral compounds absorbed through the vine roots '
            'from the volcanic soil. Overlaid on this mineral core: '
            'the citrus-floral register of the Verdelho variety '
            '(lemon zest, pink grapefruit, white peach — '
            'the same aromatic profile as Pico Verdelho but '
            'with a slightly warmer stone-fruit development '
            'from the Biscoitos coastal thermal retention); '
            'a characteristic green herb note (fennel, bay leaf) '
            'from the Atlantic hedgerow herbs that grow on the '
            'basalt lava plain; and the faint volcanic sulphur '
            '(struck flint, wet basalt) that is the terroir '
            'signature of all Azorean wines in youth.'
        ),
        'palate': (
            'High natural acidity (pH 3.0–3.2; TA 7–9g/L) '
            'from the cool Atlantic climate and the Verdelho '
            'variety\'s inherent tartaric acid retention; '
            'the entry is citrus-bright and mineral, with '
            'the Atlantic-iodine salinity providing a savoury '
            'counterpoint to the citrus fruit; medium body '
            '(10.5–12% ABV) with the lighter texture of '
            'volcanic island wines; the mid-palate develops '
            'the white peach and lemon cream character of '
            'ripe Verdelho while the volcanic mineral core '
            'remains constant; the finish is long (30–45 seconds) '
            'with persistent citrus-mineral salinity — '
            'the hallmark Atlantic freshness of Biscoitos. '
            'The wine is dry (residual sugar below 4g/L) '
            'with no perceptible sweetness despite the '
            'peachy fruit register of the variety.'
        ),
        'conclusion': (
            'The most direct expression of Atlantic volcanic currais '
            'viticulture outside the Pico Island UNESCO benchmark — '
            'a wine of mineral precision and Atlantic freshness '
            'that documents the Azorean volcanic wine tradition '
            'from Terceira\'s northwest coast.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'DOC Biscoitos single-quinta or single-currais selection '
                'from the oldest vine blocks (pre-1970 Verdelho, ungrafted '
                'or own-rooted on volcanic basalt); extended lees aging '
                '(8–12 months sur lie) adding biscuit-yeast complexity '
                'to the citrus-mineral core; only in exceptional '
                'Atlantic-calm harvests (low disease pressure, '
                'full phenolic ripeness despite the cool climate); '
                'typically from the Biscoitos DOC northern sub-blocks '
                'with maximum Atlantic wind exposure through the '
                'highest-built currais walls. Minimum 12% ABV. '
                'Aging potential 5–10 years.'
            ),
            'markers': (
                'Old-vine Verdelho; single-currais selection; '
                'sur lie complexity; citrus-mineral-biscuit; '
                '12%+ ABV; extended aging potential.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Cooperative-produced DOC Biscoitos Verdelho from '
                'identified member grower currais with selection '
                'criteria applied; clean primary citrus-mineral '
                'character with Atlantic salinity; pneumatic pressing; '
                'temperature-controlled fermentation; bottled within '
                '6 months of harvest; 10.5–12% ABV. '
                'The standard bearer of the Terceira wine tradition '
                'at accessible price (EUR 8–14 in the Azores market).'
            ),
            'markers': (
                'Identified grower currais; DOC Biscoitos; '
                'pneumatic press; temperature-controlled; '
                'primary citrus-Atlantic-mineral; 6-month bottling.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Cooperative blend without single-block selection; '
                'the primary Atlantic-mineral character is present '
                'but the citrus precision is diluted by blending '
                'across multiple harvest dates and currais locations; '
                'competent everyday Azorean white wine at EUR 4–8; '
                'the DOC Biscoitos minimum standard without the '
                'terroir specificity of the estate tier.'
            ),
            'markers': (
                'Cooperative blend; multi-block; primary fruit; '
                'diluted mineral precision; EUR 4–8.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Unclassified Terceira island white from non-Biscoitos '
                'zones (interior highland Terceira lacks the currais '
                'coastal thermal influence); higher pH from inland '
                'warmth reducing the acid tension that defines '
                'Biscoitos; oxidative handling during transport '
                'from cooperative to local cantinas; the Verdelho '
                'character is present but flattened by poor '
                'fermentation temperature control or oxidation.'
            ),
            'markers': (
                'Non-Biscoitos zone; flat acidity; oxidative '
                'handling; no currais terroir expression.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve at 8–10°C — the cool Atlantic freshness of '
            'Biscoitos Verdelho is best expressed at the lower '
            'end of the white wine service range. At temperatures '
            'above 12°C the volatile marine-mineral aromatic compounds '
            'dissipate quickly and the citrus register flattens. '
            'Ice bucket with water recommended; serve within '
            '30 minutes of opening. No decanting — the wine '
            'is a primary-fruit, reductive style that does not '
            'benefit from aeration. Serve young (within 2–3 years '
            'of harvest for standard tier; within 5–8 years '
            'for reserve single-currais selections).'
        ),
        'vessel': (
            'Standard white wine ISO glass (215ml tulip) or a '
            'slightly larger Burgundy-style white bowl to allow '
            'the Atlantic mineral aromatics to develop above '
            'the liquid surface. A Riedel Veritas Sauvignon Blanc '
            'glass is the closest shape match to the aromatic '
            'profile of Biscoitos Verdelho — the citrus-mineral '
            'register shares the aromatic lift requirement of '
            'Sauvignon Blanc without the herbaceous cut. '
            'For PCT programme service: present alongside '
            'the Pico Island UNESCO Verdelho and the Graciosa '
            'Island Arinto to complete the three-island '
            'Azorean white wine comparative.'
        ),
        'technique': (
            'Pour 90ml per guest; serve chilled from ice bucket; '
            'no decanting. Present the currais viticulture context — '
            'the stone-wall enclosure system, the basalt volcanic soil, '
            'and the Atlantic wind protection as the terroir '
            'explanation for the mineral-saline character.'
        ),
        'programme_position': (
            'PCT Atlantic volcanic wine arc: Terceira Biscoitos Verdelho '
            'alongside Pico UNESCO Verdelho, Faial Verdelho, and '
            'Graciosa Arinto for a four-island Azorean comparative; '
            'or as the Atlantic volcanic white wine foil in a '
            'volcanic island comparative alongside Lanzarote '
            'Malvasía Volcánica (Canary Islands) and Santorini '
            'Assyrtiko (Aegean volcanic) for a global '
            'volcanic white wine flight.'
        ),
        'verbal_presentation': (
            'Terceira Island. Biscoitos. The northwest coast. '
            'The black basalt walls that a farmer built by hand '
            'to stop the Atlantic wind killing his vines. '
            'The same volcanic soil, the same Verdelho grape, '
            'the same Atlantic iodine in the air. '
            'That is what you are tasting in this glass.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Adega Cooperativa da Terceira (Angra do Heroísmo, Terceira Island) '
            '— the primary commercial producer of DOC Biscoitos Verdelho; '
            'the cooperative manages the majority of the island\'s '
            'classified currais viticulture. '
            'Secondary reference: Quinta do Badejo (independent producer, '
            'Biscoitos zone — small production, estate-bottled).'
        ),
        'producer_location': 'Angra do Heroísmo, Terceira Island, Azores, Portugal',
        'key_person': 'Cooperative winemaking team; individual growers within the Biscoitos DOC zone',
        'production_volume': 'Approximately 200,000–350,000 litres/year cooperative total; Biscoitos DOC tier approximately 50,000–80,000 litres',
        'certifications': ['DOC Biscoitos', 'Indicação Geográfica Protegida Açores'],
        'bc_distributor': '[PROVIDER: verify through Azores/Portugal specialist importer — no confirmed BC listing as of 2026]',
        'us_distributor': '[PROVIDER: verify through mid-Atlantic Portugal specialist — limited US import as of 2026]',
        'uk_distributor': '[PROVIDER: verify through Azores specialist — Wines of Portugal trade body for UK leads]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Terceira Biscoitos Verdelho is primarily available '
            'in the Azores market and metropolitan Portugal; '
            'export infrastructure is limited compared to '
            'Pico Island wines (which have established the '
            'Azorean volcanic wine brand internationally). '
            'Programme buyers should source through Azores '
            'regional wine agents or direct-import from '
            'the cooperative. The DOC Biscoitos designation '
            'provides legal appellation verification.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Terceira Island Biscoitos occupies the Atlantic volcanic wine '
        'node of the Portuguese Colonial Trail — the currais viticulture '
        'system that developed in the 15th–16th century Azores as '
        'Portuguese settlers adapted mainland viticulture technology '
        'to the Atlantic volcanic island conditions. Terceira '
        '(named for being the third island discovered) was a '
        'critical mid-Atlantic waypoint in the Portuguese colonial '
        'trade routes from Lisbon to Brazil, the Caribbean, and '
        'the African coast — the island\'s wine tradition developed '
        'in parallel with its function as a resupply station for '
        'the Carreira da Índia (the India trade route). The Biscoitos '
        'currais viticulture is the living agricultural heritage '
        'of that colonial-era Atlantic island settlement.'
    ),
    'food_pairings': [
        {
            'technique_id': 'TER-001',
            'dish': 'Alcatra (Terceira Island beef stew with bay leaf, allspice, and Verdelho wine — the island\'s signature dish)',
            'pairing_type': 'bridge',
            'rationale': (
                'Alcatra is the traditional Terceira dish — a slow-braised '
                'beef stew made with Biscoitos Verdelho as the braising '
                'liquid, creating a within-terroir pairing where the '
                'wine\'s Atlantic mineral character bridges the beef '
                'richness through the citrus acidity cutting the fat '
                'while the volcanic mineral salinity of the wine '
                'resonates with the allspice and bay leaf aromatics '
                'of the stew.'
            )
        },
        {
            'technique_id': 'TER-002',
            'dish': 'Lapas grelhadas (Atlantic limpets grilled with lemon, butter, and garlic — the Azorean seafood staple)',
            'pairing_type': 'complement',
            'rationale': (
                'The Atlantic-iodine mineral salinity of Biscoitos Verdelho '
                'is the defining complement to grilled Atlantic limpets — '
                'the limpets\' intense iodine-mineral character from the '
                'rocky volcanic coastline resonates with the same volcanic '
                'mineral register in the wine, while the citrus acidity '
                'of the Verdelho cuts the butter and garlic richness.'
            )
        }
    ],
    'source': 'IVBAM (Instituto do Vinho, do Bordado e do Artesanato da Madeira) Azores wine documentation; Wines of Portugal Azores region technical notes; Jancis Robinson Oxford Companion to Wine (Azores entry); Mayson Richard — Portugal\'s Wines and Wine Makers; Adega Cooperativa da Terceira producer documentation',
    'price_trajectory': 'rising'
})

session.commit_batch()

# Entry 2: Madeira Terrantez
session.switch_region(
    'fortified',
    'Portugal — Madeira (Terrantez Rare Variety, Historic Blending Component, Near-Extinct Heritage, D\'Oliveiras Reserve)'
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Pereira d\'Oliveira Vinhos',
    'location': 'Funchal, Madeira, Portugal',
    'country': 'Portugal',
    'region': 'Madeira — island-wide production; Terrantez stocks from surviving pre-phylloxera vine parcels',
    'key_person': 'Luis d\'Oliveira — fifth-generation family winemaker; the d\'Oliveira family holds some of the oldest documented Madeira wine stocks in existence, including Terrantez back to the 1850s',
    'founded': '1820 — one of the oldest surviving Madeira wine houses; predates phylloxera, oidium, and both world wars',
    'production_volume': 'Small family producer; Terrantez production is measured in hundreds of litres per year from surviving vine parcels; total production approximately 100,000–200,000 litres/year across all varieties',
    'notable_products': [
        'D\'Oliveiras Terrantez (rare variety — the benchmark world reference)',
        'D\'Oliveiras Colheita Boal (single-vintage medium-sweet)',
        'D\'Oliveiras Malmsey 10-Year (reserve rich sweet)',
        'D\'Oliveiras Verdelho 10-Year (reserve semi-dry)',
        'D\'Oliveiras Reserva Old Blends (pre-20th-century stocks)',
    ],
    'certifications': ['DOP Madeira', 'Indicação Geográfica Protegida Madeira'],
    'website': 'www.oliveiras.pt',
    'philosophy': (
        'Pereira d\'Oliveira represents the family-house tradition of Madeira '
        'winemaking — estate-level production from owned vine parcels on the '
        'island\'s terraced basalt slopes, with the d\'Oliveira family holding '
        'pre-phylloxera vine material (Terrantez, Bastardo, Tinta Negra) that '
        'no other Madeira house can replicate. The Terrantez holdings are '
        'the most significant surviving collection of this near-extinct variety.'
    ),
    'trail_connection': 'PCT (Portugal — Madeira fortified wine node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Madeira Terrantez — Near-Extinct Heritage Variety, D\'Oliveiras Reserve, '
        'Medium to Medium-Sweet, Pre-Phylloxera Vine Heritage, PCT Fortified Pinnacle'
    ),
    'tradition': 'fortified',
    'sub_tradition': 'madeira — Terrantez variety, canteiro aging, medium to medium-sweet style (between Bual and Malmsey)',
    'region': 'Portugal — Madeira (Terrantez Rare Variety, Historic Blending Component, Near-Extinct Heritage, D\'Oliveiras Reserve)',
    'terroir_origin': (
        'Madeira is a 741km² volcanic island in the Atlantic Ocean, '
        '600km west of Morocco and 1,000km southwest of Lisbon, '
        'at 32°37\'N. The island\'s terrain is dominated by steep '
        'basalt ridges rising to 1,862m (Pico Ruivo) — the '
        'extreme topography that creates the multi-aspect '
        'viticulture of Madeira, where different varieties '
        'are planted on different aspects at different altitudes '
        'to exploit the range of sun exposure and rainfall '
        'across the island. Terrantez is historically planted '
        'on the south-facing mid-altitude terraces (300–600m) '
        'of the island — volcanic basalt soils of low fertility '
        'and excellent drainage, with the Atlantic-moderated '
        'climate delivering consistent temperatures (18–25°C '
        'growing season) and high humidity from the '
        'north-Atlantic trade winds. Terrantez was one of '
        'the "noble" Madeira varieties — the historic classification '
        'that included Sercial, Verdelho, Bual, and Malmsey '
        'as the four canonical Madeira wines — until the '
        '19th-century epidemics of oidium (1852) and '
        'phylloxera (1872–1880) eliminated the vast majority '
        'of Terrantez plantings. The few surviving vine parcels '
        'are concentrated in the hands of the oldest family '
        'houses — primarily D\'Oliveiras, which holds the '
        'most significant documented Terrantez stocks on '
        'the island. The variety is positioned between '
        'Bual (medium-sweet, 65–80g/L residual sugar) '
        'and Malmsey (rich sweet, 96–135g/L) in sweetness, '
        'with a higher natural acidity than Malmsey that '
        'creates an unusual tension between sweetness and '
        'freshness not achievable with other Madeira varieties.'
    ),
    'production_technique': (
        'Terrantez Madeira is produced using the canteiro '
        'aging method — the traditional sun-heated loft '
        'aging system that is the mark of quality in Madeira '
        'production. The Terrantez harvest occurs in late '
        'September to early October from the surviving '
        'mid-altitude terraced parcels; the grapes are '
        'pressed in pneumatic or hydraulic presses and '
        'the must is fermented in stainless steel or '
        'traditional lagares (stone tanks) until a '
        'target sugar level is reached. Fortification '
        'with 96% ABV grape spirit (aguardente vínica '
        'produced from Portuguese mainland wine) '
        'arrests fermentation, preserving the target '
        'residual sugar level characteristic of Terrantez '
        '(typically 65–100g/L — the medium-sweet register '
        'between Bual and Malmsey). The fortified wine '
        'is then transferred to 600-litre American oak '
        'pipes for canteiro aging: the pipes are stored '
        'in the sun-heated lofts (estufas naturais) '
        'of the lodge buildings in Funchal, where summer '
        'temperatures reach 30–40°C in the upper loft '
        'levels. The heat accelerates the Maillard reaction '
        'and oxidative esterification that creates the '
        'characteristic Madeira flavour profile — '
        'caramelisation, dried fruit concentration, '
        'and the irreversible oxidation that makes '
        'Madeira the most stable aged wine on earth. '
        'Terrantez is aged minimum 5 years in canteiro '
        'for the 5-year reserve; the D\'Oliveiras '
        'reserve expressions age 10–20+ years before '
        'bottling. The exceptional Terrantez colheita '
        '(single-vintage) expressions from D\'Oliveiras '
        'include bottles dated to the 1870s and 1900s — '
        'wines from before and after the phylloxera '
        'epidemic that nearly destroyed the variety.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'fortified — Sherry (Jerez, Spain — oxidative cask aging)',
            'beverage': 'Amontillado Sherry — Oxidative Cask Aging, Flor Layer, Mid-Range Sweetness',
            'connection': (
                'Terrantez Madeira and Amontillado Sherry occupy the same '
                'conceptual position in their respective fortified wine '
                'traditions: both are positioned at the mid-sweetness '
                'register between the dry and rich-sweet expressions, '
                'both derive their complexity from extended oxidative '
                'aging in wood (Terrantez in American oak pipes under '
                'canteiro sun-heat; Amontillado in American oak butts '
                'under the solera system after the flor yeast dies), '
                'and both display the nutty-dried-fruit-caramel '
                'oxidative character that is the hallmark of '
                'extended cask aging under oxidative conditions. '
                'The key difference is the heat source: Madeira '
                'canteiro relies on Atlantic sun-heated loft temperatures '
                '(30–40°C) to drive the Maillard reaction; Sherry relies '
                'on the Jerez climate and the biological flor layer '
                'modulating the oxidation rate. Both produce wines '
                'of extraordinary longevity — Terrantez Madeira and '
                'Old Amontillado Sherry share the 50–100-year '
                'aging potential that makes them the longest-lived '
                'wines in the fortified wine world.'
            )
        },
        {
            'tradition': 'fortified — Vintage Port (Douro, Portugal — bottle aging)',
            'beverage': 'Vintage Port — 20-Year Bottle Aging, Douro Schist, Declared Vintage',
            'connection': (
                'Terrantez Madeira and Vintage Port represent the two '
                'Portuguese fortified wine traditions at their highest '
                'expression — both are aged for decades, both derive '
                'complex dried-fruit and caramel character from their '
                'aging method, and both are among the most age-worthy '
                'wines produced anywhere in the world. The '
                'fundamental distinction is the aging environment: '
                'Madeira canteiro aging is oxidative (the wine '
                'is continuously exposed to oxygen through the '
                'wood pores in the heated loft), while Vintage '
                'Port is reduced (sealed in bottle after only '
                '2 years in cask, developing complexity through '
                'reductive bottle aging without oxygen contact). '
                'Terrantez Madeira from D\'Oliveiras demonstrates '
                'that oxidative aging, when driven by heat '
                'rather than contact with rancio bacteria, '
                'produces a wine of equal complexity and '
                'longevity to the greatest Vintage Port expressions.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber-mahogany with a tawny-orange rim — the colour '
            'of 10+ years of canteiro oxidative aging in American oak; '
            'the Maillard reaction products (melanoidins from caramelised '
            'sugars and amino acids) produce the characteristically dense, '
            'warm amber of aged Madeira that distinguishes it from '
            'the paler Amontillado amber of Sherry; brilliant clarity '
            'from extended aging; the viscous, slow-moving legs '
            'of a high-sugar, high-alcohol fortified wine (19–20% ABV, '
            '65–100g/L residual sugar). Pre-phylloxera Terrantez '
            'colheita bottles from the D\'Oliveiras archive display '
            'the near-black mahogany of extreme oxidative aging.'
        ),
        'nose': (
            'The defining aromatic character of Terrantez Madeira is the '
            'tension between the medium-sweet Bual-adjacent richness '
            'and the unusually high natural acidity of the Terrantez '
            'variety — a combination that produces the unique aromatic '
            'register of candied citrus peel (the orange marmalade '
            'quality from the citric acid preserved through the '
            'Maillard caramelisation), roasted walnut (Maillard '
            'browning product of the amino acids in the grape must '
            'under canteiro heat), dried apricot and figs '
            '(the oxidative ester concentration from extended '
            'cask aging), and a characteristic mineral-volcanic '
            'note from the basalt soil that survives the '
            'canteiro aging process as a smoky-mineral background. '
            'The rancio oxidative character (the deliberate '
            'controlled rancidity of extended fortified wine aging) '
            'is present in reserve expressions — a characteristic '
            'that is only found in wines of 10+ years canteiro aging.'
        ),
        'palate': (
            'The Terrantez palate is defined by its unusual acidity-sweetness '
            'balance: at 65–100g/L residual sugar the wine has significant '
            'sweetness, but the Terrantez variety\'s high natural acidity '
            '(TA 7–10g/L even after the Maillard caramelisation reduces '
            'some of the volatile acid) creates a tension that prevents '
            'the sweetness from cloying — the finish has a clean, '
            'citrus-acid length that the richer Malmsey style lacks. '
            'Entry: orange marmalade and roasted walnut from the '
            'Maillard products; mid-palate: dried apricot and fig '
            'from the oxidative ester concentration; '
            'the finish (45–60 seconds minimum in reserve expressions) '
            'resolves through the citrus-acid signature of the '
            'Terrantez variety — the longest and most complex finish '
            'of any Madeira variety at the medium-sweet register. '
            'The 19–20% ABV fortification is perfectly integrated '
            'in aged expressions — no alcohol heat.'
        ),
        'conclusion': (
            'Terrantez is Madeira at its most intellectually demanding — '
            'the near-extinct variety that balances between '
            'the known benchmarks of Bual and Malmsey with '
            'an acidity-sweetness tension unique to its genetic character. '
            'D\'Oliveiras holds the world reference stock.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'D\'Oliveiras Terrantez Colheita (single-vintage, '
                'dated bottle from specific harvest year) — the world '
                'benchmark for Terrantez; minimum 20 years canteiro aging '
                'before release; the pre-phylloxera archive expressions '
                '(1875, 1907, 1920s) represent the pinnacle of what '
                'Terrantez can achieve before the variety\'s near-extinction; '
                'contemporary colheita from post-2000 Terrantez replanted '
                'parcels requires minimum 20 years to show the '
                'full aromatic complexity. Amber-mahogany colour; '
                'rancio oxidative character; 65–100g/L residual sugar; '
                'TA 7–10g/L; finish 60+ seconds.'
            ),
            'markers': (
                'D\'Oliveiras colheita; single vintage; 20+ years canteiro; '
                'rancio character; marmalade-walnut-apricot complex; '
                'extraordinary acid-sweet tension; 60-second finish.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'D\'Oliveiras Terrantez 10-Year Reserve — blended '
                'across multiple colheita years with minimum 10 years '
                'canteiro aging; the commercial expression of the '
                'D\'Oliveiras Terrantez house style; shows the '
                'characteristic orange marmalade, roasted walnut, '
                'and dried apricot of the variety in clear development; '
                'the acid-sweet tension is present and defined; '
                '65–80g/L residual sugar; EUR 35–60 per 500ml. '
                'This is the accessible entry point into Terrantez '
                'for programme buyers.'
            ),
            'markers': (
                'D\'Oliveiras 10-Year; blended colheita; 10+ years canteiro; '
                'marmalade-walnut-apricot profile; defined acid-sweet tension.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Other producers\' Terrantez expressions where the variety '
                'is used as a blending component rather than a varietal '
                'bottling — Terrantez is often blended into Bual '
                'or Verdelho reserves for complexity without the '
                'reserve designation; the Terrantez character '
                'contributes to the blend but is not the sole '
                'aromatic driver. Market-tier access to the variety '
                'through blended Madeira at EUR 20–35.'
            ),
            'markers': (
                'Blended with Bual or Verdelho; Terrantez character '
                'present but not dominant; market price access.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Terrantez does not have a house/entry-level tier '
                'in the conventional sense — the variety is too rare '
                'and too expensive to produce to exist at an entry-level '
                'price point. Any claim of "Terrantez" at very low price '
                '(below EUR 25 per 500ml) should be questioned for '
                'varietal authenticity. The house tier reference '
                'for programme purposes is unverified Terrantez blend '
                'without D\'Oliveiras or IVBAM certification.'
            ),
            'markers': (
                'Unverified provenance; low price; potential mislabeling '
                'of Bual or Verdelho as Terrantez.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Terrantez Madeira at 14–16°C — slightly below room '
            'temperature but significantly warmer than table wine service. '
            'At the correct temperature the orange marmalade and roasted '
            'walnut aromatic compounds (the Maillard products of the '
            'canteiro heat aging) are fully expressed; below 12°C '
            'they contract and the wine reads as flat and overly '
            'sweet; above 18°C the alcohol (19–20% ABV) becomes '
            'perceptible as heat on the nose and palate. '
            'Remove from cellar storage (14°C) 15 minutes before service. '
            'No ice bucket — this is not a wine to chill.'
        ),
        'vessel': (
            'A tulip-shaped copita (the traditional Sherry service glass, '
            '120ml capacity) is the correct vessel for Terrantez Madeira '
            'at 45–60ml per pour; the tulip shape concentrates the '
            'complex oxidative aromatics above the liquid surface. '
            'Alternatively a standard ISO white wine glass at 60ml pour. '
            'Avoid large Bordeaux-style bowls — the oxidative aromatic '
            'compounds dissipate too quickly in the large air volume. '
            'For PCT programme comparative: present the Terrantez '
            'alongside the Bual (medium-sweet) and Malmsey (rich sweet) '
            'at matching pour volumes to demonstrate the variety\'s '
            'position in the Madeira sweetness spectrum.'
        ),
        'technique': (
            'Serve at 14–16°C; 45–60ml in copita or ISO white glass; '
            'no decanting required — Madeira is fully oxidised '
            'and does not benefit from aeration. Present the variety '
            'narrative: the near-extinction from phylloxera and oidium; '
            'the D\'Oliveiras archive; the unique acidity-sweetness '
            'tension of Terrantez between Bual and Malmsey.'
        ),
        'programme_position': (
            'PCT Madeira varietal arc: Terrantez alongside Sercial (dry), '
            'Verdelho (semi-dry), Bual (medium-sweet), and Malmsey (rich sweet) '
            'for the complete five-variety Madeira spectrum; or as the '
            'rarefied heritage single-variety in a fortified wine '
            'comparative alongside Vintage Port and PX Sherry '
            'for a three-tradition sweet wine depth flight.'
        ),
        'verbal_presentation': (
            'This variety nearly ceased to exist in the 1870s. '
            'Phylloxera killed the vines. D\'Oliveiras saved the last stocks. '
            'What you are tasting is the genetic memory of a variety '
            'that should have been extinct for 150 years. '
            'Notice the acid — that tension between sweet and sharp. '
            'Nothing else in Madeira does that.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Pereira d\'Oliveira Vinhos (Funchal, Madeira) — the world '
            'benchmark producer of Terrantez Madeira; holds the largest '
            'documented stocks of the variety including archive colheita '
            'bottles back to the 19th century. No other Madeira house '
            'has comparable Terrantez holdings. '
            'Secondary: Blandy\'s (The Madeira Wine Company) occasionally '
            'bottles small Terrantez releases when sourced from D\'Oliveiras '
            'or independent growers.'
        ),
        'producer_location': 'Funchal, Madeira, Portugal',
        'key_person': 'Luis d\'Oliveira — fifth-generation family winemaker',
        'production_volume': 'Hundreds of litres per year from surviving Terrantez parcels; extremely limited commercial release',
        'certifications': ['DOP Madeira', 'IVBAM registered producer'],
        'bc_distributor': '[PROVIDER: verify through BC Liquor Distribution Branch special order or private wine merchant specialising in Portugal]',
        'us_distributor': '[PROVIDER: check through Rare Wine Co. (specialist Madeira importer, USA) — primary US Madeira specialist]',
        'uk_distributor': '[PROVIDER: The Wine Society UK carries D\'Oliveiras — verify Terrantez availability through their Portugal buyer]',
        'price_tier': 'Reserve',
        'availability_notes': (
            'Terrantez is one of the rarest wines in the world — '
            'commercial availability is limited to direct-from-producer '
            'orders through D\'Oliveiras (funchal@oliveiras.pt) '
            'or through specialist Madeira merchants. '
            'The Rare Wine Co. in the USA is the primary English-language '
            'specialist importer for D\'Oliveiras expressions. '
            'Programme buyers should source the 10-year reserve '
            'as the standard programme expression '
            'and secure colheita expressions through '
            'specialist auction if required for '
            'advanced programme use.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Terrantez Madeira sits at the intersection of two PCT narratives: '
        'the Madeira fortified wine tradition as a British-Portuguese colonial '
        'trade product (the historical Madeira wine trade to the American '
        'colonies, the British Royal Navy, and the East India Company) and '
        'the near-extinction narrative of varieties destroyed by European '
        'agricultural epidemics in the 19th century. The D\'Oliveiras '
        'Terrantez archive represents the single most concentrated '
        'repository of pre-phylloxera Azorean-Atlantic wine heritage '
        'still in active commercial production.'
    ),
    'food_pairings': [
        {
            'technique_id': 'MAD-001',
            'dish': 'Queijo da Serra da Estrela (Portuguese mountain ewe\'s milk cheese, soft runny interior, washed rind)',
            'pairing_type': 'complement',
            'rationale': (
                'The orange marmalade and roasted walnut oxidative character '
                'of Terrantez Madeira complements the pungent, ammonia-touched '
                'washed rind of Queijo da Serra da Estrela through the '
                'sweet-salt contrast — the residual sugar (65–100g/L) '
                'of the Terrantez balancing the savory intensity of '
                'the cheese while the high acidity (TA 7–10g/L) '
                'prevents the pairing from becoming heavy.'
            )
        },
        {
            'technique_id': 'MAD-002',
            'dish': 'Bolo de mel da Madeira (Madeiran molasses cake with spices, nuts, and dried fruit)',
            'pairing_type': 'bridge',
            'rationale': (
                'The Madeiran bolo de mel shares the same Maillard-reaction '
                'aromatic vocabulary as the Terrantez Madeira — '
                'the molasses caramelisation and the spice-and-nut '
                'profile of the cake resonating with the orange '
                'marmalade, roasted walnut, and dried apricot '
                'of the wine in a within-island terroir bridge.'
            )
        }
    ],
    'source': 'IVBAM Madeira wine technical documentation; Cossart Gordon Norman — Madeira: The Island Vineyard; Mayson Richard — Madeira: The Mid-Atlantic Wine; Pereira d\'Oliveira producer archive; Rare Wine Co. Madeira importation records; Robinson Jancis Oxford Companion to Wine (Terrantez entry)',
    'price_trajectory': 'rising'
})

session.commit_batch()

# Entry 3: Niepoort Vintage Port 2011
session.switch_region(
    'fortified',
    'Portugal — Douro (Niepoort Vintage Port 2011, Declared Year, Granite and Schist Terraces, Single Quinta Expression)'
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Niepoort Vinhos',
    'location': 'Vila Nova de Gaia, Douro, Portugal (lodge); Quinta de Nápoles and Quinta do Carril, Cima Corgo (vineyards)',
    'country': 'Portugal',
    'region': 'Douro — Cima Corgo and Baixo Corgo; principal vineyards at Quinta de Nápoles (Santa Marta de Penaguião)',
    'key_person': 'Dirk Niepoort — fifth-generation family principal; considered one of the most innovative minds in Douro wine and Port production globally',
    'founded': '1842 — founded by Eduard Niepoort, a Dutch merchant; the Dutch connection to the Port wine trade predates the Methuen Treaty (1703) by which Britain secured preferential Port duties',
    'production_volume': 'Small by Port house standards; approximately 250,000–400,000 bottles/year total Port and Douro table wine production; Vintage Port declarations are rare and limited',
    'notable_products': [
        'Niepoort Vintage Port (declared years only — universally acclaimed)',
        'Niepoort Batuta (unfortified Douro red, the PCT\'s Douro table wine benchmark)',
        'Niepoort Redoma Branco (Douro white wine, critically acclaimed)',
        'Niepoort Tawny 10-Year (oxidative cask-aged Port)',
        'Niepoort Colheita (single-vintage tawny, the Niepoort tawny pinnacle)',
    ],
    'certifications': ['DOP Porto', 'DOP Douro', 'Instituto dos Vinhos do Douro e Porto (IVDP) registered shipper'],
    'website': 'www.niepoort-vinhos.com',
    'philosophy': (
        'Dirk Niepoort operates as the philosophical counterweight to the large '
        'Symington-owned houses that dominate the Port trade by volume — his '
        'Vintage Port declarations are among the most critically anticipated '
        'in the industry, his Douro table wines are internationally benchmark, '
        'and his approach to Port production (single quinta expressions, '
        'minimal intervention, traditional lagar foot-treading for the '
        'finest expressions) defines the artisan end of the Port wine spectrum.'
    ),
    'trail_connection': 'PCT (Portugal — Douro Port node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Niepoort Vintage Port 2011 — Universally Declared Year, Cima Corgo Schist Terraces, '
        'Foot-Treaded Lagar, Single Quinta Character, PCT Fortified Pinnacle'
    ),
    'tradition': 'fortified',
    'sub_tradition': 'vintage_port — declared vintage, bottle-aged, Douro Cima Corgo schist, foot-treaded lagar',
    'region': 'Portugal — Douro (Niepoort Vintage Port 2011, Declared Year, Granite and Schist Terraces, Single Quinta Expression)',
    'terroir_origin': (
        'Niepoort\'s Vintage Port draws from the Cima Corgo — '
        'the central and most prestigious sub-region of the Douro '
        'Valley, between the Régua and Pinhão tributaries, '
        'where the schist (xisto) bedrock dominates the '
        'steep terraced vineyard slopes. The Cima Corgo '
        'schist is the defining terroir of the greatest '
        'Vintage Port: the dark, heat-retaining slate-schist '
        'rock fractures naturally to allow vine root penetration '
        'to depths of 3–8 metres, accessing moisture from deep '
        'underground water tables during the dry Douro summer '
        '(June–September: less than 30mm rainfall/month, '
        'daytime temperatures 35–42°C). The schist retains '
        'and radiates heat at night, extending the photosynthetic '
        'activity window and concentrating the phenolic ripeness '
        '(tannin, anthocyanin, flavour precursors) in the '
        'Touriga Nacional, Touriga Franca, Tinta Roriz, '
        'and Tinta Barroca field-blend varieties that '
        'constitute the Vintage Port blend at Niepoort. '
        'The Douro\'s continental climate (hot dry summers, '
        'cold winters — rainfall concentrated October–March) '
        'produces a radically different viticulture challenge '
        'from the Atlantic-moderated Azores; the 2011 vintage '
        'in the Douro was characterised by a cool, wet spring '
        'followed by a hot, dry summer that concentrated '
        'the berry sugars and phenolics perfectly — '
        'universally declared by all the major houses '
        '(Symington, Quinta do Crasto, Graham\'s, Fonseca, '
        'and Niepoort among them).'
    ),
    'production_technique': (
        'Niepoort Vintage Port 2011 is produced using the '
        'traditional foot-treading in stone lagares — '
        'the granite or schist stone tanks in which the '
        'harvest grapes are trodden by foot for 4–6 hours '
        'during the initial extraction phase. Foot-treading '
        'is the historic and technically superior method '
        'for Vintage Port quality production: the human foot '
        'applies the correct pressure to extract colour '
        'and tannin from the grape skins without crushing '
        'the pips (seed tannin contamination would make '
        'the wine harsh), while the body heat of the '
        'treaders maintains the lagar at the ideal '
        'extraction temperature (28–32°C). The harvest '
        'occurs in late September; the field blend of '
        'indigenous Douro varieties is hand-harvested '
        'in 20kg baskets on the steep terraced schist slopes '
        'where mechanical harvesting is impossible '
        'given the gradient (30–70%). After 3–4 days '
        'of foot-treading fermentation (monitoring '
        'Baumé drop from 14–15° to the target '
        '6–7° for Vintage Port sweetness), the '
        'wine is run off into toneis (large oak vats) '
        'and fortified with 77% ABV grape spirit '
        '(aguardente vínica) at the rate of approximately '
        '110 litres per 440-litre pipe to arrest '
        'fermentation and preserve the target '
        'residual sugar (90–120g/L for Vintage Port). '
        'Vintage Port is aged only 18–24 months in '
        'wood (rather than the decades of canteiro '
        'aging for Tawny) before being bottled unfiltered '
        'for decades of reductive bottle aging. '
        'The 2011 Niepoort was bottled in 2013 '
        'and is now (2026) in the early-to-mid '
        'development window — fully structured '
        'but requiring further bottle age (10–20+ years) '
        'for the tannin to fully resolve into the '
        'complex bottle-aged character of a mature '
        'Vintage Port.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'wine — Barossa Valley (Australia, old-vine Shiraz, heat-concentrated)',
            'beverage': 'Barossa Valley Old-Vine Shiraz — Penfolds RWT, Heat-Concentrated, Dense Phenolic',
            'connection': (
                'Niepoort 2011 Vintage Port and Barossa Valley old-vine '
                'Shiraz share the critical production challenge of '
                'managing extreme phenolic concentration in a '
                'hot-climate continental growing environment: '
                'the Douro schist terraces (35–42°C summer days) '
                'and the Barossa Valley floor (35–44°C peak summer) '
                'both produce grapes with maximum anthocyanin and '
                'tannin concentration that require careful extraction '
                'management to avoid harsh tannin and jammy '
                'over-ripeness. Foot-treading in the Douro achieves '
                'the precision extraction that mechanical pumping '
                'cannot replicate; Barossa old-vine producers use '
                'open-ferment basket pressing to achieve similar '
                'tannin precision from Shiraz. Both wines are built '
                'for decades of aging — the Vintage Port through '
                'reductive bottle aging; the old-vine Shiraz through '
                'the same principle. The PCT connection: the schist-'
                'derived mineral character of Niepoort 2011 is the '
                'Douro equivalent of the ironstone-mineral character '
                'that defines Barossa old-vine expression.'
            )
        },
        {
            'tradition': 'fortified — Banyuls (France, Roussillon — fortified Grenache, schist terroir)',
            'beverage': 'Banyuls Grand Cru — Grenache Noir, Schist Terroir, Oxidative and Vintage Styles',
            'connection': (
                'Niepoort Vintage Port and Banyuls Grand Cru represent '
                'the two European fortified red wine traditions built on '
                'schist terroir and Grenache-family grapes (Douro: '
                'Touriga Nacional, Tinta Roriz, Touriga Franca; '
                'Banyuls: Grenache Noir on the Roussillon schist coastal '
                'cliffs). Both fortify during fermentation to preserve '
                'residual sugar and prevent full alcohol development; '
                'both produce vintage-dated expressions that age '
                'for decades in bottle. The schist mineral character '
                'is a shared terroir fingerprint — the slate-schist '
                'bedrock of the Douro Cima Corgo and the dark '
                'Banyuls schist both contribute a mineral-saline '
                'depth to the palate that distinguishes these '
                'wines from fortified wines produced on '
                'non-schist terroir (Port from granite-dominant '
                'Douro Superior; Roussillon fortified from '
                'clay-limestone zones). The most significant '
                'difference is scale: the Douro Vintage Port '
                'trade is globally dominant; Banyuls Grand Cru '
                'is a regional French speciality with limited '
                'international distribution.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep ruby-purple with a violet rim at 2026 assessment '
            '(13 years post-harvest) — the colour of a Vintage Port '
            'in its early development window; the anthocyanin pigments '
            'are still largely monomeric (bound to sulphur dioxide) '
            'and not yet fully polymerised into the brick-tawny '
            'rim of maturity; in a 750ml bottle the opacity is '
            'complete against a light source. The legs are slow '
            'and viscous from the 20% ABV and 90–120g/L residual '
            'sugar. By 2036–2040 the rim will show the first '
            'tawny-brick development signalling approaching maturity.'
        ),
        'nose': (
            'The 2011 Niepoort at 13 years post-harvest presents '
            'the primary-to-secondary aromatic transition of a '
            'Vintage Port in early development: dense blackcurrant '
            'and dark plum fruit (Touriga Nacional and Tinta Roriz '
            'primary aromatic compounds — anthocyanin-bound cassis '
            'and plum esters) with the first development of dried '
            'dark fruit character (the oxidative transformation '
            'from fresh to dried fruit beginning through the '
            'cork over 13 years); the schist-mineral note '
            '(the graphite-slate aromatic from the Cima Corgo '
            'xisto) provides depth; the 20% ABV fortification '
            'spirit aromatics are fully integrated — no alcohol '
            'heat on the nose; violet and dark chocolate '
            '(Touriga Nacional characteristic ester compounds) '
            'add complexity in the aromatic mid-section. '
            'The full complexity of a mature Vintage Port '
            '(tertiary dried fruit, leather, earth, rancio) '
            'requires further bottle aging.'
        ),
        'palate': (
            'Firm, structured tannin from the schist terroir and '
            'foot-treading extraction — the tannin of a 2011 '
            'Vintage Port at 13 years is still tight and '
            'requires 10–20 more years in bottle to fully '
            'resolve into the velvet texture of a mature '
            'Vintage Port. The entry is dense and sweet '
            '(90–120g/L residual sugar), with concentrated '
            'blackcurrant and dark plum fruit filling '
            'the mid-palate; the schist-mineral backbone '
            'provides structure beneath the fruit. '
            'The finish is long (45–60 seconds) with '
            'the characteristic Douro tannic grip of a '
            'young Vintage Port — dry tannin framing '
            'the sweet-fruit mid-palate. The 20% ABV '
            'integration is complete; no heat perceptible. '
            'The 2011 requires patience — drink from '
            '2030–2040 for the optimal maturity window.'
        ),
        'conclusion': (
            'A Vintage Port of the highest declared-year quality '
            'from the most critically regarded small Douro house — '
            'structured for multi-decade bottle aging and currently '
            'in the demanding early-development window. The PCT '
            'fortified wine pinnacle expression.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Declared Vintage Port from universally-declared years '
                '(2011, 2017, 2000, 1994, 1970, 1963, 1945) at '
                'benchmark small houses (Niepoort, Quinta do Crasto, '
                'Quinta do Vale Meão, Ramos Pinto) — wines with '
                'minimum 15 years bottle age showing the transition '
                'from primary fruit to secondary dried fruit and '
                'schist-mineral tertiary complexity. '
                'Dense ruby-tawny colour; blackcurrant-to-dried-plum '
                'aromatic evolution; velvet tannin structure; '
                '45–60 second finish; 20% ABV integrated; '
                '90–120g/L residual sugar balanced by schist acidity. '
                'Price: EUR 80–300+ per 750ml for declared single-quinta.'
            ),
            'markers': (
                'Declared year; small artisan house; 15+ years bottle age; '
                'dried fruit evolution; velvet tannin; schist mineral; '
                '45+ second finish.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Late Bottled Vintage (LBV) unfiltered from declared or '
                'non-declared years at quality producers (Ramos Pinto, '
                'Churchill, Quinta do Crasto) — 4–6 years in cask '
                'before bottling, producing a wine with the accessibility '
                'of early-drinking tannin structure but the characteristic '
                'Douro schist-mineral and Touriga Nacional aromatic '
                'profile; 18–20% ABV; 80–100g/L residual sugar. '
                'Price: EUR 20–45 per 750ml.'
            ),
            'markers': (
                'LBV unfiltered; quality producer; 4–6 years cask; '
                'accessible tannin; schist mineral present; '
                'Touriga Nacional aromatics.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Filtered LBV from volume producers (Sandeman, Cockburn\'s, '
                'Fonseca commercial tier) — filtered before bottling for '
                'commercial stability, removing the texture complexity '
                'of unfiltered production; the Douro character is present '
                'but softened; suitable for everyday commercial use '
                'without decanting. EUR 10–20.'
            ),
            'markers': (
                'Filtered LBV; volume producer; accessible tannin; '
                'commercial stability; lower complexity.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Ruby Port or generic Reserve Port (the lowest category '
                'in the Port classification — aged minimum 3 years '
                'in large casks, no vintage date, industrial production '
                'from Tinta Negra-dominant blends without the aromatic '
                'contribution of the noble Touriga Nacional family); '
                'the entry-level category that does not qualify as '
                'Vintage or LBV. EUR 5–12.'
            ),
            'markers': (
                'Ruby Port; no vintage; Tinta Negra blend; '
                'industrial production; no schist-mineral complexity.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Niepoort 2011 Vintage Port at 16–18°C — '
            'the correct temperature for a young-to-developing '
            'Vintage Port where the tannin structure and fruit '
            'concentration are the primary service experience. '
            'At temperatures below 15°C the tannin appears harsher '
            'and the fruit contracts; above 20°C the 20% ABV '
            'becomes perceptible as alcohol heat and the sweetness '
            'becomes heavy. If decanting (recommended for the 2011 '
            'at this stage of development): decant minimum 2 hours '
            'before service to allow the dense primary-fruit '
            'character to open and begin its aromatic development. '
            'Stand the bottle upright for 24 hours before opening '
            'to allow any sediment to settle.'
        ),
        'vessel': (
            'A standard ISO tasting glass or a slightly wider '
            'tulip-style Port glass (150–180ml capacity; 90ml pour '
            'maximum for Vintage Port — the sugar concentration '
            'makes larger pours overwhelming). For PCT programme '
            'comparative: present alongside the D\'Oliveiras '
            'Terrantez Madeira and a 20-year Tawny to demonstrate '
            'the three aging trajectories of Portuguese fortified '
            'wine (Vintage Port reductive bottle aging; '
            'Tawny Port oxidative cask aging; '
            'Madeira canteiro heat-oxidative aging) — '
            'the defining comparative of the PCT fortified wine arc.'
        ),
        'technique': (
            'Decant 2 hours before service; 16–18°C; 90ml maximum '
            'in ISO or Port glass; stand bottle 24 hours before '
            'opening for sediment settlement. Present the declared '
            'vintage narrative — 2011 as a universally great year, '
            'the foot-treading production, and the '
            '20–30-year maturity window.'
        ),
        'programme_position': (
            'PCT fortified wine pinnacle: Niepoort 2011 alongside '
            'D\'Oliveiras Terrantez Madeira and a 20-year Tawny '
            'for the three-tradition Portuguese fortified comparative; '
            'or as the structure benchmark in a world fortified '
            'wine flight alongside Banyuls Grand Cru (France), '
            'PX Sherry (Spain), and Commandaria (Cyprus) '
            'for a global fortified wine depth programme.'
        ),
        'verbal_presentation': (
            '2011. A year that every major Douro house declared. '
            'The cool spring, the dry summer, the concentration '
            'in the schist. Dirk Niepoort treads these grapes by foot '
            'in the old granite lagares. This wine needs 20 more years. '
            'What you are tasting now is potential — '
            'structured, dense, and not yet ready. '
            'That is what Vintage Port is for.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Niepoort Vinhos (Vila Nova de Gaia and Quinta de Nápoles, Douro) '
            '— the world benchmark for artisan-scale Vintage Port; '
            'Dirk Niepoort is consistently cited alongside '
            'Quinta do Crasto and Quinta do Vale Meão '
            'as the defining small-house Douro producer. '
            'For declared vintage Port from the large houses: '
            'Graham\'s, Fonseca, and Taylor Fladgate are the '
            'volume benchmarks; Niepoort is the artisan pinnacle.'
        ),
        'producer_location': 'Vila Nova de Gaia (lodge); Quinta de Nápoles, Cima Corgo (vineyards)',
        'key_person': 'Dirk Niepoort',
        'production_volume': '250,000–400,000 bottles/year total; Vintage Port declarations limited to declared years only',
        'certifications': ['DOP Porto', 'DOP Douro', 'IVDP registered shipper'],
        'bc_distributor': '[PROVIDER: verify through BC Liquor Distribution Branch — Niepoort wines listed periodically; check Marquis Wine Cellars Vancouver for allocation]',
        'us_distributor': '[PROVIDER: Niepoort USA is distributed through Skurnik Wines (New York) — verify current allocation and availability]',
        'uk_distributor': '[PROVIDER: Niepoort UK through Lea & Sandeman or Haynes Hanson & Clark — verify current UK import agent]',
        'price_tier': 'Reserve',
        'availability_notes': (
            'Niepoort 2011 Vintage Port at 2026 is in the secondary '
            'market phase — the original release was 2013; programme '
            'buyers should source through fine wine merchants '
            'with Port specialist departments (Berry Bros & Rudd UK; '
            'K&L Wine Merchants USA; or specialist Douro agent). '
            'The 2011 Vintage Port will continue to develop '
            'through 2035–2050 and should not be consumed '
            'before 2030 for optimal experience.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Niepoort 2011 Vintage Port is the PCT fortified wine pinnacle entry — '
        'the highest tier of the Portuguese colonial beverage heritage '
        'expressed in the Douro Valley\'s schist-terraced vineyards '
        'that have supplied Port wine to the world since the '
        'Methuen Treaty (1703) secured British trading preferences '
        'for Portuguese wine over French competition. The PCT '
        'Douro arc runs from the White Port aperitif culture '
        'through Tawny oxidative aging to the Vintage Port '
        'reductive bottle aging pinnacle — Niepoort 2011 '
        'is the structural reference point of that arc.'
    ),
    'food_pairings': [
        {
            'technique_id': 'DOU-001',
            'dish': 'Stilton (British blue cheese — the traditional Anglo-Port pairing, a cultural legacy of the Methuen Treaty trade)',
            'pairing_type': 'complement',
            'rationale': (
                'The Stilton-Vintage Port pairing is the most historically '
                'documented wine-cheese combination in the British '
                'colonial trade legacy — the Methuen Treaty (1703) '
                'gave British wine merchants preferential Port duties, '
                'and the combination of British blue cheese and '
                'Portuguese Port became a tradition of the British '
                'dining table from the 18th century. The pairing '
                'works through contrast: the sweet residual sugar '
                '(90–120g/L) of the Vintage Port balancing the '
                'salty-ammonia pungency of the Stilton while '
                'the Port tannin cuts the cheese fat.'
            )
        },
        {
            'technique_id': 'DOU-002',
            'dish': 'Dark chocolate (70%+ cacao — the tannin-tannin bridge pairing)',
            'pairing_type': 'bridge',
            'rationale': (
                'Dark chocolate at 70%+ cacao contains tannin '
                '(proanthocyanidins) at levels comparable to '
                'red wine — the Vintage Port tannin-bridges '
                'with the chocolate tannin in a shared phenolic '
                'register, while the Port residual sugar balances '
                'the chocolate bitterness. The Touriga Nacional '
                'dark-chocolate ester compound in the Niepoort '
                '2011 creates a within-compound aromatic bridge '
                'with the cocoa aromatics of high-cacao chocolate.'
            )
        }
    ],
    'source': 'IVDP (Instituto dos Vinhos do Douro e Porto) Vintage Port declaration records 2011; Niepoort Vinhos technical documentation; Mayson Richard — Port and the Douro; Robinson Jancis Oxford Companion to Wine (Vintage Port entry); Wine Spectator 2011 Vintage Port assessment; Symington Family Estates 2011 harvest report',
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
