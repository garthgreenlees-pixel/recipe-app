import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='São Tomé and Príncipe — Príncipe Island (Monte Café Arabica, Colonial Roça System, Biosphere Reserve Coffee)',
    output_dir='.',
    starting_entry=1,
    session_number=87,
    running_total=0
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Claudio Corallo / Monte Café Estate (Roça system heritage)',
    'location': 'Príncipe Island and São Tomé Island, São Tomé and Príncipe',
    'country': 'São Tomé and Príncipe',
    'region': 'Príncipe Island — UNESCO Biosphere Reserve',
    'key_person': 'Claudio Corallo (the defining producer for São Tomé fine coffee and chocolate revival)',
    'founded': 'Monte Café estate: 18th century colonial roça; Claudio Corallo on São Tomé from 1993',
    'production_volume': 'Claudio Corallo: approximately 15–20 tonnes per year (both coffee and cocoa); total STP coffee production: 150–300 tonnes per year across all producers',
    'notable_products': [
        'Claudio Corallo Príncipe single-origin Arabica',
        'Monte Café single-origin Arabica (estate revival brand)',
        'Corallo 73% dark chocolate (São Tomé origin cocoa)',
    ],
    'certifications': ['Organic (informal practice — no synthetic inputs due to geographic isolation)', 'Príncipe Island UNESCO Biosphere Reserve'],
    'website': 'claudiocorallo.com',
    'philosophy': (
        'Claudio Corallo arrived in São Tomé in 1993 after 15 years '
        'of cacao work in Zaire (DRC) and began the systematic '
        'revival of the colonial roça estate Arabica production '
        'that had collapsed after Portuguese colonial departure '
        'in 1975. His production model — hand-selecting ripe '
        'cherries from trees that have been growing without '
        'chemical input for decades, natural and honey processing '
        'on raised beds, and direct-trade export — established '
        'São Tomé as a specialty coffee origin of international '
        'significance for the first time in the post-colonial era.'
    ),
    'trail_connection': 'PCT (São Tomé and Príncipe colonial node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'São Tomé Príncipe Monte Café Arabica — Colonial Roça Estate, '
        'Biosphere Reserve Single Origin, Equatorial Atlantic Island '
        'Terroir, PCT Gulf of Guinea Coffee Heritage'
    ),
    'tradition': 'coffee',
    'sub_tradition': 'single-origin Arabica — equatorial volcanic island, roça estate revival, natural/honey process',
    'region': 'São Tomé and Príncipe — Príncipe Island (Monte Café Arabica, Colonial Roça System, Biosphere Reserve Coffee)',
    'terroir_origin': (
        'São Tomé and Príncipe is a microstate consisting of two '
        'volcanic islands in the Gulf of Guinea at 0°N latitude — '
        'São Tomé Island (859km²) and the smaller Príncipe Island '
        '(139km²) — straddling the equator 300km from the Gabon '
        'coast of Central Africa. Both islands are remnants of '
        'the ancient Cameroon Volcanic Line hotspot chain, with '
        'soils dominated by deeply weathered basalt and '
        'ferralitic clay — iron-rich, extremely porous, '
        'and hypermineral. Príncipe Island has been designated '
        'a UNESCO Biosphere Reserve since 2012, with '
        'approximately 70% of the island remaining in '
        'primary forest; the coffee cultivation is '
        'concentrated in the roça (colonial estate) '
        'clearings and forest margins at 300–800m altitude, '
        'where the Atlantic humidity from the Gulf of Guinea '
        '(annual rainfall 1,500–3,000mm, concentrated '
        'April–September with a dry Gravana season '
        'July–September) sustains year-round coffee '
        'cultivation without irrigation. The equatorial '
        'altitude terroir of São Tomé and Príncipe '
        'is distinct from East African high-altitude '
        'growing regions: at 0°N latitude, there '
        'is no defined annual season — the trees '
        'flower and fruit continuously throughout '
        'the year, producing three harvests per '
        'year (March, July, November) rather than '
        'a single annual harvest. The Monte Café '
        'estate on São Tomé Island — a historic '
        'colonial roça at 800m altitude on the '
        'north slopes of the island — was the '
        'flagship coffee production estate '
        'of the Portuguese colonial administration '
        'from the 18th century until nationalization '
        'in 1975; it has been partially revived '
        'under the post-colonial STP government '
        'and represents the historical anchor '
        'of the STP coffee tradition.'
    ),
    'production_technique': (
        'The São Tomé and Príncipe colonial coffee production '
        'system was built around the roça — a large estate '
        'system established by Portuguese colonial administration '
        'from the 17th century onward, using forced and '
        'contract labour from West Africa and the Azores '
        'to cultivate cacao, coffee, and palm oil at industrial '
        'scale. The collapse of the roça system after '
        'independence in 1975 left the estates in decay, '
        'and the coffee production fell from the colonial '
        'peak of several hundred tonnes per year to near '
        'zero by the 1980s. The contemporary São Tomé coffee '
        'revival, led by producers like Claudio Corallo on '
        'Príncipe Island, begins with the existing estate trees '
        '— many of which are Amelonado Arabica (the same '
        'Bourbon-lineage Arabica used in São Tomé cacao '
        'cultivation) that have been growing without '
        'chemical input for 30–50 years since the '
        'colonial collapse, producing naturally low-yield, '
        'high-complexity fruit from decades of adaptation '
        'to the volcanic forest ecosystem. Corallo\'s '
        'production protocol: selective hand-picking of '
        'fully ripe red (or yellow, depending on variety) '
        'cherries at the three annual harvest periods; '
        'honey processing (pulped-natural — the mucilage '
        'is left intact on the parchment and the cherry '
        'is dried with the mucilage still attached); '
        'raised bed drying in the equatorial sun and '
        'shade (at 0°N latitude, sun intensity is '
        'constant year-round, requiring careful bed '
        'management to prevent over-drying); 3–4 '
        'weeks drying time; wet milling at Corallo\'s '
        'Príncipe facility; hand-sorting for defects; '
        'export as green bean to direct-trade buyers '
        'in Europe and North America. The STP coffee '
        'is among the few origins worldwide where '
        'the producer is also the master chocolatier — '
        'Corallo processes the same estate\'s cacao '
        'into single-origin chocolate in the same '
        'facility, creating a dual heritage of '
        'tree-to-cup coffee and bean-to-bar chocolate '
        'from the same equatorial volcanic island estate.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'coffee — Cape Verde Brava and Fogo Islands (Atlantic volcanic, Portuguese colonial)',
            'beverage': 'Cape Verde Brava Island Arabica — Volcanic Ridge, Atlantic Isolation, PCT Atlantic Coffee',
            'connection': (
                'São Tomé Príncipe Arabica and Cape Verde Brava Island '
                'Arabica are the two arms of the Portuguese colonial '
                'Atlantic island coffee introduction narrative — both '
                'established through the same Portuguese colonial '
                'agricultural expansion that created the PCT spice '
                'and commodity trade corridors in the 16th–18th '
                'centuries. Both use volcanic basalt-derived soils '
                'with Atlantic isolation terroir; both maintain '
                'essentially wild-growing, low-input Arabica '
                'populations that have adapted to their '
                'specific island microclimate over three '
                'centuries without mainland cross-pollination. '
                'The sensory divergence: São Tomé grows at '
                'equatorial 0°N with full tropical humidity '
                'producing a heavier-bodied, more tropical-fruit '
                'forward cup; Brava grows at 14°N subtropical '
                'Atlantic with trade-wind aridity producing '
                'a lighter-bodied, more mineral cup. '
                'Together they bracket the latitudinal '
                'range of the Atlantic island coffee terroir '
                'established by the Portuguese colonial trade.'
            )
        },
        {
            'tradition': 'chocolate — São Tomé Príncipe cocoa (same estate, same roça, same volcanic island)',
            'beverage': 'Claudio Corallo São Tomé 73% Dark Chocolate — Roça Estate Cacao, Equatorial Volcanic Terroir',
            'connection': (
                'The most distinctive parallel in the PCT system: '
                'São Tomé coffee and São Tomé chocolate are '
                'produced from the same estate, in the same '
                'volcanic soil, by the same producer (Claudio '
                'Corallo on Príncipe), using the same minimal-'
                'intervention approach to agricultural production '
                'and fermentation/drying processing. Both the '
                'coffee cherry and the cacao pod express the '
                'same equatorial Gulf of Guinea terroir through '
                'different crop biology — the fermentation-derived '
                'acidity of the cacao processing parallels the '
                'honey-process development of the coffee cherry; '
                'both carry the characteristic tropical stone '
                'fruit (mango, jackfruit, passion fruit) aromatic '
                'register of the São Tomé Biosphere Reserve '
                'microclimate. The within-origin pairing of '
                'São Tomé single-origin coffee with São Tomé '
                'single-origin chocolate (both Corallo estate) '
                'is the definitive expression of the equatorial '
                'Atlantic island terroir as a unified agricultural '
                'system — the same volcanic mineral base '
                'expressed through two completely different '
                'production paths.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'The green bean: medium to large-sized (screen 16–18), '
            'irregular shape (the multi-harvest equatorial '
            'cultivation produces variable cherry size), '
            'medium-green with a yellowish cast from the '
            'honey-process mucilage residue; the roasted bean '
            'at full-city medium-dark (Corallo\'s recommended '
            'roast for STP Arabica): warm mahogany with '
            'very slight surface oil indicating full '
            'development without charring; the espresso '
            'crema is thick and dark brown-amber, '
            'reflecting the high melanoidin concentration '
            'from the equatorial honey-process development.'
        ),
        'nose': (
            'The defining STP aromatic register is the tropical '
            'stone fruit signature of the honey-process equatorial '
            'Arabica: passion fruit, dried mango, jackfruit, '
            'and ripe banana from the mucilage-fermentation '
            'compounds retained on the bean through the '
            'honey process; dark chocolate from the '
            'volcanic mineral richness and the full-city '
            'roast development — a reminder of the '
            'same estate\'s cacao processing heritage; '
            'a characteristic "forest floor" earthy '
            'note from the Biosphere Reserve forest '
            'margin cultivation (the shading trees '
            'contribute leaf-litter and fungal aromatic '
            'precursors to the coffee cherry through '
            'the porous volcanic soil drainage); '
            'brown sugar and molasses sweetness from '
            'the honey process caramelisation; '
            'very low acidity in the aromatic register '
            '(the equatorial cultivation and honey '
            'process produce a low-acid cup compared '
            'to East African high-altitude washed).'
        ),
        'palate': (
            'Full, velvety body from the honey-process development '
            'and the equatorial Arabica density — significantly '
            'heavier body than comparable East African '
            'washed coffees; the entry is immediately '
            'tropical-fruit forward (passion fruit, mango, '
            'dried stone fruit) dissolving into the '
            'dark chocolate mid-palate; low but '
            'perceived acidity (malic and citric acids '
            'at low concentration from the honey-process '
            'fermentation) provides a gentle brightness '
            'that prevents the tropical fruit heaviness '
            'from dominating; the volcanic mineral character '
            '— iron-rich, slightly saline, oceanic — '
            'emerges at mid-to-finish and provides the '
            'terroir signature that distinguishes STP '
            'from mainland African or Latin American '
            'tropical naturals; the finish is long '
            '(35–50 seconds) with dark chocolate, '
            'dried mango, and the lingering forest-floor '
            'earthy note of the Biosphere Reserve '
            'shade-grown cultivation.'
        ),
        'conclusion': (
            'The most complete expression of the equatorial '
            'Atlantic volcanic island terroir in beverage form: '
            'the same geological system, the same Portuguese '
            'colonial agricultural heritage, and the same '
            'minimal-intervention production approach that '
            'defines Corallo\'s São Tomé chocolate — '
            'expressed through the coffee tree.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Claudio Corallo Príncipe single-origin Arabica '
                '(direct-trade, identified roça estate, honey process, '
                'raised-bed dried, hand-sorted) — the benchmark for '
                'STP fine coffee; consistently scoring 85–88 at SCA '
                'protocol cupping; limited production (under 5 tonnes '
                'per year); available only through Corallo\'s direct '
                'trade network and specialist international importers; '
                'priced at USD $35–50 per 250g bag internationally.'
            ),
            'markers': (
                'Corallo estate label; Príncipe Island origin; honey process; '
                'raised-bed drying; hand-sorted; SCA 85+ score; '
                'equatorial volcanic mineral profile.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Monte Café estate São Tomé Arabica — the historic '
                'roça revival brand under the STP government '
                'cooperative programme; identified estate origin; '
                'natural or honey process; hand-picked; less '
                'rigorous defect sorting than Corallo; '
                'priced at USD $15–25 per 250g through '
                'European specialty importers; the accessible '
                'reference for São Tomé single-origin at the '
                'estate tier.'
            ),
            'markers': (
                'Monte Café label; São Tomé island origin; '
                'natural or honey process; cooperative '
                'production; European specialty distribution.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'STP archipelago blended commercial coffee (roasting '
                'in Portugal or Netherlands from STP green bean '
                'purchased through commercial channels without '
                'estate-specific selection) — recognisably STP '
                'tropical character but without the volcanic '
                'mineral precision of the estate tiers; '
                'available through Portuguese speciality '
                'food retailers and African goods importers; '
                'priced at USD $10–15 per 250g.'
            ),
            'markers': (
                'STP archipelago blend; commercial roast; '
                'no estate identification; European roasting; '
                'tropical fruit character without mineral depth.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Commercial robusta or blended coffee sold in '
                'STP domestic market under local brands — '
                'the domestic market is dominated by instant '
                'and commercial roasted coffee due to the '
                'limited domestic purchasing power and the '
                'historical export orientation of the '
                'colonial production system; the local '
                'everyday coffee has limited connection '
                'to the fine Arabica tradition of the '
                'estate revival producers.'
            ),
            'markers': (
                'Commercial blend; robusta component; '
                'domestic STP market; no estate connection.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'The Claudio Corallo STP Arabica performs best at a '
            'medium-dark full-city roast extracted as espresso '
            '(93°C, 25–28 second pull, 7–8g dose for 25–30ml) — '
            'the equatorial honey-process development produces '
            'a thick, sweet espresso with prominent tropical '
            'fruit in the crema that is the standard reference '
            'service for this origin. For filter evaluation '
            'of the volcanic mineral terroir character: '
            'V60 pour-over at 91–93°C, 60g per litre, '
            '3–4 minute total brew time — the lighter '
            'filter extraction preserves the passion '
            'fruit and volcanic mineral character that '
            'the espresso concentration can overwhelm. '
            'Do not serve cold brew — the low-temperature '
            'extraction suppresses the volatile tropical '
            'aromatics that are the defining character '
            'of this origin.'
        ),
        'vessel': (
            'Espresso service: a pre-warmed white ceramic '
            'demitasse (60–80ml) with the crema served '
            'immediately on pulling; for the PCT programme '
            'context, serve alongside a square of Claudio '
            'Corallo 73% São Tomé dark chocolate on the saucer '
            '— the within-origin pairing of coffee and chocolate '
            'from the same estate is the defining PCT service '
            'moment for the Gulf of Guinea node. The chocolate '
            'should be placed on the saucer before the espresso '
            'is pulled so that the guest\'s first sensory '
            'interaction is the São Tomé cacao aroma before '
            'the coffee arrives — the aromatic comparison '
            'illuminates both products simultaneously.'
        ),
        'technique': (
            'Espresso at full-city roast; or V60 at 91–93°C '
            'for mineral terroir evaluation. '
            'Always serve with Corallo STP chocolate in programme context. '
            'Describe the roça system, the 1975 colonial collapse, '
            'and the estate revival as the essential narrative.'
        ),
        'programme_position': (
            'PCT equatorial Atlantic island coffee flight: serve '
            'alongside Brava Island Arabica (pct_82) and '
            'with Corallo São Tomé dark chocolate for the '
            'definitive within-origin coffee-chocolate pairing '
            'of the PCT system; or in a volcanic terroir '
            'comparison alongside Ethiopian Yirgacheffe '
            '(basalt), Hawaiian Kona (volcanic), and '
            'Fogo Island Cape Verde (basalt) to demonstrate '
            'how volcanic geology shapes coffee character '
            'across different latitudes.'
        ),
        'verbal_presentation': (
            'The same equatorial island. The same volcanic soil. '
            'The coffee tree and the cacao tree. Both from '
            'the same colonial estate system that the '
            'Portuguese built here with forced labour '
            'three centuries ago. Claudio Corallo '
            'arrived after independence with two hands '
            'and no machine and brought both back. '
            'Eat the chocolate. Then drink the coffee. '
            'Same mountain. Same tree. Same ground.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Claudio Corallo, Príncipe Island, São Tomé and Príncipe '
            '(established coffee and chocolate on Príncipe from 1993 — '
            'the benchmark for STP fine coffee and the direct-trade '
            'reference for international buyers; his production '
            'defined the international recognition of STP '
            'as a specialty coffee and fine chocolate origin; '
            'claudiocorallo.com for direct contact and '
            'distribution).'
        ),
        'producer_location': 'Príncipe Island and São Tomé Island, São Tomé and Príncipe',
        'key_person': 'Claudio Corallo',
        'production_volume': '15–20 tonnes/year (coffee + cocoa combined)',
        'certifications': ['Organic (de facto — no synthetic inputs)', 'Príncipe UNESCO Biosphere Reserve'],
        'bc_distributor': '[PROVIDER: verify — Corallo chocolate is distributed by specialty food importers in North America; coffee lots are rare; check Beanworks Coffee or specialty African origins importers in Vancouver]',
        'us_distributor': '[PROVIDER: verify — Corallo has a US importer; check claudiocorallo.com for current US distribution contact]',
        'uk_distributor': 'Has Bean Coffee (UK) has carried Corallo STP in the past; verify current stock; Volcano Coffee Works may carry',
        'price_tier': 'Reserve',
        'availability_notes': (
            'Corallo Príncipe Arabica is available in very limited '
            'quantities through direct-trade European and North American '
            'specialty importers and through claudiocorallo.com. '
            'The green bean appears occasionally at major specialty '
            'coffee auctions (Cup of Excellence does not operate '
            'in STP; check direct from Corallo for current crop '
            'availability). Monte Café estate coffee is available '
            'through Portuguese specialty food retailers (Celeiro, '
            'El Corte Inglés) and through European African '
            'specialty food importers. International price: '
            'USD $30–50 per 250g for Corallo Príncipe; '
            'USD $15–25 for Monte Café estate expression.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'São Tomé and Príncipe is the equatorial Atlantic pivot of '
        'the Portuguese Colonial Trail — the islands were the first '
        'sugar-producing colony of the Portuguese Empire (from 1485) '
        'and the transit point for West African forced labour '
        'that would go on to populate Brazil, the Caribbean, '
        'and the Gulf of Guinea coast. The coffee and cacao '
        'cultivated on the same colonial roça estates '
        'that were built by that forced labour are the '
        'agricultural legacy of the PCT at its most '
        'historically complex — the plant material, '
        'the estate system, and the export infrastructure '
        'are all colonial creations now operating as '
        'a post-colonial specialty food revival through '
        'the ethical direct-trade model of Claudio Corallo.'
    ),
    'food_pairings': [
        {
            'technique_id': 'STP-001',
            'dish': 'Claudio Corallo 73% São Tomé dark chocolate (same estate)',
            'pairing_type': 'complement',
            'rationale': (
                'The definitive within-origin pairing: both the '
                'coffee and the chocolate are produced from the '
                'same volcanic basalt soil on the same equatorial '
                'island by the same producer; the passion fruit '
                'and dried mango of the coffee honey-process '
                'mirrors the fermentation-derived tropical '
                'fruit character of the cacao; the dark '
                'chocolate bitterness is the mirror of the '
                'espresso bitterness — together they produce '
                'a sensory doubling of the volcanic terroir '
                'through two different plant metabolisms.'
            )
        },
        {
            'technique_id': 'STP-002',
            'dish': 'Calulu de peixe (STP dried fish and okra stew with palm oil)',
            'pairing_type': 'bridge',
            'rationale': (
                'The full-body, low-acid STP espresso bridges to '
                'the palm oil richness and dried fish umami of '
                'calulu — the dominant STP national dish — '
                'through the shared tropical agricultural terroir '
                'of the same equatorial island; the coffee\'s '
                'low acidity prevents the citrus clash that '
                'higher-acid East African coffees would produce '
                'with the palm oil base.'
            )
        }
    ],
    'source': 'Claudio Corallo production documentation (claudiocorallo.com); UNESCO Príncipe Biosphere Reserve documentation; Sweet Maria\'s Library STP origin notes; SCA cupping protocol records for STP entries; Francesc Guillen roça historical research',
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
