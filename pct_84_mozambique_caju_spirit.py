import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Mozambique — Gaza Province (Caju Spirit, Cashew Apple Distillate, Southern African Colonial Fruit Spirit Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=88,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Gaza Province Small Producers (various family-operated distilleries)',
    'location': 'Xai-Xai and surrounding districts, Gaza Province, southern Mozambique',
    'country': 'Mozambique',
    'region': 'Gaza Province, Inhambane Province — southern Mozambique cashew belt',
    'key_person': 'Various smallholder family distillery operators; no single commercial benchmark producer has been internationally documented',
    'founded': '17th century Portuguese colonial introduction of cashew (Anacardium occidentale) to southern Africa; continuous family distillation tradition',
    'production_volume': 'Total southern Mozambique caju spirit production estimated at several hundred thousand litres per year; primarily domestic consumption in the cashew-growing provinces',
    'notable_products': [
        'Caju spirit (unaged cashew apple distillate, 40–60% ABV)',
        'Caju wine (fermented cashew apple, 3–6% ABV, pre-distillation base)',
    ],
    'certifications': [],
    'website': '[PROVIDER: no commercial website — no internationally recognised branded caju spirit producer has been identified; domestic production only]',
    'philosophy': (
        'The Mozambique caju spirit tradition is a subsistence-to-market '
        'agricultural distillation practice maintained by cashew-farming '
        'families in Gaza and Inhambane provinces, where the cashew '
        'apple (the fleshy peduncle of the cashew tree, not the nut) '
        'is fermented and distilled into a spirit using the same copper '
        'pot still technology introduced by the Portuguese colonial '
        'administration in the 17th century — the same colonial '
        'distillation transfer that produced Goa feni from the '
        'same species of cashew tree on the Indian Ocean\'s '
        'eastern shore.'
    ),
    'trail_connection': 'PCT (Mozambique — Indian Ocean corridor)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Mozambique Caju Spirit — Cashew Apple Distillate, Gaza Province '
        'Southern Cashew Belt, Colonial Copper Pot Still Heritage, '
        'Indian Ocean PCT Parallel with Goa Feni'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'cashew_spirit — cashew apple fermentation and pot still distillation',
    'region': 'Mozambique — Gaza Province (Caju Spirit, Cashew Apple Distillate, Southern African Colonial Fruit Spirit Heritage)',
    'terroir_origin': (
        'Mozambique is among the five largest cashew producers '
        'in the world by nut volume, with the cashew tree '
        '(Anacardium occidentale) widely cultivated across '
        'the coastal provinces of Gaza, Inhambane, Sofala, '
        'and Nampula. The cashew was introduced to '
        'Mozambique by Portuguese colonial administration '
        'from Brazil (where it is native to the northeastern '
        'coast) in the 17th century — part of the same '
        'Columbian Exchange agricultural transfer that '
        'introduced cashew to India via Goa in the '
        'same period, creating the shared botanical '
        'foundation for both Mozambique caju spirit '
        'and Goan cashew feni from the same species. '
        'The cashew apple (caju or cajú in Portuguese '
        'and local Mozambican languages including '
        'Tsonga and Changana) is the swollen floral '
        'peduncle — the fleshy, astringent, juice-rich '
        'fruit that grows beneath the cashew nut; '
        'it is not botanically a true fruit but a '
        'pseudo-fruit that develops from the flower '
        'stem. In Mozambique\'s Gaza Province, the '
        'cashew apple season runs from October to '
        'December (southern hemisphere spring-summer) '
        'when the cashew trees fruit simultaneously '
        'across the semi-arid savanna landscape '
        'between the coast and the Limpopo River. '
        'The soils of Gaza Province are predominantly '
        'sandy Arenosols with some clay-loam Luvisols '
        'in the alluvial Limpopo flood zones — '
        'well-draining, low-nutrient soils that '
        'stress the cashew trees into producing '
        'high-sugar-concentration apples with '
        'intense tannin and astringency, the same '
        'characteristics that make the cashew apple '
        'ideal for fermentation and distillation '
        'despite its aggressive raw astringency '
        'when consumed fresh.'
    ),
    'production_technique': (
        'The Mozambique caju spirit production begins with the '
        'collection of ripe cashew apples at the base of the '
        'cashew trees — the apples fall naturally when fully '
        'ripe (the attached cashew nut is harvested separately '
        'for commercial export; the apple is the agricultural '
        'byproduct of nut production). The ripe cashew apples '
        'are collected in baskets and transported to the '
        'family distillery compound within hours of falling, '
        'as the high natural sugar (8–12% fructose and glucose) '
        'combined with the wild yeast populations on the '
        'apple skin begins spontaneous fermentation immediately '
        'at the ambient Gaza temperature of 28–36°C. '
        'The apples are pressed manually (foot-treading '
        'in large wooden or concrete vats, or by simple '
        'mechanical press) to extract the juice — the '
        'pressing requires care to avoid excessive '
        'tannin extraction from the skin, as the cashew '
        'apple tannin (urushiol and anacardic acid compounds) '
        'at high concentration produces an aggressively '
        'astringent spirit that is unmarketable even '
        'in the domestic context. The freshly pressed '
        'cashew apple juice (clarified by gravity settling '
        'for 12–24 hours) is inoculated with the wild '
        'yeast population from the previous batch\'s '
        'spent press cake (the traditional back-slop '
        'method equivalent to the dunder method in '
        'Caribbean rum) and fermented in open wooden '
        'or clay vats for 3–5 days at ambient temperature. '
        'The fermented caju wine (3–6% ABV) is then '
        'distilled in a simple copper pot still — '
        'the standard Portuguese colonial copper '
        'alambique design, introduced by Portuguese '
        'colonial agriculture extension services '
        'and now manufactured locally by Mozambican '
        'coppersmiths from recycled industrial copper '
        'sheet — to produce the caju spirit at '
        '40–60% ABV in a single distillation run. '
        'The spirit is bottled immediately in '
        'used glass bottles (including recycled '
        'commercial beer and wine bottles) '
        'without aging, filtration, or any '
        'additive — raw from the still to '
        'local market sale or family consumption. '
        'Total production per family operation: '
        '50–500 litres per cashew season; '
        'multiple families in each Gaza '
        'village participate, making '
        'the caju spirit the dominant '
        'agricultural spirit of southern '
        'Mozambique by volume.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Goa cashew feni (India, the parallel Indian Ocean expression)',
            'beverage': 'Goa Cashew Feni — Anacardium occidentale Apple Distillation, Copper Bhann, Triple Distillation',
            'connection': (
                'Mozambique caju spirit and Goa cashew feni are the '
                'two primary expressions of a single PCT botanical '
                'narrative: both distill the cashew apple '
                '(Anacardium occidentale) through copper pot '
                'still technology introduced by Portuguese colonial '
                'administration from the same Brazilian original '
                'plant material to two opposite shores of the '
                'Indian Ocean — Goa on the eastern shore (PCT-8 '
                'Indian node) and Mozambique on the western shore '
                '(PCT Mozambique node). The botanical identity '
                'is the same species; the production distinction '
                'is the distillation sophistication: Goa feni '
                'is triple-distilled to a defined 40–45% ABV '
                'spirit with GI protection (2009) and a '
                'defined tasting standard; Mozambique caju '
                'spirit is single-distilled to variable ABV '
                'without regulatory framework or GI protection, '
                'consumed entirely in the domestic market without '
                'international commercial presence. The PCT '
                'narrative arc: both spirits trace to the same '
                'botanical source (Amazonian northeast Brazil), '
                'transmitted by the same colonial power '
                '(Portugal) through the same trade route '
                '(the eastern-western Indian Ocean corridor) '
                'to produce two expressions that are '
                'genetically identical in raw material '
                'but culturally and technically divergent.'
            )
        },
        {
            'tradition': 'spirits — urrak (cashew spirit, single distillation Goa pre-feni)',
            'beverage': 'Goa Urrak — Single Distillation Cashew Apple, Agricultural Worker Spirit, Pre-Feni Expression',
            'connection': (
                'Mozambique caju spirit and Goa urrak (the single-'
                'distillation cashew spirit, the precursor step '
                'before the triple-distillation that produces '
                'true feni) are the most precise technical '
                'parallel in the PCT spirits system: both are '
                'single-distillation products from fermented '
                'cashew apple juice, both are consumed primarily '
                'by the agricultural community that produces them '
                'rather than for export, and both operate at '
                'variable ABV (15–40%) without the standardisation '
                'that triple-distillation and GI regulation '
                'impose on the Goa feni category. '
                'The Mozambique caju spirit is, in production '
                'technical terms, the functional equivalent '
                'of Goa urrak — a single-pass cashew apple '
                'distillate consumed domestically as an '
                'agricultural byproduct spirit in the '
                'same way that urrak is consumed by '
                'Goa\'s cane and cashew farmers before '
                'the surplus is redistilled into feni '
                'for the commercial market.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Water-clear to very pale yellow — the spirit is '
            'unaged and bottled directly from the still '
            'with minimal resting; the clarity varies '
            'by producer and filtration practice; '
            'some domestic Gaza Province caju spirit '
            'shows a slight natural haze from the '
            'tannin-rich cashew apple compounds '
            'retained through minimal filtration; '
            'the high ABV (often 50–60% for the '
            'most assertive expressions) produces '
            'pronounced legs and tears in the glass.'
        ),
        'nose': (
            'The defining aromatic of cashew apple distillate '
            'is ethyl caproate and ethyl caprate — the medium-'
            'chain fatty acid ethyl esters that produce '
            'the characteristic apple-pear ester register '
            'of cashew fermentation; unlike coconut feni '
            '(delta-decalactone dominant), cashew feni '
            'and Mozambique caju spirit share the same '
            'ester profile: fruity, apple-pear, with '
            'a distinctive "green mango" or "cashew '
            'fruit" freshness from the anacardic acid '
            'volatile compounds of the cashew apple '
            'skin; beneath, a light astringency from '
            'the urushiol derivatives retained in '
            'the spirit (at trace levels — above '
            'trace, urushiol is an allergen and '
            'toxic compound, but at the levels '
            'present in properly managed cashew '
            'apple spirit it contributes only '
            'an aromatic dryness); higher-proof '
            'expressions show prominent fusel '
            'alcohol from the single-distillation '
            'heads integration; the overall '
            'aromatic is raw and agricultural, '
            'immediately distinct from any '
            'barrel-aged or industrial spirit.'
        ),
        'palate': (
            'At 40–50% ABV: medium body; the entry '
            'is immediately defined by the apple-pear '
            'ester character — the ethyl caproate '
            'cashew apple register — dissolving into '
            'the raw spirit warmth; the mid-palate '
            'develops the astringent-dry character '
            'of the cashew tannin compounds that '
            'persist from the pressing; the finish '
            'is medium-short (15–25 seconds) with '
            'cashew apple freshness and persistent '
            'ester warmth; at 50–60% ABV '
            '(the stronger expressions): more '
            'pronounced fusel heat, the ester '
            'character more concentrated, and '
            'the cashew tannin astringency more '
            'assertive; water dilution to 40% '
            'before service is strongly advised '
            'for the higher-proof expressions; '
            'the traditional Gaza Province service '
            'is neat at ambient temperature (32–36°C) '
            'as a midday agricultural break drink, '
            'not a sipping experience in the '
            'connoisseur sense.'
        ),
        'conclusion': (
            'The Mozambique caju spirit is a direct-from-agricultural-'
            'byproduct distillate without commercial polish or '
            'regulatory framework — its significance is historical '
            'and botanical (the Indian Ocean cashew-apple-spirit '
            'parallel to Goa feni) rather than in the conventional '
            'quality register of fine spirits.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'There is no established international commercial '
                'reserve tier for Mozambique caju spirit at this '
                'time (2026). A potential future benchmark would '
                'be a double-distilled, controlled-fermentation, '
                'identified-estate caju spirit from Gaza or '
                'Inhambane Province marketed through a formal '
                'producer with verifiable GI compliance — '
                'the technical parallel to what Goa achieved '
                'with the feni GI in 2009 applied to the '
                'Mozambique tradition. Until such a producer '
                'emerges with international export capability, '
                'the Reserve tier is occupied by the '
                'highest-quality domestic production from '
                'identified family distilleries with '
                'documented provenance.'
            ),
            'markers': (
                'Double-distillation (if available); identified producer; '
                'controlled tannin extraction; clean ester profile; '
                'verifiable Gaza Province origin.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Single-distillation caju spirit from identified '
                'Gaza Province family producers with controlled '
                'fermentation (timed, temperature-managed in '
                'covered vessels) and careful pressing (low '
                'tannin extraction); ABV 40–48%; clean apple '
                'ester character without excessive fusel '
                'alcohol from heads integration; the professional '
                'domestic tier for Mozambican hospitality industry '
                'buyers who understand the tradition and select '
                'premium family producers.'
            ),
            'markers': (
                'Identified family producer; controlled fermentation; '
                'careful pressing; clean ester profile; '
                '40–48% ABV; domestic Mozambique hospitality '
                'industry distribution.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Standard Gaza Province village caju spirit — '
                'single distillation from open vat fermentation '
                'with variable tannin extraction and variable ABV '
                '(40–60%); authentic but inconsistent; the '
                'dominant form of the tradition as consumed '
                'by the agricultural community; priced at '
                'MZN 50–150 per litre (USD $0.80–2.40) '
                'in local village markets.'
            ),
            'markers': (
                'Variable ABV; open vat fermentation; '
                'single distillation; village market sale; '
                'inconsistent tannin management.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Improperly processed caju spirit with high '
                'tannin extraction (from over-pressing the '
                'cashew apple skin and kernel) producing '
                'urushiol astringency at uncomfortable levels; '
                'or high-fusel spirit from poorly managed '
                'single-pass distillation without adequate '
                'heads removal; the problematic expressions '
                'that give caju spirit a poor reputation '
                'in Mozambican urban markets; these can '
                'cause gastric discomfort at high consumption '
                'due to anacardic acid and urushiol retention.'
            ),
            'markers': (
                'Harsh astringency; high fusel alcohol; '
                'heads contamination; gastric irritant potential; '
                'avoid in any programme context.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Mozambique caju spirit has no established international '
            'professional service protocol — as a domestic '
            'agricultural spirit, it is consumed at ambient '
            'Gaza Province temperature (28–36°C) without '
            'temperature management. For a PCT programme '
            'presentation that places caju spirit in its '
            'Indian Ocean context: serve a small measure '
            '(15–20ml) diluted to 40% ABV with still water '
            'at 22–24°C in a small Glencairn or copita, '
            'alongside a comparative pour of Goa cashew '
            'feni (same ABV, same raw material, triple '
            'distillation) — the comparison illuminates '
            'the impact of distillation sophistication '
            'on the same botanical source better than '
            'any description.'
        ),
        'vessel': (
            'For PCT programme comparison: small Glencairn '
            '(50–75ml) with 15–20ml diluted pour; '
            'present in a two-glass flight with Goa '
            'cashew feni, labelled with the origin '
            'and the distillation method (single vs. triple) '
            'to make the comparison explicit. '
            'In the Mozambique domestic service context: '
            'a simple glass (any available) or '
            'a calabash at ambient temperature '
            '— the agricultural break context '
            'is as important to communicate as '
            'the liquid character for international '
            'programme audiences unfamiliar '
            'with the tradition.'
        ),
        'technique': (
            'Always dilute to 40% for programme service. '
            'Present alongside Goa cashew feni for the '
            'PCT Indian Ocean parallel. '
            'Describe the Columbian Exchange botanical '
            'transmission: Brazil → Goa → Mozambique '
            'via Portuguese colonial trade.'
        ),
        'programme_position': (
            'PCT Indian Ocean spirits comparative flight: '
            'Mozambique caju (western shore) — Goa cashew feni '
            '(eastern shore) — South Goa coconut feni '
            '(third plant species comparison); '
            'the three-glass flight demonstrates the '
            'botanical and PCT historical '
            'connections across the Indian Ocean.'
        ),
        'verbal_presentation': (
            'The same cashew tree. The same copper pot still. '
            'One on the coast of Goa, one on the coast of '
            'Mozambique. Both sides of the Indian Ocean. '
            'Both reached by the same Portuguese ship '
            'in the same century. The nut went to market. '
            'The apple became the spirit.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'No internationally documented commercial benchmark '
            'producer exists for Mozambique caju spirit (2026). '
            'The tradition is entirely domestic and subsistence-scale. '
            'For programme sourcing, the closest available '
            'Indian Ocean cashew spirit with verifiable '
            'international distribution is Cazulo Premium '
            'Cashew Feni from Goa — which shares the same '
            'botanical source and serves as the commercial '
            'benchmark for the cashew apple distillation '
            'tradition that Mozambique caju spirit '
            'represents at its pre-commercial stage.'
        ),
        'producer_location': 'Gaza Province and Inhambane Province, southern Mozambique',
        'key_person': '[PROVIDER: no internationally documented individual producer]',
        'production_volume': 'Several hundred thousand litres per year domestic; no export volume',
        'certifications': [],
        'bc_distributor': '[NOT AVAILABLE: Mozambique caju spirit has no international commercial distribution as of 2026; for programme use, substitute Cazulo Premium Cashew Feni (Goa) as the botanical parallel]',
        'us_distributor': '[NOT AVAILABLE: same as above]',
        'uk_distributor': '[NOT AVAILABLE: same as above]',
        'price_tier': 'House',
        'availability_notes': (
            'Mozambique caju spirit is available only domestically '
            'in the cashew-growing provinces of Gaza, Inhambane, '
            'Sofala, and Nampula during the October–December '
            'cashew season. It is not commercially exported '
            'and has no international retail presence. '
            'For PCT programme purposes, the tradition '
            'should be documented as a cultural and '
            'botanical reference point within the '
            'Indian Ocean spirits corridor narrative, '
            'with Goa cashew feni (available internationally) '
            'substituting for the actual Mozambique '
            'spirit where physical service is required.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Mozambique caju spirit documents the western Indian Ocean '
        'node of the PCT cashew apple distillation tradition — '
        'the direct complement to Goa feni on the eastern '
        'shore. The botanical transmission route (Brazil → '
        'Portuguese colonial trade → Goa and Mozambique '
        'simultaneously in the 17th century) is one of '
        'the clearest single-species PCT agricultural '
        'heritage narratives in the entire system: '
        'the same tree, the same colonial introduction, '
        'the same Indian Ocean crossing, producing '
        'two spirits that are now separated by culture '
        'and regulatory sophistication (Goa GI-protected '
        'triple-distillation vs. Mozambique domestic '
        'single-distillation) but share the same '
        'Amazonian botanical ancestor and the same '
        'Portuguese copper pot still ancestor.'
    ),
    'food_pairings': [
        {
            'technique_id': 'MOZ-001',
            'dish': 'Matapa (Gaza Province cassava leaf and cashew nut stew with coconut milk)',
            'pairing_type': 'complement',
            'rationale': (
                'The cashew nut in matapa is the commercial '
                'byproduct of the same tree whose apple '
                'produces the caju spirit — a within-species '
                'pairing where the nut and the apple spirit '
                'of Anacardium occidentale meet on the plate; '
                'the coconut milk base of matapa bridges '
                'to the ester character of the caju spirit '
                'through shared tropical agricultural terroir.'
            )
        },
        {
            'technique_id': 'MOZ-002',
            'dish': 'Piri-piri grilled prawns (Mozambique coast — Portuguese colonial spice heritage)',
            'pairing_type': 'cleanse',
            'rationale': (
                'The high ABV and sharp ester character of '
                'Gaza Province caju spirit at working strength '
                'provides an effective palate cleanse of '
                'the piri-piri capsaicin heat and the '
                'prawn iodine — the same function '
                'that Goa feni performs in the '
                'prawn-and-feni pairing of Goan '
                'coastal cuisine, connecting '
                'the two shores of the '
                'Indian Ocean cashew '
                'spirit tradition through '
                'the shared Portuguese '
                'colonial chilli-and-seafood '
                'cuisine vocabulary.'
            )
        }
    ],
    'source': 'CABI Cashew crop international distribution records; FAO Mozambique cashew production data; Goa feni GI documentation (for botanical parallel); INIDA West Africa cashew agricultural heritage research; Hanlon & Smart Mozambique post-war agricultural recovery research',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
