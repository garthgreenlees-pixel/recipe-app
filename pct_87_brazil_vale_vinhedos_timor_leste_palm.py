import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Brazil — Vale dos Vinhedos (Miolo Reserva Especial Branco, Chardonnay and Riesling Itálico, Serra Gaúcha White Wine)',
    output_dir='.',
    starting_entry=1,
    session_number=91,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Miolo Wine Group',
    'location': 'Bento Gonçalves, Rio Grande do Sul, Brazil',
    'country': 'Brazil',
    'region': 'Vale dos Vinhedos DOCG — Serra Gaúcha highlands, Rio Grande do Sul',
    'key_person': 'Adriano Miolo — CEO and second-generation family director; Andrea Miolo — export and marketing director; family founded by Giuseppe Miolo (Italian immigrant, 1897)',
    'founded': '1897 (farming); 1989 (modern winery). The Miolo family traces its presence in Vale dos Vinhedos to the Italian immigrant settlement of the Serra Gaúcha highlands from 1875 onward',
    'production_volume': 'Approximately 10 million litres/year across all Miolo estates (Vale dos Vinhedos, Campanha Gaúcha, and purchased grapes from contracted growers); the DOCG Vale dos Vinhedos tier is a fraction of total production',
    'notable_products': [
        'Miolo Reserva Especial Branco (Chardonnay-Riesling Itálico blend, Vale dos Vinhedos)',
        'Miolo Reserva Especial Tinto (Merlot-Tannat-Cabernet Franc, DOCG Vale dos Vinhedos)',
        'Miolo Lote 43 (premium Merlot-Cabernet Sauvignon blend)',
        'Miolo Cuvée Giuseppe (estate-vineyard single selection)',
        'Miolo Millennium (aged Cabernet Sauvignon, vintage-specific)',
    ],
    'certifications': ['IP Vale dos Vinhedos (Indicação de Procedência)', 'DOCG Vale dos Vinhedos (Denominação de Origem Controlada e Garantida — red wine)'],
    'website': 'www.miolo.com.br',
    'philosophy': (
        'Miolo represents the modern commercial face of Vale dos Vinhedos — '
        'the Italian immigrant family winery that grew from a single-farm '
        'cooperative to Brazil\'s largest premium wine exporter, demonstrating '
        'that South American Italian-settler viticulture can produce wines of '
        'international quality from the same highland soil that their '
        'grandparents cleared for agriculture in the late 19th century.'
    ),
    'trail_connection': 'PCT (Brazil — Italian immigrant wine heritage node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Miolo Reserva Especial Branco — Vale dos Vinhedos DOCG White, '
        'Chardonnay and Riesling Itálico, Serra Gaúcha Highland, '
        'Italian Immigrant Viticulture Legacy'
    ),
    'tradition': 'wine',
    'sub_tradition': 'still white — IP/DOCG Vale dos Vinhedos, Serra Gaúcha highland, Chardonnay-Riesling Itálico blend, volcanic basalt soil',
    'region': 'Brazil — Vale dos Vinhedos (Miolo Reserva Especial Branco, Chardonnay and Riesling Itálico, Serra Gaúcha White Wine)',
    'terroir_origin': (
        'Vale dos Vinhedos (Valley of the Vineyards) occupies '
        'a 82km² sub-region of Serra Gaúcha in the highlands '
        'of Rio Grande do Sul, Brazil\'s southernmost state, '
        'at latitude 29°S and elevation 600–850m above sea '
        'level. The valley was settled by Italian immigrants '
        '(predominantly from the Veneto and Trentino regions '
        'of northern Italy) from 1875 onward — the Brazilian '
        'imperial government recruited Italian agricultural '
        'workers to settle the southern highlands as part of '
        'a colonisation policy for the previously forested '
        'upper plateau. The immigrants brought Vitis vinifera '
        'cuttings from northern Italy alongside traditional '
        'wine production knowledge; the first wine was produced '
        'in the valley in the 1880s. The geology of Serra Gaúcha '
        'is basalt-derived — the Paraná volcanic plateau, '
        'a vast lava field from the Cretaceous period, '
        'underlies the region, with the highland soils '
        'developing as basalt weathers into iron-rich, '
        'well-drained red earth (Terra Roxa, the red soil '
        'that is the signature of Brazilian highland viticulture). '
        'The subtropical highland climate at 600–850m '
        'provides annual rainfall of 1,600–1,800mm '
        '(concentrated in the January–March summer growing '
        'period), temperatures of 16–24°C in the growing '
        'season, and the critical diurnal temperature variation '
        '(10–12°C day-night differential in March–April) '
        'that produces aromatic retention in white varieties. '
        'Chardonnay was introduced to Vale dos Vinhedos in '
        'the 1970s–1980s by the international winery '
        'joint ventures (Moet & Chandon established the '
        'first sparkling wine operation in 1973) and '
        'became the dominant international white variety; '
        'Riesling Itálico (Welschriesling — not related to '
        'German Rhine Riesling) was brought by the Italian '
        'immigrants from the Veneto and remains a '
        'signature white variety of the Italian-Brazilian '
        'wine tradition in Serra Gaúcha.'
    ),
    'production_technique': (
        'Miolo Reserva Especial Branco is produced from '
        'estate Chardonnay and Riesling Itálico vines '
        'at 650–800m elevation in the Vale dos Vinhedos. '
        'The harvest occurs in February–March (the southern '
        'hemisphere autumn) with selective hand or mechanical '
        'picking depending on the parcel gradient; the '
        'highland elevation allows a later harvest date '
        'than valley-floor vineyards, extending phenolic '
        'and aromatic development through the February '
        'diurnal temperature swing. The Chardonnay component '
        'is fermented in a combination of new French oak '
        'barriques (225L, 20–30% new wood) and stainless '
        'steel to build body and texture without '
        'overwhelming the tropical-fruit character of '
        'the subtropical Chardonnay; the Riesling Itálico '
        'component is fermented entirely in stainless '
        'steel at 16–18°C to preserve the high-acid '
        'aromatic freshness of the Welschriesling variety. '
        'The blend is assembled post-fermentation with '
        'the Riesling Itálico contributing acidity and '
        'the characteristic cidery-apple aromatic '
        '(acetaldehyde-derived from the Welschriesling '
        'fermentation profile) while the Chardonnay '
        'provides body, tropical fruit, and the oak '
        'integration. The wine is bottled after 4–6 months '
        'aging (stainless and/or partial oak) in '
        'September–October of the harvest year for release '
        'in the same calendar year. The IP Vale dos Vinhedos '
        '(Indicação de Procedência) white wine regulations '
        'permit Chardonnay, Riesling Itálico, Gewürztraminer, '
        'and Pinot Grigio as the principal white varieties; '
        'DOCG Vale dos Vinhedos is currently restricted '
        'to the Merlot-Cabernet-Tannat red blend but the '
        'IP certification covers the white production.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'wine — Northern Italy (Veneto, Friuli-Venezia Giulia — Welschriesling and Chardonnay blend)',
            'beverage': 'Friuli Grave DOC Bianco — Chardonnay and Riesling Italico Blend, Friulian Granite Gravel',
            'connection': (
                'Miolo Reserva Especial Branco and northern Italian '
                'Chardonnay-Welschriesling blends from Friuli and the Veneto '
                'share the same variety portfolio and the same Italian '
                'settler origin — the Riesling Itálico in Brazil is '
                'the identical Welschriesling that the Veneto and '
                'Friulian Italian immigrants carried to Rio Grande do Sul '
                'in their luggage in 1875, planted in the Serra Gaúcha '
                'highland soil because it reminded them of home. '
                'The difference is climate: northern Italy\'s Friuli '
                'produces Welschriesling with alpine-floral aromatics '
                'from the cool continental climate; Brazil\'s Serra '
                'Gaúcha produces a warmer, more tropical expression '
                'of the same variety from the subtropical highland '
                'climate. Both wines demonstrate that the Welschriesling '
                'variety maintains its characteristic high-acid, '
                'cidery-apple aromatic profile across radically '
                'different climate conditions — the genetic character '
                'of the variety is resilient across transplantation.'
            )
        },
        {
            'tradition': 'wine — Uruguay (Canelones, Tannat, South American Italian immigrant highland)',
            'beverage': 'Bodega Bouza Chardonnay — Montevideo Sur, Uruguayan White Wine, Atlantic Highland',
            'connection': (
                'Miolo Vale dos Vinhedos Branco and Uruguayan Chardonnay '
                'from the Canelones region share the South American '
                'Italian immigrant wine tradition context — both '
                'regions were settled by Italian agricultural '
                'immigrants in the late 19th century and both '
                'developed a white wine tradition around '
                'the Chardonnay variety as the international '
                'benchmark alongside indigenous or settler-imported '
                'local varieties. The parallel illuminates the '
                'geographic spread of the same Italian immigrant '
                'viticulture knowledge across the Southern Cone: '
                'from Rio Grande do Sul (Brazil) south through '
                'Uruguay to Mendoza (Argentina), the Italian '
                'settler agricultural heritage defines the '
                'white wine tradition of the entire South American '
                'Atlantic coast viticulture zone, and the '
                'variety palette (Chardonnay, Riesling Itálico, '
                'Trebbiano, Pinot Grigio) reflects the northern '
                'Italian origin of the wave of colonists.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale golden-yellow with a green highlight from the '
            'Riesling Itálico acid freshness and the cool highland '
            'fermentation temperature; the oak-fermented Chardonnay '
            'component contributes a warmer, more golden tone to '
            'the blend than a pure stainless-steel Riesling Itálico '
            'would produce alone; brilliant clarity from cold settling '
            'before fermentation; medium body legs from '
            '12–13% ABV and the partial oak texture.'
        ),
        'nose': (
            'The Vale dos Vinhedos subtropical climate delivers '
            'a Chardonnay aromatic profile with more tropical '
            'fruit character than temperate-climate Chardonnay: '
            'ripe mango and pineapple (the terpene-ester '
            'compounds of subtropical Chardonnay, produced '
            'in higher quantities at the 29°S latitude despite '
            'the highland elevation cooling); overlaid with '
            'the cidery-apple character of the Riesling Itálico '
            '(acetaldehyde-produced in the fermentation of '
            'the Welschriesling variety — the characteristic '
            'bruised-apple/cider note of the variety); '
            'beneath: the light vanilla-coconut from the '
            'Chardonnay oak-fermentation component '
            '(lactone compounds from the new French '
            'barrique contact); and the characteristic '
            'Terra Roxa volcanic mineral note '
            '(iron-rich basalt soil — a subtle '
            'iron-mineral character in the aromatic background).'
        ),
        'palate': (
            'Medium body from the Chardonnay oak-texture and '
            'the Serra Gaúcha basalt soil richness; '
            'the entry is dominated by the tropical fruit '
            'of the subtropical Chardonnay — mango, pineapple, '
            'ripe yellow apple; the mid-palate develops the '
            'Riesling Itálico\'s cidery freshness and high acidity '
            '(TA 7–8g/L from the highland elevation retaining '
            'natural tartaric acid); the oak integration '
            'from the Chardonnay component adds a biscuit-cream '
            'mid-palate texture; the finish is medium-length '
            '(20–30 seconds) with the cidery-apple and '
            'light mineral character of the Riesling Itálico '
            'providing the clean, fresh close. '
            'The wine is dry (residual sugar below 5g/L) '
            'despite the tropical fruit register of the '
            'subtropical Chardonnay — the acidity balances '
            'the fruit richness effectively.'
        ),
        'conclusion': (
            'The Italian immigrant white wine heritage of Vale dos Vinhedos '
            'expressed through the subtropical adaptation of the '
            'Chardonnay-Welschriesling variety pairing — '
            'the northern Italian settler viticulture tradition '
            'translated to the Brazilian highland basalt.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Single-vineyard IP Vale dos Vinhedos Chardonnay from '
                'identified highland parcels (640–800m elevation) with '
                '100% new French barrique fermentation and 8–12 months '
                'sur lie aging; the tropical fruit character of subtropical '
                'Chardonnay integrated with the biscuit-cream of intensive '
                'oak contact; Riesling Itálico as a minor blending component '
                'only for acidity management (10–20% of blend); '
                'estate-bottled with certified IP Vale dos Vinhedos '
                'geographic certification. Miolo Cuvée Giuseppe or '
                'Miolo Reserva de Família expressions. '
                'EUR/BRL premium tier; limited international export.'
            ),
            'markers': (
                'Single vineyard; 640m+ elevation; 100% French barrique; '
                'sur lie 8–12 months; tropical-biscuit-cream; IP certified.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Miolo Reserva Especial Branco or equivalent — identified '
                'estate-grown Chardonnay-Riesling Itálico blend with '
                'partial oak fermentation (20–30% new French barrique); '
                'tropical fruit balanced by Riesling Itálico acidity; '
                'IP Vale dos Vinhedos certified; EUR 18–35 export price. '
                'The professional-quality expression of the Serra Gaúcha '
                'Italian immigrant white wine tradition.'
            ),
            'markers': (
                'Estate Chardonnay-Riesling blend; partial oak; IP certified; '
                'tropical-cidery-mineral; EUR 18–35.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Miolo Selection or equivalent commercial Chardonnay '
                'without Serra Gaúcha highland-specific fruit source — '
                'broader Vale dos Vinhedos or Serra Gaúcha geographic '
                'designation using valley-floor fruit with less '
                'aromatic concentration from lower elevation; '
                'competent commercial white wine at BRL 30–50 '
                'domestic price. No IP certification required.'
            ),
            'markers': (
                'Commercial Chardonnay; no IP designation; '
                'valley-floor fruit; lower elevation; BRL 30–50.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic Rio Grande do Sul Branco without variety '
                'or geographic specification — bulk commercial white '
                'from the cooperative sector using the Isabella '
                'or Niagara hybrid grapes that dominated Serra Gaúcha '
                'production before the vinifera premium shift; '
                'the foxy-labrusca character of Isabella is the '
                'quality indicator of the entry-level Brazilian white '
                'wine market. Not relevant to the PCT programme context.'
            ),
            'markers': (
                'Hybrid grape; foxy labrusca; no IP; bulk commercial; '
                'not relevant to premium programme use.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve at 8–10°C to preserve the aromatic freshness '
            'of the Riesling Itálico component — the cidery-apple '
            'volatile esters of the Welschriesling variety '
            'dissipate at temperatures above 12°C. '
            'The Chardonnay component can tolerate slightly warmer '
            'service (10–12°C) to express the tropical fruit '
            'and oak texture, so a compromise service temperature '
            'of 9–10°C serves both variety components. '
            'Ice bucket with water recommended; pour fresh '
            'from the bucket for each service. '
            'Consume within 2–3 years of harvest for optimal '
            'aromatic freshness.'
        ),
        'vessel': (
            'Standard ISO white wine glass (215ml) or a Riedel '
            'Chardonnay-style glass (220–250ml capacity) with '
            'a 90ml pour — the wider bowl allows the tropical '
            'Chardonnay aromatics to develop above the surface '
            'while the narrowing tulip concentrates them for '
            'the nose. For PCT programme comparative: present '
            'alongside the Cave Geisse Brut Nature (sparkling '
            'Vale dos Vinhedos) and the Campanha Meridional '
            'Tannat to demonstrate the three white/sparkling/red '
            'expressions of the Brazilian Italian immigrant '
            'wine tradition in a single regional flight.'
        ),
        'technique': (
            'Serve at 9–10°C from ice bucket; 90ml in Chardonnay-style '
            'glass; no decanting. Present the Italian immigrant '
            'settlement narrative — the 1875 migration from '
            'Veneto/Trentino, the Riesling Itálico as the '
            'preserved varietal memory of the emigrants, '
            'and the DOCG Vale dos Vinhedos as the Brazilian '
            'recognition of the Italian appellation system.'
        ),
        'programme_position': (
            'PCT Brazilian wine arc: Miolo Reserva Especial Branco '
            'alongside Cave Geisse Brut Nature (sparkling), '
            'Miolo Reserva Tinto (red), and Campanha Meridional '
            'Guatambu Tannat for a four-expression Brazilian '
            'wine depth programme; or as the New World Italian '
            'immigrant white wine foil in a comparative '
            'alongside Friuli Grave DOC Bianco (the Italian origin) '
            'and a California Chardonnay (the American immigrant parallel).'
        ),
        'verbal_presentation': (
            'Rio Grande do Sul. 1875. Italian farmers arriving in '
            'the Brazilian highlands with vine cuttings from Veneto. '
            'This Riesling Itálico is the same variety they brought. '
            'Four generations later, Vale dos Vinhedos has a DOCG — '
            'the first in Brazil. This is what transplanted heritage looks like '
            'after 150 years of highland volcanic soil.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Miolo Wine Group (Bento Gonçalves, Vale dos Vinhedos) — '
            'Brazil\'s largest premium wine exporter; the commercial '
            'benchmark for internationally distributed Vale dos Vinhedos '
            'white wine. '
            'Secondary: Cave Geisse (sparkling specialist, Vale dos Vinhedos) '
            'and Casa Valduga (the other major IP Vale dos Vinhedos estate) '
            'for alternative white wine expressions.'
        ),
        'producer_location': 'Bento Gonçalves, Vale dos Vinhedos, Serra Gaúcha, Rio Grande do Sul, Brazil',
        'key_person': 'Adriano Miolo (CEO) and Andrea Miolo (export director)',
        'production_volume': '10 million litres/year total; IP Vale dos Vinhedos certified tier approximately 500,000–800,000 litres',
        'certifications': ['IP Vale dos Vinhedos', 'DOCG Vale dos Vinhedos (red tier)', 'Wines of Brasil export certification'],
        'bc_distributor': '[PROVIDER: verify through Wines of Brasil Canada trade office; Miolo has historically been listed through BCLDB special order — confirm current status]',
        'us_distributor': '[PROVIDER: Miolo USA through World Shiner or similar Latin American wine specialist — verify current US importer]',
        'uk_distributor': '[PROVIDER: verify through Wines of Brasil UK trade representation; limited UK distribution as of 2026]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Miolo is the most widely exported Brazilian wine brand '
            'internationally and the most likely of the Vale dos Vinhedos '
            'producers to be available through major wine merchants. '
            'The Reserva Especial Branco is the programme-accessible '
            'white wine expression of the DOCG Vale dos Vinhedos tradition. '
            'Programme buyers should source through the Wines of Brasil '
            'trade body for current distributor listings in their market.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Miolo Vale dos Vinhedos Branco connects the PCT Brazilian colonial '
        'wine arc to the Italian immigrant settlement narrative of '
        'Serra Gaúcha — the Portuguese colonial administration of Brazil '
        'that recruited Italian agricultural settlers in 1875 created '
        'the conditions for a European transplanted viticulture tradition '
        'that developed its own DOCG certification (the first in Brazil) '
        'from the same highland volcanic soil that the settlers found '
        'when they arrived in the Brazilian interior. The PCT '
        'connection runs from the Portuguese colonial administration '
        'through the Italian immigrant settlement through the '
        '150-year development of a certified Brazilian wine region.'
    ),
    'food_pairings': [
        {
            'technique_id': 'BRZ-001',
            'dish': 'Galeto (young chicken grilled with herbs — the traditional Serra Gaúcha Italian immigrant meal, eaten at the colonial vineyard cantinas)',
            'pairing_type': 'complement',
            'rationale': (
                'Galeto (young rotisserie chicken with herbs) is the '
                'traditional meal of the Italian immigrant cantinas '
                'of Serra Gaúcha — the same heritage as the '
                'Chardonnay-Riesling Itálico white wine tradition. '
                'The wine\'s tropical fruit and cidery acidity '
                'complement the light poultry fat and herb aromatics '
                'of the galeto through the classic white wine '
                'acidity-fat complementarity, while the within-region '
                'cultural pairing reflects the Italian settler '
                'meal tradition of wine with the cantina roast.'
            )
        },
        {
            'technique_id': 'BRZ-002',
            'dish': 'Moqueca baiana (Bahian coconut-palm oil fish stew with dende and lime)',
            'pairing_type': 'contrast',
            'rationale': (
                'The high natural acidity (TA 7–8g/L) and tropical '
                'fruit character of the Vale dos Vinhedos Branco '
                'create a within-country contrast pairing with '
                'the coconut-dende richness of moqueca baiana — '
                'the wine\'s acidity cutting the coconut-palm oil '
                'weight while the tropical Chardonnay fruit '
                'resonates with the coconut and lime of the stew '
                'in a pan-Brazilian flavour bridge between '
                'the Italian immigrant south and the '
                'Afro-Brazilian northeast.'
            )
        }
    ],
    'source': 'APROVALE (Associação dos Produtores de Vinhos Finos do Vale dos Vinhedos) technical documentation; IBRAVIN (Instituto Brasileiro do Vinho) regional reports; Miolo Wine Group producer documentation; Wines of Brasil trade export data; Trott Cristina — Brazilian Wine Guide; Robinson Jancis Oxford Companion to Wine (Brazil entry)',
    'price_trajectory': 'rising'
})

session.commit_batch()

# Entry 2: Pinto Bandeira Sparkling
session.switch_region(
    'wine',
    'Brazil — South (Pinto Bandeira Sub-Region, Aliança Espumante Brut, Italian Immigrant Sparkling, Serra Gaúcha Alpine)'
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Vinícola Aliança (and collective Pinto Bandeira producers cooperative)',
    'location': 'Pinto Bandeira, Rio Grande do Sul, Brazil (the dedicated sparkling wine sub-region of Serra Gaúcha)',
    'country': 'Brazil',
    'region': 'Pinto Bandeira — IP Pinto Bandeira sub-region of Serra Gaúcha, 700–900m elevation',
    'key_person': 'The Pinto Bandeira sparkling wine tradition is a collective community production heritage from the Italian immigrant settlement — individual small family producers alongside the cooperative structure',
    'founded': '1870s (Italian immigrant settlement of the Pinto Bandeira community); commercial sparkling wine production from the 1980s when Pinto Bandeira was identified as the optimal sparkling wine terroir within Serra Gaúcha',
    'production_volume': 'Combined Pinto Bandeira IP sub-region production estimated at 500,000–800,000 litres/year espumante; Aliança and Salton are the primary commercial-scale producers',
    'notable_products': [
        'Aliança Espumante Brut (traditional method, Chardonnay-Pinot Noir)',
        'Salton Espumante Brut (the other major Pinto Bandeira producer)',
        'Pinto Bandeira IP-certified sparkling wines (the collective sub-region designation)',
    ],
    'certifications': ['IP Pinto Bandeira (Indicação de Procedência — Brazil\'s first dedicated sparkling wine IP designation, 2010)'],
    'website': '[PROVIDER: Vinícola Aliança — www.vinicola-alianca.com.br — verify current status]',
    'philosophy': (
        'The Pinto Bandeira sparkling wine community represents the Italian immigrant '
        'settlement\'s highest achievement in the application of traditional method '
        'sparkling wine production to the Brazilian highland climate — the same method '
        'as Champagne (secondary fermentation in bottle) applied to the '
        'Chardonnay-Pinot Noir variety pair at 700–900m Serra Gaúcha elevation.'
    ),
    'trail_connection': 'PCT (Brazil — Italian immigrant sparkling wine heritage node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Pinto Bandeira IP Espumante Brut — Traditional Method Sparkling, '
        'Chardonnay and Pinot Noir, Serra Gaúcha Alpine, Italian Immigrant '
        'Champenoise Heritage, Brazil\'s First Dedicated Sparkling Wine IP'
    ),
    'tradition': 'wine',
    'sub_tradition': 'sparkling_wine — traditional method (méthode traditionnelle), IP Pinto Bandeira, Chardonnay-Pinot Noir, 700–900m Serra Gaúcha alpine',
    'region': 'Brazil — South (Pinto Bandeira Sub-Region, Aliança Espumante Brut, Italian Immigrant Sparkling, Serra Gaúcha Alpine)',
    'terroir_origin': (
        'Pinto Bandeira is a mountain community within Serra Gaúcha '
        'at 700–900m elevation, occupying the upper reaches of the '
        'Petrópolis River valley in Rio Grande do Sul\'s Bento Gonçalves '
        'municipality. The sub-region was identified in the 1980s as '
        'the optimal terroir for traditional method sparkling wine '
        'within Brazil — the higher elevation (100–200m higher than '
        'the main Vale dos Vinhedos floor) provides cooler growing '
        'temperatures (average 2–3°C cooler at harvest) that preserve '
        'the natural acidity and fine phenolic development critical '
        'to base wine quality for sparkling production. The basalt-'
        'derived Terra Roxa soils at Pinto Bandeira are thinner than '
        'the valley floor, with more fractured basalt bedrock providing '
        'better drainage and lower vigour — the conditions that '
        'concentrate the flavour precursors in the berry without '
        'excessive vegetal character from over-vigorous vine growth. '
        'The Italian immigrant community of Pinto Bandeira '
        'settled primarily from Trentino-Alto Adige '
        '(the Italian region that borders Trento DOC, '
        'northern Italy\'s own high-altitude traditional method '
        'sparkling wine zone) — the settlers brought not only '
        'their Vitis vinifera cuttings but the specific knowledge '
        'that cool-climate high-altitude was the optimal condition '
        'for sparkling wine production. Pinto Bandeira received '
        'Brazil\'s first dedicated Indicação de Procedência (IP) '
        'for sparkling wine in 2010, recognising that the '
        'sub-region had a distinctive terroir identity '
        'separate from the broader Serra Gaúcha designation.'
    ),
    'production_technique': (
        'Pinto Bandeira traditional method espumante uses the same '
        'production architecture as Champagne méthode traditionnelle: '
        'the base wines are produced from Chardonnay (dominant) '
        'and Pinot Noir (contributing body and red-fruit character) '
        'harvested at the target base wine acidity of 8–10g/L TA '
        '(maintained by the 700–900m altitude cool growing season); '
        'base wine fermentation in stainless steel at 16–18°C; '
        'blending of base wines across parcels and sometimes '
        'reserve wines from previous years (non-vintage assemblage '
        'for the Brut NV expressions); the blended base wine '
        'is bottled with a tirage dosage (sugar and yeast addition '
        'in crown cap) for the secondary fermentation in bottle; '
        'secondary fermentation produces CO₂ (bubbles) and '
        'lees yeast autolysis at the cellar temperature of '
        '12–14°C over 12–18 months minimum for Brut NV; '
        'riddling (remuage) turns the bottles to consolidate '
        'the spent yeast sediment on the crown cap; '
        'dégorgement (disgorging) removes the frozen yeast '
        'plug and the dosage (liqueur d\'expédition) '
        'adjusts the final sweetness (Brut: 0–12g/L '
        'residual sugar; Extra-Brut: 0–6g/L). '
        'The completed wine is sealed with a '
        'mushroom cork and wire cage. '
        'The key Pinto Bandeira distinction from '
        'the Vale dos Vinhedos Cave Geisse '
        'Brut Nature (zero dosage) is the use '
        'of a modest dosage (8–10g/L) in the '
        'Brut expression that moderates the '
        'Serra Gaúcha acidity to the commercial '
        'Brut profile that the Brazilian domestic '
        'market favours. Italian-heritage varieties '
        '(Prosecco/Glera, Trebbiano) are sometimes '
        'blended in at 5–15% for a within-heritage '
        'aromatic component.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'wine — Trentodoc (Trento DOC, northern Italy — traditional method sparkling, alpine altitude)',
            'beverage': 'Ferrari Trento DOC Brut — Traditional Method, High Alpine, Chardonnay-Pinot Noir',
            'connection': (
                'Pinto Bandeira IP espumante and Trento DOC traditional method '
                'represent the same production tradition transplanted from '
                'the same geographic origin to the same production conditions: '
                'the Italian immigrants who founded the Pinto Bandeira '
                'sparkling wine community came predominantly from '
                'Trentino-Alto Adige — the Italian alpine region that '
                'produces Ferrari Trento DOC at 300–900m altitude '
                'using the traditional method with Chardonnay-Pinot Noir. '
                'The variety pair (Chardonnay dominant; Pinot Noir for body), '
                'the production method (méthode traditionnelle), '
                'and the fundamental terroir logic (altitude for acidity '
                'preservation) are identical between the two traditions. '
                'The difference is soil: Trentino\'s calcareous limestone '
                'alpine soils versus Pinto Bandeira\'s volcanic basalt '
                'Terra Roxa — the mineral character diverges '
                '(limestone-floral versus volcanic-iron) while '
                'the method and variety produce a recognisably '
                'shared sparkling wine identity across the '
                'Atlantic immigrant transfer.'
            )
        },
        {
            'tradition': 'wine — Cave Geisse (Vale dos Vinhedos, Brazil — Brut Nature zero dosage sparkling)',
            'beverage': 'Cave Geisse Brut Nature — Vale dos Vinhedos DOCG, Zero Dosage, Traditional Method',
            'connection': (
                'Pinto Bandeira IP Espumante Brut and Cave Geisse '
                'Brut Nature are the two poles of the Brazilian '
                'traditional method sparkling wine tradition — '
                'both use the same production method and the same '
                'highland Serra Gaúcha terroir, but Pinto Bandeira '
                'produces its sparkling at the higher sub-region '
                'elevation (700–900m versus Cave Geisse\'s 600–700m) '
                'and uses a modest dosage (8–10g/L) while Cave '
                'Geisse bottles zero-dosage Brut Nature with no '
                'residual sugar addition. The acidity at Pinto '
                'Bandeira\'s altitude makes zero-dosage possible '
                'in exceptional years but the standard commercial '
                'expression uses dosage to round the acidity for '
                'the Brazilian domestic market. Together they '
                'define the complete arc of Brazilian Italian '
                'immigrant traditional method sparkling wine: '
                'from the accessible Brut to the demanding Brut Nature, '
                'both from volcanic highland Serra Gaúcha basalt.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale straw-gold with fine persistent bubbles (the fine '
            'bead of traditional method lees-contact secondary fermentation '
            'in bottle — distinctly finer than tank-method Charmat '
            'espumante bubbles); the mousse is creamy and persistent, '
            'not aggressive; colour brightness from the cool-climate '
            'fermentation preserving the pale lemon-straw spectrum '
            'of the highland Chardonnay; small Pinot Noir component '
            'contributes no pink tone at this proportion.'
        ),
        'nose': (
            'The traditional method lees autolysis character defines '
            'the Pinto Bandeira Brut nose: the brioche-biscuit-toasted '
            'bread complex of the Saccharomyces yeast lees autolysis '
            '(mannoproteins and fatty acid ethyl esters produced '
            'by the 12–18 months contact with the spent yeast in bottle) '
            'overlaid on the green apple and lemon zest primary '
            'fruit of the high-altitude Chardonnay (the citric '
            'and malic acid-dominant spectrum of the cooler '
            'Pinto Bandeira growing environment); the Pinot Noir '
            'component contributes a subtle red cherry or strawberry '
            'note (anthocyanin-adjacent aromatic from the Pinot '
            'Noir rosé press fraction); beneath: the volcanic '
            'Terra Roxa mineral character — an iron-mineral, '
            'slightly earthy background note from the basalt soil.'
        ),
        'palate': (
            'Fine, creamy mousse from the traditional method secondary '
            'fermentation in bottle (the CO₂ is molecularly integrated '
            'into the wine over 12–18 months rather than force-carbonated); '
            'the entry is citrus-bright with the green apple and '
            'lemon zest of the highland Chardonnay acidity; '
            'the brioche lees-autolysis character of the mid-palate '
            'adds texture and weight; the dosage (8–10g/L residual sugar) '
            'rounds the acidity without producing perceptible sweetness — '
            'the wine reads as a clean, refreshing Brut; '
            'the finish is medium (25–35 seconds) with '
            'the mineral-acid character of the Pinto Bandeira '
            'altitude persisting through the close. '
            'Total acidity 7–9g/L maintains the tension '
            'that distinguishes traditional method from '
            'Charmat tank-method espumante in the Brazilian market.'
        ),
        'conclusion': (
            'The most complete expression of the Italian immigrant '
            'traditional method sparkling wine tradition in Brazil — '
            'the Trentino settler knowledge applied to the volcanic '
            'highland basalt of Pinto Bandeira at 800m altitude.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Vintage-dated IP Pinto Bandeira Brut Rosé or Blanc de Blancs '
                'from identified highland parcels (800–900m); minimum 36 months '
                'lees contact producing the full autolysis complex '
                '(brioche, cream, hazelnuts from the extended Maillard '
                'and lysis products); manual riddling by remueur; '
                'traditional dégorgement; zero-dosage or Extra-Brut '
                '(0–6g/L) to showcase the natural altitude acidity; '
                'Cave Geisse Brut Nature or Aliança Vintage expressions '
                'at the premium tier. EUR 30–60 export price.'
            ),
            'markers': (
                'Vintage dated; 800m+ altitude; 36+ months lees; '
                'manual riddling; zero or Extra-Brut dosage; '
                'hazelnuts-brioche-cream complexity.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Non-vintage IP Pinto Bandeira Brut from identified '
                'highland parcels with minimum 18 months lees contact; '
                'the commercial expression of the traditional method '
                'sparkling wine heritage; Brut dosage (8–12g/L); '
                'clean brioche-biscuit autolysis character; '
                'Chardonnay dominant (70–80%) with Pinot Noir; '
                'EUR 18–30 export price.'
            ),
            'markers': (
                'IP Pinto Bandeira NV Brut; 18+ months lees; '
                'Chardonnay dominant; brioche-lemon character; '
                'fine persistent bead.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Serra Gaúcha Espumante Brut without IP Pinto Bandeira '
                'designation — broader geographic origin from the '
                'valley floor (below 700m) with Charmat (tank) method '
                'rather than traditional method; competent commercial '
                'sparkling wine without the lees-autolysis character '
                'of bottle secondary fermentation; BRL 40–80 domestic; '
                'EUR 10–18 export.'
            ),
            'markers': (
                'No IP designation; Charmat method; no lees autolysis; '
                'commercial bubble; valley floor fruit.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic Brazilian espumante using Moscatel or hybrid '
                'grape varieties rather than Chardonnay-Pinot Noir — '
                'the domestic sweet sparkling market (Espumante Moscatel, '
                'Espumante Demi-Sec) that dominates Brazilian per-capita '
                'consumption but has no connection to the traditional '
                'method Champagne-heritage tradition of Pinto Bandeira. '
                'Not relevant to PCT programme use.'
            ),
            'markers': (
                'Moscatel or hybrid; sweet sparkling; Charmat; '
                'no traditional method; mass-market domestic.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve at 6–8°C — the correct service temperature for '
            'traditional method sparkling wine to preserve the fine '
            'bead (CO₂ solubility increases at lower temperatures, '
            'maintaining the molecular integration of the bubbles), '
            'the aromatic freshness of the lees-autolysis character, '
            'and the citrus-acid brightness of the highland Chardonnay. '
            'Ice bucket with water for service; 30 minutes in ice '
            'bucket before opening; serve continuously from the '
            'bucket between pours. Open with a gentle twist '
            'and tilt (never a pop — the CO₂ is precision-formed '
            'through 18 months of bottle fermentation '
            'and should not be wasted in the pour).'
        ),
        'vessel': (
            'A traditional Champagne flute (180–200ml capacity; '
            '100ml pour) or a white Burgundy-style glass (240ml; '
            '100ml pour — the wider bowl expresses the lees '
            'autolysis character more fully than the flute). '
            'For PCT programme comparative: present alongside '
            'a Ferrari Trento DOC Brut (the Italian origin tradition) '
            'and the Cave Geisse Brut Nature (the Brazilian '
            'zero-dosage extreme) to complete the three-expression '
            'traditional method Italian immigrant sparkling wine arc: '
            'origin (Trentino) → highland highland Brut → Brut Nature.'
        ),
        'technique': (
            'Serve at 6–8°C from ice bucket; 100ml in flute or '
            'Burgundy glass; gentle pour with tilt to preserve '
            'the bead; no decanting. Present the IP Pinto Bandeira '
            'designation — Brazil\'s first dedicated sparkling wine '
            'geographic indication — and the Trentino immigrant '
            'origin narrative.'
        ),
        'programme_position': (
            'PCT Italian immigrant sparkling arc: Pinto Bandeira '
            'alongside Ferrari Trento DOC (Italian origin) and '
            'Cave Geisse Brut Nature (Brazilian traditional method '
            'pinnacle) for the three-expression sparkling wine '
            'heritage comparative; or as the New World traditional '
            'method sparkling in a global comparative alongside '
            'Champagne (France), Cava (Spain), and Franciacorta '
            '(Italy) for a world traditional method sparkling programme.'
        ),
        'verbal_presentation': (
            'Pinto Bandeira. 800 metres. The settlers came from Trentino '
            'where they had been making sparkling wine in the mountains '
            'for centuries. They arrived in Brazil in 1875 and found '
            'the same altitude, the same basalt, and the same cool air '
            'that their sparkling wine required. This is the result: '
            'Brazil\'s first IP for sparkling wine. The method is unchanged '
            'from Trentino. The soil is South American volcanic basalt.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'IP Pinto Bandeira collective designation — multiple producers '
            'hold the IP certification; the benchmark commercial expression '
            'is Aliança Espumante Brut (Vinícola Aliança, Pinto Bandeira) '
            'and Salton Espumante Brut (the volume benchmark). '
            'For the quality pinnacle: Cave Geisse Brut Nature '
            '(Vale dos Vinhedos, same tradition — the artisan standard) '
            'and Miolo Cuvée Brut (the Miolo traditional method expression). '
            'For the Italian original: Ferrari Trento DOC Brut '
            '(the ancestral origin; available internationally).'
        ),
        'producer_location': 'Pinto Bandeira, Bento Gonçalves municipality, Serra Gaúcha, Rio Grande do Sul, Brazil',
        'key_person': 'Multiple family producers; the IP Pinto Bandeira association coordinates the collective certification',
        'production_volume': '500,000–800,000 litres/year combined IP Pinto Bandeira espumante production',
        'certifications': ['IP Pinto Bandeira (Indicação de Procedência — Brazil\'s first dedicated sparkling wine IP, awarded 2010)'],
        'bc_distributor': '[PROVIDER: verify through Wines of Brasil Canada — Pinto Bandeira espumante has limited direct international export infrastructure; Aliança brand may be available through Latin American specialty importers]',
        'us_distributor': '[PROVIDER: verify through Brazilian specialty wine importers in Florida/California market — primary US Brazilian wine entry points]',
        'uk_distributor': '[PROVIDER: limited UK distribution as of 2026; verify through Wines of Brasil UK trade representative]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Pinto Bandeira IP espumante is primarily available in the '
            'Brazilian domestic market; international export is growing '
            'but limited compared to Vale dos Vinhedos still wine. '
            'Programme buyers in North America and Europe may prefer '
            'to source Ferrari Trento DOC (the Italian original tradition) '
            'as the heritage reference and use Pinto Bandeira documentation '
            'for the programme narrative context without requiring '
            'the Brazilian expression in the flight.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Pinto Bandeira IP espumante is the sparkling wine node of the '
        'Brazilian Italian immigrant wine heritage arc in the PCT — '
        'the specific point where the Trentino alpine traditional '
        'method sparkling wine knowledge transplanted to Brazilian '
        'volcanic highland soil produced a legally recognised and '
        'geographically specific product that stands as evidence '
        'of the cultural transfer capability of the Italian '
        'immigrant agricultural settlement in southern Brazil.'
    ),
    'food_pairings': [
        {
            'technique_id': 'BRZ-003',
            'dish': 'Casquinha de siri (Brazilian crab gratin with breadcrumbs and parmesan — the classic espumante aperitif pairing)',
            'pairing_type': 'complement',
            'rationale': (
                'The fine bead and citrus acidity of the Pinto Bandeira '
                'Espumante Brut complement the richness of casquinha '
                'de siri through the classic sparkling wine fat-cutting '
                'mechanism — the dissolved CO₂ and natural acidity '
                '(TA 7–9g/L) of the traditional method sparkling wine '
                'cleanses the crab-parmesan fat from the palate '
                'while the lees autolysis brioche character bridges '
                'with the toasted breadcrumb of the gratin.'
            )
        },
        {
            'technique_id': 'BRZ-004',
            'dish': 'Polenta grelhada com cogumelos (grilled polenta with wild mushrooms — the Italian immigrant highland staple, invoking the Trentino mountain origin)',
            'pairing_type': 'bridge',
            'rationale': (
                'Grilled polenta with wild mushrooms invokes the '
                'Trentino mountain table of the immigrant settlers\' '
                'origin region — the combination of corn polenta '
                '(the staple grain of northern Italy and of the '
                'Brazilian highland settler diet) and wild mushrooms '
                '(porcini, Caesar\'s mushroom) creates an earthy-mineral '
                'food pairing that bridges with the Terra Roxa '
                'volcanic mineral character and the '
                'lees autolysis earthiness of the '
                'Pinto Bandeira sparkling wine.'
            )
        }
    ],
    'source': 'IBRAVIN (Instituto Brasileiro do Vinho) IP Pinto Bandeira documentation; APROVALE sparkling wine sub-region technical notes; Wines of Brasil export data; Rizzon and Miele Embrapa Uva e Vinho Serra Gaúcha viticultural research; Robinson Jancis Oxford Companion to Wine (Brazil sparkling wine entry)',
    'price_trajectory': 'rising'
})

session.commit_batch()

# Entry 3: Timor-Leste Palm Toddy
session.switch_region(
    'fermented',
    'Timor-Leste — Dili (Tua Mutin and Tua Sabu, Traditional Fermented Palm Beverages, Timorese Cultural Heritage)'
)

session.add_producer({
    'tradition': 'fermented',
    'name': 'Timorese Palm Toddy Tappers (collective community practice — no commercial producer)',
    'location': 'Dili district and rural sub-districts of Timor-Leste; coconut palms (tua mutin) concentrated in coastal lowlands; lontar palms (Borassus flabellifer — tua sabu) in the drier interior and south coast',
    'country': 'Timor-Leste',
    'region': 'Timor-Leste — nationally distributed; tua mutin (coconut toddy) in coastal zones; tua sabu (lontar palm toddy) in the Oecusse enclave and south coast Manatuto and Manufahi districts',
    'key_person': 'Traditional tappers (tobak — the Tetun word for the specialist who climbs and taps the palm; the skill is transmitted within family and community lineage)',
    'founded': 'Pre-colonial origin (pre-Portuguese contact before 1511); the palm toddy tradition of Timor-Leste predates Portuguese colonial presence by millennia — it is part of the Austronesian fermented palm tradition that spread from the Philippines through Indonesia to Timor over 3,000+ years',
    'production_volume': 'Estimated thousands of litres per day during peak tapping season; entirely domestic subsistence and community consumption; no reliable production data',
    'notable_products': [
        'Tua mutin (fresh coconut toddy — white palm wine from Cocos nucifera inflorescence sap, 1–7% ABV depending on fermentation stage)',
        'Tua sabu (lontar palm toddy — slightly thicker, sweeter fresh toddy from Borassus flabellifer inflorescence sap)',
        'Tua fermentadu (over-fermented toddy, higher ABV, more sour — the household beer substitute)',
        'Sopi (distilled palm spirit — the Timorese distilled version; rare; produced in some rural communities)',
    ],
    'certifications': [],
    'website': '[NO COMMERCIAL PRESENCE — traditional subsistence production only]',
    'philosophy': (
        'The tua mutin and tua sabu traditions of Timor-Leste are living '
        'expressions of the Austronesian palm fermentation heritage that '
        'connects Timor to the broader Indian Ocean palm toddy network '
        '(Kerala kallu, Mozambique nipa, Goa toddy, Philippines tuba) — '
        'the fermented sap of the coconut or lontar palm consumed at '
        'traditional ceremonies (uma lulik sacred house rituals, '
        'barlaque marriage negotiations, tara bandu community governance '
        'meetings) as a social-spiritual beverage of the Timorese '
        'animist tradition.'
    ),
    'trail_connection': 'PCT (Timor-Leste — Portuguese colonial node, Indian Ocean Austronesian fermentation network)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Timor-Leste Tua Mutin and Tua Sabu — Coconut and Lontar Palm Toddy, '
        'Austronesian Indian Ocean Fermentation Heritage, Ceremonial Timorese '
        'Community Beverage, PCT Cultural Bridge'
    ),
    'tradition': 'fermented',
    'sub_tradition': 'palm_toddy — coconut palm (tua mutin, Cocos nucifera) and lontar palm (tua sabu, Borassus flabellifer) fresh-fermented inflorescence sap; ancestral Austronesian fermentation tradition',
    'region': 'Timor-Leste — Dili (Tua Mutin and Tua Sabu, Traditional Fermented Palm Beverages, Timorese Cultural Heritage)',
    'terroir_origin': (
        'Timor-Leste occupies the eastern half of Timor Island '
        'in the Lesser Sunda Islands of maritime Southeast Asia, '
        'at 8–9°S latitude, between Indonesia and Australia. '
        'The island is geologically complex — a collision zone '
        'between the Australian continental plate and the Asian '
        'oceanic plate, producing a mountainous interior '
        '(maximum elevation 2,963m, Mount Ramelau) with '
        'dramatic climate variation between the wet north '
        'coast (monsoon 1,500–2,000mm/year) and the dry '
        'south coast (700–1,000mm/year). Coconut palms '
        '(Cocos nucifera) are abundant on the coastal '
        'lowlands of the north and west; lontar palms '
        '(Borassus flabellifer — the African fan palm '
        'that extended through the Indian Ocean trade '
        'routes to Southeast Asia) grow in the drier '
        'south coastal zones and the Oecusse enclave '
        '(the Portuguese-colonial remnant enclave within '
        'Indonesian West Timor). The Timorese palm '
        'toddy tradition is part of the Austronesian '
        'fermentation heritage network that connected '
        'Timor to the Philippines (tuba, lambanog), '
        'Kerala India (kallu, toddy), Mozambique '
        '(nipa palm spirits), and Goa (feni/toddy '
        'precursors) through the Indian Ocean trade '
        'routes that preceded and coexisted with '
        'Portuguese colonial contact from 1511. '
        'The Portuguese found an existing palm '
        'fermentation tradition on Timor when they '
        'arrived; colonial records from the 16th–17th '
        'century document the tua production as a '
        'critical part of the island\'s subsistence '
        'agricultural economy alongside sandalwood, '
        'beeswax, and coffee.'
    ),
    'production_technique': (
        'Tua mutin production begins before dawn: the tobak '
        '(trained palm tapper) climbs the coconut palm '
        '(Cocos nucifera, 15–20m height) using a climbing '
        'technique with a hip loop rope (the same technique '
        'documented across the entire Austronesian coconut '
        'toddy belt from the Philippines to Kerala); '
        'the immature coconut flower inflorescence '
        '(the spadix, before it opens to produce '
        'individual coconuts) is bent downward, '
        'the tip scored with a knife, and a clay '
        'pot or bamboo container tied beneath the cut '
        'to collect the sap. The sap (neera — the '
        'Tetun term parallels the Malayalam kallu neera '
        'and the Konkani terminology) drips at a rate '
        'of 1–2 litres per day from each inflorescence '
        'and is collected twice daily (morning and evening). '
        'Fresh sap (tua mutin sweet — within 2–4 hours '
        'of collection) is a non-alcoholic sweet beverage '
        '(pH 6.5–7.0, Brix 12–16°) rich in sucrose '
        'and B-vitamins. Within 4–8 hours at ambient '
        'temperature (28–34°C in the Timor lowland climate) '
        'the Saccharomyces cerevisiae and Lactobacillus '
        'bacteria naturally present on the container '
        'surfaces initiate fermentation, converting '
        'the sucrose to ethanol and lactic acid. '
        'Fresh fermented tua mutin at 8–12 hours '
        '(1–3% ABV, slightly effervescent, sour-sweet) '
        'is the most common consumption stage. '
        'Extended fermentation (12–24+ hours) '
        'produces tua fermentadu at 4–7% ABV, '
        'more sour and more alcoholic — the '
        'Timorese equivalent of the West African '
        'opaque fermented grain beer tradition. '
        'Tua sabu from the lontar palm '
        '(Borassus flabellifer) uses the same '
        'collection technique but from the '
        'lontar palm inflorescence, producing '
        'a slightly thicker, sweeter base sap '
        '(Brix 14–18°) that ferments to a '
        'comparable 2–5% ABV toddy with a '
        'distinctive palm-sugar caramel character '
        'from the lontar\'s higher sucrose-to-glucose '
        'ratio. Tua sabu is considered culturally '
        'superior in traditional Timorese ceremony '
        '(uma lulik sacred house rituals) due to the '
        'lontar\'s symbolic importance in the Timorese '
        'cosmological tradition. No distillation is '
        'standard practice for the community tradition — '
        'the sopi distillate is a peripheral product '
        'in rural communities with access to still technology.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'fermented — Kerala toddy (India — kallu, Cocos nucifera, Malabar Coast)',
            'beverage': 'Kerala Kallu — Coconut Palm Toddy, Malabar Coast, Indian Ocean Austronesian Network',
            'connection': (
                'Timor-Leste tua mutin and Kerala kallu are the eastern '
                'and western poles of the same Indian Ocean Austronesian '
                'coconut palm toddy tradition — the fermented inflorescence '
                'sap of Cocos nucifera consumed as a community social '
                'and ceremonial beverage. Both traditions use the same '
                'production technology (early-morning climbing and '
                'collection; clay pot or bamboo vessel fermentation; '
                '4–8-hour fresh consumption before over-fermentation); '
                'both document the same production terminology in '
                'their respective languages (neera/kallu in Malayalam; '
                'tua in Tetun — both meaning the fresh sap before '
                'fermentation). The Indian Ocean connection is '
                'documented: Timorese sandalwood traders reached '
                'the Malabar Coast (Kerala) through the Indian Ocean '
                'pre-colonial trade network and brought shared '
                'agricultural technology including palm tapping. '
                'The PCT connects both traditions through the '
                'Portuguese colonial presence in Kerala (Goa) '
                'and Timor simultaneously — the same colonial '
                'administrators who governed Portuguese Timor '
                'also administered Goa, and the palm fermentation '
                'tradition they observed in both territories '
                'was the same Indian Ocean Austronesian heritage.'
            )
        },
        {
            'tradition': 'fermented — Mozambique nipa palm (East Africa — nipa palm, Indian Ocean coast)',
            'beverage': 'Mozambique Nipa Palm Wine — Nypa fruticans, East African Indian Ocean Coast, Colonial Sugar Heritage',
            'connection': (
                'Timor-Leste tua sabu (lontar palm, Borassus flabellifer) '
                'and Mozambique nipa palm wine represent the Indian Ocean '
                'spread of the Borassus palm fermentation tradition '
                'from Southeast Asia (where B. flabellifer is indigenous '
                'to the region spanning from India to Timor through '
                'the Malay Archipelago) to the East African coast '
                '(where the lontar palm was introduced through '
                'Indian Ocean trade). Both use the same production '
                'technology — inflorescence sap collection and '
                'ambient fermentation — and both are consumed '
                'in community ceremony contexts. The Portuguese '
                'colonial connection links both: Portuguese traders '
                'and colonial administrators encountered the '
                'Borassus palm fermentation tradition in both '
                'Timor (tua sabu) and Mozambique (nipa wine) '
                'and documented it in the same colonial period '
                '(16th–17th century). The PCT connects the '
                'two through the Indian Ocean colonial trade '
                'route that linked Lisbon-Mozambique-Goa-Malacca-Timor '
                'as the Portuguese Estado da Índia network.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Tua mutin (fresh 4–8 hours): milky-white to translucent '
            'pale straw — the characteristic colour of coconut sap '
            'in early fermentation, with a fine effervescence from '
            'the active Saccharomyces fermentation; the milky turbidity '
            'comes from the lactic acid bacteria precipitation of '
            'proteins in the palm sap at the pH-drop during '
            'initial fermentation. Tua sabu (lontar, fresh 4–8 hours): '
            'slightly clearer, pale straw to gold — the lontar sap '
            'is less turbid than coconut sap due to lower protein content; '
            'both are consumed from clay cups or carved '
            'coconut shell vessels in the traditional context.'
        ),
        'nose': (
            'Tua mutin at optimal freshness (4–8 hours): '
            'a distinctive volatile aromatic of fermented coconut — '
            'the ethyl esters of the Saccharomyces fermentation '
            '(ethyl acetate, isoamyl acetate) in combination with '
            'the sucrose-derived caramel background of the palm sap; '
            'lactic acid sourness from the co-fermenting Lactobacillus '
            'bacteria provides the characteristic "fresh sourdough" '
            'aromatic that defines Asian palm toddy across the '
            'Austronesian belt; the coconut-specific medium-chain '
            'fatty acids (caprylic, capric, lauric) contribute '
            'a light coconut-cream background note in the sap phase. '
            'Tua sabu: the lontar palm sap is higher in sucrose '
            'and produces a sweeter, more caramel-forward aromatic '
            'with less coconut-fatty character and more '
            'palm sugar sweetness — a distinctly different '
            'aromatic register from the coconut expression.'
        ),
        'palate': (
            'Tua mutin at 2–4% ABV (8–12 hours fermentation): '
            'light to medium body; the entry is gently sweet '
            'from the remaining unfermented sucrose; mid-palate '
            'lactic-sour from the co-fermentation; '
            'the effervescence is soft and natural from '
            'the active CO₂ production of the yeast; '
            'the finish is short (10–15 seconds) and clean '
            'with a mild coconut-acid persistence. '
            'At 4–7% ABV (24-hour tua fermentadu): '
            'more sour, less sweet, more alcohol warmth, '
            'the effervescence has subsided; a nutritional '
            'drink as much as an alcoholic one, consumed '
            'with palm sugar sweetener added for the '
            'higher-ABV expression. Tua sabu: '
            'sweeter and fuller-bodied at equivalent '
            'fermentation stage; the palm-sugar caramel '
            'character persists longer in the mid-palate '
            'finish.'
        ),
        'conclusion': (
            'The most direct expression of the Indian Ocean Austronesian '
            'fermented palm beverage tradition in the PCT architecture — '
            'connecting Timor-Leste\'s pre-colonial cultural heritage '
            'with the Kerala, Mozambique, and Goa nodes of the same '
            'global fermentation network through the Portuguese '
            'colonial maritime trade infrastructure.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Fresh tua sabu collected from the uma lulik (sacred house) '
                'ceremony lontar palms of the interior highlands — the '
                'specific ritual tapping for tara bandu governance '
                'ceremonies or barlaque marriage negotiations where '
                'the quality and freshness of the tua is a point '
                'of ceremonial honour for the host family. '
                'Must be consumed within 2–4 hours of collection; '
                'Brix 14–18°; minimal fermentation; maximum sweetness '
                'and aromatic freshness of the fresh sap. '
                'This tier exists only within the traditional '
                'ceremonial context — no commercial equivalent.'
            ),
            'markers': (
                'Uma lulik ceremony lontar; maximum freshness (2–4 hours); '
                'Brix 14–18°; sweet, minimally fermented; ceremonial context only.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Fresh tua mutin from identified coconut palm groves '
                '(recognised community tappers with established '
                'collection routes); consumed within 4–8 hours '
                'of collection at 1–3% ABV; the optimal daily '
                'consumption stage for the community social drink. '
                'The closest equivalent to an artisan-produced '
                'beverage in the domestic tradition.'
            ),
            'markers': (
                'Known tapper; identified palm grove; 4–8 hours; '
                '1–3% ABV; effervescent; sour-sweet balance.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Market-sold tua from street vendors in Dili and '
                'district towns — sold in repurposed plastic '
                'water bottles or old liquor bottles, fermentation '
                'stage variable (4–16 hours); the domestic '
                'commercial expression of the tua tradition '
                'outside the ceremonial context. Freshness '
                'of the sap cannot be fully verified in '
                'the market context; some over-fermented '
                'examples at 4–6% ABV.'
            ),
            'markers': (
                'Dili street market; plastic bottle; variable '
                'fermentation stage; 1–6% ABV range.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Over-fermented tua fermentadu (24–48 hours, 5–7% ABV) '
                'that has crossed from fresh palm toddy into a sour, '
                'acidic fermented beverage with high volatile acidity '
                '(acetic acid) from the Acetobacter contamination '
                'that inevitably follows extended ambient fermentation. '
                'The acetic acid produces a vinegar-like character '
                'that displaces the fresh palm sweetness and '
                'lactic-sour character of the optimal stage.'
            ),
            'markers': (
                'Over-fermented; 24–48 hours; vinegar-volatile acidity; '
                'Acetobacter contamination; not for programme use.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Fresh tua mutin and tua sabu are consumed at ambient '
            'temperature in the Timorese tradition — the 28–34°C '
            'tropical ambient of the Dili lowlands. For PCT programme '
            'purposes: present the Kerala kallu (the most internationally '
            'accessible close analogue) at 20–22°C (the closest '
            'approximation to tropical ambient without the heat '
            'that would over-volatilise the delicate fermentation '
            'aromatics in a temperate programme setting). '
            'Do not chill — the fermentation aromatics of fresh '
            'palm toddy are suppressed below 18°C, losing '
            'the characteristic effervescence and the lactic '
            'sour-sweet aromatic register.'
        ),
        'vessel': (
            'Traditional service: carved coconut shell (tua mutin) '
            'or clay cup (tua sabu, the ceremonial expression); '
            'in the contemporary Dili market context: plastic cup or '
            'repurposed vessel at ambient temperature. '
            'For PCT programme presentation: a small flat-based '
            'clay cup (100–150ml) at 30–50ml pour serves the '
            'educational context better than a standard wine glass — '
            'the traditional vessel is part of the sensory experience '
            'of a ceremonial fermented palm beverage. Present alongside '
            'Kerala kallu (if available from Indian grocery suppliers) '
            'or a comparable fermented palm product for the '
            'Indian Ocean comparative flight.'
        ),
        'technique': (
            'Consume within 4–8 hours of collection; clay cup or '
            'coconut shell; ambient temperature (22–28°C for programme); '
            '30–50ml tasting pour. The educational context is essential: '
            'the Austronesian Indian Ocean palm fermentation network, '
            'the uma lulik ceremonial use, and the PCT colonial '
            'connection through Timor\'s position in the '
            'Portuguese Estado da Índia trade route.'
        ),
        'programme_position': (
            'PCT Austronesian fermented palm comparative: Timor-Leste '
            'tua alongside Kerala kallu (India), Mozambique nipa '
            '(Africa), and Goa feni base toddy (the distilled '
            'expression of the same tradition) for the four-point '
            'Indian Ocean fermented palm heritage flight that defines '
            'the PCT colonial maritime beverage connection; '
            'or as the fermented beverage bridge connecting '
            'the Asian and African nodes of the PCT trail '
            'through the shared palm fermentation technology.'
        ),
        'verbal_presentation': (
            'This is what the Portuguese found when they arrived in Timor in 1511. '
            'The same palm tree, the same morning climb, the same sap '
            'collected before dawn. They found it in Goa too. And in Mozambique. '
            'The Indian Ocean connected these places before Europe arrived. '
            'This drink is 3,000 years old. '
            'The PCT is, in part, the story of what the Portuguese '
            'found already in place when they got there.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'No commercial international producer of Timorese tua mutin '
            'or tua sabu exists as of 2026. The tradition is entirely '
            'domestic subsistence and ceremonial production. '
            'For programme sourcing of a close analogue: '
            'Kerala coconut toddy (kallu) is available through '
            'Indian grocery and specialty beverage suppliers in '
            'major international cities (Toronto, London, Sydney) '
            'from Keralite-operated suppliers. '
            'For the lontar palm (Borassus flabellifer) toddy parallel: '
            'Indonesian nira saguer (North Sulawesi lontar toddy) '
            'is the closest accessible commercial variant. '
            'The Goa toddy connection: Goa coconut feni '
            '(the distilled version of coconut toddy) '
            'is available internationally through '
            'specialist Indian spirits importers.'
        ),
        'producer_location': 'Nationally distributed; Dili district and rural Timor-Leste',
        'key_person': '[NO COMMERCIAL PRODUCER — traditional community practice]',
        'production_volume': 'Thousands of litres/day nationally during tapping season; entirely domestic',
        'certifications': [],
        'bc_distributor': '[NOT AVAILABLE: no international commercial distribution of Timorese tua as of 2026]',
        'us_distributor': '[NOT AVAILABLE: same as above]',
        'uk_distributor': '[NOT AVAILABLE: same as above — source Kerala kallu through Keralite food suppliers as analogue]',
        'price_tier': 'House',
        'availability_notes': (
            'Timor-Leste tua mutin and tua sabu are not available '
            'internationally and have no commercial export infrastructure. '
            'This entry is documented for its PCT cultural and historical '
            'significance as the Timorese node of the Indian Ocean '
            'Austronesian fermented palm beverage network. '
            'Programme buyers should use Kerala kallu, Goa coconut '
            'toddy, or Mozambique nipa wine as substitute programme '
            'expressions with full Timorese documentation '
            'provided as programme context material.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Timor-Leste tua mutin and tua sabu close the Timor-Leste PCT arc — '
        'the coffee (Ermera, Aileu) and the fermented palm tradition together '
        'constitute the complete Timorese beverage heritage documentation '
        'in the PCT system. The tua tradition predates Portuguese colonial '
        'contact by millennia and was part of the cultural landscape '
        'that the Portuguese found when they established their Timor '
        'trading post in 1511 — alongside sandalwood, beeswax, and '
        'Timor-Hybrido coffee (which postdates colonial contact). '
        'The PCT connection: the same Portuguese Estado da Índia '
        'colonial infrastructure that brought coffee cultivation to '
        'Timor (18th–19th century) encountered and documented the '
        'tua tradition as part of the Timorese agricultural heritage '
        'it was governing. The Indian Ocean Austronesian connection '
        'links Timor to Kerala (Goa, PCT node), Mozambique (PCT node), '
        'and Malacca (PCT node) through the shared palm fermentation '
        'technology that the Portuguese colonial network observed '
        'and documented across all their Indian Ocean territories.'
    ),
    'food_pairings': [
        {
            'technique_id': 'TLS-001',
            'dish': 'Batar daan (Timorese corn and vegetable stew with coconut — the staple traditional Timorese meal)',
            'pairing_type': 'complement',
            'rationale': (
                'Tua mutin alongside batar daan (the Timorese '
                'corn-coconut stew) represents the traditional '
                'subsistence meal of the Timorese highland '
                'agricultural community — the palm sap and '
                'corn starch together constituting the primary '
                'caloric and nutritional intake of the rural '
                'population. The lactic-sweet freshness of '
                'the tua complements the starchy coconut '
                'richness of the batar through the same '
                'acidity-fat complementarity that defines '
                'fermented beverage-starchy food pairings '
                'globally.'
            )
        },
        {
            'technique_id': 'TLS-002',
            'dish': 'Ikan sabuko (Timorese grilled fish with lemon and chili — the coastal coastal community fish preparation)',
            'pairing_type': 'bridge',
            'rationale': (
                'The lactic-sour character of fresh tua mutin '
                'bridges with the lime-chili seasoning of '
                'ikan sabuko through the shared acidic register — '
                'the lactic acid of the fermented palm sap '
                'and the citric acid of the lime both '
                'provide the brightness that cuts through '
                'the fish protein-fat of the grilled coastal '
                'catch; a within-coastline terroir pairing '
                'of the Dili fishing tradition.'
            )
        }
    ],
    'source': 'Gusmão and Ramos Timor-Leste ethnobotanical research (2008–2015); Kammen and Hayashi Timor-Leste colonial agricultural records; FAO Timor-Leste agricultural heritage documentation; Molnar and Monk Timor-Leste biodiversity assessment (palm species); Sheraton International Palms database (Borassus flabellifer distribution); Clarence-Smith Portuguese colonial palm fermentation documentation across the Estado da Índia',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
